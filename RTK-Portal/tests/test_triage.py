# SPDX-License-Identifier: Apache-2.0
from datetime import date
from types import SimpleNamespace

import pytest

from rtk_portal import triage
from rtk_portal.kg import KG
from rtk_portal.triage import rules

TODAY = date(2026, 10, 30)
CTX = {"public_id": "RTK-2026-0001", "received": "October 30, 2026", "due": "November 9, 2026",
       "salutation": "Requester", "text": "", "log_url": "http://portal.test/log/RTK-2026-0001"}


def run(settings, text, **kw):
    kg = KG(settings.kg_path)
    return triage.run({"text": text}, CTX | {"text": text}, settings, kg, today=TODAY, **kw)


@pytest.mark.parametrize("text,category", [
    ("Please send the minutes and the video of the school board meeting on October 7, 2026.", "public_info"),
    ("I request my son's IEP and his discipline records.", "outside_policy"),
    ("How many students were suspended at Stevens High School in 2025, by grade?", "aggregate_only"),
    ("The personnel file and any complaints against the Stevens High School principal.", "outside_rsa"),
    ("Why did the superintendent leave?", "outside_rsa"),
    ("Please compile a spreadsheet of every legal expense in FY25.", "outside_rsa"),
    ("Police reports from the City of Claremont about an incident on Main Street.", "outside_policy"),
    ("Copies of all emails between the superintendent and the board chair about the audit, October 2026.", "records_search"),
    ("The school safety plan and the locations of security cameras.", "outside_rsa"),
    ("What did the board say about the 63 percent of IEPs out of compliance?", "public_info"),
])
def test_rules_categories(settings, text, category):
    assert run(settings, text)["category"] == category


def test_public_info_draft_has_links_and_reproducible_query(settings):
    r = run(settings, "Please send the minutes and the video of the school board meeting on October 7, 2026.")
    body = r["draft"]["body"]
    assert "https://drive.google.com/file/d/1MINUTESFIXTURE0000000000000000/view" in body
    assert "https://reflect-claremont.cablecast.tv/internetchannel/show/17634?site=1" in body
    assert "http://portal.test/kg/search?q=" in body
    assert "To repeat this search yourself" in body
    assert "—" not in body


def test_dates_and_fiscal_years():
    ds, lo, hi = rules.extract_dates("minutes of 10/7/26 and the FY25 budget", TODAY)
    assert ds == ["2026-10-07"] and lo == "2024-07-01" and hi == "2026-10-07"
    ds, lo, hi = rules.extract_dates("meetings in September 2026", TODAY)
    assert (lo, hi) == ("2026-09-01", "2026-09-30")


def test_forced_category(settings):
    r = run(settings, "The signed contract with the auditors.", forced="public_info")
    assert r["category"] == "public_info" and r["confidence"] == "staff"


# ---------------------------------------------------------------- Claude path, with a fake client

def _block(**kw):
    return SimpleNamespace(model_dump=lambda kw=kw: kw)


class FakeClient:
    """Plays two turns: one knowledge-graph search, then a submission with a bad
    citation id, an invented URL and an em dash."""

    def __init__(self):
        self.calls = 0
        self.messages = self

    def create(self, **kw):
        self.calls += 1
        if self.calls == 1:
            content = [_block(type="tool_use", id="t1", name="search_knowledge_graph",
                              input={"query": "signed audit contract", "date_from": "2026-10-01"})]
        else:
            # find the ref the search returned
            results = kw["messages"][-1]["content"][0]["content"]
            import json
            ref = json.loads(results)["results"][0]["ref"]
            content = [_block(type="tool_use", id="t2", name="submit_triage", input={
                "category": "records_search", "confidence": "medium",
                "reasons": [{"code": "custodian_search", "explanation": "Not public.",
                             "citations": ["rsa91a-4-iv-b", "made-up-id"]}],
                "hit_refs": [ref, "item:999999"],
                "kg_query": {"q": "signed audit contract"},
                "reproducible_prompt": "Find the signed audit contract.",
                "draft_subject": "Request RTK-2026-0001 — receipt",
                "draft_body": "Dear Requester,\n\nSee https://evil.example.com/x and http://portal.test/log/RTK-2026-0001.\n",
                "review_notes": []})]
        return SimpleNamespace(content=content, stop_reason="tool_use",
                               usage=SimpleNamespace(input_tokens=10, output_tokens=5))


def test_claude_output_is_validated(settings):
    fake = FakeClient()
    r = run(settings, "The signed contract with the auditors.", client=fake)
    assert r["engine"].startswith("claude:")
    assert r["category"] == "records_search"
    assert r["reasons"][0]["citations"] == ["rsa91a-4-iv-b"]
    assert any("made-up-id" in n for n in r["review_notes"])
    assert "https://evil.example.com/x [[unverified link]]" in r["draft"]["body"]
    assert "http://portal.test/log/RTK-2026-0001." in r["draft"]["body"]
    assert "—" not in r["draft"]["subject"]
    assert len(r["hits"]) == 1


def test_claude_failure_falls_back_to_rules(settings):
    class Broken:
        messages = SimpleNamespace(create=lambda **kw: (_ for _ in ()).throw(RuntimeError("boom")))
    r = run(settings, "The signed contract with the auditors.", client=Broken())
    assert r["engine"] == "rules" and "Claude triage failed" in r["review_notes"][0]


def test_missing_minutes_leave_a_blocking_placeholder(settings):
    r = run(settings, "The minutes of the SAU 6 board meeting on September 10, 2026.")
    assert r["category"] == "public_info" and r["missing"] == ["minutes"]
    assert "[[" in r["draft"]["body"]


def test_policy_request_is_public(settings):
    r = run(settings, "A copy of Policy EH and the procedures that go with it.")
    assert r["category"] == "public_info"
    assert "1BTHJCvjPSXnX17cOG9MWJ3B9L0lCy88Q" in r["draft"]["body"]


def test_delivery_and_fee_notes(settings):
    r = run(settings, "All emails about the audit in 2026, on my own USB thumb drive, free of charge.")
    notes = " ".join(r["review_notes"])
    assert "unopened" in notes and "EH-F(1)" in notes and "250" in notes
