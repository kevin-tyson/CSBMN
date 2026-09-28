#!/usr/bin/env python3
#
# Copyright 2026 Kevin Tyson
# SPDX-License-Identifier: Apache-2.0
#
"""Validate Government Transparency Project meeting pages before delivery.

Checks every *.HTML file in the given directory (plus style.css) for:
  structure   - balanced tags, no stray closers, no duplicate ids
  anchors     - every internal #fragment resolves; cross-page links exist
  stylesheet  - page links style.css; no <style> blocks or inline style= attrs
  disclaimer  - required text present in style.css (body::after) and NOT in HTML
  snippets    - .snip elements carry tabindex="0" (keyboard access); CSS expands
                on :hover and :focus
  contrast    - WCAG ratios for the :root palette pairs (AA: 4.5 text, 3.0 UI)
  rel-links   - with --project-root, ../ links resolve on disk
  timestamps  - seekto deep links: link seconds equal the displayed H:MM:SS,
                every link written with &amp;, all links on a page use one show
                ID that a plain (non-seekto) Cablecast link on the page also
                uses, no unlinked <td class="num"> timestamps when the page
                knows a Cablecast URL, and the required sentence "Timestamps
                link to the same moment in the Cablecast recording." appears
                on any page with seekto links

Exit code 0 = clean, 1 = problems (each printed with file and reason).
Plain-text H:MM:SS outside links are printed as non-fatal "note -" lines:
each must be a recording-length/cutoff value left unlinked on purpose —
review them, they do not affect the exit code.

Usage:
  python3 validate_pages.py Output/HTML [--project-root /path/to/project]
"""
import argparse, os, re, sys, urllib.parse
from html.parser import HTMLParser

DISCLAIMER = "AI-Generated Content from official sources. Not warranted for any use."
VOID = {"meta", "link", "br", "hr", "img", "input", "wbr", "col", "source"}

problems: list[str] = []
notes: list[str] = []


def err(fn: str, msg: str) -> None:
    problems.append(f"{fn}: {msg}")


def note(fn: str, msg: str) -> None:
    notes.append(f"{fn}: {msg}")


TS_RE = re.compile(r"(?<![\d:])(\d+):(\d{2}):(\d{2})(?![\d:])")
SEEK_A = re.compile(r'<a href="([^"]*[?&](?:amp;)?seekto=(\d+))"[^>]*>([^<]*)</a>')
SHOW_RE = re.compile(r"cablecast\.tv/internetchannel/show/(\d+)")
LINK_SENTENCE = "Timestamps link to the same moment in the Cablecast recording"


def check_timestamps(fn: str, raw: str) -> None:
    """Enforce the seekto deep-link convention (see references/page-template.md)."""
    shows_plain = {SHOW_RE.search(h).group(1)
                   for h in re.findall(r'<a href="([^"]*)"', raw)
                   if "seekto=" not in h and SHOW_RE.search(h)}
    seek_shows: set[str] = set()
    n_seek = 0
    for m in SEEK_A.finditer(raw):
        href, sec, text = m.group(1), int(m.group(2)), m.group(3).strip()
        n_seek += 1
        t = TS_RE.fullmatch(text)
        if not t:
            err(fn, f"seekto link text is not H:MM:SS: {text!r}")
        elif int(t.group(1)) * 3600 + int(t.group(2)) * 60 + int(t.group(3)) != sec:
            err(fn, f"seekto={sec} disagrees with displayed time {text}")
        sm = SHOW_RE.search(href)
        if sm:
            seek_shows.add(sm.group(1))
        else:
            err(fn, f"seekto link is not a Cablecast show URL: {href}")
    if re.search(r"&(?!amp;)seekto=", raw):
        err(fn, "seekto joined with bare '&' — write '&amp;' in the href")
    if len(seek_shows) > 1:
        err(fn, f"seekto links point at more than one show: {sorted(seek_shows)}")
    if seek_shows and shows_plain and not seek_shows <= shows_plain:
        err(fn, f"seekto show {sorted(seek_shows)} never appears as a plain "
                f"Recording/appendix link (page links show(s) {sorted(shows_plain)})")
    unlinked_num = re.findall(r'<td class="num">(\d+:\d{2}:\d{2})</td>', raw)
    if unlinked_num and (shows_plain or seek_shows):
        err(fn, f"{len(unlinked_num)} timeline/agenda timestamp(s) not deep-linked "
                f"(e.g. {unlinked_num[0]}) although the page knows a Cablecast URL")
    if n_seek and LINK_SENTENCE not in raw:
        err(fn, f'page has seekto links but lacks the sentence "{LINK_SENTENCE}…" '
                f"(subtitle or timeline intro; continuing the sentence is fine)")
    # plain-text times outside any <a>: legitimate only for durations/cutoffs
    depth = skip = 0
    for part in re.split(r"(<[^>]+>)", raw):
        if part.startswith("<"):
            low = part.lower()
            if re.match(r"<a[\s>]", low):
                depth += 1
            elif re.match(r"</a\s*>", low):
                depth = max(0, depth - 1)
            elif re.match(r"<(title|script|style)\b", low):
                skip += 1
            elif re.match(r"</(title|script|style)\b", low):
                skip = max(0, skip - 1)
            continue
        if depth == 0 and skip == 0:
            for m in TS_RE.finditer(part):
                note(fn, f"plain-text time {m.group(0)} — confirm it names a "
                         f"recording length/cutoff, not a moment that should link")


