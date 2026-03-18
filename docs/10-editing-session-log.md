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

### 2026-03-18 — Performance Read Panel: Four HTML Visuals for Ch10

**Change:** Built four HTML panel constants in `build-book.py` for Chapter 10 (originally "The Performance Read Panel"):
- `FIVE_THINGS_PANEL_HTML` — 3+2 grid layout (5 colored cards), SVG-based, with one card per "question to ask"
- `SIGNAL_TABLE_HTML` — HTML/CSS div table "Chris Michael's Tell Table" — 3-color sections (green/yellow/red), `160px 1fr 1fr 170px` grid
- `MINI_SCENARIOS_HTML` — two-card HTML/CSS layout (green card + red card) showing behavioral read scenarios
- `CHEAT_SHEET_HTML` — 3-column HTML grid, 10 items per column with alternating row backgrounds

**Why:** Chris wanted a rich visual chapter for in-performance behavioral reading (the "Tell Table").

**Pattern/Lesson:** SVG text is unreadable at typical HTML viewport widths — text in a 900-unit viewBox renders at ~6px. Always use HTML/CSS for text-heavy tables and panels. Reserve SVG for graphical/geometric layouts only.

---

### 2026-03-18 — Ch10 Renamed and Rewritten: "Chris Michael's Tell Table"

**Change:**
- Chapter renamed from "The Performance Read Panel" → "Chris Michael's Tell Table"
- New 4-paragraph intro added distinguishing the 80-Signal System (profiling/predictions) from the Tell Table (real-time behavioral reading)
- Key distinction: profiling answers "who is this person?"; Tell Table answers "what is happening right now?"
- Phrase: "Profiling reads the person. Reading reads the moment." added as the BEHAVIORAL_READING_DEF_HTML trigger point
- `BEHAVIORAL_READING_DEF_HTML` callout box moved from Ch11 to Ch10 (it conceptually belongs at the profiling/reading boundary)

**Why:** Chris wanted the chapter intro to clearly articulate the distinction between the 80-Signal System and the Tell Table.

**Pattern/Lesson:** The "profiling vs reading" distinction is load-bearing for the whole book architecture — profiling = building predictions over time, reading = extracting direct information in the moment.

---

### 2026-03-18 — Ch11 Opener Rewritten

**Change:** Removed the "From Profiling to Reading" transition section from Ch11 (it now belongs in Ch10). Wrote fresh 2-paragraph opener focused on the face vs. eyes distinction:
- "The face is the most socially managed surface in human interaction."
- "The eyes are different. Not because people are not trying to manage them, but because the movements that carry real information happen before the social response is assembled."

**Why:** Ch11 had redundant content now handled by Ch10's new intro. The face/eyes chapter needed an opening that earned reader attention on its own terms.

---

### 2026-03-18 — BTE Signal Panel Color Fix

**Change:** Changed `.bte-signal` and `.bte-cluster-wrap` background from `rgba(13,30,48,.5)` to solid `#0d1117`. Also changed `.bte-cluster-header` to `#0a0e14`. Font sizes bumped to `.78rem`.

