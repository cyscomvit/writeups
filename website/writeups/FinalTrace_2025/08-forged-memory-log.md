---
layout: writeup

title: Forged Memory Log
difficulty: Medium
points: 500
categories: [General]
tags: []

flag: CYS{brute_forcing_is_the_way}
---

# Forged Memory Log

 * Category: Cryptography
 * Author: P C Guhan

## Description

> Inside the Hourglass Citadel, Lyra uncovers a crystalline data shard said to contain the key to the final confession. But the key has been forged and obfuscated — mirrored fragments, deliberate noise, and counterfeit characters woven into its structure to mimic authenticity. Every attempt to read it only reveals more copies of itself, each slightly altered. To move forward, the player must isolate the genuine cipher sequence hidden beneath layers of forged keys and false reflections.

## Solution

Brute force base-32 decode 39 times
(I was limited to 39 as python had a memory error after 39 and I was lazy to do it in C/C++)

```python
import base64
with open("output.txt", "r") as f:
    inp = f.read()
inp = inp.encode('ascii')
inp = inp[2:-1]

for i in range(39):
    inp = base64.b32decode(inp)
    print(i)

print(inp)
```
>Flag: CYS{brute_forcing_is_the_way}