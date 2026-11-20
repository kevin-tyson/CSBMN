#!/usr/bin/env python3
"""Run the RTK Portal locally on test data and capture its real screens for the explainer.

  python3 capture_portal.py <portal dir> <CSBMN checkout> <out dir>

Starts uvicorn with the outbox mail backend (codes are read from data/outbox/*.eml),
files four fictional requests, signs in as staff, sends one response and saves
3840x2160 screenshots (a 1024x576 window at 3.75x), each stamped TEST DATA. Every request here is invented test data.
"""
import email, glob, os, re, shutil, subprocess, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

PORTAL, REPO, OUT = (Path(p).resolve() for p in sys.argv[1:4])
OUT.mkdir(parents=True, exist_ok=True)
DATA = PORTAL / "data_demo"
if DATA.exists(): shutil.rmtree(DATA)
DATA.mkdir()
shutil.copy(PORTAL / "data" / "kg.db", DATA / "kg.db")
BASE = "http://127.0.0.1:8091"
env = dict(os.environ, RTK_DATA_DIR=str(DATA), RTK_SECRET_KEY="demo-key-for-captures", RTK_BASE_URL=BASE,
           RTK_REPO_PATH=str(REPO), RTK_STAFF_EMAILS="custodian@sau6.example", RTK_MAIL_BACKEND="outbox",
           RTK_HTTPS_ONLY="false", RTK_TRUST_PROXY="false", RTK_ANTHROPIC_API_KEY="")
srv = subprocess.Popen([sys.executable, "-m", "uvicorn", "rtk_portal.web:app", "--host", "127.0.0.1", "--port", "8091",
                        "--log-level", "warning"], cwd=PORTAL, env=env)

def code_for(addr):
    """newest six-digit code mailed to addr"""
    for _ in range(40):
        for f in sorted(glob.glob(str(DATA / "outbox" / "*.eml")), key=os.path.getmtime, reverse=True):
            m = email.message_from_string(Path(f).read_text())
            if addr in (m["To"] or ""):
                body = m.get_payload(decode=True).decode() if not m.is_multipart() else m.get_payload(0).get_payload(decode=True).decode()
                c = re.search(r"\b(\d{3}\s?\d{3})\b", body)
                if c: return c.group(1).replace(" ", "")
        time.sleep(0.25)
    raise SystemExit("no code for " + addr)

REQS = [
    ("pat.resident@example.org", "Pat Resident", True,
     "Please send me the approved minutes of the Claremont School Board meeting held on October 7, 2026."),
    ("pat.resident@example.org", "Pat Resident", True,
     "Please provide the District's contract with its legal counsel and the invoices paid under it for the fiscal year that ended June 30, 2026."),
    ("lee.neighbor@example.org", "", False,
     "How many students at Stevens High School received an out-of-school suspension during the 2025-26 school year?"),
    ("sam.parent@example.org", "", False,
     "I am the parent of Jamie Example, a seventh grader. Please send me my child's discipline records and IEP."),
]
try:
    for _ in range(60):
        try:
            import urllib.request; urllib.request.urlopen(BASE + "/healthz"); break
        except Exception: time.sleep(0.25)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        ctx = b.new_context(viewport={"width": 1024, "height": 576}, device_scale_factor=3.75)
        pg = ctx.new_page()
        BADGE = """(() => { if (document.getElementById('tdb')) return; const d = document.createElement('div'); d.id = 'tdb';
          d.textContent = 'TEST DATA: invented requests'; d.style.cssText = 'position:fixed;right:10px;bottom:10px;z-index:9999;' +
          'background:#a3471f;color:#fff;font:700 11px Inter,sans-serif;letter-spacing:.06em;padding:5px 9px;border-radius:5px';
          document.body.appendChild(d); })()"""
        def shot(name, full=False, at=None, dy=-12):
            pg.evaluate(BADGE)
            if at:
                pg.evaluate("([s, dy]) => { const e = document.querySelector(s); if (e) window.scrollTo(0, e.getBoundingClientRect().top + window.scrollY + dy); }", [at, dy])
            pg.wait_for_timeout(250)
            pg.screenshot(path=str(OUT / f"{name}.jpg"), type="jpeg", quality=92, full_page=full)
            print("shot", name, pg.url)
        pg.goto(BASE + "/"); shot("01_home")
        ids = []
        for i, (addr, name, pub, text) in enumerate(REQS):
            pg.goto(BASE + "/request")
            pg.fill("#text", text); pg.fill("#email", addr)
            if name: pg.fill("#name", name)
            if pub: pg.check("input[name=publish_name]")
            pg.check("input[name=ack]")
            if i == 0: shot("02_form_top", at="h1", dy=-70); shot("02_form_bottom", at="#email", dy=-40)
            pg.click("button.primary")
            pg.wait_for_url(re.compile(r"/verify/"))
            code = code_for(addr)
            pg.fill("#code", code)
            if i == 0: shot("03_verify_code")
            pg.click("button[value=verify]")
            pg.wait_for_url(re.compile(r"/log/"))
            ids.append(pg.url.split("/log/")[1].split("?")[0])
            if i == 0: shot("04_filed_status")
            time.sleep(1.1)
        print("ids", ids)
        # staff sign-in
        pg.goto(BASE + "/staff/login"); pg.fill("#email", "custodian@sau6.example"); pg.click("button[value=start]")
        pg.wait_for_selector("#code"); pg.fill("#code", code_for("custodian@sau6.example")); pg.click("button[value=verify]")
        pg.wait_for_url(re.compile(r"/staff$|/staff\?"))
        for _ in range(80):       # wait for the first draft
            pg.goto(BASE + "/staff")
            if pg.query_selector("#body"): break
            time.sleep(1)
        shot("05_console_top"); shot("05_console_draft", at="#subject", dy=-60)
        pg.goto(BASE + "/log"); shot("06_log_before")
        pg.goto(BASE + "/staff")
        pg.click("button[formaction$='/send']")
        pg.wait_for_load_state("networkidle"); shot("07_after_send")
        for _ in range(80):       # next request's draft
            pg.goto(BASE + "/staff")
            if pg.query_selector("#body"): break
            time.sleep(1)
        shot("08_console_next"); shot("08_console_next_draft", at="#subject", dy=-60)
        pg.click("button[formaction$='/send']")       # placeholders should block this one
        pg.wait_for_load_state("networkidle"); shot("09_send_blocked")
        pg.goto(BASE + "/log"); shot("10_log_list")
        pg.goto(BASE + "/log/" + ids[0]); shot("11_log_detail"); shot("11_log_detail_response", at="h2:nth-of-type(2), h3", dy=-20)
        pg.goto(BASE + "/log/" + ids[3]); shot("12_log_held")
        pg.goto(BASE + "/"); shot("13_home_after")
        b.close()
finally:
    srv.terminate()
