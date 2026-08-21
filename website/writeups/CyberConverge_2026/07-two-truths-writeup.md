---
layout: writeup

title: Two Truths and a Steg
difficulty: Easy
points: 10
categories: [Steganography]
tags: []

flag: CYS{th3_d1ff_w4s_th3_p01nt}
---

### Two Truths and a Steg

* Author: Sagnik

This is a steganography challenge involving two seemingly identical images.

We are given:

```text
before.png
after.png
```

Although the images look identical, their SHA-256 hashes are different, indicating that the underlying files have been modified.

We can compare the images directly using ImageMagick:

```text id="4t7h7w"
magick compare before.png after.png -compose src diff.png
```

This generates `diff.png`, which highlights the differences between the two images.

Opening the difference image reveals the hidden message:

```text id="4k7g4c"
CYS{th3_d1ff_w4s_th3_p01nt}
```

