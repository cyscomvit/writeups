---
layout: writeup

title: Level 6 - Der Anfang
difficulty: easy
points: 30
categories: [osint, steganography]
tags: []

flag: zyp{VG3wf$xxRM1mCq$CMyBJjO0zflAV$q}
---

## Challenge

An image file is given. [Der Anfang](writeupfiles/level6/der_Anfang.jpg)

## Solution

The link to the social media post is given in the meta data of the image file in the id name of UserComment and the meta data can be viewed using exiftool.

```bash
$ exiftool der_Anfang.jpg
```

![exiftool](writeupfiles/level6/exiftool.png){:width="70%"}

In the reddit post the link to the git history is salted and placed

![reddit](writeupfiles/level6/reddit.png){:width="70%"}

Link after removing unwanted special characters 👇🏻

[https://github.com/yshui/picom/commit/a2bcf94ce8fa7216f69fb6ace2c1b3776bdce823](https://github.com/yshui/picom/commit/a2bcf94ce8fa7216f69fb6ace2c1b3776bdce823)

The flag is in the commit message.

![flag](writeupfiles/level6/flag.png){:width="70%"}
