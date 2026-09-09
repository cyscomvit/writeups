---
layout: writeup

title: The Same Wheel, Twice Turned
difficulty: Hard
points: 500
categories: Cryptography

flag: CYS{tH1$_3cd$A_1S_b3tTeR_tH@n_h3is3n83rGs_b1Ue_Pr0DuCt}
---

The Same Wheel, Twice Turned

Author: Om

This is a cryptography challenge demonstrating ECDSA nonce reuse, followed by ECDH shared-secret recovery, XORShift8-based salt reconstruction, SHA-256 hash-chain analysis, HKDF-SHA256 key derivation, and AES-256-GCM decryption to recover the final flag.

For the ECDSA nonce recovery:

The two messages are:

```text
Archive access request: sector-17
Archive access request: sector-42
```

The challenge provides `info.json` containing the two ECDSA signatures.

Read the values:

```python id="d7k3p1"
import json

with open("info.json", "r") as f:
    data = json.load(f)

r1 = int(data["sector_17_log"]["echo"], 16)
s1 = int(data["sector_17_log"]["trace"], 16)
r2 = int(data["sector_42_log"]["echo"], 16)
s2 = int(data["sector_42_log"]["trace"], 16)
```

Both signatures were generated using the same ECDSA nonce `k`.

For ECDSA:

```text id="j2m8q4"
s = (k^-1)(z + rd) mod n
```

Since the same `k` was used for both messages:

```text id="p5v1x9"
k = (z1 - z2) / (s1 - s2) mod n
```

Use:

```python id="h6r3t8"
from hashlib import sha256
from ecdsa import SECP256k1

message1 = b"Archive access request: sector-17"
message2 = b"Archive access request: sector-42"

n = SECP256k1.order

z1 = int.from_bytes(sha256(message1).digest(), "big")
z2 = int.from_bytes(sha256(message2).digest(), "big")

k = ((z1 - z2) * pow(s1 - s2, -1, n)) % n

print("Recovered k:", hex(k))
```

For recovering the ECDSA private key:

Once `k` is known:

```text id="r9w2f6"
d = (s1k - z1) / r1 mod n
```

```python id="q4n7s1"
d = ((s1 * k - z1) * pow(r1, -1, n)) % n
print("Recovered private key:", hex(d))
```

For recovering the ECDH shared secret:

The `info.json` file also contains the ECDH public key coordinates:

```text id="u8c3m5"
rendezvous_point.north
rendezvous_point.east
```

```python id="a6k1p9"
from cryptography.hazmat.primitives.asymmetric import ec

public_x = int(data["rendezvous_point"]["north"], 16)
public_y = int(data["rendezvous_point"]["east"], 16)

ecdh_public = ec.EllipticCurvePublicNumbers(
    public_x, public_y, ec.SECP256K1()
).public_key()

ecdh_private = ec.derive_private_key(d, ec.SECP256K1())

shared_secret = ecdh_private.exchange(ec.ECDH(), ecdh_public)
print("Shared secret:", shared_secret.hex())
```

For recovering the XORShift8 seed:

The PRNG clue gives:

```text id="v3h7n2"
Observed X1 = f5
```

The XORShift8 function is:

```python id="m8q4x6"
def xorshift8(x):
    x ^= (x << 3) & 0xff
    x ^= x >> 5
    x ^= (x << 1) & 0xff
    return x & 0xff
```

The seed is one byte, so test all 256 possibilities:

```python id="k5r1d9"
observed_x1 = 0xf5

seed = None

for candidate in range(256):
    if xorshift8(candidate) == observed_x1:
        seed = candidate
        break

if seed is None:
    raise ValueError("Seed not found")

print("Seed:", f"{seed:02x}")
```

The recovered seed is:

```text id="n2w7p4"
99
```

For generating the PRNG sequence:

```python id="c6t3m8"
outputs = []
state = seed

for _ in range(16):
    state = xorshift8(state)
    outputs.append(state)

for i, value in enumerate(outputs, 1):
    print(f"X{i} = {value:02x}")
```

The sequence is:

```text id="f4j9s2"
X1  = f5
X2  = e1
X3  = 32
X4  = e9
X5  = ec
X6  = 98
X7  = ee
X8  = ae
X9  = 68
X10 = 7b
X11 = ea
X12 = c1
X13 = 51
X14 = 61
X15 = be
X16 = d4
```

For reconstructing the salt:

The fixed permutation is:

```python id="p7v2h5"
permutation = [
    13, 6, 7, 10,
    14, 1, 2, 9,
    15, 4, 16, 3,
    11, 8, 5, 12
]

salt = bytes(outputs[i - 1] for i in permutation)
print("Salt:", salt.hex())
```

This gives:

```text id="s8m4q1"
5198ee7b61f5e168bee9d432eaaeecc1
```

For building the hash chain:

There are two possible branches.

Story A:

```text id="b3n7x9"
BLUE → 99.1 → JESSE → 17 → HEISENBERG
```

Story B:

```text id="d6r2k8"
RED → 96.4 → MAX → 42 → FRING
```

The hash-chain operation is:

```text id="w5p1c7"
H1 = SHA256(token1)
H2 = SHA256(H1 || token2)
H3 = SHA256(H2 || token3)
...
```

```python id="q9f3m6"
from hashlib import sha256

def build_chain(tokens):
    current = sha256(tokens[0].encode()).digest()
    for token in tokens[1:]:
        current = sha256(current + token.encode()).digest()
    return current

story_a = ["BLUE", "99.1", "JESSE", "17", "HEISENBERG"]
story_b = ["RED", "96.4", "MAX", "42", "FRING"]

info_a = build_chain(story_a)
info_b = build_chain(story_b)

print("INFO A:", info_a.hex())
print("INFO B:", info_b.hex())
```

The results are:

```text id="r4k8t2"
INFO A:
00f9f80029d42eb7672b9daf7c3ae1f203e628b30ff5fc22ba08e98f6d4c2191

INFO B:
85f3b386efd3d31d6eac7e8b240f84ad4d3c0bc2795cd148250e9535ae13f7b3
```

For deriving the AES key:

For each branch, derive the AES-256 key using HKDF-SHA256:

```python id="h1v6n9"
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

aes_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    info=info
).derive(shared_secret)
```

For decrypting the ciphertext:

The participant receives:

```text id="m3q7s5"
info.json
aes_nonce.bin
aes_ciphertext.bin
```

Read the AES files:

```python id="x8d2p4"
from pathlib import Path

nonce = Path("aes_nonce.bin").read_bytes()
ciphertext = Path("aes_ciphertext.bin").read_bytes()
```

Try both hash-chain branches:

```python id="t5k9w1"
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

for branch, info in [("A", info_a), ("B", info_b)]:
    aes_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=info
    ).derive(shared_secret)

    try:
        flag = AESGCM(aes_key).decrypt(nonce, ciphertext, None)
        print("Correct branch:", branch)
        print("FLAG:", flag.decode())
        break
    except Exception:
        pass
else:
    print("Decryption failed")
```

Only the correct `INFO` produces a valid AES-GCM authentication tag. The successful decryption identifies the correct branch and reveals the flag.

The final flag is:

```text id="n6r3x8"
CYS{tH1$_3cd$A_1S_b3tTeR_tH@n_h3is3n83rGs_b1Ue_Pr0DuCt}
```
