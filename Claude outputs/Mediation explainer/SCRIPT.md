# Claude as the Front Desk for Claremont School District Records: explainer video script

Video version of the Claude Doc "Claude as Mediator of Claremont School District Knowledge: Theory and Appeal to Anthropic"
(https://claude.ai/artifact/JhnEnNf4KaNy7t5kQGQHWs). Built November 14, 2026.
Draft length 7:38 at an estimated 156 words a minute; the finished length follows your narration.

## What is in this folder

| Path | What it is |
|---|---|
| `Mediation-explainer-DRAFT.mp4` | Timing draft with no voice: narration shown as a caption band, 1920x1080 |
| `ElevenLabs narration/part_1.txt` to `part_4.txt` | The four blocks to paste into ElevenLabs, one generation each; `retake_<id>.txt` holds one paragraph |
| `SCRIPT.md` | This file: narration and picture for every segment |
| `script_data.py` | Single source for narration and pictures; edit here and rebuild |
| `build_video.py` | Builds the cut; writes `captions.srt`, `timeline.csv` and `chapters.txt` (same builder as the RTK explainer) |
| `align_narration.py` | Finds each paragraph's start in your audio (speech recognition) |
| `cards/` | 25 cards drawn at 2x, including the five-layer diagram in six highlight states |
| `portal_shots/` | Three screens reused from the RTK explainer: the working portal on invented test requests, stamped TEST DATA |
| `draft_captions/` | The caption bands used only in the draft |
| `_source/` | `make_cards.py`, `_css.py` (shared palette), `make_docs.py` |

## Generating the narration in ElevenLabs

1. Model **Eleven v4**, one voice for all four parts (the RTK explainer's voice, if you want the two to match).
2. Paste one file per generation:

| Part | Covers | Characters | Words | Paragraphs | Save as |
|---|---|---|---|---|---|
| 1 | Who is owed what | 1,681 | 279 | 6 | `audio/part_1.mp3` |
| 2 | How Claude would mediate | 1,420 | 244 | 6 | `audio/part_2.mp3` |
| 3 | Safeguards and a path | 1,508 | 248 | 5 | `audio/part_3.mp3` |
| 4 | Self-government and the appeal | 2,274 | 359 | 8 | `audio/part_4.mp3` |

3. Each file starts with the tag `[calm, friendly narration]`. If the voice reads it aloud, delete the line and regenerate.
4. Listen for "A-I", "Right-to-Know" and "Tocqueville". If "A-I" comes out wrong, try "A I".
5. Put the files in `audio/` as `part_1.mp3` to `part_4.mp3`, run `python3 align_narration.py`, then `python3 build_video.py` (or send them to Claude to build). To replace one paragraph, save it as `audio/seg_<id>.mp3` and rebuild.

## Running order

Narration is exactly what ElevenLabs reads.

**T0 · hold 4.0 s, silent** `cards/title.png`

### Part 1: Who is owed what

**1.01** This video describes a proposal for the Claremont School District. The idea is to use Claude, an A-I model made by Anthropic, to help the district answer the people it serves, on time and within the law. It also explains why the project is asking Anthropic for support.

> Picture: `cards/title.png`; then `cards/oneline.png`

**1.02** A school district owes information to many people, and the rules differ for each. Taxpayers and the public may inspect governmental records under New Hampshire's Right-to-Know Law. When a record is not immediately available, the district has five business days to respond.

> Picture: `cards/constituents.png` with a slow push-in

**1.03** Parents may see their own child's education records. Three laws set three deadlines for that: forty-five days under federal rule, fourteen days under one state law, and ten business days under a newer state law. A careful system follows the shortest.

> Picture: `cards/clocks.png`

**1.04** Students take over those rights at eighteen. Former students can ask for their own records for as long as the district keeps them. Teachers and staff need the policies that govern their work, including the version that was in force on a given date.

> Picture: `cards/constituents.png`

**1.05** The record is large. The School Board's policy index lists two hundred eighty-four policies, and one hundred twenty of them are dated before twenty fifteen. The archive of recorded meetings holds three hundred nineteen recordings. A resident with one free evening cannot read all of that.

> Picture: `cards/volume.png`

**1.06** That has consequences. In August of twenty twenty-five, the Board announced a deficit then estimated at up to five million dollars. Yet the Board had been told at public meetings in twenty eighteen and twenty nineteen that its audits were years behind. Those warnings were on the public record, in hours of video that few residents had watched.

> Picture: `cards/warning.png` with a slow push-in

### Part 2: How Claude would mediate

**2.01** Here is the proposed design. Every question, from any channel, passes through the same four layers. Every step is written to a log.

> Picture: `cards/arch.png`

**2.02** First, a gate. It is made of fixed rules, not a model. It decides who is asking, which privacy tier the request falls in, and which legal deadline applies. A public question needs no sign-in. A request for a person's own records is verified by staff.

> Picture: `cards/arch_gate.png`

**2.03** Second, the district's records graph. It holds public records only: every dated version of each policy, minutes, budgets, the index of recorded meetings, and each legal duty with its deadline and owner. Student and employee files stay in the district's own systems. They never enter the graph.

> Picture: `cards/arch_graph.png`

**2.04** Third, Claude. It searches the graph and answers in plain language, with a link to the minute, policy or recording behind each statement. When the graph holds nothing on point, Claude says so, and offers to open a records request.

> Picture: `cards/arch_claude.png`

**2.05** Fourth, a person. Where the law calls for a decision, Claude only drafts. A records custodian reads, edits and sends every response, and a draft with a blank left in it cannot be sent. The project's Right-to-Know portal already works this way. These screens show it running on invented test requests.

> Picture: `cards/arch_custodian.png`; then `portal_shots/05_console_draft.jpg`; then `portal_shots/09_send_blocked.jpg`

**2.06** Last, the log. Every request, answer, review and release is recorded in a chain that shows whether any entry was later changed. The public part of the log lists each request, its due date, and its response.

> Picture: `cards/arch_log.png`; then `portal_shots/10_log_list.jpg` with a slow push-in

### Part 3: Safeguards and a path

**3.01** The district's own policies set conditions that come first. Its policy on generative A-I requires the Superintendent's written approval before any A-I tool enters district systems. Its data governance policy requires the security officer to approve the vendor, even for a free service. The project's records show neither approval yet.

> Picture: `cards/conditions.png`

**3.02** Federal privacy rules let an outside company handle student records only under the district's direct control. That is a question for the district's lawyer. Until it is answered, Claude would see public records only.

> Picture: `cards/conditions.png` with a slow push-in

**3.03** A mediator is also a gatekeeper. Whoever runs it shapes what people find. The design limits that power. Answers link to the original records, so anyone can check them. The log is public. The meeting navigator stays independent of the district. And the portal can draft responses with no model at all, so the district never depends on one company.

> Picture: `cards/gatekeeper.png`

**3.04** The proposal starts small. Stage one answers questions about the public record. Stage two helps staff find the policy in force and draft routine letters. Stage three routes requests for a person's own records to staff, without the model reading them. Classroom use would come later, under the district's A-I plan, and is not part of this request.

> Picture: `cards/stages.png`

**3.05** Nobody yet knows whether wide use of A-I will raise achievement in Claremont, and this proposal does not claim it. What a pilot can measure is narrower: answers given on time, sources that check out, how often staff change a draft, and what each answer costs.

> Picture: `cards/measures.png`

### Part 4: Self-government and the appeal

**4.01** Why does this matter beyond one office? In Claremont, the voters act as the school district's legislature. In February of twenty twenty-six, residents debated the budget for four hours at the deliberative session. In March, they decided it by ballot. Each of those votes assumed that voters could find out what the district had done.

> Picture: `cards/voters.png`

**4.02** New Hampshire's constitution says government should be open, accessible, accountable and responsive, and that public access to its records shall not be unreasonably restricted. The Right-to-Know Law begins by calling openness essential to a democratic society.

> Picture: `cards/constitution.png` with a slow push-in

**4.03** In eighteen thirty-five, Alexis de Tocqueville wrote that town meetings are to liberty what primary schools are to science. They put self-government within reach. That worked when a farmer could know the town's business first-hand. A district with a budget near forty-three million dollars, and recordings back to twenty fifteen, is past that point. Search with cited answers can bring the record back within reach.

> Picture: `cards/tocqueville.png`

**4.04** Claremont has led before. Its name is on the nineteen ninety-three decision holding that the state must provide an adequate education and guarantee its funding. A district with a median household income of about fifty-four thousand dollars changed the rule for the whole state.

> Picture: `cards/precedent.png`

**4.05** That is why the project is writing to Anthropic. In its October twenty twenty-six registration statement, Anthropic says its public benefit work may include programs designed to make Claude accessible to underserved communities, educators, and public institutions. It also placed five percent of its shares in a public benefit fund.

> Picture: `cards/s1.png` with a slow push-in

**4.06** The draft letter asks for two things: use of Claude at no charge during a pilot, and an operating grant to a nonprofit operator. In return, the project would publish what it measures, failures included. Anthropic has made no commitment, and the filing describes no application process.

> Picture: `cards/ask.png`

**4.07** Some things must happen before the letter is sent. The district has to approve the tool, counsel has to review the design, and the sender should be a nonpartisan organization. The full proposal and its sources are in the written document that goes with this video.

> Picture: `cards/before.png`

**4.08** Rules decide who may see what. Claude finds and drafts. People decide. Thank you for watching.

> Picture: `cards/closing.png`

**END · hold 5.0 s, silent** `cards/end.png`

## Before you publish

1. **District approval.** Segments 3.01 and 4.07 say Claude is not yet approved under Policies EHAG and EHAB. That is from the project's records; confirm with the Superintendent's office before publishing, in case a request has been made since.
2. **The portal screens are test data.** They are the RTK explainer's captures of November 13, 2026 (rules engine only, no API key set). Segment 2.05 says they are test requests and each screen is stamped. They do not show Claude drafting.
3. **The 2018 and 2019 warnings** (1.06, `cards/warning.png`) are cited from The Elite Theory Perspective, which lists them as auditor warnings. The narration says only that the Board "had been told", because the 2018 speaker's role is not confirmed. Check the recordings before using the stronger wording.
4. **Budget "near forty-three million dollars"** (4.03) is the $42.9 million the Board recommended for 2026-27 (Valley News, January 22, 2026), not an adopted figure.
5. **Income figure** (4.04) is the NCES ACS-ED district dashboard, 2019-23. The written proposal flags other Claremont figures as secondary; none of those are used in the video.
6. **Anthropic.** Segments 4.05 and 4.06 quote the S-1 (page 144) and say plainly that Anthropic has made no commitment and the filing describes no application process. Recheck the page against the final prospectus.
7. **Political neutrality.** The video names the spending-cap article only as a ballot question (4.01 card) and takes no side. Segment 4.07 says the sender should be nonpartisan.
8. **Not legal advice.** The end card says so. Counsel has not reviewed the design.

## Sources

- Claude Doc "Claude as Mediator of Claremont School District Knowledge" and its Sources section (November 14, 2026)
- Claremont School Board [Policy EHAG](https://docs.google.com/document/d/1kNSusE8FCKmcwbniPH9WbJc8OgdHT8Q1v3jzy27PolI/edit) and [Policy EHAB](https://drive.google.com/file/d/1oqirKZ_27wFnxxqmc8WHHJ7GOPSS2UV3/view); policy index snapshot of October 30, 2026
- [RSA 91-A:1](https://gc.nh.gov/rsa/html/VI/91-A/91-A-1.htm); [RSA 91-A:4](https://gc.nh.gov/rsa/html/VI/91-A/91-A-4.htm); [RSA 189:66](https://gc.nh.gov/rsa/html/XV/189/189-66.htm); [RSA 189-B:4](https://gc.nh.gov/rsa/html/XV/189-B/189-B-4.htm); 34 CFR 99.10(b) and [99.31](https://www.ecfr.gov/current/title-34/subtitle-A/part-99/subpart-D/section-99.31)
- N.H. Const. pt. I, art. 8, as quoted in [Associated Press v. State (2005)](https://caselaw.findlaw.com/court/nh-supreme-court/1217347.html)
- Tocqueville, [Democracy in America, vol. 1](https://gutenberg.org/cache/epub/815/pg815-images.html), ch. 5, Reeve translation; [Claremont School District v. Governor, 138 N.H. 183 (1993)](https://leagle.com/decision/1993321138nh1831291)
- Anthropic, PBC, [Form S-1](https://www.sec.gov/Archives/edgar/data/2130357/000162828026067168/anthropicpbc-sx1.htm), filed October 26, 2026, pages 13 and 144
- Valley News: [January 22, 2026](https://vnews.com/2026/01/22/claremont-school-board-vote/), [February 9, 2026](https://vnews.com/2026/02/09/claremont-school-budget-spending-cap/), [September 23, 2026](https://vnews.com/2026/09/23/forensic-audit-of-claremont-school-district-faces-delay-and-potential-scope-cut/); [NCES ACS-ED dashboard](https://nces.ed.gov/Programs/Edge/ACSDashboard/3302340)
- The Elite Theory Perspective (project report, September 27, 2026); RTK Portal build record (October 30, 2026)
