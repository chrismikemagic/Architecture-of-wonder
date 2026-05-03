#!/usr/bin/env python3
"""
Extract the manuscript from Architecture-of-Wonder.docx into manuscript-extracted.txt
in the format build-book.py's parser expects: explicit "CHAPTER N" / "PART X" markers
inferred from Word Heading 1/2/3 styles.

Heading-style heuristic for the new "Built for Wonder" merged DOCX:
  - Heading 1 ALL CAPS  -> chapter title  (auto-numbered)
  - Heading 1 Title Case -> part divider  (mapped to PART ONE..FIVE in order)
  - Heading 1 "THE META REVEAL" -> special, emitted verbatim
  - Heading 1 "CONTROLLING THE ROOM" -> interlude, emitted verbatim (no chapter number)
  - Heading 1 "sw" or empty -> junk, skipped
  - Heading 2 / 3 -> emitted verbatim (parser treats them as content / section headers)
"""

import re
import sys
from pathlib import Path

from docx import Document

DOCX_PATH = Path(__file__).parent / "Architecture-of-Wonder.docx"
OUT_PATH  = Path(__file__).parent / "manuscript-extracted.txt"

PART_ORDINALS = ["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT"]

# Heading-1 strings that are part dividers, not chapter titles.
# Order matches the book's part order. Match is case-insensitive on text only.
PART_TITLES = [
    "Built for Wonder",
    "Reading the Room",
    "The Methods",
    "Performance Craft",
    "Authority, Influence & The Deep Framework",
]

# Heading-1 strings that are special / not chapters
SPECIAL_VERBATIM = {
    "THE META REVEAL",
    "CONTROLLING THE ROOM",   # unnumbered interlude between CH 37 and 38
}

# Headings whose Word-level text is corrupted but which represent a real chapter.
# Maps the corrupted Heading-1 text -> the title we should emit instead.
# (Verified against running-header text inside the DOCX, e.g.
#  "BUILT FOR WONDERCHAPTER 22 — MAKING BETTER PROPLESS MENTALISM".)
CORRUPTED_HEADING_FIXUPS = {
    "sw": "MAKING BETTER PROPLESS MENTALISM",
}

# Junk headings to skip outright (empty H1s)
JUNK_HEADINGS = {""}

# Chapter titles that should be Heading 1 in the DOCX but are stuck on
# 'normal' style. We promote them to chapter breaks when we encounter them
# in the body text. First occurrence only — subsequent occurrences are
# treated as running-header chrome and dropped.
UNSTYLED_CHAPTER_TITLES = {
    "PROPLESS SYSTEMS THAT ACTUALLY WORK",
}


def is_all_caps(text: str) -> bool:
    """True if string contains at least one letter and all letters are uppercase."""
    letters = [c for c in text if c.isalpha()]
    return bool(letters) and all(c.isupper() for c in letters)


def normalize(s: str) -> str:
    return s.strip()


def main():
    if not DOCX_PATH.exists():
        sys.exit(f"DOCX not found: {DOCX_PATH}")

    doc = Document(str(DOCX_PATH))

    out_lines = []
    chapter_counter = 0
    part_index = 0  # which PART_ORDINALS slot we are on
    promoted_unstyled = set()  # titles already promoted to chapter once
    in_toc = False  # we drop the entire TOC; build-book.py renders its own

    for p in doc.paragraphs:
        style = p.style.name if p.style else ""
        text  = normalize(p.text)

        # TOC skipping — Heading 2 "Contents" opens it, ends at the next
        # Heading 1/2 (typically "How to Read This Book").
        if in_toc:
            if style in ("Heading 1", "Heading 2"):
                in_toc = False
                # fall through to process this heading normally
            else:
                continue

        if style == "Heading 2" and text.strip().lower() == "contents":
            in_toc = True
            continue

        if style == "Heading 1":
            if text in JUNK_HEADINGS:
                continue

            # Corrupted heading -> rewrite to the real title and treat as chapter.
            if text in CORRUPTED_HEADING_FIXUPS:
                text = CORRUPTED_HEADING_FIXUPS[text]
                chapter_counter += 1
                out_lines.append("")
                out_lines.append(f"CHAPTER {chapter_counter}")
                out_lines.append(text)
                out_lines.append("")
                continue

            if text in SPECIAL_VERBATIM:
                out_lines.append("")
                out_lines.append(text)
                out_lines.append("")
                continue

            # Part divider?  Match by exact (case-sensitive) title or by title-case heuristic.
            is_part = False
            matched_part_title = None
            for pt in PART_TITLES:
                if text == pt:
                    is_part = True
                    matched_part_title = pt
                    break

            if is_part:
                if part_index >= len(PART_ORDINALS):
                    # Defensive: more parts than expected, just skip the marker
                    out_lines.append(matched_part_title)
                    continue
                ordinal = PART_ORDINALS[part_index]
                part_index += 1
                out_lines.append("")
                out_lines.append(f"PART {ordinal}")
                out_lines.append(matched_part_title)
                out_lines.append("")
                continue

            # Otherwise treat as a chapter title (whether ALL CAPS or not — H1
            # at this point is a chapter heading)
            chapter_counter += 1
            out_lines.append("")
            out_lines.append(f"CHAPTER {chapter_counter}")
            out_lines.append(text)
            out_lines.append("")
            continue

        if style == "Heading 2":
            # Treat as front-matter section header / content.  Some H2s in this
            # DOCX are TOC-ish ("Contents"), some are real ("How to Read This
            # Book", "ACKNOWLEDGMENTS"). The build-book.py parser looks for
            # exact strings — emit as-is and uppercased for the structural ones.
            upper = text.upper()
            if upper in {"HOW TO READ THIS BOOK", "ACKNOWLEDGMENTS"}:
                out_lines.append("")
                out_lines.append(upper)
                out_lines.append("")
            else:
                # Misc H2 (like emoji-prefixed category headers in CH 17,
                # "ONE WORD TITLES", "Contents"): pass through verbatim.
                out_lines.append(text)
            continue

        if style == "Heading 3":
            # Section sub-headers — pass through verbatim, build script can
            # detect them by Title Case matching later.
            out_lines.append(text)
            continue

        # Normal / Body / unstyled paragraphs.
        # Promote certain unstyled titles to real chapter breaks (first occurrence only).
        if text in UNSTYLED_CHAPTER_TITLES and text not in promoted_unstyled:
            promoted_unstyled.add(text)
            chapter_counter += 1
            out_lines.append("")
            out_lines.append(f"CHAPTER {chapter_counter}")
            out_lines.append(text)
            out_lines.append("")
            continue

        out_lines.append(text)

    # Collapse 3+ consecutive blank lines into 2.
    cleaned = []
    blank_run = 0
    for line in out_lines:
        if line == "":
            blank_run += 1
            if blank_run <= 2:
                cleaned.append(line)
        else:
            blank_run = 0
            cleaned.append(line)

    OUT_PATH.write_text("\n".join(cleaned) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_PATH.name}")
    print(f"  Chapters detected: {chapter_counter}")
    print(f"  Parts emitted:     {part_index}")
    print(f"  Total lines:       {len(cleaned):,}")


if __name__ == "__main__":
    main()
