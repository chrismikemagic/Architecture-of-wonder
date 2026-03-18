# Editorial Decisions Log

> Every structural decision, chapter move, or content reorganization documented here with rationale.

---

## Chapter 6 Removal (Authority Stub → Chapter 24)

**Decision:** Removed Chapter 6 ("Authority, Credibility, and the Psychology of Belief") as a standalone chapter. It was only two paragraphs — a fragment, not a chapter.

**Where the content went:** Folded into Chapter 24 (The Authority Frame) as opening paragraphs. The two paragraphs about trust as a physiological state and credibility as behavioral broadcasting now lead into the Five Pillars of Authority.

**New flow:** Trust is limbic → Credibility is behavioral → Here are the five pillars

**Result:** Part One tightened from 6 chapters to 5. Book renumbered from 41 chapters to 40.

---

## Chapter 7 (now Chapter 6) Restructuring — Behavioral Profiling

**Decision:** Complete reorder of sections based on editorial blueprint.

**Old order:** What You Have Felt Before → Definition → Evidence Framework → Three-Signal Rule → Stage/Strolling → Observer Errors → Cultural Calibration → Lie Detection → Baseline → Five Cs → Deviation → Leakage → Eye Movement

**New order:**
1. Body Language Is Mostly Bullshit (provocative hook)
2. What Behavioral Profiling Is — and Is Not
3. The Foundation: Baseline First
4. High-Yield Baseline Signals
5. The Five Cs
6. Reading Deviation
7. The Leakage Window
8. Eye Movement and the Baseline Principle
9. The Evidence Framework: T1–T4
10. The Three-Signal Rule
11. Stage Context vs. Strolling Context
12. Common Observer Errors
13. Cultural Calibration in Practice
14. Observation Is Not Lie Detection

**Rationale:** myth → definition → foundation → framework → application → caution. The old order front-loaded technical frameworks before establishing why they matter. The new order kills the cheap version of body language, positions behavioral profiling as the serious alternative, then builds from foundation (baseline) through framework (Five Cs) to application (deviation, leakage, evidence tiers) and ends with disciplined boundaries (not lie detection).

**The "Body Language Is BS" opening:** Option A (strongest) was chosen — it's the first line of the chapter. Immediately qualified with "At least, the way most people use the term." Provocation and solution arrive together.

---

## Five Cs Expansion

**Decision:** Expanded the Five Cs from single-line definitions to full textbook-style descriptions with rules, field applications, and the "chain not checklist" doctrine.

**Format:** Each C gets: definition, key question, the rule, field application for mentalists, and common mistakes.

**Doctrine line:** "If you are not observing through all five, you are not reading behavior. You are narrating noise."

---

## Mentalist Framing Throughout

**Decision:** Added mentalist-specific context throughout Chapter 6 (formerly 7). Not changing the science, but grounding every principle in performer reality.

