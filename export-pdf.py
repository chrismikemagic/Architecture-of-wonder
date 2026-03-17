#!/usr/bin/env python3
"""
The Architecture of Wonder — PDF Export Script
Converts the designed HTML output into a print-ready 6"×9" PDF using Chrome headless.

Usage:
    python export-pdf.py

Output:
    Architecture-of-Wonder-FINAL.pdf

Requirements:
    Google Chrome installed (detected automatically at default Windows path)
"""

import os
import subprocess
import sys

INPUT_HTML = "Architecture-of-Wonder-DESIGNED.html"
OUTPUT_PDF = "Architecture-of-Wonder-FINAL.pdf"

# Common Chrome install paths on Windows
CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",  # Edge fallback
]


def find_chrome():
    for path in CHROME_PATHS:
        if os.path.exists(path):
            return path
    return None


def export_pdf():
    if not os.path.exists(INPUT_HTML):
        print(f"Error: {INPUT_HTML} not found. Run build-book.py first.")
        sys.exit(1)

    chrome = find_chrome()
    if not chrome:
        print("Chrome not found at default paths.")
        print_manual_instructions()
        sys.exit(1)

    html_abs = os.path.abspath(INPUT_HTML)
    pdf_abs = os.path.abspath(OUTPUT_PDF)

    print(f"Using: {chrome}")
    print(f"Input:  {html_abs}")
    print(f"Output: {pdf_abs}")
    print("Generating PDF...")

    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--run-all-compositor-stages-before-draw",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={pdf_abs}",
        # 6"×9" in microns: 6*25400=152400, 9*25400=228600
        "--print-paper-size-width=152400",
        "--print-paper-size-height=228600",
        f"file:///{html_abs.replace(chr(92), '/')}",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Chrome exited with code {result.returncode}")
        if result.stderr:
            print(result.stderr[:500])
        print("\nFalling back to manual instructions:")
        print_manual_instructions()
        sys.exit(1)

    if os.path.exists(pdf_abs):
        size_mb = os.path.getsize(pdf_abs) / (1024 * 1024)
        print(f"\nDone. {OUTPUT_PDF} ({size_mb:.1f} MB)")
    else:
        print("PDF file not created. Chrome may not support --print-paper-size flags.")
        print("Try the manual export instead:")
        print_manual_instructions()


def print_manual_instructions():
    print("""
─────────────────────────────────────────────
Manual PDF Export (Browser Print-to-PDF)
─────────────────────────────────────────────
1. Open Architecture-of-Wonder-DESIGNED.html in Chrome or Edge
2. Press Ctrl+P
3. Destination → Save as PDF
4. More settings:
   - Paper size: Custom — 6 x 9 inches (152.4 x 228.6 mm)
   - Margins: None  (CSS handles margins)
   - Background graphics: ON
5. Save as: Architecture-of-Wonder-FINAL.pdf
─────────────────────────────────────────────
""")


if __name__ == "__main__":
    export_pdf()
