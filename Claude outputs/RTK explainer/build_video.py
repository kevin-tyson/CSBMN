#!/usr/bin/env python3
"""Build the RTK Portal explainer from script_data.py.

  python3 build_video.py            # uses audio/part_1.mp3 .. part_3.mp3 (ElevenLabs)
  python3 build_video.py --draft    # no audio needed: estimated timing, narration shown as captions
  options: --size 1280x720  (quick look)   --only 2.05,3.02  (re-render only those scenes)

Narration: with audio/alignment.json (written by align_narration.py) each paragraph starts where
speech recognition found it. Without that file, each part is split at its longest pauses.
A file audio/seg_<id>.mp3 replaces that paragraph. Needs ffmpeg/ffprobe.
Writes the video, captions.srt, timeline.csv and chapters.txt.
"""
import argparse, csv, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import script_data as S

ap = argparse.ArgumentParser()
ap.add_argument("--draft", action="store_true")
ap.add_argument("--size", default="1920x1080")
ap.add_argument("--only", default="")
ap.add_argument("--out", default="")
A = ap.parse_args()
W, H = map(int, A.size.split("x")); FPS = S.FPS
BUILD = ROOT / "_build" / f"{W}x{H}{'_draft' if A.draft else ''}"; BUILD.mkdir(parents=True, exist_ok=True)
OUT = Path(A.out) if A.out else ROOT / (f"{S.NAME}-DRAFT.mp4" if A.draft else f"{S.NAME}.mp4")
VENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-r", str(FPS)]
AENC = ["-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit("ffmpeg failed:\n" + " ".join(map(str, cmd)) + "\n" + r.stderr[-2500:])
    return r

def dur(p):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).stdout)

def part_file(part):
    for n in (f"part_{part}.mp3", f"Part_{part}.mp3"):
        if (ROOT / "audio" / n).exists(): return ROOT / "audio" / n
    sys.exit(f"missing audio/part_{part}.mp3 (or run with --draft)")

# ------------------------------------------------------------ narration timing
narr = [s for s in S.SEGMENTS if s["kind"] == "narr"]
audio_for = {}   # id -> (file, start, length)
if A.draft:
    for s in narr:
        audio_for[s["id"]] = (None, 0, round(len(s["text"].split()) / 2.6 + 0.6, 2))
else:
    normed = {}
    for part in sorted(S.PARTS):
        src = part_file(part); dst = BUILD / f"norm_part_{part}.wav"
        if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
            run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-af", "loudnorm=I=-18:TP=-1.5:LRA=11", "-ar", "48000", str(dst)])
        normed[part] = dst
    if (ROOT / "audio" / "alignment.json").exists():
        al = json.loads((ROOT / "audio" / "alignment.json").read_text())
        for s in narr:
            _, st, ln = al[s["id"]]
            audio_for[s["id"]] = (normed[s["part"]], st, ln)
    else:
        for part in sorted(S.PARTS):
            segs = [s for s in narr if s["part"] == part]; f = normed[part]; total = dur(f)
            out = run(["ffmpeg", "-hide_banner", "-i", str(f), "-af", "silencedetect=n=-38dB:d=0.25", "-f", "null", "-"]).stderr
            sil = [(float(a), float(b)) for a, b in zip(re.findall(r"silence_start: ([\d.]+)", out), re.findall(r"silence_end: ([\d.]+)", out))]
            inner = [x for x in sil if x[0] > 0.5 and x[1] < total - 0.3]
            cuts = sorted(sorted(inner, key=lambda x: x[1] - x[0], reverse=True)[:len(segs) - 1])
            if len(cuts) < len(segs) - 1:
                sys.exit(f"part {part}: found {len(cuts)} pauses for {len(segs)} paragraphs; run align_narration.py or add seg_ files")
            bounds = [0.0] + [round((a + b) / 2, 3) for a, b in cuts] + [total]
            for i, s in enumerate(segs):
                audio_for[s["id"]] = (f, bounds[i], round(bounds[i + 1] - bounds[i], 3))
            print(f"part {part}: {len(segs)} paragraphs, {total:.1f}s; pauses used: " + ", ".join(f"{b-a:.2f}" for a, b in cuts))
    for s in narr:
        seg = ROOT / "audio" / f"seg_{s['id']}.mp3"
        if seg.exists(): audio_for[s["id"]] = (seg, 0, round(dur(seg) + 0.35, 3))

