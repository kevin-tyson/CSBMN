#!/bin/bash
#
# Copyright 2026 Kevin Tyson
# SPDX-License-Identifier: Apache-2.0
#
# ---------------------------------------------------------------------------
# download_videos_missing_dialogue.sh - fetch the recording of every school
# board / SAU 6 / committee meeting that has no dialogue CSV in
# Output/HTML/Dialogue yet and no video in Input/Videos, from Claremont
# Community Television (CCTV) / Claremont Community Media Center (CCMC)
# Cablecast.
#
# Run it on the Mac itself, in Terminal. reflect-claremont.cablecast.tv
# answers HTTP 403 to the Cowork/Claude sandboxes (they sit behind an egress
# allowlist proxy); a normal Terminal.app process on the Mac reaches it.
#
#     cd "/Volumes/BigData/Cowork Projects/Government Transparency Project"
#     bash Scripts/download_videos_missing_dialogue.sh --dry-run
#
# The dry run fetches no video. It lists every in-scope meeting that lacks a
# dialogue, split into "already on disk" and "to download", with show id,
# event date, size, whether a transcript exists, and the source URL. The real
# run is the same command without --dry-run.
#
# HOW THIS DIFFERS FROM THE OTHER TWO DOWNLOAD SCRIPTS
# ---------------------------------------------------------------------------
#   download_untranscribed_videos.sh  skips a meeting once it has a TRANSCRIPT.
#   download_missing_videos.sh        fetches whatever MAP.md names, dialogue
#                                     or not.
#   this script                       skips a meeting only once it has a
#                                     DIALOGUE CSV, so a meeting that was
#                                     transcribed but never attributed still
#                                     gets its video.
#
# WHICH MEETINGS COUNT
# ---------------------------------------------------------------------------
#   The universe is the union of
#     - every "Video:" entry in Input/SupportingDocuments/MAP.md, and
#     - every show the Cablecast catalog search returns for SEARCH_TERMS whose
#       title passes SCOPE_INCLUDE and not SCOPE_EXCLUDE (the same two
#       regexes download_untranscribed_videos.sh uses; keep them in step).
#   A catalog show with no video attached is dropped unless its eventDate is
#   within SEARCH_RECENT_DAYS (the catalog reaches back to 2006, mostly with
#   no video).
#
# HOW "HAS A DIALOGUE" AND "ON DISK" ARE DECIDED
# ---------------------------------------------------------------------------
#   A show id is read from a file name in either project form:
#   "<id> <title>.ext" or "<YYYY-MM-DD>_<id>_<title>.ext".
#   A meeting has a dialogue if any of these holds:
#     1. a CSV in Output/HTML/Dialogue carries its show id;
#     2. MAP.md names its local file, and a CSV exists with that file's stem
#        ("Claremont School Board 72126.mp4" -> "Claremont School Board
#        72126.CSV" or "... 72126.mp4.CSV");
#     3. for a show MAP.md does not list: a CSV with no show id, not already
#        assigned to another show by MAP.md, has exactly the same digits as
#        the show's Cablecast title ("7/21/26" -> 72126). Exact, not
#        substring. These matches are printed so they can be checked.
#   "On disk" uses the same three tests against Input/Videos (finished files
#   only; a .part is resumed, not counted as present).
#
# FILE NAMES
# ---------------------------------------------------------------------------
#   If MAP.md already names the local file, that exact name is used, so
#   MAP.md needs no edit. Otherwise the file is saved as
#   "<id> <Cablecast title>.mp4", the project's convention.
#
# SAFETY
# ---------------------------------------------------------------------------
#   - Downloads go to "<file>.part" and are renamed only once the size matches
#     the server's Content-Length (or, with no length given, once the file is
#     over 1 MB). Ctrl-C is safe; re-run and each .part resumes (curl -C -).
#   - HLS (.m3u8) sources are remuxed with ffmpeg (-c copy, no re-encode);
#     without ffmpeg they are skipped and listed (brew install ffmpeg).
#   - Before each download the script stops if the file would leave less than
#     MIN_FREE_GB free on the volume.
#   - Nothing outside Input/Videos is written except the log,
#     Scripts/download_videos_missing_dialogue.log.
#
# OPTIONS
# ---------------------------------------------------------------------------
#   --dry-run          list what would be fetched, with sizes; fetch nothing
#   --no-sizes         skip the per-file size check (faster dry run)
#   --limit N          stop after N successful downloads
#   --oldest           oldest meetings first (default: newest first)
#   --since YYYY-MM-DD only meetings on or after this date
#   --until YYYY-MM-DD only meetings on or before this date
#   --ids "7313 7408"  only these show ids
#   --map-only         only meetings MAP.md lists (no catalog-only meetings)
#   --no-scope-filter  keep every catalog search hit, not just meetings
#   -h, --help         print this header
#
# Examples
#   bash Scripts/download_videos_missing_dialogue.sh --dry-run
#   bash Scripts/download_videos_missing_dialogue.sh --since 2024-01-01
#   bash Scripts/download_videos_missing_dialogue.sh --oldest --limit 10
#
# After a run: the new videos still need a transcript (Input/Transcripts) and
# then the transcript-to-dialogue step; meetings MAP.md does not list yet
# need a full map update.
# ---------------------------------------------------------------------------
set -uo pipefail

