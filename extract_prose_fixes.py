"""Extract prose-level (non-HTML) replacement pairs from the audit-fix scripts.

A pair is "prose-level" when neither the old nor new string contains an HTML
tag (`<...>`). Those are the candidates to backport into the DOCX. Structural
HTML rebuilds are handled by build-book.py and don't belong in the source.
"""
from __future__ import annotations
import ast
import sys
from pathlib import Path

SCRIPTS = [
    Path(__file__).parent / "apply_audit_fixes.py",
    Path(__file__).parent / "apply_audit_fixes_pass2.py",
]


def is_html(s: str) -> bool:
    return "<" in s and ">" in s


def extract_pairs(path: Path):
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fname = getattr(node.func, "id", None)
        if fname not in ("must_replace", "maybe_replace"):
            continue
        # Args: old, new, label=...
        if len(node.args) < 2:
            continue
        try:
            old = ast.literal_eval(node.args[0])
            new = ast.literal_eval(node.args[1])
        except (ValueError, SyntaxError):
            continue
        # label may be kwarg
        label = ""
        for kw in node.keywords:
            if kw.arg == "label":
                try:
                    label = ast.literal_eval(kw.value)
                except (ValueError, SyntaxError):
                    label = ""
        if not isinstance(old, str) or not isinstance(new, str):
            continue
        out.append((old, new, label, path.name, node.lineno))
    return out


def main():
    all_pairs = []
    for p in SCRIPTS:
        all_pairs.extend(extract_pairs(p))

    prose = [t for t in all_pairs if not is_html(t[0]) and not is_html(t[1])]
    structural = [t for t in all_pairs if is_html(t[0]) or is_html(t[1])]

    print(f"# Total replacement calls: {len(all_pairs)}")
    print(f"# Prose-level (DOCX-backport candidates): {len(prose)}")
    print(f"# Structural (HTML-only — handled by build-book.py): {len(structural)}")
    print()
    print("=" * 70)
    print("PROSE-LEVEL FIXES (candidates for DOCX backport)")
    print("=" * 70)
    for i, (old, new, label, fname, lineno) in enumerate(prose, 1):
        print(f"\n[{i:02d}] {label}  ({fname}:{lineno})")
        print(f"  - {old!r}")
        print(f"  + {new!r}")


if __name__ == "__main__":
    main()
