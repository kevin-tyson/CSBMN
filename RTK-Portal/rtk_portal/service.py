# SPDX-License-Identifier: Apache-2.0
"""What the portal does, independent of HTTP: file, verify, queue, triage,
review, send, publish.

Queue rule. When a request is verified it gets a round: 1 if its requester has
no other request outstanding, 2 if they have one, and so on. The portal always
takes the waiting request with the lowest round, and within a round the one
received first. So a requester's second through nth requests wait until every
other requester's earlier requests have been handled, and two heavy users
alternate rather than one blocking the other.

One request at a time. A request is active from the moment triage starts until
staff send a response or close it. While one is active, no other is taken from
the queue. The only exception is the five-business-day acknowledgment staff can
send for a waiting request, because RSA 91-A:4, IV(b) runs whatever the queue
says; it does not change the request's place.
"""

from __future__ import annotations

import json
import logging
import re
import secrets
import textwrap
import threading
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from . import db, otp, privacy, triage
from .bizdays import Calendar
from .kg import KG
from .mailer import Mailer
from .triage import drafts

log = logging.getLogger("rtk.service")

OUTSTANDING = ("queued", "triage", "review")
ACTIVE = ("triage", "review")
PLACEHOLDER = re.compile(r"\[\[|\]\]")


class PortalError(Exception):
    """A user-facing error with a message safe to show."""


