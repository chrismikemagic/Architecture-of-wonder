# Built for Wonder — Editor page setup

A private, editable copy of the designed book (images + SVGs intact) that your
editor can open on **phone or laptop**. They can:

- **Edit the text directly** — click any paragraph, type; changed blocks are
  highlighted and auto-saved.
- **Leave notes** — select a passage → tap **＋ Note** → comment. All notes
  collect in a Notes panel **in the order they were added**, and you review them
  in a dashboard.

## Files

| File | What it is |
|---|---|
| `editor.html` | The book + editing layer (built by `build-editor.py`) |
| `editor.js` / `editor.css` | The editing engine + styles |
| `editor-config.js` | Where you paste your Supabase keys (cloud sync) |
| `review.html` | **Your** dashboard — all edits + all notes, read-only |
| `build-editor.py` | Rebuilds `editor.html` from the designed book |

## Build the editor page

```bash
cd /c/Users/Chris/Architecture-of-wonder
python build-editor.py
```

This reads `Built-for-Wonder-DESIGNED.html` and writes `editor.html` with the
editor layer injected. Re-run it whenever the book source changes.

---

## Turn on cloud sync (Supabase — free, ~5 min)

Without this, the editor still works but edits/notes stay in one browser (LOCAL
mode). Cloud sync is what lets your editor work across devices and lets **you**
see their edits.

### 1. Create the project
1. Go to <https://supabase.com> → sign in → **New project**.
2. Name it (e.g. `built-for-wonder`), set a DB password, pick a region, create.

### 2. Create the tables
Open **SQL Editor** → **New query**, paste this, click **Run**:

```sql
create table if not exists edits (
  eid           text primary key,
  chapter       text,
  chapter_title text,
  original      text,
  edited        text,
  edited_html   text,
  author        text,
  updated_at    timestamptz default now()
);

create table if not exists notes (
  id            bigint generated always as identity primary key,
  node_id       text,
  chapter       text,
  chapter_title text,
  quote         text,
  body          text,
  author        text,
  created_at    timestamptz default now()
);

-- Row Level Security ON, with open policies.
-- Access is gated by keeping the editor URL private (share it only with people
-- you want editing). Anyone with the link + anon key can read/write these two
-- tables — and nothing else in your project.
alter table edits enable row level security;
alter table notes enable row level security;

create policy "edits read"   on edits for select using (true);
create policy "edits write"  on edits for insert with check (true);
create policy "edits update" on edits for update using (true) with check (true);
create policy "edits delete" on edits for delete using (true);

create policy "notes read"   on notes for select using (true);
create policy "notes write"  on notes for insert with check (true);
create policy "notes delete" on notes for delete using (true);
```

### 3. Get your keys
**Settings → API**, copy:
- **Project URL** → `https://xxxx.supabase.co`
- **anon public** key (the long one labelled *anon* / *public*)

### 4. Paste them into `editor-config.js`
```js
window.EDITOR_CONFIG = {
  supabaseUrl:     "https://xxxx.supabase.co",
  supabaseAnonKey: "eyJhbGciOi...your anon key..."
};
```

That's it. Reload `editor.html` — the top bar should read **Cloud synced**.

---

## Deploy (goes live on your Netlify site)

Copy the editor files into the deploy repo alongside `index.html`:

```bash
cd /c/Users/Chris/Architecture-of-wonder
cp editor.html editor.js editor.css editor-config.js review.html \
   /c/Users/Chris/Architecture-of-wonder-v2/
cd /c/Users/Chris/Architecture-of-wonder-v2
git add editor.html editor.js editor.css editor-config.js review.html
git commit -m "Add editor + review pages"
git push
```

After Netlify deploys:
- **Editor link (send to your editor):** `https://<your-site>/editor.html`
- **Your dashboard:** `https://<your-site>/review.html`

> Keep the editor link private — it *is* the access control.

## A note on direct edits

When a paragraph is edited, its rich inline styling in that one block may be
simplified to plain text (the wording is what's preserved and what shows in your
dashboard). Everything untouched stays exactly as designed.
