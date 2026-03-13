# The Architecture of Wonder — Designer Implementation Guide

> This document translates the design specification into page-by-page production instructions. Hand this to your book designer alongside `design-specification.md` and the SVG mockups in `/graphics/`.

---

## 1. Trim Size & Grid

### Trim Size
- **6" × 9"** (152mm × 229mm) — standard US trade non-fiction
- Alternative: **234mm × 156mm** (Royal format, UK trade)

### Page Grid

```
┌─────────────────────────────────────────────┐
│  Top margin: 20mm                           │
│  ┌──────┬───────────────────────┬─────────┐ │
│  │Margin│                       │ Margin  │ │
│  │Icons │    BODY TEXT BLOCK    │  Notes  │ │
│  │Zone  │                       │  Zone   │ │
│  │12mm  │    100mm wide         │  25mm   │ │
│  │      │    50-75 chars/line   │         │ │
│  │      │                       │         │ │
│  │      │                       │         │ │
│  │      │                       │         │ │
│  └──────┴───────────────────────┴─────────┘ │
│  Bottom margin: 18mm                        │
│  Inner (gutter) margin: 18mm                │
│  Outer margin: 25mm (accommodates marginalia)│
└─────────────────────────────────────────────┘
```

### Margin Zones
- **Inner margin (gutter)**: 18mm — generous for perfect binding
- **Outer margin**: 25mm minimum — accommodates marginalia text frame
- **Top margin**: 20mm — space for running headers
- **Bottom margin**: 18mm — space for page numbers and footer
- **Icon zone**: 12mm strip between gutter and body text (verso pages) or between body text and outer margin (recto pages) — icons placed here at reduced opacity

### Baseline Grid
- Set to match body text leading (e.g., if body text is 11pt on 15pt leading, baseline grid = 15pt)
- All text elements should align to the baseline grid
- Marginalia, pull quotes, and captions can use half-grid increments

---

## 2. Page-by-Page Templates

### TEMPLATE A: Chapter Opener (Dark Page)

**Always recto (right-hand page). Always starts a new page.**

```
┌─────────────────────────────────────────┐
│                                         │
│  ████████████████████████████████████   │  ← Full dark gradient
│  ████████████████████████████████████   │    (#080F1A → #0D1E30)
│  ████████████████████████████████████   │
│  ████████████████████████████████████   │
│            PART TWO                     │  ← Dim gray, 11pt sans, letterspaced
│            ─── gold line ───            │
│                                         │
│               06                        │  ← Gold, 72pt sans, light weight
│                                         │
│      BEHAVIORAL PROFILING               │  ← White, 18pt sans, bold, all-caps
│         IN REAL TIME                    │    Letter-spacing: 5px
│            ─── gold line ───            │
│                                         │
│    "Every person who walks toward       │  ← Gray-blue italic, 13pt serif
│     you is already broadcasting."       │    THE HOOK LINE (Serial Position)
│                                         │
│        [T1] [T2] [T3] [T4]            │  ← Tier badge examples
│      SIGNAL CONFIDENCE TIERS            │
│                                         │
│     (BP)  (CR)  (VS)  (AM)            │  ← Margin icon demonstration
│   MARGIN OBSERVATION ICONS              │
│                                         │
│  THE ARCHITECTURE OF WONDER | DECODE    │  ← Footer
│  ████████████████████████████████████   │
└─────────────────────────────────────────┘
```

**SVG reference:** `graphics/chapter-opener-mockup.svg`

### TEMPLATE B: Body Page (Cream Background)

