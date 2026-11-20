# Asking Claude About Claremont School Board Policy: explainer video script

How to install and use the csb-policy-query skill. Built November 20, 2026, the day the skill was created.
Finished length 4:03 (648 words of narration), built November 20, 2026 from the ElevenLabs audio in `audio/`.

## What is in this folder

| Path | What it is |
|---|---|
| `Policy-query-explainer.mp4` | The finished video, 1920x1080, narration loudness-normalized to -18 LUFS |
| `Policy-query-explainer-DRAFT.mp4` | Earlier timing draft with no voice: narration shown as a caption band |
| `audio/` | `part_1.mp3` to `part_3.mp3` from ElevenLabs, and `alignment.json` (where each paragraph starts) |
| `captions.srt`, `chapters.txt` | Captions and YouTube chapter times for upload |
| `csb-policy-query.zip` | The skill itself, ready to upload (one folder, one `SKILL.md`); identical to the copy saved in your Claude account |
| `ElevenLabs narration/part_1.txt` to `part_3.txt` | The three blocks to paste into ElevenLabs, one generation each; `retake_<id>.txt` holds one paragraph |
| `SCRIPT.md` | This file: narration and picture for every segment |
| `script_data.py` | Single source for narration and pictures; edit here and rebuild |
| `build_video.py` | Builds the cut; writes `captions.srt`, `timeline.csv` and `chapters.txt` (same builder as the Mediation explainer) |
| `align_narration.py` | Finds each paragraph's start in your audio (speech recognition) |
| `cards/` | 19 cards drawn at 2x |
| `draft_captions/` | The caption bands used only in the draft |
| `_source/` | `make_cards.py`, `_css.py` (shared palette), `make_docs.py` |

## Generating the narration in ElevenLabs

1. Model **Eleven v4**, one voice for all three parts (the voice from the earlier explainers, if you want them to match).
2. Paste one file per generation:

| Part | Covers | Characters | Words | Paragraphs | Save as |
|---|---|---|---|---|---|
| 1 | What the skill does | 873 | 153 | 4 | `audio/part_1.mp3` |
| 2 | Installing it | 986 | 173 | 3 | `audio/part_2.mp3` |
| 3 | Using it | 1,923 | 322 | 8 | `audio/part_3.mp3` |

3. Each file starts with the tag `[calm, friendly narration]`. If the voice reads it aloud, delete the line and regenerate.
4. Listen for the letter-by-letter names: "C-S-B policy query", "J-I-C-J", "J-I-C-A-B" and "B-B-B". If the voice runs letters together, try spaces ("J I C J").
5. Put the files in `audio/` as `part_1.mp3` to `part_3.mp3`, run `python3 align_narration.py`, then `python3 build_video.py` (or send them to Claude to build). To replace one paragraph, save it as `audio/seg_<id>.mp3` and rebuild.

## Running order

Narration is exactly what ElevenLabs reads.

**T0 · hold 4.0 s, silent** `cards/title.png`

### Part 1: What the skill does

**1.01** This video shows how to install and use a skill for Claude called C-S-B policy query. A skill is a set of written instructions that Claude follows for one kind of task. This one answers questions about Claremont School Board policy.

> Picture: `cards/title.png`; then `cards/what.png`

**1.02** The district publishes its policies through one Google document: an index with about three hundred fifty links, in twelve sections lettered A through L. Each link opens a policy, a regulation, or a form.

> Picture: `cards/index.png` with a slow push-in

**1.03** The skill answers from that index and the documents it links, and nothing else. It does not use news, meeting minutes, or what Claude already knows about New Hampshire law. When a policy cites a statute, the answer says so, but it does not say what the statute requires.

> Picture: `cards/scope.png`

**1.04** Every statement in an answer names the policy behind it, with a link. And when the policies do not answer the question, the reply is two words: Insufficient Data.

> Picture: `cards/promise.png`

### Part 2: Installing it

**2.01** Installing it takes three steps. First, skills need code execution. On a Free, Pro or Max plan, open Settings, then Capabilities, and turn on Code execution and file creation. Newer versions of the settings page call it Create and edit files. On a Team or Enterprise plan, an owner has to allow skills for the organization first.

> Picture: `cards/step1.png`

**2.02** Second, upload the skill. It comes as a zip file holding one folder with one instruction file. In Claude, open Customize, then Skills. Click the plus button, choose Create skill, then Upload a skill, and pick the zip file. The skill appears in your list with a switch. Make sure it is on. A skill you upload is private to your account.

> Picture: `cards/step2.png`

**2.03** Third, connect Google Drive, because the policies live there. Open Customize, then Connectors, find Google Drive, choose Connect, and sign in with your Google account. Claude can open only the files that account can open. The index is shared with anyone who has the link, and so are the policies tested for this video.

> Picture: `cards/step3.png`

### Part 3: Using it

**3.01** To use it, ask a question about school board policy in plain words. Claude picks the skill on its own when a question fits. Here are two real questions, asked on November twentieth, twenty twenty-six.

> Picture: `cards/ask.png`

**3.02** The first: may students use their cell phones during lunch? Claude reads the index fresh, lists every entry, and looks for titles about phones, devices and lunch. It also searches Google Drive, and keeps only files the index links. Then it reads the strongest matches.

> Picture: `cards/flow.png`; then `cards/flow_q1.png`

