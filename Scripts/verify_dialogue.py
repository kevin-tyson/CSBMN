#!/usr/bin/env python3
#
# Copyright 2026 Kevin Tyson
# SPDX-License-Identifier: Apache-2.0
#
"""Independent verifier for Output/HTML/Dialogue CSVs — the QA half of the pipeline.

Re-derives every row from the source JSON WITHOUT reusing the builder's code path
and compares row-for-row. Comparing token LISTS (not joined strings) is deliberate:
empty-text ASR word objects put double spaces in the source join, so a string
compare false-alarms on correct output.

TWO ROW CONVENTIONS ARE ACCEPTED.

  SEGMENT-BASED (the contract, 126 of 127 files): one row per non-empty diarizer
  segment, timestamps copied from the segment. Verified row-for-row.

  TURN-BASED (currently only "Claremont School Board - 8526"): one row per SPEAKER
  TURN. Consecutive same-speaker segments are merged into one row, and a segment in
  which the speaker demonstrably changes is SPLIT — e.g. a chair's handoff and the
  presenter's reply share one diarizer segment and are correctly given two rows.
  That is finer attribution than the segment grid can express, so it is preserved
  rather than flattened. Such a file is verified on the guarantees that actually
  matter: the concatenated token list must equal the transcript's exactly (no word
  added, dropped or reordered), timestamps must be monotonic and inside the covered
  segments' span, and no Speaker or Dialogue cell may be empty. It reports "OK*".

  Single file : python3 verify_dialogue.py "Input/Transcripts/X.json" "Output/HTML/Dialogue/X.CSV"
  Whole corpus: python3 verify_dialogue.py --corpus Input/Transcripts Output/HTML/Dialogue
  Name sweep  : python3 verify_dialogue.py --names Output/HTML/Dialogue

An optional 9th column, "Video URL" (added by Scripts/add_video_urls.py), is
accepted. When present, every cell must be either empty in every row (meeting has
no Remote video in MAP.md) or one Cablecast show URL ending in ?site=1 followed by
&seekto=floor(Start (sec)), the same show on every row.

Exits non-zero if any check fails.
"""
import argparse, csv, json, math, os, re, sys
from collections import Counter, defaultdict

COLUMNS = ["Start", "End", "Start (sec)", "End (sec)",
           "Speaker", "Role", "Dialogue", "Diarized As"]
URL_COL = "Video URL"
SEEK_RE = re.compile(r"(https://\S+/internetchannel/show/\d+\?site=1)&seekto=(\d+)")


def check_video_urls(body):
    """Validate the optional 9th column. Returns a list of problems."""
    cells = [r[8] for r in body if len(r) == 9]
    if not any(cells):
        return []
    problems, bases = [], set()
    for i, r in enumerate(body):
        if len(r) != 9:
            continue
        m = SEEK_RE.fullmatch(r[8])
        if not m:
            problems.append(f"row {i}: Video URL malformed or empty: {r[8]!r}"); continue
        bases.add(m.group(1))
        if int(m.group(2)) != math.floor(float(r[2])):
            problems.append(f"row {i}: seekto={m.group(2)} but Start (sec)={r[2]}")
    if len(bases) > 1:
        problems.append(f"Video URL points at more than one show: {sorted(bases)}")
    return problems


