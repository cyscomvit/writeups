---
layout: writeup

title: Level 9 - f0x3rr
difficulty: medium
points: 40
categories: [web, osint]
tags: []

flag: zyp{language_en}
---

## Challenge

You are given a [website](https://f0x3rr.onrender.com/)

## Solution

In the website, f0x3rr is a endpoint

![](writeupfiles/level9/1.png){:width="70%"}

Click Download and a file will be downloaded

![](writeupfiles/level9/2.png){:width="70%"}

Convert this decimal to string using online converter and you'll get a github and in the issue section there will be a password hidden in the conversation

Password is `zero-day`

![](writeupfiles/level9/3.png){:width="80%"}

![](writeupfiles/level9/4.png){:width="80%"}

When you visit the endpoint, click the download button and you'll Zypher event poster

![](writeupfiles/level9/5.png){:width="60%"}

![](writeupfiles/level9/6.png){:width="60%"}

![](writeupfiles/level9/7.png){:width="50%"}

Scan the QR code and you'll get a `base64` encoded string, decode it and you'll get a link an endpoint `/vitcyscomzypher`

![](writeupfiles/level9/8.png){:width="80%"}

Go to the endpoint and download the file

![](writeupfiles/level9/9.png){:width="80%"}

![](writeupfiles/level9/10.png){:width="80%"}

Convert the binary to string

![](writeupfiles/level9/11.png){:width="60%"}

Decoding the Caesar cipher

![](writeupfiles/level9/12.png){:width="70%"}