**3.03** The answer is no. Policy J-I-C-J, Unauthorized Communication Devices, adopted in September twenty twenty-five, bars student use of personal devices from the first bell to the dismissal bell. It says the school day includes lunch periods, passing time and recesses. It also lists exceptions for medical needs, disabilities and language access.

> Picture: `cards/answer1.png`; then `cards/jicj_text.png` with a slow push-in

**3.04** The answer also reports an older policy that is still in the index. J-I-C-A-B, from twenty ten, says permitted uses of electronic devices will be set out in the student and parent handbooks. Neither policy says it replaces the other, so the skill shows both, with their dates.

> Picture: `cards/overlap.png`

**3.05** The second question: how many votes did each candidate get in the March twenty twenty-six school board election? The skill read policy B-B-B, on board membership and elections. It says board members are elected each March for three-year terms. It gives no results. The Drive search also turned up meeting minutes and an agenda, but those are not policies, so the skill set them aside.

> Picture: `cards/q2.png`

**3.06** So the reply is: Insufficient Data. That tells you the answer is not in board policy, and you need another source, such as the election results.

> Picture: `cards/answer2.png`

**3.07** Two more cases. If the policies answer only part of a question, the skill answers that part and marks the rest Insufficient Data. If a policy cannot be opened, it says which one, instead.

> Picture: `cards/cases.png`

**3.08** One source. A policy behind every statement. Two words when the policies are silent. Thank you for watching.

> Picture: `cards/closing.png`

**END · hold 5.0 s, silent** `cards/end.png`

## The two demo answers, as produced

Both questions were run through the skill on November 20, 2026, against the index as read that day.

**Question 1.** May students use their cell phones during lunch at Claremont schools?

> No. Policy JICJ prohibits student use of personal communication devices "from when the first bell rings to start instructional time until the dismissal bell rings to end the academic school day," and states: "The school day includes lunch periods, passing time, and recesses." (Policy JICJ, Unauthorized Communication Devices, Section J, index date 9/17/2025, section B "Restrictions")
>
> Students with medical needs, students with disabilities whose IEP or Section 504 plan requires a device, and multilingual students with language access services are exempt, and the superintendent or a designee may approve other exceptions case by case or through the student handbook. (JICJ, section C "Exceptions")
>
> The index also lists Policy JICAB, Electronic Communication/Recording Devices (index date 11/17/2010; adopted November 17, 2010), which states: "Permissible uses of electronic devices will be detailed in the School Board approved – Student / Parent Handbooks annually." Neither policy says it replaces the other; both are listed in the index. (Policy JICAB, Section J)
>
> Policy JECCA, High School Lunch (index date 9/2/2015), covers where students eat lunch and does not mention devices.

Candidates by title: JICJ, JICAB, JECCA, JIC, EDCA (employees), EFAA (meal charges). Read: JICJ, JICAB, JECCA. The Drive full-text search for "cellphones" returned nothing.

**Question 2.** How many votes did each candidate get in the March 2026 school board election?

> Insufficient Data.

Read: BBB Board Membership-Elections (index date 6/2/2004), which sets an odd number of members, elected at the annual District elections in March, for three-year terms. The Drive search for "election results" returned meeting minutes and an agenda from the same shared drive; the index does not link them, so they were set aside.

## Before you publish

1. **Install steps.** Segments 2.01 to 2.03 follow the Claude Help Center article "Use skills in Claude" and the Google Drive connector page as of November 20, 2026. Menu names have changed before ("Create and edit files" is the newer name for "Code execution and file creation"). Click through once on your own account before publishing.
2. **Access for other people.** The index, JICJ and BBB are set to "anyone with the link" (Drive metadata, November 20, 2026). The skill has been run only from your Google account. Before telling residents it works for them, have someone run one question from a different Google account. Segment 2.03 says only "the policies tested for this video" for this reason.
3. **JICAB.** The connector returned only the handbook sentence and the adoption dates for JICAB. Open the original document to confirm nothing else is in it (a header or table the connector skipped), since segment 3.04 rests on it.
4. **The skill names you.** Its instructions say "Kevin's question" and point to an optional cache folder on your computer. For other users that step is skipped and nothing breaks, but you may want a public edition that says "the user's question". If you change it, rebuild `csb-policy-query.zip`.
5. **Answers age.** The demo answers are true for the index of November 20, 2026. JICJ section E calls for an annual review, with recommendations to the Board by its second meeting in April, so recheck question 1 if you publish after that.
6. **Not legal advice.** The end card says so.

## Sources

- [Claremont School Board Policies index](https://docs.google.com/document/d/1JmygIGNaVc8ZfaQWtoIA25tRaBGw2Oh5k5ARsGlreqg/edit?tab=t.0#heading=h.gjdgxs), read November 20, 2026 (350 links in Sections A to L)
- [Policy JICJ](https://docs.google.com/document/d/1n6QOnsGVuLCzqfzxF5mo_MhWpxHVqgPC/edit), [Policy JICAB](https://drive.google.com/open?id=1BLnwk3-g85v6AioXGJyAySeVCFHz6tYWPuMkPWRj6ig), [Policy JECCA](https://drive.google.com/open?id=1ZDW7pAdyGY4PO-34ea2Hfs9pxm6hE60k2BlSK1DiBAY), [Policy BBB](https://drive.google.com/open?id=16V7Rld_jMzzolvZdwS_ZLT5NhyxHZAO7Wh4rxX1vbMc)
- Claude Help Center, [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills)
- Claude documentation, [Google Drive connector](https://claude.com/docs/connectors/google/drive)
