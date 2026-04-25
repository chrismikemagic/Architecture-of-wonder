"""
Part 3 Restructure Script
Renames Part 3 to "The Methods" and reorganizes all chapters.

New Part 3 order:
  Ch 15  — Closing the Barn Door            (from current Part 2)
  Ch 25  — Memory Distortion                (from v2 Ch 18)
  Ch 12  — Cold Reading, Warm Reading...    (from current Part 2)
  Ch 13  — Contact Mind Reading             (from current Part 2)
  Ch 16  — How Hypnosis Really Works        (from current Part 2, title changed)
  Ch 26  — The Babel Count                  (new)
  Ch 27  — Psychological Forces             (from v2 Ch 20)
  Ch 28  — Making Better Propless Mentalism (from v2 Ch 21)
  Ch 24  — Propless Systems That Actually Work (from current Part 5)
  Ch 29  — Zodiac Divinations Without Anagrams (from v2 Ch 23)

Part 4 — The Corporate Stage (adds Ch 17 Pre-Show at front):
  Ch 17  — Pre-Show
  Ch 18, 19, 19B, 20, 21, 22, 23 (unchanged)

Part 5 — Performance Craft (Ch 24 removed; Ch 30 added):
  Ch 30  — Architecture of Obedience        (from v2 Ch 16)

Part 8 — unchanged
"""

import re

MAIN = r'C:\Users\Chris\Architecture-of-wonder\manuscript-extracted.txt'
V2   = r'C:\Users\Chris\Architecture-of-wonder-v2\manuscript-extracted.txt'

with open(MAIN, 'r', encoding='utf-8') as f:
    main_lines = f.readlines()

with open(V2, 'r', encoding='utf-8') as f:
    v2_lines = f.readlines()

# ─── helper: find where a chapter starts in a line list ───────────────────────
def find_chapter_start(lines, chapter_str):
    """Return 0-based index of the line matching '^CHAPTER N$'"""
    for i, line in enumerate(lines):
        if line.strip() == chapter_str:
            return i
    raise ValueError(f"Chapter not found: {chapter_str!r}")

def find_next_chapter_or_part(lines, start):
    """Return 0-based index of the next CHAPTER/PART line after start."""
    for i in range(start + 1, len(lines)):
        stripped = lines[i].strip()
        if re.match(r'^(CHAPTER\s+\d+[A-Z]?|PART\s+(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT))$', stripped):
            return i
    return len(lines)

def extract_chapter(lines, chapter_str):
    """Return list of lines for this chapter (up to the next CHAPTER/PART)."""
    start = find_chapter_start(lines, chapter_str)
    end   = find_next_chapter_or_part(lines, start)
    return lines[start:end]

def renumber_chapter(chapter_lines, new_num):
    """Replace the first 'CHAPTER N' line with 'CHAPTER new_num'."""
    result = list(chapter_lines)
    for i, line in enumerate(result):
        if re.match(r'^CHAPTER\s+\d+[A-Z]?\s*$', line.strip()):
            result[i] = f'CHAPTER {new_num}\n'
            break
    return result

def rename_chapter_title(chapter_lines, new_title):
    """Replace the second non-empty line (the title) after CHAPTER header."""
    result = list(chapter_lines)
    found_header = False
    for i, line in enumerate(result):
        if re.match(r'^CHAPTER\s+\d+[A-Z]?\s*$', line.strip()):
            found_header = True
            continue
        if found_header and line.strip():
            result[i] = new_title + '\n'
            break
    return result

# ─── extract sections from MAIN ───────────────────────────────────────────────

# Front matter: everything up to (but not including) "PART ONE" actual content
part_one_idx = find_chapter_start(main_lines, 'PART ONE')
front_matter = main_lines[:part_one_idx]

# Part Two: PART TWO header through end of Ch 11
part_two_idx = find_chapter_start(main_lines, 'PART TWO')

# Part One block: PART ONE through just before PART TWO
part_one_block = main_lines[part_one_idx:part_two_idx]
ch12_idx = find_chapter_start(main_lines, 'CHAPTER 12')
ch13_idx = find_chapter_start(main_lines, 'CHAPTER 13')
ch14_idx = find_chapter_start(main_lines, 'CHAPTER 14')
ch15_idx = find_chapter_start(main_lines, 'CHAPTER 15')
ch16_idx = find_chapter_start(main_lines, 'CHAPTER 16')
part3_idx = find_chapter_start(main_lines, 'PART THREE')

# Part Two: from PART TWO line through end of Ch 11 (stops at Ch 12)
part_two_thru_ch11 = main_lines[part_two_idx:ch12_idx]

