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

### 2026-03-15 — Chapter Reorder: Eyes/Face Moved to Ch9

**Change:** Moved the Eyes/Face chapter (was Ch11) to Ch9, immediately after DISC (Ch8). New order: Ch9 = Eyes/Face, Ch10 = Micro-Expression Matrix, Ch11 = Cold Reading. HOOK_LINES, KEY_READS, and FIGURES in `build-book.py` updated to match.
**Why:** Chris determined face/eye-reading is foundational and logically follows DISC before micro-expression and cold reading application.
**Pattern/Lesson:** Chapter order request required two passes — first script swapped wrong pair. Always verify chapter order by reading the resulting manuscript headers, not just trusting the script ran cleanly.

---

### 2026-03-15 — Duchenne Marker → Duchenne Smile; Performer's Note → Chris Michael's Take

**Change:** Renamed "The Duchenne Marker" to "The Duchenne Smile" in manuscript and build script. Renamed `gen_performer_note()` label from "Performer's Note" to "Chris Michael's Take."
**Why:** Chris's preference for both. "Duchenne Smile" is the standard anatomical term. "Chris Michael's Take" is more personal and author-specific.
**Pattern/Lesson:** When Chris gives an exact rename, apply it everywhere — manuscript text, build script constants, card generators.

---

### 2026-03-15 — Lip Compression Section Added to Ch9

