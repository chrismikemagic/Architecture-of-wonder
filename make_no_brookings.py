#!/usr/bin/env python
"""Produce manuscript-extracted-NoBrookings.txt by stripping every section listed
in brookings_manifest.py from manuscript-extracted.txt.

For each entry, removes lines from the `start` header up to (but not including)
the first subsequent line equal to `end_anchor`. Reports exactly what it removed
so the result can be eyeballed.

Usage:
    python make_no_brookings.py
    python make_no_brookings.py <in.txt> <out.txt>
"""
import sys
import os

from brookings_manifest import BROOKINGS_SECTIONS

BASE = os.path.dirname(os.path.abspath(__file__))
IN = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "manuscript-extracted.txt")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(BASE, "manuscript-extracted-NoBrookings.txt")


def main():
    with open(IN, "r", encoding="utf-8") as f:
        lines = f.read().split("\n")

    # Collect index ranges to delete (start_idx inclusive, end_idx exclusive).
    to_delete = []
    for sec in BROOKINGS_SECTIONS:
        start, anchor = sec["start"], sec["end_anchor"]
        start_idx = None
        for i, ln in enumerate(lines):
            if ln.strip() == start:
                start_idx = i
                break
        if start_idx is None:
            print(f"  ! WARNING: start header not found, skipping: {sec['id']!r} ({start!r})")
            continue
        end_idx = None
        for j in range(start_idx + 1, len(lines)):
            if lines[j].strip() == anchor:
                end_idx = j
                break
        if end_idx is None:
            print(f"  ! WARNING: end_anchor not found after {sec['id']!r}; skipping to avoid over-deletion")
            continue
        to_delete.append((start_idx, end_idx, sec["id"]))

    # Apply deletions from the bottom up so indices stay valid.
    removed_total = 0
    for start_idx, end_idx, sid in sorted(to_delete, reverse=True):
        n = end_idx - start_idx
        removed_total += n
        del lines[start_idx:end_idx]
        print(f"  - removed {sid:<12} : {n} lines")

    # Collapse any 3+ consecutive blanks left behind.
    cleaned, blanks = [], 0
    for ln in lines:
        if ln.strip() == "":
            blanks += 1
            if blanks <= 2:
                cleaned.append(ln)
        else:
            blanks = 0
            cleaned.append(ln)

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(cleaned))

    print(f"Wrote {os.path.basename(OUT)}  (removed {removed_total} lines across "
          f"{len(to_delete)} Brookings sections)")


if __name__ == "__main__":
    main()
