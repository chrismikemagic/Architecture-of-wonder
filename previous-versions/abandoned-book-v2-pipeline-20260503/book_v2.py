#!/usr/bin/env python3
"""
Built for Wonder — clean editorial build, v2.

Reads Architecture-of-Wonder.docx directly, filters all the running-header /
tier-code / drop-cap / editor-note junk that bled in from the merged source
document, and emits a single self-contained book.html with a modern editorial
design (warm cream, Source Serif body, Inter display, single column).

No dependence on the legacy build-book.py.
"""

from __future__ import annotations

import html
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table as DocxTable
from docx.text.paragraph import Paragraph as DocxParagraph

ROOT = Path(__file__).parent
DOCX_PATH = ROOT / "Architecture-of-Wonder.docx"
OUT_PATH  = ROOT / "book-cleaned.html"


# ─────────────────────────────────────────────────────────────────────────────
# Filtering rules
# ─────────────────────────────────────────────────────────────────────────────

# Lines we always drop (running headers, footers, page chrome, indicator codes).
JUNK_EXACT = {
    "SIGNAL CONFIDENCE TIERS",
    "OBSERVATION CATEGORIES",
    "BUILT FOR WONDER",
    "VANISHING INC.",
    "VANISHING INC",
    "BPCRVSAM",
    "C H R I S   M I C H A E L",
    "D E C O D E   B E H A V I O R",
    "A WORKING DEFINITION",
    # Redundant contributor labels that appear right before an expert panel.
    # The branded box already shows these — filtering avoids duplication.
    "Colin CloudFramework",
    "Colin Cloud Framework",
    "Colin Cloud Framework",
    "Anthem & AriaField Advice",
    "Anthem & Aria Field Advice",
    "Anthem & Aria Field Advice",
    "Anthem and AriaField Advice",
    "Anthem and Aria Field Advice",
    # Repeated title/cover material between the acknowledgments and Ch 1 —
    # already presented by the cover/title-slide at the top of the book.
    "BUILT",
    "FOR WONDER",
    "FRONT MATTER",
    "ABOUT THE AUTHOR",
    "Behavioral Strategist · Mentalist · Keynote Speaker",
    "— CHRIS MICHAEL",
    "CHRIS MICHAEL",
    # Duplicate "FRUIT TO FANG" all-caps that follows the proper Heading-3 title.
    "FRUIT TO FANG",
}

JUNK_PREFIXES = (
    "BUILT FOR WONDER ",   # em-space variant: "BUILT FOR WONDER<em-space>|<em-space>VANISHING INC"
    "BUILT FOR WONDER | ",
    "BUILT FOR WONDERCHAPTER",  # "BUILT FOR WONDERCHAPTER 1 — TITLE"
    "BUILT FOR WONDERABOUT",    # "BUILT FOR WONDERABOUT THE AUTHOR"
    "BUILT FOR WONDERTHE",      # "BUILT FOR WONDERTHE META REVEAL"
    "BUILT FOR WONDER ",
    "__*note to the editor",
    "__*editor",
    # CH 10's DISC communication styles run-on paragraph: the whole DISC
    # quadrant smashed into one line.  Standalone D/I/S/C entries that
    # follow already cover the content cleanly.
    "THE DISC COMMUNICATION STYLES",
)

# Standalone tier codes (T1..T4) and category codes (BP/CR/VS/AM)
TIER_CODE_RE = re.compile(r"^T[1-4]\s*$")
CATEGORY_CODE_RE = re.compile(r"^(BP|CR|VS|AM)\s*$")
# Concatenated tier codes like "T2T3"
CONCAT_TIER_RE = re.compile(r"^(T[1-4]){2,4}\s*$")
# Concatenated tier+code combo like "T2AM" / "T1BP CR" — chapter-opener chrome
TIER_PLUS_CODE_RE = re.compile(r"^T[1-4]\s*(?:BP|CR|VS|AM)(?:\s*(?:BP|CR|VS|AM))*\s*$")
# Page-bottom running header: "PART <ORDINAL>" inside body text (real part
# dividers come from Heading 1 styles, not plain-style PART lines).
PART_HEADER_RE = re.compile(r"^PART\s+(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT)\s*$")
# Placeholder artifacts left in the manuscript by earlier design passes —
# things like PERF_ARCH_FRAMEWORK_SVG, PERFORMANCE_MATRIX, CH18_DIAGNOSTIC_PANEL,
# CH18_IFYRE_PANEL, #SIGNALTIER, "CHAPTER ROADMAP — SUGGESTED ADDITION".
PLACEHOLDER_TOKEN_RE = re.compile(
    r"^(?:#?[A-Z][A-Z0-9_]*_(?:SVG|PANEL|MATRIX|FRAMEWORK|ROADMAP|DIAGRAM|FIGURE|GRID)"
    r"|#SIGNALTIER"
    r"|CHAPTER ROADMAP[\s\S]*"
    r"|SUGGESTED ADDITION"
    r"|.*SUGGESTED ADDITION.*"
    r")\s*$"
)
# Designer-spec placeholder lines.  Each placeholder pair looks like:
#   ALL CAPS LABEL
#   Designed insert: …  /  Designed reference table: …  / Designed one-page insert: …
DESIGNER_LABEL_RE = re.compile(
    r"^(FIVE QUESTIONS PANEL|SIGNAL TABLE|MINI SCENARIOS|QUICK-REFERENCE SHEET|"
    r"DESIGNED INSERT|DESIGNED PANEL|DESIGNED REFERENCE TABLE|DESIGNED TABLE|"
    r"DESIGNED ONE-PAGE INSERT|DESIGNED FLOWCHART|DESIGNED FIGURE)\s*$"
)
DESIGNER_NOTE_RE = re.compile(
    r"^(Designed insert|Designed reference table|Designed one-page insert|"
    r"Designed table|Designed panel|Designed flowchart|Designed figure)\b",
    re.IGNORECASE,
)
# Page numbers — short bare numbers
PAGE_NUM_RE = re.compile(r"^\d{1,3}\s*$")
# Section divider in the manuscript
SECTION_BREAK_RE = re.compile(r"^[·•]\s+[·•]\s+[·•]\s*$")
# A drop-cap letter on its own line: a single uppercase letter
DROPCAP_RE = re.compile(r"^[A-Z]$")


def is_junk(line: str) -> bool:
    s = line.strip()
    if not s:
        return False  # we keep blank lines as paragraph separators
    if s in JUNK_EXACT:
        return True
    for pre in JUNK_PREFIXES:
        if s.startswith(pre):
            return True
    if TIER_CODE_RE.match(s):
        return True
    if CATEGORY_CODE_RE.match(s):
        return True
    if CONCAT_TIER_RE.match(s):
        return True
    if TIER_PLUS_CODE_RE.match(s):
        return True
    # NOTE: bare-number pages (1, 2, 13) are no longer auto-filtered here —
    # they overlap with list-marker numbers ("1\nNovelty\n<body>" in CH 4
    # Five Forces).  Context-aware filtering happens in the parser.
    if PART_HEADER_RE.match(s):
        return True
    if DESIGNER_LABEL_RE.match(s):
        return True
    if DESIGNER_NOTE_RE.match(s):
        return True
    if PLACEHOLDER_TOKEN_RE.match(s):
        return True
    return False


def is_section_break(line: str) -> bool:
    return bool(SECTION_BREAK_RE.match(line.strip()))


# DISC personality first-letter prefix repair.  Source has malformed concats
# like "DDIRECT" / "IINFLUENTIAL" / "SSTEADY" / "CCONSCIENTIOUS".
DISC_REPAIR = {
    "DDIRECT":         "D — Direct",
    "IINFLUENTIAL":    "I — Influential",
    "SSTEADY":         "S — Steady",
    "CCONSCIENTIOUS":  "C — Conscientious",
}

# Numbered concat: "01EARLY COMMITMENT" or "01The Reflect and Reset"
# -> "01 — Early Commitment" / "01 — The Reflect and Reset"
NUMBERED_CONCAT_RE = re.compile(r"^(0[1-9]|[1-9][0-9])([A-Z][A-Za-z\s\-']+)$")


def repair_text(text: str) -> str:
    """Fix common manuscript-extraction artifacts at the paragraph level
    BEFORE classification.  Cheap regex repairs only — not content edits."""
    if not text:
        return text
    s = text.strip()
    # 1. Dropped-W bug: "HAT IT FEELS LIKE" -> "WHAT IT FEELS LIKE"
    if s == "HAT IT FEELS LIKE":
        return "WHAT IT FEELS LIKE"
    # 2. DISC personality letter+word concat
    if s in DISC_REPAIR:
        return DISC_REPAIR[s]
    # 3. Numbered concat — preserve original case unless source was ALL CAPS
    # (in which case title-case it for readability).
    m = NUMBERED_CONCAT_RE.match(s)
    if m:
        num, label = m.group(1), m.group(2).strip()
        if label.isupper():
            label = " ".join(w.capitalize() for w in label.split())
        return f"{num} — {label}"
    return text


# Known callout labels that may appear glued onto the end of a paragraph
# (separated by a newline).  Matches must be exact.
TRAILING_LABEL_PATTERNS = [
    "KEY PRINCIPLE",
    "KEY CONCEPT",
    "WHAT IT FEELS LIKE",
    "CHRIS MICHAEL'S TAKE",
    "CHRIS MICHAEL’S TAKE",
    "IF YOU REMEMBER NOTHING ELSE",
    "COMMON MISREAD",
    "WARNING",
    "THE TRUTH",
    "THE BOTTOM LINE",
]


def split_trailing_callout_label(raw_text: str) -> tuple[str, str | None]:
    """If a paragraph's text ends with a known callout label after a
    newline (e.g. 'prose...\\n\\nKEY PRINCIPLE'), split it: return
    (prose_only, label).  Otherwise return (raw_text.strip(), None)."""
    if not raw_text:
        return ("", None)
    for label in TRAILING_LABEL_PATTERNS:
        # Trim any trailing whitespace, then check for "\n…<label>" suffix.
        s = raw_text.rstrip()
        # Allow one or more newlines/spaces between the prose and the label.
        m = re.search(r"^(.*?)\n+\s*" + re.escape(label) + r"\s*$", s, re.S)
        if m:
            prose = m.group(1).rstrip()
            return (prose, label)
        # Also catch when the label is just glued on at end with a space/period
        # (very rare — only fire when there's clear punctuation before).
        if s.endswith(" " + label):
            prose_part = s[: -(len(label) + 1)].rstrip()
            if prose_part.endswith((".", "!", "?", "\"", "”")):
                return (prose_part, label)
    return (raw_text.strip(), None)


def looks_like_subhead(line: str, max_words: int = 9) -> bool:
    """Heuristic for a sub-section header that's stuck on 'normal' style.
    All-caps, short, no terminal punctuation."""
    s = line.strip()
    if not s or len(s) > 90:
        return False
    if s.endswith((".", ",", ":", "?", "!")):
        return False
    # Must contain at least one letter and all letters uppercase
    letters = [c for c in s if c.isalpha()]
    if not letters or not all(c.isupper() for c in letters):
        return False
    if len(s.split()) > max_words:
        return False
    # Skip our junk-but-uppercase strings (handled separately)
    if is_junk(s):
        return False
    return True


# ─────────────────────────────────────────────────────────────────────────────
# Document model
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class Block:
    kind: str            # see kinds list — adds: "type_cards" | "matrix2x2" | "method_cards" | "indicator_cards" | "expression_table" | "force_cards"
    text: str = ""
    rows: list[list[str]] = field(default_factory=list)   # for kind="table" | "pillars" | "levels"
    caption: str = ""    # optional caption above tables / figures, or label for callouts
    src: str = ""        # for kind="figure" — image path
    alt: str = ""        # alt text for figures
    # for kind="t4_panel"
    title: str = ""
    claim: str = ""
    research: str = ""
    valid: str = ""

@dataclass
class Chapter:
    number: int          # 1-indexed across the book; 0 for unnumbered (interlude / front)
    title: str
    epigraph: str = ""   # the hook line just under the chapter title
    blocks: list[Block] = field(default_factory=list)
    part_index: int | None = None    # which part this chapter sits inside
    interlude: bool = False
    label: str = ""      # e.g. "CHAPTER 1" or "INTERLUDE"

@dataclass
class Part:
    index: int           # 1-based
    ordinal: str         # "ONE" | "TWO" | ...
    title: str
    chapters: list[Chapter] = field(default_factory=list)


PART_ORDINALS = ["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT"]

PART_TITLES = [
    "Built for Wonder",
    "Reading the Room",
    "The Methods",
    "Performance Craft",
    "Authority, Influence & The Deep Framework",
]

# Per-chapter signal-tier and observation-category metadata used to render
# the symbol-pill row at each chapter opener.
# tiers: list from ['t1','t2','t3','t4']  cats: list from ['bp','cr','vs','am']
CHAPTER_LEGEND: dict[int, dict[str, list[str]]] = {
    1:  {'tiers': ['t1'],             'cats': ['am']},
    2:  {'tiers': ['t1'],             'cats': ['am']},
    3:  {'tiers': ['t1'],             'cats': ['am']},
    4:  {'tiers': ['t1', 't2'],       'cats': ['am']},
    5:  {'tiers': ['t1'],             'cats': ['am']},
    6:  {'tiers': ['t1'],             'cats': ['am']},
    7:  {'tiers': ['t1', 't2'],       'cats': ['am']},
    8:  {'tiers': ['t1', 't2'],       'cats': ['bp']},
    9:  {'tiers': ['t2', 't3'],       'cats': ['bp']},
    10: {'tiers': ['t2', 't3'],       'cats': ['bp']},
    11: {'tiers': ['t2', 't3'],       'cats': ['am']},
    12: {'tiers': ['t2', 't3'],       'cats': ['bp']},
    13: {'tiers': ['t2', 't3'],       'cats': ['bp', 'cr']},
    14: {'tiers': ['t1', 't2'],       'cats': ['bp']},
    15: {'tiers': ['t3'],             'cats': ['bp']},
    16: {'tiers': ['t1', 't2'],       'cats': ['am']},
    17: {'tiers': ['t3'],             'cats': ['cr']},
    18: {'tiers': ['t2'],             'cats': ['bp']},
    19: {'tiers': ['t1', 't2'],       'cats': ['am']},
    20: {'tiers': ['t2', 't3'],       'cats': ['cr']},
    21: {'tiers': ['t2', 't3'],       'cats': ['cr']},
    22: {'tiers': ['t2', 't3'],       'cats': ['am']},
    23: {'tiers': ['t2', 't3'],       'cats': ['am']},
    24: {'tiers': ['t2', 't3'],       'cats': ['bp', 'vs']},
    25: {'tiers': ['t2', 't3'],       'cats': ['cr']},
    26: {'tiers': ['t1', 't2'],       'cats': ['am']},
    27: {'tiers': ['t1', 't2'],       'cats': ['am']},
    28: {'tiers': ['t1', 't2', 't3'], 'cats': ['bp', 'cr']},
    29: {'tiers': ['t1', 't2'],       'cats': ['am']},
    30: {'tiers': ['t3'],             'cats': ['am']},
    31: {'tiers': ['t2', 't3'],       'cats': ['am']},
    32: {'tiers': ['t2', 't3'],       'cats': ['am']},
    33: {'tiers': ['t3'],             'cats': ['am']},
    34: {'tiers': ['t2', 't3'],       'cats': ['am']},
    35: {'tiers': ['t3'],             'cats': ['am']},
    36: {'tiers': ['t3'],             'cats': ['am']},
    37: {'tiers': ['t2', 't3'],       'cats': ['bp']},
    38: {'tiers': ['t2', 't3'],       'cats': ['am']},
    39: {'tiers': ['t2', 't3'],       'cats': ['bp']},
    40: {'tiers': ['t2', 't3'],       'cats': ['am']},
    41: {'tiers': ['t2', 't3'],       'cats': ['am']},
    42: {'tiers': ['t2', 't3'],       'cats': ['am']},
}

# Heading-1 strings we know are corrupted in the source DOCX -> the real title
CORRUPTED_H1_FIXUPS = {"sw": "MAKING BETTER PROPLESS MENTALISM"}

# Expert / collaborator paragraphs that should render in their own branded
# panels, matching the colors/typography from the legacy designed build.  The
# match key is a unique opening substring of the paragraph in the manuscript;
# the value is (variant, label, subtitle).  Variant drives the CSS class.
EXPERT_PANELS: list[tuple[str, str, str, str]] = [
    # Colin Cloud — Framework (forest green gradient)
    ("Most performers learn pre-show and start using it",
     "colin-cloud", "Colin Cloud", "Framework"),
    ("Every pre-show is a dual reality",
     "colin-cloud", "Colin Cloud", "Framework"),
    ("If one person in the audience learns how this was done",
     "colin-cloud", "Colin Cloud", "Framework"),
    ("The question isn’t only whether the audience talks",
     "colin-cloud", "Colin Cloud", "Framework"),
    ("The question isn't only whether the audience talks",
     "colin-cloud", "Colin Cloud", "Framework"),
    ("Concealment protects the effect. Design protects the career",
     "colin-cloud", "Colin Cloud", "Framework"),
    ("The best pre-show target isn’t the most interesting person",
     "colin-cloud", "Colin Cloud", "Framework"),
    ("The best pre-show target isn't the most interesting person",
     "colin-cloud", "Colin Cloud", "Framework"),
    ("Pre-show solves a performance problem. The cleaner solution",
     "colin-cloud", "Colin Cloud", "Framework"),
    # Anthem & Aria — Field Advice (rose-blue gradient)
    ("Anthem and Aria also stress that readings land harder",
     "anthem-aria", "Anthem & Aria", "Field Advice"),
    ("As Anthem and Aria point out, stock lines work best",
     "anthem-aria", "Anthem & Aria", "Field Advice"),
    ("Aria’s idea of a DIY oracle is useful",
     "anthem-aria", "Anthem & Aria", "Field Advice"),
    ("Aria's idea of a DIY oracle is useful",
     "anthem-aria", "Anthem & Aria", "Field Advice"),
]


def _expert_panel_match(text: str) -> tuple[str, str, str] | None:
    """Return (variant, label, subtitle) if this paragraph should be rendered
    as an expert panel, else None."""
    for prefix, variant, label, subtitle in EXPERT_PANELS:
        if text.startswith(prefix):
            return (variant, label, subtitle)
    return None


# All-caps short subhead labels that should kick off a CALLOUT BOX rather than
# render as a normal section header.  When the parser sees one of these, the
# next non-empty paragraph becomes the callout body, and the label is the title.
CALLOUT_LABELS = {
    "KEY PRINCIPLE":          ("key",     "Key Principle"),
    "KEY CONCEPT":            ("key",     "Key Concept"),
    "WHAT IT FEELS LIKE":     ("feel",    "What It Feels Like"),
    "CHRIS MICHAEL'S TAKE":   ("take",    "Chris Michael's Take"),
    "CHRIS MICHAEL’S TAKE":   ("take",    "Chris Michael's Take"),  # smart quote variant
    "COMMON MISREAD":         ("warn",    "Common Misread"),
    "WARNING":                ("warn",    "Warning"),
    "IF YOU REMEMBER NOTHING ELSE":  ("memorable", "If You Remember Nothing Else"),
    "THE TRUTH":              ("truth",   "The Truth"),
    "THE BOTTOM LINE":        ("truth",   "The Bottom Line"),
}

