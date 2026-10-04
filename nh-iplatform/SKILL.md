---
name: "nh-iplatform"
description: "Pull structured NH Department of Education iPlatform data (iExplore, iAchieve, iReport, iGrant, the my.doe.nh.gov Public Reports, DOE-25 filings) through the local browser for any NH district, school, or the state over a span of years. Use whenever the user wants New Hampshire school or district numbers, such as enrollment, cost per pupil, expenditures, adequacy aid, valuation, teacher salary, staffing, class size, assessment proficiency or growth, graduation or dropout rates, ESSA ratings, suspensions, ESSER or Title grants, or DOE-25 reports, even when they only name a place (Claremont, Stevens High School, SAU 6) and a topic or years. Also use when the user says iPlatform, iExplore, iReport, iAchieve, iGrant, \"NH DOE data\", asks to refresh the iPlatform catalog, or asks to change which browser the skill uses (Chrome or the built-in Cowork browser) or where it keeps intermediate results (its scratch folder)."
---

# NH iPlatform

A data-access skill for New Hampshire's school data portal. iPlatform is two things behind one landing page: a set of Tableau dashboards (iExplore, iReport, iAchieve, iGrant, iGlossary) served through a token wrapper at `jwt.nh.gov`, and a set of SQL Server Reporting Services reports plus DOE-25 file downloads at `my.doe.nh.gov`. The Tableau dashboards expose the Tableau Embedding API in the page, so the skill sets filters and reads the data tables in code instead of clicking through charts. That is what makes multi-year, multi-district pulls cheap and exact.

The skill carries its own catalog of what the portal offers (the **Catalog** section at the end, with a refresh date). A run reads the catalog to route the request, then pulls the data in the local browser and delivers a checked, sourced table. When the catalog is empty, stale, or contradicted by the live site, the skill rediscovers the offerings and proposes an updated copy of itself with the new catalog (Step R). The user saves that proposal, and the catalog is remembered from then on.

## Settings

Settings live in the skill, beside the Catalog, and change the same way: the user asks ("set the iPlatform browser to built-in"), the skill proposes an updated copy of itself with the new value, and the change takes effect once saved. An explicit choice in a request ("use Chrome for this", "do it in the built-in browser") overrides the setting for that run only and is never written back.

| Setting | Value | Meaning |
|---|---|---|
| `browser` | `session` | Follow the desktop app's Preferred browser setting for this session. |
| | `chrome` | Always use Claude in Chrome, the user's own Chrome with the extension. |
| | `builtin` | Always use the built-in Cowork browser pane, which has its own profile. |
| | `ask` | Ask once per session which browser to use, then keep that answer for the session. |
| `scratch` | `session` | Keep intermediate results in the session's scratchpad directory. They are private and are deleted when the session ends. |
| | `ask` | Ask once per session where to keep intermediate results (offer the connected folders and `session`), then keep that answer for the session. |
| | an absolute path | Keep intermediate results in that folder on the user's computer, for example `/Volumes/BigData/Cowork Projects/NHDOE iPlatform/scratch`. It must be inside a connected folder, or become one when the user grants access. |

Current values:

`browser: session`
`scratch: session`

Whichever browser the setting or the request names is the one used. If that browser is unreachable, say so and offer the other; never switch silently, because the user may have picked one to keep the skill out of their personal Chrome, or to keep it in it.

### Scratch folder

Intermediate results are everything a run produces on the way to the answer: raw `emit()` CSVs read back through `get_page_text`, probe output from Step R, per-year or per-entity partial pulls, entity-resolution lists, SSRS page reads, and the working copy of a combined table before checking. Final deliverables (Step F) are not intermediate results and keep going where Step F puts them.

The folder is chosen in this order: an explicit choice in the request ("keep the scratch files in my iPlatform folder") for that run only, else the `scratch` setting. `ask` means one question per session; use AskUserQuestion with the connected folders from `get_device_info` plus `session` as options, then keep the answer for the session. When the user picks or names a folder:

- Confirm it exists and is inside a connected folder (`device_list_dir`). If it is not connected, call `device_request_folder_access` once for it. If access is declined or no computer is linked, say so and fall back to `session` for this run; never write intermediate files anywhere the user did not choose.
- If the chosen path names a subfolder that does not exist yet (such as `scratch`), create it with `device_bash` (`mkdir -p`).
- Write each intermediate result as soon as it is read, so a run that stalls halfway still leaves its partial pulls behind. With a working `device_bash`, write the file there directly. Otherwise write it in the workspace and copy it over with `device_commit_files`.
- Name files `<YYYY-MM-DD>_<HHMM>_<tool>_<step>_<detail>.<ext>`, for example `2026-09-28_2140_iexplore_pull_avg-cost-per-pupil_claremont-newport.csv` or `2026-09-28_2140_iexplore_probe.txt`. Never overwrite a file of the same name; add `_2`, `_3`.
- Start each run by appending one line to `<scratch>/runs.log`: timestamp, the request in the user's words, the tool and filters used. The log is how the user finds which files belong to which question.
- Never delete scratch files. The user owns that folder and clears it.
- Before a run, check the scratch folder for a file from the same tool, indicator, entities and years pulled earlier the same day. Mention it, but re-pull anyway: the Hard rules require every number in the answer to come from a read made in this session.

To change the setting, the user asks ("set the iPlatform scratch folder to /Volumes/BigData/Cowork Projects/NHDOE iPlatform/scratch"), and the skill proposes an updated copy of itself with the new `scratch` value, exactly as for `browser`. Every source line in Step F names the scratch folder when it is not `session`.

## Inputs

- A description of the information wanted, in the user's words ("cost per pupil", "how many kids", "math proficiency for economically disadvantaged students", "Title I money").
- The entities: one or more districts, schools, SAUs, or the state. If none is named and the question reads as statewide, use the state. Otherwise ask once, with the entity resolution list from Step D so the user picks the exact name.
- The time span: a year range, "latest", or "all years". Default to the five most recent years the tool holds. Say which default you applied.
- Optional: the disaggregation (subgroup, grade, subject), the grain (district or school), and the delivery format (table in chat, CSV, xlsx).

## Procedure

1. Parse the request (Step A) and settle the scratch folder (see Scratch folder).
2. Read the Catalog and route to a tool (Step B). If the Catalog is marked empty or stale, run Step R first. If no tool holds what was asked, go to Step N after a live check.
3. Open the tool in the local browser and wait for it to be ready (Step C).
4. Pull the data by filter and table read, not by scraping pixels (Step D), saving each raw read to the scratch folder.
5. Check it against the rendered dashboard and against expectations (Step E).
6. Deliver a sourced table and any files (Step F), with a Step N warning for every part of the request iPlatform could not answer.

### Step A. Parse

Write down, before touching the browser: topic words; entities as typed; years; grain; disaggregation; format. Map the topic to a catalog indicator name using the Catalog's synonym hints. When two indicators could fit (for instance "spending" could be Total Expenditures or Average Cost Per Pupil), pull both if cheap, otherwise pick the one that matches the user's unit (dollars per pupil versus total dollars) and say so.

