#!/usr/bin/env bash
#
# Download the MP4 recordings of Claremont City Council meetings from the
# Claremont Cablecast site (https://reflect-claremont.cablecast.tv).
#
# How it works
#   The site's search page is backed by a public JSON API. This script runs the
#   same search ("city council" by default) against
#     /cablecastapi/v1/shows?search=...&include=vod
#   and reads the direct MP4 address ("url") from each show's video record.
#   Files are saved as:  <OUT_DIR>/<YYYY-MM-DD>_<show id>_<title>.mp4
#
# Size warning
#   The full set is roughly 600 GB (about 320 files, median 1.9 GB, largest
#   7.3 GB). Run with --list first to see sizes, then narrow the set with the
#   filters below if you do not want everything.
#
# Requires: bash, curl, jq, awk
#
# Usage
#   ./download_claremont_council_videos.sh --list    show what would be downloaded, with sizes
#   ./download_claremont_council_videos.sh           download
#   ./download_claremont_council_videos.sh --help
#
# Optional environment variables
#   OUT_DIR         destination folder                 (default ./claremont_council_videos)
#   SEARCH          search text                        (default "city council")
#   FROM_DATE       earliest meeting date, YYYY-MM-DD  (default none)
#   TO_DATE         latest meeting date, YYYY-MM-DD    (default none)
#   TITLE_INCLUDE   keep only titles matching this regex, case-insensitive
#   TITLE_EXCLUDE   drop titles matching this regex     (default "Your Candidates";
#                   set TITLE_EXCLUDE="" to keep everything the search returns)
#   LIMIT           only the N most recent matches      (default 0 = all)
#   DELAY           seconds to pause between files      (default 2)
#   BASE_URL        site address (default https://reflect-claremont.cablecast.tv)
#
# Examples
#   FROM_DATE=2025-01-01 ./download_claremont_council_videos.sh
#   LIMIT=5 ./download_claremont_council_videos.sh
#   TITLE_INCLUDE='^(special )?city council' ./download_claremont_council_videos.sh --list
#
# Safe to stop and re-run: finished files are skipped and partial downloads
# (*.part) resume where they left off.

set -u

BASE_URL="${BASE_URL:-https://reflect-claremont.cablecast.tv}"
BASE_URL="${BASE_URL%/}"
SEARCH="${SEARCH:-city council}"
OUT_DIR="${OUT_DIR:-./claremont_council_videos}"
FROM_DATE="${FROM_DATE:-}"
TO_DATE="${TO_DATE:-}"
TITLE_INCLUDE="${TITLE_INCLUDE:-}"
TITLE_EXCLUDE="${TITLE_EXCLUDE-Your Candidates}"
LIMIT="${LIMIT:-0}"
PAGE_SIZE="${PAGE_SIZE:-1000}"
DELAY="${DELAY:-2}"
UA="Mozilla/5.0 (compatible; council-video-archiver)"

usage() {
  sed -n '2,/^set -u/p' "$0" | sed '$d' | sed 's/^# \{0,1\}//'
}

LIST_ONLY=0
case "${1:-}" in
  --list) LIST_ONLY=1 ;;
  -h|--help) usage; exit 0 ;;
  "") ;;
  *) echo "Unknown option: $1" >&2; echo "Try --help" >&2; exit 1 ;;
esac

for tool in curl jq awk; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "Missing required tool: $tool" >&2
    exit 1
  fi
done

case "$LIMIT" in
  ''|*[!0-9]*) echo "LIMIT must be a whole number, got: $LIMIT" >&2; exit 1 ;;
esac

# ---------- helpers ----------

# Size in bytes of a local file.
fsize() { wc -c < "$1" | tr -d ' '; }

# Size in bytes the server reports for a URL (empty if unknown).
remote_size() {
  curl -sIL -A "$UA" "$1" </dev/null | tr -d '\r' |
    awk 'tolower($1) == "content-length:" { v = $2 } END { if (v != "") print v }'
}

# Human readable size.
human() {
  awk -v b="$1" 'BEGIN { if (b >= 1e9) printf "%.2f GB", b / 1e9; else printf "%.1f MB", b / 1e6 }'
}

# Free space in bytes on the filesystem holding $1.
free_bytes() {
  df -Pk "$1" 2>/dev/null | awk 'NR == 2 { print $4 * 1024 }'
}

# ---------- get the listing ----------

enc_search="$(jq -rn --arg s "$SEARCH" '$s | @uri')"
api_url="$BASE_URL/cablecastapi/v1/shows?search=${enc_search}&page_size=${PAGE_SIZE}&include=vod"

echo "Searching for \"$SEARCH\" ..." >&2
json="$(curl -fsS -A "$UA" "$api_url" </dev/null)" || {
  echo "Could not fetch the show listing from: $api_url" >&2
  exit 1
}

api_total="$(printf '%s' "$json" | jq -r '.meta.count // 0' 2>/dev/null)"
api_returned="$(printf '%s' "$json" | jq -r '(.shows // []) | length' 2>/dev/null)"
if [ -z "$api_returned" ]; then
  echo "The response was not the JSON this script expects." >&2
  exit 1
fi
if [ "$api_returned" -lt "$api_total" ]; then
  echo "WARN: the site reports $api_total shows but returned $api_returned. Try a larger PAGE_SIZE." >&2
fi

