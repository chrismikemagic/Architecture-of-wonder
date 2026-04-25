"""Update the Table of Contents in the manuscript to match the new structure."""

MAIN = r'C:\Users\Chris\Architecture-of-wonder\manuscript-extracted.txt'

with open(MAIN, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find TOC start and end (between "TABLE OF CONTENTS" and "INTRODUCTION" actual section)
toc_start = None
toc_end = None
for i, line in enumerate(lines):
    if line.strip() == 'TABLE OF CONTENTS':
        toc_start = i
    if toc_start and line.strip() == 'INTRODUCTION' and i > toc_start + 5:
        # The actual INTRODUCTION section header (not TOC entry)
        toc_end = i
        break

print(f"TOC runs from line {toc_start+1} to {toc_end} (exclusive)")

new_toc = [
    'TABLE OF CONTENTS\n',
    'Page numbers will be finalized at layout. This manuscript is organized using heading styles. Use Word\'s automatic Table of Contents feature (References \u2192 Table of Contents) to generate a linked TOC with current page numbers.\n',
    'INTRODUCTION  \u2014  On Being the Person Who Admits What They Do\n',
    'What you are holding and why it exists. The Crystal City story. A note on sources and the two categories of evidence.\n',
    'PART ONE  \u2014  The Architecture of Wonder\n',
    'The neurobiology of performance. What is happening in the audience\'s brain and how to design for it.\n',
    'Chapter 1  \u2014  Designing for Reality\n',
    'Cognitive economy, metabolic efficiency, and predictive processing. The three properties of the brain that make wonder possible.\n',
    'Chapter 2  \u2014  The Five Forces of Attention\n',
    'Novelty, emotional relevance, social signal, unresolved uncertainty, and contrast. The five inputs the brain uses to decide what matters.\n',
    'Chapter 3  \u2014  Tension, Threat and the Window of Wonder\n',
    'Cortisol, productive tension, and the six visible indicators that tell you where the room sits inside the window.\n',
    'Chapter 4  \u2014  The Art of Anticipation\n',
    'Dopamine fires during the build, not the reveal. Why most performers are timing their shows wrong.\n',
    'Chapter 5  \u2014  Attention as a Weapon\n',
    'Inattentional blindness, change blindness, psychological marking, and why misdirection is a narrative problem, not a visual one.\n',
    'PART TWO  \u2014  Reading the Room\n',
    'Body language, cold reading, micro-expressions, and the art of extracting information before a single question is asked.\n',
    'Chapter 6  \u2014  Reading Body Language in Real Time\n',
    'The Five Cs, the T1\u2013T4 evidence tiers, the Three-Signal Rule, baseline-first methodology, and the complete framework for reading body language under pressure.\n',
    'Chapter 7  \u2014  The 80-Signal System\n',
    'Eighty observable signals organized by evidential tier. The Six-Category Radar and the 10-Second Scan.\n',
    'Chapter 8  \u2014  The Four Personalities That Change How You Perform\n',
    'Four communication styles, six blends, and how to adjust your approach to each in the first thirty seconds.\n',
    'Chapter 9  \u2014  The Volunteer\'s Brain\n',
    'Seven volunteer types, the cortisol contract, and how to manage neurological state on stage.\n',
    'Chapter 10  \u2014  The Eyes, the Face, and the Way Thought Leaks Out\n',
    'Eye access cues, facial expression clusters, and the behavioral tells that precede conscious awareness.\n',
    'Chapter 11  \u2014  The Micro-Expression Matrix\n',
    'The seven universal expressions, the Duchenne marker, the leakage hierarchy, and why clusters matter more than snapshots.\n',
    'Chapter 14  \u2014  The Language of Yes\n',
    'Pacing and leading, presupposition, yes sets, and the four degrees of certainty for delivering reads.\n',
    'PART THREE  \u2014  The Methods\n',
    'Technical methods, systems, and practical frameworks. How the tools work at the level of mechanics, psychology, and application.\n',
    'Chapter 15  \u2014  Closing the Barn Door\n',
    'Why the brain reduces impossibility to cheap explanations, and the specific language that closes the window before it opens.\n',
    'Chapter 25  \u2014  Memory Distortion\n',
    'How memory is reconstructed rather than recalled, and how to use that process to deepen the impact of any effect.\n',
    'Chapter 12  \u2014  Cold Reading, Warm Reading, and Thin Slicing\n',
    'The Forer effect, modality pacing, collocation analysis, and the honest account of what each technique is and is not.\n',
    'Chapter 13  \u2014  Contact Mind Reading\n',
    'Muscle reading, ideomotor response, and how to extract information through physical connection without a single verbal cue.\n',
    'Chapter 16  \u2014  How Hypnosis Really Works\n',
    'What hypnosis actually is at the network and cellular level. Neuromodulators, oscillations, and why suggestion can feel involuntary.\n',
    'Chapter 26  \u2014  The Babel Count\n',
    'Counting the letters in a thought they never wrote down. The timing method, body-language backup, and the birthday application.\n',
    'Chapter 27  \u2014  Psychological Forces\n',
    'How to steer a free choice without asking for one. The mechanics of influence that operate below the threshold of awareness.\n',
    'Chapter 28  \u2014  Making Better Propless Mentalism\n',
    'What propless performance actually requires, and how to design effects that hold up with nothing in your hands.\n',
    'Chapter 24  \u2014  Propless Systems That Actually Work\n',
    'Understanding propless mentalism and being able to build it are different skills. This chapter is primarily about the second one.\n',
    'Chapter 29  \u2014  Zodiac Divinations Without Anagrams\n',
    'Clean approaches to zodiac and birth information that do not rely on anagram systems or dual-reality methodology.\n',
    'PART FOUR  \u2014  The Corporate Stage\n',
    'From pre-show intelligence to keynote halls to boardrooms. Behavioral science applied to the professional performance context.\n',
    'Chapter 17  \u2014  Pre-Show\n',
    'What happens before you walk on. The pre-show window, intelligence gathering, and the decisions that set every effect up to land.\n',
    'Chapter 18  \u2014  Mentalism in the Boardroom\n',
    'Executive audiences, the credibility sequence, and the real power map in any room.\n',
    'Chapter 19  \u2014  Why Most Training Fails\n',
    'Experience before explanation. Why most corporate training fails and how the performer advantage changes the equation.\n',
    'Chapter 19B  \u2014  The Digital Preshow\n',
    'Open source intelligence for the working performer. OSINT sources, Google dorking, corroboration, delivery protocol, and the ethical framework for intelligence-based reveals.\n',
    'Chapter 20  \u2014  Influence Without Authority\n',
    'Compliance vs. internalization, the self-attribution principle, and the reflection protocol for performance contexts.\n',
    'Chapter 21  \u2014  The Ethics of Influence\n',
    'The consent framework, the distress test, and where the line is drawn in performance, training, and volunteer work.\n',
    'Chapter 22  \u2014  The Intro Video\n',
    'Solving the most unreliable variable in corporate performance. Why most host introductions fail and how to fix them before you walk on.\n',
    'Chapter 23  \u2014  Introductions, Bios, and Testimonials\n',
    'Why most bios fail, the four-move bio structure, and what testimonials are actually for.\n',
    'PART FIVE  \u2014  Performance Craft\n',
    'The architecture of a full show. Structural choices, obedience dynamics, and the behavioral intelligence that governs every room.\n',
    'Chapter 30  \u2014  The Architecture of Obedience\n',
    'Why some rooms comply and others resist. The authority gradient, the compliance window, and how to design both into the structure of a show.\n',
    'PART EIGHT  \u2014  Behavioral Intelligence for the Stage\n',
    'Corporate behavioral intelligence frameworks adapted for the mentalist\'s stage. The science is identical. The application is sharper.\n',
    'Chapter 39  \u2014  What the Room Decides Before You Speak\n',
    'Focus, Authority, Tribe, Emotion. Four forces the limbic system evaluates before you speak, and how to control all four.\n',
    'Chapter 40  \u2014  Authority Architecture\n',
    'The five pillars of authority, the Milgram findings applied to performance, and the self-assessment that tells you which pillars need building.\n',
    'Chapter 41  \u2014  The Performer\'s Signal Dictionary\n',
    'The DRS system, three signal clusters (engagement retreat, evaluation, certainty drop), and the field notation system.\n',
    'Chapter 42  \u2014  How Influence Actually Works\n',
    'Novelty plus authority equals influence. Compliance architecture, the critical compliance window, and five speech patterns that build authority.\n',
    'Chapter 43  \u2014  Six Steps from Observation to Ovation\n',
    'Six steps from observation to installation. Detect, engage, calibrate, observe, decode, elevate.\n',
]

# Replace TOC section
new_lines = lines[:toc_start] + new_toc + ['\n'] + lines[toc_end:]

with open(MAIN, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"TOC updated. Replaced {toc_end - toc_start} lines with {len(new_toc)} lines.")
