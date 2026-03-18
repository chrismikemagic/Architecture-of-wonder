#!/usr/bin/env python3
"""Insert chapter-end consolidation boxes, pre-show checklist, compliance cross-ref, and WYHFB improvements."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('manuscript-extracted.txt', encoding='utf-8') as f:
    content = f.read()

changes = 0

# ─── 1. Ch7 (80-Signal) chapter-end consolidation ───────────────────────────
CH7_CONSOLIDATION = """
What You Now Have
The 80-Signal System is not a reading list. It is a behavioral vocabulary — the difference between noticing something and knowing what you noticed.

Before this chapter, you could see. After this chapter, you can read. The signals are the words. The Six-Category Radar is the grammar. The 10-Second Scan is the sentence you run every time you enter a room.

Three things to practice before the next show:
Run a full 10-Second Scan on the next group you enter — coffee shop, meeting, lobby. No performance stakes. Just data.
The next time someone speaks to you, track which category their strongest signal falls into: posture, gaze, gesture, proxemics, touch, or micro.
After your next performance, name three specific signals you observed that shaped a decision you made.

The signals do not wait for you to be ready. They are running now, in the people around you, whether you are reading them or not.

"""

CH7_ANCHOR = ("First you collect. Then you group. Then you adjust.\n"
              "\n"
              "· · ·")

if CH7_ANCHOR in content:
    content = content.replace(
        CH7_ANCHOR,
        "First you collect. Then you group. Then you adjust.\n" + CH7_CONSOLIDATION + "· · ·",
        1
    )
    print("Ch7 consolidation inserted.")
    changes += 1
else:
    print("Ch7 ANCHOR NOT FOUND")
    idx = content.find("First you collect. Then you group. Then you adjust.")
    if idx >= 0:
        print(f"  Partial found at {idx}: {repr(content[idx:idx+100])}")

# ─── 2. Cold Reading chapter-end consolidation ───────────────────────────────
COLDREAD_CONSOLIDATION = """
What You Now Have
Cold reading is not one technique. It is a layered observational system in which each layer — collocation, modality, Barnum framing, thin-slicing — adds a different kind of specificity to the same fundamental act: returning to a person what you observed in them so accurately that the observation feels impossible.

The Forer effect gives you the room's willing credulity. Warm reading gives you confirmation without exposure. Thin-slicing gives you reads from signals you could not have manufactured. Collocation gives you the architecture of how someone privately thinks.

Together, these four tools move a reading from "accurate" to "unforgettable."

The consolidation test: after your next cold reading, ask yourself these three questions:
Which observation was T1 — grounded in something physically observable? Which was T2 — research-backed behavioral pattern? Which was T3 — field-tested intuition from experience?

If every read was T3, the reading was guesswork. If every read was T1, it may have lacked emotional resonance. The strongest readings use all three in sequence, ascending in intimacy as the session deepens.

"""

COLDREAD_ANCHOR = ("Collocation is not a technique you announce. You do not say 'I noticed you keep putting these two words together.' You listen. You identify the fused concepts. You deliver the read as if you perceived it directly. Because you did. The audience hears insight. They do not hear linguistics. The mechanism disappears. The perception remains.\n"
                   "\n"
                   "· · ·")

if COLDREAD_ANCHOR in content:
    content = content.replace(
        COLDREAD_ANCHOR,
        ("Collocation is not a technique you announce. You do not say 'I noticed you keep putting these two words together.' You listen. You identify the fused concepts. You deliver the read as if you perceived it directly. Because you did. The audience hears insight. They do not hear linguistics. The mechanism disappears. The perception remains.\n"
         + COLDREAD_CONSOLIDATION +
         "· · ·"),
        1
    )
    print("Cold Reading consolidation inserted.")
    changes += 1
else:
    print("Cold Reading ANCHOR NOT FOUND")
    idx = content.find("Collocation is not a technique you announce")
    if idx >= 0:
        print(f"  Partial found at {idx}: {repr(content[idx:idx+100])}")

# ─── 3. Pre-show master checklist (inserted before Part 5 or at Ch23 area) ──
PRESHOWCHECKLIST = """
The Pre-Show Master Checklist
The best show you can give happens before the lights come up. Every item on this list addresses a variable that, if left unmanaged, will surface during the performance at a cost that is always higher than the cost of handling it in advance.

This checklist is not a formality. It is the behavioral design layer that runs underneath everything the audience sees.

