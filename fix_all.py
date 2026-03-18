#!/usr/bin/env python3
"""
Apply all remaining quality fixes:
1. Fix TOC chapter numbering (add Tell Table as Ch10, increment all subsequent)
2. Fix duplicate sentence in Ch40
3. Fix typos in Ch2 opener
4. Rewrite Ch2 WYHFB wall of text
5. Add missing WYHFB openers (Ch1, Ch4, Ch6, Ch7, Ch18-26, Ch31, Ch33-35)
6. Update Meta Reveal for HTML accuracy
7. Add Recommended Reading section
8. Add new compelling intro section (What This Book Is + Who It Is For)
"""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('manuscript-extracted.txt', encoding='utf-8') as f:
    content = f.read()

changes = 0

# ═══════════════════════════════════════════════════════════════════════════
# 1. FIX TOC — insert Chapter 10 (Tell Table) and increment all from 10→43
# ═══════════════════════════════════════════════════════════════════════════
OLD_TOC = """Chapter 9  —  The Volunteer's Brain
Seven volunteer types, the cortisol contract, and how to manage neurological state on stage.
Chapter 10  —  The Eyes, the Face, and the Way Thought Leaks Out
Eye movement, facial cues, and the practical difference between useful observation and overclaimed detection.
Chapter 11  —  The Micro-Expression Matrix
The seven universal expressions, the Duchenne marker, the leakage hierarchy, and why clusters matter more than snapshots.
PART THREE  —  The Methods
Cold reading, contact mind reading, hypnosis, and compliance language. The core mentalism techniques, each made more effective by the behavioral foundation in Parts One and Two.
Chapter 12  —  The Science of Hypnosis
What hypnosis actually is at the network and cellular level. Neuromodulators, oscillations, and why suggestion can feel involuntary.
Chapter 13  —  Cold Reading, Warm Reading, and Thin Slicing
The Forer effect, modality pacing, collocation analysis, and the honest account of what each technique is and is not.
Chapter 14  —  Contact Mind Reading
Muscle reading, intent cues, the grip, and how to frame the effect so the method disappears.
Chapter 15  —  The Architecture of Obedience
Pacing and leading, presupposition, yes sets, and the four degrees of certainty for delivering reads.
Chapter 16  —  Closing the Barn Door
Why the brain reduces impossibility to cheap explanations, and the specific language that closes the window before it opens.
PART FOUR  —  Performance Craft
How to build the show: the arc, timing, room management, revelation structure, and the decisions that determine whether skill becomes experience.
Chapter 17  —  The Performance Arc
Seven stages, the neural performance checklist, and the four-layer Performance Architecture Framework.
Chapter 18  —  Turning Observation into Performance
The five structural moves that convert observation into performance: opening read, layered read, soft hit, strong hit, and callback.
Chapter 19  —  Method Invisibility
Temporal separation, anti-backtracking architecture, and why looking directly at what is happening should tell you nothing.
Chapter 20  —  Patter, Rhythm, and Silence
Timing, tempo, the recovery protocol, the performance decision matrix, and why silence is the loudest tool you have.
Chapter 21  —  The Art of Strolling
The 90-second set structure, the delayed discovery method, state architecture, and the exit principle.
Chapter 22  —  When the Room Rises
Standing ovation mechanics, social contagion cascades, duration neglect, and the peak-end rule.
Chapter 23  —  Audio as Architecture
Pre-show, transition, and close-out sound design. What plays when you are not speaking is not logistics.
Chapter 24  —  Making the Room Say Yes
Environmental compliance, room layout, and why the dance floor of death is a design failure.
Chapter 25  —  The Authority Frame
The Five Authority Signals. How authority is broadcast through behavior, pace, and signal consistency before and during performance.
PART FIVE  —  Authority, Influence, and the Deep Framework
The invisible architecture that determines whether a performance has power before the first effect begins. The FATE Model, Authority Architecture, the Signal Dictionary, the Influence Equation, and the DECODE Framework.
Chapter 26  —  What the Room Decides Before You Speak
Focus, Authority, Tribe, Emotion. Four forces the limbic system evaluates before you speak, and how to control all four.
Chapter 27  —  Authority Architecture
The Five Pillars of Authority, the Milgram findings applied to performance, and the self-assessment that tells you which pillars need building.
Chapter 28  —  The Performer's Signal Dictionary
The BTE system, signal clusters (engagement, retreat, evaluation, certainty drop), and the field notation system.
Chapter 29  —  How Influence Actually Works
Novelty plus authority equals influence. Compliance architecture, the critical compliance window, and five speech patterns that build authority.
Chapter 30  —  Insight Demonstrations
Six complete life-reading frameworks built from signal clusters. Travel pattern, life pivot, hidden interest, relationship dynamic, social role, and self-image gap.
Chapter 31  —  Six Steps from Observation to Ovation
The DECODE Framework: six steps from raw observation to installed experience.
PART SIX  —  The Professional Stage
Behavioral science applied to the professional performance context — keynote halls, boardrooms, corporate training, and the ethics of influence.
Chapter 32  —  Mentalism in the Boardroom
Executive audiences, the credibility sequence, and the real power map in any room.
Chapter 33  —  Why Most Training Fails
Experience before explanation. Why most corporate training fails and how the performer advantage changes the equation.
Chapter 34  —  Influence Without Authority
Compliance vs. internalization, the self-attribution principle, and the reflection protocol.
Chapter 35  —  The Ethics of Influence
The consent framework, the distress test, and where the line is drawn in performance, training, and volunteer work.
PART SEVEN  —  The Business Brain
Where bookings are actually won, how authority is built before you walk in the room, and the business of performing at the highest level.
Chapter 36  —  Where Bookings Are Actually Won
The Limbic Ledger: seven items the client's nervous system scores from first email to follow-through.
Chapter 37  —  Building a Career, Not a Calendar
The discovery call, site visits, customization architecture, and post-show follow-through.
Chapter 38  —  The Intro Video
Solving the most unreliable variable in corporate performance.
Chapter 39  —  Introductions, Bios, and Testimonials
Why most bios fail, the four-move bio structure, and what testimonials are actually for.
Chapter 40  —  The Language of Authority
Processing fluency, silence as signal, weak language patterns, and high-authority positioning.
Chapter 41  —  Reading the Booking Room
The discovery call as performance. Baseline-building, buying signals, and why you state the fee and stop.
Chapter 42  —  From First Contact to Follow-Up
Observe, position, match, decode, install. A complete behavioral model from first contact to final follow-up."""

