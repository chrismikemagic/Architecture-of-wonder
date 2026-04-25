"""
Insert "The Method Is Not the Point" as new CHAPTER 1.
Old CHAPTER 1 → CHAPTER 2, all subsequent chapters shift +1.
Updates manuscript-extracted.txt and build-book.py.
"""
import re, shutil

NEW_CHAPTER_TEXT = """\
CHAPTER 1
The Method Is Not the Point
I was nearly done writing this book when I had a conversation with Colin Cloud.
By that point, most of what you are about to read already existed in some form. The behavioral frameworks. The performance craft chapters. The systems for making mentalism feel real in ways that most performers never reach. I had spent years building this material and months putting it into a form worth handing to someone.
And then Colin said something that I felt needed to come before all of it.
So I put this chapter here.
This book is going to give you a new world of method.
Techniques used by the best performers in the world. Behavioral systems that have never been explained in this way before. Frameworks for using mentalism with a level of realism and precision that most performers never reach. You are going to walk away with things that will change how you work.
And none of it will save you if you do not understand what this chapter is saying.
Colin was on tour with The Illusionists, a full-scale theater production that has played some of the largest stages in the world, night after night, with a rotating cast of elite performers. He was surrounded, every night, by people at the top of the field.
And the two best performances he ever watched had nothing to do with methods.
The first was Jeff Hobson doing the egg bag.
The egg bag is not a new trick. It is not even a relatively new trick. It is one of the oldest pieces of apparatus in all of magic, a routine with roots stretching back centuries. Any working magician knows it. Most have access to how it works. The method is not hidden from the performing community.
And yet Colin watched it tear the entire show down.
Not because the method was stronger than anything else on the bill. Because Jeff Hobson is a character. Because what he does with that bag is not a magic trick. It is a piece of theater built around a specific human being, performed so completely and with such genuine craft that it does not matter what is inside the bag. You are watching a person who has become an irreplaceable presence in that moment. Magicians watched it. Laypeople watched it. Everyone watched it the same way. With joy. With full attention. With a feeling that something real was happening.
The second was Dave Williamson doing the Rocky Raccoon act with four kids on stage.
If you have seen it, you already know. If you have not, what you need to understand is this: the method is not the point. What is happening on that stage is a human being creating a small world, and pulling four children and a few hundred strangers into it for several minutes, and making something that cannot be reduced to a method or a gimmick or a move. Colin watched it more than once over the course of that tour. He said each time, it took the show.
Think about what that means. You are on stage with some of the most technically accomplished performers alive. People with acts built on extraordinary skill, original material, and years of refinement. And the piece that tears the show is a routine everyone in the field already knows. The methods are simple. The prop is straightforward.
What wins is not the method. What wins is the performer.
This is uncomfortable for a lot of people to sit with, because it sounds like it is arguing against learning. It is not.
What it is arguing against is the belief that the next strong method is what is standing between you and a great career. That if you had better material, more original ideas, more protected methods, everything would change.
It will not change. Not on its own.
The method is the vehicle. It matters that the vehicle runs. But a car that drives perfectly is still not a destination.
This book is going to give you the vehicle.
We will cover techniques used by the best performers working today, explained in a way they have not been explained before. You will learn how behavioral profiling changes what is possible in a performance. You will learn systems for making mentalism feel real that most performers never encounter, let alone master. You will learn how to construct effects that land with a force that has nothing to do with luck. These things matter. They are worth learning. The material in these pages represents years of applied work across corporate stages, government contracts, and live performance at every scale.
But you are also going to learn the other half.
Because if you cannot create a genuine connection with the person in front of you, and with the room around them, the method will perform for a stranger. It will not move anyone. And a performance that does not move people is just a demonstration. Demonstrations are forgettable.
In Part Five we are going to get specific about the psychological mechanics of connection. How interest is triggered, how trust is built in real time, how to make a room feel like it belongs to the moment rather than just observing it. These are not vague performance principles. They are learnable. They are repeatable. They work.
But even before we get there, understand this now: the work you are about to do means nothing if you are doing it from behind glass. The methods in this book are tools. The performer using them is either in the room or they are not. Jeff Hobson is in the room. Dave Williamson is in the room. You can feel it before they say a word.
That is what this book is ultimately building toward.
Not just better methods. A more complete performer.
The methods come first. The connection makes them mean something.
· · ·
"""

# ─── Manuscript ───────────────────────────────────────────────────────────────

with open('manuscript-extracted.txt', 'r', encoding='utf-8') as f:
    ms = f.read()