48 Hours Before
Room confirmation. Do you know the exact layout? Size of space, stage height, sightlines from the back, audio configuration. If you have not been in the room, request a photo or floorplan.
Pre-show communication sent. The event contact has received your confirmation email. It names something specific about this organization or audience. It is not a template.
Volunteer intelligence gathered. Who is the room leader? Who is the most skeptical person likely to be present? Who has a recent milestone — promotion, anniversary, project launch — that the room is aware of? Three names, three seats if possible.
Introduction prepared. Not your bio. A behavioral frame for the audience: what to expect, how to engage, what the experience is designed to produce. If you are using a video intro, it has been reviewed and sent.
24 Hours Before
Logistics confirmed. AV contact named. Load-in time confirmed. Any technical requirements communicated and acknowledged.
Show arc finalized. You know the opening effect, the first volunteer interaction, the peak, and the close. The order is not flexible after this point. Rehearsal is not run-throughs. It is running the internal architecture until the decisions are automatic.
Recovery lines ready. You have your Level 1, Level 2, Level 3, and Level 4 recovery protocols warmed up. A missed read on the night of the show is never the first time those lines have been spoken aloud.
Day of Show
Arrive with margin. Not exactly on time. You need time in the space before the audience enters. You need to walk the room, check the stage from the back row, speak to the AV technician, and have one quiet moment before anyone is watching.
Run the pre-entry sequence. AV briefed on cue. Client contact greeted — not for logistics, for relationship. Your own state assessed. Entry threshold identified and walked once.
10-Second Scan run on early arrivals. While the room fills, you are reading. Posture clusters. Social hierarchies. Who is already looking toward the stage. Who is the social anchor. The show is already running.
Volunteer positions confirmed mentally. You know where your pre-selected volunteers are sitting. If the room changed layout, you have updated your targeting. Pre-show intelligence is only useful if it is current.
First 60 Seconds
Know exactly what you will say before you say it. The opening is not improvised. The first line is the single highest-leverage sentence in the entire performance. It is written, reviewed, and delivered as if it cost you nothing — because by now, it did not.
The pre-show checklist is not about eliminating uncertainty. Uncertainty is part of the work. It is about eliminating the preventable failures — the logistics that surface mid-show, the volunteer who was never profiled, the introduction that handed the room to you facing the wrong direction. Handle everything on this list and what remains is performance. That is the only variable left.

· · ·
"""

# Insert the pre-show checklist before Part Five (after Ch24 ends)
PRESHOWCHECKLIST_ANCHOR = ("Compliance is not something you command in the moment. It is something you engineer before the moment arrives. By the time you are asking someone to do something difficult, all the work that makes that possible should already be done.\n"
                            "Mirror Neurons and Modeling")

if PRESHOWCHECKLIST_ANCHOR in content:
    content = content.replace(
        PRESHOWCHECKLIST_ANCHOR,
        (PRESHOWCHECKLIST +
         "Compliance is not something you command in the moment. It is something you engineer before the moment arrives. By the time you are asking someone to do something difficult, all the work that makes that possible should already be done.\n"
         "Mirror Neurons and Modeling"),
        1
    )
    print("Pre-show checklist inserted.")
    changes += 1
else:
    print("Pre-show checklist ANCHOR NOT FOUND")
    idx = content.find("Compliance is not something you command in the moment")
    if idx >= 0:
        print(f"  Partial found at {idx}: {repr(content[idx:idx+100])}")

# ─── 4. Compliance doctrine cross-reference ──────────────────────────────────
COMPLIANCE_XREF = """
The Compliance Thread
Compliance runs through three chapters of this book. Each one addresses a different layer of the same principle.

This chapter (The Architecture of Obedience) gives you the linguistic tools: pacing and leading, presupposition, yes sets, the four degrees of certainty. These are the moment-to-moment mechanics.

Making the Room Say Yes (Chapter 24 in this section) gives you the environmental design tools: mirror neurons, the compliance arc, the first-mover principle, how to engineer the room's willingness before you ask anything of it.

How Influence Actually Works (Chapter 29) gives you the underlying formula: Novelty + Authority = Influence. This is the architecture that makes compliance feel natural rather than manufactured.

Reading all three as a set is recommended. Each answers a different question. This chapter answers: what do you say? Chapter 24 answers: what do you build? Chapter 29 answers: why does any of it work?

"""

COMPLIANCE_ANCHOR = ("That is the real skill. Not making people say yes. Making yes feel inevitable.\n"
                     "\n"
                     "Most performers chase compliance after the interaction has already started.")

if COMPLIANCE_ANCHOR in content:
    content = content.replace(
        COMPLIANCE_ANCHOR,
        ("That is the real skill. Not making people say yes. Making yes feel inevitable.\n"
         + COMPLIANCE_XREF +
         "\nMost performers chase compliance after the interaction has already started."),
        1
    )
    print("Compliance cross-reference inserted.")
    changes += 1
else:
    print("Compliance ANCHOR NOT FOUND")
    idx = content.find("That is the real skill. Not making people say yes.")
    if idx >= 0:
        print(f"  Partial found at {idx}: {repr(content[idx:idx+100])}")

# ─── 5. Strengthen WYHFB opener for Ch28 (BTE / Performer's Signal Dictionary) ─
OLD_WYHFB_3096 = """What You Have Felt Before

