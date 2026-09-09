---
layout: writeup

title: ECHO Intercept
difficulty: Medium
points: 300
categories: [Crypto]
tags: [AES-GCM, Nonce Reuse]

flag: CYS{d5f69cd87d635c915132}
---

ECHO Intercept

Author: Divya Dharshini S G

This is a cryptography-based CTF challenge involving **AES-128-GCM nonce reuse**.

We are provided with approximately 6000 encrypted packets. Each packet contains a packet ID, nonce, ciphertext, and authentication tag.

The important vulnerability is that exactly one 12-byte nonce is reused by two packets. One of these packets contains a known heartbeat message:

```text
USR PING_OK_1234
```

The objective is to use the nonce reuse vulnerability to forge a valid authenticated packet containing:

```text
ADM OPEN_VAULT01
```

which causes the server to return the flag.

## Finding the Reused Nonce

Since the nonce is 12 bytes, we can first analyze the traffic and count the frequency of each nonce rather than attempting to decrypt all 6000 packets.

The challenge guarantees that there are 5999 unique nonces, meaning exactly one nonce appears twice.

The two packets using the same nonce are separated in the shuffled log, so they may not be adjacent.

Once the duplicated nonce is identified, we have our two ciphertexts encrypted using the same AES-GCM nonce.

## Recovering the Keystream

AES-GCM uses counter mode for encryption. Reusing a nonce causes the same CTR keystream to be used for both packets.

For two ciphertexts:

```text
C1 = P1 XOR S

C2 = P2 XOR S
```

where `S` is the shared keystream.

One of the colliding packets is the known heartbeat:

```text
USR PING_OK_1234
```

It is exactly 16 bytes long.

Therefore, we can recover the keystream using:

```text
S = C_heartbeat XOR P_heartbeat
```

We can then XOR this keystream with the ciphertext of the second packet to recover its plaintext.

## Recovering the GCM Authentication Key

Recovering the CTR keystream is not enough because AES-GCM also authenticates the ciphertext.

The GCM authentication subkey is:

```text
H = AES_K(0^128)
```

Since both packets use the same nonce and associated data, their authentication tags use the same AES-generated authentication mask.

By XORing the authentication equations for the two packets, the common authentication mask cancels out.

For the fixed one-block packet structure used in this challenge, the resulting equation contains `H²`.

Because squaring is a bijection in `GF(2^128)`, we can recover `H` using the field square-root/Frobenius operation.

The required finite-field operations are implemented in `gf128.py`.

## Recovering the Authentication Mask

Once `H` is recovered, we can evaluate GHASH for one of the known colliding packets.

Using the corresponding authentication tag, we can then recover the authentication mask associated with the reused nonce.

This gives us the information required to generate a valid GCM authentication tag for a new ciphertext.

## Forging the Vault Packet

The target plaintext is:

```text
ADM OPEN_VAULT01
```

We use the recovered CTR keystream to encrypt the target plaintext.

The recovered GHASH authentication information is then used to calculate a valid authentication tag for the forged ciphertext.

The resulting packet is submitted to:

```text
POST /vault
```

The server verifies the authentication tag before decrypting the packet.

If the packet is valid, the server decrypts it and checks that:

```text
role = ADM 
body = OPEN_VAULT01
```

When both checks succeed, the server returns the flag.

## Important Observation

This challenge cannot be solved using XOR alone.

Nonce reuse allows us to recover the CTR keystream and therefore decrypt or encrypt messages, but a forged packet must still contain a valid **GCM authentication tag**.

Therefore, the complete solution requires understanding both:

- AES-GCM's CTR encryption
- GCM's GHASH authentication

The complete attack chain is:

```text
6000 encrypted packets
        ↓
Find repeated nonce
        ↓
Identify known heartbeat packet
        ↓
Recover CTR keystream
        ↓
Recover GCM authentication subkey H
        ↓
Recover authentication mask
        ↓
Encrypt ADM OPEN_VAULT01
        ↓
Generate valid GCM tag
        ↓
POST /vault
        ↓
Flag
```

## Flag

```text
CYS{d5f69cd87d635c915132}
```