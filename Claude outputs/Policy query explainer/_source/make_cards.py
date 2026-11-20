#!/usr/bin/env python3
"""Draw the 1920x1080 cards (at 2x) and the draft caption bands for the policy-query explainer.

  python3 _source/make_cards.py            # cards/ and draft_captions/
  python3 _source/make_cards.py step2 q2   # only those cards
Needs Playwright and the Inter and Lora fonts. Palette matches the earlier project explainers.
"""
import html, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import script_data as S
exec(open(Path(__file__).with_name("_css.py")).read())   # NAVY, PAPER ... and CSS

CSS += f"""
.crumbs{{display:flex;flex-wrap:wrap;align-items:center;gap:16px}}
.crumb{{font-size:40px;font-weight:700;background:{NAVY};color:{PAPER};padding:18px 28px;border-radius:12px;line-height:1}}
.crumb.end{{background:{TEAL}}}
.sep{{font-size:44px;color:{RUST};font-weight:700}}
.note{{font-size:32px;line-height:1.4;color:{INK};border-left:6px solid {AMBER};padding:6px 0 6px 26px;max-width:1560px}}
.tree{{font-family:'DejaVu Sans Mono',monospace;font-size:34px;line-height:1.6;background:{PAPER2};border-radius:16px;padding:26px 36px;color:{NAVY};width:fit-content}}
.tree i{{color:{MUTED};font-style:normal}}
.bars{{display:grid;grid-template-columns:64px 710px 1fr;gap:6px 24px;align-items:center}}
.bars .l{{font-family:Lora,serif;font-size:42px;font-weight:600;color:{RUST};line-height:1.15}}
.bars .t{{font-size:34px;color:{NAVY};white-space:nowrap}}
.bars .bw{{display:flex;align-items:center;gap:18px}}
.bars .b{{height:30px;background:{TEAL};border-radius:6px;flex:none}}
.bars .n{{font-size:38px;font-weight:700;color:{NAVY};line-height:1}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:40px}}
.col{{background:{PAPER2};border-radius:20px;padding:34px 40px}}
.col h3{{font-size:40px;margin-bottom:14px}}
.col.yes h3{{color:{TEAL}}} .col.no h3{{color:{RUST}}}
.col li{{font-size:31px;line-height:1.35;color:{INK};margin:12px 0 12px 32px}}
.q{{align-self:flex-end;background:{NAVY};color:{PAPER};font-size:38px;line-height:1.35;padding:26px 36px;border-radius:24px 24px 6px 24px;max-width:1300px}}
.qlabel{{font-size:22px;font-weight:700;letter-spacing:.14em;color:{AMBER};display:block;margin-bottom:8px}}
.a{{background:#fff;border:3px solid {LINE};border-radius:24px 24px 24px 6px;padding:28px 40px;max-width:1600px}}
.alabel{{font-size:22px;font-weight:700;letter-spacing:.14em;color:{TEAL};margin-bottom:10px}}
.a p{{font-size:29px;line-height:1.42;color:{NAVY};margin:10px 0}}
.a .c{{color:{TEAL};font-weight:600}}
.doc{{background:#fff;box-shadow:0 6px 30px rgba(22,38,63,.18);border-radius:6px;padding:56px 80px;max-width:1500px;align-self:center;font-family:Lora,serif;color:#222}}
.doc .h{{font-size:28px;color:#555;margin-bottom:6px}}
.doc .tt{{font-size:40px;font-weight:600;margin:12px 0 22px}}
.doc .s{{font-size:30px;font-weight:600;margin-top:18px}}
.doc p{{font-size:30px;line-height:1.5;margin-top:10px}}
.doc mark{{background:#F6DFAF;padding:0 4px}}
.flow{{display:flex;align-items:stretch;gap:14px}}
.step{{flex:1;background:{PAPER2};border-radius:18px;padding:26px 24px;display:flex;flex-direction:column;gap:10px;border:3px solid transparent}}
.step .k{{font-family:Lora,serif;font-size:50px;font-weight:600;color:{RUST};line-height:1}}
.step h4{{font-size:31px;line-height:1.2}}
.step p{{font-size:25px;line-height:1.35;color:{INK}}}
.step.on{{border-color:{TEAL};background:#DCEBEA}}
.flow .ar{{align-self:center;font-size:44px;color:{RUST};font-weight:700}}
.big3 .step{{padding:44px 40px;gap:18px}} .big3 .step h4{{font-size:46px}} .big3 .step p{{font-size:34px}}
.big{{font-family:Lora,serif;font-size:150px;font-weight:600;line-height:1;color:{RUST}}}
.pol{{background:{PAPER2};border-radius:20px;padding:32px 38px;display:flex;flex-direction:column;gap:12px}}
.pol .code{{font-family:Lora,serif;font-size:56px;font-weight:600;color:{RUST};line-height:1}}
.pol h3{{font-size:36px;line-height:1.2}}
.pol .d{{font-size:27px;font-weight:700;color:{MUTED};letter-spacing:.04em}}
.pol blockquote{{font-family:Lora,serif;font-size:31px;line-height:1.45;border-left:6px solid {AMBER};padding-left:24px;margin-top:6px}}
"""