class Scan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.ids: list[str] = []
        self.hrefs: list[str] = []
        self.style_blocks = 0
        self.inline_styles = 0
        self.css_links: list[str] = []
        self.snips_missing_tabindex = 0
        self.snips = 0
        self.errors: list[str] = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if "id" in d:
            self.ids.append(d["id"])
        if "style" in d:
            self.inline_styles += 1
        if tag == "a" and "href" in d:
            self.hrefs.append(d["href"])
        if tag == "style":
            self.style_blocks += 1
        if tag == "link" and d.get("rel") == "stylesheet":
            self.css_links.append(d.get("href", ""))
        cls = d.get("class", "")
        if "snip" in cls.split():
            self.snips += 1
            if d.get("tabindex") != "0":
                self.snips_missing_tabindex += 1
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"</{tag}> with empty stack")
        elif self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            while self.stack and self.stack[-1] != tag:
                self.errors.append(f"<{self.stack[-1]}> implicitly closed by </{tag}>")
                self.stack.pop()
            self.stack.pop()
        else:
            self.errors.append(f"stray </{tag}>")


def luminance(hexstr: str) -> float:
    hexstr = hexstr.lstrip("#")
    r, g, b = (int(hexstr[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = f(r), f(g), f(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def check_css(css_path: str) -> None:
    fn = os.path.basename(css_path)
    css = open(css_path, encoding="utf-8").read()
    if DISCLAIMER not in css:
        err(fn, "required disclaimer text not found (should live in body::after)")
    if "body::after" not in css:
        err(fn, "no body::after rule — disclaimer must be CSS-injected")
    if not re.search(r"\.snip[^{]*:hover", css) or not re.search(r"\.snip[^{]*:focus", css):
        err(fn, ".snip must expand on both :hover and :focus (keyboard access)")
    vars_ = dict(re.findall(r"--([a-z0-9-]+):\s*#([0-9a-fA-F]{6})", css))
    def pair(fg, bg, need, label):
        if fg in vars_ and bg in vars_:
            r = contrast(vars_[fg], vars_[bg])
            if r < need:
                err(fn, f"contrast {label} = {r:.2f} (< {need})")
    pair("ink", "paper", 4.5, "ink/paper")
    pair("muted", "paper", 4.5, "muted/paper")
    pair("accent", "paper", 4.5, "accent/paper")
    pair("ink", "panel", 4.5, "ink/panel")
    pair("focus", "paper", 3.0, "focus ring/paper")
    for sev in ("high", "med", "obs", "pos"):
        pair(f"flag-{sev}-ink", f"flag-{sev}-bg", 4.5, f"{sev} chip")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html_dir", help="directory containing the .HTML pages and style.css")
    ap.add_argument("--project-root", default=None,
                    help="project root on disk; enables ../ relative-link existence checks")
    args = ap.parse_args()

    d = args.html_dir
    pages = sorted(f for f in os.listdir(d) if f.lower().endswith(".html"))
    if not pages:
        raise SystemExit(f"no .HTML files in {d}")

    css_path = os.path.join(d, "style.css")
    if os.path.exists(css_path):
        check_css(css_path)
    else:
        err("style.css", "missing from the output directory")

    page_ids: dict[str, set] = {}
    scans: dict[str, Scan] = {}
    for fn in pages:
        raw = open(os.path.join(d, fn), encoding="utf-8").read()
        s = Scan()
        s.feed(raw)
        scans[fn] = s
        check_timestamps(fn, raw)
        page_ids[fn] = set(s.ids)
        if s.stack:
            err(fn, f"unclosed tags at EOF: {s.stack}")
        for e in s.errors:
            err(fn, e)
        dupes = {i for i in s.ids if s.ids.count(i) > 1}
        if dupes:
            err(fn, f"duplicate ids: {sorted(dupes)}")
        if "style.css" not in [os.path.basename(u) for u in s.css_links]:
            err(fn, "does not link style.css")
        if s.style_blocks:
            err(fn, f"{s.style_blocks} <style> block(s) — styles belong in style.css")
        if s.inline_styles:
            err(fn, f"{s.inline_styles} inline style= attribute(s)")
        if s.snips and s.snips_missing_tabindex:
            err(fn, f"{s.snips_missing_tabindex}/{s.snips} .snip elements lack tabindex=\"0\"")
        body_text = re.sub(r"<[^>]+>", " ", raw)
        if DISCLAIMER in body_text:
            err(fn, "disclaimer text duplicated in HTML — it must come only from style.css")

    for fn, s in scans.items():
        for h in s.hrefs:
            if h.startswith("#"):
                if h[1:] not in page_ids[fn]:
                    err(fn, f"unresolved anchor {h}")
            elif h.lower().split("#")[0].endswith(".html") and not h.startswith(("http://", "https://")):
                target = urllib.parse.unquote(h.split("#")[0])
                frag = h.split("#")[1] if "#" in h else None
                tpath = os.path.join(d, target)
                if not os.path.exists(tpath):
                    err(fn, f"cross-page link target missing: {target}")
                elif frag and os.path.basename(target) in page_ids and frag not in page_ids[os.path.basename(target)]:
                    err(fn, f"cross-page fragment missing: {h}")
            elif h.startswith("../") and args.project_root:
                rel = urllib.parse.unquote(h)
                full = os.path.normpath(os.path.join(args.project_root, "Output/HTML", rel))
                if not os.path.exists(full):
                    err(fn, f"relative link does not resolve: {h}")

    if notes:
        print(f"{len(notes)} note(s) — review, not automatically errors:")
        for n in notes:
            print("  note -", n)
    if problems:
        print(f"FAIL — {len(problems)} problem(s):")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print(f"OK — {len(pages)} page(s) + style.css passed all checks")


if __name__ == "__main__":
    main()
