"""Pass 2: remaining audit fixes + items missed by pass 1 due to apostrophe variants."""
from __future__ import annotations
import re
import sys
from pathlib import Path

SRC = Path(r"C:\Users\Chris\Architecture-of-wonder\book-cleaned.html")
content = SRC.read_text(encoding="utf-8")
original = content


def must_replace(old: str, new: str, *, label: str) -> None:
    global content
    if old not in content:
        print(f"  [skip] {label}: old text not found", file=sys.stderr)
        return
    n = content.count(old)
    content = content.replace(old, new)
    print(f"  [ok]   {label}: replaced {n}")


def maybe_replace(old: str, new: str, *, label: str) -> None:
    global content
    if old in content:
        n = content.count(old)
        content = content.replace(old, new)
        print(f"  [ok]   {label}: replaced {n}")


# ========================================================================
# Pass 1 misses
# ========================================================================
print("\n== Pass 1 misses ==")

# Five Cs grid (curly apostrophe)
must_replace(
    "<p>THE FIVE C’s OF BEHAVIORAL READING</p><p>Context</p><p>What environment?</p><p>Context determines meaning. Always.</p><p>Clusters</p><p>Multiple signals?</p><p>Never act on a single signal.</p><p>Congruence</p><p>Body = words?</p><p>Incongruence is your most reliable signal.</p><p>Consistency</p><p>Their baseline?</p><p>Without baseline, every read is a projection.</p><p>Culture</p><p>Background norms?</p><p>Calibrate before concluding.</p><p>Context›Clusters›Congruence›Consistency›Culture›READ</p>",
    "<h3>The Five C’s of Behavioral Reading</h3>"
    '<section class="pillars-grid">'
    '<article class="pillar-card"><div class="pillar-num">1</div><div class="pillar-body"><h4 class="pillar-name">Context</h4><p class="pillar-tag">What environment?</p><p class="pillar-text">Context determines meaning. Always.</p></div></article>'
    '<article class="pillar-card"><div class="pillar-num">2</div><div class="pillar-body"><h4 class="pillar-name">Clusters</h4><p class="pillar-tag">Multiple signals?</p><p class="pillar-text">Never act on a single signal.</p></div></article>'
    '<article class="pillar-card"><div class="pillar-num">3</div><div class="pillar-body"><h4 class="pillar-name">Congruence</h4><p class="pillar-tag">Body = words?</p><p class="pillar-text">Incongruence is your most reliable signal.</p></div></article>'
    '<article class="pillar-card"><div class="pillar-num">4</div><div class="pillar-body"><h4 class="pillar-name">Consistency</h4><p class="pillar-tag">Their baseline?</p><p class="pillar-text">Without baseline, every read is a projection.</p></div></article>'
    '<article class="pillar-card"><div class="pillar-num">5</div><div class="pillar-body"><h4 class="pillar-name">Culture</h4><p class="pillar-tag">Background norms?</p><p class="pillar-text">Calibrate before concluding.</p></div></article>'
    "</section>"
    '<p class="five-c-chain">Context → Clusters → Congruence → Consistency → Culture → <strong>READ</strong></p>',
    label="Ch8: rebuild Five Cs grid (curly apostrophe variant)",
)

# Ch 8 callout meta-observation moment (was previously missed)
must_replace(
    "<p>You have been reading this page for about ninety seconds. Notice which hand is holding the book. That is Observation #01 — handedness indicator. You just demonstrated it without thinking.</p>",
    '<aside class="callout callout-take"><div class="callout-label">Observation</div><div class="callout-body">You have been reading this page for about ninety seconds. Notice which hand is holding the book. That is Observation #01 — handedness indicator. You just demonstrated it without thinking.</div></aside>',
    label="Ch8: callout the meta-observation moment",
)

# Ch 18 — availble (2 occurrences)
maybe_replace("availble", "available", label="Ch18+other: availble→available")

# Other typos
maybe_replace("lcoks", "locks", label="Global: lcoks→locks")
maybe_replace("similiar", "similar", label="Global: similiar→similar")
maybe_replace("thattakes", "that takes", label="Global: thattakes")

