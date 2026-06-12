"""One-shot DOCX update — 2026-06-12 release-prep session.

1. Back up the DOCX to backups/
2. Remove the two "CHAPTER ROADMAP — SUGGESTED ADDITION" editorial notes (Ch16, Ch28)
3. Re-add [ITALIC] markers to the three Juke Box Oracle script paragraphs (lost in re-merge)
4. Insert Rado Sheytanov's "Ephemeris" + Christopher Parrish's "The Red Dwarf" into Ch25
5. Add a thank-you paragraph to ACKNOWLEDGMENTS
"""
import zipfile, shutil, os
import xml.etree.ElementTree as ET

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
ET.register_namespace('w', W)
ET.register_namespace('r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')

DOCX = 'Architecture-of-Wonder.docx'
BACKUP = 'backups/Architecture-of-Wonder.pre-contributions-20260612.docx'

shutil.copy2(DOCX, BACKUP)
print('backed up to', BACKUP)

with zipfile.ZipFile(DOCX, 'r') as z:
    names = z.namelist()
    contents = {n: z.read(n) for n in names}

root = ET.fromstring(contents['word/document.xml'])
body = root.find(f'{{{W}}}body')
paras = body.findall(f'{{{W}}}p')

def ptext(p):
    return ''.join(t.text or '' for t in p.iter(f'{{{W}}}t'))

