#!/usr/bin/env python3
"""Apply James (Spike) Scott's editorial comments (Parts 1-3, July-Aug 2026)
to Built-for-Wonder.docx. Source comments: spike-edits/spike-comments.json
(extracted from his annotated PDFs in ~/Downloads).

Three kinds of operations:
  EDITS      substring find -> replace inside one paragraph (quote-flexible
             matching: straight/curly apostrophes and double quotes both match)
  HEADINGS   whole-paragraph text swaps (lowercase subheads -> ALL CAPS so
             build-book.py's is_section_header picks them up)
  STRUCTURAL volunteer-type cards rebuilt into the one-paragraph format
             gen_volunteer_card expects; the "T"/"he 80-Signal" drop-cap
             split repaired
  SWEEPS     global consistency passes Spike requested: microexpression,
             propless, pre-show, roll a die
"""
import re
import shutil
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "Built-for-Wonder.docx"
BACKUP_DIR = ROOT / "backups"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
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
    def __init__(self):
        with zipfile.ZipFile(MASTER) as z:
            self.root = ET.fromstring(z.read("word/document.xml"))
        self.body = self.root.find(q("body"))

    def paras(self):
        return list(self.root.iter(q("p")))

    def find_paras(self, pattern):
        hits = []
        for el in self.paras():
            m = pattern.search(para_text(el))
            if m:
                hits.append((el, m))
        return hits

    def edit(self, find, replace, expect=1, label=""):
        pat = flex_pattern(find)
        hits = self.find_paras(pat)
        if len(hits) != expect:
            print(f"  !! [{label}] expected {expect} match(es), got {len(hits)}: {find[:70]!r}")
            return False
        for el, m in hits:
            splice(el, m.start(), m.end(), replace)
        print(f"  ok [{label}] x{expect}: {find[:60]!r}")
        return True

    def whole_para_swap(self, old, new, label=""):
        found = 0
        for el in self.paras():
            if para_text(el).strip() == old:
                m = re.search(re.escape(old), para_text(el))
                splice(el, m.start(), m.end(), new)
                found += 1
        if found != 1:
            print(f"  !! [{label}] whole-para {old!r}: {found} matches")
            return False
        print(f"  ok [{label}] heading: {old!r} -> {new!r}")
        return True

    def set_para(self, el, new_text):
        runs = el.findall(q("r"))
        assert runs, "paragraph without runs"
        import copy
        proto = copy.deepcopy(runs[0])
        for t in proto.findall(q("t")):
            proto.remove(t)
        for br in proto.findall(q("br")):
            proto.remove(br)
        t = ET.SubElement(proto, q("t"))
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        t.text = new_text
        for r in runs:
            el.remove(r)
        el.append(proto)

    def delete_para(self, el):
        parent = self.body
        if el in list(parent):
            parent.remove(el)
            return True
        for anc in self.root.iter():
            if el in list(anc):
                anc.remove(el)
                return True
        return False

    def unique_para(self, probe):
        pat = flex_pattern(probe)
        hits = [el for el, _ in self.find_paras(pat)]
        assert len(hits) == 1, f"probe {probe!r}: {len(hits)} hits"
        return hits[0]

    def sweep(self, pattern, repl, label=""):
        pat = re.compile(pattern)
        n = 0
        for el in self.paras():
            text = para_text(el)
            for m in reversed(list(pat.finditer(text))):
                splice(el, m.start(), m.end(), m.expand(repl) if "\\" in repl else repl)
                n += 1
        print(f"  sweep [{label}] {pattern!r}: {n} replacements")
        return n

    def save(self):
        backup = BACKUP_DIR / f"Built-for-Wonder.pre-spike-edits-{date.today().isoformat()}.docx"
        if not backup.exists():
            shutil.copy2(MASTER, backup)
            print(f"backup: {backup.name}")
        new_doc = ET.tostring(self.root, xml_declaration=True, encoding="UTF-8")
        tmp = MASTER.with_suffix(".tmp.docx")
        with zipfile.ZipFile(MASTER) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = new_doc if item.filename == "word/document.xml" else zin.read(item.filename)
                zout.writestr(item, data)
        tmp.replace(MASTER)
        print("saved", MASTER.name)


