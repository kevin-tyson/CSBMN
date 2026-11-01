# SPDX-License-Identifier: Apache-2.0
import json
from datetime import date, timedelta

import pytest

from rtk_portal import db, otp, privacy
from rtk_portal.bizdays import Calendar, nh_legal_holidays
from rtk_portal.service import PortalError

from .conftest import file_and_verify


# ---------------------------------------------------------------- business days

def test_holidays_2026():
    h = nh_legal_holidays(2026)
    assert h[date(2026, 11, 3)] == "Election Day"
    assert h[date(2026, 11, 26)] == "Thanksgiving Day"
    assert h[date(2026, 10, 12)] == "Columbus Day"
    assert h[date(2026, 1, 19)] == "Martin Luther King, Jr. Civil Rights Day"
    assert date(2026, 11, 3) in h and date(2027, 11, 2) not in nh_legal_holidays(2027)


def test_five_business_days_skips_weekend_and_election_day():
    cal = Calendar()
    # Friday Oct 30, 2026: Nov 2 (1), Nov 3 is Election Day, Nov 4-6 (2-4), Nov 9 (5)
    assert cal.add_business_days(date(2026, 10, 30), 5) == date(2026, 11, 9)


def test_calendar_overrides():
    # Office open on Election Day: the fifth business day moves up to Friday.
    assert Calendar({date(2026, 11, 3): True}).add_business_days(date(2026, 10, 30), 5) == date(2026, 11, 6)
    # Office also closed on Monday Nov 2 (snow day): back to Nov 9.
    cal = Calendar({date(2026, 11, 2): False, date(2026, 11, 3): True})
    assert cal.add_business_days(date(2026, 10, 30), 5) == date(2026, 11, 9)
    assert cal.business_days_elapsed(date(2026, 10, 30), date(2026, 11, 4)) == 2


# ---------------------------------------------------------------- otp

def test_otp_wrong_expired_and_single_use(portal):
    conn = portal.conn()
    code = otp.issue(conn, "k", "A@B.org", "request", "r1", 10)
    with pytest.raises(otp.OTPError):
        otp.verify(conn, "k", "a@b.org", "request", "r1", "000000" if code != "000000" else "111111", 5)
    otp.verify(conn, "k", "a@b.org", "request", "r1", code, 5)
    with pytest.raises(otp.OTPError):
        otp.verify(conn, "k", "a@b.org", "request", "r1", code, 5)
    code2 = otp.issue(conn, "k", "a@b.org", "request", "r2", 10)
    conn.execute("UPDATE otp SET expires_at=? WHERE ref='r2'", (db.iso(db.utcnow() - timedelta(minutes=1)),))
    with pytest.raises(otp.OTPError, match="expired"):
        otp.verify(conn, "k", "a@b.org", "request", "r2", code2, 5)


def test_otp_attempt_limit_and_rate_limit(portal):
    conn = portal.conn()
    code = otp.issue(conn, "k", "x@y.org", "request", "r", 10)
    wrong = "123456" if code != "123456" else "654321"
    for _ in range(3):
        with pytest.raises(otp.OTPError):
            otp.verify(conn, "k", "x@y.org", "request", "r", wrong, 3)
    with pytest.raises(otp.OTPError, match="Too many"):
        otp.verify(conn, "k", "x@y.org", "request", "r", code, 3)
    otp.issue(conn, "k", "x@y.org", "request", "r", 10)
    otp.issue(conn, "k", "x@y.org", "request", "r", 10)
    with pytest.raises(otp.RateLimited):
        otp.issue(conn, "k", "x@y.org", "request", "r", 10)


# ---------------------------------------------------------------- privacy

def test_privacy_holds_child_and_masks_contacts():
    hold, reasons, masked = privacy.screen("Please send my daughter's IEP. Call me at 603-555-0142 or jo@ex.com")
    assert hold and reasons
    assert "603-555-0142" not in masked and "jo@ex.com" not in masked
    hold, _, _ = privacy.screen("The signed contract with the auditors for FY25.")
    assert not hold


