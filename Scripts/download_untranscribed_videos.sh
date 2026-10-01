#!/bin/bash
#
# Copyright 2026 Kevin Tyson
# SPDX-License-Identifier: Apache-2.0
#
# ---------------------------------------------------------------------------
# download_untranscribed_videos.sh (v4) - walk the CCTV "CLAREMONT SCHOOLS"
# Cablecast gallery (internetchannel, channel 6) AND search the Cablecast show
# catalog for meetings the gallery leaves out, keep only school board / SAU 6 /
# subcommittee meeting recordings, drop anything already downloaded or already
# transcribed, and fetch the rest into Input/Videos.
#
# Run it on the Mac itself, in Terminal - not from a Cowork/Claude session.
# reflect-claremont.cablecast.tv returns HTTP 403 to every route available
# inside this account's cloud container and inside the Cowork desktop
# workspace's own sandboxed shell (both sit behind the same egress allowlist
# proxy) - confirmed directly while writing this version. Only a normal
# Terminal.app process on the Mac has a real path to the site.
#
#     cd "/Volumes/BigData/Cowork Projects/Government Transparency Project"
#     bash Scripts/download_untranscribed_videos.sh --dry-run --debug
#
#   Run that first. It fetches nothing, only lists what it found and what it
#   excluded, and (with --debug) saves the raw gallery pages under
#   Scripts/.gallery_debug/ plus a gallery_excluded.tsv / gallery_in_scope.tsv
#   you can scan for anything that landed on the wrong side of the filter.
#
# WHAT CHANGED IN v4 (2026-10-01), AND WHY
# ---------------------------------------------------------------------------
#   - The gallery is not a complete list. The full 9/2/26 board meeting (show
#     17566, 3h14m) was never added to it, nor were SAU 6 board meetings such
#     as 4/9/26 (show 17307) or 12/1/22 (show 14765), or the 5/7/24 Policy
#     Committee (show 15738). Step 2b now also searches the show catalog
#     through /CablecastAPI/v1/shows?search=<term>&include=vod for each term in
#     SEARCH_TERMS and merges whatever the gallery missed. --no-search turns
#     this off.
#   - With include=vod the API returns a progressive store-N/.../vod.mp4 for
#     recent shows too (checked 2026-10-01: 206 Partial Content, video/mp4,
#     6.9 GB for 17566), where the gallery hands back an .m3u8. When both
#     exist the script now prefers the API's .mp4: a plain resumable curl,
#     no ffmpeg needed.
#   - Catalog shows with no video attached are listed as "no link yet" only if
#     their eventDate falls within SEARCH_RECENT_DAYS; older ones (the
#     catalog goes back to 2006, mostly with no video) are dropped quietly and
#     recorded in the --debug TSV.
#   - The SAU clause in SCOPE_INCLUDE used the POSIX class [[:space:]], which
#     Python's re does not support, so "SAU 6 Board Meeting" titles only ever
#     matched when they also said "school board". Fixed. SCOPE_EXCLUDE gained
#     the county, city-budget, PSA, election-night and interview programming
#     that the catalog search turns up.
#   - The title/date alias check now also indexes Input/Transcripts, not just
#     Input/Videos, and compares the date digits exactly (file extensions
#     stripped) instead of by substring. Six mid-2026 meetings have
#     transcripts under names without a show id ("Claremont School Board
#     81926.mp4.json"); with Input/Videos emptied, v3 would have downloaded all
#     six again. The old substring test could also skip the wrong meeting
#     ("12/1/23" contains "2123").
#
# WHAT CHANGED FROM v1/v2, AND WHY
# ---------------------------------------------------------------------------
# Earlier drafts assumed every show's page had to be fetched one at a time to
# find its title and a "store-N/.../vod.mp4" link, either from the
# CablecastAPI JSON or the show's own page. Pulling six real gallery pages and
# reading them closely (this could only be done here by working from copies
# fetched earlier on the Mac and staged in for inspection - this script itself
# still can't reach the site from where it's written) showed something
# simpler and something important:
#
#   - The gallery page ITSELF embeds a JSON block, per show, with the show id,
#     title, and a direct "vodUrl" - no per-show request needed at all. That
#     block is what this version reads (see extract_gallery_json() below).
#     The old per-show API/legacy-page/SPA-page chase is gone; it was solving
#     a problem the gallery page had already solved.
#
#   - "vodUrl" is NOT always an .mp4. Every show with an id up to about 11056
#     (roughly meetings through late 2020) still points at a progressive
#     store-N/.../vod.mp4 file - a plain curl -o download, exactly like the
#     231 recordings download_videos.sh already fetched that way. Every show
#     from about id 11106 onward (everything from ~Jan 2021 to today, i.e.
#     essentially all of what could still be "not yet transcribed") instead
#     points at a store-N/.../vod.m3u8 HLS playlist - a manifest that lists
#     video segments, not a single file. curl can only fetch that manifest's
#     text; it cannot turn it into a playable recording on its own.
#
#     So for .m3u8 shows this script hands the URL to ffmpeg
#     ("ffmpeg -i <url> -c copy <file>.mp4", i.e. a remux/copy, not a
#     re-encode - fast, and no quality loss) instead of curl. If ffmpeg isn't
#     on this Mac, `brew install ffmpeg` gets it; until then, this script
#     skips any .m3u8 show and lists it separately (see NEEDS_FFMPEG below)
#     rather than saving the tiny playlist text as if it were a video - the
#     same size-floor check as before (a real recording is never under 1MB)
#     would catch that anyway, but there is no reason to let it try.
#
#   - Not every show in this gallery is a board/SAU/committee meeting - it
#     also carries school graduations, candidate forums, funding-policy
#     panels, safety forums, holiday concerts, and the like. This version
#     filters on each show's title (SCOPE_INCLUDE/SCOPE_EXCLUDE below) so
#     those don't get pulled in as if they were meetings. Check
#     Scripts/.gallery_debug/gallery_excluded.tsv after a --debug run and
#     adjust the two regexes if something is on the wrong side of the line,
#     or pass --no-scope-filter to keep everything the gallery lists.
#
#   - As of the run that produced the gallery pages this script was written
#     against (2026-09-27), Input/Videos already had every school-board/SAU
#     recording through the most recent one in the gallery (9/16/26) - the
#     only in-scope gap was a show already downloaded but not yet
#     transcribed, which this script correctly leaves alone (that's a
#     transcription task, not a download one). A normal run of this script
#     right after a meeting airs should find just that one new show to fetch.
#
# Safe to stop (Ctrl-C) and re-run: anything already in Input/Videos or
# Input/Transcripts is left alone and skipped, and a partial curl download
# resumes where it left off (ffmpeg remuxes are all-or-nothing; a partial one
# is deleted and the show is retried from scratch on the next run).
#
#   bash Scripts/download_untranscribed_videos.sh --dry-run          list only, fetch nothing
#   bash Scripts/download_untranscribed_videos.sh --debug            save raw gallery pages + scope audit under Scripts/.gallery_debug/
#   bash Scripts/download_untranscribed_videos.sh --limit 5          stop after 5 new downloads
#   bash Scripts/download_untranscribed_videos.sh --oldest           oldest missing shows first
#   bash Scripts/download_untranscribed_videos.sh --max-pages 80     raise the gallery page-scan cap (default 60)
#   bash Scripts/download_untranscribed_videos.sh --no-scope-filter  keep every show in the gallery, not just meetings
#   bash Scripts/download_untranscribed_videos.sh --no-search        gallery only, skip the catalog search (v3 behavior)
# ---------------------------------------------------------------------------
set -uo pipefail