NEW_TOC = """Chapter 9  —  The Volunteer's Brain
Seven volunteer types, the cortisol contract, and how to manage neurological state on stage.
Chapter 10  —  Chris Michael's Tell Table
The in-performance behavioral reading tool. Green, yellow, and red signal clusters for real-time decisions.
Chapter 11  —  The Eyes, the Face, and the Way Thought Leaks Out
Eye movement, facial cues, and the practical difference between useful observation and overclaimed detection.
Chapter 12  —  The Micro-Expression Matrix
The seven universal expressions, the Duchenne marker, the leakage hierarchy, and why clusters matter more than snapshots.
PART THREE  —  The Methods
Cold reading, contact mind reading, hypnosis, and compliance language. The core mentalism techniques, each made more effective by the behavioral foundation in Parts One and Two.
Chapter 13  —  The Science of Hypnosis
What hypnosis actually is at the network and cellular level. Neuromodulators, oscillations, and why suggestion can feel involuntary.
Chapter 14  —  Cold Reading, Warm Reading, and Thin Slicing
The Forer effect, modality pacing, collocation analysis, and the honest account of what each technique is and is not.
Chapter 15  —  Contact Mind Reading
Muscle reading, intent cues, the grip, and how to frame the effect so the method disappears.
Chapter 16  —  The Architecture of Obedience
Pacing and leading, presupposition, yes sets, and the four degrees of certainty for delivering reads.
Chapter 17  —  Closing the Barn Door
Why the brain reduces impossibility to cheap explanations, and the specific language that closes the window before it opens.
PART FOUR  —  Performance Craft
How to build the show: the arc, timing, room management, revelation structure, and the decisions that determine whether skill becomes experience.
Chapter 18  —  The Performance Arc
Seven stages, the neural performance checklist, and the four-layer Performance Architecture Framework.
Chapter 19  —  Turning Observation into Performance
The five structural moves that convert observation into performance: opening read, layered read, soft hit, strong hit, and callback.
Chapter 20  —  Method Invisibility
Temporal separation, anti-backtracking architecture, and why looking directly at what is happening should tell you nothing.
Chapter 21  —  Patter, Rhythm, and Silence
Timing, tempo, the recovery protocol, the performance decision matrix, and why silence is the loudest tool you have.
Chapter 22  —  The Art of Strolling
The 90-second set structure, the delayed discovery method, state architecture, and the exit principle.
Chapter 23  —  When the Room Rises
Standing ovation mechanics, social contagion cascades, duration neglect, and the peak-end rule.
Chapter 24  —  Audio as Architecture
Pre-show, transition, and close-out sound design. What plays when you are not speaking is not logistics.
Chapter 25  —  Making the Room Say Yes
Environmental compliance, room layout, and why the dance floor of death is a design failure.
Chapter 26  —  The Authority Frame
The Five Authority Signals. How authority is broadcast through behavior, pace, and signal consistency before and during performance.
PART FIVE  —  Authority, Influence, and the Deep Framework
The invisible architecture that determines whether a performance has power before the first effect begins. The FATE Model, Authority Architecture, the Signal Dictionary, the Influence Equation, and the DECODE Framework.
Chapter 27  —  What the Room Decides Before You Speak
Focus, Authority, Tribe, Emotion. Four forces the limbic system evaluates before you speak, and how to control all four.
Chapter 28  —  Authority Architecture
The Five Pillars of Authority, the Milgram findings applied to performance, and the self-assessment that tells you which pillars need building.
Chapter 29  —  The Performer's Signal Dictionary
The BTE system, signal clusters (engagement, retreat, evaluation, certainty drop), and the field notation system.
Chapter 30  —  How Influence Actually Works
Novelty plus authority equals influence. Compliance architecture, the critical compliance window, and five speech patterns that build authority.
Chapter 31  —  Insight Demonstrations
Six complete life-reading frameworks built from signal clusters. Travel pattern, life pivot, hidden interest, relationship dynamic, social role, and self-image gap.
Chapter 32  —  Six Steps from Observation to Ovation
The DECODE Framework: six steps from raw observation to installed experience.
PART SIX  —  The Professional Stage
Behavioral science applied to the professional performance context — keynote halls, boardrooms, corporate training, and the ethics of influence.
Chapter 33  —  Mentalism in the Boardroom
Executive audiences, the credibility sequence, and the real power map in any room.
Chapter 34  —  Why Most Training Fails
Experience before explanation. Why most corporate training fails and how the performer advantage changes the equation.
Chapter 35  —  Influence Without Authority
Compliance vs. internalization, the self-attribution principle, and the reflection protocol.
Chapter 36  —  The Ethics of Influence
The consent framework, the distress test, and where the line is drawn in performance, training, and volunteer work.
PART SEVEN  —  The Business Brain
Where bookings are actually won, how authority is built before you walk in the room, and the business of performing at the highest level.
Chapter 37  —  Where Bookings Are Actually Won
The Limbic Ledger: seven items the client's nervous system scores from first email to follow-through.
Chapter 38  —  Building a Career, Not a Calendar
The discovery call, site visits, customization architecture, and post-show follow-through.
Chapter 39  —  The Intro Video
Solving the most unreliable variable in corporate performance.
Chapter 40  —  Introductions, Bios, and Testimonials
Why most bios fail, the four-move bio structure, and what testimonials are actually for.
Chapter 41  —  The Language of Authority
Processing fluency, silence as signal, weak language patterns, and high-authority positioning.
Chapter 42  —  Reading the Booking Room
The discovery call as performance. Baseline-building, buying signals, and why you state the fee and stop.
Chapter 43  —  From First Contact to Follow-Up
Observe, position, match, decode, install. A complete behavioral model from first contact to final follow-up."""

