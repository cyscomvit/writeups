---
layout: writeup

title: Blue Noise
difficulty: Easy
points: 200
categories: [Forensics / Steganography]
tags: []

flag: CYS{BLU3_H1D35_M0R3_TH4N_C0L0R}
---

Blue Noise

The player receives only `blue_noise.png`. The visible photograph is a
distraction; the solve has two layers.

## Recover the key from a blue-channel bit plane

Start with structural checks:

```sh
file blue_noise.png
strings blue_noise.png
binwalk blue_noise.png
```

The image itself does not contain a readable flag. Inspect RGB channels and
their bit planes. In blue-channel bit plane 2, the image contains a QR code.
Visualizing that plane or extracting the hidden region reveals the QR. Scanning
it gives:

```text
737-ABQ
```

The key is deliberately in bit plane 2 rather than the obvious LSB.

## Find and unlock the appended artifact

The PNG has data after its `IEND` chunk. `binwalk` reports a ZIP archive in the
suffix. Recover it either with `binwalk -e` or by locating the ZIP local header
and copying from there:

```sh
offset=$(binwalk blue_noise.png | awk '/Zip archive data/ {print $1; exit}')
dd if=blue_noise.png of=hidden.zip bs=1 skip="$offset" status=none
unzip -P 737-ABQ hidden.zip
cat note.txt
```

The password-protected `note.txt` contains:

```text
CYS{BLU3_H1D35_M0R3_TH4N_C0L0R}
```

The intended chain is therefore: blue bit plane → QR key → trailing ZIP →
flag.