CARDS = ROOT / "cards"; CAPS = ROOT / "draft_captions"
for d in (CARDS, CAPS): d.mkdir(exist_ok=True)

FOOT = ('<div class="foot"><span>Asking Claude about Claremont School Board policy</span>'
        '<span>Government Transparency Project · November 2026</span></div>')

def page(body, dark=False, foot=True):
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head>"
            f"<body class='{'dark' if dark else ''}'>{body}{FOOT if foot else ''}</body></html>")

def std(kicker, title, main, dark=False, tight=False):
    return page(f"<div class='wrap{' tight' if tight else ''}'><div class='kicker'>{kicker}</div><h2>{title}</h2>"
                f"<div class='main'>{main}</div></div>", dark)

def rows(items, cls=""):
    return f"<div class='{cls}'>" + "".join(f"<div class='row'><b>{a}</b><span>{b}</span></div>" for a, b in items) + "</div>"

def crumbs(*items):
    out = []
    for i, x in enumerate(items):
        if i: out.append("<span class='sep'>›</span>")
        out.append(f"<span class='crumb{' end' if i == len(items) - 1 else ''}'>{html.escape(x)}</span>")
    return "<div class='crumbs'>" + "".join(out) + "</div>"

Q1 = "May students use their cell phones during lunch at Claremont schools?"
Q2 = "How many votes did each candidate get in the March 2026 school board election?"
def q(text): return f"<div class='q'><span class='qlabel'>QUESTION</span>{html.escape(text)}</div>"

C = {}
C["title"] = page(f"<div class='wrap' style='justify-content:center'><div class='kicker'>A HOW-TO FROM THE GOVERNMENT TRANSPARENCY PROJECT</div>"
                  f"<h1>{S.TITLE}</h1><p class='lead'>{S.SUBTITLE}</p></div>", dark=True, foot=False)

C["what"] = std("WHAT A SKILL IS", "Written instructions Claude follows for one task",
    "<div class='flow big3'>"
    "<div class='step'><h4>Your question</h4><p>About Claremont School Board policy, in plain words</p></div><div class='ar'>→</div>"
    "<div class='step on'><h4>csb-policy-query</h4><p>Reads the policy index and the documents it links</p></div><div class='ar'>→</div>"
    "<div class='step'><h4>The answer</h4><p>Each statement cited to a policy, or <b>Insufficient Data.</b></p></div></div>")

SECS = [("A", "Foundation and Basic Commitments", 15), ("B", "School Board Governance and Operations", 44),
        ("C", "General School Administration", 6), ("D", "Fiscal Management", 25), ("E", "Support Services", 46),
        ("F", "Facilities Planning and Development", 4), ("G", "Personnel", 36), ("H", "Negotiations", 2),
        ("I", "Instruction", 60), ("J", "Students", 92), ("K", "School-Community-Home Relations", 18),
        ("L", "Education Agency Relations", 2)]
C["index"] = std("THE SOURCE", "One index, about 350 links, twelve sections",
    "<div class='bars'>" + "".join(
        f"<div class='l'>{l}</div><div class='t'>{t}</div><div class='bw'><div class='b' style='width:{n/92*720:.0f}px'></div><div class='n'>{n}</div></div>"
        for l, t, n in SECS) + "</div>"
    "<p class='cite'>Links per section, Claremont School Board Policies index, November 20, 2026</p>", tight=True)

C["scope"] = std("ONE SOURCE ONLY", "What the answers rest on",
    "<div class='two'>"
    "<div class='col yes'><h3>Uses</h3><ul>"
    "<li>The policy index</li><li>Every policy, regulation and form it links</li>"
    "<li>Documents linked from inside those</li><li>Related policies a policy names</li></ul></div>"
    "<div class='col no'><h3>Does not use</h3><ul>"
    "<li>News, minutes, agendas, recordings</li><li>What a cited statute says</li>"
    "<li>Claude's general knowledge</li><li>Web search</li></ul></div></div>")

