"""DOCX repair #2 — 2026-06-12: restore card-system trigger formats flattened by the PDF merge.

R1 DISC type + blend cards (Ch10)
R2 Six-Category Radar (Ch9) -> SIX_AREA_RADAR + signal lines
R3 10-Second Scan step headers (01 — SHOES ...)
R4 Seven Stages arc cards (01 · PRIME ...)
R5 Neural Performance Checklist (join items with ' · ', uppercase heading)
R6 Warning callout trigger (strip the warning glyph prefix)
R7 Pattern interrupt marker (PATTERN_INTERRUPT_40PCT)
R8 Typos in stage/checklist text; split inline Performer's Note
"""
import zipfile, shutil
import xml.etree.ElementTree as ET

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
XMLSPACE = '{http://www.w3.org/XML/1998/namespace}space'
ET.register_namespace('w', W)
ET.register_namespace('r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')

DOCX = 'Architecture-of-Wonder.docx'
shutil.copy2(DOCX, 'backups/Architecture-of-Wonder.pre-cardrepair-20260612.docx')

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
    if not ts:
        r = ET.SubElement(p, f'{{{W}}}r')
        t = ET.SubElement(r, f'{{{W}}}t')
        ts = [t]
    ts[0].set(XMLSPACE, 'preserve')
    ts[0].text = text
    for t in ts[1:]:
        t.text = ''

def paras():
    return [el for el in body if el.tag == f'{{{W}}}p']

EM = chr(0x2014)   # em dash
MID = chr(0x00B7)  # middle dot

DISC_BODIES = {
 'D': 'Fast ' + MID + ' Decisive ' + MID + ' Results-focused ' + MID + ' Dislikes hesitation. On stage: Skip the warm-up. Lead with precision. A vague read loses them instantly. A dead-accurate specific wins them for the entire show. Signals: Fast walking ' + MID + ' Forward lean ' + MID + ' Direct unbroken eye contact ' + MID + ' Speaks first.',
 'I': 'Expressive ' + MID + ' Social ' + MID + ' Enthusiastic ' + MID + ' Wants to be part of the story. On stage: Ideal reactor. Their visible enthusiasm gives the room permission to feel the same thing. Select immediately for effects requiring emotional amplification. Signals: Open posture ' + MID + ' Frequent smiling ' + MID + ' Immediate humor response ' + MID + ' Forward lean.',
 'S': 'Calm ' + MID + ' Cooperative ' + MID + ' Supportive ' + MID + ' Dislikes conflict and rapid change. On stage: Cooperates without resistance. Best for imagination routines where quiet cooperation matters more than visible reaction. Signals: Minimal movement ' + MID + ' Settled posture ' + MID + ' Relaxed shoulders ' + MID + ' Unhurried speech.',
 'C': 'Analytical ' + MID + ' Precise ' + MID + ' Detail-oriented ' + MID + ' Processes before committing. On stage: Analyzes in real time. Needs coherence before compliance. Slow-burn effects work. Avoid rapid-fire routines. Signals: Balanced posture ' + MID + ' Measured speech ' + MID + ' Deliberate pauses ' + MID + ' Careful object handling.',
}
DISC_NAMES = {'D': 'DIRECT', 'I': 'INFLUENTIAL', 'S': 'STEADY', 'C': 'CONSCIENTIOUS'}

BLEND_BODIES = {
 'D/C': 'High-drive and highly analytical. Will comply. But only once they have decided you are credible. Most common in senior leadership and technical roles. Will not fake enthusiasm. Signals: Fast walk + deliberate conversational pauses + careful object handling. Strategy: Lead with precision. One dead-accurate specific wins them completely.',
 'I/S': 'Warm, expressive, genuinely people-focused. Easiest volunteer to work with. Risk: they react enthusiastically to almost anything. Calibrate what counts as genuine. Signals: Open posture + immediate expressiveness + head tilts frequently. Strategy: Use for effects requiring visible emotional response.',
 'D/I': 'Confident, high-energy, competitive. The natural Performer volunteer. Wants to succeed and be seen. Best asset when channeled. Most complex management challenge when not. Signals: Occupies space + animated gestures + immediately comfortable center-stage. Strategy: Give them a role, not a task. Frame as collaboration.',
 'C/S': 'Methodical, quiet, nearly unreadable in normal social interaction. Least expressive type. But capable of the deepest reaction when genuinely moved. Signals: Very little movement + minimal expression + looks at hands when thinking. Strategy: A C/S volunteer who goes wide-eyed is the most powerful moment in your show.',
}

