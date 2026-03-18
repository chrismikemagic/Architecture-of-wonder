#!/usr/bin/env python3
"""Fix remaining issues: TOC renumber, Ch40 dup, Ch2 WYHFB, and Part 4/5/6 missing WYHFB."""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('manuscript-extracted.txt', encoding='utf-8') as f:
    content = f.read()

changes = 0

# ─── 1. TOC UPDATE — insert Ch10 (Tell Table) and renumber 10→43 ─────────────
# The manuscript uses em-dash \u2014 and curly quotes. Build the replacement
# by targeted replacements rather than one big block.

# First insert the new Chapter 10 entry (between Ch9 and what was Ch10)
CH10_INSERT = (
    "Chapter 10  \u2014  Chris Michael\u2019s Tell Table\n"
    "The in-performance behavioral reading tool. Green, yellow, and red signal clusters for real-time decisions.\n"
)
AFTER_CH9 = (
    "Seven volunteer types, the cortisol contract, and how to manage neurological state on stage.\n"
    "Chapter 10  \u2014  The Eyes, the Face, and the Way Thought Leaks Out"
)
NEW_AFTER_CH9 = (
    "Seven volunteer types, the cortisol contract, and how to manage neurological state on stage.\n"
    + CH10_INSERT
    + "Chapter 11  \u2014  The Eyes, the Face, and the Way Thought Leaks Out"
)
if AFTER_CH9 in content:
    content = content.replace(AFTER_CH9, NEW_AFTER_CH9, 1)
    print("TOC: Chapter 10 (Tell Table) inserted.")
    changes += 1
else:
    print("TOC Ch9→10 ANCHOR NOT FOUND")

# Now renumber all subsequent TOC chapters 11→12 through 42→43
# Do in reverse order to avoid double-replacing
toc_renames = [
    ("Chapter 42  \u2014  From First Contact", "Chapter 43  \u2014  From First Contact"),
    ("Chapter 41  \u2014  Reading the Booking Room", "Chapter 42  \u2014  Reading the Booking Room"),
    ("Chapter 40  \u2014  The Language of Authority", "Chapter 41  \u2014  The Language of Authority"),
    ("Chapter 39  \u2014  Introductions, Bios", "Chapter 40  \u2014  Introductions, Bios"),
    ("Chapter 38  \u2014  The Intro Video", "Chapter 39  \u2014  The Intro Video"),
    ("Chapter 37  \u2014  Building a Career", "Chapter 38  \u2014  Building a Career"),
    ("Chapter 36  \u2014  Where Bookings Are", "Chapter 37  \u2014  Where Bookings Are"),
    ("Chapter 35  \u2014  The Ethics of Influence", "Chapter 36  \u2014  The Ethics of Influence"),
    ("Chapter 34  \u2014  Influence Without Authority", "Chapter 35  \u2014  Influence Without Authority"),
    ("Chapter 33  \u2014  Why Most Training Fails", "Chapter 34  \u2014  Why Most Training Fails"),
    ("Chapter 32  \u2014  Mentalism in the Boardroom", "Chapter 33  \u2014  Mentalism in the Boardroom"),
    ("Chapter 31  \u2014  Six Steps from Observation", "Chapter 32  \u2014  Six Steps from Observation"),
    ("Chapter 30  \u2014  Insight Demonstrations", "Chapter 31  \u2014  Insight Demonstrations"),
    ("Chapter 29  \u2014  How Influence Actually Works", "Chapter 30  \u2014  How Influence Actually Works"),
    ("Chapter 28  \u2014  The Performer\u2019s Signal Dictionary", "Chapter 29  \u2014  The Performer\u2019s Signal Dictionary"),
    ("Chapter 27  \u2014  Authority Architecture", "Chapter 28  \u2014  Authority Architecture"),
    ("Chapter 26  \u2014  What the Room Decides", "Chapter 27  \u2014  What the Room Decides"),
    ("Chapter 25  \u2014  The Authority Frame", "Chapter 26  \u2014  The Authority Frame"),
    ("Chapter 24  \u2014  Making the Room Say Yes", "Chapter 25  \u2014  Making the Room Say Yes"),
    ("Chapter 23  \u2014  Audio as Architecture", "Chapter 24  \u2014  Audio as Architecture"),
    ("Chapter 22  \u2014  When the Room Rises", "Chapter 23  \u2014  When the Room Rises"),
    ("Chapter 21  \u2014  The Art of Strolling", "Chapter 22  \u2014  The Art of Strolling"),
    ("Chapter 20  \u2014  Patter, Rhythm, and Silence", "Chapter 21  \u2014  Patter, Rhythm, and Silence"),
    ("Chapter 19  \u2014  Method Invisibility", "Chapter 20  \u2014  Method Invisibility"),
    ("Chapter 18  \u2014  Turning Observation into Performance", "Chapter 19  \u2014  Turning Observation into Performance"),
    ("Chapter 17  \u2014  The Performance Arc", "Chapter 18  \u2014  The Performance Arc"),
    ("Chapter 16  \u2014  Closing the Barn Door", "Chapter 17  \u2014  Closing the Barn Door"),
    ("Chapter 15  \u2014  The Architecture of Obedience", "Chapter 16  \u2014  The Architecture of Obedience"),
    ("Chapter 14  \u2014  Contact Mind Reading", "Chapter 15  \u2014  Contact Mind Reading"),
    ("Chapter 13  \u2014  Cold Reading, Warm Reading", "Chapter 14  \u2014  Cold Reading, Warm Reading"),
    ("Chapter 12  \u2014  The Science of Hypnosis", "Chapter 13  \u2014  The Science of Hypnosis"),
    ("Chapter 11  \u2014  The Micro-Expression Matrix", "Chapter 12  \u2014  The Micro-Expression Matrix"),
    ("Chapter 10  \u2014  The Eyes, the Face", "Chapter 11  \u2014  The Eyes, the Face"),
]

