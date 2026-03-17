# Design Bible Summary

> Condensed reference for all design decisions. Full specs in `design-reference/design-specification.md`.

---

## Color Palette

| Role | Hex | Psychological Function |
|------|-----|----------------------|
| Deep Navy (dark) | `#080F1A` | Authority, mystery — chapter openers, dark pages |
| Deep Navy (light) | `#0D1E30` | Gradient endpoint for dark backgrounds |
| Gold | `#C9A84C` | Premium, wisdom — signature accent for key terms, T1 badges, key reads |
| Steel Blue | `#1A8FA8` | Analytical clarity — sidebars, cross-references, T2 badges |
| Warm Cream | `#F5F0E8` | Trust, craft — body page background |
| Red/Rust | `#A83030` | Urgency — T4 disclaimers, warnings (use sparingly) |
| Deep Purple | `#6B52A0` | Mystery — advanced concepts |
| Body Text Gray-Blue | `#8A9AB5` | Secondary text on dark backgrounds |

### The Color Arc (Cool → Warm)

| Parts | Temperature | What the Reader Feels |
|-------|-------------|----------------------|
| Parts 1–2 | Cool steel blue | "You are learning" |
| Part 3 | Transitional blue-gold | Theory becomes practice |
| Parts 4–5 | Warm gold | "You are applying" |
| Parts 6–7 | Deep gold/amber | "You have arrived" |

The brain processes color 60,000x faster than text. The reader will not consciously notice the arc. They will feel it.

---

## Typography

| Element | Font | Size | Function |
|---------|------|------|----------|
| Body text | Garamond or Minion Pro (serif) | 10.5–11pt | Trust via processing fluency (+40%) |
| Chapter titles | Montserrat or Brandon Grotesque (sans) | 18pt, all-caps, 5px letterspacing | Geometric precision = confidence |
| Section headers | Same sans-serif | Semibold, 12–13pt | Hierarchy without font proliferation |
| Marginalia | Helvetica Neue Light (sans) | 9pt, gold or steel blue | Greene-model dual reading path |
| Pull quotes | Sans-serif | 14–16pt, gold | Visual interrupt + content teaser |
| Key reads | Serif italic | 11pt, gold, centered between gold rules | Serial position recency anchor |
| Drop caps | Sans-serif | 3 lines tall, gold | Visual entry point |

**Line length:** 50–75 characters per line (non-negotiable — affects comprehension more than font choice)
**Leading:** Minimum 135% of type size
**Number style:** Old-style figures in body, lining figures in tables

---

## Page Architecture

### Trim Size
6" x 9" (152mm x 229mm) — standard US trade non-fiction

### Grid
- Inner margin (gutter): 18mm
- Outer margin: 25mm minimum (for marginalia)
- Top margin: 20mm (running headers)
- Bottom margin: 18mm
- Icon zone: 12mm strip for BP/CR/VS/AM icons
- Body text block: 100mm wide

### Templates
- **Template A:** Chapter Opener — dark gradient, gold chapter number, white title, hook line, always recto
- **Template B:** Body Page — cream background, running header, margin icon zones, marginalia space
- **Template C:** Pattern Interrupt — full-bleed dark, single gold element, every 8-12 pages
- **Template D:** Part Opener — full dark spread, Ten-Second Scan exercise

### Recto Page Bias
Right-hand pages receive more visual attention. Key content, spotlight boxes, pull quotes, and "What You Just Did" moments go on recto pages. Key reads on recto pages force the reader to turn past them — leaving the gold sentence as the last thing in working memory.

---

## Design Elements

### Margin Icons (BP/CR/VS/AM)
| Code | Icon | Meaning |
|------|------|---------|
| BP | Eye icon | Baseline / Physical |
| CR | Profile silhouette | Character Reading |
| VS | Waveform | Verbal / Social |
| AM | Directional arrow | Action / Motivation |

Placed at 60% opacity in outer margins. By Chapter 10, readers process them unconsciously.

### Tier Badges (T1–T4)
| Tier | Style | Color |
|------|-------|-------|
| T1 | Solid pill | Gold `#C9A84C` |
| T2 | Solid pill | Steel Blue `#1A8FA8` |
| T3 | Outlined pill | Gray outline |
| T4 | Dashed pill | Dim gray, dashed border |

### Spotlight Box (Von Restorff)
ONE per chapter maximum. Dark gradient background, 4px gold left border, reversed white text. The single thing the reader will remember from the chapter.

