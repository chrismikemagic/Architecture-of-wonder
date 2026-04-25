"""
Full manuscript rebuild to the new sequential 1-39 chapter structure.

New TOC:
  Intro / Ch 1  — On Being the Person Who Admits What They Do

  PART ONE — The Architecture of Wonder
  Ch 2   Designing for Reality
  Ch 3   The Five Forces of Attention
  Ch 4   Tension, Threat and the Window of Wonder
  Ch 5   The Art of Anticipation
  Ch 6   Attention as a Weapon

  PART TWO — Reading the Room
  Ch 7   Reading Body Language in Real Time
  Ch 8   The 80-Signal System
  Ch 9   The Four Personalities That Change How You Perform
  Ch 10  The Volunteer's Brain
  Ch 11  Chris Michael's Tell Table        [v2 Ch 10]
  Ch 12  The Eyes, the Face, and the Way Thought Leaks Out
  Ch 13  The Micro-Expression Matrix

  PART THREE — The Methods
  Ch 14  Closing the Barn Door
  Ch 15  Memory Distortion
  Ch 16  Cold Reading, Warm Reading, and Thin Slicing
  Ch 17  Contact Mind Reading
  Ch 18  How Hypnosis Really Works
  Ch 19  The Babel Count
  Ch 20  Psychological Forces
  Ch 21  Making Better Propless Mentalism
  Ch 22  Propless Systems That Actually Work
  Ch 23  Zodiac Divinations Without Anagrams
  Ch 24  Pre-Show
  Ch 25  Digital Preshow

  PART FOUR — Performance Craft
  Ch 26  The Performance Arc              [v2 Ch 24]
  Ch 27  Method Invisibility              [v2 Ch 25]
  Ch 28  Patter, Rhythm, and Silence      [v2 Ch 26]
  Ch 29  When the Room Rises              [v2 Ch 28]
  Ch 30  The Art of Strolling             [v2 Ch 27]
  Ch 31  Making the Room Say Yes          [v2 Ch 29]
  Ch 32  The Intro Video
  Ch 33  Introductions, Bios, and Testimonials

  PART FIVE — Authority, Influence, and the Deep Framework
  Ch 34  What the Room Decides Before You Speak
  Ch 35  The Ethics of Influence
  Ch 36  How Influence Actually Works
  Ch 37  Influence Without Authority
  Ch 38  The Authority Frame              [v2 Ch 31]
  Ch 39  Authority Architecture

Chapters dropped: Language of Yes, Mentalism in Boardroom, Why Most Training Fails,
                  Architecture of Obedience, Performer's Signal Dictionary,
                  Six Steps from Observation to Ovation
"""

import re, shutil, os

MAIN = r'C:\Users\Chris\Architecture-of-wonder\manuscript-extracted.txt'
V2   = r'C:\Users\Chris\Architecture-of-wonder-v2\manuscript-extracted.txt'

shutil.copy(MAIN, r'C:\Users\Chris\Architecture-of-wonder\backups\manuscript-before-full-rebuild.txt')
print("Backup created.")

with open(MAIN, 'r', encoding='utf-8') as f:
    main = f.readlines()
with open(V2, 'r', encoding='utf-8') as f:
    v2 = f.readlines()

# ─── helpers ──────────────────────────────────────────────────────────────────
def find_start(lines, pattern):
    for i, line in enumerate(lines):
        if line.strip() == pattern:
            return i
    raise ValueError(f"Not found: {pattern!r}")

def find_next_boundary(lines, start):
    for i in range(start + 1, len(lines)):
        if re.match(r'^(CHAPTER\s+\d+[A-Z]?|PART\s+(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT)|INTRODUCTION|ABOUT THE AUTHOR|GLOSSARY)$', lines[i].strip()):
            return i
    return len(lines)

def get_chapter(lines, old_id, new_num):
    """Extract chapter, replace first CHAPTER line with new number."""
    start = find_start(lines, f'CHAPTER {old_id}')
    end   = find_next_boundary(lines, start)
    chunk = list(lines[start:end])
    chunk[0] = f'CHAPTER {new_num}\n'
    return chunk

def get_intro_as_chapter1(lines):
    """Turn INTRODUCTION into CHAPTER 1."""
    start = find_start(lines, 'INTRODUCTION')
    end   = find_next_boundary(lines, start)
    chunk = list(lines[start:end])
    chunk[0] = 'CHAPTER 1\n'
    return chunk

def get_about(lines):
    try:
        start = find_start(lines, 'ABOUT THE AUTHOR')
        return lines[start:]
    except ValueError:
        return []

# ─── front matter (everything before INTRODUCTION) ────────────────────────────
intro_idx  = find_start(main, 'INTRODUCTION')
front_matter = main[:intro_idx]