doc = Doc()
failures = []


def E(find, replace, expect=1, label=""):
    if not doc.edit(find, replace, expect, label):
        failures.append(label or find[:50])


print("== Part 1 edits ==")
E("helping me find language for thoughts I had felt for a long time",
  "helping me find language for ideas I had carried for a long time", label="P1-1")
E("law enforcement or behavioral Training", "law enforcement or behavioral training", label="P1-2")
E("Much of the material here is inspired by Chase Hughes and I really recommend anyone with a fascination with the topic of behavior read his materials and support him.",
  "Much of the material here was inspired by Chase Hughes, and I strongly recommend his work to anyone fascinated by human behavior.", label="P1-3")
E("PROILLUSIONS, Ray and Pratik, I love you both.",
  "PROILLUSIONS, Ray and Pratik. I love you both.", label="P1-5")
E("many of who I have dreamed of working for my whole life",
  "many of whom I had dreamed of working with throughout my career", label="P1-6")
E("And to the PROILLUSIONS customers, you know who you are, many of you have become genuine friends, thank you.",
  "And to the PROILLUSIONS customers, thank you. You know who you are, and many of you have become genuine friends.", label="P1-7")
E("There is so much more I wanted to teach but knew that none of the methods or techniques would matter if I didn't remove those to make room to discuss what I cover here before the book begins.",
  "There was much more I wanted to teach, but none of those methods or techniques would matter unless I first made room for what this chapter covers.", label="P1-9")
E("And the two best performances he ever watched in his whole life were a part of that show, and it had nothing to do with their methods.",
  "The two best performances he had ever seen were part of that show, and neither depended on the strength of its method.", label="P1-10")
E("The performer using them is either applying these methods or limiting their growth and audience experience.",
  "The performer either applies those tools in a way that creates connection or limits both their own growth and the audience's experience.", label="P1-11")
E("From the early nineteen-hundreds, performers", "In the early 1900s, performers", label="P1-12")
E("like the shoes you have for your dress uniform, which you have resoled as your shoes have soles that don't match the age of the upper.",
  "like the shoes you have for your dress uniform. I can tell they have been resoled because the soles do not show the same age as the uppers.", label="P1-13")
E("While the line on the shoes seems impressive, it is more so just them assuming my ignorance of their standards.",
  "While the line about the shoes sounds impressive, it depends largely on knowing the standards and habits of that environment.", label="P1-14")
E("They are always serving customers and I got my shoes shined there and struck up a conversation where it was mentioned casually that it was easier in this location because it is almost always the same shoe being brought in.",
  "The shop was always busy. While having my shoes shined there, I struck up a conversation and learned that the same few styles came through repeatedly.", label="P1-15")
E("which is a fairly stiff calf to begin with", "which is a fairly stiff calfskin to begin with", label="P1-16")
E("The mechanisms underneath that memory I shared are the same ones",
  "The mechanisms at work in that experience are the same ones", label="P1-17")
E("Wonder is what happens when the prediction fails at a moment of maximum confidence, in a context the nervous system has already decided to prepare for their imagined scenario.",
  "Wonder is what happens when a prediction fails at the moment of maximum confidence, after the nervous system has already prepared for the expected outcome.", label="P1-18")
E("The previous sentence started with your name.",
  "The previous sentence interrupted the pattern by addressing you directly.", label="P1-19")
E("Most people who watch mentalism and believe it is a collection of tricks and covert methods believe the reveal or the moment JUST before is where the work happens.",
  "Most people who see mentalism as a collection of tricks and covert methods assume the reveal, or the moment just before it, is where the real work happens.", label="P1-20")
E("you can see their chest lifting instead", "you can see their chests lifting instead", label="P1-21")
E("What you can not control (in most cases) are habits, past experiences, and biology.",
  "What you cannot control (in most cases) are ingrained habits, past experiences, and biology.", label="P1-22")
