#!/usr/bin/env python3
"""Expand thin Part 7 chapters and add key cross-references throughout."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('manuscript-extracted.txt', encoding='utf-8') as f:
    content = f.read()

changes = 0

# ─── 1. Expand Ch38 (Building a Career) — add actionable content ─────────────
CH38_EXPANSION = """
The Three Questions Before Every Show
Before any engagement — strolling set, keynote, private consultation — three client questions are worth having answered before the first conversation ends.

What does success look like to you tonight? This is not logistics. It is outcome. The performer who knows what success means to the person who hired them can design toward it. The one who does not is guessing.

Who in the room will be watching the client's reaction most closely? Every corporate event has at least one person whose opinion the client values more than the rest. If the right person has a strong response, the booking becomes a story the client tells at the next event. If the wrong person is flat, the same show becomes a quiet disappointment nobody quite names.

What would make this a story they tell for the next five years? That question tells you more about the client's emotional vocabulary than anything else they say in the meeting. The words they use to answer it are the words you build the show around.

These questions are not formulas. They are genuine information-gathering, treated as exactly that. The goal is not to seem invested. The goal is to actually be invested — which is the only version that produces the result.

Pricing Without Apologizing
Price is a behavioral signal before it is an economic one. The moment you introduce your fee, the client's nervous system runs a rapid unconscious evaluation: does this person believe what they are charging? That evaluation happens in seconds, before reasoning has time to engage.

State the fee. Stop. Do not explain it. Do not follow it with a qualifier. The pause after a fee is not rejection forming — it is a calculation running. Let it run.

The performers who consistently command the highest fees are not always the most technically gifted. They are the ones who stated their number with the same certainty they would use to state their own name. That certainty is itself an authority signal. It tells the client's limbic system: this person knows exactly what this is worth, which means they know exactly what they are doing.

"""

CH38_ANCHOR = ("People refer performers to protect their own reputation. They refer someone they would stake their professional credibility on. Build the relationship completely, before, during, and after, and the referral becomes a natural extension of the relationship, not an ask.\n"
               "· · ·\n"
               "\n"
               "CHAPTER 39")

if CH38_ANCHOR in content:
    content = content.replace(
        CH38_ANCHOR,
        ("People refer performers to protect their own reputation. They refer someone they would stake their professional credibility on. Build the relationship completely, before, during, and after, and the referral becomes a natural extension of the relationship, not an ask.\n"
         + CH38_EXPANSION +
         "· · ·\n"
         "\n"
         "CHAPTER 39"),
        1
    )
    print("Ch38 expansion inserted.")
    changes += 1
else:
    print("Ch38 ANCHOR NOT FOUND")
    idx = content.find("Build the relationship completely, before, during, and after")
    if idx >= 0:
        print(f"  Partial at char {idx}")

# ─── 2. Expand Ch39 (The Intro Video) — add video scripting detail ──────────
CH39_EXPANSION = """
Writing the Intro Video Script
The sixty-to-ninety second intro video is the most cost-effective authority investment available to a working performer. It is also one of the most commonly miswritten.

Most intro videos fail for the same reason most bios fail: they are written from the performer's perspective rather than the client's psychology. They list credits. They describe the performer. They fail to answer the only question the audience is actually asking in that moment: is this going to be worth my next hour?

A strong intro video script follows four moves in sequence:

One: name a problem the audience recognizes. Not generic ('communication is hard') but specific to this audience, this organization, this moment. The audience's attention activates when they hear themselves described.

Two: reframe that problem as something that can be solved behaviorally — not with tips and tools, but through genuine understanding of how people actually work. This is where your credibility enters, not as biography, but as demonstrated perspective.

Three: introduce the experience. Not what you are going to do. What they are going to feel. Outcome language, not technique language. 'By the end of this session, several of you will not be able to look at the person sitting next to you the same way.' That is a promise worth leaning forward for.

Four: close on specificity. Name the company. Reference the event. Use language that is clearly not generic. The moment the audience hears something specific to their organization, the attention that was ambient becomes focused. They are in the room. They are the subject.

The video ends. The room is looking at where you are about to appear. That is when you enter. Not into an empty room waiting for a performer — into a room that is already inside the beginning of an experience you designed.

What the Video Is Not For
The intro video is not your highlight reel. It is not where you prove your credentials. Those things belong in the marketing conversation, earlier in the process, before the event. By the time the video plays, the booking has been made. The decision has been confirmed. The video's job is not to sell you — it is to prime the room to receive you at the level you belong.