if OLD_TOC in content:
    content = content.replace(OLD_TOC, NEW_TOC, 1)
    print("TOC updated — Chapter 10 (Tell Table) added, Chapters 10-42 renumbered to 11-43.")
    changes += 1
else:
    print("TOC ANCHOR NOT FOUND — check for formatting differences")

# ═══════════════════════════════════════════════════════════════════════════
# 2. FIX DUPLICATE SENTENCE in Ch40 intro
# ═══════════════════════════════════════════════════════════════════════════
OLD_DUP = ("Introductions change the state of the room before the performer begins. A weak introduction makes you climb uphill. "
           "A strong introduction creates borrowed certainty. A great introduction does something better still: it changes the "
           "audience's posture toward the experience before the first line is spoken. A strong introduction creates borrowed "
           "certainty. A great introduction does something better still: it changes the audience's posture toward the experience "
           "before the first line is spoken.")
NEW_DUP = ("Introductions change the state of the room before the performer begins. A weak introduction makes you climb uphill. "
           "A strong introduction creates borrowed certainty. A great introduction does something better still: it changes the "
           "audience's posture toward the experience before the first line is spoken.")
if OLD_DUP in content:
    content = content.replace(OLD_DUP, NEW_DUP, 1)
    print("Duplicate sentence in Ch40 fixed.")
    changes += 1
else:
    print("Ch40 duplicate ANCHOR NOT FOUND")

# ═══════════════════════════════════════════════════════════════════════════
# 3. FIX TYPOS in Ch2 opener
# ═══════════════════════════════════════════════════════════════════════════
content = content.replace("Its' an uncomfortable truth.", "It's an uncomfortable truth.", 1)
content = content.replace("Human attention and behavior show lawful , patterns.", "Human attention and behavior show lawful patterns.", 1)
print("Ch2 typos fixed (Its' → It's, stray comma removed).")
changes += 1

# ═══════════════════════════════════════════════════════════════════════════
# 4. REWRITE Ch2 WYHFB wall of text — break into readable paragraphs
# ═══════════════════════════════════════════════════════════════════════════
OLD_CH2_WYHFB = """What You Have Felt Before
Something powerful, and rarely taught outside of covert operations is this: the moments that command human attention are not random. They follow patterns. Human behavior is constrained, and salience is not arbitrary. It's an uncomfortable truth. Human attention and behavior show lawful patterns. Human behavior may feel unpredictable, but it is not random. Let me have you read that again. Just as no triangle exists with a total sum of its angles exceeding 180 degrees, no human can be random. Human attention is structured, constrained, and responsive to causes. Attention, memory, emotion, context, incentives, habit, fatigue, social pressure, past experience, and biology, all shape what stimulates people, how they interpret those stimuli, and how they respond. What you can not control (in most cases) are habits, past experiences, and biology. What we can control as performers are attention, memory, emotion, context, incentives, habit, fatigue, and social pressure. We will discuss ethical ways to control those later in the book, but for now we will focus on attention.    The brain has a built-in priority system for deciding what deserves your attention first. Two important parts of that system are the anterior insula and the dorsal anterior cingulate cortex. You do not need to memorize those names. What matters is what they do. Together, they help form what is known as the salience network: the system that scans everything coming in and asks, What matters here? What is different? What might require attention right now? Out of the roughly eleven million bits of sensory information your nervous system is taking in each second, only a tiny fraction reaches conscious awareness. Even less will make it to the hypothalamus which controls the endocrine system which controls what we feel. The salience network helps decide what makes the cut. To a performer, that matters."""

NEW_CH2_WYHFB = """What You Have Felt Before
The room is noise and motion and glasses clinking and nobody particularly interesting. Then your eyes move — not because you decided to look, but because something recalculated. Across the room, one person has gone still. Shoulders settled, chin level, not scanning for confirmation. In the middle of all that movement they appear as though they already belong here in a way the room has not caught up to yet. You are looking twice. So is everyone else.

That was not an accident. It was physics.

The moments that command human attention are not random — they follow lawful patterns. Human behavior is constrained. Salience is not arbitrary. Just as no triangle can have angles totaling more than 180 degrees, no human can be truly random. Attention, memory, emotion, context, habit, social pressure — all of it shapes what stimulates people and how they respond. The performer who understands that is not guessing at attention. They are engineering it.

The brain has a built-in priority system for deciding what deserves your attention. The anterior insula and the dorsal anterior cingulate cortex work together to form the salience network: the system that scans everything coming in and asks what matters right now. Out of the roughly eleven million bits of sensory information your nervous system processes each second, only a tiny fraction reaches conscious awareness. The salience network decides what makes the cut.

Five forces reliably activate this system."""

if OLD_CH2_WYHFB in content:
    content = content.replace(OLD_CH2_WYHFB, NEW_CH2_WYHFB, 1)
    print("Ch2 WYHFB rewritten — wall of text broken into paragraphs.")
    changes += 1
else:
    print("Ch2 WYHFB ANCHOR NOT FOUND — check for typo fixes altering the string")
    idx = content.find("Something powerful, and rarely taught outside of covert operations")
    if idx >= 0:
        print(f"  Partial found at char {idx}")

# ═══════════════════════════════════════════════════════════════════════════
# 5. ADD MISSING WYHFB OPENERS
# ═══════════════════════════════════════════════════════════════════════════

