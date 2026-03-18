#!/usr/bin/env python3
"""Insert new strolling content into Ch22."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

NEW_SECTIONS = """
Leaving Them Wanting More
Strolling is not only about what you show. It is about how you enter, how you frame the moment, how you choose who to involve, and how you leave. Those decisions often carry as much weight as the method itself.

On stage, the audience has already agreed to watch you. In strolling, you are stepping into a social environment that already has its own momentum, hierarchy, and emotional weather. It was there before you arrived.

That means the first job is rarely the trick. The first job is to make participation feel easy.

Leaving on the Reveal
Marcus Eddie taught me this, and I have not forgotten it: sometimes the strongest move after the reveal is to leave.

Not every time. Not with every effect. But with the right moment, especially a hard visual ending or a deeply personal climax, walking away can intensify the reaction rather than diminish it.

If you place an object in a spectator's hand, the temptation is to stand there and watch the realization happen. Many performers do exactly that. They stay in front of the moment as though their presence is required to certify it. Often it is not. In fact, it can weaken what follows.

A stronger approach: let the conditions settle, say something simple like, "My name is Chris Michael. Thank you so much for having me over here. I am going to let you discover this one on your own." Then step away.

The reason this works is social. When you remain in front of the volunteer, they are still inside the structure of the performance. There is still an expectation of behavior, even a subtle one. They are not only reacting to the effect. They are reacting while being observed by the person who created the conditions. That changes the emotional freedom of the moment.

When you leave, that pressure drops.

Without you as the center of gravity, the volunteer is suddenly free to gasp, laugh, stare, or fall silent without managing their reaction for your benefit. The response becomes less polished. It often becomes louder. And honest reactions travel further than polite ones.

There is also a second mechanism at work. When the emotional energy has nowhere immediate to discharge, it gets thrown outward. They turn to their friends. They call after you. They make noise across the room. You are not abandoning the moment. You are giving it room to finish itself.

Letting the Moment Belong to Them
One of the consistent mistakes in strolling is over-managing the payoff. You land a strong effect and immediately fill the space. You explain. You joke. You wait for the reaction you expected. In doing so, you often step on the strongest emotional beat.

Astonishment needs room.

Silence is not failure. Sometimes silence is the strongest possible evidence that the effect landed. When people are genuinely stunned, they do not always react in the tidy way performers expect. They freeze. They stare. They say nothing for several seconds because the brain is still catching up to what happened. That is not a flat reaction. That is often the most honest one you will ever see.

The performer who trusts the effect can leave the final beat alone long enough for the audience to own it.

Announce the Visit Before You Begin
One of the most reliable ways to lower resistance at a new table is to approach the group, acknowledge them, and then not begin.

A line like this works well: "Hey, I was asked to come over and show you all something, but I am being pulled away for just a moment first. I will be back in about two minutes. While I am gone, decide which one of you is the most unpredictable person in this group."

Then leave. Come back in two minutes.

This does several things at once. It frames your arrival as expected rather than intrusive. You are not a random interruption drifting into their space. You are there because someone arranged it. That single framing drops resistance before you have done anything.

It also gives them time to adjust to you before the performance begins. In strolling environments, resistance is rarely hostility. It is usually unpreparedness. People are mid-conversation. Their attention is already occupied. If you try to force a performance into that space too quickly, you create friction. If you give them a beat to prepare, that friction disappears.

Third, you create anticipation before the demonstration begins.

They start wondering what you are going to do. They begin talking about who the unpredictable one is. They start thinking about your return. By the time you come back, they are already partially inside the experience. The group is better. The attention is cleaner. The reactions are stronger. The entry feels earned instead of imposed.

The underlying principle is simple. A sudden request demands immediate adjustment. A delayed request allows the mind to begin preparing. That preparation lowers uncertainty and increases investment, because the group now has a small role in setting the conditions. They are no longer passive. They are already participating.

Sometimes the strongest opening move is to plant the hook and leave. Then return when the room has leaned toward you on its own.

