#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2026 Kevin Tyson
# SPDX-License-Identifier: Apache-2.0
#
"""
Build Output/CSBMN-<newest>-<oldest>.DOCX from Output/HTML/index.html and every
local .HTML page it links to.

  * index.html becomes the first document section
  * every local HTML link target is appended as its own section
  * every <a href="local.HTML#frag"> becomes an internal DOCX bookmark link
  * narrow (0.5in) margins, dense typography, Section 508 conventions carried
    over from Output/HTML/style.css

Raw WordprocessingML is emitted directly (no python-docx) because the corpus is
~2 million words; a DOM-per-paragraph library is far too slow at this size.
"""
import os, re, sys, html, zipfile, urllib.parse, datetime
from lxml import html as LH

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
HTMLDIR = os.path.join(ROOT, 'Output', 'HTML')
OUTDIR = os.path.join(ROOT, 'Output')
INDEX = 'index.html'

# ---------------------------------------------------------------- palette ----
# lifted from Output/HTML/style.css (contrast ratios verified there)
INK        = '1A2733'
MUTED      = '44535F'
ACCENT     = '14558F'
ACCENT_INK = '0F3F6B'
RULE       = 'B9C6CF'
PANEL      = 'F3F6F8'
CHIP = {
    'chip-high': ('F9E3DE', '7C1D10', 'C4826F'),
    'chip-med':  ('FDF3D4', '5F4700', 'C2A24A'),
    'chip-obs':  ('E3EDF6', '123F66', '7FA3C4'),
    'chip-pos':  ('E2F2E5', '175226', '74A983'),
}
FLAGRULE = {
    'flag-high': '7C1D10', 'flag-med': 'C2A24A',
    'flag-obs':  '7FA3C4', 'flag-pos': '74A983',
}
DISCLAIMER = ("AI-Generated Content from official sources. "
              "Not warranted for any use.")

TEXT_W = 10800          # 7.5in of text between 0.5in margins, in DXA
BAD_XML = re.compile(u'[\x00-\x08\x0b\x0c\x0e-\x1f￾￿]')


def esc(s):
    return html.escape(BAD_XML.sub('', s), quote=False).replace('"', '&quot;')


# ------------------------------------------------------------ file survey ----
def link_targets(doc):
    """local .html hrefs, in document order"""
    out = []
    for a in doc.iter('a'):
        h = a.get('href') or ''
        if re.match(r'^(https?:|mailto:|#)', h):
            continue
        p = h.split('#')[0]
        if p.lower().endswith('.html'):
            p = urllib.parse.unquote(p)
            if p not in out:
                out.append(p)
    return out


print('parsing HTML ...', flush=True)
os.chdir(HTMLDIR)
index_doc = LH.parse(INDEX).getroot()
order = [INDEX] + [f for f in link_targets(index_doc) if f != INDEX]
missing = [f for f in order if not os.path.exists(f)]
if missing:
    sys.exit('missing link targets: %r' % missing)

# CSBMN_SUBSET=<n> builds a small proof copy (first n sections) for QA
_sub = os.environ.get('CSBMN_SUBSET')
if _sub:
    order = order[:int(_sub)]

docs = {}
for f in order:
    docs[f] = index_doc if f == INDEX else LH.parse(f).getroot()
print('  %d sections' % len(order), flush=True)

# ------------------------------------------------------------- bookmarks ----
# bookmark name per (file, fragment). Word: <=40 chars, [A-Za-z0-9_], must not
# start with a digit.
sec_no = {f: i for i, f in enumerate(order)}
bm = {}                       # (file, frag or None) -> name
for f in order:
    tag = 'S%03d' % sec_no[f]
    bm[(f, None)] = tag
    for el in docs[f].iter():
        i = el.get('id')
        if i:
            bm[(f, i)] = (tag + '_' + re.sub(r'[^A-Za-z0-9]', '_', i))[:40]

bm_files = set(order)

# ---------------------------------------------------------- rel handling ----
rels = []                     # (rid, target, mode)
ext_rid = {}


def external(target):
    if target not in ext_rid:
        rid = 'rIdX%d' % len(ext_rid)
        ext_rid[target] = rid
        rels.append((rid, target, 'External'))
    return ext_rid[target]


