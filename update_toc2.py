"""Update TOC after moving Ch 17, 19B to Part 3 and merging Part 8 into Part 5."""

MAIN = r'C:\Users\Chris\Architecture-of-wonder\manuscript-extracted.txt'

with open(MAIN, 'r', encoding='utf-8') as f:
    lines = f.readlines()

toc_start = None
toc_end = None
for i, line in enumerate(lines):
    if line.strip() == 'TABLE OF CONTENTS':
        toc_start = i
    if toc_start and line.strip() == 'INTRODUCTION' and i > toc_start + 5:
        toc_end = i
        break

new_toc = """TABLE OF CONTENTS
Page numbers will be finalized at layout. This manuscript is organized using heading styles. Use Word's automatic Table of Contents feature (References \u2192 Table of Contents) to generate a linked TOC with current page numbers.
INTRODUCTION  \u2014  On Being the Person Who Admits What They Do
What you are holding and why it exists. The Crystal City story. A note on sources and the two categories of evidence.
PART ONE  \u2014  The Architecture of Wonder
The neurobiology of performance. What is happening in the audience's brain and how to design for it.
Chapter 1  \u2014  Designing for Reality
Cognitive economy, metabolic efficiency, and predictive processing. The three properties of the brain that make wonder possible.
Chapter 2  \u2014  The Five Forces of Attention
Novelty, emotional relevance, social signal, unresolved uncertainty, and contrast. The five inputs the brain uses to decide what matters.
Chapter 3  \u2014  Tension, Threat and the Window of Wonder
Cortisol, productive tension, and the six visible indicators that tell you where the room sits inside the window.
Chapter 4  \u2014  The Art of Anticipation
Dopamine fires during the build, not the reveal. Why most performers are timing their shows wrong.
Chapter 5  \u2014  Attention as a Weapon
Inattentional blindness, change blindness, psychological marking, and why misdirection is a narrative problem, not a visual one.
PART TWO  \u2014  Reading the Room
Body language, cold reading, micro-expressions, and the art of extracting information before a single question is asked.
Chapter 6  \u2014  Reading Body Language in Real Time
The Five Cs, the T1\u2013T4 evidence tiers, the Three-Signal Rule, baseline-first methodology, and the complete framework for reading body language under pressure.
Chapter 7  \u2014  The 80-Signal System
Eighty observable signals organized by evidential tier. The Six-Category Radar and the 10-Second Scan.
Chapter 8  \u2014  The Four Personalities That Change How You Perform
Four communication styles, six blends, and how to adjust your approach to each in the first thirty seconds.
Chapter 9  \u2014  The Volunteer's Brain
Seven volunteer types, the cortisol contract, and how to manage neurological state on stage.
Chapter 10  \u2014  The Eyes, the Face, and the Way Thought Leaks Out
Eye access cues, facial expression clusters, and the behavioral tells that precede conscious awareness.
Chapter 11  \u2014  The Micro-Expression Matrix
The seven universal expressions, the Duchenne marker, the leakage hierarchy, and why clusters matter more than snapshots.
Chapter 14  \u2014  The Language of Yes
Pacing and leading, presupposition, yes sets, and the four degrees of certainty for delivering reads.
PART THREE  \u2014  The Methods
Technical methods, systems, and practical frameworks. How the tools work at the level of mechanics, psychology, and application.
Chapter 15  \u2014  Closing the Barn Door
Why the brain reduces impossibility to cheap explanations, and the specific language that closes the window before it opens.
Chapter 25  \u2014  Memory Distortion
How memory is reconstructed rather than recalled, and how to use that process to deepen the impact of any effect.
Chapter 12  \u2014  Cold Reading, Warm Reading, and Thin Slicing
The Forer effect, modality pacing, collocation analysis, and the honest account of what each technique is and is not.
Chapter 13  \u2014  Contact Mind Reading
Muscle reading, ideomotor response, and how to extract information through physical connection without a single verbal cue.
Chapter 16  \u2014  How Hypnosis Really Works
What hypnosis actually is at the network and cellular level. Neuromodulators, oscillations, and why suggestion can feel involuntary.
Chapter 26  \u2014  The Babel Count
Counting the letters in a thought they never wrote down. The timing method, body-language backup, and the birthday application.
Chapter 27  \u2014  Psychological Forces
How to steer a free choice without asking for one. The mechanics of influence that operate below the threshold of awareness.
Chapter 28  \u2014  Making Better Propless Mentalism
What propless performance actually requires, and how to design effects that hold up with nothing in your hands.
Chapter 24  \u2014  Propless Systems That Actually Work
Understanding propless mentalism and being able to build it are different skills. This chapter is primarily about the second one.
Chapter 29  \u2014  Zodiac Divinations Without Anagrams
Clean approaches to zodiac and birth information that do not rely on anagram systems or dual-reality methodology.
Chapter 17  \u2014  Pre-Show
What happens before you walk on. The pre-show window, intelligence gathering, and the decisions that set every effect up to land.
Chapter 19B  \u2014  Digital Preshow
Open source intelligence for the working performer. OSINT sources, Google dorking, corroboration, delivery protocol, and the ethical framework for intelligence-based reveals.
PART FOUR  \u2014  The Corporate Stage
From keynote halls to boardrooms. Behavioral science applied to the professional performance context.
Chapter 18  \u2014  Mentalism in the Boardroom
Executive audiences, the credibility sequence, and the real power map in any room.
Chapter 19  \u2014  Why Most Training Fails
Experience before explanation. Why most corporate training fails and how the performer advantage changes the equation.
Chapter 20  \u2014  Influence Without Authority
Compliance vs. internalization, the self-attribution principle, and the reflection protocol for performance contexts.
Chapter 21  \u2014  The Ethics of Influence
The consent framework, the distress test, and where the line is drawn in performance, training, and volunteer work.
Chapter 22  \u2014  The Intro Video
Solving the most unreliable variable in corporate performance. Why most host introductions fail and how to fix them before you walk on.
Chapter 23  \u2014  Introductions, Bios, and Testimonials
Why most bios fail, the four-move bio structure, and what testimonials are actually for.
PART FIVE  \u2014  Performance Craft
The architecture of a full show. Structural choices, obedience dynamics, and the behavioral intelligence that governs every room.
Chapter 30  \u2014  The Architecture of Obedience
Why some rooms comply and others resist. The authority gradient, the compliance window, and how to design both into the structure of a show.
Chapter 39  \u2014  What the Room Decides Before You Speak
Focus, Authority, Tribe, Emotion. Four forces the limbic system evaluates before you speak, and how to control all four.
Chapter 40  \u2014  Authority Architecture
The five pillars of authority, the Milgram findings applied to performance, and the self-assessment that tells you which pillars need building.
Chapter 41  \u2014  The Performer's Signal Dictionary
The DRS system, three signal clusters (engagement retreat, evaluation, certainty drop), and the field notation system.
Chapter 42  \u2014  How Influence Actually Works
Novelty plus authority equals influence. Compliance architecture, the critical compliance window, and five speech patterns that build authority.
Chapter 43  \u2014  Six Steps from Observation to Ovation
Six steps from observation to installation. Detect, engage, calibrate, observe, decode, elevate.
"""

new_toc_lines = [l + '\n' for l in new_toc.split('\n')]
new_lines = lines[:toc_start] + new_toc_lines + lines[toc_end:]

with open(MAIN, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"TOC updated. Replaced lines {toc_start+1}-{toc_end}.")