SITE_ID=1
GALLERY_ID=6
BASE_SITE="https://reflect-claremont.cablecast.tv"
GALLERY_URL="$BASE_SITE/internetchannel/gallery/$GALLERY_ID?site=$SITE_ID"
PAGE_PARAM="page"          # <- if page 2+ keeps returning the same shows as page 1, this project's
                            #    hydration payload may just be a fixed recent-items window regardless
                            #    of page (that's what was observed while writing this) - harmless either
                            #    way, since a fixed window already reaches back further than anything
                            #    still needing a transcript.

# Titles must match this (case-insensitive) to be treated as an in-scope
# meeting at all...
SCOPE_INCLUDE='school board|\bs\.?a\.?u\.?\s*#?\s*6\b|\bsau board|school bud(get)? hearing|finance (committee|subcommittee)|budget.*(hearing|committee|workshop|study)|deliberative|policy committee|negotiations? committee|building committee|facilities committee|subcommittee|city council.*school board|school board.*city council'
# ...and must NOT match this, even if it also matched SCOPE_INCLUDE (a "school
# board candidates forum" contains "school board" but is not a meeting).
SCOPE_EXCLUDE='graduation|commencement|class night|recognition night|holiday concert|spring concert|candidates? forum|funding fairness|restructuring discussion|open house|science fair|spelling bee|talent show|scholarship|kindergarten screening|preschool|8th grade|the last bake sale|portrait unveiling|your candidates|candidates for|sullivan county|county budget|board of commissioners|nh issues|state budget hearing|city (council )?budget hearing|city budget public hearing|cardinal perspective|\bpsa\b|sugar river report|election results|come join us|ballot guide|movement towards excellence|smarter balance|community forum|superintendent search'
# These two patterns are evaluated by Python's re module (case-insensitive),
# so use Python syntax: \s not [[:space:]].

