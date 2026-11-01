#!/bin/bash
#
# Copyright 2026 Kevin Tyson
# SPDX-License-Identifier: Apache-2.0
#
# ---------------------------------------------------------------------------
# download_missing_videos.sh - fetch every meeting recording that
# Input/SupportingDocuments/MAP.md names under Input/Videos but that is not
# on disk, from Claremont Community Television (CCTV) / Claremont Community
# Media Center (CCMC) Cablecast, saving each one under the exact file name
# MAP.md already uses. MAP.md needs no edit afterwards.
#
# Run it on the Mac itself, in Terminal. reflect-claremont.cablecast.tv
# answers HTTP 403 to the Cowork/Claude sandboxes (they sit behind an egress
# allowlist proxy); a normal Terminal.app process on the Mac reaches it.
#
#     cd "/Volumes/BigData/Cowork Projects/Government Transparency Project"
#     bash Scripts/download_missing_videos.sh --dry-run
#
# The dry run fetches no video. It lists each missing file with its Cablecast
# show id, event date, size and source URL, then prints the total and the
# free space on the volume. The real run is the same command without
# --dry-run.
#
# HOW "MISSING" IS DECIDED
# ---------------------------------------------------------------------------
#   - Every "Video:" line in MAP.md whose first backticked path is
#     `Input/Videos/<file>` is a wanted file. Lines that say there is no local
#     copy (no recording on Cablecast) are ignored.
#   - The show id is the file name's numeric prefix ("7313 SchoolBoard012115.mp4"
#     -> 7313). Six mid-2026 files have no prefix ("Claremont School Board
#     72126.mp4"); for those the id comes from the line's first
#     internetchannel/show/<id> link.
#   - A wanted file counts as present if that exact name exists in
#     Input/Videos, or if any other finished file there starts with
#     "<id> " (a recording saved under a different title is not fetched twice).
#     A leftover "<file>.part" is a partial download and is resumed.
#
# WHERE THE VIDEO LINKS COME FROM (checked live 2026-10-29)
# ---------------------------------------------------------------------------
#   - /CablecastAPI/v1/shows?site=1&search=<term>&page_size=5000&include=vod
#     returns each show with its vod ids and, in "vods", the file URL. Six
#     terms resolved 308 of the 311 missing shows on 2026-10-29.
#   - /CablecastAPI/v1/shows/<id>?site=1&include=vod resolves the rest one
#     show at a time (10624 and 10649, the 2019 special school district
#     meetings, and 16408, the 3/17/25 school safety discussion).
#   - Every one of the 311 resolved to a progressive .mp4 (plain resumable
#     curl). The API lists one video file per show, so there is no quality
#     choice to make; some older shows only have a "...-Low.mp4" encode.
#     A HEAD request answered for all 311. Total on 2026-10-29: 661.9 GB (161 GB for
#     2015-2020, 202 GB for 2021-2023, 299 GB for 2024-2026). If Cablecast
#     ever hands back an HLS .m3u8 instead, the script remuxes it with
#     ffmpeg (-c copy, no re-encode) and skips it if ffmpeg is not installed
#     (brew install ffmpeg).
#
# SAFETY
# ---------------------------------------------------------------------------
#   - Downloads go to "<file>.part" and are renamed only once the size matches
#     the server's Content-Length (or, if the server gave none, once the file
#     is over 1 MB). Ctrl-C is safe; re-run and each .part resumes (curl -C -).
#   - Before each download the script checks free space on the volume and
#     stops if the file would leave less than MIN_FREE_GB free.
#   - Nothing in the project outside Input/Videos is written except the log,
#     Scripts/download_missing_videos.log. The only files ever deleted are a
#     .part larger than the server's copy (it cannot be resumed) and a failed
#     ffmpeg remux.
#
# OPTIONS
# ---------------------------------------------------------------------------
#   --dry-run          list what would be fetched, with sizes; fetch nothing
#   --no-sizes         skip the per-file size check (faster dry run, and the
#                      real run then verifies only the 1 MB floor)
#   --limit N          stop after N successful downloads
#   --oldest           oldest meetings first (default: newest first)
#   --since YYYY-MM-DD only meetings on or after this date (Cablecast eventDate)
#   --until YYYY-MM-DD only meetings on or before this date
#   --ids "7313 7408"  only these show ids
#   -h, --help         print this header
#
# Examples
#   bash Scripts/download_missing_videos.sh --dry-run
#   bash Scripts/download_missing_videos.sh --since 2024-01-01
#   bash Scripts/download_missing_videos.sh --oldest --limit 20
#   bash Scripts/download_missing_videos.sh --ids "17594 17575"
#
# New meetings that MAP.md does not list yet are not this script's job:
# download_untranscribed_videos.sh finds and fetches those.
# ---------------------------------------------------------------------------
set -uo pipefail

