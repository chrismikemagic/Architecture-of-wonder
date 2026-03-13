# The Architecture of Wonder — Book Design Specification

## Design Philosophy

Every design decision in this book is an example of the psychology it teaches. The color choices are behavioral priming. The layout uses attention and salience. The pattern interrupts demonstrate the Von Restorff effect. The margin icons teach pattern recognition. The typography choices exploit processing fluency to build trust before the first paragraph ends. The page turns create micro-tension. The recto pages carry the weight. The cover hides a message only touch reveals.

In Part Six or the afterword, we reveal to the reader what we did to them — breaking down the book's own design as a case study in applied behavioral architecture. That is the standing ovation moment.

**Key statistic:** The brain processes color 60,000 times faster than text. 85% of consumers cite color as the primary reason for a purchase decision. First impressions form in 250 milliseconds. Every surface of this book must win that window.

---

## Color Palette

### Primary Palette

| Role | Hex | Usage | Psychological Function |
|------|-----|-------|----------------------|
| Deep Navy (dark) | `#080F1A` | Chapter opener backgrounds, interstitial pages, "stage" feeling | Authority, intellectual depth, mystery — the mentalism "controlled darkness" |
| Deep Navy (light) | `#0D1E30` | Gradient endpoint, dark page backgrounds | Trust, intelligence, stability |
| Gold | `#C9A84C` | Signature accent — chapter numbers, key terms, pull quotes, tier labels, T1 badges | Premium positioning, prestige, wisdom, achievement |
| Steel Blue | `#1A8FA8` | Secondary accent — sidebars, cross-references, science content, T2 badges | Cognitive stimulation, analytical clarity |
| Warm White/Cream | `#F5F0E8` | Body page background — easier on eyes, signals "crafted" | Clarity, minimalism, scanability |
| Red/Rust | `#A83030` | Warnings, T4 disclaimers, danger callouts — used sparingly for psychological potency | Urgency, danger — sparingly signals high stakes |
| Deep Purple | `#6B52A0` | Advanced concepts, social signal content | Mystery, imagination, mentalism-adjacent resonance |
| Body Text Gray-Blue | `#8A9AB5` | Secondary text on dark backgrounds | — |
| Dim Gray | `#3A4A5C` | Footer text, minor structural elements | — |

### Chapter-to-Chapter Color Drift

| Parts | Temperature | Accent Shift | Psychological Arc |
|-------|-------------|--------------|-------------------|
| Parts 1–2 (The Performance Brain, Reading the Room) | Cool | Steel blue emphasis, clinical precision | Analytical, cerebral — "you are learning" |
| Part 3 (Field Notes) | Transitional | Blue-gold blend, application warmth | Bridge — theory becomes practice |
| Parts 4–5 (Corporate Stage, Neural Performance Model) | Warm | Gold emphasis, mastery and authority | Empowerment, competence — "you are applying" |
| Parts 6–7 (Presence & Perception, The Business Brain) | Deep warm | Dark gold and amber, full authority | Full authority — "you have arrived" |

