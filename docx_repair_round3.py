"""DOCX repair #3 — 2026-06-12 full read-through fixes.

R1  Ch9: un-mash the 80-signal observation table (header + 80 single-line rows -> 5-line format)
R2  Front matter: delete the editor note paragraph
R3  Ch12: remove the four 'Designed insert' production specs; rewire prose; TELL_TABLE marker
R4  Ch13: Fruit-to-Fang flattened table + flowchart -> markers
R5  Ch17: remove flattened emoji nav/legend; feedback-signals table -> marker
R6  Ch20: delete duplicated Babel closing line
R7  Ch21: delete duplicated 'examples' paragraph; fix mashed Level headers
R8  Ch25: ZODIAC_ELEMENT_TABLE marker after 'table you need to know cold'
R9  Ch29: delete duplicated 'One concrete way to train this' paragraph; THings typo
R10 Ch32: fix 'A' + 'standing ovation's are predictable' opener
R11 Ch36: remove duplicated sentences inside introductions paragraph
R12 Ch37: remove duplicated lede (orphan F + 'our forces...')
"""
import re, zipfile, shutil
import xml.etree.ElementTree as ET

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
XMLSPACE = '{http://www.w3.org/XML/1998/namespace}space'
ET.register_namespace('w', W)
ET.register_namespace('r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')

DOCX = 'Architecture-of-Wonder.docx'
shutil.copy2(DOCX, 'backups/Architecture-of-Wonder.pre-round3-20260612.docx')

with zipfile.ZipFile(DOCX, 'r') as z:
    names = z.namelist()
    contents = {n: z.read(n) for n in names}

root = ET.fromstring(contents['word/document.xml'])
body = root.find(f'{{{W}}}body')

def ptext(p):
    return ''.join(t.text or '' for t in p.iter(f'{{{W}}}t'))

def make_para(text):
    p = ET.Element(f'{{{W}}}p')
    r = ET.SubElement(p, f'{{{W}}}r')
    t = ET.SubElement(r, f'{{{W}}}t')
    t.set(XMLSPACE, 'preserve')
    t.text = text
    return p

def set_text(p, text):
    ts = [t for t in p.iter(f'{{{W}}}t')]
    ts[0].set(XMLSPACE, 'preserve')
    ts[0].text = text
    for t in ts[1:]:
        t.text = ''

def paras():
    return [el for el in body if el.tag == f'{{{W}}}p']

def delete_by_text(exact_texts, expect):
    n = 0
    for p in paras():
        if ptext(p).strip() in exact_texts:
            body.remove(p)
            n += 1
    assert n == expect, (exact_texts[:2], 'expected', expect, 'got', n)
    return n

EM = chr(0x2014)

# ── R1: 80-signal observation table ────────────────────────────
pl = paras()
texts = [ptext(p).strip() for p in pl]
hi = texts.index('#OBSERVATIONWHAT IT TELLS YOUTIERUSE')
rows = []
boundary = re.compile('[a-z' + chr(0x201d) + chr(0x2019) + ')\\]][A-Z]')
rowre = re.compile(r'^(\d{2})(.+)(T[1-4])((?:[A-Z]{2}[/ ]?)+)$')
k = hi + 1
while k < len(texts):
    m = rowre.match(texts[k])
    if not m:
        break
    num, middle, tier, codes = m.group(1), m.group(2), m.group(3), m.group(4).strip()
    b = boundary.search(middle)
    assert b, ('no obs/what boundary in row', texts[k])
    obs = middle[:b.start() + 1]
    what = middle[b.start() + 1:]
    rows.append((num, obs, what, tier, codes))
    k += 1
assert len(rows) == 80, ('expected 80 rows, parsed', len(rows))
pos = list(body).index(pl[hi])
for p in pl[hi:k]:
    body.remove(p)
new_lines = ['#', 'OBSERVATION', 'WHAT IT TELLS YOU', 'TIER', 'USE']
for num, obs, what, tier, codes in rows:
    new_lines += [num, obs, what, tier, codes]
for off, line in enumerate(new_lines):
    body.insert(pos + off, make_para(line))
print('R1: observation table rebuilt -', len(rows), 'rows ->', len(new_lines), 'paragraphs')

# ── R2: editor note ────────────────────────────────────────────
n = 0
for p in paras():
    if ptext(p).strip().startswith('__*note to the editor'):
        body.remove(p)
        n += 1
