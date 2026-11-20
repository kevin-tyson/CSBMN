# A Right-to-Know Request Portal for the Claremont School District: explainer video script

Companion to the briefing deck for the Claremont School Board and Administration. Built November 13, 2026.
Draft length 4:38 at an estimated 156 words a minute; the finished length follows your narration.

## What is in this folder

| Path | What it is |
|---|---|
| `RTK-Portal-explainer-DRAFT.mp4` | Timing draft with no voice: narration shown as a caption band, 1920x1080 |
| `ElevenLabs narration/part_1.txt` to `part_3.txt` | The three blocks to paste into ElevenLabs, one generation each; `retake_<id>.txt` holds one paragraph |
| `SCRIPT.md` | This file: narration and picture for every segment |
| `script_data.py` | Single source for narration and pictures; edit here and rebuild |
| `build_video.py` | Builds the cut; writes `captions.srt`, `timeline.csv` and `chapters.txt` |
| `align_narration.py` | Finds each paragraph's start in your audio (speech recognition), as in the Retrieval explainer |
| `portal_shots/` | Real screens of the RTK Portal at 3840x2160, running locally on four invented requests, each stamped TEST DATA |
| `cards/` | Title, law, policy, overview, queue, outcomes, triage, status, Anthropic, decisions and closing cards, drawn at 2x |
| `draft_captions/` | The caption bands used only in the draft |
| `_source/` | `capture_portal.py` (runs the portal and takes the screens), `make_cards.py`, `make_docs.py` |

## Generating the narration in ElevenLabs

1. Model **Eleven v4**, one voice for all three parts.
2. Paste one file per generation:

| Part | Covers | Characters | Words | Paragraphs | Save as |
|---|---|---|---|---|---|
| 1 | What the portal is | 1,055 | 177 | 4 | `audio/part_1.mp3` |
| 2 | How a request moves | 1,792 | 314 | 7 | `audio/part_2.mp3` |
| 3 | Why Anthropic | 1,097 | 184 | 6 | `audio/part_3.mp3` |

3. Each file starts with the tag `[calm, friendly narration]`. If the voice reads it aloud, delete the line and regenerate.
4. Listen for "R-S-A ninety-one A", "Policy E-H" and "A-I". If one comes out wrong, try spaces instead of hyphens.
5. Put the files in `audio/` as `part_1.mp3` to `part_3.mp3`, run `python3 align_narration.py`, then `python3 build_video.py` (or send them to Claude to build). To replace one paragraph, save it as `audio/seg_<id>.mp3` and rebuild.

## Running order

Narration is exactly what ElevenLabs reads.

**T0 · hold 4.0 s, silent** `cards/title.png`

### Part 1: What the portal is

**1.01** This is a short introduction to a Right-to-Know request portal, built for the Claremont School District. It shows how a request would move through the portal. It also explains why the project is asking a company called Anthropic for support.

> Picture: `cards/title.png`; then `portal_shots/13_home_after.jpg` with a slow push-in

**1.02** New Hampshire's Right-to-Know Law, R-S-A ninety-one A, gives every citizen the right to inspect public records. When a record is not immediately available, the District has five business days to produce it, deny the request in writing, or say in writing when it will answer.

> Picture: `cards/law.png`

**1.03** In September of twenty twenty-five, the School Board adopted Policy E-H. It directs the Superintendent's procedures to include, in the policy's words, a method for logging and tracking both the requests and the responses. The policy also allows that log to be posted on the District's website.

> Picture: `cards/policy.png` with a slow push-in

**1.04** The portal is one way to do that. A resident files a request online. The portal logs it, puts it in line, and prepares a draft response. District staff review and send every response. Then the request and the response appear on a public log.

> Picture: `cards/overview.png`

### Part 2: How a request moves

**2.01** Here is how a request moves. The screens you are about to see are the working portal, running on invented test requests. A resident describes the records they want, and confirms an email address with a six-digit code. The request then gets a public number, and a due date on the fifth business day.

> Picture: `portal_shots/02_form_top.jpg`; then `portal_shots/03_verify_code.jpg`; then `portal_shots/04_filed_status.jpg`

**2.02** Requests are handled one at a time, in a fair order. A person's first open request goes ahead of anyone's second. So one person who files many requests does not hold up everyone else.

> Picture: `cards/queue.png`

**2.03** Next, the portal sorts the request into one of five outcomes, and writes a draft to match. The most common is expected to be a records search, for a record that is not posted anywhere. Other drafts point to a record that is already public, offer combined figures about students, or cite the exemption that applies.

> Picture: `cards/outcomes.png`

