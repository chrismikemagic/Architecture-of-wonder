# 📖 Built for Wonder — Online Editor: handoff for Claude Code (Mac)

**Read this top to bottom, then drive the remaining steps with Chris.** This is a
continuation of work started on Chris's Windows machine. The online-editor feature
is fully built and tested; what's left is **Supabase setup → paste keys → deploy to
`/edit`**. Everything you need is in this repo.

---

## What this feature is

Instead of a Word export, Chris wanted a private web page where his **book editor**
can, from **phone or laptop**:
- **Edit the book text directly** — click any paragraph, type; changed blocks are
  highlighted and auto-saved.
- **Leave notes** — select any passage → **＋ Note** → comment. Notes collect in a
  panel **in the order added**.

Chris reviews all of it in a read-only **dashboard** (`review.html`): every edit as a
red/green before-after diff grouped by chapter, and every note in chronological order.

Decisions Chris already made (don't re-litigate): **cloud sync via Supabase** +
**direct-edit-with-notes** (not comment-only / not track-changes).

---

## Current state (done ✅)

- `editor.js` / `editor.css` — the editing engine + styles (an *additive layer*; it
  never edits book markup on disk — it assigns IDs and wires editing in the browser).
- `review.html` — Chris's dashboard (reads the same Supabase tables).
- `build-editor.py` — wraps the designed book in the editor layer.
- `editor-config.js` — **blank** Supabase keys → currently **LOCAL mode**. This is the
  one thing left to fill in.
- **Verified**: 49/49 logic tests pass (engine, Supabase request-shaping, dashboard
  diff/ordering) via jsdom on the Windows box. Live in-browser render was NOT tested
  there (sandbox couldn't reach localhost) — doing a real browser smoke test on the
  Mac is worthwhile (see step 4).
- **Not yet deployed.** Nothing is live.

## Files

| File | Role |
|---|---|
| `editor.js` | Engine: ID assignment, contenteditable + change tracking, notes, Supabase/local storage adapter, deep-link jump |
| `editor.css` | Editor UI (top bar, notes drawer / mobile bottom-sheet, edit + note highlights) |
| `editor-config.js` | **Paste Supabase URL + anon key here** (blank = local mode) |
| `review.html` | Chris's read-only dashboard (edits diff + notes feed, search, export) |
| `build-editor.py` | Reads `Built-for-Wonder-DESIGNED.html`, injects the 3 assets, writes an editor HTML file. `--base` sets asset URL prefix, `--out` the filename. |
| `EDITOR-SETUP.md` | Longer-form setup notes (Supabase SQL, deploy) — this handoff supersedes it for the task list |
| `Built-for-Wonder-DESIGNED.html` | The designed book (tracked). Editor is built FROM this. |

---

## Your task list

### Step 1 — Get oriented
```bash
python build-editor.py            # regenerates editor.html (relative asset paths, local preview)
```
Open `editor.html` in a browser. Top bar should say **“Local only”**. Try editing a
paragraph and adding a note to confirm the UX. (This is local mode — that's expected
until Supabase is wired.)

### Step 2 — Supabase (Chris does the web part; you take the keys)
Supabase project creation needs Chris's account, so **ask Chris to do this** and paste
you the two values:

1. Chris: go to https://supabase.com → sign in → **New project** (name `built-for-wonder`,
   any DB password, nearest region).
2. Chris: **SQL Editor → New query →** paste and **Run** the schema in
   `EDITOR-SETUP.md` (section “Create the tables” — two tables `edits` + `notes` with
   open RLS policies). Expect “Success. No rows returned.”
3. Chris: **Settings → API →** copy **Project URL** and the **`anon` `public`** key.
4. Chris pastes both to you. The anon key is **public by design** (it ships in the
   browser) — safe to handle. Write them into `editor-config.js`:
   ```js
   window.EDITOR_CONFIG = {
     supabaseUrl:     "https://xxxx.supabase.co",
     supabaseAnonKey: "eyJhbGci...anon key..."
   };
   ```
> Access control = **keep the `/edit` URL private**. Anyone with the link + anon key
> can read/write only these two tables, nothing else.

### Step 3 — Build the deploy pages (served at `/edit`)
The live site is a **static Netlify site** that serves a folder's `index.html` at its
clean path, so the editor goes in an `edit/` folder. Build with absolute `/edit/`
asset paths so it works with or without a trailing slash:

```bash
# macOS/Linux: no MSYS path-mangling to worry about (that was a Windows-only quirk)
python build-editor.py --base /edit/ --out edit/index.html
cp editor.js editor.css editor-config.js review.html edit/
```
Then confirm the injected tags are absolute:
```bash
grep -oE '(href|src)="/edit/editor[^"]*"' edit/index.html
# → /edit/editor.css, /edit/editor-config.js, /edit/editor.js
```

Add the clean `/review` route. Ensure `_redirects` (at the repo/site root that Netlify
deploys) contains:
```
/review    /edit/review.html   200
```
(Keep any existing redirect lines, e.g. the old `/Architecture-of-Wonder-GATED.html` → `/`.)

### Step 4 — Smoke test in a real browser (recommended)
Serve locally and click through — this is the check the Windows box couldn't do:
```bash
python -m http.server 8080
# open http://127.0.0.1:8080/edit/  → should say "Cloud synced" now
```
Verify: edit a paragraph (reload → edit persists), add a note (appears in drawer),
open `http://127.0.0.1:8080/edit/review.html` → the edit + note show up. If they do,
cloud sync is working.

### Step 5 — Deploy
Netlify builds from **`main`**. Commit the `edit/` folder + `_redirects` to `main` and
push. On this repo `main` == the deployed commit, so it's a clean fast-forward — **no
force-push** (the deploy repo has a sensitive history; never force-push it):
```bash
git checkout main
git pull
# bring the edit/ folder + editor sources + _redirects onto main, then:
git add edit/ _redirects editor.js editor.css editor-config.js review.html build-editor.py
git commit -m "Add online book editor at /edit + review dashboard"
git push origin main
```
Netlify auto-builds. Result:
- **`https://<site>/edit`** → editor (send this to the book editor)
- **`https://<site>/review`** → Chris's dashboard

> ⚠️ `editor-config.js` will contain the (public) anon key once you commit it. That's
> intended — it's a browser key. Do NOT ever commit a Supabase **service_role** key.

---

## How it works (reference)

- On load, `editor.js` assigns each prose block (`p, h1–h4, li, blockquote, figcaption`,
  skipping decoration/symbol-only and non-leaf nodes) a stable
  `data-eid = ${chapterId}~${index}~${textHash}`, makes it `contenteditable`, and
  tracks changes (debounced 650 ms; edited blocks get `.bfw-modified`).
- **Storage** = Supabase REST with a localStorage write-through cache. Two tables:
  `edits` (pk `eid`, upsert via `on_conflict=eid` + `Prefer: resolution=merge-duplicates`)
  and `notes` (identity `id`). If keys are blank → localStorage-only (LOCAL mode).
- The dashboard's “Open in editor” links deep-link to `/edit/#<eid>`; the editor reads
  the hash and scrolls+flashes that block.

## Gotchas / notes

- **Direct edits flatten inline styling in that one block** to plain text — the wording
  is what's preserved (and what shows cleanly in the dashboard). Untouched blocks keep
  their exact design. This is an accepted trade-off, not a bug.
- **Rebuild after any book change:** re-run the `build-editor.py` commands above so
  `edit/index.html` reflects the current `Built-for-Wonder-DESIGNED.html`.
- The `--base /edit/` absolute paths are what make the clean `/edit` URL robust
  regardless of trailing slash — don't switch them back to relative for the deploy build.
- Tests: they were ad-hoc jsdom scripts in a scratch dir on Windows (not committed). If
  you want them, they're easy to recreate, but the feature is already verified.
