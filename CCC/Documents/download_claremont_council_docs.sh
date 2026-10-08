#!/usr/bin/env bash
# Download all council agendas, minutes and other documents hosted on
# claremontnh.com, skipping video (Zoom, Facebook, Cablecast, video files).
#
# Source of the file list: the page https://www.claremontnh.com/council-minutes
# calls /get-resources.php?my=YYYYMM&grpid=24 and renders the JSON it returns.
# This script calls that same endpoint for every month.
#
# Usage: ./download_claremont_council_docs.sh [dest_dir] [start_year] [end_year]
# Needs: bash, curl, jq

set -euo pipefail

DEST="${1:-claremont_council_docs}"
START_YEAR="${2:-2015}"
END_YEAR="${3:-$(date +%Y)}"
BASE="https://www.claremontnh.com"
GRPID=24
DELAY=0.5   # seconds between requests, to be polite to the server

for tool in curl jq; do
  command -v "$tool" >/dev/null || { echo "Missing required tool: $tool" >&2; exit 1; }
done

mkdir -p "$DEST"
LOG="$DEST/download_log.tsv"
: > "$LOG"

ok=0; skipped=0; failed=0

for ((year = START_YEAR; year <= END_YEAR; year++)); do
  for month in 01 02 03 04 05 06 07 08 09 10 11 12; do
    ym="${year}${month}"

    listing=$(curl -fsS --retry 3 "$BASE/get-resources.php?my=${ym}&grpid=${GRPID}" || true)
    [[ -z "$listing" ]] && continue

    # Keep only entries hosted on claremontnh.com (this drops Zoom, Facebook,
    # Cablecast) and drop anything with a video file extension. Entries with a
    # null or empty URL are ignored. Spaces and odd characters in the file name
    # are percent-encoded so curl accepts the URL.
    entries=$(printf '%s' "$listing" | jq -r --arg base "$BASE" '
      (if type == "object" then to_entries | map(.value) else . end)
      | .[]
      | select(.[1] != null and .[1] != "")
      | .[1] as $u
      | select($u | test("^https?://(www\\.)?claremontnh\\.com/"))
      | select($u | test("\\.(mp4|mov|avi|mkv|wmv|m4v|webm|mp3|m4a|wav)$"; "i") | not)
      | ($u | sub("^.*/"; "")) as $name
      | ($u | sub("/[^/]*$"; "/")) as $dir
      | [.[0], ($dir + ($name | @uri)), $name]
      | @tsv' 2>/dev/null || true)

    [[ -z "$entries" ]] && continue

    outdir="$DEST/$year"
    mkdir -p "$outdir"

    while IFS=$'\t' read -r title url name; do
      # Local file name: the server's name, with path separators removed.
      safe="${name//\//_}"
      # Percent-decoding of the encoded name is not needed; $name is the raw one.
      target="$outdir/$safe"

      if [[ -s "$target" ]]; then
        skipped=$((skipped + 1))
        continue
      fi

      if curl -fsSL --retry 3 --retry-delay 2 -o "$target.part" "$url"; then
        mv "$target.part" "$target"
        ok=$((ok + 1))
        printf '%s\t%s\t%s\t%s\n' "$ym" "$title" "$url" "$target" >> "$LOG"
        echo "[ok]   $ym  $safe"
      else
        rm -f "$target.part"
        failed=$((failed + 1))
        echo "[FAIL] $ym  $url" >&2
      fi
      sleep "$DELAY"
    done <<< "$entries"

    sleep "$DELAY"
  done
done

echo
echo "Downloaded: $ok   Already present: $skipped   Failed: $failed"
echo "Files are in: $DEST   Log: $LOG"