def rebase(p):
    """relative non-HTML path, expressed from Output/HTML/ -> from Output/"""
    q = os.path.normpath(os.path.join('Output/HTML', urllib.parse.unquote(p)))
    return os.path.relpath(q, 'Output').replace(os.sep, '/')


def resolve(href, cur):
    """-> ('anchor', name, tip) | ('ext', rid) | None"""
    if not href:
        return None
    if href.startswith('#'):
        frag = href[1:]
        return ('anchor', bm.get((cur, frag), bm[(cur, None)]), href)
    if re.match(r'^(https?:|mailto:)', href, re.I):
        return ('ext', external(href))
    path, _, frag = href.partition('#')
    path = urllib.parse.unquote(path)
    if path.lower().endswith('.html'):
        if path in bm_files:
            name = bm.get((path, frag)) or bm[(path, None)]
            return ('anchor', name, href)
        return None
    if path in ('style.css', ''):
        return None
    return ('ext', external(rebase(path)))


# ------------------------------------------------------------ XML writing ----
_bid = [1000]


def bookmark(name):
    _bid[0] += 1
    return ('<w:bookmarkStart w:id="%d" w:name="%s"/>'
            '<w:bookmarkEnd w:id="%d"/>' % (_bid[0], esc(name), _bid[0]))


def rpr(fmt, link=False):
    p = []
    if link:
        p.append('<w:rStyle w:val="Hyperlink"/>')
    if fmt.get('code'):
        p.append('<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" '
                 'w:cs="Consolas"/>')
    if fmt.get('b'):
        p.append('<w:b/>')
    if fmt.get('i'):
        p.append('<w:i/>')
    chip = fmt.get('chip')
    if chip and chip in CHIP:
        fill, ink, _ = CHIP[chip]
        p.append('<w:b/><w:color w:val="%s"/>'
                 '<w:shd w:val="clear" w:color="auto" w:fill="%s"/>'
                 '<w:sz w:val="16"/><w:szCs w:val="16"/>' % (ink, fill))
    elif fmt.get('muted'):
        p.append('<w:color w:val="%s"/><w:sz w:val="17"/>'
                 '<w:szCs w:val="17"/>' % MUTED)
    if fmt.get('code'):
        p.append('<w:shd w:val="clear" w:color="auto" w:fill="%s"/>'
                 '<w:sz w:val="17"/><w:szCs w:val="17"/>' % PANEL)
    return '<w:rPr>%s</w:rPr>' % ''.join(p) if p else ''


def run(text, fmt, link=False):
    return ('<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>'
            % (rpr(fmt, link), esc(text)))


# ---- inline collection ------------------------------------------------------
INLINE_FMT = {'strong': 'b', 'b': 'b', 'em': 'i', 'i': 'i'}
BLOCK_IDS = {'h1', 'h2', 'h3', 'p', 'table', 'ul', 'ol', 'dl', 'article',
             'div', 'main', 'header', 'section', 'footer', 'tr', 'td', 'th'}


def collect(el, fmt, cur, out, inlink=False):
    if el.text:
        out.append(('t', el.text, fmt))
    for ch in el:
        f = dict(fmt)
        t = ch.tag if isinstance(ch.tag, str) else ''
        cls = (ch.get('class') or '').split()
        if t in INLINE_FMT:
            f[INLINE_FMT[t]] = True
        if t == 'code' or 'path' in cls:
            f['code'] = True
        if 'tag' in cls or 'cite' in cls:
            f['muted'] = True
        for c in cls:
            if c in CHIP:
                f['chip'] = c
        if ch.get('id') and (ch.tag, ch.get('id')) != (None, None):
            key = (cur, ch.get('id'))
            if key in bm and t not in BLOCK_IDS:
                out.append(('bm', bm[key], None))
        if t == 'br':
            out.append(('br', None, fmt))
        elif t == 'a' and not inlink:
            if 'skip-link' in cls:
                continue
            tgt = resolve(ch.get('href'), cur)
            inner = []
            collect(ch, f, cur, inner, inlink=True)
            if tgt:
                out.append(('ls', tgt, None))
                out.extend(inner)
                out.append(('le', None, None))
            else:
                out.extend(inner)
        else:
            collect(ch, f, cur, out, inlink)
        if ch.tail:
            out.append(('t', ch.tail, fmt))


