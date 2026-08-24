#!/usr/bin/env python3
"""Reusable DOCX editing engine for editorial passes on Built-for-Wonder.docx.

Extracted from apply_spike_edits.py (2026-08-13) so later passes can import it
instead of copying the code. Operations work on the concatenated w:t text of a
paragraph and splice replacements back into the existing runs, so run
formatting (italics, bold) is preserved wherever the edit does not cross it.

Usage:
    from docx_engine import Doc, para_text, flex_pattern
    doc = Doc()
    doc.edit("old substring", "new substring", label="P1")
    doc.save(backup_tag="pre-something")
"""
import copy
import re
import shutil
import zipfile
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "Built-for-Wonder.docx"
BACKUP_DIR = ROOT / "backups"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML_NS = "http://www.w3.org/XML/1998/namespace"
ET.register_namespace("w", W)
ET.register_namespace("r", "http://schemas.openxmlformats.org/officeDocument/2006/relationships")
ET.register_namespace("w14", "http://schemas.microsoft.com/office/word/2010/wordml")


def q(tag):
    return f"{{{W}}}{tag}"


def para_text(el):
    return "".join(t.text or "" for t in el.iter(q("t")))


def flex_pattern(literal):
    """Regex matching literal with straight/curly quote flexibility."""
    out = []
    for ch in literal:
        if ch in "'’‘":
            out.append("['’‘]")
        elif ch in '"“”':
            out.append('["“”]')
        else:
            out.append(re.escape(ch))
    return re.compile("".join(out))


def splice(el, start, end, replacement):
    """Replace char range [start,end) of el's concatenated w:t text."""
    pos = 0
    ts = list(el.iter(q("t")))
    done_insert = False
    for t in ts:
        txt = t.text or ""
        t_start, t_end = pos, pos + len(txt)
        pos = t_end
        if t_end <= start or t_start >= end:
            continue
        pre = txt[: max(0, start - t_start)]
        post = txt[max(0, min(len(txt), end - t_start)):]
        if not done_insert:
            t.text = pre + replacement + post
            done_insert = True
        else:
            t.text = pre + post
    assert done_insert, "splice found no covering text node"