BASE_SITE="${CABLECAST_BASE:-https://reflect-claremont.cablecast.tv}"
SITE_ID=1
SEARCH_TERMS="School Board|SAU|Finance Committee|Budget|Deliberative|Committee"
MIN_FREE_GB=20
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MAP="$ROOT/Input/SupportingDocuments/MAP.md"
VIDEOS="$ROOT/Input/Videos"
LOG="$ROOT/Scripts/download_missing_videos.log"

DRY=0; SIZES=1; LIMIT=0; ORDER=newest; SINCE=""; UNTIL=""; ONLY_IDS=""
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run)  DRY=1 ;;
    --no-sizes) SIZES=0 ;;
    --limit)    shift; LIMIT="${1:-0}" ;;
    --oldest)   ORDER=oldest ;;
    --since)    shift; SINCE="${1:-}" ;;
    --until)    shift; UNTIL="${1:-}" ;;
    --ids)      shift; ONLY_IDS="${1:-}" ;;
    -h|--help)  awk 'NR > 1 && !/^#/ { exit } NR > 1' "$0"; exit 0 ;;
    *) echo "unknown option: $1 (try --help)" >&2; exit 2 ;;
  esac
  shift
done
case "$LIMIT" in ''|*[!0-9]*) echo "--limit needs a whole number" >&2; exit 2 ;; esac
for d in "$SINCE" "$UNTIL"; do
  [ -z "$d" ] && continue
  printf '%s' "$d" | grep -Eq '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' || { echo "dates must be YYYY-MM-DD (got $d)" >&2; exit 2; }
done

[ -f "$MAP" ]    || { echo "MAP.md not found at $MAP" >&2; exit 1; }
[ -d "$VIDEOS" ] || { echo "Input/Videos not found at $VIDEOS" >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "python3 is required but was not found on PATH" >&2; exit 1; }
command -v curl    >/dev/null 2>&1 || { echo "curl is required but was not found on PATH" >&2; exit 1; }
HAVE_FFMPEG=0; command -v ffmpeg >/dev/null 2>&1 && HAVE_FFMPEG=1

