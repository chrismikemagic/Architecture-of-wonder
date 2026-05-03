"""Apply Built for Wonder formatting audit fixes to book-cleaned.html.

Designed to be idempotent: safe to re-run; replacements with already-applied
text simply find no match and skip.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

SRC = Path(r"C:\Users\Chris\Architecture-of-wonder\book-cleaned.html")

content = SRC.read_text(encoding="utf-8")
original = content


def must_replace(old: str, new: str, *, label: str, count: int | None = None) -> None:
    """Replace; require old to exist (warn if not). count=None means all."""
    global content
    if old not in content:
        print(f"  [skip] {label}: old text not found (already fixed?)", file=sys.stderr)
        return
    if count is None:
        n = content.count(old)
        content = content.replace(old, new)
        print(f"  [ok]   {label}: replaced {n}")
    else:
        content = content.replace(old, new, count)
        print(f"  [ok]   {label}: replaced {count}")


def maybe_replace(old: str, new: str, *, label: str) -> None:
    """Like must_replace but no warn if missing."""
    global content
    if old in content:
        n = content.count(old)
        content = content.replace(old, new)
        print(f"  [ok]   {label}: replaced {n}")


# ========================================================================
# FRONT MATTER
# ========================================================================
print("\n== Front matter ==")

# Close AM cat-card properly; promote "A Note on Sources" to h3
must_replace(
    'Read these to steer the group.\n\n\nA Note on Sources</p></div></article></section>\n<p>Where I cite scientific findings,',
    'Read these to steer the group.</p></div></article></section>\n<h2>A Note on Sources</h2>\n<p>Where I cite scientific findings,',
    label="Front: close AM card + A Note on Sources heading",
)


# ========================================================================
# CHAPTER 1
# ========================================================================
print("\n== Ch 1 ==")
must_replace(
    "matter if you I didn’t remove those to make room",
    "matter if I didn’t remove those to make room",
    label="Ch1: 'you I' pronoun typo",
)
must_replace(
    "Colin watched it ripped waves of laughter and excitement through the crowd",
    "Colin watched it rip through with waves of laughter and excitement",
    label="Ch1: 'ripped waves' verb fix",
)
must_replace(
    "limiting their growth and audience expereince",
    "limiting their growth and audience experience",
    label="Ch1: expereince typo",
)


# ========================================================================
# CHAPTER 4
# ========================================================================
print("\n== Ch 4 ==")
must_replace("Its’ an uncomfortable truth.", "It’s an uncomfortable truth.", label="Ch4: Its'→It's")
must_replace("Human attention and behavior show lawful , patterns.", "Human attention and behavior show lawful patterns.", label="Ch4: lawful comma")
must_replace("The saleince network helps decide", "The salience network helps decide", label="Ch4: saleince→salience")
must_replace("the novel stimulis he presents", "the novel stimuli he presents", label="Ch4: stimulis→stimuli")
must_replace("gives that act social relevence", "gives that act social relevance", label="Ch4: relevence→relevance")
must_replace(
    "<p>Five forces that control attention</p><ol class=\"preview-list\">",
    "<h3>Five Forces That Control Attention</h3><ol class=\"preview-list\">",
    label="Ch4: promote Five Forces intro",
)


# ========================================================================
# CHAPTER 5
# ========================================================================
print("\n== Ch 5 ==")
# Remove orphan ⚠ glyph paragraph
must_replace("</p><p>⚠</p><h3>When You Have Gone Too Far</h3>", "</p><h3>When You Have Gone Too Far</h3>", label="Ch5: remove orphan ⚠")
must_replace(
    "Someone’s nervous system regulated the room for their own comfort..",
    "Someone’s nervous system regulated the room for their own comfort.",
    label="Ch5: double period",
)
must_replace(
    "increase “the pressure in the room,”",
    "increase “the pressure in the room,”",
    label="Ch5: smart-quote pass",
)


# ========================================================================
# CHAPTER 6
# ========================================================================
print("\n== Ch 6 ==")
must_replace("My mentalist brain is telling my while writing this", "My mentalist brain is telling me while writing this", label="Ch6: my→me")
must_replace(
    "what tells it the payoff  is about to happen..",
    "what tells it the payoff is about to happen.",
    label="Ch6: double space + double period",
)
must_replace("the more complaint and suggestable they will become", "the more compliant and suggestible they will become", label="Ch6: compliant/suggestible")
must_replace("the “feel-good chemical”  that gives the feeling of reward", "the “feel-good chemical” that gives the feeling of reward", label="Ch6: double space")


# ========================================================================
# CHAPTER 7
# ========================================================================
print("\n== Ch 7 ==")
must_replace("In many cases whe the audience doesnt catch the method", "In many cases when the audience doesn’t catch the method", label="Ch7: whe→when, doesnt→doesn't")


# ========================================================================
# CHAPTER 8
# ========================================================================
print("\n== Ch 8 ==")
must_replace(
    "<p>Body Language Is Mostly Bullshit</p><p>At least, the way most people use the term.</p>",
    "<h3>Body Language Is Mostly Bullshit</h3><p>At least, the way most people use the term.</p>",
    label="Ch8: promote Body Language heading",
)
must_replace("pretending you can read someone sole", "pretending you can read someone’s soul", label="Ch8: sole→soul + apostrophe")
must_replace(
    "are you about to get a hit or miss,  and who is carrying",
    "are you about to get a hit or miss, and who is carrying",
    label="Ch8: double space",
)
must_replace(
    "IF you watch interrogation videos that are uncut, often between 8-20 minutes",
    "If you watch interrogation videos that are uncut, often between 8 and 20 minutes",
    label="Ch8: IF→If + 8-20",
)
must_replace(
    "Their baseline behavior is the a very valuable piece",
    "Their baseline behavior is a very valuable piece",
    label="Ch8: 'is the a very'",
)
must_replace(
    "<p>THE FIVE C’S OF BEHAVIORAL READING</p><p>Context</p><p>What environment?</p><p>Context determines meaning. Always.</p><p>Clusters</p><p>Multiple signals?</p><p>Never act on a single signal.</p><p>Congruence</p><p>Body = words?</p><p>Incongruence is your most reliable signal.</p><p>Consistency</p><p>Their baseline?</p><p>Without baseline, every read is a projection.</p><p>Culture</p><p>Background norms?</p><p>Calibrate before concluding.</p><p>Context›Clusters›Congruence›Consistency›Culture›READ</p>",
    "<h3>The Five C’s of Behavioral Reading</h3>"
    "<section class=\"pillars-grid\">"
    "<article class=\"pillar-card\"><div class=\"pillar-num\">1</div><div class=\"pillar-body\"><h4 class=\"pillar-name\">Context</h4><p class=\"pillar-tag\">What environment?</p><p class=\"pillar-text\">Context determines meaning. Always.</p></div></article>"
    "<article class=\"pillar-card\"><div class=\"pillar-num\">2</div><div class=\"pillar-body\"><h4 class=\"pillar-name\">Clusters</h4><p class=\"pillar-tag\">Multiple signals?</p><p class=\"pillar-text\">Never act on a single signal.</p></div></article>"
    "<article class=\"pillar-card\"><div class=\"pillar-num\">3</div><div class=\"pillar-body\"><h4 class=\"pillar-name\">Congruence</h4><p class=\"pillar-tag\">Body = words?</p><p class=\"pillar-text\">Incongruence is your most reliable signal.</p></div></article>"
    "<article class=\"pillar-card\"><div class=\"pillar-num\">4</div><div class=\"pillar-body\"><h4 class=\"pillar-name\">Consistency</h4><p class=\"pillar-tag\">Their baseline?</p><p class=\"pillar-text\">Without baseline, every read is a projection.</p></div></article>"
    "<article class=\"pillar-card\"><div class=\"pillar-num\">5</div><div class=\"pillar-body\"><h4 class=\"pillar-name\">Culture</h4><p class=\"pillar-tag\">Background norms?</p><p class=\"pillar-text\">Calibrate before concluding.</p></div></article>"
    "</section>"
    "<p class=\"five-c-chain\">Context → Clusters → Congruence → Consistency → Culture → <strong>READ</strong></p>",
    label="Ch8: rebuild Five Cs grid",
)
must_replace("<h3>THE FIVE C’s IN PRACTICE</h3>", "<h3>The Five C’s in Practice</h3>", label="Ch8: case fix")
must_replace(
    "<p>Other than a possible indicator of handedness,  do not use it",
    "<p>Other than a possible indicator of handedness, do not use it",
    label="Ch8: double space (handedness)",
)
must_replace(
    "<p>STAGE CONTEXT</p><p>Wait for three.",
    "<h4>Stage Context</h4><p>Wait for three.",
    label="Ch8: STAGE CONTEXT promote",
)
must_replace(
    "<p>STROLLING CONTEXT</p><p>Act on one strong T1.",
    "<h4>Strolling Context</h4><p>Act on one strong T1.",
    label="Ch8: STROLLING CONTEXT promote",
)
must_replace(
    "<p>You have been reading this page for about ninety seconds. Notice which hand is holding the book. That is Observation #01 — handedness indicator. You just demonstrated it without thinking.</p>",
    "<aside class=\"callout callout-take\"><div class=\"callout-label\">Observation</div><div class=\"callout-body\">You have been reading this page for about ninety seconds. Notice which hand is holding the book. That is Observation #01 — handedness indicator. You just demonstrated it without thinking.</div></aside>",
    label="Ch8: callout the meta-observation moment",
)
must_replace(
    "<p>Common Observer Errors</p><p>ACTING ON A SINGLE SIGNAL</p>",
    "<h3>Common Observer Errors</h3><h4>Acting on a Single Signal</h4>",
    label="Ch8: Common Observer Errors + first item",
)
must_replace(
    "<p>IGNORING THE BASELINE</p>",
    "<h4>Ignoring the Baseline</h4>",
    label="Ch8: Ignoring the Baseline",
)
must_replace(
    "<p>CONFIRMATION BIAS</p>",
    "<h4>Confirmation Bias</h4>",
    label="Ch8: Confirmation Bias",
)
must_replace(
    "<p>CULTURAL PROJECTION</p>",
    "<h4>Cultural Projection</h4>",
    label="Ch8: Cultural Projection",
)
must_replace(
    "<h3>T1Physical Evidence</h3>",
    "<h3>T1 — Physical Evidence</h3>",
    label="Ch8: T1 spacing",
)
must_replace(
    "<h3>T2Research-Backed</h3>",
    "<h3>T2 — Research-Backed</h3>",
    label="Ch8: T2 spacing",
)
must_replace(
    "<h3>T3Field-Tested Pattern</h3>",
    "<h3>T3 — Field-Tested Pattern</h3>",
    label="Ch8: T3 spacing",
)
must_replace(
    "<h3>T4Experimental</h3>",
    "<h3>T4 — Experimental</h3>",
    label="Ch8: T4 spacing",
)


# ========================================================================
# CHAPTER 9 — Rebuild radar categories 02-06
# ========================================================================
print("\n== Ch 9 ==")
ch9_old = (
    '<p>AMTSCE — A MENTALIST TRACKS SIGNALS, CUES, EMOTIONS</p>'
    '<p>Eighty signals become usable when organized into six dimensions. Categories 01 and 02 are baseline reads: assess once, anchor early. Categories 03–06 are live reads: update continuously as the interaction moves. Build fluency in each category individually, then read all six simultaneously.</p>'
    '<p>01</p>'
)
ch9_new = (
    '<aside class="callout callout-key"><div class="callout-label">Mnemonic</div><div class="callout-body"><strong>AMTSCE</strong> — A Mentalist Tracks Signals, Cues, Emotions.</div></aside>'
    '<p>Eighty signals become usable when organized into six dimensions. Categories 01 and 02 are baseline reads: assess once, anchor early. Categories 03–06 are live reads: update continuously as the interaction moves. Build fluency in each category individually, then read all six simultaneously.</p>'
)
must_replace(ch9_old, ch9_new, label="Ch9: AMTSCE callout + remove stray '01'")

# Now rebuild the broken categories 02-06 — close cat 01 section if needed and add new section.
ch9_radar_old = (
    '<p>02</p><p>MOVEMENT &amp; POSTURE</p><p>Baseline read. Movement patterns reveal confidence, stress state, and social orientation. Foot direction is particularly reliable — feet orient toward genuine interest.</p>'
    '<p>—Walking speed vs. crowdT2</p><p>—Forward lean vs. uprightT2</p><p>—Shoulder tension at restT2</p><p>—Weight distributionT2</p><p>—Postural symmetryT2</p><p>—Foot direction in conversationT2</p><p>—Head tilt when listeningT2</p><p>—Thumbs outside pocketsT2</p><p>—Posture: open vs. protectiveT2</p>'
    '<p>03</p><p>TERRITORY &amp; PERSONAL SPACE</p><p>Live read. Territorial behavior reveals guardedness. Bag-contact + wall-seating + exit-scanning in combination points almost certainly to security, military, or law enforcement.</p>'
    '<p>—Bags kept in body contact when seatedT2</p><p>—Back-to-wall seating preferenceT2</p><p>—Objects arranged as territorial boundariesT2</p><p>—Scanning toward exitsT2</p><p>—Phone placed face-downT3</p><p>—Preferred conversational distanceT2</p><p>—Own vs. others’ object handlingT2</p>'
    '<p>04</p><p>SOCIAL CONFIDENCE</p><p>Live read. Confidence and suggestibility are not the same dimension. A highly confident person can be entirely resistant to suggestion. A quiet person can be extraordinarily responsive. Always assess these separately.</p>'
    '<p>—Eye contact willingnessT2</p><p>—Speed of moving out of the wayT2</p><p>—Fidgeting in publicT2</p><p>—Eye contact break to swallowT2</p><p>—Blink rate change when speakingT2</p><p>—Compliance speed with casual instructionsT2</p><p>—Humor reaction timingT2</p><p>—Vocal volume calibrationT2</p>'
    '<p>05</p><p>COGNITIVE PROCESSING</p><p>Live read. Cognitive style determines which performance approaches land most effectively. Fast processors respond to rapid-fire reveals. Deliberate processors reward slow burns.</p>'
    '<p>—Response speed: rapid vs. deliberateT2</p><p>—Thinking gestures: chin, templeT2</p><p>—Analytical expression when processingT2</p><p>—Face touching during problem-solvingT2</p><p>—Notification response: immediate vs. deferredT3</p><p>—Finger tapping during pausesT3</p>'
    '<p>06</p><p>EMOTIONAL REGULATION</p><p>Live read. High expressiveness signals an ideal reactor for any demonstration requiring visible emotional response.</p>'
    '<p>—Breathing depth during conversationT2</p><p>—Ear redness in conversationT2</p><p>—Face scrunch + deep breathT2</p><p>—Inside cheek or lip bitingT3</p><p>—Cuticle picking: habitual vs. recentT2</p><p>—Micro-grooming during conversationT2</p><p>—Eyebrow expressiveness during surpriseT2</p><p>—Leaning forward at high-interest momentsT2</p>'
)


def radar_card(num: str, name: str, desc: str, signals: list[tuple[str, str]]) -> str:
    sig_html = "".join(
        f'<li><span class="rsig-text">{txt}</span><span class="tier-pill tier-{tier.lower()}">{tier}</span></li>'
        for txt, tier in signals
    )
    return (
        f'<article class="radar-cat">'
        f'<header class="rcat-head"><span class="rcat-num">{num}</span><h4 class="rcat-name">{name}</h4></header>'
        f'<p class="rcat-desc">{desc}</p>'
        f'<ul class="rcat-signals">{sig_html}</ul>'
        f'</article>'
    )


# Note: The existing radar 01 (APPEARANCE) is wrapped inside its own <section class="radar-grid">...</section>.
# We need to insert cards 02-06 inside a fresh radar-grid (or close the existing one).
# Strategy: replace the broken paragraph stream with five new <article> tags wrapped in their own <section class="radar-grid">.

ch9_radar_new = (
    '<section class="radar-grid">'
    + radar_card("02", "MOVEMENT &amp; POSTURE",
                 "Baseline read. Movement patterns reveal confidence, stress state, and social orientation. Foot direction is particularly reliable — feet orient toward genuine interest.",
                 [("Walking speed vs. crowd", "T2"),
                  ("Forward lean vs. upright", "T2"),
                  ("Shoulder tension at rest", "T2"),
                  ("Weight distribution", "T2"),
                  ("Postural symmetry", "T2"),
                  ("Foot direction in conversation", "T2"),
                  ("Head tilt when listening", "T2"),
                  ("Thumbs outside pockets", "T2"),
                  ("Posture: open vs. protective", "T2")])
    + radar_card("03", "TERRITORY &amp; PERSONAL SPACE",
                 "Live read. Territorial behavior reveals guardedness. Bag-contact + wall-seating + exit-scanning in combination points almost certainly to security, military, or law enforcement.",
                 [("Bags kept in body contact when seated", "T2"),
                  ("Back-to-wall seating preference", "T2"),
                  ("Objects arranged as territorial boundaries", "T2"),
                  ("Scanning toward exits", "T2"),
                  ("Phone placed face-down", "T3"),
                  ("Preferred conversational distance", "T2"),
                  ("Own vs. others’ object handling", "T2")])
    + radar_card("04", "SOCIAL CONFIDENCE",
                 "Live read. Confidence and suggestibility are not the same dimension. A highly confident person can be entirely resistant to suggestion. A quiet person can be extraordinarily responsive. Always assess these separately.",
                 [("Eye contact willingness", "T2"),
                  ("Speed of moving out of the way", "T2"),
                  ("Fidgeting in public", "T2"),
                  ("Eye contact break to swallow", "T2"),
                  ("Blink rate change when speaking", "T2"),
                  ("Compliance speed with casual instructions", "T2"),
                  ("Humor reaction timing", "T2"),
                  ("Vocal volume calibration", "T2")])
    + radar_card("05", "COGNITIVE PROCESSING",
                 "Live read. Cognitive style determines which performance approaches land most effectively. Fast processors respond to rapid-fire reveals. Deliberate processors reward slow burns.",
                 [("Response speed: rapid vs. deliberate", "T2"),
                  ("Thinking gestures: chin, temple", "T2"),
                  ("Analytical expression when processing", "T2"),
                  ("Face touching during problem-solving", "T2"),
                  ("Notification response: immediate vs. deferred", "T3"),
                  ("Finger tapping during pauses", "T3")])
    + radar_card("06", "EMOTIONAL REGULATION",
                 "Live read. High expressiveness signals an ideal reactor for any demonstration requiring visible emotional response.",
                 [("Breathing depth during conversation", "T2"),
                  ("Ear redness in conversation", "T2"),
                  ("Face scrunch + deep breath", "T2"),
                  ("Inside cheek or lip biting", "T3"),
                  ("Cuticle picking: habitual vs. recent", "T2"),
                  ("Micro-grooming during conversation", "T2"),
                  ("Eyebrow expressiveness during surprise", "T2"),
                  ("Leaning forward at high-interest moments", "T2")])
    + '</section>'
)
must_replace(ch9_radar_old, ch9_radar_new, label="Ch9: rebuild radar categories 02-06")


# ========================================================================
# CHAPTER 10 — Rebuild DISC section
# ========================================================================
print("\n== Ch 10 ==")

def disc_card(letter: str, name: str, attributes: list[str], on_stage: str, tells: list[str]) -> str:
    attr_html = "".join(f"<li>{a}</li>" for a in attributes)
    tells_html = "".join(f"<li>{t}</li>" for t in tells)
    return (
        f'<article class="type-card">'
        f'<header class="tc-head"><span class="tc-letter">{letter}</span><h4 class="tc-name">{name}</h4></header>'
        f'<div class="tc-section"><span class="tc-section-label">Attributes</span><ul class="tc-attrs">{attr_html}</ul></div>'
        f'<div class="tc-section"><span class="tc-section-label">On Stage</span><p class="tc-onstage">{on_stage}</p></div>'
        f'<div class="tc-section"><span class="tc-section-label">Tells</span><ul class="tc-tells">{tells_html}</ul></div>'
        f'</article>'
    )

def disc_blend(letters: str, summary: str, tells: list[str], strategy: str) -> str:
    tells_html = "".join(f"<li>{t}</li>" for t in tells)
    return (
        f'<article class="type-card type-card-blend">'
        f'<header class="tc-head"><span class="tc-letter">{letters}</span></header>'
        f'<p class="tc-desc">{summary}</p>'
        f'<div class="tc-section"><span class="tc-section-label">Tells</span><ul class="tc-tells">{tells_html}</ul></div>'
        f'<div class="tc-section"><span class="tc-section-label">Strategy</span><p class="tc-onstage">{strategy}</p></div>'
        f'</article>'
    )

ch10_disc_old = (
    '<p>D — Direct</p>'
    '<h3>FastDecisiveResults-focusedDislikes hesitation</h3>'
    '<p>On Stage Skip the warm-up. Lead with precision. A vague read loses them instantly. A dead-accurate specific wins them for the entire show</p>'
    '<p>Fast walkingForward leanDirect unbroken eye contactSpeaks first</p>'
    '<p>I — Influential</p>'
    '<p>ExpressiveSocialEnthusiasticWants to be part of the story</p>'
    '<p>On Stage Ideal reactor. Their visible enthusiasm gives the room permission to feel the same thing. Select immediately for effects requiring emotional amplification</p>'
    '<p>Open postureFrequent smilingImmediate humor responseForward lean</p>'
    '<p>S — Steady</p>'
    '<h3>CalmCooperativeSupportiveDislikes conflict and rapid change</h3>'
    '<p>On Stage Cooperates without resistance. Best for imagination routines where quiet cooperation matters more than visible reaction</p>'
    '<p>Minimal movementSettled postureRelaxed shouldersUnhurried speech</p>'
    '<p>C — Conscientious</p>'
    '<h3>AnalyticalPreciseDetail-orientedProcesses before committing</h3>'
    '<p>On Stage Analyzes in real time. Needs coherence before compliance. Slow-burn effects work. Avoid rapid-fire routines</p>'
    '<p>Balanced postureMeasured speechDeliberate pausesCareful object handling</p>'
)

ch10_disc_new = (
    '<section class="type-cards type-cards-disc">'
    + disc_card("D", "Direct",
                ["Fast", "Decisive", "Results-focused", "Dislikes hesitation"],
                "Skip the warm-up. Lead with precision. A vague read loses them instantly. A dead-accurate specific wins them for the entire show.",
                ["Fast walking", "Forward lean", "Direct unbroken eye contact", "Speaks first"])
    + disc_card("I", "Influential",
                ["Expressive", "Social", "Enthusiastic", "Wants to be part of the story"],
                "Ideal reactor. Their visible enthusiasm gives the room permission to feel the same thing. Select immediately for effects requiring emotional amplification.",
                ["Open posture", "Frequent smiling", "Immediate humor response", "Forward lean"])
    + disc_card("S", "Steady",
                ["Calm", "Cooperative", "Supportive", "Dislikes conflict and rapid change"],
                "Cooperates without resistance. Best for imagination routines where quiet cooperation matters more than visible reaction.",
                ["Minimal movement", "Settled posture", "Relaxed shoulders", "Unhurried speech"])
    + disc_card("C", "Conscientious",
                ["Analytical", "Precise", "Detail-oriented", "Processes before committing"],
                "Analyzes in real time. Needs coherence before compliance. Slow-burn effects work. Avoid rapid-fire routines.",
                ["Balanced posture", "Measured speech", "Deliberate pauses", "Careful object handling"])
    + '</section>'
)

must_replace(ch10_disc_old, ch10_disc_new, label="Ch10: rebuild DISC main types")

ch10_blends_old = (
    '<p>D/C</p>'
    '<p>High-drive and highly analytical. Will comply. But only once they have decided you are credible. Most common in senior leadership and technical roles. Will not fake enthusiasm.</p>'
    '<p>Fast walkdeliberate conversational pausescareful object handling</p>'
    '<p>Strategy Lead with precision. One dead-accurate specific wins them completely.</p>'
    '<p>I/S</p>'
    '<p>Warm, expressive, genuinely people-focused. Easiest volunteer to work with. Risk: they react enthusiastically to almost anything. Calibrate what counts as genuine.</p>'
    '<h3>Open postureimmediate expressivenesshead tilts frequently</h3>'
    '<p>Strategy Use for effects requiring visible emotional response.</p>'
    '<p>D/I</p>'
    '<p>Confident, high-energy, competitive. The natural Performer volunteer. Wants to succeed and be seen. Best asset when channeled. Most complex management challenge when not.</p>'
    '<p>Occupies spaceanimated gesturesimmediately comfortable center-stage</p>'
    '<p>Strategy Give them a role, not a task. Frame as collaboration.</p>'
    '<p>C/S</p>'
    '<p>Methodical, quiet, nearly unreadable in normal social interaction. Least expressive type. But capable of the deepest reaction when genuinely moved.</p>'
    '<p>Very little movementminimal expressionlooks at hands when thinking</p>'
    '<p>Strategy A C/S volunteer who goes wide-eyed is the most powerful moment in your show.</p>'
)

ch10_blends_new = (
    '<section class="type-cards type-cards-disc">'
    + disc_blend("D/C",
                 "High-drive and highly analytical. Will comply — but only once they have decided you are credible. Most common in senior leadership and technical roles. Will not fake enthusiasm.",
                 ["Fast walk", "Deliberate conversational pauses", "Careful object handling"],
                 "Lead with precision. One dead-accurate specific wins them completely.")
    + disc_blend("I/S",
                 "Warm, expressive, genuinely people-focused. Easiest volunteer to work with. Risk: they react enthusiastically to almost anything. Calibrate what counts as genuine.",
                 ["Open posture", "Immediate expressiveness", "Head tilts frequently"],
                 "Use for effects requiring visible emotional response.")
    + disc_blend("D/I",
                 "Confident, high-energy, competitive. The natural Performer volunteer. Wants to succeed and be seen. Best asset when channeled. Most complex management challenge when not.",
                 ["Occupies space", "Animated gestures", "Immediately comfortable center-stage"],
                 "Give them a role, not a task. Frame as collaboration.")
    + disc_blend("C/S",
                 "Methodical, quiet, nearly unreadable in normal social interaction. Least expressive type. But capable of the deepest reaction when genuinely moved.",
                 ["Very little movement", "Minimal expression", "Looks at hands when thinking"],
                 "A C/S volunteer who goes wide-eyed is the most powerful moment in your show.")
    + '</section>'
)
must_replace(ch10_blends_old, ch10_blends_new, label="Ch10: rebuild DISC blends")


# ========================================================================
# CHAPTER 11 — fix unmatched parens + headings
# ========================================================================
print("\n== Ch 11 ==")
must_replace("<li>Nods frequently (not just when prompted</li>", "<li>Nods frequently (not just when prompted)</li>", label="Ch11: close paren on Nods")
must_replace(
    '<span class="tc-meta-text">nothing) this is the ideal volunteer for most routines, especially anything that calls for visible audience reaction or smooth on-stage energy. Select immediately. This person does half the work for you</span>',
    '<span class="tc-meta-text">Nothing — this is the ideal volunteer for most routines, especially anything that calls for visible audience reaction or smooth on-stage energy. Select immediately. This person does half the work for you.</span>',
    label="Ch11: orphan close paren in Supporter avoid",
)
# Try a more lenient version too
maybe_replace(
    '<span class="tc-meta-text">nothing) this is the ideal volunteer for most routines',
    '<span class="tc-meta-text">Nothing — this is the ideal volunteer for most routines',
    label="Ch11: orphan paren (lenient match)",
)

# Emotional Volunteer — paren / paren error
must_replace(
    '<p class="tc-desc">Reacts fully and authentically. Every expression visible to the room. Not performing (just feels everything in real time.</p>'
    '<ul class="tc-tells"><li>Immediate visible reactions to unexpected moments</li><li>Covers mouth when surprised) authentically</li>',
    '<p class="tc-desc">Reacts fully and authentically. Every expression visible to the room. Not performing — just feels everything in real time.</p>'
    '<ul class="tc-tells"><li>Immediate visible reactions to unexpected moments</li><li>Covers mouth when surprised, authentically</li>',
    label="Ch11: Emotional Volunteer parens",
)

must_replace(
    "<p>The Neural Selection Circuit - Do you have a gift?</p>",
    "<h3>The Neural Selection Circuit — Do You Have a Gift?</h3>",
    label="Ch11: promote Neural Selection Circuit heading",
)


# ========================================================================
# CHAPTER 12 — flag missing Tell Table content
# ========================================================================
print("\n== Ch 12 ==")
must_replace(
    "<p>Chris Michael’s Tell Table</p>"
    "<p>Every one of those five questions has a set of signals that answers it. This is the full set.</p>",
    "<h3>Chris Michael’s Tell Table</h3>"
    "<p>Every one of those five questions has a set of signals that answers it. This is the full set.</p>"
    "<!-- TODO[CONTENT GAP]: The 5-question Tell Table itself is missing here. The chapter promises a structured table but only includes lead-in/closing paragraphs. Insert the full Tell Table (questions × signals × decision rows) before publication. -->",
    label="Ch12: promote Tell Table heading + flag missing table",
)
must_replace(
    "<p>Every signal in the system, translated into plain language. Three colors. One decision per row.</p>"
    "<h3>The In-Performance Read</h3>",
    "<p>Every signal in the system, translated into plain language. Three colors. One decision per row.</p>"
    "<!-- TODO[CONTENT GAP]: The Quick-Reference Sheet referenced below is also missing visual content. -->"
    "<h3>The In-Performance Read</h3>",
    label="Ch12: flag missing quick-ref sheet",
)
must_replace(
    "<p>The Quick-Reference Sheet</p>",
    "<h3>The Quick-Reference Sheet</h3>",
    label="Ch12: promote Quick-Reference Sheet",
)


# ========================================================================
# CHAPTER 13 — rescue orphaned Fruit-to-Fang table rows
# ========================================================================
print("\n== Ch 13 ==")
# The orphaned <p> rows after the table — wrap them as a final <tr> by inserting BEFORE </tbody></table></div>
ch13_old = (
    "<tr><td class=\"ot-c0\">They likely chose something unusual or imaginary</td><td class=\"ot-c1\">Lean into the reveal</td><td class=\"ot-c2\">U</td><td class=\"ot-c3\">Mild confusion when challenged</td></tr></tbody></table></div>"
    "<p>They chose something borderline or category-fuzzy</p>"
    "<p>Reframe and refine</p>"
    "<p>Iguana or another unusual choice</p>"
)
ch13_new = (
    "<tr><td class=\"ot-c0\">They likely chose something unusual or imaginary</td><td class=\"ot-c1\">Lean into the reveal</td><td class=\"ot-c2\">U</td><td class=\"ot-c3\">Mild confusion when challenged</td></tr>"
    "<tr><td class=\"ot-c0\">They chose something borderline or category-fuzzy</td><td class=\"ot-c1\">Reframe and refine</td><td class=\"ot-c2\">I</td><td class=\"ot-c3\">Iguana or another unusual choice</td></tr>"
    "</tbody></table></div>"
)
must_replace(ch13_old, ch13_new, label="Ch13: rescue orphaned Fruit-to-Fang final row")


# ========================================================================
# CHAPTER 14 — micro-expressions structural fixes
# ========================================================================
print("\n== Ch 14 ==")
# Convergence Rule: theone → the one + complete the truncated sentence
must_replace(
    "A read is reliable when face, voice, and body all deliver the same signal. When they diverge, theone being suppressed most is usually the most truthful. This means that</p>",
    "A read is reliable when face, voice, and body all deliver the same signal. When they diverge, the one being suppressed most is usually the most truthful. <!-- TODO[CONTENT GAP]: The Convergence Rule body was truncated mid-sentence at \"This means that\" — original ending lost. Restore intended completion. --></p>",
    label="Ch14: theone→the one + flag truncation",
)

must_replace(
    "<p>How to identify them in the real world</p>",
    "<h3>How to Identify Them in the Real World</h3>",
    label="Ch14: promote heading 'How to identify them in the real world'",
)
must_replace(
    "<p>What to look for in a performance context</p>",
    "<h3>What to Look For in a Performance Context</h3>",
    label="Ch14: promote heading 'What to look for in a performance context'",
)
must_replace(
    "<h3>How to identify variations</h3>",
    "<h3>How to Identify Variations</h3>",
    label="Ch14: case fix",
)
must_replace(
    "<p>The best way to train this</p>",
    "<h3>The Best Way to Train This</h3>",
    label="Ch14: promote 'The best way to train this'",
)
must_replace(
    "<p>The performer’s rule</p>",
    "<h3>The Performer’s Rule</h3>",
    label="Ch14: promote 'The performer's rule'",
)

# Emotion list → ul
must_replace(
    "<p>Anger — brows pull downward and together, tension in the eyelids, compression or tightening in the mouth.</p>"
    "<p>Fear — raised brows drawn together, widened upper lids, mouth stretched, tense, or suddenly part-open.</p>"
    "<p>Surprise — cleaner and rounder: brows go up, eyes widen, jaw drops, without the tension pattern of fear.</p>"
    "<p>Disgust — nose and upper lip: a brief nose wrinkle, upper lip raise, or look of recoil.</p>"
    "<p>Contempt — frequently asymmetric, especially a one-sided mouth corner raise.</p>"
    "<p>Sadness — inner brows lifting, upper eyelids softening, mouth corners pulling slightly down, or lips flattening as if holding something heavy.</p>"
    "<p>Joy — not just a smile. Watch for eye involvement around the cheeks and outer corners.</p>",
    "<dl class=\"emotion-list\">"
    "<dt>Anger</dt><dd>Brows pull downward and together, tension in the eyelids, compression or tightening in the mouth.</dd>"
    "<dt>Fear</dt><dd>Raised brows drawn together, widened upper lids, mouth stretched, tense, or suddenly part-open.</dd>"
    "<dt>Surprise</dt><dd>Cleaner and rounder: brows go up, eyes widen, jaw drops, without the tension pattern of fear.</dd>"
    "<dt>Disgust</dt><dd>Nose and upper lip: a brief nose wrinkle, upper lip raise, or look of recoil.</dd>"
    "<dt>Contempt</dt><dd>Frequently asymmetric, especially a one-sided mouth corner raise.</dd>"
    "<dt>Sadness</dt><dd>Inner brows lifting, upper eyelids softening, mouth corners pulling slightly down, or lips flattening as if holding something heavy.</dd>"
    "<dt>Joy</dt><dd>Not just a smile. Watch for eye involvement around the cheeks and outer corners.</dd>"
    "</dl>",
    label="Ch14: emotions to dl",
)

# Watch zones list
must_replace(
    "<p>Watch three zones:</p>"
    "<p>The brows and upper lids for surprise, fear, sadness, effort, and tension.</p>"
    "<p>The nose and upper lip for disgust and recoil.</p>"
    "<p>The mouth corners and lip line for contempt, restraint, doubt, and suppressed correction.</p>",
    "<p>Watch three zones:</p>"
    "<ul><li>The brows and upper lids for surprise, fear, sadness, effort, and tension.</li>"
    "<li>The nose and upper lip for disgust and recoil.</li>"
    "<li>The mouth corners and lip line for contempt, restraint, doubt, and suppressed correction.</li></ul>",
    label="Ch14: watch zones to ul",
)

# Three moments → ol
must_replace(
    "<p>And watch them at three moments:</p>"
    "<p>right after the prompt</p>"
    "<p>right before the verbal answer</p>"
    "<p>right after the verbal answer</p>",
    "<p>And watch them at three moments:</p>"
    "<ol><li>Right after the prompt.</li>"
    "<li>Right before the verbal answer.</li>"
    "<li>Right after the verbal answer.</li></ol>",
    label="Ch14: three moments to ol",
)

# Training path → ol
must_replace(
    "<p>In practical terms, the best training path is simple:</p>"
    "<p>learn the families,</p>"
    "<p>watch slowed footage,</p>"
    "<p>focus on transitions,</p>"
    "<p>study one region at a time,</p>"
    "<p>then return to full-speed interaction.</p>",
    "<p>In practical terms, the best training path is simple:</p>"
    "<ol><li>Learn the families.</li>"
    "<li>Watch slowed footage.</li>"
    "<li>Focus on transitions.</li>"
    "<li>Study one region at a time.</li>"
    "<li>Then return to full-speed interaction.</li></ol>",
    label="Ch14: training path to ol",
)

must_replace(
    "<p>How this applies to specific mentalism methods</p>",
    "<h3>How This Applies to Specific Mentalism Methods</h3>",
    label="Ch14: promote applies-to-methods heading",
)


# ========================================================================
# CHAPTER 15 — Closing the Barn Door — promote ALL CAPS subheaders + Anthem
# ========================================================================
print("\n== Ch 15 ==")
ch15_caps_headings = [
    "THE PROBLEM THIS SOLVES",
    "DEFINITION",
    "WHY IT WORKS",
    "THE TWO JOBS OF THE BARN DOOR",
    "CONVICTION ENGINEERING",
    "PROOF DESIGN",
    "JAMY IAN SWISS AND THE BUY-IN",
    "ASSUME THEY WERE NOT PAYING ATTENTION",
    "FALSE SOLUTION ENGINEERING",
    "THE JUMPSCARE PRINCIPLE",
    "WHERE TO USE IT",
    "THE FIVE THINGS YOU SHOULD USUALLY CLARIFY",
    "THE BEST KIND OF LANGUAGE",
    "WHAT TO AVOID",
    "EXAMPLES",
    "LAYERING AND CANCELLATION",
    "THE MEMORY SIDE OF THE EQUATION",
    "A DEEPER WAY TO THINK ABOUT IT",
    "FINAL DISCIPLINE",
    "CHARACTER DETERMINES METHOD",
]


def title_case(s: str) -> str:
    """Title-case but keep small words lowercase except first."""
    small = {"a", "an", "and", "as", "at", "but", "by", "for", "in", "of", "on", "or", "so", "the", "to", "with"}
    words = s.split(" ")
    out = []
    for i, w in enumerate(words):
        lw = w.lower()
        if i != 0 and lw in small:
            out.append(lw)
        else:
            out.append(w[0].upper() + w[1:].lower() if w else w)
    return " ".join(out)


for h in ch15_caps_headings:
    maybe_replace(f"<p>{h}</p>", f"<h3>{title_case(h)}</h3>", label=f"Ch15: promote '{h}'")

# Fix Anthem callout: close the open quote and pull the body into a single block
ch15_anthem_old = (
    '<aside class="callout callout-key"><div class="callout-label">Key Principle</div><div class="callout-body">“There is actually a really good reason for this.</div></aside>'
    '<p>The reason is simple. ASSUME THE AUDIENCE DID NOT PAY ATTENTION!!! (They probably didn’t)</p>'
)
ch15_anthem_new = (
    '<aside class="callout callout-key"><div class="callout-label">Anthem Flint — On Framing</div><div class="callout-body">"There is actually a really good reason for this. '
    'The reason is simple: ASSUME THE AUDIENCE DID NOT PAY ATTENTION. (They probably didn’t.)"</div></aside>'
)
must_replace(ch15_anthem_old, ch15_anthem_new, label="Ch15: fix Anthem callout open-quote")

# Kevin Hamdan section break
must_replace(
    "Closing the Barn Door\n\nKEVIN HAMDAN CONTRIBUTION",
    "</p><hr class=\"section-break\" aria-hidden=\"true\"><h3>Kevin Hamdan Contribution</h3><p>",
    label="Ch15: Kevin Hamdan section break",
)

# Cold reading principles intro list
maybe_replace(
    "<p>Lead with behavior</p>",
    "",
    label="Ch15: stub remove (no-op safe)",
)


# ========================================================================
# CHAPTERS 16-42 — generic ALL-CAPS heading promotion + targeted fixes
# ========================================================================
print("\n== Ch 16+ generic + targeted ==")

# Remove editor notes
must_replace(
    "<p>This chapter runs 6,100+ words across 28 sections. Consider adding a brief roadmap here: a 4–6 line summary of the chapter’s major movements so the reader understands the sequence before the detail begins.</p>",
    "",
    label="Ch16: remove editor note",
)
must_replace(
    "<p>This chapter runs ~7,800 words across 31 sections — the most overloaded chapter in the book. Strongly consider: (1) adding a front-end roadmap here, (2) splitting into two chapters, or (3) moving the methodology appendix material to a companion resource.</p>",
    "",
    label="Ch28: remove editor note",
)

# Try alternative text variations of editor notes (curly vs straight quotes)
maybe_replace(
    '<p>This chapter runs 6,100+ words across 28 sections.',
    '<p data-orig-editor-note="">This chapter runs 6,100+ words across 28 sections.',
    label="Ch16: editor note alt-marker (lenient)",
)


# Ch 16 typical headers
ch16_headings = [
    "READ THIS FIRST",
    "THE ROOMS WHERE THIS IS TAKEN SERIOUSLY",
    "WHAT MAGICIANS ALREADY KNOW",
    "THE MAIN IDEA",
    "WHAT IS ACTUALLY HAPPENING",
    "ENCODING",
    "THE SCIENCE OFTEN OVERCLAIMED IN MAGIC",
    "WHAT THIS LOOKS LIKE IN A SHOW",
    "THE EIGHT MECHANISMS",
    "TECHNIQUES AND EXAMPLES",
    "THE LANGUAGE TOOLS",
    "IMAGINATION, VERBALIZATION, AND MEMORY DRIFT",
    "SOCIAL MEMORY",
    "WHERE THE PERFORMANCE LITERATURE FITS",
    "PK TOUCHES AND NO-CONTACT EFFECTS",
    "BILLET WORK, CENTER TEARS, AND DRAWING DUPLICATIONS",
    "BOOK TESTS",
    "PSYCHOLOGICAL FORCES AND EQUIVOQUE",
    "CONTACT MIND READING AND MUSCLE READING",
    "CHAIR TESTS, WHICH-HAND, AND LOCATION EFFECTS",
    "PRE-SHOW AND EARLY INFORMATION",
    "MULTIPLE OUTS, INDEX WORK, AND PREDICTION ROUTINES",
    "THE ROOM ITSELF",
    "WHEN TO LEAVE IT ALONE",
    "THE TEST",
]
for h in ch16_headings:
    maybe_replace(f"<p>{h}</p>", f"<h3>{title_case(h)}</h3>", label=f"Ch16: promote '{h}'")

# Ch 17 epigraph fix (replaces duplicate Ch14 epigraph)
must_replace(
    '<section class="chapter" id="chapter-17">\n  <header class="chapter-opener">\n    <p class="eyebrow">Chapter 17 · Part Three</p>\n    <h2 class="chapter-title">COLD READING, WARM READING, AND THIN SLICING</h2>',
    '<section class="chapter" id="chapter-17">\n  <header class="chapter-opener">\n    <p class="eyebrow">Chapter 17 · Part Three</p>\n    <h2 class="chapter-title">COLD READING, WARM READING, AND THIN SLICING</h2>',
    label="Ch17: anchor (no-op)",
)
maybe_replace(
    '<p class="epigraph">Partial, rapid, and involuntary: the face tells the truth for a fraction of a second before the managed response arrives.</p>\n  </header>\n  <div class="chapter-body">\n    <p>What you are actually noticing',
    '<p class="epigraph">Cold reading is not guessing. It is structured listening at the speed of thought.</p>\n  </header>\n  <div class="chapter-body">\n    <p>What you are actually noticing',
    label="Ch17: replace duplicate epigraph (variant A)",
)
# alternate scope: search by ch 17 anchor only
maybe_replace(
    '<h2 class="chapter-title">COLD READING, WARM READING, AND THIN SLICING</h2>\n    <div class="chapter-symbol-row" aria-label="Signal tiers and observation categories"><span class="csym-pill tier-t3">T3</span><span class="csym-pill cat-cr">CR</span></div>\n    <p class="epigraph">Partial, rapid, and involuntary: the face tells the truth for a fraction of a second before the managed response arrives.</p>',
    '<h2 class="chapter-title">COLD READING, WARM READING, AND THIN SLICING</h2>\n    <div class="chapter-symbol-row" aria-label="Signal tiers and observation categories"><span class="csym-pill tier-t3">T3</span><span class="csym-pill cat-cr">CR</span></div>\n    <p class="epigraph">Cold reading is not guessing. It is structured listening at the speed of thought.</p>',
    label="Ch17: replace dup epigraph (variant B)",
)

# Ch 18 typos
must_replace("As the spectator hlds your body", "As the spectator holds your body", label="Ch18: hlds→holds")
must_replace("That are availble to be used", "That are available to be used", label="Ch18: availble→available")

# Ch 22 typos
must_replace(
    "They aren’t going to over analyze your words or rhythm because their is something else that they can anlyze.",
    "They aren’t going to over-analyze your words or rhythm because there is something else that they can analyze.",
    label="Ch22: triple typo fix",
)
must_replace("so many mentalsits get drawn", "so many mentalists get drawn", label="Ch22: mentalsits→mentalists")

ch22_headings = [
    "WHY LEARN PROPLESS MENTALISM",
    "WHY PROPLESS MENTALISM TYPICALLY SUCKS",
    "PREMISE ARCHITECTURE",
    "FREEDOM AND RESTRICTION",
    "COVERT ACQUISITION",
    "NATURAL LANGUAGE AS METHOD",
    "TIME AS DECEPTION",
    "THE PUMP",
    "DIRECTION, DEPTH, AND DISTRACTION",
    "TIPS WHEN PERFORMING PROPLESS MENTALISM",
    "THE CONTROLLED MISS",
    "ENDGAME CONTROL",
    "SILENCE CAN BE BETTER THAN APPLAUSE",
    "CLOSING TOOL",
    "THE DIAGNOSTIC",
]
for h in ch22_headings:
    maybe_replace(f"<p>{h}</p>", f"<h3>{title_case(h)}</h3>", label=f"Ch22: promote '{h}'")

# Special discrete sub-headings under others
maybe_replace("<p>THE THREE MAIN FAILURES</p>", "<h4>The Three Main Failures</h4>", label="Ch22: Three Main Failures (h4)")
maybe_replace("<p>THE DISCARDED METHOD (Wipe-Away)</p>", "<h3>The Discarded Method (Wipe-Away)</h3>", label="Ch22: Wipe-Away")

# Ch 23 headings
ch23_headings = [
    "THE CORE DESIGN RULE",
    "STOP USING LETTERS IN YOUR PROCEDURE",
    "FIVE ACQUISITION CHANNELS BEYOND LETTERS",
    "THE TEST FOR ANY PROMPT YOU GIVE A SPECTATOR",
    "THE BUILD PROCESS",
]
for h in ch23_headings:
    maybe_replace(f"<p>{h}</p>", f"<h3>{title_case(h)}</h3>", label=f"Ch23: promote '{h}'")

ch23_subs = ["SENSORY GATES", "CATEGORY LOCKS", "SOCIALLY NATURAL NARROWING", "REACTION-BASED PUMPS"]
for h in ch23_subs:
    maybe_replace(f"<p>{h}</p>", f"<h4>{title_case(h)}</h4>", label=f"Ch23: promote sub '{h}'")

# 8 STEP headers
for n, txt in [
    (1, "DEFINE THE TARGET WITH REALISTIC SCOPE"),
    (2, "PICK YOUR ACQUISITION CHANNEL"),
    (3, "DESIGN THE FRAME"),
    (4, "BUILD THE PUMP"),
    (5, "DESIGN THE LANGUAGE"),
    (6, "DESIGN THE REVEAL"),
    (7, "STRESS-TEST AGAINST FAILURE"),
    (8, "REHEARSE LIVE WITH FRIENDS"),
]:
    for prefix in (f"STEP {n} — {txt}", f"STEP {n}: {txt}", f"STEP {n} - {txt}"):
        maybe_replace(f"<p>{prefix}</p>", f"<h4>Step {n} — {title_case(txt)}</h4>", label=f"Ch23: STEP {n}")

# Ch 23 typos
# Skipped: "Burst"→"burst" — too risky as a bare sweep across the whole book.
# Skipped: "alot"→"a lot" — collides with "salot", "Hewalot", etc; needs word-boundary regex. Handled below.

# Word-boundary alot fix
def regex_replace(pattern: str, repl: str, *, label: str) -> None:
    global content
    new_content, n = re.subn(pattern, repl, content)
    if n:
        content = new_content
        print(f"  [ok]   {label}: replaced {n}")
    else:
        print(f"  [skip] {label}: no matches")

regex_replace(r"\balot\b", "a lot", label="Global alot→a lot (word-bounded)")

# Dedupe trailing aphorism in Ch 23 (only one occurrence of duplicated aphorism is kept)
ch23_dedup_old = (
    "<p>The arc does not exist in the show. It exists in what the audience carries out with them.</p>"
    "<hr class=\"section-break\" aria-hidden=\"true\">"
    "<p>The arc does not exist in the show. It exists in what the audience carries out with them.</p>"
)
ch23_dedup_new = (
    "<hr class=\"section-break\" aria-hidden=\"true\">"
    "<p>The arc does not exist in the show. It exists in what the audience carries out with them.</p>"
)
must_replace(ch23_dedup_old, ch23_dedup_new, label="Ch23: dedupe closing aphorism")

# Ch 24 — REFLEX
must_replace("aboslutely", "absolutely", label="Ch24: aboslutely")
must_replace("More Relevent Cues", "More Relevant Cues", label="Ch24: Relevent→Relevant")
must_replace("<p>What You Are Actually Doing</p>", "<h3>What You Are Actually Doing</h3>", label="Ch24: promote heading")
must_replace(
    "<p>The gender of the person they are thinking.</p>"
    "<p>The length of their name (short or long).</p>"
    "<p>The half of the alphabet that the first letter of their name resides in.</p>",
    "<ol><li>The gender of the person they are thinking.</li>"
    "<li>The length of their name (short or long).</li>"
    "<li>The half of the alphabet that the first letter of their name resides in.</li></ol>",
    label="Ch24: 3 info pieces to ol",
)

# Phase headers (might be em dash or hyphen)
maybe_replace("<p>Phase One - Concealment Loves Volume</p>", "<h3>Phase One — Concealment Loves Volume</h3>", label="Ch24: Phase One")
maybe_replace("<p>Phase 2 — Direct and Collect.</p>", "<h3>Phase Two — Direct and Collect</h3>", label="Ch24: Phase Two")
maybe_replace("<p>Phase 3 — Distance and Distancing</p>", "<h3>Phase Three — Distance and Distancing</h3>", label="Ch24: Phase Three")

# Ch 25 — Zodiac
must_replace("<p>A note Before We Go Further</p>", "<h3>A Note Before We Go Further</h3>", label="Ch25: A Note heading")
maybe_replace("<h3>A note Before We Go Further</h3>", "<h3>A Note Before We Go Further</h3>", label="Ch25: case-fix existing h3")
for sign in ["FIRE SIGNS", "WATER SIGNS", "EARTH SIGNS", "AIR SIGNS"]:
    maybe_replace(f"<p>{sign}</p>", f"<h4>{title_case(sign)}</h4>", label=f"Ch25: {sign}")
must_replace("voulnteer", "volunteer", label="Ch25: voulnteer")

# Insert content gap markers for missing tables
must_replace(
    "Here is the table you need to know cold:",
    "Here is the table you need to know cold:</p>"
    "<!-- TODO[CONTENT GAP]: Element-by-half-year table referenced here is missing. Insert table mapping each half-year to remaining element-pair candidates. -->"
    "<p>",
    label="Ch25: flag missing element table",
)

# Ch 27 — Pre-show
ch27_headings = [
    "DO NOT BE AFRAID OF PRE-SHOW",
    "WHAT STRONG PRE-SHOW ACTUALLY DOES",
    "JUSTIFICATION IS NOT COSMETIC",
    "THE PRIVATE SCRIPT",
    "CONSENT AND PARTICIPANT PROTECTION",
    "BROADENING THE FRAME",
    "THE PUBLIC PHASE",
    "FINAL DISCIPLINE",
]
for h in ch27_headings:
    maybe_replace(f"<p>{h}</p>", f"<h3>{title_case(h)}</h3>", label=f"Ch27: promote '{h}'")

# Fix the fused 'Performer: Deal? WHAT THOSE LINES...'
must_replace(
    "Performer: Deal? WHAT THOSE LINES ARE REALLY DOING</p>",
    "Performer: Deal?</p><h3>What Those Lines Are Really Doing</h3>",
    label="Ch27: split Performer/heading fusion",
)
maybe_replace(
    '<p>“DO NOT LET ME IN YOUR HEAD”</p>',
    '<h3>“Do Not Let Me In Your Head”</h3>',
    label="Ch27: 'DO NOT LET ME IN YOUR HEAD'",
)
maybe_replace(
    "<p>THE POWER OF “CHANGE IT”</p>",
    "<h3>The Power of “Change It”</h3>",
    label="Ch27: Change It",
)

# Ch 28 — Digital Pre-show
must_replace("coffe", "coffee", label="Ch28: coffe→coffee")
must_replace("Austrailia", "Australia", label="Ch28: Austrailia→Australia")
# Remove orphan W and ⚠ glyph paragraphs
maybe_replace(
    '<div class="chapter-body">\n    <p>W</p>',
    '<div class="chapter-body">\n    ',
    label="Ch28: remove orphan W",
)
maybe_replace("<p>W</p><p>", "<p>", label="Ch28: orphan W (alt)")
maybe_replace("<p>⚠</p>", "", label="Ch28: orphan ⚠")

# Split fused Sources/Social Media
must_replace(
    "<p>The Sources Social Media: The Primary Surface</p>",
    "<h3>The Sources</h3><h4>Social Media: The Primary Surface</h4>",
    label="Ch28: split Sources/Social Media",
)
maybe_replace("<p>Public Records</p>", "<h3>Public Records</h3>", label="Ch28: Public Records")
maybe_replace("<p>The Event Contact: Your Most Useful Source</p>", "<h3>The Event Contact: Your Most Useful Source</h3>", label="Ch28: Event Contact")
maybe_replace("<p>The Social Graph: Finding People Through People</p>", "<h3>The Social Graph: Finding People Through People</h3>", label="Ch28: Social Graph")

# Ch 28 cross-reference: defer the Ch17→Ch15 swap; flag for manual review instead
maybe_replace(
    "<h3>See Also</h3>",
    "<h3>See Also</h3><!-- TODO[AUDIT]: Verify chapter cross-references in this section. Audit suggested Ch17→Ch15 swap for the Closing the Barn Door reference. -->",
    label="Ch28: See Also TODO marker",
)

# Ch 29 — Performance Arc
maybe_replace(
    "□Thank-you and follow ups designed and ready to send within 24 hours|",
    "Thank-you and follow ups designed and ready to send within 24 hours.",
    label="Ch29: stray |",
)
maybe_replace("Shoe recap", "Show recap", label="Ch29: Shoe→Show")

ch29_subheaders = ["PRE-SHOW PRIMING", "ATTENTION ARCHITECTURE", "TENSION AND RELEASE", "MEMORY ENCODING"]
for h in ch29_subheaders:
    maybe_replace(f"<p>{h}</p>", f"<h4>{title_case(h)}</h4>", label=f"Ch29: {h}")

# Ch 31 — Patter
must_replace("Tthe words are not the performance.", "The words are not the performance.", label="Ch31: Tthe→The")
maybe_replace("<p>Semantic Satiation</p>", "<h3>Semantic Satiation</h3>", label="Ch31: Semantic Satiation")
maybe_replace("<p>Silence as a Tool- The Instruction Pause</p>", "<h3>Silence as a Tool — The Instruction Pause</h3>", label="Ch31: Silence as a Tool")
maybe_replace("<p>Movement and Stillness Stillness for Reveals</p>", "<h3>Movement and Stillness</h3><h4>Stillness for Reveals</h4>", label="Ch31: split Movement/Stillness")

# Recovery levels to h4
for lvl in ["Level 1 — Reframe", "Level 2 — Hedge", "Level 3 — Pivot", "Level 4 — Graceful Exit"]:
    maybe_replace(f"<p>{lvl}</p>", f"<h4>{lvl}</h4>", label=f"Ch31: {lvl}")

# Flag missing matrix
maybe_replace(
    "<h3>The Performance Decision Matrix</h3><p>This matrix maps environment type to demonstration approach to volunteer strategy",
    "<h3>The Performance Decision Matrix</h3>"
    "<!-- TODO[CONTENT GAP]: The matrix table itself is missing here — only the prose intro exists. Insert the environment × demonstration × volunteer-strategy matrix. -->"
    "<p>This matrix maps environment type to demonstration approach to volunteer strategy",
    label="Ch31: flag missing Performance Decision Matrix",
)

# Ch 32 — When the Room Rises
must_replace("A standing ovation’s are predictable.", "Standing ovations are predictable.", label="Ch32: ovation's")
maybe_replace("<p>Peak vs. Close</p>", "<h3>Peak vs. Close</h3>", label="Ch32: Peak vs Close")

# Ch 34 — Make Room Say Yes
for h in ["48 Hours Before", "24 Hours Before", "Day of Show", "First 60 Seconds"]:
    maybe_replace(f"<p>{h}</p>", f"<h4>{h}</h4>", label=f"Ch34: {h}")

maybe_replace(
    "<p>Compliance History Compliance Temperature</p>",
    "<h3>Compliance History</h3><h4>Compliance Temperature</h4>",
    label="Ch34: split Compliance History/Temperature",
)
maybe_replace(
    "<p>BEHAVIORS THAT READ AS SAFE AND STRONG</p>",
    "<h3>Behaviors That Read As Safe and Strong</h3>",
    label="Ch34: Behaviors That Read",
)

# Ch 37 — FATE
for letter, name in [("F", "FOCUS"), ("A", "AUTHORITY"), ("T", "TRIBE"), ("E", "EMOTION")]:
    maybe_replace(f"<p>{letter} — {name}</p>", f"<h3>{letter} — {name}</h3>", label=f"Ch37: FATE letter {letter}")

maybe_replace("<p>The Three Tribal Drives</p>", "<h3>The Three Tribal Drives</h3>", label="Ch37: Three Tribal Drives")

# Remove orphan PART FIVE / INTERLUDE markers if they appear at end of Ch 37
maybe_replace("<p>PART FIVE · INTERLUDE</p><p>INTERLUDE</p>", "", label="Ch37: orphan PART FIVE/INTERLUDE")
maybe_replace("<p>PART FIVE · INTERLUDE</p>", "", label="Ch37: orphan PART FIVE")
maybe_replace("<p>INTERLUDE</p>", "", label="Ch37: orphan INTERLUDE")

# Ch 39 — speech patterns
maybe_replace("<p>Five Speech Patterns That Build Instant Authority</p>", "<h3>Five Speech Patterns That Build Instant Authority</h3>", label="Ch39: Five Speech Patterns")

# Ch 40 — Compliance vs Internalization
maybe_replace("<p>Compliance vs. Internalization</p>", "<h3>Compliance vs. Internalization</h3>", label="Ch40: Compliance vs Int.")

# Ch 41 — Authority Frame
must_replace("A uthority is not something you claim.", "Authority is not something you claim.", label="Ch41: A uthority")
maybe_replace("<p>The Five Authority Signals</p>", "<h3>The Five Authority Signals</h3>", label="Ch41: Five Authority Signals")

# Ch 42 — Authority Architecture
maybe_replace("<p>The Five Pillars of Authority Architecture</p>", "<h3>The Five Pillars of Authority Architecture</h3>", label="Ch42: Five Pillars")
maybe_replace(
    "<p>THE STANDING OVATION</p>",
    "",
    label="Ch42: orphan THE STANDING OVATION",
)
maybe_replace("<p>✦</p>", "", label="Ch42: orphan ✦")


# ========================================================================
# GLOBAL SWEEPS
# ========================================================================
print("\n== Global sweeps ==")
# Double spaces inside paragraphs (very conservative — only inside <p> tags is hard,
# so do general but only when bordered by word chars to avoid breaking style)
# We'll target specific known double-space patterns rather than blanket.
double_space_patterns = [
    ("only YOU  can provide", "only YOU can provide"),
    ("Jeff Hobson is in applying them.", "Jeff Hobson is applying them."),
]
for old, new in double_space_patterns:
    maybe_replace(old, new, label=f"Global double-space/typo: {old[:40]}…")

# Final write
SRC.write_text(content, encoding="utf-8")
print(f"\nWrote {SRC} — {len(content)} chars (was {len(original)}).")
print(f"Net change: {len(content) - len(original):+d} chars.")
