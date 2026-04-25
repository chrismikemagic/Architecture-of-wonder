"""
Extract manuscript-extracted.txt from Architecture-of-Wonder.docx.

The Google Doc source uses Word styles (Heading1 / Heading2 / Heading3) and
mixes several chapter-heading conventions (a bare chapter-number line followed
by an ALL-CAPS Heading1 title; "CHAPTER N - TITLE" lines in Heading2; running-
header text "BUILT FOR WONDERCHAPTER N - TITLE" leaking into the body).

This script normalizes all of that into the format build-book.py expects:

    CHAPTER N
    <Title in Title Case>

    <body paragraphs...>

    PART ONE
    <Subtitle>

    ...

It also strips repeated page running headers, T-tier and observation-category
marker noise that build-book.py re-injects from CHAPTER_LEGEND, horizontal
rules, and reattaches drop-cap fragments (a single uppercase letter on its own
line followed by a paragraph that starts mid-word).
"""
from __future__ import annotations
import re, sys, zipfile
import xml.etree.ElementTree as ET

DOCX_PATH = 'Architecture-of-Wonder.docx'
OUT_PATH  = 'manuscript-extracted.txt'

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

# Lines that exist purely as visual chapter-opener markers (build-book.py
# regenerates these from CHAPTER_LEGEND / SECTION_BADGES). Drop them.
NOISE_EXACT = {
    'SIGNAL CONFIDENCE TIERS', 'OBSERVATION CATEGORIES',
    'CHAPTER LEGEND', 'WHAT IT FEELS LIKE',
    'BUILT FOR WONDER', 'BUILT FOR WONDER | VANISHING INC',
    'VANISHING INC', 'VANISHING INC.',
    'DECODE BEHAVIOR',
    'BPCRVSAM',
    'FRONT MATTER',
}
TIER_RE = re.compile(r'^T[1-4](?:T[1-4])*$')          # T1, T2T3, T1T2, etc.
CAT_RE  = re.compile(r'^(?:BP|CR|VS|AM){1,4}$')        # BP, AM, BPCR, BPCRVSAM
HRULE_RE = re.compile(r'^_{4,}$|^-{4,}$|^={4,}$')
RUNNING_HEADER_RE = re.compile(r'^BUILT FOR WONDER\b.*$')
PAGE_NUM_RE = re.compile(r'^\d{1,3}$')                 # standalone page number
CHAPTER_INLINE_RE = re.compile(r'^CHAPTER\s+(\d+[A-Z]?)\s*[—–\-]\s*(.+)$', re.I)
# Chapter numbers are 1..99 with optional letter suffix (1A, 19B). Zero-padded
# numbers like "01", "02" are list-item markers in the body, not chapters.
BARE_CHAPTER_NUM_RE = re.compile(r'^([1-9]\d?[A-Z]?)$')

PART_NAMES = {1: 'ONE', 2: 'TWO', 3: 'THREE', 4: 'FOUR', 5: 'FIVE'}

SMALL_WORDS = {
    'a','an','the','and','or','but','nor','for','of','in','on','at','to',
    'by','vs','vs.','with','from','as','if','so',
}

# Tokens that should stay all-caps in chapter / section titles. Any other
# all-caps word — even one that "looks like" an acronym — is title-cased.
ACRONYM_KEEP = {
    'REFLEX', 'FATE', 'FBI', 'CIA', 'NLP', 'OSINT', 'DRS', 'DISC',
    'AI', 'API', 'CEO', 'PR', 'TV', 'US', 'USA', 'UK',
}

def _cap_word(w: str) -> str:
    """Capitalize a word, including segments after hyphens (Pre-Show, 80-Signal)."""
    if not w:
        return w
    if w in ACRONYM_KEEP:
        return w
    return '-'.join(seg[:1].upper() + seg[1:].lower() if seg else seg
                    for seg in w.split('-'))


def title_case(s: str) -> str:
    """Title-case while keeping small words lowercase (except first/last) and a
    short whitelist of true acronyms in all-caps."""
    words = s.split()
    out = []
    for i, w in enumerate(words):
        bare = re.sub(r'[^A-Za-z]', '', w)
        if w in ACRONYM_KEEP or bare in ACRONYM_KEEP:
            out.append(w)
            continue
        bare_lower = bare.lower()
        if i not in (0, len(words)-1) and bare_lower in SMALL_WORDS:
            out.append(w.lower())
        else:
            out.append(_cap_word(w))
    return ' '.join(out)


def fix_smart_apostrophe(s: str) -> str:
    return s.replace('’', "'")


def read_paragraphs(docx_path: str):
    """Yield (style, text) for every body paragraph in document order."""
    with zipfile.ZipFile(docx_path) as z:
        doc_xml = z.read('word/document.xml')
    root = ET.fromstring(doc_xml)
    body = root.find('.//w:body', NS)
    for p in body.findall('.//w:p', NS):
        pStyle = p.find('.//w:pPr/w:pStyle', NS)
        style = pStyle.get(W + 'val') if pStyle is not None else 'Normal'
        text = ''.join(r.text or '' for r in p.findall('.//w:r/w:t', NS))
        yield style, text