# Title strings that should be H1 chapter starts but live under 'normal' style
UNSTYLED_CHAPTER_TITLES = {"PROPLESS SYSTEMS THAT ACTUALLY WORK"}

# Figure anchor map: {chapter_number: [(anchor_substring, image_relative_path, caption, alt), ...]}
# When a paragraph in the named chapter STARTS WITH (or exactly matches) the anchor,
# the figure is injected immediately BEFORE that paragraph.
FIGURES: dict[int, list[tuple[str, str, str, str]]] = {
    24: [
        # Chapter opener — a wide setup image
        ("REFLEX, my which-hand routine",
         "resources/figures/reflex-head-tilt.png",
         "The setup. Volunteer presents both fists; you read the tell.",
         "Volunteer holding out both fists toward the performer."),
        # Phase 1, Tell 1 — thumb placement
        ("The primary tell is thumb placement",
         "resources/figures/reflex-both-fists-thumb.png",
         "Tell #1 — Thumb placement. Watch where each thumb sits when the hands come out.",
         "Two fists side by side; one thumb tucks against the index, the other rests outside."),
        # Phase 1, Tell 3 — knuckle stepping
        ("The third tell is knuckle stepping",
         "resources/figures/reflex-knuckles-stepped.png",
         "Tell #3 — Knuckle stepping. The first two knuckles step forward when the hand grips an object.",
         "Close-up of a fist with the first two knuckles raised above the rest."),
        # Phase 3 — chin / head-tilt tell
        ("The chin tell",
         "resources/figures/reflex-fist-side.png",
         "Phase 3 — Head tilt. By the third round, the head leans subtly toward the concealing hand.",
         "Side view of a fist held forward, illustrating the body's tilt cue."),
    ],
}

# H1s that are not numbered chapters
SPECIAL_H1 = {
    "THE META REVEAL": ("finale", "Finale"),
    "CONTROLLING THE ROOM": ("interlude", "Interlude"),
}


def merge_dropcap(letter: str, next_text: str) -> str | None:
    """Glue a Word drop-cap letter onto the next paragraph correctly.

    Three patterns to distinguish:
      1. 'T' + 'his effect...'  -> drop cap, next starts lowercase -> "This effect..."
      2. 'T' + 'His effect...'  -> drop cap with capitalization typo, long prose
                                    follows -> "This effect..." (we lowercase the H)
      3. 'I' + 'Confidence'     -> Roman numeral + heading -> don't merge
      4. 'I' + 'was nearly done'-> 'I' is a real one-letter word -> "I was..."
    """
    next_text = next_text.lstrip()
    if not next_text:
        return letter
    if next_text[0].isupper():
        # Heuristic: short label-like next text (no terminal punctuation, ≤4
        # words) is a Roman numeral pattern → don't merge.  Long prose-like
        # next text is a drop cap whose first letter just got mis-cased.
        is_label_like = (
            len(next_text) < 40
            and not next_text.endswith((".", ",", ":", "?", "!"))
            and len(next_text.split()) <= 4
        )
        if is_label_like:
            return None
        # Drop cap with a capitalized typo → lowercase first letter for a
        # clean merge: "T" + "His effect..." → "This effect..."
        next_text = next_text[0].lower() + next_text[1:]
    if letter in ("I", "A") and next_text and next_text[0].islower():
        return f"{letter} {next_text}"
    return f"{letter}{next_text}"


_ROMAN_RE = re.compile(r"^(I|II|III|IV|V|VI|VII|VIII|IX|X)$")
_LEVEL_RE = re.compile(r"^Level\s+(\d+)$", re.IGNORECASE)

# Six-Category Radar names (CH 9, after T4)
RADAR_CATEGORIES = [
    "APPEARANCE",
    "MOVEMENT & POSTURE",
    "TERRITORY & PERSONAL SPACE",
    "SOCIAL CONFIDENCE",
    "COGNITIVE PROCESSING",
    "EMOTIONAL REGULATION",
]

# 10-Second Scan step names
SCAN_STEPS = ["SHOES", "HANDS", "EYES", "POSTURE", "ENERGY"]

# Match a signal line that arrives as "—Signal textT[1-4]" (em-dash prefix or
# leading dash, plus collapsed tier code).  The tier may also be missing.
_RADAR_SIGNAL_RE = re.compile(
    r"^[—–\-]?\s*(?P<text>.+?)(?P<tier>T[1-4])\s*$"
)


def _is_pillar_marker(b: Block) -> str | None:
    if b.kind not in ("para", "subhead"):
        return None
    m = _ROMAN_RE.match(b.text.strip())
    return m.group(1) if m else None


def _is_level_marker(b: Block) -> str | None:
    if b.kind not in ("para", "subhead"):
        return None
    m = _LEVEL_RE.match(b.text.strip())
    return m.group(1) if m else None


CATEGORY_NAME_TO_LETTER = {
    "Behavioral Profiling": "BP",
    "Cold Reading":         "CR",
    "Volunteer Selection":  "VS",
    "Audience Management":  "AM",
}


def _collapse_observation_category_cards(blocks: list[Block]) -> list[Block]:
    """Convert the front-matter 'Observation Categories' section into a
    category-card grid.  The single-letter codes (BP/CR/VS/AM) get filtered
    out as junk during parse so we match by category name instead.
    Pattern: subhead 'Observation Categories' -> intro para -> 4× (name, desc)."""
    out: list[Block] = []
    i = 0
    n = len(blocks)
    while i < n:
        b = blocks[i]
        if (b.kind == "subhead"
                and b.text.strip().lower() == "observation categories"
                and i + 1 < n):
            out.append(b)
            i += 1
            # Intro paragraph passes through.
            if i < n and blocks[i].kind == "para" and blocks[i].text.strip() not in CATEGORY_NAME_TO_LETTER:
                out.append(blocks[i])
                i += 1
            # Collect (name, desc) pairs.
            entries: list[tuple[str, str, str]] = []
            while i + 1 < n and blocks[i].kind == "para":
                name = blocks[i].text.strip()
                if name not in CATEGORY_NAME_TO_LETTER:
                    break
                desc = blocks[i + 1].text.strip() if blocks[i + 1].kind == "para" else ""
                if not desc:
                    break
                entries.append((CATEGORY_NAME_TO_LETTER[name], name, desc))
                i += 2
            if len(entries) >= 2:
                cb = Block(kind="category_cards")
                cb.rows = [list(e) for e in entries]
                out.append(cb)
            continue
        out.append(b)
        i += 1
    return out


def _promote_title_case_subheads(blocks: list[Block]) -> list[Block]:
    """Detect short Title Case paragraphs followed by a longer body and promote
    them to subheads.  Catches unstyled section headers like
    'Cognitive Economy' / 'Metabolic Efficiency' / 'Predictive Processing'
    that the source DOCX leaves on `normal` style.

    Conservative rules to avoid false positives:
      - 2..6 words
      - 3..60 chars
      - no terminal punctuation
      - first character is uppercase, but not ALL caps (those are already subheads)
      - the IMMEDIATELY-following block is a "para" of length >= 80
      - paragraph has no internal punctuation that signals a sentence
        (".", "?", "!" anywhere, or "," followed by space within the first 30 chars)
      - not in skip list (e.g. callout labels, contributor names)
    """
    SKIP = {
        "chris michael", "chris michael's take", "chris michael’s take",
        "colin cloud", "anthem & aria", "anthem and aria",
        "patrick redford", "fraser parker", "kevin hamdan",
        "what to say", "what you say", "the line", "the move",
        "the truth", "the bottom line", "the tradeoff",
        "performer's note", "performer’s note", "field note", "author's note",
    }
    out: list[Block] = []
    n = len(blocks)
    for i, b in enumerate(blocks):
        if b.kind != "para":
            out.append(b)
            continue
        t = b.text.strip()
        if not (3 <= len(t) <= 60):
            out.append(b)
            continue
        words = t.split()
        if not (1 <= len(words) <= 6):
            out.append(b)
            continue
        # Single-word labels are dangerous (could just be a name in narrative).
        # Require a longer body and capitalized first letter to compensate.
        if len(words) == 1 and (i + 1 >= n or len(blocks[i + 1].text.strip()) < 100):
            out.append(b)
            continue
        if t.endswith((".", ",", ":", "?", "!", "”", "\"")):
            out.append(b)
            continue
        if any(ch in t for ch in (".", "?", "!")):
            out.append(b)
            continue
        if not t[0].isupper() or t.isupper():
            out.append(b)
            continue
        if t.lower() in SKIP:
            out.append(b)
            continue
        # Avoid promoting story/narrative openers like proper nouns mid-sentence
        # or paragraphs that contain quotes / dialogue markers.
        if any(ch in t for ch in ("“", "”", "'", "—", " — ", "(", ")")):
            out.append(b)
            continue
        # Require following block to be a real prose paragraph.
        if i + 1 >= n or blocks[i + 1].kind != "para":
            out.append(b)
            continue
        next_text = blocks[i + 1].text.strip()
        if len(next_text) < 50:
            out.append(b)
            continue
        # Looks like a section header — promote.
        out.append(Block(kind="subhead", text=t))
    return out


def _collapse_design_summary(blocks: list[Block]) -> list[Block]:
    """The Meta Reveal's 'Design Summary' is a sequence of paragraphs where
    each paragraph is two cells smashed together with no separator (the
    book-element name in lowercase letters, then the psychological-mechanism
    name starting with a Capital).  Split at the lowercase→Capital boundary
    and render as a 2-column table."""
    out: list[Block] = []
    i = 0
    n = len(blocks)
    SPLIT_RE = re.compile(r"(?<=[a-z\)\.\!\?])(?=[A-Z])")
    while i < n:
        b = blocks[i]
        if (b.kind in ("subhead", "para")
                and b.text.strip() == "The Design Summary"):
            # promote the title to a real subhead in the output
            out.append(Block(kind="subhead", text="The Design Summary"))
            i += 1
            rows: list[list[str]] = []
            while i < n and blocks[i].kind == "para":
                t = blocks[i].text.strip()
                # stop at a section divider line or anything that isn't a
                # short two-cell smash (keep an upper bound on length).
                if not t or len(t) > 120:
                    break
                parts = SPLIT_RE.split(t, maxsplit=1)
                if len(parts) != 2:
                    break
                rows.append([parts[0].strip(), parts[1].strip()])
                i += 1
            if rows:
                tb = Block(kind="table")
                tb.rows = [["Book Element", "Psychological Mechanism"]] + rows
                tb.caption = "design-summary"
                out.append(tb)
            continue
        out.append(b)
        i += 1
    return out


def _dedupe_adjacent_paragraphs(blocks: list[Block]) -> list[Block]:
    """Drop a paragraph if it's identical to the immediately-prior paragraph.
    Catches manuscript artifacts like CH 20's duplicated 'Influence and
    counting. That is the whole secret of The Babel Count.' line."""
    out: list[Block] = []
    last_para_text = None
    for b in blocks:
        if b.kind == "para":
            t = b.text.strip()
            if t and t == last_para_text:
                continue  # skip duplicate
            last_para_text = t
        else:
            last_para_text = None
        out.append(b)
    return out


def _split_concatenated_signals(text: str) -> list[tuple[str, str]]:
    """A run of em-dash-prefixed signals that got jammed into one paragraph
    can be split on the em-dash separator: '—Signal AT2 —Signal BT1 —...'.
    Returns list of (signal_text, tier).
    """
    parts = re.split(r"\s*[—–]\s+", text)
    out: list[tuple[str, str]] = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        m = _RADAR_SIGNAL_RE.match(p)
        if m:
            out.append((m.group("text").strip(), m.group("tier")))
        else:
            # tier-less leftover
            out.append((p, ""))
    return out


def _collapse_radar_and_scan(blocks: list[Block]) -> list[Block]:
    """Detect the Six-Category Radar block and the 10-Second Scan block,
    replace each with a structured Block."""
    out: list[Block] = []
    i = 0
    n = len(blocks)
    while i < n:
        b = blocks[i]

        # Trigger on the section subhead.
        if b.kind == "subhead" and b.text.strip().lower() == "the six-category radar":
            out.append(b)  # keep the subhead
            i += 1
            # Optionally absorb the AMTSCE acronym line + intro paragraph
            while i < n and blocks[i].kind in ("para", "subhead") \
                    and blocks[i].text.strip().upper() not in RADAR_CATEGORIES:
                out.append(blocks[i])
                i += 1
                # Stop just before a category name so we can collect the radar
                if i < n and blocks[i].kind in ("para", "subhead") and blocks[i].text.strip().upper() in RADAR_CATEGORIES:
                    break
            # Collect 6 categories.
            radar_rows: list[tuple[str, str, list[tuple[str, str]]]] = []
            while i < n:
                cat_b = blocks[i]
                if cat_b.kind not in ("para", "subhead"):
                    break
                cat_name = cat_b.text.strip().upper()
                if cat_name not in RADAR_CATEGORIES:
                    break
                i += 1
                # next: description paragraph
                desc = ""
                if i < n and blocks[i].kind == "para":
                    desc = blocks[i].text.strip()
                    i += 1
                # then: signal lines until the next category or non-signal.
                signals: list[tuple[str, str]] = []
                while i < n:
                    nxt = blocks[i]
                    if nxt.kind not in ("para", "subhead"):
                        break
                    nxt_text = nxt.text.strip()
                    # Stop if we hit the next category name.
                    if nxt_text.upper() in RADAR_CATEGORIES:
                        break
                    # If it looks like a single signal line:
                    m = _RADAR_SIGNAL_RE.match(nxt_text)
                    if m and (nxt_text.startswith(("—", "–", "-")) or len(nxt_text) < 80):
                        signals.append((m.group("text").strip(), m.group("tier")))
                        i += 1
                        continue
                    # Concatenated signals?
                    if "—" in nxt_text and re.search(r"T[1-4]", nxt_text):
                        split = _split_concatenated_signals(nxt_text)
                        if split and all(s[1] for s in split[:3]):
                            signals.extend(split)
                            i += 1
                            continue
                    break
                radar_rows.append((cat_name, desc, signals))
            if radar_rows:
                rb = Block(kind="radar")
                rb.rows = [[name, desc, signals] for (name, desc, signals) in radar_rows]
                out.append(rb)
            continue

        # 10-Second Scan
        if b.kind in ("subhead", "para") and b.text.strip().lower() in ("the 10-second scan", "the ten-second scan"):
            # promote to a subhead in the output
            out.append(Block(kind="subhead", text=b.text.strip()))
            i += 1
            # Absorb intro paragraph(s) until first scan step
            while i < n and blocks[i].kind in ("para", "subhead") \
                    and blocks[i].text.strip().upper() not in SCAN_STEPS:
                out.append(blocks[i])
                i += 1
            steps: list[tuple[str, str]] = []
            while i < n:
                step_b = blocks[i]
                if step_b.kind not in ("para", "subhead"):
                    break
                step_name = step_b.text.strip().upper()
                if step_name not in SCAN_STEPS:
                    break
                i += 1
                # collect paragraphs until the next step or another subhead.
                buf: list[str] = []
                while i < n:
                    nxt = blocks[i]
                    if nxt.kind not in ("para",):
                        break
                    if nxt.text.strip().upper() in SCAN_STEPS:
                        break
                    buf.append(nxt.text.strip())
                    i += 1
                steps.append((step_name, "\n\n".join(buf)))
            if steps:
                sb = Block(kind="scan")
                sb.rows = [[name, body] for (name, body) in steps]
                out.append(sb)
            continue

        out.append(b)
        i += 1
    return out


# ── Observation Table (CH 13 Fruit to Fang, possibly elsewhere) ──
# Detects the 4-column "What you observe / What it usually suggests / What you
# do next / What it may indicate" header pattern, then collects N×4 rows.
OBS_HEADERS = ["What you observe", "What it usually suggests", "What you do next", "What it may indicate"]


def _collapse_observation_table(blocks: list[Block]) -> list[Block]:
    out: list[Block] = []
    i = 0
    n = len(blocks)
    while i < n:
        # Look for the 4 header lines in sequence
        if (i + 4 <= n
                and all(b.kind in ("para", "subhead") for b in blocks[i:i+4])
                and [b.text.strip() for b in blocks[i:i+4]] == OBS_HEADERS):
            # Now gather data rows: each row = next 4 paragraphs.
            rows: list[list[str]] = []
            j = i + 4
            while j + 3 < n:
                cells = [b.text.strip() for b in blocks[j:j+4]]
                # Stop if any cell looks like a section header (ALL CAPS) or empty.
                if not all(cells):
                    break
                if any(c.isupper() and len(c) > 4 and c.replace(" ", "").isalpha() for c in cells):
                    # First cell of next group might be a new section title.
                    break
                rows.append(cells)
                j += 4
            if rows:
                ob = Block(kind="obs_table")
                ob.rows = [list(OBS_HEADERS)] + rows
                out.append(ob)
                i = j
                continue
        out.append(blocks[i])
        i += 1
    return out


# ── Fruit to Fang flowchart (CH 13) ──
# This is a fixed-content widget ported from the legacy build.  The source DOCX
# expresses it as a series of paragraphs separated by ↓ arrows; we replace the
# whole run with a single Block(kind="ftf_flow") whose renderer outputs the
# proper branching structure.
def _collapse_ftf_flow(blocks: list[Block]) -> list[Block]:
    out: list[Block] = []
    i = 0
    n = len(blocks)
    while i < n:
        b = blocks[i]
        if (b.kind in ("para", "subhead")
                and b.text.strip().upper() == "HOW SEARCH EFFORT NARROWS THE FIELD"):
            # Skip every following block until we leave the flowchart region
            # (heuristic: ≥ ~30 short blocks of arrows / labels, or a long
            # narrative paragraph (>200 chars) signals the end).
            j = i + 1
            consumed = 0
            while j < n and consumed < 60:
                nxt = blocks[j]
                if nxt.kind not in ("para", "subhead"):
                    break
                t = nxt.text.strip()
                if len(t) > 200:
                    break
                # Stop on a known next subhead
                if t in ("Microexpressions", "Microexpressions in Mentalism") or t.endswith("KEY PRINCIPLE"):
                    break
                j += 1
                consumed += 1
            fb = Block(kind="ftf_flow")
            out.append(fb)
            i = j
            continue
        out.append(b)
        i += 1
    return out


# ── Flowchart (CH 13 "HOW SEARCH EFFORT NARROWS THE FIELD") ──
# Detect a sequence containing ↓ arrows and convert to a structured flow.
def _collapse_flowchart(blocks: list[Block]) -> list[Block]:
    out: list[Block] = []
    i = 0
    n = len(blocks)
    while i < n:
        # Trigger: a subhead/para with "HOW " in title and "FIELD" or "FLOWCHART"
        b = blocks[i]
        is_trigger = (
            b.kind in ("para", "subhead")
            and b.text.strip().upper() in ("HOW SEARCH EFFORT NARROWS THE FIELD",)
        )
        if not is_trigger:
            out.append(b)
            i += 1
            continue
        # Title found — collect subsequent paragraphs until we hit something
        # that clearly isn't part of the flow (e.g. another subhead, or a long
        # narrative paragraph followed by something non-flowy).
        title = b.text.strip()
        j = i + 1
        steps: list[dict] = []
        # We'll group into "stages" separated by ↓ markers. Each stage is a
        # list of lines; the first line is the prompt, additional lines are
        # outcome details.
        cur_stage: list[str] = []
        max_steps = 60
        while j < n and len(steps) < max_steps:
            nxt = blocks[j]
            if nxt.kind not in ("para", "subhead"):
                break
            t = nxt.text.strip()
            if not t:
                j += 1
                continue
            # Stop if we hit a clearly-out-of-flow paragraph (long narrative > 200 chars
            # with no arrow/category language)
            if len(t) > 200:
                break
            if t == "↓":
                if cur_stage:
                    steps.append({"lines": cur_stage})
                    cur_stage = []
                j += 1
                continue
            cur_stage.append(t)
            j += 1
        if cur_stage:
            steps.append({"lines": cur_stage})
        if len(steps) >= 3:
            fb = Block(kind="flowchart")
            fb.title = title
            fb.rows = [[" ".join(s["lines"][:1])] + s["lines"][1:] for s in steps]
            out.append(fb)
            i = j
            continue
        out.append(b)
        i += 1
    return out