You are watching someone and you know something is wrong before they say a word. Their posture shifted. The jaw tightened almost imperceptibly. The hands that were open on the table have curled inward. You noticed it before you had language for it and filed it as a feeling rather than an observation. What the Performer's Signal Dictionary gives you is the language — a precise vocabulary for the thing your nervous system already knew.

The Performer's Signal Dictionary gives you the language."""

NEW_WYHFB_3096 = """What You Have Felt Before

The interaction ended fifteen minutes ago and something is still unresolved. Not the words — the words were fine. Something underneath them. A pattern you caught in the way they moved when a specific topic arrived. A sequence of behaviors that was too consistent to be accidental and too fast to have been managed. Your nervous system filed it before your mind had a frame for it.

Every performer has had this experience. Most stop there — with the feeling but not the vocabulary. The BTE gives you the vocabulary. Not so you can explain what you noticed. So you can use it before it disappears.

The Performer's Signal Dictionary gives you the language."""

if OLD_WYHFB_3096 in content:
    content = content.replace(OLD_WYHFB_3096, NEW_WYHFB_3096, 1)
    print("WYHFB Ch28 (BTE) strengthened.")
    changes += 1
else:
    print("WYHFB Ch28 ANCHOR NOT FOUND")
    idx = content.find("You are watching someone and you know something is wrong before they say a word")
    if idx >= 0:
        print(f"  Partial found at {idx}: {repr(content[idx:idx+100])}")

# ─── 6. Strengthen WYHFB opener for Ch29 (Influence Equation) ────────────────
OLD_WYHFB_3204 = """What You Have Felt Before

A performer walks on stage and you are already leaning forward. Nothing has happened yet. No effect, no line, no moment worth reacting to. Something about the way they arrived — the way they stood, the quality of stillness, the way the room reorganized when they appeared — activated a response in your body before your mind had time to evaluate whether that response was warranted. That is not charisma. That is engineering.

That is the Influence Equation at work: novelty hijacking the dopamine circuit while authority activates the compliance shortcut. Together, they overwhelm the prefrontal cortex's skepticism filter before it has time to engage."""

NEW_WYHFB_3204 = """What You Have Felt Before

You have been in rooms where the performer was technically skilled and the room was politely attentive. And you have been in rooms where something different happened — where the attention was not polite but physical. Where people were not watching the performance but being pulled forward by it, involuntarily, before anything impressive had occurred. The difference between those two experiences is not talent. It is architecture.

The room that gets pulled forward was designed to. Before the first line, before the first effect, the conditions were set. Novelty running through the dopamine circuit. Authority registered by the limbic system. Skepticism deprioritized before it had a chance to organize. The audience was not won. They were positioned.

That is the Influence Equation at work: novelty hijacking the dopamine circuit while authority activates the compliance shortcut. Together, they overwhelm the prefrontal cortex's skepticism filter before it has time to engage."""

if OLD_WYHFB_3204 in content:
    content = content.replace(OLD_WYHFB_3204, NEW_WYHFB_3204, 1)
    print("WYHFB Ch29 (Influence Equation) strengthened.")
    changes += 1
else:
    print("WYHFB Ch29 ANCHOR NOT FOUND")
    idx = content.find("A performer walks on stage and you are already leaning forward")
    if idx >= 0:
        print(f"  Partial found at {idx}: {repr(content[idx:idx+100])}")

# ─── 7. Add recovery protocol cross-reference in contact mind reading ─────────
CMR_XREF = """
Recovery in Contact Work
Contact mind reading is the one method where a miss is immediately visible. Unlike a cold read — where you can reframe confidently and the audience experiences a refinement — a missed direction in muscle reading is physically apparent to anyone watching.

The recovery protocol from Chapter 21 applies, but contact work has its own specific version. If the direction misses: pause, reset the grip naturally, and redirect with 'Let me try this a different way — this time I want you to think about the direction, not the destination.' The reframe suggests precision, not correction. The audience reads recalibration as rigor. They saw you working more carefully, not working incorrectly.

"""

CMR_ANCHOR = ("Muscle reading, ideomotor response, hellstromism, contemporary motor imagery theory, or contact mind reading is something so mysterious to so many, and I am sure you are surprised to find it in a book like this.")

if CMR_ANCHOR in content:
    content = content.replace(
        CMR_ANCHOR,
        (CMR_XREF + "\n" + CMR_ANCHOR),
        1
    )
    print("Contact mind reading recovery cross-ref inserted.")
    changes += 1
else:
    print("CMR recovery ANCHOR NOT FOUND")

with open('manuscript-extracted.txt', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/7 changes applied. Done.")