# ---------------------------------------------------------------- event chain

def test_chain_detects_tampering(portal, mailer):
    file_and_verify(portal, mailer, "a@ex.org", "The signed audit engagement letter for FY25.")
    ev = portal.events()
    assert db.verify_chain(ev)[0]
    ev[0] = dict(ev[0]) | {"data": json.dumps({"text": "something else"})}
    ok, bad = db.verify_chain(ev)
    assert not ok and bad == ev[0]["seq"]


# ---------------------------------------------------------------- queue

def _ids_in_order(portal):
    conn = portal.conn()
    act = portal.active(conn)
    q = [r["public_id"] for r in portal.queue(conn)]
    return ([act["public_id"]] if act else []) + q


def test_fair_queue_defers_a_users_later_requests(portal, mailer):
    a1 = file_and_verify(portal, mailer, "a@ex.org", "The FY25 audit engagement letter.")  # becomes active at once
    a2 = file_and_verify(portal, mailer, "a@ex.org", "The FY24 audit engagement letter.")
    a3 = file_and_verify(portal, mailer, "a@ex.org", "The FY23 audit engagement letter.")
    b1 = file_and_verify(portal, mailer, "b@ex.org", "The transportation contract for 2026.")
    c1 = file_and_verify(portal, mailer, "c@ex.org", "The plow and sand contract for 2026.")
    b2 = file_and_verify(portal, mailer, "b@ex.org", "The food service contract for 2026.")
    # a1 active; then round 1 (b1, c1), round 2 (a2, b2 by time), round 3 (a3)
    assert _ids_in_order(portal) == [a1, b1, c1, a2, b2, a3]


def test_one_request_at_a_time(portal, mailer):
    a1 = file_and_verify(portal, mailer, "a@ex.org", "The FY25 audit engagement letter.")
    b1 = file_and_verify(portal, mailer, "b@ex.org", "The transportation contract for 2026.")
    conn = portal.conn()
    act = portal.active(conn)
    assert act["public_id"] == a1 and act["status"] == "review"
    assert [r["public_id"] for r in portal.queue(conn)] == [b1]
    portal.advance()  # must not take b1 while a1 is open
    assert portal.get(conn, public_id=b1)["status"] == "queued"
    body = act["draft_body"].replace("[[", "").replace("]]", "")
    portal.send_response(act["pk"], act["draft_subject"], body, None, "clerk@sau6.test")
    assert portal.get(conn, public_id=a1)["status"] == "closed"
    assert portal.get(conn, public_id=b1)["status"] == "review"


def test_closing_frees_the_slot_and_round_is_not_recomputed(portal, mailer):
    a1 = file_and_verify(portal, mailer, "a@ex.org", "The FY25 audit engagement letter.")
    a2 = file_and_verify(portal, mailer, "a@ex.org", "The FY24 audit engagement letter.")
    conn = portal.conn()
    portal.close_without_response(portal.get(conn, public_id=a1)["pk"], "withdrawn", "", "clerk@sau6.test")
    b1 = file_and_verify(portal, mailer, "b@ex.org", "The transportation contract for 2026.")
    # a2 (round 2) became active when a1 closed because nobody else was waiting; b1 waits behind it.
    assert _ids_in_order(portal) == [a2, b1]


# ---------------------------------------------------------------- filing and sending

def test_unverified_request_is_not_public(portal, mailer):
    portal.file_request("z@ex.org", "", False, "The FY25 audit engagement letter.")
    assert portal.public_log() == []