def normalize(toks):
    """collapse HTML whitespace across the token stream"""
    res, prev_space = [], True
    for kind, val, fmt in toks:
        if kind != 't':
            res.append((kind, val, fmt))
            if kind == 'bm':
                continue
            if kind == 'br':
                prev_space = True
            continue
        s = re.sub(r'\s+', ' ', val)
        if prev_space:
            s = s.lstrip()
        if not s:
            continue
        res.append(('t', s, fmt))
        prev_space = s.endswith(' ')
    while res and res[-1][0] == 't' and not res[-1][1].strip():
        res.pop()
    if res and res[-1][0] == 't':
        k, v, f = res[-1]
        res[-1] = (k, v.rstrip(), f)
    return res


def serialize(toks):
    out, link = [], False
    for kind, val, fmt in toks:
        if kind == 't':
            out.append(run(val, fmt, link))
        elif kind == 'bm':
            out.append(bookmark(val))
        elif kind == 'br':
            out.append('<w:r><w:br/></w:r>')
        elif kind == 'ls':
            if val[0] == 'anchor':
                out.append('<w:hyperlink w:anchor="%s" w:tooltip="%s" '
                           'w:history="1">' % (esc(val[1]),
                                               esc(val[2])[:250]))
            else:
                out.append('<w:hyperlink r:id="%s" w:history="1">' % val[1])
            link = True
        elif kind == 'le':
            out.append('</w:hyperlink>')
            link = False
    if link:
        out.append('</w:hyperlink>')
    return ''.join(out)


def inline(el, cur, base=None):
    toks = []
    collect(el, dict(base or {}), cur, toks)
    return serialize(normalize(toks))


def para(content, style=None, extra='', pre=''):
    ppr = ''
    if style or extra:
        ppr = '<w:pPr>%s%s</w:pPr>' % (
            '<w:pStyle w:val="%s"/>' % style if style else '', extra)
    return '<w:p>%s%s%s</w:p>' % (ppr, pre, content)


FLAG_BORDER = ('<w:pBdr><w:left w:val="single" w:sz="24" w:space="6" '
               'w:color="%s"/></w:pBdr><w:ind w:left="170"/>')


# ------------------------------------------------------------------ tables ---
def cellw(tbl):
    """data-driven column widths summing to TEXT_W"""
    rows = list(tbl.iter('tr'))
    ncol = 0
    for r in rows:
        n = sum(int(c.get('colspan') or 1) for c in r)
        ncol = max(ncol, n)
    if ncol == 0:
        return []
    acc = [0.0] * ncol
    cnt = [0] * ncol
    for r in rows:
        i = 0
        for c in r:
            span = int(c.get('colspan') or 1)
            if span == 1 and i < ncol:
                acc[i] += len(c.text_content().strip())
                cnt[i] += 1
            i += span
    w = []
    for i in range(ncol):
        avg = acc[i] / cnt[i] if cnt[i] else 8.0
        w.append(max(4.0, min(avg, 200.0)) ** 0.60)
    tot = sum(w)
    out = [max(760, int(TEXT_W * x / tot)) for x in w]
    out[out.index(max(out))] += TEXT_W - sum(out)
    return out


