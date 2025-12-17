---
layout: writeup

title: Spectogram Shadows
difficulty: Medium
points: 500
categories: [General]
tags: []

flag: cys{N9OO22_ESOO7S}
---

## Spectogram Shadows
**Category**: Forensics
**Author**: Suraj Kumar

## Challenge Description

A wav audio file contains a hidden, encrypted flag visible in the spectrogram. The flag in the spectrogram was encrypted with the vigenere cipher. The key for the cipher is stored at the end of the file's hex data. Several dummy encoded flags are present in WAV comment metadata (they are red herrings).

---

## Solution

### Initial Analysis

1. Open the WAV file and inspect metadata and appended data. The spectrogram shows a message (the encrypted flag) so the flag text is present in the audio itself (as visual data). The ciphertext visible in the spectrogram looks like ASCII when transcribed.
2. The key is appended at the end of the WAV file (in the file's hex). The hint "vigenere" is encoded in rot13 base32 base64 base64" and added in audios metadata Title

### Tools Used

* cyberchef/Any online decoders
* audacity?any spectograph tool
---

### Step-by-step Solution

#### Step 1 _Find Key
Key is at the end of hex of the audio("secretkey")
#### Step 2: See Spectograph
See audio spectography to find the vigenere encoded flag(ucu{e9sh22_owmg7w})
#### Step 3 — Find flag using the discovered key to decode the cipher
Giving the key will decode and return the original flag 

## Flag

```
cys{N9OO22_ESOO7S}