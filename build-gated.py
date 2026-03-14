#!/usr/bin/env python3
"""
build-gated.py — Generates a gated ebook HTML for Netlify deployment.

Reads the designed HTML, wraps it with an email/name gate overlay,
replaces the placeholder with a personalized span, removes the editor
note, and outputs to site/index.html.

Run after build-book.py:
    python3 build-gated.py
"""

import os
import re

SOURCE = "Architecture-of-Wonder-DESIGNED.html"
OUTPUT_DIR = "site"
OUTPUT = os.path.join(OUTPUT_DIR, "index.html")

# ── Gate overlay + personalization JS ──────────────────────────────
GATE_CSS = """
/* ═══ GATE OVERLAY ═══ */
#gate-overlay {
  position: fixed; inset: 0; z-index: 10000;
  background: linear-gradient(180deg, #080F1A, #0D1E30);
  display: flex; align-items: center; justify-content: center;
  transition: opacity 0.6s ease;
}
#gate-overlay.fade-out {
  opacity: 0; pointer-events: none;
}
#gate-box {
  text-align: center; max-width: 440px; padding: 50px 40px;
}
#gate-box .gate-author {
  font-family: var(--sans); font-size: .65rem; letter-spacing: 7px;
  color: var(--gray-blue); font-weight: 300; margin-bottom: 12px;
}
#gate-box .gate-title {
  font-family: var(--sans); font-size: 1.8rem; font-weight: 700;
  letter-spacing: 4px; color: var(--gold); line-height: 1.35;
  margin-bottom: 8px;
  text-shadow: 0 0 50px rgba(201,168,76,.12);
}
#gate-box .gate-subtitle {
  font-family: var(--sans); font-size: .6rem; letter-spacing: 3px;
  color: var(--gray-blue); font-weight: 300; line-height: 1.7;
  margin-bottom: 28px;
}
#gate-box .gate-rule {
  width: 140px; height: 1px; margin: 0 auto 28px;
  background: linear-gradient(90deg, transparent, rgba(201,168,76,.35), transparent);
}
#gate-box .gate-desc {
  font-family: var(--serif); font-size: 1rem; color: var(--gray-blue);
  line-height: 1.65; margin-bottom: 30px; font-style: italic;
}
#gate-box form {
  display: flex; flex-direction: column; gap: 14px;
  align-items: center;
}
#gate-box input {
  width: 100%; max-width: 320px; padding: 12px 16px;
  font-family: var(--sans); font-size: .8rem;
  background: rgba(255,255,255,.06); border: 1px solid rgba(201,168,76,.25);
  border-radius: 4px; color: #F5F0E8; letter-spacing: .5px;
  outline: none; transition: border-color 0.3s;
}
#gate-box input::placeholder { color: rgba(138,154,181,.5); }
#gate-box input:focus { border-color: var(--gold); }
#gate-box button {
  width: 100%; max-width: 320px; padding: 14px 24px;
  font-family: var(--sans); font-size: .7rem; font-weight: 700;
  letter-spacing: 3px; text-transform: uppercase;
  background: linear-gradient(135deg, var(--gold), #D4B85C);
  color: var(--navy); border: none; border-radius: 4px;
  cursor: pointer; transition: transform 0.2s, box-shadow 0.2s;
  margin-top: 6px;
}
#gate-box button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 20px rgba(201,168,76,.3);
}
#gate-box .gate-note {
  font-family: var(--sans); font-size: .5rem; letter-spacing: 1px;
  color: var(--dim); margin-top: 16px; line-height: 1.6;
}
#book-content { display: none; }
#book-content.visible { display: block; }
"""