toc_count = 0
for old, new in toc_renames:
    if old in content:
        content = content.replace(old, new, 1)
        toc_count += 1
    else:
        print(f"  TOC rename NOT FOUND: {old[:50]}")

print(f"TOC: {toc_count}/33 chapter renames applied.")
if toc_count > 0:
    changes += 1

# ─── 2. FIX Ch40 DUPLICATE SENTENCE (using exact Unicode chars found) ─────────
# The first copy has \u2019 (curly apostrophe), second has ' (straight)
DUP_FULL = (
    "A strong introduction creates borrowed certainty. A great introduction does something better still: it changes the audience\u2019s posture toward the experience before the first line is spoken. "
    "A strong introduction creates borrowed certainty. A great introduction does something better still: it changes the audience\u2019s posture toward the experience before the first line is spoken."
)
DUP_FIXED = (
    "A strong introduction creates borrowed certainty. A great introduction does something better still: it changes the audience\u2019s posture toward the experience before the first line is spoken."
)
if DUP_FULL in content:
    content = content.replace(DUP_FULL, DUP_FIXED, 1)
    print("Ch40 duplicate sentence fixed.")
    changes += 1
else:
    # Try the mixed-apostrophe version found in actual file
    DUP_MIXED = (
        "A strong introduction creates borrowed certainty. A great introduction does something better still: it changes the audience\u2019s posture toward the experience before the first line is spoken. "
        "A strong introduction creates borrowed certainty. A great introduction does something better still: it changes the audience\u2019s posture toward the experience before the first line is spoken."
    )
    # Try finding and replacing via index
    idx = content.find("A strong introduction creates borrowed certainty")
    if idx >= 0:
        segment = content[idx:idx+500]
        # Count occurrences in this window
        if segment.count("A strong introduction creates borrowed certainty") >= 2:
            end_pos = idx + segment.find("\nThe room is always ask")
            old_seg = content[idx:end_pos]
            # Replace with just the first occurrence
            first_end = old_seg.find("before the first line is spoken.") + len("before the first line is spoken.")
            new_seg = old_seg[:first_end]
            content = content[:idx] + new_seg + content[end_pos:]
            print("Ch40 duplicate fixed (fallback method).")
            changes += 1
        else:
            print("Ch40 duplicate: only one occurrence found — may already be fixed")
    else:
        print("Ch40 duplicate ANCHOR NOT FOUND completely")

