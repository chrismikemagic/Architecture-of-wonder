#!/usr/bin/env python3
"""
Update build-book.py chapter numbers for Architecture of Wonder v2.

Two categories of keys to update:

1. HOOK_LINES / KEY_READS — simple keys like 'CHAPTER N'
   These use v1 MANUSCRIPT chapter numbers → remap to v2 numbers.

2. SECTION_BADGES / FIGURES — compound keys like 'CHAPTER N:Section Header'
   These used a mix of correct and stale v1 numbers → apply corrections
   (Ch 11→10 for Eyes/Face, Ch 12→11 for Micro-Exp, Ch 13 CMR split→14)
   plus the standard remapping.

Also update part header text in the HTML template and part description
strings embedded in build-book.py.
"""

import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('build-book.py', encoding='utf-8') as f:
    src = f.read()

# ── 1. HOOK_LINES / KEY_READS mapping ────────────────────────────────────────
# Keys use v1 manuscript chapter numbers.
HOOK_MAP = {
    12: 13,   # Cold Reading
    13: 14,   # Contact Mind Reading
    14: 15,   # Language of Yes
    15: 16,   # Closing the Barn Door
    16: 12,   # Science of Hypnosis → leads Methods section
    17: 32,   # Mentalism in the Boardroom
    18: 33,   # Why Most Training Fails
    19: 34,   # Influence Without Authority
    20: 35,   # The Ethics of Influence
    21: 17,   # The Performance Arc
    22: 21,   # The Art of Strolling
    23: 22,   # When the Room Rises
    24: 23,   # Audio as Architecture
    25: 24,   # Making the Room Say Yes
    26: 25,   # The Authority Frame
    27: 37,   # Building a Career, Not a Calendar
    28: 38,   # The Intro Video
    29: 18,   # Turning Observation into Performance
    30: 30,   # Insight Demonstrations (same)
    31: 19,   # Method Invisibility
    32: 20,   # Patter, Rhythm, and Silence
    33: 36,   # Where Bookings Are Actually Won
    34: 39,   # Introductions, Bios, and Testimonials
    35: 40,   # The Language of Authority
    36: 41,   # Reading the Booking Room
    37: 42,   # From First Contact to Follow-Up
    38: 26,   # What the Room Decides (FATE)
    39: 27,   # Authority Architecture
    40: 28,   # The Performer's Signal Dictionary
    41: 29,   # How Influence Actually Works
    42: 31,   # Six Steps from Observation to Ovation (DECODE)
}

# ── 2. SECTION_BADGES / FIGURES mapping ──────────────────────────────────────
# Some v1 entries were stale (wrong chapter numbers); handle those first.

# Eyes/Face sections were stale at CHAPTER 11 → correct v2 = CHAPTER 10
EYES_FACE_SECTIONS = {
    'Where the Eyes Go When the Mind Reaches',
    'Fruit to Fang',
    'Pupil Constriction/Dilation',
    'Social Referencing Glance',
    'The Eyebrow Flash',
    'Lip Compression',
    'Directional Preference',
    'Cognitive Load and the Search for the Right Thing',
}

# Micro-Expression sections were stale at CHAPTER 12 → correct v2 = CHAPTER 11
MICRO_EXP_SECTIONS = {
    'The Seven Expressions',
    'The Duchenne Smile',
    'The Leakage Hierarchy',
    'Convergence Rule',
    'Reading in Clusters, Not Snapshots',
    'Microexpressions in Mentalism',
}

# CMR sections were under stale CHAPTER 13 → correct v2 = CHAPTER 14
CMR_SECTIONS = {
    'Muscle Reading',
    'The Method',
    'Focus, Not Clutter',
    'Suggestibility and the Frame',
    'Setting Up the Conditions',
    'The Grip',
    'Verify, Verify, Verify',
    'The Science Behind Contact Mind Reading',
    'Framing the Effect',
    'Intent Cues Beyond the Stage',
}

# Standard SECTION_BADGES/FIGURES chapter mapping (after stale corrections applied)
# Key: old chapter number as it appears in v1 build-book.py
# Value: new chapter number for v2
BADGE_MAP = {
    # Eyes/Face stale 11 → 10
    # Micro-Exp stale 12 → 11
    # CMR stale 13 → 14 (handled above in CMR_SECTIONS)
    # Cold Reading at 13 → stays 13 (no change needed)
    14: 15,   # Language of Yes
    15: 16,   # Closing Barn Door
    16: 12,   # Hypnosis
    17: 32,   # Boardroom
    18: 33,
    19: 34,
    20: 35,
    21: 17,   # Performance Arc
    22: 21,
    23: 22,
    24: 23,
    25: 24,
    26: 25,   # Authority Frame
    27: 37,
    28: 38,
    29: 18,   # Turning Observation
    30: 30,   # Insight Demos (same number)
    31: 19,
    32: 20,
    33: 36,
    34: 39,
    35: 40,
    36: 41,
    37: 42,
    38: 26,   # FATE
    39: 27,
    40: 28,
    41: 29,
    42: 31,
}

# ── Apply simple-key replacements (HOOK_LINES, KEY_READS) ────────────────────
# Pattern: 'CHAPTER N' as a complete dict key (not followed by ':')
# Use temp markers to avoid double-substitution

def replace_simple_keys(text, mapping):
    """Replace 'CHAPTER N' keys using temp markers to avoid conflicts."""
    # Phase 1: old numbers → temp markers
    result = text
    for old_n, new_n in sorted(mapping.items(), reverse=True):
        result = result.replace(f"'CHAPTER {old_n}'", f"'__TMPCH_{new_n}__'")
    # Phase 2: temp markers → new numbers
    result = re.sub(r"'__TMPCH_(\d+)__'", lambda m: f"'CHAPTER {m.group(1)}'", result)
    return result


