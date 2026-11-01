# RTK Portal

A Right-to-Know request portal for the Claremont School District, built on the Claremont School Board Meeting Navigator knowledge graph ([kevin-tyson/CSBMN](https://github.com/kevin-tyson/CSBMN)).

A resident files a request for District records under RSA 91-A and confirms an email address with a one-time code. The portal numbers and logs the request, puts it in a fair queue, triages it against the statute, the Superintendent's procedures and the public record, and drafts a response. A person at the Superintendent's office edits and sends every response. Requests, dates and responses are published in a hash-chained public log.

**Not legal advice.** The portal drafts; District staff decide. Have counsel review `rtk_portal/law.py` and the draft templates before a pilot.

---

## How the brief maps to the code

Requirement

Where

Log requests for school district information under RSA 91-A

`service.Portal.file_request`, `verify_request`; `requests` table

Verify the requester by a one-time password sent by email

`otp.py` (6 digits, HMAC-stored, 10-minute expiry, 5 tries, single use, rate-limited)

Triage: outside RSA 91-A, with draft email

`triage/rules.py` (`outside_rsa`), `triage/drafts.py`

Triage: outside the Superintendent's policies, with draft email

`outside_policy`: Policy EH / EH-R(1), and parent requests routed to Policy JRA

Triage: answerable from public information, with the query or prompt

`public_info`: draft lists the records, a rerunnable search URL and an AI prompt

Triage: answerable only with anonymized or aggregated information

`aggregate_only`

All requests and responses logged and public

`/log`, `/log/<id>`, `/log.csv`, `/log.json`, `/log/events.json`

One request at a time

`service.Portal.advance` and `_claim_next` (database write lock)

Queue by requester and time; a requester's 2nd to nth requests after all others

queue rounds, below

Two additions the brief did not ask for:

-   **A fifth outcome, `records_search`.** The most common request is a valid one for a District record that is not posted anywhere (a contract, invoices, emails). None of the four outcomes fits it. The draft is the written statement RSA 91-A:4, IV(b) requires within five business days.
-   **A five-business-day statement for waiting requests.** Serving one request at a time can push a waiting request past its fifth business day. The statute's clock does not stop for the queue, so staff can send the statement for any waiting request from the console without changing its place. The console marks requests in yellow from business day 3 and red when overdue.

## The queue rule

When a request is verified it gets a round: 1 if its requester has no other request open, 2 if they have one, and so on. The portal takes the waiting request with the lowest round, and within a round the one received first.

Example. A files three requests, then B files one, then C files one, then B a second. A's first is taken at once. The order after it is B1, C1 (round 1), A2, B2 (round 2, by time), A3 (round 3). This is `test_fair_queue_defers_a_users_later_requests`.

The brief's literal wording ("handled after all other outstanding requests") cannot hold for two requesters who both have several requests open, since each would have to wait for the other. Rounds resolve that by alternating them. Rounds are fixed when a request arrives and are not recomputed, so a heavy requester's later requests cannot jump ahead when their first one closes.

A requester is an email address, normalized so that `jane+1@gmail.com` and `j.ane@gmail.com` count as one person. Someone with several real addresses can still get several round-1 places; the portal cannot prevent that without collecting identity the statute does not require.

## Triage

`triage/rules.py` runs first, needs no network, and decides in this order:

1.  A parent or student asking for their own education records: Policy JRA (principal, 14 days, RSA 189:66, IV). `outside_policy`.
2.  A named meeting's minutes, agenda, packet or recording that the knowledge graph holds: `public_info`. If the minutes are missing, the draft carries a placeholder that blocks sending.
3.  A named Board policy: `public_info`.
4.  Individual student, personnel, attorney-client or security records: `outside_rsa`, citing the exemption (RSA 91-A:5, III, IV, VI, XI, XII). Personnel requests carry a note that, since *Union Leader v. Town of Salem* and *Seacoast Newspapers v. Portsmouth* (2020), they need a balancing test, not a categorical refusal.
5.  Counts or rates about students: `aggregate_only`, small counts suppressed.
6.  Records kept by another agency (the City, the state): `outside_policy`.
7.  A question or a request to compile something new, with no record named: `outside_rsa` (RSA 91-A:4, VII), unless the public record already answers it.
8.  A strong knowledge-graph match: `public_info`.
9.  Everything else: `records_search`.

It also notes bulk email requests (the $1.00 charge past 250 communications and the EH-F(1) waiver), thumb-drive and free-copy requests (EH-R(1) terms), drafts (RSA 91-A:5, IX) and other requests from the same person within 30 days.

With `RTK_ANTHROPIC_API_KEY` set, Claude then triages with the rules result as hints. It searches the knowledge graph through tools and submits a structured result. The portal checks that result before staff see it:

-   citations must come from the closed list in `law.py`; others are dropped;
-   every URL in the draft must have come from a tool result, the citation list or the portal; any other is marked `[[unverified link]]`;
-   the request text is passed as quoted data, never as instructions;
-   any error falls back to the rules draft, with a note saying so.

Drafts mark anything a person must supply as `[[...]]`. The console refuses to send a draft that still contains `[[` or `]]`.

## What is published

-   Each verified request: number, time received, due date, round, status, requester shown as "Requester" unless they ticked the box to show their name.
-   The request text, with emails and phone numbers masked. Text that may identify a student or another private person (a parent naming a child, a date of birth, a student ID, a name next to a word like IEP or discipline) is held until staff publish a redacted copy.
-   Every response and five-day statement sent through the portal. The public copy replaces the quoted request with its public text, removes the requester's email address, and removes their name unless they chose to show it.
-   Nothing about unverified requests, which are deleted after 24 hours.

Every public event is chained: `hash = sha256(prev_hash + canonical_json({request_id, at, type, actor, data}))`, starting from 64 zeros, where canonical JSON has sorted keys and no spaces. To check the log:

```python
import hashlib, json, urllib.request
ev = json.load(urllib.request.urlopen("https://PORTAL/log/events.json"))["events"]
prev = "0" * 64
for e in ev:
    body = json.dumps({k: e[k] for k in ("request_id", "at", "type", "actor", "data")},
                      sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    assert e["prev_hash"] == prev and hashlib.sha256((prev + body).encode()).hexdigest() == e["hash"], e["seq"]
    prev = e["hash"]
print("chain intact through", ev[-1]["seq"] if ev else 0)
```

## Business days

A request is received when its email is verified. It is due on the fifth business day after the day of receipt. A business day is a weekday that is not a legal holiday under RSA 288:1 (including Election Day in even years) and not a day staff mark closed on the console's calendar page. Staff can also mark a holiday open. A request filed on a weekend is counted from that day, which gives a due date no later than counting from the next business day would.

## Running it

```sh
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements-dev.txt
cp config.example.env .env            # edit it
set -a; . ./.env; set +a
python -m rtk_portal.kg build --repo "$RTK_REPO_PATH"    # about 6 s, about 90 MB
uvicorn rtk_portal.web:app --host 127.0.0.1 --port 8091
pytest -q                              # 56 tests, uses a small fixture graph
```

For a local trial, `RTK_MAIL_BACKEND=outbox` writes every message, including the codes, to `data/outbox/*.eml`.

Production notes:

-   Run **one** uvicorn worker. The single-request rule is enforced in the database, but triage runs on one worker thread inside the process, which also checks the queue every 30 seconds.
-   Put it behind a reverse proxy that terminates TLS, and set `RTK_HTTPS_ONLY=true` and `RTK_TRUST_PROXY=true`. Without `RTK_TRUST_PROXY`, every visitor looks like the proxy and the per-IP limits (20 filings and 30 codes an hour) apply to everyone at once. The portal reads the rightmost `X-Forwarded-For` entry, the one a single proxy appends; behind a chain of proxies, run uvicorn with `--proxy-headers --forwarded-allow-ips` instead.
-   Restrict the staff console to the District's network with `RTK_STAFF_ALLOWED_IPS` (comma-separated CIDR ranges). Staff sign in with an emailed code; wrong guesses are capped at 15 a day per address across all codes, which also means an outsider who knows a staff address can lock it out for a day. An IP restriction, or single sign-on in front of `/staff`, closes both gaps.
-   Anchor the event chain outside the portal. `/log/head.json` gives the latest sequence number and hash; a nightly job that commits it to the CSBMN repository (or posts it anywhere public) means a rewritten log no longer matches what was published before.
-   Back up `data/rtk.db`. It is the log of record. `kg.db` can be rebuilt.
-   Rebuild the index after each Navigator publish, for example nightly: `git -C "$RTK_REPO_PATH" pull && python -m rtk_portal.kg build --repo "$RTK_REPO_PATH"`. The build writes a temporary file and swaps it in, so the running portal is not disturbed. The console shows when the index was built and from which commit.
-   The policy index is a snapshot (`rtk_portal/data/policy_index.md`, taken 2026-10-30). Refresh it when the Board adopts policies.

## Review

An independent review of the code on 2026-10-30 reported 19 defects, all fixed, each with a regression test in `tests/test_review_fixes.py`. The serious ones: held request text could reach the public log through the search link and AI prompt in a sent response; email subjects were published unscrubbed; citing "Policy EH" in a request for emails made the draft say the records were already public; mail and Claude calls blocked the web server; and the Claude path sent response-only fields back to the API, which would likely have made every Claude triage fall back to the rules engine. The Claude path has been tested with a fake client only; run one real request through it before a pilot.

## Decisions to confirm before a pilot

1.  **Who operates it.** The footer names CCTV/CCMC, following the October 2026 proposal. Change `RTK_OPERATOR` if the boards decide otherwise.
2.  **Name publication.** The name box is unchecked by default, so a name is shown only on an affirmative choice. The proposal said "shown by default"; a pre-ticked box is weak consent.
3.  **When request text goes public.** At verification, unless the privacy screen holds it. The proposal said status pages show the request text while a request is open, which this follows.
4.  **Contact retention.** `RTK_CONTACT_RETENTION_DAYS` replaces requester email addresses on closed requests after that many days (in the request and audit tables; the development `outbox/` folder is not touched). It is off by default because the District's retention schedule (Policy EHB) may require keeping them; set it once that is settled.
5.  **SAU 6 records.** Policy EH covers Claremont School District records. SAU 6 is a separate public agency; requests for SAU office records are triaged like District requests. Decide whether the same custodian handles them.

## Limits

-   The one-time code proves control of an inbox, not who someone is. RSA 91-A does not ask requesters to identify themselves.
-   The rules engine reads keywords. It will misfile some requests; that is why staff can re-run triage with a chosen category, and why nothing is sent without review.
-   The knowledge graph is a snapshot of what the Navigator holds. A record the District posted after the last build will not be found.
-   `law.py` was checked against gc.nh.gov on 2026-10-30. That site's RSA 91-A:4 page did not yet show HB 164 (2026, ch. 206, effective August 31, 2026), which lets an agency answer for a record on the state-designated website by giving its address; the drafts do not rely on it.

## Sources

-   [RSA 91-A:1-a](https://gc.nh.gov/rsa/html/VI/91-A/91-A-1-a.htm), [91-A:2](https://gc.nh.gov/rsa/html/VI/91-A/91-A-2.htm), [91-A:4](https://gc.nh.gov/rsa/html/VI/91-A/91-A-4.htm), [91-A:5](https://gc.nh.gov/rsa/html/VI/91-A/91-A-5.htm), [91-A:7](https://gc.nh.gov/rsa/html/VI/91-A/91-A-7.htm)
-   [RSA 189:66](https://gc.nh.gov/rsa/html/XV/189/189-66.htm), [RSA 288:1](https://gencourt.state.nh.us/rsa/html/XXV/288/288-mrg.htm)
-   Claremont School Board [Policy EH](https://docs.google.com/document/d/1BTHJCvjPSXnX17cOG9MWJ3B9L0lCy88Q/edit), [Procedure EH-R(1)](https://docs.google.com/document/d/1hvzCwEFgpb3HxhuuREmQuscERXjGhPYu/edit), [Policy JRA](https://docs.google.com/document/d/1VLVtiQxCRKyj-tUIobXisXcc7IHFdu2K/edit), [policy index](https://docs.google.com/document/d/1JmygIGNaVc8ZfaQWtoIA25tRaBGw2Oh5k5ARsGlreqg/edit)
-   [NHMA on *Union Leader v. Town of Salem* (2020)](https://www.nhmunicipal.org/court-update/internal-personnel-practices-are-not-se-exempt-disclosure-exempt-if-disclosure)
-   [Granite State Report, September 16, 2026: changes to RSA 91-A since 2024](https://granitestatereport.com/2026/09/16/what-changed-in-new-hampshires-right-to-know-law/)

## License

Code: Apache License 2.0, like the rest of the CSBMN repository's software (each `.py` file carries the SPDX header). The policy index snapshot is the District's document, included for search and linked to its source.