E("The amygdala in our brain. It continuously evaluates incoming information for personal significance. Particularly for threat or reward.",
  "The amygdala continuously evaluates incoming information for personal significance, particularly potential threat or reward.", label="P1-23")
E("Who are the people in the group facing towards.", "Who is the group facing toward?", label="P1-24")
E("the book “Ice Cold” by Morgan Strebler", "the book Ice Cold by Morgan Strebler", label="P1-26/P3-71")
E("The show ran for several weeks in the speakeasy of the upscale Graham Hotel outside of Georgetown University and there were many performances that when attempting to increase the discomfort of the audience and increase “the pressure in the room,” someone would cut through it with a laugh.",
  "The show ran for several weeks in the speakeasy of the upscale Graham Hotel outside of Georgetown University. In many performances, when we attempted to increase the discomfort of the audience and raise “the pressure in the room,” someone would cut through it with a laugh.", label="P1-27")
E("A room inside the window goes progressively still (the stillness of held breath, not boredom. If that stillness starts to fracture) people shifting, recrossing legs, pulling at sleeves, preening, playing with their hair: the tension has tipped from engaging to uncomfortable.",
  "A room inside the window grows progressively still. This is the stillness of held breath, not boredom. If that stillness begins to fracture through shifting, recrossing legs, pulling at sleeves, preening, or playing with hair, the tension may have tipped from engaging to uncomfortable.", label="P1-28")
E("and all of us performing will experience it again", "and everyone who performs will experience it again", label="P1-29")
E("center): Which means", "center). This means", label="P1-30")
E("Turn over your cards slower, look towards the envelope slower.",
  "Turn your cards over more slowly. Let your gaze move toward the envelope more slowly.", label="P1-32")
E("After the slight internal snicker you had when reading that name I thought it wise",
  "After the slight internal snicker you had when reading that name, I thought it wise", label="P1-33")
E("For performers, this is not interesting but it is foundational.",
  "For performers, this is not merely interesting. It is foundational.", label="P1-34")
E("and the narrative is consuming what would otherwise be available for peripheral monitoring and likely to seek out methods.",
  "and the narrative consumes cognitive resources that might otherwise be available for peripheral monitoring or searching for a method.", label="P1-35")
E("than a volley of technique.", "than a volley of techniques.", label="P1-36")
E("Amos Tversky (who I am a huge fan of), though", "Amos Tversky (whose work I am a huge fan of), though", label="P1-37")
E("Design for available, not effortful.", "Design for availability, not effort.", label="P1-38")

print("== Part 2 edits ==")
E("just without a neocortex available to override the read with logic or social politeness",
  "just without the human language and social reasoning that override the read with logic or social politeness", label="P2-40")
E("Later, it was used as evidence that the subject had a meaningful connection to the name that had been spoken and the case was cleared to move forward on investigating the person whose mention of their name caused the observable shift in behavior from the interviewee.",
  "Later, the reaction helped support further investigation into the person whose name had triggered the behavioral shift.", label="P2-41")
E("who is comfortable, who is resistant, who is in rapport with you, are you about to get a hit or miss, and who is carrying some visible internal conflict",
  "who is comfortable, who is resistant, who is in rapport with you, whether you are approaching a hit or a miss, and who is carrying visible internal conflict", label="P2-42")
E("isn't when the shaking happens, rather, when it stops", "isn't when the shaking happens, but when it stops", label="P2-43")
E("Arms crossed during a one-on-one reading is a barrier.",
  "Arms crossed during a one-on-one reading may indicate a barrier, depending on the person's baseline and the moment in which the change occurs.", label="P2-44")
E("In fact, observe any change, significant or insignificant, as a change in someone's body language or behavior is the number one most important piece here.",
  "In fact, observe every change, whether large or small. A shift in someone's body language or behavior is the most important information here.", label="P2-45")
E("though I will likely release something in the coming time to cover this topic in depth for mentalists",
  "though I will likely release something in the future that covers this topic in depth for mentalists", label="P2-48")
