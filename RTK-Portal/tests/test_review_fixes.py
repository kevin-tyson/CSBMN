# SPDX-License-Identifier: Apache-2.0
"""Regression tests for the findings of the independent review (2026-10-30)."""
import json
import re
import shutil
import time
from types import SimpleNamespace

import pytest

from rtk_portal import kg as kgmod
from rtk_portal import otp
from rtk_portal.kg import KG
from rtk_portal.service import Portal
from rtk_portal.triage import llm

from .conftest import FIXTURE_REPO, file_and_verify
from .test_triage import FakeClient, run


def _send_clean(portal, pk, public_text=None, subject=None):
    conn = portal.conn()
    act = portal.get(conn, pk=pk)
    body = re.sub(r"\[\[[^\]]*\]\]", "", act["draft_body"].replace("[[Or:", "[[")).replace("]]", "").replace("[[", "")
    portal.send_response(pk, subject or act["draft_subject"], body, public_text, "clerk@sau6.test")


def _public_events(portal, pid):
    return json.dumps(portal.public_detail(pid)["events"], default=str).lower()


# 1. held text must not leak through the search link or the prompt
def test_held_text_does_not_leak_through_prompt(portal, mailer):
    pid = file_and_verify(portal, mailer, "a@ex.org",
                          "Minutes of the October 7, 2026 school board meeting where Jacob Miller's suspension was discussed.")
    conn = portal.conn()
    act = portal.active(conn)
    assert act["text_held"] and act["category"] == "public_info"
    _send_clean(portal, act["pk"])
    pub = _public_events(portal, pid)
    assert "jacob" not in pub and "miller" not in pub and "suspension" not in pub


def test_contact_details_never_reach_search_terms(portal, mailer):
    pid = file_and_verify(portal, mailer, "a@ex.org",
                          "Minutes of the October 7, 2026 school board meeting. Call 603-555-0142 or pat.doe@gmail.com")
    conn = portal.conn()
    act = portal.active(conn)
    assert "555" not in act["draft_body"].split("You asked:")[1].split("To repeat")[1]
    _send_clean(portal, act["pk"])
    pub = _public_events(portal, pid)
    assert "555" not in pub and "gmail" not in pub


# 2 and 7. subjects are scrubbed; names removed whole-word and case-insensitively
def test_subject_and_name_scrubbing(portal, mailer):
    pid = file_and_verify(portal, mailer, "b@ex.org", "The signed audit engagement letter for FY25.", name="Ed Jones")
    conn = portal.conn()
    act = portal.active(conn)
    body = act["draft_body"] + "\nSee also the Department of Education. Thank you, MR. JONES."
    portal.send_response(act["pk"], "Response for Ed Jones (b@ex.org)",
                         body.replace("[[", "").replace("]]", ""), None, "clerk@sau6.test")
    ev = [e for e in portal.public_detail(pid)["events"] if e["type"] == "response_sent"][0]["data"]
    assert "jones" not in ev["subject"].lower() and "b@ex.org" not in ev["subject"]
    assert "jones" not in ev["body"].lower() and "Department of Education" in ev["body"]


# 4 and 5. a cited policy or a named meeting does not end triage when other records are asked for
def test_citing_policy_eh_is_not_a_policy_request(settings):
    r = run(settings, "Pursuant to RSA 91-A and Policy EH, please provide all emails between the superintendent "
                      "and the business administrator in October 2026.")
    assert r["category"] == "records_search"


def test_emails_about_a_meeting_are_a_records_search(settings):
    r = run(settings, "All emails about the agenda for the October 7, 2026 school board meeting.")
    assert r["category"] == "records_search"
    assert r["public_parts"] and "already public" in r["draft"]["body"]


# 6. response blocks go back to the API without null response-only fields
def test_blocks_sent_back_without_nulls():
    tool = SimpleNamespace(model_dump=lambda: {"type": "tool_use", "id": "t", "name": "n", "input": {"q": 1},
                                               "caller": None, "toolset_name": None})
    text = SimpleNamespace(model_dump=lambda: {"type": "text", "text": "hi", "citations": None})
    assert llm._as_param(tool) == {"type": "tool_use", "id": "t", "name": "n", "input": {"q": 1}}
    assert llm._as_param(text) == {"type": "text", "text": "hi"}


