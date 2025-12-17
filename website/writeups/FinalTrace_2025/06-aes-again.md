---
layout: writeup

title: AES again??
difficulty: Medium
points: 500
categories: [General]
tags: []

flag: CYS{tiny_change_huge_difference}
---

# AES again??

 * Category: Cryptography
 * Author: P C Guhan

## Description

> ECB mode this time...
> Random function, PKCS 7 padding - should be good
> Or is it??
>(Encode the flag as CYS{flag} separated by underscores)

## Source
```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import random

random_int = random.getrandbits(128)
key = random_int.to_bytes(16, byteorder='big')
cipher = AES.new(key, AES.MODE_ECB)

def encrypt(str):
    padded = pad(str.encode(), 16)
    encrypted = cipher.encrypt(padded)
    return encrypted

with open("flag.txt", "r") as f:
    plaintext = f.read()
encrypted_blocks = [encrypt(c).hex() for c in plaintext]
with open("output.txt", "w") as f:
    f.write(" ".join(encrypted_blocks))
```
[output.txt](output.txt)

## Solution
![ECB Mode](image.png)

AES ECB mode uses the same key to encrypt different blocks.

The vulnerability in this code is that we take a single character from the flag, pad it and encrypt it as opposed to padding the entire flag and encrypting it.
Therefore all instances of the same character have the same cipher i.e. all 'a's will have the same cipher.

This in turn can be broken through frequency analysis

Frequency analysis also becomes easier when a large amount of text is given

## Solution script
```python
import string

def read_encrypted(filename):
    with open(filename, "r") as f:
        content = f.read()
    return content.strip().split()

def map_blocks_to_letters(encrypted_blocks):
    unique_blocks = sorted(set(encrypted_blocks))
    if len(unique_blocks) > 26:
        raise ValueError(f"Too many unique blocks: {len(unique_blocks)} (max 26 allowed)")
    letters = list(string.ascii_lowercase)
    mapping = {block: letter for block, letter in zip(unique_blocks, letters)}
    return mapping

def substitute_blocks_with_letters(encrypted_blocks, mapping):
    return "".join(mapping.get(block, "?") for block in encrypted_blocks)

def main():
    encrypted_file = "output.txt"
    decoded_file = "test.txt"

    encrypted_blocks = read_encrypted(encrypted_file)
    mapping = map_blocks_to_letters(encrypted_blocks)
    decoded_text = substitute_blocks_with_letters(encrypted_blocks, mapping)

    with open(decoded_file, "w") as f:
        f.write(decoded_text)

if __name__ == "__main__":
    main()
```
[test.txt](test.txt)
This script substitutes each unique hex value with a letter. There are only 26 unique hex values in output.txt

When doing frequency analysis and substitution on the contents of test.txt, we get the plaintext.

Frequency analysis tools are available online.
[The tool I used](https://www.dcode.fr/frequency-analysis)

>Flag: CYS{tiny_change_huge_difference}