# ── Volunteer Types (Ch 11) ──
VOLUNTEER_TYPES = [
    "The Supporter", "The Performer", "The Challenger",
    "The Anxious Volunteer", "The Analytical Volunteer",
    "The Emotional Volunteer", "The Reserved Volunteer",
]


def _split_camelcase_bullets(text: str) -> list[str]:
    """Split a paragraph that has bullets jammed together with no separator
    (lowercase-then-capital boundary)."""
    if not text:
        return []
    # Insert a marker at every lowercase->Capital boundary, then split on it.
    marked = re.sub(r"(?<=[a-z\)\.\!\?])(?=[A-Z])", "", text)
    parts = [p.strip() for p in marked.split("") if p.strip()]
    return parts


def _collapse_volunteer_types(blocks: list[Block], chapter_num: int) -> list[Block]:
    if chapter_num != 11:
        return blocks
    out: list[Block] = []
    i = 0
    types_collected: list[dict] = []
    while i < len(blocks):
        b = blocks[i]
        if b.kind in ("para", "subhead") and b.text.strip() in VOLUNTEER_TYPES:
            # collect 4 paragraphs after the name: desc, tells, works, avoid
            entry = {"name": b.text.strip(), "desc": "", "tells": [], "works": "", "avoid": ""}
            j = i + 1
            grabbed = 0
            while j < len(blocks) and grabbed < 4:
                nxt = blocks[j]
                if nxt.kind not in ("para", "subhead"):
                    break
                # If next block is another type name, stop
                if nxt.text.strip() in VOLUNTEER_TYPES:
                    break
                t = nxt.text.strip()
                if grabbed == 0:
                    entry["desc"] = t
                elif grabbed == 1:
                    entry["tells"] = _split_camelcase_bullets(t)
                elif grabbed == 2:
                    # Strip leading "Works best for" if present
                    entry["works"] = re.sub(r"^Works best for\s*", "", t, flags=re.IGNORECASE)
                elif grabbed == 3:
                    entry["avoid"] = re.sub(r"^Avoid for\s*", "", t, flags=re.IGNORECASE)
                grabbed += 1
                j += 1
            types_collected.append(entry)
            i = j
            continue
        # If we already have a run of types collected and this isn't another type,
        # flush them as one block first.
        if types_collected:
            tb = Block(kind="type_cards")
            tb.rows = [[e["name"], e["desc"], e["tells"], e["works"], e["avoid"]] for e in types_collected]
            tb.caption = "volunteer"
            out.append(tb)
            types_collected = []
        out.append(b)
        i += 1
    if types_collected:
        tb = Block(kind="type_cards")
        tb.rows = [[e["name"], e["desc"], e["tells"], e["works"], e["avoid"]] for e in types_collected]
        tb.caption = "volunteer"
        out.append(tb)
    return out


# ── Volunteer Selection Matrix (Ch 11) ──
MATRIX_QUADRANTS = [
    "High Confidence + High Suggestibility",
    "High Confidence + Low Suggestibility",
    "Low Confidence + High Suggestibility",
    "Low Confidence + Low Suggestibility",
]


def _collapse_volunteer_matrix(blocks: list[Block], chapter_num: int) -> list[Block]:
    if chapter_num != 11:
        return blocks
    out: list[Block] = []
    i = 0
    n = len(blocks)
    while i < n:
        b = blocks[i]
        if b.kind in ("para", "subhead") and b.text.strip() == MATRIX_QUADRANTS[0]:
            # Collect the 4 quadrants × (header, badge, description).
            cells: list[tuple[str, str, str]] = []
            j = i
            for _ in range(4):
                if j + 2 >= n:
                    break
                hdr = blocks[j].text.strip() if blocks[j].kind in ("para", "subhead") else ""
                badge = blocks[j+1].text.strip() if blocks[j+1].kind in ("para", "subhead") else ""
                desc = blocks[j+2].text.strip() if blocks[j+2].kind in ("para", "subhead") else ""
                if hdr in MATRIX_QUADRANTS:
                    cells.append((hdr, badge, desc))
                    j += 3
                else:
                    break
            if len(cells) == 4:
                mb = Block(kind="matrix2x2")
                mb.rows = [list(c) for c in cells]
                out.append(mb)
                i = j
                continue
        out.append(b)
        i += 1
    return out


# ── Generic named-card lists ──
# When a chapter has a sequence of (Title-case-name, body-paragraph) pairs,
# render them as a card grid.  We trigger these on specific known section
# titles to avoid false positives.

NAMED_CARD_LISTS = {
    # chapter -> (trigger_subhead_lower, list_of_card_names, output_caption)
    4:  ("the five forces", ["Novelty", "Emotional Relevance", "Social Signal", "Unresolved Uncertainty", "Contrast"], "five-forces"),
    5:  None,  # CH 5 has two structures — handled separately below
    7:  ("the three concepts", ["The Octopus Principle", "Change Blindness", "System 2 Load"], "concepts"),
    8:  ("common observer errors", ["Acting on a Single Signal", "Ignoring Baseline", "Confirmation Bias", "Cultural Projection"], "observer-errors"),
    10: ("the four personalities", ["The Dominant", "The Influencer", "The Steady", "The Compliant"], "disc"),
    21: ("the thirteen forces", None, "psychological-forces"),  # auto-detect by all-caps titles
}


def _collapse_named_card_lists(blocks: list[Block], chapter_num: int) -> list[Block]:
    """Look for a sequence of (CardName, body-para) pairs anywhere in the chapter
    and convert them to a card grid.  We don't require a specific trigger —
    just look for 3+ consecutive pairs where the title is short Title Case (not
    all-caps subhead noise) and the body is a real paragraph."""
    out: list[Block] = []
    i = 0
    n = len(blocks)

    # Names that should NOT trigger card-title detection (they're callouts /
    # author voice / running headers).
    skip_as_title = {
        "chris michael's take", "chris michael’s take",
        "chris michael's note", "chris michael’s note",
        "if you remember nothing else",
        "key principle", "key concept",
        "the bottom line", "the truth",
        "performer's note", "performer’s note",
        "what to say", "what you say",
        "what it feels like",
    }

    def looks_like_card_title(b: Block) -> bool:
        if b.kind not in ("para", "subhead"):
            return False
        t = b.text.strip()
        if not t or len(t) > 60 or len(t) < 3:
            return False
        if t.endswith((".", ",", ":", "?", "!")):
            return False
        if t.lower() in skip_as_title:
            return False
        # Skip strings that contain T1/T2/T3/T4 fragments — these are tier-coded leftovers
        if re.search(r"\bT[1-4]\b", t):
            return False
        words = t.split()
        if len(words) < 2 or len(words) > 8:
            return False
        if t.isupper():
            return False
        if not t[0].isupper():
            return False
        return True

    while i < n:
        # Look ahead for a run of (title, body, title, body, ...)
        run = []
        j = i
        while j + 1 < n:
            t_b = blocks[j]
            b_b = blocks[j + 1]
            if (looks_like_card_title(t_b)
                    and b_b.kind == "para"
                    and len(b_b.text.strip()) >= 60
                    and not looks_like_card_title(b_b)):
                run.append((t_b.text.strip(), b_b.text.strip()))
                j += 2
                continue
            break
        if len(run) >= 3:
            cb = Block(kind="type_cards")
            cb.caption = "auto"
            cb.rows = [[name, body, [], "", ""] for name, body in run]
            out.append(cb)
            i = j
            continue
        out.append(blocks[i])
        i += 1
    return out


# ── Micro-Expression Matrix (Ch 14) ──
MICRO_EXPRESSIONS = ["Anger", "Contempt", "Disgust", "Fear", "Happiness", "Sadness", "Surprise"]


def _collapse_micro_expression_matrix(blocks: list[Block], chapter_num: int) -> list[Block]:
    if chapter_num != 14:
        return blocks
    out: list[Block] = []
    i = 0
    n = len(blocks)
    while i < n:
        b = blocks[i]
        if b.kind in ("para", "subhead") and b.text.strip() in MICRO_EXPRESSIONS:
            entries: list[tuple[str, str]] = []
            j = i
            while j < n:
                tb = blocks[j]
                if tb.kind not in ("para", "subhead"):
                    break
                if tb.text.strip() not in MICRO_EXPRESSIONS:
                    break
                name = tb.text.strip()
                # collect description paragraphs until next expression name or non-para
                desc_parts: list[str] = []
                k = j + 1
                while k < n:
                    nxt = blocks[k]
                    if nxt.kind != "para":
                        break
                    if nxt.text.strip() in MICRO_EXPRESSIONS:
                        break
                    desc_parts.append(nxt.text.strip())
                    k += 1
                entries.append((name, "\n\n".join(desc_parts)))
                j = k
            if len(entries) >= 4:
                eb = Block(kind="expression_table")
                eb.rows = [list(e) for e in entries]
                out.append(eb)
                i = j
                continue
        out.append(b)
        i += 1
    return out


_ARABIC_RE = re.compile(r"^(\d{1,2})$")


def _is_numbered_marker(b: Block) -> str | None:
    if b.kind not in ("para", "subhead"):
        return None
    m = _ARABIC_RE.match(b.text.strip())
    return m.group(1) if m else None


def _collapse_numbered_cards(blocks: list[Block]) -> list[Block]:
    """Detect (Arabic number, name, body) ×N pattern and render as numbered cards.
    Pattern matches the Five Forces of Attention layout in CH 4 and similar.
    Requires N >= 3 to avoid false positives (e.g. random '1' in narrative)."""
    out: list[Block] = []
    i = 0
    n = len(blocks)
    while i < n:
        b = blocks[i]
        num = _is_numbered_marker(b)
        if num is not None:
            entries: list[tuple[str, str, str]] = []
            j = i
            while j + 2 < n:
                m = _is_numbered_marker(blocks[j])
                if m is None:
                    break
                name = blocks[j + 1].text.strip() if blocks[j + 1].kind in ("para", "subhead") else ""
                body = blocks[j + 2].text.strip() if blocks[j + 2].kind == "para" else ""
                if not name or len(name) > 60 or name.endswith((".", ",")):
                    break
                if len(body) < 80:
                    break
                entries.append((m, name, body))
                j += 3
            if len(entries) >= 3:
                pb = Block(kind="pillars")
                pb.rows = [[num_, name, "", body] for (num_, name, body) in entries]
                pb.caption = "numbered"
                out.append(pb)
                i = j
                continue
        out.append(b)
        i += 1
    return out


_METHOD_NUM_NAME_RE = re.compile(r"^(\d{2})\s*(?:—\s*)?(.+)$")
_METHOD_WHEN_RE     = re.compile(r"^WHEN\s+(.+)$")


def _collapse_method_cards(blocks: list[Block]) -> list[Block]:
    """Detect (num+name, WHEN trigger, body) ×N pattern and render as method
    cards.  Targets things like CH 5's Cortisol Window Recovery Methods:
        '01 — The Reflect and Reset'
        'WHEN The room is leaning back...'
        '<long body>'
    """
    out: list[Block] = []
    i = 0
    n = len(blocks)
    while i < n:
        b = blocks[i]
        if b.kind != "para":
            out.append(b)
            i += 1
            continue
        m = _METHOD_NUM_NAME_RE.match(b.text.strip())
        if not m:
            out.append(b)
            i += 1
            continue

        # Try to collect at least 2 (num+name, WHEN, body) triplets.
        entries: list[tuple[str, str, str, str]] = []
        j = i
        while j + 2 < n:
            if blocks[j].kind != "para":
                break
            mm = _METHOD_NUM_NAME_RE.match(blocks[j].text.strip())
            if not mm:
                break
            num, name = mm.group(1), mm.group(2).strip()
            if not (3 < len(name) <= 60) or name.endswith((".", ",")):
                break
            if blocks[j + 1].kind != "para":
                break
            wm = _METHOD_WHEN_RE.match(blocks[j + 1].text.strip())
            if not wm:
                break
            trigger = wm.group(1).strip()
            if blocks[j + 2].kind != "para":
                break
            body = blocks[j + 2].text.strip()
            if len(body) < 60:
                break
            entries.append((num, name, trigger, body))
            j += 3

        if len(entries) >= 2:
            mc = Block(kind="method_cards")
            mc.rows = [list(e) for e in entries]
            out.append(mc)
            i = j
            continue
        out.append(b)
        i += 1
    return out


def _collapse_preview_list(blocks: list[Block]) -> list[Block]:
    """Detect a paragraph that contains a smashed-together TitleCase list of
    items separated by NEWLINES (not arbitrary whitespace).  These show up
    in the source where the manuscript intended a bullet list — e.g. CH 4's
    Five Forces preview ('Novelty\\nEmotional Relevance\\nSocial Signal\\n
    Unresolved Uncertainty\\nContrast').

    Strict rules to avoid false positives:
      - Paragraph must contain at least 2 newlines (3+ items).
      - Each item must be ≤ 4 words.
      - Each item must start with a capital letter.
      - No item ends in terminal punctuation.
      - Total length ≤ 200 chars.
    """
    out: list[Block] = []
    SPLIT_NL = re.compile(r"\n+")
    for b in blocks:
        if b.kind != "para":
            out.append(b)
            continue
        t = b.text
        if not t or "\n" not in t or len(t.strip()) > 200:
            out.append(b)
            continue
        items = [s.strip() for s in SPLIT_NL.split(t) if s.strip()]
        if not (3 <= len(items) <= 10):
            out.append(b)
            continue
        if not all(
            it and it[0].isupper()
            and not it.endswith((".", "!", "?", ","))
            and 1 <= len(it.split()) <= 4
            for it in items
        ):
            out.append(b)
            continue
        pl = Block(kind="preview_list")
        pl.rows = [[it] for it in items]
        out.append(pl)
    return out


def _collapse_pillars_and_levels(blocks: list[Block]) -> list[Block]:
    """Walk the block stream and find runs of (Roman, Name, Tagline, Body) → Pillars,
    or (Level N, Name, Description) → Levels. Replace each run with one structured block.
    """
    out: list[Block] = []
    i = 0
    while i < len(blocks):
        b = blocks[i]

        # Try to start a Pillars run: (Roman, Title-case name, tagline, body) ×N
        roman = _is_pillar_marker(b)
        if roman is not None and i + 3 < len(blocks):
            entries: list[tuple[str, str, str, str]] = []
            j = i
            while j + 3 < len(blocks):
                r = _is_pillar_marker(blocks[j])
                if r is None:
                    break
                name = blocks[j + 1].text.strip() if blocks[j + 1].kind in ("para", "subhead") else ""
                tag  = blocks[j + 2].text.strip() if blocks[j + 2].kind in ("para", "subhead") else ""
                body = blocks[j + 3].text.strip() if blocks[j + 3].kind in ("para", "subhead") else ""
                # name should be a Title Case word, no terminal punctuation
                if not name or len(name) > 50 or name.endswith(("."  , ",")):
                    break
                entries.append((r, name, tag, body))
                j += 4
            if len(entries) >= 3:
                pb = Block(kind="pillars")
                pb.rows = [list(e) for e in entries]
                out.append(pb)
                i = j
                continue

        # Try to start a Levels run: (Level N, Name, Description) ×N
        lvl = _is_level_marker(b)
        if lvl is not None and i + 2 < len(blocks):
            entries2: list[tuple[str, str, str]] = []
            j = i
            while j + 2 < len(blocks):
                ln = _is_level_marker(blocks[j])
                if ln is None:
                    break
                name = blocks[j + 1].text.strip() if blocks[j + 1].kind == "para" else ""
                desc = blocks[j + 2].text.strip() if blocks[j + 2].kind == "para" else ""
                if not name or len(name) > 40:
                    break
                entries2.append((ln, name, desc))
                j += 3
            if len(entries2) >= 3:
                lb = Block(kind="levels")
                lb.rows = [list(e) for e in entries2]
                out.append(lb)
                i = j
                continue

        out.append(b)
        i += 1
    return out