assert n == 1, n
print('R2: editor note removed')

# ── R3: Chapter 12 ─────────────────────────────────────────────
for p in paras():
    t = ptext(p)
    if 'The five questions below are the architecture for that.' in t:
        set_text(p, t.split('The five questions below')[0]
                 + 'The Tell Table below is the architecture for that.')
        print('R3: promise line rewired')
        break

delete_by_text({
    'FIVE QUESTIONS PANEL',
    'Designed insert: five questions that map to real-time signal categories. Each question is the architectural root of a Tell Table column. To be built as a formatted panel or visual grid.',
    'Every one of those five questions has a set of signals that answers it. This is the full set.',
    'MINI SCENARIOS',
    'Designed insert: three to five short performance scenarios showing the Tell Table in action. Each scenario presents a signal cluster and the corresponding in-performance decision.',
    'The Quick-Reference Sheet',
    'If you remember nothing else, remember this page.',
    'QUICK-REFERENCE SHEET',
    'Designed one-page insert: the most essential signals condensed for at-a-glance recall. Intended as a tear-out or printable reference spread. Three signals minimum per category.',
}, 9)
print('R3: ch12 production specs removed')

# SIGNAL TABLE header + spec -> TELL_TABLE marker
pl = paras()
texts = [ptext(p).strip() for p in pl]
i_st = texts.index('SIGNAL TABLE')
assert texts[i_st + 1].startswith('Designed reference table:'), texts[i_st + 1]
pos = list(body).index(pl[i_st])
body.remove(pl[i_st]); body.remove(pl[i_st + 1])
body.insert(pos, make_para('TELL_TABLE'))
print('R3: TELL_TABLE marker placed')

for p in paras():
    if ptext(p).strip() == 'The table shows you what to look for. This is what to do when you see it.':
        set_text(p, 'The table pairs each color with the move it calls for. Green: continue building. '
                    'Yellow: reframe before you continue. Red: reset or pivot. '
                    'The colors are decisions, not decorations.')
        print('R3: in-performance read line rewired')
        break

# ── R4: Fruit to Fang table + flowchart ────────────────────────
pl = paras()
texts = [ptext(p).strip() for p in pl]
i_t = texts.index('What you observe')
assert texts[i_t + 1] == 'What it usually suggests'
i_end = texts.index('Iguana or another unusual choice')
pos = list(body).index(pl[i_t])
for p in pl[i_t:i_end + 1]:
    body.remove(p)
body.insert(pos, make_para('FRUIT_TO_FANG_TABLE'))
print('R4: fruit-to-fang table marker placed, replaced', i_end - i_t + 1, 'paras')

pl = paras()
texts = [ptext(p).strip() for p in pl]
i_f = texts.index('Think of the first vowel')
i_fe = next(i for i, t in enumerate(texts) if t.startswith('points toward U rather than I'))
assert 0 < i_fe - i_f < 40, (i_f, i_fe)
pos = list(body).index(pl[i_f])
for p in pl[i_f:i_fe + 1]:
    body.remove(p)
body.insert(pos, make_para('FRUIT_TO_FANG_FLOW'))
print('R4: fruit-to-fang flow marker placed, replaced', i_fe - i_f + 1, 'paras')

# ── R5: Ch17 emoji nav/legend + feedback signals table ─────────
EMOJI_LINES = {
    'Jump to section',
    'Appearance, Movement, Territory, Social Confidence, Cognitive Processing, Emotional Regulation',
    'Feedback Signals ' + chr(0xB7) + ' Quick Reference',
    chr(0x1F3AD) + 'Stage or crowd',
    chr(0x1F3C3) + 'Strolling',
    chr(0x1F441) + 'Close-up or baseline',
    chr(0x26A0) + chr(0xFE0F) + 'Adjust first',
    'Lip compression ' + chr(0x2192) + ' pause, then reverse the direction of the line',
    'Eyebrow flash + pause ' + chr(0x2192) + ' broaden the statement, give it more room to land',
    'Head turning away ' + chr(0x2192) + ' switch cue category entirely',
    'Smile or nod ' + chr(0x2192) + ' expand on the theme ' + EM + ' you have the thread',
    chr(0x2728) + ' Appearance',
    chr(0x1F3C3) + ' Movement and Posture',
    chr(0x1F6E1) + ' Territory and Personal Space',
    chr(0x1F441) + ' Social Confidence',
    chr(0x1F9E0) + ' Cognitive Processing',
    chr(0x2764) + chr(0xFE0F) + ' Emotional Regulation',
}
n = 0
for p in paras():
    t = ptext(p).strip()
    if t in EMOJI_LINES or t.startswith('Icons: ' + chr(0x1F3AD)):
        body.remove(p)
        n += 1
