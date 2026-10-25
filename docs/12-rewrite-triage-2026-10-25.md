# Rewrite triage, 2026-10-25

Chapter-by-chapter verdict for the Built for Wonder rewrite, after a full read of the manuscript (143,170 words in chapters plus 1,224 of front matter) against two things that changed since the book was drafted: Chris's own writing register (memory `chris-voice.md`, Register 6, the Sapien edit) and the Joe Navarro Body Language Academy method Chris now trains in (memory `body-language-academy.md`, modules 07 and 08, and the Train the Trainer pre-readings, Vrij 2019 as the ceiling for any deception claim).

Nothing in the DOCX was changed for this triage.

## Verdict key

- KEEP: the content stands. Chris re-dictates the connective prose in his own voice; his named passages stay verbatim; listed fixes get made.
- REWRITE: the content is defensible but the whole chapter reads as a model essay. Chris re-dictates it from a brief; cuts listed.
- REBUILD: the content itself has to change (Navarro frame, new knowledge, truth or rights).
- MERGE or CUT: as stated.

## Why a cleanup pass is not enough

- The repo's own voice guides (`CLAUDE.md` "Chris's Voice" and `docs/02-voice-and-style-profile.md`) prescribe mic-drop closers, short declarative punches and provocative one-line openers. That is the register Chris rejected in October 2026. Every model pass so far, including the 861-span cadence fix of 2026-09-09, aimed at that target.
- After that pass GPTZero still read Ch1, 3, 17 and 37 as fully AI; Chris's own Crystal City passage read as human; a loosened spoken-register model rewrite still read as AI. Only Chris's dictated Chapter 1 moved it (`docs/ai-cadence-fixes-2026-09-09.md`).
- Nothing has changed in the repo since 2026-09-10.

## Step zero

1. Replace the voice sections of `CLAUDE.md` and `docs/02-voice-and-style-profile.md` with the Register 6 rules: full conversational sentences joined with commas and "and", ideas unpacked not compressed, terms glossed in the sentence that uses them, "we" from inside the communities, under-claimed credentials, parentheses for caveats, short lines only as instructions or lists, plain subheads, end on the last point. No mic-drop closers, no fragment stacks, no "not X but Y".
2. Settle the open calls listed at the end before drafting briefs.

## Part One, Built for Wonder

