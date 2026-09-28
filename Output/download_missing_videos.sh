#!/usr/bin/env bash
#
# Copyright 2026 Kevin Tyson
# SPDX-License-Identifier: Apache-2.0
#
# Download the 81 Cablecast recordings that have no transcript yet.
#
# RUN THIS FROM A NORMAL TERMINAL ON YOUR MAC - not from Claude.
# The Cowork sandbox has no network route to reflect-claremont.cablecast.tv.
#
#   chmod +x download_missing_videos.sh
#   ./download_missing_videos.sh            # download everything
#   ./download_missing_videos.sh --dry-run  # just report sizes and what is missing
#
# Safe to re-run: finished files are skipped, partial files resume (curl -C -).
# Total size is unknown until you run --dry-run (it sums Content-Length for all 81).
# These are the web VODs, lower bitrate than the station masters already in Input/Videos,
# but 127h45m of video is still likely tens of GB. There is 5.8 TB free on BigData.
# Ctrl-C is safe; re-run to continue where it stopped.

set -uo pipefail
DEST="/Volumes/BigData/Cowork Projects/Government Transparency Project/Input/Videos"
DRY=0; [ "${1:-}" = "--dry-run" ] && DRY=1
mkdir -p "$DEST" || { echo "Cannot create $DEST"; exit 1; }

ok=0; skip=0; fail=0; failed=()
total=0

dl() {
  local out="$1" url="$2" dur="$3"
  local path="$DEST/$out"

  local remote
  remote=$(curl -sIL --max-time 60 "$url" | awk 'BEGIN{IGNORECASE=1}/^content-length:/{v=$2}END{gsub(/\r/,"",v);print v+0}')

  if [ "$DRY" = "1" ]; then
    printf '%14s  %-52s %s\n' "$remote" "$out" "$dur"
    total=$((total + remote))
    return
  fi

  if [ -f "$path" ]; then
    local local_sz; local_sz=$(stat -f%z "$path" 2>/dev/null || echo 0)
    if [ "$remote" -gt 0 ] && [ "$local_sz" -eq "$remote" ]; then
      echo "SKIP  $out (complete)"; skip=$((skip+1)); return
    fi
    echo "RESUME $out ($local_sz / $remote)"
  else
    echo "GET   $out ($dur)"
  fi

  if curl -fL --retry 5 --retry-delay 5 --retry-all-errors -C - --max-time 7200 \
          -o "$path" "$url"; then
    local now; now=$(stat -f%z "$path" 2>/dev/null || echo 0)
    if [ "$remote" -gt 0 ] && [ "$now" -ne "$remote" ]; then
      echo "  !! size mismatch: got $now expected $remote"; fail=$((fail+1)); failed+=("$out")
    else
      ok=$((ok+1))
    fi
  else
    echo "  !! FAILED $out"; fail=$((fail+1)); failed+=("$out")
  fi
}

