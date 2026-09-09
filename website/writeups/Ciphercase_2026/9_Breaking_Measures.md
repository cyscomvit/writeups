---
layout: writeup

title: Breaking Measures
difficulty: Hard
points: 500
categories: [Forensics]
tags: []

flag: CYS{no_m0r3_ha1f_m3a5ur3s}
---

Breaking Measures

**Author:** Amarnath

This is a forensics-based CTF challenge chaining SSH log analysis, HTTP access log correlation, EXIF metadata extraction, and JPEG steganography at the DCT-coefficient level, ending in a PBKDF2-derived AES decryption.

We're given two log files, `auth.log` and `access.log`, and a folder of images.

## Step 1 — Decoding the passphrase from auth.log

First, we look at `auth.log`. Several IPs get an "Accepted" line for an SSH login, so a successful login by itself doesn't tell us which one is the one that matters — each candidate has to be checked individually.

For every IP that has an Accepted line, we pull all of its lines (its failed attempts plus the final accepted one, in chronological order), take the seconds field out of each timestamp, and decode it as a letter using `letter = chr(65 + (seconds % 26))`.

**Script:**

```python
import re
import sys


def main():
    logfile = sys.argv[1] if len(sys.argv) > 1 else "auth.log"

    with open(logfile) as f:
        lines = f.readlines()

    accepted_ips = []
    for line in lines:
        if "Accepted" in line:
            m = re.search(r"from (\d+\.\d+\.\d+\.\d+)", line)
            if m:
                accepted_ips.append(m.group(1))

    accepted_ips = list(dict.fromkeys(accepted_ips))
    print(f"Found {len(accepted_ips)} IP(s) with a successful login:\n")

    for ip in accepted_ips:
        ip_lines = [line for line in lines if f"from {ip} " in line]

        seconds_values = []
        for line in ip_lines:
            m = re.search(r"\d{2}:\d{2}:(\d{2})", line)
            if m:
                seconds_values.append(int(m.group(1)))

        decoded = "".join(chr(65 + (s % 26)) for s in seconds_values)

        print(f"IP: {ip}")
        print(f"  seconds sequence: {seconds_values}")
        print(f"  decoded string:   {decoded}")
        print()


if __name__ == "__main__":
    main()
```

**Output:**

Running this against `auth.log`, only one of the three IPs decodes to a real word:

```
IP: 115.77.138.131
  decoded string:   HALFMEASURES
```

That gives us both the real IP and the passphrase, `HALFMEASURES`, which we'll need again later.

## Step 2 — Correlating with access.log

Next, we filter `access.log` by that same IP to see what it actually touched:

**Command:**

```bash
grep "115.77.138.131" access.log
```

**Output:**

```
GET  img040.jpg  200
GET  img004.jpg  200
HEAD img007.jpg  200
HEAD img042.jpg  200
GET  img031.jpg  206 (x3)
GET  img023.jpg  206 (x3)
```

Six images, in two pairs and two singles. Two files get a single plain GET — just noise. Two get a single HEAD request each — one of these is the real salt carrier, the other a decoy with an identical request pattern. Two get three repeated 206 Partial Content requests each — one is the real cipher carrier, the other a decoy shaped the same way. The log narrows things down but doesn't hand over which file in each pair is real; that has to be confirmed by actually checking each one. In this case `img042.jpg` and `img023.jpg` turn out to be the real pair.

## Step 3 — Extracting the salt from img042.jpg (EXIF)

`img042.jpg` carries the AES salt, hidden in its EXIF `UserComment` field, base32-encoded twice.

**Command:**

```bash
exiftool -UserComment images/img042.jpg
```

**Output:**

```
User Comment : JJNEGVKLKJBUOS2WI5CVSVCLIZEUMSSWJNKVGRQ=
```

**Decode script:**

```python
import sys
import base64

if __name__ == "__main__":
    encoded_once = sys.argv[1]
    once = base64.b32decode(encoded_once).decode()
    twice = base64.b32decode(once).decode()

    print("first decode: ", once)
    print("salt:         ", twice)
```

**Output:**

