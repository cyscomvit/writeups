---

layout: writeup

title: The Missing RV
difficulty: Hard
points: 500
categories: [OSINT]
tags: []

## flag: CYS{5SUR_MEGASORIANA_PUEBLA_ABANDONED}

The Missing RV

Author: Nekkanti Aishani

This is an OSINT-based CTF challenge where players must investigate hidden information, online identities, GitHub history, deleted files, social-media clues, travel locations, Wi-Fi information, and geographic evidence to determine the final location of the missing RV.

Firstly, we inspect the given image:

We are initially given an image of an RV. Since the supplied file is an SVG, we inspect the source/contents of the file rather than treating it only as an image.

After examining the SVG source, we find a hidden identifier:

[jpinkman04]

Finding Jesse:

Searching the discovered identifier leads us to Jesse's online presence. From the account, we establish the identity as Jesse Pinkman and begin examining the available repositories.

The GitHub account contains several repositories, but most appear to be ordinary personal material. The relevant repositories are:

notes
projects
archive

https://github.com/jpinkman04

The 4 April clue:

Inside the notes repository, we find a reference to 4 April. At this point, the date does not appear to mean much by itself, so we retain it as a potential clue.

Inspecting Git history:

The important information is not visible in the current version of the archive repository. Looking through the commit history, we find the commit "remove temporary information".

Inspecting the changes shows that notes/old-contact.txt was deleted. Recovering the deleted file gives us:

old contact
jpink 4 april
don't keep this around.

This confirms that jpink and 4 April are connected.

Following the Jane connection:

The 4 April clue leads us to Jane. Jane's fictional Mosaic profile contains a post associated with April 4:

April 4

met the guy next door properly today. we ended up talking for way longer than either of us planned. weird how some people are easier to talk to than you'd expect.

This establishes a connection between Jane and Jesse and gives context to the previously unexplained date.

Finding Andrea:

Returning to Jesse's Mosaic profile, we find a comment containing another unique identifier:

Andrea M. @andrea_b0317
did you ever find that old thing?

The profile is unavailable, so we search for the handle externally. This leads us to Andrea's controlled X/Twitter account:

https://x.com/andrea_b0317

Investigating Andrea's posts:

Andrea's account contains several travel-related posts.

"Jamaica Market just stopped for a bit before heading out."

Investigating the image leads us to Mercado Jamaica, Mexico City.

Another post shows an airport:

"made it here. way too early for this ■"

The interior can be identified as Mexico City International Airport — Terminal 2.

Another post shows a mountain/highway:

"Long drive, but the view was worth it."

The distinctive snow-covered volcano is identified as Popocatépetl, placing the journey along the Mexico City–Puebla corridor.

Wi-Fi investigation:

Separately, Andrea's account contains a screenshot pointing toward a DeepPaste-style Wi-Fi artifact.

The artifact contains multiple SSIDs. We identify the relevant SSID and search for it in WiGLE.

The intended investigation is:

SSID → WiGLE → BSSID / Net ID → mapped coordinates

This provides an independent geographic anchor. The BSSID is obtained from WiGLE rather than being directly exposed in the artifact.

THIS IS A RABBIT HOLE.

Correlating the geographic evidence:

Andrea: Mercado Jamaica → Mexico City → MEX Terminal 2 → Popocatépetl → Mexico–Puebla corridor

These clues can now be correlated to narrow down the relevant geographic area.

Investigating the RV:

We then return to the Jesse/RV evidence. The final location is not written plainly in one document. Instead, the player must combine geographic evidence, route information, visual evidence, and RV-specific evidence.

The investigation narrows to the Puebla area, with the final location identified as:

5 Sur / Mega Soriana, Puebla

Determining the final incident:

The separate phone/timestamp evidence provides the final piece of the investigation. This thread establishes Jesse's last relevant phone call and is intentionally separate from the earlier geographic investigation.

The two streams converge:

last phone call + geographic evidence + RV evidence

This reconstructs the incident and establishes where the missing RV ended up.

Final flag:

The final answer is based on the identified RV location and what incident took place through the phone call:

5Sur_MegaSoriana_Puebla_abadoned

The player submits the single final flag based on that location.

## CYS{5SUR_MEGASORIANA_PUEBLA_ABANDONED}