C["promise"] = std("WHAT YOU GET BACK", "A source for every statement",
    "<div class='two'>"
    "<div class='pol'><div class='d'>WHEN THE POLICIES ANSWER</div><h3>Each statement is cited</h3>"
    "<blockquote>Policy JICJ, Unauthorized Communication Devices, Section J, index date 9/17/2025, section B “Restrictions” (link)</blockquote></div>"
    "<div class='pol'><div class='d'>WHEN THEY DO NOT</div><h3>Two words</h3><div class='big' style='font-size:110px'>Insufficient Data.</div></div>"
    "</div>")

C["step1"] = std("INSTALL · STEP 1 OF 3", "Turn on code execution",
    crumbs("Settings", "Capabilities", "Code execution and file creation") +
    "<p class='note'>Newer versions of the settings page call it <b>Create and edit files</b>.</p>"
    "<p class='note'>Team and Enterprise plans: an owner turns on Skills and code execution first, in "
    "<b>Organization settings › Plugins &amp; skills</b>, Policy tab.</p>")

C["step2"] = std("INSTALL · STEP 2 OF 3", "Upload the skill",
    crumbs("Customize", "Skills", "+", "Create skill", "Upload a skill") +
    "<div style='display:flex;gap:56px;align-items:center'>"
    "<div class='tree'>csb-policy-query.zip<br>└─ csb-policy-query/<br>&nbsp;&nbsp;&nbsp;└─ SKILL.md <i>(the instructions)</i></div>"
    "<p class='strong' style='max-width:720px'>Check that its switch is on. A skill you upload is private to your account.</p></div>")

C["step3"] = std("INSTALL · STEP 3 OF 3", "Connect Google Drive",
    crumbs("Customize", "Connectors", "Google Drive", "Connect") +
    "<p class='note'>Sign in with your Google account. Claude can open only the files that account can open.</p>"
    "<p class='note'>The policy index is shared with anyone who has the link, and so are the policies tested for this video.</p>")

C["ask"] = std("USE", "Ask in plain words",
    q(Q1) + q(Q2) +
    "<p class='cite'>Claude picks the skill on its own when a question fits. Both questions were asked on November 20, 2026; "
    "the answers that follow are the skill's real output.</p>", tight=True)

FLOW = [("1", "Read the index", "Fresh, every time"), ("2", "List every entry", "Code, title, section, date, link"),
        ("3", "Find candidates", "Titles, sections, and a Drive search kept to indexed files"),
        ("4", "Read the best", "Usually three to eight documents"), ("5", "Answer", "Cited, or Insufficient Data")]
FLOW_Q1 = ["Index read November 20, 2026", "350 entries", "Title matches: JICJ, JICAB, JECCA and others",
           "Read JICJ, JICAB, JECCA", "No, with exceptions"]
def flow(detail=None):
    out = []
    for i, (k, h, p) in enumerate(FLOW):
        if i: out.append("<div class='ar'>→</div>")
        out.append(f"<div class='step{' on' if detail else ''}'><div class='k'>{k}</div><h4>{h}</h4><p>{detail[i] if detail else p}</p></div>")
    return "<div class='flow'>" + "".join(out) + "</div>"
C["flow"] = std("BEHIND THE SCENES", "What Claude does with a question", flow())
C["flow_q1"] = std("QUESTION 1 · CELL PHONES AT LUNCH", "The same steps, filled in", flow(FLOW_Q1) +
    "<p class='cite'>The Drive full-text search for this question returned no policy files, so the title match carried it.</p>")

C["answer1"] = std("QUESTION 1 · THE ANSWER", "No, with stated exceptions",
    "<div class='a'><div class='alabel'>ANSWER FROM CSB-POLICY-QUERY</div>"
    "<p>No. Policy JICJ prohibits student use of personal communication devices “from when the first bell rings to start "
    "instructional time until the dismissal bell rings,” and states: “The school day includes lunch periods, passing time, and recesses.” "
    "<span class='c'>(Policy JICJ, Unauthorized Communication Devices, Section J, index date 9/17/2025, section B “Restrictions”)</span></p>"
    "<p>Students with medical needs, disabilities under an IEP or Section 504 plan, or language access services are exempt, and the "
    "superintendent may approve other exceptions. <span class='c'>(JICJ, section C “Exceptions”)</span></p>"
    "<p>The index also lists Policy JICAB (11/17/2010). Neither policy says it replaces the other. "
    "<span class='c'>(Policy JICAB, Electronic Communication/Recording Devices, Section J)</span></p></div>", tight=True)

C["jicj_text"] = page(
    "<div class='wrap tight'><div class='kicker'>THE SOURCE TEXT</div><div class='main' style='justify-content:center'>"
    "<div class='doc'><div class='h'>Claremont School Board Policy JICJ</div>"
    "<div class='tt'>UNAUTHORIZED COMMUNICATION DEVICES</div><div class='s'>B. Restrictions</div>"
    "<p>Student use of personal communication devices is strictly prohibited from when the first bell rings to start instructional "
    "time until the dismissal bell rings to end the academic school day (referred to as “the school day”). "
    "<mark>The school day includes lunch periods, passing time, and recesses.</mark></p>"
    "<p style='margin-top:26px;font-size:26px;color:#555'>District Policy History: First reading/adopted: September 17, 2025</p>"
    "</div></div></div>")

