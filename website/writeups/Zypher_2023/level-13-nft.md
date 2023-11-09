---
layout: writeup

title: Level 13 - NFT
difficulty: medium
points: 60
categories: [misc]
tags: []

flag: zyp{reward_6228}
---

## Challenge

You have been given a file called [image.nft](writeupfiles/level13/image.nft)

### Hints

1. Look at this [hint](writeupfiles/level13/hint1.txt)

## Solution

Download the file

Here `Z0d1ac_1` seems to look like a username. Let's google `digital market for sea of art` and see if something related to nfts comes up.

![google](writeupfiles/level13/1.png){:width="80%"}

The first link itself comes up to be the biggest nft marketplace and we the link the word `sea` to opensea from previous hint. Lets lookup for `Z0d1ac_1` username in opensea.

![opensea](writeupfiles/level13/2.png){:width="80%"}

![opensea](writeupfiles/level13/3.png){:width="80%"}

On the profile page of Z0d1ac_1 you can see the same nft as image.nft file, open
the NFT

![opensea](writeupfiles/level13/4.png){:width="70%"}

In the description it key is `mastermind`

When you look in the item activity section, you’ll find transfers between different entities of Z0d1ac but one suspicious account involved in all these transfers is `RU55I4N_M45T3R`

![opensea](writeupfiles/level13/5.png){:width="80%"}

When you look for the `RU55I4N_M45T3R` username, you’ll find another NFT

![opensea](writeupfiles/level13/6.png){:width="80%"}

![opensea](writeupfiles/level13/7.png){:width="80%"}

In the description you can see the reward link

![opensea](writeupfiles/level13/8.png){:width="80%"}

Go to [https://www.dcode.fr/cipher-identifier](https://www.dcode.fr/cipher-identifier) and look for possible ciphers

![opensea](writeupfiles/level13/9.png){:width="80%"}

Here we can see that highest probability is for ASCII Code

![opensea](writeupfiles/level13/10.png){:width="80%"}