Room Leader First
In any strolling set, the highest-leverage first impression is the one made on whoever is most visibly in charge.

If that person reacts well, the rest of the room reads it as permission.

People watch the behavior of high-status individuals to decide how they themselves should respond in unfamiliar situations. That is true at dinners, at conferences, and on strolling gigs. If the room leader laughs, leans in, or looks genuinely astonished, the room relaxes around you faster. You are no longer an unknown variable. You have been socially cleared.

There is also a practical version of this that works well at corporate events. Perform for the host or senior person first, then ask them to take you to the next group or the next person they would like to see experience it. They spent money to have you there. They know the room. They know who matters. If they bring you to someone and say, in effect, "You need to see this," you are arriving with an endorsement that no cold approach can replicate.

You are no longer a strolling performer moving table to table. You are someone the most important person in the room thought was worth introducing.

Use Applause to Prime the Next Table
Applause in strolling is not only for the group you are with. It is also information for the groups who are not with you yet.

After a strong moment, especially with a good volunteer, it can be worth having the group acknowledge what just happened while you take a small bow and say something like: "Give them a hand so the other tables know you had a good time."

That line does several things. It creates closure for the current group. It rewards the volunteer. It signals to nearby tables that something worth reacting to just happened. And it does all of that without asking for approval.

Rooms watch rooms. If one table is clearly having a good time, the next table becomes easier. That visible emotional evidence is part of how a strolling set spreads through a room.

Compliment the Group First
An underused strolling tool is a direct, genuine compliment aimed at the group before you ask anything of them.

A group that feels seen feels safer. A group that feels safe becomes easier to lead.

The compliment does not need to be heavy. "You all look like you are actually paying attention to each other" is more than enough. "I could already tell from across the room that this table had something going on." None of those lines feel manipulative if you mean them. All of them do useful work. They reduce the feeling that you are arriving to take something. Instead, it feels like you arrived because something good was already here.

Get Their Names
Names matter because they make the interaction real.

The moment you know someone's name, the performance becomes less generic and more relational. The spectator stops being a body used for procedure and starts being a person inside an experience. That shift happens faster than most performers expect, and it changes the emotional quality of everything that follows.

It also gives you more ways to steer attention, create callbacks, and guide the emotional tone of the set. A group warms up faster when it feels like you are actually with them, rather than simply performing at them.

Choose the Right Volunteer
The quality of the volunteer often matters more than the quality of the effect.

The wrong volunteer can flatten strong material. The right volunteer can elevate average material.

When you have a choice, pick the person who is most expressive, most emotionally available, and most likely to react honestly. Not always the loudest. Not always the most talkative. The person whose reaction will travel well through the room.

That reaction becomes social evidence for everyone watching.

If they respond big, the room feels bigger. If they respond flat, the room shrinks with it.

This is one more reason the two-minute approach works. It gives the group time to unconsciously surface the kind of person who will help the experience succeed. They are not only waiting for you. They are already organizing around the frame you left behind.

"""

with open('manuscript-extracted.txt', encoding='utf-8') as f:
    content = f.read()

# Insert after the Exit Principle section, just before the · · · separator
ANCHOR = ("The discipline of the early exit is the hardest skill in walk-around work and the"
          " one that separates professionals from hobbyists. Time your departure to the energy,"
          " not to your comfort.\n"
          "· · ·")
if ANCHOR in content:
    content = content.replace(
        ANCHOR,
        ("The discipline of the early exit is the hardest skill in walk-around work and the"
         " one that separates professionals from hobbyists. Time your departure to the energy,"
         " not to your comfort.\n"
         + NEW_SECTIONS +
         "· · ·"),
        1
    )
    print("Strolling content inserted.")
else:
    print("ANCHOR NOT FOUND")
    idx = content.find("discipline of the early exit")
    if idx >= 0:
        print(f"  Partial found at {idx}: {repr(content[idx:idx+150])}")

with open('manuscript-extracted.txt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done.")