# Ch 12 — Cold Reading
ch12_lines = extract_chapter(main_lines, 'CHAPTER 12')

# Ch 13 — Contact Mind Reading
ch13_lines = extract_chapter(main_lines, 'CHAPTER 13')

# Ch 14 — Language of Yes (stays at end of Part 2)
ch14_lines = extract_chapter(main_lines, 'CHAPTER 14')

# Ch 15 — Closing the Barn Door
ch15_lines = extract_chapter(main_lines, 'CHAPTER 15')

# Ch 16 — How Hypnosis Really Works (title change)
ch16_lines = extract_chapter(main_lines, 'CHAPTER 16')
ch16_lines = rename_chapter_title(ch16_lines, 'How Hypnosis Really Works')

# Old Part 3 content: Part Three header up to Part Four
ch17_idx    = find_chapter_start(main_lines, 'CHAPTER 17')
part4_idx   = find_chapter_start(main_lines, 'PART FOUR')
ch17_lines  = main_lines[ch17_idx:part4_idx]   # Ch 17 Pre-Show (no Part 3 header)

# Part 4 block: from PART FOUR through end of Ch 23
part4_header_start = part4_idx
ch18_idx = find_chapter_start(main_lines, 'CHAPTER 18')
ch24_idx = find_chapter_start(main_lines, 'CHAPTER 24')
part5_idx = find_chapter_start(main_lines, 'PART FIVE')
part8_idx = find_chapter_start(main_lines, 'PART EIGHT')

# Part 4: header + Ch 18-23
part4_thru_ch23 = main_lines[part4_idx:part5_idx]

# Ch 24 — Propless Systems (moves to Part 3)
ch24_lines = extract_chapter(main_lines, 'CHAPTER 24')

# Part 8 to end (unchanged)
part8_to_end = main_lines[part8_idx:]

# ─── extract chapters from V2 ─────────────────────────────────────────────────

# v2 Ch 18 → main Ch 25 (Memory Distortion)
ch25_lines = renumber_chapter(extract_chapter(v2_lines, 'CHAPTER 18'), 25)

# v2 Ch 20 → main Ch 27 (Psychological Forces)
ch27_lines = renumber_chapter(extract_chapter(v2_lines, 'CHAPTER 20'), 27)

# v2 Ch 21 → main Ch 28 (Making Better Propless Mentalism)
ch28_lines = renumber_chapter(extract_chapter(v2_lines, 'CHAPTER 21'), 28)

# v2 Ch 23 → main Ch 29 (Zodiac Divinations Without Anagrams)
ch29_lines = renumber_chapter(extract_chapter(v2_lines, 'CHAPTER 23'), 29)

# v2 Ch 16 → main Ch 30 (Architecture of Obedience)
ch30_lines = renumber_chapter(extract_chapter(v2_lines, 'CHAPTER 16'), 30)