class Portal:
    def __init__(self, settings, mailer=None, kg=None, client=None):
        self.s = settings
        db.init(settings.db_path)
        self.kg = kg or KG(settings.kg_path)
        self.mailer = mailer or Mailer(settings)
        self.client = client
        self.tz = ZoneInfo(settings.timezone)
        self._lock = threading.Lock()
        self._wake = threading.Event()
        self._stop = threading.Event()
        self._worker: threading.Thread | None = None

    # ------------------------------------------------------------ helpers

    def conn(self):
        return db.connect(self.s.db_path)

    def calendar(self, conn) -> Calendar:
        rows = conn.execute("SELECT day, is_open FROM calendar").fetchall()
        return Calendar({date.fromisoformat(r["day"]): bool(r["is_open"]) for r in rows})

    def local(self, iso_s: str | None) -> datetime | None:
        dt = db.parse_iso(iso_s)
        return dt.astimezone(self.tz) if dt else None

    def today(self) -> date:
        return datetime.now(self.tz).date()

    def log_url(self, public_id: str) -> str:
        return f"{self.s.base_url}/log/{public_id}"

    @staticmethod
    def fmt_date(d: date | None) -> str:
        return f"{d:%B} {d.day}, {d.year}" if d else ""

    def salutation(self, row) -> str:
        return (row["requester_name"] or "").strip() or "Requester"

    def display_name(self, row) -> str:
        if row["publish_name"] and (row["requester_name"] or "").strip():
            return row["requester_name"].strip()
        return "Requester"

    def draft_context(self, row) -> dict:
        received = self.local(row["received_at"])
        return {
            "public_id": row["public_id"],
            "received": self.fmt_date(received.date()) if received else "",
            "due": self.fmt_date(date.fromisoformat(row["due_date"])) if row["due_date"] else "",
            "salutation": self.salutation(row),
            "text": row["text"],
            "log_url": self.log_url(row["public_id"]),
        }

    def _mail(self, to: str, subject: str, body: str) -> None:
        try:
            self.mailer.send(to, subject, body)
        except Exception as e:
            log.exception("mail to %s failed", to)
            raise PortalError(f"The email could not be sent ({type(e).__name__}). Nothing was changed; try again "
                              "or check the mail settings.")

    def get(self, conn, pk=None, public_id=None, token=None):
        if pk is not None:
            return conn.execute("SELECT * FROM requests WHERE pk=?", (pk,)).fetchone()
        if public_id is not None:
            return conn.execute("SELECT * FROM requests WHERE public_id=?", (public_id,)).fetchone()
        return conn.execute("SELECT * FROM requests WHERE pending_token=?", (token,)).fetchone()

    # ------------------------------------------------------------ filing

    def file_request(self, email: str, name: str, publish_name: bool, text: str, ip: str = "") -> str:
        email = otp.normalize_email(email)
        text = (text or "").strip()
        name = (name or "").strip()[:120]
        if not otp.looks_like_email(email):
            raise PortalError("Enter a valid email address.")
        if len(text) < 15:
            raise PortalError("Describe the records you want in a sentence or more.")
        if len(text) > self.s.max_request_chars:
            raise PortalError(f"Keep the request under {self.s.max_request_chars} characters, or split it.")
        token = secrets.token_urlsafe(18)
        conn = self.conn()
        try:
            n = conn.execute("SELECT COUNT(*) FROM requests WHERE client_ip=? AND created_at>=?",
                             (ip, db.iso(db.utcnow() - timedelta(hours=1)))).fetchone()[0] if ip else 0
            if n >= 20:
                raise PortalError("Too many requests from this connection in the last hour. Try again later.")
            with db.transaction(conn):
                cur = conn.execute(
                    "INSERT INTO requests(pending_token, requester_email, requester_name, publish_name, text, status,"
                    " created_at, client_ip) VALUES(?,?,?,?,?,?,?,?)",
                    (token, email, name or None, 1 if publish_name else 0, text, "pending_verification",
                     db.iso(db.utcnow()), ip))
                db.audit(conn, cur.lastrowid, "filed", "requester", {"email": email})
            self._send_code(conn, email, token, ip)
        finally:
            conn.close()
        return token

    def _send_code(self, conn, email, token, ip):
        try:
            code = otp.issue(conn, self.s.secret_key, email, "request", token, self.s.otp_ttl_minutes, ip)
        except otp.RateLimited as e:
            raise PortalError(str(e))
        self._mail(email, "Your Right-to-Know request verification code",
                         f"Your verification code is {code}\n\n"
                         f"Enter it on the verification page within {self.s.otp_ttl_minutes} minutes to file your "
                         f"request with the {self.s.district_name}. Your request is not filed until you do.\n\n"
                         "If you did not ask for this code, ignore this message.\n")

    def resend_code(self, token: str, ip: str = "") -> None:
        conn = self.conn()
        try:
            row = self.get(conn, token=token)
            if row is None or row["status"] != "pending_verification":
                raise PortalError("This request is not waiting for verification.")
            self._send_code(conn, row["requester_email"], token, ip)
        finally:
            conn.close()

    def verify_request(self, token: str, code: str) -> str:
        conn = self.conn()
        try:
            row = self.get(conn, token=token)
            if row is None or row["status"] != "pending_verification":
                raise PortalError("This request is not waiting for verification.")
            try:
                otp.verify(conn, self.s.secret_key, row["requester_email"], "request", token, code,
                           self.s.otp_max_attempts)
            except otp.OTPError as e:
                raise PortalError(str(e))
            now = db.utcnow()
            local_day = now.astimezone(self.tz).date()
            hold, reasons, masked = privacy.screen(row["text"])
            with db.transaction(conn):
                cal = self.calendar(conn)
                due = cal.add_business_days(local_day, 5)
                year = local_day.year
                n = db.next_counter(conn, f"rtk-{year}")
                public_id = f"RTK-{year}-{n:04d}"
                key = otp.grouping_key(row["requester_email"])
                outstanding = conn.execute(
                    "SELECT COUNT(*) FROM requests WHERE requester_key=? AND status IN (?,?,?)",
                    (key, *OUTSTANDING)).fetchone()[0]
                rnd = outstanding + 1
                conn.execute(
                    "UPDATE requests SET public_id=?, status='queued', received_at=?, due_date=?, queue_round=?,"
                    " public_text=?, text_held=?, held_reasons=?, pending_token=NULL, requester_key=? WHERE pk=?",
                    (public_id, db.iso(now), due.isoformat(), rnd, None if hold else masked, 1 if hold else 0,
                     json.dumps(reasons) if hold else None, key, row["pk"]))
                db.log_event(conn, public_id, "received", "portal", {
                    "received_at": db.iso(now), "due_date": due.isoformat(), "queue_round": rnd,
                    "requester": self.display_name(row), "text": None if hold else masked, "text_held": hold,
                    "held_reasons": reasons if hold else [],
                })
                db.audit(conn, row["pk"], "verified", "requester", {"email": row["requester_email"]})
            pos = self.position(conn, public_id)
            new = self.get(conn, pk=row["pk"])
        finally:
            conn.close()
        self._send_receipt(new, pos)
        self.kick()
        return public_id

    def _send_receipt(self, row, pos):
        ctx = self.draft_context(row)
        place = f"It is number {pos} in the queue." if pos else "It is being reviewed now."
        held = ("\n\nTo protect privacy, the text of your request is held back from the public log until staff "
                "review it. The request's dates and status are public now." if row["text_held"] else "")
        body = (f"The {self.s.district_name} received your Right-to-Know request {row['public_id']} on "
                f"{ctx['received']}. {place}\n\n"
                f"Under RSA 91-A:4, IV(b) the District must make the records available, deny the request, or tell "
                f"you in writing how much time it needs, within five business days: by {ctx['due']}.\n\n"
                f"Follow the request in the public log: {ctx['log_url']}{held}\n\n"
                "Requests are handled one at a time, in order of receipt, with each requester's first "
                "outstanding request ahead of anyone's second.\n")
        try:
            self.mailer.send(row["requester_email"], f"Right-to-Know request {row['public_id']} received", body)
        except Exception:
            log.exception("receipt email failed for %s", row["public_id"])

    # ------------------------------------------------------------ queue

    def queue(self, conn) -> list:
        return conn.execute(
            "SELECT * FROM requests WHERE status='queued' ORDER BY queue_round, received_at, pk").fetchall()

    def active(self, conn):
        return conn.execute("SELECT * FROM requests WHERE status IN (?,?) ORDER BY pk LIMIT 1", ACTIVE).fetchone()

    def position(self, conn, public_id: str) -> int | None:
        for i, r in enumerate(self.queue(conn), 1):
            if r["public_id"] == public_id:
                return i
        return None

    def kick(self) -> None:
        """Ask the worker to advance the queue. With RTK_START_WORKER=false (tests)
        the queue advances inline instead."""
        if self.s.start_worker:
            self._wake.set()
        else:
            self.advance()

    def start_worker(self) -> None:
        if self._worker is None or not self._worker.is_alive():
            self._worker = threading.Thread(target=self._run, name="rtk-worker", daemon=True)
            self._worker.start()

    def stop_worker(self) -> None:
        self._stop.set()
        self._wake.set()

    def _run(self) -> None:
        # One thread does all queue work. A kick that arrives while it is busy
        # leaves the event set, so the loop runs again; the timeout is a backstop.
        while not self._stop.is_set():
            self._wake.wait(timeout=30)
            self._wake.clear()
            try:
                self.advance()
            except Exception:
                log.exception("queue advance failed")

    def advance(self) -> None:
        """Take the next request if the active slot is free, and triage it."""
        with self._lock:
            pk = self._claim_next()
            if pk is not None:
                self._triage(pk)

    def _claim_next(self):
        conn = self.conn()
        try:
            with db.transaction(conn):
                act = self.active(conn)
                if act is not None:
                    return act["pk"] if act["status"] == "triage" and not act["triage_json"] else None
                q = self.queue(conn)
                if not q:
                    return None
                nxt = q[0]
                conn.execute("UPDATE requests SET status='triage', triage_started_at=? WHERE pk=?",
                             (db.iso(db.utcnow()), nxt["pk"]))
                db.log_event(conn, nxt["public_id"], "triage_started", "portal", {})
                return nxt["pk"]
        finally:
            conn.close()

    def _triage(self, pk: int, forced: str | None = None, actor: str = "portal") -> dict:
        conn = self.conn()
        try:
            row = self.get(conn, pk=pk)
            ctx = self.draft_context(row)
            try:
                result = triage.run(dict(row), ctx, self.s, self.kg, forced=forced, client=self.client,
                                    today=self.today())
            except Exception as e:
                log.exception("triage failed for %s", row["public_id"])
                result = {"engine": "none", "category": "records_search", "confidence": "low", "reasons": [],
                          "review_notes": [f"Triage failed ({type(e).__name__}: {e}). Write the response by hand."],
                          "signals": {}, "kg": {}, "hits": [], "all_hits": [], "prompt": "",
                          "draft": {"subject": f"Right-to-Know request {row['public_id']}", "body": "[[write the response]]"}}
            since = db.iso(db.utcnow() - timedelta(days=30))
            others = conn.execute(
                "SELECT public_id FROM requests WHERE requester_key=? AND pk<>? AND public_id IS NOT NULL"
                " AND received_at>=? ORDER BY received_at", (row["requester_key"], pk, since)).fetchall()
            if others:
                result["review_notes"].append(
                    "The same requester filed " + ", ".join(o["public_id"] for o in others) + " in the last 30 "
                    "days. Check for duplicates; for the 250-communication threshold, RSA 91-A:4, VIII and "
                    "Procedure EH-R(1) count one person's requests within 30 days as one.")
            with db.transaction(conn):
                first = row["status"] == "triage"
                conn.execute(
                    "UPDATE requests SET status='review', triaged_at=?, category=?, triage_json=?, draft_subject=?,"
                    " draft_body=? WHERE pk=?",
                    (db.iso(db.utcnow()), result["category"], json.dumps(result), result["draft"]["subject"],
                     result["draft"]["body"], pk))
                if first:
                    db.log_event(conn, row["public_id"], "ready_for_review", "portal", {"engine": result["engine"]})
                db.audit(conn, pk, "triaged", actor, {"category": result["category"], "engine": result["engine"],
                                                     "forced": forced})
            return result
        finally:
            conn.close()

    def recover(self) -> None:
        """At startup: finish a triage interrupted by a crash, then advance."""
        self.expire_pending()
        if self.s.start_worker:
            self.start_worker()
        self.kick()

    def expire_pending(self) -> int:
        """Delete unverified requests and spent codes; if RTK_CONTACT_RETENTION_DAYS
        is set, replace the email address of requests closed longer ago than that."""
        conn = self.conn()
        try:
            cutoff = db.iso(db.utcnow() - timedelta(hours=self.s.pending_ttl_hours))
            with db.transaction(conn):
                cur = conn.execute("DELETE FROM requests WHERE status='pending_verification' AND created_at<?", (cutoff,))
                conn.execute("DELETE FROM otp WHERE created_at<?", (db.iso(db.utcnow() - timedelta(days=7)),))
                if self.s.contact_retention_days > 0:
                    old = db.iso(db.utcnow() - timedelta(days=self.s.contact_retention_days))
                    gone = [r["pk"] for r in conn.execute(
                        "SELECT pk FROM requests WHERE status='closed' AND closed_at<? AND requester_email NOT LIKE"
                        " 'removed:%'", (old,))]
                    for pk in gone:
                        conn.execute("UPDATE requests SET requester_email='removed:' || pk, client_ip=NULL WHERE pk=?", (pk,))
                        conn.execute("UPDATE audit SET data='{}' WHERE request_pk=? AND type IN ('filed','verified')", (pk,))
            return cur.rowcount
        finally:
            conn.close()

    # ------------------------------------------------------------ staff

    def is_staff(self, email: str) -> bool:
        return otp.normalize_email(email) in self.s.staff_emails

    def staff_login_start(self, email: str, ip: str = "") -> None:
        email = otp.normalize_email(email)
        if not self.is_staff(email):
            return  # same response either way, so the form does not reveal who is staff
        conn = self.conn()
        try:
            try:
                code = otp.issue(conn, self.s.secret_key, email, "staff", "login", self.s.otp_ttl_minutes, ip)
            except otp.RateLimited as e:
                raise PortalError(str(e))
            db.audit(conn, None, "staff_code_sent", email, {})
        finally:
            conn.close()
        self._mail(email, "RTK Portal staff sign-in code",
                         f"Your sign-in code is {code}. It expires in {self.s.otp_ttl_minutes} minutes.\n")

    def staff_login_verify(self, email: str, code: str) -> None:
        email = otp.normalize_email(email)
        if not self.is_staff(email):
            raise PortalError("That code is not right.")
        conn = self.conn()
        try:
            try:
                otp.verify(conn, self.s.secret_key, email, "staff", "login", code, self.s.otp_max_attempts)
            except otp.OTPError as e:
                raise PortalError(str(e))
            db.audit(conn, None, "staff_login", email, {})
        finally:
            conn.close()

    def save_draft(self, pk: int, subject: str, body: str, public_text: str | None, actor: str) -> None:
        conn = self.conn()
        try:
            row = self.get(conn, pk=pk)
            if row is None or row["status"] != "review":
                raise PortalError("Only the request under review can be edited.")
            with db.transaction(conn):
                conn.execute("UPDATE requests SET draft_subject=?, draft_body=?, reviewer=? WHERE pk=?",
                             (subject, body, actor, pk))
                db.audit(conn, pk, "draft_saved", actor, {"subject": subject})
            if public_text is not None:
                self._set_public_text(conn, row, public_text, actor)
        finally:
            conn.close()

    def _set_public_text(self, conn, row, public_text: str, actor: str) -> None:
        public_text = privacy.mask(public_text.strip())
        if not public_text or public_text == (row["public_text"] or ""):
            return
        with db.transaction(conn):
            conn.execute("UPDATE requests SET public_text=?, text_held=0 WHERE pk=?", (public_text, row["pk"]))
            db.log_event(conn, row["public_id"], "text_published", "custodian", {"text": public_text})
            db.audit(conn, row["pk"], "text_published", actor, {})

    def retriage(self, pk: int, forced: str | None, actor: str) -> dict:
        conn = self.conn()
        try:
            row = self.get(conn, pk=pk)
            if row is None or row["status"] != "review":
                raise PortalError("Only the request under review can be re-triaged.")
        finally:
            conn.close()
        return self._triage(pk, forced=forced or None, actor=actor)

    def _scrub(self, row, text: str) -> str:
        """Remove the requester's email and, unless they consented, their name."""
        text = re.sub(re.escape(row["requester_email"]), "[email removed]", text, flags=re.I)
        name = (row["requester_name"] or "").strip()
        if name and not row["publish_name"]:
            text = re.sub(r"(?m)^(Dear )[^\n,]+,", r"\1Requester,", text)
            text = re.sub(r"\b" + re.escape(name) + r"\b", "Requester", text, flags=re.I)
            for part in re.split(r"[\s,]+", name):
                part = part.strip(".")
                if len(part) >= 3 and part.lower() not in ("the", "and", "mrs", "miss"):
                    text = re.sub(r"\b" + re.escape(part) + r"\b", "[name removed]", text, flags=re.I)
        return privacy.mask(text)

    def _public_search(self, row) -> str:
        """The repeat-search section rebuilt from the request's public text, so the
        published copy never carries words from a held or unmasked request."""
        if row["text_held"] or not row["public_text"]:
            return "To repeat this search yourself: [search details withheld for privacy]\n"
        from .triage import rules
        sig = rules.extract_signals(row["public_text"], self.today())
        q = " ".join(sig.terms[:16])
        url = rules.search_url(self.s.base_url, q, sig.date_from, sig.date_to)
        prompt = rules.reproducible_prompt(row["public_text"], sig, self.s)
        return ("To repeat this search yourself:\n- Meeting Navigator search: " + url + "\n"
                "- Or give this prompt to an AI assistant that can read the public knowledge graph:\n"
                + "\n".join("  " + w for w in textwrap.wrap('"' + prompt + '"', 76)) + "\n")

    def public_copy(self, row, body: str) -> str:
        """The version of a sent message that goes in the public log."""
        quoted = drafts._quote(row["public_text"]) if (row["public_text"] and not row["text_held"]) \
            else "> [request text withheld for privacy]"
        out, in_quote = [], False
        for line in body.splitlines():
            if line.startswith(">"):
                if not in_quote:
                    out.append(quoted)
                    in_quote = True
                continue
            in_quote = False
            out.append(line)
        text = "\n".join(out) + "\n"
        # Replace the whole "To repeat this search yourself" block (heading plus its
        # indented or bulleted lines), then any stray search link elsewhere.
        block = re.compile(r"To repeat this search yourself:[^\n]*\n(?:(?:- |  )[^\n]*\n)*")
        if block.search(text):
            text = block.sub(lambda m: self._public_search(row), text, count=1)
        text = re.sub(r"\S*/kg/search\?\S+", "[search link removed; see the log entry for the public search]", text)
        return self._scrub(row, text).rstrip("\n")

    def public_subject(self, row, subject: str) -> str:
        if row["text_held"] or row["held_reasons"]:
            return f"Right-to-Know request {row['public_id']}: response"
        return self._scrub(row, subject)

    def send_response(self, pk: int, subject: str, body: str, public_text: str | None, actor: str) -> None:
        if PLACEHOLDER.search(subject + body):
            raise PortalError("The draft still has [[...]] placeholders. Fill them in or delete them before sending.")
        if not body.strip() or not subject.strip():
            raise PortalError("The response needs a subject and a body.")
        conn = self.conn()
        try:
            row = self.get(conn, pk=pk)
            if row is None or row["status"] != "review":
                raise PortalError("Only the request under review can be answered.")
            if public_text is not None:
                self._set_public_text(conn, row, public_text, actor)
                row = self.get(conn, pk=pk)
            self._mail(row["requester_email"], subject, body)
            now = db.iso(db.utcnow())
            with db.transaction(conn):
                conn.execute(
                    "UPDATE requests SET status='closed', close_reason='responded', sent_subject=?, sent_body=?,"
                    " sent_at=?, closed_at=?, reviewer=? WHERE pk=?", (subject, body, now, now, actor, pk))
                db.log_event(conn, row["public_id"], "response_sent", "custodian", {
                    "category": row["category"], "subject": self.public_subject(row, subject),
                    "body": self.public_copy(row, body)})
                db.log_event(conn, row["public_id"], "closed", "custodian", {"reason": "responded"})
                db.audit(conn, pk, "response_sent", actor, {"subject": subject})
        finally:
            conn.close()
        self.kick()

    def close_without_response(self, pk: int, reason: str, note: str, actor: str) -> None:
        if reason not in ("withdrawn", "duplicate", "abandoned"):
            raise PortalError("Choose a reason.")
        conn = self.conn()
        try:
            row = self.get(conn, pk=pk)
            if row is None or row["status"] not in OUTSTANDING:
                raise PortalError("This request is not open.")
            now = db.iso(db.utcnow())
            with db.transaction(conn):
                conn.execute("UPDATE requests SET status='closed', close_reason=?, closed_at=?, reviewer=? WHERE pk=?",
                             (reason, now, actor, pk))
                db.log_event(conn, row["public_id"], "closed", "custodian",
                             {"reason": reason, "note": privacy.mask(note.strip())[:500]})
                db.audit(conn, pk, "closed", actor, {"reason": reason})
        finally:
            conn.close()
        self.kick()

    def ack_draft(self, pk: int) -> tuple[str, str]:
        conn = self.conn()
        try:
            row = self.get(conn, pk=pk)
            return drafts.acknowledgment(self.draft_context(row), self.s)
        finally:
            conn.close()

    def send_ack(self, pk: int, subject: str, body: str, actor: str) -> None:
        if PLACEHOLDER.search(subject + body):
            raise PortalError("The acknowledgment still has [[...]] placeholders.")
        conn = self.conn()
        try:
            row = self.get(conn, pk=pk)
            if row is None or row["status"] not in OUTSTANDING:
                raise PortalError("This request is not open.")
            self._mail(row["requester_email"], subject, body)
            now = db.iso(db.utcnow())
            with db.transaction(conn):
                conn.execute("UPDATE requests SET ack_sent_at=COALESCE(ack_sent_at, ?) WHERE pk=?", (now, pk))
                db.log_event(conn, row["public_id"], "acknowledgment_sent", "custodian",
                             {"subject": self.public_subject(row, subject), "body": self.public_copy(row, body)})
                db.audit(conn, pk, "ack_sent", actor, {})
        finally:
            conn.close()

    def set_calendar(self, day: date, is_open: bool | None, note: str, actor: str) -> None:
        conn = self.conn()
        try:
            with db.transaction(conn):
                if is_open is None:
                    conn.execute("DELETE FROM calendar WHERE day=?", (day.isoformat(),))
                else:
                    conn.execute("INSERT INTO calendar(day, is_open, note) VALUES(?,?,?) ON CONFLICT(day) DO UPDATE"
                                 " SET is_open=excluded.is_open, note=excluded.note",
                                 (day.isoformat(), 1 if is_open else 0, note[:200]))
                db.log_event(conn, None, "calendar_changed", "custodian",
                             {"day": day.isoformat(), "office": None if is_open is None else ("open" if is_open else "closed"),
                              "note": note[:200]})
                db.audit(conn, None, "calendar", actor, {"day": day.isoformat(), "is_open": is_open})
        finally:
            conn.close()

    # ------------------------------------------------------------ public views

    STATUS = {"queued": "Waiting", "triage": "In triage", "review": "In staff review", "closed": "Closed"}
    CLOSE = {"responded": "Responded", "withdrawn": "Withdrawn", "duplicate": "Closed as duplicate",
             "abandoned": "Closed"}

    def public_row(self, conn, row, cal: Calendar, positions: dict) -> dict:
        received = self.local(row["received_at"])
        due = date.fromisoformat(row["due_date"]) if row["due_date"] else None
        first = [x for x in (row["ack_sent_at"], row["sent_at"]) if x]
        first_resp = min(self.local(x) for x in first) if first else None
        end_day = first_resp.date() if first_resp else self.today()
        elapsed = cal.business_days_elapsed(received.date(), end_day) if received else None
        status = self.STATUS.get(row["status"], row["status"])
        if row["status"] == "closed":
            status = self.CLOSE.get(row["close_reason"], "Closed")
        elif row["status"] == "queued":
            status = f"Waiting, number {positions.get(row['public_id'], '?')}"
        return {
            "public_id": row["public_id"],
            "received": received,
            "due": due,
            "status": status,
            "state": row["status"],
            "round": row["queue_round"],
            "requester": self.display_name(row),
            "text": row["public_text"],
            "text_held": bool(row["text_held"]),
            "category": row["category"] if row["status"] == "closed" and row["close_reason"] == "responded" else None,
            "first_response": first_resp,
            "business_days": elapsed,
            "on_time": (first_resp.date() <= due) if (first_resp and due) else (None if not due or self.today() <= due else False),
            "closed": self.local(row["closed_at"]),
        }

    def public_log(self, state: str | None = None, limit: int = 500) -> list[dict]:
        conn = self.conn()
        try:
            cal = self.calendar(conn)
            positions = {r["public_id"]: i for i, r in enumerate(self.queue(conn), 1)}
            sql = "SELECT * FROM requests WHERE public_id IS NOT NULL"
            args: list = []
            if state == "open":
                sql += " AND status IN (?,?,?)"
                args += list(OUTSTANDING)
            elif state == "closed":
                sql += " AND status='closed'"
            sql += " ORDER BY received_at DESC LIMIT ?"
            args.append(limit)
            return [self.public_row(conn, r, cal, positions) for r in conn.execute(sql, args)]
        finally:
            conn.close()

    def public_detail(self, public_id: str) -> dict | None:
        conn = self.conn()
        try:
            row = self.get(conn, public_id=public_id)
            if row is None:
                return None
            cal = self.calendar(conn)
            positions = {r["public_id"]: i for i, r in enumerate(self.queue(conn), 1)}
            d = self.public_row(conn, row, cal, positions)
            d["events"] = [dict(e) | {"data": json.loads(e["data"]), "at_local": self.local(e["at"])}
                           for e in conn.execute("SELECT * FROM events WHERE request_id=? ORDER BY seq", (public_id,))]
            return d
        finally:
            conn.close()

    def events(self, since: int = 0) -> list[dict]:
        conn = self.conn()
        try:
            return [dict(e) for e in conn.execute("SELECT * FROM events WHERE seq>? ORDER BY seq", (since,))]
        finally:
            conn.close()

    def stats(self) -> dict:
        conn = self.conn()
        try:
            r = conn.execute(
                "SELECT COUNT(*) total, SUM(status IN ('queued','triage','review')) open,"
                " SUM(status='closed') closed FROM requests WHERE public_id IS NOT NULL").fetchone()
            return dict(r)
        finally:
            conn.close()
