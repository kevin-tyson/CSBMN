#!/usr/bin/env python3
"""Write SCRIPT.md and the ElevenLabs narration files from script_data.py."""
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import script_data as S

EL = ROOT / "ElevenLabs narration"; EL.mkdir(exist_ok=True)
narr = [s for s in S.SEGMENTS if s["kind"] == "narr"]
TAG = "[calm, friendly narration]\n\n"
rows = []
for part, name in S.PARTS.items():
    segs = [s for s in narr if s["part"] == part]
    body = "\n\n".join(s["text"] for s in segs)
    (EL / f"part_{part}.txt").write_text(TAG + body + "\n")
    rows.append(f"| {part} | {name} | {len(body):,} | {len(body.split())} | {len(segs)} | `audio/part_{part}.mp3` |")
for s in narr:
    (EL / f"retake_{s['id']}.txt").write_text(TAG + s["text"] + "\n")

tl = {}
if (ROOT / "timeline.csv").exists():
    tl = {r["id"]: r for r in csv.DictReader(open(ROOT / "timeline.csv"))}
total = float(list(tl.values())[-1]["end"]) if tl else 0
words = sum(len(s["text"].split()) for s in narr)
def pics(s): return "; then ".join("`%s`%s" % (p.split("|")[0], " with a slow push-in" if p.endswith("|push") else "") for p in s["pics"])

out = [f"""# {S.TITLE}: explainer video script

{S.SUBTITLE}. Built November 20, 2026, the day the skill was created.
Finished length {int(total//60)}:{int(total%60):02d} ({words} words of narration), built November 20, 2026 from the ElevenLabs audio in `audio/`.

## What is in this folder

| Path | What it is |
|---|---|
| `{S.NAME}.mp4` | The finished video, 1920x1080, narration loudness-normalized to -18 LUFS |
| `{S.NAME}-DRAFT.mp4` | Earlier timing draft with no voice: narration shown as a caption band |
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
""" + "\n".join(rows) + """

3. Each file starts with the tag `[calm, friendly narration]`. If the voice reads it aloud, delete the line and regenerate.
4. Listen for the letter-by-letter names: "C-S-B policy query", "J-I-C-J", "J-I-C-A-B" and "B-B-B". If the voice runs letters together, try spaces ("J I C J").
5. Put the files in `audio/` as `part_1.mp3` to `part_3.mp3`, run `python3 align_narration.py`, then `python3 build_video.py` (or send them to Claude to build). To replace one paragraph, save it as `audio/seg_<id>.mp3` and rebuild.

## Running order

Narration is exactly what ElevenLabs reads.
"""]
part = 0
for s in S.SEGMENTS:
    if s["kind"] == "hold":
        out.append(f"\n**{s['id']} · hold {s['secs']:.1f} s, silent** {pics(s)}\n")
        continue
    if s["part"] != part:
        part = s["part"]; out.append(f"\n### Part {part}: {S.PARTS[part]}\n")
    out.append(f"\n**{s['id']}** {s['text']}\n\n> Picture: {pics(s)}\n")
out.append("""
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
""")
(ROOT / "SCRIPT.md").write_text("".join(out))
print("wrote SCRIPT.md and", len(list(EL.glob('*.txt'))), "narration files")
