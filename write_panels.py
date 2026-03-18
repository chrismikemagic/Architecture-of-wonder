#!/usr/bin/env python3
"""Replace the four Performance Read Panel HTML constants with improved versions."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('build-book.py', encoding='utf-8') as f:
    content = f.read()

OLD_START = '# \u2500\u2500 Ch10: Performance Read Panel visuals \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500'
OLD_END   = '# \u2500\u2500 Ch7: 10-Second Scan visual \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500'

i1 = content.find(OLD_START)
i2 = content.find(OLD_END)

NEW_BLOCK = """# \u2500\u2500 Ch10: Performance Read Panel visuals \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500

# Five Things Panel \u2014 3+2 SVG layout for readable card widths
FIVE_THINGS_PANEL_HTML = '''
<div style="margin:2em 0 2.5em;page-break-inside:avoid;">
<svg viewBox="0 0 900 530" xmlns="http://www.w3.org/2000/svg" style="width:100%;display:block;border-radius:4px;overflow:hidden;">
  <rect width="900" height="530" fill="#0d1117"/>
  <rect x="0" y="0" width="900" height="44" fill="#0a0e14"/>
  <line x1="0" y1="44" x2="900" y2="44" stroke="#C9A84C" stroke-width="0.5" opacity="0.4"/>
  <text x="450" y="18" text-anchor="middle" fill="white" font-size="13" font-family="Georgia,serif" letter-spacing="5" font-weight="bold">THE FIVE THINGS YOU\u2019RE ALWAYS READING</text>
  <text x="450" y="35" text-anchor="middle" fill="#C9A84C" font-size="10" font-family="Georgia,serif" font-style="italic">Every signal maps to one of these five questions. Answer them and you know the room.</text>

  <!-- ROW 1: Cards 1, 2, 3 \u2014 width 282 each -->

  <!-- Card 1 -->
  <rect x="10" y="56" width="282" height="210" rx="3" fill="#131920" stroke="#1c2535" stroke-width="1"/>
  <rect x="10" y="56" width="282" height="5" rx="3" fill="#C9A84C"/>
  <text x="40" y="86" fill="#C9A84C" font-size="32" font-family="Georgia,serif" font-weight="bold" opacity="0.18">1</text>
  <text x="151" y="88" text-anchor="middle" fill="#C9A84C" font-size="11" font-family="Georgia,serif" letter-spacing="2" font-weight="bold">DID IT LAND?</text>
  <line x1="26" y1="98" x2="276" y2="98" stroke="#1c2535" stroke-width="0.7"/>
  <text x="151" y="116" text-anchor="middle" fill="#7a8ba8" font-size="10" font-family="Georgia,serif">Are they still with you, or did</text>
  <text x="151" y="130" text-anchor="middle" fill="#7a8ba8" font-size="10" font-family="Georgia,serif">the last moment miss its mark?</text>
  <line x1="26" y1="144" x2="276" y2="144" stroke="#1c2535" stroke-width="0.7"/>
  <text x="151" y="160" text-anchor="middle" fill="#4a5e7a" font-size="8.5" font-family="Georgia,serif" letter-spacing="1.5">LOOK FOR</text>
  <text x="151" y="176" text-anchor="middle" fill="#c0cce0" font-size="10" font-family="Georgia,serif">Eye contact shift</text>
  <text x="151" y="191" text-anchor="middle" fill="#c0cce0" font-size="10" font-family="Georgia,serif">Blink rate change</text>
  <text x="151" y="206" text-anchor="middle" fill="#c0cce0" font-size="10" font-family="Georgia,serif">Postural lean</text>
  <text x="151" y="221" text-anchor="middle" fill="#c0cce0" font-size="10" font-family="Georgia,serif">Breath pattern</text>

  <!-- Card 2 -->
  <rect x="308" y="56" width="282" height="210" rx="3" fill="#131920" stroke="#1c2535" stroke-width="1"/>
  <rect x="308" y="56" width="282" height="5" rx="3" fill="#1A8FA8"/>
  <text x="338" y="86" fill="#1A8FA8" font-size="32" font-family="Georgia,serif" font-weight="bold" opacity="0.18">2</text>
  <text x="449" y="88" text-anchor="middle" fill="#1A8FA8" font-size="11" font-family="Georgia,serif" letter-spacing="2" font-weight="bold">CAN THEY BE LED?</text>
  <line x1="324" y1="98" x2="574" y2="98" stroke="#1c2535" stroke-width="0.7"/>
  <text x="449" y="116" text-anchor="middle" fill="#7a8ba8" font-size="10" font-family="Georgia,serif">Are they following your pace,</text>
  <text x="449" y="130" text-anchor="middle" fill="#7a8ba8" font-size="10" font-family="Georgia,serif">or running their own script?</text>
  <line x1="324" y1="144" x2="574" y2="144" stroke="#1c2535" stroke-width="0.7"/>
  <text x="449" y="160" text-anchor="middle" fill="#4a5e7a" font-size="8.5" font-family="Georgia,serif" letter-spacing="1.5">LOOK FOR</text>
  <text x="449" y="176" text-anchor="middle" fill="#c0cce0" font-size="10" font-family="Georgia,serif">Mirroring your pace</text>
  <text x="449" y="191" text-anchor="middle" fill="#c0cce0" font-size="10" font-family="Georgia,serif">Head nodding</text>
  <text x="449" y="206" text-anchor="middle" fill="#c0cce0" font-size="10" font-family="Georgia,serif">Open body toward you</text>
  <text x="449" y="221" text-anchor="middle" fill="#c0cce0" font-size="10" font-family="Georgia,serif">Silence as compliance</text>

  <!-- Card 3 -->
  <rect x="606" y="56" width="284" height="210" rx="3" fill="#131920" stroke="#1c2535" stroke-width="1"/>
  <rect x="606" y="56" width="284" height="5" rx="3" fill="#A83030"/>
  <text x="636" y="86" fill="#A83030" font-size="32" font-family="Georgia,serif" font-weight="bold" opacity="0.18">3</text>
  <text x="748" y="88" text-anchor="middle" fill="#A83030" font-size="11" font-family="Georgia,serif" letter-spacing="2" font-weight="bold">PUSHING BACK?</text>
  <line x1="622" y1="98" x2="874" y2="98" stroke="#1c2535" stroke-width="0.7"/>
  <text x="748" y="116" text-anchor="middle" fill="#7a8ba8" font-size="10" font-family="Georgia,serif">Is there resistance \u2014 visible</text>
  <text x="748" y="130" text-anchor="middle" fill="#7a8ba8" font-size="10" font-family="Georgia,serif">or just below the surface?</text>
  <line x1="622" y1="144" x2="874" y2="144" stroke="#1c2535" stroke-width="0.7"/>
  <text x="748" y="160" text-anchor="middle" fill="#4a5e7a" font-size="8.5" font-family="Georgia,serif" letter-spacing="1.5">LOOK FOR</text>
  <text x="748" y="176" text-anchor="middle" fill="#c0cce0" font-size="10" font-family="Georgia,serif">Lean back + arms cross</text>
  <text x="748" y="191" text-anchor="middle" fill="#c0cce0" font-size="10" font-family="Georgia,serif">Smirk at wrong moment</text>
  <text x="748" y="206" text-anchor="middle" fill="#c0cce0" font-size="10" font-family="Georgia,serif">Breaking eye contact</text>
  <text x="748" y="221" text-anchor="middle" fill="#c0cce0" font-size="10" font-family="Georgia,serif">Whisper to neighbor</text>

  <!-- ROW 2: Cards 4, 5 \u2014 width 435 each -->

  <!-- Card 4 -->
  <rect x="10" y="278" width="435" height="238" rx="3" fill="#131920" stroke="#1c2535" stroke-width="1"/>
  <rect x="10" y="278" width="435" height="5" rx="3" fill="#6B52A0"/>
  <text x="42" y="314" fill="#6B52A0" font-size="40" font-family="Georgia,serif" font-weight="bold" opacity="0.15">4</text>
  <text x="228" y="310" text-anchor="middle" fill="#6B52A0" font-size="12" font-family="Georgia,serif" letter-spacing="2" font-weight="bold">ARE THEY COMFORTABLE?</text>
  <line x1="26" y1="322" x2="429" y2="322" stroke="#1c2535" stroke-width="0.7"/>
  <text x="228" y="342" text-anchor="middle" fill="#7a8ba8" font-size="10.5" font-family="Georgia,serif">Is this person safe enough to go deeper, or do they need space?</text>
  <line x1="26" y1="356" x2="429" y2="356" stroke="#1c2535" stroke-width="0.7"/>
  <text x="228" y="374" text-anchor="middle" fill="#4a5e7a" font-size="8.5" font-family="Georgia,serif" letter-spacing="1.5">LOOK FOR</text>
  <text x="228" y="392" text-anchor="middle" fill="#c0cce0" font-size="10.5" font-family="Georgia,serif">Relaxed hands and face \u00b7 Breathing depth normal</text>
  <text x="228" y="410" text-anchor="middle" fill="#c0cce0" font-size="10.5" font-family="Georgia,serif">Comfortable conversational distance \u00b7 Unprompted smiling</text>

  <!-- Card 5 -->
  <rect x="455" y="278" width="435" height="238" rx="3" fill="#131920" stroke="#C9A84C" stroke-width="1" opacity="0.8"/>
  <rect x="455" y="278" width="435" height="5" rx="3" fill="#C9A84C"/>
  <text x="487" y="314" fill="#C9A84C" font-size="40" font-family="Georgia,serif" font-weight="bold" opacity="0.15">5</text>
  <text x="672" y="310" text-anchor="middle" fill="#C9A84C" font-size="12" font-family="Georgia,serif" letter-spacing="2" font-weight="bold">IS THE ROOM HOLDING?</text>
  <line x1="471" y1="322" x2="874" y2="322" stroke="#1c2535" stroke-width="0.7"/>
  <text x="672" y="342" text-anchor="middle" fill="#7a8ba8" font-size="10.5" font-family="Georgia,serif">Is the collective energy building, or beginning to fracture?</text>
  <line x1="471" y1="356" x2="874" y2="356" stroke="#1c2535" stroke-width="0.7"/>
  <text x="672" y="374" text-anchor="middle" fill="#4a5e7a" font-size="8.5" font-family="Georgia,serif" letter-spacing="1.5">LOOK FOR</text>
  <text x="672" y="392" text-anchor="middle" fill="#c0cce0" font-size="10.5" font-family="Georgia,serif">Room-wide stillness \u00b7 Collective blink slowing</text>
  <text x="672" y="410" text-anchor="middle" fill="#c0cce0" font-size="10.5" font-family="Georgia,serif">Nobody reaching for phone \u00b7 Shared forward lean</text>
  <rect x="582" y="490" width="180" height="18" rx="9" fill="rgba(201,168,76,0.15)" stroke="#C9A84C" stroke-width="0.7"/>
  <text x="672" y="502" text-anchor="middle" fill="#C9A84C" font-size="8.5" font-family="Georgia,serif" letter-spacing="1.5">THE MASTER READ</text>
</svg>
</div>
'''