E("Fast walk + deliberate conversational pauses + careful object handling",
  "Fast walk + Deliberate conversational pauses + Careful object handling", label="P2-50")
E("Open posture + immediate expressiveness + head tilts frequently",
  "Open posture + Immediate expressiveness + Head tilts frequently", label="P2-51")
E("The natural Performer volunteer.", "The natural Performer Volunteer.", label="P2-52")
E("Occupies space + animated gestures + immediately comfortable center-stage",
  "Occupies space + Animated gestures + Immediately comfortable center-stage", label="P2-53")
E("Very little movement + minimal expression + looks at hands when thinking",
  "Very little movement + Minimal expression + Looks at hands when thinking", label="P2-54")
E("Which I strongly feel deserves to be in the book for the same reason the eye material belongs in this book:",
  "I strongly feel it deserves to be in the book for the same reason the eye material does:", label="P2-64")
E("The participant experiences this as ease and also this helps you feel less limited in your method to the audience.",
  "The participant experiences this as ease, and it leaves your method feeling more flexible and less procedural.", label="P2-65")

print("== Part 3 edits ==")
E("Three well-chosen conditions is almost always the right number.",
  "Three well-chosen conditions are almost always the right number.", label="P3-67")
E("The inspiration for the way he thinks about this is from The Magic Way by Juan Tamariz.",
  "Kevin's thinking here was inspired by Juan Tamariz's The Magic Way.", label="P3-69")
E("The fun part about that is they almost certainly will have an impactful encounter with someone who drives a black Tesla sometime in their near future by the sheer volume that those cars exist.",
  "The fun part: given how common black Teslas are, there is a very good chance they will later notice one in a personally meaningful context.", label="P3-72")
E("If attention is elsewhere, if the action reads as administration, friendliness, or a necessary process, then the audience has no reason yet to mark the moment as important; then the moment may be encoded weakly or fail to become useful later.",
  "If attention is elsewhere, or if the action reads as administration, friendliness, or necessary procedure, the audience has no reason yet to mark the moment as important. As a result, the moment may be encoded weakly or become difficult to retrieve later.", label="P3-73")
E("You'll also employ some cognitive dissonance so they don't later contradict the idea that they formed by themselves.",
  "You may also create enough internal consistency that the spectator is less inclined to challenge a conclusion they experienced as self-generated.", label="P3-75")
E("In corpus linguistics, which is something they mention over and over and over in counterintelligence training programs, so much that you get sick of hearing it, collocation is the probability that any two words frequently occur together, typically within five words of each other.",
  "In corpus linguistics, collocation is the probability that any two words frequently occur together, typically within five words of each other. It is something they mention over and over in counterintelligence training programs, so much that you get sick of hearing it.", label="P3-79")
E("'my mother's house', they are telling you", "'my mother's house,' they are telling you", label="P3-80")
E("Muscle reading, ideomotor response, hellstromism, contemporary motor imagery theory, or contact mind reading is something so mysterious to so many, and I am sure you are surprised to find it in a book like this.",
  "Muscle reading, ideomotor response, hellstromism, contemporary motor imagery theory, and contact mind reading remain mysterious to many people, and I am sure you are surprised to find them in a book like this.", label="P3-81")
E("contemporary motor imagery theory, which is peer-reviewed. Cool, huh?",
  "contemporary motor imagery theory, which has been examined in peer-reviewed research. Cool, huh?", label="P3-82")
E("Perhaps you have heard this to refer to something called out in the bedroom.",
  "Perhaps you have heard the term used for something called out in the bedroom.", label="P3-84")
E("Ask the back row if it is they that you are sensing to raise their hand.",
  "Ask whether anyone in the back row is thinking of something tropical, and have those people raise their hands.", label="P3-85")
E("Once you have done this, give the direction that if you have named their safeword, they should take a seat.",
  "Once you have done this, work through the group, giving the direction that anyone whose safeword you have named should take a seat.", label="P3-86")
