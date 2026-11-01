# SPDX-License-Identifier: Apache-2.0
"""Triage entry point: rules first, then Claude when a key is configured.
Either way the result carries a draft email for human review."""

from __future__ import annotations

import logging
from datetime import date

from . import drafts, llm, rules

log = logging.getLogger("rtk.triage")


def run(req: dict, ctx: dict, settings, kg, forced: str | None = None, client=None,
        today: date | None = None) -> dict:
    """req: the request row as a dict. ctx: public_id, received, due,
    salutation, text, log_url (see web.draft_context)."""
    result = rules.triage(req, settings, kg, forced=forced, today=today)
    subject, body = drafts.compose(result, ctx, settings)
    result["draft"] = {"subject": subject, "body": body}
    if settings.claude_api_key or client is not None:
        try:
            ai = llm.triage(req, settings, kg, result, ctx, forced=forced, client=client)
            ai["rules_draft"] = result["draft"]
            return ai
        except Exception as e:  # never lose a request to an API error
            log.exception("Claude triage failed; using rules result")
            result["review_notes"].insert(0, f"Claude triage failed ({type(e).__name__}: {e}); "
                                             "this draft comes from the rules engine.")
    return result