```
first decode:  JZCUKRCGKVGEYTKFIFJVKUSF
salt:          NEEDFULLMEASURE
```

That gives us the salt, `NEEDFULLMEASURE`.

## Step 4 — Extracting the cipher payload from img023.jpg (DCT steganography)

`img023.jpg` is where the actual encrypted flag lives, hidden inside the image's DCT coefficients rather than pixel LSBs — this is why LSB-focused tools like `steghide` or `zsteg` come back empty on it. The coefficients used are chosen by seeding a PRNG from SHA-256 of the passphrase, shuffling the list of candidate coefficients (every non-DC coefficient with an absolute value of 2 or higher), and writing the payload's bits into the LSB of those coefficients in that shuffled order, with a 32-bit length header first.

**Script:**

```python
import sys
import hashlib
import random
import jpegio as jio


def seed_from_passphrase(passphrase: bytes) -> int:
    digest = hashlib.sha256(passphrase).digest()
    return int.from_bytes(digest[:8], "big")


def get_candidate_coords(jpg):
    coords = []
    for comp_idx, arr in enumerate(jpg.coef_arrays):
        h, w = arr.shape
        for by in range(0, h, 8):
            for bx in range(0, w, 8):
                for i in range(8):
                    for j in range(8):
                        if i == 0 and j == 0:
                            continue
                        if abs(arr[by + i, bx + j]) >= 2:
                            coords.append((comp_idx, by + i, bx + j))
    return coords


def extract(stego_path: str, passphrase: bytes) -> bytes:
    jpg = jio.read(stego_path)
    coords = get_candidate_coords(jpg)

    rng = random.Random(seed_from_passphrase(passphrase))
    rng.shuffle(coords)

    header_bits = "".join(str(abs(jpg.coef_arrays[c][y, x]) & 1) for (c, y, x) in coords[:32])
    length = int(header_bits, 2)

    need = 32 + length * 8
    data_bits = "".join(str(abs(jpg.coef_arrays[c][y, x]) & 1) for (c, y, x) in coords[32:need])
    data = bytes(int(data_bits[i:i + 8], 2) for i in range(0, len(data_bits), 8))
    return data


if __name__ == "__main__":
    stego_path, passphrase_str = sys.argv[1], sys.argv[2]
    out = extract(stego_path, passphrase_str.encode())

    with open("cipher_payload_extracted.bin", "wb") as f:
        f.write(out)

    print(f"Extracted {len(out)} bytes -> cipher_payload_extracted.bin")
```

**Command:**

```bash
pip install jpegio
python3 solve_extract_dct.py images/img023.jpg HALFMEASURES
```

**Output:**

```
Extracted 48 bytes -> cipher_payload_extracted.bin
```

That's 16 bytes of IV followed by 32 bytes of AES ciphertext.

## Step 5 — Deriving the key and decrypting

Finally, the AES key is derived with PBKDF2-HMAC-SHA256 from the passphrase and salt we already have, 100,000 iterations, 32-byte output, and that key decrypts the payload with AES-CBC.

**Script:**

```python
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

PASSPHRASE = b"HALFMEASURES"
SALT = b"NEEDFULLMEASURE"
ITERATIONS = 100_000


def derive_key(passphrase=PASSPHRASE, salt=SALT, iterations=ITERATIONS):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iterations)
    return kdf.derive(passphrase)


def decrypt(payload, key):
    iv, ct = payload[:16], payload[16:]
    decryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
    padded = decryptor.update(ct) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded) + unpadder.finalize()


if __name__ == "__main__":
    with open("cipher_payload_extracted.bin", "rb") as f:
        payload = f.read()

    key = derive_key()
    flag = decrypt(payload, key)
    print("FLAG:", flag.decode())
```

**Output:**

```
FLAG: CYS{no_m0r3_ha1f_m3a5ur3s}
```

## Summary

The full chain: the seconds field in `auth.log` gives up the passphrase, the `access.log` request pattern narrows fifty images down to the two that matter, `img042`'s EXIF gives up the salt, `img023`'s DCT coefficients (unlocked by the passphrase) give up the encrypted payload, and PBKDF2 plus AES-CBC turns all of that into the flag.
