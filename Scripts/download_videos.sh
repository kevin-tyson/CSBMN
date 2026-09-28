#!/bin/bash
#
# Copyright 2026 Kevin Tyson
# SPDX-License-Identifier: Apache-2.0
#
# ---------------------------------------------------------------------------
# download_videos.sh - fetch the missing Claremont school board / SAU 6 / committee
# recordings from Claremont Community TV (Cablecast) into Input/Videos.
#
# Generated 2026-09-01. Run it on the Mac itself, in Terminal:
#
#     cd "/Volumes/BigData/Cowork Projects/Government Transparency Project"
#     bash Scripts/download_videos.sh
#
# It cannot run inside a Cowork session - the sandbox has no route to
# reflect-claremont.cablecast.tv.
#
#   231 files, about 440 hours, roughly 570-600 GB.
#
# Safe to stop (Ctrl-C) and re-run: finished files are skipped, and a partial
# file resumes from where it left off. Nothing already in Input/Videos is
# touched or overwritten.
#
#   bash Scripts/download_videos.sh --dry-run     list what would be fetched
#   bash Scripts/download_videos.sh --limit 10    stop after 10 new files
#   bash Scripts/download_videos.sh --oldest      oldest meetings first
#   bash Scripts/download_videos.sh --include-aliased
#                                                 also fetch meetings that already
#                                                 exist under an older title-based
#                                                 filename
# ---------------------------------------------------------------------------
set -uo pipefail

BASE="https://reflect-claremont.cablecast.tv/store-3"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$ROOT/Input/Videos"
LOG="$ROOT/Scripts/download_videos.log"

DRY=0; LIMIT=0; ORDER=newest; ALIASED=0
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY=1 ;;
    --limit)   shift; LIMIT="${1:-0}" ;;
    --oldest)  ORDER=oldest ;;
    --include-aliased) ALIASED=1 ;;
    -h|--help) sed -n '2,30p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done

if [ ! -d "$DEST" ]; then
  echo "Destination folder not found: $DEST" >&2
  exit 1
fi

