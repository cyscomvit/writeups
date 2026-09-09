---
layout: writeup

title: Signal Lost
difficulty: Hard
points: 500
categories: Steganography

flag: CYS{dynamic_flag}
---
Signal Lost

Author: Shreehari

This is a multi-layer forensics/steganography challenge. The image contains three decoy investigation paths and one genuine path requiring cross-referencing.

Tools used: exiftool, strings, binwalk, zsteg, Python (Pillow)

For the initial reconnaissance:

We inspect the image metadata using exiftool:

```bash
exiftool signal_lost.png
```

The metadata contains:

Artist: Probe HELIOS-7 / Autonomous Imaging Unit

Description: Deep field survey - unit helios7 - final burst before LOS

Comment: T3BlcmF0aW9uIERlZXAgU2t5IC0gRnJhbWUgNDcvMTI4

The Comment is base64 encoded. We decode it using:

```bash
echo "T3BlcmF0aW9uIERlZXAgU2t5IC0gRnJhbWUgNDcvMTI4" | base64 -d
```

This gives:

```text
Operation Deep Sky - Frame 47/128
```

This is flavour text and leads to a dead end.

For the binwalk part:

We inspect the image using binwalk:

```bash
binwalk signal_lost.png
binwalk -e signal_lost.png
```

This finds zlib data after IEND. Decompressing it gives:

```text
[HELIOS-7 DIAGNOSTIC LOG]
Status: CRITICAL - Loss of signal imminent
Result: Primary data stream: CORRUPTED
        Backup stream: UNAVAILABLE
```

For the pixel analysis:

We use zsteg:

```bash
zsteg signal_lost.png
```

The relevant output is:

```text
b1,r,lsb,xy    .. text: [garbage/noise]
b1,g,lsb,xy    .. text: "auth:probe_designation"
b1,b,lsb,xy    .. file: data
```

The channels can be interpreted as:

Red = noise (corrupted primary stream)

Green = auth:probe_designation ← KEY HINT

Blue = encrypted payload

The value `auth:probe_designation` means that the decryption key is the probe's designation.

From the Step 1 metadata, the Description contains `unit helios7`.

Therefore:

```text
key = "helios7"
```

For the decryption part:

We extract the blue channel LSBs using Python and Pillow:

```python
from PIL import Image

img = Image.open("signal_lost.png")
pixels = list(img.getdata())

# Extract blue channel LSBs
blue_bytes = []
bits = []
for p in pixels:
    bits.append(p[2] & 1)
    if len(bits) == 8:
        val = 0
        for b in bits:
            val = (val << 1) | b
        if val == 0:
            break
        blue_bytes.append(val)
        bits = []

# XOR with key
key = b"NEWKEY123"
flag = bytes([blue_bytes[i] ^ key[i % len(key)] for i in range(len(blue_bytes))])
print(flag.decode())
```

The output is:

```text
CYS{dynamic_flag}
```
