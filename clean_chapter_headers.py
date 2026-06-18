"""Strip 'BUILT FOR WONDER' prefix from chapter-heading paragraphs and delete
standalone 'VANISHING INC.' paragraphs.

Pattern: 'BUILT FOR WONDERCHAPTER N — TITLE' -> 'CHAPTER N — TITLE'
Also: 'BUILT FOR WONDER | CHAPTER N: TITLE' (variant) -> 'CHAPTER N: TITLE'
"""
from __future__ import annotations
import re
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


def main() -> int:
    BACKUPS.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = BACKUPS / f"Architecture-of-Wonder-pre-header-strip-{ts}.docx"
    shutil.copy2(DOCX, backup)
    print(f"Backed up DOCX -> {backup.name}")

    with zipfile.ZipFile(DOCX, "r") as zin:
        names = zin.namelist()
        files = {name: zin.read(name) for name in names}

    root = ET.fromstring(files["word/document.xml"])
    body = root.find(W_BODY)

    stripped = 0
    deleted = 0
    to_remove = []

    for p in list(body.iter(W_P)):
        text_nodes = p.findall(f".//{W_T}")
        if not text_nodes:
            continue
        joined = "".join(t.text or "" for t in text_nodes)

        # Delete standalone VANISHING paragraphs
        if joined.strip() in ("VANISHING INC.", "VANISHING INC"):
            to_remove.append(p)
            deleted += 1
            continue

        # Strip "BUILT FOR WONDER" prefix when followed by another heading
        # (CHAPTER, INTRODUCTION, ABOUT, AUTHORITY, THE META REVEAL, etc.).
        # Keep the rest of the paragraph intact.
        m = re.match(r"^BUILT FOR WONDER\s*\|?\s*([A-Z].*)", joined, flags=re.DOTALL)
        if m and joined.strip() != "BUILT FOR WONDER":
            new = m.group(1)
            # Also strip trailing 'BUILT FOR WONDER | ...' (DISC paragraph variant)
            new = re.sub(r"\s*BUILT FOR WONDER\s*\|.*$", "", new, flags=re.DOTALL)
            text_nodes[0].text = new
            text_nodes[0].set(f"{{{XML_NS}}}space", "preserve")
            for t in text_nodes[1:]:
                t.text = ""
                t.set(f"{{{XML_NS}}}space", "preserve")
            stripped += 1
            continue

        # Strip TRAILING running-header text from any paragraph (e.g., the
        # DISC mega-paragraph ends with 'BUILT FOR WONDER | CHAPTER 8: ...').
        m_trail = re.search(r"\s*BUILT FOR WONDER\s*\|\s*[A-Z].*$", joined, flags=re.DOTALL)
        if m_trail and not joined.startswith("BUILT FOR WONDER"):
            new = joined[: m_trail.start()].rstrip()
            text_nodes[0].text = new
            text_nodes[0].set(f"{{{XML_NS}}}space", "preserve")
            for t in text_nodes[1:]:
                t.text = ""
                t.set(f"{{{XML_NS}}}space", "preserve")
            stripped += 1

    # Remove standalone paragraphs from body. Iterate body's direct children;
    # if a target paragraph is a descendant (e.g., inside a table), unparenting
    # is more involved — just blank it.
    body_children = list(body)
    for p in to_remove:
        if p in body_children:
            body.remove(p)
        else:
            # blank instead
            for t in p.findall(f".//{W_T}"):
                t.text = ""

    print(f"\n[ok] Stripped 'BUILT FOR WONDER' prefix from {stripped} chapter headings")
    print(f"[ok] Deleted/blanked {deleted} 'VANISHING INC.' paragraphs")

    body_xml = ET.tostring(root, encoding="UTF-8", xml_declaration=False)
    files["word/document.xml"] = b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + body_xml

    with zipfile.ZipFile(DOCX, "w", zipfile.ZIP_DEFLATED) as zout:
        for name in names:
            zout.writestr(name, files[name])

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
