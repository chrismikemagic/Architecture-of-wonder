# Built for Wonder — Version snapshot 2026-07-05 (publish prep)

This folder is an immutable snapshot of the book taken after the 2026-07-05
editing session. Nothing in the working repo or prior versions was overwritten
to create it. Source of truth remains the repo's `Built-for-Wonder.docx`; this
is a point-in-time copy.

Branch: `claude/publish-prep-rem-formatting-20260705`
(off `claude/release-prep-formatting-contributions-20260612`)

## What changed this session

### 1. New content — Chapter 19 (Chris's own idea)
Added a new section, **"Where the Swinging Watch Comes From,"** immediately after
"The Alpha Shift" in Ch19 (HOW HYPNOSIS REALLY WORKS). It explains that rhythmic
light flickering across closed eyes — the back-seat car ride, sun strobing
through trees, streetlights sweeping past — echoes the eye activity of
REM/hypnagogic drift and produces that heavy, relaxed, sleepy feeling, and that
this is the real mechanism behind the swinging watch. It pays off the chapter's
own "no swinging watch" setup and its earlier dream section.

- In Chris's voice: no em dashes; uneven contrasts / standalone imperatives only
  (no mirror-pair or deny-rename-command AI tells); REM glossed inline.
- Chris's own material, not Atlas Brookings — ships in BOTH editions, no
  `brookings_manifest.py` entry.
- Insertion script: `insert_swinging_watch.py`.
- Verified: renders as an `h3` section header; 0 lines removed / 8 added;
  46 chapter openers intact; present in all four HTML outputs.

### 2. Mechanical fixes — 76 applied, 7 held back
A 45-chapter editorial audit produced 83 double-verified mechanical-fix
candidates (auditor safe-flag + adversarial verifier). After a character-level
review, **76 pure spelling/spacing/punctuation/homophone corrections were
applied** run-aware (inline bold/italic preserved); **7 were held back** because
they were rewrites, would introduce errors, or are header-separator style
choices. Full record: `mechanical-fixes-apply-log.json` and the "Session actions"
section of `EDITORIAL-AUDIT-2026-07-05.md`.

Apply script: `apply_audit_fixes_20260705.py` (idempotent, backs up first).

### 3. Build fix — orphaned marker tokens no longer leak to readers
Four unresolved build placeholder tokens were rendering as literal visible
`<h3>` headers in the finished book: `CH18_DIAGNOSTIC_PANEL`, `CH18_IFYRE_PANEL`,
`PERF_ARCH_FRAMEWORK_SVG`, `PERFORMANCE_MATRIX`. `build-book.py` now drops any
unresolved `ALL_CAPS_WITH_UNDERSCORES` token that no handler claimed (last-resort
guard placed after every real handler, so `PATTERN_INTERRUPT_40PCT` and
`SIX_AREA_RADAR` content is untouched). Output only — the tokens remain in the
DOCX for you to delete or fill with real content.

### 3. Editorial audit report (the "notes for you")
`EDITORIAL-AUDIT-2026-07-05.md` — 515 findings across all chapters: high-priority
items, does-not-fit flags (nothing removed — your call), material/structure ideas,
tone/voice notes, and readability fixes. `all-findings-raw.json` is the complete
raw finding set.

## Files in this snapshot
- `Built-for-Wonder.docx` — source after this session's edits
- `Built-for-Wonder-DESIGNED.html` / `-GATED.html` — MAIN edition (with Brookings)
- `Built-for-Wonder-NoBrookings-DESIGNED.html` / `-GATED.html` — no-Brookings edition
- `EDITORIAL-AUDIT-2026-07-05.md` — the full editorial report
- `mechanical-fixes-apply-log.json` — exactly what was applied / skipped
- `all-findings-raw.json` — all 515 raw audit findings

## Not done (deliberately — needs your go)
- **Live deploy.** The GATED file was NOT copied to `../Architecture-of-wonder-v2/index.html`
  and nothing was pushed to Netlify. To deploy after review:
  `cp Built-for-Wonder-GATED.html /c/Users/Chris/Architecture-of-wonder-v2/index.html`,
  then commit + push v2 `main`.
- The 12+ high-severity content issues in the audit (placeholder text in Ch3,
  the Ch4 habit contradiction, shaky stats, worked-system math in Ch24/Ch25,
  build-token placeholders) are flagged, not fixed — they need your judgment.

## How to reproduce this build
```
python insert_swinging_watch.py       # (already applied; backs up first)
python apply_audit_fixes_20260705.py  # (already applied; backs up first)
python build_all.py                   # rebuild both editions
```
