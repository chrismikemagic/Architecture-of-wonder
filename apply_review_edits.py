#!/usr/bin/env python3
"""Apply all review edits for VERSION FOR REVIEW build."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('manuscript-extracted.txt', encoding='utf-8') as f:
    content = f.read()

changes = 0

# ── 1. Soften dopamine→compliance claim (Ch. 4) ──────────────────────────────
OLD1 = ("The more dopamine you deliver to your audience, the more compliant and suggestible"
        " they will become. This is good for making fans, selling merch, booking more shows,"
        " and above all else giving them a better experience.")
NEW1 = ("The practical implication: sustained anticipation increases engagement, lowers"
        " cognitive resistance, and creates the neurological conditions for a more impactful"
        " performance. Dopamine's role here is motivational and attentional — it tags experience"
        " as worth attending to — rather than a simple lever that produces compliance. The"
        " relationship is probabilistic and context-dependent. What the design principle gives you"
        " is this: extend the build, and you extend the most productive neurological state"
        " available to the room. That is what makes fans, fills rooms, and produces the experiences"
        " people talk about afterward.")
if OLD1 in content:
    content = content.replace(OLD1, NEW1, 1)
    print("Change 1 done: dopamine claim softened (T3 framing)")
    changes += 1
else:
    print("Change 1 FAILED: string not found")
    # debug
    idx = content.find("The more dopamine you deliver")
    if idx >= 0:
        print(f"  Found partial match at {idx}: {repr(content[idx:idx+80])}")

# ── 2. Add ethics preview in intro ───────────────────────────────────────────
ETHICS_PREVIEW = (
    "\n\nA Note on Consent and Intended Use\n"
    "The attention mechanisms, compliance architecture, and influence frameworks in this"
    " book work whether the person using them intends the audience's benefit or not. That"
    " is worth stating directly. This book is written for performers who use these tools to"
    " create genuinely extraordinary experiences for people who have, by being in the room,"
    " implicitly consented to being surprised, moved, and temporarily managed. The full"
    " ethics framework is in Chapter 35. Read it — especially before deploying compliance"
    " or influence material in advisory, training, or consulting contexts where the power"
    " differential differs from a stage setting. The line between performance and manipulation"
    " is drawn by consent, context, and the performer's honest accounting of their own intent."
)

INTRO_ANCHOR = "The science is real. The application is immediate."
if INTRO_ANCHOR in content:
    content = content.replace(INTRO_ANCHOR, INTRO_ANCHOR + ETHICS_PREVIEW, 1)
    print("Change 2 done: ethics preview added to intro")
    changes += 1
else:
    print("Change 2 FAILED: intro anchor not found")

# ── 3. Add DECODE workflow preview before Part Three ─────────────────────────
DECODE_PREVIEW = (
    "\nThe Workflow That Ties This Together\n"
    "Before you move into the methods, it helps to name the framework that will unify"
    " everything you learn next. DECODE is covered in full in Chapter 31. The reason to"
    " know it now is that it gives you a spine to hang the methods on.\n"
    "D — Detect: observe before acting, establish baseline. E — Engage: position as peer,"
    " not performer. C — Calibrate: match pace and communication style. O — Observe: watch"
    " for hesitation, retreat, and evaluation signals. D — Decode: identify the real response"
    " beneath the surface behavior. E — Elevate: guide the experience to its natural conclusion.\n"
    "Every method in Part Three feeds one or more of these steps. Cold reading feeds Decode"
    " and Elevate. Contact work feeds Engage and Calibrate. Compliance language runs across all"
    " six. When you return to DECODE in Chapter 31, it will feel familiar because you will have"
    " been practicing its components.\n"
    "\n"
)

PART3_ANCHOR = ("PART THREE\nThe Methods\n"
                "Cold reading, contact mind reading, hypnosis, compliance language, and the core"
                " mentalism techniques — each made stronger by the behavioral foundation in Part Two.")
if PART3_ANCHOR in content:
    content = content.replace(PART3_ANCHOR, DECODE_PREVIEW + PART3_ANCHOR, 1)
    print("Change 3 done: DECODE preview added before Part Three")
    changes += 1
else:
    print("Change 3 FAILED: Part Three anchor not found")
    idx = content.find("PART THREE\nThe Methods")
    if idx >= 0:
        print(f"  Found at {idx}: {repr(content[idx:idx+100])}")

# ── 4. Expand Ch. 22 with Closer Design Protocol ─────────────────────────────
CLOSER_PROTOCOL = (
    "\nCloser Design Protocol\n"
    "Before you choose your closer, answer these five questions. They force the design"
    " decisions most performers leave to habit.\n"
    "One: What is the peak moment of this show — the moment of maximum emotional intensity"
    " — and where does it sit in the sequence? It should not be the last effect. If it is,"
    " you have no closer.\n"
    "Two: What do you want the audience to feel when the lights change? Not think. Feel."
    " The emotion of the final memory is the close's real output. Design backward from that.\n"
    "Three: Have you created collective framing before the close? The room must feel like a"
    " shared experience, not an audience of individuals, before social cascade can begin."
    " A callback to an earlier moment in the show is the fastest route.\n"
    "Four: Is the first person to stand in a predictable location? Front rows and people who"
    " have been leaning forward are your cascade starters. Proximity to them matters.\n"
    "Five: Does the close have a clear, unambiguous signal that it is over? Ambiguous endings"
    " suppress cascade. The room needs to know the moment has arrived.\n"
    "The peak handles emotional intensity. The close handles meaning. The cascade handles the"
    " room. They are three separate engineering problems.\n"
)

SONG_ANCHOR = (
    "The Song Anchor Technique\n"
    "A specific instrumental piece plays as you are introduced. Before you speak, before the"
    " audience has formed any impression. You deliver your opening line over it. The same piece"
    " plays again at the close, fully, as you deliver your final sequence. The emotional state"
    " the audience has accumulated across the entire performance becomes neurologically tethered"
    " to that audio. When it returns, the association fires. The accumulated weight of the"
    " evening arrives at once, at exactly the moment you need it.\n"
    "· · ·"
)
if SONG_ANCHOR in content:
    content = content.replace(SONG_ANCHOR,
        "The Song Anchor Technique\n"
        "A specific instrumental piece plays as you are introduced. Before you speak, before the"
        " audience has formed any impression. You deliver your opening line over it. The same piece"
        " plays again at the close, fully, as you deliver your final sequence. The emotional state"
        " the audience has accumulated across the entire performance becomes neurologically tethered"
        " to that audio. When it returns, the association fires. The accumulated weight of the"
        " evening arrives at once, at exactly the moment you need it.\n"
        + CLOSER_PROTOCOL +
        "· · ·",
        1)
    print("Change 4 done: Closer Design Protocol added to Ch. 22")
    changes += 1
else:
    print("Change 4 FAILED: Song Anchor section not found")
    idx = content.find("The Song Anchor Technique")
    if idx >= 0:
        print(f"  Found partial at {idx}: {repr(content[idx:idx+120])}")

# ── 5. Authority reconciliation note in Ch. 27 ───────────────────────────────
RECONCILE = (
    "\nTwo Systems, One Architecture\n"
    "Chapter 25 maps the Five Authority Signals — the external behavioral cues the room reads"
    " as authority before conscious evaluation: Certainty, Congruence, Presence, Composure, and"
    " Investment. Those are the outputs. What follows in this chapter is the input layer: the"
    " internal character traits that produce those signals under pressure, and collapse into"
    " performed authority when they are absent. The two systems are not competing frameworks."
    " They are the surface and the source. Strong internal pillars with weak external signals:"
    " the room cannot read what you actually have. Strong external signals with hollow internal"
    " pillars: the room will feel the crack — usually at the worst possible moment.\n"
)

AUTH_ANCHOR = ("The Five Pillars of Authority\n\n"
               "In Chapter 25, you encountered the Five Authority Signals")
if AUTH_ANCHOR in content:
    content = content.replace(AUTH_ANCHOR,
        "The Five Pillars of Authority\n" + RECONCILE + "\nIn Chapter 25, you encountered the Five Authority Signals",
        1)
    print("Change 5 done: authority reconciliation note added to Ch. 27")
    changes += 1
else:
    print("Change 5 FAILED: Ch. 27 anchor not found")
    idx = content.find("Five Pillars of Authority")
    if idx >= 0:
        print(f"  Found at {idx}: {repr(content[idx:idx+80])}")

with open('manuscript-extracted.txt', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nDone. {changes}/5 changes applied.")
