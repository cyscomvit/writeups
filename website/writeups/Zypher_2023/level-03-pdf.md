---
layout: writeup

title: Level 3 - Password Protected PDF
difficulty: easy
points: 10
categories: [general]
tags: []

flag: zyp{string_1408}
---

## Challenge

You are given a [PDF](writeupfiles/level3/unknown.pdf)

## Solution

You need to first extract the crackable information from the file using `John the Ripper` tool.

```bash
$ pdf2john.py unknown.pdf > hash
```

![](writeupfiles/level3/1.png)

Now, crack the hash using `John the Ripper` tool.

```bash
$ john hash --wordlist=/usr/share/wordlists/rockyou.txt hash
```

![](writeupfiles/level3/2.png){: width="70%"}

Now, you can see the password for the PDF file is `mystery`. Use this password to open the PDF file and you will get the flag.

![](writeupfiles/level3/3.png){: width="70%"}
