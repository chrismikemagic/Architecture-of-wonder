# Built for Wonder — Editorial Audit (2026-07-05)

## Session actions — what was actually changed (2026-07-05)

This session made two kinds of change to the source `Built-for-Wonder.docx`, then rebuilt both editions. Everything below is ground truth from the apply log; it supersedes the auditor's optimistic "applied automatically" table in section 7.

**1. New content (Chris's own idea).** Added a new Chapter 19 section, *"Where the Swinging Watch Comes From,"* after "The Alpha Shift." It explains that rhythmic light flickering across closed eyes (the back-seat car ride, sun through trees, streetlights) echoes the eye activity of REM/hypnagogic drift, and that this is the real mechanism behind the swinging watch — paying off the chapter's own "no swinging watch" setup and its dream section. Written in-voice (no em dashes; uneven contrasts and standalone imperatives only; REM glossed inline). Ships in BOTH editions (no Brookings manifest entry). Verified: renders as an `h3`, 0 lines removed / 8 added, 46 chapter openers intact.

**2. Mechanical fixes: 76 applied, 7 held back.** From the audit's 83 double-verified candidates, 76 pure spelling/spacing/punctuation/homophone corrections were applied run-aware (inline bold/italic preserved). 7 were held back after a character-level review (see below). No prose was rewritten; every applied change is a mechanical correction.

**3. Build fix — 4 orphaned marker tokens no longer leak to readers (output only; DOCX untouched).** The audit flagged `CH18_DIAGNOSTIC_PANEL` / `CH18_IFYRE_PANEL` as possibly rendering garbled. They were: both appeared in the finished HTML as literal `<h3>` headers. A build check confirmed **four** such orphans were leaking as visible headers — `CH18_DIAGNOSTIC_PANEL`, `CH18_IFYRE_PANEL`, `PERF_ARCH_FRAMEWORK_SVG`, and `PERFORMANCE_MATRIX` (the audit caught the first two). `build-book.py` now drops any unresolved `ALL_CAPS_WITH_UNDERSCORES` token that no handler claimed, as a last-resort guard placed after every real handler so registered tokens like `PATTERN_INTERRUPT_40PCT` and `SIX_AREA_RADAR` are unaffected (their content was verified intact). The tokens still exist in the source DOCX — **you decide** whether to delete them or replace them with real panel content; the build simply stops emitting garbage in the meantime. The other flagged placeholders (`FEEDBACK_SIGNALS_TABLE`, `ZODIAC_ELEMENT_TABLE`, and the Ch3 `*PLACE HOLDER*`) were already correctly substituted or stripped by the build and never reached readers.

### Applied (76)

| Chapter | Was | Now |
|---|---|---|
| Ch1 | It is how much fun you can have with the audience in an authentic tru… | It is how much fun you can have with the audience in an authentic, tr… |
| Ch1 | You need to be applying these in the room you’re in.  Jeff Hobson is … | You need to be applying these in the room you’re in. Jeff Hobson is a… |
| Ch2 | You are far to careful for that to be an accident. | You are far too careful for that to be an accident. |
| Ch2 | If you know me personally, than you know I am always observing small … | If you know me personally, then you know I am always observing small … |
| Ch4 | This is why your opening cannot be something they have seen multiple … | This is why your opening cannot be something they have seen multiple … |
| Ch4 | commands more attention than the one who out-performances everyone el… | commands more attention than the one who out-performs everyone else. |
| Ch5 | the upscale Graham Hotel outside of Georgetown university | the upscale Graham Hotel outside of Georgetown University |
| Ch5 | For nearly as century this is part of the subconscious reason we trus… | For nearly a century this is part of the subconscious reason we trust… |
| Ch5 | just noise or someone dealing with unrealted stressors. | just noise or someone dealing with unrelated stressors. |
| Ch5 | This loads more cortisol onto an audiences nervous system that is alr… | This loads more cortisol onto an audience's nervous system that is al… |
| Ch5 | One word of caution that surprisingly comes from my law enforcement t… | One word of caution that surprisingly comes from my law enforcement t… |
| Ch6 | To answer the question I forced you to ask:  Pavlov showed the learne… | To answer the question I forced you to ask: Pavlov showed the learned… |
| Ch7 | its not that the audience is being deceived or physically misdirected | it’s not that the audience is being deceived or physically misdirected |
| Ch7 | When you want to be paid attention to limit stimuli, when you want to… | When you want to be paid attention to, limit stimuli; when you want t… |
| Ch7 | System 1 = fast, intuitive, automatic System 2 = slow, effortful, ana… | System 1 = fast, intuitive, automatic. System 2 = slow, effortful, an… |
| Ch7 | you're about to feel this now. | you’re about to feel this now. |
| Ch9 | Other than a possible indicator of handedness,  do not use it in any … | Other than a possible indicator of handedness, do not use it in any p… |
| Ch14 | who offers an excellent entry level course that I recommend taking | who offers an excellent entry-level course that I recommend taking |
| Ch14 | You can also see kicking motions as a distancing behavior that displa… | You can also see kicking motions as a distancing behavior that displa… |
| Ch14 | theone being suppressed most is usually the most truthful | the one being suppressed most is usually the most truthful |
| Ch16 | “Several times,” “from the beginning,” “the whole time,” “at every st… | “Several times,” “from the beginning,” “the whole time,” “at every st… |
| Ch17 | Clips as short as six seconds still produced predictions that  were a… | Clips as short as six seconds still produced predictions that were ac… |
| Ch18 | arrival that looked nothing like guessing.They do not have a word for… | arrival that looked nothing like guessing. They do not have a word fo… |
| Ch18 | As the spectator holds your body, typically your arm, They subconscio… | As the spectator holds your body, typically your arm, they subconscio… |
| Ch21 | Psychological Forces which is volume 7 in Peter Turner’s Propless Men… | Psychological Forces, which is volume 7 in Peter Turner’s Propless Me… |
| Ch21 | Think of that feeling in deep in your heart. | Think of that feeling deep in your heart. |
| Ch21 | you could have been at the bar fill with your friends that all know a… | you could have been at the bar filled with your friends that all know… |
| Ch21 | pluck the very notes of this song from your head to mind | pluck the very notes of this song from your head to mine |
| Ch21 | Who would want to imagine sadness or hatred deep in their heart. | Who would want to imagine sadness or hatred deep in their heart? |
| Ch21 | Do however, consider the mood of the person you are performing this f… | Do, however, consider the mood of the person you are performing this … |
| Ch21 | even if they do chose love, the outcome with likely be the same anyway | even if they do choose love, the outcome will likely be the same anyw… |
| Ch22 | so many mentalists get drawn to propless mentalism at some point ot a… | so many mentalists get drawn to propless mentalism at some point or a… |
| Ch23 | If they grip me higher on the arm, I know that its going to be either… | If they grip me higher on the arm, I know that it's going to be eithe… |
| Ch23 | to get the first vowel that appears in the show's name and instantly … | to get the first vowel that appears in the show's name and instantly … |
| Ch23 | Just like in the example where I could possibly be between Be Witched… | Just like in the example where I could possibly be between Bewitched … |
| Ch23 | This helps you cover the method afterward, Because it is possible tha… | This helps you cover the method afterward, because it is possible tha… |
| Ch23 | You only need the field small enough that your system can parse throu… | You only need the field small enough that your system can parse throu… |
| Ch23 | The person you're thinking of isn't an ex is it? | The person you're thinking of isn't an ex, is it? |
| Ch23 | A sudden Burst of laughter when asking this question | A sudden burst of laughter when asking this question |
| Ch23 | Think of these as “off-beats” in traditional selight-of-hand routines. | Think of these as “off-beats” in traditional sleight-of-hand routines. |
| Ch23 | Your job isn't to win an guessing contest with infinity. | Your job isn't to win a guessing contest with infinity. |
| Ch23 | by giving existing frameworks, people will ignore that piece of advise | by giving existing frameworks, people will ignore that piece of advice |
| Ch23 | It’s just better than sticking the prepackaged version in the oven an… | It’s just better than sticking the prepackaged version in the oven an… |
| Ch23 | Stability matters more than cleverness, if you have to chose. | Stability matters more than cleverness, if you have to choose. |
| Ch23 | making it difficult to be a reliable part of your repetoire | making it difficult to be a reliable part of your repertoire |
| Ch23 | Next, comes the reveal. | Next comes the reveal. |
| Ch23 | State the reveal clearly and is if you have zero doubts. | State the reveal clearly and as if you have zero doubts. |
| Ch23 | That was D’wight you were seeing. I can bet my house that right now i… | That was Dwight you were seeing. I can bet my house that right now I’… |
| Ch23 | A performer who knows the fallback plam is solid carries the routine … | A performer who knows the fallback plan is solid carries the routine … |
| Ch23 | We are playing with the limbic system of the spectator when creating … | We are playing with the limbic system of the spectator when creating … |
| Ch23 | They're the place where the spectator becomes a true believer, a fan,… | They're the place where the spectator becomes a true believer, a fan,… |
| Ch24 | but it is can be done with absolutely nothing except you and the spec… | but it can be done with absolutely nothing except you and the spectat… |
| Ch24 | Everything here has been developed through live hundreds of live perf… | Everything here has been developed through hundreds of live performan… |
| Ch24 | but you will get unconciously competent overtime requiring very littl… | but you will get unconsciously competent over time, requiring very li… |
| Ch24 | the hands begin to emerge from behind the back and pass their waste —… | the hands begin to emerge from behind the back and pass their waist —… |
| Ch24 | even more likely, a microexpession of contempt. You may also so a dro… | even more likely, a micro-expression of contempt. You may also see a … |
| Ch24 | Yes, it is Ben.If you get stuck on a category that has many possible … | Yes, it is Ben. If you get stuck on a category that has many possible… |
| Ch24 | That means i know for certain it has to be in that hand | That means I know for certain it has to be in that hand |
| Ch24 | Youll now notice your chin pointing towards the concealing hand. | You'll now notice your chin pointing towards the concealing hand. |
| Ch24 | This would be the participants right hand. | This would be the participant's right hand. |
| Ch24 | Either way, It takes between one and three seconds for a long name. | Either way, it takes between one and three seconds for a long name. |
| Ch24 | Most people, when think of a friend from their past will think of som… | Most people, when they think of a friend from their past, will think … |
| Ch24 | That is not a common name for young people in the US t ohave grown up… | That is not a common name for young people in the US to have grown up… |
| Ch24 | think of someone you grew up, someone you’ve lost touch with, but not… | think of someone you grew up with, someone you’ve lost touch with, bu… |
| Ch24 | that was the name ive gotten the last 3 times | that was the name I've gotten the last 3 times |
| Ch24 | The need for”cheats” will diminish as you train your mind | The need for ”cheats” will diminish as you train your mind |
| Ch25 | I will teach you a super easy way remember this. | I will teach you a super easy way to remember this. |
| Ch27 | You saying the word outloud is enough proof that you were thinking of… | You saying the word out loud is enough proof that you were thinking o… |
| Ch28 | The layout of theiri street, their mailbox color, the town they visit… | The layout of their street, their mailbox color, the town they visite… |
| Ch29 | you will find you still likely need need more moments, and longer per… | you will find you still likely need more moments, and longer periods … |
| Ch29 | Dopamine peaks during anticipation not the revelation. | Dopamine peaks during anticipation, not the revelation. |
| Ch29 | System 2 load sufficient to render method invisible \| (The spectator’… | System 2 load sufficient to render method invisible (The spectator’s … |
| Ch29 | Tension arc designed. Peak  moment is identified separately from reve… | Tension arc designed. Peak moment is identified separately from reveal |
| Ch29 | Win given to the audience member provided before any complex task dem… | Win given to the audience member before any complex task demand |
| Ch29 | Thank-you and follow ups designed and ready to send within 24 hours. | Thank-you and follow-ups designed and ready to send within 24 hours. |
| Ch32 | You can control this by having that person be pivotal to the shows la… | You can control this by having that person be pivotal to the show's l… |

### Held back — NOT applied (7) — flagged for your decision

| Chapter | Text | Why held back |
|---|---|---|
| Ch24 | you can almost be certain that the gender will be the same as theirs … | Proposed fix was a truncated rewrite starting with '...', not a real replacement. NOTE: the underlying typo 'friend form their childhood' → 'from' is real; fix it by hand. |
| Ch31 | The words are not the performance. The timing between the words is th… | Would drop the leading 'T' ('The words' → 'he words'). The 'T' is a drop-cap the auditor misread; applying it introduces an error. |
| Ch31 | Silence as a Tool- The Instruction Pause | Introduces an em dash into a section header ('Tool- ' → 'Tool — '); you dislike em dashes. Pick a separator (colon works). |
| Ch31 | Movement and Stillness Stillness for Reveals | Injects a newline; this is an extraction artifact (two headers joined in the plain-text), not a DOCX error. Verify the two headers in Word. |
| Ch33 | Seconds 70–90. Close With Impossibility, Then Leave | Introduces an em dash into a section header ('70–90. Close' → '70–90 — Close'); your call on the separator. |
| Ch41 | Walk in certain. Walk in certain. Speak without seeking approval. | Removes a repeated 'Walk in certain.' — may be intentional anaphora. Your call. |
| Ch21 | Example“F"Focus on one of these words: Ambient, Fracture, Storm, Deri… | Spans runs with mixed formatting; skipped to avoid clobbering inline styling. The 'Example“F"Focus' garble is real — fix by hand. |

---


## Executive summary

The manuscript is substantively finished and its research-forward voice is strong and consistent, but a full-team pass surfaced 512 findings across the 45 chapters that should be cleared before print. The single highest-value opportunity is a cleanup sweep of mechanical errors: roughly 150 typo/mechanical issues were found; 83 were double-verified and **76 were applied this session** (7 held back after review — see "Session actions" at the top of this document, which is the ground-truth record and supersedes section 7's proposed list). The second priority is a set of about a dozen high-severity content problems that damage credibility — a literal `*PLACE HOLDER*` left in Ch3, a self-contradiction where "habit" appears on both the controllable and uncontrollable lists (Ch4), a debunked "60,000x faster" color statistic and other shaky science (Back matter, Ch16 monarch/V2K, Ch37 Milgram figures), and math/logic errors in the worked systems (Ch24 phase mapping, Ch25 "six of the eight"). Third, several build placeholders and extraction artifacts (`FEEDBACK_SIGNALS_TABLE`, `CH18_DIAGNOSTIC_PANEL`, `ZODIAC_ELEMENT_TABLE`, `SIX_AREA_RADAR`, run-together signal lists in Ch11 and the Design Summary) must be verified against the build or they will render garbled. The recurring craft note is voice: the author's flagged AI tells (symmetrical mirror-contrast pairs, deny-rename triads, em-dash density, stray exclamation marks) cluster heavily in Ch8, Ch11, Ch30–32, Ch37, and Ch42. Findings by category: **typo/mechanical ~150, readability & formatting ~136, structure & flow ~73, does-not-fit ~63, tone & voice ~48, material improvement ~42.**

---

## High-priority items

| Chapter | Category | Issue | Suggested action |
|---|---|---|---|
| Ch3 | typo | Literal `*PLACE HOLDER*` in finished prose; the name-in-a-sentence device also cannot work in print | Resolve placeholder; replace with a print-workable direct-address beat |
| Ch4 | does-not-fit | "habit"/"habits" appears in BOTH the controllable and uncontrollable lists; "can not" | Decide which list habit belongs in (likely uncontrollable); fix "cannot" |
| Ch5 | readability | Malformed nested parentheses run across sentences ("goes progressively still (…legs, pulling…)") | Restructure without the nested parenthetical |
| Ch7 | typo | "this is not interesting but it is foundational" — missing word reverses meaning | Insert "just": "not just interesting. It is foundational." |
| Ch9 | does-not-fit | Smooth-Lower-Eyelids entry asserts as valid the exact wrinkle claim the next entry debunks | Rewrite to address eyelid tension; remove the contradicted wrinkle material |
| Ch11 | readability | Supporter signal list lost item separators; parenthesis opens and never closes | Re-split into discrete items; repair parens against DOCX |
| Ch11 | readability | Five more volunteer-type signal lists concatenated ("throughoutVery") | Re-split all seven lists; verify no text truncated at joins |
| Ch13 | does-not-fit | Vowel/unicorn paragraph is a near-verbatim duplicate of "Reading the Reaction" | Consolidate; keep the shoulder-shrug/search-quality detail |
| Ch13 | material | Reveal script only works for A/O (fruit) branch; animal branches get no payoff | Add reveal path for animal branches or label the script as A/O only |
| Ch13 | does-not-fit | Children-glancing example repeated in full in the Eyebrow-Flash section | Replace second instance with a one-line callback |
| Ch13 | readability | "this helps you feel less limited in your method to the audience" does not parse | Rewrite the clause; confirm intended meaning |
| Ch14 | readability | "the smile is consciously constructed, not because they are truly happy" — broken contrast | Complete the contrast clause |
| Ch14 | typo | "theone" (missing space) | "the one" (auto-applied) |
| Ch14 | readability | Convergence Rule callout ends mid-sentence: "…most truthful. This means that" | Complete the sentence or delete the fragment |
| Ch14 | typo | "four variations worth caring about" but the list has five | Change to "five" (or split item 5) — author call |
| Ch15 | typo | "Spidey, Timon Krause, and Taha Mansour have all produced." — no object | Complete the sentence |
| Ch15 | structure | 8-item cold-reading primer sits in the barn-door chapter, pre-empting Ch17 | Move block into Ch17; leave a forward pointer |
| Ch16 | does-not-fit | "monarch programming, V2K" listed as real "more effective methods" | Cut or explicitly mark as unsubstantiated conspiracy lore |
| Ch16 | does-not-fit | Direct-address "Notice your posture" interjection pasted mid-setup | Relocate; it breaks the setup→Derren Brown payoff |
| Ch17 | readability | `FEEDBACK_SIGNALS_TABLE` unresolved placeholder; promised table content absent | Verify build substitutes it or write/remove the content |
| Ch17 | does-not-fit | Ambady glossary says "six-second clips"; later section says thirty-second (published figure) | Align to thirty-second initially, compressed to six |
| Ch17 | structure | Thin Slicing and Forer each fully defined twice (glossary + dedicated sections) | Keep one full treatment each; reduce the other to pointers |
| Ch18 | typo | Missing space: "guessing.They" | "guessing. They" (auto-applied) |
| Ch18 | readability | "perhaps envelopes could also be a freely chosen object" — garbled comma splice | Split into two clean sentences |
| Ch18 | typo | "your arm, They subconsciously" — "They" capitalized mid-sentence | lowercase (auto-applied) |
| Ch21 | readability | "don't stop believing" punctuated as imperative, not song title; titles lowercase/unquoted | Quote and capitalize titles; repunctuate |
| Ch22 | readability | `CH18_DIAGNOSTIC_PANEL` / `CH18_IFYRE_PANEL` placeholder tokens reference CH18 inside Ch22 | Verify build; renumber to CH22 if stale |
| Ch23 | structure | Roadmap promises "two worked systems"; chapter ends after Step 8 with none | Add systems or revise roadmap to point forward |
| Ch23 | readability | Physical Tagging is one ~450-word paragraph mixing example, tip, strategy, pump timing | Break into 4–5 paragraphs; relocate pump-timing sentences |
| Ch24 | structure | Phase-to-question mapping contradicts itself (length vs alphabet across script boxes/summary) | Pick one canonical order; align all references |
| Ch24 | does-not-fit | "Female Long K–Z" worked example lists "Heather" (H is A–J) | Swap for a genuine K–Z name (Vanessa, Teresa) |
| Ch24 | readability | "a name that you likely also know several people in your life that has that name" — collapses | Rewrite |
| Ch24 | typo | "it is can be done" — stray verb | Delete "is" (auto-applied) |
| Ch25 | does-not-fit | "In six of the eight combinations…resolves to a single sign" — math wrong; next line says four | Change to "four of the eight" |
| Ch27 | typo | "you are just decided…instead…you still know remember what it is right" — multiple garbles | Rewrite the script line |
| Ch28 | tone | "BINGO! … WOW! … Great!" — exclamation-heavy, violates no-exclamation voice | Strip exclamations; recast as flat declaratives |
| Ch28 | structure | OSINT not defined until past mid-chapter, after the tactical Sarah walkthrough | Move OSINT definition up front; relocate Sarah example after methodology |
| Ch29 | typo | "There are Seven stages insides of one arc." | "seven stages inside of one arc." (flagged — not auto; overcorrection risk) |
| Ch29 | typo | "need need more moments" — doubled word | Delete duplicate (auto-applied) |
| Ch29 | readability | 50-word run-on closing beat with buried subject | Break into two or three sentences |
| Ch30 | structure | "Delay Principle" callout repeats section opening verbatim; example time shifts 30→15 min | Keep commands once; pick one time figure |
| Ch30 | tone | "Certainty sounds like a system. Perception sounds like a human being…" — mirror pair | Break the symmetry |
| Ch31 | typo | Drop-cap "T" followed by full word "The" → renders "TThe" | Change continuation to "he words are not…" (auto-applied) |
| Ch31 | structure | "After a Recovery" references Graceful Exit/recovery before they're defined (next section) | Move after the Recovery Protocol or add a forward pointer |
| Ch31 | does-not-fit | "a Level 4 reveal" collides with "Level 4 = Graceful Exit" defined 30 lines earlier | Disambiguate ("top-tier reveal" / name the ladder) |
| Ch32 | readability | Parenthesis opens after "stands (" and never closes; runs across sentences | Close the aside cleanly; remove orphan close-paren later |
| Ch32 | readability | "backing track (the lead parts removed) piece plays" — stray "piece" garbles it | Delete "piece"; smooth the sentence |
| Ch34 | readability | "Compliance History Compliance Temperature" — two labels merged onto one line | Split into separate headers |
| Part Five intro | does-not-fit | Milgram figures shaky ("lethal" label, 100% "would kill", 0.04%) and contradict Ch37 | Align both tellings to documented facts (300V/450V, ~1 in 1000) |
| Ch37 | structure | Entire Milgram story told twice, nearly verbatim, a few pages apart | Keep full treatment in Ch37; tease it in the intro |
| Ch37 | does-not-fit | "recency effect" meta aside is misplaced, premature ("final section"), and misdefines recency | Relocate to a true final section; reground as goal-gradient |
| Ch41 | typo | "Walk in certain. Walk in certain." — doubled sentence | Delete one (auto-applied) |
| Ch42 | does-not-fit | Chapter is FIVE pillars but closes on "four forces"/FATE (belongs to another chapter) | Rewrite the close around the five pillars |
| Back matter (Meta Reveal) | structure | Chapter says About the Author is "after this chapter"; it actually appears before | Move About the Author after the Meta Reveal, or fix the sentence |
| Back matter (Meta Reveal) | does-not-fit | "brain processes color sixty thousand times faster than text" — debunked myth | Replace with a defensible pre-attentive-processing claim |
| Back matter (Meta Reveal) | readability | Design Summary: all 17 rows have both columns run together ("Definition pagesFraming") | Verify table renders; restore separators if plain paragraphs |
| Back matter (About the Author) | typo | "decodebehavior.co" — likely missing "m" (brand site is .com) | Verify registered domain; correct if needed |

---

## Does-not-fit flags (author decides, nothing was removed)

**Ch2**
- "I simply told his team what I had noticed…" — narration says the read went to the team, but the scripted read is addressed to the general ("Your watch is set 4 minutes fast, General."). Reader can't tell who was being spoken to.

**Ch3**
- "you open by asking the whole room to silently think of any city…you reveal it" — hundreds of different cities, singular "it"; the other two examples are concrete about the mechanism, this one isn't.
- "The brain is energetically expensive tissue…" — Metabolic Efficiency section substantially duplicates Cognitive Economy (same helps/hurts examples).

**Ch4**
- "What you can not control…habits…What we can control…habit" — habit on both lists (also flagged high).

**Ch5**
- "Although, some people are just realtors. Those people check their phone constantly." — tonal swerve inside a serious diagnostic section; may undercut the phone-as-exit-signal point.

**Ch8**
- "Authority is not claimed. It is perceived — in the first 250 milliseconds." — epigraph is about being perceived; chapter teaches reading spectators (direction reversed); 250 ms figure is shaky vs. the ~100 ms literature.
- "A volunteer who stands closer…is not necessarily an I-type" + "DISC profiles" — DISC never introduced in Ch7/7A/8; unanchored forward reference.
- "Grey elephant in Denmark, if you know it." — insider wink whose logical connection to deferring deception detection is unclear.

**Ch9**
- Smooth-Lower-Eyelids valid-claim contradicts the next entry (also flagged high).
- "that should not be taken to mean they are unreliable" — T4 intro grants blanket permission that individual entries prohibit.
- "NLP eye movement…are documented below" — eight removed T4 signals promised, only four documented.
- "T4 signals…documented in the T4 Appendix" vs. the inline "documented below" — conflicting locations.
- "Dominant lifetime emotional baseline" (row 17, rated T2) restates the wrinkle claim the T4 section debunks.
- "Watch type and condition [T1]…" — ~a dozen radar signals don't appear in the 80-signal table.
- "Bag-contact + wall-seating + exit-scanning…almost certainly…security, military, or law enforcement" — "almost certainly" overclaims; cuts against the book's own Five-C ethos.

**Ch10**
- "Eighty signals. Four tiers. One chain to read them all." — Ch10 epigraph belongs to Ch9's material; Ch10 is DISC.
- "Eighty signals. Five filters. One practice." — closing tagline references Ch9's system and a "Five filters" count that maps to nothing in the chapter.

**Ch11**
- "What happened was a cortisol event…" — cortisol rises over minutes; an instant room-visible shift is an acute adrenaline response.
- "The 80-signal system from Part Two…" — this chapter is itself in Part Two; the system lives in Ch9.
- "the same Five C principle…Context, clusters, and congruence" — invokes Five Cs but names only three.

**Ch13**
- Vowel/unicorn duplicate paragraph and children-glancing duplicate (both flagged high).

**Ch14**
- "The left side of the face is the honest side." — hemispheric-lateralization account is contested; it's also the only major claim with no tier code.
- "Seven expressions. One-fifth of a second." — closer says one-fifth; body defines micro-expressions as "half a second or less."

**Ch16**
- monarch/V2K and misplaced direct-address (both flagged high).
- "You'll also employ some cognitive dissonance…" — mechanism described is commitment/consistency pressure, not dissonance.

**Ch17**
- Ambady figure contradiction (flagged high).
- "Thin slicing, the Forer effect, context dependency, cluster reading — tested, replicated" — cluster reading/context dependency are practitioner heuristics, not replicated constructs.
- "the modality matching system and the VAK pacing framework" — two glossary entries describe the same construct.
- "Eye movement upward during recall" — VAK table asserts NLP eye-accessing cues as fact right after conceding they're unconfirmed.
- "And a psychological force is not about steering someone against their will…" — recap of a topic this chapter never covers.
- "Contempt pivot…eyebrow flash. Head tilts." — cues described are surprise/evaluation, not contempt (contempt = unilateral lip-corner raise).
- "Chase Hughes, a former Navy intelligence officer" — credential may be inaccurate; usually described as a Navy chief in behavior profiling.

**Ch18**
- "This is why interrogation and forensic interviewing is so successful." — unsupported causal leap that thought "leaking" drives interviewing success.

**Ch19**
- "Together they produce a measurable shift in the receiving architecture." — Alpha Shift section states confident mechanistic claims with none of the chapter's usual hedging; shakier science than surrounding material.

**Ch21A**
- "No single mentalist has written about this method before now" — unverifiable absolute priority claim.
- "This reinforces the fact that all the people…have a different paragraph" — everyone typed the same word; it's an impression, not a fact.

**Ch22**
- "I then suggested we broaden it further to anything with a unique shape or quality" — references a third expansion that never appears in the dialogue; "Zoo" also capitalized mid-sentence.
- "Sorry. He is standing beside you…" — continuity slip: setup said "in front of you."

**Ch23**
- "an older sitcom like Frasier" — Frasier (1993–2004) is a 90s show, contradicting the "pre-90s = older" dividing line.
- "The arc does not exist in the show. It exists in what the audience carries out…" — appears twice, before and after the section separator.

**Ch25**
- "In six of the eight combinations…single sign" — math error (flagged high).
- "You can also hear Sagittarius as two syllables in your head." — Sagittarius is not two syllables.
- "The Repeat It Ploy Created by Jerry Sadowitz and Bob Farmer" — later section credits Sadowitz + Derren Brown; attributions don't match.

**Ch28**
- OSINT-late structure (flagged high).
- "almost never requires a clever delivery…This can only be made better by clever and unexpected methods" — mild internal contradiction.

**Ch29**
- "the Neural Performance Model describes the arc" — retroactively renames "the Performance Arc"; a term used nowhere else.

**Ch30**
- "Effective separation is measured in minutes…not in spatial distance" — contradicts two lines earlier ("temporally and spatially separated").

**Ch31**
- "Level 4 reveal" collision (flagged high).
- "better recognition of those words from non-native speakers" — research generally finds reduced affective charge for L2 speakers; overreaches.

**Ch37 / Part Five intro**
- Milgram figures and recency-effect aside (flagged high).
- "Ordinary Stanford students became genuinely cruel within days, with no instruction to be cruel." — contested; 2018 recordings show guards were coached.
- "This study has been replicated hundreds of times. The results are always the same." — full replications ethically barred since the 1970s; Milgram's own variations showed obedience collapsing (which actually supports the thesis).
- "And without that signal, they could not make decisions. Not worse decisions. No decisions." — overstates Damasio; Elliot made (catastrophically bad) decisions.

**Ch37A**
- "Specific frames are believed. Grand claims are evaluated." — "evaluated" implies scrutiny, contradicting the tribal-frame premise.

**Ch42**
- Four-forces/FATE close in a five-pillars chapter (flagged high).

**Back matter (Meta Reveal)**
- 60,000x color myth (flagged high).
- "easier-to-read fonts increase perceived trustworthiness by up to forty percent" — precise figure is uncited (real effect, invented number); Design Summary hard-codes "(+40%)".
- "Edge color gradientProgressive Identity Shift" — Design Summary row for a concept never explained anywhere in the chapter.
- "The soft-touch matte lamination created a tactile first impression." — print-only and digital-only claims both addressed to an unconditional "you"; false for whichever edition the reader holds.
- "That is the mere exposure effect. Familiarity produces trust." — the described mechanism (attributing an insight to a named person) is source credibility, not mere exposure.

---

## Material & structure improvement ideas

**Ch1**
- Repeated book-promise paragraph ("techniques used by the best performers…") near-duplicates one three pages earlier; "most performers never reach" appears three times. Compress one.
- "Train Tracking" is dropped in capitalized with no gloss or forward reference at first appearance — add an appositive or "you'll meet it in Part Two."

**Ch2**
- The four-minutes-fast watch read (the most eyebrow-raising observation) gets no grounding while the shoe deduction gets a full note — add one sentence of tradecraft.

**Ch3**
- Setup promises three brain properties, but the sections don't map (conserve-effort gets two, premature closure gets none) — give "good-enough explanations" its own section.
- Expectation Loading gets three abstract sentences and no example while its pair Earned Completion gets three — add one worked example.

**Ch4**
- Move the amygdala gloss to its first mention (Ch4) rather than Ch6.

**Ch5**
- The blink-rate paragraph runs on to cover bombing/people-leaving/doubling-down; break blink rate into its own indicator beat consistent with the labeled sections below.

**Ch6**
- "The more dopamine you deliver…the more compliant and suggestible" — strong causal claim with no grounding; anchor or soften to "tend to."
- Dopamine used from the opener with no gloss; add one at first substantive use.

**Ch7**
- "The Dunninger ploy is a great example." — named but never described; add a sentence or a pointer.
- Octopus Principle name never explained (the Gorilla Principle earns its name); add a line tying the image to the idea.
- Change Blindness is the only section with no performance application; add two or three sentences of use.

**Ch8**
- Three-signal/triangulation idea stated four times; make the KEY CONCEPT box canonical, trim the rest. Cultural-calibration content also appears three times — let "Cultural Calibration in Practice" carry it.
- Expand NLP, and add a one-line credential for Chase Hughes at first mention.

**Ch9**
- The 10-Second Scan defines five checkpoints but never runs on a real person; add one worked example.

**Ch11**
- "Give the volunteer a win" — the section's most actionable idea has no example; add one in performance language.
- Three-Response Principle presented as fact with no grounding; it's the foot-in-the-door effect (Freedman & Fraser) — cite it to match the book's tier ethos.

**Ch13**
- Reveal only covers A/O branch, and search-timing depends on a "got it" signal that's never scripted (both flagged high/medium).

**Ch15**
- Cold-reading primer relocation to Ch17; identify Anthem at first mention; name at least one of the promised "exceptions"; decide placement of CHARACTER DETERMINES METHOD (currently after the Take, so the chapter ends twice).

**Ch16**
- "the key-bending eyewitness material" referenced as known but never introduced; name the Wiseman & Greening study.

**Ch17**
- Opener pre-uses the Stock Lines payoff ("I notice you"); let it detonate once. Cite Baker fully (Lancaster, 2008). Add an ethics line distinguishing public vs. private materials for the collocation/email passage.

**Ch21**
- "Change it" byplay creates a method hole vs. the preshow clipboard reveal; add one clarifying sentence. "keep"/"wear" don't echo "ring" phonetically — split sound-words vs. function-words.

**Ch21A**
- Add an iOS-version durability caveat for predictive-text seed phrases (biggest way the printed sentence goes stale).

**Ch23**
- MULTIPLE WORD TITLES branch is never developed (holds most of the named shows). Vowel map has holes (Uranus for U; no A fallback) — complete it or restrict to E/I/O.

**Ch28**
- The SOCOM-training credential is buried in an awkward sentence; foreground it.

**Ch29**
- The four Performance Architecture layers are described abstractly; add one concrete failure example. Bridge the "do not explain → reveals easy to understand" logic jump.

**Ch35 / Ch36**
- Add a complete 60–90 second sample intro-video script (Ch35). Reorder Ch36 bio material to problem-then-solution (Why Most Bios Fail first); the four-move bio structure is crammed into one line and never shown — add a before/after example.

**Ch37**
- Close the "wordless signal" loop the epigraph promises. Add a concrete "close with resonance vs. impossibility" example.

**Ch39**
- Gloss "anterior cingulate cortex" and "dopaminergic" at first use per house convention.

**Ch42**
- Bridge Ch41 (signals) and Ch42 (pillars) so Ch42 doesn't read as a re-run; write a genuine opening paragraph (currently repeats the epigraph as its first line).

**Structural repetition to consolidate** (strongest cross-chapter cleanups): Ch4 (attention "not random" stated four ways), Ch19 (DMN-quieting three times; "not X/not Y/it is Z" cadence three times), Ch22 ("three failures" three times), Ch26 ("every pre-show is dual reality" four times), Ch31 (STW defined twice; counting instruction restated), Ch33 (leave-at-the-peak stated five times), Ch37 ("most sales training…one or two forces" three times).

---

## Tone & voice notes

Four flagged AI-tell patterns recur and are worth a dedicated pass (never auto-fixed — all are voice calls):

1. **Symmetrical mirror-contrast pairs** — the densest issue. Examples: "Surprise is a system reset. Earned completion is a system confirmation." (Ch3); "The words are the performance. The body is the truth." (Ch8); "The first gives you the room. The second puts you in a fight…" (Ch4); "Certainty sounds like a system. Perception sounds like a human being…" (Ch30); "Desperation is the opposite of authority. Abundance is its clearest expression." (Ch42). Also heavy in Ch11, Ch12, Ch19, Ch22, Ch32, Ch37, Ch37A, Ch39, and the Meta Reveal. Recommend roughening one side of each pair into an uneven contrast.

2. **Deny-rename constructions** — "The sensation is not surprise — it is recognition." (Ch3); "A testimonial is not peer validation. It is borrowed certainty…" (Ch36); "The FATE model is not a performance technique. It is a perceptual architecture…" (Ch37, which also lands the deny-rename-command triad). Vary so they summarize rather than echo.

3. **Em-dash density** — Ch8 carries at least eight spaced em dashes on facing pages while Ch7/7A run nearly dash-free; also flagged in Ch15, Ch20. Recast most as periods, colons, or commas.

4. **Exclamation marks (house style bans them)** — "It's okay! … Fret not!" (Ch6); "do your research!" (Ch8); "BINGO! … WOW!" (Ch28, worst offender); "right on target!" (Ch21); "Take risks!" (Ch23); "Does this mean, yes!" (Ch22). Recast as declaratives.

Minor voice notes: hedge "and some of the psychology" (Ch2); contractions in narration where the book otherwise spells them out (Ch13, Ch37 "I don't use them myself," "So let's say it"); passive "is felt by the room" (Ch35); "It is also incomplete in a way" hedge (Part Five intro).

---

## Readability & formatting

**Ch1** — Convoluted "remove those to make room" sentence; circular "tools" sentence; ambiguous "the method will perform for a stranger."
**Ch2** — Shoe-resoled run-on; "more so just them assuming my ignorance" garbled; three-`and` run-on (shoe shine); trailing dangling conditional; heading casing mixes ALL-CAPS and Title Case ("WHAT IT FEELS LIKE" vs "What This Book Is").
**Ch3** — "Wonder is what happens…decided to prepare for their imagined scenario" garbled ("their" has no antecedent); double "believe"; missing paragraph breaks in the "in practice" passage.
**Ch4** — Chained "which…which…" hypothalamus run-on (also overstates its role); "Who are the people in the group facing towards." incomplete.
**Ch5** — Malformed parentheses (flagged high); "show ran…many performances that when attempting" run-on; "Fortunately, the way we calibrate does not [transfer]" confusing.
**Ch7** — Aside interrupts the study mid-stream; "available for peripheral monitoring and likely to seek out methods" broken parallelism.
**Ch7A** — "the eyes defocus slightly from their outward focus" redundant.
**Ch8** — Opening 200-word wall of text; "instead…Otherwise" double pivot; tangered "the person whose mention of their name…" run-on; "who is…are you about to get a hit or miss" parallelism break; "For us we can"; bare "Eye movement pattern." list item; Five C's styled four ways ("Five C's"/"Five Cs"/"THE FIVE C's"); `T1Physical Evidence` fused tier codes.
**Ch9** — `T4NLP Eye Movement Direction` fused headings (all four); "I find it useful and I teach it as others will find it useful" garbled; garden-path shoes appositive; stray `SIX_AREA_RADAR` token.
**Ch10** — "Open posture + immediate expressiveness + head tilts frequently" parallelism break.
**Ch11** — Signal-list scrambles (flagged high); anchoring wall of text; header "The Neural Selection Circuit - Do you have a gift?" (spaced hyphen, mixed case); "C/D" vs Ch10's "D/C"; "what walks toward your stage" echo.
**Ch12** — Epigraph lacks the quotation marks the Ch10/Ch11 epigraphs carry.
**Ch13** — "one of the most useful mouth behaviors in the whole book…in the book…in this book" ("book" ×3); header casing switches Title Case → sentence case mid-chapter (continues into Ch14).
**Ch14** — "smile is consciously constructed, not because…" and "This means that" truncation (both flagged high); "micro-expression" vs "microexpression" inconsistency.
**Ch15** — KEY PRINCIPLE label splits an intro from its block quote; orphaned "Closing the Barn Door" line; "correct under conditions that make correctness impossible" paradox (needs "should"); "by the sheer volume that those cars exist" ungrammatical; floating Tamariz paragraph with unclear "he"; "None of it" (singular antecedent); sentence-case "What to take away from Kevin Hamdan" among ALL-CAPS headers; "JUMPSCARE" vs "jump scare."
**Ch16** — "then…; then" run-on; sentence-case "Consolidation" among ALL-CAPS; incomplete "A brief note on the function"; two-clause run-on ("should you want…as I am certain"); eight term-mappings crammed into one paragraph (should be a list/table); mixed-construction authority/compliance sentence; "the word feels like they have locked in" garbled; forces/spectators subject shift; "They exist all together" vague.
**Ch17** — VAK table orphan rows ("Often tilts the head," "Speaks deliberately"); imperative buried in a 20-word parenthetical; collocation definition buried under a 24-word aside; "Your talking stops"; single-word "Observe." header breaks the 01–03 pattern.
**Ch18** — Muscle-reading comma splice (flagged high).
**Ch21** — Fused header "WHY PSYCHOLOGICAL FORCES WORK THE PSYCHOLOGY BEHIND IT"; ~350-word "why it works" paragraph; "if it is they that you are sensing to raise their hand" garbled; five failure sources crammed into one paragraph; `01Dominant Choice` / `Example"…"→` fused; "Earlier if you talked" word order; song-title punctuation garbles (flagged high + medium).
**Ch21A** — Run-on gym-reveal sentence mixing instruction and patter; snap procedure introduced with no setup; "Now you know the secret…" confusing.
**Ch22** — 71-word run-on ("I find a lot of peace…"); "just that it's feasible one exists" broken grammar; transition loses its spine after a long quotation; "Does this mean, yes!" garbled.
**Ch23** — "matrixes Or when" broken definition (also "matrixes"→matrices); "What line gives if you are correct" missing object; "They" with no antecedent.
**Ch24** — Garbled name sentence and reflexmagix clause (flagged high/medium); "On the other hand" idiom collides with the anatomical hand.
**Ch25** — `ZODIAC_ELEMENT_TABLE` placeholder; "Gemini = Wind" inconsistent with "= air."
**Ch27** — Merged header "Performer: Deal? WHAT THOSE LINES ARE REALLY DOING"; inconsistent/unbalanced script quotation marks.
**Ch28** — "Targeted intelligence, which is what this chapter addresses." fragment + near-repeat; "on the year" comma splice; single very long Sarah paragraph.
**Ch29** — 50-word run-on and merged frameworks (flagged high); discursive 02 SIGNAL block; "Chapter Three" vs "Chapter 2" reference style.
**Ch30** — quote-style inconsistency (straight vs curly) across Ch30/31.
**Ch31** — merged headers and dangling pronouns (flagged high/medium); "brain wishing it had saved glycogen" convoluted; "call these two pieces together" awkward; appositive-list "the recognition, a slight forward lean, a micro-nod" hard to parse.
**Ch32** — malformed paren and "piece plays" (flagged high); comma-spliced backing-track sentence; stray all-caps "FORCED."
**Ch33** — "Seconds 70–90." period breaks the em-dash series; overlapping "First Three Seconds" / "Seconds 0–10" windows; "a specific that cannot be explained" missing head noun.
**Ch34** — merged "Compliance History Compliance Temperature" (flagged high).
**Ch35** — numeral style inconsistency ("15 minutes"/"90 seconds" vs spelled-out neighbors).
**Ch37** — "cannot part emotion and action from each other" nonstandard; "You as a mentalist have such a shortcut" reads as translated.
**Ch37A** — Step headers run ordinal into label ("Step One Environmental Compliance") across all nine.
**Ch39** — quote-glyph inconsistency between epigraphs (straight) and body examples (curly).
**Back matter** — Design Summary merged columns (flagged high); About-the-Author appositive list needs a colon; Meta-Reveal appositive separates subject from verb by 20 words; "Those were the Von Restorff effect" predication off.

---

## Mechanical fixes applied automatically

> ⚠️ **This table is the auditor's PROPOSED set and overstates what was applied.** It includes 6 items that were held back after character-level review (e.g. the Ch31 drop-cap "TThe", the Ch31/Ch33 header em dashes, the Ch41 repeated "Walk in certain") and a few that never reached the verified list. The authoritative record of what actually changed is the **"Session actions"** section at the top of this document (76 applied, 7 held back). Treat the rows below as candidates, not confirmations.

| Chapter | Was | Now |
|---|---|---|
| Ch1 | "only YOU  can provide" / "authentic truly unique" | "only YOU can provide" / "authentic, truly unique" |
| Ch1 | "Jeff Hobson is in applying them." (+ double space) | "Jeff Hobson is applying them." |
| Ch2 | "You are far to careful" | "far too careful" |
| Ch2 | "than you know I am always observing" | "then you know" |
| Ch4 | "seen multiple times  before" | "times before" (single space) |
| Ch4 | "who out-performances everyone else" | "out-performs" |
| Ch5 | "Georgetown university" | "Georgetown University" |
| Ch5 | "For nearly as century" | "nearly a century" |
| Ch5 | "unrealted stressors" | "unrelated stressors" |
| Ch5 | "an audiences nervous system" | "an audience's" |
| Ch5 | "law enforcement traingings" | "trainings" |
| Ch6 | "ask:  Pavlov" | "ask: Pavlov" (single space) |
| Ch7 | "its not that the audience is being deceived" | "it's not that" |
| Ch7 | "paid attention to limit stimuli, when you want to distract increase stimuli." | "paid attention to, limit stimuli; when you want to distract, increase stimuli." |
| Ch7 | "automatic System 2 =" | "automatic. System 2 =" |
| Ch7 | "you're about to feel this now." (straight apostrophe) | curly apostrophe |
| Ch9 | "handedness,  do not use it" | "handedness, do not use it" (single space) |
| Ch14 | "excellent entry level course" | "entry-level course" |
| Ch14 | "discomfort.  In a 1977" | "discomfort. In a 1977" (single space) |
| Ch14 | "theone being suppressed" | "the one" |
| Ch16 | "at every stage,” — these phrases" | "at every stage” — these phrases" (dropped comma) |
| Ch17 | "predictions that  were accurate" | "that were accurate" (single space) |
| Ch18 | "guessing.They do not" | "guessing. They" |
| Ch18 | "your arm, They subconsciously" | "they subconsciously" |
| Ch21 | "Psychological Forces which is volume 7" | "Psychological Forces, which is volume 7" |
| Ch21 | "Example“F\"Focus on one of these words…" | "Example“Focus on one of these words…” |
| Ch21 | "that feeling in deep in your heart" | "deep in your heart" |
| Ch21 | "at the bar fill with your friends" | "bar filled" |
| Ch21 | "from your head to mind" | "to mine" |
| Ch21 | "deep in their heart." (rhetorical question) | "…in their heart?" |
| Ch21 | "Do however, consider" | "Do, however, consider" |
| Ch21 | "even if they do chose love, the outcome with likely" | "do choose love, the outcome will likely" |
| Ch22 | "at some point ot another" | "or another" |
| Ch23 | "I know that its going to be either: I love Lucy" | "it's going to be either: I Love Lucy" |
| Ch23 | "get down to one of those instantly instantly" | "get down to one of those" |
| Ch23 | "between Be Witched and Cheers" | "Bewitched" |
| Ch23 | "afterward, Because it is possible" | "afterward, because" |
| Ch23 | "parse through it.I used sitcoms" | "through it. I used" |
| Ch23 | "isn't an ex is it?" | "isn't an ex, is it?" |
| Ch23 | "A sudden Burst of laughter" | "sudden burst" |
| Ch23 | "traditional selight-of-hand routines" | "sleight-of-hand" |
| Ch23 | "win an guessing contest" | "a guessing contest" |
| Ch23 | "ignore that piece of advise" | "advice" |
| Ch23 | "serving that those same friends" | "serving that to those" |
| Ch23 | "if you have to chose" | "choose" |
| Ch23 | "part of your repetoire" | "repertoire" |
| Ch23 | "Next, comes the reveal." | "Next comes the reveal." |
| Ch23 | "clearly and is if you have zero doubts" | "clearly and as if" |
| Ch23 | "That was D'wight… right now i've stepped" | "Dwight… I've stepped" |
| Ch23 | "the fallback plam… differently nad more" | "plan… differently and more" |
| Ch23 | "creating wonder afterall" | "after all" |
| Ch23 | "a fan, and lifelong contact" | "and a lifelong contact" |
| Ch24 | "but it is can be done" | "but it can be done" |
| Ch24 | "through live hundreds of live performances" | "hundreds of live performances" |
| Ch24 | "unconciously competent overtime… the hand that possess" | "unconsciously competent over time… possesses" |
| Ch24 | "pass their waste" | "waist" |
| Ch24 | "a microexpession… You may also so a dropping" | "micro-expression… also see" |
| Ch24 | "Yes, it is Ben.If you get stuck" | "Ben. If you get stuck" |
| Ch24 | "That means i know for certain" | "I know" |
| Ch24 | "Youll now notice" | "You'll" |
| Ch24 | "the participants right hand" | "participant's" |
| Ch24 | "a friend form their childhood" | "from their childhood" |
| Ch24 | "Either way, It takes" | "it takes" |
| Ch24 | "Most people, when think of a friend" | "when they think" |
| Ch24 | "in the US t ohave grown up with" | "to have" |
| Ch24 | "think of someone you grew up, someone" | "you grew up with, someone" |
| Ch24 | "that was the name ive gotten" | "I've gotten" |
| Ch24 | "The need for”cheats”" | "The need for ”cheats”" (added space) |
| Ch25 | "a super easy way remember this" | "way to remember" |
| Ch27 | "You saying the word outloud" | "out loud" |
| Ch28 | "The layout of theiri street" | "their street" |
| Ch29 | "you still likely need need more moments" | "need more moments" |
| Ch29 | "Dopamine peaks during anticipation not the revelation." | "anticipation, not the revelation." |
| Ch29 | "render method invisible \| (The spectator's…" | "render method invisible (The spectator's…" (dropped pipe) |
| Ch29 | "Peak  moment is identified" | "Peak moment" (single space) |
| Ch29 | "Win given to the audience member provided before" | "Win given to the audience member before" |
| Ch29 | "Thank-you and follow ups" | "follow-ups" |
| Ch31 | "TThe words are not the performance." (drop-cap) | "he words are not the performance." |
| Ch31 | "Silence as a Tool- The Instruction Pause" | "Silence as a Tool — The Instruction Pause" |
| Ch31 | "Movement and Stillness Stillness for Reveals" | split onto two heading lines |
| Ch32 | "pivotal to the shows last effect" | "show's last effect" |
| Ch33 | "Seconds 70–90. Close With Impossibility" | "Seconds 70–90 — Close With Impossibility" |
| Ch41 | "Walk in certain. Walk in certain." | "Walk in certain." |

---

## Mechanical issues flagged but NOT auto-applied

These are genuine errors or ambiguous cases the verifier declined to auto-apply (multiple valid rewrites, style/voice judgment, or a change beyond a pure mechanical fix). Eyeball each.

**Ch1** — "it had nothing to do with their methods" (plural subject "two best performances"; "neither had" or "they had"); "the piece that tears the show" (intended verb unclear: steals / tears apart).
**Ch2** — "set 4 minutes fast" (elsewhere "four minutes"; numeral-style, not an error).
**Ch3** — "their bellies stop moving…their chest lifting" (distributive singular — acceptable, but "chests" reads cleaner).
**Ch4** — "those 12 seconds" (elsewhere "twelve"); "The amygdala in our brain." (fragment — but the author uses deliberate fragments here); "Any act…that utilizes 3 or more…are far higher" (agreement fix "is" bundled with a "3"→"three" style change).
**Ch7** — "this is not interesting but it is foundational" (missing "just"; high severity).
**Ch8** — "as long as you can get away with it" (trailing "it" — arguably the author's voice); "between 8 and 20 minutes" (numeral style); "The goal is not to prove whether someone is lying or share their every thought" (wrong verb — likely "read"); "isn't when the shaking happens, rather, when it stops" (needs "but rather").
**Ch11** — "The Anxious and Reserved Volunteer are both S-dominant" (pluralize — but names are proper types); straight single-quote scripts vs curly elsewhere; "not disinterested either" (should be "uninterested"); lowercase "can you think of something private?"; anchoring paragraph breaks (structural, not mechanical).
**Ch12** — "This real table" (stray/leftover "real").
**Ch13** — lone curly apostrophe "individual's" (manuscript here uses straight — but the curly is not itself wrong).
**Ch14** — "four variations" but five follow (content edit; high severity).
**Ch15** — "honing in" (should be "homing in"); "working cold as a wider net" garbled; straight quotes in the Kevin Hamdan lines; "juke box" vs "jukebox"; "Don't Stop Believing" (official title "Don't Stop Believin'", also unquoted); "Spidey…have all produced." truncated (high).
**Ch16** — "Chris Michael's Take:" trailing colon (label-consistency, not a typo).
**Ch17** — "Context is not a background factor, it is the dominant piece" (comma splice — multiple valid repairs); "Anthem and Aria's tips they have genuinely shared" (garbled; "genuinely" likely "generously").
**Ch18** — "interrogation and forensic interviewing is so successful" (agreement — but readable as a single combined practice); "hellstromism" capitalization (eponym; may be intentionally lexicalized).
**Ch21** — "right on target!" exclamation (voice, not error); "It felt that he truly read my mind" (needs "as if"); "Age, background, location, style, of the bar patrons is" (stray comma + agreement — multi-part rewrite).
**Ch21A** — "roll a dice" (should be "a die"; recurs later — informal usage).
**Ch23** — backticks around `fruit to fang` (will render literally — but the proposed fix also restructured the clause); "much more things" (should be "many"); "possible the show to have been" (garbled — multiple repairs); "1950's/2020's" decade apostrophes (contested style); "dificult to correctly perscribe" (spelling fix bundled with a wrong-word substitution — "prescribe" vs "ascribe"?); "Take risks!" exclamation; double space + missing terminal period in "in the spectator's mind  you would…anyway" (real, but the proposed fix added optional commas); "feels I was explaining" (missing "like"/"as if"/"that").
**Ch24** — "you will learn you a minimum of 3 tells" (stray "you"); "it is an amazingly reliable" (dangling article); "Overtime you will…know which name it is likey" ("Over time" + "likely").
**Ch25** — "once more….." five-dot ellipsis (may be an intentional performance pause).
**Ch28** — "turn into into something" (doubled word + missing object "it"); "a powerful story for them to be shared"; "by revealing…respectfully is delivering" (no subject); "effects almost never requires" (agreement); "most the Tier One material" (missing "of" — arguably colloquial voice); "…becomes the differentiator" (compound subject → "become"); "For the sake of all of us performers handle it" (missing comma); "After a few questions…in your mind." (fragment).
**Ch29** — "insides of one arc" + mid-sentence "Seven" (real errors, but the proposed fix over-corrected "inside of"→"inside"); "This is not just reveals, this is the audience" (comma splice — voice-adjacent).
**Ch30** — "Make Them Remember the Impossibility, not what led you there." (heading casing/period — style); "the audience is feeling. You are not analyzing." (wrong pronoun — should be "They"; meaning change).
**Ch32** — "its always stronger when they are not told" (real its/it's error — but the proposed fix rewrote the whole sentence).
**Ch31** — "Most people cannot usually get past 12" (word-order preference).
**Ch35** — "sixty to ninety second intro video" (suspended hyphens — style-guide convention).
**Ch37** — "their excellencies" (honorific capitalization — style); "The FATE model" lowercase vs "FATE Model" (consistency, not a typo type).
**Ch38** — "they are also a human" (number mismatch — drop the article).
**Back matter (About the Author)** — "decodebehavior.co" (likely missing "m"; high — verify domain); "practitioners…who operates" (should be "operate"); "Chris is trained by a founding member" (tense — likely "was trained").
**Back matter (Meta Reveal)** — "The firehose of falsehoods." (RAND term is singular "firehood of falsehood"); "The Juke Box Oracle" label vs body "jukebox" / section title "The Psychological Force" (can't be cross-matched).