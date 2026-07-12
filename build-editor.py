#!/usr/bin/env python3
"""
build-editor.py — wrap the designed book in the editor layer.

Reads  Built-for-Wonder-DESIGNED.html
Writes an editor HTML file (same book + editor-config.js / editor.css /
        editor.js injected right before </body>).

The editor layer is additive: it never alters the book markup on disk. Editable
IDs are assigned in the browser at load time, so this stays a pure, repeatable
wrapper — re-run it any time the book source changes.

Usage:
  python build-editor.py                       # -> editor.html, relative asset paths (local preview)
  python build-editor.py --base /edit/ --out edit-index.html
                                               # -> deploy build served at /edit (absolute asset paths)
"""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "Built-for-Wonder-DESIGNED.html"

INJECT_TMPL = """
<!-- ===== Built for Wonder — editor layer (injected by build-editor.py) ===== -->
<link rel="stylesheet" href="{base}editor.css">
<script src="{base}editor-config.js"></script>
<script defer src="{base}editor.js"></script>
<!-- ===== end editor layer ===== -->
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="",
                    help="URL prefix for injected assets, e.g. '/edit/'. Empty = relative (local).")
    ap.add_argument("--out", default="editor.html", help="Output filename (relative to this dir).")
    args = ap.parse_args()

    if not SRC.exists():
        print(f"ERROR: {SRC.name} not found. Run the book build first.", file=sys.stderr)
        return 1
    for asset in ("editor.css", "editor.js", "editor-config.js"):
        if not (HERE / asset).exists():
            print(f"ERROR: missing {asset}", file=sys.stderr)
            return 1

    html = SRC.read_text(encoding="utf-8")
    marker = "</body>"
    idx = html.rfind(marker)
    if idx == -1:
        print("ERROR: no </body> found in source HTML.", file=sys.stderr)
        return 1

    inject = INJECT_TMPL.format(base=args.base)
    out_path = HERE / args.out
    out_html = html[:idx] + inject + html[idx:]
    out_path.write_text(out_html, encoding="utf-8")

    print(f"OK  wrote {out_path.name}  ({len(out_html):,} bytes)")
    print(f"    asset base: {args.base or '(relative)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
