---
layout: writeup

title: Project To'hajiilee
difficulty: Easy
points: 200
categories: [Steganography]
tags: [LSB, zsteg]

flag: CYS{34_59_20_106_36_52_custom_l5b_3ncrypt10n_m4ster}
---
Project To'hajiilee

Author: Joeliyn

This is a steganography-based CTF challenge demonstrating Least Significant Bit (LSB) steganography.

The challenge provides a PNG image with a secret message hidden inside the least significant bits of the Red channel. Since modifying the LSB of a pixel channel changes its value by at most 1, the modification is not noticeable to the human eye.

Firstly, we can inspect the metadata of the provided image using:

exiftool challenge_1.png

The comment in the metadata gives us a useful hint:

LSB secret hidden in Red channel (RGB -> R_LSB). Reads top-left to bottom-right until null byte.

This tells us that the secret is hidden in the LSBs of the Red channel.

Instead of manually extracting the LSBs, we can use zsteg, a tool commonly used for detecting hidden data in PNG and BMP images.

We run:

zsteg challenge_1.png

The output reveals hidden data in the Red channel LSB plane. We can then extract the data using:

zsteg -E b1,r challenge_1.png

Here, b1 refers to the least significant bit plane and r specifies the Red channel.

The extracted data gives us the flag:

CYS{34_59_20_106_36_52_custom_l5b_3ncrypt10n_m4ster}

The challenge demonstrates how information can be hidden inside image pixels using LSB steganography. Since only the least significant bit of the Red channel is modified, the resulting image looks practically identical to the original while still containing the hidden message.