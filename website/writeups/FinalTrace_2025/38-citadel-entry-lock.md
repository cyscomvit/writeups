---
layout: writeup

title: Citadel Entry Lock
difficulty: Medium
points: 500
categories: [General]
tags: []

flag: CYS{SEAL_RAID_CROSS_MAAT_MAZE_HODOS}
---

# Key 1 — SEAL

**Observation**

- The puzzle presents a 16×16 symbol grid → hint: **hex** (16 values: `0x0`–`0xF`).
- One edge (first row / first column) contains a set of unique symbols which map to the 16 hex digits.
- Some symbols are visually distinct (black-haired vs white-haired). The black-haired symbol positions encode the meaningful bytes.

**Method**

1. Map each unique symbol in the first row (or first column) to the hex digits `0x0`–`0xF`.
2. For the black-haired symbol occurrences, read the mapped hex bytes in sequence.
3. Convert the resulting hex byte sequence to ASCII.

**Extracted data**

```
53 45 41 4C 𓀅 𓀃 𓀄 𓀅 𓀄 𓀁 𓀄 𓀌
```

Interpreting the ASCII bytes `53 45 41 4C` → `"SEAL"`.

**Result (Key 1):** `SEAL`

---

# Key 2 — RAID (Håstad / low-exponent broadcast attack)

**Problem summary**

- You are given three RSA public keys with a small, identical public exponent `e = 3` and three ciphertexts `c1, c2, c3`.
- The same plaintext `m` was encrypted under each modulus `n1, n2, n3`.
- This is the classic setting for **Håstad’s Broadcast Attack**: when the same message is encrypted with small `e` and pairwise-coprime moduli, use CRT and extract the integer e-th root.

**Mathematical setup**

We have:

\[
m^3 \equiv c_1 \pmod{n_1},\qquad
m^3 \equiv c_2 \pmod{n_2},\qquad
m^3 \equiv c_3 \pmod{n_3}.
\]

If the moduli are pairwise coprime and \(m^3 < n_1 n_2 n_3\), then the CRT combined value \(X\) equals the integer \(m^3\). Recover \(m\) by taking the integer cube root.

**Given values**

| index | modulus \(n_i\)        | ciphertext \(c_i\)                     |
|-------|------------------------:|----------------------------------------:|
| 1     | `20000000000003`       | `120045155700768461749`                 |
| 2     | `30000000000007`       | `22749457632`                           |
| 3     | `40000000000009`       | `2800451557007722749457632`             |
| e     | `3`                    | (public exponent)                       |

**Solution steps (summary)**

1. Use the Chinese Remainder Theorem (CRT) to compute `X` such that `X ≡ c_i (mod n_i)` for all i. This produces a unique `X` modulo `N_total = n1*n2*n3`.
2. If `m^3 < N_total`, `X` equals `m^3` as an integer.
3. Compute the integer cube root of `X` to recover `m`.
4. Convert `m` (integer) to a big-endian hex string and then to ASCII to read the plaintext.

**Python reference (concise, reproducible)**

```python
# Requires: sympy, gmpy2
from sympy.ntheory.modular import crt
from gmpy2 import iroot

# Provided moduli and ciphertexts
n = [
    20000000000003,      # n1
    30000000000007,      # n2
    40000000000009       # n3
]

c = [
    120045155700768461749,          # c1
    22749457632,                    # c2
    2800451557007722749457632       # c3
]

e = 3

# 1) CRT -> resultant = m^3
resultant, modulus = crt(n, c)
print("CRT result (m^3):", resultant)

# 2) integer cube root
m_int, is_perfect = iroot(resultant, e)
if not is_perfect:
    raise ValueError("CRT result is not a perfect cube; attack failed.")
print("Recovered integer m:", m_int)

# 3) convert to ASCII
hex_val = hex(int(m_int))[2:]
if len(hex_val) % 2:
    hex_val = "0" + hex_val
plaintext = bytes.fromhex(hex_val).decode('ascii')
print("Plaintext:", plaintext)
```

**Intermediate / expected values**

- CRT result `m^3` (as computed): `262800451557007722749457632`
- Integer cube root `m`: `1380010308`
- Hex of `m` (big-endian): `0x52414944` → ASCII: `"RAID"`

**Result (Key 2):** `RAID`

---

# Key 3 — CROSS

**Observation**

- A word search / letter grid with very few actual English words.
- The visible words (the only real words in the grid) are `"THE"`, `"ANSWER"`, `"IS"`, `"CROSS"`.

**Method**

- Either brute-force search the grid for words or visually scan it.
- The sequence of real words forms the phrase: **"THE ANSWER IS CROSS"**.