# Signal Table \u2014 HTML/CSS for readable text at any screen width
SIGNAL_TABLE_HTML = '''
<div style="margin:2em 0 2.5em;page-break-inside:avoid;background:#0d1117;border-radius:6px;overflow:hidden;border:1px solid rgba(255,255,255,0.07);">
  <div style="background:#0a0e14;padding:1em 1.5em 0.8em;text-align:center;border-bottom:1px solid rgba(201,168,76,0.3);">
    <div style="font-size:0.7em;letter-spacing:0.3em;color:white;font-weight:bold;text-transform:uppercase;margin-bottom:0.3em;">The Signal Table</div>
    <div style="font-size:0.8em;color:#C9A84C;font-style:italic;">Three colors. One decision per row. Signal / What You See / What It Means / What To Do.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:#0f1520;border-bottom:1px solid #1c2535;">
    <div style="padding:0.5em 1em;font-size:0.65em;letter-spacing:0.15em;color:#4a5e7a;text-transform:uppercase;">Signal</div>
    <div style="padding:0.5em 0.8em;font-size:0.65em;letter-spacing:0.15em;color:#4a5e7a;text-transform:uppercase;border-left:1px solid #1c2535;">What You See</div>
    <div style="padding:0.5em 0.8em;font-size:0.65em;letter-spacing:0.15em;color:#4a5e7a;text-transform:uppercase;border-left:1px solid #1c2535;">What It Means</div>
    <div style="padding:0.5em 0.8em;font-size:0.65em;letter-spacing:0.15em;color:#4a5e7a;text-transform:uppercase;border-left:1px solid #1c2535;">What To Do</div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;background:rgba(34,168,85,0.12);border-left:4px solid #22a855;border-bottom:1px solid rgba(34,168,85,0.2);padding:0.45em 1em;">
    <div style="font-size:0.7em;letter-spacing:0.15em;color:#22a855;font-weight:bold;">GREEN \u2014 ENGAGED</div>
    <div style="font-size:0.72em;color:rgba(34,168,85,0.65);font-style:italic;text-align:right;padding-right:0.5em;">Stay the course. Go deeper. This is working.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:rgba(34,168,85,0.04);border-bottom:1px solid #161e16;border-left:2px solid rgba(34,168,85,0.35);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Forward lean</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Body tilted toward you; weight on front of chair</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Invested. Emotionally present.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#22a855;border-left:1px solid #1c2535;">Increase specificity</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid #161e16;border-left:2px solid rgba(34,168,85,0.35);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Slow blink rate</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Long intervals between blinks; relaxed eyelids</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Attention locked. Prediction system active.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#22a855;border-left:1px solid #1c2535;">Hold pace. Don\u2019t break.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:rgba(34,168,85,0.04);border-bottom:1px solid #161e16;border-left:2px solid rgba(34,168,85,0.35);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Room-wide stillness</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Movement stops; nobody shifting or reaching</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Full cortisol window. Collective hold.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#22a855;border-left:1px solid #1c2535;">Extend the build</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid #161e16;border-left:2px solid rgba(34,168,85,0.35);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Sustained eye contact</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Holding gaze without looking away</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Trust. Open to suggestion.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#22a855;border-left:1px solid #1c2535;">Hold contact. Slow down.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:rgba(34,168,85,0.04);border-bottom:1px solid #161e16;border-left:2px solid rgba(34,168,85,0.35);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Head nod (slow)</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Deliberate nods during your delivery</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Processing and agreeing simultaneously.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#22a855;border-left:1px solid #1c2535;">Name what they feel</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid #161e16;border-left:2px solid rgba(34,168,85,0.35);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Open posture</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Arms relaxed, hands visible, chest open</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">No defensive blocking. Receptive state.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#22a855;border-left:1px solid #1c2535;">Move into their space</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:rgba(34,168,85,0.04);border-bottom:1px solid #161e16;border-left:2px solid rgba(34,168,85,0.35);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Arms uncrossed (shift)</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Arms drop from crossed to open</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Resistance just dropped. Window opened.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#22a855;border-left:1px solid #1c2535;">Immediate ask or reveal</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid #161e16;border-left:2px solid rgba(34,168,85,0.35);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Spontaneous smile</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Genuine smile reaching eyes (Duchenne)</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Dopamine active. Wants more.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#22a855;border-left:1px solid #1c2535;">Reward immediately</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:rgba(34,168,85,0.04);border-bottom:1px solid #161e16;border-left:2px solid rgba(34,168,85,0.35);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Mirroring your pace</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">They match your speed and rhythm unconsciously</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Deep rapport. Following your lead.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#22a855;border-left:1px solid #1c2535;">Lead the change you want</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid rgba(34,168,85,0.25);border-left:2px solid rgba(34,168,85,0.35);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Held breath (visible)</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Chest stops moving; breath suspended</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Peak anticipation. Reveal window is now.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#22a855;border-left:1px solid #1c2535;">Deliver. Don\u2019t extend.</div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;background:rgba(201,168,76,0.12);border-left:4px solid #C9A84C;border-bottom:1px solid rgba(201,168,76,0.2);border-top:1px solid rgba(201,168,76,0.15);padding:0.45em 1em;">
    <div style="font-size:0.7em;letter-spacing:0.15em;color:#C9A84C;font-weight:bold;">YELLOW \u2014 UNCERTAIN</div>
    <div style="font-size:0.72em;color:rgba(201,168,76,0.65);font-style:italic;text-align:right;padding-right:0.5em;">Adjust. Check in. Don\u2019t push yet.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:rgba(201,168,76,0.04);border-bottom:1px solid #1e1c12;border-left:2px solid rgba(201,168,76,0.4);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Looking around</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Eyes scanning the room instead of staying on you</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Checking for social permission.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#C9A84C;border-left:1px solid #1c2535;">Reestablish with room</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid #1e1c12;border-left:2px solid rgba(201,168,76,0.4);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Face touch</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Hand moves to mouth, nose, or cheek mid-thought</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Cognitive load spiking. Self-soothing.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#C9A84C;border-left:1px solid #1c2535;">Simplify. Reduce complexity.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:rgba(201,168,76,0.04);border-bottom:1px solid #1e1c12;border-left:2px solid rgba(201,168,76,0.4);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Neutral expression</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Face flat; no visible affect</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Evaluating. Verdict not in yet.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#C9A84C;border-left:1px solid #1c2535;">Deliver proof. Don\u2019t explain.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid #1e1c12;border-left:2px solid rgba(201,168,76,0.4);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Arms starting to cross</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Folding across body, not yet fully closed</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Early defensive signal. Not yet closed off.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#C9A84C;border-left:1px solid #1c2535;">Reduce pressure. Add warmth.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:rgba(201,168,76,0.04);border-bottom:1px solid #1e1c12;border-left:2px solid rgba(201,168,76,0.4);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Hesitation before reply</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Delay between prompt and response</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Processing or calculating. Uncertain.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#C9A84C;border-left:1px solid #1c2535;">Wait. Give them space.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid #1e1c12;border-left:2px solid rgba(201,168,76,0.4);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Eyebrow micro-raise</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Quick flash of brow lift, gone in under a second</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Surprise or disbelief. Not fully sold yet.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#C9A84C;border-left:1px solid #1c2535;">Restate and anchor</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:rgba(201,168,76,0.04);border-bottom:1px solid #1e1c12;border-left:2px solid rgba(201,168,76,0.4);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Evaluative squint</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Eyes narrow slightly; concentrating hard</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Scrutinizing. Wants more evidence.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#C9A84C;border-left:1px solid #1c2535;">Give a T1 proof point</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid #1e1c12;border-left:2px solid rgba(201,168,76,0.4);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Reduced eye contact</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Brief breaks increasing; gaze wandering</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Starting to disengage. Attention drifting.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#C9A84C;border-left:1px solid #1c2535;">Re-engage with name or question</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid rgba(201,168,76,0.2);border-left:2px solid rgba(201,168,76,0.4);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Brow furrow</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Vertical lines between brows; effortful thinking</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Confusion or dissonance. Lost the thread.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#C9A84C;border-left:1px solid #1c2535;">Recap. Back up one step.</div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;background:rgba(168,48,48,0.15);border-left:4px solid #A83030;border-bottom:1px solid rgba(168,48,48,0.2);border-top:1px solid rgba(168,48,48,0.15);padding:0.45em 1em;">
    <div style="font-size:0.7em;letter-spacing:0.15em;color:#A83030;font-weight:bold;">RED \u2014 DISENGAGED / RESISTANT</div>
    <div style="font-size:0.72em;color:rgba(168,48,48,0.65);font-style:italic;text-align:right;padding-right:0.5em;">Pivot now. Don\u2019t push through.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:rgba(168,48,48,0.05);border-bottom:1px solid #1e1212;border-left:2px solid rgba(168,48,48,0.45);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Lean back + arms cross</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Full body retreat; closed, symmetric posture</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Closed off. Disengaged or resistant.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#A83030;border-left:1px solid #1c2535;">Reframe. Lower the stakes.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid #1e1212;border-left:2px solid rgba(168,48,48,0.45);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Phone check</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Hand reaches for phone or screen glanced at</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Fully broken. Nothing competes anymore.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#A83030;border-left:1px solid #1c2535;">Call it out or skip them</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:rgba(168,48,48,0.05);border-bottom:1px solid #1e1212;border-left:2px solid rgba(168,48,48,0.45);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Laugh at wrong moment</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Nervous or contemptuous laugh; nothing was funny</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Cortisol discharge. Tension broke wrong way.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#A83030;border-left:1px solid #1c2535;">Reset. Drop the bit entirely.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid #1e1212;border-left:2px solid rgba(168,48,48,0.45);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Fidgeting / leg-recross</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Repetitive movement; crossing and uncrossing</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Anxious or impatient. Needs release.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#A83030;border-left:1px solid #1c2535;">Shorter format. Move on.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:rgba(168,48,48,0.05);border-bottom:1px solid #1e1212;border-left:2px solid rgba(168,48,48,0.45);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Whisper to neighbor</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Leaning and murmuring to person beside them</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">You\u2019ve lost them to each other.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#A83030;border-left:1px solid #1c2535;">Bring them in or move past them</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid #1e1212;border-left:2px solid rgba(168,48,48,0.45);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Evaluative smirk</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Asymmetric half-smile; contemptuous micro-expression</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Disbelief with a power stance. Challenge.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#A83030;border-left:1px solid #1c2535;">Acknowledge, don\u2019t compete</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;background:rgba(168,48,48,0.05);border-bottom:1px solid #1e1212;border-left:2px solid rgba(168,48,48,0.45);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Sharp blink increase</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Blink rate jumps; rapid repeated blinking</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Mental reset. Lost focus. Stress spike.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#A83030;border-left:1px solid #1c2535;">Pattern interrupt. Change state.</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-bottom:1px solid #1e1212;border-left:2px solid rgba(168,48,48,0.45);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Feet toward exit</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Lower body oriented away or toward door</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Mind already leaving. Most honest signal.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#A83030;border-left:1px solid #1c2535;">Close fast or release</div>
  </div>
  <div style="display:grid;grid-template-columns:160px 1fr 1fr 170px;border-left:2px solid rgba(168,48,48,0.45);">
    <div style="padding:0.6em 1em;font-size:0.85em;color:#c0cce0;">Full shift back in chair</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Maximum posterior shift; distance sought</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#8a9ab8;border-left:1px solid #1c2535;">Creating space. Wants separation.</div>
    <div style="padding:0.6em 0.8em;font-size:0.85em;color:#A83030;border-left:1px solid #1c2535;">Don\u2019t follow in. Give space.</div>
  </div>
  <div style="background:#080e14;padding:0.8em 1.5em;text-align:center;border-top:1px solid rgba(201,168,76,0.2);">
    <div style="font-size:0.75em;letter-spacing:0.12em;color:#C9A84C;margin-bottom:0.25em;">THE THREE-SIGNAL RULE</div>
    <div style="font-size:0.8em;color:#4a5e7a;">One signal is noise. Two is a pattern forming. Three signals in the same color is a read. Act on it.</div>
  </div>
</div>
'''


