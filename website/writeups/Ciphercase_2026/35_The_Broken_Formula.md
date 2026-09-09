---
layout: writeup

title: The Broken Formula
difficulty: Medium
points: 300 
categories: [Cryptography / Steganography]
tags: []

flag: CYS{W@1t$_d3@D_dR0P_pR0t0c01_c0mpr0m1$3d_8y_J3$$3}
---

The Broken Formula

## Challenge Description

You are given six files:

```text
01.jpg
02.jpg
03.jpg
04.png
05.png
audio.mp3
```

The goal is to recover the flag.

The challenge is a chain of clues and cryptographic mistakes. The main path is:

```text
Find authenticated carrier
        ↓
Recover fragment order
        ↓
Break RSA
        ↓
Find nonce reuse
        ↓
Recover ChaCha20 keystream
        ↓
Recover Poly1305 parameters
        ↓
Forge command
        ↓
Derive vault key
        ↓
Decrypt vault
        ↓
Flag
```

`audio.mp3` is a deliberate decoy. It contains a misleading flag-like result and is not part of the successful solve path.

---

## 1. Inspect the Files

Start by checking the files:

```bash
ls -lah
file 01.jpg 02.jpg 03.jpg 04.png 05.png audio.mp3
```

The interesting files are `02.jpg` and `05.png`.

They both contain hidden index data.

The important clue is that the two indexes contain the same candidate fragments, but only one index is authenticated.

The audio file is a decoy and does not contribute to the real solve.

So don't simply choose the first index you can extract.

---

## 2. Find the Authenticated Index

`05.png` contains an `IDX8` structure hidden in the image data.

The beginning of the hidden structure is:

```text
IDX8
```

The PNG uses the image pixels themselves to hide the data. The relevant bit is the least significant bit of the red channel.

A simple extraction script can recover the bytes:

```python
from PIL import Image

image = Image.open("05.png").convert("RGB")

bits = []

for r, g, b in image.getdata():
    bits.append(r & 1)

raw = bytearray()

for i in range(0, len(bits) - 7, 8):
    value = 0

    for bit in range(8):
        value |= bits[i + bit] << (7 - bit)

    raw.append(value)

    if raw[:4] == b"IDX8":
        print(raw[:64].hex())
        break
```

The structure contains an authentication value.

The equivalent decoy data is present in `02.jpg`.

The important observation is:

```text
05.png → authority VALID
02.jpg → authority INVALID
```

Therefore the authenticated index from `05.png` is the one to trust.

---

## 3. Recover the Fragment Candidates

The authenticated index gives these candidates:

```text
A17
C04
B29
D38
E52
F11
```

At this point, don't assume all six are real.

The challenge contains continuity information that determines which fragment follows which.

The valid chain is:

```text
A17 → C04 → B29
```

The other entries are decoys:

```text
D38
E52
F11
```

The useful clue is the transition relationship:

```text
A17 → C04
C04 → B29
B29 → END
```

So the real fragment order is:

```text
A17 → C04 → B29
```

This establishes the correct path into the next layer.

---

## 4. Recover the RSA Private Key

The next clue comes from the recovered protocol information.

The protocol uses RSA keys A, B and C.

The important mistake is that RSA keys A and B share a prime factor.

For RSA:

```text
n = p × q
```

If two moduli share `p`:

```text
nA = p × qA
nB = p × qB
```

then:

```text
gcd(nA, nB) = p
```

You can therefore recover the shared prime directly.

First load the two public moduli:

```python
import json
import math

data = json.load(open("master.json"))

n_a = int(data["rsa"]["A"]["n"])
e_a = int(data["rsa"]["A"]["e"])

n_b = int(data["rsa"]["B"]["n"])

p = math.gcd(n_a, n_b)
q = n_a // p
```

Then calculate the private exponent:

```python
phi = (p - 1) * (q - 1)

d = pow(
    e_a,
    -1,
    phi
)
```

The RSA private key can then be reconstructed with the recovered `p`, `q`, `d`, `e` and `n`.

The encrypted protocol value is the top-level `protocol` field in the recovered data:

```python
ciphertext = bytes.fromhex(
    data["protocol"]
)
```

Decrypt it using RSA-OAEP with SHA-256:

```python
plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(
            algorithm=hashes.SHA256()
        ),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print(plaintext.decode())
```

The decrypted protocol contains the critical clue:

```text
DEAD-DROP/07
AUTH=CHACHA20-POLY1305
WARNING=NONCE-REUSE
PACKETS=50
TARGET=OPEN-VAULT
```

The important line is:

```text
WARNING=NONCE-REUSE
```

---

## 5. Parse the Traffic

The next artifact is the binary traffic.

It has the header:

```text
DDPK
```

followed by:

```text
Protocol version: 8
Packet count: 50
```

Each packet contains:

```text
sequence number
AAD length
nonce length
ciphertext length
tag length
AAD
nonce
ciphertext
tag
```

Parse the packet header with:

```python
import struct

seq, aad_len, nonce_len, cipher_len, tag_len = struct.unpack(
    ">HBBHB",
    raw[offset:offset + 7]
)
```

The traffic contains several reused nonce groups.

The important one is:

```text
[13, 34, 47]
```

All three packets use the same nonce.

The packet structure is:

