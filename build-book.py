#!/usr/bin/env python3
"""
The Architecture of Wonder — Book Design Generator
Converts the manuscript into a fully designed HTML book implementing
the complete design specification.
"""

import re
import html
import os

# ═══════════════════════════════════════════════════════════
# CONFIGURATION — Design System Constants
# ═══════════════════════════════════════════════════════════

COLORS = {
    'navy_dark': '#080F1A',
    'navy_light': '#0D1E30',
    'gold': '#C9A84C',
    'steel_blue': '#1A8FA8',
    'cream': '#F5F0E8',
    'red': '#A83030',
    'purple': '#6B52A0',
    'text_gray_blue': '#8A9AB5',
    'dim_gray': '#3A4A5C',
    'body_text': '#2A2520',
    'rule_color': '#D8D0C4',
}

# Part-to-color-temperature mapping
PART_COLORS = {
    1: {'accent': '#1A8FA8', 'accent2': '#C9A84C', 'temp': 'cool'},
    2: {'accent': '#1A8FA8', 'accent2': '#C9A84C', 'temp': 'cool'},
    3: {'accent': '#7A9A6C', 'accent2': '#C9A84C', 'temp': 'transitional'},
    4: {'accent': '#C9A84C', 'accent2': '#1A8FA8', 'temp': 'warm'},
    5: {'accent': '#C9A84C', 'accent2': '#A83030', 'temp': 'warm'},
    6: {'accent': '#C9A84C', 'accent2': '#6B52A0', 'temp': 'deep_warm'},
    7: {'accent': '#D4A030', 'accent2': '#C9A84C', 'temp': 'deep_warm'},
    8: {'accent': '#D4A030', 'accent2': '#C9A84C', 'temp': 'deep_warm'},
}

