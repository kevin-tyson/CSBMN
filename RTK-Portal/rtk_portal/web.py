# SPDX-License-Identifier: Apache-2.0
"""HTTP layer (Starlette). Run with:

    uvicorn rtk_portal.web:app --host 127.0.0.1 --port 8091

Run one worker process: the single active-request rule is enforced with a
database lock, but triage runs on a thread inside the process.
"""

from __future__ import annotations

import csv
import io
import ipaddress
import json
import secrets
from contextlib import asynccontextmanager
from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup, escape
from starlette.applications import Starlette
from starlette.concurrency import run_in_threadpool
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, Response
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from . import __version__, db, law
from .config import Settings
from .service import Portal, PortalError

HERE = Path(__file__).parent
STAFF_SESSION_HOURS = 8


def create_app(settings: Settings | None = None, portal: Portal | None = None) -> Starlette:
    settings = settings or Settings.from_env()
    portal = portal or Portal(settings)
    env = Environment(loader=FileSystemLoader(str(HERE / "templates")),
                      autoescape=select_autoescape(["html"]), trim_blocks=True, lstrip_blocks=True)

    def fdate(d):
        if not d:
            return ""
        if isinstance(d, str):
            d = date.fromisoformat(d[:10])
        return f"{d:%b} {d.day}, {d.year}"

    def fdatetime(dt):
        if not dt:
            return ""
        return f"{dt:%b} {dt.day}, {dt.year}, {dt:%I:%M %p}".replace(" 0", " ")

    def snippet(s):
        s = escape(s or "")
        return Markup(str(s).replace("\x02", "<mark>").replace("\x03", "</mark>"))

    env.filters.update(fdate=fdate, fdatetime=fdatetime, snippet=snippet,
                       tojson_pretty=lambda o: json.dumps(o, indent=2, ensure_ascii=False))
    env.globals.update(settings=settings, version=__version__, categories=law.CATEGORIES, citations=law.CITATIONS)

    def client_ip(request: Request) -> str:
        if settings.trust_proxy:
            # The rightmost entry is the one our own proxy appended; anything to
            # its left came from the client and can be forged.
            fwd = request.headers.get("x-forwarded-for", "")
            if fwd:
                return fwd.split(",")[-1].strip()
        return request.client.host if request.client else ""

    def csrf(request: Request) -> str:
        tok = request.session.get("csrf")
        if not tok:
            tok = secrets.token_urlsafe(24)
            request.session["csrf"] = tok
        return tok

    async def form_checked(request: Request):
        form = await request.form()
        if not secrets.compare_digest(str(form.get("csrf", "")), request.session.get("csrf", "") or "x"):
            raise PortalError("Your session expired. Reload the page and try again.")
        return form

    def staff(request: Request) -> str | None:
        email = request.session.get("staff")
        exp = request.session.get("staff_exp", 0)
        if email and exp > db.utcnow().timestamp() and portal.is_staff(email):
            return email
        return None

    def render(request: Request, name: str, status: int = 200, **ctx) -> HTMLResponse:
        ctx.setdefault("staff_user", staff(request))
        html = env.get_template(name).render(request=request, csrf=csrf(request), **ctx)
        return HTMLResponse(html, status_code=status)

    def error(request, msg, status=400):
        return render(request, "message.html", status=status, title="Something went wrong", message=msg)

    # ------------------------------------------------------------ public

    async def home(request):
        return render(request, "home.html", stats=portal.stats(), kg=portal.kg.meta())

    async def about(request):
        return render(request, "about.html")

    async def request_form(request):
        if request.method == "GET":
            return render(request, "request_form.html", form={})
        try:
            form = await form_checked(request)
        except PortalError as e:
            return error(request, str(e))
        data = {k: str(form.get(k, "")) for k in ("email", "name", "text")}
        data["publish_name"] = form.get("publish_name") == "on"
        if form.get("ack") != "on":
            return render(request, "request_form.html", status=400, form=data,
                          error="Confirm that you have read how the portal publishes requests.")
        if form.get("website"):  # honeypot field, hidden from people
            return RedirectResponse("/", status_code=303)
        try:
            token = await run_in_threadpool(portal.file_request, data["email"], data["name"],
                                            data["publish_name"], data["text"], client_ip(request))
        except PortalError as e:
            return render(request, "request_form.html", status=400, form=data, error=str(e))
        return RedirectResponse(f"/verify/{token}", status_code=303)

    async def verify(request):
        token = request.path_params["token"]
        conn = portal.conn()
        try:
            row = portal.get(conn, token=token)
        finally:
            conn.close()
        if row is None:
            return error(request, "This verification link has expired or was already used.", 404)
        masked = row["requester_email"]
        local, _, domain = masked.partition("@")
        masked = (local[:2] + "***@" + domain) if local else masked
        if request.method == "GET":
            return render(request, "verify.html", token=token, email=masked)
        try:
            form = await form_checked(request)
            if form.get("action") == "resend":
                await run_in_threadpool(portal.resend_code, token, client_ip(request))
                return render(request, "verify.html", token=token, email=masked, notice="A new code is on its way.")
            public_id = await run_in_threadpool(portal.verify_request, token, str(form.get("code", "")))
        except PortalError as e:
            return render(request, "verify.html", status=400, token=token, email=masked, error=str(e))
        return RedirectResponse(f"/log/{public_id}?filed=1", status_code=303)

    async def log_list(request):
        state = request.query_params.get("state")
        rows = portal.public_log(state if state in ("open", "closed") else None)
        return render(request, "log_list.html", rows=rows, state=state)

    async def log_detail(request):
        d = portal.public_detail(request.path_params["public_id"])
        if d is None:
            return error(request, "No request has that number.", 404)
        return render(request, "log_detail.html", r=d, filed=request.query_params.get("filed") == "1")

    def _export_rows():
        out = []
        for r in portal.public_log(limit=100000):
            out.append({
                "id": r["public_id"], "received": r["received"].isoformat() if r["received"] else None,
                "due": r["due"].isoformat() if r["due"] else None, "status": r["status"], "queue_round": r["round"],
                "requester": r["requester"], "text": r["text"], "text_held": r["text_held"],
                "category": r["category"],
                "first_response": r["first_response"].isoformat() if r["first_response"] else None,
                "business_days_to_first_response": r["business_days"] if r["first_response"] else None,
                "on_time": r["on_time"],
                "closed": r["closed"].isoformat() if r["closed"] else None,
            })
        return out

    async def log_json(request):
        return JSONResponse({"generated": db.iso(db.utcnow()), "requests": _export_rows()})

    async def log_csv(request):
        rows = _export_rows()
        buf = io.StringIO()
        fields = list(rows[0].keys()) if rows else ["id"]
        w = csv.DictWriter(buf, fieldnames=fields)
        w.writeheader()
        for row in rows:
            # A cell starting with = + - @ would run as a formula in a spreadsheet.
            w.writerow({k: ("'" + v if isinstance(v, str) and v[:1] in "=+-@\t\r" else v) for k, v in row.items()})
        return Response(buf.getvalue(), media_type="text/csv",
                        headers={"Content-Disposition": "attachment; filename=rtk-log.csv"})

    async def events_json(request):
        try:
            since = int(request.query_params.get("since", "0"))
        except ValueError:
            since = 0
        ev = portal.events(since)
        ok, bad = db.verify_chain(portal.events(0))
        return JSONResponse({"chain_ok": ok, "first_bad_seq": bad, "genesis": db.GENESIS,
                             "hash_rule": ("hex(sha256(utf8(prev_hash + json.dumps({request_id, at, type, actor, data}, "
                                           "sort_keys=True, separators=(',', ':'), ensure_ascii=False))))"),
                             "events": [e | {"data": json.loads(e["data"])} for e in ev]})

    async def log_head(request):
        ev = portal.events(0)
        head = ev[-1] if ev else None
        return JSONResponse({"seq": head["seq"] if head else 0, "hash": head["hash"] if head else db.GENESIS,
                             "at": head["at"] if head else None, "generated": db.iso(db.utcnow())})

    async def kg_search(request):
        qp = request.query_params
        q = qp.get("q", "").strip()[:300]
        kinds = [k for k in qp.getlist("kind") if k]
        d1, d2 = qp.get("from") or None, qp.get("to") or None
        hits = portal.kg.search(q, kinds or None, d1, d2, limit=25, dialogue_limit=8) if q else []
        if qp.get("format") == "json":
            return JSONResponse({"q": q, "from": d1, "to": d2, "kinds": kinds,
                                 "results": [h.to_dict() | {"snippet": h.snippet.replace("\x02", "").replace("\x03", "")}
                                             for h in hits]})
        return render(request, "kg_search.html", q=q, hits=hits, d1=d1 or "", d2=d2 or "", kinds=kinds,
                      kg=portal.kg.meta())

    # ------------------------------------------------------------ staff

    async def staff_login(request):
        if not staff_ip_ok(request):
            return error(request, "Not found.", 404)
        if request.method == "GET":
            return render(request, "staff_login.html")
        email = ""
        try:
            form = await form_checked(request)
            email = str(form.get("email", "")).strip().lower()
            if form.get("action") == "verify":
                await run_in_threadpool(portal.staff_login_verify, email, str(form.get("code", "")))
                request.session["staff"] = email
                request.session["staff_exp"] = db.utcnow().timestamp() + STAFF_SESSION_HOURS * 3600
                request.session["csrf"] = secrets.token_urlsafe(24)
                return RedirectResponse("/staff", status_code=303)
            await run_in_threadpool(portal.staff_login_start, email, client_ip(request))
            return render(request, "staff_login.html", email=email, sent=True)
        except PortalError as e:
            return render(request, "staff_login.html", status=400, error=str(e), email=email, sent=bool(email))

    async def staff_logout(request):
        request.session.clear()
        return RedirectResponse("/", status_code=303)

    allowed_nets = [ipaddress.ip_network(n.strip(), strict=False) for n in settings.staff_allowed_ips if n.strip()]

    def staff_ip_ok(request) -> bool:
        if not allowed_nets:
            return True
        try:
            ip = ipaddress.ip_address(client_ip(request))
        except ValueError:
            return False
        return any(ip in n for n in allowed_nets)

    def need_staff(fn):
        async def wrapper(request):
            if not staff_ip_ok(request):
                return error(request, "Not found.", 404)
            if not staff(request):
                return RedirectResponse("/staff/login", status_code=303)
            return await fn(request)
        return wrapper

    @need_staff
    async def staff_home(request):
        conn = portal.conn()
        try:
            act = portal.active(conn)
            queue = portal.queue(conn)
            cal = portal.calendar(conn)
            closed = conn.execute("SELECT * FROM requests WHERE status='closed' ORDER BY closed_at DESC LIMIT 15").fetchall()
        finally:
            conn.close()
        today = portal.today()
        qrows = []
        for i, r in enumerate(queue, 1):
            rec = portal.local(r["received_at"]).date()
            due = date.fromisoformat(r["due_date"])
            qrows.append({"pos": i, "r": r, "received": rec, "due": due,
                          "elapsed": cal.business_days_elapsed(rec, today),
                          "left": cal.business_days_elapsed(today, due) if today < due else 0,
                          "overdue": today > due and not r["ack_sent_at"],
                          "urgent": today >= cal.add_business_days(rec, 3) and not r["ack_sent_at"]})
        result = json.loads(act["triage_json"]) if act and act["triage_json"] else None
        act_info = None
        if act:
            rec = portal.local(act["received_at"]).date()
            act_info = {"received": rec, "due": date.fromisoformat(act["due_date"]),
                        "elapsed": cal.business_days_elapsed(rec, today), "email": act["requester_email"]}
        return render(request, "staff_dashboard.html", act=act, act_info=act_info, result=result, queue=qrows,
                      closed=closed, kg=portal.kg.meta(), engine=settings.triage_engine,
                      notice=request.query_params.get("notice"), err=request.query_params.get("error"))

    def _back(notice=None, error=None):
        from urllib.parse import urlencode
        q = urlencode({k: v for k, v in (("notice", notice), ("error", error)) if v})
        return RedirectResponse("/staff" + ("?" + q if q else ""), status_code=303)

    @need_staff
    async def staff_action(request):
        user = staff(request)
        pk = int(request.path_params["pk"])
        action = request.path_params["action"]
        try:
            form = await form_checked(request)
            subject = str(form.get("subject", ""))
            body = str(form.get("body", "")).replace("\r\n", "\n")
            public_text = form.get("public_text")
            public_text = str(public_text) if public_text is not None and form.get("publish_text") == "on" else None
            if action == "save":
                await run_in_threadpool(portal.save_draft, pk, subject, body, public_text, user)
                return _back("Draft saved.")
            if action == "retriage":
                await run_in_threadpool(portal.retriage, pk, str(form.get("category", "")) or None, user)
                return _back("Triage re-run. The draft below replaces the previous one.")
            if action == "send":
                await run_in_threadpool(portal.send_response, pk, subject, body, public_text, user)
                return _back("Response sent and published. The next request is being triaged.")
            if action == "close":
                await run_in_threadpool(portal.close_without_response, pk, str(form.get("reason", "")),
                                        str(form.get("note", "")), user)
                return _back("Request closed.")
            if action == "ack":
                await run_in_threadpool(portal.send_ack, pk, subject, body, user)
                return _back("Acknowledgment sent and published.")
            return _back(error="Unknown action.")
        except PortalError as e:
            return _back(error=str(e))

    @need_staff
    async def staff_ack(request):
        pk = int(request.path_params["pk"])
        conn = portal.conn()
        try:
            row = portal.get(conn, pk=pk)
        finally:
            conn.close()
        if row is None:
            return error(request, "No such request.", 404)
        subject, body = portal.ack_draft(pk)
        return render(request, "staff_ack.html", r=row, subject=subject, body=body)

    @need_staff
    async def staff_calendar(request):
        user = staff(request)
        if request.method == "POST":
            try:
                form = await form_checked(request)
                day = date.fromisoformat(str(form.get("day")))
                mode = form.get("mode")
                portal.set_calendar(day, None if mode == "clear" else mode == "open", str(form.get("note", "")), user)
            except (PortalError, ValueError) as e:
                return render(request, "message.html", status=400, title="Calendar", message=str(e))
        conn = portal.conn()
        try:
            rows = conn.execute("SELECT * FROM calendar ORDER BY day").fetchall()
            cal = portal.calendar(conn)
        finally:
            conn.close()
        today = portal.today()
        from .bizdays import nh_legal_holidays
        hol = sorted((d, n) for y in (today.year, today.year + 1) for d, n in nh_legal_holidays(y).items() if d >= today)
        return render(request, "staff_calendar.html", rows=rows, holidays=hol[:14])

    async def healthz(request):
        return PlainTextResponse("ok")

    @asynccontextmanager
    async def lifespan(app):
        await run_in_threadpool(portal.recover)
        yield
        portal.stop_worker()

    async def security_headers(scope, receive, send, inner):
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                headers = message.setdefault("headers", [])
                headers += [
                    (b"x-content-type-options", b"nosniff"),
                    (b"x-frame-options", b"DENY"),
                    (b"referrer-policy", b"same-origin"),
                    (b"content-security-policy",
                     b"default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; "
                     b"form-action 'self'; frame-ancestors 'none'"),
                ]
            await send(message)
        await inner(scope, receive, send_wrapper)

    class Headers:
        def __init__(self, app):
            self.app = app

        async def __call__(self, scope, receive, send):
            if scope["type"] != "http":
                return await self.app(scope, receive, send)
            await security_headers(scope, receive, send, self.app)

    routes = [
        Route("/", home),
        Route("/about", about),
        Route("/request", request_form, methods=["GET", "POST"]),
        Route("/verify/{token}", verify, methods=["GET", "POST"]),
        Route("/log", log_list),
        Route("/log.json", log_json),
        Route("/log.csv", log_csv),
        Route("/log/events.json", events_json),
        Route("/log/head.json", log_head),
        Route("/log/{public_id}", log_detail),
        Route("/kg/search", kg_search),
        Route("/staff/login", staff_login, methods=["GET", "POST"]),
        Route("/staff/logout", staff_logout, methods=["POST"]),
        Route("/staff", staff_home),
        Route("/staff/calendar", staff_calendar, methods=["GET", "POST"]),
        Route("/staff/request/{pk:int}/ack", staff_ack),
        Route("/staff/request/{pk:int}/{action}", staff_action, methods=["POST"]),
        Route("/healthz", healthz),
        Mount("/static", StaticFiles(directory=str(HERE / "static")), name="static"),
    ]
    middleware = [
        Middleware(Headers),
        Middleware(SessionMiddleware, secret_key=settings.secret_key, session_cookie="rtk_session",
                   max_age=STAFF_SESSION_HOURS * 3600, same_site="lax", https_only=settings.https_only),
    ]
    app = Starlette(routes=routes, middleware=middleware, lifespan=lifespan)
    app.state.portal = portal
    app.state.settings = settings
    return app


def __getattr__(name):
    # `uvicorn rtk_portal.web:app` builds the app from the environment on first use.
    if name == "app":
        global app
        app = create_app()
        return app
    raise AttributeError(name)