# Fields (tab separated): date, show id, mp4 url, file-name slug, title
rows="$(
  printf '%s' "$json" | jq -r \
    --arg from "$FROM_DATE" --arg to "$TO_DATE" \
    --arg inc "$TITLE_INCLUDE" --arg exc "$TITLE_EXCLUDE" \
    --argjson limit "$LIMIT" '
    (.vods // [] | map({key: (.id | tostring), value: .}) | from_entries) as $v
    | [ .shows[]
        | . as $s
        | ($s.vods // [])[]
        | ($v[tostring] // empty)
        | select((.url // "") | test("\\.mp4([?].*)?$"; "i"))
        | select((.disabled // false) | not)
        | { date: (($s.eventDate // "")[0:10]),
            id: $s.id,
            url: .url,
            title: (($s.title // "") | gsub("^\\s+|\\s+$"; "")) }
      ]
    | map(select($from == "" or .date >= $from))
    | map(select($to == "" or .date <= $to))
    | map(select($inc == "" or (.title | test($inc; "i"))))
    | map(select($exc == "" or ((.title | test($exc; "i")) | not)))
    | sort_by(.date) | reverse
    | (if $limit > 0 then .[:$limit] else . end)
    | .[]
    | [ .date,
        (.id | tostring),
        .url,
        (.title | gsub("[^A-Za-z0-9]+"; "_") | gsub("^_+|_+$"; "") | .[0:80]),
        .title ]
    | @tsv
  '
)" || {
  echo "Could not parse the listing (check TITLE_INCLUDE / TITLE_EXCLUDE regex syntax)." >&2
  exit 1
}

if [ -z "$rows" ]; then
  echo "No MP4 recordings matched." >&2
  exit 0
fi

n_sel="$(printf '%s\n' "$rows" | grep -c .)"
mkdir -p "$OUT_DIR"
MANIFEST="$OUT_DIR/manifest.tsv"
FAILED="$OUT_DIR/failed.tsv"
printf '%s\n' "$rows" | cut -f1,2,3,5 > "$MANIFEST"
: > "$FAILED"

echo "$n_sel recordings selected (of $api_total search results; the rest have no downloadable MP4 or were filtered out)." >&2

# ---------- list mode ----------

if [ "$LIST_ONLY" -eq 1 ]; then
  total_bytes=0
  while IFS=$'\t' read -r date id url slug title; do
    size="$(remote_size "$url")"
    if [ -n "$size" ]; then
      total_bytes=$((total_bytes + size))
      printf '%s  %10s  %s\n    %s\n' "$date" "$(human "$size")" "$title" "$url"
    else
      printf '%s  %10s  %s\n    %s\n' "$date" "unknown" "$title" "$url"
    fi
  done <<< "$rows"
  echo
  echo "Total: $n_sel files, $(human "$total_bytes")"
  echo "Manifest: $MANIFEST"
  exit 0
fi

# ---------- download ----------

trap 'echo; echo "Interrupted. Partial files (*.part) are kept and will resume on the next run." >&2; exit 130' INT TERM

n_ok=0
n_skip=0
n_fail=0
i=0

while IFS=$'\t' read -r date id url slug title; do
  i=$((i + 1))
  dest="$OUT_DIR/${date}_${id}_${slug}.mp4"
  part="$dest.part"

  if [ -s "$dest" ]; then
    n_skip=$((n_skip + 1))
    continue
  fi

  expected="$(remote_size "$url")"
  have=0
  [ -f "$part" ] && have="$(fsize "$part")"

  # A .part larger than the real file cannot be resumed; start over.
  if [ -n "$expected" ] && [ "$have" -gt "$expected" ]; then
    rm -f "$part"
    have=0
  fi

  if [ -n "$expected" ]; then
    echo "[$i/$n_sel] $date  $title  ($(human "$expected"))"
    need=$((expected - have))
    avail="$(free_bytes "$OUT_DIR")"
    if [ -n "$avail" ] && [ "$need" -gt "$avail" ]; then
      echo "Not enough free disk space for the next file (need $(human "$need"), have $(human "$avail")). Stopping." >&2
      echo "Free some space and re-run; finished files will be skipped." >&2
      exit 3
    fi
  else
    echo "[$i/$n_sel] $date  $title  (size unknown)"
  fi

  attempt=1
  while [ "$attempt" -le 3 ]; do
    if [ -n "$expected" ] && [ -f "$part" ] && [ "$(fsize "$part")" -eq "$expected" ]; then
      break
    fi
    if curl -fL -C - -# --retry 3 --retry-delay 5 -A "$UA" -o "$part" "$url" </dev/null; then
      break
    fi
    attempt=$((attempt + 1))
    sleep 5
  done

  if [ -f "$part" ] && { [ -z "$expected" ] || [ "$(fsize "$part")" -eq "$expected" ]; }; then
    mv "$part" "$dest"
    n_ok=$((n_ok + 1))
  else
    n_fail=$((n_fail + 1))
    printf '%s\t%s\t%s\n' "$date" "$url" "$title" >> "$FAILED"
    echo "FAILED: $title ($url)" >&2
  fi

  sleep "$DELAY"
done <<< "$rows"

echo
echo "Downloaded: $n_ok   Already present: $n_skip   Failed: $n_fail   (selected: $n_sel)"
echo "Files:    $OUT_DIR"
echo "Manifest: $MANIFEST"
if [ "$n_fail" -gt 0 ]; then
  echo "Failures: $FAILED (re-run to retry them)"
  exit 2
fi
