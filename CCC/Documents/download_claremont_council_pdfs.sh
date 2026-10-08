#!/usr/bin/env bash
#
# Download every council minutes, agenda, packet and related PDF listed at
# https://www.claremontnh.com/council-minutes
#
# How it works: the page fills its list from
#   https://www.claremontnh.com/get-resources.php?my=YYYYMM&grpid=24
# which returns JSON of [title, url] pairs. This script asks for each month,
# keeps the entries that point to a .pdf on claremontnh.com, and saves them to
#   <OUT_DIR>/<YYYY>/<YYYYMM>/<original file name>
#
# Requires: bash, curl, jq
#
# Usage:
#   ./download_claremont_council_pdfs.sh          download everything
#   ./download_claremont_council_pdfs.sh --list   only print what would be downloaded
#
# Optional environment variables:
#   OUT_DIR      destination folder          (default ./claremont_council_pdfs)
#   START_YEAR   first year to fetch         (default 2015)
#   END_YEAR     last year to fetch          (default current year)
#   DELAY        seconds between downloads   (default 0.5)
#
# Safe to re-run: files already on disk are skipped.

set -u

BASE="https://www.claremontnh.com"
GRPID=24
OUT_DIR="${OUT_DIR:-./claremont_council_pdfs}"
START_YEAR="${START_YEAR:-2015}"
CUR_Y="$(date +%Y)"
CUR_M=$((10#$(date +%m)))
END_YEAR="${END_YEAR:-$CUR_Y}"
DELAY="${DELAY:-0.5}"
UA="Mozilla/5.0 (compatible; council-pdf-archiver)"

LIST_ONLY=0
if [ "${1:-}" = "--list" ]; then
  LIST_ONLY=1
fi

for tool in curl jq; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "Missing required tool: $tool" >&2
    exit 1
  fi
done

mkdir -p "$OUT_DIR"
MANIFEST="$OUT_DIR/manifest.tsv"
FAILED="$OUT_DIR/failed.tsv"
: > "$MANIFEST"
: > "$FAILED"

# Fetch one URL to a destination. Returns 0 on success, 1 on HTTP/network
# failure, 2 if the response is not a PDF.
fetch_pdf() {
  local url="$1" dest="$2" tmp="$2.part"
  curl -fsSL --retry 3 --retry-delay 2 -A "$UA" -o "$tmp" "$url" </dev/null || {
    rm -f "$tmp"
    return 1
  }
  if [ "$(head -c 4 "$tmp")" != "%PDF" ]; then
    rm -f "$tmp"
    return 2
  fi
  mv "$tmp" "$dest"
}

n_ok=0
n_skip=0
n_fail=0
n_listed=0

for ((y = START_YEAR; y <= END_YEAR; y++)); do
  for m in 01 02 03 04 05 06 07 08 09 10 11 12; do
    if [ "$y" -eq "$CUR_Y" ] && [ $((10#$m)) -gt "$CUR_M" ]; then
      continue
    fi
    ym="${y}${m}"

    json="$(curl -fsS -A "$UA" "$BASE/get-resources.php?my=${ym}&grpid=${GRPID}" </dev/null)" || {
      echo "WARN: could not fetch the listing for $ym" >&2
      continue
    }

    # Fields: yearmonth, URL with the file name percent-encoded, file name, raw URL, title
    while IFS=$'\t' read -r _ym url file raw title; do
      [ -n "$url" ] || continue
      n_listed=$((n_listed + 1))
      printf '%s\t%s\t%s\n' "$ym" "$raw" "$title" >> "$MANIFEST"

      if [ "$LIST_ONLY" -eq 1 ]; then
        echo "$ym  $raw"
        continue
      fi

      dest_dir="$OUT_DIR/$y/$ym"
      dest="$dest_dir/$file"
      mkdir -p "$dest_dir"

      if [ -s "$dest" ]; then
        n_skip=$((n_skip + 1))
        continue
      fi

      fetch_pdf "$url" "$dest"
      rc=$?
      if [ "$rc" -eq 1 ]; then
        # Fallback: encode only spaces in the original URL.
        fetch_pdf "${raw// /%20}" "$dest"
        rc=$?
      fi

      if [ "$rc" -eq 0 ]; then
        n_ok=$((n_ok + 1))
        echo "ok    $ym  $file"
      else
        n_fail=$((n_fail + 1))
        printf '%s\t%s\texit=%s\n' "$ym" "$raw" "$rc" >> "$FAILED"
        echo "FAIL  $ym  $file (code $rc)" >&2
      fi
      sleep "$DELAY"
    done < <(
      printf '%s' "$json" | jq -r --arg ym "$ym" '
        .[]?
        | select(type == "array" and ((.[1] // "") != ""))
        | select(.[1] | test("^https?://www\\.claremontnh\\.com/.*\\.pdf$"; "i"))
        | (.[1] | sub("[^/]*$"; "")) as $dir
        | (.[1] | sub("^.*/"; "")) as $file
        | [$ym, ($dir + ($file | @uri)), $file, .[1], (.[0] // "")]
        | @tsv
      ' 2>/dev/null
    )
  done
done

echo
if [ "$LIST_ONLY" -eq 1 ]; then
  echo "Listed $n_listed PDF entries. Manifest: $MANIFEST"
else
  echo "Downloaded: $n_ok   Already present: $n_skip   Failed: $n_fail   (listed: $n_listed)"
  echo "Files:    $OUT_DIR"
  echo "Manifest: $MANIFEST"
  if [ "$n_fail" -gt 0 ]; then
    echo "Failures: $FAILED"
  fi
fi
