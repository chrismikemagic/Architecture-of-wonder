#!/usr/bin/env python3
"""
Restructure manuscript-extracted.txt for Architecture of Wonder v2.

OLD STRUCTURE                          NEW STRUCTURE
─────────────────────────────────────  ─────────────────────────────────────
PART ONE:   Chs 1-5   (unchanged)      PART ONE:   Chs 1-5   (unchanged)
PART TWO:   Chs 6-16  (reading room)   PART TWO:   Chs 6-11  (reading room, trimmed)
PART THREE: Field Notes (ref cards)    PART THREE: Chs 12-16 (THE METHODS — new)
PART FOUR:  Chs 17-20 (corporate)      PART FOUR:  Chs 17-25 (PERFORMANCE CONSTRUCTION)
PART FIVE:  Ch 21     (perf arc)       PART FIVE:  Chs 26-31 (AUTHORITY & INFLUENCE)
PART SIX:   Chs 22-32 (presence)      PART SIX:   Chs 32-35 (PROFESSIONAL STAGE)
PART SEVEN: Chs 33-37 (business)      PART SEVEN: Chs 36-42 (BUSINESS BRAIN)
PART EIGHT: Chs 38-42 (frameworks)    REFERENCE:  Field Notes (moved to back)

Chapter remapping:
  Old 12 (Cold Reading)         → New 13
  Old 13 (Contact Mind Reading) → New 14
  Old 14 (Language of Yes)      → New 15
  Old 15 (Closing Barn Door)    → New 16
  Old 16 (Hypnosis)             → New 12  (leads Methods section)
  Old 17 (Boardroom)            → New 32
  Old 18 (Why Training Fails)   → New 33
  Old 19 (Influence W/O Auth)   → New 34
  Old 20 (Ethics)               → New 35
  Old 21 (Performance Arc)      → New 17
  Old 22 (Strolling)            → New 21
  Old 23 (Room Rises)           → New 22
  Old 24 (Audio)                → New 23
  Old 25 (Making Room Say Yes)  → New 24
  Old 26 (Authority Frame)      → New 25
  Old 27 (Building Career)      → New 37
  Old 28 (Intro Video)          → New 38
  Old 29 (Turning Observation)  → New 18
  Old 30 (Insight Demos)        → New 30  (same — moved to Part 5)
  Old 31 (Method Invisibility)  → New 19
  Old 32 (Patter/Rhythm)        → New 20
  Old 33 (Where Bookings Won)   → New 36
  Old 34 (Intros/Bios)          → New 39
  Old 35 (Language of Authority)→ New 40
  Old 36 (Booking Room)         → New 41
  Old 37 (First Contact)        → New 42
  Old 38 (FATE)                 → New 26
  Old 39 (Authority Arch)       → New 27
  Old 40 (Signal Dictionary)    → New 28
  Old 41 (How Influence Works)  → New 29
  Old 42 (DECODE/Six Steps)     → New 31
"""