RADAR = [
 ('01 ' + EM + ' Appearance', 'Clothing condition vs. posture [T2] ' + MID + ' Watch type and condition [T1] ' + MID + ' Shoe type and overall condition [T1] ' + MID + ' Belt notch wear [T1] ' + MID + ' Clothing brand level [T2] ' + MID + ' Teeth condition [T2] ' + MID + ' Privacy screen on device [T3] ' + MID + ' Cuff dirt [T1] ' + MID + ' Shoe lacing consistency [T1] ' + MID + ' Tattoo placement [T2]. Appearance builds your background picture fast: socioeconomic range, occupation type, self-image investment. T1 indicators here are physical-evidence reads. High reliability when anchored to posture and social signals.'),
 ('02 ' + EM + ' Movement & Posture', 'Walking speed vs. crowd [T2] ' + MID + ' Forward lean vs. upright [T2] ' + MID + ' Shoulder tension at rest [T2] ' + MID + ' Weight distribution [T2] ' + MID + ' Postural symmetry [T2] ' + MID + ' Foot direction in conversation [T2] ' + MID + ' Head tilt when listening [T2] ' + MID + ' Thumbs outside pockets [T2] ' + MID + ' Posture: open vs. protective [T2]. Movement patterns reveal confidence, stress state, and social orientation. Foot direction is particularly reliable, feet orient toward genuine interest.'),
 ('03 ' + EM + ' Territory & Personal Space', 'Bags kept in body contact when seated [T2] ' + MID + ' Back-to-wall seating preference [T2] ' + MID + ' Objects arranged as territorial boundaries [T2] ' + MID + ' Scanning toward exits [T2] ' + MID + ' Phone placed face-down [T3] ' + MID + ' Preferred conversational distance [T2] ' + MID + " Own vs. others' object handling [T2]. Territorial behavior reveals guardedness. Bag-contact + wall-seating + exit-scanning in combination points almost certainly to security, military, or law enforcement."),
 ('04 ' + EM + ' Social Confidence', 'Eye contact willingness [T2] ' + MID + ' Speed of moving out of way [T2] ' + MID + ' Fidgeting in public [T2] ' + MID + ' Eye contact break to swallow [T2] ' + MID + ' Blink rate change when speaking [T2] ' + MID + ' Compliance speed with casual instructions [T2] ' + MID + ' Humor reaction timing [T2] ' + MID + ' Vocal volume calibration [T2]. Confidence and suggestibility are NOT the same dimension. A highly confident person can be entirely resistant to suggestion. A quiet person can be extraordinarily responsive. Always assess these separately.'),
 ('05 ' + EM + ' Cognitive Processing', 'Response speed: rapid vs. deliberate [T2] ' + MID + ' Thinking gestures: chin, temple [T2] ' + MID + ' Analytical expression when processing [T2] ' + MID + ' Face touching during problem-solving [T2] ' + MID + ' Notification response: immediate vs. deferred [T3] ' + MID + ' Finger tapping during pauses [T3]. Cognitive style determines which performance approaches land most effectively. Fast processors respond to rapid-fire reveals. Deliberate processors reward slow burns.'),
 ('06 ' + EM + ' Emotional Regulation', 'Breathing depth during conversation [T2] ' + MID + ' Ear redness in conversation [T2] ' + MID + ' Face scrunch + deep breath [T2] ' + MID + ' Inside cheek or lip biting [T3] ' + MID + ' Cuticle picking: habitual vs. recent [T2] ' + MID + ' Micro-grooming during conversation [T2] ' + MID + ' Eyebrow expressiveness during surprise [T2] ' + MID + ' Leaning forward at high-interest moments [T2]. High expressiveness signals an ideal reactor for any demonstration requiring visible emotional response.'),
]

