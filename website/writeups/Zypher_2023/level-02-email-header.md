---
layout: writeup

title: Level 2 - Email Header
difficulty: easy
points: 10
categories: [cryptography, forensics]
tags: []

flag: zyp{Welcometozyphequest_0012}
---

## Challenge

You have given a [Message.eml](writeupfiles/level2/Message.eml)

### Hints

1. Check for authenticity of the email

2. Analyse DKIM-SIGNATURE in the email header

3. Decrypt the cipher using ROT13

## Solution

Download the given .eml file

Check for the DKIM-SIGNATURE (A DKIM signature in an email header is a cryptographic
stamp that verifies the authenticity of the email. Usually it uses `rsa256` for encryption but here we used `ROT13` weak cipher text for encryption)

```eml
DKIM-Signature: v=3D1; a=3Drot13; c=3Dsimple/simple;
  d=3Dtech=2Ecom; i=3D@tech=2Ecom; q=3Ddns/txt; s=3Dmain;
  t=3D169784749; x=3D17293849;
  h=3Dmime-version:from:to:subject:message-id:date;
  p=3Dmlc{Jrypbzrgbmlcurdhrfg_0012}
```

Decrypt the cipher using ROT13 to get the flag