def parse_docx(path: Path) -> tuple[list[Chapter], list[Part], dict]:
    """Walk the DOCX paragraphs and produce a clean ordered list of chapters
    (some labeled with which Part they belong to)."""
    doc = Document(str(path))

    chapters: list[Chapter] = []
    parts: list[Part] = []
    front_acknowledgments: list[Block] = []
    front_how_to_read: list[Block] = []

    cur_chapter: Chapter | None = None
    cur_part_idx: int | None = None
    cur_chapter_num = 0  # auto-increment for numbered chapters
    in_toc = False
    in_acknowledgments = False
    in_how_to_read = False
    skip_to_next_h1 = False  # used to drop repeated cover material between ack and Ch 1
    pending_dropcap: str | None = None
    pending_number: str | None = None  # buffered standalone digit awaiting context decision
    promoted_unstyled: set[str] = set()
    expecting_epigraph = False
    # 80-Signal-System collection state
    collecting_signals = False
    signal_rows: list[tuple[str, str, str, str, str]] = []
    # Callout collection state
    pending_callout: tuple[str, str] | None = None  # (variant_class, label_text)
    # T4 panel collection state
    in_t4_section = False
    cur_t4: Block | None = None
    pending_t4_field: str | None = None  # 'claim' | 'research' | 'valid'

    def push_block(b: Block) -> None:
        nonlocal cur_chapter
        if in_acknowledgments:
            front_acknowledgments.append(b)
        elif in_how_to_read:
            front_how_to_read.append(b)
        elif cur_chapter is not None:
            cur_chapter.blocks.append(b)

    def flush_dropcap_into(text: str) -> str:
        nonlocal pending_dropcap
        if pending_dropcap is None:
            return text
        merged = merge_dropcap(pending_dropcap, text)
        pending_dropcap = None
        return merged

    def iter_body_content(document):
        """Yield (kind, element) pairs in document order. kind in {'para','table'}."""
        body = document.element.body
        for child in body.iterchildren():
            if child.tag == qn("w:p"):
                yield ("para", DocxParagraph(child, document))
            elif child.tag == qn("w:tbl"):
                yield ("table", DocxTable(child, document))

    def extract_table_rows(tbl: DocxTable) -> list[list[str]]:
        rows = []
        for row in tbl.rows:
            cells = []
            for c in row.cells:
                # join paragraphs in cell with newlines, then strip
                txt = "\n".join(p.text for p in c.paragraphs).strip()
                cells.append(txt)
            rows.append(cells)
        return rows

    for kind, item in iter_body_content(doc):
        if kind == "table":
            rows = extract_table_rows(item)
            if not rows or all(not any(c for c in r) for r in rows):
                continue
            # Skip TOC-side tables that might be pure layout (rare)
            block = Block("table", rows=rows)
            push_block(block)
            continue

        # kind == "para"
        p = item
        style = p.style.name if p.style else ""
        raw = p.text
        # If this paragraph has a callout label glued onto its end (e.g.
        # "...thing to engineer.\n\nKEY PRINCIPLE"), split it: emit the
        # prose as a normal paragraph and arm pending_callout for the next
        # paragraph to become the callout body.
        prose, trailing_label = split_trailing_callout_label(raw)
        if trailing_label is not None and prose:
            # push the prose first, like a normal paragraph would be processed
            cleaned_prose = repair_text(prose)
            if cleaned_prose:
                push_block(Block("para", cleaned_prose))
            if trailing_label in CALLOUT_LABELS:
                pending_callout = CALLOUT_LABELS[trailing_label]
            continue
        text = repair_text(raw.strip())

        # ── front-matter modal sections ──
        if in_toc:
            if style in ("Heading 1", "Heading 2"):
                in_toc = False
            else:
                continue

        # Heading 2 transitions
        if style == "Heading 2":
            low = text.lower()
            if low == "contents":
                in_toc = True
                continue
            if low == "how to read this book":
                # finish any current section
                in_acknowledgments = False
                in_how_to_read = True
                cur_chapter = None
                continue
            if low == "acknowledgments":
                in_how_to_read = False
                in_acknowledgments = True
                cur_chapter = None
                continue
            # Misc H2 inside chapters → treat as subhead
            if cur_chapter is not None and text:
                push_block(Block("subhead", text))
            continue

        if style == "Heading 3":
            if text and not is_junk(text) and (
                cur_chapter is not None or in_how_to_read or in_acknowledgments
            ):
                push_block(Block("subhead", text))
            continue

        if style == "Heading 1":
            in_acknowledgments = False
            in_how_to_read = False
            skip_to_next_h1 = False
            pending_dropcap = None
            pending_number = None  # drop unconfirmed numbers when chapter changes
            # Close any open T4 panel before changing chapters.
            if cur_t4 is not None:
                push_block(cur_t4)
                cur_t4 = None
            in_t4_section = False
            pending_t4_field = None
            pending_callout = None
            collecting_signals = False
            if signal_rows:
                block = Block(kind="table")
                block.rows = [["#", "Observation", "What It Tells You", "Tier", "Use"]]
                for r in signal_rows:
                    block.rows.append(list(r))
                block.caption = "signal-table"
                push_block(block)
                signal_rows = []

            if text in CORRUPTED_H1_FIXUPS:
                text = CORRUPTED_H1_FIXUPS[text]
            if not text or text == "sw":
                continue

            # Is this a Part divider?
            matched_part = None
            for pt in PART_TITLES:
                if text == pt:
                    matched_part = pt
                    break
            if matched_part is not None:
                idx = len(parts) + 1
                ordinal = PART_ORDINALS[idx - 1]
                parts.append(Part(index=idx, ordinal=ordinal, title=matched_part))
                cur_part_idx = idx - 1
                cur_chapter = None
                expecting_epigraph = False
                continue

            # Is this a special non-chapter H1 (Meta Reveal / Controlling The Room interlude)?
            if text in SPECIAL_H1:
                kind, label_text = SPECIAL_H1[text]
                ch = Chapter(
                    number=0,
                    title=text,
                    part_index=cur_part_idx,
                    interlude=True,
                    label=label_text or kind.upper(),
                )
                chapters.append(ch)
                cur_chapter = ch
                expecting_epigraph = True
                continue

            # Otherwise: a regular numbered chapter
            cur_chapter_num += 1
            ch = Chapter(
                number=cur_chapter_num,
                title=text,
                part_index=cur_part_idx,
                label=f"Chapter {cur_chapter_num}",
            )
            chapters.append(ch)
            cur_chapter = ch
            expecting_epigraph = True
            continue

        # ── body / normal paragraphs ──
        if not text:
            continue

        # If we're in skip-to-next-H1 mode (triggered by repeated cover
        # material after acknowledgments), drop everything until the next H1.
        if skip_to_next_h1:
            continue

        # Sentinel: end acknowledgments + start skipping when we hit the
        # repeated cover-page material.  The first H1 (Ch 1) will reset.
        if in_acknowledgments and text.strip() in ("VANISHING INC.", "VANISHING INC", "BUILT"):
            in_acknowledgments = False
            skip_to_next_h1 = True
            continue

        # Promote unstyled chapter titles
        if text in UNSTYLED_CHAPTER_TITLES and text not in promoted_unstyled:
            promoted_unstyled.add(text)
            cur_chapter_num += 1
            ch = Chapter(
                number=cur_chapter_num,
                title=text,
                part_index=cur_part_idx,
                label=f"Chapter {cur_chapter_num}",
            )
            chapters.append(ch)
            cur_chapter = ch
            expecting_epigraph = True
            continue

        # 80-Signal table collection (only inside CH 9)
        if cur_chapter is not None and cur_chapter.number == 9:
            # Header line that announces the table
            if not collecting_signals and text.strip() == "#OBSERVATIONWHAT IT TELLS YOUTIERUSE":
                collecting_signals = True
                signal_rows = []
                continue
            if collecting_signals:
                row = _try_split_signal_row(text)
                if row is not None:
                    signal_rows.append(row)
                    continue
                # Stop collecting — flush the rows as a table block, then fall through
                if signal_rows:
                    block = Block(kind="table")
                    block.rows = [["#", "Observation", "What It Tells You", "Tier", "Use"]]
                    for r in signal_rows:
                        block.rows.append(list(r))
                    block.caption = "signal-table"  # marker for renderer
                    push_block(block)
                signal_rows = []
                collecting_signals = False
                # fall through to handle this line normally

        # Filter junk
        if is_junk(text):
            continue

        # Bare-number paragraph: could be a page-chrome number OR a list
        # marker.  Buffer it; the next paragraph decides.
        if PAGE_NUM_RE.match(text):
            pending_number = text
            continue
        # If we have a pending number, this paragraph is the lookahead.
        if pending_number is not None:
            buffered = pending_number
            pending_number = None
            stripped = text.strip()
            looks_like_list_item_title = (
                stripped
                and stripped[0].isupper()
                and 1 <= len(stripped.split()) <= 5
                and not stripped.endswith((".", ",", ":", "?", "!"))
                and len(stripped) <= 60
            )
            if looks_like_list_item_title:
                # Push the buffered number as its own paragraph so the
                # numbered-cards detector can pair it with this title and the
                # following body.
                push_block(Block("para", buffered))
            # else: drop the buffered number — it was page chrome.


        # Section divider
        if is_section_break(text):
            push_block(Block("break"))
            continue

        # Hook quote sits right under the title — first non-junk line after H1
        if expecting_epigraph and cur_chapter is not None:
            # An epigraph is typically a quoted line; accept any short line as the epigraph.
            stripped_quotes = text.strip("“”‘’\"' ")
            cur_chapter.epigraph = stripped_quotes
            expecting_epigraph = False
            continue

        # Drop cap accumulator
        if pending_dropcap is not None:
            merged = merge_dropcap(pending_dropcap, text)
            if merged is None:
                # Not actually a drop cap — push the letter as its own paragraph
                # so downstream detectors (pillars, levels) can see Roman numerals.
                push_block(Block("para", pending_dropcap))
                pending_dropcap = None
                # fall through to process this paragraph normally
            else:
                pending_dropcap = None
                push_block(Block("para", merged))
                continue

        if DROPCAP_RE.match(text):
            pending_dropcap = text
            continue

        # ── T4 section opener (case-insensitive, runs before subhead check) ──
        if cur_chapter is not None and cur_chapter.number == 9:
            tlow = text.strip().lower()
            if tlow == "t4 signals removed" and not in_t4_section:
                in_t4_section = True
                cur_t4 = None
                push_block(Block("subhead", "T4 Signals Removed — and What Remains Valid"))
                continue
            # Exit T4 mode when the radar / scan sections begin.
            if in_t4_section and tlow in (
                "the six-category radar",
                "the 10-second scan",
                "the ten-second scan",
                "performer's note",
                "performer’s note",
            ):
                if cur_t4 is not None:
                    push_block(cur_t4)
                    cur_t4 = None
                in_t4_section = False
                pending_t4_field = None
                push_block(Block("subhead", text.strip()))
                continue

        # T4 sub-section labels (THE CLAIM / THE RESEARCH / WHAT REMAINS VALID)
        if in_t4_section and cur_t4 is not None:
            up = text.strip().upper()
            if up in {"THE CLAIM", "THE RESEARCH", "WHAT REMAINS VALID"}:
                pending_t4_field = {
                    "THE CLAIM": "claim",
                    "THE RESEARCH": "research",
                    "WHAT REMAINS VALID": "valid",
                }[up]
                continue

        # T4 panel title detection: paragraph that starts with "T4" followed by a title
        if in_t4_section and text.startswith("T4") and len(text) > 3 and text[2] != " ":
            # finalize prior panel
            if cur_t4 is not None:
                push_block(cur_t4)
            title = text[2:].strip()
            cur_t4 = Block(kind="t4_panel", title=title)
            pending_t4_field = None
            continue

        # T4 collection: feed paragraphs into the active field
        if in_t4_section and cur_t4 is not None and pending_t4_field is not None:
            existing = getattr(cur_t4, pending_t4_field) or ""
            new = (existing + ("\n\n" if existing else "") + text).strip()
            setattr(cur_t4, pending_t4_field, new)
            continue

        # All-caps short line — could be a callout label, a T4-section opener, or a subhead.
        if looks_like_subhead(text):
            up = text.strip().upper()
            # Callout label?  Pair with the NEXT paragraph as the callout body.
            if up in CALLOUT_LABELS:
                pending_callout = CALLOUT_LABELS[up]
                continue

        # Title Case callout labels (e.g. "Chris Michael's Take",
        # "Common Misread", "⚠ Common Misread") — case-insensitive lookup
        # with leading-symbol stripping (warning triangles, bullets, etc.).
        tc_text = text.strip().lstrip("⚠✦●•◆◇□■*†‡§◦› ").strip()
        if tc_text and tc_text.upper() in CALLOUT_LABELS and len(tc_text) <= 50:
            pending_callout = CALLOUT_LABELS[tc_text.upper()]
            continue
            # Enter T4 section?
            if up == "T4 SIGNALS REMOVED":
                in_t4_section = True
                cur_t4 = None
                # render the heading itself as a sub-section header so the section is visible
                push_block(Block("subhead", "T4 Signals Removed — and What Remains Valid"))
                continue
            # The "Six-Category Radar" subsection ends T4
            if up == "THE SIX-CATEGORY RADAR" and in_t4_section:
                if cur_t4 is not None:
                    push_block(cur_t4)
                    cur_t4 = None
                in_t4_section = False
                pending_t4_field = None
            push_block(Block("subhead", text))
            continue

        # If we have a pending callout, this paragraph IS the callout body.
        if pending_callout is not None:
            variant, label = pending_callout
            push_block(Block(kind="callout", text=text, caption=f"{variant}|{label}"))
            pending_callout = None
            continue

        # Figure-anchor injection: if this paragraph starts with a configured
        # anchor for the current chapter, push the figure block FIRST.
        if cur_chapter is not None and not cur_chapter.interlude:
            for anchor, src, caption, alt in FIGURES.get(cur_chapter.number, []):
                if text.startswith(anchor) and not any(
                    b.kind == "figure" and b.src == src for b in cur_chapter.blocks
                ):
                    push_block(Block(kind="figure", src=src, caption=caption, alt=alt))
                    break

        # Expert panel match (Colin Cloud / Anthem & Aria — branded callouts)
        expert = _expert_panel_match(text)
        if expert is not None:
            variant, label, subtitle = expert
            push_block(Block(kind="expert_panel", text=text, caption=f"{variant}|{label}|{subtitle}"))
            continue

        push_block(Block("para", text))

    # Post-pass on front matter: convert BP/CR/VS/AM letter+name+desc triplets
    # in the "Observation Categories" section into a styled category-card grid.
    front_how_to_read = _collapse_observation_category_cards(front_how_to_read)

    # Post-pass: collapse runs of paragraphs into structured widgets.
    for ch in chapters:
        ch.blocks = _dedupe_adjacent_paragraphs(ch.blocks)
        ch.blocks = _collapse_design_summary(ch.blocks)
        ch.blocks = _collapse_method_cards(ch.blocks)
        ch.blocks = _collapse_numbered_cards(ch.blocks)
        ch.blocks = _collapse_preview_list(ch.blocks)
        ch.blocks = _promote_title_case_subheads(ch.blocks)
        ch.blocks = _collapse_radar_and_scan(ch.blocks)
        ch.blocks = _collapse_pillars_and_levels(ch.blocks)
        ch.blocks = _collapse_volunteer_types(ch.blocks, ch.number)
        ch.blocks = _collapse_volunteer_matrix(ch.blocks, ch.number)
        ch.blocks = _collapse_observation_table(ch.blocks)
        ch.blocks = _collapse_ftf_flow(ch.blocks)
        ch.blocks = _collapse_flowchart(ch.blocks)
        ch.blocks = _collapse_named_card_lists(ch.blocks, ch.number)
        ch.blocks = _collapse_micro_expression_matrix(ch.blocks, ch.number)

    # Tie chapters into their parts (preserve order)
    for ch in chapters:
        if ch.part_index is not None and 0 <= ch.part_index < len(parts):
            parts[ch.part_index].chapters.append(ch)

    front = {
        "how_to_read": front_how_to_read,
        "acknowledgments": front_acknowledgments,
    }
    return chapters, parts, front


# ─────────────────────────────────────────────────────────────────────────────
# HTML rendering
# ─────────────────────────────────────────────────────────────────────────────

