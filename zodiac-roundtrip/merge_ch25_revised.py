#!/usr/bin/env python3
"""Merge the revised Zodiac chapter (revised-full.html — the source of the
chrismichael.site/zodiac page) into the master Built-for-Wonder.docx,
replacing the old Chapter 25 body wholesale.

Rules (per the production notes embedded in revised-full.html):
  - New chapter title propagates to the opener paragraph, the running
    header line, and the DOCX table of contents.
  - Bracketed italic notes and the REVISED-DRAFT preamble are editor
    chrome, not book text: dropped.
  - <img> previews (renders of the designed build) are dropped; the
    marker tokens (T2T3, KEY PRINCIPLE, ZODIAC_ELEMENT_TABLE, ...) stay.
  - The drafted three-block element list is dropped from the manuscript;
    the designed ZODIAC_ELEMENT_TABLE gets rebuilt in build-book.py in
    that layout instead.
  - Performance-script paragraphs keep the literal [ITALIC]...[/ITALIC]
    marker convention the build pipeline expects (single paragraph each).

The lead-in paragraphs (title, epigraph, badge tokens, running header —
master body indices 2853..2859) are reused verbatim from the master so
their formatting and bookmarks survive; only the two title texts change.
"""
import copy
import html as htmllib
import re
import shutil
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MASTER = ROOT.parent / "Built-for-Wonder.docx"
SRC = ROOT / "revised-full.html"
TXT = ROOT / "ch25-REVISED-chris-edits.txt"
BACKUP_DIR = ROOT.parent / "backups"

NEW_TITLE = "ZODIAC DIVINATIONS THAT FOOLED THE GREATEST MENTALISTS"
NEW_TITLE_TC = "Zodiac Divinations That Fooled the Greatest Mentalists"
OLD_TITLE_TC = "Zodiac Divinations Without Anagrams"
RUNNING_HEADER = f"CHAPTER 25 — {NEW_TITLE}"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
ET.register_namespace("w", W)
ET.register_namespace("r", "http://schemas.openxmlformats.org/officeDocument/2006/relationships")
ET.register_namespace("w14", "http://schemas.microsoft.com/office/word/2010/wordml")


def q(tag):
    return f"{{{W}}}{tag}"


def para_text(el):
    return "".join(t.text or "" for t in el.iter(q("t")))


def norm(s):
    return re.sub(r"\s+", " ", (s or "")).strip()