# Ch 17 — duplicate "Cold-Warm-Hot Spectrum" stream (lines exist as plain p)
must_replace(
    "<p>The Cold-Warm-Hot Spectrum</p><p>COLD</p><h3>Pure Cold Reading</h3>",
    '<h3>The Cold-Warm-Hot Spectrum</h3>'
    '<section class="type-cards type-cards-spectrum">'
    '<article class="type-card"><header class="tc-head"><span class="tc-letter">COLD</span><h4 class="tc-name">Pure Cold Reading</h4></header>',
    label="Ch17: rebuild spectrum start (Pure Cold)",
)
must_replace(
    "<p>No prior knowledge. Works entirely from observation, context, and the Forer effect.</p><p>→</p><p>WARM</p><h3>Warm Reading</h3>",
    "<p class=\"tc-desc\">No prior knowledge. Works entirely from observation, context, and the Forer effect.</p></article>"
    '<article class="type-card"><header class="tc-head"><span class="tc-letter">WARM</span><h4 class="tc-name">Warm Reading</h4></header>',
    label="Ch17: spectrum WARM",
)
must_replace(
    "<p>Live observation. Using behavioral signals the participant has already broadcast. Most real readings are here.</p><p>→</p><p>HOT</p><h3>Hot Reading</h3>",
    "<p class=\"tc-desc\">Live observation. Using behavioral signals the participant has already broadcast. Most real readings are here.</p></article>"
    '<article class="type-card"><header class="tc-head"><span class="tc-letter">HOT</span><h4 class="tc-name">Hot Reading</h4></header>',
    label="Ch17: spectrum HOT",
)
must_replace(
    "<p>Research-based. Specific knowledge gathered in advance before the participant arrives.</p><h3>The Forer Effect</h3>",
    "<p class=\"tc-desc\">Research-based. Specific knowledge gathered in advance before the participant arrives.</p></article></section>"
    "<h3>The Forer Effect</h3>",
    label="Ch17: close spectrum + Forer Effect",
)

# Ch 17 — VAK 3-column rebuild (replace paragraph stream with table)
ch17_vak_old = (
    "<p>Visual</p><p>Language</p><p>see, clear, picture, frame, look, perspective</p><p>Eye movement</p><p>upward during recall</p><p>Gesture</p><p>frames and defines spatial space</p><p>Posture</p><p>composed, still</p>"
    "<p>Auditory</p><p>Language</p><p>hear, sounds like, rings true, loud and clear</p><p>Eye movement</p><p>horizontal or down-left</p><p>Gesture</p><p>rhythmic, in time with speech</p><p>Often tilts the head</p><p>Speaks deliberately</p>"
    "<p>Kinesthetic</p><p>Language</p><p>feel, sense, heavy, smooth, get a grip, gut feeling</p><p>Eye movement</p><p>down-right</p><p>Gesture</p><p>large and embodied</p><p>Breathing</p><p>deeper, lower in the body</p>"
)
ch17_vak_new = (
    '<div class="data-block vak-block"><table class="tbl-vak"><thead><tr>'
    "<th></th><th>Visual</th><th>Auditory</th><th>Kinesthetic</th></tr></thead><tbody>"
    "<tr><th scope=\"row\">Language</th>"
    "<td>see, clear, picture, frame, look, perspective</td>"
    "<td>hear, sounds like, rings true, loud and clear</td>"
    "<td>feel, sense, heavy, smooth, get a grip, gut feeling</td></tr>"
    "<tr><th scope=\"row\">Eye movement</th>"
    "<td>upward during recall</td>"
    "<td>horizontal or down-left</td>"
    "<td>down-right</td></tr>"
    "<tr><th scope=\"row\">Gesture</th>"
    "<td>frames and defines spatial space</td>"
    "<td>rhythmic, in time with speech; often tilts the head</td>"
    "<td>large and embodied</td></tr>"
    "<tr><th scope=\"row\">Posture / Voice</th>"
    "<td>composed, still</td>"
    "<td>speaks deliberately</td>"
    "<td>breathing deeper, lower in the body</td></tr>"
    "</tbody></table></div>"
)
must_replace(ch17_vak_old, ch17_vak_new, label="Ch17: rebuild VAK 3-column table")

