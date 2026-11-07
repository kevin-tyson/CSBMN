#!/bin/bash
#
# Copyright 2026 Kevin Tyson
# SPDX-License-Identifier: Apache-2.0
#
# download_shows.sh - fetch specific Cablecast shows by id into Input/Videos.
#
# A targeted companion to download_untranscribed_videos.sh: no gallery walk,
# no catalog search, just the show ids you name. Run it in Terminal on the
# Mac (the cloud and Cowork shells get HTTP 403 from Cablecast).
#
#     cd "/Volumes/BigData/Cowork Projects/Government Transparency Project"
#     bash Scripts/download_shows.sh                 # default: 17693 (School Board 11/4/26)
#     bash Scripts/download_shows.sh 17693 17700     # any ids you name
#     bash Scripts/download_shows.sh --dry-run 17693 # show what would happen
#
# For each id it asks /CablecastAPI/v1/shows/<id>?include=vod for the title
# and the progressive vod.mp4, then saves "<id> <title>.mp4" with "/" and
# other unsafe characters turned into "-" (same naming as the main script).
# It skips ids already in Input/Videos or Input/Transcripts, and ids listed in
# the main script's EXCLUDE_IDS (15738, the city Policy Committee) unless
# --force is given. Ctrl-C is safe: re-run and curl resumes the .part file.
# ---------------------------------------------------------------------------
set -uo pipefail

BASE="https://reflect-claremont.cablecast.tv"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
DEFAULT_IDS="17693"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VIDEOS="$ROOT/Input/Videos"
TRANSCRIPTS="$ROOT/Input/Transcripts"
LOG="$ROOT/Scripts/download_untranscribed_videos.log"
MAIN="$ROOT/Scripts/download_untranscribed_videos.sh"

DRY=0; FORCE=0; IDS=""
for a in "$@"; do
  case "$a" in
    --dry-run) DRY=1 ;;
    --force)   FORCE=1 ;;
    -h|--help) awk 'NR > 1 && !/^#/ { exit } NR > 1' "$0"; exit 0 ;;
    *[!0-9]*|"") echo "Not a show id: $a" >&2; exit 2 ;;
    *) IDS="$IDS $a" ;;
  esac
done
[ -z "$IDS" ] && IDS="$DEFAULT_IDS"

[ -d "$VIDEOS" ] && [ -d "$TRANSCRIPTS" ] || { echo "Input/Videos or Input/Transcripts not found under $ROOT" >&2; exit 1; }
command -v python3 >/dev/null || { echo "python3 is required" >&2; exit 1; }

EXCLUDE_IDS=""
[ -f "$MAIN" ] && EXCLUDE_IDS="$(sed -nE 's/^EXCLUDE_IDS="([^"]*)".*/\1/p' "$MAIN")"

have_id() { # $1 dir, $2 id
  ls "$1" 2>/dev/null | grep -qE "^$2 "
}

ok=0; skipped=0; failed=0
for id in $IDS; do
  echo "== show $id"
  case " $EXCLUDE_IDS " in
    *" $id "*) if [ "$FORCE" = 0 ]; then echo "   in EXCLUDE_IDS of download_untranscribed_videos.sh - skipped (use --force to override)"; skipped=$((skipped+1)); continue; fi ;;
  esac
  if have_id "$TRANSCRIPTS" "$id"; then echo "   already transcribed - skipped"; skipped=$((skipped+1)); continue; fi
  if ls "$VIDEOS" 2>/dev/null | grep -E "^$id " | grep -qv '\.part$'; then echo "   already in Input/Videos - skipped"; skipped=$((skipped+1)); continue; fi

  json="$(curl -fsSL -A "$UA" --connect-timeout 20 --max-time 60 --retry 3 \
          "$BASE/CablecastAPI/v1/shows/$id?site=1&include=vod")" \
    || { echo "   !! API request failed"; failed=$((failed+1)); continue; }

  IFS=$'\t' read -r title event vod < <(printf '%s' "$json" | python3 -c '
import json, sys
j = json.load(sys.stdin); s = j.get("show") or {}
urls = [v.get("url") for v in j.get("vods") or [] if v.get("url")]
mp4 = next((u for u in urls if u.endswith(".mp4")), urls[0] if urls else "")
print("\t".join([(s.get("title") or "").strip(), (s.get("eventDate") or "")[:10], mp4]))')

  echo "   title: $title   event date: $event"
  if [ -z "$vod" ]; then echo "   !! no video attached yet - skipped"; failed=$((failed+1)); continue; fi
  case "$vod" in *.mp4) ;; *) echo "   !! only an HLS stream ($vod) - use download_untranscribed_videos.sh, which remuxes with ffmpeg"; failed=$((failed+1)); continue ;; esac

  slug="$(printf '%s' "$title" | sed -E 's/[\/:*?"<>|\\]/-/g; s/[[:space:]]+/ /g; s/^ +//; s/ +$//')"
  [ -z "$slug" ] && slug="Show $id"
  out="$VIDEOS/$id $slug.mp4"; tmp="$out.part"
  echo "   -> Input/Videos/$(basename "$out")"
  echo "      from $vod"
  [ "$DRY" = 1 ] && { ok=$((ok+1)); continue; }

  if curl -fL -A "$UA" --retry 5 --retry-delay 5 --retry-all-errors --connect-timeout 30 \
          -C - -o "$tmp" "$vod"; then
    size=$(wc -c < "$tmp" | tr -d ' ')
    if [ "$size" -lt 1000000 ]; then
      echo "   !! only $size bytes - not a video, left as $(basename "$tmp")" | tee -a "$LOG"; failed=$((failed+1))
    else
      mv "$tmp" "$out"
      echo "   ok  $(du -h "$out" | cut -f1)  $(date '+%F %T') download_shows.sh $id" | tee -a "$LOG"; ok=$((ok+1))
    fi
  else
    echo "   !! download failed; re-run to resume $(basename "$tmp")" | tee -a "$LOG"; failed=$((failed+1))
  fi
done

echo
[ "$DRY" = 1 ] && echo "Dry run: $ok would be fetched, $skipped skipped, $failed problem(s)." \
               || echo "Done: $ok fetched, $skipped skipped, $failed problem(s)."
[ "$failed" = 0 ]
