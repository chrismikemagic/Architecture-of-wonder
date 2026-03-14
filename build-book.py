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
    'CHAPTER 9': '"Four styles. One conversation. The read starts before anyone speaks."',
    'CHAPTER 10': '"You already know more than you think. The trick is knowing what to trust."',
    'CHAPTER 11': '"The face lies. But it lies too slowly."',
    'CHAPTER 12': '"The volunteer chose you before you chose them."',
    'CHAPTER 13': '"Compliance is not obedience. It is agreement they did not know they gave."',
    'CHAPTER 14': '"The moment after the effect is where the real work happens."',
    'CHAPTER 15': '"Hypnosis is not what you think it is. That is why it works."',
    'CHAPTER 16': '"The boardroom is the most dangerous stage you will ever work."',
    'CHAPTER 17': '"You cannot teach observation. You can only remove the obstacles to seeing."',
    'CHAPTER 18': '"Every performance teaches you something. Most of the lessons hurt."',
    'CHAPTER 19': '"The most powerful person in the room is rarely the one with the title."',
    'CHAPTER 20': '"The question is never whether to influence. It is whether to admit it."',
    'CHAPTER 21': '"The walk to the stage is the performance."',
    'CHAPTER 22': '"Standing ovations are not earned. They are engineered."',
    'CHAPTER 23': '"Sound is the invisible stage."',
    'CHAPTER 24': '"The environment gives the instruction before you do."',
    'CHAPTER 25': '"Authority is not claimed. It is perceived."',
    'CHAPTER 26': '"Your career is a performance with a very long run."',
    'CHAPTER 27': '"They have already decided before you walk on stage."',
    'CHAPTER 28': '"The signal is data. The statement is performance. The gap between them is skill."',
    'CHAPTER 29': '"The best insight demonstration looks like telepathy and works like science."',
    'CHAPTER 30': '"Method invisibility is not misdirection. It is architecture."',
    'CHAPTER 31': '"A performer with perfect reads and poor timing is less effective than the reverse."',
    'CHAPTER 32': '"The booking was won or lost before you picked up the phone."',
    'CHAPTER 33': '"Your introduction is the first frame the audience receives. Control it."',
    'CHAPTER 34': '"What you say matters less than how it sounds when you say it."',
    'CHAPTER 35': '"The client is reading you harder than you are reading them."',
    'CHAPTER 36': '"Every framework in this book leads here."',
    'CHAPTER 37': '"FATE is not a model. It is a diagnostic for every performance you will ever give."',
    'CHAPTER 38': '"Authority is not one thing. It is five things, and most people have two."',
    'CHAPTER 39': '"The periodic table of behavioral elements. Every signal has a weight."',
    'CHAPTER 40': '"Influence is not a trick. It is an equation with variables you can measure."',
    'CHAPTER 41': '"Every framework in this book was designed to work on stage. This one ties them together."',
    'GLOSSARY': '"The language shapes the thinking. Know the words."',
}

