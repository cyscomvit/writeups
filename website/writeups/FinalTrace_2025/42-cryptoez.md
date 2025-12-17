---
layout: writeup

title: CryptoEZ
difficulty: Medium
points: 500
categories: [General]
tags: []

flag: CYS{y0u_kn0w_cryp70}
---

# CryptoEZ

**Category**: Cryptography  
**Author**: Abhay Krishna

---

*This challenge explores the basics of image cryptography with basic concepts like `EXIF metadata` and `steganography`*

---

## Initial Analysis

As the description suggests there is something hidden inside the message it is very common and basic to view the metadata of the Image.

---

## Tools Used

- Online EXIF data viewer
- Zsteg

---

## Step-by-Step Solution

### Step 1: Check EXIF Metadata
On viewing the metadata of the image we can see a hint saying *"Listen to the least significant whispers"*. This indicates the use of **LSB steganography** - a technique for hiding secret data by replacing the least significant bits (LSBs) of a carrier file, like an image, with the bits of the hidden message.

### Step 2: Use Steganography Tools
To solve this we can use tools like `zsteg` which is used for detecting and extracting steganographic data from images.

### Step 3: Extract Hidden Data
On running the command:
```shell
zsteg flag.png

b1,r,lsb,xy         .. text: "<~^#vS\\p"
b1,g,msb,xy         .. file: OpenPGP Secret Key
b1,rgb,lsb,xy       .. text: "CYS{y0u_kn0w_cryp70}"
b4,r,lsb,xy         .. text: "vU\"#4\"$DDDD3#C2 "
b4,g,lsb,xy         .. text: "##DEEVfeef"
b4,b,lsb,xy         .. text: "\"3EUUUEEEEfw"
b4,rgb,lsb,xy       .. text: "`U'rw'rw'qf"
b4,bgr,lsb,xy       .. text: "Pw'rw'rw&af"

---
## Flag:

- CYS{y0u_kn0w_cryp70}

---
