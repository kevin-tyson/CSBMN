#!/usr/bin/env python3
"""Find where each narration paragraph starts in the ElevenLabs part files.

Runs pocketsphinx speech recognition (bundled US English model) over each part, lines the
recognized words up with the script text, and takes each paragraph's start as the middle of
the pause just before its first matched word. Writes audio/alignment.json, which
build_video.py uses in place of pause-length splitting.  pip install pocketsphinx
"""
import array, difflib, json, re, subprocess, sys
from pathlib import Path
from pocketsphinx import Decoder

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import script_data as S

SPELL = {"r-s-a": "r s a", "e-h": "e h", "a-i": "a i"}
def norm(text):
    t = text.lower()
    for a, b in SPELL.items(): t = t.replace(a, b)
    t = t.replace("twenty-", "twenty ").replace("-", " ")
    return re.findall(r"[a-z']+", t)

def part_file(part):
    for n in (f"part_{part}.mp3", f"Part_{part}.mp3"):
        if (ROOT / "audio" / n).exists(): return ROOT / "audio" / n
    sys.exit(f"missing audio/part_{part}.mp3")

def recognize(mp3):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(mp3), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    dec = Decoder(samprate=16000)
    words = []; sr = 16000
    a = array.array("h", raw); n = len(a); pos = 0
    while pos < n:      # decode in ~20 s windows cut at quiet points so the decoder stays accurate
        end = min(n, pos + 20 * sr)
        if end < n:
            best, bi = None, end
            for i in range(end - 3 * sr, end, 800):
                e = sum(abs(x) for x in a[i:i + 800:8])
                if best is None or e < best: best, bi = e, i
            end = bi
        dec.start_utt(); dec.process_raw(a[pos:end].tobytes(), full_utt=True); dec.end_utt()
        for s in dec.seg():
            w = re.sub(r"\(\d+\)$", "", s.word)
            if w.startswith("<") or w.startswith("["): continue
            words.append((w.lower(), pos / sr + s.start_frame / 100, pos / sr + (s.end_frame + 1) / 100))
        pos = end
    return words

def main():
    narr = [s for s in S.SEGMENTS if s["kind"] == "narr"]
    result = {}
    for part in sorted(S.PARTS):
        f = part_file(part)
        total = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                                     capture_output=True, text=True).stdout)
        segs = [s for s in narr if s["part"] == part]
        script, owner = [], []
        for i, s in enumerate(segs):
            ws = norm(s["text"]); script += ws; owner += [i] * len(ws)
        rec = recognize(f)
        sm = difflib.SequenceMatcher(a=script, b=[w for w, _, _ in rec], autojunk=False)
        match = {}
        for blk in sm.get_matching_blocks():
            for k in range(blk.size): match[blk.a + k] = blk.b + k
        starts = [0.0]
        for i in range(1, len(segs)):
            first = owner.index(i)
            cand = [(j, match[j]) for j in range(first, min(first + 8, len(script))) if j in match and owner[j] == i]
            if not cand:
                sys.exit(f"part {part}: could not place paragraph {segs[i]['id']}; regenerate it as seg_{segs[i]['id']}.mp3")
            j, r = cand[0]
            t_word = rec[r][1] - (j - first) / 2.7       # step back over unmatched leading words
            prev_end = rec[r - 1][2] if r > 0 else 0.0
            starts.append(round((prev_end + t_word) / 2 if j == first and prev_end < t_word else t_word - 0.15, 3))
        bounds = starts + [total]
        for i, s in enumerate(segs):
            result[s["id"]] = [f.name, bounds[i], round(bounds[i + 1] - bounds[i], 3)]
        print(f"part {part}: {len(rec)} words recognized, {len(match) / max(1, len(script)):.0%} of script words matched")
        for i, s in enumerate(segs):
            d = bounds[i + 1] - bounds[i]
            print(f"   {s['id']:5s} start {bounds[i]:6.2f}  {d:5.1f}s  {len(s['text'].split())/d*60:4.0f} wpm")
    (ROOT / "audio" / "alignment.json").write_text(json.dumps(result, indent=1))

if __name__ == "__main__":
    main()
