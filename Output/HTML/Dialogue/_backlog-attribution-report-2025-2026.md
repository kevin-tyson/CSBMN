# Backlog attribution report — Claremont / SAU 6, Jan 2025 – Jan 2026

39 transcripts processed into `Output/Dialogue/*.CSV`. **25,432 dialogue rows,
~73 hours of public meetings.** Every transcribed word is preserved verbatim,
including ASR garbles; all timestamps come straight from the source JSON.

## Verification

An independent QA pass re-derived every CSV from its source JSON and compared
row-for-row. **Zero discrepancies** across all 39 files on: token parity (every
transcribed word present, in order), clock and second-precision timestamps,
timestamp monotonicity, `end >= start`, preserved `Diarized As` cluster labels,
non-empty Speaker and Dialogue cells, and the fixed 8-column schema.

Each file additionally passed its own build-time integrity checks and a skeptical
review pass (sub-second onset-clip audit, spot-checks against the working
transcript, and reconciliation of the speaker distribution against the override
ledger).

**8.2% of rows (2,076) are labelled `Unidentified`** with an explanatory Role
rather than being guessed. These concentrate in crisis-era meetings with long
open-mic public comment (8/25/25: 36%; 1/20/26 budget hearing: 39%; 9/17/25: 33%)
where dozens of speakers approach a podium without stating a name.

## Attribution method

Every name rests on an in-transcript anchor — roll call, self-identification at
the mic, the chair's recognition, floor control, or role-specific content —
corroborated wherever possible against approved minutes and public reporting.
Uncertainty lives in the Role column (`(uncertain — …)`, `(attribution by
elimination)`, `(as announced; not on public roster)`), never silently inside a
name.

This diarizer merges same-sex voices into single clusters, splits one voice
across clusters mid-speech, absorbs the chair's recognition into the next
speaker's segment, and clips sentence onsets into neighbouring clusters. Those
flaps were corrected with per-segment overrides — **roughly 5,900 across the
corpus** — while the original cluster label stays in `Diarized As` so every
attribution remains auditable.

## Governance findings established from the record

These were unknown or unsettled at the start and are now documented:

- **Board officers.** Heather Whitney chaired throughout the whole window.
  Frank Sprague was Vice Chair through the March 2025 election; **Michael Petrin
  was elected Vice Chair on 3/19/25** (in absentia) and held it thereafter.
- **SAU 6 Board reorganized 4/10/25:** Arlene Hawkins Chair, Rocco Ruggeri
  (Unity) Vice Chair, Candace Crawford Treasurer.
- **The Sprague vacancy, resolved.** Sprague resigned (announced 9/3/25). Five
  people applied; the 10/1/25 appointment vote **deadlocked 3–3** (Don Lavalette:
  Crawford/Hawkins/Howard — Kevin Tyson: Whitney/Petrin/Madden) and was tabled.
  The seat stayed empty through 10/6 and 10/15. On **11/5/25**, appointing
  Lavalette failed 3–3 again, reopening applications failed, and Petrin's motion
  to **reinstate Frank Sprague carried 3–2 with Howard abstaining**. Sprague was
  seated and active from 11/13/25 on. (Don Lavalette, who lost that appointment,
  won a seat in the March 2026 election — he appears in this backlog only as a
  Ward 2 public commenter and applicant.)
- **Finance subcommittee membership changed hands.** Sprague chaired it in early
  2025; by fall 2025 it was **Crawford (chair) + Whitney only**, staffed by Angell
  and Kennedy.
- **Leadership timeline confirmed on the record:** Pratt's last public meeting
  8/14/25 → Patrick O'Hearn acting superintendent 8/28–9/12 → **Kerry Kennedy
  appointed interim superintendent at the 9/11/25 SAU 6 meeting**, which also
  accepted Pratt's resignation. Kennedy kept the CMS principalship concurrently.
  Mary Henry was on medical leave by 6/18/25, on administrative leave from ~8/22,
  and terminated by mutual agreement effective 11/4/25. Matt Angell ran finance
  from 8/22/25 onward.