### Step B. Route

| Ask | Tool | Why |
|---|---|---|
| One or more indicators for districts, schools, or the state across years; district-to-district comparison; rankings | iExplore | 45 indicators, 10 years, all 693 entities, in one table read |
| State assessment detail: proficiency, participation, growth, scaled scores, achievement levels, by subject, grade, and subgroup | iAchieve | The only tool with subject × grade × subgroup detail |
| One school or district's report card for one year: ESSA ratings and designation, suspension and expulsion detail by category, school improvement funds, IDEA indicators | iReport | Snapshot per entity and year, 123 metric ids |
| Federal grant money by district and program (ESSER, Title I to V, IDEA, Perkins, CSI): allocated, budgeted, approved, reimbursed | iGrant | Weekly refresh from the grants system |
| Fall enrollment by grade span, ADM, SAU totals, free and reduced lunch, demographic enrollment, attendance, dropouts and completers, class size, staff counts, codes | Public Reports (SSRS) | Tabular reports back to 2012, exportable |
| A district's DOE-25 annual financial report as filed | DOE-25 filings | Per-district xlsx by fiscal year, 2013 to 2025 |
| What a metric means | iDefine, iGlossary | Definitions; cite them when the meaning matters |

Prefer iExplore whenever it holds the indicator, because it returns every year and every entity in a single call. Use iReport only for what iExplore and iAchieve lack (designations, suspension breakdowns, SIF, IDEA).

When nothing in this table or the Catalog fits the ask, do not conclude yet. First confirm against the live site: search the iExplore `Indicator Name Clean` domain, the iAchieve metric list, the iReport `Metric Id` domain, and the Public Reports subcategory list for the topic words and their synonyms. Only when that live check also comes up empty is the item not in iPlatform; handle it with Step N. If the live check finds it, the Catalog is out of date: answer from the live finding and fix the Catalog through Step R.

### Step C. Open