# Some meetings are already in Input/Videos under older title-based filenames
# ("Claremont School Board 81926.mp4"). Rather than a fixed list, every file in
# the folder is indexed by the digits in its name, so anything downloaded by
# hand later is recognised too. Pass --include-aliased to ignore this and fetch
# by the "<show id> <Body><MMDDYY>.mp4" name regardless.
INDEX_DATE=(); INDEX_SAU=(); INDEX_NAME=()
build_index() {
  # Index ONLY files that are not already in the "<show id> <Body><MMDDYY>.mp4"
  # convention - those are matched by exact filename. For each title-based file
  # take the last run of 4+ digits, which is its date.
  local f base d sau
  for f in "$DEST"/*.mp4; do
    [ -e "$f" ] || continue
    base="$(basename "$f")"
    case "$base" in
      [0-9][0-9][0-9][0-9]\ *|[0-9][0-9][0-9][0-9][0-9]\ *) continue ;;
    esac
    d="$(printf '%s' "$base" | grep -oE '[0-9]{4,}' | tail -1)"
    [ -n "$d" ] || continue
    case "$base" in
      *SAU*|*sau*) sau=1 ;;
      *)           sau=0 ;;
    esac
    INDEX_DATE+=("$d"); INDEX_SAU+=("$sau"); INDEX_NAME+=("$base")
  done
}

MATCHED_NAME=""
have_already() {
  # $1 = target filename. True if it, or a title-named copy of the same meeting,
  # is already on disk. Sets MATCHED_NAME when it matched by date.
  MATCHED_NAME=""
  [ -f "$DEST/$1" ] && return 0
  [ "$ALIASED" = 1 ] && return 1

  local body mmddyy mm dd yy sau i v
  body="${1#* }"; body="${body%.mp4}"
  mmddyy="${body: -6}"
  case "$mmddyy" in ''|*[!0-9]*) return 1 ;; esac
  mm="${mmddyy:0:2}"; dd="${mmddyy:2:2}"; yy="${mmddyy:4:2}"
  # every spelling the station has used: 080526, 8526, 80526, 08526
  local variants="$mmddyy $((10#$mm))$((10#$dd))$yy $((10#$mm))$dd$yy $mm$((10#$dd))$yy"
  case "$1" in *SAU*) sau=1 ;; *) sau=0 ;; esac

  for i in "${!INDEX_DATE[@]}"; do
    [ "${INDEX_SAU[$i]}" = "$sau" ] || continue
    for v in $variants; do
      # exact match on the whole date run - never a substring
      if [ "${INDEX_DATE[$i]}" = "$v" ]; then
        MATCHED_NAME="${INDEX_NAME[$i]}"; return 0
      fi
    done
  done
  return 1
}

read_entries() {
  if [ "$ORDER" = oldest ]; then
    rev() { awk '{ line[NR] = $0 } END { for (i = NR; i > 0; i--) print line[i] }'; }
  else
    rev() { cat; }
  fi
  sed -e '/^#/d' -e '/^$/d' <<'ENTRIES' | rev
17529-CSB-081926-v2/vod.mp4|17529 SchoolBoard081926.mp4
17530-CSB-Finance-081226-v2/vod.mp4|17530 SchoolBoardFinance081226.mp4
17489-SchoolBoard080526-v2/vod.mp4|17489 SchoolBoard080526.mp4
17512-ClaremontSchoolBoard072926-v4/vod.mp4|17512 SchoolBoard072926.mp4
17473-SchoolBoard072126-v2/vod.mp4|17473 SchoolBoard072126.mp4
17431-SchoolBoardFinance061926-v2/vod.mp4|17431 SchoolBoardFinance061926.mp4
17095-SchoolBoard012126-v1/vod.mp4|17095 SchoolBoard012126.mp4
17116-SchoolBoardPublicHearing012026-v1/vod.mp4|17116 SchoolBoardPublicHearing012026.mp4
17092-SchoolBoard010726-v1/vod.mp4|17092 SchoolBoard010726.mp4
17046-BSOTB-December-2025-HD-v1/vod.mp4|17046 SchoolBoard121725.mp4
17037-SchoolBoard-Finance-121225-v1/vod.mp4|17037 SchoolBoard-Finance-121225.mp4
17029-SchoolBoardFinance121025-v2/vod.mp4|17029 SchoolBoardFinance121025.mp4
17017-SchoolBoard120325-v1/vod.mp4|17017 SchoolBoard120325.mp4
16982-SchoolBoard111925-v3/vod.mp4|16982 SchoolBoard111925.mp4
16976-SAU6-111325-v1/vod.mp4|16976 SAU6-111325.mp4
16951-SchoolBoard110525-v1/vod.mp4|16951 SchoolBoard110525.mp4
16896-SchoolBoard101525-v1/vod.mp4|16896 SchoolBoard101525.mp4
16882-SAU6BoardMeeting100625-v1/vod.mp4|16882 SAU6BoardMeeting100625.mp4
16872-SchoolBoard100125-v1/vod.mp4|16872 SchoolBoard100125.mp4
16857-SchoolBoard091725-v1/vod.mp4|16857 SchoolBoard091725.mp4
16833-SAU6-091125-v1/vod.mp4|16833 SAU6-091125.mp4
16831-School-Board-091025-v1/vod.mp4|16831 School Board 091025.mp4
16820-SAU6-090425-v1/vod.mp4|16820 SAU6-090425.mp4
16813-SchoolBoard090325-v1/vod.mp4|16813 SchoolBoard090325.mp4
16786-School-Board-082525-v1/vod.mp4|16786 School Board 082525.mp4
16776-SchoolBoard082025-v2/vod.mp4|16776 SchoolBoard082025.mp4
16764-School-Board-081425-v1/vod.mp4|16764 School Board 081425.mp4
16602-SchoolBoard061825-v1/vod.mp4|16602 SchoolBoard061825.mp4
16596-SAU6-061225-v1/vod.mp4|16596 SAU6-061225.mp4
16580-SchoolBoard060325-v1/vod.mp4|16580 SchoolBoard060325.mp4
16556-SchoolBoard052125-v1/vod.mp4|16556 SchoolBoard052125.mp4
16530-School-Board-050725-v1/vod.mp4|16530 School Board 050725.mp4
16477-SchoolBoard041625-v1/vod.mp4|16477 SchoolBoard041625.mp4
16463-SAU6Mtg-041025-v1/vod.mp4|16463 SAU6Mtg-041025.mp4
16433-SchoolBoard-040225-v1/vod.mp4|16433 SchoolBoard-040225.mp4
16409-SchoolBoard031925-v1/vod.mp4|16409 SchoolBoard031925.mp4
16408-SchoolSafetyForum031725-v1/vod.mp4|16408 SchoolSafetyForum031725.mp4
16371-SchoolBoard030525-v1/vod.mp4|16371 SchoolBoard030525.mp4
16351-School-Board-021925-v1/vod.mp4|16351 School Board 021925.mp4
16322-School-Board-020525-v1/vod.mp4|16322 School Board 020525.mp4
16315-School-Board-Deliberatibe-020125-v1/vod.mp4|16315 School Board Deliberatibe 020125.mp4
16286-SchoolBoard-012125-v1/vod.mp4|16286 SchoolBoard-012125.mp4
16266-SchoolBoard011525-v1/vod.mp4|16266 SchoolBoard011525.mp4
16253-SchoolBoard010725-v1/vod.mp4|16253 SchoolBoard010725.mp4
16246-SchoolBoardFinance010625-v1/vod.mp4|16246 SchoolBoardFinance010625.mp4
14847-SAU6-ClaremontBudget-v1/vod.mp4|14847 SchoolBoardBudgetHearing011723.mp4
14833-School-Board-Meeting-011123-v1/vod.mp4|14833 SchoolBoard011123.mp4
14835-School-Board-010923-v1/vod.mp4|14835 SchoolBoard010923.mp4
14822-SAU6-Board-Meeting-010323-v1/vod.mp4|14822 SAU6010323.mp4
14765-SAU6BoardMeeting120122-v1/vod.mp4|14765 SAU6120122.mp4
14728-ClaremontSchoolBoard111722-v1/vod.mp4|14728 SchoolBoard111722.mp4
14727-SAU6BoardMeeting111622-v1/vod.mp4|14727 SAU6111622.mp4
14693-Claremont-School-Board-Special-Meeting-110322-v1/vod.mp4|14693 SchoolBoardSpecial110322.mp4
14681-ClaremontSchoolBoard101922-v1/vod.mp4|14681 SchoolBoard101922.mp4
14654-SchoolBoard100522-v1/vod.mp4|14654 SchoolBoard100522.mp4
14630-v1/vod.mp4|14630 SAU6092922.mp4
14627-ClaremontSchoolBoard092122-v1/vod.mp4|14627 SchoolBoard091522.mp4
14595-SchoolBoard090722-Fixed-v6/vod.mp4|14595 SchoolBoard090722.mp4
14582-SchoolBoard082422-v1/vod.mp4|14582 SchoolBoardSpecial082422.mp4
13556-School-Board-Meeting-081722-v1/vod.mp4|13556 SchoolBoard081722.mp4
13521-SchoolBoardMeeting-072022-v1/vod.mp4|13521 SchoolBoard072022.mp4
13444-v1/vod.mp4|13444 SAU6061622.mp4
13420-v1/vod.mp4|13420 SchoolBoard061522.mp4
12400-SAU6Meeting051922-v1/vod.mp4|12400 SAU6051922.mp4
12399-ClaremontSchoolBoard051822-v1/vod.mp4|12399 SchoolBoard051822.mp4
12366-School-Board-Meeting-050422-v1/vod.mp4|12366 SchoolBoard050422.mp4
12353-SAU-6-042122-v1/vod.mp4|12353 SAU6042122.mp4
12315-School-Board-Meeting-040622-v1/vod.mp4|12315 SchoolBoard040622.mp4
12210-School-Board-Emergency-Meeting-021622-v1/vod.mp4|12210 SchoolBoard021622.mp4
12204-Claremont-School-Board-v2/vod.mp4|12204 SchoolBoardDeliberative020922.mp4
12180-022-02-02-School-Board-Meeting-v1/vod.mp4|12180 SchoolBoard020222.mp4
12151-School-Board-011822-v1/vod.mp4|12151 SchoolBoard011822.mp4
12115-School-Board-010522-v1/vod.mp4|12115 SchoolBoard010522.mp4
12088-v1/vod.mp4|12088 SAU6121621.mp4
12056-School-Board-120121-v1/vod.mp4|12056 SchoolBoard120121.mp4
12033-SAU-6-111821-v1/vod.mp4|12033 SAU6111821.mp4
12005-School-Board-110321-v1/vod.mp4|12005 SchoolBoard110321.mp4
11980-v1/vod.mp4|11980 SAU6102121.mp4
11963-v1/vod.mp4|11963 SchoolBoard102021.mp4
11933-SAU-6-Elementary-Schoo-v1/vod.mp4|11933 SAU6092021.mp4
11886-v1/vod.mp4|11886 SchoolBoard091521.mp4
11862-v1/vod.mp4|11862 SchoolBoard090121.mp4
11825-v1/vod.mp4|11825 SchoolBoard081821.mp4
11793-v1/vod.mp4|11793 SchoolBoard080421.mp4
11776-School-Board-of-7-21-21-v1/vod.mp4|11776 SchoolBoard072121.mp4
11720-SAU-6-Board-Meeting-070121-v1/vod.mp4|11720 SAU6070121.mp4
11649-v1/vod.mp4|11649 SchoolBoard060221.mp4
11510-v1/vod.mp4|11510 SchoolBoard050521.mp4
11527-VOD-School-Board-of-4-7-21-v1/vod.mp4|11527 SchoolBoard041521.mp4
11444-School-Board-of-4-7-21-v2/vod.mp4|11444 SchoolBoard040721.mp4
11390-School-Board-of-3-17-21-v1/vod.mp4|11390 SchoolBoard031721.mp4
11281-School-Board-of-2-4-21-v1/vod.mp4|11281 SchoolDistrictMeeting020421.mp4
11216-School-Board-of-1-27-21-v1/vod.mp4|11216 SchoolBoard020321.mp4
11276-School-Board-2-1-21-v1/vod.mp4|11276 SchoolDistrictMeeting020121.mp4
11262-School-Board-Budget-Meeting-of-1-13-21-v1/vod.mp4|11262 SchoolBoard011321.mp4
11175-School-Board-1-6-21-v1/vod.mp4|11175 SchoolBoard010621.mp4
11106-School-Board-of-12-16-20-v1/vod.mp4|11106 SchoolBoard121620.mp4
11127-SAU-6-Board-Meeting-of-12-10-12-High-v1.mp4|11127 SAU6121020.mp4
11056-High-v1.mp4|11056 SchoolBoard120220.mp4
11007-SCHOOL-BOARD-of-10-7-20-High-v1.mp4|11007 SchoolBoard100720.mp4
10993-SCHOOL-BOARD-MEETING-9-23-20-High-v1.mp4|10993 SchoolBoard092320.mp4
10992-SAU-6-SCHOOL-BOARD-MEETING-9-22-20-High-v1.mp4|10992 SAU6092220.mp4
10974-Claremont-School-Board-9-2-2020-High-v1.mp4|10974 SchoolBoard090220.mp4
10942-SCHOOL-BOARD-8-5-20-High-v1.mp4|10942 SchoolBoard080520.mp4
10876-SCHOOL-BOARD-632020-High-v1.mp4|10876 SchoolBoard060320.mp4
10842-SCHOOL-BOARD-5-6-20-High-v1.mp4|10842 SchoolBoard050620.mp4
10768-SCHOOL-BOARD-3-4-20-High-v1.mp4|10768 SchoolBoard030420.mp4
10722-DELIBERATIVE-SESSION-SCHOOL-BOARD-2-3-20-High-v1.mp4|10722 SchoolBoardDeliberative020120.mp4
10704-SCHOOL-BOARD-1-21-20-High-v1.mp4|10704 SchoolBoard012120.mp4
10694-SCHOOL-BOARD-1-15-20-High-v1.mp4|10694 SchoolBoard011520.mp4
10683-SCHOOL-BOARD-1-8-20-Low-v1.mp4|10683 SchoolBoard010820.mp4
10675-SAU-6-SCHOOL-BOARD-PUBLIC-HEARING-1-2-20-Low-v1.mp4|10675 SAU6010220.mp4
10649-SCHOOL-DISTRICT-SPECIAL-MEETING-12-12-19-Low-v1.mp4|10649 SchoolBoardSpecial121219.mp4
10639-SAU-6-SCHOOL-BOARD-MEETING-125-19-Low-v1.mp4|10639 SAU6120519.mp4
10638-HEARING-SCHOOL-BOARD-MEETING-12-4-19-Low-v1.mp4|10638 SchoolBoard120419.mp4
10624-SCHOOL-SP-MEETING-EDUCATION-WARRANT-11-2219-Low-v1.mp4|10624 SchoolBoardSpecial112119.mp4
10623-SCHOOL-BOARD-11-20-19-Low-v1.mp4|10623 SchoolBoard112019.mp4
10605-SCHOOL-BOARD-11-6-19-Low-v1.mp4|10605 SchoolBoard110619.mp4
10577-SCHOOL-BOARD-MEETING-10-17-19-Low-v1.mp4|10577 SchoolBoard101619.mp4
10567-SAU-10-10-19-Low-v1.mp4|10567 SAU6101019.mp4
10558-SCHOOL-BOARD-MEETING-10-1-19-1-Low-v1.mp4|10558 SchoolBoard100219.mp4
10537-SCHOOL-BOARD-9-18-19-Low-v1.mp4|10537 SchoolBoard091819.mp4
10522-SAU-SCHOOL-BOARD-0F-9-5-19-Low-v1.mp4|10522 SAU6090519.mp4
10521-school-board-9-4-19-13dB-Low-v1.mp4|10521 SchoolBoard090419.mp4
10506-SCHOOL-BOARD-MEETING-8-21-19-Low-v1.mp4|10506 SchoolBoard082119.mp4
10472-SCHOOL-BOARD-MEETING-7-31-19-Low-v1.mp4|10472 SchoolBoard073019.mp4
10463-SAU-6-MEETING-7-25-19-Low-v1.mp4|10463 SAU6072519.mp4
10407-SAU-6-SCHOOL-BOARD-6-4-19-Low-v1.mp4|10407 SAU6060419.mp4
10375-SAU-6-MEETING-5-16-19-Low-v1.mp4|10375 SAU6051619.mp4
10374-SCHOOL-BOARD-and-PRECEDURAL-DEFECT-MEETING-5-15-Low-v1.mp4|10374 SchoolBoardSpecial051519.mp4
10358-JOINT-SCHOOL-BOARD-CITY-COUNCIL-MEETING-5-6-19-Low-v1.mp4|10358 SchoolBoardCityCouncilJoint050619.mp4
10350-SCHOOL-BOARD-OF-5-1-19-Low-v1.mp4|10350 SchoolBoard050119.mp4
10330-SCHOOL-BOARD-MEETING-4-17-19-Low-v1.mp4|10330 SchoolBoard041719.mp4
10321-SAU-6-MEETING-4-11-19-Low-v1.mp4|10321 SAU6041119.mp4
10310-SCHOOL-BOARD-4-3-19-Low-v1.mp4|10310 SchoolBoard040319.mp4
10304-SAU-SCHOOL-BRD-MEETING-3-28-19-Low-v1.mp4|10304 SAU6032519.mp4
10294-SCHOOL-BOARD-OF-3-20-19-Low-v1.mp4|10294 SchoolBoard032019.mp4
10274-SCHOOL-BOARD-MEETING-3-6-19-Low-v1.mp4|10274 SchoolBoard030619.mp4
10252-SCHOOL-BOARD-2-20-19-Low-v1.mp4|10252 SchoolBoard022019.mp4
10232-DELIB-SESSION-2-6-19-Low-v1.mp4|10232 SchoolBoardDeliberative020619.mp4
10185-SCHOOL-BUDGET-HEARING-1-2-19-Low-v1.mp4|10185 SchoolBoardBudgetHearing010219.mp4
10161-8EA-SCHOOL-BOARD-MEETING-12-19-Low-v1.mp4|10161 SchoolBoard121918.mp4
10165-SAU-6-SCHOOL-BOARD-MEETING-12-13-18-Low-v1.mp4|10165 SAU6121318.mp4
10139-8EA-SCHOOL-BOARD-12-5-Low-v1.mp4|10139 SchoolBoard120518.mp4
10094-SAU-6-OF-11-08-18-Low-v1.mp4|10094 SAU6110918.mp4
10093-8EA-SCHOOL-BOARD-11-7-Low-v1.mp4|10093 SchoolBoard110718.mp4
10095-8EA-SCHOOL-BOARD-10-30-Low-v1.mp4|10095 SchoolBoard103018.mp4
10059-SAU-MEETING-OF-10-19-18-Low-v1.mp4|10059 SAU6101818.mp4
10044-SCHOOL-BOARD-10-3-18-Low-v1.mp4|10044 SchoolBoard100318.mp4
10012-8EA-SCHOOL-BOARD-9-19-Low-v1.mp4|10012 SchoolBoard091918.mp4
10002-8EA-SAU6-SCHOOL-BOARD-MEETING-9-13-Low-v1.mp4|10002 SAU6091318.mp4
9986-8EA-SCHOOL-BOARD-9-5-Low-v2.mp4|9986 SchoolBoard090518.mp4
9974-8EA-SAU-6-BOARD-MEETING-8-25-18-Low-v1.mp4|9974 SAU6082318.mp4
9950-8EA-SCHOOL-BOARD-MEETING-8-15-Low-v1.mp4|9950 SchoolBoard081518.mp4
9953-SCHOOL-CITY-JOINT-MTG-8-9-18-Low-v1.mp4|9953 SchoolBoardCityCouncilJoint080918.mp4
9928-SAU-6-OF-7-26-18-Low-v1.mp4|9928 SAU6072618.mp4
9907-8PB-SCHOOL-BOARD-7-18-Low-v1.mp4|9907 SchoolBoard071818.mp4
9906-8EA-SAU6-BOARD-MEETING-7-12-Low-v1.mp4|9906 SAU6071218.mp4
9876-SAU-6-SCHOOL-BOARD-OF-6-28-18-Low-v1.mp4|9876 SAU6062818.mp4
9849-8GEA-CITY-COUNCIL-SCHOOL-BOARD-6-21-Low-v1.mp4|9849 SchoolBoardCityCouncilJoint062118.mp4
9850-8EA-SCHOOL-BOARD-MEETING-6-20-Low-v1.mp4|9850 SchoolBoard062018.mp4
9853-SAU-SCHOOL-BOARD-6-14-18-Low-v1.mp4|9853 SAU6061418.mp4
9828-SCHOOL-BOARD-6-6-18-Low-v1.mp4|9828 SchoolBoard060618.mp4
9790-8EA-SCHOOL-BOARD-MEETING-5-16-Low-v1.mp4|9790 SchoolBoard051618.mp4
9799-SAU-6-MEETING-OF-5-10-18-Low-v1.mp4|9799 SAU6051018.mp4
9764-8EA-School-Board-5-2-18-Low-v1.mp4|9764 SchoolBoard050218.mp4
9734-8GA-COUNCIL-SCHOOL-BOARD-4-17-Low-v1.mp4|9734 SchoolBoardCityCouncilJoint042418.mp4
9740-8EA-SCHOOL-BOARD-MEETING-4-18-Low-v1.mp4|9740 SchoolBoard041818.mp4
9711-8EA-SCHOOL-BOARD-MEETING-4-4-Low-v1.mp4|9711 SchoolBoard040418.mp4
9715-8EA-SAU-SCHOOL-BOARD-MEETING-3-29-Low-v1.mp4|9715 SAU6032918.mp4
9682-8EA-SCHOOL-BOARD-MEETING-3-21-Low-v1.mp4|9682 SchoolBoard032118.mp4
9631-8EA-SCHOOL-BOARD-MEETING-2-21-Low-v1.mp4|9631 SchoolBoard022118.mp4
9602-at-10db-adjustment-SCHOOL-BOARD-DELIB-SESSION-PAR-Low-v1.mp4|9602 SchoolBoardDeliberative020818.mp4
9586-8EA-SCHOOL-BOARD-MEETING-1-31-Low-v1.mp4|9586 SchoolBoard013118.mp4
9592-8GA-JOINT-MEETING-CITY-SCHOOL-BOARD-1-30-Low-v1.mp4|9592 SchoolBoardCityCouncilJoint013018.mp4
9550-SCH-BRD-MEETING-OF-1-3-18-Low-v1.mp4|9550 SchoolBoard010318.mp4
9549-SCH-BRD-MEET-1-3-18-REEL-1-Copy-Low-v1.mp4|9549 SchoolBoard010318.mp4
9548-VOD-ONLY-SPECIIAL-SCH-BUD-HEARING-PART-2-OF-1-3-1-Low-v1.mp4|9548 SchoolBoardBudgetHearing010318.mp4
9547-for-vod-only-specail-SCHOOL-BUDGET-HEARING-1-3-1-Low-v1.mp4|9547 SchoolBoardBudgetHearing010318.mp4
9507-SCHOOL-BOARD-12-20-2017-Low-v1.mp4|9507 SchoolBoard122017.mp4
9497-PART-TWO-SCHOOL-BOARD-MEETING-12-6-17-Low-v2.mp4|9497 SchoolBoard120617.mp4
9496-for-VOD-ONLY-PART-1-SCHOOL-BOARD-MEETING-12-6-17-Low-v2.mp4|9496 SchoolBoard120617.mp4
9495-17EA-SCHOOL-BOARD-MEETING-12-6-17-High-v1.mp4|9495 SchoolBoard120617.mp4
9470-SCHOOL-BUDGET-WORK-SESSION-11-29-17-High-v1.mp4|9470 SchoolBoard112917.mp4
9442-SCHOOL-BOARD-MEETING-High-v1.mp4|9442 SchoolBoard111517.mp4
9431-7EA-SAU-BUDGET-MEETING-11-2-17-High-v1.mp4|9431 SAU6110217.mp4
9406-7EA-SCHOOL-BOARD-MEETING-11-1-17-High-v1.mp4|9406 SchoolBoard110117.mp4
9385-7EA-SCHOOL-BOARD-MEETING-10-18-17-High-v1.mp4|9385 SchoolBoard101817.mp4
9386-SAU-MEETING-OF-10-12-17-High-v1.mp4|9386 SAU6101217.mp4
9354-7EA-SCHOOL-BOARD-MEETING-10-4-17-High-v1.mp4|9354 SchoolBoard100417.mp4
9357-CITY-COUNCIL-SCHOOL-BRD-JOINT-MTG-9-28-17-High-v1.mp4|9357 SchoolBoardCityCouncilJoint092817.mp4
9328-7EA-SCHOOL-BOARD-MEETING-9-20-17-High-v1.mp4|9328 SchoolBoard092017.mp4
9315-7EA-SCHOOL-BOARD-MEETING-9-6-17-High-v1.mp4|9315 SchoolBoard090617.mp4
9268-7EA-SCHOOL-BOARD-MEETING-8-16-17-High-v1.mp4|9268 SchoolBoard081617.mp4
9248-7EA-SCHOOL-BOARD-MEETING-8-2-17-High-v1.mp4|9248 SchoolBoard080217.mp4
9170-SCHOOL-CITY-JOINT-MEETING-6-22-17-High-v1.mp4|9170 SchoolBoardCityCouncilJoint062217.mp4
9171-7EA-SCHOOL-BOARD-6-21-17-High-v1.mp4|9171 SchoolBoard062117.mp4
9128-7EA-SCHOOL-BOARD-MEETING-5-31-17-High-v1.mp4|9128 SchoolBoard053117.mp4
9098-7EA-SCHOOL-BOARD-MEETING-5-17-17-High-v1.mp4|9098 SchoolBoard051717.mp4
9073-SCHOOL-BOARD-5-3-2017-High-v1.mp4|9073 SchoolBoard050317.mp4
9041-7EA-SCHOOL-BOARD-MEETING-4-19-17-High-v1.mp4|9041 SchoolBoard041917.mp4
9020-7EA-SCHOOL-BOARD-MEETING-4-5-17-High-v1.mp4|9020 SchoolBoard040517.mp4
9010-7GAi-CITY-AND-SCHOOL-JOINT-MEETING-3-28-17-High-v1.mp4|9010 SchoolBoardCityCouncilJoint033017.mp4
8976-7EA-SCHOOL-BOARD-MEETING-3-15-17-High-v1.mp4|8976 SchoolBoard031517.mp4
8948-7EA-SCHOOL-BOARD-MEETING-3-1-17-High-v1.mp4|8948 SchoolBoard030117.mp4
8899-7EAi-SCHOOL-BOARD-BUDGET-SESSION-1-24-17-High-v1.mp4|8899 SchoolBoard012417.mp4
8884-7GA-CITY-COUNCIL-SCHOOL-BOARD-1-24-17-High-v1.mp4|8884 SchoolBoardCityCouncilJoint012417.mp4
8875-7EA-SCHOOL-BOARD-MEETING-1-18-17-High-v1.mp4|8875 SchoolBoard011817.mp4
8873-7EA-SCHOOL-BOARD-BUDGET-HEARING-1-11-17-High-v1.mp4|8873 SchoolBoard011117.mp4
8845-6EA-SCHOOL-BOARD-1-4-16-High-v1.mp4|8845 SchoolBoard010417.mp4
8815-6EA-SCHOOL-BOARD-12-21-16-High-v1.mp4|8815 SchoolBoard122116.mp4
8794-6EA-SCHOOL-BOARD-MEETING-12-7-16-High-v1.mp4|8794 SchoolBoard120716.mp4
8762-SCHOOL-BOARD-11-16-16-High-v1.mp4|8762 SchoolBoard111616.mp4
8761-6GA-JOINT-MEETING-City-Council-School-Board-11-1-High-v1.mp4|8761 SchoolBoardCityCouncilJoint111516.mp4
8732-6EA-SCHOOL-BOARD-11-2-16-High-v1.mp4|8732 SchoolBoard110216.mp4
8706-6PBi-SCHOOL-BOARD-10-19-16-High-v1.mp4|8706 SchoolBoard101916.mp4
8679-6EA-SCHOOL-BOARD-MEETING-10-5-16-High-v1.mp4|8679 SchoolBoard100516.mp4
8648-6EA-SCHOOL-BOARD-9-21-16-High-v1.mp4|8648 SchoolBoard092116.mp4
8577-6EA-SCHOOL-BOARD-8-17-16-High-v1.mp4|8577 SchoolBoard081716.mp4
8568-JOINT-MEETING-OF-CITY-COUNCIL-SCHOOL-BOARD-8-9-High-v1.mp4|8568 SchoolBoardCityCouncilJoint080916.mp4
8558-SCHOOL-BOARD-8-3-16-High-v1.mp4|8558 SchoolBoard080316.mp4
8433-SCHOOL-BOARD-MEETING-6-1-16-High-v1.mp4|8433 SchoolBoard060116.mp4
8407-SCHOOL-BOARD-5-18-16-High-v1.mp4|8407 SchoolBoard051816.mp4
8380-SCHOOL-BOARD-5-4-16-High-v1.mp4|8380 SchoolBoard050416.mp4
8313-SCHOOL_BOARD_MEETING_4-6-High.mp4|8313 SchoolBoard040616.mp4
8258-SCHOOL_BOARD_MEETING_of_3-16-16-High.mp4|8258 SchoolBoard031616.mp4
8192-SCHOOL_BOARD_MEETING_2-3-16-High.mp4|8192 SchoolBoard020316.mp4
8162-SCHOOL_BUDGET_DELIBERATIVE_SESSION_2-3-16-High.mp4|8162 SchoolBoardDeliberative020316.mp4
8114-SCHOOL_BOARD_BUDGET_STUDY_MEETING_1-9-16-High.mp4|8114 SchoolBoard010916.mp4
7408-CLAREMONT_SCHOOL_BOARD_3_4-Low.mp4|7408 SchoolBoard030415.mp4
7313-CLAREMONT_SCHOOL_BOARD_1_21-Low.mp4|7313 SchoolBoard012115.mp4
ENTRIES
}

total=0; done_already=0; fetched=0; failed=0; skipped_limit=0
declare -a FAILURES=()
declare -a ALREADY=()
build_index

# first pass: count
while IFS='|' read -r path name; do
  total=$((total+1))
  if have_already "$name"; then
    done_already=$((done_already+1))
    [ -n "$MATCHED_NAME" ] && ALREADY+=("$name  ->  already on disk as: $MATCHED_NAME")
  fi
done < <(read_entries)

todo=$((total-done_already))
echo "Claremont school board video download"
echo "  destination : $DEST"
echo "  in the list : $total"
echo "  already have: $done_already"
echo "  to fetch    : $todo"
[ "$LIMIT" -gt 0 ] && echo "  limit       : $LIMIT this run"
if [ "${#ALREADY[@]}" -gt 0 ]; then
  echo
  echo "  Skipped - the same meeting is already here under another name:"
  for a in "${ALREADY[@]}"; do echo "    $a"; done
fi
echo

n=0
while IFS='|' read -r path name; do
  out="$DEST/$name"
  if have_already "$name"; then continue; fi
  if [ "$LIMIT" -gt 0 ] && [ "$fetched" -ge "$LIMIT" ]; then
    skipped_limit=$((skipped_limit+1)); continue
  fi
  n=$((n+1))
  url="$BASE/$path"
  if [ "$DRY" = 1 ]; then
    printf '%3d/%d  %s\n           <- %s\n' "$n" "$todo" "$name" "$url"
    fetched=$((fetched+1))
    continue
  fi
  printf '[%s] %3d/%d  %s\n' "$(date '+%H:%M:%S')" "$n" "$todo" "$name"
  tmp="$out.part"
  if curl -fL --retry 5 --retry-delay 5 --retry-all-errors --connect-timeout 30 \
          -C - -o "$tmp" "$url"; then
    size=$(wc -c < "$tmp" | tr -d ' ')
    if [ "$size" -lt 1000000 ]; then
      echo "  !! only ${size} bytes - not a video, leaving as $(basename "$tmp")" | tee -a "$LOG"
      FAILURES+=("$name  (too small: ${size} bytes)")
      failed=$((failed+1))
    else
      mv "$tmp" "$out"
      echo "  ok  $(du -h "$out" | cut -f1)" | tee -a "$LOG"
      fetched=$((fetched+1))
    fi
  else
    echo "  !! download failed, partial file kept for resume: $(basename "$tmp")" | tee -a "$LOG"
    FAILURES+=("$name  <- $url")
    failed=$((failed+1))
  fi
done < <(read_entries)

echo
echo "--------------------------------------------------------------"
if [ "$DRY" = 1 ]; then
  echo "Dry run: $fetched file(s) would be downloaded."
else
  echo "Downloaded : $fetched"
  echo "Failed     : $failed"
  [ "$skipped_limit" -gt 0 ] && echo "Left for a later run (--limit): $skipped_limit"
  if [ "$failed" -gt 0 ]; then
    echo
    echo "These did not finish - re-run the script to resume them:"
    for f in "${FAILURES[@]}"; do echo "  $f"; done
  fi
fi
echo "--------------------------------------------------------------"
[ "$failed" -gt 0 ] && exit 1
exit 0
