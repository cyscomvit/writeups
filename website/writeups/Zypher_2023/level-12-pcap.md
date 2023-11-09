---
layout: writeup

title: Level 12 - PCAP
difficulty: medium
points: 60
categories: [forensics, network]
tags: []

flag: zyp{We1Com_R3Dact3d_4130}
---

## Challenge

You are given a [network_mitm.pcap](writeupfiles/level12/network_mitm.pcap) file

## Solution

Extract contents using [NetworkMiner](https://www.netresec.com/?page=NetworkMiner)

![](writeupfiles/level12/1.png){:width="70%"}

Load in the pcap file and extract the zip file

![](writeupfiles/level12/2.png){:width="70%"}

Extract flag.zip using hashed password inside welcome.pdf

Decrypt hashing using [CrackStation](https://crackstation.net/)

![](writeupfiles/level12/3.png){:width="70%"}

Extract the files using password `welC0me`

![](writeupfiles/level12/4.png){:width="60%"}

```bash
$ cat flag.txt
```
