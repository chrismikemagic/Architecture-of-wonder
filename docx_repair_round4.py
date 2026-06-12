"""DOCX repair #4 — 2026-06-12: Five Cs duplicate block, standalone-download chrome.

R1 Ch7: remove the flattened Five Cs card block (the designed FIVE_CS_HTML grid
   already injects after the trigger sentence) + the mashed breadcrumb line.
R2 Part Five intro: join the split "B/efore You Begin" drop-cap and remove the
   two standalone-download paragraphs that don't belong in the full book.
"""
import zipfile, shutil
import xml.etree.ElementTree as ET

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
XMLSPACE = '{http://www.w3.org/XML/1998/namespace}space'
ET.register_namespace('w', W)
ET.register_namespace('r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')

DOCX = 'Architecture-of-Wonder.docx'
shutil.copy2(DOCX, 'backups/Architecture-of-Wonder.pre-round4-20260612.docx')

with zipfile.ZipFile(DOCX, 'r') as z:
    names = z.namelist()
    contents = {n: z.read(n) for n in names}

root = ET.fromstring(contents['word/document.xml'])
body = root.find(f'{{{W}}}body')

def ptext(p):
    return ''.join(t.text or '' for t in p.iter(f'{{{W}}}t'))

def set_text(p, text):
    ts = [t for t in p.iter(f'{{{W}}}t')]
    ts[0].set(XMLSPACE, 'preserve')
    ts[0].text = text
    for t in ts[1:]:
        t.text = ''

def paras():
    return [el for el in body if el.tag == f'{{{W}}}p']

RSQ = chr(0x2019)

# ── R1: Five Cs flattened block ────────────────────────────────
expected = [
    'THE FIVE C' + RSQ + 's OF BEHAVIORAL READING',
    'Context', 'What environment?', 'Context determines meaning. Always.',
    'Clusters', 'Multiple signals?', 'Never act on a single signal.',
    'Congruence', 'Body = words?', 'Incongruence is your most reliable signal.',
    'Consistency', 'Their baseline?', 'Without baseline, every read is a projection.',
    'Culture', 'Background norms?', 'Calibrate before concluding.',
    'Context' + chr(0x203A) + 'Clusters' + chr(0x203A) + 'Congruence' + chr(0x203A) + 'Consistency' + chr(0x203A) + 'Culture' + chr(0x203A) + 'READ',
]
pl = paras()
texts = [ptext(p).strip() for p in pl]
hi = texts.index(expected[0])
window = [t for t in texts[hi:hi + 30]]
to_delete = []
k = hi
matched = 0
for want in expected:
    while k < hi + 30 and texts[k] != want:
        k += 1
    assert k < hi + 30, ('missing expected line near Five Cs block:', want)
    to_delete.append(pl[k])
    matched += 1
    k += 1
for p in to_delete:
    body.remove(p)
print('R1: Five Cs flattened block removed -', matched, 'paragraphs')

# ── R2: standalone-download chrome ─────────────────────────────
pl = paras()
texts = [ptext(p).strip() for p in pl]
fixed = 0
for i, t in enumerate(texts):
    if t == 'B' and i + 1 < len(texts) and texts[i + 1] == 'efore You Begin':
        set_text(pl[i + 1], 'Before You Begin')
        body.remove(pl[i])
        fixed += 1
        break
assert fixed == 1, 'Before You Begin split not found'
print('R2: Before You Begin drop-cap joined')

removed = 0
for p in paras():
    t = ptext(p).strip()
    if (t == 'If you are reading this as a standalone download, here is what you are stepping into.'
            or t.startswith('The full book that this section is pulled from is not a mentalism book')):
        body.remove(p)
        removed += 1
assert removed == 2, removed
print('R2: standalone-download paragraphs removed:', removed)

out = ET.tostring(root, xml_declaration=True, encoding='UTF-8')
with zipfile.ZipFile(DOCX, 'w', zipfile.ZIP_DEFLATED) as z:
    for n in names:
        z.writestr(n, out if n == 'word/document.xml' else contents[n])
print('DOCX rewritten OK')