# Ch 17 — Jump-to-section concatenated nav (split into proper inline labels)
must_replace(
    "<h3>Jump to section</h3><p>AppearanceMovementTerritorySocial ConfidenceCognitive ProcessingEmotional Regulation</p>",
    '<h4 class="jumpnav-label">Jump to section</h4><p class="jumpnav">Appearance · Movement · Territory · Social Confidence · Cognitive Processing · Emotional Regulation</p>',
    label="Ch17: jump-to-section split",
)

# Ch 17 — Feedback Signals heading promote
maybe_replace(
    "<p>Feedback Signals · Quick Reference</p>",
    "<h4>Feedback Signals · Quick Reference</h4>",
    label="Ch17: Feedback Signals header",
)

# Ch 17 — Reading the Feedback (concatenated phrase)
maybe_replace(
    "Reading the FeedbackFour signals. Four corrections.",
    "Reading the Feedback. Four signals. Four corrections.",
    label="Ch17: Reading the Feedback split",
)

# Ch 17 — Stock Lines vs Seeing the Person
maybe_replace("<p>Stock Lines vs. Seeing the Person</p>", "<h3>Stock Lines vs. Seeing the Person</h3>", label="Ch17: Stock Lines heading")

# Ch 17 — Listening for Collocates / Collocation
maybe_replace("<p>Listening for Collocates</p>", "<h3>Listening for Collocates</h3>", label="Ch17: Listening for Collocates")
maybe_replace("<p>Why Collocation Works Where Direct Statements Fail</p>", "<h3>Why Collocation Works Where Direct Statements Fail</h3>", label="Ch17: Why Collocation Works")
maybe_replace("<p>Collocation. Reading How a Person Connects Ideas</p>", "<h3>Collocation: Reading How a Person Connects Ideas</h3>", label="Ch17: Collocation heading")
maybe_replace("<p>The Four Principles of Translation</p>", "<h3>The Four Principles of Translation</h3>", label="Ch17: Four Principles heading")


# ========================================================================
# CHAPTER 18 — Contact Mind Reading: missing paragraph break
# ========================================================================
print("\n== Ch 18 ==")
# Find missing paragraph break inside the opening (heuristic)
maybe_replace(
    "There have been many effects where muscle reading is the method.\r\n\r\nMuscle reading, ideomotor response, hellstromism",
    "There have been many effects where muscle reading is the method.</p><p>Muscle reading, ideomotor response, hellstromism",
    label="Ch18: missing paragraph break",
)


# ========================================================================
# CHAPTER 19 — Hypnosis subheaders
# ========================================================================
print("\n== Ch 19 ==")
ch19_headings = [
    "Why People Find Hypnosis Hard to Believe",
    "Hypnotic Responsiveness vs. Compliance",
    "Pain as a Model for Understanding Hypnosis",
    "Oscillations and Timing",
    "A Useful Comparison to Alcohol, With an Important Warning",
]
for h in ch19_headings:
    maybe_replace(f"<p>{h}</p>", f"<h3>{h}</h3>", label=f"Ch19: {h}")


# ========================================================================
# CHAPTER 20 — Babel Count
# ========================================================================
print("\n== Ch 20 ==")
maybe_replace("<p>The Method</p>", "<h3>The Method</h3>", label="Ch20: The Method (note: also matches Ch24)")
maybe_replace("<p>Hiding the Method: The Season Reading</p>", "<h3>Hiding the Method: The Season Reading</h3>", label="Ch20: Hiding the Method")