**2.04** The first sorting is done by fixed rules. When it is switched on, Claude, an A-I model made by Anthropic, can then search the public record and prepare the draft. Either way, the portal accepts legal citations only from an approved list.

> Picture: `cards/triage.png`; then `portal_shots/05_console_top.jpg` with a slow push-in

**2.05** Nothing is sent automatically. A staff member at the Superintendent's office reads the draft, edits it, and sends it. If a draft still has a blank to fill in, the portal refuses to send it.

> Picture: `portal_shots/05_console_draft.jpg`; then `portal_shots/09_send_blocked.jpg`

**2.06** The public log shows each request, its due date, its status, and every response. Email addresses are never shown. A requester's name appears only if they choose. And text that may identify a student is held back until staff publish a redacted copy.

> Picture: `portal_shots/10_log_list.jpg`; then `portal_shots/11_log_detail_response.jpg`; then `portal_shots/12_log_held.jpg`

**2.07** The software passes fifty-six automated tests. An independent review found nineteen defects, and all of them were fixed. Two steps remain before a pilot. The District's counsel should review the legal citations and the response templates. And the Claude step, tested so far with a stand-in, needs one live test.

> Picture: `cards/status.png`

### Part 3: Why Anthropic

**3.01** Why Anthropic? The drafting step can use Anthropic's model, and that use costs money. The project does not want that cost to fall on the District's budget.

> Picture: `cards/why.png`

**3.02** In October of twenty twenty-six, Anthropic filed papers to become a public company. In that filing, it says its public benefit work may include programs designed to make Claude accessible to underserved communities, educators, and public institutions. It has also placed five percent of its shares in a public benefit fund.

> Picture: `cards/s1.png` with a slow push-in

**3.03** So the project plans to ask Anthropic for two things. The first is use of Claude at no charge. The second is an operating grant to the proposed operator, Claremont Community Television, also known as the Claremont Community Media Center.

> Picture: `cards/ask.png`

**3.04** Anthropic has made no commitment. If the answer is no, the portal still works, because the fixed rules can draft responses without Claude.

> Picture: `cards/ask2.png`

**3.05** We are asking the Board and the Administration for a small set of decisions. The first is whether to run a pilot. The briefing that goes with this video lists the rest.

> Picture: `cards/decisions.png`

**3.06** The portal drafts. District staff decide. Thank you for your time.

> Picture: `cards/closing.png`

**END · hold 5.0 s, silent** `cards/end.png`

## Before you publish

1. **The portal screens are test data.** `capture_portal.py` ran the portal from `RTK-Portal/` on November 13, 2026 against a fresh checkout of kevin-tyson/CSBMN (319 meetings indexed), filed four invented requests from example.org addresses, signed in as an invented staff address, and sent one response. Every screen carries a TEST DATA stamp, segment 2.01 says so, and the end card repeats it. "Pat Resident" and "Jamie Example" are not real people.
2. **The screens show the rules engine only.** No API key was set, so the console reads "rules only (no API key set)". Segment 2.04 and the triage card describe Claude as a step that runs when switched on. The Claude path has still been tested only with a stand-in (README, Review).
3. **"Most common is expected to be a records search"** (2.03) is the README's expectation, not a measured share. No request volume has been measured.
4. **Operator.** Segment 3.03 calls Claremont Community Television (CCTV) / Claremont Community Media Center (CCMC) the proposed operator. Neither board has approved that. The portal footer in the screens says "Operated by", which is the software's default text.
5. **Anthropic.** Segments 3.02 to 3.04 quote the S-1 and say plainly that Anthropic has made no commitment. The filing describes no application process.
6. **The October 7, 2026 minutes** linked in the test response are labeled DRAFT in the knowledge graph, while the invented request asks for approved minutes. It is visible only briefly in the console screen.
7. **Not legal advice.** The end card says so. Counsel has not reviewed the citation list or templates.

## Sources

- RTK Portal `README.md` and build record, October 30, 2026: functions, queue rule, triage outcomes, citation checks, tests (56), review (19 defects), limits
- [RSA 91-A:4](https://gc.nh.gov/rsa/html/VI/91-A/91-A-4.htm), paragraphs I and IV(b)
- Claremont School Board [Policy EH](https://docs.google.com/document/d/1BTHJCvjPSXnX17cOG9MWJ3B9L0lCy88Q/edit), adopted September 17, 2025
- Anthropic, PBC, [Form S-1 registration statement](https://www.sec.gov/Archives/edgar/data/2130357/000162828026067168/anthropicpbc-sx1.htm), filed October 26, 2026, pages 13 and 144
- [kevin-tyson/CSBMN](https://github.com/kevin-tyson/CSBMN), cloned November 13, 2026, for the portal's search index
