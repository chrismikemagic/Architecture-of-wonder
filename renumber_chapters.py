"""
Renumber chapter references >= 10 by incrementing by 1.
Goes from highest (42) to lowest (10) to avoid double-substitution.
"""
import re

BUILD_BOOK = r'C:\Users\Chris\Architecture-of-wonder-v2\build-book.py'
MANUSCRIPT  = r'C:\Users\Chris\Architecture-of-wonder-v2\manuscript-extracted.txt'

# ── build-book.py ────────────────────────────────────────────────────────────
with open(BUILD_BOOK, 'r', encoding='utf-8') as f:
    bb_text = f.read()

bb_replacements = 0

# Pattern: 'CHAPTER N' followed by either ' (end of token), : (section key), or
# end-of-word boundary.  We use a literal replacement loop, highest→lowest.
for n in range(42, 9, -1):   # 42, 41, ... 10
    old = f'CHAPTER {n}'
    new = f'CHAPTER {n + 1}'
    count = bb_text.count(old)
    if count:
        bb_text = bb_text.replace(old, new)
        bb_replacements += count
        print(f'  build-book.py: replaced {count}x  {old!r} -> {new!r}')

with open(BUILD_BOOK, 'w', encoding='utf-8') as f:
    f.write(bb_text)

print(f'\nbuild-book.py total replacements: {bb_replacements}')

# ── manuscript-extracted.txt ─────────────────────────────────────────────────
with open(MANUSCRIPT, 'r', encoding='utf-8') as f:
    ms_text = f.read()

ms_replacements = 0

# In the manuscript the headers appear as "^CHAPTER N\n<Title>" — but the
# task says to replace CHAPTER 10 and all subsequent headers (i.e. numbers
# from 10 upward on their own line).  We match CHAPTER N at start of line
# (or anywhere — the manuscript only uses "CHAPTER N" as chapter headers for
# the numbered chapters; using .replace() is safe because we go high→low).
for n in range(42, 9, -1):   # 42, 41, ... 10
    old = f'CHAPTER {n}'
    new = f'CHAPTER {n + 1}'
    count = ms_text.count(old)
    if count:
        ms_text = ms_text.replace(old, new)
        ms_replacements += count
        print(f'  manuscript: replaced {count}x  {old!r} -> {new!r}')

with open(MANUSCRIPT, 'w', encoding='utf-8') as f:
    f.write(ms_text)

print(f'\nmanuscript total replacements: {ms_replacements}')
print(f'\nGrand total: {bb_replacements + ms_replacements} replacements')