# ─── Babel Count — Ch 26 ──────────────────────────────────────────────────────
babel_count_text = r"""CHAPTER 26
The Babel Count
Counting the letters in a thought they never wrote down.
────────────────────────────────────────────────────────────────────────────────
This is not about guessing. This is timing and body language together. Body language takes priority, and if you are not getting a clear read, you can switch to using timing on the fly.
You are counting how long it takes them to think. That is it. Once you establish a cadence, every letter occupies a unit of time. They move through the word step by step, and you count those steps.
They think a letter. Time passes. They think the next letter. Time passes.
You are not pretending to hear their thoughts — you are measuring the length of the word.

The Basic Idea
Most people think silently. They do not realize they typically move a lot when they think. Give someone the simple task of spelling a word in their head. Their body leaks the structure of that thought.
A finger taps. A head nods. A rhythm forms. They are not doing this for you. They are doing it to keep track. Most of the time they are completely unaware.
Working memory is limited. The moment a person is asked to hold and sequence information, especially something as linear as letters, the brain looks for external support. It offloads part of the process into the body. This is why people count on their fingers, nod as they list items, or pulse their breath when stepping through something internally. The thought becomes physical.
Without an external anchor, the sequence drifts. A nod marks a step. A finger marks a step. A breath marks a step. You are going to use that function.
Additionally, we want to increase the reliability of this so it can be a common tool in our tool belt by influencing them to think in a certain cadence and rhythm.

Setting the Rhythm
Do not expect this to happen on its own. You cause it. Before they ever think of their word, you demonstrate the process.
"Close your eyes."
Slowly, clearly, you spell a word out loud and mark each letter visibly: "S... T... R... A... W... B... E... R... R... Y — DONE!"
As you do, your head nods with each letter. Not exaggerated or theatrical. Just enough to establish a pattern that they will follow.
Do this naturally, without rushing, and you will land at roughly one letter every 0.6 to 0.7 seconds. That is not entirely set by you, though you are reinforcing it. This pacing is where most people settle when they are being deliberate and clear in going through something sequentially.
That rhythm becomes the crux of the method.
People mirror structure more than instruction. You are not telling them how to think. You are showing them how thinking looks. When they take their turn, they follow it. This works as long as you have not raised their guard or given them a reason to resist.
Since they will mirror your structure, you do not need to tell them to say "done" when they finish. They will either say it without being told, or mirror your example by snapping their eyes open and punctuating the moment they finished with their body language.
If this seems too advanced, instruct them to open their eyes as soon as they are done or say "done" when finished. Disguise the instruction as part of what makes it impressive: "The exact moment you do this, I will immediately tell you every letter I heard you say in your head." You are saying this so they believe it serves the effect, not so it serves you.

The Key Insight
People believe they are thinking freely. They are not.
They are following a structure you gave them. That structure has a pace. Pace is measurable. Once you understand that, the method becomes very easy and approachable.

The Method
Once the rhythm is set, the rest is counting.
You both close your eyes. You ask them to think of their word and spell it, one letter at a time, exactly as you demonstrated. From there, you have two options depending on your conditions.

One-on-One
This is where the method is strongest.
You close your eyes with them initially so they see your eyes closing with them, then secretly open your eyes to watch. You find their counting rhythm by watching their head nod or fingers tap as you count. Then you stop counting as soon as you spot that they open their eyes. You now know the length of the word.
From there, you reveal it as if you heard each letter in sequence. With practice and careful routining, you will always know the word immediately and can deliver a fast, shocking reveal.
"I heard S—" Pause here to check their reaction and confirm the hit. If it lands, continue quickly: "T... R... A... W... B... E... R... R... Y."
The reactions are larger than you expect.

In Front of a Group
Do not reopen your eyes after closing them. That weakens the premise.
Keep the conditions clean. You both close your eyes. Tell them to say "done" when they finish. The moment you say start, you begin counting internally at the established pace. When they say done, you stop. That gives you a letter count, plus or minus one letter if you are not yet well practiced. That margin is workable.

Days of the Week
The same structure applies to days of the week, with one important difference. The distribution is uneven in your favor.

01 — MONDAY | 6 letters
02 — TUESDAY | 7 letters
03 — WEDNESDAY | 9 letters
04 — THURSDAY | 8 letters
05 — FRIDAY | 6 letters
06 — SATURDAY | 8 letters
07 — SUNDAY | 6 letters

At first glance, the overlap looks like a problem. Three days share six letters. In practice, people overwhelmingly reach for Monday, Friday, or Sunday when given a free choice. One small adjustment eliminates the ambiguity entirely: "Think of a weekday, not the weekend." Now you have five options with four distinct letter counts. Wednesday and Thursday stand alone. Tuesday stands alone. Monday and Friday remain a pair — but a pair is manageable. Determining whether it is at the start or end of the week gives you your answer immediately.

The Birthday Application
Where this becomes genuinely powerful is in birthday work.
There are situations where you have already obtained the date. You know the month, the day, the year. What you do not know — what no one expects you to know — is what day of the week that date falls on. That is the detail most people would never think to calculate, which makes it the detail that lands hardest. Have them concentrate on the day of the week they were born. If they do not know, they can look it up. Then run the count and confirm the day.
Then reveal it alongside the month, day, and year. The spectator's perspective: you started with a question about a single day of the week. You ended with the full picture — day, date, month, year. That escalation from small to large is what makes this method worth learning.
KEY PRINCIPLE
Never show your ceiling early. If they think you are only reaching for the day of the week, the date and year land as something they cannot explain. The method only costs you if you reveal its edges. Keep the frame small. Let the reveal break out of it.

Hiding the Method: The Season Reading
Once you have the day, you have an opening.
Ask them to stop thinking about letters entirely. Ask them instead to think about the season they were born in — specifically, the things people do during that time of year. Not the season by name. The images and activities that come with that season.
Spring brings cleaning, allergies, rain, flowers. Summer brings beach, heat, vacation, evenings outdoors. Fall brings leaves, sweaters, school starting, Halloween, Thanksgiving. Winter brings snow, skiing, holidays, staying cozy inside.
As they hold those images, you begin naming them. You are not guessing the season. You are describing it through its associations. They hear their own mental images reflected back to them, and the method disappears entirely. It reads as deep perceptual access, not arithmetic.
What you have done, across a few minutes of apparently separate work, is obtained the day, the season, and everything that implies — all while they believed you were hearing the thoughts inside their head.

Credit
This principle has been pushed further than almost anyone by Fraser Parker, through his work on Obsidian. Obsidian builds on the Babel Count as a foundation, layering in additional techniques and automating much of the process to the point where you can identify a freely chosen word from an open category with minimal verbal output from the spectator.
What is written here is the foundation. What Parker built on top of it is worth your time if you enjoy finding where this principle leads.
· · ·
Influence and counting. That is the whole secret of The Babel Count.

"""

