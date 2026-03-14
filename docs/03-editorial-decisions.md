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

## Content Consolidation (Field Notes)

**Decision:** Consolidated scattered neuroscience content into Part Three (Field Notes) as themed sections rather than numbered chapters. Topics: Attention and Prediction, Neurochemistry and Threat, Memory and Embodiment, Influence and Compliance, Salience and Framing, The Body as Signal.