def table(tbl, cur):
    widths = cellw(tbl)
    if not widths:
        return ''
    o = []
    cap = tbl.find('caption')
    if cap is not None:
        o.append(para(inline(cap, cur), 'Caption'))
    grid = ''.join('<w:gridCol w:w="%d"/>' % w for w in widths)
    o.append('<w:tbl><w:tblPr><w:tblStyle w:val="GTPTable"/>'
             '<w:tblW w:w="%d" w:type="dxa"/>'
             '<w:tblLayout w:type="fixed"/>'
             '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" '
             'w:firstColumn="0" w:lastColumn="0" w:noHBand="0" '
             'w:noVBand="1"/></w:tblPr><w:tblGrid>%s</w:tblGrid>'
             % (TEXT_W, grid))
    body_i = 0
    for tr in tbl.iter('tr'):
        head = tr.getparent().tag == 'thead'
        if not head:
            body_i += 1
        shade = ACCENT_INK if head else (PANEL if body_i % 2 == 0 else None)
        o.append('<w:tr><w:trPr>%s</w:trPr>'
                 % ('<w:cantSplit/><w:tblHeader/>' if head else ''))
        rowbm = bookmark(bm[(cur, tr.get('id'))]) if tr.get('id') else ''
        col = 0
        for c in tr:
            span = int(c.get('colspan') or 1)
            w = sum(widths[col:col + span]) or 760
            col += span
            hdrcell = head or c.tag == 'th'
            fill = PANEL if (c.tag == 'th' and not head) else shade
            tcpr = ['<w:tcW w:w="%d" w:type="dxa"/>' % w]
            if span > 1:
                tcpr.append('<w:gridSpan w:val="%d"/>' % span)
            if fill:
                tcpr.append('<w:shd w:val="clear" w:color="auto" '
                            'w:fill="%s"/>' % fill)
            tcpr.append('<w:tcMar><w:top w:w="28" w:type="dxa"/>'
                        '<w:bottom w:w="28" w:type="dxa"/>'
                        '<w:left w:w="72" w:type="dxa"/>'
                        '<w:right w:w="72" w:type="dxa"/></w:tcMar>')
            base = {'b': True} if hdrcell else {}
            body = inline(c, cur, base)
            style = 'TableHead' if head else 'TableCell'
            cellbm = ''
            if c.get('id'):
                cellbm += bookmark(bm[(cur, c.get('id'))])
            if rowbm:
                cellbm, rowbm = rowbm + cellbm, ''
            o.append('<w:tc><w:tcPr>%s</w:tcPr>%s</w:tc>'
                     % (''.join(tcpr), para(body, style, pre=cellbm)))
        o.append('</w:tr>')
    o.append('</w:tbl>')
    o.append(para('', 'AfterTable'))
    return ''.join(o)


# ------------------------------------------------------------ block walker ---
def blocks(el, cur, out, flagcolor=None):
    for ch in el:
        t = ch.tag if isinstance(ch.tag, str) else None
        if t is None or t in ('script', 'style', 'caption'):
            continue
        cls = (ch.get('class') or '').split()
        anchor = bookmark(bm[(cur, ch.get('id'))]) if ch.get('id') else ''
        if t in ('header', 'main', 'div', 'section'):
            if anchor:
                out.append(para('', 'Anchor', '', anchor))
            blocks(ch, cur, out, flagcolor)
        elif t == 'article':
            col = None
            for c in cls:
                if c in FLAGRULE:
                    col = FLAGRULE[c]
            if anchor:
                out.append(para('', 'Anchor', '', anchor))
            blocks(ch, cur, out, col)
        elif t == 'footer':
            out.append(para('', 'HRule'))
            if anchor:
                out.append(para('', 'Anchor', '', anchor))
            blocks(ch, cur, out, flagcolor)
        elif t == 'h1':
            out.append(para(inline(ch, cur), 'Heading1',
                            pre=bookmark(bm[(cur, None)]) + anchor))
        elif t in ('h2', 'h3'):
            style = 'Heading2' if t == 'h2' else 'Heading3'
            extra = FLAG_BORDER % flagcolor if flagcolor else ''
            out.append(para(inline(ch, cur), style, extra, anchor))
        elif t == 'p':
            parent_cls = (el.get('class') or '')
            style = ('Subtitle' if 'subtitle' in cls else
                     'Cite' if 'cite' in cls else
                     'Tagline' if 'tag' in cls else
                     'FootNote' if 'pagefoot' in parent_cls else 'Body')
            extra = FLAG_BORDER % flagcolor if flagcolor else ''
            body = inline(ch, cur)
            if body or anchor:
                out.append(para(body, style, extra, anchor))
        elif t in ('ul', 'ol'):
            if anchor:
                out.append(para('', 'Anchor', '', anchor))
            for li in ch.findall('li'):
                extra = ('<w:numPr><w:ilvl w:val="0"/>'
                         '<w:numId w:val="%d"/></w:numPr>'
                         % (2 if t == 'ol' else 1))
                if flagcolor:
                    extra += FLAG_BORDER % flagcolor
                out.append(para(inline(li, cur), 'ListItem', extra))
        elif t == 'dl':
            if anchor:
                out.append(para('', 'Anchor', '', anchor))
            for d in ch.iter('div'):
                dt, dd = d.find('dt'), d.find('dd')
                if dt is None:
                    continue
                term = inline(dt, cur, {'b': True})
                val = inline(dd, cur) if dd is not None else ''
                out.append(para(term + run(' ', {}) + val, 'Fact'))
        elif t == 'table':
            if anchor:
                out.append(para('', 'Anchor', '', anchor))
            out.append(table(ch, cur))
        elif t == 'hr':
            out.append(para('', 'HRule'))
        elif t == 'a' and 'skip-link' in cls:
            continue
        else:
            blocks(ch, cur, out, flagcolor)