# Ch1 — Designing for Reality
CH1_WYHFB = """What You Have Felt Before
You have been in a room where nothing was technically wrong and something was deeply off. The performer was skilled. The material was solid. But the experience never lifted. You watched the whole thing from the outside, engaged but not moved, impressed but not transported. And afterward, when someone asked how it was, you said "it was good" and meant something much smaller than that.

You have also been in a room where the opposite happened. And you remember it. Not the methods — those have mostly dissolved. You remember how it felt to be in the room while it was happening. Wonder is not what you see. It is what the brain does when the world briefly violates its own rules, and the body catches the impossibility before the mind can explain it away.

That state is not accidental. It is designed. This book is about the design.

"""
if "CHAPTER 1\nDesigning for Reality" in content:
    content = content.replace(
        "CHAPTER 1\nDesigning for Reality\nCognitive economy, metabolic efficiency, and predictive processing. The three properties of the brain that make wonder possible.\n────────────────────────────────────────────────────────────────────────────────\n",
        "CHAPTER 1\nDesigning for Reality\nCognitive economy, metabolic efficiency, and predictive processing. The three properties of the brain that make wonder possible.\n────────────────────────────────────────────────────────────────────────────────\n" + CH1_WYHFB,
        1
    )
    print("Ch1 WYHFB added.")
    changes += 1
else:
    print("Ch1 ANCHOR NOT FOUND")

# Ch6 — Reading Body Language in Real Time
CH6_WYHFB = """What You Have Felt Before
You watched someone walk into a room and you already knew something. Not from anything they said. Not from any single thing you could point to. Something in the combination — the pace, the way they paused at the threshold, the direction their weight shifted before they spoke — assembled itself into a conclusion before you had language for it. It was not a guess. It felt like a fact. That instinct is real. This chapter is the methodology behind it.

"""
CH6_ANCHOR = "CHAPTER 6\nReading Body Language in Real Time\n"
if CH6_ANCHOR in content:
    idx = content.find(CH6_ANCHOR)
    # Find the dashes line after the chapter header
    dash_end = content.find('\n', content.find('────', idx)) + 1
    content = content[:dash_end] + CH6_WYHFB + content[dash_end:]
    print("Ch6 WYHFB added.")
    changes += 1
else:
    print("Ch6 ANCHOR NOT FOUND")

# Ch7 — The 80-Signal System
CH7_WYHFB = """What You Have Felt Before
You shook someone's hand and formed an opinion before they said a word. You watched a group and identified who the real leader was before anyone spoke at a meeting. You entered a room and felt within seconds whether the energy was relaxed or tight. None of that was mysticism. It was T1-level signal reading — shoe wear, grip pressure, postural orientation, gaze direction — processed and synthesized below the level of conscious analysis. You were already doing this. This chapter gives you the vocabulary to do it on purpose.

"""
CH7_ANCHOR = "CHAPTER 7\nThe 80-Signal System\n"
if CH7_ANCHOR in content:
    idx = content.find(CH7_ANCHOR)
    dash_end = content.find('\n', content.find('────', idx)) + 1
    content = content[:dash_end] + CH7_WYHFB + content[dash_end:]
    print("Ch7 WYHFB added.")
    changes += 1
else:
    print("Ch7 ANCHOR NOT FOUND")

# Ch4 — The Art of Anticipation (check if it starts right before Ch5)
CH4_WYHFB = """What You Have Felt Before
Something is about to happen. You do not know what. The performer has set a condition, named a possibility, and now you are waiting — not passively but actively, leaning slightly forward, the breath held just a fraction shallower than before. That feeling is not suspense in the colloquial sense. It is dopamine. The anticipatory circuit firing before the outcome arrives. The feeling is the reward. The reveal is just the resolution.

"""
CH4_ANCHOR = "CHAPTER 4\nThe Art of Anticipation\n"
if CH4_ANCHOR in content:
    idx = content.find(CH4_ANCHOR)
    dash_end = content.find('\n', content.find('────', idx)) + 1
    content = content[:dash_end] + CH4_WYHFB + content[dash_end:]
    print("Ch4 WYHFB added.")
    changes += 1
else:
    print("Ch4 ANCHOR NOT FOUND")

# Ch18 — Turning Observation into Performance
CH18_WYHFB = """What You Have Felt Before
You had the read. The signal was clear, the conclusion was real, and you knew you were right. And then you did not know what to do with it. The observation sat in your hands like a tool with no obvious place to apply it. The gap between noticing and delivering is the gap between behavioral knowledge and performance. This chapter closes it.

"""
CH18_ANCHOR = "CHAPTER 18\nTurning Observation into Performance\n"
if CH18_ANCHOR in content:
    idx = content.find(CH18_ANCHOR)
    dash_end = content.find('\n', content.find('────', idx)) + 1
    content = content[:dash_end] + CH18_WYHFB + content[dash_end:]
    print("Ch18 WYHFB added.")
    changes += 1
else:
    print("Ch18 ANCHOR NOT FOUND")

# Ch19 — Method Invisibility
CH19_WYHFB = """What You Have Felt Before
You watched something happen, replayed it immediately, and could not locate the seam. Not because it was fast. Not because you weren't paying attention. Because the structure of what you were watching had been built specifically so that looking directly at it would tell you nothing. The method was not hidden. It was invisible because the architecture around it had made it structurally undetectable. That is not a trick. That is engineering.

"""
CH19_ANCHOR = "CHAPTER 19\nMethod Invisibility\n"
if CH19_ANCHOR in content:
    idx = content.find(CH19_ANCHOR)
    dash_end = content.find('\n', content.find('────', idx)) + 1
    content = content[:dash_end] + CH19_WYHFB + content[dash_end:]
    print("Ch19 WYHFB added.")
    changes += 1
