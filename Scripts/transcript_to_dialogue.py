#!/usr/bin/env python3
#
# Copyright 2026 Kevin Tyson
# SPDX-License-Identifier: Apache-2.0
#
"""Deterministic half of the transcript-to-dialogue skill — PATCHED for this project.

Differences from the stock skill script (both were needed on every Claremont JSON):

1. TOKEN parity, not word-object parity. These transcripts contain empty-text ASR
   word objects; the stock check counts word objects and exits 1 on a correct CSV.
   This version counts whitespace tokens of the source word texts.
2. Per-segment overrides. Add "__overrides__" to speakers.json to reassign single
   segments where the diarizer merged voices, flapped mid-sentence, or absorbed a
   chair's recognition into the next speaker's onset:

     {"Speaker 1": {"name": "Jane Doe", "role": "Board Chair"},
      "__overrides__": {"68": {"name": "Tim Broadrick", "role": "Superintendent"},
                        "140": {"name": "Tim Broadrick"}}}

   Indices are the 0-based [idx] numbers printed by --dump-text, counted over ALL
   segments including zero-word ones. A role may be omitted; it is then inherited
   from any label mapping carrying the same name. The build FAILS if a declared
   override never applies (stale index, or an index pointing at a dropped
   zero-word segment) — that catches off-by-one edits.

The "Diarized As" column always keeps the ORIGINAL cluster label, so an override
never hides what the diarizer actually produced.

Modes:
  python3 transcript_to_dialogue.py "<t>.json" --dump-text working.txt [--scan-names "a,b"]
  python3 transcript_to_dialogue.py "<t>.json" --speakers speakers.json --out "<t>.CSV"
"""
import argparse
import csv
import json
import sys
from collections import Counter

COLUMNS = ["Start", "End", "Start (sec)", "End (sec)",
           "Speaker", "Role", "Dialogue", "Diarized As"]


