---
layout: writeup

title: The Hacker Left a Note
difficulty: Easy-Medium
points: 10
categories: [Web Recon, Basic Web Security]
tags: []

flag: FLAG{debugging_is_recon}
---

### The Hacker Left a Note

* Author: Shruthi

This is a web reconnaissance challenge where the flag is hidden through a chain of developer artifacts.

First, visit the homepage

Viewing the page source reveals a hidden comment:

```html
<!-- TODO: remove debug endpoint before deployment -->
```

Following the clue, visit: /debug endpoint

The debug console contains a note mentioning that the backup log was saved as `backup.txt` in the static assets folder.

We then visit: /static/backup.txt

The log contains a temporary access code:

```text
Temporary access code: 4832
```

The surrounding log indicates that the code is intended for the `/profile` endpoint.

Finally enter the code and the page reveals the flag.

