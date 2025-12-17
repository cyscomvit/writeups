---
layout: writeup

title: Shattered Glass Logs
difficulty: Medium
points: 500
categories: [Forensics]
tags: []

flag: CYS{gl4ss_un5h4tt3rd}
---

## Shattered Glass Logs
- **Category**: [Forensics]
- **Author**: [Htarizzs]

## Challenge Description
[Find the flag by reconstructing the hidden message scattered across multiple fragmented and tampered system logs.]

## Solution

### Initial Analysis
- **Reconnaissance**
Upon receiving several ```.log``` files, started with a manual inspection using cat and less to preview their contents and overall event structures.
- **Metadata & Consistency Check**
Examined timestamps, event flows, and error messages for clues about which log fragments could be authentic versus tampered.
- **Keyword/Pattern Search**
Used ```grep``` to extract all unique data fragments and looked for recurring suspicious patterns—like out-of-place error codes or data that did not match the rest of the logs.

### Tools Used
- [grep]
- [neovim]
- [online vignere cypher/decypher tool]

### Step-by-Step Solution

#### Step 1: [List and Inspect Log files]
[There are 5 log files, go through them]

#### Step 2: [Look for Curly braces]
[Look for logs containing the curly braces, as it is unusual for a log and most prolly a flag]

#### Step 3: [Search for any word that is out of place]
[As the found flag is encrypted using Vignere cypher, it requires an extra key, hence this word is prolly that! Here, it is cyscom]

### Flag
```
CYS{gl4ss_un5h4tt3rd}
```