else:
    print("Ch19 ANCHOR NOT FOUND")

# Ch20 — Patter, Rhythm, and Silence
CH20_WYHFB = """What You Have Felt Before
The performer said something and it landed in the room with a weight that surprised you. The sentence itself was not extraordinary. But the silence before it was exactly right. The pause after it was exactly long enough. You felt the moment arrive before you understood why. Timing is not decoration. It is the primary delivery mechanism. The same sentence, differently timed, is a different sentence.

"""
CH20_ANCHOR = "CHAPTER 20\nPatter, Rhythm, and Silence\n"
if CH20_ANCHOR in content:
    idx = content.find(CH20_ANCHOR)
    dash_end = content.find('\n', content.find('────', idx)) + 1
    content = content[:dash_end] + CH20_WYHFB + content[dash_end:]
    print("Ch20 WYHFB added.")
    changes += 1
else:
    print("Ch20 ANCHOR NOT FOUND")

# Ch21 — The Art of Strolling
CH21_WYHFB = """What You Have Felt Before
Someone approached your table at a dinner and within thirty seconds you forgot there had been a dinner. The room collapsed down to the four feet of space between you. Nobody had agreed to this. The conversation you were mid-sentence in dissolved. The performer did not ask for your attention. They simply arrived in a way that made attention the only available response. That is not charisma. That is the engineering of proximity, pacing, and first contact — all of which can be learned.

"""
CH21_ANCHOR = "CHAPTER 21\nThe Art of Strolling\n"
if CH21_ANCHOR in content:
    idx = content.find(CH21_ANCHOR)
    dash_end = content.find('\n', content.find('────', idx)) + 1
    content = content[:dash_end] + CH21_WYHFB + content[dash_end:]
    print("Ch21 WYHFB added.")
    changes += 1
else:
    print("Ch21 ANCHOR NOT FOUND")

# Ch22 — When the Room Rises
CH22_WYHFB = """What You Have Felt Before
The applause started before anyone decided to stand. One person began to rise and the rest of the room followed in a wave that you were part of before you chose to be. It felt unanimous, spontaneous, unanimous because it was spontaneous. It was not. It was a cascade event — initiated at a specific moment, with a specific person, under specific conditions. The standing ovation is not the audience's decision. It is the performer's design. This chapter is that design.

"""
CH22_ANCHOR = "CHAPTER 22\nWhen the Room Rises\n"
if CH22_ANCHOR in content:
    idx = content.find(CH22_ANCHOR)
    dash_end = content.find('\n', content.find('────', idx)) + 1
    content = content[:dash_end] + CH22_WYHFB + content[dash_end:]
    print("Ch22 WYHFB added.")
    changes += 1
else:
    print("Ch22 ANCHOR NOT FOUND")

# Ch23 — Audio as Architecture
CH23_WYHFB = """What You Have Felt Before
You walked into a room before a show and something was already happening. Not the performance — the music. And the music was setting something in you that you did not consciously agree to. By the time the show started your body was already at a specific level of alertness, openness, and readiness that the performer designed four hours before you arrived. Sound is not atmosphere. It is instruction.

"""
CH23_ANCHOR = "CHAPTER 23\nAudio as Architecture\n"
if CH23_ANCHOR in content:
    idx = content.find(CH23_ANCHOR)
    dash_end = content.find('\n', content.find('────', idx)) + 1
    content = content[:dash_end] + CH23_WYHFB + content[dash_end:]
    print("Ch23 WYHFB added.")
    changes += 1
else:
    print("Ch23 ANCHOR NOT FOUND")

# Ch24 — Making the Room Say Yes
CH24_WYHFB = """What You Have Felt Before
Someone asked you to do something and you did it without quite deciding to. Not because you were coerced and not because you stopped thinking. Because by the time the request arrived, the conditions around it had already set the direction. The yes was not manufactured in the moment. It was built into the environment ten minutes before the ask. That is compliance architecture. This chapter is how it works.

"""
CH24_ANCHOR = "CHAPTER 24\nMaking the Room Say Yes\n"
if CH24_ANCHOR in content:
    idx = content.find(CH24_ANCHOR)
    dash_end = content.find('\n', content.find('────', idx)) + 1
    content = content[:dash_end] + CH24_WYHFB + content[dash_end:]
    print("Ch24 WYHFB added.")
    changes += 1
else:
    print("Ch24 ANCHOR NOT FOUND")

# Ch25 — The Authority Frame
CH25_WYHFB = """What You Have Felt Before
The performer had not done anything impressive yet and you already believed they were going to. Something about the way they arrived — not arrogance, not energy, but a specific quality of not needing anything from the room — told your nervous system: follow. The authority frame was set before the first effect. This chapter is what set it.

"""
CH25_ANCHOR = "CHAPTER 25\nThe Authority Frame\n"
if CH25_ANCHOR in content:
    idx = content.find(CH25_ANCHOR)
    dash_end = content.find('\n', content.find('────', idx)) + 1
    content = content[:dash_end] + CH25_WYHFB + content[dash_end:]
    print("Ch25 WYHFB added.")
    changes += 1
else:
    print("Ch25 ANCHOR NOT FOUND")

# Ch26 — What the Room Decides Before You Speak
CH26_WYHFB = """What You Have Felt Before
You watched a performer fail and the failure was not about the material. The material was fine. But the room had made a decision before the first line — something about the lighting, the introduction, the way the energy of the preceding hour had left people closed and slightly guarded — and no amount of skill recovered it. The room decided before you spoke. This chapter is about controlling that decision.

"""
CH26_ANCHOR = "CHAPTER 26\nWhat the Room Decides Before You Speak\n"
if CH26_ANCHOR in content:
    idx = content.find(CH26_ANCHOR)
    dash_end = content.find('\n', content.find('────', idx)) + 1
    content = content[:dash_end] + CH26_WYHFB + content[dash_end:]
    print("Ch26 WYHFB added.")
    changes += 1
