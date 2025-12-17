---
layout: writeup

title: POEM OF HIDDEN LIES
difficulty: Medium
points: 500
categories: [OSInt/Forensics/Text]
tags: []

flag: CYS{january_2019}
---

## POEM OF HIDDEN LIES

- **Category**: OSInt/Forensics/Text
- **Author**: S S Kishore Kumar

## Challenge Description
Govindaraja a budding entreprenuer has writte a poem , Find clues from his poem, unravel his life and his hidden secrets and finally capture THE FLAG!!

## Solution

### Initial Analysis
The diary entry leads to github and with further analysis leads to the flag.

### Tools Used
- Steghide
- Google.com
- Google Drive
- Base 64 encoder/decoder
- Instagram
- Github


### Step-by-Step Solution

Step 1: [Find the github account]
Upon analysing the file you find out the github handle Govindaraja-GopalaKrishna-Ricky and the Public-Talk rep . (All these names are in the initial challenge file but hidden)

#### Step 2: [Read the readme.md file]
After reading the readme file you find out a password "IAuditYou" and the word "Base64" in it. Which are crucial for next steps.

#### Step 3: [Finding the correct file]
There are multiple files in the rep , among which only one leads to the next step . Which is "RmluYWxUcmFjZQ==.zip" and RmluYWxUcmFjZQ== can be decoded to FinalTrace (Event name) using a base64 decoder.

#### Step 4: [Analyze the file]
The zip file is password protected with "IAuditYou" and there are 5 images name 1,2,3,4,5.jpg among which img 3 has a hidden text file embedded. (3 can be chosen easily as if you inspect challenge file closely the verses are 3.3,3.33,3.333)

#### Step 5: [Find the text file in 3.jpg]
Using steghide and the passphrase same as before "IAuditYou" you get a second.txt file hidden in it.

#### Step 6: [Analyze second.txt]
The text file leads to a google drive link with a zip file of 3 images and a text file. The password for this is "QuantumLeap Inc.". As second.txt says "However successful you become in life don't forget where you came from.". Which points to the challenge file which has the password.

#### Step 7: [Analyze readme2.txt]
readme2.txt says about the flag which is that "there is three images below out of these 3 , find the most liked one and see when they have created their youtube/instagram/twitter (oldest one)

CYS{month_year}

#### Step 7: [Find the flag]
Among those images the egg is the most liked picture . And the insta account was created on 19th January

### Flag
```CYS{january_2019}```
