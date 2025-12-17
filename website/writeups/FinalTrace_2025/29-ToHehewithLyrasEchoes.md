---
layout: writeup

title: To Hehe with Lyra's Echoes
difficulty: Medium
points: 500
categories: [General]
tags: []

flag: CYS{HERACTUALECHOES}
---


# Basically you're treated with the link.
https://echositee.vercel.app/

If you open the site, it'll lead you to the login page where you'll be asked for a username and the password. But don't you worry because if you open

Inspect -> JavaScript segment of the code

You'll see username = lyra
Password = Base16 version of $#1n0332

Decode it and then enter the site 
The site is broken with not visible images. 

From there, get the steg image (the third image in the site)

![alt text](image-1.png)

- Also if you press it, you may see a flag like thing, don't worry it's a RED herring.

Then if you get echoes.jpg and do

steghide extract -sf echoes.jpg

And then for the passphrase, put $#1n0332 because I have already given in the description that her passwords became the same everywhere, so putting it leads you to get a Drive link

If you open the Drive Link, you'll be rewarded with a PDF.

If you open the PDF, you can see that some texts are redacted. But no issues because if you copy all the texts and put in a notepad.

As you can see after this process, everything makes sense until in the end, there is random gibberish

If you look closely, it's the last part of a pastebin URL.

If you put it along with the full pastebin URL, you'll be rewarded with DOT cipher 

Put it in thins link,
https://www.dcode.fr/pollux-cipher

When decoded gives the full actual FLAG!
CYS{HERACTUALECHOES}

