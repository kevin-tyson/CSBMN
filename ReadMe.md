# Government Transparency Project

Machine-assisted public-records pipeline for Claremont, New Hampshire and SAU 6.
It turns public meeting recordings, agendas, packets and minutes into
speaker-attributed transcripts and dense, citation-backed, Section 508 meeting
pages.

**AI-generated content from official sources. Not warranted for any use.**
See [DISCLAIMER.md](DISCLAIMER.md) before relying on anything here.

---

## What this is

This repository holds the tooling and published output of a project that
converts public meetings of the Claremont School Board, the SAU 6 board and
related Claremont bodies into a searchable public record.

The pipeline takes a meeting recording, produces a diarized transcript, replaces
anonymous speaker labels with named participants verified against agendas and
minutes, and renders a per-meeting HTML page carrying:

* the meeting's basic facts and every participant, including citizens who spoke
  at public comment
* the official agenda as published
* timestamped topics whose snippets expand on hover and on keyboard focus
* quoted exchanges, each linking back to the exact second of the official
  Cablecast recording
* flags where the record raises a question under New Hampshire's Right-to-Know
  Law (RSA 91-A) or another cited statute, with the statute's text linked
* a source appendix naming every document the page drew on

Coverage runs January 2015 to the present. As of 29 September 2026: 312
meetings with transcripts, dialogue and pages, from 21 January 2015 to
16 September 2026 (313 transcripts and dialogue files, one meeting having a
second recording), with `MAP.md` (317 sections) mapping them to their Drive
packets, minutes and recordings.