class Doc:
    def __init__(self, path=MASTER):
        self.path = Path(path)
        with zipfile.ZipFile(self.path) as z:
            self.root = ET.fromstring(z.read("word/document.xml"))
        self.body = self.root.find(q("body"))
        self.failures = []

    # ── lookup ────────────────────────────────────────────────────────
    def paras(self):
        return list(self.root.iter(q("p")))

    def find_paras(self, pattern):
        hits = []
        for el in self.paras():
            m = pattern.search(para_text(el))
            if m:
                hits.append((el, m))
        return hits

    def unique_para(self, probe, exact=False):
        if exact:
            hits = [el for el in self.paras() if para_text(el).strip() == probe]
        else:
            pat = flex_pattern(probe)
            hits = [el for el, _ in self.find_paras(pat)]
        assert len(hits) == 1, f"probe {probe!r}: {len(hits)} hits"
        return hits[0]

    def parent_of(self, el):
        for anc in self.root.iter():
            if el in list(anc):
                return anc
        return None

    def next_para(self, el):
        """Next w:p sibling (skipping non-paragraph siblings)."""
        parent = self.parent_of(el)
        kids = list(parent)
        i = kids.index(el)
        for k in kids[i + 1:]:
            if k.tag == q("p"):
                return k
        return None

    def prev_para(self, el):
        parent = self.parent_of(el)
        kids = list(parent)
        i = kids.index(el)
        for k in reversed(kids[:i]):
            if k.tag == q("p"):
                return k
        return None

    # ── edits ─────────────────────────────────────────────────────────
    def edit(self, find, replace, expect=1, label=""):
        pat = flex_pattern(find)
        hits = self.find_paras(pat)
        if len(hits) != expect:
            msg = f"[{label}] expected {expect} match(es), got {len(hits)}: {find[:70]!r}"
            print("  !!", msg)
            self.failures.append(msg)
            return False
        for el, m in hits:
            # a paragraph may contain the substring more than once; replace all
            text = para_text(el)
            for mm in reversed(list(pat.finditer(text))):
                splice(el, mm.start(), mm.end(), replace)
        print(f"  ok [{label}] x{expect}: {find[:60]!r}")
        return True

    def whole_para_swap(self, old, new, label="", expect=1):
        found = [el for el in self.paras() if para_text(el).strip() == old]
        if len(found) != expect:
            msg = f"[{label}] whole-para {old!r}: {len(found)} matches (expected {expect})"
            print("  !!", msg)
            self.failures.append(msg)
            return False
        for el in found:
            m = re.search(re.escape(old), para_text(el))
            splice(el, m.start(), m.end(), new)
        print(f"  ok [{label}] heading: {old!r} -> {new!r}")
        return True

    def set_para(self, el, new_text):
        """Replace all runs of el with one run (cloned formatting) holding new_text."""
        runs = el.findall(q("r"))
        assert runs, "paragraph without runs"
        proto = copy.deepcopy(runs[0])
        for child in list(proto):
            if child.tag != q("rPr"):
                proto.remove(child)
        t = ET.SubElement(proto, q("t"))
        t.set(f"{{{XML_NS}}}space", "preserve")
        t.text = new_text
        for r in runs:
            el.remove(r)
        el.append(proto)

    def delete_para(self, el):
        parent = self.parent_of(el)
        if parent is None:
            return False
        parent.remove(el)
        return True

    def delete_exact(self, text, label="", expect=1):
        found = [el for el in self.paras() if para_text(el).strip() == text]
        if len(found) != expect:
            msg = f"[{label}] delete {text[:60]!r}: {len(found)} matches (expected {expect})"
            print("  !!", msg)
            self.failures.append(msg)
            return False
        for el in found:
            self.delete_para(el)
        print(f"  ok [{label}] deleted x{expect}: {text[:60]!r}")
        return True

    def split_para(self, probe, first, second, label=""):
        """Split the unique paragraph matching probe into two paragraphs."""
        try:
            el = self.unique_para(probe)
        except AssertionError as e:
            print("  !!", f"[{label}] {e}")
            self.failures.append(f"[{label}] {e}")
            return False
        parent = self.parent_of(el)
        idx = list(parent).index(el)
        clone = copy.deepcopy(el)
        self.set_para(el, first)
        self.set_para(clone, second)
        parent.insert(idx + 1, clone)
        print(f"  ok [{label}] split: {first[:40]!r} | {second[:40]!r}")
        return True

    def merge_with_next(self, probe, joiner=" ", new_text=None, label="", exact=True):
        """Merge the unique paragraph matching probe with the paragraph after it.
        new_text overrides the merged result if given."""
        try:
            el = self.unique_para(probe, exact=exact)
        except AssertionError as e:
            print("  !!", f"[{label}] {e}")
            self.failures.append(f"[{label}] {e}")
            return False
        nxt = self.next_para(el)
        merged = new_text if new_text is not None else (
            para_text(el).strip() + joiner + para_text(nxt).strip())
        self.set_para(el, merged)
        self.delete_para(nxt)
        print(f"  ok [{label}] merged: {merged[:60]!r}")
        return True

    def sweep(self, pattern, repl, label="", flags=0):
        pat = re.compile(pattern, flags)
        n = 0
        for el in self.paras():
            text = para_text(el)
            for m in reversed(list(pat.finditer(text))):
                splice(el, m.start(), m.end(), m.expand(repl) if "\\" in repl else repl)
                n += 1
        print(f"  sweep [{label}] {pattern!r}: {n} replacements")
        return n

    # ── save ──────────────────────────────────────────────────────────
    def save(self, backup_tag="pre-edit"):
        BACKUP_DIR.mkdir(exist_ok=True)
        backup = BACKUP_DIR / f"Built-for-Wonder.{backup_tag}-{date.today().isoformat()}.docx"
        if not backup.exists():
            shutil.copy2(self.path, backup)
            print(f"backup: {backup.name}")
        new_doc = ET.tostring(self.root, xml_declaration=True, encoding="UTF-8")
        tmp = self.path.with_suffix(".tmp.docx")
        with zipfile.ZipFile(self.path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = new_doc if item.filename == "word/document.xml" else zin.read(item.filename)
                zout.writestr(item, data)
        tmp.replace(self.path)
        print("saved", self.path.name)
