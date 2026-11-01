# SPDX-License-Identifier: Apache-2.0
"""Deterministic triage. Runs with no network and no API key, and also feeds
its signals to the Claude triage as hints.

Order of decision (first match wins):
  1. A parent or student asking for their own education records: JRA route.
  2. A named meeting's minutes, agenda, packet or recording that the knowledge
     graph holds: public.
  3. A named Board policy the index holds: public.
  4. Individual student, personnel, attorney or security records: exempt.
  5. Counts or rates about students: aggregate only.
  6. Records kept by another agency: outside Policy EH.
  7. A question or a request to compile something new, with no record named:
     outside RSA 91-A, unless the public record already answers it.
  8. Strong knowledge-graph match: public.
  9. Otherwise: a records search by the custodian.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, timedelta
from urllib.parse import urlencode

from .. import kg as kgmod
from .. import privacy

MONTH_RE = r"(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)"

RECORD_TYPES = {
    "minutes": r"\bminutes\b",
    "agenda": r"\bagendas?\b",
    "packet": r"\bpackets?\b|\bboard materials\b|\bsupporting documents\b",
    "recording": r"\b(video|recording|recorded|footage|broadcast|livestream)\b",
    "budget": r"\bbudgets?\b|\bwarrant\b|\bms-?2[2-7]c?\b",
    "contract": r"\bcontracts?\b|\bagreements?\b|\bmemorandum of understanding\b|\bmou\b",
    "invoice": r"\binvoices?\b|\bbills?\b|\breceipts?\b|\bpurchase orders?\b|\bmanifests?\b|\bcheck register\b|\bexpenditures?\b",
    "audit": r"\baudits?\b|\bauditor'?s?\b|\bcorrective action\b|\bdoe-?25\b",
    "policy": r"\bpolic(?:y|ies)\b|\bby-?laws\b|\bhandbooks?\b|\bprocedures?\b",
    "email": r"\be-?mails?\b|\btext messages?\b|\btexts\b|\bcorrespondence\b|\bcommunications?\b|\bletters?\b|\bmemos?\b|\bmemoranda\b",
    "payroll": r"\bpayroll\b|\bsalar(?:y|ies)\b|\bwages?\b|\bstipends?\b|\bcompensation\b",
    "report": r"\breports?\b|\bpresentations?\b|\bstud(?:y|ies)\b|\bplans?\b|\bproposals?\b|\bbids?\b|\brfps?\b|\brfqs?\b",
}
RECORD_NOUN = re.compile(
    r"\b(records?|documents?|cop(?:y|ies)|files?|spreadsheets?|data|lists?|statements?|ledgers?|logs?)\b|"
    + "|".join(RECORD_TYPES.values()), re.I)

QUESTION_START = re.compile(r"(^|[.!?]\s+)(why|how|what|who|whom|when|where|which|is|are|was|were|does|do|did|can|could|will|would|has|have|should)\b", re.I)
COMPILE = re.compile(
    r"\b(compile|create|prepare|make|generate|build|calculate|tabulate|summari[sz]e|cross-reference|analy[sz]e|"
    r"total up|add up)\b[^.?!]{0,50}\b(lists?|spreadsheets?|summary|summaries|table|analysis|breakdown|totals?|chart|report|tally)\b",
    re.I)
OWN_RECORDS = re.compile(
    r"\b(records?|files?|IEP|504|grades?|report cards?|transcripts?|discipline|disciplinary|attendance|"
    r"evaluations?|cumulative|assessments?|test scores?|progress reports?|notes)\b", re.I)
STUDENT_WORD = re.compile(r"\b(student|pupil|child|kid|minor)'?s?\b", re.I)
AGG_CUE = re.compile(
    r"\b(how many|number of|numbers of|count|counts|percentage|percent|rates?|statistics|stats|totals?|"
    r"aggregate|average|median|by grade|by school|per school|per grade|trend|breakdown)\b", re.I)
STUDENT_SUBJECT = re.compile(
    r"\b(students?|pupils?|enrollment|suspensions?|suspended|expulsions?|expelled|IEPs?|special education|"
    r"504 plans?|english learners?|ELL|homeless|free (?:and|or) reduced|graduat\w*|dropouts?|absences|"
    r"absenteeism|truan\w*|test scores?|proficiency|restraints?|seclusions?|bullying|incidents|referrals|"
    r"out-of-district placements?|class sizes?)\b", re.I)
PERSONNEL = re.compile(
    r"\b(personnel files?|employee files?|personnel records?|disciplinary (?:records?|actions?|history)|"
    r"performance (?:evaluations?|reviews?)|evaluations? of (?:the |a )?(?:superintendent|principal|teacher|employee|staff|coach|director)|"
    r"complaints? (?:against|about) (?:a |the |an )?(?:teacher|employee|staff|principal|coach|director|superintendent|bus driver|para)|"
    r"investigation (?:of|into) (?:a |the |an )?(?:teacher|employee|staff|coach|principal|director)|"
    r"background checks?|criminal records? check|medical (?:records?|leave)|fmla|workers'? comp\w*|"
    r"why (?:was|were) \w+(?: \w+)? (?:fired|terminated|dismissed|placed on leave|let go))\b", re.I)
ATTORNEY = re.compile(
    r"\b(legal (?:advice|opinions?|memos?|memoranda)|(?:attorney|counsel|lawyer|law firm)'?s? "
    r"(?:advice|opinions?|memos?|memoranda|communications?|letters?|e-?mails?|work product)|"
    r"communications? (?:with|from|to) (?:the )?(?:district'?s? )?(?:attorney|counsel|lawyer|law firm))\b", re.I)
SECURITY = re.compile(
    r"\b(security plans?|emergency (?:operations|response|management) plans?|school safety plans?|"
    r"camera locations?|locations? of (?:security )?cameras|surveillance (?:footage|video)|security (?:camera )?footage|"
    r"network (?:diagrams?|maps?)|passwords?|vulnerability (?:assessments?|scans?)|cyber ?security plans?|"
    r"penetration tests?|lockdown procedures?)\b", re.I)
OTHER_AGENCY = [
    ("City of Claremont", re.compile(
        r"\b(city of claremont|claremont city (?:council|manager|hall|clerk)|city manager|city clerk|"
        r"claremont police|police (?:reports?|department|records?)|fire department|tax assessor|"
        r"planning board|zoning board|city'?s (?:budget|records?|minutes))\b", re.I)),
    ("New Hampshire Department of Education", re.compile(
        r"\b(?:nh|new hampshire) (?:department of education|doe)\b|\bstate board of education\b|"
        r"\beducator certification\b", re.I)),
    ("New Hampshire Department of Revenue Administration", re.compile(
        r"\b(?:nh|new hampshire) (?:department of revenue|dra)\b", re.I)),
    ("Sullivan County", re.compile(r"\bsullivan county (?:commission|delegation|attorney|sheriff|records?)\b", re.I)),
]
BULK_ECOMMS = re.compile(
    r"\b(all|every|any)\s+(?:of the\s+)?(e-?mails?|text messages?|texts|messages|communications|correspondence)\b|"
    r"\be-?mails?\s+(?:between|among|from|to)\b", re.I)
POLICY_CODE = re.compile(r"\b[Pp]olic(?:y|ies)\s+([A-L][A-Z]{0,4}(?:-[A-Z0-9()]+)?)(?![a-z])|\b([A-L][A-Z]{1,4}(?:-R\(?\d?\)?)?)\s+[Pp]olic(?:y|ies)\b")
DISCUSSION_Q = re.compile(r"\b(say|said|discuss\w*|report(?:ed)?|present\w*|mention\w*|told|explain\w*|decid\w*|vote\w*)\b", re.I)
LAST_MEETING = re.compile(r"\b(last|latest|most recent|previous)\s+(?:school\s+)?(?:board\s+)?meeting\b", re.I)
REQUEST_VERB = re.compile(
    r"\b(send|provide|cop(?:y|ies)|produce|inspect|obtain|release|requesting|request a|request the|request all|"
    r"i (?:would like|want|need|am asking for|ask for)|please)\b", re.I)
WHY_HOW = re.compile(r"^\s*(why|how come|how|what is the reason|who decided|is it true)\b", re.I)
SELF_STUDENT = re.compile(
    r"\b(?:i am|i'm|i was) (?:a |an )?(?:current |former )?(?:student|graduate|alumn\w*|senior|junior)\b|"
    r"\bmy (?:own )?(?:transcripts?|diplomas?|report cards?|grades|IEP|504 plan|student (?:file|records?)|"
    r"school records?|education(?:al)? records?|cumulative (?:file|folder))\b", re.I)
FINANCE = re.compile(r"\b(tuition|costs?|spent|spending|paid|pay(?:ing|ments?)|price|fees?|dollars?|\$\d|"
                     r"expenses?|funding|grants?|reimburse\w*)\b", re.I)
CITING_POLICY = re.compile(r"\b(?:pursuant to|under|per|in accordance with|according to|consistent with)\s+"
                           r"(?:RSA\s*91-A[:\d,() IVX]*\s*(?:and|,)\s*)?(?:the\s+)?(?:board\s+)?[Pp]olic(?:y|ies)\s+"
                           r"([A-L][A-Z]{0,4}(?:-[A-Z0-9()]+)?)")
MEETING_TYPES = {"minutes", "agenda", "packet", "recording"}
THUMB_DRIVE = re.compile(r"\b(thumb ?drive|usb|flash drive|memory stick|external (?:hard )?drive)\b", re.I)
FREE_COPIES = re.compile(r"\b(free (?:of charge|copies)|without (?:charge|cost)|no (?:charge|cost)|waive\w* (?:the |any )?fees?)\b", re.I)
DRAFT = re.compile(r"\b(drafts?|preliminary|working copy|notes taken by)\b", re.I)


@dataclass
class Signals:
    question_form: bool = False
    compile_request: bool = False
    own_child: bool = False
    student_individual: bool = False
    student_aggregate: bool = False
    personnel: bool = False
    attorney: bool = False
    security: bool = False
    other_agency: str | None = None
    bulk_ecomms: bool = False
    mentions_draft: bool = False
    last_meeting: bool = False
    asks_about_discussion: bool = False
    record_types: list[str] = field(default_factory=list)
    named_record: bool = False
    policy_codes: list[str] = field(default_factory=list)
    dates: list[str] = field(default_factory=list)
    date_from: str | None = None
    date_to: str | None = None
    terms: list[str] = field(default_factory=list)

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items()}


# ---------------------------------------------------------------- dates

def _mk(y, m, d):
    try:
        return date(y, m, d)
    except ValueError:
        return None


def extract_dates(text: str, today: date) -> tuple[list[str], str | None, str | None]:
    t = text
    specific: list[date] = []
    ranges: list[tuple[date, date]] = []
    for m in re.finditer(MONTH_RE + r"\.?\s+(\d{1,2})(?:st|nd|rd|th)?(?:,?\s+(\d{4}))?", t, re.I):
        mon = kgmod.MONTHS.get(m.group(1).lower().rstrip("."), kgmod.MONTHS.get(m.group(1).lower()[:3]))
        day = int(m.group(2))
        if m.group(3):
            dd = _mk(int(m.group(3)), mon, day)
        else:
            dd = _mk(today.year, mon, day)
            if dd and dd > today:
                dd = _mk(today.year - 1, mon, day)
        if dd:
            specific.append(dd)
    for m in re.finditer(r"\b(\d{1,2})[/.](\d{1,2})[/.](\d{2}|\d{4})\b", t):
        y = int(m.group(3))
        y = y + 2000 if y < 100 else y
        dd = _mk(y, int(m.group(1)), int(m.group(2)))
        if dd:
            specific.append(dd)
    for m in re.finditer(r"\b(20\d\d)-(\d\d)-(\d\d)\b", t):
        dd = _mk(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        if dd:
            specific.append(dd)
    # Month and year with no day: "September 2026"
    for m in re.finditer(MONTH_RE + r"\.?\s+(?:of\s+)?(\d{4})\b", t, re.I):
        mon = kgmod.MONTHS.get(m.group(1).lower(), kgmod.MONTHS.get(m.group(1).lower()[:3]))
        y = int(m.group(2))
        start = date(y, mon, 1)
        end = (date(y + (mon == 12), mon % 12 + 1, 1) - timedelta(days=1))
        ranges.append((start, end))
    # Fiscal years: FY25, FY 2025, fiscal year 2025 (NH school fiscal year ends June 30)
    for m in re.finditer(r"\b(?:fy|fiscal year)\s?'?(\d{2}|\d{4})\b", t, re.I):
        y = int(m.group(1))
        y = y + 2000 if y < 100 else y
        ranges.append((date(y - 1, 7, 1), date(y, 6, 30)))
    # Bare years
    for m in re.finditer(r"(?<![/\-\d])\b(20[0-3]\d|199\d)\b(?![/\-]\d)", t):
        y = int(m.group(1))
        if not any(r[0].year <= y <= r[1].year for r in ranges) and not any(s.year == y for s in specific):
            ranges.append((date(y, 1, 1), date(y, 12, 31)))
    if re.search(r"\b(last|past|previous)\s+(12 months|year)\b", t, re.I):
        ranges.append((today - timedelta(days=365), today))
    dates = sorted({d.isoformat() for d in specific})
    lo = [d for d in specific] + [r[0] for r in ranges]
    hi = [d for d in specific] + [r[1] for r in ranges]
    return dates, (min(lo).isoformat() if lo else None), (max(hi).isoformat() if hi else None)


# ---------------------------------------------------------------- signals

def extract_signals(text: str, today: date) -> Signals:
    s = Signals()
    low = text.lower()
    s.record_types = [k for k, rx in RECORD_TYPES.items() if re.search(rx, low, re.I)]
    s.named_record = bool(RECORD_NOUN.search(text))
    qs = len(re.findall(r"\?", text)) + len(QUESTION_START.findall(text.strip()))
    asks_for_record = bool(REQUEST_VERB.search(text))
    # A question is still a question when it mentions a record ("why is the audit late?"),
    # unless it also asks for a copy of something.
    s.question_form = qs > 0 and (not s.named_record or (bool(WHY_HOW.search(text)) and not asks_for_record))
    s.compile_request = bool(COMPILE.search(text))
    child = privacy.CHILD_REF.search(text)
    s.own_child = bool(child and OWN_RECORDS.search(text)) or bool(SELF_STUDENT.search(text))
    finance = bool({"budget", "contract", "invoice", "payroll"} & set(s.record_types)) or bool(FINANCE.search(text))
    s.student_aggregate = bool(AGG_CUE.search(text) and STUDENT_SUBJECT.search(text)) and not finance
    names = privacy._names_near_sensitive(text)
    s.student_individual = (not s.own_child and not s.student_aggregate and
                            bool(STUDENT_WORD.search(text)) and bool(privacy.SENSITIVE.search(text)) and
                            bool(names or re.search(r"\b(the|that|this|a) (student|pupil|child)\b", text, re.I)))
    s.personnel = bool(PERSONNEL.search(text))
    s.attorney = bool(ATTORNEY.search(text))
    s.security = bool(SECURITY.search(text))
    for name, rx in OTHER_AGENCY:
        if rx.search(text):
            s.other_agency = name
            break
    s.bulk_ecomms = bool(BULK_ECOMMS.search(text))
    s.mentions_draft = bool(DRAFT.search(text))
    s.last_meeting = bool(LAST_MEETING.search(text))
    s.asks_about_discussion = bool(DISCUSSION_Q.search(text))
    cited = {m.group(1).upper() for m in CITING_POLICY.finditer(text)}
    codes = []
    for m in POLICY_CODE.finditer(text):
        c = (m.group(1) or m.group(2) or "").upper()
        if c and c not in codes and c not in {"I", "A"} and c not in cited:
            codes.append(c)
    s.policy_codes = codes
    s.dates, s.date_from, s.date_to = extract_dates(text, today)
    clean = privacy.strip_contacts(text)
    terms = kgmod.tokens(re.sub(r"\b\d{1,2}[/.]\d{1,2}[/.]\d{2,4}\b", " ", clean))
    if s.date_from:
        terms = [t for t in terms if not t.isdigit() and t not in kgmod.MONTHS and not re.fullmatch(r"fy\d{2,4}", t)]
    s.terms = terms
    return s


# ---------------------------------------------------------------- triage

def reason(code: str, explanation: str, citations: list[str]) -> dict:
    return {"code": code, "explanation": explanation, "citations": citations}


def search_url(base_url: str, q: str, date_from=None, date_to=None, kinds=None) -> str:
    params = [("q", q)]
    if date_from:
        params.append(("from", date_from))
    if date_to:
        params.append(("to", date_to))
    for k in kinds or []:
        params.append(("kind", k))
    return f"{base_url}/kg/search?{urlencode(params)}"


def _meeting_resources(kg, s: Signals, today: date) -> list[dict]:
    """Meetings on the request's specific dates, with the resource types asked for."""
    wanted = {"minutes", "agenda", "packet", "recording"} & set(s.record_types)
    if not wanted or not kg.available:
        return []
    dates = list(s.dates)
    if not dates and s.last_meeting:
        recent = kg.meetings_between((today - timedelta(days=120)).isoformat(), today.isoformat())
        if recent:
            dates = [recent[-1]["date"]]
    out = []
    for d in dates:
        for m in kg.meetings_between(d, d):
            res = kg.meeting_resources(m["id"])
            picked = []
            for r in res:
                k = r["kind"]
                if k == "meeting" or (k == "minutes" and "minutes" in wanted and r["extra"].get("own")) or \
                   (k == "agenda" and "agenda" in wanted) or (k == "recording" and "recording" in wanted) or \
                   (k == "folder" and "packet" in wanted) or (k == "document" and "packet" in wanted):
                    picked.append(r)
            has_minutes = any(r["kind"] == "minutes" and r["extra"].get("own") for r in res)
            out.append({"meeting": m, "resources": picked, "wanted": sorted(wanted), "has_minutes": has_minutes})
    return out


