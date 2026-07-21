/* ============================================================
   Built for Wonder — Editor engine
   Layers a direct-edit + notes workflow on top of the designed
   book. Cloud sync via Supabase REST, with a localStorage
   fallback so the page still works before cloud is configured.
   ============================================================ */
(function () {
  'use strict';

  var CFG = window.EDITOR_CONFIG || {};
  var CLOUD = !!(CFG.supabaseUrl && CFG.supabaseAnonKey);

  // Blocks that become directly editable + note-able. The book's headers and
  // subheaders are mostly <div>/<span> with heading CLASSES (e.g.
  // .sub-header-label, .chapter-number, .nc-title, .section-header) rather than
  // semantic <h*> tags, so the class-based matches below are what let the editor
  // edit and annotate every heading/subheader/label — not just body prose.
  // assignIds() only makes the leaf text block editable, so wrapping containers
  // that merely hold a matching child stay untouched.
  var HEADING_SELECTOR =
    '[class*="-title"],[class*="-head"],[class*="-label"],[class*="-number"],' +
    '.title,.subtitle';
  var EDIT_SELECTOR = 'p,h1,h2,h3,h4,h5,h6,li,blockquote,figcaption,' + HEADING_SELECTOR;
  var LS_EDITS = 'bfw_edits_v1';
  var LS_NOTES = 'bfw_notes_v1';
  var LS_NAME  = 'bfw_editor_name';

  // ---- state ----
  var author = localStorage.getItem(LS_NAME) || '';
  var edits  = {};            // eid -> {eid, chapter, chapter_title, original, edited, edited_html, author, updated_at}
  var notes  = [];            // [{id, node_id, chapter, chapter_title, quote, body, author, created_at}]
  var origText = {};          // eid -> original textContent (trimmed)
  var savingCount = 0;
  var savedRange = null;      // Range captured when the "add note" button is shown

  // =========================================================
  //  Small helpers
  // =========================================================
  function el(tag, attrs, html) {
    var e = document.createElement(tag);
    if (attrs) for (var k in attrs) {
      if (k === 'class') e.className = attrs[k];
      else e.setAttribute(k, attrs[k]);
    }
    if (html != null) e.innerHTML = html;
    return e;
  }
  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
  function norm(s) { return String(s || '').replace(/\s+/g, ' ').trim(); }
  function hash(s) {
    var h = 5381, i = s.length;
    while (i) h = (h * 33) ^ s.charCodeAt(--i);
    return (h >>> 0).toString(36);
  }
  function nowISO() { return new Date().toISOString(); }
  function uid() { return Date.now().toString(36) + Math.random().toString(36).slice(2, 8); }
  function debounce(fn, ms) {
    var t; return function () { var a = arguments, c = this; clearTimeout(t); t = setTimeout(function () { fn.apply(c, a); }, ms); };
  }
  function toast(msg) {
    var t = document.getElementById('bfw-toast');
    t.textContent = msg; t.classList.add('show');
    clearTimeout(toast._t); toast._t = setTimeout(function () { t.classList.remove('show'); }, 2200);
  }

  function chapterInfo(node) {
    var sec = node.closest('section[id], article[id], [id^="chapter-"]');
    // prefer an ancestor chapter section
    var chap = node.closest('[id^="chapter-"]') || sec;
    var id = chap ? chap.id : '';
    var title = '';
    if (chap) {
      var h = chap.querySelector('h1, h2, .chapter-title, .chapter-number');
      if (h) title = norm(h.textContent).slice(0, 80);
    }
    return { chapter: id || '', title: title };
  }

  // =========================================================
  //  Status pill
  // =========================================================
  function setStatus(state, text) {
    var s = document.getElementById('bfw-status');
    if (!s) return;
    s.setAttribute('data-state', state);
    s.querySelector('.bfw-status-text').textContent = text;
  }
  function refreshStatus() {
    if (savingCount > 0) { setStatus('saving', 'Saving…'); return; }
    if (CLOUD) setStatus('saved', 'Cloud synced');
    else setStatus('local', 'Local only');
  }

  // =========================================================
  //  Storage adapter (cloud + local, write-through)
  // =========================================================
  function lsGet(k, d) { try { return JSON.parse(localStorage.getItem(k)) || d; } catch (e) { return d; } }
  function lsSet(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }

  var Cloud = {
    base: CLOUD ? CFG.supabaseUrl.replace(/\/+$/, '') : '',
    hdr: function (extra) {
      var h = { apikey: CFG.supabaseAnonKey, Authorization: 'Bearer ' + CFG.supabaseAnonKey, 'Content-Type': 'application/json' };
      if (extra) for (var k in extra) h[k] = extra[k];
      return h;
    },
    req: function (method, path, body, extraHeaders) {
      return fetch(this.base + '/rest/v1/' + path, {
        method: method, headers: this.hdr(extraHeaders),
        body: body ? JSON.stringify(body) : undefined
      }).then(function (r) {
        if (!r.ok) return r.text().then(function (t) { throw new Error(method + ' ' + path + ' → ' + r.status + ' ' + t); });
        return r.text().then(function (t) { return t ? JSON.parse(t) : null; });
      });
    },
    upsertEdit: function (rec) { return this.req('POST', 'edits?on_conflict=eid', [rec], { Prefer: 'resolution=merge-duplicates,return=minimal' }); },
    deleteEdit: function (eid) { return this.req('DELETE', 'edits?eid=eq.' + encodeURIComponent(eid)); },
    listEdits: function () { return this.req('GET', 'edits?select=*'); },
    addNote: function (n) { return this.req('POST', 'notes', [n], { Prefer: 'return=representation' }).then(function (rows) { return rows && rows[0]; }); },
    deleteNote: function (id) { return this.req('DELETE', 'notes?id=eq.' + encodeURIComponent(id)); },
    listNotes: function () { return this.req('GET', 'notes?select=*&order=created_at.asc'); }
  };

  function track(promise) {
    savingCount++; refreshStatus();
    return promise.then(function (v) { savingCount--; refreshStatus(); return v; })
      .catch(function (err) {
        savingCount--; console.error('[bfw] sync error', err);
        setStatus('error', 'Sync error — saved locally');
        return null;
      });
  }

  var Store = {
    saveEdit: function (rec) {
      edits[rec.eid] = rec;
      lsSet(LS_EDITS, edits);
      if (CLOUD) return track(Cloud.upsertEdit(rec));
      return Promise.resolve();
    },
    removeEdit: function (eid) {
      delete edits[eid];
      lsSet(LS_EDITS, edits);
      if (CLOUD) return track(Cloud.deleteEdit(eid));
      return Promise.resolve();
    },
    addNote: function (n) {
      // optimistic local
      notes.push(n); lsSet(LS_NOTES, notes);
      if (CLOUD) {
        var payload = { node_id: n.node_id, chapter: n.chapter, chapter_title: n.chapter_title, quote: n.quote, body: n.body, author: n.author, created_at: n.created_at };
        return track(Cloud.addNote(payload)).then(function (row) {
          if (row && row.id != null) { n.id = row.id; lsSet(LS_NOTES, notes); }
          return n;
        });
      }
      return Promise.resolve(n);
    },
    removeNote: function (n) {
      notes = notes.filter(function (x) { return x !== n; });
      lsSet(LS_NOTES, notes);
      if (CLOUD && n.id != null && String(n.id).indexOf('local-') !== 0) return track(Cloud.deleteNote(n.id));
      return Promise.resolve();
    },
    load: function () {
      // local first for instant paint
      edits = lsGet(LS_EDITS, {});
      notes = lsGet(LS_NOTES, []);
      if (!CLOUD) return Promise.resolve();
      return Promise.all([Cloud.listEdits(), Cloud.listNotes()]).then(function (res) {
        var e = {}; (res[0] || []).forEach(function (r) { e[r.eid] = r; });
        edits = e; lsSet(LS_EDITS, edits);
        notes = (res[1] || []); lsSet(LS_NOTES, notes);
      }).catch(function (err) {
        console.error('[bfw] load error, using local cache', err);
        setStatus('error', 'Offline — local cache');
      });
    }
  };

  // =========================================================
  //  Assign stable ids + make prose editable
  // =========================================================
  function assignIds() {
    var scopeCount = {};
    var nodes = document.querySelectorAll(EDIT_SELECTOR);
    nodes.forEach(function (node) {
      if (node.closest('[data-bfw-ui]')) return;               // skip our own UI
      if (node.closest('nav, a')) return;                      // skip TOC / nav links (keep them clickable)
      if (node.hasAttribute('data-eid')) return;
      if (node.querySelector(EDIT_SELECTOR)) return;            // only leaf text blocks (e.g. <li> holding <p>)
      var txt = norm(node.textContent);
      if (!txt || !/[A-Za-z0-9]/.test(txt)) return;             // skip symbol/decoration rows
      var info = chapterInfo(node);
      var scope = info.chapter || 'doc';
      scopeCount[scope] = (scopeCount[scope] || 0) + 1;
      var eid = scope + '~' + scopeCount[scope] + '~' + hash(txt.slice(0, 160));
      node.setAttribute('data-eid', eid);
      node.setAttribute('contenteditable', 'true');
      node.setAttribute('spellcheck', 'true');
      node.classList.add('bfw-editable');
      origText[eid] = node.textContent.trim();
      node._bfwChapter = info;
    });
  }

  function nodeByEid(eid) { return document.querySelector('[data-eid="' + (window.CSS && CSS.escape ? CSS.escape(eid) : eid.replace(/"/g, '\\"')) + '"]'); }

  // Apply stored edits + note highlights to the DOM
  function applyStored() {
    Object.keys(edits).forEach(function (eid) {
      var rec = edits[eid]; var node = nodeByEid(eid);
      if (!node) return;
      if (rec.edited_html != null && rec.edited_html !== node.innerHTML) node.innerHTML = rec.edited_html;
      else if (rec.edited != null && rec.edited !== node.textContent.trim()) node.textContent = rec.edited;
      if ((origText[eid] || '') !== node.textContent.trim()) node.classList.add('bfw-modified');
    });
    notes.forEach(function (n) { rehighlight(n); });
  }

  // Wrap the first occurrence of a note's quote inside its node (best-effort, cross-device)
  function rehighlight(n) {
    if (!n.quote) return;
    var node = nodeByEid(n.node_id);
    if (!node) return;
    if (node.querySelector('.bfw-note-anchor[data-note-id="' + n.id + '"]')) return;
    var walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT, null);
    var q = n.quote.trim(); if (!q) return;
    var tn;
    while ((tn = walker.nextNode())) {
      var idx = tn.nodeValue.indexOf(q);
      if (idx !== -1) {
        try {
          var r = document.createRange();
          r.setStart(tn, idx); r.setEnd(tn, idx + q.length);
          var span = el('span', { 'class': 'bfw-note-anchor', 'data-note-id': n.id });
          r.surroundContents(span);
        } catch (e) { /* quote spans markup; leave un-highlighted */ }
        return;
      }
    }
  }

  // =========================================================
  //  Change tracking (delegated)
  // =========================================================
  var pendingSave = {};
  function commitEdit(node) {
    var eid = node.getAttribute('data-eid'); if (!eid) return;
    var cur = node.textContent.trim();
    var orig = origText[eid] || '';
    if (cur === orig) {
      node.classList.remove('bfw-modified');
      if (edits[eid]) Store.removeEdit(eid);
      return;
    }
    node.classList.add('bfw-modified');
    var info = node._bfwChapter || chapterInfo(node);
    Store.saveEdit({
      eid: eid, chapter: info.chapter, chapter_title: info.title,
      original: orig, edited: cur, edited_html: node.innerHTML,
      author: author || 'editor', updated_at: nowISO()
    });
  }
  var onInput = function (e) {
    var node = e.target.closest && e.target.closest('[data-eid]');
    if (!node) return;
    var eid = node.getAttribute('data-eid');
    if (!pendingSave[eid]) pendingSave[eid] = debounce(function () { commitEdit(node); }, 650);
    node.classList.add('bfw-modified'); // instant feedback; commit reconciles
    pendingSave[eid]();
  };

  // Force plain-text paste so we don't inherit foreign styles
  function onPaste(e) {
    var node = e.target.closest && e.target.closest('[data-eid]');
    if (!node) return;
    e.preventDefault();
    var text = (e.clipboardData || window.clipboardData).getData('text');
    document.execCommand('insertText', false, text);
  }

  // =========================================================
  //  Notes: selection → add-note button → composer
  // =========================================================
  function inContent(nodeOrSel) {
    var n = nodeOrSel; if (n && n.nodeType === 3) n = n.parentElement;
    return n && n.closest && n.closest('[data-eid]') && !n.closest('[data-bfw-ui]');
  }

  var onSelectionChange = debounce(function () {
    if (document.body.classList.contains('bfw-reading')) return;
    var sel = window.getSelection();
    var btn = document.getElementById('bfw-addnote');
    if (!sel || sel.isCollapsed || !sel.rangeCount) { btn.style.display = 'none'; return; }
    var range = sel.getRangeAt(0);
    var text = norm(sel.toString());
    if (text.length < 2 || !inContent(range.startContainer)) { btn.style.display = 'none'; return; }
    var rect = range.getBoundingClientRect();
    if (!rect || (!rect.width && !rect.height)) { btn.style.display = 'none'; return; }
    savedRange = range.cloneRange();
    btn.style.display = 'block';
    btn.style.left = (rect.left + rect.width / 2) + 'px';
    btn.style.top = Math.max(rect.top - 8, 46) + 'px';
  }, 120);

  function openComposer() {
    if (!savedRange) return;
    var text = norm(savedRange.toString());
    if (!text) return;
    var anchorEl = savedRange.startContainer.nodeType === 3 ? savedRange.startContainer.parentElement : savedRange.startContainer;
    var host = anchorEl.closest('[data-eid]');
    var info = host ? (host._bfwChapter || chapterInfo(host)) : { chapter: '', title: '' };
    var comp = document.getElementById('bfw-composer');
    comp._ctx = { quote: text, node_id: host ? host.getAttribute('data-eid') : '', chapter: info.chapter, title: info.title };
    comp.querySelector('.bfw-quote').textContent = '“' + (text.length > 240 ? text.slice(0, 240) + '…' : text) + '”';
    comp.querySelector('textarea').value = '';
    comp.style.display = 'block';
    document.getElementById('bfw-addnote').style.display = 'none';
    setTimeout(function () { comp.querySelector('textarea').focus(); }, 30);
  }

  function saveComposer() {
    var comp = document.getElementById('bfw-composer');
    var ctx = comp._ctx; if (!ctx) return;
    var body = comp.querySelector('textarea').value.trim();
    if (!body) { toast('Add a note first'); return; }
    ensureName(function () {
      var n = {
        id: 'local-' + uid(), node_id: ctx.node_id, chapter: ctx.chapter, chapter_title: ctx.title,
        quote: ctx.quote, body: body, author: author, created_at: nowISO()
      };
      Store.addNote(n).then(function () { rehighlight(n); renderNotes(); });
      comp.style.display = 'none';
      window.getSelection().removeAllRanges();
      toast('Note added');
      renderNotes();
    });
  }

  // =========================================================
  //  Notes drawer
  // =========================================================
  function openDrawer(open) {
    var d = document.getElementById('bfw-drawer');
    var bd = document.getElementById('bfw-backdrop');
    if (open) { d.classList.add('open'); bd.classList.add('show'); renderNotes(); }
    else { d.classList.remove('open'); bd.classList.remove('show'); }
  }
  function updateCount() {
    var c = document.getElementById('bfw-notes-count');
    if (c) { c.textContent = notes.length; c.style.display = notes.length ? '' : 'none'; }
  }
  function renderNotes() {
    updateCount();
    var body = document.getElementById('bfw-drawer-body');
    if (!body) return;
    var sorted = notes.slice().sort(function (a, b) { return (a.created_at || '').localeCompare(b.created_at || ''); });
    if (!sorted.length) {
      body.innerHTML = '<div class="bfw-empty">No notes yet.<br>Select any text in the book, then tap <b>＋ Note</b> to leave a comment. Notes appear here in the order you add them.</div>';
      return;
    }
    body.innerHTML = '';
    sorted.forEach(function (n, i) {
      var when = '';
      try { when = new Date(n.created_at).toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }); } catch (e) {}
      var card = el('div', { 'class': 'bfw-note-card' });
      card.innerHTML =
        '<div class="bfw-note-meta"><span class="bfw-idx">#' + (i + 1) + '</span>' +
        (n.chapter_title ? '<span>' + esc(n.chapter_title) + '</span>' : '') +
        '<span style="margin-left:auto">' + esc(n.author || '') + (when ? ' · ' + esc(when) : '') + '</span></div>' +
        (n.quote ? '<div class="bfw-note-quote">“' + esc(n.quote) + '”</div>' : '') +
        '<div class="bfw-note-body">' + esc(n.body) + '</div>' +
        '<div class="bfw-note-actions"><button data-jump="1">Jump to text ↦</button>' +
        '<button class="bfw-del" data-del="1">Delete</button></div>';
      card.querySelector('[data-jump]').onclick = function () { jumpTo(n); };
      card.querySelector('[data-del]').onclick = function () {
        if (!confirm('Delete this note?')) return;
        Store.removeNote(n).then(function () {
          var sp = document.querySelector('.bfw-note-anchor[data-note-id="' + n.id + '"]');
          if (sp) { var p = sp.parentNode; while (sp.firstChild) p.insertBefore(sp.firstChild, sp); p.removeChild(sp); }
          renderNotes();
        });
      };
      body.appendChild(card);
    });
  }
  function jumpTo(n) {
    var target = document.querySelector('.bfw-note-anchor[data-note-id="' + n.id + '"]') || nodeByEid(n.node_id);
    if (!target) { toast('Passage not found on this page'); return; }
    if (window.innerWidth <= 640) openDrawer(false);
    flashTo(target);
  }
  function flashTo(target) {
    if (!target) return;
    target.classList.add('bfw-flash');
    setTimeout(function () { target.classList.remove('bfw-flash'); }, 1300);
    if (target.scrollIntoView) { try { target.scrollIntoView({ behavior: 'smooth', block: 'center' }); } catch (e) {} }
  }
  // Deep-link: /edit/#<eid> (used by the review dashboard's "Open in editor")
  function handleHash() {
    var h = decodeURIComponent((location.hash || '').replace(/^#/, ''));
    if (!h) return;
    var node = nodeByEid(h);
    if (node) setTimeout(function () { flashTo(node); }, 350);
  }

  // =========================================================
  //  Reading mode
  // =========================================================
  function setReading(on) {
    document.body.classList.toggle('bfw-reading', on);
    document.body.classList.toggle('bfw-editing', !on);
    document.querySelectorAll('[data-eid]').forEach(function (nd) {
      nd.setAttribute('contenteditable', on ? 'false' : 'true');
    });
    var b = document.getElementById('bfw-read-btn');
    if (b) b.querySelector('.bfw-btn-label').textContent = on ? 'Edit mode' : 'Reading mode';
    document.getElementById('bfw-addnote').style.display = 'none';
  }

  // =========================================================
  //  Identity modal
  // =========================================================
  function ensureName(cb) {
    if (author) { cb && cb(); return; }
    showModal(function () { cb && cb(); });
  }
  function showModal(afterSave) {
    var m = document.getElementById('bfw-modal');
    var input = m.querySelector('input');
    input.value = author || '';
    m.classList.add('show');
    setTimeout(function () { input.focus(); }, 40);
    m._after = afterSave;
  }

  // Instructions popup — reopenable any time via the "?" button
  function openHelp(open) {
    var h = document.getElementById('bfw-help');
    if (!h) return;
    h.classList.toggle('show', open !== false);
  }

  // =========================================================
  //  Build the editor UI
  // =========================================================
  function buildUI() {
    var bar = el('div', { id: 'bfw-bar', 'data-bfw-ui': '1' });
    bar.innerHTML =
      '<div class="bfw-brand">EDITOR MODE<small>Built for Wonder</small></div>' +
      '<div id="bfw-status" data-state="local"><span class="dot"></span><span class="bfw-status-text">Local only</span></div>' +
      '<div class="bfw-spacer"></div>' +
      '<button class="bfw-btn" id="bfw-name-btn"><span>👤</span><span class="bfw-btn-label">Your name</span></button>' +
      '<button class="bfw-btn" id="bfw-read-btn"><span>📖</span><span class="bfw-btn-label">Reading mode</span></button>' +
      '<button class="bfw-btn" id="bfw-help-btn" title="How this works"><span>?</span></button>' +
      '<button class="bfw-btn bfw-primary" id="bfw-notes-btn"><span>🗒</span><span class="bfw-btn-label">Notes</span>' +
        '<span class="bfw-count" id="bfw-notes-count" style="display:none">0</span></button>';
    document.body.appendChild(bar);

    var addnote = el('button', { id: 'bfw-addnote', 'data-bfw-ui': '1' }, '＋ Note');
    document.body.appendChild(addnote);

    var comp = el('div', { id: 'bfw-composer', 'data-bfw-ui': '1' });
    comp.innerHTML =
      '<h4>Add a note</h4>' +
      '<div class="bfw-quote"></div>' +
      '<textarea placeholder="What should the author know about this passage?"></textarea>' +
      '<div class="bfw-composer-actions">' +
        '<button class="bfw-btn" id="bfw-comp-cancel">Cancel</button>' +
        '<button class="bfw-btn bfw-primary" id="bfw-comp-save">Save note</button>' +
      '</div>';
    document.body.appendChild(comp);

    var backdrop = el('div', { id: 'bfw-backdrop', 'data-bfw-ui': '1' });
    document.body.appendChild(backdrop);

    var drawer = el('div', { id: 'bfw-drawer', 'data-bfw-ui': '1' });
    drawer.innerHTML =
      '<div class="bfw-drawer-head"><h3>Notes</h3>' +
      '<button class="bfw-btn" id="bfw-drawer-close">Close ✕</button></div>' +
      '<div class="bfw-drawer-body" id="bfw-drawer-body"></div>';
    document.body.appendChild(drawer);

    var modal = el('div', { id: 'bfw-modal', 'data-bfw-ui': '1' });
    modal.innerHTML =
      '<div class="bfw-modal-card">' +
      '<h2>Welcome, editor 👋</h2>' +
      '<p>This is a live, editable copy of <b>Built for Wonder</b>. Two things you can do:</p>' +
      '<ul>' +
      '<li><b>Edit the text directly</b> — click into any paragraph and type. Changed blocks are highlighted and saved automatically.</li>' +
      '<li><b>Leave notes</b> — select any passage, tap <b>＋ Note</b>, and write a comment. All notes collect in the Notes panel in the order you add them.</li>' +
      '</ul>' +
      '<p>First, what name should your edits and notes be signed with?</p>' +
      '<input type="text" id="bfw-name-input" placeholder="e.g. Sarah (editor)" autocomplete="name">' +
      '<div class="bfw-modal-actions"><button class="bfw-btn bfw-primary" id="bfw-name-save">Start editing</button></div>' +
      '</div>';
    document.body.appendChild(modal);

    var help = el('div', { id: 'bfw-help', 'data-bfw-ui': '1' });
    help.innerHTML =
      '<div class="bfw-modal-card">' +
      '<button class="bfw-help-x" id="bfw-help-x" aria-label="Close">✕</button>' +
      '<h2>How to edit this book</h2>' +
      '<p>This is a live, editable copy of <b>Built for Wonder</b>. Everything you do saves automatically.</p>' +
      '<ul>' +
      '<li><b>Edit any text</b> — click into any paragraph, <b>heading, subheader</b>, list item, or caption and just type. Changed blocks turn blue and are marked “edited.”</li>' +
      '<li><b>Leave a note</b> — select any text (headings and subheaders included), then tap the <b>＋ Note</b> button that pops up. Write your comment and Save. The passage gets highlighted.</li>' +
      '<li><b>See every note</b> — open the <b>🗒 Notes</b> panel (top right). Jump straight to any passage or delete a note.</li>' +
      '<li><b>Reading mode</b> — tap <b>📖 Reading mode</b> to turn editing off and just read; tap again to edit.</li>' +
      '<li><b>Your name</b> — tap <b>👤</b> to set or change the name your edits and notes are signed with.</li>' +
      '</ul>' +
      '<p>Reopen these instructions any time with the <b>?</b> button up top.</p>' +
      '<div class="bfw-modal-actions"><button class="bfw-btn bfw-primary" id="bfw-help-close">Got it</button></div>' +
      '</div>';
    document.body.appendChild(help);

    var t = el('div', { id: 'bfw-toast', 'data-bfw-ui': '1' });
    document.body.appendChild(t);

    // ---- wire events ----
    addnote.addEventListener('mousedown', function (e) { e.preventDefault(); });
    addnote.addEventListener('click', openComposer);
    comp.querySelector('#bfw-comp-cancel').onclick = function () { comp.style.display = 'none'; };
    comp.querySelector('#bfw-comp-save').onclick = saveComposer;

    document.getElementById('bfw-notes-btn').onclick = function () { openDrawer(!drawer.classList.contains('open')); };
    document.getElementById('bfw-drawer-close').onclick = function () { openDrawer(false); };
    backdrop.onclick = function () { openDrawer(false); };
    document.getElementById('bfw-read-btn').onclick = function () { setReading(!document.body.classList.contains('bfw-reading')); };
    document.getElementById('bfw-name-btn').onclick = function () { showModal(); };
    document.getElementById('bfw-help-btn').onclick = function () { openHelp(true); };
    help.querySelector('#bfw-help-close').onclick = function () { openHelp(false); };
    help.querySelector('#bfw-help-x').onclick = function () { openHelp(false); };
    help.addEventListener('click', function (e) { if (e.target === help) openHelp(false); });

    modal.querySelector('#bfw-name-save').onclick = function () {
      var v = modal.querySelector('input').value.trim();
      if (!v) { modal.querySelector('input').focus(); return; }
      author = v; localStorage.setItem(LS_NAME, author);
      modal.classList.remove('show');
      var after = modal._after; modal._after = null; if (after) after();
    };
    modal.querySelector('input').addEventListener('keydown', function (e) { if (e.key === 'Enter') modal.querySelector('#bfw-name-save').click(); });

    // global listeners (delegated)
    document.addEventListener('input', onInput, true);
    document.addEventListener('paste', onPaste, true);
    document.addEventListener('selectionchange', onSelectionChange);
    window.addEventListener('scroll', function () { document.getElementById('bfw-addnote').style.display = 'none'; }, { passive: true });
    document.getElementById('bfw-status').onclick = function () { if (CLOUD) refresh(); };
  }

  // Periodic pull so a second device sees new notes/edits (skips the block being edited)
  function refresh() {
    if (!CLOUD) return;
    Store.load().then(function () {
      var active = document.activeElement;
      Object.keys(edits).forEach(function (eid) {
        var node = nodeByEid(eid); if (!node || node === active) return;
        var rec = edits[eid];
        if (rec.edited_html != null && rec.edited_html !== node.innerHTML) node.innerHTML = rec.edited_html;
        if ((origText[eid] || '') !== node.textContent.trim()) node.classList.add('bfw-modified');
      });
      renderNotes();
    });
  }

  // =========================================================
  //  Boot
  // =========================================================
  function boot() {
    document.body.classList.add('bfw-editor-on', 'bfw-editing');
    buildUI();
    assignIds();
    refreshStatus();
    Store.load().then(function () {
      applyStored();
      renderNotes();
      handleHash();
      if (!author) showModal();
    });
    window.addEventListener('hashchange', handleHash);
    if (CLOUD) setInterval(refresh, 60000);
    console.log('[bfw] editor ready — ' + (CLOUD ? 'cloud sync ON' : 'LOCAL mode (configure editor-config.js for cloud)') + ', ' + document.querySelectorAll('[data-eid]').length + ' editable blocks');
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
