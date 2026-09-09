#!/usr/bin/env python3
"""Apply the Fix-marked AI-cadence rewrites (artifact "Built for Wonder Cadence
Pass", Chris's marks read 2026-09-09) to Built-for-Wonder.docx.

Inputs (scratchpad): packets.json (one entry per manuscript paragraph with the
flagged spans) and out/chunk-*.json (the replacement text per span).

  python3 apply_cadence_fixes_20260909.py --dry-run [--identity]   # report only
  python3 apply_cadence_fixes_20260909.py --apply                   # patch DOCX

--identity uses the original span text as its own replacement, to validate the
DOCX mapping before the real replacements exist.

Matching is paragraph-level: the manuscript line (from extract_manuscript.py) is
located as a substring of exactly one DOCX paragraph (python-docx, body + table
cells); duplicates are disambiguated by document order. Each span is then
replaced run-aware (same algorithm as apply-editor-edits.py / apply_audit_fixes):
single-run spans keep their formatting, multi-run spans with uniform formatting
collapse into the first run, mixed-format spans are reported for manual work.
"""
import json, sys, os, re, glob, shutil, collections
from pathlib import Path
from docx import Document

ROOT = Path(__file__).parent
DOCX = ROOT / 'Built-for-Wonder.docx'
S = Path(sys.argv[sys.argv.index('--scratch') + 1]) if '--scratch' in sys.argv else Path(
    '/private/tmp/claude-501/-Users-chrismichael/3e92f5c8-685f-434d-bd7c-e8019d3e8b3b/scratchpad')
IDENTITY = '--identity' in sys.argv
APPLY = '--apply' in sys.argv


def all_paragraphs(doc):
    ps = list(doc.paragraphs)
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                ps.extend(cell.paragraphs)
    return ps


def ptext(p):
    return ''.join(r.text or '' for r in p.runs)


def run_fmt(r):
    return (bool(r.bold), bool(r.italic), bool(r.underline))


def replace_at(p, idx, old_len, new, commit):
    """Replace paragraph text [idx, idx+old_len) with new, run-aware, at an exact
    character offset (no substring search). Trims the common prefix/suffix first
    so only the characters that actually change are touched; that keeps bold
    labels and italic script lines intact when the edit is elsewhere in the span."""
    runs = p.runs
    joined = ''.join(r.text or '' for r in runs)
    old = joined[idx:idx + old_len]
    # trim common prefix / suffix
    pre = 0
    while pre < len(old) and pre < len(new) and old[pre] == new[pre]: pre += 1
    suf = 0
    while suf < len(old) - pre and suf < len(new) - pre and old[-1 - suf] == new[-1 - suf]: suf += 1
    idx2 = idx + pre; old2 = old[pre:len(old) - suf]; new2 = new[pre:len(new) - suf]
    if old2 == '' and new2 == '':
        return 'identical'
    end = idx2 + len(old2)
    pos = 0; start_run = end_run = None; ls = le = None
    for ri, r in enumerate(runs):
        rt = r.text or ''; rs, re_ = pos, pos + len(rt)
        if start_run is None and rs <= idx2 < re_: start_run, ls = ri, idx2 - rs
        if old2 == '' and start_run is None and rs <= idx2 <= re_ and rt: start_run, ls = ri, idx2 - rs
        if rs < end <= re_: end_run, le = ri, end - rs
        pos = re_
    if old2 == '':
        # pure insertion: put it at the boundary inside the run that owns idx2
        if start_run is None:
            return 'run-span'
        end_run, le = start_run, ls
    if start_run is None or end_run is None:
        return 'run-span'
    if start_run == end_run:
        if commit:
            r = runs[start_run]; r.text = r.text[:ls] + new2 + r.text[le:]
        return 'single-run'
    fmts = {run_fmt(runs[ri]) for ri in range(start_run, end_run + 1)}
    if len(fmts) > 1:
        return rebuild_mixed(p, runs, start_run, ls, end_run, le, new2, commit)
    if commit:
        prefix = (runs[start_run].text or '')[:ls]; suffix = (runs[end_run].text or '')[le:]
        runs[start_run].text = prefix + new2 + suffix
        for ri in range(start_run + 1, end_run + 1): runs[ri].text = ''
    return 'collapsed'


