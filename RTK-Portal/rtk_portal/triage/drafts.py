# SPDX-License-Identifier: Apache-2.0
"""Draft emails for each triage outcome.

Anything a person must supply is written as [[...]]. The staff console will not
send a draft that still contains [[ or ]], so a placeholder cannot reach a
requester by accident.
"""

from __future__ import annotations

import textwrap
from datetime import date

from .. import law

IPLATFORM = "https://my.doe.nh.gov/iPlatform"
FOOTER = ("This response was prepared with the help of an automated triage tool and reviewed by "
          "District staff before it was sent.")


def _quote(text: str) -> str:
    lines = []
    for para in text.strip().splitlines():
        wrapped = textwrap.wrap(para, 76) or [""]
        lines += ["> " + w for w in wrapped]
    return "\n".join(lines)


def _wrap(text: str) -> str:
    return "\n\n".join(textwrap.fill(p, 78) for p in text.strip().split("\n\n"))


def _authorities(ids: list[str]) -> str:
    cites = law.cite(ids)
    if not cites:
        return ""
    return "Authorities cited:\n" + "\n".join(f"- {c.label}: {c.url}" for c in cites)


def _fdate(iso_d: str) -> str:
    try:
        d = date.fromisoformat(iso_d[:10])
    except (TypeError, ValueError):
        return iso_d or ""
    return f"{d:%B} {d.day}, {d.year}"


def _hit_lines(hits: list[dict], limit: int = 8) -> str:
    out = []
    for i, h in enumerate(hits[:limit], 1):
        title = (h.get("title") or "Record").replace(" \u2014 ", ": ").replace("\u2014", ", ")
        if h.get("kind") in ("minutes", "agenda", "document", "folder") and h.get("meeting_title"):
            title = f"{title} ({h['meeting_title']})"
        when = ""
        if h.get("date") and str(h["date"])[:4] not in title:
            when = f" ({_fdate(h['date'])})"
        line = f"{i}. {title}{when}\n   {h.get('url') or '[[link]]'}"
        snip = (h.get("snippet") or "").strip()
        if snip:
            snip = snip if len(snip) <= 220 else snip[:217].rsplit(" ", 1)[0] + "..."
            line += "\n   " + "\n   ".join(textwrap.wrap(snip, 74))
        out.append(line)
    return "\n".join(out)


def _all_citations(result: dict) -> list[str]:
    ids = []
    for r in result.get("reasons", []):
        ids += r.get("citations", [])
    return ids


