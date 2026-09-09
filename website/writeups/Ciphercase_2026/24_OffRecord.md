---
layout: writeup

title: OffRecord
difficulty: Medium
points: 300
categories: [Stego/Crypto]
tags: []

flag: CYS{BEST_QUALITY_VACUUM_IS_KEY_42}
---

# OffRecord

Author: Sagnik

This challenge is a combination of image steganography, QR extraction, metadata clues, Breaking Bad trivia, Base64, and XOR.

The intended solve path is:

```text
PNG
 ↓
EXIF metadata
 ↓
Blue-channel LSB
 ↓
Hidden QR
 ↓
Base64 ciphertext
 ↓
Breaking Bad trivia
 ↓
XOR
 ↓
FLAG
```

## Firstly, inspect the image metadata

We can use:

```bash
exiftool challenge.png
```

The relevant metadata contains:

```text
Image Description : The model is written continuously.
Artist            : Walter H.
User Comment      : Some reactions are exclusive.
```

The two important clues are:

```text
The model is written continuously.
Some reactions are exclusive.
```

The first clue tells us how the eventual key should be formatted.

The second clue hints at the cryptographic operation.

## Inspect the image for steganography

Since the challenge involves image steganography, we can inspect the PNG bit planes.

For example:

```bash
zsteg challenge.png
```

The hidden QR is stored in the:

```text
Blue channel
Bit 0 (LSB)
```

The QR is not directly visible in the original image.

The relevant pixels can be extracted by taking:

```python
bit = blue_channel_pixel & 1
```

and reconstructing the corresponding region as a black-and-white image.

The resulting image contains the hidden QR code.

## Decode the QR code

After extracting the QR region, decode it using a QR decoder.

The QR contains:

```text
CxYcLQcXHhUHFA0VHggXDQ8EBBAGAB8aGQEQBgodGngETQ==
```

This looks like Base64.

Decode it:

```bash
echo 'CxYcLQcXHhUHFA0VHggXDQ8EBBAGAB8aGQEQBgodGngETQ==' | base64 -d
```

The result is binary data rather than readable text.

This means Base64 is only an encoding layer and there is still another operation to reverse.

## Solve the Breaking Bad clue

The visible image contains the question:

> Which vacuum cleaner's dust filter do I need to disappear?

This references the vacuum cleaner/disappearance service from *Breaking Bad* and *Better Call Saul*.

The relevant model is:

```text
Hoover Max Extract Pressure Pro, Model 60
```

The EXIF clue says:

```text
The model is written continuously.
```

Therefore remove spaces and punctuation and use one continuous uppercase string:

```text
HOOVERMAXEXTRACTPRESSUREPROMODEL60
```

This is the key.

## Identify XOR

The second EXIF clue says:

```text
Some reactions are exclusive.
```

The word "exclusive" points toward:

```text
XOR = Exclusive OR
```

The encryption process is:

```text
FLAG
 ↓
XOR with key
 ↓
Base64
 ↓
QR
```

So we reverse it:

```text
QR
 ↓
Base64
 ↓
Base64 decode
 ↓
XOR with key
 ↓
FLAG
```

## Decrypt the ciphertext

The ciphertext is:

```text
CxYcLQcXHhUHFA0VHggXDQ8EBBAGAB8aGQEQBgodGngETQ==
```

The key is:

```text
HOOVERMAXEXTRACTPRESSUREPROMODEL60
```

After Base64 decoding and XORing the resulting bytes with the key, the plaintext is:

```text
CYS{BEST_QUALITY_VACUUM_IS_KEY_42}
```

## Complete solve chain

```text
                         challenge.png
                              |
                 +------------+------------+
                 |                         |
                 v                         v
             EXIF data                 Image data
                 |                         |
        +--------+--------+                |
        |                 |                v
        v                 v          Blue-channel LSB
 "written continuously" "exclusive"       |
        |                 |                v
        |                 |          Hidden QR
        |                 |                |
        |                 |                v
        |                 |          Base64 text
        |                 |                |
        +--------+--------+----------------+
                 |
                 v
       Hoover Max Extract Pressure
             Pro Model 60
                 |
                 v
HOOVERMAXEXTRACTPRESSUREPROMODEL60
                 |
                 v
             XOR decrypt
                 |
                 v
                FLAG
```

## Final Flag

```text
CYS{BEST_QUALITY_VACUUM_IS_KEY_42}
```