**Change:** Added full Lip Compression section (Chris's exact words) to Ch9 (Eyes/Face) before "The Eyes in the Larger Frame." Only formatting applied: paragraph breaks and `·` bullet separation.
**Why:** Chris provided the text and said "ADD IT AS IS, but do format it."
**Pattern/Lesson:** Never rewrite directly supplied content. Format it only. First attempt rewrote it and was rejected.

---

### 2026-03-15 — Fruit to Fang: Reorder, New Subtitle, REFLEX Context, Em Dashes Removed

**Change:** Restructured the Fruit to Fang section: title → flow chart trigger → all prose. Updated subtitle to "Propless Method: Using the Eyes to Discern a Vowel in a Word." E branch updated to "Eagle / Elephant." Two em dashes replaced with commas. REFLEX context added to The Setup sub-section.
**Why:** Chris wanted the chart first, then the explanation. New subtitle reflects that any vowel in any word can be obtained. REFLEX is Chris's own Any Name Divination that uses this method.
**Pattern/Lesson:** Em dashes read as AI-generated to Chris. Replace with commas or restructure. This is a firm style preference.

---

### 2026-03-15 — T4 Signal Cards Reinstated Inline (Ch7)

**Change:** Added T4 signal cards (SIGNAL 1–4: Micro-Leakage, Proximity Inference, Timing Tells, Vocal Micro-Patterns) back into Ch7 as inline rendered cards using `gen_t4_signal_card()`, after the explanatory disclaimer paragraph.
**Why:** Chris wanted the cards visually present, not omitted. The disclaimer paragraph sets proper epistemic context before the cards appear.

---

### 2026-03-15 — Post-Pattern-Interrupt Spacing Fix

**Change:** Added CSS rule `.chapter-body .pattern-interrupt+p{margin-top:2.4em}` to build-book.py.
**Why:** Text following pattern interrupt sections had insufficient top margin — screenshotted and flagged by Chris.
**Pattern/Lesson:** Pattern interrupts are full-bleed dark blocks. The paragraph following them needs extra breathing room or it reads as a caption rather than new body text.

---

### 2026-03-15 — 40% Pattern Interrupt Moved to End of Ch9; Explicit Trigger System Added

**Change:** Added `PATTERN_INTERRUPT_40PCT` trigger string to end of Ch9 in manuscript. Added explicit trigger handler in `build_chapter_body()` so named triggers fire specific pattern interrupts at exact locations.
**Why:** Chris wanted the "40% INCREASE IN TRUST / Processing Fluency" card at the end of Ch9 (Eyes/Face) specifically.
**Pattern/Lesson:** Auto-interval placement (every 45 paragraphs) is not precise enough when a specific card belongs at a specific narrative moment. Named trigger strings in the manuscript give exact placement control.

---

### 2026-03-15 — Microexpressions in Mentalism Section Added to Ch10

**Change:** Inserted full "Microexpressions in Mentalism" section in Ch10 (Micro-Expression Matrix) after "Reading in Clusters, Not Snapshots." Covers: emotional families (anger/fear/surprise/disgust/contempt/sadness/joy), four expression variation types (full/partial/subtle/masked), three watch zones, five performance applications (readings, anagrams, forces, dual reality, Q&A), training method, and the performer's rule.
**Why:** Chris provided the full text. Largest single content addition this session.

---

### 2026-03-15 — Seven Expressions Image Injection Fixed

**Change:** Corrected FIGURES dict key from `'CHAPTER 10:7 Universal Microexpressions'` to `'CHAPTER 10:The Seven Expressions'` to match the actual section header in the manuscript.
**Why:** Key mismatch meant the image was not injecting. The section header in the manuscript is "The Seven Expressions," not the more descriptive label used in the dict key.
**Pattern/Lesson:** FIGURES keys must match the manuscript section header text exactly, character for character. Always verify by checking the actual manuscript after any chapter reorder.

---

### 2026-03-17 — Cold Reading Toolkit Redesign + Visual Overhaul

**Change:** Complete redesign of Cold Reading Toolkit chapter rendering. Replaced verbose entry cards with compact 3-column scan tables (Cue | Line + context symbols | DISC badge). Added `gen_crt_table()`, `gen_feedback_signals_ref()`, `_ctx_to_symbols()`. Added section icons via `_SECTION_ICONS` dict. Buffering system accumulates `CRT:` rows per section, flushes as single `<table>` at section end. Toolkit color scheme changed from gold to cool blue (#4A8DB5). Recovery card headers redesigned with dark navy gradient background + white text. Feedback chart left column widened from 118px to 150px to prevent Microexpression of Contempt overflow. Six-Area-to-Watch radar chart added to Ch7 via `gen_six_area_radar()` SVG function with dynamic height and stacked legend.
**Why:** Multiple Chris feedback: overflow bug, unreadable headers, gold color preference, "integrate this chart."
**Pattern/Lesson:** When two adjacent card systems share a color language, readers cannot distinguish them. Buffering enables proper `<thead>/<tbody>` structure for multi-row tables. SVG height must be computed dynamically to avoid clipping.

---

### 2026-03-17 — Chapter Reorder: Volunteer's Brain Moved to Ch9

**Change:** Moved Volunteer's Brain chapter from Ch13 to Ch9 (immediately after DISC Ch8). Old Ch9-12 shifted to Ch10-13. HOOK_LINES, KEY_READS, SECTION_BADGES, FIGURES all updated. Added DISC profiling bridge paragraph and 80-signal VS callout in Volunteer's Brain intro. SECTION_BADGES corrected from stale CHAPTER 9/10 keys to correct CHAPTER 13/9 keys.
**Why:** Chris determined face/eye-reading is foundational and logically follows DISC; Volunteer's Brain builds on personality typing material.
**Pattern/Lesson:** Chapter reorder requires two-phase placeholder approach to avoid swap collisions. Always verify SECTION_BADGES keys match actual chapter numbers in manuscript after any reorder.

---

### 2026-03-17 — Contact Mind Reading Chapter Expanded (Ch13)

**Change:** Replaced "The Method" (short version) with full expanded version including Trevo Sheikh refinements on performer focus, practice conditions, and natural walking contact. Added five new sections: "Focus, Not Clutter" (Satori's end-target approach, clutter vs. clarity), "Suggestibility and the Frame" (Peter Turner's observation on the guiding-line suggestion, I-type participant selection), "Setting Up the Conditions" (pendulum/ideomotor screening, emotional investment, in-contact coaching), "The Grip" (Trevo's surface-area grip principle), "Verify, Verify, Verify" (patience over certainty). "The Science Behind Contact Mind Reading" rewritten with cleaner scope statement and relational/psychological caveat. "Framing the Effect" expanded with performer's internal state note. SECTION_BADGES added for all new sections (t2/t3/bp).
**Why:** Chris provided full expanded text and said "combine this into the contact mind reading section — overwrite shared headings, add new ones."
**Pattern/Lesson:** Never rewrite directly supplied content. Format and integrate only. Multi-section replacements are safest done via a temp Python script to avoid bash heredoc quoting issues.

---

### 2026-03-15 — Neural Term Inline Descriptions Added Throughout

**Change:** Added brief parenthetical descriptions at the first body-text use of each neural structure and neurotransmitter throughout the manuscript.
**Terms added:** dopamine, salience network, limbic system, hippocampus, amygdala, visual cortex, orbitofrontal cortex, medial prefrontal regions, basal ganglia, dorsolateral prefrontal cortex, executive control network, primary somatosensory cortex, locus coeruleus, nociceptors, brainstem, thalamus, mirror neurons.
**Why:** Chris wants readers without a neuroscience background to have the anatomical context at the moment they need it, not in a glossary they have to flip to.
**Pattern/Lesson:** Already self-described terms (zygomatic major, orbicularis oculi, cortical pyramidal neurons, norepinephrine/acetylcholine functions) do not need additions. Terms already introduced with explicit "you do not need to memorize these" explanations (anterior insula, dorsal anterior cingulate) are also fine.

---

### 2026-06-12 — Release-prep: restore flattened design systems, lost figures, and add two contributed routines

**Change (DOCX, via `docx_update_contributions.py` + `docx_repair_cards.py`, backups in `backups/*20260612*`):**
- Removed two leaked editorial notes ("CHAPTER ROADMAP — SUGGESTED ADDITION" + advisory paragraphs) from Ch16 and Ch28.
- Re-added [ITALIC] markers to the three Juke Box Oracle script paragraphs (lost in the merged-DOCX swap).
- Inserted Rado Sheytanov's "Ephemeris" (complete prop-less star sign divination) and Christopher Parrish's "The Red Dwarf" (+ Group Variation + closing thoughts) into Ch25 ZODIAC DIVINATIONS, each with a narrative thank-you intro and gold byline. Added a joint thank-you paragraph to ACKNOWLEDGMENTS. Sources archived in `resources/rado-ephemeris.txt` and `resources/For-Rado-The-Red-Dwarf.pdf`.
- Rebuilt flattened card-trigger text the PDF→DOCX merge destroyed: DISC type cards (`D — DIRECT` …), DISC blend cards (`D/C Blend` …), Six-Category Radar (`SIX_AREA_RADAR` + `NN — Name` + signal lines), 10-Second Scan step headers (`01 — SHOES` …), Seven Stages cards (`01 · PRIME` …), Neural Performance Checklist (items joined with ` · `, heading VOLUNTEERS AND AUDIENCE MANAGEMENT uppercased), warning-callout trigger (stripped ⚠ prefix), PATTERN_INTERRUPT_40PCT marker. Fixed five typos (memeber, breath/breathe, th memory, theis, audiences brain).

**Change (`build-book.py`):**
- FIGURES keys re-anchored after the merge shifted chapters: Lip Compression → CH13, Seven Expressions/Duchenne → CH14; Ch19 figures renumbered 19.1–19.4 (brain-wave chart re-anchored at "Oscillations and Timing"; fractionation figure dropped — its prose no longer exists). Added four zodiac element mnemonic figures (CH25 FIRE/WATER/EARTH/AIR SIGNS; images copied from v2 Gemini JPGs into `resources/metv-images/zodiac-*-mnemonic.jpg`).
- All images now embed as base64 data URIs (`image_data_uri()`) — the deployed gated HTML is fully self-contained (image file refs were 404ing on Netlify since the v2 folder has no resources/).
- New chapter-body cleanup: strips opener-metadata bleed (hook quote, T-badges incl. mashed `T2AM` forms, icon codes, legend labels, repeated CHAPTER lines) from chapter starts AND mid-body (7A/21A/37A interludes); re-joins orphaned drop-cap letters with their sentences; suppresses in-text duplicates of config hook lines/key reads.
- Roman-numeral pillar headers (I — Confidence … V — Enjoyment) and Level-scale headers (Level 1 — Burden …) now render as section headers in Ch42.
- KEY_READS completed to all 42 chapters: CH30/32/33/34 ported from the v2 build config by title match; CH1/2/12/26/27/29/31 newly authored.
- Generic gold byline rule (`"Title" by Author`), "Chris Michael's Take" added to the Performer's-Note trigger set, numbered-card detection no longer swallows section headers.

**Why:** Chris reported formatting degraded and SVGs/images lost after new content was merged in; release-readiness pass. Rado and Christopher contributed routines that needed inclusion with thanks.
**Pattern/Lesson:** The designed-PDF→DOCX merge flattens every generator trigger (em-dashes/middots eaten, numbers split from names, infographics dumped as mashed text). After any re-merge, diff the rendered element counts (stage-card, disc-type-card, radar, checklist, key-read, figure) against the last good build — silent zeroes mean eaten triggers, not removed content.
**Open items:** Ch12 Tell Table's flat 4-column tables still render as stacked lines (needs a dedicated table design pass). "The Architecture of Obedience" chapter (pacing/leading, yes sets, certainty frames, double binds) is absent from the merged DOCX — content drop, needs Chris's decision.