KEY_READS = {
    'CHAPTER 1': 'Design the memory, and you design the experience.',
    'CHAPTER 2': 'Salience is not what you show. It is what they cannot ignore.',
    'CHAPTER 3': 'Tension is not the enemy. Boredom is.',
    'CHAPTER 4': 'Delay is not cruelty. It is craft.',
    'CHAPTER 5': 'Direct their eyes, and you direct their minds.',
    'CHAPTER 6': 'Credibility is not what you say. It is what they decide before you say it.',
    'CHAPTER 7': 'The read is never one signal. The read is the chain.',
    'CHAPTER 8': 'Eighty signals. Five filters. One practice.',
    'CHAPTER 9': 'Style is not personality. But it is the first thing the room broadcasts.',
    'CHAPTER 10': 'The best cold read is a warm observation delivered cold.',
    'CHAPTER 11': 'Seven expressions. One-fifth of a second. That is the window.',
    'CHAPTER 12': 'Handle the person, not the trick.',
    'CHAPTER 13': 'The best instruction is the one that feels like their idea.',
    'CHAPTER 14': 'Close the moment before they close it for you.',
    'CHAPTER 15': 'The trance state is not extraordinary. It is the brain doing what it does best.',
    'CHAPTER 16': 'In the boardroom, the audience writes the review before the show ends.',
    'CHAPTER 17': 'Training is not instruction. It is guided noticing.',
    'CHAPTER 18': 'The face is the performance. The hands are the truth.',
    'CHAPTER 19': 'Authority is borrowed. Influence is earned in the moment.',
    'CHAPTER 20': 'Ethics is not a constraint. It is the architecture that makes the rest stand.',
    'CHAPTER 21': 'The walk is the show. Everything after is confirmation.',
    'CHAPTER 22': 'The ovation begins in the first thirty seconds.',
    'CHAPTER 23': 'Control the sound, and you control the space.',
    'CHAPTER 24': 'Design the compliance. Then act surprised when they comply.',
    'CHAPTER 25': 'The frame precedes the content. Always.',
    'CHAPTER 26': 'Advance the system, not the ego.',
    'CHAPTER 27': 'You are not what you do. You are what they remember you doing.',
    'CHAPTER 28': 'The signal is the data. The statement is the art. Never confuse the two.',
    'CHAPTER 29': 'The best insight feels impossible because it is grounded in what is actually there.',
    'CHAPTER 30': 'If they are looking for the method, the architecture failed.',
    'CHAPTER 31': 'Silence is not absence. It is the loudest tool you have.',
    'CHAPTER 32': 'The booking is won in the room they never see you in.',
    'CHAPTER 33': 'The introduction is the first frame. Own it.',
    'CHAPTER 34': 'Language is not communication. It is positioning.',
    'CHAPTER 35': 'Read them first. Then let them think they read you.',
    'CHAPTER 36': 'Decode is not a technique. It is a way of seeing.',
    'CHAPTER 37': 'FATE is not a formula. It is a mirror.',
    'CHAPTER 38': 'Build all five pillars. Then let them carry the weight.',
    'CHAPTER 39': 'Every element has a weight. The table tells you which ones matter.',
    'CHAPTER 40': 'Influence without understanding is manipulation. With understanding, it is leadership.',
    'CHAPTER 41': 'Go see what others miss.',
}

WHAT_YOU_JUST_DID = {
    3: "You have been reading for approximately three minutes. Notice your breathing. It slowed when you hit the section on cortisol. That is your nervous system responding to content about threat\u2009\u2014\u2009even though the threat is not real. Observation, applied to yourself.",
    7: "You have been reading this page for about ninety seconds. Notice which hand is holding the book. That is Observation #01\u2009\u2014\u2009handedness indicator. You just demonstrated it without thinking.",
    10: "If you skipped ahead to this chapter because the title interested you more than the previous one, that is salience at work. Your brain prioritized novelty over sequence. Chapter Two explained why.",
    15: "Notice your posture right now. Did you lean forward slightly in the last few paragraphs? That is engagement. Your body responded before your mind decided the content was interesting.",
    21: "You just turned to this chapter. Before reading a word, you formed an impression of its length by glancing at the page count. That is thin-slicing applied to a book. You do this with people too.",
    28: "Your eyes moved to this callout before reading the surrounding text. That is the Von Restorff effect\u2009\u2014\u2009your brain prioritized the visually distinct element. Chapter Two taught you this. The book just demonstrated it.",
    36: "You are in the final section. Notice how your reading pace has changed. If it has accelerated, that is the recency effect\u2009\u2014\u2009your brain knows it is close to the end and is already preparing to consolidate.",
}

