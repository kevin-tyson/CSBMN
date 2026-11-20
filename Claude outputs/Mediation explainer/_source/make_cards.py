#!/usr/bin/env python3
"""Draw the 1920x1080 cards (at 2x) and the draft caption bands for the mediation explainer.

  python3 _source/make_cards.py            # cards/ and draft_captions/
  python3 _source/make_cards.py arch s1    # only those cards
Needs Playwright and the Inter and Lora fonts. Palette matches the RTK explainer and briefing deck.
"""
import html, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import script_data as S
exec(open(Path(__file__).with_name("_css.py")).read())   # NAVY, PAPER ... and CSS

CARDS = ROOT / "cards"; CAPS = ROOT / "draft_captions"
for d in (CARDS, CAPS): d.mkdir(exist_ok=True)

FOOT = ('<div class="foot"><span>Claude as the front desk for district records</span>'
        '<span>Government Transparency Project · November 2026</span></div>')

def page(body, dark=False, foot=True):
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head>"
            f"<body class='{'dark' if dark else ''}'>{body}{FOOT if foot else ''}</body></html>")

def std(kicker, title, main, dark=False):
    return page(f"<div class='wrap'><div class='kicker'>{kicker}</div><h2>{title}</h2><div class='main'>{main}</div></div>", dark)

def cards(items, cols):
    return (f"<div class='grid' style='grid-template-columns:repeat({cols},1fr)'>" +
            "".join(f"<div class='card'>{('<div class=num>%s</div>' % n) if n else ''}<h3>{h}</h3><p>{t}</p></div>" for n, h, t in items) + "</div>")

def rows(items, cls=""):
    return f"<div class='{cls}'>" + "".join(f"<div class='row'><b>{a}</b><span>{b}</span></div>" for a, b in items) + "</div>"

C = {}
C["title"] = page(f"<div class='wrap' style='justify-content:center'><div class='kicker'>AN EXPLAINER FOR CLAREMONT RESIDENTS, THE SCHOOL BOARD AND ANTHROPIC</div>"
                  f"<h1>{S.TITLE}</h1><p class='lead'>How it would work, what must come first, and why we are asking Anthropic to help</p></div>", dark=True, foot=False)

C["oneline"] = std("THE PROPOSAL", "One idea",
    "<p class='quote'>Fixed rules decide who may see what. Claude finds the record and drafts the answer. A person decides what is sent.</p>"
    "<p class='cite'>Student and employee files never go to the model.</p>")

C["constituents"] = std("WHO IS OWED WHAT", "Six groups, different rules",
    rows([("Taxpayers and the public", "Governmental records under RSA 91-A: five business days"),
          ("Parents", "Their own child's education records: the shortest of three clocks"),
          ("Students", "The same rights at age 18; the policies that bind them"),
          ("Former students", "Their own records, for as long as the district keeps them"),
          ("Teachers and staff", "Their own personnel file; the policy in force on a date"),
          ("Administrators and Board", "Only the access the job needs (Policy EHAB)")], "wide"))

C["clocks"] = std("PARENTS' RECORDS", "Three laws, three clocks",
    "<div>"
    "<div class='clock'><div class='n'>45</div><div class='u'>days</div><div class='s'>Federal rule, 34 CFR 99.10(b)</div></div>"
    "<div class='clock'><div class='n'>14</div><div class='u'>days</div><div class='s'>RSA 189:66, IV</div></div>"
    "<div class='clock win'><div class='n'>10</div><div class='u'>business days</div><div class='s'>RSA 189-B:4, I(o), in force since July 1, 2025</div></div>"
    "</div><p class='strong'>A careful system follows the shortest. Board Policy JRA cites only the 14-day rule.</p>")

C["volume"] = std("THE SIZE OF THE RECORD", "Too much for one free evening",
    "<div class='grid' style='grid-template-columns:repeat(3,1fr);gap:40px'>"
    "<div class='stat'><div class='n'>284</div><p>School Board policies in the index</p></div>"
    "<div class='stat'><div class='n'>120</div><p>of them dated before 2015</p></div>"
    "<div class='stat'><div class='n'>319</div><p>recorded meetings indexed, back to 2015</p></div></div>"
    "<p class='cite'>Policy index snapshot of October 30, 2026; Government Transparency Project meeting index.</p>")

