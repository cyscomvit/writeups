---
layout: writeup

title: Maelle Confrontation
difficulty: Medium
points: 500
categories: [OSINT]
tags: []

flag: CYS{d3nyy}
---

# Maelle Confrontation

- **Category**: [OSINT]
- **Author**: [ace6002]
- **Level**: [Medium]

## Challenge Description
Multi flag OSINT based on social media/tracking down a certain user.

## Question to be given
```
Beneath whispers of the forgotten web, one name drifts between the cracks: 1skim. Seek not the obvious, but what lingers behind the veil of public traces. Threads lead where shadows meet data. The flag is no secret—only unseen. Follow the noise, and let open eyes find the hidden truth.
```

## Solution

### Tools Used
- [Instagram, bsky.app, Discord]

#### Step 1: Take given username in question (1skim_) and find the instagram account with the same username.

#### Step 2: There are 2 posts. Each post leads to a different flag.

#### Path 1: Post 1 states `man, i sure love bisky kruger from HxH. definitely one of the best teachers out there. shes for sure my number 2.` The hint lies with `bisky` it translates to `bsky` i.e. `bsky.app`. A twitter alternative, much lesser known. Search for username 2skim on bsky.app, the player will find the flag 1, in base64.

#### Path 2: Post 2 states `goat. did you know laid loved Clyde more than anything? that's my number 3 though, god knows how it's his top.` The hint lies with Clyde. Sent a request to the discord username `3skim_`. In the About Me lies a clue, `ANIME LOVAR. NO QUESTIONIG. It really has some Soul in it you know, unlike Hollywood.` the clue here is AnimeSoul, the largest public anime server on Discord. The status of 3skim_ reads `just chillin'`, another clue. Join AnimeSoul, head into #chill-chat, and search for messages by 3skim_. There is only one message, with the flag in base64.

### Flag 1
```
CYS{l0v3_Y0uu}
```

### Flag 2
```
CYS{d3nyy}
```

