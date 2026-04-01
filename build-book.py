#!/usr/bin/env python3
"""
The Architecture of Wonder — Book Design Generator v2
Converts the manuscript into a fully designed HTML book.

Fixes from v1:
- Typographic (curly) quotes throughout
- Title Case section headers properly detected
- Running headers on body pages
- Section breaks (· · ·) properly detected
- "What You Have Felt Before" motif styled distinctly
- Pull quotes generated from strong passages
- Field Notes styled as reference cards
- Better spotlight box content selection
- TOC with dotted leaders and proper spacing
- Fixed text-indent issues
- Proper front matter ordering
- Better paragraph flow and spacing
"""

import re
import html as html_module
import os
import textwrap
import base64
import mimetypes

# ═══════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════

HOOK_LINES = {
    'INTRODUCTION': '"What you are about to read was designed to demonstrate its own content. Every page is a performance."',
    'CHAPTER 1': '"Reality is not what happens. It is what they remember happening."',
    'CHAPTER 2': '"Your audience\u2019s brain is deciding what matters before you open your mouth."',
    'CHAPTER 3': '"The moment before the reveal is worth more than the reveal itself."',
    'CHAPTER 4': '"Dopamine does not reward the outcome. It rewards the anticipation."',
    'CHAPTER 5': '"Attention is not given. It is taken."',
    'CHAPTER 6': '"Authority is not claimed. It is perceived\u2009\u2014\u2009in the first 250 milliseconds."',
    'CHAPTER 7': '"Every person who walks toward you is already broadcasting."',
    'CHAPTER 8': '"Eighty signals. Four tiers. One chain to read them all."',
    'CHAPTER 9': '"Thought does not stay inside the head. The body has been listening the whole time."',
    'CHAPTER 11': '"The face performs. The eyes search."',
    'CHAPTER 12': '"Partial, rapid, and involuntary: the face tells the truth for a fraction of a second before the managed response arrives."',
    'CHAPTER 14': '"You already know more than you think. The trick is knowing what to trust."',
    'CHAPTER 15': '"The volunteer chose you before you chose them."',
    'CHAPTER 16': '"Compliance is not obedience. It is agreement they did not know they gave."',
    'CHAPTER 17': '"The moment after the effect is where the real work happens."',
    'CHAPTER 18': '"The strongest version of an effect is not what happened. It is what they are willing to swear happened."',
    'CHAPTER 13': '"Hypnosis is not what you think it is. That is why it works."',
    'CHAPTER 34': '"The boardroom is the most dangerous stage you will ever work."',
    'CHAPTER 35': '"You cannot teach observation. You can only remove the obstacles to seeing."',
    'CHAPTER 36': '"Every performance teaches you something. Most of the lessons hurt."',
    'CHAPTER 37': '"The most powerful person in the room is rarely the one with the title."',
    'CHAPTER 23': '"Zodiac divination without a single anagram. Every read built from behavior, setting, and the architecture of what people already know."',
    'CHAPTER 24': '"Design backward from the end. The last two minutes are where the hippocampus decides what to keep."',
    'CHAPTER 26': '"The question is never whether to influence. It is whether to admit it."',
    'CHAPTER 27': '"The walk to the stage is the performance."',
    'CHAPTER 28': '"Sound is the invisible stage."',
    'CHAPTER 29': '"The environment gives the instruction before you do."',
    'CHAPTER 39': '"Authority is not claimed. It is perceived."',
    'CHAPTER 40': '"Your career is a performance with a very long run."',
    'CHAPTER 24': '"The best insight demonstration looks like telepathy and works like science."',
    'CHAPTER 25': '"Method invisibility is not misdirection. It is architecture."',
    'CHAPTER 38': '"A performer with perfect reads and poor timing is less effective than the reverse."',
    'CHAPTER 41': '"The booking was won or lost before you picked up the phone."',
    'CHAPTER 42': '"Your introduction is the first frame the audience receives. Control it."',
    'CHAPTER 43': '"What you say matters less than how it sounds when you say it."',
    'CHAPTER 44': '"The client is reading you harder than you are reading them."',
    'CHAPTER 19': '"A psychological force does not always create a thought. Often, it calls one forward."',
    'CHAPTER 20': '"Propless mentalism is the hardest thing to do well and the easiest thing to do badly. That gap is what this chapter closes."',
    'CHAPTER 21': '"Understanding propless mentalism and being able to build it are different skills. This chapter is for the second one."',
    'CHAPTER 30': '"Every framework in this book leads here."',
    'CHAPTER 31': '"FATE is not a model. It is a diagnostic for every performance you will ever give."',
    'CHAPTER 32': '"The periodic table of behavioral elements. Every signal has a weight."',
    'CHAPTER 33': '"Influence is not a trick. It is an equation with variables you can measure."',
    'CHAPTER 33': '"Every framework in this book was designed to work on stage. This one ties them together."',
    'GLOSSARY': '"The language shapes the thinking. Know the words."',
}

KEY_READS = {
    'CHAPTER 1': 'Design the memory, and you design the experience.',
    'CHAPTER 2': 'Salience is not what you show. It is what they cannot ignore.',
    'CHAPTER 3': 'Tension is not the enemy. Boredom is.',
    'CHAPTER 4': 'Delay is not cruelty. It is craft.',
    'CHAPTER 5': 'You cannot give someone an experience they were not paying attention for.',
    'CHAPTER 6': 'Credibility is not what you say. It is what they decide before you say it.',
    'CHAPTER 7': 'The read is never one signal. The read is the chain.',
    'CHAPTER 8': 'Eighty signals. Five filters. One practice.',
    'CHAPTER 9': 'Intention is not invisible. It is just smaller than you were looking for.',
    'CHAPTER 11': 'Handle the person, not the trick.',
    'CHAPTER 12': 'Once you can see the difference between an easy answer and a hunted one, you are no longer just watching thought. You are shaping what the search reveals.',
    'CHAPTER 14': 'The best cold read is a warm observation delivered cold.',
    'CHAPTER 15': 'Seven expressions. One-fifth of a second. That is the window.',
    'CHAPTER 16': 'The best instruction is the one that feels like their idea.',
    'CHAPTER 17': 'Close the moment before they close it for you.',
    'CHAPTER 18': 'The only effect that lasts is the one that survives the retelling. Build for that version, not the version in the room.',
    'CHAPTER 13': 'The trance state is not extraordinary. It is the brain doing what it does best.',
    'CHAPTER 34': 'In the boardroom, the audience writes the review before the show ends.',
    'CHAPTER 35': 'Training is not instruction. It is guided noticing.',
    'CHAPTER 36': 'The face is the performance. The hands are the truth.',
    'CHAPTER 37': 'You have no title on that stage. That is the advantage.',
    'CHAPTER 23': 'The spectator thinks you guessed. What actually happened is that you eliminated everything else.',
    'CHAPTER 24': 'The arc does not exist in the show. It exists in what the audience carries out with them.',
    'CHAPTER 26': 'Ethics is not a constraint. It is the architecture that makes the rest stand.',
    'CHAPTER 27': 'The walk is the show. Everything after is confirmation.',
    'CHAPTER 28': 'Control the sound, and you control the space.',
    'CHAPTER 29': 'Design the compliance. Then act surprised when they comply.',
    'CHAPTER 39': 'Forfeit the game before somebody else takes you out of the frame.',  # deliberate — serial position trough (Linkin Park, Papercut)
    'CHAPTER 40': 'Every room holds the memory of a performance it has not yet seen.',  # deliberate — serial position trough
    'CHAPTER 24': 'The best insight feels impossible because it is grounded in what is actually there.',
    'CHAPTER 25': 'If they are looking for the method, the architecture failed.',
    'CHAPTER 38': 'Silence is not absence. It is the loudest tool you have.',
    'CHAPTER 41': 'The booking is won in the room they never see you in.',
    'CHAPTER 42': 'Your biography arrives before you do. Make sure it is doing the right job.',
    'CHAPTER 43': 'Language is not communication. It is positioning.',
    'CHAPTER 44': 'Read them first. Then let them think they read you.',
    'CHAPTER 19': 'A force that feels like a force has already failed. The method is in the architecture, not the aggression.',
    'CHAPTER 20': 'The method is in service of the experience. The moment that relationship inverts, you are no longer a mentalist. You are a technician showing your work.',
    'CHAPTER 21': 'Enter through the form the thought is already living in. Work your way out to the word from there.',
    'CHAPTER 30': 'Decode is not a technique. It is a way of seeing.',
    'CHAPTER 31': 'Four forces. Every room is already running the equation before you open your mouth.',
    'CHAPTER 32': 'There are no random behaviors. There are only patterns you have not mapped yet.',
    'CHAPTER 33': 'Influence without understanding is manipulation. With understanding, it is leadership.',
    'CHAPTER 33': 'Go see what others miss.',
}

# Per-chapter legend: only the most prevalent tier(s) and observation category/categories.
# tiers: list from ['t1','t2','t3','t4']   cats: list from ['bp','cr','vs','am']
# BP=Behavioral Profiling  CR=Cold Reading  VS=Verbal/Vocal Signals  AM=Audience Management
CHAPTER_LEGEND = {
    'CHAPTER 1':  {'tiers': ['t1'],       'cats': ['am']},
    'CHAPTER 2':  {'tiers': ['t1'],       'cats': ['am']},
    'CHAPTER 3':  {'tiers': ['t1', 't2'], 'cats': ['am']},
    'CHAPTER 4':  {'tiers': ['t1'],       'cats': ['am']},
    'CHAPTER 5':  {'tiers': ['t1', 't2'], 'cats': ['am']},
    'CHAPTER 6':  {'tiers': ['t1', 't2'], 'cats': ['am']},
    'CHAPTER 7':  {'tiers': ['t1', 't2'], 'cats': ['bp']},
    'CHAPTER 8':  {'tiers': ['t2', 't3'], 'cats': ['bp']},
    'CHAPTER 12':  {'tiers': ['t2', 't3'], 'cats': ['bp']},
    'CHAPTER 14': {'tiers': ['t1', 't2'], 'cats': ['bp']},
    'CHAPTER 15': {'tiers': ['t3'],       'cats': ['cr']},
    'CHAPTER 9': {'tiers': ['t2', 't3'], 'cats': ['bp']},
    'CHAPTER 11': {'tiers': ['t2', 't3'], 'cats': ['am']},
    'CHAPTER 16': {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 17': {'tiers': ['t3'],       'cats': ['bp']},
    'CHAPTER 18': {'tiers': ['t2', 't3'], 'cats': ['am', 'vs']},
    'CHAPTER 13': {'tiers': ['t1', 't2'], 'cats': ['am']},
    'CHAPTER 34': {'tiers': ['t2', 't3'], 'cats': ['am']},
    'CHAPTER 35': {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 36': {'tiers': ['t3'],       'cats': ['am']},
    'CHAPTER 37': {'tiers': ['t2', 't3'], 'cats': ['am']},
    'CHAPTER 23': {'tiers': ['t2', 't3'], 'cats': ['cr', 'bp']},
    'CHAPTER 24': {'tiers': ['t1', 't2'], 'cats': ['am']},
    'CHAPTER 26': {'tiers': ['t1', 't2'], 'cats': ['am']},
    'CHAPTER 27': {'tiers': ['t3'],       'cats': ['am']},
    'CHAPTER 28': {'tiers': ['t2', 't3'], 'cats': ['am']},
    'CHAPTER 29': {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 39': {'tiers': ['t1', 't2'], 'cats': ['am']},
    'CHAPTER 40': {'tiers': ['t3'],       'cats': ['am']},
    'CHAPTER 24': {'tiers': ['t2', 't3'], 'cats': ['cr']},
    'CHAPTER 25': {'tiers': ['t3'],       'cats': ['am']},
    'CHAPTER 38': {'tiers': ['t3'],       'cats': ['am']},
    'CHAPTER 41': {'tiers': ['t3'],       'cats': ['am']},
    'CHAPTER 42': {'tiers': ['t3'],       'cats': ['am']},
    'CHAPTER 43': {'tiers': ['t2', 't3'], 'cats': ['vs']},
    'CHAPTER 44': {'tiers': ['t2', 't3'], 'cats': ['bp']},
    'CHAPTER 19': {'tiers': ['t2', 't3'], 'cats': ['am', 'cr']},
    'CHAPTER 20': {'tiers': ['t2', 't3'], 'cats': ['am', 'cr']},
    'CHAPTER 21': {'tiers': ['t2', 't3'], 'cats': ['am', 'cr']},
    'CHAPTER 30': {'tiers': ['t2', 't3'], 'cats': ['bp']},
    'CHAPTER 31': {'tiers': ['t2', 't3'], 'cats': ['am']},
    'CHAPTER 32': {'tiers': ['t2', 't3'], 'cats': ['bp']},
    'CHAPTER 33': {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 33': {'tiers': ['t2', 't3'], 'cats': ['bp']},
}

# T4 signal table data — (signal name, brief read, use category)
T4_SIGNALS = [
    (
        'NLP Eye Movement Direction',
        'Eye direction maps to cognitive mode: visual memory, visual construction, auditory recall, or kinesthetic processing.',
        'BP',
    ),
    (
        'Smooth Lower Eyelids as Confidence Indicator',
        'Relaxed lower eyelids indicate genuine confidence. Tension around the lower eyelid signals concealed anxiety or stress.',
        'BP',
    ),
    (
        'Deep Under-Eye Wrinkles as Chronic Worry Indicator',
        'Deep permanent under-eye wrinkles reflect a lifetime pattern of chronic worry or emotional suppression.',
        'BP',
    ),
    (
        'Hair Part Direction as Personality Indicator',
        'Left = dominance and logic. Right = cooperation and nurturance. Center = balance or ambivalence.',
        'BP',
    ),
]

WHAT_YOU_JUST_DID = {
    3: "You have been reading for approximately three minutes. Notice your breathing. It slowed when you hit the section on cortisol. That is your nervous system responding to content about threat\u2009\u2014\u2009even though the threat is not real. Observation, applied to yourself.",
    7: "You have been reading this page for about ninety seconds. Notice which hand is holding the book. That is Observation #01\u2009\u2014\u2009handedness indicator. You just demonstrated it without thinking.",
    15: "Notice your posture right now. Did you lean forward slightly in the last few paragraphs? That is engagement. Your body responded before your mind decided the content was interesting.",
    21: "You just turned to this chapter. Before reading a word, you formed an impression of its length by glancing at the page count. That is thin-slicing applied to a book. You do this with people too.",
    28: "Your eyes moved to this callout before reading the surrounding text. That is the Von Restorff effect\u2009\u2014\u2009your brain prioritized the visually distinct element. Chapter Two taught you this. The book just demonstrated it.",
    36: "You are in the final section. Notice how your reading pace has changed. If it has accelerated, that is the recency effect\u2009\u2014\u2009your brain knows it is close to the end and is already preparing to consolidate.",
}

PATTERN_INTERRUPTS = [
    {'number': '250', 'unit': 'MILLISECONDS', 'text': 'The time it takes your brain to form a first impression of a stranger.', 'source': 'Willis & Todorov, 2006', 'wyajd': 'You formed yours of this page in less time than that. What did you notice first\u2009\u2014\u2009the number, or the word? That is salience at work.'},
    {'number': '40%', 'unit': 'INCREASE IN TRUST', 'text': 'The boost in perceived credibility when text is set in a highly readable font.', 'source': 'Processing Fluency Research', 'wyajd': 'The font you are reading right now was chosen for this reason.'},
    {'number': '7', 'unit': 'EXPRESSIONS', 'text': 'The number of universal micro-expressions the human face produces. Each lasts less than one-fifth of a second.', 'source': 'Ekman & Friesen, 1971', 'wyajd': ''},
    {'number': '3', 'unit': 'SIGNALS', 'text': 'The minimum number of co-occurring behavioral signals required to form a reliable pattern.', 'source': 'The Five Cs\u2009\u2014\u2009Clusters', 'wyajd': 'One signal is noise. Two is coincidence. Three is a read.'},
    # NOTE: 60,000× FASTER (color processing) is reserved for the Meta Reveal only — do not add back here
    # NOTE: ⅙ OF A SECOND redundant with 7 EXPRESSIONS
    # NOTE: 85% OF DECISIONS (color/purchase) too far from book content
    # NOTE: 5 FILTERS redundant with 3 SIGNALS
]

# ═══════════════════════════════════════════════════════════
# FIGURES — Images injected after specific section headers
# ═══════════════════════════════════════════════════════════

FIGURES = {
    # Key: "CHAPTER <num>:<section header text>" → figure data
    # Note: chapter_key comes from parse_manuscript() numbering, not the TOC
    'CHAPTER 12:The Seven Expressions': {
        'src': 'resources/metv-images/seven-universal-expressions.png',
        'alt': 'The 7 universal microexpressions: Anger, Disgust, Fear, Happiness, Sadness, Surprise, and Contempt',
        'caption': 'Figure 10.1 \u2014 The 7 universal microexpressions: Anger, Disgust, Fear, Happiness, Sadness, Surprise, and Contempt.',
        'rights': 'Author-owned photograph',
    },
    'CHAPTER 12:The Duchenne Smile': {
        'src': 'resources/metv-images/duchenne-smile-comparison.jpg',
        'alt': 'Duchenne Smile (top) vs non-Duchenne smile (bottom) — the eye crease distinguishes genuine from social smiling',
        'caption': 'Figure 10.2 \u2014 The Duchenne Smile (top) engages the orbicularis oculi, producing the eye crease. The non-Duchenne smile (bottom) does not. If the eyes are not involved, the smile is consciously constructed.',
        'rights': 'Author-owned photograph',
    },
    'CHAPTER 11:Lip Compression': {
        'src': 'resources/metv-images/lip-compression-example.png',
        'alt': 'Lip compression — lips pressed together, showing orbicularis oris tension and mentalis chin dimpling',
        'caption': 'Figure 9.1 \u2014 Lip compression. Note the slight dimpling at the chin (mentalis activation) and the tension line below the lower lip (orbicularis oris). The mouth has moved into management.',
        'rights': 'AI-generated illustration',
    },
    'CHAPTER 23:FIRE SIGNS': {
        'src': 'resources/metv-images/zodiac-image1.jpg',
        'alt': 'Fire signs mnemonic: Leo (lion on burning castle), Sagittarius (archers with flaming arrows), Aries (ram)',
        'caption': 'Fire Signs \u2014 Aries, Leo, Sagittarius.',
        'rights': 'AI-generated illustration',
    },
    'CHAPTER 23:WATER SIGNS': {
        'src': 'resources/metv-images/zodiac-image4.jpg',
        'alt': 'Water signs mnemonic: Pisces (fish leaping from ocean), Cancer (crab), Scorpio (scorpion)',
        'caption': 'Water Signs \u2014 Cancer, Scorpio, Pisces.',
        'rights': 'AI-generated illustration',
    },
    'CHAPTER 23:EARTH SIGNS': {
        'src': 'resources/metv-images/zodiac-image2.jpg',
        'alt': 'Earth signs mnemonic: Capricorn (corn field), Taurus (bull ploughing), Virgo (goddess of agriculture)',
        'caption': 'Earth Signs \u2014 Capricorn, Taurus, Virgo.',
        'rights': 'AI-generated illustration',
    },
    'CHAPTER 23:AIR SIGNS': {
        'src': 'resources/metv-images/zodiac-image3.jpg',
        'alt': 'Air signs mnemonic: Gemini (twins in storm), Libra (scales in wind), Aquarius (water-bearer)',
        'caption': 'Air Signs \u2014 Aquarius, Gemini, Libra.',
        'rights': 'AI-generated illustration',
    },
}

# ═══════════════════════════════════════════════════════════
# SECTION BADGES — Tier + category badges injected after section headers
# Key: "CHAPTER <num>:<section header text>" → {tiers, cats}
# Shows readers the evidence tier and observation category for each topic.
# ═══════════════════════════════════════════════════════════

SECTION_BADGES = {
    # ── CHAPTER 1: Designing for Reality ──
    'CHAPTER 1:The Setup Is the Performance':    {'tiers': ['t1'],       'cats': ['am']},
    'CHAPTER 1:Expectation Loading':             {'tiers': ['t1'],       'cats': ['am']},
    'CHAPTER 1:Predictive Processing':           {'tiers': ['t1'],       'cats': ['am']},
    'CHAPTER 1:Cognitive Economy':               {'tiers': ['t1'],       'cats': ['am']},
    # ── CHAPTER 2: Five Forces of Salience ──
    'CHAPTER 2:1. Novelty':                      {'tiers': ['t1'],       'cats': ['am']},
    'CHAPTER 2:2. Emotional Relevance':          {'tiers': ['t1'],       'cats': ['am']},
    'CHAPTER 2:3. Social Signal':                {'tiers': ['t1'],       'cats': ['am']},
    'CHAPTER 2:4. Unresolved Uncertainty':       {'tiers': ['t1'],       'cats': ['am']},
    'CHAPTER 2:5. Contrast':                     {'tiers': ['t1'],       'cats': ['am']},
    'CHAPTER 2:Stacking the Forces':             {'tiers': ['t2'],       'cats': ['am']},
    # ── CHAPTER 3: Tension, Threat and Window ──
    'CHAPTER 3:The Cortisol Threshold':          {'tiers': ['t1'],       'cats': ['am']},
    'CHAPTER 3:Breathing Visibility':            {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 3:Stillness Gradient':              {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 3:The Laughter Signal':             {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 3:Phone Emergence':                 {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 3:Reading the Audience\'s Cortisol Level': {'tiers': ['t2'], 'cats': ['am']},
    # ── CHAPTER 4: Art of Anticipation ──
    'CHAPTER 4:Increasing Dopamine':             {'tiers': ['t1'],       'cats': ['am']},
    'CHAPTER 4:Premature Resolution':            {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 4:Intermittent Structure':          {'tiers': ['t2'],       'cats': ['am']},
    # ── CHAPTER 5: Attention as a Weapon ──
    'CHAPTER 5:The Gorilla Principle':           {'tiers': ['t1'],       'cats': ['am']},
    'CHAPTER 5:Change Blindness':                {'tiers': ['t1'],       'cats': ['am']},
    'CHAPTER 5:Psychological Marking':           {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 5:The Effort Inversion':            {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 5:How to Create the Feeling of Novelty': {'tiers': ['t2'], 'cats': ['am']},
    # ── CHAPTER 6: Behavioral Profiling ──
    'CHAPTER 6:The Foundation: Baseline First':  {'tiers': ['t2'],       'cats': ['bp']},
    'CHAPTER 6:The Five Cs':                     {'tiers': ['t2'],       'cats': ['bp']},
    'CHAPTER 6:Reading Deviation':               {'tiers': ['t2'],       'cats': ['bp']},
    'CHAPTER 6:The Leakage Window':              {'tiers': ['t2'],       'cats': ['bp']},
    'CHAPTER 6:Eye Movement and the Baseline Principle': {'tiers': ['t3'], 'cats': ['bp']},
    'CHAPTER 6:The Three-Signal Rule':           {'tiers': ['t2'],       'cats': ['bp']},
    'CHAPTER 6:Observation Is Not Lie Detection':{'tiers': ['t1'],       'cats': ['bp']},
    'CHAPTER 6:Common Observer Errors':          {'tiers': ['t2'],       'cats': ['bp']},
    'CHAPTER 6:Cultural Calibration in Practice':{'tiers': ['t2'],       'cats': ['bp']},
    # ── CHAPTER 7: 80-Signal System ──
    'CHAPTER 7:The Six-Category Radar':          {'tiers': ['t2'],       'cats': ['bp']},
    'CHAPTER 7:The 10-Second Scan':              {'tiers': ['t2'],       'cats': ['bp']},
    'CHAPTER 7:T4 Signals Removed':              {'tiers': ['t4'],       'cats': ['bp']},
    # ── CHAPTER 8: DISC ──
    'CHAPTER 8:Reading DISC Blends':             {'tiers': ['t3'],       'cats': ['bp']},
    'CHAPTER 8:DISC and Volunteer Strategy':     {'tiers': ['t3'],       'cats': ['am']},
    # ── CHAPTER 9: Eyes/Face ──
    'CHAPTER 11:Where the Eyes Go When the Mind Reaches': {'tiers': ['t3'], 'cats': ['bp']},
    'CHAPTER 11:Fruit to Fang':                   {'tiers': ['t3'],       'cats': ['bp']},
    'CHAPTER 11:Pupil Constriction/Dilation':     {'tiers': ['t2'],       'cats': ['bp']},
    'CHAPTER 11:Social Referencing Glance':       {'tiers': ['t2'],       'cats': ['bp']},
    'CHAPTER 11:The Eyebrow Flash':               {'tiers': ['t2'],       'cats': ['bp']},
    'CHAPTER 11:Lip Compression':                 {'tiers': ['t2'],       'cats': ['bp']},
    'CHAPTER 11:Directional Preference':          {'tiers': ['t3'],       'cats': ['bp']},
    'CHAPTER 11:Cognitive Load and the Search for the Right Thing': {'tiers': ['t2'], 'cats': ['bp']},
    # ── CHAPTER 11: Micro-Expression Matrix ──
    'CHAPTER 12:The Seven Expressions':          {'tiers': ['t1'],       'cats': ['bp']},
    'CHAPTER 12:The Duchenne Smile':             {'tiers': ['t1'],       'cats': ['bp']},
    'CHAPTER 12:The Leakage Hierarchy':          {'tiers': ['t2'],       'cats': ['bp']},
    'CHAPTER 12:Convergence Rule':               {'tiers': ['t2'],       'cats': ['bp']},
    'CHAPTER 12:Reading in Clusters, Not Snapshots': {'tiers': ['t2'],   'cats': ['bp']},
    'CHAPTER 12:Microexpressions in Mentalism':  {'tiers': ['t2'],       'cats': ['bp']},
    # ── CHAPTER 12: Cold Reading ──
    'CHAPTER 14:The Forer Effect':               {'tiers': ['t1'],       'cats': ['cr']},
    'CHAPTER 14:One Name, Three Different Skills':{'tiers': ['t3'],      'cats': ['cr']},
    'CHAPTER 14:The Cold-Warm-Hot Spectrum':     {'tiers': ['t3'],       'cats': ['cr']},
    'CHAPTER 14:Thin Slicing':                   {'tiers': ['t2'],       'cats': ['cr']},
    'CHAPTER 14:The Cold Reading Toolkit':       {'tiers': ['t2', 't3'], 'cats': ['cr', 'bp']},
    'CHAPTER 14:Collocation. Reading How a Person Connects Ideas': {'tiers': ['t3'], 'cats': ['cr']},
    'CHAPTER 14:Visual Signals':                 {'tiers': ['t3'],       'cats': ['cr']},
    'CHAPTER 14:Auditory Signals':               {'tiers': ['t3'],       'cats': ['cr']},
    'CHAPTER 14:Kinesthetic Signals':            {'tiers': ['t3'],       'cats': ['cr']},
    # ── CHAPTER 14: Contact Mind Reading ──
    'CHAPTER 15:Muscle Reading':                        {'tiers': ['t2'],       'cats': ['bp']},
    'CHAPTER 15:The Method':                            {'tiers': ['t2'],       'cats': ['bp']},
    'CHAPTER 15:Focus, Not Clutter':                    {'tiers': ['t2'],       'cats': ['bp']},
    'CHAPTER 15:Suggestibility and the Frame':          {'tiers': ['t2'],       'cats': ['bp']},
    'CHAPTER 15:Setting Up the Conditions':             {'tiers': ['t3'],       'cats': ['bp']},
    'CHAPTER 15:The Grip':                              {'tiers': ['t3'],       'cats': ['bp']},
    'CHAPTER 15:Verify, Verify, Verify':                {'tiers': ['t3'],       'cats': ['bp']},
    'CHAPTER 15:The Science Behind Contact Mind Reading': {'tiers': ['t1'],     'cats': ['bp']},
    'CHAPTER 15:Framing the Effect':                    {'tiers': ['t3'],       'cats': ['bp']},
    'CHAPTER 15:Intent Cues Beyond the Stage':          {'tiers': ['t3'],       'cats': ['bp']},
    # ── CHAPTER 9: Volunteer's Brain ──
    'CHAPTER 9:Seven Volunteer Types':                  {'tiers': ['t3'],       'cats': ['vs']},
    'CHAPTER 9:The Volunteer Selection Matrix':         {'tiers': ['t3'],       'cats': ['vs']},
    'CHAPTER 9:Anchoring in Performance':               {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 9:The Neural Selection Circuit':           {'tiers': ['t2'],       'cats': ['vs']},
    # ── CHAPTER 16: Architecture of Obedience ──
    'CHAPTER 16:Pacing and Leading':             {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 16:Yes Sets':                       {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 16:Double Binds':                   {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 16:Presupposition Check':           {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 16:Degrees of Certainty':           {'tiers': ['t2'],       'cats': ['am']},
    # ── CHAPTER 16: Closing the Barn Door ──
    'CHAPTER 17:The Memory Problem':             {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 17:The Language of Preemptive Closure': {'tiers': ['t2'],   'cats': ['am']},
    # ── CHAPTER 17: Science of Hypnosis ──
    'CHAPTER 13:The Neuroscience of Hypnosis, Down to the Cell Level': {'tiers': ['t1'], 'cats': ['am']},
    'CHAPTER 13:What the Brain Is Doing at the Network Level': {'tiers': ['t1'], 'cats': ['am']},
    'CHAPTER 13:The Rainville Finding':          {'tiers': ['t1'],       'cats': ['am']},
    'CHAPTER 13:Hypnotic Responsiveness vs. Compliance': {'tiers': ['t2'], 'cats': ['am']},
    'CHAPTER 13:Down to the Cell Level':         {'tiers': ['t1'],       'cats': ['am']},
    'CHAPTER 13:Pain as a Model for Understanding Hypnosis': {'tiers': ['t1'], 'cats': ['am']},
    # ── CHAPTER 20: Mentalism in Boardroom ──
    'CHAPTER 35:Credibility as the First Act':   {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 35:Corporate Audience Signals':     {'tiers': ['t3'],       'cats': ['bp']},
    'CHAPTER 35:The Real Power Map':             {'tiers': ['t3'],       'cats': ['bp']},
    # ── CHAPTER 21: Behavioral Training ──
    'CHAPTER 36:Why Most Training Fails':        {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 36:The Hippocampus Test':           {'tiers': ['t2'],       'cats': ['am']},
    # ── CHAPTER 23: Influence Without Authority ──
    'CHAPTER 37:Compliance vs. Internalization': {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 37:The Self-Attribution Principle': {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 37:The Mirror Technique':           {'tiers': ['t3'],       'cats': ['am']},
    # ── CHAPTER 24: Ethics of Influence ──
    'CHAPTER 38:The Consent Framework':          {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 38:The Manipulation Line':          {'tiers': ['t2'],       'cats': ['am']},
    # ── CHAPTER 25: The Performance Arc ──
    'CHAPTER 20:Seven Stages of the Performance Arc':      {'tiers': ['t1'],       'cats': ['am']},
    'CHAPTER 20:The Neural Performance Checklist':         {'tiers': ['t1'],       'cats': ['am']},
    'CHAPTER 20:The Performance Architecture Framework':   {'tiers': ['t1', 't2'], 'cats': ['am']},
    # ── CHAPTER 26: Art of Strolling ──
    'CHAPTER 25:State Architecture':             {'tiers': ['t3'],       'cats': ['am']},
    'CHAPTER 25:The 90-Second Set Structure':    {'tiers': ['t3'],       'cats': ['am']},
    # ── CHAPTER 27: Duration Neglect / Standing Ovation ──
    'CHAPTER 26:Duration Neglect':               {'tiers': ['t1'],       'cats': ['am']},
    'CHAPTER 26:Peak vs. Close':                 {'tiers': ['t2'],       'cats': ['am']},
    # ── CHAPTER 27: Audio as Architecture ──
    # ── CHAPTER 28: Compliance by Design ──
    'CHAPTER 27:Mirror Neurons and Modeling':    {'tiers': ['t1'],       'cats': ['am']},
    'CHAPTER 27:The Compliance Arc':             {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 27:Creepy Collapses the Frame':     {'tiers': ['t3'],       'cats': ['am']},
    # ── CHAPTER 29: Authority Frame ──
    'CHAPTER 28:The Five Pillars of Authority':  {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 28:Certainty Under Pressure':       {'tiers': ['t3'],       'cats': ['am']},
    'CHAPTER 28:The Congruence Gap':             {'tiers': ['t3'],       'cats': ['bp']},
    'CHAPTER 28:Five Speech Patterns That Build Instant Authority': {'tiers': ['t2'], 'cats': ['am']},
    # ── CHAPTER 32: Signal to Statement ──
    'CHAPTER 21:The Opening Read':               {'tiers': ['t2'],       'cats': ['bp']},
    'CHAPTER 21:The T1 Opener':                  {'tiers': ['t1'],       'cats': ['bp']},
    'CHAPTER 21:The Behavioral Opener':          {'tiers': ['t2'],       'cats': ['bp']},
    'CHAPTER 21:The Layered Read':               {'tiers': ['t2'],       'cats': ['cr']},
    # ── CHAPTER 33: Insight Demonstrations ──
    'CHAPTER 33:01 \u2014 The Travel Pattern Read': {'tiers': ['t3'],    'cats': ['cr']},
    'CHAPTER 33:02 \u2014 The Life Pivot Read':  {'tiers': ['t3'],       'cats': ['cr']},
    'CHAPTER 33:03 \u2014 The Hidden Interest Read': {'tiers': ['t3'],   'cats': ['cr']},
    # ── CHAPTER 34: Method Invisibility ──
    'CHAPTER 23:Separate Method from Payoff':    {'tiers': ['t3'],       'cats': ['am']},
    'CHAPTER 23:Anti-Backtracking Architecture': {'tiers': ['t3'],       'cats': ['am']},
    # ── CHAPTER 36: Where Bookings Are Won ──
    'CHAPTER 39:The Limbic Ledger':              {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 39:Referral Psychology':            {'tiers': ['t2'],       'cats': ['am']},
    # ── CHAPTER 38: Language of Authority ──
    'CHAPTER 43:Processing Fluency':             {'tiers': ['t1'],       'cats': ['am']},
    'CHAPTER 43:Declaration vs. Invitation':     {'tiers': ['t2'],       'cats': ['am']},
    # ── CHAPTER 39: Reading the Booking Room ──
    'CHAPTER 44:Establishing the Baseline':      {'tiers': ['t2'],       'cats': ['bp']},
    'CHAPTER 44:Third Person to First Person':   {'tiers': ['t3'],       'cats': ['am']},
    # ── CHAPTER 41: FATE Model ──
    'CHAPTER 29:How the Brain Builds Experience Before It Receives It': {'tiers': ['t1'], 'cats': ['am']},
    'CHAPTER 29:The FATE Model':                 {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 29:F \u2014 Focus':                 {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 29:A \u2014 Authority':             {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 29:T \u2014 Tribe':                 {'tiers': ['t3'],       'cats': ['am']},
    'CHAPTER 29:E \u2014 Emotion':               {'tiers': ['t2'],       'cats': ['am']},
    # ── CHAPTER 42: Authority Architecture ──
    'CHAPTER 30:The Five Pillars of Authority':  {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 30:Pillar One: Confidence':         {'tiers': ['t3'],       'cats': ['am']},
    # ── CHAPTER 43: Performer's Signal Dictionary ──
    'CHAPTER 31:Cluster One: Engagement Retreat':{'tiers': ['t3'],       'cats': ['bp']},
    'CHAPTER 31:Cluster Two: Evaluation':        {'tiers': ['t3'],       'cats': ['bp']},
    'CHAPTER 31:Cluster Three: Certainty Drop':  {'tiers': ['t3'],       'cats': ['bp']},
    # ── CHAPTER 44: Influence Equation ──
    'CHAPTER 32:The Two Components':             {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 32:Compliance Architecture':        {'tiers': ['t2'],       'cats': ['am']},
    # ── CHAPTER 44: DECODE Framework ──
    'CHAPTER 34:D \u2014 Detect':                {'tiers': ['t2'],       'cats': ['bp']},
    'CHAPTER 34:E \u2014 Engage':                {'tiers': ['t2'],       'cats': ['am']},
    'CHAPTER 34:C \u2014 Calibrate':             {'tiers': ['t2'],       'cats': ['bp']},
    'CHAPTER 34:O \u2014 Observe':               {'tiers': ['t2'],       'cats': ['bp']},
    'CHAPTER 34:D \u2014 Decode':                {'tiers': ['t2'],       'cats': ['bp']},
    'CHAPTER 34:E \u2014 Elevate':               {'tiers': ['t2'],       'cats': ['am']},
}

def gen_section_badge_strip(tiers, cats):
    """Compact inline tier+category strip shown beneath section headers."""
    _all_tiers = ['t1', 't2', 't3', 't4']
    _all_cats  = ['bp', 'cr', 'vs', 'am']
    tier_html = ''.join(
        f'<span class="badge {t}">{t.upper()}</span>'
        for t in _all_tiers if t in tiers
    )
    cat_html = ''.join(
        f'<span class="sec-cat-pill {c}">{c.upper()}</span>'
        for c in _all_cats if c in cats
    )
    return f'<div class="section-badge-strip">{tier_html}<span class="sbs-divider"></span>{cat_html}</div>'

# ═══════════════════════════════════════════════════════════
# THE FIVE Cs FRAMEWORK — Injected at beginning of Chapter 7
# ═══════════════════════════════════════════════════════════

FIVE_CS_HTML = '''
<div class="five-cs-inline">
  <div class="fci-header">THE FIVE C&#8217;s OF BEHAVIORAL READING</div>
  <div class="fci-grid">
    <div class="fci-item" data-c="context">
      <div class="fci-name">Context</div>
      <div class="fci-q">What environment?</div>
      <div class="fci-rule">Context determines meaning. Always.</div>
    </div>
    <div class="fci-item" data-c="clusters">
      <div class="fci-name">Clusters</div>
      <div class="fci-q">Multiple signals?</div>
      <div class="fci-rule">Never act on a single signal.</div>
    </div>
    <div class="fci-item" data-c="congruence">
      <div class="fci-name">Congruence</div>
      <div class="fci-q">Body = words?</div>
      <div class="fci-rule">Incongruence is your most reliable signal.</div>
    </div>
    <div class="fci-item" data-c="consistency">
      <div class="fci-name">Consistency</div>
      <div class="fci-q">Their baseline?</div>
      <div class="fci-rule">Without baseline, every read is a projection.</div>
    </div>
    <div class="fci-item" data-c="culture">
      <div class="fci-name">Culture</div>
      <div class="fci-q">Background norms?</div>
      <div class="fci-rule">Calibrate before concluding.</div>
    </div>
  </div>
  <div class="fci-chain">
    <span class="chain-pill" data-c="context">Context</span>
    <span class="chain-arrow">›</span>
    <span class="chain-pill" data-c="clusters">Clusters</span>
    <span class="chain-arrow">›</span>
    <span class="chain-pill" data-c="congruence">Congruence</span>
    <span class="chain-arrow">›</span>
    <span class="chain-pill" data-c="consistency">Consistency</span>
    <span class="chain-arrow">›</span>
    <span class="chain-pill" data-c="culture">Culture</span>
    <span class="chain-arrow">›</span>
    <span class="chain-pill chain-read">READ</span>
  </div>
</div>

<div class="section-break">· · ·</div>
'''

DISC_HTML = '''
<div class="disc-chart">
  <div class="disc-graphic">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 620" font-family="Montserrat, sans-serif">
  <defs>
    <linearGradient id="bgDisc" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#080F1A"/>
      <stop offset="100%" stop-color="#0D1E30"/>
    </linearGradient>
  </defs>
  <rect width="800" height="620" fill="url(#bgDisc)" rx="8"/>

  <!-- Title -->
  <text x="400" y="36" text-anchor="middle" fill="#C9A84C" font-size="13" letter-spacing="4" font-weight="700">THE DISC COMMUNICATION STYLES</text>
  <line x1="180" y1="49" x2="620" y2="49" stroke="#C9A84C" stroke-width="0.5" opacity="0.6"/>
  <text x="400" y="66" text-anchor="middle" fill="#8A9AB5" font-size="11">Read the style. Adjust the approach. Before you speak.</text>

  <!-- Axis labels -->
  <text x="400" y="88" text-anchor="middle" fill="#8A9AB5" font-size="10" letter-spacing="2">FAST-PACED · DECISIVE</text>
  <text x="400" y="594" text-anchor="middle" fill="#8A9AB5" font-size="10" letter-spacing="2">SLOW-PACED · DELIBERATE</text>
  <text x="42" y="348" text-anchor="middle" fill="#8A9AB5" font-size="10" letter-spacing="2" transform="rotate(-90 42 348)">TASK-FOCUSED</text>
  <text x="758" y="348" text-anchor="middle" fill="#8A9AB5" font-size="10" letter-spacing="2" transform="rotate(90 758 348)">PEOPLE-FOCUSED</text>

  <!-- Crosshairs -->
  <line x1="60" y1="346" x2="740" y2="346" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
  <line x1="400" y1="96" x2="400" y2="580" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>

  <!-- ── D: top-left (Fast + Task) ── -->
  <rect x="62" y="98" width="334" height="244" rx="5" fill="#A83030" fill-opacity="0.10" stroke="#A83030" stroke-width="1" stroke-opacity="0.4"/>
  <circle cx="108" cy="138" r="24" fill="#A83030" fill-opacity="0.22"/>
  <text x="108" y="146" text-anchor="middle" fill="#A83030" font-size="24" font-weight="700">D</text>
  <text x="145" y="132" fill="#FFFFFF" font-size="14" font-weight="700">DIRECT</text>
  <text x="145" y="150" fill="#8A9AB5" font-size="11">Fast · Decisive · Results-focused</text>
  <line x1="76" y1="165" x2="384" y2="165" stroke="#A83030" stroke-width="0.5" stroke-opacity="0.4"/>
  <text x="76" y="184" fill="#8A9AB5" font-size="10" font-weight="600">ON STAGE</text>
  <text x="76" y="201" fill="#FFFFFF" font-size="10.5">Skip the warm-up. Lead with precision.</text>
  <text x="76" y="218" fill="#FFFFFF" font-size="10.5">One dead-accurate specific wins them.</text>
  <text x="76" y="241" fill="#A83030" font-size="10" font-style="italic">Fast walk · Forward lean · Direct eye contact</text>
  <text x="76" y="257" fill="#A83030" font-size="10" font-style="italic">Speaks first · Occupies space</text>
  <text x="76" y="328" fill="#A83030" font-size="11" font-weight="700">PRECISION IS CURRENCY</text>

  <!-- ── I: top-right (Fast + People) ── -->
  <rect x="404" y="98" width="334" height="244" rx="5" fill="#C9A84C" fill-opacity="0.08" stroke="#C9A84C" stroke-width="1" stroke-opacity="0.4"/>
  <circle cx="450" cy="138" r="24" fill="#C9A84C" fill-opacity="0.18"/>
  <text x="450" y="146" text-anchor="middle" fill="#C9A84C" font-size="24" font-weight="700">I</text>
  <text x="487" y="132" fill="#FFFFFF" font-size="14" font-weight="700">INFLUENTIAL</text>
  <text x="487" y="150" fill="#8A9AB5" font-size="11">Expressive · Social · Enthusiastic</text>
  <line x1="418" y1="165" x2="726" y2="165" stroke="#C9A84C" stroke-width="0.5" stroke-opacity="0.4"/>
  <text x="418" y="184" fill="#8A9AB5" font-size="10" font-weight="600">ON STAGE</text>
  <text x="418" y="201" fill="#FFFFFF" font-size="10.5">Ideal reactor. Give them a visible role.</text>
  <text x="418" y="218" fill="#FFFFFF" font-size="10.5">Their enthusiasm gives the room permission.</text>
  <text x="418" y="241" fill="#C9A84C" font-size="10" font-style="italic">Open posture · Frequent smiling</text>
  <text x="418" y="257" fill="#C9A84C" font-size="10" font-style="italic">Immediate humor response · Forward lean</text>
  <text x="418" y="328" fill="#C9A84C" font-size="11" font-weight="700">REACTION IS THE EFFECT</text>

  <!-- ── C: bottom-left (Slow + Task) ── -->
  <rect x="62" y="350" width="334" height="228" rx="5" fill="#6B52A0" fill-opacity="0.10" stroke="#6B52A0" stroke-width="1" stroke-opacity="0.4"/>
  <circle cx="108" cy="390" r="24" fill="#6B52A0" fill-opacity="0.22"/>
  <text x="108" y="398" text-anchor="middle" fill="#6B52A0" font-size="24" font-weight="700">C</text>
  <text x="145" y="384" fill="#FFFFFF" font-size="14" font-weight="700">CONSCIENTIOUS</text>
  <text x="145" y="402" fill="#8A9AB5" font-size="11">Analytical · Precise · Detail-oriented</text>
  <line x1="76" y1="417" x2="384" y2="417" stroke="#6B52A0" stroke-width="0.5" stroke-opacity="0.4"/>
  <text x="76" y="436" fill="#8A9AB5" font-size="10" font-weight="600">ON STAGE</text>
  <text x="76" y="453" fill="#FFFFFF" font-size="10.5">Logic must precede compliance.</text>
  <text x="76" y="470" fill="#FFFFFF" font-size="10.5">Slow-burn reveals. Avoid rapid-fire.</text>
  <text x="76" y="493" fill="#6B52A0" font-size="10" font-style="italic">Balanced posture · Measured speech</text>
  <text x="76" y="509" fill="#6B52A0" font-size="10" font-style="italic">Deliberate pauses · Careful object handling</text>
  <text x="76" y="562" fill="#6B52A0" font-size="11" font-weight="700">BUILD COHERENCE FIRST</text>

  <!-- ── S: bottom-right (Slow + People) ── -->
  <rect x="404" y="350" width="334" height="228" rx="5" fill="#1A8FA8" fill-opacity="0.08" stroke="#1A8FA8" stroke-width="1" stroke-opacity="0.4"/>
  <circle cx="450" cy="390" r="24" fill="#1A8FA8" fill-opacity="0.18"/>
  <text x="450" y="398" text-anchor="middle" fill="#1A8FA8" font-size="24" font-weight="700">S</text>
  <text x="487" y="384" fill="#FFFFFF" font-size="14" font-weight="700">STEADY</text>
  <text x="487" y="402" fill="#8A9AB5" font-size="11">Calm · Cooperative · Supportive</text>
  <line x1="418" y1="417" x2="726" y2="417" stroke="#1A8FA8" stroke-width="0.5" stroke-opacity="0.4"/>
  <text x="418" y="436" fill="#8A9AB5" font-size="10" font-weight="600">ON STAGE</text>
  <text x="418" y="453" fill="#FFFFFF" font-size="10.5">Cooperates without resistance.</text>
  <text x="418" y="470" fill="#FFFFFF" font-size="10.5">Slow the pace. Warm, clear framing.</text>
  <text x="418" y="493" fill="#1A8FA8" font-size="10" font-style="italic">Minimal movement · Relaxed shoulders</text>
  <text x="418" y="509" fill="#1A8FA8" font-size="10" font-style="italic">Settled posture · Unhurried speech</text>
  <text x="418" y="562" fill="#1A8FA8" font-size="11" font-weight="700">PATIENCE IS THE ASSET</text>

  <!-- Center badge -->
  <rect x="372" y="332" width="56" height="28" rx="4" fill="#0D1E30" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
  <text x="400" y="350" text-anchor="middle" fill="#8A9AB5" font-size="10" letter-spacing="1">DISC</text>

  <!-- Footer -->
  <text x="400" y="610" text-anchor="middle" fill="#3A4A5C" font-size="9">THE ARCHITECTURE OF WONDER  |  CHAPTER 8: THE FOUR PERSONALITIES</text>
</svg>
  </div>
</div>
'''


# ── Ch11: Leakage Hierarchy visual ───────────────────────────────────────────
LEAKAGE_HIERARCHY_HTML = '''
<div style="margin:1.4em 0 1.2em;background:#080e1a;border-radius:6px;overflow:hidden;border:1px solid rgba(255,255,255,0.07);">
  <div style="font-size:0.67em;letter-spacing:0.16em;color:#4a5e7a;text-transform:uppercase;padding:0.85em 1.4em 0.7em;border-bottom:1px solid rgba(255,255,255,0.05);">The Leakage Hierarchy — Most to Least Managed</div>
  <div style="display:grid;grid-template-columns:120px 1fr;font-size:0.85em;">
    <div style="padding:0.65em 0.8em 0.65em 1.4em;border-bottom:1px solid rgba(255,255,255,0.04);color:white;font-weight:bold;">Face</div>
    <div style="padding:0.65em 1.4em 0.65em 0.4em;border-bottom:1px solid rgba(255,255,255,0.04);color:#7a8ba8;">Most managed &nbsp;·&nbsp; highest social training</div>
    <div style="padding:0.65em 0.8em 0.65em 1.4em;border-bottom:1px solid rgba(255,255,255,0.04);color:white;font-weight:bold;">Upper Body</div>
    <div style="padding:0.65em 1.4em 0.65em 0.4em;border-bottom:1px solid rgba(255,255,255,0.04);color:#7a8ba8;">Moderate management</div>
    <div style="padding:0.65em 0.8em 0.65em 1.4em;border-bottom:1px solid rgba(255,255,255,0.04);color:white;font-weight:bold;">Hands</div>
    <div style="padding:0.65em 1.4em 0.65em 0.4em;border-bottom:1px solid rgba(255,255,255,0.04);color:#7a8ba8;">Less managed &nbsp;·&nbsp; self-soothing reveals</div>
    <div style="padding:0.65em 0.8em 0.65em 1.4em;color:#C9A84C;font-weight:bold;">Feet</div>
    <div style="padding:0.65em 1.4em 0.65em 0.4em;color:#C9A84C;">Least managed &nbsp;·&nbsp; most honest</div>
  </div>
</div>
'''


# ── Cold Reading: Three Opener Frameworks visual ─────────────────────────────
THREE_OPENERS_HTML = '''
<div style="margin:2em 0 2.5em;page-break-inside:avoid;background:#0d1117;border-radius:6px;overflow:hidden;border:1px solid rgba(255,255,255,0.07);">
  <div style="padding:0.7em 1.4em;border-bottom:1px solid #1c2535;">
    <span style="font-size:0.65em;letter-spacing:0.28em;color:#4a5e7a;text-transform:uppercase;font-weight:600;">Three Opener Frameworks</span>
  </div>

  <!-- Card 1: T1 Opener -->
  <div style="background:#131920;border-left:5px solid #C9A84C;padding:1.2em 1.4em 1.1em;border-bottom:1px solid #1c2535;">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.6em;">
      <div style="font-size:0.8em;font-weight:700;color:#C9A84C;letter-spacing:0.18em;text-transform:uppercase;">The T1 Opener</div>
      <div style="display:flex;gap:5px;flex-shrink:0;">
        <span style="background:#C9A84C;color:#0d1117;font-size:0.65em;font-weight:700;padding:2px 7px;border-radius:3px;letter-spacing:0.05em;">T1</span>
        <span style="background:rgba(201,168,76,0.15);color:#C9A84C;font-size:0.65em;padding:2px 7px;border-radius:3px;letter-spacing:0.05em;">BP</span>
      </div>
    </div>
    <div style="font-size:0.84em;color:#7a8ba8;line-height:1.6;margin-bottom:0.9em;">Lead with a physical evidence read. T1 signals require no conversation, no setup, and no interpretation &mdash; they are facts anchored to the body. The precision reads as impossible to anyone who met you thirty seconds ago.</div>
    <div style="border-top:1px solid #1e2a3a;padding-top:0.8em;">
      <div style="font-size:0.62em;letter-spacing:0.2em;color:#4a5e7a;text-transform:uppercase;margin-bottom:0.5em;">Sample Script</div>
      <div style="font-size:0.87em;color:#c0cce0;font-style:italic;line-height:1.7;">&lsquo;I want to start with you specifically &mdash; not because of anything you&rsquo;ve said, but because of something I noticed when you walked in. You&rsquo;ve been on your feet most of today. Not because you had to be. Because that&rsquo;s how you think.&rsquo;</div>
      <div style="font-size:0.75em;color:#3a4f66;margin-top:0.6em;">Anchored to: shoe sole wear pattern &middot; trouser crease relaxation &middot; posture shift when seated</div>
    </div>
  </div>

  <!-- Card 2: Behavioral Opener -->
  <div style="background:#0f1720;border-left:5px solid #1A8FA8;padding:1.2em 1.4em 1.1em;border-bottom:1px solid #1c2535;">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.6em;">
      <div style="font-size:0.8em;font-weight:700;color:#1A8FA8;letter-spacing:0.18em;text-transform:uppercase;">The Behavioral Opener</div>
      <div style="display:flex;gap:5px;flex-shrink:0;">
        <span style="background:#1A8FA8;color:white;font-size:0.65em;font-weight:700;padding:2px 7px;border-radius:3px;letter-spacing:0.05em;">T2</span>
        <span style="background:rgba(26,143,168,0.15);color:#1A8FA8;font-size:0.65em;padding:2px 7px;border-radius:3px;letter-spacing:0.05em;">BP</span>
      </div>
    </div>
    <div style="font-size:0.84em;color:#7a8ba8;line-height:1.6;margin-bottom:0.9em;">Lead with a DISC-based personality read. Fast, broad, and specific enough to feel personal without requiring defense. Particularly effective for high-D and high-C profiles where certainty and precision land harder than warmth.</div>
    <div style="border-top:1px solid #1e2a3a;padding-top:0.8em;">
      <div style="font-size:0.62em;letter-spacing:0.2em;color:#4a5e7a;text-transform:uppercase;margin-bottom:0.5em;">Sample Script</div>
      <div style="font-size:0.87em;color:#c0cce0;font-style:italic;line-height:1.7;">&lsquo;You&rsquo;re someone who decides quickly and explains later. That&rsquo;s not impatience. That&rsquo;s a specific kind of intelligence. The people around you don&rsquo;t always understand the gap between where you are and where they&rsquo;re still standing.&rsquo;</div>
      <div style="font-size:0.75em;color:#3a4f66;margin-top:0.6em;">Anchored to: DISC behavioral cluster &middot; confidence signals &middot; pace and decision indicators from the 10-Second Scan</div>
    </div>
  </div>

  <!-- Card 3: Social Opener -->
  <div style="background:#131920;border-left:5px solid #6B52A0;padding:1.2em 1.4em 1.1em;">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.6em;">
      <div style="font-size:0.8em;font-weight:700;color:#6B52A0;letter-spacing:0.18em;text-transform:uppercase;">The Social Opener</div>
      <div style="display:flex;gap:5px;flex-shrink:0;">
        <span style="background:rgba(107,82,160,0.2);color:#6B52A0;font-size:0.65em;padding:2px 7px;border-radius:3px;letter-spacing:0.05em;">BP</span>
      </div>
    </div>
    <div style="font-size:0.84em;color:#7a8ba8;line-height:1.6;margin-bottom:0.9em;">Open with a read about the subject&rsquo;s social role. Particularly powerful in strolling work where the group dynamic is visible before you approach. The room has already told you who this person is. You are reading the room&rsquo;s answer.</div>
    <div style="border-top:1px solid #1e2a3a;padding-top:0.8em;">
      <div style="font-size:0.62em;letter-spacing:0.2em;color:#4a5e7a;text-transform:uppercase;margin-bottom:0.5em;">Sample Script</div>
      <div style="font-size:0.87em;color:#c0cce0;font-style:italic;line-height:1.7;">&lsquo;Before I start. You&rsquo;re not the one who organized this evening, but you&rsquo;re the reason most of these people are enjoying it.&rsquo;</div>
      <div style="font-size:0.75em;color:#3a4f66;margin-top:0.6em;">Anchored to: energy level &middot; eye contact pattern across the group &middot; who others look to before laughing</div>
    </div>
  </div>
</div>
'''


# ── Ch10: Behavioral Reading vs. Profiling definition callout ────────────────
BEHAVIORAL_READING_DEF_HTML = '''
<div style="display:grid;grid-template-columns:1fr 44px 1fr;margin:1.8em 0 2em;background:#080e1a;border-radius:6px;overflow:hidden;border:1px solid rgba(255,255,255,0.07);">
  <div style="padding:1.5em 1.8em;">
    <div style="font-size:0.67em;letter-spacing:0.16em;color:#4a5e7a;text-transform:uppercase;margin-bottom:0.75em;">Chapters 6 – 9</div>
    <div style="font-size:0.92em;color:white;font-weight:bold;margin-bottom:0.65em;letter-spacing:0.02em;">Behavioral Profiling</div>
    <div style="font-size:0.83em;color:#8a9ab8;line-height:1.65;">Grouping repeated behavioral patterns to predict likely tendencies and future behavior.</div>
  </div>
  <div style="display:flex;align-items:center;justify-content:center;background:#0d1320;">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M5 12h14M13 6l6 6-6 6" stroke="#C9A84C" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
  </div>
  <div style="padding:1.5em 1.8em;border-left:1px solid rgba(255,255,255,0.06);">
    <div style="font-size:0.67em;letter-spacing:0.16em;color:#C9A84C;text-transform:uppercase;margin-bottom:0.75em;">Chapter 10 onwards</div>
    <div style="font-size:0.92em;color:white;font-weight:bold;margin-bottom:0.65em;letter-spacing:0.02em;">Behavioral Reading</div>
    <div style="font-size:0.83em;color:#8a9ab8;line-height:1.65;">Reading behavior in real time to glean information about thoughts, feelings, and internal processing.</div>
  </div>
</div>
'''


# ── DECODE Framework reference panel ─────────────────────────────────────────
DECODE_PANEL_HTML = '''
<div style="margin:2em 0 2.5em;page-break-inside:avoid;">
  <div style="background:#0d1117;border-radius:6px;border:1px solid rgba(201,168,76,0.25);overflow:hidden;">
    <div style="background:rgba(201,168,76,0.08);padding:0.75em 1.4em;border-bottom:1px solid rgba(201,168,76,0.2);">
      <span style="font-size:0.68em;letter-spacing:0.18em;color:#C9A84C;text-transform:uppercase;font-weight:700;">The DECODE Framework</span>
    </div>
    <div style="padding:0.25em 0;">
      <div style="display:flex;align-items:baseline;padding:0.75em 1.4em;border-bottom:1px solid rgba(255,255,255,0.04);">
        <span style="font-size:1.35em;font-weight:800;color:#C9A84C;letter-spacing:0.04em;min-width:1.6em;line-height:1;">D</span>
        <div>
          <span style="font-size:0.78em;font-weight:700;color:#e8dfc8;letter-spacing:0.08em;text-transform:uppercase;">Detect</span>
          <span style="font-size:0.78em;color:#7a8ba0;margin-left:0.6em;">Observe before acting. Establish baseline first.</span>
        </div>
      </div>
      <div style="display:flex;align-items:baseline;padding:0.75em 1.4em;border-bottom:1px solid rgba(255,255,255,0.04);background:rgba(255,255,255,0.015);">
        <span style="font-size:1.35em;font-weight:800;color:#C9A84C;letter-spacing:0.04em;min-width:1.6em;line-height:1;">E</span>
        <div>
          <span style="font-size:0.78em;font-weight:700;color:#e8dfc8;letter-spacing:0.08em;text-transform:uppercase;">Engage</span>
          <span style="font-size:0.78em;color:#7a8ba0;margin-left:0.6em;">Position as peer, not performer.</span>
        </div>
      </div>
      <div style="display:flex;align-items:baseline;padding:0.75em 1.4em;border-bottom:1px solid rgba(255,255,255,0.04);">
        <span style="font-size:1.35em;font-weight:800;color:#C9A84C;letter-spacing:0.04em;min-width:1.6em;line-height:1;">C</span>
        <div>
          <span style="font-size:0.78em;font-weight:700;color:#e8dfc8;letter-spacing:0.08em;text-transform:uppercase;">Calibrate</span>
          <span style="font-size:0.78em;color:#7a8ba0;margin-left:0.6em;">Match pace and communication style.</span>
        </div>
      </div>
      <div style="display:flex;align-items:baseline;padding:0.75em 1.4em;border-bottom:1px solid rgba(255,255,255,0.04);background:rgba(255,255,255,0.015);">
        <span style="font-size:1.35em;font-weight:800;color:#C9A84C;letter-spacing:0.04em;min-width:1.6em;line-height:1;">O</span>
        <div>
          <span style="font-size:0.78em;font-weight:700;color:#e8dfc8;letter-spacing:0.08em;text-transform:uppercase;">Observe</span>
          <span style="font-size:0.78em;color:#7a8ba0;margin-left:0.6em;">Watch for hesitation, retreat, and evaluation signals.</span>
        </div>
      </div>
      <div style="display:flex;align-items:baseline;padding:0.75em 1.4em;border-bottom:1px solid rgba(255,255,255,0.04);">
        <span style="font-size:1.35em;font-weight:800;color:#C9A84C;letter-spacing:0.04em;min-width:1.6em;line-height:1;">D</span>
        <div>
          <span style="font-size:0.78em;font-weight:700;color:#e8dfc8;letter-spacing:0.08em;text-transform:uppercase;">Decode</span>
          <span style="font-size:0.78em;color:#7a8ba0;margin-left:0.6em;">Identify the real response beneath the surface behavior.</span>
        </div>
      </div>
      <div style="display:flex;align-items:baseline;padding:0.75em 1.4em;background:rgba(255,255,255,0.015);">
        <span style="font-size:1.35em;font-weight:800;color:#C9A84C;letter-spacing:0.04em;min-width:1.6em;line-height:1;">E</span>
        <div>
          <span style="font-size:0.78em;font-weight:700;color:#e8dfc8;letter-spacing:0.08em;text-transform:uppercase;">Elevate</span>
          <span style="font-size:0.78em;color:#7a8ba0;margin-left:0.6em;">Guide the experience to its natural conclusion.</span>
        </div>
      </div>
    </div>
  </div>
</div>
'''


# ── Ch10: Performance Read Panel visuals ─────────────────────────────────────

# Five Things Panel — 3+2 SVG layout for readable card widths
FIVE_THINGS_PANEL_HTML = '''
<div style="margin:2em 0 2.5em;page-break-inside:avoid;">
<svg viewBox="0 0 900 610" xmlns="http://www.w3.org/2000/svg" style="width:100%;display:block;border-radius:4px;overflow:hidden;">
  <rect width="900" height="610" fill="#0d1117"/>
  <rect x="0" y="0" width="900" height="48" fill="#0a0e14"/>
  <line x1="0" y1="48" x2="900" y2="48" stroke="#C9A84C" stroke-width="0.5" opacity="0.4"/>
  <text x="450" y="20" text-anchor="middle" fill="white" font-size="17" font-family="Georgia,serif" letter-spacing="5" font-weight="bold">THE FIVE THINGS YOU'RE ALWAYS READING</text>
  <text x="450" y="39" text-anchor="middle" fill="#C9A84C" font-size="13" font-family="Georgia,serif" font-style="italic">Every signal maps to one of these five questions. Answer them and you know the room.</text>

  <!-- ROW 1: Cards 1, 2, 3 — width 282 each -->

  <!-- Card 1 -->
  <rect x="10" y="60" width="282" height="248" rx="3" fill="#131920" stroke="#1c2535" stroke-width="1"/>
  <rect x="10" y="60" width="282" height="5" rx="3" fill="#C9A84C"/>
  <text x="40" y="96" fill="#C9A84C" font-size="42" font-family="Georgia,serif" font-weight="bold" opacity="0.18">1</text>
  <text x="151" y="98" text-anchor="middle" fill="#C9A84C" font-size="14" font-family="Georgia,serif" letter-spacing="2" font-weight="bold">DID IT LAND?</text>
  <line x1="26" y1="110" x2="276" y2="110" stroke="#1c2535" stroke-width="0.7"/>
  <text x="151" y="130" text-anchor="middle" fill="#7a8ba8" font-size="13" font-family="Georgia,serif">Are they still with you, or did</text>
  <text x="151" y="148" text-anchor="middle" fill="#7a8ba8" font-size="13" font-family="Georgia,serif">the last moment miss its mark?</text>
  <line x1="26" y1="163" x2="276" y2="163" stroke="#1c2535" stroke-width="0.7"/>
  <text x="151" y="181" text-anchor="middle" fill="#4a5e7a" font-size="11" font-family="Georgia,serif" letter-spacing="1.5">LOOK FOR</text>
  <text x="151" y="200" text-anchor="middle" fill="#c0cce0" font-size="13" font-family="Georgia,serif">Eye contact shift</text>
  <text x="151" y="218" text-anchor="middle" fill="#c0cce0" font-size="13" font-family="Georgia,serif">Blink rate change</text>
  <text x="151" y="236" text-anchor="middle" fill="#c0cce0" font-size="13" font-family="Georgia,serif">Postural lean</text>
  <text x="151" y="254" text-anchor="middle" fill="#c0cce0" font-size="13" font-family="Georgia,serif">Breath pattern</text>

  <!-- Card 2 -->
  <rect x="308" y="60" width="282" height="248" rx="3" fill="#131920" stroke="#1c2535" stroke-width="1"/>
  <rect x="308" y="60" width="282" height="5" rx="3" fill="#1A8FA8"/>
  <text x="338" y="96" fill="#1A8FA8" font-size="42" font-family="Georgia,serif" font-weight="bold" opacity="0.18">2</text>
  <text x="449" y="98" text-anchor="middle" fill="#1A8FA8" font-size="14" font-family="Georgia,serif" letter-spacing="2" font-weight="bold">CAN THEY BE LED?</text>
  <line x1="324" y1="110" x2="574" y2="110" stroke="#1c2535" stroke-width="0.7"/>
  <text x="449" y="130" text-anchor="middle" fill="#7a8ba8" font-size="13" font-family="Georgia,serif">Are they following your pace,</text>
  <text x="449" y="148" text-anchor="middle" fill="#7a8ba8" font-size="13" font-family="Georgia,serif">or running their own script?</text>
  <line x1="324" y1="163" x2="574" y2="163" stroke="#1c2535" stroke-width="0.7"/>
  <text x="449" y="181" text-anchor="middle" fill="#4a5e7a" font-size="11" font-family="Georgia,serif" letter-spacing="1.5">LOOK FOR</text>
  <text x="449" y="200" text-anchor="middle" fill="#c0cce0" font-size="13" font-family="Georgia,serif">Mirroring your pace</text>
  <text x="449" y="218" text-anchor="middle" fill="#c0cce0" font-size="13" font-family="Georgia,serif">Head nodding</text>
  <text x="449" y="236" text-anchor="middle" fill="#c0cce0" font-size="13" font-family="Georgia,serif">Open body toward you</text>
  <text x="449" y="254" text-anchor="middle" fill="#c0cce0" font-size="13" font-family="Georgia,serif">Silence as compliance</text>

  <!-- Card 3 -->
  <rect x="606" y="60" width="284" height="248" rx="3" fill="#131920" stroke="#1c2535" stroke-width="1"/>
  <rect x="606" y="60" width="284" height="5" rx="3" fill="#A83030"/>
  <text x="636" y="96" fill="#A83030" font-size="42" font-family="Georgia,serif" font-weight="bold" opacity="0.18">3</text>
  <text x="748" y="98" text-anchor="middle" fill="#A83030" font-size="14" font-family="Georgia,serif" letter-spacing="2" font-weight="bold">PUSHING BACK?</text>
  <line x1="622" y1="110" x2="874" y2="110" stroke="#1c2535" stroke-width="0.7"/>
  <text x="748" y="130" text-anchor="middle" fill="#7a8ba8" font-size="13" font-family="Georgia,serif">Is there resistance — visible</text>
  <text x="748" y="148" text-anchor="middle" fill="#7a8ba8" font-size="13" font-family="Georgia,serif">or just below the surface?</text>
  <line x1="622" y1="163" x2="874" y2="163" stroke="#1c2535" stroke-width="0.7"/>
  <text x="748" y="181" text-anchor="middle" fill="#4a5e7a" font-size="11" font-family="Georgia,serif" letter-spacing="1.5">LOOK FOR</text>
  <text x="748" y="200" text-anchor="middle" fill="#c0cce0" font-size="13" font-family="Georgia,serif">Lean back + arms cross</text>
  <text x="748" y="218" text-anchor="middle" fill="#c0cce0" font-size="13" font-family="Georgia,serif">Smirk at wrong moment</text>
  <text x="748" y="236" text-anchor="middle" fill="#c0cce0" font-size="13" font-family="Georgia,serif">Breaking eye contact</text>
  <text x="748" y="254" text-anchor="middle" fill="#c0cce0" font-size="13" font-family="Georgia,serif">Whisper to neighbor</text>

  <!-- ROW 2: Cards 4, 5 — width 435 each -->

  <!-- Card 4 -->
  <rect x="10" y="320" width="435" height="270" rx="3" fill="#131920" stroke="#1c2535" stroke-width="1"/>
  <rect x="10" y="320" width="435" height="5" rx="3" fill="#6B52A0"/>
  <text x="42" y="360" fill="#6B52A0" font-size="52" font-family="Georgia,serif" font-weight="bold" opacity="0.15">4</text>
  <text x="228" y="356" text-anchor="middle" fill="#6B52A0" font-size="15" font-family="Georgia,serif" letter-spacing="2" font-weight="bold">ARE THEY COMFORTABLE?</text>
  <line x1="26" y1="370" x2="429" y2="370" stroke="#1c2535" stroke-width="0.7"/>
  <text x="228" y="393" text-anchor="middle" fill="#7a8ba8" font-size="13.5" font-family="Georgia,serif">Is this person safe enough to go deeper, or do they need space?</text>
  <line x1="26" y1="410" x2="429" y2="410" stroke="#1c2535" stroke-width="0.7"/>
  <text x="228" y="430" text-anchor="middle" fill="#4a5e7a" font-size="11" font-family="Georgia,serif" letter-spacing="1.5">LOOK FOR</text>
  <text x="228" y="452" text-anchor="middle" fill="#c0cce0" font-size="13.5" font-family="Georgia,serif">Relaxed hands and face · Breathing depth normal</text>
  <text x="228" y="474" text-anchor="middle" fill="#c0cce0" font-size="13.5" font-family="Georgia,serif">Comfortable conversational distance · Unprompted smiling</text>

  <!-- Card 5 -->
  <rect x="455" y="320" width="435" height="270" rx="3" fill="#131920" stroke="#C9A84C" stroke-width="1" opacity="0.8"/>
  <rect x="455" y="320" width="435" height="5" rx="3" fill="#C9A84C"/>
  <text x="487" y="360" fill="#C9A84C" font-size="52" font-family="Georgia,serif" font-weight="bold" opacity="0.15">5</text>
  <text x="672" y="356" text-anchor="middle" fill="#C9A84C" font-size="15" font-family="Georgia,serif" letter-spacing="2" font-weight="bold">IS THE ROOM HOLDING?</text>
  <line x1="471" y1="370" x2="874" y2="370" stroke="#1c2535" stroke-width="0.7"/>
  <text x="672" y="393" text-anchor="middle" fill="#7a8ba8" font-size="13.5" font-family="Georgia,serif">Is the collective energy building, or beginning to fracture?</text>
  <line x1="471" y1="410" x2="874" y2="410" stroke="#1c2535" stroke-width="0.7"/>
  <text x="672" y="430" text-anchor="middle" fill="#4a5e7a" font-size="11" font-family="Georgia,serif" letter-spacing="1.5">LOOK FOR</text>
  <text x="672" y="452" text-anchor="middle" fill="#c0cce0" font-size="13.5" font-family="Georgia,serif">Room-wide stillness · Collective blink slowing</text>
  <text x="672" y="474" text-anchor="middle" fill="#c0cce0" font-size="13.5" font-family="Georgia,serif">Nobody reaching for phone · Shared forward lean</text>
  <rect x="582" y="532" width="180" height="22" rx="11" fill="rgba(201,168,76,0.15)" stroke="#C9A84C" stroke-width="0.7"/>
  <text x="672" y="547" text-anchor="middle" fill="#C9A84C" font-size="11" font-family="Georgia,serif" letter-spacing="1.5">THE MASTER READ</text>
</svg>
</div>
'''


# Tell Table — HTML/CSS for readable text at any screen width
SIGNAL_TABLE_HTML = '''
<div style="margin:2em 0 2.5em;page-break-inside:avoid;background:#0d1117;border-radius:6px;overflow:hidden;border:1px solid rgba(255,255,255,0.07);">
  <div style="background:#0a0e14;padding:1em 1.5em 0.8em;text-align:center;border-bottom:1px solid rgba(201,168,76,0.3);">
    <div style="font-size:0.7em;letter-spacing:0.3em;color:white;font-weight:bold;text-transform:uppercase;margin-bottom:0.3em;">Chris Michael's Tell Table</div>
    <div style="font-size:0.8em;color:#C9A84C;font-style:italic;">Three colors. One decision per row. Signal / What You See / What It Means / What To Do.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:#0f1520;border-bottom:1px solid #1c2535;">
    <div style="padding:0.5em 1em;font-size:0.65em;letter-spacing:0.15em;color:#4a5e7a;text-transform:uppercase;">Signal</div>
    <div style="padding:0.5em 0.8em;font-size:0.65em;letter-spacing:0.15em;color:#4a5e7a;text-transform:uppercase;border-left:1px solid #1c2535;">What You See</div>
    <div style="padding:0.5em 0.8em;font-size:0.65em;letter-spacing:0.15em;color:#4a5e7a;text-transform:uppercase;border-left:1px solid #1c2535;">What It Means</div>
    <div style="padding:0.5em 0.8em;font-size:0.65em;letter-spacing:0.15em;color:#4a5e7a;text-transform:uppercase;border-left:1px solid #1c2535;">What To Do</div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;background:rgba(34,168,85,0.12);border-left:4px solid #22a855;border-bottom:1px solid rgba(34,168,85,0.2);padding:0.45em 1em;">
    <div style="font-size:0.7em;letter-spacing:0.15em;color:#22a855;font-weight:bold;">GREEN — ENGAGED</div>
    <div style="font-size:0.72em;color:rgba(34,168,85,0.65);font-style:italic;text-align:right;padding-right:0.5em;">Stay the course. Go deeper. This is working.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:rgba(34,168,85,0.04);border-bottom:1px solid #161e16;border-left:2px solid rgba(34,168,85,0.35);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Forward lean</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Body tilted toward you; weight on front of chair</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Invested. Emotionally present.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#22a855;border-left:1px solid #1c2535;">Increase specificity</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid #161e16;border-left:2px solid rgba(34,168,85,0.35);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Slow blink rate</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Long intervals between blinks; relaxed eyelids</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Attention locked. Prediction system active.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#22a855;border-left:1px solid #1c2535;">Hold pace. Don't break.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:rgba(34,168,85,0.04);border-bottom:1px solid #161e16;border-left:2px solid rgba(34,168,85,0.35);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Room-wide stillness</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Movement stops; nobody shifting or reaching</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Full cortisol window. Collective hold.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#22a855;border-left:1px solid #1c2535;">Extend the build</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid #161e16;border-left:2px solid rgba(34,168,85,0.35);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Sustained eye contact</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Holding gaze without looking away</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Trust. Open to suggestion.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#22a855;border-left:1px solid #1c2535;">Hold contact. Slow down.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:rgba(34,168,85,0.04);border-bottom:1px solid #161e16;border-left:2px solid rgba(34,168,85,0.35);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Head nod (slow)</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Deliberate nods during your delivery</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Processing and agreeing simultaneously.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#22a855;border-left:1px solid #1c2535;">Name what they feel</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid #161e16;border-left:2px solid rgba(34,168,85,0.35);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Open posture</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Arms relaxed, hands visible, chest open</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">No defensive blocking. Receptive state.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#22a855;border-left:1px solid #1c2535;">Move into their space</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:rgba(34,168,85,0.04);border-bottom:1px solid #161e16;border-left:2px solid rgba(34,168,85,0.35);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Arms uncrossed (shift)</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Arms drop from crossed to open</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Resistance just dropped. Window opened.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#22a855;border-left:1px solid #1c2535;">Immediate ask or reveal</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid #161e16;border-left:2px solid rgba(34,168,85,0.35);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Spontaneous smile</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Genuine smile reaching eyes (Duchenne)</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Dopamine active. Wants more.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#22a855;border-left:1px solid #1c2535;">Reward immediately</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:rgba(34,168,85,0.04);border-bottom:1px solid #161e16;border-left:2px solid rgba(34,168,85,0.35);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Mirroring your pace</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">They match your speed and rhythm unconsciously</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Deep rapport. Following your lead.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#22a855;border-left:1px solid #1c2535;">Lead the change you want</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid rgba(34,168,85,0.25);border-left:2px solid rgba(34,168,85,0.35);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Held breath (visible)</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Chest stops moving; breath suspended</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Peak anticipation. Reveal window is now.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#22a855;border-left:1px solid #1c2535;">Deliver. Don't extend.</div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;background:rgba(201,168,76,0.12);border-left:4px solid #C9A84C;border-bottom:1px solid rgba(201,168,76,0.2);border-top:1px solid rgba(201,168,76,0.15);padding:0.45em 1em;">
    <div style="font-size:0.7em;letter-spacing:0.15em;color:#C9A84C;font-weight:bold;">YELLOW — UNCERTAIN</div>
    <div style="font-size:0.72em;color:rgba(201,168,76,0.65);font-style:italic;text-align:right;padding-right:0.5em;">Adjust. Check in. Don't push yet.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:rgba(201,168,76,0.04);border-bottom:1px solid #1e1c12;border-left:2px solid rgba(201,168,76,0.4);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Looking around</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Eyes scanning the room instead of staying on you</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Checking for social permission.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#C9A84C;border-left:1px solid #1c2535;">Reestablish with room</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid #1e1c12;border-left:2px solid rgba(201,168,76,0.4);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Face touch</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Hand moves to mouth, nose, or cheek mid-thought</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Cognitive load spiking. Self-soothing.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#C9A84C;border-left:1px solid #1c2535;">Simplify. Reduce complexity.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:rgba(201,168,76,0.04);border-bottom:1px solid #1e1c12;border-left:2px solid rgba(201,168,76,0.4);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Neutral expression</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Face flat; no visible affect</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Evaluating. Verdict not in yet.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#C9A84C;border-left:1px solid #1c2535;">Deliver proof. Don't explain.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid #1e1c12;border-left:2px solid rgba(201,168,76,0.4);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Arms starting to cross</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Folding across body, not yet fully closed</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Early defensive signal. Not yet closed off.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#C9A84C;border-left:1px solid #1c2535;">Reduce pressure. Add warmth.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:rgba(201,168,76,0.04);border-bottom:1px solid #1e1c12;border-left:2px solid rgba(201,168,76,0.4);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Hesitation before reply</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Delay between prompt and response</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Processing or calculating. Uncertain.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#C9A84C;border-left:1px solid #1c2535;">Wait. Give them space.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid #1e1c12;border-left:2px solid rgba(201,168,76,0.4);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Eyebrow micro-raise</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Quick flash of brow lift, gone in under a second</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Surprise or disbelief. Not fully sold yet.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#C9A84C;border-left:1px solid #1c2535;">Restate and anchor</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:rgba(201,168,76,0.04);border-bottom:1px solid #1e1c12;border-left:2px solid rgba(201,168,76,0.4);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Evaluative squint</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Eyes narrow slightly; concentrating hard</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Scrutinizing. Wants more evidence.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#C9A84C;border-left:1px solid #1c2535;">Give a T1 proof point</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid #1e1c12;border-left:2px solid rgba(201,168,76,0.4);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Reduced eye contact</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Brief breaks increasing; gaze wandering</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Starting to disengage. Attention drifting.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#C9A84C;border-left:1px solid #1c2535;">Re-engage with name or question</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid rgba(201,168,76,0.2);border-left:2px solid rgba(201,168,76,0.4);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Brow furrow</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Vertical lines between brows; effortful thinking</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Confusion or dissonance. Lost the thread.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#C9A84C;border-left:1px solid #1c2535;">Recap. Back up one step.</div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;background:rgba(168,48,48,0.15);border-left:4px solid #A83030;border-bottom:1px solid rgba(168,48,48,0.2);border-top:1px solid rgba(168,48,48,0.15);padding:0.45em 1em;">
    <div style="font-size:0.7em;letter-spacing:0.15em;color:#A83030;font-weight:bold;">RED — DISENGAGED / RESISTANT</div>
    <div style="font-size:0.72em;color:rgba(168,48,48,0.65);font-style:italic;text-align:right;padding-right:0.5em;">Pivot now. Don't push through.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:rgba(168,48,48,0.05);border-bottom:1px solid #1e1212;border-left:2px solid rgba(168,48,48,0.45);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Lean back + arms cross</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Full body retreat; closed, symmetric posture</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Closed off. Disengaged or resistant.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#A83030;border-left:1px solid #1c2535;">Reframe. Lower the stakes.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid #1e1212;border-left:2px solid rgba(168,48,48,0.45);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Phone check</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Hand reaches for phone or screen glanced at</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Fully broken. Nothing competes anymore.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#A83030;border-left:1px solid #1c2535;">Call it out or skip them</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:rgba(168,48,48,0.05);border-bottom:1px solid #1e1212;border-left:2px solid rgba(168,48,48,0.45);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Laugh at wrong moment</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Nervous or contemptuous laugh; nothing was funny</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Cortisol discharge. Tension broke wrong way.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#A83030;border-left:1px solid #1c2535;">Reset. Drop the bit entirely.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid #1e1212;border-left:2px solid rgba(168,48,48,0.45);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Fidgeting / leg-recross</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Repetitive movement; crossing and uncrossing</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Anxious or impatient. Needs release.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#A83030;border-left:1px solid #1c2535;">Shorter format. Move on.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:rgba(168,48,48,0.05);border-bottom:1px solid #1e1212;border-left:2px solid rgba(168,48,48,0.45);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Whisper to neighbor</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Leaning and murmuring to person beside them</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">You've lost them to each other.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#A83030;border-left:1px solid #1c2535;">Bring them in or move past them</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid #1e1212;border-left:2px solid rgba(168,48,48,0.45);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Evaluative smirk</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Asymmetric half-smile; contemptuous micro-expression</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Disbelief with a power stance. Challenge.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#A83030;border-left:1px solid #1c2535;">Acknowledge, don't compete</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:rgba(168,48,48,0.05);border-bottom:1px solid #1e1212;border-left:2px solid rgba(168,48,48,0.45);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Sharp blink increase</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Blink rate jumps; rapid repeated blinking</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Mental reset. Lost focus. Stress spike.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#A83030;border-left:1px solid #1c2535;">Pattern interrupt. Change state.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid #1e1212;border-left:2px solid rgba(168,48,48,0.45);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Feet toward exit</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Lower body oriented away or toward door</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Mind already leaving. Most honest signal.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#A83030;border-left:1px solid #1c2535;">Close fast or release</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-left:2px solid rgba(168,48,48,0.45);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Full shift back in chair</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Maximum posterior shift; distance sought</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Creating space. Wants separation.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#A83030;border-left:1px solid #1c2535;">Don't follow in. Give space.</div>
  </div>
  <div style="background:#080e14;padding:0.8em 1.5em;text-align:center;border-top:1px solid rgba(201,168,76,0.2);">
    <div style="font-size:0.75em;letter-spacing:0.12em;color:#C9A84C;margin-bottom:0.25em;">THE THREE-SIGNAL RULE</div>
    <div style="font-size:0.8em;color:#4a5e7a;">One signal is noise. Two is a pattern forming. Three signals in the same color is a read. Act on it.</div>
  </div>
</div>
'''


MINI_SCENARIOS_HTML = '''
<div style="margin:2em 0 2.5em;page-break-inside:avoid;background:#0d1117;border-radius:6px;overflow:hidden;border:1px solid rgba(255,255,255,0.07);">
  <!-- Header -->
  <div style="background:#0a0e14;padding:0.9em 1.5em 0.75em;text-align:center;border-bottom:1px solid #1c2535;">
    <div style="font-size:0.7em;letter-spacing:0.3em;color:white;font-weight:bold;text-transform:uppercase;margin-bottom:0.25em;">In-Performance Reads</div>
    <div style="font-size:0.8em;color:#4a5e7a;font-style:italic;">Observation cluster &#8594; Decision</div>
  </div>
  <!-- Two cards -->
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:0;">
    <!-- GREEN card -->
    <div style="background:#0a1410;border-right:1px solid rgba(255,255,255,0.06);border-top:3px solid #22a855;">
      <div style="padding:1.2em 1.4em 0.8em;border-bottom:1px solid rgba(34,168,85,0.12);">
        <div style="display:flex;align-items:center;gap:0.7em;margin-bottom:0.9em;">
          <span style="font-size:0.68em;letter-spacing:0.12em;color:#22a855;background:rgba(34,168,85,0.12);border:1px solid rgba(34,168,85,0.3);padding:0.2em 0.7em;border-radius:9px;">GREEN</span>
          <span style="font-size:0.9em;color:#c0cce0;font-weight:bold;">You See:</span>
        </div>
        <p style="font-size:0.9em;color:#7a9a88;line-height:1.65;margin:0;">Volunteer leans forward. Body still. Blink rate slowed. Hands open in lap. Eyes holding yours.</p>
      </div>
      <div style="padding:1em 1.4em 0.8em;border-bottom:1px solid rgba(34,168,85,0.12);">
        <div style="font-size:0.8em;color:#c0cce0;font-weight:bold;margin-bottom:0.5em;">What It Means:</div>
        <p style="font-size:0.9em;color:#7a9a88;line-height:1.65;margin:0;">Three green signals in a cluster. They are fully inside the experience. Resistance is gone.</p>
      </div>
      <div style="padding:1em 1.4em 1.4em;">
        <div style="font-size:0.8em;color:#c0cce0;font-weight:bold;margin-bottom:0.7em;">What To Do:</div>
        <div style="background:rgba(34,168,85,0.08);border:1px solid rgba(34,168,85,0.2);border-radius:4px;padding:1em 1.2em;text-align:center;">
          <div style="font-size:1.35em;color:#22a855;font-style:italic;font-family:Georgia,serif;margin-bottom:0.3em;">Stay. Go deeper.</div>
          <div style="font-size:0.78em;color:rgba(34,168,85,0.5);">This is your window. Don&#x27;t break it with explanation.</div>
        </div>
      </div>
    </div>
    <!-- RED card -->
    <div style="background:#140a0a;border-top:3px solid #A83030;">
      <div style="padding:1.2em 1.4em 0.8em;border-bottom:1px solid rgba(168,48,48,0.12);">
        <div style="display:flex;align-items:center;gap:0.7em;margin-bottom:0.9em;">
          <span style="font-size:0.68em;letter-spacing:0.12em;color:#A83030;background:rgba(168,48,48,0.12);border:1px solid rgba(168,48,48,0.3);padding:0.2em 0.7em;border-radius:9px;">RED</span>
          <span style="font-size:0.9em;color:#c0cce0;font-weight:bold;">You See:</span>
        </div>
        <p style="font-size:0.9em;color:#9a7a7a;line-height:1.65;margin:0;">Volunteer squints. Shifts back in chair. Touches face. Blink rate increasing. Eyes leave yours.</p>
      </div>
      <div style="padding:1em 1.4em 0.8em;border-bottom:1px solid rgba(168,48,48,0.12);">
        <div style="font-size:0.8em;color:#c0cce0;font-weight:bold;margin-bottom:0.5em;">What It Means:</div>
        <p style="font-size:0.9em;color:#9a7a7a;line-height:1.65;margin:0;">Three signals: discomfort, scrutiny, self-soothing. The last move missed. They are managing anxiety.</p>
      </div>
      <div style="padding:1em 1.4em 1.4em;">
        <div style="font-size:0.8em;color:#c0cce0;font-weight:bold;margin-bottom:0.7em;">What To Do:</div>
        <div style="background:rgba(168,48,48,0.08);border:1px solid rgba(168,48,48,0.2);border-radius:4px;padding:1em 1.2em;text-align:center;">
          <div style="font-size:1.35em;color:#A83030;font-style:italic;font-family:Georgia,serif;margin-bottom:0.3em;">You missed. Pivot.</div>
          <div style="font-size:0.78em;color:rgba(168,48,48,0.5);">Acknowledge, redirect, or drop the bit entirely.</div>
        </div>
      </div>
    </div>
  </div>
</div>
'''


# Cheat Sheet — HTML/CSS grid for readable text
CHEAT_SHEET_HTML = '''
<div style="margin:2em 0 2.5em;page-break-inside:avoid;background:#0d1117;border-radius:6px;overflow:hidden;border:1px solid rgba(255,255,255,0.07);">
  <div style="background:#0a0e14;padding:1em 1.5em 0.8em;text-align:center;border-bottom:1px solid rgba(201,168,76,0.3);">
    <div style="font-size:0.7em;letter-spacing:0.3em;color:white;font-weight:bold;text-transform:uppercase;margin-bottom:0.3em;">Quick-Reference Cheat Sheet</div>
    <div style="font-size:0.8em;color:#C9A84C;font-style:italic;">If you remember nothing else, remember these. One cluster from any column is a read.</div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;">
    <div style="border-right:1px solid rgba(255,255,255,0.06);">
      <div style="background:rgba(34,168,85,0.12);border-left:4px solid #22a855;padding:0.75em 1.2em;border-bottom:1px solid rgba(34,168,85,0.2);">
        <div style="font-size:0.75em;letter-spacing:0.2em;color:#22a855;font-weight:bold;margin-bottom:0.15em;">TOP 10 GREEN</div>
        <div style="font-size:0.75em;color:rgba(34,168,85,0.6);font-style:italic;">Stay. Deepen. Deliver.</div>
      </div>
      <div style="padding:0 0 0.5em;">
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(34,168,85,0.07);"><span style="font-size:0.72em;color:rgba(34,168,85,0.45);padding-top:0.1em;">01</span><span style="font-size:0.87em;color:#c0cce0;">Forward lean</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(34,168,85,0.07);background:rgba(34,168,85,0.03);"><span style="font-size:0.72em;color:rgba(34,168,85,0.45);padding-top:0.1em;">02</span><span style="font-size:0.87em;color:#c0cce0;">Slow blink rate</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(34,168,85,0.07);"><span style="font-size:0.72em;color:rgba(34,168,85,0.45);padding-top:0.1em;">03</span><span style="font-size:0.87em;color:#c0cce0;">Room-wide stillness</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(34,168,85,0.07);background:rgba(34,168,85,0.03);"><span style="font-size:0.72em;color:rgba(34,168,85,0.45);padding-top:0.1em;">04</span><span style="font-size:0.87em;color:#c0cce0;">Sustained eye contact</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(34,168,85,0.07);"><span style="font-size:0.72em;color:rgba(34,168,85,0.45);padding-top:0.1em;">05</span><span style="font-size:0.87em;color:#c0cce0;">Slow head nod</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(34,168,85,0.07);background:rgba(34,168,85,0.03);"><span style="font-size:0.72em;color:rgba(34,168,85,0.45);padding-top:0.1em;">06</span><span style="font-size:0.87em;color:#c0cce0;">Open posture</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(34,168,85,0.07);"><span style="font-size:0.72em;color:rgba(34,168,85,0.45);padding-top:0.1em;">07</span><span style="font-size:0.87em;color:#c0cce0;">Arms uncrossing (shift)</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(34,168,85,0.07);background:rgba(34,168,85,0.03);"><span style="font-size:0.72em;color:rgba(34,168,85,0.45);padding-top:0.1em;">08</span><span style="font-size:0.87em;color:#c0cce0;">Spontaneous smile</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(34,168,85,0.07);"><span style="font-size:0.72em;color:rgba(34,168,85,0.45);padding-top:0.1em;">09</span><span style="font-size:0.87em;color:#c0cce0;">Mirroring your pace</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;background:rgba(34,168,85,0.03);"><span style="font-size:0.72em;color:rgba(34,168,85,0.45);padding-top:0.1em;">10</span><span style="font-size:0.87em;color:#c0cce0;">Held breath</span></div>
      </div>
      <div style="margin:0 1em 1em;padding:0.6em 1em;background:rgba(34,168,85,0.07);border-radius:3px;border:1px solid rgba(34,168,85,0.15);">
        <div style="font-size:0.82em;color:#22a855;font-style:italic;margin-bottom:0.2em;">Three of these = your window is open.</div>
        <div style="font-size:0.78em;color:rgba(34,168,85,0.5);">Act. Don't wait for four.</div>
      </div>
    </div>
    <div style="border-right:1px solid rgba(255,255,255,0.06);">
      <div style="background:rgba(201,168,76,0.1);border-left:4px solid #C9A84C;padding:0.75em 1.2em;border-bottom:1px solid rgba(201,168,76,0.2);">
        <div style="font-size:0.75em;letter-spacing:0.2em;color:#C9A84C;font-weight:bold;margin-bottom:0.15em;">TOP 10 YELLOW</div>
        <div style="font-size:0.75em;color:rgba(201,168,76,0.6);font-style:italic;">Adjust. Check. Don't escalate.</div>
      </div>
      <div style="padding:0 0 0.5em;">
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(201,168,76,0.07);"><span style="font-size:0.72em;color:rgba(201,168,76,0.4);padding-top:0.1em;">01</span><span style="font-size:0.87em;color:#c0cce0;">Looking around</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(201,168,76,0.07);background:rgba(201,168,76,0.03);"><span style="font-size:0.72em;color:rgba(201,168,76,0.4);padding-top:0.1em;">02</span><span style="font-size:0.87em;color:#c0cce0;">Face touch mid-thought</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(201,168,76,0.07);"><span style="font-size:0.72em;color:rgba(201,168,76,0.4);padding-top:0.1em;">03</span><span style="font-size:0.87em;color:#c0cce0;">Neutral expression</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(201,168,76,0.07);background:rgba(201,168,76,0.03);"><span style="font-size:0.72em;color:rgba(201,168,76,0.4);padding-top:0.1em;">04</span><span style="font-size:0.87em;color:#c0cce0;">Arms starting to cross</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(201,168,76,0.07);"><span style="font-size:0.72em;color:rgba(201,168,76,0.4);padding-top:0.1em;">05</span><span style="font-size:0.87em;color:#c0cce0;">Hesitation before reply</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(201,168,76,0.07);background:rgba(201,168,76,0.03);"><span style="font-size:0.72em;color:rgba(201,168,76,0.4);padding-top:0.1em;">06</span><span style="font-size:0.87em;color:#c0cce0;">Eyebrow micro-raise</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(201,168,76,0.07);"><span style="font-size:0.72em;color:rgba(201,168,76,0.4);padding-top:0.1em;">07</span><span style="font-size:0.87em;color:#c0cce0;">Evaluative squint</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(201,168,76,0.07);background:rgba(201,168,76,0.03);"><span style="font-size:0.72em;color:rgba(201,168,76,0.4);padding-top:0.1em;">08</span><span style="font-size:0.87em;color:#c0cce0;">Reduced eye contact</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(201,168,76,0.07);"><span style="font-size:0.72em;color:rgba(201,168,76,0.4);padding-top:0.1em;">09</span><span style="font-size:0.87em;color:#c0cce0;">Brow furrow</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;background:rgba(201,168,76,0.03);"><span style="font-size:0.72em;color:rgba(201,168,76,0.4);padding-top:0.1em;">10</span><span style="font-size:0.87em;color:#c0cce0;">Posture shift mid-point</span></div>
      </div>
      <div style="margin:0 1em 1em;padding:0.6em 1em;background:rgba(201,168,76,0.07);border-radius:3px;border:1px solid rgba(201,168,76,0.15);">
        <div style="font-size:0.82em;color:#C9A84C;font-style:italic;margin-bottom:0.2em;">Two yellows = slow down and check.</div>
        <div style="font-size:0.78em;color:rgba(201,168,76,0.5);">Three = you lost them. Adjust now.</div>
      </div>
    </div>
    <div>
      <div style="background:rgba(168,48,48,0.12);border-left:4px solid #A83030;padding:0.75em 1.2em;border-bottom:1px solid rgba(168,48,48,0.2);">
        <div style="font-size:0.75em;letter-spacing:0.2em;color:#A83030;font-weight:bold;margin-bottom:0.15em;">TOP 10 RED</div>
        <div style="font-size:0.75em;color:rgba(168,48,48,0.6);font-style:italic;">Pivot. Pivot. Pivot.</div>
      </div>
      <div style="padding:0 0 0.5em;">
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(168,48,48,0.07);"><span style="font-size:0.72em;color:rgba(168,48,48,0.4);padding-top:0.1em;">01</span><span style="font-size:0.87em;color:#c0cce0;">Lean back + arms cross</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(168,48,48,0.07);background:rgba(168,48,48,0.03);"><span style="font-size:0.72em;color:rgba(168,48,48,0.4);padding-top:0.1em;">02</span><span style="font-size:0.87em;color:#c0cce0;">Phone check</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(168,48,48,0.07);"><span style="font-size:0.72em;color:rgba(168,48,48,0.4);padding-top:0.1em;">03</span><span style="font-size:0.87em;color:#c0cce0;">Laugh at wrong moment</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(168,48,48,0.07);background:rgba(168,48,48,0.03);"><span style="font-size:0.72em;color:rgba(168,48,48,0.4);padding-top:0.1em;">04</span><span style="font-size:0.87em;color:#c0cce0;">Fidgeting / leg-recross</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(168,48,48,0.07);"><span style="font-size:0.72em;color:rgba(168,48,48,0.4);padding-top:0.1em;">05</span><span style="font-size:0.87em;color:#c0cce0;">Whisper to neighbor</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(168,48,48,0.07);background:rgba(168,48,48,0.03);"><span style="font-size:0.72em;color:rgba(168,48,48,0.4);padding-top:0.1em;">06</span><span style="font-size:0.87em;color:#c0cce0;">Evaluative smirk</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(168,48,48,0.07);"><span style="font-size:0.72em;color:rgba(168,48,48,0.4);padding-top:0.1em;">07</span><span style="font-size:0.87em;color:#c0cce0;">Sharp blink increase</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(168,48,48,0.07);background:rgba(168,48,48,0.03);"><span style="font-size:0.72em;color:rgba(168,48,48,0.4);padding-top:0.1em;">08</span><span style="font-size:0.87em;color:#c0cce0;">Feet toward exit</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(168,48,48,0.07);"><span style="font-size:0.72em;color:rgba(168,48,48,0.4);padding-top:0.1em;">09</span><span style="font-size:0.87em;color:#c0cce0;">Full shift back in chair</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;background:rgba(168,48,48,0.03);"><span style="font-size:0.72em;color:rgba(168,48,48,0.4);padding-top:0.1em;">10</span><span style="font-size:0.87em;color:#c0cce0;">Eyes leaving performer</span></div>
      </div>
      <div style="margin:0 1em 1em;padding:0.6em 1em;background:rgba(168,48,48,0.07);border-radius:3px;border:1px solid rgba(168,48,48,0.15);">
        <div style="font-size:0.82em;color:#A83030;font-style:italic;margin-bottom:0.2em;">One red = watch. Two = pivot.</div>
        <div style="font-size:0.78em;color:rgba(168,48,48,0.5);">Three = stop the bit. Redirect now.</div>
      </div>
    </div>
  </div>
</div>
'''


# ── Ch33: Credibility Sequence numbered boxes ────────────────────────────────
PERFORMANCE_MATRIX_HTML = '''
<div style="margin:2em 0 2.5em;page-break-inside:avoid;overflow-x:auto;">
  <div style="background:#0d1117;border-radius:6px;border:1px solid rgba(201,168,76,0.25);padding:0;overflow:hidden;">
    <div style="background:rgba(201,168,76,0.12);padding:0.9em 1.4em;border-bottom:1px solid rgba(201,168,76,0.25);">
      <div style="font-size:0.7em;letter-spacing:0.15em;color:#C9A84C;text-transform:uppercase;font-weight:700;">The Performance Decision Matrix</div>
      <div style="font-size:0.78em;color:#8a9ab8;margin-top:0.3em;">Match environment to approach before the lights come up. Every row is a different neurological contract.</div>
    </div>
    <table style="width:100%;border-collapse:collapse;font-size:0.78em;">
      <thead>
        <tr style="border-bottom:1px solid rgba(201,168,76,0.2);">
          <th style="padding:0.7em 1em;text-align:left;color:#C9A84C;font-weight:700;letter-spacing:0.08em;font-size:0.85em;white-space:nowrap;">ENVIRONMENT</th>
          <th style="padding:0.7em 1em;text-align:left;color:#C9A84C;font-weight:700;letter-spacing:0.08em;font-size:0.85em;">DEMONSTRATION TYPE</th>
          <th style="padding:0.7em 1em;text-align:left;color:#C9A84C;font-weight:700;letter-spacing:0.08em;font-size:0.85em;">VOLUNTEER APPROACH</th>
          <th style="padding:0.7em 1em;text-align:left;color:#C9A84C;font-weight:700;letter-spacing:0.08em;font-size:0.85em;">REVEAL STYLE</th>
          <th style="padding:0.7em 1em;text-align:left;color:#C9A84C;font-weight:700;letter-spacing:0.08em;font-size:0.85em;">KEY RULE</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
          <td style="padding:0.8em 1em;color:#e8dfc8;font-weight:700;white-space:nowrap;border-right:1px solid rgba(201,168,76,0.1);">STROLLING</td>
          <td style="padding:0.8em 1em;color:#c8d4e0;">T1 cold reads · Social role · 90-sec behavioral profile</td>
          <td style="padding:0.8em 1em;color:#c8d4e0;">T1 opener on whoever is present. Act on one or two strong signals.</td>
          <td style="padding:0.8em 1em;color:#c8d4e0;">Soft hit + one strong hit</td>
          <td style="padding:0.8em 1em;color:#8a9ab8;font-style:italic;">No pre-selection. Leave at the peak.</td>
        </tr>
        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);background:rgba(255,255,255,0.02);">
          <td style="padding:0.8em 1em;color:#e8dfc8;font-weight:700;white-space:nowrap;border-right:1px solid rgba(201,168,76,0.1);">CLOSE-UP</td>
          <td style="padding:0.8em 1em;color:#c8d4e0;">Hidden interest read · Relationship dynamic · Life pivot</td>
          <td style="padding:0.8em 1em;color:#c8d4e0;">Emotional, Reserved, or Analytical volunteer. Intimacy is the asset.</td>
          <td style="padding:0.8em 1em;color:#c8d4e0;">Full layered read at Level 3–4</td>
          <td style="padding:0.8em 1em;color:#8a9ab8;font-style:italic;">Depth earns trust. Use the full reading lines.</td>
        </tr>
        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
          <td style="padding:0.8em 1em;color:#e8dfc8;font-weight:700;white-space:nowrap;border-right:1px solid rgba(201,168,76,0.1);">PARLOR (8–30)</td>
          <td style="padding:0.8em 1em;color:#c8d4e0;">Curiosity-based reads · Social role · Life pivot</td>
          <td style="padding:0.8em 1em;color:#c8d4e0;">Room is the volunteer. Read everyone simultaneously.</td>
          <td style="padding:0.8em 1em;color:#c8d4e0;">Layered read + callback</td>
          <td style="padding:0.8em 1em;color:#8a9ab8;font-style:italic;">Intimacy creates permission. Work the whole room.</td>
        </tr>
        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);background:rgba(255,255,255,0.02);">
          <td style="padding:0.8em 1em;color:#e8dfc8;font-weight:700;white-space:nowrap;border-right:1px solid rgba(201,168,76,0.1);">CORPORATE KEYNOTE</td>
          <td style="padding:0.8em 1em;color:#c8d4e0;">Behavioral profile · Pre-show reveals · Travel pattern read</td>
          <td style="padding:0.8em 1em;color:#c8d4e0;">Pre-show selection. Win the room leader first.</td>
          <td style="padding:0.8em 1em;color:#c8d4e0;">Strong hit + pre-show reveal</td>
          <td style="padding:0.8em 1em;color:#8a9ab8;font-style:italic;">Authority matters. Win the room leader in effect one.</td>
        </tr>
        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
          <td style="padding:0.8em 1em;color:#e8dfc8;font-weight:700;white-space:nowrap;border-right:1px solid rgba(201,168,76,0.1);">STAGE SHOW</td>
          <td style="padding:0.8em 1em;color:#c8d4e0;">Full layered read · Life reading · Social role reveal</td>
          <td style="padding:0.8em 1em;color:#c8d4e0;">Full matrix selection. Assess confidence and suggestibility independently.</td>
          <td style="padding:0.8em 1em;color:#c8d4e0;">All four levels of the layered read</td>
          <td style="padding:0.8em 1em;color:#8a9ab8;font-style:italic;">Level 4 staging mechanics every time.</td>
        </tr>
        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);background:rgba(255,255,255,0.02);">
          <td style="padding:0.8em 1em;color:#e8dfc8;font-weight:700;white-space:nowrap;border-right:1px solid rgba(201,168,76,0.1);">THEATER</td>
          <td style="padding:0.8em 1em;color:#c8d4e0;">Insight demonstration sequence · Callback close</td>
          <td style="padding:0.8em 1em;color:#c8d4e0;">Supporter or Emotional for peaks. Challenger for prediction.</td>
          <td style="padding:0.8em 1em;color:#c8d4e0;">Layered read + insight demo + callback</td>
          <td style="padding:0.8em 1em;color:#8a9ab8;font-style:italic;">Plant in first effect. Pay off at the close.</td>
        </tr>
        <tr>
          <td style="padding:0.8em 1em;color:#e8dfc8;font-weight:700;white-space:nowrap;border-right:1px solid rgba(201,168,76,0.1);">PRIVATE CONSULT</td>
          <td style="padding:0.8em 1em;color:#c8d4e0;">Complete deep-read · All six insight frameworks</td>
          <td style="padding:0.8em 1em;color:#c8d4e0;">One subject. Full session. No audience management required.</td>
          <td style="padding:0.8em 1em;color:#c8d4e0;">All levels, extended, with full DISC framing</td>
          <td style="padding:0.8em 1em;color:#8a9ab8;font-style:italic;">Only context where explaining your framework serves the work.</td>
        </tr>
      </tbody>
    </table>
    <div style="padding:0.6em 1.4em 0.8em;border-top:1px solid rgba(201,168,76,0.1);">
      <span style="font-size:0.72em;color:#4a5e7a;font-style:italic;">Sit with this grid before every show. Circle the row. That ten-second decision shapes every choice that follows.</span>
    </div>
  </div>
</div>
'''

CREDIBILITY_SEQUENCE_HTML = '''
<div style="margin:1.5em 0 2em;page-break-inside:avoid;">
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;">
    <div style="background:#0d1117;border-radius:6px;border:1px solid rgba(201,168,76,0.25);padding:1.4em 1.2em 1.3em;text-align:center;">
      <div style="font-size:2.2em;font-weight:900;color:#C9A84C;line-height:1;margin-bottom:0.4em;font-family:serif;">1</div>
      <div style="font-size:0.88em;color:#c8d4e0;line-height:1.5;font-weight:600;">Demonstrate before explaining.</div>
    </div>
    <div style="background:#0d1117;border-radius:6px;border:1px solid rgba(201,168,76,0.25);padding:1.4em 1.2em 1.3em;text-align:center;">
      <div style="font-size:2.2em;font-weight:900;color:#C9A84C;line-height:1;margin-bottom:0.4em;font-family:serif;">2</div>
      <div style="font-size:0.88em;color:#c8d4e0;line-height:1.5;font-weight:600;">Name what happened accurately.</div>
    </div>
    <div style="background:#0d1117;border-radius:6px;border:1px solid rgba(201,168,76,0.25);padding:1.4em 1.2em 1.3em;text-align:center;">
      <div style="font-size:2.2em;font-weight:900;color:#C9A84C;line-height:1;margin-bottom:0.4em;font-family:serif;">3</div>
      <div style="font-size:0.88em;color:#c8d4e0;line-height:1.5;font-weight:600;">Invite their framework before offering yours.</div>
    </div>
  </div>
</div>
'''


# ── Ch43/44: Sitcom Constellation table ─────────────────────────────────────
SITCOM_TABLE_HTML = '''
<div style="margin:2em 0 2.5em;page-break-inside:avoid;overflow-x:auto;">
  <div style="background:#0d1117;border-radius:6px;border:1px solid rgba(201,168,76,0.25);padding:0;overflow:hidden;">
    <div style="background:rgba(201,168,76,0.08);padding:0.8em 1.4em;border-bottom:1px solid rgba(201,168,76,0.2);">
      <div style="font-size:0.7em;letter-spacing:0.15em;color:#C9A84C;text-transform:uppercase;font-weight:700;">The Sitcom Constellation — Three Splits, Eight Outcomes</div>
    </div>
    <table style="width:100%;border-collapse:collapse;font-size:0.82em;">
      <thead>
        <tr style="border-bottom:1px solid rgba(201,168,76,0.2);">
          <th style="padding:0.65em 1em;text-align:left;color:#C9A84C;font-weight:700;letter-spacing:0.08em;font-size:0.85em;">SHOW</th>
          <th style="padding:0.65em 1em;text-align:left;color:#C9A84C;font-weight:700;letter-spacing:0.08em;font-size:0.85em;">TEMPERATURE</th>
          <th style="padding:0.65em 1em;text-align:left;color:#C9A84C;font-weight:700;letter-spacing:0.08em;font-size:0.85em;">SOCIAL WORLD</th>
          <th style="padding:0.65em 1em;text-align:left;color:#C9A84C;font-weight:700;letter-spacing:0.08em;font-size:0.85em;">TEXTURE</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
          <td style="padding:0.75em 1em;color:#e8dfc8;font-weight:600;">Cheers</td>
          <td style="padding:0.75em 1em;"><span style="color:#4a9d8f;font-size:0.85em;font-weight:600;">Warm</span></td>
          <td style="padding:0.75em 1em;color:#c8d4e0;">Public</td>
          <td style="padding:0.75em 1em;color:#8a9ab8;font-style:italic;">Classic</td>
        </tr>
        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);background:rgba(255,255,255,0.02);">
          <td style="padding:0.75em 1em;color:#e8dfc8;font-weight:600;">Friends</td>
          <td style="padding:0.75em 1em;"><span style="color:#4a9d8f;font-size:0.85em;font-weight:600;">Warm</span></td>
          <td style="padding:0.75em 1em;color:#c8d4e0;">Public</td>
          <td style="padding:0.75em 1em;color:#c8d4e0;">Modern</td>
        </tr>
        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
          <td style="padding:0.75em 1em;color:#e8dfc8;font-weight:600;">The Golden Girls</td>
          <td style="padding:0.75em 1em;"><span style="color:#4a9d8f;font-size:0.85em;font-weight:600;">Warm</span></td>
          <td style="padding:0.75em 1em;color:#c8d4e0;">Domestic</td>
          <td style="padding:0.75em 1em;color:#8a9ab8;font-style:italic;">Classic</td>
        </tr>
        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);background:rgba(255,255,255,0.02);">
          <td style="padding:0.75em 1em;color:#e8dfc8;font-weight:600;">Modern Family</td>
          <td style="padding:0.75em 1em;"><span style="color:#4a9d8f;font-size:0.85em;font-weight:600;">Warm</span></td>
          <td style="padding:0.75em 1em;color:#c8d4e0;">Domestic</td>
          <td style="padding:0.75em 1em;color:#c8d4e0;">Modern</td>
        </tr>
        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
          <td style="padding:0.75em 1em;color:#e8dfc8;font-weight:600;">Seinfeld</td>
          <td style="padding:0.75em 1em;"><span style="color:#9a5050;font-size:0.85em;font-weight:600;">Sharp</span></td>
          <td style="padding:0.75em 1em;color:#c8d4e0;">Public</td>
          <td style="padding:0.75em 1em;color:#8a9ab8;font-style:italic;">Classic</td>
        </tr>
        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);background:rgba(255,255,255,0.02);">
          <td style="padding:0.75em 1em;color:#e8dfc8;font-weight:600;">The Office</td>
          <td style="padding:0.75em 1em;"><span style="color:#9a5050;font-size:0.85em;font-weight:600;">Sharp</span></td>
          <td style="padding:0.75em 1em;color:#c8d4e0;">Public</td>
          <td style="padding:0.75em 1em;color:#c8d4e0;">Modern</td>
        </tr>
        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
          <td style="padding:0.75em 1em;color:#e8dfc8;font-weight:600;">I Love Lucy</td>
          <td style="padding:0.75em 1em;"><span style="color:#9a5050;font-size:0.85em;font-weight:600;">Sharp</span></td>
          <td style="padding:0.75em 1em;color:#c8d4e0;">Domestic</td>
          <td style="padding:0.75em 1em;color:#8a9ab8;font-style:italic;">Classic</td>
        </tr>
        <tr>
          <td style="padding:0.75em 1em;color:#e8dfc8;font-weight:600;">The Big Bang Theory</td>
          <td style="padding:0.75em 1em;"><span style="color:#9a5050;font-size:0.85em;font-weight:600;">Sharp</span></td>
          <td style="padding:0.75em 1em;color:#c8d4e0;">Domestic</td>
          <td style="padding:0.75em 1em;color:#c8d4e0;">Modern</td>
        </tr>
      </tbody>
    </table>
    <div style="padding:0.6em 1.4em 0.75em;border-top:1px solid rgba(201,168,76,0.1);">
      <span style="font-size:0.72em;color:#4a5e7a;font-style:italic;">Three splits. Eight outcomes. The participant never hears them as categories. They experience them as impressions.</span>
    </div>
  </div>
</div>
'''


# ── Ch18: Diagnostic reference panel (ten questions) ─────────────────────────
CH18_DIAGNOSTIC_PANEL_HTML = '''
<div style="margin:1.8em 0 2.2em;page-break-inside:avoid;">
  <div style="background:#0d1117;border-radius:6px;border:1px solid rgba(201,168,76,0.25);overflow:hidden;">
    <div style="background:rgba(201,168,76,0.07);padding:0.75em 1.4em;border-bottom:1px solid rgba(201,168,76,0.2);display:flex;align-items:center;gap:.7em;">
      <span style="font-size:0.63em;letter-spacing:0.18em;color:#C9A84C;text-transform:uppercase;font-weight:700;">Run against every routine — ten diagnostic questions</span>
    </div>
    <div style="padding:.1em 0 .3em;">
      <div style="display:flex;gap:1em;padding:.7em 1.4em;border-bottom:1px solid rgba(255,255,255,0.04);">
        <span style="font-size:.68em;color:#C9A84C;font-weight:700;flex-shrink:0;padding-top:.1em;min-width:1.6em;">01</span>
        <div><div style="font-size:.84em;font-weight:600;color:#e2e8f0;line-height:1.4;">Does the revelation exceed what the audience saw you receive?</div><div style="font-size:.76em;color:rgba(180,185,210,.65);line-height:1.4;margin-top:.2em;">If no, the line from inputs to output is the method. Find where the output exceeds the input.</div></div>
      </div>
      <div style="display:flex;gap:1em;padding:.7em 1.4em;border-bottom:1px solid rgba(255,255,255,0.04);background:rgba(255,255,255,.015);">
        <span style="font-size:.68em;color:#C9A84C;font-weight:700;flex-shrink:0;padding-top:.1em;min-width:1.6em;">02</span>
        <div><div style="font-size:.84em;font-weight:600;color:#e2e8f0;line-height:1.4;">Does this have a premise the audience can believe in?</div><div style="font-size:.76em;color:rgba(180,185,210,.65);line-height:1.4;margin-top:.2em;">If no, the audience defaults to "trick." Build the home before the method lives in it.</div></div>
      </div>
      <div style="display:flex;gap:1em;padding:.7em 1.4em;border-bottom:1px solid rgba(255,255,255,0.04);">
        <span style="font-size:.68em;color:#C9A84C;font-weight:700;flex-shrink:0;padding-top:.1em;min-width:1.6em;">03</span>
        <div><div style="font-size:.84em;font-weight:600;color:#e2e8f0;line-height:1.4;">Does the participant feel free throughout?</div><div style="font-size:.76em;color:rgba(180,185,210,.65);line-height:1.4;margin-top:.2em;">If no, the audience is watching a procedure. Review every instruction — make it feel like conversation.</div></div>
      </div>
      <div style="display:flex;gap:1em;padding:.7em 1.4em;border-bottom:1px solid rgba(255,255,255,0.04);background:rgba(255,255,255,.015);">
        <span style="font-size:.68em;color:#C9A84C;font-weight:700;flex-shrink:0;padding-top:.1em;min-width:1.6em;">04</span>
        <div><div style="font-size:.84em;font-weight:600;color:#e2e8f0;line-height:1.4;">Does the audience know when certainty arrived?</div><div style="font-size:.76em;color:rgba(180,185,210,.65);line-height:1.4;margin-top:.2em;">If yes, they know where the method is. Bury the acquisition deeper in transition or time.</div></div>
      </div>
      <div style="display:flex;gap:1em;padding:.7em 1.4em;border-bottom:1px solid rgba(255,255,255,0.04);">
        <span style="font-size:.68em;color:#C9A84C;font-weight:700;flex-shrink:0;padding-top:.1em;min-width:1.6em;">05</span>
        <div><div style="font-size:.84em;font-weight:600;color:#e2e8f0;line-height:1.4;">Is the thought meaningful, or only procedural?</div><div style="font-size:.76em;color:rgba(180,185,210,.65);line-height:1.4;margin-top:.2em;">If procedural, the revelation will be correct and forgettable. Push for emotional weight.</div></div>
      </div>
      <div style="display:flex;gap:1em;padding:.7em 1.4em;border-bottom:1px solid rgba(255,255,255,0.04);background:rgba(255,255,255,.015);">
        <span style="font-size:.68em;color:#C9A84C;font-weight:700;flex-shrink:0;padding-top:.1em;min-width:1.6em;">06</span>
        <div><div style="font-size:.84em;font-weight:600;color:#e2e8f0;line-height:1.4;">Can this survive retelling?</div><div style="font-size:.76em;color:rgba(180,185,210,.65);line-height:1.4;margin-top:.2em;">If no, the effect dies in the room. Design for the story the audience tells tomorrow.</div></div>
      </div>
      <div style="display:flex;gap:1em;padding:.7em 1.4em;border-bottom:1px solid rgba(255,255,255,0.04);">
        <span style="font-size:.68em;color:#C9A84C;font-weight:700;flex-shrink:0;padding-top:.1em;min-width:1.6em;">07</span>
        <div><div style="font-size:.84em;font-weight:600;color:#e2e8f0;line-height:1.4;">Does the post-reveal moment strengthen the impossibility?</div><div style="font-size:.76em;color:rgba(180,185,210,.65);line-height:1.4;margin-top:.2em;">If it weakens, you are overproving or reacting to your own hit. Move on before the audience opens it.</div></div>
      </div>
      <div style="display:flex;gap:1em;padding:.7em 1.4em;border-bottom:1px solid rgba(255,255,255,0.04);background:rgba(255,255,255,.015);">
        <span style="font-size:.68em;color:#C9A84C;font-weight:700;flex-shrink:0;padding-top:.1em;min-width:1.6em;">08</span>
        <div><div style="font-size:.84em;font-weight:600;color:#e2e8f0;line-height:1.4;">Does this fit the performer's character?</div><div style="font-size:.76em;color:rgba(180,185,210,.65);line-height:1.4;margin-top:.2em;">If not, the method is floating. The audience feels "something off" before they can name why.</div></div>
      </div>
      <div style="display:flex;gap:1em;padding:.7em 1.4em;border-bottom:1px solid rgba(255,255,255,0.04);">
        <span style="font-size:.68em;color:#C9A84C;font-weight:700;flex-shrink:0;padding-top:.1em;min-width:1.6em;">09</span>
        <div><div style="font-size:.84em;font-weight:600;color:#e2e8f0;line-height:1.4;">Does this leave the audience with a decoy explanation?</div><div style="font-size:.76em;color:rgba(180,185,210,.65);line-height:1.4;margin-top:.2em;">If not, they find the real one. Plant something true but insufficient. Give them pride in the wrong theory.</div></div>
      </div>
      <div style="display:flex;gap:1em;padding:.7em 1.4em;">
        <span style="font-size:.68em;color:#C9A84C;font-weight:700;flex-shrink:0;padding-top:.1em;min-width:1.6em;">10</span>
        <div><div style="font-size:.84em;font-weight:600;color:#e2e8f0;line-height:1.4;">Does the method disappear inside the experience — or the experience inside the method?</div><div style="font-size:.76em;color:rgba(180,185,210,.65);line-height:1.4;margin-top:.2em;">This governs everything else. The method is in service of the experience. Always. When that inverts, you are a technician.</div></div>
      </div>
    </div>
    <div style="padding:.6em 1.4em .75em;border-top:1px solid rgba(201,168,76,0.1);">
      <span style="font-size:0.7em;color:#4a5e7a;font-style:italic;">When a question reveals a gap, the gap tells you which section to return to. The diagnostic is the index.</span>
    </div>
  </div>
</div>
'''

# ── Ch18: IF YOU REMEMBER NOTHING ELSE capstone ──────────────────────────────
CH18_IFYRE_PANEL_HTML = '''
<div class="concept-box" style="margin:1.6em 0 1.2em;">
  <div class="concept-label">If You Remember Nothing Else</div>
  <div class="concept-body">
    <p><strong>Propless mentalism fails for three reasons:</strong> the audience hears you working, can trace a line from inputs to output, or watches you think. Every principle in this chapter addresses one of those three failures.</p>
    <p><strong>The premise is not the explanation.</strong> It is the frame that makes explanation unnecessary. Give the audience something to believe before you ask them to witness something they cannot explain.</p>
    <p><strong>Certainty arrives before the audience knows you are looking for it.</strong> The earlier the acquisition sits in the timeline, the more invisible it becomes. The decisive moment was buried inside something that did not look like performance.</p>
    <p><strong>The revelation must exceed the question.</strong> If you name the word, you answered a question. If you describe the life that word opened inside them, you did something the audience cannot file under any category they already own.</p>
  </div>
</div>
'''

# ── Ch19: IF YOU REMEMBER NOTHING ELSE capstone ──────────────────────────────
CH19_IFYRE_PANEL_HTML = '''
<div class="concept-box" style="margin:1.6em 0 1.2em;">
  <div class="concept-label">If You Remember Nothing Else</div>
  <div class="concept-body">
    <p><strong>The thought is not a word.</strong> It is an experience that has a word attached to it. Design your extraction around the experience, not the label.</p>
    <p><strong>Obtain information in the form the thought is naturally experienced.</strong> Enter through image, scale, movement, temperature, and emotional register. Letters are the last room, not the door.</p>
    <p><strong>The visible method should often happen after the real method is over.</strong> Get the information early inside something that looks like preparation or ritual, then stage a visible second phase that absorbs all suspicion. The audience assigns causality to the second phase. The first disappears.</p>
    <p><strong>Only reveal when it is inevitable.</strong> The C.E.R.T.A.I.N. framework ends in a declaration, not a guess. If you are not certain, do not name. Describe another quality. Add another layer.</p>
    <p><strong>Design for the worst participant.</strong> When every prompt produces structural value from either a yes or a no, you have a real system. Until then, you have a theory.</p>
  </div>
  <p class="concept-highlight">Enter through the form the thought is already living in. Work your way out to the word from there.</p>
</div>
'''

# ── Ch45: Psychological Forces — categories placeholder ──────────────────────
PSYFORCE_CATEGORIES_TBC_HTML = '''

<div style="margin:1.6em 0 2em;">
  <div style="margin-bottom:1.2em;"><p style="font-size:.82em;color:#c0ccd8;line-height:1.5;">The examples below are not designed to be creative or fooling. They are here to give you a clear reference so you can understand the architecture of each category.</p></div>
<div style="margin:0 0 1.1em;border:1px solid rgba(201,168,76,0.13);border-radius:5px;overflow:hidden;break-inside:avoid;">
  <div style="background:#0d1117;padding:.5em 1.1em .45em;border-bottom:1px solid rgba(201,168,76,0.13);display:flex;align-items:center;gap:.7em;">
    <span style="font-size:.75em;color:rgba(201,168,76,.45);font-weight:700;min-width:1.5em;">01</span>
    <span style="font-size:1.0em;font-weight:700;color:#e8dfc8;letter-spacing:.02em;">Dominant Choice</span>
  </div>
  <div style="background:#0d1117;padding:.6em 1.1em .7em;">
    <p style="font-size:.95em;color:#d8e2ea;line-height:1.55;margin:.15em 0 .6em;">Prompts where one answer dominates the category so heavily that most people arrive there immediately.</p>
    <div style="font-size:.88em;line-height:1.5;margin:.15em 0 .55em;"><span style="color:#7a8a9a;font-weight:600;">How they work:&nbsp;</span><span style="color:#c8d4e0;">Fast associative retrieval. The brain favors the lowest-effort, highest-familiarity memory trace rather than exhaustively searching all options.</span></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:.35em;margin:.4em 0 .55em;">
      <div style="border-radius:3px;padding:.35em .65em;border:1px solid rgba(74,157,143,.18);">
        <div style="font-size:.68em;letter-spacing:.1em;color:#4a9d8f;text-transform:uppercase;font-weight:700;margin-bottom:.2em;">Pros</div>
        <div style="font-size:.87em;color:#ccd6e0;line-height:1.4;">Very high hit rate. Easy to understand. Good for demonstrating the principle.</div>
      </div>
      <div style="border-radius:3px;padding:.35em .65em;border:1px solid rgba(154,80,80,.18);">
        <div style="font-size:.68em;letter-spacing:.1em;color:#9a5050;text-transform:uppercase;font-weight:700;margin-bottom:.2em;">Cons</div>
        <div style="font-size:.87em;color:#ccd6e0;line-height:1.4;">Often too transparent. The spectator may feel the answer was obvious rather than secretly influenced.</div>
      </div>
    </div>
    <div style="font-size:.88em;margin:.3em 0 .38em;line-height:1.5;"><span style="color:#C9A84C;font-weight:600;">When to use:&nbsp;</span><span style="color:#c8d4e0;">As a teaching example, quick opener, or stepping stone into a larger effect rather than the final revelation itself.</span></div>
    <div style="font-size:.86em;margin:.22em 0 .42em;line-height:1.5;"><span style="color:#8a9aaa;font-weight:600;">How to construct:&nbsp;</span><span style="color:#b8c8d4;">What is the most culturally dominant answer in this category? What would a child know first? What answer appears most in media, repetition, and memory? Keep the wording clean and fast.</span></div>
    <div style="background:rgba(255,255,255,.03);border-left:2px solid rgba(201,168,76,.25);border-radius:0 3px 3px 0;padding:.42em .7em;margin:.42em 0 0;display:flex;align-items:baseline;gap:.55em;flex-wrap:wrap;">
      <span style="font-size:.68em;letter-spacing:.1em;color:#7a8a9a;text-transform:uppercase;font-weight:700;flex-shrink:0;">Example</span>
      <span style="font-size:.92em;font-style:italic;color:#d8e2ea;">“Name a famous reindeer.”</span> <span style="font-size:.92em;color:#C9A84C;font-weight:600;">&rarr;&nbsp;Rudolph</span>
    </div>
  </div>
</div>
<div style="margin:0 0 1.1em;border:1px solid rgba(201,168,76,0.13);border-radius:5px;overflow:hidden;break-inside:avoid;">
  <div style="background:#0d1117;padding:.5em 1.1em .45em;border-bottom:1px solid rgba(201,168,76,0.13);display:flex;align-items:center;gap:.7em;">
    <span style="font-size:.75em;color:rgba(201,168,76,.45);font-weight:700;min-width:1.5em;">02</span>
    <span style="font-size:1.0em;font-weight:700;color:#e8dfc8;letter-spacing:.02em;">Statistical</span>
  </div>
  <div style="background:#0d1117;padding:.6em 1.1em .7em;">
    <p style="font-size:.95em;color:#d8e2ea;line-height:1.55;margin:.15em 0 .6em;">Common answers that are strong statistically, but not always transparently obvious.</p>
    <div style="font-size:.88em;line-height:1.5;margin:.15em 0 .55em;"><span style="color:#7a8a9a;font-weight:600;">How they work:&nbsp;</span><span style="color:#c8d4e0;">A tug-of-war between fast intuitive retrieval and light self-monitoring. The participant edits slightly, but not enough to escape the cluster.</span></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:.35em;margin:.4em 0 .55em;">
      <div style="border-radius:3px;padding:.35em .65em;border:1px solid rgba(74,157,143,.18);">
        <div style="font-size:.68em;letter-spacing:.1em;color:#4a9d8f;text-transform:uppercase;font-weight:700;margin-bottom:.2em;">Pros</div>
        <div style="font-size:.87em;color:#ccd6e0;line-height:1.4;">Better balance of hit rate and mystery. Stronger than Dominant Choice forces.</div>
      </div>
      <div style="border-radius:3px;padding:.35em .65em;border:1px solid rgba(154,80,80,.18);">
        <div style="font-size:.68em;letter-spacing:.1em;color:#9a5050;text-transform:uppercase;font-weight:700;margin-bottom:.2em;">Cons</div>
        <div style="font-size:.87em;color:#ccd6e0;line-height:1.4;">Can vary by culture, age, and wording. Needs testing.</div>
      </div>
    </div>
    <div style="font-size:.88em;margin:.3em 0 .38em;line-height:1.5;"><span style="color:#C9A84C;font-weight:600;">When to use:&nbsp;</span><span style="color:#c8d4e0;">For direct predictions, casual mindreading demonstrations, or one-ahead style pieces.</span></div>
    <div style="font-size:.86em;margin:.22em 0 .42em;line-height:1.5;"><span style="color:#8a9aaa;font-weight:600;">How to construct:&nbsp;</span><span style="color:#b8c8d4;">What answer feels random but is actually common? What avoids the obvious extremes? Remove the extremes and let them settle into the “quiet default” zone.</span></div>
    <div style="background:rgba(255,255,255,.03);border-left:2px solid rgba(201,168,76,.25);border-radius:0 3px 3px 0;padding:.42em .7em;margin:.42em 0 0;display:flex;align-items:baseline;gap:.55em;flex-wrap:wrap;">
      <span style="font-size:.68em;letter-spacing:.1em;color:#7a8a9a;text-transform:uppercase;font-weight:700;flex-shrink:0;">Example</span>
      <span style="font-size:.92em;font-style:italic;color:#d8e2ea;">“Think of a number from 1 to 10. Don’t make it too obvious.”</span> <span style="font-size:.92em;color:#C9A84C;font-weight:600;">&rarr;&nbsp;7</span>
    </div>
  </div>
</div>
<div style="margin:0 0 1.1em;border:1px solid rgba(201,168,76,0.13);border-radius:5px;overflow:hidden;break-inside:avoid;">
  <div style="background:#0d1117;padding:.5em 1.1em .45em;border-bottom:1px solid rgba(201,168,76,0.13);display:flex;align-items:center;gap:.7em;">
    <span style="font-size:.75em;color:rgba(201,168,76,.45);font-weight:700;min-width:1.5em;">03</span>
    <span style="font-size:1.0em;font-weight:700;color:#e8dfc8;letter-spacing:.02em;">Scene-Completion</span>
  </div>
  <div style="background:#0d1117;padding:.6em 1.1em .7em;">
    <p style="font-size:.95em;color:#d8e2ea;line-height:1.55;margin:.15em 0 .6em;">You put the person inside a familiar mental scene and let them fill in the missing detail.</p>
    <div style="font-size:.88em;line-height:1.5;margin:.15em 0 .55em;"><span style="color:#7a8a9a;font-weight:600;">How they work:&nbsp;</span><span style="color:#c8d4e0;">Schema activation. Familiar scene templates help the brain predict and complete missing elements quickly. The mind prefers completion over generation.</span></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:.35em;margin:.4em 0 .55em;">
      <div style="border-radius:3px;padding:.35em .65em;border:1px solid rgba(74,157,143,.18);">
        <div style="font-size:.68em;letter-spacing:.1em;color:#4a9d8f;text-transform:uppercase;font-weight:700;margin-bottom:.2em;">Pros</div>
        <div style="font-size:.87em;color:#ccd6e0;line-height:1.4;">Feel much more psychological and personal. Less obviously mechanical.</div>
      </div>
      <div style="border-radius:3px;padding:.35em .65em;border:1px solid rgba(154,80,80,.18);">
        <div style="font-size:.68em;letter-spacing:.1em;color:#9a5050;text-transform:uppercase;font-weight:700;margin-bottom:.2em;">Cons</div>
        <div style="font-size:.87em;color:#ccd6e0;line-height:1.4;">Need careful wording. Too broad a scene can create multiple common answers.</div>
      </div>
    </div>
    <div style="font-size:.88em;margin:.3em 0 .38em;line-height:1.5;"><span style="color:#C9A84C;font-weight:600;">When to use:&nbsp;</span><span style="color:#c8d4e0;">Close-up and intimate mentalism, book tests, drawing duplications, or anything memory-themed.</span></div>
    <div style="font-size:.86em;margin:.22em 0 .42em;line-height:1.5;"><span style="color:#8a9aaa;font-weight:600;">How to construct:&nbsp;</span><span style="color:#b8c8d4;">What object is expected but not guaranteed in this scene? What item is noticed most when missing? What captures the function of the moment? Use a familiar place, a specific moment in time, and a missing functional object.</span></div>
    <div style="background:rgba(255,255,255,.03);border-left:2px solid rgba(201,168,76,.25);border-radius:0 3px 3px 0;padding:.42em .7em;margin:.42em 0 0;display:flex;align-items:baseline;gap:.55em;flex-wrap:wrap;">
      <span style="font-size:.68em;letter-spacing:.1em;color:#7a8a9a;text-transform:uppercase;font-weight:700;flex-shrink:0;">Example</span>
      <span style="font-size:.92em;font-style:italic;color:#d8e2ea;">“Picture a junk drawer in a kitchen. Think of the one object people always seem to need, but never when they’re actually looking for it.”</span> <span style="font-size:.92em;color:#C9A84C;font-weight:600;">&rarr;&nbsp;Scissors</span>
    </div>
  </div>
</div>
<div style="margin:0 0 1.1em;border:1px solid rgba(201,168,76,0.13);border-radius:5px;overflow:hidden;break-inside:avoid;">
  <div style="background:#0d1117;padding:.5em 1.1em .45em;border-bottom:1px solid rgba(201,168,76,0.13);display:flex;align-items:center;gap:.7em;">
    <span style="font-size:.75em;color:rgba(201,168,76,.45);font-weight:700;min-width:1.5em;">04</span>
    <span style="font-size:1.0em;font-weight:700;color:#e8dfc8;letter-spacing:.02em;">Contextual</span>
  </div>
  <div style="background:#0d1117;padding:.6em 1.1em .7em;">
    <p style="font-size:.95em;color:#d8e2ea;line-height:1.55;margin:.15em 0 .6em;">Framing, emotion, or story narrows the answer until one choice feels natural.</p>
    <div style="font-size:.88em;line-height:1.5;margin:.15em 0 .55em;"><span style="color:#7a8a9a;font-weight:600;">How they work:&nbsp;</span><span style="color:#c8d4e0;">Concept priming through emotional and narrative context. Once a frame is active, compatible answers become easier to retrieve. People choose inside the frame, not outside it.</span></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:.35em;margin:.4em 0 .55em;">
      <div style="border-radius:3px;padding:.35em .65em;border:1px solid rgba(74,157,143,.18);">
        <div style="font-size:.68em;letter-spacing:.1em;color:#4a9d8f;text-transform:uppercase;font-weight:700;margin-bottom:.2em;">Pros</div>
        <div style="font-size:.87em;color:#ccd6e0;line-height:1.4;">Very deceptive. Hides the method well. Feels organic and genuinely psychological.</div>
      </div>
      <div style="border-radius:3px;padding:.35em .65em;border:1px solid rgba(154,80,80,.18);">
        <div style="font-size:.68em;letter-spacing:.1em;color:#9a5050;text-transform:uppercase;font-weight:700;margin-bottom:.2em;">Cons</div>
        <div style="font-size:.87em;color:#ccd6e0;line-height:1.4;">Requires stronger scripting and delivery. Harder to improvise cleanly.</div>
      </div>
    </div>
    <div style="font-size:.88em;margin:.3em 0 .38em;line-height:1.5;"><span style="color:#C9A84C;font-weight:600;">When to use:&nbsp;</span><span style="color:#c8d4e0;">Longer routines, stage pieces, or when you want the force to feel like genuine thought-reading rather than coincidence.</span></div>
    <div style="font-size:.86em;margin:.22em 0 .42em;line-height:1.5;"><span style="color:#8a9aaa;font-weight:600;">How to construct:&nbsp;</span><span style="color:#b8c8d4;">What answer best fits this mood? What answer feels cinematic inside this frame? What is emotionally right, not logically correct? Build with a feeling, a qualifier, and a vivid tone.</span></div>
    <div style="background:rgba(255,255,255,.03);border-left:2px solid rgba(201,168,76,.25);border-radius:0 3px 3px 0;padding:.42em .7em;margin:.42em 0 0;display:flex;align-items:baseline;gap:.55em;flex-wrap:wrap;">
      <span style="font-size:.68em;letter-spacing:.1em;color:#7a8a9a;text-transform:uppercase;font-weight:700;flex-shrink:0;">Example</span>
      <span style="font-size:.92em;font-style:italic;color:#d8e2ea;">“Think of a city that feels expensive and impressive. Not just big…”</span> <span style="font-size:.92em;color:#C9A84C;font-weight:600;">&rarr;&nbsp;Dubai (backup: Tokyo)</span>
    </div>
  </div>
</div>
<div style="margin:0 0 1.1em;border:1px solid rgba(201,168,76,0.13);border-radius:5px;overflow:hidden;break-inside:avoid;">
  <div style="background:#0d1117;padding:.5em 1.1em .45em;border-bottom:1px solid rgba(201,168,76,0.13);display:flex;align-items:center;gap:.7em;">
    <span style="font-size:.75em;color:rgba(201,168,76,.45);font-weight:700;min-width:1.5em;">05</span>
    <span style="font-size:1.0em;font-weight:700;color:#e8dfc8;letter-spacing:.02em;">Anchoring</span>
  </div>
  <div style="background:#0d1117;padding:.6em 1.1em .7em;">
    <p style="font-size:.95em;color:#d8e2ea;line-height:1.55;margin:.15em 0 .6em;">An earlier word, image, or idea quietly biases a later choice.</p>
    <div style="font-size:.88em;line-height:1.5;margin:.15em 0 .55em;"><span style="color:#7a8a9a;font-weight:600;">How they work:&nbsp;</span><span style="color:#c8d4e0;">Associative priming. Related concepts remain more available in memory after activation. Earlier ideas stay mentally warm when the later choice arrives.</span></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:.35em;margin:.4em 0 .55em;">
      <div style="border-radius:3px;padding:.35em .65em;border:1px solid rgba(74,157,143,.18);">
        <div style="font-size:.68em;letter-spacing:.1em;color:#4a9d8f;text-transform:uppercase;font-weight:700;margin-bottom:.2em;">Pros</div>
        <div style="font-size:.87em;color:#ccd6e0;line-height:1.4;">Elegant and invisible when done well. Can happen far before the reveal moment.</div>
      </div>
      <div style="border-radius:3px;padding:.35em .65em;border:1px solid rgba(154,80,80,.18);">
        <div style="font-size:.68em;letter-spacing:.1em;color:#9a5050;text-transform:uppercase;font-weight:700;margin-bottom:.2em;">Cons</div>
        <div style="font-size:.87em;color:#ccd6e0;line-height:1.4;">Subtle enough that results can be inconsistent without good supporting structure.</div>
      </div>
    </div>
    <div style="font-size:.88em;margin:.3em 0 .38em;line-height:1.5;"><span style="color:#C9A84C;font-weight:600;">When to use:&nbsp;</span><span style="color:#c8d4e0;">As an early seed in a routine, or layered with another force to strengthen the outcome. Best when combined, not used alone.</span></div>
    <div style="font-size:.86em;margin:.22em 0 .42em;line-height:1.5;"><span style="color:#8a9aaa;font-weight:600;">How to construct:&nbsp;</span><span style="color:#b8c8d4;">What words or images connect naturally to your target? How can you plant them organically? How far before the force can you seed the answer?</span></div>
    <div style="background:rgba(255,255,255,.03);border-left:2px solid rgba(201,168,76,.25);border-radius:0 3px 3px 0;padding:.42em .7em;margin:.42em 0 0;display:flex;align-items:baseline;gap:.55em;flex-wrap:wrap;">
      <span style="font-size:.68em;letter-spacing:.1em;color:#7a8a9a;text-transform:uppercase;font-weight:700;flex-shrink:0;">Example</span>
      <span style="font-size:.92em;font-style:italic;color:#d8e2ea;">Talk casually about celebrities, fame, constellations, wishes, Hollywood, and the night sky. Then ask: “Think of a simple shape or symbol you could easily draw.”</span> <span style="font-size:.92em;color:#C9A84C;font-weight:600;">&rarr;&nbsp;Star</span>
    </div>
  </div>
</div>
<div style="margin:0 0 1.1em;border:1px solid rgba(201,168,76,0.13);border-radius:5px;overflow:hidden;break-inside:avoid;">
  <div style="background:#0d1117;padding:.5em 1.1em .45em;border-bottom:1px solid rgba(201,168,76,0.13);display:flex;align-items:center;gap:.7em;">
    <span style="font-size:.75em;color:rgba(201,168,76,.45);font-weight:700;min-width:1.5em;">06</span>
    <span style="font-size:1.0em;font-weight:700;color:#e8dfc8;letter-spacing:.02em;">Exclusion</span>
  </div>
  <div style="background:#0d1117;padding:.6em 1.1em .7em;">
    <p style="font-size:.95em;color:#d8e2ea;line-height:1.55;margin:.15em 0 .6em;">Establish a category, remove the most obvious options, and let the remaining target feel self-chosen.</p>
    <div style="font-size:.88em;line-height:1.5;margin:.15em 0 .55em;"><span style="color:#7a8a9a;font-weight:600;">How they work:&nbsp;</span><span style="color:#c8d4e0;">Local search after pruning. Once options are excluded, the brain works from remaining nearby candidates rather than rebuilding the full answer-space from scratch.</span></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:.35em;margin:.4em 0 .55em;">
      <div style="border-radius:3px;padding:.35em .65em;border:1px solid rgba(74,157,143,.18);">
        <div style="font-size:.68em;letter-spacing:.1em;color:#4a9d8f;text-transform:uppercase;font-weight:700;margin-bottom:.2em;">Pros</div>
        <div style="font-size:.87em;color:#ccd6e0;line-height:1.4;">Can be very strong. Feels impossible when it lands. Useful for narrowing broad categories without sounding procedural.</div>
      </div>
      <div style="border-radius:3px;padding:.35em .65em;border:1px solid rgba(154,80,80,.18);">
        <div style="font-size:.68em;letter-spacing:.1em;color:#9a5050;text-transform:uppercase;font-weight:700;margin-bottom:.2em;">Cons</div>
        <div style="font-size:.87em;color:#ccd6e0;line-height:1.4;">If exclusions are too specific, the method becomes visible. If handled clumsily, it feels like steering rather than mind-reading.</div>
      </div>
    </div>
    <div style="font-size:.88em;margin:.3em 0 .38em;line-height:1.5;"><span style="color:#C9A84C;font-weight:600;">When to use:&nbsp;</span><span style="color:#c8d4e0;">When you want to guide a thought inside a known category while keeping the choice feeling free. Works especially well layered with anchoring or earlier framing.</span></div>
    <div style="font-size:.86em;margin:.22em 0 .42em;line-height:1.5;"><span style="color:#8a9aaa;font-weight:600;">How to construct:&nbsp;</span><span style="color:#b8c8d4;">What are the top 2–3 most obvious answers in this category? If you remove them, what attractive remainder is left? Can you make the exclusions sound casual rather than procedural?</span></div>
    <div style="background:rgba(255,255,255,.03);border-left:2px solid rgba(201,168,76,.25);border-radius:0 3px 3px 0;padding:.42em .7em;margin:.42em 0 0;display:flex;align-items:baseline;gap:.55em;flex-wrap:wrap;">
      <span style="font-size:.68em;letter-spacing:.1em;color:#7a8a9a;text-transform:uppercase;font-weight:700;flex-shrink:0;">Example</span>
      <span style="font-size:.92em;font-style:italic;color:#d8e2ea;">“Picture a simple shape. Not a square or a rectangle.”</span> <span style="font-size:.92em;color:#C9A84C;font-weight:600;">&rarr;&nbsp;Triangle</span>
    </div>
    <div style="font-size:.87em;color:#c8b49a;margin:.4em 0 0;line-height:1.5;padding:.35em .65em;border-left:2px solid rgba(154,120,80,.3);">Note: Simply mentioning the alternatives tends to suppress them. The exclusion does not need to be forceful to be effective.</div>
  </div>
</div>
<div style="margin:0 0 1.1em;border:1px solid rgba(201,168,76,0.13);border-radius:5px;overflow:hidden;break-inside:avoid;">
  <div style="background:#0d1117;padding:.5em 1.1em .45em;border-bottom:1px solid rgba(201,168,76,0.13);display:flex;align-items:center;gap:.7em;">
    <span style="font-size:.75em;color:rgba(201,168,76,.45);font-weight:700;min-width:1.5em;">07</span>
    <span style="font-size:1.0em;font-weight:700;color:#e8dfc8;letter-spacing:.02em;">Phonetic</span>
  </div>
  <div style="background:#0d1117;padding:.6em 1.1em .7em;">
    <p style="font-size:.95em;color:#d8e2ea;line-height:1.55;margin:.15em 0 .6em;">Forces based on the sound, rhythm, or feel of words.</p>
    <div style="font-size:.88em;line-height:1.5;margin:.15em 0 .55em;"><span style="color:#7a8a9a;font-weight:600;">How they work:&nbsp;</span><span style="color:#c8d4e0;">Cross-links between sound processing, meaning, and imagery. The word does not just mean something—it feels like something. Similar sounds and word-texture can bias retrieval.</span></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:.35em;margin:.4em 0 .55em;">
      <div style="border-radius:3px;padding:.35em .65em;border:1px solid rgba(74,157,143,.18);">
        <div style="font-size:.68em;letter-spacing:.1em;color:#4a9d8f;text-transform:uppercase;font-weight:700;margin-bottom:.2em;">Pros</div>
        <div style="font-size:.87em;color:#ccd6e0;line-height:1.4;">Very unusual. Can feel deeply psychological and non-obvious when constructed well.</div>
      </div>
      <div style="border-radius:3px;padding:.35em .65em;border:1px solid rgba(154,80,80,.18);">
        <div style="font-size:.68em;letter-spacing:.1em;color:#9a5050;text-transform:uppercase;font-weight:700;margin-bottom:.2em;">Cons</div>
        <div style="font-size:.87em;color:#ccd6e0;line-height:1.4;">Harder to script. More language-dependent. Can fail if the wording is not precise.</div>
      </div>
    </div>
    <div style="font-size:.88em;margin:.3em 0 .38em;line-height:1.5;"><span style="color:#C9A84C;font-weight:600;">When to use:&nbsp;</span><span style="color:#c8d4e0;">When you want to force shapes, invented words, textures, or qualities rather than obvious named objects.</span></div>
    <div style="font-size:.86em;margin:.22em 0 .42em;line-height:1.5;"><span style="color:#8a9aaa;font-weight:600;">How to construct:&nbsp;</span><span style="color:#b8c8d4;">What target word has helpful sound echoes? What nearby words can smuggle those sounds into natural speech? What does the target feel like in the mouth or ear?</span></div>
    <div style="background:rgba(255,255,255,.03);border-left:2px solid rgba(201,168,76,.25);border-radius:0 3px 3px 0;padding:.42em .7em;margin:.42em 0 0;display:flex;align-items:baseline;gap:.55em;flex-wrap:wrap;">
      <span style="font-size:.68em;letter-spacing:.1em;color:#7a8a9a;text-transform:uppercase;font-weight:700;flex-shrink:0;">Example</span>
      <span style="font-size:.92em;font-style:italic;color:#d8e2ea;">“Think of a small object. Something simple. Something people bring with them, wear, hold, or keep.”</span> <span style="font-size:.92em;color:#C9A84C;font-weight:600;">&rarr;&nbsp;Ring</span>
    </div>
    <div style="font-size:.87em;color:#b8c8d4;font-style:italic;margin:.4em 0 0;line-height:1.5;padding:.35em .65em;border-left:2px solid rgba(201,168,76,.2);">Why it works: “Bring,” “thing,” “keep,” and “wear” share phonetic echoes with ring without naming it directly.</div>
  </div>
</div>
<div style="margin:0 0 1.1em;border:1px solid rgba(201,168,76,0.13);border-radius:5px;overflow:hidden;break-inside:avoid;">
  <div style="background:#0d1117;padding:.5em 1.1em .45em;border-bottom:1px solid rgba(201,168,76,0.13);display:flex;align-items:center;gap:.7em;">
    <span style="font-size:.75em;color:rgba(201,168,76,.45);font-weight:700;min-width:1.5em;">08</span>
    <span style="font-size:1.0em;font-weight:700;color:#e8dfc8;letter-spacing:.02em;">Sensory</span>
  </div>
  <div style="background:#0d1117;padding:.6em 1.1em .7em;">
    <p style="font-size:.95em;color:#d8e2ea;line-height:1.55;margin:.15em 0 .6em;">Forces through smell, touch, temperature, sound, or physical memory.</p>
    <div style="font-size:.88em;line-height:1.5;margin:.15em 0 .55em;"><span style="color:#7a8a9a;font-weight:600;">How they work:&nbsp;</span><span style="color:#c8d4e0;">Sensory cues—especially smell—connect strongly to autobiographical memory and emotion. Sensory memory often feels more private, vivid, and immediate than verbal category search.</span></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:.35em;margin:.4em 0 .55em;">
      <div style="border-radius:3px;padding:.35em .65em;border:1px solid rgba(74,157,143,.18);">
        <div style="font-size:.68em;letter-spacing:.1em;color:#4a9d8f;text-transform:uppercase;font-weight:700;margin-bottom:.2em;">Pros</div>
        <div style="font-size:.87em;color:#ccd6e0;line-height:1.4;">One of the strongest theatrical categories. Feels private, emotional, and real.</div>
      </div>
      <div style="border-radius:3px;padding:.35em .65em;border:1px solid rgba(154,80,80,.18);">
        <div style="font-size:.68em;letter-spacing:.1em;color:#9a5050;text-transform:uppercase;font-weight:700;margin-bottom:.2em;">Cons</div>
        <div style="font-size:.87em;color:#ccd6e0;line-height:1.4;">Can split into a few common answers. Needs careful exclusions to narrow the cluster.</div>
      </div>
    </div>
    <div style="font-size:.88em;margin:.3em 0 .38em;line-height:1.5;"><span style="color:#C9A84C;font-weight:600;">When to use:&nbsp;</span><span style="color:#c8d4e0;">Intimate work, emotional routines, memory pieces, or material that should feel less like a trick and more like a genuine reading.</span></div>
    <div style="font-size:.86em;margin:.22em 0 .42em;line-height:1.5;"><span style="color:#8a9aaa;font-weight:600;">How to construct:&nbsp;</span><span style="color:#b8c8d4;">What sensory memory is early, vivid, and common? What cue is simple rather than complex? What can you exclude to remove diffuse or competing answers?</span></div>
    <div style="background:rgba(255,255,255,.03);border-left:2px solid rgba(201,168,76,.25);border-radius:0 3px 3px 0;padding:.42em .7em;margin:.42em 0 0;display:flex;align-items:baseline;gap:.55em;flex-wrap:wrap;">
      <span style="font-size:.68em;letter-spacing:.1em;color:#7a8a9a;text-transform:uppercase;font-weight:700;flex-shrink:0;">Example</span>
      <span style="font-size:.92em;font-style:italic;color:#d8e2ea;">“Think of a smell from childhood. Not food, not perfume. Something simple that takes you back immediately.”</span> <span style="font-size:.92em;color:#C9A84C;font-weight:600;">&rarr;&nbsp;Crayons</span>
    </div>
  </div>
</div>
<div style="margin:0 0 1.1em;border:1px solid rgba(201,168,76,0.13);border-radius:5px;overflow:hidden;break-inside:avoid;">
  <div style="background:#0d1117;padding:.5em 1.1em .45em;border-bottom:1px solid rgba(201,168,76,0.13);display:flex;align-items:center;gap:.7em;">
    <span style="font-size:.75em;color:rgba(201,168,76,.45);font-weight:700;min-width:1.5em;">09</span>
    <span style="font-size:1.0em;font-weight:700;color:#e8dfc8;letter-spacing:.02em;">Social-Normalcy</span>
  </div>
  <div style="background:#0d1117;padding:.6em 1.1em .7em;">
    <p style="font-size:.95em;color:#d8e2ea;line-height:1.55;margin:.15em 0 .6em;">These exploit the tendency to choose the safe, acceptable, non-weird answer.</p>
    <div style="font-size:.88em;line-height:1.5;margin:.15em 0 .55em;"><span style="color:#7a8a9a;font-weight:600;">How they work:&nbsp;</span><span style="color:#c8d4e0;">Choice shaped by self-monitoring and social evaluation. People filter their answer through what feels normal to say aloud in front of others.</span></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:.35em;margin:.4em 0 .55em;">
      <div style="border-radius:3px;padding:.35em .65em;border:1px solid rgba(74,157,143,.18);">
        <div style="font-size:.68em;letter-spacing:.1em;color:#4a9d8f;text-transform:uppercase;font-weight:700;margin-bottom:.2em;">Pros</div>
        <div style="font-size:.87em;color:#ccd6e0;line-height:1.4;">Often highly reliable in live performance. Spectators rarely realize social pressure is shaping their choice.</div>
      </div>
      <div style="border-radius:3px;padding:.35em .65em;border:1px solid rgba(154,80,80,.18);">
        <div style="font-size:.68em;letter-spacing:.1em;color:#9a5050;text-transform:uppercase;font-weight:700;margin-bottom:.2em;">Cons</div>
        <div style="font-size:.87em;color:#ccd6e0;line-height:1.4;">Can feel ordinary if overused. The safest answer is sometimes also the dullest.</div>
      </div>
    </div>
    <div style="font-size:.88em;margin:.3em 0 .38em;line-height:1.5;"><span style="color:#C9A84C;font-weight:600;">When to use:&nbsp;</span><span style="color:#c8d4e0;">When asking about preferences, drinks, pets, habits, or anything where people want to seem like a reasonable, normal person.</span></div>
    <div style="font-size:.86em;margin:.22em 0 .42em;line-height:1.5;"><span style="color:#8a9aaa;font-weight:600;">How to construct:&nbsp;</span><span style="color:#b8c8d4;">What answer sounds socially safe in this room? What avoids embarrassment or over-literalness? What sounds like what a “normal person” would say aloud?</span></div>
    <div style="background:rgba(255,255,255,.03);border-left:2px solid rgba(201,168,76,.25);border-radius:0 3px 3px 0;padding:.42em .7em;margin:.42em 0 0;display:flex;align-items:baseline;gap:.55em;flex-wrap:wrap;">
      <span style="font-size:.68em;letter-spacing:.1em;color:#7a8a9a;text-transform:uppercase;font-weight:700;flex-shrink:0;">Example</span>
      <span style="font-size:.92em;font-style:italic;color:#d8e2ea;">“Think of a drink people have every day.”</span> <span style="font-size:.92em;color:#C9A84C;font-weight:600;">&rarr;&nbsp;Coffee</span>
    </div>
    <div style="font-size:.87em;color:#b8c8d4;font-style:italic;margin:.4em 0 0;line-height:1.5;padding:.35em .65em;border-left:2px solid rgba(201,168,76,.2);">Why it works: Water is technically correct but often feels too literal or socially flat. Coffee sounds more human and more performatively normal.</div>
  </div>
</div>
<div style="margin:0 0 1.1em;border:1px solid rgba(201,168,76,0.13);border-radius:5px;overflow:hidden;break-inside:avoid;">
  <div style="background:#0d1117;padding:.5em 1.1em .45em;border-bottom:1px solid rgba(201,168,76,0.13);display:flex;align-items:center;gap:.7em;">
    <span style="font-size:.75em;color:rgba(201,168,76,.45);font-weight:700;min-width:1.5em;">10</span>
    <span style="font-size:1.0em;font-weight:700;color:#e8dfc8;letter-spacing:.02em;">Contrast / Opposites</span>
  </div>
  <div style="background:#0d1117;padding:.6em 1.1em .7em;">
    <p style="font-size:.95em;color:#d8e2ea;line-height:1.55;margin:.15em 0 .6em;">You ask for the opposite of something, and they land on a dominant contrast rather than searching broadly.</p>
    <div style="font-size:.88em;line-height:1.5;margin:.15em 0 .55em;"><span style="color:#7a8a9a;font-weight:600;">How they work:&nbsp;</span><span style="color:#c8d4e0;">The original concept stays active and shapes the search. The “opposite” is found nearby, not globally. People do not search the full universe of opposites.</span></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:.35em;margin:.4em 0 .55em;">
      <div style="border-radius:3px;padding:.35em .65em;border:1px solid rgba(74,157,143,.18);">
        <div style="font-size:.68em;letter-spacing:.1em;color:#4a9d8f;text-transform:uppercase;font-weight:700;margin-bottom:.2em;">Pros</div>
        <div style="font-size:.87em;color:#ccd6e0;line-height:1.4;">Feels broad, but is often narrower than it sounds. Good for more disguised forcing.</div>
      </div>
      <div style="border-radius:3px;padding:.35em .65em;border:1px solid rgba(154,80,80,.18);">
        <div style="font-size:.68em;letter-spacing:.1em;color:#9a5050;text-transform:uppercase;font-weight:700;margin-bottom:.2em;">Cons</div>
        <div style="font-size:.87em;color:#ccd6e0;line-height:1.4;">Can produce multiple valid opposites unless the setup is tight.</div>
      </div>
    </div>
    <div style="font-size:.88em;margin:.3em 0 .38em;line-height:1.5;"><span style="color:#C9A84C;font-weight:600;">When to use:&nbsp;</span><span style="color:#c8d4e0;">When you want a force to feel conceptually open, but still converge on a predictable answer.</span></div>
    <div style="font-size:.86em;margin:.22em 0 .42em;line-height:1.5;"><span style="color:#8a9aaa;font-weight:600;">How to construct:&nbsp;</span><span style="color:#b8c8d4;">What is the most prototypical opposite of this idea? Can you constrain the kind of opposite they choose? How can you stop them from going abstract?</span></div>
    <div style="background:rgba(255,255,255,.03);border-left:2px solid rgba(201,168,76,.25);border-radius:0 3px 3px 0;padding:.42em .7em;margin:.42em 0 0;display:flex;align-items:baseline;gap:.55em;flex-wrap:wrap;">
      <span style="font-size:.68em;letter-spacing:.1em;color:#7a8a9a;text-transform:uppercase;font-weight:700;flex-shrink:0;">Example</span>
      <span style="font-size:.92em;font-style:italic;color:#d8e2ea;">“Think of something soft. Now think of something the exact opposite.”</span> <span style="font-size:.92em;color:#C9A84C;font-weight:600;">&rarr;&nbsp;Rock or metal (depending on framing)</span>
    </div>
  </div>
</div>
<div style="margin:0 0 1.1em;border:1px solid rgba(201,168,76,0.13);border-radius:5px;overflow:hidden;break-inside:avoid;">
  <div style="background:#0d1117;padding:.5em 1.1em .45em;border-bottom:1px solid rgba(201,168,76,0.13);display:flex;align-items:center;gap:.7em;">
    <span style="font-size:.75em;color:rgba(201,168,76,.45);font-weight:700;min-width:1.5em;">11</span>
    <span style="font-size:1.0em;font-weight:700;color:#e8dfc8;letter-spacing:.02em;">Psychological Framing</span>
  </div>
  <div style="background:#0d1117;padding:.6em 1.1em .7em;">
    <p style="font-size:.95em;color:#d8e2ea;line-height:1.55;margin:.15em 0 .6em;">The answer is shaped by order, pause, emphasis, gesture, salience, or how the idea is presented.</p>
    <div style="font-size:.88em;line-height:1.5;margin:.15em 0 .55em;"><span style="color:#7a8a9a;font-weight:600;">How they work:&nbsp;</span><span style="color:#c8d4e0;">Attentional weighting. The brain privileges what is most salient or easiest to process. The answer that is most emphasized, best placed, or easiest to picture often wins.</span></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:.35em;margin:.4em 0 .55em;">
      <div style="border-radius:3px;padding:.35em .65em;border:1px solid rgba(74,157,143,.18);">
        <div style="font-size:.68em;letter-spacing:.1em;color:#4a9d8f;text-transform:uppercase;font-weight:700;margin-bottom:.2em;">Pros</div>
        <div style="font-size:.87em;color:#ccd6e0;line-height:1.4;">Very powerful when combined with other categories. Often entirely invisible.</div>
      </div>
      <div style="border-radius:3px;padding:.35em .65em;border:1px solid rgba(154,80,80,.18);">
        <div style="font-size:.68em;letter-spacing:.1em;color:#9a5050;text-transform:uppercase;font-weight:700;margin-bottom:.2em;">Cons</div>
        <div style="font-size:.87em;color:#ccd6e0;line-height:1.4;">Rarely strong enough by itself. Depends heavily on performance skill and live delivery.</div>
      </div>
    </div>
    <div style="font-size:.88em;margin:.3em 0 .38em;line-height:1.5;"><span style="color:#C9A84C;font-weight:600;">When to use:&nbsp;</span><span style="color:#c8d4e0;">As a hidden support layer underneath another force, not as the primary mechanism.</span></div>
    <div style="font-size:.86em;margin:.22em 0 .42em;line-height:1.5;"><span style="color:#8a9aaa;font-weight:600;">How to construct:&nbsp;</span><span style="color:#b8c8d4;">What can you place for maximum attention? What is easiest to picture? What word sounds strongest when spoken aloud?</span></div>
    <div style="background:rgba(255,255,255,.03);border-left:2px solid rgba(201,168,76,.25);border-radius:0 3px 3px 0;padding:.42em .7em;margin:.42em 0 0;display:flex;align-items:baseline;gap:.55em;flex-wrap:wrap;">
      <span style="font-size:.68em;letter-spacing:.1em;color:#7a8a9a;text-transform:uppercase;font-weight:700;flex-shrink:0;">Example</span>
      <span style="font-size:.92em;font-style:italic;color:#d8e2ea;">“Focus on one of these words: Furmery, Redundant, Capcasian Hemisphere, or Triage.”</span> <span style="font-size:.92em;color:#C9A84C;font-weight:600;">&rarr;&nbsp;Hemisphere</span>
    </div>
    <div style="font-size:.87em;color:#b8c8d4;font-style:italic;margin:.4em 0 0;line-height:1.5;padding:.35em .65em;border-left:2px solid rgba(201,168,76,.2);">Why it works: Second to last in the list, naturally emphasized in speech, and the easiest to picture of the four.</div>
  </div>
</div>
<div style="margin:0 0 1.1em;border:1px solid rgba(201,168,76,0.13);border-radius:5px;overflow:hidden;break-inside:avoid;">
  <div style="background:#0d1117;padding:.5em 1.1em .45em;border-bottom:1px solid rgba(201,168,76,0.13);display:flex;align-items:center;gap:.7em;">
    <span style="font-size:.75em;color:rgba(201,168,76,.45);font-weight:700;min-width:1.5em;">12</span>
    <span style="font-size:1.0em;font-weight:700;color:#e8dfc8;letter-spacing:.02em;">Timing and Compliance</span>
  </div>
  <div style="background:#0d1117;padding:.6em 1.1em .7em;">
    <p style="font-size:.95em;color:#d8e2ea;line-height:1.55;margin:.15em 0 .6em;">Forces that depend on when the instruction lands and when the participant mentally commits.</p>
    <div style="font-size:.88em;line-height:1.5;margin:.15em 0 .55em;"><span style="color:#7a8a9a;font-weight:600;">How they work:&nbsp;</span><span style="color:#c8d4e0;">Commitment inertia under time pressure. Once a person begins a response pattern, they usually continue it. The brain starts the action path before later instructions can reshape it.</span></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:.35em;margin:.4em 0 .55em;">
      <div style="border-radius:3px;padding:.35em .65em;border:1px solid rgba(74,157,143,.18);">
        <div style="font-size:.68em;letter-spacing:.1em;color:#4a9d8f;text-transform:uppercase;font-weight:700;margin-bottom:.2em;">Pros</div>
        <div style="font-size:.87em;color:#ccd6e0;line-height:1.4;">Can be extremely deceptive. Useful in live, controlled interaction where you manage the pacing.</div>
      </div>
      <div style="border-radius:3px;padding:.35em .65em;border:1px solid rgba(154,80,80,.18);">
        <div style="font-size:.68em;letter-spacing:.1em;color:#9a5050;text-transform:uppercase;font-weight:700;margin-bottom:.2em;">Cons</div>
        <div style="font-size:.87em;color:#ccd6e0;line-height:1.4;">Timing must be precise. Harder to teach on paper than to perform in person.</div>
      </div>
    </div>
    <div style="font-size:.88em;margin:.3em 0 .38em;line-height:1.5;"><span style="color:#C9A84C;font-weight:600;">When to use:&nbsp;</span><span style="color:#c8d4e0;">In a polished live performance, especially when you can control rhythm and interrupt thought flow before the participant settles on a deliberate choice.</span></div>
    <div style="font-size:.86em;margin:.22em 0 .42em;line-height:1.5;"><span style="color:#8a9aaa;font-weight:600;">How to construct:&nbsp;</span><span style="color:#b8c8d4;">When does the participant begin deciding? Can you deliver a clarification after commitment starts? Can you use rhythm to create a predictable lag between instruction and action?</span></div>
    <div style="background:rgba(255,255,255,.03);border-left:2px solid rgba(201,168,76,.25);border-radius:0 3px 3px 0;padding:.42em .7em;margin:.42em 0 0;display:flex;align-items:baseline;gap:.55em;flex-wrap:wrap;">
      <span style="font-size:.68em;letter-spacing:.1em;color:#7a8a9a;text-transform:uppercase;font-weight:700;flex-shrink:0;">Example</span>
      <span style="font-size:.92em;font-style:italic;color:#d8e2ea;">When dealing cards onto a table, tell the spectator to say stop at any time. They will often stop 3 cards after the instruction—but you must already be dealing before giving the direction.</span>
    </div>
  </div>
</div>
<div style="margin:0 0 1.1em;border:1px solid rgba(201,168,76,0.13);border-radius:5px;overflow:hidden;break-inside:avoid;">
  <div style="background:#0d1117;padding:.5em 1.1em .45em;border-bottom:1px solid rgba(201,168,76,0.13);display:flex;align-items:center;gap:.7em;">
    <span style="font-size:.75em;color:rgba(201,168,76,.45);font-weight:700;min-width:1.5em;">13</span>
    <span style="font-size:1.0em;font-weight:700;color:#e8dfc8;letter-spacing:.02em;">Piggyback</span>
  </div>
  <div style="background:#0d1117;padding:.6em 1.1em .7em;">
    <p style="font-size:.95em;color:#d8e2ea;line-height:1.55;margin:.15em 0 .6em;">You start with one force, then convert that answer into another domain.</p>
    <div style="font-size:.88em;line-height:1.5;margin:.15em 0 .55em;"><span style="color:#7a8a9a;font-weight:600;">How they work:&nbsp;</span><span style="color:#c8d4e0;">Associative chaining. Once the first answer is stabilized, later thoughts build naturally from it. The original force becomes less visible because attention has moved on.</span></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:.35em;margin:.4em 0 .55em;">
      <div style="border-radius:3px;padding:.35em .65em;border:1px solid rgba(74,157,143,.18);">
        <div style="font-size:.68em;letter-spacing:.1em;color:#4a9d8f;text-transform:uppercase;font-weight:700;margin-bottom:.2em;">Pros</div>
        <div style="font-size:.87em;color:#ccd6e0;line-height:1.4;">Excellent for disguising the original force. Makes the final reveal seem much broader and more impossible.</div>
      </div>
      <div style="border-radius:3px;padding:.35em .65em;border:1px solid rgba(154,80,80,.18);">
        <div style="font-size:.68em;letter-spacing:.1em;color:#9a5050;text-transform:uppercase;font-weight:700;margin-bottom:.2em;">Cons</div>
        <div style="font-size:.87em;color:#ccd6e0;line-height:1.4;">More structure required. If the first force is weak, the whole chain suffers.</div>
      </div>
    </div>
    <div style="font-size:.88em;margin:.3em 0 .38em;line-height:1.5;"><span style="color:#C9A84C;font-weight:600;">When to use:&nbsp;</span><span style="color:#c8d4e0;">For multi-phase routines, apparent mindreading, and effects that should grow in impossibility across multiple steps.</span></div>
    <div style="font-size:.86em;margin:.22em 0 .42em;line-height:1.5;"><span style="color:#8a9aaa;font-weight:600;">How to construct:&nbsp;</span><span style="color:#b8c8d4;">If they think X, what naturally follows? Can you move from image to word, word to letter, object to place? Does the second step feel justified rather than forced?</span></div>
    <div style="background:rgba(255,255,255,.03);border-left:2px solid rgba(201,168,76,.25);border-radius:0 3px 3px 0;padding:.42em .7em;margin:.42em 0 0;display:flex;align-items:baseline;gap:.55em;flex-wrap:wrap;">
      <span style="font-size:.68em;letter-spacing:.1em;color:#7a8a9a;text-transform:uppercase;font-weight:700;flex-shrink:0;">Example</span>
      <span style="font-size:.92em;font-style:italic;color:#d8e2ea;">Force Paris, then ask them to think of the first letter of the country it is in.</span> <span style="font-size:.92em;color:#C9A84C;font-weight:600;">&rarr;&nbsp;Paris → France → F</span>
    </div>
  </div>
</div>
</div>

'''


# ── Ch45: Psychological Forces — strength level panel ────────────────────────
PSYFORCE_STRENGTH_PANEL_HTML = '''
<div style="margin:1.8em 0 2em;page-break-inside:avoid;">
  <div style="background:#0d1117;border-radius:6px;border:1px solid rgba(201,168,76,0.25);overflow:hidden;">
    <div style="background:rgba(201,168,76,0.07);padding:0.7em 1.4em;border-bottom:1px solid rgba(201,168,76,0.2);">
      <span style="font-size:.63em;letter-spacing:.18em;color:#C9A84C;text-transform:uppercase;font-weight:700;">Force Strength — Three Levels</span>
    </div>
    <div style="padding:.8em 0 .4em;">
      <div style="padding:.8em 1.4em 1em;border-bottom:1px solid rgba(255,255,255,0.05);">
        <div style="display:flex;align-items:baseline;gap:.8em;margin-bottom:.4em;">
          <span style="font-size:.63em;letter-spacing:.12em;color:#4a7a8a;text-transform:uppercase;font-weight:700;flex-shrink:0;">Level 1</span>
          <span style="font-size:.88em;font-weight:700;color:#c8d4e0;">Soft Influence</span>
        </div>
        <div style="font-size:.8em;color:rgba(180,185,210,.75);margin-bottom:.35em;">Phonetic &nbsp;·&nbsp; Anchoring &nbsp;·&nbsp; Framing</div>
        <div style="font-size:.77em;color:rgba(150,160,180,.6);">Used alone: weak &nbsp;&nbsp;|&nbsp;&nbsp; Used together: powerful</div>
      </div>
      <div style="padding:.8em 1.4em 1em;border-bottom:1px solid rgba(255,255,255,0.05);background:rgba(255,255,255,.015);">
        <div style="display:flex;align-items:baseline;gap:.8em;margin-bottom:.4em;">
          <span style="font-size:.63em;letter-spacing:.12em;color:#7a7a4a;text-transform:uppercase;font-weight:700;flex-shrink:0;">Level 2</span>
          <span style="font-size:.88em;font-weight:700;color:#c8d4e0;">Guided Choice</span>
        </div>
        <div style="font-size:.8em;color:rgba(180,185,210,.75);margin-bottom:.35em;">Exclusion &nbsp;·&nbsp; Contextual &nbsp;·&nbsp; Scene-completion</div>
        <div style="font-size:.77em;color:rgba(150,160,180,.6);">Balanced and practical</div>
      </div>
      <div style="padding:.8em 1.4em 1em;">
        <div style="display:flex;align-items:baseline;gap:.8em;margin-bottom:.4em;">
          <span style="font-size:.63em;letter-spacing:.12em;color:#9a6a30;text-transform:uppercase;font-weight:700;flex-shrink:0;">Level 3</span>
          <span style="font-size:.88em;font-weight:700;color:#c8d4e0;">Hard Bias</span>
        </div>
        <div style="font-size:.8em;color:rgba(180,185,210,.75);margin-bottom:.35em;">Dominant Choice &nbsp;·&nbsp; Statistical &nbsp;·&nbsp; Social-normalcy</div>
        <div style="font-size:.77em;color:rgba(150,160,180,.6);">High hit rate &nbsp;&nbsp;|&nbsp;&nbsp; Higher risk of feeling obvious</div>
      </div>
    </div>
    <div style="padding:.55em 1.4em .7em;border-top:1px solid rgba(201,168,76,0.1);">
      <span style="font-size:.74em;color:#4a5e7a;font-style:italic;">The stronger the force, the more it risks feeling obvious. The weaker the force, the more it needs support.</span>
    </div>
  </div>
</div>
'''

# ── Ch45: Psychological Forces — construction framework panel ─────────────────
PSYFORCE_CONSTRUCT_PANEL_HTML = '''
<div style="margin:1.8em 0 2em;page-break-inside:avoid;">
  <div style="background:#0d1117;border-radius:6px;border:1px solid rgba(201,168,76,0.25);overflow:hidden;">
    <div style="background:rgba(201,168,76,0.07);padding:0.7em 1.4em;border-bottom:1px solid rgba(201,168,76,0.2);">
      <span style="font-size:.63em;letter-spacing:.18em;color:#C9A84C;text-transform:uppercase;font-weight:700;">Five Moving Parts of Every Psychological Force</span>
    </div>
    <div style="padding:.3em 0 .5em;">
      <div style="display:flex;gap:1em;padding:.7em 1.4em;border-bottom:1px solid rgba(255,255,255,0.04);">
        <span style="font-size:.68em;color:#C9A84C;font-weight:700;flex-shrink:0;min-width:1.6em;padding-top:.15em;">01</span>
        <div><div style="font-size:.85em;font-weight:700;color:#e2e8f0;line-height:1.3;">Activation</div><div style="font-size:.76em;color:rgba(180,185,210,.65);margin-top:.2em;line-height:1.4;">What ideas are now mentally on the table?</div></div>
      </div>
      <div style="display:flex;gap:1em;padding:.7em 1.4em;border-bottom:1px solid rgba(255,255,255,0.04);background:rgba(255,255,255,.015);">
        <span style="font-size:.68em;color:#C9A84C;font-weight:700;flex-shrink:0;min-width:1.6em;padding-top:.15em;">02</span>
        <div><div style="font-size:.85em;font-weight:700;color:#e2e8f0;line-height:1.3;">Restriction</div><div style="font-size:.76em;color:rgba(180,185,210,.65);margin-top:.2em;line-height:1.4;">What ideas feel less valid, less likely, or less attractive?</div></div>
      </div>
      <div style="display:flex;gap:1em;padding:.7em 1.4em;border-bottom:1px solid rgba(255,255,255,0.04);">
        <span style="font-size:.68em;color:#C9A84C;font-weight:700;flex-shrink:0;min-width:1.6em;padding-top:.15em;">03</span>
        <div><div style="font-size:.85em;font-weight:700;color:#e2e8f0;line-height:1.3;">Fluency</div><div style="font-size:.76em;color:rgba(180,185,210,.65);margin-top:.2em;line-height:1.4;">Which answer is easiest to access?</div></div>
      </div>
      <div style="display:flex;gap:1em;padding:.7em 1.4em;border-bottom:1px solid rgba(255,255,255,0.04);background:rgba(255,255,255,.015);">
        <span style="font-size:.68em;color:#C9A84C;font-weight:700;flex-shrink:0;min-width:1.6em;padding-top:.15em;">04</span>
        <div><div style="font-size:.85em;font-weight:700;color:#e2e8f0;line-height:1.3;">Commitment</div><div style="font-size:.76em;color:rgba(180,185,210,.65);margin-top:.2em;line-height:1.4;">At what moment do they mentally lock in?</div></div>
      </div>
      <div style="display:flex;gap:1em;padding:.7em 1.4em;">
        <span style="font-size:.68em;color:#C9A84C;font-weight:700;flex-shrink:0;min-width:1.6em;padding-top:.15em;">05</span>
        <div><div style="font-size:.85em;font-weight:700;color:#e2e8f0;line-height:1.3;">Memory</div><div style="font-size:.76em;color:rgba(180,185,210,.65);margin-top:.2em;line-height:1.4;">How will they remember the freedom they had?</div></div>
      </div>
    </div>
    <div style="padding:.55em 1.4em .7em;border-top:1px solid rgba(201,168,76,0.1);">
      <span style="font-size:.72em;color:#4a5e7a;font-style:italic;">A force works when it reduces the search space, increases accessibility, and lets the answer feel self-generated.</span>
    </div>
  </div>
</div>
'''


# ── Ch45: Psychological Forces — category map panel ──────────────────────────
PSYFORCE_MAP_PANEL_HTML = '''
<div style="margin:1.8em 0 2em;page-break-inside:avoid;">
  <div style="background:#0d1117;border-radius:6px;border:1px solid rgba(201,168,76,0.25);overflow:hidden;">
    <div style="background:rgba(201,168,76,0.07);padding:0.7em 1.4em;border-bottom:1px solid rgba(201,168,76,0.2);">
      <span style="font-size:.63em;letter-spacing:.18em;color:#C9A84C;text-transform:uppercase;font-weight:700;">Force Category Reference Map</span>
    </div>
    <div style="padding:.7em 1.4em 1em;">
      <div style="margin-bottom:1.1em;">
        <div style="font-size:.63em;letter-spacing:.12em;color:#4a9d8f;text-transform:uppercase;font-weight:700;margin-bottom:.35em;">Best Raw Reliability</div>
        <div style="font-size:.83em;color:#c8d4e0;">Dominant Choice &nbsp;·&nbsp; Statistical &nbsp;·&nbsp; Social-normalcy</div>
      </div>
      <div style="margin-bottom:1.1em;">
        <div style="font-size:.63em;letter-spacing:.12em;color:#9a7a50;text-transform:uppercase;font-weight:700;margin-bottom:.35em;">Best Theatrical Strength</div>
        <div style="font-size:.83em;color:#c8d4e0;">Scene &nbsp;·&nbsp; Contextual &nbsp;·&nbsp; Sensory</div>
      </div>
      <div style="margin-bottom:1.1em;">
        <div style="font-size:.63em;letter-spacing:.12em;color:#5a6a8a;text-transform:uppercase;font-weight:700;margin-bottom:.35em;">Best Hidden Support</div>
        <div style="font-size:.83em;color:#c8d4e0;">Anchoring &nbsp;·&nbsp; Framing &nbsp;·&nbsp; Timing &nbsp;·&nbsp; Piggyback</div>
      </div>
      <div>
        <div style="font-size:.63em;letter-spacing:.12em;color:#9a5050;text-transform:uppercase;font-weight:700;margin-bottom:.35em;">Most Dangerous If Used Badly</div>
        <div style="font-size:.83em;color:#c8d4e0;">Dominant &nbsp;·&nbsp; Exclusion &nbsp;·&nbsp; Opposites</div>
      </div>
    </div>
  </div>
</div>
'''


# ── Ch7: 10-Second Scan visual ───────────────────────────────────────────────
TEN_SECOND_SCAN_HTML = '''
    '<div style="margin:2em 0;text-align:center;">'
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 680" '
    'style="max-width:100%;height:auto;display:block;margin:0 auto;" '
    'font-family="Georgia, Times New Roman, serif">'
    '<defs><linearGradient id="paf-bg" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0%" stop-color="#0d1117"/>'
    '<stop offset="100%" stop-color="#111820"/>'
    '</linearGradient></defs>'
    '<rect width="700" height="680" fill="url(#paf-bg)" rx="8"/>'
    '<rect width="700" height="680" fill="none" stroke="#C9A84C" stroke-width="1" stroke-opacity=".2" rx="8"/>'
    '<rect x="0" y="0" width="700" height="3" fill="#C9A84C" fill-opacity=".5" rx="2"/>'
    '<text x="350" y="36" text-anchor="middle" font-family="Helvetica Neue,Arial,sans-serif" font-size="9" letter-spacing="3" fill="#C9A84C" fill-opacity=".7" font-weight="600">THE PERFORMANCE ARCHITECTURE FRAMEWORK</text>'
    '<line x1="200" y1="47" x2="500" y2="47" stroke="#C9A84C" stroke-width=".5" stroke-opacity=".3"/>'
    '<text x="350" y="64" text-anchor="middle" font-size="13" fill="#8a9aaa" font-style="italic">Four layers. Each required before the next is accessible.</text>'
    '<rect x="40" y="80" width="620" height="120" rx="5" fill="#fff" fill-opacity=".028" stroke="#C9A84C" stroke-width=".8" stroke-opacity=".35"/>'
    '<rect x="40" y="80" width="4" height="120" fill="#C9A84C" fill-opacity=".7" rx="2"/>'
    '<text x="62" y="103" font-family="Helvetica Neue,Arial,sans-serif" font-size="8.5" letter-spacing="2" fill="#C9A84C" fill-opacity=".6" font-weight="700">LAYER 1</text>'
    '<text x="62" y="122" font-size="15.5" fill="#e8dfc8" letter-spacing=".3">Observation Architecture</text>'
    '<text x="62" y="141" font-size="12" fill="#8a9aaa" font-style="italic">Always active — does not stop when the show begins.</text>'
    '<text x="62" y="159" font-size="12.5" fill="#7a8898">The 80-signal system · Six-Category radar · 10-Second Scan</text>'
    '<text x="62" y="177" font-size="12.5" fill="#7a8898">Read continuously. Your reads at minute twenty should be better than at minute one.</text>'
    '<line x1="350" y1="200" x2="350" y2="218" stroke="#C9A84C" stroke-width="1" stroke-opacity=".35" stroke-dasharray="3,3"/>'
    '<polygon points="345,218 355,218 350,226" fill="#C9A84C" fill-opacity=".35"/>'
    '<rect x="40" y="228" width="620" height="120" rx="5" fill="#fff" fill-opacity=".028" stroke="#4a7a9a" stroke-width=".8" stroke-opacity=".35"/>'
    '<rect x="40" y="228" width="4" height="120" fill="#4a7a9a" fill-opacity=".7" rx="2"/>'
    '<text x="62" y="251" font-family="Helvetica Neue,Arial,sans-serif" font-size="8.5" letter-spacing="2" fill="#4a9aaa" fill-opacity=".7" font-weight="700">LAYER 2</text>'
    '<text x="62" y="270" font-size="15.5" fill="#e8dfc8" letter-spacing=".3">Environmental Architecture</text>'
    '<text x="62" y="289" font-size="12" fill="#8a9aaa" font-style="italic">Set before the audience arrives. Cannot be changed mid-show.</text>'
    '<text x="62" y="308" font-size="12.5" fill="#7a8898">Position · prop placement · sightlines · social cluster map</text>'
    '<text x="62" y="326" font-size="12.5" fill="#7a8898">Who is sitting near whom. Which clusters will influence each other.</text>'
    '<line x1="350" y1="348" x2="350" y2="366" stroke="#C9A84C" stroke-width="1" stroke-opacity=".35" stroke-dasharray="3,3"/>'
    '<polygon points="345,366 355,366 350,374" fill="#C9A84C" fill-opacity=".35"/>'
    '<rect x="40" y="376" width="620" height="120" rx="5" fill="#fff" fill-opacity=".028" stroke="#4a8a6a" stroke-width=".8" stroke-opacity=".35"/>'
    '<rect x="40" y="376" width="4" height="120" fill="#4a9a7a" fill-opacity=".6" rx="2"/>'
    '<text x="62" y="399" font-family="Helvetica Neue,Arial,sans-serif" font-size="8.5" letter-spacing="2" fill="#4a9a7a" fill-opacity=".8" font-weight="700">LAYER 3</text>'
    '<text x="62" y="418" font-size="15.5" fill="#e8dfc8" letter-spacing=".3">Pre-Show Intelligence</text>'
    '<text x="62" y="437" font-size="12" fill="#8a9aaa" font-style="italic">From real-time reading, not research. Formed before the first effect.</text>'
    '<text x="62" y="456" font-size="12.5" fill="#7a8898">Behavioral profiles · social anchor · best volunteer per effect</text>'
    '<text x="62" y="474" font-size="12.5" fill="#7a8898">Room energy state and what it implies about pacing.</text>'
    '<line x1="350" y1="496" x2="350" y2="514" stroke="#C9A84C" stroke-width="1" stroke-opacity=".35" stroke-dasharray="3,3"/>'
    '<polygon points="345,514 355,514 350,522" fill="#C9A84C" fill-opacity=".35"/>'
    '<rect x="40" y="524" width="620" height="100" rx="5" fill="#fff" fill-opacity=".018" stroke="#6a6a7a" stroke-width=".8" stroke-opacity=".3"/>'
    '<rect x="40" y="524" width="4" height="100" fill="#6a6a8a" fill-opacity=".5" rx="2"/>'
    '<text x="62" y="547" font-family="Helvetica Neue,Arial,sans-serif" font-size="8.5" letter-spacing="2" fill="#8a8aaa" fill-opacity=".8" font-weight="700">LAYER 4</text>'
    '<text x="62" y="566" font-size="15.5" fill="#c8c0b0" letter-spacing=".3">Structural Sequence</text>'
    '<text x="62" y="585" font-size="12" fill="#7a8898" font-style="italic">The last layer — and the least important.</text>'
    '<text x="62" y="604" font-size="12.5" fill="#6a7888">Effect order · pacing · callbacks · silence placement</text>'
    '<line x1="60" y1="642" x2="640" y2="642" stroke="#C9A84C" stroke-width=".5" stroke-opacity=".2"/>'
    '<text x="350" y="660" text-anchor="middle" font-size="11.5" fill="#6a7888" font-style="italic">When a show underperforms, the failure almost always lives in layers 1–3.</text>'
    '</svg></div>'
)

<div style="margin:2.5rem 0 2rem;page-break-inside:avoid;">
<svg viewBox="0 0 900 720" xmlns="http://www.w3.org/2000/svg" style="width:100%;display:block;border-radius:4px;overflow:hidden;">
  <defs>
    <linearGradient id="scanBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0d1117"/>
      <stop offset="100%" style="stop-color:#0f1520"/>
    </linearGradient>
  </defs>
  <rect width="900" height="720" fill="url(#scanBg)"/>
  <rect x="0" y="0" width="900" height="44" fill="#0a0e14" opacity="0.6"/>
  <line x1="0" y1="44" x2="900" y2="44" stroke="#C9A84C" stroke-width="0.5" opacity="0.3"/>
  <text x="450" y="22" text-anchor="middle" fill="white" font-size="14" font-family="Georgia,serif" letter-spacing="5" font-weight="bold">THE 10-SECOND SCAN</text>
  <text x="450" y="37" text-anchor="middle" fill="#C9A84C" font-size="9.5" font-family="Georgia,serif" font-style="italic">Ten seconds · Five data points · One read · Run in this order, every time.</text>
  <!-- Row 1 arrows -->
  <polygon points="305,197 298,192 298,202" fill="#2a3548"/>
  <polygon points="601,197 594,192 594,202" fill="#2a3548"/>
  <!-- Row 2 arrow -->
  <polygon points="454,509 447,504 447,514" fill="#2a3548"/>

  <!-- ═══ CARD 1: SHOES — x=10, w=286, y=47, cx=153 ═══ -->
  <rect x="10" y="47" width="286" height="300" fill="#131920" rx="3"/>
  <rect x="10" y="47" width="286" height="6" fill="#C9A84C" rx="2"/>
  <rect x="10" y="47" width="286" height="300" fill="none" stroke="#1c2535" stroke-width="1" rx="3"/>
  <text x="153" y="101" text-anchor="middle" fill="#C9A84C" font-size="34" font-family="Georgia,serif" font-weight="bold" opacity="0.85">01</text>
  <text x="153" y="122" text-anchor="middle" fill="white" font-size="11" font-family="Georgia,serif" letter-spacing="4">SHOES</text>
  <line x1="28" y1="133" x2="278" y2="133" stroke="#222d3e" stroke-width="0.8"/>
  <text x="28" y="150" fill="#4a5e7a" font-size="8" font-family="Georgia,serif" letter-spacing="2.5">NOTICE</text>
  <text x="28" y="167" fill="#8a9ab8" font-size="10.5" font-family="Georgia,serif">Condition · Style</text>
  <text x="28" y="183" fill="#8a9ab8" font-size="10.5" font-family="Georgia,serif">Brand level</text>
  <line x1="28" y1="218" x2="278" y2="218" stroke="#222d3e" stroke-width="0.8"/>
  <text x="28" y="235" fill="#9a8245" font-size="8" font-family="Georgia,serif" letter-spacing="2">TELLS YOU</text>
  <text x="28" y="252" fill="#c0cce0" font-size="10.5" font-family="Georgia,serif">Appearance investment</text>
  <text x="28" y="268" fill="#c0cce0" font-size="10.5" font-family="Georgia,serif">Likely profession</text>
  <text x="28" y="284" fill="#c0cce0" font-size="10.5" font-family="Georgia,serif">Economic background</text>
  <text x="153" y="318" text-anchor="middle" fill="#2e3e52" font-size="9" font-family="Georgia,serif" font-style="italic">Furthest from the face.</text>
  <text x="153" y="332" text-anchor="middle" fill="#2e3e52" font-size="9" font-family="Georgia,serif" font-style="italic">Hardest to manage.</text>

  <!-- ═══ CARD 2: HANDS — x=306, w=286, y=47, cx=449 ═══ -->
  <rect x="306" y="47" width="286" height="300" fill="#131920" rx="3"/>
  <rect x="306" y="47" width="286" height="6" fill="#C9A84C" rx="2"/>
  <rect x="306" y="47" width="286" height="300" fill="none" stroke="#1c2535" stroke-width="1" rx="3"/>
  <text x="449" y="101" text-anchor="middle" fill="#C9A84C" font-size="34" font-family="Georgia,serif" font-weight="bold" opacity="0.85">02</text>
  <text x="449" y="122" text-anchor="middle" fill="white" font-size="11" font-family="Georgia,serif" letter-spacing="4">HANDS</text>
  <line x1="324" y1="133" x2="574" y2="133" stroke="#222d3e" stroke-width="0.8"/>
  <text x="324" y="150" fill="#4a5e7a" font-size="8" font-family="Georgia,serif" letter-spacing="2.5">NOTICE</text>
  <text x="324" y="167" fill="#8a9ab8" font-size="10.5" font-family="Georgia,serif">Calluses · Nails</text>
  <text x="324" y="183" fill="#8a9ab8" font-size="10.5" font-family="Georgia,serif">Rings · Wear patterns</text>
  <line x1="324" y1="218" x2="574" y2="218" stroke="#222d3e" stroke-width="0.8"/>
  <text x="324" y="235" fill="#9a8245" font-size="8" font-family="Georgia,serif" letter-spacing="2">TELLS YOU</text>
  <text x="324" y="252" fill="#c0cce0" font-size="10.5" font-family="Georgia,serif">Occupation signals</text>
  <text x="324" y="268" fill="#c0cce0" font-size="10.5" font-family="Georgia,serif">Stress level</text>
  <text x="324" y="284" fill="#c0cce0" font-size="10.5" font-family="Georgia,serif">Self-care · Relationship</text>
  <text x="449" y="318" text-anchor="middle" fill="#2e3e52" font-size="9" font-family="Georgia,serif" font-style="italic">The story the face</text>
  <text x="449" y="332" text-anchor="middle" fill="#2e3e52" font-size="9" font-family="Georgia,serif" font-style="italic">has learned to conceal.</text>

  <!-- ═══ CARD 3: EYES — x=602, w=286, y=47, cx=745 ═══ -->
  <rect x="602" y="47" width="286" height="300" fill="#131920" rx="3"/>
  <rect x="602" y="47" width="286" height="6" fill="#C9A84C" rx="2"/>
  <rect x="602" y="47" width="286" height="300" fill="none" stroke="#1c2535" stroke-width="1" rx="3"/>
  <text x="745" y="101" text-anchor="middle" fill="#C9A84C" font-size="34" font-family="Georgia,serif" font-weight="bold" opacity="0.85">03</text>
  <text x="745" y="122" text-anchor="middle" fill="white" font-size="11" font-family="Georgia,serif" letter-spacing="4">EYES</text>
  <line x1="620" y1="133" x2="870" y2="133" stroke="#222d3e" stroke-width="0.8"/>
  <text x="620" y="150" fill="#4a5e7a" font-size="8" font-family="Georgia,serif" letter-spacing="2.5">NOTICE</text>
  <text x="620" y="167" fill="#8a9ab8" font-size="10.5" font-family="Georgia,serif">Eye contact willingness</text>
  <text x="620" y="183" fill="#8a9ab8" font-size="10.5" font-family="Georgia,serif">Blink rate · Lid tension</text>
  <text x="620" y="199" fill="#8a9ab8" font-size="10.5" font-family="Georgia,serif">Curious or guarded?</text>
  <line x1="620" y1="218" x2="870" y2="218" stroke="#222d3e" stroke-width="0.8"/>
  <text x="620" y="235" fill="#9a8245" font-size="8" font-family="Georgia,serif" letter-spacing="2">TELLS YOU</text>
  <text x="620" y="252" fill="#c0cce0" font-size="10.5" font-family="Georgia,serif">Confidence level</text>
  <text x="620" y="268" fill="#c0cce0" font-size="10.5" font-family="Georgia,serif">Compliance vs. resistance</text>
  <text x="620" y="284" fill="#c0cce0" font-size="10.5" font-family="Georgia,serif">Supporter or Challenger</text>
  <text x="745" y="318" text-anchor="middle" fill="#2e3e52" font-size="9" font-family="Georgia,serif" font-style="italic">Often visible before</text>
  <text x="745" y="332" text-anchor="middle" fill="#2e3e52" font-size="9" font-family="Georgia,serif" font-style="italic">either speaks.</text>

  <!-- ═══ CARD 4: POSTURE — x=10, w=435, y=359, cx=227 ═══ -->
  <rect x="10" y="359" width="435" height="300" fill="#131920" rx="3"/>
  <rect x="10" y="359" width="435" height="6" fill="#C9A84C" rx="2"/>
  <rect x="10" y="359" width="435" height="300" fill="none" stroke="#1c2535" stroke-width="1" rx="3"/>
  <text x="227" y="413" text-anchor="middle" fill="#C9A84C" font-size="34" font-family="Georgia,serif" font-weight="bold" opacity="0.85">04</text>
  <text x="227" y="434" text-anchor="middle" fill="white" font-size="11" font-family="Georgia,serif" letter-spacing="4">POSTURE</text>
  <line x1="28" y1="445" x2="427" y2="445" stroke="#222d3e" stroke-width="0.8"/>
  <text x="28" y="462" fill="#4a5e7a" font-size="8" font-family="Georgia,serif" letter-spacing="2.5">NOTICE</text>
  <text x="28" y="479" fill="#8a9ab8" font-size="10.5" font-family="Georgia,serif">Lean direction</text>
  <text x="28" y="495" fill="#8a9ab8" font-size="10.5" font-family="Georgia,serif">Shoulders · Weight forward or settled</text>
  <line x1="28" y1="530" x2="427" y2="530" stroke="#222d3e" stroke-width="0.8"/>
  <text x="28" y="547" fill="#9a8245" font-size="8" font-family="Georgia,serif" letter-spacing="2">TELLS YOU</text>
  <text x="28" y="564" fill="#c0cce0" font-size="10.5" font-family="Georgia,serif">Dominance or deference</text>
  <text x="28" y="580" fill="#c0cce0" font-size="10.5" font-family="Georgia,serif">Stress level</text>
  <text x="28" y="596" fill="#c0cce0" font-size="10.5" font-family="Georgia,serif">Overall confidence</text>
  <text x="227" y="632" text-anchor="middle" fill="#2e3e52" font-size="9" font-family="Georgia,serif" font-style="italic">The body&#39;s honest summary of everything.</text>

  <!-- ═══ CARD 5: ENERGY — x=455, w=435, y=359, cx=672 — KEY ═══ -->
  <rect x="455" y="359" width="435" height="300" fill="#161d24" rx="3"/>
  <rect x="455" y="359" width="435" height="6" fill="#C9A84C" rx="2"/>
  <rect x="455" y="359" width="435" height="300" fill="none" stroke="#C9A84C" stroke-width="1" rx="3" opacity="0.35"/>
  <rect x="841" y="349" width="34" height="14" fill="#C9A84C" rx="2"/>
  <text x="858" y="360" text-anchor="middle" fill="#0d1117" font-size="7" font-family="Georgia,serif" letter-spacing="1.5" font-weight="bold">KEY</text>
  <text x="672" y="413" text-anchor="middle" fill="#C9A84C" font-size="34" font-family="Georgia,serif" font-weight="bold">05</text>
  <text x="672" y="434" text-anchor="middle" fill="white" font-size="11" font-family="Georgia,serif" letter-spacing="4">ENERGY</text>
  <line x1="473" y1="445" x2="872" y2="445" stroke="#2a3548" stroke-width="0.8"/>
  <text x="473" y="462" fill="#4a5e7a" font-size="8" font-family="Georgia,serif" letter-spacing="2.5">NOTICE</text>
  <text x="473" y="479" fill="#8a9ab8" font-size="10.5" font-family="Georgia,serif">Expression · Animation</text>
  <text x="473" y="495" fill="#8a9ab8" font-size="10.5" font-family="Georgia,serif">Eye contact with room</text>
  <text x="473" y="511" fill="#8a9ab8" font-size="10.5" font-family="Georgia,serif">Arm height in space</text>
  <line x1="473" y1="530" x2="872" y2="530" stroke="#2a3548" stroke-width="0.8"/>
  <text x="473" y="547" fill="#9a8245" font-size="8" font-family="Georgia,serif" letter-spacing="2">TELLS YOU</text>
  <text x="473" y="564" fill="#c0cce0" font-size="10.5" font-family="Georgia,serif">Reactive potential</text>
  <text x="473" y="580" fill="#c0cce0" font-size="10.5" font-family="Georgia,serif">High arm = openness</text>
  <text x="473" y="596" fill="#c0cce0" font-size="10.5" font-family="Georgia,serif">What impossible looks like</text>
  <text x="672" y="632" text-anchor="middle" fill="#7a6430" font-size="9" font-family="Georgia,serif" font-style="italic">This is the number you came here for.</text>

  <!-- Footer -->
  <line x1="60" y1="674" x2="840" y2="674" stroke="#1a2333" stroke-width="0.8"/>
  <text x="450" y="694" text-anchor="middle" fill="#c0cce0" font-size="11" font-family="Georgia,serif">When you have three signals pointing in the same direction, you have a read.</text>
  <text x="450" y="712" text-anchor="middle" fill="#C9A84C" font-size="11" font-family="Georgia,serif" font-style="italic">Commit before the moment passes.</text>
</svg>
</div>
'''

PERF_ARCH_FRAMEWORK_SVG_HTML = (
    '<div style="margin:2em 0;text-align:center;">'
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 680"'
    ' style="max-width:100%;height:auto;display:block;margin:0 auto;"'
    ' font-family="Georgia, Times New Roman, serif">'
    '<defs><linearGradient id="paf-bg" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0%" stop-color="#0d1117"/>'
    '<stop offset="100%" stop-color="#111820"/>'
    '</linearGradient></defs>'
    '<rect width="700" height="680" fill="url(#paf-bg)" rx="8"/>'
    '<rect width="700" height="680" fill="none" stroke="#C9A84C" stroke-width="1" stroke-opacity=".2" rx="8"/>'
    '<rect x="0" y="0" width="700" height="3" fill="#C9A84C" fill-opacity=".5" rx="2"/>'
    '<text x="350" y="36" text-anchor="middle" font-family="Helvetica Neue,Arial,sans-serif" font-size="9" letter-spacing="3" fill="#C9A84C" fill-opacity=".7" font-weight="600">THE PERFORMANCE ARCHITECTURE FRAMEWORK</text>'
    '<line x1="200" y1="47" x2="500" y2="47" stroke="#C9A84C" stroke-width=".5" stroke-opacity=".3"/>'
    '<text x="350" y="64" text-anchor="middle" font-size="13" fill="#8a9aaa" font-style="italic">Four layers. Each required before the next is accessible.</text>'
    '<rect x="40" y="80" width="620" height="120" rx="5" fill="#fff" fill-opacity=".028" stroke="#C9A84C" stroke-width=".8" stroke-opacity=".35"/>'
    '<rect x="40" y="80" width="4" height="120" fill="#C9A84C" fill-opacity=".7" rx="2"/>'
    '<text x="62" y="103" font-family="Helvetica Neue,Arial,sans-serif" font-size="8.5" letter-spacing="2" fill="#C9A84C" fill-opacity=".6" font-weight="700">LAYER 1</text>'
    '<text x="62" y="122" font-size="15.5" fill="#e8dfc8" letter-spacing=".3">Observation Architecture</text>'
    '<text x="62" y="141" font-size="12" fill="#8a9aaa" font-style="italic">Always active \u2014 does not stop when the show begins.</text>'
    '<text x="62" y="159" font-size="12.5" fill="#7a8898">The 80-signal system \u00b7 Six-Category radar \u00b7 10-Second Scan</text>'
    '<text x="62" y="177" font-size="12.5" fill="#7a8898">Read continuously. Your reads at minute twenty should be better than at minute one.</text>'
    '<line x1="350" y1="200" x2="350" y2="218" stroke="#C9A84C" stroke-width="1" stroke-opacity=".35" stroke-dasharray="3,3"/>'
    '<polygon points="345,218 355,218 350,226" fill="#C9A84C" fill-opacity=".35"/>'
    '<rect x="40" y="228" width="620" height="120" rx="5" fill="#fff" fill-opacity=".028" stroke="#4a7a9a" stroke-width=".8" stroke-opacity=".35"/>'
    '<rect x="40" y="228" width="4" height="120" fill="#4a7a9a" fill-opacity=".7" rx="2"/>'
    '<text x="62" y="251" font-family="Helvetica Neue,Arial,sans-serif" font-size="8.5" letter-spacing="2" fill="#4a9aaa" fill-opacity=".7" font-weight="700">LAYER 2</text>'
    '<text x="62" y="270" font-size="15.5" fill="#e8dfc8" letter-spacing=".3">Environmental Architecture</text>'
    '<text x="62" y="289" font-size="12" fill="#8a9aaa" font-style="italic">Set before the audience arrives. Cannot be changed mid-show.</text>'
    '<text x="62" y="308" font-size="12.5" fill="#7a8898">Position \u00b7 prop placement \u00b7 sightlines \u00b7 social cluster map</text>'
    '<text x="62" y="326" font-size="12.5" fill="#7a8898">Who is sitting near whom. Which clusters will influence each other.</text>'
    '<line x1="350" y1="348" x2="350" y2="366" stroke="#C9A84C" stroke-width="1" stroke-opacity=".35" stroke-dasharray="3,3"/>'
    '<polygon points="345,366 355,366 350,374" fill="#C9A84C" fill-opacity=".35"/>'
    '<rect x="40" y="376" width="620" height="120" rx="5" fill="#fff" fill-opacity=".028" stroke="#4a8a6a" stroke-width=".8" stroke-opacity=".35"/>'
    '<rect x="40" y="376" width="4" height="120" fill="#4a9a7a" fill-opacity=".6" rx="2"/>'
    '<text x="62" y="399" font-family="Helvetica Neue,Arial,sans-serif" font-size="8.5" letter-spacing="2" fill="#4a9a7a" fill-opacity=".8" font-weight="700">LAYER 3</text>'
    '<text x="62" y="418" font-size="15.5" fill="#e8dfc8" letter-spacing=".3">Pre-Show Intelligence</text>'
    '<text x="62" y="437" font-size="12" fill="#8a9aaa" font-style="italic">From real-time reading, not research. Formed before the first effect.</text>'
    '<text x="62" y="456" font-size="12.5" fill="#7a8898">Behavioral profiles \u00b7 social anchor \u00b7 best volunteer per effect</text>'
    '<text x="62" y="474" font-size="12.5" fill="#7a8898">Room energy state and what it implies about pacing.</text>'
    '<line x1="350" y1="496" x2="350" y2="514" stroke="#C9A84C" stroke-width="1" stroke-opacity=".35" stroke-dasharray="3,3"/>'
    '<polygon points="345,514 355,514 350,522" fill="#C9A84C" fill-opacity=".35"/>'
    '<rect x="40" y="524" width="620" height="100" rx="5" fill="#fff" fill-opacity=".018" stroke="#6a6a7a" stroke-width=".8" stroke-opacity=".3"/>'
    '<rect x="40" y="524" width="4" height="100" fill="#6a6a8a" fill-opacity=".5" rx="2"/>'
    '<text x="62" y="547" font-family="Helvetica Neue,Arial,sans-serif" font-size="8.5" letter-spacing="2" fill="#8a8aaa" fill-opacity=".8" font-weight="700">LAYER 4</text>'
    '<text x="62" y="566" font-size="15.5" fill="#c8c0b0" letter-spacing=".3">Structural Sequence</text>'
    '<text x="62" y="585" font-size="12" fill="#7a8898" font-style="italic">The last layer \u2014 and the least important.</text>'
    '<text x="62" y="604" font-size="12.5" fill="#6a7888">Effect order \u00b7 pacing \u00b7 callbacks \u00b7 silence placement</text>'
    '<line x1="60" y1="642" x2="640" y2="642" stroke="#C9A84C" stroke-width=".5" stroke-opacity=".2"/>'
    '<text x="350" y="660" text-anchor="middle" font-size="11.5" fill="#6a7888" font-style="italic">'
    'When a show underperforms, the failure almost always lives in layers 1\u20133.'
    '</text>'
    '</svg></div>'
)


# ── Ch7: Signal Chain Flow (closing bridge to Ch8) ───────────────────────────
CHAIN_FLOW_HTML = '''
<div style="background:#0b1220;border:1px solid rgba(42,157,143,0.2);border-radius:6px;padding:1.8em 2em 1.6em;margin:2em 0;">
  <div style="font-size:0.68em;letter-spacing:0.16em;color:#2a9d8f;text-transform:uppercase;margin-bottom:1.3em;">The Reading Chain</div>
  <div style="display:flex;align-items:stretch;gap:0.5em;">

    <div style="flex:1;background:#141f38;border-top:2px solid #2a9d8f;border-radius:3px;padding:1.1em 1em;text-align:center;">
      <div style="color:#2a9d8f;font-size:0.62em;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:0.5em;">01</div>
      <div style="color:#fff;font-weight:800;font-size:1em;letter-spacing:0.04em;text-transform:uppercase;">Observe</div>
      <div style="color:#6a7c96;font-size:0.78em;line-height:1.5;margin-top:0.5em;">80 signals<br>6 categories<br>10-second scan</div>
    </div>

    <div style="display:flex;align-items:center;padding:0 0.2em;">
      <svg width="24" height="16" viewBox="0 0 24 16"><path d="M0 8 L18 8 M14 3 L20 8 L14 13" stroke="#c9a84c" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </div>

    <div style="flex:1;background:#141f38;border-top:2px solid #c9a84c;border-radius:3px;padding:1.1em 1em;text-align:center;">
      <div style="color:#c9a84c;font-size:0.62em;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:0.5em;">02</div>
      <div style="color:#fff;font-weight:800;font-size:1em;letter-spacing:0.04em;text-transform:uppercase;">Cluster</div>
      <div style="color:#6a7c96;font-size:0.78em;line-height:1.5;margin-top:0.5em;">group by direction<br>weight the chain<br>look for pattern</div>
    </div>

    <div style="display:flex;align-items:center;padding:0 0.2em;">
      <svg width="24" height="16" viewBox="0 0 24 16"><path d="M0 8 L18 8 M14 3 L20 8 L14 13" stroke="#c9a84c" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </div>

    <div style="flex:1;background:#141f38;border-top:2px solid #c9a84c;border-radius:3px;padding:1.1em 1em;text-align:center;">
      <div style="color:#c9a84c;font-size:0.62em;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:0.5em;">03</div>
      <div style="color:#fff;font-weight:800;font-size:1em;letter-spacing:0.04em;text-transform:uppercase;">Adjust</div>
      <div style="color:#6a7c96;font-size:0.78em;line-height:1.5;margin-top:0.5em;">pace &amp; framing<br>selection strategy<br>performance opening</div>
    </div>

  </div>
  <div style="margin-top:1.4em;border-top:1px solid rgba(255,255,255,0.06);padding-top:1em;font-size:0.82em;color:#6a7c96;font-style:italic;">The grouping logic that connects observation to adjustment begins in the next chapter.</div>
</div>
'''


# ── Ch8: Methodology Bridge (Ch7 → Ch8 transition visual) ────────────────────
DISC_OPENING_HTML = '''
<div style="background:#080e1a;border-radius:6px;padding:1.5em 2em;margin:1.6em 0 0.5em;border:1px solid rgba(255,255,255,0.07);">
  <div style="font-size:0.67em;letter-spacing:0.16em;color:#c9a84c;text-transform:uppercase;margin-bottom:1.1em;">Chapter 7 → Chapter 8</div>
  <div style="display:grid;grid-template-columns:1fr 32px 1fr;gap:0;align-items:center;">

    <div style="background:#111b30;border-radius:4px;padding:1em;">
      <div style="font-size:0.65em;letter-spacing:0.12em;color:#2a9d8f;text-transform:uppercase;margin-bottom:0.7em;">Chapter 7 gave you</div>
      <div style="display:flex;flex-direction:column;gap:0.45em;">
        <div style="display:flex;align-items:center;gap:0.6em;">
          <div style="width:6px;height:6px;border-radius:50%;background:#2a9d8f;flex-shrink:0;"></div>
          <div style="color:#c8d4e8;font-size:0.84em;">The 80-Signal inventory</div>
        </div>
        <div style="display:flex;align-items:center;gap:0.6em;">
          <div style="width:6px;height:6px;border-radius:50%;background:#2a9d8f;flex-shrink:0;"></div>
          <div style="color:#c8d4e8;font-size:0.84em;">The Six-Category Radar</div>
        </div>
        <div style="display:flex;align-items:center;gap:0.6em;">
          <div style="width:6px;height:6px;border-radius:50%;background:#2a9d8f;flex-shrink:0;"></div>
          <div style="color:#c8d4e8;font-size:0.84em;">The 10-Second Scan</div>
        </div>
        <div style="display:flex;align-items:center;gap:0.6em;">
          <div style="width:6px;height:6px;border-radius:50%;background:#2a9d8f;flex-shrink:0;"></div>
          <div style="color:#c8d4e8;font-size:0.84em;">Raw observational data</div>
        </div>
      </div>
    </div>

    <div style="display:flex;align-items:center;justify-content:center;">
      <svg width="20" height="40" viewBox="0 0 20 40"><path d="M10 2 L10 32 M4 26 L10 34 L16 26" stroke="#c9a84c" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </div>

    <div style="background:#111b30;border-radius:4px;padding:1em;">
      <div style="font-size:0.65em;letter-spacing:0.12em;color:#c9a84c;text-transform:uppercase;margin-bottom:0.7em;">Chapter 8 gives you</div>
      <div style="display:flex;flex-direction:column;gap:0.45em;">
        <div style="display:flex;align-items:center;gap:0.6em;">
          <div style="width:6px;height:6px;border-radius:50%;background:#c9a84c;flex-shrink:0;"></div>
          <div style="color:#c8d4e8;font-size:0.84em;">The pattern grouping logic</div>
        </div>
        <div style="display:flex;align-items:center;gap:0.6em;">
          <div style="width:6px;height:6px;border-radius:50%;background:#c9a84c;flex-shrink:0;"></div>
          <div style="color:#c8d4e8;font-size:0.84em;">Four communication styles</div>
        </div>
        <div style="display:flex;align-items:center;gap:0.6em;">
          <div style="width:6px;height:6px;border-radius:50%;background:#c9a84c;flex-shrink:0;"></div>
          <div style="color:#c8d4e8;font-size:0.84em;">Performance adjustments per type</div>
        </div>
        <div style="display:flex;align-items:center;gap:0.6em;">
          <div style="width:6px;height:6px;border-radius:50%;background:#c9a84c;flex-shrink:0;"></div>
          <div style="color:#c8d4e8;font-size:0.84em;">Volunteer strategy by style</div>
        </div>
      </div>
    </div>

  </div>
  <div style="margin-top:1.1em;text-align:center;font-size:0.8em;color:#4a5c78;letter-spacing:0.04em;font-style:italic;">Same signals. The first true level of organization.</div>
</div>
'''


# ── Ch8: DISC Signal Clusters + Rule Callout ─────────────────────────────────
DISC_CLUSTER_HTML = '''
<div style="margin:2em 0;">

  <!-- Rule callout: ONE SIGNAL IS NOT A TYPE -->
  <div style="background:#0d1422;border-left:5px solid #c9a84c;border-radius:2px;padding:1.2em 1.6em;margin-bottom:1.4em;position:relative;">
    <div style="font-size:0.65em;letter-spacing:0.18em;color:#c9a84c;text-transform:uppercase;margin-bottom:0.45em;">Field Rule</div>
    <div style="color:#fff;font-weight:800;font-size:1em;letter-spacing:0.05em;text-transform:uppercase;margin-bottom:0.4em;">One signal is not a type.</div>
    <div style="color:#c8d4e8;font-size:0.86em;line-height:1.65;">DISC comes from clusters, not cues. Look for one strong signal and two supporting signals, or three moderate signals pointing in the same direction. The read is the chain &mdash; not the single tell. Use one strong signal plus two supporting signals, or three moderate signals all moving in the same direction. When you are not sure, wait for a third data point before committing to an adjustment.</div>
  </div>

  <!-- Cluster label -->
  <div style="font-size:0.68em;letter-spacing:0.14em;color:#8a9ab5;text-transform:uppercase;margin-bottom:0.9em;">Signal Clusters by Type &mdash; Which Signals From Chapter 7 Point Where</div>

  <!-- 2x2 grid of cluster boxes -->
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.9em;">

    <!-- D: Direct -->
    <div style="background:#120d1a;border-left:4px solid #A83030;border-radius:3px;padding:1.1em 1.2em;">
      <div style="display:flex;align-items:center;gap:0.7em;margin-bottom:0.9em;">
        <div style="background:#A83030;color:#fff;font-weight:800;font-size:1em;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;">D</div>
        <div>
          <div style="color:#fff;font-weight:700;font-size:0.9em;">Direct</div>
          <div style="color:#A83030;font-size:0.74em;">Fast &middot; Decisive &middot; Results-focused</div>
        </div>
      </div>
      <div style="font-size:0.72em;letter-spacing:0.1em;color:#8a9ab5;text-transform:uppercase;margin-bottom:0.45em;">Look first for</div>
      <div style="color:#c8d4e8;font-size:0.82em;line-height:1.7;margin-bottom:0.8em;">#43 walking speed &middot; #46 weight at rest &middot; #57 handshake pressure &middot; #67 interruption rate &middot; #71 contradiction reaction &middot; #80 silence reclaim speed</div>
      <div style="font-size:0.72em;letter-spacing:0.1em;color:#8a9ab5;text-transform:uppercase;margin-bottom:0.35em;">Also watch</div>
      <div style="color:#7a8a9c;font-size:0.8em;line-height:1.6;margin-bottom:0.8em;">#04 thumbs out &middot; #08 eye contact &middot; #58 sitting speed &middot; #60 chair choice</div>
      <div style="background:#1a1020;border-radius:2px;padding:0.6em 0.8em;">
        <div style="color:#A83030;font-size:0.74em;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;">Adjustment</div>
        <div style="color:#c8d4e8;font-size:0.8em;margin-top:0.2em;">Skip warm-up. Lead with precision. Precision is currency.</div>
      </div>
    </div>

    <!-- I: Influential -->
    <div style="background:#161208;border-left:4px solid #C9A84C;border-radius:3px;padding:1.1em 1.2em;">
      <div style="display:flex;align-items:center;gap:0.7em;margin-bottom:0.9em;">
        <div style="background:#C9A84C;color:#0e1628;font-weight:800;font-size:1em;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;">I</div>
        <div>
          <div style="color:#fff;font-weight:700;font-size:0.9em;">Influential</div>
          <div style="color:#C9A84C;font-size:0.74em;">Expressive &middot; Social &middot; Enthusiastic</div>
        </div>
      </div>
      <div style="font-size:0.72em;letter-spacing:0.1em;color:#8a9ab5;text-transform:uppercase;margin-bottom:0.45em;">Look first for</div>
      <div style="color:#c8d4e8;font-size:0.82em;line-height:1.7;margin-bottom:0.8em;">#08 eye contact &middot; #45 head tilt &middot; #50 humor timing &middot; #56 eyebrow expressiveness &middot; #64 mirroring &middot; #72 smile duration &middot; #73 laughter delay</div>
      <div style="font-size:0.72em;letter-spacing:0.1em;color:#8a9ab5;text-transform:uppercase;margin-bottom:0.35em;">Also watch</div>
      <div style="color:#7a8a9c;font-size:0.8em;line-height:1.6;margin-bottom:0.8em;">#43 walking speed &middot; #48 micro-grooming &middot; #52 conversational distance &middot; #55 ear redness</div>
      <div style="background:#161208;border-radius:2px;padding:0.6em 0.8em;border:1px solid rgba(201,168,76,0.15);">
        <div style="color:#C9A84C;font-size:0.74em;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;">Adjustment</div>
        <div style="color:#c8d4e8;font-size:0.8em;margin-top:0.2em;">Give them a visible role. Their reaction is the effect.</div>
      </div>
    </div>

    <!-- S: Steady -->
    <div style="background:#091418;border-left:4px solid #1A8FA8;border-radius:3px;padding:1.1em 1.2em;">
      <div style="display:flex;align-items:center;gap:0.7em;margin-bottom:0.9em;">
        <div style="background:#1A8FA8;color:#fff;font-weight:800;font-size:1em;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;">S</div>
        <div>
          <div style="color:#fff;font-weight:700;font-size:0.9em;">Steady</div>
          <div style="color:#1A8FA8;font-size:0.74em;">Calm &middot; Cooperative &middot; Supportive</div>
        </div>
      </div>
      <div style="font-size:0.72em;letter-spacing:0.1em;color:#8a9ab5;text-transform:uppercase;margin-bottom:0.45em;">Look first for</div>
      <div style="color:#c8d4e8;font-size:0.82em;line-height:1.7;margin-bottom:0.8em;">#14 fidgeting level &middot; #45 head tilt &middot; #49 breathing depth &middot; #52 conversational distance &middot; #66 agreement speed &middot; #74 permission-seeking &middot; #75 public mistake recovery</div>
      <div style="font-size:0.72em;letter-spacing:0.1em;color:#8a9ab5;text-transform:uppercase;margin-bottom:0.35em;">Also watch</div>
      <div style="color:#7a8a9c;font-size:0.8em;line-height:1.6;margin-bottom:0.8em;">#21 eye contact break &middot; #44 shoulder tension &middot; #46 weight distribution &middot; #61 coat placement</div>
      <div style="background:#091418;border-radius:2px;padding:0.6em 0.8em;border:1px solid rgba(26,143,168,0.15);">
        <div style="color:#1A8FA8;font-size:0.74em;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;">Adjustment</div>
        <div style="color:#c8d4e8;font-size:0.8em;margin-top:0.2em;">Slow the pace. Warm framing. Patience is the asset.</div>
      </div>
    </div>

    <!-- C: Conscientious -->
    <div style="background:#0f0d1a;border-left:4px solid #6B52A0;border-radius:3px;padding:1.1em 1.2em;">
      <div style="display:flex;align-items:center;gap:0.7em;margin-bottom:0.9em;">
        <div style="background:#6B52A0;color:#fff;font-weight:800;font-size:1em;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;">C</div>
        <div>
          <div style="color:#fff;font-weight:700;font-size:0.9em;">Conscientious</div>
          <div style="color:#6B52A0;font-size:0.74em;">Analytical &middot; Precise &middot; Detail-oriented</div>
        </div>
      </div>
      <div style="font-size:0.72em;letter-spacing:0.1em;color:#8a9ab5;text-transform:uppercase;margin-bottom:0.45em;">Look first for</div>
      <div style="color:#c8d4e8;font-size:0.82em;line-height:1.7;margin-bottom:0.8em;">#35 privacy screen &middot; #42 notification speed &middot; #53 face-touching during thought &middot; #59 object-moving before sitting &middot; #65 response lag &middot; #76 unprompted explanations &middot; #79 object alignment</div>
      <div style="font-size:0.72em;letter-spacing:0.1em;color:#8a9ab5;text-transform:uppercase;margin-bottom:0.35em;">Also watch</div>
      <div style="color:#7a8a9c;font-size:0.8em;line-height:1.6;margin-bottom:0.8em;">#12 shoelace condition &middot; #22 object handling &middot; #41 phone grip &middot; #60 chair choice &middot; #62 drink placement</div>
      <div style="background:#0f0d1a;border-radius:2px;padding:0.6em 0.8em;border:1px solid rgba(107,82,160,0.15);">
        <div style="color:#6B52A0;font-size:0.74em;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;">Adjustment</div>
        <div style="color:#c8d4e8;font-size:0.8em;margin-top:0.2em;">Build coherence first. Logic must precede compliance.</div>
      </div>
    </div>

  </div>

  <!-- Footer note -->
  <div style="margin-top:0.9em;padding:0.8em 1em;background:#080e1a;border-radius:4px;font-size:0.78em;color:#4a5c78;line-height:1.6;">
    <strong style="color:#6a7a90;">These are patterns, not proof.</strong> Signals <em>suggest</em> &mdash; they do not confirm. Use as a probability filter for performance adjustment, not as a diagnosis. One strong signal plus two supporting signals. Three moderate signals pointing the same direction. That is a read. That is also the minimum standard before you adjust your approach.
  </div>

</div>
'''


# ── Novelty Techniques ───────────────────────────────────────────────────────
NOVELTY_TECHNIQUES_HTML = '''
<div style="background:linear-gradient(160deg,#090e1a 0%,#0e1628 55%,#111e35 100%);border-radius:8px;padding:2em 2em 1.5em;margin:2em 0;position:relative;overflow:hidden;">
  <!-- Broken grid / interruption waveform overlay -->
  <svg style="position:absolute;top:0;left:0;width:100%;height:100%;opacity:0.06;pointer-events:none;" viewBox="0 0 700 420" preserveAspectRatio="xMidYMid slice">
    <line x1="-40" y1="80" x2="280" y2="400" stroke="#2a9d8f" stroke-width="1.2"/>
    <line x1="120" y1="-10" x2="480" y2="350" stroke="#2a9d8f" stroke-width="0.6"/>
    <line x1="400" y1="-20" x2="760" y2="340" stroke="#c9a84c" stroke-width="0.6"/>
    <!-- Interruption: waveform that breaks in the middle -->
    <path d="M0,230 Q80,215 160,230 Q200,238 230,228" stroke="#2a9d8f" stroke-width="1.2" fill="none" stroke-dasharray="3 7"/>
    <circle cx="240" cy="226" r="2.5" fill="#2a9d8f"/>
    <path d="M252,224 Q330,210 420,228 Q480,238 560,220 Q620,210 700,218" stroke="#2a9d8f" stroke-width="1.2" fill="none"/>
    <!-- Horizontal grid fragments -->
    <line x1="0" y1="140" x2="90" y2="140" stroke="#c9a84c" stroke-width="0.4" stroke-dasharray="2 5"/>
    <line x1="580" y1="300" x2="700" y2="300" stroke="#2a9d8f" stroke-width="0.4" stroke-dasharray="2 5"/>
  </svg>

  <!-- Section label + title -->
  <div style="font-size:0.7em;letter-spacing:0.14em;color:#2a9d8f;text-transform:uppercase;margin-bottom:0.3em;position:relative;">Novelty is Designed &mdash; Not Accidental</div>
  <h3 style="color:#fff;font-size:1.25em;margin:0 0 1.3em;font-weight:700;letter-spacing:0.02em;position:relative;">How to Create the Feeling of Novelty</h3>

  <!-- HERO CARD: Violate the Format -->
  <div style="background:#1a2540;border-radius:2px;padding:1.3em 1.5em 1.3em 2em;margin-bottom:1.1em;position:relative;">
    <!-- Glow bar -->
    <div style="position:absolute;top:0;left:0;width:5px;height:100%;background:#2a9d8f;border-radius:2px 0 0 2px;box-shadow:0 0 14px rgba(42,157,143,0.7);"></div>
    <div style="font-size:0.64em;letter-spacing:0.18em;color:#2a9d8f;text-transform:uppercase;margin-bottom:0.5em;">Entry Point</div>
    <div style="color:#fff;font-weight:800;font-size:1.05em;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:0.55em;">Violate the Format</div>
    <div style="color:#c8d4e8;font-size:0.9em;line-height:1.65;">Start in silence. Open with the unexpected. The pattern interrupt activates dopaminergic attention before a word is spoken. Every format creates a prediction. Breaking it at the moment of maximum confidence is where the effect begins.</div>
  </div>

  <!-- 2-col staggered grid -->
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.9em;position:relative;">

    <!-- LEFT COLUMN -->
    <div style="display:flex;flex-direction:column;gap:0.9em;">
      <!-- Name the Unnamed: sharp corners, heavy gold accent -->
      <div style="background:#141f38;border-left:5px solid #c9a84c;border-radius:1px;padding:1em 1em 1em 1.1em;margin-top:0.5em;">
        <div style="color:#c9a84c;font-weight:700;font-size:0.82em;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.45em;">Name the Unnamed</div>
        <div style="color:#c8d4e8;font-size:0.86em;line-height:1.55;">Give language to a feeling they&rsquo;ve had but never named. &ldquo;I&rsquo;ve always felt this&rdquo; turns you into a mirror they didn&rsquo;t know existed.</div>
      </div>
      <!-- Unexplained Specificity: glow inset, no hard border -->
      <div style="background:#1a2540;border-radius:4px;padding:1em;box-shadow:inset 0 0 0 1px rgba(42,157,143,0.28);">
        <div style="color:#c9a84c;font-weight:700;font-size:0.82em;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.45em;">Unexplained Specificity</div>
        <div style="color:#c8d4e8;font-size:0.86em;line-height:1.55;">&ldquo;Companies in your range hit a bottleneck around month 8.&rdquo; The specific number with no explanation opens a curiosity loop the brain cannot close.</div>
      </div>
    </div>

    <!-- RIGHT COLUMN -->
    <div style="display:flex;flex-direction:column;gap:0.9em;">
      <!-- Deliberate Withhold: teal accent, standard -->
      <div style="background:#1a2540;border-left:4px solid #2a9d8f;border-radius:4px;padding:1em;">
        <div style="color:#c9a84c;font-weight:700;font-size:0.82em;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.45em;">The Deliberate Withhold</div>
        <div style="color:#c8d4e8;font-size:0.86em;line-height:1.55;">&ldquo;There&rsquo;s one thing that changes everything. I want to come back to it.&rdquo; Anticipation is its own novelty state.</div>
      </div>
      <!-- Reframe the Familiar: gold accent, uniform with Name the Unnamed -->
      <div style="background:#141f38;border-left:5px solid #c9a84c;border-radius:1px;padding:1em 1em 1em 1.1em;">
        <div style="color:#c9a84c;font-weight:700;font-size:0.82em;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.45em;">Reframe the Familiar</div>
        <div style="color:#c8d4e8;font-size:0.86em;line-height:1.55;">&ldquo;That&rsquo;s not a pricing objection. That&rsquo;s a trust deficit.&rdquo; Reframes feel like discoveries because they are.</div>
      </div>
      <!-- Physical Novelty Anchors: teal accent, uniform with Deliberate Withhold -->
      <div style="background:#1a2540;border-left:4px solid #2a9d8f;border-radius:4px;padding:1em;">
        <div style="color:#c9a84c;font-weight:700;font-size:0.82em;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.45em;">Physical Novelty Anchors</div>
        <div style="color:#c8d4e8;font-size:0.86em;line-height:1.55;">An unusual prop, a distinct handout format. Memory encodes around novelty. What stands out during the pitch is recalled during the decision.</div>
      </div>
    </div>

  </div>
</div>
'''

# ── Speech Patterns ──────────────────────────────────────────────────────────
SPEECH_PATTERNS_HTML = '''
<div style="background:#0e1628;border-radius:8px;padding:2em 2em 1.5em;margin:2em 0;">
  <div style="font-size:0.72em;letter-spacing:0.12em;color:#c9a84c;text-transform:uppercase;margin-bottom:0.3em;">Neuroscience // Processing Fluency (Reber &amp; Schwarz)</div>
  <h3 style="color:#fff;font-size:1.3em;margin:0 0 1.2em;font-weight:700;">5 Speech Patterns That Build Instant Authority</h3>
  <div style="display:flex;flex-direction:column;gap:0.6em;">
    <div style="display:flex;align-items:flex-start;gap:1em;background:#1a2540;border-radius:4px;padding:0.9em 1em;">
      <div style="background:#c9a84c;color:#0e1628;font-weight:800;font-size:0.85em;padding:0.3em 0.6em;border-radius:3px;min-width:2.2em;text-align:center;flex-shrink:0;">01</div>
      <div style="flex:1;">
        <div style="color:#fff;font-weight:700;font-size:0.95em;">Slow the Beginning <span style="color:#c9a84c;font-size:0.8em;font-weight:400;margin-left:0.5em;">Processing Fluency</span></div>
        <div style="color:#c8d4e8;font-size:0.88em;margin-top:0.3em;">Slower opening + clear statement = authority rises. &ldquo;Let me show you something interesting&hellip;&rdquo;</div>
      </div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:1em;background:#1a2540;border-radius:4px;padding:0.9em 1em;">
      <div style="background:#c9a84c;color:#0e1628;font-weight:800;font-size:0.85em;padding:0.3em 0.6em;border-radius:3px;min-width:2.2em;text-align:center;flex-shrink:0;">02</div>
      <div style="flex:1;">
        <div style="color:#fff;font-weight:700;font-size:0.95em;">The Spontaneous Compliment <span style="color:#c9a84c;font-size:0.8em;font-weight:400;margin-left:0.5em;">Social Trust Circuits</span></div>
        <div style="color:#c8d4e8;font-size:0.88em;margin-top:0.3em;">&ldquo;&mdash;Oh, that&rsquo;s a good question.&rdquo; The exclamation makes praise feel unplanned and genuine.</div>
      </div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:1em;background:#1a2540;border-radius:4px;padding:0.9em 1em;">
      <div style="background:#c9a84c;color:#0e1628;font-weight:800;font-size:0.85em;padding:0.3em 0.6em;border-radius:3px;min-width:2.2em;text-align:center;flex-shrink:0;">03</div>
      <div style="flex:1;">
        <div style="color:#fff;font-weight:700;font-size:0.95em;">Future Memory Language <span style="color:#c9a84c;font-size:0.8em;font-weight:400;margin-left:0.5em;">Neural Simulation</span></div>
        <div style="color:#c8d4e8;font-size:0.88em;margin-top:0.3em;">&ldquo;Imagine it&rsquo;s next quarter&hellip;&rdquo; The brain simulates futures using the same circuits as memory.</div>
      </div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:1em;background:#1a2540;border-radius:4px;padding:0.9em 1em;">
      <div style="background:#c9a84c;color:#0e1628;font-weight:800;font-size:0.85em;padding:0.3em 0.6em;border-radius:3px;min-width:2.2em;text-align:center;flex-shrink:0;">04</div>
      <div style="flex:1;">
        <div style="color:#fff;font-weight:700;font-size:0.95em;">The Status Frame <span style="color:#c9a84c;font-size:0.8em;font-weight:400;margin-left:0.5em;">Decision-Maker Positioning</span></div>
        <div style="color:#c8d4e8;font-size:0.88em;margin-top:0.3em;">&ldquo;I&rsquo;m curious which direction you&rsquo;re leaning.&rdquo; The other person becomes the expert, not the target.</div>
      </div>
    </div>
    <div style="display:flex;align-items:flex-start;gap:1em;background:#1a2540;border-radius:4px;padding:0.9em 1em;">
      <div style="background:#c9a84c;color:#0e1628;font-weight:800;font-size:0.85em;padding:0.3em 0.6em;border-radius:3px;min-width:2.2em;text-align:center;flex-shrink:0;">05</div>
      <div style="flex:1;">
        <div style="color:#fff;font-weight:700;font-size:0.95em;">Strategic Silence <span style="color:#c9a84c;font-size:0.8em;font-weight:400;margin-left:0.5em;">FBI Negotiation Tactic</span></div>
        <div style="color:#c8d4e8;font-size:0.88em;margin-top:0.3em;">After a proposal &mdash; stop talking. Whoever speaks first gives ground. Silence signals certainty.</div>
      </div>
    </div>
  </div>
</div>
'''

# ── Tension Signals SVG ──────────────────────────────────────────────────────
TENSION_SIGNALS_HTML = '''
<div style="background:#0e1628;border-radius:8px;padding:1.8em 2em 1.5em;margin:2em 0;">
  <div style="font-size:0.72em;letter-spacing:0.12em;color:#c9a84c;text-transform:uppercase;margin-bottom:0.3em;">T2 &middot; Audience Management</div>
  <h3 style="color:#fff;font-size:1.2em;margin:0 0 1.1em;font-weight:700;">Six Cortisol Signals — Reading the Room in Real Time</h3>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.8em;">
    <div style="background:#1a2540;border-left:4px solid #c9a84c;border-radius:4px;padding:0.9em 1em;">
      <div style="color:#c9a84c;font-weight:700;font-size:0.9em;margin-bottom:0.4em;">Breathing Visibility</div>
      <div style="color:#c8d4e8;font-size:0.84em;line-height:1.5;">Slow breathing + still shoulders = inside the window. Shallow, rapid breathing + rising shoulder pads = window exceeded. Watch the first two rows. They read out the whole room.</div>
    </div>
    <div style="background:#1a2540;border-left:4px solid #c9a84c;border-radius:4px;padding:0.9em 1em;">
      <div style="color:#c9a84c;font-weight:700;font-size:0.9em;margin-bottom:0.4em;">The Laughter Signal</div>
      <div style="color:#c8d4e8;font-size:0.84em;line-height:1.5;">Laughter at a non-funny moment is cortisol discharge. The window is at its edge. Offer a brief social release, then resume the build. Because these are less common, take them more seriously when they appear.</div>
    </div>
    <div style="background:#1a2540;border-left:4px solid #c9a84c;border-radius:4px;padding:0.9em 1em;">
      <div style="color:#c9a84c;font-weight:700;font-size:0.9em;margin-bottom:0.4em;">Stillness Gradient</div>
      <div style="color:#c8d4e8;font-size:0.84em;line-height:1.5;">Inside the window: progressive stillness (held breath, leaning in). Window exceeded: shifting, recrossing legs, pulling at clothing, beginning to lean back.</div>
    </div>
    <div style="background:#1a2540;border-left:4px solid #c9a84c;border-radius:4px;padding:0.9em 1em;">
      <div style="color:#c9a84c;font-weight:700;font-size:0.9em;margin-bottom:0.4em;">Phone Emergence</div>
      <div style="color:#c8d4e8;font-size:0.84em;line-height:1.5;">A phone in a tense moment is a nervous system looking for an exit. Tension was not earned or has been held too long. (Some people are just realtors.)</div>
    </div>
    <div style="background:#1a2540;border-left:4px solid #c9a84c;border-radius:4px;padding:0.9em 1em;">
      <div style="color:#c9a84c;font-weight:700;font-size:0.9em;margin-bottom:0.4em;">Self-Soothing</div>
      <div style="color:#c8d4e8;font-size:0.84em;line-height:1.5;">Self-touch to neck, face, hair, and arms rises with cortisol. A wave of soothing behaviors moving across a section at the same time is a specific, high-confidence signal.</div>
    </div>
    <div style="background:#1a2540;border-left:4px solid #c9a84c;border-radius:4px;padding:0.9em 1em;">
      <div style="color:#c9a84c;font-weight:700;font-size:0.9em;margin-bottom:0.4em;">Absence of Response</div>
      <div style="color:#c8d4e8;font-size:0.84em;line-height:1.5;">Flat room where energy should have risen. Dopamine response interrupted. Volunteer selection shifts from playful hesitation to social reluctance. The room is not with you. It is protecting itself from you.</div>
    </div>
  </div>
</div>
'''

# ═══════════════════════════════════════════════════════════
# TYPOGRAPHIC UTILITIES
# ═══════════════════════════════════════════════════════════

def smart_quotes(text):
    """Convert straight quotes to typographic curly quotes and em dashes."""
    # Em dashes
    text = text.replace(' -- ', '\u2009\u2014\u2009')
    text = text.replace('--', '\u2014')
    # Double quotes - use lambda to avoid regex escape issues
    text = re.sub(r'"(\w)', lambda m: '\u201c' + m.group(1), text)  # opening
    text = re.sub(r'(\w)"', lambda m: m.group(1) + '\u201d', text)  # closing
    text = text.replace('"', '\u201d')  # remaining (likely closing)
    # Single quotes / apostrophes
    text = re.sub(r"'(\w)", lambda m: '\u2019' + m.group(1), text)  # apostrophe
    text = re.sub(r"(\w)'", lambda m: m.group(1) + '\u2019', text)  # apostrophe
    text = re.sub(r"\s'", lambda m: ' \u2018', text)  # opening single
    # Ellipsis
    text = text.replace('...', '\u2026')
    return text


def escape(text):
    """HTML escape then apply smart typography."""
    if not text:
        return ''
    t = html_module.escape(text)
    t = smart_quotes(t)
    return t


def is_section_header(text):
    """Detect if a line is a section header (Title Case or ALL CAPS, short)."""
    stripped = text.strip()
    if not stripped or len(stripped) > 120 or len(stripped) < 4:
        return False
    # Skip lines that look like regular sentences
    if stripped.endswith('.') and len(stripped) > 60:
        return False
    # ALL CAPS headers
    if stripped.isupper() and not stripped.startswith('CHAPTER') and not stripped.startswith('PART'):
        return True
    # Title Case headers (short, no period at end, most words capitalized)
    words = stripped.rstrip(':').split()
    if len(words) > 12:
        return False
    if stripped.endswith('.'):
        return False
    # Count capitalized words (excluding small conjunctions); digits count as title tokens
    # Strip em-dash separators — they're punctuation, not title words
    small_words = {'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'vs.', 'vs', 'is', 'not'}
    words = [w for w in words if w not in ('—', '–', '-')]
    if not words:
        return False
    cap_count = sum(1 for w in words if w[0].isupper() or w[0].isdigit() or w.lower() in small_words)
    if cap_count >= len(words) * 0.7 and len(words) >= 2 and len(stripped) < 65:
        # Additional check: shouldn't start with common sentence patterns
        if not stripped.startswith(('There ', 'This ', 'That ', 'It ', 'You ', 'We ', 'I ', 'If ', 'When ', 'Most ', 'Some ', 'The audience', 'The brain', 'The key', 'Consider ', 'Notice ', 'Make ', 'Seconds ')):
            return True
    return False


def is_section_break(text):
    """Detect section break markers."""
    stripped = text.strip()
    return stripped in ('· · ·', '···', '• • •', '* * *', '---', '***', '- - -', '\u2022 \u2022 \u2022')


def is_what_you_have_felt(text):
    """Detect the recurring chapter motif."""
    stripped = text.strip()
    return stripped.lower().startswith('what you have felt before') or stripped == 'What You Have Felt Before'


# ═══════════════════════════════════════════════════════════
# PARSER
# ═══════════════════════════════════════════════════════════

def parse_manuscript(filepath):
    """Parse the manuscript into structured sections."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    lines = text.split('\n')
    sections = []
    current_section = None
    current_part = 0

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Detect PART headers (standalone line)
        part_match = re.match(r'^PART\s+(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT)\s*$', line)
        if part_match and i > 55:  # Skip TOC
            part_names = {'ONE':1,'TWO':2,'THREE':3,'FOUR':4,'FIVE':5,'SIX':6,'SEVEN':7,'EIGHT':8}
            current_part = part_names.get(part_match.group(1), current_part)
            subtitle = ''
            if i+1 < len(lines) and lines[i+1].strip():
                subtitle = lines[i+1].strip()
            if current_section:
                sections.append(current_section)
            current_section = {
                'type': 'part',
                'part_num': current_part,
                'title': f'PART {part_match.group(1)}',
                'subtitle': subtitle,
                'content': [],
                'chapter_key': f'PART {part_match.group(1)}'
            }
            i += 2
            continue

        # Detect REFERENCE SECTION header (back matter)
        if line == 'REFERENCE SECTION' and i > 2000:
            subtitle = ''
            if i+1 < len(lines) and lines[i+1].strip():
                subtitle = lines[i+1].strip()
            if current_section:
                sections.append(current_section)
            current_part = 8
            current_section = {
                'type': 'part',
                'part_num': 8,
                'title': 'REFERENCE SECTION',
                'subtitle': subtitle,
                'content': [],
                'chapter_key': 'REFERENCE SECTION'
            }
            i += 2
            continue

        # Detect CHAPTER headers
        chapter_match = re.match(r'^CHAPTER\s+(\d+)\s*$', line)
        if chapter_match and i > 55:
            chapter_num = int(chapter_match.group(1))
            title = ''
            if i+1 < len(lines) and lines[i+1].strip():
                title = lines[i+1].strip()
            if current_section:
                sections.append(current_section)
            current_section = {
                'type': 'chapter',
                'chapter_num': chapter_num,
                'part_num': current_part,
                'title': title,
                'content': [],
                'chapter_key': f'CHAPTER {chapter_num}'
            }
            i += 2
            if i < len(lines) and '\u2500' in lines[i]:
                i += 1
            continue

        # Detect INTRODUCTION (after TOC)
        if line == 'INTRODUCTION' and i > 106:
            subtitle = ''
            if i+1 < len(lines) and lines[i+1].strip():
                subtitle = lines[i+1].strip()
            if current_section:
                sections.append(current_section)
            current_section = {
                'type': 'chapter',
                'chapter_num': 0,
                'part_num': 0,
                'title': subtitle,
                'content': [],
                'chapter_key': 'INTRODUCTION'
            }
            i += 2
            continue

        # Detect HOW TO READ THIS BOOK (front matter, after Introduction)
        if line == 'HOW TO READ THIS BOOK' and i > 106:
            if current_section:
                sections.append(current_section)
            current_section = {
                'type': 'how_to_read',
                'chapter_num': -1,
                'part_num': 0,
                'title': 'How to Read This Book',
                'content': [],
                'chapter_key': 'HOW TO READ'
            }
            i += 1
            continue

        # Detect ACKNOWLEDGMENTS (early in file)
        if line == 'ACKNOWLEDGMENTS' and i < 50:
            if current_section:
                sections.append(current_section)
            current_section = {
                'type': 'front_matter',
                'chapter_num': -2,
                'part_num': 0,
                'title': 'Acknowledgments',
                'content': [],
                'chapter_key': 'ACKNOWLEDGMENTS'
            }
            i += 1
            continue

        # Detect GLOSSARY
        if line.startswith('GLOSSARY') and i > 2000:
            if current_section:
                sections.append(current_section)
            current_section = {
                'type': 'glossary',
                'chapter_num': 99,
                'part_num': 9,
                'title': 'Glossary',
                'content': [],
                'chapter_key': 'GLOSSARY'
            }
            i += 1
            continue

        # Detect THE META REVEAL (handled separately via META_REVEAL_HTML; skip manuscript content)
        if line == 'THE META REVEAL' and i > 2000:
            if current_section:
                sections.append(current_section)
            current_section = {
                'type': 'meta_reveal',
                'chapter_num': 98,
                'part_num': 9,
                'title': 'The Meta Reveal',
                'content': [],
                'chapter_key': 'META_REVEAL'
            }
            i += 1
            continue

        # Detect ABOUT THE AUTHOR
        if line == 'ABOUT THE AUTHOR' and i > 2000:
            if current_section:
                sections.append(current_section)
            current_section = {
                'type': 'about',
                'chapter_num': 100,
                'part_num': 9,
                'title': 'About the Author',
                'content': [],
                'chapter_key': 'ABOUT'
            }
            i += 1
            continue

        # Skip early front matter before ACKNOWLEDGMENTS
        if i < 34 and current_section is None:
            i += 1
            continue

        # Skip TOC block
        if i >= 57 and i <= 107 and current_section is None:
            i += 1
            continue

        # Skip separator lines
        if '\u2500' in line:
            i += 1
            continue

        # Add content
        if current_section is not None:
            if line.startswith('TABLE OF CONTENTS'):
                while i < len(lines) and '\u2500' not in lines[i]:
                    i += 1
                i += 1
                continue
            current_section['content'].append(lines[i])

        i += 1

    if current_section:
        sections.append(current_section)

    return sections


# ═══════════════════════════════════════════════════════════
# HTML GENERATORS
# ═══════════════════════════════════════════════════════════



# ── SVG margin icons ──
def _svg_bp():
    # Magnifying glass — observation/behavioral profiling
    return (
        '<svg class="margin-icon" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">'
        # Lens circle
        '<circle cx="7.5" cy="7.5" r="4.8" stroke="#C9A84C" stroke-width="1.4"/>'
        # Handle
        '<line x1="11.3" y1="11.3" x2="15.5" y2="15.5" stroke="#C9A84C" stroke-width="1.6" stroke-linecap="round"/>'
        '</svg>'
    )
def _svg_cr():
    # Book (open, two pages meeting at spine) + head (top-left) + snowflake asterisk (top-right)
    return (
        '<svg class="margin-icon" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">'
        # Open book — left page
        '<path d="M2 11 L9 9.5 L9 17 L2 17 Z" stroke="#1A8FA8" stroke-width="1.1" stroke-linejoin="round"/>'
        # Open book — right page
        '<path d="M16 11 L9 9.5 L9 17 L16 17 Z" stroke="#1A8FA8" stroke-width="1.1" stroke-linejoin="round"/>'
        # Head silhouette (top-left)
        '<circle cx="4.5" cy="4.5" r="2.2" stroke="#1A8FA8" stroke-width="1.1"/>'
        # Snowflake asterisk (top-right, centre 13.5, 4.5)
        '<line x1="13.5" y1="2.4" x2="13.5" y2="6.6" stroke="#1A8FA8" stroke-width="1.1" stroke-linecap="round"/>'
        '<line x1="11.4" y1="4.5" x2="15.6" y2="4.5" stroke="#1A8FA8" stroke-width="1.1" stroke-linecap="round"/>'
        '<line x1="12.0" y1="3.0" x2="15.0" y2="6.0" stroke="#1A8FA8" stroke-width="1.0" stroke-linecap="round"/>'
        '<line x1="15.0" y1="3.0" x2="12.0" y2="6.0" stroke="#1A8FA8" stroke-width="1.0" stroke-linecap="round"/>'
        '</svg>'
    )
def _svg_vs():
    # Raised hand — volunteer selection
    return (
        '<svg class="margin-icon" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">'
        # Palm — upright rectangle
        '<rect x="6" y="6" width="6" height="7" rx="1.2" stroke="#6B52A0" stroke-width="1.2"/>'
        # Index finger raised above palm
        '<rect x="8.5" y="2" width="2" height="5" rx="1" stroke="#6B52A0" stroke-width="1.1"/>'
        # Wrist/arm stub
        '<path d="M7 13 Q7 16 9 16 Q11 16 11 13" stroke="#6B52A0" stroke-width="1.1" stroke-linecap="round"/>'
        '</svg>'
    )
def _svg_am():
    # Two person silhouettes side by side — audience/group
    return (
        '<svg class="margin-icon" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">'
        # Left person — head
        '<circle cx="5" cy="5" r="2.2" stroke="#A83030" stroke-width="1.2"/>'
        # Left person — body
        '<path d="M1.5 16.5c0-2.2 1.6-3.5 3.5-3.5s3.5 1.3 3.5 3.5" stroke="#A83030" stroke-width="1.2" stroke-linecap="round"/>'
        # Right person — head
        '<circle cx="13" cy="5" r="2.2" stroke="#A83030" stroke-width="1.2"/>'
        # Right person — body
        '<path d="M9.5 16.5c0-2.2 1.6-3.5 3.5-3.5s3.5 1.3 3.5 3.5" stroke="#A83030" stroke-width="1.2" stroke-linecap="round"/>'
        '</svg>'
    )

def _opener_legend(tiers=None, cats=None):
    # tiers/cats: lists restricting which badges to show; None = show all
    _all_tiers = ['t1', 't2', 't3', 't4']
    _all_cats  = ['bp', 'cr', 'vs', 'am']
    show_tiers = tiers if tiers else _all_tiers
    show_cats  = cats  if cats  else _all_cats

    tier_html = ''.join(
        f'<span class="badge {t}">{t.upper()}</span>'
        for t in _all_tiers if t in show_tiers
    )
    _cat_html = {
        'bp': f'<span class="icon-item">{_svg_bp()}<span class="icon-code bp">BP</span></span>',
        'cr': f'<span class="icon-item">{_svg_cr()}<span class="icon-code cr">CR</span></span>',
        'vs': f'<span class="icon-item">{_svg_vs()}<span class="icon-code vs">VS</span></span>',
        'am': f'<span class="icon-item">{_svg_am()}<span class="icon-code am">AM</span></span>',
    }
    cat_html = ''.join(_cat_html[c] for c in _all_cats if c in show_cats)

    return (
        '<div class="opener-legend">'
        f'<div class="tier-row">{tier_html}</div>'
        '<div class="legend-label">SIGNAL CONFIDENCE TIERS</div>'
        f'<div class="icon-row">{cat_html}</div>'
        '<div class="legend-label">OBSERVATION CATEGORIES</div>'
        '</div>'
    )

def gen_chapter_opener(section):
    ch_num = section.get('chapter_num', 0)
    part_num = section.get('part_num', 0)
    title = section.get('title', '')
    chapter_key = section.get('chapter_key', '')
    hook = HOOK_LINES.get(chapter_key, '')

    part_names = {0:'',1:'PART ONE',2:'PART TWO',3:'PART THREE',4:'PART FOUR',
                  5:'PART FIVE',6:'PART SIX',7:'PART SEVEN',8:'REFERENCE SECTION'}
    part_label = part_names.get(part_num, '')

    if ch_num > 0:
        ch_display = f'{ch_num:02d}'
    else:
        ch_display = '\u2726'  # diamond for intro

    legend_data = CHAPTER_LEGEND.get(chapter_key, {})
    legend = _opener_legend(tiers=legend_data.get('tiers'), cats=legend_data.get('cats'))
    ch_id = f'chapter-{ch_num}'
    return f'''<section class="chapter-opener" id="{ch_id}" data-part="{part_num}">
  <div class="opener-content">
    <div class="part-label">{escape(part_label)}</div>
    <div class="gold-line"></div>
    <div class="chapter-number">{ch_display}</div>
    <h1 class="chapter-title">{escape(title.upper())}</h1>
    <div class="gold-line thin"></div>
    <div class="hook-line">{hook}</div>
    {legend}
  </div>
</section>'''


def gen_part_opener(section):
    part_num = section.get('part_num', 0)
    subtitle = section.get('subtitle', '')
    part_names = {1:'ONE',2:'TWO',3:'THREE',4:'FOUR',5:'FIVE',6:'SIX',7:'SEVEN'}
    # Part description overrides (mentalism-relevant rewrites)
    _PART_DESCS = {
        1: 'The neurobiology of performance. Predictive processing, salience, cortisol, dopamine, attention, authority, and credibility\u2009\u2014\u2009the mechanisms every mentalist exploits whether they know it or not.',
    }
    # Pull the first content paragraph as the part description
    desc = ''
    content_paras = [p.strip() for p in section.get('content', []) if p.strip()]
    desc_text = _PART_DESCS.get(part_num, content_paras[0] if content_paras else '')
    if desc_text:
        desc = f'<p class="part-desc">{escape(desc_text)}</p>'
    # Reference Section gets its own display label
    if part_num == 8:
        part_label_html = 'REFERENCE SECTION'
    else:
        part_label_html = f'PART {part_names.get(part_num, "")}'
    return f'''<section class="part-opener" data-part="{part_num}">
  <div class="part-opener-content">
    <div class="part-number">{part_label_html}</div>
    <div class="gold-line wide"></div>
    <h1 class="part-title">{escape(subtitle)}</h1>
    {desc}
  </div>
</section>'''


def gen_pattern_interrupt(data):
    wyajd = ''
    if data.get('wyajd'):
        wyajd = f'<p class="pi-wyajd">{data["wyajd"]}</p>'
    return f'''<section class="pattern-interrupt">
  <div class="pi-content">
    <div class="gold-line"></div>
    <div class="pi-number">{data["number"]}</div>
    <div class="pi-unit">{data["unit"]}</div>
    <div class="gold-line"></div>
    <p class="pi-text">{data["text"]}</p>
    <p class="pi-source">{data["source"]}</p>
    {wyajd}
  </div>
</section>'''


def gen_spotlight(text):
    return f'''<aside class="spotlight-box">
  <div class="spotlight-label">KEY PRINCIPLE</div>
  <p class="spotlight-text">{text}</p>
</aside>'''


def gen_key_read(text):
    return f'''<div class="key-read">
  <div class="kr-rule"></div>
  <p class="kr-text">{escape(text)}</p>
  <div class="kr-rule"></div>
</div>'''


def gen_observation_table(rows):
    """Render the 80-observation table as a styled HTML table."""
    use_colors = {'BP':'#C9A84C','CR':'#1A8FA8','VS':'#6B52A0','AM':'#A83030'}
    header = (
        '<div class="obs-table-wrap">'
        '<div class="obs-table-header">'
        '<span class="obs-th obs-num">#</span>'
        '<span class="obs-th obs-name">OBSERVATION</span>'
        '<span class="obs-th obs-what">WHAT IT TELLS YOU</span>'
        '<span class="obs-th obs-tier">TIER</span>'
        '<span class="obs-th obs-use">USE</span>'
        '</div>'
    )
    body_rows = []
    for num, obs, what, tier, use in rows:
        # Tier badge
        tier_cls = tier.lower().replace(' ','') if tier else 'unk'
        tier_badge = f'<span class="badge {tier_cls}">{tier}</span>' if tier else ''
        # Use badges (may be "BP/CR" etc)
        use_parts = use.replace('/',' ').split()
        use_html = ' '.join(
            f'<span class="use-badge" style="color:{use_colors.get(u,"#8A9AB5")};">{u}</span>'
            for u in use_parts
        )
        row_class = 'obs-row-alt' if int(num) % 2 == 0 else 'obs-row'
        body_rows.append(
            f'<div class="obs-row-wrap {row_class}">' +
            f'<span class="obs-num-cell">{num}</span>' +
            f'<span class="obs-name-cell">{escape(obs)}</span>' +
            f'<span class="obs-what-cell">{escape(what)}</span>' +
            f'<span class="obs-tier-cell">{tier_badge}</span>' +
            f'<span class="obs-use-cell">{use_html}</span>' +
            '</div>'
        )
    return header + ''.join(body_rows) + '</div>'


def gen_t4_table():
    """Render the T4 signals as a table in the same style as the 80-signal system."""
    use_colors = {'BP':'#C9A84C','CR':'#1A8FA8','VS':'#6B52A0','AM':'#A83030'}
    header = (
        '<div class="obs-table-wrap t4-table-wrap">'
        '<div class="obs-table-header">'
        '<span class="obs-th obs-num">#</span>'
        '<span class="obs-th obs-name">SIGNAL</span>'
        '<span class="obs-th obs-what">THE READ</span>'
        '<span class="obs-th obs-tier">TIER</span>'
        '<span class="obs-th obs-use">USE</span>'
        '</div>'
    )
    body_rows = []
    for i, (name, read, use) in enumerate(T4_SIGNALS, 1):
        tier_badge = '<span class="badge t4">T4</span>'
        use_parts = use.replace('/',' ').split()
        use_html = ' '.join(
            f'<span class="use-badge" style="color:{use_colors.get(u,"#8A9AB5")};">{u}</span>'
            for u in use_parts
        )
        row_class = 'obs-row-alt' if i % 2 == 0 else 'obs-row'
        body_rows.append(
            f'<div class="obs-row-wrap {row_class}">' +
            f'<span class="obs-num-cell">{i}</span>' +
            f'<span class="obs-name-cell">{escape(name)}</span>' +
            f'<span class="obs-what-cell">{escape(read)}</span>' +
            f'<span class="obs-tier-cell">{tier_badge}</span>' +
            f'<span class="obs-use-cell">{use_html}</span>' +
            '</div>'
        )
    return header + ''.join(body_rows) + '</div>'


_DISC_COLORS = {
    'D': '#A83030',
    'I': '#C9A84C',
    'S': '#1A8FA8',
    'C': '#6B52A0',
}

def _parse_disc_body(body):
    """Split 'Traits. On stage: ... Signals: ...' into parts."""
    traits_raw = body
    on_stage = ''
    signals = []
    if 'On stage:' in body or 'On Stage:' in body:
        sep = 'On stage:' if 'On stage:' in body else 'On Stage:'
        traits_raw, _, rest = body.partition(sep)
        if 'Signals:' in rest:
            on_stage_text, _, sigs_raw = rest.partition('Signals:')
            on_stage = on_stage_text.strip().rstrip('.')
            signals = [s.strip().rstrip('.') for s in sigs_raw.split(' · ') if s.strip()]
        else:
            on_stage = rest.strip()
    traits = [t.strip().rstrip('.') for t in traits_raw.split(' · ') if t.strip()]
    return traits, on_stage, signals

def gen_disc_type_card(letter, name, body):
    """Render a DISC type card (D/I/S/C) with traits, on-stage strategy, signals."""
    color = _DISC_COLORS.get(letter, 'var(--gold)')
    traits, on_stage, signals = _parse_disc_body(body)
    trait_html = ''.join(f'<span class="disc-trait">{escape(t)}</span>' for t in traits)
    sig_html = ''.join(f'<span class="disc-sig">{escape(s)}</span>' for s in signals)
    on_stage_html = f'<div class="disc-onstage"><span class="disc-onstage-label">On Stage</span> {escape(on_stage)}</div>' if on_stage else ''
    return (
        f'<div class="disc-type-card" style="--disc-color:{color}">'
        f'<div class="disc-type-header">'
        f'<span class="disc-letter">{escape(letter)}</span>'
        f'<span class="disc-name">{escape(name)}</span>'
        f'</div>'
        f'<div class="disc-traits">{trait_html}</div>'
        f'{on_stage_html}'
        f'<div class="disc-sigs">{sig_html}</div>'
        f'</div>'
    )

def gen_disc_blend_card(blend, body):
    """Render a DISC blend card (D/C, I/S, D/I, C/S)."""
    letters = [c for c in blend if c in _DISC_COLORS]
    color1 = _DISC_COLORS.get(letters[0], '#888') if letters else '#888'
    color2 = _DISC_COLORS.get(letters[1], '#888') if len(letters) > 1 else color1
    desc = body
    signals = ''
    strategy = ''
    if 'Signals:' in body:
        desc, _, rest = body.partition('Signals:')
        if 'Strategy:' in rest:
            signals, _, strategy = rest.partition('Strategy:')
        else:
            signals = rest
    sig_html = ''.join(
        f'<span class="disc-sig">{escape(s.strip().rstrip("."))}</span>'
        for s in signals.split(' + ') if s.strip()
    ) if signals else ''
    strategy_html = f'<div class="disc-strategy"><span class="disc-strategy-label">Strategy</span> {escape(strategy.strip())}</div>' if strategy.strip() else ''
    return (
        f'<div class="disc-blend-card" style="--blend-color1:{color1};--blend-color2:{color2}">'
        f'<div class="disc-blend-header">'
        f'<span class="disc-blend-name">{escape(blend)}</span>'
        f'</div>'
        f'<p class="disc-blend-desc">{escape(desc.strip())}</p>'
        f'<div class="disc-sigs">{sig_html}</div>'
        f'{strategy_html}'
        f'</div>'
    )


def gen_video_embed(file_id, label, caption):
    """Render a Google Drive video embed."""
    embed_url = f'https://drive.google.com/file/d/{file_id}/preview'
    return (
        f'<div class="video-embed">'
        f'<div class="video-label">{escape(label)}</div>'
        f'<div class="video-frame-wrap">'
        f'<iframe src="{embed_url}" allow="autoplay" allowfullscreen loading="lazy"></iframe>'
        f'</div>'
        f'<p class="video-caption">{escape(caption)}</p>'
        f'</div>'
    )


def gen_bte_signal(name, code, drs, description):
    """Render a single BTE signal entry as a styled card."""
    try:
        drs_val = float(drs)
    except ValueError:
        drs_val = 0
    if drs_val >= 3.0:
        drs_color = '#A83030'
    elif drs_val >= 2.0:
        drs_color = '#C9A84C'
    else:
        drs_color = '#8A9AB5'
    return (
        '<div class="bte-signal">' +
        '<div class="bte-signal-head">' +
        f'<span class="bte-name">{escape(name)}</span>' +
        f'<span class="bte-code">{escape(code)}</span>' +
        f'<span class="bte-drs" style="color:{drs_color}">DRS {drs}</span>' +
        '</div>' +
        f'<p class="bte-desc">{escape(description)}</p>' +
        '</div>'
    )


def gen_six_area_radar():
    """Inline SVG spider/radar chart — Six Areas to Watch, three example profiles."""
    import math

    # ── layout constants ──
    SVG_W  = 520
    HDR_H  = 72   # space reserved for title/subtitle above radar group
    cx, cy = 260, 210   # radar centre inside the translated group
    r_max  = 130
    levels = 5

    # Axes clockwise from top
    axes = [
        'Appearance',
        'Movement',
        'Territory',
        'Social\nConfidence',
        'Cognitive\nProcessing',
        'Emotional\nRegulation',
    ]

    profiles = [
        ('The Take-Charge Type', '#C9A84C', [4.2, 4.5, 4.5, 3.0, 1.8, 2.5]),
        ('The Ideal Volunteer',  '#4A8DB5', [2.5, 2.5, 1.8, 4.5, 3.0, 4.5]),
        ('The Skeptic',          '#C85A5A', [2.8, 2.2, 3.5, 2.0, 4.5, 1.8]),
    ]
    descriptions = [
        'Strong on confidence, movement, and territory. Don\u2019t slow them down.',
        'High reactivity and social confidence. Follows your lead eagerly.',
        'Guards their space. Analytical. Low emotional reaction.',
    ]

    n = len(axes)
    LABEL_R = r_max + 30   # radius to axis label centres
    # Compute total group height: cy + r_max + label clearance (2 lines × 14px + 6px gap)
    GROUP_H = cy + r_max + LABEL_R - r_max + 34   # ~cy + label_r + a bit
    # SVG height: header + radar group + gap + legend (3 rows × 26px)
    LEG_START = HDR_H + GROUP_H + 16
    SVG_H     = LEG_START + 3 * 28 + 8

    def ang(i):
        return math.radians(-90 + i * 360 / n)

    def pt(i, val):
        a   = ang(i)
        rad = (val / levels) * r_max
        return cx + rad * math.cos(a), cy + rad * math.sin(a)

    # ── grid hexagons ──
    grid = ''
    for lvl in range(1, levels + 1):
        pts = ' '.join(
            f'{cx + (lvl/levels)*r_max*math.cos(ang(i)):.1f},'
            f'{cy + (lvl/levels)*r_max*math.sin(ang(i)):.1f}'
            for i in range(n)
        )
        op = '.22' if lvl == levels else '.1'
        grid += f'<polygon points="{pts}" fill="none" stroke="rgba(42,37,32,{op})" stroke-width="1"/>'

    # ── axis spokes ──
    spokes = ''
    for i in range(n):
        x2 = cx + r_max * math.cos(ang(i))
        y2 = cy + r_max * math.sin(ang(i))
        spokes += f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="rgba(42,37,32,.15)" stroke-width="1"/>'

    # ── level labels (Low / Mid / High) ──
    lvl_labels = ''
    for lvl, lbl in ((1, 'Low'), (3, 'Mid'), (5, 'High')):
        lx = cx + (lvl/levels) * r_max * math.cos(ang(0)) + 5
        ly = cy + (lvl/levels) * r_max * math.sin(ang(0)) - 3
        lvl_labels += (
            f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="8" fill="rgba(42,37,32,.35)"'
            f' font-family="sans-serif">{lbl}</text>'
        )

    # ── profile polygons + dots ──
    polys = ''
    for _, color, data in profiles:
        pts = ' '.join(f'{px:.1f},{py:.1f}' for px, py in (pt(i, v) for i, v in enumerate(data)))
        r_v = int(color[1:3], 16); g_v = int(color[3:5], 16); b_v = int(color[5:7], 16)
        polys += (
            f'<polygon points="{pts}" fill="rgba({r_v},{g_v},{b_v},.15)"'
            f' stroke="{color}" stroke-width="2.2" stroke-linejoin="round"/>'
        )
        for i, v in enumerate(data):
            dx, dy = pt(i, v)
            polys += (
                f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="3.8"'
                f' fill="{color}" stroke="white" stroke-width="1.5"/>'
            )

    # ── axis labels — placed at LABEL_R from centre ──
    cat_labels = ''
    for i, cat in enumerate(axes):
        a   = ang(i)
        lx  = cx + LABEL_R * math.cos(a)
        ly  = cy + LABEL_R * math.sin(a)
        anc = 'middle'
        if lx < cx - 12: anc = 'end'
        elif lx > cx + 12: anc = 'start'
        lines  = cat.split('\n')
        base_y = ly - (len(lines) - 1) * 7
        for j, ln in enumerate(lines):
            cat_labels += (
                f'<text x="{lx:.1f}" y="{base_y + j*14:.1f}" text-anchor="{anc}"'
                f' font-size="11" font-weight="700" fill="#2A2520" font-family="sans-serif">{ln}</text>'
            )

    # ── legend — stacked vertically, centred ──
    legend = ''
    lx0 = 60   # left edge of legend block
    for idx, ((pname, color, _), desc) in enumerate(zip(profiles, descriptions)):
        row_y = LEG_START + idx * 28
        legend += (
            f'<rect x="{lx0}" y="{row_y}" width="12" height="12" fill="{color}" rx="2"/>'
            f'<text x="{lx0+18}" y="{row_y+10}" font-size="10.5" font-weight="700"'
            f' fill="{color}" font-family="sans-serif">{pname}</text>'
            f'<text x="{lx0+18}" y="{row_y+23}" font-size="9" fill="rgba(42,37,32,.6)"'
            f' font-family="sans-serif">{desc}</text>'
        )

    return (
        '<div class="six-area-radar">'
        f'<svg viewBox="0 0 {SVG_W} {int(SVG_H)}" xmlns="http://www.w3.org/2000/svg"'
        ' style="width:100%;max-width:540px;display:block;margin:0 auto;">'
        # header
        f'<text x="{SVG_W//2}" y="18" text-anchor="middle" font-size="8" font-weight="700"'
        ' letter-spacing="2.5" fill="#C9A84C" font-family="sans-serif">'
        'READING THE WHOLE PERSON AT ONCE</text>'
        f'<text x="{SVG_W//2}" y="40" text-anchor="middle" font-size="18" font-weight="700"'
        ' fill="#2A2520" font-family="sans-serif">Six Areas to Watch</text>'
        f'<text x="{SVG_W//2}" y="57" text-anchor="middle" font-size="9" fill="rgba(42,37,32,.55)"'
        ' font-family="sans-serif">'
        'Each axis = one dimension of behavior. Farther from center = stronger signal.</text>'
        # radar body
        f'<g transform="translate(0,{HDR_H})">{grid}{spokes}{lvl_labels}{polys}{cat_labels}</g>'
        # legend
        f'<g>{legend}</g>'
        '</svg>'
        '</div>'
    )


def gen_radar_category(num, name, signals_text):
    """Render a Six-Category Radar entry as a styled card with signal chips."""
    raw_parts = [p.strip() for p in signals_text.split(' · ')]
    if raw_parts and raw_parts[0].startswith('Signals: '):
        raw_parts[0] = raw_parts[0][len('Signals: '):]
    signals = []
    insight = ''
    for part in raw_parts:
        m = re.match(r'^(.+?)\s*\[(T[1-4])\][.]?\s*(.*)$', part)
        if m:
            sig_name = m.group(1).strip().rstrip('.')
            tier = m.group(2)
            remainder = m.group(3).strip()
            signals.append((sig_name, tier))
            if remainder:
                insight = remainder
        elif signals:
            insight = (insight + ' ' + part).strip() if insight else part
    chip_html = ''.join(
        f'<span class="rc-signal rc-{tier.lower()}">'
        f'<span class="rc-name">{escape(sig_name)}</span>'
        f'<span class="badge {tier.lower()}">{tier}</span>'
        f'</span>'
        for sig_name, tier in signals
    )
    insight_html = f'<p class="rc-insight">{escape(insight)}</p>' if insight else ''
    return (
        f'<div class="radar-category">'
        f'<div class="rc-header">'
        f'<span class="rc-num">{escape(num)}</span>'
        f'<span class="rc-title">{escape(name)}</span>'
        f'</div>'
        f'<div class="rc-signals">{chip_html}</div>'
        f'{insight_html}'
        f'</div>'
    )


_VOLUNTEER_COLORS = {
    'The Supporter':           '#1A8FA8',
    'The Performer':           '#C9A84C',
    'The Challenger':          '#A83030',
    'The Anxious Volunteer':   '#6B52A0',
    'The Analytical Volunteer':'#8BAAB8',
    'The Emotional Volunteer': '#D4A030',
    'The Reserved Volunteer':  '#3A6B8A',
}

def gen_volunteer_card(name, body):
    """Render a volunteer type as a styled profile card."""
    color = _VOLUNTEER_COLORS.get(name, 'var(--gold)')
    works = ''
    avoid = ''
    desc = body

    if 'Works best for:' in body:
        desc_raw, _, rest = body.partition('Works best for:')
        if 'Avoid for:' in rest:
            works_text, _, avoid_rest = rest.partition('Avoid for:')
            works = works_text.strip().rstrip('.')
            avoid = avoid_rest.strip()
        else:
            works = rest.strip()
        desc = desc_raw.strip()

    # Extract signals: split on ' · ' — description is sentences before the signal chain
    signals = []
    description = desc
    if ' · ' in desc:
        raw = desc.split(' · ')
        first = raw[0]
        last_dot = first.rfind('. ')
        if last_dot >= 0:
            description = first[:last_dot + 1].strip()
            first_sig = first[last_dot + 2:].strip()
        else:
            description = ''
            first_sig = first.strip()
        signals = [s.strip().rstrip('.') for s in [first_sig] + raw[1:] if s.strip()]

    chip_html = (
        '<div class="vc-signals">' +
        ''.join(f'<span class="vc-chip">{escape(s)}</span>' for s in signals) +
        '</div>'
    ) if signals else ''

    meta_html = ''
    if works or avoid:
        meta_html = '<div class="vc-meta">'
        if works:
            meta_html += f'<div class="vc-works"><span class="vc-meta-label">Works best for</span> {escape(works.strip(". "))}</div>'
        if avoid:
            meta_html += f'<div class="vc-avoid"><span class="vc-meta-label">Avoid for</span> {escape(avoid.strip(". "))}</div>'
        meta_html += '</div>'

    desc_html = f'<p class="vc-desc">{escape(description)}</p>' if description else ''

    return (
        f'<div class="volunteer-card" style="--vc-color:{color}">'
        f'<div class="vc-header"><span class="vc-name">{escape(name)}</span></div>'
        f'{desc_html}{chip_html}{meta_html}'
        f'</div>'
    )


def gen_volunteer_matrix_entry(heading, body):
    """Render one cell of the confidence×suggestibility matrix."""
    h = heading.lower()
    if 'high' in h and h.count('high') == 2:
        color   = '#4BAA72'                         # HH: best — green
        bg      = 'linear-gradient(135deg,rgba(16,48,28,.95),rgba(22,58,34,.98))'
        glow    = 'rgba(75,170,114,.18)'
    elif 'high confidence' in h:
        color   = '#C9B832'                         # HL: use with care — yellow
        bg      = 'linear-gradient(135deg,rgba(42,38,6,.95),rgba(52,46,8,.98))'
        glow    = 'rgba(201,184,50,.15)'
    elif 'low suggestibility' in h and 'low confidence' in h:
        color   = '#B83030'                         # LL: avoid — red
        bg      = 'linear-gradient(135deg,rgba(44,10,10,.95),rgba(54,14,14,.98))'
        glow    = 'rgba(184,48,48,.18)'
    else:
        color   = '#D4823B'                         # LH: limited use — orange
        bg      = 'linear-gradient(135deg,rgba(48,24,6,.95),rgba(58,30,8,.98))'
        glow    = 'rgba(212,130,59,.15)'

    # Extract ALL-CAPS recommendation from body start
    rec = ''
    body_rest = body
    if '. ' in body:
        first, _, rest = body.partition('. ')
        if first == first.upper() and len(first) > 2:
            rec = first
            body_rest = rest

    return (
        f'<div class="vm-cell" style="--vm-color:{color};--vm-bg:{bg};--vm-glow:{glow}">'
        f'<div class="vm-heading">{escape(heading)}</div>'
        f'<div class="vm-rec">{escape(rec)}</div>'
        f'<p class="vm-body">{escape(body_rest)}</p>'
        f'</div>'
    )


def gen_wyajd(text):
    return f'''<aside class="wyajd">
  <div class="wyajd-bar"></div>
  <p class="wyajd-text">{text}</p>
</aside>'''


def gen_pull_quote(text):
    return f'''<blockquote class="pull-quote">
  <p>{escape(text)}</p>
</blockquote>'''


# Map C-word to data-c slug and brand color
_FIVE_C_MAP = {
    'Context':     ('context',     'What environment is the behavior occurring in?'),
    'Clusters':    ('clusters',    'Are multiple signals pointing the same direction?'),
    'Congruence':  ('congruence',  'Does the body match the words?'),
    'Consistency': ('consistency', 'How does this compare to their baseline?'),
    'Culture':     ('culture',     'What are the background norms?'),
}

def gen_five_c_entry(c_word, body_text):
    slug, question = _FIVE_C_MAP[c_word]
    opener = closer = ''
    if c_word == 'Context':
        opener = (
            '<div class="five-cs-prose-chart">' +
            '<div class="fcp-header">' +
            '<div class="fcp-title">THE FIVE C&#x27;s IN PRACTICE</div>' +
            '<div class="fcp-subtitle">Apply as a chain. Each filter builds on the last.</div>' +
            '</div>'
        )
    if c_word == 'Culture':
        closer = (
            '<div class="fcp-footer">' +
            '<span class="fcp-chain">Context › Clusters › Congruence › Consistency › Culture › <span class="fcp-read">READ</span></span>' +
            '</div>' +
            '</div>'
        )
    return (
        opener +
        f'<div class="five-c-entry" data-c="{slug}">' +
        f'  <div class="fce-head">' +
        f'    <span class="fce-name">{c_word}</span>' +
        f'    <span class="fce-dash">—</span>' +
        f'    <span class="fce-question">{escape(question)}</span>' +
        f'  </div>' +
        f'  <p class="fce-body">{escape(body_text)}</p>' +
        f'</div>' +
        closer
    )

def gen_performer_note():
    return '''<div class="performer-note-header">
  <span class="pn-label">Chris Michael's Take</span>
</div>'''


def gen_warning_header(text):
    """Render a high-visibility warning section header (e.g. 'When You Have Gone Too Far')."""
    return f'''<div class="warning-header">
  <div class="wh-icon">&#9888;</div>
  <h3 class="wh-title">{escape(text)}</h3>
</div>'''


def gen_warning_callout(heading, body):
    """Render a 'Common Misread' or similar caution callout box."""
    return f'''<div class="warning-callout">
  <div class="wc-label">&#9888; {escape(heading)}</div>
  <p class="wc-body">{escape(body)}</p>
</div>'''


# Certainty level colors for Soft/Moderate/Strong/Pinpoint frames
_CERTAINTY_FRAME_META = {
    'Soft Frame':     {'color': '#8A9AB5', 'tier': 'T3 / T4 signals', 'badge_cls': 'cf-soft'},
    'Moderate Frame': {'color': '#C9A84C', 'tier': 'T2 cluster read', 'badge_cls': 'cf-moderate'},
    'Strong Frame':   {'color': '#D4763B', 'tier': 'T1 / T2 anchor', 'badge_cls': 'cf-strong'},
    'Pinpoint Frame': {'color': '#4BAA72', 'tier': 'Evidence-locked', 'badge_cls': 'cf-pinpoint'},
}

def gen_certainty_frame(name, body):
    """Render a Soft/Moderate/Strong/Pinpoint Frame as a styled card."""
    meta = _CERTAINTY_FRAME_META.get(name, {'color': '#C9A84C', 'tier': '', 'badge_cls': 'cf-moderate'})
    color = meta['color']
    tier  = meta['tier']
    badge = meta['badge_cls']

    # Parse body: "Use when ... '[line]' · '[line]' ... Avoid/Never ..."
    # Split on bullet separator first, then classify each segment
    use_text = ''
    examples = []
    avoid_text = ''

    segments = [s.strip() for s in body.split(' · ')]
    for seg in segments:
        if not seg:
            continue
        sl = seg.lower()
        if sl.startswith('avoid ') or sl.startswith('never '):
            avoid_text = seg.rstrip('.')
        elif seg.startswith("'") or seg.startswith('\u2018'):
            # Extract from first quote to last quote, handling internal apostrophes
            first_q = seg.find("'") if "'" in seg else seg.find('\u2018')
            last_q  = seg.rfind("'") if "'" in seg else seg.rfind('\u2019')
            if last_q > first_q:
                example = seg[first_q + 1:last_q].strip()
                after   = seg[last_q + 1:].strip()
                examples.append(example)
                if after.lower().startswith('avoid') or after.lower().startswith('never'):
                    avoid_text = after.rstrip('.')
            else:
                examples.append(seg.strip("'\u2018\u2019"))
        else:
            if not examples:
                # Pre-quote text is the "Use when" sentence
                use_text = (use_text + ' ' + seg).strip().rstrip('.') if use_text else seg.rstrip('.')

    lines_html = ''.join(
        f'<div class="cf-line">\u201c{escape(ex)}\u201d</div>' for ex in examples
    )
    avoid_html = (
        f'<div class="cf-avoid">{escape(avoid_text)}</div>' if avoid_text else ''
    )
    use_html = f'<div class="cf-use">{escape(use_text)}</div>' if use_text else ''

    return (
        f'<div class="certainty-frame {badge}" style="--cf-color:{color}">'
        f'  <div class="cf-header">'
        f'    <span class="cf-name">{escape(name)}</span>'
        f'    <span class="cf-tier">{escape(tier)}</span>'
        f'  </div>'
        f'  {use_html}'
        f'  <div class="cf-lines">{lines_html}</div>'
        f'  {avoid_html}'
        f'</div>'
    )


def gen_rule_callout(heading, body):
    """Render sub-concept rules (Pace-Lead Ratio, X Check, X Structure) as compact callouts."""
    return (
        f'<div class="rule-callout">'
        f'  <div class="rc-heading">{escape(heading)}</div>'
        f'  <p class="rc-body">{escape(body)}</p>'
        f'</div>'
    )


# Seven Stages — color arc from cool steel to warm gold to emerald
_STAGE_COLORS = {
    '01': '#5B8EA6', '02': '#4A9B8E', '03': '#8A9AB5',
    '04': '#C9A84C', '05': '#D4823B', '06': '#D4763B', '07': '#4BAA72',
}

def gen_stage_card(num, name, body):
    """Render a Seven Stages card — sequential arc feel, distinct from radar categories."""
    color = _STAGE_COLORS.get(num, '#C9A84C')
    return (
        f'<div class="stage-card" style="--stage-color:{color}">'
        f'  <div class="stage-num">{escape(num)}</div>'
        f'  <div class="stage-content">'
        f'    <div class="stage-name">{escape(name)}</div>'
        f'    <div class="stage-rule"></div>'
        f'    <p class="stage-body">{escape(body)}</p>'
        f'  </div>'
        f'</div>'
    )


def gen_checklist_section(heading, bullets_text):
    """Render a Neural Performance Checklist section — checkbox item rows."""
    items = [b.strip() for b in bullets_text.split(' · ') if b.strip()]
    def _cl_item(it):
        if ' | ' in it:
            main, note = it.split(' | ', 1)
            return (
                f'<div class="cl-item">'
                f'<span class="cl-box">□</span>'
                f'<span class="cl-text">{escape(main)}'
                f'<span class="cl-note">{escape(note)}</span>'
                f'</span></div>'
            )
        return f'<div class="cl-item"><span class="cl-box">□</span><span class="cl-text">{escape(it)}</span></div>'
    items_html = ''.join(_cl_item(it) for it in items)
    return (
        f'<div class="checklist-section">'
        f'  <div class="cl-heading">{escape(heading)}</div>'
        f'  <div class="cl-items">{items_html}</div>'
        f'</div>'
    )


def gen_mnemonic(acronym, phrase, expansion, note):
    """Render a mnemonic memory-aid block."""
    exp_html = ''.join(
        f'<span class="mn-item">{escape(item.strip())}</span>'
        for item in expansion.split('·') if item.strip()
    )
    return (
        f'<div class="mnemonic-block">'
        f'<div class="mn-header">'
        f'<span class="mn-label">REMEMBER IT</span>'
        f'<span class="mn-acronym">{escape(acronym)}</span>'
        f'</div>'
        f'<div class="mn-phrase">&ldquo;{escape(phrase)}&rdquo;</div>'
        f'<div class="mn-expansion">{exp_html}</div>'
        f'<div class="mn-note">{escape(note)}</div>'
        f'</div>'
    )


def gen_def_card(term, definition):
    """Render a compact inline definition card — term in gold, definition beside it."""
    return (
        f'<div class="def-card">'
        f'<div class="dc-term">{escape(term)}</div>'
        f'<div class="dc-def">{escape(definition)}</div>'
        f'</div>'
    )


def gen_numbered_card(num, title, body):
    """Render a numbered variation card (e.g. 1. Full-face micros)."""
    return (
        f'<div class="numbered-card">'
        f'<div class="nc-num">{escape(num)}</div>'
        f'<div class="nc-content">'
        f'<div class="nc-title">{escape(title)}</div>'
        f'<p class="nc-body">{escape(body)}</p>'
        f'</div>'
        f'</div>'
    )


def gen_recovery_card(num, name, when, body):
    """Render a cortisol-recovery method card — amber, numbered, with a WHEN tag."""
    # Process body for bold terms
    body_html = _apply_bold(escape(body))
    return (
        f'<div class="recovery-card">'
        f'<div class="rc-header">'
        f'<span class="rc-num">0{num}</span>'
        f'<span class="rc-name">{escape(name)}</span>'
        f'</div>'
        f'<div class="rc-when"><span class="rc-when-label">WHEN</span> {escape(when)}</div>'
        f'<div class="rcv-body">{body_html}</div>'
        f'</div>'
    )


def gen_anthem_aria_card(body):
    """Render an Anthem & Aria field advice card — pink/blue split header."""
    body_html = _apply_bold(escape(body))
    return (
        '<div class="anthem-aria-card">'
        '<div class="aa-header">'
        '<span class="aa-label">Anthem &amp; Aria</span>'
        '<span class="aa-subtitle">Field Advice</span>'
        '</div>'
        f'<div class="aa-body">{body_html}</div>'
        '</div>'
    )


def gen_toolkit_nav():
    """Render jump-link navigation panel for the Cold Reading Toolkit."""
    cats = [
        ('Appearance',          'cr-appearance'),
        ('Movement',            'cr-movement'),
        ('Territory',           'cr-territory'),
        ('Social Confidence',   'cr-confidence'),
        ('Cognitive Processing','cr-cognitive'),
        ('Emotional Regulation','cr-emotional'),
    ]
    links = ''.join(
        f'<a href="#{aid}" class="tn-link">{name}</a>' for name, aid in cats
    )
    return (
        '<div class="toolkit-nav">'
        '<span class="tn-label">Jump to section</span>'
        f'<div class="tn-links">{links}</div>'
        '</div>'
    )


def gen_cr_summary_table():
    """Render quick-reference summary table for the Cold Reading Toolkit."""
    _ROWS = [
        ('Appearance',          'Immaculate clothing or grooming',  'C',   'Baseline / Stage',   'Every detail is in place. Nothing about you is accidental.'),
        ('Appearance',          'Bold, eye-catching colors',        'I',   'Stage / Strolling',  'You dress to be seen. Not out of vanity — because ordinary clothes could not contain it.'),
        ('Movement',            'Purposeful stride, forward lean',  'D',   'Leadership',         'You walk like you have a destination, even when you do not.'),
        ('Movement',            'Arms crossed, guarded posture',    'S',   'Guarded',            'You cross your arms so naturally you probably do not notice. Trust does not come easily.'),
        ('Territory',           'Back to wall, exit scanning',      'C/S', 'Security baseline',  'You like a clear view of the room. You do not miss much happening around you.'),
        ('Territory',           'Sprawls, claims space',            'D',   'Stage / Dominant',   'You quietly own any space you enter.'),
        ('Social Confidence',   'Initiates warmly, no strangers',   'I',   'Crowd / Stage',      'You have never met a stranger. That warmth makes others feel seen.'),
        ('Social Confidence',   'Listens quietly, speaks once',     'C',   'Close-up / Intimate','When you speak, everyone goes quiet — because they know it will matter.'),
        ('Cognitive Processing','Pauses carefully before speaking', 'C',   'Thoughtful',         'That pause is not uncertainty. It is precision.'),
        ('Cognitive Processing','Rapid, run-on speech',             'I',   'Influence / Crowd',  'Your thoughts race. Even at rest, your mind does not slow down.'),
        ('Emotional Regulation','Calm in chaos, refuses to panic',  'D',   'Dominant control',   'You do feel panic. You just refuse to feed it.'),
        ('Emotional Regulation','Smiles or laughs when hurt',       'S',   'Emotional baseline', 'You smile even when you are hurting. The gentleness in your eyes gives it away.'),
    ]
    rows_html = ''.join(
        f'<tr class="crs-{"alt" if idx % 2 else "base"}">'
        f'<td class="crs-cat">{escape(cat)}</td>'
        f'<td class="crs-cue">{escape(cue)}</td>'
        f'<td class="crs-disc"><span class="crs-dbadge">{escape(disc)}</span></td>'
        f'<td class="crs-ctx">{escape(ctx)}</td>'
        f'<td class="crs-line"><em>{escape(line)}</em></td>'
        '</tr>'
        for idx, (cat, cue, disc, ctx, line) in enumerate(_ROWS)
    )
    return (
        '<div class="cr-summary-table">'
        '<div class="crst-header">'
        '<span class="crst-title">Quick Reference</span>'
        '<span class="crst-sub">Cue &rarr; Type &rarr; Line</span>'
        '</div>'
        '<table class="crst-table">'
        '<thead><tr>'
        '<th>Category</th><th>Cue</th><th>Type</th><th>Context</th><th>Opening Line</th>'
        '</tr></thead>'
        f'<tbody>{rows_html}</tbody>'
        '</table>'
        '</div>'
    )


def gen_feedback_chart():
    """Render the 4-signal reading feedback reference chart as a uniform grid."""
    _SIGNALS = [
        ('01', 'Lip Compression',
         'Suppressed disagreement. They think the read is wrong.',
         'Reframe without defending. Preserve the theme, reverse the direction.',
         'Instead of <em>You trust people easily</em>, try <em>You want to trust people, but experience has made you careful.</em>'),
        ('02', 'Eyebrow Flash + Pause',
         'Uncertainty. The frame did not fit cleanly.',
         'Broaden the statement. Give it more room to land.',
         '<em>This may not apply in every situation, but there is a pattern around you where&hellip;</em>'),
        ('03', 'Head Turning Away',
         'Low recognition. This category has lost traction.',
         'Change topic territory entirely.',
         'Move from relationships to work, or from work to trust and decision-making.'),
        ('04', 'Microexpression of Contempt',
         'They have rejected the frame. Not disagreed. Rejected.',
         'Full reset. Do not push further.',
         '<em>You strike me as someone who does not particularly like being read too quickly.</em> Their resistance becomes your hit.'),
    ]
    # Column header row
    col_heads = (
        '<div class="fbc-ch"></div>'
        '<div class="fbc-ch">Signal Means</div>'
        '<div class="fbc-ch">Adjustment</div>'
        '<div class="fbc-ch">Pivot To</div>'
    )
    cells_html = col_heads
    for num, signal, meaning, action, example in _SIGNALS:
        cells_html += (
            f'<div class="fbc-sig-cell"><span class="fbc-num">{num}</span><span class="fbc-name">{signal}</span></div>'
            f'<div class="fbc-data-cell">{meaning}</div>'
            f'<div class="fbc-data-cell">{action}</div>'
            f'<div class="fbc-data-cell fbc-pivot">{example}</div>'
        )
    return (
        '<div class="feedback-chart">'
        '<div class="fbc-header"><span class="fbc-title">Reading the Feedback</span>'
        '<span class="fbc-sub">Four signals. Four corrections.</span></div>'
        f'<div class="fbc-grid">{cells_html}</div>'
        '</div>'
    )


def gen_cr_toolkit_entry(cue, line, disc, context):
    """Render a Cold Reading Toolkit entry — cue + DISC/context meta + reading line."""
    _DISC_LABELS = {
        'D': 'D · Decisive', 'I': 'I · Expressive',
        'S': 'S · Steady',   'C': 'C · Analytical',
        'D / I': 'D / I', 'D/I': 'D / I',
        'C / S': 'C / S', 'C/S': 'C / S',
        '—': '—', '-': '—', '': '',
    }
    disc_label = _DISC_LABELS.get(disc.strip(), disc.strip())
    line_html = _apply_bold(escape(line))
    disc_html = f'<span class="crt-disc">{escape(disc_label)}</span>' if disc_label else ''
    ctx_html  = f'<span class="crt-context">{escape(context)}</span>' if context else ''
    return (
        '<div class="cr-toolkit-entry">'
        '<div class="crt-header">'
        f'<span class="crt-cue">{escape(cue)}</span>'
        f'<span class="crt-meta">{disc_html}{ctx_html}</span>'
        '</div>'
        f'<div class="crt-line">{line_html}</div>'
        '</div>'
    )


_SECTION_ICONS = {
    'Appearance':                   '✨',
    'Movement and Posture':         '🏃',
    'Territory and Personal Space': '🛡',
    'Social Confidence':            '👁',
    'Cognitive Processing':         '🧠',
    'Emotional Regulation':         '❤️',
}

def _ctx_to_symbols(ctx):
    """Map context string to emoji performance symbols."""
    ctx_l = ctx.lower()
    syms = []
    if any(x in ctx_l for x in ('stage', 'crowd', 'audience', 'leadership', 'dominant', 'influence')):
        syms.append('🎭')
    if any(x in ctx_l for x in ('strolling', 'walk-around', 'walk around')):
        syms.append('🏃')
    if any(x in ctx_l for x in ('close-up', 'intimate', 'baseline', 'quiet', 'subtle', 'analytical', 'thoughtful', 'preparation')):
        syms.append('👁')
    if any(x in ctx_l for x in ('guarded', 'hiding', 'reserved', 'restraint', 'caution')):
        syms.append('⚠️')
    return '\u2009'.join(syms)


def gen_feedback_signals_ref():
    """Compact feedback-signals callout — sits below the toolkit nav."""
    signals = [
        ('Lip compression',       'pause, then reverse the direction of the line'),
        ('Eyebrow flash + pause', 'broaden the statement, give it more room to land'),
        ('Head turning away',     'switch cue category entirely'),
        ('Smile or nod',          'expand on the theme — you have the thread'),
    ]
    sym_key = [
        ('🎭', 'Stage or crowd'),
        ('🏃', 'Strolling'),
        ('👁', 'Close-up or baseline'),
        ('⚠️', 'Adjust first'),
    ]
    sigs_html = ''.join(
        f'<li><span class="fsr-sig">{escape(s)}</span>'
        f'<span class="fsr-arrow"> → </span>{escape(a)}</li>'
        for s, a in signals
    )
    key_html = ''.join(
        f'<span class="fsr-key-item"><span class="fsr-key-sym">{sym}</span>{escape(label)}</span>'
        for sym, label in sym_key
    )
    return (
        '<div class="feedback-signals-ref">'
        '<div class="fsr-header">'
        '<span class="fsr-title">Feedback Signals · Quick Reference</span>'
        f'<span class="fsr-key">{key_html}</span>'
        '</div>'
        f'<ul class="fsr-list">{sigs_html}</ul>'
        '</div>'
    )


def gen_crt_table(rows):
    """Render buffered CRT rows as a 3-col scan table: Cue | Line + symbols | DISC badge."""
    _DISC_CLASS = {
        'D': 'disc-d', 'I': 'disc-i', 'S': 'disc-s', 'C': 'disc-c',
        'D / I': 'disc-di', 'D/I': 'disc-di',
        'C / S': 'disc-cs', 'C/S': 'disc-cs',
        '\u2014': 'disc-other', '-': 'disc-other', '': 'disc-other',
    }
    if not rows:
        return ''
    rows_html = ''
    for cue, line, disc, context in rows:
        disc_clean = disc.strip().replace('/', ' / ')
        disc_cls   = _DISC_CLASS.get(disc.strip(), 'disc-other')
        syms       = _ctx_to_symbols(context)
        sym_html   = f'<span class="crt-syms">{syms}</span>' if syms else ''
        line_html  = _apply_bold(escape(line))
        rows_html += (
            f'<tr>'
            f'<td class="crt-cue-cell">{escape(cue)}</td>'
            f'<td class="crt-line-cell">'
            f'<span class="crt-line-text">{line_html}</span>'
            f'{sym_html}'
            f'</td>'
            f'<td class="crt-disc-cell">'
            f'<span class="crt-disc-badge {disc_cls}">{escape(disc_clean) if disc_clean else "\xb7"}</span>'
            f'</td>'
            f'</tr>'
        )
    return (
        '<table class="crt-table">'
        '<thead><tr>'
        '<th class="crt-th crt-th-cue">Cue</th>'
        '<th class="crt-th crt-th-line">Line</th>'
        '<th class="crt-th crt-th-disc">Type</th>'
        '</tr></thead>'
        f'<tbody>{rows_html}</tbody>'
        '</table>'
    )


def gen_cm_takeaway(body):
    """Render a CM Takeaway callout block — dark navy, gold label, cream italic body."""
    body_html = _apply_bold(escape(body))
    return (
        '<div class="cm-takeaway">'
        '<div class="cm-label">CM Takeaway</div>'
        f'<div class="cm-body">{body_html}</div>'
        '</div>'
    )


def gen_what_you_have_felt():
    return '''<div class="felt-before">
  <p class="felt-label">WHAT IT FEELS LIKE</p>
</div>'''


def gen_forces_intro(statement, forces_text):
    """Render a 'Five forces...' doctrine block with force pills."""
    # Split forces by comma/and
    raw = re.split(r',\s*(?:and\s+)?|\s+and\s+', forces_text.rstrip('.'))
    pills = ''.join(
        f'<span class="force-pill">{escape(f.strip())}</span>'
        for f in raw if f.strip()
    )
    return f'''<div class="forces-intro">
  <p class="forces-statement">{escape(statement)}</p>
  <div class="forces-pills">{pills}</div>
</div>'''


# ── BOLD TERMS — key technical/named signals bolded on every occurrence ──
# Regex applies optional plural 's' automatically — no need for duplicate entries.
BOLD_TERMS = [
    # DISC personality system
    'DISC',
    'D-type', 'I-type', 'S-type', 'C-type',
    'D/I-type', 'D/C-type', 'I/S-type', 'S/C-type',
    # Named behavioral signals
    'confirmation glance', 'social referencing glance', 'eyebrow flash',
    'lip compression', 'transderivational search', 'chiral expression', 'chirality',
    'leakage hierarchy', 'baseline deviation',
    'microexpression', 'micro-expression',
    'productive tension', 'cortisol threshold', 'cortisol window',
    # Named measurement systems
    'Duchenne smile', 'Duchenne marker',
    'FACS', 'Action Units',
    # Cognitive / psychological named effects
    'cognitive load', 'cognitive dissonance', 'cognitive bias',
    'confirmation bias', 'social proof',
    'Von Restorff effect', 'framing effect',
    'inattentional blindness', 'change blindness',
    'predictive processing', 'processing fluency',
    'variable reward',
    # NLP / hypnosis / suggestion techniques
    'double bind', 'presupposition', 'yes set',
    'pacing and leading', 'modality matching',
    'VAK', 'suggestibility', 'absorption',
    'pseudo-hypnotic',
    # Mentalism & performance techniques
    'misdirection', 'psychological force', 'dual reality',
    'pattern interrupt', 'soft hit', 'strong hit',
    'layered read', 'opening read',
    'salience',
    # Observation categories
    'Behavioral Profiling', 'Volunteer Selection', 'Audience Management',
    # Performance framing headers
    'How it helps your performances:', 'How it hurts your performances:',
    'Watch three zones:', 'And watch them at three moments:',
    'In practical terms, the best training path is simple:',
    'A better use is invisible.',
    # Book core frameworks
    'Five Cs', 'Six-Category Radar',
    'Cluster Reading', 'context dependency',
    # Reading types & book-named techniques
    'cold reading', 'warm reading', 'hot reading',
    'thin slicing', 'Forer effect',
    'Three-Signal Rule',
    'serial position', 'primacy effect', 'recency effect',
    # Book-system concepts
    'method invisibility', 'volunteer management',
    'Fruit to Fang',
    # T4 clinical terms
    'phrenology', 'physiognomy', 'graphology',
]

def _apply_bold(text):
    """Apply bold to BOLD_TERMS in text, safely skipping existing HTML tags.
    Automatically handles plurals by appending optional 's' to each term pattern."""
    segments = re.split(r'(<[^>]+>)', text)
    out = []
    for seg in segments:
        if seg.startswith('<'):
            out.append(seg)
        else:
            for term in BOLD_TERMS:
                # s? handles plurals (D-types, microexpressions, etc.)
                seg = re.sub(
                    rf'(?<!\w)({re.escape(term)}s?)(?!\w)',
                    r'<strong>\1</strong>',
                    seg,
                    flags=re.IGNORECASE
                )
            out.append(seg)
    return ''.join(out)


def process_paragraph(text, part_num=1):
    """Process a single paragraph with inline design elements."""
    stripped = text.strip()
    if not stripped:
        return ''

    # Skip figure captions extracted from DOCX (handled by FIGURES config)
    if re.match(r'^Figure\s+\d+\.\d+\s*[\u2014\-]', stripped):
        return ''

    # Section breaks
    if is_section_break(stripped):
        return '<div class="section-break">\u00b7 \u00b7 \u00b7</div>'

    # "What You Have Felt Before" motif
    if is_what_you_have_felt(stripped):
        return gen_what_you_have_felt()

    # Five Cs prose entries: "Context — ...", "Clusters — ...", etc.
    for c_word in ('Context', 'Clusters', 'Congruence', 'Consistency', 'Culture'):
        prefix = c_word + ' — '
        prefix_alt = c_word + ' - '
        if stripped.startswith(prefix) or stripped.startswith(prefix_alt):
            sep = prefix if stripped.startswith(prefix) else prefix_alt
            rest = stripped[len(sep):]
            # Strip the question sentence from the start of rest
            _q, _, body = rest.partition('?')
            body = body.strip()
            if not body:
                body = rest  # fallback: use full text if no question mark found
            return gen_five_c_entry(c_word, body)

    # Performer's Note — distinct from section headers
    if stripped in ("Performer's Note", "Performer's Note", "Performers Note"):
        return gen_performer_note()

    # Italic paragraphs — [ITALIC]...[/ITALIC] markers
    if stripped.startswith('[ITALIC]') and stripped.endswith('[/ITALIC]'):
        inner = escape(stripped[8:-8])
        return f'<p style="font-style:italic;color:#c8d4e0;">{inner}</p>'

    # Bylines — bold attribution lines beneath section headers
    _bylines = {
        '\u201cWatch Your Figure\u201d by Chris Michael',
        '"Watch Your Figure" by Chris Michael',
    }
    if stripped in _bylines:
        return f'<p style="font-weight:700;font-style:italic;color:#c9a84c;margin:0.2em 0 1em;">{escape(stripped)}</p>'

    # Warning section headers — stand-out treatment
    _warning_headers = {
        'When You Have Gone Too Far',
    }
    if stripped in _warning_headers:
        return gen_warning_header(stripped)

    # Major parent section headers — elevated divider treatment
    # Featured concept headers — split on colon, elevated two-line treatment
    _concept_headers = {
        'Semantic Satiation: Why Words Die in Your Mouth',
    }
    if stripped in _concept_headers:
        if ':' in stripped:
            concept, _, tagline = stripped.partition(':')
            return (
                f'<div class="concept-header">'
                f'<div class="ch-rule"></div>'
                f'<div class="ch-concept">{escape(concept.strip())}</div>'
                f'<div class="ch-tagline">{escape(tagline.strip())}</div>'
                f'<div class="ch-rule"></div>'
                f'</div>'
            )

    _major_headers = {
        'Fruit to Fang',
        # Ch20 parent buckets — Propless Mentalism
        'WHY LEARN PROPLESS MENTALISM',
        'WHY PROPLESS MENTALISM TYPICALLY SUCKS',
        'PREMISE ARCHITECTURE',
        'FREEDOM AND RESTRICTION',
        'COVERT ACQUISITION',
        'THE PUMP',
        'TIPS WHEN PERFORMING PROPLESS MENTALISM',
        'ENDGAME CONTROL',
        # Ch18 Memory Distortion parent buckets
        'WHAT IS ACTUALLY HAPPENING',
        'THE EIGHT MECHANISMS',
        'THE LANGUAGE TOOLS',
        'APPLICATIONS FOR MENTALISTS: WHEN AND HOW TO USE IT',
        # Ch19 parent buckets
        'THE DESIGN DOCTRINE',
        'THE BUILD PROCESS',
        'THE OPERATOR MODEL',
        'EXAMPLE SYSTEMS',
        'ADVANCED REFINEMENTS',
        # Ch19 parent buckets — Psychological Forces
        'My Current Favorite Psychological Force',
        'WHY PSYCHOLOGICAL FORCES WORK',
        'USING PSYCHOLOGICAL FORCES AS A TOSSED-OUT DECK',
        'CATEGORIZING PSYCHOLOGICAL FORCES',
        'HOW FORCES COMBINE',
        'HOW TO CONSTRUCT YOUR OWN PSYCHOLOGICAL FORCES',
        'THE SIMPLEST WAY TO THINK ABOUT ALL 13',
    }
    if stripped in _major_headers:
        return f'<h3 class="section-header sh-major">{escape(stripped)}</h3>'

    # Child sub-headers — visually indented, clearly subordinate to a named parent section
    _child_heads = {
        # Lip Compression child sub-sections
        'Why context matters',
        'In mentalism, this often means: you have something wrong',
        'The mouth often reveals restraint before language does',
        'The silent objection is often more useful than the spoken one',
        'How it changes handling on stage',
        'What this is really showing you',
        'The Architecture of Obedience',
    }
    if stripped in _child_heads:
        return f'<div class="sub-header sh-child"><span class="sub-header-label">{escape(stripped)}</span></div>'

    # Sub-section headers — subordinate topics sitting under a parent section header
    _sub_section_heads = {
        'Breathing Visibility', 'The Laughter Signal', 'Stillness Gradient',
        'Phone Emergence', 'Self-Soothing', 'Absence of Response',
        'The Redirect',
        'Image or feeling', 'Fast impression or gradual realization',
        'Attention and concentration', 'Emotional framing', 'Stage management',
        'The Setup', 'Watching the First Search', 'The Pivot',
        'Reading the Animal Search', 'Reading the Reaction',
        # Zodiac chapter sub-sections
        'When They Do Not Know Their Element',
        'The Explanation',
        # Contact mind reading sub-sections
        'Lipping',
        # Cold Reading Toolkit single-word headers
        'Appearance',
        # Field Notes sub-sections
        'Reflect and Reset',
        # Double binds sub-sections
        'Why this matters on stage',
        'What a double bind really does',
        "The mentalist's version",
        'An easy way to understand it',
        'Examples for mentalism',
        'Why this increases compliance',
        'Where performers misuse this',
        'A useful rule for building them',
        # Transderivational search sub-sections
        'How to spot it',
        'Why it happens',
        # Microexpression sub-sections
        'How to identify them in the real world',
        'How to identify variations',
        'What to look for in a performance context',
        'How this applies to specific mentalism methods',
        'The best way to train this',
        "The performer's rule",
        'The deeper point',
        # Ch18 Memory Distortion — memory stage sub-items
        'ENCODING', 'Consolidation', 'Retrieval', 'Reconstruction',
        'Source monitoring', 'A brief note on the function',
        # Ch19 Psychological Forces sub-headers
        'Performance Note', 'THE PSYCHOLOGY BEHIND IT', 'A NOTE ON PERFORMING THIS',
        # Ch19 Example System structural labels (repeated across each system)
        'Why this target', 'The stable variables', 'The prompts', 'The cluster map',
        'Ambiguity resolution', 'The reveal sequence', 'The fallback', 'Why this works',
        'The core insight', 'The reveal', 'The temporal read',
        # Ch19 Sitcom Constellation structural labels
        'Why sitcoms work as a category', 'The target set', 'The hidden architecture',
        'The acquisition ritual', 'Reading the contact', 'The reveal structure',
        'The show-world pumps', 'The fallback', 'Why it works', 'Performance notes',
        # Ch19 Advanced Refinements sub-labels
        'The two-phase structure', 'What the second phase actually does',
        'The calibration line', 'The rule that changes what you build',
        # Ch19 Real Secrets sub-items
        'Rejection is structure', 'Simplicity is not minimalism',
        'Design for the worst participant',
        # Ch45 Psychological Forces sub-labels
        'Over-restriction', 'Under-restriction', 'Poor timing',
        'Lack of layering', 'Bad framing',
    }
    if stripped in _sub_section_heads:
        return f'<div class="sub-header"><span class="sub-header-label">{escape(stripped)}</span></div>'

    # Numbered step headers: "01 — SHOES", "02 — HANDS", etc.
    # Pattern: 1-2 digits, dash/em-dash, ALL CAPS label (≤4 words)
    _step_m = re.match(r'^(\d{1,2})\s*[\u2014\u2013\-]+\s*([A-Z][A-Z /]+)$', stripped)
    if _step_m:
        _sn, _sl = _step_m.group(1), _step_m.group(2).strip()
        return f'<div class="step-header"><span class="step-num">{escape(_sn)}</span><span class="step-name">{escape(_sl)}</span></div>'

    # Dialogue lines — standalone paragraphs fully enclosed in quotation marks
    if ((stripped.startswith('\u201c') and stripped.endswith('\u201d')) or
            (stripped.startswith('"') and stripped.endswith('"'))) and len(stripped) > 8:
        return f'<p class="dialogue-line"><strong><em>{escape(stripped)}</em></strong></p>'

    # Headers forced to sh-section (child items in numbered sequences)
    _force_sh_section = {
        # Ch19 Five Acquisition Channels — child of FIVE ACQUISITION CHANNELS BEYOND LETTERS
        '1. EMBODIED BINARIES', '2. SENSORY GATES', '3. CATEGORY LOCKS',
        '4. SOCIALLY NATURAL NARROWING', '5. REACTION-BASED PUMPS',
        # Ch19 Eight Steps — all uniform, child of THE EIGHT-STEP DESIGN PROCESS
        'STEP 1: DEFINE THE TARGET WITH REALISTIC SCOPE',
        'STEP 2: IDENTIFY STABLE VARIABLES ONLY',
        'STEP 3: CONVERT QUESTIONS INTO RECOGNITION PROMPTS',
        'STEP 4: LIMIT TO TWO STRUCTURAL EXTRACTIONS',
        'STEP 5: BUILD TARGET CLUSTERS',
        'STEP 6: DESIGN AMBIGUITY RESOLUTION WITHOUT ADDITIONAL PROMPTS',
        'STEP 7: DESIGN THE REVEAL IN LAYERS',
        'STEP 8: BUILD THE FALLBACK PATH FIRST',
    }
    if stripped in _force_sh_section and is_section_header(stripped):
        return f'<h3 class="section-header sh-section">{escape(stripped)}</h3>'

    # Section headers — 2 visual styles based on word count
    if is_section_header(stripped):
        wc = len(stripped.split())
        sh_cls = 'sh-section' if wc >= 8 else 'sh-standard'
        return f'<h3 class="section-header {sh_cls}">{escape(stripped)}</h3>'

    t = escape(stripped)

    # Tier badges
    t = re.sub(r'\bT1\b', '<span class="badge t1">T1</span>', t)
    t = re.sub(r'\bT2\b', '<span class="badge t2">T2</span>', t)
    t = re.sub(r'\bT3\b', '<span class="badge t3">T3</span>', t)
    t = re.sub(r'\bT4\b', '<span class="badge t4">T4</span>', t)

    # Observation references
    t = re.sub(r'Observation\s+#(\d+)', r'<span class="obs-ref">Observation #\1</span>', t, flags=re.IGNORECASE)

    # Five Cs references
    for c_word in ['Context', 'Clusters', 'Congruence', 'Consistency', 'Culture']:
        t = re.sub(rf'\b({c_word})\b(?=[^<]*(?:<|$))', rf'<span class="five-c">\1</span>', t, count=1)

    # Inline margin icon — float into outer margin
    icon_html = ''
    tl = stripped.lower()
    if any(w in tl for w in ['posture', 'stance', 'shoe', 'handedness', 'physical', 'body language', 'clothing', 'gait', 'grip']):
        icon_html = _svg_bp()
    elif any(w in tl for w in ['personality', 'character', 'profile', 'behavioral style', 'disc', 'introvert', 'extrovert']):
        icon_html = _svg_cr()
    elif any(w in tl for w in ['verbal', 'speech', 'words', 'vocal', 'tone of voice', 'language pattern', 'phrasing']):
        icon_html = _svg_vs()
    elif any(w in tl for w in ['motivation', 'compliance', 'action', 'decision', 'drive', 'goal-oriented', 'directive']):
        icon_html = _svg_am()
    # Bold inline "Label:" openers — short defined terms at the start of a paragraph
    # Matches 1–7 word phrase followed by colon (e.g. "For the D-type:", "THE CLAIM:", "How it helps your performances:")
    t = re.sub(
        r'^(<[^>]+>)*([A-Z][A-Za-z\s\'\-,/]{2,60}:)(?=\s)',
        lambda m: (m.group(1) or '') + f'<strong>{m.group(2)}</strong>',
        t
    )
    t = _apply_bold(t)
    return f'<p>{icon_html}{t}</p>'


def is_tier_definition(text):
    """Detect T1-T4 tier definition lines like 'T1 — Physical Evidence'."""
    stripped = text.strip()
    m = re.match(r'^T([1-4])\s*[\u2014\u2013\-]+\s*(.+)$', stripped)
    return m

def gen_glossary_entry(num, term, definition):
    """Render a single glossary entry as a definition card."""
    return (
        f'<div class="gloss-entry">'
        f'<div class="gloss-head">'
        f'<span class="gloss-num">{escape(str(num))}</span>'
        f'<span class="gloss-term">{escape(term)}</span>'
        f'</div>'
        f'<p class="gloss-def">{escape(definition)}</p>'
        f'</div>'
    )


def gen_principle_card(num, body):
    """Render one of the Four Principles of Translation as a numbered card."""
    # Split first sentence as the title punch
    first, _, rest = body.partition('. ')
    title = first.rstrip('.')
    return (
        f'<div class="principle-card">'
        f'<div class="pc-num">{num:02d}</div>'
        f'<div class="pc-body">'
        f'<p class="pc-title">{escape(title)}.</p>'
        f'<p class="pc-rest">{escape(rest.strip())}</p>'
        f'</div>'
        f'</div>'
    ) if rest.strip() else (
        f'<div class="principle-card">'
        f'<div class="pc-num">{num:02d}</div>'
        f'<div class="pc-body"><p class="pc-title">{escape(body)}</p></div>'
        f'</div>'
    )


COLD_WARM_HOT_HTML = '''<div class="cwh-spectrum">
  <div class="cwh-item cwh-cold">
    <div class="cwh-label">COLD</div>
    <div class="cwh-name">Pure Cold Reading</div>
    <div class="cwh-desc">No prior knowledge. Works entirely from observation, context, and the Forer effect.</div>
  </div>
  <div class="cwh-arrow">&#8594;</div>
  <div class="cwh-item cwh-warm">
    <div class="cwh-label">WARM</div>
    <div class="cwh-name">Warm Reading</div>
    <div class="cwh-desc">Live observation. Using behavioral signals the participant has already broadcast. Most real readings are here.</div>
  </div>
  <div class="cwh-arrow">&#8594;</div>
  <div class="cwh-item cwh-hot">
    <div class="cwh-label">HOT</div>
    <div class="cwh-name">Hot Reading</div>
    <div class="cwh-desc">Research-based. Specific knowledge gathered in advance before the participant arrives.</div>
  </div>
</div>'''


FRUIT_TO_FANG_HTML = '''<div class="ftf-card">
  <div class="ftf-header">
    <div class="ftf-title">FRUIT TO FANG</div>
    <div class="ftf-subtitle">Propless Method: Using the Eyes to Discern a Vowel in a Word</div>
  </div>
  <p class="ftf-intro">I call this process Fruit to Fang because it begins in an easy category and pivots into a wilder one, allowing the difficulty of the search itself to reveal the hidden vowel. What looks like a casual broadening of options is actually a narrowing device. The participant believes the field has expanded. In reality, the way they search through that expansion gives the game away.</p>
  <p class="ftf-method-note"><em>The performer is not reading a fixed signal here. He is reading the ease or difficulty of retrieval and using that change in search effort to reduce the field.</em></p>
  <div class="ftf-table">
    <div class="ftf-row ftf-head">
      <div class="ftf-cell">What you observe</div>
      <div class="ftf-cell">What it usually suggests</div>
      <div class="ftf-cell">What you do next</div>
      <div class="ftf-cell">What it may indicate</div>
    </div>
    <div class="ftf-row">
      <div class="ftf-cell">Fruit comes immediately</div>
      <div class="ftf-cell">Easy category access, common answer</div>
      <div class="ftf-cell">Stay with the fruit path</div>
      <div class="ftf-cell ftf-vowel">Likely A or O</div>
    </div>
    <div class="ftf-row">
      <div class="ftf-cell">Visible search, no fruit arrives</div>
      <div class="ftf-cell">Harder category access</div>
      <div class="ftf-cell">Offer the animal option</div>
      <div class="ftf-cell ftf-vowel">Less likely A or O</div>
    </div>
    <div class="ftf-row">
      <div class="ftf-cell">Animal arrives immediately after the shift</div>
      <div class="ftf-cell">Easy animal retrieval once redirected</div>
      <div class="ftf-cell">Move toward a confident reveal</div>
      <div class="ftf-cell ftf-vowel">E &mdash; Eagle / Elephant</div>
    </div>
    <div class="ftf-row">
      <div class="ftf-cell">Animal takes a little longer</div>
      <div class="ftf-cell">Narrower, less common animal search</div>
      <div class="ftf-cell">Use a playful test statement</div>
      <div class="ftf-cell ftf-vowel">I</div>
    </div>
    <div class="ftf-row">
      <div class="ftf-cell">Strong surprise when you dismiss it as not a real animal</div>
      <div class="ftf-cell">They likely chose something unusual or imaginary</div>
      <div class="ftf-cell">Lean into the reveal</div>
      <div class="ftf-cell ftf-vowel">U</div>
    </div>
    <div class="ftf-row">
      <div class="ftf-cell">Mild confusion when challenged</div>
      <div class="ftf-cell">They chose something borderline or category-fuzzy</div>
      <div class="ftf-cell">Reframe and refine</div>
      <div class="ftf-cell ftf-vowel">Iguana or another unusual choice</div>
    </div>
  </div>
  <div class="ftf-flow">
    <div class="ftf-flow-title">HOW SEARCH EFFORT NARROWS THE FIELD</div>
    <div class="ftf-flow-body">
      <div class="ftf-node ftf-node-start">Think of the first vowel</div>
      <div class="ftf-arrow">&#8595;</div>
      <div class="ftf-node">Think of a fruit with that letter</div>
      <div class="ftf-arrow">&#8595;</div>
      <div class="ftf-branch">
        <div class="ftf-branch-item ftf-yes"><strong>Fruit comes immediately</strong><br><span class="ftf-note">likely common fruit</span><br>think <span class="ftf-vowel-inline">A / O</span><br><span class="ftf-note">apple or orange</span></div>
        <div class="ftf-branch-mid">Did it come easily?</div>
        <div class="ftf-branch-item ftf-no"><strong>No fruit / visible search</strong><br><span class="ftf-note">offer the animal option</span></div>
      </div>
      <div class="ftf-arrow">&#8595;</div>
      <div class="ftf-branch">
        <div class="ftf-branch-item ftf-yes"><strong>Animal comes immediately</strong><br>think <span class="ftf-vowel-inline">E</span><br><span class="ftf-note">Eagle / Elephant &mdash; ask if it feels like a large animal; confident yes confirms elephant</span></div>
        <div class="ftf-branch-mid">Animal ease?</div>
        <div class="ftf-branch-item ftf-no"><strong>Animal takes longer</strong><br>think <span class="ftf-vowel-inline">I / U</span><br><span class="ftf-note">watch quality of search &amp; reaction to challenge</span></div>
      </div>
      <div class="ftf-arrow">&#8595;</div>
      <div class="ftf-node ftf-node-test">Playful challenge: <em>&ldquo;That&rsquo;s not a real animal.&rdquo;</em></div>
      <div class="ftf-arrow">&#8595;</div>
      <div class="ftf-branch">
        <div class="ftf-branch-item ftf-yes"><strong>Mild confusion</strong><br>likely <span class="ftf-vowel-inline">I</span><br><span class="ftf-note">iguana or another borderline answer</span></div>
        <div class="ftf-branch-mid">Reaction?</div>
        <div class="ftf-branch-item ftf-no"><strong>Strong surprise</strong><br>likely <span class="ftf-vowel-inline">U</span><br><span class="ftf-note">unicorn &mdash; watch for shoulder shrug or head wobble as social protection</span></div>
      </div>
      <div class="ftf-arrow">&#8595;</div>
      <div class="ftf-node ftf-node-note"><strong>Very long search before settling</strong><br><span class="ftf-note">points toward <span class="ftf-vowel-inline">U</span> rather than <span class="ftf-vowel-inline">I</span> &mdash; the mind is reaching for a less natural answer</span></div>
    </div>
  </div>
</div>'''

def gen_t4_signal_card(signal_name, claim, research, valid):
    """Render an Appendix A1 T4 signal card with claim/research/valid sections."""
    return (
        f'<div class="t4-signal-card">'
        f'<div class="t4s-header"><span class="t4s-badge">T4</span><span class="t4s-name">{escape(signal_name)}</span></div>'
        f'<div class="t4s-section t4s-claim">'
        f'<div class="t4s-label">THE CLAIM</div>'
        f'<p class="t4s-body">{escape(claim)}</p>'
        f'</div>'
        f'<div class="t4s-section t4s-research">'
        f'<div class="t4s-label">THE RESEARCH</div>'
        f'<p class="t4s-body">{escape(research)}</p>'
        f'</div>'
        f'<div class="t4s-section t4s-valid">'
        f'<div class="t4s-label">WHAT REMAINS VALID</div>'
        f'<p class="t4s-body">{escape(valid)}</p>'
        f'</div>'
        f'</div>'
    )


def gen_modality_card(modality, signals_text):
    """Render Visual/Auditory/Kinesthetic Signals as a compact reference card."""
    colors = {
        'Visual':       ('#1A8FA8', 'rgba(26,143,168,.08)'),
        'Auditory':     ('#6B52A0', 'rgba(107,82,160,.08)'),
        'Kinesthetic':  ('#4BAA72', 'rgba(75,170,114,.08)'),
    }
    color, bg = colors.get(modality, ('#C9A84C', 'rgba(201,168,76,.08)'))
    # Parse the signals text into labeled fields
    fields_html = ''
    for chunk in signals_text.split('. '):
        chunk = chunk.strip().rstrip('.')
        if not chunk:
            continue
        if ':' in chunk:
            label, _, value = chunk.partition(':')
            fields_html += (
                f'<div class="mod-field">'
                f'<span class="mod-label">{escape(label.strip())}</span>'
                f'<span class="mod-value">{escape(value.strip())}</span>'
                f'</div>'
            )
        else:
            fields_html += (
                f'<div class="mod-field">'
                f'<span class="mod-label"></span>'
                f'<span class="mod-value mod-note">{escape(chunk)}</span>'
                f'</div>'
            )
    return (
        f'<div class="modality-card" style="--mod-color:{color};--mod-bg:{bg}">'
        f'<div class="mod-name">{escape(modality)}</div>'
        f'<div class="mod-fields">{fields_html}</div>'
        f'</div>'
    )


def gen_reading_line_card(disc_type, context, body_text):
    """Render a behavioral reading line card (IF YOU SEE / LINE)."""
    context_cls = 'rl-stage' if 'stage' in context.lower() or 'theatrical' in context.lower() else 'rl-closeup'
    context_label = 'STAGE / THEATRICAL' if context_cls == 'rl-stage' else 'STROLLING / CLOSE-UP'
    # Parse IF YOU SEE and LINE from body
    see_html = ''
    line_html = ''
    see_m = re.search(r'IF YOU SEE:\s*(.+?)(?:\.\s*LINE:|LINE:|$)', body_text, re.IGNORECASE)
    line_m = re.search(r"LINE:\s*['\u2018\u201c](.+?)['\u2019\u201d]", body_text, re.IGNORECASE)
    if not line_m:
        line_m = re.search(r"LINE:\s*(.+)$", body_text, re.IGNORECASE)
    if see_m:
        signals = [s.strip() for s in see_m.group(1).split('+') if s.strip()]
        chips = ''.join(f'<span class="rl-signal">{escape(s)}</span>' for s in signals)
        see_html = f'<div class="rl-signals">{chips}</div>'
    if line_m:
        line_html = f'<p class="rl-line"><strong>&ldquo;{escape(line_m.group(1).strip())}&rdquo;</strong></p>'
    return (
        f'<div class="reading-line-card {context_cls}">'
        f'<div class="rl-head">'
        f'<span class="rl-type">{escape(disc_type)}</span>'
        f'<span class="rl-context">{context_label}</span>'
        f'</div>'
        f'{see_html}'
        f'{line_html}'
        f'</div>'
    )


def gen_tier_card(tier_num, tier_name, body_text):
    """Generate a textbook-style tier definition card."""
    tier_class = f't{tier_num}-block'
    badge_class = f't{tier_num}'
    return f'''<div class="tier-block {tier_class}">
  <div class="tier-header">
    <span class="badge {badge_class}">T{tier_num}</span>
    <span class="tier-name">{escape(tier_name)}</span>
  </div>
  <div class="tier-body"><p>{escape(body_text)}</p></div>
</div>'''

def gen_concept_box(title, body_lines, highlight=''):
    """Generate a concept callout box (textbook-style)."""
    body_html = ''.join(f'<p>{escape(line)}</p>' for line in body_lines if line.strip())
    highlight_html = f'<p class="concept-highlight">{escape(highlight)}</p>' if highlight else ''
    return f'''<div class="concept-box">
  <div class="concept-label">KEY CONCEPT</div>
  <div class="concept-title">{escape(title)}</div>
  <div class="concept-body">{body_html}{highlight_html}</div>
</div>'''

def gen_context_card(label, body_text):
    """Generate a context application card (Stage, Strolling, etc)."""
    return f'''<div class="context-card">
  <div class="context-label">{escape(label.upper())}</div>
  <p>{escape(body_text)}</p>
</div>'''

def gen_error_card(label, body_text):
    """Generate an observer error card."""
    return f'''<div class="error-card">
  <div class="error-label">{escape(label.upper())}</div>
  <p>{escape(body_text)}</p>
</div>'''


def build_chapter_body(section, global_para_count):
    """Build the full body of a chapter with all design elements."""
    content = section.get('content', [])
    chapter_num = section.get('chapter_num', 0)
    part_num = section.get('part_num', 0)
    chapter_key = section.get('chapter_key', '')
    title = section.get('title', '')

    parts = []
    paragraphs = [line for line in content if line.strip()]
    if not paragraphs:
        return '', global_para_count

    # Running header
    if chapter_num > 0:
        header_text = f'CHAPTER {chapter_num}\u2003\u2014\u2003{title.upper()}'
    elif chapter_num == 0:
        header_text = 'INTRODUCTION'
    else:
        header_text = title.upper()

    parts.append(f'<header class="running-header"><span>THE ARCHITECTURE OF WONDER</span><span>{escape(header_text)}</span></header>')

    # First paragraph with drop cap
    first = escape(paragraphs[0].strip())
    if len(first) > 2:
        parts.append(f'<p class="first-para"><span class="drop-cap">{first[0]}</span>{first[1:]}</p>')
    else:
        parts.append(f'<p>{first}</p>')

    # ── FIVE Cs FRAMEWORK — injected inline after first mention (see loop below) ──
    five_cs_injected = False
    # ── DISC CHART — injected before first D — DIRECT entry ──
    disc_injected = False
    # ── NOVELTY TECHNIQUES — injected after trigger line in Ch5 ──
    novelty_injected = False
    # ── SPEECH PATTERNS — injected after trigger line in Ch25 ──
    speech_injected = False
    # ── TENSION SIGNALS — injected after trigger line in Ch3 ──
    tension_injected = False
    # ── THREE OPENERS — injected after Social Opener body in Cold Reading ch ──
    three_openers_injected = False
    # ── BEHAVIORAL READING DEF — injected after bridge paragraph in Ch10 ──
    behavioral_def_injected = False
    # ── 10-SECOND SCAN — injected after closing sentence in Ch7 ──
    scan_injected = False
    # ── CHAIN FLOW — injected after "First you collect." in Ch7 ──
    chain_injected = False
    # ── DISC OPENING BRIDGE — injected after Ch8 opening paragraph ──
    disc_opening_injected = False
    # ── DISC CLUSTER BOXES — injected before "Reading DISC Blends" in Ch8 ──
    disc_cluster_injected = False
    # ── PERFORMANCE READ PANEL components ──
    five_things_injected = False
    signal_table_injected = False
    mini_scenarios_injected = False
    cheat_sheet_injected = False

    # Track for element insertion
    total = len(paragraphs)
    spotlight_done = False
    wyajd_done = False
    pull_quote_done = False
    _toolkit_section_open = False
    _crt_buffer = []          # rows buffered within current toolkit section
    _current_section_id = ''  # id of open toolkit section
    pi_count = 0
    pi_idx = global_para_count % len(PATTERN_INTERRUPTS)

    i = 1
    while i < len(paragraphs):
        para = paragraphs[i]
        global_para_count += 1
        stripped = para.strip()

        # ── EXPLICIT PATTERN INTERRUPT TRIGGERS ──
        # ── EXPLICIT KEY PRINCIPLE CALLOUT ──
        if stripped == 'KEY PRINCIPLE' and i + 1 < len(paragraphs):
            body_text = paragraphs[i + 1].strip()
            parts.append(gen_spotlight(escape(body_text)))
            spotlight_done = True
            i += 2
            continue

        if stripped == 'LEAKAGE_HIERARCHY':
            parts.append(LEAKAGE_HIERARCHY_HTML)
            i += 1
            continue

        if stripped == 'FIVE_THINGS_PANEL':
            parts.append(FIVE_THINGS_PANEL_HTML)
            five_things_injected = True
            i += 1
            continue

        if stripped == 'SIGNAL_TABLE':
            parts.append(SIGNAL_TABLE_HTML)
            signal_table_injected = True
            i += 1
            continue

        if stripped == 'SITCOM_TABLE':
            parts.append(SITCOM_TABLE_HTML)
            i += 1
            continue

        if stripped == 'DECODE_PANEL':
            parts.append(DECODE_PANEL_HTML)
            i += 1
            continue

        if stripped == 'CH18_DIAGNOSTIC_PANEL':
            parts.append(CH18_DIAGNOSTIC_PANEL_HTML)
            i += 1
            continue

        if stripped == 'CH18_IFYRE_PANEL':
            parts.append(CH18_IFYRE_PANEL_HTML)
            i += 1
            continue

        if stripped == 'CH19_IFYRE_PANEL':
            parts.append(CH19_IFYRE_PANEL_HTML)
            i += 1
            continue

        if stripped == 'PSYFORCE_CATEGORIES_TBC':
            parts.append(PSYFORCE_CATEGORIES_TBC_HTML)
            i += 1
            continue

        if stripped == 'PSYFORCE_STRENGTH_PANEL':
            parts.append(PSYFORCE_STRENGTH_PANEL_HTML)
            i += 1
            continue

        if stripped == 'PSYFORCE_CONSTRUCT_PANEL':
            parts.append(PSYFORCE_CONSTRUCT_PANEL_HTML)
            i += 1
            continue

        if stripped == 'PSYFORCE_MAP_PANEL':
            parts.append(PSYFORCE_MAP_PANEL_HTML)
            i += 1
            continue

        if stripped == 'PERF_ARCH_FRAMEWORK_SVG':
            parts.append(PERF_ARCH_FRAMEWORK_SVG_HTML)
            i += 1
            continue

        if stripped == 'MINI_SCENARIOS':
            parts.append(MINI_SCENARIOS_HTML)
            mini_scenarios_injected = True
            i += 1
            continue

        if stripped == 'CHEAT_SHEET':
            parts.append(CHEAT_SHEET_HTML)
            cheat_sheet_injected = True
            i += 1
            continue

        if stripped == 'CREDIBILITY_SEQUENCE':
            parts.append(CREDIBILITY_SEQUENCE_HTML)
            i += 1
            continue

        if stripped == 'PERFORMANCE_MATRIX':
            parts.append(PERFORMANCE_MATRIX_HTML)
            i += 1
            continue

        if stripped == 'PATTERN_INTERRUPT_40PCT':
            pi_data = next((p for p in PATTERN_INTERRUPTS if p['number'] == '40%'), None)
            if pi_data:
                parts.append(gen_pattern_interrupt(pi_data))
            i += 1
            continue

        # ── OBSERVATION TABLE (flat 5-column format from DOCX) ──
        if stripped == '#' and i + 4 < len(paragraphs):
            next4 = [paragraphs[i+j].strip() for j in range(1, 5)]
            if next4 == ['OBSERVATION', 'WHAT IT TELLS YOU', 'TIER', 'USE']:
                rows = []
                j = i + 5
                while j + 4 < len(paragraphs):
                    num = paragraphs[j].strip()
                    if not re.match(r'^\d{1,2}$', num):
                        break
                    obs  = paragraphs[j+1].strip()
                    what = paragraphs[j+2].strip()
                    tier = paragraphs[j+3].strip()
                    use  = paragraphs[j+4].strip()
                    rows.append((num, obs, what, tier, use))
                    j += 5
                if rows:
                    global_para_count += len(rows) * 5 + 5
                    parts.append(gen_observation_table(rows))
                    i = j
                    continue

        # ── DISC TYPE CARDS (D — DIRECT, I — INFLUENTIAL, etc.) ──
        disc_type_m = re.match(r'^([DISC]) — ([A-Z]+)$', stripped)
        if disc_type_m and i + 1 < len(paragraphs):
            # Inject DISC chart before the first card
            if not disc_injected:
                parts.append(DISC_HTML)
                disc_injected = True
            body_para = paragraphs[i + 1].strip()
            parts.append(gen_disc_type_card(disc_type_m.group(1), disc_type_m.group(2), body_para))
            i += 2
            global_para_count += 2
            continue

        # ── DISC BLEND CARDS (D/C Blend, I/S Blend, etc.) ──
        disc_blend_m = re.match(r'^([DISC]/[DISC]) Blend$', stripped)
        if disc_blend_m and i + 1 < len(paragraphs):
            body_para = paragraphs[i + 1].strip()
            parts.append(gen_disc_blend_card(disc_blend_m.group(1), body_para))
            i += 2
            global_para_count += 2
            continue

        # ── VIDEO EMBEDS ──
        # Pattern: "VIDEO EMBED :: FILE_ID :: Label :: Caption"
        if stripped.startswith('VIDEO EMBED :: '):
            parts_ve = stripped.split(' :: ', 3)
            if len(parts_ve) == 4:
                _, file_id, label, caption = parts_ve
                parts.append(gen_video_embed(file_id.strip(), label.strip(), caption.strip()))
                i += 1
                global_para_count += 1
                continue

        # ── VOLUNTEER TYPE CARDS ──
        if stripped in _VOLUNTEER_COLORS and i + 1 < len(paragraphs):
            body_para = paragraphs[i + 1].strip()
            parts.append(gen_volunteer_card(stripped, body_para))
            i += 2
            global_para_count += 2
            continue

        # ── VOLUNTEER SELECTION MATRIX ENTRIES ──
        vm_m = re.match(r'^(High|Low) Confidence \+ (High|Low) Suggestibility$', stripped)
        if vm_m and i + 1 < len(paragraphs):
            body_para = paragraphs[i + 1].strip()
            parts.append(gen_volunteer_matrix_entry(stripped, body_para))
            i += 2
            global_para_count += 2
            continue

        # ── SIX-CATEGORY RADAR CARDS ──
        # Pattern: "01 — Category Name" followed by "signal [T#] · signal [T#] ... Insight."
        radar_m = re.match(r'^(\d{2}) — (.+)$', stripped)
        if radar_m and i + 1 < len(paragraphs):
            next_para = paragraphs[i + 1].strip()
            if ' · ' in next_para and '[T' in next_para:
                parts.append(gen_radar_category(radar_m.group(1), radar_m.group(2), next_para))
                i += 2
                global_para_count += 2
                continue

        # ── BTE CLUSTER SIGNAL ENTRIES ──
        # Pattern: "Signal Name (Code). DRS X.X. Description."
        # or:      "Signal Name (Code) — DRS X.X. Description."
        bte_m = re.match(
            r'^([A-Z][A-Za-z ]+)\s*\(([A-Z][a-z]{0,4})\)[.\s—-]+DRS\s+([\d.]+)[.\s]+(.+)$',
            stripped
        )
        if bte_m:
            parts.append(gen_bte_signal(
                bte_m.group(1).strip(),
                bte_m.group(2).strip(),
                bte_m.group(3).strip(),
                bte_m.group(4).strip()
            ))
            i += 1
            global_para_count += 1
            continue

        # ── SEVEN STAGES ARC CARDS (01 · PRIME … 07 · EMBED) ──
        stage_m = re.match(r'^(0[1-7]) · ([A-Z]+)$', stripped)
        if stage_m and i + 1 < len(paragraphs):
            body_para = paragraphs[i + 1].strip()
            parts.append(gen_stage_card(stage_m.group(1), stage_m.group(2), body_para))
            i += 2
            global_para_count += 2
            continue

        # ── PERFORMANCE CHECKLIST SECTIONS (ALL-CAPS heading + bullet text) ──
        checklist_heads = {
            'PRE-SHOW PRIMING', 'ATTENTION ARCHITECTURE', 'TENSION AND RELEASE',
            'BEHAVIORAL PROFILING', 'MEMORY ENCODING',
            'BEHAVIORS THAT READ AS SAFE AND STRONG'
        }
        if stripped in checklist_heads and i + 1 < len(paragraphs):
            bullet_para = paragraphs[i + 1].strip()
            if ' · ' in bullet_para:
                parts.append(gen_checklist_section(stripped, bullet_para))
                i += 2
                global_para_count += 2
                continue

        # ── CERTAINTY FRAME CARDS (Soft/Moderate/Strong/Pinpoint Frame) ──
        if stripped in _CERTAINTY_FRAME_META and i + 1 < len(paragraphs):
            body_para = paragraphs[i + 1].strip()
            parts.append(gen_certainty_frame(stripped, body_para))
            i += 2
            global_para_count += 2
            continue

        # ── WARNING CALLOUTS (Common Misread, When This Read Misses) ──
        _warning_callout_triggers = {'Common Misread', 'When This Read Misses:'}
        if stripped in _warning_callout_triggers and i + 1 < len(paragraphs):
            body_para = paragraphs[i + 1].strip()
            parts.append(gen_warning_callout(stripped, body_para))
            i += 2
            global_para_count += 2
            continue

        # ── RULE CALLOUTS (Pace-Lead Ratio, X Check, X Structure) ──
        _rule_callout_triggers = {
            'Pace-Lead Ratio', 'Presupposition Check', 'Yes Set Structure',
        }
        if stripped in _rule_callout_triggers and i + 1 < len(paragraphs):
            body_para = paragraphs[i + 1].strip()
            parts.append(gen_rule_callout(stripped, body_para))
            i += 2
            global_para_count += 2
            continue

        # ── TIER DEFINITION CARDS ──
        tier_match = is_tier_definition(stripped)
        if tier_match:
            tier_num = tier_match.group(1)
            tier_name = tier_match.group(2).strip()
            # Next paragraph is the body
            body = ''
            if i + 1 < len(paragraphs):
                body = paragraphs[i + 1].strip()
                i += 1
                global_para_count += 1
            parts.append(gen_tier_card(tier_num, tier_name, body))
            i += 1
            continue

        # ── CONCEPT CALLOUT BOXES ──
        # Three-Signal Rule, Foundation: Baseline First, etc.
        concept_triggers = {
            'The Three-Signal Rule': 'CORE RULE',
            'The Foundation: Baseline First': 'FOUNDATION',
            'The Leakage Window': 'KEY CONCEPT',
            'High-Yield Baseline Signals': 'KEY CONCEPT',
        }
        matched_concept = None
        for trigger, label in concept_triggers.items():
            if stripped == trigger or stripped.startswith(trigger):
                matched_concept = (trigger, label)
                break

        if matched_concept:
            concept_title = matched_concept[0]
            # Collect following paragraphs as body (until next section header or break)
            body_lines = []
            highlight = ''
            j = i + 1
            while j < len(paragraphs):
                next_stripped = paragraphs[j].strip()
                if is_section_header(next_stripped) or is_section_break(next_stripped) or is_tier_definition(next_stripped):
                    break
                if not next_stripped:
                    j += 1
                    continue
                body_lines.append(next_stripped)
                j += 1
                global_para_count += 1
                # Cap at 3 body paragraphs for the callout
                if len(body_lines) >= 3:
                    break
            # Use last line as highlight if it's short and punchy
            if body_lines and len(body_lines[-1]) < 120:
                highlight = body_lines.pop()
            parts.append(gen_concept_box(concept_title, body_lines, highlight))
            i = j
            continue

        # ── CONTEXT APPLICATION CARDS ──
        context_triggers = ['Stage Context', 'Strolling Context']
        matched_context = None
        for trigger in context_triggers:
            if stripped == trigger:
                matched_context = trigger
                break

        if matched_context:
            body = ''
            if i + 1 < len(paragraphs):
                body = paragraphs[i + 1].strip()
                i += 1
                global_para_count += 1
            parts.append(gen_context_card(matched_context, body))
            i += 1
            continue

        # ── COMMON OBSERVER ERRORS ──
        error_triggers = [
            'Acting on a Single Signal.',
            'Ignoring the Baseline.',
            'Confirmation Bias.',
            'Cultural Projection.',
            'Conflating Observation with Lie Detection.',
        ]
        matched_error = None
        for trigger in error_triggers:
            if stripped.startswith(trigger):
                matched_error = trigger.rstrip('.')
                break

        if matched_error:
            # The rest of the line after the trigger is the body
            body = stripped[len(matched_error) + 1:].strip() if len(stripped) > len(matched_error) + 1 else ''
            parts.append(gen_error_card(matched_error, body))
            i += 1
            continue

        # Auto pattern interrupts DISABLED — use explicit PATTERN_INTERRUPT_40PCT
        # trigger in the manuscript at natural section breaks instead.

        # "What You Just Did" at ~65% through chapter
        if not wyajd_done and chapter_num in WHAT_YOU_JUST_DID and i > total * 0.6:
            parts.append(gen_wyajd(WHAT_YOU_JUST_DID[chapter_num]))
            wyajd_done = True

        # ── FRUIT TO FANG APPLICATION ──
        if stripped == 'FRUIT TO FANG APPLICATION':
            parts.append(FRUIT_TO_FANG_HTML)
            i += 1
            global_para_count += 1
            continue

        # ── COLD-WARM-HOT SPECTRUM ──
        if stripped == 'The Cold-Warm-Hot Spectrum':
            parts.append(f'<h3 class="section-header sh-standard">{escape(stripped)}</h3>')
            parts.append(COLD_WARM_HOT_HTML)
            i += 1
            continue

        # ── FOUR PRINCIPLES OF TRANSLATION (collect 4 paras after header) ──
        if stripped == 'The Four Principles of Translation':
            parts.append(f'<h3 class="section-header sh-standard">{escape(stripped)}</h3>')
            j = i + 1
            pcount = 0
            while j < len(paragraphs) and pcount < 4:
                nxt = paragraphs[j].strip()
                if nxt:
                    parts.append(gen_principle_card(pcount + 1, nxt))
                    global_para_count += 1
                    pcount += 1
                j += 1
            i = j
            continue

        # ── T4 SIGNAL CARDS / TABLE (SIGNAL N — Name) ──
        _t4_m = re.match(r'^SIGNAL\s+(\d+)\s*[\u2014\u2013\-]+\s*(.+)$', stripped)
        if _t4_m and i + 3 < len(paragraphs):
            sig_num = int(_t4_m.group(1))
            # In Ch7: inject full T4 table on signal 1, skip all 4 signal blocks
            if chapter_num == 7:
                if sig_num == 1:
                    parts.append(gen_t4_table())
                # Fast-forward past this signal's CLAIM/RESEARCH/VALID content
                j = i + 1
                while j < len(paragraphs):
                    nxt = paragraphs[j].strip()
                    # Stop at next SIGNAL marker or a non-T4 section header
                    if re.match(r'^SIGNAL\s+\d+', nxt):
                        break
                    if is_section_header(nxt) and not re.match(r'^(THE CLAIM|THE RESEARCH|WHAT REMAINS)', nxt, re.IGNORECASE):
                        break
                    j += 1
                global_para_count += (j - i)
                i = j
                continue
            # All other chapters (appendix): render detailed card as before
            sig_name = _t4_m.group(2).strip()
            claim = research = valid = ''
            j = i + 1
            while j < len(paragraphs):
                nxt = paragraphs[j].strip()
                if re.match(r'^THE CLAIM:?', nxt, re.IGNORECASE):
                    claim = nxt.partition(':')[2].strip() if ':' in nxt else ''
                    j += 1
                    while j < len(paragraphs):
                        cont = paragraphs[j].strip()
                        if re.match(r'^THE RESEARCH:?|^WHAT REMAINS', cont, re.IGNORECASE):
                            break
                        if cont:
                            claim += ' ' + cont
                        j += 1
                    continue
                if re.match(r'^THE RESEARCH:?', nxt, re.IGNORECASE):
                    research = nxt.partition(':')[2].strip() if ':' in nxt else ''
                    j += 1
                    while j < len(paragraphs):
                        cont = paragraphs[j].strip()
                        if re.match(r'^WHAT REMAINS', cont, re.IGNORECASE):
                            break
                        if cont:
                            research += ' ' + cont
                        j += 1
                    continue
                if re.match(r'^WHAT REMAINS VALID:?', nxt, re.IGNORECASE):
                    valid = nxt.partition(':')[2].strip() if ':' in nxt else ''
                    j += 1
                    while j < len(paragraphs):
                        cont = paragraphs[j].strip()
                        if re.match(r'^SIGNAL\s+\d+', cont, re.IGNORECASE):
                            break
                        if cont:
                            valid += ' ' + cont
                        j += 1
                    break
                j += 1
            global_para_count += (j - i)
            parts.append(gen_t4_signal_card(sig_name, claim, research, valid))
            i = j
            continue

        # ── MODALITY SIGNAL CARDS (Visual/Auditory/Kinesthetic Signals) ──
        _modality_triggers = {'Visual Signals', 'Auditory Signals', 'Kinesthetic Signals'}
        if stripped in _modality_triggers and i + 1 < len(paragraphs):
            modality = stripped.replace(' Signals', '')
            body_para = paragraphs[i + 1].strip()
            parts.append(gen_modality_card(modality, body_para))
            i += 2
            global_para_count += 2
            continue

        # ── BEHAVIORAL READING LINE CARDS (D-Type — Stage/Strolling etc.) ──
        _rl_ctx_m = re.match(
            r'^(.+?)\s*[\u2014\u2013\-]+\s*(Stage/Strolling|Close-Up/Theatrical)$',
            stripped, re.IGNORECASE
        )
        if _rl_ctx_m and i + 1 < len(paragraphs):
            disc_type = _rl_ctx_m.group(1).strip()
            context   = _rl_ctx_m.group(2).strip()
            body_para = paragraphs[i + 1].strip()
            if 'IF YOU SEE' in body_para.upper() or 'LINE:' in body_para.upper():
                parts.append(gen_reading_line_card(disc_type, context, body_para))
                i += 2
                global_para_count += 2
                continue

        # ── FORCES INTRO DOCTRINE BLOCK ──
        # "Five forces reliably activate this system." + next line = pill list
        if stripped == 'Five forces reliably activate this system.' and i + 1 < len(paragraphs):
            forces_line = paragraphs[i + 1].strip()
            parts.append(gen_forces_intro(stripped, forces_line))
            i += 2
            global_para_count += 2
            continue

        # ── TOOLKIT SECTION BOX (open/close) ──
        if stripped.startswith('TOOLKIT_SECTION:'):
            name = stripped[len('TOOLKIT_SECTION:'):].strip()
            _id_map = {
                'Appearance':               'cr-appearance',
                'Movement and Posture':     'cr-movement',
                'Territory and Personal Space': 'cr-territory',
                'Social Confidence':        'cr-confidence',
                'Cognitive Processing':     'cr-cognitive',
                'Emotional Regulation':     'cr-emotional',
            }
            sec_id = _id_map.get(name, 'cr-' + name.lower().replace(' ', '-'))
            icon   = _SECTION_ICONS.get(name, '')
            # flush previous section buffer + close div
            if _toolkit_section_open:
                parts.append(gen_crt_table(_crt_buffer))
                _crt_buffer.clear()
                parts.append('</div></div>')
            _toolkit_section_open = True
            _current_section_id = sec_id
            icon_html = f'<span class="tks-icon">{icon}</span>' if icon else ''
            parts.append(
                f'<div id="{sec_id}" class="toolkit-section">'
                f'<div class="tks-header">{icon_html}<span class="tks-name">{escape(name)}</span></div>'
                f'<div class="tks-body">'
            )
            i += 1; global_para_count += 1; continue

        if stripped == 'TOOLKIT_SECTION_END':
            if _toolkit_section_open:
                parts.append(gen_crt_table(_crt_buffer))
                _crt_buffer.clear()
                parts.append('</div></div>')
                _toolkit_section_open = False
            i += 1; global_para_count += 1; continue

        # ── TOOLKIT NAVIGATION PANEL ──
        if stripped == 'TOOLKIT_NAV':
            parts.append(gen_toolkit_nav())
            parts.append(gen_feedback_signals_ref())
            i += 1; global_para_count += 1; continue

        # ── TOOLKIT SUMMARY TABLE ──
        if stripped == 'CR_SUMMARY_TABLE':
            parts.append(gen_cr_summary_table())
            i += 1; global_para_count += 1; continue

        # ── INVISIBLE ANCHOR for in-page navigation ──
        if stripped.startswith('CRANCHOR:'):
            anchor_id = stripped[len('CRANCHOR:'):].strip()
            parts.append(f'<span id="{escape(anchor_id)}" class="cr-anchor"></span>')
            i += 1; global_para_count += 1; continue

        # ── COLD READING TOOLKIT — "CRT: Cue | DISC | Context" followed by line paragraph ──
        if stripped.startswith('CRT:') and i + 1 < len(paragraphs):
            header = stripped[len('CRT:'):].strip()
            parts_h = [p.strip() for p in header.split('|')]
            cue_t  = parts_h[0] if len(parts_h) > 0 else ''
            disc_t = parts_h[1] if len(parts_h) > 1 else ''
            ctx_t  = parts_h[2] if len(parts_h) > 2 else ''
            line_t = paragraphs[i + 1].strip()
            _crt_buffer.append((cue_t, line_t, disc_t, ctx_t))
            i += 2; global_para_count += 2; continue

        # ── FEEDBACK CHART — standalone "FEEDBACK_CHART" trigger ──
        if stripped == 'FEEDBACK_CHART':
            parts.append(gen_feedback_chart())
            i += 1; global_para_count += 1; continue

        # ── SIX AREA RADAR CHART ──
        if stripped == 'SIX_AREA_RADAR':
            parts.append(gen_six_area_radar())
            i += 1; global_para_count += 1; continue

        # Spotlight box: find a good quote-like line at ~20-55% through
        if not spotlight_done and i > total * 0.2 and i < total * 0.55:
            if (stripped.startswith(('\u201c', '"', '\u2018')) and len(stripped) < 250 and len(stripped) > 30) or \
               (len(stripped) < 200 and len(stripped) > 35 and any(kw in stripped.lower() for kw in ['principle', 'key', 'rule', 'fundamental', 'critical', 'essential', 'never', 'always', 'the real', 'the most important', 'is not', 'does not', 'cannot'])):
                parts.append(gen_spotlight(escape(stripped)))
                spotlight_done = True
                i += 1
                continue

        # Pull quote: find a strong short statement at ~55-75%
        if not pull_quote_done and i > total * 0.55 and i < total * 0.75:
            if len(stripped) < 120 and len(stripped) > 30 and not is_section_header(stripped) and not is_section_break(stripped):
                if any(kw in stripped.lower() for kw in ['is not', 'is the', 'that is', 'the real', 'the most', 'every ', 'never ', 'always ']):
                    parts.append(gen_pull_quote(stripped))
                    pull_quote_done = True
                    i += 1
                    continue

        # ── MNEMONIC BLOCK — "MNEMONIC: ACRONYM — phrase" followed by "expansion. note" ──
        if stripped.startswith('MNEMONIC:') and i + 1 < len(paragraphs):
            header = stripped[len('MNEMONIC:'):].strip()
            # header format: "ACRONYM — phrase"
            if '\u2014' in header:
                acronym, _, phrase = header.partition('\u2014')
            elif ' - ' in header:
                acronym, _, phrase = header.partition(' - ')
            else:
                acronym, phrase = header, ''
            body = paragraphs[i + 1].strip()
            # Split body into expansion (first sentence up to period) and note (rest)
            if '. ' in body:
                expansion, _, note = body.partition('. ')
            else:
                expansion, note = body, ''
            parts.append(gen_mnemonic(acronym.strip(), phrase.strip(), expansion.strip(), note.strip()))
            i += 2
            global_para_count += 2
            continue

        # ── CM TAKEAWAY CARDS ──
        if stripped == 'CM Takeaway' and i + 1 < len(paragraphs):
            body = paragraphs[i + 1].strip()
            parts.append(gen_cm_takeaway(body))
            i += 2
            global_para_count += 2
            continue

        # ── ANTHEM & ARIA FIELD ADVICE CARDS ──
        if stripped.startswith('ANTHEM_ARIA:'):
            body = stripped[len('ANTHEM_ARIA:'):].strip()
            parts.append(gen_anthem_aria_card(body))
            i += 1
            global_para_count += 1
            continue

        # ── RECOVERY CARDS — "RECOVERY: Name | when text" followed by body paragraph ──
        if stripped.startswith('RECOVERY:') and i + 1 < len(paragraphs):
            header = stripped[len('RECOVERY:'):].strip()
            if '|' in header:
                name_part, when_part = header.split('|', 1)
            else:
                name_part, when_part = header, ''
            body_part = paragraphs[i + 1].strip()
            # Count recovery cards in this chapter to auto-number
            _rc_num = sum(1 for p in parts if 'recovery-card' in p) + 1
            parts.append(gen_recovery_card(_rc_num, name_part.strip(), when_part.strip(), body_part))
            i += 2
            global_para_count += 2
            continue

        # ── DEFINITION CARDS — "DEFCARD: Term" followed by definition paragraph ──
        if stripped.startswith('DEFCARD:') and i + 1 < len(paragraphs):
            term = stripped[len('DEFCARD:'):].strip()
            defn = paragraphs[i + 1].strip()
            parts.append(gen_def_card(term, defn))
            i += 2
            global_para_count += 2
            continue

        # ── NUMBERED CARDS — "N. Title" followed by body paragraph ──
        _num_m = re.match(r'^(\d+)\.\s+(.+)$', stripped)
        if _num_m and i + 1 < len(paragraphs):
            _body = paragraphs[i + 1].strip()
            if _body and not re.match(r'^\d+\.', _body):
                parts.append(gen_numbered_card(_num_m.group(1), _num_m.group(2), _body))
                i += 2
                global_para_count += 2
                continue

        # ── BULLET LIST — consecutive · prefixed lines ──
        if stripped.startswith('\u00b7') and stripped not in ('\u00b7 \u00b7 \u00b7', '\u00b7\u00b7\u00b7'):
            items = []
            while i < len(paragraphs):
                s = paragraphs[i].strip()
                if s.startswith('\u00b7') and s not in ('\u00b7 \u00b7 \u00b7', '\u00b7\u00b7\u00b7'):
                    item_text = s.lstrip('\u00b7').strip()
                    items.append(escape(item_text))
                    i += 1
                    global_para_count += 1
                else:
                    break
            li_html = '\n'.join(f'<li>{it}</li>' for it in items)
            parts.append(f'<ul class="book-list">{li_html}</ul>')
            continue

        processed = process_paragraph(para, part_num)
        if processed:
            parts.append(processed)

        # ── FIVE Cs GRAPHIC — inject after first "Context. Clusters. Congruence..." sentence ──
        if not five_cs_injected and stripped == 'Context. Clusters. Congruence. Consistency. Culture.':
            parts.append(FIVE_CS_HTML)
            five_cs_injected = True

        # ── NOVELTY TECHNIQUES — inject after trigger line in Ch5 ──
        if not novelty_injected and stripped == 'Violate the Format. The Deliberate Withhold. Name the Unnamed. Reframe the Familiar. Unexplained Specificity. Physical Novelty Anchors.':
            parts.append(NOVELTY_TECHNIQUES_HTML)
            novelty_injected = True

        # ── SPEECH PATTERNS — inject after trigger line in Ch25 ──
        if not speech_injected and stripped == 'Slow the Beginning. The Spontaneous Compliment. Future Memory Language. The Status Frame. Strategic Silence.':
            parts.append(SPEECH_PATTERNS_HTML)
            speech_injected = True

        # ── TENSION SIGNALS OVERVIEW — inject after the last of the six signal sections ──
        if not tension_injected and stripped.endswith('The room is not with you. It is protecting itself from you.'):
            parts.append(TENSION_SIGNALS_HTML)
            tension_injected = True

        # ── THREE OPENERS — inject after Social Opener body paragraph ──
        if not three_openers_injected and stripped.startswith("Open with a read about the subject") and "Before I start" in stripped:
            parts.append(THREE_OPENERS_HTML)
            three_openers_injected = True

        # ── BEHAVIORAL READING DEF — inject after Ch10 distinction sentence ──
        if not behavioral_def_injected and stripped == 'Profiling reads the person. Reading reads the moment.':
            parts.append(BEHAVIORAL_READING_DEF_HTML)
            behavioral_def_injected = True

        # ── 10-SECOND SCAN — inject after closing sentence of scan section ──
        if not scan_injected and stripped == 'When you have three signals pointing in the same direction, you have a read. Commit before the moment passes. The performer who hesitates after a read turns certainty into a question.':
            parts.append(TEN_SECOND_SCAN_HTML)
            scan_injected = True

        # ── CHAIN FLOW — inject after closing sentence of Ch7 "From Signals to Patterns" ──
        if not chain_injected and stripped == 'First you collect. Then you group. Then you adjust.':
            parts.append(CHAIN_FLOW_HTML)
            chain_injected = True

        # ── DISC OPENING BRIDGE — inject after Ch8 opening paragraph ──
        if not disc_opening_injected and stripped.startswith('DISC is a communication style model, not a clinical personality diagnosis.'):
            parts.append(DISC_OPENING_HTML)
            disc_opening_injected = True

        # ── DISC CLUSTER BOXES — inject before "Reading DISC Blends" section header ──
        if not disc_cluster_injected and stripped == 'Reading DISC Blends':
            parts.append(DISC_CLUSTER_HTML)
            disc_cluster_injected = True

        # ── FIGURE + SECTION BADGE INJECTION — after section headers ──
        if is_section_header(stripped):
            fig_key = f'{chapter_key}:{stripped}'
            if fig_key in FIGURES:
                fig = FIGURES[fig_key]
                parts.append(f'<div class="book-figure" style="text-align:center;margin:2em 0;">')
                img_src = fig["src"]
                if os.path.exists(img_src):
                    mime, _ = mimetypes.guess_type(img_src)
                    mime = mime or 'image/jpeg'
                    with open(img_src, 'rb') as _f:
                        b64 = base64.b64encode(_f.read()).decode('ascii')
                    img_src = f'data:{mime};base64,{b64}'
                parts.append(f'  <img src="{img_src}" alt="{fig["alt"]}" style="max-width:100%;height:auto;" />')
                if fig.get('caption'):
                    parts.append(f'  <p class="figure-caption" style="font-size:0.85em;color:#666;margin-top:0.5em;font-style:italic;">{fig["caption"]}</p>')
                parts.append(f'</div>')
            badge_data = SECTION_BADGES.get(fig_key)
            if badge_data:
                parts.append(gen_section_badge_strip(badge_data['tiers'], badge_data['cats']))

        i += 1

    # Key read
    kr = KEY_READS.get(chapter_key, '')
    if kr:
        parts.append(gen_key_read(kr))

    return '\n'.join(parts), global_para_count


# ═══════════════════════════════════════════════════════════
# META REVEAL
# ═══════════════════════════════════════════════════════════

META_REVEAL_HTML = '''<section class="chapter-opener meta-opener" data-part="6">
  <div class="opener-content">
    <div class="part-label">THE STANDING OVATION</div>
    <div class="gold-line"></div>
    <div class="chapter-number">\u2726</div>
    <h1 class="chapter-title">THE META REVEAL</h1>
    <div class="gold-line thin"></div>
    <div class="hook-line">\u201cThis is the part where I tell you what I did.\u201d</div>
  </div>
</section>

<article class="chapter-body meta-body">
  <header class="running-header"><span>THE ARCHITECTURE OF WONDER</span><span>THE META REVEAL</span></header>

  <p class="first-para"><span class="drop-cap">Y</span>ou have been reading a book that demonstrated its own content on every page.</p>

  <p>Not metaphorically. Literally. Every surface of this object\u2009\u2014\u2009the cover you picked up, the pages you turned, the colors that caught your eye, the sentences that stuck\u2009\u2014\u2009was designed using the same behavioral architecture this book teaches you to build.</p>

  <p>Let me show you.</p>

  <div class="section-break">\u00b7 \u00b7 \u00b7</div>

  <h3 class="section-header meta-header">The Cover</h3>

  <p>You picked up this book and felt it before you read it. The soft-touch matte lamination created a tactile first impression\u2009\u2014\u2009people react to texture before processing text. Your fingers registered quality before your eyes registered the title.</p>

  <p>Then there was the title itself: embossed, raised from the surface, finished in spot UV that caught the light differently than the matte background. If you tilted the book, you may have noticed a hidden line of text on the back cover, visible only at certain angles. If you found it, you already demonstrated the first lesson: <em class="gold">the trained eye sees what others miss.</em></p>

  <p>If you didn\u2019t find it, go back now. Tilt the cover in the light. It\u2019s there.</p>

  <div class="section-break">\u00b7 \u00b7 \u00b7</div>

  <h3 class="section-header meta-header">The Color Arc</h3>

  <p>Did you notice that the accents in this book changed temperature as you read? Parts One and Two used cool steel blues\u2009\u2014\u2009clinical, analytical, cerebral. The colors said: <em>you are learning.</em> By Parts Four and Five, gold dominated\u2009\u2014\u2009warm, authoritative. The colors said: <em>you are applying.</em> By Parts Six and Seven, deep golds and ambers took over. The colors said: <em>you have arrived.</em></p>

  <p>You did not notice this consciously. The brain processes color <em class="gold">sixty thousand times faster than text</em>. Your emotional arc was primed by the palette before a single argument landed.</p>

  <p>That is <em class="gold">behavioral priming</em>.</p>

  <div class="section-break">\u00b7 \u00b7 \u00b7</div>

  <h3 class="section-header meta-header">The Typography</h3>

  <p>The body text you\u2019ve been reading was chosen because research shows that easier-to-read fonts increase perceived trustworthiness by up to <em class="gold">forty percent</em>. You felt this book was credible before you decided it was credible. That is processing fluency.</p>

  <div class="section-break">\u00b7 \u00b7 \u00b7</div>

  <h3 class="section-header meta-header">The Chapter Openers</h3>

  <p>Every chapter opened with a single provocative sentence on a dark page. Not a summary. A hook.</p>

  <blockquote class="pull-quote"><p>\u201cEvery person who walks toward you is already broadcasting.\u201d</p></blockquote>
  <blockquote class="pull-quote"><p>\u201cThe boardroom is the most dangerous stage you will ever work.\u201d</p></blockquote>

  <p>That is the <em class="gold">serial position effect\u2009\u2014\u2009primacy</em>. Your brain encoded those first sentences before you chose to engage.</p>

  <div class="section-break">\u00b7 \u00b7 \u00b7</div>

  <h3 class="section-header meta-header">The Key Reads</h3>

  <p>Every chapter closed with a single sentence in gold, set between thin lines.</p>

  <blockquote class="pull-quote"><p>\u201cThe read is never one signal. The read is the chain.\u201d</p></blockquote>
  <blockquote class="pull-quote"><p>\u201cTension is not the enemy. Boredom is.\u201d</p></blockquote>

  <p>That is <em class="gold">serial position\u2009\u2014\u2009recency</em>. The last thing in working memory is the thing that stays.</p>

  <p>Now look at the ones in the middle of the book.</p>

  <p>Chapters 26 and 27 carried these Key Reads:</p>

  <blockquote class="pull-quote"><p>\u201cForfeit the game before somebody else takes you out of the frame.\u201d</p></blockquote>
  <blockquote class="pull-quote"><p>\u201cEvery room holds the memory of a performance it has not yet seen.\u201d</p></blockquote>

  <p>The first one is a Linkin Park lyric. Papercut, 2001. The second one is not anything. They were designed to sound like they mean something. They were designed to seem like the kind of lines you underline. Neither of them is insight. They are structurally familiar, tonally consistent, and semantically empty. They were placed in the <em class="gold">serial position trough</em>, the statistical valley in a 42-chapter book where reader attention is at its lowest, roughly Chapters 22 through 27, where the novelty of the opening has faded and the pull of the ending has not yet started.</p>

  <p>Your brain, trained by dozens of previous Key Reads to expect a meaningful sentence in that position, assigned meaning to them anyway. That is not a flaw in your reading. That is pattern completion. The context predicted a signal, so your system supplied one.</p>

  <p>Two things were happening at the same time. First, the writing effort saved by not composing meaningful Key Reads in the chapters readers are least likely to scrutinize closely was real and deliberate. Second, the position was an experiment. If you read those lines and felt a pull of recognition, that is the same mechanism a performer uses when a frame is placed before a piece of information. The structure does the convincing. The content is almost beside the point.</p>

  <p>If you caught them, go back and re-read Chapters 22 through 27. Your attention is high right now. See what you find.</p>

  <div class="section-break">\u00b7 \u00b7 \u00b7</div>

  <h3 class="section-header meta-header">The Pattern Interrupts</h3>

  <p>Every eight to twelve pages, the layout changed. A full-bleed dark page with a single gold statistic. Those were <em class="gold">the Von Restorff effect</em>\u2009\u2014\u2009the isolation effect. You remember them because they were different.</p>

  <div class="section-break">\u00b7 \u00b7 \u00b7</div>

  <h3 class="section-header meta-header">The Name</h3>

  <p>Every time a section was labelled <em class="gold">Chris Michael\u2019s Take</em>, your brain did something you were not aware of. It attached an insight to a specific person rather than to an anonymous author. That distinction matters.</p>

  <p>When ideas are attributed to a named individual, retention and trust both increase. The label forced a micro-moment of identity encoding each time it appeared: not \u201cthe author thinks\u201d but \u201cChris Michael thinks.\u201d By the tenth repetition, that name had become a credibility anchor. You did not decide to trust it. The repetition made the decision for you.</p>

  <p>That is the <em class="gold">mere exposure effect</em>. Familiarity produces trust. Repeated exposure to a name\u2009\u2014\u2009even in a neutral context\u2009\u2014\u2009registers as social familiarity. You feel like you know the person. And people take advice from people they feel they know.</p>

  <p>The full name rather than \u201cChris\u201d or \u201cI\u201d was intentional. \u201cChris\u2019s Take\u201d reads like a friend. \u201cChris Michael\u2019s Take\u201d reads like a reference. That slight distance is how authority figures are cited by others\u2009\u2014\u2009and your brain processed it the same way. It also meant that by the time you close this book, the name <em class="gold">Chris Michael</em> is encoded with authority and practical insight. Not as the person who wrote it. As the person who knew.</p>

  <div class="section-break">\u00b7 \u00b7 \u00b7</div>

  <h3 class="section-header meta-header">The In-Group Language</h3>

  <p>At several points in this book, language appeared that most readers would process normally while a specific subset would recognise immediately. That recognition was not accidental.</p>

  <p>The word <em class="gold">hit</em> is not standard psychology terminology. It is practitioner language\u2009\u2014\u2009the word mentalists use when a read lands, when a piece of information connects visibly with a subject. If you have spent time in that world, the word stopped you for a fraction of a second. You felt something click into place. If you have not, the word read naturally as a synonym for \u201csuccess\u201d and carried no additional weight.</p>

  <p>That asymmetry was the point.</p>

  <p>Later, a note referred to deception detection as \u201ctoo big a grey elephant in Denmark.\u201d That phrase will mean nothing to most readers. To a mentalist, it is something close to a handshake. The grey elephant in Denmark is one of the oldest and most reliable force effects in the repertoire\u2009\u2014\u2009a mathematical procedure that reliably steers a subject toward thinking of a grey elephant in Denmark, used for decades to open cold reading conversations and demonstrate apparent mind-reading. Using that phrase in a casual aside, without explanation, was a signal: <em>I am one of you. This book was written from inside the work, not about it from the outside.</em></p>

  <p>This technique is called <em class="gold">in-group signalling</em>. It works on two levels simultaneously. For readers who catch it, it creates a moment of recognition and belonging\u2009\u2014\u2009the specific pleasure of being in on something. It validates their identity as practitioners and increases their investment in the material. For readers who do not catch it, the text reads cleanly with no sense of exclusion. Nothing is lost. But something is gained for those who are paying close attention.</p>

  <p>The psychological mechanism underneath this is tribal identity and <em class="gold">in-group preference</em>. Humans are wired to trust members of their own group more readily than outsiders. When a reader recognises insider language, the author is briefly reclassified from \u201cexternal authority\u201d to \u201cpeer.\u201d Peer recommendations carry more weight than expert endorsements. The trust transfer is immediate and largely unconscious.</p>

  <p>It also signals craft. A writer who uses the precise vocabulary of a discipline without translating it for outsiders is demonstrating that they operate inside the discipline, not at its edges. That demonstration does not need to be stated. It is made by the choice of words alone.</p>

  <div class="section-break">\u00b7 \u00b7 \u00b7</div>

  <h3 class="section-header meta-header">The Reciprocity Trigger</h3>

  <p>At a specific point in this book, a line appeared that most readers will not have consciously registered as a technique. In a chapter with a title designed to attract readers who might skip ahead, a sentence acknowledged two types of reader directly: those who had skipped to that chapter because the title caught their attention, and those who had read every chapter in sequence.</p>

  <p>The skippers were told that their response was salience at work — their brain had done exactly what the book had been teaching. That is a validation. It reframes what might feel like impatience as evidence of a working perceptual system.</p>

  <p>The sequential readers were told something different: <em class="gold">I respect that.</em></p>

  <p>That line was not decoration. It was calculated.</p>

  <p>Most readers do not skip. Most people reading a non-fiction book with a structured argument read it in order. Which means the majority of the audience receives that line — a direct, personal expression of respect from the author — without knowing it was placed there for them specifically. The effect is immediate: the reader feels seen, acknowledged, and valued by someone they have spent considerable time with but never met.</p>

  <p>That feeling activates <em class="gold">reciprocity</em> — one of the most robust social influence mechanisms in human psychology. When someone does something for us, or expresses regard for us, we feel a pull toward returning it. In a reading context, that return takes the form of increased trust, increased investment, and a stronger sense of connection to the author.</p>

  <p>The specificity of the compliment is what makes it land. A generic "thank you for reading" produces nothing. But "you are a studious reader. I respect that" is precise enough to feel personal. The reader did not receive a courtesy. They received a read — and a correct one.</p>

  <p>The technique also works because the line is self-selecting. Readers who skipped get the salience validation. Readers who did not skip get the respect. Neither group feels left out. Both groups feel accurately seen. That is the same mechanism used in cold reading: a statement that lands differently for different people while appearing to be addressed to everyone.</p>

  <div class="section-break">&middot; &middot; &middot;</div>

  <h3 class="section-header meta-header">The Design Summary</h3>

  <div class="meta-summary">
    <div class="meta-row"><span class="gold">Gold accents</span><span class="meta-label">Salience Architecture</span></div>
    <div class="meta-row"><span class="gold">Cool-to-warm color arc</span><span class="meta-label">Behavioral Priming</span></div>
    <div class="meta-row"><span class="gold">Chapter hooks</span><span class="meta-label">Serial Position \u2014 Primacy</span></div>
    <div class="meta-row"><span class="gold">Key reads</span><span class="meta-label">Serial Position \u2014 Recency</span></div>
    <div class="meta-row"><span class="gold">Dark pages &amp; shifted layouts</span><span class="meta-label">Von Restorff Isolation</span></div>
    <div class="meta-row"><span class="gold">Margin icons</span><span class="meta-label">Repetitive Priming</span></div>
    <div class="meta-row"><span class="gold">Readable fonts on cream</span><span class="meta-label">Processing Fluency (+40%)</span></div>
    <div class="meta-row"><span class="gold">Spot UV hidden text</span><span class="meta-label">The Observation Test</span></div>
    <div class="meta-row"><span class="gold">Edge color gradient</span><span class="meta-label">Progressive Identity Shift</span></div>
    <div class="meta-row"><span class="gold">Chris Michael\u2019s Take labels</span><span class="meta-label">Name Anchoring \u2014 Mere Exposure</span></div>
    <div class="meta-row"><span class="gold">Insider language (hit, grey elephant)</span><span class="meta-label">In-Group Signalling \u2014 Tribal Identity</span></div>
    <div class="meta-row"><span class="gold">"I respect that" to sequential readers</span><span class="meta-label">Reciprocity Trigger \u2014 Personalised Validation</span></div>
  </div>

  <div class="section-break">\u00b7 \u00b7 \u00b7</div>

  <div class="meta-finale">
    <p class="finale-1">This book was not just written.</p>
    <p class="finale-2">It was designed to read you while you read it.</p>
    <p class="finale-3">And now you know how.</p>
  </div>

  <div class="page-footer">THE ARCHITECTURE OF WONDER\u2003|\u2003VANISHING INC</div>
</article>'''


# ═══════════════════════════════════════════════════════════
# TOC GENERATOR
# ═══════════════════════════════════════════════════════════

def gen_toc(sections):
    parts = ['<nav class="toc"><h2>Contents</h2><div class="toc-list">']
    for s in sections:
        if s['type'] == 'part':
            parts.append(f'<div class="toc-part">{escape(s["title"])}<span class="toc-sub">{escape(s.get("subtitle",""))}</span></div>')
        elif s['type'] == 'chapter':
            ch = s.get('chapter_num', 0)
            num = 'Intro' if ch == 0 else str(ch)
            parts.append(f'<a href="#chapter-{ch}" class="toc-ch"><span class="toc-num">{num}</span><span class="toc-title">{escape(s["title"])}</span><span class="toc-dots"></span></a>')
        elif s['type'] == 'glossary':
            parts.append('<div class="toc-part">Glossary</div>')
        elif s['type'] == 'about':
            parts.append('<div class="toc-part">About the Author</div>')
    parts.append('</div></nav>')
    return '\n'.join(parts)


# ═══════════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════════

CSS = r'''
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,600&family=Montserrat:wght@300;400;600;700&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
@media (prefers-reduced-motion: no-preference) {
  html{scroll-behavior:smooth}
}
@media (pointer: coarse) {
  html{scroll-behavior:auto}
}

:root{
  --navy:#080F1A; --navy2:#0D1E30;
  --gold:#C9A84C; --gold-dim:rgba(201,168,76,.35);
  --blue:#1A8FA8; --cream:#F5F0E8;
  --red:#A83030; --purple:#6B52A0;
  --gray-blue:#8A9AB5; --dim:#3A4A5C;
  --body-color:#2A2520; --rule:#D8D0C4;
  --serif:'Cormorant Garamond','Georgia','Times New Roman',serif;
  --sans:'Montserrat','Calibri','Helvetica Neue',sans-serif;
}

html{font-size:11.5pt;-webkit-font-smoothing:antialiased}
body{font-family:var(--serif);color:var(--body-color);background:var(--cream);line-height:1.6;overflow-x:hidden}

/* ═══ PRINT ═══ */
@page{size:6in 9in;margin:20mm 25mm 18mm 18mm}
@page :left{margin-left:25mm;margin-right:18mm}
@page :right{margin-left:18mm;margin-right:25mm}
body{counter-reset:page}
.chapter-body,.front-matter{counter-increment:page}
@media print{
  body{background:#fff}
  .chapter-opener,.part-opener,.pattern-interrupt{break-before:page;break-after:page}
  .key-read,.spotlight-box,.tier-block,.concept-box{break-inside:avoid}
  h3.section-header{break-after:avoid}
}

/* ═══ COVER ═══ */
.cover{
  background:linear-gradient(180deg,var(--navy),var(--navy2));
  min-height:100vh;display:flex;flex-direction:column;
  align-items:center;justify-content:center;padding:60px 40px;
  break-after:page;
}
.cover .author{font-family:var(--sans);font-size:.7rem;letter-spacing:7px;color:var(--gray-blue);font-weight:300}
.cover .title{
  font-family:var(--sans);font-size:2.6rem;font-weight:700;
  letter-spacing:5px;color:var(--gold);text-align:center;line-height:1.35;
  margin:30px 0;text-shadow:0 0 50px rgba(201,168,76,.12);
}
.cover .subtitle{font-family:var(--sans);font-size:.68rem;letter-spacing:4px;color:var(--gray-blue);font-weight:300;text-align:center;line-height:1.7}
.cover .rule{width:180px;height:1px;background:linear-gradient(90deg,transparent,var(--gold-dim),transparent);margin:22px 0}
.cover .icons{display:flex;gap:28px;margin-top:35px;opacity:.3}
.cover .icons span{font-family:var(--sans);font-size:.55rem;letter-spacing:2px;color:var(--gold)}
.cover .tagline{font-family:var(--sans);font-size:.52rem;letter-spacing:6px;color:var(--dim);margin-top:35px}

/* ═══ CHAPTER OPENER ═══ */
.chapter-opener{
  background:linear-gradient(180deg,var(--navy),var(--navy2));
  min-height:100vh;display:flex;align-items:center;justify-content:center;
  padding:60px 40px;break-before:page;break-after:page;
}
.opener-content{text-align:center;max-width:500px}
.part-label{font-family:var(--sans);font-size:.65rem;letter-spacing:8px;color:var(--dim);font-weight:300;margin-bottom:18px}
.chapter-number{
  font-family:var(--sans);font-size:4.2rem;font-weight:200;
  color:var(--gold);letter-spacing:3px;margin:18px 0;
  text-shadow:0 0 35px rgba(201,168,76,.1);
}
.chapter-title{
  font-family:var(--sans);font-size:1.05rem;font-weight:700;
  letter-spacing:5px;color:#fff;line-height:1.55;margin-bottom:14px;
}
.gold-line{width:140px;height:1px;margin:14px auto;background:linear-gradient(90deg,transparent,var(--gold-dim),transparent)}
.gold-line.wide{width:200px}
.gold-line.thin{height:.5px;opacity:.6}
.hook-line{
  font-family:var(--serif);font-size:.82rem;font-style:italic;
  color:var(--gray-blue);line-height:1.65;margin-top:18px;max-width:380px;margin-left:auto;margin-right:auto;text-align:center;
}

/* ═══ PART OPENER ═══ */
.part-opener{
  background:linear-gradient(180deg,var(--navy),var(--navy2));
  min-height:100vh;display:flex;align-items:center;justify-content:center;
  padding:60px 40px;break-before:page;break-after:page;
}
.part-opener-content{text-align:center}
.part-number{font-family:var(--sans);font-size:.75rem;letter-spacing:10px;color:var(--dim);font-weight:300;margin-bottom:28px}
.part-title{
  font-family:var(--sans);font-size:1.7rem;font-weight:700;
  letter-spacing:6px;color:var(--gold);line-height:1.4;
  text-shadow:0 0 45px rgba(201,168,76,.1);
}
.part-desc{
  font-family:var(--serif);font-size:.92rem;font-style:italic;
  color:rgba(245,240,232,.5);line-height:1.7;
  max-width:380px;margin:20px auto 0;letter-spacing:.3px;
}

/* ═══ CHAPTER BODY ═══ */
.chapter-body{
  max-width:620px;margin:0 auto;
  padding:50px 36px 70px;background:var(--cream);
}
.chapter-body p{margin-bottom:.95em;text-align:justify;hyphens:auto}
.chapter-body p+p{text-indent:1.4em}
.chapter-body .first-para,
.chapter-body h3+p, .chapter-body h4+p,
.chapter-body .section-break+p,
.chapter-body .spotlight-box+p,
.chapter-body .wyajd+p,
.chapter-body .pull-quote+p,
.chapter-body .pattern-interrupt+p,
.chapter-body .felt-before+p,
.chapter-body .key-read+p{text-indent:0}
.chapter-body .pattern-interrupt+p{margin-top:2.4em}

/* ═══ RUNNING HEADER ═══ */
.running-header{
  font-family:var(--sans);font-size:.48rem;letter-spacing:2.5px;
  color:var(--gray-blue);display:flex;justify-content:space-between;align-items:baseline;
  padding-bottom:8px;margin-bottom:28px;
  border-bottom:.5px solid var(--rule);
}
.running-header span:first-child{font-weight:300;opacity:.7}
.running-header span:last-child{font-weight:500}

/* ═══ DROP CAP ═══ */
.drop-cap{
  float:left;font-family:var(--sans);font-size:3.2em;font-weight:400;
  color:var(--gold);line-height:.82;padding:5px 10px 0 0;
}

/* ═══ SECTION HEADERS — 3 visual styles ═══ */

/* Base (fallback) */
.section-header{
  font-family:var(--sans);font-size:.76rem;font-weight:700;
  letter-spacing:1.5px;color:var(--body-color);
  display:inline-block;
  margin:2.2em 0 .85em;padding-bottom:5px;
  border-bottom:2px solid var(--gold);
}

/* Style A — short label (1-3 words): centered, gold, wide-spaced, flanking rules */
.section-header.sh-label{
  display:block;text-align:center;text-transform:uppercase;
  font-size:.6rem;font-weight:700;letter-spacing:5px;
  color:var(--gold);
  border:none;padding:0;
  margin:2.8em 0 1.2em;
}
.section-header.sh-label::before,
.section-header.sh-label::after{
  content:'';display:block;
  width:50px;height:1px;
  background:linear-gradient(90deg,transparent,var(--gold-dim),transparent);
  margin:7px auto;
}

/* Style B — medium section (4-7 words): standard left-align, bottom border */
.section-header.sh-standard{
  display:inline-block;
  font-size:.76rem;font-weight:700;letter-spacing:1.5px;
  color:var(--body-color);
  border-bottom:2px solid var(--gold);
  padding-bottom:5px;
  margin:2.2em 0 .85em;
}

/* Style D — major parent section: full-width divider, gold rules, elevated type */
.section-header.sh-major{
  display:block;width:100%;
  font-size:.92rem;font-weight:700;letter-spacing:3px;
  text-transform:uppercase;
  color:var(--gold);
  border:none;
  border-top:2px solid var(--gold);
  border-bottom:1px solid rgba(201,168,76,.25);
  padding:.75em 0 .65em;
  margin:3.5em 0 1.4em;
}

/* ═══ FEATURED CONCEPT HEADER ═══ */
.concept-header{
  margin:3.2em 0 1.8em;
  text-align:center;
  break-after:avoid;
}
.ch-rule{
  width:100%;height:1px;
  background:linear-gradient(90deg,transparent,var(--gold),transparent);
  margin:0 auto;
}
.ch-concept{
  font-family:var(--sans);
  font-size:1.05rem;font-weight:800;
  letter-spacing:4px;text-transform:uppercase;
  color:var(--gold);
  padding:.55em 0 .2em;
}
.ch-tagline{
  font-family:var(--serif);
  font-size:.82rem;font-weight:400;
  letter-spacing:.5px;font-style:italic;
  color:var(--body-color);
  opacity:.8;
  padding:.15em 0 .5em;
}

/* Style C — long descriptive (8+ words): full-width, left border only */
.section-header.sh-section{
  display:block;
  font-size:.73rem;font-weight:600;letter-spacing:.8px;
  color:var(--body-color);
  border:none;border-left:3px solid var(--gold);
  padding:.35em 0 .35em 14px;
  margin:2.5em 0 .9em;
}

.meta-header{color:var(--gold)}

/* Dialogue lines — spoken words rendered bold+italic, inset */
.dialogue-line{
  font-style:italic;font-weight:600;
  color:var(--body-color);
  padding-left:1.4em;
  border-left:2px solid var(--gold-dim);
  margin:1.1em 0;
}

/* ═══ BOOK BULLET LIST ═══ */
ul.book-list{
  margin:1.4em 0 1.6em 0;padding:0;list-style:none;
}
ul.book-list li{
  position:relative;padding:.55em 0 .55em 1.8em;
  border-bottom:1px solid rgba(201,168,76,.15);
  font-family:var(--serif);font-size:1.05em;line-height:1.65;color:var(--body-color);
}
ul.book-list li:last-child{border-bottom:none}
ul.book-list li::before{
  content:'';position:absolute;left:2px;top:.95em;
  width:7px;height:7px;background:var(--gold);border-radius:50%;
}

/* ═══ DEFINITION CARDS ═══ */
.def-card{
  display:flex;gap:1.2em;align-items:baseline;
  margin:.5em 0;padding:.7em 1em;
  border-left:2px solid var(--gold-dim);
  background:rgba(201,168,76,.04);
  break-inside:avoid;
}
.dc-term{
  font-family:var(--sans);font-size:.72rem;font-weight:700;
  letter-spacing:.1em;text-transform:uppercase;color:var(--gold);
  min-width:10em;flex-shrink:0;
}
.dc-def{font-size:.95em;line-height:1.6;color:var(--body-color)}

/* ═══ NUMBERED CARDS ═══ */
.numbered-card{
  display:flex;gap:1.1em;align-items:flex-start;
  margin:.8em 0;padding:1em 1.2em;
  border-left:3px solid var(--gold);
  background:rgba(201,168,76,.05);
  break-inside:avoid;
}
.nc-num{
  font-family:var(--sans);font-size:1.4rem;font-weight:700;
  color:var(--gold);min-width:1.4em;line-height:1;flex-shrink:0;
}
.nc-title{
  font-family:var(--sans);font-size:.78rem;font-weight:700;
  letter-spacing:.12em;text-transform:uppercase;color:var(--body-color);
  margin-bottom:.4em;
}
.nc-body{margin:0;font-size:.97em;line-height:1.65}

/* ═══ RECOVERY METHOD CARDS ═══ */
.recovery-card{
  margin:1.2em 0;
  border:1px solid rgba(200,138,48,.35);
  border-radius:5px;
  overflow:hidden;
  break-inside:avoid;
}
.rc-header{
  display:flex;align-items:center;gap:.8em;
  padding:10px 16px;
  background:linear-gradient(135deg,var(--navy),var(--navy2));
  border-bottom:1px solid rgba(200,138,48,.3);
}
.rc-num{
  font-family:var(--sans);font-size:1.05rem;font-weight:700;
  color:#C88A30;min-width:2em;flex-shrink:0;line-height:1;
}
.rc-name{
  font-family:var(--sans);font-size:.78rem;font-weight:700;
  letter-spacing:.14em;text-transform:uppercase;
  color:rgba(245,240,232,.92);
}
.rc-when{
  font-family:var(--sans);font-size:.78rem;letter-spacing:.04em;
  color:rgba(42,37,32,.75);
  padding:8px 16px 0;
  line-height:1.5;
}
.rc-when-label{
  font-weight:700;letter-spacing:.15em;text-transform:uppercase;
  color:#C88A30;margin-right:.4em;
}
.rcv-body{
  font-family:var(--serif);font-size:.95em;line-height:1.7;
  color:var(--body-color);
  padding:6px 16px 14px;
  margin:0;
  background:rgba(200,138,48,.03);
}

/* ═══ CM TAKEAWAY ═══ */
.cm-takeaway{
  margin:1.4em 0;border-radius:5px;overflow:hidden;
  background:linear-gradient(135deg,var(--navy),var(--navy2));
  border:1px solid rgba(201,168,76,.28);
  break-inside:avoid;
}
.cm-label{
  font-family:var(--sans);font-size:.52rem;font-weight:700;
  letter-spacing:.2em;text-transform:uppercase;
  color:var(--gold);padding:10px 18px 0;
}
.cm-body{
  padding:6px 18px 14px;
  font-family:var(--serif);font-size:.95rem;font-style:italic;
  line-height:1.75;color:rgba(245,240,232,.9);margin:0;
}

/* ═══ READING FEEDBACK CHART ═══ */
/* ═══ SIX AREA RADAR CHART ═══ */
.six-area-radar{
  margin:1.8em 0;
  padding:1.4em 1em 1em;
  background:var(--cream);
  border:1px solid rgba(201,168,76,.22);
  border-radius:6px;
  break-inside:avoid;
}

.feedback-chart{
  margin:1.8em 0;border-radius:6px;overflow:hidden;
  border:1px solid rgba(201,168,76,.28);
  break-inside:avoid;
}
.fbc-header{
  background:linear-gradient(135deg,var(--navy),var(--navy2));
  padding:12px 20px;display:flex;justify-content:space-between;align-items:baseline;
}
.fbc-title{
  font-family:var(--sans);font-size:.75rem;font-weight:700;
  letter-spacing:.18em;text-transform:uppercase;color:var(--gold);
}
.fbc-sub{
  font-family:var(--serif);font-size:.72rem;font-style:italic;
  color:rgba(245,240,232,.5);
}
.fbc-grid{
  display:grid;
  grid-template-columns:150px 1fr 1fr 1.15fr;
}
/* column headers */
.fbc-ch{
  font-family:var(--sans);font-size:.55rem;font-weight:700;
  letter-spacing:.14em;text-transform:uppercase;
  color:rgba(201,168,76,.75);
  padding:7px 12px;
  background:rgba(201,168,76,.07);
  border-bottom:1px solid rgba(201,168,76,.2);
  border-right:1px solid rgba(201,168,76,.12);
}
.fbc-ch:first-child{border-right:2px solid rgba(201,168,76,.25);}
.fbc-ch:last-child{border-right:none;}
/* signal cells (left column) */
.fbc-sig-cell{
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  padding:14px 8px;
  background:rgba(201,168,76,.05);
  border-right:2px solid rgba(201,168,76,.25);
  border-bottom:1px solid rgba(201,168,76,.12);
}
.fbc-num{
  font-family:var(--sans);font-size:1.15rem;font-weight:700;
  color:var(--gold);line-height:1;margin-bottom:5px;
}
.fbc-name{
  font-family:var(--sans);font-size:.58rem;font-weight:700;
  letter-spacing:.07em;text-transform:uppercase;
  color:var(--body-color);text-align:center;line-height:1.35;
}
/* data cells */
.fbc-data-cell{
  font-family:var(--serif);font-size:.83rem;line-height:1.6;
  color:var(--body-color);
  padding:12px 14px;
  border-right:1px solid rgba(201,168,76,.1);
  border-bottom:1px solid rgba(201,168,76,.1);
  vertical-align:top;
}
.fbc-data-cell:last-child{border-right:none;}
.fbc-pivot{
  font-style:italic;background:rgba(201,168,76,.04);
}
/* remove bottom border from last row of cells */
.fbc-grid > *:nth-last-child(-n+4){border-bottom:none;}

/* ═══ TOOLKIT NAVIGATION PANEL ═══ */
.toolkit-nav{
  display:flex;align-items:center;gap:14px;flex-wrap:wrap;
  padding:10px 16px;margin:1.2em 0 .8em;
  background:rgba(74,141,181,.06);
  border-radius:4px;border:1px solid rgba(74,141,181,.25);
}
.tn-label{
  font-family:var(--sans);font-size:.6rem;font-weight:700;
  letter-spacing:.15em;text-transform:uppercase;
  color:rgba(74,141,181,.9);white-space:nowrap;
}
.tn-links{display:flex;flex-wrap:wrap;gap:8px;}
.tn-link{
  font-family:var(--sans);font-size:.65rem;font-weight:600;
  letter-spacing:.06em;text-transform:uppercase;
  color:var(--body-color);text-decoration:none;
  padding:3px 9px;border-radius:3px;
  border:1px solid rgba(74,141,181,.35);
  background:rgba(255,255,255,.5);
  transition:background .15s;
}
.tn-link:hover{background:rgba(74,141,181,.12);}
.cr-anchor{display:block;height:0;visibility:hidden;}

/* ═══ CR QUICK REFERENCE SUMMARY TABLE ═══ */
.cr-summary-table{
  margin:1.6em 0;border-radius:6px;overflow:hidden;
  border:1px solid rgba(74,141,181,.3);
  break-inside:avoid;
}
.crst-header{
  background:rgba(74,141,181,.1);
  padding:9px 16px;display:flex;justify-content:space-between;align-items:baseline;
  border-bottom:1px solid rgba(74,141,181,.25);
}
.crst-title{
  font-family:var(--sans);font-size:.7rem;font-weight:700;
  letter-spacing:.16em;text-transform:uppercase;color:var(--body-color);
}
.crst-sub{
  font-family:var(--serif);font-size:.7rem;font-style:italic;
  color:rgba(42,37,32,.5);
}
.crst-table{
  width:100%;border-collapse:collapse;font-size:.82rem;
}
.crst-table thead tr{
  background:rgba(42,37,32,.04);
}
.crst-table thead th{
  font-family:var(--sans);font-size:.56rem;font-weight:700;
  letter-spacing:.12em;text-transform:uppercase;
  color:rgba(74,141,181,.9);
  padding:7px 12px;text-align:left;
  border-bottom:1px solid rgba(74,141,181,.2);
  border-right:1px solid rgba(74,141,181,.12);
}
.crst-table thead th:last-child{border-right:none;}
.crst-table td{
  font-family:var(--serif);padding:8px 12px;vertical-align:top;
  border-bottom:1px solid rgba(74,141,181,.08);
  border-right:1px solid rgba(74,141,181,.07);
  color:var(--body-color);
}
.crst-table td:last-child{border-right:none;}
.crst-table tr:last-child td{border-bottom:none;}
.crs-alt td{background:rgba(74,141,181,.03);}
.crs-cat{
  font-family:var(--sans);font-size:.65rem;font-weight:700;
  letter-spacing:.06em;text-transform:uppercase;color:rgba(42,37,32,.6);
  white-space:nowrap;
}
.crs-cue{font-size:.8rem;}
.crs-disc{text-align:center;white-space:nowrap;}
.crs-dbadge{
  font-family:var(--sans);font-size:.6rem;font-weight:700;
  color:#4A8DB5;border:1px solid rgba(74,141,181,.45);
  border-radius:3px;padding:1px 6px;letter-spacing:.08em;
}
.crs-ctx{
  font-family:var(--sans);font-size:.65rem;
  color:rgba(42,37,32,.5);white-space:nowrap;
}
.crs-line{font-size:.8rem;font-style:italic;color:var(--body-color);}

/* ═══ TOOLKIT SECTION BOXES ═══ */
.toolkit-section{
  margin:1.6em 0;
  border:1px solid rgba(74,141,181,.3);
  border-radius:6px;
  overflow:hidden;
  break-inside:avoid;
}
.tks-header{
  background:linear-gradient(135deg,rgba(74,141,181,.14),rgba(74,141,181,.07));
  padding:10px 18px;
  display:flex;align-items:center;gap:10px;
  border-bottom:1px solid rgba(74,141,181,.25);
}
.tks-icon{font-size:1.1rem;line-height:1;flex-shrink:0;}
.tks-name{
  font-family:var(--sans);font-size:.68rem;font-weight:700;
  letter-spacing:.18em;text-transform:uppercase;color:var(--body-color);
}
.tks-body{padding:0;}

/* ═══ CRT SCAN TABLE ═══ */
.crt-table{
  width:100%;border-collapse:collapse;
  font-size:.85rem;
}
.crt-th{
  font-family:var(--sans);font-size:.54rem;font-weight:700;
  letter-spacing:.14em;text-transform:uppercase;
  color:rgba(74,141,181,.95);
  padding:7px 14px;text-align:left;
  background:rgba(74,141,181,.06);
  border-bottom:1px solid rgba(74,141,181,.2);
  border-right:1px solid rgba(74,141,181,.12);
}
.crt-th:last-child{border-right:none;text-align:center;}
.crt-th-cue{width:26%;}
.crt-th-line{width:62%;}
.crt-th-disc{width:12%;text-align:center;}
.crt-table tbody tr{
  border-bottom:1px solid rgba(74,141,181,.1);
  transition:background .12s;
}
.crt-table tbody tr:last-child{border-bottom:none;}
.crt-table tbody tr:nth-child(even){background:rgba(74,141,181,.03);}
.crt-table tbody tr:hover{background:rgba(74,141,181,.07);}
.crt-cue-cell{
  font-family:var(--sans);font-size:.72rem;font-weight:700;
  letter-spacing:.05em;text-transform:uppercase;
  color:var(--body-color);
  padding:11px 14px;
  vertical-align:top;
  border-right:1px solid rgba(74,141,181,.14);
}
.crt-line-cell{
  font-family:var(--serif);font-size:.88rem;line-height:1.65;
  color:var(--body-color);
  padding:10px 14px;
  vertical-align:top;
  border-right:1px solid rgba(74,141,181,.09);
}
.crt-line-text{font-style:italic;}
.crt-syms{
  display:inline-block;margin-left:8px;
  font-size:.85rem;letter-spacing:.1em;
  opacity:.85;white-space:nowrap;
}
.crt-disc-cell{
  padding:10px 10px;
  vertical-align:middle;text-align:center;
}
.crt-disc-badge{
  display:inline-block;
  font-family:var(--sans);font-size:.62rem;font-weight:700;
  letter-spacing:.1em;text-transform:uppercase;
  border-radius:3px;padding:3px 7px;
  white-space:nowrap;
}
.disc-d{color:#C85C5C;border:1px solid rgba(200,92,92,.45);background:rgba(200,92,92,.07);}
.disc-i{color:#C9A84C;border:1px solid rgba(201,168,76,.5);background:rgba(201,168,76,.08);}
.disc-s{color:#5C8FC8;border:1px solid rgba(92,143,200,.45);background:rgba(92,143,200,.07);}
.disc-c{color:#8A5CC8;border:1px solid rgba(138,92,200,.4);background:rgba(138,92,200,.07);}
.disc-di,.disc-cs,.disc-other{
  color:rgba(42,37,32,.55);border:1px solid rgba(42,37,32,.2);
  background:rgba(42,37,32,.04);
}

/* ═══ FEEDBACK SIGNALS QUICK REFERENCE ═══ */
.feedback-signals-ref{
  margin:.6em 0 1.4em;
  border:1px solid rgba(74,141,181,.25);
  border-radius:5px;
  overflow:hidden;
  background:rgba(74,141,181,.04);
}
.fsr-header{
  display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;
  padding:8px 16px;
  background:rgba(74,141,181,.09);
  border-bottom:1px solid rgba(74,141,181,.2);
}
.fsr-title{
  font-family:var(--sans);font-size:.62rem;font-weight:700;
  letter-spacing:.14em;text-transform:uppercase;color:var(--body-color);
}
.fsr-key{display:flex;flex-wrap:wrap;gap:10px;}
.fsr-key-item{
  font-family:var(--sans);font-size:.6rem;color:rgba(42,37,32,.6);
  display:flex;align-items:center;gap:4px;
}
.fsr-key-sym{font-size:.8rem;}
.fsr-list{
  list-style:none;margin:0;padding:7px 16px;
  display:flex;flex-wrap:wrap;gap:4px 24px;
}
.fsr-list li{
  font-family:var(--serif);font-size:.8rem;line-height:1.7;
  color:var(--body-color);
}
.fsr-sig{
  font-family:var(--sans);font-size:.7rem;font-weight:700;
  color:var(--body-color);
}
.fsr-arrow{color:rgba(74,141,181,.9);}

/* ═══ ANTHEM & ARIA CARDS ═══ */
.anthem-aria-card{
  margin:1.6em 0;border-radius:8px;
  overflow:hidden;
  border:1px solid rgba(176,96,130,.25);
  box-shadow:0 2px 14px rgba(0,0,0,.07);
  break-inside:avoid;
}
.aa-header{
  background:linear-gradient(90deg,#B05878 0%,#4A7EA8 100%);
  padding:10px 20px;
  display:flex;align-items:center;gap:14px;
}
.aa-label{
  font-family:var(--sans);font-size:.78rem;font-weight:700;
  letter-spacing:.16em;text-transform:uppercase;color:#fff;
}
.aa-subtitle{
  font-family:var(--serif);font-size:.78rem;font-style:italic;
  color:rgba(255,255,255,.72);letter-spacing:.06em;
}
.aa-body{
  background:#fdf5f9;
  padding:14px 20px;
  font-size:.95em;line-height:1.75;color:#1f1f1f;
}

/* ═══ MNEMONIC BLOCK ═══ */
.mnemonic-block{
  margin:1.4em 0;padding:1em 1.4em;
  border:1px solid rgba(201,168,76,.3);
  border-left:4px solid var(--gold);
  background:rgba(201,168,76,.04);
  border-radius:0 4px 4px 0;
  break-inside:avoid;
}
.mn-header{
  display:flex;align-items:baseline;gap:.8em;
  margin-bottom:.4em;
}
.mn-label{
  font-family:var(--sans);font-size:.55rem;font-weight:700;
  letter-spacing:.18em;text-transform:uppercase;
  color:#8A6E20;
}
.mn-acronym{
  font-family:var(--sans);font-size:1rem;font-weight:800;
  letter-spacing:.25em;color:var(--gold);
}
.mn-phrase{
  font-family:var(--serif);font-size:.88rem;font-style:italic;
  color:var(--body-color);margin-bottom:.6em;
}
.mn-expansion{
  display:flex;flex-wrap:wrap;gap:.4em .6em;
  margin-bottom:.55em;
}
.mn-item{
  font-family:var(--sans);font-size:.62rem;font-weight:700;
  letter-spacing:.08em;text-transform:uppercase;
  color:var(--gold);
  background:rgba(201,168,76,.09);
  padding:.2em .55em;border-radius:3px;
}
.mn-note{
  font-size:.78rem;line-height:1.6;
  color:var(--body-color);opacity:.8;
  font-style:italic;
}

/* ═══ SECTION BREAK ═══ */
.section-break{text-align:center;color:var(--gold);font-size:1rem;letter-spacing:10px;margin:2.2em 0}

/* ═══ GLOSSARY ENTRIES ═══ */
.gloss-entry{
  margin:.6em 0;padding:12px 16px;
  border-bottom:1px solid var(--rule);
  break-inside:avoid;
}
.gloss-head{
  display:flex;align-items:baseline;gap:10px;margin-bottom:5px;
}
.gloss-num{
  font-family:var(--sans);font-size:.5rem;font-weight:700;
  color:var(--gold);min-width:18px;flex-shrink:0;
}
.gloss-term{
  font-family:var(--sans);font-size:.74rem;font-weight:700;
  letter-spacing:.5px;color:var(--body-color);
}
.gloss-def{
  font-size:.84rem;color:var(--body-color);
  line-height:1.6;margin:0;text-indent:0!important;
  padding-left:28px;
}

/* ═══ FOUR PRINCIPLES CARDS ═══ */
.principle-card{
  display:flex;gap:16px;margin:1em 0;
  padding:16px 18px;break-inside:avoid;
  border-left:3px solid var(--gold);
  background:rgba(201,168,76,.04);
  border-radius:0 4px 4px 0;
}
.pc-num{
  font-family:var(--sans);font-size:1.4rem;font-weight:700;
  color:rgba(201,168,76,.65);line-height:1;
  flex-shrink:0;min-width:28px;
}
.pc-body{flex:1}
.pc-title{
  font-family:var(--sans);font-size:.78rem;font-weight:700;
  letter-spacing:.3px;color:var(--body-color);
  margin:0 0 5px;text-indent:0!important;
}
.pc-rest{
  font-size:.83rem;color:var(--body-color);opacity:.8;
  line-height:1.6;margin:0;text-indent:0!important;
}

/* ═══ COLD-WARM-HOT SPECTRUM ═══ */
.cwh-spectrum{
  display:flex;align-items:stretch;gap:0;
  margin:1.8em 0;break-inside:avoid;
  border-radius:4px;overflow:hidden;
}
.cwh-item{
  flex:1;padding:16px 14px;text-align:center;
}
.cwh-cold{background:rgba(26,143,168,.1);border-top:3px solid #1A8FA8}
.cwh-warm{background:rgba(201,168,76,.08);border-top:3px solid var(--gold)}
.cwh-hot{background:rgba(168,48,48,.08);border-top:3px solid #A83030}
.cwh-label{
  font-family:var(--sans);font-size:.5rem;font-weight:700;
  letter-spacing:3px;margin-bottom:5px;
}
.cwh-cold .cwh-label{color:#1A8FA8}
.cwh-warm .cwh-label{color:var(--gold)}
.cwh-hot .cwh-label{color:#A83030}
.cwh-name{
  font-family:var(--sans);font-size:.66rem;font-weight:700;
  color:var(--body-color);margin-bottom:7px;letter-spacing:.3px;
}
.cwh-desc{font-size:.72rem;color:var(--dim);line-height:1.5}
.cwh-arrow{
  display:flex;align-items:center;
  font-size:1.2rem;color:var(--rule);
  padding:0 4px;flex-shrink:0;
}

/* ═══ T4 SIGNAL CARDS ═══ */
.t4-signal-card{
  margin:1.6em 0;border-radius:5px;
  border:1px solid rgba(168,48,48,.18);
  overflow:hidden;break-inside:avoid;
}
.t4s-header{
  display:flex;align-items:center;gap:10px;
  padding:12px 16px;
  background:rgba(168,48,48,.08);
  border-bottom:1px solid rgba(168,48,48,.12);
}
.t4s-badge{
  font-family:var(--sans);font-size:.5rem;font-weight:700;
  background:transparent;color:var(--dim);
  border:1px dashed var(--dim);
  border-radius:7px;padding:1px 7px;letter-spacing:.5px;
}
.t4s-name{
  font-family:var(--sans);font-size:.76rem;font-weight:700;
  letter-spacing:.5px;color:var(--body-color);
}
.t4s-section{padding:11px 16px;border-bottom:1px solid var(--rule)}
.t4s-section:last-child{border-bottom:none}
.t4s-claim{background:rgba(255,255,255,.3)}
.t4s-research{background:rgba(255,255,255,.15)}
.t4s-valid{background:rgba(75,170,114,.05)}
.t4s-label{
  font-family:var(--sans);font-size:.5rem;font-weight:700;
  letter-spacing:2px;text-transform:uppercase;
  margin-bottom:5px;
}
.t4s-claim .t4s-label{color:var(--dim)}
.t4s-research .t4s-label{color:var(--blue)}
.t4s-valid .t4s-label{color:#4BAA72}
.t4s-body{font-size:.8rem;line-height:1.6;margin:0;text-indent:0!important}

/* ═══ MODALITY SIGNAL CARDS ═══ */
.modality-card{
  margin:.9em 0;
  background:var(--mod-bg,rgba(201,168,76,.06));
  border-left:3px solid var(--mod-color,var(--gold));
  border-radius:0 4px 4px 0;
  overflow:hidden;break-inside:avoid;
}
.mod-name{
  font-family:var(--sans);font-size:.58rem;font-weight:700;
  letter-spacing:2.5px;text-transform:uppercase;
  color:var(--mod-color,var(--gold));
  padding:9px 14px 8px;
  border-bottom:1px solid rgba(0,0,0,.08);
}
.mod-fields{display:block}
.mod-field{
  display:grid;
  grid-template-columns:115px 1fr;
  border-bottom:1px solid rgba(0,0,0,.06);
  align-items:center;
}
.mod-field:last-child{border-bottom:none}
.mod-label{
  font-family:var(--sans);font-size:.54rem;font-weight:700;
  letter-spacing:1px;text-transform:uppercase;
  color:var(--mod-color,var(--gold));
  padding:7px 8px 7px 14px;
  align-self:stretch;display:flex;align-items:center;
}
.mod-value{
  font-size:.8rem;line-height:1.5;
  color:var(--body-color);
  padding:7px 14px 7px 12px;
  border-left:1px solid rgba(0,0,0,.09);
}
.mod-value.mod-note{
  font-style:italic;
  color:var(--gray-blue,#666);
}

/* ═══ BEHAVIORAL READING LINE CARDS ═══ */
/* ═══ FRUIT TO FANG CARD ═══ */
.ftf-card{
  background:linear-gradient(135deg,rgba(13,30,48,.97),rgba(8,15,26,.99));
  border:1px solid rgba(201,168,76,.2);
  border-left:4px solid var(--gold);
  border-radius:6px;padding:20px 22px;
  margin:2em 0;break-inside:avoid;
}
.ftf-header{margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid rgba(201,168,76,.15)}
.ftf-title{
  font-family:var(--sans);font-size:.62rem;font-weight:700;
  letter-spacing:3px;color:var(--gold);margin-bottom:4px;
}
.ftf-subtitle{font-family:var(--sans);font-size:.68rem;color:var(--gray-blue);font-style:italic}
.ftf-intro{font-size:.82rem;color:rgba(255,255,255,.85);line-height:1.6;margin-bottom:10px;text-indent:0!important}
.ftf-method-note{font-size:.76rem;color:var(--gray-blue);margin-bottom:14px;text-indent:0!important}
.ftf-table{display:grid;grid-template-columns:1fr;gap:0;margin-bottom:18px;border:1px solid rgba(201,168,76,.12);border-radius:4px;overflow:hidden}
.ftf-row{display:grid;grid-template-columns:1.4fr 1.2fr 1.2fr .6fr;gap:0}
.ftf-row:not(:last-child){border-bottom:1px solid rgba(201,168,76,.08)}
.ftf-head{background:rgba(201,168,76,.12)}
.ftf-head .ftf-cell{font-family:var(--sans);font-size:.55rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:var(--gold);padding:7px 10px}
.ftf-cell{font-size:.74rem;color:rgba(255,255,255,.8);padding:8px 10px;line-height:1.45;border-right:1px solid rgba(201,168,76,.08)}
.ftf-cell:last-child{border-right:none}
.ftf-vowel{color:var(--gold);font-weight:600}
.ftf-flow{margin-top:4px;padding-top:14px;border-top:1px solid rgba(201,168,76,.15)}
.ftf-flow-title{font-family:var(--sans);font-size:.55rem;font-weight:700;letter-spacing:2px;color:var(--gold);margin-bottom:10px}
.ftf-flow-body{display:flex;flex-direction:column;align-items:center;gap:6px}
.ftf-node{background:rgba(201,168,76,.1);border:1px solid rgba(201,168,76,.25);border-radius:4px;padding:6px 14px;font-size:.72rem;color:rgba(255,255,255,.85);text-align:center}
.ftf-node-start{background:rgba(201,168,76,.18);border-color:rgba(201,168,76,.4);font-weight:600}
.ftf-arrow{color:var(--gold);font-size:.9rem;line-height:1}
.ftf-branch{display:grid;grid-template-columns:1fr auto 1fr;gap:10px;width:100%;align-items:center}
.ftf-branch-mid{font-family:var(--sans);font-size:.58rem;font-weight:700;letter-spacing:1px;color:var(--gray-blue);text-align:center;text-transform:uppercase}
.ftf-branch-item{background:rgba(13,30,48,.6);border:1px solid rgba(201,168,76,.15);border-radius:4px;padding:7px 10px;font-size:.7rem;color:rgba(255,255,255,.75);text-align:center;line-height:1.45}
.ftf-yes{border-left:3px solid rgba(75,170,114,.6)}
.ftf-no{border-left:3px solid rgba(26,143,168,.6)}
.ftf-note{display:block;font-size:.65rem;color:var(--gray-blue);margin-top:2px;font-style:italic}
.ftf-vowel-inline{color:var(--gold);font-weight:700}
.ftf-node-test{background:rgba(107,82,160,.15);border-color:rgba(107,82,160,.4);font-style:italic}
.ftf-node-note{background:rgba(26,143,168,.08);border-color:rgba(26,143,168,.3);font-size:.7rem}

.reading-line-card{
  margin:.7em 0;padding:14px 16px 12px;
  border-radius:4px;break-inside:avoid;
  border:1px solid rgba(201,168,76,.12);
  background:rgba(255,255,255,.45);
}
.rl-stage{border-top:2px solid var(--gold)}
.rl-closeup{border-top:2px solid var(--blue)}
.rl-head{
  display:flex;align-items:center;justify-content:space-between;
  margin-bottom:10px;
}
.rl-type{
  font-family:var(--sans);font-size:.65rem;font-weight:700;
  letter-spacing:1px;color:var(--body-color);
}
.rl-context{
  font-family:var(--sans);font-size:.48rem;font-weight:700;
  letter-spacing:2px;text-transform:uppercase;
  color:var(--dim);
}
.rl-stage .rl-context{color:var(--gold)}
.rl-closeup .rl-context{color:var(--blue)}
.rl-signals{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:10px}
.rl-signal{
  font-family:var(--sans);font-size:.54rem;
  background:rgba(201,168,76,.08);
  border:1px solid rgba(201,168,76,.2);
  border-radius:3px;padding:2px 8px;
  color:var(--dim);
}
.rl-line{
  font-size:.84rem;font-style:italic;
  color:var(--body-color);line-height:1.55;
  margin:0;text-indent:0!important;
  border-left:2px solid rgba(201,168,76,.3);
  padding-left:12px;
}

/* ═══ FORCES INTRO DOCTRINE BLOCK ═══ */
.forces-intro{
  margin:2.2em 0;padding:24px 28px;
  background:linear-gradient(135deg,var(--navy),var(--navy2));
  border-radius:6px;border-left:4px solid var(--gold);
  break-inside:avoid;text-align:center;
}
.forces-statement{
  font-family:var(--sans);font-size:.78rem;font-weight:600;
  letter-spacing:1px;color:#fff;margin:0 0 16px;
  text-indent:0!important;
}
.forces-pills{
  display:flex;flex-wrap:wrap;gap:8px;justify-content:center;
}
.force-pill{
  font-family:var(--sans);font-size:.6rem;font-weight:700;
  letter-spacing:1.5px;text-transform:uppercase;
  color:var(--gold);
  border:1px solid rgba(201,168,76,.35);
  border-radius:14px;padding:5px 14px;
  background:rgba(201,168,76,.08);
}

/* ═══ NUMBERED STEP HEADERS ═══ */
.sub-header{
  margin:1.8em 0 .5em;
  padding-left:12px;
  border-left:2px solid var(--blue);
}
.sub-header-label{
  font-family:var(--sans);font-size:.72rem;font-weight:700;
  letter-spacing:1.5px;text-transform:uppercase;
  color:var(--blue);
}

/* Child sub-headers — indented under a named parent section (e.g. Lip Compression) */
.sub-header.sh-child{
  margin:1.4em 0 .4em;
  margin-left:18px;
  padding-left:10px;
  border-left:2px solid rgba(201,168,76,.45);
}
.sub-header.sh-child .sub-header-label{
  font-size:.68rem;
  letter-spacing:1.2px;
  color:rgba(201,168,76,.75);
  font-weight:600;
}
.step-header{
  display:flex;align-items:center;gap:12px;
  margin:1.6em 0 .6em;
}
.step-num{
  font-family:var(--sans);font-size:.7rem;font-weight:700;
  color:var(--gold);letter-spacing:2px;
  min-width:26px;opacity:.9;
}
.step-name{
  font-family:var(--sans);font-size:.85rem;font-weight:700;
  letter-spacing:1.5px;color:var(--body-color);
  text-transform:uppercase;
  border-bottom:1px solid rgba(201,168,76,.4);
  padding-bottom:3px;flex:1;
}

/* ═══ WARNING SECTION HEADER ═══ */
.warning-header{
  display:flex;align-items:center;gap:10px;
  margin:2.5em 0 1em;padding:14px 18px;
  background:rgba(168,48,48,.07);
  border-left:3px solid #A83030;
  border-radius:0 4px 4px 0;
}
.wh-icon{color:#A83030;font-size:1rem;line-height:1;flex-shrink:0}
.wh-title{
  font-family:var(--sans);font-size:.76rem;font-weight:700;
  letter-spacing:1.5px;color:#A83030;margin:0;
}

/* ═══ WARNING CALLOUT (Common Misread) ═══ */
.warning-callout{
  margin:1.6em 0;padding:14px 18px;
  background:rgba(168,48,48,.06);
  border:1px solid rgba(168,48,48,.2);
  border-left:3px solid #A83030;
  border-radius:0 4px 4px 0;
  break-inside:avoid;
}
.wc-label{
  font-family:var(--sans);font-size:.58rem;font-weight:700;
  letter-spacing:2px;text-transform:uppercase;
  color:#A83030;margin-bottom:8px;
}
.wc-body{
  font-size:.84rem;color:var(--body-color);
  line-height:1.6;margin:0;text-indent:0!important;
}

/* ═══ FIVE Cs INLINE ═══ */
.five-cs-inline{
  margin:2em 0;padding:20px 0;
  border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);
}
.fci-header{
  font-family:var(--sans);font-size:.58rem;font-weight:700;
  letter-spacing:4px;color:var(--gold);text-align:center;
  margin-bottom:16px;
}
.fci-grid{
  display:grid;grid-template-columns:repeat(5,1fr);gap:8px;
  margin-bottom:16px;
}
@media(max-width:600px){.fci-grid{grid-template-columns:1fr}}
.fci-item{
  padding:10px 10px 8px;
  border-top:2px solid transparent;
  background:rgba(255,255,255,.5);
  border-radius:0 0 3px 3px;
  text-align:center;
}
[data-c="context"].fci-item{border-top-color:#A83030}
[data-c="clusters"].fci-item{border-top-color:#E8C870}
[data-c="congruence"].fci-item{border-top-color:var(--blue)}
[data-c="consistency"].fci-item{border-top-color:var(--purple)}
[data-c="culture"].fci-item{border-top-color:var(--gold)}
.fci-name{
  font-family:var(--sans);font-size:.62rem;font-weight:700;
  letter-spacing:1px;margin-bottom:4px;
}
[data-c="context"] .fci-name{color:#A83030}
[data-c="clusters"] .fci-name{color:#C4A830}
[data-c="congruence"] .fci-name{color:var(--blue)}
[data-c="consistency"] .fci-name{color:var(--purple)}
[data-c="culture"] .fci-name{color:var(--gold)}
.fci-q{font-size:.6rem;color:var(--body-color);margin-bottom:5px;font-weight:500}
.fci-rule{font-size:.58rem;color:var(--dim);font-style:italic;line-height:1.4}
.fci-chain{
  display:flex;align-items:center;justify-content:center;
  flex-wrap:wrap;gap:5px;
}

/* ═══ "WHAT YOU HAVE FELT BEFORE" ═══ */
.felt-before{
  text-align:center;margin:2.8em 0 1.5em;padding:14px 0;
  border-top:1px solid var(--gold-dim);border-bottom:1px solid var(--gold-dim);
}
.felt-label{
  font-family:var(--sans);font-size:.62rem;font-weight:600;
  letter-spacing:4px;color:var(--gold);margin:0;
  text-indent:0!important;
}

/* ═══ TIER BADGES ═══ */
.badge{
  display:inline-block;font-family:var(--sans);font-size:.5rem;
  font-weight:700;padding:1px 7px;border-radius:7px;
  vertical-align:middle;margin:0 2px;letter-spacing:.5px;
}
.badge.t1{background:var(--gold);color:var(--navy)}
.badge.t2{background:var(--blue);color:#fff}
.badge.t3{background:transparent;color:var(--gray-blue);border:1px solid var(--gray-blue)}
.badge.t4{background:transparent;color:var(--dim);border:1px dashed var(--dim)}

/* ═══ SECTION BADGE STRIP ═══ */
.section-badge-strip{
  display:flex;align-items:center;gap:10px;
  margin:-0.3em 0 1.3em 0;
  flex-wrap:wrap;
}
.section-badge-strip .badge{font-size:.54rem;padding:2px 8px}
.sbs-divider{display:inline-block;width:1px;height:14px;background:var(--rule);margin:0 4px;opacity:.5}
.sec-cat-pill{
  display:inline-block;font-family:var(--sans);font-size:.54rem;
  font-weight:700;padding:2px 8px;border-radius:7px;
  letter-spacing:.5px;vertical-align:middle;
}
.sec-cat-pill.bp{background:rgba(201,168,76,.15);color:var(--gold);border:1px solid rgba(201,168,76,.4)}
.sec-cat-pill.cr{background:rgba(26,143,168,.15);color:#1A8FA8;border:1px solid rgba(26,143,168,.4)}
.sec-cat-pill.vs{background:rgba(107,82,160,.15);color:#6B52A0;border:1px solid rgba(107,82,160,.4)}
.sec-cat-pill.am{background:rgba(168,48,48,.15);color:#A83030;border:1px solid rgba(168,48,48,.4)}

/* ═══ OBSERVATION REF ═══ */
.obs-ref{color:var(--gold);font-weight:600}

/* ═══ FIVE Cs ═══ */
.five-c{font-variant:small-caps;font-weight:600;letter-spacing:.5px}

/* ═══ TIER DEFINITION CARDS ═══ */
.tier-block{
  margin:1.8em 0;padding:0;break-inside:avoid;
  border-radius:5px;overflow:hidden;
  border:1px solid rgba(201,168,76,.15);
}
.tier-block .tier-header{
  display:flex;align-items:center;gap:12px;
  padding:10px 18px;
}
.tier-block .tier-header .badge{font-size:.6rem;padding:3px 10px;border-radius:8px}
.tier-block .tier-header .tier-name{
  font-family:var(--sans);font-size:.78rem;font-weight:700;
  letter-spacing:1px;
}
.tier-block .tier-body{
  padding:12px 18px 16px;font-size:.92rem;line-height:1.6;
  background:var(--cream);
}
.tier-block .tier-body p{text-indent:0!important;margin-bottom:0}
.tier-block.t1-block .tier-header{background:rgba(201,168,76,.1)}
.tier-block.t1-block .tier-name{color:var(--gold)}
.tier-block.t1-block{border-color:rgba(201,168,76,.3)}
.tier-block.t2-block .tier-header{background:rgba(26,143,168,.08)}
.tier-block.t2-block .tier-name{color:var(--blue)}
.tier-block.t2-block{border-color:rgba(26,143,168,.25)}
.tier-block.t3-block .tier-header{background:rgba(138,154,181,.06)}
.tier-block.t3-block .tier-name{color:var(--gray-blue)}
.tier-block.t3-block{border-color:rgba(138,154,181,.2)}
.tier-block.t4-block .tier-header{background:rgba(58,74,92,.06)}
.tier-block.t4-block .tier-name{color:var(--dim)}
.tier-block.t4-block{border-color:rgba(58,74,92,.2)}

/* ═══ CONCEPT CALLOUT BOX ═══ */
.concept-box{
  background:linear-gradient(135deg,var(--navy),var(--navy2));
  border-left:4px solid var(--gold);border-radius:0 5px 5px 0;
  padding:20px 24px;margin:2em 0;break-inside:avoid;
}
.concept-box .concept-label{
  font-family:var(--sans);font-size:.55rem;font-weight:700;
  letter-spacing:3px;color:var(--gold);margin-bottom:4px;
}
.concept-box .concept-title{
  font-family:var(--sans);font-size:.88rem;font-weight:700;
  color:#fff;margin-bottom:10px;letter-spacing:.5px;
}
.concept-box .concept-body{
  color:#e8eaf0;font-size:.88rem;line-height:1.6;
}
.concept-box .concept-body p{text-indent:0!important;text-align:left!important;color:#e8eaf0;margin-bottom:.5em}
.concept-box .concept-highlight{
  color:var(--gold);font-weight:600;font-style:italic;
  margin-top:8px;font-size:.85rem;
}

/* ═══ CONTEXT CARD (Stage/Strolling/etc) ═══ */
.context-card{
  border:1px solid rgba(201,168,76,.2);border-radius:5px;
  padding:14px 18px;margin:1.2em 0;break-inside:avoid;
  background:rgba(201,168,76,.03);
}
.context-card .context-label{
  font-family:var(--sans);font-size:.55rem;font-weight:700;
  letter-spacing:2px;color:var(--gold);margin-bottom:6px;
}
.context-card p{text-indent:0!important;font-size:.9rem;margin-bottom:0}

/* ═══ ERROR/WARNING CARD ═══ */
.error-card{
  border-left:3px solid var(--red);
  padding:10px 16px;margin:1em 0;
  background:rgba(168,48,48,.03);border-radius:0 4px 4px 0;
  break-inside:avoid;
}
.error-card .error-label{
  font-family:var(--sans);font-size:.55rem;font-weight:700;
  letter-spacing:2px;color:var(--red);margin-bottom:4px;
}
.error-card p{text-indent:0!important;font-size:.9rem;margin-bottom:0}

/* ═══ SPOTLIGHT BOX ═══ */
.spotlight-box{
  background:linear-gradient(135deg,var(--navy),var(--navy2));
  border-left:4px solid var(--gold);border-radius:4px;
  padding:22px 26px;margin:2.2em 0;
}
.spotlight-label{
  font-family:var(--sans);font-size:.55rem;font-weight:700;
  letter-spacing:3px;color:var(--gold);margin-bottom:10px;
}
.spotlight-text{font-style:italic;color:#fff;font-size:.95rem;line-height:1.6;margin:0}

/* ═══ PULL QUOTE ═══ */
.pull-quote{
  text-align:center;margin:2.5em auto;max-width:400px;padding:20px 10px;
  border-top:1px solid var(--gold-dim);border-bottom:1px solid var(--gold-dim);
}
.pull-quote p{
  font-family:var(--sans);font-size:1rem;font-weight:600;
  font-style:italic;color:var(--gold);line-height:1.5;
  text-indent:0!important;text-align:center!important;margin:0;
}

/* ═══ PATTERN INTERRUPT ═══ */
.pattern-interrupt{
  background:linear-gradient(180deg,#060B14,var(--navy2));
  min-height:100vh;display:flex;align-items:center;justify-content:center;
  padding:60px 40px;break-before:page;break-after:page;
}
.pi-content{text-align:center;max-width:440px}
.pi-number{
  font-family:var(--sans);font-size:5rem;font-weight:200;
  color:var(--gold);text-shadow:0 0 35px rgba(201,168,76,.18);letter-spacing:3px;
}
.pi-unit{font-family:var(--sans);font-size:.72rem;letter-spacing:4px;color:var(--gold);font-weight:300;margin-bottom:18px}
.pi-text{font-style:italic;color:var(--gray-blue);font-size:.82rem;line-height:1.65;margin:22px 0 12px}
.pi-source{font-size:.6rem;color:var(--dim);margin-bottom:25px}
.pi-wyajd{
  color:#fff;font-style:italic;font-size:.75rem;margin-top:28px;line-height:1.55;
  border-top:1px solid rgba(201,168,76,.25);padding-top:18px;
}

/* ═══ WHAT YOU JUST DID ═══ */
.wyajd{display:flex;gap:14px;margin:2.2em 0;padding:14px 0 14px 18px}
.wyajd-bar{width:3px;background:var(--gold);opacity:.6;flex-shrink:0;border-radius:2px}
.wyajd-text{font-style:italic;font-size:.88rem;line-height:1.55;margin:0;text-indent:0!important}

/* ═══ KEY READ ═══ */
.key-read{display:block;width:100%;margin:3em 0 1.5em;text-align:center}
.kr-rule{width:180px;height:1px;background:var(--gold);opacity:.35;margin:0 auto}
.kr-text{
  font-style:italic;color:var(--gold);font-size:.92rem;
  font-weight:600;line-height:1.55;padding:18px 8px;margin:0;
  text-indent:0!important;text-align:center!important;
}

/* ═══ GOLD / META ═══ */
.gold,em.gold{color:var(--gold);font-weight:600;font-style:normal}

.meta-summary{margin:2em 0}
.meta-row{
  display:flex;justify-content:space-between;align-items:baseline;
  padding:9px 0;border-bottom:1px solid rgba(201,168,76,.12);font-size:.88rem;
}
.meta-label{font-family:var(--sans);font-size:.58rem;letter-spacing:2px;color:var(--dim);text-transform:uppercase}

.meta-finale{text-align:center;margin:4.5em 0;padding:45px 20px}
.finale-1{color:var(--gold);font-size:1.08rem;font-style:italic;margin:0 0 2em!important;text-indent:0!important;text-align:center!important}
.finale-2{
  color:var(--gold);font-size:1.18rem;font-style:italic;font-weight:600;
  margin:0 0 2.5em!important;text-indent:0!important;text-align:center!important;
  text-shadow:0 0 25px rgba(201,168,76,.12);
}
.finale-3{
  font-family:var(--sans);font-size:1.05rem;font-weight:700;
  letter-spacing:4px;text-transform:uppercase;color:var(--gold);
  margin:0!important;text-indent:0!important;text-align:center!important;
}

/* ═══ PAGE FOOTER ═══ */
.page-footer{
  font-family:var(--sans);font-size:.45rem;letter-spacing:3.5px;
  color:var(--dim);text-align:center;padding:28px 0 8px;margin-top:35px;
}

/* ═══ TOC ═══ */
.toc{max-width:480px;margin:0 auto;padding:60px 36px;break-after:page}
.toc h2{
  font-family:var(--sans);font-size:.85rem;font-weight:700;
  letter-spacing:7px;color:var(--gold);text-align:center;margin-bottom:3em;text-transform:uppercase;
}
.toc-list{list-style:none}
.toc-part{
  font-family:var(--sans);font-size:.62rem;font-weight:700;
  letter-spacing:3px;color:var(--dim);margin:2em 0 .3em;
  padding-top:1em;border-top:1px solid var(--rule);
}
.toc-sub{display:block;font-weight:400;letter-spacing:1px;font-size:.58rem;color:var(--gray-blue);margin-top:2px}
a.toc-ch{
  display:flex;align-items:baseline;padding:5px 0 5px 16px;font-size:.82rem;
  text-decoration:none;color:inherit;cursor:pointer;transition:opacity .2s;
}
a.toc-ch:hover{opacity:.7}
.toc-num{color:var(--gold);font-weight:600;min-width:32px;flex-shrink:0}
.toc-title{flex-shrink:0}
.toc-dots{
  flex-grow:1;margin:0 8px;
  border-bottom:1px dotted var(--rule);min-width:20px;
}

/* ═══ SIGNAL KEY ═══ */
.signal-key{
  max-width:100%;margin:0;padding:60px calc(50% - 260px);break-before:page;
  background:linear-gradient(180deg,var(--navy),var(--navy2));
  min-height:100vh;box-sizing:border-box;
}
.signal-key h2{
  font-family:var(--sans);font-size:.85rem;font-weight:700;
  letter-spacing:7px;color:var(--gold);text-align:center;
  margin-bottom:1.5em;text-transform:uppercase;
}
.signal-key .sk-intro{
  font-family:var(--serif);font-size:.9rem;font-style:italic;
  color:rgba(245,240,232,.55);line-height:1.7;text-align:center;
  margin-bottom:2.5em;
}
.signal-key .sk-section{margin-bottom:2.5em}
.signal-key .sk-section h3{
  font-family:var(--sans);font-size:.68rem;font-weight:700;
  letter-spacing:4px;color:rgba(138,154,181,.9);text-transform:uppercase;
  margin-bottom:.6em;padding-bottom:.5em;
  border-bottom:1px solid var(--rule);
}
.signal-key .sk-desc{
  font-family:var(--serif);font-size:.88rem;color:rgba(245,240,232,.72);
  line-height:1.65;margin-bottom:1.5em;
}
.signal-key .sk-grid{display:flex;flex-direction:column;gap:18px}
.signal-key .sk-item{
  display:grid;grid-template-columns:60px 1fr;grid-template-rows:auto auto;
  column-gap:16px;row-gap:2px;align-items:start;
}
.signal-key .sk-item .badge{
  grid-row:1/3;align-self:center;justify-self:center;
  font-size:.6rem;padding:3px 10px;
}
.signal-key .sk-item .sk-icon{
  grid-row:1/3;align-self:center;justify-self:center;
  display:flex;align-items:center;gap:6px;
}
.signal-key .sk-item .sk-icon svg{width:22px;height:22px;opacity:.8}
.signal-key .sk-label{
  font-family:var(--sans);font-size:.75rem;font-weight:600;
  color:var(--gold);letter-spacing:1px;
}
.signal-key .sk-explain{
  font-family:var(--serif);font-size:.82rem;color:rgba(245,240,232,.5);
  line-height:1.55;
}
/* ═══ COMPACT TIER TABLE ═══ */
.tier-table{width:100%;border-collapse:collapse;margin:.5em 0 1.8em}
.tier-table tr{border-bottom:1px solid rgba(138,154,181,.1)}
.tier-table tr:last-child{border-bottom:none}
.tier-table td{padding:11px 14px;vertical-align:top}
.tier-table .tt-badge-cell{width:52px;padding-right:0;vertical-align:middle}
.tier-table .tt-name{
  font-family:var(--sans);font-size:.67rem;letter-spacing:2px;
  font-weight:700;color:#fff;text-transform:uppercase;margin-bottom:4px;
}
.tier-table .tt-desc{
  font-family:var(--serif);font-size:.85rem;color:rgba(245,240,232,.78);
  line-height:1.6;
}
.tier-table .tt-ex{
  font-family:var(--serif);font-style:italic;font-size:.8rem;
  color:rgba(201,168,76,.75);margin-top:5px;
}

/* ═══ FRONT MATTER ═══ */
.front-matter{max-width:520px;margin:0 auto;padding:60px 36px;break-before:page}
.front-matter h2{
  font-family:var(--sans);font-size:1rem;font-weight:700;
  letter-spacing:5px;color:var(--gold);text-align:center;margin-bottom:2.5em;
}
.front-matter p{margin-bottom:.9em;font-size:.92rem;line-height:1.6}

/* ═══ ACKNOWLEDGMENT NAME GLOW ═══ */
.ack-name{
  color:var(--gold);
  text-shadow:0 0 8px rgba(201,168,76,.35), 0 0 20px rgba(201,168,76,.15);
}

/* ═══ TITLE PAGE (after acknowledgments) ═══ */
.title-page{
  break-before:page;display:flex;flex-direction:column;align-items:center;
  justify-content:center;min-height:80vh;text-align:center;
  padding:80px 36px;max-width:520px;margin:0 auto;
}
.title-page .tp-brand{
  font-family:var(--sans);font-size:.55rem;font-weight:700;
  letter-spacing:6px;color:var(--dim);margin-bottom:40px;
}
.title-page .tp-title{
  font-family:var(--sans);font-size:1.8rem;font-weight:700;
  letter-spacing:5px;color:var(--gold);line-height:1.35;margin-bottom:12px;
  text-shadow:0 0 40px rgba(201,168,76,.12);
}
.title-page .tp-subtitle{
  font-family:var(--serif);font-size:.95rem;font-style:italic;
  color:rgba(245,240,232,.55);line-height:1.6;margin-bottom:6px;
}
.title-page .tp-edition{
  font-family:var(--sans);font-size:.5rem;font-weight:600;
  letter-spacing:4px;color:var(--dim);margin-bottom:40px;
}
.title-page .tp-rule{
  width:120px;height:1px;margin:0 auto 32px;
  background:linear-gradient(90deg,transparent,rgba(201,168,76,.35),transparent);
}
.title-page .tp-author{
  font-family:var(--sans);font-size:1rem;font-weight:700;
  letter-spacing:4px;color:var(--gold);margin-bottom:8px;
}
.title-page .tp-roles{
  font-family:var(--sans);font-size:.55rem;letter-spacing:2px;
  color:var(--gray-blue);line-height:1.8;margin-bottom:4px;
}
.title-page .tp-dots{
  font-size:.7rem;color:var(--dim);margin:28px 0;letter-spacing:12px;
}
.title-page .tp-quote{
  font-family:var(--serif);font-size:1rem;font-style:italic;
  color:rgba(42,37,32,.72);line-height:1.7;max-width:400px;margin-bottom:8px;
}
.title-page .tp-attribution{
  font-family:var(--sans);font-size:.6rem;letter-spacing:3px;
  color:var(--dim);font-weight:600;
}

/* ═══ DEFINITIONS PAGE ═══ */
.definitions{
  max-width:440px;margin:0 auto;padding:100px 36px 60px;
  text-align:center;break-before:page;break-after:page;
}
.def-word{font-family:var(--sans);font-size:.85rem;letter-spacing:5px;color:var(--dim);margin-bottom:6px}
.def-phonetic{font-size:.72rem;color:var(--gray-blue);margin-bottom:3px}
.def-pos{font-size:.72rem;color:var(--dim);font-style:italic;margin-bottom:14px}
.def-meaning{font-size:.88rem;line-height:1.65;max-width:380px;margin:0 auto 50px}

/* ═══ OBSERVATION TABLE ═══ */
.obs-table-wrap{
  margin:2em 0;font-size:.72rem;
  background:var(--navy2);border-radius:5px;overflow:hidden;
  break-inside:auto;
}
.obs-table-header{
  display:grid;
  grid-template-columns:28px 1fr 1fr 40px 52px;
  gap:0 10px;
  background:rgba(201,168,76,.1);
  padding:8px 14px;
  border-bottom:1px solid rgba(201,168,76,.2);
}
.obs-th{
  font-family:var(--sans);font-size:.48rem;font-weight:700;
  letter-spacing:2px;color:var(--gold);text-transform:uppercase;
}
.obs-row-wrap,.obs-row-alt{
  display:grid;
  grid-template-columns:28px 1fr 1fr 40px 52px;
  gap:0 10px;align-items:center;
  padding:6px 14px;
  border-bottom:1px solid rgba(255,255,255,.04);
}
.obs-row-alt{background:rgba(255,255,255,.02)}
.obs-num-cell{
  font-family:var(--sans);font-size:.55rem;font-weight:700;
  color:var(--gold);opacity:.7;
}
.obs-name-cell{
  font-family:var(--sans);font-size:.65rem;font-weight:500;
  color:#fff;line-height:1.3;
}
.obs-what-cell{
  font-size:.65rem;color:var(--gray-blue);line-height:1.3;
  text-indent:0!important;text-align:left!important;
}
.obs-tier-cell{text-align:center}
.obs-use-cell{
  font-family:var(--sans);font-size:.5rem;font-weight:700;
  letter-spacing:.5px;
}
.use-badge{display:inline-block;margin-right:2px}

/* ═══ BTE SIGNAL CARDS ═══ */
.bte-signal{
  display:grid;grid-template-columns:1fr;
  padding:12px 18px;margin:0;
  border-bottom:1px solid rgba(255,255,255,.06);
  background:#0d1117;
}
.bte-signal:last-child{border-bottom:none;}
.bte-cluster-wrap{
  background:#0d1117;border-radius:6px;
  margin:1.6em 0;overflow:hidden;
  border:1px solid rgba(255,255,255,.07);
  break-inside:auto;
}
.bte-cluster-header{
  padding:12px 18px;
  background:#0a0e14;
  border-bottom:1px solid rgba(201,168,76,.2);
}
.bte-cluster-name{
  font-family:var(--sans);font-size:.68rem;font-weight:700;
  letter-spacing:2px;color:var(--gold);margin-bottom:3px;
}
.bte-cluster-desc{font-size:.75rem;color:#7a8ba8;font-style:italic}
.bte-signal-head{
  display:flex;align-items:baseline;gap:10px;margin-bottom:5px;
}
.bte-name{
  font-family:var(--sans);font-size:.78rem;font-weight:700;color:#e8eef5;
}
.bte-code{
  font-family:var(--sans);font-size:.62rem;font-weight:600;
  color:#4a5e7a;letter-spacing:1px;
}
.bte-drs{
  font-family:var(--sans);font-size:.62rem;font-weight:700;
  letter-spacing:.5px;margin-left:auto;flex-shrink:0;
}
.bte-desc{
  font-size:.78rem;color:#7a8ba8;
  line-height:1.6;margin:0;
  text-indent:0!important;text-align:left!important;
}
/* ── SIX-CATEGORY RADAR ── */
.radar-category{
  background:linear-gradient(135deg,rgba(13,30,48,.95),rgba(8,15,26,.98));
  border:1px solid rgba(26,143,168,.18);
  border-left:4px solid #1A8FA8;
  border-radius:6px;
  padding:14px 18px;
  margin:1.2em 0;
  break-inside:avoid;
}
.rc-header{
  display:flex;align-items:center;gap:10px;
  margin-bottom:10px;padding-bottom:8px;
  border-bottom:1px solid rgba(26,143,168,.18);
}
.rc-num{
  font-family:var(--sans);font-size:.6rem;font-weight:700;
  color:#1A8FA8;letter-spacing:.1em;
  background:rgba(26,143,168,.15);
  padding:2px 7px;border-radius:3px;
}
.rc-title{
  font-family:var(--sans);font-size:.75rem;font-weight:700;
  letter-spacing:.08em;color:#d0e8f0;text-transform:uppercase;
}
.rc-signals{
  display:flex;flex-wrap:wrap;gap:5px 7px;margin-bottom:8px;
}
.rc-signal{
  display:inline-flex;align-items:center;gap:4px;
  background:rgba(26,143,168,.08);
  border:1px solid rgba(26,143,168,.2);
  border-radius:3px;padding:3px 7px;
}
.rc-name{
  font-size:.7rem;color:rgba(208,232,240,.9);
}
.rc-insight{
  margin:6px 0 0;font-size:.78rem;color:rgba(26,143,168,.9);
  font-style:italic;line-height:1.55;
  border-top:1px solid rgba(26,143,168,.15);
  padding-top:7px;
  text-indent:0!important;text-align:left!important;
}
/* ── VOLUNTEER TYPE CARDS ── */
.volunteer-card{
  background:linear-gradient(135deg,rgba(8,15,26,.85),rgba(13,30,48,.95));
  border-left:3px solid var(--vc-color,var(--gold));
  border-radius:6px;
  padding:14px 18px;
  margin:.9em 0;
  break-inside:avoid;
}
.vc-header{
  margin-bottom:9px;padding-bottom:7px;
  border-bottom:1px solid rgba(255,255,255,.08);
}
.vc-name{
  font-family:var(--sans);font-size:.78rem;font-weight:700;
  letter-spacing:.07em;color:var(--vc-color,var(--gold));
  text-transform:uppercase;
}
.vc-desc{
  font-size:.8rem;color:rgba(255,255,255,.85);
  line-height:1.55;margin:0 0 9px;
  text-indent:0!important;text-align:left!important;
}
.vc-signals{display:flex;flex-wrap:wrap;gap:5px 6px;margin-bottom:9px}
.vc-chip{
  display:inline-block;
  background:rgba(255,255,255,.05);
  border:1px solid rgba(255,255,255,.1);
  border-radius:3px;padding:2px 8px;
  font-size:.7rem;color:rgba(255,255,255,.75);
}
.vc-meta{
  border-top:1px solid rgba(255,255,255,.06);
  padding-top:8px;display:flex;gap:16px;flex-wrap:wrap;
}
.vc-works,.vc-avoid{font-size:.75rem;color:var(--gray-blue);line-height:1.45}
.vc-meta-label{
  font-family:var(--sans);font-size:.6rem;font-weight:700;
  letter-spacing:.08em;text-transform:uppercase;margin-right:3px;
}
.vc-works .vc-meta-label{color:var(--blue)}
.vc-avoid .vc-meta-label{color:#A83030}
/* ── VOLUNTEER SELECTION MATRIX ── */
.vm-cell{
  background:var(--vm-bg,linear-gradient(135deg,rgba(42,28,6,.95),rgba(52,36,8,.98)));
  border:1px solid var(--vm-glow,rgba(201,168,76,.15));
  border-left:4px solid var(--vm-color,#C9A84C);
  border-radius:6px;
  padding:16px 18px;
  margin:.6em 0;
  break-inside:avoid;
  box-shadow:0 2px 12px var(--vm-glow,rgba(201,168,76,.08));
}
.vm-heading{
  font-family:var(--sans);font-size:.62rem;font-weight:700;
  letter-spacing:.1em;text-transform:uppercase;
  color:rgba(220,190,140,.6);margin-bottom:5px;
}
.vm-rec{
  font-family:var(--sans);font-size:.75rem;font-weight:700;
  color:var(--vm-color,#C9A84C);letter-spacing:.04em;margin-bottom:7px;
}
.vm-body{
  font-size:.78rem;color:rgba(220,200,170,.75);line-height:1.55;
  margin:0;text-indent:0!important;text-align:left!important;
}
.bte-application{
  padding:12px 16px;background:rgba(201,168,76,.04);
  border-top:1px solid rgba(201,168,76,.12);
}
.bte-app-label{
  font-family:var(--sans);font-size:.48rem;font-weight:700;
  letter-spacing:2.5px;color:var(--gold);margin-bottom:5px;
  text-transform:uppercase;
}
.bte-app-text{
  font-size:.72rem;color:var(--gray-blue);line-height:1.55;
  margin:0;text-indent:0!important;text-align:left!important;
}

/* ═══ BACK COVER ═══ */
.back-cover{
  background:linear-gradient(180deg,var(--navy),var(--navy2));
  min-height:100vh;display:flex;flex-direction:column;
  align-items:center;justify-content:center;padding:60px 40px;
  break-before:page;
}
.back-blurb{
  color:var(--gray-blue);font-style:italic;font-size:.78rem;
  max-width:380px;text-align:center;line-height:1.65;margin:18px 0;
}
.hidden-text{color:rgba(255,255,255,.06);font-style:italic;font-size:.68rem;margin-top:35px}

/* ═══ FIVE Cs FRAMEWORK ═══ */
.five-cs-graphic{margin:20px 0 0;line-height:0}
.disc-chart{margin:1.8em 0;break-inside:avoid}
/* ── DISC TYPE CARDS ── */
.disc-type-card{
  border-left:3px solid var(--disc-color,var(--gold));
  background:linear-gradient(135deg,rgba(8,15,26,.85),rgba(13,30,48,.95));
  border-radius:6px;padding:14px 18px;margin:.9em 0;break-inside:avoid;
}
.disc-type-header{
  display:flex;align-items:center;gap:12px;
  margin-bottom:10px;padding-bottom:8px;
  border-bottom:1px solid rgba(255,255,255,.08);
}
.disc-letter{
  font-family:var(--sans);font-size:1.6rem;font-weight:700;
  color:var(--disc-color,var(--gold));line-height:1;
  width:36px;text-align:center;flex-shrink:0;
}
.disc-name{
  font-family:var(--sans);font-size:.8rem;font-weight:700;
  letter-spacing:.1em;color:#fff;text-transform:uppercase;
}
.disc-traits{display:flex;flex-wrap:wrap;gap:5px 6px;margin-bottom:10px}
.disc-trait{
  display:inline-block;
  background:rgba(255,255,255,.06);
  border:1px solid rgba(255,255,255,.12);
  border-radius:3px;padding:2px 9px;
  font-size:.72rem;color:rgba(255,255,255,.8);
}
.disc-onstage{
  background:rgba(255,255,255,.04);
  border-left:2px solid var(--disc-color,var(--gold));
  border-radius:0 4px 4px 0;
  padding:7px 12px;margin-bottom:10px;
  font-size:.78rem;color:rgba(255,255,255,.85);line-height:1.5;
}
.disc-onstage-label{
  font-family:var(--sans);font-size:.6rem;font-weight:700;
  letter-spacing:.1em;text-transform:uppercase;
  color:var(--disc-color,var(--gold));margin-right:6px;
}
.disc-sigs{display:flex;flex-wrap:wrap;gap:4px 6px;margin-top:6px}
.disc-sig{
  display:inline-block;
  font-size:.68rem;color:var(--disc-color,var(--gold));
  border:1px solid var(--disc-color,var(--gold));
  border-radius:10px;padding:1px 8px;
  opacity:.8;
}
/* ── DISC BLEND CARDS ── */
.disc-blend-card{
  border-top:2px solid;
  border-image:linear-gradient(90deg,var(--blend-color1),var(--blend-color2)) 1;
  background:rgba(13,30,48,.9);
  border-radius:0 0 5px 5px;
  padding:12px 16px;margin:.7em 0;break-inside:avoid;
}
.disc-blend-header{margin-bottom:8px}
.disc-blend-name{
  font-family:var(--sans);font-size:.75rem;font-weight:700;
  letter-spacing:.08em;color:#fff;
}
.disc-blend-desc{
  font-size:.78rem;color:rgba(255,255,255,.8);line-height:1.55;
  margin:0 0 8px;text-indent:0!important;text-align:left!important;
}
.disc-strategy{
  font-size:.75rem;color:var(--gray-blue);
  margin-top:8px;padding-top:7px;
  border-top:1px solid rgba(255,255,255,.06);
}
.disc-strategy-label{
  font-family:var(--sans);font-size:.6rem;font-weight:700;
  letter-spacing:.08em;text-transform:uppercase;
  color:var(--gold);margin-right:5px;
}
/* ── VIDEO EMBEDS ── */
.video-embed{margin:2em 0;break-inside:avoid}
.video-label{
  font-family:var(--sans);font-size:.65rem;font-weight:700;
  letter-spacing:.1em;text-transform:uppercase;
  color:var(--gold);margin-bottom:8px;
}
.video-frame-wrap{
  position:relative;width:100%;padding-bottom:56.25%;
  background:#000;border-radius:5px;overflow:hidden;
}
.video-frame-wrap iframe{
  position:absolute;top:0;left:0;width:100%;height:100%;
  border:none;
}
.video-caption{
  font-size:.78rem;color:var(--gray-blue);font-style:italic;
  margin-top:8px;line-height:1.5;
  text-indent:0!important;text-align:left!important;
}
.disc-graphic{line-height:0}
.disc-graphic svg{width:100%;height:auto;border-radius:6px;display:block}

/* Reference table */
.five-cs-table{
  width:100%;border-collapse:collapse;
  margin:18px 0 0;font-size:.78rem;
  background:var(--navy2);border-radius:4px;overflow:hidden;
}
.five-cs-table thead tr{background:rgba(201,168,76,.12)}
.five-cs-table th{
  font-family:var(--sans);font-size:.52rem;font-weight:700;
  letter-spacing:2.5px;text-transform:uppercase;
  color:var(--gold);padding:9px 14px;text-align:left;
  border-bottom:1px solid rgba(201,168,76,.2);
}
.five-cs-table td{
  padding:9px 14px;color:var(--gray-blue);
  font-size:.78rem;line-height:1.45;
  border-bottom:1px solid rgba(255,255,255,.05);
  text-align:left!important;text-indent:0!important;
}
.five-cs-table .c-name{
  font-family:var(--sans);font-weight:700;font-size:.7rem;
  letter-spacing:1px;white-space:nowrap;
}
.five-cs-table .c-rule-cell{font-style:italic}
.five-cs-table tr[data-c="context"] .c-name{color:#A83030}
.five-cs-table tr[data-c="clusters"] .c-name{color:#E8C870}
.five-cs-table tr[data-c="congruence"] .c-name{color:var(--blue)}
.five-cs-table tr[data-c="consistency"] .c-name{color:var(--purple)}
.five-cs-table tr[data-c="culture"] .c-name{color:var(--gold)}
.five-cs-table tr[data-c="context"] .c-rule-cell{color:#A83030}
.five-cs-table tr[data-c="clusters"] .c-rule-cell{color:#E8C870}
.five-cs-table tr[data-c="congruence"] .c-rule-cell{color:var(--blue)}
.five-cs-table tr[data-c="consistency"] .c-rule-cell{color:var(--purple)}
.five-cs-table tr[data-c="culture"] .c-rule-cell{color:var(--gold)}

/* ═══ FIVE Cs FRAMEWORK ═══ */
.five-cs-framework{
  background:linear-gradient(135deg,var(--navy),var(--navy2));
  border-radius:6px;padding:32px 28px;margin:2.5em 0;
  break-inside:avoid;
}
.five-cs-header{text-align:center;margin-bottom:24px}
.five-cs-title{
  font-family:var(--sans);font-size:.72rem;font-weight:700;
  letter-spacing:4px;color:var(--gold);margin-bottom:6px;
}
.five-cs-subtitle{font-size:.72rem;color:var(--gray-blue);font-style:italic}

.five-cs-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-bottom:24px}
@media(max-width:768px){.five-cs-grid{grid-template-columns:1fr;gap:8px}}

.five-cs-card{border-radius:4px;overflow:hidden}
.c-tab{
  font-family:var(--sans);font-size:.58rem;font-weight:700;
  letter-spacing:2px;text-align:center;padding:7px 4px;
}
.c-body{padding:12px 10px;background:rgba(13,30,48,.8);border-top:2px solid transparent}
.c-question{font-size:.7rem;font-weight:700;color:#fff;margin-bottom:6px}
.c-desc{font-size:.65rem;color:var(--gray-blue);line-height:1.5;margin-bottom:8px;text-indent:0!important;text-align:left!important}
.c-rule{font-size:.62rem;font-style:italic;margin:0;text-indent:0!important;text-align:left!important}

/* Card colors — each C gets its own accent */
[data-c="context"] .c-tab{background:rgba(168,48,48,.2);color:#A83030}
[data-c="context"] .c-body{border-top-color:#A83030}
[data-c="context"] .c-rule{color:#A83030}

[data-c="clusters"] .c-tab{background:rgba(232,200,112,.12);color:#E8C870}
[data-c="clusters"] .c-body{border-top-color:#E8C870}
[data-c="clusters"] .c-rule{color:#E8C870}

[data-c="congruence"] .c-tab{background:rgba(26,143,168,.12);color:var(--blue)}
[data-c="congruence"] .c-body{border-top-color:var(--blue)}
[data-c="congruence"] .c-rule{color:var(--blue)}

[data-c="consistency"] .c-tab{background:rgba(107,82,160,.12);color:var(--purple)}
[data-c="consistency"] .c-body{border-top-color:var(--purple)}
[data-c="consistency"] .c-rule{color:var(--purple)}

[data-c="culture"] .c-tab{background:rgba(201,168,76,.1);color:var(--gold)}
[data-c="culture"] .c-body{border-top-color:var(--gold)}
[data-c="culture"] .c-rule{color:var(--gold)}

/* Chain flow */
.five-cs-chain{text-align:center;margin-top:20px}
.chain-label{font-family:var(--sans);font-size:.62rem;font-weight:700;color:#fff;letter-spacing:1.5px;margin-bottom:14px}
.chain-flow{display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:6px;margin-bottom:14px}
.chain-pill{
  font-family:var(--sans);font-size:.58rem;font-weight:700;
  padding:4px 12px;border-radius:12px;
}
[data-c="context"].chain-pill{background:rgba(168,48,48,.18);color:#A83030}
[data-c="clusters"].chain-pill{background:rgba(232,200,112,.12);color:#E8C870}
[data-c="congruence"].chain-pill{background:rgba(26,143,168,.12);color:var(--blue)}
[data-c="consistency"].chain-pill{background:rgba(107,82,160,.12);color:var(--purple)}
[data-c="culture"].chain-pill{background:rgba(201,168,76,.1);color:var(--gold)}
.chain-read{background:rgba(255,255,255,.08);color:#fff}
.chain-arrow{color:var(--dim);font-size:.8rem}
.chain-note{font-size:.65rem;color:var(--gray-blue);margin:0 0 4px;text-indent:0!important;text-align:center!important}
.chain-note-gold{font-size:.65rem;color:var(--gold);font-style:italic;margin:0;text-indent:0!important;text-align:center!important}

/* ═══ COLOR TEMPERATURE ARC (cool blue → warm gold) ═══ */
/* Parts 1-2: Clinical steel blue */
[data-part="1"] .section-header.sh-standard,[data-part="2"] .section-header.sh-standard{border-bottom-color:var(--blue)}
[data-part="1"] .section-header.sh-section,[data-part="2"] .section-header.sh-section{border-left-color:var(--blue)}
[data-part="1"] .section-header.sh-label,[data-part="2"] .section-header.sh-label{color:var(--blue)}
[data-part="1"] .section-header.sh-label::before,[data-part="1"] .section-header.sh-label::after,
[data-part="2"] .section-header.sh-label::before,[data-part="2"] .section-header.sh-label::after{
  background:linear-gradient(90deg,transparent,rgba(26,143,168,.3),transparent)
}
[data-part="1"] .felt-before,[data-part="2"] .felt-before{border-color:rgba(26,143,168,.25)}
[data-part="1"] .felt-label,[data-part="2"] .felt-label{color:var(--blue)}
[data-part="1"] .obs-ref,[data-part="2"] .obs-ref{color:var(--blue)}
/* Part 3: Transitional — blue-gold blend */
[data-part="3"] .section-header.sh-standard{border-bottom-color:#8BAAB8}
[data-part="3"] .section-header.sh-section{border-left-color:#8BAAB8}
[data-part="3"] .section-header.sh-label{color:#9BA870}
[data-part="3"] .chapter-number{color:#B8A060}
/* Parts 4-5: Applied gold — mastery */
[data-part="4"] .key-read .kr-text,[data-part="5"] .key-read .kr-text{color:#C9A84C}
[data-part="4"] .chapter-number,[data-part="5"] .chapter-number{color:var(--gold)}
/* Parts 6-7: Authority — deep warm gold */
[data-part="6"] .section-header.sh-standard,[data-part="7"] .section-header.sh-standard{border-bottom-color:#D4A030}
[data-part="6"] .section-header.sh-section,[data-part="7"] .section-header.sh-section{border-left-color:#D4A030}
[data-part="6"] .section-header.sh-label,[data-part="7"] .section-header.sh-label{color:#D4A030}
[data-part="6"] .chapter-number,[data-part="7"] .chapter-number{color:#D4A030}
[data-part="6"] .spotlight-box,[data-part="7"] .spotlight-box{border-left-color:#D4A030}
[data-part="6"] .key-read .kr-text,[data-part="7"] .key-read .kr-text{color:#D4A030}
/* Part 8: Full command — amber */
[data-part="8"] .section-header.sh-standard{border-bottom-color:#C8901A}
[data-part="8"] .section-header.sh-section{border-left-color:#C8901A}
[data-part="8"] .section-header.sh-label{color:#C8901A}
[data-part="8"] .chapter-number{color:#C8901A}
[data-part="8"] .spotlight-box{border-left-color:#C8901A}
[data-part="8"] .key-read .kr-text{color:#C8901A}

/* ═══ FIVE Cs PROSE CHART ═══ */
.five-cs-prose-chart{
  background:linear-gradient(160deg,var(--navy),var(--navy2));
  border-radius:6px;margin:2.5em 0;
  overflow:hidden;break-inside:avoid;
}
.fcp-header{
  padding:20px 22px 14px;
  border-bottom:1px solid rgba(201,168,76,.15);
}
.fcp-title{
  font-family:var(--sans);font-size:.68rem;font-weight:700;
  letter-spacing:4px;color:var(--gold);margin-bottom:4px;
}
.fcp-subtitle{
  font-size:.7rem;color:var(--gray-blue);font-style:italic;
}
.fcp-footer{
  padding:14px 22px;
  border-top:1px solid rgba(201,168,76,.12);
  text-align:center;
}
.fcp-chain{
  font-family:var(--sans);font-size:.55rem;font-weight:600;
  letter-spacing:1.5px;color:var(--dim);
}
.fcp-read{color:var(--gold);font-weight:700;letter-spacing:2px;}
.five-c-entry{
  padding:14px 22px 14px 20px;
  border-left:none;border-radius:0;margin:0;
  border-bottom:1px solid rgba(255,255,255,.04);
  break-inside:avoid;
}
.five-c-entry:last-of-type{border-bottom:none}
.five-c-entry .fce-head{
  display:flex;align-items:baseline;gap:10px;
  margin-bottom:8px;
}
.five-c-entry .fce-name{
  font-family:var(--sans);font-size:.78rem;font-weight:700;
  letter-spacing:1.5px;flex-shrink:0;
}
.five-c-entry .fce-dash{color:var(--gray-blue);font-weight:300;flex-shrink:0}
.five-c-entry .fce-question{
  font-family:var(--sans);font-size:.7rem;font-weight:500;
  color:#fff;letter-spacing:.3px;
}
.five-c-entry .fce-body{
  font-family:var(--serif);font-size:.92rem;line-height:1.6;
  color:var(--gray-blue);text-indent:0!important;text-align:left!important;margin:0;
}
/* Per-C colors */
.five-c-entry[data-c="context"]{background:rgba(168,48,48,.07);border-left:3px solid #A83030}
.five-c-entry[data-c="context"] .fce-name{color:#A83030}
.five-c-entry[data-c="clusters"]{background:rgba(232,200,112,.06);border-left:3px solid #E8C870}
.five-c-entry[data-c="clusters"] .fce-name{color:#E8C870}
.five-c-entry[data-c="congruence"]{background:rgba(26,143,168,.07);border-left:3px solid var(--blue)}
.five-c-entry[data-c="congruence"] .fce-name{color:var(--blue)}
.five-c-entry[data-c="consistency"]{background:rgba(107,82,160,.07);border-left:3px solid var(--purple)}
.five-c-entry[data-c="consistency"] .fce-name{color:var(--purple)}
.five-c-entry[data-c="culture"]{background:rgba(201,168,76,.06);border-left:3px solid var(--gold)}
.five-c-entry[data-c="culture"] .fce-name{color:var(--gold)}

/* ═══ PERFORMER'S NOTE ═══ */
.performer-note-header{
  display:flex;align-items:center;gap:10px;
  margin:2.2em 0 .7em;
  padding:10px 14px;
  border-left:3px solid var(--blue);
  background:rgba(26,143,168,.04);
  border-radius:0 4px 4px 0;
}
.performer-note-header::before{
  content:"✦";
  font-size:.7rem;color:var(--blue);flex-shrink:0;opacity:.8;
}
.performer-note-header .pn-label{
  font-family:var(--sans);font-size:.58rem;font-weight:700;
  letter-spacing:3px;color:var(--blue);text-transform:uppercase;
  font-style:normal;
}

/* ═══ CERTAINTY FRAMES ═══ */
.certainty-frame{
  border-left:4px solid var(--cf-color,#C9A84C);
  border-radius:0 6px 6px 0;
  padding:14px 16px 12px;
  margin:.5em 0;
  break-inside:avoid;
  background:linear-gradient(135deg,var(--navy,#080F1A),var(--navy2,#0D1E30));
  border-top:1px solid rgba(255,255,255,.06);
  border-bottom:1px solid rgba(255,255,255,.06);
  border-right:1px solid rgba(255,255,255,.06);
}
.cf-header{
  display:flex;align-items:baseline;gap:10px;margin-bottom:8px;
}
.cf-name{
  font-family:var(--sans);font-size:.72rem;font-weight:700;
  color:var(--cf-color,#C9A84C);letter-spacing:.05em;text-transform:uppercase;
}
.cf-tier{
  font-family:var(--sans);font-size:.55rem;font-weight:600;
  color:rgba(138,154,181,.7);letter-spacing:.08em;text-transform:uppercase;
}
.cf-use{
  font-family:var(--serif);font-size:.84rem;color:rgba(245,240,232,.85);
  line-height:1.6;margin-bottom:8px;
}
.cf-lines{
  display:flex;flex-direction:column;gap:4px;margin:8px 0;
  padding:8px 12px;
  background:rgba(0,0,0,.25);border-radius:4px;
}
.cf-line{
  font-family:var(--serif);font-style:italic;font-size:.84rem;
  color:var(--cf-color,#C9A84C);line-height:1.55;
}
.cf-avoid{
  font-family:var(--sans);font-size:.68rem;color:rgba(220,100,100,.9);
  letter-spacing:.02em;margin-top:8px;padding-top:6px;
  border-top:1px solid rgba(168,48,48,.25);
}

/* ═══ RULE CALLOUTS ═══ */
.rule-callout{
  background:linear-gradient(135deg,var(--navy,#080F1A),var(--navy2,#0D1E30));
  border:1px solid rgba(201,168,76,.2);
  border-left:3px solid rgba(201,168,76,.6);
  border-radius:0 4px 4px 0;
  padding:10px 14px;margin:.5em 0 1em;
  break-inside:avoid;
}
.rc-heading{
  font-family:var(--sans);font-size:.6rem;font-weight:700;
  letter-spacing:.1em;text-transform:uppercase;
  color:rgba(201,168,76,.9);margin-bottom:5px;
}
.rc-body{
  font-family:var(--serif);font-size:.84rem;color:rgba(245,240,232,.85);
  line-height:1.6;margin:0;text-indent:0!important;
}

/* ═══ SEVEN STAGES ARC ═══ */
.stage-card{
  display:grid;grid-template-columns:52px 1fr;gap:0;
  margin:.4em 0;break-inside:avoid;
  border-radius:0 6px 6px 0;
  overflow:hidden;
}
.stage-num{
  background:var(--stage-color,#C9A84C);
  color:var(--navy,#080F1A);
  font-family:var(--sans);font-size:.75rem;font-weight:900;
  letter-spacing:.05em;
  display:flex;align-items:center;justify-content:center;
  padding:14px 0;
}
.stage-content{
  padding:14px 18px;
  background:linear-gradient(135deg,var(--navy,#080F1A),var(--navy2,#0D1E30));
  border-top:1px solid rgba(255,255,255,.06);
  border-right:1px solid rgba(255,255,255,.06);
  border-bottom:1px solid rgba(255,255,255,.06);
}
.stage-name{
  font-family:var(--sans);font-size:.68rem;font-weight:800;
  letter-spacing:.15em;color:var(--stage-color,#C9A84C);
  text-transform:uppercase;margin-bottom:6px;
}
.stage-rule{
  width:24px;height:1px;background:var(--stage-color,#C9A84C);
  opacity:.5;margin-bottom:8px;
}
.stage-body{
  font-family:var(--serif);font-size:.86rem;color:rgba(245,240,232,.88);
  line-height:1.65;margin:0;text-indent:0!important;
}

/* ═══ PERFORMANCE CHECKLIST ═══ */
.checklist-section{
  margin:.4em 0 .8em;break-inside:avoid;
  border-radius:6px;overflow:hidden;
  background:linear-gradient(135deg,var(--navy,#080F1A),var(--navy2,#0D1E30));
  border:1px solid rgba(138,154,181,.2);
}
.cl-heading{
  font-family:var(--sans);font-size:.6rem;font-weight:700;
  letter-spacing:.12em;color:rgba(138,154,181,1);
  text-transform:uppercase;
  padding:8px 14px;
  background:rgba(138,154,181,.12);
  border-bottom:1px solid rgba(138,154,181,.2);
}
.cl-items{display:flex;flex-direction:column;}
.cl-item{
  display:grid;grid-template-columns:28px 1fr;align-items:baseline;
  gap:0;padding:8px 14px 8px 10px;
  border-bottom:1px solid rgba(255,255,255,.06);
  font-family:var(--serif);font-size:.84rem;
  color:rgba(245,240,232,.88);line-height:1.55;
}
.cl-item:last-child{border-bottom:none}
.cl-box{
  font-size:.75rem;color:rgba(201,168,76,.7);
  font-family:var(--sans);justify-self:center;padding-top:2px;
}
.cl-text{color:rgba(245,240,232,.88);}
.cl-note{display:block;font-size:.8em;color:rgba(180,190,210,.5);font-style:italic;margin-top:.18em;line-height:1.4;}

/* ═══ CHAPTER OPENER LEGEND ═══ */
.opener-legend{
  margin-top:40px;padding-top:22px;
  border-top:1px solid rgba(201,168,76,.18);
  display:flex;flex-direction:column;align-items:center;gap:16px;
}
.opener-legend .tier-row{display:flex;align-items:center;gap:10px;flex-wrap:wrap;justify-content:center}
.opener-legend .icon-row{display:flex;align-items:center;gap:20px;flex-wrap:wrap;justify-content:center}
.opener-legend .legend-label{
  font-family:var(--sans);font-size:.52rem;letter-spacing:3px;
  color:var(--gray-blue);text-transform:uppercase;margin-top:2px;
}
.opener-legend .badge{font-size:.58rem;padding:2px 9px}
.icon-item{display:flex;align-items:center;gap:7px}
.icon-item svg{opacity:.75;width:20px;height:20px}
.icon-item .icon-code{
  font-family:var(--sans);font-size:.58rem;font-weight:700;
  letter-spacing:2px;
}
.icon-item .icon-code.bp{color:var(--gold)}
.icon-item .icon-code.cr{color:var(--blue)}
.icon-item .icon-code.vs{color:var(--purple)}
.icon-item .icon-code.am{color:var(--red)}

/* ═══ INLINE MARGIN ICONS ═══ */
.margin-icon{
  float:right;clear:right;
  margin:0 -18px 4px 12px;
  opacity:.55;width:18px;height:18px;
}
@media print{
  .margin-icon{margin-right:-22px}
}

/* ═══ RESPONSIVE ═══ */
@media(max-width:768px){
  .chapter-body,.front-matter{padding:28px 18px}
  .chapter-number{font-size:3.2rem}
  .chapter-title{font-size:.9rem;letter-spacing:3px}
  .cover .title{font-size:1.9rem}
  .pi-number{font-size:3.5rem}
}
'''


# ═══════════════════════════════════════════════════════════
# MAIN BUILDER
# ═══════════════════════════════════════════════════════════

def build_book(manuscript_path, output_path):
    print("Parsing manuscript...")
    sections = parse_manuscript(manuscript_path)
    print(f"Found {len(sections)} sections")

    html = [f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Architecture of Wonder \u2014 Decode Behavior</title>
<style>{CSS}</style>
</head>
<body>
''']

    # ── FRONT COVER ──
    html.append('''<section class="cover">
  <div class="author">C H R I S \u2003 M I C H A E L</div>
  <div class="rule"></div>
  <div class="title">THE<br>ARCHITECTURE<br>OF WONDER</div>
  <div class="rule"></div>
  <div class="subtitle">A BEHAVIORAL GUIDE TO ATTENTION,<br>SUGGESTION, AND ASTONISHMENT</div>
  <div class="rule"></div>
  <div class="icons"><span>BP</span><span>CR</span><span>VS</span><span>AM</span></div>
  <div class="tagline">D E C O D E \u2003 B E H A V I O R</div>
</section>''')

    # ── DEFINITIONS ──
    html.append('''<section class="definitions">
  <p class="def-word">wonder</p>
  <p class="def-phonetic">/\u02c8w\u028cnd\u0259r/</p>
  <p class="def-pos">noun</p>
  <p class="def-meaning">A feeling of surprise mingled with admiration, caused by something beautiful, unexpected, unfamiliar, or inexplicable. The state of being open to what cannot yet be explained.</p>
  <div class="section-break">\u00b7 \u00b7 \u00b7</div>
  <p class="def-word">architecture</p>
  <p class="def-phonetic">/\u02c8\u0251\u02d0rk\u026atekt\u0283\u0259r/</p>
  <p class="def-pos">noun</p>
  <p class="def-meaning">The complex or carefully designed structure of something. The deliberate arrangement of elements to produce a specific experience in the person who moves through it.</p>
</section>''')

    # ── TOC ──
    html.append(gen_toc(sections))

    # ── SIGNAL KEY ──
    html.append(f'''<section class="signal-key">
  <h2>How to Read This Book</h2>
  <p class="sk-intro">Every chapter opener in this book carries two rows of symbols. They are not decoration. They tell you what kind of evidence each chapter uses and what domain it applies to. Here is how to read them.</p>

  <div class="sk-section">
    <h3>Signal Confidence Tiers</h3>
    <p class="sk-desc">Every behavioral signal in this book is rated by evidential strength. The tier tells you how much weight to put behind a read.</p>
    <table class="tier-table">
      <tr>
        <td class="tt-badge-cell"><span class="badge t1">T1</span></td>
        <td><div class="tt-name">Physical Evidence</div><div class="tt-desc">Directly observable, documentable, and not subject to interpretation. The most reliable tier.</div><div class="tt-ex">Shoe resoling, cuff wear, belt notch wear, callus distribution</div></td>
      </tr>
      <tr>
        <td class="tt-badge-cell"><span class="badge t2">T2</span></td>
        <td><div class="tt-name">Research-Backed</div><div class="tt-desc">Supported by peer-reviewed behavioral science. High reliability when baseline is established.</div><div class="tt-ex">Eye contact shift, blink rate change, foot direction, postural lean</div></td>
      </tr>
      <tr>
        <td class="tt-badge-cell"><span class="badge t3">T3</span></td>
        <td><div class="tt-name">Field-Tested Pattern</div><div class="tt-desc">Consistent operational evidence from applied practice. Reliable in the room without formal laboratory support.</div><div class="tt-ex">Tonality drop at certainty, eye block before disclosure, breath-hold at decision</div></td>
      </tr>
      <tr>
        <td class="tt-badge-cell"><span class="badge t4">T4</span></td>
        <td><div class="tt-name">Field-Used, Evidence-Disputed</div><div class="tt-desc">Limited or contested formal research support. Widely used by experienced practitioners. Hold as context, not anchor.</div><div class="tt-ex">NLP eye-movement direction, lower eyelid tension, hair part direction</div></td>
      </tr>
    </table>
  </div>

  <div class="sk-section">
    <h3>Observation Categories</h3>
    <p class="sk-desc">Each signal is tagged by its primary application domain. These codes appear as margin icons throughout the signal tables.</p>
    <div class="sk-grid">
      <div class="sk-item"><span class="sk-icon">{_svg_bp()}<span class="icon-code bp">BP</span></span><div class="sk-label">Behavioral Profiling</div><div class="sk-explain">Signals used to build a behavioral read on a person. Physical evidence, posture, grooming, belongings, and habitual patterns.</div></div>
      <div class="sk-item"><span class="sk-icon">{_svg_cr()}<span class="icon-code cr">CR</span></span><div class="sk-label">Cold Reading</div><div class="sk-explain">Signals that support verbal reads and statements. The cues that let you tell someone what they are thinking before they say it.</div></div>
      <div class="sk-item"><span class="sk-icon">{_svg_vs()}<span class="icon-code vs">VS</span></span><div class="sk-label">Volunteer Selection</div><div class="sk-explain">Signals that help you identify the right participant from a crowd. Who will play along, who will resist, who will make the moment land.</div></div>
      <div class="sk-item"><span class="sk-icon">{_svg_am()}<span class="icon-code am">AM</span></span><div class="sk-label">Audience Management</div><div class="sk-explain">Signals that tell you how the room is responding. Energy, attention, resistance, compliance. Read these to steer the group.</div></div>
    </div>
  </div>
</section>''')

    # ── CONTENT ──
    global_para = 0

    for section in sections:
        stype = section['type']
        part_num = section.get('part_num', 0)

        if stype == 'meta_reveal':
            continue  # rendered via META_REVEAL_HTML below

        if stype == 'front_matter':
            html.append(f'<section class="front-matter"><h2>{escape(section["title"].upper())}</h2>')
            content = section['content']
            # Find where the title page block starts (DECODE BEHAVIOR line)
            tp_start = None
            for ci, para in enumerate(content):
                if para.strip() == 'DECODE BEHAVIOR':
                    tp_start = ci
                    break
            ack_paras = content[:tp_start] if tp_start is not None else content
            # Acknowledgment names to highlight
            _ACK_NAMES = [
                'Zach Alexander', 'Mike Gardner', 'Joe Navarro', 'Greg Hartley',
                'Scott Rouse', 'Chris Edin', 'Kasia Wezowski', 'Tim Miller',
                'Nadia Ait', 'Lena Sisco', 'Kevin Hamdan', 'Philo',
                'Jack Thomson', 'Tyler Reed', 'Anthem Flint', 'Michael Carroway',
                'TJ Tana', 'Ian Rowland', 'Chase Hughes', 'Peter Turner',
                'Fraser Parker', 'Jerome Finley', 'Ray', 'Pratik',
            ]
            for para in ack_paras:
                if para.strip():
                    t = escape(para.strip())
                    for name in _ACK_NAMES:
                        t = t.replace(escape(name), f'<span class="ack-name">{escape(name)}</span>')
                    html.append(f'<p>{t}</p>')
            html.append('</section>')
            # Render the title page block as a styled section
            if tp_start is not None:
                html.append('''<section class="title-page">
  <div class="tp-brand">DECODE BEHAVIOR</div>
  <div class="tp-title">THE ARCHITECTURE<br>OF WONDER</div>
  <div class="tp-subtitle">A Behavioral Guide to Attention, Suggestion,<br>and Astonishment for Mentalists</div>
  <div class="tp-edition">EXPANDED EDITION</div>
  <div class="tp-rule"></div>
  <div class="tp-author">CHRIS MICHAEL</div>
  <div class="tp-roles">Behavioral Strategist &middot; Mentalist &middot; Keynote Speaker</div>
  <div class="tp-roles">Founder, Decode Behavior &middot; Global Institute of Behavior</div>
  <div class="tp-dots">&middot; &middot; &middot;</div>
  <div class="tp-quote">&ldquo;The brain is a prediction machine. Every performance is a negotiation between what the mind expects and what you choose to deliver.&rdquo;</div>
  <div class="tp-attribution">&mdash; CHRIS MICHAEL</div>
</section>''')

        elif stype == 'part':
            html.append(gen_part_opener(section))
            # Part body content (Field Notes, NPM) — skip first para (used as part desc in opener)
            # Route through build_chapter_body so all special formatters (stage cards, checklist, etc.) apply
            content_paras = [p for p in section['content'] if p.strip()][1:]
            if content_paras:
                part_section_proxy = dict(section)
                part_section_proxy['content'] = content_paras
                html.append(f'<article class="chapter-body" data-part="{part_num}">')
                html.append(f'<header class="running-header"><span>THE ARCHITECTURE OF WONDER</span><span>{escape(section.get("subtitle","").upper())}</span></header>')
                body_html, global_para = build_chapter_body(part_section_proxy, global_para)
                html.append(body_html)
                html.append('<div class="page-footer">THE ARCHITECTURE OF WONDER\u2003|\u2003VANISHING INC</div>')
                html.append('</article>')

        elif stype == 'how_to_read':
            html.append('<article class="chapter-body how-to-read" data-part="0" style="break-before:page">')
            body, global_para = build_chapter_body(section, global_para)
            html.append(body)
            html.append('<div class="page-footer">THE ARCHITECTURE OF WONDER\u2003|\u2003VANISHING INC</div>')
            html.append('</article>')

        elif stype == 'chapter':
            html.append(gen_chapter_opener(section))
            html.append(f'<article class="chapter-body" data-part="{part_num}">')
            body, global_para = build_chapter_body(section, global_para)
            html.append(body)
            html.append('<div class="page-footer">THE ARCHITECTURE OF WONDER\u2003|\u2003VANISHING INC</div>')
            html.append('</article>')

        elif stype == 'glossary':
            html.append(gen_chapter_opener({
                'type':'chapter','chapter_num':0,'part_num':9,
                'title':'Glossary','chapter_key':'GLOSSARY'
            }))
            html.append('<article class="chapter-body">')
            html.append('<header class="running-header"><span>THE ARCHITECTURE OF WONDER</span><span>GLOSSARY</span></header>')
            paras = [p.strip() for p in section['content']]
            gi = 0
            while gi < len(paras):
                p = paras[gi]
                if not p:
                    gi += 1
                    continue
                # ── APPENDIX SECTION HEADER ──
                if re.match(r'^APPENDIX\s+A\d+', p):
                    html.append(f'<div class="section-break">\u00b7 \u00b7 \u00b7</div>')
                    html.append(f'<h3 class="section-header sh-standard" style="margin-top:2em">{escape(p)}</h3>')
                    if gi + 1 < len(paras) and paras[gi+1]:
                        html.append(f'<p class="first-para">{escape(paras[gi+1])}</p>')
                        gi += 2
                    else:
                        gi += 1
                    continue
                # ── T4 SIGNAL CARDS (SIGNAL N — name OR SIGNAL N. name) ──
                sig_m = re.match(r'^(SIGNAL\s+\d+)\s*[\u2014\u2013\-\.]+\s*(.+)$', p)
                if sig_m:
                    sig_name = sig_m.group(2).strip()
                    claim = research = valid = ''
                    gi += 1
                    while gi < len(paras):
                        np = paras[gi]
                        if re.match(r'^THE CLAIM', np, re.I):
                            claim = np.partition(':')[2].strip()
                            gi += 1
                            while gi < len(paras) and not re.match(r'^THE RESEARCH|^WHAT REMAINS|^SIGNAL\s+\d', paras[gi], re.I):
                                if paras[gi]: claim += ' ' + paras[gi]
                                gi += 1
                        elif re.match(r'^THE RESEARCH', np, re.I):
                            research = np.partition(':')[2].strip()
                            gi += 1
                            while gi < len(paras) and not re.match(r'^WHAT REMAINS|^SIGNAL\s+\d', paras[gi], re.I):
                                if paras[gi]: research += ' ' + paras[gi]
                                gi += 1
                        elif re.match(r'^WHAT REMAINS VALID', np, re.I):
                            valid = np.partition(':')[2].strip()
                            gi += 1
                            while gi < len(paras) and not re.match(r'^SIGNAL\s+\d', paras[gi], re.I):
                                if paras[gi]: valid += ' ' + paras[gi]
                                gi += 1
                            break
                        else:
                            break
                    html.append(gen_t4_signal_card(sig_name, claim.strip(), research.strip(), valid.strip()))
                    continue
                # ── STANDARD GLOSSARY ENTRY: "N.  Term  Definition" ──
                gm = re.match(r'^(\d+)\.?\s{2,}(.+?)\s{2,}(.+)$', p)
                if gm:
                    html.append(gen_glossary_entry(gm.group(1), gm.group(2).strip(), gm.group(3).strip()))
                    gi += 1
                    continue
                # ── SECTION BREAK ──
                if is_section_break(p):
                    html.append('<div class="section-break">\u00b7 \u00b7 \u00b7</div>')
                    gi += 1
                    continue
                # ── FALLBACK ──
                html.append(f'<p>{escape(p)}</p>')
                gi += 1
            html.append('</article>')

        elif stype == 'about':
            html.append('<article class="chapter-body" style="break-before:page">')
            html.append('<header class="running-header"><span>THE ARCHITECTURE OF WONDER</span><span>ABOUT THE AUTHOR</span></header>')
            html.append('<h3 class="section-header" style="display:block;text-align:center;border:none;padding-bottom:0;margin-bottom:2em">ABOUT THE AUTHOR</h3>')
            for para in section['content']:
                if para.strip():
                    html.append(f'<p>{escape(para.strip())}</p>')
            html.append('</article>')

    # ── META REVEAL ──
    html.append(META_REVEAL_HTML)

    # ── BACK COVER ──
    html.append('''<section class="back-cover">
  <div class="rule" style="width:180px;height:1px;background:linear-gradient(90deg,transparent,rgba(201,168,76,.35),transparent);margin:22px 0"></div>
  <div class="title" style="font-family:var(--sans);font-size:1.6rem;font-weight:700;letter-spacing:5px;color:var(--gold);text-align:center;margin:18px 0">THE ARCHITECTURE<br>OF WONDER</div>
  <div class="rule" style="width:180px;height:1px;background:linear-gradient(90deg,transparent,rgba(201,168,76,.35),transparent);margin:22px 0"></div>
  <p class="back-blurb">Every design decision in this book demonstrates the psychology it teaches. The colors, the typography, the layout, the pattern interrupts\u2009\u2014\u2009all of it was engineered using the same behavioral architecture you just learned to build.</p>
  <div class="rule" style="width:120px;height:1px;background:linear-gradient(90deg,transparent,rgba(201,168,76,.25),transparent);margin:18px 0"></div>
  <p class="hidden-text">You\u2019re already reading people. You just proved it.</p>
  <div class="tagline" style="font-family:var(--sans);font-size:.5rem;letter-spacing:6px;color:var(--dim);margin-top:50px">D E C O D E \u2003 B E H A V I O R</div>
</section>''')

    html.append('</body></html>')

    full = '\n'.join(html)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full)

    print(f"Book written to {output_path}")
    print(f"Size: {len(full):,} chars ({len(full)//1024} KB)")


if __name__ == '__main__':
    import os as _os
    _base = _os.path.dirname(_os.path.abspath(__file__))
    build_book(
        _os.path.join(_base, 'manuscript-extracted.txt'),
        _os.path.join(_base, 'Architecture-of-Wonder-DESIGNED.html')
    )
