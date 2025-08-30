---
layout: writeup

title: Passz CheckS
level:
difficulty: hard
points: 500
categories: [Reverse Engineering]
tags: []

flag: CBCV{CiCaDAzznotz141}

---
# Passz CheckS

## Challenge Description

You are given a password checker program which is encrypted through an algorithm, decipher,decomipiler and decode the file to find the password

Inspect binary file and Locate custom alphabet and encoded flag
`strings password_checker | grep -E "(Correct!|Wrong!|Usage:|[A-Za-z0-9+/]{10,})" `

Locate XOR key (12 bytes)
`xxd password_checker | grep -A2 -B2 "0a0b 0c0d`

Locate expected-hash bytes (0x7a repeated)
`grep -a -b -o "zzzz" password_checker xxd password_checker | sed -n '94,96p' `

Compute password from key and target byte 0x7a

```python
python3 - <<'PY' xor_key = [0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x14,
0x15] expected = 0x7A password = ''.join(chr(expected ^ b) for b in xor_key) print(password) PY
```

Retrieve flag
`./password_checker "pqvwtujkhino" `

### Final flag is:
## CBCV{CiCaDAzznotz141}