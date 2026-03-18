#!/usr/bin/env python3
"""Insert compliance opening sections into Ch16 Architecture of Obedience."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

NEW_INTRO = """Compliance
Every effect you perform depends on it. Not the method. Not the psychology. Compliance. The willingness of another person to follow your lead, enter your frame, and respond the way the architecture requires. A mentalist who understands the theory but cannot produce compliance in the room has a collection of ideas and nothing to show with them.

Compliance is not obedience. Obedience is what happens when someone does something because they were told to. Compliance is what happens when someone does something because it feels natural, easy, or like their own idea. The distinction matters enormously in performance. You do not want a room full of obedient participants. You want a room full of people who are moving in the direction you designed without knowing there was a direction at all.

That is the real skill. Not making people say yes. Making yes feel inevitable.

Most performers chase compliance after the interaction has already started. They ask a question, notice resistance, and try to recover. That is too late. The architecture of compliance begins before the first word is spoken, in the framing of the invitation, the tone of the approach, the design of the question. Every interaction either builds a compliance runway or consumes it. This chapter gives you the tools to build it deliberately.

Why Mentalists Need This More Than Anyone Else
A corporate trainer loses a resistant participant and moves on. A comedian heckles back. A motivational speaker powers through. A mentalist cannot do any of these things without the effect collapsing.

The mentalist's work is built on the voluntary participation of specific individuals whose cooperation is not optional. It is structural. Without compliance the architecture falls. The volunteer who freezes mid-effect, the participant who challenges the framing, the group that decides to treat the whole thing as a test of your credibility, these are not minor inconveniences. They are performance failures. And they are almost always preventable, because they almost always result from compliance failure that was already in motion before the critical moment arrived.

The performer who understands compliance does not recover from resistance. They design the interaction so resistance never finds purchase.

This is why the techniques in this chapter are not persuasion tactics. They are environmental design. You are building the conditions under which a specific kind of participation becomes the path of least resistance. The participant will still feel like they made a choice. That feeling is the point.

The Neuroscience of Compliance
Compliance has a biological architecture. Understanding it changes how you build the conditions for it.

The prefrontal cortex, the brain's executive decision-making region, is where deliberate evaluation happens. This is where "should I do this?" gets processed. What compliance architecture does at a neurological level is engage other systems before that evaluation starts. By the time the prefrontal cortex gets the question, the answer has already been shaped by several prior events.

When the brain encounters a sequence of undeniable, verifiable statements, it enters a processing rhythm where the cost of evaluating each new statement rises. By the third accurate observation in a row, the brain has already created an expectation of agreement. The next statement is processed in that context. Evaluation does not disappear, but the threshold for challenge rises. This is why yes sets work. They condition the evaluative system to expect agreement before the request that actually matters arrives.

The amygdala adds a second layer. Social threat, the fear of being wrong, looking foolish, or breaking from the group response, activates a mild amygdala response. That arousal narrows attentional bandwidth and increases social compliance. People in mildly elevated social-threat states follow social cues more readily. A well-managed room where the group is watching is more compliant than an inattentive one. The mild exposure that looks like a risk is also a compliance accelerant. Handle it correctly and it works for you.

Dopamine's anticipatory function is the third lever. A person in genuine anticipation, curious about what is about to happen, is in an active seeking state. That seeking system lowers evaluative resistance and increases openness to direction. An audience that wants to know what happens next is an audience that will follow where you lead. This is why building anticipation before asking for participation produces better compliance than asking cold.

The practical implication: compliance is not a persuasion problem. It is a design problem. The neurological conditions that produce willing, natural participation can be built before the interaction begins. The tools that follow are how you build them.

"""

with open('manuscript-extracted.txt', encoding='utf-8') as f:
    content = f.read()

ANCHOR = "That quiet movement from agreement to commitment, invisible while it is happening, is pacing and leading working exactly as designed.\nPacing and Leading\nPacing is the act of accurately"
REPLACEMENT = ("That quiet movement from agreement to commitment, invisible while it is happening,"
               " is pacing and leading working exactly as designed.\n"
               + NEW_INTRO +
               "Pacing and Leading\nPacing is the act of accurately")

if ANCHOR in content:
    content = content.replace(ANCHOR, REPLACEMENT, 1)
    print("Compliance intro inserted.")
else:
    print("ANCHOR NOT FOUND")
    idx = content.find("pacing and leading working exactly as designed")
    if idx >= 0:
        print(f"Partial found at {idx}: {repr(content[idx:idx+100])}")

with open('manuscript-extracted.txt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done.")