CSS = r"""
:root {
  --bg:        #FBF8F1;
  --bg-soft:   #F4EFE3;
  --ink:       #1B1B1B;
  --ink-soft:  #4A4742;
  --muted:     #847E72;
  --rule:      #DAD3C2;
  --accent:    #B65422;
  --accent-soft: #C97A50;
  --max:       38rem;       /* body column width */
  --max-wide:  56rem;       /* chapter opener / quote width */
  --serif:     "Source Serif 4", "Source Serif Pro", "Iowan Old Style", "Charter", Georgia, serif;
  --sans:      "Inter", system-ui, -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg:       #1A1815;
    --bg-soft:  #24201B;
    --ink:      #ECE6D8;
    --ink-soft: #C9C2B1;
    --muted:    #8C8676;
    --rule:     #3A352D;
    --accent:   #E08D5C;
    --accent-soft: #B65422;
  }
}

* { box-sizing: border-box; }

html, body {
  margin: 0;
  padding: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: var(--serif);
  font-size: 19px;
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}

a { color: var(--accent); text-decoration: none; border-bottom: 1px solid transparent; transition: border-color .15s; }
a:hover { border-color: var(--accent); }

/* ── layout shell ── */
.page {
  max-width: var(--max);
  margin: 0 auto;
  padding: clamp(2rem, 5vw, 4.5rem) clamp(1.25rem, 4vw, 2rem) 6rem;
}

.cover, .chapter-opener, .part-divider, .toc, .frontmatter {
  max-width: var(--max-wide);
  margin-left: auto;
  margin-right: auto;
}

/* ── cover / title slide ── */
.cover {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: stretch;
  text-align: left;
  padding: clamp(3rem, 8vh, 6rem) 0 clamp(3rem, 6vh, 4rem);
  position: relative;
}
.cover::after {
  /* faint baseline rule under the cover */
  content: "";
  position: absolute;
  left: 0; right: 0; bottom: 0;
  height: 1px;
  background: var(--rule);
}
.cover .imprint-top {
  font-family: var(--sans);
  font-size: .7rem;
  letter-spacing: .35em;
  text-transform: uppercase;
  color: var(--muted);
  margin: 0 0 clamp(2rem, 8vh, 5rem);
}
.cover h1 {
  font-family: var(--sans);
  font-weight: 800;
  font-size: clamp(3.4rem, 13vw, 8.5rem);
  line-height: .92;
  letter-spacing: -0.035em;
  margin: 0 0 1.5rem;
  color: var(--ink);
}
.cover h1 .line { display: block; }
.cover h1 .for { color: var(--accent); font-weight: 500; font-style: italic; }
.cover .subtitle {
  font-family: var(--serif);
  font-style: italic;
  font-size: clamp(1.05rem, 2vw, 1.3rem);
  color: var(--ink-soft);
  max-width: 40rem;
  margin: 0 0 clamp(2.5rem, 6vh, 4rem);
  line-height: 1.45;
}
.cover .author-block {
  border-top: 1px solid var(--rule);
  padding-top: 1.5rem;
}
.cover .author-name {
  font-family: var(--sans);
  font-weight: 700;
  font-size: 1.1rem;
  letter-spacing: .2em;
  text-transform: uppercase;
  color: var(--ink);
  margin: 0 0 .35rem;
}
.cover .author-role {
  font-family: var(--sans);
  font-weight: 400;
  font-size: .82rem;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: var(--muted);
  margin: 0;
}

/* ── hero quote (between cover and front matter) ── */
.hero-quote {
  padding: clamp(5rem, 14vh, 9rem) 0;
  border-bottom: 1px solid var(--rule);
}
.hero-quote blockquote {
  margin: 0;
  font-family: var(--serif);
  font-style: italic;
  font-weight: 400;
  font-size: clamp(1.4rem, 3.2vw, 2.2rem);
  line-height: 1.32;
  color: var(--ink);
  letter-spacing: -0.005em;
  border: 0;
  padding: 0;
  position: relative;
}
.hero-quote blockquote::before {
  content: "“";
  position: absolute;
  top: -.4em;
  left: -.55em;
  font-size: 4em;
  color: var(--accent);
  font-style: normal;
  line-height: 1;
  opacity: .35;
  font-family: var(--serif);
}
.hero-quote .attrib {
  margin: 1.5rem 0 0;
  font-family: var(--sans);
  font-size: .78rem;
  letter-spacing: .25em;
  text-transform: uppercase;
  color: var(--muted);
  font-weight: 600;
}

/* ── frontmatter divider ── */
.fm-divider {
  text-align: center;
  margin: clamp(4rem, 8vh, 6rem) auto 2rem;
}
.fm-divider .label {
  font-family: var(--sans);
  font-size: .72rem;
  letter-spacing: .45em;
  text-transform: uppercase;
  color: var(--accent);
  font-weight: 700;
  display: inline-block;
  padding: 0 1.25rem;
  background: var(--bg);
  position: relative;
  z-index: 1;
}
.fm-divider {
  position: relative;
}
.fm-divider::before {
  content: "";
  position: absolute;
  left: 0; right: 0; top: 50%;
  height: 1px;
  background: var(--rule);
  z-index: 0;
}

/* ── about the author ── */
.about-author {
  margin: 3rem auto 5rem;
  max-width: var(--max);
}
.about-author h2 {
  font-family: var(--sans);
  font-weight: 700;
  font-size: 1.5rem;
  letter-spacing: -0.01em;
  margin: 0 0 1.5rem;
  color: var(--ink);
}
.about-author p {
  margin: 0 0 1.1rem;
  color: var(--ink-soft);
  font-size: 1.02rem;
}
.about-author strong {
  font-weight: 600;
  color: var(--ink);
  /* tiny bg tint to make the credibility phrases visually 'earned' */
  background: linear-gradient(transparent 65%, color-mix(in srgb, var(--accent) 18%, transparent) 65%);
  padding: 0 .05em;
}

/* General strong styling for body prose — modest emphasis */
.chapter-body strong, .frontmatter strong {
  font-weight: 600;
  color: var(--ink);
}

/* ── frontmatter / how to read ── */
.frontmatter h2 {
  font-family: var(--sans);
  font-weight: 700;
  font-size: 1.6rem;
  letter-spacing: -0.01em;
  margin: 4.5rem 0 1.5rem;
  color: var(--ink);
}
.frontmatter p { margin: 0 0 1.1rem; }

/* ── TOC ── */
.toc { margin: 5rem auto 4rem; }
.toc h2 {
  font-family: var(--sans);
  font-weight: 700;
  font-size: 1.05rem;
  letter-spacing: .25em;
  text-transform: uppercase;
  color: var(--muted);
  margin: 0 0 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--rule);
}
.toc ol { list-style: none; padding: 0; margin: 0; counter-reset: chap; }
.toc .toc-part {
  font-family: var(--sans);
  font-size: .72rem;
  letter-spacing: .3em;
  text-transform: uppercase;
  color: var(--accent);
  margin: 2rem 0 .35rem;
  font-weight: 700;
}
.toc .toc-part .pt-title { color: var(--ink-soft); font-weight: 500; letter-spacing: .15em; margin-left: .8rem; }
.toc li.toc-row {
  display: flex;
  align-items: baseline;
  padding: .35rem 0;
  font-family: var(--serif);
  border-bottom: 1px dotted var(--rule);
}
.toc li.toc-row .num {
  font-family: var(--sans);
  font-variant-numeric: tabular-nums;
  font-size: .85rem;
  color: var(--muted);
  width: 2.5rem;
  flex-shrink: 0;
}
.toc li.toc-row .ttl { flex: 1; }
.toc li.toc-row a {
  color: var(--ink);
  border-bottom: 0;
}
.toc li.toc-row a:hover { color: var(--accent); }
.toc li.toc-row.interlude .num { color: var(--accent); }
.toc li.toc-row.interlude .ttl { font-style: italic; color: var(--ink-soft); }

/* ── part divider ── */
.part-divider {
  text-align: center;
  padding: 6rem 0 3rem;
  margin: 4rem auto;
  border-top: 1px solid var(--rule);
  border-bottom: 1px solid var(--rule);
}
.part-divider .eyebrow {
  font-family: var(--sans);
  font-size: .75rem;
  letter-spacing: .35em;
  text-transform: uppercase;
  color: var(--accent);
  font-weight: 700;
}
.part-divider .pt-title {
  font-family: var(--sans);
  font-weight: 200;
  font-size: clamp(2rem, 5vw, 3.4rem);
  letter-spacing: -0.01em;
  color: var(--ink);
  margin: 1rem 0 0;
  line-height: 1.1;
}

/* ── chapter opener ── */
.chapter {
  margin: 5rem auto;
  scroll-margin-top: 2rem;
}
.chapter-opener {
  border-top: 1px solid var(--rule);
  padding-top: 3rem;
  margin-bottom: 2.5rem;
}
.chapter-opener .eyebrow {
  font-family: var(--sans);
  font-size: .72rem;
  letter-spacing: .3em;
  text-transform: uppercase;
  color: var(--accent);
  font-weight: 700;
  margin: 0 0 1.25rem;
}
.chapter-opener h2.chapter-title {
  font-family: var(--sans);
  font-weight: 700;
  font-size: clamp(2rem, 4.5vw, 3rem);
  letter-spacing: -0.02em;
  line-height: 1.05;
  color: var(--ink);
  margin: 0 0 2rem;
}
.chapter-opener .epigraph {
  font-family: var(--serif);
  font-style: italic;
  font-size: 1.18rem;
  line-height: 1.5;
  color: var(--ink-soft);
  border-left: 2px solid var(--accent);
  padding: .25rem 0 .25rem 1.25rem;
  margin: 0 0 .5rem;
  max-width: 32rem;
}

/* chapter-opener symbol pill row */
.chapter-symbol-row {
  display: flex;
  gap: .4rem;
  align-items: center;
  margin: 0 0 1.5rem;
  flex-wrap: wrap;
}
.csym-pill {
  font-family: var(--sans);
  font-weight: 800;
  font-size: .68rem;
  letter-spacing: .12em;
  padding: .22rem .55rem;
  border-radius: 2px;
  color: var(--bg);
}
.csym-pill.tier-t1 { background: #2D7A3E; }
.csym-pill.tier-t2 { background: var(--accent); }
.csym-pill.tier-t3 { background: #8C5A2A; }
.csym-pill.tier-t4 { background: var(--muted); }
.csym-pill.cat-bp  { background: #2D7A3E; }
.csym-pill.cat-cr  { background: var(--accent); }
.csym-pill.cat-vs  { background: #6B86A6; }
.csym-pill.cat-am  { background: var(--muted); }

/* ── chapter body ── */
.chapter-body p {
  margin: 0 0 1.25rem;
  hyphens: auto;
}
.chapter-body p.lead { font-size: 1.05rem; }

/* drop cap on the first paragraph after the chapter header */
.chapter-body > p:first-of-type::first-letter {
  font-family: var(--serif);
  font-weight: 600;
  font-size: 4.2em;
  line-height: 0.85;
  float: left;
  margin: 0.08em 0.08em 0 0;
  color: var(--accent);
}

.chapter-body h3 {
  font-family: var(--sans);
  font-weight: 700;
  font-size: 1.18rem;
  letter-spacing: -0.005em;
  color: var(--ink);
  margin: 2.75rem 0 .75rem;
  padding-top: 1rem;
  border-top: 1px solid var(--rule);
  line-height: 1.25;
}
/* When the heading text is itself ALL-CAPS in the source, present it as
   the field-manual-style small-caps subsection label.  This catches things
   like "STAGE CONTEXT", "ACTING ON A SINGLE SIGNAL", etc., distinct from
   normal Title Case section headers. */
.chapter-body h3.allcaps {
  font-size: .82rem;
  letter-spacing: .22em;
  text-transform: uppercase;
  color: var(--accent);
  border-top: 0;
  padding-top: 0;
  margin: 2.5rem 0 .65rem;
}

.chapter-body hr.section-break {
  border: 0;
  text-align: center;
  margin: 2.5rem 0;
  height: 1.25rem;
  position: relative;
}
.chapter-body hr.section-break::before {
  content: "· · ·";
  display: inline-block;
  font-family: var(--serif);
  letter-spacing: .65em;
  color: var(--accent);
  font-size: 1rem;
}

.chapter-body blockquote {
  font-family: var(--serif);
  font-style: italic;
  font-size: 1.15rem;
  line-height: 1.5;
  color: var(--ink-soft);
  border-left: 2px solid var(--rule);
  margin: 2rem 0;
  padding: .25rem 0 .25rem 1.5rem;
}

/* ── figures ── */
.book-figure {
  margin: 2.5rem -1rem;
  text-align: center;
}
.book-figure img {
  display: block;
  width: 100%;
  max-width: 100%;
  height: auto;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0,0,0,.04), 0 4px 16px rgba(0,0,0,.06);
}
.book-figure figcaption {
  font-family: var(--sans);
  font-size: .82rem;
  letter-spacing: .02em;
  color: var(--muted);
  text-align: center;
  margin: .85rem auto 0;
  max-width: 32rem;
  line-height: 1.45;
  font-style: normal;
}
.book-figure figcaption strong {
  font-weight: 700;
  color: var(--accent);
  letter-spacing: .15em;
  text-transform: uppercase;
  font-size: .72rem;
}
@media (max-width: 700px) {
  .book-figure { margin: 2rem -.6rem; }
}

/* ── Observation Table (4-col) ── */
.obs-block {
  margin: 2.5rem -1.5rem;
  overflow-x: auto;
}
.tbl-obs {
  width: 100%;
  border-collapse: collapse;
  font-family: var(--sans);
}
.tbl-obs thead th {
  font-weight: 700;
  font-size: .65rem;
  letter-spacing: .2em;
  text-transform: uppercase;
  color: var(--accent);
  text-align: left;
  padding: .85rem 1rem .65rem;
  border-bottom: 1px solid var(--accent);
  vertical-align: bottom;
}
.tbl-obs tbody td {
  padding: 1rem;
  border-bottom: 1px solid var(--rule);
  vertical-align: top;
  font-size: .92rem;
  line-height: 1.45;
}
.tbl-obs .ot-c0 {
  font-weight: 600;
  color: var(--ink);
  width: 27%;
}
.tbl-obs .ot-c1 {
  color: var(--ink-soft);
  font-family: var(--serif);
  font-style: italic;
  width: 25%;
}
.tbl-obs .ot-c2 {
  color: var(--ink);
  width: 22%;
}
.tbl-obs .ot-c3 {
  font-weight: 700;
  color: var(--accent);
  text-align: center;
  width: 14rem;
  font-size: .88rem;
  letter-spacing: .03em;
}
.tbl-obs tbody tr:hover { background: rgba(182, 84, 34, 0.04); }

@media (max-width: 800px) {
  .obs-block { margin: 2rem -.5rem; }
  .tbl-obs { font-size: .85rem; }
  .tbl-obs td, .tbl-obs th { padding: .65rem .5rem; }
}

/* ── Observation Categories card grid (front matter) ── */
.category-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin: 1.5rem 0 2.5rem;
}
.cat-card {
  display: grid;
  grid-template-columns: 4rem 1fr;
  gap: 1rem;
  align-items: start;
  padding: 1.1rem 1.25rem;
  background: var(--bg-soft);
  border: 1px solid var(--rule);
  border-left: 4px solid var(--accent);
  border-radius: 0 4px 4px 0;
}
.cat-card.cat-bp { border-left-color: #2D7A3E; }
.cat-card.cat-cr { border-left-color: var(--accent); }
.cat-card.cat-vs { border-left-color: #6B86A6; }
.cat-card.cat-am { border-left-color: var(--muted); }
.cat-letter {
  font-family: var(--sans);
  font-weight: 800;
  font-size: 1.5rem;
  letter-spacing: .04em;
  text-align: center;
  padding: .35rem 0;
  border-radius: 3px;
  color: #fff;
}
.cat-card.cat-bp .cat-letter { background: #2D7A3E; }
.cat-card.cat-cr .cat-letter { background: var(--accent); }
.cat-card.cat-vs .cat-letter { background: #6B86A6; }
.cat-card.cat-am .cat-letter { background: var(--muted); }
.cat-name {
  font-family: var(--sans);
  font-weight: 700;
  font-size: 1rem;
  color: var(--ink);
  margin: 0 0 .35rem;
}
.cat-desc {
  font-family: var(--serif);
  font-size: .92rem;
  line-height: 1.5;
  color: var(--ink-soft);
  margin: 0;
}
@media (max-width: 700px) {
  .category-grid { grid-template-columns: 1fr; }
}

/* ── Branded expert panels (Colin Cloud, Anthem & Aria) ──
   Colors restored from the legacy designed build. These intentionally
   break out of the book's warm-cream palette to honor each contributor's
   own visual identity. */
.expert-panel {
  margin: 2rem 0;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 14px rgba(0,0,0,.08);
}
.ep-head {
  padding: .8rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}
.ep-label {
  font-family: var(--sans);
  font-size: .78rem;
  font-weight: 700;
  letter-spacing: .18em;
  text-transform: uppercase;
  color: #fff;
}
.ep-subtitle {
  font-family: var(--serif);
  font-size: .78rem;
  font-style: italic;
  color: rgba(255,255,255,.72);
  letter-spacing: .06em;
}
.ep-body {
  padding: 1rem 1.4rem;
  font-family: var(--serif);
  font-size: 1rem;
  line-height: 1.7;
}

/* Colin Cloud — forest-green Framework gradient */
.ep-colin-cloud {
  border: 1px solid rgba(30,100,60,.25);
  box-shadow: 0 4px 24px rgba(0,0,0,.1), 0 1px 4px rgba(31,107,58,.12);
}
.ep-colin-cloud .ep-head {
  background: linear-gradient(105deg, #1A5C2A 0%, #266B3B 45%, #6B8A90 78%, #A8BFC4 100%);
}
.ep-colin-cloud .ep-body {
  background: #F2F9F4;
  border-left: 4px solid #1F6B38;
  color: #1A1A1A;
}

/* Anthem & Aria — rose-to-blue Field Advice gradient */
.ep-anthem-aria {
  border: 1px solid rgba(176,96,130,.25);
}
.ep-anthem-aria .ep-head {
  background: linear-gradient(90deg, #B05878 0%, #4A7EA8 100%);
}
.ep-anthem-aria .ep-body {
  background: #FDF5F9;
  color: #1F1F1F;
  font-size: .98rem;
}

@media (prefers-color-scheme: dark) {
  .ep-colin-cloud .ep-body {
    background: #102A1B;
    color: #E5EFE3;
    border-left-color: #4FA868;
  }
  .ep-anthem-aria .ep-body {
    background: #2A1A22;
    color: #F0E0E8;
  }
}

@media (max-width: 600px) {
  .ep-head { flex-wrap: wrap; gap: .35rem 1rem; }
  .ep-body { padding: .85rem 1.1rem; font-size: .96rem; }
}

/* ── Fruit to Fang flowchart (CH 13) ── */
.ftf-flow {
  margin: 2.5rem -1rem;
  background: var(--bg-soft);
  border: 1px solid var(--rule);
  border-left: 4px solid var(--accent);
  border-radius: 0 6px 6px 0;
  padding: 1.75rem;
}
.ftf-flow-title {
  font-family: var(--sans);
  font-weight: 800;
  font-size: .68rem;
  letter-spacing: .3em;
  text-transform: uppercase;
  color: var(--accent);
  text-align: center;
  margin: 0 0 1.5rem;
}
.ftf-flow-body {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: .55rem;
}
.ftf-node {
  background: var(--bg);
  border: 1px solid var(--rule);
  border-radius: 4px;
  padding: .7rem 1.1rem;
  font-family: var(--sans);
  font-size: .92rem;
  color: var(--ink);
  text-align: center;
  max-width: 30rem;
}
.ftf-node-start {
  background: color-mix(in srgb, var(--accent) 12%, var(--bg));
  border-color: var(--accent);
  font-weight: 700;
}
.ftf-node-test {
  background: color-mix(in srgb, #6B86A6 10%, var(--bg));
  border-color: #6B86A6;
  font-style: italic;
}
.ftf-node-note {
  background: color-mix(in srgb, var(--muted) 8%, var(--bg));
  border-color: var(--muted);
  font-size: .88rem;
  display: flex;
  flex-direction: column;
  gap: .25rem;
}
.ftf-arrow {
  color: var(--accent);
  font-size: 1.15rem;
  line-height: 1;
  font-weight: 700;
}
.ftf-branch {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 1rem;
  width: 100%;
  align-items: stretch;
  max-width: 40rem;
}
.ftf-branch-item {
  background: var(--bg);
  border: 1px solid var(--rule);
  border-radius: 4px;
  padding: .85rem 1rem;
  display: flex;
  flex-direction: column;
  gap: .25rem;
  font-family: var(--sans);
  font-size: .82rem;
  color: var(--ink);
  text-align: center;
}
.ftf-branch-item strong {
  font-weight: 700;
  color: var(--ink);
  font-size: .9rem;
}
.ftf-yes { border-left: 3px solid #2D7A3E; }
.ftf-no  { border-left: 3px solid #6B86A6; }
.ftf-branch-mid {
  font-family: var(--sans);
  font-weight: 800;
  font-size: .65rem;
  letter-spacing: .2em;
  text-transform: uppercase;
  color: var(--muted);
  align-self: center;
  white-space: nowrap;
  padding: 0 .5rem;
}
.ftf-note {
  font-style: italic;
  color: var(--muted);
  font-size: .78rem;
  font-family: var(--serif);
}
.ftf-vowel {
  color: var(--accent);
  font-weight: 800;
  letter-spacing: .03em;
}
@media (max-width: 700px) {
  .ftf-branch { grid-template-columns: 1fr; gap: .5rem; }
  .ftf-branch-mid { padding: .35rem 0; border-top: 1px dashed var(--rule); border-bottom: 1px dashed var(--rule); }
}

/* ── Flowchart ── */
.flowchart {
  margin: 2.5rem -1rem;
  background: var(--bg-soft);
  border: 1px solid var(--rule);
  border-radius: 6px;
  padding: 2rem 1.75rem;
}
.fc-title {
  font-family: var(--sans);
  font-weight: 800;
  font-size: .68rem;
  letter-spacing: .3em;
  text-transform: uppercase;
  color: var(--accent);
  text-align: center;
  margin: 0 0 1.75rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--rule);
}
.fc-steps {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 0;
}
.fc-step {
  display: grid;
  grid-template-columns: 3.25rem 1fr;
  gap: 1.25rem;
  position: relative;
  padding: 0 0 1.5rem;
  align-items: start;
}
.fc-step:not(:last-child)::before {
  content: "";
  position: absolute;
  left: 1.55rem;
  top: 3rem;
  bottom: 0;
  width: 2px;
  background: var(--accent);
  opacity: .35;
}
.fc-step:not(:last-child)::after {
  content: "↓";
  position: absolute;
  left: 1.05rem;
  bottom: .3rem;
  color: var(--accent);
  font-size: 1rem;
  font-weight: 700;
}
.fc-num {
  font-family: var(--sans);
  font-weight: 800;
  font-variant-numeric: tabular-nums;
  font-size: .75rem;
  color: var(--bg);
  background: var(--accent);
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  letter-spacing: .04em;
  position: relative;
  z-index: 1;
}
.fc-card {
  background: var(--bg);
  border: 1px solid var(--rule);
  border-radius: 4px;
  padding: .85rem 1.1rem;
}
.fc-head {
  font-family: var(--sans);
  font-weight: 600;
  font-size: 1rem;
  color: var(--ink);
  line-height: 1.4;
}
.fc-detail {
  list-style: none;
  padding: 0;
  margin: .65rem 0 0;
  border-top: 1px dotted var(--rule);
  padding-top: .55rem;
}
.fc-detail li {
  font-family: var(--serif);
  font-size: .9rem;
  color: var(--ink-soft);
  padding: .25rem 0;
  line-height: 1.45;
  position: relative;
  padding-left: 1rem;
}
.fc-detail li::before {
  content: "›";
  color: var(--accent);
  position: absolute;
  left: 0;
  font-weight: 700;
}

/* ── generic Type Cards ── */
.type-cards {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.25rem;
  margin: 2.5rem -1rem;
}
.type-cards-volunteer {
  grid-template-columns: 1fr 1fr;
}
.type-card {
  background: var(--bg-soft);
  border: 1px solid var(--rule);
  border-left: 4px solid var(--accent);
  border-radius: 0 4px 4px 0;
  padding: 1.4rem 1.5rem 1.5rem;
}
.tc-name {
  font-family: var(--sans);
  font-weight: 700;
  font-size: 1.2rem;
  letter-spacing: -0.005em;
  color: var(--ink);
  margin: 0 0 .55rem;
}
.tc-desc {
  font-family: var(--serif);
  font-size: 1rem;
  line-height: 1.55;
  color: var(--ink-soft);
  margin: 0 0 1rem;
}
.tc-tells {
  list-style: none;
  padding: 0;
  margin: 0 0 1rem;
  border-top: 1px dotted var(--rule);
}
.tc-tells li {
  font-family: var(--sans);
  font-size: .85rem;
  color: var(--ink);
  padding: .5rem 0 .5rem 1.5rem;
  border-bottom: 1px dotted var(--rule);
  position: relative;
  line-height: 1.4;
}
.tc-tells li::before {
  content: "›";
  color: var(--accent);
  font-weight: 700;
  position: absolute;
  left: 0;
}
.tc-meta {
  display: flex;
  flex-direction: column;
  gap: .55rem;
  font-family: var(--sans);
  font-size: .87rem;
  border-top: 1px dotted var(--rule);
  padding-top: .85rem;
}
.tc-meta-row {
  display: grid;
  grid-template-columns: 5.5rem 1fr;
  gap: .85rem;
  align-items: baseline;
}
.tc-meta-label {
  font-weight: 700;
  font-size: .65rem;
  letter-spacing: .2em;
  text-transform: uppercase;
}
.tc-good { color: #2D7A3E; }
.tc-warn { color: #B53030; }
.tc-meta-text {
  color: var(--ink-soft);
  line-height: 1.45;
  font-family: var(--serif);
  font-size: .95rem;
}
@media (max-width: 800px) {
  .type-cards-volunteer { grid-template-columns: 1fr; }
  .type-cards { margin: 2rem 0; }
}

/* ── 2x2 Matrix ── */
.matrix2x2 {
  margin: 2.5rem -1rem;
  position: relative;
}
.m22-axes {
  position: relative;
  height: 0;
}
.m22-axis-y, .m22-axis-x {
  position: absolute;
  font-family: var(--sans);
  font-weight: 700;
  font-size: .65rem;
  letter-spacing: .25em;
  text-transform: uppercase;
  color: var(--accent);
}
.m22-axis-y {
  top: 1rem;
  left: -1rem;
  transform: rotate(-90deg);
  transform-origin: left top;
}
.m22-axis-x {
  bottom: -2rem;
  left: 50%;
  transform: translateX(-50%);
}
.m22-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
  border: 1px solid var(--rule);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 2rem;
}
.m22-cell {
  padding: 1.5rem 1.4rem;
  background: var(--bg);
  border-right: 1px solid var(--rule);
  border-bottom: 1px solid var(--rule);
  display: flex;
  flex-direction: column;
  gap: .65rem;
}
.m22-cell:nth-child(2n) { border-right: 0; }
.m22-cell:nth-child(n+3) { border-bottom: 0; }
.m22-cell:first-child  { background: color-mix(in srgb, #2D7A3E 8%, var(--bg)); }
.m22-cell:nth-child(2) { background: color-mix(in srgb, var(--accent) 8%, var(--bg)); }
.m22-cell:nth-child(3) { background: color-mix(in srgb, #6B86A6 7%, var(--bg)); }
.m22-cell:nth-child(4) { background: color-mix(in srgb, var(--muted) 6%, var(--bg)); }
.m22-head {
  font-family: var(--sans);
  font-weight: 600;
  font-size: .82rem;
  letter-spacing: .03em;
  color: var(--ink);
  line-height: 1.4;
}
.m22-badge {
  font-family: var(--sans);
  font-weight: 800;
  font-size: .65rem;
  letter-spacing: .25em;
  text-transform: uppercase;
  color: var(--accent);
  padding: .25rem .55rem;
  background: var(--bg);
  border: 1px solid var(--accent);
  border-radius: 2px;
  align-self: flex-start;
}
.m22-cell:first-child  .m22-badge { color: #2D7A3E; border-color: #2D7A3E; }
.m22-cell:nth-child(3) .m22-badge { color: #6B86A6; border-color: #6B86A6; }
.m22-cell:nth-child(4) .m22-badge { color: var(--muted); border-color: var(--muted); }
.m22-desc {
  font-family: var(--serif);
  font-size: .96rem;
  line-height: 1.5;
  color: var(--ink-soft);
  margin: 0;
}
@media (max-width: 700px) {
  .m22-grid { grid-template-columns: 1fr; }
  .m22-cell { border-right: 0 !important; border-bottom: 1px solid var(--rule) !important; }
  .m22-cell:last-child { border-bottom: 0 !important; }
  .m22-axis-y { display: none; }
}

/* ── Micro-Expression Matrix ── */
.exp-block {
  margin: 2.5rem -1rem;
}
.tbl-expression {
  width: 100%;
  border-collapse: collapse;
}
.tbl-expression .exp-name {
  font-family: var(--sans);
  font-weight: 800;
  font-size: .95rem;
  letter-spacing: .05em;
  color: var(--accent);
  text-align: left;
  vertical-align: top;
  width: 8rem;
  padding: 1rem 1rem 1rem 0;
  border-bottom: 1px solid var(--rule);
  text-transform: uppercase;
}
.tbl-expression .exp-desc {
  font-family: var(--serif);
  font-size: 1rem;
  line-height: 1.55;
  color: var(--ink-soft);
  padding: 1rem 0;
  border-bottom: 1px solid var(--rule);
}

/* ── Six-Category Radar grid ── */
.radar-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
  margin: 2.5rem -1rem;
}
.radar-cat {
  background: var(--bg-soft);
  border: 1px solid var(--rule);
  border-radius: 4px;
  padding: 1.25rem 1.4rem;
}
.rcat-head {
  display: flex;
  align-items: baseline;
  gap: .85rem;
  margin: 0 0 .65rem;
  padding-bottom: .65rem;
  border-bottom: 1px solid var(--rule);
}
.rcat-num {
  font-family: var(--sans);
  font-variant-numeric: tabular-nums;
  font-weight: 800;
  font-size: .82rem;
  letter-spacing: .12em;
  color: var(--accent);
}
.rcat-name {
  font-family: var(--sans);
  font-weight: 700;
  font-size: .92rem;
  letter-spacing: .15em;
  text-transform: uppercase;
  color: var(--ink);
  margin: 0;
  flex: 1;
}
.rcat-desc {
  font-family: var(--serif);
  font-style: italic;
  font-size: .94rem;
  line-height: 1.5;
  color: var(--ink-soft);
  margin: 0 0 .9rem;
}
.rcat-signals {
  list-style: none;
  padding: 0;
  margin: 0;
}
.rcat-signals li {
  display: flex;
  justify-content: space-between;
  gap: .75rem;
  align-items: baseline;
  padding: .35rem 0;
  border-bottom: 1px dotted var(--rule);
  font-family: var(--sans);
  font-size: .82rem;
  color: var(--ink);
}
.rcat-signals li:last-child { border-bottom: 0; }
.rsig-text { flex: 1; line-height: 1.4; }

@media (max-width: 800px) {
  .radar-grid { grid-template-columns: 1fr; margin: 2rem 0; }
}

/* ── 10-Second Scan grid ── */
.scan-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
  margin: 2.5rem -1rem;
}
.scan-step {
  border: 1px solid var(--rule);
  border-top: 4px solid var(--accent);
  border-radius: 0 0 4px 4px;
  padding: 1.25rem 1.25rem 1.5rem;
  background: var(--bg);
}
.sstep-head {
  display: flex;
  align-items: baseline;
  gap: .85rem;
  margin: 0 0 .9rem;
  padding-bottom: .85rem;
  border-bottom: 1px solid var(--rule);
}
.sstep-num {
  font-family: var(--sans);
  font-weight: 200;
  font-size: 2rem;
  line-height: 1;
  color: var(--accent);
  letter-spacing: -0.02em;
}
.sstep-name {
  font-family: var(--sans);
  font-weight: 700;
  font-size: 1.05rem;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: var(--ink);
  margin: 0;
}
.sstep-body p {
  font-family: var(--serif);
  font-size: .95rem;
  line-height: 1.5;
  color: var(--ink-soft);
  margin: 0 0 .65rem;
}
.sstep-body p:last-child { margin-bottom: 0; }
.sstep-body strong {
  font-family: var(--sans);
  font-weight: 700;
  font-size: .68rem;
  letter-spacing: .2em;
  text-transform: uppercase;
  color: var(--accent);
  display: inline-block;
  margin-right: .35rem;
}

/* ── method cards (numbered methods with WHEN trigger) ── */
.method-cards {
  display: grid;
  gap: 1.5rem;
  margin: 2.5rem 0;
}
.method-card {
  display: grid;
  grid-template-columns: 4.5rem 1fr;
  gap: 1.25rem;
  align-items: start;
  padding: 1.4rem 1.5rem;
  background: var(--bg-soft);
  border: 1px solid var(--rule);
  border-left: 4px solid var(--accent);
  border-radius: 0 4px 4px 0;
}
.mc-num {
  font-family: var(--sans);
  font-weight: 200;
  font-size: 2.4rem;
  line-height: 1;
  letter-spacing: -0.03em;
  color: var(--accent);
  font-variant-numeric: tabular-nums;
  text-align: center;
  padding-top: .2rem;
}
.mc-name {
  font-family: var(--sans);
  font-weight: 700;
  font-size: 1.18rem;
  letter-spacing: -0.005em;
  color: var(--ink);
  margin: 0 0 .65rem;
  line-height: 1.25;
}
.mc-when {
  display: flex;
  align-items: baseline;
  gap: .6rem;
  margin: 0 0 .85rem;
  padding: .55rem .75rem;
  border-left: 2px solid var(--accent);
  background: color-mix(in srgb, var(--accent) 5%, transparent);
}
.mc-when-label {
  font-family: var(--sans);
  font-weight: 800;
  font-size: .65rem;
  letter-spacing: .25em;
  text-transform: uppercase;
  color: var(--accent);
  flex-shrink: 0;
}
.mc-when-text {
  font-family: var(--serif);
  font-style: italic;
  font-size: .96rem;
  color: var(--ink-soft);
  line-height: 1.45;
}
.mc-text {
  font-family: var(--serif);
  font-size: 1rem;
  line-height: 1.6;
  color: var(--ink);
  margin: 0;
}
@media (max-width: 700px) {
  .method-card { grid-template-columns: 3rem 1fr; gap: .75rem; padding: 1.15rem 1rem; }
  .mc-num { font-size: 1.85rem; }
  .mc-name { font-size: 1.05rem; }
  .mc-when { flex-direction: column; gap: .25rem; padding: .5rem .65rem; }
}

/* ── preview list (smashed-together TitleCase items become a styled mini-ToC) ── */
.preview-list {
  list-style: none;
  padding: 0;
  margin: 1.25rem 0 2rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0;
  border-top: 1px solid var(--rule);
  border-bottom: 1px solid var(--rule);
  background: var(--bg-soft);
}
.preview-list li {
  display: flex;
  align-items: baseline;
  gap: .55rem;
  padding: .7rem 1rem;
  flex: 1 1 0;
  min-width: 9rem;
  border-right: 1px solid var(--rule);
}
.preview-list li:last-child { border-right: 0; }
.pl-num {
  font-family: var(--sans);
  font-weight: 800;
  font-size: .65rem;
  letter-spacing: .12em;
  color: var(--accent);
  font-variant-numeric: tabular-nums;
}
.pl-name {
  font-family: var(--sans);
  font-weight: 700;
  font-size: .92rem;
  color: var(--ink);
  letter-spacing: -0.005em;
  line-height: 1.3;
}
@media (max-width: 700px) {
  .preview-list { flex-direction: column; }
  .preview-list li { border-right: 0; border-bottom: 1px solid var(--rule); }
  .preview-list li:last-child { border-bottom: 0; }
}

/* ── pillars grid ── */
.pillars-grid {
  display: grid;
  gap: 1.25rem;
  margin: 2.5rem 0;
}
.pillar-card {
  display: grid;
  grid-template-columns: 4.5rem 1fr;
  gap: 1.25rem;
  align-items: start;
  padding: 1.5rem 1.5rem 1.5rem 0;
  border-top: 1px solid var(--rule);
}
.pillar-card:last-child { border-bottom: 1px solid var(--rule); }
.pillar-num {
  font-family: var(--sans);
  font-weight: 200;
  font-size: 3.5rem;
  line-height: 1;
  letter-spacing: -0.04em;
  color: var(--accent);
  text-align: center;
  font-feature-settings: "lnum";
}
.pillar-body { padding-top: .35rem; }
.pillar-name {
  font-family: var(--sans);
  font-weight: 700;
  font-size: 1.35rem;
  letter-spacing: -0.01em;
  color: var(--ink);
  margin: 0 0 .35rem;
}
.pillar-tag {
  font-family: var(--serif);
  font-style: italic;
  font-size: 1.08rem;
  color: var(--ink-soft);
  margin: 0 0 .85rem;
  line-height: 1.5;
}
.pillar-text {
  font-family: var(--serif);
  font-size: 1rem;
  color: var(--ink);
  line-height: 1.6;
  margin: 0;
}
@media (max-width: 600px) {
  .pillar-card { grid-template-columns: 3rem 1fr; gap: .75rem; }
  .pillar-num { font-size: 2.4rem; }
  .pillar-name { font-size: 1.15rem; }
}

/* ── levels ladder ── */
.levels-ladder {
  margin: 2.5rem 0;
  border-top: 1px solid var(--rule);
}
.level-row {
  display: grid;
  grid-template-columns: 5.5rem 8rem 1fr;
  gap: 1.5rem;
  align-items: baseline;
  padding: 1.1rem 0;
  border-bottom: 1px solid var(--rule);
}
.level-num {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.level-tag {
  font-family: var(--sans);
  font-weight: 600;
  font-size: .58rem;
  letter-spacing: .25em;
  text-transform: uppercase;
  color: var(--muted);
}
.level-n {
  font-family: var(--sans);
  font-weight: 200;
  font-size: 2.5rem;
  line-height: 1;
  color: var(--accent);
  letter-spacing: -0.03em;
}
.level-name {
  font-family: var(--sans);
  font-weight: 700;
  font-size: 1.05rem;
  letter-spacing: -0.005em;
  color: var(--ink);
}
.level-desc {
  font-family: var(--serif);
  font-size: .98rem;
  line-height: 1.55;
  color: var(--ink-soft);
}
@media (max-width: 700px) {
  .level-row { grid-template-columns: 1fr; gap: .25rem; padding: 1.25rem 0; }
  .level-name { font-size: 1.15rem; }
  .level-n { font-size: 1.85rem; }
}

/* ── callout boxes ── */
.callout {
  margin: 2.25rem 0;
  padding: 1.25rem 1.5rem;
  border-left: 3px solid var(--accent);
  background: color-mix(in srgb, var(--accent) 6%, var(--bg));
  border-radius: 0 4px 4px 0;
  position: relative;
}
.callout-label {
  font-family: var(--sans);
  font-weight: 800;
  font-size: .68rem;
  letter-spacing: .28em;
  text-transform: uppercase;
  color: var(--accent);
  margin: 0 0 .55rem;
}
.callout-body {
  font-family: var(--serif);
  font-size: 1.05rem;
  line-height: 1.55;
  color: var(--ink);
}
.callout-body p { margin: 0; }

/* variants */
.callout-key { /* default copper */ }
.callout-feel {
  border-left-color: #6B86A6;
  background: color-mix(in srgb, #6B86A6 6%, var(--bg));
}
.callout-feel .callout-label { color: #6B86A6; }
.callout-feel .callout-body { font-style: italic; color: var(--ink-soft); }
.callout-take {
  border-left-color: #2D7A3E;
  background: color-mix(in srgb, #2D7A3E 6%, var(--bg));
}
.callout-take .callout-label { color: #2D7A3E; }
.callout-warn {
  border-left-color: #B53030;
  background: color-mix(in srgb, #B53030 6%, var(--bg));
}
.callout-warn .callout-label { color: #B53030; }
.callout-warn .callout-label::before { content: "⚠  "; }
.callout-memorable {
  border-left-color: #8C5A2A;
  background: color-mix(in srgb, #8C5A2A 7%, var(--bg));
}
.callout-memorable .callout-label { color: #8C5A2A; }
.callout-memorable .callout-body { font-weight: 600; }
.callout-truth {
  border-left-color: var(--ink);
  background: color-mix(in srgb, var(--ink) 4%, var(--bg));
}
.callout-truth .callout-label { color: var(--ink); }

/* ── T4 panels ── */
.t4-panel {
  margin: 2.5rem 0;
  border: 1px solid var(--rule);
  border-left: 4px solid var(--muted);
  background: var(--bg-soft);
  border-radius: 0 4px 4px 0;
  padding: 1.5rem 1.75rem;
}
.t4-head {
  display: flex;
  align-items: baseline;
  gap: 1rem;
  margin: 0 0 1.25rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--rule);
}
.t4-tag {
  font-family: var(--sans);
  font-weight: 800;
  font-size: .72rem;
  letter-spacing: .12em;
  padding: .25rem .55rem;
  background: var(--muted);
  color: var(--bg);
  border-radius: 2px;
  flex-shrink: 0;
}
.t4-title {
  font-family: var(--sans);
  font-weight: 700;
  font-size: 1.1rem;
  letter-spacing: -0.005em;
  color: var(--ink);
  margin: 0;
  line-height: 1.3;
}
.t4-row {
  display: grid;
  grid-template-columns: 11rem 1fr;
  gap: 1.25rem;
  margin: 0 0 1rem;
}
.t4-row:last-child { margin-bottom: 0; }
.t4-label {
  font-family: var(--sans);
  font-weight: 700;
  font-size: .68rem;
  letter-spacing: .25em;
  text-transform: uppercase;
  color: var(--accent);
  padding-top: .25rem;
}
.t4-content {
  font-family: var(--serif);
  font-size: 1rem;
  line-height: 1.55;
  color: var(--ink-soft);
}
@media (max-width: 700px) {
  .t4-row { grid-template-columns: 1fr; gap: .35rem; }
  .t4-panel { padding: 1.25rem 1rem; }
}

/* ── data tables ── */
.data-block {
  margin: 2.5rem -1rem;
  overflow-x: auto;
}
.data-block table {
  width: 100%;
  border-collapse: collapse;
  font-family: var(--sans);
  font-size: .92rem;
}
.data-block th, .data-block td {
  text-align: left;
  vertical-align: top;
  padding: .85rem 1rem;
  border-bottom: 1px solid var(--rule);
}
.data-block thead th {
  font-weight: 700;
  font-size: .7rem;
  letter-spacing: .25em;
  text-transform: uppercase;
  color: var(--accent);
  border-bottom: 1px solid var(--accent);
  background: transparent;
  padding-bottom: .65rem;
}

/* tier table (T1..T4 → title + description) */
.tbl-tier .tier-key {
  font-family: var(--sans);
  font-weight: 800;
  font-size: 1.1rem;
  letter-spacing: .08em;
  color: var(--accent);
  width: 4.5rem;
  border-bottom: 1px solid var(--rule);
}
.tbl-tier .tier-title {
  font-family: var(--sans);
  font-weight: 700;
  font-size: 1rem;
  color: var(--ink);
  margin-bottom: .25rem;
}
.tbl-tier .tier-desc {
  font-family: var(--serif);
  font-size: .98rem;
  line-height: 1.5;
  color: var(--ink-soft);
}

/* tell table (cue / line / type) */
.tbl-tell {
  table-layout: fixed;
}
.tbl-tell thead th:nth-child(1) { width: 30%; }
.tbl-tell thead th:nth-child(2) { width: 60%; }
.tbl-tell thead th:nth-child(3) { width: 10%; text-align: center; }
.tbl-tell .tell-cue {
  font-family: var(--sans);
  font-weight: 600;
  color: var(--ink);
  font-size: .92rem;
  line-height: 1.4;
}
.tbl-tell .tell-line {
  font-family: var(--serif);
  font-style: italic;
  color: var(--ink-soft);
  font-size: 1rem;
  line-height: 1.5;
}
.tbl-tell .tell-type {
  font-family: var(--sans);
  font-weight: 800;
  font-size: .85rem;
  letter-spacing: .1em;
  color: var(--accent);
  text-align: center;
  border-left: 1px solid var(--rule);
}

/* matrix table (vowels x eras) */
.tbl-matrix {
  text-align: center;
}
.tbl-matrix thead th {
  text-align: center;
  font-size: .8rem;
}
.tbl-matrix .matrix-rowhead {
  font-weight: 700;
  font-size: .72rem;
  letter-spacing: .2em;
  text-transform: uppercase;
  color: var(--ink);
  text-align: left;
  border-right: 1px solid var(--rule);
}
.tbl-matrix .matrix-empty {
  color: var(--rule);
  font-family: var(--serif);
}
.tbl-matrix .matrix-fill {
  font-family: var(--serif);
  font-style: italic;
  color: var(--ink-soft);
}

/* plain fallback */
.tbl-plain th { font-weight: 600; color: var(--ink); }
.tbl-plain td { font-family: var(--serif); color: var(--ink-soft); }

/* Design Summary 2-column table (Meta Reveal) */
.design-block { margin: 2rem -1rem; }
.tbl-design {
  width: 100%;
  border-collapse: collapse;
  font-family: var(--sans);
  background: var(--bg-card, var(--bg));
}
.tbl-design thead th {
  font-weight: 700;
  font-size: .65rem;
  letter-spacing: .25em;
  text-transform: uppercase;
  color: var(--accent);
  text-align: left;
  padding: .85rem 1rem .65rem;
  border-bottom: 1px solid var(--accent);
}
.tbl-design td {
  padding: .85rem 1rem;
  border-bottom: 1px solid var(--rule);
  vertical-align: top;
  font-size: .92rem;
  line-height: 1.45;
}
.tbl-design tbody tr:last-child td { border-bottom: 0; }
.tbl-design .ds-element { font-weight: 600; color: var(--ink); width: 40%; }
.tbl-design .ds-mech { font-family: var(--serif); font-style: italic; color: var(--ink-soft); }

/* 80-Signal System table */
.signal-block {
  margin: 2.5rem -2rem;
}
.tbl-signal {
  table-layout: fixed;
  font-family: var(--sans);
}
.tbl-signal thead th {
  font-size: .65rem;
  letter-spacing: .25em;
  text-transform: uppercase;
  color: var(--accent);
  border-bottom: 1px solid var(--accent);
  padding-bottom: .55rem;
}
.tbl-signal thead th:nth-child(1) { width: 3rem; text-align: center; }
.tbl-signal thead th:nth-child(2) { width: 30%; }
.tbl-signal thead th:nth-child(3) { width: auto; }
.tbl-signal thead th:nth-child(4) { width: 4rem; text-align: center; }
.tbl-signal thead th:nth-child(5) { width: 7rem; text-align: center; }
.tbl-signal tbody tr:hover { background: rgba(182, 84, 34, 0.04); }
.tbl-signal td { vertical-align: top; padding: .65rem .75rem; }
.tbl-signal .sig-num {
  font-family: var(--sans);
  font-variant-numeric: tabular-nums;
  font-weight: 800;
  font-size: .8rem;
  color: var(--muted);
  text-align: center;
}
.tbl-signal .sig-obs {
  font-family: var(--sans);
  font-weight: 600;
  font-size: .92rem;
  color: var(--ink);
  line-height: 1.4;
}
.tbl-signal .sig-ins {
  font-family: var(--serif);
  font-style: italic;
  color: var(--ink-soft);
  font-size: 1rem;
  line-height: 1.45;
}
.tbl-signal .sig-tier { text-align: center; }
.tbl-signal .sig-codes { text-align: center; }

.tier-pill {
  display: inline-block;
  font-family: var(--sans);
  font-weight: 800;
  font-size: .75rem;
  letter-spacing: .08em;
  padding: .15rem .5rem;
  border-radius: 2px;
  color: white;
  background: var(--ink-soft);
}
.tier-pill.tier-t1 { background: #2D7A3E; }
.tier-pill.tier-t2 { background: var(--accent); }
.tier-pill.tier-t3 { background: #8C5A2A; }
.tier-pill.tier-t4 { background: #6B6660; }

.code-pill {
  display: inline-block;
  font-family: var(--sans);
  font-weight: 700;
  font-size: .65rem;
  letter-spacing: .08em;
  padding: .12rem .4rem;
  border-radius: 2px;
  margin: 0 .12rem;
  border: 1px solid var(--rule);
  color: var(--ink-soft);
}
.code-pill.code-bp { color: #2D7A3E; border-color: #2D7A3E; }
.code-pill.code-cr { color: var(--accent); border-color: var(--accent); }
.code-pill.code-vs { color: #8C5A2A; border-color: #8C5A2A; }
.code-pill.code-am { color: #6B6660; border-color: #6B6660; }

@media (max-width: 800px) {
  .signal-block { margin: 2rem -1rem; }
  .tbl-signal { font-size: .85rem; }
  .tbl-signal td, .tbl-signal th { padding: .5rem .4rem; }
  .tbl-signal thead th:nth-child(2) { width: 28%; }
}

@media (max-width: 700px) {
  .data-block { margin: 2rem -1rem; }
  .data-block table { font-size: .85rem; }
  .data-block th, .data-block td { padding: .7rem .6rem; }
}

/* ── back-to-top ── */
.totop {
  position: fixed;
  right: 1.25rem;
  bottom: 1.25rem;
  background: var(--ink);
  color: var(--bg);
  font-family: var(--sans);
  font-size: .72rem;
  letter-spacing: .15em;
  padding: .5rem .75rem;
  text-transform: uppercase;
  border: 0;
  cursor: pointer;
  opacity: 0;
  transition: opacity .2s;
  border-radius: 2px;
}
.totop.show { opacity: .85; }
.totop:hover { opacity: 1; }

/* ── small screens ── */
@media (max-width: 600px) {
  html, body { font-size: 17px; }
  .page { padding: 1.5rem 1.1rem 4rem; }
  .chapter-opener .epigraph { font-size: 1.05rem; }
}

/* ── print: stick to web styles, but hide back-to-top ── */
@media print {
  .totop { display: none; }
  body { background: white; color: black; }
}
"""