**Standard content page. Warm cream (#F5F0E8) background.**

```
┌─────────────────────────────────────────────┐
│  CHAPTER 6 — BEHAVIORAL PROFILING    47     │ ← Running header + page number
│  ────────────────────────────────────────    │
│                                             │
│  [BP]  The first thing to understand about  │ ← Margin icon in left zone
│  icon  behavioral reading is that you are   │   Body text: Garamond 11pt
│        not looking for single signals.      │
│        You are looking for patterns.        │
│                                             │
│        Consider Observation #02: Shoe       │
│        sole wear direction [T1]. This is    │ ← Inline tier badge
│        a concrete, visible, low-inference   │
│        observation.                         │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │  ████ KEY PRINCIPLE ████████████████│    │ ← Spotlight box (Von Restorff)
│  │  ████                          █████│    │   Dark bg, gold left border
│  │  ████ "One signal is noise.    █████│    │   White reversed text
│  │  ████  Three co-occurring      █████│    │   ONE per chapter maximum
│  │  ████  behaviors form          █████│    │
│  │  ████  a pattern."             █████│    │
│  │  ████████████████████████████████████│    │
│  └─────────────────────────────────────┘    │
│                                             │
│        Now compare this with                │   Marginalia zone (outer
│        Observation #08: Eye contact  [T2]   │   margin) available for
│        willingness. This is a useful        │   sans-serif war stories
│        contextual signal...                 │   in gold/blue at 9pt
│                                             │
│                 · · ·                       │ ← Section break (gold dots)
│                                             │
│        THE FIVE Cs CHAIN                    │ ← Section header, sans bold
│        ══ gold underline ══                 │
│                                             │
│  ─────────── gold line ───────────          │
│  The read is never one signal.              │ ← Key Read (chapter closer)
│  The read is the chain.                     │   Gold italic, generous space
│  ─────────── gold line ───────────          │
│                                             │
│  THE ARCHITECTURE OF WONDER | DECODE        │ ← Footer
└─────────────────────────────────────────────┘
```

**SVG reference:** `graphics/body-page-mockup.svg`

### TEMPLATE C: Pattern Interrupt Page (Full-Bleed Dark)

**Appears every 8–12 pages. Full dark background. Single striking element.**

```
┌─────────────────────────────────────────┐
│  ████████████████████████████████████   │
│  ████████████████████████████████████   │
│  ████████████████████████████████████   │
│  ████████████████████████████████████   │
│  ████████████████████████████████████   │
│           ═══ gold glow ═══             │
│                                         │
│              250                        │  ← Gold, 96pt, light weight
│          MILLISECONDS                   │    with glow filter
│                                         │
│           ═══ gold glow ═══             │
│                                         │
│     The time it takes your brain        │  ← Gray-blue italic, 12pt
│     to form a first impression          │
│     of a stranger.                      │
│                                         │
│   Willis & Todorov, 2006               │  ← Dim gray, 10pt
│                                         │
│   You formed yours of this page         │  ← White italic, 11pt
│   in less time than that.               │    "What You Just Did" moment
│   What did you notice first —           │
│   the number, or the word?              │  ← Gold, 10pt
│   That is salience at work.             │
│                                         │
│  ████████████████████████████████████   │
│  THE ARCHITECTURE OF WONDER | DECODE    │
└─────────────────────────────────────────┘
```

**SVG reference:** `graphics/pattern-interrupt-page.svg`

### TEMPLATE D: Part Opener (Full Dark Spread)

**Two-page spread. Always starts on a verso page so the spread is fully visible.**

```
VERSO (LEFT)                              RECTO (RIGHT)
┌───────────────────────┐ ┌───────────────────────┐
│  ██████████████████   │ │   ██████████████████   │
│  ██████████████████   │ │   ██████████████████   │
│  ██████████████████   │ │   ██████████████████   │
│  ██████████████████   │ │   ██████████████████   │
│  ██████████████████   │ │   ██████████████████   │
│                       │ │                        │
│                       │ │        PART TWO        │ ← Dim gray, 12pt
│                       │ │                        │
│                       │ │   READING THE ROOM     │ ← Gold, 28pt, letterspaced
│                       │ │                        │
│                       │ │  ─── gold line ───     │
│                       │ │                        │
│                       │ │  "Observation is not    │ ← Gray-blue italic
│                       │ │   a passive act."       │
│                       │ │                        │
│                       │ │  Chapters 6–10b        │ ← Dim gray, chapter list
│  ██████████████████   │ │   ██████████████████   │
│  ██████████████████   │ │   ██████████████████   │
└───────────────────────┘ └───────────────────────┘
```

### TEMPLATE E: Ten-Second Scan Exercise

**Immediately follows each Part Opener. Two pages.**

```
PAGE 1 (RECTO):                          PAGE 2 (VERSO):
┌───────────────────────┐                ┌───────────────────────┐
│                       │                │                       │
│                       │                │  WHAT DID YOU SEE?    │ ← Gold, sans
│                       │                │                       │
│   ┌───────────────┐   │                │  1. SHOES — lateral   │ ← Numbered
│   │               │   │                │     wear on right     │   annotations
│   │  PHOTOGRAPH   │   │                │     indicates...      │   with tier
│   │  (full page,  │   │                │                       │   badges
│   │   no labels)  │   │                │  2. HANDS — calluses  │
│   │               │   │                │     on index finger   │
│   │               │   │                │     suggest...    [T1]│
│   └───────────────┘   │                │                       │
│                       │                │  3. POSTURE — weight  │
│   What do you notice? │ ← Gold, 14pt  │     shifted left,     │
│   Take ten seconds.   │   italic      │     arms crossed...   │
│                       │                │              [T2]     │
│                       │                │                       │
│                       │                │  Apply the Five Cs    │ ← Reminder
│                       │                │  before concluding.   │
└───────────────────────┘                └───────────────────────┘
```

**SVG reference:** `graphics/ten-second-scan.svg`

### TEMPLATE F: Marginalia Spread (Greene Model)

**Body page with active marginalia — dual reading path.**

```
┌──────────────────────────────────────────────────┐
│  CHAPTER 14 — STORIES FROM THE FIELD        127  │
│  ─────────────────────────────────────────────    │
│                                                  │
│        The corporate boardroom is a stage.        │
│        Every seat placement is a choice.          │   I once walked into
│        The person who arrives first and            │   a CEO's office and
│        chooses the seat facing the door             │   counted seven
│        has told you something before                │   dominance signals
│        they have said a word.                       │   before he spoke.
│                                                     │   The chair, the desk
│        This is Observation #60:                     │   width, the family
│        Chair choice in a room [T2].                │   photos facing OUT.
│        Security, status, or social                  │   — Field note, 2019
│        strategy. Run it through the                 │
│        Five Cs before concluding.                   │
│                                                     │
│        But the strongest signal in                  │   The best readers
│        any room is the one no one                   │   I've trained all
│        expects you to notice.                       │   say the same thing:
│                                                     │   "I stopped trying
│                                                     │   to be impressive
│                 · · ·                               │   and started trying
│                                                     │   to be observant."
│  MAIN TEXT (Garamond, 11pt, black)     MARGINALIA  │
│                                    (Helvetica Neue  │
│                                     Light, 9pt,     │
│                                     gold)           │
│                                                     │
│  THE ARCHITECTURE OF WONDER | DECODE BEHAVIOR       │
└──────────────────────────────────────────────────────┘
```

### TEMPLATE G: "What You Just Did" Moment

**Inline within body text. Distinct visual treatment.**

```
│                                                  │
│     ...and that is why clusters matter more       │
│     than individual signals.                      │
│                                                  │
│     ┃  You have been reading for approximately   │ ← Thin gold vertical
│     ┃  four minutes. Which hand is holding       │   rule on left margin
│     ┃  this book? That is Observation #01.       │   Italic serif, 11pt
│     ┃  You just demonstrated handedness          │   Indented from body
│     ┃  without thinking about it.                │
│                                                  │
│     The point is not that handedness              │
│     matters. The point is that...                 │
│                                                  │
```

---

## 3. Color Application Map

### By Chapter

| Chapter | Part | Accent Color | Background | Edge Tint |
|---------|------|-------------|------------|-----------|
| Intro | — | Gold | Cream | — |
| Ch 1–5 | Part 1 | Steel Blue primary, Gold secondary | Cream | Cool blue-gray |
| Ch 6–10b | Part 2 | Steel Blue primary, Gold secondary | Cream | Steel blue |
| Field Notes | Part 3 | Blue-Gold blend | Cream | Neutral |
| Ch 11–15 | Part 4 | Gold primary, Steel Blue secondary | Cream | Warm gold |
| NPM | Part 5 | Gold primary, Red for Stage 5 | Cream | Amber |
| Ch 16–22 | Part 6 | Gold primary, Deep Purple secondary | Cream | Deep gold |
| Ch 23–27 | Part 7 | Dark Gold/Amber primary | Cream | Dark warm |
| Meta Reveal | Part 6/7 | Full Gold | Dark spread | — |

### Color Rules
1. **Gold** is always the signature accent — never absent from any page
2. **Steel Blue** appears most in Parts 1–2, fades through Parts 3–4, nearly absent by Part 7
3. **Deep Purple** appears most in social/behavioral signal chapters (Part 2 and Part 6)
4. **Red/Rust** appears ONLY for warnings, T4 badges, and Stage 5 of the NPM (failure point)
5. **The shift is gradual** — no sudden color changes between adjacent chapters

---

## 4. Marginalia Placement Rules

### When to Use Marginalia
- Chapter contains a practitioner anecdote or field story
- A cross-reference to another chapter/observation would be helpful
- The author wants to share a "in practice, here's what actually happens" note
- A contrarian perspective adds depth

### When NOT to Use Marginalia
- Dense technical or framework content (marginalia would compete for attention)
- Chapters shorter than 6 pages (not enough space to establish the pattern)
- When the margin note would be longer than 3 sentences (use a sidebar instead)

### Placement
- **Align vertically** with the paragraph the note references
- **Outer margin only** (never gutter side)
- **Sans-serif light weight, 9pt**
- **Gold** for field stories and practitioner notes
- **Steel Blue** for cross-references and science notes
- **Set with 12pt leading** for readability at small size
- **Maximum 6 margin notes per chapter** — restraint is critical

---

## 5. Icon and Badge Specifications

### Margin Icons (BP, CR, VS, AM)

**Size:** 16px × 16px within a 22px diameter circle
**Stroke weight:** 0.6–0.8px
**Opacity:** 60%
**Placement:** Centered in the icon zone, vertically aligned with the relevant paragraph's first line

| Icon | Symbol | Color |
|------|--------|-------|
| BP | Eye (almond shape + circle pupil) | Gold `#C9A84C` |
| CR | Profile silhouette (head + shoulders) | Steel Blue `#1A8FA8` |
| VS | Waveform (zigzag audio wave) | Deep Purple `#6B52A0` |
| AM | Directional arrow (→ with arrowhead) | Red/Rust `#A83030` |

### Tier Badges (T1–T4)

**Size:** 24px × 13px, rounded corners (6.5px radius)
**Font:** Sans-serif bold, 7pt, centered
**Placement:** Inline, immediately after the observation name

| Badge | Fill | Text Color | Border |
|-------|------|-----------|--------|
| T1 | Solid Gold `#C9A84C` | Dark Navy `#080F1A` | None |
| T2 | Solid Steel Blue `#1A8FA8` | White `#FFFFFF` | None |
| T3 | None (transparent) | Gray-Blue `#8A9AB5` | 1px solid `#8A9AB5` |
| T4 | None (transparent) | Dim Gray `#3A4A5C` | 1px dashed `#3A4A5C` |

---

## 6. Pull Quote Specifications

### Style
- **Font:** Sans-serif (Montserrat/Brandon Grotesque), Semibold, 14–16pt
- **Color:** Gold `#C9A84C`
- **Alignment:** Centered or left-aligned, depending on page composition
- **Surrounding whitespace:** Minimum 24pt above and below
- **Optional:** Thin gold horizontal rules above and below (0.5pt, 40% opacity)
- **Optional:** Large opening quotation mark in gold at 48pt, positioned as a decorative element

### Frequency
- **Maximum ONE per spread** (two-page view)
- **Preferred placement:** Recto pages
- **Content source:** Extracted from the body text on the same or facing page

---

## 7. Drop Cap Specifications

### Style
- **Font:** Sans-serif (Montserrat/Brandon Grotesque), Regular or Light weight
- **Size:** 3 lines tall (spans 3 lines of body text)
- **Color:** Gold `#C9A84C`
- **Placement:** First letter of the first paragraph in each chapter (not section)
- **Wrap:** Body text wraps around the drop cap with 4pt clearance

---

## 8. Running Headers & Footers

### Running Header (Top of Page)
- **Verso (left) pages:** Book title — `THE ARCHITECTURE OF WONDER`
- **Recto (right) pages:** Chapter number and title — `CHAPTER 6 — BEHAVIORAL PROFILING IN REAL TIME`
- **Font:** Sans-serif, 8pt, letter-spacing 2px
- **Color:** Gray-Blue `#8A9AB5`
- **Separator:** 0.5pt rule below, color `#D8D0C4`
- **Not shown on:** Chapter openers, Part openers, pattern interrupt pages, blank pages

### Page Numbers
- **Position:** Top outer corner (recto: right; verso: left)
- **Font:** Sans-serif, 9pt
- **Color:** Gray-Blue `#8A9AB5`
- **Style:** Lining figures

### Footer
- **Content:** `THE ARCHITECTURE OF WONDER  |  DECODE BEHAVIOR`
- **Font:** Sans-serif, 7pt, letter-spacing 2px
- **Color:** Dim Gray `#3A4A5C` (body pages) or same (dark pages)
- **Shown on:** Every page except blanks

---

## 9. Spotlight Box (Von Restorff Element)

### Style
- **Background:** Dark gradient (same as chapter opener: `#080F1A` → `#0D1E30`)
- **Left border:** 4px solid Gold `#C9A84C`
- **Corner radius:** 4px
- **Padding:** 20px all sides
- **Label:** `KEY PRINCIPLE` in Gold, sans-serif, 9pt, letterspaced
- **Content text:** White, serif italic, 12pt
- **Width:** Full text block width (stretches across body text column)

### Frequency
- **Exactly ONE per chapter** — this is the Von Restorff element
- If there are two equally important concepts, choose the one that best represents the chapter's core insight

---

## 10. Key Read (Chapter Closer)

### Style
- **Top rule:** Gold, 0.5pt, 40% opacity, centered, 200px wide
- **Text:** Gold, serif italic, 11pt, 600 weight, centered
- **Bottom rule:** Gold, 0.5pt, 40% opacity, centered, 200px wide
- **Whitespace:** Minimum 30pt above top rule, 20pt below bottom rule
- **Placement:** Final element on the last page of each chapter, preferably on a recto page

### Content
- One sentence that captures the chapter's core insight
- Written to be memorable in isolation (no context needed)
- This is the serial position recency anchor — it must be strong

---

## 11. French Flap Content

### Inside Front Flap
```
THE FIVE Cs — BEHAVIORAL READING CHAIN

1. CONTEXT — What environment?
2. CLUSTERS — Multiple signals?
3. CONGRUENCE — Body = words?
4. CONSISTENCY — Their baseline?
5. CULTURE — Background norms?

Apply as a chain, not a checklist.
```

### Inside Back Flap
```
OBSERVATION ICONS

[Eye]  BP — Baseline / Physical
[Head] CR — Character Reading
[Wave] VS — Verbal / Social
[Arrow] AM — Action / Motivation

TIER CONFIDENCE

[Gold]  T1 — Concrete, visible
[Blue]  T2 — Contextual, cluster-dependent
[Gray]  T3 — Higher-inference, use caution
[Dash]  T4 — Weak/disputed (appendix only)
```

---

## 12. Printing & Production Notes

### Paper
- **Interior:** Munken Cream or equivalent — uncoated, 80–90gsm, warm ivory tone
- **Why cream:** Reduces eye strain for extended reading; signals craft over mass-market

### Cover
1. **Substrate:** 350gsm board
2. **Lamination:** Soft-touch matte over full cover
3. **Spot UV:** High-gloss clear coating on:
   - Title text (front cover)
   - Author name (front cover)
   - Hidden message text (back cover) — `"You're already reading people. You just proved it."`
4. **Embossing:** Blind deboss on title text (creates raised effect on reverse)
5. **French flaps:** 75mm fold-in on front and back
6. **Spine:** Title and author in gold foil or metallic ink

### Edge Printing
- 7-shade progression from cool blue-gray (Part 1) to dark warm gold (Part 7)
- Applied to fore-edge only (top and bottom edges remain natural)
- Creates a visible "progress bar" when book is viewed from the side

### Binding
- **Perfect binding** with PUR adhesive (stronger than standard EVA for lay-flat)
- **Consideration:** If budget allows, Swiss binding or exposed-spine binding allows the book to lie flat more naturally — important for a reference/tool book

---

## 13. File Delivery Checklist for Designer

### From Author/Editor
- [ ] Final manuscript in Word/Google Docs with chapter breaks clearly marked
- [ ] Observation list (80 signals) — see `Expanded-Observation-List.md`
- [ ] Five Cs framework text — see `design-specification.md`
- [ ] Neural Performance Model stages — see `graphics/neural-performance-model.svg`
- [ ] Marginalia text for each chapter (field stories, cross-references)
- [ ] "What You Just Did" moment text for each chapter
- [ ] Key Read sentences for each chapter
- [ ] Hook lines for each chapter opener
- [ ] Epigraphs for each chapter opener
- [ ] Meta Reveal text (full section)
- [ ] Ten-Second Scan photograph selections (7 images)
- [ ] Ten-Second Scan annotation text (7 sets)
- [ ] Cover copy (front, back, spine, French flap text)
- [ ] Back cover hidden message text for spot UV

### SVG References (in `/graphics/`)
- `chapter-opener-mockup.svg` — Chapter opener template
- `body-page-mockup.svg` — Body page template
- `pattern-interrupt-page.svg` — Pattern interrupt template
- `spot-uv-cover-concept.svg` — Cover design concept
- `marginalia-spread-mockup.svg` — Marginalia layout
- `recto-verso-spread.svg` — Two-page spread composition
- `five-cs-behavioral-reading.svg` — Five Cs framework
- `neural-performance-model.svg` — NPM seven stages
- `observation-table-styled.svg` — Observation list display
- `ten-second-scan.svg` — Ten-Second Scan exercise
- `behavioral-training-framework.svg` — Training framework
- `bte-signal-clusters.svg` — Signal clustering
- `cortisol-window.svg` — Stress response
- `disc-comparison-matrix.svg` — DISC types
- `dopamine-anticipation.svg` — Anticipation neuroscience
- `field-notes-process.svg` — Field notes methodology
- `five-forces-salience.svg` — Salience framework
- `stat-callouts.svg` — Statistical highlights