# -------------------------------------------------------------- assemble -----
print('rendering sections ...', flush=True)
body = []
today = datetime.date.today().isoformat()
NEWEST, OLDEST = '20260819', '20230201'

body.append(para(run('Claremont School Board Meeting Navigator', {}), 'Title'))
body.append(para(run('The complete printed archive: the navigator index, the '
                     'Data Quality Report, and all %d meeting pages, '
                     'February 1, 2023 – August 19, 2026'
                     % (len(order) - 2), {}), 'Subtitle'))
body.append(para(run('An experimental service of the Claremont Community '
                     'Media Center. Compiled from the Output/HTML edition on '
                     '%s. Every cross-reference that was a hyperlink to '
                     'another page in the web edition is an internal bookmark '
                     'link here: follow it with Ctrl+Click (⌘+Click on '
                     'macOS) and come back with Alt+←. Links to outside '
                     'sources — the Cablecast recordings, the district’s '
                     'Google Drive folders, and the statutes cited in the '
                     'flags — remain live web links.' % today, {}), 'Body'))
body.append(para(run('Contents', {}), 'Heading2'))
body.append('<w:p><w:pPr><w:pStyle w:val="Body"/></w:pPr>'
            '<w:r><w:fldChar w:fldCharType="begin" w:dirty="1"/></w:r>'
            '<w:r><w:instrText xml:space="preserve"> TOC \\o "1-1" \\h \\z \\u '
            '</w:instrText></w:r>'
            '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
            '<w:r><w:t xml:space="preserve">Right-click here and choose '
            '&quot;Update Field&quot; to build the table of contents.'
            '</w:t></w:r>'
            '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>')

for n, f in enumerate(order, 1):
    if n == 1 or n % 20 == 0 or n == len(order):
        print('  [%3d/%d] %s' % (n, len(order), f), flush=True)
    blocks(docs[f].find('body'), f, body)

print('serialising document.xml ...', flush=True)
sectpr = ('<w:sectPr><w:footerReference w:type="default" r:id="rIdFtr"/>'
          '<w:pgSz w:w="12240" w:h="15840"/>'
          '<w:pgMar w:top="720" w:right="720" w:bottom="864" w:left="720" '
          'w:header="360" w:footer="288" w:gutter="0"/>'
          '<w:docGrid w:linePitch="360"/></w:sectPr>')
document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<w:document '
            'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            '<w:body>' + ''.join(body) + sectpr + '</w:body></w:document>')


# -------------------------------------------------------------- packaging ---
def style(sid, name, based, ppr, rpr_):
    return ('<w:style w:type="paragraph" w:styleId="%s">'
            '<w:name w:val="%s"/><w:basedOn w:val="%s"/>'
            '<w:qFormat/><w:pPr>%s</w:pPr><w:rPr>%s</w:rPr></w:style>'
            % (sid, name, based, ppr, rpr_))


HEAD_BDR = ('<w:pBdr><w:bottom w:val="single" w:sz="12" w:space="2" '
            'w:color="%s"/></w:pBdr>' % RULE)
