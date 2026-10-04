# create-html run briefing — 2026-08-28

Shared contract for the 78-page backlog run. Read this IN FULL before your meeting.
It carries corrections to the skill's own reference files and to earlier briefings.
Where this file and the skill disagree, **this file wins** — it is newer.

---

## 1. Two hard rules

**Quote the source, don't improve it.** The pilot found all three agents silently
cleaning up ASR text while quoting it. That is the single defect most likely to
discredit the project. The convention:

- **Brackets mean insertion or correction, and the garbled wording stays visible
  whenever the correction changes sense.** `[ESSER] monies` is fine when the source
  says "SR monies" and the meaning is obvious. `"school boys" [boards]` — keep both,
  because a reader skimming needs to see that the transcript says something else.
- **Stutters may be condensed unmarked.** "we have a, a line" → "we have a line" is
  allowed. Nothing else is.
- **A dropped negation is NEVER supplied.** If the transcript reads "we can do that"
  where context says "can't", quote it as it stands and say so in the surrounding text.
  Supplying the negation invents a vote.
- **Quotations from the agenda, minutes or a statute must be attributed to that
  document**, not left to read as speech from the recording.
- State the convention in one sentence in the method footer.

**Name only what you can defend.** An unnamed voice is "Unidentified" plus whatever
role you can establish. A wrong name is far worse than no name.

## 2. Run `verify_quotes.py` — it is not optional

```
python3 Scripts/verify_quotes.py "Output/HTML/<base>.HTML" "Output/HTML/Dialogue/<base>.CSV"
```

It reports every quoted fragment that is not in the dialogue CSV. **Each one is either
a legitimate agenda/minutes/statute quotation — in which case the page must attribute
it to that document — or a transcript quotation you cleaned up, which you must fix.**
Work through the whole list before you deliver. It is stutter-tolerant and handles
both bracket styles, so a hit is a real question, not noise.

Also run `scripts/validate_pages.py` (structure, anchors, timestamps) and fix everything
including its `note:` lines.

## 3. CORRECTION: who was superintendent

**Michael "Mike" Tempesta was Superintendent of SAU 6 from July 2019 until he was fired
11–12 January 2024.** Any 2023 recording has Tempesta. An earlier briefing in this run
wrongly said Chris Pratt was acting superintendent in 2023 — that is **wrong**, and the
pilot caught it from the primary sources.

- **Chris Pratt** was Stevens High School principal through 11 January 2024, became
  **interim** superintendent that night, and was made permanent ~22–23 May 2024,
  effective June 2024, formally recognised by the SAU 6 board 9/12/24. Never write
  "interim" for anything after May 2024, and never write "Superintendent Pratt" before
  January 2024.
- The 9/6/23 packet's "Questions for B. Nester" and "Questions for C. Pratt" are **not**
  a superintendent search.

`Scripts/briefing.md` (1,311+ lines, eleven addenda) is the authority on rosters, ASR
garbles and diarizer behaviour for 2023–26. **Addendum 2 covers the 2023–24 roster.**
Read the addenda covering your meeting's date before you name anyone.

## 4. CORRECTION: legal anchors have vintage problems

`Scripts/pending_legal_anchors.md` carries anchors verified in the pilot plus three
corrections you must respect:

- **RSA 186-C:18, III** — the skill's catalog claims an "80%-of-entitlement floor" on
  catastrophic-aid proration. **That floor did not exist before 2025** (added by 2025
  N.H. HB 2 §137). Citing it against a pre-FY2026 meeting would wrongly accuse the State
  of breaking the law. There is also **no 90% figure** anywhere in that section.
- **RSA 198:40-a** — current per-pupil dollar amounts are post-2023 amendments. For an
  earlier meeting cite the NHDOE year explainer, not the statute.
- **Title IX** — eCFR serves the 2024 rule. Meetings before August 2024 need the 2020
  rule at 85 FR 30026.

**Rule: before citing any provision whose dollar amount, percentage or deadline carries
the flag, check what it said on the meeting's date.** Roughly half this backlog predates
the 2025 and 2026 session laws. When in doubt, cite the year's NHDOE/DRA guidance
instead of the statute, or label the point an OBSERVATION.

You may verify NEW anchors — fetch the primary source, confirm the holding, cite it.
**Never invent an RSA number.** Report every new anchor in your final message; do not
write to the skill's `references/legal-anchors.md` (it is a read-only cache that is
discarded when the session ends, and concurrent agents clobber each other there).

## 5. Severity rule for missing records — decided by the user, apply consistently

The corpus currently grades the identical "no agenda, no packet, no minutes" fact both
HIGH and MEDIUM. From now on:

- **HIGH** where the absence is unmitigated: a public body met, and no minutes exist in
  any district share, with nothing on the record explaining it. RSA 91-A:2, II sets five
  business days; RSA 91-A:1-a, VI(d) makes a subcommittee a public body. A years-old gap
  is a missed statutory deadline, full stop.
- **MEDIUM** where the record mitigates it: someone on tape says minutes exist elsewhere
  or are coming, the body lacked a quorum and transacted nothing, or the meeting was
  noticed and packeted and only the minutes are missing.
- Say which limb you are applying and why, in the flag text.

**A page with no HIGH flag is a valid outcome.** Do not manufacture one.

## 6. SAU 6 minutes: search two stages before writing a negative

The SAU 6 share files a meeting's minutes with a **later** meeting's packet, and the lag
can be long — the 4/11/24 draft turned up in `1. SAU6 9.12.24`, **154 days on**, after an
earlier folder-scoped check wrongly reported it missing. Before writing "no minutes":
check the meeting's own folder, then **every** later SAU 6 folder by filename date, then
the Claremont Meeting Minutes share (which has never held an SAU 6 file). If you still
find nothing, say the search was two-stage and name the folders checked.

## 7. Page length

**Density follows the source — there is no size cap.** A 1,762-row meeting earns a
longer timeline than a 60-row one. Do not pad, and do not trim material the public
record depends on: for the finance and SAU 6 meetings there is often no agenda and no
minutes, so your timeline is the only public account of what was said. Pilot pages ran
115–122 KB against a 61 KB corpus average and that was the right call.

## 8. Small things the pilot learned

- **Same-second link collisions:** consecutive CSV rows can share a truncated second, so
  a `seekto` may land one row early. Take the `Start (sec)` integer and render the visible
  `H:MM:SS` from that same number — text and link then cannot disagree.
- **Add a "Board composition" row to `<dl class="facts">`** for any meeting with a vacancy
  or mid-year roster change; six-versus-seven members is otherwise invisible.
- **Maintainer disclosure:** Kevin Tyson maintains this project. Where he appears in a
  meeting's records, say so plainly in the footer and report the record with exactly the
  neutrality you would apply to anyone else. Where he does not, the existing footers say
  "Kevin Tyson maintains this project; his name does not appear in this meeting's records."
- **Four sections have no Cablecast recording** (12/3/24, 8/21/25, 8/26/25, 5/28/26 SAU 6).
  They are not on your worklist. If MAP.md has no `Remote video:` line, print plain
  timestamps and note it in the footer — never guess a show URL.

---

## 9. Corrections found by pages already built (append as you find more)

- **`Scripts/briefing.md` Addendum 2 dates the 2023 deliberative session 2/10/23. It was
  2/8/23** (snow date 2/9) — per the warrant in the 2/1/23 packet, the agenda, Addendum 3
  and MAP.md §2. Trust the packet over the addendum here.
- **MAP.md's note on the twin 2/1/23 recordings says "825 vs 774 segments".** Those are
  transcript segment counts; the dialogue CSVs hold **816 and 768 rows**. Use row counts
  when describing the CSVs.
- **RSA 188-E:9-a is NOT the CTE construction-funding statute** — it covers charitable
  donations and the BPT credit. Do not cite it for building-aid splits; report such
  figures as the speaker's characterization unless you verify the real provision.
- **34 CFR 106.30 now 404s on eCFR** (the 2024 Title IX rule replaced it). For a
  pre-August-2024 meeting quote the **2022 CFR annual edition** on govinfo.gov instead.
- **Ed 306.17 "Class Size" was the number in force through 2024**; it was renumbered to
  **Ed 306.14 "Student-Educator Ratios" effective 12-13-24**. Cite the numbering that
  existed on your meeting's date.

