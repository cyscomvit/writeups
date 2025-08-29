---
layout: writeup

title: RSA Hard
difficulty: hard
points: 400
categories: [cyptography]
tags: []

flag: CBCV{cryptanalysis}
---

### RSA Hard
* Author: Om Mishra

## Challenge (what participant gets)

You are given:

n = 5860838794991910814284665112683385463954646048771125316431872432348926417447

e1 = 17

e2 = 65537

c1 = 3720477122812330210392570666622835188001585746013783461634956703564926609316

c2 = 2374066440947720297446444451505697411347728841883956859393928588819879545418


Recover the original plaintext (ASCII) and submit it as the flag.



## Hints
- `gcd(e1, e2) = 1` → find integers `a,b` such that `a*e1 + b*e2 = 1`.
- Use: `m = (c1^a * c2^b) mod n`. For negative exponents, use modular inverses.
- Convert integer `m` → bytes → ASCII.

---

## Walkthrough
1. Compute extended gcd to get `a, b` with `a*e1 + b*e2 = 1`.  
2. Compute `part1 = c1^a (mod n)` (handle negative `a` via inverse).  
3. Compute `part2 = c2^b (mod n)` (handle negative `b`).  
4. `m = (part1 * part2) % n`. Convert `m` to bytes → that is the flag.

Expected flag (hidden): `CBCV{cryptanalysis}`

---

## Reference solver
```python
# solver_rsa_common.py
# Pure-Python solver for RSA common modulus challenge.

def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise ValueError("No inverse")
    return x % m

def modexp_with_signed_exponent(base, exp, mod):
    if exp >= 0:
        return pow(base, exp, mod)
    inv = modinv(base, mod)
    return pow(inv, -exp, mod)

n  = 322373040362292717649168841216788477297
e1 = 17
e2 = 65537
c1 = 12755149773111262113925394772571626614
c2 = 199765691046492609176467359736241258709

g, a, b = egcd(e1, e2)
if g != 1:
    raise SystemExit("e1 and e2 are not coprime")

print("Found coefficients a, b:", a, b)

part1 = modexp_with_signed_exponent(c1, a, n)
part2 = modexp_with_signed_exponent(c2, b, n)
m = (part1 * part2) % n

# convert int -> bytes
def int_to_bytes(x):
    if x == 0: return b'\x00'
    length = (x.bit_length() + 7) // 8
    return x.to_bytes(length, 'big')

pt = int_to_bytes(m)
print("Recovered bytes:", pt)
print("Recovered string:", pt.lstrip(b'\x00').decode('utf-8'))

```

### Final flag recovered is:
## CBCV{cryptanalysis}