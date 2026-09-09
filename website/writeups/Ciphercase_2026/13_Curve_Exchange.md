---
layout: writeup

title: CurveExchange
difficulty: Hard
points: 500
categories: [Crypto]
tags: [ECC, ECDH, Invalid-Curve, Small-Subgroup, CRT]

flag: CYS{dynamic}
---

# CurveExchange

**Author:** htarizzs

This is a cryptography CTF challenge exploiting a classic **ECDH Invalid-Curve / Small-Subgroup Attack** combined with the **Chinese Remainder Theorem (CRT)** to fully recover the server's private scalar.

---

## Understanding the Setup

Connecting to the service gives us an interactive menu:

```
╔══════════════════════════════════════════╗
║       CURVEEXCHANGE KEY AGREEMENT        ║
╚══════════════════════════════════════════╝

  [1]  View curve parameters
  [2]  Request server public key
  [3]  Submit client public point
  [4]  Derive shared secret (key confirmation)
  [5]  Get encrypted flag
  [6]  Exit
```

Selecting option `[1]` reveals the curve parameters for a custom 72-bit elliptic curve over a prime field:

```
p       = 3541774862152233910451
a       = 3541774862152233910448   (= -3 mod p)
b       = 5
G.x     = 948593498517026279058
G.y     = 1065975613846311390974
order   = 3541774862209346234424
```

And option `[5]` gives us the encrypted flag (AES-256-GCM), along with the hint that the key is derived as:

```
key = HKDF-SHA256(
    ikm   = server_private_scalar (big-endian, 17 bytes),
    salt  = b"ecdh-challenge-v1",
    info  = b"flag-encryption-key",
    len   = 32
)
```

So to decrypt the flag, we need to recover the server's private scalar `d`.

---

## Reading the Source Code

The challenge provides `server.py`. The critical insight is buried in the comments of `_recv_client_point`:

```python
# NOTE: We intentionally do NOT validate that the point lies on the
# curve  y^2 = x^3 + ax + b  (mod p).  This preserves compatibility
# with clients that may transmit points using alternative parameter
# sets or compressed representations.
self.client_point = (x, y)
```

The server only checks that the coordinates are in range `[0, p)` — it never verifies that the submitted point actually satisfies `y^2 = x^3 + ax + b (mod p)`.

Meanwhile, the point arithmetic in `_point_add` and `_scalar_mult` uses only the coefficient `a` (not `b`) in its formulas:

```python
# Point doubling:
lam = (3 * x1 * x1 + a) * pow(2 * y1, -1, p) % p
# Point addition:
lam = (y2 - y1) * pow(x2 - x1, -1, p) % p
x3 = (lam * lam - x1 - x2) % p
y3 = (lam * (x1 - x3) - y1) % p
```

This is the fundamental property of the Short Weierstrass addition law — `b` only determines *which* points lie on the curve; it plays no role in the actual arithmetic. This is the root cause of the vulnerability.

---

## The Vulnerability: Invalid-Curve Attack

Since the server:
1. Does **not** validate that submitted points lie on the intended curve, and
2. Computes `S = d x ClientPoint` using formulas that only care about `a` and `p`,

...we can submit a point `P` that lies on a *different* curve `y^2 = x^3 + ax + b'` (same `a`, same `p`, but a different constant `b'`). The server will happily compute `S = d x P` using the same formulas, producing a valid result on the *invalid* curve `E'`.

### Why Does This Help?

If we pick `b'` such that the curve `E'` has an order `n'` with **small prime factors**, we can find points of **small order** on `E'`. Suppose `P` has order `r` on `E'`. Then:

```
d x P = (d mod r) x P
```

The server's computation of `d x P` only reveals `d mod r`. But crucially, the server provides a **key confirmation oracle**: it encrypts the known plaintext `ECDH_KEY_CONFIRMATION_OK` with a key derived from the shared secret `S`. We can brute-force all `r` possible values of `k` in `[1, r)`, compute `k x P`, derive the trial key, and attempt decryption. When decryption succeeds, we learn `d ≡ k (mod r)`.

---

## The Attack: Step by Step

### Step 1 — Find Invalid Curves with Small-Order Points

We search over different values of `b'` and compute the group order of `y^2 = x^3 + ax + b'` over `F_p` using Baby-step Giant-step (BSGS). For each candidate order `n'`, we factor it and look for **small prime factors `r`** (roughly `r < 5000`).

Some useful invalid curves discovered:

| b' | Small prime `r` |
|----|-----------------|
| 6  | 3, 5, 11        |
| 7  | 41, 487         |
| 10 | 163, 661, 2029  |
| 11 | 619             |
| 12 | 29, 191         |
| 14 | 43              |

