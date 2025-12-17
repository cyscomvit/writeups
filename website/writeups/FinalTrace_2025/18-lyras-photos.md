---
layout: writeup

title: Lyra's Photos
difficulty: Medium
points: 500
categories: [Forensics]
tags: []

flag: CYS{f1v3_53n535_s1x_3m0t10n5}
---

## Lyra's Photos

- **Category**: Forensics
- **Author**: Aadhyanth

## Challenge Description

Hark, seeker of secrets! Before thee lies not cold stone, but the scattered remnants of a life lived, perhaps loved, perhaps lost. Six timeworn likenesses, captured by the enigmatic Lyra, lay strewn upon the dusty floor of this forgotten chamber. They say Lyra possessed the sight, able to bind not just light, but feeling, into her creations.

Each portrait – a frozen moment of joy, sorrow, anger, fear, surprise, or contemplation – pulses with a faint, spectral energy. Within the very weave of these images, Lyra concealed fragments of a greater truth, echoes of the heart bound to the canvas.

Thy task, should thou possess the keen eye and sharper wit, is to delve into the hidden layers of each depiction. Uncover the six fragments of data, each resonating with the soul of the emotion it guards. Only by piecing together these spectral whispers can the full secret be unveiled. Tread carefully, for memories, like ghosts, oft cling tightly to their resting place.

## Solution

This challenge consists of 6 separate image files.
Each image contains one part of the flag, hidden at a random location.

Extraction hints (for stegsolve):

- image_1_red.png: Channels -> Red ; Bitplanes -> 0
- image_2_yellow.png: Channels -> Green ; Bitplanes -> 0
- image_3_green.png: Channels -> Blue ; Bitplanes -> 0
- image_4_blue.png: Channels -> Red ; Bitplanes -> 4
- image_5_black.png: Channels -> Green ; Bitplanes -> 4
- image_6_white.png: Channels -> Blue ; Bitplanes -> 4

Alternatively, using a random colormap usually works for all 6 images

Parts:
Part 1: "CYS{f"
Part 2: "1v3*5"
Part 3: "3n535"
Part 4: "\_s1x*"
Part 5: "3m0t1"
Part 6: "0n5}"

### Tools Used

- Stegsolve

### Step-by-Step Solution

#### Step 1:

```
java -jar Stegsolve.jar
```

Opens stegsolve

#### Step 2:

Use the arrows to find the correct setting

### Flag

```
CYS{f1v3_53n535_s1x_3m0t10n5}
```