def _make_run(template_r, text):
    from copy import deepcopy
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    el = deepcopy(template_r._r)
    for child in list(el):
        if child.tag != qn('w:rPr'):
            el.remove(child)
    t = OxmlElement('w:t'); t.text = text; t.set(qn('xml:space'), 'preserve'); el.append(t)
    return el


def rebuild_mixed(p, runs, start_run, ls, end_run, le, new2, commit):
    """The changed region crosses runs with different formatting (usually a bold
    key term inside plain text). Rebuild the region: plain text takes the
    formatting of the region's first plain run; every formatted segment whose
    text survives verbatim in the new text is re-emitted with its own run
    formatting, so bold terms and italic quotes keep their look."""
    segs = []  # (fmt, text, run)
    for ri in range(start_run, end_run + 1):
        rt = runs[ri].text or ''
        a = ls if ri == start_run else 0
        b = le if ri == end_run else len(rt)
        if b > a: segs.append((run_fmt(runs[ri]), rt[a:b], runs[ri]))
    plain = [r for f, t, r in segs if f == (False, False, False)]
    if not plain:
        return 'mixed-fmt-noplain'
    plain_run = plain[0]
    formatted = [(t, r) for f, t, r in segs if f != (False, False, False) and t.strip()]
    # split new2 into pieces: formatted segment text (if present) keeps its run formatting
    pieces = [(new2, plain_run)]
    for t, r in sorted(formatted, key=lambda x: -len(x[0])):
        out = []
        for text, tmpl in pieces:
            if tmpl is not plain_run or t not in text:
                out.append((text, tmpl)); continue
            i = text.find(t)
            if i: out.append((text[:i], plain_run))
            out.append((t, r))
            if text[i + len(t):]: out.append((text[i + len(t):], plain_run))
        pieces = out
    kept = sum(1 for _, r in pieces if r is not plain_run)
    if not commit:
        return 'mixed-rebuilt' if kept else 'mixed-flattened'
    prefix = (runs[start_run].text or '')[:ls]; suffix = (runs[end_run].text or '')[le:]
    anchor = runs[start_run]._r
    for text, tmpl in pieces:
        el = _make_run(tmpl, text); anchor.addnext(el); anchor = el
    runs[start_run].text = prefix
    for ri in range(start_run + 1, end_run + 1): runs[ri].text = ''
    if end_run != start_run: runs[end_run].text = suffix
    else: runs[start_run].text = prefix  # unreachable (mixed implies >1 run)
    if end_run == start_run: pass
    # suffix handling when end_run == start_run is impossible here; when different, suffix set above
    return 'mixed-rebuilt' if kept else 'mixed-flattened'


def tidy_gap(text, start, end, rep):
    """Apply rep at [start,end) and clean double spaces / space-before-period left by a cut."""
    new = text[:start] + rep + text[end:]
    if rep == '':
        left = text[:start]; right = text[end:]
        if left.endswith(' ') and (right.startswith(' ') or right == ''):
            new = left[:-1] + right
        elif left.endswith(' ') and right.startswith(('.', ',')):
            new = left[:-1] + right
    return new