## 10. Scratch files: use a per-meeting path

**`/tmp/cond.txt` and similar shared names are a real hazard.** During wave 1 one agent's
condensed dialogue was overwritten by a sibling working on a different meeting; it read
~230 lines of the wrong meeting believing they were its own and began drafting a
treasurer election and a procurement discussion that never happened at its meeting. It
caught the swap on a length mismatch.

Write every scratch file to a path containing your meeting's base name, e.g.
`/tmp/gtp-<BASE>/cond.txt`, and **treat any `/tmp` file you did not just create yourself
as untrusted**. If a dump looks longer, shorter or thematically wrong for your meeting,
re-dump before reading further.

## 11. Confirmed: RSA 91-A:2, II's mover/seconder clause applies to EVERY meeting here

Independently re-verified three times in wave 1 against the 2017 and 2019 codifications.
In force from **2018, 244:1, eff. January 1, 2019**. Every meeting in this corpus is later
than that, so minutes that omit a mover or seconder are a real defect and should be
flagged — not excused as pre-dating the requirement. What 2025, 112:1 added (start time,
end time, who produced the minutes) genuinely is later and must not be applied before
August 22, 2025.


## 12. A FIFTH vintage trap, and a catalog correction

**RSA 35:9 (capital reserve funds) was amended by 2023, 36:2, effective July 16, 2023.**
The text gc.nh.gov serves today is not the text in force for any meeting before mid-July
2023 — which is every 2023 meeting through the 6/21/23 board and 7/13/23 SAU 6 sessions.
Joins the four traps in §4 and Addendum 11 (RSA 186-C:18 III, RSA 198:40-a, Title IX,
RSA 198:20-b).

**The catalog's quotation of RSA 91-A:1-a, VI(d) is truncated.** It stops before the
operative clause. The full text ends: "…or other political subdivision, **or any committee,
subcommittee, or subordinate body thereof, or advisory committee thereto**." That trailing
clause is what actually carries every subcommittee flag — quote it in full.

## 13. Two research traps that nearly produced misattributions

- **"Policy Committee" minutes in Drive are the CITY of Claremont's committee** (cemeteries,
  DPW, mobile food units), not the school board's. A title search surfaces them. Using them
  as board subcommittee minutes would be a serious misattribution.
- **Chris Pratt says "when I was superintendent there" on the 4/19/23 recording** — of
  Bellows Falls, before Claremont. It is a live trap for §3's correction: he is NOT
  Claremont's superintendent in 2023, and that sentence does not make him one.

## 14. Student privacy — do not reproduce what the district exposed

The 5/3/23 packet's Special Education Director's Report carries an appendix listing
individual students by **full name and grade** under headings naming a disability basis,
published in the district's public Drive folder. **Reproduce no name, grade or count from
any such document.** Describe the exposure, cite FERPA (34 CFR 99.3, 99.30(a); 20 U.S.C.
§1232g(b)(1)) and IDEA (34 CFR 300.622(a)), and flag it — but the page must not become a
second copy of the disclosure. Grep your finished page against the names to be sure.

## 15. Budget-season corrections (folded in 2026-08-29, after the December 2023 – January 2024 wave)

These come from four pages built on 12/14/23, 12/18/23, 12/20/23 and 1/3/24. Several were
errors in **my own task briefs**, so do not assume a figure in your brief is checked.

**a. RSA 32:5 — get the paragraph numbers right.** The correct mapping, verified against
both the current text and the **2023 codification**:

| Requirement | Paragraph |
|---|---|
| At least one public hearing, **not later than 25 days** before the meeting, 7 days' notice, **"and after the conclusion of public testimony shall finalize the budget"** | **I** |
| Appropriations stipulated on a **"gross" basis** | **III** |
| Budget forms carry **comparative columns** (prior year appropriated / actual) | **IV** |
| Special warrant articles appearing in the warrant | V |

Earlier pages in this run said gross basis was ¶IV and the columns ¶V. **That is wrong by
one paragraph.** If you cite either, cite III and IV.

**CLEARED 2026-08-29.** All 40 shipped pages carrying `32:5` were audited paragraph by
paragraph; every citation is now correct, including the range citations. **Do not "fix"
a 32:5 citation you find on an existing page** — they are right.

**b. ¶I's finalisation clause is the answer to "they changed the number after the hearing".**
Paragraph I expressly contemplates the body finalising the budget *after* public testimony
closes. A reduction voted after the hearing — the post-hearing $196,001.10 cut, for example —
is therefore **the statute working as written, not a violation**. Do not flag it as one.
This clause was in force throughout the corpus: ¶I's current wording predates the only recent
amendment (2025, 144:1, eff. Aug. 30, 2025) and appears verbatim in the 2023 codification.

¶II independently confirms it: its bar runs only against **insertions**, so a reduction
cannot breach it either. A post-hearing cut is lawful twice over.

**CLEARED 2026-08-29.** No shipped page flags a post-hearing reduction as a violation.
Every post-hearing mention in the corpus concerns ¶II insertions, correctly.

**c. The 25-day rule is a *floor* between hearing and meeting** — it is not a December 31
deadline, and the two must not be blended. The SAU-budget deadline is a different statute,
**RSA 194-C:9, I** ("At a meeting held before January 1"). **Do the arithmetic, in days, and
check it.** The 12/7/23 page shipped with "December 14 is twenty-four days before the
statutory deadline"; December 14 → January 1 is **eighteen** days. My brief carried the wrong
figure and the agent adopted it. Corrected on the page 2026-08-29.

**d. There is no RSA chapter 92-A.** Title VI runs 91-A, 91-B, 91-C, 92, 93-A… — chapter
92 is "Tenure and Oath of Office in Certain Cases". The 12/14/23 agenda cites a "92-A" and
the citation is simply bad. Report it as an error in the document; do not go looking for the
chapter and do not silently "correct" it to 91-A on the district's behalf.

**e. RSA 671:30 defeats the caucus exemption.** **CORRECTED 2026-08-29 — the lettering below
was wrong.** RSA 91-A:2, ¶I runs: **(a)** strategy or negotiations with respect to collective
bargaining · **(b)** consultation with legal counsel · **(c)** a caucus of members of the same
political party · **(d)** circulation of draft documents formalising decisions previously made.
So legal counsel is **I(b)**, not I(c); the caucus really is **I(c)**, and the argument below is
unaffected. The caucus exemption That exemption
cannot reach a New Hampshire school board: **RSA 671:30** requires every school district
without a special statute to use the **non-partisan ballot system** for the election of
district officers — unamended since **1979, 321:1, eff. Aug. 21, 1979**. A body whose members
are elected on a non-partisan ballot has no party caucus to hold. Where a quorum meets off
the record before a budget vote, the caucus exemption is not available and should not be
offered as a possible defence.