def compose(result: dict, ctx: dict, settings) -> tuple[str, str]:
    """ctx keys: public_id, received, due, salutation, text, log_url."""
    cat = result["category"]
    codes = {r["code"] for r in result.get("reasons", [])}
    rid = ctx["public_id"]
    head = (f"Dear {ctx['salutation']},\n\n"
            f"The {settings.district_name} received your Right-to-Know request {rid} on {ctx['received']}. "
            f"You asked:\n\n{_quote(ctx['text'])}\n\n")
    tail_log = _wrap(f"This request and the District's response are posted in the public Right-to-Know log: "
                     f"{ctx['log_url']}")
    sig = settings.custodian_signature
    ids = _all_citations(result)

    if cat == "public_info":
        subject = f"Right-to-Know request {rid}: the records are already public"
        hits = result.get("hits") or []
        body = head + _wrap(
            "The records that answer your request are already public. You can inspect and download them "
            "at no charge at these addresses:") + "\n\n" + (_hit_lines(hits) or "[[list the records]]") + "\n\n"
        for what in result.get("missing") or []:
            body += _wrap(f"[[The {what} you asked for are not in the public record yet. Give the link if they are "
                          f"posted, or say when they will be available and treat that part as a records request "
                          f"(RSA 91-A:4, IV(b)).]]") + "\n\n"
        kgq = result.get("kg") or {}
        if kgq.get("url") or result.get("prompt"):
            body += "To repeat this search yourself:\n"
            if kgq.get("url"):
                body += f"- Meeting Navigator search: {kgq['url']}\n"
            if result.get("prompt"):
                body += ("- Or give this prompt to an AI assistant that can read the public knowledge graph:\n"
                         + "\n".join("  " + w for w in textwrap.wrap('"' + result["prompt"] + '"', 76)) + "\n")
            body += "\n"
        body += _wrap(
            "Inspection is free. If you would rather have paper copies, Procedure EH-R(1) sets the fee at "
            "$0.25 per letter-size page. If these records do not answer what you were looking for, reply "
            "and describe the record you want, and the District will treat your reply as a new request.") + "\n\n"
    elif cat == "outside_rsa":
        subject = f"Right-to-Know request {rid}: response"
        exempt = [r for r in result["reasons"] if r["code"].startswith("exempt_")]
        if exempt:
            body = head + _wrap(
                "The District is withholding the records you describe because they are exempt from public "
                "disclosure. RSA 91-A:4, IV(c) requires the District to state the specific exemption and how "
                "it applies:") + "\n\n"
            for r in exempt:
                labels = ", ".join(c.label for c in law.cite(r["citations"]) if c.kind in ("statute", "federal"))
                body += "- " + "\n  ".join(textwrap.wrap(f"{labels}: {r['explanation']}", 76)) + "\n"
            body += "\n" + _wrap(
                "[[If any part of the records can be released with the exempt material redacted, say what is "
                "being released and when; otherwise delete this paragraph.]]") + "\n\n"
            body += _wrap("If you disagree with this decision, RSA 91-A:7 allows you to petition the superior "
                          "court.") + "\n\n"
            ids.append("rsa91a-7")
        else:
            body = head + _wrap(
                "RSA 91-A gives every citizen access to governmental records that are reasonably described. "
                "It does not require District staff to answer questions, explain decisions, or compile "
                "information into a form the District does not already keep (RSA 91-A:4, VII).") + "\n\n"
            if "question_not_record" in codes:
                body += _wrap("Your request asks a question rather than naming a record, so as written it is not "
                              "one the District must fulfill under RSA 91-A.") + "\n\n"
            if "compile_new_record" in codes:
                body += _wrap("Your request asks the District to prepare a new list, summary or analysis, which "
                              "RSA 91-A does not require.") + "\n\n"
            body += _wrap(
                "You can restate it as a request for existing records, and the District may suggest a "
                "reasonable way to do that (RSA 91-A:4, IV(e)). Records that may hold this information include "
                "[[name the records, such as minutes, budget documents, contracts or reports]].") + "\n\n"
            hits = [h for h in (result.get("hits") or []) if h.get("url")][:5]
            if hits:
                body += _wrap("The public record may already cover part of what you asked:") + "\n\n" + _hit_lines(hits) + "\n\n"
    elif cat == "outside_policy":
        subject = f"Right-to-Know request {rid}: where to send this request"
        if "jra_own_records" in codes:
            body = head + _wrap(
                "Your request is for a student's own education records. Those are not public records, so the "
                "District handles them under Policy JRA instead of the Right-to-Know Law. Under Policy JRA, a "
                "parent or eligible student asks the building principal to inspect the records, and the "
                "District must arrange access within 14 days (RSA 189:66, IV).") + "\n\n" + _wrap(
                "Please contact the principal of [[school]] at [[contact]]. [[Or: with your permission, the "
                "District has forwarded your request to the principal on [[date]].]]") + "\n\n" + _wrap(
                "To protect the student's privacy, the text of this request is not posted in the public log.") + "\n\n"
        elif "other_custodian" in codes:
            agency = (result.get("signals") or {}).get("other_agency") or "[[agency]]"
            body = head + _wrap(
                f"Policy EH makes the Superintendent custodian of {settings.district_name} records. The records "
                f"you describe appear to be kept by {agency}, a separate public body with its own records "
                f"custodian. Please send your request to {agency} at [[contact]].") + "\n\n" + _wrap(
                "If you also want District records on this subject, reply and describe them, and the District "
                "will treat your reply as a new request.") + "\n\n"
        else:
            body = head + _wrap(
                "[[Explain which provision of Policy EH or Procedure EH-R(1) the request falls outside of, and "
                "what the requester can do instead.]]") + "\n\n"
    elif cat == "aggregate_only":
        subject = f"Right-to-Know request {rid}: what the District can release"
        body = head + _wrap(
            "Records about individual students are exempt from public disclosure (RSA 91-A:5, III) and "
            "protected by federal law (FERPA). The District can answer a request like yours only with "
            "anonymized or aggregated figures, and it must withhold or combine any count small enough to "
            "identify a student: Policy JRA treats information that would let a reasonable person in the "
            "school community identify a student as personally identifiable.") + "\n\n" + _wrap(
            "RSA 91-A does not require the District to create a new compilation (RSA 91-A:4, VII), but the "
            "District will release figures it already keeps or reports:") + "\n\n" + _wrap(
            f"[[List the existing reports or data the District can release, with any count below "
            f"{settings.min_cell_size} suppressed, or state that none exist in that form.]]") + "\n\n"
        body += "Public sources that already report figures of this kind:\n"
        body += f"- New Hampshire Department of Education iPlatform: {IPLATFORM}\n"
        hits = [h for h in (result.get("hits") or []) if h.get("url")][:4]
        if hits:
            body += "- Meeting records where related figures were discussed:\n" + "\n".join(
                "  " + line for line in _hit_lines(hits).splitlines()) + "\n"
        body += "\n"
    else:  # records_search
        subject = f"Right-to-Know request {rid}: receipt and time needed"
        body = head + _wrap(
            "The records you describe are not posted publicly, so the custodian must locate them and review "
            "them for information that RSA 91-A:5 or other law exempts before releasing them (Procedure "
            "EH-R(1)). As RSA 91-A:4, IV(b) requires, this is the District's written response within five "
            f"business days (by {ctx['due']}):") + "\n\n"
        body += ("- Time needed: the District expects to respond by [[date]], because [[reason]].\n"
                 "- Cost: [[No charge is expected. / Itemized estimate: ...]]\n\n")
        if result.get("public_parts"):
            body += _wrap("Part of what you asked for is already public, and you can have it now:") + "\n\n"
            body += _hit_lines(result["public_parts"]) + "\n\n"
        if (result.get("signals") or {}).get("bulk_ecomms"):
            body += _wrap(
                "Your request may cover a large number of emails or messages. Under Procedure EH-R(1) there is "
                "no charge for the first 250 individual electronic communications; beyond that the charge is "
                "$1.00 each, paid before copies are released, and requests from the same person within 30 days "
                "are counted together. You may ask for a waiver on Form EH-F(1) if you qualify as indigent, as "
                "a media requester, or because the records will contribute significantly to public "
                "understanding of the District.") + "\n\n"
            ids += ["policy-eh-f1", "rsa91a-4-viii", "rsa91a-4-ix"]
        body += _wrap(
            "Narrowing the request by date range, subject or the people involved will speed it up, and the "
            "District may suggest how (RSA 91-A:4, IV(e)).") + "\n\n"

    body += tail_log + "\n\n" + "Sincerely,\n\n" + sig + "\n\n"
    auth = _authorities(ids)
    if auth:
        body += auth + "\n\n"
    body += _wrap(FOOTER) + "\n"
    return subject, body


def acknowledgment(ctx: dict, settings) -> tuple[str, str]:
    """Five-business-day statement for a request still waiting in the queue."""
    rid = ctx["public_id"]
    subject = f"Right-to-Know request {rid}: receipt and time needed"
    body = (f"Dear {ctx['salutation']},\n\n"
            + _wrap(f"The {settings.district_name} received your Right-to-Know request {rid} on "
                    f"{ctx['received']}. Requests are handled in the order the public log shows, and yours "
                    "has not reached review yet.") + "\n\n"
            + _wrap("As RSA 91-A:4, IV(b) requires, this is the District's written statement within five "
                    f"business days (by {ctx['due']}) of the time reasonably necessary to respond:") + "\n\n"
            + "- Time needed: the District expects to respond by [[date]], because [[reason]].\n"
            + "- Cost: [[No charge is expected. / Itemized estimate: ...]]\n\n"
            + _wrap(f"You can follow the request in the public log: {ctx['log_url']}") + "\n\n"
            + "Sincerely,\n\n" + settings.custodian_signature + "\n\n"
            + _authorities(["rsa91a-4-iv-b", "policy-eh-r1"]) + "\n")
    return subject, body
