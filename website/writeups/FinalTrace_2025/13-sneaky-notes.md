---
layout: writeup

title: Sneaky Notes
difficulty: Medium
points: 500
categories: [Web]
tags: []

flag: CYS{sneaky_notes_xss}
---

## Sneaky Notes

- **Category**: [Web]
- **Author**: [Akshitha]

## Challenge Description
Some notes were left behind, look deeper and you will find what is yours.

## Solution

### Initial Analysis
Look at easy potential web exploits to use 

### Tools Used
- Python
- Flask

### Step-by-Step Solution

#### Step 1: Login page
   
   <img width="940" height="400" alt="image" src="https://github.com/user-attachments/assets/fc04b343-df27-4891-9efb-36f9a14a22c7" />

#### Step 2:	Inspect and get credentials

<img width="940" height="283" alt="image" src="https://github.com/user-attachments/assets/38cbb7c8-4a20-4dd4-9702-54b093805560" />

#### Step 3 :XSS payload in notes page to get flag
<img width="940" height="462" alt="image" src="https://github.com/user-attachments/assets/f16cc1d7-466f-40a0-8489-26a3804c963f" />

 #### Step 4:	Flag found
 <img width="940" height="364" alt="image" src="https://github.com/user-attachments/assets/3b4683ab-a02e-44ce-968b-2b646105436c" />

 

### Flag
```
CYS{sneaky_notes_xss}
```