STYLES = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:docDefaults><w:rPrDefault><w:rPr>'
    '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>'
    '<w:color w:val="%s"/><w:sz w:val="20"/><w:szCs w:val="20"/>'
    '<w:lang w:val="en-US" w:eastAsia="en-US" w:bidi="ar-SA"/>'
    '</w:rPr></w:rPrDefault><w:pPrDefault><w:pPr>'
    '<w:spacing w:before="0" w:after="40" w:line="228" w:lineRule="auto"/>'
    '<w:widowControl/></w:pPr></w:pPrDefault></w:docDefaults>'
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
    '<w:name w:val="Normal"/><w:qFormat/></w:style>'
    '<w:style w:type="character" w:default="1" w:styleId="DefaultParagraphFont">'
    '<w:name w:val="Default Paragraph Font"/></w:style>'
    '<w:style w:type="table" w:default="1" w:styleId="TableNormal">'
    '<w:name w:val="Normal Table"/></w:style>'
    '<w:style w:type="numbering" w:default="1" w:styleId="NoList">'
    '<w:name w:val="No List"/></w:style>'
    '<w:style w:type="character" w:styleId="Hyperlink">'
    '<w:name w:val="Hyperlink"/>'
    '<w:rPr><w:color w:val="%s"/><w:u w:val="single"/></w:rPr></w:style>'
    % (INK, ACCENT)
    + style('Title', 'Title', 'Normal',
            '<w:spacing w:before="240" w:after="80"/>',
            '<w:b/><w:color w:val="%s"/><w:sz w:val="40"/>' % ACCENT_INK)
    + style('Heading1', 'heading 1', 'Normal',
            '<w:pageBreakBefore/><w:outlineLvl w:val="0"/><w:keepNext/>'
            '<w:spacing w:before="0" w:after="60"/>',
            '<w:b/><w:color w:val="%s"/><w:sz w:val="30"/>' % ACCENT_INK)
    + style('Heading2', 'heading 2', 'Normal',
            '<w:outlineLvl w:val="1"/><w:keepNext/>'
            '<w:spacing w:before="200" w:after="60"/>' + HEAD_BDR,
            '<w:b/><w:color w:val="%s"/><w:sz w:val="24"/>' % ACCENT_INK)
    + style('Heading3', 'heading 3', 'Normal',
            '<w:outlineLvl w:val="2"/><w:keepNext/>'
            '<w:spacing w:before="120" w:after="30"/>',
            '<w:b/><w:sz w:val="21"/>')
    + style('Body', 'Body Text', 'Normal', '', '')
    + style('Anchor', 'Anchor', 'Normal',
            '<w:spacing w:before="0" w:after="0" w:line="20" '
            'w:lineRule="exact"/>', '<w:sz w:val="2"/>')
    + style('Subtitle', 'Subtitle', 'Normal',
            '<w:spacing w:after="100"/>',
            '<w:color w:val="%s"/><w:sz w:val="19"/>' % MUTED)
    + style('Fact', 'Fact', 'Normal',
            '<w:spacing w:after="20"/><w:ind w:left="220" w:hanging="220"/>',
            '<w:sz w:val="19"/>')
    + style('Caption', 'caption', 'Normal',
            '<w:spacing w:before="120" w:after="20"/><w:keepNext/>',
            '<w:b/><w:color w:val="%s"/><w:sz w:val="17"/>' % MUTED)
    + style('Cite', 'Citation', 'Normal',
            '<w:spacing w:after="60"/>',
            '<w:color w:val="%s"/><w:sz w:val="17"/>' % MUTED)
    + style('Tagline', 'Tagline', 'Normal',
            '<w:spacing w:after="40"/>',
            '<w:color w:val="%s"/><w:sz w:val="17"/>' % MUTED)
    + style('FootNote', 'Page Note', 'Normal',
            '<w:spacing w:before="80" w:after="40"/>',
            '<w:color w:val="%s"/><w:sz w:val="17"/>' % MUTED)
    + style('ListItem', 'List Bullet', 'Normal',
            '<w:spacing w:after="10"/><w:contextualSpacing/>', '')
    + style('TableCell', 'Table Cell', 'Normal',
            '<w:spacing w:before="10" w:after="10" w:line="216" '
            'w:lineRule="auto"/>', '<w:sz w:val="18"/>')
    + style('TableHead', 'Table Head', 'Normal',
            '<w:spacing w:before="10" w:after="10" w:line="216" '
            'w:lineRule="auto"/><w:keepNext/>',
            '<w:b/><w:color w:val="FFFFFF"/><w:sz w:val="18"/>')
    + style('AfterTable', 'After Table', 'Normal',
            '<w:spacing w:before="0" w:after="0" w:line="40" '
            'w:lineRule="exact"/>', '<w:sz w:val="4"/>')
    + style('HRule', 'Horizontal Rule', 'Normal',
            '<w:spacing w:before="120" w:after="60" w:line="40" '
            'w:lineRule="exact"/><w:pBdr><w:top w:val="single" w:sz="8" '
            'w:space="1" w:color="%s"/></w:pBdr>' % RULE, '<w:sz w:val="4"/>')
    + style('FooterText', 'footer', 'Normal',
            '<w:spacing w:before="0" w:after="0"/><w:jc w:val="center"/>'
            '<w:pBdr><w:top w:val="single" w:sz="8" w:space="3" '
            'w:color="%s"/></w:pBdr>' % RULE, '<w:b/><w:sz w:val="15"/>')
    + ''.join('<w:style w:type="paragraph" w:styleId="TOC%d">'
              '<w:name w:val="toc %d"/><w:basedOn w:val="Normal"/>'
              '<w:pPr><w:spacing w:after="0"/>'
              '<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="10800"/>'
              '</w:tabs><w:ind w:left="%d"/></w:pPr></w:style>'
              % (i, i, (i - 1) * 220) for i in (1, 2, 3))
    + '<w:style w:type="table" w:styleId="GTPTable">'
      '<w:name w:val="GTP Table"/><w:basedOn w:val="TableNormal"/>'
      '<w:tblPr><w:tblBorders>'
    + ''.join('<w:%s w:val="single" w:sz="4" w:space="0" w:color="%s"/>'
              % (e, RULE) for e in ('top', 'left', 'bottom', 'right',
                                    'insideH', 'insideV'))
    + '</w:tblBorders></w:tblPr></w:style></w:styles>')