MINI_SCENARIOS_HTML = '''
<div style="margin:2em 0 2.5em;page-break-inside:avoid;">
<svg viewBox="0 0 900 310" xmlns="http://www.w3.org/2000/svg" style="width:100%;display:block;border-radius:4px;overflow:hidden;">
  <rect width="900" height="310" fill="#0d1117"/>
  <rect x="0" y="0" width="900" height="36" fill="#0a0e14"/>
  <line x1="0" y1="36" x2="900" y2="36" stroke="#1c2535" stroke-width="0.8"/>
  <text x="450" y="14" text-anchor="middle" fill="white" font-size="12" font-family="Georgia,serif" letter-spacing="4" font-weight="bold">IN-PERFORMANCE READS</text>
  <text x="450" y="29" text-anchor="middle" fill="#4a5e7a" font-size="9" font-family="Georgia,serif" font-style="italic">Observation cluster \u2192 Decision</text>

  <!-- LEFT CARD: Green scenario -->
  <rect x="10" y="48" width="430" height="248" rx="3" fill="#0f1a14" stroke="rgba(34,168,85,0.3)" stroke-width="1"/>
  <rect x="10" y="48" width="430" height="4" rx="3" fill="#22a855"/>
  <rect x="18" y="62" width="58" height="19" rx="9" fill="rgba(34,168,85,0.15)" stroke="rgba(34,168,85,0.4)" stroke-width="0.7"/>
  <text x="47" y="75" text-anchor="middle" fill="#22a855" font-size="8.5" font-family="Georgia,serif" letter-spacing="1">GREEN</text>
  <text x="90" y="75" fill="#c0cce0" font-size="10" font-family="Georgia,serif" font-weight="bold">You See:</text>
  <text x="18" y="100" fill="#7a8ba8" font-size="9.5" font-family="Georgia,serif">Volunteer leans forward. Body still. Blink rate</text>
  <text x="18" y="115" fill="#7a8ba8" font-size="9.5" font-family="Georgia,serif">slowed. Hands open in lap. Eyes holding yours.</text>
  <line x1="18" y1="129" x2="420" y2="129" stroke="#1a2e1a" stroke-width="0.7"/>
  <text x="18" y="148" fill="#c0cce0" font-size="10" font-family="Georgia,serif" font-weight="bold">What It Means:</text>
  <text x="18" y="166" fill="#7a8ba8" font-size="9.5" font-family="Georgia,serif">Three green signals in a cluster. They are fully</text>
  <text x="18" y="181" fill="#7a8ba8" font-size="9.5" font-family="Georgia,serif">inside the experience. Resistance is gone.</text>
  <line x1="18" y1="195" x2="420" y2="195" stroke="#1a2e1a" stroke-width="0.7"/>
  <text x="18" y="214" fill="#c0cce0" font-size="10" font-family="Georgia,serif" font-weight="bold">What To Do:</text>
  <rect x="18" y="222" width="404" height="60" rx="3" fill="rgba(34,168,85,0.08)" stroke="rgba(34,168,85,0.2)" stroke-width="0.7"/>
  <text x="220" y="248" text-anchor="middle" fill="#22a855" font-size="20" font-family="Georgia,serif" font-weight="bold" font-style="italic">Stay. Go deeper.</text>
  <text x="220" y="270" text-anchor="middle" fill="#4a7a5a" font-size="9" font-family="Georgia,serif">This is your window. Don\u2019t break it with explanation.</text>

  <!-- RIGHT CARD: Red scenario -->
  <rect x="460" y="48" width="430" height="248" rx="3" fill="#1a0f0f" stroke="rgba(168,48,48,0.3)" stroke-width="1"/>
  <rect x="460" y="48" width="430" height="4" rx="3" fill="#A83030"/>
  <rect x="468" y="62" width="52" height="19" rx="9" fill="rgba(168,48,48,0.15)" stroke="rgba(168,48,48,0.4)" stroke-width="0.7"/>
  <text x="494" y="75" text-anchor="middle" fill="#A83030" font-size="8.5" font-family="Georgia,serif" letter-spacing="1">RED</text>
  <text x="530" y="75" fill="#c0cce0" font-size="10" font-family="Georgia,serif" font-weight="bold">You See:</text>
  <text x="468" y="100" fill="#7a8ba8" font-size="9.5" font-family="Georgia,serif">Volunteer squints. Shifts back in chair. Touches</text>
  <text x="468" y="115" fill="#7a8ba8" font-size="9.5" font-family="Georgia,serif">face. Blink rate increasing. Eyes leave yours.</text>
  <line x1="468" y1="129" x2="870" y2="129" stroke="#2e1a1a" stroke-width="0.7"/>
  <text x="468" y="148" fill="#c0cce0" font-size="10" font-family="Georgia,serif" font-weight="bold">What It Means:</text>
  <text x="468" y="166" fill="#7a8ba8" font-size="9.5" font-family="Georgia,serif">Three signals: discomfort, scrutiny, self-soothing.</text>
  <text x="468" y="181" fill="#7a8ba8" font-size="9.5" font-family="Georgia,serif">The last move missed. They are managing anxiety.</text>
  <line x1="468" y1="195" x2="870" y2="195" stroke="#2e1a1a" stroke-width="0.7"/>
  <text x="468" y="214" fill="#c0cce0" font-size="10" font-family="Georgia,serif" font-weight="bold">What To Do:</text>
  <rect x="468" y="222" width="404" height="60" rx="3" fill="rgba(168,48,48,0.08)" stroke="rgba(168,48,48,0.2)" stroke-width="0.7"/>
  <text x="670" y="248" text-anchor="middle" fill="#A83030" font-size="20" font-family="Georgia,serif" font-weight="bold" font-style="italic">You missed. Pivot.</text>
  <text x="670" y="270" text-anchor="middle" fill="#7a3a3a" font-size="9" font-family="Georgia,serif">Acknowledge, redirect, or drop the bit entirely.</text>
</svg>
</div>
'''


