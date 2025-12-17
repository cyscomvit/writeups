---
layout: writeup

title: Challenge Name
difficulty: Medium
points: 500
categories: [Web]
tags: []

flag: CYS{B43aking_th3_m1rr0r_1$_c00l}
---

## Challenge Name

- **Category**: Web
- **Author**: Kirubahari

## Challenge Description
The Challenge is about web enumeration and find the hidden endpoints and parameters to get the flag

## Solution

### Initial Analysis
What I did first - enumeration, bruteforcing for endpoints

### Tools Used
- ffuf
- base64
- python

### Step-by-Step Solution

#### Step 1: Finding the endpoint
```
ffuf -u "http://$IP:$PORT/FUZZ" -w WORDLIST --ic
```
It gives the hidden endpoint

#### Step 2: Fidning the parameter
```
ffuf -u "http://$IP:$PORT/mirror?FUZZ=true" -w WORDLIST --ic -fs int(x)
```
Which gievs the hiddenendpoint which downlaods the zip file which has the encoded flag

#### Step 3: Decoing
```
cat flag.txt | base64 -d
```
which gives the decoded dna encoded text decoding gives the flag

#### Script

```python
import sys

MAP = {
    'A': '00',
    'C': '01',
    'G': '10',
    'T': '11'
}

def dna_to_bytes(dna: str) -> bytes:
    dna = ''.join(dna.split())
    if len(dna) % 4 != 0:
        raise ValueError("DNA length not multiple of 4 (each byte = 4 nucleotides).")
    bits = ''.join(MAP[nuc] for nuc in dna)
    out = bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
    return out

def main():
    if len(sys.argv) == 2 and sys.argv[1] != '-':
        s = open(sys.argv[1], 'r').read()
    else:
        s = sys.stdin.read()
    try:
        b = dna_to_bytes(s)
        print(b.decode('utf-8'))
    except Exception as e:
        print("Decoding failed:", e, file=sys.stderr)
        try:
            b = dna_to_bytes(s.strip())
            import binascii
            print("HEX:", binascii.hexlify(b).decode())
        except:
            pass
        sys.exit(1)

if __name__ == '__main__':
    main()
```

### Flag
```
CYS{B43aking_th3_m1rr0r_1$_c00l}
```
