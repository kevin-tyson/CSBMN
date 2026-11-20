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

Video version of the Claude Doc "Claude as Mediator of Claremont School District Knowledge: Theory and Appeal to Anthropic"
(https://claude.ai/artifact/JhnEnNf4KaNy7t5kQGQHWs). Built November 14, 2026.
Draft length {int(total//60)}:{int(total%60):02d} at an estimated 156 words a minute; the finished length follows your narration.

## What is in this folder

| Path | What it is |
|---|---|
| `{S.NAME}-DRAFT.mp4` | Timing draft with no voice: narration shown as a caption band, 1920x1080 |
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
""" + "\n".join(rows) + """

3. Each file starts with the tag `[calm, friendly narration]`. If the voice reads it aloud, delete the line and regenerate.
4. Listen for "A-I", "Right-to-Know" and "Tocqueville". If "A-I" comes out wrong, try "A I".
5. Put the files in `audio/` as `part_1.mp3` to `part_4.mp3`, run `python3 align_narration.py`, then `python3 build_video.py` (or send them to Claude to build). To replace one paragraph, save it as `audio/seg_<id>.mp3` and rebuild.

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
""")
(ROOT / "SCRIPT.md").write_text("".join(out))
print("wrote SCRIPT.md and", len(list(EL.glob('*.txt'))), "narration files")
