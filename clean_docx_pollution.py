"""Clean structural pollution from the DOCX:

1. Delete running-header paragraphs ("BUILT FOR WONDER | VANISHING INC").
2. Strip leading `□` from checklist paragraphs (matches the pattern Chris used
   in audit fix #29).
3. Fix specific word-mashes the build inherits from the merged source.
4. Fix 2 double periods that survived pass 1/2.

Backs up to backups/ before writing.
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
W_BODY = f"{{{W_NS}}}body"
ET.register_namespace("w", W_NS)


# Word-mash & punctuation fixes that go through paragraph-level replacement.
TEXT_FIXES: list[tuple[str, str]] = [
    # double periods
    ("performing will experience it again..", "performing will experience it again."),
    ("or different than expected..", "or different than expected."),
    # CamelCase word-mashes from radar list (Ch9)
    ("AppearanceMovementTerritorySocial ConfidenceCognitive ProcessingEmotional Regulation",
     "Appearance, Movement, Territory, Social Confidence, Cognitive Processing, Emotional Regulation"),
    # Anthem & Aria — Field Advice section header
    ("Anthem & AriaField Advice", "Anthem & Aria — Field Advice"),
    # Example labels mashed with first word of paragraph
    ("ExampleTalk casually about celebrities", "Example: Talk casually about celebrities"),
    ("ExampleWhen dealing cards onto a table", "Example: When dealing cards onto a table"),
    ("ExampleForce Paris", "Example: Force Paris"),
    # Colin Cloud — Framework
    ("Colin CloudFramework", "Colin Cloud — Framework"),
    # Mid-paragraph stray □ after Ch29 follow-up checklist line bled into next item
    ("send within 24 hours.□Show recap is designed",
     "send within 24 hours. Show recap is designed"),
]


def fix_paragraph_text(p: ET.Element, old: str, new: str) -> bool:
    text_nodes = p.findall(f".//{W_T}")
    if not text_nodes:
        return False
    joined = "".join(t.text or "" for t in text_nodes)
    if old not in joined:
        return False
    text_nodes[0].text = joined.replace(old, new, 1)
    text_nodes[0].set(f"{{{XML_NS}}}space", "preserve")
    for t in text_nodes[1:]:
        t.text = ""
        t.set(f"{{{XML_NS}}}space", "preserve")
    return True


def main() -> int:
    BACKUPS.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = BACKUPS / f"Architecture-of-Wonder-pre-pollution-clean-{ts}.docx"
    shutil.copy2(DOCX, backup)
    print(f"Backed up DOCX -> {backup.name}")

    with zipfile.ZipFile(DOCX, "r") as zin:
        names = zin.namelist()
        files = {name: zin.read(name) for name in names}

    root = ET.fromstring(files["word/document.xml"])
    body = root.find(W_BODY)

    # 1. Delete running-header paragraphs.
    deleted_running = 0
    to_remove = []
    for p in list(body):
        if p.tag != W_P:
            continue
        text = "".join((t.text or "") for t in p.findall(f".//{W_T}"))
        # Match "BUILT FOR WONDER" + "VANISHING" with any whitespace/separator
        if "BUILT FOR WONDER" in text and "VANISHING" in text:
            to_remove.append(p)
    for p in to_remove:
        body.remove(p)
        deleted_running += 1
    print(f"\n[ok] Deleted {deleted_running} 'BUILT FOR WONDER | VANISHING INC' running-header paragraphs")

    # 2. Strip leading □ from paragraphs.
    stripped_box = 0
    for p in root.iter(W_P):
        text_nodes = p.findall(f".//{W_T}")
        if not text_nodes:
            continue
        joined = "".join(t.text or "" for t in text_nodes)
        if not joined.lstrip().startswith("□"):
            continue
        # remove leading whitespace+□+optional whitespace, and replace with empty
        # so build emits these as regular paragraph items.
        new = joined.lstrip()
        if new.startswith("□"):
            new = new[1:].lstrip()
        # preserve leading whitespace from original to keep paragraph indent
        leading_ws = joined[: len(joined) - len(joined.lstrip())]
        text_nodes[0].text = leading_ws + new
        text_nodes[0].set(f"{{{XML_NS}}}space", "preserve")
        for t in text_nodes[1:]:
            t.text = ""
            t.set(f"{{{XML_NS}}}space", "preserve")
        stripped_box += 1
    print(f"[ok] Stripped leading □ from {stripped_box} paragraphs")

    # 3+4. Apply text fixes.
    print()
    paragraphs = list(root.iter(W_P))
    for old, new in TEXT_FIXES:
        count = 0
        for p in paragraphs:
            if fix_paragraph_text(p, old, new):
                count += 1
        if count:
            print(f"[ok]   {old[:60]!r} -> {new[:60]!r} (x{count})")
        else:
            print(f"[skip] {old[:60]!r} not found")

    # Write back.
    body_xml = ET.tostring(root, encoding="UTF-8", xml_declaration=False)
    files["word/document.xml"] = b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + body_xml

    with zipfile.ZipFile(DOCX, "w", zipfile.ZIP_DEFLATED) as zout:
        for name in names:
            zout.writestr(name, files[name])

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