- **Crisis actions captured:** the 20-position RIF and elimination of
  extracurriculars (8/25/25), the $4M Revenue Anticipation Note hearing and 6–0
  approval (9/3/25), the TMS Consulting engagement (9/11/25), the school
  realignment models and their rejection (12/17/25, 1/7/26), and the 4–3 adoption
  of the $42.9M FY27 budget (1/21/26) — recorded on the tape as a voice vote
  ("three ayes have it" for the opposition), consistent with the reported 4–3.

## Corrections worth noting (transcripts left verbatim)

The ASR mangles proper names relentlessly; the CSVs carry the garbles as heard.
The most consequential, now documented for future runs: `Mr. Peterson` /
`Mr. Patron` / `Mr. Trump` = **Petrin**; `Miss Gillan` = **Skillen**;
`Arlene Hopkins` = **Hawkins**; `Matt Angel` / `Matt Eagle` = **Angell**;
`Carrie Kennedy` / `miscarry Kennedy` = **Kerry Kennedy**; `Mr. Caskey` =
**Koski**; `Chromebook` / `Mr. Cromer` = **Kronberg**; `Doctor Harrington` =
**Herrington**; `Candace Parker` / `Kenneth Crawford` = **Candace Crawford**;
`Plasma and Sanderson` = **Plodzik & Sanderson**; `Nasdaq` = **NESDEC** (or
NEASC, by topic). A full glossary of ~200 mappings was accumulated during the run.

**Auditor naming:** these CSVs use **Michael Campo** (Plodzik & Sanderson), the
verified name. The previously shipped 8/5/26 and 8/12/26 dialogues still carry the
incorrect label "Mike Campbell" — worth fixing if those are ever regenerated.

## Open items for human review

- **Two 1/6/25 finance details:** no formal chair was addressed; Crawford presided
  in practice but Sprague pronounced adjournment, so the nominal chairmanship that
  day is unresolved (Roles say only "presides over this session").
- **Possible same-person pairs left unmerged** because the evidence differed
  across meetings: `Hannah Brooks` (3/5, public-health presenter) vs `Hanna Brooks`
  (3/19, commenter); `Jennifer Gallagher` (3/5, Turning Points educator) vs
  `Jen Gallagher` (3/19, former board member); `Cassandra Edwards` (11/5, 12/17)
  vs `Sandra Edwards` (1/7); `Kari Hague` (3/5) vs `Karry Rochford-Hague` (3/19).
- **Normalized during QA:** `Don Lavallee` → **Don Lavalette** (10/1) and
  `Cameron Lownie` → **Camron Lownie** (11/5), with the change noted in each
  affected Role cell.
- **Unity board membership in 2025** is only partly verifiable: Ruggeri, Popescu
  and **Crystal Davis** appear in roll calls; Davis is absent from the 2026
  roster and could not be confirmed against any public source.
- **Meeting minutes are sparse on Drive.** Approved CSB minutes exist for
  Jan–Apr 2025 plus a 10/15/25 draft (`CSB_2025_Minutes.pdf`); a
  `CSB_Finance.pdf` holds fall-2025 finance minutes. No SAU 6 minutes are posted
  at all, and the 2026 minutes folder was empty. Most Aug 2025 – Jan 2026
  attributions therefore rest on transcript evidence plus contemporaneous
  reporting.

## Sources

Eagle Times 3/12/25 (election results). Valley News: 2/26/25 (candidates),
3/17/25 (Unity withdrawal), 3/21/25 (3/19 meeting), 8/21/25 (crisis), 9/12/25
(Pratt resignation, Kennedy appointment), 9/18/25 (Bluff), 10/9/25 (staff
resignations), 11/6/25 (Henry), 12/19/25 (realignment), 1/8/26 (three-school
rejection), 1/22/26 (budget adoption). Union Leader Aug 2025 (leave, O'Hearn).
sau6.org rosters. Ballotpedia (Claremont School District). Google Drive:
`CSB_2025_Minutes.pdf`, `CSB_Finance.pdf`, `CSB_Unseeled_Minutes.pdf`, packet
folders. Project memory `claremont_speakers.md`.