"""

CH39_ANCHOR = ("The video ends. There is a beat of silence. Then you enter. That silence is part of the design. Do not fill it.\n"
               "The Pre-Entry Architecture")

if CH39_ANCHOR in content:
    content = content.replace(
        CH39_ANCHOR,
        ("The video ends. There is a beat of silence. Then you enter. That silence is part of the design. Do not fill it.\n"
         + CH39_EXPANSION +
         "The Pre-Entry Architecture"),
        1
    )
    print("Ch39 expansion inserted.")
    changes += 1
else:
    print("Ch39 ANCHOR NOT FOUND")
    idx = content.find("The video ends. There is a beat of silence.")
    if idx >= 0:
        print(f"  Partial at char {idx}")

# ─── 3. Add cross-reference at end of Ch1 (Designing for Reality) → Ch2 ──────
CH1_XREF = """
See Also
The three brain properties in this chapter — cognitive economy, metabolic efficiency, and predictive processing — each map to specific tools in Part Two. Cognitive economy is the engine behind the T1 signal tier in Chapter 7. Predictive processing is the mechanism that makes pacing and leading (Chapter 16) function. Metabolic efficiency is why the Barn Door (Chapter 17) closes faster than most performers think it opens. Reading Part One and Part Two together reveals the why behind every what.

"""

CH1_XREF_ANCHOR = ("Predictive processing applies not just to your audience but to you. The frame you hold going into any performance shapes what you perceive and what you miss. Build accurate predictions and update them in real time. Your read of the room is only as good as the model you are running.\n"
                   "· · ·")

if CH1_XREF_ANCHOR in content:
    content = content.replace(
        CH1_XREF_ANCHOR,
        ("Predictive processing applies not just to your audience but to you. The frame you hold going into any performance shapes what you perceive and what you miss. Build accurate predictions and update them in real time. Your read of the room is only as good as the model you are running.\n"
         + CH1_XREF +
         "· · ·"),
        1
    )
    print("Ch1 cross-reference inserted.")
    changes += 1
else:
    print("Ch1 xref ANCHOR NOT FOUND")
    idx = content.find("The frame you hold going into any performance")
    if idx >= 0:
        print(f"  Partial at char {idx}")

# ─── 4. Add cross-reference in Ch9 (Volunteer Types) → Ch7 and Ch8 ──────────
VOL_XREF = """
Cross-Reference
The seven volunteer types here are the behavioral output of the DISC profiles in Chapter 8. The signals that identify each type — posture, gaze pattern, social orientation, response to unexpected events — are drawn from the VS (Verbal/Social) category of the 80-Signal System in Chapter 7. Run the 10-Second Scan before any volunteer interaction and the type often surfaces before you have spoken. The selection becomes a read, not a guess.

"""

VOL_XREF_ANCHOR = "Seven Volunteer Types\nMost volunteer failures are selection failures."

if VOL_XREF_ANCHOR in content:
    content = content.replace(
        VOL_XREF_ANCHOR,
        VOL_XREF + "Seven Volunteer Types\nMost volunteer failures are selection failures.",
        1
    )
    print("Volunteer cross-reference inserted.")
    changes += 1
else:
    print("Volunteer xref ANCHOR NOT FOUND")
    idx = content.find("Most volunteer failures are selection failures")
    if idx >= 0:
        print(f"  Partial at char {idx}")

# ─── 5. Add cross-reference at DECODE preview → Ch31 ─────────────────────────
DECODE_XREF = """
How to Use DECODE
The DECODE framework appears in two places in this book. Here, as an orientation map — a spine to hang the methods on as you read Part Three. And again in Chapter 31, where each step is broken down into specific behavioral tools: what to look for, how to read it, and how to move from raw observation to installed experience. When you return to Chapter 31, the framework will feel familiar because you will have been practicing its components for several chapters.

"""

DECODE_XREF_ANCHOR = ("Every method in Part Three feeds one or more of these steps. Cold reading feeds Decode and Elevate. Contact work feeds Engage and Calibrate. Compliance language runs across all six. When you return to DECODE in Chapter 31, it will feel familiar because you will have been practicing its components.\n"
                      "\n"
                      "PART THREE")

if DECODE_XREF_ANCHOR in content:
    content = content.replace(
        DECODE_XREF_ANCHOR,
        ("Every method in Part Three feeds one or more of these steps. Cold reading feeds Decode and Elevate. Contact work feeds Engage and Calibrate. Compliance language runs across all six. When you return to DECODE in Chapter 31, it will feel familiar because you will have been practicing its components.\n"
         + DECODE_XREF +
         "\nPART THREE"),
        1
    )
    print("DECODE cross-reference inserted.")
    changes += 1
else:
    print("DECODE xref ANCHOR NOT FOUND")
    idx = content.find("When you return to DECODE in Chapter 31, it will feel familiar")
    if idx >= 0:
        print(f"  Partial at char {idx}")

with open('manuscript-extracted.txt', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/5 changes applied. Done.")