C["overlap"] = std("QUESTION 1 · TWO POLICIES ON ONE SUBJECT", "Both are in the index",
    "<div class='two'>"
    "<div class='pol'><div class='code'>JICJ</div><h3>Unauthorized Communication Devices</h3><div class='d'>ADOPTED SEPTEMBER 17, 2025</div>"
    "<blockquote>Student use of personal communication devices is strictly prohibited … The school day includes lunch periods, passing time, and recesses.</blockquote></div>"
    "<div class='pol'><div class='code'>JICAB</div><h3>Electronic Communication/Recording Devices</h3><div class='d'>ADOPTED NOVEMBER 17, 2010</div>"
    "<blockquote>Permissible uses of electronic devices will be detailed in the School Board approved – Student / Parent Handbooks annually.</blockquote></div>"
    "</div><p class='strong'>Neither says it replaces the other, so the skill reports both, with their dates.</p>", tight=True)

C["q2"] = std("QUESTION 2 · ELECTION RESULTS", "The policies describe elections, not results",
    q(Q2) +
    "<div class='two' style='margin-top:6px'>"
    "<div class='pol'><div class='d'>READ</div><h3>BBB Board Membership-Elections (6/2/2004)</h3>"
    "<blockquote>Members “elected by the qualified voters of the District at the annual District elections held in March.” Terms of three years.</blockquote></div>"
    "<div class='pol'><div class='d'>SET ASIDE</div><h3>Meeting minutes and an agenda</h3>"
    "<p class='cite' style='color:#3D4A5C'>The Drive search found them in the same shared drive, but the index does not link them. They are not policies.</p></div>"
    "</div>", tight=True)

C["answer2"] = page("<div class='wrap' style='justify-content:center;align-items:flex-start'>"
                    "<div class='kicker'>QUESTION 2 · THE ANSWER</div><div class='big'>Insufficient Data.</div>"
                    "<p class='lead'>The answer is not in board policy. Look to another source, such as the election results.</p></div>")

C["cases"] = std("OTHER OUTCOMES", "Four ways an answer can come back",
    rows([("Fully answered", "Answer, with a policy cited for each statement"),
          ("Partly answered", "The supported part, then “Insufficient Data” for the rest"),
          ("Not answered", "“Insufficient Data.” and nothing else"),
          ("A policy will not open", "Names that policy; not reported as Insufficient Data")], "wide"))

C["closing"] = page("<div class='wrap' style='justify-content:center'><div class='kicker'>IN ONE LINE</div>"
                    "<h1>One source.<br>A policy behind every statement.<br>Two words when the policies are silent.</h1></div>",
                    dark=True, foot=False)

C["end"] = page("<div class='wrap' style='justify-content:center'><div class='kicker'>ASKING CLAUDE ABOUT CLAREMONT SCHOOL BOARD POLICY</div>"
                "<h2>Kevin Tyson, Government Transparency Project</h2>"
                "<p class='lead'>November 2026. The skill file, csb-policy-query.zip, goes with this video. Answers come from the "
                "district's published policies only and are not legal advice.</p>"
                "<p class='cite' style='margin-top:36px'>Sources: Claremont School Board Policies index and Policies JICJ, JICAB, JECCA and BBB, "
                "read through the Google Drive connector on November 20, 2026; Claude Help Center, “Use skills in Claude”; "
                "Claude documentation, “Google Drive connector.”</p></div>", dark=True, foot=False)

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
        over = pg.evaluate("() => { const w = document.querySelector('.wrap'); if (!w) return 0;"
                           " const f = document.querySelector('.foot'); const lim = f ? f.getBoundingClientRect().top - 8 : 1080;"
                           " let m = 0; w.querySelectorAll('*').forEach(e => { m = Math.max(m, e.getBoundingClientRect().bottom); });"
                           " return Math.round(m - lim); }")
        pg.screenshot(path=str(CARDS / f"{name}.png")); print("card", name, f"OVERFLOW {over}px" if over > 0 else "")
    if not only:
        pg2 = b.new_context(viewport={"width": 1920, "height": 1080}).new_page()
        for s in S.SEGMENTS:
            if s["kind"] == "narr":
                pg2.set_content(caption(s["text"])); pg2.wait_for_timeout(60)
                pg2.screenshot(path=str(CAPS / f"{s['id']}.png"), omit_background=True)
    b.close()
