# Production Workflow

> How to edit, build, and produce the book.

---

## The Editing Workflow

### Master Document
**`Architecture-of-Wonder.docx`** is the single source of truth for all content.

Edit this file in Word, Google Docs, or any DOCX editor. All 40 chapters, glossary, T4 appendix, Meta Reveal, and About the Author live here.

### What Lives Where
| Content | Location | Editable? |
|---------|----------|-----------|
| All chapter text | Architecture-of-Wonder.docx | Yes — this is your working document |
| Hook lines (chapter openers) | build-book.py + design-reference/chapter-template.md | Yes — update both when changing |
| Key reads (chapter closers) | build-book.py + design-reference/chapter-template.md | Yes — update both when changing |
| Design specs | design-reference/design-specification.md | Reference only |
| SVG graphics | design-reference/graphics/ | Reference — final graphics will be production files |
| Book figures/photos | resources/metv-images/ | Yes — drop image files here |
| Figure placement map | build-book.py (FIGURES dict) | Yes — Claude updates when you add/move figures |

### Updating the Meta Reveal
When any design decision changes (new hook lines, different color choices, different chapter structure), the Meta Reveal chapter must be updated to match. The Meta Reveal explicitly references:
- The cover (soft-touch matte, embossed title, spot UV hidden text)
- The color arc (cool → warm progression)
- The typography (Garamond, 11pt, cream background)
- The chapter openers (hook lines)
- The key reads (chapter closers)
- The pattern interrupts (every 8-12 pages)
- The margin icons (BP/CR/VS/AM)
- The page architecture (recto bias)
- The paper (cream, uncoated)
- The edge colors (7-shade thumb index)
- The "What You Just Did" moments

**If you change any of these, update the Meta Reveal to match.** The reveal only works if it accurately describes what the reader actually experienced.

---

## The Build Workflow

### Step 1: Extract text from DOCX
The build script reads `manuscript-extracted.txt` (a plain-text extraction of the DOCX).

To re-extract after editing the DOCX:
```bash
python3 -c "
import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile('Architecture-of-Wonder.docx', 'r') as z:
    doc_xml = z.read('word/document.xml')

ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
root = ET.fromstring(doc_xml)
body = root.find('.//w:body', ns)

with open('manuscript-extracted.txt', 'w') as f:
    for p in body.findall('.//w:p', ns):
        text = ''.join(r.text or '' for r in p.findall('.//w:r/w:t', ns))
        f.write(text + '\n')
"
```

### Step 2: Generate designed HTML
```bash
python3 build-book.py
```

This produces `Architecture-of-Wonder-DESIGNED.html` with:
- All design system elements (colors, typography, layout)
- Hook lines and key reads for every chapter
- Pattern interrupts, spotlight boxes, tier badges
- Margin icons, marginalia zones
- The full color arc (cool → warm)
- Running headers and page numbers
- The Meta Reveal with full dark treatment
- Figures/photos injected at the correct locations (from `FIGURES` dict)

### Step 3: View and export
Open `Architecture-of-Wonder-DESIGNED.html` in a browser. Print to PDF for the formatted version.

---

## DOCX Manipulation (Programmatic)

### Approach
The DOCX format is a ZIP file containing XML. We use Python's `zipfile` and `xml.etree.ElementTree` to manipulate it directly (no external dependencies).

### Key namespace
```python
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
```

### Reading paragraphs
```python
with zipfile.ZipFile('Architecture-of-Wonder.docx', 'r') as z:
    doc_xml = z.read('word/document.xml')

root = ET.fromstring(doc_xml)
body = root.find('.//w:body', ns)

for p in body.findall('.//w:p', ns):
    text = ''.join(r.text or '' for r in p.findall('.//w:r/w:t', ns))
```

### Inserting paragraphs
```python
new_p = ET.SubElement(body, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p')
new_r = ET.SubElement(new_p, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r')
new_t = ET.SubElement(new_r, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t')
new_t.text = "Your text here"
new_t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')

# Move to desired position
body.remove(new_p)
body.insert(target_position, new_p)
```

### Writing back
```python
new_doc_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + \
    ET.tostring(root, encoding='unicode', xml_declaration=False)

with zipfile.ZipFile('file.docx', 'r') as zin:
    with zipfile.ZipFile('file.tmp', 'w') as zout:
        for item in zin.infolist():
            if item.filename == 'word/document.xml':
                zout.writestr(item, new_doc_xml)
            else:
                zout.writestr(item, zin.read(item.filename))

os.replace('file.tmp', 'file.docx')
```

### Important: Register namespaces
Always register OOXML namespaces before writing to avoid `ns0:` prefixes:
```python
ET.register_namespace('w', 'http://schemas.openxmlformats.org/wordprocessingml/2006/main')
ET.register_namespace('r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')
# ... etc
```

### Gotcha: Element positions shift after insertions/removals
After inserting or removing elements, re-read `list(body)` before using position-based indexing again.

---

## Adding Figures and Photos

### The workflow
1. Prepare the image (Canva, Photoshop, camera, whatever you like)
2. Save it to `resources/metv-images/` with a descriptive filename (e.g., `seven-universal-expressions.png`)
3. Tell Claude where it goes (e.g., "put this after The Seven Expressions in Chapter 10")
4. Claude will:
   - Embed the image into the DOCX at the right position (visible when you open in Word/Docs)
   - Add a `FIGURES` entry in `build-book.py` so the HTML build includes it
   - Add a caption (which you can revise)

### How it works technically
- **In the DOCX:** Images are embedded as inline drawings in OOXML format (`word/media/`), with a relationship entry and content type. The image appears in Word/Google Docs.
- **In the HTML build:** The `FIGURES` dictionary in `build-book.py` maps `"CHAPTER <num>:<section header>"` to figure data. After the build script renders a section header, it checks for a matching figure and injects the `<img>` tag with caption.
- **Caption deduplication:** The build script skips extracted text lines matching `Figure X.X —` to avoid duplicate captions (one from DOCX extraction, one from the FIGURES config).

### Important notes
- The `CHAPTER <num>` in the FIGURES key uses the **parser's chapter number** (from `parse_manuscript()`), not the TOC number. These can differ. When in doubt, run the parser to check.
- Always back up the DOCX before embedding images (`backups/` directory).
- Image rights status is tracked in the `rights` field of each FIGURES entry.

### Current figures
| Figure | Chapter | Section | File | Rights |
|--------|---------|---------|------|--------|
| 10.1 | The Micro-Expression Matrix | The Seven Expressions | `seven-universal-expressions.png` | Author-owned |

---

## Git Workflow

- All changes committed to feature branch `claude/book-writing-organization-5csut`
- Commit messages describe what changed and why
- DOCX is binary — diffs won't show content changes, so commit messages must be descriptive
- Backups stored in `backups/` before major edits
