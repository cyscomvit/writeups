---
layout: writeup

title: The Archive Behind the Chunk
difficulty: Easy
points: 10
categories: [Steganography]
tags: []

flag: CYS{W4k4nd443v3R}
---

### The Archive Behind the Chunk

* Author: Utkarsh

This is a steganography challenge involving image metadata, an encrypted payload, and a custom PNG chunk.

We are given:

```text
CTF1.png
CTF2.png
```

First, inspect `CTF1.png` using `exiftool`:

```text
exiftool CTF1.png
```

The metadata contains a Base64-encoded payload and the hint:

```text
key - thor
```

Decode the payload and decrypt it using `age`:

```text
base64 -d encoded.txt > secret.age
age -d -p secret.age
```

Using the password `thor` reveals a link to a Word document.

The document contains several images. Inspecting their metadata reveals the **first half** of the flag in one image's Description field.

Next, inspect `CTF2.png`. Running:

```text
pngcheck -v CTF2.png
```

reveals an unusual custom PNG chunk. The hidden data can also be located using:

```text
strings CTF2.png | grep drive.google.com
```

This reveals a Google Drive folder containing a video. The video provides the **second half** of the flag.

Combining both fragments gives:

```text
CYS{W4k4nd443v3R}
```

### The flag would be:

## CYS{W4k4nd443v3R}