def test_placeholders_block_sending(portal, mailer):
    a1 = file_and_verify(portal, mailer, "a@ex.org", "Copies of all emails between the superintendent and the board chair about the audit in October 2026.")
    conn = portal.conn()
    act = portal.active(conn)
    assert act["category"] == "records_search"
    assert "[[" in act["draft_body"]
    with pytest.raises(PortalError, match="placeholders"):
        portal.send_response(act["pk"], act["draft_subject"], act["draft_body"], None, "clerk@sau6.test")


def test_public_copy_hides_email_and_unconsented_name(portal, mailer):
    pid = file_and_verify(portal, mailer, "jane@ex.org", "The FY25 audit engagement letter.", name="Jane Roe")
    conn = portal.conn()
    act = portal.active(conn)
    body = act["draft_body"].replace("[[", "").replace("]]", "") + "\nReply to jane@ex.org"
    portal.send_response(act["pk"], act["draft_subject"], body, None, "clerk@sau6.test")
    d = portal.public_detail(pid)
    sent = [e for e in d["events"] if e["type"] == "response_sent"][0]["data"]["body"]
    assert "jane@ex.org" not in sent and "Jane Roe" not in sent and "Dear Requester" in sent
    assert mailer.sent[-1]["to"] == "jane@ex.org" and "Jane Roe" in mailer.sent[-1]["body"]


def test_held_text_until_published(portal, mailer):
    pid = file_and_verify(portal, mailer, "p@ex.org", "I want my son Jacob Smith's discipline records and his IEP.")
    d = portal.public_detail(pid)
    assert d["text_held"] and d["text"] is None
    conn = portal.conn()
    act = portal.active(conn)
    assert act["category"] == "outside_policy"
    body = act["draft_body"].replace("[[", "").replace("]]", "")
    portal.send_response(act["pk"], act["draft_subject"], body, "A parent asked for a student's education records.", "clerk@sau6.test")
    d = portal.public_detail(pid)
    assert not d["text_held"] and "Jacob" not in json.dumps(d["events"], default=str)


def test_acknowledgment_for_waiting_request_keeps_place(portal, mailer):
    file_and_verify(portal, mailer, "a@ex.org", "The FY25 audit engagement letter.")
    b1 = file_and_verify(portal, mailer, "b@ex.org", "The transportation contract for 2026.")
    conn = portal.conn()
    row = portal.get(conn, public_id=b1)
    subject, body = portal.ack_draft(row["pk"])
    body = body.replace("[[date]]", "November 20, 2026").replace("[[reason]]", "the contract is in storage")
    body = body.replace("[[No charge is expected. / Itemized estimate: ...]]", "No charge is expected.")
    portal.send_ack(row["pk"], subject, body, "clerk@sau6.test")
    row = portal.get(conn, public_id=b1)
    assert row["status"] == "queued" and row["ack_sent_at"]
    assert portal.public_detail(b1)["first_response"] is not None


def test_same_requester_within_30_days_is_noted(portal, mailer):
    a1 = file_and_verify(portal, mailer, "a@ex.org", "The FY25 audit engagement letter.")
    conn = portal.conn()
    act = portal.active(conn)
    portal.send_response(act["pk"], act["draft_subject"], act["draft_body"].replace("[[", "").replace("]]", ""), None, "clerk@sau6.test")
    file_and_verify(portal, mailer, "a@ex.org", "The FY24 audit engagement letter.")
    act = portal.active(conn)
    assert any(a1 in n for n in json.loads(act["triage_json"])["review_notes"])


def test_mail_failure_changes_nothing(portal, mailer):
    file_and_verify(portal, mailer, "a@ex.org", "The FY25 audit engagement letter.")
    conn = portal.conn()
    act = portal.active(conn)

    def boom(*a, **k):
        raise OSError("smtp down")
    mailer.send = boom
    with pytest.raises(PortalError, match="could not be sent"):
        portal.send_response(act["pk"], act["draft_subject"], act["draft_body"].replace("[[", "").replace("]]", ""), None, "clerk@sau6.test")
    assert portal.get(conn, pk=act["pk"])["status"] == "review"
