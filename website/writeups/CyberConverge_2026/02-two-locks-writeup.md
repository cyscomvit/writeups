---
layout: writeup

title: Two Locks, One Message
difficulty: Easy
points: 10
categories: [Cryptography]
tags: []

flag: CYS{c4es4r_x0r_2x}

---

### Two Locks, One Message

* Author: Sagnik

This is a cryptography-based CTF using two layers of encryption: a Caesar cipher and XOR.

From `clue.txt`, we determine the Caesar shift is `3` and the XOR key is `42` (`0x2A`).

A simple google search gives you the second lock key. :D

Since the message was encrypted twice, we reverse the operations during decryption.

The encrypted data is:

```text
6c687c514c1e425c1e5f754b1a5f75184b57
```

First, undo the XOR layer using key `2A`:

```text
FBV{f4hv4u_a0u_2a}
```

Then undo the Caesar shift by shifting the letters back by `3`:

```text
CYS{c4es4r_x0r_2x}
```