C["warning"] = std("WHY IT MATTERS", "The warnings were public",
    rows([("September 5, 2018", "Board told of 14 outstanding audits"),
          ("February 20, 2019", "Board told audits were behind since 2012"),
          ("November 20, 2019", "Auditor calls the district one of its most delinquent clients"),
          ("August 2025", "Board announces a deficit then estimated at up to $5 million")], "wide") +
    "<p class='cite'>Recorded board meetings, as cited in The Elite Theory Perspective (project report, September 2026); Valley News, September 23, 2026.</p>")

def arch(on=None):
    def cls(k, extra=""):
        if on is None: return f"box {extra}"
        return f"box {extra} {'on' if k == on else 'dim'}"
    b = lambda k, h, p, extra="": f"<div class='{cls(k, extra)}'><h4>{h}</h4><p>{p}</p></div>"
    return page("<div class='wrap tight'><div class='kicker'>HOW CLAUDE WOULD MEDIATE</div><h2>Four layers and a log</h2><div class='main'>"
        "<div class='arch'>" +
        b("in", "Public and taxpayers", "No sign-in needed") +
        b("in", "Parents, students, former students", "Identity verified by staff") +
        b("in", "Teachers and staff", "District sign-in") +
        b("gate", "1 · Gate: fixed rules, not a model", "Sets identity, privacy tier and legal deadline for each request", "span3") +
        b("claude", "3 · Claude", "Searches the graph; answers with a source link; drafts, never sends", "span2") +
        b("custodian", "4 · Records custodian", "Reviews and sends every draft; handles own-record requests", "c3") +
        b("graph", "2 · District records graph", "Public tiers only: dated policies, minutes, budgets, meeting index, legal duties", "span2") +
        b("systems", "Systems of record", "Student and employee files, never in the graph", "c3") +
        b("log", "5 · Hash-chained log", "Every request, answer, review and release is recorded", "span3") +
        "</div></div></div>")
C["arch"] = arch()
for k in ("gate", "graph", "claude", "custodian", "log"):
    C[f"arch_{k}"] = arch(k)

C["conditions"] = std("WHAT MUST COME FIRST", "Conditions the district has already set",
    "<div>" + "".join(f"<div class='tick'><b>{a}</b><span>{b}</span><span class='st'>{c}</span></div>" for a, b, c in [
        ("Superintendent's written approval", "Policy EHAG, section C", "NOT YET"),
        ("Security officer approves the vendor", "Policy EHAB, section G; free or not", "NOT YET"),
        ("Public list of approved AI tools", "Policy EHAG, section E.5", "NOT FOUND"),
        ("Direct control over any student data", "34 CFR 99.31(a)(1)(i)(B); counsel to advise", "OPEN"),
        ("Counsel reviews citations and templates", "RTK portal build record", "NOT YET")]) + "</div>"
    "<p class='strong'>Until these are settled, Claude sees public records only.</p>")

C["gatekeeper"] = std("A MEDIATOR IS ALSO A GATEKEEPER", "Four limits on the mediator",
    cards([("1", "Checkable answers", "Every statement links to the original record."),
           ("2", "A public log", "Requests, due dates and responses are posted."),
           ("3", "An independent navigator", "The meeting index stays outside district control."),
           ("4", "No lock-in", "Fixed rules can draft responses with no model at all.")], 4))

C["stages"] = std("A PATH, NOT A LEAP", "Start with the duties the law already sets",
    "<div>" + "".join(f"<div class='row'><b>{a}</b><span>{b}</span></div>" for a, b in [
        ("1 · Public record", "Anyone asks about minutes, policies, budgets, meetings"),
        ("2 · Staff desk", "Policy in force on a date; drafts of routine letters"),
        ("3 · Own records", "Rights explained and the clock started; staff retrieve the file"),
        ("4 · Classroom", "Later, under the district's AI Use Plan; not in this request")]) + "</div>"
    "<p class='cite'>Each stage would be an entry in the Generative AI Use Plan reported to the Board each June (Policy EHAG, section J).</p>")

C["measures"] = std("WHAT A PILOT CAN SHOW", "Measured, not promised",
    cards([("", "On time", "Share of requests answered inside each legal clock"),
           ("", "Accurate", "Share of answers whose source links support them"),
           ("", "Edited", "How often, and how, staff change a draft"),
           ("", "Cost", "Staff hours and model cost per request")], 4) +
    "<p class='strong'>No baseline has been measured yet. The proposal makes no claim about student achievement.</p>")