SCAN_STEPS = {'SHOES': '01', 'HANDS': '02', 'EYES': '03', 'POSTURE': '04', 'ENERGY': '05'}
STAGES = {'PRIME': '01', 'SIGNAL': '02', 'TENSION': '03', 'ANCHOR': '04', 'ESCALATE': '05', 'RELEASE': '06', 'EMBED': '07'}

# ── R1: DISC ───────────────────────────────────────────────────
pl = paras()
texts = [ptext(p).strip() for p in pl]

# delete the flattened infographic blob
blob_idx = next(i for i, t in enumerate(texts) if t.startswith('THE DISC COMMUNICATION STYLES'))
body.remove(pl[blob_idx])
print('R1: removed DISC infographic blob')

def replace_block(header_txt, n_followers, new_header, new_body):
    """Replace para with text header_txt and its n followers with header+body pair."""
    pl = paras()
    texts = [ptext(p).strip() for p in pl]
    idx = texts.index(header_txt)
    pos = list(body).index(pl[idx])
    for k in range(n_followers + 1):
        body.remove(pl[idx + k])
    body.insert(pos, make_para(new_header))
    body.insert(pos + 1, make_para(new_body))

for letter in 'DISC':
    mash = letter + DISC_NAMES[letter]
    replace_block(mash, 3, letter + ' ' + EM + ' ' + DISC_NAMES[letter], DISC_BODIES[letter])
    print('R1: rebuilt', letter, EM, DISC_NAMES[letter])

for blend in ['D/C', 'I/S', 'D/I', 'C/S']:
    replace_block(blend, 3, blend + ' Blend', BLEND_BODIES[blend])
    print('R1: rebuilt', blend, 'Blend')

# ── R2: Radar ──────────────────────────────────────────────────
pl = paras()
texts = [ptext(p).strip() for p in pl]
start = next(i for i, t in enumerate(texts) if t.startswith('#SIGNAL'))
end = next(i for i, t in enumerate(texts) if t == 'The 10-Second Scan')
assert start < end and end - start < 90, (start, end)
pos = list(body).index(pl[start])
for k in range(start, end):
    body.remove(pl[k])
new_paras = [make_para('SIX_AREA_RADAR')]
for h, b in RADAR:
    new_paras.append(make_para(h))
    new_paras.append(make_para(b))
for off, np in enumerate(new_paras):
    body.insert(pos + off, np)
print('R2: radar region rebuilt,', end - start, 'paras ->', len(new_paras))

# ── R3 + R4: merge number/name pairs ───────────────────────────
merged = 0
while True:
    pl = paras()
    texts = [ptext(p).strip() for p in pl]
    hit = None
    for i in range(len(pl) - 1):
        num, name = texts[i], texts[i + 1]
        if name in SCAN_STEPS and num == SCAN_STEPS[name]:
            hit = (i, num + ' ' + EM + ' ' + name)
            break
        if name in STAGES and num == STAGES[name]:
            hit = (i, num + ' ' + MID + ' ' + name)
            break
    if hit is None:
        break
    i, newtext = hit
    set_text(pl[i], newtext)
    body.remove(pl[i + 1])
    merged += 1
print('R3/R4: merged number/name pairs:', merged)

# ── R5: checklist joins ────────────────────────────────────────
pl = paras()
texts = [ptext(p).strip() for p in pl]
ck_start = texts.index('The Neural Performance Checklist')
# uppercase the renamed heading
for i in range(ck_start, ck_start + 60):
    if texts[i] == 'Volunteers and Audience Management':
        set_text(pl[i], 'VOLUNTEERS AND AUDIENCE MANAGEMENT')
        texts[i] = 'VOLUNTEERS AND AUDIENCE MANAGEMENT'
        print('R5: heading uppercased')
        break

