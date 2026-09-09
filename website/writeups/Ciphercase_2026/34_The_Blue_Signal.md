---
layout: writeup

title: The Blue Signal
difficulty: Easy
points: 200
categories: [OSINT]
tags: []

flag: CYS{11AM_35.1381_-106.5156_00BFFF}
---

The Blue Signal

Author: Akshitha M

This is a OSING based CTF challenge using instagram, github and Google docs.


<img width="1200" height="628" alt="@capncookmrwhite" src="https://github.com/user-attachments/assets/a71f0622-d063-4726-b496-f13e00f28852" />
In the right side we can see the user @capncookmrwhite
The picture is colored differently (purple and pink instead of the original blue) pointing to instagram's iconic colors.

Upon searching the username on instagram we land on a public page with one post
<img width="717" height="1600" alt="image" src="https://github.com/user-attachments/assets/bb80b978-3909-4d24-84f6-336975062c08" />
<img width="717" height="1600" alt="image" src="https://github.com/user-attachments/assets/8384f469-ab19-46bb-af09-0c0af803e00d" />

Few letters in the caption of the post are capitalized randomly spelling out GITHUB.

<img width="972" height="624" alt="image" src="https://github.com/user-attachments/assets/feb49a82-6846-4207-91dd-641375ea85c6" />

All are fake except last one

<img width="1021" height="531" alt="image" src="https://github.com/user-attachments/assets/dc0ff3f8-3215-4d21-94bc-8a15dca04058" />

download the last html and enter the password
<img width="362" height="97" alt="image" src="https://github.com/user-attachments/assets/fd57fbda-2a43-4c32-b1a9-195080398241" />

use base64 decoder
<img width="1356" height="568" alt="image" src="https://github.com/user-attachments/assets/26e72997-2d32-489c-b567-4b038eaabacd" />

A google docs will open, all visible text is useless

<img width="619" height="485" alt="image" src="https://github.com/user-attachments/assets/3f6d0e3f-5154-4616-9e21-534036fdc289" />
<img width="677" height="170" alt="image" src="https://github.com/user-attachments/assets/8710bfe5-e67d-40ea-b9ce-8003b786b63e" />

Hex of sky blue is 00BFFF

Epi number is 11 and it’s morning 11AM

"Where my world leaks into yours" refers to coordinates of shooting location which is John B. Robert Dam with decimal coordinates 35.1381 -106.5156

Use flag format to get answer


CYS{11AM_35.1381_-106.5156_00BFFF}