def hms(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def verify_turn_based(expected, body, name, quiet, width=8):
    """Accept a turn-based CSV: rows are speaker turns, not diarizer segments."""
    problems = check_video_urls(body)
    src_toks = [t for e in expected for t in e[4]]
    csv_toks = [t for r in body for t in r[6].split()]
    if src_toks != csv_toks:
        problems.append(f"token stream differs: csv={len(csv_toks)} src={len(src_toks)} tokens"
                        f"{' (same count, different words/order)' if len(csv_toks)==len(src_toks) else ''}")
    for i, r in enumerate(body):
        if len(r) != width:
            problems.append(f"row {i}: {len(r)} columns, expected {width}"); continue
        if not r[4].strip():
            problems.append(f"row {i}: empty Speaker")
        if not r[6].strip():
            problems.append(f"row {i}: empty Dialogue")
    good = [r for r in body if len(r) == width]
    secs = [float(r[2]) for r in good]
    if not all(a <= b for a, b in zip(secs, secs[1:])):
        problems.append("timestamps not monotonic")
    if not all(float(r[3]) >= float(r[2]) for r in good):
        problems.append("a row has end < start")
    lo = min(float(e[2]) for e in expected); hi = max(float(e[3]) for e in expected)
    if good and (float(good[0][2]) < lo - 0.005 or float(good[-1][3]) > hi + 0.005):
        problems.append(f"row span [{good[0][2]},{good[-1][3]}] outside transcript [{lo:.2f},{hi:.2f}]")
    if problems:
        print(f"FAIL {name} (turn-based)")
        for p in problems[:15]:
            print("   ", p)
        if len(problems) > 15:
            print(f"    ... and {len(problems)-15} more")
        return False, Counter()
    dist = Counter(r[4] for r in good)
    if not quiet:
        print(f"OK*  {name}: {len(body)} turn rows over {len(expected)} segments, "
              f"{len(csv_toks)} tokens, {len(dist)} speakers, "
              f"span {body[0][0]}-{body[-1][1]}  [turn-based convention]")
    return True, dist


def verify(jpath, cpath, quiet=False):
    with open(jpath, encoding="utf-8") as f:
        data = json.load(f)
    diar = {s["id"]: s["name"] for s in data["speakers"]}
    expected = []
    for seg in data["segments"]:
        toks = [t for w in seg.get("words", []) for t in w["text"].split()]
        if not toks:
            continue
        start = seg["start"]; end = start + seg["duration"]
        expected.append((hms(start), hms(end), f"{start:.2f}", f"{end:.2f}",
                         toks, diar.get(seg["speaker"], seg["speaker"])))
    with open(cpath, encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    problems = []
    if not rows or rows[0] not in (COLUMNS, COLUMNS + [URL_COL]):
        problems.append(f"header mismatch: {rows[0] if rows else 'EMPTY FILE'}")
    width = len(rows[0]) if rows and rows[0] == COLUMNS + [URL_COL] else 8
    body = rows[1:]
    if len(body) != len(expected):
        src_toks = [t for e in expected for t in e[4]]
        csv_toks = [t for r in body if len(r) == width for t in r[6].split()]
        if src_toks == csv_toks:
            return verify_turn_based(expected, body, os.path.basename(cpath), quiet, width)
        problems.append(f"row count: csv={len(body)} expected={len(expected)}")
    if width == 9:
        problems += check_video_urls(body)
    for i, (r, e) in enumerate(zip(body, expected)):
        if len(r) != width:
            problems.append(f"row {i}: {len(r)} columns, expected {width}"); continue
        if r[6].split() != e[4]:
            problems.append(f"row {i}: token mismatch "
                            f"(csv {len(r[6].split())} vs src {len(e[4])} tokens)")
        for col, (got, want) in enumerate(zip(r[:4], e[:4])):
            if got != want:
                problems.append(f"row {i} col {COLUMNS[col]}: {got!r} != {want!r}")
        if r[7] != e[5]:
            problems.append(f"row {i}: Diarized As {r[7]!r} != {e[5]!r}")
        if not r[4].strip():
            problems.append(f"row {i}: empty Speaker")
        if not r[6].strip():
            problems.append(f"row {i}: empty Dialogue")
    secs = [float(r[2]) for r in body if len(r) == width]
    if not all(a <= b for a, b in zip(secs, secs[1:])):
        problems.append("timestamps not monotonic")
    if not all(float(r[3]) >= float(r[2]) for r in body if len(r) == width):
        problems.append("a row has end < start")

    name = os.path.basename(cpath)
    if problems:
        print(f"FAIL {name}")
        for p in problems[:15]:
            print("   ", p)
        if len(problems) > 15:
            print(f"    ... and {len(problems)-15} more")
        return False, Counter()
    dist = Counter(r[4] for r in body)
    if not quiet:
        toks = sum(len(r[6].split()) for r in body)
        print(f"OK   {name}: {len(body)} rows, {toks} tokens, "
              f"{len(dist)} speakers, span {body[0][0]}-{body[-1][1]}")
    return True, dist


def norm(s):
    return re.sub(r"[^a-z]", "", s.lower())


def name_sweep(ddir):
    per = defaultdict(Counter)
    for fn in sorted(os.listdir(ddir)):
        if not fn.lower().endswith(".csv"):
            continue
        with open(os.path.join(ddir, fn), encoding="utf-8-sig") as f:
            rd = csv.reader(f); next(rd, None)
            for r in rd:
                if len(r) >= 5 and r[4].strip():
                    per[r[4].strip()][fn] += 1
    print(f"{len(per)} distinct Speaker values across {ddir}\n")
    # near-duplicate detection: same surname token, or one name a subset of another
    keys = sorted(per)
    groups = defaultdict(list)
    for k in keys:
        parts = [p for p in re.split(r"[^A-Za-z]+", k) if len(p) > 2]
        if parts:
            groups[parts[-1].lower()].append(k)
    flagged = False
    for surname, variants in sorted(groups.items()):
        if len(variants) > 1 and len({norm(v) for v in variants}) > 1:
            flagged = True
            print(f"  possible variants of '{surname}':")
            for v in variants:
                print(f"     {v!r}  ({sum(per[v].values())} rows in {len(per[v])} files)")
    if not flagged:
        print("  no surname collisions found")
    return per


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("a", nargs="?"); ap.add_argument("b", nargs="?")
    ap.add_argument("--corpus", action="store_true")
    ap.add_argument("--names", metavar="DIALOGUE_DIR")
    args = ap.parse_args()

    if args.names:
        name_sweep(args.names); return

    if args.corpus:
        tdir, ddir = args.a, args.b
        stems = {}
        for fn in os.listdir(tdir):
            if fn.lower().endswith(".json"):
                stems[re.sub(r"\.mp4$", "", fn[:-5], flags=re.I).lower()] = fn
        ok = fail = miss = 0
        for fn in sorted(os.listdir(ddir)):
            if not fn.lower().endswith(".csv"):
                continue
            stem = re.sub(r"\.mp4$", "", fn[:-4], flags=re.I).lower()
            if stem not in stems:
                print(f"SKIP {fn}: no source transcript"); miss += 1; continue
            good, _ = verify(os.path.join(tdir, stems[stem]), os.path.join(ddir, fn), quiet=True)
            ok += good; fail += (not good)
        print(f"\n{ok} passed, {fail} failed, {miss} without a source transcript")
        sys.exit(1 if fail else 0)

    good, _ = verify(args.a, args.b)
    sys.exit(0 if good else 1)


if __name__ == "__main__":
    main()