else:
    print("Ch26 ANCHOR NOT FOUND")

# Ch31 — Insight Demonstrations
CH31_WYHFB = """What You Have Felt Before
A performer looked at someone in the audience and said something specific enough that the audience went quiet. Not the polite quiet of people pretending to be impressed. The uncomfortable quiet of people recalibrating what they thought was possible. Whatever just happened felt less like a trick and more like an invasion — a precise, surgical entry into something private. This chapter gives you six complete frameworks for producing that experience on purpose.

"""
CH31_ANCHOR = "CHAPTER 31\nInsight Demonstrations\n"
if CH31_ANCHOR in content:
    idx = content.find(CH31_ANCHOR)
    dash_end = content.find('\n', content.find('────', idx)) + 1
    content = content[:dash_end] + CH31_WYHFB + content[dash_end:]
    print("Ch31 WYHFB added.")
    changes += 1
else:
    print("Ch31 ANCHOR NOT FOUND")

# Ch32 — Six Steps from Observation to Ovation (DECODE)
CH32_WYHFB = """What You Have Felt Before
The room goes silent. The sentence lands. And the thought that follows is not how did they do that — it is something quieter and more unsettling: they saw me. Not in a general way. In a specific way. They noticed something. They interpreted something. They delivered something. And the entire sequence from observation to delivery was completely invisible. That sequence has a structure. This chapter maps it.

"""
CH32_ANCHOR = "CHAPTER 32\nSix Steps from Observation to Ovation\n"
if CH32_ANCHOR in content:
    idx = content.find(CH32_ANCHOR)
    dash_end = content.find('\n', content.find('────', idx)) + 1
    content = content[:dash_end] + CH32_WYHFB + content[dash_end:]
    print("Ch32 WYHFB added.")
    changes += 1
else:
    print("Ch32 ANCHOR NOT FOUND")

# Ch33 — Mentalism in the Boardroom
CH33_WYHFB = """What You Have Felt Before
You were in a professional environment — a meeting, a presentation, a conference — and you watched someone read the room in real time and adjust everything accordingly. Not the content. The approach. The pace. The way they leaned into one person and gave space to another. The read was invisible to everyone else. It was only visible to you because you were watching for it. The boardroom is a performance stage. The people who know that are not playing by the same rules as the ones who don't.

"""
CH33_ANCHOR = "CHAPTER 33\nMentalism in the Boardroom\n"
if CH33_ANCHOR in content:
    idx = content.find(CH33_ANCHOR)
    dash_end = content.find('\n', content.find('────', idx)) + 1
    content = content[:dash_end] + CH33_WYHFB + content[dash_end:]
    print("Ch33 WYHFB added.")
    changes += 1
else:
    print("Ch33 ANCHOR NOT FOUND")

# Ch34 — Why Most Training Fails
CH34_WYHFB = """What You Have Felt Before
You sat through a training that covered the right material, delivered by someone who clearly knew what they were talking about, and you left able to pass a quiz and unable to do anything differently. Six weeks later you remembered almost none of it. That is not a retention problem. That is a design problem. Experience encodes differently than explanation. The performer who understands that distinction has access to a kind of influence that no slide deck can replicate.

"""
CH34_ANCHOR = "CHAPTER 34\nWhy Most Training Fails\n"
if CH34_ANCHOR in content:
    idx = content.find(CH34_ANCHOR)
    dash_end = content.find('\n', content.find('────', idx)) + 1
    content = content[:dash_end] + CH34_WYHFB + content[dash_end:]
    print("Ch34 WYHFB added.")
    changes += 1
else:
    print("Ch34 ANCHOR NOT FOUND")

# Ch35 — Influence Without Authority
CH35_WYHFB = """What You Have Felt Before
Someone junior in a room ended the argument. Not through force. Not through rank. They said something and the room reorganized around it. The idea landed and was taken up by people with the formal authority to reject it, who instead adopted it as their own. That is the self-attribution principle operating exactly as designed. Influence without authority is not soft power. It is precise social engineering. This chapter is the mechanics.

"""
CH35_ANCHOR = "CHAPTER 35\nInfluence Without Authority\n"
if CH35_ANCHOR in content:
    idx = content.find(CH35_ANCHOR)
    dash_end = content.find('\n', content.find('────', idx)) + 1
    content = content[:dash_end] + CH35_WYHFB + content[dash_end:]
    print("Ch35 WYHFB added.")
    changes += 1
else:
    print("Ch35 ANCHOR NOT FOUND")

# Ch36 — Ethics of Influence
CH36_WYHFB = """What You Have Felt Before
You used a technique and it worked better than you expected and you had a moment — brief, quiet, easy to dismiss — of wondering whether what you just did was entirely right. Not illegal. Not harmful in any clear way. Just slightly past a line you hadn't formally drawn. The tools in this book are powerful enough to warrant an honest chapter about exactly that question. This is that chapter. Read it before you deploy the compliance and influence material in contexts where the power differential differs from a stage.

"""
CH36_ANCHOR = "CHAPTER 36\nThe Ethics of Influence\n"
if CH36_ANCHOR in content:
    idx = content.find(CH36_ANCHOR)
    dash_end = content.find('\n', content.find('────', idx)) + 1
    content = content[:dash_end] + CH36_WYHFB + content[dash_end:]
    print("Ch36 WYHFB added.")
    changes += 1
else:
    print("Ch36 ANCHOR NOT FOUND")