PATTERN_INTERRUPTS = [
    {'number': '250', 'unit': 'MILLISECONDS', 'text': 'The time it takes your brain to form a first impression of a stranger.', 'source': 'Willis & Todorov, 2006', 'wyajd': 'You formed yours of this page in less time than that. What did you notice first\u2009\u2014\u2009the number, or the word? That is salience at work.'},
    {'number': '40%', 'unit': 'INCREASE IN TRUST', 'text': 'The boost in perceived credibility when text is set in a highly readable font.', 'source': 'Processing Fluency Research', 'wyajd': 'The font you are reading right now was chosen for this reason.'},
    {'number': '7', 'unit': 'EXPRESSIONS', 'text': 'The number of universal micro-expressions the human face produces. Each lasts less than one-fifth of a second.', 'source': 'Ekman & Friesen, 1971', 'wyajd': ''},
    {'number': '60,000\u00d7', 'unit': 'FASTER', 'text': 'The speed at which the brain processes color compared to text.', 'source': 'Visual Cognition Research', 'wyajd': 'The gold accent on this page reached your brain before the words did.'},
    {'number': '3', 'unit': 'SIGNALS', 'text': 'The minimum number of co-occurring behavioral signals required to form a reliable pattern.', 'source': 'The Five Cs\u2009\u2014\u2009Clusters', 'wyajd': 'One signal is noise. Two is coincidence. Three is a read.'},
    {'number': '\u2159', 'unit': 'OF A SECOND', 'text': 'The duration of a micro-expression. Blink and you miss it. But your limbic system does not.', 'source': 'Ekman, 2003', 'wyajd': ''},
    {'number': '85%', 'unit': 'OF DECISIONS', 'text': 'The percentage of consumer choices where color is cited as the primary factor.', 'source': 'Color Psychology Research', 'wyajd': ''},
    {'number': '5', 'unit': 'FILTERS', 'text': 'Context. Clusters. Congruence. Consistency. Culture. The Five Cs that separate noise from signal.', 'source': 'The Architecture of Wonder', 'wyajd': ''},
]

# ═══════════════════════════════════════════════════════════
# FIGURES — Images injected after specific section headers
# ═══════════════════════════════════════════════════════════

FIGURES = {
    # Key: "CHAPTER <num>:<section header text>" → figure data
    # Note: chapter_key comes from parse_manuscript() numbering, not the TOC
    'CHAPTER 10:The Seven Expressions': {
        'src': 'resources/metv-images/seven-universal-expressions.png',
        'alt': 'The seven universal facial expressions: Anger, Disgust, Fear, Happiness, Sadness, Surprise, and Contempt',
        'caption': 'Figure 10.1 \u2014 The seven universal expressions: Anger, Disgust, Fear, Happiness, Sadness, Surprise, and Contempt.',
        'rights': 'Author-owned photograph',
    },
}

# ═══════════════════════════════════════════════════════════
# THE FIVE Cs FRAMEWORK — Injected at beginning of Chapter 7
# ═══════════════════════════════════════════════════════════

