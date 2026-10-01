# Master data-quality inventory — Government Transparency Project

Compiled 2026-08-29 by merging the four independent inventories in `Scripts/`:

| Source file | Compiled from | Input records |
|---|---|---|
| `_dq_inventory_briefing.md` (2,058 lines) | the corpus briefing set (`briefing.md`, `html_briefing.md`) | A1–A87, B1–B50, C1–C58, D1–D24 = **219** |
| `_dq_inventory_html_briefing.md` (619 lines) | the run contract (`html_briefing.md`, 126-page run) | A1–A46, B1–B17, C1–C25, D1–D27 = **115** |
| `_dq_inventory_legal_anchors.md` (866 lines) | the legal-citation catalogue (`pending_legal_anchors.md`, 1,486 lines) | A1–A20, C1–C47, D1–D18, V1–V54, N1–N55, F1–F16 = **210** |
| `_dq_inventory_map_and_pages.md` (463 lines) | `Input/SupportingDocuments/MAP.md` (6,169 lines, 129 sections) and the 126 finished pages in `Output/HTML/` | 75 discrete findings across Parts 1–2 and Appendices A–B |
| | | **619 input records** |

**Output: 392 records.** The merge collapsed **227** — records describing the same defect from two or three vantage points, each merged record taking the fullest figure, the exact Drive ID, the statute and session law, and the meeting date and timestamp from whichever source carried it.

**Classes.** **A** district source records · **B** project pipeline data · **C** the project's own analytical errors · **D** method limitations. The legal-anchors file's VINTAGE TRAP and NEGATIVE ANCHOR records are folded in by subject: a vintage trap the project would have got wrong is **C**; a district document citing law wrongly is **A**; a URL trap or an unresolved source note is **D**.

**Tiers.** **Tier 1** — affects what a reader can conclude: the record says something wrong, or would have produced a wrong statement about someone's conduct or the law; the near-miss false accusations sit here, as do the privacy exposures. **Tier 2** — affects what a reader can find or verify: missing records, misfilings, unreliable search, sealed or unrecoverable material. **Tier 3** — affects precision, not conclusions: spellings, transcription garbles, metadata quirks, cosmetic defects.

**IDs** are stable and run `<class><tier>.<n>` within each class-and-tier block: `A1.1` is the first Class A Tier 1 record, `C2.3` the third Class C Tier 2 record. Every record carries a `Sources:` line naming which of the four inventories it came from, with the original record numbers, so the merge is auditable in both directions.

Where the sources genuinely disagree, the disagreement is stated inside the record and again in **Points where the four inventories disagree** at the foot of this file.

---

## Count table

| Class | Tier 1 | Tier 2 | Tier 3 | Total |
|---|---:|---:|---:|---:|
| **A** — district source records | 62 | 34 | 30 | **126** |
| **B** — project pipeline data | 21 | 7 | 25 | **53** |
| **C** — the project's own analytical errors | 155 | 9 | 5 | **169** |
| **D** — method limitations | 10 | 32 | 2 | **44** |
| **Total** | **248** | **82** | **62** | **392** |

---

## The ten most consequential single findings

1. **A2.1 — the missing-sessions table.** Roughly thirty public sessions across 2023–2026 left no recording, no minutes, or neither; four of them were scheduled and never held, and in three cases what is missing is the cancellation.
2. **A1.4 — the 14 November 2024 Claremont nonpublic session.** Mislettered and truncated exemption, no motion to seal, so RSA 91-A:3, III required disclosure within 72 hours — and no nonpublic minutes exist, no recording exists, and the "Unsealed Minutes" folder built seven weeks later has no 2024 folder at all.
3. **A1.59 — a student-by-name special-education appendix published in the district's public Drive**, listing individual students by full name and grade under headings naming a disability basis.
4. **A2.34 — the scale of the negatives.** Of 129 MAP sections: 29 have no minutes, 17 have neither packet nor minutes, 19 have no packet, 4 have no video — fourteen of the seventeen are Finance Committee meetings.
5. **C1.26 — the reversed reading of RSA 198:4-b, II(a).** It manufactures a false HIGH flag on any vote to retain fund balance, and it nearly shipped on the 16 October 2024 page.
6. **C1.51 — RSA 40:13, II-a's "notwithstanding" clause displaces RSA 32:5's 25-day floor.** Without it every SB 2 budget hearing in the corpus, including the live 15 January 2025 page, would be flagged for a breach that does not exist.
7. **C1.1 — the RSA 91-A:2, II mover/seconder clause was wrongly dated to 2023.** It has bound every meeting here since 1 January 2019, so the error was about to credit districts with voluntary compliance and to miss real defects in 2019–2023 minutes.
8. **C1.151 — SAU 6 does not dissolve on 1 July 2026.** Two officials said it did and the project recorded it as settled background across §28 and several shipped pages; the SAU 6 chair corrects them on tape, and what ends is Unity's membership under RSA 194-C:2, IV.
9. **B1.1 — phantom names at full ASR confidence.** `Nathan Ward, please` is the podium prompt, `Mr. Clark` is the District Clerk, `Leah` is the LEA, `Sussex` is SAU 6 — a class of garble that mints people who were never in the room.
10. **D1.1 — the maintainer's CCTV board seat.** Kevin Tyson maintains this project and has served on the Claremont Community Television (CCTV) / Claremont Community Media Center (CCMC) Board of Directors since 13 July 2022, first in Seat 3, and still does (corrected 29 September 2026); CCTV is the source of every recording in the corpus, and he also appears in the record as a board applicant and a floor speaker.

---
# CLASS A — DISTRICT SOURCE RECORDS

Defects in what the district, SAU 6, or the CCTV archive actually recorded.

## A · Tier 1 — affects what a reader can conclude

### A1.1 · The phantom RSA chapter 92-A, in agendas, minutes and aloud
**Tier 1 · systemic · Sources: briefing A2 · html-briefing A1 · legal-anchors A1, N7**

There is no RSA chapter 92-A: Title VI runs 91-A, 91-B, 91-C, 92, 93-A, 93-B, 98-A, 99-A, 100-A, 101-A, 101-B, 102, 103, and chapter 92 is "Tenure and Oath of Office in Certain Cases". Three SAU 6 agendas carry the citation (12/14/23, 1/11/24, 2/15/24), two sets of SAU 6 minutes repeat it (1/11, 2/15) — including a sentence the clerk composed, "motioned to move into non-public under RSA 92-A:3,II" — and on show 15580 at 0:02:37 the chair speaks it aloud, corrects herself once, and lands on the wrong chapter both times. It stops in SAU 6 paperwork after 15 February 2024; from the 4/11/24 agenda ("Non public meeting session RSA 91-A:3, II (a)") the SAU 6 nonpublic citations are right, but that clearance covers SAU 6 nonpublic-session citations only. The standing instruction is to report it as a defective citation in the document, never to repair it silently to 91-A and never to assume the body meant 91-A:3, II "even though it plainly did" — a helpful repair would manufacture a Right-to-Know holding the agenda never invoked.

*Primary source:* the 12/14/23, 1/11/24 and 2/15/24 SAU 6 agendas; the 1/11 and 2/15 minutes; show 15580 at 0:02:37; https://gc.nh.gov/rsa/html/NHTOC/NHTOC-VI.htm (verified 2026-08-29).

### A1.2 · Claremont by-laws Appendix D counts the nonpublic grounds four different ways
**Tier 1 · one-off document, standing effect · Sources: briefing A3 · html-briefing A8 · legal-anchors A12**

Appendix D of the by-laws adopted 5 June 2024 says RSA 91-A:3 "sets forth eight grounds" in prose, then enumerates nine, then calls them "the nine statutory bases" two paragraphs later, then letters only six (a)–(f) in its compliance checklist — fusing II(d), II(e) and II(g) into one item and continuing the same letter series g–o for procedural steps. The statute runs (a) through (m): thirteen lettered subparagraphs with (f) repealed, so twelve live grounds (2023, 189:1, eff. Oct. 3, 2023). A page adopting the document's count would understate the available grounds and could flag a validly-cited ground as outside the statute. Appendix D also states the 72-hour rule and a nine-item minimum-content list for nonpublic minutes, citing policy BEDG, and its miscounting propagates into the board's own citations (see A1.3).

*Primary source:* by-laws Appendix D, adopted 5 June 2024; https://gc.nh.gov/rsa/html/VI/91-A/91-A-3.htm.

### A1.3 · The 7 August 2024 Claremont minutes cite "RSA 91-A:3, I & II (1)"
**Tier 1 · one-off · Sources: briefing A4 · html-briefing A9 · legal-anchors C39, N33**

Paragraph I of RSA 91-A:3 contains no exemptions at all — it is the procedural entry provision, and I(b) requires the motion to "state on its face the specific exemption under paragraph II", by roll call, majority of members present. "II (1)" is the by-laws' own invented numbering rather than the statute's lettering. A motion or set of minutes citing 91-A:3, I for a subject-matter ground has stated no valid exemption at all. This record is why §20's "the paperwork is right from April 2024" clearance covers SAU 6 only and must never be read across to Claremont: check both bodies separately.

*Primary source:* the 7 August 2024 Claremont minutes; https://gc.nh.gov/rsa/html/VI/91-A/91-A-3.htm.

### A1.4 · The 14 November 2024 Claremont nonpublic session — mislettered, truncated, unsealed and undisclosed
**Tier 1 · one-off · Sources: briefing A5 · html-briefing A28 · legal-anchors A10**

The draft minutes (Drive `1h9fxbyMjj9OxwkICoO6wAaA5B_chW1k2`, filed in `8. CSB 11.20.24`) cite the entry as "RSA 91-A: 3, II (a & d)" and print "(b)" against the text of II(d) — but II(b) is "The hiring of any person as a public employee" and II(d) is the real-property ground, so a reader takes a property discussion for a hiring exemption. They also print II(d) truncated, dropping its operative condition, "which, if discussed in public, would likely benefit a party or parties" — a trailing clause the file records as routinely dropped by district paperwork and the very clause that decides whether the exemption was available. The session ran 8:19–8:59 p.m. with **no motion to seal**, so RSA 91-A:3, III required disclosure within 72 hours, **and no nonpublic minutes exist**. Both provisions are 2023, 189:1, eff. Oct. 3, 2023.

*Primary source:* draft minutes Drive `1h9fxbyMjj9OxwkICoO6wAaA5B_chW1k2`; https://gc.nh.gov/rsa/html/VI/91-A/91-A-3.htm.

### A1.5 · Policy BBBH-S §E cites RSA 194:4 for the duty to provide superintendent services
**Tier 1 · one-off, member of a systemic set · Sources: briefing A6 · html-briefing A2 · legal-anchors A2, N17**

RSA 194:4 is "Notes of Districts" — district borrowing, notes authenticated by the treasurer and school board (1909, 138:1 · PL 119:4 · RL 138:4). It says nothing about superintendent services. The policy was adopted by SAU 6 on 12 September 2024 and is carried in `pending_legal_anchors.md` as a negative anchor; a page treating the citation as good law would have described a borrowing statute as the source of SAU service authority. The correct route is RSA 194-C:5, II(a) → RSA 194-C:4. It is one of the six misdirected district citations enumerated at html-briefing §29f.

*Primary source:* SAU 6 policy BBBH-S §E, adopted 12 September 2024; RSA 194-C:4 at https://gc.nh.gov/rsa/html/XV/194-C/194-C-4.htm.

### A1.6 · Policy DIE attributes an NHDOE filing requirement to RSA 671:5
**Tier 1 · one-off, member of a systemic set · Sources: briefing A7 · html-briefing A3 · legal-anchors A3, N18**

RSA 671:5 contains no NHDOE filing requirement and never mentions the department — it is the election of district auditors at each district election (1979, 321:1; 2010, 262:2, eff. Sept. 4, 2010). Adopted by SAU 6 on 12 September 2024 and filed as a negative anchor. A page repeating the policy would have asserted a state filing obligation that no statute imposes, and might then have flagged non-filing as a violation. Second of the two wrong statutes in the 12 September 2024 SAU 6 policies, and a member of the §29f set of six.

*Primary source:* SAU 6 policy DIE, adopted 12 September 2024.

### A1.7 · By-law 4.03 grounds the clerk's minutes, notice and posting duties in "RSA 671:20 and RSA 671:25"
**Tier 1 · one-off, member of a systemic set · Sources: briefing A8 · html-briefing A4 · legal-anchors A4, N23**

RSA 671:20 ¶I is ballot preparation by the district clerk (1979, 321:1); ¶II — cost-per-pupil and proficiency scores on the ballot — was added 2025, 281:1, eff. Sept. 30, 2025. RSA 671:25 is ballot preparation and delivery to the town moderator (1979, 321:1; 1997, 176:7). Neither says anything about minutes, notice or posting, and a page adopting the by-law's citation would have located the minutes duty in the wrong chapter entirely and missed RSA 91-A:2, II, which actually carries it. The defective citation sits on an otherwise load-bearing rule: 4.03(d) makes posting agenda materials with the agenda a clerk's duty, and is the right anchor for a missing exhibit.

*Primary source:* Claremont School Board by-law 4.03; https://gc.nh.gov/rsa/html/LXIII/671/671-20.htm.

### A1.8 · By-law 1.11 cites "RSA 91-A:II" — a chapter and a paragraph with no section
**Tier 1 · one-off, member of a systemic set · Sources: briefing A9 · html-briefing A6**

The citation is malformed on its face: it names a chapter and a paragraph but omits the section, so it resolves to nothing. It matters because by-laws 1.05(c)–(d) and 1.11 are the rules that send every subcommittee notice and every set of subcommittee minutes to the SAU 6 website — the defective citation is attached to the subcommittee-publication duty itself (see A2.22). Sixth and last member of the §29f set: phantom RSA 92-A; RSA 194:4 (BBBH-S §E); RSA 671:5 (DIE); by-law 4.03's RSA 671:20/671:25; policy JLCK's Ed 306.04(b)(15)/(b)(23); by-law 1.11's RSA 91-A:II.

*Primary source:* Claremont School Board by-law 1.11.

### A1.9 · Policy JLCK misdescribes two Ed 306.04(b) subparagraphs
**Tier 1 · one-off, member of a systemic set · Sources: briefing A10 · html-briefing A5 · legal-anchors A5**

Claremont policy JLCK as adopted 4 February 2026 gives Ed 306.04(b)(15) as "Behavior Management and Intervention for Students" and (b)(23) as "Meeting the Special Physical Health Needs of Students." Under readoption Doc. #14150, eff. 12-13-24, (b)(15) is "Supporting the physical and emotional health needs of students…" and (b)(23) is "Developmentally appropriate daily physical activity pursuant to Ed 310." Both are wrong, and a page quoting the policy's captions as the rule's text would have attributed two non-existent requirements to the State Board. The briefing inventory records only its membership in the set of six; the legal-anchors file supplies the adoption date and the actual rule captions.

*Primary source:* Claremont policy JLCK as adopted 4 Feb 2026; https://gc.nh.gov/rules/state_agencies/ed300.html.

### A1.10 · A district policy cites 42 U.S.C. §218d, which does not exist
**Tier 1 · one-off, easily propagated · Sources: briefing A11 · html-briefing A7 · legal-anchors A11, N13**

The PUMP Act is 29 U.S.C. §218d (Pub. L. 117-328, div. KK, §102(a)(2), 136 Stat. 6093, in force 29 December 2022); 42 U.S.C. §218 is the National Advisory Council on Migrant Health. Copying the policy's citation would have pointed readers at a public-health advisory body as the source of a lactation-break duty. The briefing flags it as "easy to copy" — a citation a page could propagate. It is not counted among the §29f six, which are the RSA and Ed-rule citations. Related negative: 29 U.S.C. §218d(b) does not require compensation for break time, so a board that pays hourly nursing periods exceeds the federal floor and is not thereby irregular.

*Primary source:* the district policy identified in the February–March 2024 wave; "NEGATIVE ANCHOR — there is no 42 U.S.C. §218d."

### A1.11 · Claremont by-laws Appendix A misstates Ed 303.01(f)
**Tier 1 · one-off · Sources: legal-anchors A6, F15**

Appendix A presents the State Board rule as requiring board meetings "at least once a month (except the month of July)." Ed 303.01(f) says "at least once in 2 months" and requires the attendance of the superintendent or designee (New #8583 eff. 3-15-06; ss by #10649 eff. 7-26-14). The by-law is stricter, so no violation turns on it, but it is offered as the State Board's text and is not — a page quoting Appendix A as the rule would have created a monthly-meeting mandate that does not exist. The defect is the misattribution, not an under-meeting; and the rule's pre-12-13-24 vintage is unresolved, so the file directs that it not be flagged until the earlier Ed 300 text is recovered (see D2.24).

*Primary source:* https://gc.nh.gov/rules/state_agencies/ed300.html.

### A1.12 · SAU 6 policy BBBH-S §D lets a single board member demand a weighted vote
**Tier 1 · one-off · Sources: legal-anchors A7**

RSA 194-C:8 provides that weighted votes "shall only be used upon the demand of a majority of the members of any board present and voting" (1996, 298:3, eff. Aug. 9, 1996). Policy BBBH-S §D lets "a board member" demand one. The file records this as "a real conflict with the statute, adopted on counsel's advice that the sentence was needed 'to be in compliance'." A page taking the policy at face value would have treated a single-member demand as lawful and missed the conflict.

*Primary source:* https://gc.nh.gov/rsa/html/XV/194-C/194-C-8.htm.

### A1.13 · The district's nonpublic-minutes form carries the repealed subparagraph (f)
**Tier 1 · one-off · Sources: legal-anchors A13**

`7.21.26 Non-Public Meeting Session Minutes.docx` (Drive `198DxPDMeugFuROP2VygIl9qxjWwmAojJ`) is the district's nonpublic-minutes form, listing all thirteen lettered grounds with tick boxes, and its (f) entry is the repealed adult-parole-board ground. A board ticking (f) would have stated a ground that no longer exists; a page treating the form as authoritative would have reported a live exemption where none remains. The file notes that by July 2026 the board uses a proper instrument, and that for most of the corpus no such document is reachable at all.

*Primary source:* Google Drive `198DxPDMeugFuROP2VygIl9qxjWwmAojJ`.

### A1.14 · Claremont's Rules of Procedure misstate the voter's remedy for a doubted vote
**Tier 1 · systemic · Sources: briefing A16 · html-briefing A17 · legal-anchors A8**

The sheet tells voters that "any voter who doubts the accuracy of any non-counted vote may require the Moderator to determine a vote by a counted show of hands or counted standing vote." Neither statute says that: RSA 40:4-a (2006, 117:1, eff. July 9, 2006) requires 5 voters in writing before a vote; RSA 40:4-b (1971, 524:1; never amended) requires 7 or more immediately after; and in both the remedy is a secret "yes-no" ballot, not a counted show of hands. The same sheet omits RSA 40:13, IV(a) and IV(c) entirely. It appears in 2023 and 2024, is expected in 2025 and 2026, and governs deliberative sessions where the body is the voters rather than the board — so it is the participants' operating instructions, and a page relying on it would describe the wrong threshold and the wrong remedy.

*Primary source:* Claremont's published Rules of Procedure sheet, 2023 and 2024 editions; https://gc.nh.gov/rsa/html/III/40/40-4-a.htm ; /40-4-b.htm.

### A1.15 · Claremont's published default-budget worksheets truncate RSA 40:13, IX(b)
**Tier 1 · systemic · Sources: briefing A15 · html-briefing A18 · legal-anchors A9**

The 2023 and FY25 worksheets quote the default-budget definition with the eliminated-positions clause cut off — stopping before "…and by salaries and benefits of positions that have been eliminated in the proposed budget," and before the exclusion for "vacant positions under recruitment or positions redefined in the proposed operating budget." Independently confirmed from the tape: Mary Henry read the definition aloud almost verbatim and stopped at the same place — in the very year the district eliminated PreK (~$500,000 / 23 identified students, per the 7 January minutes). A page repeating the worksheet would state the formula without the reduction most likely to be contested, and would describe the district's own calculation as complete when the statute requires more. **No default-budget form exists in the December packet or in the 15 January hearing packet at all.**

*Primary source:* Claremont's published default-budget worksheets; https://gc.nh.gov/rsa/html/III/40/40-13.htm ; 2023 codification at law.justia.com.

### A1.16 · "Interim moderator" is not a New Hampshire office, and none was lawfully designated on 3 February 2024
**Tier 1 · one-off, flagged HIGH · Sources: briefing A17 · html-briefing A19 · legal-anchors N9**

All four district documents for 2/3/2024 — agenda, Rules of Procedure, draft and approved minutes — style Charlene Lovett "interim moderator", a title with no statutory basis. RSA 197:26 expressly bars a school board from filling a moderator vacancy ("except that of moderator"; unamended since RL 139:25), and its power over other district offices runs only "until the next annual meeting". The two lawful branches are the clerk presiding (RSA 197:20; RSA 671:33, III) or a moderator pro tempore chosen by the meeting or appointed by the district clerk — neither happened. Elected moderator Tracy Pope is absent from the entire record: not on tape, not in either set of minutes. This is the page's HIGH flag, and the file directs agents to expect the same title elsewhere in the corpus and check it.

*Primary source:* the 2/3/24 deliberative-session record read against RSA 197:26, RSA 197:20 and RSA 671:33, III.

### A1.17 · A chair defeated a postponement by misstating RSA 198:4-b
**Tier 1 · one-off, recorded as a general trap · Sources: briefing A14 · html-briefing A10**

¶I of RSA 198:4-b is the contingency fund — a separate warrant article, limited to unanticipated expenses. ¶II is retained year-end unassigned fund balance (≤5% of net assessment, prior public hearing, 7 days' newspaper notice) and states no purpose limitation at all. On 6 March 2024 a chair told the board that ¶I's "unanticipated expenses" limitation reached ¶II money and used that to defeat a postponement. The paragraph distinction is recorded as a research trap that nearly produced a wrong finding in the other direction as well (see C1.26).

*Primary source:* the 3/6/24 board recording, against the text of RSA 198:4-b ¶¶I–II.

### A1.18 · By-law 2.04 narrows RSA 189:74 and policy BEDH by meeting type
**Tier 1 · one-off by-law, systemic in effect · Sources: html-briefing A15 · legal-anchors A14**

By-law 2.04 confines public comment to "each regular meeting". RSA 189:74 (2022, 333:1, eff. Sept. 6, 2022; never amended) has only two exceptions — ¶II emergency meetings and ¶III meetings held solely for a nonpublic session — and does not distinguish regular from special meetings, which is what defeats the by-law. Policy BEDH (Drive Doc `1fcf5-e0lKvMTRlW7e6NjpCZ6OFQPC-wymYBu0ydf1CE`, first read 17 May 2023, adopted 6 September 2023) likewise requires comment at "all Board meetings", a "minimum of thirty minutes in total", and at §B.3 the chair's "vocal invitation" to the audience. By-law 2.15 subordinates the by-laws to state law, so BEDH governs; every Claremont agenda hyperlinks it at its foot. A page applying by-law 2.04 would conclude no comment period was owed at a special meeting when the statute owes one.

*Primary source:* policy BEDH, Drive Doc `1fcf5-e0lKvMTRlW7e6NjpCZ6OFQPC-wymYBu0ydf1CE`, read against by-laws 2.04 and 2.15 and https://gc.nh.gov/rsa/html/xv/189/189-74.htm.

### A1.19 · Policy BEDH is internally contradictory on public comment
**Tier 1 · one-off, standing · Sources: briefing A22 · html-briefing A15 · legal-anchors N50**

Adopted 6 September 2023 (first read 17 May 2023), BEDH requires comment at "all Board meetings" with a "minimum of thirty minutes in total" in §B, against a procedures clause saying the chair "will close the public comment period after there is no response". Read together with the statutory question at D2.27 — whether the 30 minutes is a floor on the opportunity or on elapsed time — this is why a short comment period cannot be flagged as a violation where nobody was turned away. The countervailing reading is recorded too: B.2 expressly locates the first comment period on non-agenda topics and B.5 requires the chair to open "Board Discussion Regarding Citizens Comments" after closing it, so a chair restricting the first period to non-agenda business is following policy, not narrowing it.

*Primary source:* Claremont policy BEDH, adopted 6 September 2023; by-law 2.04.

### A1.20 · 9/4/24 Exhibit D states the wrong statutory basis for SAU cost apportionment, uncorrected
**Tier 1 · one-off with downstream effect · Sources: briefing A12**

The exhibit reads "Current percentages are based on student population per district", where RSA 194-C:9, I is ½ average daily membership + ½ equalized valuation. Mary Henry corrected it aloud at the table; the document was not changed and the minutes do not record the correction. The board then sent it to Unity characterised as "It's fact. It's data.", and it landed badly at the SAU 6 meeting of 12 September 2024. Two clauses of ¶I that the project's own catalogue had not recorded bear on it: the equalized valuation is that "of each district as of June 30 of the preceding school year", and a new service requires "a majority of the school districts … representing not less than 60 percent of the total pupils" (2003, 279:1, in force from 16 Sept 2003).

*Primary source:* briefing Addendum 16, "Document defects worth carrying"; https://gc.nh.gov/rsa/html/XV/194-C/194-C-9.htm.

### A1.21 · The $420,000 released under RSA 198:4-b, II(a) was re-described as roof money and the minutes adopted the wrong version
**Tier 1 · one-off · Sources: briefing A13, C29**

The 6 March 2024 release was confined by the clerk's own read-back to "unintentional, unanticipated special education costs". Mary Henry corrected the roof attribution twice on tape, at 0:31:43 and 0:31:45; a member restated it anyway and the approved minutes adopted his version. The project inherited the district's error: briefing Addendum 8's "$400,000 from reserves for the Stevens roof" is therefore unsupported (see C1.73). The ASR compounds it — `for $20,000` in the clerk's read-back is $420,000 (see B1.3).

*Primary source:* briefing Addendum 16 §3; the approved 3/6/24 minutes against the recording at 0:31:43–0:31:45.

### A1.22 · A petition cites RSA 32:5-b to create a school district budget cap
**Tier 1 · one-off · Sources: legal-anchors A15, N26**

RSA 32:5-b is the LOCAL TAX CAP, a municipal provision (2011, 234:6 … 2025, 170:1 and 183:1, eff. Sept. 13, 2025). The school district budget cap is RSA 32:5-e / 32:5-f (2024, 353:2, eff. Oct. 1, 2024; 2025, 183:5–7, eff. Sept. 13, 2025). A petition citing 32:5-b while purporting to create a school budget cap has cited the wrong section, and a page validating it would have applied municipal tax-cap mechanics to a school warrant article.

*Primary source:* https://gc.nh.gov/rsa/html/III/32/32-5-b.htm ; /32-5-e.htm ; /32-5-f.htm.

### A1.23 · A statement on the 6 May 2026 recording that RSA 198:4-d allows an extension
**Tier 1 · one-off · Sources: legal-anchors A16, N30**

RSA 198:4-d provides that the report "shall be submitted on or before September 1 of each year" and contains no extension provision (source note ends 2025, 141:401, eff. July 1, 2025). The assertion made on the 6 May 2026 recording is contrary to the section, and a page repeating the speaker's claim would have excused a late DOE-25 on a statutory basis that does not exist. Only the September 1 filing date is safe to rely on for meetings before July 2025 (see C1 vintage records).

*Primary source:* legal-anchors entry "RSA 198:4-d — and a negative."

### A1.24 · A board member's floor claim that RSA 194-C:5 "fixes salaries and benefits"
**Tier 1 · one-off · Sources: legal-anchors A17**

The full ¶III reads that the SAU board "shall fix the salaries of all school administrative unit personnel, shall apportion the expense of the salaries and benefits among the several districts…" — "and benefits" sits in the apportionment clause, not the fixing clause (1996, 298:3, eff. Aug. 9, 1996; never amended). The floor claim is therefore inexact, and a page adopting it would have credited the SAU board with a benefits-setting power the section does not grant.

*Primary source:* https://gc.nh.gov/rsa/html/XV/194-C/194-C-5.htm.

### A1.25 · "The State covers 75%" of CTE construction — a funding practice recited as statute
**Tier 1 · systemic · Sources: legal-anchors A18, N14**

RSA 188-E:3 fixes no percentage: ¶I says the commissioner "shall make grants available to designated regional centers for construction… or renovation, expansion, or replacement"; ¶II is site work. The 75% figure heard repeatedly across this corpus is a funding practice, not a statutory share — the SRVRTC director says as much himself. A page treating 75% as a statutory entitlement would have reported a shortfall against a legal standard that does not exist. Vintage: the section's source note now ends 2025, 190:1, eff. July 1, 2025; use the 2021, 210:2 text for 2023–24 (see C1 vintage records).

*Primary source:* https://gc.nh.gov/rsa/html/XV/188-E/188-E-3.htm.

### A1.26 · "Supposed to fund up to 90%" — catastrophic aid, 11/19/24 finance meeting
**Tier 1 · one-off statement, systemic consequence · Sources: legal-anchors A19**

No 90% figure appears anywhere in RSA 186-C:18 — the file confirms this expressly. The paragraph's two real 80 percents are the department's share of costs above the 3½× threshold up to 10× (2023, 79:141, 142, eff. July 1, 2023) and the 2025 HB 2 §137 entitlement floor. The 11/19/24 statement is a misstatement of the governing rate, and repeating it would have measured FY2025's 67.5% reimbursement against a nonexistent 90% legal benchmark.

*Primary source:* https://gc.nh.gov/rsa/html/XV/186-C/186-C-18.htm ; 2023/2024 Justia codifications.

### A1.27 · The Claremont/Unity tuition agreement names two different approving bodies
**Tier 1 · one-off · Sources: legal-anchors A20**

RSA 194:22 provides that "If the contract is approved by the state board the school with which it is made shall be deemed a high school maintained by the district" (note ends RL 138:21; never amended). The file records it as a LIVE TRAP: the approving body is the STATE BOARD, not the Department of Education, and the Claremont/Unity agreement names both, in different clauses. A page following the agreement's Department clause would have described approval by a body with no approval role, and could have flagged a properly approved contract as defective, or the reverse.

*Primary source:* legal-anchors entry under "RSA 194:2, 194:22, 194:23-b."

### A1.28 · The adopted strategic plan assigns oversight to "the Board of Education," a body NH statute does not create at district level
**Tier 1 · one-off · Sources: briefing A19**

Inside the same adopted plan: the Appendix defines chronic absenteeism as "10 or more unexcused absences in a school year" while the presenter said "10% or more of the school year" (0:15:14) and the adopted measure carries neither; the Fast Facts page classifies SRVRTC as "1 Alternative Program"; and one measurable goal is "Decrease the number of bullying and harassment investigations" — a count of the district's own responses to reports. A reader relying on the plan takes its governance structure, its absenteeism definition and its programme classification from a document that is internally inconsistent on all three.

*Primary source:* briefing Addendum 18; the adopted plan p. 5 and Appendix.

### A1.29 · The SAU 6 board had no statutory secretary through 2023 and no treasurer through 2024–25
**Tier 1 · systemic · Sources: briefing A20 · legal-anchors N39**

RSA 194-C:5, I requires the board to "organize by choosing a chairperson, a secretary, and a treasurer" — and note that vice chair is not one of the three statutory offices, so a reorganization flag over an unfilled vice-chair seat cites nothing. Both 2023 mastheads print only Chair and Vice Chair while the agenda line still reads "Secretary Roll Call of Attendance", and the vacancy runs at least through 17 August 2023. The treasurer vacancy surfaces only when auditor Michael Campo tells the board "the treasurer should review the check register": the 4/10/25 minutes record Hawkins noting "the SAU Board currently has no treasurer", after which Candace Crawford was elected treasurer plus two voucher signers. The 11 April 2024 reorganization had elected only chair and vice chair.

*Primary source:* briefing Addenda 11 (corrections, part 2) and 18; https://gc.nh.gov/rsa/html/XV/194-C/194-C-5.htm.

### A1.30 · No secretary was elected at the 20 March 2024 organizational meeting, though policy BDB requires three officers
**Tier 1 · one-off · Sources: briefing A21**

Policy BDB, adopted 2 January 2019, requires chair, vice-chair and secretary, one-year terms. On 20 March 2024 only chair and vice chair were elected, both by uncounted voice vote taken *before* the roll call. Note the countervailing anchor: under RSA 194-C:8 weighted votes are used only on the demand of a majority present and voting, so an uncounted voice vote is not by itself irregular (see C1 negative-anchor records) — the defect here is the missing office and the sequence, not the voice vote.

*Primary source:* briefing Addendum 14; the approved 3/20/24 minutes; policy BDB read from the live policy index.

### A1.31 · Votes recorded without tallies, movers or seconders
**Tier 1 · systemic · Sources: briefing A53 · html-briefing A35**

Across the corpus almost every vote is a voice vote with no announced tally: the 1/11/24 termination and the Pratt appointment both 10–1–1 with no tally announced and no reason stated by anyone; the 4/11/24 SAU 6 reorganization with no tally for any vote that night; 12/12/24's "Opposed? One. And any abstentions" — one dissent counted, ayes uncounted, no name and no minutes, so the dissenter cannot be identified by anyone; the 3/20/24 officer elections by uncounted voice vote; six subcommittee assignments disposed of by "no objection" with no votes. RSA 91-A:2, II's mover/seconder clause has been in force since 2018, 244:1, eff. 1 January 2019 — re-verified three times against the 2017 and 2019 codifications — so every meeting in this corpus is inside it and the omissions are real defects, not compliance the law did not yet require (see C1.1).

*Primary source:* briefing Addenda 6, 7, 8, 9, 14, 18; RSA 91-A:2, II as codified 2018, 244:1.

### A1.32 · Sealed nonpublic minutes with no announced tally and no RSA 91-A:3, III determination
**Tier 1 · systemic · Sources: briefing A54 · html-briefing A28**

The 1/11/2024 nonpublic minutes were sealed 30 years with no announced tally and no RSA 91-A:3, III determination on the record; the 12/7/23 nonpublic was sealed 99 years with Hawkins voting No, Erickson abstaining, and no tally announced; the 22 May 2024 nonpublic was sealed 10 years; the 14 November 2024 Claremont nonpublic had no motion to seal at all. ¶III's sealing sentence requires a "recorded vote of 2/3 of the members present taken in public session" — those last four words sit inside the operative clause and are the test for a defective seal (2023, 189:1, eff. Oct. 3, 2023).

*Primary source:* briefing Addenda 5, 6; html-briefing §23b, §25d; https://gc.nh.gov/rsa/html/VI/91-A/91-A-3.htm.

### A1.33 · The 14 November 2024 unsealing omitted the one 2024 seal whose term had lapsed
**Tier 1 · one-off · Sources: briefing A55**

The board unsealed eight sets in public session — 13 Jul 2018, 14 Jun 2018, 10 May 2018, 17 Jul 2018, 13 Apr 2023, 11 May 2023, 31 Jul 2023, 17 Aug 2023 — with the chair saying "These minutes will be posted within 72 hours on the website." Nothing from 2024 is on the list, and the 11 April 2024 six-month seal, whose term lapsed 11 October 2024, is missing — 34 days earlier. Item IV.4 was itself added by amendment at 6:31 p.m. and is not on the posted agenda.

*Primary source:* briefing Addendum 17; the 14 November 2024 record.

### A1.34 · The superintendent's contract was transacted off-agenda and no executed instrument exists in any share
**Tier 1 · one-off, eleven-month thread · Sources: briefing A57**

Opened 11 January 2024, when terms were "expressly delegated" to the chair and counsel "for subsequent approval". The whole November 2024 trace is one sentence — the chair at 0:29:39, "We also have to go over the superintendent's contract, which we did not have a chance to discuss tonight" — and neither the 3 December nor the 12 December SAU 6 agenda carries a contract item. It was transacted anyway at the 12 December budget hearing, 43 seconds after the nonpublic session: the chair moved "the 3% salary increase for the superintendent", Whitney seconded, Crawford added the term, restated as "for a two year contract? So for this year, it's 3% increase. And to renew your contract for two years." Voice vote, no count. Still no executed instrument in any share; Exhibit G's December line ("Review Superintendent Contract for renewal every 2 - 3 years(due next in 2025)") is the first document implying a term and was never read aloud. A reader working from the agendas would conclude no contract action occurred.

*Primary source:* briefing Addenda 17 and 18; the 12 December 2024 recording.

### A1.35 · The Assistant Tech Center Director was hired before the board approved the position
**Tier 1 · one-off · Sources: briefing A59**

On 21 August 2024, on tape: Miles — "we've already hired someone for a position that we have not approved"; Pratt — "this is a time sensitive thing, and I had to make the decision", because a prior meeting had failed for want of a quorum (the meeting recorded at A2.1). He apologises on the record.

*Primary source:* briefing Addendum 8; the 21 August 2024 recording.

### A1.36 · A ten-cent-per-meal written agreement was signed by the former business administrator without board approval
**Tier 1 · one-off · Sources: briefing A60**

Recorded in the 10/15/25 draft minutes, described by the briefing as an unmined source that also carries Henry's unpaid disciplinary suspension, Weatherford as acting HR manager, Jennifer O'Neil as interim CMS principal, and tax-rate options of 9.18% / 6.08%. Note the federal ceiling that bounds the subject: 7 CFR 210.14(e), last amended 89 FR 32073, 25 April 2024, provides that "The maximum annual average price increase required under this paragraph shall not exceed ten cents."

*Primary source:* briefing Addendum 19; the 10/15/25 draft minutes.

### A1.37 · Exhibit G proposes finalising board business "through electronic means" in place of a June meeting
**Tier 1 · one-off · Sources: briefing A32**

The proposed pre-populated agenda's June line reads: "NOTE: No June meeting; bulleted items to be finalized through electronic means" — with "Review of Superintendent Evaluation Results" among the bullets. The briefing flags it against RSA 91-A:2-a, which has been in force from 2008, 303:4, eff. 1 July 2008, never amended, and binds the whole corpus: "Communications outside a meeting, including, but not limited to, sequential communications … shall not be used to circumvent the spirit and purpose of this chapter."

*Primary source:* briefing Addendum 16; the 9/12/24 packet Exhibit G; https://gc.nh.gov/rsa/html/VI/91-A/91-A-2-a.htm.

### A1.38 · 21 November 2024 SAU 6 — no quorum at 6:30, business before the gavel, citizens' comment minuted as "none" but never called
**Tier 1 · one-off · Sources: briefing A31**

There was no quorum at 6:30; the DMGroup strategic-plan presentation ran before the gavel; the board was called to order at 0:44:57 and adjourned at 0:50:40 — five minutes fifty seconds of meeting after forty-five minutes of business. Citizens' comment, noticed on the agenda and recorded in the minutes as "none", was never called, while members of the public were in the room and had been speaking. A reader taking the minutes at face value concludes no one wished to speak. (The same documents' header-date error is recorded separately at A3.3.)

*Primary source:* briefing Addendum 18; the 21 November 2024 recording and minutes.

### A1.39 · The 10/18/23 approved minutes account for only five of seven members
**Tier 1 · one-off, with an internal source conflict · Sources: briefing A48, C20**

The approved minutes read `Absent: Jennifer Gallagher`, four present, one absent — Bonnie Miles and Whitney Skillen appear in neither column. **The briefing set is internally inconsistent here and says so:** Addendum 5 states the minutes "wrongly recorded her present", and the Addendum 11 correction of 2026-08-29 states flatly that "the second half is FALSE", confirmed independently by two agents against the document. The likelier reading is that Miles was a second, unrecorded absentee — the 11/1 minutes attribute the minutes-correction request to Bonnie Miles, and the chair's on-tape reply "You're documented as being on there" only fits a member the 10/18 minutes did *not* list as absent; Miles never speaks on the 10/18 recording while Skillen speaks nineteen times. This is disagreement 1 of the five carried forward at the foot of this file, and it is the premise whose collapse leaves the `15357` Speaker-4 cluster unresolved (C1.65).

*Primary source:* the approved 10/18/23 minutes; the 11/1/23 minutes; briefing Addendum 5 against Addendum 11.

### A1.40 · The 17 January 2024 minutes conflict with the recording on the mover, on a question's author and on a tax figure
**Tier 1 · one-off · Sources: briefing A49**

The minutes read "Whitney Skillen amended the motion… Jennifer Gallagher seconded", while the recording has the chair addressing the mover as Jennifer/Jen three times and the second is unattributable. Skillen and Miles are recorded present and are never heard or named — zero occurrences of either surname or any variant. The minutes give the benchmark question to Bonnie Miles; the CSV gives it to Arlene Hawkins. The minutes print $69.33 per $100,000 where Henry says $69.39, twice. And the approved minutes are the draft word for word, so nothing was corrected between them.

*Primary source:* briefing Addendum 13; the 1/17/24 draft and approved minutes against the recording and the dialogue CSV.

### A1.41 · The 5 June 2024 approved minutes credit two incompatible speakers
**Tier 1 · one-off · Sources: briefing A50**

They credit the Alex Herzog tribute to Patrick O'Hearn and the by-laws motion to Mike Petrin, but the diarizer places both inside the same four-utterance cluster. Both cannot be right, and the instruction is to report rather than resolve it.

*Primary source:* briefing Addendum 15; the approved 6.5.24 minutes against the dialogue CSV.

### A1.42 · The 15 May 2024 recording and that meeting's own minutes give different Capital Improvements membership
**Tier 1 · one-off, resolved as a project artefact · Sources: briefing A51 · html-briefing §23c**

The recording appeared to yield "Whitney + Sprague + Crawford"; the approved 5/15 minutes and the 4/17 minutes give the chair as Miles. The apparent conflict dissolved: the recording reading was itself a CSV-label artefact (B1.13), and the surviving point is that briefing Addendum 7's "later readings drift" needs that qualification (C1.70). Recorded here because on its face it presented as a district-record contradiction and was carried as one.

*Primary source:* briefing Addendum 14; html-briefing §23c.

### A1.43 · The 2 October 2024 minutes erase the meeting's only ESSER mention
**Tier 1 · one-off · Sources: briefing A52**

At 0:09:13 school counsellor Amelia Rhines says "this was the last summer of the summer school staff funding coming from Esser funds. So starting next year will have to be in the Stevens High School budget…" No board member takes it up. The minutes render it as "summer school is funded by a grant" and contain no occurrence of the word ESSER. The 18 September minutes, approved by consent that same night, had promised "Mary Henry will share a summary report of ESSER funding and where the FY24 budget stands in October" — and on 2 October there was no finance item, no superintendent's report item at all, Henry absent, and none of the four Finance Subcommittee dates printed on that agenda falls in October (12 Nov – 18 Dec).

*Primary source:* briefing Addendum 17; the approved 10.2.24 minutes against the recording at 0:09:13.

### A1.44 · The 21 August 2024 approved minutes contradict themselves within four lines
**Tier 1 · one-off · Sources: briefing A25**

The amendment titles the post "acting assistant CTE director" while the main motion four lines later says "with the amendment in the title to 'assistant'". The same passage carries the typo `Voten taken`. The vote counts on those two motions were themselves mis-recorded by the project and corrected: the title/amendment vote was 5–2, not 6–1 (C1.71).

*Primary source:* briefing Addendum 16; approved CSB minutes 8.21.24, item IV.4.

### A1.45 · The 7 August 2024 minutes style Matthew Upton "Claremont District Attorney"
**Tier 1 · one-off · Sources: briefing A18**

New Hampshire has county attorneys; there is no district attorney. Upton is the district's counsel, not a prosecutor, and a reader taking the minutes at face value concludes a prosecutor addressed the board.

*Primary source:* briefing Addendum 16, "Document defects worth carrying"; the 7 August 2024 minutes.

### A1.46 · The by-laws were adopted on a bare quorum, and the adopted text is not the noticed draft
**Tier 1 · one-off · Sources: html-briefing A16**

On 5 June 2024, "Mike Petrin made a motion to approve the by-laws as presented, Bonnie Miles seconded; voice vote taken, all present voting in favor", corroborated on show 15786 at 0:41:52 — with four of seven members present, the bare quorum, and the member who had dissected the draft on 20 March absent. The text adopted is not the 20 March draft: the chair reported "all SAU and Unity portions have been taken out." From 5 June 2024 onward these by-laws are a governing document every Claremont page must be checked against.

*Primary source:* the 6/5/24 minutes and show 15786 at 0:41:52.

### A1.47 · The 9/4/24 approved minutes state 0.05% where the arithmetic gives 0.508%
**Tier 1 · one-off · Sources: briefing A35**

$193,000 ÷ $38,000,000 = 0.508% — ten times the figure printed — and the wrong figure carried the characterisation "It's minuscule."

*Primary source:* briefing Addendum 16; the approved 9.4.24 minutes.

### A1.48 · The FY25 retention ceiling is published $2,335.57 above the maximum the business administrator stated
**Tier 1 · one-off · Sources: briefing A36**

Henry states the statutory maximum as $466,664.43; within four minutes everyone in the room says "469", the approved 16 October minutes publish "$469,000", and the board twice discussed retaining "the full 469". The board actually voted "to retain up to $350,000 with the stipulation that it be used to offset the 25/26 tax rate" — so a page saying the board *retained* $469,000 would be wrong. That $350,000 was earmarked for FY2025–26 and is never mentioned in the budget built on 13 December.

*Primary source:* briefing Addenda 17 and 19; the approved 16 October 2024 minutes.

### A1.49 · The FY24 close was never reconciled, and the worksheet that would settle it is missing from the packet
**Tier 1 · one-off · Sources: briefing A37**

Three figures are in play — $544,145.29, $648,931.76 and $583,931.76 — and on 16 October nobody speaks any of them; the entire reconciliation is Petrin's "Does this say these numbers take into account the roofs that we were doing?" answered "Yes. They're all done." The board works from $497,000 with no bridge to September's figure. **Exhibit B — cited on the agenda and in the minutes — is absent from the eight-document packet.** And $544,145.29 is an *exhibit* figure, never a minuted one: the approved 18 September minutes print only "At about $540,000", "Down about $60,000 after roof projects", "a revenue surplus at about $210,000". The project's own transposition of these figures is corrected at C1.72, which leaves a ~$584,000 ambiguity the board never resolved.

*Primary source:* briefing Addenda 17 and 19; the 16 October 2024 packet and minutes.

### A1.50 · The Capital Improvements minutes of 10 December 2024 price one roof item twice
**Tier 1 · one-off · Sources: briefing A38**

"SHS Roof Replacement, final section $96,000" and, two paragraphs later, "the third phase of the SHS Roof Repair at $98,000" — against 16 October's "Yes. They're all done." Capital Improvements Reserve Fund balance $150,000.

*Primary source:* briefing Addendum 19; the 10 December 2024 Capital Improvements minutes.

### A1.51 · The SAU 6 FY26 budget sheet advertises a decrease on an appropriation that rises
**Tier 1 · one-off, three documents · Sources: briefing A39**

V1 (14 Nov) prints "Total Budget % Increase 7.23%" on a gross rise of $305,000.54 = 12.25%; V2 (3 Dec, never presented) prints 7.22% against 12.24%; V3 prints −0.67% against +4.35%. The headline crosses zero, and the comparison is net FY26 against gross FY25 — the FY25 ledger in the same packet foots to $2,489,151.00 with no revenue lines. The 7.23% is net of $125,000 of revenue, and the superintendent had to prise the gross out of the presenter: "the real number isn't really 180,000" / "No it's 305".

*Primary source:* briefing Addenda 17 and 18 (three-version table); the FY26 SAU 6 budget sheets V1–V3.

### A1.52 · The adopted SAU 6 FY26 figure appears in none of the packet documents and no total or percentage was ever stated aloud
**Tier 1 · one-off · Sources: briefing A40**

$2,755,723 was produced orally by the business administrator ("Are you ready. 2,755,000. Make it even $723.") and appears in none of the eight packet documents; against FY24 actual expenditure it is +18.06%. In the whole 55½-minute hearing no total, no increase and no percentage was spoken — the tokens `2,794 / 2794 / 2,489 / 2489 / 7.23 / 12.25 / 305 / 180 / apportion` appear nowhere in the 489-row CSV. The chair asked at 0:39:34 and got "I would have to figure that out because I don't know." No member of the public attended.

*Primary source:* briefing Addenda 9, 17, 18; the 12/12/24 hearing recording and packet.

### A1.53 · The FY26 default budget — a figure delivered to the dollar five hours after being called an estimate, then moving $2.98M in 28 days
**Tier 1 · one-off · Sources: briefing A41**

At about 2:24 p.m. on 18 December 2024 the chair asked the Finance Committee for the default budget and was told "I'm working on that tonight… I will get you a rough estimated number"; at about 7:25 p.m. the board was given $39,791,261, to the dollar, and it appears in no document in either packet. By the 15 January approved hearing minutes it is $42,772,778 — +$2,981,517, +7.49% in 28 days after "some minor changes" — and proposed FY26 came in at $42,933,564, i.e. $160,786 *above* the default, reversing the December expectation.

*Primary source:* briefing Addendum 19; the 18 December 2024 recordings and the 15 January approved hearing minutes.

### A1.54 · SAU 6 ledger controls — spending against zero or absent appropriations
**Tier 1 · systemic · Sources: briefing A43**

From the FY25/FY26 packets: HR cell phone $1,000.00 spent against a $0.00 appropriation; business office $2,000 vs $1,000; superintendent $2,500 vs $2,100; SPED mileage $1,439.07 vs $1,250 (the 4/10/25 minutes concede it "should have been budgeted for $2500"); Supt Dues & Fees $10,853.64 vs $8,450; SPED Supplies $3,301.48 vs $600; negative FY24 actuals of ($5,907.78) and ($241.95); and Supt Office Salaries FY24 actual $570,258.79 against an FY25 budget of $475,229.15. Exhibit A adds: superintendent's office salaries over by $107,204.88 (−23.49%), business-office contracted services over by $24,905.87 (−498%), maintenance telephone $4,000 budgeted / $0.00 spent, FY23 mileage exactly $2,500.00 on two lines against FY24 $0.00 on both.

*Primary source:* briefing Addenda 16, 17, 18; the FY25 and FY26 SAU 6 packets, Exhibit A.

### A1.55 · "Auditors $0.00" across years in which three years were unaudited
**Tier 1 · systemic · Sources: briefing A44**

Exhibit A shows Auditors $10,000 budgeted, $0.00 spent; the FY26 ledger shows $0.00 in FY23 and FY24 against three unaudited years. The wider backlog: FY2022 not issued until 2025; as of November 2024 FY21 nearly done, FY22/FY23 targeted before 6/30/2025, FY24 unpromised, cash reconciled back to 2020, three years still unaudited at SAU 6. The legal frame matters and cuts against an automatic finding: RSA 21-J:19 is permissive and does not name SAUs, so no located NH statute requires an SAU annual audit — treat a late audit as a control weakness, not automatically a missed statutory deadline (C1.15).

*Primary source:* briefing Addenda 2, 8, 16, 17; Exhibit A and the FY26 ledger.

### A1.56 · The Region 10 agreement carries a wrong region name twice, a dead cross-reference, and an unmentioned money split
**Tier 1 · one-off · Sources: briefing A46**

The "Region 17" error appears twice — in section II (amended) and in section IX.2, uncorrected; IX.1 cross-references "paragraph 19", which does not exist; and VII.7 splits regional tuition reimbursement "80% Newport, 20% Claremont", a term never mentioned at the table. Clause XIV.3 requires signature "by the chairs", with three notarised blocks reading "Chairperson, … School Board" and no superintendent signature line anywhere — which is why the approved 9/4 minutes' "for the Superintendent to sign the agreement" is wrong; the tape has Petrin saying "Our school board chair to sign."

*Primary source:* briefing Addendum 16; the Region 10 agreement and the approved 9.4.24 minutes.

### A1.57 · The Finance Committee reached a number that never entered the board's record
**Tier 1 · one-off · Sources: briefing A62**

On 18 December 2024 the committee converged on a fully loaded FY26 increase of 5.5% on an FY25 base of $36,349,753 (draft $1,128,543 over after revenues, 8.91% gross, about $800,000 for two unratified CBAs), then: Sprague "Well, I'm going to throw out 4%" → Whitney "We want the total number to be a 4% increase" → Crawford "Just find me 200,000" (≈4.5% fully loaded) → Pratt "you got our orders." No motion, no second, no vote, no roll call, no adjournment. The approved 12.18.24 board minutes dispose of the Finance item in three sentences telling the public to watch the CCTV recordings.

*Primary source:* briefing Addendum 19; the 18 December 2024 Finance recording and the approved 12.18.24 minutes.

### A1.58 · The record contains two incompatible characterisations of what happens to SAU 6 on 1 July 2026
**Tier 1 · systemic · Sources: html-briefing A46 · briefing C48**

The Claremont staff report of 27 March 2026 (Drive `16M5jaunMtgwaVWRIi_iojNp2FgqMcl1W`) reads "It is anticipated at this time that SAU 6 will dissolve as a legal separate entity from the Claremont School District", and two officials said the same at the 18 February 2026 meeting — while the SAU 6 chair corrects them on tape at show 17307, 0:35:20: Whitney, "the saw is dissolving"; Ruggeri, "It's not. It's not dissolving. Just to clarify." and "It would just be the Claremont board at that point, but it would still be the same. Six." The 15 April 2026 approved Claremont minutes agree that Unity is withdrawing "and it will only be Claremont in the SAU as of July 1, 2026". The only legal mechanism any record identifies is Unity's withdrawal under RSA 194-C:2, IV; the unit continues with one district. A page quoting either characterisation is quoting accurately, and a district document that says "dissolve" must not be silently corrected. The project's own adoption of the dissolution as settled background is recorded separately at C1.88.

*Primary source:* the 27 March 2026 staff report, Drive `16M5jaunMtgwaVWRIi_iojNp2FgqMcl1W`, against show 17307 at 0:35:20 and the 15 April 2026 approved Claremont minutes.

### A1.59 · A student-by-name special-education appendix published in the public Drive
**Tier 1 · one-off, the most severe privacy exposure · Sources: briefing A83 · html-briefing A41**

The 5/3/23 packet's Special Education Director's Report carries an appendix listing individual students by full name and grade under headings naming a disability basis, in the district's public Drive folder. The standing rule is to reproduce no name, grade or count; to describe the exposure; to cite FERPA (34 CFR 99.3, 99.30(a); 20 U.S.C. §1232g(b)(1)) and IDEA (34 CFR 300.622(a)); and to grep the finished page against the names so the page does not become a second copy of the disclosure.

*Primary source:* the 5/3/23 packet, Special Education Director's Report appendix, in the district's public Drive folder.

### A1.60 · Two donor cheques published with bank, cheque number and the full MICR line legible
**Tier 1 · systemic (two instances, four and a half months apart) · Sources: briefing A84, A85 · html-briefing A42**

The 4/17/24 packet Exhibit B is a photograph of a donor's cheque with bank, cheque number and account/routing digits legible; the 9/4/24 packet Exhibit A is a second donor cheque with the full MICR routing/account line legible. The repetition four and a half months later is what makes it a pattern rather than an accident. Reproduce none of the numbers, and cite RSA 91-A:5, IV noting that it *permits* withholding rather than requiring it — it is not authority for publishing anything, and it is permissive in both directions (see C1.25).

*Primary source:* the 4/17/24 packet Exhibit B and the 9/4/24 packet Exhibit A.

### A1.61 · 6/5/24 Exhibit D — the CCTV roster carries home addresses, personal phone numbers and e-mail addresses
**Tier 1 · one-off · Sources: briefing A86**

The exhibit carries home addresses, personal phone numbers and e-mail addresses for nine named individuals. Describe, reproduce nothing. The same exhibit is the document that establishes the maintainer's CCTV board seat (D1.1), and it is a two-column PDF whose column order cannot be trusted on extraction (D2.6).

*Primary source:* the 6/5/24 packet Exhibit D.

### A1.62 · A student named in the district's own 2/21/24 Exhibit A
**Tier 1 · one-off · Sources: briefing A87**

"Aubree Herzog" appears in the district's own exhibit. The instruction is explicit — "Student privacy: do not print this on a page" — even though the district published it. The corpus separately carried the spelling "Aubrey"; the district document settles it as Aubree, and the surname collides with Alex Herzog and with a third Herzog, Shawn/Sean (Title I at Maple), none of whom may be merged (D1.8).

*Primary source:* briefing Addendum 14; the district's 2/21/24 Exhibit A.

---

## A · Tier 2 — affects what a reader can find or verify

### A2.1 · The missing-sessions table — public sessions that left no recording, no minutes, or neither
**Tier 2 · systemic · Sources: briefing A1 · html-briefing A20–A33 · map+pages §1a, §1e**

Every row the four inventories record, merged. The absences at 3 April and 1 May 2024 were established by **enumerating** the Cablecast archive (shows 15672–15687 and 15721–15734) and the full 2024 Drive packet share rather than by searching, and the archive carries other programming on both dates, so neither is an outage.

| Date / session | What exists | What does not |
|---|---|---|
| **17 May 2023** Claremont board | nothing; policy BEDH's own history block (first reading 17 May 2023) proves it happened | minutes in any share; the district's own minutes numbering skips it (7 = 5/3, 8 = 6/7, 9 = 6/21); searches on `5.17.23`, `May 17`, `5-17-23`, `051723`, `5.17.2023` all return nothing. Two policies had their first reading there. The recording **failed** — the chair on the record: "We do have some issues with May 17th, 2020 [2023] minutes" |
| **16 May 2023** retreat | minutes, filed as **"Retreat Minutes May 16, 2020"** — file name and heading three years wrong; a **quorum, 6 of 7** | notice (none located) |
| **12 October 2023** SAU 6 | minutes (they carry the contract/policy dispute); they reached the 11/9 packet folder 28 days after the meeting | no recording, no agenda and no folder anywhere in the district's shares; no transcript in the corpus |
| **10 January 2024** finance working session, 9 a.m. at the SAU office | only two packet exhibits — `Exhibit D- Claremont FY25 Proposed Budget Updated 1-10-24 Finance Committee` and `Exhibit E- Claremont Summary Page 1-10-24` (filed under MAP §39). Eight function movements between the two published summaries sum **exactly to $196,001.10** | notice, recording, minutes. Decided on camera 5 Jan (1:42:26) not to televise it; set at 1:50:49 |
| **29 January 2024** working session | minutes only — `Minutes from CSB working session 1.29.24 (1).pdf`, Drive `1cUypy-yz4rC3KT9vRLmMia7-mLXk5M7F`, in `4. CSB 2.21.24`, approved on the 21 Feb consent agenda; three pages of substantive business — slide-by-slide assignment of the deliberative presentation, wording changes to the district's public case, and a direction to move to restrict reconsideration | notice, attendance, times, location, video, MAP §. Announced on the 1/17/24 recording and in its minutes as **24 January at 6:00 at the Dow** — a different date |
| **3 April 2024** | *nothing* | everything — scheduled on the 20 March agenda with ESSER-balance and pre-populated-agenda items; no cancellation anywhere; packet sequence runs `6. CSB 3.20.24` → `7. CSB 4.17.24`; the 17 April consent agenda approves the **20 March** minutes, skipping it; the by-laws, deferred to "our next meeting", appear on neither the 17 April nor the 15 May agenda |
| **1 May 2024** | *nothing* | everything — scheduled in the 17 April minutes |
| **11 May 2024** retreat | minutes, Drive `1zDKtSVGmFjjT3aMlrsP_R4-iPTYtpN5N` — **5 of 7 + clerk**, SAU 6 conference room, 10:00–noon; a written action item, "Establish a norm that the board will meet in a non-meeting or non-public once before collective bargaining…" | notice. Announced on 17 April as "10:00-11:00 **at the Teal Lantern**" — wrong venue and wrong end time. Minutes 7 business days late |
| **22 May 2024** | minutes, Drive `1UJPYxAD3cTgcFNO8FKz7QprHoDxC0y2i` — 6:00 call to order, nonpublic under 91-A:3, II(c) 6:10–6:45 on roll-call votes, **sealed 10 years** | video, packet, MAP §. This is the likeliest date of Pratt's permanent appointment |
| **29 May 2024** SAU 6 retreat | minutes — quorate, 8 of 12 + superintendent + clerk, "Goodwin Community Room" (*sic*; every other document says Goodrich), 6:00–8:00 p.m. | recording, MAP section; folder `4. SAU Retreat 5.29.24` sits **unmapped at MAP line 6135**. Draft minutes reached Drive 2024-09-11 = the **73rd** business day |
| **13 June 2024** SAU 6 | nothing | the meeting **was never held** — chair on tape 12 Sept 2024 at 0:36:43: "Things were in our packets from the June meeting that we did not hold." MAP §45's negative upgrades from "no record exists" to "did not happen" |
| **between 20 June and 7 Aug 2024**, Claremont — failed for want of a quorum | *nothing* | notice, agenda, minutes, folder, video, MAP section. Four independent mentions on the 21 Aug recording (Pratt 0:49:26; Miles 0:49:38 and 0:49:44; Petrin 0:57:33) and the approved minutes ("was on a previous board agenda but there was not a quorum"). It is not 20 June (six present) nor 7 August (six present, item absent from its agenda). **No member names a day** |
| **7 August 2024** | draft minutes `1gMCLl0rvbUw7I8-rB_t-OKIAw-iRnjdr`; packet folder `1. CSB 8.7.24` | **recording, Cablecast show, MAP §** — a full regular meeting with a consent agenda, counsel presentation and a nonpublic session |
| **6 November 2024** | packet folder `7. CSB 11.6.24` | **no minutes were ever created**; closed as **never held** — Cablecast 16140/16141 are both 3 Nov, 16142 is SAU 6 on 14 Nov, other programming on 1, 3 and 4 Nov; the 20 Nov consent agenda approved "10.16.24 & 11.14.24", skipping it; the 14 Nov minutes show a *separate special* meeting, not a rescheduled regular one |
| **12 November 2024** Finance | nothing | the announced first public budget meeting "either did not happen or was not recorded" — nothing in the 11/19 file refers back to it and every presenter treats 11/19 as their first pass |
| **14 November 2024, 8:16 p.m.** Claremont special meeting (same night as the SAU 6 meeting, same room, five of the same people) | draft minutes `1h9fxbyMjj9OxwkICoO6wAaA5B_chW1k2`, in `8. CSB 11.20.24` | packet folder, MAP §, **and no recording** — Cablecast 16143–16154 each fetched, all other programming, and 16153's own event date is 14 Nov so CCTV was operating. Nonpublic 8:19–8:59 with no motion to seal and no nonpublic minutes (A1.4). Settles MAP line 6159: that file records the **Claremont** meeting, not the SAU 6 one |
| **3 December 2024** SAU 6 | agenda (posted 11:13 a.m. on its own meeting day) | the meeting **failed for want of a quorum**; also one of the four sections with no Cablecast recording; no minutes in either share — the next folder `5. SAU6 12.12.24` carries 11/14/24 and 11/21/24 drafts but nothing for 12/3/24 |
| **4 December 2024** Finance | nothing | no public record; noticed in the approved 16.10.24 minutes and on the 20.11.24 agenda |
| **12 December 2024** Finance | nothing | no public record; noticed as above |
| **12 December 2024** SAU 6 | recording; packet | **no minutes published in either share.** Written, circulated and approved **119 days later** — the 10 April 2025 draft SAU 6 minutes, Drive `1KcmceeO49Fd392oO_RBk86who2DyTLkT` in `6. SAU6 6.12.25`, record their approval. MAP §63 should say so; the next SAU 6 packet folder is six months later |
| **13 December 2024** Finance | a recording | **no posted notice found.** Announced on camera nine days ahead (4 Dec recording 1:08:04–1:12:30 and the approved 4 Dec minutes). Five district documents publish the Finance dates as **Nov 12, Nov 19, Dec 4, Dec 18, all 1–3 PM**; 13 December is on none of them and it was a **morning** meeting |
| **18 December 2024** Policy subcommittee | nothing | announced on tape, no record |
| **Christmas week 2024** Finance session | nothing | announced on tape, no record |
| **2 January 2025** Claremont | nothing | announced and **never held**; closed three ways by the 7 Jan minutes (consent line "Minutes Approval-**none**", future dates skip it, the four policies promised for 2 Jan — KCD, JRA, GBEAA, JFABD — taken up on 7 Jan). **The business moved; what is missing is the cancellation** |
| **13 February 2025** SAU 6 | nothing | **cancelled**, per the 12/12/24 recording at 1:08:10, the 3 Dec agenda and the 4/10/25 minutes. Explains the six-month folder gap; **no MAP section is owed** |
| **6 October 2025** Claremont, 5:30 p.m. | recording — **show 16881** (a shipped page wrongly said there was none; MAP §96 had conflated it with SAU 6's 6:00 p.m. show 16882, now split into §96 and §96a) | **no minutes exist and none were ever approved.** The approved 12/3/25 minutes list 9/17, 10/1, 10/15, 11/5 and 11/19 and omit 10/6; the clerk's maternity leave left the board with no minute-taker for six weeks and the 12/3 minutes thank Sherry Williams for the backlog, in which 10/6 was never included. Folder `9. CSB 10.6.25` holds one document, created 2025-10-03T17:02:57Z with the agenda six seconds later — about **76 hours' notice** |
| **21 August 2025 · 26 August 2025** SAU 6 | minutes filed in later folders | no Cablecast recording |
| **26 and 30 March 2026** Claremont special meetings | approved minutes, per MAP.md | no video, no packet folder, no MAP section |
| **28 May 2026** SAU 6 | agenda, Drive doc `1z95pRjknlr4unl7TKBbZyaZrLe-CakIgHrRwLuauQMI`, folder `14. SAU6 5.28.26`, MAP §120 | **no minutes and no recording** — and it is the meeting carrying the Unity separation as five action items. Also one of the four no-recording sections; nothing has been added to the folder since 2026-05-22 |

*Primary source:* html-briefing §§8, 23b, 24a, 25d, 26d, 27b, 27f, 29d; briefing Addenda 11, 13, 16, 17, 18, 19; MAP.md §§20, 25, 31, 45, 61, 63, 96, 96a, 120.

### A2.2 · Meetings with a packet folder but no minutes anywhere in either share
**Tier 2 · systemic · Sources: map+pages §1a**

MAP.md's own table, preserved. Fourteen sections where a packet exists and the minutes do not.

| § | Meeting | Defect |
|---|---|---|
| 20 | Claremont School Board — 9/6/23 | "**No minutes found for this meeting in either share.**" The 2023 Meeting Minutes folder (`1TeuCGSKrQNrrBV1yvgd1_R_epbE1DPyQ`) jumps `13. CSB Meeting Minutes 8.16.23` → `14. CSB meeting minutes 9.20.23`; the next packet folder `21. CSB 9.20.23` carries only the 9.20 and 10.4 drafts; quoted-date search returns nothing — verified 2026-08-28 |
| 31 | SAU 6 Board — 12/7/23 | "**The minutes of this meeting EXIST, were approved, and are in no public share — verified exhaustively 2026-08-29.**" The 12/14/23 draft records "Approval of Minutes 12.7.23", a floor correction (Erickson's abstention, audible at 0:30:26), and "Rocco Ruggeri moved to approve the minutes as amended, Atonya Hart seconded; unanimously approved." All 19 SAU 6 folders dated after the meeting were opened (`16. SAU6 12.14.23` through `14. SAU6 5.28.26`), plus the packets-share root and the Claremont 2023/2024 Minutes year folders (46 files, all CSB). "**December 7 is the single break in this board's filing chain.**" |
| 45 | SAU 6 Board — 4/11/24 | **No approved-form version** in any public share; **no minutes of the 4/11/24 nonpublic session** anywhere (sealed six months); draft approved 9/12/24, **154 days after the meeting** |
| 61 | SAU 6 Board — 12/3/24 | No minutes in either share. Next folder `5. SAU6 12.12.24` carries 11/14/24 and 11/21/24 drafts but nothing for 12/3/24 |
| 63 | SAU 6 Budget Public Hearing — 12/12/24 | No minutes in either share. Next SAU 6 packet folder is `6. SAU6 6.12.25`, **six months later**, carrying only the 4/10/25 draft |
| 93 | SAU 6 Board — 9/11/25 | "No minutes for this meeting have been posted." |
| 95 | Claremont School Board — 10/1/25 | No minutes in the Meeting Minutes share (2025 and 2026 year folders checked). DRAFT only, in the 11/19/25 packet folder: `draft CSB Meeting Minutes 10.1.25.docx.pdf` (`1VQqJ-CHaL-AAti-z9lt3pHc12oopmXSp`) |
| 96 | Claremont School Board, Special — 10/6/25 | "**No minutes exist for 10/6/25 and none were ever approved**" — see A2.1 |
| 96a | SAU 6 Board, Special — 10/6/25 | No minutes posted |
| 99 | SAU 6 Board — 11/13/25 | No minutes posted |
| 116 | SAU 6 Board — 4/9/26 | No minutes posted. "The newest SAU 6 minutes in either share are still the 9/4/25 draft, and the two folders that follow this one carry no minutes at all." |
| 120 | SAU 6 Board — 5/28/26 | No minutes posted; newest folder in the SAU 6 share — "nothing has been added to it since 2026-05-22" |
| 125 | CSB Goal Setting — 7/29/26 | No `Minutes:` line at all (folder `2. 7.29.26 -- Goal Setting Meeting`, 2 documents) |
| 128 | Claremont School Board — 8/19/26 | Packet folder holds only the draft agenda as of 8/25/26 (Drive last-modified 8/14/26, **five days before the meeting**); the section note says no minutes have appeared (2026 and 2027 year folders checked, plus a Drive search for "8.19.26"; re-verified 8/25/26). **The note is now stale relative to its own header line**, which links a `8.19.26 DRAFT CSB Minutes` Google Doc added 8/28/26 |

*Primary source:* MAP.md §§20, 31, 45, 61, 63, 93, 95, 96, 96a, 99, 116, 120, 125, 128.

### A2.3 · The Finance Committee series — no packet folder and no minutes, fourteen sections
**Tier 2 · systemic · Sources: map+pages §1b · briefing A61 · html-briefing A29**

§27 (11/30/23), §28 (12/1/23), §29 (12/6/23), §32 (12/13/23), §34 (12/18/23), §37 (1/5/24), §58 (11/19/24), §64 (12/13/24), §65 (12/18/24), §67 (1/6/25), §102 (12/10/25), §103 (12/12/25), §123 (6/19/26), §127 (8/12/26). The standing text: "**No packet or minutes found in either district share.** The main packets share has never carried a Finance Committee folder" — checked against the year's packet archive, both candidate year folders in Meeting Minutes, the next board meeting's packet folder, and keyword searches on `finance` and the quoted dotted date; verified 2026-08-28, and the nine 2023–24 finance meetings were "checked three ways for each." The single corpus-wide exception is `Exhibit B- Meeting Minutes Finance Subcommittee 7.22.24`, filed as a board exhibit inside the 8/21/24 packet (§50). The district-owned [Claremont Finance Sub Committee] folder `1tRpGMsplz7AVzNThjhWtl7yOHiCiNZmn` (owner `sau6webmaster`) exists but is **empty**, verified 2026-08-23, as does [SAU6 Board Packets (Web)] `1cH2iJq_AugeT1V3kOJAEN4Xdirs28xHT`. The only Finance minutes the index holds at all for these dates are two 2026 files owned by this project's maintainer, not by the district — which is itself a disclosure item (D1.1). The comparator that makes this a finding rather than a bare negative: `10. CSB 12.18.24` contains `CSB Visioning Sub 12.9.24.docx.pdf` and `Cap Improvements Committee Meeting minutes 12.10.24.pdf`, so two other subcommittees minuted their December meetings and the district filed them, while Finance filed none for any of its three televised sessions.

*Primary source:* MAP.md §§27, 28, 29, 32, 34, 37, 58, 64, 65, 67, 102, 103, 123, 127; packet folder `10. CSB 12.18.24`.

### A2.4 · Meetings with no packet folder at all (non-Finance)
**Tier 2 · one-off each · Sources: map+pages §1c**

**§54** — CSB and City Council Joint Meeting, 9/30/24: "Minutes only — no packet folder." No folder in the 2024 Meeting Documents archive; drafts surfaced inside the two following board packets, approved version in the 2024 Meeting Minutes folder. **§70** — CSB, 1/21/25: "No packet folder exists for this meeting." The 2025 Meeting Documents archive jumps `12. CSB Budget Public Hearing 1.15.25` → `13. CSB Deliberative Session 2.1.25`; minutes were posted. **§75** — Claremont School Safety Public Discussion, 3/17/25: no packet or minutes, no dated folder, and the Minutes share holds nothing for 3/17/25 (2025 and 2026 checked). **§115** — Superintendent Candidate Interview (Broderick), 4/6/26: "No packet or minutes found." The FY 2025-2026 archive holds special-meeting folders for 3.26.26, 3.30.26, 4.9.26, 4.13.26 and 4.17.26 but none for 4.6.26, and the 2026 Meeting Minutes folder likewise skips that date while carrying approved special-meeting minutes for 3.26, 3.30, 4.9 and 4.17. **§111** — Article 8 excerpt, 2/18/26: no separate packet or minutes, expected for an excerpt.

*Primary source:* MAP.md §§54, 70, 75, 111, 115.

### A2.5 · Four corpus sections have no Cablecast recording at all
**Tier 2 · systemic · Sources: html-briefing A34 · map+pages §1d, Appendix B**

§61 (SAU 6 12/3/24), §87 (SAU 6 8/21/25), §89 (SAU 6 8/26/25) and §120 (SAU 6 5/28/26) have MAP.md sections but no recording — all SAU 6. The search API was queried for each date and for `SAU`, `SAU6`, `Board Meeting`, `School Board`, `Meeting`, `Special`, `Superintendent`, `Budget Hearing` (about 200 shows scanned) on 2026-08-26 and re-confirmed 8/28/26. These four sections carry no `Remote video:` line, which is the map's own signal to re-check. Where MAP.md has no `Remote video:` line the instruction is to print plain timestamps and note it in the footer, never to guess a show URL. Separately, 43 of 129 sections have no local copy in `Input/Videos/` and are reachable only through the remote link — a fact about the project's collection, not about the public record.

*Primary source:* MAP.md's absent `Remote video:` lines for §61, §87, §89, §120.

### A2.6 · 9 September 2023 — the recording is truncated and there are no minutes
**Tier 2 · one-off, the reference case · Sources: map+pages §1d, Appendix A1**

MAP §20 / page `15286 SchoolBoard090623`: the archived video runs **0:52:52** against a 6:30–8:30 p.m. agenda and stops during discussion item 2 of 7, the last dialogue row ending at 0:52:47 on Ben Nester's unfinished clause, "especially as we go into the, you know, 25 budget cycle, in case there are." So the board-governance discussion, two bargaining slates, the subcommittee round, the athletic-fields licence and a nonpublic session have no public record of any kind — and the meeting also has no minutes, so the public cannot establish whether the session was held, whether a motion naming the exemption was made, who voted, whether nonpublic minutes were kept, whether they were disclosed within 72 hours, or whether they were sealed and on what finding. Also lost: "Whitney Review of School Board Retreat Goals Exhibit F" — the largest governance item of the meeting, with no record whatsoever. Cross-referenced at `15311`, `15336` and `15357`.

*Primary source:* MAP.md §20 and page `15286 SchoolBoard090623.mp4.HTML`.

### A2.7 · 13 June 2024 SAU 6 — a meeting the board scheduled for itself and never held
**Tier 2 · one-off · Sources: map+pages §1e · briefing A1, B48**

"The next folder in the SAU 6 archive after this one is `4. SAU Retreat 5.29.24`, and no folder, agenda, recording or minutes exists for the 6/13/24 SAU 6 meeting this board scheduled for itself." The chair settles it on tape on 12 September 2024 at 0:36:43: "Things were in our packets from the June meeting that we did not hold." MAP §45's negative is therefore upgradable from "no record exists" to "did not happen."

*Primary source:* MAP.md §45; the 12 September 2024 recording at 0:36:43.

### A2.8 · Drive folders with no video on hand, and one share never opened
**Tier 2 · systemic · Sources: map+pages §1f, §4.8**

From MAP.md's "Drive items not tied to any current video" list. **SAU 6 share, unmapped:** `1. SAU SB 1.3.23`, `2. SAU Public Hearing FY24 Budget 1.17.23`, `3. SAU SB Retreat 1.26.23`, `9. SAU 7.31.23`, `11. SAU Retreat 8.23.23`, `12. SAU SB 9.14.23`, `13. SAU 10.12.23`, `4. SAU Retreat 5.29.24`; `2022 Meeting Packets` **remains unopened**. **2023 Meeting Documents:** `1. CSB Meeting 1.9.23`, `2. CSB Public Hearing & Board Meeting 1.11.23`, `3. CSB FY24 Budget Public Hearing 1.17.2[3]`, `8. CSB 3.15.23- Canceled`, `12. CSB 5.17.23`, `15. CSB 7.5.23`, `23. Claremont Board Retreat`. **2024 Meeting Documents:** `1. CSB 8.7.24`, `7. CSB 11.6.24`, `8. CSB Retreat 5.11.24` — the same three folders a Drive `parentId` enumeration silently omits (D2.1). **FY 2025-2026 archive:** `Special Meeting 3.26.26`, `3.30.26`, `4.9.26` (a **CSB** special meeting, not the SAU 6 meeting of the same date), `4.13.26`, `4.17.26`, `20. CSB 2.21.26 Self Evaluation Me[eting]`.

*Primary source:* MAP.md, "Drive items not tied to any current video".

### A2.9 · The SAU 6 next-packet filing rule — where a meeting's minutes actually sit
**Tier 2 · systemic · Sources: map+pages §2a · html-briefing A36 · briefing D2**

MAP.md's caveat: "**SAU 6 minutes follow their own filing rule**, confirmed across 2023–24: the draft is filed inside the *next* meeting's packet folder, and often a second copy sits in the meeting's own folder. Nothing SAU 6 ever reaches the Claremont Meeting Minutes share. 12/7/23 and 4/11/24 have no minutes anywhere." The explicitly annotated instances, preserved:

| § | Meeting | Where the minutes actually sit |
|---|---|---|
| 4 | SAU 6 — 2/16/23 | own folder; **second copy** in `5. SAU SB 3.30.23` |
| 6 | SAU 6 — 3/30/23 | own folder; second copy in `6. SAU SB 4.13.23` |
| 8 | SAU 6 — 4/13/23 | *filed in the **NEXT** meeting's packet folder,* `7. SAU SB 5.11.23` |
| 11 | SAU 6 — 5/11/23 | own folder; second copy in `8. SAU6 7.13.23` |
| 14 | SAU 6 — 7/13/23 | own folder; second copy in `10. SAU 8.17.23` |
| 25 | SAU 6 — 11/9/23 | own folder; draft copy in `15. SAU6 12.7.23` |
| 33 | SAU 6 FY25 Budget Hearing — 12/14/23 | *NEXT meeting's folder,* `1. SAU 1.11.24` |
| 38 | SAU 6 — 1/11/24 | *NEXT meeting's folder,* `2. SAU 2.15.24` |
| 41 | SAU 6 — 2/15/24 | *NEXT meeting's folder,* `3. SAU 4.11.24` |
| 45 | SAU 6 — 4/11/24 | draft only, in `1. SAU6 9.12.24`, **not** in this meeting's own folder — which carries the 2.15.24 draft instead |
| 52 | SAU 6 — 9/12/24 | `2. SAU6 11.14.24` |
| 57 | SAU 6 — 11/14/24 | `5. SAU6 12.12.24` |
| 60 | SAU 6 Strategic Plan — 11/21/24 | `5. SAU6 12.12.24` |
| 78 | SAU 6 — 4/10/25 | `6. SAU6 6.12.25` |
| 83 | SAU 6 — 6/12/25 | `10. SAU6 9.11.25` and `12. SAU6 11.13.25` |
| 87 | SAU 6 — 8/21/25 | `10. SAU6 9.11.25` and `12. SAU6 11.13.25` |
| 89 | SAU 6 — 8/26/25 | `10. SAU6 9.11.25` |
| 91 | SAU 6 — 9/4/25 | `10. SAU6 9.11.25` and `12. SAU6 11.13.25` |
| 54 | Joint CSB/City Council — 9/30/24 | draft in `9. CSB 12.4.24`; second draft copy in `8. CSB 11.20.24` |
| 70 | CSB — 1/21/25 | a DRAFT copy also in the 2/5/25 packet as `1.21.25 DRAFT CSB meeting minutes.pdf` (`1oej86Ppz-HZos9EgcX4_SkML-ohz0IU7`) |

Two further caveats: "**Every SAU 6 minutes file in Drive is a DRAFT, and the trail stops at the 9/4/25 draft.**" And the Claremont Minutes share year folders, re-read 2026-08-26 — 2024 (26 files), 2025 (30), 2026 (20), 2027 (2) — hold only CSB documents.

*Primary source:* MAP.md §2a caveats and the `Minutes:` lines of the sections listed.

### A2.10 · SAU 6 files a meeting's minutes with a later meeting's packet, with lags up to 154 days
**Tier 2 · systemic · Sources: html-briefing A36 · briefing D2**

The 4/11/24 draft minutes turned up in `1. SAU6 9.12.24` — 154 days on — after an earlier folder-scoped check wrongly reported them missing. The practice means a meeting's own folder is not where its minutes live, and no negative may be written without a two-stage search (D2.2). The practice changed mid-corpus: 5/11/23 is the first SAU 6 meeting whose minutes were filed in its own packet folder and inside the five-business-day window, so the two-stage rule still applies to 2024–25.

*Primary source:* the 4/11/24 draft minutes found in folder `1. SAU6 9.12.24`.

### A2.11 · Claremont minutes reach the public share only when the next meeting's packet folder is created
**Tier 2 · systemic · Sources: html-briefing A37 · briefing C53**

Verified on three consecutive folders: `2. CSB 1.17.24` created 2024-01-16T14:47:07Z with the 1/3 minutes at 14:47:22Z, 15 seconds later; `4. CSB 2.21.24` created 2024-02-14T21:08:52Z with the 1/17 draft *and* the 1/29 working-session minutes both at 21:09:38Z; `5. CSB 3.6.24` created 2024-02-29T13:58:35Z with the 2/21 draft at 13:58:58Z. Publication is therefore batched to the next packet's assembly rather than to the five-business-day statutory clock, and `createdTime` is evidence of when the public could see a document, not of when it was written (D2.1 and C1 method records). Note for the arithmetic: 15 January 2024 was a national holiday under RSA 288:1 (third Monday in January), so the 1/3 minutes landed on the 8th business day, not the 9th.

*Primary source:* Drive folder and file `createdTime` on `2. CSB 1.17.24`, `4. CSB 2.21.24` and `5. CSB 3.6.24`.

### A2.12 · Minutes filed long after the statutory five business days, and after the events they governed
**Tier 2 · systemic · Sources: briefing A64**

Measured from Drive `createdTime`: the 1/17/24 draft dated 14 Feb 2024, 4:09 p.m. ET — the 20th business day (deadline 24 Jan) — filed in the *21 February* packet, eleven days after voters deliberated on the budget it records; the 3/20 draft 16 Apr = the 19th business day (deadline 27 March), the day before the meeting that approved them, with two grants gated on them ("We have to send in the minutes from this meeting to the state and then the funds will become available"); 17 April draft 8 May = 15th, approved 20 May = 23rd, with the federal General Assurances FY 2025 gated on them; the 11 May retreat minutes seven business days late; the 20 June approved minutes 8 Aug = the 34th business day with no draft ever filed. At SAU 6: the 4/11/24 draft reached Drive 2024-09-11 = the 106th business day (deadline 4/18/24); the 5/29/24 retreat draft the 73rd; the 9/12/24 draft 2024-11-08 = the 39th; folder `3. SAU 4.11.24` was created 2024-05-29, so the entire April 11 packet went up 48 days after the meeting and the February minutes reached the share 104 days after theirs. Every one of these counts must exclude all eleven RSA 288:1 holidays and use the RSA 91-A:2, II business-day definition (C1.33, C1.38).

*Primary source:* briefing Addenda 13, 14, 15, 16; Drive `createdTime` on the drafts named.

### A2.13 · Notice regression at SAU 6 — packets posted hours before the gavel
**Tier 2 · systemic · Sources: briefing A65**

The whole 12/12/24 packet folder was created 3:59 p.m. Eastern on the day of the meeting, the agenda at 4:01 and the adopted budget V3 at 4:03 — about 2½ hours before the gavel. The 3 December agenda went up at 11:13 a.m. on its own meeting day. The 11/21 packet: folder 1:51 p.m., both files 2:00 p.m. — four and a half hours before a 6:30 start. Against 14 November's six days and 14 December 2023's thirty-one hours. Compare the 76 hours' notice for the 6 October 2025 special meeting (A2.1) and the 8/19/26 agenda last modified five days before the meeting (A2.2).

*Primary source:* briefing Addendum 18; Drive `createdTime` on the SAU 6 packet folders.

### A2.14 · Wrong body in a file name
**Tier 2 · one-off each · Sources: map+pages §2b**

"**Two 2024 minutes filenames say `CSB` for meetings this map treats as SAU 6 or joint**" — `8. Approved CSB meeting minutes 11.14.24` (the 11/14/24 SAU 6 board meeting) and `5. Approved minutes for Joint CSB_City Council meeting 9.30.24`; contents were not opened, so the body each actually records is unverified. **§78** (SAU 6, 4/10/25): "The packet folder is filed under the Claremont board's naming scheme (`CSB`) even though the recording and the minutes both call this an SAU 6 board meeting." And "**8/21/25 is filed twice under different bodies**": the SAU 6 share holds `9. DRAFT SAU6 Board Meeting Minutes 8.21 (1).25_` while the Claremont Minutes share holds `04. Approved CSB Meeting Minutes 8.21.25` — whether that is one gathering recorded twice or two separate meetings was not determined.

*Primary source:* MAP.md §2b caveats and §78.

### A2.15 · Nonpublic minutes filed under the day after their meeting, and therefore unlinked
**Tier 2 · one-off each · Sources: map+pages §2c**

**§77** (CSB, 4/2/25): the Unsealed Minutes share holds `4.3.25 CSB nonpublic minutes Unsealed` (`1S5bhZcYSHSwq2t3BUpiOh5_cNjeleTkr`), "dated the following day; it is not linked to this meeting because the date does not match." **§97** (CSB, 10/15/25): two nonpublic files dated the following day — `10.16.25 Nonpublic Meeting session minutes.docx` (`1kJO94QsBP7bDAaymaYQK0ZyoYBs1VAQF`) and `10.16.25 CSB Nonpublic Meeting session minutes Unsealed` (`12IfpLopJoYV2s5hYO6qOEhd5uIogdjz6`) — likewise not linked. Because MAP.md matches by dates in folder and file names and document contents were not opened, a misdated upload is not caught; a reader searching by meeting date will not find these files.

*Primary source:* MAP.md §77, §97 and the matching caveat.

### A2.16 · 2026 minutes filed under the 2027 year folder
**Tier 2 · systemic in that window · Sources: map+pages §2c**

§124 (7/21/26), §126 (8/5/26) and §128 (8/19/26) all have their draft minutes filed under the **2027 Meeting Minutes** folder (`1aNhxjZSbvCrpjTZpCT7Y4XrW9ZM-bfhe`) rather than 2026. Consistent with a fiscal-year convention — FY2027 begins 1 July 2026 — rather than an error, but recorded because a reader searching by calendar year will not find them.

*Primary source:* MAP.md §§124, 126, 128.

### A2.17 · Structural filing anomalies in the packet share
**Tier 2 · one-off each · Sources: map+pages §2d, §4.7, §4.11**

**§109** (Deliberative Session, 2/7/26): "The packet folder is named `2026 Deliberative Session` rather than by date, and holds a single file — a copy of the warrant marked `(OLD)`." **§124** (CSB, 7/21/26): archive folder `29. CSB 7.21.26` holds two more agenda files for the same meeting beyond the one linked — `7.21.26 CSB Meeting Agenda` (Google Docs) and `1 -- 7.21.2026 - CSB Agenda` (PDF). **§119** (CSB, 5/20/26): four of the packet's ten entries are sub-folders, not documents — `5/20 Financial Update Documents`, `5/20 Policies`, `Food Service Contract Documents`, `Photography Contract Documents` — and their contents were not opened. And a standing verifiability problem: "The 4/9/26 and 5/28/26 agendas are **live Google Docs, not PDFs**, so their content can change after the meeting"; contents will change as the district posts new packets, so the share must be re-checked before publishing.

*Primary source:* MAP.md §§109, 119, 124 and the method caveats.

### A2.18 · Agendas name the wrong minutes for approval, repeatedly
**Tier 2 · systemic · Sources: briefing A30 · html-briefing A40**

The 20 November 2024 agenda printed "Minutes Approval- 10.2.24 & 11.14.24" where the approved minutes print 10.16.24 and record Koski's correction; the same defect repeats on the 4 December agenda ("10.2.24 & 9.30.24") — and the 2 October minutes had already been approved on 16 October. The consequence is that the agendas cannot be relied on for what was actually before the board.

*Primary source:* the 20 November and 4 December 2024 agendas against the approved minutes.

### A2.19 · The by-laws exist in two versions that differ in numbering AND wording
**Tier 2 · systemic · Sources: briefing A24 · html-briefing A11 · briefing C49 · html-briefing §29e**

The adopted PDF (`Exhibit E- Claremont School Board By-Laws .pdf`, Drive `1zjjPqW00SUYvvGuTtDEOKnREw-rB6Nff`, 22 pages, in the 6/5 packet) and the live Google Doc (`1ufhE0flW6DdmhKfON7QH8PG_coPnGhFBfdyEVRId8DE`, modified 2026-03-23) are not the same document. **Wording:** rule 2.07 in the PDF reads "…unless governed by the 2/3 vote rule in CSBL **or Robert's Rules exceptions**…" and ends its abstention passage at "counter to a member's public duty", while the live Doc drops the Robert's Rules words and adds "The NHSBA recommends voting 'No' if members do not have enough knowledge or resources to support a motion rather than abstain"; rule 4.01 reads "Vote upon any question that arises" (PDF) against "Vote on all questions. Maintains all board member privileges." (Doc). **Numbering:** the special-meeting sentence is folded into 2.01 in the live Doc and attributed to "policy BEDD-R. 2.0"; the Ed 302.02(i) temporary-staff rule is 5.04 in both copies; 2.07/2.11/2.12/2.13/2.15 are numbered identically. **Which copy was in force on a given date is generally unknowable from here** — quote by-law text, never a number alone, and say which copy was read and when it was modified.

*Primary source:* the adopted 6/5/24 packet PDF `1zjjPqW00SUYvvGuTtDEOKnREw-rB6Nff` against the live Doc `1ufhE0flW6DdmhKfON7QH8PG_coPnGhFBfdyEVRId8DE`.

### A2.20 · The by-laws contain two rules numbered 2.09
**Tier 2 · one-off defect with systemic consequences · Sources: briefing A23 · html-briefing A12**

The 5 June 2024 adopted text numbers both "(Amendments)" and the agenda-itemisation/publication rule 2.09. Any page citing "by-law 2.09" — the `15814` page does — is ambiguous on its face. Re-confirmed still present in the final check at html-briefing §29e. The remedy is to quote the rule's text rather than its number, and to prefer 2.02 (special meetings, "Except by 2/3rds vote of all members, only matters contained in the notice shall be considered") or 4.03(d) as hooks — with the caveat at A2.21.

*Primary source:* the adopted by-laws PDF `1zjjPqW00SUYvvGuTtDEOKnREw-rB6Nff`.

### A2.21 · In the live by-laws Doc there is no rule 2.02 at all
**Tier 2 · one-off · Sources: html-briefing A13 · briefing A24, C49**

Chapter 2 of the live Doc runs 2.01 → 2.03. The "2.02" reported in the earlier §27c pass was the string `302.02(i)` inside rule 5.04. This removes the special-meeting rule that §26c had recommended as the better hook than the ambiguous 2.09 — depending on which copy a reader has.

*Primary source:* the live by-laws Doc as served on 2026-08-29.

### A2.22 · The district's subcommittee minutes have no working destination
**Tier 2 · systemic · Sources: briefing A61 · html-briefing A38 · briefing D16 · html-briefing D22**

By-laws 1.05(c)–(d) and 1.11 send every subcommittee notice and every set of subcommittee minutes to the SAU 6 website. All four subcommittee Drive folders owned by `sau6webmaster@sau6.org` and created 27 Oct 2022 — Capital Improvement, Claremont Policy Sub Committee, Curriculum Committee, Ad Hoc SAU Exploratory Subcommittee — return **zero files** (verified 2026-08-29). The five folders linked from `sau6.org/119765_1`, read 2026-08-29: Capital Improvement `1zh_axsEVchb_tN0TP56OB5kuJMMnFaQY` (created 2026-02-04, empty); Finance `1LLMD5zj9ZxEWxx3nRLlVrSFBupA6mGO5` (2026-02-04, holding only a purpose statement dated 2025-06-02 and a `2025-2026` item dated 2026-07-02); Policy `1UyUWBMgA6z4tZxbc8SSt-wgUEo-Ovlmh` (2026-02-04, empty); SRVRTC `1OKp_pu7XrZ1_GYwUHNM7EnKAh5rZGDd0` (2026-02-04, empty); Ad Hoc Reconfiguration `1sBcCWTWabFKR3P89uBbgV8SgPzV86LXq` (2026-04-15, empty). **Nothing from 2024 is reachable from any of them**, and there is no folder at all for the SAU 6 Exploratory Ad Hoc, Ad Hoc Communications or Curriculum subcommittees. The board itself conceded the venue was not operating (21 August 2024 approved minutes: "once the website is up and running, those will be available"), so the honest limit is "not published where the by-laws require, and not recoverable" — not "never existed."

*Primary source:* `sau6.org/119765_1` and the five linked Drive folders, read 2026-08-29; the four `sau6webmaster` folders; 21 August 2024 approved minutes.

### A2.23 · The Claremont "Unsealed Minutes" destination was built seven weeks late and contains nothing from 2024
**Tier 2 · one-off, with systemic effect on 2024 nonpublic disclosure · Sources: html-briefing A39 · briefing A56**

The Meeting Minutes share (`1482gj2MFrWIESHvadUpXEx5Tn_L3Vjdv`) has exactly six children — year folders 2023–2027 plus `Unsealed Minutes` (`1KRYrJx5pHxbgiuYUK734SBpAaxyTelnc`), created 13 January 2025, holding only `2025/2026/2027 Non-Public`. **There is no 2024 folder.** The district built the right destination seven weeks after November 2024 and put nothing from 2024 in it — directly load-bearing on the undisclosed 14 November nonpublic at A1.4.

*Primary source:* Drive share `1482gj2MFrWIESHvadUpXEx5Tn_L3Vjdv` and folder `1KRYrJx5pHxbgiuYUK734SBpAaxyTelnc`.

### A2.24 · The Policy Committee's own sealed-minutes review, and the Sealed Minutes List the policy orders, do not exist
**Tier 2 · one-off, standing · Sources: briefing A56**

The review was announced for 2 October and BEDG D.5.b requires it "in a duly noticed meeting in full compliance with RSA 91-A:2"; it has no notice, agenda, minutes or recording anywhere. The **Sealed Minutes List** that BEDG D.4 orders published **does not exist in any share**. RSA 91-A:3, ¶IV — the 10-year review duty, new at 2023, 189:1, eff. 3 Oct 2023 — provides that pre-existing minutes never reviewed become "subject to public disclosure without further action of the public body", and must not be applied to any meeting before that date.

*Primary source:* briefing Addendum 17; policy BEDG D.4 and D.5.b.

### A2.25 · A committee that exists only on a recording
**Tier 2 · one-off · Sources: briefing A63 · html-briefing C20**

The **Parliamentary Procedure ad hoc committee** — chair Whitney, members Sprague and, established later, Petrin — appears in no packet, agenda or minutes: not in the board's own subcommittee list of 1/17/24, not in the 3/20/24 reading. The 2/3/24 minutes reduce Whitney's whole introduction to "and their committee positions", so the recording is the only public record of it. The 3/20/24 recording (1:30:18–1:31:53) adds that it was formed in 2022, was "composed of two board officers and an saw officer. The superintendent and the Business administrator", produced the pre-populated agenda, the onboarding manual, the SAU 6 website, the public-communication policy review and the draft by-laws, and refers to "prior to **suspension of the subcommittee's activity**." It does not survive into the 2024–25 list. The third member was settled by Whitney on 4/17 at 1:13:11: "we Mike patron and Frank Sprague and myself, we're part of an ad hoc parliamentary and procedure committee."

*Primary source:* briefing Addenda 12–15; the 3/20/24 recording at 1:30:18–1:31:53; Whitney, 4/17 at 1:13:11.

### A2.26 · No contract, engagement letter, purchase order, cost figure or vote exists anywhere for District Management Group
**Tier 2 · one-off, standing · Sources: briefing A58**

Announced 15 May 2024 as settled, called ESSER-funded and "budget neutral" on 5 June, with Phase IV dated "December 2024 - Ongoing" — *after* the 30 September obligation deadline. The FY26 SAU 6 budget carries $23,800.00 of contracted services in total, every line unchanged from FY25. The strategic-planning Working Committee's board membership also changed between June and November with no vote or minute anywhere: June (Exhibit F slide 14) Crawford, Hawkins, **Sprague**, Erickson; November (adopted plan p. 5) Crawford, Hawkins, **Whitney**, Erickson.

*Primary source:* briefing Addendum 18; the FY26 SAU 6 budget; Exhibit F slide 14 and the adopted plan p. 5.

### A2.27 · The revenue side is absent from the budget packet
**Tier 2 · systemic ("again") · Sources: briefing A42**

Exhibit D (54 pp.) returns **zero** occurrences of Revenue / Revenues / Adequacy / Receipt / Fund Balance / Estimated / SWEPT, and Exhibit E has no revenue line — yet $852,000, $519,000 of new state aid, a $420,000 fund balance and grant-funded initiatives all exist only as speech. The 29 January working-session minutes prove the schedule existed; it reached the public only at the 3 February deliberative session. RSA 32:5, ¶III is the anchor — appropriations stipulated on a gross basis showing anticipated revenues from all sources — and it is ¶III, not ¶IV (C1.2).

*Primary source:* briefing Addendum 13; the FY25 budget packet Exhibits D and E.

### A2.28 · A district contract whose clause numbering runs 1–16, then 27, 21, 22
**Tier 2 · one-off · Sources: briefing A47 · html-briefing §25b**

Recovered only with `pdftotext -layout`: the Drive MCP's scrambled read hid both the numbering and a missing sub-clause, and interleaved the DRAFT watermark. The defect in the source document is a clause sequence a reader cannot follow and a sub-clause that is absent; the tooling defect that concealed it is recorded at D2.6.

*Primary source:* the contract as recovered by `pdftotext -layout`.

### A2.29 · Recordings that end early — business missing from the end
**Tier 2 · systemic · Sources: map+pages Appendix A1**

| Page / § | Meeting | What is missing |
|---|---|---|
| §20 / `15286 SchoolBoard090623` | CSB 9/6/23 | the reference case — see A2.6; copy runs 0:52:52, last dialogue row ends 0:52:47 |
| `Claremont School Board Finance - 81226` (§127) | CSB Finance 8/12/26 | "the recording **cuts off mid-sentence at 1:10:07**; the end of the meeting is not captured" (show 17530). Missing: the SREA ground-rules scheduling note and any later agenda business; as a subcommittee its minutes must be open within 5 business days wherever kept, and the recording — the fullest public record — cuts off mid-meeting |
| `16253 SchoolBoard010725` (§68) | CSB 1/7/25 | "**The recording stops at the nonpublic transition; the last 17 minutes of the meeting exist only on paper.**" Runs 2:09:08, ends mid-sentence as the chair says the board is "moving into a banana public [nonpublic]" session |
| `16286 SchoolBoard-012125` (§70) | CSB 1/21/25 | "ends mid-exchange at **0:41:49** with the chair asking 'Okay.'" (it also opens mid-room) |
| `15022 SAU6041323` (§8) | SAU 6 4/13/23 | "The recording's last words are the chair's, **cut off at 1:10:31**; the file itself runs to 1:10:57" |
| `15028 SchoolBoard041923` (§9) | CSB 4/19/23 | "not continuous — the nonpublic session is absent from it — and it **ends nine seconds after the motion to adjourn**", so the second and the vote exist only in the minutes |
| `16215 SchoolBoardFinance121324` (§64) | CSB Finance 12/13/24 | "There is no call to order, no roll call and no adjournment vote; the recording **ends on the chair's thanks at 2:22:29**", seconds after an unidentified member moves to adjourn |
| `16158 SAU6112124` (§60) | SAU 6 11/21/24 | "the dialogue transcript runs to 0:50:47, **about sixty-five seconds short of the show's run time**" |
| `Claremont School Board - 72926` (§125) | CSB Goal Setting 7/29/26 | the recording (2:39:58) "opens with the workshop already underway and **ends at a five-minute break before the noticed nonpublic session**" |

*Primary source:* MAP.md and the pages named.

### A2.30 · Recordings that start mid-business — the opening is missing
**Tier 2 · systemic · Sources: map+pages Appendix A2**

| Page / § | Meeting | What is missing |
|---|---|---|
| `14909 SchoolBoard021523` (§3) | CSB 2/15/23 | "The recording joins the pledge mid-sentence" (0:00:03) |
| `14911 SAU6021623` (§4) | SAU 6 2/16/23 | "opens mid-exchange at 0:00:05"; chair calls to order at 0:00:16 |
| `15003 SchoolBoard040523` (§7) | CSB 4/5/23 | "**carries no call to order** — the first 17 seconds have no speech at all" |
| `15022 SAU6041323` (§8) | SAU 6 4/13/23 | "opens on Kelly Simpson **mid-sentence**" (0:00:09) |
| `15205 SchoolBoard071923` (§15) | CSB 7/19/23 | "opens mid-sentence on an off-mic exchange about the new agenda format, then the gavel" |
| `15228 SchoolBoard080223` (§16) | CSB 8/2/23 | "opens **mid-word** — '630 and we're going to commence the August 2nd, 2023 Claremont School Board meeting'" |
| `15385 SchoolBoard110123` (§24) | CSB 11/1/23 | "opens mid-Pledge; **no clock time is spoken and none is recorded**" |
| `15443 SchoolBoardFinance113023` (§27) | CSB Finance 11/30/23 | runs 1:24:07; "opens mid-sentence on 'It looks like we're on the air'"; "There is no call to order, no roll call, no motion, no vote and no adjournment" |
| `15472 SAU6121423` (§33) | SAU 6 12/14/23 | "opens mid-conversation at 0:00:16 and the chair gavels in at 0:01:01 with an apology" |
| `16155 SchoolBoardFinance111924` (§58) | CSB Finance 11/19/24 | runs 1:49:03; "opens mid-greeting on 'We're on the air'"; no call to order, roll call, motion or adjournment |
| `16215 SchoolBoardFinance121324` (§64) | CSB Finance 12/13/24 | "opens mid-greeting and appears to capture the whole session" |
| `16246 SchoolBoardFinance010625` (§67) | CSB Finance 1/6/25 | runs 1:43:56; "opens mid-sentence, so any call to order, roll call and opening business are outside the recording" — first words are Whitney mid-question about "the congruence or the integration of district wide special education salaries and positions into existing programs"; with no notice, agenda or minutes located, "the scheduled start time cannot be established" |
| `16286 SchoolBoard-012125` (§70) | CSB 1/21/25 | "opens mid-room — 'It is not just us.'" |
| `16580 SchoolBoard060325` (§82) | CSB 6/3/25 | runs 2:00:02 — "**begins mid-roll-call; the call to order and Pledge are not captured**"; first captured words "Attendance are here for." (0:00:09) |
| `16596 SAU6-061225` (§83) | SAU 6 6/12/25 | "opens mid-sentence" |
| `16786 School Board 082525` (§88) | CSB 8/25/25 | runs 2:15:05 — "**begins mid-call-to-order; roughly the first 13 seconds of the opening are missing**" |
| `Claremont School Board - 72926` (§125) | CSB 7/29/26 | "begins mid-session and speaker diarization for this meeting is partial (123 segments remain unattributed)" |

*Primary source:* MAP.md and the pages named.

### A2.31 · Recordings that are edits — wall time absent from the middle
**Tier 2 · systemic · Sources: map+pages Appendix A3 · legal-anchors C43 · html-briefing §26a, §29c**

| Page / § | Meeting | Wall time missing |
|---|---|---|
| `15455 SAU6120723` (§31) | SAU 6 12/7/23 | local copy 39:48, transcript 0:00:00–0:39:21; "the published file contains **no break** — the largest gap between consecutive transcript rows is 1.1 seconds — but it is nonetheless an edit: **about ten minutes of wall time across the caucus recess and the nonpublic session are absent**", so positions are pointers into the file and not clock times after 0:25:04. The chair says "It is now 625. We will resume at 635" and the board is back 45 recording-seconds later |
| `15472 SAU6121423` (§33) | SAU 6 12/14/23 | largest inter-row gap 4.4 s, and 0.08 s across the nonpublic session — "**about thirty-four minutes of wall time are absent**", so positions are not clock times after 0:06:33 |
| `16157 SchoolBoard112024` (§59) | CSB 11/20/24 | "**about fourteen and a half minutes of wall clock are missing**, and the district's own clock references locate them inside the nonpublic session"; the page adds that this finding is favourable to CCTV — stopping the recording during a lawful nonpublic session is correct practice rather than a defect |
| `15687 SAU6041124` (§45) | SAU 6 4/11/24 | "the nonpublic session occupies a **47-second gap in the recording between 0:10:27 and 0:11:14**, so recording time and clock time diverge after that point" |
| `15580 SAU6021524` (§41) | SAU 6 2/15/24 | "the recording position converts to about 8:25 PM **on the post-cut offset**" — a cut is presupposed |
| `16463 SAU6Mtg-041025` (§78) | SAU 6 4/10/25 | "the transcript then **jumps 51 seconds** to Campo mid-sentence describing the correct procedure, his connection having dropped again" |

Two further splices were settled by methods other than pixels: show 16157 by two spoken clock times against the minutes' 7:41 p.m. adjournment, and show 17323 by arithmetic — 5,103 s of tape against minuted 6:30 → 8:11 p.m. (101 min) with a 17-minute nonpublic gives 84 minutes public against 85 minutes of recording (B2.3).

*Primary source:* MAP.md and the pages named.

### A2.32 · Meetings whose recording failed or never existed
**Tier 2 · one-off each · Sources: map+pages Appendix A4**

**17 May 2023 CSB** — `15153 SchoolBoard062123` (§13): "Its recording failed." The chair on the record: "We do have some issues with May 17th, 2020 [2023] minutes"; the clerk is named as "the person who could not produce minutes of the May 17 meeting because the recording failed — 'miss Chelsea miss whether it was unable to, transcribe the minutes.'" **12 October 2023 SAU 6** — `15299` (§25): "no recording, no agenda and no folder anywhere in the district's shares." **26 January 2023 SAU 6 board retreat** — `14911` (§4): "a meeting with no recording; its draft minutes are in this packet." **16 and 17 May 2023** — `15058` (§10): "Two board meetings announced at this one — a retreat on May 16 and a regular meeting on May 17 — have no recording, packet or minutes in this project's record." Plus the four SAU 6 meetings with no Cablecast show at all (A2.5).

*Primary source:* MAP.md §§4, 10, 13, 25 and the pages named.

### A2.33 · The systemic cause the boards themselves recorded — CCTV cut off at 8:30 p.m.
**Tier 2 · systemic · Sources: map+pages Appendix A5, A6**

`17017 SchoolBoard120325` (§101), on a 3:33:53 recording that "covers the meeting end to end": "**Board members noted on the record that the CCTV capture had been extended to four hours after earlier meetings were cut off at 8:30 p.m.**" `16982 SchoolBoard111925` (§100) shows the effect at the agenda level: an item was "Deferred on the night — 'in deference of time, because I know **we got cut off the last [time]**' — with a fuller presentation on results, the improvement plan and grant funding promised for the next meeting." For contrast, the pages that affirmatively state coverage is complete: `15357`, `15505`, `15510`, `15531`, `15607`, `15638`, `15693` ("no visible splice"), `15722`, `15786`, `15814`, `15947` (complete at both ends; the nonpublic-session question open at flag 15), `16011` ("no nonpublic session and no gap in the recording"), `16958`, `17017`.

*Primary source:* pages `17017 SchoolBoard120325` and `16982 SchoolBoard111925`.

### A2.34 · Scale of the four negative-finding categories, out of 129 MAP sections
**Tier 2 · systemic · Sources: map+pages Appendix B**

Denominator: 129 MAP sections (§1–§128 plus §96a). The tests are structural — the presence or absence of the `Minutes:`, `Drive folder:` and `Remote video:` fields on each section's header line — so they are reproducible from the file itself.

| Category | Test applied | Sections affected | Share of 129 |
|---|---|---|---|
| **No minutes** | header carries no `Minutes:` field | **29** | 22.5% |
| **No packet AND no minutes** | header carries neither `Drive folder:` nor `Minutes:` | **17** | 13.2% |
| **No packet** | header carries no `Drive folder:` field | **19** | 14.7% |
| **No video** | header carries no `Remote video:` field **and** no local copy in `Input/Videos/` | **4** | 3.1% |

**No minutes (29):** §20, §27, §28, §29, §31, §32, §34, §37, §58, §61, §63, §64, §65, §67, §75, §93, §95, §96, §96a, §99, §102, §103, §111, §115, §116, §120, §123, §125, §127. §45 is *not* counted — a draft exists but no approved-form version does. §128 is *not* counted — its header links a draft added 8/28/26, though its own narrative note says no minutes had appeared. **No packet AND no minutes (17):** §27, §28, §29, §32, §34, §37, §58, §64, §65, §67, §75, §102, §103, §111, §115, §123, §127 — fourteen of the seventeen are Claremont School Board Finance Committee meetings. **No packet (19):** those seventeen plus §54 (Joint CSB/City Council 9/30/24, minutes only) and §70 (CSB 1/21/25, minutes posted). **No video (4):** §61, §87, §89, §120 — all SAU 6, all searched on the Cablecast API 2026-08-26 and re-confirmed 8/28/26.

*Primary source:* MAP.md, structural scan of 129 section headers.

---

## A · Tier 3 — affects precision, not conclusions

### A3.1 · The consent-agenda label changed five times in five months
**Tier 3 · systemic · Sources: briefing A29**

"(vote required)" 17 Jan 2024 → "(consent required)" 21 Feb → "(consent approval required)" 6 Mar → back to "(vote required)" 5 June. The briefing twice instructs: report it, infer no motive.

*Primary source:* briefing Addenda 14 and 15; the agendas named.

### A3.2 · The by-laws' source is stated two different ways two weeks apart
**Tier 3 · one-off · Sources: briefing A28**

The 6 March 2024 minutes say the draft was "Taken and adapted from the **NHSBA** by-laws"; the 20 March minutes say the "School district's attorney recommended **Manchester** By-Laws as a model". The recording supports Manchester — Matt Upton is named.

*Primary source:* briefing Addendum 14; the 3/6/24 and 3/20/24 minutes.

### A3.3 · The 21 November 2024 SAU 6 agenda and minutes head their bodies with the previous meeting's date
**Tier 3 · one-off · Sources: briefing A31**

Both documents read "SAU#6 School Board November 14, 2024" for a 21 November meeting. The substantive defects of that meeting are recorded at A1.38.

*Primary source:* briefing Addendum 18; the 11/21/24 agenda and minutes.

### A3.4 · The board's governing document is owned by the account of a superintendent terminated in January 2024
**Tier 3 · one-off · Sources: html-briefing A14 · briefing A24**

The live by-laws Doc `1ufhE0flW6DdmhKfON7QH8PG_coPnGhFBfdyEVRId8DE` has Drive `owner` `mtempesta@sau6.org` — Michael Tempesta, whose contract the SAU 6 board terminated effective 12 January 2024. Recorded as checkable, with the express warning not to build a finding on a metadata field alone.

*Primary source:* Drive metadata on Doc `1ufhE0flW6DdmhKfON7QH8PG_coPnGhFBfdyEVRId8DE`.

### A3.5 · A one-dollar error at the head of the whole budget sequence
**Tier 3 · one-off · Sources: briefing A33**

The 1/17/23 minutes state both budget motions as "…three hundred and **thirteen** dollars" ($38,345,313 / $37,345,313) where the warrant, the ballot and every other record say $38,345,312 / $37,345,312.

*Primary source:* briefing Addendum 11, "District records that disagree with themselves".

### A3.6 · The FY24 appropriation is given three different ways in the district's own documents
**Tier 3 · one-off · Sources: briefing A34**

`.71` in the 3 January summary, `.72` in Exhibit E, `.92` in the Exhibit D grand total, on a base of $34,880,311. Report the discrepancy rather than picking one.

*Primary source:* briefing Addendum 13.

### A3.7 · The $3,600 "Wages School Board Secretary" line is actually the clerk's
**Tier 3 · one-off · Sources: briefing A45**

4/10/25 minutes: "That's your board clerk. Yes. Okay, I can change that from board side." The line was mislabelled against an office — secretary — the board had not filled (A1.29), and was corrected at the table.

*Primary source:* briefing Addendum 18; the 4/10/25 minutes.

### A3.8 · The 3/6/24 approved minutes give the student member two names in one document
**Tier 3 · one-off · Sources: briefing A26**

The masthead says **Kylee**, the body says **Kylie**. The 15607 dialogue CSV also labels her Kylie. District filings elsewhere — the agenda and both sets of 1/17/24 minutes, the 5/15 agenda and minutes — settle on **Kylee**.

*Primary source:* briefing Addenda 13 and 14; the approved 3/6/24 minutes.

### A3.9 · The "Alex Barney" template error — minutes naming a student member who is not in their own masthead
**Tier 3 · systemic (at least two meetings) · Sources: briefing A27**

The body of the 12/20/23 approved minutes reads "Student Board Members-Nicole Bouchard and Alex Barney - not present" while that document's own masthead reads "Kylee Plummer". The same defect appears at 11/1/23, and the briefing warns it is "not confined" to that meeting.

*Primary source:* briefing Addendum 14; the approved 12/20/23 and 11/1/23 minutes.

### A3.10 · The district cannot spell its own Director of Student Services
**Tier 3 · systemic · Sources: briefing A66**

**McCosker** on the 7 August 2024 masthead → **McKosker** on 21 August, 4 September and 18 September → **McCosker** again from 2 October — same clerk, consecutive documents. The 9/30 minutes then print "Micheal McCosker" in the agenda body three pages after their own masthead prints McCosker. A separate person, **Tina McCosker**, is printed correctly in the agenda and minutes and appears in the dialogue CSV as "Tina McCusker".

*Primary source:* briefing Addenda 16 and 17; the mastheads named.

### A3.11 · The curriculum director's name has six renderings and is still unsettled
**Tier 3 · systemic, unresolved · Sources: briefing A67, C36**

**Cat** (2/21/24 minutes) · **Catlin** (5/15/24 agenda and both sets of minutes; the 2/21/24 SAU 6 Office Monthly Report, "Curriculum/Grants (Catlin / Michael)") · **Kat** (`CSB Curriculum Sub-Comm. Proposal.pdf`, 19 Aug 2024, the first with a title: "Kat McLaughlin, Curriculum Director") · **Katlyn** (spoken by the chair on 30 September and 20 November 2024, where the minutes print Catlin) · and the December Superintendent's Report printing both "Cat" and "Catlin McLaughlin" on one page. The ASR adds `Caitlin McLaughlin` and bare `cat`. The standing instruction is to print no spelling as fact. This is disagreement 5 of the five carried at the foot of this file: the project's own resolution was claimed and withdrawn four times across briefing Addenda 13–17 (C3.3).

*Primary source:* briefing Addenda 4, 13, 14, 15, 16, 17, 19.

### A3.12 · The business-office "Lori" had six spellings and is now settled
**Tier 3 · systemic, resolved · Sources: briefing A68 · html-briefing B17**

**Murray** (8/2/23) · **Maury** / **Marie** (8/16/23) · **Morey** (9/20/23) · **Mallory** (2026 files) · **Mowrey** (the only district-document spelling), plus the ASR's `Laurie Maori` and `Lori Marie`. Settled as **Lori Mowrey** by the 3/18 Banking Resolution: "Matthew Angell, Interim Business Administrator; Lori Mowrey, Finance Director; Vicki Lee, Staff Accountant."

*Primary source:* the 3/18 Banking Resolution.

### A3.13 · The Rebecca cluster — five district spellings, with a seventh data point
**Tier 3 · systemic · Sources: briefing A69 · html-briefing A44**

The corpus carries **Duska**, **Vendesco**, **Vinduska**, **Vindeska** (3/19/25 approved minutes) and "**von Duska**" (ASR) — almost certainly one person, Ward 1, Claremont Middle School teacher. The strongest source is not a district document: the Jack and Dorothy Byrne Foundation letter of 7 February 2023, on foundation letterhead, in the 3/1/23 packet, is addressed to "Rebecca Vinduska" at Claremont Middle School — a third party writing to her by name outranking the district's own inconsistency — and the approved 18 February 2026 minutes print "Rebecca Vinduska" and "Ms. Vinduska", agreeing with it. **The two inventories do not reconcile:** `briefing.md` Addenda 6 and 9 record a *different* Rebecca — **Rebecca Duska**, CMS 6th-grade science teacher, Ward 1 — as the applied resolution of `15483` Speaker 10, named by Bonnie Miles on 1/3/24 at conf 1.00/0.97. This is disagreement 2 of the five carried at the foot of this file; pending a ruling, describe the role and attribute any spelling to its document.

*Primary source:* the Byrne Foundation letter of 7 February 2023 in the 3/1/23 packet; the approved 18 February 2026 minutes; briefing Addenda 6 and 9.

### A3.14 · Broderick vs Broadrick — the incoming superintendent's own signature against the district's filings
**Tier 3 · one-off · Sources: briefing A70 · html-briefing A43**

He signs his own memo **Timothy Broadrick, EdD** and the 5/20 agenda spells it Broadrick; both sets of minutes and the Cablecast gallery spell it **Broderick**. On the Byrne-letter precedent the rule is to follow his own document: briefing Addendum 1's "Dr. Tim Broadrick" is right and MAP §115's "Broderick" follows the district.

*Primary source:* the superintendent's own signed memo and the 5/20 agenda, against the minutes and the Cablecast gallery.

### A3.15 · McLeod vs McCleod
**Tier 3 · one-off · Sources: briefing A71**

`Jessica McLeod` in the dialogue CSV and two shipped pages against `Jessica McCleod` in the district's own 10.15.25 draft minutes. Recorded as a two-spelling name with no resolution offered.

*Primary source:* briefing Addendum 19; the 10.15.25 draft minutes.

### A3.16 · Lownie / Louny — two real people, both ASR-derived
**Tier 3 · one-off, settled · Sources: briefing A72**

`Camron Lownie` and `Ken Lownie` are different people — father and son, Ward 2 — proven distinct because they co-occur in two files, 16409 and 17046. Both spellings are ASR-derived from "Louny", so neither is documentary. **No "Lowney" variant appears anywhere in the briefing set**, and the briefing inventory records this expressly as one of two items a task named that are not attested (the other being a "Lavallette" variant: only `Lavalette` appears — Don Lavalette, sworn in 3/18/26, and the eight `16951` rows corrected to him).

*Primary source:* briefing Addenda 1 and 9.

### A3.17 · Rhines — one approved minutes document uses two first names
**Tier 3 · one-off · Sources: briefing A73**

The approved 12/18 minutes use both *Mimi* and *Amelia* Rhines in one document. The corpus separately carried "Amalia", corrected to **Amelia** by the agenda and both sets of minutes.

*Primary source:* briefing Addenda 17 and 19; the approved 12/18 minutes.

### A3.18 · Michelle Herrington's title is given three ways inside one packet, and six ways across seven weeks
**Tier 3 · systemic, "a finding, not an error" · Sources: briefing A74**

Inside one packet: "Tech Director", "Assistant Director", and "Ms. Herrington"/"Ms. **Harringont**". Across seven weeks in 2024 the same body called her: 9/4 — the board votes to strike "acting" from the **Assistant** Director title; 9/18 — Crawford, "the new, director, actor [acting] director at the tech center… she's been on the job for 17 days"; 9/30 — Manale and Crawford both say **director**; 10/2 — Crawford, "the director"; 10/16 — the chair introduces her as "our new **assistant** director"; 11/19 — she introduces herself as **assistant** director. The board's formal action was on "Assistant Director"; colloquial usage ran ahead of it. The briefing calls this a finding rather than an error and forbids normalising it. She must never be merged with Michael Herrington (B1.5).

*Primary source:* briefing Addenda 8 and 19.

### A3.19 · Stephanie Hurst's title cannot be settled — the district uses both in one packet
**Tier 3 · one-off · Sources: briefing A75**

The agenda and minutes head her item "**Curriculum Director** Presentation" while the framework she authored, in the same folder, titles her "**Literacy Specialist, SAU 6**". The 2/15/23 minutes also name her Literacy Specialist, anchoring the surname to a 2023 primary source but contradicting the corpus's "SAU 6 Curriculum Director" (see C1.60).

*Primary source:* briefing Addendum 11; the packet agenda, minutes and framework.

### A3.20 · The 3/6/24 approved minutes misspell three presenters against their own self-IDs on tape
**Tier 3 · one-off · Sources: briefing A76**

**Scott Blewitt / Blewett**, **Kari Rothford-Hague / Kerry Rochford**, **Taylor Lauck / Taylor Luke**.

*Primary source:* briefing Addendum 14; the approved 3/6/24 minutes against the recording.

### A3.21 · The 2/8/23 minutes misname two residents against other district records
**Tier 3 · one-off · Sources: briefing A77**

The minutes read "**Shawn Wadsworth — Ward 3**" against the corpus's "John Wadsworth (W2)", and "**Anne Feln**" against "Ann Fine" — the latter settled by the 2/15/23 minutes ("Ann Fine (Ward 2)"). The same minutes supply **Raqual Fluette**, a surname briefing Addendum 3 said was never spoken, and record **Patrick Adrian, Ward 1** moving the $1,000,000 amendment though he is absent from the corpus's list of 2023 voices.

*Primary source:* briefing Addenda 10 and 11; the 2/8/23 minutes.

### A3.22 · Lee Malloy vs Lee Mulloy
**Tier 3 · one-off · Sources: briefing A78**

Two district documents spell it **Mulloy** — the 1/17/24 packet's Exhibit A ("Program Data Review - Lee Mulloy - Lead Teacher") and both sets of 1/17 minutes — against briefing Addendum 4's Malloy. Per the Shaun Laplante precedent the district documents are the stronger source, but the instruction is to record the conflict, not pick.

*Primary source:* briefing Addendum 13; the 1/17/24 Exhibit A and both sets of 1/17 minutes.

### A3.23 · Lilly vs Lily Clark, and Kylee vs Kylie Plummer — self-identification against district spelling
**Tier 3 · one-off each · Sources: briefing A79 · html-briefing A45, §15h**

"Lilly Clark" appears in every district document from 2 Oct 2024 (also 16 Oct, 5 Feb 2025) while *Lily* is her own self-identification on tape; report the conflict and use the district spelling in prose. **Kylee** is the district's spelling in its own filings against the corpus's Kylie. The corpus-wide normalisation applied the opposite convention for Clark — `Lilly Clark`→`Lily Clark`, 69 rows across 4 files (B3.20).

*Primary source:* briefing Addendum 17; html-briefing §15h; the district filings named.

### A3.24 · Tracy vs Tracey Pope
**Tier 3 · one-off · Sources: briefing A80**

The 2/1/25 minutes spell the moderator "**Tracey**" against Tracy elsewhere. Standing instruction: show the conflict, never pick silently.

*Primary source:* briefing Addendum 1; the 2/1/25 minutes.

### A3.25 · Noel vs Noelle Kronberg, and Kronberg vs Cronenberg
**Tier 3 · one-off · Sources: briefing A81**

Both `Noel` vs `Noelle` and `Kronberg` vs `Cronenberg` are unsettled on the tape at her 11/9/23 and 11/15/23 appointments; the project normalised to **Noelle Kronberg** corpus-wide, 34 rows across 3 files, against `15455` and `15523` which carried `Noel` (B3.20).

*Primary source:* briefing Addenda 5, 6, 9.

### A3.26 · CCTV titles carrying the wrong year — eight shows
**Tier 3 · systemic in the January-rollover window · Sources: map+pages §5a · briefing A82 · html-briefing B7**

MAP.md's caveat: "Gallery titles carry the opposite failure — the wrong *year* — so titles are reproduced verbatim as identifiers but never relied on for dating." The error is CCTV's, not MAP's; quote the title as given and note the discrepancy rather than silently correcting it.

| § | Meeting | Cablecast title as returned | Wrong by |
|---|---|---|---|
| 36 | CSB FY25 Budget Public Hearing — 1/3/2024 | `School Board Meeting 1/3/23` | −1 year |
| 37 | CSB Finance — 1/5/2024 | `School Board Finance Meeting 1/5/23` | −1 year |
| 38 | SAU 6 Board — 1/11/2024 | `SAU 6 Board Meeting 1/11/23` | −1 year |
| 67 | CSB Finance — 1/6/2025 | `School Board Finance Meeting 1/6/24` | −1 year |
| 68 | CSB — 1/7/2025 | `School Board Meeting - 1/7/24` | −1 year |
| 100 | CSB — 11/19/2025 | `Claremont School Board 11/19/26` | **+1 year** |
| 105 | CSB — 1/7/2026 | `Claremont School Board - 1/7/25` | −1 year |
| 106 | CSB Public Hearing on Proposed Budgets — 1/20/2026 | `School Board - Public Hearing Proposed New Budgets 1/20/25` | −1 year |

§100, §105 and §106 carry explicit "Title note" paragraphs; §68 carries a "Date note" recording both the title error and the `eventDate` error. Show 17116's API title likewise reads "…1/20/**25**" against `eventDate` 2026-01-20.

*Primary source:* the Cablecast API titles for the shows listed; MAP.md §§36, 37, 38, 67, 68, 100, 105, 106.

### A3.27 · Cablecast `eventDate` is not always the meeting date — five shows off by one day, and the mechanism
**Tier 3 · systemic · Sources: map+pages §5b · html-briefing B6, C22 · briefing C50**

| Show | `eventDate` | Actual meeting | § |
|---|---|---|---|
| 16253 | 1/6/25 | 1/7/25 | 68 |
| 16315 | 1/30/25 | 2/1/25 — "a Saturday, which is when NH deliberative sessions are held" | 71 |
| 16872 | 9/26/25 | 10/1/25 | 95 |
| 17241 | 3/17/26 | 3/18/26 (found 2026-08-28) | 113 |
| 17291 | 3/31/26 | 4/1/26 (found 2026-08-28) | 114 |

"In each case the show title, the transcript file name and the district's own dated packet folder agree with one another, and that date was used." The mechanism: an operator opening a record early lets `eventDate` default to *now*. Show 17291 returns `2026-03-31T13:35:06` with `created` 70 seconds later for a meeting on 1 April; show 17307 returns `2026-04-09T08:18:44` +43 s for a 6:00 p.m. meeting; show 17241 returns a precise stamp from the day before. So a precise `eventDate` plus a creation stamp a minute later is **not** proof that recording began then — check the field against both the meeting's date and its noticed hour before trusting it.

*Primary source:* the Cablecast API `eventDate`/`created` pairs for shows 16253, 16315, 16872, 17241, 17291, 17307.

### A3.28 · Cablecast show numbers follow record-creation order, not event order
**Tier 3 · systemic · Sources: html-briefing B5, C22 · briefing C50**

Show 17125 (7 February 2026) has a **lower** number than 17134 (4 February 2026), because 17125's record was opened on 23 January and 17134's on 3 February; two more confirm it — 17095 for 21 January created 6 January, and 17116 for 20 January created 19 January. Never infer a sequence from show numbers alone, and treat a `created` stamp that precedes the event date as a hand-entered, pre-scheduled record that says nothing about when recording began. The diagnostic holds only for the other kind of record: show 17126 is a textbook case, and show 16226 is the one that settled the ordering of the two 18 December 2024 meetings.

*Primary source:* the Cablecast API `created` stamps for shows 17125, 17134, 17095, 17116, 17126, 16226.

### A3.29 · Other Cablecast title quirks, reproduced verbatim
**Tier 3 · systemic · Sources: map+pages §5c**

`SAU #6` vs `SAU 6`; `Claremont School Board - 09/4/24` (§51); `School Board Meeting live 4/5/23` (§7). §75's title, `Claremont School Safety Public Discussion`, carries no date at all.

*Primary source:* the Cablecast gallery titles for the shows named.

### A3.30 · File names carrying a wrong date or a reproduced typo
**Tier 3 · one-off each · Sources: map+pages §2c**

**§104** (CSB, 12/17/25): "The two budget-model PDFs are dated `12.16.2026` in their file names; the district's own typo is reproduced" — the meeting is 12/17/**2025**. The Drive-items list carries `3. CSB FY24 Budget Public Hearing 1.17.2[3]`, a truncated year in the folder name. And the standing caveat: "File names are reproduced exactly as they appear in Drive, typos included (`FY26 Expeditures`, `3 .Claremont`)." Also in this family: the 16 May 2023 retreat minutes filed as "Retreat Minutes May 16, **2020**" (A2.1), and the "Goodwin Community Room" for Goodrich in the 29 May 2024 SAU 6 retreat minutes.

*Primary source:* MAP.md §104 and the file-name caveats.

---

# CLASS B — PROJECT PIPELINE DATA

Defects in the transcripts, dialogue CSVs, MAP.md and the built page set.

## B · Tier 1 — affects what a reader can conclude

### B1.1 · Phantom names — high-confidence surnames that name nobody in the room
**Tier 1 · systemic, the corpus's most dangerous class · Sources: briefing B20 · html-briefing B13**

The briefing keeps a standing list and forbids minting people from any of it: **`Nathan Ward, please` = "name and ward, please"** (the podium prompt, not a person) · **`Mr. Clark` = District Clerk** (mints a person out of an office) · **`a second by Brittany`** — the chair failing to identify a seconder, reading as a real name · **`So, Donald, we'd like to have a rollback` (1.00) = "so down the line"** · **`Sussex` (1.00) = SAU 6**, reading as a real place · `Mr. Crowder` (0.95 and 1.00) and `Mr. Free` (0.58) in one Petrin sentence · `Mr. Smith.` (0.98) and `Mr. Pittman.` (0.87) = the chair recognising Sprague · `Mr. Dean, how are you today?` · `Another Mr. Costa to chime in` · `just like Mr. Foster said` · `Mr. governor` and `Charlie` (later resolved to Gessner, C3.4) · `Mr. Broughton` (0.56, recurs at 15607 @0:51:08) · `Barrett` · `Mr. Braxton` (0.82) · `Edmond` (0.44) · `Mr. Caskey` (0.74) · `James prophet here` (0.60–0.94) · `My dad Mattos is in there` (≥0.93, later resolved to **Matteau**) · `Dave. Jack.` · `Now, Tyler, take it away` (0.50) · `the good magazines tonight` · `Clarence Surprise` · `National Association of Taxpayer` (an organisation that does not exist; it is the paraprofessionals' association/Teamsters) · **`Leah,` (0.88) / `Leah` / `L a` / `li e a` = LEA**, a statutory role rendered as a woman's name · `Miss Kestner` · `Sniper.` · `The Oscar` · `Brian Souter` · `Police Chief Walmart` · `Sue car` · `City Management, Olli` · `Bill. The newest newbie` · `Eric Perry` (single-source, later confirmed a real person). **The two inventories disagree on one entry.** `briefing.md` Addendum 8 lists **`the Dow building` / `the Dow office` (both 1.00)** here as "the SAU 6 central office… full confidence, plausible proper noun, no such place", while `html_briefing.md` §29i un-flags it: "**`the Dow` is NOT an ASR garble** — it is the district's own name for the SAU office building, used in its approved minutes and on an agenda." This is disagreement 4 of the five carried at the foot of this file; the html-briefing reading is the later and better-evidenced one, and both are recorded here.

*Primary source:* briefing Addenda 3, 5, 6, 7, 8, 9, 12, 16, 17, 19; html-briefing §29i.

### B1.2 · Dropped and inverted negations
**Tier 1 · systemic, quote-critical · Sources: briefing B21 · html-briefing C1**

Settled against packet PDFs: **`admitting during` = "admin just ignoring"**; **`Avenue` = "admin"**; **`feel heard` = "feel unheard"**; **`I can't hold myself to a high standard` = "I hold myself to a higher standard"**. Two more are quoted as recorded and repaired nowhere: Pratt at 0:55:58 (16226), "And we just gone to the days that we were allowed…", and at 1:20:16, "we can't I can't in good faith say…". Also `We use to increase` = "reduced and increased", inside a verbatim reading of RSA 40:13, IX(b). The standing rule is absolute: **a dropped negation is NEVER supplied — supplying it invents a vote.**

*Primary source:* briefing Addenda 18 and 19; html-briefing §1.

### B1.3 · Fused digit pairs and impossible numbers
**Tier 1 · systemic · Sources: briefing B22 · html-briefing B12**

`378 minute classes` = three 78-minute classes · `178 minute prep` = one 78-minute prep · `646 minute classes` = six 46-minute · `146 minute prep` = one 46-minute · **`$57,592, 852,500 and 857,000 $357,592` = a single $857,592**. Confidence gives no protection: **`3.53 to 12.75` (every token 1.00)** for the NH Retirement rate is arithmetically impossible against a sentence calling it a decrease — settled by the packet as 13.53% → 12.75% — and **`77 years`** for the LED payback is 7 years, settled by the 16 Oct approved minutes. Also `for $20,000` = **$420,000** and `$82,000` = **$583,000**, both the clerk reading a motion back; `October 16th, 2021` = 2024; `19927` = a collision of Claremont I (1993) and Claremont II (1997). The rule: **any number that looks impossible is probably two numbers**, and a reader taking the transcript at face value gets a 378-minute class.

*Primary source:* briefing Addenda 8, 9, 14, 15, 18, 19; html-briefing §27i.

### B1.4 · Statute, policy and code numbers garbled by the recognizer
**Tier 1 · systemic · Sources: briefing B24 · html-briefing §28b**

**`RSA 44 and 13` = RSA 40:13** · **`RSA 91-8` = 91-A** · **`RSA 3215-F` vs `are essay 32 colon 5-F`** — two independent transcriptions of the same sentence · `policy CVI`, `GCU`, `GCA` = **CBI / GCQ** · `policy DEDH` = **BEDH** · `policy BEED` = **BEDH** · `Policies BED. B.` = **BEDB** · `Policy HAC` = **EHAC** · `K. E b.` = **KEE** · `a sore 102` / `Saw 99` = SAU 102 / SAU 99 · `43403` = ¶4.03 · `Warren article` / `the abhorrent article` = warrant article · `jet services` = debt service (inside a verbatim reading of RSA 40:13, IX(b)). A page that repeats any of these repeats a citation the district did not make.

*Primary source:* briefing Addenda 11, 12, 14, 17, 18, 19; html-briefing §28b.

### B1.5 · Identical high-confidence ASR output for two different people — the two Herringtons
**Tier 1 · systemic · Sources: briefing B17 · html-briefing B11**

`Harrington` is produced at **0.99–1.00 confidence for two different people in one file** — Michael Herrington (Stevens principal) and Michelle Herrington (SRVRTC). They appear together in at least 16021, 16070 and 16222 and **must never be merged**; a confidence score is not an identification. Related variants: `Doctor Harrington` · `Doctor Herren` · `Doctor Herron` · `Michael Arrington` (0.52, reads as a real surname) · `a shell` = Michelle · the district's own `Ms. Harringont`.

*Primary source:* briefing Addenda 2, 7, 8, 9, 19; html-briefing §27h.

### B1.6 · `15580 SAU6021524.mp4.CSV` — three separate label failures in one file
**Tier 1 · one-off file, systemic class · Sources: briefing B26**

The row at **2956.86 s** ("To make a motion to change our meeting schedule to a bi monthly schedule") is labelled Arlene Hawkins; it is diarized Speaker 11 = Heather Whitney, and the minutes name Whitney as mover — the label is wrong. **Rocco Ruggeri has zero rows in the file's 460** while the minutes credit him with six acts; the Speaker 4 cluster labelled Frank Sprague holds *both* the second on the HR contract motion (1307.5 s) and the abstention on it (1322.2 s), so Ruggeri's voice is inside that cluster and **no mover in it is safe from the label alone**. The "lose touch" run at **2980.34 s** labelled Bonnie Miles sits inside the chair's Speaker 1 cluster and plainly holds an interjection; the minutes split it between Atonya Hart and Miles.

*Primary source:* briefing Addendum 14; `15580 SAU6021524.mp4.CSV` against the approved minutes.

### B1.7 · CSV attributions that the approved minutes contradict
**Tier 1 · systemic · Sources: briefing B27 · html-briefing §23c**

4/17/24 — the Valley Regional / Dartmouth-Hitchcock remark at 0:55:32 is Arlene Hawkins in the CSV and Bonnie Miles in the approved minutes, and the diarizer merges the two women so the tape cannot settle it. 6/5/24 — the Herzog tribute and the by-laws motion sit in one four-utterance cluster the minutes split between O'Hearn and Petrin. 9/12/24 — the ADC motion at **2681 s** falls in the Whitney-cluster gap, so the CSV labels it Arlene Hawkins while the minutes credit Heather Whitney. 1/17/24 — the benchmark question is Miles in the minutes and Hawkins in the CSV. The generalised rule: **when a CSV label produces a body or a fact that exists in no document, suspect the label before you suspect the document.**

*Primary source:* briefing Addenda 13, 15, 16; html-briefing §23c.

### B1.8 · Merged speaker clusters — same-sex voices, as the default expectation
**Tier 1 · systemic · Sources: briefing B28**

The diarizer merges hard: Whitney+Kennedy+Hawkins into one cluster, Kennedy+Lewis into another, Blount+Madden+Sprague into a third in the Feb–Mar 2026 wave. The era's hardest case is **Bonnie Miles and Arlene Hawkins — 48 segments in 16021, 106 in 15947, 7 rows in 16046** — whose anchored blocks *interleave*, so no temporal or topical cut works; where a chair recognition does not separate them the row must stay `Unidentified` with both candidates in the Role. Two open merges await a human ruling: **16192's Speaker 7/12 cluster** merges Sprague and Petrin (the approved 12.4.24 minutes give three of its turns to Petrin, including the answer running continuously into "I only have an associate's degree"), and **the Speaker 6/11 cluster filed Arlene Hawkins probably also merges Bonnie Miles** (the same minutes give two of its questions to Miles). **Two women or two men in one cluster is the default expectation, not the exception.**

*Primary source:* briefing Addenda 1, 8, 18.

### B1.9 · One voice split across clusters, and clusters inherited by a second person
**Tier 1 · systemic · Sources: briefing B29**

The 2/7/26 deliberative split the moderator across **seven** clusters. The diarizer splits **Heather Whitney into two temporally disjoint clusters at SAU 6 meetings** — seen at 4/11/24 and 9/12/24 (Speaker 3 ends 2578.44 s, Speaker 11 starts 2770.80 s, zero overlap). And the chair's vacated cluster is inherited by whoever is silent early: at 10/2/24 Whitney occupied Speaker 2 to 1471 s, moved to Speaker 7, and Arlene Hawkins — silent for the first 25 minutes — fell into the cluster Whitney vacated. **A single cluster spanning a meeting is not a single person.**

*Primary source:* briefing Addenda 1 and 8.

### B1.10 · Chair recognitions absorbed into the next speaker's onset, and sub-second onset clipping
**Tier 1 · systemic · Sources: briefing B30**

"Thank you. Lauren." lands at the head of Loren Howard's segment; "Yes, Mr. Howard." at the head of Howard's own. Separately, **any fragment under about 1 s with an ~80 ms gap to the next segment is almost certainly the NEXT speaker's onset** and must be checked every time. Off-by-one override indices against the printed label distribution are named as **the commonest error in this run's history**.

*Primary source:* briefing opening contract and Addendum 1.

### B1.11 · Segments that contain two speakers
**Tier 1 · systemic · Sources: briefing B31**

In `Claremont School Board - 8526` (8/5/26), **160 of 554 segments carry more than one speaker** — e.g. the chair's handoff "Mr. Campo, I'm going to turn it over to you" and the auditor's reply share one diarizer segment. That file is the corpus's one turn-based CSV (375 rows over 554 segments) precisely because flattening it onto the segment grid would destroy real attribution work; `verify_dialogue.py` was extended to accept both conventions, re-checking a turn-based file **only if its concatenated token list equals the transcript's exactly** and reporting `OK*`.

*Primary source:* briefing Addendum 9; `Claremont School Board - 8526` transcript and CSV.

### B1.12 · Members recorded present with zero attributed rows
**Tier 1 · systemic · Sources: briefing B32 · map+pages Part 2 §2b · html-briefing §23c**

The briefing's instruction in these cases is to present both candidates and choose neither. Its headline instances: **Rocco Ruggeri** zero rows in 15580's 460 against six minuted acts; **Bonnie Miles** present on 12/18/24 speaking zero attributed words, and present with zero attributed rows on 15 May 2024 — which is what exposed the CSV artefact at B1.13; **Whitney Skillen and Bonnie Miles** recorded present on 1/17/24 and never heard or named, zero occurrences of either surname or any variant. The finished pages disclose the same defect meeting by meeting:

| Page | Member(s) with zero attributed rows |
|---|---|
| `14911 SAU6021623` | **Shannon Popescu** ("no segment anywhere in the 513-row dialogue file, and no other speaker addresses her"); **Michael Koski** (minutes have him co-presenting TeachUNITED; "the dialogue file attributes no row to him at all") |
| `14986 SAU6033023` | **Bonnie Miles, Shannon Popescu, Kelly Simpson** — "Three members present… have no attributed row in the dialogue file at all" |
| `15022 SAU6041323` | **Bonnie Miles** — "present per the minutes and per the roll calls but has no attributed speaking row" |
| `15073 SAU6051123` | **Rocco Ruggeri, Shannon Popescu** — "the minutes credit Ruggeri with a motion the dialogue file attributes to Frank Sprague" |
| `15193 SAU6071323` | **Skillen, Gallagher, Miles, Simpson, Hart, Popescu** — "six of the eleven members… have no attributed speaking row at all" |
| `15254 SAU6081723` | **Miles, Skillen, Simpson, Erickson, Popescu** — five of twelve; "Atonya Hart has exactly one, a single word" |
| `15299 SAU6110923` | **Ruggeri, Popescu, Simpson, Hart, Miles**, and absent **Skillen** — six of twelve; "Gallagher has four rows totalling nineteen words" |
| `15443 SchoolBoardFinance113023` | **Ben Nester** — "recorded present in the chair's round-robin… and then speaks not one recorded word in eighty-four minutes" |
| `15472 SAU6121423` | **Eleven of the twelve members** — "the chair reads every roll call herself and eleven members' answers are absorbed into her own rows" |
| `15523 SAU6011124` | **Half the board** — "their roll answers are absorbed into the reader's own diarized rows" |
| `15580 SAU6021524` | **Four seated board members** — "which for the second-most-active member in the minutes is itself the transcript's largest defect" |
| `15687 SAU6041124` | **Michael Petrin** — answers "Here" and "Yes" and "has no attributed speaking segment anywhere in the dialogue file" |
| `15722 SchoolBoard051524` | **Bonnie Miles** — "while the approved minutes credit her with seconding two motions and with the closing thanks" |
| `16046 SchoolBoardCityCouncilJoint093024` | **Noelle Kronberg** — "Zero attributed rows" |
| `16049 SchoolBoard100224` | **Bonnie Miles** — "Zero attributed segments and zero attributed words, on a night when she was present and the board was complete"; **Michael Koski** — "Zero attributed rows — and the minutes have him speaking twice" |
| `16070 SchoolBoard101624` | **Noelle Kronberg** — "Zero attributed rows"; **Patrick O'Hearn** — "Zero attributed rows, and he is the leading candidate for the unidentified administrator above" |
| `16142 SAU6111424` | **Candace Crawford** — "named as the seconder of the unsealing motion. No segment in the dialogue file is attributed to her, and no name is spoken for her at any point" |
| `16157 SchoolBoard112024` | **Noelle Kronberg** — "Zero attributed rows" |
| `16158 SAU6112124` | **Michael Petrin, Shannon Popescu** — "the whole board accounts for a seventh of the words spoken" |
| `16192 SchoolBoard120424` | **Bonnie Miles, Michael Petrin** — "the approved minutes give them five turns that the recording places in two other clusters" |
| `16213 SAU6121224` | **Rocco Ruggeri** — "The transcript's Rockford Ruggieri here opens the roll and no segment anywhere in the file is attributed to him" |
| `16226 SchoolBoardFinance121824` | **Michael Koski** — "The opening sentence places 'Mike Kosky' in the room; no row in the dialogue file is attributed to him" |
| `16580 SchoolBoard060325` | **Mary Henry** — "no segment anywhere in the 623-row file is attributed to Henry, although the chair thanks her by name at 1:51:00" |
| `16786 School Board 082525` | **Loren Howard** — "Present; opposed both motions. No speaking turn is attributed to him" |
| `16881 SchoolBoardSpecial100625` | **Michael Petrin** and **William Madden** — "Not named in the roll call as transcribed; no speech attributed. Two unnamed affirmatives are audible in the roll and either could be his, but the recording does not settle it and there are no minutes." Also **Loren Howard** and **Candace Crawford** — "Answered the roll. No separately attributable speech" |
| `16882 SAU6BoardMeeting100625` | **Shannon Popescu** — "Thanked by the chair for seconding the motion to seal… so present, but no speech is separately attributed to her" |
| `17159 SchoolBoard021826` | **Michael Petrin** — "The minutes credit him with seconding the nonpublic motion and moving to seal the nonpublic minutes; no row in the dialogue file is attributed to him by name" |
| `17201 SchoolBoard030426` | **Michael Petrin** — "the second consecutive Claremont meeting for which that is true" |
| `17291 SchoolBoard040126` | **Makaila Gallow** (Student Board Member) — "Introduced by the chair; no attributed speech in the dialogue file" |
| `17307 SAU6040926` | **Darlene Ayotte, Kelly Simpson, William Madden, Loren Howard, Michael Petrin** — "No row in the dialogue file is attributed to any of them by name" |
| `17348 SchoolBoard050626` | **Brian Rapp** — "has no attributed row at all, while the minutes credit him with five contributions" |

*Primary source:* briefing Addenda 13, 14, 19; the 31 pages named.

### B1.13 · A CSV label that invented a subcommittee membership
**Tier 1 · one-off, with a general lesson · Sources: html-briefing B10 · briefing B33, C26 · html-briefing C20**

Nobody read a membership list aloud on 15 May 2024. There is one first-person sentence — "today I sent an email to Mr. Sprague and Miss Crawford to get together so we can begin with our vision" — which the CSV labels for the chair, producing the phantom "Whitney + Sprague + Crawford" Capital Improvements roster that then entered briefing Addendum 7 and the project's own briefs. Read as **Bonnie Miles** it is exactly right, supported three ways: Miles is present with zero attributed rows; the sentence sits in a `Speaker 1` cluster that by then carries a different voice by override while the chair's own words either side are `Speaker 21`; and the same merge happens three more times with the approved minutes naming Miles each time. The approved 5/15 and 4/17 minutes both give the Capital Improvements chair as Miles.

*Primary source:* the 15 May dialogue CSV read against the approved 5/15 and 4/17 minutes.

### B1.14 · When a chair reads a document aloud, the CSV makes its contents her speech
**Tier 1 · systemic · Sources: briefing B34 · html-briefing B9**

In the October 2025 candidate recordings the chair reads three applicants' letters of intent aloud and the CSV attributes every word to her. On show 16872 at 0:51:02 a passage labelled "Heather Whitney" reads "…the last two as president of the Sri, which is the educators union" — an applicant's biography that nearly made a board member a union president.

*Primary source:* show 16872 at 0:51:02, dialogue CSV.

### B1.15 · Four shipped-CSV corrections, all applied
**Tier 1 · one-off each, resolved · Sources: briefing B36**

`16951 SchoolBoard110525.mp4.CSV`: eight rows labelled `Unidentified public commenter — Ward 2` (starts 8980.22, 9063.26, 9063.94, 9073.70, 9085.66, 9119.22, 9147.34, 9406.74) are **Don Lavalette**, proven three ways — he offers the board "Mr. Tyson[,] me" as the two options, another speaker names the field as "Mr. Lava[lette] and… Mr. Tyson", and the excerpt file 16958 already carried four of the eight under that name. `15336 SchoolBoard100423.mp4.CSV` @3680.30: the curriculum-committee line labelled `Unidentified` is **Jennifer Gallagher**. `15483 SchoolBoard122023.mp4.CSV`: Speaker 10's "Rebecca, surname never spoken" is **Rebecca Duska**, named by Bonnie Miles on 1/3/24 at conf 1.00/0.97 — see the unreconciled Rebecca question at A3.13. `15357 SchoolBoard101823.mp4.CSV`: Speaker 4's candidate list was re-weighted, and that re-weighting is now itself doubtful because its premise collapsed (C1.65).

*Primary source:* briefing Addenda 1, 5, 6, 9.

### B1.16 · A wrong speaker label carried against the person's own document
**Tier 1 · one-off each · Sources: briefing B38**

**Shaun Laplante** (not Sean/Shawn) is established by his own grant proposal, signature block and district e-mail `slaplante@sau6.org` — and the dialogue CSV speaker label is also wrong. Separately, `15607` labels the student member **Kylie** where the district's own filings print Kylee (A3.8).

*Primary source:* briefing Addendum 11 (name resolutions) and Addendum 14.

### B1.17 · Two recordings in the corpus are excerpts of other recordings, one with a spliced cold open
**Tier 1 · one-off pair, standing rule · Sources: briefing B39 · html-briefing B3 · map+pages §3**

**16958 is an excerpt of 16951** (11/5/25) beginning **7,768.8 s** in, covering the board-vacancy item (`eventDate` 2025-11-05, verified 8/28/26), plus a spliced cold open; it has its own transcript and dialogue CSV. **17168 is an excerpt of 17159** (2/18/26) at offset **+2,277.9 s**, created the afternoon after the meeting and clipped mid-turn at the end; 121 of 134 substantial rows align at the constant offset with no drift, and the excerpt's first segment **fuses the 6:30 call to order onto "Moving on to article eight"** — two utterances **38 minutes apart** in the room. Standing rule: **never compute a wall-clock time from an excerpt's timestamps**; and if a recording opens mid-business, has no roll call, or ends mid-sentence, look for a sibling show on the same date before concluding the meeting itself was odd.

*Primary source:* the alignment of 17168 against 17159 (121 of 134 rows at 2,277.9 s); MAP.md §98, §110, §111.

### B1.18 · Two independent machine transcriptions of the same 49 minutes differ materially
**Tier 1 · one-off, standing rule · Sources: briefing B40 · html-briefing B4**

Because 17168 is derived from 17159, the corpus holds two transcriptions of the same audio and they disagree in substance: **`RSA 3215-F` vs `are essay 32 colon 5-F`**, and "We're going to have to cut the budget roughly 9 million" vs "We were going to cut the budget. Roughly 9 million." Quote only from your own page's CSV; `verify_quotes.py` catches cross-transcript quotations and caught two. Where the other must be quoted, label it with its show number and do not deep-link it — one show ID per page.

*Primary source:* the two transcripts of shows 17159 and 17168, compared.

### B1.19 · The same 2/1/2023 meeting was transcribed twice, with correlated errors
**Tier 1 · one-off, standing rule · Sources: briefing B41 · map+pages §3.1**

`14875 SchoolBoard020123` and `Claremont School Board Meeting 2123` are the same meeting, transcribed twice with different diarization; each gets its own CSV because the CSV mirrors the transcript file, not the meeting. **They are two runs of the same stack, not two systems**: both produce "Nathan Ward", "Macedonia", the same isolated administrator cluster and the same Miles clustering. **Agreement between them is weak corroboration; DISAGREEMENT is the strong signal** — the 2/1 agents resolved every disagreement on content, never by vote. Whether the duplicate should be retired is an open question in MAP.md.

*Primary source:* briefing Addenda 2 and 3; MAP.md §1.

### B1.20 · MAP §96 conflated two different meetings on the same evening, and a shipped page inherited the error
**Tier 1 · one-off, error class recurred twice · Sources: html-briefing B2, C55 · briefing B46 · map+pages §3.5**

MAP.md had merged the Claremont board meeting of 6 October 2025 (5:30 p.m.) with the SAU 6 meeting (6:00 p.m.), and the `16882` page consequently stated that the Claremont meeting "has no recording of its own in the Cablecast gallery." **Show 16881 IS that recording** — title *Special School Board Meeting 10/6/25*, `eventDate` 2025-10-06, `totalRunTime` 774 s, agenda headed CLAREMONT SCHOOL BOARD MEETING at 5:30 p.m., Heather Whitney presiding — while 16882 is the SAU 6 meeting at 6:00 p.m. "The two agendas describe two different meetings of two different bodies." MAP was split into §96 (Claremont, show 16881) and §96a (SAU 6, show 16882) on 2026-08-29. The general rule that follows: **before writing that a meeting has no recording, fetch the neighbouring show IDs from the Cablecast API and read their titles** — several agents have now done this and it has changed the answer twice.

*Primary source:* the Cablecast API record for show 16881; MAP.md §96 / §96a.

### B1.21 · The ASR loses the podium "name and ward" at deliberative sessions
**Tier 1 · systemic · Sources: html-briefing B14 · briefing D24**

At deliberative sessions the minutes are the register of who spoke and the recording usually is not — the ASR loses the podium self-identification almost every time, and `Nathan Ward, please` is the podium prompt rendered as a person (B1.1). Claremont's minutes list floor speakers **grouped by position (for / against / neither) but in speaking order within each group**, verified twice on 2/3/24 against speakers who do self-identify — Gary Merchant 4th of 4 in both, Matt Bean 1st and Chris Pratt 5th in both — which makes ordinal identification defensible provided the working is shown and no name is given where two turns cannot be told apart.

*Primary source:* the 2/3/24 minutes verified twice against self-identifying speakers.

---

## B · Tier 2 — affects what a reader can find or verify

### B2.1 · Honest `Unidentified` rates, and where a high rate is the correct outcome
**Tier 2 · systemic · Sources: briefing D14 · html-briefing B15 · map+pages Part 2 §2a**

The corpus norm is 8–10%; the Feb–Mar 2026 wave ran 3–9%. **16046** (the joint session) carries 16.9% — roughly half of it `Unidentified City Councilor`, body and role established, name not — and the briefing says plainly "that is the correct outcome, not a defect." **16142** runs 24.2% because four seated members are never anchored to a voice, and the page states that in its footer with the number rather than guessing. The 2/7/26 open-floor deliberative ran 21% — open-mic public comment is where the rate belongs, not the board table. Ninety of the 126 pages mention "Unidentified" at all; **41 attach a number to it**:

| Page | Figure | | Page | Figure |
|---|---|---|---|---|
| `14911 SAU6021623` | 4 of 512 rows = 0.8% | | `16011 SAU6091224` | 20 of 548 = 3.6% |
| `14986 SAU6033023` | 38 rows = 4.4% — "including both speeches in the chair debate, the ballot count and the member who raised the $30,000 city bill" | | `16021 SchoolBoard091824` | 36 segments = 2.9% |
| `15022 SAU6041323` | 38 of 556 = 6.8% | | `16049 SchoolBoard100224` | 4 segments, 21 words = 0.3% |
| `15073 SAU6051123` | 51 of 283 rows | | `16070 SchoolBoard101624` | 15 segments, 246 words = 1.2% |
| `15193 SAU6071323` | **67 of 313 = 21.4%** — "more than double this corpus's usual rate" | | `16142 SAU6111424` | **105 of 434 = 24.2%** — "against a corpus norm nearer 8 to 10 percent" |
| `15254 SAU6081723` | 89 of 689 = 12.9% | | `16157 SchoolBoard112024` | 14 segments, 44 words = 0.5% — "the lowest unattributed share this project has recorded on any Claremont board page" |
| `15299 SAU6110923` | 34 of 334 = 10.2% (365 words) | | `16158 SAU6112124` | 27 of 199 = 13.6% |
| `15443 SchoolBoardFinance113023` | 12 rows = 1.5% | | `16192 SchoolBoard120424` | 31 segments, 112 words = 5.9% of rows / 0.9% of words |
| `15455 SAU6120723` | 25 of 298 = 8.4% (260 words) | | `16213 SAU6121224` | 17 of 489 = 3.5% |
| `15472 SAU6121423` | **44 of 196 = 22.4%** | | `16215 SchoolBoardFinance121324` | 2 of 939 = 0.2% |
| `15523 SAU6011124` | 3 of 78 = 3.8% — "and that number flatters it" | | `16222 SchoolBoard121824` | 10 segments, 80 words = 0.6% |
| `15531 SchoolBoard011724` | 78 segments, 468 words = 2.0% (78 of 787 rows = 9.9%) | | `16226 SchoolBoardFinance121824` | 14 of 999 = 1.4% |
| `15580 SAU6021524` | **77 of 460 = 16.7%** | | `16872 SchoolBoard100125` | 149 of 1,362 = 11% |
| `15585 SchoolBoard022124` | 75 segments, 250 words = 1.3% (75 of 887 rows = 8.5%) | | `17116 SchoolBoardPublicHearing012026` | **154 of 398 rows ≈ 39%** — "recorded as unidentified public comment" |
| `15607 SchoolBoard030624` | 41 of 644 = 6.4% | | `17125 SchoolBoardDeliberative020726` | **191 of 904 = 21.1%** across 36 speaker labels |
| `15638 SchoolBoard032024` | 3 segments, 10 words = 0.1% | | `17307 SAU6040926` | 11.4% of rows / 5.2% of words |
| `15687 SAU6041124` | 58 of 677 = 8.6% | | `17323 SchoolBoard041526` | 2.7% of rows / 1.5% of words — "the lowest rate of any meeting in this stretch of the corpus" |
| `15693 SchoolBoard041724` | 18 segments, 153 words = 0.9% | | `17373 SchoolBoard052026` | 32 of 852 = 3.8% |
| `15722 SchoolBoard051524` | 26 segments, 57 words = 0.3% | | | |
| `15786 SchoolBoard060524` | 1 of 375 = 0.3% | | | |
| `15814 SchoolBoard062024` | 39 segments = 5.7% | | | |
| `15947 SchoolBoard082124` | 17 segments, 69 words = 0.5% | | | |
| `15994 SchoolBoard090424` | 14 segments, 340 words = 3.5% — "well inside this corpus's 8–10 per cent norm" | | | |

`16958 SchoolBoardVacancy110525` states the inverse: "The dialogue file carries 271 rows across thirteen speakers, and no row is left unattributed." Where a page cannot settle who spoke, the district's minutes often can — two "Unidentified public commenter" clusters on show 17159 are named in the approved minutes as January King, ward 3, and Kyle Messier, ward 1.

*Primary source:* the 41 pages named; briefing Addenda 1, 8; html-briefing §25g.

### B2.2 · Two CSV provenance notes that are wrong or over-general
**Tier 2 · one-off each · Sources: briefing B37**

`15193 SAU6071323.mp4.CSV`: its note says the 7/13 chair-election tally is unrecoverable, but the Ruggeri rows at **339.3 s** read "Okay, we got three and Arlene. Two. Three" — a possible show-of-hands count the file does not surface, and the minutes later gave it outright: **Hawkins 8, Erickson 3** (C1.62). Its roll-reader note also claims no prior SAU meeting used the same reader; 5/11/23 had Ben Nester read the roll at the chair's request. `15455 SAU6120723.mp4.CSV`: its note that Kronberg read all four rolls is right for that night but must not be read as general — Hawkins reads them herself on 12/14/23 and 1/11/24.

*Primary source:* briefing Addenda 4, 6, 11; the two CSV provenance notes.

### B2.3 · Zero-gap splices established, and one proven by arithmetic
**Tier 2 · systemic class · Sources: html-briefing §26a, §29c · briefing B42**

On show **16157** the zero-gap question was settled by two spoken clock times — "Mr. Upton will be available in roughly 15 minutes" at 0:34:15, and "I asked him if he's available soon. At 719." at 0:51:14 — against the minutes' "Consent adjournment at 7:41pm": the spliced reading fits all three anchors to within 20 seconds; the continuous reading fits none. On show **17323**, 5,103 s of tape against minuted 6:30 → 8:11 p.m. (101 min) with a 17-minute nonpublic gives **84 minutes public against 85 minutes of recording**, proving an excision of 17 minutes in 18 recording-seconds, confirming a call to order the minutes never state and validating the minuted adjournment. Pixels cannot do this (D2 records). The recommended order of cheap tests: run-time arithmetic first, then spoken clock times, then spoken countdowns ("45 minutes left in this session", "we have a half hour left", "we got ten minutes for the calendar" — three on one file, projecting ends of 2:50 / 2:47 / 2:46 p.m. against an actual 2:47 from the event stamp).

*Primary source:* show 16157 at 0:34:15 and 0:51:14 against the minutes' 7:41 p.m. adjournment; show 17323's run time against its minuted times.

### B2.4 · Two 12/6/2023 shows that look like an excerpt pair and are not
**Tier 2 · one-off, negative finding · Sources: briefing B43**

`15452` (finance subcommittee, afternoon, ~89 min) and `15453` (full board, evening, ~35 min) share **zero n-gram overlap**. Both are complete, genuinely separate meetings — not a 16951/16958-style pair.

*Primary source:* briefing Addendum 5; the n-gram comparison of 15452 and 15453.

### B2.5 · MAP §111 records the excerpt offset but not the splice
**Tier 2 · one-off · Sources: briefing B47 · html-briefing B3**

It gives 17168's +2,277.9 s offset from 17159 without recording that the excerpt's opening fuses two utterances 38 minutes apart, so a reader following MAP literally will search for the opening words at 0:38 of 17159 and not find them.

*Primary source:* MAP.md §111 against the 17168/17159 alignment.

### B2.6 · MAP sections carrying a stale or superseded negative
**Tier 2 · one-off each · Sources: briefing B48 · html-briefing §25d, §29i**

**§45** records "no record exists" for 13 June 2024 where the chair states on tape that the meeting was never held — upgradable (A2.7). **§63** should read "no minutes published in either share; the 4/10/25 draft records their approval on 10 April 2025" for 12 December 2024. **MAP line 6135** lists folder `4. SAU Retreat 5.29.24` **unmapped** — there is no MAP section for the quorate 29 May 2024 SAU retreat. **MAP line 6159's** open question is settled: that file records the **Claremont** 14 November meeting, not the SAU 6 one. **MAP §115** spells the incoming superintendent "Broderick", following the district against his own signature (A3.14). MAP §20's earlier note called the 9/6/23 interviewees "superintendent candidates"; they were not — there was no search (corrected 2026-08-29).

*Primary source:* briefing Addenda 16, 18; html-briefing §25d, §29i; MAP.md §§20, 45, 63, 115 and lines 6135, 6159.

### B2.7 · Duplicate recordings on hand in `Input/Videos/`
**Tier 2 · one-off each · Sources: map+pages §3**

Four distinct cases beyond the excerpt pair at B1.17 and the twin 2/1/23 transcription at B1.19: `Input/Videos/Claremont School Board 81926 copy.mp4` is a **byte-identical duplicate** of `Claremont School Board 81926.mp4`, both **7,028,140,594 bytes**, deliberately not mapped as a separate meeting; and two shows on one date at §96/§96a, resolved at B1.20. Whether the 2/1/23 duplicate should be retired remains open in the map.

*Primary source:* MAP.md §§1, 96, 96a, 98, 110, 111 and the method caveats.

---

## B · Tier 3 — affects precision, not conclusions

The ASR garble catalogue. These are transcription defects: they do not by themselves produce a wrong finding, but they are the raw material of the Tier 1 hazards at B1.1–B1.5, and the catalogue is what lets an agent recognise a garble instead of publishing it.

### B3.1 · Petrin is never rendered correctly, in any file
**Tier 3 · systemic · Sources: briefing B1 · html-briefing B13**

The briefing states it flatly twice: "never once correct in the 9/4 file" and "Petrin, never once correct in any file". Variants: `Michael Patron` · `Patrone` · `Mr. Patron` · `Mike Patron` · `Mike. Patron.` · `Michael Keaton` (0.85) · `Michael. Peter.` · `Mr. Peter` · `Mr. Peters` (1.00) · `Mr. Peterson` (1.00) · `Mike Peterson` · `Mr. Putin` (1.00) · `featuring` (1.00) · `Michael. Future.` · `So patrons seconding`. Two of these are an ordinary English word and a head of state, both at full confidence.

*Primary source:* briefing Addenda 2, 7, 9, 16, 19.

### B3.2 · Skillen is the worst name in the set
**Tier 3 · systemic · Sources: briefing B2**

`Miss Gillen` · `Gillan` · `Gillam` · `Scullin` (**0.94**) · `Skilling` · `Skillet` · `Whitney. Skeleton.` · `Whitney. Scaling.` · `East. Gillen.` · `Beneath. Skilling.` (0.89) · `Miss Whitney Scullin` · `Miss Whitney Gillan` (0.56) · `Miss Kellen` · `miss going` · `still on` · `the skill` · `Vinnie. Skilling` · `Miss skill` · `And skill` · `Whitney Skilling` · `Miss Gilman` · `Miss Guilherme` · `It's Gillen` · `Wendy` — plus whole-sentence forms `What are you still in for?`, `with me still here`, `Let me. Skilling`, `Whitney still here`, `You still here?`, all rendering "Whitney Skillen here". One 3/20/24 sentence uses two spellings for her in a row, and the 3/20/24 subcommittee reading contains three variants within 40 seconds. **`Scullin` at 0.94 is the standing warning that high ASR confidence is no protection on these names.**

*Primary source:* briefing Addenda 2, 3, 5, 7, 14, 16, 19.

### B3.3 · Tempesta garbles read as real surnames
**Tier 3 · systemic · Sources: briefing B3**

`Mr. Dempster` · `Mr. Thompson` · `Mr. Pesto` · `Mister Timbuktu` · `Mike pesca` · `Mr. Contessa` · `Mr. Temper` · `Mister Tuesday`. Thompson, Dempster and Contessa are singled out as dangerous because they read as plausible real people, and `Mister Tuesday` because it reads as an ordinary phrase.

*Primary source:* briefing Addenda 3, 4, 5, 11.

### B3.4 · Hawkins, including two full-confidence wrong people
**Tier 3 · systemic · Sources: briefing B4**

`Hopkins` · `Arlene Hopkins` · `Eileen Hopkins` · `Carly` · `Harley` · `Riley Hawkins` · `Hoffman` · `Arlene Hoffman` (**0.99**) · `Miss Hoffman` · **`Arlene Foster` (0.99)** — which reads as a real public figure · `Marlene` · `Marlin` · `Barley. Hawkins` · `Marlene. Hawkins.` · `Eileen` · `Eileen Hawkins` · `early knocking` · **bare `early` (1.00) = "Arlene"** · `You are Lane.` / `Our lane.` = Arlene · `Miss Hocking`.

*Primary source:* briefing Addenda 2, 5, 7, 8, 14, 15.

### B3.5 · Sprague, including two spurious self-names at high confidence
**Tier 3 · systemic · Sources: briefing B5**

`Greg` · `Craig` · `Craig. Sprague.` · `Craig Sprague` · `Frank's Greg` · `Spriggs` · `Frank Spriggs` · `Bragg` · `Frank. Strange.` · `Spring. Sprague` · `Mr. Springs` (1.00) · `Frank spray` · `Yes, daddy` · `upon your great Sprague here` · `Frank's great work to` = "Frank Sprague, Ward Two" · **`Mr. Smith.` (0.98)** and **`Mr. Pittman.` (0.87)**, both the chair recognising him. Two spurious forms invent him where he is not: **`Frank speaking` / `I see those same way. Frank.` = "frankly speaking" (0.97)** and **`And Sprague, a couple other ancillary responsibilities` = "and perhaps a couple other…" (1.00)** — a Sprague at full confidence that means no person at all.

*Primary source:* briefing Addenda 2, 3, 5, 6, 7, 9, 14, 19.

### B3.6 · Crawford, including the phantom-first-name trap
**Tier 3 · systemic · Sources: briefing B6**

`Is proffered` · `And is Crawford` · `Candice. Proper.` · `Candice. Parker.` · `Candace Parker` · `Dennis Crawford` · `Ines Crawford` (0.73) · `Mr. Crawford` · `No candy` = "Now, Candace" · `Kansas is last this here` = "Candace, as I said…" · `Kenny` (0.77) = "Candy" · **`Andy` = "Candy" (12/6/23) and `Andy Crawford` (1.00) twice — once inside an attendance list, once in the chair's own introduction.** The Andy form is the worst because Andy is a real recurring person in this corpus, so the garble can manufacture a phantom attendee. `As Kennedy said earlier` = "as Candace said earlier" is separately dangerous because Kennedy is a 2025–26 name that must not leak into 2023.

*Primary source:* briefing Addenda 3, 4, 5, 6, 8, 9, 19.

### B3.7 · Heather Whitney, including a common noun at full confidence
**Tier 3 · systemic · Sources: briefing B7**

`Craig. Ivan. Whitney.` · `Heather. Wendy.` · `Heather Whitman` · `Heather wisdom` · `Dear Whitney` · **`head` (1.00) = "Heather"** ("if head is working at her job…"), which reads as a common noun and hides a reference to the chair · `Okay windy` (0.80), an ambiguous form this corpus attests for **both** Whitney and "Candy" (Crawford). The era-specific hazard compounds it: **"Whitney" is both a surname and a first name on the same board** — Heather Whitney (chair) and Whitney Skillen (member), the corpus's highest-risk collision.

*Primary source:* briefing Addenda 2, 5, 8, 9, 12.

### B3.8 · Bonnie Miles
**Tier 3 · systemic · Sources: briefing B8**

`A lot of miles` · `20 miles` · `Bonnie Myles` · `Miss Myles` · `Bonnie Myers` · `Ronnie Miles` · `Donnie miles` · `Only. Miles.` · `smiles` (in the mover naming herself).

*Primary source:* briefing Addenda 4, 5, 7, 15, 17, 18.

### B3.9 · Horsky
**Tier 3 · systemic within 2023 · Sources: briefing B9**

`Hauschka` · `Steve Gorski` · `Mr. Horton` · `Stephen Hausman` · `Mr. Horse Keeper` · `Even asking`.

*Primary source:* briefing Addenda 2 and 3.

### B3.10 · Kronberg, at up to full confidence
**Tier 3 · systemic · Sources: briefing B10**

**`Bromberg` (conf 1.00)** · **`Miss Grunberg` (1.00)** · `Miss Kronborg` (0.62) · `Miss Cronenberg` · `Mr. Cronenberg`. Plus the underlying spelling instability, `Noel` vs `Noelle` (A3.25).

*Primary source:* briefing Addenda 5, 7, 8, 15, 17.

### B3.11 · Koski, and the three-way "Michael" ambiguity
**Tier 3 · systemic · Sources: briefing B11**

`my Kosky` · `Kosky kosky to skis` · `Mr. Kosky` · `Mr. Kosugi` · `Michael Coffee` · `Michael Cosby` · `Mr. Costa` (0.56) · `Mr. Caskey` · `Assistant Superintendent Kosky`. The standing rule: **treat a bare "Michael" or "Mike" in any SAU 6 or Finance file as ambiguous three ways — Koski, McCosker, Petrin** — as in 16158, where "Go ahead Michael" comes through at confidence 1.00 with two Michaels in the room and was left unnamed.

*Primary source:* briefing Addenda 3, 7, 9, 14, 16, 17, 19.

### B3.12 · McCosker, including a wrong honorific at full confidence
**Tier 3 · systemic · Sources: briefing B12**

`Michael McCusker` · `Mr. Oscar` (0.95) · `Mr. Costco` (0.96) · **`Miss McCosker` (1.00)** — correct surname, wrong honorific, on a man · `Tina McCusker` for Tina McCosker.

*Primary source:* briefing Addenda 7, 9, 16.

### B3.13 · Nester, including a verb and a collision with the ESSER family
**Tier 3 · systemic · Sources: briefing B13**

`Mr. Nestor` · **`pester` (1.00)**, which reads as a verb · `Nestor. Gallagher.` (dangerous with Nester in the room) · **`Ben Esther`**, dangerous because `Esther` is this corpus's standing ESSER garble and both occur inside one budget presentation.

*Primary source:* briefing Addenda 3, 8, 12, 13.

### B3.14 · Erickson
**Tier 3 · systemic · Sources: briefing B14**

`Marjorie. Harrison.` · `Margaret Erickson` · `Marjorie Rhodes` · `Andre. Erickson.` · **`Frederick Erickson` (0.98)** · **`Or three years.`**, which reads as a question about a seal duration and names nobody · `LED by Marjorie Erickson` = "led by" — dangerous because the same meeting has an "Affinity LED Lighting" item.

*Primary source:* briefing Addenda 3, 5, 6, 9, 17.

### B3.15 · Ruggeri
**Tier 3 · systemic · Sources: briefing B15 · map+pages `16213`**

`Gary` (inside a roll call) · `Rothko` · `Rocco. Jerry.` · `Rocco Gerry` · `Afterwards` · `Rock over. Garrett.` · `rock over here` · `Rocky times` · **`Rocky Ridge` (0.93)**, which reads as a place · `Rocco and Roger from unity` · and `Rockford Ruggieri` on 16213, where he opens the roll and no segment in the file is attributed to him.

*Primary source:* briefing Addenda 3, 6, 7, 9, 18; page `16213 SAU6121224`.

### B3.16 · Atonya Hart
**Tier 3 · systemic · Sources: briefing B16**

`LaTanya` · `Tommy Hart` · `Tanya. Hurt.` · `Tanya. Hot` · `It's on your heart.` · `Tony. Hawk.` · `Fine art.` · and the near-miss **`The time of art is a chair`**, which *may* be "Atonya Hart is the chair" — one of three such near-misses in one file, none decisive, and the briefing forbids manufacturing a name from them.

*Primary source:* briefing Addenda 3, 6, 7.

### B3.17 · Lower-frequency personal-name garbles, grouped
**Tier 3 · systemic in aggregate · Sources: briefing B19 · html-briefing B13, §28g**

`Assistant Superintendent Simmons` / `Richard Sheets` = **Seaman** · `David Jackson` = **David Jack** · `Mr. Craft` = **Pratt** · `Mr. Plant` = **LaPlante** · `Alyssa` = **Melissa** (Lewis) · `Jeff Smalley` = **Jeff Small** · `Mr. Holtz` = **Mr. Holt** · `new Cole` = **Nicole** (Bouchard) · `Joseph.` = **Jennifer** (Gallagher) · `Billy Simpson` = **Kelly Simpson** · `Shannon, you.` / `Shannon. Perpetuo.` = **Popescu** · `professor Hughes here` = possibly Popescu, unresolved · `Meeting your eyes` / `Mimi Ryan's` / `Miss Rhymes` / `Miss Ryan's` / `rhymes` / `Miss Rhimes` = **Rhines** · `Michelle, be in Ward two` / `Michelle beaten` = **Michelle Beaton** · `Next on Ward three` = **Nick Stone** · `Matt being` / `Matt Beam` = **Matt Bean** · `John Claudia` = **John Cloutier** · `Wayne coming away` = **Wayne Hemingway** · `Miss David` = **Miss Damon** · `Sandra Edwards` = **Cassandra Edwards** · `Li` / `Lily Malloy` = **Lee Malloy** · `Dave Erwin` = **David Irwin** · `Mark blunt` / `Mr. Blue` = **Mark Blount** · `Catlin` / `Caitlin McLaughlin` / `cat` / `Katlyn` = **Cat/Catlin McLaughlin** · `Baxter Hearn` and `Patrick Ahern. O'Hearn. Not her. Patrick overheard` (three failures in one sentence) = **Patrick O'Hearn** · **`Frank Miller` (1.00) = Frank Romeo, in his own self-introduction** · `Billboard` = **Milbourn** · `Mr. governor` / `Charlie` = **Charles Gessner** · `Mr. Smith, knocks` = **Thomas Smith-Knox** · `Lauren Howard` = **Loren Howard** · `Gary Martin for two` = "Gary Merchant, Ward Two" · `challenge for` = **Charlene** (Lovett) · `Malik, I` = **Malachi** · `Chelsea Warren` = "Chelsea [Weatherford] *warn*" · `Bernstein Shaw` = **Bernstein Shur** · **`polymath is at our school` = "Polly Bath[urst] is at our school"** — and the ASR splits that surname, so **"Polly Bathurst" is Polly Bath** and a page carrying "Bathurst" is wrong · `the doctor state's` = **Dr. Staves** · `Miss Quarter` = **Miss Porter** · `Mr. Dupree` / `Mr. Joe Perry` = **Doug Beaupre** · `Laurie Maori` / `Lori Marie` = the Lori surname · and a speaker the CSVs called **"Noah Bosch"** in one file and **"Nora Shane"** in another is **Noel Beauchaine**, corroborated by the interim superintendent thanking her by name on tape.

*Primary source:* briefing Addenda 3–19, passim; html-briefing §15h, §28g.

### B3.18 · Institutional and acronym garbles — SAU 6 above all
**Tier 3 · systemic · Sources: briefing B23**

**SAU 6**: `Sussex` (1.00) · `saw six` · `Saw six` · `SAS six` · `SC six` · `C six` · `Siu six` · `essay you` · `s a you` · `the SA` · `the s a year` · `an saw` · `an Saw board` · `6SA6` · `say you six` · `the essay costs` · `Essar six` (0.42, **not** ESSER) · `at the issue level` · `departments within six` · `to move six forward` · `the Saw meeting` · `the SEO office` · `the Sioux office` · `other essays` = other SAUs. **ESSER**: `Esther is going to write out` · `The answer grant` · `the ceremony` · `s s are funds`. **SREA/SREB**: `Syria` (1.00) · `the SRE` · `SRA` · `the Sri` · `sRGB`/`SRGB` · `shrub process` · `the shrub report` · `Ezra` · `Shri` · **`Astro`** (full confidence, proper noun) · `S Rev` · `SRM` · `the urban s` · `the s report`. **IXL**: `I excel` · `Excel` · `the Excel` (~25×, never a spreadsheet). **paras**: `pears` · `Paris` · `special Ed Perez` · `Paris CBA` · **`parents` and `pairs`**, which run through the whole Article 5 debate and, read literally, turn a paraprofessional pay debate into one about parents. **deliberative session**: `delivered session` · `the liquid session` · `I don't recession`. Others: `Disney`/`Dinard`/`Dessner`/`this nard`/`dessert`/`Denard`/`Dennard`/`dinner`/`Citizens married`/`Does not`/`Disney art` = **Disnard** · `Luft` = Bluff · `dough 25` = DOE-25 · `miss 25`/`miss 26` = MS-25/MS-26 · `sweat tax`/`swept` = SWEPT · `the Dre` = DRA · `DC Wife`/`DC f` = DCYF · `Icon Belt lawsuit`/`Con Valley`/`the canal and the rand`/`the calm down lawsuit`/`convey` (0.98) = ConVal · `500 fours`/`Bible fours`/`five or fours` = 504s · `Kenny Benton`/`McKinney Bento` = McKinney-Vento · `Whitten Wisdom` = Wit & Wisdom · `Vlachs`/`blacks`/`V lax` = VLACS · `New Visions`/`I visions`/`divisions` = iVisions · `Navy`/`Navy Ellis` = Naviance · `yonder` = Yondr · `Tanev`/`Tanith`/`chain up` = TANF · `through primates` = Primex · `recompute` (0.78) = Recompete · `Fate` = FAPE · `admirer` = ADM · `kneecap` = NECAP · `Coast County` = Coös · `Eureka squared`/`Eureka two` = Eureka Math² · `crickets` = Cricut · `pirate school` = PowerSchool · `the front line` = Frontline · `Swiss data` = SWIS · `Swat protocol` = SWOT · `a Chins` = CHINS · `coda` = COTA · `Yes. Why` = ESY · `the Wind blows` = WIN block · `SSL with an a` = ESSA · `type one teachers` = Title I · `the city`/`the state`/`the seat` = **the SAT**, and `the CT`/`the PS`/`the PS 80` = **the PSAT** — "a city that is a test, in a corpus with a City Council" · **`on ceiling previously sealed minutes` = "unsealing previously sealed minutes"**, which reads as a building feature and **hides an entire agenda item** · `See it regarding` = "discussion and vote regarding" · `assistant comments` = citizens' comments · `Extension(s)`/`I opposed graduations` = abstentions · `No lies. Have it.` = "the ayes have it" · `do vocal a motion` = "do a roll call on the motion" · `taking a local` = "taking a roll call" · `the tendency of board members`/`the tenants` (1.00) = the attendance. Three of these change meaning rather than spelling — the unsealing item, the paras/parents inversion and the SAT/PSAT collision — and are the reason this catalogue is load-bearing rather than cosmetic.

*Primary source:* briefing Addenda 3–19, passim.

### B3.19 · Unrecoverable fragments the briefing forbids guessing at
**Tier 3 · systemic · Sources: briefing B25**

Listed wave by wave and never resolved: `Are there witnesses here?` · `buzzsaw into` · `success bonus` · `Patrick Sky` · `Nice meeting in junction` · `Alex Easter who brought you and pester and myself` · `I did chalk at request` · `Is 80 S80` / `585` · `There are three schools in Ireland` · `where we grow the legions. Li.` · `Plot up` (precedes the Stevens roof figure) · `blank mount` (probably "blanket amount") · `2501 0000000` · `to a dot. Dot be done.` · `and ally` · `Below average council` · `And the King's Speech.` · `make sure that map` · `an even a zero` · `Teal in teal room` · `Humbleness just.` · `the lack of said` · `saving answers for funding education` · `And it crops the deposits` · `our customers` · `Is it all the data for you to have?` · `It's not an H anymore` · `It's 25025256 estimate` · `the 1010 3115` · `debris of angles` · `high school is in the cheap` · `regular at a loan` · `their Institute of Justice model` · `That out of your land` · `we can strengthen back to` · `the next female member` · `So this would be a subsidy we have to do` · `Microsoft.` (0.42) and `micros` (1.00), the latter later resolved to **Mikros**.

*Primary source:* briefing Addenda 8, 16, 17, 19.

### B3.20 · Speaker-label inconsistency across the corpus — 1,084 rows normalised
**Tier 3 · systemic, resolved · Sources: briefing B35**

The QA sweep found **342 distinct Speaker values** and normalised **1,084 rows across 17 variants**, with backups in `Scripts/backup_prenorm/` and the `Scripts/speakers/*.speakers.json` mappings updated in step so a rebuild reproduces the corrected names: `Dr. Tim Broadrick`→`Tim Broadrick` (242 rows / 2 files) · `Michael McCosker`→`Mike McCosker` (174/4) · `Dr. Alex Herzog`,`Dr. Herzog`→`Alex Herzog` (151/4) · `Dr. Michael Herrington`→`Michael Herrington` (120/3) · `Lilly Clark`→`Lily Clark` (69/4) · `Michael Koski`→`Mike Koski` (61/3) · `Candace "Candy" Crawford`→`Candace Crawford` (53/1) · **`Mike Campbell`→`Michael Campo` (49/1)** · `Board member (unidentified)`,`Unidentified School Board member`→`Unidentified board member` (46/3) · `Bill Madden`,`William "Bill" Madden`→`William 'Bill' Madden` (43/3) · `Noel Kronberg`→`Noelle Kronberg` (34/3) · `Tessa Nicholson Powers`→`Tess Nicholson-Powers` (22/1) · `Multiple speakers`→`Multiple` (14/5) · `Jen Gallagher`→`Jennifer Gallagher` (10/2). The `Multiple` split was 152 rows across 41 files against 4 rows in 2 files (`14875 SchoolBoard020123`, `15814 SchoolBoard062024`); the clerk split was 28 CSVs on `Noelle Kronberg` against `15455` and `15523` on `Noel`.

*Primary source:* briefing Addenda 8 and 9; `Scripts/backup_prenorm/` and `Scripts/speakers/*.speakers.json`.

### B3.21 · Campo, the auditor — and a spurious "Campbell" next door to it
**Tier 3 · systemic, corrected · Sources: briefing B18**

`Mike Campbell` and `my Campbell` for **Michael Campo**, present from 2023 so not a 2026 artifact; 49 rows in one file were normalised to `Michael Campo` in the QA pass. The neighbouring hazard: **`the Claremont Middle School. Campbell.` at confidence 1.00 is "…Middle School handbook"** — a spurious Campbell at full confidence that names nobody. On many recordings the auditor is only ever "Mike", and the briefing forbids importing the surname or the firm (Plodzik & Sanderson) into files that do not speak them (D1.5).

*Primary source:* briefing Addenda 1, 3, 7, 8, 9.

### B3.22 · A filename that sorts into the wrong month
**Tier 3 · one-off · Sources: briefing B44**

`15299 SAU6110923` sorts among the September shows but the meeting is 11/9/2023. Sort by the DATE in the filename, never by show ID — reinforced by the finding that Cablecast show numbers follow record-creation order, not event order (A3.28).

*Primary source:* briefing Addendum 2; the `Input/Videos` filename set.

### B3.23 · MAP.md miscounts the twin 2/1/23 recordings
**Tier 3 · one-off · Sources: briefing B45 · html-briefing B1 · map+pages §3.1**

MAP.md's note says "825 vs 774 segments"; those are transcript segment counts, while the dialogue CSVs hold **816 and 768 rows**. Use row counts when describing the CSVs.

*Primary source:* the two dialogue CSVs against MAP.md §1's note.

### B3.24 · A cohort of shipped pages cites stale MAP.md section numbers
**Tier 3 · systemic, deferred · Sources: briefing B49 · html-briefing C23**

From before the MAP was renumbered: `17046`→"section 43" (now §104) · `17092`→44 (§105) · `17116`→45 (§106) · `17095`→46 (§107) · `16882`→35 (§96a). A known end-of-run sweep, explicitly **not** to be fixed page by page; new pages use the current numbers.

*Primary source:* MAP.md's renumbering against the shipped pages' citations.

### B3.25 · `Output/HTML/index.html` is roughly 26 pages behind the corpus
**Tier 3 · one-off, deferred · Sources: briefing B50 · html-briefing C24**

It still reads "Forty-five meetings, January 6, 2025 – August 19, 2026" and has been flagged by six agents. One regeneration pass at the end of the run; nobody is to edit it mid-run.

*Primary source:* the index page's own text against the built corpus.

---

# CLASS C — THE PROJECT'S OWN ANALYTICAL ERRORS

Errors the project made and corrected, including the legal-anchor catalogue's own defects, the statute-vintage traps it would have fallen into, the negative anchors that prevent false accusations, and the roster and chronology corrections.

## C · Tier 1 — affects what a reader can conclude

### C-a. Legal-analysis and catalogue corrections

### C1.1 · The mover/seconder clause was wrongly dated, which would have produced two opposite classes of error
**Tier 1 · systemic, corrected 2026-08-29 · Sources: briefing C1 · html-briefing A35, §11 · legal-anchors V21**

Briefing Addendum 10 stated that RSA 91-A:2, II's "names of the members who made or seconded each motion" clause was new — added 2023, 188:1 and amended 2025, 112:1 — and told agents not to apply it before those dates. **That was wrong.** The clause has been in force since **2018, 244:1, eff. January 1, 2019**: the 2017 codification lacks it, the 2019 codification carries it, and it was re-verified three times in wave 1. What 2025, 112:1 added was the start-time, end-time and minutes-producer requirements, which genuinely must not be applied before **22 August 2025**. Two consequences, both stated in the briefing: agents were about to credit districts with voluntary compliance for something the law required, and to miss real defects in 2019–2023 minutes that omit movers or seconders (A1.31).

*Primary source:* the 2017 and 2019 Justia codifications of RSA 91-A:2; https://gc.nh.gov/rsa/html/VI/91-A/91-A-2.htm.

### C1.2 · RSA 32:5 paragraph drift — gross basis and comparative columns both off by one
**Tier 1 · systemic (40 pages), cleared 2026-08-29 · Sources: briefing C2 · html-briefing C12 · legal-anchors C13, F2**

Pages built before 2026-08-29 cite the gross-basis requirement as ¶IV and the comparative columns as ¶V. Both are off by one. The verified mapping: **¶I** is the public hearing not later than 25 days before the meeting with 7 days' notice, and the "after the conclusion of public testimony shall finalize the budget" clause; **¶III** is the gross-basis requirement showing anticipated revenues from all sources; **¶IV** is the comparative columns (at least prior-year appropriations and expenditures), with **¶IV(b)** carrying the alternative for districts whose annual meeting precedes the fiscal-year close; **¶V** is purposes of appropriation appearing in the warrant. Any flag written against "¶IV gross basis" or "¶V columns" cites a paragraph imposing a different duty, so the district would be accused of breaching a provision that says something else and the finding collapses on inspection. **All 40 shipped pages carrying `32:5` were audited paragraph by paragraph and are now correct**, including range citations — so an existing 32:5 citation must not be "fixed".

*Primary source:* https://gc.nh.gov/rsa/html/III/32/32-5.htm ; the 2023 codification at law.justia.com; the paragraph-by-paragraph audit of all 40 shipped pages.

### C1.3 · RSA 91-A:2, ¶I's lettering was wrong, and the caucus argument survives it
**Tier 1 · one-off, corrected 2026-08-29 · Sources: briefing C3 · html-briefing C15 · legal-anchors N8, N10**

The project's own guidance placed legal counsel at I(c). ¶I runs: **(a)** strategy or negotiations for collective bargaining · **(b)** consultation with legal counsel · **(c)** a caucus of members of the same political party · **(d)** circulation of draft documents formalising decisions previously made in a meeting. Counsel is **I(b)**; the caucus really is I(c), so the substantive argument stands — **RSA 671:30** requires every school district without a special statute to use the non-partisan ballot system for electing district officers, unamended since **1979, 321:1, eff. 21 Aug 1979**, so a board elected non-partisanly has no party caucus to hold and the exemption is unavailable as a defence for an off-record quorum. Two further points on ¶I: there is **no "work session" exclusion**, and (d) does not reach a session at which the decision is made.

*Primary source:* https://gc.nh.gov/rsa/html/VI/91-A/91-A-2.htm ; https://gc.nh.gov/rsa/html/LXIII/671/671-30.htm.

### C1.4 · A post-hearing budget reduction was nearly flagged as a violation and is not one
**Tier 1 · systemic rule, cleared 2026-08-29 with no shipped instances · Sources: briefing C4 · html-briefing C13 · legal-anchors N5, N6, F13**

RSA 32:5, ¶I expressly directs the body, "after the conclusion of public testimony", to "finalize the budget to be submitted to the legislative body" — so the post-hearing **$196,001.10** cut is the statute working as written. ¶II confirms it independently: its bar runs only against **insertions** — "shall not thereafter insert … an additional amount or purpose of appropriation which was not disclosed or discussed at that hearing" — so a reduction cannot breach it either. **A post-hearing cut is lawful twice over.** ¶I's wording predates the only recent amendment (2025, 144:1, eff. 30 Aug 2025) and appears verbatim in the 2023 codification, so it was in force throughout the corpus. No shipped page flags a post-hearing reduction as a violation; every post-hearing mention concerns ¶II insertions, correctly.

*Primary source:* RSA 32:5 ¶¶I–II, current text and 2023 codification; corpus sweep of post-hearing mentions.

### C1.5 · The 25-day rule was blended with a calendar deadline and the arithmetic was wrong
**Tier 1 · one-off, corrected on the page 2026-08-29 · Sources: briefing C5 · html-briefing C14**

The 25-day rule is a **floor between hearing and meeting**, not a December 31 deadline, and must not be blended with the SAU-budget deadline, which is a different statute — **RSA 194-C:9, I**, "At a meeting held before January 1". The 12/7/23 page shipped saying "December 14 is twenty-four days before the statutory deadline"; December 14 → January 1 is **eighteen** days. The briefing records that the task brief carried the wrong figure and the agent adopted it — which is why it warns "do not assume a figure in your brief is checked."

*Primary source:* the arithmetic in days against RSA 194-C:9, I.

### C1.6 · A shipped page overstated what an off-camera caucus decided
**Tier 1 · one-off, fixed 2026-08-29 · Sources: briefing C6 · html-briefing C16**

The 12/13/23 page (`15471`) computed a correct **$117,000** binder-to-vote net change and then *located* it at the 18 December caucus, asserting the caucus was "the session at which the figure the board voted on was assembled." That is overreach. The real gap is **$350,000**, between the 18 December **televised** figure (Sprague on tape at 2:04:16, "we're looking at 1.783" on the FY24 base of $34,880,312, i.e. about $36,663,000) and the **$36,313,407.97** moved on 20 December — and Crawford was still reverse-engineering that same difference herself on 5 January ("I was trying to determine where the 350,000…"). The rule generalises: **a gap between what was discussed on tape and what was moved is a hole in the record, not proof of what was decided off camera** — report both figures and the gap, assert nothing about the closed session.

*Primary source:* Sprague on tape 18 December at 2:04:16 against the 20 December motion figure; Crawford on 5 January.

### C1.7 · A consent-agenda sentence was nearly attributed to the wrong meeting
**Tier 1 · systemic risk, cleared as to shipped pages · Sources: briefing C7 · html-briefing C17**

"No discussion, unanimously approved" belongs to the **6 December draft minutes**, not 20 December, and there it disposes of the **11.15.23** minutes rather than 6 December's own. The 20 December defect is the opposite and worse: **no vote was taken at all**. Cleared 2026-08-29 as to shipped pages — `15483` and `15453` both attribute it correctly — and retained as a standing warning to check which document a minutes sentence lives in.

*Primary source:* the December 6 draft minutes; corpus check of `Output/HTML`.

### C1.8 · The catalogue's RSA 186-C:18, III "80%-of-entitlement floor" did not exist before 2025
**Tier 1 · systemic · Sources: briefing C8 · html-briefing C4 · legal-anchors C1, C37, V1, F4**

The skill's catalogue asserted an 80%-of-entitlement floor on proration of catastrophic special-education aid. That floor was added by **2025 N.H. HB 2 §137**, codified at RSA 186-C:18, III(a); the earlier text ends "the appropriation shall be **prorated proportionally based on entitlement**" — no floor at all in 2023–24. Citing the catalogued holding against a pre-FY2026 meeting "would wrongly imply the State broke the law by funding catastrophic aid at 67.5%", and there is **no 90% figure anywhere in that section** (A1.26). An earlier 2025 amendment (2025 N.H. Laws ch. 138 / SB 292, eff. 8/24/25) was superseded in the codified text, so HB 2 is the cite, not SB 292. The paired hazard: the paragraph contains **two different 80 percents** — the department's share of costs above the 3½× threshold up to 10× (2023, 79:141, 142, eff. 1 July 2023) is not the entitlement floor, and reading one as the other reproduces the error by another route.

*Primary source:* https://legiscan.com/NH/text/HB2/id/3254745 ; https://gc.nh.gov/rsa/html/XV/186-C/186-C-18.htm ; 2023 and 2024 Justia codifications.

### C1.9 · RSA 188-E:9-a is not the CTE construction-funding statute
**Tier 1 · one-off miscited anchor, corpus-wide warning · Sources: briefing C9 · html-briefing C10**

It covers charitable donations and the business profits tax credit, not building-aid splits. It must not be cited for building-aid splits, and such figures are to be reported as the speaker's characterization unless the real provision is verified. The related substantive negative is at A1.25: RSA 188-E:3 fixes no percentage at all.

*Primary source:* the text of RSA 188-E:9-a.

### C1.10 · The catalogue's quotation of RSA 91-A:1-a, VI(d) is truncated before the operative clause
**Tier 1 · systemic — it underpins every subcommittee finding · Sources: briefing C9 · html-briefing C9 · legal-anchors C5**

The quotation stops early. The full text ends "…or other political subdivision, **or any committee, subcommittee, or subordinate body thereof, or advisory committee thereto**." That trailing clause is what actually carries every subcommittee flag in the corpus, so with the truncated version no subcommittee of a board or SAU could be shown to be a "public body," and every subcommittee notice and minutes finding would have failed for want of an anchor.

*Primary source:* https://gc.nh.gov/rsa/html/VI/91-A/91-A-1-a.htm.

### C1.11 · The RSA 198:40-a note over-corrected and banned a valid citation
**Tier 1 · systemic · Sources: legal-anchors C2, V2 · html-briefing C5**

The file's earlier note "was wrong in a way that over-corrects, and pages were told not to cite the statute at all. That is too strong." The current amounts — **$4,100 base / $2,300 F&R / $2,100 SPED / $800 ELL**, third-grade reading repealed — were enacted by **2023, 79:150, eff. July 1, 2023**, so for meetings from July 2023 the current statutory text *is* the right one to quote. Uncorrected, pages from the great majority of the corpus would have omitted the governing statute and substituted an NHDOE explainer for it. Before July 2023 the figures were **$3,866.18 / $1,933.08 / $2,079.89 / $756.43** plus $756.43 per third grader below proficient — FY2024 *estimate* rates from NHDOE's 15 November 2022 explainer, computed under the pre-amendment formula, not FY2024–25 actuals.

*Primary source:* https://gc.nh.gov/rsa/html/XV/198/198-40-a.htm ; the 8/2/23 packet Exhibit H; Mary Henry on tape, "base adequacy aid went from 3866 to 4100".

### C1.12 · The RSA 198:40-f row was wrong twice
**Tier 1 · systemic — touches every adequacy-aid page · Sources: legal-anchors C3, V22**

Marked "CORRECTED 2026-08-29 — this row was wrong twice." (a) The dollar figure is the **maximum grant per free-and-reduced-eligible pupil**, not a "grant floor" — the grant floor is an equalized-valuation threshold, **$1,600,000** in the 2023 text. (b) The amounts: **$8,500 governs FY2024 and FY2025** (2023, 79:153, running to 1 July 2025); **$11,500** eff. 1 July 2025; **$11,730** is today's text, from 2025, 141:224, eff. 1 July 2026. Uncorrected, a page would have described a per-pupil maximum as a district-level funding floor and applied a 2026 dollar figure to a 2024 meeting — overstating the grant by roughly 38%.

*Primary source:* https://law.justia.com/codes/new-hampshire/2023/title-xv/chapter-198/section-198-40-f/.

### C1.13 · RSA 198:40-d and RSA 198:40-f were crossed
**Tier 1 · one-off, corrected in place · Sources: legal-anchors C4, V25**

RSA 198:40-d is the **2% annual-adjustment** section, not the extraordinary-needs section; the extraordinary-need grants live at **40-f**. A page citing 40-d for extraordinary-need grants would have pointed at an escalator clause as the authority for a grant programme. Vintage: 40-d is original 2023, 79:151, eff. 1 July 2023, and **2025, 141:223 rewrites it effective 1 July 2026** (adding "rounded up to the nearest whole dollar"), which reaches the 2026 meetings at the end of this backlog.

*Primary source:* https://gc.nh.gov/rsa/html/XV/198/198-40-d.htm ; the 2023 codification of 198:40-f.

### C1.14 · RSA 91-A:3, II(l) vs II(k) — a live misattribution risk
**Tier 1 · systemic · Sources: legal-anchors C6**

**II(l) is the legal-advice exemption. II(k) is the student/tuition-contract exemption**, which carries its own publication duty: the contract **and** the nonpublic minutes must be public **before** approval, and approval must be at a public meeting "at which, or after which, the public has had an opportunity to participate". Crossing them would either excuse a tuition-contract session as legal advice or attribute a publication duty to a privileged consultation.

*Primary source:* https://gc.nh.gov/rsa/html/VI/91-A/91-A-3.htm.

### C1.15 · The RSA 21-J:19 entry quotes words that are not in the statute
**Tier 1 · systemic — a sweep of any page quoting it is directed · Sources: legal-anchors C7, N20, F11**

The file's own "Catalog corrections" section said the section is "permissive as to timing — '*may be conducted within one year*'." **That phrase is not in the section.** The holding (permissive) is right; the quotation is invented, and any page that quoted it must be corrected — it asserts a one-year statutory window that does not exist, which would convert a late audit into a missed statutory deadline. Compounding it, RSA 21-J:19 says "may hire" and names towns, school districts and village districts — **not school administrative units** — so no located NH statute requires an SAU annual audit at all. The only located SAU audit duty is RSA 194-C:4, II(a), which lists "audits" among the services each SAU must provide (1996, 298:3; 2010, 5:2). RSA 197:25 is a *district* fallback. **Treat a late audit as a control weakness, not automatically a missed statutory deadline** (A1.55).

*Primary source:* legal-anchors, "Corrections to THIS file (2026-08-29, waves 6–7)"; https://gc.nh.gov/rsa/html/XV/194-C/194-C-4.htm.

### C1.16 · The catalogue paraphrase of 34 CFR 300.101 was quoted as the regulation
**Tier 1 · systemic — a heavily reused anchor · Sources: legal-anchors C8**

The catalogue paraphrases it as "all children **with disabilities** aged 3 through 21." The regulation says "**all children** residing in the State between the ages of 3 and 21, inclusive." Quoting the paraphrase narrows FAPE's stated scope and would misstate the rule in any page that puts it in quotation marks. Do not quote the paraphrase as the regulation.

*Primary source:* https://www.ecfr.gov/current/title-34/subtitle-B/chapter-III/part-300/subpart-B/subject-group-ECFR6f45db2a2f22b73/section-300.101.

### C1.17 · Two 2023 session laws crossed: 188:1 vs 189:1
**Tier 1 · systemic — three agents independently tripped on it · Sources: legal-anchors C9**

Both took effect **October 3, 2023**: **2023, 188:1 amended RSA 91-A:2** (minutes and notice); **2023, 189:1 amended RSA 91-A:3** and is the source of **¶IV**, the 10-year seal review. Do not attribute ¶IV to 188:1. An attribution error here puts the seal-review duty in the wrong section and would misdate the provision if the two chapters had differed.

*Primary source:* gc.nh.gov source notes — RSA 91-A:3's note ends `2023, 189:1`.

### C1.18 · An agent drafted a flag citing "RSA 91-A:1-a, IX" — there is no such paragraph
**Tier 1 · one-off, caught pre-publication; the failure mode is systemic · Sources: legal-anchors C10, N48**

**RSA 91-A:1-a runs paragraphs I–VI only.** The definition of "meeting" — a quorum convened to discuss or act on a matter within the body's jurisdiction — is at **RSA 91-A:2, I**. The agent caught it; the file records it as "exactly the invented-subsection failure the briefing warns about." Published, the flag would have rested on a paragraph that does not exist.

*Primary source:* https://gc.nh.gov/rsa/html/VI/91-A/91-A-1-a.htm ; https://gc.nh.gov/rsa/html/VI/91-A/91-A-2.htm.

### C1.19 · The catalogue truncates RSA 32:5's disclosure sentence, and it is ¶II
**Tier 1 · systemic — budget pages across the corpus · Sources: legal-anchors C11, C12**

The sentence ends "…shall be disclosed or discussed **AT THE FINAL HEARING**." The catalogue's truncation drops the qualifier, so the sentence reads as a general disclosure duty rather than one keyed to a specific hearing — which would support a flag against a body that disclosed a purpose at an earlier hearing. The same sentence also appeared elsewhere in the catalogue as an unnumbered correction: **it is ¶II**, the paragraph a "changed after the hearing" question actually engages, and without the number it could not be cited precisely and invited the paragraph drift at C1.2.

*Primary source:* https://gc.nh.gov/rsa/html/III/32/32-5.htm ; the 2023 codification at law.justia.com.

### C1.20 · RSA 194-C:5 paragraph error in the 2026-08-28 SAU-governance table
**Tier 1 · one-off · Sources: legal-anchors C14**

That table puts "the SAU board fixes the salaries of all SAU personnel and apportions the expense" at **¶I**. Those sentences are **¶III**. ¶I is the April 1 – June 1 meeting and the election of chairperson, secretary and treasurer (1996, 298:3, eff. Aug. 9, 1996; never amended). A page citing ¶I for salary-fixing points at the reorganization paragraph instead.

*Primary source:* https://gc.nh.gov/rsa/html/XV/194-C/194-C-5.htm.

### C1.21 · RSA 194-C:5, III was quoted incompletely, dropping the removal power
**Tier 1 · one-off entry, high consequence · Sources: legal-anchors C15**

Full ¶III: "…shall fix the salaries of all school administrative unit personnel, shall apportion the expense of the **salaries and benefits** among the several districts, and shall certify the apportionment **to their respective treasurers and to the state board of education**. The school administrative unit board shall have the authority to **remove superintendents and other administrators**." The removal power is the statutory anchor for the January 2024 termination and appears nowhere else in the catalogue; without it, that termination had no located statutory authority and could have been described as ultra vires.

*Primary source:* https://gc.nh.gov/rsa/html/XV/194-C/194-C-5.htm.

### C1.22 · The RSA 91-A:2, I entry drops "contemporaneously" and the chance-encounter sentence
**Tier 1 · systemic · Sources: legal-anchors C16**

The definition of a meeting requires members able to communicate with each other "**contemporaneously**." That single word decides every shared-document and e-mail question, and the catalogue's entry omits it; the entry also omits the chance and social-encounter sentence. Without "contemporaneously", an e-mail chain or a circulated document could be characterised as a meeting, producing a Right-to-Know violation the statute does not support.

*Primary source:* https://gc.nh.gov/rsa/html/VI/91-A/91-A-2.htm.

### C1.23 · "Sequential communications" wrongly attributed to RSA 91-A:2, I
**Tier 1 · systemic, flagged as a live invention risk · Sources: legal-anchors C17**

RSA 91-A:2, I contains **no** "sequential communications" prohibition. The language is in **RSA 91-A:2-a, II**: "Communications outside a meeting, including, but not limited to, sequential communications … shall not be used to circumvent the spirit and purpose of this chapter." RSA 91-A:2-a is in force from **2008, 303:4, eff. July 1, 2008; never amended — it binds the whole corpus**. A serial-communications flag hung on 91-A:2, I quotes text that is not there.

*Primary source:* https://gc.nh.gov/rsa/html/VI/91-A/91-A-2-a.htm.

### C1.24 · 20 U.S.C. §6311(c)(4)(E) — an earlier page cited the wrong clause
**Tier 1 · one-off · Sources: legal-anchors C18**

"(i) is the 95%-participation requirement. (ii) is the denominator rule. (iii) is only the State's duty to explain how it factors (i) in. **An earlier page cited (iii).**" A 95%-participation finding anchored on (iii) rests on a State reporting obligation rather than the participation requirement itself.

*Primary source:* https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title20-section6311&num=0&edition=prelim.

### C1.25 · The attorney-client exemption is RSA 91-A:5, XII, not ¶IV
**Tier 1 · systemic — a sweep of any page citing ¶IV for privilege is directed · Sources: legal-anchors C19, N34, N35**

Corrected 2026-08-29: the attorney-client exemption is **¶XII** — "Records protected under the attorney-client privilege or the attorney work product doctrine." **Any page citing ¶IV for privilege is wrong.** ¶IV covers internal personnel practices, confidential/commercial/financial information and privacy-invading files; both paragraphs from 2022, 122:3, eff. 27 May 2022. ¶IV is also **permissive, not prohibitory** — it permits withholding, does not require it, and is not authority for publishing anything, so citing it in either direction misreads it (A1.60). Related: ¶VI, the emergency-functions/security exemption, is limited by its own terms to material "developed by local or state safety officials that are directly intended to thwart" an act "intended to result in widespread or severe damage to property", so a general safety-plan withholding does not qualify.

*Primary source:* https://gc.nh.gov/rsa/html/VI/91-A/91-A-5.htm.

### C1.26 · The reversed reading of RSA 198:4-b, II(a) — a false HIGH flag on any vote to retain
**Tier 1 · systemic — "correct it wherever you find it" · Sources: legal-anchors C20, F1, V27**

The text reads "**Prior to expending retained general funds**, the school board shall hold a prior public hearing", with newspaper notice of at least 7 days. Earlier wording in the catalogue read as though the hearing had to precede *retention*. That misreading manufactures a false HIGH flag on any vote to retain, and it nearly did on the 16 October 2024 page. ¶II permits retention of ≤5% of net assessment under RSA 198:5 and **states no purpose limitation**; ¶I's "unanticipated expenses" constraint does not reach ¶II money (A1.17). Vintage note recorded to prevent the inverse error: **¶II's cap was 2.5% before 2020, 38:25, eff. 27 Sept 2020** — every meeting in this corpus post-dates that, so applying 2.5% would flag a lawful retention as excessive.

*Primary source:* https://law.justia.com/codes/new-hampshire/2023/title-xv/chapter-198/section-198-4-b/ ; the 2019 codification at law.justia.com.

### C1.27 · "2024, 69:1 post-dates any 2023–24 meeting" was wrong
**Tier 1 · systemic, marked "CORRECTION, ACT ON THIS" · Sources: legal-anchors C21, V18**

The catalogue said RSA 194:23-f's 2024 amendment post-dates the corpus. **It does not. 2024, 69:1, eff. August 13, 2024 binds every meeting from that date**, which is most of the 2024–25 school year in this corpus. New text: the high school selects; the student body elects by simple majority; student government sets procedures; one-year term; ¶III "The school board shall decide the date at which the term shall begin." Use the 2022, 195:2 text only before 13 Aug 2024. The trap runs both ways — 2023 meetings need the earlier text, and post-13-Aug-2024 meetings need the new one — so every student-member page after that date would otherwise have applied superseded text and could have flagged compliant practice as non-conforming.

*Primary source:* https://gc.nh.gov/rsa/html/XV/194/194-23-f.htm.

### C1.28 · RSA 194-C:2's source note was stale, and ¶V (Merger) and ¶IV's withdrawal duties were unrecorded
**Tier 1 · systemic — the Unity withdrawal runs through much of the corpus · Sources: legal-anchors C22, V47**

The catalogue said "Note ends 2010, 5:1, eff. June 18, 2010." **gc.nh.gov now ends 2024, 250:1, 2, eff. July 1, 2024**, and there is a new **¶V (Merger)** — one superintendent, a merger grant of "an additional $200 per pupil… for a period of 2 years", and "merger must be completed by July 1, 2030." **Do not cite ¶V before 1 July 2024.** ¶IV also carries duties the file had not recorded: construction and operating cost estimates; "a proposed plan for the disposition of any school administrative unit assets and liabilities"; a transition plan and timeline; "hold at least one public hearing **no less than 14 days prior** to submission to the state board"; and withdrawal takes effect **on the date the state board issues its certificate**, not a date the parties choose. Uncorrected, a Unity-withdrawal page would have missed the 14-day hearing duty and the certificate-date rule entirely — and would have run on a fourteen-year-old source note.

*Primary source:* https://gc.nh.gov/rsa/html/XV/194-C/194-C-2.htm.

### C1.29 · RSA 197:23 was repealed; the treasurer text is RSA 197:23-a
**Tier 1 · one-off · Sources: legal-anchors C23**

RSA 197:23 was **repealed (1963, 87:2, eff. July 16, 1963)**; the treasurer's-duties text is **RSA 197:23-a**. Citing 197:23 for the manifest or payment-order duty cites a repealed section. Related: RSA 197:22 is the treasurer's bond (1997, 319:4); RSA 197:24 is the acting treasurer. And **RSA 671:2 is "Election Dates" and 671:1 is "Applicability"** — neither enumerates district officers or mentions a treasurer.

*Primary source:* legal-anchors, "FINAL corrections and additions (2026-08-29)".

### C1.30 · The RSA 197:23-a source-note caution — raised, then lifted
**Tier 1 · one-off · Sources: legal-anchors C24**

An earlier entry cautioned that the fetched source note ended "2023, 36:2, eff. July 16, 2023" — the same session-law cite recorded for RSA 35:9 — so a merged neighbouring note could not be ruled out, and directed citing the holding rather than the note. The caution can be **lifted**: two independent re-fetches confirm its own source note genuinely runs 1887, 105:8 … 2021, 65:20-22 … 2023, 36:2, eff. July 16, 2023. Left standing, the caution would have suppressed a valid vintage statement.

*Primary source:* legal-anchors, "FINAL corrections and additions".

### C1.31 · 34 CFR 106.41(c) — "equipment and supplies" is factor (2), not (8)
**Tier 1 · one-off · Sources: legal-anchors C25**

Factor **(2)** is equipment and supplies; **(8)** is "Provision of medical and training facilities and services" (45 FR 30955, as amended 85 FR 30579, 89 FR 33888). An athletics-equity finding citing (8) for equipment points at medical and training facilities instead.

*Primary source:* legal-anchors entry; the Federal Register citations as given.

### C1.32 · The McKinney-Vento definition is at 42 U.S.C. §11434a, not §11432
**Tier 1 · one-off · Sources: legal-anchors C26**

**42 U.S.C. §11434a(2)(A), (2)(B)(i)** carries the definition — "lack a fixed, regular, and adequate nighttime residence" and the "doubled up" category. An earlier catalogue entry points at §11432, which is the definitions section's neighbour: §11432(g)(1)(J)(iii) is the transportation duty, not the definition. A homelessness-eligibility finding cited to §11432 quotes text that is not there.

*Primary source:* https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title42-section11432&num=0&edition=prelim ; §11434a per the correction.

### C1.33 · RSA 288:1's holiday list was under-recorded, producing wrong business-day arithmetic
**Tier 1 · systemic — touches every minutes-timeliness calculation · Sources: legal-anchors C27, N46**

Earlier entries listed only three or four of them, which produced wrong business-day arithmetic. The complete enumeration is **eleven**: January 1 · third Monday in January (MLK Civil Rights Day) · third Monday in February (Washington's Birthday) · last Monday in May · July 4 · first Monday in September · second Monday in October · biennial election day · November 11 · Thanksgiving · Christmas Day. Source note ends 1999, 105:2 / 106:2, eff. Aug. 6, 1999 — so **Juneteenth is not on the list**, and treating it as excluded would shorten a count and manufacture a late posting. Every minutes-timeliness calculation in this corpus must exclude all eleven; with a short list a compliant posting would have been counted late. RSA chapter 288 is Title XXV, not XXIII (D2.16).

*Primary source:* https://gc.nh.gov/rsa/html/xxv/288/288-1.htm.

### C1.34 · RSA 194-C:4, II was recorded as one service when it runs to eighteen
**Tier 1 · systemic, a near-miss false accusation · Sources: legal-anchors C28, N51, F5**

The catalogue recorded only II(a), "audits". The full list includes **(b)** recruitment, supervision and evaluation of staff · **(c)** curriculum development and professional development · **(e)** assessment of pupil achievement · **(f)** district needs assessment · **(p)** annual budgeting · **(r)** consultant identification (1996, 298:3; 2010, 5:2, eff. June 18, 2010). The consequence: **most of what an SAU strategic plan proposes sits INSIDE the SAU's statutory remit** — do not flag such a plan as ultra vires. Where a gap exists it is fiscal, not jurisdictional: the money is appropriated by the constituent district meetings (RSA 194-C:9, I; RSA 189:39). With the one-service record, the SAU strategic plan would have been reported as acting beyond its statutory authority. The chapter also says nothing about employing or evaluating the superintendent — RSA 194-C:5, I is the right anchor for SAU-board authority, and ¶III for the removal power (C1.21).

*Primary source:* https://gc.nh.gov/rsa/html/XV/194-C/194-C-4.htm.

### C1.35 · RSA 40:13, II-a's four lettered subparagraphs were not recorded
**Tier 1 · systemic — every SB 2 budget season · Sources: legal-anchors C29**

¶II-a has four lettered subparagraphs the catalogue did not record: **(a)** notice of budget hearings posted by the second Tuesday in January; **(b)** the RSA 273-A:1, III budget submission date and petitioned articles, also the second Tuesday; **(c)** hearings on or before the third Tuesday, plus supplemental hearings on 7 days' notice, the recessed-hearing rule and the budget-committee delivery date; **(d)** warrants and budgets posted on or before the last Monday in January. In force from 2019, 192:2, eff. July 10, 2019. Without the lettering, the "notwithstanding" resolution at C1.51 could not be pinned to (c), and the January calendar could not be tested article by article.

*Primary source:* https://gc.nh.gov/rsa/html/III/40/40-13.htm.

### C1.36 · RSA 40:13's default-budget definition is ¶IX(b), not ¶XI
**Tier 1 · systemic — every deliberative-session page · Sources: legal-anchors C30 · html-briefing A18**

Recorded twice as a TRAP. **XI(a)** is the disclosure duty plus the four minimum contents of the default-budget form; **XI(b)** is "This amount shall not be amended by the legislative body"; **XI(c)** is the prescribed second-session ballot wording. A page citing XI for the definition quotes a disclosure/form provision as though it defined the budget, and would fail to test the IX(b) eliminated-positions reduction at all — the exact reduction the district's own worksheets truncate (A1.15). Affects the deliberative-session pages at show 14892 (2/8/23), 15552 (2/3/24), 16315 (2/1/25) and 17125 (2/7/26).

*Primary source:* https://gc.nh.gov/rsa/html/III/40/40-13.htm ; the 2023 codification at law.justia.com.

### C1.37 · RSA 40:4 was recorded as ¶I only — the weather-postponement provision was missing
**Tier 1 · one-off entry, systemic use · Sources: legal-anchors C31**

¶II(a)–(c) is the weather-postponement provision: the moderator may postpone "up to 2 hours but not more than 48 hours prior", with a consultation duty, a deeming clause, a **72-hour cap for RSA 40:13 districts**, and the rule that the original date still satisfies statutory deadlines (1998, 278:1; 2019, 192:1, eff. July 10, 2019). Without ¶II, a postponed meeting would appear to breach a statutory deadline that the deeming clause preserves — directly relevant to the 2/8/23 deliberative session, whose snow date was 2/9 (C1.57).

*Primary source:* https://gc.nh.gov/rsa/html/III/40/40-4.htm.

### C1.38 · The RSA 91-A:2, II business-day definition was not previously recorded
**Tier 1 · systemic · Sources: legal-anchors C32**

"A business day means the hours of 8 a.m. to 5 p.m. on Monday through Friday, excluding national and state holidays." It governs every minutes-timeliness calculation in this corpus and was not recorded in the catalogue; absent it, a five-business-day or 144-hour calculation runs on calendar days and calls compliant postings late. Use with the full eleven-holiday list at C1.33.

*Primary source:* https://gc.nh.gov/rsa/html/VI/91-A/91-A-2.htm.

### C1.39 · The RSA 275:42 negative was over-generalised across chapter 275
**Tier 1 · systemic (a reasoning error, not a single citation) · Sources: legal-anchors C33, N2**

The catalogue records that RSA 275:42, I's "employer" does not reach political subdivisions — true, so the eight-day wage-payment rule should not be cited against a school district, but **subdivision-specific**. **RSA 275:78, II** carries its own definition — "…or the state or any of its political subdivisions, which has 6 or more employees working in the state" — which **does** reach a school district. **Check each section's own definition.** Generalised, the negative would have wrongly exempted the district from the state nursing-mothers provisions once they took effect.

*Primary source:* https://gc.nh.gov/rsa/html/XXIII/275/275-78.htm.

### C1.40 · The RSA 194-C:9, ¶IV warning was one-sided
**Tier 1 · systemic for the autumn-2024 wave · Sources: legal-anchors C34, V15**

The catalogue warns against citing ¶IV before October 2024. **¶IV IS in force from 1 October 2024 (2024, 329:1) and therefore binds 11/14/24, 12/3/24, 12/12/24 and everything after** — which matters precisely because the Unity apportionment is contested in that window. Text: the SAU board "may consider other methods" of apportionment; any method "shall have been approved by the constituent school districts"; adopted "only if there is a **majority affirmative vote in each school district**." The 2023 codification runs only to ¶III (source note 2003, 279:1), so the trap misleads both ways: citing ¶IV against a pre-Oct-2024 meeting is wrong, and omitting it from the contested window is equally wrong.

*Primary source:* https://gc.nh.gov/rsa/html/XV/194-C/194-C-9.htm ; the 2023 codification at law.justia.com.

### C1.41 · RSA 194-C:9, ¶I — two clauses not previously recorded
**Tier 1 · systemic for the Unity apportionment thread · Sources: legal-anchors C35**

The equalized valuation is that "of each district **as of June 30 of the preceding school year**"; and the new-service bar runs "unless a majority of the school districts … **representing not less than 60 percent of the total pupils** … have voted favorably." In force from 16 September 2003 (2003, 279:1). Without the June 30 date an apportionment could be tested against the wrong valuation year; without the 60% clause a new-service objection could not be evaluated. Bears directly on the misstated apportionment basis at A1.20.

*Primary source:* https://gc.nh.gov/rsa/html/XV/194-C/194-C-9.htm ; the 2023 codification at law.justia.com.

### C1.42 · Two SAU certifications conflated
**Tier 1 · systemic · Sources: legal-anchors C36**

**RSA 194-C:9, I** — the apportionment is certified **prior to January 15 to the chairperson of each district school board** (2003, 279:1). **RSA 194-C:5, III** — certification is **to the treasurers and to the state board of education** (1996, 298:3). Two different duties, two different recipients, two different deadlines. Conflating them produces a January-15 deadline finding against the wrong duty, or a missed-recipient finding against a district that certified correctly.

*Primary source:* https://gc.nh.gov/rsa/html/XV/194-C/194-C-9.htm ; /194-C-5.htm.

### C1.43 · Three RSA 91-A:3 clauses easy to drop or misquote
**Tier 1 · systemic · Sources: legal-anchors C38, N45, F12**

**¶III's sealing sentence in full**: a seal requires "recorded vote of 2/3 of the members present **taken in public session**" — those four words sit inside the operative clause and are the test for a defective seal. **¶II(c)** ends "other than a member of **the public body itself**" — not "of this board"; **an agenda quoting it correctly must not be flagged**, and reading it the other way would flag an agenda that quoted the statute exactly. **¶IV(b)**: pre-existing minutes never reviewed become "subject to public disclosure **without further action of the public body**." All 2023, 189:1, eff. Oct. 3, 2023.

*Primary source:* https://gc.nh.gov/rsa/html/VI/91-A/91-A-3.htm.

### C1.44 · RSA 91-A:3, ¶I contains no exemptions
**Tier 1 · systemic · Sources: legal-anchors C39, N33**

All of them are in ¶II. **A motion or a set of minutes citing "91-A:3, I(a)" for a subject-matter ground has stated no valid exemption at all.** ¶I(b) requires the motion to state on its face the specific exemption under paragraph II, by roll call, majority of members present; ¶I(c) confines discussion to the matters in the motion. This both supplies a finding — against the 7 August 2024 Claremont minutes (A1.3) — and prevents the inverse error of treating I(a) as a valid ground.

*Primary source:* https://gc.nh.gov/rsa/html/VI/91-A/91-A-3.htm.

### C1.45 · RSA 91-A:3, II(j) and II(i) are routinely misused
**Tier 1 · systemic · Sources: legal-anchors C40, N43, N44**

**II(j)**: "Consideration of confidential, commercial, or financial information that is exempt from public disclosure under RSA 91-A:5, IV **in an adjudicative proceeding pursuant to RSA 541 or RSA 541-A**." Outside an adjudicative proceeding it is not available. **II(i) is EMERGENCY-FUNCTIONS PREPARATION, not student matters** — **II(c)** is the right forum for an individual student matter. Both 2023, 189:1, eff. Oct. 3, 2023. A page validating a II(j) entry outside an adjudicative proceeding, or a II(i) entry for a student matter, would have endorsed a nonpublic session with no available ground.

*Primary source:* https://gc.nh.gov/rsa/html/VI/91-A/91-A-3.htm.

### C1.46 · RSA 189:35-a and RSA 189:34 must not be crossed
**Tier 1 · systemic risk flag · Sources: legal-anchors C41**

**189:35-a, II**: "Ten half days of unexcused absence during a school year shall constitute habitual truancy"; ¶III requires the district to define "half day" (2005, 7:1; 2010, 9:2, eff. July 6, 2010). **189:34, ¶II(a)** is the duty to define "**excused absence**" — a different duty in a different section (2013, 249:14, eff. Sept. 1, 2013). Citing 189:34 for the truancy threshold, or 189:35-a for the excused-absence definition, attributes a duty to a section that does not impose it. Related negative: **RSA 189:24 is "Standard School"**, not attendance or discipline, so a truancy or discipline finding cited to it points at a school-standards provision.

*Primary source:* legal-anchors entry, April–June 2024 wave.

### C1.47 · RSA 53-A:1 does not reach school districts
**Tier 1 · one-off · Sources: legal-anchors C42, N47**

RSA 53-A:1 is "Purpose" and reaches only "municipalities and counties." The definition that names school districts is **RSA 53-A:2**: "public agency" = "any political subdivision… **including but not limited to school districts**" (2016, 46:1, eff. July 2, 2016). **RSA 53-A:3** is the joint-exercise mechanism for a city/district shared position (2016, 46:2). A shared-position analysis anchored on 53-A:1 would have concluded the chapter does not reach the district at all.

*Primary source:* legal-anchors entry, autumn 2024 wave.

### C1.48 · The zero-gap-transcript inference was wrong, and one page still carries it
**Tier 1 · systemic inference pattern; one page outstanding · Sources: legal-anchors C43, F8**

A page in this run inferred from a 1.1-second maximum inter-row gap that "the camera keeps running through the recess and the nonpublic session." **That inference is wrong.** On the 12/7/23 SAU 6 recording the chair says "It is now 625. We will resume at 635" and the board is back **45 recording-seconds later**; the nonpublic session spans 53 recording-seconds of audio that is audibly the room reassembling. Continuous audio plus ten missing wall-clock minutes is a **spliced broadcast**: recording positions stop being clock times after the splice, adjournment times inferred from the tape are wrong, and a nonpublic session's true length is unrecoverable. **The 8/17/23 SAU 6 page makes the same inference ("seventy-six seconds of an unbroken recording") and needs re-checking.**

*Primary source:* the 12/7/23 SAU 6 recording; the 8/17/23 SAU 6 page.

### C1.49 · RSA 32:5, ¶V-a and ¶V-b were not previously recorded
**Tier 1 · systemic for warrant pages · Sources: legal-anchors C44**

**¶V-a** is the recorded-vote / numerical-tally requirement — the tally must appear beside the article. **¶V-b** is the tax-impact notation. Their absence from the catalogue meant the two most directly testable warrant-presentation duties had no anchor, so a warrant omitting a tally could not be flagged.

*Primary source:* https://gc.nh.gov/rsa/html/III/32/32-5.htm.

### C1.50 · HB 358's internal section number is contradicted by the source
**Tier 1 · one-off · Sources: legal-anchors C45**

Two fetches of the bill text disagreed (§20 vs §22). **The effective date is corroborated four ways; the section number is not** — do not state one. The file's own nursing-mothers entry gives the source note as "2023, 191:20". Stating a section number the source does not support would put a specific, checkable falsehood into a page.

*Primary source:* https://legiscan.com/NH/bill/HB358/2023 ; https://gc.nh.gov/rsa/html/XXIII/275/275-78.htm.

### C1.51 · RSA 40:13, II-a's "Notwithstanding any other provision of law" displaces the 25-day floor
**Tier 1 · systemic — every SB 2 budget hearing in the corpus, marked "ACT ON THIS" · Sources: legal-anchors F3, N22**

**RSA 40:13, ¶II-a opens "Notwithstanding any other provision of law"** and expressly governs "Budget hearings under RSA 32:5 and RSA 195:12." Its subparagraph **(c)** puts those hearings "on or before the **third Tuesday in January**", while **¶III** puts the first session "between the first and second Saturdays following the last Monday in January." The two are irreconcilable by design — a third-Tuesday hearing can never be 25 days before a first-Saturday-of-February session — and II-a's "notwithstanding" clause is what resolves it. **LIVE: the 15 January 2025 budget hearing page (MAP §69). 15 Jan → 1 Feb is 17 days. DO NOT FLAG IT.** In force from 2019, 192:2, eff. July 10, 2019.

*Primary source:* https://gc.nh.gov/rsa/html/III/40/40-13.htm.

### C1.52 · 28 CFR 35.200 — a corpus-wide bar on web-accessibility flags
**Tier 1 · systemic · Sources: legal-anchors V33, F6**

Published 89 FR 31337, eff. 24 April 2024 (WCAG 2.1 AA); the compliance dates were amended by **91 FR 20912, 20 April 2026** and now read **26 April 2027 / 26 April 2028 (special district governments)**. **No compliance date had arrived in 2024 and none has arrived yet** — do not flag a district PDF or website as a violation of it on any page in this corpus. A page doing so would accuse the district of breaching a rule whose obligations have not begun. The available provision for a missing coordinator or grievance procedure is **28 CFR 35.107**, in force since 1991.

*Primary source:* https://www.ecfr.gov/current/title-28/chapter-I/part-35/subpart-H/section-35.200.

### C-b. Statute-vintage traps the project would have got wrong

Each is a provision whose currently-served text is not the text in force on a meeting's date. Roughly half this backlog predates the 2025 and 2026 session laws. The vintage traps folded into records above are RSA 186-C:18, III (C1.8), RSA 198:40-a (C1.11), RSA 198:40-f (C1.12), RSA 198:40-d (C1.13), RSA 194-C:9 ¶IV (C1.40), RSA 194:23-f (C1.27), RSA 198:4-b ¶II (C1.26), RSA 194-C:2 ¶V (C1.28), RSA 91-A:2 (C1.1) and 28 CFR 35.200 (C1.52); Ed 503.01 and the two unverified 2026 chapters are held in Class D as unresolved.

### C1.53 · 34 CFR 106.8 / 106.45 — eCFR serves the 2024 Title IX rule
**Tier 1 · systemic · Sources: legal-anchors V3 · html-briefing C6 · briefing D12**

eCFR now serves the 2024 text at 106.8 and 106.45 (2024 Title IX rule, 89 FR 33885). Meetings before August 2024 need the **2020 rule at 85 FR 30026 (May 19, 2020), "These regulations are effective August 14, 2020"** — a page using eCFR would test a 2023 grievance procedure against 2024 requirements. Compounding it, **34 CFR 106.30 now 404s on eCFR** because the 2024 rule replaced it, so for a pre-August-2024 meeting the **2022 CFR annual edition** on govinfo.gov must be quoted. The legal-anchors file records no entry for 106.30; its Title IX trap is anchored on 106.8, 106.45 and 106.41(c).

*Primary source:* https://www.federalregister.gov/documents/2020/05/19/2020-10512/ ; https://www.ecfr.gov/current/title-34/subtitle-B/chapter-I/part-106/subpart-B/section-106.8.

### C1.54 · RSA 188-E:3, II — the 20-year repurposing exception did not exist in 2023
**Tier 1 · systemic for CTE pages · Sources: legal-anchors V4**

The 2023 source note ended 2021, 210:2; the note now ends **2025, 190:1, eff. July 1, 2025**. Today's text carries a 20-year repurposing exception that did not exist in 2023, when a CTE facility became district property "for use by the career and technical education center **exclusively**". A repurposing that breached the 2023 exclusivity rule would look permitted under today's text. Use the 2023 codification (2021, 210:2 text).

*Primary source:* https://gc.nh.gov/rsa/html/XV/188-E/188-E-3.htm.

### C1.55 · 88 Fed. Reg. 65778 — the CEP identified-student percentage fell 40% → 25%
**Tier 1 · one-off provision, systemic within the food-service thread · Sources: legal-anchors V5**

Published 26 September 2023, effective **26 October 2023**. For any meeting before that date, "citing today's rule makes correct 2023 advice look wrong" — a superintendent correctly stating a 40% floor would appear to have misinformed the board. The working link is the govinfo copy; note the document-number trap at D2.17.

*Primary source:* https://www.govinfo.gov/content/pkg/FR-2023-09-26/html/2023-20294.htm.

### C1.56 · RSA 189:11 — Holocaust and genocide instruction, with an incomplete source note
**Tier 1 · one-off · Sources: legal-anchors V6**

Three amendments took effect **1 July 2023**, plus 2024 and 2025 amendments, and "gc.nh.gov's source note shows only the later ones". Subparagraph content and lettering changed. For meetings before 7/1/23 cite the **2020, 29:14** provision and do not assert current subparagraph lettering, or a page will quote a requirement that had not yet been enacted.

*Primary source:* gc.nh.gov RSA 189:11 (source note incomplete).

### C1.57 · RSA 193-F:4 — the bullying-policy element list was amended August 2025
**Tier 1 · systemic for policy-review pages · Sources: legal-anchors V7**

2025, 57:1, **eff. Aug. 1, 2025**, amended the enumerated list of required policy elements, so a district policy compliant with the earlier list would appear deficient on any pre-August-2025 page. Mitigation: cite chapter 193-F rather than quoting the list.

*Primary source:* gc.nh.gov RSA 193-F:4.

### C1.58 · RSA 35:9 — capital reserve funds, amended 16 July 2023
**Tier 1 · one-off · Sources: legal-anchors V8 · html-briefing C7 · briefing D12**

Amended by **2023, 36:2, eff. July 16, 2023**, so the text gc.nh.gov serves today is not the text in force for any 2023 meeting before mid-July — which is every 2023 meeting through the 6/21/23 board and 7/13/23 SAU 6 sessions. Mitigation: **RSA 35:15 is stable (last amended 2021) and is usually the better anchor.** The same session-law cite appears in RSA 197:23-a's note, which triggered and then resolved the merge caution at C1.30.

*Primary source:* gc.nh.gov RSA 35:9 / 35:15.

### C1.59 · RSA 91-A:3, IV — the 10-year sealed-minutes review did not exist before 3 October 2023
**Tier 1 · systemic · Sources: legal-anchors V9**

New paragraph at 2023, 189:1, eff. Oct. 3, 2023: a body may adopt review procedures; absent one it must review and vote by majority whether the ¶III circumstances still apply, "no more than 10 years from the last time the public body voted"; minutes sealed before the effective date and not reviewed within 10 years of it become "subject to public disclosure without further action." **Exclude it from any earlier meeting** — otherwise a board with 30- or 99-year seals would be flagged under a duty that did not yet exist (A1.32).

*Primary source:* https://gc.nh.gov/rsa/html/VI/91-A/91-A-3.htm.

### C1.60 · RSA 141-C:20-c, II — "notarized" was struck in July 2022
**Tier 1 · one-off · Sources: legal-anchors V10**

2022 ch. 55 (HB 1035), **eff. July 19, 2022**, struck the word "notarized". The current text is correct from that date onward, so a district accepting a non-notarized exemption form after 19 July 2022 is compliant; only pre-7/19/22 material needs the earlier text.

*Primary source:* gc.nh.gov RSA 141-C:20-c.

### C1.61 · 2 CFR 200.344 — the 120-day liquidation rule moved paragraph
**Tier 1 · systemic — every 2023–24 ESSER/liquidation page · Sources: legal-anchors V11**

The 120-day liquidation rule was at **paragraph (b)** in 2023 and is at **(c)** today, after the 2024 Uniform Guidance revision effective 1 October 2024. **ED's own June 2024 guidance still cites (b)**, so a page citing (c) would be at odds with the very memo it relies on. Cite the paragraph that existed.

*Primary source:* https://www.govinfo.gov/content/pkg/CFR-2023-title2-vol1/xml/CFR-2023-title2-vol1-sec200-344.xml ; the ED memo on ARP ESSER obligation deadlines and extensions.

### C1.62 · 2 CFR 200.302(b) — reworded by the 2024 revision
**Tier 1 · systemic · Sources: legal-anchors V12**

eCFR now serves "Identification of all Federal awards…", **dropping the 2023 text's "in its accounts"** and rewriting the source-and-application sentence. For 2023–24 meetings a financial-records finding would quote language the district was never subject to. Use the 2023 annual edition via the govinfo pattern (D2.15).

*Primary source:* the govinfo CFR-2023-title2-vol1 annual edition.

### C1.63 · RSA 32:5 — the budget-hearing section was amended in 2025, but ¶¶I–V are unchanged
**Tier 1 · systemic · Sources: legal-anchors V13**

2025, 144:1, **eff. Aug. 30, 2025**; the 2023 text's source note ended 2021, 134:3–4. The file verified that **¶I, ¶II, ¶III, ¶IV and ¶V are identical in the 2023 codification and today** — the 2025 amendment did not disturb them, so those paragraphs bind every meeting in the corpus. Any paragraph outside that verified set needs its own vintage check: "a core budget-process provision — get the vintage right."

*Primary source:* https://gc.nh.gov/rsa/html/III/32/32-5.htm ; https://law.justia.com/codes/new-hampshire/2023/title-iii/chapter-32/section-32-5/.

### C1.64 · RSA 198:41 — the education grant formula changes across 2025, 2026 and 2027
**Tier 1 · systemic · Sources: legal-anchors V14**

The 2023 text is **2023, 79:156, eff. July 1, 2023**; the current note runs to 2025, 141:83, with further 2026 and 2027 effective dates. Any 2023–24 meeting, and each of the late-corpus 2026 meetings, needs its own in-force check.

*Primary source:* gc.nh.gov RSA 198:41.

### C1.65 · RSA 91-A:4 — the Right-to-Know records section carries its own 2024 trap
**Tier 1 · systemic · Sources: legal-anchors V16**

2024, 49:1, 2, **eff. Aug. 13, 2024**. ¶I's inspection right is old and safe. The current ¶IV(b)–(d) cost rule — five business days to make available, deny, or state the time reasonably necessary; **(d)** only "the actual cost of providing the copy"; "**No cost or fee shall be charged for the inspection or delivery, without copying**" — carries the 2024 note and must not be applied to a pre-August-2024 records request.

*Primary source:* gc.nh.gov RSA 91-A:4.

### C1.66 · RSA 198:4-d — only the September 1 filing date is safe for earlier meetings
**Tier 1 · systemic for finance pages · Sources: legal-anchors V17**

The section was amended by **2025, 141:401, eff. July 1, 2025**. For any pre-July-2025 meeting, only the September 1 DOE-25 filing date is safe to rely on; quoting any non-date element of the current section would import later text. The section contains no extension provision in any vintage (A1.23).

*Primary source:* gc.nh.gov RSA 198:4-d.

### C1.67 · RSA 198:15-a, IV — building aid, with a 2024 amendment that post-dates 2023
**Tier 1 · one-off · Sources: legal-anchors V19**

2023, 35:2, eff. July 1, 2023; **2024, 47:1 post-dates any 2023 meeting**. Applying the 2024 text to a 2023 meeting misstates the provision.

*Primary source:* gc.nh.gov RSA 198:15-a.

### C1.68 · RSA 169-D:2 — the CHINS definitions were amended in 2024
**Tier 1 · one-off · Sources: legal-anchors V20**

Last pre-October-2023 amendment 2021, 182:5; **2024, 42:7 and 88:6 post-date** any 2023 meeting, so quoting the current definition against one imports later text.

*Primary source:* gc.nh.gov RSA 169-D:2.

### C1.69 · Ed 306.07 (School Facilities) — the 12-13-2024 readoption
**Tier 1 · systemic, part of the Ed 306 renumbering family · Sources: legal-anchors V23**

Both Cornell/LII and the state site serve the readopted text (Doc. #14150, eff. 12-13-24), so any 2023–24 facilities finding tested against it is tested against later text. Recovery route: the 2023 text is recoverable from NHDOE's own March 2023 side-by-side revision draft, which prints the quoted requirements in the *existing* column.

*Primary source:* https://gc.nh.gov/rules/state_agencies/ed300.html ; NHDOE March 2023 side-by-side.

### C1.70 · Ed 306.15 — renumbered and re-captioned
**Tier 1 · systemic · Sources: legal-anchors V24**

Under Doc. #14150, eff. 12-13-24, **Ed 306.15 is "School Year" today but was "Provision of Staff and Staff Qualifications" in 2023.** The catalogue's 2026-08-19 entry gives Ed 306.15 as the 180-day/hour-equivalents rule (≥450 h kindergarten, ≥945 h grades 1–6, ≥990 h grades 7–12). For any 2023 meeting a school-year finding cited to Ed 306.15 would point at a staffing rule.

*Primary source:* https://gc.nh.gov/rules/state_agencies/ed300.html.

### C1.71 · RSA 275:78, :79, :81 — the NH nursing-mothers duty did not exist before 1 July 2025
**Tier 1 · systemic across the 2023–mid-2025 window · Sources: legal-anchors V26**

2023, 191:20 (HB 358, 2023 N.H. Laws ch. 191, signed August 2023), **eff. July 1, 2025**; penalties at RSA 275:82 follow **1 July 2026**. "**Any 2023 – mid-2025 meeting told a nursing-mothers policy is 'required by state law' is being told something not yet true.**" The binding source in that window is the federal **PUMP Act, 29 U.S.C. §218d**, in force from 29 December 2022 — which the district's own policy miscites to title 42 (A1.10). Do not state HB 358's internal section number (C1.50).

*Primary source:* https://gc.nh.gov/rsa/html/XXIII/275/275-78.htm · /275-79.htm · /275-81.htm ; https://legiscan.com/NH/bill/HB358/2023.

### C1.72 · RSA 198:20-b, III — the hearing threshold was $5,000, not $20,000
**Tier 1 · one-off boundary, systemic in the gift-acceptance thread · Sources: legal-anchors V28 · briefing D12**

2023, 38:1, **eff. July 18, 2023**, raised the threshold from **$5,000** to **$20,000**. III(a) at ≥$20,000: public hearing plus newspaper notice ≥7 days stating **time, place AND subject**; III(b) under $20,000: "school board shall post notice in agenda and include notice in meeting minutes." ¶I conditions the authority on a district enabling article. Any pre-18-July-2023 gift or grant between $5,000 and $20,000 is affected: citing the current text "turns a *required* hearing into an apparently voluntary courtesy, inverting the finding."

*Primary source:* gc.nh.gov RSA 198:20-b.

### C1.73 · RSA 193:38 — discrimination in public schools, amended September 2024
**Tier 1 · systemic for the 2023–Aug 2024 window · Sources: legal-anchors V29**

2019, 282:1 (SB 263), eff. Sept. 17, 2019; **2024, 117:1, eff. Sept. 1, 2024**. "The text served today is not the text in force for any 2023 – Aug 2024 meeting" — a discrimination finding for that window would be tested against later language.

*Primary source:* https://gc.nh.gov/rsa/html/xv/193/193-38.htm.

### C1.74 · RSA 671:20 — ¶II was added in 2025
**Tier 1 · systemic across the ballot pages · Sources: legal-anchors V30**

The section was one sentence (ballot preparation by the district clerk) from 1979, 321:1; **2025, 281:1, eff. Sept. 30, 2025** adds ¶II, which requires the ballot to print, immediately preceding the school-budget question, the preceding year's average cost per pupil per RSA 189:75, I(a) and "ELA Proficiency: X%; Math Proficiency: X%; Science Proficiency: X%", as the school district clerk's duty. **Do not apply ¶II before that date** — a 2024 ballot omitting proficiency scores would be flagged under a duty that did not exist; it *is* in force for any page dated on or after 30 September 2025.

*Primary source:* https://gc.nh.gov/rsa/html/LXIII/671/671-20.htm.

### C1.75 · RSA 193-C:6 — statewide assessment and the parental opt-out, amended October 2024
**Tier 1 · systemic · Sources: legal-anchors V31**

2018, 91:1, eff. July 24, 2018; **amended 2024, 350:3, eff. Oct. 1, 2024**, so the section as served today post-dates every meeting before that date. Content: unconditional parental exemption; "shall not penalize any exempted student nor shall the department… penalize any school district for a lower participation rate"; the district must develop an exemption **form** and provide an **alternative activity**.

*Primary source:* gc.nh.gov RSA 193-C:6.

### C1.76 · RSA 188-E:1-a — ¶VI was added in July 2025
**Tier 1 · one-off · Sources: legal-anchors V32**

2022, 272:2, eff. July 1, 2022; **2025, 229:1, 2, eff. 1 July 2025** adds a ¶VI (a CTE access programme by 1 January 2026). The 2023 codification has **five** paragraphs — do not cite ¶VI before July 2025, or a pre-July-2025 CTE page is tested against an access-programme duty that did not exist.

*Primary source:* gc.nh.gov RSA 188-E:1-a.

### C1.77 · RSA 193-E:2-a, I — the eleven learning areas were amended September 2024
**Tier 1 · systemic for adequacy pages · Sources: legal-anchors V34**

Source note ends **2024, 186:1, eff. Sept. 10, 2024**. Today's text does not govern meetings before that date.

*Primary source:* https://gc.nh.gov/rsa/html/XV/193-E/193-E-2-a.htm.

### C1.78 · RSA 193:3 — change of school / best interest of student, amended July 2025
**Tier 1 · one-off · Sources: legal-anchors V35**

**2025, 293:1, eff. July 1, 2025.** Today's text is not the 2023–24 text.

*Primary source:* gc.nh.gov RSA 193:3.

### C1.79 · 89 FR 30046 — the 2024 Uniform Guidance revision is the boundary for this backlog
**Tier 1 · systemic · Sources: legal-anchors V37**

Published 22 April 2024, **effective 1 October 2024**, and it "applies to awards issued on or after that date, so a 2023–24 award stays under the 2023 annual edition." The revision doubled the equipment/supplies threshold **$5,000 → $10,000** and raised the single audit threshold **$750,000 → $1,000,000**. It is "the boundary that makes the govinfo `CFR-2023-…` pattern the right one for this backlog" (D2.15). The file gives two different Federal Register starting pages for the same revision — see C2.8.

*Primary source:* https://www.federalregister.gov/documents/2024/04/22/2024-07496/.

### C1.80 · 2 CFR 200.313 — the equipment disposition threshold doubled
**Tier 1 · systemic · Sources: legal-anchors V38**

**89 FR 30136, Apr. 22, 2024, eff. 1 Oct 2024**; the pre-2024 threshold was **$5,000**, and disposition now applies to equipment "with a current fair market value of **$10,000 or less (per unit)**." Section content: equipment use, property records, **biennial** physical inventory, loss-prevention control system, maintenance. A 2023–24 disposal of $6,000 equipment would look exempt under today's text when it was not.

*Primary source:* eCFR 2 CFR 200.313 and the govinfo CFR-2023 annual edition.

### C1.81 · 2 CFR 200.501 — the single-audit threshold depends on the audited year's vintage
**Tier 1 · systemic · Sources: legal-anchors V39**

**$1,000,000 for fiscal years beginning on or after 2024-10-01, otherwise $750,000.** A district spending $800,000 in FY2024 owed a single audit; the same spend in a fiscal year beginning after 1 October 2024 does not. Pick the threshold by the audited year's vintage.

*Primary source:* https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-F/section-200.501.

### C1.82 · RSA 186-C:2 — the ages 3–21 definition was amended September 2025
**Tier 1 · systemic for special-education eligibility pages · Sources: legal-anchors V40**

**2025, 156:1, eff. Sept. 5, 2025.** "Today's gc.nh.gov text is not the text in force for any 2023–24 meeting; use the 2024 codification."

*Primary source:* gc.nh.gov RSA 186-C:2.

### C1.83 · RSA 186-C:3-a — today's text is the December-2024 text, and it says nothing about preschool
**Tier 1 · one-off · Sources: legal-anchors V41, N24**

Source note ends **2024, 351:2, eff. Oct. 1, 2024**, so today's text does not govern pre-October-2024 meetings. Substantively it is also a negative anchor: the section opens "The division shall help school districts meet their responsibilities under this chapter…", imposing duties on the State's division and department, and says **nothing about preschool, pre-kindergarten or children aged 3–5, and nothing releasing a district from operating a preschool programme**. Citing it for a preschool obligation or exemption quotes a State-duty provision.

*Primary source:* https://gc.nh.gov/rsa/html/XV/186-C/186-C-3-a.htm.

### C1.84 · Ed 306 — the December 2024 readoption, with the numbers
**Tier 1 · systemic · Sources: legal-anchors V42, D14 · html-briefing C8 · briefing D12**

Doc. **#14150, eff. 12-13-24**, readopted Ed 306.01–306.28. **Ed 306.14 "Student-Educator Ratios"** was 306.17 "Class Size": K–2 **25 or fewer** per educator (striving for 20); grades 3–5 **30 or fewer** (striving for 25); middle and high school **30 or fewer**. **Ed 306.12(d)** (was 306.15): each school with an **enrollment of 500 or more** provides an assistant principal, or two or more persons with Ed 506 administrative licensure acting as an FTE — "keyed to **enrollment**, not ADA/ADM, and it is a **floor**." **Ed 306.17 is now "Alternative Programs."** Any class-size or administrator-staffing finding for a pre-13-Dec-2024 meeting cited to today's numbering points at a different subject, and using ADA/ADM instead of enrollment misapplies the assistant-principal rule in either vintage. **Cite the part page; do not guess subsection numbers.**

*Primary source:* https://gc.nh.gov/rules/state_agencies/ed300.html ; NHDOE's March 2023 side-by-side.

### C1.85 · RSA 32:5-e and RSA 32:5-f — the school district budget cap did not exist before 1 October 2024
**Tier 1 · systemic for the 2025–26 pages · Sources: legal-anchors V43**

**2024, 353:2, eff. Oct. 1, 2024**; **2025, 183:5 (32:5-e) and 183:6, 7 (32:5-f), eff. Sept. 13, 2025**. **32:5-f ¶III** requires a public hearing "at least 15 days, but not more than 30 days, before the question is to be voted on", notice in ≥2 public places and published in a newspaper ≥7 days prior; **¶IV** fixes mandatory ballot wording carrying a *dollar* blank — "_____ dollars per pupil cost" — closing "as of October 1." In force, ¶III is why a budget-cap article can require a February hearing of its own even in an SB 2 district that has already held its deliberative session: for a 10 March vote the window is 8–23 February, and a 7 February deliberative session falls one day outside it. Applying any of it to a pre-October-2024 meeting is wrong (A1.22).

*Primary source:* https://gc.nh.gov/rsa/html/III/32/32-5-e.htm ; /32-5-f.htm.

### C1.86 · RSA 189:75–189:78 — cost-per-pupil and the Mandatory Report to Voters
**Tier 1 · one-off boundary, systemic within the 2026 pages · Sources: legal-anchors V44, N49**

All **2024, 332:3, eff. July 1, 2025**. **189:75, I** cost-per-pupil is "the **LOWEST** of three alternatives (a)/(b)/(c)"; **189:76** Mandatory Report to Voters is "a real, testable posting duty **first reaching the 2026 annual meeting**". Applying the report duty to any earlier meeting, or computing cost-per-pupil by any alternative other than the lowest, is wrong. **Chapter 189 ends at 189:78** — a citation to a higher section number in that chapter does not exist.

*Primary source:* gc.nh.gov RSA 189:75–:78.

### C1.87 · RSA 194-D:5 — open enrolment, amended September 2025
**Tier 1 · one-off · Sources: legal-anchors V45**

2009, 241:14, eff. Sept. 14, 2009; **2025, 211:2, eff. Sept. 13, 2025**. ¶I carries the 80% figure; **¶II assigns special-education funding and decision-making to the SENDING district**. Applying the current ¶II allocation to a pre-September-2025 meeting is wrong.

*Primary source:* gc.nh.gov RSA 194-D:5.

### C1.88 · RSA 194-B:11 — chartered public school adequacy, amended July 2025
**Tier 1 · one-off · Sources: legal-anchors V46**

Note ends **2025, 141:81, 82, eff. July 1, 2025**. The State pays a state-authorised chartered public school adequacy under RSA 198:40-a "**plus an additional grant of $4,900**" per pupil from the education trust fund, and "The child's **resident district** shall have the responsibility, including financial responsibility, to ensure the provision of the special education and related services in the child's IEP." Applying the $4,900 figure or the current resident-district allocation to a pre-July-2025 meeting is wrong.

*Primary source:* gc.nh.gov RSA 194-B:11.

### C1.89 · RSA 200:11-a — school air quality, amended September 2024
**Tier 1 · one-off · Sources: legal-anchors V48**

**2024, 226:7, eff. Sept. 17, 2024**; the core annual air-quality survey duty dates to 2010, 319:1 and is safe throughout. Quoting the current text against a pre-September-2024 meeting imports later language.

*Primary source:* gc.nh.gov RSA 200:11-a.

### C1.90 · RSA 194:61 — unused district facilities, amended August 2023
**Tier 1 · one-off · Sources: legal-anchors V49, N29**

**2021, 186:1, eff. Aug. 10, 2021; 2023, 198:3, eff. Aug. 4, 2023.** A sale or lease must be subject to an approved chartered public school's **right of first refusal**, and the superintendent reports unused facilities annually. Applying the current text to a meeting before 4 August 2023 is wrong. Paired negative: **RSA 194-B:3-a is NOT the charter-school property statute** — chapter 194-B contains no such section; 194:61 is.

*Primary source:* gc.nh.gov RSA 194:61.

### C1.91 · RSA 189:13-a — the SAU is named in some paragraphs and not others
**Tier 1 · systemic paragraph-scope trap · Sources: legal-anchors V50**

2023, 55:1, eff. July 31, 2023; **164:1, 2, eff. Sept. 26, 2023** (last amendment). **¶V** — "The governing body of **a school district**, chartered public school, or public academy shall adopt a policy relative to hiring practices…" — does **not** name the SAU; **¶I(a)/¶VI** — "The **employing school administrative unit**, school district, or chartered public school shall complete a criminal history records check…" — does. A hiring-policy flag against the SAU under ¶V cites a paragraph that does not reach it, and pre-26-September-2023 meetings need the earlier text.

*Primary source:* https://gc.nh.gov/rsa/html/xv/189/189-13-a.htm.

### C1.92 · 7 CFR 210.16 and 7 CFR 210.14(e) — food service
**Tier 1 · one-off · Sources: legal-anchors V51**

210.16 runs 53 FR 29147 through **88 FR 57845, Aug. 23, 2023**; 210.14(e) was last amended **89 FR 32073, Apr. 25, 2024**. 210.16(d): a food service management company contract "shall be of a duration of no longer than 1 year", renewals "may not exceed 4 additional years". 210.14(e): "The maximum annual average price increase required under this paragraph shall not exceed ten cents." Applying the post-April-2024 paid-lunch-equity cap to an earlier year is wrong — and this is the ceiling that bounds the ten-cent-per-meal agreement at A1.36.

*Primary source:* https://www.ecfr.gov/current/title-7/subtitle-B/chapter-II/subchapter-A/part-210/subpart-D/section-210.16.

### C1.93 · RSA 485:17-a — lead in school drinking water, amended July 2022
**Tier 1 · one-off · Sources: legal-anchors V52**

2018, 4:18, eff. July 1, 2019; **2022, 325:1, eff. July 8, 2022**. Three rounds of testing, sampling completed 1 Jan 2016 – 30 Jun 2024; action level **5 ppb**; on exceedance **notify parents within 5 business days** and supply compliant water; department-approved remediation plan **within 180 days**. Applying the 5 ppb action level or the 5-business-day notice to a pre-July-2022 event is wrong.

*Primary source:* gc.nh.gov RSA 485:17-a.

### C-c. Negative anchors — provisions verified NOT to say what one might assume

Each of these prevents a finding the record would otherwise seem to support. Those already folded into records above: RSA 92-A (A1.1), RSA 194:4 (A1.5), RSA 671:5 (A1.6), RSA 671:20/671:25 (A1.7), 42 U.S.C. §218d (A1.10), RSA 188-E:3 (A1.25), RSA 32:5-b (A1.22), RSA 198:4-d (A1.23), "interim moderator" (A1.16), BEDH §B.2 (A1.19), RSA 194-C:5, I's three offices (A1.29), RSA 32:5 ¶¶I–II (C1.4), RSA 671:30 and the ¶I exclusions (C1.3), RSA 21-J:19 (C1.15), RSA 194-C:4 (C1.34), RSA 91-A:5 ¶IV and ¶VI (C1.25), RSA 91-A:3 ¶I, II(c), II(i), II(j) (C1.43–C1.45), RSA 288:1 (C1.33), RSA 53-A:1 (C1.47), RSA 91-A:1-a ¶IX (C1.18), RSA 189:24 (C1.46), RSA 186-C:3-a (C1.83), RSA 194-B:3-a (C1.90), chapter 189's last section (C1.86), RSA 275:42 (C1.39) and RSA 40:13, II-a (C1.51).

### C1.94 · 45 CFR part 1308 no longer exists
**Tier 1 · one-off · Sources: legal-anchors N4**

Head Start disability standards are now at **45 CFR 1302 subpart F, §§1302.60–.63**. A citation to part 1308 resolves to nothing.

*Primary source:* legal-anchors catalogue correction.

### C1.95 · RSA 91-A:2, IV is state-government-only — a school board must be assessed under ¶III
**Tier 1 · systemic · Sources: legal-anchors N11**

¶IV applies "only to boards, committees, councils, advisory committees and like bodies of **STATE** government." It is not available to a school board or an SAU board; **¶III** is the paragraph that governs them. ¶III(a)–(e): remote attendance only when in-person "is not reasonably practical", with the reason stated in the minutes; a quorum physically present; all members able simultaneously to hear and speak to each other; and **(e) "All votes taken during such a meeting shall be by roll call vote."** In force 2023, 188:1, eff. Oct. 3, 2023 (next 2025, 112:1, eff. Aug. 22, 2025).

*Primary source:* https://gc.nh.gov/rsa/html/VI/91-A/91-A-2.htm.

### C1.96 · New Hampshire does not require a district to employ a school nurse
**Tier 1 · systemic · Sources: legal-anchors N12**

**RSA 200:27** says a district "may provide"; **RSA 200:29** "may nominate and … appoint". **RSA 200:38** imposes mandatory immunisation and examination duties **on the nurse**, "so a vacancy leaves those duties unheld — that, not a staffing mandate, is the defensible finding." 1971, 499:1 · 2023, 172:1, 2, eff. July 28, 2023 · 2001, 83:2, II.

*Primary source:* gc.nh.gov RSA 200:27, :29, :38.

### C1.97 · RSA 188-E:5, I names no region number
**Tier 1 · one-off · Sources: legal-anchors N15**

The program "shall be broad enough to serve the **reasonable business and industry needs of the area**" (note ends 2022, 272:3, 4). A finding that a centre served the wrong region has no statutory region definition to rest on — which bears on the Region 10 / "Region 17" confusion at A1.56.

*Primary source:* gc.nh.gov RSA 188-E:5.

### C1.98 · 20 U.S.C. §7801 — the "highly qualified teacher" definition was struck
**Tier 1 · systemic as a corrective · Sources: legal-anchors N16**

ESSA §8002 (Pub. L. 114-95, Dec. 10, 2015) struck the definition. "Reach for it whenever a board dates a staffing constraint to NCLB" — a page repeating a board's NCLB-era framing would apply a repealed federal standard.

*Primary source:* legal-anchors entry.

### C1.99 · RSA 189:68-a imposes duties on OPERATORS, not districts
**Tier 1 · one-off · Sources: legal-anchors N19**

"Student Online Personal Information" (2015, 128:1, eff. Jan. 1, 2016). **A district cannot breach it; do not cite it against one.**

*Primary source:* legal-anchors entry.

### C1.100 · RSA 273-A:3 contains no two-week duty on a public employer
**Tier 1 · one-off · Sources: legal-anchors N21**

¶II(a) is a **120-day-before-budget-submission-date** notice on the party *desiring to bargain*; ¶IV requires the employer to record that date with the PELRB (note ends 2013, 244:1, eff. Sept. 22, 2013). A two-week response finding against the board has no basis in the section. Related: **RSA 197:3, III**, not RSA 273-A:3, is the special-meeting authority for negotiated cost items (note ends 2021, 77:1, eff. Aug. 17, 2021). RSA 273-A is Title XXIII, not LXIII (D2.16).

*Primary source:* gc.nh.gov RSA 273-A:3.

### C1.101 · RSA 193:13, I(a) — the suspension gate is a WRITTEN DESIGNATION, not a credential
**Tier 1 · systemic for discipline pages · Sources: legal-anchors N25**

"A representative **designated in writing** by the superintendent … may suspend pupils … not to exceed 10 consecutive school days" (2020, 38:1, eff. July 29, 2020 and July 1, 2021). The gate is the written designation, not an administrator's credential, so a suspension flag based on the suspender's job title or licence misses the actual test.

*Primary source:* gc.nh.gov RSA 193:13.

### C1.102 · RSA 33:7 does not reach school districts, and RSA 198:20-a is not it either
**Tier 1 · one-off · Sources: legal-anchors N27**

"Tax Anticipation Notes" runs to *cities and towns* and *village districts* only (note ends 1997, 105:3, 4). RSA 33:1's "municipality" does include a school district (2018, 118:1) "but 33:7 does not use that word." And RSA 198:20-a is about payments to non-approved nonpublic schools for disabled children. **Do not cite either for a school-district tax anticipation note.**

*Primary source:* legal-anchors entry.

### C1.103 · RSA 189:1 creates no State Board waiver power
**Tier 1 · one-off · Sources: legal-anchors N28**

180 days "or the equivalent number of hours as required in the rules of the department of education" (2011, 42:1, eff. July 8, 2011; unamended). A page describing a State Board waiver of the school-year requirement would invent a power.

*Primary source:* gc.nh.gov RSA 189:1.

### C1.104 · RSA 5-B:5 sets standards for the pooled risk management PROGRAMME, not a duty on a district
**Tier 1 · one-off · Sources: legal-anchors N31**

It is not a resolution duty on a participating district. A finding that the district failed to adopt a required resolution misreads whom the section binds. RSA chapter 5-B is Title I (D2.16).

*Primary source:* `gc.nh.gov/rsa/html/I/5-B/5-B-mrg.htm`.

### C1.105 · RSA 189:29-b creates no gifted-and-talented programming mandate
**Tier 1 · one-off · Sources: legal-anchors N32**

It requires only an annual narrative report, which "**shall so state**" if no programmes exist. A district with no gifted programme is compliant so long as it reports, and a page treating 189:29-b as a mandate would flag the absence of a programme.

*Primary source:* legal-anchors catalogue correction.

### C1.106 · RSA 194-C:9 requires no public hearing on the SAU budget
**Tier 1 · systemic · Sources: legal-anchors N36, F14**

¶I is the only calendar duty: "At a meeting held before January 1, the school administrative unit board shall adopt a budget." **So a district that holds a hearing exceeds the statutory minimum**, and a page importing RSA 32:5's hearing regime into the SAU budget would flag a compliant board for doing more than the law requires.

*Primary source:* https://law.justia.com/codes/new-hampshire/2023/title-xv/chapter-194-c/section-194-c-9/.

### C1.107 · RSA 32:1 does not name school administrative units
**Tier 1 · systemic · Sources: legal-anchors N37**

RSA 32:1 states the chapter's application in terms of "towns, districts, school districts and village districts — **it does not name school administrative units**." RSA 32:10 lets a *governing body* transfer between appropriations, which is useful when a district or SAU policy is said to be "consistent with RSA 32:10". **Chapter 194-C, not RSA ch. 32, is where an SAU's budget authority lives.**

*Primary source:* https://gc.nh.gov/rsa/html/III/32/32-1.htm ; /32-10.htm.

### C1.108 · RSA 194-C:5, II(a) — the office of superintendent is not compulsory
**Tier 1 · systemic · Sources: legal-anchors N38**

"School districts shall not be required to have a superintendent" — superintendent *services* are compulsory, the office is not, "which is why 'superintendent or executive director' appears in this record." II(c): a new administrative position needs **50% of districts representing 60% of pupils**. 1996, 298:3; never amended. A page flagging the absence of a titled superintendent would flag a lawful arrangement.

*Primary source:* https://gc.nh.gov/rsa/html/XV/194-C/194-C-5.htm.

### C1.109 · RSA 194-C:8 — an uncounted voice vote is not irregular
**Tier 1 · systemic · Sources: legal-anchors N40**

Weighted votes "shall only be used **upon the demand of a majority** of the members of any board present and voting", so uncounted voice votes are not irregular — but the statute makes district voting strength relevant to officer elections. This bounds the tally findings at A1.31: the defect there is the absence of movers, seconders and any announced count where the minutes must record them, not the voice vote as such.

*Primary source:* https://gc.nh.gov/rsa/html/XV/194-C/194-C-8.htm.

### C1.110 · RSA 194-C:1 — an SAU may not hold land, buildings, borrow or mortgage
**Tier 1 · one-off · Sources: legal-anchors N41**

Units "shall be corporations… to make necessary contracts in relation to any function of the corporation", with an **express bar on land, buildings, borrowing and mortgages** (1996, 298:3, eff. Aug. 9, 1996). Establishes both what an SAU may do and the outer bound of it — relevant to the asset-and-liability disposition plan RSA 194-C:2, ¶IV requires on withdrawal (C1.28).

*Primary source:* gc.nh.gov RSA 194-C:1.

### C1.111 · RSA 197:7 fixes no number of signatures
**Tier 1 · one-off · Sources: legal-anchors N42**

Posting the warrant, attested copy, **14 days** (1975, 11:4, eff. Apr. 25, 1975) — "and it fixes no number of signatures." A finding that a warrant lacked required signatures has no basis here.

*Primary source:* gc.nh.gov RSA 197:7.

### C1.112 · RSA 194:10 — officer salaries belong to the voters
**Tier 1 · one-off; this one supplies a finding rather than preventing one · Sources: legal-anchors N52**

"At its annual meeting each school district shall determine the salaries of its school board and other district officers, and the district clerk shall certify the same to the selectmen" — unamended since 1927. In an SB 2 district the "annual meeting" is the deliberative session plus the March ballot, so **a board that fixes an officer's pay by its own vote — Claremont, 11/1/23, clerk at $300 per meeting — is doing what this section gives to the voters.**

*Primary source:* https://gc.nh.gov/rsa/html/XV/194/194-10.htm.

### C1.113 · RSA 40:13 has no vintage trap, and neither do seven neighbouring provisions
**Tier 1 · systemic · Sources: legal-anchors N53 · briefing D12**

"IN FORCE FROM: 2019, 192:2, eff. July 10, 2019 — the last amendment. The text served today is the text in force for EVERY meeting in this corpus. Durable; no vintage trap." Likewise **RSA 40:10** (1996, 64:1, eff. July 1, 1996; never amended), **RSA 40:4-b** (1971, 524:1; never amended), **RSA 189:39** (1971, 371:2; never amended), **RSA 273-A:5, I(e)** (1979, 374:4; never amended), **RSA 32:8** (1993, 332:1, eff. Aug. 28, 1993; unamended), **RSA 671:30** (1979, 321:1; never amended) and **RSA 91-A:2-a** (2008, 303:4; never amended). Recorded so that a vintage caveat is not attached where none is needed.

*Primary source:* the source notes of the sections named.

### C1.114 · RSA 40:10's reconsideration restriction does not reach the March ballot
**Tier 1 · systemic for deliberative sessions · Sources: legal-anchors N54**

¶III: the restriction lasts only "until final adjournment of the meeting at which it is adopted, or any adjourned session of such meeting" — **so it does NOT reach the March ballot.** ¶V applies the section to "school district meetings under RSA 197". A floor citation to "RSA 40:13, IV" for a motion to restrict reconsideration is defensible, because IV incorporates 40:6–40:10, but the operative section is 40:10 — which matters because the 29 January 2024 working session directed a move to restrict reconsideration (A2.1).

*Primary source:* https://gc.nh.gov/rsa/html/III/40/40-10.htm.

### C1.115 · RSA 40:13, VI — the first session cannot keep an article off the ballot
**Tier 1 · systemic · Sources: legal-anchors N55**

"All warrant articles shall be placed on the official ballot for a final vote, including warrant articles as amended by the first session." The first session cannot keep an article off the ballot, and no motion is needed to send one forward. Related clauses recorded with it: **XI(b)** "This amount shall not be amended by the legislative body"; **XV** "Votes taken at the second session shall not be reconsidered"; **IV(c)** "An amendment that changes the dollar amount of an appropriation in a warrant article shall not be deemed to violate this subparagraph."

*Primary source:* https://gc.nh.gov/rsa/html/III/40/40-13.htm.

### C-d. Roster, chronology, attribution and severity corrections

### C1.116 · All three pilot agents silently cleaned up ASR text while quoting it
**Tier 1 · systemic; the convention is now corpus-wide · Sources: html-briefing C1**

The pilot found every agent improving the transcript inside quotation marks — "the single defect most likely to discredit the project". The convention that resolves it: brackets mean insertion or correction with the garbled wording left visible whenever the correction changes sense (`"school boys" [boards]` keeps both); stutters may be condensed unmarked; **a dropped negation is NEVER supplied**, because supplying it invents a vote (B1.2); and quotations from an agenda, minutes or statute must be attributed to that document rather than left reading as speech.

*Primary source:* the pilot's review of all three agents' pages.

### C1.117 · An earlier briefing had the wrong superintendent for 2023
**Tier 1 · systemic — affects every 2023–24 page's roster · Sources: briefing C10 · html-briefing C2, C24 (trap)**

It said Chris Pratt was acting superintendent in 2023. **Michael "Mike" Tempesta was Superintendent of SAU 6 from July 2019 until he was fired 11–12 January 2024**, so any 2023 recording has Tempesta. Pratt was Stevens High School principal through 11 January 2024, became interim superintendent that night, and was made permanent about 22–23 May 2024 effective June 2024 — so never "interim" after May 2024 and never "Superintendent Pratt" before January 2024. The 9/6/23 packet's "Questions for B. Nester" and "Questions for C. Pratt" are **not** a superintendent search. The trap that produced the error survives: on the 4/19/23 recording Pratt says "when I was superintendent there" — of **Bellows Falls**, before Claremont.

*Primary source:* the primary sources as read by the pilot; the 4/19/23 recording.

### C1.118 · The superintendent changeover date was left open and is now settled
**Tier 1 · one-off, closed · Sources: html-briefing C3**

The SAU 6 board voted the evening of **Thursday 11 January 2024** with both motions effective **Friday 12 January 2024** — terminating Tempesta's contract under paragraph nine with six months' severance, and appointing **Christopher Pratt interim superintendent** with contract terms expressly delegated to the chair and counsel for later approval. Roll on each: **10 in favour, Erickson opposed, Popescu abstaining**. Pratt was *appointed* that night, not contracted — the contract thread runs on to A1.34. The statutory authority for the removal is RSA 194-C:5, III (C1.21).

*Primary source:* the 1/11/24 recording (show 15523 at 0:06:15 and 0:08:11), the draft minutes `1hQ4ByhOf5iYiiZbot4XueUVQzVohOoqh`, and the 1/17/24 Claremont agenda masthead six days later.

### C1.119 · "Noelle Kronberg is a 2025 arrival" was wrong by more than a year
**Tier 1 · systemic, corrected · Sources: briefing C11**

She was appointed **SAU 6 board clerk on 11/9/2023** and **Claremont School Board clerk on 11/15/2023**, and reads the roll at every meeting after that. The related line also needed qualifying: the *elected* clerk seat drew no candidate in March 2023, but the board *appointed* a clerk in November — two different things. Before 11/9/23 the roll-reader is Ben Nester, or occasionally Koski, Sprague, Erickson or Tempesta.

*Primary source:* briefing Addendum 5 correcting Addendum 2.

### C1.120 · The 2023 deliberative session was dated 2/10/23; it was 2/8/23
**Tier 1 · one-off · Sources: briefing C12 · html-briefing C11**

Snow date 2/9. The warrant in the 2/1/23 packet, the notice, the agenda, both sets of minutes, MAP.md §2 and briefing Addendum 3 all agree. The amount and tally in that sentence were right. The packet is to be trusted over the addendum here — and the postponement machinery that makes the snow date lawful is RSA 40:4, ¶II (C1.37).

*Primary source:* the warrant in the 2/1/23 packet, corroborated by the agenda, Addendum 3 and MAP.md §2.

### C1.121 · The 2/8/23 moderator was said never to be named; she is Tracy Pope, and the caution was backwards
**Tier 1 · one-off, reversed · Sources: briefing C13**

Briefing Addendum 3 said the moderator is never named and warned against equating her with Pope because Pope "is elected moderator at that election — after this meeting". **Reverse that caution.** Three documents name her presiding: both sets of minutes ("Meeting called to order by Moderator, Tracy Pope"), the packet's Rules of Procedure ("Tracy Pope, Moderator"), and the 11/3/22 special-district minutes in the same packet. She was the **incumbent**, presiding over a session at which her own one-year seat was on the warrant, and was **re-elected** 3/14/23.

*Primary source:* briefing Addendum 10; both sets of 2/8/23 minutes and the packet's Rules of Procedure.

### C1.122 · "Andy" was carried as one unreconciled name; it is two people plus a fifth documentary spelling
**Tier 1 · one-off, closed · Sources: briefing C14**

Briefing Addendum 3 listed `Andy Bernier` (2/8/23) and `Andy LaFrance` (12/1/23) as unreconciled, later joined by `Lafreniere` (11/1/23) and `Andre Lafont` (5/15/24). **The 2/8/23 minutes list "Andy Lafreniere — Ward 3" speaking against the amendment *during debate*, while the recording has the moderator naming Andy Bernier of the NH School Funding Fairness Project *after the meeting closed* — different people, different moments.** And the SRVRTC Vision Committee chair is **Andre LaFreniere**, per the approved 6.20.24 minutes ("Alex Herzog read a statement on behalf of Andre LaFreniere") — the fifth rendering and the first in a district document. Note the collision with the Crawford garble `Andy Crawford` (1.00) at B3.6.

*Primary source:* briefing Addenda 10 and 15; the 2/8/23 minutes and the approved 6.20.24 minutes.

### C1.123 · The Stephanie Hurst citation was misattributed to the wrong speaker and the wrong meeting
**Tier 1 · one-off, corrected · Sources: briefing C15**

Briefing Addendum 3 cited a "4/2/25 Whitney" recollection; **4/2/25 is Sprague**, and "we lost her within a year to… Georgia" is in **12/3/25**, not 4/2/25. The surname is nevertheless solid — six renderings across four meetings and two speakers, best anchored by 4/16/25 Whitney at conf 0.94 in the act of retrieving it, and 12/3/25 at 0.92–0.93; the 1/5/24 hit everyone had been relying on is the **weakest** of the six (`Hurst` at 0.61). Ignore the false positives `Polly Bathurst` (1/17/24) and `Zach Hurst` (2/15/23). Addendum 3's title claim ("SAU 6 Curriculum Director") is separately contradicted by the 2/15/23 minutes ("Literacy Specialist") — see A3.19.

*Primary source:* briefing Addenda 6 and 11.

### C1.124 · Two principals were dated a year and a half too late
**Tier 1 · one-off each, corrected · Sources: briefing C16**

Briefing Addendum 2 said Frank Romeo (CMS) and David Irwin were documented "2024-25 only". **Romeo is CMS principal from at least 2/1/23**; **David Irwin is CMS assistant principal from at least Aug 2023** — he self-IDs 8/16/23 and is on that night's nomination list — and district documents place him earlier still, as CMS **Academic Dean** on the 2021–23 ELA advisory board. Note the ASR hazards: `Frank Miller` (1.00) is Romeo in his own self-introduction, and `Dave Erwin` is Irwin (B3.17).

*Primary source:* briefing Addenda 3, 4, 11.

### C1.125 · "The 7/13/23 SAU 6 chair vote is not audible" — the minutes give it outright
**Tier 1 · one-off, corrected · Sources: briefing C17**

**Hawkins 8, Erickson 3.** Ruggeri nominated Erickson (2nd Gallagher); **Sprague** nominated Hawkins (2nd Simpson). So **Arlene Hawkins is SAU 6 chair from 7/13/23**, not "from 11/9/23 onward" as Addendum 2 had it. Hawkins had been elected SAU 6 **treasurer** on 4/13/23 and vacated that office by becoming chair; **Bonnie Miles** became treasurer 8/17/23. Horsky's 6/21/23 resignation had vacated the chair he won 6–5 on 3/30/23, which is why officers reopened on 7/13. The CSV provenance note that called the tally unrecoverable is corrected at B2.2.

*Primary source:* briefing Addendum 11, corrections part 2; the approved 7/13/23 SAU 6 minutes.

### C1.126 · Addendum 2 overstates the 7/19/23 appointment
**Tier 1 · one-off, corrected · Sources: briefing C18**

It reads "Candace Crawford appointed 4-2 over David Bailey and Kevin Tyson." **Bailey drew no nomination** — the 4–2 was **Crawford v. Tyson only**. (Tyson is this project's maintainer; see D1.1.)

*Primary source:* briefing Addendum 11, corrections part 2.

### C1.127 · Kelly Simpson was placed on the SAU 6 board a year early, and Garry Bator was missing entirely
**Tier 1 · one-off, corrected then re-narrowed · Sources: briefing C19**

Three mastheads — 12/1/22, 1/17/23, 2/16/23 — name exactly five Unity members: **Erickson, Popescu, Bator, Ruggeri, Hart**. So **Simpson was NOT on the board** in that window, and **Garry Bator**, absent from every addendum, was. The hedge "at least through February 2023" is right and its window is the limit: **from 4/13/23 the position reverses** — the 4/13, 5/11 and 7/13 mastheads all name Simpson and none names Bator, and on 5/11 Simpson answers every roll, is named by the chair, seconds the recess motion and is credited by Erickson with raising the conflict-of-interest concern.

*Primary source:* briefing Addendum 11 and its corrections part 2; the mastheads named.

### C1.128 · "The 10/18 minutes wrongly recorded Gallagher present" is FALSE — and a correction built on it must be unwound
**Tier 1 · one-off, consequential · Sources: briefing C20 · briefing A48**

The approved 10/18 minutes read, in terms, `Absent: Jennifer Gallagher`; two agents confirmed it independently against the document. Because the 2026-08-28 re-weighting of `15357`'s Speaker-4 Role note rested on the premise that "Gallagher, not Miles, was the 10/18 absentee" — and Miles was promoted as a candidate on that basis — **the premise is now doubtful and the Speaker-4 cluster must be treated as unresolved**; live candidates are Assistant Superintendent Mike Koski, curriculum director Cat/Kat McLaughlin, and Candace Crawford. The separate `15336` @3680.30 correction is unaffected. The underlying source conflict is carried at A1.39. The `15357` page states its own limit correctly: "Bonnie Miles is treated as neither — she is named in no record and heard in none, and this page makes no claim about her attendance in either direction."

*Primary source:* briefing Addendum 11, "Addendum 5 correction"; the approved 10/18/23 minutes.

### C1.129 · Addendum 4's 10/4/23 subcommittee roster is incomplete and wrong on chairs
**Tier 1 · one-off, corrected · Sources: briefing C21**

The agenda names them: **Capital Improvement chair Bonnie Miles**, **Budget chair Frank Sprague** (not Whitney), Policy chair Skillen, Ad Hoc chair Gallagher — and the addendum **omits the Curriculum Committee entirely**, which Gallagher chairs. Attendance for 10/4/23: **Candace Crawford absent**, the other six present.

*Primary source:* briefing Addendum 11; the 10/4/23 agenda.

### C1.130 · Addendum 7's officer-election seconders are wrong against the district's own minutes
**Tier 1 · one-off, corrected · Sources: briefing C22**

Addendum 7 recorded the vice-chair second as "Whitney", taken from the ASR's ambiguous "A second now." The **approved 3/20/24 minutes** say: chair — "Frank Sprague nominated Heather Whitney, **Arlene Hawkins** seconded"; vice chair — "Candace Crawford nominated Frank Sprague, **Bonnie Miles** seconded". The tape has one unidentifiable word. **Report both; choose neither.**

*Primary source:* briefing Addendum 14; the approved 3/20/24 minutes.

### C1.131 · "Alex Herzog is leaving… no departure is ever stated outright" is wrong
**Tier 1 · one-off, corrected · Sources: briefing C23**

It is stated outright on 6/5/24 at 1:08:44 ("resignation as director of the Tech center") and in the approved 6.5.24 minutes ("recognized Dr. Herzog, his resignation") — seven weeks after he presented a 5–7-year strategic plan and a $10–12M renovation to that board.

*Primary source:* briefing Addendum 15; the 6/5/24 recording at 1:08:44 and the approved minutes.

### C1.132 · The "Present" roll-answer signature was carried forward past its expiry, twice
**Tier 1 · one-off, retired · Sources: briefing C25**

Gallagher was the only member answering "Present" rather than "Here" — until the March 2024 election, after which that answer is Heather Whitney's; two later files record a "Present" answer that is not Gallagher's. Then it dies altogether: on **15 May 2024 three members answer *Present*** (Sprague, Skillen, the chair), Miles answers *Yes*, and Hawkins, Petrin and Crawford answer *here*. **The tell is retired** — an attribution heuristic that outlived its evidence would have put the wrong name on roll answers.

*Primary source:* briefing Addenda 6, 7, 15.

### C1.133 · Addendum 7's "later readings drift" was a CSV artefact, not a drifting record
**Tier 1 · one-off, corrected · Sources: briefing C26 · html-briefing C20, §23c**

The 15 May 2024 recording's "Whitney + Sprague + Crawford" Capital Improvements membership came from a mislabelled first-person sentence that belongs to **Bonnie Miles** (B1.13); the approved 5/15 and 4/17 minutes both give the chair as Miles. The correction reaches the project's own Addendum 14 brief as well as Addendum 7, and the same §23c pass closed Addendum 14 by establishing the Parliamentary Procedure committee's third member as **Michael Petrin** (A2.25).

*Primary source:* html-briefing §23c; briefing Addendum 14.

### C1.134 · Addendum 8's 8/21/24 vote count was wrong
**Tier 1 · one-off, corrected · Sources: briefing C27**

Addendum 8 says "Petrin was the lone No (6–1)" for both motions. **The title/amendment vote was 5–2** — yes: Skillen, Miles, Hawkins, Crawford, Sprague; **no: Petrin *and* Heather Whitney**. Only the **main** motion was 6–1.

*Primary source:* briefing Addendum 16 §1; approved CSB minutes 8.21.24, item IV.4.

### C1.135 · Addendum 8 repeated a transposition of the FY24 encumbrance figures
**Tier 1 · one-off, corrected · Sources: briefing C28**

Exhibit B p.22 gives **total encumbrance $648,931.76**; $648,931.76 − $65,000 = **$583,931.76**, which matches the two roofs voted on 20 June. So **$648,000 is the total and the roofs are the difference** — Henry transposed them on tape and Addendum 8 repeated it. The consequence is material: on the exhibit's own derivation a $65,000 encumbrance leaves a budget balance of about **$1,128,000**, not $544,145.29 — a **~$584,000 ambiguity the board never resolved** (A1.49).

*Primary source:* briefing Addendum 16 §2; Exhibit B p.22.

### C1.136 · Addendum 8's "$400,000 from reserves" for the Stevens roof is unsupported
**Tier 1 · one-off, corrected · Sources: briefing C29 · briefing A13**

The $420,000 was released 6 March 2024 under RSA 198:4-b, II(a), the clerk's read-back confining it to "unintentional, unanticipated special education costs". Mary Henry corrected the roof attribution twice on tape (0:31:43, 0:31:45); a member restated it anyway and the approved minutes adopted his version — so the project inherited the district's error (A1.21).

*Primary source:* briefing Addendum 16 §3.

### C1.137 · Addendum 8's ESSER account was wrong in two directions
**Tier 1 · one-off each, corrected · Sources: briefing C30**

First closure: the 16 October approved minutes record only "Frank Sprague shared that he would still like to see a presentation on ESSER"; the 2 October minutes contain no finance report and no ESSER mention; **ESSER is never mentioned at the 4 September meeting at all**, in any garble form; and on 18 September Pratt says "we have the end of September to spend the money" — **the wrong verb**, since 30 September was the *obligation* deadline and liquidation ran to 28 January 2025 (see the 2 CFR 200.344 paragraph move at C1.61). Then the counter-correction: **16 October is NOT the corpus's last ESSER mention** — it is spoken at 16155, 16157, 16213, 16215, 16222, 16226, 16253 and 16266, always retrospectively. What ends on 16 October is the board *asking* for an accounting, and no later recording contains one. Addendum 16 §4 must be amended because ESSER *is* mentioned on 2 October at 0:09:13 (A1.43).

*Primary source:* briefing Addenda 16 §4 and 17.

### C1.138 · Addendum 8 read the wrong column for the Whitney cluster boundaries
**Tier 1 · one-off, corrected · Sources: briefing C31**

The quoted values were **End(sec)**, not Start; the Start-column values are **2578.44 / 2770.80**. The practical consequence is a live attribution conflict: the ADC motion at 2681 s falls inside that gap, so the CSV labels it Arlene Hawkins while the minutes credit Heather Whitney (B1.7).

*Primary source:* briefing Addendum 16 §5; the 9/12/24 dialogue CSV.

### C1.139 · Addendum 8's joint-meeting caution is overturned — the names were recoverable after all
**Tier 1 · one-off, overturned · Sources: briefing C32**

Addendum 8 held that only Girard, Manale and "Limoges/Lemos" were defensibly nameable, that the chair's attendance list "is not parseable into clean names", and that treating it as an attendance record "would manufacture people". The approved minutes (Drive `1aY0leNEDzk_VGJLu9WsMoCideg5x4zhB`) name eight: **Mayor Dale Girard, Asst. Mayor Deb Matteau, Brian Zutter, Jonathan Hayden, William Greenrose, Wayne Hemingway, William Limoges, City Manager Yoshi Manale** — and the chair's garbled list names exactly those eight and nobody else: `Gerard`=Girard, `Deborah McGill`=Matteau, `Brian Sutter`=Zutter, `Mr. William green. Rose.`=Greenrose (the surname split in two, which is what made the list look unparseable), `Yoshi Marnell`=Manale. **It manufactures nobody.** The minutes' per-question attributions then match the diarizer's clusters nine times over: the 18-row cluster is Zutter, the 11-row clusters Greenrose and Hemingway, each at three separate points; the 6-row closing cluster is Matteau on the minutes' ordering alone — the weaker call.

*Primary source:* briefing Addendum 17; the approved joint-meeting minutes, Drive `1aY0leNEDzk_VGJLu9WsMoCideg5x4zhB`.

### C1.140 · "Pratt read all four rolls on 11/14" — he read three
**Tier 1 · one-off, corrected · Sources: briefing C33**

Attendance 0:00:43, into nonpublic 0:04:41, out 0:06:07. **The fourth roll of that evening was Kronberg's, at the separate Claremont meeting later the same night**, where she was present, read the roll and both roll-call votes, and signed the minutes (A1.4, A2.1).

*Primary source:* briefing Addendum 17; the 11/14/24 SAU 6 recording and the Claremont draft minutes.

### C1.141 · Addendum 9's SAU 6 "no tally" claim needs qualifying
**Tier 1 · one-off, qualified · Sources: briefing C34**

The 11/14 **minutes** record a named dissent — "all present voting in favor with the exception of **Kelly Simpson** who opposed" — four weeks before the 12/12 counted dissent. **The recordings carry no tally; the minutes do.**

*Primary source:* briefing Addendum 17; the 11/14/24 SAU 6 minutes.

### C1.142 · Deborah vs Danielle Skinner — the "do not merge" instruction was right
**Tier 1 · one-off, confirmed · Sources: briefing C38**

Addendum 4 flagged that Koski's 8/16/23 nomination list reads "**Deborah Skinner**, art, Stevens High School" while the 6/21 and 7/19 "Miss Skinner / D Skinner" is *support* staff doing food service, free-and-reduced lunch and PowerSchool, and forbade merging them on the surname. District documents confirm two people: **Danielle Skinner** = Data Manager / Food Service / PowerSchool, SAU 6, distinct from **Deborah Skinner**, art teacher at Stevens.

*Primary source:* briefing Addenda 4 and 11; the district documents named.

### C1.143 · The Stevens principal changeover was dated repeatedly and each dating was wrong
**Tier 1 · systemic, narrowed · Sources: briefing C39**

Addendum 2 left it open; Addendum 6 narrowed it to after 1/17/24 (Pratt still reports "as being the principal at the high school"); Addendum 7 put the window at 1/17/24 → 3/6/24 and had Herrington unambiguously in post by 6/20/24. **All of that is superseded by district documents:** Michael Herrington was **Stevens ASSISTANT principal in the 2023-24 handbook** alongside Paige Jarvis; the 2/21 Exhibit 4 is written by "the new interim principal", unsigned, speaking of "continuity between Chris and myself", with reports due 8 Feb and the packet posted 14 Feb — so the change had happened by **mid-February 2024, not by 6 March**; and Exhibit F (DMG deck, posted 4 June 2024) names him **High School Principal**, earlier than Addendum 7's 6/20 dating. **The interim principal is still named nowhere.**

*Primary source:* briefing Addenda 2, 6, 7, 11, 14, 15; the 2023-24 handbook and the 2/21 Exhibit 4.

### C1.144 · Pratt's permanent appointment was carried as "unwitnessed"; it is now dated and witnessed
**Tier 1 · one-off, closed · Sources: briefing C40**

Addendum 7 recorded it as "~22–23 May 2024, unwitnessed". Three confirmations landed: 8/21/24 (15947) two members speaking to his face — Petrin, "Chris was the acting superintendent because someone left mid-term"; Miles, "Mr. Pratt was an interim superintendent **before you became** the superintendent" — and 9/12/24 (16011) Hawkins announcing "the appointment of Superintendent Christopher Pratt… which was **effective in June**." District documents bracket it: the 5/15/24 masthead reads "**Interim** Superintendent", the 6/5/24 agenda and approved minutes read "Superintendent". **Settled: announced ~22–23 May 2024, effective June 2024, formally recognised 9/12/24** — with the caveat that the **Claremont board does not appoint the superintendent** (RSA 194-C:5), so the 11 May retreat note "Hired a great superintendent" is loose usage, not a record of appointment. 22 May 2024 is the meeting whose minutes exist but whose video, packet and MAP section do not (A2.1).

*Primary source:* briefing Addenda 7, 8, 15; shows 15947 and 16011.

### C1.145 · "No student rep exists yet" and "Bonnie Miles is elimination-only" were both over-generalised
**Tier 1 · systemic, qualified · Sources: briefing C41**

Addendum 4's "no student rep exists yet for 2023-24" was true **only as of 9/6**: Nicole Bouchard and Kylee Plummer were seated **11/1/2023**. And "Miles is an elimination-only call in almost every 2023 meeting" holds in some files and not others — she is named outright on 8/9 (three ways), 8/16, 9/20, 3/6, 4/17, 6/5 and 6/20, and remains elimination-only in 2/21, 4/11 SAU and 5/15. **Check per meeting; never inherit** — and three separate agents reached her the same way and all flagged it, so "do not let repetition harden into confidence."

*Primary source:* briefing Addenda 3, 4, 5, 7.

### C1.146 · Era 0's vacant seat — an inference upgraded to a document
**Tier 1 · one-off, closed · Sources: briefing C43**

Addendum 10 treated **Joshua Lambert** as "a strong inference, not a fact" — the 11/3/22 minutes list him sitting; on 2/8/23 he seconds the amendment from the audience. Addendum 11 closes it documentarily: the 12/1/22 SAU 6 minutes list twelve members including him; 1/17/23 and 2/16/23 list eleven, **with Lambert the only name removed**.

*Primary source:* briefing Addenda 10 and 11; the 12/1/22, 1/17/23 and 2/16/23 SAU 6 mastheads.

### C1.147 · Mary Henry's appointment date was carried as her start date
**Tier 1 · one-off, corrected · Sources: briefing C44**

Addendum 2's "starting early July 2023" is her **start** date. She was **appointed business administrator on 11 May 2023**, on Tempesta's nomination.

*Primary source:* briefing Addendum 11, corrections part 2.

### C1.148 · Sprague's SAU 6 vice-chairship was carried past its end
**Tier 1 · one-off, corrected · Sources: briefing C45**

**Frank Sprague was SAU 6 Vice Chair** before Ruggeri — recorded in no earlier addendum — and **his SAU 6 vice-chairship ends 3/30/23**. From that date the SAU 6 vice chair is **Rocco Ruggeri**, and Sprague's "vice chair" title thereafter is the **Claremont** board's. Do not carry the SAU role past March 2023. Note that vice chair is not one of RSA 194-C:5, I's three statutory offices (A1.29).

*Primary source:* briefing Addendum 11, corrections part 2.

### C1.149 · Two claims about the SAU 6 chair in early 2023 were wrong in opposite directions
**Tier 1 · one-off, corrected · Sources: briefing C46**

Addendum 2 put Hawkins in the SAU chair from 11/9/23. **The SAU 6 chair in Feb 2023 is Marjorie Erickson (Unity)**, established four ways at the 2/16/23 meeting — cleanest being a roll-call residual where she reads the roll naming every member except herself and answers "Me? Yes." Horsky then beats her **6–5 on 3/30/23 by PAPER BALLOT**, so individual votes are not on the record, with Ruggeri elected vice chair by unanimous voice vote the same night. **Do not put Hawkins in the SAU chair before late 2023** — and per C1.125, from 7/13/23 she is.

*Primary source:* briefing Addendum 3; the 2/16/23 and 3/30/23 SAU 6 records.

### C1.150 · The Unity withdrawal planning committee was recorded with the wrong size, and a chair that was never named
**Tier 1 · one-off, corrected · Sources: briefing C47**

The project note carried a **seven-member** committee. Ruggeri, 4/11/2024: the Unity town vote of "March 16th" approved creating it, and it is **5 town members + 2 board members + the superintendent = EIGHT**. **No chair is named on the recording** — Ruggeri delivers the report but never says he chairs it — and the briefing later confirms **no planning-committee chair has ever been named, in any file, in the whole corpus**.

*Primary source:* briefing Addenda 7 and 9; the 4/11/2024 recording.

### C1.151 · SAU 6 does not dissolve on 1 July 2026 — the run's biggest factual correction
**Tier 1 · systemic, corrected · Sources: briefing C48 · html-briefing C25 · html-briefing A46**

§28 and several shipped pages recorded the dissolution as settled background because two officials said so at the 18 February 2026 meeting. **They were wrong, and the SAU 6 chair corrects them on tape** — show 17307 at 0:35:20, Whitney: "the saw is dissolving"; Ruggeri: *"It's not. It's not dissolving. Just to clarify."* and *"It would just be the Claremont board at that point, but it would still be the same. Six."* The 15 April 2026 approved Claremont minutes agree. **What ends is UNITY'S MEMBERSHIP under RSA 194-C:2, IV; the unit continues with one district.** Ruggeri himself uses the loose word twice before correcting it, which is how the error propagated. But do not over-correct: the district's own staff report of 27 March 2026 (Drive `16M5jaunMtgwaVWRIi_iojNp2FgqMcl1W`) says SAU 6 "will dissolve as a legal separate entity", so the record genuinely contains both characterisations and a page quoting either is quoting accurately (A1.58). The business administrator's own words support only that "Saw six employees get merged to the school district."

*Primary source:* show 17307 at 0:35:20; the 15 April 2026 approved Claremont minutes; the 27 March 2026 staff report.

### C1.152 · The corpus graded the identical missing-record fact both HIGH and MEDIUM
**Tier 1 · systemic, resolved by rule · Sources: briefing C56 · html-briefing C18, §22h · map+pages Part 2 §4**

The user's ruling now governs: **HIGH** where the absence is unmitigated — a public body met, no minutes exist in any district share, nothing on the record explaining it (RSA 91-A:2, II sets five business days; RSA 91-A:1-a, VI(d) makes a subcommittee a public body, C1.10); **MEDIUM** where the record mitigates it — someone on tape says minutes exist elsewhere or are coming, the body lacked a quorum and transacted nothing, or the meeting was noticed and packeted with only the minutes missing. Each page must say which limb it applies and why; **a page with no HIGH flag is a valid outcome** and one must not be manufactured; and where severity diverges from a neighbouring page on similar facts the divergence must be stated, as the 2/21/24 page did against the 17 January page. The resulting distribution across the 126 pages — 1,614 flags, mapped to years by the date in each page's `<h1>`, counting `flag-high`, `flag-med`, `flag-obs`, `flag-pos`, the only flag classes in the corpus:

| Year | Pages | HIGH | MEDIUM | OBSERVATION | POSITIVE | Total |
|---|---|---|---|---|---|---|
| 2023 | 35 | 58 | 189 | 158 | 122 | 527 |
| 2024 | 30 | 68 | 209 | 164 | 100 | 541 |
| 2025 | 38 | 24 | 76 | 129 | 80 | 309 |
| 2026 | 23 | 25 | 81 | 90 | 41 | 237 |
| **All** | **126** | **175** | **555** | **541** | **343** | **1,614** |

Per-page averages: 2023 = 15.1 flags/page (1.7 HIGH); 2024 = 18.0 (2.3 HIGH); 2025 = 8.1 (0.6 HIGH); 2026 = 10.3 (1.1 HIGH).

*Primary source:* the corpus's own inconsistent grading, resolved by the user's decision; the flag-class scan of the 126 pages.

### C1.153 · Two 2023–24 claims about who could read the roll were over-general
**Tier 1 · one-off each, corrected · Sources: briefing C58**

"The clerk reads the roll" is wrong as a general rule: **Hawkins reads the rolls herself on 12/14/23 and on two of the four rolls on 1/11/24**; when the chair says "the secretary take a roll call," it is Kronberg, otherwise check. And a roll-reader **no addendum records** turns up in a document: the 1/11/24 minutes read "roll call vote taken by **Mike Koski**." Kronberg's 2024 attendance had to be established file by file — 8/21 absent (chair read it), 9/4 present, 9/12 present, 9/18 absent (**Crawford** read it), 10/16 present, **11/14 absent (Pratt)**, 11/20 present, 12/4 present, 12/12 present, **12/18 absent (Mary Henry read it)** — **four distinct substitute readers in five months**.

*Primary source:* briefing Addenda 6, 8, 9, 13; the 1/11/24 minutes.

### C1.154 · §22e's "the paperwork is right from April 2024" clearance was too broad
**Tier 1 · systemic — a scoping error relied on by later pages · Sources: html-briefing C19**

The clearance covers **SAU 6 only, and nonpublic-session citations only**. Claremont has its own ongoing version of the citation problem — the by-laws' Appendix D and the 7 August 2024 minutes (A1.2, A1.3) — and SAU 6's own 12 September 2024 policies cite the wrong statutes twice (A1.5, A1.6). The corrected instruction is to check every SAU 6 page **through February 2024**, and to check both bodies separately rather than reading one body's clearance across.

*Primary source:* html-briefing §22e's own re-scoping of the earlier clearance.

### C1.155 · MAP §20 called the 9/6/23 interviewees "superintendent candidates"; there was no search
**Tier 1 · one-off, corrected 2026-08-29 · Sources: map+pages §4.15**

"An earlier version of this note called them 'superintendent candidates'. They were not — there was no search." Consistent with C1.117: the 9/6/23 packet's "Questions for B. Nester" and "Questions for C. Pratt" are not a superintendent search, and Tempesta was superintendent until January 2024.

*Primary source:* MAP.md §20 correction, 2026-08-29.

---

## C · Tier 2 — affects what a reader can find or verify

### C2.1 · "No draft minutes exist for 12/3/24 or 12/12/24" was right about publication and wrong about existence
**Tier 2 · one-off, corrected · Sources: briefing C35**

The **10 April 2025 draft SAU 6 minutes** (Drive `1KcmceeO49Fd392oO_RBk86who2DyTLkT`, in `6. SAU6 6.12.25`) record: "Heather Whitney made a motion to approve the minutes from 12.12.24 as presented, Michael Petrin seconded the motion", voice vote, all in favour. Written, circulated and approved **119 days** after the meeting; never published. The distinction between "not published" and "does not exist" is the whole point of the finding (A2.1, A2.2).

*Primary source:* briefing Addendum 18; the 10 April 2025 draft SAU 6 minutes.

### C2.2 · The 41–27 amendment tally was said to be absent from the recording; it is absent from the transcript
**Tier 2 · one-off, restated · Sources: briefing C42**

Briefing Addendum 3 recorded that about 22 minutes of balloting came through as untranscribed crosstalk and "the announcement never appears", concluding the recording supports only that the amendment went to a secret ballot. Addendum 10 restates it precisely: **the dialogue CSV has no rows between 1:35:11 and 1:43:19, and whether the announcement is audible on the recording was never tested.** Say "not in the transcript", not "not on the recording."

*Primary source:* briefing Addenda 3 and 10; the 2/8/23 dialogue CSV.

### C2.3 · The continuity diagnostic built on Cablecast `eventDate` is wrong as written
**Tier 2 · one-off, corrected twice · Sources: briefing C50 · html-briefing C22**

§27a offered "a precise `eventDate` plus a creation stamp a minute after it" as evidence of when recording began. §28a corrects it: **show numbers follow record-creation order, not event order**, and a `created` stamp preceding the event date is a hand-entered, pre-scheduled record that says nothing about recording. §29b adds a third case: three shows whose `eventDate` misdates the meeting outright. The diagnostic holds only for the other kind of record — show 17126 is a textbook case and show 16226 is the one that settled the ordering of the two 18 December 2024 meetings. The underlying source-system facts are recorded at A3.27 and A3.28.

*Primary source:* html-briefing §27a, §28a, §29b; the Cablecast API records named.

### C2.4 · §24e was too pessimistic about settling a splice
**Tier 2 · one-off, corrected · Sources: briefing C51 · html-briefing C21**

It concluded "the video does not decide it". Pixels do not, but **a spoken clock time can** (show 16157) and **arithmetic is better still** (show 17323 — run time plus minuted nonpublic duration). Before giving up on a zero-gap question, grep the CSV for spoken times and for spoken countdowns: "45 minutes left in this session", "we have a half hour left", "we got ten minutes for the calendar" — three on one file, projecting ends of 2:50 / 2:47 / 2:46 p.m. against an actual 2:47 from the event stamp. See B2.3.

*Primary source:* html-briefing §24e, §26a, §27a, §29c.

### C2.5 · §18's Drive-metadata guidance was wrong about what `createdTime` measures, and has been refined four times
**Tier 2 · systemic, refined · Sources: briefing C53 · html-briefing D6, D7, D8, D9**

§18 treated `createdTime` as dating the posting of a packet or minutes and therefore as a test of timeliness. §22c corrects it: Claremont minutes reach the public share only when the next meeting's packet folder is created, within seconds of it (A2.11), **so `createdTime` is evidence of when the public could see a document, not of when it was written**. `modifiedTime` proves earlier existence only when the gap is measured in **days** — in several packets every file carries a `modifiedTime` a few seconds *before* its own folder, an upload artefact that proves nothing, and the same artefact recurs at 60–70 seconds in the FY25 sequence; where the gap is days it does work, as with the 2/21 draft whose `modifiedTime` (28 February) puts it inside the five-day window while its `createdTime` falls outside. §24c refines again: **for the FY25 sequence use the FILE `createdTime`, not the folder's** — `2. CSB 8.21.24` was created 2024-07-25, a month ahead, while all eight of its files were uploaded 2024-08-19. §29h refines a fourth time: **for the 2026 Claremont minutes `createdTime` dates the CALL TO ORDER**, because the clerk drafts live — the 3.4.26 minutes created 6:30 p.m. on 3 March, the 3.18.26 minutes at 6:30 p.m. on 18 March — so it cannot test the five-day rule for those but is an excellent anchor for an unstated start time. Findings must say which field they rest on.

*Primary source:* html-briefing §18, §22c, §24c, §29h; the folder and file `createdTime` values named.

### C2.6 · §18's advice on reading board policies is superseded
**Tier 2 · one-off, superseded · Sources: briefing C54 · html-briefing D15, D16**

§18 sent agents to `WebFetch`. **`WebFetch` on a `docs.google.com/document/d/…` URL returns only the JavaScript shell.** `mcp__Google_Drive__read_file_content` on the document ID returns the full text including the District Policy History block — strictly better. And for contracts and multi-column PDFs the Drive MCP itself scrambles the text, so the route is `download_file_content` → base64 decode → **`pdftotext -layout`** in the cloud container (D2.6).

*Primary source:* html-briefing §18, §25a, §25b; the two tools' outputs on the same document ID.

### C2.7 · "Policy Committee" minutes in Drive were nearly used as the board's
**Tier 2 · one-off, trap avoided · Sources: briefing C57 · html-briefing D23**

They are the **CITY of Claremont's** Policy Committee — cemeteries, DPW, mobile food units — and a title search surfaces them. Using them as school-board subcommittee minutes "would be a serious misattribution." Related and separately disclosed: the only policy-subcommittee minutes the project can locate anywhere in Drive are from 2022 and 2023 and are owned by the project's maintainer (D1.1).

*Primary source:* the documents' own subject matter.

### C2.8 · Internal inconsistency — two Federal Register citations for the 2024 Uniform Guidance revision
**Tier 2 · one-off, unresolved · Sources: legal-anchors C46**

Line 1080 of the catalogue gives the revision as **89 FR 30046** with URL `https://www.federalregister.gov/documents/2024/04/22/2024-07496/`; line 1457 gives **89 FR 30136, Apr. 22, 2024** for the same revision's effect on 2 CFR 200.313. Both are dated 22 April 2024 and both are stated as effective 1 October 2024. One page number is wrong and the file does not say which; a page citing the wrong starting page gives a Federal Register cite that will not resolve to the document. Observed in the file, not flagged there.

*Primary source:* the catalogue's own two entries.

### C2.9 · Internal inconsistency — 89 FR 33885 vs 89 FR 33888 for the 2024 Title IX rule
**Tier 2 · one-off, unresolved · Sources: legal-anchors C47**

Line 115 gives the 2024 Title IX rule as **89 FR 33885**; line 1388 gives **89 FR 33888** in the amendment history of 34 CFR 106.41(c). The second is plausibly the page for the amended section rather than the rule's first page, but the file does not reconcile them. Observed in the file, not flagged there.

*Primary source:* the catalogue's own two entries.

---

## C · Tier 3 — affects precision, not conclusions

### C3.1 · §17c understated the quote-checker limitation
**Tier 3 · one-off, corrected · Sources: briefing C52 · html-briefing D2 · legal-anchors D4**

§17c said to set single-token transcript items in `<em>`. §22b widens it: **never put fewer than 8 characters inside typographic quotes anywhere on a page** — a quoted name (`"Chris"`, `"Whitney"`) or a single quoted word in the project's own prose shifts the open/close pairing for the rest of the block and manufactures phantom REVIEW lines built out of the page's own sentences. **Twelve phantoms on one page.** Use `<em>` instead, every time, and say so in the method footer.

*Primary source:* html-briefing §17c, §22b; the checker's regex `"([^"]{8,600})"`.

### C3.2 · A cluster of project name errors corrected by district documents
**Tier 3 · systemic, corrected · Sources: briefing C37 · html-briefing §15h**

**Kristina Sanford**, not Christina, and her title is **Early Childhood Director**, not preschool/early-childhood coordinator (2/15/23 minutes and the superintendent's own report; the recording says only "Christina") · **Shaun Laplante**, not Sean/Shawn (his own grant proposal, signature block, `slaplante@sau6.org`) · **Susan Cantara**, not Sue Kantara · **Crystal Simonds**, not Simmons · **Megan Fagans**, not Fagan · **Amalia → Amelia Rhines** (agenda and both sets of minutes) · **Aubree Herzog**, not Aubrey · **Gage Morin**, not Moran · **Polly Bath**, not Bathurst (the board's own deck reads "Polly Bath Classroom Mgmt", and a page carrying "Bathurst" is wrong) · **Kylee Plummer**, not Kylie · **Jill Chastenay**, not "Ms. Chastain" (her own signed 2/21/24 Exhibit A letter, the agenda and the approved minutes) · **Lilly Clark** in every district document from 2 Oct 2024, against her own spoken *Lily* · **Sharon Mezzack** for the SAU 6 business-office "Sharon" · **Steve Holt = Maintenance Director**, not "Stevens/district facilities".

*Primary source:* briefing Addenda 11, 13, 14, 15, 17; html-briefing §15h; the district documents named.

### C3.3 · The Cat/Catlin resolution was claimed twice and withdrawn twice
**Tier 3 · systemic, unresolved · Sources: briefing C36**

Addendum 13 said "the minutes spell her Cat; Addendum 11's 'Catlin Cat' is not the district's spelling" — **Addendum 14 says Addendum 13 overstated it** (the 2/21/24 SAU 6 Office Monthly Report spells it Catlin). Addendum 15 then narrowed toward **Catlin** on three district documents to one — and **Addendum 16 sent it back to unresolved** when a fourth spelling with a title turned up (`Kat McLaughlin, Curriculum Director`, 19 Aug 2024), followed by a fifth (`Katlyn`, spoken) and a sixth data point (one Superintendent's Report page printing both Cat and Catlin). **Still not settled** — disagreement 5 of the five carried at the foot of this file. The district-side facts are at A3.11.

*Primary source:* briefing Addenda 13, 14, 15, 16, 17, 19.

### C3.4 · Addendum 7 was wrong that `Mr. governor` and `Charlie` "name nobody recoverable"
**Tier 3 · one-off, corrected · Sources: briefing C24**

The approved 6.20.24 minutes name that voice **Charles Gessner**. Two more from the same class were later recovered: **`micros` = Mikros** (listed as unrecoverable in Addendum 8) and **`My dad Mattos` = Matteau**, where the CSV Role field still reads "THE NAME IS NOT RECOVERABLE" — a stale note in shipped data.

*Primary source:* briefing Addenda 15 and 17; the approved 6.20.24 minutes.

### C3.5 · "Vinduska" was printed as fact on five project pages
**Tier 3 · one-off · Sources: html-briefing A44, §15h · briefing A69**

The spelling is printed as fact on `14937`, `16409`, `16776`, `16951` and `17046`, against a standing instruction to describe the role and attribute any spelling to its document. The Byrne Foundation letter and the approved 18 February 2026 minutes both support Vinduska, but the briefing file's own resolution of `15483` Speaker 10 is **Rebecca Duska** and the two are unreconciled (A3.13).

*Primary source:* the five pages named; html-briefing §15h and §28f.

---

# CLASS D — METHOD LIMITATIONS

What the tooling, the environment and the available sources cannot do, and the standing rules that follow.

## D · Tier 1 — affects what a reader can conclude

### D1.1 · A maintainer conflict of interest that must be disclosed, not managed away
**Tier 1 · systemic, standing rule · Sources: briefing D23 · html-briefing §8, §23h · map+pages Part 2 §3**

**Kevin Tyson maintains this project**, and the 6/5/24 packet (Exhibit D, the CCTV roster — itself a privacy exposure, A1.61) names him as the holder of **Seat 3 on the CCTV Board of Directors**, a City Council appointment running **13 July 2022 – 31 May 2025** — CCTV being the source of every recording in this corpus. He also appears in the record as a candidate for the seat Crawford took on 7/19/23 (C1.126) and as one of the two options offered at the 11/5/25 meeting. Wherever the maintainer, CCTV's board or CCTV's own interests appear in a document a page relies on, disclose it plainly in the footer; where he does not appear, the footers say so explicitly. Do not omit the item and do not soften it. Ninety-six of the 126 pages carry some form of "Kevin Tyson maintains this project"; **16 additionally disclose the CCTV seat**:

| Page | Disclosure |
|---|---|
| `15786 SchoolBoard060524` | "the City of Claremont's roster of the CCTV Board of Directors, filed in this packet as part of Exhibit D, lists him as the holder of **Seat 3**, a City Council appointment made **13 July 2022** and running to **31 May 2025**" |
| `15947 SchoolBoard082124` | "…which covers the date of this meeting" — the meeting arranged for CCTV to televise four Finance Subcommittee budget meetings |
| `15994 SchoolBoard090424` | "He held Seat 3… and CCTV is the source of this and every other recording in this corpus" |
| `16021 SchoolBoard091824` | "…and so on the date of this meeting; CCTV produced the recording this page is built on… and the decision recorded at flag 22 to televise the autumn budget sessions concerns CCTV's channel" |
| `16046 SchoolBoardCityCouncilJoint093024` | "…and so on the date of this meeting; that seat is a City Council appointment" |
| `16049 SchoolBoard100224` | "…CCTV produced the recording this page is built on, and the agenda and minutes carry the district's standing CCTV broadcast note" |
| `16070 SchoolBoard101624` | "…and so on the date of this meeting" |
| `16157 SchoolBoard112024` | "…and so on the date of this meeting" |
| `16192 SchoolBoard120424` | "…and so on the date of this meeting" |
| `16215 SchoolBoardFinance121324` | "he held Seat 3 on the board of directors of Claremont Community Television, which produced this recording… and that appointment therefore overlaps the date of this meeting" |
| `16222 SchoolBoard121824` | "…and so on the date of this meeting" |
| `16226 SchoolBoardFinance121824` | "…and therefore on the date of this meeting" |
| `16958 SchoolBoardVacancy110525` | "The recordings themselves come from Claremont Community TV, on whose board of directors he held a City Council appointment to Seat 3 from July 13, 2022 to May 31, 2025" |
| `17125 SchoolBoardDeliberative020726` | "Every recording this project works from is produced by Claremont Community Television, whose executive director the moderator thanked at 0:05:48…" — compounded: "**Maintainer disclosure: the project's maintainer moved both amendments that carried, and the recording is CCTV's**" |
| `17241 SchoolBoard031826` | "…has served on the board of Claremont Community Television, whose operations are the subject of the exchange quoted above; CCTV is the source of every recording in this corpus" (a second instance ties it to flag 4) |
| `17348 SchoolBoard050626` | "the board reappointed a member of the CCTV Board of Directors, the body on which he held a seat until 2025, and CCTV is the source of every recording in this corpus" |

Related non-CCTV maintainer disclosures: `14937 SchoolBoard030123` — "Frank Sprague names him at 0:49:01 as the interviewer of the school board candidates on CCTV, calling him 'a much better interviewer than I was'"; `15205 SchoolBoard071923` — "was one of the three applicants for the seat filled at this meeting"; `16433 SchoolBoard-040225` — "spoke during citizens' comments at this meeting and is a named speaker in the source dialogue file"; `16463 SAU6Mtg-041025` — spoke at the 4/2/25 CSB meeting covered by the companion page; `16813 SchoolBoard090325` — "spoke during the public hearing and later applied for the board seat announced at this meeting"; `16831 School Board 091025` and `16857 SchoolBoard091725` — named as one of five applicants; `16872 SchoolBoard100125` — "one of the two candidates who received votes at this meeting… nothing on this page was reviewed or altered by him before generation"; `17125 SchoolBoardDeliberative020726` — "Voter, Ward 2… Moved both of the amendments that carried"; `17201 SchoolBoard030426` — "the only policy-subcommittee minutes this project can locate anywhere in Drive are from 2022 and 2023 and are owned by Kevin Tyson"; `15510 SchoolBoardFinance010524` — "the only Finance Committee minutes the index holds at all are two 2026 files owned by this project's maintainer, not by the district".

*Primary source:* the 6/5/24 packet Exhibit D (CCTV roster); the 16 pages named and the related disclosures.

### D1.2 · Unquoted heredocs silently corrupted money on generated pages
**Tier 1 · one-off incident, standing hazard on every heredoc-built page · Sources: briefing D8 · html-briefing D1**

`cat >> page.html <<EOF` makes bash expand `$688` as a variable, so **`$688,426.17` lands on the page as `88,426.17`**, `$36,313,407.97` as `6,313,407.97`, and `$196,001.10` as `96,001.10`. **One agent corrupted six of ten page chunks this way**, and on a budget page that is a page full of wrong money with nothing visibly broken. It was caught only because `verify_quotes.py` failed the quotations containing amounts — the quoted spans no longer matched the dialogue CSV. The fix: always write `<<'EOF'`, never `<<EOF`; if the page needs a shell variable, write the literal text and substitute afterwards with python.

*Primary source:* `verify_quotes.py` failing the quotations that contained amounts.

### D1.3 · Reformatted scratch dumps silently drop text, producing fabricated quotations
**Tier 1 · one-off incident, systemic hazard · Sources: briefing D6 · html-briefing D13**

A re-wrapped dump dropped a three-word repeat out of the middle of a quotation — "There's there is over 60 parents" for "There's there is **that there is** over 60 parents" — and it reads as clean text. It is a fabricated quotation. **Copy long quotations from the CSV field itself, not from a reformatted dump**, and run the checker before believing your own transcription.

*Primary source:* the re-wrapped scratch dump compared against the CSV field.

### D1.4 · Shared `/tmp` scratch names let one agent read another meeting's dialogue as its own
**Tier 1 · one-off incident, rule imposed · Sources: briefing D7 · html-briefing D12**

During wave 1 an agent's condensed dialogue at `/tmp/cond.txt` was overwritten by a sibling working on a different meeting; it read **about 230 lines of the wrong meeting believing they were its own** and began drafting a treasurer election and a procurement discussion **that never happened at its meeting**. It caught the swap only on a length mismatch. Rule: write every scratch file to a path containing the meeting's base name, e.g. `/tmp/gtp-<BASE>/cond.txt`, and **treat any `/tmp` file you did not just create as untrusted**.

*Primary source:* the wave-1 incident, caught on a length mismatch.

### D1.5 · Standing prohibitions against importing a name the file does not speak
**Tier 1 · systemic · Sources: briefing D20**

**The auditor is only ever "Mike"** on many recordings — the corpus canon is Michael Campo / Plodzik & Sanderson, and the briefing forbids importing the surname or the firm into files that do not speak them (B3.21). **Michael McCosker is nearly absent from the 2024 board record** — named nowhere in 15947, 15814, 15994, 16011 or 16021 — so do not assume he attends Claremont board meetings in 2024 and do not attribute unnamed administrator voices to him by default. **A "Crawford" voice before 7/19/23 is not a board member**, and **a "Petrin" voice between mid-March 2023 and March 2024 is not a board member** — both are errors the 2025 roster would invite if applied backwards. And **"Heather" in charter-school context is Heather Shepherd, not the chair**.

*Primary source:* briefing Addenda 2, 4, 8.

### D1.6 · Excerpt timestamps must never be converted to wall-clock time
**Tier 1 · systemic · Sources: briefing D21 · html-briefing §28b**

Stated as a hard rule alongside the excerpt pair at B1.17: if a recording opens mid-business, has no roll call, or ends mid-sentence, **look for a sibling show on the same date before concluding the meeting itself was odd** — and never compute a wall-clock time from an excerpt's timestamps. The same prohibition applies after any established splice, where recording positions stop being clock times (A2.31, C1.48).

*Primary source:* briefing Addendum 1.

### D1.7 · Statute-vintage traps: current text does not govern most of this corpus
**Tier 1 · systemic — the standing rule behind 40-plus individual traps · Sources: briefing D12 · html-briefing C4–C8 · legal-anchors, VINTAGE TRAPS header**

Before citing any provision whose dollar amount, percentage, deadline or numbering carries the flag, check what it said on the meeting's date. **Roughly half this backlog predates the 2025 and 2026 session laws**, and the catalogue's holdings "need an 'in force from' column before the remaining 78 pages are built." The individual traps are recorded at C1.8, C1.11–C1.13, C1.26–C1.28, C1.40, C1.52 and C1.53–C1.93; the durable provisions that need no caveat are at C1.113. For any 2023–24 Uniform Guidance or title-34 citation use the govinfo annual edition, never the current eCFR (D2.15).

*Primary source:* html-briefing §4, §9, §12, §16; briefing Addenda 10 and 11; the legal-anchors vintage tables.

### D1.8 · Surname collisions the sweep flagged and deliberately left unmerged — for a human, not an agent
**Tier 1 · systemic · Sources: briefing D13**

**`Cassandra Edwards` (39 rows / 5 files) vs `Sandra Edwards` (11 / 1)** — same ward (3), same profession, never co-occur, **probably one person**; a merge is recommended but needs a document, and the 17092 Role already hedges "as announced; not on public roster". **`Michael Myers` (1/7/26, Ward 3) vs `Mike Myers` (2/7/26, Ward 3, also an assistant moderator)** — almost certainly one man a month apart, but **both are self-identifications**, and overriding what someone called himself needs better grounds. **`Hilary Walsh`** (Stevens technology teacher, self-ID) vs **`Hillary Walsh`** (Ward 1 commenter, adult-ed teacher, "name per approved minutes") — plausibly one person, independently sourced two ways, left split. **`Hanna Brooks`** (resident commenter) vs **`Hannah Brooks`** (Greater Sullivan County Public Health Network / Dartmouth-Hitchcock presenter) — different roles, left split. Genuinely different people sharing a surname, no action: Kiran/Onyx/Patrick Adrian · Michelle/Rod Beaton · Christina/Ray Bernard · Derek/Sarah Ferland · Jennifer/Maggie Gallagher · Dale/Ellie Girard · Alex Hill/Karen Liot Hill · Cynthia/Loren Howard · Charlene/Marian/Mary/Rob Lovett · Paul/Tom Luther · Eric/Leslie Peabody · Michael/Hannah Petrin · Scott/Tracy Pope · Rob/Stephen Walker · Sherry Williams/Asher James Williams · **Alex vs Aubree Herzog**, plus **Shawn/Sean Herzog** (Title I at Maple) as a third · **Michael vs Michelle Herrington**, which appears in the same file at least three times and must never be merged (B1.5).

*Primary source:* briefing Addendum 9; the corpus-wide surname sweep.

### D1.9 · Sprague's biography is contradictory six ways and neither reading was forced
**Tier 1 · one-off, deliberately open · Sources: briefing D19**

Across the corpus one man is a **guidance counselor** (8/2/23), a **principal** ("three different high schools", 7/19/23; 11/15/23; 12/18/23; "when I was in Mr. Herrington's position", 8/21/24), a **director of student services** ("and I acted as the LEA", 12/6/23), an administrator ("when I was working for the district", 1/5/24), a Newport employee in the early 90s (12/13/23), and a **juvenile-court liaison** ("I did that for six years", 11/19/24) — and on **12/4/24, every word at conf 1.00**: "I'm not considered to have a higher degree because I only have an associate's degree… both my wife and I both have [associate's] degrees." **That cannot be squared with a principalship.** Two possibilities remain open and neither was forced: an unusually varied career, or **`Speaker 7` in 16192 merges two men** — and the approved 12.4.24 minutes give three of that cluster's turns to Michael Petrin, including the answer running continuously into the associate's-degree line, which is external support for the merge reading (B1.8). **A human should rule before either CSV is changed.**

*Primary source:* briefing Addenda 4, 5, 6, 9, 18; the 12/4/24 recording and approved minutes.

### D1.10 · ffmpeg scene analysis cannot distinguish a splice from a camera cut
**Tier 1 · systemic — a permanent limit of the pixel method on these recordings · Sources: briefing D3 · html-briefing D11**

An agent frame-differenced a suspected join and found YAVG spikes of **42–140** — but the same measure shows routine spikes of **60–74** elsewhere in the same file, from multi-camera shot changes. **The video does not decide it.** Where a zero-gap transcript raises the question, present both readings and say what would settle it — a district-side clock reference, or the raw CCTV log — and **never assert a splice from pixels**. The cheaper tests that do work, in order: run-time arithmetic, then spoken clock times, then spoken countdowns (B2.3, C2.4).

*Primary source:* the frame-differencing run — YAVG 42–140 at the join against 60–74 elsewhere in the same file.

---

## D · Tier 2 — affects what a reader can find or verify

### D2.1 · Google Drive `search_files` returns unreliable negatives — and unreliable positives
**Tier 2 · systemic, nine-plus documented failures · Sources: briefing D1 · html-briefing D5 · legal-anchors D1, F7**

Two agents independently established it, and the confirmations now run to nine or more. `parentId` queries return `{}` for folders that demonstrably hold files — `27. CSB 12.6.23`, which has four documents; `6. CSB 10.16.24` and `8. CSB 11.20.24`, whose files are readable individually by `get_file_metadata` seconds earlier; the 2024 minutes folder. `title contains` misses files whose names contain the exact search string — a search for `working session` returned two unrelated files and **not** the document the 2/21 page was about, and `title contains '9.30.24'` returned `{}` while two files carrying that exact string were readable individually. It appears to index only items the signed-in account has previously opened. Worse, **a non-empty result proves nothing about completeness**: a `parentId` enumeration of the 2024 packets share returns the same 18 folders every time and **silently omits three that MAP.md records** — `1. CSB 8.7.24`, `7. CSB 11.6.24`, `8. CSB Retreat 5.11.24`. And a folder-scoped check wrongly reported the 4/11/24 SAU 6 draft missing. **Never write "the share contains N folders" from a `parentId` call, and write every packet negative as "not found", never as "does not exist"** — a missing-minutes finding built on a `{}` result would assert a records failure the browser enumeration disproves. Folder contents must be enumerated through the signed-in browser, as the `update-google-drive-map` skill does, and any negative must name the folders opened and how. **Some negatives already in MAP.md are contaminated by this.**

*Primary source:* `get_file_metadata` and browser enumeration returning what `search_files` omits, repeatedly.

### D2.2 · SAU 6 minutes require a two-stage search before any negative
**Tier 2 · systemic · Sources: briefing D2 · html-briefing §6**

Check the meeting's own folder, then **every** later SAU 6 folder by filename date, then the Claremont Meeting Minutes share — which **has never held an SAU 6 file** — and if still nothing, say the search was two-stage and name the folders checked. The 12/7/23 negative was reached this way: all 19 SAU 6 folders dated after the meeting were opened, plus the packets-share root and the Claremont 2023/2024 Minutes year folders, 46 files, all CSB. The filing practice behind the rule is at A2.9 and A2.10.

*Primary source:* html-briefing §6; briefing Addendum 11; MAP.md §31.

### D2.3 · `rollcall_evidence_2023_2024.md` is unreliable and provably so
**Tier 2 · systemic · Sources: briefing D4**

It reported "(none matched)" for the 2/16/23 SAU meeting's self-IDs and direct addresses — a file "dense with both" — and again for 15947, 16011, 16021, 16142 and others whose transcripts contain a dozen or more usable chair recognitions. Its window **stops at segment 79**, and in **16070 every anchor fell outside it**. Use it as a fast start only; it is not a substitute for reading the working transcript.

*Primary source:* briefing Addenda 3 and 8.

### D2.4 · `verify_quotes.py` has four documented limitations
**Tier 2 · systemic · Sources: briefing D5 · html-briefing D2, D3 · legal-anchors D2, D3, D4**

(1) Its scanner is `"([^"]{8,600})"`, so **any quoted span under 8 characters is skipped**, which shifts the open/close pairing for the rest of that block and manufactures REVIEW lines built from the page's own prose — twelve phantoms on one page (C3.1). (2) **A quotation over 600 characters exceeds the matcher's window and silently swallows the quotes that follow it** — split long ones; silent swallowing means downstream quotations go unverified with no signal. (3) Its stutter collapse is `\b(\w+)( \1\b)+`, which handles single-word repeats only and **cannot** collapse repeats containing an apostrophe (`we've we've`) or phrase repeats (`we want to we want to`, `at the at the`); those always show as unmatched and must be **preserved verbatim** rather than tidied to satisfy the tool, since tidying would publish a quotation the recording does not support. (4) It **used to cap the list at 12** with "... and N more", making a before/after audit of an edit impossible; patched 2026-08-29 so a single-page run prints every miss, while `--corpus` still caps at 12. Limitations (1) and (4) are also recorded in `pending_legal_anchors.md`.

*Primary source:* `Scripts/verify_quotes.py`.

### D2.5 · Drive folder labels change under the project and cannot support a finding
**Tier 2 · systemic · Sources: briefing D15 · html-briefing D10**

`1sBcCWTWabFKR3P89uBbgV8SgPzV86LXq`, listed as Ad Hoc Reconfiguration, now returns the title **"[Documents posted to Web]"**, created 2026-04-15; `1UyUWBMgA6z4tZxbc8SSt-wgUEo-Ovlmh`, listed as Policy, is now titled **"[Documents posted to web}"**, modified 2026-07-20. Folder labels must be re-read at the time of writing and never made load-bearing.

*Primary source:* re-reading the two folder IDs on 2026-08-29.

### D2.6 · Two-column district PDFs interleave on extraction, so their ORDERING is unreliable even when the text is clean
**Tier 2 · systemic — every multi-column district PDF · Sources: briefing D9 · html-briefing D14, D15**

The 6/5 packet's CCTV roster reads as though a seat sits under the wrong heading, and the same scrambling **manufactured a plausible committee name that does not exist**. The Drive MCP's `read_file_content` compounds it on contracts — on one it interleaved the DRAFT watermark and reordered clauses, hiding a sub-clause and the 1–16, 27, 21, 22 numbering (A2.28). **Treat column order in any two-column district PDF as unverified.** The fix: `mcp__Google_Drive__download_file_content` → base64 decode → **`pdftotext -layout`** in the cloud container, which has `pdftotext`, `pdftoppm`, `pypdf` and `pdfplumber`. `read_file_content` remains the right tool for Google Docs (C2.6) but must not be used for contracts or multi-column PDFs.

*Primary source:* the 6/5 packet CCTV roster; the contract recovered by `pdftotext -layout`.

### D2.7 · Network access is partial and asymmetric, and `WebFetch` caps quotation length
**Tier 2 · systemic — an environment constraint on every page · Sources: briefing D10 · html-briefing D17, D18**

**`curl` does not work** — there is no egress at all from the device shell, and from the cloud container the agent proxy returns 403 / `connect_rejected` for `gc.nh.gov`, `law.justia.com`, `govinfo.gov`, `drive.google.com` and `reflect-claremont.cablecast.tv`. **`WebFetch` reaches all of them** and is the route for statute texts and the Cablecast API — **but it caps quotation length**, so verbatim statutory text must be requested as "short exact fragments, each under 120 characters, labelled by paragraph, plus the source note verbatim"; otherwise the quotation is truncated silently.

*Primary source:* the observed 403 / `connect_rejected` responses; `WebFetch`'s own quotation cap.

### D2.8 · The live policy index gives the latest revision date, not the adoption date
**Tier 2 · systemic, with a workaround · Sources: briefing D11 · html-briefing D19**

Open the policy itself and read its own "District Policy History" block — doing that recovered two supposedly unrecoverable adoptions on one page: **BEDH, first reading 17 May 2023, adopted 6 September 2023**, which independently corroborates that the unminuted 5/17/23 meeting really happened (A2.1); and **JLDBB, read and adopted 6 May 2020**. The index itself is nonetheless the authoritative answer to "what was actually adopted": `Claremont SB Policies (for Web)`, Drive doc `1JmygIGNaVc8ZfaQWtoIA25tRaBGw2Oh5k5ARsGlreqg`, owner `sau6webmaster@sau6.org`, listing every board policy with its adoption date and linking the current text — **check it on every page that touches a policy reading** instead of writing that an adopted text is unrecoverable.

*Primary source:* each policy's own "District Policy History" block; the live policy index doc.

### D2.9 · Which by-laws copy was in force on a given date is generally unknowable from here
**Tier 2 · systemic — every by-law citation from 5 June 2024 onward · Sources: briefing D15 · html-briefing D27, §27c**

Two versions differ in numbering and wording — the adopted PDF and the live Google Doc — with no version history recoverable (A2.19). The available mitigation is to **quote by-law TEXT, never a number alone, and say which copy was read and when it was modified**.

*Primary source:* html-briefing §27c's own statement of the limit.

### D2.10 · The SAU 6 website as it stood in 2024 cannot be inspected
**Tier 2 · systemic — a permanent evidentiary limit for the 2024 period · Sources: briefing D16 · html-briefing D22**

The by-laws send every subcommittee notice and set of minutes there. The honest limit is **"not published where the by-laws require, and not recoverable" — not "never existed"**, because the board itself conceded the venue was not operating (21 August 2024 approved minutes: "once the website is up and running, those will be available"). The destination is checkable prospectively for every Claremont page from 5 June 2024 onward (A2.22).

*Primary source:* the state of `sau6.org/119765_1` and its five linked folders as read on 2026-08-29.

### D2.11 · A joint city/district meeting cannot be assessed from the district's shares alone
**Tier 2 · systemic — every joint meeting · Sources: briefing D17 · html-briefing D25**

It is **two bodies** and must be handled as two, each quorum established against its own membership — the City Council is a **nine-member** body (Valley News, 27 Oct 2025), so seven present is its own quorum and the two bodies met separately in the same room. The city's notice, agenda and minutes live in the **city clerk's** system, not the district's Drive. **Never write a city-side negative from the district's shares**; say what was inspected and what could not be. The `16046` page does this correctly and is the model. Note also that the joint meeting has minutes but no packet folder (A2.4).

*Primary source:* html-briefing §25e; briefing Addendum 17; Valley News, 27 Oct 2025.

### D2.12 · A subcommittee minutes-gap needs a comparator, not a bare negative
**Tier 2 · systemic method rule · Sources: html-briefing D26**

"No minutes found" alone is not the finding; the same night's board packet is the comparator — `10. CSB 12.18.24` contains `CSB Visioning Sub 12.9.24.docx.pdf` and `Cap Improvements Committee Meeting minutes 12.10.24.pdf`, so two other subcommittees minuted their December meetings and the district filed them, while Finance filed none for any of its three televised sessions. **That contrast is the finding** (A2.3).

*Primary source:* packet folder `10. CSB 12.18.24` and its two subcommittee minutes files.

### D2.13 · Where an attribution cannot be settled from the tape, the district's own minutes often can
**Tier 2 · systemic method · Sources: briefing D24 · html-briefing §16, §28g**

Two "Unidentified public commenter" clusters on show 17159 are named in the approved minutes — **January King, ward 3; Kyle Messier, ward 1** — and a speaker the CSVs called "Noah Bosch" in one file and "Nora Shane" in another is **Noel Beauchaine**, corroborated by the interim superintendent thanking her by name on tape. Likewise Claremont's minutes list floor speakers grouped by position but in speaking order within each group, verified twice on 2/3/24, which makes ordinal identification defensible provided the working is shown and no name is given where two turns cannot be told apart (B1.21). **Read the minutes before writing "unidentified."**

*Primary source:* html-briefing §16, §28g; briefing Addendum 12.

### D2.14 · Facts that cannot be settled from the record, itemised
**Tier 2 · systemic · Sources: briefing D18**

**Who cast the single No** on the SAU 6 budget on 12/12/24 — not named, not counted, no minutes; "the dissenter cannot be identified by anyone." **The 11/14/24 SAU 6 policy-motion mover** — the chair's recognition is `Okay windy` (0.80), an ASR form this corpus attests for **both** Heather Whitney and "Candy" (Crawford); the two lines of evidence disagree and the approved minutes would settle it. **The `15357` Speaker-4 cluster** — unresolved after its premise collapsed (C1.128). **The 2/8/23 41–27 tally** — absent from the transcript, untested on the video (C2.2). **The Parliamentary Procedure committee's third member** — open until 4/17 settled it as Petrin. **The Stevens interim principal of early 2024** — named nowhere, the report unsigned (C1.143). **The 15607 / `Mr. Broughton` class of garble** — recurs and still names nobody.

*Primary source:* briefing Addenda 9, 13, 14, 15, 18; html-briefing §23d.

### D2.15 · The current eCFR must not be cited for 2023–24 federal material; use the govinfo annual edition
**Tier 2 · systemic, adopted as a fix · Sources: html-briefing D20 · legal-anchors D15**

`https://govinfo.gov/content/pkg/CFR-2023-title2-volN/xml/CFR-2023-title2-volN-sec200-NNN.xml` returns the 2023 annual edition; **vol1** is the working volume for 200.344. Verified for 2 CFR 200.439(b)(1)–(3) and 2 CFR 200.344(b). Reuse it for every Uniform Guidance citation in this backlog. The pattern extends to title 34: `…/CFR-2023-title34-vol1/xml/CFR-2023-title34-vol1-sec99-3.xml`. Without it, eCFR's current text silently substitutes post-2024 paragraph lettering and thresholds (C1.61, C1.62, C1.79–C1.81).

*Primary source:* https://www.govinfo.gov/content/pkg/CFR-2023-title2-vol1/xml/CFR-2023-title2-vol1-sec200-344.xml.

### D2.16 · URL traps — RSA chapter-to-title mismatches
**Tier 2 · systemic · Sources: legal-anchors D9**

Six recorded, each of which produces a dead citation URL in a published page: **RSA 198 is Title XV, not Title IX** (`gc.nh.gov/rsa/html/IX/198/…` 404s); **RSA 21-J is Title I, not Title III**; **RSA 273-A is Title XXIII** (`/LXIII/273-A/…` 404s); **RSA 288 is Title XXV, not XXIII**; **RSA 671 is Title LXIII** (`/XV/671/…` and `/xv/671/…` both 404, and law.justia's title-xv path 404s too); **RSA 5-B is Title I** (`gc.nh.gov/rsa/html/I/5-B/5-B-mrg.htm`). Also: `gencourt.state.nh.us/rules/…` 302-redirects to `gc.nh.gov/rules/state_agencies/…`.

*Primary source:* the URL tests recorded in the legal-anchors file.

### D2.17 · Bad URL — the CEP rule's Federal Register document number
**Tier 2 · one-off · Sources: legal-anchors D10**

88 Fed. Reg. 65778 (the CEP 40%→25% change, C1.55) is Federal Register document **2023-20294, not 2023-20971** — that number is an Indian gaming notice, so a reader checking the citation finds a document about gaming. Working link: https://www.govinfo.gov/content/pkg/FR-2023-09-26/html/2023-20294.htm.

*Primary source:* the two document numbers tested.

### D2.18 · The statewide bell-to-bell phone ban is not verifiable as a codified RSA
**Tier 2 · one-off, unresolved · Sources: legal-anchors D11**

It did **not** come from **HB 781 (2025), which was vetoed July 7, 2025**. It arrived in the 2025 budget trailer, effective July 1, 2025. **No codified section was found — do not cite one.** Citing HB 781 would attribute a live mandate to a vetoed bill; inventing a codified section would put an unverifiable RSA number in a page.

*Primary source:* legal-anchors, "Two more vintage traps (waves 3–4)".

### D2.19 · HB 1563's chapter number is not verified
**Tier 2 · one-off, unresolved · Sources: legal-anchors D12, V54**

The 2026 special-education formula bill is recorded with the caveat "bill text verified; **chapter number NOT verified against a primary source — do not state one**." Reported signed July 2026, effective **July 2028**; three-tier formula — a new 2.5×–3.5× band at **15%**, 3.5×–10× stays at **80%**, above 10× cut from 100% to **90%** — plus a Medicaid-to-Schools exhaustion requirement, five-year reviews and random/targeted audits. No meeting in this corpus is after July 2028, so it governs none of them; stating a chapter number would fabricate a primary-source citation.

*Primary source:* https://legiscan.com/NH/text/HB1563/id/3290318 ; NH Bulletin, 10 July 2026.

### D2.20 · 2026 N.H. Laws ch. 153 (HB 564) is volatile and unre-verified
**Tier 2 · one-off, flagged for re-verification · Sources: legal-anchors D13, V53**

Signed 6/19/2026, **effective 8/18/2026** — revises the annual budget adoption procedure for school administrative units and **repeals the alternative procedure at RSA 194-C:9-a / 9-b**. "Volatile: re-verify before applying to any post-August-2026 meeting." Applying it without re-verification risks citing a repealed alternative procedure, or missing a repeal that took effect mid-corpus.

*Primary source:* https://legiscan.com/NH/bill/HB564/2026.

### D2.21 · The NH Supreme Court slip opinion is unreachable from this environment
**Tier 2 · one-off, unresolved · Sources: legal-anchors D16**

*Appeal of Pittsfield School District*, No. 2024-0445, October 2025 — a resident district owes RSA 194-D tuition even if it has not adopted open enrolment. **The slip opinion 403s from this environment**, so the holding rests on secondary reporting, not on a read primary source; cite the statute plus the InDepthNH report of 19 October 2025 as reporting.

*Primary source:* InDepthNH, 19 Oct 2025 (reporting); RSA 194-D:3, :4, :5.

### D2.22 · Press anchors are secondary and must be attributed as reporting — and two of them disagree
**Tier 2 · systemic handling rule; one unresolved discrepancy · Sources: legal-anchors D17**

The file segregates press sources and directs "attribute as reporting, not law": Valley News 2026-01-02 (audit findings; auditor Michael Campo, Plodzik & Sanderson), Valley News 2026-07-27 (interim business administrator resignation), NH Bulletin 2026-04-22 (SB 586), NH Bulletin 2024-11-15 (FY2025 catastrophic aid — $33.9M appropriated vs $50.3M eligible, **67.5%**; 87% in 2023, 98.3% in 2022), NH Bulletin 2026-07-10 (HB 1563), NHFPI (FY2025 proration **68.8%**; prorated in all but two years since SFY 2009). **The two FY2025 proration figures differ between sources — 67.5% vs 68.8% — and the file does not reconcile them**, which matters because the figure is the denominator of the catastrophic-aid finding at A1.26 and C1.8.

*Primary source:* the URLs listed in the legal-anchors file.

### D2.23 · Several holdings are recorded without the page being individually fetched
**Tier 2 · systemic provenance gap · Sources: legal-anchors D18**

Marked in the Verified column: **2 CFR 200.303** ("holding standard; page not individually fetched"), **2 CFR 200.318–.327** ("holding standard"), **7 CFR 210.16** ("holding standard"), and **RSA 194-C:9** ("holding from the chapter index; section page not individually fetched"). These are asserted holdings without a read primary text behind them at the time of entry.

*Primary source:* the eCFR / gc.nh.gov URLs as listed in the catalogue.

### D2.24 · OPEN — the pre-12-13-24 text of Ed 302.02(j) has not been recovered
**Tier 2 · one-off, unresolved; blocks two potential findings · Sources: legal-anchors D5, F9**

Ed 302.02(j) as readopted 12-13-24 (Doc #14150) reads "Be responsible for maintaining records and filing reports as required by the state board of education and the local school boards." **SAU 6's policy BEDG cites it for "all minutes will be kept at the office of the Superintendent," which the current text does not say.** A copy of the Ed 300 rules as they stood before 12-13-24 would settle this and the Ed 303.01(f) vintage question at A1.11. **Do not flag either as a defect until it is found** — flagging now would accuse the policy of misciting a rule whose relevant vintage has not been read.

*Primary source:* https://gc.nh.gov/rules/state_agencies/ed300.html.

### D2.25 · OPEN — the pre-11-16-24 text of Ed 503.01 has not been recovered
**Tier 2 · one-off, unresolved · Sources: legal-anchors D6, V36**

Ed 503.01 ("Requirement for Employment") was amended by Doc. **#14109, eff. 11-16-24**. **The pre-amendment text has not been recovered — say so rather than guessing.** Any credentialing finding for a pre-November-2024 meeting rests on unread text.

*Primary source:* the NH Ed 500 rules at gc.nh.gov.

### D2.26 · OPEN — RSA 671:33, II(a)'s measuring base is ambiguous
**Tier 2 · one-off, unresolved · Sources: legal-anchors D7**

Whether "unable, by majority vote, to agree" measures the remaining members or those present and voting is **not settled by the text; both readings are live; do not choose.** Source note ends 2021, 42:1, eff. July 16, 2021; 91:318, eff. July 1, 2021. Choosing a reading would produce a determinate finding on whether a board validly failed to fill a vacancy, on a question the text does not settle.

*Primary source:* https://gc.nh.gov/rsa/html/LXIII/671/671-33.htm.

### D2.27 · OPEN — RSA 189:74's 30 minutes is not settled as opportunity or elapsed time
**Tier 2 · systemic (every public-comment page), unresolved · Sources: legal-anchors D8, F10**

Whether the 30 minutes is a floor on the *opportunity* or on elapsed time is not settled by the text — **say so rather than asserting a violation when nobody was turned away** (2022, 333:1, eff. Sept. 6, 2022; never amended). A page assuming elapsed time would flag a short comment period as a violation where no speaker was refused. The `14937` page states the limit correctly on its face. It is also not settled on this record that RSA 189:74 reaches an SAU board at all: the chapter speaks of "school board" and "school district matters", while RSA 194-C:5 calls that body "the school board of each school administrative unit".

*Primary source:* https://gc.nh.gov/rsa/html/xv/189/189-74.htm ; page `14937 SchoolBoard030123` and `14911 SAU6021623`.

### D2.28 · Ed 306 renumbering makes subsection numbers unsafe to guess
**Tier 2 · systemic · Sources: legal-anchors D14**

Cite the part page; **do not guess subsection numbers** — the rules were renumbered in the 2024–25 revision. Confirmed movements under Doc. #14150, eff. 12-13-24: Ed 306.14 was 306.17; Ed 306.12(d) was 306.15; Ed 306.17 is now "Alternative Programs"; Ed 306.15 is "School Year" today but was "Provision of Staff and Staff Qualifications" in 2023; Ed 306.07 was also renumbered and readopted. A guessed subsection number cites a rule about a different subject (C1.69, C1.70, C1.84).

*Primary source:* https://gc.nh.gov/rules/state_agencies/ed300.html ; NHDOE's March 2023 side-by-side.

### D2.29 · The open questions MAP.md itself flags as unresolved
**Tier 2 · systemic · Sources: map+pages §4**

Fifteen, preserved as the map states them. **(1)** §1 — "whether the duplicate should be retired is an open question." **(2)** §96a — a same-date folder also exists in the Claremont packets share, `9. CSB 10.6.25`; "whether the two agendas describe the same gathering was not determined" (superseded for §96 by the 2026-08-29 split, but the note stands in §96a). **(3)** Caveats, 8/21/25 — "whether that is one gathering recorded twice or two separate meetings was not determined… The same ambiguity affects 10/6/25." **(4)** Two 2024 filenames — "contents were not opened, so the body each actually records is unverified." **(5)** §93, §96a, §99 — "the SAU 6 packet folders carry minutes for *earlier* meetings rather than their own, so this meeting's minutes may appear in a later folder." **(6)** §109 — "the minutes remain a DRAFT; every other 2026 meeting through June has approved minutes, so this one is worth re-checking." **(7)** §119 — four sub-folders whose "contents were not opened." **(8)** `2022 Meeting Packets` "remains unopened." **(9)** The two empty district folders — "worth re-checking: if finance-committee material is ever posted, the first is where it would go." **(10)** "Document contents were not opened, so a misdated upload would not be caught." **(11)** "Contents will change as the district posts new packets; re-check before publishing." **(12)** Four SAU 6 meetings with no recording — "their sections carry no `Remote video:` line, which is the map's signal to re-check." **(13)** "This run covered Drive only. The 74 sections added on 2026-08-28 carry no `Remote video:` line… Run that skill to fill them in" (subsequently satisfied the same day). **(14)** §123 — the only 6/19/26 finance material anywhere is *outside* the district share: `Finance Sub-Committee 2026-06-19 - Minutes with video links` (`1Ku7qQ-q6Ubure_1YE83EbOGuklm_uv24`) and `Copy of Finance Sub-Committee June 19, 2026.docx` (`14h3LrdZWWgIG4RtNZ_QPxNdy_LfYSXDs`), both owned by the maintainer (D1.1). **(15)** §20's 2026-08-29 correction, recorded at C1.155.

*Primary source:* MAP.md, section notes and "Method and caveats".

### D2.30 · The corpus's own unresolved-question phrase scan
**Tier 2 · systemic · Sources: map+pages Part 2 §1**

A measure of how much of the finished corpus is hedged rather than concluded. Denominator 126 pages (`index.html` and `style.css` excluded).

| Phrase | Pages carrying it | Total occurrences |
|---|---|---|
| `could not` | 104 | 360 |
| `cannot be` | 94 | 278 |
| `no record` | 63 | 157 |
| `does not exist` | 46 | 104 |
| `not settled` | 41 | 59 |
| `would settle` | 30 | 51 |
| `not found` | 29 | 50 |
| `names nobody` | 20 | 31 |
| `not located` | 15 | 32 |
| `left unresolved` | 13 | 17 |
| `states the limit` | 3 | 3 |
| `chooses neither` | 2 | 2 |

Representative instances the map quotes exactly: `14892` — the written amendment the moderator required to be signed by mover and seconder and read from at 0:29:47, and the DRA default budget form RSA 40:13, XI(a) requires with its line for "Reductions for eliminated positions", both absent from the packet and from the February 1 packet; `14909` — "the fiscal 2024 default budget form (MS-DSB)… the document that would show how $36,342,948 and then $36,942,948 were derived", with "The form is a governmental record; nothing here suggests it does not exist, only that it is not where a resident would look"; `15153` — "no nonpublic-session minutes for June 21, 2023 in this meeting's packet folder, in the district's Meeting Minutes share, or in that share's Unsealed Minutes folder"; `15253` — no amended student handbooks, no list of withheld nonpublic minutes of the kind RSA 91-A:3, III requires, no written record of the school nurse's input, and no surname anywhere for the nurse the record calls "Ronnie"; `15413` — "the seals were entered without the statutory finding, that they expired on the board's own terms and nothing followed, and that the list the statute requires does not exist"; `15451` — "an approved public record tells the public that a record exists which does not exist"; `15452` — "A ninety-minute video satisfies none of those requirements: it is not indexed, it is not searchable, it names nobody, and it cannot be inspected in the sense the statute means"; `15531`, `15693`, `15947`, `15994`, `16157` — each writing its Drive negatives as **not found**, never as **does not exist**, on the strength of D2.1.

*Primary source:* the phrase scan of the 126 pages in `Output/HTML/`.

### D2.31 · The public Cablecast show page gives no run time; only the API does
**Tier 2 · systemic · Sources: html-briefing B8, §23f**

Run times are unavailable from the public show page but are returned by `https://reflect-claremont.cablecast.tv/cablecastapi/v1/shows/<ID>?include=reel` as `totalRunTime` in seconds, which is what bounds a page's `seekto` values and what makes the run-time arithmetic at B2.3 possible.

*Primary source:* the Cablecast API `?include=reel` endpoint.

### D2.32 · "When I was superintendent there" is a live trap for the roster correction
**Tier 2 · one-off, guarding a systemic correction · Sources: html-briefing D24**

Chris Pratt says it on the 4/19/23 recording — of **Bellows Falls**, before Claremont. He is not Claremont's superintendent in 2023 and that sentence does not make him one (C1.117).

*Primary source:* the 4/19/23 recording.

---

## D · Tier 3 — affects precision, not conclusions

### D3.1 · Same-second link collisions in generated pages
**Tier 3 · systemic, with a fix · Sources: briefing D22 · html-briefing D21, §8, §23f, §25c**

Consecutive CSV rows can share a truncated second, so a `seekto` may land one row early. **Take the `Start (sec)` integer and render the visible `H:MM:SS` from that same number** — text and link then cannot disagree.

*Primary source:* the CSV's truncated-second timestamps.

### D3.2 · `validate_pages.py` flags UTC clock times as malformed timestamps
**Tier 3 · systemic false positive, with a workaround · Sources: html-briefing D4 · briefing D22**

Writing a UTC clock time such as `14:06:36` trips `validate_pages.py`'s H:MM:SS note. The workaround is to drop the seconds when citing Drive metadata.

*Primary source:* `validate_pages.py`'s H:MM:SS note.

---

# POINTS WHERE THE FOUR INVENTORIES DISAGREE

Reported rather than resolved, as the merge rules require. The first five are the ones the briefing inventory's own closing section lists; the last three were found in the merge.

1. **The 10/18/23 minutes (A1.39, C1.128).** Briefing Addendum 5 says they wrongly recorded Gallagher present; the Addendum 11 correction says that is FALSE and the minutes read `Absent: Jennifer Gallagher`, confirmed independently by two agents against the document. The unresolved consequence is that the `15357` Speaker-4 cluster's 2026-08-28 re-weighting rests on a collapsed premise.
2. **The Rebecca cluster (A3.13, C3.5).** `html_briefing.md` §15h/§28f treats Duska / Vendesco / Vinduska / Vindeska / "von Duska" as one person probably named **Vinduska**, on the Byrne Foundation letter of 7 February 2023 and the approved 18 February 2026 minutes. `briefing.md` Addenda 6 and 9 record **Rebecca Duska**, CMS 6th-grade science teacher, Ward 1, as the settled resolution of `15483` Speaker 10 — an applied CSV correction. **Neither file reconciles the two.**
3. **The corpus size.** `briefing.md` Addendum 9 reports **127 transcripts, 127 CSVs, 0 missing**; `html_briefing.md` §29 reports the page run "complete at **126 pages**"; the map-and-pages inventory counts **126 finished pages** in `Output/HTML/` and **129 MAP sections**. Not reconciled anywhere. The 126/127 gap is consistent with — but not proven by — the excerpt and duplicate files at B1.17, B1.19 and B2.7.
4. **`the Dow` (B1.1).** `briefing.md` Addendum 8 carries `the Dow building` / `the Dow office` (both conf 1.00) as a phantom-name ASR garble — "full confidence, plausible proper noun, no such place". `html_briefing.md` §29i explicitly un-flags it: "**`the Dow` is NOT an ASR garble** — it is the district's own name for the SAU office building, used in its approved minutes and on an agenda." The html-briefing reading is later and better evidenced; both are recorded.
5. **Cat / Catlin / Kat McLaughlin (A3.11, C3.3).** Resolved and un-resolved four times across briefing Addenda 13–17, with a sixth data point (one Superintendent's Report page printing both spellings) leaving it open. The standing instruction is to print no spelling as fact.
6. **Where the Cablecast records belong.** `briefing.md` A82 files CCTV's mis-titled shows as **Class A**, "source-system record"; `html_briefing.md` files the same material and the `eventDate` behaviour as **Class B**, project pipeline data. This master inventory follows the briefing file and places CCTV title and `eventDate` defects in Class A (A3.26–A3.29), because CCTV is a third-party source rather than project output.
7. **Where the `Unidentified` rate belongs.** `briefing.md` D14 files it as a **method limitation (Class D)**; `html_briefing.md` B15 files it as **pipeline data (Class B)**. This inventory places it in Class B (B2.1) as a property of the dialogue CSVs, with the honest-rate rule carried in the same record.
8. **The FY2025 catastrophic-aid proration rate (D2.22).** NH Bulletin 2024-11-15 gives **67.5%**; NHFPI gives **68.8%**. The legal-anchors file records both and reconciles neither, and the figure is the denominator of the findings at A1.26 and C1.8.

## Two items named in the source task that are not attested anywhere

- **Lavalette / Lavallette.** Only `Lavalette` appears in the briefing set — Don Lavalette, sworn in 3/18/26, and the eight `16951` rows corrected to him (B1.15). No second spelling exists.
- **Lowney / Lownie.** The attested pair is `Ken Lownie` / `Camron Lownie` — two different people, father and son, Ward 2, proven distinct because they co-occur in 16409 and 17046. Both spellings are ASR-derived from "Louny"; no documentary spelling exists and no "Lowney" appears (A3.16).