NUMBERING = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:abstractNum w:abstractNumId="1">'
    '<w:multiLevelType w:val="hybridMultilevel"/>'
    + ''.join('<w:lvl w:ilvl="%d"><w:start w:val="1"/>'
              '<w:numFmt w:val="bullet"/><w:lvlText w:val="%s"/>'
              '<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="%d" '
              'w:hanging="200"/></w:pPr><w:rPr><w:rFonts w:ascii="Symbol" '
              'w:hAnsi="Symbol" w:hint="default"/></w:rPr></w:lvl>'
              % (i, ('', 'o', '')[i % 3], 260 + 260 * i)
              for i in range(9))
    + '</w:abstractNum>'
      '<w:abstractNum w:abstractNumId="2">'
      '<w:multiLevelType w:val="hybridMultilevel"/>'
    + ''.join('<w:lvl w:ilvl="%d"><w:start w:val="1"/>'
              '<w:numFmt w:val="decimal"/><w:lvlText w:val="%%%d."/>'
              '<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="%d" '
              'w:hanging="240"/></w:pPr></w:lvl>' % (i, i + 1, 260 + 260 * i)
              for i in range(9))
    + '</w:abstractNum>'
      '<w:num w:numId="1"><w:abstractNumId w:val="1"/></w:num>'
      '<w:num w:numId="2"><w:abstractNumId w:val="2"/></w:num>'
      '</w:numbering>')

FOOTER = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:p><w:pPr><w:pStyle w:val="FooterText"/></w:pPr>'
    '<w:r><w:t xml:space="preserve">%s</w:t></w:r></w:p>'
    '<w:p><w:pPr><w:jc w:val="center"/>'
    '<w:spacing w:before="20" w:after="0"/></w:pPr>'
    '<w:r><w:rPr><w:color w:val="%s"/><w:sz w:val="15"/></w:rPr>'
    '<w:t xml:space="preserve">Page </w:t></w:r>'
    '<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
    '<w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
    '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
    '<w:r><w:t>1</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r>'
    '<w:r><w:rPr><w:color w:val="%s"/><w:sz w:val="15"/></w:rPr>'
    '<w:t xml:space="preserve"> of </w:t></w:r>'
    '<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
    '<w:r><w:instrText xml:space="preserve"> NUMPAGES </w:instrText></w:r>'
    '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
    '<w:r><w:t>1</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r>'
    '</w:p></w:ftr>' % (esc(DISCLAIMER), MUTED, MUTED))

SETTINGS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:zoom w:percent="100"/><w:defaultTabStop w:val="720"/>'
    '<w:updateFields w:val="true"/><w:themeFontLang w:val="en-US"/>'
    '<w:compat><w:compatSetting w:name="compatibilityMode" '
    'w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat>'
    '</w:settings>')

