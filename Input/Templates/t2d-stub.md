# `/transcript-to-dialogue` — detailed skill description

| | |
|---|---|
| **Skill name** | `transcript-to-dialogue` |
| **Kind** | Account skill (appears in the session skill list; invoked as `/transcript-to-dialogue` or triggered by matching requests) |
| **Scope** | Government Transparency Project — diarized public-meeting transcripts. Developed on Claremont / SAU 6 recordings; written to apply to any school board, city council, or committee. |
| **Bundle contents** | `SKILL.md` (6.4 KB) + `scripts/transcript_to_dialogue.py` (7.2 KB), ~14 KB total |
| **Described from** | The installed copy synced into a Cowork session on 2026-08-20 |

This file documents the skill; it is not the skill. Editing this stub changes nothing about how the skill runs — the procedure lives in the installed bundle.

## Purpose

The skill turns `Input/Transcripts/{TranscriptName}.json` — a word-level, diarized ASR transcript — into a speaker-attributed dialogue CSV at `Output/HTML/Dialogue/{TranscriptName}.CSV`, keeping every timestamp and every transcribed word while replacing anonymous "Speaker N" labels with real, verifiable people. `{TranscriptName}` is the parameter: the output keeps the exact base name of the input, spaces and date suffix included, plus the uppercase `.CSV` extension. Directory names are fixed project conventions, not to be renamed or relocated. A transcript that lives on the user's device is staged first, and the finished CSV is committed back to the device folder.

Downstream, these CSVs are what the `create-html` skill builds meeting pages from — its stub calls the dialogue CSV "the backbone of the page", and the page generator skips any meeting that lacks one. The CSV's `Start (sec)` column also feeds that skill's Cablecast `&seekto=` deep links, so timestamp fidelity here carries through to the published pages.

## The two hard rules

`SKILL.md` states that "two hard rules define success"; the rest of the procedure exists to satisfy them.

1. **Retain the data.** Every transcribed word appears verbatim in the output, ASR garbles included. What was heard is never "fixed" — a garbled "Second Sanderson" stays as-is even when the firm is known to be Plodzik & Sanderson; corrections belong in the delivery reply, not the CSV. All timestamps come straight from the source.
2. **Name only what you can defend.** Every name in the Speaker column needs an anchor in the transcript itself (roll call, self-identification, direct address) or a public record, and ideally both. Uncertainty goes in the Role column, never silently into a name.

## When it triggers

Per the registered description: whenever the user asks to turn a transcript into a dialogue, identify or name the speakers in a meeting recording or transcript, attribute diarized voices, or produce a dialogue/conversation CSV for a school board, city council, committee, or other public-meeting transcript — even if they only name a JSON file in `Input/Transcripts` or say something like "make this transcript readable" or "who is saying what".

## Inputs

- `Input/Transcripts/{TranscriptName}.json` — word-level diarized ASR. Expected schema: top-level `language`, `speakers[]` (each `{id, name: "Speaker N"}`), and `segments[]` (each `{start, duration, speaker, words[]}`, where `speaker` holds an id — a UUID in the SAU 6 files — resolved through `speakers[]`, and each word carries `text`, `start`, `confidence`). If a transcript's schema differs, the instruction is to adapt the bundled script rather than hand-roll a new pipeline, so the CSV format and integrity checks stay consistent.
- Project memory, when a roster/voice-mapping note exists for the body. `claremont_speakers` covers the Claremont School Board / SAU 6: members, staff names, common ASR garbles, and prior voice mappings. A prior mapping usually resolves most voices immediately; a new meeting then only needs its roll call checked against it.
- External corroboration: the body's official website (roster, committee chairs, term years) and local news coverage.

## Outputs

- `Output/HTML/Dialogue/{TranscriptName}.CSV` with fixed columns `Start, End, Start (sec), End (sec), Speaker, Role, Dialogue, Diarized As` — clock times as h:mm:ss.cc for video deep-links, raw seconds for analysis, and the original cluster label so attributions stay auditable. Written UTF-8 with a BOM (`utf-8-sig`). Zero-word diarizer segments are dropped.
- A closing report in the delivery reply: the voice mapping with its evidence and confidence per speaker, known ASR garbles worth a correction note, and cited sources.
- A saved or updated project-memory roster note, so the next meeting of the same body starts warm.

## Procedure

**Step 1 — Reuse what the project already knows.** Check project memory for a roster/voice-mapping note covering this body before doing anything else.

**Step 2 — Extract a working transcript.** Run the bundled script in analysis mode:

```bash
python3 scripts/transcript_to_dialogue.py "Input/Transcripts/{TranscriptName}.json" --dump-text working.txt
```

and read `working.txt` in full. It shows each segment as `[idx] start-end Speaker N: text`, plus total speech duration, per-speaker segment counts, and any zero-word segments.

**Step 3 — Attribute each diarized voice with linguistic evidence.** Diarization gives anonymous clusters; language gives identities. The skill works through six cue families, strongest first, collecting evidence per cluster rather than per line:

- Roll call / attendance, usually in the first segments. ASR mangles proper names, so the script is re-run with `--scan-names` to inspect word-level confidences and timing gaps — a "word" with a long audio gap and odd spelling is often a swallowed name (`SKILL.md`'s example: "Present our level" hiding "Present are: Lavalette").
- Self-identification ("as a board member…", "I'm the one signing every contract right now").
- Direct address and third-person references ("just so Don knows…" places a Don in the room and rules the speaker out as Don).
- Floor control: the voice that calls the meeting to order, reads the roll, moves between agenda items, and closes discussion is the chair.
- Role-specific content: the person reporting operational detail (payroll, DOE filings, hiring, vendor contracts) is staff, typically the superintendent or administrator. Members ask; staff answer.
- Institutional memory: references to long-gone officials mark long-tenured participants; needing things explained marks new ones.

Then corroborate externally. The evidentiary standard: a cue plus a record is an identification; a cue alone is a hypothesis. If an announced name matches no public roster (a minute-taker, a staff attendee), the name is kept exactly as announced and the limitation stated in the Role column — e.g. `Attendee (named in roll call; not on 2026 board roster)`. Diarization noise is expected — short interjections sometimes land in the wrong cluster. The diarizer's segmentation is kept (the `Diarized As` column preserves auditability) and notable noise is reported to the user.

**Step 4 — Generate and verify.** Write a `speakers.json` mapping every diarized label to `{name, role}`:

```json
{"Speaker 1": {"name": "Candace Crawford", "role": "School Board Chair / Finance Subcommittee Chair"},
 "Speaker 2": {"name": "Tim Broadrick", "role": "Superintendent, SAU 6"}}
```

then build the CSV:

```bash
python3 scripts/transcript_to_dialogue.py "Input/Transcripts/{TranscriptName}.json" \
    --speakers speakers.json --out "Output/HTML/Dialogue/{TranscriptName}.CSV"
```

The script refuses unmapped labels and exits non-zero unless its integrity checks pass; a failed check is treated as a bug to fix, never something to bypass. Before delivery, one skeptical pass is required: re-read the segments behind the weakest attribution hunting for counterevidence, and spot-check a few rows against the source. Then deliver and close the loop (see Outputs).

## The bundled script

`scripts/transcript_to_dialogue.py` — its docstring calls it the "deterministic half" of the skill; the judgment half, attribution, stays with the model. Python 3 standard library only. Two modes:

**Analysis dump** (`--dump-text working.txt`, optional `--scan-names "name1,name2"`), run first: writes the working transcript and prints speech duration, diarized-voice count, segments per label, and zero-word segments. The name scan prints every word-level match with segment index, label, time, and ASR confidence — built for chasing roll-call garbles.

**Final CSV** (`--speakers speakers.json --out …`; the two flags are required together), run once the mapping is settled. Before writing, it validates that every diarized label in use is mapped (the error message says to use the announced/roll-call name, with a caveat in `role`, when the person cannot be verified) and that every entry has a non-empty `name` (`role` may be empty). After writing, it self-checks and exits 1 on any failure — per the script's own comment, "a passing run is the verification record":

| Check | Meaning |
|---|---|
| Word parity | The JSON's word-object count equals the whitespace-token count of all Dialogue cells — nothing lost, nothing added |
| Monotonic timestamps | Row start times never go backward |
| end ≥ start | Every row's interval is valid |
| No empty dialogue | Zero-word segments were dropped, not written as blank rows |

It also prints row count, dropped-segment count, time span, and the per-speaker row distribution; the project's practice notes treat reconciling that distribution against the mapping as a cheap invariant check.

## Known deviations in practice

Recorded in the `claremont_speakers` project memory, not in the bundle. Anyone rerunning the skill on SAU 6 material should read that note first.

- **Empty-text word objects break the stock parity check.** The 7/21/26 JSON contains 376 empty-text word objects and the 6/19/26 JSON 351; word parity must count text tokens rather than word objects, or the stock script exits 1 on a correct CSV.
- **Merged clusters need per-segment overrides.** This diarizer merges same-sex voices into one cluster and clips sentence onsets into neighboring clusters. A patched script accepting `"__overrides__": {"<seg idx>": {name, role}}` in `speakers.json` was used for 7/21 (61 overrides) and 6/19 (68), keeping `Diarized As` auditable. Override indices must be verified against diarized labels before shipping — an audit pass on the 6/19 CSV caught two off-by-one indices.
- **One known-wrong name is shipped.** The 8/5 and 8/12 CSVs carry "Mike Campbell" for the Plodzik & Sanderson auditor; the verified name is Michael Campo. The memory note says to fix the label if those CSVs are regenerated and to flag the discrepancy when citing them.

## Delivery history

Five CSVs exist in `Output/Dialogue/` as of 2026-08-20: `School Board Finance Committee - 61926.CSV` (verified and corrected 8/19/26), `Claremont School Board 72126.CSV`, `Claremont School Board - 72926.CSV`, `Claremont School Board - 8526.CSV` (source recording undiarized — a single "Unknown" voice, split by phrase anchors), and `Claremont School Board Finance - 81226.CSV`. The inconsistent file naming follows from the base-name rule: each CSV inherits its transcript's exact name, hyphens or not.

## Sources

- `transcript-to-dialogue` skill bundle as synced 2026-08-20: `SKILL.md`, `scripts/transcript_to_dialogue.py`.
- Project memory `claremont_speakers.md`: roster, meeting mappings, tooling notes, ASR garble glossary.
- `Input/Templates/create-html-stub.md`: the downstream consumer's documented dependence on these CSVs.
- `Output/Dialogue/` directory listing, 2026-08-20 (delivery history).