E("And there is an emotion that you truly in heart want the people in that bar to feel before they leave.",
  "And there is an emotion that you genuinely want everyone in that bar to feel before they leave.", label="P3-87")
E("Age, background, location, style, of the bar patrons is never called to attention so they instead have to think of a song that would be known by everybody.",
  "The age, background, location, and style of the bar's patrons are never called to attention, so they instead have to think of a song that would be known by everybody.", label="P3-88")
E("the song will be \"Sweet Caroline\" or “Wonderwall” though, and this seems hard to believe, Wonderwall is seldom chosen in this context due to the habituation of the song in American culture and the loss of its emotional meaning.",
  "the song will be “Sweet Caroline” or “Wonderwall.” Though this seems hard to believe, “Wonderwall” is seldom chosen in this context, due to the habituation of the song in American culture and the loss of its emotional meaning.", label="P3-89")
E("Some examples. Ask ChatGPT to ask you any question.",
  "Some examples: Ask ChatGPT to ask you any question.", label="P3-90")
E("That is theoretically more impressive which is why",
  "That is theoretically more impressive, which is why", label="P3-92")
E("Spidey, Timon Krause, and Taha Mansour have all produced.",
  "Spidey, Timon Krause, and Taha Mansour have all produced excellent work in this area.", label="P3-68")
E("What to take away from Kevin Hamdan", "WHAT TO TAKE AWAY FROM KEVIN HAMDAN", label="P3-70")

print("== Headings ==")
for old, new, lab in (
    ("Credit", "CREDIT", "P3-83"),
    ("Consolidation", "CONSOLIDATION", "P3-74a"),
    ("Retrieval", "RETRIEVAL", "P3-74b"),
    ("Reconstruction", "RECONSTRUCTION", "P3-74c"),
    ("Source monitoring", "SOURCE MONITORING", "P3-74d"),
):
    if not doc.whole_para_swap(old, new, lab):
        failures.append(lab)

print("== Structural: 80-Signal drop-cap repair ==")
kids = list(doc.body)
he_idx = None
for i, el in enumerate(kids):
    if para_text(el).startswith("he 80-Signal System tells you who."):
        he_idx = i
        break
if he_idx is None:
    failures.append("P2-63-he")
else:
    el = kids[he_idx]
    txt = para_text(el)
    m = re.match(r"he 80-Signal System tells you who\. This real table will tell you what['’]s happening right now\.", txt)
    assert m, f"unexpected 80-signal text: {txt[:90]!r}"
    splice(el, m.start(), m.end(),
           "The 80-Signal System tells you who. This Tell Table will tell you what's happening right now.")
    prev = kids[he_idx - 1]
    assert para_text(prev).strip() == "T", f"paragraph before 80-Signal is {para_text(prev)[:30]!r}, not the stray T"
    doc.body.remove(prev)
    print("  ok merged stray 'T' drop-cap into the 80-Signal paragraph")

print("== Structural: volunteer cards ==")
GLUE = re.compile(r"(?<=[a-z\)])(?=[A-Z])")

def unglue(text):
    return " · ".join(s.strip() for s in GLUE.split(text))