BASE_SITE="${CABLECAST_BASE:-https://reflect-claremont.cablecast.tv}"
SITE_ID=1
SEARCH_TERMS="School Board|SAU|Finance Committee|Budget|Deliberative|Committee"
SEARCH_RECENT_DAYS=45
MIN_FREE_GB=20
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"

# Show ids never to fetch, whatever their title. Keep in step with
# download_untranscribed_videos.sh (15738 = City of Claremont Policy Committee
# 5/7/24, dropped 2026-10-29).
EXCLUDE_IDS="15738"
# Same patterns as download_untranscribed_videos.sh (Python re, case-insensitive).
SCOPE_INCLUDE='school board|\bs\.?a\.?u\.?\s*#?\s*6\b|\bsau board|school bud(get)? hearing|finance (committee|subcommittee)|budget.*(hearing|committee|workshop|study)|deliberative|policy committee|negotiations? committee|building committee|facilities committee|subcommittee|city council.*school board|school board.*city council'
SCOPE_EXCLUDE='graduation|commencement|class night|recognition night|holiday concert|spring concert|candidates? forum|funding fairness|restructuring discussion|open house|science fair|spelling bee|talent show|scholarship|kindergarten screening|preschool|8th grade|the last bake sale|portrait unveiling|your candidates|candidates for|sullivan county|county budget|board of commissioners|nh issues|state budget hearing|city (council )?budget hearing|city budget public hearing|cardinal perspective|\bpsa\b|sugar river report|election results|come join us|ballot guide|movement towards excellence|smarter balance|community forum|superintendent search'

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MAP="$ROOT/Input/SupportingDocuments/MAP.md"
VIDEOS="$ROOT/Input/Videos"
TRANSCRIPTS="$ROOT/Input/Transcripts"
DIALOGUE="$ROOT/Output/HTML/Dialogue"
LOG="$ROOT/Scripts/download_videos_missing_dialogue.log"
# For offline testing only: a folder of saved catalog-search JSON files to read
# instead of querying Cablecast (sizes are then not checked).
CATALOG_DIR="${CATALOG_DIR:-}"

DRY=0; SIZES=1; LIMIT=0; ORDER=newest; SINCE=""; UNTIL=""; ONLY_IDS=""; MAP_ONLY=0; SCOPE_FILTER=1
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run)         DRY=1 ;;
    --no-sizes)        SIZES=0 ;;
    --limit)           shift; LIMIT="${1:-0}" ;;
    --oldest)          ORDER=oldest ;;
    --since)           shift; SINCE="${1:-}" ;;
    --until)           shift; UNTIL="${1:-}" ;;
    --ids)             shift; ONLY_IDS="${1:-}" ;;
    --map-only)        MAP_ONLY=1 ;;
    --no-scope-filter) SCOPE_FILTER=0 ;;
    -h|--help)         awk 'NR > 1 && !/^#/ { exit } NR > 1' "$0"; exit 0 ;;
    *) echo "unknown option: $1 (try --help)" >&2; exit 2 ;;
  esac
  shift
done
case "$LIMIT" in ''|*[!0-9]*) echo "--limit needs a whole number" >&2; exit 2 ;; esac
for d in "$SINCE" "$UNTIL"; do
  [ -z "$d" ] && continue
  printf '%s' "$d" | grep -Eq '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' || { echo "dates must be YYYY-MM-DD (got $d)" >&2; exit 2; }
done

for p in "$VIDEOS" "$DIALOGUE"; do
  [ -d "$p" ] || { echo "folder not found: $p" >&2; exit 1; }
done
[ -f "$MAP" ] || echo "note: MAP.md not found at $MAP - using the Cablecast catalog only" >&2
[ -d "$TRANSCRIPTS" ] || mkdir -p "$TRANSCRIPTS" 2>/dev/null || true
command -v python3 >/dev/null 2>&1 || { echo "python3 is required but was not found on PATH" >&2; exit 1; }
command -v curl    >/dev/null 2>&1 || { echo "curl is required but was not found on PATH" >&2; exit 1; }
HAVE_FFMPEG=0; command -v ffmpeg >/dev/null 2>&1 && HAVE_FFMPEG=1
[ -n "$CATALOG_DIR" ] && SIZES=0

