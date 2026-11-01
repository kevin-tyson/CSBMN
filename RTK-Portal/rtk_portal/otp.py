# SPDX-License-Identifier: Apache-2.0
"""One-time codes sent by email, for requesters and for staff sign-in.

Codes are six digits, stored only as an HMAC keyed with the portal secret,
expire after RTK_OTP_TTL_MINUTES, allow RTK_OTP_MAX_ATTEMPTS guesses and work
once. Sends are rate-limited per address and per client IP.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
from datetime import timedelta

from . import db

SEND_LIMITS = (  # (window, max sends) per email address
    (timedelta(minutes=15), 3),
    (timedelta(hours=24), 10),
)
IP_LIMIT = (timedelta(hours=1), 30)
FAILURE_CAP = (timedelta(hours=24), 15)  # wrong guesses per address and purpose, across all codes


class RateLimited(Exception):
    pass


class OTPError(Exception):
    pass


def normalize_email(email: str) -> str:
    return (email or "").strip().lower()


def grouping_key(email: str) -> str:
    """One key per person for the queue and the 30-day rule: drops a +tag, and
    Gmail's dots, so jane+1@gmail.com and j.ane@gmail.com count as one requester."""
    email = normalize_email(email)
    local, _, domain = email.partition("@")
    local = local.split("+", 1)[0]
    if domain in ("gmail.com", "googlemail.com"):
        local, domain = local.replace(".", ""), "gmail.com"
    return f"{local}@{domain}"


def looks_like_email(email: str) -> bool:
    email = normalize_email(email)
    if len(email) > 254 or email.count("@") != 1:
        return False
    local, domain = email.split("@")
    return bool(local) and "." in domain and " " not in email and not domain.startswith(".")


def _digest(secret: str, purpose: str, email: str, ref: str, code: str, salt: str) -> str:
    msg = "|".join((purpose, email, ref, code, salt)).encode()
    return hmac.new(secret.encode(), msg, hashlib.sha256).hexdigest()


def issue(conn, secret: str, email: str, purpose: str, ref: str, ttl_minutes: int, ip: str = "") -> str:
    """Create a code and return it in clear text for the mailer. Older unused
    codes for the same purpose and ref are retired."""
    email = normalize_email(email)
    now = db.utcnow()
    for window, limit in SEND_LIMITS:
        n = conn.execute(
            "SELECT COUNT(*) FROM otp WHERE email=? AND purpose=? AND created_at>=?",
            (email, purpose, db.iso(now - window)),
        ).fetchone()[0]
        if n >= limit:
            raise RateLimited("Too many codes sent to this address. Try again later.")
    if ip:
        window, limit = IP_LIMIT
        n = conn.execute(
            "SELECT COUNT(*) FROM otp WHERE ip=? AND created_at>=?", (ip, db.iso(now - window))
        ).fetchone()[0]
        if n >= limit:
            raise RateLimited("Too many codes requested from this connection. Try again later.")
    code = f"{secrets.randbelow(1_000_000):06d}"
    salt = secrets.token_hex(8)
    with db.transaction(conn):
        conn.execute(
            "UPDATE otp SET used_at=? WHERE email=? AND purpose=? AND ref=? AND used_at IS NULL",
            (db.iso(now), email, purpose, ref),
        )
        conn.execute(
            "INSERT INTO otp(email, purpose, ref, salt, code_hash, created_at, expires_at, ip) "
            "VALUES(?,?,?,?,?,?,?,?)",
            (email, purpose, ref, salt, _digest(secret, purpose, email, ref, code, salt),
             db.iso(now), db.iso(now + timedelta(minutes=ttl_minutes)), ip),
        )
    return code


def verify(conn, secret: str, email: str, purpose: str, ref: str, code: str, max_attempts: int) -> None:
    """Raise OTPError unless code is the live code for (email, purpose, ref)."""
    email = normalize_email(email)
    code = "".join(ch for ch in (code or "") if ch.isdigit())
    now = db.utcnow()
    problem = None
    # Record the outcome (attempt count, retirement) and commit it before raising:
    # raising inside the transaction would roll the attempt counter back.
    with db.transaction(conn):
        row = conn.execute(
            "SELECT * FROM otp WHERE email=? AND purpose=? AND ref=? AND used_at IS NULL "
            "ORDER BY pk DESC LIMIT 1",
            (email, purpose, ref),
        ).fetchone()
        window, cap = FAILURE_CAP
        failures = conn.execute(
            "SELECT COALESCE(SUM(attempts), 0) FROM otp WHERE email=? AND purpose=? AND created_at>=?",
            (email, purpose, db.iso(now - window))).fetchone()[0]
        if failures >= cap:
            if row is not None:
                conn.execute("UPDATE otp SET used_at=? WHERE pk=?", (db.iso(now), row["pk"]))
            problem = "Too many wrong codes for this address today. Try again tomorrow."
        elif row is None:
            problem = "No active code. Request a new one."
        elif db.parse_iso(row["expires_at"]) < now:
            conn.execute("UPDATE otp SET used_at=? WHERE pk=?", (db.iso(now), row["pk"]))
            problem = "That code has expired. Request a new one."
        elif row["attempts"] >= max_attempts:
            conn.execute("UPDATE otp SET used_at=? WHERE pk=?", (db.iso(now), row["pk"]))
            problem = "Too many wrong codes. Request a new one."
        else:
            given = _digest(secret, purpose, email, ref, code, row["salt"])
            if len(code) != 6 or not hmac.compare_digest(row["code_hash"], given):
                conn.execute("UPDATE otp SET attempts=attempts+1 WHERE pk=?", (row["pk"],))
                left = max_attempts - row["attempts"] - 1
                problem = f"That code is not right. {max(left, 0)} tries left."
            else:
                conn.execute("UPDATE otp SET used_at=? WHERE pk=?", (db.iso(now), row["pk"]))
    if problem:
        raise OTPError(problem)
