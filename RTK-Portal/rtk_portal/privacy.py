# SPDX-License-Identifier: Apache-2.0
"""Screen request text before it goes in the public log.

Contact details (email, phone, SSN-like numbers) are always masked in the
public copy. Text that seems to identify a student or other private person
(a parent naming a child, a date of birth, a student ID, a named person next
to a sensitive record word) is held back from the public log until staff
publish a redacted copy. Holding is cautious by design: a false positive only
delays publication of the text; the request's dates and status stay public.
"""

from __future__ import annotations

import re

EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
PHONE = re.compile(r"(?<!\d)(?:\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}(?!\d)")
SSN = re.compile(r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)")

CHILD_REF = re.compile(
    r"\bmy\s+(?:\d+(?:st|nd|rd|th)?[- ]grade\s+)?"
    r"(son|daughter|child|children|kid|kids|grandson|granddaughter|grandchild|stepson|stepdaughter|"
    r"foster child|ward|student)\b",
    re.I,
)
DOB = re.compile(r"\b(date of birth|d\.?o\.?b\.?|born on)\b", re.I)
STUDENT_ID = re.compile(r"\b(student|sasid|lunch)\s*(id|number|no\.?|#)\b", re.I)
SENSITIVE = re.compile(
    r"\b(IEP|504 plan|discipline|disciplinary|suspen\w+|expul\w+|diagnos\w+|medical|"
    r"counsel(?:ing|or)|evaluation|grades?|report card|transcript|attendance record|"
    r"special education|behavior plan|investigation|complaint against|harass\w+)\b",
    re.I,
)
# Two capitalized words in a row, not at a sentence start, as a rough person-name cue.
NAME = re.compile(r"(?<![.!?]\s)(?<!^)\b([A-Z][a-z]{1,20})\s+([A-Z][a-z]{1,20})\b")
NOT_NAMES = {
    "School", "Board", "District", "Claremont", "Stevens", "High", "Middle", "Elementary",
    "Superintendent", "Policy", "City", "Council", "New", "Hampshire", "Right", "Know",
    "Finance", "Committee", "Sullivan", "County", "Department", "Education", "Bluff",
    "Disnard", "Maple", "Avenue", "Street", "January", "February", "March", "April", "May",
    "June", "July", "August", "September", "October", "November", "December", "Monday",
    "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Community",
    "Television", "Media", "Center", "Navigator", "Unit", "Regional", "Technical", "River",
    "Valley", "Career", "Technology", "Business", "Administrator", "Capital", "Improvement",
}


SELF_STUDENT = re.compile(
    r"\b(?:i am|i'm|i was) (?:a |an )?(?:current |former )?(?:student|graduate|alumn\w*|senior|junior)\b|"
    r"\bmy (?:own )?(?:transcripts?|report cards?|grades|IEP|504 plan|student (?:file|records?)|"
    r"education(?:al)? records?)\b", re.I)


def strip_contacts(text: str) -> str:
    """Remove contact details outright (for building search terms)."""
    return PHONE.sub(" ", SSN.sub(" ", EMAIL.sub(" ", text)))


def mask(text: str) -> str:
    text = EMAIL.sub("[email removed]", text)
    text = SSN.sub("[number removed]", text)
    text = PHONE.sub("[phone removed]", text)
    return text


def _names_near_sensitive(text: str) -> list[str]:
    hits = []
    for m in NAME.finditer(text):
        a, b = m.group(1), m.group(2)
        if a in NOT_NAMES or b in NOT_NAMES:
            continue
        window = text[max(0, m.start() - 120): m.end() + 120]
        if SENSITIVE.search(window):
            hits.append(m.group(0))
    return hits


def screen(text: str) -> tuple[bool, list[str], str]:
    """Return (hold, reasons, masked_text)."""
    reasons = []
    if CHILD_REF.search(text):
        reasons.append("refers to the requester's own child or student")
    if SELF_STUDENT.search(text):
        reasons.append("refers to the requester's own student records")
    if DOB.search(text):
        reasons.append("mentions a date of birth")
    if STUDENT_ID.search(text):
        reasons.append("mentions a student identifier")
    names = _names_near_sensitive(text)
    if names:
        reasons.append("names a person next to a sensitive record term")
    return bool(reasons), reasons, mask(text)