GATE_HTML = """
<div id="gate-overlay">
  <div id="gate-box">
    <div class="gate-author">CHRIS MICHAEL</div>
    <div class="gate-title">THE ARCHITECTURE<br>OF WONDER</div>
    <div class="gate-subtitle">BEHAVIORAL PROFILING &middot; AUDIENCE PSYCHOLOGY &middot; PERFORMANCE CRAFT</div>
    <div class="gate-rule"></div>
    <div class="gate-desc">Read the unreleased draft. Enter your name and email to get access.</div>
    <form id="gate-form">
      <input type="text" id="gate-name" placeholder="First name" required autocomplete="given-name">
      <input type="email" id="gate-email" placeholder="Email address" required autocomplete="email">
      <button type="submit">Read the Draft</button>
    </form>
    <div class="gate-note">Your name personalizes the reading experience.<br>No spam. Just the book.</div>
  </div>
</div>
"""

GATE_JS = """
<script>
(function() {
  var STORAGE_KEY = 'aow_reader';
  var overlay = document.getElementById('gate-overlay');
  var content = document.getElementById('book-content');
  var form = document.getElementById('gate-form');

  function personalize(name) {
    var spans = document.querySelectorAll('.reader-name');
    for (var i = 0; i < spans.length; i++) {
      spans[i].textContent = name;
    }
  }

  function showBook(data) {
    personalize(data.firstName);
    content.classList.add('visible');
    overlay.classList.add('fade-out');
    setTimeout(function() {
      overlay.style.display = 'none';
    }, 600);
  }

  // Check localStorage for returning readers
  var saved = null;
  try { saved = JSON.parse(localStorage.getItem(STORAGE_KEY)); } catch(e) {}

  if (saved && saved.firstName && saved.email) {
    showBook(saved);
  }

  form.addEventListener('submit', function(e) {
    e.preventDefault();
    var firstName = document.getElementById('gate-name').value.trim();
    var email = document.getElementById('gate-email').value.trim();
    if (!firstName || !email) return;

    // Capitalize first letter
    firstName = firstName.charAt(0).toUpperCase() + firstName.slice(1).toLowerCase();

    var data = { firstName: firstName, email: email, ts: new Date().toISOString() };
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(data)); } catch(e) {}
    showBook(data);
  });
})();
</script>
"""


def build():
    if not os.path.exists(SOURCE):
        print(f"ERROR: {SOURCE} not found. Run build-book.py first.")
        return

    with open(SOURCE, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Replace the placeholder with a targetable span
    html = html.replace(
        "*PLACE HOLDER*",
        '<span class="reader-name" style="font-style:italic">Reader</span>'
    )

    # 2. Remove the editor note paragraph
    html = re.sub(
        r"<p>__\*note to the editor:.*?__</p>\n?",
        "",
        html,
        flags=re.DOTALL,
    )

    # 3. Inject gate CSS before closing </style>
    html = html.replace("</style>", GATE_CSS + "\n</style>", 1)

    # 4. Wrap body content: insert gate overlay after <body>, wrap rest in #book-content
    # Find the opening body tag (there's no explicit <body> in the source, content starts after </style>)
    # The HTML structure is: </style>\n</head>\n... then content starts
    # Let's check if there's a <body> tag
    if "<body>" in html:
        html = html.replace("<body>", "<body>\n" + GATE_HTML + '\n<div id="book-content">', 1)
    elif "<body" in html:
        # body with attributes
        body_match = re.search(r"(<body[^>]*>)", html)
        if body_match:
            html = html.replace(
                body_match.group(1),
                body_match.group(1) + "\n" + GATE_HTML + '\n<div id="book-content">',
                1,
            )
    else:
        # No body tag — inject after </head> or after </style>
        html = html.replace(
            "</head>",
            "</head>\n<body>\n" + GATE_HTML + '\n<div id="book-content">',
            1,
        )
        html = html.replace("</html>", "</div>\n" + GATE_JS + "\n</body>\n</html>")

    # Close the #book-content div and add JS before </body>
    if "</body>" in html:
        html = html.replace("</body>", "</div>\n" + GATE_JS + "\n</body>", 1)

    # 5. Write output
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Gated ebook written to {OUTPUT}")
    print(f"  - Placeholder replaced with personalized <span>")
    print(f"  - Editor note removed")
    print(f"  - Gate overlay + localStorage persistence added")
    print(f"  - Ready for Netlify deployment")


if __name__ == "__main__":
    build()