def triage(req: dict, settings, kg, forced: str | None = None, today: date | None = None) -> dict:
    """req: dict with at least text, public_id, received_at (ISO) fields."""
    text = req["text"]
    today = today or date.today()
    s = extract_signals(text, today)
    reasons: list[dict] = []
    notes: list[str] = []
    missing: list[str] = []
    resources = _meeting_resources(kg, s, today)
    q = " ".join(s.terms[:16])
    hits = kg.search(q, date_from=s.date_from, date_to=s.date_to, limit=10, dialogue_limit=3) if (kg.available and q) else []
    policy_hits = []
    for code in s.policy_codes:
        policy_hits += kg.policy(code) if kg.available else []
    strong = [h for h in hits if h.kind != "dialogue" and h.coverage >= 0.75 and len(s.terms) >= 2]
    # Record types the knowledge graph cannot hold. When one is asked for, a match on
    # a meeting or a policy answers only part of the request and must not end triage.
    other_types = set(s.record_types) - MEETING_TYPES - {"report"}
    if s.bulk_ecomms:
        other_types.add("email")
    category = None
    confidence = "medium"

    if s.own_child:
        category, confidence = "outside_policy", "high"
        reasons.append(reason("jra_own_records",
            "A parent or eligible student asking for the student's own education records uses Policy JRA, "
            "through the building principal, with access within 14 days. That is a FERPA access right, "
            "separate from RSA 91-A, and RSA 91-A:5, III keeps pupil records out of the public-records route.",
            ["policy-jra", "rsa189-66-iv", "ferpa", "rsa91a-5-iii"]))
    elif resources and any(r["resources"] for r in resources) and not other_types:
        category, confidence = "public_info", "high"
        reasons.append(reason("meeting_resources",
            "The request names a meeting whose records the Meeting Navigator already links: "
            + "; ".join(r["meeting"]["title"] for r in resources) + ".",
            ["rsa91a-4-iv-a", "policy-eh-r1"]))
        if "minutes" in resources[0]["wanted"] and not any(r["has_minutes"] for r in resources):
            missing.append("minutes")
            notes.append("The knowledge graph has no minutes for this meeting. RSA 91-A:2, II makes minutes "
                         "available within 5 business days of the meeting. Find them, or say when they will be "
                         "available; the draft has a placeholder that blocks sending until you do.")
    elif policy_hits and not (other_types - {"policy", "report"}) and not s.bulk_ecomms:
        category, confidence = "public_info", "high"
        reasons.append(reason("policy_public",
            "The request names a Board policy that is posted in the District's public policy index.",
            ["rsa91a-4-iv-a", "policy-eh-r1"]))
    elif s.student_individual or s.personnel or s.attorney or s.security:
        category, confidence = "outside_rsa", "medium"
        if s.student_individual:
            reasons.append(reason("exempt_pupil",
                "The records you describe are about an individual student. Personal school records of pupils are "
                "exempt from public disclosure, and federal law (FERPA) bars releasing personally identifiable "
                "information from education records without consent.", ["rsa91a-5-iii", "ferpa", "rsa91a-4-iv-c"]))
            notes.append("If the requester is the student's parent or the student, reclassify as outside_policy: "
                         "Policy JRA gives them access through the principal.")
        if s.personnel:
            reasons.append(reason("exempt_personnel",
                "The records you describe are personnel, evaluation, complaint, investigation or medical records "
                "about an employee. RSA 91-A:5, IV exempts records whose disclosure would invade personal privacy. "
                "The District weighed the employee's privacy interest against the public interest in disclosure "
                "and [[state the result of that balancing for these records, and what if anything is released "
                "with redactions]].",
                ["rsa91a-5-iv", "rsa91a-4-iv-c"]))
            notes.append("Legal review recommended before sending. Policy GBJ governs personnel records. Since 2020 "
                         "most personnel records need a privacy balancing test, not a categorical refusal, and some "
                         "(for example, records of misconduct findings) may have to be released with redactions. "
                         "Personnel exemptions now turn on a balancing "
                         "test (Union Leader v. Town of Salem; Seacoast Newspapers v. Portsmouth, both 2020). "
                         "Consider partial release with redaction (RSA 91-A:4, IV protects good-faith redaction) rather than a full denial.")
        if s.attorney:
            reasons.append(reason("exempt_attorney",
                "The records you describe are legal advice or communications with the District's lawyers, which "
                "RSA 91-A:5, XII exempts as attorney-client privileged or attorney work product.",
                ["rsa91a-5-xii", "rsa91a-4-iv-c"]))
            notes.append("Legal invoices and engagement letters are usually public with privileged detail redacted; "
                         "if the request reaches them, release them rather than deny.")
        if s.security:
            reasons.append(reason("exempt_security",
                "The records you describe are security, emergency-response or information-technology records "
                "whose release could aid an attack or a security breach.", ["rsa91a-5-vi", "rsa91a-5-xi", "rsa91a-4-iv-c"]))
    elif s.student_aggregate and s.asks_about_discussion and strong:
        category, confidence = "public_info", "medium"
        reasons.append(reason("kg_match",
            "The request asks what was said or reported about student figures, and the public meeting record "
            "covers it.", ["rsa91a-4-iv-a", "policy-eh-r1"]))
        notes.append("The request touches student figures. If the requester wants the underlying data rather "
                     "than what was said at the meeting, reclassify as aggregate_only.")
    elif s.student_aggregate:
        category, confidence = "aggregate_only", "medium"
        reasons.append(reason("aggregate_only",
            "The request asks for counts or rates about students. Individual records are exempt, so the answer "
            "can only be anonymized or aggregated figures, with small counts suppressed so no student can be "
            "identified. The District need not create a new compilation, but it can release figures it already "
            "keeps or reports.", ["rsa91a-5-iii", "ferpa", "policy-jra", "rsa91a-4-vii"]))
    elif s.other_agency and not strong:
        category, confidence = "outside_policy", "medium"
        reasons.append(reason("other_custodian",
            f"The records described appear to be kept by {s.other_agency}, not the District. Policy EH makes the "
            "Superintendent custodian of District records only; the request should go to the agency that keeps "
            "the records.", ["policy-eh", "rsa91a-1a-v"]))
    elif (s.question_form or s.compile_request) and not strong:
        category, confidence = "outside_rsa", "medium"
        if s.question_form:
            reasons.append(reason("question_not_record",
                "The request asks a question rather than describing a record. RSA 91-A gives access to "
                "governmental records reasonably described; it does not require staff to answer questions or "
                "explain decisions.", ["rsa91a-4-i", "rsa91a-4-iv-a", "rsa91a-4-iv-e"]))
        if s.compile_request:
            reasons.append(reason("compile_new_record",
                "The request asks the District to compile or create a new list, summary or analysis. RSA 91-A "
                "does not require an agency to assemble information into a form it does not already keep.",
                ["rsa91a-4-vii", "rsa91a-4-iv-e"]))
    elif strong and not (other_types & {"email", "contract", "invoice", "payroll"}):
        category, confidence = "public_info", "medium" if strong[0].coverage < 1 else "high"
        reasons.append(reason("kg_match",
            "Public records in the Meeting Navigator match the request.", ["rsa91a-4-iv-a", "policy-eh-r1"]))
        if s.question_form:
            notes.append("The request is phrased as a question. RSA 91-A does not require an answer, but the public "
                         "record appears to cover it, so the draft points to where.")
    else:
        category, confidence = "records_search", "medium"
        reasons.append(reason("custodian_search",
            "The request describes District records that are not in the public knowledge graph. The custodian "
            "must locate them, review them for exempt material and respond in writing within 5 business days.",
            ["rsa91a-4-iv-b", "policy-eh-r1"]))

    public_parts = []
    if category != "public_info" and resources:
        for r in resources:
            for x in r["resources"]:
                public_parts.append({"ref": x["ref"], "kind": x["kind"], "title": x["title"], "url": x["url"],
                                     "date": x.get("date"), "snippet": "", "meeting_title": r["meeting"]["title"]})
        if public_parts:
            notes.append("Part of the request is already public (meeting records listed in the draft); the rest "
                         "needs a records search.")
    if s.bulk_ecomms:
        notes.append("Possible bulk electronic communications. Policy EH-R(1): no charge for the first 250 "
                     "individual electronic communications, then $1.00 each, paid in advance; requests from the "
                     "same person within 30 days are aggregated; waiver by Form EH-F(1). Give an itemized estimate "
                     "in the 5-day response (RSA 91-A:4, IV(b)).")
    if THUMB_DRIVE.search(text):
        notes.append("Asks for delivery on a storage device. Procedure EH-R(1): a thumb drive must be supplied in "
                     "unopened manufacturer's packaging or bought from the District at cost.")
    if FREE_COPIES.search(text):
        notes.append("Asks for free copies or a fee waiver. Inspection and electronic delivery are free; paper "
                     "copies cost $0.25 to $1.00 a page under Procedure EH-R(1); the per-communication charge "
                     "beyond 250 can be waived on Form EH-F(1).")
    if s.mentions_draft:
        notes.append("Mentions drafts or notes. RSA 91-A:5, IX exempts only drafts not circulated to a quorum or "
                     "majority of the body; drafts that went to the Board in a packet are public.")
    if s.other_agency and category != "outside_policy":
        notes.append(f"Mentions {s.other_agency}; some of the records may be kept there rather than by the District.")
    if s.compile_request and category not in ("outside_rsa",):
        notes.append("Part of the request asks for a new compilation (RSA 91-A:4, VII); the draft offers existing records.")

    if forced:
        if forced != category:
            notes.insert(0, f"Category set by staff to '{forced}' (rules engine suggested '{category}').")
        category = forced
        confidence = "staff"

    kg_q = q
    url = search_url(settings.base_url, kg_q, s.date_from, s.date_to) if kg_q else None

    used_hits = []
    if category == "public_info":
        if resources:
            for r in resources:
                for x in r["resources"]:
                    used_hits.append({"ref": x["ref"], "kind": x["kind"], "title": x["title"], "url": x["url"],
                                      "date": x.get("date"), "snippet": "", "meeting_title": r["meeting"]["title"]})
        for p in policy_hits:
            used_hits.append({"ref": p["ref"], "kind": "policy", "title": p["title"], "url": p["url"],
                              "date": None, "snippet": "", "meeting_title": None})
        if not used_hits:
            used_hits = [h.to_dict() for h in (strong[:6] + [h for h in hits if h.kind == "dialogue"][:2])]
    else:
        used_hits = [h.to_dict() for h in hits[:6]]
    for h in used_hits:
        h["snippet"] = (h.get("snippet") or "").replace("\x02", "").replace("\x03", "")

    prompt = reproducible_prompt(text, s, settings)
    return {
        "engine": "rules",
        "category": category,
        "confidence": confidence,
        "reasons": reasons,
        "review_notes": notes,
        "signals": s.to_dict(),
        "kg": {"query": kg_q, "date_from": s.date_from, "date_to": s.date_to, "url": url,
               "available": kg.available},
        "hits": used_hits,
        "all_hits": [h.to_dict() | {"snippet": h.snippet.replace("\x02", "").replace("\x03", "")} for h in hits],
        "prompt": prompt,
        "missing": missing,
        "public_parts": public_parts,
    }


def reproducible_prompt(text: str, s: Signals, settings) -> str:
    if s.date_from and s.date_from == s.date_to:
        span = f" for the meeting of {s.date_from}"
    elif s.date_from and s.date_to:
        span = f" dated {s.date_from} through {s.date_to}"
    else:
        span = ""
    kinds = ", ".join(s.record_types) if s.record_types else "meeting pages, packet documents, minutes and recordings"
    generic = set(RECORD_TYPES) | {"video", "meeting", "meetings", "board", "school", "claremont", "district",
                                   "send", "copy", "copies", "recording", "minutes", "agenda", "packet"}
    subject = " ".join(t for t in s.terms if t not in generic)[:160]
    about = f" about {subject}" if subject else ""
    return (
        "Using the Claremont School Board Meeting Navigator knowledge graph "
        "(https://github.com/kevin-tyson/CSBMN: Input/SupportingDocuments/MAP.md, the meeting pages in "
        "Output/HTML and the dialogue CSVs in Output/HTML/Dialogue), find the "
        f"{kinds}{span}{about}. "
        "For each match give the record's title, meeting date and link, and quote the passage that answers "
        "the request with its Cablecast timestamp link. Say plainly if nothing in the record answers it."
    )