# Days of week table
ch20_days_old = (
    "<p>01 — MONDAY | 6 letters</p>"
    "<p>02 — TUESDAY | 7 letters</p>"
    "<p>03 — WEDNESDAY | 9 letters</p>"
    "<p>04 — THURSDAY | 8 letters</p>"
    "<p>05 — FRIDAY | 6 letters</p>"
    "<p>06 — SATURDAY | 8 letters</p>"
    "<p>07 — SUNDAY | 6 letters</p>"
)
ch20_days_new = (
    '<div class="data-block days-block"><table class="tbl-days"><thead><tr><th>#</th><th>Day</th><th>Letters</th></tr></thead><tbody>'
    "<tr><td>01</td><td>MONDAY</td><td>6</td></tr>"
    "<tr><td>02</td><td>TUESDAY</td><td>7</td></tr>"
    "<tr><td>03</td><td>WEDNESDAY</td><td>9</td></tr>"
    "<tr><td>04</td><td>THURSDAY</td><td>8</td></tr>"
    "<tr><td>05</td><td>FRIDAY</td><td>6</td></tr>"
    "<tr><td>06</td><td>SATURDAY</td><td>8</td></tr>"
    "<tr><td>07</td><td>SUNDAY</td><td>6</td></tr>"
    "</tbody></table></div>"
)
must_replace(ch20_days_old, ch20_days_new, label="Ch20: days-of-week table")


# ========================================================================
# CHAPTER 21 — Psychological Forces (heading-only fixes; full rebuild deferred)
# ========================================================================
print("\n== Ch 21 ==")
# Wrap the orphaned <p>21A</p> sub-chapter marker
maybe_replace("<p>21A</p>", '<p class="subchapter-marker">21A</p>', label="Ch21: 21A marker style")

# Promote the subheaders that exist as <p>
ch21_headings = [
    "The ‘My Favorite’ Force",
    "Forcing a Single Word",
]
for h in ch21_headings:
    maybe_replace(f"<p>{h}</p>", f"<h3>{h}</h3>", label=f"Ch21: {h}")

# Fix the two h3 tags wrapping heading + body together
maybe_replace(
    "<h3>HOW FORCES COMBINE\r\n\r\nMost psychological forces are not strong enough on their own",
    "<h3>How Forces Combine</h3>\n<p>Most psychological forces are not strong enough on their own",
    label="Ch21: HOW FORCES COMBINE split",
)
maybe_replace(
    "<h3>THE SIMPLEST WAY TO THINK ABOUT ALL 13\r\n\r\nAfter everything in this chapter",
    "<h3>The Simplest Way to Think About All 13</h3>\n<p>After everything in this chapter",
    label="Ch21: SIMPLEST WAY split",
)


# ========================================================================
# CHAPTER 24 — Phase Two/Three (additional)
# ========================================================================
print("\n== Ch 24 ==")
maybe_replace("<p>Phase 2 — Direct and Collect.</p>", "<h3>Phase Two — Direct and Collect</h3>", label="Ch24: Phase Two")
maybe_replace("<p>Phase 3 — Distance and Distancing</p>", "<h3>Phase Three — Distance and Distancing</h3>", label="Ch24: Phase Three")
maybe_replace("<p>Variations</p>", "<h4>Variations</h4>", label="Ch24: Variations")


# ========================================================================
# CHAPTER 25 — Zodiac (more headings)
# ========================================================================
print("\n== Ch 25 ==")
ch25_headings = [
    ("<p>When They Do Not Know Their Element</p>", "<h3>When They Do Not Know Their Element</h3>"),
    ("<p>The Alternative Opener</p>", "<h3>The Alternative Opener</h3>"),
    ("<p>The Repeat It Ploy Created by Jerry Sadowitz and Bob Farmer</p>", "<h3>The Repeat It Ploy (Jerry Sadowitz &amp; Bob Farmer)</h3>"),
    ("<p>TRULY IMPOSSIBLE FEELING ZODIAC DIVINATION</p>", "<h3>Truly Impossible-Feeling Zodiac Divination</h3>"),
    ("<p>“Watch Your Figure” by Chris Michael</p>", "<h3>“Watch Your Figure” by Chris Michael</h3>"),
    ("<p>The Figure Method: Working With the Spectator Who Doesn’t Know Zodiacs</p>", "<h3>The Figure Method: Working With the Spectator Who Doesn’t Know Zodiacs</h3>"),
    ("<p>Half-Year Split: The Rope Visualization</p>", "<h3>Half-Year Split: The Rope Visualization</h3>"),
    ("<p>Working the First Half (Capricorn, Aquarius, Gemini)</p>", "<h3>Working the First Half (Capricorn, Aquarius, Gemini)</h3>"),
]
for old, new in ch25_headings:
    maybe_replace(old, new, label=f"Ch25: {old[:40]}…")