def main():
    packets = json.load(open(S / 'packets.json', encoding='utf-8'))
    reps = {}
    for f in sorted(glob.glob(str(S / 'out' / 'chunk-*.json'))):
        for o in json.load(open(f, encoding='utf-8')):
            reps[(o['line'], o['start'], o['end'])] = o
    doc = Document(str(DOCX))
    paras = all_paragraphs(doc)
    texts = [ptext(p) for p in paras]
    stats = collections.Counter(); report = []
    predicted = {}   # manuscript line -> new paragraph text
    # document-order rank for duplicates
    lines_sorted = sorted(packets, key=lambda p: p['line'])
    for pk in lines_sorted:
        ln = pk['line']; old_par = pk['paragraph']
        hits = [i for i, t in enumerate(texts) if old_par in t]
        if not hits:
            stats['para-not-in-docx'] += 1; report.append((ln, 'PARA NOT IN DOCX', old_par[:80])); continue
        if len(hits) > 1:
            # rank of this manuscript line among manuscript occurrences of the same text
            ms = [q['line'] for q in packets if q['paragraph'] == old_par]
            # occurrences in the manuscript file itself
            allms = [i + 1 for i, l in enumerate(open(ROOT / 'manuscript-extracted.txt', encoding='utf-8').read().split('\n')) if old_par in l]
            rank = allms.index(ln) if ln in allms else 0
            hi = hits[min(rank, len(hits) - 1)]
            report.append((ln, 'DUP resolved by rank', f'rank {rank} -> docx para {hi}'))
        else:
            hi = hits[0]
        p = paras[hi]
        base = texts[hi].find(old_par)
        new_par = old_par
        spans = sorted(pk['spans'], key=lambda m: -m['start'])
        for m in spans:
            key = (ln, m['start'], m['end'])
            if IDENTITY: rep = m['span_text']
            elif key in reps: rep = reps[key]['replacement']
            else:
                stats['no-replacement'] += 1; report.append((ln, 'NO REPLACEMENT', m['span_text'][:60])); continue
            if '—' in rep or '–' in rep or '!' in rep:
                stats['bad-chars'] += 1; report.append((ln, 'DASH/BANG IN REPLACEMENT', rep[:80]))
            status = replace_at(p, base + m['start'], m['end'] - m['start'], rep, commit=APPLY)
            stats[status] += 1
            if status not in ('single-run', 'collapsed', 'identical', 'mixed-rebuilt', 'mixed-flattened'):
                report.append((ln, status.upper(), m['span_text'][:80]))
            else:
                new_par = tidy_gap(new_par, m['start'], m['end'], rep)
        if APPLY and new_par != ptext(p):
            # tidy spacing in the DOCX to match prediction when a cut left a double space
            cur = ptext(p)
            if re.sub(r'\s+', ' ', cur).strip() == re.sub(r'\s+', ' ', new_par).strip() and cur != new_par:
                # collapse whitespace differences inside the runs: rewrite runs text conservatively
                for r in p.runs:
                    r.text = re.sub(r'  +', ' ', r.text).replace(' .', '.').replace(' ,', ',')
        predicted[ln] = new_par
        if APPLY and old_par.strip() and not ptext(p).strip() and texts[hi].strip() == old_par.strip():
            p._p.getparent().remove(p._p); stats['paragraph-deleted'] += 1
    # extra whole-line replacements (hook/key-read copies inside the DOCX that mirror build-script fixes)
    ex = S / 'extra-lines.json'
    if ex.exists():
        for e in json.load(open(ex, encoding='utf-8')):
            hits = [i for i, t in enumerate(texts) if t.strip() == e['old'].strip()] or [i for i, t in enumerate(texts) if e['old'] in t]
            if len(hits) != 1:
                stats['extra-ambiguous'] += 1; report.append((e.get('line'), f'EXTRA hits={len(hits)}', e['old'][:60])); continue
            p = paras[hits[0]]; base = texts[hits[0]].find(e['old'])
            status = replace_at(p, base, len(e['old']), e['new'], commit=APPLY)
            stats['extra-' + status] += 1
            if status not in ('single-run', 'collapsed', 'identical', 'mixed-rebuilt', 'mixed-flattened'): report.append((e.get('line'), 'EXTRA ' + status.upper(), e['old'][:60]))
            else: predicted[e.get('line', 0)] = e['new']
    print('stats:', dict(stats))
    for r in report[:80]: print('  ', r)
    if len(report) > 80: print(f'   ... {len(report) - 80} more')
    json.dump(predicted, open(S / 'predicted-lines.json', 'w'), indent=1, ensure_ascii=False)
    if APPLY:
        bk = ROOT / 'backups' / 'Built-for-Wonder.pre-cadence-fixes-2026-09-09.docx'
        if not bk.exists(): shutil.copy2(DOCX, bk); print('backup ->', bk)
        doc.save(str(DOCX)); print('saved', DOCX)


if __name__ == '__main__':
    main()
