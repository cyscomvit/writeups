---
layout: writeup

title: Blue Sky Telemetry 
difficulty: Easy
points: 200
categories: [Steganography/Reverse Engineering]
tags: [stego, reverse-engineering]

flag: CTF{h3is3nb3rg_c00k_t3l3m3try_99_1}
---

Blue Sky Telemetry 

Author: Prateet Gogia

This is a Steganography and Reverse Engineering-based CTF challenge demonstrating layered hidden data, red herrings, and custom firmware encryption.

Firstly for the Decoy part:

Running `strings artifact.jpg` yields a fake Base64 string decoding to `CTF{y0u_g0dd4mn_r1ght_I_h1d_1t_but_n0t_h3r3}`. 

For the Steganography part:

First, we check the metadata. `exiftool artifact.jpg` reveals `Artist : c3VwZXJzZWNyZXRrZXk=`, which Base64 decodes to `supersecretkey`.

Next, we use this for the Archive Extraction. Running `steghide extract -sf artifact.jpg -p supersecretkey` drops `payload.zip`. 

For the Reverse Engineering part:

Unzipping reveals `intercept_log.txt` (containing a Base32 decoy and a raw hex array) and `firmware_snippet.c`. 

The C script shows the data was encrypted using `(data[i] ^ 0x33) + 0x05`. 

To get the final flag, the player must write a script to reverse this operation `chr((byte - 0x05) ^ 0x33)` against the hex array to yield the final flag: `CTF{h3is3nb3rg_c00k_t3l3m3try_99_1}`.