# ========================================================================
# CHAPTER 27 — More numbered subsections
# ========================================================================
print("\n== Ch 27 ==")
ch27_subsections = [
    "01 — Early Commitment",
    "02 — Writing It Down",
    "03 — Selection By Trait",
    "04 — Hold To Account",
    "01 — Broaden The Time Frame",
    "02 — The Fairness Frame",
    "03 — ONE EXAMPLE, NOT THE KEY",
    "04 — Part Of The Environment",
]
for h in ch27_subsections:
    maybe_replace(f"<p>{h}</p>", f"<h4>{h}</h4>", label=f"Ch27: {h}")

ch27_more = [
    "Lines That Justify Choosing This Person",
    "Lines That Justify Doing This Before the Show",
    "Lines That Hide the Fact That the Earlier Contact Is the Method",
    "On-Stage Lines That Quietly Reinforce the Earlier Selection",
    "Lines That Make the Thought Feel In-the-Moment Even Though It Is Earlier",
    "Lines That Redirect the Spectator When They Give You the Wrong Answer",
]
for h in ch27_more:
    maybe_replace(f"<p>{h}</p>", f"<h3>{h}</h3>", label=f"Ch27 lines: {h[:30]}")


# ========================================================================
# CHAPTER 30 — Method Invisibility minor cleanup
# ========================================================================
print("\n== Ch 30 ==")
maybe_replace(
    "<p>Make Them Remember the Impossibility, not what led you there.</p>",
    "<h3>Make Them Remember the Impossibility — Not What Led You There</h3>",
    label="Ch30: Make Them Remember promote",
)


# ========================================================================
# CHAPTER 31 — More heading fixes
# ========================================================================
print("\n== Ch 31 ==")
# Dedupe duplicated "One concrete way to train this" paragraphs
maybe_replace(
    "<p>One concrete way to train this. Pick a point in the sequence about ten seconds before the reveal",
    "<p data-removed-dup=\"\"><!-- removed dup paragraph: One concrete way to train this -->Pick a point in the sequence about ten seconds before the reveal",
    label="Ch31: comment dup (variant A)",
)
# Better: actually remove the older variant fully if both still exist together
maybe_replace(
    "<p data-removed-dup=\"\"><!-- removed dup paragraph: One concrete way to train this -->Pick a point in the sequence about ten seconds before the reveal until the next reveal… stretch every micro-second between them as long as you can. After the reveal, breathe slower than you were before. The experience inside that gap teaches more than any word a teacher can give.</p>",
    "",
    label="Ch31: remove dup paragraph fully",
)


# ========================================================================
# CHAPTER 33 — Strolling
# ========================================================================
print("\n== Ch 33 ==")
maybe_replace("<p>Use Applause to Prime the Next Table</p>", "<h3>Use Applause to Prime the Next Table</h3>", label="Ch33: Use Applause")


# ========================================================================
# CHAPTER 34 — Day of Show / First 60 Seconds (additional)
# ========================================================================
print("\n== Ch 34 ==")
maybe_replace("<p>Day of Show</p>", "<h4>Day of Show</h4>", label="Ch34: Day of Show")
maybe_replace("<p>First 60 Seconds</p>", "<h4>First 60 Seconds</h4>", label="Ch34: First 60 Seconds")


# ========================================================================
# CHAPTER 36 — Weak vs Strong Testimonial
# ========================================================================
print("\n== Ch 36 ==")
maybe_replace("<p>Weak vs. Strong Testimonial</p>", "<h3>Weak vs. Strong Testimonial</h3>", label="Ch36: Weak vs Strong")


# ========================================================================
# CHAPTER 37 — Tribal Drives + Observable Signals dedup
# ========================================================================
print("\n== Ch 37 ==")
# leave the multiple Observable Signals/For the Performer headings alone; flagging only
maybe_replace(
    '<h3>Significance-Driven</h3>',
    '<h3>Significance-Driven</h3><!-- TODO[AUDIT]: Three repeated <h3>Observable Signals</h3>/<h3>For the Performer</h3> headings appear under each tribal drive (Significance/Approval/Acceptance). Consider collapsing to inline bold labels or restructuring as a 3-card grid. -->',
    label="Ch37: Tribal Drives TODO marker",
)