CORE = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<cp:coreProperties '
    'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
    'xmlns:dc="http://purl.org/dc/elements/1.1/" '
    'xmlns:dcterms="http://purl.org/dc/terms/" '
    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
    '<dc:title>Claremont School Board Meeting Navigator — complete '
    'archive, February 1, 2023 to August 19, 2026</dc:title>'
    '<dc:subject>Claremont School Board, SAU 6 Board and Finance Committee '
    'public meetings: video, agenda, packet and minutes</dc:subject>'
    '<dc:creator>Claremont Community Media Center — Government '
    'Transparency Project</dc:creator>'
    '<dc:language>en-US</dc:language>'
    '<cp:keywords>Claremont; SAU 6; school board; RSA 91-A; public meetings'
    '</cp:keywords><dc:description>%s</dc:description>'
    '<dcterms:created xsi:type="dcterms:W3CDTF">%sT00:00:00Z</dcterms:created>'
    '<dcterms:modified xsi:type="dcterms:W3CDTF">%sT00:00:00Z'
    '</dcterms:modified></cp:coreProperties>'
    % (esc(DISCLAIMER), today, today))

APP = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
       '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/'
       '2006/extended-properties">'
       '<Application>Government Transparency Project</Application>'
       '<Company>Claremont Community Media Center</Company></Properties>')

CT = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
      '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
      '<Default Extension="rels" ContentType="application/vnd.openxmlformats-'
      'package.relationships+xml"/>'
      '<Default Extension="xml" ContentType="application/xml"/>'
      + ''.join('<Override PartName="/word/%s.xml" ContentType="application/'
                'vnd.openxmlformats-officedocument.wordprocessingml.%s+xml"/>'
                % (p, c) for p, c in (('document', 'document.main'),
                                      ('styles', 'styles'),
                                      ('settings', 'settings'),
                                      ('numbering', 'numbering'),
                                      ('footer1', 'footer')))
      + '<Override PartName="/docProps/core.xml" ContentType="application/vnd.'
        'openxmlformats-package.core-properties+xml"/>'
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.'
        'openxmlformats-officedocument.extended-properties+xml"/></Types>')

RELS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/'
        'relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/'
        'officeDocument/2006/relationships/officeDocument" '
        'Target="word/document.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/'
        'package/2006/relationships/metadata/core-properties" '
        'Target="docProps/core.xml"/>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/'
        'officeDocument/2006/relationships/extended-properties" '
        'Target="docProps/app.xml"/></Relationships>')

B = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/'
docrels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
           '<Relationships xmlns="http://schemas.openxmlformats.org/package/'
           '2006/relationships">']
for rid, typ, tgt in (('rIdSty', 'styles', 'styles.xml'),
                      ('rIdSet', 'settings', 'settings.xml'),
                      ('rIdNum', 'numbering', 'numbering.xml'),
                      ('rIdFtr', 'footer', 'footer1.xml')):
    docrels.append('<Relationship Id="%s" Type="%s%s" Target="%s"/>'
                   % (rid, B, typ, tgt))
for rid, target, mode in rels:
    docrels.append('<Relationship Id="%s" Type="%shyperlink" Target="%s" '
                   'TargetMode="External"/>' % (rid, B, esc(target)))
docrels.append('</Relationships>')

out_path = os.path.join(OUTDIR, 'CSBMN-%s-%s.DOCX' % (NEWEST, OLDEST))
if _sub:
    out_path = os.environ.get('CSBMN_OUT', '/tmp/CSBMN-sample.docx')
print('writing %s\n  document.xml %.1f MB, %d bookmarks, %d external links'
      % (out_path, len(document) / 1e6, len(bm), len(rels)), flush=True)
tmp = out_path + '.tmp'
with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    z.writestr('[Content_Types].xml', CT)
    z.writestr('_rels/.rels', RELS)
    z.writestr('docProps/core.xml', CORE)
    z.writestr('docProps/app.xml', APP)
    z.writestr('word/document.xml', document)
    z.writestr('word/_rels/document.xml.rels', ''.join(docrels))
    z.writestr('word/styles.xml', STYLES)
    z.writestr('word/settings.xml', SETTINGS)
    z.writestr('word/numbering.xml', NUMBERING)
    z.writestr('word/footer1.xml', FOOTER)
os.replace(tmp, out_path)
print('done: %.1f MB' % (os.path.getsize(out_path) / 1e6), flush=True)
