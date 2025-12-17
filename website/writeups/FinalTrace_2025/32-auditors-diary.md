---
layout: writeup

title: Auditor's Diary
difficulty: Medium
points: 500
categories: [OSINT/TEXT]
tags: []

flag: CYS{olofkgustafsson}
---

## Auditor's Diary

- **Category**: OSINT/TEXT
- **Author**: S S Kishore Kumar

## Challenge Description
You given the Auditor's Log: MDE-12.1993 from the Auditor's diary . 

There is famous foreign historical figure hidden in the file. 

Identify him and the CEO of the company named after him is gives you the flag.
 
Flag format : CYS{<founder>} (all in lower-case , with no spaces).

## Solution

### Initial Analysis
Read the log and find its about Pablo Escobar , The company Escobar Inc. and its founder Olof K Gustafsson

### Tools Used
- Wikipedia
- Textfile

### Step-by-Step Solution

#### Step 1: [Read the audit-diary.md]
The log in it is based on Pablo Escobar.

#### Step 2: [Find the founder]
The company based of him is Escobar Inc. and its founder is Olof K Gustafsson

### Flag
```
CYS{olofkgustafsson}
```