# ── 1. Parse revised-full.html into ordered blocks ──────────────────
class Parser(HTMLParser):
    """Blocks: (tag, [(text, italic, bold), ...]). img/meta ignored."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks = []
        self.tag = None
        self.segs = []
        self.italic = 0
        self.bold = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("h1", "h2", "h3", "p"):
            self.tag = tag
            self.segs = []
        elif tag == "em":
            self.italic += 1
        elif tag == "strong":
            self.bold += 1
        elif tag == "br":
            self.segs.append(("\n", False, False))

    def handle_endtag(self, tag):
        if tag in ("h1", "h2", "h3", "p"):
            if self.tag:
                self.blocks.append((self.tag, self.segs))
            self.tag = None
        elif tag == "em":
            self.italic = max(0, self.italic - 1)
        elif tag == "strong":
            self.bold = max(0, self.bold - 1)

    def handle_data(self, data):
        if self.tag and data:
            self.segs.append((data, self.italic > 0, self.bold > 0))


parser = Parser()
parser.feed(SRC.read_text(encoding="utf-8"))
blocks = parser.blocks

# ── 2. Clean the block list ─────────────────────────────────────────
# Script blocks that must keep literal [ITALIC] markers, matched by text.
script_texts = {
    norm(b) for b in re.findall(r"\[ITALIC\](.*?)\[/ITALIC\]",
                                TXT.read_text(encoding="utf-8"), re.S)
}

LEAD_IN_SKIP = {
    '"The method disappears when the frame is large enough."',
    "T2T3", "SIGNAL CONFIDENCE TIERS", "CR", "OBSERVATION CATEGORIES",
}

content = []       # (kind, segs) with kind in body/header/script
stats = {"notes": 0, "scripts": 0, "italic_asides": 0}
for tag, segs in blocks:
    # strip inline bracketed italic notes, then rebuild text
    segs = [s for s in segs
            if not (s[1] and s[0].strip().startswith("[") and s[0].strip().endswith("]"))]
    text = norm("".join(s[0] for s in segs))
    if not text:
        continue
    if text.startswith("REVISED DRAFT, for your review"):
        continue
    if text.startswith("[") and text.endswith("]"):
        stats["notes"] += 1
        continue
    if tag == "h1":
        assert text == NEW_TITLE, f"unexpected h1: {text!r}"
        continue  # handled via the reused master title paragraph
    if text in LEAD_IN_SKIP or text.startswith("CHAPTER 25"):
        continue  # reused verbatim from master lead-in
    if text.startswith("Beginning of the year:"):
        continue  # drafted element table -> becomes the designed table
    whole_italic = segs and all(s[1] for s in segs)
    if whole_italic and text in script_texts:
        stats["scripts"] += 1
        content.append(("script", [(f"[ITALIC]{text}[/ITALIC]", True, False)]))
        continue
    if whole_italic:
        stats["italic_asides"] += 1
    kind = "header" if tag in ("h2", "h3") else "body"
    cleaned = [(re.sub(r"\s+", " ", s[0]), s[1], s[2]) for s in segs]
    if cleaned:
        cleaned[0] = (cleaned[0][0].lstrip(), cleaned[0][1], cleaned[0][2])
        cleaned[-1] = (cleaned[-1][0].rstrip(), cleaned[-1][1], cleaned[-1][2])
    content.append((kind, cleaned))

print(f"content paragraphs: {len(content)}  {stats}")
assert stats["scripts"] == 6, "expected exactly 6 [ITALIC] script blocks"

# ── 3. Load master, locate chapter boundaries ───────────────────────
with zipfile.ZipFile(MASTER) as z:
    doc_xml = z.read("word/document.xml")
root = ET.fromstring(doc_xml)
body = root.find(q("body"))
children = list(body)

start = end = None
for i, el in enumerate(children):
    t = norm(para_text(el))
    if start is None and t == "ZODIAC DIVINATIONS WITHOUT ANAGRAMS":
        start = i
    elif start is not None and t == "IS PRE-SHOW WORTH IT?":
        end = i
        break
assert start is not None and end is not None, "boundary detection failed"
picked = list(range(start, end))
while picked and norm(para_text(children[picked[-1]])) in ("PART THREE", "26", ""):
    picked.pop()
last = picked[-1]
assert norm(para_text(children[last])).startswith("The zodiac is a frame"), \
    f"unexpected chapter end: {para_text(children[last])!r}"
print(f"replacing master paragraphs {start}..{last} ({len(picked)} paras)")

# ── 4. Templates ────────────────────────────────────────────────────
def template_at(text_probe):
    for el in children[start:last + 1]:
        if norm(para_text(el)) == text_probe:
            return el
    sys.exit(f"template not found: {text_probe!r}")


TPL_BODY = template_at("If you have seen me perform a zodiac divination, you will notice that I do not get any verbal yes or no. I simply ask the person to picture when in the year they are born, and then which part of that month they are born in. With as little as that, I am able to name the zodiac on the first attempt.")
TPL_HEADER = template_at("The Half-Year Split")


def set_para_text(el, new_text):
    """Replace all runs of el with one run cloned from its first run."""
    runs = el.findall(q("r"))
    assert runs, "paragraph has no runs"
    proto = copy.deepcopy(runs[0])
    for t in proto.findall(q("t")):
        proto.remove(t)
    t = ET.SubElement(proto, q("t"))
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    t.text = new_text
    for r in runs:
        el.remove(r)
    el.append(proto)


def make_para(tpl, segs):
    """Clone tpl's pPr/run formatting; fill with segs (text, italic, bold)."""
    el = copy.deepcopy(tpl)
    runs = el.findall(q("r"))
    proto = copy.deepcopy(runs[0])
    for r in runs:
        el.remove(r)
    for text, italic, bold in segs:
        if not text:
            continue
        r = copy.deepcopy(proto)
        for t in r.findall(q("t")):
            r.remove(t)
        rpr = r.find(q("rPr"))
        if rpr is None:
            rpr = ET.SubElement(r, q("rPr"))
        if italic and rpr.find(q("i")) is None:
            i = ET.SubElement(rpr, q("i"))
            i.set(q("val"), "1")
            ic = ET.SubElement(rpr, q("iCs"))
            ic.set(q("val"), "1")
        if bold and rpr.find(q("b")) is None:
            b = ET.SubElement(rpr, q("b"))
            b.set(q("val"), "1")
            bc = ET.SubElement(rpr, q("bCs"))
            bc.set(q("val"), "1")
        if text == "\n":
            ET.SubElement(r, q("br"))
        else:
            t = ET.SubElement(r, q("t"))
            t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            t.text = htmllib.unescape(text)
        el.append(r)
    return el


