---
layout: writeup

title: XORception
difficulty: Easy
points: 10
categories: [Cryptography]
tags: []

flag: CTF{x0r_iS_fUn}
---

### XORception

* Author: Guhan (DaBot)

This is a cryptography-based CTF using a repeating-key XOR cipher.

The provided ciphertext is:

```text
3b3b340317420a301b2b30142d010f
```

The challenge uses the repeating key:

```text
xor
```

Since XOR is its own inverse, we can decrypt the ciphertext by applying the same key again.

Using CyberChef, first apply **From Hex**, followed by **XOR** with:

```text
Key: xor
Key type: UTF-8
Scheme: Standard
```

The repeating key is applied across the ciphertext:

```text
xor xor xor xor xor
```

This produces the original plaintext:

```text
CTF{x0r_iS_fUn}
```

