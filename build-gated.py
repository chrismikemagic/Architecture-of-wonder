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
OUTPUT = "Architecture-of-Wonder-GATED.html"

# ── Gate overlay + personalization JS ──────────────────────────────
GATE_CSS = """
/* ═══ GATE OVERLAY ═══ */
#gate-overlay {
  position: fixed; inset: 0; z-index: 10000;
  background: rgba(8, 15, 26, .82);
  backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px);
  display: flex; align-items: center; justify-content: center;
  transition: opacity 0.6s ease;
}
#gate-overlay.fade-out {
  opacity: 0; pointer-events: none;
}

/* ═══ PULSE & ZOOM ANIMATION ═══ */
#name-reveal {
  position: absolute; inset: 0;
  display: flex; align-items: center; justify-content: center;
  flex-direction: column; gap: 20px;
  opacity: 0; z-index: 2;
  pointer-events: none;
}
#name-reveal.active { opacity: 1; pointer-events: auto; }
#name-reveal .reveal-logo {
  width: 260px; max-width: 70vw; height: auto;
  filter: drop-shadow(0 4px 24px rgba(0,0,0,.55))
          drop-shadow(0 0 80px rgba(201,168,76,.12));
  transform: scale(0.8);
  animation: none;
}
#name-reveal .reveal-tagline {
  font-family: var(--serif); font-size: 1rem;
  color: rgba(245,240,232,.5); font-style: italic;
  letter-spacing: 1px; opacity: 0;
}

@keyframes pulseIn {
  0% { transform: scale(0.8); opacity: 0; }
  40% { transform: scale(1.08); opacity: 1; }
  55% { transform: scale(0.97); }
  70% { transform: scale(1.03); }
  100% { transform: scale(1); opacity: 1; }
}
@keyframes tagFade {
  0% { opacity: 0; transform: translateY(8px); }
  100% { opacity: 1; transform: translateY(0); }
}
@keyframes zoomThrough {
  0% { transform: scale(1); opacity: 1; }
  100% { transform: scale(12); opacity: 0; }
}
#gate-box {
  position: relative;
  text-align: center; max-width: 460px; width: 90%;
  padding: 52px 44px 42px;
  background: linear-gradient(165deg, rgba(13,30,48,.92), rgba(8,15,26,.96));
  border: 1px solid rgba(201,168,76,.18);
  border-radius: 6px;
  box-shadow:
    0 0 0 1px rgba(201,168,76,.06),
    0 24px 80px rgba(0,0,0,.55),
    0 0 120px rgba(201,168,76,.04);
}
#gate-box::before {
  content: ''; position: absolute; inset: -1px;
  border-radius: 7px; pointer-events: none;
  background: linear-gradient(180deg, rgba(201,168,76,.12), transparent 40%, transparent 60%, rgba(201,168,76,.06));
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor; mask-composite: exclude;
  padding: 1px;
}
#gate-box .gate-author {
  font-family: var(--sans); font-size: .6rem; letter-spacing: 7px;
  color: var(--gray-blue); font-weight: 300; margin-bottom: 14px;
}
#gate-box .gate-title {
  font-family: var(--sans); font-size: 1.6rem; font-weight: 700;
  letter-spacing: 4px; color: var(--gold); line-height: 1.35;
  margin-bottom: 8px;
  text-shadow: 0 0 40px rgba(201,168,76,.1);
}
#gate-box .gate-subtitle {
  font-family: var(--sans); font-size: .52rem; letter-spacing: 3px;
  color: var(--gray-blue); font-weight: 300; line-height: 1.7;
  margin-bottom: 24px;
}
#gate-box .gate-rule {
  width: 120px; height: 1px; margin: 0 auto 24px;
  background: linear-gradient(90deg, transparent, rgba(201,168,76,.3), transparent);
}
#gate-box .gate-desc {
  font-family: var(--serif); font-size: .95rem; color: rgba(245,240,232,.7);
  line-height: 1.65; margin-bottom: 28px; font-style: italic;
}
#gate-box form {
  display: flex; flex-direction: column; gap: 12px;
  align-items: center;
}
#gate-box input {
  width: 100%; max-width: 300px; padding: 11px 16px;
  font-family: var(--sans); font-size: .78rem;
  background: rgba(255,255,255,.04); border: 1px solid rgba(201,168,76,.2);
  border-radius: 3px; color: #F5F0E8; letter-spacing: .5px;
  outline: none; transition: border-color 0.3s, background 0.3s;
}
#gate-box input::placeholder { color: rgba(138,154,181,.4); }
#gate-box input:focus {
  border-color: rgba(201,168,76,.5);
  background: rgba(255,255,255,.06);
}
#gate-box button {
  width: 100%; max-width: 300px; padding: 13px 24px;
  font-family: var(--sans); font-size: .65rem; font-weight: 700;
  letter-spacing: 3px; text-transform: uppercase;
  background: linear-gradient(135deg, var(--gold), #D4B85C);
  color: var(--navy); border: none; border-radius: 3px;
  cursor: pointer; transition: transform 0.2s, box-shadow 0.2s;
  margin-top: 4px;
}
#gate-box button:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 24px rgba(201,168,76,.25);
}
#gate-box .gate-note {
  font-family: var(--sans); font-size: .46rem; letter-spacing: 1px;
  color: rgba(58,74,92,.8); margin-top: 18px; line-height: 1.7;
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
    <form id="gate-form" name="readers" method="POST" data-netlify="true">
      <input type="text" id="gate-name" name="name" placeholder="First name" required autocomplete="given-name">
      <input type="email" id="gate-email" name="email" placeholder="Email address" required autocomplete="email">
      <button type="submit">Read the Draft</button>
    </form>

  </div>
  <div id="name-reveal">
    <img class="reveal-logo" id="reveal-logo" src="https://i.postimg.cc/Ghr5HTTC/w1000-n22219Jlqy-T2z-Qo-E.png" alt="Vanishing Inc">
    <div class="reveal-tagline">presents</div>
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

    var box = document.getElementById('gate-box');
    var nameReveal = document.getElementById('name-reveal');
    var revealLogo = document.getElementById('reveal-logo');

    var boxVisible = box.style.display !== 'none';

    function startReveal() {
      box.style.display = 'none';

      // Phase 2: Logo appears with pulse
      nameReveal.classList.add('active');
      revealLogo.style.animation = 'pulseIn 0.8s cubic-bezier(.22,.68,.36,1.2) forwards';

      // Phase 3: Tagline fades in
      setTimeout(function() {
        nameReveal.querySelector('.reveal-tagline').style.animation = 'tagFade 0.5s ease forwards';
      }, 600);

      // Phase 4: Zoom through
      setTimeout(function() {
        content.classList.add('visible');
        overlay.style.animation = 'zoomThrough 0.7s cubic-bezier(.4,0,.2,1) forwards';
        setTimeout(function() {
          overlay.style.display = 'none';
        }, 700);
      }, 1800);
    }

    if (boxVisible) {
      // Phase 1: Fade out the form box first
      box.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      box.style.opacity = '0';
      box.style.transform = 'scale(0.95)';
      setTimeout(startReveal, 450);
    } else {
      // Box already hidden (returning reader) — go straight to reveal
      startReveal();
    }
  }

  // Check localStorage for returning readers
  var saved = null;
  try { saved = JSON.parse(localStorage.getItem(STORAGE_KEY)); } catch(e) {}

  if (saved && saved.firstName && saved.email) {
    // Hide the form box immediately, then play the animation
    document.getElementById('gate-box').style.display = 'none';
    showBook(saved);
  }

  form.addEventListener('submit', function(e) {
    e.preventDefault();
    var firstName = document.getElementById('gate-name').value.trim();
    var email = document.getElementById('gate-email').value.trim();
    if (!firstName || !email) return;

    // Use only the first name if they typed a full name
    firstName = firstName.split(/\s+/)[0];
    // Capitalize first letter
    firstName = firstName.charAt(0).toUpperCase() + firstName.slice(1).toLowerCase();

    var data = { firstName: firstName, email: email, ts: new Date().toISOString() };
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(data)); } catch(e) {}

    // Submit to Netlify Forms
    var formData = new FormData(form);
    fetch('/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams(formData).toString()
    }).catch(function() {});

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
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Gated ebook written to {OUTPUT}")
    print(f"  - Placeholder replaced with personalized <span>")
    print(f"  - Editor note removed")
    print(f"  - Gate overlay + localStorage persistence added")
    print(f"  - Ready for Netlify deployment")


if __name__ == "__main__":
    build()
