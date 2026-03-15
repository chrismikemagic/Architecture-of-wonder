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

### 2026-03-14 — Expand and reposition How to Read This Book
**Change:** Replaced the two-sentence "What This Book Is" in the Introduction with a pointer. Added a full "HOW TO READ THIS BOOK" section after the Introduction with: structural overview of all 7 parts, T1–T4 tier card definitions (using the existing tier card system), the visual element glossary (Key Reads, Pattern Interrupts, Signal Cards, Concept Boxes, Performer's Notes), two reading modes (linear vs. reference), and an epistemic note.
**Why:** Chris wanted the How to Read section to have more detail and be positioned below the Acknowledgements and Introduction, not buried inside the intro.
**Pattern/Lesson:** Front matter order: Why This Book → Acknowledgements → Introduction → How to Read This Book → Part One.

### 2026-03-14 — Seven Volunteer Types Formatting + DISC Size Fix
**Change:** Added `gen_volunteer_card()` and `gen_volunteer_matrix_entry()` to `build-book.py`. All 7 volunteer type profiles (The Supporter through The Reserved Volunteer) now render as dark profile cards with: type name badge in distinct color, description, signal chips, and Works best for / Avoid for labels. The 4 Volunteer Selection Matrix entries render as colored cells with recommendation and body. DISC SVG scaled up to 800×620 with larger fonts throughout.
**Why:** User said "this all needs better formatting" about the Seven Volunteer Types section. DISC graphic was too small to read.
**Pattern/Lesson:** Chris wants structured card treatment for any named-type catalog. Consistent visual pattern: dark card, colored left accent, chips for signal lists, labeled metadata for strategic guidance.

### 2026-03-14 — DISC Quadrant Chart
**Change:** Added `DISC_HTML` constant to `build-book.py` with inline SVG quadrant chart (2×2 grid: D=red, I=gold, C=purple, S=blue). Chart injects before the first "D — DIRECT" entry in Chapter 8. Shows axis labels (Fast/Slow, Task/People), on-stage strategy, and key signals per quadrant. Created `design-reference/graphics/disc-quadrant.svg`.
**Why:** User wanted a chart or graphic for the DISC profile section.
**Pattern/Lesson:** 2×2 quadrant works well for DISC because the axes are the model's core logic. Style matches Five Cs chart (dark navy, brand colors, Montserrat).

### 2026-03-14 — Six-Category Radar Cards + Five Cs Graphic Move
**Change:** Added `gen_radar_category()` to `build-book.py`. All `NN — Category Name` + signal-bullet paragraphs now render as styled cards: numbered header badge, signal chips with T-tier badges, and insight text separated by a rule. Applied to both Six-Category Radar (Ch. 7) and Pattern Read sets. Moved Five Cs SVG graphic to appear inline directly after the trigger sentence "Context. Clusters. Congruence. Consistency. Culture." rather than at chapter start.
**Why:** User wanted better organization for radar sections (dense paragraph blobs were hard to scan) and wanted the graphic closer to where it's introduced.
**Pattern/Lesson:** Chris wants structured visual hierarchy for any numbered-list content. Cards > paragraphs for signal catalogs.

### 2026-03-14 — Formatting Consistency Pass + New Visual Components

**Change (section header consistency):** Removed the 3-tier word-count-based section header system (sh-label / sh-standard / sh-section). All section headers ≤7 words now use `sh-standard` (left-aligned, underlined). Only 8+ word headers use `sh-section` (left-border only). The old `sh-label` (centered, small caps, flanking rules) was creating inconsistency when same-level sub-headers had different word counts.
**Why:** User showed that "The Refect and Reset" (4 words → sh-standard) and "PRODUCTIVE SILENCE" (2 words → sh-label) looked completely different despite being the same semantic level.
**Pattern/Lesson:** Chris is very sensitive to visual inconsistency between same-tier items. If siblings look different, it reads as a design error. Never let word count alone determine visual treatment for peer-level items.

**Change (numbered step headers):** Added `step-header` CSS class and detection for `NN — WORD` pattern (e.g., "01 — SHOES"). These now render as compact subordinate step items: small gold number + uppercase label, visually distinct from and smaller than section headers.
**Why:** "THE 10-SECOND SCAN" header and its sub-steps (01 — SHOES, 02 — HANDS, etc.) all had identical visual weight. The steps looked like peer headers rather than sub-items.
**Pattern/Lesson:** Hierarchical visual weight is critical. Parent headers must be visually dominant over their children. If it looks like 3 options, it will read as 3 options.

**Change (warning headers):** Added `gen_warning_header()` for "When You Have Gone Too Far" — renders as a red-left-border alert box with ⚠ icon. Added `gen_warning_callout()` for "Common Misread" and "When This Read Misses:" — compact red-tinted callout box.
**Why:** "When You Have Gone Too Far" should stand out as a significant topic shift with a cautionary tone. "Common Misread" functions as a warning, not a regular subheading.
**Pattern/Lesson:** Tonal cues in section titles should map to visual treatment. Cautionary/warning sections need a distinct visual register, not generic header styling.

**Change (Five Cs block redesigned):** Replaced the large dark-background Five Cs card (SVG chart + table + chain flow, ~900px tall) with a compact inline grid: 5 items in a horizontal grid with color-coded top borders, key question, and rule. Chain flow below. No outer dark container.
**Why:** User said "I do not like this giant card here." The original card was overwhelmingly large and broke the reading flow.
**Pattern/Lesson:** Inline reference elements should sit naturally within body text, not stop the reading experience. Dark full-width cards work for chapter openers and pattern interrupts — not for mid-chapter reference blocks.

**Change ("What You Have Felt Before" icon removed):** Removed the floating `◉` circle icon from the `felt-before` block.
**Why:** User showed the isolated dot floating above the label text looked "weird."
**Pattern/Lesson:** Decorative icons only work when they're tightly associated with their label. Vertical spacing between icon and label can make the icon look like an orphaned artifact.

**Change (manuscript text):** Changed "Yup. Unless you are using the Five C's..." to "That is unless you are using the Five C's..." and added the sentence "If you are not observing through all five, you are not reading behavior. You are instead narrating meaninglessly what you see."
**Why:** Chris wanted the text adjusted for tone and added a punchy doctrine line.
**Pattern/Lesson:** Chris's voice is direct and declarative. When softening an opener ("Yup" → "That is"), he compensates by adding a harder doctrine punch immediately after.

**Change (radar category color):** Redesigned Six-Category Radar cards from teal/blue to pastel pink (#D4879A) with dark rose background.
**Why:** Cards were too similar visually to the adjacent BTE signal cards, which also use teal/blue accents.
**Pattern/Lesson:** Adjacent card systems must be visually distinct. When two unrelated systems share the same color/style language, readers can't tell where one system ends and the other begins.