**f. Do not overstate a caucus from its outcome. FIXED 2026-08-29 — read the arithmetic.**
The 12/13/23 page (`15471`) computed a correct $117,000 binder-to-vote net change and then
*located* it at the 18 December caucus, asserting the caucus was "the session at which the
figure the board voted on was assembled." That is the overreach. **The real $350,000 gap is
between the 18 December TELEVISED figure and the 20 December motion** — Sprague on tape,
18 Dec 2:04:16, "we're looking at 1.783" on the FY24 base of $34,880,312, i.e. ~$36,663,000,
against the $36,313,407.97 moved on 20 December. Not binder-to-motion. Crawford was still
reverse-engineering the same difference herself on 5 January ("I was trying to determine
where the 350,000…").

The rule stands and is general: **a gap between what was discussed on tape and what was moved
is a hole in the record, not proof of what was decided off camera.** Report both figures and
the gap; assert nothing about the closed session.

**g. A misattribution to avoid — the 12/20/23 Consent Agenda.** The sentence "No discussion,
unanimously approved" belongs to the **December 6 draft minutes**, not December 20 — and
there it disposes of the **11.15.23** minutes, not 12.6's own. The December 20 defect is the
opposite and worse: **no vote was taken at all**. Check which document a minutes sentence
lives in before you build a finding on it.

**CLEARED 2026-08-29 as to the shipped pages** — `15483` and `15453` both attribute it
correctly; no page in `Output/HTML` misattributes it. The rule stays as a standing warning.

**h. Names the district itself gets wrong.**
- **"Polly Bathurst" is Polly Bath.** ASR splits the surname; a page carrying "Bathurst"
  is wrong.
- **The Rebecca cluster is FIVE spellings, not two, and it may now be settled.** The corpus
  carries Duska, Vendesco, **Vinduska** (printed as fact on five pages: 14937, 16409, 16776,
  16951, 17046), Vindeska (3/19/25 approved minutes) and "von Duska" (ASR). Almost certainly
  one person: Ward 1, Claremont Middle School teacher. **The strongest source in the corpus is
  not a district document**: the Jack and Dorothy Byrne Foundation letter of 7 February 2023,
  on foundation letterhead, in the 3/1/23 packet, is addressed to **"Rebecca Vinduska" at
  Claremont Middle School**. A third party writing to her by name outranks the district's own
  inconsistency. **Pending the user's ruling, keep describing the role and do not print a
  spelling as fact** — but cite the Byrne letter where it is relevant.
- The student representative is **Kylee**, not Kylie, in the district's own filings.

## 16. Deliberative sessions (added 2026-08-29, from the 2/3/24 page)

A deliberative session is the **first session of the annual school district meeting** under RSA 40:13.
The body is the **voters**, not the board. Consequences that change how a page is written:

- **No roll call, no quorum, no consent agenda, no citizens' comment period, no nonpublic session.**
  RSA 189:74's 30-minute rule applies to "a meeting of the school board held under RSA 91-A:2" and
  has no application here; do not flag its absence.
- **The governing law is RSA ch. 40 as extended to school districts**, plus RSA 197:19/197:20 and
  RSA 671:33, III on who presides, and the district's own Rules of Procedure. Every one of those is
  now written up with an IN FORCE FROM date in `pending_legal_anchors.md` under "SB 2 deliberative
  sessions" — read that section before writing a deliberative-session page. **RSA 40:13 is durable:
  last amended 2019, 192:2, eff. July 10, 2019, so today's text governs the whole corpus.**
- **The default-budget definition is RSA 40:13, IX(b), not XI.** XI(a) is the disclosure duty plus
  the four minimum contents of the default budget form; XI(b) is "This amount shall not be amended by
  the legislative body"; XI(c) is the prescribed ballot wording. Claremont's published worksheets
  quote IX(b) with the eliminated-positions clause cut off — check before repeating.
- **Claremont's Rules of Procedure sheet misstates the voter's remedy for a doubted vote** and omits
  RSA 40:13, IV(a) and IV(c) entirely. Same sheet in 2023 and 2024; expect it in 2025 and 2026.
- **The minutes are the register of who spoke, and the recording usually is not.** The ASR loses the
  podium "name and ward" almost every time. Claremont's minutes list floor speakers **grouped by
  position (for / against / neither) but in speaking order within each group** — verified twice on
  2/3/24 against speakers who do self-identify. That makes ordinal identification defensible; say so
  and show the working, and refuse to name where two turns cannot be told apart.
- **"Interim moderator" is not a New Hampshire office** and a school board cannot create one
  (RSA 197:26 excepts the moderator). If a page's presiding officer is not the elected moderator,
  look for a moderator *pro tempore* being chosen by the meeting or appointed by the district clerk;
  on 2/3/24 neither happened and that is the page's HIGH flag.

## 17. METHOD — three ways this run has silently corrupted its own output (2026-08-29)

**a. An unquoted heredoc eats your dollar figures. Always write `<<'EOF'`, never `<<EOF`.**
`cat >> page.html <<EOF` makes bash expand `$688` as a variable, so
`$688,426.17` lands on the page as `88,426.17`, `$36,313,407.97` as `6,313,407.97`,
`$196,001.10` as `96,001.10`. One agent corrupted **six of ten** page chunks this way and
only caught it because `verify_quotes.py` failed the quotations containing amounts. On a
budget page that is a page full of wrong money with nothing visibly broken. Quote the
delimiter, every time. If your page needs a shell variable, write the literal text and
substitute afterwards with python.

**b. Copy long quotations from the CSV field itself, not from a reformatted dump.** A
re-wrapped scratch dump dropped a three-word phrase repeat out of the middle of a
quotation ("There's there is over 60 parents" for "There's there is **that there is** over
60 parents"). It reads like clean text and it is a fabricated quotation.

**c. `verify_quotes.py` mis-pairs quotation marks around very short quoted spans.** Its
scanner is `"([^"]{8,600})"`, so anything **under 8 characters** inside typographic quotes
is skipped — which shifts the open/close pairing for the rest of that block and
manufactures REVIEW lines made of your own prose. Twelve phantoms on one page. **Set
single-token transcript items (`Yes.`, `Aye.`, `SAU`, `RSA`) in `<em>` rather than
quotation marks**, and say so in the page's method footer. This is now the second
documented limitation of the checker; both are in `pending_legal_anchors.md`.

## 18. Network, and where the evidence actually is (2026-08-29)

- **`curl` does not work.** From the device shell there is no egress at all; from the cloud
  container the agent proxy returns 403 / `connect_rejected` for `gc.nh.gov`,
  `law.justia.com`, `govinfo.gov`, `drive.google.com` and `reflect-claremont.cablecast.tv`.
  **`WebFetch` reaches all of them.** Use it for statute texts and for the Cablecast API.
- **WebFetch caps quotation length.** To pull verbatim statutory text reliably, ask for
  "short exact fragments, each under 120 characters, labelled by paragraph, plus the source
  note verbatim."
- **Google Drive `get_file_metadata` is load-bearing evidence and it works where
  `search_files` does not.** Its `createdTime` / `modifiedTime` date the posting of a packet
  or a set of minutes, which is how you test a minutes-timeliness or notice claim. It
  returns real data for folders whose `search_files` with `parentId` returns `{}` — a third
  independent confirmation of the METHOD WARNING in `pending_legal_anchors.md`. **Any
  negative derived from `search_files` alone is unsafe.**
- **The live policy index gives you the *latest* revision date, not the adoption date.**
  Open the policy itself and read its own "District Policy History" block. Doing that
  recovered two supposedly unrecoverable adoptions on one page (BEDH: first reading
  17 May 2023, adopted 6 Sep 2023 — which independently corroborates that the unminuted
  5/17/23 meeting really happened; JLDBB: read and adopted 6 May 2020).
- **For any 2023–24 Uniform Guidance citation**, the pattern
  `govinfo.gov/content/pkg/CFR-2023-title2-volN/xml/CFR-2023-title2-volN-sec200-NNN.xml`
  returns the correct annual edition. Do not cite the current eCFR for a 2023–24 meeting.

## 19. The superintendent changeover is SETTLED — supersedes §3's open date

**Voted the evening of Thursday 11 January 2024; both motions effective Friday 12 January
2024.** The SAU 6 board terminated Michael Tempesta's contract under paragraph nine, with
six months' severance, and appointed **Christopher Pratt interim superintendent**, contract
terms expressly delegated to the chair and counsel for later approval. Roll on each: 10 in
favour, Erickson opposed, Popescu abstaining. Sources: the 1/11/24 recording (show 15523,
0:06:15 and 0:08:11), the draft minutes `1hQ4ByhOf5iYiiZbot4XueUVQzVohOoqh`, and the
1/17/24 Claremont agenda, whose masthead prints "Christopher Pratt, Interim Superintendent"
six days later.

So: **Tempesta is superintendent through 11 January 2024. Pratt from 12 January 2024** — and
he was *appointed* that night, not contracted. §3's correction stands; its open date closes
here. `briefing.md` Addendum 2's "fired Jan 11-12, 2024" resolves the same way.

## 20. The phantom RSA chapter 92-A recurs — and reaches the minutes

§15d records the 12/14/23 SAU 6 agenda citing a chapter that does not exist. The **1/11/24**
agenda repeats it, and this time **the minutes repeat it too**, in a sentence the clerk
composed: "motioned to move into non-public under RSA 92-A:3,II". Treat it as a standing
defect of this board's paperwork rather than a one-off typo — check for it on every SAU 6
page. Report it as a defective citation. Never repair it silently, and never assume the
body meant 91-A:3, II even though it plainly did.

## 21. A meeting the corpus does not have — the working session of 29 January 2024

Announced on the 1/17/24 recording and in its minutes as **24 January at 6:00 at the Dow**;
the only surviving record is `Minutes from CSB working session 1.29.24 (1).pdf`
(Drive `1cUypy-yz4rC3KT9vRLmMia7-mLXk5M7F`), filed in the **`4. CSB 2.21.24`** packet and
approved on the 21 February consent agenda. Three pages of substantive business — slide-by-
slide assignment of the deliberative presentation, wording changes to the district's public
case, a direction to move to restrict reconsideration — with **no attendance, no times, no
location**. It has no video, no MAP.md section and no notice. Any page touching late
January or February 2024 should account for it.

## 22. Corrections from the February–March 2024 wave (2026-08-29)

**a. `verify_quotes.py` now prints every miss on a single-page run.** It used to cap the
list at 12 and print "... and N more", which made a before/after audit of an edit
impossible. Patched 2026-08-29: a single-page run prints all of them; `--corpus` still caps
at 12 so the sweep stays readable. **Read the whole list.**

**b. §17c is under-stated. The rule is: never put fewer than 8 characters inside typographic
quotes anywhere on a page.** Not only single-token transcript items — a quoted name
(`"Chris"`, `"Whitney"`) or a single quoted word in your own prose does it too. Each one
shifts the open/close pairing for the rest of that block and manufactures phantom REVIEW
lines built from your own sentences. Use `<em>` instead, every time.

**c. The Drive `createdTime` proxy measures PACKET ASSEMBLY, not minutes production.
REFINED — `modifiedTime` rescues a document only when the gap is DAYS.** In several packets
every file carries a `modifiedTime` a few seconds *before the folder that holds it was
created* — an upload-session artefact that proves nothing about authorship. Check the size of
the gap before you rest a timeliness finding on `modifiedTime`. The original observation:
This is a real correction to §18 and it changes findings. Verified on three folders:
Claremont minutes reach the public share **only when the next meeting's packet folder is
created**, within seconds of it —
`2. CSB 1.17.24` folder 2024-01-16T14:47:07Z → 1/3 minutes 14:47:22Z (15 s);
`4. CSB 2.21.24` folder 2024-02-14T21:08:52Z → the 1/17 draft *and* the 1/29 working-session
minutes both at 21:09:38Z; `5. CSB 3.6.24` folder 2024-02-29T13:58:35Z → 2/21 draft 13:58:58Z.
**So `createdTime` is evidence of when the public could see a document, not of when it was
written — and `modifiedTime` can prove the document existed earlier.** The 2/21 draft's
`modifiedTime` (28 Feb) puts it inside the five-day window while its `createdTime` is
outside. Use both, and say which one your finding rests on.
(Also: 15 January 2024 was a national holiday — RSA 288:1, third Monday in January. The
1/3 minutes landed on the **8th** business day, not the 9th.)

**d. Fourth confirmation of the Drive-search METHOD WARNING.** A title search for
`working session` returned two unrelated files and **not** the very document the 2/21 page
was about. Any negative from `search_files` alone is unsafe. `get_file_metadata` and
browser enumeration are the reliable routes.

**e. §20's phantom RSA 92-A stops after 15 February 2024 — IN THE SAU 6 PAPERWORK ONLY.**
Claremont has its own, different, ongoing version: the by-laws' Appendix D (adopted 5 June
2024) says RSA 91-A:3 "sets forth eight grounds" and then lists **nine** (the statute has
twelve live grounds, (a)–(m) with (f) repealed), and the **7 August 2024 Claremont minutes
cite "RSA 91-A:3, I & II (1)"** — paragraph I, which contains no exemptions at all, plus the
by-laws' own invented numbering. So do not read "the paperwork is right from April 2024" as
covering Claremont. Check both bodies separately.

**And even for SAU 6 the clearance is narrow: it covers NONPUBLIC-SESSION citations only.**
SAU 6's own policies adopted 12 September 2024 cite the wrong statutes twice — BBBH-S §E
cites **RSA 194:4**, which is *Notes of Districts* (district borrowing), for the duty to
provide superintendent services; and DIE attributes an NHDOE filing requirement to
**RSA 671:5**, which contains none. Both are in `pending_legal_anchors.md` as negative
anchors. As to nonpublic-session citations in SAU 6 paperwork: Three SAU 6
agendas carry it (12/14/23, 1/11/24, 2/15/24), two sets of SAU 6 minutes repeat it (1/11,
2/15), and on show 15580 at 0:02:37 **the chair speaks it aloud**, correcting herself once
and landing on the wrong chapter both times. The 4/11/24 agenda then heads its item
"Non public meeting session RSA 91-A:3, II (a)" and the minutes cite "91-A:3, II a & b".
So: check every SAU 6 page **through February 2024**; from April 2024 the paperwork is right.

**f. A second corpus gap, alongside §21's 29 January working session: the 3 April 2024
board meeting does not exist in the record.** Scheduled on the 20 March agenda with
ESSER-balance and pre-populated-agenda items. The packet sequence runs `6. CSB 3.20.24` →
`7. CSB 4.17.24`, and the 17 April consent agenda approves the **20 March** minutes. The
by-laws, deferred to "our next meeting", appear on neither the 17 April nor the 15 May
agenda. No video, no minutes, no notice, no MAP.md section.

**g. Two research traps in this wave that nearly produced wrong findings.**
- **RSA 198:4-b, ¶I's "unanticipated expenses" limitation does not reach ¶II money.** ¶I is
  the contingency fund (separate warrant article, unanticipated expenses). ¶II is retained
  year-end unassigned funds (≤5%, prior public hearing, 7 days' newspaper notice) and **states
  no purpose limitation at all.** A chair who told the 3/6/24 board otherwise defeated a
  postponement with it.
- **There is no 42 U.S.C. §218d.** The PUMP Act is **29** U.S.C. §218d; 42 U.S.C. §218 is the
  National Advisory Council on Migrant Health. A district policy in this corpus cites the
  wrong title, and it is easy to copy.

**h. On grading a document-only meeting.** The 2/21/24 page graded the 29 January working
session HIGH where the 17 January page graded a related defect MEDIUM. That divergence is
fine — but the page **stated the §5 limb analysis explicitly and explained the divergence
rather than leaving it silent.** Do the same whenever your severity differs from a
neighbouring page on similar facts.

## 23. April–June 2024 wave (2026-08-29): closures, and a much bigger record gap

**a. THE BY-LAWS ARE CLOSED. Adopted 5 June 2024.** "Mike Petrin made a motion to approve
the by-laws as presented, Bonnie Miles seconded; voice vote taken, all present voting in
favor" — corroborated on show 15786 at 0:41:52. **Four of seven members present**, the bare
quorum, and the member who had dissected the draft on 20 March was absent. The adopted text
is **not** the 20 March draft: the chair reported "all SAU and Unity portions have been taken
out". Adopted text: `Exhibit E- Claremont School Board By-Laws .pdf`, Drive
`1zjjPqW00SUYvvGuTtDEOKnREw-rB6Nff`, 22 pages, in the 6/5 packet. **From 5 June 2024 onward
the by-laws are a governing document you must check a Claremont page against**, and their own
defects (see §22e) are findings in their own right.

**b. §21 and §22f were the tip of it. There are SIX 2024 sessions outside the corpus.**

| Date | What exists | What does not |
|---|---|---|
| **29 Jan 2024** working session | minutes only, in `4. CSB 2.21.24` | notice, attendance, times, location, video, MAP § |
| **3 Apr 2024** | *nothing* | everything — scheduled 20 March, no cancellation anywhere |
| **1 May 2024** | *nothing* | everything — scheduled in the 17 April minutes |
| **11 May 2024 retreat** | minutes (`1zDKtSVGmFjjT3aMlrsP_R4-iPTYtpN5N`) — **5 of 7 + clerk**, SAU 6 conference room, 10:00–noon | notice. Announced on 17 April as "10:00-11:00 **at the Teal Lantern**" — wrong venue, wrong end time. Minutes 7 business days late |
| **22 May 2024** | minutes (`1UJPYxAD3cTgcFNO8FKz7QprHoDxC0y2i`) — 6:00 call to order, nonpublic under 91-A:3, II(c) 6:10–6:45 on roll-call votes, **sealed 10 years** | video, packet, MAP § |
| **7 Aug 2024** | draft minutes (`1gMCLl0rvbUw7I8-rB_t-OKIAw-iRnjdr`), packet folder `1. CSB 8.7.24` | **recording, Cablecast show, MAP §** — a full regular meeting with a consent agenda, counsel presentation and a nonpublic session |

The 3 April and 1 May absences were established by **enumerating** the Cablecast archive
(15672–15687, 15721–15734) and the full 2024 Drive packet share, not by searching — and the
same archive carries other programming on both dates, so it is not an outage. **Any page in
this window must account for the gap that precedes it.** The 11 May retreat carries a written
action item ("Establish a norm that the board will meet in a non-meeting or non-public once
before collective bargaining…") adopted at a session whose announced venue and end time were
both wrong.

**c. The 15 May "Whitney + Sprague + Crawford" subcommittee was a CSV artefact, not a
misreading — and this corrects my own Addendum 14 brief.** Nobody read a membership list
aloud on 15 May. There is one first-person sentence — "today I sent an email to Mr. Sprague
and Miss Crawford to get together so we can begin with our vision" — which the dialogue CSV
labels for the chair. Read as **Bonnie Miles** it is exactly right. Three supports: Miles is
present with **zero** attributed rows; the sentence sits in a `Speaker 1` cluster that by then
carries a different voice by override, while the chair's own words either side are
`Speaker 21`; and the same merge happens three more times, with the approved minutes naming
Miles each time. **The lesson is general: when a CSV label produces a body or a fact that
exists in no document, suspect the label before you suspect the document.**

**d. The Parliamentary Procedure committee's third member is Michael Petrin** — Whitney,
4/17 at 1:13:11, "we Mike patron and Frank Sprague and myself, we're part of an ad hoc
parliamentary and procedure committee" (`Mike patron` is the standing garble). Closes
Addendum 14.

**e. Method: a two-column district PDF interleaves on text extraction, so its ORDERING is
unreliable even when its text is clean.** The 6/5 packet's CCTV roster reads as though a seat
sits under the wrong heading, and the same scrambling manufactured a plausible committee name
that does not exist. Same class of hazard as §17b. Treat column order in any two-column
district PDF as unverified.

**f. Cablecast run times.** The public show page gives none; the API does —
`https://reflect-claremont.cablecast.tv/cablecastapi/v1/shows/<ID>?include=reel` returns
`totalRunTime` in seconds. Use it to bound your `seekto` values.

**g. `search_files` with `parentId` sometimes works.** It returned 18 children for the 2024
packet folder and `{}` for the 2024 minutes folder whose contents were readable by
`get_file_metadata` seconds earlier. **Try it — but a `{}` result still means nothing.**

**h. Maintainer disclosure — a standing rule.** The 6/5/24 packet names **Kevin Tyson**, this
project's maintainer, as the holder of Seat 3 on the CCTV Board of Directors (City Council
appointment, 13 July 2022; the packet shows the term ending 31 May 2025, but he has served
continuously since and still sits on the board, as of 29 September 2026). Claremont
Community Television (CCTV) and Claremont Community Media Center (CCMC) are one organization;
always name it with both names. CCTV/CCMC is the source of every recording in this corpus
and publishes these pages as the Claremont School Board Meeting Navigator. **Wherever the maintainer, CCTV's board, or CCTV's own interests appear in a
document a page relies on, disclose it plainly in the page footer** — as the 15786 page does
— and keep the finding to what the documents support. Do not omit the item, and do not soften
it.

## 24. August–September 2024 wave (2026-08-29)

**a. A SEVENTH 2024 session outside the corpus — add a row to §23b.** A Claremont board
meeting **between 20 June and 7 August 2024 failed for want of a quorum**. Four independent
mentions on the 21 August recording (Pratt 0:49:26, Miles 0:49:38 and 0:49:44, Petrin
0:57:33) and the approved minutes — "was on a previous board agenda but there was not a
quorum." It is not 20 June (six present) nor 7 August (six present, and the item is absent
from its agenda). **No notice, agenda, minutes, folder, video or MAP section exists**, and
no member names a day. Like 3 April, nothing at all survives.

**b. THE SAU 6 WEBSITE HAS NOW BEEN SEARCHED — and it is empty for our period.** The by-laws
(1.05(c)–(d), 1.11) send every subcommittee notice and every set of subcommittee minutes
there, and this project had only ever searched Drive. The Claremont board page
(`sau6.org/119765_1`) links five subcommittee Drive folders, read 2026-08-29:

| Subcommittee | Folder | Created | Contents |
|---|---|---|---|
| Capital Improvement | `1zh_axsEVchb_tN0TP56OB5kuJMMnFaQY` | 2026-02-04 | empty |
| Finance | `1LLMD5zj9ZxEWxx3nRLlVrSFBupA6mGO5` | 2026-02-04 | purpose statement (2025-06-02), `2025-2026` (2026-07-02) |
| Policy | `1UyUWBMgA6z4tZxbc8SSt-wgUEo-Ovlmh` | 2026-02-04 | empty |
| SRVRTC | `1OKp_pu7XrZ1_GYwUHNM7EnKAh5rZGDd0` | 2026-02-04 | empty |
| Ad Hoc Reconfiguration | `1sBcCWTWabFKR3P89uBbgV8SgPzV86LXq` | 2026-04-15 | empty |

**Nothing from 2024 is reachable from any of them**, and there is no folder at all for the
SAU 6 Exploratory Ad Hoc, Ad Hoc Communications or Curriculum subcommittees. The board itself
conceded the venue was not operating — 21 August 2024 approved minutes, of subcommittee
folders and purpose statements: "once the website is up and running, those will be
available." **State the honest limit**: the site as it stood in 2024 cannot be inspected from
here, so this is "not published where the by-laws require, and not recoverable", not "never
existed". This destination is checkable for every Claremont page from 5 June 2024 onward.

**c. Drive metadata, third refinement — for the FY25 sequence use the FILE createdTime, not
the folder's.** The `2. CSB 8.21.24` folder was created **2024-07-25**, a month ahead, while
all eight files were uploaded **2024-08-19**. §22c's folder-creation proxy holds for the
2024 packets and breaks for FY25. And the `modifiedTime` artefact recurs at 60–70 seconds —
still rescuing nothing (see §22c as refined).

**d. Fifth confirmation of the Drive-search warning, and the sharpest one yet.** A `parentId`
enumeration of the 2024 packets share returned 18 folders and **silently omitted three that
MAP.md records**: `1. CSB 8.7.24`, `7. CSB 11.6.24`, `8. CSB Retreat 5.11.24`. A `{}` result
proves nothing — and now a *non-empty* result proves nothing about completeness either.
**Never write "the share contains N folders" from a `parentId` call.**

**e. ffmpeg scene analysis CANNOT distinguish a splice from a camera cut on these CCTV
recordings.** An agent tried to settle a zero-gap question empirically: frame-differencing
showed YAVG spikes of 42–140 at the suspected join, but the same measure shows routine spikes
of 60–74 elsewhere in the same file — multi-camera shot changes. **The video does not decide
it.** Where a zero-gap transcript raises the question, present both readings and say what
would settle it (a district-side clock reference, or the raw CCTV log). Do not assert a
splice from pixels.

**f. Two more donor-cheque privacy exposures**, after 4/17/24 Exhibit B: the **9/4/24 Exhibit
A** is a photograph of a donor's cheque with bank, cheque number and the full MICR
routing/account line legible. Same class, four and a half months later. **Reproduce no
number.** Cite RSA 91-A:5, IV — noting it *permits* withholding rather than requiring it.

**g. A by-law defect that makes existing citations ambiguous: the 5 June 2024 by-laws contain
TWO rules numbered 2.09** — "(Amendments)" and the agenda-itemisation/publication rule. Any
page citing "by-law 2.09" (the 15814 page does) is ambiguous on its face. **Quote the rule's
text, not only its number.**

## 25. Autumn 2024 wave (2026-08-29): a much better way to read documents, and two more gaps

**a. READ GOOGLE DOCS WITH THE DRIVE MCP, NOT WebFetch.** Board policies live as Google Docs.
`WebFetch` on a `docs.google.com/document/d/…` URL returns only the JavaScript shell —
nothing usable. **`mcp__Google_Drive__read_file_content` on the document ID returns the full
text, including the District Policy History block** that §18 tells you to read. This is
strictly better than §18's advice; use it.

**b. FOR CONTRACTS AND MULTI-COLUMN PDFs, USE `pdftotext -layout` IN THE CLOUD CONTAINER.**
The Drive MCP's `read_file_content` scrambles them — on one contract it interleaved the DRAFT
watermark and reordered clauses. The route: `mcp__Google_Drive__download_file_content` →
base64 decode → `pdftotext -layout`. That recovered a missing sub-clause and a clause
numbering that runs **1–16, then 27, 21, 22**, neither visible in the scrambled text. The
container has `pdftotext`, `pdftoppm`, `pypdf` and `pdfplumber`. This is the §17b hazard's
actual fix.

**c. Small validator gotcha:** writing a UTC clock time as `14:06:36` trips
`validate_pages.py`'s H:MM:SS note. **Drop the seconds** when citing Drive metadata.

**d. Two more sessions outside the corpus — §23b/§24a's table now runs to NINE.**

| Date | What exists | What does not |
|---|---|---|
| **6 Nov 2024** | packet folder `7. CSB 11.6.24` | **no minutes were ever created.** Cablecast 16140/16141 are both 3 Nov and 16142 is SAU 6 on 14 Nov, with other programming on 1, 3 and 4 Nov. The 20 Nov consent agenda approved "10.16.24 & 11.14.24", skipping it |
| **14 Nov 2024, 8:16 p.m.** — a **Claremont** board meeting held the same night as the SAU 6 meeting, in the same room, before five of the same people | draft minutes `1h9fxbyMjj9OxwkICoO6wAaA5B_chW1k2`, in `8. CSB 11.20.24` | packet folder, MAP §, **and no recording** — Cablecast 16143–16154 were each fetched and are all other programming, and 16153's own event date is 14 Nov, so CCTV was operating. Nonpublic 8:19–8:59 under "RSA 91-A: 3, II (a & d)" with **no motion to seal**, so RSA 91-A:3, III required disclosure within 72 hours — **and no nonpublic minutes exist.** The minutes also misletter the exemption, printing "(b)" against the text of II(d) |

**This settles MAP.md line 6159's open question**: that file records the **Claremont** meeting,
not the SAU 6 one.

**e. A joint city/district meeting is TWO bodies and must be handled as two.** Establish each
body's quorum separately against its own membership (the City Council is a **nine-member**
body). The city's notice, agenda and minutes live in the **city clerk's** system, not the
district's Drive. **Say what you inspected and what you could not; never write a city-side
negative from the district's shares.** The 16046 page does this correctly — model it.