# ========================================================================
# CHAPTER 38 — dedupe closing aphorism if present in body
# ========================================================================
print("\n== Ch 38 ==")
ch38_dup_old = (
    "<p>The work that requires no ethical attention is the work that is not powerful enough to need it.</p>"
    "<hr class=\"section-break\" aria-hidden=\"true\"><p>The work that requires no ethical attention is the work that is not powerful enough to need it.</p>"
)
ch38_dup_new = (
    "<hr class=\"section-break\" aria-hidden=\"true\"><p>The work that requires no ethical attention is the work that is not powerful enough to need it.</p>"
)
must_replace(ch38_dup_old, ch38_dup_new, label="Ch38: dedupe closing aphorism")


# ========================================================================
# Global remaining sweeps
# ========================================================================
print("\n== Final sweeps ==")

# More alot variants (already done by pass 1, but check)
maybe_replace("alot", "a lot", label="Global alot (raw — last attempt)")  # word-bounded done in pass 1; this is fallback

# CSS for new classes (inject lightweight rules so the new tags display reasonably)
inject_css = """
/* Audit pass additions */
.tbl-vak { width: 100%; border-collapse: collapse; margin: 1.5rem 0; font-family: var(--sans); font-size: .92rem; }
.tbl-vak th, .tbl-vak td { padding: .55rem .7rem; border-top: 1px solid var(--rule); text-align: left; vertical-align: top; }
.tbl-vak thead th { font-weight: 700; color: var(--accent); border-bottom: 1px solid var(--rule); }
.tbl-vak tbody th { color: var(--ink); font-weight: 600; background: var(--bg-soft); }
.tbl-days { width: auto; border-collapse: collapse; margin: 1rem 0; font-family: var(--sans); font-size: .95rem; }
.tbl-days th, .tbl-days td { padding: .35rem .9rem; border-bottom: 1px dotted var(--rule); }
.tbl-days thead th { color: var(--accent); }
.five-c-chain { font-family: var(--sans); letter-spacing: .12em; text-transform: uppercase; font-size: .82rem; color: var(--muted); text-align: center; margin: 1.25rem 0 2rem; }
.five-c-chain strong { color: var(--accent); }
.tc-section { margin: .75rem 0; }
.tc-section-label { display: inline-block; font-family: var(--sans); font-size: .7rem; letter-spacing: .2em; text-transform: uppercase; color: var(--muted); margin-bottom: .25rem; }
.tc-attrs, .tc-tells { margin: .25rem 0 0; padding-left: 1.2rem; }
.tc-onstage { margin: .25rem 0 0; }
.type-card .tc-head { display: flex; align-items: baseline; gap: .6rem; margin-bottom: .35rem; }
.type-card .tc-letter { font-family: var(--sans); font-weight: 800; font-size: 1.4rem; color: var(--accent); }
.jumpnav { font-family: var(--sans); font-size: .85rem; letter-spacing: .04em; color: var(--muted); }
.jumpnav-label { font-family: var(--sans); font-size: .72rem; letter-spacing: .25em; text-transform: uppercase; color: var(--accent); margin: 1.5rem 0 .35rem; }
.subchapter-marker { font-family: var(--sans); font-weight: 800; font-size: 1.2rem; letter-spacing: .15em; color: var(--accent); margin: 2rem 0 .5rem; }
.emotion-list { margin: 1rem 0; }
.emotion-list dt { font-family: var(--sans); font-weight: 700; color: var(--accent); margin-top: .6rem; }
.emotion-list dd { margin: 0 0 .35rem 0; }
"""
must_replace(
    "/* ── print: stick to web styles, but hide back-to-top ── */",
    inject_css + "/* ── print: stick to web styles, but hide back-to-top ── */",
    label="Inject CSS for new classes",
)

SRC.write_text(content, encoding="utf-8")
print(f"\nWrote {SRC} — {len(content)} chars (was {len(original)}).")
print(f"Net change: {len(content) - len(original):+d} chars.")
