#!/usr/bin/env python3
#
# Copyright 2026 Kevin Tyson
# SPDX-License-Identifier: Apache-2.0
#
"""Add or refresh the "Video URL" column of the dialogue CSVs.

Each row gets the meeting's Cablecast `Remote video:` URL from MAP.md, verbatim,
with `&seekto={seconds}` appended, where seconds = floor(Start (sec)). That is the
same integer the meeting pages render as H:MM:SS, so a CSV cell and the page link
for the same row are identical (project convention, Kevin 2026-08-19; Cablecast
does not publicly document seekto).

The URL is plain text (no HTML escaping: `&`, not `&amp;`). The column is appended
as the 9th and last column so every reader that indexes columns 0-7 or reads by
name keeps working.

A CSV is matched to MAP.md by the `dialogue:` path in its section, compared on the
file's base name (case-insensitive). If the section has no `Remote video:` line,
or no section names the CSV, the cells are left EMPTY: a show ID is never guessed
from a file-name prefix or borrowed from another meeting. When MAP.md links the
right show somewhere other than a `dialogue:` line (an excerpt or duplicate
recording mentioned in a note), pass it explicitly with --url "NAME.CSV=URL"
after confirming the CSV's timeline matches that show.

Idempotent: an existing "Video URL" column is recomputed, never duplicated. The
first eight columns are rewritten byte-for-byte unchanged (checked before saving).

  python3 Scripts/add_video_urls.py Input/SupportingDocuments/MAP.md Output/HTML/Dialogue
  python3 Scripts/add_video_urls.py MAP.md Output/HTML/Dialogue --only "X.mp4.CSV" [--dry-run]
"""
import argparse, csv, io, math, os, re, sys

BASE = ["Start", "End", "Start (sec)", "End (sec)",
        "Speaker", "Role", "Dialogue", "Diarized As"]
COL = "Video URL"
URL_RE = re.compile(r"Remote video:\s*\[[^\]]*\]\((https://[^)\s]+/internetchannel/show/\d+\?site=1)\)")
SHOW_RE = re.compile(r"\]\((https://[^)\s]+/internetchannel/show/(\d+)\?site=1)\)")
DLG_RE = re.compile(r"dialogue:\s*`([^`]+\.csv)`", re.I)


def map_urls(map_path):
    """basename(lower) -> URL or None, from each '## ' section of MAP.md.

    One linked show in the section: every CSV named there gets it. Several shows
    (e.g. 9/2/26: two handbook excerpts plus the full meeting): each CSV gets the
    show whose id equals its file-name prefix, and None if no linked show matches.
    The prefix only selects among links MAP.md already gives; it never creates one."""
    text = open(map_path, encoding="utf-8").read()
    out, conflicts = {}, []
    for sec in re.split(r"(?m)^## ", text)[1:]:
        if not URL_RE.search(sec):
            shows = {}
        else:
            shows = {sid: u for u, sid in SHOW_RE.findall(sec)}
        for d in DLG_RE.findall(sec):
            key = os.path.basename(d).lower()
            if len(shows) == 1:
                url = next(iter(shows.values()))
            else:
                m = re.match(r"(\d+)\s", os.path.basename(d))
                url = shows.get(m.group(1)) if m else None
            if key in out and out[key] != url:
                conflicts.append((key, [out[key], url]))
            out[key] = url
    return out, conflicts


def seekto(url, start_sec):
    return f"{url}&seekto={math.floor(float(start_sec))}"


def process(path, url, dry):
    raw = open(path, "rb").read()
    text = raw.decode("utf-8-sig")
    newline = "\r\n" if "\r\n" in text else "\n"
    rows = list(csv.reader(io.StringIO(text, newline="")))
    if not rows or rows[0][:8] != BASE or rows[0][8:] not in ([], [COL]):
        return f"SKIP (unexpected header {rows[0] if rows else 'EMPTY'})"
    width = len(rows[0])
    new = [BASE + [COL]]
    for i, r in enumerate(rows[1:], 1):
        if len(r) != width:
            return f"SKIP (row {i} has {len(r)} columns, header has {width})"
        new.append(r[:8] + [seekto(url, r[2]) if url else ""])
    buf = io.StringIO(newline="")
    csv.writer(buf, lineterminator=newline).writerows(new)
    # guard: first eight columns unchanged
    back = list(csv.reader(io.StringIO(buf.getvalue(), newline="")))
    if [r[:8] for r in back] != [r[:8] for r in rows]:
        return "SKIP (round-trip changed existing columns)"
    if not dry:
        with open(path, "wb") as f:
            f.write(("﻿" if raw.startswith(b"\xef\xbb\xbf") else "").encode() + buf.getvalue().encode("utf-8"))
    return "ok" if url else "ok (no Remote video in MAP.md: column left empty)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("map"); ap.add_argument("dialogue_dir")
    ap.add_argument("--only", action="append", help="process just this CSV file name (repeatable)")
    ap.add_argument("--url", action="append", default=[], metavar="NAME.CSV=URL",
                    help="explicit Remote video URL for a CSV that MAP.md does not name on a dialogue: line")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    urls, conflicts = map_urls(a.map)
    for spec in a.url:
        name, _, u = spec.partition("=")
        if not re.fullmatch(r"https://[^\s]+/internetchannel/show/\d+\?site=1", u):
            sys.exit(f"ERROR: --url {spec!r} is not a Cablecast show URL ending in ?site=1")
        urls[name.lower()] = u
    for c in conflicts:
        print("CONFLICT", c)
    names = a.only or sorted(f for f in os.listdir(a.dialogue_dir) if f.lower().endswith(".csv"))
    tally = {}
    for fn in names:
        key = fn.lower()
        url = urls.get(key)
        status = process(os.path.join(a.dialogue_dir, fn), url, a.dry_run) if key in urls \
            else process(os.path.join(a.dialogue_dir, fn), None, a.dry_run).replace(
                "no Remote video in MAP.md", "CSV not named in MAP.md")
        tally[status] = tally.get(status, 0) + 1
        if status != "ok":
            print(f"{status}: {fn}")
    print({k: v for k, v in tally.items()})
    sys.exit(1 if conflicts or any(k.startswith("SKIP") for k in tally) else 0)


if __name__ == "__main__":
    main()