The reader will not consciously notice. Research confirms that color shifts signal transitions, mood changes, and dramatic turns without conscious awareness (Journal of Children's Literature, 2020). Color saturation shifts — from cool, desaturated tones to warm, rich golds — create a felt sense of progression from clinical understanding to mastery.

### Color Saturation Progression

Within each Part, accent colors should shift in saturation:
- **Part openers**: Full saturation accent colors (maximum visual impact)
- **Early chapters**: Slightly desaturated accents (analytical, restrained)
- **Late chapters**: Full saturation returning (building toward next Part)
- **Effect**: Micro-rhythms of intensity that prevent visual fatigue

---

## Typography

### The Research Foundation

Over 100 years of typography research shows no clear winner between serif and sans-serif for raw readability. The choice should be driven by **personality and context**:

- **Serif fonts** score higher on tradition, authority, credibility, sophistication
- **Sans-serif fonts** score higher on modernity, clarity, friendliness, efficiency
- **The real readability drivers**: Size, spacing, contrast, and line length (50–75 characters optimal) matter far more than serif vs. sans-serif
- **Processing fluency**: Easier-to-read fonts increase trust by up to **40%** — font readability directly affects how favorably people judge content

This means our typography choices are not cosmetic. They are a credibility mechanism. Every font decision either builds or erodes authority before the reader consciously processes a single word.

### Font Pairing

| Element | Font | Style | Psychological Function |
|---------|------|-------|----------------------|
| Body text | Garamond or Minion Pro (serif) | Regular, 10.5–11pt | Authority, credibility, trust — maximizes processing fluency |
| Chapter titles | Montserrat or Brandon Grotesque (sans) | Bold, all-caps, wide letter-spacing (3–4px) | Geometric precision signals modernity and confidence |
| Section headers | Same sans-serif family | Semibold, title case | Visual hierarchy without font proliferation |
| Marginalia / War Stories | Helvetica Neue Light or similar sans-serif | Light weight, 9pt, gold or steel blue | "Double-encoding" — distinct from body by both typeface AND color (Greene/Andrews model) |
| Callouts/Sidebars | Same sans-serif family | Medium weight, smaller size | Separates "aside" from main flow |
| Diagrams | Calibri (sans) | As established in existing SVG system | Consistency with existing graphics |

### Display Typography for Chapter Titles

The contrast between header and body fonts should be immediately distinguishable — "if everything stands out, nothing stands out." For mentalism/psychology:
- **Chapter titles**: Elegant geometric sans-serif with wide letter-spacing creates intrigue without sacrificing readability
- **Drop caps**: Oversized first letter of each chapter in the display sans-serif, set in gold — signals new unit, adds visual flair
- **The contrast** between sans-serif chapter titles and serif body text creates a rhythm of "announcement then conversation"

### Number Style

- **Old-style (lowercase) figures** in body text — signals design literacy
- **Lining (uppercase) figures** in tables, data, observation numbers — clean alignment

### Line Length

- **Body text**: 50–75 characters per line (optimal for comprehension)
- Set text block width to achieve this range at the chosen type size
- This is non-negotiable — line length affects comprehension more than font choice

---

## Layout & Cognitive Psychology Techniques

### 1. Von Restorff Effect (Isolation Effect)

**Principle:** When multiple similar items are present, the one that differs is most likely to be remembered (Fabiani & Donchin, 1995).

**Application:**
- Every chapter has ONE "spotlight" element — a callout box with dark background, reversed-out text, gold border
- In the observation list, T1 observations are visually distinct: bolder, slightly larger, gold marker
- Readers anchor on T1 first, then navigate to T2/T3
- **Critical constraint: "If everything stands out, nothing stands out."** Use sparingly and with intention — maximum ONE spotlight per chapter, maximum ONE pull quote per spread

### 2. Serial Position Effect (Primacy + Recency)

**Principle:** People remember the first and last items in a sequence best; middle items are forgotten. The primacy effect persists even after distractions. The recency effect fades after ~30 seconds.

**Application — Chapter Level:**
- **Open** every chapter with a provocative one-liner or observation (a hook, not a summary) — primacy
- **Close** every chapter with a "key read" — one sentence set in gold with generous whitespace — recency
- **Bury** supporting details, elaboration, and nuance in the middle — this is where depth lives, but not where memory anchors

**Application — Page Level:**
- Place key takeaways at the **top and bottom** of pages
- Middle content can be elaboration and supporting detail

**Application — Book Level:**
- The **first chapter** (Designing for Reality) and **last section** (The Meta Reveal / Closing) carry disproportionate weight in memory
- The Introduction must hook within the first paragraph
- The Meta Reveal must land as a standing ovation

### 3. Pattern Interrupts

**Principle:** An unexpected element that breaks habitual processing captures attention (derived from NLP). The brain stops noticing anything predictable.

**Application — every 8–12 pages, break the layout:**
- Full-bleed dark page with a single quote or stat in gold
- "Field Note" sidebar that shifts column width
- Case study in distinctly different format (narrower column, tinted background)
- Hand-drawn-style annotation or sketch
- Shift in ink color for a single paragraph or pull quote
- **Must be used with restraint** — too frequent and they become the new pattern

**Effective interrupt types (ranked by impact):**
1. Full-page dark spread with single gold element (strongest)
2. Column width change (strong)
3. Pull quote in contrasting typeface (moderate)
4. Tinted background box (moderate)
5. Margin annotation shift (subtle)

### 4. Progressive Disclosure

**Principle:** Sequence information to prevent overwhelm. Reveal complexity gradually.

**Application for complex frameworks (80 observations, Neural Performance Model):**
- Introduce 3–5 observations in context within a chapter
- Reference the full list as a "turn to page X" moment
- The full list in the back acts as a reward — readers feel they earned the reference tool
- **Structure**: Chapter opener frames the "big idea" → supporting arguments unfold → synthesis at end

### 5. Visual Anchoring and Priming

**Principle:** Exposure to a word, image, or color unconsciously influences how the reader processes subsequent content. Colors, imagery, and symbols can all prime emotional responses without conscious awareness.

**Application:**
- **Epigraphs at chapter openers** prime the reader's mindset for the content ahead — associative priming
- **Recurring visual motifs** (observation icons, tier badges) build unconscious associations across chapters — repetitive priming
- **Color-coded section openers** prime emotional state: cool blue primes analytical thinking, warm gold primes confidence and mastery
- **The Ten-Second Scan photographs** prime observational alertness before each Part

### 6. Processing Fluency

**Principle:** The easier something is to process, the more the reader trusts it, likes it, and remembers it. Font readability directly affects how favorably people judge content.

**Application:**
- Body text in a highly readable serif at optimal size (10.5–11pt)
- Generous leading (line spacing) — minimum 135% of type size
- Optimal line length (50–75 characters)
- Consistent, predictable page grid — the structure itself is invisible and trustworthy
- **White space reduces cognitive load, guides the eye, and creates mental rest stops**
- White space is not wasted space — it is an active design element

---

## Design Elements

### Margin Observation Icons

Four small icons placed as margin markers whenever an observation type appears in text:

| Code | Icon | Meaning |
|------|------|---------|
| BP | Eye icon | Baseline / Physical |
| CR | Fingerprint or profile silhouette | Character Reading |
| VS | Waveform or speech indicator | Verbal / Social |
| AM | Directional arrow | Action / Motivation |

Readers develop pattern recognition without conscious effort — they start "seeing" the categories everywhere. Icons placed in outer margins where they get their own space without competing with body text.

**Icon design requirements:**
- Must match the book's overall typographic style — simple, geometric, monoline
- Rendered in the category's accent color at reduced opacity (60%)
- Consistent size across all instances
- Placed at the vertical center of the paragraph they reference

### Tier Badges

Small, color-coded pill shapes used inline whenever a signal is mentioned:

| Tier | Style | Color |
|------|-------|-------|
| T1 | Solid pill | Gold `#C9A84C` |
| T2 | Solid pill | Steel Blue `#1A8FA8` |
| T3 | Outlined/hollow pill | Gray outline |
| T4 | Dashed-outline pill | Dim gray, dashed border |

Visual hierarchy instantly communicates confidence level.

### The Greene-Model Marginalia System

**Inspiration:** Robert Greene's *48 Laws of Power* (designed by Joost Elffers) uses two-color, dual-narrative marginalia. RJ Andrews adapted this in *Info We Trust* using blue + Helvetica Neue Light for sans-serif "double-encoding."

**Our implementation:**
- **Main text** (serif, black/dark brown): Teaches the concept, presents the framework
- **Marginalia** (sans-serif light weight, gold or steel blue): War stories, practitioner notes, "in practice" wisdom, shortcuts
- **The reader chooses** when and how to engage with the secondary layer — it enriches without disrupting
- **Requires wide outer margins** (minimum 25mm / 1 inch) to accommodate 9pt marginalia text
- **Visual separation through double-encoding**: Different in BOTH typeface (sans vs. serif) AND color (gold/blue vs. black)

**What goes in the marginalia:**
- Field stories and anecdotes ("I once had a volunteer who...")
- Practitioner shortcuts ("In practice, skip to the cluster check")
- Cross-references ("See Observation #34")
- Historical quotes and parables relevant to the main text
- Contrarian notes ("Some performers disagree — here's why")

### "What You Just Did" Moments

The book reveals something the reader just did without realizing it:

- "You've been reading this page for about 90 seconds. Notice which hand is holding the book. That's Observation #01."
- "If you skipped the Tier 4 appendix heading, that's confirmation bias — you trusted my framing. Flip back and read it."
- "You formed your first impression of this page in 250 milliseconds. What did you notice first — the number, or the word? That is salience at work."
- Embed an observation test in a chapter opening photo, reveal what they should have noticed at chapter's end.

Experiential design — the book practices what it preaches.

**Design treatment:** Set in a distinct style — italicized body font, indented, with a thin gold vertical rule on the left margin. Must feel like the author leaning in and speaking directly to the reader.

### The "Ten-Second Scan" Page

Before each Part: a full spread showing a photograph of a person. No labels. No guidance.

"What do you notice? Take ten seconds."

Next page: numbered annotations breaking down what a trained reader catches. This is the primary exercise format.

**Design requirements:**
- Photograph on recto (right-hand) page for maximum visual attention
- Annotations on the following verso (left-hand) page — so the reader must turn the page to see answers
- This prevents accidental spoiling and creates a natural page-turn suspense mechanism

### Pull Quotes

- Extract key phrases and re-present them in a larger, distinct typeface
- Serve dual purpose: visual pattern interrupt AND content teaser
- Increase skimmability for readers who scan before committing to deep reading
- Set in sans-serif display weight, gold color, with generous surrounding whitespace
- **Maximum frequency**: One per spread (two-page view). More than that dilutes impact.
- Place on recto pages when possible — right-hand pages receive more visual attention

### Black-Edge Pages / Thumb Index

Page edges of each Part printed in a subtly different shade:

| Part | Edge Color | Temperature |
|------|------------|-------------|
| Part 1 | Cool blue-gray | Clinical |
| Part 2 | Steel blue tint | Analytical |
| Part 3 | Neutral | Transitional |
| Part 4 | Warm gold tint | Applied |
| Part 5 | Amber | Mastery |
| Part 6 | Deep gold | Authority |
| Part 7 | Dark warm | Full command |

Tactile navigation — the book feels like a tool, not just a read.

### Footnotes as Performance (Dual Reading Path)

Main text teaches. Footnotes/marginalia share war stories, shortcuts, and "in practice, here's what actually happens." Two reading experiences in one book.

**The Greene insight (from RJ Andrews):** This system "not only provides an additional layer of information, it creates an opportunity for a whole new dimension of meaning" — and it does so without disrupting the main text, unlike textbook-style annotations.

---

## Spread Design & Page Architecture

### Recto Page Bias

**Research finding:** Right-hand (recto) pages receive more visual attention than left-hand (verso) pages.

**Application:**
- Place key content, spotlight callouts, and "What You Just Did" moments on recto pages
- Chapter openers always begin on recto pages (standard practice, reinforced by research)
- Pull quotes preferentially placed on recto pages
- The Ten-Second Scan photograph on recto; annotations on following verso

### The Page Turn as Suspense

**Principle:** The page turn is a natural suspense mechanism. Ending a recto page with an unresolved thought or question creates micro-tension.

**Application:**
- End recto pages with questions, incomplete thoughts, or setup lines when possible
- The reveal, answer, or payoff appears at the top of the next verso page
- This is the reading equivalent of the "open loop" technique in performance
- **Chapter closers**: The "key read" sentence in gold should appear on a recto page, forcing the reader to turn past it to reach the next chapter — leaving the key read as the last thing in working memory

### Spread Composition

The two-page view when a book lies open should be considered as a compositional unit:

- **Verso (left)**: Can carry denser text, supporting detail, marginalia
- **Recto (right)**: Key content, spotlight elements, pull quotes
- **Balance**: The spread should feel balanced but not symmetrical — visual weight slightly favoring recto
- **Whitespace**: Generous inner margins (gutter) prevent text from feeling cramped at the spine

---

## Chapter Structure Template

Every chapter follows a consistent structure. Consistency creates rhythm and predictability while delivering varied content. The reader develops expectations that the book can then satisfy — or strategically violate.

### The Chapter Arc

| Element | Position | Design Treatment | Cognitive Function |
|---------|----------|-----------------|-------------------|
| **Epigraph** | Chapter opener (dark page) | Italic serif, gray-blue, centered | Associative priming — sets mindset |
| **Chapter Number** | Chapter opener | Large gold sans-serif (72pt), centered | Visual anchor, wayfinding |
| **Chapter Title** | Chapter opener | All-caps sans-serif, letterspaced, white | Identity, expectation setting |
| **Hook Line** | Chapter opener | Italic serif, gray-blue, below title | Serial position (primacy) — the first thing remembered |
| **Drop Cap** | First paragraph of body text | Oversized first letter in sans-serif, gold | Signals new unit, creates visual entry point |
| **Body Text** | Main content | Serif, 10.5–11pt, warm cream background | Processing fluency, trust building |
| **Spotlight Box** | Once per chapter | Dark background, reversed text, gold border | Von Restorff isolation — the ONE thing they remember |
| **Pattern Interrupt** | Every 8–12 pages | Varies (dark page, sidebar, case study) | Attention reset, prevents habituation |
| **Marginalia** | Throughout, outer margins | Sans-serif light, gold or blue | Dual reading path, practitioner wisdom |
| **Section Breaks** | Between major sections | Gold centered dots (· · ·) | Breathing room, cognitive reset |
| **Key Read** | Final element | Gold italic, generous whitespace, between gold rules | Serial position (recency) — the last thing remembered |

### Chapter Opener Design

- **Sink**: Chapter text starts one-third to halfway down the dark page
- **Part number** in subtle dim gray at top
- **Chapter number** large and gold in the center third
- **Title** in white, all-caps, letterspaced below the number
- **Hook line** in gray-blue italic below a thin gold divider
- **Tier badges** and **margin icons** as a visual legend at the bottom
- **Always begins on a recto page**

### Part Opener Design

- **Full dark spread** (both pages dark)
- Part number and title centered
- **The Ten-Second Scan** exercise follows the Part opener
- Opportunity for a visual map of the Part's chapters
- Can include a single epigraph or thematic image
- **Interstitial breathing room**: At least one blank or near-blank page between Parts

---

## Physical / Print Design

| Element | Specification | Psychological Function |
|---------|---------------|----------------------|
| Paper stock | Uncoated, cream/ivory, 80–90gsm matte | Intellectual, premium feel — uncoated signals authenticity and craft |
| Cover | Soft-touch matte lamination + spot UV on title and key elements | Tactile contrast — people react to texture before processing text |
| Cover texture | Emboss or deboss the title | Tactile engagement — 3D relief creates deeper first impression |
| Spot UV hidden message | A line of text on the back cover visible only at certain angles | For a mentalism book, the reader who discovers it has already passed the first test |
| Chapter openers | Heavier stock or different background tint | Tactile "new section" signal |
| Cover format | French flaps (folded-in flaps on trade paperback) | Adds perceived value; inside flaps carry Five Cs reference and icon key |
| Part divider pages | Consider slightly different paper stock (e.g., slightly heavier, or lightly tinted) | Tactile chapter markers — the book becomes a physical tool |

### Cover Design Psychology

**Research-backed approach for psychology/mentalism non-fiction:**
- **Dark base** (black or deep navy) — nearly universal in mentalism-adjacent books, signals sophistication and mystery
- **Gold or metallic typography** against dark field — premium positioning
- **Restrained, monochromatic scheme** — signals scholarly depth, avoids "campy magic" associations
- **Effect**: "Controlled mystery" — sophisticated, not theatrical
- **A single well-executed tactile element** (embossed title with spot UV) is more impactful than multiple competing techniques

### Spot UV Hidden Element

**Concept:** On the cover or endpapers, include a line of text or symbol rendered in spot UV (clear high-gloss coating) on a matte background. It is invisible at most angles but discoverable by touch and by tilting the book in light.

**Suggested text:** *"You're already reading people. You just proved it."*

**Why this works:** For a book about observation and perception, a hidden element that rewards close attention is the perfect opening move. The reader who notices it before reading the book has already demonstrated the skill the book teaches. The reader who discovers it after finishing the book experiences the Meta Reveal physically.

---

## The Five Cs of Behavioral Reading

**This chart is essential to the book** — it is the framework without which individual signals are noise.

### The Five Cs Chain

| # | C | Key Question | Rule |
|---|---|-------------|------|
| 1 | **Context** | What environment? | Same gesture means different things in different settings. Context determines meaning. Always. |
| 2 | **Clusters** | Multiple signals? | One signal is noise. Three co-occurring behaviors = a pattern. Never act on a single signal. |
| 3 | **Congruence** | Body = words? | When body says one thing and words say another: body is truth. Incongruence is your most reliable signal. |
| 4 | **Consistency** | Their baseline? | Compare to that individual's personal baseline. Not generic. Deviation from their baseline is the data. |
| 5 | **Culture** | Background norms? | Eye contact, space, expressiveness vary significantly. Calibrate before concluding. |

**Apply as a chain — not a checklist.**

Most weak readings fail because they skip this chain. They treat behavior like a vending machine. Real behavior breathes. It moves. It has to be read in motion, against a baseline, inside a context.

### Placement in the Book

The Five Cs should appear:
1. **First introduction** in Chapter 6 (Behavioral Profiling in Real Time) as the foundational framework
2. **Reference card** in the Field Notes section (Part Three) as a standalone page
3. **Quick-reference** on the inside French flap or bookmark ribbon pull-out
4. **Reinforced** throughout — every case study and observation discussion should implicitly or explicitly reference the chain

---

## The Meta Reveal

Somewhere in Part Six or the afterword, break the fourth wall. This is the culmination of every design decision in the book. It should be a full section — not just a paragraph — that systematically unpacks what was done to the reader.

> *"You have been reading a book that demonstrated its own content on every page.*
>
> *The gold accent that drew your eye to key terms? That was salience architecture — the same attentional capture this book teaches you to engineer on stage.*
>
> *The pattern interrupts every eight pages — the dark spreads, the shifted columns, the sudden statistics? Von Restorff. The isolation effect. You remembered those pages because they were different. That is exactly what Chapter Two taught you to do.*
>
> *The chapter openers that hooked you with a single line before you decided whether to keep reading? Serial position effect. Primacy. Your brain encoded that first sentence before you chose to engage — and it anchored everything that followed.*
>
> *The margin icons you stopped noticing but kept processing? Priming. By Chapter Ten, you were categorizing behavioral signals into BP, CR, VS, and AM without thinking about it. The icons trained you.*
>
> *The warm cream pages that made you trust the text before you evaluated a single argument? Processing fluency. Readable fonts increase trust by forty percent. You felt this book was credible before you decided it was credible.*
>
> *The color temperature of the accents — cool and clinical at the start, warming to gold and amber by the end? You didn't notice. But you felt the progression. From student to practitioner to authority. The color arc primed your identity shift.*
>
> *The key read at the end of every chapter, set in gold between thin lines with generous whitespace? Recency. The last thing in working memory is the thing that stays. Every chapter planted its seed in that final line.*
>
> *Even the cover. Soft-touch matte with a raised title you could feel. A hidden line of text in spot UV, visible only when you tilted the book into light. If you found it, you already proved the first lesson: the trained eye sees what others miss.*
>
> *This book was not just written. It was designed to read you while you read it.*
>
> *And now you know how."*

That is the standing ovation moment.

### Design Treatment for the Meta Reveal

- **Full dark spread** to signal this is different from normal body text
- Each paragraph separated by generous whitespace
- Key psychological terms set in **gold** inline
- The final two lines — *"This book was not just written..."* and *"And now you know how."* — isolated with maximum whitespace, gold, larger type
- This section should feel like the curtain call: dramatic, confident, earned

---

## Design Reference: Inspirational Models

### Robert Greene / Joost Elffers (48 Laws of Power)
- Two-color dual-narrative marginalia (black body + red marginalia)
- Structured chapter template (statement, explanation, transgression, observance, reversal)
- Multiple reading paths — reader chooses engagement depth

### RJ Andrews (Info We Trust)
- Adapted Greene model: blue marginalia (Helvetica Neue Light) alongside black body (Minion)
- "Textual double-encoding" through both color AND typeface differentiation
- 4-column grid with strong baseline grid

### House of Leaves (Mark Z. Danielewski)
- Typography IS narrative: different typefaces distinguish narrators
- Page layouts control reading pace (single words to dense footnote blocks)
- "Interrogated established practices of book design and refocused them to narrative ends"

### Key Takeaway for This Book
We are not making an art object. We are making a **tool that teaches by example**. Every Greene-model element we adopt must serve the reader's learning, not the designer's portfolio. The test: *Does this design choice demonstrate a principle taught in the text?* If yes, include it. If no, it is decoration.

---

## Production Checklist

### Pre-Design
- [ ] Finalize trim size (recommended: 6" × 9" or 234mm × 156mm — standard trade non-fiction)
- [ ] Confirm page count estimate (target: 280–320 pages)
- [ ] Source cover photography or commission illustration
- [ ] License typefaces (Garamond/Minion Pro, Montserrat/Brandon Grotesque, Helvetica Neue Light)
- [ ] Commission Ten-Second Scan photographs (7 photographs, one per Part)

### Cover Design
- [ ] Dark navy/black base with gold foil or metallic ink title
- [ ] Soft-touch matte lamination across full cover
- [ ] Spot UV on title text and key cover element
- [ ] Embossed/debossed title for tactile engagement
- [ ] Spot UV hidden text on back cover (discoverable by touch/angle)
- [ ] French flaps with Five Cs reference (inside front) and icon key (inside back)

### Interior Design
- [ ] Set up master page grid with wide outer margins (minimum 25mm for marginalia)
- [ ] Create chapter opener template (dark gradient, gold number, white title, hook line)
- [ ] Create body page template (cream background, running header, margin icon zones)
- [ ] Create pattern interrupt templates (dark full-bleed, sidebar shift, case study box)
- [ ] Create spotlight box template (Von Restorff element)
- [ ] Create key read template (chapter closer in gold)
- [ ] Create Part opener template (full dark spread + Ten-Second Scan)
- [ ] Design tier badges (T1–T4) as character styles or inline graphics
- [ ] Design margin icons (BP, CR, VS, AM) as placed graphics
- [ ] Set up marginalia text frame on all body pages
- [ ] Design pull quote style (sans-serif, gold, generous whitespace)
- [ ] Design drop cap style for chapter first paragraphs
- [ ] Design "What You Just Did" moment style

### Typography Setup
- [ ] Body text: Garamond/Minion Pro, 10.5–11pt, 135%+ leading
- [ ] Chapter titles: Sans-serif, bold, all-caps, 3–4px letter-spacing
- [ ] Marginalia: Sans-serif light, 9pt, gold or steel blue
- [ ] Pull quotes: Sans-serif, 14–16pt, gold
- [ ] Key read: Serif italic, 11pt, gold, centered
- [ ] Running headers: Sans-serif, 8pt, gray-blue, letterspaced
- [ ] Footnotes: Sans-serif, 8pt, gray

### Printing
- [ ] Paper: Uncoated cream/ivory, 80–90gsm matte
- [ ] Binding: Perfect bound with French flaps
- [ ] Edge printing: 7-shade thumb index progression (cool to warm)
- [ ] Consider heavier stock for Part divider pages
- [ ] Confirm spot UV and embossing capabilities with printer
- [ ] Request press proof for color accuracy on cream stock