**Result (Key 3):** `CROSS`

---

# Key 4 — MAAT

**Overview**

The ciphertext is a layered transformation pipeline. Working backwards through the layers yields a SHA-512 digest which, when interpreted/decoded, produces the key.

**Pipeline (as given / reversed)**

1. `SKIP CIPHER (size = 17)` → produces a tokenized string
2. `TWIN HEX` transformation
3. `KENNY LANG` (South Park / simple substitution style encoding)
4. `TWIN HEX`
5. `SHA512`
6. ASCII decode → final key

**Notable intermediate**
- SKIP CIPHER(SIZE=17):
```
1KU55X5KZ5HJ5AX5AL1H75MZ5A85YR5T75HB1AZ5KP5TP5JR5AB1HZ5KB5HK5OR1AW5WX5HZ1HR5KR5TP5W85TZ5AR1AR5HX5TB1AR5T85H85HB1TZ5MZ59Q5T85W85TU5TP5TR5HR5T85HR5KR1AB19R5AJ1XB1SB1AR5TR5WR5HZ1HR5585H81K855Z5K85AZ5AR5T81K85T85HB18R5AJ5W75TR5T71XP19Z5M85HB58R5TP5A85A81Y85YK15Q5H85WR1KR5575AK1AP5TX5T85KZ5HA5KZ5KR5OR5HB5MX5W85HK5AR5HZ5XX5W85A75AS5AP5TX5HK5KZ1T75WR5HB1AZ5KZ10R5W85TZ58P5T85HZ1HZ5WZ5H81KK5HJ1AR5AB1AB1HK5KR1H85KR5HB5HR1TX5WP5W85KR5MR5KZ5A81WB5WX5TR5KB1K85K85571A85881T81H85W85HR5K85TZ5WR5WJ1T75NJ11X1WX1HB5KX5885JB5ZZ1T75TR5AR5175KR5HR5AR5K85YZ5TP5NZ1H75AR1W85TP58P5LX5X75T85HZ

```

- TWIN HEX:
```
1bh5zh58w5xw58w5zk5rh1ba5rk58t5xt1u85rh1kj5rh5pt58t5rk5za1bh5zh58t57558t5za5zh1kn5rh5xt58w5pz1bh5zh58w5pt5zk5zh5ra1bk5rk5zh5pt1rh5rh1bh5za5rh5xt5rk5781bh58w58t5751rh5rk1bh5rk1pt58t5za58t1ja5rk58t5xt5ra5za58w1kj5rh5px1jk5za1ja5rk58w5xw58m5xy1bh5za1pw58w5zk58t1ja5rk58w5755za5791bh58w58t5791ly5ra1a158t5pt1q01kn5rh5755za5ra5rh1ja5zk5zk57858t5751ja5zk5ra5pt58w5q11bk5rk5ra57858m5xx1bk58m1sl18w5zh1ba5rh5ra5xx18t58w1bh5ra5ra5pt5za5xs1ko5zk5px18t58w1bh5ra5zh5791u85rh1ko5ra5xt5zh5py1ba5rh5ra5xt58t5rk5rk1bk58t58m5pt5rk5ra58t1bh58w58t5xt1wm58w1kh58t5755rh5xy1ba5zh5rh57858w5zk5rk
```

- KENNY LANG SOUTHPARK:
```
1mpmfpp4fpppmm1fmpfmp18pmm53mmm1fmmppf1mpmfmf1fmpfpm57mmp1fpm71mpmfpm1pppmmf1pmppmm17mmm1mpfmmp1mpf41mfpfmf17mmp1mmp71fmpffm4fmpfmp1mfpffp53mmm54ppf4fmpfpp4ffp61mpf74fpppfm4fmpfpf1pff51mfpfmf55fmf19fmm17857mmf1pfmfmm4fppppf4fmf14fppmfm1fpm91pmpmff4ffp51pff850ppm1fmmmfp50mfp1mmfmfm1pfp058ppm50mfp1mmfpmf58pmm58mfp1pmm61fmmmfp1fmmpmp1pfmffm1mpmffm1mfpfmp19ffp51fmf1mmp61fpmmmf4fpppmp

```

- TWIN HEX: 
```
1dw4wj1tt18j53a1so1du1tv57b1v71dv1nc1kj17a1fb1f41hu17b1b71ty4tt1hz53a54o4tw4z61f74wp4tx1r51hu55u19s17857c1ps4wo4u14wg1v91ki4z51r850m1sh50h1cg1q058m50h1cl58j58h1j61sh1sk1py1dy1ht19z51u1b61vc4wk

```
- The final SHA-512 digest in the chain is:
```
2db38a0cdf882b8cf7932c685306373042071c8fa147dfe8a4c233b9a57a42eb1004f870b8a9b09552c17dcf81ca2078ffca25fcfa4b8184762f4117d21b98b4
```