The published pages are served as the **Claremont School Board Meeting
Navigator** (<https://csbmn.claremontv.org/>), an experimental service of
Claremont Community Television (CCTV) / Claremont Community Media Center
(CCMC). See [Affiliation](#affiliation).

Source video is not redistributed here. Each meeting links to the Cablecast
recording published by Claremont Community Television (CCTV) / Claremont
Community Media Center (CCMC) and to the Google Drive packet and minutes files
the district publishes.

## What this is not

It is not legal advice, it is not a finding of any violation, and it is not the
official record of any meeting. A concern flag means a machine reading of the
record raised a question a human should look at, and a flag is always about the
conduct of the public body, never about a member of the public.

Residents who give public comment are named in full, because they state their
name and ward on the record at a noticed and cablecast meeting. The protections
they are owed are accuracy controls rather than anonymity, and any of them may
have their name removed from a page on request without giving a reason. Read
[DISCLAIMER.md](DISCLAIMER.md) in full.

The maintainer has personally participated in some of the proceedings covered
here. That is disclosed in [CONFLICTS.md](CONFLICTS.md).

---

## Workflow

### 1. Video processing

* Download the MP4.
* Extract a diarized transcript in JSON using Adobe Premiere Pro, into
  `Input/Transcripts/`.
* Transform the transcript into attributed dialogue with the
  **`/transcript-to-dialogue`** skill, producing `Output/HTML/Dialogue/{name}.CSV`.

### 2. Gather documents

* Find the packets and minutes for the meeting in the SAU 6 Google Drive shares
  and record their location in `MAP.md`, using **`/update-google-drive-map`**.
* Find the Cablecast VOD URL for the meeting and record it in `MAP.md`, using
  **`/full-map-update`**.

Use `/full-map-update` whenever video links are in scope; use
`/update-google-drive-map` alone only for purely Drive questions.

### 3. Process meetings

* Generate any missing pages with **`/create-html`**. It is incremental by
  default and rebuilds only what changed.

### 4. Verify

Run the audits in `Scripts/` on every batch, without exception:

| Script | Checks |
| --- | --- |
| `validate_pages.py` | structure and cross-page links, run against a directory holding *all* pages |
| `verify_quotes.py` | every quotation against the transcript corpus |
| `verify_dialogue.py` | dialogue CSV integrity against its source transcript |

Also audit, every batch: that every citation URL is on the verified closed list;
that every `seekto=N` equals a real `Start (sec)` in the CSV and renders the
displayed `H:MM:SS` from that same N; and that the index links resolve both ways.

---

## Layout

```
Input/
  Videos/              source MP4s, NOT in version control (~237 GB)
  Transcripts/         diarized transcript JSON, one per meeting
  Agendas/  Minutes/   local scratch for third-party records, not committed
  SupportingDocuments/
    MAP.md             the meeting to document and recording map
  Templates/           stubs for the skills
Output/
  HTML/                published meeting pages, index.html, style.css
    Dialogue/          speaker-attributed dialogue CSVs, published with the pages
  Reports/             cross-meeting reports
  CCTV-CCMC-Site/      explainer page for the CCTV/CCMC website
Scripts/               pipeline and audit code, plus build briefings
```

`Output/HTML/style.css` injects the required disclaimer through `body::after`.
That is a required feature of the output, not a style choice. A build that
renders pages without it is a defective build.

---

## Working with this repository

Source video is excluded by `.gitignore` and must stay excluded. GitHub blocks
files over 100 MiB, warns over 50 MiB, and recommends repositories stay under
1 GB; `Input/Videos/` alone is roughly 237 GB, which Git LFS does not solve at
that scale. Generated bundles (`Output/CSBMN-*.pdf`, `.DOCX`, the HTML zips) are
regenerable from `Scripts/html_to_docx_csbmn.py` and belong on a GitHub Release
rather than in history.

Anything committed once and later deleted still sits in history and still counts
against repository size. Get `.gitignore` right before the first commit.

---

## Licensing

This repository is licensed in two layers.

| Layer | What it covers | License |
| --- | --- | --- |
| Software | the `.py` and `.sh` files under `Scripts/` and `Output/`, each carrying an SPDX header | [Apache License 2.0](LICENSE) |
| Output and data | `Output/HTML/` (including `Output/HTML/Dialogue/`), `Input/Transcripts/`, `Scripts/speakers/`, `Scripts/*.md`, `MAP.md`, project documentation | [CC BY 4.0](LICENSE-DATA) |

Three limits on the second grant, set out in full in [LICENSE-DATA](LICENSE-DATA):

1. **Facts are not licensed, because they cannot be.** Dates, votes, dollar
   figures and the rest may be used freely and without attribution. What CC BY
   covers is the expression layered over them.
2. **District and third-party documents are not licensed here.** 17 U.S.C. § 105
   removes copyright only from *federal* works, and RSA 91-A confers access
   without addressing reuse. This project links to the district's copies rather
   than mirroring them.
3. **The warranty disclaimer is not severable.** CC BY 4.0 § 3(a)(1)(D) requires
   retaining it. Copy a page, carry the disclaimer.

New `.py` and `.sh` files must carry the `SPDX-License-Identifier: Apache-2.0`
header that the existing ones do, so the boundary stays unambiguous when a
script is copied out on its own. The speaker maps and briefings under `Scripts/`
are data, not code, and are covered by `LICENSE-DATA`.

## Attribution

    Government Transparency Project (Kevin Tyson), <URL>, licensed CC BY 4.0.
    AI-generated content from official sources; not warranted for any use.

## Corrections

Open an issue. Errors of fact are corrected and the page notes the correction.
Requests from a private individual to remove their name are acted on without
requiring a reason. See [DISCLAIMER.md](DISCLAIMER.md).

## Affiliation

The Claremont School Board Meeting Navigator, which publishes this project's
output, is an experimental service of Claremont Community Television (CCTV) /
Claremont Community Media Center (CCMC). CCTV and CCMC are one organization
under two names; it also produces and publishes the meeting recordings the
pages are built from. The maintainer's seat on its board is disclosed in
[CONFLICTS.md](CONFLICTS.md).

This project is not affiliated with, endorsed by, or authorized by the
Claremont School District, SAU 6, or the City of Claremont. Their names are
used only to identify the public proceedings that are its subject.