def esc(s: str) -> str:
    """Escape text for HTML, then re-decode any literal &quot;/&amp; the manuscript
    might contain (because the source DOCX has these as actual characters)."""
    # Decode literal HTML entities the source mistakenly contains
    s = s.replace("&quot;", "”")  # most "&quot;" appear as closing quotes; we'll re-fix smart quoting below
    s = s.replace("&amp;", "&")
    s = s.replace("&hellip;", "…")
    s = s.replace("&mdash;", "—")
    s = s.replace("&ndash;", "–")
    return html.escape(s, quote=False)


def smart_quote_pass(s: str) -> str:
    """Light typographic cleanup on visible text."""
    # Triple dot to ellipsis where appropriate
    s = re.sub(r"\.{3,}", "…", s)
    # Convert "--" and " - " to em-dashes (when surrounded by word chars or spaces)
    s = re.sub(r"\s+--\s+", " — ", s)
    s = re.sub(r"--", "—", s)
    # Convert remaining straight quotes to curly. Heuristic: " preceded by a letter/punct/digit -> closing
    s = _curl_quotes(s)
    return s


def _curl_quotes(s: str) -> str:
    out = []
    prev = ""
    for ch in s:
        if ch == '"':
            if not prev or prev in " \n\t ([{—–-":
                out.append("“")  # opening
            else:
                out.append("”")  # closing
        elif ch == "'":
            if not prev or prev in " \n\t ([{—–-":
                out.append("‘")
            else:
                out.append("’")
        else:
            out.append(ch)
        prev = ch
    return "".join(out)


