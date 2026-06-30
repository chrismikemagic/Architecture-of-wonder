"""Registry of Atlas Brookings-sourced sections added to Built for Wonder.

Used by make_no_brookings.py to produce the no-Brookings edition. Each entry
marks a section in manuscript-extracted.txt to remove for that edition.

To register a NEW Brookings section: add an entry with
  - id:           short slug (docs only)
  - start:        the EXACT section-header line as it appears in the manuscript
  - end_anchor:   the EXACT text of the first line to KEEP after the section
                  (removal runs from `start` up to, but not including, this line)
Keep each Brookings section as the last thing before a natural boundary
(a "· · ·" separator, a chapter closer line, etc.) so end_anchor is unambiguous.
"""

BROOKINGS_SECTIONS = [
    {
        "id": "three-eras",
        "chapter": 1,
        "start": "THE THREE ERAS OF METHOD",
        "end_anchor": "Now we can formally begin where I originally intended. Let’s get started.",
    },
    {
        "id": "imbalanced",
        "chapter": 24,
        "start": "IMBALANCED",
        "end_anchor": "· · ·",
    },
    {
        "id": "preshow-failure",
        "chapter": "27A",  # standalone interlude beat (mirrors 7A/21A/37A)
        "start": "THE PRE-SHOW THAT LOOKS LIKE A FAILURE",
        "end_anchor": "· · ·",
    },
    {
        "id": "cloud-nine",
        "chapter": 25,
        "start": "CLOUD NINE",
        "end_anchor": "· · ·",
    },
]