**Examples added:**
- Volunteer walks as baseline windows (5-7 seconds of unguarded movement)
- Leakage during reveals (the hand that tightened on the card)
- T1 reads as opening gambits (they land because they're specific and verifiable)
- Strolling set tactics (move on one, verify on two, adjust on three)
- Strategic case for "behavioral profiling" over "lie detection" as professional identity

---

## Part Structure (Conceptual vs. Applied)

**Editorial note from restructuring session:** The book has both a conceptual argument and a practitioner manual. These should feel separated within chapters:

- **Part 1 (Conceptual):** Body language is misunderstood → behavioral profiling defined → baseline → Five Cs → deviation
- **Part 2 (Application):** Leakage window → eye movement → evidence tiers → three-signal rule → stage vs strolling → observer errors → cultural calibration → not lie detection

---

## Chapter 15 Expansion (Hypnosis)

**Decision:** Expanded from a brief overview to comprehensive cell-level neuroscience treatment. This is one of the deepest scientific chapters in the book.

**Approach:** Goes to the neural mechanism level while maintaining Chris's voice (short declaratives between long analytical passages, TikTok parenthetical humor).

---

## Voice Overhaul (Early Sessions)

**Decision:** Rewrote Acknowledgments, Introduction, and Chapters 1-2 to match Chris's actual speaking voice.

**Key changes:**
- Cut academic tone
- Added field stories with setting, stakes, and a clock
- Fixed opener duplication
- Added direct reader address

---

## Em Dash Reduction (v3.0)

**Decision:** Reduced excessive em dash usage throughout manuscript. Standardized labels and formatting.

---

## Figure Integration System

**Decision:** Established a system for embedding photos/figures into the book, starting with the seven universal expressions photo in Chapter 10 (The Micro-Expression Matrix).

**Approach:** Figures are managed through two parallel systems:
1. Embedded in the DOCX via OOXML (visible in Word/Google Docs)
2. Mapped in `build-book.py`'s `FIGURES` dictionary for HTML output

**Why not just one?** The text extraction step strips images from the DOCX. The build script needs its own figure map to inject `<img>` tags into the HTML. The DOCX embedding ensures the author sees images while writing.

**First figure:** Author-owned photograph of the seven universal facial expressions (Anger, Disgust, Fear, Happiness, Sadness, Surprise, Contempt), placed after "The Seven Expressions" section header.

**Rights tracking:** Each FIGURES entry includes a `rights` field. Only author-owned or properly licensed images should be embedded.

---

## Chapter Reorder: Eyes/Face Moved Before Micro-Expression and Cold Reading

**Decision:** Moved Chapter 11 (The Language of the Face / Eyes/Face) to Ch9, immediately after the DISC chapter (Ch8). New order: Ch9 = Eyes/Face, Ch10 = Micro-Expression Matrix, Ch11 = Cold Reading.

**Why:** Chris determined that physical face-reading (eyes, brow, lip compression) is foundational and should follow DISC directly, before micro-expressions and cold reading. The logical sequence is: DISC profiles → face/eye reading → micro-expression → cold reading application.

**FIGURES, HOOK_LINES, KEY_READS** all updated in `build-book.py` to reflect new numbering. Ch9 hook: "The face performs. The eyes search." Ch10 hook: "Partial, rapid, and involuntary…"

---

## Duchenne Marker → Duchenne Smile

**Decision:** Renamed "The Duchenne Marker" to "The Duchenne Smile" everywhere in manuscript and build script.

**Why:** Chris's preference. "Duchenne Smile" is the standard term; "marker" felt clinical.

---

## Performer's Note → Chris Michael's Take

**Decision:** Renamed the "Performer's Note" callout box label to "Chris Michael's Take" everywhere via `gen_performer_note()`.

**Why:** More personal, more specific to the author, better fits the conversational authority voice.

---

## Lip Compression Section Added to Ch9 (Eyes/Face)

**Decision:** Added full Lip Compression section to Ch9 (Eyes/Face) before "The Eyes in the Larger Frame." Text added exactly as Chris supplied, with bullet points formatted on separate `·` lines.

**Lesson:** Never rewrite Chris's directly-supplied text. Add it as-is and format it for the book's visual system.

---

## D-Type Precision and Group Strategy (DISC Chapter)

**Decision:** Added two new passages to the D-type section:
1. "They also notice, and reward, when you get to the point." — added to the D-type signal paragraph.
2. New paragraph on winning D/DI personalities first in a group room — they function as opinion-leaders whose compliance lowers the threshold for everyone else.

---

## Fruit to Fang Section Restructured

**Decision:** Reordered the Fruit to Fang section in Ch9: Title → flow chart (FRUIT TO FANG APPLICATION trigger) → all explanatory prose. Previously prose appeared both before and after the chart.

**Other Fruit to Fang changes:**
- Subtitle changed to "Propless Method: Using the Eyes to Discern a Vowel in a Word"
- E branch: "Eagle / Elephant" (not just Elephant)
- "not a real animal" (not "not really an animal")
- Em dashes replaced with commas in two phrases
- REFLEX context added to The Setup sub-section

---

## T4 Signal Cards Reinstated Inline (Ch7)

**Decision:** Added T4 signal cards (SIGNAL 1–4) back into Ch7 (80-Signal System) as inline rendered cards after the "T4 Signals Removed" explanatory paragraph, using `gen_t4_signal_card()`.

**Why:** Chris wanted the T4 signals visually present in the chapter rather than removed entirely. The disclaimer paragraph explains their epistemic status before the cards appear.

---

## Meta Reveal: Reciprocity Trigger Section Added

**Decision:** Added "The Reciprocity Trigger" section to META_REVEAL_HTML. Explains the skipped-ahead note at the top of Ch10 (Micro-Expression) and the reciprocity mechanism: acknowledging sequential readers with "I respect that" creates goodwill and trust.

---

## Neural Term Inline Descriptions

**Decision:** Added brief parenthetical descriptions at the first body-text use of every neural/brain term throughout the manuscript.

**Terms annotated:** dopamine, salience network, limbic system, hippocampus, amygdala, visual cortex, orbitofrontal cortex, medial prefrontal regions, basal ganglia, dorsolateral prefrontal cortex, executive control network, primary somatosensory cortex, locus coeruleus, nociceptors, brainstem, thalamus, mirror neurons.

**Terms already self-described inline (no change needed):** zygomatic major, orbicularis oculi, cortical pyramidal neurons, norepinephrine function, acetylcholine function.

**Why:** Chris wants readers who are not neuroscientists to have the anatomical context immediately, without needing to look it up.

---

## Content Consolidation (Field Notes)

**Decision:** Consolidated scattered neuroscience content into Part Three (Field Notes) as themed sections rather than numbered chapters. Topics: Attention and Prediction, Neurochemistry and Threat, Memory and Embodiment, Influence and Compliance, Salience and Framing, The Body as Signal.

---

## Chapter 10 Renamed + Rewritten: "Chris Michael's Tell Table"

**Decision:** Chapter 10 renamed from "The Performance Read Panel" to "Chris Michael's Tell Table." Full introduction rewritten.

**New intro distinction:** The 80-Signal System is a *profiling tool* — used before/during performance to build predictions about who someone is. The Tell Table is a *reading tool* — used in real time to extract what is happening right now. Key phrase: "Profiling reads the person. Reading reads the moment."

**BEHAVIORAL_READING_DEF_HTML callout:** Moved from Ch11 to Ch10. It defines Behavioral Profiling vs. Behavioral Reading — this boundary chapter is the correct location. New trigger point: "Profiling reads the person. Reading reads the moment."

**Chapter structure:** Five Things Panel → Tell Table (full signal grid) → Mini Scenarios → Quick-Reference Cheat Sheet → prose close.

---

## Chapter 11 Opener Rewritten

**Decision:** Removed "From Profiling to Reading" transition section (now in Ch10). New opener focuses on the face/eyes distinction:
- "The face is the most socially managed surface in human interaction."
- "The eyes are different. Not because people are not trying to manage them, but because the movements that carry real information happen before the social response is assembled."

**Why:** The old intro's subject matter had been moved to Ch10. Ch11 needed a standalone opening that worked without relying on Ch10's profiling/reading framing.

---

## BTE Signal Panel Color Fix

**Decision:** Changed `.bte-signal` background from `rgba(13,30,48,.5)` to solid `#0d1117`. Changed `.bte-cluster-wrap` from opacity-based dark to `#0d1117`. Changed `.bte-cluster-header` to `#0a0e14`.

**Why:** 50% opacity dark blue over parchment background computed to washed-out gray (~#818b8c). Screenshot showed panels were unattractive and hard to read.

**Rule going forward:** Never use rgba opacity for container backgrounds in this book. The parchment page background will interact with any transparency and produce gray. Always use solid hex.

---

## APPENDIX A1 (T4 Signal Review) Removed

**Decision:** Removed APPENDIX A1 "T4 Signal Review: The Evidence Record" entirely. Also removed the sentence referencing the appendix from the Ch7 signal table intro.

**Content removed:** 8-signal deep-dive on NLP eye movement, smooth lower eyelids, under-eye wrinkles, hair part direction, finger length ratios, ear shape, phrenology, graphology — each with THE CLAIM / THE RESEARCH / WHAT REMAINS VALID structure.

**Note:** The T4 tier designation itself remains in the system — signals are still labeled T1-T4 in the working table. The removed appendix was the explanatory deep-dive. It's gone; the tier label stays.

---

## Performance Read Panel: Four HTML Visual Components

**Decision:** Built four HTML panel constants in `build-book.py` for Ch10:
1. `FIVE_THINGS_PANEL_HTML` — 3+2 SVG card grid (5 questions, color-coded)
2. `SIGNAL_TABLE_HTML` — "Chris Michael's Tell Table" HTML/CSS table, 3-color sections
3. `MINI_SCENARIOS_HTML` — 2-card green/red scenario pair
4. `CHEAT_SHEET_HTML` — 3-column quick-reference grid

**Architecture decision:** All text-heavy panels use HTML/CSS, not SVG. SVG text in a 900-unit viewBox renders at approximately 6px on screen — unreadable. Only the Five Things Panel (graphical card layout) uses SVG.

---

## Credibility Sequence Numbered Boxes (Ch33)

**Decision:** Replaced flat single-line "1. Demonstrate before explaining. 2. Name what happened accurately. 3. Invite their framework before offering yours." in Ch33 with a `CREDIBILITY_SEQUENCE` marker injecting three dark-background numbered cards (CREDIBILITY_SEQUENCE_HTML).

---

## VERSION FOR REVIEW: Developmental Critique Editorial Pass

**Decision:** Applied targeted fixes from a professional developmental critique. Five changes:
1. Softened dopamine→compliance causal claim in Ch4 (T3 framing added)
2. Ethics preview paragraph added to intro ("A Note on Consent and Intended Use")
3. DECODE workflow map inserted before Part Three (spine preview before methods)
4. Closer Design Protocol (5 design questions) added to Ch22
5. "Two Systems, One Architecture" reconciliation note added to Ch27

**Output:** `Architecture-of-Wonder-VERSION-FOR-REVIEW.html`

**Items already resolved in v2:** saleince typo, complaint/suggestable typo, intro part-map omission, Five Pillars naming collision (Ch25 = "Five Authority Signals" / Ch27 = "Five Pillars").
