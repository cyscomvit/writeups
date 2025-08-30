---
layout: writeup

title: Look beyond what you see 
level:
difficulty: medium
points: 300
categories: [misc]
tags: []

flag: CBCV{MORSE_OR_REMORSE}
---

## Look beyond what you see 

* Created by: P C Guhan (DaBot)

## Description

> Look beyond what you see 
> (Change the brackets in the flag to {} when submitting)

[output.txt](output.txt)


## Solution

Upon opening the txt file in a standard hex editor, we find that the file consists of only 3 characters - \x00 (null), \x20 (space) and \xe2\x80\x8b (Zero Width Space). 
Here we substitute \x00 as a space, \x20 as '.' and \xe2\x80\x8b as '- and get the morse code encoded text. We then decode it to get the flag.

Script:

```python
import re

def substitute_morse_escaped(filename, output_filename):
    with open(filename, "r", encoding="utf-8") as f:
        raw_text = f.read()

    decoded_bytes = raw_text.encode("utf-8").decode("unicode_escape").encode("latin1")

    decoded_bytes = decoded_bytes.replace(b"\xe2\x80\x8b", b"-")
    decoded_bytes = decoded_bytes.replace(b"\x20", b".")

    decoded_bytes = re.sub(b'\x00{3,}', b'   ', decoded_bytes)

    decoded_bytes = re.sub(b'\x00', b' ', decoded_bytes)

    morse_code = decoded_bytes.decode("utf-8")

    with open(output_filename, "w", encoding="utf-8") as out:
        out.write(morse_code)

if __name__ == "__main__":
    substitute_morse_escaped(
        "hexa.txt",
        "morse_output.txt"
    )
```

[morse_output.txt](morse_output.txt)


### Final flag reterived:
## CBCV{MORSE_OR_REMORSE}