# ─── 3. REWRITE Ch2 WYHFB (post typo-fix version) ────────────────────────────
OLD_CH2_WYHFB = (
    "What You Have Felt Before\n"
    "Something powerful, and rarely taught outside of covert operations is this: the moments that command human attention are not random. They follow patterns. Human behavior is constrained, and salience is not arbitrary. It\u2019s an uncomfortable truth. Human attention and behavior show lawful patterns. Human behavior may feel unpredictable, but it is not random. Let me have you read that again. Just as no triangle exists with a total sum of its angles exceeding 180 degrees, no human can be random. Human attention is structured, constrained, and responsive to causes. Attention, memory, emotion, context, incentives, habit, fatigue, social pressure, past experience, and biology, all shape what stimulates people, how they interpret those stimuli, and how they respond. What you can not control (in most cases) are habits, past experiences, and biology. What we can control as performers are attention, memory, emotion, context, incentives, habit, fatigue, and social pressure. We will discuss ethical ways to control those later in the book, but for now we will focus on attention.    The brain has a built-in priority system for deciding what deserves your attention first. Two important parts of that system are the anterior insula and the dorsal anterior cingulate cortex. You do not need to memorize those names. What matters is what they do. Together, they help form what is known as the salience network: the system that scans everything coming in and asks, What matters here? What is different? What might require attention right now? Out of the roughly eleven million bits of sensory information your nervous system is taking in each second, only a tiny fraction reaches conscious awareness. Even less will make it to the hypothalamus which controls the endocrine system which controls what we feel. The salience network helps decide what makes the cut. To a performer, that matters."
)

NEW_CH2_WYHFB = (
    "What You Have Felt Before\n"
    "The room is noise and motion and glasses clinking and nobody particularly interesting. Then your eyes move \u2014 not because you decided to look, but because something recalculated. Across the room, one person has gone still. Shoulders settled, chin level, not scanning for confirmation. In the middle of all that movement they appear as though they already belong here in a way the room has not caught up to yet. You are looking twice. So is everyone else.\n"
    "\n"
    "That was not an accident. It was physics.\n"
    "\n"
    "The moments that command human attention are not random \u2014 they follow lawful patterns. Human behavior is constrained. Salience is not arbitrary. Just as no triangle can have angles totaling more than 180 degrees, no human can be truly random. Attention, memory, emotion, context, habit, social pressure \u2014 all of it shapes what stimulates people and how they respond. The performer who understands that is not guessing at attention. They are engineering it.\n"
    "\n"
    "The brain has a built-in priority system for deciding what deserves your attention. The anterior insula and the dorsal anterior cingulate cortex work together to form the salience network: the system that scans everything coming in and asks what matters right now. Out of the roughly eleven million bits of sensory information your nervous system processes each second, only a tiny fraction reaches conscious awareness. The salience network decides what makes the cut.\n"
)

if OLD_CH2_WYHFB in content:
    content = content.replace(OLD_CH2_WYHFB, NEW_CH2_WYHFB, 1)
    print("Ch2 WYHFB rewritten.")
    changes += 1
else:
    # Search with the apostrophe variant that might be in the file
    idx = content.find("Something powerful, and rarely taught outside of covert operations")
    if idx >= 0:
        # Find the end of this paragraph (ends before "Five forces reliably activate")
        end_marker = "Five forces reliably activate this system."
        end_idx = content.find(end_marker, idx)
        # Find the "What You Have Felt Before" before this text
        wyhfb_idx = content.rfind("What You Have Felt Before", 0, idx)
        if wyhfb_idx >= 0 and end_idx >= 0:
            old_block = content[wyhfb_idx:end_idx]
            content = content[:wyhfb_idx] + NEW_CH2_WYHFB + content[end_idx:]
            print("Ch2 WYHFB rewritten (fallback method).")
            changes += 1
        else:
            print(f"Ch2 WYHFB: couldn't locate boundaries. wyhfb_idx={wyhfb_idx}, end_idx={end_idx}")
    else:
        print("Ch2 WYHFB: source text not found at all")