# Cheat Sheet \u2014 HTML/CSS grid for readable text
CHEAT_SHEET_HTML = '''
<div style="margin:2em 0 2.5em;page-break-inside:avoid;background:#0d1117;border-radius:6px;overflow:hidden;border:1px solid rgba(255,255,255,0.07);">
  <div style="background:#0a0e14;padding:1em 1.5em 0.8em;text-align:center;border-bottom:1px solid rgba(201,168,76,0.3);">
    <div style="font-size:0.7em;letter-spacing:0.3em;color:white;font-weight:bold;text-transform:uppercase;margin-bottom:0.3em;">Quick-Reference Cheat Sheet</div>
    <div style="font-size:0.8em;color:#C9A84C;font-style:italic;">If you remember nothing else, remember these. One cluster from any column is a read.</div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;">
    <div style="border-right:1px solid rgba(255,255,255,0.06);">
      <div style="background:rgba(34,168,85,0.12);border-left:4px solid #22a855;padding:0.75em 1.2em;border-bottom:1px solid rgba(34,168,85,0.2);">
        <div style="font-size:0.75em;letter-spacing:0.2em;color:#22a855;font-weight:bold;margin-bottom:0.15em;">TOP 10 GREEN</div>
        <div style="font-size:0.75em;color:rgba(34,168,85,0.6);font-style:italic;">Stay. Deepen. Deliver.</div>
      </div>
      <div style="padding:0 0 0.5em;">
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(34,168,85,0.07);"><span style="font-size:0.72em;color:rgba(34,168,85,0.45);padding-top:0.1em;">01</span><span style="font-size:0.87em;color:#c0cce0;">Forward lean</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(34,168,85,0.07);background:rgba(34,168,85,0.03);"><span style="font-size:0.72em;color:rgba(34,168,85,0.45);padding-top:0.1em;">02</span><span style="font-size:0.87em;color:#c0cce0;">Slow blink rate</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(34,168,85,0.07);"><span style="font-size:0.72em;color:rgba(34,168,85,0.45);padding-top:0.1em;">03</span><span style="font-size:0.87em;color:#c0cce0;">Room-wide stillness</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(34,168,85,0.07);background:rgba(34,168,85,0.03);"><span style="font-size:0.72em;color:rgba(34,168,85,0.45);padding-top:0.1em;">04</span><span style="font-size:0.87em;color:#c0cce0;">Sustained eye contact</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(34,168,85,0.07);"><span style="font-size:0.72em;color:rgba(34,168,85,0.45);padding-top:0.1em;">05</span><span style="font-size:0.87em;color:#c0cce0;">Slow head nod</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(34,168,85,0.07);background:rgba(34,168,85,0.03);"><span style="font-size:0.72em;color:rgba(34,168,85,0.45);padding-top:0.1em;">06</span><span style="font-size:0.87em;color:#c0cce0;">Open posture</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(34,168,85,0.07);"><span style="font-size:0.72em;color:rgba(34,168,85,0.45);padding-top:0.1em;">07</span><span style="font-size:0.87em;color:#c0cce0;">Arms uncrossing (shift)</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(34,168,85,0.07);background:rgba(34,168,85,0.03);"><span style="font-size:0.72em;color:rgba(34,168,85,0.45);padding-top:0.1em;">08</span><span style="font-size:0.87em;color:#c0cce0;">Spontaneous smile</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(34,168,85,0.07);"><span style="font-size:0.72em;color:rgba(34,168,85,0.45);padding-top:0.1em;">09</span><span style="font-size:0.87em;color:#c0cce0;">Mirroring your pace</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;background:rgba(34,168,85,0.03);"><span style="font-size:0.72em;color:rgba(34,168,85,0.45);padding-top:0.1em;">10</span><span style="font-size:0.87em;color:#c0cce0;">Held breath</span></div>
      </div>
      <div style="margin:0 1em 1em;padding:0.6em 1em;background:rgba(34,168,85,0.07);border-radius:3px;border:1px solid rgba(34,168,85,0.15);">
        <div style="font-size:0.82em;color:#22a855;font-style:italic;margin-bottom:0.2em;">Three of these = your window is open.</div>
        <div style="font-size:0.78em;color:rgba(34,168,85,0.5);">Act. Don\u2019t wait for four.</div>
      </div>
    </div>
    <div style="border-right:1px solid rgba(255,255,255,0.06);">
      <div style="background:rgba(201,168,76,0.1);border-left:4px solid #C9A84C;padding:0.75em 1.2em;border-bottom:1px solid rgba(201,168,76,0.2);">
        <div style="font-size:0.75em;letter-spacing:0.2em;color:#C9A84C;font-weight:bold;margin-bottom:0.15em;">TOP 10 YELLOW</div>
        <div style="font-size:0.75em;color:rgba(201,168,76,0.6);font-style:italic;">Adjust. Check. Don\u2019t escalate.</div>
      </div>
      <div style="padding:0 0 0.5em;">
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(201,168,76,0.07);"><span style="font-size:0.72em;color:rgba(201,168,76,0.4);padding-top:0.1em;">01</span><span style="font-size:0.87em;color:#c0cce0;">Looking around</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(201,168,76,0.07);background:rgba(201,168,76,0.03);"><span style="font-size:0.72em;color:rgba(201,168,76,0.4);padding-top:0.1em;">02</span><span style="font-size:0.87em;color:#c0cce0;">Face touch mid-thought</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(201,168,76,0.07);"><span style="font-size:0.72em;color:rgba(201,168,76,0.4);padding-top:0.1em;">03</span><span style="font-size:0.87em;color:#c0cce0;">Neutral expression</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(201,168,76,0.07);background:rgba(201,168,76,0.03);"><span style="font-size:0.72em;color:rgba(201,168,76,0.4);padding-top:0.1em;">04</span><span style="font-size:0.87em;color:#c0cce0;">Arms starting to cross</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(201,168,76,0.07);"><span style="font-size:0.72em;color:rgba(201,168,76,0.4);padding-top:0.1em;">05</span><span style="font-size:0.87em;color:#c0cce0;">Hesitation before reply</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(201,168,76,0.07);background:rgba(201,168,76,0.03);"><span style="font-size:0.72em;color:rgba(201,168,76,0.4);padding-top:0.1em;">06</span><span style="font-size:0.87em;color:#c0cce0;">Eyebrow micro-raise</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(201,168,76,0.07);"><span style="font-size:0.72em;color:rgba(201,168,76,0.4);padding-top:0.1em;">07</span><span style="font-size:0.87em;color:#c0cce0;">Evaluative squint</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(201,168,76,0.07);background:rgba(201,168,76,0.03);"><span style="font-size:0.72em;color:rgba(201,168,76,0.4);padding-top:0.1em;">08</span><span style="font-size:0.87em;color:#c0cce0;">Reduced eye contact</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(201,168,76,0.07);"><span style="font-size:0.72em;color:rgba(201,168,76,0.4);padding-top:0.1em;">09</span><span style="font-size:0.87em;color:#c0cce0;">Brow furrow</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;background:rgba(201,168,76,0.03);"><span style="font-size:0.72em;color:rgba(201,168,76,0.4);padding-top:0.1em;">10</span><span style="font-size:0.87em;color:#c0cce0;">Posture shift mid-point</span></div>
      </div>
      <div style="margin:0 1em 1em;padding:0.6em 1em;background:rgba(201,168,76,0.07);border-radius:3px;border:1px solid rgba(201,168,76,0.15);">
        <div style="font-size:0.82em;color:#C9A84C;font-style:italic;margin-bottom:0.2em;">Two yellows = slow down and check.</div>
        <div style="font-size:0.78em;color:rgba(201,168,76,0.5);">Three = you lost them. Adjust now.</div>
      </div>
    </div>
    <div>
      <div style="background:rgba(168,48,48,0.12);border-left:4px solid #A83030;padding:0.75em 1.2em;border-bottom:1px solid rgba(168,48,48,0.2);">
        <div style="font-size:0.75em;letter-spacing:0.2em;color:#A83030;font-weight:bold;margin-bottom:0.15em;">TOP 10 RED</div>
        <div style="font-size:0.75em;color:rgba(168,48,48,0.6);font-style:italic;">Pivot. Pivot. Pivot.</div>
      </div>
      <div style="padding:0 0 0.5em;">
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(168,48,48,0.07);"><span style="font-size:0.72em;color:rgba(168,48,48,0.4);padding-top:0.1em;">01</span><span style="font-size:0.87em;color:#c0cce0;">Lean back + arms cross</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(168,48,48,0.07);background:rgba(168,48,48,0.03);"><span style="font-size:0.72em;color:rgba(168,48,48,0.4);padding-top:0.1em;">02</span><span style="font-size:0.87em;color:#c0cce0;">Phone check</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(168,48,48,0.07);"><span style="font-size:0.72em;color:rgba(168,48,48,0.4);padding-top:0.1em;">03</span><span style="font-size:0.87em;color:#c0cce0;">Laugh at wrong moment</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(168,48,48,0.07);background:rgba(168,48,48,0.03);"><span style="font-size:0.72em;color:rgba(168,48,48,0.4);padding-top:0.1em;">04</span><span style="font-size:0.87em;color:#c0cce0;">Fidgeting / leg-recross</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(168,48,48,0.07);"><span style="font-size:0.72em;color:rgba(168,48,48,0.4);padding-top:0.1em;">05</span><span style="font-size:0.87em;color:#c0cce0;">Whisper to neighbor</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(168,48,48,0.07);background:rgba(168,48,48,0.03);"><span style="font-size:0.72em;color:rgba(168,48,48,0.4);padding-top:0.1em;">06</span><span style="font-size:0.87em;color:#c0cce0;">Evaluative smirk</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(168,48,48,0.07);"><span style="font-size:0.72em;color:rgba(168,48,48,0.4);padding-top:0.1em;">07</span><span style="font-size:0.87em;color:#c0cce0;">Sharp blink increase</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(168,48,48,0.07);background:rgba(168,48,48,0.03);"><span style="font-size:0.72em;color:rgba(168,48,48,0.4);padding-top:0.1em;">08</span><span style="font-size:0.87em;color:#c0cce0;">Feet toward exit</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;border-bottom:1px solid rgba(168,48,48,0.07);"><span style="font-size:0.72em;color:rgba(168,48,48,0.4);padding-top:0.1em;">09</span><span style="font-size:0.87em;color:#c0cce0;">Full shift back in chair</span></div>
        <div style="display:grid;grid-template-columns:28px 1fr;padding:0.55em 1.2em 0.55em 1em;background:rgba(168,48,48,0.03);"><span style="font-size:0.72em;color:rgba(168,48,48,0.4);padding-top:0.1em;">10</span><span style="font-size:0.87em;color:#c0cce0;">Eyes leaving performer</span></div>
      </div>
      <div style="margin:0 1em 1em;padding:0.6em 1em;background:rgba(168,48,48,0.07);border-radius:3px;border:1px solid rgba(168,48,48,0.15);">
        <div style="font-size:0.82em;color:#A83030;font-style:italic;margin-bottom:0.2em;">One red = watch. Two = pivot.</div>
        <div style="font-size:0.78em;color:rgba(168,48,48,0.5);">Three = stop the bit. Redirect now.</div>
      </div>
    </div>
  </div>
</div>
'''


"""

new_content = content[:i1] + NEW_BLOCK + content[i2:]

with open('build-book.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Done. Old block: {i2-i1} chars. New block: {len(NEW_BLOCK)} chars.")