```text
Packet 13 → 16-byte ciphertext

Packet 34 → 16-byte ciphertext

Packet 47 → 16-byte ciphertext
```

This is the real nonce-reuse group.

---

## 6. Recover the ChaCha20 Keystream

ChaCha20 is a stream cipher.

The basic relationship is:

```text
ciphertext = plaintext XOR keystream
```

Therefore:

```text
keystream = ciphertext XOR plaintext
```

Packet 13 has known plaintext:

```text
PING|NODE=07|OK!
```

Recover the keystream:

```python
known = b"PING|NODE=07|OK!"

keystream = bytes(
    a ^ b
    for a, b in zip(
        known,
        ciphertext
    )
)

print(keystream.hex())
```

The recovered 16-byte keystream is:

```text
885516f46eb4af483e1bbc30598645c0
```

Because the nonce was reused, the same keystream is valid for packets 34 and 47.

Their first 16 plaintext bytes become:

```text
AUTH|USER|STAT!!

AUTH|USER|READ!!
```

That confirms the nonce-reuse attack.

---

## 7. Recover Poly1305 `r` and `s`

ChaCha20-Poly1305 also authenticates the encrypted data using Poly1305.

Nonce reuse means the same Poly1305 one-time key is reused.

For this challenge, the three reused packets all have 16-byte ciphertexts, making the equations manageable.

The Poly1305 modulus is:

```python
P = (1 << 130) - 5

MOD = 1 << 128
```

The challenge's fixed-length polynomial can be represented as:

```python
def poly_value(ciphertext, r):

    message = (
        int.from_bytes(
            ciphertext,
            "little"
        ) +
        (1 << 128)
    )

    length_block = 16 << 64

    h = 0

    h = (
        (h + message) * r
    ) % P

    h = (
        (h + length_block) * r
    ) % P

    return h
```

For two packets:

```text
tag1 = Poly1305(message1, r) + s

tag2 = Poly1305(message2, r) + s
```

Subtracting the equations removes `s`.

The final tag is reduced modulo:

```text
2^128
```

so the solver also accounts for the small possible tag carries.

The recovered values are:

```text
r = 0xd22de48026933b0053407780e113741

s = 0x190aef408628d7c22942d84aecf852c9
```

The important point is that the recovered candidate is checked against the third packet before it is accepted.

---

## 8. Forge `AUTH|MAINT|OPEN!`

Now we have both things needed for a forgery:

```text
ChaCha20 keystream

Poly1305 r and s
```

The target command is:

```text
AUTH|MAINT|OPEN!
```

It is exactly 16 bytes.

Generate its ciphertext:

```python
target = b"AUTH|MAINT|OPEN!"

forged_ciphertext = bytes(
    a ^ b
    for a, b in zip(
        target,
        keystream
    )
)

print(forged_ciphertext.hex())
```

The resulting ciphertext is:

```text
c90042bc12f9ee01704fc07f09c30be1
```

Calculate the new Poly1305 tag:

```python
forged_tag = (
    (
        poly_value(
            forged_ciphertext,
            r
        ) + s
    ) % (1 << 128)
).to_bytes(
    16,
    "little"
)

print(forged_tag.hex())
```

The resulting tag is:

```text
3d4cb61e46cb99c0360f10207fc01b5f
```

So the forged packet represents:

```text
AUTH|MAINT|OPEN!
```

with a valid authentication tag.

---

## 9. Derive the Vault Key

The challenge uses the forged packet to derive the vault key.

The transcript is:

```text
nonce || forged ciphertext || forged tag
```

Build it:

```python
transcript = (
    bytes.fromhex(nonce) +
    bytes.fromhex(forged_ciphertext) +
    bytes.fromhex(forged_tag)
)
```

Then derive the key:

```python
import hashlib

vault_key = hashlib.sha256(
    b"DD07-VAULT-V1|" +
    transcript
).digest()
```

This is the key used to protect the final vault.

---

## 10. Decrypt the Vault

The vault uses ChaCha20-Poly1305 again.

Load its nonce and ciphertext, then decrypt using the derived key:

```python
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

vault_nonce = bytes.fromhex(
    data["vault"]["nonce"]
)

vault_ciphertext = bytes.fromhex(
    data["vault"]["ciphertext"]
)

flag = ChaCha20Poly1305(
    vault_key
).decrypt(
    vault_nonce,
    vault_ciphertext,
    None
)

print(flag.decode())
```

The vault decrypts successfully.

---

## 11. Final Flag

```text
CYS{W@1t$_d3@D_dR0P_pR0t0c01_c0mpr0m1$3d_8y_J3$$3}
```

---

## Solve Summary

| Step | What you discover |
|---|---|
| 1 | `05.png` contains the authenticated index |
| 2 | The real fragment chain is `A17 → C04 → B29` |
| 3 | RSA A and B share a prime |
| 4 | The decrypted protocol warns about nonce reuse |
| 5 | Packets `13, 34, 47` reuse a nonce |
| 6 | Known plaintext recovers the ChaCha20 keystream |
| 7 | Reused Poly1305 material gives `r` and `s` |
| 8 | Forge `AUTH|MAINT|OPEN!` |
| 9 | Hash the forged transcript to derive the vault key |
| 10 | Decrypt the vault |
| 11 | Recover the flag |
