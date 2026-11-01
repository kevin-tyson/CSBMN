# SPDX-License-Identifier: Apache-2.0
import re

from starlette.testclient import TestClient

from rtk_portal.web import create_app


def csrf_of(html):
    return re.search(r'name="csrf" value="([^"]+)"', html).group(1)


def test_end_to_end(settings, portal, mailer):
    app = create_app(settings, portal)
    with TestClient(app) as c:
        r = c.get("/request")
        tok = csrf_of(r.text)
        r = c.post("/request", data={"csrf": tok, "email": "Res@Example.org", "name": "Pat Doe",
                                     "text": "Please send the minutes and the video of the school board meeting on October 7, 2026.",
                                     "ack": "on"}, follow_redirects=False)
        assert r.status_code == 303 and r.headers["location"].startswith("/verify/")
        verify_url = r.headers["location"]
        r = c.get(verify_url)
        assert "re***@example.org" in r.text
        r = c.post(verify_url, data={"csrf": tok, "code": mailer.last_code("res@example.org"), "action": "verify"},
                   follow_redirects=False)
        assert r.status_code == 303
        pid = re.search(r"/log/(RTK-\d{4}-\d{4})", r.headers["location"]).group(1)
        r = c.get(f"/log/{pid}")
        assert "Received and logged" in r.text and "res@example.org" not in r.text.lower()
        assert "Pat Doe" not in r.text  # name not consented

        # public pages
        assert c.get("/log").status_code == 200
        assert pid in c.get("/log.csv").text
        ev = c.get("/log/events.json").json()
        assert ev["chain_ok"] is True
        s = c.get("/kg/search", params={"q": "audit contract"})
        assert "Madden asks for the signed audit contract" in s.text

        # staff
        r = c.get("/staff", follow_redirects=False)
        assert r.status_code == 303
        r = c.post("/staff/login", data={"csrf": tok, "email": "clerk@sau6.test", "action": "start"})
        r = c.post("/staff/login", data={"csrf": tok, "email": "clerk@sau6.test", "action": "verify",
                                         "code": mailer.last_code("clerk@sau6.test")}, follow_redirects=False)
        assert r.status_code == 303
        r = c.get("/staff")
        assert pid in r.text and "Answerable from publicly available information" in r.text
        tok = csrf_of(r.text)
        body = re.search(r'<textarea id="body" name="body"[^>]*>(.*?)</textarea>', r.text, re.S).group(1)
        import html
        body = html.unescape(body)
        subject = html.unescape(re.search(r'id="subject" name="subject" value="([^"]*)"', r.text).group(1))
        pk = re.search(r"/staff/request/(\d+)/send", r.text).group(1)
        r = c.post(f"/staff/request/{pk}/send", data={"csrf": tok, "subject": subject, "body": body},
                   follow_redirects=False)
        assert r.status_code == 303 and "error" not in r.headers["location"], r.headers["location"]
        r = c.get(f"/log/{pid}")
        assert "Response sent" in r.text and "Responded" in r.text
        assert mailer.sent[-1]["to"] == "res@example.org"


def test_csrf_and_staff_enumeration(settings, portal, mailer):
    app = create_app(settings, portal)
    with TestClient(app) as c:
        c.get("/request")
        r = c.post("/request", data={"csrf": "wrong", "email": "a@b.org", "text": "x" * 30, "ack": "on"})
        assert r.status_code == 400
        tok = csrf_of(c.get("/staff/login").text)
        before = len(mailer.sent)
        r = c.post("/staff/login", data={"csrf": tok, "email": "random@else.org", "action": "start"})
        assert r.status_code == 200 and len(mailer.sent) == before  # same page, no code sent
        r = c.get("/")
        assert r.headers["x-frame-options"] == "DENY"