**f. Sixth and seventh confirmations of the Drive warning, and a new failure mode.** A
`parentId` enumeration of the 2024 packets share returns the same 18 folders every time and
**silently omits three that MAP.md records**. `parentId` on `6. CSB 10.16.24` and on
`8. CSB 11.20.24` returns `{}` while every file in the former is readable individually. And a
`title contains '9.30.24'` search returned `{}` while two files carrying that exact string are
readable by `get_file_metadata`. **Write every packet negative as "not found", never as "does
not exist".**

**g. When a page's speaker attribution is thin, say so in the footer with a number.** The
16142 page runs **24.2% Unidentified** because four seated members are never anchored to a
voice, and it states that plainly rather than guessing. That is the right handling of the
second hard rule.

## 26. December 2024 wave (2026-08-29)

**a. A district-side clock reference CAN settle a splice — §24e was too pessimistic.** Pixels
cannot decide it, but a **spoken clock time** can. On show 16157 the chair supplies two
("Mr. Upton will be available in roughly 15 minutes" at 0:34:15; "I asked him if he's
available soon. At 719." at 0:51:14) against the minutes' "Consent adjournment at 7:41pm".
The spliced reading fits all three anchors to within 20 seconds; the continuous reading fits
none. **Before giving up on a zero-gap question, grep the CSV for spoken times.**

**b. §22e, final count: the by-laws' Appendix D counts the nonpublic grounds FOUR ways** —
"eight grounds" in prose, **nine** enumerated, "the **nine** statutory bases" two paragraphs
later, and **six** lettered (a)–(f) in the compliance checklist, which fuses II(d), II(e) and
II(g) into one item and then continues lettering procedural steps g–o in the same series. The
statute has **twelve** live grounds. Appendix D also states the 72-hour rule and a nine-item
minimum-content list for nonpublic minutes, citing policy BEDG.

**c. Better by-law hooks than 2.09** (which is ambiguous — two rules share the number, §24g):
**2.02** special meetings, "Except by 2/3rds vote of all members, only matters contained in
the notice shall be considered"; **4.03(d)** makes posting agenda materials with the agenda a
**clerk's duty** — the right hook for a missing exhibit.

**d. The corpus's missing-session table keeps growing. Three more Finance Subcommittee
meetings with no public record: 12 November, 4 December and 12 December 2024**, all noticed
in the approved 16.10.24 minutes and on the 20.11.24 agenda. And the 20.11.24 agenda,
minutes and superintendent's report all notice Finance meetings for **4 and 18 December**,
while the corpus holds recordings for **13 and 18 December** — no notice for 13 December has
been located. Add these to §23b / §24a / §25d when citing the table.
**6 November 2024 is now CLOSED as never held**: the 14 Nov minutes show a *separate special*
meeting (Thursday 8:16 p.m., nonpublic only), not a rescheduled regular meeting, and the
consent agenda approves only 10.16 and 11.14. No 6 November minutes were ever created.

**e. A small correction to §25d's framing.** The 20 November **agenda** printed "Minutes
Approval- 10.2.24 & 11.14.24"; it is the **approved minutes** that print 10.16.24 and record
Koski's correction. The same agenda defect repeats on 4 December ("10.2.24 & 9.30.24"), and
the 2 October minutes had already been approved on 16 October.

**f. The Claremont "Unsealed Minutes" destination is datable, and it is empty for our
period.** The Meeting Minutes share (`1482gj2MFrWIESHvadUpXEx5Tn_L3Vjdv`) has exactly six
children — year folders 2023–2027 plus `Unsealed Minutes` (`1KRYrJx5pHxbgiuYUK734SBpAaxyTelnc`),
**created 13 January 2025**, holding only `2025/2026/2027 Non-Public`. **There is no 2024
folder.** The district built the right destination seven weeks after November 2024 and put
nothing from 2024 in it.

**g. `Output/HTML/index.html` is now ~26 pages behind** and has been flagged by six agents.
It still reads "Forty-five meetings, January 6, 2025 – August 19, 2026". **Nobody should
edit it mid-run** — it gets one regeneration pass at the end. Do not touch it.

## 27. Late-2024 and 2025 wave (2026-08-29)

**a. TWO NEW CONTINUITY TESTS, both cheaper than pixels (extends §24e and §26a).**
- **The Cablecast API's `eventDate` sometimes carries a real wall-clock time and sometimes a
  midnight placeholder, and the difference is diagnostic.** Show 16226 returns
  `eventDate 2024-12-18T12:50:39-05:00` with `created` a minute later; show 16222 returns a
  date-only stamp. **A precise eventDate plus a creation stamp a minute after it reads as
  auto-created when recording began** — usable evidence of when a meeting with no call to
  order actually started, and it is what settled the ordering of the two 18 December
  meetings.
- **Spoken countdowns, which are far commoner in these recordings than spoken clock times.**
  Three on one file — "45 minutes left in this session", "we have a half hour left", "we got
  ten minutes for the calendar" — projected ends of 2:50 / 2:47 / 2:46 p.m. against an actual
  2:47 from the event stamp. Grep the CSV for "minutes left", "half hour", "we have until".

**b. A SHIPPED PAGE WAS WRONG AND IS NOW FIXED — the lesson generalises.** The `16882` page
said the earlier Claremont meeting of 6 October 2025 "has no recording of its own in the
Cablecast gallery." **Show 16881 IS that recording.** MAP.md §96 had conflated the two
meetings; it is now split into **§96 (Claremont, 5:30 p.m., show 16881)** and **§96a (SAU 6,
6:00 p.m., show 16882)**. **Before writing that a meeting has no recording, fetch the
neighbouring show IDs from the Cablecast API and read their titles** — several agents have
now done this and it has changed the answer twice.

**c. THE BY-LAWS EXIST IN TWO VERSIONS THAT DIFFER IN BOTH NUMBERING AND WORDING.** Beyond
§24g's duplicate 2.09: the live Google Doc `1ufhE0flW6DdmhKfON7QH8PG_coPnGhFBfdyEVRId8DE`
(modified 2026-03-23) carries the special-meeting sentence **not as 2.02** but folded into 2.01
and attributed to "policy BEDD-R. 2.0", and numbers the Ed 302.02(i) temporary-staff rule
**2.02** where the adopted PDF (`1zjjPqW00SUYvvGuTtDEOKnREw-rB6Nff`) numbers it **5.04**.
**CORRECTED 2026-08-29 — an earlier version of this section said "wording identical". It is
not.** Rule **2.07**: the adopted PDF reads "…unless governed by the 2/3 vote rule in CSBL **or
Robert's Rules exceptions**…" and its abstention passage ends at "counter to a member's public
duty"; the live Doc drops the Robert's Rules words and **adds** "The NHSBA recommends voting
'No' if members do not have enough knowledge or resources to support a motion rather than
abstain." Rule **4.01**: adopted "Vote upon any question that arises" against live "Vote on all
questions. Maintains all board member privileges." Numbering of 2.07/2.11/2.12/2.13/2.15 is
identical in both.
**Quote by-law TEXT, never a number alone, and say which copy you read and when it was
modified.** Which copy was in force on a given date is generally unknowable from here.

**d. A fourth district citation that points at the wrong statute.** Joining RSA 194:4
(policy BBBH-S §E) and RSA 671:5 (policy DIE): **Claremont by-law 4.03 heads the board
clerk's minutes, notice and posting duties "per RSA 671:20 and RSA 671:25"** — both of which
are ballot-preparation provisions and say nothing about minutes. All three are negative
anchors in `pending_legal_anchors.md`.

**e. Policy BEDH resolves, for this board, the RSA 189:74 ambiguity the anchors file flags.**
BEDH (Drive Doc `1fcf5-e0lKvMTRlW7e6NjpCZ6OFQPC-wymYBu0ydf1CE`, first read 17 May 2023,
adopted 6 Sept 2023) requires comment at "**all Board meetings**" with only RSA 189:74's two
exceptions, "a minimum of thirty minutes in total", and §B.3 the chair's "**vocal invitation**
to the audience". **It overrides by-law 2.04's narrower "each regular meeting"** — by-law 2.15
subordinates the by-laws to state law. Every Claremont agenda hyperlinks BEDH at its foot.

**f. A tenth and eleventh session for the missing-meetings table.**
- **2 January 2025**: a Claremont board meeting announced and never held. Closed as never held
  by the 7 January minutes three ways — the consent line reads "Minutes Approval-**none**",
  the future dates skip it, and the four policies promised for 2 January (KCD, JRA, GBEAA,
  JFABD) are taken up on 7 January. **Unlike 3 April / 1 May 2024, the business demonstrably
  moved; what is missing is the cancellation.**
- **A Policy subcommittee meeting on 18 December 2024** and **a Finance session in Christmas
  week 2024**, both announced on tape, neither with any record.

**g. Where a subcommittee's minutes-gap looks unanswerable, the same night's board packet is
the comparator.** `10. CSB 12.18.24` contains `CSB Visioning Sub 12.9.24.docx.pdf` and
`Cap Improvements Committee Meeting minutes 12.10.24.pdf` — **two other subcommittees minuted
their December meetings and the district filed them.** Finance filed none, for any of its
three televised sessions. That contrast is the finding; "no minutes found" alone is not.

**h. A standing ASR hazard, confirmed live: `Harrington` is produced at 0.99–1.00 confidence
for TWO different people in one file** — Michael Herrington (SHS principal) and Michelle
Herrington (SRVRTC). **Never merge them**, and never let a confidence score stand in for
identification.

**i. A new garble class: FUSED DIGIT PAIRS.** `378 minute classes` = *three 78-minute
classes* · `178 minute prep` = *one 78-minute prep* · `646 minute classes` = *six 46-minute*
· `$57,592, 852,500 and 857,000 $357,592` for a single **$857,592**. A reader taking the
transcript at face value gets a 378-minute class. **Any number that looks impossible is
probably two numbers.**

## 28. Early-2026 wave (2026-08-29) — read §27a's correction first

**a. §27a IS WRONG AS WRITTEN for most of this archive. Corrected here.** Cablecast show
numbers follow **record-creation order, not event order** — which is why show 17125
(7 February 2026) has a lower number than 17134 (4 February 2026): 17125's record was opened
on 23 January, 17134's on 3 February. Two more confirm it (17095 for 21 Jan created 6 Jan;
17116 for 20 Jan created 19 Jan).

