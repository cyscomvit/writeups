---
layout: writeup

title: The Archivist's Last Secret
difficulty: Hard
categories: Steganography
points: 500
flag: CYS{1_@m_iN_+h3_3mp1r3_8u$in388}
---
The Archivist's Last Secret

Author: Om

This is a steganography challenge combining DCT-based steganography, PNG chunk analysis, ML-KEM-768 decapsulation, HKDF-SHA256 key derivation, and AES-256-GCM decryption.

For the seed identification part:

The story gives the date `21-08-2026` and indicates that it should be written without separators.

This gives the deterministic seed:

```text
20260821
```

The same seed is used when shuffling the candidate DCT coefficients.

For the AES payload extraction from Image 1:

The first image hides data in JPEG DCT coefficients. The DCT position is `(1,2)`, zero coefficients are ignored, and the parity of each remaining coefficient encodes a bit.

```python
from pathlib import Path
import jpegio as jio
import random

IMAGE = "FINAL_CHALL_1.jpg"
SEED = 20260821
DCT_POS = (1, 2)
PAYLOAD_SIZE = 60

jpeg = jio.read(IMAGE)
Y = jpeg.coef_arrays[0]

candidates = []

height, width = Y.shape

for block_y in range(0, height, 8):
    for block_x in range(0, width, 8):
        y = block_y + DCT_POS[0]
        x = block_x + DCT_POS[1]

        if Y[y, x] != 0:
            candidates.append(Y[y, x])

rng = random.Random(SEED)
rng.shuffle(candidates)

bits = [
    abs(value) % 2
    for value in candidates[:PAYLOAD_SIZE * 8]
]

payload = bytes(
    sum(bits[i + j] << (7 - j) for j in range(8))
    for i in range(0, len(bits), 8)
)

Path("aes_payload.bin").write_bytes(payload)
```

The recovered payload is 60 bytes. The first 48 bytes contain the AES-GCM ciphertext and authentication tag, while the final 12 bytes are the nonce.

```python
from pathlib import Path

payload = Path("aes_payload.bin").read_bytes()

Path("aes_ciphertext.bin").write_bytes(payload[:48])
Path("aes_nonce.bin").write_bytes(payload[48:])
```

For the ML-KEM private key extraction from Image 2:

The second image uses six DCT positions. The same non-zero coefficient rule, parity extraction, and deterministic shuffle are applied.

```python
import jpegio as jio
import random
from pathlib import Path

IMAGE = "FINAL_CHALL_2.jpg"
SEED = 20260821

POSITIONS = [
    (0, 1),
    (0, 2),
    (1, 1),
    (1, 2),
    (2, 1),
    (2, 2),
]

PAYLOAD_SIZE = 2498

jpeg = jio.read(IMAGE)
Y = jpeg.coef_arrays[0]

candidates = []

height, width = Y.shape

for block_y in range(0, height, 8):
    for block_x in range(0, width, 8):
        for row, col in POSITIONS:
            y = block_y + row
            x = block_x + col

            if Y[y, x] != 0:
                candidates.append((y, x))

rng = random.Random(SEED)
rng.shuffle(candidates)

required_bits = PAYLOAD_SIZE * 8

if len(candidates) < required_bits:
    raise RuntimeError(
        f"Not enough DCT candidates: "
        f"{len(candidates)} available, "
        f"{required_bits} required"
    )

selected = candidates[:required_bits]

bits = [
    abs(Y[y, x]) % 2
    for y, x in selected
]

payload = bytearray()

for i in range(0, len(bits), 8):
    byte = 0

    for bit in bits[i:i + 8]:
        byte = (byte << 1) | bit

    payload.append(byte)

Path("mlkem768.der").write_bytes(payload)
```

The extracted payload is 2498 bytes, which matches the ML-KEM-768 private-key size.

For the Image 3 inspection:

The third image is a PNG containing an additional custom chunk. Its chunk structure can be inspected with `pngcheck`.

```bash
pngcheck -v FINAL_CHALL_3.png
```

The output reveals the custom chunk containing the ML-KEM ciphertext.

For the ML-KEM ciphertext extraction:

The custom chunk can be extracted directly from the PNG.

```python
from pathlib import Path
import struct

PNG = "FINAL_CHALL_3.png"
TARGET = b"ctXT"

data = Path(PNG).read_bytes()
offset = 8

while offset < len(data):
    length = struct.unpack(">I", data[offset:offset + 4])[0]
    chunk_type = data[offset + 4:offset + 8]
    chunk_data = data[offset + 8:offset + 8 + length]

    if chunk_type == TARGET:
        Path("mlkem_ciphertext.bin").write_bytes(chunk_data)
        break

    offset += 12 + length
```

The extracted ciphertext is 1088 bytes, matching the ML-KEM-768 ciphertext size.

For the ML-KEM-768 decapsulation:

The 2498-byte private key and the 1088-byte ciphertext are used together to recover the ML-KEM shared secret.

```bash
openssl pkeyutl \
    -decap \
    -inkey mlkem768.der \
    -keyform DER \
    -in mlkem_ciphertext.bin \
    -secret shared_secret.bin
```

The resulting shared secret can be checked with:

```bash
xxd -p shared_secret.bin
```

For the AES-256 key derivation:

The ML-KEM shared secret is used as the input key material for HKDF-SHA256. The information string is `CTF-AES-256-GCM`, and the output length is 32 bytes.

```bash
openssl kdf -binary \
    -keylen 32 \
    -kdfopt digest:SHA256 \
    -kdfopt key:$(xxd -p -c 256 shared_secret.bin) \
    -kdfopt info:CTF-AES-256-GCM \
    -kdfopt mode:EXTRACT_AND_EXPAND \
    HKDF > aes_key.bin
```

Verify the derived key:

```bash
xxd -p aes_key.bin
```

The resulting AES-256 key is:

```text
b7a85ccc454bae8b8eab9af0fe946ddbcc51538eb5557895ffd16a7f050ba06f
```

For the AES-256-GCM decryption:

The derived AES key is combined with the ciphertext and nonce recovered from Image 1.

```python
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

key = Path("aes_key.bin").read_bytes()
ciphertext = Path("aes_ciphertext.bin").read_bytes()
nonce = Path("aes_nonce.bin").read_bytes()

flag = AESGCM(key).decrypt(nonce, ciphertext, None)
print(flag.decode())
```

AES-GCM verifies the authentication tag during decryption. A mismatch in the key, nonce, ciphertext, or authentication tag causes decryption to fail.

The successful AES-256-GCM decryption reveals the final flag:

```text
CYS{1_@m_iN_+h3_3mp1r3_8u$in388}
```