# ── Apply compound-key replacements (SECTION_BADGES, FIGURES) ────────────────
def replace_compound_keys(text):
    """Replace 'CHAPTER N:Section' keys with correct v2 chapter numbers."""

    def sub(m):
        n = int(m.group(1))
        section = m.group(2)

        # Stale Eyes/Face correction: stale 11 → 10
        if n == 11 and section in EYES_FACE_SECTIONS:
            return f"'CHAPTER 10:{section}'"

        # Stale Micro-Expression correction: stale 12 → 11
        if n == 12 and section in MICRO_EXP_SECTIONS:
            return f"'CHAPTER 11:{section}'"

        # CMR split: stale 13 CMR sections → 14
        if n == 13 and section in CMR_SECTIONS:
            return f"'CHAPTER 14:{section}'"

        # Standard remap
        new_n = BADGE_MAP.get(n, n)
        return f"'CHAPTER {new_n}:{section}'"

    # Match 'CHAPTER N:Section Name' as dict keys
    return re.sub(r"'CHAPTER (\d+):([^']+)'", sub, text)


# ── Execute ───────────────────────────────────────────────────────────────────
updated = src
updated = replace_simple_keys(updated, HOOK_MAP)
updated = replace_compound_keys(updated)

# ── Update part descriptions in the HTML template ────────────────────────────
# The build script has hardcoded part descriptions in the HTML output.
# Update only the parts that change.

PART_DESC_REPLACEMENTS = [
    # Part Three: Field Notes → The Methods
    (
        'Reading Body Language in Real Time\n─',  # anchor - don\'t change
        'Reading Body Language in Real Time\n─',  # same - we change part header separately
    ),
    # Part descriptions embedded in the HTML part header generator
    # These are in the part_html generation section
]

# Update part subtitle strings in the section that generates part HTML
# Find and replace the old part descriptions
OLD_PART_SUBS = [
    # Part Three: old Field Notes description → new Methods description
    (
        'A personal reference library pairing neurobiological findings',
        'Cold reading, contact mind reading, hypnosis, compliance language, '
        'and the core mentalism techniques — each made stronger by the behavioral foundation in Part Two.'
    ),
    # Part Four: old Corporate Stage → new Performance Construction
    (
        'From keynote halls to boardrooms. Behavioral science applied to the professional performance context.',
        'How to build the show: the arc, the craft of revelation, timing, room management, '
        'and the structural decisions that determine whether skill becomes experience.'
    ),
    # Part Five: old Performance Craft → new Authority/Influence
    (
        'The Performance Arc as a chapter, plus show structure, scripting, and effect order.',
        'The invisible architecture that determines whether a performance has power before the first effect begins. '
        'The FATE Model, Authority Architecture, the Signal Dictionary, the Influence Equation, and the DECODE Framework.'
    ),
    # Part Six: old Presence and Perception → new Professional Stage
    (
        'The gap between skilled execution and genuine command. Walk-around, room energy, audio design, compliance engineering, and authority framing.',
        'Behavioral science applied to the professional performance context — '
        'from keynote halls and boardrooms to corporate training and the ethics of influence.'
    ),
    # Part Seven: old Business Brain (stays, but update the reference to Part Eight)
    (
        'Where bookings are actually won, how authority is built before you walk in the room, and the complete Decode Behavior framework for the performing professional.',
        'Where bookings are actually won, how authority is built before you walk in the room, and the business of performing at the highest level.'
    ),
    # Part Eight: old Behavioral Intelligence header → Reference Section note
    (
        'Behavioral Intelligence for the Stage',
        'Reference Section — Field Notes'
    ),
]

for old, new in OLD_PART_SUBS:
    if old in updated:
        updated = updated.replace(old, new, 1)
        print(f'Part desc updated: {old[:50]}...')
    else:
        print(f'NOT FOUND (skipped): {old[:50]}...')

# ── Update any in-text forward references to Part Eight ──────────────────────
# The Authority Frame chapter (now Ch 25) references "Part Eight"
updated = updated.replace(
    'Part Eight provides the complete Authority Architecture framework',
    'Part Five provides the complete Authority Architecture framework'
)
updated = updated.replace(
    'Part Eight: Behavioral Intelligence',
    'Part Five: Authority, Influence, and the Deep Framework'
)

# ── Write updated file ────────────────────────────────────────────────────────
with open('build-book.py', 'w', encoding='utf-8') as f:
    f.write(updated)

# ── Verify ────────────────────────────────────────────────────────────────────
print()
print('build-book.py updated.')
print()

# Check for any remaining old chapter key references
with open('build-book.py', encoding='utf-8') as f:
    final = f.read()

# Report remaining 'CHAPTER N' keys in HOOK_LINES/KEY_READS/SECTION_BADGES/FIGURES
# that should have been transformed
old_keys_remaining = set()
for n in HOOK_MAP.keys():
    if f"'CHAPTER {n}'" in final:
        old_keys_remaining.add(f'CHAPTER {n} (simple key)')
    if f"'CHAPTER {n}:" in final:
        old_keys_remaining.add(f'CHAPTER {n} (compound key)')

if old_keys_remaining:
    print('WARNING: These old keys still present:')
    for k in sorted(old_keys_remaining):
        print(f'  {k}')
else:
    print('All chapter keys remapped — no old keys remaining.')