def is_noise(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    if s in NOISE_EXACT:
        return True
    if TIER_RE.match(s):
        return True
    if CAT_RE.match(s):
        return True
    if HRULE_RE.match(s):
        return True
    if RUNNING_HEADER_RE.match(s):
        return True
    return False


def join_drop_cap(paragraphs: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """If a [Normal, single-uppercase-letter] is followed by a [Normal, lowercase-start]
    paragraph, merge them. This handles drop-cap fragments like:
        P
        ropless mentalism is...
    """
    out: list[tuple[str, str]] = []
    i = 0
    while i < len(paragraphs):
        style, text = paragraphs[i]
        if (style == 'Normal' and re.fullmatch(r'[A-Z]', text.strip())
                and i + 1 < len(paragraphs)):
            nxt_style, nxt_text = paragraphs[i+1]
            if (nxt_style == 'Normal' and nxt_text and nxt_text[0].islower()):
                drop = text.strip()
                # 'I' and 'A' are real English words; keep them as their own
                # token rather than fusing into the next word.
                sep = ' ' if drop in ('I', 'A') else ''
                merged = drop + sep + nxt_text
                out.append(('Normal', merged))
                i += 2
                continue
        # Heading1 used as drop-cap garbage like "sw" before chapter 22
        if (style == 'Heading1' and len(text.strip()) <= 4
                and not text.strip().isupper()
                and i + 1 < len(paragraphs)):
            # likely a Word styling glitch; drop it
            i += 1
            continue
        out.append((style, text))
        i += 1
    return out


def find_body_start(paragraphs: list[tuple[str, str]]) -> int:
    """Return the index of the paragraph immediately after acknowledgments end.

    Acknowledgments is a Heading2 = 'ACKNOWLEDGMENTS' block. We treat everything
    after it (and before the first chapter) as transitional material to keep.
    The first chapter starts with a Normal '1' followed by Heading1 'THE METHOD...'.
    """
    for i, (style, text) in enumerate(paragraphs):
        if text.strip().upper() == 'ACKNOWLEDGMENTS' and style.startswith('Heading'):
            return i
    return 0


def find_first_chapter(paragraphs: list[tuple[str, str]]) -> int:
    for i in range(len(paragraphs) - 1):
        st, t = paragraphs[i]
        st2, t2 = paragraphs[i+1]
        if (st == 'Normal' and BARE_CHAPTER_NUM_RE.fullmatch(t.strip())
                and t.strip().lstrip('0') == '1'
                and st2 == 'Heading1' and t2.strip().isupper()):
            return i
    return -1


def extract():
    paragraphs = list(read_paragraphs(DOCX_PATH))
    paragraphs = join_drop_cap(paragraphs)

    # Drop the leading TOC: everything before ACKNOWLEDGMENTS that looks like
    # the bullet TOC (Heading2 'Contents' through to Heading2 'ACKNOWLEDGMENTS').
    ack_idx = find_body_start(paragraphs)
    first_ch_idx = find_first_chapter(paragraphs)
    if first_ch_idx < 0:
        sys.exit('Could not find Chapter 1 start.')

    out_lines: list[str] = []

    # ── Front matter: from after the front-of-doc TOC through Acknowledgments
    #    and into the bridge paragraphs that lead up to Chapter 1.
    contents_idx = next(
        (i for i, (s, t) in enumerate(paragraphs)
         if s == 'Heading2' and t.strip().lower() == 'contents'),
        0,
    )

    # Everything from the very top to the line before "Contents" is the cover-
    # block "wonder / building" definitions. Keep those verbatim.
    for style, text in paragraphs[:contents_idx]:
        if is_noise(text):
            continue
        out_lines.append(text)
    # Skip the visible bullet TOC (Contents -> Acknowledgments)
    # But keep "How to Read This Book" + "A Note on Sources" + Acknowledgments.
    keep_after_contents = False
    for i in range(contents_idx, first_ch_idx):
        style, text = paragraphs[i]
        s = text.strip()
        if not keep_after_contents:
            if s == 'How to Read This Book' or s.upper() == 'HOW TO READ THIS BOOK':
                keep_after_contents = True
            elif s.upper() == 'ACKNOWLEDGMENTS':
                keep_after_contents = True
        if not keep_after_contents:
            continue
        if is_noise(text):
            continue
        if style == 'Heading2' and s.upper() == 'ACKNOWLEDGMENTS':
            out_lines.append('')
            out_lines.append('ACKNOWLEDGMENTS')
            continue
        out_lines.append(text)

    # Pad so the parser's `i > 143` TOC-skip threshold is satisfied.
    while len(out_lines) < 145:
        out_lines.append('')

    # ── Body: chapters and parts ────────────────────────────────────────────
    i = first_ch_idx
    n = len(paragraphs)
    last_part = 0  # for part-header detection

    def emit_chapter(num: str, title: str):
        out_lines.append('')
        out_lines.append('')
        out_lines.append(f'CHAPTER {num}')
        out_lines.append(title_case(title.strip()))

    def emit_part(num_word: str, subtitle: str):
        out_lines.append('')
        out_lines.append('')
        out_lines.append(f'PART {num_word}')
        out_lines.append(subtitle.strip())

    seen_part_word = None  # to dedupe the PART X running header
    emitted_chapters: set[str] = set()

    BFW_CHAPTER_RE = re.compile(
        r'^BUILT\s+FOR\s+WONDER\s*CHAPTER\s+(\d+[A-Z]?)\s*[—–\-]\s*(.+)$', re.I,
    )

    while i < n:
        style, text = paragraphs[i]
        s = text.strip()

        # PART X header: "PART ONE" Normal followed by Heading1 subtitle. Only
        # the FIRST sighting of each part word triggers part-emission; later
        # sightings are running-header noise that we drop without look-ahead.
        m_part = re.match(r'^PART\s+(ONE|TWO|THREE|FOUR|FIVE)\s*$', s, re.I)
        if m_part:
            part_word = m_part.group(1).upper()
            if part_word == seen_part_word:
                i += 1
                continue
            # First sighting: look only at the immediately next non-blank line
            subtitle = ''
            j = i + 1
            while j < n and not paragraphs[j][1].strip():
                j += 1
            if j < n:
                ns, nt = paragraphs[j]
                nt_s = nt.strip()
                if ns == 'Heading1' and not nt_s.isupper():
                    subtitle = nt_s
                elif ns == 'Normal' and nt_s and not nt_s.isupper() and not BARE_CHAPTER_NUM_RE.fullmatch(nt_s):
                    subtitle = nt_s
            emit_part(part_word, subtitle)
            seen_part_word = part_word
            if subtitle and j < n and paragraphs[j][1].strip() == subtitle:
                i = j + 1
            else:
                i += 1
            continue

        # Chapter heading: "BUILT FOR WONDERCHAPTER N - TITLE" running-header
        # leak — used as the chapter heading anchor when no other heading exists.
        m_bfw = BFW_CHAPTER_RE.match(s)
        if m_bfw:
            num = m_bfw.group(1)
            if num not in emitted_chapters:
                emit_chapter(num, m_bfw.group(2))
                emitted_chapters.add(num)
            i += 1
            continue

        # Chapter heading: "CHAPTER N - TITLE" inline (any style)
        m_inline = CHAPTER_INLINE_RE.match(s)
        if m_inline:
            num = m_inline.group(1)
            if num not in emitted_chapters:
                emit_chapter(num, m_inline.group(2))
                emitted_chapters.add(num)
            i += 1
            continue

        # Chapter heading: bare-number line followed by ALL-CAPS title (Heading1
        # OR Normal — chapter 23 uses Normal for its title).
        if (style == 'Normal' and BARE_CHAPTER_NUM_RE.fullmatch(s)
                and i + 1 < n
                and paragraphs[i+1][1].strip().isupper()
                and len(paragraphs[i+1][1].strip()) > 4
                and paragraphs[i+1][0] in ('Heading1', 'Normal')):
            num = s
            if num not in emitted_chapters:
                emit_chapter(num, paragraphs[i+1][1])
                emitted_chapters.add(num)
            i += 2
            continue

        # Skip noise lines
        if is_noise(s):
            i += 1
            continue

        # Skip remaining "BUILT FOR WONDER..." running header lines
        if RUNNING_HEADER_RE.match(s):
            i += 1
            continue

        # Heading2 (subsection or interlude) -> emit as bare heading line
        if style == 'Heading2':
            # Convert ALL-CAPS to Title Case for consistency with build-book.py is_section_header()
            heading = title_case(s) if s.isupper() else s
            out_lines.append('')
            out_lines.append(heading)
            i += 1
            continue

        # Heading3 (subsection)
        if style == 'Heading3':
            out_lines.append('')
            out_lines.append(s)
            i += 1
            continue

        # Heading1 used inside the body (rare): emit verbatim
        if style == 'Heading1':
            heading = title_case(s) if s.isupper() else s
            out_lines.append('')
            out_lines.append(heading)
            i += 1
            continue

        # Skip bare digits that aren't followed by Heading1 — these are list
        # numbers handled inline by build-book.py's text rendering.
        if BARE_CHAPTER_NUM_RE.fullmatch(s):
            # Pass through; build-book.py will render them as enumerated items.
            out_lines.append(text)
            i += 1
            continue

        out_lines.append(text)
        i += 1

    # Final cleanup: collapse 3+ blank lines into 2
    cleaned: list[str] = []
    blank_run = 0
    for line in out_lines:
        if not line.strip():
            blank_run += 1
            if blank_run <= 2:
                cleaned.append('')
        else:
            blank_run = 0
            cleaned.append(line)

    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(cleaned) + '\n')

    # Report
    chapter_count = sum(1 for l in cleaned if re.match(r'^CHAPTER \d+[A-Z]?$', l))
    part_count    = sum(1 for l in cleaned if re.match(r'^PART (ONE|TWO|THREE|FOUR|FIVE)$', l))
    print(f'Wrote {OUT_PATH}: {len(cleaned)} lines, {chapter_count} chapters, {part_count} parts.')

if __name__ == '__main__':
    extract()
