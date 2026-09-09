---
layout: writeup

title: Los Stegos Hermanos
difficulty: Medium
points: 300
categories: [Steganography]
tags: []

flag: CYS{W@1t3r_w0ul0_ch3ck_8he_8u@nt1$@t10n_t@813}
---

Los Stegos Hermanos

Author: Utkarsh Raj

## Description

A set of images and an audio file were provided. At first, most of them looked like normal media files, but each one contained a small clue pointing towards another file.

There were also a couple of decoy paths with fake flags, so blindly extracting everything was not enough.

The final flag was:

`CYS{W@1t3r_w0ul0_ch3ck_8he_8u@nt1$@t10n_t@813}`

## Initial Enumeration

Start by identifying the supplied files:

`file *`

This showed:

- `01.jpeg` — JPEG
- `02.png` — PNG
- `03.jpg` — JPEG
- `04.jpeg` — JPEG
- `05.png` — palette-based PNG
- `audio.wav` — WAV audio

`05.png` immediately stood out because it used an 8-bit colour palette.

## 1. Palette Manipulation — 05.png

Check the PNG:

`identify -verbose 05.png | grep -E "Type:|Colors:|Depth:"`

It showed:

`Type: Palette`  
`Depth: 8-bit`

Instead of only looking at the colours themselves, inspect consecutive palette entries and look for repeated runs.

A small Python script was used to compare neighbouring palette entries.

The interesting result was:

`17 33 17`

meaning palette entries `17` through `33` all contained the same RGB value.

There was another shorter repeated run at `240–242`, which acted as a distraction.

The unusual run length gives the first clue:

`17`

## 2. Histogram — 03.jpg

The value `17` was used as a ranking rather than as a pixel value.

Convert the image to grayscale and count the frequency of every grayscale value:

`python3 - <<'PY'
from PIL import Image
from collections import Counter

img = Image.open("03.jpg").convert("L")
h = Counter(img.getdata())

for rank, (value, count) in enumerate(
    sorted(h.items(), key=lambda x: x[1], reverse=True), 1
):
    if rank <= 25:
        print(rank, value, count)
PY`

The 17th most frequent value was:

`17 22 18330`

So the next clue was:

`22`

## 3. Image Dimensions — 02.png

The next image was `02.png`.

Check its dimensions:

`identify 02.png`

It was:

`1000 x 664`

Use the previous clue as the modulus:

`1000 % 22 = 10`  
`664 % 22 = 4`

This gives the coordinate:

`(10,4)`

## 4. Pixel as ASCII — 02.png

Read the RGB value at that coordinate:

`python3 - <<'PY'
from PIL import Image

img = Image.open("02.png").convert("RGB")
p = img.getpixel((10,4))

print("RGB:", p)
print("ASCII:", "".join(chr(x) for x in p))
PY`

The result was:

`RGB: (83, 84, 65)`

Those values correspond to ASCII:

`83 = S`  
`84 = T`  
`65 = A`

giving:

`STA`

This was the beginning of the next instruction, pointing towards the `START / QTABLE` stage.

## 5. JPEG Quantization Table — 04.jpeg

The next target was `04.jpeg`.

JPEG quantization tables can be inspected directly with Pillow:

`python3 - <<'PY'
from PIL import Image

img = Image.open("04.jpeg")

for table, values in img.quantization.items():
    print("TABLE", table)
    print("POSITION 29:", values[29])
PY`

The relevant table was table `0`.

At position `29`:

`QTABLE[29] = 37`

So the next clue was:

`37`

## 6. Audio / Spectrogram

There was also an audio file:

`audio.wav`

Playing it normally did not reveal a useful spoken message. The useful information was hidden in its spectrogram.

Opening the WAV in Audacity and switching the track to Spectrogram view revealed:

`HEY YO! NEW COMPETITION`

and:

`QTABLE 29`

This acted as a confirmation for the quantization-table stage rather than being a separate route to the flag.

## 7. Palette Index 37

Return to `05.png` and inspect palette index `37`.

The important observation is that the previous clue, `37`, is specifically a palette index.

The PNG also contained a custom ancillary chunk holding the final encrypted payload.

A small textual clue was included in the PNG:

`Palette37=CHUNK`

This tells the solver that the palette result should lead to inspection of the PNG chunks.

The custom chunk was named:

`cYSd`

It contained `46` encrypted bytes.

## 8. Recovering the Payload

The payload was XOR encrypted with the key:

`1722362937`

The encrypted bytes from the custom PNG chunk were XORed against this key repeatedly.

Conceptually:

`plaintext[i] = ciphertext[i] XOR key[i % len(key)]`

This produced the final flag.

## Decoy Paths

There were also deliberate false leads.

### 01.jpeg

`file 01.jpeg`

revealed a JPEG comment containing:

`CYS{m3t4d4t4_l13s}`

This was a fake flag.

It was useful as an early distraction, but it did not connect to the other clues.

### 03.jpg

`binwalk 03.jpg`

revealed an embedded ZIP archive.

Extracting it produced another fake flag:

`CYS{c0mpr3ss10n_1s_n0t_th3_4nsw3r}`

This was another dead end.

The presence of real embedded data made the decoy more convincing, but it did not contribute to the actual chain.

## Final Flag

After following the connected clues:

`05.png → 17`

`03.jpg histogram → 22`

`02.png dimensions → (10,4)`

`02.png pixel → STA`

`04.jpeg QTABLE[29] → 37`

`05.png palette 37 → custom PNG chunk`

`XOR key → 1722362937`

the final flag is:

`CYS{W@1t3r_w0ul0_ch3ck_8he_8u@nt1$@t10n_t@813}`
