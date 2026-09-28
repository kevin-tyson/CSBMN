# Backlog attribution report: Claremont / SAU 6, Jan 2015 to Jan 2023

184 transcripts processed into `Output/Dialogue/*.CSV` on 2026-09-26. **116,969 dialogue rows, about 342 hours of public meetings.** Every transcribed word is preserved verbatim, ASR garbles included; all timestamps come straight from the source JSON.

## Verification

Every CSV passed the builder's integrity checks and an independent run of `Scripts/verify_dialogue.py` against its source JSON (token parity, timestamps, monotonicity, schema, non-empty cells). No CSV contains an em or en dash. A name-normalization pass merged twelve variant spellings of the same person (for example `Pat Barry` into Patricia Barry, `Mike Koski` into Michael Koski, `Josh Lambert` into Joshua Lambert); the 24 affected files were rebuilt and re-verified.

**14.8% of rows (17,325) are `Unidentified`** with an explanatory Role. This is higher than the 2025-26 backlog (8.2%) because pre-2019 roll calls often run the names together, the diarizer merged same-sex voices heavily, and several recordings are deliberative sessions and special district meetings with long, unnamed public comment (12/12/19 special meeting 58.5%; 11/21/19 52.7%; 10/16/19 52%, mostly Bluff Elementary students). Roughly **10,200 per-segment overrides** correct diarizer merges and flaps; the original cluster label stays in `Diarized As`.

Per-meeting evidence, confidence ratings and open items: `Scripts/attribution_reports_2015_2023/<TranscriptName>.md`. Speaker maps: `Scripts/speakers/`. Roster: `Scripts/roster_2015_2023.md`. Raw roll-call harvest: `Scripts/rollcall_evidence_2015_2023.md`.

## Governance timeline established from the record

**Claremont School Board chairs**
- Richard Seaman chaired in 2015 and through the 2/3/16 meeting and deliberative session (addressed as "Richard" by the superintendent).
- 3/16/16: Brian Rapp elected chair 4-3 over Becky (Rebecca) Ferland; Chris Irish vice chair.
- 3/15/17: Rapp re-elected chair, Irish vice chair.
- Rapp still chaired the 1/30/18 joint meeting. Frank Sprague chairs from 1/31/18 (the transfer vote is not on the 1/31 recording).
- 3/21/18: Sprague re-elected chair, Rebecca Zullo vice chair. 3/20/19: Sprague re-elected, Zullo elected vice chair over Jason Benware.
- 5/6/20: Sprague re-elected, Heather Whitney elected vice chair. 3/17/21: Sprague re-elected.
- 4/6/22: Michael Petrin elected chair, Heather Whitney vice chair.

**SAU 6 Board chairs**
- Sara Lowe (Unity) chair in 2017; re-elected 3/29/18 with Petrin vice chair and Michelle Pierce treasurer.
- 6/14/18: Lowe stepped down; Marjorie Erickson elected chair 6-4 over Petrin.
- 3/28/19 (file 10304, named 032519): Petrin elected chair, Erickson vice chair. Petrin re-elected 7/1/21 in absentia.
- 4/21/22: Erickson elected chair in absentia after Petrin declined; Frank Sprague vice chair.

**Superintendents and key staff**
- Middleton McGoodwin through June 2018; read his resignation 6/14/18. Cory LeClair appointed acting superintendent that night.
- Keith Pfeifer approved as interim superintendent 7/26/18 (first board meeting 8/15/18). Cory LeClair acting superintendent again Feb to Jun 2019.
- Michael Tempesta from 7/1/19 through Jan 2023.
- Business administrator Michael O'Neill through spring 2019; Richard Seaman (the former board chair) business administrator / assistant superintendent for finance from fall 2019.
- Ben Nester approved as SAU 6 special education director by roll call 5/10/18.
- Mary Woodman clerk and recording secretary throughout; her resignation announced effective 6/1/22 (clerk pay then raised from $75 to $150 per meeting at SAU 6).

**Seat changes**
- Becky Ferland resigned (treated as accepted 10/5/16); Alex Herzog appointed and sworn in 11/2/16 (Richard Seaman withdrew).
- Brent Ferland's resignation accepted effective 3/13/17 (1/18/17).
- Patrick Adrian's seat: Alex Herzog appointed and sworn in again on 11/1/17 (recording says Herzog was appointed to Adrian's seat; check against minutes given the 11/2/16 appointment).
- Steven Horsky resignation announced 10/3/18; Rob Lovett Jr. appointed 11/7/18 to serve until March.
- Carolyn Towle died 5/11/21 while serving; Nicholas Stone appointed and sworn in 6/2/21.
- Joshua Lambert resigned by 1/11/23; the board left the seat for the March 2023 election.