# Catalog search (Step 2b). Each term is sent to the Cablecast show search;
# the union of results then goes through the same scope filter as the gallery.
SEARCH_TERMS=("School Board" "SAU" "Finance Committee" "Budget" "Deliberative" "Committee")
SEARCH_RECENT_DAYS=45      # a catalog show with no video yet is reported only if this recent
SEARCH_MAX_PAGES=20        # per term, 100 shows per page

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VIDEOS="$ROOT/Input/Videos"
TRANSCRIPTS="$ROOT/Input/Transcripts"
LOG="$ROOT/Scripts/download_untranscribed_videos.log"
DEBUG_DIR="$ROOT/Scripts/.gallery_debug"

UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"

DRY=0; LIMIT=0; ORDER=newest; DEBUG=0; MAX_PAGES=60; SCOPE_FILTER=1; SEARCH=1
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run)          DRY=1 ;;
    --limit)            shift; LIMIT="${1:-0}" ;;
    --oldest)           ORDER=oldest ;;
    --debug)            DEBUG=1 ;;
    --max-pages)        shift; MAX_PAGES="${1:-60}" ;;
    --no-scope-filter)  SCOPE_FILTER=0 ;;
    --no-search)        SEARCH=0 ;;
    -h|--help)          sed -n '2,115p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done

if [ ! -d "$VIDEOS" ] || [ ! -d "$TRANSCRIPTS" ]; then
  echo "Expected folders not found under $ROOT (Input/Videos, Input/Transcripts)" >&2
  exit 1
fi
command -v python3 >/dev/null 2>&1 || { echo "python3 is required (used to parse the gallery listing) but was not found on PATH" >&2; exit 1; }
HAVE_FFMPEG=0
command -v ffmpeg >/dev/null 2>&1 && HAVE_FFMPEG=1
[ "$DEBUG" = 1 ] && mkdir -p "$DEBUG_DIR"

fetch() { # $1 = url  -> prints body to stdout, returns curl's exit code
  curl -fsSL -A "$UA" --connect-timeout 20 --max-time 90 \
       --retry 3 --retry-delay 3 --retry-all-errors "$1"
}