def render_para_text(text: str) -> str:
    return esc(smart_quote_pass(text))


# 80-Signal System row parser.  Each row arrived as
#   ##<observation><Insight starting with capital>T[1-4]<codes>
# with no separators (the source DOCX collapsed tabbed columns).  Some rows
# include quotes, commas and stray capital letters mid-text, so we use a
# layered approach: anchored split on T[1-4] then the trailing code run, then
# a soft observation/insight split inside the middle string.

_SIGNAL_NUM_RE   = re.compile(r"^(\d{2})(.+)$")
_SIGNAL_TAIL_RE  = re.compile(r"^(.*?)(T[1-4])((?:\s*(?:BP|CR|VS|AM))+)\s*$")
_OBS_INSIGHT_RE  = re.compile(r"^(.*?[a-z\.\)\?\!\"’”—–-])([A-Z].*)$")


def _try_split_signal_row(line: str) -> tuple[str, str, str, str, str] | None:
    s = line.strip()
    m_num = _SIGNAL_NUM_RE.match(s)
    if not m_num:
        return None
    num, rest = m_num.group(1), m_num.group(2)

    # Find the LAST T[1-4]<codes> at the end — anchor by scanning right-to-left.
    m_tail = _SIGNAL_TAIL_RE.match(rest)
    if not m_tail:
        return None
    middle = m_tail.group(1)
    tier   = m_tail.group(2)
    codes  = m_tail.group(3).strip()

    # Soft split observation/insight.  If we can't, dump everything into observation.
    m_split = _OBS_INSIGHT_RE.match(middle)
    if m_split:
        obs = m_split.group(1).strip()
        ins = m_split.group(2).strip()
    else:
        obs = middle.strip()
        ins = ""

    return (num, obs, ins, tier, codes)


# Heuristics that classify what kind of table we're rendering, so we can
# style each appropriately.
_TIER_HEAD_RE = re.compile(r"^T[1-4]$")
_DISC_LETTER_RE = re.compile(r"^[DISC](\s*/\s*[DISC])?$")  # e.g. "D" or "D / I"


def _classify_table(rows: list[list[str]], caption_hint: str = "") -> str:
    """Return a CSS variant: 'signal' | 'tier' | 'tell' | 'matrix' | 'design' | 'plain'."""
    if caption_hint == "signal-table":
        return "signal"
    if caption_hint == "design-summary":
        return "design"
    if not rows:
        return "plain"
    cols = max(len(r) for r in rows)
    # Tier table: 2 cols, first col is T1..T4
    if cols == 2 and all(_TIER_HEAD_RE.match(r[0].strip()) for r in rows if r and r[0]):
        return "tier"
    # Tell table: 3 cols with header row "Cue / Line / Type" (case-insensitive)
    if cols == 3 and rows[0] and len(rows[0]) >= 3:
        header = [h.strip().lower() for h in rows[0]]
        if header[:3] == ["cue", "line", "type"]:
            return "tell"
    # Matrix table: first row is mostly empty + single letters (vowel matrix etc.)
    if cols >= 4 and rows[0]:
        first_row = [c.strip() for c in rows[0]]
        if first_row[0] == "" and all(len(c) <= 3 for c in first_row[1:]):
            return "matrix"
    return "plain"


def render_obs_table(block: Block) -> str:
    if len(block.rows) < 2:
        return ""
    headers = block.rows[0]
    rows = block.rows[1:]
    head_html = "".join(f'<th>{esc(h)}</th>' for h in headers)
    body_html = "".join(
        '<tr>' + "".join(
            f'<td class="ot-c{ci}">{render_para_text(c)}</td>'
            for ci, c in enumerate(row)
        ) + '</tr>'
        for row in rows
    )
    return (
        f'<div class="data-block obs-block">'
        f'<table class="tbl-obs">'
        f'<thead><tr>{head_html}</tr></thead>'
        f'<tbody>{body_html}</tbody>'
        f'</table></div>'
    )


def render_expert_panel(block: Block) -> str:
    cap = block.caption or "||"
    parts = (cap.split("|") + ["", "", ""])[:3]
    variant, label, subtitle = parts[0], parts[1], parts[2]
    return (
        f'<aside class="expert-panel ep-{esc(variant)}">'
        f'<header class="ep-head">'
        f'<span class="ep-label">{esc(label)}</span>'
        f'<span class="ep-subtitle">{esc(subtitle)}</span>'
        f'</header>'
        f'<div class="ep-body">{render_para_text(block.text)}</div>'
        f'</aside>'
    )


def render_ftf_flow() -> str:
    """Hardcoded Fruit-to-Fang decision flowchart, structurally ported from
    the legacy build (with branching yes/no nodes), restyled for the new
    design language."""
    return """
<section class="ftf-flow">
  <header class="ftf-flow-title">How Search Effort Narrows the Field</header>
  <div class="ftf-flow-body">
    <div class="ftf-node ftf-node-start">Think of the first vowel</div>
    <div class="ftf-arrow">&#8595;</div>
    <div class="ftf-node">Think of a fruit with that letter</div>
    <div class="ftf-arrow">&#8595;</div>
    <div class="ftf-branch">
      <div class="ftf-branch-item ftf-yes">
        <strong>Fruit comes immediately</strong>
        <span class="ftf-note">likely common fruit</span>
        <span>think <span class="ftf-vowel">A / O</span></span>
        <span class="ftf-note">apple or orange</span>
      </div>
      <div class="ftf-branch-mid">Did it come easily?</div>
      <div class="ftf-branch-item ftf-no">
        <strong>No fruit / visible search</strong>
        <span class="ftf-note">offer the animal option</span>
      </div>
    </div>
    <div class="ftf-arrow">&#8595;</div>
    <div class="ftf-branch">
      <div class="ftf-branch-item ftf-yes">
        <strong>Animal comes immediately</strong>
        <span>think <span class="ftf-vowel">E</span></span>
        <span class="ftf-note">Eagle / Elephant &mdash; ask if it feels like a large animal; confident yes confirms elephant</span>
      </div>
      <div class="ftf-branch-mid">Animal ease?</div>
      <div class="ftf-branch-item ftf-no">
        <strong>Animal takes longer</strong>
        <span>think <span class="ftf-vowel">I / U</span></span>
        <span class="ftf-note">watch quality of search &amp; reaction to challenge</span>
      </div>
    </div>
    <div class="ftf-arrow">&#8595;</div>
    <div class="ftf-node ftf-node-test">Playful challenge: <em>&ldquo;That&rsquo;s not a real animal.&rdquo;</em></div>
    <div class="ftf-arrow">&#8595;</div>
    <div class="ftf-branch">
      <div class="ftf-branch-item ftf-yes">
        <strong>Mild confusion</strong>
        <span>likely <span class="ftf-vowel">I</span></span>
        <span class="ftf-note">iguana or another borderline answer</span>
      </div>
      <div class="ftf-branch-mid">Reaction?</div>
      <div class="ftf-branch-item ftf-no">
        <strong>Strong surprise</strong>
        <span>likely <span class="ftf-vowel">U</span></span>
        <span class="ftf-note">unicorn &mdash; watch for shoulder shrug or head wobble as social protection</span>
      </div>
    </div>
    <div class="ftf-arrow">&#8595;</div>
    <div class="ftf-node ftf-node-note">
      <strong>Very long search before settling</strong>
      <span class="ftf-note">points toward <span class="ftf-vowel">U</span> rather than <span class="ftf-vowel">I</span> &mdash; the mind is reaching for a less natural answer</span>
    </div>
  </div>
</section>
"""


def render_flowchart(block: Block) -> str:
    title = block.title or "Decision Flow"
    nodes = []
    for idx, row in enumerate(block.rows):
        head = row[0] if row else ""
        details = row[1:] if len(row) > 1 else []
        det_html = ""
        if details:
            det_html = '<ul class="fc-detail">' + "".join(
                f'<li>{render_para_text(d)}</li>' for d in details
            ) + '</ul>'
        nodes.append(
            f'<li class="fc-step">'
            f'<div class="fc-num">{idx + 1}</div>'
            f'<div class="fc-card">'
            f'<div class="fc-head">{render_para_text(head)}</div>'
            f'{det_html}'
            f'</div>'
            f'</li>'
        )
    return (
        f'<section class="flowchart">'
        f'<header class="fc-title">{esc(title)}</header>'
        f'<ol class="fc-steps">{"".join(nodes)}</ol>'
        f'</section>'
    )


def render_type_cards(block: Block) -> str:
    cards = []
    is_volunteer = block.caption == "volunteer"
    for row in block.rows:
        name, desc, tells, works, avoid = (row + ["", "", [], "", ""])[:5]
        # tells could be a list (volunteer) or empty (auto); be defensive
        if isinstance(tells, str):
            tells = []
        tells_html = ""
        if tells:
            tells_items = "".join(f"<li>{render_para_text(t)}</li>" for t in tells)
            tells_html = f'<ul class="tc-tells">{tells_items}</ul>'
        meta_html = ""
        if works or avoid:
            meta_html = '<div class="tc-meta">'
            if works:
                meta_html += f'<div class="tc-meta-row"><span class="tc-meta-label tc-good">Use for</span><span class="tc-meta-text">{render_para_text(works)}</span></div>'
            if avoid:
                meta_html += f'<div class="tc-meta-row"><span class="tc-meta-label tc-warn">Avoid for</span><span class="tc-meta-text">{render_para_text(avoid)}</span></div>'
            meta_html += '</div>'
        cards.append(
            f'<article class="type-card">'
            f'<h4 class="tc-name">{esc(name)}</h4>'
            f'<p class="tc-desc">{render_para_text(desc)}</p>'
            f'{tells_html}'
            f'{meta_html}'
            f'</article>'
        )
    cls_extra = " type-cards-volunteer" if is_volunteer else ""
    return f'<section class="type-cards{cls_extra}">{"".join(cards)}</section>'


def render_matrix2x2(block: Block) -> str:
    if len(block.rows) < 4:
        return ""
    cells_html = []
    for hdr, badge, desc in [(r[0], r[1], r[2]) for r in block.rows]:
        cells_html.append(
            f'<article class="m22-cell">'
            f'<header class="m22-head">{esc(hdr)}</header>'
            f'<div class="m22-badge">{esc(badge)}</div>'
            f'<p class="m22-desc">{render_para_text(desc)}</p>'
            f'</article>'
        )
    return (
        f'<section class="matrix2x2">'
        f'<div class="m22-axes">'
        f'<span class="m22-axis-y">Suggestibility</span>'
        f'<span class="m22-axis-x">Confidence</span>'
        f'</div>'
        f'<div class="m22-grid">{"".join(cells_html)}</div>'
        f'</section>'
    )


def render_expression_table(block: Block) -> str:
    rows = []
    for row in block.rows:
        name, desc = (row + ["", ""])[:2]
        rows.append(
            f'<tr>'
            f'<th scope="row" class="exp-name">{esc(name)}</th>'
            f'<td class="exp-desc">{render_para_text(desc)}</td>'
            f'</tr>'
        )
    return f'<div class="data-block exp-block"><table class="tbl-expression"><tbody>{"".join(rows)}</tbody></table></div>'


def render_category_cards(block: Block) -> str:
    cards = []
    for row in block.rows:
        letter, name, desc = (row + ["", "", ""])[:3]
        cards.append(
            f'<article class="cat-card cat-{letter.lower()}">'
            f'<div class="cat-letter">{esc(letter)}</div>'
            f'<div class="cat-body">'
            f'<h4 class="cat-name">{esc(name)}</h4>'
            f'<p class="cat-desc">{render_para_text(desc)}</p>'
            f'</div>'
            f'</article>'
        )
    return f'<section class="category-grid">{"".join(cards)}</section>'


