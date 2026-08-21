---
layout: writeup

title: The King's Last Recipe
difficulty: Easy
points: 10
categories: [Cryptography]
tags: []

flag: CYS{B3LL4_C1A0}
---

### The King's Last Recipe

* Author: Utkarsh

This is a cryptography-based CTF involving multiple encoding layers and hidden clues.

The original Google Doc contains hidden white-on-white text. Selecting the page contents reveals:

```text
K;v>Sk,6xIrfXt3EJw<nlld)t7h9S2RuIR'Diqb/ysC3?NaZ=1h\sT6:su[llzdxGh1!cyWbK'j9XK6sHkkppx57KzH6({(Z@=vkhV4/yak!kv41Hm_LQ'$<ZT)(9E
```

This string is encoded using **Base92 followed by ROT13**. Reversing these operations gives a link to a second Google Doc.

The second document contains the encrypted key.

The story in the first document provides the encoding layers in order:

```text
64 → 64 → 8 → 32 → 45 → 58 → 62 → 64 → 92
```

Therefore, the layers must be decoded in reverse order:

```text
Base92 → Base64 → Base62 → Base58 → Base45 → Base32 → Octal → Base64 → Base64
```

Using CyberChef with the corresponding `From Base` operations reveals:

```text
B3LL4_C1A0
```