**Votes captured on the record (sample)**
- 1/3/18: FY19 budget of $31,148,256.95 sent to deliberative session 4-3 (Irish, Pierce, Sprague, Zullo yes; Herzog, Petrin, Rapp no); Herzog's $31,455,410 amendment failed 3-4.
- 9/5/18: needle-exchange approval 5-2 by roll call.
- 1/21/20: warrant cut to $350k/$150k failed 2-4; $38,202,661 budget sent to deliberative session.
- 8/5/20: hybrid reopening passed 5-2. 9/1/21: COVID matrix amendment 4-3. 2/16/22: mask-optional matrix 5-2.
- 4/21/22 SAU 6: merit-pay motions failed (4-6 to suspend; 5-5 on the amended motion).
- 1/17/23: $37,345,312 sent to deliberative session 5-1 (the prior private-ballot result on $38,345,312 is inaudible).

## Possible file-name date errors (for MAP.md)
- `14627 SchoolBoard091522` is probably the **9/21/22** meeting (chair says "September 21st").
- `10304 SAU6032519` is the **3/28/19** SAU 6 meeting.
- `11216 SchoolBoard020321` content fits **1/27/21**.
- `11527 SchoolBoard041521` is the same recording as `11444 SchoolBoard040721` (identical tokens, different diarization).
- 12/6/17 has three recordings (9495, 9496 full; 9497 partial); 1/3/18 has four parts (9547/9548 hearing, 9549/9550 meeting).

## Open items for human review
- **2015 board roster**: Richard Seaman chair; a member "Richard Madigan" rests on one ASR mention; board member "John" and "Bob" have no surnames.
- **Frank Sprague's start**: he said on 5/1/19 he was in his "sixth year", implying service before 2016.
- **Student representative**: "Marion / Marian / Mary Ann Lovett" (2016-17) left unmerged pending a record.
- **CMS principal 2017-18**: "Paulette Gerald / Paul Gerald / Paulette Fitzgerald / Paula Fitzgerald" left unmerged.
- **Special education director "Chris" (2016-17)**: surname heard only as "Bezos".
- **Moderator**: "Tracy" is on the record several times; surname Pope is from the roster; the 11/21/19 and 12/12/19 moderators are unnamed.
- **"Dr. Janeiro" / "Mary Ellen"** (curriculum, 2021-22) spelling unverified.
- Same-name pairs kept separate: Tom Connor / Tom Connair, Christine Downing / Christine Downey, Chris Pratt / Christopher Pratt, Steve / Steven Moss, Lisa / Liza Draper.
- The Rapp-to-Sprague chair vote (reported 5-2, 1/31/18) is not on any recording in this batch.

## Follow-through on 2026-09-26: map and pages

- `MAP.md` gained 180 sections (2015 to 2022; every later section renumbered by 180), each with a `Remote video:` line confirmed against the Cablecast API. The 2022 packet archives supplied folders for ten meetings; the other 170 predate anything the district posts online.
- 184 meeting pages were built in `Output/HTML/` (the 180 plus the four January 2023 meetings) and `index.html` now covers 312 meetings, January 21, 2015 to September 16, 2026. Flags on the new pages: 12 HIGH, 119 MEDIUM, 605 OBSERVATION, 282 POSITIVE (counted from the pages after an independent review of every HIGH flag downgraded 5 to MEDIUM).
- Page builders logged suggested attribution fixes (mostly names the minutes supply for Unidentified rows, and roll-call answers in the wrong cluster) in `Scripts/csv_corrections_2015_2023.md`. The CSVs were not edited; apply the ledger in a later pass and rebuild the affected pages.
- Vintage-checked legal anchors for 2015 to 2022 are in `Scripts/anchors_2015_2022.md` (statutes as they read on each meeting date).

### Date questions for a human decision (MAP headings left unchanged)
- `9734 SchoolBoardCityCouncilJoint042418`: the recording, the show title ("4-17"), a 4/18/18 public comment and the 6/21/18 minutes approval all point to **April 17, 2018**, not April 24.
- `10722 SchoolBoardDeliberative020120`: the Valley News notice and the 1/21/20 board vote point to **Wednesday, February 5, 2020**; the moderator says "February 6th"; Cablecast says 2/1.
- `9602 SchoolBoardDeliberative020818`: announced on 1/30 and 1/31/18 for February 7; Cablecast title and eventDate say 2/8.