# ── 5. Build the new chapter sequence ───────────────────────────────
lead_in = [copy.deepcopy(children[i]) for i in range(start, start + 7)]
assert norm(para_text(lead_in[0])) == "ZODIAC DIVINATIONS WITHOUT ANAGRAMS"
assert norm(para_text(lead_in[6])).startswith("CHAPTER 25")
set_para_text(lead_in[0], NEW_TITLE)
set_para_text(lead_in[6], RUNNING_HEADER)

new_paras = list(lead_in)
for kind, segs in content:
    tpl = TPL_HEADER if kind == "header" else TPL_BODY
    new_paras.append(make_para(tpl, segs))

# ── 6. TOC entry ────────────────────────────────────────────────────
toc_hits = 0
for el in children[:start]:
    for t in el.iter(q("t")):
        if t.text and OLD_TITLE_TC in t.text:
            t.text = t.text.replace(OLD_TITLE_TC, NEW_TITLE_TC)
            toc_hits += 1
print(f"TOC replacements: {toc_hits}")
assert toc_hits == 1, "expected exactly one TOC entry"

# ── 7. Splice and write ─────────────────────────────────────────────
for el in children[start:last + 1]:
    body.remove(el)
for offset, el in enumerate(new_paras):
    body.insert(start + offset, el)

BACKUP_DIR.mkdir(exist_ok=True)
backup = BACKUP_DIR / f"Built-for-Wonder.pre-ch25-merge-{date.today().isoformat()}.docx"
if not backup.exists():
    shutil.copy2(MASTER, backup)
    print(f"backup: {backup.name}")

new_doc = ET.tostring(root, xml_declaration=True, encoding="UTF-8")
tmp = MASTER.with_suffix(".tmp.docx")
with zipfile.ZipFile(MASTER) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = new_doc if item.filename == "word/document.xml" else zin.read(item.filename)
        zout.writestr(item, data)
tmp.replace(MASTER)

# ── 8. Verify ───────────────────────────────────────────────────────
with zipfile.ZipFile(MASTER) as z:
    root2 = ET.fromstring(z.read("word/document.xml"))
paras = [para_text(el) for el in root2.find(q("body"))]
texts = [norm(t) for t in paras]
i_title = texts.index(NEW_TITLE)
i_end = texts.index("IS PRE-SHOW WORTH IT?")
chapter = [t for t in texts[i_title:i_end]]
print(f"merged chapter: {len(chapter)} paragraphs (incl. ch26 lead-in tail)")
for probe in (RUNNING_HEADER, "A Note Before We Go Further",
              "Think Like a Creator, Not a Customer", "ZODIAC_ELEMENT_TABLE",
              '#2: "Symbols of Ignorance" by Chris Michael',
              "The zodiac is a frame. What you put inside it is the work."):
    assert any(norm(probe) == t for t in chapter), f"missing: {probe!r}"
assert sum(1 for t in chapter if t.startswith("[ITALIC]")) == 6
assert not any(t.startswith("[NOTE") or t.startswith("[PRODUCTION") for t in chapter)
assert NEW_TITLE_TC in " ".join(texts[:start])
print("verification passed")
