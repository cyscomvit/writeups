---
layout: writeup

title: Echo in Black & White
difficulty: Medium
points: 500
categories: [Forensics]
tags: []

flag: CYS{7H3_H1DD3N_L4Y3R}
---

# Echo in Black & White

## Challenge Information
- **Title**: Echo in Black & White
- **Category**: Forensics
- **Difficulty**: Easy–Medium

## Challenge Description
What if complexity is just an illusion? Sometimes, the most ordinary patterns hold extraordinary secrets — if you learn to see them differently.
The challenge is about observing the given image carefully — it may look random, but it hides a binary pattern where black represents 1 and white represents 0.
Instead of overcomplicating it, try to read the pattern as bits, group them properly, and see what message it reveals.
Sometimes, the simplest patterns lead you straight to the flag.

## Hint
the grid is 16*10 bits 
## Solution

### Initial Analysis
The challenge image looked like a small QR-like binary grid.  
Since the description mentioned interpreting colors as binary bits, the first idea was to treat each black pixel as **1** and each white pixel as **0**, then group them to extract ASCII text.

### Tools Used
- **Python**
- **Pillow (PIL)** – for reading and resizing the image
- **NumPy** – for pixel manipulation

### Step-by-Step Solution

#### Step 1: Load and Convert the Image
```python
from PIL import Image
import numpy as np

img = Image.open("download.png").convert("L")
binary_img = (np.array(img) < 128).astype(np.uint8)  # Black = 1, White = 0
```
This converts the image to grayscale, then thresholds it so that each pixel is either 1 or 0.

#### Step 2: Resize to Match the Hint Dimensions
```python
resized = np.array(Image.fromarray(binary_img * 255).resize((16, 10), Image.NEAREST))
resized = (resized > 128).astype(np.uint8)
```
According to the challenge hint, the grid has **16 columns** and **10 rows**, so we resize it to that exact shape.

#### Step 3: Extract Binary and Convert to ASCII
```python
ascii_text = ""
for row in resized:
    bits = "".join(map(str, row))
    byte1, byte2 = bits[:8], bits[8:]
    ascii_text += chr(int(byte1, 2)) + chr(int(byte2, 2))

print(ascii_text)
```
Each row gives **16 bits** (2 ASCII characters of 8 bits each).  
After converting the binary values to text, the decoded message appears as:

```
CYS{7H3_H1DD3N_L4Y3R}
```

### Flag
```
CYS{7H3_H1DD3N_L4Y3R}
```

## Lessons Learned
- Binary-encoded patterns in images can directly store ASCII text.
- Always check for pixel-level hints in Forensics challenges.
- Knowing how to manipulate images programmatically is very useful in CTFs.

## Resources
- [Binary to ASCII Conversion Reference](https://www.rapidtables.com/convert/number/binary-to-ascii.html)
