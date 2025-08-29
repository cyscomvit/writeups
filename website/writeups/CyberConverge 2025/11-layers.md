---
layout: writeup

title: Layers
difficulty: easy
points: 150
categories: [Cryptography]
tags: []

flag: CBCV{cRy9T0_L4y3r5_4RE_FuN_3135}
---

# Layers

* Author: Om Mishra

## Description
The challenge provides an encoded string. It is encrypted using a Caesar cipher with a shift of 7, then Base64 encoded.

## Steps to Solve
1. Take the given encoded string: `Q0JEVntrb3RyeX...}`  
2. First, decode it from **Base64**.  
3. Next, apply a **Caesar cipher decryption with shift = 19**.  
4. You will get the final flag.

## Flag
CBCV{cRy9T0_L4y3r5_4RE_FuN_3135}
