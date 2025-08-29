---
layout: writeup

title: Where's The Flag?
difficulty: hard
points: 400
categories: [steganography]
tags: []

flag: CBCV{1t5_n01_4_5p4c3_bUt_4_mY573Ry_009315}
---

### Where's The Flag?

* Author: Aakansh Gupta (Unknown)


```bash
┌──(kali㉿kali)-[~/Desktop/Cyscom]
└─$ stegseek esquie.jpg /usr/share/wordlists/rockyou.txt  
StegSeek 0.6 - https://github.com/RickdeJager/StegSeek

[i] Found passphrase: "1313"
[i] Original filename: "encoded_url.txt".
[i] Extracting to "esquie.jpg.out".
```

Using StegSeek, we discover a hidden file (`encoded_url.txt`) embedded in `esquie.jpg` using the password `1313`.

Inside the flag.txt -> `https://www.youtube.com/watch?v=-qgOZDRDynw?data=‌​‌‌‌‌​​‌​‌‌‌‌​‌‌​‌‌‌‌​​‌​‌​‌​​‌‌​​​​‌​​‌‌​​‌‌‌​‌​​​‌​‌‌‌‌​​‌​‌​‌​‌​​​​​‌​​‌​​​‌‌‌​​‌‌‌‌‌‌​​‌‌‌​‌​‌​​​​​‌‌​​‌​‌‌‌​‌​​​​​‌‌​​‌​‌​‌​​​‌‌‌‌‌‌​​‌​‌‌‌​​‌‌‌​​‌‌​​‌‌​​‌​‌​​​​​‌​​‌‌‌​‌‌​‌​‌​‌​‌​​​‌​‌‌‌​‌​​​​​‌‌​​‌​‌‌‌​‌​​​​​‌​​‌​​‌​‌​‌​​‌‌​‌‌​​‌​‌​‌‌​​‌​​​‌‌​​‌‌​​‌​‌​‌‌​‌‌​​​​‌‌​‌​‌​​​​​‌‌​​‌‌‌‌‌‌​​‌‌‌‌‌‌​​​‌‌​‌‌​​‌‌​​‌‌​​‌‌‌​‌‌​​‌​‌​‌​​​​​‌​‌‌‌‌​‌​‌‌‌‌​‌‌​‌‌‌‌​‌‌​‌‌‌‌​‌​​​​​‌​‌‌‌‌​‌​‌`, where there are zero-width charactersm, identified as blank spaces.

Using tools like [CyberChef](https://gchq.github.io/CyberChef/) we can see that there are hidden charecters.It turns out zero-width characters like `U+200C` and `U+200B` were used to encode binary data. Using online tools like [this](https://330k.github.io/misc_tools/unicode_steganography.html), we can analyze the extracted content.

<img src="../images/cyberchef.png" />

Once decoded, we download the revealed hidden file.

<img src="../images/decode.png" />

We inspect the contents using `xxd` to view the raw hex data:

<img src="../images/outxxd.png" />

The content looks XOR-encoded, so we decode it using the key 0xFF:

```python
hex_data = bytes.fromhex(
    "b1b7b1bc8485cc8dcfd288ce9bab97a0"
    "ca8fcb9cccd2d2c1cea085cc8dcfd2a8"
    "ce9bb7a091cf91d295cfceb1cc8dd2d2"
    "c1cfa09ccfcf93dededededede82f5"
)
decoded = bytes(b ^ 0xFF for b in hex_data)
print(decoded.decode('ascii'))
```

### The flag found is:
## CBCV{1t5_n01_4_5p4c3_bUt_4_mY573Ry_009315}
