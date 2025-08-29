---
layout: writeup

title: Monoalphabetic Shenanigans
difficulty: hard
points: 450
categories: [cryptography]
tags: []

flag: CBCV{FREQUENCY_ANALYSIS_FTW}
---

# Monoalphabetic Shenanigans

* Author: P C Guhan (DaBot)
    
## Description

> Looks Secure? Check again
> Add the CBCV{flag} and underscores while submitting the flag (ALL CAPS)

`script_redacted.py`: 

```python
def __(_0, _1, _2, _3):
    ___ = list(map(ord, _3))
    ____ = (_0 << 0) ^ (_1 >> 0) ^ (_1 - _1)
    _____ = (_1 ^ 0) * (_2 ^ 0)
    return [__import__("builtins").pow(x, ____ or _0, _____) for x in ___]


with open("plaintext.txt", "r") as f:
    T = f.read().strip()

p = REDACTED
q = REDACTED

e = 65537

output = __(e, p, q, T)

with open("output.txt", "w") as f:
    f.write(str(output))
```

[output.txt](output.txt)

## Solution

Here, RSA is implemented by converting each letter to its ASCII value and then encrypting it. Hence each letter will have the same encrypted value. Since there are only 26 unique encoded numbers, we can map each cipertext to a letter. Once mapped, the cipertext needs to be replaced with the letter and then a frequency analysis can be run.

A frequency analysis refers to the guessing of the correct cipertext based on the number of occurences of a letter in the text. This can be done using online tools.

Script:

```python
import re
import string

def read_encrypted(filename):
    with open(filename, "r") as f:
        content = f.read()
    return list(map(int, re.findall(r"\d+", content)))

def map_numbers_to_letters(encrypted_numbers):
    unique_numbers = sorted(set(encrypted_numbers))
    if len(unique_numbers) > 26:
        raise ValueError(f"Too many unique numbers: {len(unique_numbers)} (max 26 allowed)")
    letters = list(string.ascii_lowercase)
    mapping = {num: letter for num, letter in zip(unique_numbers, letters)}
    return mapping

def substitute_numbers_with_letters(encrypted_numbers, mapping):
    return "".join(mapping.get(num, "?") for num in encrypted_numbers)

def main():
    encrypted_file = "output.txt"
    decoded_file = "test.txt"

    encrypted_numbers = read_encrypted(encrypted_file)

    mapping = map_numbers_to_letters(encrypted_numbers)

    decoded_text = substitute_numbers_with_letters(encrypted_numbers, mapping)

    with open(decoded_file, "w") as f:
        f.write(decoded_text)

if __name__ == "__main__":
    main()
```

Output:
[test.txt](test.txt)

The we need to do frequency analysis on the output file i.e. test.txt.
Upon doing frequency analysis using online resources. We get the frequency of each letter and the approximate substitution which will give us the desired result.
![frequency](./images/lkby.png)

This webiste: https://www.dcode.fr/frequency-analysis provides the ability to directly substitute the required letters and the gives the flag as FLAGFREQUENCYANALYSISFTW.

### Final flag reterived:
## CBCV{FREQUENCY_ANALYSIS_FTW}
