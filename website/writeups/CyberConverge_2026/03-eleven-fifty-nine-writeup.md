---
layout: writeup

title: The 11:59 PM Special
difficulty: Easy
points: 10
categories: [Steganography/File Forensics]
tags: []

## flag: CYS{s00n_m4y_th3_w3_p4ss_c0m3}

### The 11:59 PM Special

* Author: Aditi Sahu

This is a steganography and file forensics challenge. The provided PNG appears to be corrupted, so we inspect the file contents instead of relying only on the image.

Using the `strings` command, we can search for readable text inside the binary file:

```text
strings challenge.png | grep CYS
```

This reveals the hidden flag appended at the end of the PNG file:

```text
CYS{s00n_m4y_th3_w3_p4ss_c0m3}
```