### Pattern Interrupts
Every 8–12 pages. Options: full-bleed dark page, sidebar shift, pull quote, "What You Just Did" moment. Must be used with restraint — too frequent and they become the new pattern.

---

## Physical / Print Specs

| Element | Specification |
|---------|---------------|
| Paper | Uncoated cream/ivory, 80–90gsm matte |
| Cover | Soft-touch matte lamination + spot UV on title |
| Cover finish | Emboss/deboss title for tactile engagement |
| Hidden element | Spot UV text on back cover — visible only at angle: "You're already reading people. You just proved it." |
| Format | French flaps — inside front: Five Cs reference, inside back: icon key |
| Edge printing | 7-shade thumb index (cool blue-gray → deep warm gold) |
| Binding | Perfect bound with French flaps |
| Page count target | 280–320 pages |

---

## Design Psychology Techniques Used

1. **Von Restorff Effect** — Spotlight boxes, pattern interrupts (the different thing is remembered)
2. **Serial Position (Primacy)** — Hook lines at chapter openers
3. **Serial Position (Recency)** — Key reads at chapter closers
4. **Processing Fluency** — Readable serif, cream paper, generous whitespace = trust
5. **Behavioral Priming** — Color arc, epigraphs, recurring icons
6. **Progressive Disclosure** — Introduce signals in context, full list as earned reference
7. **Visual Anchoring** — Tier badges, margin icons build unconscious associations
8. **Recto Page Bias** — Key content on right-hand pages
9. **Page Turn as Suspense** — Open loops at recto page bottoms, reveals on next verso

---

## Design Override Rules

> **Chris's observed preferences override the original design bible where they conflict.**

| Decision | Original Spec | Actual Preference |
|----------|--------------|-------------------|
| AM icon | Directional arrow | Two person silhouettes |
| CR icon | Profile silhouette | Open book + head + snowflake |
| Five Cs block | Large dark card with SVG chart | Compact inline grid, no dark container |
| "WHAT YOU HAVE FELT BEFORE" | Floating circle icon above label | Clean label only, no icon |
| Section headers | 3 tiers (sh-label / sh-standard / sh-section) | 2 tiers only (sh-standard / sh-section) — word-count-based sh-label removed to fix inconsistency |
| Section headers (numbered steps) | Treated same as regular section headers | Distinct subordinate step-header style (01 — SHOES etc.) |
| Warning headings | No special treatment | Red/amber warning-header box (e.g. "When You Have Gone Too Far") |
| "Common Misread" | Plain paragraph | Warning callout box with red border |
| Six-Category Radar cards | Same style as BTE signal cards | Pastel pink (#D4879A) to distinguish |
| Volunteer matrix | Single color | Traffic-light scale: green → yellow → orange → red |

---

## SVG Graphics Inventory

| File | What It Shows | Where It Goes |
|------|--------------|---------------|
| behavioral-training-framework.svg | Training methodology diagram | Ch 12 |
| bte-signal-clusters.svg | Behavioral Table of Elements clusters | Ch 39 |
| chapter-opener-mockup.svg | Template A reference | Designer guide |
| body-page-mockup.svg | Template B reference | Designer guide |
| cortisol-window.svg | Cortisol curve and performance window | Ch 3 |
| disc-comparison-matrix.svg | DISC profiles comparison | Ch 8 |
| dopamine-anticipation.svg | Dopamine reward/anticipation cycle | Ch 4 |
| field-notes-process.svg | Field notes methodology | Part 3 |
| five-cs-behavioral-reading.svg | The Five Cs chain diagram | Ch 6 |
| five-forces-salience.svg | Five forces of salience model | Ch 2 |
| marginalia-spread-mockup.svg | Greene-model dual reading path | Designer guide |
| meta-reveal-spread.svg | Meta Reveal page design | Final chapter |
| neural-performance-model.svg | Seven-stage performance arc | Part 5 |
| observation-table-styled.svg | 80-signal observation table | Ch 7 |
| pattern-interrupt-page.svg | Template C reference | Designer guide |
| recto-verso-spread.svg | Spread composition guide | Designer guide |
| spot-uv-cover-concept.svg | Hidden cover element concept | Cover design |
| stat-callouts.svg | Statistical highlight treatment | Throughout |
| ten-second-scan.svg | Ten-Second Scan exercise format | Part openers |
