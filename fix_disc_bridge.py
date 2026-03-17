#!/usr/bin/env python3
"""Fix DISC bridge placement: remove from Ch31, add before Ch8 separator."""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('manuscript-extracted.txt', encoding='utf-8') as f:
    content = f.read()

DISC_BRIDGE = """Signals That Point Toward DISC
The 80-Signal System gives you the raw data. DISC gives you the pattern that organizes it into a usable performance adjustment. The signals are not the personality type — they are the behavioral evidence that lets you predict pace, resistance, expressiveness, and compliance before the first instruction is given. Chapter 8 gives you the full DISC framework. The signals below are the fastest path to getting there.
D-Type Signals to Watch: #43 walking speed vs. crowd, #46 weight distribution at rest, #57 handshake pressure, #58 how quickly they sit, #67 interruption frequency, #71 reaction to contradiction, #80 how quickly they reclaim silence.
I-Type Signals to Watch: #08 eye contact willingness, #45 head tilt when listening, #50 humor reaction timing, #56 eyebrow expressiveness, #64 whether they mirror pace or tone, #72 speed of smile disappearance, #73 delay before laughter after others laugh.
S-Type Signals to Watch: #14 fidgeting level in public, #45 head tilt when listening, #49 breathing depth in conversation, #52 conversational distance preference, #66 speed of agreeing to small requests, #74 whether they ask permission before moving, #75 how they handle mistakes publicly.
C-Type Signals to Watch: #35 privacy screen on device, #42 notification response speed, #53 face touching during thinking, #59 whether they move objects before sitting, #65 response lag before answering personal questions, #76 whether they explain simple choices unprompted, #79 object straightening and alignment behavior."""

# Remove from wrong location (between last chapter body and first · · · after the bridge)
# The bridge section was inserted before a · · · separator in the wrong chapter
wrong_pattern = '\n\n' + DISC_BRIDGE + '\n\n· · ·'
if DISC_BRIDGE in content:
    # Find the bridge and remove it (just the bridge text + surrounding whitespace)
    idx = content.find(DISC_BRIDGE)
    # Remove from 2 newlines before to the bridge end
    before = content[:idx].rstrip('\n') + '\n'
    after = content[idx + len(DISC_BRIDGE):]
    content = before + after
    print('Removed DISC bridge from wrong location')
else:
    print('DISC bridge not found to remove')

# Find correct insertion: just before CHAPTER 8 in the manuscript
# The separator before Ch8 is · · · followed by blank lines then CHAPTER 8
ch8_match = re.search(r'(· · ·\n\n)\nCHAPTER 8\n', content)
if ch8_match:
    insert_at = ch8_match.start(1)
    content = content[:insert_at] + '\n' + DISC_BRIDGE + '\n\n' + content[insert_at:]
    print('DISC bridge inserted before Ch8 separator')
else:
    # Try alternate pattern
    ch8_match = re.search(r'(· · ·)\n+CHAPTER 8\n', content)
    if ch8_match:
        insert_at = ch8_match.start()
        content = content[:insert_at] + DISC_BRIDGE + '\n\n' + content[insert_at:]
        print('DISC bridge inserted before Ch8 (alternate)')
    else:
        print('Ch8 boundary not found — checking context:')
        idx = content.find('CHAPTER 8\n')
        print(f'  CHAPTER 8 at idx {idx}')
        print(f'  Context before: {repr(content[idx-50:idx])}')

with open('manuscript-extracted.txt', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done.')
