# nh-iplatform

A Claude skill that pulls structured data from the New Hampshire Department of Education's iPlatform portal for any district, school, SAU, or the state, across a span of years. It drives the portal's Tableau dashboards through the Tableau Embedding API in a real browser session and reads the data tables in code, so a multi-year, multi-district pull takes one call and returns exact values. Every table it delivers carries a source line naming the tool, worksheet, filters, year convention, extraction date, and URL.

The skill is the single file `SKILL.md`. It has no scripts or other supporting files. The catalog of what iPlatform offers lives inside that file, in the Catalog section at the end, and was last refreshed 2026-09-13.

## What it covers

Question

Tool the skill uses

Years held

Indicators by district, school, or state; comparisons; rankings (45 indicators, 693 entities)

iExplore

2016 to 2025

Assessment proficiency, participation, growth, scaled scores, achievement levels, by subject, grade, and subgroup

iAchieve

2016 to 2025

One entity's report card for one year: ESSA ratings and designation, suspension and expulsion detail, school improvement funds, IDEA indicators

iReport

2018 to 2025

Federal grants (ESSER, Title I to V, IDEA, Perkins, CSI): allocated, budgeted, approved, reimbursed

iGrant

FY2020 to FY2027

Fall enrollment, ADM, free and reduced lunch, demographics, attendance, dropouts, class size, staff

Public Reports (SSRS) at my.doe.nh.gov

2012 to 2026, varies by report

A district's DOE-25 annual financial report as filed

DOE-25 filings

FY2013 to FY2025

What a metric means

iDefine, iGlossary

not applicable

When a request asks for something iPlatform does not hold (individual teacher names, bond schedules, years outside the ranges above), the skill says so in a "Warning: not found in iPlatform" block that lists what it checked and why it failed. It does not fill the gap from memory or from other sites.

## Requirements

-   A Claude plan that supports skills (Free, Pro, Max, Team, or Enterprise) with code execution enabled ([Claude Help Center](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)).
-   A browser the skill can drive. The skill supports two: Claude in Chrome (your own Chrome with the extension) and the built-in browser pane in the Claude desktop app. The Tableau dashboards need a live browser session, so the skill stops if neither is reachable.
-   Access to `jwt.nh.gov` and `my.doe.nh.gov` from that browser. The built-in browser may ask you to approve each site the first time.
-   Optional: a folder connected to the Claude desktop app, if you want intermediate results kept on your computer (see Settings).

## Installation

### Claude desktop app or claude.ai

1.  Zip the `nh-iplatform` folder so the folder itself is the root of the archive. The documentation says "The ZIP should contain the skill folder as its root (not a subfolder)", which means the zip opens to `nh-iplatform/SKILL.md`, not to a wrapper folder around it.
    -   macOS: right-click the `nh-iplatform` folder and choose Compress, or run `zip -r nh-iplatform.zip nh-iplatform` from the parent folder.
2.  In Claude, open Customize, then Skills, and choose Add. Upload `nh-iplatform.zip`.
3.  Enable the skill in Customize, then Skills.

Claude decides when to use a skill from its description, so you do not need to invoke it by name. You can still ask for it directly ("use nh-iplatform to ...").

### Claude Code (terminal)

Copy the folder to your personal skills directory so it loads in every project on that machine:

```
mkdir -p ~/.claude/skills
cp -R nh-iplatform ~/.claude/skills/
```