FIVE_CS_HTML = '''
<div class="five-cs-framework">
  <div class="five-cs-header">
    <div class="five-cs-title">THE FIVE C\u2019s OF BEHAVIORAL READING</div>
    <div class="five-cs-subtitle">The architecture without which individual signals are noise</div>
  </div>

  <div class="five-cs-grid">
    <div class="five-cs-card" data-c="context">
      <div class="c-tab">CONTEXT</div>
      <div class="c-body">
        <div class="c-question">What environment?</div>
        <p class="c-desc">Same gesture means different things in different settings. Arms crossed at a cold outdoor show is thermoregulation. Arms crossed during a one-on-one reading is a barrier.</p>
        <p class="c-rule">Context determines meaning. Always.</p>
      </div>
    </div>

    <div class="five-cs-card" data-c="clusters">
      <div class="c-tab">CLUSTERS</div>
      <div class="c-body">
        <div class="c-question">Multiple signals?</div>
        <p class="c-desc">One signal is noise. Three co-occurring behaviors multiply each other\u2019s diagnostic weight. A cluster is a pattern.</p>
        <p class="c-rule">Never act on a single signal.</p>
      </div>
    </div>

    <div class="five-cs-card" data-c="congruence">
      <div class="c-tab">CONGRUENCE</div>
      <div class="c-body">
        <div class="c-question">Body = words?</div>
        <p class="c-desc">When the body says one thing and the words say another, the body is telling the truth. Not by confronting it\u2009\u2014\u2009by creating a frame where the truth can emerge voluntarily.</p>
        <p class="c-rule">Incongruence is your most reliable signal.</p>
      </div>
    </div>

    <div class="five-cs-card" data-c="consistency">
      <div class="c-tab">CONSISTENCY</div>
      <div class="c-body">
        <div class="c-question">Their baseline?</div>
        <p class="c-desc">Compare what you are seeing to that individual\u2019s personal baseline. Not a generic chart. Deviation from their baseline is the data point.</p>
        <p class="c-rule">Without baseline, every read is a projection.</p>
      </div>
    </div>

    <div class="five-cs-card" data-c="culture">
      <div class="c-tab">CULTURE</div>
      <div class="c-body">
        <div class="c-question">Background norms?</div>
        <p class="c-desc">Eye contact, personal space, and emotional expressiveness vary significantly across cultures. What registers as confidence in one culture registers as challenge in another.</p>
        <p class="c-rule">Calibrate before concluding.</p>
      </div>
    </div>
  </div>

  <div class="five-cs-chain">
    <div class="chain-label">APPLY AS A CHAIN \u2014 NOT A CHECKLIST</div>
    <div class="chain-flow">
      <span class="chain-pill" data-c="context">Context</span>
      <span class="chain-arrow">\u203a</span>
      <span class="chain-pill" data-c="clusters">Clusters</span>
      <span class="chain-arrow">\u203a</span>
      <span class="chain-pill" data-c="congruence">Congruence</span>
      <span class="chain-arrow">\u203a</span>
      <span class="chain-pill" data-c="consistency">Consistency</span>
      <span class="chain-arrow">\u203a</span>
      <span class="chain-pill" data-c="culture">Culture</span>
      <span class="chain-arrow">\u203a</span>
      <span class="chain-pill chain-read">READ</span>
    </div>
    <p class="chain-note">Most weak readings fail because they skip this chain. They treat behavior like a vending machine.</p>
    <p class="chain-note-gold">Real behavior breathes. It moves. It has to be read in motion, against a baseline, inside a context.</p>
  </div>
</div>

<div class="section-break">\u00b7 \u00b7 \u00b7</div>
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
    # Count capitalized words (excluding small conjunctions)
    small_words = {'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'vs.', 'vs', 'is', 'not'}
    cap_count = sum(1 for w in words if w[0].isupper() or w.lower() in small_words)
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
    return '<svg class="margin-icon" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg"><ellipse cx="9" cy="9" rx="8" ry="5.5" stroke="#C9A84C" stroke-width="1.2"/><circle cx="9" cy="9" r="2.2" fill="#C9A84C"/></svg>'
def _svg_cr():
    return '<svg class="margin-icon" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="9" cy="6" r="3" stroke="#1A8FA8" stroke-width="1.2"/><path d="M3 16c0-3.3 2.7-6 6-6s6 2.7 6 6" stroke="#1A8FA8" stroke-width="1.2" stroke-linecap="round"/></svg>'
def _svg_vs():
    return '<svg class="margin-icon" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg"><polyline points="2,9 5,5 8,13 11,5 14,9 16,9" stroke="#6B52A0" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def _svg_am():
    return '<svg class="margin-icon" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg"><line x1="3" y1="9" x2="14" y2="9" stroke="#A83030" stroke-width="1.3" stroke-linecap="round"/><polyline points="10,5 15,9 10,13" stroke="#A83030" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def _opener_legend():
    return (
        '<div class="opener-legend">'
        '<div class="tier-row">'
        '<span class="badge t1">T1</span>'
        '<span class="badge t2">T2</span>'
        '<span class="badge t3">T3</span>'
        '<span class="badge t4">T4</span>'
        '</div><div class="legend-label">SIGNAL CONFIDENCE TIERS</div>'
        '<div class="icon-row">'
        f'<span class="icon-item">{_svg_bp()}<span class="icon-code bp">BP</span></span>'
        f'<span class="icon-item">{_svg_cr()}<span class="icon-code cr">CR</span></span>'
        f'<span class="icon-item">{_svg_vs()}<span class="icon-code vs">VS</span></span>'
        f'<span class="icon-item">{_svg_am()}<span class="icon-code am">AM</span></span>'
        '</div><div class="legend-label">OBSERVATION CATEGORIES</div>'
        '</div>'
    )

def gen_chapter_opener(section):
    ch_num = section.get('chapter_num', 0)
    part_num = section.get('part_num', 0)
    title = section.get('title', '')
    chapter_key = section.get('chapter_key', '')
    hook = HOOK_LINES.get(chapter_key, '')

    part_names = {0:'',1:'PART ONE',2:'PART TWO',3:'PART THREE',4:'PART FOUR',
                  5:'PART FIVE',6:'PART SIX',7:'PART SEVEN',8:'PART EIGHT'}
    part_label = part_names.get(part_num, '')

    if ch_num > 0:
        ch_display = f'{ch_num:02d}'
    else:
        ch_display = '\u2726'  # diamond for intro

    legend = _opener_legend()
    return f'''<section class="chapter-opener" data-part="{part_num}">
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
    part_names = {1:'ONE',2:'TWO',3:'THREE',4:'FOUR',5:'FIVE',6:'SIX',7:'SEVEN',8:'EIGHT'}
    return f'''<section class="part-opener" data-part="{part_num}">
  <div class="part-opener-content">
    <div class="part-number">PART {part_names.get(part_num, "")}</div>
    <div class="gold-line wide"></div>
    <h1 class="part-title">{escape(subtitle)}</h1>
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


def gen_wyajd(text):
    return f'''<aside class="wyajd">
  <div class="wyajd-bar"></div>
  <p class="wyajd-text">{text}</p>
