---
layout: writeup

title: The Watcher's Gaze
difficulty: Medium
points: 500
categories: [OSINT]
tags: []

flag: CYS{341184_125001_6B011D}
---

## The Watcher's Gaze

- **Category**: [OSINT]
- **Author**: [Akshitha]

## Challenge Description
Go through a variety of open source data and find out the observer's den. Follow lyra's trail but beware do not get caught. 
All you need is right infront of your eyes, just know where to look.

## Solution

### Initial Analysis
Build up a narrative, look at various social media platforms, come up with a cohesive plot that built on the story.

### Tools Used
- Metadat2go
- Instagram
- Github
- Google docs

### Step-by-Step Solution

#### Step 1: The Image

<img width="750" height="422" alt="image" src="https://github.com/user-attachments/assets/eed1ecfe-6e15-4d74-bee0-7e123142b529" />

The binary numbers are decoys, they dont point to anything important 

Things to dedue:

i.	Bottom right: Instagram account (hinted by the purple/ blue colour scheme) @LC_HOURGLASS

ii.	Extracting meta data

<img width="738" height="827" alt="image" src="https://github.com/user-attachments/assets/5cc475ba-d453-4621-9025-4231d330328c" />


We see a hex value (6B011D)

It is a part of the flag, to be noted and kept




#### Step 2: The Instagram account

<img width="940" height="290" alt="image" src="https://github.com/user-attachments/assets/b4dd9be4-f75a-4fad-ba09-32c53f821ae6" />

The bio points to a username (Caellum-Archivist)

<img width="940" height="318" alt="image" src="https://github.com/user-attachments/assets/9cf91ad8-9a6a-450e-95f8-1e17ddbcc8cb" />

Upon inspection of the post caption, the last line has weird capitalization 

In the word gift notice only capital letters (GIT)



#### Step 3: The github

<img width="940" height="833" alt="image" src="https://github.com/user-attachments/assets/7096aa1f-b445-48b3-98cb-b4b4a2202037" />


In the old haven archive 

<img width="940" height="412" alt="image" src="https://github.com/user-attachments/assets/21e233c9-0612-4c02-acb3-7debf4e81c89" />

90210 points to a famous los angeles pincode 

The reset attempts are dummies

Shes-gone-and-its-just-me-repo:-

<img width="940" height="424" alt="image" src="https://github.com/user-attachments/assets/e08fe9cd-64ca-4003-a339-06b737174409" />

Multiple access_gate decoys so even if we want to get password from code it takes a little bit of time

<img width="940" height="330" alt="image" src="https://github.com/user-attachments/assets/6bea8346-7dfd-450a-a6c2-3e368aec8aae" />

README points to a link

<img width="940" height="385" alt="image" src="https://github.com/user-attachments/assets/e7dccaf3-9c6d-48f7-ae8c-f0f4767c384b" />

Enter the CITY NAME

Code- losangles/la

<img width="940" height="439" alt="image" src="https://github.com/user-attachments/assets/b9a9d0ef-6681-4d8d-aada-b668a8ddc9a0" />



#### Step 4: The Google Doc

The information is all filler 

<img width="653" height="605" alt="image" src="https://github.com/user-attachments/assets/caa132d8-bfde-4824-b4cc-582eacaf99ec" />

Location coordinates of the picture point to 

Griffith Observatory  : 34.1184° N, 118.3004° W

Rest of the text is white and revealed when selected

<img width="940" height="474" alt="image" src="https://github.com/user-attachments/assets/215469ba-3b60-436d-ac2b-5d0758abc278" />

Time: 12:47 + 3mins+ 1 sec
12:50:01

Piece together final flag from "VITAL DATA"

### Flag
```
CYS{341184_125001_6B011D}
```
