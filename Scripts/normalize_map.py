#!/usr/bin/env python3
"""Undo the flattening of MAP.md into the layout the map skills write.

  python3 normalize_map.py IN.md OUT.md

1. In each section's "Video:" paragraph, put "Remote video:", "Drive folder:"
   and "Minutes:" back on their own lines (they had been joined with spaces).
2. Rebuild each one-cell-per-paragraph "Document / Format / Link" table as a
   pipe table.
3. Turn pandoc-style "-   " bullets (and their 4-space continuation indent)
   into "- " bullets with a 2-space continuation indent.
Nothing else changes. Exits non-zero if a table does not parse cleanly.
"""
import re
import sys

src, dst = sys.argv[1], sys.argv[2]
text = open(src, encoding="utf-8").read()
paras = text.split("\n\n")

SPLIT = re.compile(r" (?=(?:Remote video|Drive folder|Minutes): \[)")
LINK = re.compile(r"^\[[^\]]+\]\([^)\s]+\)$")

out, i, tables, rows = [], 0, 0, 0
while i < len(paras):
    p = paras[i]
    if p.startswith("Video:"):
        out.append(SPLIT.sub("\n", p))
        i += 1
        continue
    if p == "Document" and paras[i + 1:i + 3] == ["Format", "Link"]:
        j = i + 3
        lines = ["| Document | Format | Link |", "|---|---|---|"]
        while j + 2 < len(paras):
            trio = paras[j:j + 3]
            if not LINK.match(trio[2].strip()) or trio[0].startswith(("## ", "Video:")):
                break
            cells = [c.strip().replace("|", "\\|") for c in trio]
            if any("\n" in c for c in cells):
                sys.exit(f"multi-line table cell near: {cells[0][:80]}")
            lines.append("| " + " | ".join(cells) + " |")
            j += 3
            rows += 1
        if len(lines) == 2:
            sys.exit(f"empty table at paragraph {i}")
        out.append("\n".join(lines))
        tables += 1
        i = j
        continue
    if p.lstrip("\n").startswith("-   "):
        p = re.sub(r"(?m)^-   ", "- ", p)
        p = re.sub(r"(?m)^    (?=\S)", "  ", p)
    out.append(p)
    i += 1

open(dst, "w", encoding="utf-8").write("\n\n".join(out))
print(f"tables rebuilt: {tables}, rows: {rows}")