dl "14875 SchoolBoard020123.mp4" "https://reflect-claremont.cablecast.tv/store-3/14875-Claremont-School-Board-020123-v1/vod.mp4" "2:47:53"
dl "14892 SchoolBoardDeliberative020823.mp4" "https://reflect-claremont.cablecast.tv/store-3/14892-ClaremontDeliberative020823-v1/vod.mp4" "1:53:57"
dl "14909 SchoolBoard021523.mp4" "https://reflect-claremont.cablecast.tv/store-3/14909-ClaremontSchoolBoard021523-v3/vod.mp4" "1:49:34"
dl "14911 SAU6021623.mp4" "https://reflect-claremont.cablecast.tv/store-3/14911-SAU6-Board-Meeting-021623-v1/vod.mp4" "1:39:06"
dl "14937 SchoolBoard030123.mp4" "https://reflect-claremont.cablecast.tv/store-3/14937-School-Board-030123-v1/vod.mp4" "0:58:27"
dl "14986 SAU6033023.mp4" "https://reflect-claremont.cablecast.tv/store-3/14986-SAU6-BoardMtg033023-v1/vod.mp4" "2:01:37"
dl "15003 SchoolBoard040523.mp4" "https://reflect-claremont.cablecast.tv/store-3/15003-CSB-040523-v1/vod.mp4" "2:04:23"
dl "15022 SAU6041323.mp4" "https://reflect-claremont.cablecast.tv/store-3/15022-SAU6BoardMtg041323-v1/vod.mp4" "1:10:58"
dl "15028 SchoolBoard041923.mp4" "https://reflect-claremont.cablecast.tv/store-3/15028-Claremont-School-Board-041923-v1/vod.mp4" "1:50:35"
dl "15058 SchoolBoard050323.mp4" "https://reflect-claremont.cablecast.tv/store-3/15058-ClaremontSchoolBoard050323-v1/vod.mp4" "1:48:20"
dl "15073 SAU6051123.mp4" "https://reflect-claremont.cablecast.tv/store-3/15073-SAU6-Meeting-051123-v1/vod.mp4" "0:42:29"
dl "15123 SchoolBoard060723.mp4" "https://reflect-claremont.cablecast.tv/store-3/15123-SchoolBoard060723-v1/vod.mp4" "1:45:37"
dl "15153 SchoolBoard062123.mp4" "https://reflect-claremont.cablecast.tv/store-3/15153-SchoolBoard062123-v1/vod.mp4" "1:14:51"
dl "15193 SAU6071323.mp4" "https://reflect-claremont.cablecast.tv/store-3/15193-SAU-6-071323-v1/vod.mp4" "0:29:11"
dl "15205 SchoolBoard071923.mp4" "https://reflect-claremont.cablecast.tv/store-3/15205-SchoolBoard071921-v1/vod.mp4" "2:02:30"
dl "15228 SchoolBoard080223.mp4" "https://reflect-claremont.cablecast.tv/store-3/15228-SchoolBoard080223-v1/vod.mp4" "2:40:15"
dl "15240 SchoolBoard080923.mp4" "https://reflect-claremont.cablecast.tv/store-3/15240-SchoolBoard080923-v1/vod.mp4" "2:01:47"
dl "15253 SchoolBoard081623.mp4" "https://reflect-claremont.cablecast.tv/store-3/15253-SchoolBoard081623-v2/vod.mp4" "1:14:27"
dl "15254 SAU6081723.mp4" "https://reflect-claremont.cablecast.tv/store-3/15254-SAU6-081723-v1/vod.mp4" "1:22:55"
dl "15286 SchoolBoard090623.mp4" "https://reflect-claremont.cablecast.tv/store-3/15286-SchoolBoard090623-v1/vod.mp4" "0:52:53"
dl "15311 SchoolBoard092023.mp4" "https://reflect-claremont.cablecast.tv/store-3/15311-30917-FAITH-LIFE-Fellowship-v1/vod.mp4" "1:20:39"
dl "15336 SchoolBoard100423.mp4" "https://reflect-claremont.cablecast.tv/store-3/15336-DN-Monday-October-2-2023-v1/vod.mp4" "1:26:29"
dl "15357 SchoolBoard101823.mp4" "https://reflect-claremont.cablecast.tv/store-3/15357-SchoolBoard101823-v1/vod.mp4" "1:43:25"
dl "15385 SchoolBoard110123.mp4" "https://reflect-claremont.cablecast.tv/store-3/15385-SchoolBoard110123-v1/vod.mp4" "1:29:49"
dl "15299 SAU6110923.mp4" "https://reflect-claremont.cablecast.tv/store-3/15299-SAU6Board-110923-v1/vod.mp4" "1:03:22"
dl "15413 SchoolBoard111523.mp4" "https://reflect-claremont.cablecast.tv/store-3/15413-schoolboard111523-v1/vod.mp4" "1:04:30"
dl "15443 SchoolBoardFinance113023.mp4" "https://reflect-claremont.cablecast.tv/store-3/15443-School-Board-Finance-Mtg-113023-v1/vod.mp4" "1:24:08"
dl "15444 SchoolBoardFinance120123.mp4" "https://reflect-claremont.cablecast.tv/store-3/15444-SchoolBoardFinance120123-v1/vod.mp4" "3:00:40"
dl "15452 SchoolBoardFinance120623.mp4" "https://reflect-claremont.cablecast.tv/store-3/15452-SchoolBoardFinance120623-v1/vod.mp4" "1:30:00"
dl "15453 SchoolBoard120623.mp4" "https://reflect-claremont.cablecast.tv/store-3/15453-SchoolBoard120623-v1/vod.mp4" "0:35:43"
dl "15455 SAU6120723.mp4" "https://reflect-claremont.cablecast.tv/store-3/15455-SAU6BoardMeeting120723-v2/vod.mp4" "0:39:49"
dl "15471 SchoolBoardFinance121323.mp4" "https://reflect-claremont.cablecast.tv/store-3/15471-SchoolBoardFinance121323-v1/vod.mp4" "1:37:58"
dl "15472 SAU6121423.mp4" "https://reflect-claremont.cablecast.tv/store-3/15472-SAU6121423-v1/vod.mp4" "0:22:35"
dl "15451 SchoolBoardFinance121823.mp4" "https://reflect-claremont.cablecast.tv/store-3/15451-SchoolBoardFinance121823-v1/vod.mp4" "2:24:52"
dl "15483 SchoolBoard122023.mp4" "https://reflect-claremont.cablecast.tv/store-3/15483-SchoolBoard122023-v1/vod.mp4" "1:07:07"
dl "15505 SchoolBoard010324.mp4" "https://reflect-claremont.cablecast.tv/store-3/15505-School-Board-010323-v1/vod.mp4" "1:33:43"
dl "15510 SchoolBoardFinance010524.mp4" "https://reflect-claremont.cablecast.tv/store-3/15510-SchoolBoardFin010524-v1/vod.mp4" "1:52:17"
dl "15523 SAU6011124.mp4" "https://reflect-claremont.cablecast.tv/store-3/15523-SAU6011124-TempestaRemoval-v1/vod.mp4" "0:11:41"
dl "15531 SchoolBoard011724.mp4" "https://reflect-claremont.cablecast.tv/store-3/15531-CSB-011724-v2/vod.mp4" "2:30:13"
dl "15552 SchoolBoardDeliberative020324.mp4" "https://reflect-claremont.cablecast.tv/store-3/15552-School-Board-Deliberative-020324-v1/vod.mp4" "1:33:12"
dl "15580 SAU6021524.mp4" "https://reflect-claremont.cablecast.tv/store-3/15580-SAU6-021524-v1/vod.mp4" "0:59:53"
dl "15585 SchoolBoard022124.mp4" "https://reflect-claremont.cablecast.tv/store-3/15585-SchoolBoard022124-v1/vod.mp4" "2:01:17"
dl "15607 SchoolBoard030624.mp4" "https://reflect-claremont.cablecast.tv/store-3/15607-SCSO-030424-v3/vod.mp4" "1:55:22"
dl "15638 SchoolBoard032024.mp4" "https://reflect-claremont.cablecast.tv/store-3/15638-School-Board-Meeting-032024-v2/vod.mp4" "2:09:40"
dl "15687 SAU6041124.mp4" "https://reflect-claremont.cablecast.tv/store-3/15687-SAU6-MTG-041124-v2/vod.mp4" "1:10:00"
dl "15693 SchoolBoard041724.mp4" "https://reflect-claremont.cablecast.tv/store-3/15693-SchoolBoardMtg041724-v2/vod.mp4" "1:36:45"
dl "15722 SchoolBoard051524.mp4" "https://reflect-claremont.cablecast.tv/store-3/15722-SchoolBoard051524-v2/vod.mp4" "2:03:24"
dl "15786 SchoolBoard060524.mp4" "https://reflect-claremont.cablecast.tv/store-3/15786-SchoolBoard060524-v2/vod.mp4" "1:12:05"
dl "15814 SchoolBoard062024.mp4" "https://reflect-claremont.cablecast.tv/store-3/15814-SchoolBoard062024-v2/vod.mp4" "2:02:06"
dl "15947 SchoolBoard082124.mp4" "https://reflect-claremont.cablecast.tv/store-3/15947-SchoolBoard082124-v2/vod.mp4" "1:34:05"
dl "15994 SchoolBoard090424.mp4" "https://reflect-claremont.cablecast.tv/store-3/15994-SchoolBoard090424-v2/vod.mp4" "1:06:50"
dl "16011 SAU6091224.mp4" "https://reflect-claremont.cablecast.tv/store-3/16011-SAU6-091224-v2/vod.mp4" "1:32:08"
dl "16021 SchoolBoard091824.mp4" "https://reflect-claremont.cablecast.tv/store-3/16021-SchoolBoard091824-v2/vod.mp4" "1:03:02"
dl "16046 SchoolBoardCityCouncilJoint093024.mp4" "https://reflect-claremont.cablecast.tv/store-3/16046-SchoolBoardCityCouncil093024-v3/vod.mp4" "2:10:47"
dl "16049 SchoolBoard100224.mp4" "https://reflect-claremont.cablecast.tv/store-3/16049-SchoolBoard100224-v1/vod.mp4" "0:47:14"
dl "16070 SchoolBoard101624.mp4" "https://reflect-claremont.cablecast.tv/store-3/16070-SchoolBoard101624-JN-fix-v3/vod.mp4" "2:08:11"
dl "16142 SAU6111424.mp4" "https://reflect-claremont.cablecast.tv/store-3/16142-SAU6-111424-v1/vod.mp4" "0:48:40"
dl "16155 SchoolBoardFinance111924.mp4" "https://reflect-claremont.cablecast.tv/store-3/16155-SchoolBoardFinance111924-v1/vod.mp4" "1:50:01"
dl "16157 SchoolBoard112024.mp4" "https://reflect-claremont.cablecast.tv/store-3/16157-SchoolBaord112024-v2/vod.mp4" "0:57:21"
dl "16158 SAU6112124.mp4" "https://reflect-claremont.cablecast.tv/store-3/16158-Sau6-112124-v1/vod.mp4" "0:51:52"
dl "16192 SchoolBoard120424.mp4" "https://reflect-claremont.cablecast.tv/store-3/16192-SchoolBoard120424-v1/vod.mp4" "1:25:50"
dl "16213 SAU6121224.mp4" "https://reflect-claremont.cablecast.tv/store-3/16213-SAU6-121224-v1/vod.mp4" "1:09:44"
dl "16215 SchoolBoardFinance121324.mp4" "https://reflect-claremont.cablecast.tv/store-3/16215-SchoolBoardFinance121324-v1/vod.mp4" "2:23:04"
dl "16222 SchoolBoard121824.mp4" "https://reflect-claremont.cablecast.tv/store-3/16222-SchoolBoard128124-v1/vod.mp4" "1:25:06"
dl "16226 SchoolBoardFinance121824.mp4" "https://reflect-claremont.cablecast.tv/store-3/16226-SchoolBoardFinance121824-v1/vod.mp4" "1:57:25"
dl "16881 SchoolBoardSpecial100625.mp4" "https://reflect-claremont.cablecast.tv/store-3/16881-SchoolBoard100625-v1/vod.mp4" "0:12:54"
dl "16958 SchoolBoardVacancy110525.mp4" "https://reflect-claremont.cablecast.tv/store-3/16958-CSB-Vacancy110525-v1/vod.mp4" "0:49:55"
dl "17134 SchoolBoard020426.mp4" "https://reflect-claremont.cablecast.tv/store-3/17134-SchoolBoard020426-v1/vod.mp4" "1:17:17"
dl "17125 SchoolBoardDeliberative020726.mp4" "https://reflect-claremont.cablecast.tv/store-3/17125-CSB-Deliberative-020726-v1/vod.mp4" "3:59:37"
dl "17159 SchoolBoard021826.mp4" "https://reflect-claremont.cablecast.tv/store-3/17159-SchoolBoard-021826-v1/vod.mp4" "2:56:25"
dl "17168 SchoolBoardArticle8021826.mp4" "https://reflect-claremont.cablecast.tv/store-3/17168-SchoolBoard-Article8Discussion021826-v1/vod.mp4" "0:49:28"
dl "17201 SchoolBoard030426.mp4" "https://reflect-claremont.cablecast.tv/store-3/17201-SchoolBoard030426-v1/vod.mp4" "2:03:12"
dl "17241 SchoolBoard031826.mp4" "https://reflect-claremont.cablecast.tv/store-3/17241-SchoolBoard031826-v2/vod.mp4" "2:00:46"
dl "17291 SchoolBoard040126.mp4" "https://reflect-claremont.cablecast.tv/store-3/17291-SchoolBoard-040126-v1/vod.mp4" "2:53:21"
dl "17300 SchoolBoardBroderickInterview040626.mp4" "https://reflect-claremont.cablecast.tv/store-3/17300-CSB-Superintendent-Broderick-Int-040625-v1/vod.mp4" "1:20:50"
dl "17307 SAU6040926.mp4" "https://reflect-claremont.cablecast.tv/store-3/17307-Sau6-040926-v1/vod.mp4" "1:14:50"
dl "17323 SchoolBoard041526.mp4" "https://reflect-claremont.cablecast.tv/store-3/17323-School-Board-041526-v1/vod.mp4" "1:25:03"
dl "17348 SchoolBoard050626.mp4" "https://reflect-claremont.cablecast.tv/store-3/17348-SchoolBoard050626-v1/vod.mp4" "1:55:40"
dl "17373 SchoolBoard052026.mp4" "https://reflect-claremont.cablecast.tv/store-3/17373-SchoolBoard052026-v1/vod.mp4" "2:05:44"
dl "17397 SchoolBoard060326.mp4" "https://reflect-claremont.cablecast.tv/store-3/17397-SchoolBoard060326-v1/vod.mp4" "1:52:27"
dl "17418 SchoolBoard061726.mp4" "https://reflect-claremont.cablecast.tv/store-3/17418-SchoolBoard061726-v1/vod.mp4" "1:21:25"

if [ "$DRY" = "1" ]; then
  echo
  echo "81 files, total bytes: $total  (~$((total/1024/1024/1024)) GB)"
  exit 0
fi

echo
echo "downloaded: $ok   skipped: $skip   failed: $fail"
if [ "$fail" -gt 0 ]; then
  printf 'failed:\n'; printf '  %s\n' "${failed[@]}"
  echo "Re-run the script to retry - completed files are skipped and partials resume."
  exit 1
fi
