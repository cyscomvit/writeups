---
layout: writeup

title: Choir Echoes
difficulty: Medium
points: 500
categories: [Forensics]
tags: []

flag: CYS{1tal1an0}
---

# Choir Echoes

- **Category**: [Forensics]
- **Author**: [ace6002]
- **Level**: [Medium]

## Challenge Description
Audio Forensics.

## Question to be given
```
You could not live with your own failures. Where did that bring you? Back to the beginning. Wear your spectacles better, perhaps you'll succeed this time.
```

## Solution

### Tools Used
- [Audacity]
- [Hexedit]

#### Step 1: Hexedit given .wav file, correct the headers from KaFX to RIFF and WAWW to WAVE.

#### Step 2: Read the file using audacity spectrography to find the key. But this is not the flag, its simply the key of a Vigenere Cipher.

#### Step 3: The tail of the file `excellente!.wav` contains the encoded text `TCE{1rrp1ml0}` .

#### Step 4: Decode Vigenere using key `remy` obtained from spectral view to get flag `CYS{1tal1an0}`.

### Flag 1
```
CYS{1tal1an0}
```