# ═══════════════════════════════════════════════════════════════════════════
# 6. ADD NEW COMPELLING INTRO SECTION (What This Book Is / Who It's For)
# ═══════════════════════════════════════════════════════════════════════════
NEW_INTRO_SECTION = """What You Are About to Learn
This book teaches you to do something most people do not believe is learnable: read people accurately, create compliance without coercion, build authority before you've said a word, and design experiences that the people inside them cannot explain afterward.

It does this by fusing two disciplines that almost never appear in the same room. Behavioral science — the rigorous, research-based study of how human beings actually make decisions, process social information, and respond to environmental cues. And mentalism — the performance art of making the impossible seem inevitable, of knowing what people are thinking before they say it, of producing experiences that bypass analytical defenses and land directly in emotional memory.

Separately, each discipline is powerful. Together, they are something else entirely.

Who This Book Is For
This book was written for performers who want to stop guessing and start reading. For mentalists and close-up workers who are technically skilled but want to understand why their strongest moments work and how to make them repeatable. For keynote speakers and corporate trainers who suspect that the most memorable ten minutes of any event are not the content but the experience — and who want to know how to engineer that experience deliberately.

It is also for the curious non-performer: the negotiator who wants to read a room before the first offer is made. The consultant who wants to understand why some rooms receive information and others reject it. The leader who wants authority that does not require a title.

The behavioral frameworks in this book are drawn from peer-reviewed research, intelligence community training, clinical observational methodology, and field-tested performance practice across thousands of hours in front of rooms that ranged from skeptical to hostile. The performance frameworks come from a career working every format: strolling galas, corporate keynotes, private consultations, military installations, and late-night residencies in speakeasies.

What You Will Leave With
By the end of this book you will be able to profile a person's personality type, risk tolerance, and social orientation in under sixty seconds from purely observable signals. You will understand how to build compliance into the architecture of an event before anyone has said yes to anything. You will know how the brain creates wonder — at the cellular level — and which specific conditions trigger it.

You will have a complete cold-reading methodology that produces reads accurate enough to stop conversations. You will have a contact mind-reading framework grounded in motor imagery neuroscience. You will have a compliance language system with four degrees of certainty and a recovery protocol for every level of miss.

You will understand authority: what broadcasts it, what erodes it, and how to build it from the inside out. You will have the DECODE framework: a six-step system for moving from raw observation to installed experience. You will have annotated performance sequences for strolling, parlor, and corporate keynote work. And you will have the business architecture — the emails, the conversations, the pre-show protocols — that turn a strong show into a long career.

The science is real. The application is immediate.

One more thing: this book will make you harder to fool. Once you understand how attention is managed, compliance is built, and authority is signaled, you will start seeing these mechanisms everywhere — in boardrooms, at dinner tables, in news broadcasts, in conversations you thought were casual. That is not a side effect. It is the point. The safest person in any room is the one who knows how it works.

"""

INTRO_ANCHOR = "What This Book Is\nPart One is the neuroscience of what your audience experiences."
if INTRO_ANCHOR in content:
    content = content.replace(
        INTRO_ANCHOR,
        NEW_INTRO_SECTION + "What This Book Is\nPart One is the neuroscience of what your audience experiences.",
        1
    )
    print("New intro section inserted.")
    changes += 1
else:
    print("Intro ANCHOR NOT FOUND")
    idx = content.find("What This Book Is")
    if idx >= 0:
        print(f"  'What This Book Is' found at char {idx}")

# ═══════════════════════════════════════════════════════════════════════════
# 7. ADD RECOMMENDED READING SECTION (before About the Author)
# ═══════════════════════════════════════════════════════════════════════════
RECOMMENDED_READING = """RECOMMENDED READING

The following books and resources shaped the thinking in this book or represent the best available material for going deeper in specific areas. Organized by subject.

Behavioral Science and Nonverbal Communication
Joe Navarro — What Every BODY is Saying. The standard-bearer for applied nonverbal reading. Navarro spent twenty-five years as an FBI Special Agent and counterintelligence officer. His work is precise, practical, and free of the overclaiming that plagues most body language writing.

Joe Navarro — Louder Than Words and Be Exceptional. Navarro's later books apply behavioral observation to leadership and professional excellence. Both are directly applicable to performers working in corporate contexts.

Paul Ekman — Emotions Revealed. The foundational text on micro-expressions and universal emotion recognition. If you want to go deeper into the facial action coding system, Ekman's website also offers formal certification training.

Chase Hughes — The Ellipsis Manual and The 6 Pillars of Persuasion. Hughes is one of the most rigorous applied behavioral scientists working in the practitioner space. His work on the BTE (Behavioral Table of Elements) is referenced throughout this book. His materials reward close reading.

Greg Hartley and Maryann Karinch — I Can Read You Like a Book. An accessible entry point into interrogation-based behavioral reading with strong practical application.

Scott Rouse — available through his training programs and consulting work. One of the most experienced behavioral analysts in the country, with particular depth in forensic applications.

Mentalism and Performance
Ian Rowland — The Full Facts Book of Cold Reading. The most technically rigorous cold-reading text available. Systematic, honest about what the techniques are and are not, and essential reading before deploying any of the material in Chapter 14.

Peter Turner — available through his published lectures and working notes. Turner's approach to psychological influence and performance language is more sophisticated than almost anything else available in mentalism. Seek out everything.

Fraser Parker — The Dedication (and related materials). Parker's thinking about psychological structure in mentalism is dense but rewarding. His concept of the open read and his approach to layering are highly applicable to the material in Part Three.

Jerome Finley — Nature of Things. Finley works at the intersection of indigenous wisdom, performance, and behavioral depth. His influence on how this book thinks about the experiential quality of a reading was significant.

Anthem Flint — available through APCA and performance lectures. One of the most well-researched working cold readers. His practical framework for building and delivering readings under live conditions is among the best I have encountered.

Neuroscience and Decision-Making
Daniel Kahneman — Thinking, Fast and Slow. The accessible masterwork on dual-process cognition. Understanding System 1 and System 2 thinking is foundational to everything in Parts One, Three, and Five of this book.

Robert Cialdini — Influence: The Psychology of Persuasion. The benchmark text on compliance and social proof. Cialdini's six principles are the research foundation behind much of what Chapter 25 and Chapter 30 address.

David Eagleman — Incognito: The Secret Lives of the Brain. A readable and surprising account of how much of behavior is generated unconsciously. Useful for understanding why behavioral reading works as well as it does.

For the Performer's Inner Game
Timothy Gallwey — The Inner Game of Tennis. Not about tennis. About the architecture of peak performance under pressure. Every chapter on state management in this book was influenced by Gallwey's framework.

"""

