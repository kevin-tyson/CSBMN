#!/usr/bin/env python3
#
# Copyright 2026 Kevin Tyson
# SPDX-License-Identifier: Apache-2.0
#
"""Extract Premiere Pro speech-to-text transcripts from a .prproj into the
Premiere "Export transcript" JSON format used in Input/Transcripts.

Decoding (reverse-engineered from the FlatBuffer in <TranscriptData>, checked
against existing exported JSON): document.f0 = segments, f1 = language,
f2 = speakers (f0 name, f1 uuid table of two u64). Segment: f0 start ticks,
f1 duration ticks, f2 speaker uuid, f3 words, f4 language. Word: f0 start
ticks, f1 duration ticks, f2 text, f3 confidence (float32), f4 trailing-
punctuation flag (not exported), f5 eos, f6/f7 disfluency markers (only on
empty-text words). 254016000000 ticks per second.

  python3 prproj_transcripts.py project.prproj OUTDIR [--only NAME.mp4]
"""
import argparse, base64, gzip, json, re, struct, sys, uuid

TPS = 254016000000


class FB:
    def __init__(s, b): s.b = b
    def u32(s, o): return struct.unpack_from('<I', s.b, o)[0]
    def i32(s, o): return struct.unpack_from('<i', s.b, o)[0]
    def u16(s, o): return struct.unpack_from('<H', s.b, o)[0]
    def q(s, o): return struct.unpack_from('<q', s.b, o)[0]
    def f32(s, o): return struct.unpack_from('<f', s.b, o)[0]
    def deref(s, o): return o + s.u32(o)
    def table(s, t):
        vt = t - s.i32(t); n = (s.u16(vt) - 4) // 2
        return {i: s.u16(vt + 4 + 2 * i) for i in range(n) if s.u16(vt + 4 + 2 * i)}
    def string(s, o):
        p = s.deref(o); L = s.u32(p); return s.b[p + 4:p + 4 + L].decode('utf-8')
    def vec(s, o):
        p = s.deref(o); return p + 4, s.u32(p)
    def uid(s, o):
        t = s.deref(o); fl = s.table(t)
        raw = s.b[t + fl[0]:t + fl[0] + 8] + s.b[t + fl[1]:t + fl[1] + 8]
        return str(uuid.UUID(bytes=raw))


def num(x):
    x = round(x, 2)
    return int(x) if x == int(x) else x


def decode(blob):
    F = FB(blob); doc = F.deref(F.u32(0) + 4); D = F.table(doc)
    lang = F.string(doc + D[1])
    sp, ns = F.vec(doc + D[2])
    speakers = []
    for k in range(ns):
        t = F.deref(sp + 4 * k); fl = F.table(t)
        speakers.append({"id": F.uid(t + fl[1]), "name": F.string(t + fl[0])})
    sg, nseg = F.vec(doc + D[0])
    segs = []
    for k in range(nseg):
        t = F.deref(sg + 4 * k); fl = F.table(t)
        wp, wn = F.vec(t + fl[3]); words = []
        for j in range(wn):
            w = F.deref(wp + 4 * j); wf = F.table(w)
            text = F.string(w + wf[2]) if 2 in wf else ""
            disfl = 6 in wf or 7 in wf
            if disfl and text:
                sys.exit(f"unexpected: disfluency marker on non-empty word {text!r}")
            words.append({"confidence": num(F.f32(w + wf[3])) if 3 in wf else 0,
                          "duration": num(F.q(w + wf[1]) / TPS),
                          "eos": bool(5 in wf and F.b[w + wf[5]]),
                          "start": num(F.q(w + wf[0]) / TPS),
                          "tags": ["disfluency"] if disfl else [],
                          "text": text, "type": "word"})
        segs.append({"duration": num(F.q(t + fl[1]) / TPS),
                     "language": F.string(t + fl[4]) if 4 in fl else lang,
                     "speaker": F.uid(t + fl[2]),
                     "start": num(F.q(t + fl[0]) / TPS),
                     "words": words})
    segs.sort(key=lambda s: s["start"])
    return {"language": lang, "segments": segs, "speakers": speakers}


def transcripts(xml):
    """yield (clip name, blob) for each transcript document."""
    for m in re.finditer(r'<TranscriptClip ObjectID="(\d+)".*?<TranscriptTextSegments ObjectRef="(\d+)"', xml, re.S):
        clip, docid = m.groups()
        mc = re.search(r'<MasterClip ObjectUID="([^"]+)"[^>]*>(?:(?!</MasterClip>).)*?ObjectRef="%s"' % clip, xml, re.S)
        cpi = re.search(r'<ClipProjectItem ObjectUID="[^"]+"[^>]*>(?:(?!</ClipProjectItem>).)*?<Name>([^<]*)</Name>(?:(?!</ClipProjectItem>).)*?ObjectURef="%s"' % mc.group(1), xml, re.S)
        d = re.search(r'<ExternallyProvidedTranscriptDocument ObjectID="%s".*?<TranscriptData Encoding="base64"[^>]*>([^<]+)<' % docid, xml, re.S)
        yield cpi.group(1), base64.b64decode(d.group(1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("prproj"); ap.add_argument("outdir")
    ap.add_argument("--only", action="append"); a = ap.parse_args()
    raw = open(a.prproj, "rb").read()
    xml = (gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw).decode("utf-8")
    for name, blob in transcripts(xml):
        d = decode(blob)
        nw = sum(len(s["words"]) for s in d["segments"])
        end = max(s["start"] + s["duration"] for s in d["segments"])
        print(f"{name}: {len(d['segments'])} segments, {nw} words, {len(d['speakers'])} speakers, ends {end:.0f}s")
        if a.only and name not in a.only:
            print("   (skipped)"); continue
        with open(f"{a.outdir}/{name}.json", "w", encoding="utf-8") as f:
            json.dump(d, f, separators=(",", ":"), ensure_ascii=False)
