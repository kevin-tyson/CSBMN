# SPDX-License-Identifier: Apache-2.0
"""The closed list of authorities the triage engine may cite.

A draft may cite only an id in CITATIONS. The gists are paraphrases written
for staff, not quotations; each entry links the primary text. Entries were
checked against their sources on 2026-10-30 (see VERIFIED_ON). Keep this file
in step with RSA 91-A and Board policy: when the law or a policy changes,
update the entry and its date here before relying on it in a draft.
"""

from __future__ import annotations

from dataclasses import dataclass

VERIFIED_ON = "2026-10-30"

RSA = "https://gc.nh.gov/rsa/html/VI/91-A/"


@dataclass(frozen=True)
class Citation:
    id: str
    label: str
    url: str
    gist: str
    kind: str = "statute"  # statute | policy | case | federal


_C = [
    # RSA 91-A
    Citation("rsa91a-1", "RSA 91-A:1", RSA + "91-A-1.htm",
             "Purpose of the chapter: the greatest possible public access to the actions, "
             "discussions and records of public bodies, and their accountability to the people."),
    Citation("rsa91a-1a-iii", "RSA 91-A:1-a, III", RSA + "91-A-1-a.htm",
             "Defines governmental records as information created, accepted or obtained by or "
             "for a public body or agency in furtherance of its official function, in any form."),
    Citation("rsa91a-1a-v", "RSA 91-A:1-a, V", RSA + "91-A-1-a.htm",
             "Public agency includes any school district and school administrative unit."),
    Citation("rsa91a-2-ii", "RSA 91-A:2, II", RSA + "91-A-2.htm",
             "Minutes of a public meeting must be open to public inspection not more than "
             "5 business days after the meeting."),
    Citation("rsa91a-4-i", "RSA 91-A:4, I", RSA + "91-A-4.htm",
             "Every citizen may inspect and copy governmental records during regular business "
             "hours, except as otherwise prohibited by statute or RSA 91-A:5."),
    Citation("rsa91a-4-iv-a", "RSA 91-A:4, IV(a)", RSA + "91-A-4.htm",
             "On request for a governmental record reasonably described, the agency makes "
             "it available immediately when it is immediately available for release."),
    Citation("rsa91a-4-iv-b", "RSA 91-A:4, IV(b)", RSA + "91-A-4.htm",
             "If a record is not immediately available, within 5 business days the agency must "
             "make it available, deny the request in writing, or state in writing the time "
             "reasonably needed and why, with an itemized cost estimate if a paragraph VIII "
             "charge will apply."),
    Citation("rsa91a-4-iv-c", "RSA 91-A:4, IV(c)", RSA + "91-A-4.htm",
             "A denial in whole or in part must state the specific exemption and briefly "
             "explain how it applies to the record withheld."),
    Citation("rsa91a-4-iv-e", "RSA 91-A:4, IV(e)", RSA + "91-A-4.htm",
             "The agency may suggest a reasonable modification of the scope of a request; the "
             "requester need not accept it."),
    Citation("rsa91a-4-vii", "RSA 91-A:4, VII", RSA + "91-A-4.htm",
             "The chapter does not require an agency to compile, cross-reference or assemble "
             "information into a form in which it is not already kept or reported."),
    Citation("rsa91a-4-viii", "RSA 91-A:4, VIII", RSA + "91-A-4.htm",
             "A fee of up to $1.00 per electronic communication may be charged only beyond the "
             "first 250 in a request; requests from one person to the same body within 30 days "
             "count as one; the agency must adopt a fee policy."),
    Citation("rsa91a-4-ix", "RSA 91-A:4, IX", RSA + "91-A-4.htm",
             "The per-communication fee is waived for indigent requesters and for requests in "
             "the public interest that are not primarily commercial."),
    Citation("rsa91a-5-iii", "RSA 91-A:5, III", RSA + "91-A-5.htm",
             "Exempts personal school records of pupils."),
    Citation("rsa91a-5-iv", "RSA 91-A:5, IV", RSA + "91-A-5.htm",
             "Exempts internal personnel practices, confidential commercial or financial "
             "information, and personnel, medical, welfare and other files whose disclosure "
             "would invade privacy. Most of these categories require a balancing test, not a "
             "categorical refusal (see the 2020 Supreme Court cases)."),
    Citation("rsa91a-5-vi", "RSA 91-A:5, VI", RSA + "91-A-5.htm",
             "Exempts records of emergency functions developed by safety officials to thwart "
             "deliberate acts that could cause widespread damage, injury or loss of life."),
    Citation("rsa91a-5-vii", "RSA 91-A:5, VII", RSA + "91-A-5.htm",
             "Exempts unique pupil identification information under RSA 193-E:5."),
    Citation("rsa91a-5-viii", "RSA 91-A:5, VIII", RSA + "91-A-5.htm",
             "Exempts notes or materials made for personal use that have no official purpose."),
    Citation("rsa91a-5-ix", "RSA 91-A:5, IX", RSA + "91-A-5.htm",
             "Exempts preliminary drafts and notes not in final form and not disclosed, "
             "circulated or available to a quorum or majority of a public body."),
    Citation("rsa91a-5-xi", "RSA 91-A:5, XI", RSA + "91-A-5.htm",
             "Exempts information technology records, such as cybersecurity plans and "
             "vulnerability assessments, whose release would aid a security breach."),
    Citation("rsa91a-5-xii", "RSA 91-A:5, XII", RSA + "91-A-5.htm",
             "Exempts records protected by attorney-client privilege or the attorney work "
             "product doctrine."),
    Citation("rsa91a-7", "RSA 91-A:7", RSA + "91-A-7.htm",
             "A person aggrieved by a violation of the chapter may petition the superior court "
             "for relief."),
    Citation("rsa189-66-iv", "RSA 189:66, IV", "https://gc.nh.gov/rsa/html/XV/189/189-66.htm",
             "Among the rights the district must publish: a parent's right to inspect and review "
             "the student's education records within 14 days of a request."),
    Citation("rsa288-1", "RSA 288:1", "https://gencourt.state.nh.us/rsa/html/XXV/288/288-mrg.htm",
             "New Hampshire legal holidays, used by the portal's business-day calendar."),
    # Federal
    Citation("ferpa", "20 U.S.C. 1232g (FERPA)", "https://www.law.cornell.edu/uscode/text/20/1232g",
             "Federal student-privacy law: personally identifiable information from education "
             "records may not be released without consent except as the statute allows.",
             kind="federal"),
    # Cases
    Citation("case-salem", "Union Leader Corp. v. Town of Salem (N.H. May 29, 2020)",
             "https://www.nhmunicipal.org/court-update/internal-personnel-practices-are-not-se-exempt-disclosure-exempt-if-disclosure",
             "Overruled Fenniman (1993) to the extent it treated internal personnel practices "
             "as categorically exempt; such records now go through a privacy balancing test.",
             kind="case"),
    Citation("case-seacoast", "Seacoast Newspapers v. City of Portsmouth (N.H. May 29, 2020)",
             "https://www.aclu-nh.org/cases/seacoast-newspapers-inc-v-city-portsmouth/",
             "Narrowed the internal personnel practices exemption to records of the internal "
             "rules and practices governing an agency's operations and employee relations.",
             kind="case"),
    # Claremont School Board policy
    Citation("policy-eh", "Claremont School Board Policy EH",
             "https://docs.google.com/document/d/1BTHJCvjPSXnX17cOG9MWJ3B9L0lCy88Q/edit",
             "Designates the Superintendent custodian of all District records (governmental "
             "records under RSA 91-A:1-a) and directs written procedures that log and track "
             "requests and responses. Adopted September 17, 2025.", kind="policy"),
    Citation("policy-eh-r1", "Claremont School Board Procedure EH-R(1)",
             "https://docs.google.com/document/d/1hvzCwEFgpb3HxhuuREmQuscERXjGhPYu/edit",
             "Right-to-Know procedures: requests go through the Superintendent's office; "
             "written requests encouraged, never required; 5-business-day written response "
             "when records are not immediately available; copy fees $0.25 (letter), $0.50 "
             "(legal), $1.00 (11x17) per page; no fee to inspect; $1.00 per electronic "
             "communication beyond the first 250, paid in advance, with 30-day aggregation; "
             "thumb drives in unopened packaging or bought at cost. Adopted September 17, 2025.",
             kind="policy"),
    Citation("policy-eh-f1", "Form EH-F(1), Request for Waiver of Electronic Communication Record Charge",
             "https://drive.google.com/file/d/135YNC2DrsH3hizBkWtAN5TieuLylxJPA/view",
             "The form a requester files to seek waiver of the per-communication charge "
             "(indigency, media requester, or public-interest grounds).", kind="policy"),
    Citation("policy-eh-f2", "Form EH-F(2), Affidavit of Indigency",
             "https://drive.google.com/file/d/1qtT5nkDmeHTn8f1KO3mJhNhJG8L5Zxwa/view",
             "Financial affidavit supporting an indigency waiver.", kind="policy"),
    Citation("policy-jra", "Claremont School Board Policy JRA, Student Records and Access (FERPA)",
             "https://docs.google.com/document/d/1VLVtiQxCRKyj-tUIobXisXcc7IHFdu2K/edit",
             "A parent or eligible student inspects education records through the building "
             "principal, within 14 days (RSA 189:66, IV); defines personally identifiable "
             "information to include data that would let a reasonable person in the school "
             "community identify a student. Adopted January 7, 2025.", kind="policy"),
    Citation("policy-gbj", "Claremont School Board Policy GBJ, Personnel Records",
             "https://docs.google.com/document/d/1DOh4N5zgIU_G5HCiNZNK5mnALvZXejf6UiFsJ8ramt8/edit",
             "Directs a confidential personnel records system; cites RSA 91-A:5.", kind="policy"),
    Citation("policy-ehb", "Claremont School Board Policy EHB, Data/Records Retention",
             "https://docs.google.com/document/d/1cyQQi0-uvyyBImqaUqK-sOf4fE7IlpVr/edit",
             "Retention and destruction schedule for District records.", kind="policy"),
]

CITATIONS: dict[str, Citation] = {c.id: c for c in _C}


def cite(ids) -> list[Citation]:
    """Return the Citation objects for known ids, in order, dropping unknown ids."""
    out, seen = [], set()
    for i in ids:
        if i in CITATIONS and i not in seen:
            out.append(CITATIONS[i])
            seen.add(i)
    return out


def unknown(ids) -> list[str]:
    return [i for i in ids if i not in CITATIONS]


# The five triage outcomes. The first four are the brief's; records_search is
# the case the brief left out: a valid request for a District record that is
# not posted anywhere public.
CATEGORIES = {
    "outside_rsa": "Outside RSA 91-A (not a records request, or an exempt record)",
    "outside_policy": "Outside the Superintendent's policies (Policy EH / EH-R(1), or routed to JRA)",
    "public_info": "Answerable from publicly available information",
    "aggregate_only": "Answerable only with anonymized or aggregated information",
    "records_search": "Valid request for District records that are not public: custodian search",
}