### Step 2 — Find a Point of Order `r`

For each small prime `r` dividing `n'`, we pick a random point `P_rand` on the invalid curve and compute:

```python
Pt = scalar_mult(n_prime // r, P_rand, a, p)
```

This kills off all other prime-order components, leaving a point `Pt` of order exactly `r`.

### Step 3 — Oracle Query

We submit `Pt` to the server (option `[3]`) and immediately request key confirmation (option `[4]`). The server responds with:

```
nonce      = <random 12 bytes>
ciphertext = <AES-GCM encrypted "ECDH_KEY_CONFIRMATION_OK">
tag        = <16-byte auth tag>
```

Internally, the server computed `S = d x Pt = (d mod r) x Pt`.

### Step 4 — Brute-Force `d mod r`

We try every `k` from `1` to `r - 1`:

```python
for k in range(1, r):
    kP = scalar_mult(k, Pt, a, p)
    trial_key = hkdf_sha256(
        kP[0].to_bytes(...) + kP[1].to_bytes(...),
        salt=b"ecdh-session-v1",
        info=b"aes-key-confirmation"
    )
    pt = aes_gcm_decrypt(trial_key, conf_nonce, conf_ct, conf_tag)
    if pt == b"ECDH_KEY_CONFIRMATION_OK":
        d_mod_r = k
        break
```

Since `r` is small (< 5000), this brute-force is trivial.

### Step 5 — Chinese Remainder Theorem

After collecting enough congruences `d ≡ ki (mod ri)` across multiple invalid curves, we apply the Chinese Remainder Theorem. Once the product of all `ri` exceeds `d`, the CRT gives us the **unique** value of `d`:

```
d ≡ k1  (mod r1)
d ≡ k2  (mod r2)
    ...
d ≡ k12 (mod r12)
─────────────────────────────────────────────────────────────────
Product = 3 x 5 x 11 x 29 x 41 x 43 x 163 x 191 x 487 x 619 x 661 x 2029 ≈ 2^76
d ≈ 2^68  -->  Product > d  [OK]
```

```python
M = product_of_all_r
d_recovered = 0
for (a_i, m_i) in remainders:
    Mi = M // m_i
    yi = pow(Mi, -1, m_i)          # modular inverse
    d_recovered = (d_recovered + a_i * Mi * yi) % M
```

### Step 6 — Decrypt the Flag

With `d` in hand, we derive the flag key and decrypt:

```python
d_bytes = d_recovered.to_bytes(17, 'big')
flag_key = hkdf_sha256(d_bytes, 32,
                       salt=b"ecdh-challenge-v1",
                       info=b"flag-encryption-key")
flag = aes_gcm_decrypt(flag_key, flag_nonce, flag_ct, flag_tag)
print(flag.decode())
```

---

## Running the Solver

```bash
python3 solve.py <HOST> 9999
```

Sample output:

```
[*] Connecting to 127.0.0.1:9999...
[*] Retrieving curve parameters...
    p     = 3541774862152233910451  (72 bits)
    a     = 3541774862152233910448
    b     = 5
    order = 3541774862209346234424
[*] Retrieving encrypted flag...
[*] Searching for invalid-curve points with small-order subgroups...
    [OK] r=    3  d mod 3  = ?   product=2^2
    [OK] r=    5  d mod 5  = ?   product=2^4
    [OK] r=   11  d mod 11 = ?   product=2^6
    [OK] r=   29  d mod 29 = ?   product=2^10
    ...
    [OK] r= 2029  d mod 2029 = ? product=2^76

[*] Collected 12 congruences, product ~= 2^76
[*] Applying Chinese Remainder Theorem...
    Recovered d = 361623542354585744737
[*] Deriving flag encryption key...
[*] Decrypting flag...

==================================================
  FLAG: CYS{dynamic}
==================================================
```

---

## Why This Works (TL;DR)

| Property | Detail |
|----------|--------|
| **Missing validation** | Server accepts any `(x, y)` without checking `y^2 = x^3 + ax + b` |
| **`b`-free arithmetic** | Short Weierstrass addition formulas don't use `b`, so they work on *any* curve with the same `a` and `p` |
| **Small-subgroup oracle** | A point of order `r` leaks `d mod r` via at most `r` key-confirmation queries |
| **CRT reconstruction** | Enough small-modulus residues uniquely determine `d` when their product exceeds `d` |

The attack is the classic **ECDH Invalid-Curve Attack** described by Antipa et al. (2003) and is the reason standards like NIST SP 800-56A mandate strict **public-key validation** before performing any scalar multiplication.
