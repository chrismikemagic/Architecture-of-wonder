# Tips and Lessons Learned

> Practical knowledge accumulated during the development of this book project.

---

## Working with DOCX Files Programmatically

### Use zipfile + ElementTree, not python-docx
The `python-docx` library is convenient but adds a dependency. For this project, we use Python's built-in `zipfile` and `xml.etree.ElementTree` to manipulate the DOCX directly. No pip installs needed.

### Always register OOXML namespaces before writing
If you don't register namespaces, ElementTree will serialize them as `ns0:p` instead of `w:p`, which can corrupt the document:
```python
ET.register_namespace('w', 'http://schemas.openxmlformats.org/wordprocessingml/2006/main')
ET.register_namespace('r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')
```

### Element positions shift after insertions/removals
After adding or removing paragraphs, re-read `list(body)` before using position-based indexing. Stale position references will target the wrong content.

### Preserve xml:space="preserve"
When setting text content, always add:
```python
new_t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
```
Without this, Word may collapse whitespace.

### Use temp files for safe writing
Write to a `.tmp` file, then `os.replace()` to the final path. This prevents corruption if the process crashes mid-write.

### Back up before major edits
Always create a `.backup` copy of the DOCX before operations that modify multiple paragraphs or reorder content.

---

## Editorial Tips

### The myth→definition→foundation→framework→application→caution flow
This is the strongest structural pattern for any chapter that introduces a new concept:
1. Kill the popular misconception
2. Define the real thing
3. Explain what makes it reliable (foundation)
4. Give the framework for using it
5. Show application in context
6. End with boundaries and discipline

### Front-load authority, back-load nuance
If you introduce disputed material too early, it slows authority. Open with clean, strong, defensible principles. Save the "here's where it gets complicated" for after the reader trusts your judgment.

### Triangulation as a structural principle
"The difference between guessing and reading is triangulation." This isn't just a behavioral rule — it's also a writing rule. Make three strong points before claiming a conclusion.

### Repetition as doctrine
Important concepts (Three-Signal Rule, Five Cs, triangulation) should appear:
- First: as a memorable principle
- Later: as an operational section with full detail
- Throughout: as reinforcing references
This isn't redundancy. It's training.

### Conceptual vs. applied split
Within any teaching chapter, separate the conceptual argument from the practitioner manual:
- Part 1: Why this matters (concepts, principles, psychology)
- Part 2: How to do it (field application, step-by-step, context-specific)

### The "doctrine block" technique
When presenting a major framework, give it visual and tonal authority:
```
The Five Cs
Context. Clusters. Congruence. Consistency. Culture.

If you are not observing through all five, you are not reading behavior.
You are narrating noise.
```
Short. Declarative. Then the elaboration follows.

---

## Design Psychology Tips

### The brain processes color 60,000x faster than text
Every color choice is a pre-verbal message. The cool→warm arc primes identity shift before the reader consciously processes it.

### First impressions form in 250 milliseconds
This applies to pages as much as people. The chapter opener must win in a quarter second.

### Processing fluency = trust
Readable fonts increase trust by up to 40%. This is why Garamond on cream at 11pt with generous leading isn't just "nice" — it's a credibility mechanism.

### "If everything stands out, nothing stands out"
Maximum ONE spotlight per chapter. Maximum ONE pull quote per spread. Pattern interrupts every 8-12 pages (not every page). Restraint is the design.

### Recto pages carry more weight
Right-hand pages get more attention. Put key reads, spotlight boxes, and "What You Just Did" moments on recto pages.

### The page turn is a suspense mechanism
End recto pages with unresolved thoughts. The reveal comes at the top of the next verso. This is the reading equivalent of the open loop.

---

## Performance / Mentalist Tips from the Content

### The walk to the stage IS the read
When a volunteer walks from their seat, you have 5-7 seconds of unguarded movement. Gait, posture, eye direction, breathing, hand position — all broadcasting before they know they're being read.

### Breathing rate is the fastest baseline indicator visible from stage distance
High and shallow = arousal (excitement or nerves). Low and slow = settled. Neither is better. Both are information.