log() { printf '%s  %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >> "$LOG"; }
free_bytes() { df -Pk "$VIDEOS" | awk 'NR == 2 { printf "%.0f", $4 * 1024 }'; }
file_size() { if [ -f "$1" ]; then wc -c < "$1" | tr -d ' '; else echo 0; fi; }
gb() { awk -v b="$1" 'BEGIN { if (b >= 1e9) printf "%.1f GB", b / 1e9; else printf "%.0f MB", b / 1e6 }'; }

PLAN="$(mktemp)"
trap 'rm -f "$PLAN"' EXIT
trap 'echo; echo "Interrupted. Partial downloads are kept as .part files; re-run to resume."; log "interrupted"; exit 130' INT TERM

# ---------------------------------------------------------------------------
# Step 1 - read MAP.md, see what is on disk, and resolve each missing show's
# video URL (and size) on Cablecast. Writes one tab-separated row per file:
#   status  id  file  eventDate  bytes  url
# status is "get", "nolink" (show has no video attached), "absent" (Cablecast
# answered 404 for the show) or "error" (the lookup itself failed).
# ---------------------------------------------------------------------------
echo "Reading MAP.md and Input/Videos..."
python3 - "$MAP" "$VIDEOS" "$BASE_SITE" "$SITE_ID" "$SEARCH_TERMS" "$UA" "$ORDER" \
          "$ONLY_IDS" "$SINCE" "$UNTIL" "$SIZES" "$PLAN" <<'PYEOF'
import json, os, re, subprocess, sys, urllib.parse
from concurrent.futures import ThreadPoolExecutor

(map_path, videos, base, site, terms, ua, order,
 only_ids, since, until, sizes, plan_path) = sys.argv[1:13]
only = {int(x) for x in re.findall(r"\d+", only_ids)}

def curl(args, timeout="120"):
    # --retry covers timeouts and 408/429/5xx; a 404 fails at once.
    return subprocess.run(["curl", "-sSL", "-A", ua, "--connect-timeout", "20",
                           "--max-time", timeout, "--retry", "3", "--retry-delay", "3"] + args,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def get_json(url):
    p = curl(["-f", url])
    if p.returncode:
        msg = p.stderr.decode("utf-8", "replace").strip().splitlines()
        return None, (msg[-1] if msg else "curl exit %d" % p.returncode)
    try:
        return json.loads(p.stdout.decode("utf-8", "replace")), None
    except ValueError:
        return None, "response was not JSON"

# --- MAP.md: wanted files ---------------------------------------------------
wanted, seen_files, heading, no_copy, no_id = [], set(), "", 0, []
video_line = re.compile(r"^\s*(?:[-*]\s*)?(?:\*\*)?Video:")
for line in open(map_path, encoding="utf-8"):
    if line.startswith("## "):
        heading = line[3:].strip()
        continue
    if not video_line.match(line):
        continue
    paths = re.findall(r"`Input/Videos/([^`]+)`", line)
    if not paths:
        no_copy += 1
        continue
    name = paths[0]
    if name in seen_files:
        continue
    seen_files.add(name)
    m = re.match(r"^(\d+) ", name)
    if m:
        sid = int(m.group(1))
    else:
        links = re.findall(r"internetchannel/show/(\d+)", line)
        if not links:
            no_id.append(name)
            continue
        sid = int(links[0])
    wanted.append((sid, name, heading))

# --- what is already on disk -------------------------------------------------
on_disk = {b for b in os.listdir(videos) if not b.startswith(".")}
disk_ids = set()
for b in on_disk:
    m = re.match(r"^(\d+) ", b)
    if m and not b.endswith(".part"):
        disk_ids.add(int(m.group(1)))
missing = [(sid, name, h) for sid, name, h in wanted
           if name not in on_disk and sid not in disk_ids]
print("  MAP.md video files      : %d" % len(wanted), file=sys.stderr)
print("  already in Input/Videos : %d" % (len(wanted) - len(missing)), file=sys.stderr)
print("  missing                 : %d" % len(missing), file=sys.stderr)
if no_copy:
    print("  sections with no recording (ignored): %d" % no_copy, file=sys.stderr)
if only:
    missing = [w for w in missing if w[0] in only]
    print("  missing among --ids     : %d" % len(missing), file=sys.stderr)
for n in no_id:
    print("  !! no show id for %s - skipped" % n, file=sys.stderr)

# --- Cablecast: resolve URLs ---------------------------------------------------
info = {}  # sid -> {"url":..., "date":...}
def absorb(doc):
    vods = {v.get("id"): (v.get("url") or "") for v in doc.get("vods", []) or []}
    shows = doc.get("shows")
    if shows is None and doc.get("show"):
        shows = [doc["show"]]
    for s in shows or []:
        sid = s.get("id")
        urls = [vods.get(v, "") for v in s.get("vods", []) or []]
        urls = [u for u in urls if u]
        best = next((u for u in urls if u.endswith(".mp4")), urls[0] if urls else "")
        prev = info.get(sid)
        if prev and prev["url"].endswith(".mp4"):
            continue
        info[sid] = {"url": best or (prev or {}).get("url", ""),
                     "date": (s.get("eventDate") or "")[:10]}

need = {sid for sid, _, _ in missing}
api_ok, last_err, lookup_err = 0, "", {}
if need:
    print("Looking up video links on Cablecast...", file=sys.stderr)
    for term in terms.split("|"):
        url = "%s/CablecastAPI/v1/shows?site=%s&search=%s&page_size=5000&include=vod" % (
            base, site, urllib.parse.quote(term))
        doc, err = get_json(url)
        if doc is None:
            print("  search \"%s\": %s" % (term, err), file=sys.stderr)
            last_err = err
            continue
        api_ok += 1
        got, count = len(doc.get("shows") or []), (doc.get("meta") or {}).get("count")
        if count is not None and got < count:
            print("  search \"%s\": %d of %d shows (capped; per-show lookups will fill gaps)" % (term, got, count), file=sys.stderr)
        absorb(doc)
    rest = sorted(sid for sid in need if not (info.get(sid) or {}).get("url"))
    if rest:
        print("  looking up %d show(s) one at a time..." % len(rest), file=sys.stderr)
        def one(sid):
            return sid, get_json("%s/CablecastAPI/v1/shows/%d?site=%s&include=vod" % (base, sid, site))
        with ThreadPoolExecutor(4) as ex:
            for sid, (doc, err) in ex.map(one, rest):
                if doc is not None:
                    api_ok += 1
                    absorb(doc)
                elif sid not in info and "404" not in err:  # 404 = no such show
                    lookup_err[sid] = err
                    last_err = err
    if api_ok == 0:
        print("\nCould not reach Cablecast at %s (%s).\n"
              "Run this script in Terminal on the Mac; the Claude/Cowork sandboxes get HTTP 403 from this site."
              % (base, last_err or "no response"), file=sys.stderr)
        sys.exit(3)
    for sid, err in sorted(lookup_err.items()):
        print("  show %d: lookup failed (%s)" % (sid, err), file=sys.stderr)

# --- sizes (HEAD), date filter, order -------------------------------------------
def head_size(url):
    # Headers of every redirect hop come back; use the last block, and only
    # if its status is 2xx (an error page's length is not the video's).
    p = curl(["-I", url], timeout="60")
    blocks = re.split(rb"(?m)^(?=HTTP/)", p.stdout)
    last = blocks[-1] if blocks else b""
    if not re.match(rb"HTTP/\S+\s+2\d\d", last):
        return 0
    m = re.search(rb"(?im)^content-length:\s*(\d+)", last)
    return int(m.group(1)) if m else 0

# Empty fields are written as "-": bash's read collapses runs of tabs, so an
# empty column would shift every column after it.
rows = []
for sid, name, h in missing:
    i = info.get(sid)
    if i is None:
        rows.append(["error" if sid in lookup_err else "absent", sid, name, "-", 0, "-"]); continue
    if since and i["date"] and i["date"] < since: continue
    if until and i["date"] and i["date"] > until: continue
    rows.append(["get" if i["url"] else "nolink", sid, name, i["date"] or "-", 0, i["url"] or "-"])

if sizes == "1":
    todo = [r for r in rows if r[0] == "get" and ".m3u8" not in r[5]]  # a playlist's size says nothing
    if todo:
        print("Checking file sizes (%d)..." % len(todo), file=sys.stderr)
        with ThreadPoolExecutor(6) as ex:
            for r, n in zip(todo, ex.map(lambda r: head_size(r[5]), todo)):
                r[4] = n

rows.sort(key=lambda r: (r[3], r[1]), reverse=(order == "newest"))
with open(plan_path, "w", encoding="utf-8") as f:
    for r in rows:
        f.write("\t".join(str(x).replace("\t", " ") for x in r) + "\n")
PYEOF
[ $? -eq 0 ] || { echo "Planning step failed." >&2; exit 1; }

COUNT=$(awk -F'\t' '$1 == "get"' "$PLAN" | wc -l | tr -d ' ')
NOLINK=$(awk -F'\t' '$1 == "nolink"' "$PLAN" | wc -l | tr -d ' ')
ABSENT=$(awk -F'\t' '$1 == "absent"' "$PLAN" | wc -l | tr -d ' ')
LOOKUP_ERR=$(awk -F'\t' '$1 == "error"' "$PLAN" | wc -l | tr -d ' ')
TOTAL=$(awk -F'\t' '$1 == "get" { s += $5 } END { printf "%.0f", s }' "$PLAN")
UNKNOWN=$(awk -F'\t' '$1 == "get" && $5 == 0' "$PLAN" | wc -l | tr -d ' ')
FREE=$(free_bytes)

echo
echo "  to download : $COUNT file(s), $(gb "$TOTAL")$( [ "$UNKNOWN" -gt 0 ] && [ "$SIZES" = 1 ] && echo " ($UNKNOWN of unknown size)")"
[ "$NOLINK" -gt 0 ] && echo "  no video attached on Cablecast : $NOLINK"
[ "$ABSENT" -gt 0 ] && echo "  not found on Cablecast         : $ABSENT"
[ "$LOOKUP_ERR" -gt 0 ] && echo "  lookup failed (re-run later)   : $LOOKUP_ERR"
echo "  free space on volume : $(gb "$FREE")"
[ "$LIMIT" -gt 0 ] && echo "  limit this run : $LIMIT"
[ "$HAVE_FFMPEG" = 0 ] && awk -F'\t' '$1 == "get" && $6 ~ /\.m3u8/' "$PLAN" | grep -q . \
  && echo "  NOTE: some links are HLS (.m3u8) and ffmpeg is not installed - those will be skipped (brew install ffmpeg)"
if [ "$SIZES" = 1 ] && [ "$TOTAL" -gt 0 ] && [ "$FREE" -lt $((TOTAL + MIN_FREE_GB * 1000000000)) ]; then
  echo "  WARNING: the full set does not fit with ${MIN_FREE_GB} GB to spare; the run will stop when space runs low."
fi
echo

# ---------------------------------------------------------------------------
# Step 2 - download.
# ---------------------------------------------------------------------------
n=0; fetched=0; failed=0; skipped_ffmpeg=0; left_by_limit=0; stopped_space=0
FAILURES=""
[ "$DRY" = 0 ] && log "run started: $COUNT file(s) planned, $(gb "$TOTAL")"
while IFS=$'\t' read -r -u 3 status id name ev bytes url; do
  [ "$ev" = "-" ] && ev=""
  case "$status" in
    nolink) echo "  -- show $id  $name  (${ev:-no date}): no video attached on Cablecast yet"; continue ;;
    absent) echo "  -- show $id  $name: not found on Cablecast"; continue ;;
    error)  echo "  -- show $id  $name: Cablecast lookup failed; re-run later"; continue ;;
  esac
  if [ "$LIMIT" -gt 0 ] && [ "$fetched" -ge "$LIMIT" ]; then
    left_by_limit=$((left_by_limit + 1)); continue
  fi
  n=$((n + 1))
  size_txt="size unknown"; [ "$bytes" -gt 0 ] && size_txt="$(gb "$bytes")"
  out="$VIDEOS/$name"

  if [ "$DRY" = 1 ]; then
    printf '%4d  show %-6s %-10s %12s  %s\n' "$n" "$id" "${ev:-no date}" "$size_txt" "$name"
    printf '      %s\n' "$url"
    continue
  fi

  printf '[%s] %d/%d  show %s  %s  (%s, %s)\n' "$(date '+%H:%M:%S')" "$n" "$COUNT" "$id" "$name" "${ev:-no date}" "$size_txt"

  case "$url" in
    *.m3u8*)
      if [ "$HAVE_FFMPEG" = 0 ]; then
        echo "  !! HLS source and no ffmpeg - skipped"; skipped_ffmpeg=$((skipped_ffmpeg + 1)); continue
      fi
      free="$(free_bytes)"
      if [ "$free" -lt $((MIN_FREE_GB * 1000000000 + 8000000000)) ]; then
        echo "  !! less than $((MIN_FREE_GB + 8)) GB free - stopping"; stopped_space=1; break
      fi
      tmp="$out.part.mp4"; rm -f "$tmp"
      if ffmpeg -nostdin -loglevel error -stats -y -user_agent "$UA" \
                -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 \
                -i "$url" -c copy "$tmp" < /dev/null && [ "$(file_size "$tmp")" -ge 1000000 ]; then
        mv "$tmp" "$out"; fetched=$((fetched + 1))
        echo "  ok  $(gb "$(file_size "$out")")"; log "ok      $id  $name  (ffmpeg)"
      else
        rm -f "$tmp"; failed=$((failed + 1))
        FAILURES="$FAILURES
  $id  $name  <- $url  (ffmpeg failed)"
        echo "  !! ffmpeg failed"; log "FAILED  $id  $name  (ffmpeg)"
      fi
      continue
      ;;
  esac

  tmp="$out.part"
  have="$(file_size "$tmp")"
  if [ "$bytes" -gt 0 ] && [ "$have" -gt "$bytes" ]; then
    echo "  .part is larger than the server's file ($have > $bytes) - starting over"
    rm -f "$tmp"; have=0
  fi
  need_bytes=$(( bytes > have ? bytes - have : 0 ))
  free="$(free_bytes)"
  if [ "$free" -lt $((need_bytes + MIN_FREE_GB * 1000000000)) ]; then
    echo "  !! only $(gb "$free") free; this file needs $(gb "$need_bytes") plus ${MIN_FREE_GB} GB to spare - stopping"
    stopped_space=1; log "stopped: low disk space before $id"; break
  fi
  if [ "$bytes" -gt 0 ] && [ "$have" -eq "$bytes" ]; then
    echo "  .part is already complete"
    rc=0   # an earlier run finished the transfer but stopped before the rename
  else
    [ "$have" -gt 0 ] && echo "  resuming at $(gb "$have")"
    curl -fL -A "$UA" --connect-timeout 30 --retry 5 --retry-delay 10 --retry-all-errors \
         -C - -o "$tmp" "$url"
    rc=$?
  fi
  got="$(file_size "$tmp")"
  if [ "$rc" -eq 0 ] && { { [ "$bytes" -gt 0 ] && [ "$got" -eq "$bytes" ]; } || { [ "$bytes" -eq 0 ] && [ "$got" -ge 1000000 ]; }; }; then
    mv "$tmp" "$out"; fetched=$((fetched + 1))
    echo "  ok  $(gb "$got")"; log "ok      $id  $name  $got bytes"
  else
    failed=$((failed + 1))
    kept=""; [ "$got" -gt 0 ] && kept="; .part kept for resume"
    FAILURES="$FAILURES
  $id  $name  (curl exit $rc, $got of $bytes bytes$kept)"
    echo "  !! incomplete (curl exit $rc, $got of $bytes bytes$kept) - re-run to retry"
    log "FAILED  $id  $name  curl exit $rc, $got/$bytes bytes"
  fi
done 3< "$PLAN"

echo
echo "--------------------------------------------------------------"
if [ "$DRY" = 1 ]; then
  echo "Dry run: $COUNT file(s), $(gb "$TOTAL"), would be fetched into Input/Videos."
  [ "$LIMIT" -gt 0 ] && echo "With --limit $LIMIT, a real run stops after $LIMIT."
else
  echo "Downloaded : $fetched"
  echo "Failed     : $failed"
  [ "$skipped_ffmpeg" -gt 0 ] && echo "Need ffmpeg: $skipped_ffmpeg"
  [ "$left_by_limit" -gt 0 ] && echo "Left for a later run (--limit): $left_by_limit"
  [ "$stopped_space" = 1 ]   && echo "Stopped early: low disk space."
  [ -n "$FAILURES" ] && { echo; echo "Did not complete (re-run to retry):$FAILURES"; }
  log "run ended: $fetched ok, $failed failed"
fi
echo "--------------------------------------------------------------"
[ "$DRY" = 0 ] && { [ "$failed" -gt 0 ] || [ "$stopped_space" = 1 ]; } && exit 1
exit 0