import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('manuscript-extracted.txt', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
N = len(lines)

def block(start_1, end_1):
    """Return lines[start_1-1 : end_1] joined with newlines + trailing newline."""
    return '\n'.join(lines[start_1-1 : end_1]) + '\n'

def renum(text, new_num):
    """Replace first 'CHAPTER N' line with 'CHAPTER new_num'."""
    return re.sub(r'^CHAPTER \d+', f'CHAPTER {new_num}', text, count=1)

# ── Block boundaries (1-indexed, inclusive) ─────────────────────────────────
# Derived from line numbers of structural markers:
FRONT        = block(1, 190)
PT1_HDR      = block(191, 195)
CH1          = block(196, 228)
CH2          = block(229, 255)
CH3          = block(256, 302)
CH4          = block(303, 320)
CH5          = block(321, 349)
PT2_HDR      = block(350, 354)
CH6          = block(355, 509)
CH7          = block(510, 990)
CH8          = block(991, 1024)
CH9          = block(1025, 1092)
CH10         = block(1093, 1319)
CH11         = block(1320, 1484)
CH12_OLD     = block(1485, 1787)   # Cold Reading
CH13_OLD     = block(1788, 1918)   # Contact Mind Reading
CH14_OLD     = block(1919, 2076)   # Language of Yes
CH15_OLD     = block(2077, 2101)   # Closing the Barn Door
CH16_OLD     = block(2102, 2187)   # The Science of Hypnosis
FIELD_NOTES  = block(2188, 2274)   # PART THREE header + all 6 field note cards
# (2275-2279 = old Part Four header — discarded, replaced)
CH17_OLD     = block(2280, 2299)   # Mentalism in Boardroom
CH18_OLD     = block(2300, 2320)   # Why Most Training Fails
CH19_OLD     = block(2321, 2345)   # Influence Without Authority
CH20_OLD     = block(2346, 2387)   # Ethics of Influence
# (2388-2392 = old Part Five header — discarded)
CH21_OLD     = block(2393, 2439)   # The Performance Arc
# (2440-2444 = old Part Six header — discarded)
CH22_OLD     = block(2445, 2489)   # Art of Strolling
CH23_OLD     = block(2490, 2503)   # When the Room Rises
CH24_OLD     = block(2504, 2554)   # Audio as Architecture
CH25_OLD     = block(2555, 2597)   # Making the Room Say Yes
CH26_OLD     = block(2598, 2635)   # The Authority Frame
CH27_OLD     = block(2636, 2656)   # Building a Career, Not a Calendar
CH28_OLD     = block(2657, 2674)   # The Intro Video
CH29_OLD     = block(2675, 2716)   # Turning Observation into Performance
CH30_OLD     = block(2717, 2776)   # Insight Demonstrations
CH31_OLD     = block(2777, 2806)   # Method Invisibility
CH32_OLD     = block(2807, 2967)   # Patter, Rhythm, and Silence
# (2968-2972 = old Part Seven header — discarded)
CH33_OLD     = block(2973, 3006)   # Where Bookings Are Actually Won
CH34_OLD     = block(3007, 3027)   # Introductions, Bios, and Testimonials
CH35_OLD     = block(3028, 3044)   # The Language of Authority
CH36_OLD     = block(3045, 3062)   # Reading the Booking Room
CH37_OLD     = block(3063, 3107)   # From First Contact to Follow-Up
# (3108-3120 = old Part Eight header + intro — discarded, replaced)
CH38_OLD     = block(3121, 3233)   # FATE Model
CH39_OLD     = block(3234, 3322)   # Authority Architecture
CH40_OLD     = block(3323, 3430)   # Performer's Signal Dictionary
CH41_OLD     = block(3431, 3513)   # How Influence Actually Works
CH42_OLD     = block(3514, 3816)   # Six Steps from Observation to Ovation (DECODE)
ABOUT_AUTHOR = block(3817, N)

# ── Strip PART THREE header from field notes (we write our own) ──────────────
# Field notes block: "PART THREE\nField Notes\n<desc>\n\nHow to Use..."
# Find the "How to Use the Field Notes" line and keep from there
fn_lines = FIELD_NOTES.split('\n')
fn_start = next((i for i, l in enumerate(fn_lines) if l.startswith('How to Use')), 0)
FIELD_NOTES_CONTENT = '\n'.join(fn_lines[fn_start:])

# ── New part headers ──────────────────────────────────────────────────────────
PT3_NEW = """\nPART THREE\nThe Methods\nCold reading, contact mind reading, hypnosis, compliance language, and the core mentalism techniques — each made stronger by the behavioral foundation in Part Two.\n\n\n"""

PT4_NEW = """\nPART FOUR\nPerformance Construction\nHow to build the show: the arc, the craft of revelation, timing, room management, and the structural decisions that determine whether skill becomes experience.\n\n\n"""

PT5_NEW = """\nPART FIVE\nAuthority, Influence, and the Deep Framework\nThe invisible architecture that determines whether a performance has power before the first effect begins. The FATE Model, Authority Architecture, the Signal Dictionary, the Influence Equation, and the DECODE Framework — each built for high-stakes behavioral work, each sharper on stage.\n\n\n"""

PT6_NEW = """\nPART SIX\nThe Professional Stage\nBehavioral science applied to the professional performance context — from keynote halls and boardrooms to corporate training and the ethics of influence.\n\n\n"""

PT7_NEW = """\nPART SEVEN\nThe Business Brain\nWhere bookings are actually won, how authority is built before you walk in the room, and the business of performing at the highest level.\n\n\n"""

REF_NEW = """\n· · ·\n\nREFERENCE SECTION\nField Notes\nA personal reference library pairing neurobiological findings with direct application on stage, in training rooms, and in the boardroom. Return to these before every performance.\n\n\n"""

# ── Assemble new manuscript ───────────────────────────────────────────────────
parts = []

# Front matter (TOC, intro, acknowledgements — unchanged)
parts.append(FRONT)

# PART ONE: The Architecture of Wonder (unchanged)
parts.append(PT1_HDR)
parts.append(CH1)
parts.append(CH2)
parts.append(CH3)
parts.append(CH4)
parts.append(CH5)

# PART TWO: Reading the Room (Ch 6-11 only — unchanged)
parts.append(PT2_HDR)
parts.append(CH6)
parts.append(CH7)
parts.append(CH8)
parts.append(CH9)
parts.append(CH10)
parts.append(CH11)

# PART THREE: The Methods (new section)
parts.append(PT3_NEW)
parts.append(renum(CH16_OLD, 12))   # Hypnosis → leads the section
parts.append(renum(CH12_OLD, 13))   # Cold Reading
parts.append(renum(CH13_OLD, 14))   # Contact Mind Reading
parts.append(renum(CH14_OLD, 15))   # Language of Yes
parts.append(renum(CH15_OLD, 16))   # Closing the Barn Door

# PART FOUR: Performance Construction (merge old Parts 5+6)
parts.append(PT4_NEW)
parts.append(renum(CH21_OLD, 17))   # Performance Arc
parts.append(renum(CH29_OLD, 18))   # Turning Observation into Performance
parts.append(renum(CH31_OLD, 19))   # Method Invisibility
parts.append(renum(CH32_OLD, 20))   # Patter, Rhythm, and Silence
parts.append(renum(CH22_OLD, 21))   # Art of Strolling
parts.append(renum(CH23_OLD, 22))   # When the Room Rises
parts.append(renum(CH24_OLD, 23))   # Audio as Architecture
parts.append(renum(CH25_OLD, 24))   # Making the Room Say Yes
parts.append(renum(CH26_OLD, 25))   # The Authority Frame

# PART FIVE: Authority, Influence, and the Deep Framework (old Part 8 — moved)
parts.append(PT5_NEW)
parts.append(renum(CH38_OLD, 26))   # FATE Model
parts.append(renum(CH39_OLD, 27))   # Authority Architecture
parts.append(renum(CH40_OLD, 28))   # Performer's Signal Dictionary
parts.append(renum(CH41_OLD, 29))   # How Influence Actually Works
parts.append(renum(CH30_OLD, 30))   # Insight Demonstrations (applied synthesis)
parts.append(renum(CH42_OLD, 31))   # Six Steps / DECODE (capstone)

# PART SIX: The Professional Stage (old Part 4 — moved)
parts.append(PT6_NEW)
parts.append(renum(CH17_OLD, 32))   # Mentalism in the Boardroom
parts.append(renum(CH18_OLD, 33))   # Why Most Training Fails
parts.append(renum(CH19_OLD, 34))   # Influence Without Authority
parts.append(renum(CH20_OLD, 35))   # The Ethics of Influence

# PART SEVEN: The Business Brain
parts.append(PT7_NEW)
parts.append(renum(CH33_OLD, 36))   # Where Bookings Are Actually Won
parts.append(renum(CH27_OLD, 37))   # Building a Career, Not a Calendar
parts.append(renum(CH28_OLD, 38))   # The Intro Video
parts.append(renum(CH34_OLD, 39))   # Introductions, Bios, and Testimonials
parts.append(renum(CH35_OLD, 40))   # The Language of Authority
parts.append(renum(CH36_OLD, 41))   # Reading the Booking Room
parts.append(renum(CH37_OLD, 42))   # From First Contact to Follow-Up

# Reference Section: Field Notes (moved from Part 3 to back matter)
parts.append(REF_NEW)
parts.append(FIELD_NOTES_CONTENT)

# About the Author
parts.append(ABOUT_AUTHOR)

# ── Write output ──────────────────────────────────────────────────────────────
new_ms = ''.join(parts)

with open('manuscript-extracted.txt', 'w', encoding='utf-8') as f:
    f.write(new_ms)

# ── Verify ────────────────────────────────────────────────────────────────────
chapters = re.findall(r'^CHAPTER (\d+)', new_ms, re.MULTILINE)
parts_found = re.findall(r'^(PART (?:ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT)|REFERENCE SECTION)', new_ms, re.MULTILINE)

print(f'Written: {len(new_ms):,} chars')
print(f'Parts: {parts_found}')
print(f'Chapters ({len(chapters)}): {chapters}')

# Check for gaps or duplicates
expected = list(range(1, 43))
actual = [int(c) for c in chapters]
if actual == expected:
    print('Chapter sequence: OK (1-42 in order)')
else:
    missing = set(expected) - set(actual)
    dupes = [x for x in actual if actual.count(x) > 1]
    extra = set(actual) - set(expected)
    if missing: print(f'  MISSING: {sorted(missing)}')
    if dupes:   print(f'  DUPES:   {sorted(set(dupes))}')
    if extra:   print(f'  EXTRA:   {sorted(extra)}')