</aside>'''


def gen_pull_quote(text):
    return f'''<blockquote class="pull-quote">
  <p>{escape(text)}</p>
</blockquote>'''


def gen_what_you_have_felt():
    return '''<div class="felt-before">
  <div class="felt-icon">\u25C9</div>
  <p class="felt-label">WHAT YOU HAVE FELT BEFORE</p>
</div>'''


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

    # Section headers
    if is_section_header(stripped):
        return f'<h3 class="section-header">{escape(stripped)}</h3>'

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
    return f'<p>{icon_html}{t}</p>' 


def is_tier_definition(text):
    """Detect T1-T4 tier definition lines like 'T1 — Physical Evidence'."""
    stripped = text.strip()
    m = re.match(r'^T([1-4])\s*[\u2014\u2013\-]+\s*(.+)$', stripped)
    return m

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

    # ── FIVE Cs FRAMEWORK — inject at beginning of Chapter 7 ──
    if chapter_num == 7:
        parts.append(FIVE_CS_HTML)

    # Track for element insertion
    total = len(paragraphs)
    spotlight_done = False
    wyajd_done = False
    pull_quote_done = False
    pi_count = 0
    pi_idx = global_para_count % len(PATTERN_INTERRUPTS)

    i = 1
    while i < len(paragraphs):
        para = paragraphs[i]
        global_para_count += 1
        stripped = para.strip()

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

        # Pattern interrupt every ~45 paragraphs
        if i > 0 and i % 45 == 0 and pi_count < 2:
            parts.append(gen_pattern_interrupt(PATTERN_INTERRUPTS[pi_idx % len(PATTERN_INTERRUPTS)]))
            pi_idx += 1
            pi_count += 1

        # "What You Just Did" at ~65% through chapter
        if not wyajd_done and chapter_num in WHAT_YOU_JUST_DID and i > total * 0.6:
            parts.append(gen_wyajd(WHAT_YOU_JUST_DID[chapter_num]))
            wyajd_done = True

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

        processed = process_paragraph(para, part_num)
        if processed:
            parts.append(processed)

        # ── FIGURE INJECTION — after section headers ──
        if is_section_header(stripped):
            fig_key = f'{chapter_key}:{stripped}'
            if fig_key in FIGURES:
                fig = FIGURES[fig_key]
                parts.append(f'<div class="book-figure" style="text-align:center;margin:2em 0;">')
                parts.append(f'  <img src="{fig["src"]}" alt="{fig["alt"]}" style="max-width:100%;height:auto;" />')
                if fig.get('caption'):
                    parts.append(f'  <p class="figure-caption" style="font-size:0.85em;color:#666;margin-top:0.5em;font-style:italic;">{fig["caption"]}</p>')
                parts.append(f'</div>')

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

  <div class="section-break">\u00b7 \u00b7 \u00b7</div>

  <h3 class="section-header meta-header">The Pattern Interrupts</h3>

  <p>Every eight to twelve pages, the layout changed. A full-bleed dark page with a single gold statistic. Those were <em class="gold">the Von Restorff effect</em>\u2009\u2014\u2009the isolation effect. You remember them because they were different.</p>

  <div class="section-break">\u00b7 \u00b7 \u00b7</div>

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
  </div>

  <div class="section-break">\u00b7 \u00b7 \u00b7</div>

  <div class="meta-finale">
    <p class="finale-1">This book was not just written.</p>
    <p class="finale-2">It was designed to read you while you read it.</p>
    <p class="finale-3">And now you know how.</p>
  </div>

  <div class="page-footer">THE ARCHITECTURE OF WONDER\u2003|\u2003DECODE BEHAVIOR</div>
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
            parts.append(f'<div class="toc-ch"><span class="toc-num">{num}</span><span class="toc-title">{escape(s["title"])}</span><span class="toc-dots"></span></div>')
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
  color:var(--gray-blue);line-height:1.65;margin-top:18px;max-width:380px;margin-left:auto;margin-right:auto;
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

/* ═══ SECTION HEADER ═══ */
.section-header{
  font-family:var(--sans);font-size:.78rem;font-weight:700;
  letter-spacing:1.5px;color:var(--body-color);
  margin:2.2em 0 .85em;padding-bottom:5px;
  border-bottom:2px solid var(--gold);display:inline-block;
}
.meta-header{color:var(--gold)}

/* ═══ SECTION BREAK ═══ */
.section-break{text-align:center;color:var(--gold);font-size:1rem;letter-spacing:10px;margin:2.2em 0}

/* ═══ "WHAT YOU HAVE FELT BEFORE" ═══ */
.felt-before{
  text-align:center;margin:2.8em 0 1.5em;padding:18px 0;
  border-top:1px solid var(--gold-dim);border-bottom:1px solid var(--gold-dim);
}
.felt-icon{color:var(--gold);font-size:1.1rem;margin-bottom:6px}
.felt-label{
  font-family:var(--sans);font-size:.62rem;font-weight:600;
  letter-spacing:4px;color:var(--gold);margin:0;
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
  color:var(--gray-blue);font-size:.88rem;line-height:1.6;
}
.concept-box .concept-body p{text-indent:0!important;text-align:left!important;color:var(--gray-blue);margin-bottom:.5em}
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
.key-read{margin:3em auto 1.5em;max-width:380px;text-align:center}
.kr-rule{width:180px;height:1px;background:var(--gold);opacity:.35;margin:0 auto}
.kr-text{
  font-style:italic;color:var(--gold);font-size:.92rem;
  font-weight:600;line-height:1.55;padding:18px 8px;margin:0;text-indent:0!important;
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
.toc-ch{
  display:flex;align-items:baseline;padding:5px 0 5px 16px;font-size:.82rem;
}
.toc-num{color:var(--gold);font-weight:600;min-width:32px;flex-shrink:0}
.toc-title{flex-shrink:0}
.toc-dots{
  flex-grow:1;margin:0 8px;
  border-bottom:1px dotted var(--rule);min-width:20px;
}

/* ═══ FRONT MATTER ═══ */
.front-matter{max-width:520px;margin:0 auto;padding:60px 36px;break-before:page}
.front-matter h2{
  font-family:var(--sans);font-size:1rem;font-weight:700;
  letter-spacing:5px;color:var(--gold);text-align:center;margin-bottom:2.5em;
}
.front-matter p{margin-bottom:.9em;font-size:.92rem;line-height:1.6}

/* ═══ DEFINITIONS PAGE ═══ */
.definitions{
  max-width:440px;margin:0 auto;padding:100px 36px 60px;
  text-align:center;break-before:page;break-after:page;
}
.def-word{font-family:var(--sans);font-size:.85rem;letter-spacing:5px;color:var(--dim);margin-bottom:6px}
.def-phonetic{font-size:.72rem;color:var(--gray-blue);margin-bottom:3px}
.def-pos{font-size:.72rem;color:var(--dim);font-style:italic;margin-bottom:14px}
.def-meaning{font-size:.88rem;line-height:1.65;max-width:380px;margin:0 auto 50px}

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
[data-part="1"] .section-header,[data-part="2"] .section-header{border-bottom-color:var(--blue)}
[data-part="1"] .felt-before,[data-part="2"] .felt-before{border-color:rgba(26,143,168,.25)}
[data-part="1"] .felt-label,[data-part="2"] .felt-label{color:var(--blue)}
[data-part="1"] .obs-ref,[data-part="2"] .obs-ref{color:var(--blue)}
/* Part 3: Transitional — blue-gold blend */
[data-part="3"] .section-header{border-bottom-color:#8BAAB8}
[data-part="3"] .chapter-number{color:#B8A060}
/* Parts 4-5: Applied gold — mastery */
[data-part="4"] .key-read .kr-text,[data-part="5"] .key-read .kr-text{color:#C9A84C}
[data-part="4"] .chapter-number,[data-part="5"] .chapter-number{color:var(--gold)}
/* Parts 6-7: Authority — deep warm gold */
[data-part="6"] .section-header,[data-part="7"] .section-header{border-bottom-color:#D4A030}
[data-part="6"] .chapter-number,[data-part="7"] .chapter-number{color:#D4A030}
[data-part="6"] .spotlight-box,[data-part="7"] .spotlight-box{border-left-color:#D4A030}
[data-part="6"] .key-read .kr-text,[data-part="7"] .key-read .kr-text{color:#D4A030}
/* Part 8: Full command — amber */
[data-part="8"] .section-header{border-bottom-color:#C8901A}
[data-part="8"] .chapter-number{color:#C8901A}
[data-part="8"] .spotlight-box{border-left-color:#C8901A}
[data-part="8"] .key-read .kr-text{color:#C8901A}

/* ═══ CHAPTER OPENER LEGEND ═══ */
.opener-legend{
  margin-top:40px;padding-top:22px;
  border-top:1px solid rgba(201,168,76,.18);
  display:flex;flex-direction:column;align-items:center;gap:14px;
}
.opener-legend .tier-row{display:flex;align-items:center;gap:8px;flex-wrap:wrap;justify-content:center}
.opener-legend .icon-row{display:flex;align-items:center;gap:14px;flex-wrap:wrap;justify-content:center}
.opener-legend .legend-label{
  font-family:var(--sans);font-size:.42rem;letter-spacing:3px;
  color:var(--dim);text-transform:uppercase;margin-top:4px;
}
.icon-item{display:flex;align-items:center;gap:5px}
.icon-item svg{opacity:.7}
.icon-item .icon-code{
  font-family:var(--sans);font-size:.42rem;font-weight:700;
  letter-spacing:1.5px;
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

    # ── CONTENT ──
    global_para = 0

    for section in sections:
        stype = section['type']
        part_num = section.get('part_num', 0)

        if stype == 'front_matter':
            html.append(f'<section class="front-matter"><h2>{escape(section["title"].upper())}</h2>')
            for para in section['content']:
                if para.strip():
                    html.append(f'<p>{escape(para.strip())}</p>')
            html.append('</section>')

        elif stype == 'part':
            html.append(gen_part_opener(section))
            # Part body content (Field Notes, NPM)
            content_paras = [p for p in section['content'] if p.strip()]
            if content_paras:
                html.append(f'<article class="chapter-body" data-part="{part_num}">')
                html.append(f'<header class="running-header"><span>THE ARCHITECTURE OF WONDER</span><span>{escape(section.get("subtitle","").upper())}</span></header>')
                for para in content_paras:
                    processed = process_paragraph(para, part_num)
                    if processed:
                        html.append(processed)
                html.append('<div class="page-footer">THE ARCHITECTURE OF WONDER\u2003|\u2003DECODE BEHAVIOR</div>')
                html.append('</article>')

        elif stype == 'chapter':
            html.append(gen_chapter_opener(section))
            html.append(f'<article class="chapter-body" data-part="{part_num}">')
            body, global_para = build_chapter_body(section, global_para)
            html.append(body)
            html.append('<div class="page-footer">THE ARCHITECTURE OF WONDER\u2003|\u2003DECODE BEHAVIOR</div>')
            html.append('</article>')

        elif stype == 'glossary':
            html.append(gen_chapter_opener({
                'type':'chapter','chapter_num':0,'part_num':9,
                'title':'Glossary','chapter_key':'GLOSSARY'
            }))
            html.append('<article class="chapter-body">')
            html.append('<header class="running-header"><span>THE ARCHITECTURE OF WONDER</span><span>GLOSSARY</span></header>')
            for para in section['content']:
                if para.strip():
                    html.append(f'<p>{escape(para.strip())}</p>')
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