# Hook lines for chapters (from chapter-template.md)
HOOK_LINES = {
    'INTRODUCTION': '"What you are about to read was designed to demonstrate its own content. Every page is a performance."',
    'CHAPTER 1': '"Reality is not what happens. It is what they remember happening."',
    'CHAPTER 2': '"Your audience\'s brain is deciding what matters before you open your mouth."',
    'CHAPTER 3': '"The moment before the reveal is worth more than the reveal itself."',
    'CHAPTER 4': '"Dopamine does not reward the outcome. It rewards the anticipation."',
    'CHAPTER 5': '"Attention is not given. It is taken."',
    'CHAPTER 6': '"Authority is not claimed. It is perceived — in the first 250 milliseconds."',
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

# Key reads (chapter closers)
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

# Observation references to detect and badge
OBSERVATION_REFS = re.compile(r'Observation\s+#(\d+)', re.IGNORECASE)
TIER_REFS = re.compile(r'\b(T1|T2|T3|T4)\b')

# "What You Just Did" moments to insert (chapter number -> text)
WHAT_YOU_JUST_DID = {
    3: "You have been reading for approximately three minutes. Notice your breathing. It slowed when you hit the section on cortisol. That is your nervous system responding to content about threat — even though the threat is not real. Observation, applied to yourself.",
    7: "You have been reading this page for about ninety seconds. Notice which hand is holding the book. That is Observation #01 — handedness indicator. You just demonstrated it without thinking.",
    10: "If you skipped ahead to this chapter because the title interested you more than the previous one, that is salience at work. Your brain prioritized novelty over sequence. Chapter Two explained why.",
    15: "Notice your posture right now. Did you lean forward slightly in the last few paragraphs? That is engagement. Your body responded before your mind decided the content was interesting.",
    21: "You just turned to this chapter. Before reading a word, you formed an impression of its length by glancing at the page count. That is thin-slicing applied to a book. You do this with people too.",
    28: "Your eyes moved to this callout before reading the surrounding text. That is the Von Restorff effect — your brain prioritized the visually distinct element. Chapter Two taught you this. The book just demonstrated it.",
    36: "You are in the final section. Notice how your reading pace has changed. If it has accelerated, that is the recency effect — your brain knows it is close to the end and is already preparing to consolidate what it has learned.",
}

# Pattern interrupt statistics
PATTERN_INTERRUPTS = [
    {'number': '250', 'unit': 'MILLISECONDS', 'text': 'The time it takes your brain to form a first impression of a stranger.', 'source': 'Willis & Todorov, 2006 — Psychological Science', 'wyajd': 'You formed yours of this page in less time than that. What did you notice first — the number, or the word? That is salience at work.'},
    {'number': '40%', 'unit': 'INCREASE IN TRUST', 'text': 'The boost in perceived credibility when text is set in a highly readable font.', 'source': 'Processing Fluency Research, Cognitive Psychology', 'wyajd': 'The font you are reading right now was chosen for this reason. You trusted this book before you evaluated a single argument.'},
    {'number': '7', 'unit': 'EXPRESSIONS', 'text': 'The number of universal micro-expressions the human face produces. Each lasts less than one-fifth of a second.', 'source': 'Ekman & Friesen, 1971', 'wyajd': 'Your face made at least two of them while reading this page.'},
    {'number': '60,000×', 'unit': 'FASTER', 'text': 'The speed at which the brain processes color compared to text.', 'source': 'Visual Cognition Research', 'wyajd': 'The gold accent on this page reached your brain before the words did.'},
    {'number': '3', 'unit': 'SIGNALS', 'text': 'The minimum number of co-occurring behavioral signals required to form a reliable pattern.', 'source': 'The Five Cs — Clusters', 'wyajd': 'One signal is noise. Two is coincidence. Three is a read.'},
    {'number': '1/5', 'unit': 'OF A SECOND', 'text': 'The duration of a micro-expression. Blink and you miss it. But your limbic system does not.', 'source': 'Ekman, 2003', 'wyajd': ''},
    {'number': '85%', 'unit': 'OF DECISIONS', 'text': 'The percentage of consumer choices where color is cited as the primary factor.', 'source': 'Color Psychology in Marketing, 2024', 'wyajd': 'The cover of this book was designed with this statistic in mind.'},
    {'number': '5', 'unit': 'FILTERS', 'text': 'Context. Clusters. Congruence. Consistency. Culture. The Five Cs that separate noise from signal.', 'source': 'The Architecture of Wonder', 'wyajd': ''},
]


def parse_manuscript(filepath):
    """Parse the manuscript text into structured sections."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    lines = text.split('\n')
    sections = []
    current_section = None
    current_part = 0
    chapter_count = 0

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Detect PART headers
        part_match = re.match(r'^PART\s+(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT)\s*$', line)
        if part_match:
            part_names = {'ONE':1,'TWO':2,'THREE':3,'FOUR':4,'FIVE':5,'SIX':6,'SEVEN':7,'EIGHT':8}
            current_part = part_names.get(part_match.group(1), current_part)
            # Next line is part subtitle
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
            i += 2  # skip subtitle
            continue

        # Detect CHAPTER headers
        chapter_match = re.match(r'^CHAPTER\s+(\d+)\s*$', line)
        if chapter_match:
            chapter_num = int(chapter_match.group(1))
            chapter_count += 1
            # Next line is chapter title
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
            # Skip the separator line
            if i < len(lines) and '────' in lines[i]:
                i += 1
            continue

        # Detect INTRODUCTION
        if line == 'INTRODUCTION' and i > 106:  # Skip TOC entries
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

        # Detect GLOSSARY
        if line.startswith('GLOSSARY'):
            if current_section:
                sections.append(current_section)
            current_section = {
                'type': 'glossary',
                'chapter_num': 99,
                'part_num': 9,
                'title': 'Scientific, Behavioral, and Performance Terms',
                'content': [],
                'chapter_key': 'GLOSSARY'
            }
            i += 1
            continue

        # Detect ABOUT THE AUTHOR
        if line == 'ABOUT THE AUTHOR':
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

        # Detect ACKNOWLEDGMENTS
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

        # Skip TOC and front matter title page content (before line 107)
        if i < 107 and current_section is None:
            i += 1
            continue

        # Skip separator lines
        if '────' in line:
            i += 1
            continue

        # Add content to current section
        if current_section is not None:
            # Skip the repeated TOC block
            if line.startswith('TABLE OF CONTENTS'):
                # Skip until we hit the separator
                while i < len(lines) and '────' not in lines[i]:
                    i += 1
                i += 1
                continue
            current_section['content'].append(lines[i])

        i += 1

    if current_section:
        sections.append(current_section)

    return sections


def escape(text):
    """HTML escape text."""
    return html.escape(text) if text else ''


def process_paragraph(text, part_num=1):
    """Process a paragraph, adding tier badges, observation refs, etc."""
    if not text.strip():
        return ''

    t = escape(text.strip())

    # Add tier badges
    def tier_badge(m):
        tier = m.group(1)
        if tier == 'T1':
            return f'<span class="tier-badge t1">T1</span>'
        elif tier == 'T2':
            return f'<span class="tier-badge t2">T2</span>'
        elif tier == 'T3':
            return f'<span class="tier-badge t3">T3</span>'
        elif tier == 'T4':
            return f'<span class="tier-badge t4">T4</span>'
        return m.group(0)

    t = TIER_REFS.sub(tier_badge, t)

    # Bold observation references
    t = re.sub(r'Observation\s+#(\d+)', r'<span class="obs-ref">Observation #\1</span>', t, flags=re.IGNORECASE)

    # Detect section headers (all-caps lines, short)
    stripped = text.strip()
    if stripped.isupper() and len(stripped) < 100 and len(stripped) > 3 and not stripped.startswith('CHAPTER') and not stripped.startswith('PART'):
        return f'<h3 class="section-header">{t}</h3>'

    # Detect sub-headers (Title Case lines that are short)
    if len(stripped) < 80 and not stripped[0].islower() and stripped.endswith((':',)) and len(stripped.split()) < 12:
        return f'<h4 class="sub-header">{t}</h4>'

    return f'<p>{t}</p>'


def generate_chapter_opener(section):
    """Generate the dark chapter opener page."""
    ch_type = section['type']
    part_num = section.get('part_num', 0)
    chapter_num = section.get('chapter_num', 0)
    title = section.get('title', '')
    chapter_key = section.get('chapter_key', '')

    part_names = {0:'', 1:'PART ONE', 2:'PART TWO', 3:'PART THREE', 4:'PART FOUR',
                  5:'PART FIVE', 6:'PART SIX', 7:'PART SEVEN', 8:'PART EIGHT'}
    part_label = part_names.get(part_num, '')

    hook = HOOK_LINES.get(chapter_key, '')

    if ch_type == 'chapter' and chapter_num > 0:
        ch_display = f'{chapter_num:02d}'
        ch_label = f'CHAPTER {chapter_num}'
    elif ch_type == 'chapter' and chapter_num == 0:
        ch_display = '00'
        ch_label = 'INTRODUCTION'
    else:
        return ''

    return f'''
    <div class="chapter-opener" data-part="{part_num}">
        <div class="opener-content">
            <div class="part-label">{escape(part_label)}</div>
            <div class="gold-line"></div>
            <div class="chapter-number">{ch_display}</div>
            <div class="chapter-title">{escape(title.upper())}</div>
            <div class="gold-line thin"></div>
            <div class="hook-line">{hook}</div>
        </div>
    </div>
    '''


def generate_part_opener(section):
    """Generate the dark part opener spread."""
    part_num = section.get('part_num', 0)
    subtitle = section.get('subtitle', '')
    part_names = {1:'ONE', 2:'TWO', 3:'THREE', 4:'FOUR', 5:'FIVE', 6:'SIX', 7:'SEVEN', 8:'EIGHT'}
    part_name = part_names.get(part_num, '')

    return f'''
    <div class="part-opener" data-part="{part_num}">
        <div class="part-opener-content">
            <div class="part-number">PART {part_name}</div>
            <div class="gold-line wide"></div>
            <div class="part-title">{escape(subtitle)}</div>
        </div>
    </div>
    '''


def generate_pattern_interrupt(interrupt_data):
    """Generate a full-bleed dark pattern interrupt page."""
    return f'''
    <div class="pattern-interrupt">
        <div class="pi-content">
            <div class="gold-line"></div>
            <div class="pi-number">{interrupt_data['number']}</div>
            <div class="pi-unit">{interrupt_data['unit']}</div>
            <div class="gold-line"></div>
            <div class="pi-text">{escape(interrupt_data['text'])}</div>
            <div class="pi-source">{escape(interrupt_data['source'])}</div>
            {f'<div class="pi-wyajd">{escape(interrupt_data["wyajd"])}</div>' if interrupt_data.get('wyajd') else ''}
        </div>
    </div>
    '''


def generate_what_you_just_did(text):
    """Generate a What You Just Did moment."""
    return f'''
    <div class="what-you-just-did">
        <div class="wyajd-bar"></div>
        <p class="wyajd-text">{escape(text)}</p>
    </div>
    '''


def generate_key_read(text):
    """Generate the chapter-closing key read."""
    return f'''
    <div class="key-read">
        <div class="kr-rule"></div>
        <p class="kr-text">{escape(text)}</p>
        <div class="kr-rule"></div>
    </div>
    '''


def generate_spotlight_box(text):
    """Generate a Von Restorff spotlight box."""
    return f'''
    <div class="spotlight-box">
        <div class="spotlight-label">KEY PRINCIPLE</div>
        <p class="spotlight-text">{text}</p>
    </div>
    '''


def build_chapter_body(section, paragraph_count_global):
    """Build the body content of a chapter with all design elements inserted."""
    content = section.get('content', [])
    chapter_num = section.get('chapter_num', 0)
    part_num = section.get('part_num', 0)
    chapter_key = section.get('chapter_key', '')

    body_html = []
    paragraphs = []

    # Collect non-empty paragraphs
    for line in content:
        if line.strip():
            paragraphs.append(line)

    if not paragraphs:
        return '', paragraph_count_global

    # Process first paragraph with drop cap
    first_para = escape(paragraphs[0].strip())
    if len(first_para) > 1:
        drop_letter = first_para[0]
        rest = first_para[1:]
        body_html.append(f'<p class="first-para"><span class="drop-cap">{drop_letter}</span>{rest}</p>')
    else:
        body_html.append(f'<p>{first_para}</p>')

    # Track paragraph count for pattern interrupt insertion
    para_count = 1
    spotlight_inserted = False
    wyajd_inserted = False
    interrupt_idx = paragraph_count_global % len(PATTERN_INTERRUPTS)

    for i, para in enumerate(paragraphs[1:], start=1):
        para_count += 1
        paragraph_count_global += 1

        # Insert pattern interrupt every ~40 paragraphs (approximately 8-12 pages)
        if para_count > 0 and para_count % 40 == 0:
            pi = PATTERN_INTERRUPTS[interrupt_idx % len(PATTERN_INTERRUPTS)]
            body_html.append(generate_pattern_interrupt(pi))
            interrupt_idx += 1

        # Insert spotlight box at ~30% through chapter (once per chapter)
        if not spotlight_inserted and para_count > len(paragraphs) * 0.3 and para_count < len(paragraphs) * 0.5:
            # Find a good quote-like paragraph
            stripped = para.strip()
            if (stripped.startswith('"') or stripped.startswith("'") or
                ('principle' in stripped.lower()) or ('key' in stripped.lower()) or
                (len(stripped) < 200 and len(stripped) > 30)):
                body_html.append(generate_spotlight_box(escape(stripped)))
                spotlight_inserted = True
                continue

        # Insert "What You Just Did" moment if available for this chapter
        if not wyajd_inserted and chapter_num in WHAT_YOU_JUST_DID and para_count > len(paragraphs) * 0.6:
            body_html.append(generate_what_you_just_did(WHAT_YOU_JUST_DID[chapter_num]))
            wyajd_inserted = True

        # Process regular paragraph
        processed = process_paragraph(para, part_num)
        if processed:
            body_html.append(processed)

    # Add key read at end
    key_read = KEY_READS.get(chapter_key, '')
    if key_read:
        body_html.append(generate_key_read(key_read))

    return '\n'.join(body_html), paragraph_count_global


def generate_meta_reveal():
    """Generate the complete meta reveal section."""
    return '''
    <div class="chapter-opener meta-reveal-opener" data-part="6">
        <div class="opener-content">
            <div class="part-label">THE STANDING OVATION</div>
            <div class="gold-line"></div>
            <div class="chapter-number meta-number">✦</div>
            <div class="chapter-title">THE META REVEAL</div>
            <div class="gold-line thin"></div>
            <div class="hook-line">"This is the part where I tell you what I did."</div>
        </div>
    </div>

    <div class="chapter-body meta-reveal-body">
        <p class="first-para"><span class="drop-cap">Y</span>ou have been reading a book that demonstrated its own content on every page.</p>

        <p>Not metaphorically. Literally. Every surface of this object — the cover you picked up, the pages you turned, the colors that caught your eye, the sentences that stuck — was designed using the same behavioral architecture this book teaches you to build.</p>

        <p>Let me show you.</p>

        <div class="section-break">· · ·</div>

        <h3 class="section-header meta-header">THE COVER</h3>

        <p>You picked up this book and felt it before you read it. The soft-touch matte lamination created a tactile first impression — people react to texture before processing text. Your fingers registered quality before your eyes registered the title.</p>

        <p>Then there was the title itself: embossed, raised from the surface, finished in spot UV that caught the light differently than the matte background. If you tilted the book, you may have noticed a hidden line of text on the back cover, visible only at certain angles. If you found it, you already demonstrated the first lesson in this book: <span class="gold-inline">the trained eye sees what others miss.</span></p>

        <p>If you didn't find it, go back now. Tilt the cover in the light. It's there.</p>

        <p>That is <span class="gold-inline">observation</span>. That is what this book is about.</p>

        <div class="section-break">· · ·</div>

        <h3 class="section-header meta-header">THE COLOR ARC</h3>

        <p>Did you notice that the accents in this book changed temperature as you read? Parts One and Two used cool steel blues — clinical, analytical, cerebral. The colors said: <em>you are learning.</em> By Part Three, golds began appearing alongside the blues. By Parts Four and Five, gold dominated — warm, authoritative, confident. The colors said: <em>you are applying.</em> By Parts Six and Seven, deep golds and ambers took over entirely. The colors said: <em>you have arrived.</em></p>

        <p>You did not notice this consciously. Research confirms that color shifts signal mood transitions and identity changes without conscious awareness. The brain processes color <span class="gold-inline">sixty thousand times faster than text</span>. Your emotional arc through this book was primed by the palette before a single argument landed.</p>

        <p>That is <span class="gold-inline">behavioral priming</span>. Chapter Two taught you how it works. This book applied it to you.</p>

        <div class="section-break">· · ·</div>

        <h3 class="section-header meta-header">THE TYPOGRAPHY</h3>

        <p>The body text you've been reading — Garamond, set at eleven points on a warm cream background — was chosen because research shows that easier-to-read fonts increase perceived trustworthiness by up to <span class="gold-inline">forty percent</span>. You felt this book was credible before you decided it was credible. Processing fluency: the smoother the reading experience, the more the reader trusts the content.</p>

        <p>The chapter titles — geometric, sans-serif, all-caps, widely letterspaced — created a visual contrast that signaled "announcement" before each chapter. Your brain registered a shift from conversation to declaration. The rhythm of serif body text and sans-serif titles trained your expectations: <em>here comes something important.</em></p>

        <div class="section-break">· · ·</div>

        <h3 class="section-header meta-header">THE CHAPTER OPENERS</h3>

        <p>Every chapter opened with a single provocative sentence on a dark page. Not a summary. Not an overview. A hook.</p>

        <p class="standalone-quote">"Every person who walks toward you is already broadcasting."</p>
        <p class="standalone-quote">"The boardroom is the most dangerous stage you will ever work."</p>
        <p class="standalone-quote">"The walk to the stage is the performance."</p>

        <p>That is the <span class="gold-inline">serial position effect — primacy</span>. Your brain encodes the first item in a sequence more deeply than anything that follows. Those opening lines anchored your understanding of every chapter before you chose to engage with the content.</p>

        <div class="section-break">· · ·</div>

        <h3 class="section-header meta-header">THE KEY READS</h3>

        <p>Every chapter closed with a single sentence in gold, set between thin lines with generous whitespace.</p>

        <p class="standalone-quote">"The read is never one signal. The read is the chain."</p>
        <p class="standalone-quote">"The face is the performance. The hands are the truth."</p>
        <p class="standalone-quote">"Tension is not the enemy. Boredom is."</p>

        <p>That is the <span class="gold-inline">serial position effect — recency</span>. The last item in a sequence stays in working memory. Those closing lines were planted as seeds. They are the sentences you will remember from this book long after you forget the supporting details.</p>

        <div class="section-break">· · ·</div>

        <h3 class="section-header meta-header">THE PATTERN INTERRUPTS</h3>

        <p>Every eight to twelve pages, the layout changed. A full-bleed dark page with a single gold statistic. A sidebar that shifted the column width. A case study in a different format.</p>

        <p>Those were <span class="gold-inline">pattern interrupts — the Von Restorff effect</span>, also known as the isolation effect. When multiple similar items are present, the one that differs is most likely to be remembered. You remember those dark pages. You remember the 250-milliseconds statistic.</p>

        <div class="section-break">· · ·</div>

        <h3 class="section-header meta-header">THE MARGIN ICONS</h3>

        <p>From the early chapters onward, small icons appeared alongside the text: an eye for Baseline/Physical observations. A profile silhouette for Character Reading. A waveform for Verbal/Social. An arrow for Action/Motivation.</p>

        <p>By the midpoint, you were processing those icons without reading them. The icons trained your <span class="gold-inline">pattern recognition through repetitive priming</span> — repeated exposure building unconscious associations.</p>

        <div class="section-break">· · ·</div>

        <h3 class="section-header meta-header">THE DESIGN SUMMARY</h3>

        <div class="meta-summary">
            <div class="meta-item"><span class="gold-inline">Gold accents</span> — <span class="meta-label">Salience Architecture</span></div>
            <div class="meta-item"><span class="gold-inline">Cool-to-warm color arc</span> — <span class="meta-label">Behavioral Priming</span></div>
            <div class="meta-item"><span class="gold-inline">Chapter hooks</span> — <span class="meta-label">Serial Position — Primacy</span></div>
            <div class="meta-item"><span class="gold-inline">Key reads</span> — <span class="meta-label">Serial Position — Recency</span></div>
            <div class="meta-item"><span class="gold-inline">Dark pages</span> — <span class="meta-label">Von Restorff Isolation</span></div>
            <div class="meta-item"><span class="gold-inline">Margin icons</span> — <span class="meta-label">Repetitive Priming</span></div>
            <div class="meta-item"><span class="gold-inline">Readable fonts on cream</span> — <span class="meta-label">Processing Fluency (+40% trust)</span></div>
            <div class="meta-item"><span class="gold-inline">Spot UV hidden text</span> — <span class="meta-label">The Observation Test</span></div>
            <div class="meta-item"><span class="gold-inline">Edge color gradient</span> — <span class="meta-label">Progressive Identity Shift</span></div>
        </div>

        <div class="section-break">· · ·</div>

        <div class="meta-finale">
            <p class="finale-line">This book was not just written.</p>
            <p class="finale-line finale-main">It was designed to read you while you read it.</p>
            <p class="finale-line finale-close">And now you know how.</p>
        </div>
    </div>
    '''


def generate_css():
    """Generate the complete CSS stylesheet."""
    return '''
/* ═══════════════════════════════════════════════════════ */
/* THE ARCHITECTURE OF WONDER — Design System CSS         */
/* ═══════════════════════════════════════════════════════ */

/* ── FONTS ── */
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600&family=Montserrat:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;1,300;1,400&display=swap');

/* ── RESET & BASE ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --navy-dark: #080F1A;
    --navy-light: #0D1E30;
    --gold: #C9A84C;
    --gold-dim: rgba(201, 168, 76, 0.4);
    --steel-blue: #1A8FA8;
    --cream: #F5F0E8;
    --red: #A83030;
    --purple: #6B52A0;
    --text-gray-blue: #8A9AB5;
    --dim-gray: #3A4A5C;
    --body-text: #2A2520;
    --rule-color: #D8D0C4;
    --font-serif: 'EB Garamond', 'Georgia', 'Garamond', serif;
    --font-sans: 'Montserrat', 'Calibri', 'Helvetica Neue', sans-serif;
}

html {
    font-size: 11pt;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

body {
    font-family: var(--font-serif);
    color: var(--body-text);
    background: var(--cream);
    line-height: 1.55;
    max-width: 100%;
    overflow-x: hidden;
}

/* ── PRINT STYLES ── */
@page {
    size: 6in 9in;
    margin: 0.75in 1in 0.7in 0.7in;
}

@media print {
    body { background: white; }
    .chapter-opener, .part-opener, .pattern-interrupt { page-break-before: always; page-break-after: always; }
    .chapter-body { page-break-before: avoid; }
    .key-read { page-break-inside: avoid; }
    .spotlight-box { page-break-inside: avoid; }
    .no-print { display: none; }
}

/* ── FRONT MATTER ── */
.front-cover {
    background: linear-gradient(180deg, var(--navy-dark), var(--navy-light));
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 40px;
    page-break-after: always;
}

.front-cover .author-name {
    font-family: var(--font-sans);
    font-size: 0.75rem;
    letter-spacing: 6px;
    color: var(--text-gray-blue);
    font-weight: 300;
    margin-bottom: 40px;
}

.front-cover .book-title {
    font-family: var(--font-sans);
    font-size: 2.8rem;
    font-weight: 700;
    letter-spacing: 5px;
    color: var(--gold);
    text-align: center;
    line-height: 1.3;
    margin-bottom: 30px;
    text-shadow: 0 0 40px rgba(201, 168, 76, 0.15);
}

.front-cover .book-subtitle {
    font-family: var(--font-sans);
    font-size: 0.7rem;
    letter-spacing: 4px;
    color: var(--text-gray-blue);
    font-weight: 300;
    text-align: center;
    line-height: 1.6;
}

.front-cover .gold-rule {
    width: 200px;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold-dim), transparent);
    margin: 25px 0;
}

.front-cover .icon-row {
    display: flex;
    gap: 30px;
    margin-top: 40px;
    opacity: 0.3;
}

.front-cover .icon-row span {
    font-family: var(--font-sans);
    font-size: 0.6rem;
    letter-spacing: 2px;
    color: var(--gold);
}

.tagline {
    font-family: var(--font-sans);
    font-size: 0.55rem;
    letter-spacing: 5px;
    color: var(--dim-gray);
    margin-top: 40px;
}

/* ── CHAPTER OPENER ── */
.chapter-opener {
    background: linear-gradient(180deg, var(--navy-dark), var(--navy-light));
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 60px 40px;
    page-break-before: always;
    page-break-after: always;
}

.opener-content {
    text-align: center;
    max-width: 520px;
}

.part-label {
    font-family: var(--font-sans);
    font-size: 0.7rem;
    letter-spacing: 8px;
    color: var(--dim-gray);
    font-weight: 300;
    margin-bottom: 20px;
}

.chapter-number {
    font-family: var(--font-sans);
    font-size: 4.5rem;
    font-weight: 200;
    color: var(--gold);
    letter-spacing: 3px;
    margin: 20px 0;
    text-shadow: 0 0 30px rgba(201, 168, 76, 0.1);
}

.meta-number {
    font-size: 3rem;
    text-shadow: 0 0 40px rgba(201, 168, 76, 0.3);
}

.chapter-title {
    font-family: var(--font-sans);
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: 5px;
    color: #FFFFFF;
    line-height: 1.5;
    margin-bottom: 15px;
}

.gold-line {
    width: 160px;
    height: 1px;
    margin: 15px auto;
    background: linear-gradient(90deg, transparent, var(--gold-dim), transparent);
}

.gold-line.wide { width: 220px; }
.gold-line.thin { height: 0.5px; opacity: 0.6; }

.hook-line {
    font-family: var(--font-serif);
    font-size: 0.85rem;
    font-style: italic;
    color: var(--text-gray-blue);
    line-height: 1.6;
    margin-top: 20px;
    max-width: 400px;
    margin-left: auto;
    margin-right: auto;
}

/* ── PART OPENER ── */
.part-opener {
    background: linear-gradient(180deg, var(--navy-dark), var(--navy-light));
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 60px 40px;
    page-break-before: always;
    page-break-after: always;
}

.part-opener-content {
    text-align: center;
}

.part-number {
    font-family: var(--font-sans);
    font-size: 0.8rem;
    letter-spacing: 10px;
    color: var(--dim-gray);
    font-weight: 300;
    margin-bottom: 30px;
}

.part-title {
    font-family: var(--font-sans);
    font-size: 1.8rem;
    font-weight: 700;
    letter-spacing: 6px;
    color: var(--gold);
    line-height: 1.4;
    text-shadow: 0 0 40px rgba(201, 168, 76, 0.1);
}

/* ── CHAPTER BODY ── */
.chapter-body {
    max-width: 640px;
    margin: 0 auto;
    padding: 60px 40px 80px;
    background: var(--cream);
}

.chapter-body p {
    margin-bottom: 1em;
    text-align: justify;
    text-justify: inter-word;
    hyphens: auto;
}

.chapter-body .first-para {
    text-indent: 0;
}

.chapter-body p + p {
    text-indent: 1.5em;
}

.chapter-body p:has(+ .section-break),
.chapter-body .section-break + p,
.chapter-body h3 + p,
.chapter-body h4 + p,
.chapter-body .spotlight-box + p,
.chapter-body .what-you-just-did + p,
.chapter-body .pattern-interrupt + p {
    text-indent: 0;
}

/* ── DROP CAP ── */
.drop-cap {
    float: left;
    font-family: var(--font-sans);
    font-size: 3.3rem;
    font-weight: 400;
    color: var(--gold);
    line-height: 0.8;
    padding-right: 8px;
    padding-top: 6px;
}

/* ── SECTION HEADERS ── */
.section-header {
    font-family: var(--font-sans);
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 2px;
    color: var(--body-text);
    margin: 2.5em 0 1em;
    padding-bottom: 6px;
    border-bottom: 2px solid var(--gold);
    display: inline-block;
}

.meta-header {
    color: var(--gold);
    border-bottom-color: var(--gold);
}

.sub-header {
    font-family: var(--font-sans);
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--body-text);
    margin: 2em 0 0.8em;
}

/* ── SECTION BREAK ── */
.section-break {
    text-align: center;
    color: var(--gold);
    font-size: 1rem;
    letter-spacing: 8px;
    margin: 2em 0;
}

/* ── TIER BADGES ── */
.tier-badge {
    display: inline-block;
    font-family: var(--font-sans);
    font-size: 0.55rem;
    font-weight: 700;
    padding: 1px 8px;
    border-radius: 8px;
    vertical-align: middle;
    margin: 0 2px;
    letter-spacing: 0.5px;
}

.tier-badge.t1 { background: var(--gold); color: var(--navy-dark); }
.tier-badge.t2 { background: var(--steel-blue); color: #FFFFFF; }
.tier-badge.t3 { background: transparent; color: var(--text-gray-blue); border: 1px solid var(--text-gray-blue); }
.tier-badge.t4 { background: transparent; color: var(--dim-gray); border: 1px dashed var(--dim-gray); }

/* ── OBSERVATION REFERENCES ── */
.obs-ref {
    color: var(--gold);
    font-weight: 600;
}

/* ── GOLD INLINE ── */
.gold-inline {
    color: var(--gold);
    font-weight: 600;
}

/* ── SPOTLIGHT BOX (VON RESTORFF) ── */
.spotlight-box {
    background: linear-gradient(135deg, var(--navy-dark), var(--navy-light));
    border-left: 4px solid var(--gold);
    border-radius: 4px;
    padding: 24px 28px;
    margin: 2em 0;
}

.spotlight-label {
    font-family: var(--font-sans);
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 3px;
    color: var(--gold);
    margin-bottom: 12px;
}

.spotlight-text {
    font-style: italic;
    color: #FFFFFF;
    font-size: 1rem;
    line-height: 1.6;
    margin: 0;
}

/* ── PATTERN INTERRUPT ── */
.pattern-interrupt {
    background: linear-gradient(180deg, #060B14, var(--navy-light));
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 60px 40px;
    page-break-before: always;
    page-break-after: always;
}

.pi-content {
    text-align: center;
    max-width: 480px;
}

.pi-number {
    font-family: var(--font-sans);
    font-size: 5.5rem;
    font-weight: 200;
    color: var(--gold);
    text-shadow: 0 0 30px rgba(201, 168, 76, 0.2);
    letter-spacing: 3px;
}

.pi-unit {
    font-family: var(--font-sans);
    font-size: 0.8rem;
    letter-spacing: 4px;
    color: var(--gold);
    font-weight: 300;
    margin-bottom: 20px;
}

.pi-text {
    font-style: italic;
    color: var(--text-gray-blue);
    font-size: 0.85rem;
    line-height: 1.6;
    margin: 25px 0 15px;
}

.pi-source {
    font-size: 0.65rem;
    color: var(--dim-gray);
    margin-bottom: 30px;
}

.pi-wyajd {
    color: #FFFFFF;
    font-style: italic;
    font-size: 0.78rem;
    margin-top: 30px;
    line-height: 1.5;
}

.pi-wyajd::before {
    content: '';
    display: block;
    width: 40px;
    height: 1px;
    background: var(--gold);
    margin: 0 auto 15px;
    opacity: 0.4;
}

/* ── WHAT YOU JUST DID ── */
.what-you-just-did {
    display: flex;
    gap: 16px;
    margin: 2em 0;
    padding: 16px 0 16px 20px;
}

.wyajd-bar {
    width: 3px;
    background: var(--gold);
    opacity: 0.6;
    flex-shrink: 0;
    border-radius: 2px;
}

.wyajd-text {
    font-style: italic;
    color: var(--body-text);
    font-size: 0.9rem;
    line-height: 1.55;
    margin: 0 !important;
    text-indent: 0 !important;
}

/* ── KEY READ (CHAPTER CLOSER) ── */
.key-read {
    margin: 3em auto 2em;
    max-width: 400px;
    text-align: center;
}

.kr-rule {
    width: 200px;
    height: 1px;
    background: var(--gold);
    opacity: 0.4;
    margin: 0 auto;
}

.kr-text {
    font-style: italic;
    color: var(--gold);
    font-size: 0.95rem;
    font-weight: 600;
    line-height: 1.5;
    padding: 20px 10px;
    margin: 0;
    text-indent: 0 !important;
}

/* ── PULL QUOTE ── */
.pull-quote {
    text-align: center;
    margin: 2.5em auto;
    max-width: 420px;
    padding: 0 20px;
}

.pull-quote p {
    font-family: var(--font-sans);
    font-size: 1.05rem;
    font-weight: 600;
    font-style: italic;
    color: var(--gold);
    line-height: 1.5;
    text-indent: 0 !important;
    text-align: center !important;
}

.standalone-quote {
    text-align: center !important;
    font-style: italic;
    color: var(--gold) !important;
    font-weight: 500;
    margin: 1em 0 !important;
    text-indent: 0 !important;
}

/* ── META REVEAL SPECIFIC ── */
.meta-reveal-body {
    max-width: 640px;
}

.meta-summary {
    margin: 2em 0;
}

.meta-item {
    padding: 8px 0;
    border-bottom: 1px solid rgba(201, 168, 76, 0.15);
    font-size: 0.9rem;
}

.meta-label {
    font-family: var(--font-sans);
    font-size: 0.65rem;
    letter-spacing: 2px;
    color: var(--dim-gray);
    text-transform: uppercase;
}

.meta-finale {
    text-align: center;
    margin: 4em 0;
    padding: 40px 20px;
}

.finale-line {
    color: var(--gold);
    font-size: 1.1rem;
    font-style: italic;
    margin: 1.5em 0 !important;
    text-indent: 0 !important;
    text-align: center !important;
}

.finale-main {
    font-size: 1.2rem;
    font-weight: 600;
    text-shadow: 0 0 20px rgba(201, 168, 76, 0.15);
}

.finale-close {
    font-family: var(--font-sans);
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 4px;
    text-transform: uppercase;
    font-style: normal;
    margin-top: 2em !important;
}

/* ── RUNNING HEADER ── */
.running-header {
    font-family: var(--font-sans);
    font-size: 0.55rem;
    letter-spacing: 2px;
    color: var(--text-gray-blue);
    padding: 10px 0;
    margin-bottom: 10px;
    border-bottom: 0.5px solid var(--rule-color);
    display: flex;
    justify-content: space-between;
}

/* ── FOOTER ── */
.page-footer {
    font-family: var(--font-sans);
    font-size: 0.5rem;
    letter-spacing: 3px;
    color: var(--dim-gray);
    text-align: center;
    padding: 30px 0 10px;
    margin-top: 40px;
}

/* ── GLOSSARY ── */
.glossary-body p {
    margin-bottom: 0.6em;
    font-size: 0.9rem;
}

/* ── FRONT MATTER / ACKNOWLEDGMENTS ── */
.front-matter-body {
    max-width: 560px;
    margin: 0 auto;
    padding: 60px 40px;
}

.front-matter-body h2 {
    font-family: var(--font-sans);
    font-size: 1.2rem;
    font-weight: 700;
    letter-spacing: 4px;
    color: var(--gold);
    text-align: center;
    margin-bottom: 2em;
}

/* ── RESPONSIVE (for screen reading) ── */
@media screen and (max-width: 768px) {
    .chapter-body, .front-matter-body { padding: 30px 20px; }
    .chapter-number { font-size: 3.5rem; }
    .chapter-title { font-size: 1rem; letter-spacing: 3px; }
    .book-title { font-size: 2rem; }
    .pi-number { font-size: 4rem; }
}

/* ── COLOR TEMPERATURE SHIFTS ── */
/* Parts 1-2: Cool accents */
[data-part="1"] .chapter-title,
[data-part="2"] .chapter-title { color: #E8E8EE; }

[data-part="1"] .section-header,
[data-part="2"] .section-header { border-bottom-color: var(--steel-blue); }

/* Parts 3: Transitional */
[data-part="3"] .section-header { border-bottom-color: #7A9A6C; }

/* Parts 4-5: Warm gold */
/* Default gold styling applies */

/* Parts 6-7-8: Deep warm */
[data-part="6"] .spotlight-box,
[data-part="7"] .spotlight-box,
[data-part="8"] .spotlight-box {
    border-left-color: #D4A030;
}

[data-part="7"] .chapter-number,
[data-part="8"] .chapter-number {
    color: #D4A030;
}

/* ── TOC ── */
.toc {
    max-width: 520px;
    margin: 0 auto;
    padding: 60px 40px;
    page-break-after: always;
}

.toc h2 {
    font-family: var(--font-sans);
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 6px;
    color: var(--gold);
    text-align: center;
    margin-bottom: 3em;
}

.toc-part {
    font-family: var(--font-sans);
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 3px;
    color: var(--dim-gray);
    margin: 2em 0 0.5em;
    padding-top: 1em;
    border-top: 1px solid var(--rule-color);
}

.toc-chapter {
    font-size: 0.85rem;
    color: var(--body-text);
    padding: 4px 0 4px 20px;
}

.toc-chapter .ch-num {
    color: var(--gold);
    font-weight: 600;
    margin-right: 6px;
}
''';


def generate_toc(sections):
    """Generate a styled table of contents."""
    html_parts = ['<div class="toc"><h2>TABLE OF CONTENTS</h2>']
    current_part = -1

    part_subtitles = {}
    for s in sections:
        if s['type'] == 'part':
            part_subtitles[s['part_num']] = s.get('subtitle', '')

    for s in sections:
        if s['type'] == 'part':
            html_parts.append(f'<div class="toc-part">{escape(s["title"])} — {escape(s.get("subtitle", ""))}</div>')
        elif s['type'] == 'chapter':
            ch = s.get('chapter_num', 0)
            if ch == 0:
                html_parts.append(f'<div class="toc-chapter"><span class="ch-num">INTRO</span> {escape(s["title"])}</div>')
            else:
                html_parts.append(f'<div class="toc-chapter"><span class="ch-num">{ch}.</span> {escape(s["title"])}</div>')
        elif s['type'] == 'glossary':
            html_parts.append(f'<div class="toc-part">GLOSSARY</div>')
        elif s['type'] == 'about':
            html_parts.append(f'<div class="toc-part">ABOUT THE AUTHOR</div>')

    html_parts.append('</div>')
    return '\n'.join(html_parts)


def build_book(manuscript_path, output_path):
    """Build the complete designed HTML book."""
    print("Parsing manuscript...")
    sections = parse_manuscript(manuscript_path)
    print(f"Found {len(sections)} sections")

    css = generate_css()

    html_parts = [f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Architecture of Wonder — Decode Behavior</title>
    <style>{css}</style>
</head>
<body>
''']

    # ── FRONT COVER ──
    html_parts.append('''
    <div class="front-cover">
        <div class="author-name">C H R I S &nbsp; M I C H A E L</div>
        <div class="gold-rule"></div>
        <div class="book-title">THE<br>ARCHITECTURE<br>OF WONDER</div>
        <div class="gold-rule"></div>
        <div class="book-subtitle">THE BEHAVIORAL SCIENCE OF<br>PERFORMANCE &amp; PERCEPTION</div>
        <div class="gold-rule"></div>
        <div class="icon-row">
            <span>BP</span>
            <span>CR</span>
            <span>VS</span>
            <span>AM</span>
        </div>
        <div class="tagline">D E C O D E &nbsp; B E H A V I O R</div>
    </div>
    ''')

    # ── DEFINITIONS PAGE ──
    html_parts.append('''
    <div class="chapter-body" style="page-break-before: always; padding-top: 120px;">
        <div style="text-align: center; margin-bottom: 60px;">
            <p style="font-family: var(--font-sans); font-size: 0.9rem; letter-spacing: 4px; color: var(--dim-gray); margin-bottom: 30px;">wonder</p>
            <p style="font-size: 0.75rem; color: var(--text-gray-blue); margin-bottom: 5px;">/ˈwʌndər/</p>
            <p style="font-size: 0.75rem; color: var(--dim-gray); margin-bottom: 15px; font-style: italic;">noun</p>
            <p style="max-width: 400px; margin: 0 auto 50px; font-size: 0.9rem; line-height: 1.6;">A feeling of surprise mingled with admiration, caused by something beautiful, unexpected, unfamiliar, or inexplicable. The state of being open to what cannot yet be explained.</p>

            <div class="section-break">· · ·</div>

            <p style="font-family: var(--font-sans); font-size: 0.9rem; letter-spacing: 4px; color: var(--dim-gray); margin-bottom: 30px;">architecture</p>
            <p style="font-size: 0.75rem; color: var(--text-gray-blue); margin-bottom: 5px;">/ˈɑːrkɪtektʃər/</p>
            <p style="font-size: 0.75rem; color: var(--dim-gray); margin-bottom: 15px; font-style: italic;">noun</p>
            <p style="max-width: 400px; margin: 0 auto 50px; font-size: 0.9rem; line-height: 1.6;">The complex or carefully designed structure of something. The deliberate arrangement of elements to produce a specific experience in the person who moves through it.</p>
        </div>
    </div>
    ''')

    # ── TABLE OF CONTENTS ──
    html_parts.append(generate_toc(sections))

    # ── BOOK CONTENT ──
    paragraph_count = 0

    for section in sections:
        sec_type = section['type']

        if sec_type == 'front_matter':
            # Acknowledgments
            html_parts.append('<div class="front-matter-body" style="page-break-before: always;">')
            html_parts.append(f'<h2>{escape(section["title"].upper())}</h2>')
            for para in section['content']:
                if para.strip():
                    html_parts.append(f'<p>{escape(para.strip())}</p>')
            html_parts.append('</div>')

        elif sec_type == 'part':
            # Part opener
            html_parts.append(generate_part_opener(section))
            # Part content (Field Notes, NPM, etc.)
            if section['content']:
                html_parts.append(f'<div class="chapter-body" data-part="{section["part_num"]}">')
                for para in section['content']:
                    processed = process_paragraph(para, section['part_num'])
                    if processed:
                        html_parts.append(processed)
                html_parts.append('</div>')

        elif sec_type == 'chapter':
            # Chapter opener
            html_parts.append(generate_chapter_opener(section))
            # Chapter body
            html_parts.append(f'<div class="chapter-body" data-part="{section["part_num"]}">')
            body, paragraph_count = build_chapter_body(section, paragraph_count)
            html_parts.append(body)
            html_parts.append('<div class="page-footer">THE ARCHITECTURE OF WONDER &nbsp;|&nbsp; DECODE BEHAVIOR</div>')
            html_parts.append('</div>')

        elif sec_type == 'glossary':
            html_parts.append(generate_chapter_opener({
                'type': 'chapter', 'chapter_num': 0, 'part_num': 9,
                'title': 'Glossary', 'chapter_key': 'GLOSSARY'
            }))
            html_parts.append('<div class="chapter-body glossary-body">')
            for para in section['content']:
                if para.strip():
                    html_parts.append(f'<p>{escape(para.strip())}</p>')
            html_parts.append('</div>')

        elif sec_type == 'about':
            html_parts.append('<div class="chapter-body" style="page-break-before: always;">')
            html_parts.append('<h3 class="section-header" style="display: block; text-align: center;">ABOUT THE AUTHOR</h3>')
            for para in section['content']:
                if para.strip():
                    html_parts.append(f'<p>{escape(para.strip())}</p>')
            html_parts.append('</div>')

    # ── META REVEAL ──
    html_parts.append(generate_meta_reveal())

    # ── BACK COVER ──
    html_parts.append('''
    <div class="front-cover" style="page-break-before: always;">
        <div class="gold-rule"></div>
        <div class="book-title" style="font-size: 1.8rem;">THE ARCHITECTURE<br>OF WONDER</div>
        <div class="gold-rule"></div>
        <p style="color: var(--text-gray-blue); font-style: italic; font-size: 0.8rem; max-width: 400px; text-align: center; line-height: 1.6; margin: 20px 0;">
            Every design decision in this book demonstrates the psychology it teaches.
            The colors, the typography, the layout, the pattern interrupts — all of it
            was engineered using the same behavioral architecture you just learned to build.
        </p>
        <div class="gold-rule"></div>
        <p style="color: rgba(255,255,255,0.08); font-style: italic; font-size: 0.7rem; margin-top: 40px;">
            You're already reading people. You just proved it.
        </p>
        <div class="tagline" style="margin-top: 60px;">D E C O D E &nbsp; B E H A V I O R</div>
    </div>
    ''')

    html_parts.append('</body></html>')

    full_html = '\n'.join(html_parts)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f"Book written to {output_path}")
    print(f"File size: {len(full_html):,} characters")
    return len(full_html)


if __name__ == '__main__':
    manuscript = '/home/user/Architecture-of-wonder/manuscript-extracted.txt'
    output = '/home/user/Architecture-of-wonder/Architecture-of-Wonder-DESIGNED.html'
    build_book(manuscript, output)
