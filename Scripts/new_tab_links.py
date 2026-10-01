import os, re, sys
# Video and document links open in a new tab, and screen readers are told so.
# - Adds target="_blank" rel="noopener" aria-describedby="newtab-note" to every
#   http(s) link and every link into Dialogue/. In-page #anchors, sibling site
#   pages (.HTML/.html) and mailto: stay in the same tab.
# - Gives each page that has such links one hidden description element,
#   <span id="newtab-note" hidden>Opens in a new tab.</span>, placed right
#   after <body>. Screen readers read it as the description of each new-tab
#   link (WCAG technique G201); sighted layout is unchanged.
# The new attributes go right after href so validate_pages.py (which expects
# <a href="..." first on seekto links) keeps matching. Idempotent.
# Usage: python3 new_tab_links.py Output/HTML [--check]
A = re.compile(r'<a\s[^>]*>', re.I)
H = re.compile(r'\shref="([^"]*)"')
NOTE = '<span id="newtab-note" hidden>Opens in a new tab.</span>'
def wants(h):
    return h.startswith(('http://', 'https://', 'Dialogue/'))
def fix(tag):
    m = H.search(tag)
    if not m or not wants(m.group(1)):
        return tag
    t = re.search(r'\starget="([^"]*)"', tag)
    if t and t.group(1) != '_blank':
        return tag                      # an explicit other target is kept
    add = ''
    if not t:
        add += ' target="_blank"'
    if 'rel="noopener"' not in tag and not re.search(r'\srel=', tag):
        add += ' rel="noopener"'
    if 'aria-describedby=' not in tag:
        add += ' aria-describedby="newtab-note"'
    if not add:
        return tag
    if not t:                           # new attributes go right after href
        return tag[:m.end()] + add + tag[m.end():]
    return tag[:-1] + add + '>'
d = sys.argv[1]
check = '--check' in sys.argv
files = links = 0
for f in sorted(os.listdir(d)):
    if not f.lower().endswith('.html'):
        continue
    p = os.path.join(d, f)
    raw = open(p, encoding='utf-8').read()
    n = [0]
    def sub(m):
        new = fix(m.group(0))
        if new != m.group(0):
            n[0] += 1
        return new
    out = A.sub(sub, raw)
    if 'aria-describedby="newtab-note"' in out and 'id="newtab-note"' not in out:
        out = re.sub(r'(<body[^>]*>)', r'\1\n' + NOTE, out, count=1)
    if out != raw:
        if check:
            print(f, n[0], 'links need new-tab attributes or the page lacks the note')
        else:
            open(p, 'w', encoding='utf-8').write(out)
            files += 1; links += n[0]
if not check:
    print(f'{links} links updated in {files} files')
