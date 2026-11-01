# SPDX-License-Identifier: Apache-2.0
"""Index the CSBMN knowledge graph into SQLite full-text search, and query it.

Sources read from a checkout of https://github.com/kevin-tyson/CSBMN:

  Input/SupportingDocuments/MAP.md   meetings, recordings, Drive packets, minutes
  Output/HTML/*.HTML                 meeting pages: summary, agenda, topics, flags
  Output/HTML/Dialogue/*.CSV         speaker-attributed transcript rows
  Output/HTML/**/*.HTML (others)     cross-meeting reports
  rtk_portal/data/policy_index.md    snapshot of the Board's policy index

Build:  python -m rtk_portal.kg build --repo /path/to/CSBMN [--out data/kg.db]
Search: python -m rtk_portal.kg search "budget deficit" --from 2025-01-01
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sqlite3
import sys
import tempfile
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))

PKG_DATA = Path(__file__).parent / "data"
POLICY_INDEX_URL = "https://docs.google.com/document/d/1JmygIGNaVc8ZfaQWtoIA25tRaBGw2Oh5k5ARsGlreqg/edit"

MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july", "august",
     "september", "october", "november", "december"], start=1)}
MONTHS.update({k[:3]: v for k, v in list(MONTHS.items())})
MONTHS["sept"] = 9

STOPWORDS = set("""
a about above after again against all also am an and any are as at be because been before being
below between both but by can could did do does doing down during each few for from further had
has have having he her here hers him his how i if in into is it its itself just me more most my
no nor not now of off on once only or other our out over own please same she should so some such
than that the their them then there these they this those through to too under until up very
was we were what when where which while who whom why will with would you your yours
request requests requesting requested pursuant rsa right know law copy copies provide provided
record records document documents information like want need get give send see all any every
regarding related relating concerning respect thank thanks sincerely dear hello hi re
""".split())


# ---------------------------------------------------------------- small HTML DOM

class Node:
    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag, attrs=None, parent=None):
        self.tag, self.attrs, self.children, self.parent = tag, dict(attrs or {}), [], parent

    def iter(self):
        for c in self.children:
            if isinstance(c, Node):
                yield c
                yield from c.iter()

    def find_all(self, tag=None, cls=None, id_=None):
        for n in self.iter():
            if tag and n.tag != tag:
                continue
            if cls and cls not in (n.attrs.get("class") or "").split():
                continue
            if id_ and n.attrs.get("id") != id_:
                continue
            yield n

    def find(self, *a, **k):
        return next(self.find_all(*a, **k), None)

    def text(self) -> str:
        parts = []

        def walk(n):
            for c in n.children:
                if isinstance(c, str):
                    parts.append(c)
                elif c.tag not in ("script", "style"):
                    walk(c)
        walk(self)
        return re.sub(r"\s+", " ", "".join(parts)).strip()


VOID = {"br", "img", "hr", "meta", "link", "input", "source", "col", "wbr", "area", "base"}


class _Builder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root")
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur)
        self.cur.children.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_endtag(self, tag):
        n = self.cur
        while n is not None and n.tag != tag:
            n = n.parent
        if n is not None and n.parent is not None:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.children.append(data)


def parse_html(text: str) -> Node:
    b = _Builder()
    b.feed(text)
    b.close()
    return b.root


def section_nodes(h2: Node):
    """Element siblings after an h2, up to the next h2."""
    parent = h2.parent
    sibs = [c for c in parent.children if isinstance(c, Node)]
    i = sibs.index(h2)
    for n in sibs[i + 1:]:
        if n.tag == "h2":
            break
        yield n


# ---------------------------------------------------------------- parsing helpers

def parse_long_date(s: str) -> str | None:
    m = re.search(r"([A-Za-z]+)\.?\s+(\d{1,2}),\s*(\d{4})", s or "")
    if not m or m.group(1).lower() not in MONTHS:
        return None
    try:
        return date(int(m.group(3)), MONTHS[m.group(1).lower()], int(m.group(2))).isoformat()
    except ValueError:
        return None


def parse_short_date(s: str) -> str | None:
    m = re.search(r"\b(\d{1,2})/(\d{1,2})/(\d{2,4})\b", s or "")
    if not m:
        return None
    y = int(m.group(3))
    y = y + 2000 if y < 100 else y
    try:
        return date(y, int(m.group(1)), int(m.group(2))).isoformat()
    except ValueError:
        return None


def hms(sec: float) -> str:
    sec = int(sec)
    return f"{sec // 3600}:{sec % 3600 // 60:02d}:{sec % 60:02d}"


LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
DOC_TRIPLE = re.compile(r"`([^`\n]+)`\s*\n\s*\n?\s*([A-Za-z][A-Za-z ./-]{0,30})\s*\n\s*\n?\s*\[open\]\((https?://[^)\s]+)\)")


def doc_kind(name: str) -> str:
    n = name.lower()
    if "minute" in n:
        return "minutes"
    if "agenda" in n:
        return "agenda"
    return "document"


def parse_map(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"(?m)^## ", text)
    meetings = []
    for part in parts[1:]:
        head, _, body = part.partition("\n")
        m = re.match(r"(\d+[a-z]?)\.\s+(.*?)\s+[—–-]\s+(.*)$", head.strip())
        if not m:
            continue
        section, org, when = m.group(1), m.group(2).strip(), m.group(3).strip()
        iso_date = parse_long_date(when)
        mt = {
            "section": section, "body": org, "date": iso_date, "date_text": when,
            "title": f"{org}, {when}",
            "dialogue_file": None, "show_id": None, "video_url": None, "video_title": None,
            "folder_url": None, "folder_name": None, "documents": [], "minutes": [],
            "no_drive": "No Drive material" in body or "No packet or minutes" in body,
            "raw": body,
        }
        d = re.search(r"dialogue: `Output/HTML/Dialogue/([^`]+?)\.CSV`", body, re.I)
        if d:
            mt["dialogue_file"] = d.group(1) + ".CSV"
        v = re.search(r"Remote video: \[([^\]]*)\]\((https://reflect-claremont\.cablecast\.tv/internetchannel/show/(\d+)[^)\s]*)\)", body)
        if v:
            mt["video_title"], mt["video_url"], mt["show_id"] = v.group(1), v.group(2), v.group(3)
        f = re.search(r"Drive folder: \[([^\]]+)\]\((https?://[^)\s]+)\)", body)
        if f:
            mt["folder_name"], mt["folder_url"] = f.group(1), f.group(2)
        for line in body.splitlines():
            for mm in re.finditer(r"Minutes(?: on hand[^:]*)?:\s", line):
                for name, url in LINK.findall(line[mm.end():]):
                    mt["minutes"].append({"name": name, "url": url})
        seen = set()
        for name, fmt, url in DOC_TRIPLE.findall(body):
            if url in seen:
                continue
            seen.add(url)
            mt["documents"].append({"name": name.strip(), "format": fmt.strip(), "url": url})
        meetings.append(mt)
    return meetings


def parse_page(path: Path) -> dict:
    root = parse_html(path.read_text(encoding="utf-8", errors="replace"))
    h1 = root.find("h1")
    sub = root.find("p", cls="subtitle")
    page = {"title": h1.text() if h1 else path.stem, "summary": sub.text() if sub else "",
            "topics": [], "agenda": [], "flags": [], "links": []}

    def first_link(n):
        a = n.find("a")
        return a.attrs.get("href") if a else None

    for sec_id in ("topics", "agenda"):
        h2 = root.find("h2", id_=sec_id)
        if not h2:
            continue
        for n in section_nodes(h2):
            for tr in n.find_all("tr"):
                tds = [c for c in tr.children if isinstance(c, Node) and c.tag == "td"]
                if len(tds) < 3:
                    continue
                row = {"time": tds[0].text(), "url": first_link(tds[0]) or first_link(tds[2]),
                       "label": tds[1].text(), "text": tds[2].text()}
                page[sec_id].append(row)
    for art in root.find_all("article", cls="flag"):
        h3 = art.find("h3")
        title = h3.text() if h3 else ""
        sev = ""
        chip = art.find("span", cls="chip")
        if chip:
            sev = chip.text()
            title = title[len(sev):].strip() if title.startswith(sev) else title
        body = " ".join(p.text() for p in art.find_all("p"))
        page["flags"].append({"severity": sev, "title": title, "text": body,
                              "url": first_link(art), "anchor": art.attrs.get("id")})
    h2 = root.find("h2", id_="appendix")
    if h2:
        for n in section_nodes(h2):
            for a in n.find_all("a"):
                href = a.attrs.get("href", "")
                if href.startswith("http"):
                    page["links"].append({"name": a.text(), "url": href})
    return page


def parse_report(path: Path) -> list[dict]:
    root = parse_html(path.read_text(encoding="utf-8", errors="replace"))
    h1 = root.find("h1")
    title = h1.text() if h1 else path.stem
    chunks = []
    for h2 in root.find_all("h2"):
        body = " ".join(n.text() for n in section_nodes(h2))
        chunks.append({"title": f"{title}: {h2.text()}", "anchor": h2.attrs.get("id"), "text": body[:6000]})
    if not chunks:
        chunks.append({"title": title, "anchor": None, "text": root.text()[:6000]})
    return chunks


def parse_policy_index(path: Path) -> list[dict]:
    out, section = [], ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# Section"):
            section = line.lstrip("# ").strip()
            continue
        for m in LINK.finditer(line):
            label, url = m.group(1).strip(), m.group(2)
            code = label.split()[0].strip("()")
            if not re.match(r"^[A-L][A-Z]{0,4}(-[A-Z0-9()]+)*$", code):
                continue
            rest = line[m.end(): m.end() + 40]
            dm = re.match(r"\s*\(?(\d{1,2}/\d{1,2}/\d{4})", rest)
            adopted = parse_short_date(dm.group(1)) if dm else None
            out.append({"code": code, "label": label.strip("()"), "url": url,
                        "section": section, "adopted": adopted})
    return out


# ---------------------------------------------------------------- build

KG_SCHEMA = """
CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE meetings (
  id INTEGER PRIMARY KEY, section TEXT, body TEXT, date TEXT, title TEXT, show_id TEXT,
  video_url TEXT, video_title TEXT, folder_url TEXT, folder_name TEXT, page_file TEXT,
  page_url TEXT, dialogue_file TEXT, summary TEXT, n_documents INTEGER, n_minutes INTEGER);