### T1 reads land hardest
Physical evidence reads (shoe wear, calluses, belt notch) land hard with audiences because they're specific, verifiable, and unexplainable. Lead with T1 whenever available.

### Strolling tactics
Move on one signal. Verify on two. Adjust on three. The strolling mentalist who waits for a perfect three-signal cluster loses the window entirely.

### "Behavioral profiling" vs. "lie detection" as professional identity
If you position as someone who detects lies, you've made an undeliverable promise. If you position as someone who reads behavioral patterns with unusual precision, you can demonstrate that every night.

---

## Process Tips

### The DOCX is the master, everything else is generated
Edit the DOCX. Run the build script. The HTML is output, not source. Never edit the HTML directly — your changes will be overwritten.

### Images live in two places
Figures are embedded in the DOCX (so they're visible in Word/Docs) AND referenced in the `FIGURES` dict in `build-book.py` (so they render in the HTML). Both must be updated when adding a figure. The text extraction step does not carry images — only the build script's `FIGURES` map handles that.

### Never edit downstream files directly
The `manuscript-extracted.txt` and `Architecture-of-Wonder-DESIGNED.html` are generated output. Edits to these files will be lost on the next extract/build cycle. Always edit upstream: DOCX for prose, `build-book.py` for design elements and figures.

### Chapter numbering: parser vs. TOC
The `parse_manuscript()` function assigns chapter numbers sequentially as it encounters `CHAPTER` headings in the text. This can differ from the TOC numbering in the designed HTML (which accounts for parts, introduction, etc.). When referencing chapters in config dicts (FIGURES, HOOK_LINES, etc.), always use the parser's numbering. Run the parser with debug output if unsure.

### When adding content, find position markers first
Before inserting into the DOCX, search for known text (chapter titles, part headers) to find the exact position. Don't rely on remembered positions — they shift with every edit.

### Commit messages must be descriptive for binary files
DOCX diffs are meaningless in git. The commit message is the only record of what changed. Write it like a change log.

### Keep the Meta Reveal in sync
Every design change needs a corresponding Meta Reveal update. Use `docs/08-meta-reveal-checklist.md` as your reference.

### Chapter renumbering cascades
When removing or adding a chapter, you must update: all chapter numbers in the DOCX, the TOC entries, the hook lines/key reads in build-book.py, and the chapter map in docs/07-chapter-map.md.

### Visual consistency: same-level items must look the same
If three things are the same semantic level (e.g., sub-methods within a chapter section), they must render identically. Mixing sh-label (centered, small) and sh-standard (left-aligned, underlined) for same-level headers is confusing. Rule: use a single visual style for all sibling headers. Avoid word-count-based style differentiation when items belong to the same hierarchy tier.

### Numbered step headers need distinct treatment
Items like "01 — SHOES", "02 — HANDS" are subordinate steps, not peer section headers. They must look visually smaller/different from the parent section header. The `process_paragraph()` step-header detector handles this — detects `\d{1,2} — [A-Z]+` pattern and renders as a compact step-header rather than a full section header.

### Large dark framework cards break page flow
Full-width dark-background cards (like the original Five Cs SVG + table) feel overwhelming when embedded in cream-background chapter body. Prefer compact inline treatments (bordered grid, chain pills) that sit naturally within the text. Reserve full dark-background treatment for pattern interrupts and chapter openers.

### The Edit tool may corrupt Python string delimiters with curly quotes
When using the Edit tool to replace multi-line Python triple-quoted strings, the `'''` delimiters can get replaced with curly quotes (`\u2018\u2019\u2019`), breaking the syntax. If you see `SyntaxError: invalid character` after an edit, check that all triple-quote delimiters in the affected string are straight ASCII quotes. Fix with a binary `replace()` if needed.

### Build always = build-book.py + build-gated.py
Always run both scripts together. build-gated.py reads from Architecture-of-Wonder-DESIGNED.html, so any change to build-book.py requires rebuilding both.