**The rule:** a `created` stamp that **precedes** the event date is a **hand-entered,
pre-scheduled record** and says nothing about when recording began. §27a's diagnostic — a
precise `eventDate` with a creation stamp a minute *after* it — holds only for the other kind
of record (show 17126 is a textbook case; show 16226 is the one that settled 18 December
2024). **Check which kind you have before relying on either field, and never infer a sequence
from show numbers alone.**

**b. A derived-excerpt show is a real thing in this archive, and it has its own transcript.**
Show **17168** is not a second meeting: it is an **edited excerpt of show 17159**, created the
afternoon *after* the meeting. 121 of 134 substantial rows align at a **constant 2,277.9 s
offset with no drift**, and the excerpt's first segment **fuses the 6:30 call to order onto
"Moving on to article eight"** — two utterances 38 minutes apart in the room. (MAP.md §111
gives the offset but not the spliced opening; a reader taking it literally will look for the
opening words at 0:38 of 17159 and not find them.)

**Consequence — a rule: the corpus holds two independent machine transcriptions of the same
49 minutes, and they differ materially** (`RSA 3215-F` vs `are essay 32 colon 5-F`; "We're
going to have to cut the budget roughly 9 million" vs "We were going to cut the budget.
Roughly 9 million."). **Quote only from your own page's CSV** — `verify_quotes.py` catches
cross-transcript quotations, and it caught two. Where you must quote the other, label it with
its show number and do **not** deep-link it (one show ID per page).

**c. A CSV attribution trap that nearly made a board member a union president.** In the
October 2025 candidate recordings **the chair reads three applicants' letters of intent
aloud, and the CSV attributes every word of them to her.** On show 16872 at 0:51:02 a passage
labelled "Heather Whitney" reads "…the last two as president of the Sri, which is the
educators union" — that is an applicant's biography. **Whenever a chair reads a document
aloud, the CSV makes its contents her speech.** Same class as §23c: when a label produces a
fact that exists in no document, suspect the label.

**d. A cohort of shipped pages cites STALE MAP.md section numbers**, from before the MAP was
renumbered: `17046`→"section 43" (now §104), `17092`→44 (§105), `17116`→45 (§106),
`17095`→46 (§107), `16882`→35 (§96a). **This is a known end-of-run sweep — do not fix it
page by page**, and use the current number on any new page.

**e. CCTV mis-titles some January 2026 shows with a 2025 year.** Show 17116's API title reads
"…1/20/**25**" against `eventDate` 2026-01-20; MAP.md §105 repeats "Claremont School Board -
1/7/**25**" for show 17092 (7 January 2026). **The error is CCTV's, not MAP's** — quote the
title as given and note the discrepancy rather than silently correcting it.

**f. §15h — the Rebecca cluster now has a seventh data point and it agrees with the Byrne
letter.** The **approved 18 February 2026 minutes print "Rebecca Vinduska" and "Ms.
Vinduska"**, matching the Jack and Dorothy Byrne Foundation letter of 7 February 2023.
**Pending the user's ruling the rule is unchanged** — describe the role; where you must give a
spelling, attribute it to the document rather than printing it as fact.

**g. Where a page cannot settle who spoke, the district's own minutes often can.** Two
"Unidentified public commenter" clusters on show 17159 are named in the approved minutes
(January King, ward 3; Kyle Messier, ward 1), and a speaker the CSVs called "Noah Bosch" and
"Nora Shane" in two different files is **Noel Beauchaine**, corroborated by the interim
superintendent thanking her by name on tape. **Read the minutes before writing "unidentified".**

## 29. FINAL corrections from the last wave (2026-08-29) — the run is complete at 126 pages

**a. THE BIGGEST FACTUAL CORRECTION OF THE RUN: SAU 6 DOES NOT DISSOLVE ON 1 JULY 2026.**
§28 and several pages record the dissolution as settled background because two officials said
so at the 18 February 2026 meeting. **They were wrong, and the SAU 6 board's own chair corrects
them on tape** — show 17307 at 0:35:20, Whitney: "the saw is dissolving"; chair Rocco Ruggeri:
*"It's not. It's not dissolving. Just to clarify."* and *"It would just be the Claremont board
at that point, but it would still be the same. Six."* The 15 April 2026 approved Claremont
minutes agree: Unity is withdrawing "and it will only be Claremont in the SAU as of July 1,
2026". **What ends is UNITY'S MEMBERSHIP under RSA 194-C:2, IV. The unit continues with one
district.** Ruggeri himself uses the loose word twice before correcting it, which is how the
error propagated.

**But do NOT over-correct, because the district's own paperwork uses the word too.** The
Claremont staff report of 27 March 2026 (Drive `16M5jaunMtgwaVWRIi_iojNp2FgqMcl1W`) reads: *"It
is anticipated at this time that SAU 6 will dissolve as a legal separate entity from the
Claremont School District."* So the record genuinely contains both characterisations, and a
page quoting either is quoting accurately. **The rule is: report what each document and each
speaker actually said, and state the legal mechanism as UNITY'S WITHDRAWAL under RSA 194-C:2,
IV — which is the only mechanism any record identifies.** Do not assert in your own voice that
the unit dissolves; do not silently correct a district document that says it does. What the
employees' side of it supports, on the business administrator's own words, is that *"Saw six
employees get merged to the school district"* — the employer changes whether or not the entity
survives.

**b. §28a needs a THIRD case, and the diagnostic must be sanity-checked twice.** A precise
`eventDate` with a creation stamp a minute later is **not** proof that recording began then.
Show 17291 returns `2026-03-31T13:35:06` with `created` 70 seconds later — for a meeting on
**1 April**. Show 17307 returns `2026-04-09T08:18:44` +43 s — for a **6:00 p.m.** meeting.
Show 17241 returns a precise stamp from **the day before**. **Check the eventDate against both
the meeting's DATE and its NOTICED HOUR before trusting it.** An operator opening a record
early lets `eventDate` default to *now*.

**c. A better continuity test than any of §24e / §26a / §27a — arithmetic, no pixels, no
spoken clocks.** Recording run time + the minuted nonpublic duration reconciles an unstated
start time. Show 17323: 5,103 s of tape; minutes 6:30 → 8:11 p.m. (101 min) with a 17-minute
nonpublic = **84 minutes public against 85 minutes of recording.** That proves the excision
(18 recording-seconds spanning 17 minutes), confirms a call to order the minutes never state,
and validates the minuted adjournment. **Reach for this first.**

**d. Two more sessions for the table, and two documentary ones.** MAP.md records approved
minutes for Claremont **special meetings on 26 March and 30 March 2026** — no video, no packet
folder, no MAP section. And the **28 May 2026 SAU 6 board meeting** has an agenda (Drive doc
`1z95pRjknlr4unl7TKBbZyaZrLe-CakIgHrRwLuauQMI`, folder `14. SAU6 5.28.26`, MAP §120), **no
minutes and no recording** — and it is the meeting that carries the Unity separation as five
action items.

**e. §27c, final state.** In the live by-laws Doc served today there is **no rule 2.02 at all**
— chapter 2 runs 2.01 → 2.03 — and the Ed 302.02(i) temporary-staff rule is **5.04**, the same
as the adopted PDF. The "2.02" reported earlier is the string `302.02(i)` inside rule 5.04.
§24g's duplicate 2.09 is confirmed and still present. The 2.07 and 4.01 wording differences
stand. **The live Doc's Drive `owner` is `mtempesta@sau6.org`** — the account of the
superintendent terminated in January 2024 still owns the board's governing document. Checkable,
but do not build a finding on a metadata field alone.

**f. A sixth district citation pointing at nothing: by-law 1.11 reads "per RSA 91-A:II"** — a
chapter and a paragraph with no section. The set is now: the phantom RSA 92-A; RSA 194:4
(policy BBBH-S §E); RSA 671:5 (policy DIE); by-law 4.03's RSA 671:20/671:25; policy JLCK's
Ed 306.04(b)(15)/(b)(23); and by-law 1.11.

**g. §24b's folder labels have changed under us.** `1sBcCWTWabFKR3P89uBbgV8SgPzV86LXq`, listed
there as Ad Hoc Reconfiguration, now returns title **"[Documents posted to Web]"**, created
2026-04-15; `1UyUWBMgA6z4tZxbc8SSt-wgUEo-Ovlmh`, listed as Policy, is titled **"[Documents
posted to web}"**, modified 2026-07-20. **Do not build a finding on a Drive folder's label** —
re-read it at the time of writing.

**h. Drive `createdTime`, fourth refinement — for the 2026 Claremont minutes it dates the CALL
TO ORDER.** The clerk drafts in the document live, so 3.4.26 minutes were created 6:30 p.m. on
4 March (`createdTime` 2026-03-04T23:30Z; this line said 3 March until corrected 2026-10-03) and 3.18.26 minutes at 6:30 p.m. on 18 March. **It cannot test the five-business-day
rule for these — but it is an excellent independent anchor for a start time the minutes omit.**

**i. Names settled at the end of the run.** The incoming superintendent signs his own memo
**Timothy Broadrick, EdD** and the 5/20 agenda spells it Broadrick; both sets of minutes and
the Cablecast gallery spell it **Broderick**. On the Byrne-letter precedent, **follow his own
document**. `briefing.md` Addendum 1's "Dr. Tim Broadrick" is right and MAP §115's "Broderick"
follows the district. **Lori Mowrey is settled** by the 3/18 Banking Resolution: "Matthew
Angell, Interim Business Administrator; **Lori Mowrey, Finance Director**; Vicki Lee, Staff
Accountant" — closing Addendum 15's six-spelling problem. **`the Dow` is NOT an ASR garble** —
it is the district's own name for the SAU office building, used in its approved minutes and on
an agenda.

## 30. HARD RULE: session legislation is cited from the enacted chapter only (2026-09-25)

**For session legislation, never use an introduced or intermediate bill version once an
enacted chapter is available.** Before a page states what a bill requires:

1. Check the bill's status. If it shows a chapter number (e.g. "Chapter 272"), the chaptered
   law is the only text you may describe or quote.
2. Do not take bill text from LegiScan's "Latest" / "Amended" link. For SB 586 that link serves
   the **Senate-passed** text (amendment 2026-0772s), while the law was later amended by the
   House (2026-1500h) and an enrolled-bill amendment (2026-2121e). "Latest" means latest
   *document LegiScan holds*, not the enacted text.
3. Press coverage of a bill describes the version current on the publication date. Use it
   only as corroboration, dated, and attributed as reporting.
4. If the chaptered text cannot be read, state only the provisions confirmed for the enacted
   law, mark the rest as unverified, and log it in `pending_legal_anchors.md`. Never fill the
   gap from an earlier version.
5. Cite as "2026 N.H. Laws ch. NNN (SB NNN), approved <date>, eff. <date>".

**The case that produced this rule.** Seven pages gave SB 586 a six-month audit deadline and
withholding of "any and all state funding", from the Senate-passed text. The enacted law, 2026
N.H. Laws ch. 272 (approved July 2, 2026; eff. July 1, 2026), repeals and reenacts RSA 198:4-d.
Its ¶VIII requires the audit report for the last completed fiscal year "within 9 months of the end
of the fiscal year" and withholds "state grant funding, not including RSA 198:40-a funding". The FY26
deadline is therefore **March 31, 2027**. Full paragraph map in `pending_legal_anchors.md`; the
chaptered text is saved at `Input/SupportingDocuments/Law/2026-ch272-SB586-chaptered.txt`.
Data Quality Report C1.156.

**Where to read chaptered text.** The NH General Court "FINAL VERSION" page
(`gc.nh.gov/bill_status/legacy/bs2016/billText.aspx?sy=YYYY&id=NNNN&txtFormat=html`) prints
"CHAPTER NNN", the amendment trail, and the Approved and Effective dates. The automated fetcher
is refused there; open it in the desktop browser pane. Save a copy under
`Input/SupportingDocuments/Law/` and cite the chaptered page, not LegiScan.