def render_method_cards(block: Block) -> str:
    cards = []
    for row in block.rows:
        num, name, trigger, body = (row + ["", "", "", ""])[:4]
        cards.append(
            f'<article class="method-card">'
            f'<div class="mc-num">{esc(num)}</div>'
            f'<div class="mc-body">'
            f'<h4 class="mc-name">{esc(name)}</h4>'
            f'<div class="mc-when"><span class="mc-when-label">When</span>'
            f'<span class="mc-when-text">{render_para_text(trigger)}</span></div>'
            f'<p class="mc-text">{render_para_text(body)}</p>'
            f'</div>'
            f'</article>'
        )
    return f'<section class="method-cards">{"".join(cards)}</section>'


def render_preview_list(block: Block) -> str:
    items = "".join(
        f'<li><span class="pl-num">{idx + 1:02d}</span>'
        f'<span class="pl-name">{render_para_text(row[0])}</span></li>'
        for idx, row in enumerate(block.rows)
    )
    return f'<ol class="preview-list">{items}</ol>'


def render_radar(block: Block) -> str:
    cards = []
    for idx, row in enumerate(block.rows, 1):
        name, desc, signals = row[0], row[1], row[2]
        sig_html = "".join(
            f'<li><span class="rsig-text">{render_para_text(t)}</span>'
            f'{f"<span class=\"tier-pill tier-{tier.lower()}\">{esc(tier)}</span>" if tier else ""}</li>'
            for t, tier in signals
        )
        cards.append(
            f'<article class="radar-cat">'
            f'<header class="rcat-head">'
            f'<span class="rcat-num">{idx:02d}</span>'
            f'<h4 class="rcat-name">{esc(name)}</h4>'
            f'</header>'
            f'<p class="rcat-desc">{render_para_text(desc)}</p>'
            f'<ul class="rcat-signals">{sig_html}</ul>'
            f'</article>'
        )
    return f'<section class="radar-grid">{"".join(cards)}</section>'


def render_scan(block: Block) -> str:
    cards = []
    for idx, row in enumerate(block.rows, 1):
        name, body = row[0], row[1]
        # Try to bold the "Notice:" / "Tells you:" prefixes
        body_html = render_para_text(body)
        body_html = re.sub(
            r"(Notice:|Tells you:)",
            r"<strong>\1</strong>",
            body_html,
        )
        # Convert paragraph breaks to <p> tags
        paras = body.split("\n\n")
        body_paras = "".join(
            "<p>" + re.sub(r"(Notice:|Tells you:)", r"<strong>\1</strong>", render_para_text(p)) + "</p>"
            for p in paras if p.strip()
        )
        cards.append(
            f'<article class="scan-step">'
            f'<header class="sstep-head">'
            f'<span class="sstep-num">{idx}</span>'
            f'<h4 class="sstep-name">{esc(name)}</h4>'
            f'</header>'
            f'<div class="sstep-body">{body_paras}</div>'
            f'</article>'
        )
    return f'<section class="scan-grid">{"".join(cards)}</section>'


def render_pillars(block: Block) -> str:
    cards = []
    for row in block.rows:
        roman, name, tagline, body = (row + ["", "", "", ""])[:4]
        cards.append(
            f'<article class="pillar-card">'
            f'<div class="pillar-num">{esc(roman)}</div>'
            f'<div class="pillar-body">'
            f'<h4 class="pillar-name">{esc(name)}</h4>'
            f'<p class="pillar-tag">{render_para_text(tagline)}</p>'
            f'<p class="pillar-text">{render_para_text(body)}</p>'
            f'</div>'
            f'</article>'
        )
    return f'<section class="pillars-grid">{"".join(cards)}</section>'


def render_levels(block: Block) -> str:
    rows = []
    for row in block.rows:
        n, name, desc = (row + ["", "", ""])[:3]
        rows.append(
            f'<div class="level-row">'
            f'<div class="level-num"><span class="level-tag">Level</span><span class="level-n">{esc(n)}</span></div>'
            f'<div class="level-name">{esc(name)}</div>'
            f'<div class="level-desc">{render_para_text(desc)}</div>'
            f'</div>'
        )
    return f'<section class="levels-ladder">{"".join(rows)}</section>'


def render_callout(block: Block) -> str:
    cap = block.caption or "|Note"
    variant, label = (cap.split("|", 1) + [""])[:2]
    return (
        f'<aside class="callout callout-{esc(variant)}">'
        f'<div class="callout-label">{esc(label)}</div>'
        f'<div class="callout-body">{render_para_text(block.text)}</div>'
        f'</aside>'
    )


def render_t4(block: Block) -> str:
    parts = []
    if block.title:
        parts.append(f'<header class="t4-head"><span class="t4-tag">T4</span><h4 class="t4-title">{render_para_text(block.title)}</h4></header>')
    rows = []
    for label, field in (("The Claim", block.claim), ("The Research", block.research), ("What Remains Valid", block.valid)):
        if field:
            rows.append(
                f'<div class="t4-row"><div class="t4-label">{esc(label)}</div>'
                f'<div class="t4-content">{render_para_text(field)}</div></div>'
            )
    return f'<section class="t4-panel">{"".join(parts)}{"".join(rows)}</section>'


def render_figure(block: Block) -> str:
    src = block.src
    alt = block.alt or block.caption
    cap = block.caption
    return (
        f'<figure class="book-figure">'
        f'<img src="{esc(src)}" alt="{esc(alt)}" loading="lazy">'
        f'{f"<figcaption>{render_para_text(cap)}</figcaption>" if cap else ""}'
        f'</figure>'
    )


def render_table(block: Block) -> str:
    rows = block.rows
    if not rows:
        return ""
    variant = _classify_table(rows, caption_hint=block.caption)

    if variant == "design":
        out = ['<div class="data-block design-block"><table class="tbl-design"><thead><tr>']
        for h in rows[0]:
            out.append(f"<th>{esc(h)}</th>")
        out.append("</tr></thead><tbody>")
        for r in rows[1:]:
            cell0 = render_para_text(r[0]) if len(r) > 0 else ""
            cell1 = render_para_text(r[1]) if len(r) > 1 else ""
            out.append(f'<tr><td class="ds-element">{cell0}</td><td class="ds-mech">{cell1}</td></tr>')
        out.append("</tbody></table></div>")
        return "\n".join(out)

    if variant == "signal":
        out = ['<div class="data-block signal-block"><table class="tbl-signal"><thead><tr>']
        for h in rows[0]:
            out.append(f"<th>{esc(h.strip())}</th>")
        out.append("</tr></thead><tbody>")
        for r in rows[1:]:
            num, obs, ins, tier, codes = (r + ["", "", "", "", ""])[:5]
            code_pills = " ".join(
                f'<span class="code-pill code-{c.lower()}">{esc(c)}</span>'
                for c in codes.split()
            )
            out.append(
                f'<tr>'
                f'<td class="sig-num">{esc(num)}</td>'
                f'<td class="sig-obs">{render_para_text(obs)}</td>'
                f'<td class="sig-ins">{render_para_text(ins)}</td>'
                f'<td class="sig-tier"><span class="tier-pill tier-{tier.lower()}">{esc(tier)}</span></td>'
                f'<td class="sig-codes">{code_pills}</td>'
                f'</tr>'
            )
        out.append("</tbody></table></div>")
        return "\n".join(out)


    if variant == "tier":
        out = ['<div class="data-block tier-block"><table class="tbl-tier"><tbody>']
        for r in rows:
            if len(r) < 2:
                continue
            tier = esc(r[0].strip())
            # cell text often has "Title\nDescription" — split first line as title
            parts_ = r[1].split("\n", 1)
            title = esc(parts_[0].strip())
            desc  = esc(parts_[1].strip()) if len(parts_) > 1 else ""
            out.append(
                f'<tr><th scope="row" class="tier-key">{tier}</th>'
                f'<td><div class="tier-title">{title}</div>'
                f'{f"<div class=\"tier-desc\">{render_para_text(parts_[1].strip())}</div>" if desc else ""}'
                f"</td></tr>"
            )
        out.append("</tbody></table></div>")
        return "\n".join(out)

    if variant == "tell":
        out = ['<div class="data-block tell-block"><table class="tbl-tell"><thead><tr>']
        for h in rows[0][:3]:
            out.append(f"<th>{esc(h.strip())}</th>")
        out.append("</tr></thead><tbody>")
        for r in rows[1:]:
            cue  = render_para_text(r[0].strip()) if len(r) > 0 else ""
            line = render_para_text(r[1].strip()) if len(r) > 1 else ""
            typ  = esc(r[2].strip()) if len(r) > 2 else ""
            out.append(
                f'<tr><td class="tell-cue">{cue}</td>'
                f'<td class="tell-line">{line}</td>'
                f'<td class="tell-type">{typ}</td></tr>'
            )
        out.append("</tbody></table></div>")
        return "\n".join(out)

    if variant == "matrix":
        out = ['<div class="data-block matrix-block"><table class="tbl-matrix"><thead><tr>']
        for h in rows[0]:
            out.append(f"<th>{esc(h.strip())}</th>")
        out.append("</tr></thead><tbody>")
        for r in rows[1:]:
            out.append("<tr>")
            for ci, cell in enumerate(r):
                txt = cell.strip()
                if ci == 0:
                    out.append(f'<th scope="row" class="matrix-rowhead">{esc(txt)}</th>')
                else:
                    cls = "matrix-empty" if txt == "—" or txt == "-" or not txt else "matrix-fill"
                    out.append(f'<td class="{cls}">{esc(txt) if txt else "&mdash;"}</td>')
            out.append("</tr>")
        out.append("</tbody></table></div>")
        return "\n".join(out)

    # plain fallback
    out = ['<div class="data-block plain-block"><table class="tbl-plain"><tbody>']
    for ri, r in enumerate(rows):
        tag = "th" if ri == 0 else "td"
        out.append("<tr>")
        for c in r:
            out.append(f"<{tag}>{render_para_text(c.strip())}</{tag}>")
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out)


def render_chapter(ch: Chapter, parts: list[Part]) -> str:
    part_label = ""
    if ch.part_index is not None and 0 <= ch.part_index < len(parts):
        p = parts[ch.part_index]
        part_label = f"Part {p.ordinal.title()}"
    if ch.interlude:
        label = ch.label or "Interlude"
        eyebrow = (f"{part_label} · {label}") if part_label else label
    else:
        eyebrow = (f"Chapter {ch.number}" + (f" · {part_label}" if part_label else ""))
    anchor = f"chapter-{ch.number}" if not ch.interlude else f"interlude-{abs(hash(ch.title)) % 99999}"

    body_html = []
    for b in ch.blocks:
        if b.kind == "para":
            body_html.append(f"<p>{render_para_text(b.text)}</p>")
        elif b.kind == "subhead":
            cls = ""
            t = b.text.strip()
            letters = [c for c in t if c.isalpha()]
            if letters and all(c.isupper() for c in letters):
                cls = ' class="allcaps"'
            body_html.append(f"<h3{cls}>{render_para_text(b.text)}</h3>")
        elif b.kind == "break":
            body_html.append('<hr class="section-break" aria-hidden="true">')
        elif b.kind == "blockquote":
            body_html.append(f"<blockquote>{render_para_text(b.text)}</blockquote>")
        elif b.kind == "table":
            body_html.append(render_table(b))
        elif b.kind == "figure":
            body_html.append(render_figure(b))
        elif b.kind == "callout":
            body_html.append(render_callout(b))
        elif b.kind == "t4_panel":
            body_html.append(render_t4(b))
        elif b.kind == "pillars":
            body_html.append(render_pillars(b))
        elif b.kind == "levels":
            body_html.append(render_levels(b))
        elif b.kind == "radar":
            body_html.append(render_radar(b))
        elif b.kind == "scan":
            body_html.append(render_scan(b))
        elif b.kind == "type_cards":
            body_html.append(render_type_cards(b))
        elif b.kind == "matrix2x2":
            body_html.append(render_matrix2x2(b))
        elif b.kind == "expression_table":
            body_html.append(render_expression_table(b))
        elif b.kind == "preview_list":
            body_html.append(render_preview_list(b))
        elif b.kind == "method_cards":
            body_html.append(render_method_cards(b))
        elif b.kind == "obs_table":
            body_html.append(render_obs_table(b))
        elif b.kind == "flowchart":
            body_html.append(render_flowchart(b))
        elif b.kind == "ftf_flow":
            body_html.append(render_ftf_flow())
        elif b.kind == "expert_panel":
            body_html.append(render_expert_panel(b))

    epi = ""
    if ch.epigraph:
        epi = f'<p class="epigraph">{render_para_text(ch.epigraph)}</p>'

    # Symbol pill row (T-tiers + observation categories) for numbered chapters
    pill_row = ""
    if not ch.interlude and ch.number in CHAPTER_LEGEND:
        leg = CHAPTER_LEGEND[ch.number]
        tier_pills = "".join(
            f'<span class="csym-pill tier-{t}">{t.upper()}</span>'
            for t in leg.get("tiers", [])
        )
        cat_pills = "".join(
            f'<span class="csym-pill cat-{c}">{c.upper()}</span>'
            for c in leg.get("cats", [])
        )
        if tier_pills or cat_pills:
            pill_row = f'<div class="chapter-symbol-row" aria-label="Signal tiers and observation categories">{tier_pills}{cat_pills}</div>'

    return f"""
<section class="chapter" id="{anchor}">
  <header class="chapter-opener">
    <p class="eyebrow">{esc(eyebrow)}</p>
    <h2 class="chapter-title">{esc(ch.title)}</h2>
    {pill_row}
    {epi}
  </header>
  <div class="chapter-body">
    {''.join(body_html)}
  </div>
</section>
"""


def render_part_divider(part: Part) -> str:
    return f"""
<section class="part-divider" id="part-{part.index}">
  <p class="eyebrow">Part {part.ordinal.title()}</p>
  <h2 class="pt-title">{esc(part.title)}</h2>
</section>
"""


def render_toc(chapters: list[Chapter], parts: list[Part]) -> str:
    rows = ['<div class="toc"><h2>Contents</h2><ol>']
    seen_part_idx = set()
    for ch in chapters:
        if ch.part_index is not None and ch.part_index not in seen_part_idx:
            p = parts[ch.part_index]
            rows.append(
                f'<li class="toc-part">Part {p.ordinal.title()}<span class="pt-title">{esc(p.title)}</span></li>'
            )
            seen_part_idx.add(ch.part_index)
        if ch.interlude:
            toc_label = ch.label or "Interlude"
            rows.append(
                f'<li class="toc-row interlude"><span class="num">✦</span>'
                f'<span class="ttl"><a href="#interlude-{abs(hash(ch.title)) % 99999}">'
                f'{esc(toc_label)} · {esc(ch.title)}</a></span></li>'
            )
        else:
            rows.append(
                f'<li class="toc-row"><span class="num">{ch.number}</span>'
                f'<span class="ttl"><a href="#chapter-{ch.number}">{esc(ch.title)}</a></span></li>'
            )
    rows.append("</ol></div>")
    return "\n".join(rows)


def render_frontmatter(front: dict) -> str:
    out = []
    def render_block_simple(b):
        if b.kind == "subhead":
            return f"<h3 style='font-family:var(--sans);font-size:.85rem;letter-spacing:.2em;text-transform:uppercase;color:var(--accent);margin:1.75rem 0 .5rem;'>{esc(b.text)}</h3>"
        if b.kind == "para":
            return f"<p>{render_para_text(b.text)}</p>"
        if b.kind == "break":
            return '<hr class="section-break" aria-hidden="true">'
        if b.kind == "table":
            return render_table(b)
        if b.kind == "category_cards":
            return render_category_cards(b)
        return ""

    if front["how_to_read"]:
        out.append('<section class="frontmatter" id="how-to-read">')
        out.append("<h2>How to Read This Book</h2>")
        for b in front["how_to_read"]:
            out.append(render_block_simple(b))
        out.append("</section>")
    if front["acknowledgments"]:
        out.append('<section class="frontmatter" id="acknowledgments">')
        out.append("<h2>Acknowledgments</h2>")
        for b in front["acknowledgments"]:
            out.append(render_block_simple(b))
        out.append("</section>")
    return "\n".join(out)


def render_book(chapters: list[Chapter], parts: list[Part], front: dict) -> str:
    cover = """
<section class="cover">
  <p class="imprint-top">Vanishing Inc.</p>
  <h1>
    <span class="line">Built</span>
    <span class="line"><span class="for">for</span> Wonder</span>
  </h1>
  <p class="subtitle">A Mentalist&rsquo;s Guide to Behavioral Science,<br>Psychological Performance, and Astonishment</p>
  <div class="author-block">
    <p class="author-name">Chris Michael</p>
    <p class="author-role">Behavioral Strategist &middot; Mentalist &middot; Keynote Speaker</p>
  </div>
</section>

<section class="hero-quote">
  <blockquote>The brain is a prediction machine. Every performance is a negotiation between what the mind expects and what you choose to deliver.</blockquote>
  <p class="attrib">&mdash; Chris Michael</p>
</section>

<div class="fm-divider"><span class="label">Front Matter</span></div>

<section class="about-author" id="about-the-author">
  <h2>About the Author</h2>
  <p>Chris Michael is a behavioral strategist and corporate mentalist. He holds a <strong>DoD-recognized certification in counterintelligence threat assessment</strong>, is trained by a <strong>founding member of the FBI&rsquo;s Behavioral Analysis Program</strong>, and serves as <strong>Executive Director of the Global Institute of Behavior</strong>. He has delivered behavioral intelligence training for <strong>FBI personnel</strong>, <strong>U.S. Army troops</strong>, <strong>Fortune 500 organizations</strong>, and government defense agencies across more than <strong>twenty industries</strong>.</p>
</section>
"""

    # Render the body in document order: chapters before any Part interleave,
    # then alternating Part dividers and their chapters.
    ordered_html = []
    pre_part_chapters = [ch for ch in chapters if ch.part_index is None]
    for ch in pre_part_chapters:
        ordered_html.append(render_chapter(ch, parts))
    for p in parts:
        ordered_html.append(render_part_divider(p))
        for ch in p.chapters:
            ordered_html.append(render_chapter(ch, parts))

    body = "\n".join(ordered_html)

    js = """
<script>
(function () {
  var btn = document.querySelector('.totop');
  if (!btn) return;
  function tick() { btn.classList.toggle('show', window.scrollY > 600); }
  window.addEventListener('scroll', tick);
  btn.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
  tick();
})();
</script>
"""

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Built for Wonder — Chris Michael</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@200;400;500;700;800&family=Source+Serif+4:ital,wght@0,400;0,500;0,600;1,400;1,600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<main class="page">
{cover}
{render_frontmatter(front)}
{render_toc(chapters, parts)}
{body}
</main>
<button class="totop" aria-label="Back to top">Top ↑</button>
{js}
</body>
</html>
"""


def main():
    if not DOCX_PATH.exists():
        sys.exit(f"DOCX not found: {DOCX_PATH}")

    chapters, parts, front = parse_docx(DOCX_PATH)
    OUT_PATH.write_text(render_book(chapters, parts, front), encoding="utf-8")

    print(f"Wrote {OUT_PATH.name}")
    print(f"  Chapters:        {sum(1 for c in chapters if not c.interlude and c.number > 0)}")
    print(f"  Interludes:      {sum(1 for c in chapters if c.interlude)}")
    print(f"  Parts:           {len(parts)}")
    print(f"  Total bytes:     {OUT_PATH.stat().st_size:,}")


if __name__ == "__main__":
    main()
