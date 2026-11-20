#!/usr/bin/env python3
"""Draw the 1920x1080 cards (at 2x) and the draft caption bands.

  python3 _source/make_cards.py            # cards/ and draft_captions/
Needs Playwright and the Inter and Lora fonts. Palette matches the briefing deck.
"""
import html, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import script_data as S

CARDS = ROOT / "cards"; CAPS = ROOT / "draft_captions"
for d in (CARDS, CAPS): d.mkdir(exist_ok=True)

NAVY = "#16263F"; PAPER = "#F6F3EC"; PAPER2 = "#EAE5D8"; RUST = "#A3471F"; TEAL = "#1F6466"; AMBER = "#E9B872"
INK = "#3D4A5C"; MUTED = "#5E6B7A"; LINE = "#D8D1BF"
CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1920px;height:1080px;overflow:hidden}}
body{{font-family:Inter,sans-serif;background:{PAPER};color:{NAVY};-webkit-font-smoothing:antialiased}}
body.dark{{background:{NAVY};color:{PAPER}}}
.wrap{{position:absolute;inset:0;padding:96px 128px 120px;display:flex;flex-direction:column}}
.kicker{{font-size:26px;font-weight:700;letter-spacing:.14em;color:{RUST};margin-bottom:18px}}
.dark .kicker{{color:{AMBER}}}
h1{{font-family:Lora,serif;font-size:92px;line-height:1.08;font-weight:600;max-width:1560px}}
h2{{font-family:Lora,serif;font-size:66px;line-height:1.1;font-weight:600}}
.lead{{font-size:38px;line-height:1.4;color:{INK};margin-top:30px;max-width:1500px}}
.dark .lead{{color:#C9D3E0}}
.main{{flex:1;display:flex;flex-direction:column;justify-content:center;gap:40px;padding-top:24px}}
.quote{{font-family:Lora,serif;font-size:70px;line-height:1.2;max-width:1560px}}
.cite{{font-size:30px;line-height:1.4;color:{MUTED};max-width:1450px}}
.dark .cite{{color:#9FB0C6}}
.grid{{display:grid;gap:32px}}
.card{{background:{PAPER2};border-radius:20px;padding:40px 36px;display:flex;flex-direction:column;gap:14px}}
.dark .card{{background:#22375A}}
.num{{font-family:Lora,serif;font-size:64px;font-weight:600;line-height:1;color:{RUST}}}
.card h3{{font-size:42px;font-weight:700;line-height:1.15}}
.card p{{font-size:32px;line-height:1.35;color:{INK}}}
.dark .card p{{color:#C9D3E0}}
.strong{{font-size:38px;line-height:1.35;font-weight:600}}
.row{{font-size:36px;line-height:1.3;color:{INK};padding:22px 0;border-top:2px solid {LINE};display:flex;gap:28px;align-items:baseline}}
.row b{{color:{NAVY};min-width:430px;font-weight:700}}
.pill{{display:inline-block;font-size:24px;font-weight:700;letter-spacing:.06em;color:#fff;padding:8px 16px;border-radius:8px}}
.round{{background:{PAPER2};border-radius:20px;padding:32px 36px;display:flex;flex-direction:column;gap:20px}}
.round span{{font-size:26px;font-weight:700;letter-spacing:.14em;color:{MUTED}}}
.chips{{display:flex;gap:18px}}
.chip{{font-size:52px;font-weight:700;color:#fff;padding:22px 34px;border-radius:14px;line-height:1}}
.arrow{{font-size:56px;color:{RUST};align-self:center;font-weight:700}}
.stat{{border-top:8px solid {RUST};padding-top:24px}}
.stat .n{{font-family:Lora,serif;font-size:150px;font-weight:600;line-height:1}}
.stat p{{font-size:34px;line-height:1.35;color:{INK};margin-top:10px}}
.foot{{position:absolute;left:128px;right:128px;bottom:48px;font-size:22px;color:{MUTED};display:flex;justify-content:space-between}}
.dark .foot{{color:#9FB0C6}}
"""
FOOT = '<div class="foot"><span>Right-to-Know Request Portal</span><span>Briefing for the Claremont School Board and Administration</span></div>'

def page(body, dark=False, foot=True):
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head>"
            f"<body class='{'dark' if dark else ''}'>{body}{FOOT if foot else ''}</body></html>")

def std(kicker, title, main, dark=False):
    return page(f"<div class='wrap'><div class='kicker'>{kicker}</div><h2>{title}</h2><div class='main'>{main}</div></div>", dark)

def cards(items, cols):
    return (f"<div class='grid' style='grid-template-columns:repeat({cols},1fr)'>" +
            "".join(f"<div class='card'>{('<div class=num>%s</div>' % n) if n else ''}<h3>{h}</h3><p>{t}</p></div>" for n, h, t in items) + "</div>")

C = {}
C["title"] = page(f"<div class='wrap' style='justify-content:center'><div class='kicker'>AN EXPLAINER FOR THE CLAREMONT SCHOOL BOARD AND ADMINISTRATION</div>"
                  f"<h1>{S.TITLE}</h1><p class='lead'>How it would work, and why we are asking Anthropic to help pay for it</p></div>", dark=True, foot=False)

C["law"] = std("THE LAW", "RSA 91-A sets a five-business-day clock",
    "<p class='lead' style='margin-top:0'>When a record is not immediately available, the District must do one of these within five business days:</p>" +
    cards([("1", "Produce it", "Make the record available."),
           ("2", "Deny it", "In writing, with the reasons."),
           ("3", "Set a time", "Say in writing when it will answer.")], 3) +
    "<p class='cite'>RSA 91-A:4, IV(b)</p>")

C["policy"] = std("THE STARTING POINT", "Policy EH already calls for a request log",
    "<p class='quote'>“a method for logging and tracking both the requests and the responses”</p>"
    "<p class='cite'>Claremont School Board Policy EH, adopted September 17, 2025, on what the Superintendent’s procedures are to include. "
    "The policy also allows the log to be posted on the District’s website.</p>")

C["overview"] = std("THE PORTAL IN BRIEF", "What the portal does",
    cards([("1", "Receives", "A resident files online and confirms an email address."),
           ("2", "Orders", "Requests wait in a fair queue, handled one at a time."),
           ("3", "Drafts", "The portal prepares a draft response for staff."),
           ("4", "Publishes", "Request and response go on a public log.")], 4) +
    "<p class='strong'>District staff review, edit and send every response.</p>")

chip = lambda t, c: f"<div class='chip' style='background:{c}'>{t}</div>"
C["queue"] = std("HOW IT WOULD WORK", "A fair queue, one request at a time",
    "<p class='lead' style='margin-top:0'>A files three requests, then B files one, C files one, and B files a second. The portal takes them in this order:</p>"
    "<div style='display:flex;gap:22px;align-items:stretch'>"
    f"<div class='round'><span>ROUND 1</span><div class='chips'>{chip('A1', NAVY)}{chip('B1', TEAL)}{chip('C1', RUST)}</div></div><div class='arrow'>→</div>"
    f"<div class='round'><span>ROUND 2</span><div class='chips'>{chip('A2', NAVY)}{chip('B2', TEAL)}</div></div><div class='arrow'>→</div>"
    f"<div class='round'><span>ROUND 3</span><div class='chips'>{chip('A3', NAVY)}</div></div></div>"
    "<p class='strong'>A person’s first open request goes ahead of anyone’s second.</p>")

C["outcomes"] = std("HOW IT WOULD WORK", "Five draft outcomes",
    "<div>" + "".join(f"<div class='row'><b>{a}</b><span>{b}</span></div>" for a, b in [
        ("Records search", "A valid request for a record that is not posted"),
        ("Public information", "The record is already public; the draft links to it"),
        ("Aggregate only", "Counts about students, with small counts suppressed"),
        ("Outside District policy", "A parent’s own-child request, or another agency’s record"),
        ("Outside RSA 91-A", "An exempt record, or a question that names no record")]) + "</div>")

step = lambda c, k, h, t: f"<div class='card' style='flex:1'><div><span class='pill' style='background:{c}'>{k}</span></div><h3>{h}</h3><p>{t}</p></div>"
C["triage"] = std("HOW IT WOULD WORK", "Who writes the draft",
    "<div style='display:flex;gap:22px;align-items:stretch'>" +
    step(NAVY, "ALWAYS", "Fixed rules", "Sort the request and write a first draft. No network needed.") + "<div class='arrow'>→</div>" +
    step(TEAL, "WHEN SWITCHED ON", "Claude", "Searches the public record and prepares the draft.") + "<div class='arrow'>→</div>" +
    step(NAVY, "ALWAYS", "Checks", "Citations must come from an approved list. Unverified links are marked.") + "<div class='arrow'>→</div>" +
    step(RUST, "ALWAYS", "District staff", "Read, edit and send.") + "</div>"
    "<p class='cite'>The portal screens in this video show the fixed rules only.</p>")

C["status"] = std("WHERE IT STANDS", "Built and tested, not yet piloted",
    "<div class='grid' style='grid-template-columns:repeat(3,1fr);gap:40px'>"
    "<div class='stat'><div class='n'>56</div><p>automated tests, all passing</p></div>"
    "<div class='stat'><div class='n'>19</div><p>defects found by an independent review, all fixed</p></div>"
    "<div class='stat'><div class='n'>2</div><p>steps left: counsel review, and one live test of the Claude step</p></div></div>")

C["why"] = std("WHY ANTHROPIC", "Why we are approaching Anthropic",
    cards([("", "The portal can use Claude", "Anthropic’s model can prepare the draft of each response."),
           ("", "That use costs money", "Model use is billed by volume. The project does not want that cost on the District’s budget.")], 2), dark=True)

C["s1"] = std("WHY ANTHROPIC", "What Anthropic has said",
    "<p class='quote'>“programs designed to make Claude accessible to underserved communities, educators, and public institutions”</p>"
    "<p class='cite'>Anthropic, PBC, Form S-1 registration statement, filed October 26, 2026, page 144. The same filing reports that "
    "5% of the company’s shares were placed in the Anthropic Public Benefit Fund.</p>", dark=True)

ASK = cards([("1", "Use of Claude at no charge", "For drafting responses."),
             ("2", "An operating grant", "To the proposed operator, Claremont Community Television (CCTV) / Claremont Community Media Center (CCMC).")], 2)
C["ask"] = std("WHY ANTHROPIC", "What we would ask of Anthropic", ASK)
C["ask2"] = std("WHY ANTHROPIC", "What we would ask of Anthropic", ASK +
    "<p class='strong'>Anthropic has made no commitment. Without it, the portal still works on its fixed rules.</p>")

C["decisions"] = std("WHAT WE ARE ASKING", "Decisions for the Board and Administration",
    "<div>" + "".join(f"<div class='row'><span>{a}</span></div>" for a in [
        "Authorize a pilot and name a records custodian",
        "Confirm the operator",
        "Have counsel review the citations and templates",
        "Settle the privacy settings: names, contact details, text sent to Claude",
        "Endorse the appeal to Anthropic"]) + "</div>"
    "<p class='cite'>The briefing deck lists all eight decisions and who makes each.</p>")

C["closing"] = page("<div class='wrap' style='justify-content:center'><div class='kicker'>IN ONE LINE</div>"
                    "<h1>The portal drafts.<br>District staff decide.</h1></div>", dark=True, foot=False)

C["end"] = page("<div class='wrap' style='justify-content:center'><div class='kicker'>RIGHT-TO-KNOW REQUEST PORTAL</div>"
                "<h2>Kevin Tyson, Government Transparency Project</h2>"
                "<p class='lead'>November 2026. Portal screens show the working software on invented test requests. "
                "The portal is not legal advice.</p>"
                "<p class='cite' style='margin-top:36px'>Sources: Claremont School Board Policy EH (adopted September 17, 2025); RSA 91-A:4; "
                "RTK Portal README, October 30, 2026; Anthropic, PBC, Form S-1, filed October 26, 2026, page 144.</p></div>", dark=True, foot=False)

def caption(text):
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>*{{margin:0;padding:0;box-sizing:border-box}}"
            f"html,body{{width:1920px;height:1080px;background:transparent}}"
            f".b{{position:absolute;left:0;right:0;bottom:0;background:rgba(22,38,63,.93);padding:26px 128px 30px;"
            f"font:500 30px/1.38 Inter,sans-serif;color:#F6F3EC}}.t{{font:700 18px Inter;letter-spacing:.14em;color:{AMBER};margin-bottom:8px}}"
            f"</style></head><body><div class='b'><div class='t'>DRAFT · NARRATION TEXT</div>{html.escape(text)}</div></body></html>")

only = set(sys.argv[1:])
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=2).new_page()
    for name, doc in C.items():
        if only and name not in only: continue
        pg.set_content(doc); pg.wait_for_timeout(120)
        pg.screenshot(path=str(CARDS / f"{name}.png")); print("card", name)
    if not only:
        pg2 = b.new_context(viewport={"width": 1920, "height": 1080}).new_page()
        for s in S.SEGMENTS:
            if s["kind"] == "narr":
                pg2.set_content(caption(s["text"])); pg2.wait_for_timeout(60)
                pg2.screenshot(path=str(CAPS / f"{s['id']}.png"), omit_background=True)
    b.close()