def load(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    diar = {s["id"]: s["name"] for s in data["speakers"]}
    return data, diar


def seg_text(seg):
    return " ".join(w["text"] for w in seg.get("words", [])).strip()


def seg_tokens(seg):
    """Source-of-truth token list for a segment (survives empty-text word objects)."""
    return [t for w in seg.get("words", []) for t in w["text"].split()]


def hms(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def dump_text(data, diar, out_path, scan_names=None):
    segs = data["segments"]
    lines, empties = [], []
    for i, seg in enumerate(segs):
        text = seg_text(seg)
        start = seg["start"]
        end = start + seg["duration"]
        label = diar.get(seg["speaker"], seg["speaker"])
        if not text:
            empties.append((i, label, round(start, 2)))
        lines.append(f"[{i:03d}] {start:8.2f}-{end:8.2f} {label}: {text}")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"working transcript: {out_path} ({len(segs)} segments)")

    counts = Counter(diar.get(s["speaker"], s["speaker"]) for s in segs)
    total = sum(s["duration"] for s in segs)
    print(f"speech duration: {total/60:.1f} min; diarized voices: {len(data['speakers'])}")
    print("segments per diarized label:", dict(counts.most_common()))
    if empties:
        print(f"zero-word segments (dropped from the CSV, but still counted in [idx]): {empties}")

    if scan_names:
        targets = {n.strip().lower() for n in scan_names.split(",") if n.strip()}
        print("\nname-mention scan (segment, label, time, word, ASR confidence):")
        hits = 0
        for i, seg in enumerate(segs):
            label = diar.get(seg["speaker"], seg["speaker"])
            for w in seg.get("words", []):
                if w["text"].strip(".,?!:;").lower() in targets:
                    print(f"  [{i:03d}] {label:12s} {w['start']:8.2f} {w['text']!r} "
                          f"conf={w.get('confidence', 1):.2f}")
                    hits += 1
        if not hits:
            print("  (no mentions found)")


def build_csv(data, diar, speakers_path, out_path):
    with open(speakers_path, encoding="utf-8") as f:
        mapping = json.load(f)
    overrides = mapping.pop("__overrides__", {}) or {}

    segs = data["segments"]
    labels_in_use = {diar.get(s["speaker"], s["speaker"]) for s in segs}
    unmapped = sorted(labels_in_use - set(mapping))
    if unmapped:
        sys.exit(f"ERROR: speakers file is missing labels {unmapped}. Map every diarized "
                 f"label (use the announced/roll-call name with a caveat in 'role' if the "
                 f"person cannot be verified).")
    bad = sorted(k for k, v in mapping.items()
                 if not isinstance(v, dict) or not str(v.get("name", "")).strip())
    if bad:
        sys.exit(f"ERROR: speakers entries {bad} need at least a non-empty 'name'.")

    role_by_name = {}
    for v in mapping.values():
        role_by_name.setdefault(str(v["name"]).strip(), v.get("role", ""))

    try:
        ov = {int(k): v for k, v in overrides.items()}
    except ValueError:
        sys.exit("ERROR: __overrides__ keys must be integer segment indices (as strings).")
    for i, v in ov.items():
        if not isinstance(v, dict) or not str(v.get("name", "")).strip():
            sys.exit(f"ERROR: __overrides__ entry {i} needs a non-empty 'name'.")
        if not 0 <= i < len(segs):
            sys.exit(f"ERROR: __overrides__ index {i} is out of range (0-{len(segs)-1}).")

    rows, dropped, applied = [], 0, set()
    for i, seg in enumerate(segs):
        text = seg_text(seg)
        if not text:
            dropped += 1
            continue
        start = seg["start"]
        end = start + seg["duration"]
        label = diar.get(seg["speaker"], seg["speaker"])
        who = mapping[label]
        name, role = who["name"], who.get("role", "")
        if i in ov:
            name = str(ov[i]["name"]).strip()
            role = ov[i].get("role", role_by_name.get(name, ""))
            applied.add(i)
        rows.append([hms(start), hms(end), f"{start:.2f}", f"{end:.2f}",
                     name, role, text, label])

    stale = sorted(set(ov) - applied)
    if stale:
        sys.exit(f"ERROR: __overrides__ indices {stale} never applied — they point at "
                 f"zero-word segments that get dropped, or the indices are stale. Re-read "
                 f"--dump-text and fix them; do not delete the check.")
    if not rows:
        sys.exit("ERROR: transcript contains no non-empty segments; nothing to write.")

    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(COLUMNS)
        w.writerows(rows)

    problems = []
    src_tokens = sum(len(seg_tokens(s)) for s in segs if seg_text(s))
    csv_tokens = sum(len(r[6].split()) for r in rows)
    if src_tokens != csv_tokens:
        problems.append(f"token parity FAILED: source={src_tokens} csv={csv_tokens}")
    starts = [float(r[2]) for r in rows]
    if not all(a <= b for a, b in zip(starts, starts[1:])):
        problems.append("timestamps not monotonic")
    if not all(float(r[3]) >= float(r[2]) for r in rows):
        problems.append("a row has end < start")
    if any(not r[6].strip() for r in rows):
        problems.append("empty dialogue cell")

    print(f"wrote {out_path}: {len(rows)} rows ({dropped} zero-word segments dropped, "
          f"{len(applied)} overrides applied), span {rows[0][0]} - {rows[-1][1]}")
    print("speaker distribution:", dict(Counter(r[4] for r in rows).most_common()))
    if problems:
        for p in problems:
            print("CHECK FAILED:", p)
        sys.exit(1)
    print(f"integrity checks passed: token parity ({src_tokens} tokens), monotonic "
          f"timestamps, end>=start, no empty cells")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("transcript")
    ap.add_argument("--dump-text", metavar="TXT")
    ap.add_argument("--scan-names", metavar="CSV_NAMES")
    ap.add_argument("--speakers", metavar="JSON")
    ap.add_argument("--out", metavar="CSV")
    args = ap.parse_args()

    data, diar = load(args.transcript)
    if args.dump_text:
        dump_text(data, diar, args.dump_text, args.scan_names)
    if args.speakers or args.out:
        if not (args.speakers and args.out):
            sys.exit("ERROR: --speakers and --out must be used together")
        build_csv(data, diar, args.speakers, args.out)
    if not args.dump_text and not args.out:
        sys.exit("Nothing to do: pass --dump-text and/or --speakers/--out")


if __name__ == "__main__":
    main()