babel_count_lines = [line + '\n' for line in babel_count_text.split('\n')]
# Clean up: remove double newlines from the join
babel_count_lines = [l for i, l in enumerate(babel_count_lines) if not (l == '\n' and i > 0 and babel_count_lines[i-1] == '\n')]

# ─── build Part 3 header ──────────────────────────────────────────────────────
part3_header = [
    '\n',
    '\n',
    'PART THREE\n',
    'The Methods\n',
    'Technical methods, systems, and practical frameworks. How the tools work at the level of mechanics, psychology, and application.\n',
    '\n',
    '\n',
]

# ─── build Part 4 header with Ch 17 at front ─────────────────────────────────
# part4_thru_ch23 already includes the PART FOUR header.
# We insert Ch 17 between the Part 4 header and Ch 18.
ch18_relative_idx = None
for i, line in enumerate(part4_thru_ch23):
    if line.strip() == 'CHAPTER 18':
        ch18_relative_idx = i
        break

if ch18_relative_idx is None:
    raise ValueError("CHAPTER 18 not found in part4 block")

part4_header_block  = part4_thru_ch23[:ch18_relative_idx]
part4_ch18_onward   = part4_thru_ch23[ch18_relative_idx:]

# ─── build Part 5 header ──────────────────────────────────────────────────────
part5_header = [
    '\n',
    '\n',
    'PART FIVE\n',
    'Performance Craft\n',
    'The architecture of a full show. Structural choices, obedience dynamics, and the behavioral intelligence that governs every room.\n',
    '\n',
    '\n',
]

# ─── assemble new manuscript ──────────────────────────────────────────────────
new_manuscript = []
new_manuscript += front_matter            # front matter + TOC (to be updated separately)
new_manuscript += part_one_block          # Part One + Ch 1-5
new_manuscript += part_two_thru_ch11      # Part Two header + Ch 6-11
new_manuscript += ch14_lines              # Ch 14 — Language of Yes (end of Part 2)
new_manuscript += part3_header            # PART THREE — The Methods
new_manuscript += ch15_lines             # Ch 15 — Closing the Barn Door
new_manuscript += ch25_lines             # Ch 25 — Memory Distortion
new_manuscript += ch12_lines             # Ch 12 — Cold Reading
new_manuscript += ch13_lines             # Ch 13 — Contact Mind Reading
new_manuscript += ch16_lines             # Ch 16 — How Hypnosis Really Works
new_manuscript += babel_count_lines      # Ch 26 — The Babel Count
new_manuscript += ch27_lines             # Ch 27 — Psychological Forces
new_manuscript += ch28_lines             # Ch 28 — Making Better Propless Mentalism
new_manuscript += ch24_lines             # Ch 24 — Propless Systems That Actually Work
new_manuscript += ch29_lines             # Ch 29 — Zodiac Divinations Without Anagrams
new_manuscript += part4_header_block     # PART FOUR header
new_manuscript += ch17_lines             # Ch 17 — Pre-Show
new_manuscript += part4_ch18_onward      # Ch 18-23
new_manuscript += part5_header           # PART FIVE header
new_manuscript += ch30_lines             # Ch 30 — Architecture of Obedience
new_manuscript += ['\n']
new_manuscript += part8_to_end           # PART EIGHT onwards

# ─── write output ─────────────────────────────────────────────────────────────
with open(MAIN, 'w', encoding='utf-8') as f:
    f.writelines(new_manuscript)

print("Done. Verifying new structure...")

# ─── verify ───────────────────────────────────────────────────────────────────
with open(MAIN, 'r', encoding='utf-8') as f:
    verify_lines = f.readlines()

import re
print("\nNew chapter/part structure:")
for i, line in enumerate(verify_lines):
    stripped = line.strip()
    if re.match(r'^CHAPTER\s+\d+[A-Z]?$', stripped) or re.match(r'^PART\s+(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT)$', stripped):
        title = verify_lines[i+1].strip() if i+1 < len(verify_lines) else ''
        print(f"  Line {i+1}: {stripped} -- {title}")
