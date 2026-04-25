"""
Insert "Is Pre-Show Worth It?" as new CHAPTER 25, shifting old Ch25-40 → Ch26-41.
Adds Colin Cloud card (green/silver) to build-book.py.
"""
import re, shutil

NEW_CHAPTER_TEXT = """\
CHAPTER 25
Is Pre-Show Worth It?
Every pre-show is a dual reality. The only question is how contagious your method is.
────────────────────────────────────────────────────────────────────────────────
Before we talk about how to do pre-show, we need to talk about whether to do it at all.
That question sounds simple. It is not.
Here is the first thing to understand: all pre-show is dual reality.
The moment you pull someone aside before the show and give them access to information the rest of the audience does not have, you have created two separate realities in the same room. The pre-showed spectator experiences one version of what happens. Everyone else experiences another. The effect lands in the gap between them. That is not a side effect of pre-show. That is the entire mechanism. Pre-show is dual reality, and dual reality is pre-show. They are the same structural idea applied at different scales.
This matters because it changes how you evaluate risk.
When you perform a dual reality effect, you are not just asking whether the moment will land. You are asking what happens if the two realities collide. If someone compares notes after the show. If the pre-showed spectator mentions what actually happened. If someone who left early tells someone who stayed.
Colin Cloud gave me a framework for thinking about this that I have not been able to improve on.
COLIN_CLOUD:Every pre-show is a dual reality. The only question is how contagious your method is.
Think of your method as a virus.
Not a dramatic, cinematic virus. A flu. Something ordinary and highly communicable. The question you have to ask before using any method that involves a second person knowing something is: how contagious is this?
If one person in the audience learns how this was done, how quickly does that information spread? How far does it travel? How much damage does it do to the effect, to the show, to the next audience who sees you perform it?
A low-contagion method is one that, even if the spectator tells someone, either sounds unbelievable, is incomplete without context, or simply does not ruin the experience for the next person who encounters it. The method is self-limiting. It does not replicate well in the wild.
A high-contagion method is one where a single disclosure unravels everything. One person tells one person, and the chain reaction begins. The effect is destroyed for anyone downstream. The method travels cleanly, replicates easily, and takes the wonder with it when it goes.
The room itself changes the math on this considerably. A virus spreads faster in close quarters. A corporate dinner for forty people who all work together, eat lunch together, and will be in a meeting together Monday morning is a petri dish. If one person learns the method, the information is already halfway around the room before the night is over. Everyone knows everyone. The network is dense and the connections are active. In that environment, a high-contagion method is a genuine liability.
A theater show is a different environment entirely. Four hundred strangers who arrived separately, sat in assigned seats, and will leave in different directions have almost no transmission network between them. One person knowing the method has almost nowhere to send it. The same disclosure that would unravel a corporate show barely registers in a theater context because the social connections that carry the information simply do not exist. Think of it the way epidemiologists think about population density. The method is the same pathogen. The audience is the population it moves through. A dense, interconnected group amplifies spread dramatically. A dispersed crowd of strangers slows it almost to a stop.
This means your risk assessment cannot be the same for every show. The method you use freely in a theater may need to be retired entirely for a private corporate event. The question is not only how contagious the method is in the abstract. It is how contagious this method is in this room, with these people, tonight.
This framework applies beyond pre-show. It applies to any situation where a second person has access to structural information the audience does not. Someone who writes one thing while the audience thinks they wrote another. A dual reality moment built into the show itself. Any method where one participant is operating in a different reality than everyone else in the room. The question is always the same: if this person talks, how far does it spread, and what does it cost you?
Most performers do not think about methods this way. They think about concealment in the moment. Colin is thinking about what happens after the moment ends, when the show is over and people are in the parking lot comparing experiences.
That is the right place to think.
Here is the practical implication.
The best pre-show, and the best dual reality work, is designed to survive disclosure. Not because you expect it to be disclosed, but because a method that holds up under scrutiny is a method you can use freely, repeatedly, and without the low-grade anxiety that follows a performer who knows their material cannot afford to be examined.
If someone in your audience talks about what happened, the description should sound impossible. It should not illuminate the method. It should deepen the mystery. That is the standard. Anything that cannot survive that test is a method you are borrowing time with, and at some point the debt comes due.
Colin also pointed out something practical about targeting.
You can usually tell before a show which audience members are not staying for the whole thing. Sometimes the client has mentioned it. Sometimes they tell you themselves. Sometimes they have luggage with them because they are catching a flight and will be gone by intermission. Those are your pre-show targets when the method is something you genuinely cannot afford to have disclosed in the room after you perform it.
Someone who leaves before the effect lands cannot connect the dots afterward. They were not there for the reveal. They hold one half of a story without the other, and that is not a version of the method that spreads cleanly. It is the difference between a virus that completes its cycle and one that gets interrupted before it can replicate.
Here is the other thing worth saying honestly.
Most of the time, if you are a strong enough performer, you do not need pre-show at all.
Forces work. Selection works. The methods that have been developed over decades for propless, worker-level mentalism work at a very high level in the right hands. If your character is compelling, if your performance is worth watching, if the audience is genuinely with you, you can accomplish most of what pre-show achieves through craft alone. Trust yourself as a performer before you trust an arrangement you made in the lobby.
Pre-show is not a shortcut to a stronger effect. In the wrong hands it is a liability dressed up as a solution.
I use pre-show in a specific and limited way. When I need a spectator to produce a particular response that will land a specific way in the room, and when that response will be called back to multiple times during the show, I need it to feel free and uncoached every time it comes up. If the audience has any sense that the choice was narrowed for them, the callbacks lose their power. So I set the conditions before the show and let the performance itself look completely open. That is the use case I return to. Everything else I try to solve on stage.
The contagion model gives you a clean way to evaluate any method that involves a second person carrying information the audience does not have.
Ask one question. If this person talks tonight, what spreads?
If the answer is: nothing that damages the effect, nothing that travels cleanly, nothing that a third person could use to reconstruct what happened, you are working with a low-contagion method and you can proceed with confidence.
If the answer is: everything, then you are not using a method. You are making a bet.
Bet carefully.
The chapters that follow will give you the full architecture of pre-show: how to set it up, how to use it in the room, and how to build effects around it that feel impossible from every seat in the house, including the one occupied by the person who helped you.
But everything in those chapters runs on the assumption that you have already asked the contagion question and liked the answer.
Start there.
· · ·
"""