HEADINGS = ['PRE-SHOW PRIMING', 'ATTENTION ARCHITECTURE', 'TENSION AND RELEASE',
            'VOLUNTEERS AND AUDIENCE MANAGEMENT', 'MEMORY ENCODING']
STOP = 'Your eyes moved to this callout'
for h in HEADINGS:
    pl = paras()
    texts = [ptext(p).strip() for p in pl]
    hi = texts.index(h, ck_start)
    items = []
    j = hi + 1
    while j < len(texts):
        t = texts[j]
        if (not t) or t in HEADINGS or t.startswith(STOP) or t == chr(0x00B7) + ' ' + chr(0x00B7) + ' ' + chr(0x00B7):
            break
        items.append(t)
        j += 1
    assert 2 <= len(items) <= 8, (h, items)
    joined = (' ' + MID + ' ').join(items)
    set_text(pl[hi + 1], joined)
    pos_list = pl[hi + 2:j]
    for p in pos_list:
        body.remove(p)
    print('R5:', h, '-', len(items), 'items joined')

# ── R6: warning glyph strip ────────────────────────────────────
pl = paras()
fixed = 0
for p in pl:
    t = ptext(p).strip()
    if t.endswith('Common Misread') and t != 'Common Misread':
        set_text(p, 'Common Misread')
        fixed += 1
print('R6: warning prefixes stripped:', fixed)

# ── R7: pattern interrupt marker ───────────────────────────────
pl = paras()
texts = [ptext(p).strip() for p in pl]
try:
    i40 = next(i for i, t in enumerate(texts)
               if t == '40%' and i + 1 < len(texts) and texts[i + 1] == 'INCREASE IN TRUST')
    # block: 40% / INCREASE IN TRUST / boost para / Processing Fluency Research / font para
    span = 2
    for j in range(i40 + 2, min(i40 + 7, len(texts))):
        span += 1
        if texts[j].startswith('The font you are reading'):
            break
    pos = list(body).index(pl[i40])
    for k in range(i40, i40 + span):
        body.remove(pl[k])
    body.insert(pos, make_para('PATTERN_INTERRUPT_40PCT'))
    print('R7: pattern interrupt marker restored, replaced', span, 'paras')
except StopIteration:
    print('R7: 40% block not found - SKIPPED')

# ── R8: typos + Performer's Note split ─────────────────────────
TYPOS = [
    ('Delay theis what feels good', 'Delay the payoff. The delay is what feels good'),
    ('Close with by reinforcing th memory', 'Close by reinforcing the memory'),
    ('The audiences brain craves resolution', "The audience's brain craves resolution"),
    ('Let the moment breath and allow', 'Let the moment breathe and allow'),
    ('audience memeber', 'audience member'),
]
tfixed = 0
for p in paras():
    full = ptext(p)
    newfull = full
    for old, new in TYPOS:
        cur = old.replace("'", chr(0x2019))
        if old in newfull:
            newfull = newfull.replace(old, new)
        elif cur in newfull:
            newfull = newfull.replace(cur, new)
    if newfull != full:
        set_text(p, newfull)
        tfixed += 1
print('R8: typo paragraphs fixed:', tfixed)

# split inline "Performer's Note. ..." into label + body
split = 0
for p in paras():
    full = ptext(p).strip()
    for variant in ("Performer's Note. ", 'Performer' + chr(0x2019) + 's Note. '):
        if full.startswith(variant) and len(full) > len(variant) + 10:
            rest = full[len(variant):]
            set_text(p, "Performer's Note")
            pos = list(body).index(p)
            body.insert(pos + 1, make_para(rest))
            split += 1
            break
print('R8: Performer Note splits:', split)

out = ET.tostring(root, xml_declaration=True, encoding='UTF-8')
with zipfile.ZipFile(DOCX, 'w', zipfile.ZIP_DEFLATED) as z:
    for n in names:
        z.writestr(n, out if n == 'word/document.xml' else contents[n])
print('DOCX rewritten OK')
