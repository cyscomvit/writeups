---
layout: writeup

title: VENONA
difficulty: Easy
points: 200
categories: [Crypto/Steg]
tags: []

flag: CYS{V3N0N4_CR4CK5_TH3_BLU3_M3TH_C0D3}
---

VENONA

Author : Daniyyel Franx

## Files handed to solvers
- `cover.png` — real Fantasian-alphabet hint image with `secret.zip` appended after IEND
- `cipher.png` — two intercepted ciphertexts (C1, C2), a visible faint clue line, K2 in EXIF


## Step-by-step solution

1. **Decode the glyphs** on `cover.png` using the real Fantasian alphabet →
   `"NOT EVERYTHING VISIBLE IS ALL THERE IS"` — nudges solver to inspect the file, not just view it.

2. **Extract the zip.** Either works:
   - `binwalk cover.png` (finds it as a Zip archive at offset 36303)
   - `unzip cover.png` directly (Info-ZIP self-corrects the offset; prints a harmless warning)

   This produces `flag.enc` — inside a password-protected zip.

3. **Open `cipher.png`.** Visible: two hex strings (C1, C2), and a faint light-grey line
   reading **"I LOVE VENONA"** — flavor + functional crib, nodding to the real VENONA project
   (Soviet one-time-pad key reuse let cryptanalysts break "unbreakable" ciphers).
   Run `exiftool cipher.png` → `Comment` field → this is **K2**, needed later (step 6).

4. **Crib-drag the two-time pad.**
   ```
   C1 = ZIP_PASSWORD XOR K
   C2 = "I LOVE VENONA STOP MEET AT DAWN..." XOR K      (same K — the bug)
   C1 XOR C2 = ZIP_PASSWORD XOR "I LOVE VENONA"
   (C1 XOR C2) XOR "I LOVE VENONA" = ZIP_PASSWORD
   ```
   → recovers the zip password: `Kryptos_Venon`

5. **Unlock the zip:** `unzip -P "Kryptos_Venon" cover.png` →
   `flag.enc` contains:
   `TRLsUeVtUBL0IBUhTugfJRZrIuDrURP1IYWhJBH0TOEfTeZ5HYQgUODsJOIeIRZ1ThD3IOWgURDtHOf4T2UdIhAfIuTsIOf1IhT=`

6. **Peel the final layer** (built as flag → XOR K2 → hex → base64 → ROT21, so undo in reverse):
   - Apply **ROT5** (not ROT21 again — ROT21 is not self-inverse; 21+5=26) → valid Base64
   - Base64-decode → hex string
   - Hex-decode → raw bytes
   - XOR those bytes with **K2** (cyclically) →

   **`CYS{V3N0N4_CR4CK5_TH3_BLU3_M3TH_C0D3}`**

## Full command sequence (copy-paste)

```bash
# 1. Recon + carve the zip out of cover.png
file cover.png
binwalk cover.png
unzip cover.png                      # or: binwalk -e cover.png

# 2. Recon on cipher.png
exiftool cipher.png                  # Comment: ee4651a612cc87e9  (= K2)
# "I LOVE VENONA" is directly visible (faint grey) near the bottom of the image

# 3. Crib-drag + full decode, all in one script
python3 << 'EOF'
import base64

C1 = bytes.fromhex("8dc0e7f2016a0115b4f1485d64")
C2 = bytes.fromhex("8f92d2cd2340521ca7da697c4b9e2a436cfe6be96bd4dec16d07c1a713a1a80555b00cdee66a9e4605d4c39e54e52bd5c8b223b20e60")
CRIB = "I LOVE VENONA"

xor_c1c2 = bytes(a ^ b for a, b in zip(C1, C2))
zip_pw = bytes(a ^ b for a, b in zip(xor_c1c2, CRIB.encode())).decode()
print("ZIP password:", zip_pw)
EOF

# 4. Unzip with the recovered password
unzip -P "Kryptos_Venon" -o cover.png -d out
cat out/flag.enc

# 5. Final decode chain: ROT5 (undoes ROT21) -> base64 decode -> hex decode -> XOR K2
python3 << 'EOF'
import base64
enc = open("out/flag.enc").read().strip()

def rot(s, n):
    return "".join(chr((ord(c)-65+n)%26+65) if c.isupper() else
                    chr((ord(c)-97+n)%26+97) if c.islower() else c for c in s)

step1 = rot(enc, 5)
step2 = base64.b64decode(step1)
raw = bytes.fromhex(step2.decode())

K2 = bytes.fromhex("ee4651a612cc87e9")
flag = bytes(b ^ K2[i % len(K2)] for i, b in enumerate(raw)).decode()
print("FLAG:", flag)
EOF
```