log() { [ "$DRY" = 1 ] || printf '%s  %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >> "$LOG"; }
free_bytes() { df -Pk "$VIDEOS" | awk 'NR == 2 { printf "%.0f", $4 * 1024 }'; }
file_size() { if [ -f "$1" ]; then wc -c < "$1" | tr -d ' '; else echo 0; fi; }
gb() { awk -v b="$1" 'BEGIN { if (b >= 1e9) printf "%.1f GB", b / 1e9; else printf "%.0f MB", b / 1e6 }'; }

PLAN="$(mktemp)"
trap 'rm -f "$PLAN"' EXIT
trap 'echo; echo "Interrupted. Partial downloads are kept as .part files; re-run to resume."; log "interrupted"; exit 130' INT TERM

# ---------------------------------------------------------------------------
# Step 1 - index the project, query Cablecast, decide what lacks a dialogue.
# Writes one tab-separated row per meeting to fetch:
#   status  id  file  eventDate  bytes  url
# status is "get", "nolink" (no video attached), "absent" (Cablecast has no
# such show) or "error" (lookup failed). Empty fields are written as "-".
# ---------------------------------------------------------------------------
echo "Indexing Input/Videos, Input/Transcripts, Output/HTML/Dialogue and MAP.md..."
python3 - "$MAP" "$VIDEOS" "$TRANSCRIPTS" "$DIALOGUE" "$BASE_SITE" "$SITE_ID" "$SEARCH_TERMS" \
          "$UA" "$ORDER" "$ONLY_IDS" "$SINCE" "$UNTIL" "$SIZES" "$PLAN" "$SCOPE_INCLUDE" \
          "$SCOPE_EXCLUDE" "$SCOPE_FILTER" "$MAP_ONLY" "$SEARCH_RECENT_DAYS" "$CATALOG_DIR" "$EXCLUDE_IDS" <<'PYEOF'
import datetime, glob, json, os, re, subprocess, sys, urllib.parse
from concurrent.futures import ThreadPoolExecutor

(map_path, videos, transcripts, dialogue, base, site, terms, ua, order, only_ids,
 since, until, sizes, plan_path, inc_re, exc_re, scope_filter, map_only,
 recent_days, catalog_dir, exclude_ids) = sys.argv[1:22]
excluded = {int(x) for x in re.findall(r"\d+", exclude_ids)}
only = {int(x) for x in re.findall(r"\d+", only_ids)}
inc = re.compile(inc_re, re.I); exc = re.compile(exc_re, re.I)
cutoff = (datetime.date.today() - datetime.timedelta(days=int(recent_days))).isoformat()

def err(*a): print(*a, file=sys.stderr)

EXT = re.compile(r"(\.(mp4|m4v|mov|json|csv|txt|part))+$", re.I)
def stem(name): return EXT.sub("", name)
def show_id(name):
    m = re.match(r"^(\d+) ", name) or re.match(r"^\d{4}-\d{2}-\d{2}_(\d+)_", name)
    return int(m.group(1)) if m else None
def digits(s): return re.sub(r"\D", "", s)

def index(folder, keep):
    ids, stems, alias = {}, set(), {}
    if not os.path.isdir(folder):
        return ids, stems, alias
    for b in os.listdir(folder):
        if b.startswith(".") or not keep(b):
            continue
        stems.add(stem(b).lower())
        sid = show_id(b)
        if sid is not None:
            ids.setdefault(sid, b)
        elif digits(stem(b)):
            alias.setdefault(digits(stem(b)), b)
    stems.discard("")
    return ids, stems, alias

dlg = index(dialogue, lambda b: b.lower().endswith(".csv"))
vid = index(videos,   lambda b: not b.endswith(".part") and not b.endswith(".part.mp4")
                                and re.search(r"\.(mp4|m4v|mov)$", b, re.I))
trn = index(transcripts, lambda b: b.lower().endswith(".json"))

# --- MAP.md: show id -> local file name ------------------------------------
map_name = {}
if os.path.isfile(map_path):
    video_line = re.compile(r"^\s*(?:[-*]\s*)?(?:\*\*)?Video:")
    for line in open(map_path, encoding="utf-8"):
        if not video_line.match(line):
            continue
        paths = re.findall(r"`Input/Videos/([^`]+)`", line)
        if not paths:
            continue
        name = paths[0]
        sid = show_id(name)
        if sid is None:
            links = re.findall(r"internetchannel/show/(\d+)", line)
            if not links:
                err("  !! MAP.md: no show id for %s - skipped" % name)
                continue
            sid = int(links[0])
        map_name.setdefault(sid, name)

claimed = {stem(n).lower() for n in map_name.values()}

def has(idx, sid, title):
    """Return how a show matches a folder index, or None."""
    ids, stems, alias = idx
    if sid in ids:
        return "file:" + ids[sid]
    n = map_name.get(sid)
    if n and stem(n).lower() in stems:
        return "file:" + n
    # Date-digit fallback, only for shows MAP.md does not place, and never onto
    # a file MAP.md already assigns to another show.
    d = digits(title or "")
    if sid not in map_name and d and d in alias and stem(alias[d]).lower() not in claimed:
        return "alias:" + alias[d]
    return None

# --- Cablecast catalog ------------------------------------------------------
def curl(args, timeout="120"):
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

info = {}  # sid -> {"title","date","url"}
def absorb(doc):
    vods = {v.get("id"): (v.get("url") or "") for v in doc.get("vods", []) or []}
    shows = doc.get("shows")
    if shows is None and doc.get("show"):
        shows = [doc["show"]]
    for s in shows or []:
        sid = s.get("id")
        urls = [u for u in (vods.get(v, "") for v in s.get("vods", []) or []) if u]
        best = next((u for u in urls if u.endswith(".mp4")), urls[0] if urls else "")
        prev = info.get(sid) or {}
        if prev.get("url", "").endswith(".mp4"):
            continue
        info[sid] = {"title": (s.get("title") or prev.get("title") or "").strip(),
                     "date": (s.get("eventDate") or "")[:10] or prev.get("date", ""),
                     "url": best or prev.get("url", "")}

api_ok, last_err, lookup_err = 0, "", {}
if catalog_dir:
    for path in sorted(glob.glob(os.path.join(catalog_dir, "*.json"))):
        try:
            absorb(json.load(open(path, encoding="utf-8"))); api_ok += 1
        except Exception:
            pass
    err("Read %d saved catalog file(s) from %s (offline test)" % (api_ok, catalog_dir))
else:
    err("Searching the Cablecast show catalog...")
    for term in terms.split("|"):
        doc, e = get_json("%s/CablecastAPI/v1/shows?site=%s&search=%s&page_size=5000&include=vod"
                          % (base, site, urllib.parse.quote(term)))
        if doc is None:
            err("  \"%s\": %s" % (term, e)); last_err = e; continue
        api_ok += 1
        got, count = len(doc.get("shows") or []), (doc.get("meta") or {}).get("count")
        if count is not None and got < count:
            err("  \"%s\": %d of %d shows - INCOMPLETE (page_size cap?)" % (term, got, count))
        absorb(doc)
    if api_ok == 0:
        err("\nCould not reach Cablecast at %s (%s).\n"
            "Run this script in Terminal on the Mac; the Claude/Cowork sandboxes get HTTP 403 from this site."
            % (base, last_err or "no response"))
        sys.exit(3)

# --- universe of meetings ---------------------------------------------------
universe = set(map_name)
out_of_scope = stale = 0
if map_only != "1":
    for sid, i in info.items():
        if sid in universe:
            continue
        if scope_filter == "1" and not (inc.search(i["title"]) and not exc.search(i["title"])):
            out_of_scope += 1; continue
        if not i["url"] and (not i["date"] or i["date"] < cutoff):
            stale += 1; continue
        universe.add(sid)
universe -= excluded
if only:
    universe &= only | set()
    for sid in only - universe:
        if sid not in excluded:
            universe.add(sid)   # an explicit --ids show is looked up even if unknown

# Shows the searches did not return (MAP.md entries, --ids): look up one at a time.
rest = sorted(sid for sid in universe if not (info.get(sid) or {}).get("url"))
if rest and not catalog_dir:
    err("  looking up %d show(s) one at a time..." % len(rest))
    def one(sid):
        return sid, get_json("%s/CablecastAPI/v1/shows/%d?site=%s&include=vod" % (base, sid, site))
    with ThreadPoolExecutor(4) as ex:
        for sid, (doc, e) in ex.map(one, rest):
            if doc is not None:
                absorb(doc)
            elif sid not in info and "404" not in e:
                lookup_err[sid] = e

# --- classify ----------------------------------------------------------------
def slug(t):
    t = re.sub(r'[/:*?"<>|\\]', "-", t)
    return re.sub(r"\s+", " ", t).strip()

with_dialogue, on_disk, to_get, alias_notes = 0, [], [], []
for sid in sorted(universe):
    i = info.get(sid) or {}
    title, date, url = i.get("title", ""), i.get("date", ""), i.get("url", "")
    d = has(dlg, sid, title)
    if d:
        with_dialogue += 1
        if d.startswith("alias:"):
            alias_notes.append("  show %d \"%s\" -> dialogue %s" % (sid, title, d[6:]))
        continue
    if since and date and date < since: continue
    if until and date and date > until: continue
    name = map_name.get(sid) or ("%d %s.mp4" % (sid, slug(title) or "Show %d" % sid))
    t = "transcript on hand" if has(trn, sid, title) else "no transcript"
    v = has(vid, sid, title)
    if v:
        on_disk.append((date, sid, v.split(":", 1)[1], t))
        continue
    if sid not in info:
        status = "error" if sid in lookup_err else "absent"
    else:
        status = "get" if url else "nolink"
    to_get.append([status, sid, name, date or "-", 0, url or "-", t])

err("  meetings considered          : %d (MAP.md %d%s)" % (
    len(universe), len(map_name), "" if map_only == "1" else
    ", plus catalog-only in-scope shows; %d out of scope, %d old with no video" % (out_of_scope, stale)))
err("  already have a dialogue      : %d" % with_dialogue)
err("  no dialogue, video on disk   : %d" % len(on_disk))
err("  no dialogue, video not on disk: %d" % len(to_get))
if alias_notes:
    err("\n  Dialogue matched by date digits only (check these):")
    for a in alias_notes: err(a)
if on_disk:
    err("\n  No dialogue yet, video already in Input/Videos (not downloaded again):")
    for date, sid, name, t in sorted(on_disk, reverse=True):
        err("    show %-6s %-10s %s  (%s)" % (sid, date or "no date", name, t))

def head_size(url):
    p = curl(["-I", url], timeout="60")
    blocks = re.split(rb"(?m)^(?=HTTP/)", p.stdout)
    last = blocks[-1] if blocks else b""
    if not re.match(rb"HTTP/\S+\s+2\d\d", last):
        return 0
    m = re.search(rb"(?im)^content-length:\s*(\d+)", last)
    return int(m.group(1)) if m else 0

if sizes == "1":
    todo = [r for r in to_get if r[0] == "get" and ".m3u8" not in r[5]]
    if todo:
        err("\nChecking file sizes (%d)..." % len(todo))
        with ThreadPoolExecutor(6) as ex:
            for r, n in zip(todo, ex.map(lambda r: head_size(r[5]), todo)):
                r[4] = n

to_get.sort(key=lambda r: (r[3], r[1]), reverse=(order == "newest"))
with open(plan_path, "w", encoding="utf-8") as f:
    for r in to_get:
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
[ "$NOLINK" -gt 0 ]     && echo "  no video attached on Cablecast : $NOLINK"
[ "$ABSENT" -gt 0 ]     && echo "  not found on Cablecast         : $ABSENT"
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
log "run started: $COUNT file(s) planned, $(gb "$TOTAL")"
while IFS=$'\t' read -r -u 3 status id name ev bytes url tnote; do
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
    printf '%4d  show %-6s %-10s %12s  %s  [%s]\n' "$n" "$id" "${ev:-no date}" "$size_txt" "$name" "$tnote"
    printf '      %s\n' "$url"
    continue
  fi

  printf '[%s] %d/%d  show %s  %s  (%s, %s)\n' "$(date '+%H:%M:%S')" "$n" "$COUNT" "$id" "$name" "${ev:-no date}" "$size_txt"

  case "$url" in
    *.m3u8*)
      if [ "$HAVE_FFMPEG" = 0 ]; then
        echo "  !! HLS source and no ffmpeg - skipped"; skipped_ffmpeg=$((skipped_ffmpeg + 1)); continue
      fi
      if [ "$(free_bytes)" -lt $((MIN_FREE_GB * 1000000000 + 8000000000)) ]; then
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
    echo "  .part is already complete"; rc=0
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
  [ "$left_by_limit" -gt 0 ]  && echo "Left for a later run (--limit): $left_by_limit"
  [ "$stopped_space" = 1 ]    && echo "Stopped early: low disk space."
  [ -n "$FAILURES" ] && { echo; echo "Did not complete (re-run to retry):$FAILURES"; }
  log "run ended: $fetched ok, $failed failed"
fi
echo "--------------------------------------------------------------"
[ "$DRY" = 0 ] && { [ "$failed" -gt 0 ] || [ "$stopped_space" = 1 ]; } && exit 1
exit 0