print('R5: emoji nav/legend lines removed:', n)
assert n >= 15, n

pl = paras()
texts = [ptext(p).strip() for p in pl]
i_s = texts.index('Signal Means')
assert texts[i_s + 1] == 'Adjustment' and texts[i_s + 2] == 'Pivot To'
assert texts[i_s + 3].startswith('01Lip Compression')
pos = list(body).index(pl[i_s])
for p in pl[i_s:i_s + 19]:
    body.remove(p)
body.insert(pos, make_para('FEEDBACK_SIGNALS_TABLE'))
print('R5: feedback signals table marker placed (19 paras replaced)')

# ── R6/R7: duplicates + level headers ──────────────────────────
seen = False
for p in paras():
    if ptext(p).strip() == 'Influence and counting. That is the whole secret of The Babel Count.':
        if seen:
            body.remove(p)
            print('R6: Babel duplicate removed')
            break
        seen = True

delete_by_text({'The examples given in the following section are not designed to be creative or fooling, but to give a very simple example so that you can understand the architecture of each category.'}, 1)
print('R7: duplicated examples paragraph removed')

lvl = 0
for p in paras():
    t = ptext(p).strip()
    m = re.match(r'^(Level [1-3])([A-Z][A-Za-z -]+)$', t)
    if m:
        set_text(p, m.group(1) + ' ' + EM + ' ' + m.group(2))
        lvl += 1
assert lvl == 3, lvl
print('R7: level headers separated:', lvl)

# ── R8: zodiac element table marker ────────────────────────────
for p in paras():
    if ptext(p).strip() == 'Here is the table you need to know cold:':
        pos = list(body).index(p)
        body.insert(pos + 1, make_para('ZODIAC_ELEMENT_TABLE'))
        print('R8: zodiac element table marker placed')
        break

# ── R9: train dup + THings ─────────────────────────────────────
n = 0
for p in paras():
    t = ptext(p).strip()
    if t.startswith('One concrete way to train this. Pick a point'):
        body.remove(p)
        n += 1
assert n == 1, n
print('R9: duplicated train paragraph removed')

for p in paras():
    t = ptext(p)
    if 'THings' in t:
        set_text(p, t.replace('THings', 'Things'))
        print('R9: THings typo fixed')
        break

# ── R10: ovation opener ────────────────────────────────────────
pl = paras()
texts = [ptext(p).strip() for p in pl]
for i, t in enumerate(texts):
    if t.startswith('standing ovation' + chr(0x2019) + 's are predictable'):
        if texts[i - 1] == 'A':
            body.remove(pl[i - 1])
        set_text(pl[i], 'Standing ovations are predictable. ' + t.split('predictable. ', 1)[1])
        print('R10: ovation opener fixed')
        break

# ── R11: introductions internal duplicate ──────────────────────
for p in paras():
    t = ptext(p)
    if t.count('A strong introduction creates borrowed certainty.') == 2:
        first = t.index('before the first line is spoken.') + len('before the first line is spoken.')
        set_text(p, t[:first])
        print('R11: introductions duplicate trimmed')
        break

# ── R12: four forces duplicated lede ───────────────────────────
pl = paras()
texts = [ptext(p).strip() for p in pl]
for i, t in enumerate(texts):
    if t.startswith('our forces every audience evaluates'):
        assert texts[i - 1] == 'F'
        assert texts[i + 1].startswith('Four forces every audience evaluates')
        body.remove(pl[i - 1])
        body.remove(pl[i])
        print('R12: duplicated four-forces lede removed')
        break

out = ET.tostring(root, xml_declaration=True, encoding='UTF-8')
with zipfile.ZipFile(DOCX, 'w', zipfile.ZIP_DEFLATED) as z:
    for n_ in names:
        z.writestr(n_, out if n_ == 'word/document.xml' else contents[n_])
print('DOCX rewritten OK')
