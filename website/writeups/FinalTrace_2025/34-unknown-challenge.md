---
layout: writeup

title: Unknown Challenge
difficulty: Medium
points: 500
categories: [General]
tags: []

flag: CYS{early_belief}
---

CTF #28 – Paradox Parable (Variant II) Writeup
This is a Easy Forensics challenge based on data carving an appended archive from a PNG file.

The challenge includes a decoy flag and a misleading handbook:

Decoy Flag: Running strings Paradox_Parable_Image.png reveals the false flag: CYS{early_belief}.
The player must use binwalk to scan the file's binary structure for embedded signatures


Command:
binwalk -e Paradox_Parable_Image.png
will give a extracted file with the true flag : CYS\{binwalk\_reveals\_truth\}
