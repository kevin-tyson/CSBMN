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
def pics(s): return "; then ".join("`%s`%s" % (p.split("|")[0], " with a slow push-in" if p.endswith("|push") else "") for p in s["pics"])

out = [f"""# {S.TITLE}: explainer video script

Companion to the briefing deck for the Claremont School Board and Administration. Built November 13, 2026.
Draft length {int(total//60)}:{int(total%60):02d} at an estimated 156 words a minute; the finished length follows your narration.

## What is in this folder

| Path | What it is |
|---|---|
| `{S.NAME}-DRAFT.mp4` | Timing draft with no voice: narration shown as a caption band, 1920x1080 |
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
""" + "\n".join(rows) + """

3. Each file starts with the tag `[calm, friendly narration]`. If the voice reads it aloud, delete the line and regenerate.
4. Listen for "R-S-A ninety-one A", "Policy E-H" and "A-I". If one comes out wrong, try spaces instead of hyphens.
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
""")
(ROOT / "SCRIPT.md").write_text("".join(out))
print("wrote SCRIPT.md and", len(list(EL.glob('*.txt'))), "narration files")
