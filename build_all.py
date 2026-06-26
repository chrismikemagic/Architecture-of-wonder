#!/usr/bin/env python
"""Build BOTH editions of Built for Wonder in one shot.

  MAIN edition (WITH Brookings material) -> the deployed version:
    Built-for-Wonder-DESIGNED.html
    Built-for-Wonder-GATED.html        (deployed to v2 as index.html)

  NO-BROOKINGS edition (Brookings sections stripped):
    Built-for-Wonder-NoBrookings-DESIGNED.html
    Built-for-Wonder-NoBrookings-GATED.html

Pipeline:
  1. extract_manuscript.py        Built-for-Wonder.docx -> manuscript-extracted.txt
  2. build-book.py  / build-gated.py            (main edition, default paths)
  3. make_no_brookings.py         manuscript-extracted.txt -> *-NoBrookings.txt
  4. build-book.py  / build-gated.py            (no-Brookings edition, explicit paths)
"""
import subprocess
import sys
import os

BASE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable


def run(*args):
    print(f"\n$ {' '.join(os.path.basename(a) if i == 1 else a for i, a in enumerate(args))}")
    subprocess.run(args, cwd=BASE, check=True)


def main():
    # 1. Extract
    run(PY, os.path.join(BASE, "extract_manuscript.py"))

    # 2. MAIN edition (defaults: manuscript-extracted.txt -> Built-for-Wonder-DESIGNED/GATED)
    run(PY, os.path.join(BASE, "build-book.py"))
    run(PY, os.path.join(BASE, "build-gated.py"))

    # 3. No-Brookings manuscript
    run(PY, os.path.join(BASE, "make_no_brookings.py"))

    # 4. NO-BROOKINGS edition (explicit input/output paths)
    nb_txt = os.path.join(BASE, "manuscript-extracted-NoBrookings.txt")
    nb_designed = os.path.join(BASE, "Built-for-Wonder-NoBrookings-DESIGNED.html")
    nb_gated = os.path.join(BASE, "Built-for-Wonder-NoBrookings-GATED.html")
    run(PY, os.path.join(BASE, "build-book.py"), nb_txt, nb_designed)
    run(PY, os.path.join(BASE, "build-gated.py"), nb_designed, nb_gated)

    print("\n[done] Both editions built.")
    print("  MAIN (with Brookings):  Built-for-Wonder-GATED.html  -> deploy as v2/index.html")
    print("  NO-BROOKINGS:           Built-for-Wonder-NoBrookings-GATED.html")


if __name__ == "__main__":
    main()
