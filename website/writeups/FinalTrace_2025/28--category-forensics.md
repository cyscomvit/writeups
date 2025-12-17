---
layout: writeup

title: Phantom Fingerprints
difficulty: Medium
points: 500
categories: [Forensics]
tags: []

flag: CYS{ph4n7om_v3n0m}
---

##  
- **Category**: [Forensics]
- **Author**: [Htarizzs]

## Challenge Description
[Use the provided netcat service and query logs to identify and analyze the activity of a phantom user whose fingerprints appear in the device logs, but who does not correspond to any registered account. Find and submit their session's flag.]

## Solution

### Initial Analysis
- **Reconnaissance** 
Begin by connecting to the provided netcat service (e.g., ```nc challenge.host 1337```).
Review the welcome message, available commands (usually presented with a help command), and the structure of returned data.
- **Information Gathering**
Use commands like show logs, query user <id>, query fingerprint <id>, etc., to get an inventory of normal and phantom records, paying attention to any IDs, timestamps, or unusual entries.

### Tools Used
- [netcat (nc)]
- [python3 (py)]

### Step-by-Step Solution

#### Step 1: [Connect & Explore]
```
nc localhost 1337
help
show logs
```
[The terminal is bought up, which will only work with specific commands which are specified in help.]

#### Step 2: [Find the phantom user]
```
query user 0x9999
query fingerprint fp9999
```
[Phantom(Unknown) user is found out, and try inspecting their fingerprint to get the flag in base64 format]

#### Step 3: [Decode the base64 string]
Decoding the base64 string obtained will give the flag

### Flag
```
CYS{ph4n7om_v3n0m}
```
