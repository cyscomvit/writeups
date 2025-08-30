---
layout: writeup

title: Intellectual Conversation
level:
difficulty: easy
points: 200
categories: [Misc]
tags: []

flag: CBCV{1nv151b1l1ty_0r_t1m3_c0ntr0l?}
---

### Intellectual Conversation

* Author: Aadhyanth

Encoding:
convert each character to ascii and insert \u200b after that many characters

Decoding:
find distance between 2 zero-width characters and convert take chr()

python code:

```
def hide_flag_in_text(text, flag):
    zwsp = "\u200b"
    result = ""

    flag_index = 0
    char_count = 0

    for ch in text:
        result += ch
        char_count += 1

        # check if we've reached the ascii value position for current flag character
        if flag_index < len(flag) and char_count == ord(flag[flag_index]):
            result += zwsp
            flag_index += 1
            char_count = 0  # reset counter

    return result

def decode_flag_from_text(encoded_text):
    char_count = 0
    flag = ""

    for ch in encoded_text:
        if ch == '\u200b':
            flag += chr(char_count)
            char_count = 0
        else:
            char_count += 1

    return flag

# Usage
huge_text = """TRANSCRIPT-1

Discussion between Dr. Sarah Chen (Theoretical Physicist) and Prof. Marcus Rodriguez (Materials Science)
...
...
Prof. Rodriguez: Thank you, Sarah. I look forward to continuing this conversation as the field evolves.

[End of Transcript]
"""
flag = "CBCV{1nv151b1l1ty_0r_t1m3_c0ntr0l?}"
encoded_text = hide_flag_in_text(huge_text, flag)

print("Encoded text:")
print(encoded_text)

with open('transcript.txt', 'w', encoding='utf-8') as file:
    file.write(encoded_text)
    file.close()


with open('transcript.txt', 'r', encoding = 'utf-8') as file:
    data = file.read()
    print("\nDecoded flag:")
    print(decode_flag_from_text(data))

```

Output:
Encoded text:
Squeezed text (182 lines).

### The flag found is:
## CBCV{1nv151b1l1ty_0r_t1m3_c0ntr0l?}
