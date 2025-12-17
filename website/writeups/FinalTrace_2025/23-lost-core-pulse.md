---
layout: writeup

title: Lost Core Pulse
difficulty: Medium
points: 500
categories: [General]
tags: []

flag: CYS{3bb12d_lostpulse_91be2d}
---

## Lost Core Pulse

- **Category:** Crypto
- **Author:** Varsaa H

---

## Challenge Description

The Eon city's memory pulse went missing in a turbulent transmission. What remains in cipher.txt is cloaked with layers recognizable only to cryptographers—and those attentive to the patterns of Eon's lost pulse.

*Hint: Sometimes, signals are wrapped not once but twice.*

---

## Solution

### Initial Analysis

- Downloaded and inspected the file `cipher.txt`.
- The content was a long string of what looked like hexadecimal characters.

---

### Tools Used

- Python (hex and base64 decoding)
- CyberChef (for alternate handy decoding)
- Any text editor

---

### Step-by-Step Solution

#### Step 1: Hex Decode the cipher.txt

with open('cipher.txt') as f:
data = bytes.fromhex(f.read())
print(data)

This produced a result that looked like base64:
b'Q1lTezNiYjEyZGF9b3N0cHVsc2VFOTFiZTJkZTFkZjQ='


#### Step 2: Base64 Decode the Result

import base64
flag = base64.b64decode(data).decode()
print(flag)

text
Output:
CYS{3bb12d_lostpulse_91be2d}

This is the flag, revealed from the two encoding layers.


### Flag

CYS{3bb12d_lostpulse_91be2d}