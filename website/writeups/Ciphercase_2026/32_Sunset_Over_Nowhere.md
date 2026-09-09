---
title: Sunset Over Nowhere
difficulty: Easy
points: 200
categories: [Forensics/Steganography]
tags: []

flag: CYS{m3t4d4t4_ch41ns_h1d3_th3_k3y}
---
Sunset Over Nowhere

Author: Chitwan

This is a forensics/steganography challenge involving image metadata, encoding, XOR, and a hidden ZIP file.

First, inspect the image:

file challenge.jpg
exiftool challenge.jpg

The metadata contains three encoded values:

Make:        U2g0ZG93
Description: Cvk3y
Keywords:    5f3939

Decode them:

Base64 U2g0ZG93 → Sh4dow
ROT13 Cvk3y → Pix3l
Hex 5f3939 → _99

The Copyright field says:

Assembly order: A + B + C

So the ZIP password is:

Sh4dowPix3l_99

Next, the XP Comment gives the XOR hint:

XOR byte = (the answer to life, the universe, and everything) minus twelve

42 - 12 = 30 = 0x1E

So the XOR key is 0x1E.

We then search for the hidden payload:

grep -oba "STEG0" challenge.jpg

Everything after the STEG0 marker is the XOR-obfuscated ZIP archive. Extract the payload and XOR each byte with 0x1E:

key = 0x1E

with open("payload.bin", "rb") as f:
    data = f.read()

decoded = bytes(b ^ key for b in data)

with open("recovered.zip", "wb") as f:
    f.write(decoded)

The recovered ZIP can then be opened using:

Sh4dowPix3l_99

Inside the archive is flag.txt, which contains:

CYS{m3t4d4t4_ch41ns_h1d3_th3_k3y}

The fake password and fake flag in the metadata are decoys, so players must follow the actual metadata clues to reach the final flag.