# ---------------------------------------------------------------------------
# Step 1 - who already has a transcript, and what's already on disk.
# ID-prefix convention throughout this project: "<show id> <title>.ext".
# ---------------------------------------------------------------------------
TRANSCRIBED_IDS=" "
for f in "$TRANSCRIPTS"/*; do
  [ -e "$f" ] || continue
  b="$(basename "$f")"
  id="$(printf '%s' "$b" | grep -oE '^[0-9]+' || true)"
  [ -n "$id" ] && TRANSCRIBED_IDS="$TRANSCRIBED_IDS$id "
done

ON_DISK_IDS=" "
for f in "$VIDEOS"/*; do
  [ -e "$f" ] || continue
  b="$(basename "$f")"
  id="$(printf '%s' "$b" | grep -oE '^[0-9]+' || true)"
  [ -n "$id" ] && ON_DISK_IDS="$ON_DISK_IDS$id "
done

is_transcribed() { case "$TRANSCRIBED_IDS" in *" $1 "*) return 0 ;; *) return 1 ;; esac; }
is_on_disk()     { case "$ON_DISK_IDS"     in *" $1 "*) return 0 ;; *) return 1 ;; esac; }

# Some recordings and transcripts carry a title-based filename with no id
# prefix ("Claremont School Board 81926.mp4.json") instead of this project's
# "<id> <title>.ext" convention, so is_on_disk()/is_transcribed() can't see
# them. Index those by the digits left in the name once its extensions are
# stripped (in practice the meeting date, M D YY) and, once a candidate's own
# title is in hand, skip it when its title's digits are exactly the same.
# Exact, not substring: "12/1/23" -> 12123 must not match "2123". This only
# ever prevents a redundant download, never touches an existing file.
declare -a ALIAS_NAME=(); declare -a ALIAS_DIGITS=()
for f in "$VIDEOS"/* "$TRANSCRIPTS"/*; do
  [ -e "$f" ] || continue
  b="$(basename "$f")"
  case "$b" in [0-9]*' '*) continue ;; esac  # id-prefixed, already covered above
  stem="$(printf '%s' "$b" | sed -E 's/(\.([Mm][Pp]4|[Mm]4[Vv]|[Mm][Oo][Vv]|[Jj][Ss][Oo][Nn]|[Cc][Ss][Vv]|[Tt][Xx][Tt]|part))+$//')"
  digits="$(printf '%s' "$stem" | tr -cd '0-9')"
  [ -n "$digits" ] || continue
  ALIAS_NAME+=("$b"); ALIAS_DIGITS+=("$digits")
done

alias_conflict() { # $1 = candidate title; echoes the matching filename, empty if none
  local tdigits i
  tdigits="$(printf '%s' "$1" | tr -cd '0-9')"
  [ -n "$tdigits" ] || return 1
  for i in "${!ALIAS_DIGITS[@]}"; do
    [ "$tdigits" = "${ALIAS_DIGITS[$i]}" ] && { printf '%s' "${ALIAS_NAME[$i]}"; return 0; }
  done
  return 1
}

# ---------------------------------------------------------------------------
# Step 2 - fetch the gallery page(s) and pull (show id, title, vod url) triples
# straight out of the embedded JSON - see the note above for why this
# replaced fetching each show's own page.
# ---------------------------------------------------------------------------
echo "Reading the CLAREMONT SCHOOLS gallery (channel $GALLERY_ID)..."
PAGES_CONCAT="$(mktemp)"
: > "$PAGES_CONCAT"
page=1; empty_streak=0; seen_ids=""
while [ "$page" -le "$MAX_PAGES" ] && [ "$empty_streak" -lt 2 ]; do
  if [ "$page" -eq 1 ]; then url="$GALLERY_URL"; else url="${GALLERY_URL}&${PAGE_PARAM}=$page"; fi
  body="$(fetch "$url")" || { echo "  page $page: fetch failed, stopping" >&2; break; }
  [ "$DEBUG" = 1 ] && printf '%s' "$body" > "$DEBUG_DIR/gallery-page-$page.html"
  ids="$(printf '%s' "$body" | grep -oE '"showId":[0-9]+' | grep -oE '[0-9]+' | sort -un)"
  new=0
  for id in $ids; do
    case " $seen_ids " in
      *" $id "*) ;;
      *) seen_ids="$seen_ids $id"; new=$((new+1)) ;;
    esac
  done
  printf '%s\n' "$body" >> "$PAGES_CONCAT"
  if [ "$new" -eq 0 ]; then empty_streak=$((empty_streak+1)); else empty_streak=0; fi
  page=$((page+1))
done
GALLERY_COUNT=$(echo $seen_ids | wc -w | tr -d ' ')
echo "  shows found in gallery: $GALLERY_COUNT (scanned $((page-1)) page(s))"
if [ "$GALLERY_COUNT" -eq 0 ]; then
  echo "  No \"showId\":N entries matched. The site may have changed how it embeds" >&2
  echo "  show data. Re-run with --debug and inspect $DEBUG_DIR/gallery-page-1.html" >&2
  echo "  for how a show's id/title/video link are represented now." >&2
  if [ "$SEARCH" = 0 ]; then rm -f "$PAGES_CONCAT"; exit 1; fi
  echo "  Continuing with the catalog search only." >&2
fi

# ---------------------------------------------------------------------------
# Step 2b - search the show catalog for meetings the gallery never listed.
# One JSON file per (term, page); Python merges them below.
# ---------------------------------------------------------------------------
API_DIR="$(mktemp -d)"
if [ "$SEARCH" = 1 ]; then
  echo "Searching the Cablecast show catalog (${#SEARCH_TERMS[@]} terms)..."
  for term in "${SEARCH_TERMS[@]}"; do
    enc="$(python3 -c 'import sys, urllib.parse; print(urllib.parse.quote(sys.argv[1]))' "$term")"
    tag="$(printf '%s' "$term" | tr -c 'A-Za-z0-9' '_')"
    offset=0; pg=0; got=0
    while [ "$pg" -lt "$SEARCH_MAX_PAGES" ]; do
      f="$API_DIR/$tag-$offset.json"
      if ! fetch "$BASE_SITE/CablecastAPI/v1/shows?site=$SITE_ID&search=$enc&page_size=100&offset=$offset&include=vod" > "$f"; then
        echo "  \"$term\": fetch failed at offset $offset, using what was read so far" >&2
        rm -f "$f"; break
      fi
      read -r total n < <(python3 -c 'import json, sys
try:
    d = json.load(open(sys.argv[1]))
    print(d.get("meta", {}).get("count", 0), len(d.get("shows", [])))
except Exception:
    print(0, 0)' "$f")
      got=$((got + n)); pg=$((pg + 1)); offset=$((offset + 100))
      [ "$n" -eq 0 ] || [ "$offset" -ge "$total" ] && break
    done
    echo "  \"$term\": $got show(s)"
    [ "$DEBUG" = 1 ] && cp "$API_DIR"/"$tag"-*.json "$DEBUG_DIR"/ 2>/dev/null
  done
fi

# id<TAB>title<TAB>vodUrl(or literally "null") for every show the gallery
# pages mentioned, scope-filtered unless --no-scope-filter was passed.
CANDIDATES_TSV="$(mktemp)"
EXCLUDED_TSV="$(mktemp)"
python3 - "$PAGES_CONCAT" "$SCOPE_FILTER" "$SCOPE_INCLUDE" "$SCOPE_EXCLUDE" \
        "$CANDIDATES_TSV" "$EXCLUDED_TSV" "$API_DIR" "$SEARCH_RECENT_DAYS" <<'PYEOF'
import datetime, glob, json, os, re, sys

pages_path, scope_filter, include_re, exclude_re, out_path, excluded_path, api_dir, recent_days = sys.argv[1:9]
scope_filter = scope_filter == "1"
recent_cutoff = datetime.date.today() - datetime.timedelta(days=int(recent_days))
inc = re.compile(include_re, re.IGNORECASE)
exc = re.compile(exclude_re, re.IGNORECASE)

body = open(pages_path, encoding="utf-8", errors="replace").read()

# Each show is a JSON object like:
#   {"showId":17594,"title":"Claremont School Board - 9/16/26",
#    "thumbnailUrl":"...","vodUrl":"https://.../vod.m3u8", ...}
# embedded directly in the gallery page's hydration data (confirmed by
# inspecting a real gallery page while writing this). Field order held for
# every entry checked; the non-greedy .*? only has to cross "thumbnailUrl",
# which is always short and present.
pat = re.compile(
    r'"showId":(\d+),"title":"((?:[^"\\]|\\.)*)".*?"vodUrl":(null|"((?:[^"\\]|\\.)*)")',
    re.DOTALL,
)

def unescape(raw):
    return json.loads('"' + raw + '"')

seen = {}  # sid -> [title, vod, source]
for m in pat.finditer(body):
    sid = int(m.group(1))
    title = unescape(m.group(2))
    vod = unescape(m.group(4)) if m.group(4) is not None else None
    seen[sid] = [title, vod, "gallery"]  # last occurrence wins if a page repeats a show
n_gallery = len(seen)

# Catalog search results: {"meta":..., "shows":[{id,title,eventDate,vods:[vodId]}],
#                          "vods":[{id, show, url}]}
api_added = 0; api_upgraded = 0; api_stale = {}
for path in sorted(glob.glob(os.path.join(api_dir, "*.json"))):
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception:
        continue
    vod_url = {v.get("id"): v.get("url") for v in d.get("vods", []) if v.get("url")}
    for s in d.get("shows", []):
        sid = s.get("id")
        if sid is None:
            continue
        url = next((vod_url[v] for v in s.get("vods", []) if v in vod_url), None)
        if sid in seen:
            # Same show the gallery listed: take the API's progressive .mp4 over an HLS playlist.
            if url and url.endswith(".mp4") and (seen[sid][1] or "").endswith(".m3u8"):
                seen[sid][1] = url; seen[sid][2] = "gallery+api-mp4"; api_upgraded += 1
            continue
        title = (s.get("title") or "").strip()
        if not url:
            try:
                ev = datetime.date.fromisoformat((s.get("eventDate") or "")[:10])
            except ValueError:
                ev = None
            if ev is None or ev < recent_cutoff:
                api_stale[sid] = (sid, title, "catalog: no video, older than cutoff")
                continue
        seen[sid] = [title, url, "catalog"]
        api_added += 1

kept = []
dropped = [v for k, v in api_stale.items() if k not in seen]
for sid, (title, vod, src) in seen.items():
    in_scope = (not scope_filter) or (bool(inc.search(title)) and not exc.search(title))
    if in_scope:
        kept.append((sid, title, vod, src))
    else:
        why = "no include match" if not inc.search(title) else "matched exclude"
        dropped.append((sid, title, f"{why} ({src})"))

with open(out_path, "w", encoding="utf-8") as f:
    for sid, title, vod, src in sorted(kept):
        f.write(f"{sid}\t{title}\t{vod if vod else 'null'}\t{src}\n")

with open(excluded_path, "w", encoding="utf-8") as f:
    for sid, title, why in sorted(dropped):
        f.write(f"{sid}\t{title}\t{why}\n")

print(f"  shows parsed from gallery         : {n_gallery}", file=sys.stderr)
print(f"  added from catalog search         : {api_added}", file=sys.stderr)
print(f"  gallery HLS links swapped for mp4 : {api_upgraded}", file=sys.stderr)
print(f"  in scope (board/SAU/committee)    : {len(kept)}", file=sys.stderr)
print(f"  out of scope                      : {len(dropped)}", file=sys.stderr)
PYEOF
rm -f "$PAGES_CONCAT"; rm -rf "$API_DIR"
if [ "$DEBUG" = 1 ]; then
  cp "$EXCLUDED_TSV" "$DEBUG_DIR/gallery_excluded.tsv"
  cp "$CANDIDATES_TSV" "$DEBUG_DIR/gallery_in_scope.tsv"
fi
rm -f "$EXCLUDED_TSV"

if [ ! -s "$CANDIDATES_TSV" ]; then
  echo "  No shows passed the scope filter. Re-run with --debug and check" >&2
  echo "  $DEBUG_DIR/gallery_excluded.tsv - if real meetings are listed there," >&2
  echo "  loosen SCOPE_INCLUDE/SCOPE_EXCLUDE near the top of this script, or" >&2
  echo "  pass --no-scope-filter to see everything the gallery lists." >&2
  rm -f "$CANDIDATES_TSV"
  exit 1
fi

# ---------------------------------------------------------------------------
# Step 3 - drop anything already transcribed or already on disk; sort the rest.
# ---------------------------------------------------------------------------
sorted_ids() {
  if [ "$ORDER" = oldest ]; then
    cut -f1 "$CANDIDATES_TSV" | sort -n
  else
    cut -f1 "$CANDIDATES_TSV" | sort -rn
  fi
}
row_for_id() { awk -F'\t' -v id="$1" '$1 == id { print; exit }' "$CANDIDATES_TSV"; }

total=0; skip_transcribed=0; skip_on_disk=0
CANDIDATE_IDS=""
while read -r id; do
  [ -n "$id" ] || continue
  total=$((total+1))
  if is_transcribed "$id"; then skip_transcribed=$((skip_transcribed+1)); continue; fi
  if is_on_disk "$id"; then skip_on_disk=$((skip_on_disk+1)); continue; fi
  CANDIDATE_IDS="$CANDIDATE_IDS $id"
done < <(sorted_ids)

todo=$(echo $CANDIDATE_IDS | wc -w | tr -d ' ')
echo "  already transcribed        : $skip_transcribed"
echo "  on disk, awaiting transcript: $skip_on_disk"
echo "  not yet transcribed or downloaded: $todo"
[ "$LIMIT" -gt 0 ] && echo "  limit: $LIMIT this run"
[ "$HAVE_FFMPEG" = 0 ] && echo "  NOTE: ffmpeg not found on PATH - any candidate needing HLS (.m3u8) will be skipped, see NEEDS_FFMPEG below"
echo

# ---------------------------------------------------------------------------
# Step 4 - fetch each candidate: curl for a plain vod.mp4, ffmpeg remux for an
# HLS vod.m3u8 (see the note at the top of this file for why the split exists).
# ---------------------------------------------------------------------------
slugify() {
  printf '%s' "$1" | sed -E 's/[\/:*?"<>|\\]/-/g; s/[[:space:]]+/ /g; s/^ +//; s/ +$//'
}

n=0; fetched=0; failed=0; no_link=0; needs_ffmpeg=0; skipped_limit=0
declare -a FAILURES=()
declare -a NEEDS_FFMPEG=()
for id in $CANDIDATE_IDS; do
  if [ "$LIMIT" -gt 0 ] && [ "$fetched" -ge "$LIMIT" ]; then
    skipped_limit=$((skipped_limit+1)); continue
  fi
  n=$((n+1))
  IFS=$'\t' read -r _ title vod src < <(row_for_id "$id")
  printf '[%s] %3d/%d  show %s (%s)  ' "$(date '+%H:%M:%S')" "$n" "$todo" "$id" "${src:-gallery}"

  if [ -z "$vod" ] || [ "$vod" = "null" ]; then
    echo "!! no video attached yet (upcoming run?) - skipped"
    FAILURES+=("$id  \"$title\"  (vodUrl is null - show may not have aired/processed yet)")
    no_link=$((no_link+1))
    continue
  fi

  slug="$(slugify "$title")"
  [ -z "$slug" ] && slug="Show $id"

  match="$(alias_conflict "$title")"
  if [ -n "$match" ]; then
    echo "already have \"$match\" (title/date match) - skipped"
    skip_on_disk=$((skip_on_disk+1))
    continue
  fi

  out="$VIDEOS/$id $slug.mp4"

  case "$vod" in
    *.mp4)
      echo "-> $(basename "$out")  [curl, progressive mp4]"
      if [ "$DRY" = 1 ]; then
        echo "     would fetch: $vod"
        fetched=$((fetched+1))
        continue
      fi
      tmp="$out.part"
      if curl -fL -A "$UA" --retry 5 --retry-delay 5 --retry-all-errors --connect-timeout 30 \
              -C - -o "$tmp" "$vod"; then
        size=$(wc -c < "$tmp" | tr -d ' ')
        if [ "$size" -lt 1000000 ]; then
          echo "  !! only ${size} bytes - not a video, leaving as $(basename "$tmp")" | tee -a "$LOG"
          FAILURES+=("$id  $slug  (too small: ${size} bytes)")
          failed=$((failed+1))
        else
          mv "$tmp" "$out"
          echo "  ok  $(du -h "$out" | cut -f1)" | tee -a "$LOG"
          fetched=$((fetched+1))
        fi
      else
        echo "  !! download failed, partial file kept for resume: $(basename "$tmp")" | tee -a "$LOG"
        FAILURES+=("$id  $slug  <- $vod")
        failed=$((failed+1))
      fi
      ;;
    *.m3u8)
      if [ "$HAVE_FFMPEG" = 0 ]; then
        echo "-> needs ffmpeg (HLS source) - skipped, see NEEDS_FFMPEG below"
        NEEDS_FFMPEG+=("$id  $slug  <- $vod")
        needs_ffmpeg=$((needs_ffmpeg+1))
        continue
      fi
      echo "-> $(basename "$out")  [ffmpeg remux, HLS]"
      if [ "$DRY" = 1 ]; then
        echo "     would fetch: $vod"
        fetched=$((fetched+1))
        continue
      fi
      tmp="$out.part.mp4"
      rm -f "$tmp"
      if ffmpeg -nostdin -loglevel error -y \
                -user_agent "$UA" \
                -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 \
                -i "$vod" -c copy "$tmp" < /dev/null; then
        size=$(wc -c < "$tmp" 2>/dev/null | tr -d ' ')
        if [ -z "$size" ] || [ "$size" -lt 1000000 ]; then
          echo "  !! ffmpeg produced only ${size:-0} bytes - leaving as $(basename "$tmp")" | tee -a "$LOG"
          FAILURES+=("$id  $slug  (ffmpeg output too small: ${size:-0} bytes)")
          failed=$((failed+1))
        else
          mv "$tmp" "$out"
          echo "  ok  $(du -h "$out" | cut -f1)" | tee -a "$LOG"
          fetched=$((fetched+1))
        fi
      else
        echo "  !! ffmpeg failed - see rerun with ffmpeg's own output for detail" | tee -a "$LOG"
        rm -f "$tmp"
        FAILURES+=("$id  $slug  <- $vod  (ffmpeg failed)")
        failed=$((failed+1))
      fi
      ;;
    *)
      echo "!! unrecognized vodUrl format ($vod) - skipped"
      FAILURES+=("$id  $slug  <- $vod  (unrecognized extension)")
      no_link=$((no_link+1))
      ;;
  esac
done
rm -f "$CANDIDATES_TSV"

echo
echo "--------------------------------------------------------------"
if [ "$DRY" = 1 ]; then
  echo "Dry run: $fetched file(s) would be fetched, $no_link had no video attached, $needs_ffmpeg need ffmpeg."
else
  echo "Downloaded  : $fetched"
  echo "Failed      : $failed"
  echo "No link yet : $no_link"
  echo "Needs ffmpeg: $needs_ffmpeg"
  [ "$skipped_limit" -gt 0 ] && echo "Left for a later run (--limit): $skipped_limit"
fi
if [ "${#FAILURES[@]}" -gt 0 ]; then
  echo
  echo "Did not complete - re-run the script to retry:"
  for f in "${FAILURES[@]}"; do echo "  $f"; done
fi
if [ "${#NEEDS_FFMPEG[@]}" -gt 0 ]; then
  echo
  echo "Skipped for lack of ffmpeg (install it - 'brew install ffmpeg' - and re-run):"
  for f in "${NEEDS_FFMPEG[@]}"; do echo "  $f"; done
fi
echo "--------------------------------------------------------------"
[ "$failed" -gt 0 ] && [ "$DRY" != 1 ] && exit 1
exit 0