# 8. wrong guesses are capped across codes
def test_failure_cap_across_codes(portal):
    from datetime import timedelta
    from rtk_portal import db
    conn = portal.conn()
    for _ in range(3):
        code = otp.issue(conn, "k", "staff@x.org", "staff", "login", 10)
        wrong = "000000" if code != "000000" else "111111"
        for _ in range(5):
            with pytest.raises(otp.OTPError):
                otp.verify(conn, "k", "staff@x.org", "staff", "login", wrong, 5)
    # Age the codes past the 15-minute send quota, still inside the 24-hour failure window.
    conn.execute("UPDATE otp SET created_at=?", (db.iso(db.utcnow() - timedelta(minutes=20)),))
    code = otp.issue(conn, "k", "staff@x.org", "staff", "login", 10)
    with pytest.raises(otp.OTPError, match="today"):
        otp.verify(conn, "k", "staff@x.org", "staff", "login", code, 5)


def test_request_codes_do_not_use_up_staff_quota(portal):
    conn = portal.conn()
    for i in range(3):
        otp.issue(conn, "k", "clerk@sau6.test", "request", f"r{i}", 10)
    otp.issue(conn, "k", "clerk@sau6.test", "staff", "login", 10)  # would raise if quotas were shared


# 9. the worker thread picks up work without a lost wake-up
def test_worker_thread_advances_queue(settings, mailer):
    p = Portal(settings.with_(start_worker=True), mailer=mailer)
    p.recover()
    try:
        pid = file_and_verify(p, mailer, "a@ex.org", "The FY25 audit engagement letter.")
        conn = p.conn()
        for _ in range(50):
            if p.get(conn, public_id=pid)["status"] == "review":
                break
            time.sleep(0.1)
        assert p.get(conn, public_id=pid)["status"] == "review"
    finally:
        p.stop_worker()


# 10. plus-tags and Gmail dots count as one requester
def test_grouping_key_for_rounds(portal, mailer):
    assert otp.grouping_key("K.Evin+1@GMail.com") == otp.grouping_key("kevin+2@googlemail.com") == "kevin@gmail.com"
    file_and_verify(portal, mailer, "kevin+1@gmail.com", "The FY25 audit engagement letter.")
    pid = file_and_verify(portal, mailer, "k.evin+2@gmail.com", "The FY24 audit engagement letter.")
    conn = portal.conn()
    assert portal.get(conn, public_id=pid)["queue_round"] == 2


# 11, 12, 13. triage corrections
@pytest.mark.parametrize("text,bad", [
    ("Why is the audit late?", "records_search"),
    ("The total paid for student transportation in FY25.", "aggregate_only"),
    ("Tuition rates for out-of-district placements.", "aggregate_only"),
    ("The special education budget and the number of paraprofessionals.", "aggregate_only"),
])
def test_misfiles_fixed(settings, text, bad):
    assert run(settings, text)["category"] != bad


def test_student_asking_for_own_transcript(settings):
    from rtk_portal import privacy
    t = "I am a student at Stevens High School and I need a copy of my transcript."
    assert run(settings, t)["category"] == "outside_policy"
    assert privacy.screen(t)[0]


# 14. a personnel denial does not tell the requester that categorical refusals are not allowed
def test_personnel_draft_is_consistent(settings):
    r = run(settings, "The personnel file and any complaints against the Stevens High School principal.")
    body = r["draft"]["body"]
    assert "categorical" not in body and "[[" in body and "balancing" in body


# 15. bare domains and subjects from Claude are checked
class BareDomainClient(FakeClient):
    def create(self, **kw):
        resp = super().create(**kw)
        if self.calls == 2:
            inp = resp.content[0].model_dump()["input"]
            inp["draft_body"] = "Pay at www.pay-rtk-fees.example/now or evil.example/pay. See csbmn.claremontv.org."
            inp["draft_subject"] = "Visit https://evil.example.com"
        return resp


def test_bare_domains_flagged(settings):
    r = run(settings, "The signed contract with the auditors.", client=BareDomainClient())
    b = r["draft"]["body"]
    assert "www.pay-rtk-fees.example/now [[unverified link]]" in b and "evil.example/pay [[unverified link]]" in b
    assert "csbmn.claremontv.org. [[" not in b and "csbmn.claremontv.org [[" not in b
    assert "evil" not in r["draft"]["subject"]


# 18. CSV cells cannot run as formulas
def test_csv_formula_injection(settings, portal, mailer):
    from starlette.testclient import TestClient
    from rtk_portal.web import create_app
    file_and_verify(portal, mailer, "a@ex.org", '=HYPERLINK("http://x.example","click") records of the FY25 audit')
    with TestClient(create_app(settings, portal)) as c:
        csv_text = c.get("/log.csv").text
    assert "'=HYPERLINK" in csv_text


# 19. a data directory with URI-special characters works
def test_kg_path_with_special_characters(tmp_path):
    d = tmp_path / "data #1?%"
    d.mkdir()
    out = d / "kg.db"
    kgmod.build(FIXTURE_REPO, out, "https://csbmn.claremontv.org/", log=lambda *a: None)
    assert KG(out).search("audit contract")