CREATE INDEX ix_meet_date ON meetings(date);
CREATE TABLE items (
  id INTEGER PRIMARY KEY, kind TEXT, meeting_id INTEGER, title TEXT, body TEXT, url TEXT,
  date TEXT, extra TEXT);
CREATE INDEX ix_items_kind ON items(kind);
CREATE INDEX ix_items_meeting ON items(meeting_id);
CREATE VIRTUAL TABLE items_fts USING fts5(title, body, content='items', content_rowid='id',
  tokenize='porter unicode61');
CREATE TABLE dialogue (
  id INTEGER PRIMARY KEY, meeting_id INTEGER, start_sec INTEGER, speaker TEXT, text TEXT, url TEXT);
CREATE VIRTUAL TABLE dialogue_fts USING fts5(text, speaker, content='dialogue', content_rowid='id',
  tokenize='porter unicode61');
"""


def build(repo: Path, out: Path, navigator_url: str, policy_index: Path | None = None,
          dialogue: bool = True, log=print) -> dict:
    repo = Path(repo)
    nav = navigator_url if navigator_url.endswith("/") else navigator_url + "/"
    map_path = repo / "Input" / "SupportingDocuments" / "MAP.md"
    html_dir = repo / "Output" / "HTML"
    dlg_dir = html_dir / "Dialogue"
    if not map_path.exists():
        raise FileNotFoundError(f"MAP.md not found under {repo}")
    policy_index = policy_index or (PKG_DATA / "policy_index.md")

    out.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix="kg-", suffix=".db", dir=str(out.parent))
    os.close(fd)
    conn = sqlite3.connect(tmp)
    conn.executescript(KG_SCHEMA)
    counts = {"meetings": 0, "documents": 0, "minutes": 0, "topics": 0, "flags": 0,
              "agenda": 0, "policies": 0, "reports": 0, "dialogue": 0, "pages": 0}

    def add_item(kind, meeting_id, title, body, url, d, extra=None):
        conn.execute("INSERT INTO items(kind, meeting_id, title, body, url, date, extra) VALUES(?,?,?,?,?,?,?)",
                     (kind, meeting_id, title, body, url, d, json.dumps(extra) if extra else None))

    def index_page(mid, mt, page, page_url, known):
        d = mt["date"]
        for link in page["links"]:
            if link["url"] in known or "cablecast" in link["url"]:
                continue
            if "drive.google.com" in link["url"] or "docs.google.com" in link["url"]:
                known.add(link["url"])
                add_item(doc_kind(link["name"]), mid, link["name"], f"{mt['title']} (page appendix)", link["url"], d)
                counts["documents"] += 1
        for t in page["topics"]:
            add_item("topic", mid, f"{t['label']} ({mt['title']}, {t['time']})", t["text"],
                     t["url"] or page_url, d, {"time": t["time"]})
            counts["topics"] += 1
        for a in page["agenda"]:
            add_item("agenda_item", mid, f"Agenda: {a['label']} ({mt['title']})", a["text"],
                     a["url"] or page_url, d)
            counts["agenda"] += 1
        for fl in page["flags"]:
            url = page_url + ("#" + fl["anchor"] if fl["anchor"] else "#flags")
            add_item("flag", mid, f"Flag ({fl['severity'] or 'review'}): {fl['title']} ({mt['title']})",
                     fl["text"], url, d, {"severity": fl["severity"]})
            counts["flags"] += 1

    def index_dialogue(mid, path):
        if not path.exists():
            return
        with open(path, encoding="utf-8-sig", newline="") as fh:
            rows = []
            for r in csv.DictReader(fh):
                txt = (r.get("Dialogue") or "").strip()
                if not txt:
                    continue
                try:
                    sec = int(float(r.get("Start (sec)") or 0))
                except ValueError:
                    sec = 0
                rows.append((mid, sec, (r.get("Speaker") or "").strip(), txt, (r.get("Video URL") or "").strip()))
        conn.executemany("INSERT INTO dialogue(meeting_id, start_sec, speaker, text, url) VALUES(?,?,?,?,?)", rows)
        counts["dialogue"] += len(rows)

    meetings = parse_map(map_path)
    page_files = {p.name for p in html_dir.glob("*.HTML")}
    used_pages = set()
    for mt in meetings:
        page_file = None
        if mt["dialogue_file"]:
            cand = mt["dialogue_file"][: -len(".CSV")] + ".HTML"
            if cand in page_files:
                page_file = cand
        page = parse_page(html_dir / page_file) if page_file else None
        if page_file:
            used_pages.add(page_file)
            counts["pages"] += 1
        page_url = nav + quote(page_file) if page_file else None
        cur = conn.execute(
            "INSERT INTO meetings(section, body, date, title, show_id, video_url, video_title, folder_url,"
            " folder_name, page_file, page_url, dialogue_file, summary, n_documents, n_minutes)"
            " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (mt["section"], mt["body"], mt["date"], mt["title"], mt["show_id"], mt["video_url"],
             mt["video_title"], mt["folder_url"], mt["folder_name"], page_file, page_url,
             mt["dialogue_file"], page["summary"] if page else "", len(mt["documents"]), len(mt["minutes"])))
        mid = cur.lastrowid
        counts["meetings"] += 1
        d = mt["date"]
        agenda_names = " ".join(a["label"] for a in page["agenda"]) if page else ""
        add_item("meeting", mid, f"{mt['title']} (meeting page)",
                 " ".join(filter(None, [mt["body"], mt["date_text"], page["summary"] if page else "", agenda_names])),
                 page_url or mt["video_url"], d,
                 {"video_url": mt["video_url"], "folder_url": mt["folder_url"]})
        if mt["video_url"]:
            add_item("recording", mid, f"Recording: {mt['video_title'] or mt['title']}",
                     f"{mt['title']} Cablecast recording video show {mt['show_id']}", mt["video_url"], d)
        if mt["folder_url"]:
            add_item("folder", mid, f"Packet folder: {mt['folder_name']}",
                     f"{mt['title']} board packet documents folder", mt["folder_url"], d)
        for m in mt["minutes"]:
            # MAP.md "Minutes:" lines are this meeting's own minutes; minutes filed
            # in a packet are usually an earlier meeting's, so they are marked apart.
            add_item("minutes", mid, m["name"], f"{mt['title']} minutes of this meeting", m["url"], d, {"own": True})
            counts["minutes"] += 1
        known = {m["url"] for m in mt["minutes"]}
        for doc in mt["documents"]:
            if doc["url"] in known:
                continue
            known.add(doc["url"])
            add_item(doc_kind(doc["name"]), mid, doc["name"], f"{mt['title']} {doc['format']}", doc["url"], d,
                     {"own": False, "filed_in": mt["folder_name"]})
            counts["documents"] += 1
        mt["_id"] = mid
        if page:
            index_page(mid, mt, page, page_url, known)
        if dialogue and mt["dialogue_file"]:
            index_dialogue(mid, dlg_dir / mt["dialogue_file"])

    # A meeting with a second recording (a split or excerpt file) has a second
    # page whose dialogue name is not the section's first. Attach it by show id.
    for name in sorted(page_files - used_pages):
        pm = re.match(r"^(\d{4,5}) ", name)
        if not pm:
            continue
        owner = next((mt for mt in meetings if "_id" in mt and pm.group(1) in mt["raw"]), None)
        if owner is None:
            continue
        page = parse_page(html_dir / name)
        page_url = nav + quote(name)
        used_pages.add(name)
        counts["pages"] += 1
        add_item("meeting", owner["_id"], f"{page['title']} (meeting page, second recording)",
                 page["summary"], page_url, owner["date"])
        index_page(owner["_id"], owner, page, page_url, set())
        if dialogue:
            index_dialogue(owner["_id"], dlg_dir / (name[: -len(".HTML")] + ".CSV"))

    # Reports: every other top-level page plus Reports/**.
    for p in sorted(list(html_dir.glob("*.HTML")) + list((html_dir / "Reports").rglob("*.HTML"))):
        if p.name in used_pages or p.name.lower() == "index.html" or (p.parent == html_dir and _is_meeting_page(p.name)):
            continue
        rel = p.relative_to(html_dir).as_posix()
        for ch in parse_report(p):
            url = nav + quote(rel) + ("#" + ch["anchor"] if ch["anchor"] else "")
            add_item("report", None, ch["title"], ch["text"], url, None)
            counts["reports"] += 1

    if policy_index.exists():
        for pol in parse_policy_index(policy_index):
            add_item("policy", None, f"Policy {pol['label']}",
                     f"Claremont School Board policy {pol['code']} {pol['label']} {pol['section']}",
                     pol["url"], None, {"code": pol["code"], "adopted": pol["adopted"]})
            counts["policies"] += 1
        add_item("policy", None, "Claremont School Board policy index",
                 "Index of all Claremont School Board policies sections A through L", POLICY_INDEX_URL, None)

    conn.execute("INSERT INTO items_fts(rowid, title, body) SELECT id, title, body FROM items")
    conn.execute("INSERT INTO dialogue_fts(rowid, text, speaker) SELECT id, text, speaker FROM dialogue")
    commit = _git_head(repo)
    meta = {"built_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "repo": str(repo), "repo_commit": commit, "navigator_url": nav,
            "counts": json.dumps(counts),
            "date_min": conn.execute("SELECT MIN(date) FROM meetings").fetchone()[0],
            "date_max": conn.execute("SELECT MAX(date) FROM meetings").fetchone()[0]}
    conn.executemany("INSERT INTO meta(key, value) VALUES(?,?)", list(meta.items()))
    conn.commit()
    conn.execute("INSERT INTO items_fts(items_fts) VALUES('optimize')")
    conn.commit()
    conn.close()
    os.replace(tmp, out)
    log(f"knowledge graph index written to {out}: {counts}")
    return counts


def _is_meeting_page(name: str) -> bool:
    return bool(re.match(r"^\d{4,5} ", name)) or name.startswith(("Claremont School Board", "School Board Finance"))


def _git_head(repo: Path) -> str | None:
    head = repo / ".git" / "HEAD"
    try:
        ref = head.read_text().strip()
        if ref.startswith("ref: "):
            return (repo / ".git" / ref[5:]).read_text().strip()[:12]
        return ref[:12]
    except OSError:
        return None


# ---------------------------------------------------------------- search

@dataclass
class Hit:
    ref: str
    kind: str
    title: str
    url: str | None
    date: str | None
    snippet: str
    score: float
    coverage: float = 0.0
    meeting_id: int | None = None
    meeting_title: str | None = None
    meeting_url: str | None = None

    def to_dict(self):
        return asdict(self)


def tokens(text: str) -> list[str]:
    out, seen = [], set()
    for t in re.findall(r"[A-Za-z0-9][A-Za-z0-9'-]*", text or ""):
        t = t.lower().strip("'-")
        if len(t) < 3 and not t.isdigit():
            continue
        if t in STOPWORDS or t in seen:
            continue
        seen.add(t)
        out.append(t)
    return out


def _stem(t: str) -> str:
    for suf in ("ings", "ing", "ies", "ied", "es", "ed", "s", "ly"):
        if len(t) > len(suf) + 3 and t.endswith(suf):
            return t[: -len(suf)]
    return t


def fts_query(terms: list[str]) -> str:
    return " OR ".join('"' + t.replace('"', "") + '"' for t in terms[:24])


def coverage(terms: list[str], text: str) -> float:
    if not terms:
        return 0.0
    low = (text or "").lower()
    return sum(1 for t in terms if _stem(t) in low) / len(terms)


class KG:
    def __init__(self, path: Path | str):
        self.path = Path(path)

    @property
    def available(self) -> bool:
        return self.path.exists()

    def _conn(self):
        conn = sqlite3.connect(self.path.resolve().as_uri() + "?mode=ro", uri=True, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def meta(self) -> dict:
        if not self.available:
            return {}
        with self._conn() as c:
            m = {r["key"]: r["value"] for r in c.execute("SELECT key, value FROM meta")}
        if "counts" in m:
            m["counts"] = json.loads(m["counts"])
        return m

    def meeting(self, mid: int) -> dict | None:
        if not self.available:
            return None
        with self._conn() as c:
            r = c.execute("SELECT * FROM meetings WHERE id=?", (mid,)).fetchone()
            return dict(r) if r else None

    def meetings_between(self, d1: str, d2: str) -> list[dict]:
        if not self.available:
            return []
        with self._conn() as c:
            rows = c.execute("SELECT * FROM meetings WHERE date BETWEEN ? AND ? ORDER BY date", (d1, d2)).fetchall()
            return [dict(r) for r in rows]

    def meeting_resources(self, mid: int) -> list[dict]:
        with self._conn() as c:
            rows = c.execute("SELECT id, kind, title, url, date, extra FROM items WHERE meeting_id=? AND kind IN"
                             " ('meeting','recording','folder','minutes','agenda','document') ORDER BY"
                             " CASE kind WHEN 'meeting' THEN 0 WHEN 'minutes' THEN 1 WHEN 'agenda' THEN 2"
                             " WHEN 'recording' THEN 3 WHEN 'folder' THEN 4 ELSE 5 END, id", (mid,)).fetchall()
            out = []
            for r in rows:
                d = dict(r)
                d["extra"] = json.loads(d["extra"]) if d["extra"] else {}
                d["ref"] = f"item:{d['id']}"
                out.append(d)
            return out

    def policy(self, code: str) -> list[dict]:
        if not self.available:
            return []
        with self._conn() as c:
            rows = c.execute("SELECT id, kind, title, url, extra FROM items WHERE kind='policy' AND"
                             " json_extract(extra, '$.code') = ?", (code.upper(),)).fetchall()
            return [dict(r) | {"ref": f"item:{r['id']}"} for r in rows]

    def search(self, q: str, kinds: list[str] | None = None, date_from: str | None = None,
               date_to: str | None = None, limit: int = 12, dialogue_limit: int = 4) -> list[Hit]:
        if not self.available:
            return []
        terms = tokens(q)
        if not terms:
            return []
        match = fts_query(terms)
        hits: list[Hit] = []
        with self._conn() as c:
            meet = {}
            sql = ("SELECT i.id, i.kind, i.title, i.body, i.url, i.date, i.meeting_id, "
                   "bm25(items_fts, 4.0, 1.0) AS score, "
                   "snippet(items_fts, 1, char(2), char(3), ' ... ', 24) AS snip "
                   "FROM items_fts JOIN items i ON i.id = items_fts.rowid WHERE items_fts MATCH ?")
            args: list = [match]
            if kinds:
                sql += " AND i.kind IN (%s)" % ",".join("?" * len(kinds))
                args += kinds
            if date_from:
                sql += " AND (i.date IS NULL OR i.date >= ?)"
                args.append(date_from)
            if date_to:
                sql += " AND (i.date IS NULL OR i.date <= ?)"
                args.append(date_to)
            sql += " ORDER BY score LIMIT ?"
            args.append(limit * 3)
            for r in c.execute(sql, args):
                cov = coverage(terms, f"{r['title']} {r['body']}")
                hits.append(Hit(f"item:{r['id']}", r["kind"], r["title"], r["url"], r["date"],
                                r["snip"] or "", round(r["score"], 3), round(cov, 2), r["meeting_id"]))
            # Re-rank: term coverage first, then bm25, so a hit that matches all of
            # the request's words beats one that repeats a single word.
            hits.sort(key=lambda h: (-h.coverage, h.score))
            hits = hits[:limit]
            if dialogue_limit and (not kinds or "dialogue" in kinds):
                dsql = ("SELECT d.id, d.meeting_id, d.start_sec, d.speaker, d.url, d.text, "
                        "bm25(dialogue_fts) AS score, snippet(dialogue_fts, 0, char(2), char(3), ' ... ', 24) AS snip, "
                        "m.date AS date, m.title AS mtitle FROM dialogue_fts JOIN dialogue d ON d.id = dialogue_fts.rowid "
                        "JOIN meetings m ON m.id = d.meeting_id WHERE dialogue_fts MATCH ?")
                dargs: list = [match]
                if date_from:
                    dsql += " AND m.date >= ?"
                    dargs.append(date_from)
                if date_to:
                    dsql += " AND m.date <= ?"
                    dargs.append(date_to)
                dsql += " ORDER BY score LIMIT ?"
                dargs.append(dialogue_limit * 5)
                drows = []
                for r in c.execute(dsql, dargs):
                    cov = coverage(terms, r["text"])
                    drows.append(Hit(f"dialogue:{r['id']}", "dialogue",
                                     f"{r['speaker'] or 'Speaker'} at {hms(r['start_sec'])}, {r['mtitle']}",
                                     r["url"], r["date"], r["snip"] or "", round(r["score"], 3), round(cov, 2),
                                     r["meeting_id"]))
                drows.sort(key=lambda h: (-h.coverage, h.score))
                hits += drows[:dialogue_limit]
            for h in hits:
                if h.meeting_id:
                    if h.meeting_id not in meet:
                        m = c.execute("SELECT title, page_url, video_url FROM meetings WHERE id=?", (h.meeting_id,)).fetchone()
                        meet[h.meeting_id] = (m["title"], m["page_url"] or m["video_url"]) if m else (None, None)
                    h.meeting_title, h.meeting_url = meet[h.meeting_id]
        return hits

    def get_hits(self, refs: list[str]) -> list[Hit]:
        """Re-fetch hits by ref, for a reviewer re-opening a draft."""
        out = []
        if not self.available:
            return out
        with self._conn() as c:
            for ref in refs:
                kind, _, n = ref.partition(":")
                if kind == "item":
                    r = c.execute("SELECT * FROM items WHERE id=?", (n,)).fetchone()
                    if r:
                        out.append(Hit(ref, r["kind"], r["title"], r["url"], r["date"], (r["body"] or "")[:200], 0, 0, r["meeting_id"]))
                elif kind == "dialogue":
                    r = c.execute("SELECT d.*, m.title AS mtitle, m.date AS mdate FROM dialogue d JOIN meetings m ON m.id=d.meeting_id WHERE d.id=?", (n,)).fetchone()
                    if r:
                        out.append(Hit(ref, "dialogue", f"{r['speaker']} at {hms(r['start_sec'])}, {r['mtitle']}",
                                       r["url"], r["mdate"], r["text"][:200], 0, 0, r["meeting_id"]))
        return out


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m rtk_portal.kg")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="index a CSBMN checkout")
    b.add_argument("--repo", required=True)
    b.add_argument("--out", default=os.environ.get("RTK_DATA_DIR", "data") + "/kg.db")
    b.add_argument("--navigator-url", default=os.environ.get("RTK_NAVIGATOR_URL", "https://csbmn.claremontv.org/"))
    b.add_argument("--policy-index", default=None)
    b.add_argument("--no-dialogue", action="store_true")
    s = sub.add_parser("search", help="query the index")
    s.add_argument("q")
    s.add_argument("--db", default=os.environ.get("RTK_DATA_DIR", "data") + "/kg.db")
    s.add_argument("--from", dest="date_from")
    s.add_argument("--to", dest="date_to")
    s.add_argument("--kind", action="append")
    a = ap.parse_args(argv)
    if a.cmd == "build":
        build(Path(a.repo), Path(a.out), a.navigator_url,
              Path(a.policy_index) if a.policy_index else None, dialogue=not a.no_dialogue)
    else:
        for h in KG(a.db).search(a.q, a.kind, a.date_from, a.date_to):
            snip = h.snippet.replace("\x02", "[").replace("\x03", "]")
            print(f"{h.coverage:.2f} {h.kind:10} {h.date or '':10} {h.title}\n      {h.url}\n      {snip[:160]}")


if __name__ == "__main__":
    main()