# ─── Manuscript ───────────────────────────────────────────────────────────────

shutil.copy('manuscript-extracted.txt', 'backups/manuscript-before-ch25-preshow-intro.txt')

with open('manuscript-extracted.txt', 'r', encoding='utf-8') as f:
    ms = f.read()

# Step 1: Renumber CHAPTER 25-40 → 26-41 in body (high→low, uppercase only)
for n in range(40, 24, -1):
    ms = ms.replace(f'\nCHAPTER {n}\n', f'\nCHAPTER {n+1}\n')

# Step 2: Insert new CHAPTER 25 before the renumbered CHAPTER 26 (old Pre-Show)
insert_before = '\nCHAPTER 26\nPre-Show\n'
if insert_before not in ms:
    raise ValueError(f"Could not find insertion point: {insert_before!r}")
ms = ms.replace(insert_before, f'\n{NEW_CHAPTER_TEXT}\n{insert_before[1:]}', 1)

with open('manuscript-extracted.txt', 'w', encoding='utf-8') as f:
    f.write(ms)

print("manuscript-extracted.txt updated.")

# ─── build-book.py ────────────────────────────────────────────────────────────

with open('build-book.py', 'r', encoding='utf-8') as f:
    bb = f.read()

# Step 1: Shift 'CHAPTER N' string keys 40→41 down to 25→26 (high→low)
for n in range(40, 24, -1):
    bb = bb.replace(f"'CHAPTER {n}'", f"'CHAPTER {n+1}'")
    bb = bb.replace(f'"CHAPTER {n}"', f'"CHAPTER {n+1}"')
    bb = bb.replace(f'# ── CHAPTER {n}:', f'# ── CHAPTER {n+1}:')

# Step 2: Add new CHAPTER 25 entries

