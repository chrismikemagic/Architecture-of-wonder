#!/usr/bin/env python3
"""Add new content sections to manuscript-extracted.txt for v2."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('manuscript-extracted.txt', encoding='utf-8') as f:
    content = f.read()

changes = 0

# ── 1. Ch5: How to Create the Feeling of Novelty ─────────────────────────────
NOVELTY_SECTION = """\nHow to Create the Feeling of Novelty\nNovelty is designed, not accidental. The salience system responds to deviation from expected patterns — which means the sensation that something genuinely new is happening can be engineered into the architecture of a performance. You do not need different content. You need structure that breaks prediction.\nViolate the Format. The Deliberate Withhold. Name the Unnamed. Reframe the Familiar. Unexplained Specificity. Physical Novelty Anchors.\nUse two or three of these in your opening and you have manufactured the novelty state before you have said anything that matters.\n"""

CH5_ANCHOR = 'The participant should feel like they are allowing, not achieving. That is usually where the best responses begin.'
if CH5_ANCHOR in content:
    content = content.replace(CH5_ANCHOR, CH5_ANCHOR + NOVELTY_SECTION, 1)
    print('Ch5 novelty section: ADDED')
    changes += 1
else:
    print('Ch5 novelty section: ANCHOR NOT FOUND')

# ── 2. Ch25: Five Speech Patterns That Build Instant Authority ────────────────
SPEECH_SECTION = """\nFive Speech Patterns That Build Instant Authority\nProcessing fluency research (Reber and Schwarz) established that when information is easy to process, the brain assigns it higher truth value. Slowing down is not a communication preference. It is a persuasion mechanism.\nSlow the Beginning. The Spontaneous Compliment. Future Memory Language. The Status Frame. Strategic Silence.\n"""

CH25_ANCHOR = 'A single gap, one inconsistency between claimed and demonstrated level, creates cognitive dissonance the client will feel but may not name.'
if CH25_ANCHOR in content:
    content = content.replace(CH25_ANCHOR, CH25_ANCHOR + SPEECH_SECTION, 1)
    print('Ch25 speech patterns section: ADDED')
    changes += 1
else:
    print('Ch25 speech patterns section: ANCHOR NOT FOUND')

# ── 3. Ch26: How the Brain Builds Experience Before It Receives It ────────────
PREDICTIVE_SECTION = """\nHow the Brain Builds Experience Before It Receives It\nThe brain does not wait for your show to begin before forming a judgment about it. The anterior insula, the anterior cingulate cortex, and the prefrontal cortex run a continuous predictive simulation: what is this person likely to do, based on every signal received so far. Your stage presence, pace, wardrobe, the quality of the room, the way you arrived — these are not background details. They are the data the brain is using to construct an anticipated version of your performance before the first word leaves your mouth.\nThis is predictive processing: the brain's mechanism for generating expected experience in advance of sensory confirmation. It conserves cognitive resources by predicting what comes next rather than building experience from scratch at each moment. The practical consequence is significant: your audience is already inside a version of your show before you begin. Every FATE variable shapes that simulation. The question is not whether the brain will build an experience in advance. It will. The question is whether the experience it builds is the one you designed.\n"""

CH26_ANCHOR = 'The audience has already made a judgment. This chapter is about controlling what that judgment is.'
if CH26_ANCHOR in content:
    content = content.replace(CH26_ANCHOR, CH26_ANCHOR + PREDICTIVE_SECTION, 1)
    print('Ch26 predictive brain section: ADDED')
    changes += 1
else:
    print('Ch26 predictive brain section: ANCHOR NOT FOUND')

# ── 4. Ch7: DISC signals bridge at end (before · · ·) ────────────────────────
DISC_BRIDGE_SECTION = """\nSignals That Point Toward DISC\nThe 80-Signal System gives you the raw data. DISC gives you the pattern that organizes it into a usable performance adjustment. The signals are not the personality type — they are the behavioral evidence that lets you predict pace, resistance, expressiveness, and compliance before the first instruction is given. Chapter 8 gives you the full DISC framework. The signals below are the fastest path to getting there.\nD-Type Signals to Watch: #43 walking speed vs. crowd, #46 weight distribution at rest, #57 handshake pressure, #58 how quickly they sit, #67 interruption frequency, #71 reaction to contradiction, #80 how quickly they reclaim silence.\nI-Type Signals to Watch: #08 eye contact willingness, #45 head tilt when listening, #50 humor reaction timing, #56 eyebrow expressiveness, #64 whether they mirror pace or tone, #72 speed of smile disappearance, #73 delay before laughter after others laugh.\nS-Type Signals to Watch: #14 fidgeting level in public, #45 head tilt when listening, #49 breathing depth in conversation, #52 conversational distance preference, #66 speed of agreeing to small requests, #74 whether they ask permission before moving, #75 how they handle mistakes publicly.\nC-Type Signals to Watch: #35 privacy screen on device, #42 notification response speed, #53 face touching during thinking, #59 whether they move objects before sitting, #65 response lag before answering personal questions, #76 whether they explain simple choices unprompted, #79 object straightening and alignment behavior.\n"""

# Anchor: end of Ch7 body — use the Key Read / final sentence before · · ·
# The last unique sentence before the Ch7 separator
CH7_ANCHOR = 'The read is never one signal. The read is the chain.'
if CH7_ANCHOR in content:
    # Find the · · · after this anchor
    idx = content.find(CH7_ANCHOR)
    sep_idx = content.find('· · ·', idx)
    if sep_idx > 0:
        content = content[:sep_idx] + DISC_BRIDGE_SECTION + '\n' + content[sep_idx:]
        print('Ch7 DISC bridge section: ADDED')
        changes += 1
    else:
        print('Ch7 DISC bridge section: separator not found after anchor')
else:
    print('Ch7 DISC bridge section: ANCHOR NOT FOUND')

with open('manuscript-extracted.txt', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\nDone. {changes}/4 sections added.')
