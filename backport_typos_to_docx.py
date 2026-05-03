"""Backport prose-level typos from the audit-fix scripts into the DOCX.

For each (old, new) pair: walk paragraphs, find the one whose joined text
contains `old`, replace once, redistribute by putting the whole new text in
the first <w:t> of that paragraph and blanking the rest. This loses
intra-paragraph run-level formatting (bold/italic mid-paragraph) but is
appropriate for plain-prose typo corrections.

Always backs up to backups/ before writing.
"""
from __future__ import annotations
import shutil
import sys
import zipfile
from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).parent
DOCX = ROOT / "Architecture-of-Wonder.docx"
BACKUPS = ROOT / "backups"

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML_NS = "http://www.w3.org/XML/1998/namespace"
W_T = f"{{{W_NS}}}t"
W_P = f"{{{W_NS}}}p"
ET.register_namespace("w", W_NS)

# (old, new) — extracted by extract_prose_fixes.py from apply_audit_fixes*.py
FIXES: list[tuple[str, str]] = [
    ("matter if you I didn’t remove those to make room",
     "matter if I didn’t remove those to make room"),
    ("Colin watched it ripped waves of laughter and excitement through the crowd",
     "Colin watched it rip through with waves of laughter and excitement"),
    ("limiting their growth and audience expereince",
     "limiting their growth and audience experience"),
    ("Its’ an uncomfortable truth.", "It’s an uncomfortable truth."),
    ("Human attention and behavior show lawful , patterns.",
     "Human attention and behavior show lawful patterns."),
    ("The saleince network helps decide", "The salience network helps decide"),
    ("the novel stimulis he presents", "the novel stimuli he presents"),
    ("gives that act social relevence", "gives that act social relevance"),
    ("Someone’s nervous system regulated the room for their own comfort..",
     "Someone’s nervous system regulated the room for their own comfort."),
    ("My mentalist brain is telling my while writing this",
     "My mentalist brain is telling me while writing this"),
    ("what tells it the payoff  is about to happen..",
     "what tells it the payoff is about to happen."),
    ("the more complaint and suggestable they will become",
     "the more compliant and suggestible they will become"),
    ("the “feel-good chemical”  that gives the feeling of reward",
     "the “feel-good chemical” that gives the feeling of reward"),
    ("In many cases whe the audience doesnt catch the method",
     "In many cases when the audience doesn’t catch the method"),
    ("pretending you can read someone sole",
     "pretending you can read someone’s soul"),
    ("are you about to get a hit or miss,  and who is carrying",
     "are you about to get a hit or miss, and who is carrying"),
    ("IF you watch interrogation videos that are uncut, often between 8-20 minutes",
     "If you watch interrogation videos that are uncut, often between 8 and 20 minutes"),
    ("Their baseline behavior is the a very valuable piece",
     "Their baseline behavior is a very valuable piece"),
    ("As the spectator hlds your body", "As the spectator holds your body"),
    ("That are availble to be used", "That are available to be used"),
    ("They aren’t going to over analyze your words or rhythm because their is something else that they can anlyze.",
     "They aren’t going to over-analyze your words or rhythm because there is something else that they can analyze."),
    ("so many mentalsits get drawn", "so many mentalists get drawn"),
    ("aboslutely", "absolutely"),
    ("More Relevent Cues", "More Relevant Cues"),
    ("voulnteer", "volunteer"),
    ("Austrailia", "Australia"),
    ("□Thank-you and follow ups designed and ready to send within 24 hours|",
     "Thank-you and follow ups designed and ready to send within 24 hours."),
    ("Shoe recap", "Show recap"),
    ("Tthe words are not the performance.",
     "The words are not the performance."),
    ("A standing ovation’s are predictable.",
     "Standing ovations are predictable."),
    ("A uthority is not something you claim.",
     "Authority is not something you claim."),
    ("availble", "available"),
    ("lcoks", "locks"),
    ("similiar", "similar"),
    ("thattakes", "that takes"),
    ("Reading the FeedbackFour signals. Four corrections.",
     "Reading the Feedback. Four signals. Four corrections."),
    ("alot", "a lot"),
    # `coffe` — word-bounded via context phrases (avoid breaking "coffee")
    ("best coffe in the world", "best coffee in the world"),
    ("coffe lover", "coffee lover"),
]


def fix_paragraph(p: ET.Element, old: str, new: str) -> bool:
    """Try to replace `old` -> `new` in paragraph `p`. Returns True if applied."""
    text_nodes = p.findall(f".//{W_T}")
    if not text_nodes:
        return False
    joined = "".join(t.text or "" for t in text_nodes)
    if old not in joined:
        return False
    new_joined = joined.replace(old, new, 1)
    text_nodes[0].text = new_joined
    text_nodes[0].set(f"{{{XML_NS}}}space", "preserve")
    for t in text_nodes[1:]:
        t.text = ""
        t.set(f"{{{XML_NS}}}space", "preserve")
    return True


def apply_fixes(root: ET.Element) -> tuple[list[tuple[str, int]], list[str]]:
    applied: list[tuple[str, int]] = []
    not_found: list[str] = []
    paragraphs = list(root.iter(W_P))
    for old, new in FIXES:
        count = 0
        for p in paragraphs:
            if fix_paragraph(p, old, new):
                count += 1
        if count > 0:
            applied.append((f"{old[:60]!r} -> {new[:60]!r}", count))
        else:
            not_found.append(old)
    return applied, not_found


def main() -> int:
    if not DOCX.exists():
        print(f"DOCX not found: {DOCX}", file=sys.stderr)
        return 2

    BACKUPS.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = BACKUPS / f"Architecture-of-Wonder-pre-prose-typo-backport-{ts}.docx"
    shutil.copy2(DOCX, backup)
    print(f"Backed up DOCX -> {backup.name}")

    with zipfile.ZipFile(DOCX, "r") as zin:
        names = zin.namelist()
        files = {name: zin.read(name) for name in names}

    root = ET.fromstring(files["word/document.xml"])
    applied, not_found = apply_fixes(root)
    body = ET.tostring(root, encoding="UTF-8", xml_declaration=False)
    files["word/document.xml"] = b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + body

    with zipfile.ZipFile(DOCX, "w", zipfile.ZIP_DEFLATED) as zout:
        for name in names:
            zout.writestr(name, files[name])

    print(f"\nApplied: {len(applied)} / {len(FIXES)}")
    for label, count in applied:
        suffix = f" (x{count})" if count > 1 else ""
        print(f"  [ok]   {label}{suffix}")
    if not_found:
        print(f"\nNot found in DOCX: {len(not_found)}")
        for n in not_found:
            print(f"  [skip] {n[:80]!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