READING_ANCHOR = "ABOUT THE AUTHOR\nChris Michael is a behavioral strategist"
if READING_ANCHOR in content:
    content = content.replace(
        READING_ANCHOR,
        RECOMMENDED_READING + "\n" + READING_ANCHOR,
        1
    )
    print("Recommended Reading section added.")
    changes += 1
else:
    print("Recommended Reading ANCHOR NOT FOUND")
    idx = content.find("ABOUT THE AUTHOR")
    if idx >= 0:
        print(f"  ABOUT THE AUTHOR found at char {idx}")

# ═══════════════════════════════════════════════════════════════════════════
# 8. UPDATE META REVEAL FOR HTML — remove print-only features
# ═══════════════════════════════════════════════════════════════════════════
OLD_META_PHYSICAL = """The Cover

You picked up this book and felt it before you read it. The soft-touch matte lamination created a tactile first impression — people react to texture before processing text. Your fingers registered quality before your eyes registered the title.

Then there was the title itself: embossed, raised from the surface, finished in spot UV that caught the light differently than the matte background. If you tilted the book, you may have noticed a hidden line of text on the back cover, visible only at certain angles. If you found it, you already demonstrated the first lesson in this book: the trained eye sees what others miss.

If you didn't find it, go back now. Tilt the cover in the light. It's there.

That is observation. That is what this book is about.

· · ·

The Color Arc

Did you notice that the accents in this book changed temperature as you read? Parts One and Two used cool steel blues — clinical, analytical, cerebral. The colors said: you are learning. By Part Three, golds began appearing alongside the blues. By Parts Four and Five, gold dominated — warm, authoritative, confident. The colors said: you are applying. By Parts Six and Seven, deep golds and ambers took over entirely. The colors said: you have arrived.

You did not notice this consciously. Research confirms that color shifts signal mood transitions and identity changes without conscious awareness. The brain processes color sixty thousand times faster than text. Your emotional arc through this book was primed by the palette before a single argument landed.

That is behavioral priming. Chapter Two taught you how it works. This book applied it to you."""

NEW_META_PHYSICAL = """The Opening

Before you read the first word of Chapter One, a decision had already been made about this book. The cover image. The title. The weight of the word "wonder" against the precision of the word "architecture." The brain ran a rapid predictive simulation — what kind of book is this? What kind of person wrote it? What will reading it say about me? — and generated an anticipatory experience before the first sentence.

That anticipation was not accidental. It was designed.

That is predictive processing. Chapter One taught you how it works. This book applied it to you before you knew the chapter.

· · ·

The Color Architecture

Did you notice that the accents in this book changed character as you read? Parts One and Two used cool steel blues — clinical, analytical, cerebral. The colors said: you are learning. By Part Three, golds began appearing. By Parts Four and Five, gold dominated — warm, authoritative, confident. The colors said: you are applying. By Parts Six and Seven, deep golds and ambers. The colors said: you have arrived.

You may not have noticed this consciously. Research confirms that color temperature shifts signal mood transitions and identity changes below conscious awareness. The brain processes color before it processes text. Your emotional arc through this book was primed by the palette before the arguments landed.

That is behavioral priming. Chapter Two taught you how it works. This book applied it to you."""

OLD_META_PHYSICAL2 = """The Warm Cream Pages

The paper is not white. It is warm cream. Uncoated. Slightly textured under your fingers.

White paper signals mass-market. Cream signals craft. Uncoated stock signals authenticity. You felt this book was different from a mass-market paperback before you compared a single word. The paper told you.

· · ·

The Edge Colors

Look at the book from the side. The fore-edge — the page edges — shifts in color from cool blue-gray at the front to deep warm gold at the back. Seven shades, one per Part. A thumb index that doubles as a progress indicator.

You felt yourself moving through the book not just cognitively but physically. The color gradient on the edge was a progress bar for your transformation.

· · ·"""

NEW_META_PHYSICAL2 = """The Typography

Every font choice in this book was a behavioral decision. Body text in a serif at eleven points on a warm background — chosen because research shows that readable typography increases perceived trustworthiness. You felt this book was credible before you decided it was credible. Processing fluency: the smoother the reading experience, the more the reader trusts the content.

The chapter titles — geometric, widely letterspaced, all-caps — created visual contrast that signaled "announcement" before each chapter. Your brain registered a shift from conversation to declaration before reading a word.

That is processing fluency. The Language of Authority chapter taught you how it works. This book used it on you from the first page.

· · ·"""

if OLD_META_PHYSICAL in content:
    content = content.replace(OLD_META_PHYSICAL, NEW_META_PHYSICAL, 1)
    print("Meta Reveal — physical cover section updated for HTML.")
    changes += 1
else:
    print("Meta Reveal cover ANCHOR NOT FOUND")

if OLD_META_PHYSICAL2 in content:
    content = content.replace(OLD_META_PHYSICAL2, NEW_META_PHYSICAL2, 1)
    print("Meta Reveal — cream/edge section updated for HTML.")
    changes += 1
else:
    print("Meta Reveal cream/edge ANCHOR NOT FOUND")

# ═══════════════════════════════════════════════════════════════════════════
# WRITE AND REPORT
# ═══════════════════════════════════════════════════════════════════════════
with open('manuscript-extracted.txt', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{'='*60}")
print(f"{changes} changes applied.")
print("Run: python build-book.py && python build-gated.py")