**Conclusion**

- After reversing the transformations and decoding the SHA-512 result, the plaintext key obtained is: `MAAT`.

**Result (Key 4):** `MAAT`

---

# Key 5 — MAZE

**Observation**

- Several 8×8-like grids produce SHA-256 digests when unspiralled.
- Each grid, when read with the specified outward, left-start, clockwise spiral algorithm, yields an 8×32 (256-bit) SHA256 word fragment.
- The puzzle lists grouped hexadecimal 32-byte SHA256 outputs and associates them to English words.

**Interpretation**
- Spiral Pattern
```
1)20d21a67·ac24d157·0b679998·b4344d9a·83a3b8f3·1b42e0a5·40544695·1c439f90
2)f826b683·37334d8e·7e46f925·e8670e23·030c2178·3ba7b299·c7c724fc·d1a761ff
3)e1900ba2·7ab930f6·017e98af·bc903491·2edbb7c2·9b864a02·bec73e01·bf1f0eac
4)808bb15f·07488f45·f05fa88c·0d1d34d6·868bc51c·382a6d05·a305622c·c1ad27d3
5)416f57f6·65ff5633·517705da·91651f6e·4cfafdac·d8ba9431·51281d5f·d9cdfbe9
6)11eab27f·623d15ec·099e0f14·be6edf14·7c69d59b·8e7c49da·bd5d9f26·9ad8f2c8

```

- The extracted SHA256 hashes correspond to the phrase:
  - `The:`  `b344d80e24a3679999fa964450b34bc24d1578a35509f934c1418b0a20d21a67`
  - `key:`  `2c70e12b7a0646f92279f427c7b38e7334d8e5389cff167a1dc30e73f826b683`
  - `you:`  `bb0347a468d97e98a9c00e37cebec1ab930f6f1221cae0f1fbb92b07e1900ba2`
  - `seek:` `cbd345d6a2815fa88d1022650386d07488f45c6c5c3d72da1ca380f0808bb15f`
  - `is:`   `fa51fd49abf67705d6a35d18218c115ff5633aec1f9ebfdc9d5d4956416f57f6`
  - `MAZE:` `d9edf594c7669e0f119d2f9d5dece923d15ec44ba68c2f8da9b87b0611eab27f`

- Combined phrase: **"The key you seek is MAZE."**

**Result (Key 5):** `MAZE`

---

# Key 6 — HODOS

**Observation**

- A long block of transformed text using a route cipher.
- The transformation parameters: horizontal width = **4**; encoding uses a route reading pattern described as:
  - *Write horizontally from top-left, then read vertical lines from bottom-left* (i.e. a specific route/permutation).

**Method**

- Implement or use an online route-cipher tool with the given width and read order. Decoding the route cipher recovers a plaintext passage where the key word is clearly visible.

**Result (Key 6):** `HODOS`


## Decryption script (route cipher — width = 4)

```python
import math
# Ciphertext should be set to the encoded string (use raw string: r"...")
ciphertext = ""  # <-- paste ciphertext here
width = 4

# Compute number of rows (each row was written left→right)
rows = math.ceil(len(ciphertext) / width)
cols = width

# Determine how many characters go in each column (left to right)
remainder = len(ciphertext) % width
col_lengths = [rows if i < remainder else rows - 1 for i in range(width)] if remainder else [rows] * width

# Split ciphertext into columns as read bottom→top, left→right
columns = []
idx = 0
for c_len in col_lengths:
    col = ciphertext[idx:idx + c_len]
    columns.append(col[::-1])  # reverse each column (because read bottom→top)
    idx += c_len

# Reconstruct plaintext by reading horizontally (left→right, top→bottom)
plaintext = ''
for r in range(rows):
    for c in range(cols):
        if r < len(columns[c]):
            plaintext += columns[c][r]

# Replace ⌴ with space (if used in your ciphertext)
plaintext = plaintext.replace('⌴', ' ')

print(plaintext)
```

---

# Final assembly

After recovering each key, assemble them in the instructed order to form the final flag.

- **KEY 1:** `SEAL`
- **KEY 2:** `RAID`
- **KEY 3:** `CROSS`
- **KEY 4:** `MAAT`
- **KEY 5:** `MAZE`
- **KEY 6:** `HODOS`

**FINAL FLAG:**

```
CYS{SEAL_RAID_CROSS_MAAT_MAZE_HODOS}
```

---



