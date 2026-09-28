#!/usr/bin/env python3
#
# Copyright 2026 Kevin Tyson
# SPDX-License-Identifier: Apache-2.0
#
"""Verify that every quotation on a meeting page actually appears in its dialogue CSV.

The create-html pilot (2026-08-28) found that all three agents silently "cleaned up"
ASR text while quoting it — replacing garbled tokens, smoothing grammar, once dropping
a negation. Structure validators cannot see this. For a project whose credibility rests
on quotation accuracy, this is the highest-value check there is.

    python3 verify_quotes.py "Output/HTML/<base>.HTML" "Output/HTML/Dialogue/<base>.CSV"
    python3 verify_quotes.py --corpus Output/HTML Output/HTML/Dialogue

How a quotation is matched
--------------------------
- Quoted spans are pulled from visible page text (curly or straight double quotes).
- Bracketed editorial insertions are DROPPED before matching: `[ESSER] monies` matches
  source text "monies", and `[Plodzik &] Sanderson` matches "Sanderson".
- An ellipsis (… or ...) splits a quotation into fragments; each is matched separately.
- Matching is on lowercased, punctuation-stripped, whitespace-collapsed word sequences,
  so smart quotes, hyphenation and spacing never cause a false alarm.
- Fragments under MIN_WORDS words are skipped — too short to be evidence either way.

Exit 1 if any fragment is not found. A miss is not automatically an error: the quotation
may come from the minutes or the agenda rather than the recording. The report says which
fragments failed so a human can confirm the source, and the page should attribute
non-transcript quotations explicitly.
"""
import argparse, csv, glob, os, re, sys, unicodedata

MIN_WORDS = 4

BLOCK = ('td','th','tr','p','li','h1','h2','h3','h4','h5','h6','div',
         'article','section','dd','dt','dl','table','caption','header','footer')

def visible_text(html):
    """Return page text with BLOCK boundaries marked, so a quotation can never
    be matched across two cells. Before this, an opening quote in one <td> and a
    closing quote three cells later produced a bogus 100-word 'quotation'."""
    html = re.sub(r'(?is)<(script|style)\b.*?</\1>', ' ', html)
    html = re.sub(r'(?s)<!--.*?-->', ' ', html)
    html = re.sub(r'(?i)<br\s*/?>', '\n\n', html)
    html = re.sub(r'(?i)</?(?:%s)\b[^>]*>' % '|'.join(BLOCK), '\n\n', html)
    html = re.sub(r'(?s)<[^>]+>', ' ', html)
    for ent, ch in (('&hellip;','…'),('&lsquo;','‘'),('&rsquo;','’'),
                    ('&ldquo;','“'),('&rdquo;','”'),('&amp;','&'),('&lt;','<'),
                    ('&gt;','>'),('&quot;','"'),('&#39;',"'"),('&nbsp;',' '),
                    ('&mdash;','—'),('&ndash;','–')):
        html = html.replace(ent, ch)
    return html

def norm(s, brackets='drop'):
    """Normalize for matching.

    Brackets are ambiguous in this corpus and both readings occur:
      drop  — `[ESSER] monies` / `[Plodzik &] Sanderson`: the bracket is a whole
              inserted word, and the source says only what is outside it.
      keep  — `PBI[S]`, `board[s]`: the bracket completes a word the ASR clipped,
              and the source word includes it.
    A fragment counts as found if EITHER reading matches; checking only one
    produced false alarms on every word-completion bracket."""
    s = unicodedata.normalize('NFKD', s)
    s = s.replace('’', "'").replace('‘', "'")
    if brackets == 'drop':
        s = re.sub(r'\[[^\]]*\]', ' ', s)
    else:
        s = s.replace('[', '').replace(']', '')
    s = re.sub(r"[^a-z0-9' ]+", ' ', s.lower())
    s = ' '.join(s.split())
    # Collapse immediate word repetitions ("we have a, a line" -> "we have a line").
    # Condensing a stutter is a legitimate, meaning-preserving edit that the project
    # allows unmarked; without this the verifier flags every honest quotation of
    # spontaneous speech and stops being read. Repetition is collapsed on BOTH sides,
    # so a page that keeps the stutter still matches a source that has it.
    prev = None
    while s != prev:
        prev = s
        s = re.sub(r'\b(\w+)( \1\b)+', r'\1', s)
    return s

def quotations(text):
    """Quotations, matched within a single block only."""
    out = []
    for block in text.split('\n\n'):
        # Collapse the block's own line wrapping first: a long quotation is
        # routinely broken across source lines, and forbidding newlines inside
        # the match silently dropped exactly the longest, most load-bearing quotes.
        block = ' '.join(block.split())
        for m in re.finditer(r'[“"]([^”"]{8,600})[”"]', block):
            out.append(m.group(1))
    return out

def fragments(q):
    for part in re.split(r'…|\.\.\.', q):
        a, b = norm(part, 'drop'), norm(part, 'keep')
        if len(a.split()) >= MIN_WORDS:
            yield part.strip(), (a, b)

def csv_corpus(path):
    rows = []
    with open(path, encoding='utf-8-sig') as f:
        for r in csv.reader(f):
            if len(r) >= 7:
                rows.append(r[6])
    return norm(' '.join(rows))

def check(page, csvpath, quiet=False, cap=None):
    corpus = csv_corpus(csvpath)
    text = visible_text(open(page, encoding='utf-8').read())
    total = miss = 0
    misses = []
    for q in quotations(text):
        for raw, n in fragments(q):
            total += 1
            if not any(v in corpus for v in n):
                miss += 1
                misses.append(raw)
    name = os.path.basename(page)
    if miss:
        print(f"REVIEW {name}: {miss} of {total} quoted fragments are not in the dialogue CSV")
        cap = miss if cap is None else cap
        for raw in misses[:cap]:
            print(f'    not in transcript: "{raw[:110]}"')
        if miss > cap:
            print(f"    ... and {miss-cap} more")
        print("    Each is EITHER a quotation from the agenda/minutes (legitimate — make sure")
        print("    the page attributes it to that document, not to the recording) OR a")
        print("    transcript quotation that was silently cleaned up (a defect — restore the")
        print("    source wording and bracket any correction).")
        return False
    if not quiet:
        print(f"OK   {name}: all {total} quoted fragments found verbatim in the dialogue CSV")
    return True

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('a'); ap.add_argument('b')
    ap.add_argument('--corpus', action='store_true')
    ap.add_argument('--strict', action='store_true',
                    help='exit non-zero on unmatched fragments (default: report only, '
                         'because agenda- and minutes-sourced quotations legitimately '
                         'do not appear in the transcript)')
    args = ap.parse_args()
    if not args.corpus:
        good = check(args.a, args.b)
        sys.exit(0 if (good or not args.strict) else 1)
    ok = bad = skip = 0
    for page in sorted(glob.glob(os.path.join(args.a, '*.HTML'))):
        base = os.path.basename(page)[:-5]
        cands = [os.path.join(args.b, base + '.CSV')]
        if base.endswith('.mp4'):
            cands.append(os.path.join(args.b, base[:-4] + '.CSV'))
        else:
            cands.append(os.path.join(args.b, base + '.mp4.CSV'))
        c = next((p for p in cands if os.path.exists(p)), None)
        if not c:
            print(f"SKIP {base}: no dialogue CSV"); skip += 1; continue
        if check(page, c, quiet=True, cap=12): ok += 1
        else: bad += 1
    print(f"\n{ok} clean, {bad} needing quotation review, {skip} skipped")
    sys.exit(1 if (bad and args.strict) else 0)

if __name__ == '__main__':
    main()
