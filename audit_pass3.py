"""Pass 3 audit — scan DESIGNED.html for issues not covered by passes 1-2.

Categories:
1. Common typos (extends past audit watchlist)
2. Formatting: double spaces, double periods, mixed straight/curly quotes
3. Word-mash patterns (NN — XX with no space, headingFollowed by paragraph text)
4. Stray glyphs (□, |, orphan ✦)
5. Suspicious whitespace (paragraph-internal triple spaces, stray tabs)

Reports findings only — does not auto-fix. Outputs a list of (category, location, snippet)
for human review or for codifying into a backport script.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

SRC = Path(__file__).parent / "Architecture-of-Wonder-DESIGNED.html"

html = SRC.read_text(encoding="utf-8")

# Strip HTML tags for prose-only checks (rough but adequate)
prose = re.sub(r"<[^>]+>", " ", html)
# Decode common entities
prose = (prose
         .replace("&nbsp;", " ")
         .replace("&amp;", "&")
         .replace("&#8217;", "’")
         .replace("&#8220;", "“")
         .replace("&#8221;", "”")
         .replace("&#8212;", "—")
         .replace("&#8211;", "–"))


def report(category: str, matches: list[str], limit: int = 10):
    if not matches:
        return
    print(f"\n[{category}] — {len(matches)} hits")
    for m in matches[:limit]:
        print(f"  • {m}")
    if len(matches) > limit:
        print(f"  ... and {len(matches) - limit} more")


# ----------------------------------------------------------------------
# 1. Common typos watchlist
# ----------------------------------------------------------------------
TYPOS = [
    # double-letter / dropped-letter classics
    "thier", "wierd", "recieve", "occured", "untill", "tommorrow",
    "definately", "seperate", "begining", "noticable", "publically",
    "occassion", "occassional", "accomodate", "embarass",
    # mentalism / book-specific
    "audeince", "audnece", "audiance", "emtional", "emotinal",
    "behavoir", "behaviuor", "psycology", "psycological",
    "mentalsim", "mentlaist", "mentlist", "performence", "performace",
    # mash-ups (no space between words)
    "ofthe", "andthe", "tothe", "isnota", "tobe", "infront",
]
hits = []
for typo in TYPOS:
    pattern = re.compile(rf"\b{re.escape(typo)}\b", re.IGNORECASE)
    for m in pattern.finditer(prose):
        s = max(0, m.start() - 40); e = min(len(prose), m.end() + 40)
        hits.append(f"{typo!r}: …{prose[s:e].strip()}…")
report("Common typos", hits, limit=20)

# ----------------------------------------------------------------------
# 2a. Double spaces between words in prose
# ----------------------------------------------------------------------
hits = []
for m in re.finditer(r"\w+  +\w+", prose):
    snippet = m.group()
    # Skip if it's just multiple spaces from tag stripping (likely)
    s = max(0, m.start() - 30); e = min(len(prose), m.end() + 30)
    context = prose[s:e]
    # Heuristic: if context is mostly whitespace, skip
    if context.count("  ") > 3:
        continue
    hits.append(f"…{context.strip()}…")
# Dedupe
seen = set(); unique = []
for h in hits:
    if h not in seen:
        seen.add(h); unique.append(h)
report("Double spaces between words", unique, limit=15)

# ----------------------------------------------------------------------
# 2b. Double periods (..) and double punctuation (,, !! ??)
# ----------------------------------------------------------------------
hits = []
for m in re.finditer(r"[a-z]\.\.\s+[A-Z]|[a-z]\.\.[a-z]|,,|!!|\?\?", prose):
    s = max(0, m.start() - 30); e = min(len(prose), m.end() + 30)
    hits.append(f"…{prose[s:e].strip()}…")
report("Doubled punctuation", hits, limit=10)

# ----------------------------------------------------------------------
# 2c. Apostrophe issues — straight ' inside otherwise-curly prose
# ----------------------------------------------------------------------
hits = []
for m in re.finditer(r"\b\w+'\w+\b", prose):
    word = m.group()
    # Skip code-y stuff
    if any(c in word for c in "<>=/"):
        continue
    s = max(0, m.start() - 30); e = min(len(prose), m.end() + 30)
    hits.append(f"{word!r}: …{prose[s:e].strip()}…")
report("Straight apostrophes (likely should be curly)", hits, limit=10)

# ----------------------------------------------------------------------
# 3. Heading-paragraph mashes: e.g., "FastDecisive", "OneTwoThree"
# Two consecutive capitalized words with no space, len > 8, in prose
# ----------------------------------------------------------------------
hits = []
for m in re.finditer(r"\b([A-Z][a-z]{2,})([A-Z][a-z]{2,})\b", prose):
    word = m.group()
    # Skip obvious legitimate compounds (TitleCase usage in URLs, etc)
    if word in {"PowerPoint", "JavaScript", "ChatGPT", "OpenAI", "BlackBerry",
                "PostMortem", "ProQuest", "PubMed", "JStor", "GoogleScholar",
                "TikTok", "iPhone", "MacBook", "FaceTime", "FaceBook"}:
        continue
    s = max(0, m.start() - 30); e = min(len(prose), m.end() + 30)
    hits.append(f"{word!r}: …{prose[s:e].strip()}…")
# Dedupe
seen = set(); unique = []
for h in hits:
    key = h.split(":")[0]
    if key not in seen:
        seen.add(key); unique.append(h)
report("CamelCase word-mashes (likely missing space)", unique, limit=15)

# ----------------------------------------------------------------------
# 4. Stray glyphs and orphan markers
# ----------------------------------------------------------------------
GLYPHS = [
    ("□", "stray box glyph"),
    ("◇", "stray diamond"),
    ("◆", "stray filled diamond"),
    ("|", "stray pipe (in prose)"),
    ("  ", "double non-breaking space"),
    ("﻿", "BOM character"),
]
for glyph, label in GLYPHS:
    matches = []
    for m in re.finditer(re.escape(glyph), prose):
        s = max(0, m.start() - 40); e = min(len(prose), m.end() + 40)
        snippet = prose[s:e].strip()
        # Skip pipes inside table-like content (heuristic: short adjacent words)
        if glyph == "|" and re.search(r"\d\s*\|\s*\d", snippet):
            continue
        matches.append(f"…{snippet}…")
    report(f"Glyph: {label} ({glyph!r})", matches, limit=5)

# ----------------------------------------------------------------------
# 5. Empty paragraphs (<p></p> or <p>\s*</p>) and orphan empty headings
# ----------------------------------------------------------------------
empty_p = len(re.findall(r"<p[^>]*>\s*</p>", html))
empty_h = len(re.findall(r"<h[1-6][^>]*>\s*</h[1-6]>", html))
print(f"\n[Empty tags]\n  empty <p>: {empty_p}\n  empty <h*>: {empty_h}")

# ----------------------------------------------------------------------
# 6. TODO/FIXME residue
# ----------------------------------------------------------------------
todo = re.findall(r"\b(?:TODO|FIXME|TKTK|TK\b|\[needs?[^\]]+\])", prose)
if todo:
    print(f"\n[TODO residue]\n  hits: {len(todo)}")
    for t in todo[:10]:
        print(f"  • {t}")

print("\n=== End of pass 3 audit ===")