# ─── 4. ADD MISSING WYHFB FOR PART 4-5 CHAPTERS (using actual titles) ─────────
# Map: (body chapter number, title, wyhfb text)
wyhfb_to_add = [
    ("CHAPTER 19\nTurning Observation into Performance",
     "What You Have Felt Before\nYou had the read. The signal was clear, the conclusion was real, and you knew you were right. And then you did not know what to do with it. The observation sat in your hands like a tool with no obvious place to apply it. The gap between noticing and delivering is the gap between behavioral knowledge and performance. This chapter closes it.\n\n"),
    ("CHAPTER 20\nMethod Invisibility",
     "What You Have Felt Before\nYou watched something happen, replayed it immediately, and could not locate the seam. Not because it was fast. Not because you were not paying attention. Because the structure of what you were watching had been built specifically so that looking directly at it would tell you nothing. The method was not hidden. It was invisible because the architecture around it made it structurally undetectable. That is not a trick. That is engineering.\n\n"),
    ("CHAPTER 21\nPatter, Rhythm, and Silence",
     "What You Have Felt Before\nThe performer said something and it landed in the room with a weight that surprised you. The sentence itself was not extraordinary. But the silence before it was exactly right. The pause after it was exactly long enough. You felt the moment arrive before you understood why. Timing is not decoration. It is the primary delivery mechanism. The same sentence, differently timed, is a different sentence.\n\n"),
    ("CHAPTER 22\nThe Art of Strolling",
     "What You Have Felt Before\nSomeone approached your table at a dinner and within thirty seconds you forgot there had been a dinner. The room collapsed down to the four feet of space between you. Nobody had agreed to this. The conversation you were mid-sentence in dissolved. The performer did not ask for your attention. They arrived in a way that made attention the only available response. That is not charisma. That is the engineering of proximity, pacing, and first contact \u2014 all of which can be learned.\n\n"),
    ("CHAPTER 23\nWhen the Room Rises",
     "What You Have Felt Before\nThe applause started before anyone decided to stand. One person began to rise and the rest of the room followed in a wave you were part of before you chose to be. It felt unanimous because it felt spontaneous. It was neither. It was a cascade event \u2014 initiated at a specific moment, with a specific person, under specific conditions. A standing ovation is not the audience\u2019s decision. It is the performer\u2019s design. This chapter is that design.\n\n"),
    ("CHAPTER 24\nAudio as Architecture",
     "What You Have Felt Before\nYou walked into a room before a show and something was already happening. Not the performance \u2014 the music. And the music was setting something in you that you did not consciously agree to. By the time the show started your body was already at a specific level of alertness, openness, and readiness that the performer designed hours before you arrived. Sound is not atmosphere. It is instruction.\n\n"),
    ("CHAPTER 25\nMaking the Room Say Yes",
     "What You Have Felt Before\nSomeone asked you to do something and you did it without quite deciding to. Not because you were coerced. Because by the time the request arrived, the conditions around it had already set the direction. The yes was not manufactured in the moment. It was built into the environment ten minutes before the ask. That is compliance architecture. This chapter is how it works.\n\n"),
    ("CHAPTER 26\nThe Authority Frame",
     "What You Have Felt Before\nThe performer had not done anything impressive yet and you already believed they were going to. Something about the way they arrived \u2014 not arrogance, not energy, but a specific quality of not needing anything from the room \u2014 told your nervous system: follow. The authority frame was set before the first effect. This chapter is what set it.\n\n"),
    ("CHAPTER 27\nWhat the Room Decides Before You Speak",
     "What You Have Felt Before\nYou watched a performer struggle and the failure was not the material. The material was fine. But the room had made a decision before the first line \u2014 something about the introduction, the lighting, the preceding hour \u2014 and no amount of skill recovered it. The room decided before they spoke. This chapter is about controlling that decision.\n\n"),
]

for anchor_title, wyhfb_text in wyhfb_to_add:
    if anchor_title in content:
        # Find the chapter block: CHAPTER N\nTitle\nSubtitle\n────\n
        idx = content.find(anchor_title)
        # Move past the title line to find the subtitle or dash
        after_title = content.find('\n', idx + len(anchor_title)) + 1
        # Insert WYHFB right after the chapter title + subtitle + dashes
        # Find where the dashes end (or where actual content starts)
        dash_pos = content.find('\u2500', after_title)
        if dash_pos > 0 and dash_pos < after_title + 400:
            dash_end = content.find('\n', dash_pos) + 1
            content = content[:dash_end] + wyhfb_text + content[dash_end:]
        else:
            # No dash line — just insert after the subtitle line
            content = content[:after_title] + wyhfb_text + content[after_title:]
        print(f"  WYHFB added for: {anchor_title.split(chr(10))[1]}")
        changes += 1
    else:
        print(f"  ANCHOR NOT FOUND: {anchor_title}")

with open('manuscript-extracted.txt', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{'='*60}")
print(f"Total additional changes: {changes}")