C["voters"] = std("SELF-GOVERNMENT", "In Claremont, the voters are the legislature",
    cards([("Feb 7", "Deliberative session", "Residents debated and amended the 2026 warrant for four hours."),
           ("Mar 10", "Ballot vote", "Voters decided the budget and a petitioned spending cap.")], 2) +
    "<p class='cite'>Valley News, February 9, 2026.</p>")

C["constitution"] = std("NEW HAMPSHIRE LAW", "Access is a right, not a courtesy",
    "<p class='quote'>“open, accessible, accountable and responsive”</p>"
    "<p class='cite'>N.H. Constitution, Part I, Article 8, as amended 1976: public access to governmental records “shall not be unreasonably restricted.” "
    "RSA 91-A:1 calls openness in public business “essential to a democratic society.”</p>", dark=True)

C["tocqueville"] = std("THE NEW ENGLAND TRADITION", "Self-government needs a readable record",
    "<p class='quote'>“Town-meetings are to liberty what primary schools are to science.”</p>"
    "<p class='cite'>Alexis de Tocqueville, Democracy in America, vol. 1, ch. 5 (1835), trans. Henry Reeve.</p>", dark=True)

C["precedent"] = std("CLAREMONT HAS LED BEFORE", "A lower-income district that changed the state's rule",
    "<div class='grid' style='grid-template-columns:repeat(2,1fr);gap:56px'>"
    "<div class='stat'><div class='n'>1993</div><p>Claremont School District v. Governor: the state must provide an adequate education and guarantee its funding</p></div>"
    "<div class='stat'><div class='n'>$54,520</div><p>median household income in the district (NCES, American Community Survey 2019 to 2023)</p></div></div>")

C["s1"] = std("WHY ANTHROPIC", "What Anthropic has said",
    "<p class='quote'>“programs designed to make Claude accessible to underserved communities, educators, and public institutions”</p>"
    "<p class='cite'>Anthropic, PBC, Form S-1 registration statement, filed October 26, 2026, page 144. The same filing reports that "
    "5% of the company’s shares were placed in the Anthropic Public Benefit Fund (pages 13 and 144).</p>", dark=True)

C["ask"] = std("THE APPEAL", "What the letter asks, and what it offers",
    cards([("1", "Claude at no charge", "For the length of a defined pilot."),
           ("2", "An operating grant", "To a nonprofit operator, for hosting and legal review."),
           ("3", "Published results", "On-time rate, source accuracy, staff edits, cost, and the failures.")], 3) +
    "<p class='strong'>Anthropic has made no commitment. The filing describes no application process.</p>")

C["before"] = std("BEFORE THE LETTER IS SENT", "What has to happen first",
    "<div>" + "".join(f"<div class='row'><span>{a}</span></div>" for a in [
        "The district approves the tool under Policies EHAG and EHAB",
        "Counsel reviews the design, the citations and the templates",
        "A nonpartisan organization signs, with the district's endorsement if given",
        "Official enrollment and income figures replace secondary sources"]) + "</div>"
    "<p class='cite'>The written proposal and its sources go with this video.</p>")

C["closing"] = page("<div class='wrap' style='justify-content:center'><div class='kicker'>IN ONE LINE</div>"
                    "<h1>Rules decide who may see what.<br>Claude finds and drafts.<br>People decide.</h1></div>", dark=True, foot=False)

C["end"] = page("<div class='wrap' style='justify-content:center'><div class='kicker'>CLAUDE AS THE FRONT DESK FOR DISTRICT RECORDS</div>"
                "<h2>Kevin Tyson, Government Transparency Project</h2>"
                "<p class='lead'>November 2026. Portal screens show the working software on invented test requests, stamped TEST DATA. "
                "Nothing here is legal advice. Anthropic has made no commitment.</p>"
                "<p class='cite' style='margin-top:36px'>Sources: Claremont School Board Policies EHAG, EHAB, EH and JRA; RSA 91-A:1 and 91-A:4; RSA 189:66; RSA 189-B:4; "
                "34 CFR 99.10 and 99.31; N.H. Const. pt. I, art. 8; Anthropic, PBC, Form S-1, filed October 26, 2026; "
                "Tocqueville, Democracy in America (1835); Valley News; NCES.</p></div>", dark=True, foot=False)

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
