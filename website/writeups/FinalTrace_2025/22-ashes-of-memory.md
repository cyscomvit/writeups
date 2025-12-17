---
layout: writeup

title: Ashes of Memory
difficulty: Medium
points: 500
categories: [Forensics]
tags: []

flag: CYS{7h3RE_15_N0_E4D}
---

# Ashes of Memory

- **Category**: [Forensics]
- **Author**: [ace6002]
- **Level**: [Easy]

## Challenge Description
Image stegseek reveals binary, decoding binary gives flag.

## Solution

### Tools Used
- [Stegseek]
- [Python to group binary by 7 bits and decode]

### Step-by-Step Solution

#### Step 1: StegSeek on given JPG
```
stegseek image.jpg -wl rockyou.txt
```
[Reveals hidden fl.txt containing flag. Passphrase for stegseek is 'cyberpunk'.]

#### Step 2: Use python code to group binary bits by 7 and convert to ASCII.
```python
binary_input = input("Enter 7-bit binary (no spaces): ")
text = ''.join(chr(int(binary_input[i:i+7], 2)) for i in range(0, len(binary_input), 7))
print(text)
```
[Converts binary into required flag.]

### Flag
```
CYS{7h3RE_15_N0_E4D}
```
