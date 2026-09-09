---

layout: writeup



title: Saul's Evidence Chain
difficulty: Hard
points: 500
categories: [Crypto]
tags: [SHA-256, Hash Collision, AES-GCM, XOR, Cryptography]



flag: CYS{saul_forged_the_chain_not_the_evidence}



#Saul's Evidence Chain



Author: Srishant



This is a cryptography-based CTF challenge involving a weak SHA-256 hash chain, a truncated hash collision, XOR encryption, and AES-256-GCM.

The challenge provides an evidence archive containing several JSON records, a manifest, an encrypted archive index, and an encrypted backup note.

#### 

#### 1. Inspect the Evidence Chain

First, we inspect `manifest.txt`:


001 previous=000000 hash_prefix=096988
002 previous=096988 hash_prefix=fdbedc
003 previous=fdbedc hash_prefix=1c5bfc
004 previous=1c5bfc hash_prefix=00211c
005 previous=00211c hash_prefix=471cbf
006 previous=471cbf hash_prefix=6cc28a


Each record contains a SHA-256 hash, but only the first 6 hexadecimal characters of the hash are used as the link to the next record.

A complete SHA-256 hash contains 64 hexadecimal characters:

64 × 4 = 256 bits

However, the challenge only uses:

6 × 4 = 24 bits

Therefore, the chain is only protected by a 24-bit hash prefix.

#### 2. Find the Suspicious Record

Record 003 is suspicious:

json
{
  "id": 3,
  "timestamp": "2009-03-15T22:14:08",
  "label": "Chemical delivery manifest",
  "payload": "Methylamine delivery paperwork. ORIGINAL SCAN DELETED. SEE BACKUP LOCKER.",
  "nonce": 26571939,
  "previous": "fdbedc",
  "hash": "1c5bfce913d44c9c35d467409fb3ab4b92de9842f6734ab01991a22d5704d214"
}


Unlike the other records, Record 003 has a non-zero nonce.



The payload also tells us:
ORIGINAL SCAN DELETED. SEE BACKUP LOCKER.



This suggests that Record 003 has been modified.

#### 

#### 3. Exploit the Weak Hash Commitment

The important weakness is that the chain only checks:

python
sha256(record)[:6]


instead of the complete SHA-256 digest.

Record 004 tells us what hash prefix Record 003 must produce:

previous = 1c5bfc


Therefore, we can brute-force the nonce until the modified Record 003 produces the required prefix.

The basic search is:

python
import hashlib
import json

r3 = json.load(open("evidence/003.json"))
target = "1c5bfc"

def canonical(r):
    return f'{r["id"]}|{r["timestamp"]}|{r["label"]}|{r["payload"]}|{r["nonce"]}'.encode()

for nonce in range(100_000_000):
    r3["nonce"] = nonce

    h = hashlib.sha256(canonical(r3)).hexdigest()

    if h[:6] == target:
        print("Collision nonce:", nonce)
        print("Hash:", h)
        break


This recovers:
Collision nonce: 26571939


The resulting hash begins with:
1c5bfc


which is exactly what Record 004 expects.

The important point is that the complete hash does not need to match. Only the first 6 characters need to match.

#### 4. Recover the Original Record

The manifest contains another important clue:
ARCHIVE INDEX: record 003
Index protection: collision nonce (4-byte big-endian, repeating XOR)


So the recovered collision nonce is also the key for `archive.idx`.

Convert the nonce into a 4-byte big-endian value:

python
nonce = 26571939
key = nonce.to_bytes(4, "big")


The resulting key is:

01 94 89 6b



The archive index is encrypted using this key repeatedly:

01 94 89 6b 01 94 89 6b 01 94 89 6b ...


Decrypt it with:

python
data = open("archive.idx", "rb").read()

plain = bytes(
    b ^ key[i % 4]
    for i, b in enumerate(data)
)

print(plain.decode())


This reveals the original Record 003.

The original record has a different payload and nonce, but its full SHA-256 hash begins with the same 6 characters:
1c5bfc


The original full SHA-256 hash is:

1c5bfcf476ee5a42529f8ee713fc7e5073a23599bb568bd046bb49765c49d799


#### 5. Understand the Collision

The forged Record 003 has the hash:
1c5bfce913d44c9c35d467409fb3ab4b92de9842f6734ab01991a22d5704d214


The original Record 003 has:

1c5bfcf476ee5a42529f8ee713fc7e5073a23599bb568bd046bb49765c49d799


The complete hashes are different.

However:

Forged:   1c5bfc
Original: 1c5bfc


Therefore, both records satisfy the 24-bit commitment used by the chain.

This allows the forged record to replace the original without breaking the visible chain.

The vulnerability is therefore a truncated SHA-256 collision.

#### 6. Recover the AES Key

The full SHA-256 hash of the original Record 003 is used as the AES-256-GCM key.

Convert the hexadecimal digest into bytes:

python
key = bytes.fromhex(
    "1c5bfcf476ee5a42529f8ee713fc7e5073a23599bb568bd046bb49765c49d799"
)


This gives a 32-byte key, which is suitable for AES-256.

#### 7. Decrypt `locker.enc`

The challenge uses AES-256-GCM.

The encrypted file is structured as:
12-byte nonce || ciphertext || 16-byte authentication tag


We can decrypt it with:

python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

data = open("locker.enc", "rb").read()

nonce = data[:12]
ciphertext = data[12:]

key = bytes.fromhex(
    "1c5bfcf476ee5a42529f8ee713fc7e5073a23599bb568bd046bb49765c49d799"
)

plaintext = AESGCM(key).decrypt(
    nonce,
    ciphertext,
    None
)

print(plaintext.decode())


The decrypted backup note contains the final flag.

#### 8. Flag

CYS{saul_forged_the_chain_not_the_evidence}


#### 9. Vulnerability Summary

The challenge relies on a weak implementation of a hash chain.

Instead of storing the complete SHA-256 digest, the application only stores:
SHA256(record)[:6]


This reduces the integrity protection from 256 bits to only 24 bits.

An attacker can therefore modify Record 003 and brute-force its nonce until its SHA-256 hash begins with the same 6-character prefix as the original.

The chain then appears valid even though the underlying record has been changed.

The recovered collision nonce is also used to decrypt `archive.idx`, which contains the original Record 003. Its full SHA-256 hash is then used as the AES-256-GCM key to decrypt the final backup note.

The key lesson is that SHA-256 itself is not broken. The vulnerability comes from truncating the hash to only 24 bits when using it as an integrity commitment.