| Ch | Title | Words | Verdict | What changes |
|---|---|---|---|---|
| Front | Definitions, legend, Note on Sources, Acknowledgments | 1,224 | KEEP | Bio fixes (below). Legend re-cut once the tier scheme is settled. The "Much of the material here was inspired by Chase Hughes" line should be reconsidered once Part Two is rebuilt on Navarro. PROILLUSIONS paragraph still pending Chris's call. |
| 1 | The Method Is Not the Point | 2,263 | DONE | Dictated by Chris 2026-09-10. Leave it. |
| 2 | On Being the Person Who Admits What They Do | 1,130 | KEEP | Crystal City read stays whole. Add one sentence that the read is a bet about habits, not proof of character (the trainer handbook bars character claims). "Four reasons" vs Ch4's five forces. |
| 3 | Designing for Reality | 1,713 | REWRITE | Fold Ch6 in as an anticipation section; cognitive economy and metabolic efficiency said twice. GPTZero 100% after the pass. |
| 4 | The Five Forces of Attention | 1,205 | REWRITE | Cut the invented AGT watch-time statistic and the hypothalamus line; "eleven million bits" uncited; Zeigarnik duplicates Ch3. |
| 5 | Tension, Threat and the Window of Wonder | 2,387 | KEEP | "Cortisol discharge event" becomes stress release (a laugh is a pacifier in Navarro's terms); "Always trust the body" absolute softened; neck pacifiers credited to Navarro; the suits line is invented. |
| 6 | The Art of Anticipation | 808 | MERGE into 3 | Keep the Schultz paragraph and the backward-mapping exercise; drop the dopamine-equals-compliance leap. |
| 7 | Attention as a Weapon | 1,243 | KEEP | Cleanest explainer in Part One. Source or drop the "Octopus Principle" name. |

## Part Two, Reading the Room (rebuilt on the Navarro frame)

The frame: comfort and discomfort, not truth and lies; pacifiers as stress markers; baseline through rapport, then watch for change timestamped to a stimulus; clusters across the Four Domains (comfort, emphasis, synchrony, perception management); feet, hands, face in that order of honesty; eye blocking and the negative rule; the 54 percent ceiling stated once. Chris's own additions since the book: the honest-behavior principle (the audience runs the four domains on the performer) and rapport before the propless read (memory `mentalism.md`).

**Terminology (Chris, 2026-10-25): the book says "subcortical", never "limbic system".** The manuscript has 36 occurrences across 11 chapters (20 in 7A, 5 in REFLEX, two each in 37 and 41, one each in 5, 7, 14, 19, 22, 35, 42) plus two in build-book.py hook or key-read lines. Navarro's wording stays only inside a direct quote of him.

| Ch | Title | Words | Verdict | What changes |
|---|---|---|---|---|
| 7A | The Limbic System | 2,495 | REWRITE, retitle | Becomes the subcortical chapter: new title, every "limbic" replaced. The big brother and little brother image maps cleanly onto subcortical and cortical, so it stays, with the dog. One sentence that the two-system picture is a teaching simplification (the Academy footnotes the triune brain as outdated). Cut the mic-drop closers. |
| 8 | Reading Body Language in Real Time | 3,465 | REBUILD | Keep: baseline first, the cigarette story, the Five Cs, the three-signal rule, self-touch as stress not deception, cultural calibration, "Observation Is Not Lie Detection". Recast the whole chapter around comfort and discomfort. Cut Chris's Take on eye direction ("lateral means processing, downward means emotional access"). Decide the fate of the T1 to T4 scheme (see open calls). |
| 9 | The 80-Signal System | 2,748 | REBUILD | The table is his profiling tool and stays, but roughly sixty signals carry a "research-backed" label with no citation. Either source each T2 or rename the scale (physical evidence, published, field, disputed). Cut the T4 appendix walk-backs ("I find it useful and I teach it", smooth eyelids as an agreeable baseline) and the physiognomy items entirely. Soften "almost certainly security, military or law enforcement". The sailor paragraph is repeated from the Note on Sources. |
| 10 | The Four Personalities | 915 | MERGE into 11 | DISC is a self-report model; reading it from gait and lean has no validation. Keep as a performer's heuristic, said plainly. |
| 11 | The Volunteer's Brain | 3,241 | REBUILD | Keep the seven volunteer types and the three recoveries. Drop DISC typing from posture, the crossed-arms tell (Ch8 debunks it), the six-region neural circuit, "resistance is gone by the fourth yes" as fact. Anchoring and the three-yes ladder stay as stage heuristics. |
| 12 | Chris Michael's Tell Table | 345 | KEEP | Re-key the green, yellow, red rows to comfort and discomfort. |
| 13 | The Eyes, the Face, and the Way Thought Leaks Out | 5,457 | REBUILD (partial) | Keep: Fruit to Fang, lip compression, the eyebrow flash, pupil cautions, social referencing, the eye-contact myth reversal, "shift detector not lie compass". Cut every directional sentence ("imagining pulls the eyes up, emotion pulls them down", "up-left, up-right"). Navarro assigns no meaning to direction: gaze aversion is a thinking aid and a comfort display, downward gaze is culturally mandated. Cut the duplicate social-referencing paragraph. |
| 14 | The Micro-Expression Matrix | 2,942 | REBUILD | Keep the five uses, the three zones and three moments, the performer's rule, re-enacting the face. Cut the Ekman course plug and "most practitioner training is built on this work". Cut chirality ("the left side of the face is the honest side"), which is Chase Hughes and not supported as honesty. Soften "the eye muscle does not respond to voluntary instruction". State the Vrij ceiling (micro-expressions in 2 percent of clips, half from truth tellers). Reconcile half a second vs a fifth of a second. Replace the third-party seven-expressions composite. |

## Part Three, The Methods

| Ch | Title | Words | Verdict | What changes |
|---|---|---|---|---|
| 15 | Closing the Barn Door | 6,421 | KEEP | Cut the two "start with the skeptic" duplicates and the jump-scare retelling; move "Character determines method" to Ch30 or 37. Permissions on file for Anthem's Facebook post and Kevin Hamdan's section. |
| 16 | Memory Distortion | 6,100 | REWRITE | A memory-science primer with almost no first person. Cut about 40 percent (the eight mechanisms are restated twice); add which show, which effect. Keep the ethics preface and the refusal to discuss sleep deprivation, propranolol, V2K. Name Wiseman and Greening 2005 if the key-bending study stays. |
| 17 | Cold Reading, Warm Reading, and Thin Slicing | 6,245 | REBUILD | Keep collocation (his counterintelligence training), Anthem and Aria, the cold, warm, hot frame. Drop VAK pacing and its eye-direction table (contradicts Ch8, 9 and 13; NLP, no support in Vrij). Re-key the 90-line toolkit away from DISC-from-one-cue ("arms crossed, S, trust does not come easily to you") to comfort and context, or present the lines openly as stock material. Thin slicing and Forer each defined twice. |
| 18 | Contact Mind Reading | 3,684 | CUT to a section | Chris does not perform it, and it reads that way: principles gathered from Trevo Sheikh and Satori, no routine, no script, no handling of a full piece. Thematically it is the purest case of thought organising the body, so keep 600 to 800 words as a section (in 7A or at the top of Part Three) that says exactly that, credits Trevo and Satori, and points readers to the people who teach it. Keep "Intent cues beyond the stage" and "Lipping", which are his lane (pre-incident indicators, Morris's intention movements), and move them into Part Two. Drop "contemporary motor imagery theory", the T1 tag, "why interrogation is so successful". |
| 19 | How Hypnosis Really Works | 4,069 | REWRITE at about 1,500 words | Hypnosis fits the book because Chris performs suggestion-based pieces (PK touch, Witch Hand, pseudo-hypnotic material, pre-show framing). The chapter as written does not: about 2,500 words are a network, cell, neuromodulator, oscillation and pain primer no performer uses, hedged to "likely" and "may" throughout, and it never says what to do. New shape: why people doubt it (the dreams argument), what it is in one paragraph (attention, expectation, absorption; Rainville as the one study), who to pick (absorption, not agreeableness; this also feeds Ch11), what the watch was doing (the car window), and how Chris actually uses it on stage. Delete the cell level, neuromodulators, oscillations, agency, alcohol and the "Alpha Shift" recipe. The Cold War quote is a declassified 1950s CIA memo; say so instead of "through my intelligence work". |
| 20 | The Babel Count | 1,577 | KEEP | Light pass. Confirm "Obsidian" is Fraser Parker's title. |
| 21 | Psychological Forces | 6,187 | KEEP | Both forces (Peter Turner's safeword, Jakob Michaels's Juke Box Oracle) and the tossed-out deck and reputation-maker handling stay. The 13-category reference reads as a model-built card; Chris re-dictates its "how they work" lines. Cut the vmPFC and hippocampus garnish. Add the Bo Burnham mention here if Ch25's cross-reference is to work. |
| 21A | Predictive Text and Algorithmic Forces | 2,400 | KEEP | Original, ahead of the literature (memory `mentalism.md` gap analysis). Re-verify every output against current iOS and ChatGPT the week before print and add a "test it the week of the show" caveat. Soften "no single mentalist has written about this". Credits present (Turner, Jermay, Sueper's Mentyx). |
| 22 | Making Better Propless Mentalism | 5,405 | KEEP | Already mostly his voice. Fix the two seams (the "unique shape or quality" line nothing sets up; the broken transition sentence). Write the Diagnostic questions or cut the promise (marker CH18_DIAGNOSTIC_PANEL). |
| 23 | Propless Systems That Actually Work | 5,032 | KEEP | Fix four seams: "two worked systems" delivers one; backward-design paragraph twice; stranded "Here is how each one works"; two duplicate closers about the performance arc. |
| 24 | REFLEX | 7,710 | KEEP | Resolve the chin tell contradiction (two passages say the chin aims at the empty hand, one says the concealing hand). Cut the fusiform, STS, insula, myelination paragraph; "nearly 100% success rate" becomes "with practice you will rarely miss". Dead QR (item i). ProIllusions line pending. Imbalanced is Brookings material. |
| 25 | Zodiac Divinations | 15,064 | KEEP | Chris's 7,510 words are among the most human in the book; touch only the closers and the DISC line. Rado's Ephemeris (3338 to 3439) and Christopher Parrish's Red Dwarf (3444 to 3471) stay verbatim; one framing sentence in Chris's intro can carry the caveat on Rado's "guaranteed 100%". Fix the dangling Psi Forces and Bo Burnham reference, reconcile the Repeat It Ploy credit (Sadowitz and Farmer vs Sadowitz alone). Cloud Nine is Brookings. |
| 26 | Is Pre-show Worth It? | 1,887 | MERGE into 27 | Colin Cloud's framework stays (confirm he approved the five pull quotes); connective prose in Chris's voice. |
| 27 | Pre-show | 4,309 | KEEP | Best material in the block. The script, the notebook, the Gutenplan sections stay verbatim; re-dictate the line-bank glosses; the "Broca and Exner are real brain regions" gloss softened. |
| 27A | The Pre-show That Looks Like a Failure | 699 | MERGE into 27, or CUT | Brookings material. In if he approves in writing, out if not. |
| 28 | Digital Pre-show | 7,767 | REBUILD | Roughly halve. Keep the Sarah example, the hierarchy, the event-contact section, the greenroom story, the rules. Cut the Google dorking manual to a short illustrative set, drop the obituary and deceased-child search strings and the dead Facebook timeline trick, remove the neuroscience paragraph, say the ethics once. Verify the SOCOM training line against canonical credentials. The deceased mother's first name in the story should be changed. |

## Part Four, Performance Craft (ten chapters become six)

| Ch | Title | Words | Verdict | What changes |
|---|---|---|---|---|
| 29 | The Performance Arc | 1,211 | MERGE with 32 | One checklist for 29, 34 and 35. Fix the "Chapter 2" cross-reference (five forces are Ch4). PERF_ARCH_FRAMEWORK_SVG is an unbuilt placeholder. |
| 30 | Method Invisibility | 1,166 | REWRITE | Half length, one of his own shows as the worked example; the delay principle is stated four times. Define "the Reveal Ladder" or drop it. |
| 31 | Patter, Rhythm, and Silence | 3,935 | KEEP | Strongest in Part Four (the satiation section, the door exercise, the gala). Fix the broken opener ("I want to say that again" refers to a hook that does not exist, item l); supply or cut the Performance Decision Matrix (item k); re-dictate the first half; "Hedge" at Level 2 contradicts Ch41. |
| 32 | When the Room Rises | 1,289 | KEEP | Becomes the single home for Peak-End (now taught in 29, 32, 37 and the Meta Reveal). "Has nothing to do with how moved they are" overstates Mann. |
| 33 | The Art of Strolling | 2,584 | MERGE the halves | The second half reads dictated and is Chris at his best; the first half says the same things in model voice with DISC and T1 dependencies. One chapter in the second half's voice. |
| 34 | Making the Room Say Yes | 2,408 | KEEP core | Creepy, first mover and compliance temperature stay (the creepy section is the consent framing Navarro's module 11 lacks). Checklist into the single list; "people copy what they see" instead of mirror neurons. |
| 35 | The Intro Video | 1,258 | MERGE with 36 | One "before you walk in" chapter. |
| 36 | Introductions, Bios, and Testimonials | 2,282 | MERGE into 35 | Keep the Take about cutting his bio and the "ask what was different by the end" tip. The "strong testimonial" example is constructed; replace with a real quote or label it a model. |
| 37 | What the Room Decides Before You Speak | 3,460 | REBUILD | FATE as Chase Hughes's credited heuristic, not T2 research. Milgram corrected (psychiatrists predicted about 0.1 percent, no label said "lethal", 65 percent to maximum is right). Zimbardo out (discredited). The invented mechanisms (anterior cingulate, amygdala) out. The Likability paragraph: GIB title out, keep only documented clients, under-claim. Peak-End moves to 32. |
| 37A | Controlling the Room | 897 | CUT | Its three real points already live in 40 and 41; carries a duplicate pattern interrupt. |

## Part Five, Authority, Influence and the Deep Framework (five chapters plus intro become four)

| Ch | Title | Words | Verdict | What changes |
|---|---|---|---|---|
| Intro | Before You Begin, A Warning | ~1,000 | CUT the recap, REBUILD the warning | The recap overclaims the earlier parts. The warning keeps the astroturfing and Firehose material with Milgram corrected and no "classified" or HUMINT-as-my-field framing unless Chris can document it. |
| 38 | The Ethics of Influence | 932 | KEEP, move first | Opens Part Five, before the warning and FATE. This is the position the Academy handbook wants him holding. Credit the 100% Plus 1 principle if it has a source. |
| 39 to 41 | How Influence Works, Without Authority, The Authority Frame | 1,802 | MERGE on 41 | 39 and 40 become sections. Credit Kelman for compliance vs internalization or drop the labels. The mirroring test is Navarro's isopraxism and holds. "Every hedge is a compliance signal" contradicts 31 and 37. |
| 42 | Authority Architecture | 3,031 | KEEP, fix attribution | The five pillars and the five-level self-assessment are Chase Hughes's Authority Behavioral Traits and Inventory, structure for structure; the Decode Behavior handout already credits them. Name him, drop the T2 tag and the "what the evidence shows" closer. The gratitude story stays. |

## Back matter

| Unit | Verdict | What changes |
|---|---|---|
| About the Author (both copies) | REBUILD | Out: "Executive Director of the Global Institute of Behavior", "APA-certified continuing education provider". In: the canonical "Certified Body Language Academy by Joe Navarro Trainer" line. Verify before print: the Army Civilian Service decoration, "licensed Center for Body Language instructor", "military operations", "NASDAQ founders", "threat assessment" wording on the DoD certification. "Among the very few practitioners in the world" is the opposite of how Chris describes himself. |
| The Standing Ovation page | CUT | A title and a diamond; the build already drops it. |
| The Meta Reveal (DOCX copy and META_REVEAL_HTML) | REWRITE | Dictated by Chris as a confession. Remove the two fake statistics (colour processed 60,000 times faster than text; readable fonts raise trust 40 percent). Sync list: the Author Note, Ch3 name insertion, Ch21 jukebox, Peak-End's new home, the warning's new framing, "every eight to twelve pages" (one interrupt exists), the "fifteen chapters" count. |
| Back cover | KEEP | One em dash left. |

## What does not fit the book (Chris's question, 2026-10-25)

The book's promise is behavioural science, psychological performance and astonishment, from someone who does the work. Judged against that:

- **Ch18 Contact Mind Reading:** fits the theme, not the author. Cut to a section (above).
- **Ch19 Hypnosis:** the subject fits, the chapter does not. Rewrite short, about how he uses it (above).
- **Part Five intro warning** (astroturfing, Firehose of Falsehood, HUMINT as "my field"): the furthest from performance in the book. A paragraph inside Ethics at most.
- **Ch42 Authority Architecture:** Chase Hughes's leadership self-assessment, the least mentalism in the book. Credit him and keep it to a page inside the merged authority chapter, or cut.
- **Ch28 Digital Pre-show:** the premise fits, the dorking manual does not fit a behavioural strategist who trains investigators. Halve it (above).
- **Ch16 Memory Distortion:** the idea fits (how the effect is remembered), the primer does not. Cut hard and tie to his shows.
- **Ch35 and 36 (intro video, bios):** business craft, not behaviour. Fine merged and short.
- **Ch10 DISC:** does not fit the Navarro frame. Folded into Ch11 as a heuristic.
- Everything else earns its place, and 21A (predictive text and ChatGPT forces), REFLEX, Zodiac, propless 22 and 23, Barn Door and pre-show 27 are the chapters nobody else could have written.

## Cross-cutting lists

**Claims a Navarro-trained reader would challenge, book-wide:** truth language ("the body is telling the truth", "believe the hands", "the limbic system cannot lie"); eye-direction meaning anywhere it survives; VAK; DISC from the body; chirality; the Ekman plug; physiognomy in the T4 appendix; hit rates ("nearly 100%", "guaranteed"); neuro-garnish (vmPFC, fusiform, insula, anterior cingulate, amygdala-vs-prefrontal, mirror neurons, "cortisol discharge"); uncited "research shows" lines (AGT watch time, suits for a century, fonts 40 percent, colour 60,000x, eleven million bits). What stays because it is Navarro's: the honest brain, feet most honest, pacifiers as stress, baseline then change, clusters, the held smile, isopraxism, the eye-contact myth reversal.

**Credential and truth lines to settle:** GIB title (three places plus Meta Reveal); APA; SOCOM training (Ch28); "through my intelligence work" (Ch19 CIA memo); HUMINT as "my specific field" (Part Five intro); the Likability paragraph list (Ch37); Army decoration, Center for Body Language, NASDAQ founders (bio); "That Fooled the Greatest Mentalists" (Ch25 title); "no single mentalist has written about this" (21A).

**Permissions to have in writing:** Atlas Brookings (four registered sections: Three Eras Ch1, Imbalanced Ch24, Cloud Nine Ch25, Pre-show Failure 27A; the no-Brookings edition exists because this was never settled); Colin Cloud (five pull quotes, Ch26); Michael Gutenplan (Ch27); Anthem's Facebook post and Kevin Hamdan (Ch15); Anthem and Aria (Ch17); Trevo, Satori, Peter Turner (Ch18, 21, 21A); Jakob Michaels (Ch21); Adam Brown, Christian Grace, Manuel Luarte, Luis Olmeda story (Ch25); Rado Sheytanov and Christopher Parrish (already thanked, printed in full).

**Academy:** the trainer handbook says to ask the Academy before adapting material and the licence says never to imply endorsement. Paraphrase in Chris's words with credit is within the standing rules; a heads-up to Nadia before print is recommended. Chris's call.

**Build dependencies the rebuild breaks:** Ch17's toolkit navigation ties to the 80-Signal System and DISC; Ch34's checklist uses DISC labels; HOOK_LINES holds the same string for Ch13 and Ch18; the recency-effect pattern interrupt renders twice (37 and 37A); KEY_READS and META_REVEAL_HTML mirror DOCX lines that will change.

## Proposed order of work

0. Step zero above. Chris answers the open calls.
1. Part Two rebuild (7A to 14, about 21,000 words) from per-chapter dictation briefs: what stays verbatim, what is cut, what he says again in his words, what is new and where it comes from, the questions only he can answer. Spike reads Part Two only when it is done.
2. The other rebuilds: 17, 28, 37 with the Part Five warning, About the Author, the Meta Reveal.
3. The rewrites: 3 with 6, 4, 16, 19, 30.
4. The keep chapters: seam fixes, merges (Part Four and Part Five), dictation touch-ups chapter by chapter.
5. Credits, permissions, truth pass; build both editions; Spike's full read.

After the merges the book is about 36 chapters (Ch18 becomes a section). Roughly 58,000 words get written fresh (Part Two plus the rebuilds and rewrites); about 80,000 are touch-ups where Chris's passages stay as they are; the rest is cut.