def make_para(text):
    p = ET.Element(f'{{{W}}}p')
    r = ET.SubElement(p, f'{{{W}}}r')
    t = ET.SubElement(r, f'{{{W}}}t')
    t.set('http://www.w3.org/XML/1998/namespace' and '{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t.text = text
    return p

# ── 2. remove editorial roadmap notes ──────────────────────────
removed = 0
for p in list(body):
    if p.tag != f'{{{W}}}p':
        continue
    txt = ptext(p).strip()
    if txt == 'CHAPTER ROADMAP — SUGGESTED ADDITION' or txt.startswith('This chapter runs 6,100+ words') or txt.startswith('This chapter runs ~7,800 words'):
        body.remove(p)
        removed += 1
print('removed editorial-note paragraphs:', removed)
assert removed == 4, f'expected 4 removals, got {removed}'

# ── 3. [ITALIC] markers for Juke Box Oracle script ─────────────
JBO_STARTS = [
    'Imagine that you are at a bar one weekend.',
    'That’s interesting. The song you chose',
    'You could have been at a heavy metal bar',
]
marked = 0
for p in body.findall(f'{{{W}}}p'):
    txt = ptext(p).strip()
    for s in JBO_STARTS:
        plain = s.replace('’', "'")
        if txt.startswith(s) or txt.startswith(plain):
            ts = [t for t in p.iter(f'{{{W}}}t')]
            if ts and not txt.startswith('[ITALIC]'):
                ts[0].text = '[ITALIC]' + (ts[0].text or '')
                ts[-1].text = (ts[-1].text or '') + '[/ITALIC]'
                marked += 1
print('juke box paragraphs italic-marked:', marked)
assert marked == 3, f'expected 3 italic wraps, got {marked}'

# ── 4. Chapter 25 contributions ────────────────────────────────
EPHEMERIS = [
"EPHEMERIS: A PROP-LESS STAR SIGN DIVINATION",
"“Ephemeris” by Rado Sheytanov",
"While this book was in its final stretch, Rado Sheytanov sent me a routine and gave me permission to print it in full. I read it once and knew it belonged in this chapter. Ephemeris is his prop-less star sign divination. It avoids anagrams completely, the audience never hears a public miss, and the engine underneath it is the same set of skills you have been building since Part Two: hanging statements, real-time observation, and the discipline to let the script do the heavy lifting. His credits section at the end doubles as a reading list for this entire plot. Take it seriously. Thank you, Rado. Everything from here to the end of this section is his work, in his words.",
"Rado’s Introduction",
"I’ve always been fascinated by the star sign divination plot. There is something beautiful in meeting a stranger, elegantly reading their personality, and finishing off with the revelation of their zodiac sign. From a presentational standpoint, it feels like genuine mind reading because the information revealed is private, secret, and seemingly unknowable to the performer.",
"The routine you’re about to read is heavily inspired from Ultimate Star Sign Divination: The Fool Who Persists in Folly by the great Fraser Parker. While I highly appreciate Fraser’s foundational work, certain aspects of his method didn’t resonate with me. My attempts to refine these parts led to a significant breakthrough. I understood that we can utilize a plethora of reliable psychological techniques to subtly extract the spectator’s star sign without them speaking.",
"Ephemeris hinges on real body language principles. Rest assured, this is a perfectly reliable method, not a “bold” or risky one. It guarantees an accurate outcome every time, enabling you to genuinely convey the impression of getting inside the mind of the participant, provide insightful personality reading, and finish with the seemingly astonishing revelation of their zodiac sign.",
"My second direct source of inspiration was Lewis Le Val’s routine, Moonstone. While I admired the routine itself, I again found parts of the method, specifically the need to “fish” for information about the participant’s star sign, to be undesirable. This reinforced my initial goal: to devise a truly unique method. I relied on the understanding that people naturally reveal information, a trait hardwired into our evolution. Even top poker players and the toughest law-enforcement targets eventually show tells. Humans are excellent communicators, whether verbally or non-verbally. In fact, our non-verbal cues are quite clear and distinct, an evolved trait that aided our survival against Mother Nature’s challenges.",
"When developing Ephemeris, I imposed several strict guidelines. My primary goal was to create a prop-less routine that completely avoided anagrams or any physical/mechanical “outs” to determine the spectator’s star sign. I also insisted that the routine be versatile enough for various settings including close-up/walk-around, parlour, and stage. The theatricality of the process comes from genuine mind-reading techniques, allowing you to truly connect with the audience, making it suitable for any performance context. Therefore, the routine’s guaranteed 100% success relies heavily on a script that is not only simple, clear, and easy to follow but also robust enough to handle the core “heavy lifting” for you.",
"Furthermore, a primary goal was to ensure the routine was completely language-independent. Unlike many prop-less effects that rely on specific linguistic elements, I designed Ephemeris so I could seamlessly perform it in English — the common language where I am based in Ireland — as well as in Bulgarian, my mother’s tongue.",
"To an audience, the principles utilized in the composition you’re about to read look like the real thing. While these concepts are not my own — having been inspired by legends of mentalism such as Peter Turner, Michael Murray and Fraser Parker — I believe the way I’ve applied them here offers a fresh perspective on the plot. The aforementioned gentlemen require no introduction. I highly recommend every piece of work they have ever released, as their genius is undeniable. This material you are about to read would not exist without them.",
"The Experience",
"Following a brief exchange, the Mind Reader probes a stranger’s psyche to reveal intimate personality traits, culminating in the impossible divination of their star sign.",
"The Presentation",
"Assume the spectator’s name is Jessica and her star sign is Aries.",
"“Jessica, please concentrate on your star sign. Repeat it silently in your mind, over and over... like, ‘Capricorn, Capricorn, Capricorn’... Excellent, you’re doing well. Now, mentally shift the thought of your star sign to your subconscious mind, to the very back of your awareness. Do you notice the change? Before, you were actively thinking about your sign, but now that it’s in your subconscious, you can fully focus on our conversation. This focus is crucial, as it’s through our dialogue that I will find the best way to read you.”",
"“Some esoteric traditions hold that psychic mediums can use a person’s palms to forecast their future or offer personal life insights. While I don’t believe in anything spiritual or psychic, I trust that our hands can reveal far more answers than we’ve ever considered.”",
"“Would you mind bringing both of your hands forward for me, please? Palms up the sky. Perfect. If you were born in the first half of the year — January through June — think of your right hand. If you were born in the second half, think of your left hand. Tell me when you’re focusing on one of your hands.”",
"Jessica directs her focus to one of her hands.",
"“Jessica, only you can know, with complete and total confidence, which hand is currently on your mind, is that right?”",
"She naturally confirms that statement.",
"“Fantastic. Focus on that hand… You’re thinking of the left hand, but you’re giving equal weight of effort to the right, and I’m struggling to get a clear read on you.”",
"“In fact, let’s take this a step further. Jessica, I want you to focus intently on your star sign.”",
"She confirms.",
"“I’m getting the feeling that you’re a very loyal person. Even though you respect your opinion, I get the impression that you’re a people pleaser which leads me to think of the star sign Cancer.”",
"“I trust that I’m probably just picking up on several clear characteristics in your personality. But please, let’s get precise. Focus on the actual letters of your star sign...”",
"“Imagine that here, on your right palm [tap], are the signs: Aquarius, Pisces, Aries, Leo, Virgo, and Libra. And here, on your left [tap], are Taurus, Gemini, Cancer, Scorpio, Sagittarius, and Capricorn.”",
"“Okay, really concentrate on the hand holding your specific sign. Let me know when you’re ready.”",
"“Perfect. If you’re thinking of your right hand, I want you to see your star sign as a vivid symbol — like an image — right here in the space between us. But if you’re thinking of the left hand, I want you to see the name of your sign written out in the air.”",
"“I’m picking up on a real analytical streak in you — someone who has a natural connection to language. Let’s lean into that. Relax your hands for a second — just see your star sign in large, bold letters… Like PISCES [gesture to the air]. Make it massive. See every single letter as if it’s hovering right in front of you.”",
"After a few moments, the mentalist gets a feeling about Jessica and decides to tell her.",
"“Hmm… Actually... Just relax your hands. While you were focusing on your palms, I picked up on a specific duality in you. You have this analytical mind that strips things down to the bone, yet you can’t ignore the aesthetics of a situation. You have a sharp eye for detail. When a problem hits, you don’t just react — you calculate. You play it out like a game of chess, weighing every angle, but in the end, you always inject your own creativity to handle things your way. You know better than anyone that life is rarely black and white, so you never settle for the obvious answer. Even in your toughest moments, I feel you’re looking for the right path, not just the easiest one.”",
"The mentalist gave Jessica a moment to take in what he’d said. After a brief pause, she confirmed that he was right.",
"“Jessica, to be honest, this rarely happens. You have traits that seem to spill over the edges of a typical star sign. For a moment, I actually struggled — I was convinced you were an Aquarius because you’re so headstrong and organized. I almost went down the wrong path.”",
"“I had to really question my instincts, but I’m grateful you stayed focused. It allowed me to see past that first impression and look at the way you were actually projecting your thoughts.”",
"The mentalist holds her gaze, allowing the moment to sink in by locking eyes with her.",
"“Taking everything I’ve seen into account... I can confidently say that you’re an Aries, yes?”",
"Jessica is left completely flabbergasted — so stunned that she nearly falls off her chair. The routine is over, and her brain is officially broken. The End.",
"Essence of the Methodology",
"While it might look like there are a hell of a lot of moving parts, the script is so tightly woven that you can nail the entire routine in under three minutes if you desire. Or even less if you decide to exclude the reading.",
"That said, I strongly suggest you don’t skip the personality read. It’s what transforms a basic zodiac reveal into something that feels genuinely profound. The reading isn’t mandatory, but it’s the soul of the routine. Don’t be lazy — perform it, and it will sell the entire premise.",
"Let’s tear this apart piece by piece. Since this is entirely prop-less, you need to rehearse every single line until it’s burnt into your muscle memory. Before you even think about putting this in your own words, you have to understand the mechanics inside and out. If you’re stuttering or second-guessing your delivery in the middle of the performance, the illusion of “real” mind reading vanishes.",
"In essence, you would be using hanging statements and real-time observation techniques to funnel twelve possibilities down to exactly three. This process is completely invisible, buried under the ruse of you “struggling” to establish a connection with the spectator. While the audience thinks you’re having a hard time, you’ve already done the heavy lifting. Once you’ve whittled it down to those three, you’ll use a few verbal principles and ploys to elegantly dismiss the outliers, leaving you with the one sign that belongs to the spectator.",
"I hope you’ll love this routine as much as I do. Let’s dive straight into Ephemeris!",
"The Explanation",
"“Jessica, please concentrate on your star sign. Repeat it silently in your mind, over and over... like, ‘Capricorn, Capricorn, Capricorn’...”",
"The routine kicks off by introducing the main idea and simultaneously exploring how people take in information. A slightly cheeky element is the use of Jerry Sadowitz’s “Repeat it” ploy to immediately deal with and discard one of the two “problematic” zodiac signs: Capricorn. (We’ll handle the other tricky sign, Cancer, later in the script.)",
"Note: While Sadowitz came up with the “Repeat it” ploy, Derren Brown made it popular in his routine “Smoke,” found in his book Pure Effect.",
"If your participant is a Capricorn, you’ve just pulled off a miracle: an instant and flawless guess of their star sign. If this happens, feel free to end the routine right there and take full credit for the hit. If, however, the participant doesn’t react to Capricorn, you can smoothly move right into the main Ephemeris process.",
"“Some esoteric traditions hold that psychic mediums can use a person’s palms to forecast their future or offer personal life insights...”",
"This serves as the opening of the presentation and provides the rationale for bringing the participant’s palms into the experiment.",
"“Would you mind bringing both of your hands forward for me, please? Palms up the sky...”",
"This is where you start the binary process of cutting the zodiac in half using the participant’s palms.",
"Note: I strongly suggest tapping each of the participant’s palms while giving instructions. I’ve found that this tactile moment — touching their palms as you tell them what to do — makes the steps they need to follow much clearer and more concrete.",
"“Jessica, only you can know, with complete and total confidence, which hand is currently on your mind, is that right?”",
"This sentence is super important. It takes what seems like a simple 50/50 choice and makes it feel personal and also uncertain for you, the performer. You absolutely have to emphasize that only the spectator knows for sure which hand they’re thinking of.",
"“Fantastic. Focus on that hand… You’re thinking of the left hand, but you’re giving equal weight of effort to the right, and I’m struggling to get a clear read on you.”",
"This section of the script incorporates the “Hanging Statement.” My inspiration for employing this concept stems from Pete Turner’s masterful contribution to hanging statements, particularly in the context of reliably knowing a binary outcome.",
"Say, “You’re thinking of the left hand” with a split-second pause and a slight nod. If there’s no reaction, immediately add “but” and finish the sentence as described above. The word “but” psychologically links the statement, making it feel seamless. The spectator would be left with the impression that you are struggling to read them, but you’ve already gained a significant advantage by slicing the zodiac in half.",
"“In fact, let’s take this a step further. Jessica, I want you to focus intently on your star sign.”",
"First, you establish the struggle to connect with the participant, making this difficulty clear. Then, you abruptly transition to acting as if you are now receiving a strong impression about them.",
"“I’m getting the feeling that you’re a very loyal person... which leads me to think of the star sign Cancer.”",
"This step involves delivering another hanging statement in the form of a seemingly insightful Barnum statement that masks itself as a definitive observation. The goal is to offer a quick intuitive reading of the spectator’s personality. Crucially, this stage also serves to eliminate the problematic Cancer sign from consideration. To execute this, look away from the participant for just a fraction of a beat, then you should pronounce the word “Cancer” while directing your gaze back at them, offering a slight smile and a nod. Observe their reaction closely. If the spectator shows no response, you can safely conclude they are not a Cancerian, and you are free to proceed with the remaining steps of the Ephemeris process.",
"“I trust that I’m probably just picking up on several clear characteristics in your personality. But please, let’s get precise...”",
"Here, we provide a logical explanation of the reading and the dismissal of the star sign Cancer, which closes the psychological loop we put the spectator into.",
"“Imagine that here, on your right palm [tap], are the signs: Aquarius, Pisces, Aries, Leo, Virgo, and Libra. And here, on your left [tap], are Taurus, Gemini, Cancer, Scorpio, Sagittarius, and Capricorn.”",
"As you may have already observed, the star signs are assigned to the participant’s hands in a very specific manner. On their right palm are the first three star signs of the first half of the year and the first three signs from the second half of the year. The same arrangement applies to their left hand. Feel free to reread this if necessary.",
"“Okay, really concentrate on the hand holding your specific sign. Let me know when you’re ready.”",
"It is imperative that we allow the spectator ample time to consider the hand holding their star sign. Rushing this stage is strictly forbidden. If the spectator mistakenly associates the star sign with the wrong hand, it will prevent us from successfully divining their sign later on. As is standard practice, particularly in prop-less mentalism, we must always ensure with absolute certainty that the participant is clearly following all instructions we are giving them.",
"“Perfect. If you’re thinking of your right hand, I want you to see your star sign as a vivid symbol — like an image — right here in the space between us. But if you’re thinking of the left hand, I want you to see the name of your sign written out in the air.”",
"I call this a “Thought Assignment.” We simply observe the participant’s reactions as they follow our instructions. If you see them attempting to visualize an image when you deliver the first part of the script, you know for certain they are focusing on the right hand. Conversely, if they show no reaction when you deliver the script about the right hand, then you know they will be thinking of the left. Include a slight pause and a nod between those sentences to signal to the spectator that they should perform the mental task you’ve assigned them.",
"Note: Most spectators will not have a visual image of their star sign in mind. While some do, I have found that when a participant takes longer to construct an image of their sign, they also take longer to think, which provides a clear and distinct tell that they are thinking of their right hand. In that situation, simply look away and continue with the rest of the script. This subtlety reinforces the idea that you are not watching their reactions, even though you are, and have already narrowed the possibilities to two or three.",
"There’s no trick to this. Just monitor them smoothly as you deliver that script, and their reaction will clearly show which hand they are focusing on.",
"Note: Once the participant has a clear reaction, simply look away until they’re done. This helps dismiss the potential idea that you’re psychoanalyzing them. This subtlety also helps to further cement the idea that you really shouldn’t know what is happening inside their mind.",
"At this stage, you will have narrowed the possibilities down to either two or three potential signs, based on the half of the year the participant was born (since the problematic Cancer and Capricorn have been eliminated). In our specific example, we are left with Aquarius, Pisces, and Aries.",
"“I’m picking up on a real analytical streak in you — someone who has a natural connection to language. Let’s lean into that... Like PISCES [gesture to the air]...”",
"This is my personal iteration of Michael Murray’s “Self Referral” technique from his excellent work, Isolation. As it’s not mine, I won’t explain the full details here, but the core idea is to guide the participant into seeing their star sign as a word, even if they initially perceive it as an image. This is crucial for the subsequent filtering process. I justify this by suggesting the spectator is inherently better at perceiving words than images. Crucially, as the performer, we are the ones sharing these impressions and defining what the spectator excels at!",
"We’ve also included Pisces, as you noted, as an example to show the spectator how to focus on their sign. However, as we make a gesture for Pisces in the air, we will smile slightly and nod. If the spectator is indeed a Pisces, they will react positively. At this point, we can confidently conclude the routine and take full credit for directly reading their mind. Otherwise, if we observe no reaction, we merely continue with the rest of the Ephemeris process.",
"Note: I first encountered this technique while studying Pete Turner’s Isabella Star 3.",
"From this moment and onwards we know that the spectator is either Aquarius or Aries.",
"“Hmm… Actually... Just relax your hands. While you were focusing on your palms, I picked up on a specific duality in you...”",
"The reading of the participant’s personality is a big moment. While you don’t have to do it, I always include this because it helps the participant stop thinking about the stuff that just happened. By getting them to focus on themselves instead of the procedure, the whole psycho-mechanical setup they just went through just becomes a way to figure out the best approach for their reading. Basically, the reading makes the process they went through disappear. After the final reveal, it should feel like you were just chatting, with a few requests to focus on specific things. Even though the Ephemeris process is well disguised within the script, this verbal switcheroo helps the spectator forget the nuts and bolts of the method.",
"Note: Like I said, the reading itself isn’t required. I’m offering this stock line as an example, but if you’re an experienced reader, totally feel free to change it up or expand on it based on the person you’re with. Once you really get the method, I strongly suggest you tweak the whole Ephemeris routine to fit your own performing vibe and personality.",
"“Jessica, to be honest, this rarely happens. You have traits that seem to spill over the edges of a typical star sign. For a moment, I actually struggled — I was convinced you were an Aquarius because you’re so headstrong and organized. I almost went down the wrong path.”",
"This is another hanging statement disguised as a reading. Once you pronounce the word “Aquarius,” you need to offer a slight smile and nod, then wait for a fraction of a second. If they react, you end the routine and take your bow. However, if they don’t react, you complete the sentence with the certain knowledge that they are an Aries.",
"Important note: The Ephemeris process was meticulously designed to enable you to divine a stranger’s star sign. It was paramount for me to avoid many of the common verbal ploys, techniques, and reductive processes so that I could reserve them for use in other routines with the same audience. However, if you prefer, once you’ve narrowed it down to two or three possible star signs, you can then employ the known techniques and verbal reductive processes to eliminate the remaining options and reveal the spectator’s true sign. This remains a matter of personal choice. Should those techniques be absent from your current toolbox, I strongly urge you to thoroughly study all the works detailed in the Credits and Inspiration section.",
"“Taking everything I’ve seen into account... I can confidently say that you’re an Aries, yes?”",
"Additional Thoughts from Rado",
"Ephemeris can be integrated into various mentalism routines. For example, I have used it as a substitute for the RAISE anagram element in Peter Turner’s Isabella Star 3. On some occasions, when performing Pete’s Isabella Star 2 (the version that incorporates the astrological number), Ephemeris was employed to divine the participant’s zodiac sign, which subsequently allowed me to deduce their full date of birth.",
"Furthermore, Ephemeris offers a modern twist to older routines. I previously used Fraser’s Oculus 2 for years, but now combining Oculus 2 with Ephemeris breathes new life into the original concept.",
"Once you perform Ephemeris, you will recognize that the underlying methodology is a simple “which hand” technique, elevated by clever scripting. This realization opens up the possibility of applying the Ephemeris method to divine any linguistic category with a limited number of possibilities, not just star signs.",
"Ephemeris is a complete effect on its own, but its flexibility allows for integration with other routines. You can easily blend its method and script with your preferred prop-less routines. Alternatively, you can use Ephemeris as a compelling introduction to any psychological force that carries a degree of risk. In this context, a “failed” psy-force can be framed as a deeper exploration of the participant’s psyche, which ultimately amplifies the power of the subsequent star sign divination.",
"Once you’ve narrowed it down to two potential star signs, instead of relying on the hanging statement I provided in the script, or any other reductive/filtering methods, you can employ Mitch Kettlewell’s “Coupling” principle. This will allow you to elegantly dismiss one of the remaining signs and pinpoint the one that belongs to the spectator. To delve deeper into the “Coupling” principle, I highly recommend acquiring Mitch’s excellent project, Streamlining the Signs, which is packed with brilliant material, including an insightful jam session with the one and only Peter Turner.",
"An elegant alternative for the final two-sign reduction is a verbal technique borrowed from “Ouija Name Guess” by Ross Tayler (featured in Fraser and Ross’ Kings Will Never Die project). By reversing the logic of the letter ploy used in that routine, you can subtly dismiss one of the two remaining star signs, leaving only the spectator’s true sign.",
"If you’re concerned about accurately reading the participant during the second phase — where they’re silently considering their star sign hand — you can simply turn away and cover your eyes, performing the Gypsy Peek. Instruct the participant to close the hand containing their star sign into a fist, while concentrating on their sign. Once you’ve obtained your peek, ask them to close the other hand into a fist as well, justifying this by explaining it will amplify their natural expressions and overall body language for a better reading. When they are ready, you can turn back and “open” your eyes, now fully confident that you have narrowed the possibilities down to three or (in some cases) two signs. From this point, you can elegantly continue the final reductive process to reveal their exact star sign.",
"Credits and Inspiration",
"This work is heavily influenced by and owes a debt of gratitude to the following creators and their foundational contributions to the field:",
"1. Parker, Fraser. Ultimate Propless Star Sign Divination – The Fool Who Persists in Folly (2018).",
"2. Le Val, Lewis. Moonstone (2025).",
"3. Murray, Michael. Isolation (2017).",
"4. Murray, Michael. A Piece of My Mind (2014).",
"5. Turner, Peter. Mentalism Masterclass: Vol. 2 – Readings (2015).",
"6. Turner, Peter. Mentalism Masterclass: Vol. 9 – Astrological/Zodiac Based Mindreading (2016).",
"7. Turner, Peter. Isabella’s Star 2: The Star Goes Supernova (2013).",
"8. Turner, Peter. Isabella’s Star 3 (2017).",
"9. Kettlewell, Mitchell; Turner, Peter. Streamlining the Signs (2019).",
]

RED_DWARF = [
"THE RED DWARF",
"“The Red Dwarf” by Christopher Parrish",
"The second contribution in this chapter comes with a story attached: Christopher Parrish originally wrote The Red Dwarf for Rado, and he sent it to me so I could share it with you. It answers the question that stops most performers from ever trying bold propless work in front of a real audience. What happens when I miss? Christopher’s answer is to keep a secretly harvested star sign in your back pocket, so that the miss itself becomes evidence you can read people. Thank you, Christopher. His work follows, in his words.",
"Christopher’s Introduction",
"I love propless Mentalism. However, I’m extremely mindful of the propless tools, principles, effects, and routines I integrate into my professional repertoire. These days, I’ve come to the simple conclusion that if a propless piece of Mentalism can’t allow me to be artistically expressive with the information I’m hoping to divine, and if the procedure can’t be done quickly, is well-justified, and done at the very start of the effect, I don’t touch it. For my tastes, I like propless Mentalism that can act the same as a billet: get the “necessary evil” over and done with at the very start, and the rest of my time is spent creating a unique and emotionally resonant reveal.",
"This is why propless name and word divinations are a big no-no for me. Not because they don’t work, but because I don’t like the aesthetic of spending the closing moments of the revelation trying to fish for letters, using the CUPs principle, or resorting to methods like the Repeat It ploy. I tend to gravitate toward propless principles and effects that can be easily framed as reading systems, and I follow a very simple rule. In fact, the rule is so simple that many propless mentalists forget to include it!",
"Note: Many of them do, indeed, “work.” Now, can they take the participant on the same level of emotional and imaginary journey compared to a name reveal using a billet? In most cases, no! They often treat the name as an arbitrary piece of information, rather than as it being a part of a human being’s identity. And, even if mentalists don’t agree with this, the way they divine information certainly does.",
"“The intended purpose of the propless effect should still be worth an audience’s time, attention, and money. If the deceptive method were to ‘fail,’ the participant is still gifted with a worthwhile experience.”",
"This is why I love propless star sign and date-of-birth effects so much. If I notice the most subtle feeling that something went wrong during the procedural part of the method, there’s still no harm done! I simply offer my participant their reading, make it an insightful and beautiful experience, and we go about our merry way! I don’t bother divining the star sign and/or the date of birth, and, most importantly, my participants are never led to believe my intention was to go down that route. I don’t mind failure. What I do mind is building a revelation to a climax only for the final revelation to fall flat. Failures should be minimal, carefully constructed, and designed to increase credibility.",
"For those who may have skeptical thoughts about propless Mentalism, this approach may be of use to you. This approach will allow you to experiment with any propless piece that piques your fancy, and in the event that the piece goes wrong, you’ll share with your participant a justified (and mysterious) reason as to why the demonstration failed. Other mentalists have shared lines for covering a miss when performing a bold piece of Mentalism. My only “issue” with some of these lines is that it can take awhile for the mentalist to “prove” their claim is genuine. Without a harvested piece of info as your backup, you have to take out your billets or prop, introduce the premise, go through the method’s procedure, get them to write something down, peek it, and segue into your reveal. This can be time wasted if the failure of the bold, propless Mentalism effect decreases belief and engagement among your participants and audience members. Also, these vague safety-net lines, I’ve found the hard way, don’t work if the expectation created from the failed propless Mentalism effect was of you attempting to read the participant’s mind.",
"To me, when delivered badly, such scripts sound like schoolchildren bragging about doing a cartwheel but saying their arm is a bit sore, so they can’t do one at that moment. Such excuses within Mentalism also remind me of old friends of mine in elementary school who would brag about having a girlfriend, but say she “goes to another school.” Such excuses only really work on laymen if they already believe, and have PROOF, that the mentalist can, indeed, read minds. Rarely is this ever the case when a mentalist decides to use an ethereal and risky piece of Mentalism as their opener!",
"These days, I most often use my Red Dwarf technique when I want to perform something bold, which can’t be justified as a propless reading system, and I don’t mind failing. I pair my Red Dwarf technique with propless effects such as Peter Turner’s Wish You Were Here and his Phantom Dictionary Test, and Nico Heinrich’s Cocaine and Lego Piece. To learn more about my theories and opinions on propless Mentalism, I suggest purchasing my e-book, The Dangerous Allure of Propless Mentalism, which also contains my purely propless date-of-birth divination, The Ring of Light.",
"How It Works",
"For my style, taste, and preference, I tend to use a quick general reading as my opening “getting-to-know-you” effect, before advancing my performance to direct, bold, and propless mind-reading. I make the general reading quick, entertaining, and not very insightful, so the reading doesn’t move into Q&A. My opening general reading, when I want to move into an effect that’s framed as direct mind-reading, and not completely sure-fire, is treated as a fun personality test, more than anything else. I do this because I love readings, I like keeping my performances as minimal as possible, and it’s the most covert way I know to bank the information I need to make The Red Dwarf work: a star sign. You can also secretly discover a person’s star sign via discrete observation, an Additional Information Billet, or even getting the participant to choose their star sign from a marked zodiac deck you carry for readings and esoteric experiences.",
"Rather than divining a star sign you’ve harvested from a participant mere seconds after learning it, save it for later. When, during your performances, you’ve mentally prepared yourself to personally road-test a risky piece of propless Mentalism, proceed as usual. Let’s say your series of Hanging Statements and Fishing has led you to believe your participant is thinking of the name, “Steve.” However, at the moment of truth… the participant says aloud that they were thinking of their father… “Mike.” Rather than spew out your ten-minute tangent on how “mind-reading doesn’t work on everyone,” I would suggest keeping your cool, pausing for a moment, and saying:",
"[ITALIC]“It’s interesting that I couldn’t pick up on the fact that your father’s name is Mike. I don’t want to make tasteless excuses, but there is one group of people I simply can’t read. I should have asked you this question before we began this demonstration; however, given that I guessed incorrectly about your father’s name, there’s no doubt how you would have answered. Peyton, be honest with me… you’re a Capricorn, correct?”[/ITALIC]",
"From this point on, you can now easily and comfortably segue into any sure-fire routine you’ve prepared for the group!",
"The Group Variation",
"This minor variation to the Red Dwarf is great when, within a group context, you intuitively feel to perform a bold piece of Mentalism for one individual, but have secretly harvested the star sign from another. The scripting begins in the same way as in the original, but with a slight twist:",
"[ITALIC]Mentalist: “It’s interesting that I couldn’t pick up on the fact that your father’s name is ‘Mike.’ I don’t want to make tasteless excuses, but there is one group of people I simply can’t read… What’s your star sign?”[/ITALIC]",
"[ITALIC]Participant: “I’m a Capricorn, why?”[/ITALIC]",
"[ITALIC]Mentalist: “Ahh, I fucking thought so! For whatever reason, Capricorns are people I simply can’t read! That must explain why my ex always mentioned I was always clueless about her needs…”[/ITALIC]",
"The performer brings his attention to another person (the one whose star sign has been secretly harvested).",
"[ITALIC]Mentalist: “You, on the other hand, I feel I can receive thoughts a lot easier than with your friend. I say this for one reason: just a ‘yes or no,’ are you a Capricorn?”[/ITALIC]",
"The newly chosen participant answers in the negative.",
"[ITALIC]Mentalist: “Hahah, thank Christ! I thought so! Just to ensure my calibration is correct this time, you’re a Virgo, correct?”[/ITALIC]",
"After this super clean and phenomenal hit on a stranger’s star sign, the mentalist segues into a routine he knows will not only work, but knock the socks off everyone in the group!",
"Closing Thoughts on The Red Dwarf",
"A lot of propless Mentalism is experimental and expensive, so it’s important that if you do take the plunge into learning more about the subject, you have a professional-grade technique to experiment with what you’re learning without your reputation as a mentalist being at risk. The Red Dwarf has been a trusty ally during moments when I woke up feeling bold and wanting to masterfully divine the very thoughts of my participants without needing anything written down or typed into an app.",
"By having a trusted safety net ready to go anytime you want to experiment with something bold and not sure-fire, you’ll be able to include such propless Mentalism effects into your performances more often. And, as a result, you’ll be quickly on your way to developing, road-testing, and creating your own style of propless Mentalism that fits your voice, character, and comfort level. That is the power and level of creative freedom techniques like The Red Dwarf offer to mentalists. A way to experiment with new ideas without the risk of giving your participants and audiences an embarrassing and boring experience.",
"Always remember, failures can be powerful; they just have to be carefully considered where they can occur in the demonstrations of a real, empathetic, and professional mentalist. At their best, failures increase credibility and make the performer appear more human and relatable to the audience. At their worst, they decrease engagement, cause audiences to not take the performer seriously, and the mentalist comes across as some jackass who THINKS they can read minds. Don’t be the jackass.",
]

ACK = ("To Rado Sheytanov and Christopher Parrish, thank you for contributing original material to the zodiac chapter of this book. "
       "Rado allowed me to print Ephemeris, his prop-less star sign divination, in full. Christopher did the same with The Red Dwarf, "
       "the safety-net technique he originally wrote for Rado. Generosity like that is rare in this art, and I am grateful to you both.")

children = list(body)

def find_index(predicate, label):
    for i, el in enumerate(children):
        if el.tag == f'{{{W}}}p' and predicate(ptext(el).strip()):
            return i
    raise SystemExit(f'ANCHOR NOT FOUND: {label}')

# Ch25 anchor: last paragraph of the chapter body before the closing section break
ch25_i = find_index(lambda t: t.startswith('The person who doesn') and 'frame of reference for how possible' in t, 'ch25 end')
for offset, text in enumerate(EPHEMERIS + RED_DWARF, start=1):
    body.insert(ch25_i + offset, make_para(text))
print('inserted', len(EPHEMERIS) + len(RED_DWARF), 'paragraphs into Ch25')

# Acknowledgments anchor (re-list children after insertion)
children = list(body)
ack_i = find_index(lambda t: t.startswith('I also want to acknowledge Patrick Redford'), 'acknowledgments')
body.insert(ack_i + 1, make_para(ACK))
print('inserted acknowledgments paragraph')

# ── write back ─────────────────────────────────────────────────
out = ET.tostring(root, xml_declaration=True, encoding='UTF-8')
with zipfile.ZipFile(DOCX, 'w', zipfile.ZIP_DEFLATED) as z:
    for n in names:
        z.writestr(n, out if n == 'word/document.xml' else contents[n])
print('DOCX rewritten OK')
