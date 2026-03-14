# Editing Session Log

Tracks every edit made to the manuscript, the reasoning behind it, and patterns that emerge over time.
This file is cumulative — each session appends to it.

---

## Format

```
### [DATE] — [Session Summary]
**Change:** What was changed and where (file + section)
**Why:** The reason or instruction behind the change
**Pattern/Lesson:** What this reveals about Chris's preferences or the book's voice
```

---

## Sessions

### 2026-03-14 — Workflow Setup
**Change:** No manuscript edits. Established editing infrastructure.
**Why:** Plan implementation — created `docs/10-editing-session-log.md` and `export-pdf.py`.
**Pattern/Lesson:** Editing surface is `manuscript-extracted.txt`. All edits flow through the Edit tool → `python build-book.py` → `Architecture-of-Wonder-DESIGNED.html`. DOCX is archive only.

### 2026-03-14 — Six-Category Radar Cards + Five Cs Graphic Move
**Change:** Added `gen_radar_category()` to `build-book.py`. All `NN — Category Name` + signal-bullet paragraphs now render as styled cards: numbered header badge, signal chips with T-tier badges, and insight text separated by a rule. Applied to both Six-Category Radar (Ch. 7) and Pattern Read sets. Moved Five Cs SVG graphic to appear inline directly after the trigger sentence "Context. Clusters. Congruence. Consistency. Culture." rather than at chapter start.
**Why:** User wanted better organization for radar sections (dense paragraph blobs were hard to scan) and wanted the graphic closer to where it's introduced.
**Pattern/Lesson:** Chris wants structured visual hierarchy for any numbered-list content. Cards > paragraphs for signal catalogs.