CARDS = [
    ("The audience member who wants you to succeed.",
     "Leans forward with open posture throughout",
     "Works best for suggestion, imagination effects",
     "Avoid for nothing) this is the ideal volunteer",
     [("Nods frequently (not just when prompted", "Nods frequently (not just when prompted)")],
     "Avoid for nothing) this is the ideal volunteer for most routines. Select immediately. This person does half the work for you",
     "Avoid for: nothing. This is the ideal volunteer for most routines. Select immediately. This person does half the work for you."),
    ("Wants to be part of the show. Not as a participant but as a character.",
     "Expressive theatrical gesturesAlready",
     "Works best for demonstrations with a collaborative structure",
     "Avoid for effects requiring silence or quiet cooperation",
     [],
     "Avoid for effects requiring silence or quiet cooperation. Give them a role, not a task",
     "Avoid for: effects requiring silence or quiet cooperation. Give them a role, not a task."),
    ("Skeptical by nature, not by choice.",
     "Arms crossed or hands claspedLeaning",
     "Works best for predictions, undeniable effects",
     "Avoid for suggestion-based effects",
     [],
     None, None),
    ("Wants to participate but fears embarrassing themselves.",
     "Visible nervous laughter when approachedHands",
     "Works best for short, success-guaranteed interactions",
     "Avoid for any long on-stage sequence",
     [],
     None, None),
    ("Processes everything before committing.",
     "Deliberate, measured response to everythingAsks",
     "Works best for slow-burn reveals",
     "Avoid for rapid-fire or emotionally-paced effects",
     [],
     None, None),
    ("Reacts fully and authentically. Every expression visible to the room.",
     "Immediate visible reactions to unexpected momentsCovers",
     "Works best for personal readings, life readings",
     None,
     [("Covers mouth when surprised) authentically", "Covers mouth when surprised, authentically")],
     None, None),
    ("This person is quiet, contained, and not demonstratively engaged",
     "Minimal facial movement throughoutVery",
     "Works best for close-up work where intimacy matters",
     "Avoid for large stage moments",
     [],
     None, None),
]

for desc_probe, sig_probe, works_probe, avoid_probe, sig_fixes, avoid_full, avoid_repl in CARDS:
    desc_el = doc.unique_para(desc_probe)
    sig_el = doc.unique_para(sig_probe)
    works_el = doc.unique_para(works_probe)
    avoid_el = doc.unique_para(avoid_probe) if avoid_probe else None

    desc = para_text(desc_el).strip()
    if desc.startswith("Reacts fully"):
        desc = desc.replace("Not performing (just feels everything in real time.",
                            "Not performing, just feels everything in real time.")
    sig = para_text(sig_el).strip()
    for a, b in sig_fixes:
        pass  # applied after unglue on item level
    sig = unglue(sig)
    for a, b in sig_fixes:
        sig = sig.replace(a, b)
    works = para_text(works_el).strip().rstrip(".")
    assert works.startswith("Works best for "), works[:40]
    works = "Works best for: " + works[len("Works best for "):] + "."
    avoid = ""
    if avoid_el is not None:
        av = para_text(avoid_el).strip().rstrip(".")
        if avoid_full and av.startswith(avoid_full[:40]):
            avoid = avoid_repl
        else:
            assert av.startswith("Avoid for "), av[:40]
            avoid = "Avoid for: " + av[len("Avoid for "):] + "."
    merged = " ".join(x for x in (desc, sig, works, avoid) if x)
    doc.set_para(desc_el, merged)
    doc.delete_para(sig_el)
    doc.delete_para(works_el)
    if avoid_el is not None:
        doc.delete_para(avoid_el)
    print(f"  ok card rebuilt: {desc_probe[:45]!r} ({len(merged)} chars)")

print("== Sweeps ==")
doc.sweep(r"\bmicro-expression\b", "microexpression", label="micro-1")
doc.sweep(r"\bmicro-expressions\b", "microexpressions", label="micro-2")
doc.sweep(r"\bMicro-expression\b", "Microexpression", label="micro-3")
doc.sweep(r"\bMicro-expressions\b", "Microexpressions", label="micro-4")
doc.sweep(r"\bprop-less\b", "propless", label="propless-1")
doc.sweep(r"\bProp-less\b", "Propless", label="propless-2")
doc.sweep(r"\bPROP-LESS\b", "PROPLESS", label="propless-3")
doc.sweep(r"\bPRESHOW\b", "PRE-SHOW", label="preshow-1")
doc.sweep(r"\bPreshow\b", "Pre-Show", label="preshow-2")
doc.sweep(r"\bpreshow\b", "pre-show", label="preshow-3")
doc.sweep(r"\broll a dice\b", "roll a die", label="die")

if failures:
    print("\nFAILED ITEMS:", failures)
    sys.exit(1)

doc.save()
print("\nAll edits applied.")