# HOOK_LINES — insert at the spot after CHAPTER 24 entry
hook_entry = "    'CHAPTER 25': '\"Every pre-show is a dual reality. The only question is how contagious your method is.\"',\n"
# Find CHAPTER 26 hook entry (old CHAPTER 25 pre-show — currently has no hook) and insert before it
# Actually CHAPTER 25 had no hook before, so insert before CHAPTER 26's hook line
# The old Ch25 (Digital Preshow) hook was at CHAPTER 26 now. Let's insert before CHAPTER 26.
bb = bb.replace(
    "    'CHAPTER 26': '\"The most powerful thing you can know about a person is the thing they never thought to hide.\"',\n",
    hook_entry + "    'CHAPTER 26': '\"The most powerful thing you can know about a person is the thing they never thought to hide.\"',\n",
)

# CHAPTER_LEGEND — insert before CHAPTER 26 (old CHAPTER 25 = Pre-Show which is now 26)
legend_entry = "    'CHAPTER 25': {'tiers': ['t1', 't2'],       'cats': ['am']},          # Is Pre-Show Worth It?\n"
bb = bb.replace(
    "    'CHAPTER 26': {'tiers': ['t1', 't2'],       'cats': ['am']},          # Pre-Show\n",
    legend_entry + "    'CHAPTER 26': {'tiers': ['t1', 't2'],       'cats': ['am']},          # Pre-Show\n",
)

# Step 3: Add gen_colin_cloud_card() function after gen_anthem_aria_card()
cc_func = '''

def gen_colin_cloud_card(body):
    """Render a Colin Cloud insight card — deep green to silver gradient header."""
    body_html = _apply_bold(escape(body))
    return (
        '<div class="cc-card">'
        '<div class="cc-header">'
        '<span class="cc-label">Colin Cloud</span>'
        '<span class="cc-subtitle">Framework</span>'
        '</div>'
        f\'<div class="cc-body">{body_html}</div>\'
        \'</div>\'
    )
'''

bb = bb.replace(
    '\n\ndef gen_toolkit_nav():',
    cc_func + '\n\ndef gen_toolkit_nav():',
)

# Step 4: Add COLIN_CLOUD: trigger handler after ANTHEM_ARIA handler
cc_handler = '''\n        # ── COLIN CLOUD FRAMEWORK CARDS ──
        if stripped.startswith('COLIN_CLOUD:'):
            body = stripped[len('COLIN_CLOUD:'):].strip()
            parts.append(gen_colin_cloud_card(body))
            i += 1
            global_para_count += 1
            continue\n'''

bb = bb.replace(
    "\n        # ── RECOVERY CARDS",
    cc_handler + "\n        # ── RECOVERY CARDS",
)

# Step 5: Add CSS for Colin Cloud card after .aa-body block
cc_css = '''
/* ═══ COLIN CLOUD FRAMEWORK CARD ═══ */
.cc-card{
  margin:1.8em 0;border-radius:8px;
  overflow:hidden;
  border:1px solid rgba(30,100,60,.25);
  box-shadow:0 4px 24px rgba(0,0,0,.1),0 1px 4px rgba(31,107,58,.12);
  break-inside:avoid;
}
.cc-header{
  background:linear-gradient(105deg,#1A5C2A 0%,#266B3B 45%,#6B8A90 78%,#A8BFC4 100%);
  padding:12px 20px;
  display:flex;align-items:center;gap:14px;
}
.cc-label{
  font-family:var(--sans);font-size:.78rem;font-weight:700;
  letter-spacing:.18em;text-transform:uppercase;color:#fff;
}
.cc-subtitle{
  font-family:var(--serif);font-size:.78rem;font-style:italic;
  color:rgba(255,255,255,.68);letter-spacing:.06em;
}
.cc-body{
  background:#F2F9F4;
  border-left:4px solid #1F6B38;
  padding:16px 22px;
  font-size:.96em;line-height:1.78;color:#1a1a1a;
}
'''

bb = bb.replace(
    '\n/* ═══ MNEMONIC BLOCK ═══ */',
    cc_css + '\n/* ═══ MNEMONIC BLOCK ═══ */',
)

with open('build-book.py', 'w', encoding='utf-8') as f:
    f.write(bb)

print("build-book.py updated.")
print("Done. Run: python build-book.py && python build-gated.py")
