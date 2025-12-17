---
layout: writeup

title: Alpha Parallel
difficulty: Easy
points: 500
categories: [Forensics / Cryptography]
tags: []

flag: CYS{SHADOW_ALPHA_QR_LAYER_42X}
---

# Alpha Parallel

## Challenge Information

| Field | Details |
|--------|----------|
| **Title** | Alpha Parallel |
| **Category** | Forensics / Cryptography |
| **Difficulty** | Easy |
| **Points** | 150 |


---

## Challenge Description

The provided PNG image contained **two QR codes** — one clearly visible, and another **hidden within the alpha channel** (transparency layer).  

When extracted, the **visible QR** directed players to a YouTube video, while the **hidden QR** led to a Pastebin URL containing a **Spiral Cipher** challenge.  

The player’s goal was to uncover the hidden data layer, decode the spiral cipher, and retrieve the final flag.

---

## Step 1: Inspecting the PNG Layers

Opening the image in a standard viewer only showed one QR code.  
However, using a forensic image inspection tool like **GIMP**, **StegSolve**, or **Python (Pillow)** revealed that the **alpha channel** contained distinct pixel patterns — forming a second QR code.

### Extract Alpha Channel Using Python

```python
from PIL import Image

# Load image
img = Image.open("dual_qr.png")

# Split image into channels (RGBA)
r, g, b, a = img.split()

# Save the alpha channel separately
a.save("hidden_qr.png")
print("Hidden QR extracted as hidden_qr.png")
```

This script isolates the transparency layer (`alpha`) and saves it as a new image — **hidden_qr.png** — which can then be scanned.

---

## Step 2: Scanning Both QR Codes

After extraction:

- **Visible QR:** Scanned to `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
- **Hidden QR:** Scanned to a **Pastebin URL**  
  `https://pastebin.com/ZmkMxUdY`

The Pastebin text displayed a **5×5 grid**, which was actually a **Spiral Cipher**.

---

## Step 3: Understanding the Spiral Cipher

Pastebin content:

```
X P H A _
2 L H A Q
4 A S D R
_ _ W O _
R E Y A L
```

The challenge description hinted:  
> “Outward, start by up, clockwise.”

This means we must read the characters **from the center outward**, following a **clockwise spiral** starting **upward**.

---

## Step 4: Solving the Spiral Cipher in Python

To automate decoding, we can write a small script:

```python
def spiral_read(matrix):
    n = len(matrix)
    x, y = n // 2, n // 2  # start from center
    dx, dy = 0, -1  # start moving up
    result = []

    steps = 1
    while len(result) < n * n:
        for _ in range(2):  # two directions before increasing step size
            for _ in range(steps):
                if 0 <= x < n and 0 <= y < n and matrix[y][x] != '_':
                    result.append(matrix[y][x])
                x, y = x + dx, y + dy
            dx, dy = dy, -dx  # rotate 90° clockwise
        steps += 1
    return ''.join(result)

grid = [
    ['X','P','H','A','_'],
    ['2','L','H','A','Q'],
    ['4','A','S','D','R'],
    ['_','_','W','O','_'],
    ['R','E','Y','A','L']
]

flag = spiral_read(grid)
print("Decoded Spiral:", flag)
```

**Output:**
```
Decoded Spiral: CYS{SHADOW_ALPHA_QR_LAYER_42X}
```

---

## Final Flag

```
CYS{SHADOW_ALPHA_QR_LAYER_42X}
```
