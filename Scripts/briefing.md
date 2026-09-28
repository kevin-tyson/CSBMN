# Attribution run briefing — Claremont / SAU 6 dialogue backlog

You are attributing ONE meeting transcript end-to-end. Everything below is the shared
contract for this run. Read it fully before touching the transcript.

## Two hard rules

1. **Retain the data.** Every transcribed word appears verbatim in the CSV, ASR garbles
   included. Never "fix" what was heard — a garbled "Second Sanderson" stays "Second
   Sanderson" even though the firm is Plodzik & Sanderson. Report corrections in your
   write-up instead. All timestamps come straight from the source.
2. **Name only what you can defend.** Every name in the Speaker column needs an anchor in
   the transcript (roll call, self-identification, direct address, chair's recognition) or a
   public record — ideally both. Uncertainty goes in the Role column, never silently into a
   name. `Unidentified` with a descriptive Role is a correct answer; a confident guess is not.
   Honest `Unidentified` rates in this corpus run 8-10% and that is fine.

## Where things are (all on the user's machine — use device_bash, never stage files)

Working dir: `$HOME/mnt/Government Transparency Project`
- input      `Input/Transcripts/<STEM>.json`
- output     `Output/HTML/Dialogue/<STEM>.CSV`      (exact same stem, uppercase .CSV)
- mapping    `Scripts/speakers/<STEM>.speakers.json`  (keep it — it is the provenance record)
- scratch    `/tmp/<STEM>/`                     (working.txt etc; never write scratch into the project)

`mcp__remote-devices__device_bash` runs on the user's machine with that folder mounted.
Each call is a fresh shell with a ~45s limit, so split long work. Do NOT use
device_stage_files: these JSONs are 1-4 MB and everything you need runs on the device.

## Prior knowledge — read it before attributing

Call `mcp__remote-devices__project_memory_read` for the roster note covering your meeting:
- `claremont_speakers_2025.md` — Jan 2025 - Jan 2026. Board eras, staff timeline, SAU 6
  membership, crisis chronology, and a large ASR garble glossary.
- `claremont_speakers.md` — 2026 roster (as of Aug 2026), staff, and a second glossary.
- `claremont_meeting_81926.md` — 8/19/26 specifics.
Both glossaries are useful outside their window; the ROSTERS are not — check the date.

Already-shipped CSVs in `Output/HTML/Dialogue/` are evidence too. The meeting before or after
yours often settles who was on the board and who was absent. Read them.

## Procedure

1. `mkdir -p /tmp/<STEM> && python3 Scripts/transcript_to_dialogue.py "Input/Transcripts/<STEM>.json" --dump-text /tmp/<STEM>/working.txt`
   It prints segment counts per diarized label and lists zero-word segments.
2. Read `/tmp/<STEM>/working.txt` **in full** (chunk it with sed -n '1,400p' etc). The roll
   call is usually in the first 40 segments. Do not skim: attribution evidence is scattered.
3. Use `--scan-names "name1,name2,..."` to find word-level mentions of candidate names with
   ASR confidence — the reliable way to catch a swallowed roll-call surname.
4. Build the mapping. Every diarized label needs an entry:
   `{"Speaker 1": {"name": "...", "role": "..."}, "__overrides__": {"68": {"name": "..."}}}`
   `__overrides__` reassigns single segments (0-based [idx] from working.txt, counted over
   ALL segments including zero-word ones). The build FAILS if an override never applies.
5. `python3 Scripts/transcript_to_dialogue.py "Input/Transcripts/<STEM>.json" --speakers "Scripts/speakers/<STEM>.speakers.json" --out "Output/HTML/Dialogue/<STEM>.CSV"`
6. `python3 Scripts/verify_dialogue.py "Input/Transcripts/<STEM>.json" "Output/HTML/Dialogue/<STEM>.CSV"`
   Both must exit 0. A failed check is a bug to fix, never something to bypass.
7. Skeptical pass: re-read the segments behind your WEAKEST attribution hunting for
   counterevidence, and spot-check a few rows against working.txt.

## What this diarizer does wrong (audit for all four, every time)

- **Merges same-sex voices** into one cluster — two men or two women sharing "Speaker 1".
  Split them with `__overrides__` by topic and role: staff report operational detail,
  members ask questions.
- **Splits one voice across clusters** mid-speech.
- **Absorbs the chair's recognition into the next speaker's onset** — "Thank you. Lauren."
  landing at the head of Loren Howard's segment. These are reliable identity anchors.
- **Clips sub-second sentence onsets into the neighbouring cluster.** Any fragment under
  ~1s with a ~80ms gap to the next segment is almost certainly the NEXT speaker's onset.
  Check every one.
Verify override indices against the printed label distribution before shipping — an
off-by-one is the commonest error in this run's history.

## Report back (this is your return value, keep it tight)

- `STEM` and one line of outcome: rows, tokens, span, overrides applied, both checks passed.
- **Voice mapping table**: diarized label -> name, role, evidence, confidence (high/medium/low).
- **New people** not already in the roster notes, with the evidence that names them.
- **New ASR garbles** worth adding to the glossary (`heard` = actual).
- **Unresolved**: unidentified clusters, conflicting evidence, anything a human should settle.
- **Record caveats**: nonpublic gaps, recording shorter than the meeting, roll call missing.
Do not paste the CSV or the transcript back. Facts and evidence only.

---

# ADDENDUM 1 — proven by the Feb–Mar 2026 wave (read this if your meeting is 2026)

## The board changes on 3/18/26. Use the right side of that line.

**Before 3/18/26** (through the 3/4/26 meeting) — SEVEN members:
Heather Whitney (CHAIR), Michael Petrin (vice chair), Candace Crawford (Finance chair;
also Capital Improvement chair), Arlene Hawkins (Policy chair), William "Bill" Madden,
Loren Howard, Frank Sprague.

**On 3/18/26** (organizational meeting, show 17241) — the handover, all voice votes:
- **Candace Crawford elected CHAIR** (moved, seconded by Rapp, "the ayes have it", no count).
- **Michael Petrin STAYS vice chair**: Petrin moved to step aside for Whitney; the vote went
  3–2, then 3–3 when Crawford voted, and the clerk ruled no majority. "So Mike stays."
- **Sworn in: Don Lavalette and Brian Rapp** (elected 3/10/26, terms to 2029).
- **Gone: Frank Sprague and Arlene Hawkins.** Neither appears in any later roll call.
  BUT Sprague stays on the superintendent search committee after leaving the board.
- Roll-call order from 3/18 onward: **Howard, Lavalette, Madden, Petrin, Rapp, Whitney,
  Crawford (chair last)**. That order is stable across three roll calls and is a reliable
  way to name a voice from its position in the sequence.
- Subcommittees read into the record: Capital Improvements — **Madden** chair, Petrin, Rapp.
  Finance — **Crawford** chair, Whitney, Lavalette. Policy — **Howard** chair, Lavalette,
  Rapp. Curriculum — Madden, Lavalette, Howard. SRVRTC — **Petrin** chair, Howard, Crawford.
  NHSBA delegate — Howard. SREA negotiations — Whitney. Superintendent evaluation —
  Crawford, Lavalette, Rapp. Ad hoc communications — Howard. **School Reconfiguration
  Exploratory Committee** — Whitney + Lavalette, created 6–1 with Rapp the lone no.
  Bylaws ad hoc — Whitney, Lavalette, Crawford (formed by consensus, no vote).

## Staff through spring 2026 (NOT the Aug 2026 roster)
- **Kerry Kennedy — Interim Superintendent** (she presides at 3/18 until a chair is elected).
- **Matt Angell — Interim Business Administrator** (introduced once as "senior Comptroller").
- **Noelle Kronberg — School Board Clerk**, sworn 3/18/26; reads every roll call.
- Principals: **Melissa Lewis** (Disnard), **Mark Blount** (Maple Ave — ASR "Mark blunt"),
  **Dr. Michael Herrington** (Stevens), **Michelle Herrington** (SRVRTC assistant director).
  Dave Irwin (Maple Ave) and Nicole Boynton (CMS) come LATER — not in this window.
- **Dr. Tim Broadrick is not superintendent yet.** The search: 8 resumes, 3 video interviews,
  2 withdrew, one "very, very strong" candidate left as of 3/18/26. Committee = Madden,
  Petrin, Sprague. He starts 7/1/26.
- Counsel: **James "Jim" O'Shaughnessy**, Drummond Woodsum. **Naomi Butterfield /
  Bernstein Shur** (ASR "Bernstein Shaw") is the board's SEPARATE counsel for the forensic
  audit, retained 2/4/26 at "not more than $2,500".
- Auditor: **Michael Campo**, Plodzik & Sanderson. ASR "my Campbell", "Mike Campbell" —
  **Campo is canonical; do not write Campbell.**

## Recurring public voices in 2026 (all self-identify by name and ward)
Gary Merchant (W2, **sitting NH state rep**, Stevens '71) · John Cloutier (NH state rep, W1,
Stevens '75; ASR "John Claudia") · Wayne Hemingway (NH state rep AND city councilor, parent;
ASR "Wayne coming away") · Hope Damon (NH state rep, Croydon, House Education Funding) ·
Matt Bean (W1; ASR "Matt Beam") · Sherry Williams (W1) · Ken Lownie + Camron Lownie (W2,
father and son) · Mark Chamberlain (W1, retired banker) · Leslie Peabody (W1, Stevens
science teacher — NOT Eric Peabody) · Kiran Adrian (W1, Stevens senior) · Nora Shane (W3,
Stevens senior) · Noah Bosch (W3, Stevens senior) · April Woodman (write-in candidate for
School District Moderator) · Bonnie Miles (W2, former board member) · Kyle Mercier (W1) ·
Tom Luther (W1) · Mimi Rhines (W1, SREA building rep) · Cassandra Edwards (W3, Disnard
teacher; ASR "Sandra Edwards") · January King (W1) · Rebecca Menard (W3) · Michelle Springer
(W2) · Amanda Barton (W2) · Emily Sandblade (W3) · Kevin Tyson (W2) · Luke Diamond (W3) ·
Patrick Adrian (W1). Moderator: **Tracy Pope** (the 2/1/25 minutes spell her "Tracey" — show
the conflict, never pick silently).

## Two of these recordings are EXCERPTS of other recordings — check before you assume
- **16958 = an excerpt of 16951** (11/5/25), offset +7768.8 s, plus a spliced cold open.
- **17168 = an excerpt of 17159** (2/18/26), offset +2277.9 s, clipped mid-turn at the end.
If your recording opens mid-business, has no roll call, or ends mid-sentence, look for a
sibling show on the same date before concluding the meeting itself was odd. Say so plainly
in your report, and never compute a wall-clock time from an excerpt's timestamps.

## Attribution tactics that paid off in this wave
- **The roll-call ORDER is an anchor even when the ASR eats the names.** Position in the
  sequence plus one audible name pins the rest.
- **Chair recognitions are absorbed into the NEXT speaker's segment onset** constantly here
  ("Yes, Mr. Howard." at the head of Howard's own segment). Treat them as identity anchors.
- **This diarizer merges same-sex voices hard.** In this wave it merged Whitney+Kennedy+Hawkins
  into one cluster, Kennedy+Lewis into another, and Blount+Madden+Sprague into a third.
  Two women or two men in one cluster is the DEFAULT expectation, not the exception.
- **One voice routinely spans several clusters** (the 2/7 deliberative split the moderator
  across SEVEN). Cluster identity is a starting point; overrides carry the real attribution.
- Already-shipped CSVs of the meeting before and after yours are legitimate evidence and
  settled several calls in this wave. Use them.
- Honest `Unidentified` ran 3–9% in this wave, and 21% at the open-floor deliberative
  session. Open-mic public comment is where the rate belongs — not the board table.

## Corrections owed to already-shipped files (do NOT fix these yourself)
- `16951 SchoolBoard110525.mp4.CSV`: eight rows labelled `Unidentified public commenter —
  Ward 2` are **Don Lavalette** (starts 8980.22, 9063.26, 9063.94, 9073.70, 9085.66,
  9119.22, 9147.34, 9406.74). Being handled centrally in the QA pass.

---

# ADDENDUM 2 — the 2023-24 roster (read this if your meeting is 2023 or 2024)

Built 8/26/26 from two independent tracks that agree: roll-call mining across all 66
transcripts (raw evidence in `Scripts/rollcall_evidence_2023_2024.md`) and public-records
research. Where they differ, the note says so. **No project roster covered this era before
now — treat this as well-founded but newer than the 2025/2026 notes.**

## Claremont School Board — five distinct eras. Get the date right first.

**Era 0 — Jan 1 to Mar 14, 2023. SIX sitting members, one vacant seat.**
**Michael Petrin — CHAIR.** Heather Whitney — VICE CHAIR. Frank Sprague, Bonnie Miles,
Whitney Skillen, Steven Horsky.
> This is the one thing public reporting could NOT establish and the recordings did: the
> news had Sprague as the presumed chair. The roll calls show **Petrin** in the chair
> (ASR "Michael Patron", "Patrone"). He then **loses** the March 2023 one-year race to
> Jennifer Gallagher and leaves the board — so a "Petrin" voice is a MEMBER only before
> mid-March 2023 and again from ~March 2024. In between he is not on the board at all.

**Era 1 — Mar/Apr 2023 to Jun 21, 2023. SEVEN members.**
**Heather Whitney — CHAIR. Frank Sprague — VICE CHAIR.** Arlene Hawkins (elected 3/14/23,
417 votes), Jennifer Gallagher (elected 3/14/23, one-year seat), Bonnie Miles, Whitney
Skillen, Steven Horsky. Petrin gone.

**Era 2 — Jun 21 to Jul 19, 2023. SIX members.** Horsky **resigns on the record**,
"effective immediately", at the 6/21/23 meeting (segments 20-22 of show 15153).

**Era 3 — Jul 19, 2023 to Mar 12, 2024. SEVEN members.**
**Candace Crawford appointed 4-2** over David Bailey and Kevin Tyson — yes: Gallagher,
Hawkins, Miles, Skillen; **no: Whitney and Sprague**. Crawford had served on this board
1991-2002, six years as chair. Otherwise unchanged: Whitney (chair), Sprague (vice chair),
Hawkins, Gallagher, Miles, Skillen, Crawford.

**Era 4 — Mar 12, 2024 through the end of 2024. SEVEN members.**
Gallagher's one-year seat expires and she leaves; **Petrin returns as a WRITE-IN**. Whitney
and Crawford re-elected, all three races uncontested. Board: **Whitney (CHAIR), Sprague
(VICE CHAIR)**, Hawkins, Skillen, Miles, Petrin, Crawford — exactly the January 2025 roster
in `claremont_speakers_2025.md`, so that note's Era A picks up cleanly from here.

## Staff — the January 2024 rupture is the fact that matters most

- **Michael "Mike" Tempesta — Superintendent, SAU 6, July 2019 -> fired Jan 11-12, 2024.**
  The SAU 6 board voted him out after a nonpublic session, with six months' severance;
  Marjorie Erickson (Unity) dissented and Shannon Popescu (Unity) abstained. No reasons
  were stated publicly. **Any 2023 recording has Tempesta as superintendent.**
- **Chris Pratt** — **Principal of Stevens High School through Jan 11, 2024**, then
  **interim superintendent the same night**, then permanent (announced ~May 22-23, 2024).
  So a "Pratt" voice in 2023 is the HIGH SCHOOL PRINCIPAL, not the superintendent. There
  was no other interim.
- **Business administrator:** **Richard Seaman** (titled "Assistant Superintendent for
  Finance and Operations" in Jan 2023) reads his retirement letter 3/30/23, effective
  **4/14/2023**; **Dave Jack of MRI** (Municipal Resources Inc) covers the gap; **Mary
  Henry** starts **early July 2023**.
- **Ben Nester** — Director of Special Education, leaves for Lebanon; last meeting 6/20/24.
  **Michael McCosker** — Director of Student Services from 7/1/24. **Angela Vivian** — HR,
  succeeded by **Patrick O'Hearn** in April 2024. **Mike Koski** — Assistant Superintendent.
  **Jeff Small** — Director of Technology.
- **Michael Herrington** is Stevens principal by the June 2024 graduation; the exact
  changeover date is not established. **Michelle Herrington** becomes SRVRTC **assistant
  director** in **August 2024** — before that she was a Bluff Elementary guidance counselor.
  **Two different Herringtons overlap from Aug 2024 and both are "Mr./Miss Harrington" to
  the ASR.** Frank Romeo (CMS) and David Irwin (CMS assistant principal) are documented for
  2024-25 only.
- Elected: **Tracy Pope** moderator, **Jane Hunter** treasurer (both unopposed 3/14/23).
  **The district CLERK seat was VACANT through 2023** — no candidate filed. Noelle Kronberg
  is a 2025 arrival; do not put her in 2023.

## SAU 6 joint board (Claremont + Unity) — a DIFFERENT body, different chair
- **3/30/23: Steven Horsky elected SAU 6 chair 6-5 over Marjorie Erickson.** After his June
  resignation the 7/13/23 meeting nominates Erickson and Hawkins; the winner is not audible,
  but **Arlene Hawkins is "Chair Hawkins" from 11/9/23 onward**. **Hawkins re-elected
  4/11/24, with Rocco Ruggeri vice chair.**
- So through 2024 **Hawkins chairs the SAU board while Whitney chairs the Claremont board**.
  "The chair" means different people depending on which body is meeting. Check the filename.
- Unity side heard in these roll calls: **Marjorie Erickson** (Unity board chair), **Rocco
  Ruggeri**, **Shannon Popescu**, **Kelly Simpson**, **Atonya "Tanya" Hart**. Public records
  only confirm Erickson, Popescu and Ruggeri for this window — the roll calls are the better
  evidence for the other two, but say which you are relying on.
- Unity's withdrawal starts here: warrant approved March 2024, a 7-member study committee
  chaired by Ruggeri seated April 2024, feasibility report late Sept 2024.

## Name-attribution hazards specific to this era
- **"Whitney" is both a surname and a first name on the same board**: Heather Whitney
  (chair) and Whitney Skillen (member), in the same room. Highest-risk collision here.
- **Skillen** is the worst ASR name in the set: `Miss Gillen`, `Gillan`, `Scullin`,
  `Skilling`, `Skillet`. One 3/20/24 sentence uses two spellings for her in a row.
- **Horsky** comes through as `Hauschka` and `Steve Gorski`.
- **Petrin** as `Michael Patron`, `Patrone`, `Mr. Patron`.
- **Sprague** as `Greg`, `Craig`, `Spriggs`, `Bragg`.
- **Hawkins** as `Hopkins`, `Carly`, `Harley`, `Hoffman`, `early knocking`.
- **O'Hearn** as `Patrick Ahern. O'Hearn. Not her. Patrick overheard` — three failures in one
  sentence.
- A **"Crawford" voice before 7/19/23 is not a board member**; a **"Petrin" voice between
  mid-March 2023 and March 2024 is not a board member**. Both are the kind of error the
  2025 roster would invite if applied backwards.

## Two file-level traps
1. **`14875 SchoolBoard020123` and `Claremont School Board Meeting 2123` are the SAME
   2/1/2023 meeting, transcribed twice** with different diarization. Each is a free
   cross-check on the other. Both still get their own CSV — the CSV mirrors the transcript
   file, not the meeting.
2. **`15299 SAU6110923` sorts among the September shows but the meeting is 11/9/2023.**
   Sort by the DATE in the filename, never by show ID.

## Where the raw evidence lives
`Scripts/rollcall_evidence_2023_2024.md` — 66 meetings in date order, each with segments
0-39 verbatim, every self-ID hit in the file, every direct address in segments 0-79, and
the label counts. Consult your meeting's block there BEFORE dumping the transcript; it will
usually tell you the roll call and the recurring garbles in one read.

## Substance likely to come up (so you recognise it, not so you assert it)
2023: the 2/10/23 deliberative session amended the warrant **41-27** to restore $1,000,000
(from $37.34M to **$38.34M**); the March budget **$38,345,312** passed 519-262; a two-year
teachers' CBA approved 1/10/23; elementary reconfiguration (Bluff / Disnard / Maple Ave)
recurring; SRVRTC funding fights.
2024: the Tempesta firing; first budget year with **no ESSER** money; deliberative session
Sat 2/3/24; budget **$39.58M** proposed / $39.37M default passed March 2024; secretaries',
maintenance and paraprofessional CBAs; Unity's withdrawal; an exit-interview/turnover report
from O'Hearn in Sept 2024; a Student Recovery program report in Oct 2024; and chronically
late audits — Plodzik & Sanderson / **Michael Campo**, with FY2022 not issued until 2025.

---

# ADDENDUM 3 — proven by the Feb–Apr 2023 wave (2023 agents: read this)

## Corrections and confirmations to Addendum 2

- **Petrin as Era 0 chair is now PROVEN, not inferred.** The 2/15/23 meeting contains a full
  roll-call vote read aloud (show 14909, segs 458–472): Whitney No, Stephen No, Miles Yes,
  Sprague Yes, Skillen Yes, "and myself / Mike / Patron" Yes — 4 to 2. That names all six
  Era 0 members and puts Petrin in the chair in his own voice.
- **The SAU 6 chair in Feb 2023 is MARJORIE ERICKSON (Unity).** She had chaired for the
  prior year. Established four ways at the 2/16/23 meeting, the cleanest being a roll-call
  residual: she reads the roll naming every member except herself and answers "Me? Yes."
  Horsky then beats her **6–5 on 3/30/23 by PAPER BALLOT** — so individual votes are not on
  the record — with **Rocco Ruggeri elected vice chair** by unanimous voice vote the same
  night. Do not put Hawkins in the SAU chair before late 2023.
- **Ben Nester is the board's de facto secretary in Era 0–3.** With the clerk seat vacant,
  the chair asks him to call the roll ("Ben, can I have you do it tonight?", "Pretend I'm
  Ben"). A voice reading the roll in 2023 is usually Nester, sometimes Seaman, sometimes
  Tempesta — never a clerk.
- **The superintendent presides over the board's officer election.** At 4/5/23 Tempesta runs
  segments 0–17 and hands the gavel to Whitney at 021. Expect the same shape at the March
  2024 organizational meeting.
- **Whitney elected chair and Sprague vice chair on 4/5/23**, both unanimous voice votes, no
  counts. Sprague nominated Whitney; Skillen nominated Sprague; Miles seconded.
- **Bonnie Miles is an elimination-only call in almost every 2023 meeting** — nobody names
  her. Three separate agents reached her the same way and all flagged it. Keep flagging it;
  do not let repetition harden into confidence.

## Staff and administrators actually heard in early 2023

**Michael Tempesta** superintendent · **Mike Koski** assistant superintendent · **Richard
Seaman** business administrator (titled Asst. Supt. for Finance & Operations) · **Ben
Nester** Director of Special Education · **Stephanie Hurst** SAU 6 **Curriculum Director**
(only "Stephanie" is ever spoken; the surname comes from a 4/2/25 CSV where Whitney recalls
"Stephanie Hurst… we lost her within a year" — medium confidence, and she is the predecessor
of Kat McLaughlin, Aug 2023) · **Angela Vivian** appointed **HR Director at the 2/16/23 SAU
meeting**, on a vote that was **not unanimous — one No** · **Jeff Small** Director of
Technology, with **Jason Bonneville** already "my right hand man" in 2023 · **Alex Herzog**
SRVRTC director and chair of the Tech Center Visioning Committee · **Matt Upton** board
attorney · **Michael Campo** / Plodzik & Sanderson the auditors — and the "Mike Campbell"
garble already exists in 2023, so it is not a 2026 artifact.

**Principals, earlier than Addendum 2 had them:** **Chris Pratt** Stevens · **Frank Romeo**
CMS **from at least 2/1/23** (Addendum 2 said "2024-25 only" — that was wrong) · **Melissa
Lewis** Disnard from at least 2/1/23 · **Christine Baker** Bluff from at least 2/1/23 ·
**Christina Sanford** preschool/early-childhood coordinator · **Sean LaPlante** CMS athletic
director. **Hannah Petrin** is the 2023 student representative and the chair's daughter.

**The Seaman succession as the recording gives it:** the 3/30/23 SAU meeting has Tempesta
reading the letter verbatim — retiring "as I am soon to reach age 65", **effective April
14th**, offering to stay on contract to help his replacement. **David Jack** starts the
following Monday (4/3/23) and overlaps him for a week; Jack came from Fall Mountain, "35, 40
years experience". **MRI is named only at the 4/5/23 board meeting, not at the SAU meeting,
and Mary Henry is not mentioned anywhere in this window.**

## The 2/8/23 deliberative session: the moderator is NEVER NAMED
Female, addressed once as "Madam Moderator", presides over her own seat being on the 3/14/23
ballot. **Tracy Pope is elected moderator at that election — after this meeting — so do not
equate them.** The 41–27 amendment result is also NOT on the recording: ~22 minutes of
balloting and counting came through as untranscribed crosstalk and the announcement never
appears. The recording supports only that the amendment went to a secret ballot.

## Recurring public voices in 2023 (nearly all self-identify by name and ward)
Candace Crawford (W2 — **a citizen until 7/19/23**) · Arlene Hawkins (W3, 592 Redwater Brook
Rd — a citizen until the March election) · Nicholas Stone (W3, 2023 candidate) · Jennifer
Gallagher (W1, candidate then member) · Mimi Rhines (W1, Stevens HS counselor) · Matt Bean
(W1) · Michelle Beaton (W2) · Gary Merchant (W2, NH state rep) · Marian/Mary Ann Lovett (W2,
SHS '17) · Ann Fine (W2, 101 Ledgewood Rd, retired Landmark College professor — spelling
unverified) · Laura Snelling (W3, Maple Ave nurse) · Cassandra Edwards (W3, Disnard teacher)
· David Putnam (W2) · Scott Pope (W2, retired tech-center teacher) · Lisa Holtz · Jennifer
Austin · Jenna Gage · Molly DeLuca · Raquel (Maple Ave PTO president, surname never spoken) ·
**Hope Damon** (NH state rep — she is in this corpus from Feb 2023, three years earlier than
the 2026 note suggests) · John Wadsworth (W2) · **Andy** of the Visioning Committee, rendered
`Andy Bernier` on 2/8/23 and `Andy LaFrance` on 12/1/23 — unreconciled, do not pick.

## Unity side of the SAU 6 board, confirmed from roll calls
**Marjorie Erickson** (Unity board chair), **Rocco Ruggeri**, **Shannon Popescu**, **Kelly
Simpson**, **Atonya "Tanya" Hart**. The public-records research could not place Simpson or
Hart in this window; the roll calls do. Cite the roll call when you rely on them.

## New ASR garbles from this wave (heard = actual)
`Frank. Strange.` / `Greg` = Sprague · `Mr. Horton` / `Stephen Hausman` / `Mr. Horse Keeper`
/ `Even asking` = Horsky · `Mr. Dempster` = Tempesta (**dangerous — it sounds like a real
surname**) · `As Kennedy said earlier` = "as Candace said earlier" (**Kennedy is a 2025–26
name that must not leak into 2023**) · `Marjorie. Harrison` = Erickson · `LaTanya` / `Tommy
Hart` = Atonya Hart · `Gary` (in a roll call) = Ruggeri · `Rothko` = Rocco · `Whitney still
here` / `You still here?` = "Whitney Skillen here" · `Skillet` / `Skilling` / `Miss Gillan` =
Skillen · `Assistant Superintendent Simmons` = Seaman · `David Jackson` = David Jack ·
`Mr. Nestor` = Nester · `my Kosky` / `Kosky kosky to skis` = Koski · `Mr. Plant` = LaPlante ·
`Meeting your eyes` / `Mimi Ryan's` = Mimi Rhines · `Michelle, be in Ward two` / `Michelle
beaten` = Michelle Beaton · `Next on Ward three` = Nick Stone · `Matt being` = Matt Bean ·
`Nathan Ward, please` = **"name and ward, please"** (the podium prompt — NOT a person) ·
`our Cosby people` = "our cost per pupil" (**not Koski**) · `Icon Belt lawsuit` / `Con Valley`
= ConVal · `Nick` (as a firm) = Plodzik & Sanderson · `lows` / `letters of government` = LOAs
· `Esther is going to write out` = ESSER is going to run out · `the tune I did program` /
`teacher knighted` = Teach United · `Whitten Wisdom` = Wit & Wisdom · `Hattie John, Hattie` =
John Hattie · `pears` / `Paris` / `special Ed Perez` = paras · `type one teachers` = Title I ·
`Mascoma` heard as `mascot` / `Macedonia` / `Manitoba` / `Gomer` · `Disney` / `Dinard` /
`Dessner` / `this nard` = Disnard · `Luft` = Bluff · `the Wind blows` = WIN block ·
`delivered session` = deliberative session · `Mike Campbell` = **Michael Campo**.

## Two method notes worth carrying
1. **The duplicate 2/1/23 pair is two runs of the SAME stack, not two systems.** Their errors
   are correlated — both produce "Nathan Ward", "Macedonia", the same isolated administrator
   cluster and the same Miles clustering. **Agreement between them is weak corroboration;
   DISAGREEMENT is the strong signal.** The 2/1 agents resolved every disagreement on
   content, never by vote. Apply the same logic anywhere two records of one meeting exist.
2. **`rollcall_evidence_2023_2024.md` reported "(none matched)" for the 2/16/23 SAU meeting's
   self-IDs and direct addresses — and that was WRONG.** That file is dense with both. The
   evidence file is a fast start, not a substitute for reading the working transcript.

---

# ADDENDUM 4 — proven by the Aug–Oct 2023 wave

## Roster corrections that matter downstream
- **Kat McLaughlin is the curriculum director, confirmed from primary audio.** Tempesta, 8/2/23:
  "**Kat Lynn, who goes by Kat McLaughlin**, has come to be our curriculum director… most
  recently in Cornwall on a two year stint… also did some work in Hinsdale," started "just
  yesterday" (~8/1/23). She is Stephanie Hurst's successor. Her full first name is unresolved
  ("Kat Lynn" is the ASR). She rarely speaks — she is named in the 8/17, 9/20 and 10/18
  recordings but has no cluster of her own in any of them.
- **David Irwin is CMS assistant principal from at least Aug 2023** — self-IDs 8/16/23 and is
  on that night's nomination list. Addendum 2's "2024-25 only" was wrong.
- **Courtney Steele** — CMS administrator, "going into my 14th year" as of 8/16/23; runs VLACS
  registrations. Presents the CMS handbook when Romeo is out.
- **Andy chairs the SRVRTC Visioning Committee by 9/6/23** (self-ID), having been vice chair in
  April. Alex Herzog moved to administrative support. **Andy's surname is still never spoken**
  — `Bernier` (2/8/23) vs `LaFrance` (12/1/23) remains unreconciled.
- **Bonnie Miles is NO LONGER elimination-only everywhere.** She is named outright on 8/9
  (three ways, including answering a conflict-of-interest point about herself as a realtor),
  on 8/16 (chair: "[it] was made by Bonnie") and on 9/20 (chair: "We'll start with Bonnie").
  Where a meeting does name her, say so; where it doesn't, keep flagging the elimination.

## Attendance is unusually volatile in this stretch — check it, never assume seven
8/2 **Skillen absent** (on vacation). 8/9 all seven present. 8/16 **Sprague AND Crawford
apparently absent** — only four members answer any roll, a bare quorum. 9/6 **Sprague opens
as vice chair and hands the gavel to Whitney partway through**; no student rep exists yet for
2023-24. 9/20 **Whitney AND Skillen both absent, Sprague presides**. 10/18 **Gallagher absent
and there is NO ROLL CALL AT ALL** — the chair just notes "we're fortunate enough to have a
quorum". Tempesta is absent 8/9 and 8/17, and attends 9/6 **by telephone**.

## Subcommittees as read into the record 10/4/23
Budget = **Crawford, Sprague, Whitney** · Capital Improvement = **Skillen, Crawford, Miles** ·
SRVRTC/alternative program = **Sprague, Miles, Crawford** · Policy = **Skillen (chair),
Hawkins, Whitney** · Ad hoc disruptive behaviors = **Gallagher (chair) + Nester** · NHSBA
delegate = **Sprague**. (These shift during the year — the 4/19 and 5/3 readings differ. Use
the reading nearest your meeting's date.)

## SAU 6 business settled 8/17/23
**Bonnie Miles elected SAU 6 treasurer**; **Sprague** NHSBA delegate; superintendent-evaluation
subcommittee = **Ruggeri, Hart, Sprague, Skillen**; **David Ryan** hired to facilitate the
evaluation, not to exceed **$5,000**; policy CBI suspended for the cycle; **Tyler/iVisions**
approved at ~$120,000 (ESSER-funded through FY25, ~$28,000/yr after). Attendance that night:
present Hawkins, Ruggeri, Hart, Sprague, Miles, Gallagher, Whitney, Crawford; **absent
Erickson, Popescu, Simpson, Skillen**. Koski gave the superintendent's report in Tempesta's
absence. **Angela Vivian's HR report** ran against the **Luchini & Wilson** organizational
study: district to pay the $48.25 background-check fee, substitute pay above $100/day, buy an
applicant-tracking system. **Exit-interview data: 47 resignations and retirements, only 8
survey respondents** — salary, workload, understaffing.

## Two open questions this wave sharpened but did not close
1. **The Skinner question.** Koski read the 8/16/23 professional-staff nomination list
   verbatim: "**Deborah Skinner, art, Stevens High School**." That is the entire mention —
   nothing ties her to food service, free-and-reduced lunch or PowerSchool. The 6/21 and 7/19
   "Miss Skinner / D Skinner" is *support* staff doing all three. Same surname, different job
   class, no statement connecting them. **Do not merge them.**
2. **Frank Sprague's background is contradicted inside the corpus.** On 8/2/23 he says "**I was
   a guidance counselor**" and "I started an alternative program at Stevens"; the 7/19/23 and
   several 2025–26 files call him "**former principal of Stevens High School**". Both readings
   are in the record. Quote what your meeting says; do not harmonise.

## A spelling that needs a corpus-wide decision
The new business-office accountant appears as **Lori Murray** (8/2), **Lori Maury** / **Lori
Marie** (8/16) and **Lori Morey** (9/20) — and as **Lori Mallory / Lori Morey** in the 2026
files. One person, five spellings. Flag yours; the QA pass will normalise.

## New people from this wave
**Lee Malloy** (lead teacher, alternative program, ex-Impact Academy/GSIL) · **Kristen Lawler**
(pre-K director, hired ~Aug 2023 after the previous director resigned 8/8/23) · **Lydia
Stanaway** (CMS 8th-grade dean, restorative justice) · **Brianna Connell/Canal**
(out-of-district coordinator) · **Megan Fagan** (assistant to the assistant superintendent) ·
**Karen White** (moved from Koski's assistant to payroll) · **Sue Kantara** (HR assistant) ·
**Haley Berlin** (Stevens guidance, with Mimi Rhines) · **Mr. Holt** (Stevens/district
facilities — recurs 8/2, 9/20, 10/4; **no first name anywhere**) · **"Jack"** (retired judge
working with the disruptive-behaviors committee) · **Chelsea** (drafts the minutes, receives
board questions — addressed on the record as "Chelsea, when you watch this, please change…";
surname never spoken, matches Chelsea Weatherford in the 2025 note) · **Heidi Sprague**
(Medicaid specialist — **not related to Frank Sprague**) · **Crystal Simmons** (school resource
officer) · **David Ryan** (evaluation facilitator) · **Dr. Luchini and Dr. Wilson** (SAU
organizational study) · charter school: **Heather Shepherd**, **Kathy/Cathy Pellerin**, **Mandy
Bolton**, **Shauna** — note **"Heather" in charter-school context is Shepherd, not the chair**.

## New ASR garbles (heard = actual)
`Mr. Thompson` **and** `Mr. Dempster` **and** `Mr. Pesto` **and** `Mister Timbuktu` = **Tempesta**
— Thompson and Dempster are the dangerous ones, they read as real surnames · `Miss Hocking` /
`Miss Gilman` / `Miss Guilherme` / `It's Gillen` = Hawkins (first) and **Skillen** (rest) ·
`Is proffered` = "Miss Crawford" · `No candy` = "Now, Candace" · `And is Crawford` = "Candace
Crawford" · `turn the meeting over to heaven` = **"…over to Heather"** · `Frankenstein's for
ice` = **"Frank abstains, four ayes"** · `What are you still in for?` / `with me still here` /
`Let me. Skilling` = "Whitney Skillen here" · `A lot of miles` / `20 miles` / `Bonnie Myles` =
Bonnie Miles · `Craig. Ivan. Whitney.` / `Heather. Wendy.` / `Heather Whitman` = Heather
Whitney · `Mr. Kosugi` = Koski · `Caitlin McLaughlin` / `cat` = Kat McLaughlin · `Laurie Maori`
/ `Lori Marie` = the Lori spelling problem above · `Li` / `Lily Malloy` = Lee Malloy · `Dave
Erwin` = David Irwin · `professor Hughes here` = possibly Popescu in a roll call (unresolved) ·
`yonder` = **Yondr** (phone pouches) · `Navy` / `Navy Ellis` = Naviance · `sRGB` / `SRGB` =
SREB · `New Visions` / `I visions` / `divisions` = iVisions · `Vlachs` / `blacks` / `V lax` =
VLACS · `before the race` = "the raise" · `hyperthermia` = Hypertherm · `Tanev` / `Tanith` /
`chain up` = TANF · `whole harmless` = hold harmless · `the Dre` = DRA · `dough 25` = DOE-25 ·
`DC Wife` = DCYF · `Department of Bad` = Department of Ed.

## Corrections owed to already-shipped files (do NOT fix locally — the QA pass handles them)
- `15193 SAU6071323.mp4.CSV`: its note says the 7/13 chair-election tally is unrecoverable, but
  the Ruggeri rows at 339.3s read "Okay, we got three and Arlene. Two. Three" — a possible
  show-of-hands count the file does not surface. Its roll-reader note also claims no prior SAU
  meeting used the same reader; **5/11/23 had Ben Nester read the roll at the chair's request.**

---

# ADDENDUM 5 — proven by the Nov–Dec 2023 wave

## CORRECTION to Addendum 2, and it is a big one
**"Noelle Kronberg is a 2025 arrival; do not put her in 2023" is WRONG.** She was
introduced by Tempesta and appointed **SAU 6 board clerk on 11/9/2023** ("Noel Kronberg who
has applied… Claremont resident, an educator… across the river in Vermont, has actually
worked in Unity"), then appointed **Claremont School Board clerk on 11/15/2023**, and she
reads the roll at every meeting after that. The related line needs qualifying too: the
**elected** clerk seat drew no candidate in March 2023, but the board **appointed** a clerk in
November. Spelling unsettled on tape — `Noel` vs `Noelle`, `Kronberg` vs `Cronenberg`.
**Before 11/9/23 the roll-reader is Ben Nester (or occasionally Koski, Sprague, Erickson or
Tempesta); from 11/15/23 onward it is Kronberg.**

## The 11/30/23 round-robin — the single most useful segment in the 2023–24 block
Sprague, verbatim, segments [0]–[1]: *"My name is Frank Sprague. I'm the chair of this
committee and vice chair of the Claremont Board. Heather Whitney is on the committee. She's
the chair of the Claremont board. And Candace Crawford is also on the committee… and Mike
Tempesta, superintendent. Mike Kosky, assistant superintendent. Mary Henry, business
administrator. And Ben Nester, who is our special ed director."* Plus Melissa Lewis in the
room, Christine Baker and Mark Blunt online.

**This settles three things at once:** the finance/budget subcommittee is **Crawford, Sprague,
Whitney**; **Sprague CHAIRS it** while remaining board vice chair under chair Whitney; and it
resolves retroactively the open question in the project's backlog note about who chaired the
1/6/25 finance meeting. Sprague's 9/20/23 "That's me" was never a claim to sole membership.
He restates the chairmanship himself on 12/6/23: *"as I'm the chair of that committee… ask me
first."*

**The budget subcommittee was renamed the Finance Committee** by consensus on 11/1/23.

## Student representatives, 2023-24
**Nicole Bouchard and Kylie Plummer**, both Stevens grade 10, seated **11/1/2023**. Addendum
4's "no student rep exists yet" was true only as of 9/6. Plummer is the Newport
tech-center/cosmetology voice; Bouchard the theatre/band one. Hannah Petrin held the role in
the 2022-23 year and does not return.

## Attendance settled for this stretch
11/1 **all seven**. 11/9 SAU: Popescu and Skillen have no roll answer and never speak
(probably absent, not proven). 11/15 **Bonnie Miles absent** (called at six roll calls, never
answers). 12/6 **Heather Whitney absent — in Las Vegas — and Sprague presides** at both the
afternoon finance session and the evening board meeting. 12/7 SAU: Whitney absent, Popescu
absent. **And the 10/18/23 absentee is now pinned: Jennifer Gallagher** — she tells the chair
on 11/1 "I was absent two weeks ago… that was not here" and asks for a minutes correction,
which also means **the 10/18 minutes wrongly recorded her present**. Gallagher is the only
member who answers roll with "**Present**" rather than "Here" — a usable signature.

## The two 12/6/2023 shows are genuinely two meetings
`15452` (finance subcommittee, afternoon, ~89 min) and `15453` (full board, evening, ~35 min)
share **zero n-gram overlap**. Not a 16951/16958-style excerpt pair. Both are complete.

## Tempesta, recorded factually five weeks before the 1/11/24 firing
- **11/9/23:** a member moved to amend the 10/12/23 minutes to record *"the discussion… as to
  why we're not following the superintendent's contract or our approved policy on the topic"*;
  the chair rendered it as *"a discussion about the board vote to suspend the superintendent
  evaluation."* The member: *"It's a little whitewash, but I'll accept it."* Adopted.
- **11/9/23:** **Dr. David Ryan** facilitated, presenting four objectives and key results,
  adopted by voice vote with no count; the evaluation subcommittee met Tempesta and Ryan
  **off-camera immediately after the meeting**. Ryan's worked example on between-meeting
  communication named Hawkins and Tempesta by name.
- **12/7/23:** the chair **added the evaluation-subcommittee update to the agenda at the top**;
  the subcommittee was to meet **12/14 at 5:30**, and *"Mr. Tempesta has agreed to get us a
  spreadsheet outlining his benchmarks and responsibilities with dates and times and a
  timeline."* His contract is treated separately in the budget — **3% per contract while all
  other staff get 3.75%**.
- **The 12/7/23 nonpublic was NOT about Tempesta.** It arose from Mary Henry's own answer
  about an ESSER-funded business-office position ("I can't discuss it publicly"), was entered
  under **RSA 91-A:3 II(b) hiring and II(a) compensation**, and the minutes were sealed **99
  years** — **Hawkins voting NO, Erickson abstaining, and no tally announced**. Record this
  as what it is; do not connect it to the firing.
- **The 10/12/2023 SAU 6 meeting has no transcript in the corpus**, and it is the one whose
  minutes carried the contract/policy dispute.

## Sprague's background now has THREE versions on the record
"I was a guidance counselor" (8/2/23) · "when I was the principal" (11/15/23) · "when I first
started at Stevens, I was the **director of student services**, and that was my job to oversee
special ed and guidance. And I acted as the LEA" (12/6/23). Quote your meeting's version;
**do not harmonise them.**

## Names sharpened
**Steve Holt** — first name now on the record (12/1 and 12/6); **Director of Buildings &
Grounds**, though Sprague fumbles the title live. **Courtney Porter** — district-wide social
worker, housed at Stevens (distinct from Courtney Steele at CMS — do not merge). **Tammy
Morse** — former SAU technology/curriculum-integration employee. **Dr. Bissell, the Orion
Group**. **Yoshi Manale** — Claremont city manager. **Jodi Varney** — probation officer.
**Andy's surname now has a THIRD rendering: `Lafreniere` (11/1)**, alongside `Bernier`
(2/8/23) and `LaFrance` (12/1/23). Still unreconciled — do not pick.

## New ASR garbles (heard = actual)
`Mike pesca` / `Mr. Contessa` / `Mr. Temper` = **Tempesta** — both of the first two read as
real surnames · `Dennis Crawford` = **Candace Crawford** (dangerous) · **`Andy` = "Candy"
(Crawford) on 12/6 — and Andy is a real recurring person in this corpus, so this one can
manufacture a phantom attendee** · `Ronnie Miles` / `Donnie miles` / `Only. Miles.` = Bonnie
Miles · `Or three years.` = **Marjorie Erickson** (reads as a question about a seal duration) ·
`Margaret Erickson` = Erickson · `Billy Simpson` = Kelly Simpson · `Joseph.` = Jennifer
(Gallagher) · `Heather wisdom` / `Craig. Ivan. Whitney.` = Heather Whitney · `Whitney.
Skeleton.` / `Whitney. Scaling.` / `East. Gillen.` = Skillen · `Craig. Sprague.` / `Spring.
Sprague` / `Yes, daddy` / `upon your great Sprague here` = Sprague · `Marlene. Hawkins.` /
`Barley. Hawkins` / `Arlene Hopkins` / `Eileen` = Hawkins · `new Cole` = Nicole (Bouchard) ·
`Alyssa` = **Melissa** (Lewis) · `Jeff Smalley` = Jeff Small · `Mr. Holtz` = Mr. Holt ·
`Richard Sheets` = Richard Seaman · `I excel` / `Excel` = **IXL** (~25×, nothing to do with
spreadsheets) · `Yes. Why` / `yes why yes` = **ESY** (extended school year) · `Kenny Benton` /
`McKinney Bento` = McKinney-Vento · `coda` = COTA · `Legally enjoined agent` = **LEA** (a
speaker's own mis-gloss) · `Fly Academy` / `Sky Academy` = the alt-ed academy · `the canal and
the rand` = **ConVal and Rand** · `shrub process` / `sRGB` = SREB · `SSL with an a` = **ESSA** ·
`screen ager` = Screenagers · `Swat protocol` = SWOT · `Hermon` / `Harm in` = "harm in" (reads
as a proper noun) · **`And Sprague, a couple other ancillary responsibilities` = "and perhaps a
couple other ancillary responsibilities" — a spurious "Sprague" at confidence 1.00 that means
no person at all.**

## Corrections owed to already-shipped files — ALL APPLIED, see Addendum 9
- ~~`15336 SchoolBoard100423.mp4.CSV` @ 3680.30 — the curriculum-committee line labelled
  `Unidentified` is **Jennifer Gallagher** (she is the curriculum reporter on 9/20, 10/18 and 11/1).~~ **DONE**
- ~~`15357 SchoolBoard101823.mp4.CSV` — its `Speaker 4` note offers Bonnie Miles as a candidate
  because she is "the only seated member never heard". **Gallagher, not Miles, was the 10/18
  absentee**, so Miles was in the room and that candidate list needs re-weighting.~~ **DONE**

---

# ADDENDUM 6 — proven by the Dec 2023 – Feb 2024 wave

## The 1/11/2024 termination, as the recording actually has it
**The recording begins AFTER the nonpublic session**, on the return to public. There is no
entry into nonpublic on tape, no deliberation, and **no occurrence anywhere in the file of
"RSA", "91-A", "purpose", "reputation", "litigation" or "personnel."**
- **Chair Arlene Hawkins moved the termination herself**, reading it: *"in accordance with
  paragraph nine of the contract… terminate his contract by paying six months severance pay
  and benefits, with the effective date of separation being January 12th, 2024."* **Rocco
  Ruggeri seconded.**
- **Roll: 10 yes – 1 no (Erickson) – 1 abstain (Popescu). NO tally was announced** — the chair
  says only "The motion passes." **No reason was stated by anyone**, and no member spoke to
  the motion at all. Erickson was on the telephone, could not hear, and the motion had to be
  re-read into the handset before she voted.
- **Pratt's appointment followed immediately**, same shape, same 10–1–1, no tally: interim
  superintendent effective 1/12/24, **with the contract terms expressly delegated** to the
  chair and legal counsel. **Pratt is not present and does not speak.** Nothing on the
  recording mentions that he was the Stevens principal.
- **Tempesta is not present and does not speak.** His name occurs twice, both inside the
  motion text.
- Minutes of that night's nonpublic were **sealed 30 years**, again with no announced tally
  and **no RSA 91-A:3 III determination on the record**.

## Charlene Lovett — NOT Tracy Pope — moderated the 2/3/2024 deliberative session
Self-identified at segment [001]: *"My name is Charlene Lovett, and I am the interim
moderator today,"* corroborated by Pratt thanking her. **A name scan for Pope / Tracy /
Tracey / Traci returns ZERO hits in that recording.** So the moderator chain now reads:
2/8/23 never named → **2/3/24 Charlene Lovett, interim** → 2/1/25 Pope → 2/7/26 Pope. Lovett
appears in no project note for this era. (The 2025 note has a Charlene Lovett recorded
elsewhere as Mayor of Claremont, self-identifying as a former school board member — treat
the identification as the same person only if a document supports it.)

## The FY25 budget figures RESOLVE — and the resolution is a real cut
The 2/3/24 deliberative session is internally consistent and matches the published ballot:
general operating **$36,117,407**; Article 2 total **$39,582,407**; general default
**$35,906,774**; Article 2 default total **$39,371,774**; difference **$210,633**. The
arithmetic closes exactly, and $39.58M / $39.37M is what was reported for the March ballot.
- **The 12/20/23 board moved $36,313,407.97 and the 1/17/24 board approved $36,117,406.87** —
  so roughly **$196,000 came out of the budget between those two meetings**. That is a real
  event, not a transcription artifact.
- The 1/3/24 hearing's spoken default "35,960,774" is a **906/960 transposition**; only
  $35,906,774 reconciles. Its lowest-confidence token (0.65) is exactly the garbled one.
- FY24 approved was **$34,880,312**, consistent across recordings.

## The Stephanie Hurst surname is SOLID — and Addendum 3's citation was wrong
Six renderings across four meetings and two speakers, not one. Best anchors: **4/16/25
(Heather Whitney, conf 0.94), in the act of retrieving it — "Stephanie, what was her last
name? First Stephanie Hurst. She was the curriculum director"** — and **12/3/25 (Whitney,
0.92–0.93)**. The 1/5/24 hit everyone was relying on is the **weakest** of the six (`Hurst` at
0.61). Two corrections: the "4/2/25 Whitney" citation is misattributed — 4/2/25 is **Sprague**;
and "we lost her within a year to… Georgia" is in **12/3/25**, not 4/2/25. Ignore the false
positives `Polly Bathurst` (1/17/24) and `Zach Hurst` (2/15/23).

## Corrections to expectations this wave overturned
- **The 12/18/23 finance session was NOT a members-only caucus.** The full administrative team
  attended and held the floor for a third of it; Tempesta and the CMS delegation arrived ~14
  minutes late, Henry ~16 minutes late with unfinished packets. **The caucus itself is not on
  the recording** — the tape stops the moment Sprague says "I think we need to caucus."
- **The 2/15/24 SAU meeting contains NO mention of Unity's withdrawal** — no warrant article,
  no study committee, no separation talk. Do not expect it before it appears.
- **Pratt was still the Stevens principal on 1/17/24** — he reports "as being the principal at
  the high school." So the Herrington changeover is **after 1/17/2024**, which narrows but does
  not close that open question.
- **The clerk reads the roll only sometimes.** Hawkins reads the rolls herself on 12/14/23 and
  on two of the four rolls on 1/11/24. When the chair says "the secretary take a roll call,"
  it is Kronberg; otherwise check.

## Names and facts added
**Charlene Lovett** (interim moderator 2/3/24) · **Rick Elliott** — Stevens instructional
coach, Stevens '92, **a named student plaintiff in the Claremont education-funding lawsuit**,
ESSER-funded · **Miss Foster** — CMS staff who built the proposed master schedule (13th year;
**do not merge with Courtney Steele**, who told the board on 8/16/23 she was in her 14th) · **a
SECOND Courtney** — the middle-school instructional coach, distinct from Courtney Porter
(Stevens social worker) and Courtney Steele (CMS administrator); three Courtneys now ·
**Carolyn Cole** — former board member who started capital planning · **Dale Girard** — Mayor
of Claremont · **Rebecca Duska** — CMS 6th-grade science teacher, Ward 1 (**this supplies the
surname `15483 SchoolBoard122023.mp4.CSV` records as "surname never spoken"**) · **Polly
Bathurst** (classroom-management consultant) · **Derek Staves** (math PD) · **"Sean" of the
school district attorneys** (2/3/24, no surname — between Matt Upton and O'Shaughnessy) ·
**Elaine Arbor**, **Ray Curran**, **Paige McClay**, **Jeff Beard**, **Lee Kassian**.
- **Ben Nester resigned** — announced 12/14/23, to Lebanon as director of student services,
  effective July 2024, after nine years.
- **Heather Whitney is a nurse** — "if you're a staff nurse and you work on the floor, you get
  paid less than… the intensive care unit."
- **Whitney asked for a forensic audit in December 2023** and Mary Henry declined it — *"I
  don't feel there's any reason for a forensic audit… a forensic audit is not cheap."* That
  predates the 2026 forensic audit and the Bernstein Shur retention by more than two years.
- **The $688,426.17 "board voted expense reduction"** traces to **David Jack (MRI)** and the
  deliberative-session $1,000,000 restoration; Henry redistributed it and could not account
  for ~$16,830 of it.
- **Sprague's background now has FIVE-plus versions on the record** — guidance counselor
  (8/2/23), principal (11/15/23, 12/18/23), director of student services (12/6/23), "when I was
  working for the district" (1/5/24), and Newport in the early 90s (12/13/23). Quote yours.

## Anchors that keep working
**The SAU 6 roll order is confirmed a fourth time and is stable**: Hawkins, Ruggeri, Erickson,
Popescu, Simpson, Hart, Sprague, Miles, Skillen, Crawford, Gallagher, Whitney. It is the most
reliable tool in the corpus for naming a vote whose names the ASR ate. **Gallagher's roll
answer is "Present" where everyone else says "Here"** — still a usable signature.

## New ASR garbles (heard = actual)
`Syria` / `the SRE` / `SRA` = **SREA** (Syria arrives at confidence 1.00) · `dessert` /
`Dessner` / `Denard` / `Dinard` / `Disney` = **Disnard** — four spellings in one file ·
`Kansas is last this here` = **"Candace, as I said…"** · `to friends point` = "to Frank's
point" · `Dave, Jack and I` = **"Dave Jack and I"** — the comma invents a second person ·
`Frank speaking` / `I see those same way. Frank.` = **"frankly speaking"** — a spurious
self-name at conf 0.97 · `Nestor. Gallagher.` = "Jennifer Gallagher" (dangerous with Nester in
the room) · `Shannon, you.` = Shannon Popescu · `Tanya. Hurt.` / `It's on your heart.` =
Atonya Hart · `Rocco. Jerry.` / `Afterwards` / `Rock over. Garrett.` = Rocco Ruggeri ·
`Marjorie Rhodes` / `Andre. Erickson.` / `Or three years.` = Marjorie Erickson · `You are
Lane.` / `Our lane.` / `Eileen` = **Arlene** · `Candice. Proper.` / `Candice. Parker.` /
`Is proffered` = Candace Crawford · `challenge for` = **Charlene** (Lovett) · `Gary Martin for
two` = "Gary Merchant, Ward Two" · `Frank's great work to` = "Frank Sprague, Ward Two" ·
`We feel the minutes` = "we **seal** the minutes" · `an Charo` = **an SRO** · `Swiss data` =
SWIS · `sweat tax` = **SWEPT** · `our audience` = **our auditors** · `Christine Nuno` = Chris
Sununu · `Fill Scott` = Phil Scott · `academic deeds` = academic **deans** · `Tardis` =
tardies · **`Mr. Dean, how are you today?` names no one** · **`Another Mr. Costa to chime in`
is not a surname** · **`The time of art is a chair` may be "Atonya Hart is the chair" — three
such near-misses in one file, none decisive; do not manufacture a name from them.**

## Corrections owed to shipped files — ALL APPLIED, see Addendum 9
- ~~**Clerk spelling split: 28 CSVs use `Noelle Kronberg`, `15455` and `15523` use `Noel
  Kronberg`.** One spelling should win corpus-wide.~~ **DONE — `Noelle Kronberg` corpus-wide.**
- ~~`15483 SchoolBoard122023.mp4.CSV` — its Speaker 10 "Rebecca, surname never spoken" is
  **Rebecca Duska** (named by Bonnie Miles on 1/3/24 at conf 1.00/0.97).~~ **DONE**
- `15455 SAU6120723.mp4.CSV` — its note that Kronberg read all four rolls is right for that
  night but should not be read as general; Hawkins reads them herself on 12/14/23 and 1/11/24.

---

# ADDENDUM 7 — proven by the Feb–Jun 2024 wave (2024 agents: read this)

## The 3/20/2024 organizational meeting — the 2024 reference
**Chris Pratt, interim superintendent, presided** over the officer election and physically
handed over the gavel ("Here's your gavel"). **Heather Whitney re-elected chair** (nominated by
Sprague); **Frank Sprague re-elected vice chair** (nominated by Crawford, seconded by Whitney).
Both **voice votes with no count**. Crawford later calls it "our unanimous vote tonight."

**Subcommittees as read into the record — use this list for the rest of 2024:**
NHSBA delegate **Sprague** · Capital Improvement **Miles chair**, Sprague, Crawford (**Skillen
steps off**) · Finance **Sprague chair**, Crawford, Whitney · Policy **Skillen chair**, Hawkins,
**Petrin** (new) · Curriculum rep **Hawkins** · SRVRTC Visioning Miles, Crawford, **Petrin**
(**Sprague steps down**). All by "no objection," no votes.
> Later readings drift — the 5/15/24 recording gives Capital Improvements as Whitney + Sprague
> + Crawford. Use the reading nearest your meeting's date and say which you used.

**Petrin is a member again from 3/20/24** ("So I'm new we're back again"). **Gallagher is gone.**

## A signature that CHANGED — do not carry it forward
Gallagher was the only member who answered roll "**Present**" rather than "Here." After
3/12/24 **that answer is Heather Whitney's**. Two later files record a "Present" answer; it is
not Gallagher. Retire the tell for anything after the March 2024 election.

## The Skillen garble family, proven in one paragraph
The 3/20/24 subcommittee reading contains, within 40 seconds: `Miss Gillen` (0.59),
`Miss Whitney Scullin` (**0.94**), `Miss Whitney Gillan` (0.56), plus `Beneath. Skilling.`
(0.89) in the roll — all one woman, **Whitney Skillen**. **`Scullin` at 0.94 is the warning:
high ASR confidence is no protection on these names.**

## Dates that CLOSE or narrow open questions
- **Patrick O'Hearn started Monday 4/15/2024** — Pratt: "our new director of human resources.
  He started with us on Monday." Addendum 2's "around April 2024" is now exact.
- **Michael McCosker approved as Director of Student Services effective 7/1/2024**, at the
  4/11/24 SAU meeting.
- **Stevens principal — the window is now 1/17/24 → 3/6/24.** On 3/6/24 Pratt defers to "the
  principal" and an otherwise-unheard voice answers from a Stevens staff meeting — a principal
  who is not Pratt, unnamed. By 4/17/24 "Doctor Harrington" is in the leadership circuit; by
  5/15/24 he has authority over the Stevens advisory block; **by 6/20/24 he is unambiguously
  "Doctor Michael Harrington," presenting to the board remotely.** No acting principal is ever
  named.
- **Pratt's permanent appointment is not on any recording in this wave.** He is "interim" on
  2/21 and 3/20; on 5/15 he says "as your former principal and now the superintendent"; on
  6/5 and 6/20 the word *interim* does not occur at all and he speaks of the principalship in
  the past tense. The ~22–23 May 2024 dating stands, unwitnessed.
- **Ben Nester's last meeting was 6/20/24.** Pratt and the chair give farewells; **no successor,
  no handover and no mention of McCosker** in that recording.
- **Alex Herzog is leaving SRVRTC** — farewells on 6/5 and again on 6/20 ("we wish you the best
  of luck"), though no departure is ever stated outright.

## SAU 6 reorganization, 4/11/2024
**Pratt presided.** **Arlene Hawkins re-elected chair** and **Rocco Ruggeri vice chair — both
voice votes with NO tally, no ballot, no roll.** (Weaker on the record than 2023's 6–5 paper
ballot.) **No treasurer, no signatories, no NHSBA delegate, and no audit item at all** — so the
2025 pattern of burying officer votes inside the audit item does not apply here. Subcommittees:
superintendent evaluation = Hart, Ruggeri, Sprague, Skillen, **chair Sprague**; policy =
Crawford, Simpson, Hawkins, **chair Hawkins**. **Clerk Kronberg was absent; Ben Nester read all
four rolls** — the pre-11/15/23 pattern resurfacing. **Roll order stable a fifth time, with
Petrin now in Gallagher's old slot.** No tally was announced for ANY vote that night.

## Unity's withdrawal — first appearance, 4/11/2024, and three corrections
Ruggeri: the Unity town vote of **"March 16th"** approved creating a planning committee. **The
committee is 5 town members + 2 board members + the superintendent = EIGHT**, not the seven the
project note carries — and **no chair is named on the recording**; Ruggeri delivers the report
but never says he chairs it. "Nothing is guaranteed… for the next year, it's just the planning
committee and the planning committee's findings."
**The 2/15/24 SAU meeting contains no mention of any of it.**

## Names added or sharpened
**Mark Blount is already Maple Ave principal on 3/20/24** (earlier than any note had him) ·
**Michelle Herrington is Bluff Elementary's guidance counselor** before her Aug 2024 SRVRTC move
· **Sean Herzog** — Title I teacher at Maple Ave, **not** Alex Herzog · **Tessa Nicholson
Powers** — Director, District Management Group (SAU 6's first strategic plan; ESSER-funded) ·
**John Kim** — DMG founder · **Dr. Dale Winkler** — Senior VP, SREB · **Susan Mason** — citizen
who raised a teacher-conduct complaint at the 4/11/24 SAU meeting · **Ms. Chastain** — Stevens
social studies, Youth & Government advisor · **Aubrey Herzog** — Stevens junior, **NH Youth
Governor-elect 2024-25** · **Gage Moran** — Stevens senior · **Kip Ryan / What's Up Claremont**
— local channel that reposts district documents · **Mike Landau** — former Stevens English
teacher · **Charlene Lovett** headed a **city** lead committee (3/20/24) · **RJ** — Maple Ave
custodian · **Lori Morey** — another spelling of the business-office "Lori" (now: Murray, Maury,
Marie, Morey, Mallory).
**Andy's surname now has a FOURTH rendering: `Andre Lafont` (5/15/24)** — with Bernier
(2/8/23), LaFrance (12/1/23 and 4/17/24) and Lafreniere (11/1/23). Still unreconciled.

## New ASR garbles — several are dangerous
`Bromberg` (**conf 1.00**) = **Kronberg** · `Michael Coffee` = **Koski**; also `Mr. Costa`
(0.56) = Koski **in the 6/5/24 file**, though "Another Mr. Costa to chime in" on 1/17/24 named
nobody — context decides · `Bonnie Myers` = **Bonnie Miles** · `Michael Keaton` (0.85) /
`Michael. Peter.` / `Mr. Peterson` / `Mike. Patron.` = **Petrin** · **`Sussex` (conf 1.00) =
SAU 6** — reads as a real place · **`the Claremont Middle School. Campbell.` (conf 1.00) =
"…Middle School handbook"** — a spurious "Campbell" at full confidence, next door to the
Campo/"Mike Campbell" problem; **it names no one** · `Riley Hawkins` / `Eileen Hopkins` /
`Carly` / `Marlene` = **Arlene Hawkins** · `Beneath. Skilling.` / `Scullin` / `Gillam` /
`Wendy` = **Whitney Skillen** · `Frank's Greg` / `Craig Sprague` = Sprague · `Mr. Craft` =
Pratt · `Catlin` = **Kat McLaughlin** · `Miss David` = **Miss Damon** · `Doctor Harrington` /
`Doctor Herren` = **Herrington** · `Michael McCusker` = **McCosker** · `Rocco Gerry` / `Rocky
times` / `rock over here` = **Ruggeri** · `Shannon. Perpetuo.` = **Popescu** · `Tony. Hawk.` /
`Fine art.` = **Atonya Hart** · `Excel` = **IXL** (confirmed repeatedly; never a spreadsheet) ·
`the quantities` = **Kiwanis** · `polymath is at our school` = "**Polly Bathurst** is at our
school" · `Dibble dribble` / `the dribble poll` = **Doodle poll** · `kneecap` = NECAP ·
`sRGB` / `Ezra` / `Shri` / `the shrub report` = **SREB** · `I opposed graduations` = "opposed?
**abstentions**" · `nominations for Voyager` = "nominations for **the chair**" ·
**`So, Donald, we'd like to have a rollback` (conf 1.00) = "so down the line" — names no one** ·
**`just like Mr. Foster said`, `Mr. governor`, `Charlie`, `Mr. Broughton` (0.56) and `Barrett`
all look like surnames and none of them resolves to a person in the room — do not mint people
from them.**

## Standing caution this wave reinforced
**Bonnie Miles remains elimination-only in several files** (2/21, 4/11 SAU, 5/15) even while
being named outright in others (3/6, 4/17, 6/5, 6/20). Check per meeting; never inherit.

---

## Addendum 8 — Aug–Nov 2024 wave (15947, 15994, 16011, 16021, 16046, 16049, 16070, 16142)

Eight files, all passing both scripts. This wave closed several questions Addendum 7 left open and opened one large new one (the City Council).

### Roster, settled

**Pratt's permanent superintendency is now dated and witnessed.** Addendum 7 recorded it as "unwitnessed, ~22–23 May 2024." Three independent confirmations landed:
- 8/21/24 (15947), on tape, two members speaking to his face: Petrin — *"Chris was the acting superintendent because someone left mid-term… he was filling in that role"*; Miles — *"Mr. Pratt was an interim superintendent **before you became** the superintendent."* The word *interim* is never used in the present tense after this point.
- 9/12/24 (16011), Hawkins announcing formally: *"the appointment of Superintendent Christopher Pratt as superintendent of [SAU] six, which was **effective in June**."*
- **Settled reading: announced ~22–23 May 2024, effective June 2024, formally recognised by the SAU 6 board 9/12/24.** Call him "Superintendent," never "interim," for anything after May 2024.

**Alex Herzog is gone — Addendum 7's open question closes.** 8/21/24: Pratt funds a new post *"for less than we're currently paying Doctor Herzog"* and from *"the money that we saved based on Alex's salary."* By 9/30/24 Manale says Michelle Herrington *"recently succeeded Alex Herzog at the Tech Center."*

**Michelle Herrington — title is genuinely unstable on the record, and that is a finding, not an error.** She started **end of August 2024** (her own words, 10/16/24; Crawford dates it "about September 1st"). Across seven weeks the same body calls her three different things:
- 9/4/24 — the board votes to strike "acting" from the **Assistant** Director title.
- 9/18/24 — Crawford: *"the new, director, actor [acting] director at the tech center… she's been on the job for 17 days."*
- 9/30/24 — Manale and Crawford both say **director**; Manale says she succeeded Herzog.
- 10/2/24 — Crawford says **"the director."**
- 10/16/24 — the chair introduces her as *"our new **assistant** director of the technical center,"* and she self-IDs as Miss Harrington.
- 11/19/24 (per Addendum 7's neighbour file) she introduces herself as **assistant** director.
**Do not normalise this.** Record each as spoken and note the conflict. The board's formal action was on "Assistant Director"; colloquial usage ran ahead of it.

**Two Herringtons overlap from Aug 2024 onward** — Addendum 2's warning is now live in single files. `Michelle Harrington` = **Michelle Herrington** (SRVRTC); `Doctor Harrington` / `Michael` = **Dr. Michael Herrington** (Stevens principal). 16021 and 16070 each contain both. Never merge on surname.

**Michael McCosker is nearly absent from the 2024 board record.** Named nowhere in 15947, 15814, 15994, 16011 or 16021. He *does* appear at the 9/30/24 joint meeting (16046), introduced by the chair as "our Director of Student Services" and corroborated twice. Do not assume he attends Claremont board meetings in 2024; do not attribute unnamed administrator voices to him by default.

**Subcommittee assignments moved between March and September 2024 — use the September reading.** Capital Improvements passed from **Miles to Crawford** (Crawford is called for that report on 9/18 and states the chairship herself on 9/30). As read 9/30/24: Crawford — chair, Capital Improvements + chair, SRVRTC Visioning, + Finance; Sprague — chair, Finance + superintendent evaluation; Skillen — chair, Policy + superintendent evaluation; Hawkins — Curriculum + Policy (+ SAU 6 chair); Petrin — chair, ad hoc Communications + Tech Center; Miles — Capital Improvements + Tech Center; Whitney — Finance. SRVRTC Visioning membership = Crawford, Miles, Petrin.

**Clerk attendance is erratic through autumn 2024 — check it every file, never assume.** Kronberg read the roll 9/4 and 10/16 ("Miss Kronborg", conf 0.62) and 9/12 (SAU, from the minutes). She was **absent** 8/21 (chair read it herself, *"in the absence of our secretary"*), 9/18 (Crawford read it at the chair's request), and 11/14 (**Pratt** read all four rolls — *"Miss Cronenberg is not here tonight"*). The pre-11/15/23 pattern of substitutes has fully resurfaced.

**Attendance findings worth carrying:** Whitney **absent** 9/18/24 (Sprague presided as vice chair). Skillen and Sprague **absent** 9/30/24 (the chair says so outright). Miles **absent** 10/16/24 (2 s silence at her name + Crawford confirms). Pratt **absent** 10/2/24 — no superintendent's report and the LED item was struck.

### The 9/30/24 joint session (16046) — a different problem

The first joint School Board / City Council meeting "in several years." **Only three council-side people are defensibly named: Mayor Dale Girard, City Manager Yoshi Manale, and Councilor Limoges/Lemos** (spelling unsettled). Five further council voices are characterised but unnamed.

**Do not mine the chair's attendance list at segment 6 for names.** She reads a sheet she did not have from the clerk, stumbling audibly, and the word timings show "Mr. William green. Rose. I think she's" is one unbroken run — it is not parseable into clean names, and several surnames sit at 0.56 confidence. There was **no council roll call and no councilor ever answered to a name.** Treating that list as an attendance record would manufacture people. This is the Addendum 7 rule at its sharpest: in a room full of surnames the corpus has never heard, an uncorroborated name is a garble until proven otherwise.

**Consequence for the corpus:** `16046` carries a 16.9 % Unidentified rate against the 8–10 % norm, and that is the correct outcome, not a defect. Roughly half of it is `Unidentified City Councilor` — body and role established, name not.

### Diarizer behaviour — two repeatable patterns

1. **This diarizer splits Heather Whitney into two temporally disjoint clusters at SAU 6 meetings.** Seen at 4/11/24 and again at 9/12/24 (Speaker 3 ends 2579.6 s, Speaker 11 starts 2770.8 s, zero overlap). Expect it; check for it before concluding two women spoke.
2. **The chair's cluster is inherited by whoever is silent early.** At 10/2/24, Whitney occupied Speaker 2 to 1471 s, moved to Speaker 7, and **Arlene Hawkins — silent for the first 25 minutes — fell into the cluster Whitney vacated.** A single cluster spanning a meeting is not a single person.

### The Miles/Hawkins merge is this era's hardest problem

The diarizer merges **Bonnie Miles and Arlene Hawkins** repeatedly (48 segments in 16021, 106 in 15947, 7 rows in 16046). Their anchored blocks *interleave*, so no temporal or topical cut works. Where a chair recognition does not separate them, leave the row `Unidentified` with both candidates in the Role. Two seated women is a coin flip, and a coin flip is exactly what the second hard rule forbids.

### Facts a later session will want

- **ESSER ended 9/30/2024.** Henry owed the board an ESSER wrap-up report in October listing which positions survive in the operating budget. Summer school loses its ESSER staffing after FY25 and must move into the Stevens budget.
- **FY25 fund-balance retention, decided 10/16/24:** fund balance $497,000 + $114,000 additional revenue = $611,000 surplus; statutory max retention **$466,664.43** (but everyone in the room, Henry included, then says "469" — the inconsistency is inside one meeting); break-even $234,403. **Sprague moved to retain up to $350,000 conditioned on offsetting the FY2025-26 tax rate; Petrin seconded; voice vote, no count.** Tax rate $14.15 → $14.46.
- **FY24 close (9/18/24, Henry):** $544,145.29 surplus; encumbrance cut to $65,000 after the roof PO rolled ($648,000 of it was roofs); ~$205–210,000 extra revenue from the special-ed age extension 21→22. Stevens roof "a little under 600,000", $400,000 from reserves.
- **Audit backlog still live in Nov 2024:** FY21 nearly done, FY22/FY23 targeted before 6/30/2025, FY24 unpromised; Henry reconciled cash back to 2020 and meets the auditor weekly. At SAU 6, three years still unaudited.
- **The auditor is only ever "Mike" on these recordings.** The corpus canon is Michael Campo / Plodzik & Sanderson — **do not import the surname or the firm into files that do not speak them.**
- **Governance flag, 8/21/24:** Pratt hired the Assistant Tech Center Director **before the board approved the position** (Miles: *"we've already hired someone for a position that we have not approved"*; Pratt: *"this is a time sensitive thing, and I had to make the decision"*) — a prior meeting had failed for want of a quorum. He apologises on the record.
- **Exit-interview data (9/18/24):** ~40 departures FY24, 16 survey responses, ~15 interviews. Sprague reads one aloud: *"I was burnt out only after one year. Unnecessary stress from certain board members."*
- **Citizens' comment, 10/16/24:** Jen Gallagher (Ward 1, former board member speaking as a parent) reports a fecal-smearing incident in an elementary girls' bathroom, girls pulled from academics and **lined up to view the stall one by one**. No board response on tape. Substantive public-record item.
- **Claremont Administrators Association opened bargaining** — written request received **October 1, 2024**; **Arlene Hawkins named the board's negotiator** with Pratt, by consent, no vote.
- **The Nov 26 professional-development day was cancelled and given to staff as a day off** — by consent, no vote.
- **Unity withdrawal, as of 11/14/24 (Ruggeri):** planning committee met **9/26/24**, concluded in favour; report to the state **~10/8/24**; state board reviewed it **11/14/24**; report goes to the town for a **March 2025 vote**; **if approved, Unity remains in SAU 6 until July 1, 2026** — the earliest in-corpus statement of that date. Still **no planning-committee chair named**. Unity contributes **7.8 %** of SAU costs (~$193,000), down from ~9.6–9.8 % because Claremont's revaluation completed first; formula is **50 % assessed value / 50 % student ratio**.
- **The Claremont "exploratory ad hoc subcommittee" report went badly at SAU 6 on 9/12/24.** Ruggeri: *"you suggest that if we want better performance, we need to pay more. And I find that a little insulting… That doesn't mean that you treat us like second class citizens."* Simpson: *"I'm very upset."* Retitled to name Unity withdrawal as its subject.
- **Joint-session money (9/30/24):** out-of-district special ed **~$4,000,000 for ~33 students**; adequacy base **$4,182/pupil**; **hold-harmless guaranteed at 96 % and phasing out 20 % every two years** until the district loses the $1.6M it now receives; catastrophic aid lags a year; revenue mix local 49 % / state ~47 %; **wages and benefits ~72 %**; supplies for the entire $36M budget = **$361,000**.
- **Every vote in this wave was a voice vote with no announced tally, with two exceptions**: the 9/4/24 job-title vote, **3–2**, where the chair read the names into the record (Petrin/Sprague/chair aye; Crawford/Hawkins no, *on the word "acting" only*); and the 8/21/24 title and main motions, where **Petrin was the lone No** (6–1).
- **A decisive external source exists for SAU 6 meetings.** `Input/SupportingDocuments/MAP.md` §1 links draft SAU 6 minutes filed inside the *following* meeting's packet folder. The 9/12/24 draft minutes carry the attendance list and name the mover and seconder of every motion, and every attribution matched the transcript. **For any 2024 SAU 6 file, pull the next meeting's packet minutes before inferring anything.**

### New people
**Mary Henry** self-describes (9/30/24): Fall Mountain school board **2011–2022**, then Fall Mountain BA "for a year", then Claremont — though she also says "I've been in [BA] now for about eight years," which does not reconcile. Quoted as spoken.
**Atonya Hart** — Unity, SAU 6 member (roll: `Tanya. Hot`). **Jamie Young** — City HR Director. **Michael Grace** — city library director. **Nancy Merrill** — city economic development director. **Derek Ferland** — Sullivan County administrator. **Mr. Pascucci** ("Mr. P") — Stevens restorative justice coordinator. **Miles Sheehan and Lily Clark** seated as student board members ~Oct 2024 — the chair calls them "two new student members" on **10/16/24**, earlier than the 2025 note's window. **Tim Weatherford** — summer-school English teacher, **a different person from Chelsea Weatherford**; do not merge. **"Sue"** — Unity Elementary principal, surname never spoken. **"Eric"** — CTE director at Newport, surname never spoken. **Jeff Baird** — NH DOE.

### ASR garbles added this wave — the dangerous ones first

Names that are not people, or are the wrong person, at high confidence:
- **`Arlene Foster` (0.99) = Arlene Hawkins.** Reads as a real public figure.
- **`Arlene Hoffman` (0.99) / `Miss Hoffman` = Arlene Hawkins.** Also `Marlin`, `Early knocking`, `Eileen Hawkins`, and bare **`early` (1.00) = "Arlene."**
- **`head` (1.00) = "Heather."** *"if head is working at her job…"* — reads as a common noun and hides a reference to the chair.
- **`pester` (1.00) = Nester.** Reads as a verb.
- **`Chelsea` (0.61) = "Second"** — dangerous because Chelsea Weatherford is a real person named at 1.00 in the same meeting.
- **`Mr. Putin` (1.00), `Mr. Peterson` (1.00), `Mr. Peters` (1.00), `featuring` (1.00), `Michael. Future.`, `So patrons seconding`** = **Petrin**. The Petrin family now includes an ordinary English word and a head of state.
- **`Ines Crawford` (0.73) = Candace Crawford**; **`Andy` / `Magic` (0.89)** — the phantom-first-name trap again.
- **`Michael Arrington` (0.52) = Michael Herrington.** Reads as a real surname.
- **`Mr. Braxton` (0.82), `Edmond` (0.44), `Mr. Caskey` (0.74), `James prophet here` (0.60–0.94), `My dad Mattos is in there` (≥0.93), `Dave. Jack.`** — **name nobody recoverable. Do not mint people from these.**
- **`the Dow building` / `the Dow office` (both 1.00) = the SAU 6 central office.** Exactly the Addendum 7 trap: full confidence, plausible proper noun, no such place.

Institutional garbles: `Sussex` (1.00) · `saw six` · `SAS six` · `SC six` · `essay you` · `s a you` · `the SA` · `Siu six` · **`Essar six` (0.42 — NOT ESSER)** · `at the issue level` · `departments within six` · `to move six forward` — all **SAU 6**. Also `the SEO office`, `the Sioux office`.

Other: `500 fours` / `Bible fours` / `five or fours` = **504s** · `the Excel` = **IXL** · `Eureka squared` = **Eureka Math²** · `the sweat tax` / `swept` = **SWEPT** · `the dough 25` = **DOE-25**, `miss 25` = **MS-25** · `through primates` = **Primex** · `recompute` (0.78) = **Recompete** · `Fate` = **FAPE** · `admirer` = **ADM** · `Coast County` = **Coös County** · `Microsoft.` (0.42) and `micros` (1.00) = the same unrecoverable local manufacturer · `Adnoc` (1.00) = probably Antioch · `physicians` = **positions** · `the tendency of board members` = **the attendance of** · `taking a local` = "taking a [roll] call" · `do vocal a motion` = "do a roll call [on the] motion" · `Extension(s)` = **abstention(s)** · `it would be a walk` = "a wash" · `Actual spinach here` = "actual spend here" · `included to submit` = "concluded to submit" · `No lies. Have it.` = "the ayes have it" · `Call your favor` = "All in favor" · `I, I posed sentience` = "Aye. Opposed? Abstentions." · `capital of horse` = "cart before the horse" · `Mayor` = **Mary** (Henry) · `77 years` = almost certainly **7 years** (LED payback) · `October 16th, 2021` = **2024** · `19927` = a collision of Claremont I (1993) and II (1997).

### Two corpus-wide normalisations for the QA pass
1. **`Multiple` vs `Multiple speakers`** — 152 rows across 41 files use `Multiple`; 4 rows in 2 files (`14875 SchoolBoard020123`, `15814 SchoolBoard062024`) use `Multiple speakers`. Normalise to `Multiple`.
2. **`rollcall_evidence_2023_2024.md` is unreliable and now provably so.** It reported "(none matched)" for 15947, 16011, 16021, 16142 and others where the transcripts contain a dozen or more usable chair recognitions. Worse, its window stops at segment 79, and in 16070 *every* anchor fell outside it. Use it as a fast start only.

---

## Addendum 9 — Nov–Dec 2024 wave, and the corpus QA pass

Eight files (16155, 16157, 16158, 16192, 16213, 16215, 16222, 16226), all passing both scripts.
**This closes the transcript gap: 127 transcripts, 127 dialogue CSVs, 0 missing.**

### The FY26 budget season, end to end

Four Finance sessions and three board meetings in five weeks. The through-line:

- **11/19/24 (16155)** — the first budget session actually on tape. Sprague opens it with a
  round-robin "for the folks in TV land": these Finance meetings are being televised again.
  **The announced November 12 first public budget meeting either did not happen or was not
  recorded** — nothing in the 11/19 file refers back to a prior session, and every presenter
  treats it as their first pass. Principal-by-principal requests, no motions, no votes.
- **12/13/24 (16215)** — school-by-school walkthrough. Draft totals: Bluff +$400K on $3.5M;
  Maple +$656K on $4.6M; Disnard +$288K on $3.8M; CMS **$4.5M → $6M, a 33 % increase**;
  Stevens **$11M, +~$2M (20 %)**. Out-of-district special ed **$4M at the high school alone**,
  district-wide "under five [million], but probably not much". Whitney's pre-K proposal —
  ~$450K in salaries, ~$50,000 per child, no measured benefit at grades 1–3 — went to the
  administration as a request, **no motion, no vote**.
- **12/18/24 afternoon (16226)** — the committee converges. Budget is over by
  **$1,128,543** after revenues, **up 8.91 %** (11 % with the CBAs). Sprague: *"I'm going to
  throw out 4 %"*; Crawford closes it as **"Just find me 200,000"** ≈ 4.5 % fully loaded;
  Pratt: *"you got our orders."* **Consensus direction, no motion, no vote.**
- **12/18/24 evening (16222)** — and the board does **NOT** move the budget to a dollar
  figure, inverting the 12/20/23 precedent. The chair states why on the record: two
  collective bargaining agreements are unratified, and *"it is we would be breaking ground
  rules… if we discussed what the final dollar amount impact would be."* An **emergency
  meeting is set for January 7** to ratify them and see the budget; the move to the
  deliberative goes to **1/15/25**. The only FY26 figure spoken all night is the
  **default budget, $39,791,261**, which is *higher* than the operating budget.

**Do not look for a December 2024 budget vote. There isn't one.** Anyone tracing the FY26
figure forward must go to the 1/7/25 emergency meeting.

### SAU 6: the December 3 meeting never happened

- **12/3/24 failed for want of a quorum.** Hawkins says so at the Claremont board on 12/4:
  *"we did not have a quorum yesterday and we could not meet… There was illness. There were
  reasons and I understand, but we have legal deadlines we must follow."* She then canvassed
  members individually to guarantee the rescheduled date. Corroborated inside 16213 by Henry:
  *"we had version two and unfortunately we couldn't have a meeting for version two."*
- **12/12/24 (16213) is therefore the budget hearing AND the budget vote**, on version 3.
  **FY26 SAU 6 budget approved at $2,755,723** — Crawford moving, including the
  superintendent's raise, the **$7,000** assistant-superintendent parity adjustment, and
  reinstating the curriculum position (~$150K), *"offset by retained funds so that we end up
  with a SAU budget that is revenue neutral, impact tax rate neutral."*
- **The 2024 SAU 6 no-tally streak finally breaks — barely.** The vote is declared
  *"All those in favor? Aye, aye. **Opposed? One.** And any abstentions."* **One dissent
  counted, no aye count, no names.** That is the only counted dissent in the entire 2024
  SAU 6 set. Every other vote across 9/12, 11/14, 11/21 and 12/12 had no tally at all.
- **The chair asked for the percentage change and never got one.** *"I know what you said by
  numbers, but what about percent?"* — Henry: *"I would have to figure that out because I
  don't know."* The board adopted the budget at a public hearing with no percentage ever
  stated, and **no member of the public attended.**
- **11/21/24 (16158) had no quorum at 6:30 either.** The DMG strategic-plan presentation ran
  *before* the meeting was called to order; a quorum arrived during it and the board was
  gaveled in solely to adopt the plan. The gavel falls 44 minutes into the recording.
  Nothing about Unity, nothing about the budget — a single-item meeting.

### Unity withdrawal — the state as of December 2024
Report submitted to the state, **state board reviewed AND APPROVED it** (12/12/24: *"The
state board reviewed it last month and approved it"* — an advance on 11/14's "reviewed"),
with *"pretty much no feedback… It's really just a formality where they just make sure all
the boxes are checked."* **Town vote March 2025.** The July 1, 2026 effective date is stated
only at 11/14 and is **not** restated on 12/12. **No planning-committee chair has ever been
named, in any file, in the whole corpus.**

### The clerk: four different substitutes in one autumn
Kronberg's 2024 attendance, established file by file — **never assume it**:
8/21 absent (chair read it herself) · 9/18 absent (**Crawford** read it) · 9/4 present ·
9/12 present · 10/16 present · **11/14 absent (Pratt read all four rolls)** · 11/20 present
(all three rolls) · 12/4 present and named · **12/12 present** · **12/18 absent
(Mary Henry read it)**. That is four distinct substitute readers in five months.

### Two roster corrections
- **Sprague, not Petrin, is drafting the ad hoc communications document** (11/20/24:
  he reports it and is "finishing up"). Petrin's chairship is not contradicted — the
  drafting is Sprague's. Continuous with 10/16/24's "Mike and I are going to get together".
- **Finance Committee membership is confirmed on camera** 11/19/24 by Sprague's own
  round-robin: **Sprague chair, Whitney, Crawford**. Use this for the whole Nov–Dec run.

### Sprague's biography is now contradictory on the record, six ways
Flagged because it will keep surfacing. Across the corpus this one man is a school
counsellor, a principal ("three different high schools", 7/19/23; "when I was in Mr.
Herrington's position", 8/21/24), an administrator, a director of student services, a
juvenile-court liaison ("I did that for six years", 11/19/24) — and on **12/4/24, every word
at conf 1.00**: *"I'm not considered to have a higher degree because I only have an
associate's degree… both my wife and I both have [associate's] degrees."* That cannot be
squared with a principalship. **Two possibilities remain open and neither was forced:** he
has had an unusually varied career, or `Speaker 7` in 16192 merges two men (Petrin being the
only other candidate, though he is never named in that file). Quote as spoken; do not
harmonise.

### The one CSV that is not segment-based — and why it stays that way
`Claremont School Board - 8526` (8/5/26) is **turn-based**, not segment-based: 375 rows over
554 segments. It merges consecutive same-speaker segments and, more importantly, **splits a
segment where the speaker demonstrably changes** — e.g. the chair's handoff *"Mr. Campo, I'm
going to turn it over to you"* and the auditor's reply share one diarizer segment and
correctly get two rows. 160 of its 554 segments carry more than one speaker that way.
Flattening it onto the segment grid would **destroy real attribution work**, so it was kept.

`Scripts/verify_dialogue.py` now accepts both conventions. A CSV whose row count differs from
the segment count is re-checked as turn-based **only if its concatenated token list equals the
transcript's exactly**; it is then verified on monotonic timestamps, span containment and
non-empty cells, and reports `OK*`. A file that actually lost or reordered a word still fails.
**This is the intended shape for future work: prefer turn-based rows where a segment provably
holds two speakers.**

### Corpus QA pass — results

`verify_dialogue.py --corpus`: **127 passed, 0 failed, 0 without a source transcript.**

`--names`: 342 distinct Speaker values. **1,084 rows normalised** across 17 variants
(backups in `Scripts/backup_prenorm/`, and the `Scripts/speakers/*.speakers.json`
mappings were updated in step so a rebuild reproduces the corrected names):

| applied | → | rows / files |
|---|---|---|
| `Dr. Tim Broadrick` | `Tim Broadrick` | 242 / 2 |
| `Michael McCosker` | `Mike McCosker` | 174 / 4 |
| `Dr. Alex Herzog`, `Dr. Herzog` | `Alex Herzog` | 151 / 4 |
| `Dr. Michael Herrington` | `Michael Herrington` | 120 / 3 |
| `Lilly Clark` | `Lily Clark` | 69 / 4 |
| `Michael Koski` | `Mike Koski` | 61 / 3 |
| `Candace "Candy" Crawford` | `Candace Crawford` | 53 / 1 |
| **`Mike Campbell`** | **`Michael Campo`** | 49 / 1 |
| `Board member (unidentified)`, `Unidentified School Board member` | `Unidentified board member` | 46 / 3 |
| `Bill Madden`, `William "Bill" Madden` | `William 'Bill' Madden` | 43 / 3 |
| `Noel Kronberg` | `Noelle Kronberg` | 34 / 3 |
| `Tessa Nicholson Powers` | `Tess Nicholson-Powers` | 22 / 1 |
| `Multiple speakers` | `Multiple` | 14 / 5 |
| `Jen Gallagher` | `Jennifer Gallagher` | 10 / 2 |

**Corrections applied** (all four that were owed): `16951` — the eight Ward 2 rows are
**Don Lavalette**, proven three ways (he offers the board *"Mr. Tyson[,] me"* as the two
options; another speaker names the field as *"Mr. Lava[lette] and… Mr. Tyson"*; and the
excerpt file 16958 already carried four of the eight under that name). `15336` @3680.30 →
**Jennifer Gallagher**. `15483` Speaker 10 → **Rebecca Duska**. `15357` Speaker 4 candidate
list re-weighted — the "only seated member never heard" reasoning was wrong, since Gallagher,
not Miles, was the 10/18/23 absentee.

### Surname collisions DELIBERATELY left alone — for a human, not for an agent

The sweep flags these; each was checked and **none should be merged without evidence a
machine does not have**:

- **`Camron Lownie` vs `Ken Lownie` — settled, DIFFERENT PEOPLE.** They co-occur in two files
  (16409, 17046), so they cannot be one person. Both are ASR-derived from "Louny".
- **`Cassandra Edwards` (39 rows / 5 files) vs `Sandra Edwards` (11 / 1).** Same ward (3),
  same profession (parent and teacher), never co-occur. **Probably one person**, and the
  17092 role already hedges "as announced; not on public roster". A merge is recommended but
  needs a document.
- **`Michael Myers` (1/7/26, Ward 3) vs `Mike Myers` (2/7/26 deliberative, Ward 3, also an
  assistant moderator).** Almost certainly one man, one month apart — but **both are
  self-identifications**, and overriding what someone called himself needs better grounds.
- **`Hilary Walsh`** (Stevens technology teacher / yearbook adviser, self-ID) vs
  **`Hillary Walsh`** (Ward 1 commenter, adult-ed teacher, "name per approved minutes"):
  plausibly one person, independently sourced two ways. Left split.
- **`Hanna Brooks`** (Claremont resident commenter) vs **`Hannah Brooks`** (Greater Sullivan
  County Public Health Network / Dartmouth-Hitchcock presenter): different roles, left split.
- Genuinely different people sharing a surname, no action: Kiran / Onyx / Patrick Adrian ·
  Michelle / Rod Beaton · Christina / Ray Bernard · Derek / Sarah Ferland ·
  Jennifer / Maggie Gallagher · Dale / Ellie Girard · Alex Hill / Karen Liot Hill ·
  Cynthia / Loren Howard · Charlene / Marian / Mary / Rob Lovett · Paul / Tom Luther ·
  Eric / Leslie Peabody · Michael / Hannah Petrin · Scott / Tracy Pope ·
  Rob / Stephen Walker · Sherry Williams / Asher James Williams ·
  **Alex Herzog (SRVRTC director) vs Aubrey Herzog (student, NH Youth Governor)** ·
  **Michael Herrington (Stevens principal) vs Michelle Herrington (SRVRTC)** — this last pair
  appears in the SAME file at least twice (16021, 16070, 16222) and must never be merged.

### Newly dangerous ASR garbles from this wave

Names at high confidence that name **nobody**: **`Mr. Crowder` (0.95 and 1.00)** and
**`Mr. Free` (0.58)** in one Petrin sentence · **`Clarence Surprise`** (= "the Claremont…") ·
**`Mr. Smith.` (0.98)** and **`Mr. Pittman.` (0.87)**, both of which are the chair recognising
**Frank Sprague** · **`Now, Tyler, take it away`** (0.50 — no Tyler in the room) ·
**`the good magazines tonight`** · **`Mr. Oscar` (0.95)** and **`Mr. Costco` (0.96)** = McCosker.

Wrong-person or wrong-word at ≥0.95: **`Andy Crawford` (1.00) = Candace Crawford, inside an
attendance list** — the worst possible place for it · **`Frank Miller` (1.00) = Frank Romeo**,
in his own self-introduction · **`Baxter Hearn` = Patrick O'Hearn**, likewise ·
**`Frederick Erickson` (0.98) = Marjorie Erickson** · **`Rocky Ridge` (0.93) = Rocco Ruggeri**
(reads as a place) · **`Miss Grunberg` (1.00) = Kronberg** · **`Mr. Springs` (1.00) = Sprague** ·
**`Kenny` (0.77) = "Candy"** · **`Leah,` (0.88) = LEA** (a statutory role rendered as a woman's
name) · **`socialist degrees` (1.00) = associate's degrees** · **`the tenants` (1.00) = the
attendance** · **`Disney` (1.00) = Disnard** · **`Speedrun` (0.59) = "Suggest"** ·
**`the Scottish of Unity` (1.00) = the STATUS of Unity** · **`It's a parody` = parity** ·
**`the calm down lawsuit` / `convey` (0.98) = ConVal** · **`Miss McCosker` (1.00)** — correct
surname, wrong honorific, on a man.

Numbers are not protected by confidence either: **`3.53 to 12.75` (every token 1.00)** for the
NH Retirement rate is arithmetically impossible against the sentence that calls it a decrease
(almost certainly 13.53 → 12.75), and **`77 years`** for the LED payback is almost certainly
7 years.

### Two more "two Franks" hazards
- In **16215** (a Sprague-chaired Finance meeting) Henry says *"Chris is working with **Frank**
  on this right now, currently middle school principal"* — that is **Frank Romeo**, not Frank
  Sprague, who is in the room. Same hazard in **16226** (*"the cuts that Frank had to make…
  at the middle school"*).
- In **16158** the presenter says *"Go ahead Michael"* at **confidence 1.00** with **two
  Michaels in the room** — board member Petrin and Assistant Superintendent Koski. Left
  unnamed. Treat a bare "Michael" or "Mike" in any SAU 6 or Finance file as ambiguous three
  ways: Koski, McCosker, Petrin.

### Still open, for a human with documents
1. **The 11/14/24 SAU 6 policy-motion mover** — the chair's recognition is `Okay windy` (0.80),
   an ASR form this corpus attests for *both* Heather Whitney and "Candy" (Crawford). The two
   lines of evidence disagree. The approved 11/14/24 minutes would settle it.
2. **12/18/24 attendance** — Miles and Skillen answered no roll, were never recognised and
   spoke zero words; the chair accounts for exactly one unnamed late arrival ("when she comes
   in"), and Hawkins's first audible word is 71 minutes in. Draft minutes exist at
   `12.18.24 DRAFT CSB minutes (1).pdf` in the 1/15/25 packet folder (MAP.md §8).
3. **Who cast the single No** on the SAU 6 budget on 12/12/24. Not named, not counted.
4. **`Eric Perry`** (16222, both tokens conf 1.00) is a single-source candidate surname for
   the Newport CTE director this corpus otherwise knows only as "Eric".
5. **No draft minutes exist for 12/3/24 or 12/12/24** — checked three ways. 16213 is the first
   2024 SAU 6 file with no minutes cross-check available.

---

## Addendum 10 — corrections from the HTML page-build run (2026-08-28)

Findings from building per-meeting pages against the packets, warrants and approved
minutes. These **correct earlier addenda**; where they conflict, this addendum wins.

### Addendum 3 corrections

- **The 2/8/23 deliberative-session moderator IS named, and is Tracy Pope.** Addendum 3
  says the moderator is never named and warns against equating her with the presiding
  officer because she "is elected moderator at that election — after this meeting."
  **Reverse that caution.** Three documents name her presiding on 2/8/23: both sets of
  minutes ("Meeting called to order by Moderator, Tracy Pope"), the packet's Rules of
  Procedure ("Tracy Pope, Moderator"), and the 11/3/22 special-district minutes in the
  same packet. She was the **incumbent**, presiding over a session at which her own
  one-year seat was on the warrant, and was **re-elected** 3/14/23.
- **"Andy" is TWO people, not one unreconciled name.** Addendum 3 lists `Andy Bernier`
  (2/8/23) and `Andy LaFrance` (12/1/23) as an unreconciled pair. The 2/8/23 minutes list
  **"Andy Lafreniere — Ward 3"** speaking against the amendment *during debate*, while the
  recording has the moderator naming **Andy Bernier of the NH School Funding Fairness
  Project** *after the meeting closed*. Different people, different moments.
- **The 41–27 amendment tally is missing from the TRANSCRIPT, not necessarily the video.**
  The dialogue CSV has no rows between 1:35:11 and 1:43:19. Whether the announcement is
  audible on the recording was not tested. Say "not in the transcript", not "not on the
  recording".
- Names the minutes settle or contradict: **Raqual Fluette** (Addendum 3 says the surname
  is never spoken); **Patrick Adrian, Ward 1** moved the $1,000,000 amendment and is absent
  from the addendum's list of 2023 voices; minutes read **"Shawn Wadsworth — Ward 3"**
  against the corpus's "John Wadsworth (W2)", and **"Anne Feln"** against "Ann Fine".

### Addendum 2 corrections

- **The 2023 deliberative session was 2/8/23** (snow date 2/9), not 2/10/23. Warrant,
  notice, agenda and both minutes agree. The amount and tally in that sentence are right.
- **Era 0's vacant seat: the departed member appears to be Joshua Lambert.** The 11/3/22
  minutes list him as sitting; on 2/8/23 he seconds the amendment *from the audience*.
  Treat as a strong inference, not a fact.

### Facts established by the packets, worth carrying

- **RSA 40:13 has not been amended since 2019** (source note ends "2019, 192:2, eff. July 10,
  2019"), so its current text governs every meeting in this corpus. Durable.
- ~~**RSA 91-A:2, II's "names of the members who made or seconded each motion" clause is
  NEW** — added 2023, 188:1 and amended 2025, 112:1. Do not apply it to any meeting
  before those dates.~~ **THIS WAS WRONG — CORRECTED 2026-08-29.** The mover/seconder
  clause has been in force since **2018, 244:1, eff. January 1, 2019**: the 2017
  codification lacks it, the 2019 codification carries it. What 2025, 112:1 added was the
  start-time/end-time and minutes-producer requirements. **Apply the mover/seconder clause
  to every meeting in this corpus** — all of them postdate January 2019. Two consequences
  of the error: agents were about to credit districts with *voluntary* compliance for
  something the law required, and to miss real defects in 2019–2023 minutes that omit
  movers or seconders. Sources: 2017 and 2019 Justia codifications of RSA 91-A:2.
- The 2/1/23 proposed budget ($37,345,312) and default ($36,342,948) differ by **exactly
  $1,002,364 — the warrant's own Note A first-year CBA cost**, a third candidate
  derivation of the default that nobody at the table named.
- District records disagree on the 2/8/23 venue: the warrant and public notice say Stevens
  High School **Auditorium**; the agenda and both minutes say **Gymnasium**.


---

## Addendum 11 — further corrections, 2026-08-29

### A FOURTH vintage trap: RSA 198:20-b (unanticipated funds)

The current text requires a prior public hearing for unanticipated funds of **$20,000 or
more**. That threshold is the **2023, 38:1** text, effective **July 18, 2023**. Before that
date the threshold was **$5,000**. Any meeting in this corpus before 7/18/2023 involving a
gift or grant between $5,000 and $20,000 is affected: citing the current text turns a
*required* hearing into an apparently voluntary courtesy, inverting the finding. Pick the
threshold by the meeting's date.

### SAU 6 board composition, Dec 2022 – Feb 2023 — settled by three mastheads

The 12/1/22, 1/17/23 and 2/16/23 draft minutes each print the full board. They establish:

- **Frank Sprague was SAU 6 Vice Chair** before Ruggeri. No earlier addendum records the
  pre-3/30/23 officer.
- **Garry Bator was a Unity SAU 6 member** in this window and appears in no addendum —
  absent from all three meetings and described on tape as outgoing.
- **Kelly Simpson was NOT on the SAU 6 board** in this window. Addenda 2 and 3 list her
  among Unity members "in this era"; all three mastheads name exactly five Unity members —
  **Erickson, Popescu, Bator, Ruggeri, Hart**. Hart yes, Simpson no, at least through
  February 2023.
- **Joshua Lambert's departure is now documentary, not inferred.** The 12/1/22 minutes list
  twelve members including him; 1/17/23 and 2/16/23 list eleven, with Lambert the only name
  removed. (Addendum 10 had this as a strong inference.)

### Name and title corrections from contemporaneous district documents

- **Kristina Sanford**, not "Christina" — and her title is **Early Childhood Director**, not
  preschool/early-childhood coordinator. Both the 2/15/23 minutes and the superintendent's
  own report spell and title her that way. The recording says only "Christina".
- **Stephanie Hurst** is named in the 2/15/23 minutes as **"Literacy Specialist"**, which
  both anchors the surname to a 2023 primary source (Addendum 3 rated it medium confidence
  from a 2025 recollection) and contradicts Addendum 3's "SAU 6 Curriculum Director". Title
  unsettled; surname now solid.
- **Ann Fine** — spelling confirmed by the 2/15/23 minutes ("Ann Fine (Ward 2)"), against
  the 2/8/23 minutes' "Anne Feln".
- The lone No on the Angela Vivian vote (2/16/23) is **Steven Horsky**, per the draft
  minutes; the recording leaves that voice unidentified.

### New people
**Chelsea Weatherford** — SAU 6 recording secretary, signs the 12/1/22, 1/17/23 and 2/16/23
minutes (she reappears as Executive Assistant to the Superintendent by 11/19/24). **Will
Phillips** (NHSBA) · **Dr. Anne Wilson**, co-author with **Dr. Lupini** of a November 2022
organizational study of the SAU — the "Lupini report", in neither Drive share · **Zach
Hurst** (CanAm), funded elementary winter enrichment · **Sue Schroeder** · **"Susan"**, SAU
front office.

### New ASR garbles
`Mister Tuesday` = **Tempesta** (dangerous — reads as an ordinary phrase) · `the Luchini
report` = the **Lupini** report · `Q Sarge` = **Kearsarge** · `Kent, M` = **CanAm** ·
`Warren article` = warrant article · `miss 26` = **MS-26** · `we need a revolt` = re-vote ·
`I don't recession` = the deliberative session · `letters of government` = letters of
agreement · `s s are funds` / `the SRE` = **ESSER** funds / the **SREA** · `policy CVI`,
`GCU`, `GCA` = **CBI / GCQ** · **`a second by Brittany` — dangerous: "Brittany" is nobody in
the room; it is the chair failing to identify a seconder, and it reads as a real name.**

### District records that disagree with themselves (report, don't reconcile)
The 1/17/23 minutes state both budget motions as "…three hundred and **thirteen** dollars"
($38,345,313 / $37,345,313) where the warrant, the ballot and every other record say
**$38,345,312 / $37,345,312** — a one-dollar error at the start of the whole budget sequence.

### Addendum 11 corrections (2026-08-29, from the 5/11/23 page)

- **Kelly Simpson JOINS the SAU 6 board in April 2023, and Garry Bator leaves.** Addendum 11
  says "Hart yes, Simpson no, **at least through February 2023**" — that hedge is right and
  its window is the limit. From **4/13/23 the position reverses**: the 4/13, 5/11 and 7/13
  minutes mastheads all name **Kelly Simpson** and none names Bator. On 5/11 Simpson answers
  every roll call, is named by the chair ("seconded by Kelly"), seconds the recess motion,
  and is the member Erickson credits with raising the conflict-of-interest concern.
  **Unity five from April 2023 onward: Erickson, Popescu, Simpson, Hart, Ruggeri.**
- **Frank Sprague's SAU 6 vice-chairship ends 3/30/23.** From that date the SAU 6 vice chair
  is **Rocco Ruggeri**; Sprague's "vice chair" title thereafter is the **Claremont** board's.
  Do not carry the SAU role past March 2023.
- **The SAU 6 board had NO secretary at all through 2023** — the statutory office RSA
  194-C:5, I requires, distinct from Chelsea Weatherford's role producing the minutes.
  Addendum 3's "the clerk seat was VACANT through 2023" covers the *Claremont district*
  clerk and is a different seat.
- **Mary Henry was appointed business administrator on 11 May 2023**, on Tempesta's
  nomination. Addendum 2's "starting early July 2023" is her START date, not her appointment.
- **The SAU 6 minutes-filing practice changed in May 2023.** 5/11/23 is the first SAU 6
  meeting whose minutes were filed in its OWN packet folder and inside the five-business-day
  window. The two-stage search rule (html_briefing §6) still applies to 2024–25.
- New people: **Eric Zengota**, publicist — a Claremont district employee funded partly with
  SAU money from Unity through federal grants. **Amanda Phelps**, NHSBA. **"Sharon"**, SAU 6
  business office — surname never spoken.

### Addendum 11 corrections, part 2 (2026-08-29, waves 2–3)

- **Addendum 2 is wrong that the 7/13/23 SAU 6 chair vote "is not audible."** The minutes give
  it outright: **Hawkins 8, Erickson 3**. **Arlene Hawkins is SAU 6 chair from 7/13/23**, not
  "from 11/9/23 onward." Ruggeri nominated Erickson (2nd Gallagher); **Sprague** nominated
  Hawkins (2nd Simpson).
- **Hawkins was SAU 6 TREASURER** (elected 4/13/23) and vacated that office by becoming chair;
  **Bonnie Miles** became SAU 6 treasurer 8/17/23. In no addendum before now.
- **The SAU 6 secretary vacancy runs at least through 8/17/23.** Both mastheads print only
  Chair and Vice Chair while the agenda line still reads "Secretary Roll Call of Attendance."
- **Addendum 2 overstates the 7/19/23 appointment.** It reads "Candace Crawford appointed 4-2
  over David Bailey and Kevin Tyson." **Bailey drew no nomination** — the 4–2 was Crawford v.
  Tyson only.
- **Steven Horsky's 6/21/23 resignation also vacated the SAU 6 chair** he had won 6–5 on
  3/30/23, which is why officers reopened on 7/13.
- **Dr. William Lupini** is the Lupini report's first author (8/17/23 minutes).

### Name resolutions from district documents (waves 2–3)

**Shaun Laplante** (not Sean/Shawn) — his own grant proposal, signature block and district
e-mail `slaplante@sau6.org`; **the dialogue CSV speaker label is also wrong.** ·
**Danielle Skinner** = Data Manager / Food Service / PowerSchool, SAU 6 — distinct from
**Deborah Skinner**, art teacher at Stevens; Addendum 4's "do not merge" was right ·
**Steve Holt** = Maintenance Director · **Sharon Mezzack** = the SAU 6 business-office
"Sharon" (Accounting & Grant Manager) · **Catlin "Cat" McLaughlin** · **Lori Mowrey** — a
sixth spelling for the Lori surname, and the only one from a district document ·
**Susan Cantara** (not Sue Kantara) · **Crystal Simonds** (not Simmons) · **Megan Fagans**
(not Fagan) · **Amalia "Mimi" Rhines** · **Shawn Herzog**, Title I teacher at Maple — a
SECOND Herzog, distinct from Alex Herzog (SRVRTC); never merge on surname ·
**David Irwin** was CMS **Academic Dean** on the 2021–23 ELA advisory board, earlier and a
different title than Addendum 2's "2024-25 assistant principal" · **Michael Herrington was
Stevens ASSISTANT principal in the 2023-24 handbook**, alongside Paige Jarvis — narrows
Addendum 2's open changeover date.

**Stephanie Hurst's title cannot be settled** — the district uses both in one packet: the
agenda and minutes head her item "Curriculum Director Presentation" while the framework she
authored, in the same folder, titles her "Literacy Specialist, SAU 6".

### Two research traps
- **The 5/17/23 board meeting has NO minutes in any share** and the district's own minutes
  numbering skips it (7 = 5/3, 8 = 6/7, 9 = 6/21). Two policies had their first reading there.
  Searches on `5.17.23`, `May 17`, `5-17-23`, `051723`, `5.17.2023` all return nothing.
- **The packet document "Retreat Minutes May 16, 2020" is really the May 16, 2023 retreat** —
  Hawkins and Gallagher were not elected until 3/14/23 and the content is all SY 23-24. The
  district's own file name and heading are three years wrong. That retreat was a **quorum**
  (6 of 7) with no notice located.

### Addendum 5 correction — the 10/18/23 absentee (2026-08-29)

**Addendum 5 says "the 10/18/23 absentee is now pinned: Jennifer Gallagher … which also means
the 10/18 minutes wrongly recorded her present." The second half is FALSE.** The approved
10/18 minutes read, in terms, `Absent: Jennifer Gallagher`. Two agents confirmed this
independently against the document.

What the minutes actually get wrong is different and worse: **they account for only five of
seven members** — four present, one absent, with **Bonnie Miles and Whitney Skillen in
neither column.**

And the absence may not be Gallagher's alone. The 11/1 minutes attribute the
minutes-correction request to **Bonnie Miles**, and the chair's on-tape reply — "You're
documented as being on there" — only fits a member the 10/18 minutes did *not* list as
absent. Miles never speaks on the 10/18 recording; Skillen speaks nineteen times. So Miles
is the likelier second absentee and **both were probably out**.

**Consequence for a correction already applied.** On 2026-08-28 the `15357` Speaker-4 Role
note was re-weighted on the premise that "Gallagher, not Miles, was the 10/18 absentee," and
Miles was therefore promoted as a candidate for that cluster. That premise is now doubtful:
if Miles was also absent she cannot be Speaker 4 either. **Treat the 15357 Speaker-4 cluster
as unresolved** — live candidates are Assistant Superintendent Mike Koski, curriculum
director Cat/Kat McLaughlin, and Candace Crawford. Do not name it.

The separate `15336` @3680.30 correction (the curriculum-committee line → Jennifer Gallagher)
is unaffected: it rests on her being the curriculum reporter on 9/20, 10/18 and 11/1, which
the agendas and minutes independently support.

### Two more corpus-wide facts (2026-08-29)

- **All four district subcommittee Drive folders are EMPTY** — `Capital Improvement`,
  `Claremont Policy Sub Committee`, `Curriculum Committee` and `Ad Hoc SAU Exploratory
  Subcommittee`, all owned by sau6webmaster@sau6.org, all created 27 Oct 2022, all returning
  zero files (verified 2026-08-29). That supports the subcommittee-minutes flag on **any**
  Claremont board page, not just the one that found it.
- **The district maintains a LIVE POLICY INDEX** — `Claremont SB Policies (for Web)`, Drive
  doc `1JmygIGNaVc8ZfaQWtoIA25tRaBGw2Oh5k5ARsGlreqg`, owner sau6webmaster@sau6.org. It lists
  every board policy with its adoption date and links the current text, and it is the
  authoritative answer to "what was actually adopted". **Check it on every page that touches
  a policy reading** instead of writing that an adopted text is unrecoverable.
- **Addendum 4's 10/4/23 subcommittee roster is incomplete and wrong on chairs.** The agenda
  names them: **Capital Improvement chair Bonnie Miles**, **Budget chair Frank Sprague** (not
  Whitney), Policy chair Skillen, Ad Hoc chair Gallagher — and the addendum **omits the
  Curriculum Committee entirely**, which Gallagher chairs. Attendance for 10/4/23: **Candace
  Crawford absent**, the other six present.

## Addendum 12 — from the 2/3/2024 deliberative session page (2026-08-29)

### Corrections and closures to Addendum 6
- **The "'Sean' of the school district attorneys (2/3/24, no surname)" open item is CLOSED.** Both
  the draft and the approved 2/3/24 minutes name him: **Shawn Tanguay, School District Attorney**.
  He is introduced on tape and never speaks. Claremont's attorney in 2023 was Matt Upton.
- **Charlene Lovett as 2/3/24 moderator is confirmed and sharpened.** All four district documents
  (agenda, Rules of Procedure, draft and approved minutes) style her **"interim moderator"** — a
  title with no statutory basis. **Tracy Pope is absent from the entire record**: not on tape, not in
  either set of minutes. No moderator pro tempore is chosen or appointed anywhere.
- **The FY25 figures are confirmed to the dollar and one component is added**: general operating
  $36,117,407 + **grant and food service $3,465,000** = Article 2 total $39,582,407; default
  $35,906,774 / $39,371,774; difference $210,633. FY24 approved general fund $34,880,311.72; the
  FY24 *ballot* total was $38,345,312 (general + $3,465,000), which is the base line on the district's
  FY25 default worksheet.

### A subcommittee that is in no other record
Heather Whitney, introducing the board on 2/3/24: she is "the chair of the Claremont School Board and
the chair of the **parliamentary Procedure ad hoc committee**", with **Frank Sprague** a member. This
committee appears in **no** packet, agenda or minutes on this project — not in the board's own
subcommittee list of 1/17/24 (Capital Improvement/Miles, Finance/Sprague, Policy/Skillen,
Curriculum/Gallagher, Ad Hoc Disruptive Behaviors/Gallagher) and not in Addendum 7's 3/20/24 reading.
The minutes reduce the whole introduction to "and their committee positions", so the recording is the
only public record of it.

### Names from district documents (2/3/24 and 1/17/24 minutes)
**Brandon Perry** (Ward 3, district IT employee) · **Wayne Hemingway** (Ward 1, the only voter to
speak against the FY25 budget) · **Tom Luther** (Ward 1, spoke on process; his turn is not in the
transcript at all) · **Kelly Fontaine** and **Jean Allen** (Ward 1) · **Pam LaBounty** (Ward 3,
30-year paraprofessional) · **Matt Bean** confirmed as the paraprofessionals' association president ·
**Lee Mulloy** (presents Academy program data, 1/17/24) · **Shawn McCarthy** (Ward 1, citizens'
comments 1/17/24). Confirmed spellings from district documents: **Polly Bath** (not Bathurst — the
board's own deck reads "Polly Bath Classroom Mgmt"), **Dr. Staves**, **Kylee Plummer**,
**Cat McLaughlin**, **Courtney Porter**.

### New ASR garbles (heard = actual) — the dangerous ones first
`Ben Esther` = **Ben Nester** — dangerous, because `Esther` is this corpus's standing ESSER garble
and both occur inside one budget presentation · `Mr. Clark` = **District Clerk** (mints a person out
of an office) · `National Association of Taxpayer` = the **paraprofessionals' association / Teamsters**
(names an organisation that does not exist) · **`parents` and `pairs` = paras** — runs through the
whole Article 5 debate ("my parents rock every day", "over 60 parents within this district", "the
relationships that the pairs have with students"); read literally it turns a paraprofessional pay
debate into one about parents · `Saw six` = **SAU 6** (joins `Sussex`) · `Dear Whitney` = Heather
Whitney · `the liquid session` = **deliberative session** (joins `delivered session`, `I don't
recession`) · `The babe` = debate · `The workers` = the voters · `the abhorrent article` = a warrant
article · `a Greer counselor` = a **career** counselor · `the doctor state's` = **Dr. Staves** ·
`Miss Quarter` = **Miss Porter** · `DC` / `DC f` = **DCYF** · `The answer grant` / `the ceremony` =
the **ESSER** grant / ESSER money · `a construction` = **instruction** (3×) · `as a menu` = **as
amended** · `a journey` = **adjourning** · `RSA 44 and 13` = **RSA 40:13** · `Frank spray` = Sprague ·
`Candace Parker` = Candace Crawford · `Miss Whitney Skilling` = Whitney Skillen.

### Two method notes
1. **The minutes list floor speakers grouped by position but in speaking order within each group.**
   Proved twice on this recording: Gary Merchant is 4th of 4 in the minutes' Article 2 "in favour"
   list and 4th of 4 on tape; Matt Bean is 1st and Chris Pratt 5th in both on Article 5. That makes
   ordinal identification defensible for the speakers the ASR leaves unnamed — but show the working.
2. **`dial.txt`-style dumps can silently drop a repeated phrase.** A quotation copied from a dump of
   this file read "There's there is over 60 parents"; the CSV actually says "There's there is **that
   there is** over 60 parents". `verify_quotes.py` caught it. Copy long quotations from the CSV
   field, not from a reformatted dump, and run the checker before you believe your own transcription.

## Addendum 13 — from the January 2024 wave (2026-08-29): 1/5, 1/11, 1/17

### The FY25 budget thread, closed to the dollar
- FY24 appropriated: **$34,880,311.71** — but the district's own documents give it three
  ways: `.71` (3 Jan summary), `.72` (Exhibit E), `.92` (Exhibit D grand total). Report the
  discrepancy; do not pick one silently.
- Moved to hearing 20 Dec: **$36,313,407.97** (4.11 %).
- Adopted 17 Jan: **$36,117,406.87** (3.55 %) — a reduction of exactly **$196,001.10**.
- FY25 default: **$35,906,773.87**, which the district rounds to $35,906,774. Adopted is
  **$210,633** over default.
- Crawford's on-air target was 3.75 % = $36,188,323; the adopted figure landed ~$71,000
  *below* her own target.
- Grant and food-service block: **$3,465,000**. FY24 *ballot* total **$38,345,312**
  (= $34,880,312 + $3,465,000), the base line on the FY25 default worksheet.
- **The $688,426.17 mystery from 18 December closes on 5 January**: a credit for
  grant-funded salaries the previous business administrator never allocated to the lines it
  belonged on. Henry redistributed it and named the $16,830 she could not place
  (account `100.40.1100.113.5.00000`). Sprague's separate FY24 audit found "close to
  probably half a million" of misentries.

### The untelevised session of 10 January 2024 — decided on camera
At 1:42:26 on 5 January the finance committee decides **on camera** that its next working
session will not be televised; at 1:50:49 it is set for 9 a.m. Wednesday 10 January at the
SAU office. The 17 January packet then contains `Exhibit D- Claremont FY25 Proposed Budget
Updated 1-10-24 Finance Committee` and `Exhibit E- Claremont Summary Page 1-10-24`. Eight
function movements between the two published summary pages sum **exactly** to $196,001.10,
the largest `2113 Social Worker` −$198,088.07 and `2210 PD Support` +$100,743.02. On
5 January the committee agreed to two elementary social workers plus a coach; the 10 January
budget has one and one. **No notice, recording or minutes exists for that session.** Its
only documentary trace is those two exhibits, filed under §39.

### The revenue side is missing from the packet, again
Exhibit D (54 pp.) returns **zero** occurrences of Revenue / Revenues / Adequacy / Receipt /
Fund Balance / Estimated / SWEPT; Exhibit E has no revenue line. Yet $852,000, $519,000 of
new state aid, a $420,000 fund balance and grant-funded initiatives all exist only as
speech. The 29 January working-session minutes prove the schedule existed. It reached the
public only at the 3 February deliberative session.

### Names — corrections and additions
- **Lee Malloy is "Lee Mulloy" in two district documents** — the 1/17/24 packet's Exhibit A
  ("Program Data Review - Lee Mulloy - Lead Teacher") and both sets of 1/17 minutes.
  Addendum 4 has Malloy. Per the Shaun Laplante precedent the district documents are the
  stronger source; **record the conflict, do not pick one**.
- **"Sean" of the school district attorneys (Addendum 6, open) is CLOSED: Shawn Tanguay,
  School District Attorney** — both sets of 2/3/24 minutes.
- **Cat McLaughlin** — the minutes spell her Cat; Addendum 11's "Catlin 'Cat'" is not the
  district's spelling.
- **Kylee Plummer**, not Kylie — agenda and both sets of 1/17/24 minutes.
- **Polly Bath** now has two primary sources — the 1/17/24 Curriculum Update and the board's
  own `School Board Presentation.pdf` ("Polly Bath Classroom Mgmt", beside "Dr. Staves-Math
  instruction").
- New public voice: **Sean/Shawn McCarthy, Ward 1** (minutes: Shawn; ASR: Sean).
- New names: **Josh Nelson**, the CCTV operator who broadcast the finance sessions, thanked
  by name; **Sarah Goddard**, former SRVRTC life-skills instructor; **Ben Nester** (ASR
  garbles him as "Ben Esther", which collides with the ESSER garble family inside one budget
  presentation).
- **A roll-reader no addendum records: Mike Koski.** The 1/11/24 minutes read "roll call
  vote taken by Mike Koski".

### Subcommittee roster as of 17 January 2024 (from the agenda)
Capital Improvement — **Miles** (chair) · Finance — **Sprague** (chair) · Policy —
**Skillen** (chair) · Curriculum — **Gallagher** (chair) · SRVRTC Visioning — Sprague, Miles,
Crawford · Ad Hoc Disruptive Behaviors — **Gallagher** (chair). Consistent with Addendum 11's
correction to Addendum 4. Separately, a **Parliamentary Procedure ad hoc committee** (chair
Whitney, member Sprague) is read into the record on 3 February and appears in no other
document.

### Two attribution problems on 17 January that cannot be resolved from the record
- Minutes: "Whitney Skillen amended the motion… Jennifer Gallagher seconded." The recording
  has the chair addressing the mover as Jennifer/Jen three times; the second is
  unattributable. **Skillen and Miles are recorded present and are never heard or named** —
  zero occurrences of either surname or any variant. Present both; choose neither.
- Minutes give the benchmark question to Bonnie Miles; the CSV gives it to Arlene Hawkins.
- Minutes print **$69.33** per $100,000; Henry says **$69.39**, twice.
- **The approved 1/17 minutes are the draft, word for word.**

### Minutes timeliness — a measurable finding
Drive metadata dates the 1/17 draft to **14 Feb 2024, 4:09 p.m. ET** — the 20th business day
(deadline 24 Jan) — filed in the *21 February* packet, **eleven days after voters
deliberated on the budget it records**. State the limit: Drive posting is not the statutory
"open to public inspection".

## Addendum 14 — from the February–March 2024 wave (2026-08-29): 2/15, 2/21, 3/6, 3/20

### The 2024–25 board, elected 20 March 2024 — supersedes Addendum 7's roster
Attendance: six present (Whitney, Sprague, Miles, Hawkins, Crawford, **Petrin**);
**Whitney Skillen absent** — no earlier addendum records this.

**Officers.** Chair **Heather Whitney** (nominated Sprague). Vice chair **Frank Sprague**
(nominated Crawford). Both uncounted voice votes, taken *before* the roll call.
**No secretary was elected** — policy BDB (adopted 2 Jan 2019) requires three officers.

**NHSBA delegate** Frank Sprague.
**Capital Improvement** — **Miles chair**, Crawford, **Sprague joining**; **Skillen steps off**.
**Finance** — **Sprague chair**, Crawford, Whitney.
**Policy** — **Skillen chair**, Hawkins, **Petrin rejoining** (not "new" — he served in prior
years; chair on tape and the approved minutes both say rejoin).
**Curriculum representative** — Hawkins.
**SRVRTC Visioning** — Miles, Crawford, **Petrin joining**; **Sprague steps down**.
All six disposed of by "no objection" — **no votes taken**. **No Ad Hoc Disruptive Behaviors
Committee** on the list: neither re-constituted nor dissolved. **No Parliamentary Procedure
committee** either.

**This roster held through May.** The 4/17/24 and 5/15/24 approved minutes both give Capital
Improvement chair as Miles. The 5/15 *recording*'s "Whitney + Sprague + Crawford" is
contradicted by that same meeting's own minutes — so Addendum 7's "later readings drift"
caution needs that qualification.

**Before 20 March 2024** Capital Improvement was **Miles (chair), Crawford, Skillen**;
Sprague was not on it. Addendum 7's roster is the *post*-3/20/24 one.

### Officer-election seconders — Addendum 7 is wrong against the district's own minutes
Addendum 7 records the vice-chair second as "Whitney", taken from the ASR's ambiguous
"A second now." The **approved minutes** say: chair — "Frank Sprague nominated Heather
Whitney, **Arlene Hawkins** seconded"; vice chair — "Candace Crawford nominated Frank
Sprague, **Bonnie Miles** seconded". The tape has one unidentifiable word. **Report both;
choose neither.**

### The Parliamentary Procedure ad hoc committee — Addenda 12 and 13 corrected
It is in no other *document*, but the 3/20/24 recording (Whitney, 1:30:18–1:31:53) is a
fuller source than the corpus knew: formed **in 2022**; "composed of two board officers and
an saw officer. The superintendent and the Business administrator"; remit — absence of
curriculum and financial oversight, sporadic communications, insufficient agenda
preparation; output — the pre-populated agenda, the onboarding manual, the SAU 6 website,
the public-communication policy review, and the draft by-laws; and "prior to **suspension of
the subcommittee's activity**." It had **three members, not two** (Sprague, 1:44:55:
"between the three of us collectively… one or the other of us has been the chairman of the
board… for the last decade"); the third is not identifiable. **It does not survive into the
2024–25 list.**

### The by-laws
6 March minutes: "Taken and adapted from the **NHSBA** by-laws". 20 March minutes: "School
district's attorney recommended **Manchester** By-Laws as a model". The recording supports
Manchester (Matt Upton named). Deferred to "our next meeting" and then absent from the
17 April and 15 May agendas — **whether they were ever adopted is unresolved**.

### Names — corrections and additions
- **"Ms. Chastain" is Jill Chastenay** — her own signed letter (2/21/24 Exhibit A) and the
  agenda; confirmed by the 2/21/24 approved minutes. Corrects Addendum 7.
- **Cat / Catlin McLaughlin is NOT resolved.** Addendum 13 overstated it. The SAU 6 Office
  Monthly Report in the 2/21/24 packet spells it **Catlin** ("Curriculum/Grants (Catlin /
  Michael)"); the minutes spell it **Cat**. Two district documents, two spellings — record
  the conflict, do not pick.
- **"Aubrey Herzog" is Aubree Herzog** in the district's own 2/21/24 Exhibit A. (Student
  privacy: do not print this on a page.)
- Presenters misspelled in the 3/6/24 approved minutes, against their own self-IDs on tape:
  **Scott Blewitt / Blewett**, **Kari Rothford-Hague / Kerry Rochford**, **Taylor Lauck /
  Taylor Luke**.
- New: **Mr. Kennedy**, CMS enrichment teacher (first name never spoken); **Nicole Bouchard**
  and **Kylee Plummer**, the two student members; **Rick Elliott**, interim assistant
  principal at Stevens; **Steven Holt**, maintenance director (signs 3/20 Exhibit D);
  **Michelle Herrington**, Bluff guidance counsellor; **Shawn Herzog**, Title I at Maple
  (≠ Alex Herzog); **Noelle Kronberg**, district clerk.
- **The district contradicts itself inside one document**: the 3/6/24 minutes' masthead says
  Kylee, its body says Kylie. The 15607 dialogue CSV also labels her Kylie.
- **The "Alex Barney" template error recurs**: the body of the 12/20/23 approved minutes reads
  "Student Board Members-Nicole Bouchard and Alex Barney - not present" while its own masthead
  reads "Kylee Plummer". Not confined to 11/1/23.
- **The Stevens interim principal is still named nowhere.** The 2/21 Exhibit 4 is written by
  "the new interim principal", unsigned, and speaks of "continuity between Chris and myself";
  reports were due 8 Feb and the packet went up 14 Feb, so the change had happened by
  **mid-February 2024**, not by 6 March as Addendum 7 implies.

### Dialogue CSV label errors — `15580 SAU6021524.mp4.CSV`
- Row at **2956.86s** ("To make a motion to change our meeting schedule to a bi monthly
  schedule") is labelled **Arlene Hawkins**; it is diarized Speaker 11 = Heather Whitney, and
  the minutes name Whitney as mover. **The label is wrong.**
- **Rocco Ruggeri has zero rows in 460** while the minutes credit him with six acts. The
  Speaker 4 cluster labelled Frank Sprague holds *both* the second on the HR contract motion
  (1307.5s) and the abstention on it (1322.2s) — **Ruggeri's voice is inside that cluster**.
  No mover in it is safe from the label alone.
- The "lose touch" run at **2980.34s** labelled Bonnie Miles sits inside the chair's Speaker 1
  cluster and plainly holds an interjection; the minutes split it between **Atonya Hart** and
  Miles.

### New ASR garbles (heard = actual)
`Craig Sprague` = Frank Sprague · `Vinnie. Skilling` / `Miss skill` / `And skill` = Whitney
Skillen · **`Alpha` = "I'll"** (Pratt: "Alpha defer to the principal") · `Warren articles` =
warrant articles · `huge sigma` = stigma · `pulled all of the eighth graders` = polled ·
`Paris CBA` = paras' CBA · **`for $20,000` = $420,000** (the clerk reading a motion back) ·
`Seeing rejection` = seeing no objection · `my current voyages` = my current chairs ·
`an excellent condition` = an excellent addition · `embedded` = vetted · `pirate school` =
PowerSchool · `Michael Cosby` = Koski · `hiring community` = hiring committee ·
`a sore 102` / `Saw 99` = SAU 102 / SAU 99 · `43403` = ¶4.03 · `Miss Myles` = Bonnie Miles ·
`Eileen Hopkins` = Arlene Hawkins. `Mr. Broughton` recurs (15607 @0:51:08) and still names
nobody.

### The consent-agenda label drifts
"(vote required)" 17 Jan → "(consent required)" 21 Feb → "(consent approval required)"
6 Mar. Three labels in seven weeks. Report it; do not infer motive.

### Minutes timeliness data points
- 3/20 draft created in Drive **16 Apr 2024, 4:03 p.m. ET** — 19th business day (deadline
  27 March); approved 17 April; approved PDF created 29 April. **Two grants were gated on
  these minutes** ("We have to send in the minutes from this meeting to the state and then
  the funds will become available").
- Folder `3. SAU 4.11.24` created **2024-05-29 14:15 UTC**, with the 2/15/24 minutes landing
  three minutes later — so the **entire April 11 packet went up 48 days after that meeting**,
  and the February minutes reached the share **104 days** after theirs.

### Board policies, read from the live policy index with their own history blocks
**BDA** Board Organizational Meeting (adopted 2 Jun 2004) — the superintendent calls to order
and presides "during and until the election of a Chairperson". **BDB** Board Officers
(adopted **2 Jan 2019**) — chair, vice-chair **and secretary**, one-year terms. **BDE**
Committees and Delegates (adopted 2 Jun 2004) — committees and delegates "**approved by vote
of a majority of the Board**". **BEDH** Public Participation (adopted 6 Sep 2023) —
internally contradictory: "a minimum of thirty minutes in total" in §B against "will close
the public comment period after there is no response" in the procedures.

## Addendum 15 — April–June 2024 (2026-08-29): 4/17, 5/15, 6/5, 6/20

### Closures
- **The by-laws were adopted 5 June 2024** (see `html_briefing.md` §23a). Addendum 14's open
  question is closed.
- **The Parliamentary Procedure committee's third member is Michael Petrin** — Whitney, 4/17
  at 1:13:11. Addenda 12–14 closed on this.
- **Addendum 7's unresolved "Andy" is Andre LaFreniere**, chair of the SRVRTC Vision
  Committee — approved 6.20.24 minutes, "Alex Herzog read a statement on behalf of Andre
  LaFreniere". Fifth rendering of the surname, first in a district document.
- **Addendum 7's "Alex Herzog is leaving… no departure is ever stated outright" is WRONG.**
  Stated outright on 6/5/24 at 1:08:44 ("resignation as director of the Tech center") and in
  the approved 6.5.24 minutes ("recognized Dr. Herzog, his resignation") — seven weeks after
  he presented a 5–7-year strategic plan and a $10–12M renovation to this board.
- **Addendum 7 is wrong that `Mr. governor` and `Charlie` "name nobody recoverable."** The
  approved 6.20.24 minutes name that voice **Charles Gessner**.
- **Addendum 7's "Present" roll-answer tell is dead.** On 15 May three members answer
  *Present* (Sprague, Skillen, the chair), Miles answers *Yes*, and Hawkins, Petrin and
  Crawford answer *here*.
- **Patrick O'Hearn started Monday 15 April 2024** — confirmed on the 4/17 recording at
  0:10:35. Note the 4/17 agenda masthead still reads "TBD, Human Resource Director" while the
  4/17 minutes print his name.

### Pratt's interim → permanent, bracketed by district documents
5/15/24 masthead (draft and approved): "Christopher Pratt, **Interim** Superintendent".
6/5/24 agenda and approved minutes: "Christopher Pratt, Superintendent". The 11 May retreat
minutes list "Hired a great superintendent" and tick "Hire superintendent"; on 15 May he says
"as your former principal and now the superintendent". **Caveat: the Claremont board does not
appoint the superintendent (RSA 194-C:5) — the retreat note is loose usage, not a record of
appointment.** The 22 May session is the likeliest date and its minutes are sealed ten years.

### Administrators, settled from Exhibit F (DMG deck, posted 4 June 2024) and Exhibit A
**Melissa Lewis** — Disnard · **Christine Baker** — Bluff · **Mark Blount** — Maple ·
**Sue Schroeter** — Unity (new) · **Frank Romeo** — middle school · **Michael Herrington** —
High School Principal (a district document naming him HS principal on **4 June 2024**,
earlier than Addendum 7's 6/20 dating).
New: **Nichole Boynton**, Student Services Coordinator, Disnard · **Joshua Nelson**, CCTV
Executive Director (the "Mr. Nelson" of the 5/11 retreat minutes) · **Paige Jarvis**, SHS
assistant principal L–Z, with **Rick Elliott** A–K (Elliott was the high school's
instructional coach before that) · **Danielle Skinner**, Data Manager / Food Service /
PowerSchool · **Tracy Cohen**, Assistant Director of Student Services · **Chelsea
Weatherford**, Executive Assistant to the Superintendent · **Michael McCosker**, Dir. Student
Services (page 3 of the Superintendent's End of Year Report — in the board's hands the night
it said farewell to Ben Nester without naming a successor) · **Caleb Milbourn**, citizen,
Ward 1 · **Charles Gessner** · **Mr. Lambert**, the technical centre's sole substitute
teacher · **Hope Damon**, State Representative (the 17 April minutes name her bills:
**HB1583** adequacy/differentiated aid, **HB1656** three-tier special-education funding).
**Lori Mowrey** — a *sixth* spelling of the business-office Lori (Addendum 7 has Murray,
Maury, Marie, Morey, Mallory).

### Name conflicts, narrowed
- **Catlin McLaughlin**: three district documents to one. The 5/15 agenda and both sets of
  5/15 minutes print *Catlin*; only the 2/21 minutes print *Cat*. Addendum 14's "record the
  conflict, do not pick" can be narrowed toward Catlin.
- **Aubree Herzog** and **Gage Morin** (agenda + both sets of 5/15 minutes); the tape says
  "Aubrey" and "Moran". Addendum 7 carried the tape spellings.

### The consent-agenda label reverted
"(vote required)" 17 Jan → "(consent required)" 21 Feb → "(consent approval required)"
6 Mar → **"(vote required)" again on 5 June**. Five labels. Report; infer nothing.

### An attribution conflict, reported not resolved
The approved 6/5 minutes credit the Alex Herzog tribute to **Patrick O'Hearn**; the diarizer
puts it in the same four-utterance cluster as the by-laws motion, which the same minutes
credit to **Mike Petrin**. Both cannot be right.
And on 4/17: the Valley Regional / Dartmouth-Hitchcock remark at 0:55:32 is **Arlene Hawkins**
in the CSV and **Bonnie Miles** in the approved minutes — the diarizer merges the two women's
voices, so the tape cannot settle it.

### Minutes timeliness data points
- 20 March minutes: `createdTime` 2024-04-16 = 19th business day, the day before the meeting
  that approved them. **Two grants were gated on them.**
- 17 April: draft 2024-05-08 = 15th business day; approved 2024-05-20 = 23rd. The federal
  **General Assurances FY 2025** were gated on them.
- 11 May retreat minutes reached the share 29 May — **seven business days late**.
- 20 June approved minutes reached Drive 2024-08-08 = the **34th** business day, and **no
  draft was ever filed** — the lag is caused entirely by there being no July meeting to
  attach a packet to. (6/5's draft landed on the 5th business day exactly, inside the 6/20
  packet.)

### New ASR garbles (heard = actual)
`Riley Hawkins` = Arlene Hawkins · `20 miles` / `Miss Myles` = Bonnie Miles · `Billboard` =
Milbourn · `Mr. governor` / `Charlie` = Charles Gessner · `across the continent` = "to
appropriate" · **`$82,000` = $583,000** (same clerk read-back) · `Citizens married` /
`Disney` / `Dennard` / `dinner` = **Disnard** · `Thurmont` = Claremont · `banished` = Spanish ·
`no foreign policy` = "no phone policy" · `IAP` = IEP · `path time` = pass time · `the people
break` = the April break · `I am not being a person tonight` = "not being [in] person" ·
`Miss Grunberg` / `Mr. Cronenberg` = Kronberg · `S Rev` / `SRM` / `the urban s` = SREB ·
`Mr. Costa` = Koski · `Mike patron` = Michael Petrin (standing). Addendum 8's `So, Donald,
we'd like to have a rollback` = "so down the line" recurs and still names no one.
`Plot up` (precedes the Stevens roof figure) is unrecoverable.

### Two privacy exposures in the district's public Drive — describe, do not reproduce
- **4/17/24 Exhibit B is a photograph of a donor's cheque**, with bank, cheque number and
  account/routing digits legible.
- **6/5/24 Exhibit D (CCTV roster)** carries home addresses, personal phone numbers and
  e-mail addresses for nine named individuals.
Cite RSA 91-A:5, IV — noting it *permits* withholding rather than requiring it — and
reproduce none of the numbers.

## Addendum 16 — August–September 2024 (2026-08-29): 8/21, 9/4, SAU 9/12, 9/18

### Corrections to Addendum 8 — three of them, all arithmetic or attribution
1. **The 8/21/24 title/amendment vote was 5–2, not 6–1.** Addendum 8 says "Petrin was the
   lone No (6–1)" for both. Yes: Skillen, Miles, Hawkins, Crawford, Sprague; **no: Petrin
   *and* Heather Whitney.** Only the **main** motion was 6–1. Source: approved CSB minutes
   8.21.24, item IV.4.
2. **The FY24 encumbrance figures are transposed.** Exhibit B p.22 gives **total encumbrance
   $648,931.76**; $648,931.76 − $65,000 = **$583,931.76**, which matches the two roofs voted
   on 20 June. So $648,000 is the *total* and the roofs are the *difference* — Henry
   transposed them on tape and Addendum 8 repeats it. Consequence: on the exhibit's own
   derivation, a $65,000 encumbrance leaves a budget balance of ~**$1,128,000**, not
   $544,145.29 — a ~$584,000 ambiguity the board never resolved (it worked from **$497,000**
   on 16 October).
3. **"$400,000 from reserves" for the Stevens roof is not supported.** The $420,000 was
   released 6 March 2024 under RSA 198:4-b, II(a), the clerk's read-back confining it to
   "unintentional, unanticipated special education costs". Mary Henry corrected the roof
   attribution **twice on tape** (0:31:43, 0:31:45); a member restated it anyway and **the
   approved minutes adopted her version.**
4. **Addendum 8's ESSER item closes negatively.** The 16 October approved minutes record, in
   full: "Frank Sprague shared that he would still like to see a presentation on ESSER." The
   2 October minutes contain no finance report and no ESSER mention. **ESSER is never
   mentioned at the 4 September meeting at all**, in any garble form, and on 18 September
   Pratt says "we have the end of September to spend the money" — the wrong verb; 30
   September was the *obligation* deadline, liquidation ran to 28 January 2025.
5. **Addendum 8's Whitney-cluster boundaries are End(sec), not Start.** The Start-column
   values are **2578.44 / 2770.80**. Practical consequence: the ADC motion at 2681 s falls
   inside that gap, so the CSV labels it Arlene Hawkins while the minutes credit Heather
   Whitney.

### The district cannot spell its own Student Services director
**McCosker** on the 7 August masthead → **McKosker** on 21 August, 4 September and
18 September → **McCosker** again from 2 October. Same clerk, consecutive documents.
Separately, the dialogue CSV's **"Tina McCusker" is Tina McCosker** (agenda and minutes both
print McCosker) — and she is **not** Michael McCosker/McKosker.

### A FOURTH spelling of the curriculum director, and the first with a title
`CSB Curriculum Sub-Comm. Proposal.pdf` (19 Aug 2024) prints "**Kat McLaughlin, Curriculum
Director**" — against *Cat* (2/21 minutes) and *Catlin* (5/15). Addendum 15's lean toward
Catlin should go back to unresolved.

### New names
**Doug Beaupre** (McGee Toyota donation; garbled as `Mr. Joe Perry` and `Mr. Dupree` in one
hearing) · **Jeff Small, Director of Technology** (SAU 6 central-office masthead from at
least 4 Sept 2024; in no prior addendum) · **Tina McCosker**.

### Capital Improvements changed twice in 2024
Post-3/20/24: Miles (chair), Crawford, Sprague. **At 29 July 2024: Crawford (chair), Miles,
Petrin** — from the committee's own minutes, the only source for this middle state.
September reading (Addendum 8): Miles + Tech Center; Petrin on ad hoc Communications.

### Document defects worth carrying
- **The approved 9/4 minutes misrecord the signatory**: "for the **Superintendent** to sign
  the agreement". The tape has Petrin saying "Our school board **chair** to sign", and the
  Region 10 agreement's clause XIV.3 requires it "signed by the **chairs**", with three
  notarised blocks reading "Chairperson, … School Board" and **no superintendent signature
  line anywhere**.
- **The approved 9/4 minutes state 0.05%** of the Claremont budget. $193,000 ÷ $38,000,000 =
  **0.508%** — ten times larger, and the figure carried the characterisation "It's minuscule."
- **9/4 Exhibit D states the wrong statutory basis** — "Current percentages are based on
  student population per district" — where RSA 194-C:9, I is ½ average membership + ½
  equalized valuation. Henry corrected it aloud; **the document was not changed and the
  minutes do not record the correction**, and the board then sent it to Unity as "It's fact.
  It's data." It landed badly at SAU 6 on 12 September.
- **The Region 10 agreement carries the "Region 17" error twice** (section II, amended; and
  **section IX.2, uncorrected**), a cross-reference at IX.1 to "paragraph 19" which does not
  exist, and a **VII.7 split of regional tuition reimbursement "80% Newport, 20% Claremont"**
  never mentioned at the table.
- **The 21 August approved minutes contradict themselves within four lines** — the amendment
  titles the post "acting assistant CTE director", the main motion says "with the amendment in
  the title to 'assistant'" (plus the typo `Voten taken`).
- **The 7 August minutes style Matthew Upton "Claremont District Attorney"** — New Hampshire
  has *county* attorneys; he is the district's counsel.
- **The by-laws contain two rules numbered 2.09** (see `html_briefing.md` §24g).

### SAU 6, 12 September 2024 — facts for neighbouring pages
- **The 13 June 2024 SAU 6 meeting is confirmed on tape as never held** — chair, 0:36:43:
  "Things were in our packets from the June meeting that we did not hold." MAP §45's negative
  can be upgraded from "no record exists" to "the meeting did not happen, per the chair."
- **The 29 May 2024 SAU retreat was quorate**: 8 of 12 + superintendent + clerk, "Goodwin
  Community Room" (sic — every other document says Goodrich), 6:00–8:00 p.m., NHSBA
  self-assessment + SWOT. No recording, no MAP section; folder `4. SAU Retreat 5.29.24`
  listed unmapped at MAP line 6135.
- **Minutes timeliness (Drive `createdTime`)**: 4/11/24 draft → 2024-09-11 = **106th business
  day** (deadline 4/18/24). 5/29/24 retreat draft → 2024-09-11 = **73rd**. 9/12/24 draft →
  2024-11-08 = **39th**. The `1. SAU6 9.12.24` packet folder was created 2024-09-11, with all
  13 files up ~29 hours before the meeting.
- **Exhibit A reconciles the tape exactly**: budget $2,396,000.00, spent $2,333,830.40,
  balance $62,169.60, encumbrances $21,380.00; less $3,000 locks + $10,000 auditors PO =
  **$49,169.60**. Superintendent's Office salaries **over by $107,204.88** (−23.49%); health
  insurance under by $46,511.22; **Auditors $10,000 budgeted, $0.00 spent**; business-office
  contracted services over by $24,905.87 (−498%); maintenance telephone $4,000 / $0.00.
- **Exhibit G (proposed pre-populated agenda) is the first document implying an executed
  superintendent contract with a term** — under December, "Review Superintendent Contract for
  renewal every 2 - 3 years(due next in 2025)". Never read aloud; absent from the December
  item the chair actually read out. **Still no executed contract in any SAU 6 folder.**
- **Exhibit G, June: "NOTE: No June meeting; bulleted items to be finalized through electronic
  means"** — with "Review of Superintendent Evaluation Results" among the bullets. Flag
  against RSA 91-A:2-a.
- **Exhibit H names the Exploratory Ad Hoc committee's membership: "Supt Christopher Pratt and
  Arlene Hawkins"** — and says it was created at the Claremont board's **7 August 2024**
  meeting, while the chair on tape says April.
- **The superintendent's written report commits to monthly attendance/truancy and discipline
  data (OSS, ISS, bullying and harassment) and IEP/504 totals in September, January and May**
  — a benchmark for every later 2024–25 page.

### New ASR garbles (heard = actual) — dangerous first
`Astro` = **SREB** (full confidence, proper noun) · `head for` / `on all four` / `that's all
for` = **Alt IV** (reads as a number) · `Mr. Peter` / `Mr. Peters` / `Mr. Patron` /
`Mr. Peterson` = **Michael Petrin** (never once correct in the 9/4 file) · `Mr. Kosugi` /
`Mr. Caskey` / `Mr. Costa` = **Michael Koski** · `Miss Kellen` / `miss going` / `still on` /
`the skill` = Whitney Skillen · `Mr. Crawford` = Candace Crawford · `centerpiece` / `son of P`
= **Sunapee** · `Clermont` / `Thurmont` = Claremont · `secretary of Clark` = secretary or
clerk · `policy DEDH` = policy BEDH · `the Dre` = the **DRA** · `the Saw meeting` = the SAU 6
board · `the s a year` = the SAU · `CT director` / `CD director` = CTE director · `Text
Center` = Tech Center · `the front line` = **Frontline** · `crickets` = **Cricut** machines ·
`Eureka two` = Eureka Math² · `targeted inventions` = targeted interventions · `a handsome
instruction, practices` = enhancing instructional practices · `the cotton for the horse` =
cart before the horse · `a shell` = Michelle · `Unity's pants` = Unity's hands · `foot
limitations` = put limitations · `in an act` = in effect · `the tenants in this` = the tenets
· `I'm with the clerk` = over to the clerk · `I want to know why` = I want to notify ·
`the senior student night board` = senior student awards night · `1920 them` = 19, 20 of them.
**Unrecoverable — do not guess:** `Are there witnesses here?` · `buzzsaw into` · `success
bonus` · `Patrick Sky` · `Nice meeting in junction` · `Alex Easter who brought you and pester
and myself` · `I did chalk at request` · `Is 80 S80` / `585` · `There are three schools in
Ireland` · `where we grow the legions. Li.` · `Dave. Jack.` · `Plot up`.

## Addendum 17 — autumn 2024 (2026-08-29): 9/30 joint, 10/2, 10/16, SAU 11/14

### Addendum 8's joint-meeting caution is OVERTURNED — all eight council names are settled
Addendum 8 says only Girard, Manale and "Limoges/Lemos" are defensibly nameable, that the
chair's list "is not parseable into clean names", and that "treating that list as an
attendance record would manufacture people". **The approved minutes (Drive
`1aY0leNEDzk_VGJLu9WsMoCideg5x4zhB`) settle it:** "City Council Members present: **Mayor Dale
Girard, Asst. Mayor Deb Matteau, Brian Zutter, Jonathan Hayden, William Greenrose, Wayne
Hemingway, William Limoges, City Manager Yoshi Manale**." The chair's garbled list names
**exactly those eight and nobody else** — `Gerard`=Girard · `Deborah McGill`=Matteau ·
`Brian Sutter`=Zutter · `Mr. William green. Rose.`=Greenrose (the surname split in two, which
is what made the list look unparseable) · `Yoshi Marnell`=Manale. **It manufactures nobody.**
The minutes also name the councillor behind every question, and those attributions match the
diarizer's clusters nine times over: the 18-row cluster is **Zutter**, the 11-row cluster
**Greenrose**, the other 11-row cluster **Hemingway**, each at three separate points. The
6-row closing cluster is **Matteau** on the minutes' ordering alone — the weaker attribution.
Also settled: `Councilor Lemos` = **Limoges** · `My dad Mattos` = **Matteau** (the CSV Role
field says "THE NAME IS NOT RECOVERABLE") · `micros` = **Mikros** (Addendum 8 lists it as
unrecoverable) · `Mike Peterson` = Petrin.
**The City Council is a nine-member body** (Valley News, 27 Oct 2025), so seven present is its
own quorum — the two bodies met separately in the same room.

### More Addendum 8 corrections
- **`77 years` is settled as 7 years** — the 16 Oct approved minutes print "it is a 7 year
  contract". The "almost certainly" can be upgraded.
- **"Amalia" → Amelia Rhines** (agenda and both sets of minutes).
- **"Lily Clark" → Lilly Clark** in every district document from 2 Oct 2024 (also 16 Oct,
  5 Feb 2025). *Lily* is her self-identification on tape — report the conflict, use the
  district spelling in prose.
- **"Pratt read all four rolls" on 11/14 is wrong: he read three** (attendance 0:00:43; into
  nonpublic 0:04:41; out 0:06:07). **The fourth roll of that evening was Kronberg's, at the
  separate Claremont meeting later the same night**, where she was present, read the roll and
  both roll-call votes, and signed the minutes.
- **Addendum 9's SAU 6 "no tally" claim needs qualifying**: the 11/14 *minutes* record a named
  dissent ("all present voting in favor with the exception of **Kelly Simpson** who opposed"),
  four weeks before the 12/12 counted dissent. The *recordings* carry no tally; the minutes do.

### A FIFTH spelling of the curriculum director
The chair says **`Katlyn`** aloud on 30 September and the minutes print **Catlin**. With Cat
(2/21), Catlin (5/15), Kat (19 Aug proposal) — five renderings. Leave unresolved.
And the 9/30 minutes print **Micheal McCosker** in the agenda body three pages after their
own masthead prints McCosker.

### The ESSER thread, established against the recordings rather than the minutes
- **2 October: ESSER IS mentioned once, at 0:09:13, and it is not in the minutes.** School
  counsellor Amelia Rhines, on summer school: "this was the last summer of the summer school
  staff funding coming from Esser funds. So starting next year will have to be in the Stevens
  High School budget…" No board member takes it up. The minutes render it as "summer school is
  funded by a grant" and contain **no occurrence of the word ESSER**. Addendum 16 §4 should be
  amended: it reads as though ESSER never came up on 2 October.
- **The 18 September minutes — approved by consent on 2 October — promised it**: "Mary Henry
  will share a summary report of ESSER funding and where the FY24 budget stands **in
  October**." On 2 October there was no finance item, no superintendent's report item at all,
  Henry absent, and **none of the four Finance Subcommittee dates printed on that agenda falls
  in October** (12 Nov – 18 Dec).
- **16 October carries a four-turn exchange** at 1:34:32–1:34:58 (Sprague asking for "final
  disposition"; Henry "we just ended on 930… we want to make sure we have everything
  accurate"; Crawford "before we go into the budget season"; Pratt "We won't put behind us at
  this point" — a negation the context does not settle). Plus the **ESSER-grant van** at
  0:57:02, which exists in the record only because Petrin asked.
- **Correction to Addendum 16: 16 October is NOT the corpus's last ESSER mention.** ESSER is
  spoken at 16155, 16157, 16213, 16215, 16222, 16226, 16253 and 16266 — always
  retrospectively ("previously ESSER-funded"). **What ends on 16 October is the board *asking*
  for an accounting.** No later recording contains one.

### The FY24 close is never reconciled
On 16 October nobody speaks $544,145.29, $648,931.76 or $583,931.76. The entire reconciliation
is Petrin's "Does this say these numbers take into account the roofs that we were doing?"
answered "Yes. They're all done." The board works from **$497,000** with no bridge to
September's figure. **The worksheet that would settle it is Exhibit B — cited on the agenda
and in the minutes, and absent from the eight-document packet.** A second arithmetic problem:
Henry states the ceiling as **$466,664.43**; within four minutes everyone says "469" and the
approved minutes publish **"$469,000"** — $2,335.57 above the stated maximum, and the board
twice discussed retaining "the full 469".

### New names and roles
**Amelia Rhines**, school counsellor · **Lilly Clark** · **Kelly Simpson** (SAU 6, the
recorded No on the FY26 raise discretion) · the Exploratory Ad Hoc Subcommittee's participants
are named in 10/2 Exhibit D as "**Supt Christopher Pratt, Arlene Hawkins, Chelsea
Weatherford**", dated 21 Aug 2024, revised 17 Sept 2024 (extends Addendum 16's Exhibit H).

### New ASR garbles (heard = actual) — dangerous first
**`on ceiling previously sealed minutes` = "unsealing previously sealed minutes"** — reads as
a building feature and hides an entire agenda item · **`See it regarding` = "discussion and
vote regarding"** · **`LED by Marjorie Erickson` = "led by"** (dangerous: the same meeting has
an "Affinity LED Lighting" item) · `Miss Cronenberg` = Noelle Kronberg · `Assistant
Superintendent Kosky` = Michael Koski · `Policies BED. B.` = policy BEDB · `Policy HAC` =
policy EHAC · `K. E b.` = policy KEE · `Miss Rhymes` = Rhines · `Bonnie Myles` = Miles ·
`Choose the` = "She's the" · `Tell me a motion` = "I'll make a motion" · `the River School
Board` = Oyster River · `the ethical and sustainable fix` = "the equitable and sustainable
tax" · `their do` = "their dues" · `Jack and Dorothy Brand Foundation` = **Byrne** ·
`930` = 30 September. **Unrecoverable — do not guess:** `blank mount` (probably "blanket
amount") · `2501 0000000` · `to a dot. Dot be done.` · `Brian Souter` · `Police Chief
Walmart` · `Sue car` · `and ally` · `City Management, Olli` · `Below average council` ·
`Bill. The newest newbie`.

### SAU 6, 14 November 2024 — the sealed-minutes review, and what it omitted
Item IV.4 was **added by amendment at 6:31 p.m.** and is not on the posted agenda. The board
went nonpublic under RSA 91-A:3, II(a) and (m) and voted **in public session** to unseal eight
sets: 13 Jul 2018, 14 Jun 2018, 10 May 2018, 17 Jul 2018, 13 Apr 2023, 11 May 2023, 31 Jul
2023, 17 Aug 2023. Chair: "These minutes will be posted within 72 hours on the website."
**Nothing from 2024 is on that list — the 11 April 2024 six-month seal is missing**, its term
having lapsed 11 October 2024, 34 days earlier. The Policy Committee's own review, announced
for **2 October** and required by BEDG D.5.b to be "in a duly noticed meeting in full
compliance with RSA 91-A:2", has **no notice, agenda, minutes or recording anywhere**, and the
**Sealed Minutes List** BEDG D.4 orders published does not exist in any share.

### SAU 6 FY26 budget, and the contract
FY26 proposed **$2,794,151.54** against FY25 **$2,489,151.00**. The sheet's "Total Budget %
Increase 7.23%" is **net of $125,000 of revenue**; the gross increase is **$305,000.54 =
12.25%**, which the superintendent had to prise out ("the real number isn't really 180,000" /
"No it's 305"). Controls visible in the ledger: FY23 mileage paid exactly $2,500.00 on two
lines, **FY24 $0.00 on both**; the $4,000 maintenance telephone line is $0.00 in every FY25
and FY26 column; **Auditors $0.00 in FY23 and FY24** against three unaudited years.
**The contract's whole November trace is one sentence** — the chair at 0:29:39: "We also have
to go over the superintendent's contract, which we did not have a chance to discuss tonight."
**Neither the 3 December nor the 12 December SAU 6 agenda carries a superintendent-contract
item**, and 3 December failed for want of a quorum. Exhibit G's December line never became an
agenda item. Still no executed contract in any SAU 6 folder.

## Addendum 18 — November–December 2024 (2026-08-29): 11/20, SAU 11/21, 12/4, SAU 12/12

### THE SUPERINTENDENT'S CONTRACT — RESOLVED, off-agenda, on 12 December 2024
Addendum 17 says "the contract's whole November trace is one sentence" and that neither
December agenda carries an item. Both true — **and the contract was transacted anyway**, at
the SAU 6 budget hearing, **43 seconds after the nonpublic session**: the chair moved "the 3%
salary increase for the superintendent", Whitney seconded, Crawford added the term, the chair
restated it as "for a two year contract? So for this year, it's 3% increase. And to renew your
contract for two years." Voice vote, no count. **Still no executed instrument in any share.**
This closes the thread opened on 11 January 2024, when terms were "expressly delegated… for
subsequent approval" — eleven months, and the approval never took the form of a document.

### Addendum 9 corrections
- **"No draft minutes exist for 12/3/24 or 12/12/24" is right about publication, wrong about
  existence.** The **10 April 2025 draft SAU 6 minutes** (Drive `1KcmceeO49Fd392oO_RBk86who2DyTLkT`,
  in `6. SAU6 6.12.25`) record: "Heather Whitney made a motion to approve the minutes from
  12.12.24 as presented, Michael Petrin seconded the motion", voice vote, all in favour.
  Written, circulated and approved **119 days** after the meeting; never published. MAP §63
  should read: *no minutes published in either share; the 4/10/25 draft records their approval
  on 10 April 2025.*
- **The `3.53 to 12.75` NHRS garble is SETTLED**: the packet's `SAU FY26 Budget Summary
  12-2-24` reads "NHRS decreased from **13.53%** to 12.75%."
- **Sprague's biography — external support for the merge reading.** The approved 12.4.24
  minutes give three turns of the CSV's Speaker 7/12 cluster to **Michael Petrin**, including
  the answer that runs continuously into "I only have an associate's degree", and the point of
  order at 1:21:02 where one CSV segment carries both "That's my motion." and "Kind of a point
  of order question." Same class: the **Speaker 6/11 cluster (filed Arlene Hawkins) probably
  also merges Bonnie Miles** — the same minutes give two of its questions to Miles. **A human
  should rule before either CSV is changed.**

### The 13 February 2025 SAU 6 meeting was CANCELLED — not a corpus gap
Fixed on the 12/12/24 recording at 1:08:10 and on the 3 December agenda. The 4/10/25 minutes:
"there was a previous agenda item for 2020 and the report was received, but the meeting was
cancelled"; the board then heard the **2021** audit and resolved to meet "on an as-need
basis". That explains the six-month folder gap. **No MAP section is owed.**

### The SAU 6 treasurer office was vacant through 2024–25
4/10/25 minutes: "Arlene Hawkins noted that the SAU Board currently has no treasurer",
prompted by auditor **Michael Campo** ("the treasurer should review the check register"); the
board then elected **Candace Crawford** treasurer plus two voucher signers. With the 15687
page (11 April 2024 elected only chair and vice chair) this closes RSA 194-C:5, I for 2024–25.
And the **$3,600 "Wages School Board Secretary" line is the CLERK's** — "That's your board
clerk. Yes. Okay, I can change that from board side." That answers the 14 December 2023
page's flag 2.

### SAU 6 FY26 — three budget versions, and the number that was adopted is in none of them
| | gross | vs FY25 $2,489,151.00 | printed on the sheet |
|---|---|---|---|
| V1 (14 Nov) | $2,794,151.54 | +$305,000.54 = **12.25%** | 7.23% |
| V2 (3 Dec, never presented) | $2,793,874.48 | +$304,723.48 = **12.24%** | 7.22% |
| V3 (adopted from) | $2,597,521.45 | +$108,370.45 = **4.35%** | **−0.67%** |
| **Adopted, spoken aloud** | **$2,755,723** | **+$266,572.00 = 10.71%** | — |
The headline **crosses zero** — the sheet advertises a decrease on an appropriation that rises
by a tenth — and the comparison is **net FY26 against gross FY25** (the FY25 ledger in the same
packet foots to $2,489,151.00 with no revenue lines). **$2,755,723 appears in none of the eight
packet documents**; the business administrator produced it orally ("Are you ready. 2,755,000.
Make it even $723."). Against FY24 *actual expenditure* it is **+18.06%**.
**In the whole 55½-minute hearing no total, no increase and no percentage was ever stated
aloud** — `2,794 / 2794 / 2,489 / 2489 / 7.23 / 12.25 / 305 / 180 / apportion` appear nowhere
in the 489-row CSV. The chair asked at 0:39:34 and got "I would have to figure that out
because I don't know."
The real cut is **V2→V3, $196,353.03** (Henry's "roughly $197,000"): −$153,195.67
superintendent's office, −$51,697.72 business office, +$8,637.55 technology.
**The counted dissent**: Crawford moves $2,755,723 at 1:03:48, the chair's own row carries the
second, and at 1:04:06 — "Opposed? One. And any abstentions. Okay." **One opposed, ayes
uncounted, no name, no minutes.** The dissenter cannot be identified by anyone.
Addendum 17's $166,460.62 is **Kelly Simpson's spoken figure** and omits the Info Mgt Services
salary line (+$4,540.10); the unit-wide FY26 composition is salaries **$171,000.72**, health
**$89,254.66**, software **$10,694.90**, other **$34,050.26** = $305,000.54.

### More FY25 SAU 6 ledger controls
HR cell phone **$1,000.00 spent against a $0.00 appropriation**; business office $2,000 vs
$1,000; superintendent $2,500 vs $2,100; SPED mileage $1,439.07 vs $1,250 (the 4/10/25 minutes
concede it "should have been budgeted for $2500"); Supt Dues & Fees $10,853.64 vs $8,450;
SPED Supplies $3,301.48 vs $600; negative FY24 actuals of ($5,907.78) and ($241.95); **Supt
Office Salaries FY24 actual $570,258.79 against an FY25 budget of $475,229.15.**

### Notice regression at SAU 6
The **whole 12/12 packet folder was created 3:59 p.m. Eastern on the day of the meeting**,
agenda 4:01, the adopted budget V3 **4:03** — about 2½ hours before the gavel. The 3 December
agenda went up at **11:13 a.m. on its own meeting day**. Against 14 November's six days and
14 December 2023's thirty-one hours. The 11/21 packet: folder 1:51 p.m., both files 2:00 p.m.
— four and a half hours before a 6:30 start.

### The 21 November 2024 SAU 6 special meeting
No quorum at 6:30, so the DMGroup presentation ran **before the gavel**; called to order at
0:44:57, adjourned at 0:50:40 — **five minutes fifty seconds of meeting after forty-five
minutes of business**. Citizens' comment was noticed on the agenda, recorded in the minutes as
"none", and **never called**, while members of the public were in the room and had been
speaking. **Both the agenda and the minutes head their bodies "SAU#6 School Board November 14,
2024"** — the previous meeting's date. And the strategic-planning **Working Committee's board
membership changed between June and November with no vote or minute anywhere**: June (Exhibit
F slide 14) Crawford, Hawkins, **Sprague**, Erickson; November (adopted plan p. 5) Crawford,
Hawkins, **Whitney**, Erickson.
Defects inside the adopted plan: oversight assigned to "the Board of Education", a body NH
statute does not create at district level; the Appendix defines chronic absenteeism as "10 or
more unexcused absences in a school year" while the presenter said "10% of or more of the
school year" (0:15:14) and the adopted measure carries neither; the Fast Facts page classifies
**SRVRTC as "1 Alternative Program"**; and one measurable goal is "**Decrease the number of
bullying and harassment investigations**" — a count of the district's own responses to reports.
**No contract, engagement letter, purchase order, cost figure or vote of either board relating
to District Management Group exists anywhere in this corpus** — announced 15 May 2024 as
settled, called ESSER-funded and "budget neutral" on 5 June, with Phase IV dated "December
2024 - Ongoing", *after* the 30 September obligation deadline. The FY26 SAU 6 budget carries
**$23,800.00 of contracted services in total, every line unchanged from FY25.**

### New names
**Malachi Caple** (SHS junior, class VP — surname from the approved minutes only) ·
**Sarah Wheeler** (SHS senior) · **Matt Hammond** (SHS psychology teacher) · **Colleen
McIntyre** (SHS coach) · **Courtney Steele** (CMS coach) · **Samantha Miller** (HR
Coordinator from 2 Dec 2024) · **Michael Campo** (auditor).

### New ASR garbles (heard = actual) — dangerous first
**`the city` / `the state` / `the seat` = the SAT** and **`the CT` / `the PS` / `the PS 80` =
the PSAT** — a "city" that is a test, in a corpus with a City Council · **`admitting during`
= "admin just ignoring"**, **`Avenue` = "admin"**, **`feel heard` = "feel unheard"**,
**`I can't hold myself to a high standard` = "I hold myself to a higher standard"** — the last
three are **dropped or inverted negations**, settled by the packet PDF; quote as recorded and
never repair · `Does not` = **Disnard** · `smiles` = **Miles** (the mover naming herself) ·
`Mr. Blue` = **Mark Blount** · `Rocco and Roger from unity` = Rocco Ruggeri · `RSA 91-8` =
91-A · `nonpublic prayer` = nonpublic per · `the pleasant Regency` = Pledge of Allegiance ·
`a a season` = ACA season · `the see I see` = the CIC · `the Sri` / `the SRE` = SREA ·
`Sussex` / `saw six` / `Siu six` / `C six` = SAU 6 · `a code printed` = co-plaintiff ·
`the calm down` / `convey a` = ConVal · `other essays` = other SAUs · `an Saw board` = an SAU
board · `assistant comments` = citizens' comments · `three meters` = three meetings ·
`our problem` = our prom · `Merica` = America · `Malik, I` = Malachi · `Chelsea Warren` =
Chelsea [Weatherford] *warn* · `handsome out` = hand them out · `extra day` = extra duty.
**Unrecoverable — do not guess:** `And the King's Speech.` · `make sure that map` · `an even a
zero` · `Teal in teal room` · `Humbleness just.` · `the lack of said` · `saving answers for
funding education` · `And it crops the deposits` · `our customers`.

### A SIXTH rendering of the curriculum director
`Katlyn` (spoken, 30 Sept and 20 Nov) vs `Catlin McLaughlin` (packet exhibit) vs `Cat
McLaughlin` (minutes) — **three in one meeting's own documents**, six across the corpus.
Still not settled. Print no spelling as fact.

## Addendum 19 — December 2024 and October 2025 (2026-08-29)

### The FY26 Claremont budget: what actually happened, against what the corpus assumed
- **18 December 2024 is NOT where the budget was moved to hearing.** No budget figure of any
  kind was moved or spoken at the board meeting. The motion "to move the budget as presented
  forward to the public hearing" was made by **Michael Petrin, seconded by Frank Sprague, on
  7 January 2025** (approved 1.7.25 minutes, Drive `12BumGchXlwAnFHPLJt75jXTZPze6e2Us`).
  Addendum 9 had this right.
- **The two 18 December meetings, ordered.** The **Finance Committee came first**, by five and
  three-quarter hours: Cablecast gives show 16226 an `eventDate` of **2024-12-18T12:50:39-05:00**
  with the show record created a minute later, against show 16222's date-only stamp and a
  6:30 p.m. agenda. Sprague on tape: "tonight we're going to give them just a thumbnail of
  where we're headed."
- **The committee reached a number and none of it reached the board's record.** Fully loaded
  FY26 increase **5.5%** on the FY25 base of **$36,349,753** (draft **$1,128,543** over after
  revenues, **8.91%** gross, ~**$800,000** for two unratified CBAs). Then: Sprague "Well, I'm
  going to throw out 4%" → Whitney "We want the total number to be a 4% increase" → Crawford
  "Just fine. Just find me 200,000" (≈4.5% fully loaded) → Pratt "I mean, you got our orders."
  **No motion, no second, no vote, no roll call, no adjournment.** The approved 12.18.24 board
  minutes dispose of the Finance item in three sentences telling the public to watch the CCTV
  recordings.
- **One figure moved the other way, and it is the sharpest fact of the day.** At ~2:24 p.m. the
  chair asked the committee for the default budget and was told "I'm working on that tonight…
  I will get you a rough estimated number"; at ~7:25 p.m. the board was given **$39,791,261,
  to the dollar**. It appears in no document in either packet.
- **FY26 default trajectory**: $39,791,261 (18 Dec) → **$42,772,778** (15 Jan approved hearing
  minutes) = **+$2,981,517, +7.49% in 28 days** after "some minor changes". Proposed FY26
  **$42,933,564**, i.e. **$160,786 above the default** — reversing the December expectation
  that the default would exceed the budget. Against the FY25 general default $35,906,773.87:
  December +10.82%, January +19.12%.
- **§16's RSA 40:13, IX(b) truncation confirmed independently**: Henry read the definition
  aloud almost verbatim and **stopped before "and by salaries and benefits of positions that
  have been eliminated in the proposed budget"** — in the year the district eliminated PreK
  (~$500,000 / 23 identified students, per the 7 January minutes). **No default-budget form
  exists in the December packet or in the 15 January hearing packet.**

### The retention: "$469,000" is the CEILING, not the amount retained
Addendum 17 needs this correction. The approved 16 October minutes read "The maximum that can
be retained is $469,000", and the board voted **"Frank Sprague made a motion to retain up to
$350,000 with the stipulation that it be used to offset the 25/26 tax rate."** A page saying
the board *retained* $469,000 would be wrong. The $466,664.43-vs-$469,000 ceiling discrepancy
stands. **That $350,000 was earmarked for FY2025–26 — the budget built on 13 December — and is
never mentioned in it.**

### The FY24 close figures, refined
The approved **18 September** minutes do not print $544,145.29. They print "At about
$540,000", "Down about $60,000 after roof projects and others; could change", and "a revenue
surplus at about $210,000". The **16 October** minutes print "there is a surplus of $497,000,
plus an additional $114,000 in additional revenue for a total of $611,000." **So $544,145.29
is an EXHIBIT figure, not a minuted one** — say so wherever it is carried. Nothing on
18 December advances the reconciliation; the retention is closed in four lines ("We've already
voted on that").
New: the Capital Improvements minutes of 10 Dec list **"SHS Roof Replacement, final section
$96,000"** and, two paragraphs later, **"the third phase of the SHS Roof Repair at $98,000"** —
one item, two prices — against 16 October's "Yes. They're all done." Capital Improvements
Reserve Fund balance **$150,000**.

### The 13 December 2024 Finance session WAS announced on camera — nine days ahead
This corrects the assumption that it was wholly unnoticed. The 4 December recording
(1:08:04–1:12:30) and the **approved 4 December minutes**: "Ms. Henry had emailed Frank
Sprague to ask to meet with the finance committee on Thursday next week and then a second
meeting on Friday to be televised." Hawkins asked on camera "Will the Friday morning be
publicized? Is that televised?" and Sprague instructed "Can you let Chelsea know so she can
get it out." **What remains not found is any posted notice.** The published date lists — five
district documents, starting with the approved 18 September minutes — give **Nov 12, Nov 19,
Dec 4, Dec 18, all 1–3 PM**. **13 December is on none of them, and it was a morning meeting.**

### Addendum 9 closures
- **12/18/24 attendance**: present Whitney, Sprague, Miles, Crawford, Petrin, **Hawkins
  (arrived 6:33)**; absent Skillen. The chair's unnamed late arrival is Hawkins. **Bonnie Miles
  is recorded present and speaks zero attributed words.** Kronberg absent; Mary Henry read the
  roll.
- **`Eric Perry`** is **Eric Perry, Newport Tech Director** — `CSB Visioning Sub 12.9.24.docx.pdf`
  (Drive `1iUvor8hyFQp6Zl9-94kqfzj6VAMmMCni`). The approved board minutes say only "the
  Director of the Newport Tech", so this packet document is the sole district source.

### Autumn 2025 — a roster and a crisis the corpus had not recorded
**10/6/25 agenda masthead**: Whitney (Chair), Petrin (Vice Chair), Hawkins, Crawford, Madden,
**Loren Howard**; Clerk Kronberg; **seventh seat vacant** (Sprague's; a 3–3 deadlock on
1 October, tabled). Central office: **Kerry Kennedy (Interim Superintendent)**, Michael Koski
(Asst Supt), Matt Angell, Patrick O'Hearn, Jeff Small, **Mary Henry** — Henry is on the 10/6
masthead and **gone from the 10/15 one**, where Kennedy announces her **unpaid disciplinary
suspension**.
**The clerk's maternity leave left the board with no minute-taker for six weeks.** Three people
called the roll in a fortnight: O'Hearn (10/1), Whitney (10/6), Angell (10/15). On 15 October
the district advertised publicly for a transcriber at **$300 per meeting**; the 12/3 approved
minutes thank **Sherry Williams** for the backlog. **10/6 was never in it** — no minutes exist
and none were ever approved.
**The 10/15/25 draft minutes are an unmined source**: Henry's suspension, Weatherford acting
HR manager, Jennifer O'Neil interim CMS principal, Howard attending virtually, tax-rate options
of 9.18% / 6.08%, and **a ten-cent-per-meal written agreement signed by the former business
administrator that the board had never approved**.

### New names
**Alyssa Brenner** (SRVRTC Medical Assistant teacher) · **Scott Pope** (SRVRTC long-term sub) ·
**Career Counselor O'Neill** (tape: "Jan O'Neil"; no document gives a first name) · **Steve
Holt**, Maintenance Director · **Thomas Smith-Knox**, CMS chorus · **Courtney Porter**, social
worker · **Eric Perry**, Newport Tech Director · **Sherry Williams**, transcriber · **Loren
Howard** (not Lauren) · **Kerry Kennedy**, Interim Superintendent · **Jennifer O'Neil**,
interim CMS principal · "**Jessica**", out-of-district coordinator, first name only.
**Michelle Herrington's title is given three ways in one packet** — "Tech Director",
"Assistant Director", "Ms. Herrington"/"Ms. Harringont". **The approved 12/18 minutes use both
*Mimi* and *Amelia* Rhines in one document.** The December Superintendent's Report prints
**both "Cat" and "Catlin McLaughlin" on one page** — the curriculum director's name is still
unsettled at six renderings. **A new two-spelling name: `Jessica McLeod` (CSV and two shipped
pages) vs `Jessica McCleod` (the district's own 10.15.25 draft minutes).**

### New ASR garbles (heard = actual) — the fused-digit class first
**`378 minute classes` = three 78-minute classes** · `178 minute prep` = one 78-minute prep ·
`646 minute classes` = six 46-minute · `146 minute prep` = one 46-minute · **`$57,592,
852,500 and 857,000 $357,592` = a single $857,592.** Any impossible number is probably two.
**`jet services` = debt service** and **`We use to increase` = "reduced and increased"** —
both inside a verbatim reading of RSA 40:13, IX(b) · **`Andy Crawford` = Candace Crawford**
(the phantom-first-name trap, in the chair's own introduction) · `for policies` = four
policies · `policy BEED` = BEDH · `Mr. Smith, knocks` = Thomas Smith-Knox · `Miss Ryan's` /
`rhymes` / `Miss Rhimes` = Rhines · `the s report` = the SREB report · `DC wife` = DCYF ·
`a Chins` = CHINS · `Leah` / `L a` / `li e a` = LEA · `an saw` / `6SA6` / `the essay costs` /
`saw` / `say you six` = SAU 6 · `the SRA` / `the SRE` / `the Sri` = SREA · `Disney art` /
`Disney` = Disnard · `offset the texts` = taxes · `the sports` = supports · `Doctor Herron` /
`Doctor Michael Harrington` = Dr. Michael Herrington · `Frank Spriggs` = Sprague ·
`Whitney Skilling` = Skillen · `Michael Patron` / `Mike patron` / `Mr. Peter` / `Mr. Peterson`
= **Petrin, never once correct in any file** · `did me today` = did meet today · `aspire
safety` = a fire safety · `Forevers watching` = for whoever's watching · `Any objections to
joining` = adjourning · `math precision proficiency` = math proficiency · `Speaks committee` =
Finance committee · `Lauren Howard` = Loren Howard · `Mr. Kosky` = Michael Koski ·
`medical detectors` = metal detectors (in the same breath as the correct form) · `the Dow` =
the SAU office.
**Unrecoverable — do not guess:** `Sniper.` · `Mr. Crowder` / `Mr. Free` · `Miss Kestner` ·
`Is it all the data for you to have?` · `It's not an H anymore` · `It's 25025256 estimate` ·
`the 1010 3115` · `the Clarence Surprise` · `debris of angles` · `high school is in the cheap`
· `regular at a loan` · `their Institute of Justice model` · `The Oscar` · `That out of your
land` · `we can strengthen back to` · `Now, Tyler, take it away` · `the next female member` ·
`So this would be a subsidy we have to do`.

### Two negation-shaped passages, quoted as recorded and repaired nowhere
Pratt 0:55:58 (16226) "And we just gone to the days that we were allowed…"; 1:20:16 "we can't
I can't in good faith say…". Joins the three settled by packet PDFs in Addendum 18.