Pick the browser in this order: an explicit choice in the request, else the `browser` setting above (`session` means the desktop app's Preferred browser; `ask` means one question, then remember the answer for the session). Say which browser is in use in the source line ("via Chrome" or "via the built-in browser"). Load that browser's tools in one ToolSearch call, create one tab and reuse it, and close it when done unless the user wants it open. If the chosen browser is unreachable, say so and offer the other rather than switching. If no browser is reachable, stop: the Tableau tools need a real browser session, and WebFetch cannot run the Embedding API.

The two browsers run the same procedure and the same JavaScript, and were both verified against iExplore on 2026-09-14. They differ in tool names and in how much a script may return:

| | Claude in Chrome | Built-in Cowork browser |
|---|---|---|
| Tools | `mcp__claude-in-chrome__*` | `mcp__remote-devices__Claude_Browser__*` |
| Open a page | `tabs_context_mcp` with `createIfEmpty`, then `navigate` with the tabId | `preview_start` with the URL; it returns the tabId |
| Run a script | `javascript_tool` returns at most 1,000 characters and refuses text that looks like a query string, so strip `=`, `&`, `?` and route long output through `emit()` plus `get_page_text` | `javascript_tool` returns the result whole (3,000+ characters verified, no query-string block); `emit()` plus `get_page_text` still works and is the safe choice for large tables |
| Read text | `get_page_text` | `get_page_text` (default cap 50,000 characters, raise with `max_chars`) |
| Look | `computer` screenshot; can time out while a viz loads | `computer` screenshot; the pane may be hidden, in which case prefer `get_page_text` |
| Site access | The extension's own site permissions | May answer that a site is not allowed yet; call `request_access` for that URL (scope `site` for jwt.nh.gov and my.doe.nh.gov, since every run uses them), then retry |
| Close | `tabs_close_mcp` | `tabs_close`; closing the last tab closes the pane |

For a Tableau tool: navigate to its wrapper URL from the Catalog, wait 6 seconds, then run the readiness check. Repeat the wait up to three times; if the workbook never appears, reload once, then report the outage rather than guessing.

```js
const viz = document.querySelector('tableau-viz'); const wb = viz && viz.workbook;
wb ? 'ready: ' + wb.activeSheet.name + ' | sheets: ' + wb.publishedSheetsInfo.map(s => s.name).join('; ') : 'not ready';
```

Install the output helper once per page load. It writes a result into the page as paragraphs so `get_page_text` can read it whole (javascript_tool returns at most 1,000 characters).

```js
window.emit = function (text) {
  let a = document.getElementById('claude-article');
  if (!a) { a = document.createElement('article'); a.id = 'claude-article'; document.body.prepend(a); }
  a.innerHTML = ''; const h = document.createElement('h1'); h.textContent = 'CLAUDE-OUT'; a.appendChild(h);
  for (const line of String(text).split('\n')) { const p = document.createElement('p'); p.textContent = line; a.appendChild(p); }
  return 'emitted ' + String(text).split('\n').length + ' lines';
};
'helper installed';
```

### Step D. Pull

Work in this order for every Tableau pull: resolve entity names against the filter's domain, set every filter you depend on with `'replace'`, read the data table, emit CSV, read it back with `get_page_text`. Set every filter explicitly, because the dashboards load with defaults (iExplore opens on Average Class Size, school grain, 2025; the iAchieve download tables open with two years and a handful of entities already applied), and an unset filter silently shapes the result.

Entity resolution (names carry suffixes and disambiguators, and the iExplore domain also holds malformed duplicates such as `Maple Avenue School(Claremont)(Claremont)(Claremont)`, so anchor the match and never guess):

```js
const wb = document.querySelector('tableau-viz').workbook;
const ws = wb.activeSheet.worksheets.find(w => w.name === 'Explore - Domain Bar View'); // use the tool's data worksheet
const f = (await ws.getFiltersAsync()).find(x => x.fieldName === 'Entity Name');          // or 'entity_name' in iAchieve
const dom = await f.getDomainAsync('database');
dom.values.map(v => v.formattedValue).filter(n => /claremont|stevens/i.test(n)).join(' ; ').replace(/[=&?]/g, ' ');
```

The tool drivers below give the exact worksheet, filter, and column names for each tool. Read the driver before the first call of a session; it is cheaper than probing.

### Step E. Check

- Row count equals entities × years × disaggregations you asked for; a shortfall means a name did not match or a year is not held. Find which, and report it with a Step N warning.
- Values marked `*N`, `*CS`, `N/A`, or with a non-null `suppressedIndicatorDesc` or `Exception Description` are suppressed or flagged by the DOE. Keep the marker; never turn it into zero or drop the row silently.
- A "state" row is not always a statewide total: in iExplore the state entity's value for a count indicator is a per-entity mean. When the user wants the statewide count, use the SSRS `State Totals` row or say which kind of figure you are giving.
- When the numbers will be quoted publicly, cross-check one value against the rendered dashboard: set the same selection in the visual (or take a screenshot after your filters are applied) and confirm the bar or tile shows the same figure.
- Year labels: iExplore `Year ID`, iAchieve `Year`, iReport `Select Year`, and the SSRS `School Year` all use the end year of the school year (2025 means 2024-25; verified by matching fall 2024 enrollment across tools). iGrant `Fiscal Year` is the federal fiscal year starting July 1. DOE-25 `Year` is the district fiscal year. State the label as the tool gives it and name the convention once.

### Step F. Deliver

Render one table per indicator (rows: entity, columns: years) or one long table (entity, indicator, year, value, flag) when there are several indicators. Under each table put a source line in this shape:

`Source: NH DOE iPlatform, iExplore, worksheet "Explore - Domain Bar View", filters Indicator Name Clean = Average Cost Per Pupil; Indicator Grain = District; Year ID = 2016-2025; Entity Name = Claremont, Newport. Extracted 2026-09-13 via https://jwt.nh.gov/?src_route=/iExplore/Explore-Dashboard`

Write CSV or xlsx when asked or when the table exceeds about 40 rows; put files in `/mnt/user-data/outputs/` and, when a folder is connected, commit them there too. Name files `iplatform_<tool>_<indicator>_<entities>_<years>.csv`. When the user asks what a metric means, quote iDefine or iGlossary rather than paraphrasing from memory.

Worked example. Request: "Claremont and Newport cost per pupil since 2016." Route: iExplore, Finance, Average Cost Per Pupil, district grain, Year ID 2016 to 2025, Entity Name Claremont and Newport. Deliver:

| District | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|
| Claremont | $16,520 | $16,852 | $16,476 | $16,755 | $17,084 | $20,542 | $19,789 | $21,590 | $23,288 | $26,013 |
| Newport | $13,813 | $13,888 | $15,101 | $15,948 | $18,283 | $19,871 | $20,393 | $22,729 | $27,628 | $29,290 |

Source: NH DOE iPlatform, iExplore, worksheet "Explore - Domain Bar View", filters Indicator Name Clean = Average Cost Per Pupil; Indicator Grain = District; Year ID = 2016-2025; Entity Name = Claremont, Newport. Year is the end year of the school year. Extracted 2026-09-13 via https://jwt.nh.gov/?src_route=/iExplore/Explore-Dashboard (those figures are the values read on that date; re-pull rather than reuse them).

### Step N. Not found in iPlatform

Some requests, or parts of them, cannot be answered from iPlatform data. Say so plainly with a warning; never fill the gap from memory, from another website, or by estimating. A request is unsatisfiable when, after the live check in Step B and the pull in Step D, any of these holds:

| Case | Example |
|---|---|
| No tool holds the topic | Individual teacher names, school board votes, bond repayment schedules, private school tuition |
| The entity is not in the tool's domain | A private school, a town that is not a district, a misspelled name with no anchored match |
| The years are not held | iExplore before 2016, iReport before 2018, DOE-25 before FY2013, any year not yet published |
| The grain is not held | Most finance indicators at school grain; ESSA ratings at district grain |
| Every value is suppressed or flagged | All cells `*N` or carrying an exception code |
| The data sits only behind a link that leaves iPlatform | The landing page's Bureau of Education Statistics links (Financial Reports, Staff Salary Reports, Adequate Education Aid and the others listed in the Catalog) |
| The tool is down | The workbook never loads after the retries in Step C |

Put the warning at the top of the answer when nothing could be answered, and directly under the tables when part of the request was answered. Use this form:

> **Warning: not found in iPlatform.** <What was asked, in the user's words>. Checked: <tools, worksheets or reports, and filter values tried>. Reason: <which case above, specifically, e.g. "Year ID holds 2016 to 2025; 2014 and 2015 are not held">.

Then, if you know it, name where the information may exist outside iPlatform (for example the NH Department of Revenue Administration MS forms, the district's warrant and budget, or the Bureau of Education Statistics page the landing page links to), label it as outside iPlatform and not searched, and offer to look there. Do not fetch it unasked, and do not put any number from it in an iPlatform table.

Keep the answered and unanswered parts apart. A table row or cell for something not found stays blank with a note pointing to the warning; it is never zero. Suppressed values keep their DOE marker in the table (Step E) and also get a warning when the suppression leaves the question unanswered. Record each warning in the scratch folder's `runs.log` line for the run.

### Step R. Discover or refresh the catalog

Run this when the Catalog says `status: empty`, when its refresh date is older than 120 days, when the user asks for a refresh, or when a live probe disagrees with it (a filter value rejected, a worksheet missing, a tool on the landing page that the Catalog lacks).

1. Open the landing page `https://www.education.nh.gov/who-we-are/division-of-educator-and-analytic-resources/iplatform` and read the "Data Reports" menu and the article body: every tool name, its link, and the DOE's one-paragraph description. The links do not surface in the accessibility tree; read them with `read_page` (filter all) or a DOM query.
2. For each `jwt.nh.gov` tool, open it, wait for the workbook, and run the probe below. It lists sheets, worksheets, filters with their domains, and parameters with allowable values. Page through the stored result 950 characters at a time (`window.__last.slice(n*950,(n+1)*950)`), or emit it and read it with `get_page_text`.
3. For iExplore, also record the indicator-by-category map: set `Indicator Grain` to District and all years, then for each `Category` value read the `relevant` domain of `Indicator Name Clean`. Repeat for School grain; the ESSA ratings exist only at school grain and most finance indicators only at district grain.
4. Open `https://my.doe.nh.gov/iPlatform` and list every report subcategory link with its `reportSubCategoryId`; open one report to confirm the year range in `select#SchoolYear`.
5. Open the DOE-25 page and read the fiscal-year filter labels.
6. Rewrite the Catalog section: same headings, new date, and a short "what changed" line. Keep the tool drivers unless a probe shows a renamed worksheet, filter, or parameter; then fix the driver and note it.
7. Call `propose_skills` with kind `improvement`, target `nh-iplatform`, and the complete SKILL.md (frontmatter, body, Settings with their current values untouched, drivers, new Catalog). Tell the user the catalog is refreshed once they save the proposal, and continue the original request with the live findings.

Probe (define once per page load, then `await window.__probe()` or `await window.__probe('Sheet Name')`):

```js
window.__probe = async function (sheetName) {
  const wb = document.querySelector('tableau-viz').workbook; if (!wb) return 'not ready';
  if (sheetName) await wb.activateSheetAsync(sheetName);
  const dash = wb.activeSheet, out = ['SHEETS: ' + wb.publishedSheetsInfo.map(s => s.name + '[' + s.sheetType[0] + ']').join(' ; '), 'ACTIVE: ' + dash.name];
  const wss = dash.sheetType === 'dashboard' ? dash.worksheets : [dash];
  out.push('WORKSHEETS: ' + wss.map(w => w.name).join(' ; '));
  const seen = new Map();
  for (const w of wss) {
    if (/^URL:|Button|Footer|Legend|Logo|Header/i.test(w.name)) continue;
    let fs = []; try { fs = await w.getFiltersAsync(); } catch (e) { continue; }
    for (const f of fs) {
      if (seen.has(f.fieldName)) continue;
      let s = f.fieldName + '{' + f.filterType[0];
      if (f.filterType === 'categorical') { s += ' ' + (f.appliedValues || []).map(v => v.formattedValue).slice(0, 3).join(',');
        try { const d = await f.getDomainAsync('database'); s += ' /' + d.values.length; if (d.values.length <= 12) s += ':' + d.values.map(v => v.formattedValue).join(','); } catch (e) {} }
      seen.set(f.fieldName, s + '}');
    }
  }
  out.push('FILTERS: ' + [...seen.values()].join(' ; '));
  const ps = await wb.getParametersAsync();
  out.push('PARAMS: ' + ps.filter(p => !/URL|Env/i.test(p.name)).map(p => { let s = p.name + '{' + (p.currentValue && p.currentValue.formattedValue); if (p.allowableValues && p.allowableValues.allowableValues) s += ' /' + p.allowableValues.allowableValues.length + ':' + p.allowableValues.allowableValues.slice(0, 10).map(v => v.formattedValue).join(','); return s + '}'; }).join(' ; '));
  window.__last = out.join('\n').replace(/[=&?]/g, ' ');
  return 'LEN ' + window.__last.length + '\n' + window.__last.slice(0, 900);
};
'probe installed';
```

## Browser mechanics

These are the things that cost time when unknown.

- The Tableau viz lives in a cross-origin iframe inside a `<tableau-viz>` element. `read_page` and `find` see nothing inside it. Drive it through `javascript_tool` (the Embedding API v3 object at `document.querySelector('tableau-viz').workbook`) and use screenshots only for visual confirmation.
- In Chrome, `javascript_tool` returns at most 1,000 characters, and it refuses to return a string that looks like a query string (it answers "[BLOCKED: Cookie/query string data]"). Strip `=`, `&`, and `?` from anything you return, and route anything long through `emit()` plus `get_page_text`. The built-in browser has neither limit, but the same habit costs nothing and keeps the scripts portable.
- Each `javascript_tool` call is a fresh evaluation in the same page, so helpers on `window` survive between calls and die on navigation.
- Filter and parameter changes persist for the page session. Reload the tool URL for a clean slate. Pass filter values as strings, years included, with update type `'replace'`. To clear a filter, apply `[]` with update type `'all'`.
- After `activateSheetAsync` or a parameter change, wait 2 to 3 seconds (`await new Promise(r => setTimeout(r, 3000))`) before reading, or the table reflects the old state.
- `getSummaryDataAsync({maxRows: N, ignoreSelection: true})` returns `columns` (with `fieldName`) and `data` (rows of cells with `formattedValue`). Build a name-to-index map from `columns` rather than trusting column order.
- Do not open `dashboards.nh.gov` directly; the wrapper page supplies the token. Do not change the wrapper's query string.
- Downloads (Tableau's download icon, the SSRS Export button, DOE-25 "Download Reports") save files to the browser's download folder, which this session can read only if that folder is connected. Ask before any download and state the file name and source. Prefer reading the data in place.
- The `computer` tool can time out while a viz is loading; use `javascript_tool` or `get_page_text` to test readiness instead of screenshots.

## Tool drivers

### iExplore (the workhorse)

URL: `https://jwt.nh.gov/?src_route=/iExplore/Explore-Dashboard&debug_session=false&toolbar=Hidden&Width=1300px&Height=1600px`
Sheets: `Explore - Dashboard` (data), `Compare Dashboard`, `Discover Dashboard`, `Indicator Search` (visual tools driven by parameters `Year ID Param`, `Entity ID of District Selected`, `Discover: Indicator A 1..5`; use them for pictures, not for data).
Data worksheet: `Explore - Domain Bar View` on `Explore - Dashboard`.
Filters: `Category` (8 values), `Indicator Name Clean` (45), `Indicator Grain` (`District`, `School`), `Year ID` (2016 to 2025), `Entity Name` (693; districts by plain name such as `Claremont`, schools by school name, sometimes with a town suffix such as `Maple Avenue School(Claremont)`), `schaprlvldesc` (`Elementary`, `Middle School`, `High School`, `District`, `State`), `schtypedesc` (10 school types), `Region` (`Lakes Region`, `North Country`, `South Central`, `Southeast`, `Southwest`, `State`).
Columns: `All: Entity Name + District` (e.g. `Claremont (District)`), `DownloadValue` (formatted, use this), `Entity ID`, `Indicator Name` (with unit, e.g. `Average Cost Per Pupil ($)`), `IndicatorQuartile`, `State`, `Year ID`, `ATTR(suppressedIndicatorDesc)`, `AVG(Display Value)`, `AVG(Graphical Value)`, `MIN(0)`. Each entity also returns one label row with `Year ID` `Null` (it carries the quartile and the state name, no value); drop those.

```js
const wb = document.querySelector('tableau-viz').workbook;
if (wb.activeSheet.name !== 'Explore - Dashboard') await wb.activateSheetAsync('Explore - Dashboard');
const ws = wb.activeSheet.worksheets.find(w => w.name === 'Explore - Domain Bar View');
await ws.applyFilterAsync('Indicator Name Clean', ['Average Cost Per Pupil'], 'replace');
await ws.applyFilterAsync('Indicator Grain', ['District'], 'replace');
await ws.applyFilterAsync('Year ID', ['2021', '2022', '2023', '2024', '2025'], 'replace');
await ws.applyFilterAsync('Entity Name', ['Claremont', 'Newport'], 'replace');   // omit this line for every entity in the state
const d = await ws.getSummaryDataAsync({ maxRows: 20000, ignoreSelection: true });
const ix = Object.fromEntries(d.columns.map((c, i) => [c.fieldName, i]));
const rows = d.data.map(r => r.map(c => c.formattedValue)).filter(r => r[ix['Year ID']] !== 'Null');
const csv = ['entity,indicator,year,value,flag'].concat(rows.map(r => [r[ix['All: Entity Name + District']], r[ix['Indicator Name']], r[ix['Year ID']], '"' + r[ix['DownloadValue']] + '"', r[ix['ATTR(suppressedIndicatorDesc)']]].join(','))).join('\n');
emit(csv);
```

Then call `get_page_text`. Several indicators: loop over indicator names inside one call and concatenate the CSVs. Statewide rankings: leave `Entity Name` unfiltered and sort in code.

State value (verified 2026-09-13). The state entity is `State of New Hampshire`. It never appears in the bar view; read it from the dashboard's own flat worksheet `*Download Explore`, whose filter `Filter: Remove NH with ID` is `False` only for the state entity (setting it to `False` on the bar view returns nothing). That worksheet keeps its own filter state, separate from the bar view: `Filter: Remove NH with ID`, `Year ID Filter` (`True` limits the years to the recent window; apply `['False', 'True']` for every year), `Category`, `Indicator Name Clean`, `Region`, `School / District`, `School / District Level`, `School / District Type`. Columns: `Indicator Category`, `Indicator Name`, `School / District`, `School / District Level`, `School / District Type`, `Region`, `Entity ID`, `Entity Name`, `Year ID`, `Category`, `DownloadValue`.

```js
const wb = document.querySelector('tableau-viz').workbook;
const dl = wb.activeSheet.worksheets.find(w => w.name === '*Download Explore');
await dl.applyFilterAsync('Filter: Remove NH with ID', ['False'], 'replace');
await dl.applyFilterAsync('Year ID Filter', ['False', 'True'], 'replace');
await dl.applyFilterAsync('Indicator Name Clean', ['Average Cost Per Pupil'], 'replace');
const d = await dl.getSummaryDataAsync({ maxRows: 5000, ignoreSelection: true });
const ix = Object.fromEntries(d.columns.map((c, i) => [c.fieldName, i]));
emit(['entity,indicator,year,value'].concat(d.data.map(r => r.map(c => c.formattedValue)).map(r => [r[ix['Entity Name']], r[ix['Indicator Name']], r[ix['Year ID']], '"' + r[ix['DownloadValue']] + '"'].join(','))).join('\n'));
```

Read the state row for what it is. For rate and per-pupil indicators it is the statewide figure (the 2024 state Average Cost Per Pupil read $21,545). For count indicators such as Total Enrollment it is a per-entity mean (767 for 2025, against a statewide count of 162,660), so take statewide counts from the SSRS District Fall Enrollment report's `State Totals` row instead. The state's 2025 cost per pupil carried the marker `*CS`, an exception code the dashboard's definition worksheets do not decode; pass it through as written.

### iAchieve (assessment detail)

URL: `https://jwt.nh.gov/?src_route=iAchieve/AssessmentParticipation&debug_session=false&toolbar=Hidden&Width=1300px&Height=1600px`
Sheets: `Assessment Participation`, `Proficiency and Growth`, `Achievement Levels`, `ESSA Indicators`. Each has a flat data worksheet whose name starts with `*Download`. Filter that worksheet directly; the visual parameters (`Stored entity`, `Stored entity type`, `Select category`, `Select Year`, `toggle proficiency vs score`) do not drive it.
Filters on the Participation and Proficiency download worksheets: `entity_name` (666; districts by plain name), `Year` (2016 to 2025), `Subject` (`ELA`, `Math`, `Science`), `Grade` (`All Grades`, `Grade 3` through `Grade 8`, `Grade 11`; for a high school `All Grades` and `Grade 11` return the same values), `sub_group` (18 values, all selected by default), `Metric ID (for download)` with 9 values: `Academic Growth`, `Assessment Percentage Proficient`, `Average Scaled Score`, `Breakdown of Students Not Tested`, `FAY Count`, `FAY Rate`, `Participation Rate`, `Percentage of Students Not Tested`, `Total Student Enrollment`.
Achievement Levels download filters: `Metric ID (for download) (2 levels and movement)` (`Academic Growth`, `Achievement Results in Current Year`, `Achievement Results in Prior Year`) plus `metric_id (vIAchievement_Levels)`. ESSA Indicators download metrics: Achievement, Growth, College and Career Readiness, English Language Proficiency, Equity, and Graduation Rate indicator Level and Value, and `ESSA Determination (Short)`. Read a download worksheet's filters with `getFiltersAsync()` before applying, since names differ by sheet.
Columns: `ID`, `Name`, `Entity_type`, `Associated District ID`, `Associated District Name`, `Year`, `Subject`, `Category`, `Subcategory` (the subgroup: `All Students`, `Female`, `Male`, race and ethnicity groups, `Economically Disadvantaged`, and others), `Grade`, `Metric ID (for download)`, `DownloadValue (vIAchievement_NoLevels)`. Suppressed cells read `*N`.

```js
const wb = document.querySelector('tableau-viz').workbook;
await wb.activateSheetAsync('Proficiency and Growth'); await new Promise(r => setTimeout(r, 2500));
const dl = wb.activeSheet.worksheets.find(w => w.name.startsWith('*Download'));
await dl.applyFilterAsync('entity_name', ['Claremont'], 'replace');
await dl.applyFilterAsync('Year', ['2022', '2023', '2024', '2025'], 'replace');
await dl.applyFilterAsync('Subject', ['ELA', 'Math'], 'replace');
await dl.applyFilterAsync('Grade', ['All Grades'], 'replace');
await dl.applyFilterAsync('Metric ID (for download)', ['Assessment Percentage Proficient'], 'replace');
// sub_group: leave alone for every subgroup, or apply ['All Students'] for the headline figure
const d = await dl.getSummaryDataAsync({ maxRows: 50000, ignoreSelection: true });
const cols = d.columns.map(c => c.fieldName);
emit([cols.join(',')].concat(d.data.map(r => r.map(c => '"' + String(c.formattedValue).replace(/"/g, '""') + '"').join(','))).join('\n'));
```

### iReport (report card snapshot)

URL: `https://jwt.nh.gov/?src_route=iReport/FrontPage&debug_session=false&toolbar=Hidden&Width=1300px&Height=1600px`
Sheets: `Front Page`, `IDEA Report`, `ESSA Profiles (School)`, `ESSA Profiles (District)`.
Selection is by parameter, not filter: `School or District` (`School`, `District`), `Search for School or District Name (Master)` (districts as `Claremont (District)`, schools by name such as `Stevens High School`), `Select Year` (2018 to 2025). Then activate the matching profile sheet and wait 3 seconds. Confirm the selection by reading worksheet `Current Selection Text (Big)`.
Data worksheets return long-format rows: `Disagg Category`, `Disagg 1Desc`, `Value (Float)`, `Metric Id`, `ShortDesc (Exception Code)`, `ATTR(Exception Description)`. Useful ones: `SE - In School`, `SE - Out of School`, `SE - Expusions` (spelled that way in the workbook), `ESSA - Indicators (District)` or `ESSA - Indicators` (school: growth, graduation, equity, EL proficiency, CCR, achievement ratings), `ESSA - Determination`, `ESSA - SIF (School)`, `***ESSA - School Designations`, `School List by District`. The `Metric Id` domain holds 123 ids (list in the Catalog) and `Disagg Category` 25 values. Several worksheets sit behind the profile's menu dots and return empty until their section is shown; if a worksheet returns zero rows, screenshot the profile and click the relevant section, or take the metric from iExplore or iAchieve instead.

```js
const wb = document.querySelector('tableau-viz').workbook; const ps = await wb.getParametersAsync();
await ps.find(p => p.name === 'School or District').changeValueAsync('District');
await ps.find(p => p.name === 'Search for School or District Name (Master)').changeValueAsync('Claremont (District)');
await ps.find(p => p.name === 'Select Year').changeValueAsync(2024);
await wb.activateSheetAsync('ESSA Profiles (District)'); await new Promise(r => setTimeout(r, 3000));
const ws = wb.activeSheet.worksheets.find(w => w.name === 'SE - Out of School');
const d = await ws.getSummaryDataAsync({ maxRows: 5000, ignoreSelection: true });
emit([d.columns.map(c => c.fieldName).join(',')].concat(d.data.map(r => r.map(c => '"' + String(c.formattedValue).replace(/"/g, '""') + '"').join(','))).join('\n'));
```

For a multi-year series from iReport, loop `Select Year` and re-read; prefer iExplore or iAchieve when they hold the same metric.

### iGrant (federal grants)

URL: `https://jwt.nh.gov/?src_route=iGrant-FinancialTransparencyfromNHSchoolsDistricts/iGrantsHome&toolbar=hidden&Width=1300px&Height=1600px`
Sheets: `iGrants Home`, `ESSER Total Funds Dashboard` (data), plus two standalone worksheets.
Data worksheets on `ESSER Total Funds Dashboard`: `NH Map (v2)` (columns `District Name`, `Geographic Region`, `CNT(Schools)`, `SUM(Funding Amount)`), `Geographic Region Bars` (`Geographic Region` holds the entity name, districts and nonpublic schools alike, then `Grant Type`, `Funding Type`, `SUM(Funding Amount)`), `Funding by Param Type`.
Filters: `DataSourceName Selected` (54 programs, names such as `ESSER`, `FY25 Title I Part A`, `FY24 IDEA/Preschool`), `Fiscal Year` (values `2027`, `2026`, `2025`, `2024`, `2023`, and the single combined label `2020, 2021, 2022` used for ESSER). The program and the fiscal year must agree (an FY25 program with `Fiscal Year` 2026 returns nothing).
Parameters: `Funding Type Parameter` (`Allocated`, `Budgeted`, `Approved`, `Reimbursed`), `Measure Type` (`Total Funds`, `per Student`), `Show Charter Schools`, `Extraction Date Param` (the data refresh date; report it).

```js
const wb = document.querySelector('tableau-viz').workbook;
await wb.activateSheetAsync('ESSER Total Funds Dashboard'); await new Promise(r => setTimeout(r, 2500));
const ws = wb.activeSheet.worksheets.find(w => w.name === 'NH Map (v2)');
await ws.applyFilterAsync('DataSourceName Selected', ['FY25 Title I Part A'], 'replace');
await ws.applyFilterAsync('Fiscal Year', ['2025'], 'replace');
const ps = await wb.getParametersAsync();
await ps.find(p => p.name === 'Funding Type Parameter').changeValueAsync('Reimbursed');
await ps.find(p => p.name === 'Measure Type').changeValueAsync('Total Funds');
await new Promise(r => setTimeout(r, 2000));
const d = await ws.getSummaryDataAsync({ maxRows: 5000, ignoreSelection: true });
const ix = Object.fromEntries(d.columns.map((c, i) => [c.fieldName, i]));
const rows = d.data.map(r => r.map(c => c.formattedValue));
emit(['district,region,schools,funding'].concat(rows.map(r => [r[ix['District Name']], r[ix['Geographic Region']], r[ix['CNT(Schools)']], '"' + r[ix['SUM(Funding Amount)']] + '"'].join(','))).join('\n'));
```

Verified 2026-09-13: FY25 Title I Part A, Reimbursed, Total Funds returned 207 district rows (Claremont $945,683 across 6 schools).

For a program-by-program breakdown of one district, read `Geographic Region Bars` and keep rows whose `Geographic Region` equals the district name.

### Public Reports (SSRS tables)

Landing: `https://my.doe.nh.gov/iPlatform`. Subcategory pages: `https://my.doe.nh.gov/iPlatform/Report/DataReportsSubCategory?reportSubCategoryId=<id>` (ids in the Catalog). Each lists reports whose links open the viewer `https://my.doe.nh.gov/iPlatform/Report/Report?path=...&name=...&categoryName=...&categoryId=<id>`.
Viewer controls: `select#SchoolYear` (a select2 dropdown; 2012 to 2026 on District Fall Enrollment), a `Run Report` button, paging (`#ReportViewerCurrentPage`, First, Previous, Next, Last), a search box `#ReportViewerSearchText` with a `Find` link, and `Export` (Excel, PDF). The report renders as HTML tables of about 30 rows per page; the largest table holds the data and starts with a header row. The select2 label may keep showing the old year after a change, so confirm the run by reading the `Report Date` text and one known row.

```js
// choose the year and run
const sel = document.getElementById('SchoolYear'); sel.value = '2025';
sel.dispatchEvent(new Event('change', { bubbles: true })); if (window.jQuery) { try { window.jQuery(sel).trigger('change'); } catch (e) {} }
[...document.querySelectorAll('button')].find(b => b.textContent.trim() === 'Run Report').click(); 'run';
```

```js
// after ~6 s: jump to the entity's page, then read the table
const box = document.getElementById('ReportViewerSearchText'); box.value = 'Claremont'; box.dispatchEvent(new Event('input', { bubbles: true }));
[...document.querySelectorAll('a')].find(a => a.textContent.trim() === 'Find').click();
await new Promise(r => setTimeout(r, 4000));
const big = [...document.querySelectorAll('table')].map(tb => ({ tb, n: tb.querySelectorAll('tr').length })).sort((a, b) => b.n - a.n)[0].tb;
const rows = [...big.querySelectorAll('tr')].map(tr => [...tr.children].map(td => td.innerText.trim().replace(/\s+/g, ' ')).filter(x => x)).filter(r => r.length > 1);
const meta = (document.body.innerText.match(/Report Date:\s*\S+/) || [''])[0];
emit(meta + '\n' + rows.map(r => r.map(c => '"' + c.replace(/"/g, '""') + '"').join(',')).join('\n'));
```

Read every page (Next Page, repeat) only when the whole state is wanted. Multi-year series: loop the year select and re-run; each run is one page load, so batch the entities per year.

### DOE-25 filings

`https://my.doe.nh.gov/iPlatform/DOE25/DOE25Reports`. Filters: `Fiscal Year` (checkbox list, 2013 to 2025, latest checked by default) and `Organization`. The table lists `Organization`, `Year`, `Filename` (district files are `d<id><id>.xlsx`, e.g. Claremont `d101101.xlsx`; the state rows are `state-consolidated-doe-25-<year>.xlsx` and `doe-25-extract-state-profile-data-<year>.xlsx`), `Date Updated`, and a checkbox. Checking rows enables `Download Reports (n)`, which confirms in a modal and then downloads `/iPlatform/DOE25/DownloadRecords?id=...`. Report the filename and Date Updated from the table without downloading; download only with the user's permission, and read the file with the xlsx skill afterward.

### iDefine and iGlossary

iDefine (data dictionary): `https://my.doe.nh.gov/DataDictionary/Default.aspx`, organized as school-submission data elements (i4see) and program-area data elements. iGlossary: `https://jwt.nh.gov/?src_route=iGlossary/Glossary&debug_session=false&toolbar=Hidden&Width=1300px&Height=1600px`, alphabetical definitions in a Tableau sheet (read its worksheets with the probe). Use either when the user asks what an indicator measures or when a unit is ambiguous.

## Hard rules

- Every number in the answer comes from a read made in this session. A year the tool does not hold stays blank in the table; it is never estimated or filled from memory.
- Every part of a request that iPlatform cannot answer gets a Step N warning naming what was checked and why it failed. A silent gap is an error.
- Intermediate results go only to the scratch folder the request or the `scratch` setting names, or to the session scratchpad. Nothing in the scratch folder is ever deleted by the skill.
- Every table carries its source line: tool, worksheet or report, filters, year label, extraction date, URL.
- Suppression and exception markers survive into the output as written by the DOE.
- Year labels stay as the tool gives them, with the convention named once.
- No downloads without asking. No direct calls to `dashboards.nh.gov`.
- The browser is the one the request or the `browser` setting names. Never switch browsers silently; say so and offer the other.
- Pull what was asked. Whole-state pulls are for rankings and comparisons the user requested.
- When the live site and the Catalog disagree, the live site wins; fix the Catalog through Step R.
- No em dashes anywhere you write.

## Catalog

`status: populated` · `refreshed: 2026-09-13` · `source: landing page and live probes of every tool` · `changes: initial build; same day, first live run verified the iExplore state entity and the *Download Explore worksheet, and recorded the *CS marker; 2026-09-14, browser setting added after verifying both browsers, iAchieve grade label confirmed as Grade 11; 2026-09-28, scratch folder setting and Step N not-found warnings added (procedure only, catalog contents unchanged)`

### Tools

| Tool | Where | Holds | Years |
|---|---|---|---|
| iExplore | jwt.nh.gov, route `/iExplore/Explore-Dashboard` | 45 indicators for 693 entities (state, districts, schools), explore, compare, discover views | 2016 to 2025 |
| iAchieve | jwt.nh.gov, route `iAchieve/AssessmentParticipation` | State assessment participation, proficiency, growth, scaled scores, achievement levels, ESSA indicators; by subject, grade, subgroup | 2016 to 2025 |
| iReport | jwt.nh.gov, route `iReport/FrontPage` | ESSA report cards per school and district, IDEA report, 123 metric ids, printable report card links | 2018 to 2025 |
| iGrant | jwt.nh.gov, route `iGrant-FinancialTransparencyfromNHSchoolsDistricts/iGrantsHome` | Federal grant allocations, budgets, approvals, reimbursements by district and program, weekly refresh | FY2020 to FY2027 |
| iGlossary | jwt.nh.gov, route `iGlossary/Glossary` | Definitions of education terms used across iPlatform | n/a |
| iDefine | my.doe.nh.gov/DataDictionary/Default.aspx | Data dictionary of collected data elements | n/a |
| Public Reports | my.doe.nh.gov/iPlatform | SSRS tables: enrollment, demographics, attendance, dropouts, class size, staff, codes; links to Bureau of Education Statistics pages for finance, salaries, adequacy aid, assessments, YRBS, safety | 2012 to 2026 (varies by report) |
| DOE-25 filings | my.doe.nh.gov/iPlatform/DOE25/DOE25Reports | Each district's annual DOE-25 financial report as an xlsx, plus state consolidated files | FY2013 to FY2025 |
| iFinance | education.nh.gov, Bureau of School Finance, financial-reporting-requirements | The DOE's page describing DOE-25 search and reporting requirements | n/a |
| iNHDEX | education.nh.gov, Bureau of Education Statistics, data-collection/inhdex | Data collection index | n/a |
| Archived profiles | my.doe.nh.gov/profiles/ | NH Profiles and Report Cards, 2017 and prior | to 2017 |
| Training | education.nh.gov, iplatform/iplatform-training-resources | Videos and PDFs on iExplore (Explore, Compare, Search, Discover, Download functionality), iReport, iAchieve, iPlatform for the public, LEAs, legislators | n/a |

The DOE's own descriptions, kept because they define scope: iAchieve "includes Assessment Participation, Proficiency and Growth, Achievement Levels, and ESSA Indicators"; iGrant covers COVID relief funds and "numerous other annual federal programs", organized "by the federal fiscal year starting July 1"; iReport "includes static information about individual schools and school districts that comprises the accountability data elements" under ESSA; iExplore "is driven by 15 identified data elements" (the workbook now exposes 45); Data Reports cover "student counts, racial statistics, teacher counts, school building information, financial data on the school districts in the form of budgets and financial statements"; iFinance "provides a search engine to explore all DOE-25 financial documents".

### iExplore indicators by category (filter `Indicator Name Clean`)

| Category | Indicators | Grain |
|---|---|---|
| Academic Growth | Student Growth - ELA; Student Growth - Math | both |
| Achievement | Participation - ELA; Participation - Math; Participation - Science; Proficiency - ELA; Proficiency - Math; Proficiency - Math & ELA | both |
| College and Career Readiness | Dropout Rate; Graduation Rate - 4YR; Graduation Rate - 5YR; Post-secondary Enrollment Rate | both |
| Educator | Average Teacher Salary; Educators certified in the subject; Experienced Educators | both |
| ESSA | Achievement Rating; College and Career Readiness Rating; English Language Proficiency Rating; Equity Rating; Graduation Rate Rating; Growth Rating; School Improvement Funds | school only |
| Finance | Adequacy Aid Revenue; Administration Expenses; Average Cost Per Pupil; Equalized Tax Rates; Equalized Valuation Per Pupil; Federal Aid Revenue; Instructional Staff Expenses; Operational/Plant Maintenance Expenses; Other State Aid Revenue; Total Expenditures; Total Revenues | district (school grain has only Average Cost Per Pupil and Total Expenditures) |
| Profile | Economically Disadvantaged Students; English Language Learner; Students with Disability; Total Enrollment | both |
| School Environment | Average Class Size; Expulsion Rate; In School Suspension Rate; Incidents of Violence; Out Of School Suspension Rate; Students/Counselors Ratio; Students/Non-Teacher Staff Ratio; Teachers/Total Staff Ratio | both |

Synonym hints: "per-pupil cost", "cost per student", "spending per pupil" → Average Cost Per Pupil. "Budget", "total spending" → Total Expenditures. "State aid", "adequacy" → Adequacy Aid Revenue, Other State Aid Revenue. "Tax rate" → Equalized Tax Rates. "Property wealth", "valuation" → Equalized Valuation Per Pupil. "Enrollment", "how many students" → Total Enrollment (iExplore) or District Fall Enrollment by grade span (Public Reports). "Free and reduced lunch", "poverty" → Economically Disadvantaged Students (iExplore) or the Free and Reduced School Lunch Eligibility report. "Test scores" → Proficiency (iExplore headline) or iAchieve for subgroups, grades, scaled scores. "Teacher pay" → Average Teacher Salary. "Discipline" → suspension and expulsion rates (iExplore) or iReport SE worksheets for the by-day and by-category breakdowns.

### iAchieve

Metrics (`Metric ID (for download)`): Academic Growth; Assessment Percentage Proficient; Average Scaled Score; Breakdown of Students Not Tested; FAY Count; FAY Rate; Participation Rate; Percentage of Students Not Tested; Total Student Enrollment. Achievement Levels sheet: Academic Growth; Achievement Results in Current Year; Achievement Results in Prior Year. ESSA Indicators sheet: Achievement, Growth, College and Career Readiness, English Language Proficiency, Equity, Graduation Rate (each as Indicator Level and Indicator Value); ESSA Determination (Short).
Subjects: ELA, Math, Science. Grades: All Grades, Grade 3 through Grade 8, Grade 11. Values seen in proficiency cells besides percentages: `*N`, `N/A`, and `<10%`. Subgroup categories (`Select category`): All Students, Sex, Race/Ethnicity, Subgroup; 18 `sub_group` values including All Students, Female, Male, American Indian or Alaskan, Asian or Pacific Islander, Black or African American, Hispanic or Latino, Multiple Races, White, Economically Disadvantaged, and the remaining ESSA subgroups (read the domain for the exact list).

### iReport

Years 2018 to 2025. Disaggregation categories (25): Achievement Level; Additional Revenues; By Day; Cost Per Pupil Type; ESSA Designation; Expenditure Type; Grade; Institution Location; Institution Type; NAEP Achievement Level By Grade; NAEP Participation By Student Group; Non-recurring Expenditures; Poverty Level; Race/Ethnicity; Recurring Expenditures; Revenue Type; School Type; Sex; Student Group; Total Revenues.
Metric ids (123), grouped: assessment (access_proficiency_nbr, access_proficiency_pct, ela_growth, ela_proficiency, ela_proficiency_number, ela_proficiency_participation, ela_proficiency_alt_participation, ela_proficiency_alt_participation_nbr, math_growth, math_proficiency, math_proficiency_number, math_proficiency_participation, math_proficiency_alt_participation, math_proficiency_alt_participation_nbr, science_proficiency, science_proficiency_number, science_proficiency_participation, science_proficiency_alt_participation, science_proficiency_alt_participation_nbr, el_proficiency, lep_first_year_ela, lep_first_year_ela_nbr); NAEP (ELA_naep_participation_NH, ELA_naep_participation_US, ELA_naep_proficiency_NH, ELA_naep_proficiency_US, Math_naep_participation_NH, Math_naep_participation_US, Math_naep_proficiency_NH, Math_naep_proficiency_US); ESSA ratings and status (achievement_rating, growth_rating, equity_rating, el_proficiency_rating, ccr_rating, grad_rating, essa_list, essa_status, school_improvement_funds); outcomes (grad_rate_4yr, grad_rate_5yr, drop_out, postsecondary_enrollment); environment (in_school_suspension_rate, out_of_school_suspension_rate, expulsion_rate, incidents_violence, class_size); educators (average_teacher_salary, experienced_teachers, experienced_teachers_count, experienced_teachers_nbr, out_of_field, out_of_field_count, out_of_field_nbr, teacher_emergency_credential, teacher_emergency_credential_count, teacher_emergency_credential_nbr); enrollment and finance (total_enrollment, pct_enrollment_race, pct_enrollment_subgroup, percent_enrollment_gender, n_schools, cost_per_pupil, total_expenditures, total_revenue); IDEA state performance plan indicators (ind_1_grad_rate_4yr, ind_2_dropout_rate, ind_3_math_participation, ind_3_math_proficiency, ind_3_reading_participation, ind_3_reading_proficiency, ind_3a and ind_3b math and reading at grades 4, 8, 11, ind_5 and ind_6 placement measures (majority regular, separate facilities, home), ind_7a to ind_7c preschool outcomes, ind_8_parent, ind_9 and ind_10 disproportionality (with _pct variants), ind_11_timely_evaluation, ind_12_early_intervention, ind_13_secondary_planning, ind_14 postsecondary enrollment and employment variants). This list is abridged: the ids between `ind_3b_reading_11` and `ind_5c_separate_facilities` (the ind_4 and early ind_5 group) were not captured. Read the live domain for the exact spelling before filtering on `Metric Id`.

### iGrant programs (`DataSourceName Selected`, 54 values)

ESSER, plus for each of FY23, FY24, FY25, FY26 (and FY27 where posted): Title I Part A; Title I Part D2; Title II Part A; Title III; Title III Immigrant Children & Youth; Title IV A; Title IVB - 21st Century Community Learning Center; Title V Part B Subpart 2 - RLIS; IDEA/Preschool; McKinney-Vento Homeless Education; Perkins V Program Improvement; CSI Grant (FY24 onward); Charter School Program (FY23). Names follow the pattern `FY25 Title I Part A`. Extraction date at last probe: September 9, 2026.

### Public Reports subcategories (`reportSubCategoryId`)

| Id | Subcategory | Reports seen |
|---|---|---|
| 9 | Enrollment Reports | ADM In Attendance and Residence; District Fall Enrollment (SAU #, SAU Name, District #, District Name, PreSchool, Kindergarten, Elementary, Middle, High, PG, Total; a `State Totals` row on page 1; years 2012 to 2026; its district totals match iExplore Total Enrollment year for year); School Administrative Unit Enrollments |
| 10 | Enrollments by Grade | |
| 12 | State Totals | |
| 18 | Free and Reduced School Lunch Eligibility | |
| 19 | Enrollments - Demographic Categories | |
| 21 | Attendance | |
| 23 | Dropouts and Completers | |
| 26 | Average Class Size | |
| 27 | Staff Reports | |

Also listed on the landing page with their own ids not yet recorded: Home Education and NonPublic Enrollments; Codes Lists. Links that leave my.doe.nh.gov for Bureau of Education Statistics pages: District and School Calendars; Schools and SAU Information; Financial Reports; Staff Salary Reports; Adequate Education Aid; Other State Aid Programs; Assessments (assessment-data); Non-Statewide Assessment (SAT) College Board Reports; NH Youth Risk Behavior Survey; School Safety Data. Federal Aid links to the U.S. Department of Education state tables.

### Entities

693 entities in iExplore (state, districts, schools); 666 in iAchieve; 699 in iReport. District example: `Claremont` (iExplore, iAchieve), `Claremont (District)` (iReport search parameter, and the iExplore output column). School examples under Claremont: `Claremont Middle School`, `Maple Avenue School(Claremont)`, `Stevens High School`. State: `State of New Hampshire` in the iExplore `Entity Name` domain (reachable only through the `*Download Explore` worksheet, see the iExplore driver) and as the iAchieve `Stored entity` default; the iExplore `State` column shows `New Hampshire`. iExplore Entity ID for Claremont district: 101 (the DOE-25 filename uses the same id, `d101101.xlsx`).