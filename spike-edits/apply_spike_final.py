#!/usr/bin/env python3
"""Apply James (Spike) Scott's FINAL editorial pass (2026-08-22/23, 151
comments on the 2026-08-13 draft PDF) to Built-for-Wonder.docx.

Source: ~/Downloads/"Built for Wonder - Decode Behavior (Spike's final
comments) (1).pdf"  -> extracted to spike-edits/spike-final-comments.json

Numbers in labels ([12] etc.) are the comment indices in that JSON.
Comments that are build-script rendering issues are fixed in build-book.py
(see the commit message); content decisions Chris has to make are listed in
the session summary, not applied here.

    python3 spike-edits/apply_spike_final.py           # dry run (no save)
    python3 spike-edits/apply_spike_final.py --apply   # write the DOCX
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from docx_engine import Doc, para_text  # noqa: E402

APPLY = "--apply" in sys.argv
doc = Doc()
E = doc.edit
H = doc.whole_para_swap
D = doc.delete_exact
S = doc.split_para

print("== Prose: Parts 1-2 ==")
E("Parts Three through Seven take those principles",
  "Parts Three through Five take those principles", label="1")
E("Any act on America’s Got Talent that utilizes 3 or more of these forces that control our attention are far higher in measured watch time and shares.",
  "Any act on America’s Got Talent that uses three or more of these attention forces earns far higher measured watch time and far more shares.", label="2")
E("often between 8 and 20 minutes is spent on small talk and friendly banter.",
  "interrogators often spend between 8 and 20 minutes on small talk and friendly banter.", label="9")
E("Three signals pointing the same direction is a read.",
  "Three signals pointing in the same direction constitute a read.", expect=2, label="24/34")
E("the one being suppressed most is usually the most truthful. This means that",
  "the one being suppressed most is usually the most truthful.", label="25")
E("There are four variations worth caring about as a mentalist.",
  "There are five variations worth caring about as a mentalist.", label="26")
E("Five or six conditions starts to feel like a courtroom brief.",
  "Five or six conditions start to feel like a courtroom brief.", label="27")
H("Chris Michael's Take:", "Chris Michael's Take", label="30")
E("Named 2025 and 2026 APCA Mentalists of the Year alongside his partner Aria, the two of them have spent over a decade studying and performing readings at the highest level,",
  "He and his partner Aria were named 2025 and 2026 APCA Mentalists of the Year, and the two of them have spent over a decade studying and performing readings at the highest level,", label="32")
E("I wanted to include Anthem and Aria's tips they have genuinely shared with me when writing this book.",
  "I wanted to include some of the advice Anthem and Aria generously shared with me while I was writing this book.", label="33")

print("== Ch17: contributor cards + epigraph ==")
# [31] the in-text hook quote is the Ch14 microexpression line; swap for a
# chapter-specific one (build-book.py HOOK_LINES gets the same text).
H('"Partial, rapid, and involuntary: the face tells the truth for a fraction of a second before the managed response arrives."',
  '"The experience of being seen by someone who had no reason to see you. That is the target state."', label="31")
# [37] three identical "Anthem & Aria — Field Advice" headings -> designed cards;
# the two back-to-back notes become one card.
_aa1 = doc.unique_para("Anthem and Aria also stress that readings land harder")
_aa2 = doc.unique_para("As Anthem and Aria point out, stock lines work best")
_aa3 = doc.unique_para("Aria's idea of a DIY oracle is useful here")
for probe_el in (_aa1, _aa2, _aa3):
    hdr = doc.prev_para(probe_el)
    assert para_text(hdr).strip() == "Anthem & Aria — Field Advice", para_text(hdr)[:40]
    doc.delete_para(hdr)
doc.set_para(_aa1, "ANTHEM_ARIA: " + para_text(_aa1).strip())
doc.set_para(_aa2, "ANTHEM_ARIA: " + para_text(_aa2).strip() + " " + para_text(_aa3).strip())
doc.delete_para(_aa3)
print("  ok [37] Anthem & Aria notes -> 2 designed cards")

print("== Prose: Part 3 ==")
H("Collocation. Reading How a Person Connects Ideas",
  "Collocation: Reading How a Person Connects Ideas", label="39")
E("Usually muscle reading is performed by having the spectator choose an object out of a presented set of objects, perhaps envelopes could also be a freely chosen object in the room.",
  "Usually, muscle reading begins with the spectator choosing an object from a presented set, such as envelopes. Alternatively, they might freely choose an object somewhere in the room.", label="40")
E("A good grip does not merely control the participant but it also allows you to feel any subtle signals, tugs, or pushes.",
  "A good grip not only controls the participant but also allows you to feel any subtle signals, tugs, or pushes.", label="41")
E("What you have done, across a few minutes of apparently separate work, is obtained the day, the season, and everything that implies",
  "Across a few minutes of apparently separate work, you have obtained the day, the season, and everything that implies", label="43")
H("WHY PSYCHOLOGICAL FORCES WORK THE PSYCHOLOGY BEHIND IT",
  "WHY PSYCHOLOGICAL FORCES WORK: THE PSYCHOLOGY BEHIND IT", label="44")

# [45] 13-category reference: glued numbers, bare Pros/Cons labels
for old, new in (("01Dominant Choice", "01 Dominant Choice"), ("02Statistical", "02 Statistical"),
                 ("03Scene-Completion", "03 Scene-Completion"), ("04Contextual", "04 Contextual"),
                 ("05Anchoring", "05 Anchoring"), ("06Exclusion", "06 Exclusion"),
                 ("07Phonetic", "07 Phonetic"), ("08Sensory", "08 Sensory"),
                 ("09Social-Normalcy", "09 Social-Normalcy")):
    H(old, new, label="45")
for lab in ("Pros", "Cons"):
    els = [el for el in doc.paras() if para_text(el).strip() == lab]
    assert len(els) == 13, (lab, len(els))
    for el in els:
        nxt = doc.next_para(el)
        doc.set_para(el, f"{lab}: " + para_text(nxt).strip())
        doc.delete_para(nxt)
    print(f"  ok [45] {lab} x13 merged into label: text")
# [46]/[47] Example lines
E('Example“F"Focus on one of these words: Ambient, Fracture, Storm, Derivative." Target: Storm.',
  'Example“Focus on one of these words: Ambient, Fracture, Storm, Derivative.”→ Storm.', label="47")
doc.sweep(r"^Example“", "Example: “", label="46a")
doc.sweep(r"”→ ", "” → ", label="46b")
doc.sweep(r"\.→ ", ". → ", label="46c")

# [49] Five Moving Parts: "01" / "Activation" / body -> "01 Activation" / body
for num, title in (("01", "Activation"), ("02", "Restriction"), ("03", "Fluency"),
                   ("04", "Commitment"), ("05", "Memory")):
    t_el = doc.unique_para(title, exact=True)
    n_el = doc.prev_para(t_el)
    assert para_text(n_el).strip() == num, (num, para_text(n_el))
    doc.delete_para(n_el)
    doc.set_para(t_el, f"{num} {title}")
print("  ok [49] five moving parts numbered headings")
D("A force works when it reduces the search space, increases accessibility, and lets the answer feel self-generated.", label="50")

# [52]/[53] song titles
E("The only song that I could imagine this would be is Don't Stop Believing by Journey.",
  "The only song that I could imagine this would be is “Don’t Stop Believin’” by Journey.", label="52")
E("Additionally if somebody does not seem to be impressed when you start implying that it could be, don't stop believing; then it may very well be living on a prayer. None of these outcomes are very likely. Don't stop believing when the script is performed properly; it will be the most common by far.",
  "Additionally, if somebody does not seem impressed when you start implying that it could be “Don’t Stop Believin’,” then it may very well be “Livin’ on a Prayer.” None of these outcomes are very likely. When the script is performed properly, “Don’t Stop Believin’” will be the most common by far.", label="53")
# [54] 21A label + title -> one heading
D("21A", label="54a")
H("PREDICTIVE TEXT AND ALGORITHMIC FORCES", "21A — PREDICTIVE TEXT AND ALGORITHMIC FORCES", label="54b")
E("you can using Marc Sueper’s Mentyx", "you can, using Marc Sueper’s Mentyx", label="55")
# [56] duplicate heading
_why = [el for el in doc.paras() if para_text(el).strip() == "WHY LEARN PROPLESS MENTALISM"]
assert len(_why) == 2, len(_why)
doc.delete_para(_why[1]); print("  ok [56] removed duplicate WHY LEARN PROPLESS MENTALISM")
E("As we'll discuss in the chapter on memory distortion", "As we discussed in the chapter on memory distortion", label="57")
E("Physical tagging, or embodied matrixes Or when the spectator does a specific action, movement, or pose to confirm the information.",
  "Physical tagging, or embodied matrices, is when the spectator performs a specific action, movement, or pose to confirm information.", label="61")
H("MULTIPLE WORD TITLES", "MULTIPLE-WORD TITLES", label="62a")
H("ONE WORD TITLES", "ONE-WORD TITLES", label="62b")
E("from the 1950’s to the late 2020’s", "from the 1950s to the late 2020s", label="63")
E("too dificult to correctly perscribe", "too difficult to correctly prescribe", label="64")
E("you would even be down to two options anyway", "you would even be down to two options anyway.", label="65")
E("His effect has become one of my most famous", "his effect has become one of my most famous", label="66")
E("This person is someone with a name that you likely also know several people in your life that has that name.",
  "This person has a name that several people in your life likely also have.", label="68")
E("place it in their right hand; if it is a woman", "place it in your right hand; if it is a woman", label="69")
E("sold on amazon for cheap", "sold on Amazon for cheap", label="70")
E("In each phase you will learn you a minimum of 3 tells to look for.",
  "In each phase you will learn a minimum of three tells to look for.", label="71")
E("which hand its in", "which hand it’s in", label="72")
E("As crazy as this sounds, it is an amazingly reliable.", "As crazy as this sounds, it is amazingly reliable.", label="74")
E("(from the Fruit to Fang method, covered in Chapter 12).You also",
  "(from the Fruit to Fang method, covered in Chapter 13). You also", label="76")
E("If you want access to a free web app i have made that you can use to secretly input information with swipes and then get the possible names it would be visit:",
  "If you want access to a free web app I made, which lets you secretly input the information with swipes and receive the possible names, visit:", label="77")
E("Overtime you will be able to just recognize patterns", "Over time you will be able to just recognize patterns", label="78")
E("know which name it is likey to be", "know which name it is likely to be", label="79")
E("Try: Common American Name: Male, Short Name,", "Try: Common American Name, Male, Short Name,", label="80")

print("== Ch25 zodiac subheads (sentence case -> Title Case so the build sees them) ==")
for old, new in (
    ("The iconic figure principle", "The Iconic Figure Principle"),
    ("The Aries insurance", "The Aries Insurance"),
    ("When they know their own figure", "When They Know Their Own Figure"),
    ("Close it with the elements", "Close It with the Elements"),
    ("Close it with cognitive load", "Close It with Cognitive Load"),
    ("The fruit close", "The Fruit Close"),
    ("The spelling interrupt", "The Spelling Interrupt"),
    ("The birthday close", "The Birthday Close"),
    ("Cognitive load on the figure's weapons", "Cognitive Load on the Figure’s Weapons"),
    ("The rounded-letter hanging statement", "The Rounded-Letter Hanging Statement"),
    ("The sibling gambit", "The Sibling Gambit"),
    ("The Gemini billet", "The Gemini Billet"),
    ("When they do not know their own figure", "When They Do Not Know Their Own Figure"),
    ("When they actually know their zodiacs", "When They Actually Know Their Zodiacs"),
):
    H(old, new, label="82-96")
E("is heavily inspired from Ultimate Star Sign Divination", "is heavily inspired by Ultimate Star Sign Divination", label="97")
E("Palms up the sky", "Palms up to the sky", expect=2, label="98")
E("and if the procedure can’t be done quickly, is well-justified, and done at the very start of the effect, I don’t touch it.",
  "and if the procedure can’t be done quickly, be well justified, and happen at the very start of the effect, I don’t touch it.", label="99")
E("it can take awhile", "it can take a while", label="100")

print("== Pre-show chapters ==")
# [102] Ch27 opens with the hook line, then repeats it as a one-line paragraph.
_dup = doc.unique_para("he strongest pre-show doesn't feel like pre-show at all.", exact=True)
_t = doc.prev_para(_dup)
assert para_text(_t).strip() == "T", para_text(_t)[:20]
doc.delete_para(_t); doc.delete_para(_dup); print("  ok [102] removed duplicated Ch27 opening line")
E("Instead, you will have whatever word you are just decided to concentrate on instead. Just checking, you still know remember what it is right?",
  "Instead, you will have whatever word you just decided to concentrate on. Just checking, you still remember what it is, right?", label="103")
S("Performer: Deal? WHAT THOSE LINES ARE REALLY DOING",
  "Performer: Deal?", "WHAT THOSE LINES ARE REALLY DOING", label="104")
for old, new in (("01EARLY COMMITMENT", "01 EARLY COMMITMENT"), ("02WRITING IT DOWN", "02 WRITING IT DOWN"),
                 ("03NARROWING THE CATEGORY", "03 NARROWING THE CATEGORY"), ("04THE ODD REQUEST", "04 THE ODD REQUEST"),
                 ("01BROADEN THE TIME FRAME", "01 BROADEN THE TIME FRAME"), ("02THE FAIRNESS FRAME", "02 THE FAIRNESS FRAME"),
                 ("03 — ONE EXAMPLE, NOT THE KEY", "03 ONE EXAMPLE, NOT THE KEY"), ("04PART OF THE ENVIRONMENT", "04 PART OF THE ENVIRONMENT")):
    H(old, new, label="106")
# [108] Ch28: the WHAT IT FEELS LIKE header was split into a drop-cap "W" + "HAT..."
_hat = doc.unique_para("HAT IT FEELS LIKE", exact=True)
_w = doc.prev_para(_hat)
assert para_text(_w).strip() == "W", para_text(_w)[:20]
doc.delete_para(_w); doc.set_para(_hat, "WHAT IT FEELS LIKE"); print("  ok [108] Ch28 WHAT IT FEELS LIKE header restored")
E("take a trick and turn into into something much more unexplainable",
  "take a trick and turn it into something much more unexplainable", label="109")
E("you know that she likely a coffee lover", "you know that she is likely a coffee lover", label="110")
E("Remember, by revealing impossibly obtained information respectfully is delivering on the implicit promise you have made to the room.",
  "Remember, revealing impossibly obtained information respectfully is how you deliver on the implicit promise you have made to the room.", label="113")
E("This is why Chapter 25, on method invisibility,", "This is why Chapter 30, on method invisibility,", label="114")
E("Targeted intelligence, which is what this chapter addresses. Targeted intelligence means you have a name",
  "Targeted intelligence, which is what this chapter addresses, means you have a name", label="115")
S("The Sources Social Media: The Primary Surface", "The Sources", "Social Media: The Primary Surface", label="116")
E("A large portion of the time being trained by US SOCOM instructors on counter-intelligence was focused on the evergreen environment of social media.",
  "A large portion of my training with U.S. SOCOM instructors in counterintelligence focused on the evergreen environment of social media.", label="117")
E("You will often find Linkedin accounts", "You will often find LinkedIn accounts", label="118")
E("This is where most the Tier One material lives.", "This is where most of the Tier One material lives.", label="119")
E("It mentioned that her and her mother loved", "It mentioned that she and her mother loved", label="120")
E("went from resistant to join on stage to immediately open and receptive of the whole experience.",
  "went from resistant to joining me on stage to immediately open and receptive to the whole experience.", label="121")
E("For the sake of all of us performers handle it accordingly, please.",
  "For the sake of all of us performers, please handle it accordingly.", label="122")
E("This falls within Chapter 17 territory.", "This falls within Chapter 15 territory.", label="123a")
E("barn door principles in Chapter 17", "barn door principles in Chapter 15", label="123b")
E("cortisol window principles from Chapter 3", "cortisol window principles from Chapter 5", label="123c (not flagged by Spike; window chapter is 5)")

print("== Part 4 ==")
E("behavioral lens.  There are Seven stages insides of one arc.", "behavioral lens. There are seven stages inside one arc.", label="124")
H("Make Them Remember the Impossibility, not what led you there.", "Make Them Remember the Impossibility, Not What Led You There", label="126")
# [127] Ch31: stray "T" drop cap + restated opening line ("I want to say that again" follows the hook).
_words = doc.unique_para("The words are not the performance. The timing between the words is the performance.", exact=True)
_t2 = doc.prev_para(_words)
assert para_text(_t2).strip() == "T", para_text(_t2)[:20]
doc.delete_para(_t2); doc.delete_para(_words); print("  ok [127] Ch31 stray T + restated hook removed")
doc.merge_with_next("Semantic Satiation", new_text="Semantic Satiation: Why Words Die in Your Mouth", label="128")
H("Silence as a Tool- The Instruction Pause", "Silence as a Tool: The Instruction Pause", label="129")
S("Movement and Stillness Stillness for Reveals", "Movement and Stillness", "Stillness for Reveals", label="130")
E("usually someone who was leaning forward for the last ten minutes. Two more follow within three seconds.",
  "usually someone who was leaning forward for the last ten minutes). Two more follow within three seconds.", label="131")
E("You cannot control who that person is) but you can reduce", "You cannot control who that person is, but you can reduce", label="132")
E("A specific instrumental backing track (the lead parts removed) piece plays as you are introduced and walking on stage.",
  "A specific instrumental backing track, with the lead parts removed, plays as you are introduced and walk on stage.", label="133")
E("and its always stronger when they are not told", "and it’s always stronger when they are not told", label="134")
H("Seconds 70–90. Close With Impossibility, Then Leave", "Seconds 70–90 — Close With Impossibility, Then Leave", label="136")
H("Compliance History Compliance Temperature", "Compliance Temperature", label="137")
E("Let the client's voice carry the weight. Your own voice delivering your own credentials is the least persuasive version of the same information.",
  "Let the client's voice carry the weight. Delivering your own credentials in your own voice is the least persuasive version of the same information.", label="138")

print("== Part 5 ==")
doc.merge_with_next("A Warning", new_text="A Warning I Should Tell You…", label="140")
D("INTERLUDE", label="144")
E("Walk in certain. Walk in certain. Speak without seeking approval.", "Walk in certain. Speak without seeking approval.", label="145")

print("== Ch5 recovery cards + Ch8/9 tier and T4 headings ==")
for num, name, when in (
    ("01", "The Reflect and Reset", "The room is leaning back. Someone laughed when nothing was funny. You can feel the contract fraying."),
    ("02", "Productive Silence", "A prop falls. Something small goes wrong. Acknowledgment would make it worse."),
    ("03", "The Redirect", "You need to stall, adjust a prop, or recapture attention that has drifted."),
):
    h_el = doc.unique_para(f"{num}{name}", exact=True)
    w_el = doc.next_para(h_el)
    assert para_text(w_el).strip() == f"WHEN {when}", para_text(w_el)[:60]
    doc.set_para(h_el, f"RECOVERY: {name} | {when}")
    doc.delete_para(w_el)
print("  ok [3-8] recovery cards -> RECOVERY: markers (designed amber cards with WHEN tag)")
for old, new in (("T1Physical Evidence", "T1 — Physical Evidence"), ("T2Research-Backed", "T2 — Research-Backed"),
                 ("T3Field-Tested Pattern", "T3 — Field-Tested Pattern"), ("T4Experimental", "T4 — Experimental")):
    H(old, new, label="11-14")
for old, new in (("T4NLP Eye Movement Direction", "T4: NLP Eye Movement Direction"),
                 ("T4Smooth Lower Eyelids as Confidence Indicator", "T4: Smooth Lower Eyelids as Confidence Indicator"),
                 ("T4Deep Under-Eye Wrinkles as Chronic Worry Indicator", "T4: Deep Under-Eye Wrinkles as Chronic Worry Indicator"),
                 ("T4Hair Part Direction as Personality Indicator", "T4: Hair Part Direction as Personality Indicator")):
    H(old, new, label="17-21")

print()
if doc.failures:
    print(f"{len(doc.failures)} FAILURES:")
    for f in doc.failures:
        print("  -", f)
if APPLY:
    if doc.failures:
        sys.exit("refusing to save with failures")
    doc.save(backup_tag="pre-spike-final")
else:
    print("dry run: nothing saved (pass --apply)")

# Applied separately on 2026-08-24 (same session) so the DOCX's own copy of
# the Meta Reveal matches META_REVEAL_HTML in build-book.py:
#   [147] "You will find it after this chapter." -> "You read it just before this chapter."
#   [148] "In Chapter 4, a sentence started with your first name." -> Chapter 3
#   [149] "Peak-End Rule in Chapter 39" -> Chapter 37