For a single repository, put it at `.claude/skills/nh-iplatform/SKILL.md` inside that repository and commit it. Claude Code watches these directories, so a new `SKILL.md` is picked up in the current session. Run `/reload-skills` only if the top-level `skills` directory did not exist when the session started. In Claude Code the skill can be called with `/nh-iplatform` ([Claude Code docs](https://code.claude.com/docs/en/skills)).

Untested caveat: the skill's text refers to tools that exist in the Claude desktop app (the built-in browser pane, the computer bridge, and the skill-proposal card used for updates). In a plain terminal session with the Claude in Chrome extension, the data pulls should work through Chrome, but the settings-change and catalog-refresh steps depend on the proposal card and may not.

### Verifying the install

Ask: "What does the nh-iplatform skill cover?" or run a small pull such as the example below. A correct run opens a browser tab at `jwt.nh.gov`, reads the table, and returns it with a source line.

## Usage

Describe what you want in plain terms. The skill needs three things and will use defaults for what you leave out:

Input

Default if you omit it

The information wanted (cost per pupil, enrollment, math proficiency, Title I money)

none, required

The entities (district, school, SAU, or the state)

The state if the question reads as statewide; otherwise it asks once and shows the exact names to choose from

The years

The five most recent years the tool holds; it states the default it applied

Optional inputs are the subgroup, grade, or subject, district or school grain, and the delivery format (table in chat, CSV, or xlsx).

### Example requests

-   "Claremont and Newport cost per pupil since 2016."
-   "Math and ELA proficiency for economically disadvantaged students in Claremont, 2022 to 2025."
-   "Rank every NH district by equalized valuation per pupil for the latest year."
-   "How much FY25 Title I Part A money was reimbursed to Claremont?"
-   "What is the out-of-school suspension breakdown for Stevens High School in 2024?"
-   "Which DOE-25 files are posted for Claremont?"
-   "Refresh the iPlatform catalog."

### What you get back

-   One table per indicator (entities as rows, years as columns), or one long table when there are several indicators.
-   A source line under each table, in this form: `Source: NH DOE iPlatform, iExplore, worksheet "Explore - Domain Bar View", filters ...; Extracted <date> via <URL>`.
-   A CSV or xlsx when you ask for one or when a table exceeds about 40 rows. Files are named `iplatform_<tool>_<indicator>_<entities>_<years>.csv`.
-   A warning block for any part of the request iPlatform cannot answer. Gaps stay blank in the table and are never shown as zero.

### Reading the numbers

-   Year labels are the end year of the school year (2025 means 2024-25) in iExplore, iAchieve, iReport, and the Public Reports. iGrant uses the federal fiscal year starting July 1. DOE-25 uses the district's fiscal year. The skill names the convention once in each answer.
-   Suppression and exception markers (`*N`, `*CS`, `N/A`, `<10%`) are passed through as the DOE wrote them.
-   In iExplore, the state row for a count indicator is a per-entity mean, not a statewide total. For a statewide enrollment count the skill reads the `State Totals` row of the District Fall Enrollment report instead.
-   Every number in an answer comes from a read made during that session. The skill re-pulls instead of reusing earlier figures, even when a same-day file exists in the scratch folder.

## Settings

Two settings sit near the top of `SKILL.md` under "Current values". Both are currently `session`.

Setting

Values

Effect

`browser`

`session`, `chrome`, `builtin`, `ask`

Which browser the skill drives. `session` follows the desktop app's Preferred browser setting.

`scratch`

`session`, `ask`, or an absolute folder path

Where intermediate results go. `session` uses the session's private scratchpad, which is deleted when the session ends. A folder path must be inside a folder connected to the desktop app.

To change one, ask in plain words ("set the iPlatform scratch folder to /Volumes/BigData/Cowork Projects/NHDOE iPlatform/scratch"). The skill proposes an updated copy of itself, and the change takes effect when you save the proposal. A choice made inside a request ("use Chrome for this run") applies to that run only and is never written back.

When a scratch folder is set, the skill appends one line per run to `<scratch>/runs.log`, names files `<YYYY-MM-DD>_<HHMM>_<tool>_<step>_<detail>.<ext>`, never overwrites a file, and never deletes anything in the folder.

## Keeping the catalog current

The skill runs a refresh (its Step R) when the catalog is empty, when it is more than 120 days old, when you ask for one, or when a live check contradicts it. The refresh reads the DOE landing page, probes each dashboard for sheets, filters, and parameters, lists the Public Reports subcategories, and then proposes an updated copy of the whole skill. The new catalog is kept only after you save that proposal. When the live site and the catalog disagree, the live site wins.

If you keep this folder in a GitHub repository, re-copy `SKILL.md` into it after each saved update, because the repository does not update itself.

## Troubleshooting

Symptom

Cause and fix

"Not ready" or a workbook that never loads

The portal's Tableau service may be down. The skill waits three times, reloads once, then reports an outage. Try again later.

Built-in browser says a site is not allowed

Approve `jwt.nh.gov` and `my.doe.nh.gov` at the site level when prompted.

Claude in Chrome returns "[BLOCKED: Cookie/query string data]"

Chrome's script tool refuses text that looks like a query string. The skill strips `=`, `&`, and `?` and routes long output through a page element read as text. If you see this in a hand-written script, do the same.

Row count is lower than entities times years

A name did not match or a year is not held. Names carry suffixes such as `Maple Avenue School(Claremont)`. The skill matches against the live domain and reports what it could not find.

A worksheet returns zero rows in iReport

Some worksheets stay empty until their section is shown in the profile. The skill opens the section, or takes the metric from iExplore or iAchieve.

Requested browser is unavailable

The skill says so and offers the other browser. It never switches silently.

## Rules the skill follows

-   No number is estimated or filled from memory.
-   No downloads without asking, and no direct calls to `dashboards.nh.gov`.
-   Whole-state pulls happeexample requestn only when you ask for a ranking or comparison.
-   Intermediate files go only where you chose.

## Sources

-   [How to create custom skills, Claude Help Center](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills): zip structure, Customize > Skills, plan availability, description-based invocation.
-   [Extend Claude with skills, Claude Code documentation](https://code.claude.com/docs/en/skills): personal and project skill paths, `/skill-name` invocation, reload behavior.
-   `SKILL.md` in this folder: coverage table, settings, Step N warnings, Step R refresh, hard rules, and troubleshooting details (read 2026-10-04).
-   [NH Department of Education iPlatform landing page](https://www.education.nh.gov/who-we-are/division-of-educator-and-analytic-resources/iplatform): the portal the skill reads.