**Why:** The 50% opacity dark blue over the parchment page background computed to a washed-out gray-slate (~#818b8c). Chris showed a screenshot — panels looked "unattractive and hard to read."

**Pattern/Lesson:** Never use rgba opacity for backgrounds over parchment/cream page backgrounds — always use solid hex values. The interaction with the cream background creates gray rather than the intended dark.

---

### 2026-03-18 — APPENDIX A1 (T4 Signal Review) Removed

**Change:** Removed APPENDIX A1 "T4 Signal Review: The Evidence Record" in its entirety from `manuscript-extracted.txt`. Also removed the sentence "T4 signals have been removed from this table and documented in the T4 Appendix." from the signal table intro in Ch7.

**Why:** Chris said "remove these please, I dont want this in the book." The appendix covered 8 T4 signals (NLP eye movement, smooth lower eyelids, under-eye wrinkles, hair part direction, finger length ratios, ear shape, phrenology, graphology).

**Pattern/Lesson:** The T4 tier designation still exists in the book's system — signals are still tiered T1-T4 in the working signal table. The appendix detailing removed signals is gone, but the concept of T4 remains as a category label.

---

### 2026-03-18 — Credibility Sequence Numbered Boxes (Ch33)

**Change:** Replaced the flat single-line "1. Demonstrate before explaining. 2. Name what happened accurately. 3. Invite their framework before offering yours." in Ch33 (Mentalism in the Boardroom) with a `CREDIBILITY_SEQUENCE` marker. Added `CREDIBILITY_SEQUENCE_HTML` to `build-book.py` — 3 dark cards in a horizontal grid, each with a large gold number + text.

**Why:** Chris said "format that better, each number should have their own box."

---

### 2026-03-18 — Developmental Critique Applied: VERSION FOR REVIEW Build

**Context:** Received a full professional developmental critique covering structural analysis, chapter-by-chapter diagnostic, inconsistency log, and priority fixes.

**Changes applied to `manuscript-extracted.txt`:**

1. **Dopamine claim softened (Ch4):** "The more dopamine you deliver to your audience, the more compliant and suggestible they will become." → Replaced with a probabilistic, T3-framed explanation: sustained anticipation increases engagement and lowers cognitive resistance — the design principle holds, but not as a linear causal chain.

2. **Ethics preview added to intro:** After "What This Book Is" section, added "A Note on Consent and Intended Use" paragraph — frames the book's intended use before readers encounter compliance/influence chapters.

3. **DECODE workflow preview added before Part Three:** Brief 2-paragraph map of all 6 DECODE steps inserted before Part Three opens, so readers have the workflow spine before learning individual methods.

4. **Closer Design Protocol added to Ch22 (When the Room Rises):** Five design questions added after "The Song Anchor Technique" — covering peak vs. close distinction, collective framing, cascade starters, and clear ending signals.

5. **Two Authority Systems reconciliation note added to Ch27:** "Two Systems, One Architecture" section explains Ch25 = external signals (outputs), Ch27 = internal traits (source). Makes the dual-pillar system explicit and coherent.

**Output:** `Architecture-of-Wonder-VERSION-FOR-REVIEW.html` (3.6MB)

**Why already clean in v2 (no changes needed):**
- "saleince" typo — already fixed
- "complaint and suggestable" — already fixed to "compliant and suggestible"
- Intro part-map — already described all 7 parts
- Five Pillars naming collision — v2 already named them differently: Ch25 = "Five Authority Signals", Ch27 = "Five Pillars of Authority"

**Pattern/Lesson:** Run a pass against the v1 critique list before assuming fixes are needed — v2 had already resolved several items. The developmental critique was based on an earlier draft.

---

### 2026-03-18 — Strolling Chapter Expanded with New Sections

**Change:** Added 10 new sections to Ch22 (The Art of Strolling), rewritten in Chris's voice, after the "Exit Principle" section:
- **Leaving Them Wanting More** — framing intro about strolling as social-environment management
- **Leaving on the Reveal** — Marcus Eddie's advice: leave after the payoff. Why: social pressure drops, honest reactions, energy throws outward
- **Letting the Moment Belong to Them** — don't over-manage the payoff; silence is often the strongest evidence of impact
- **Announce the Visit Before You Begin** — the "I'll be back in 2 minutes" technique; plants anticipation, lowers resistance, warms the group before arrival
- **Room Leader First** — expanded CEO Introduction with full social-proof mechanism explanation
- **Use Applause to Prime the Next Table** — applause as room-level social signal
- **Compliment the Group First** — group feels seen → feels safe → easier to lead
- **Get Their Names** — makes the interaction relational vs. transactional
- **Choose the Right Volunteer** — the volunteer's reaction is social evidence; quality of volunteer often matters more than quality of effect

**Why:** Chris supplied the full strolling content and asked for a rewrite in voice + insertion into the strolling chapter.

**Pattern/Lesson:** The "Announce the Visit Before You Begin" technique is genuinely distinct from any existing section. The social-orientation principle (delayed request > sudden request) is a behavioral mechanism worth preserving with that level of specificity. Keep it verbatim.