# Step 1: Renumber body CHAPTER N → CHAPTER N+1 (high→low to avoid collisions).
# Body uses uppercase "CHAPTER N" on its own line; TOC uses lowercase "Chapter N".
# We match "\nCHAPTER {n}\n" to avoid touching inline references.
for n in range(39, 0, -1):
    ms = ms.replace(f'\nCHAPTER {n}\n', f'\nCHAPTER {n+1}\n')

# Step 2: Insert new chapter before the renumbered CHAPTER 2 (old Ch1 intro).
# The old CHAPTER 1 is now CHAPTER 2.
insert_before = '\nCHAPTER 2\nOn Being the Person Who Admits What They Do\n'
if insert_before not in ms:
    raise ValueError("Could not find insertion point — check manuscript")
ms = ms.replace(insert_before, f'\n{NEW_CHAPTER_TEXT}\n{insert_before[1:]}', 1)

# Step 3: Update TOC.
# (a) "INTRODUCTION  —  On Being the Person" → "Chapter 2  —  On Being the Person"
ms = ms.replace(
    'INTRODUCTION  —  On Being the Person Who Admits What They Do',
    'Chapter 2  —  On Being the Person Who Admits What They Do',
)
# (b) TOC's "Chapter N  —" (lowercase) shift +2, high→low.
for n in range(43, 0, -1):
    ms = ms.replace(f'Chapter {n}  —  ', f'Chapter {n+2}  —  ')
# (c) Insert new Chapter 1 entry before the now-shifted "Chapter 3  —  Designing for Reality".
toc_new_entry = (
    'Chapter 1  —  The Method Is Not the Point\n'
    'Methods are the vehicle. The performer is the destination. Why Colin Cloud\'s two favorite performances had nothing to do with method.\n'
    'Chapter 2  —  On Being the Person Who Admits What They Do\n'
)
ms = ms.replace(
    'Chapter 2  —  On Being the Person Who Admits What They Do\n',
    toc_new_entry,
    1,
)

with open('manuscript-extracted.txt', 'w', encoding='utf-8') as f:
    f.write(ms)

print("manuscript-extracted.txt updated.")

# ─── build-book.py ────────────────────────────────────────────────────────────

with open('build-book.py', 'r', encoding='utf-8') as f:
    bb = f.read()

# Step 1: Shift 'CHAPTER N' string keys from 39→40 down to 1→2.
for n in range(39, 0, -1):
    bb = bb.replace(f"'CHAPTER {n}'", f"'CHAPTER {n+1}'")
    bb = bb.replace(f'"CHAPTER {n}"', f'"CHAPTER {n+1}"')

# Step 2: Also update CHAPTER refs inside string values / comments (e.g. FIGURES keys use them).
# The above already handles quoted keys; also handle inline mentions in comments.
for n in range(39, 0, -1):
    # Comment lines like: # ── CHAPTER 2: Designing for Reality ──
    bb = bb.replace(f'# ── CHAPTER {n}:', f'# ── CHAPTER {n+1}:')
    bb = bb.replace(f'# On Being the Person', f'# On Being the Person')  # no-op placeholder

# Step 3: Shift WHAT_YOU_JUST_DID integer keys {3,7,15,21,28,36} → {4,8,16,22,29,37}
wyajd_shifts = [(36, 37), (28, 29), (21, 22), (15, 16), (7, 8), (3, 4)]
for old, new in wyajd_shifts:
    # Match the key pattern: "    N: " at the start of a WYAJD entry
    bb = re.sub(rf'(\n    ){old}(:)', rf'\g<1>{new}\g<2>', bb)

# Also update the in-text "Chapter Two" reference inside WHAT_YOU_JUST_DID to "Chapter Three"
bb = bb.replace(
    'Chapter Two taught you this. The book just demonstrated it.',
    'Chapter Three taught you this. The book just demonstrated it.',
)

# Step 4: Add new CHAPTER 1 entries.

# HOOK_LINES — insert after the opening brace
new_hook = "    'CHAPTER 1':  '\"Colin Cloud said something I have not been able to stop thinking about.\"',\n"
bb = bb.replace(
    "HOOK_LINES = {\n",
    f"HOOK_LINES = {{\n{new_hook}",
)

# KEY_READS — insert after opening brace (no key read yet; use a placeholder)
# (User can fill this in later; leave absent for now — build script handles missing keys gracefully)

# CHAPTER_LEGEND — insert after opening brace
new_legend = "    'CHAPTER 1':  {'tiers': ['t1'],             'cats': ['am']},          # The Method Is Not the Point\n"
bb = bb.replace(
    "CHAPTER_LEGEND = {\n",
    f"CHAPTER_LEGEND = {{\n{new_legend}",
)

with open('build-book.py', 'w', encoding='utf-8') as f:
    f.write(bb)

print("build-book.py updated.")
print("Done. Run: python build-book.py && python build-gated.py")
