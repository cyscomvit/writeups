---
layout: writeup

title: Temporal Core Console
difficulty: Medium
points: 500
categories: [General]
tags: []

flag: CYS{E0N_SYNCHRONIZED_2F3C}
---

# Temporal Core Console

**Category:** Forensics/Crypto  
**Author:** Varsaa H

---

## Challenge Description

The Eon city has lost its memory core. You must analyze recovered data fragments, decode hidden signals, and recover the temporal flag to restore the city’s heart.

---

## Solution

### Initial Analysis

Downloaded and inspected the provided artifacts:
- `temporal_core.log`
- `core_fragment.bin`
- `memory_snapshot.img`
- `temporal_beacon.wav`
- `EON_FINAL.enc`

---

### Tools Used

- `strings`, `xxd`, `base32`, `python`
- Audacity (or any WAV audio analyzer)
- CyberChef (online multi-tool for encodings)
- pycryptodome (Python AES library)

---

### Step-by-Step Solution

#### Step 1: Inspect the Memory Dump for Keys

strings memory_snapshot.img

text

**Found:**
- AES Key: `EONSYNCHRONIZE12`
- IV:     `SYNCWAVESFLOW1234`

---

#### Step 2: Decode the Log

cat temporal_core.log | awk '{print $2}' | tr -d '\n' > log.base32
base32 -d log.base32 > fragment.bin

text

Base32-decoded the log, yielding an encrypted blob matching `core_fragment.bin`.

---

#### Step 3: AES Decrypt the Fragment

from Crypto.Cipher import AES

key = b'EONSYNCHRONIZE12'
iv = b'SYNCWAVESFLOW1234'

with open('core_fragment.bin', 'rb') as f:
data = f.read()

def unpad(s): return s[:-s[-1]]

cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = cipher.decrypt(data)
print(unpad(plaintext).decode())

text
**Output:**
This is the beacon. Decode its pulse next. QR in sound...

text
Points to the audio file next.

---

#### Step 4: Decode `temporal_beacon.wav` (Morse)

- Loaded `temporal_beacon.wav` in an online Morse decoder or Audacity.
- Decoded message:
    ```
    RECONSTRUCT THE CYCLE REVERSED SHA1 - FOLLOW THE PULSE
    ```
- This hints the final XOR key is SHA1(reversed_flag).

---

#### Step 5: Decrypt EON_FINAL.enc

import hashlib

flag = "CYS{E0N_SYNCHRONIZED_2F3C}"
rev = flag[::-1]
sha1key = hashlib.sha1(rev.encode()).hexdigest()
key_bytes = bytes.fromhex(sha1key)

with open('EON_FINAL.enc', 'rb') as f:
data = f.read()

decrypted = ''.join(chr(b ^ key_bytes[i % len(key_bytes)]) for i, b in enumerate(data))
print(decrypted)

text

**Output:**
CYS{E0N_SYNCHRONIZED_2F3C}

text

---

## Flag

CYS{E0N_SYNCHRONIZED_2F3C}