# ------------------------------------------------------------ scene renderer
def still_chain(pic, n, push):
    path = ROOT / pic
    if push:
        return (path, f"scale={2*W}:{2*H}:flags=lanczos,zoompan=z='1+0.05*on/{n}':d={n}:s={W}x{H}:fps={FPS}:"
                      f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)',setsar=1")
    return (path, f"scale={W}:{H}:flags=lanczos,setsar=1,loop=-1:1,trim=end_frame={n},setpts=N/{FPS}/TB,fps={FPS}")

def render_pics(pics, total, audio, out, caption=None):
    n_total = round(total * FPS)
    k = len(pics); xf = 0.4 if k > 1 else 0
    each = (total + xf * (k - 1)) / k
    ins, fl = [], []
    for i, p in enumerate(pics):
        name, push = (p.split("|") + [""])[:2]
        path, chain = still_chain(name, round(each * FPS), push == "push")
        ins += ["-framerate", str(FPS), "-i", str(path)]
        fl.append(f"[{i}:v]{chain},format=yuv420p[p{i}]")
    cur = "p0"; off = 0
    for i in range(1, k):
        off += each - xf
        fl.append(f"[{cur}][p{i}]xfade=transition=fade:duration={xf}:offset={off:.3f}[x{i}]"); cur = f"x{i}"
    vi = k
    if caption:
        ins += ["-i", str(caption)]
        fl.append(f"[{vi}:v]scale={W}:{H}[cap];[{cur}][cap]overlay=0:0:format=auto[cv]"); cur = "cv"; vi += 1
    fl.append(f"[{cur}]fade=t=in:st=0:d=0.25,trim=end_frame={n_total},setpts=N/{FPS}/TB,format=yuv420p[v]")
    if audio and audio[0]:
        f, st, ln = audio
        ins += ["-ss", str(st), "-t", str(ln), "-i", str(f)]
        fl.append(f"[{vi}:a]aresample=48000,apad,atrim=0:{total},afade=t=out:st={max(0,total-0.08)}:d=0.08[a]")
    else:
        ins += ["-f", "lavfi", "-t", str(total), "-i", "anullsrc=r=48000:cl=stereo"]
        fl.append(f"[{vi}:a]anull[a]")
    tmp = out.with_name(out.stem + ".tmp.mp4")
    run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(fl), "-map", "[v]", "-map", "[a]",
         *VENC, *AENC, "-t", str(total), str(tmp)])
    tmp.rename(out)

# ------------------------------------------------------------ build
only = set(x for x in A.only.split(",") if x)
files, timeline, srt = [], [], []
t = 0.0
for s in S.SEGMENTS:
    sid = s["id"]; out = BUILD / f"{len(files):03d}_{sid.replace('.', '_')}.mp4"
    redo = not out.exists() or not only or sid in only
    if s["kind"] == "hold":
        if redo: render_pics(s["pics"], s["secs"], None, out)
    else:
        au = audio_for[sid]
        cap = ROOT / "draft_captions" / f"{sid}.png" if A.draft else None
        if redo: render_pics(s["pics"], au[2], au, out, caption=cap)
    d = dur(out)
    timeline.append(dict(id=sid, kind=s["kind"], start=round(t, 2), end=round(t + d, 2), picture=" + ".join(s["pics"])))
    if s["kind"] == "narr": srt.append((t, t + d, s["text"]))
    files.append(out); t += d
    print(f"{sid:7s} {s['kind']:5s} {d:6.2f}s  at {t-d:7.2f}")

lst = BUILD / "concat.txt"
lst.write_text("".join(f"file '{f.name}'\n" for f in files))
tmp = OUT.with_name(OUT.stem + ".tmp.mp4")
run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", "-movflags", "+faststart", str(tmp)])
tmp.rename(OUT)

def ts(x):
    ms = round(x * 1000); return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"
(ROOT / "captions.srt").write_text("".join(f"{i+1}\n{ts(a)} --> {ts(b)}\n{txt}\n\n" for i, (a, b, txt) in enumerate(srt)))
with open(ROOT / "timeline.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(timeline[0])); w.writeheader(); w.writerows(timeline)
ch = []   # YouTube wants the first chapter at 0:00
for part, name in S.PARTS.items():
    first = next(x for x in timeline if x["id"] == f"{part}.01")
    m, sec = divmod(0 if part == 1 else int(first["start"]), 60); ch.append(f"{m}:{sec:02d} {name}")
(ROOT / "chapters.txt").write_text("\n".join(ch) + "\n")
print(f"\n{OUT.name}: {int(t//60)} min {t%60:.0f} s")