# ─── chapters ─────────────────────────────────────────────────────────────────
ch1  = get_intro_as_chapter1(main)          # On Being the Person...
ch2  = get_chapter(main,  '1',  2)          # Designing for Reality
ch3  = get_chapter(main,  '2',  3)          # Five Forces
ch4  = get_chapter(main,  '3',  4)          # Tension
ch5  = get_chapter(main,  '4',  5)          # Art of Anticipation
ch6  = get_chapter(main,  '5',  6)          # Attention as Weapon
ch7  = get_chapter(main,  '6',  7)          # Reading Body Language
ch8  = get_chapter(main,  '7',  8)          # 80-Signal System
ch9  = get_chapter(main,  '8',  9)          # Four Personalities
ch10 = get_chapter(main,  '9', 10)          # Volunteer's Brain
ch11 = get_chapter(v2,   '10', 11)          # Chris Michael's Tell Table
ch12 = get_chapter(main, '10', 12)          # Eyes, Face
ch13 = get_chapter(main, '11', 13)          # Micro-Expression Matrix
ch14 = get_chapter(main, '15', 14)          # Closing the Barn Door
ch15 = get_chapter(main, '25', 15)          # Memory Distortion
ch16 = get_chapter(main, '12', 16)          # Cold Reading
ch17 = get_chapter(main, '13', 17)          # Contact Mind Reading
ch18 = get_chapter(main, '16', 18)          # How Hypnosis Really Works
ch19 = get_chapter(main, '26', 19)          # Babel Count
ch20 = get_chapter(main, '27', 20)          # Psychological Forces
ch21 = get_chapter(main, '28', 21)          # Making Better Propless Mentalism
ch22 = get_chapter(main, '24', 22)          # Propless Systems
ch23 = get_chapter(main, '29', 23)          # Zodiac Divinations
ch24 = get_chapter(main, '17', 24)          # Pre-Show
ch25 = get_chapter(main, '19B', 25)         # Digital Preshow
ch26 = get_chapter(v2,  '24', 26)           # The Performance Arc
ch27 = get_chapter(v2,  '25', 27)           # Method Invisibility
ch28 = get_chapter(v2,  '26', 28)           # Patter, Rhythm, and Silence
ch29 = get_chapter(v2,  '28', 29)           # When the Room Rises
ch30 = get_chapter(v2,  '27', 30)           # The Art of Strolling
ch31 = get_chapter(v2,  '29', 31)           # Making the Room Say Yes
ch32 = get_chapter(main, '22', 32)          # The Intro Video
ch33 = get_chapter(main, '23', 33)          # Introductions, Bios, Testimonials
ch34 = get_chapter(main, '39', 34)          # What the Room Decides Before You Speak
ch35 = get_chapter(main, '21', 35)          # The Ethics of Influence
ch36 = get_chapter(main, '42', 36)          # How Influence Actually Works
ch37 = get_chapter(main, '20', 37)          # Influence Without Authority
ch38 = get_chapter(v2,  '31', 38)           # The Authority Frame
ch39 = get_chapter(main, '40', 39)          # Authority Architecture

about = get_about(main)

# ─── part headers ─────────────────────────────────────────────────────────────
def part_header(name, subtitle, description):
    return ['\n', '\n', f'PART {name}\n', f'{subtitle}\n', f'{description}\n', '\n', '\n']

p1 = part_header('ONE', 'The Architecture of Wonder',
    'The neurobiology of performance. What is happening in the audience\'s brain and how to design for it.')
p2 = part_header('TWO', 'Reading the Room',
    'Body language, cold reading, micro-expressions, and the art of extracting information before a single question is asked.')
p3 = part_header('THREE', 'The Methods',
    'Technical methods, systems, and practical frameworks. How the tools work at the level of mechanics, psychology, and application.')
p4 = part_header('FOUR', 'Performance Craft',
    'Show structure, scripting, and the craft of building a full performance. From the arc of an act to the architecture of a career.')
p5 = part_header('FIVE', 'Authority, Influence, and the Deep Framework',
    'The behavioral science of authority and influence, applied directly to performance. The frameworks that govern every room.')

# ─── assemble ─────────────────────────────────────────────────────────────────
manuscript = (
    front_matter +
    ch1 +
    p1 +
    ch2 + ch3 + ch4 + ch5 + ch6 +
    p2 +
    ch7 + ch8 + ch9 + ch10 + ch11 + ch12 + ch13 +
    p3 +
    ch14 + ch15 + ch16 + ch17 + ch18 + ch19 +
    ch20 + ch21 + ch22 + ch23 + ch24 + ch25 +
    p4 +
    ch26 + ch27 + ch28 + ch29 + ch30 + ch31 + ch32 + ch33 +
    p5 +
    ch34 + ch35 + ch36 + ch37 + ch38 + ch39 +
    ['\n'] +
    about
)

with open(MAIN, 'w', encoding='utf-8') as f:
    f.writelines(manuscript)

# ─── verify ───────────────────────────────────────────────────────────────────
with open(MAIN, 'r', encoding='utf-8') as f:
    verify = f.readlines()

print("\nNew structure:")
for i, line in enumerate(verify):
    stripped = line.strip()
    if re.match(r'^(CHAPTER\s+\d+[A-Z]?|PART\s+(ONE|TWO|THREE|FOUR|FIVE))$', stripped):
        title = verify[i+1].strip() if i+1 < len(verify) else ''
        print(f"  {stripped:12} {title[:50]}")
