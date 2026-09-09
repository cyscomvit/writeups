---
layout: writeup

title: Reverse Image Trail — Episode 3
difficulty: Easy
points: 200
categories: [OSINT/Web]
tags: []

flag: CTF{tw1st3rs_n0t_p0ll0s}
---

Reverse Image Trail — Episode 3

Author: Yukti Kapoor

This is an OSINT/Web-based CTF challenge where participants must identify the real-world restaurant shown in a cropped photograph, distinguish it from its fictional representation in Breaking Bad and Better Call Saul, and use the correct real-world name to unlock the flag.

The Misdirection:

Participants are given a cropped photo of a fast-food storefront in Albuquerque, New Mexico. The storefront is presented as "Los Pollos Hermanos", Gustavo Fring's fictional fried-chicken chain and money-laundering front in Breaking Bad and Better Call Saul.

However, the real restaurant operating at the location is called Twisters Burgers & Burritos.

The restaurant at 4257 Isleta Blvd SW, Albuquerque is actually Twisters Burgers & Burritos, a New Mexican-cuisine chain founded in 1998. It serves burgers, burritos, and green chile rather than fried chicken.

The "Los Pollos Hermanos" name, logo, and chicken menu exist only within the show's fiction.

Step 1 — Identify the clue:

We begin with the provided handout image:

handout/clue_03.jpg

We can perform a reverse image search using tools such as Google Lens or TinEye.

Step 2 — Spot the mismatch:

The search results surface both "Los Pollos Hermanos" fan content and genuine news/travel coverage identifying the real business as Twisters.

This is the key part of the challenge: the first identification should not be trusted blindly.

The correct answer is the real name of the restaurant, rather than the fictional name used in the shows.

The same real-world location was reused as Los Pollos Hermanos across Breaking Bad and Better Call Saul, with an appearance in the film El Camino as well.

Step 3 — Unlock the archive:

We visit the hosted archive page and submit the normalized answer:

twisters

The answer is normalized by converting it to lowercase and removing non-alphanumeric characters.

Step 4 — Flag delivery:

Once the correct answer is submitted, the client-side JavaScript decodes a Base64-encoded string and displays the flag.

The relevant logic is:

function normalize(s) {
  return s.toLowerCase().replace(/[^a-z0-9]/g, "");
}

function checkAnswer() {
  var userAnswer = normalize(document.getElementById("answerBox").value);
  var correct = "twisters";

  if (userAnswer === correct) {
    var encoded = "Q1RGe3R3MXN0M3JzX24wdF9wMGxsMHN9";
    document.getElementById("flagOutput").innerHTML =
      "Record unlocked. Flag: " + atob(encoded);
  }
}

The Base64-encoded value:

Q1RGe3R3MXN0M3JzX24wdF9wMGxsMHN9

decodes to:

CYS{tw1st3rs_n0t_p0ll0s}

The organizer-side build process is handled by backend_generator.py. It strips metadata from the source photo, Base64-encodes the flag, and injects the required values into index_template.html to generate index.html.

Learning Outcome:

This challenge demonstrates the importance of verifying an identification rather than trusting the first confident-looking search result or fan-page label.

It also teaches participants to:

- Distinguish fictional, in-universe branding from the real business operating at a physical location.
- Practice reverse-image-search-based OSINT.
- Understand a simple client-side flag-gating mechanism using encoding.
- Recognize the limitations of client-side flag protection.
- Build a research chain using multiple independent sources instead of relying on a single result.

Final flag:

CYS{tw1st3rs_n0t_p0ll0s}
---