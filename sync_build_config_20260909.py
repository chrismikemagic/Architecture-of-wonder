#!/usr/bin/env python3
"""Carry the 2026-09-09 cadence rewrites from the DOCX into build-book.py so the
three places that duplicate manuscript text stay in sync:

  1. HOOK_LINES / KEY_READS values that mirror a DOCX line that changed
  2. META_REVEAL_HTML sentences that mirror a changed DOCX Meta Reveal paragraph
  3. explicit build-script-only items (the five "line 0" findings) in extra-config.json

Usage: python3 sync_build_config_20260909.py [--apply]   (default: report only)
"""
import json, re, sys, html as H
from pathlib import Path
ROOT = Path(__file__).parent
S = Path('/private/tmp/claude-501/-Users-chrismichael/3e92f5c8-685f-434d-bd7c-e8019d3e8b3b/scratchpad')
APPLY = '--apply' in sys.argv
src = open(ROOT / 'build-book.py', encoding='utf-8').read(); orig = src
packets = {p['line']: p for p in json.load(open(S / 'packets.json', encoding='utf-8'))}
pred = {int(k): v for k, v in json.load(open(S / 'predicted-lines.json', encoding='utf-8')).items()}
reps = {}
import glob
for f in sorted(glob.glob(str(S / 'out' / 'chunk-*.json'))):
    for o in json.load(open(f, encoding='utf-8')): reps[(o['line'], o['start'], o['end'])] = o['replacement']
def core(s): return s.strip().strip('"“”\'').strip()
report = []
# 1. HOOK_LINES / KEY_READS
changed = {ln: (packets[ln]['paragraph'], new) for ln, new in pred.items() if ln in packets and packets[ln]['paragraph'] != new}
# chapter of each manuscript line (from the CHAPTER N marker lines the extractor emits)
import subprocess
# packet line numbers refer to the manuscript BEFORE this pass, so read that version from git
mlines = subprocess.run(['git', 'show', 'HEAD:manuscript-extracted.txt'], capture_output=True, text=True, cwd=ROOT).stdout.split('\n')
chap_of = {}; cur = None
for i, l in enumerate(mlines):
    if re.fullmatch(r'CHAPTER \d+A?', l.strip()): cur = l.strip()
    chap_of[i + 1] = cur
for name in ('HOOK_LINES', 'KEY_READS'):
    m = re.search(name + r' = \{(.*?)\n\}', src, re.S); body = m.group(1); newbody = body
    for k, a, b in re.findall(r"'(CHAPTER [0-9A]+)':\s*(?:'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\")", body):
        val = a or b; c = core(val)
        hits = [(ln, old, new) for ln, (old, new) in changed.items() if core(old) == c and chap_of.get(ln) == k]
        if not hits: continue
        ln, old, new = hits[0]; nc = core(new)
        if nc == c: continue
        quoted = val.strip().startswith(('"', '“'))
        newval = ('"%s"' % nc) if (quoted and nc) else nc
        if a: pat = "'%s':%s'%s'" ; 
        # rebuild the literal in the same quote style as the source
        lit_old = ("'" + a + "'") if a else ('"' + b + '"')
        if a: lit_new = "'" + newval.replace("'", "\\'") + "'" if "'" not in newval or '\\' in a else '"' + newval + '"'
        else: lit_new = '"' + newval.replace('"', '\\"') + '"'
        if newval.count('"') and not quoted and a: lit_new = "'" + newval + "'"
        newbody = newbody.replace(lit_old, lit_new, 1)
        report.append((name, k, ln, c[:50], '->', nc[:70]))
    src = src.replace(body, newbody)
# 2. META_REVEAL_HTML
m = re.search(r"META_REVEAL_HTML = '''(.*?)'''", src, re.S); html_block = m.group(1); nb = html_block
for ln, p in packets.items():
    if ln < 4936: continue
    for sp in p['spans']:
        key = (ln, sp['start'], sp['end']); rep = reps.get(key)
        if rep is None: report.append(('META', ln, 'NO REPLACEMENT')); continue
        cands = [sp['span_text'], H.escape(sp['span_text'], quote=False)]
        done = False
        for c in cands:
            n = nb.count(c)
            if n == 1: nb = nb.replace(c, H.escape(rep, quote=False) if c != sp['span_text'] else rep); done = True; break
            if n > 1: report.append(('META', ln, 'MULTI in HTML', c[:60])); done = True; break
        if not done: report.append(('META', ln, 'NOT IN HTML (manual)', sp['span_text'][:70]))
        else: report.append(('META', ln, 'ok', sp['span_text'][:40], '->', rep[:50]))
src = src.replace(html_block, nb)
# 3. explicit config items
extra = json.load(open(S / 'extra-config.json', encoding='utf-8')) if (S / 'extra-config.json').exists() else []
for e in extra:
    n = src.count(e['old'])
    if n != 1: report.append(('EXTRA', e['what'], f'count={n}', e['old'][:60])); continue
    src = src.replace(e['old'], e['new']); report.append(('EXTRA', e['what'], 'ok', e['new'][:70]))
for r in report: print(' ', r)
print('build-book.py changed:', src != orig, '| chars delta', len(src) - len(orig))
if APPLY and src != orig:
    open(ROOT / 'build-book.py', 'w', encoding='utf-8').write(src); print('written build-book.py')
