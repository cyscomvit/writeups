---
layout: writeup

title: Challenge Description
difficulty: Medium
points: 500
categories: [Forensics]
tags: []

flag: CYS{THE_CLOCKS_WERE_LYING}
---

#6 Lyra's Journal

- **Category**: [Forensics]
- **Author:** [Nihara Oommen]

## Challenge Description
[There are 15 such fragments scattered across files. Each fragment is appended into some of the JPEG files as plain ASCII in the raw bytes in the form `CYS{fragment} YYYY-MM-DDTHH:MM:SS`. Sorting the found fragments by timestamp reveals the final flag.]

## Solution

### Initial Analysis
[I inspected the provided files and the generator script. The images looked normal in viewers, so I suspected the fragments were embedded in the raw file bytes (not visible pixels). The pattern `CYS{` suggested a simple ASCII string was appended to some JPEG files.]

### Tools Used
- `Select-String` (PowerShell)
- `sort-object` (PowerShell)
- `unzip` (to extract the challenge ZIP)
- `PowerShell`
- `Python` (optional, for automation)

### Step-by-Step Solution

#### Step 1: Extract the files
```
tar -xf journal_pages.zip
```
Extracts all `page_###.jpg` into `journal_pages/` for inspection.

#### Step 2: Find the hidden fragments
```
Select-String -Path .\journal_pages\*.jpg -Pattern "CYS{" | ForEach-Object { $_.Line }
```
This finds lines like:
```
CYS{T} 2087-09-22T00:12:00
CYS{H} 2087-09-22T00:21:00
...
```
(Each hit is the fragment plus its timestamp.)

#### Step 3: Sort fragments by timestamp and assemble the flag
```
Select-String -Path .\journal_pages\*.jpg -Pattern "CYS{" | ForEach-Object {
    $line = $_.Line
    if ($line -match "CYS\{([^}]+)\}\s*([0-9T:-]+)") {
        [PSCustomObject]@{ Fragment = $matches[1]; Timestamp = [datetime]::ParseExact($matches[2],"yyyy-MM-ddTHH:mm:ss",$null) }
    }
} | Sort-Object Timestamp | ForEach-Object { $_.Fragment } > sorted_fragments.txt
```
Explanation: after sorting by the ISO timestamps, concatenating the fragments in order reconstructs the inner flag message.

### Flag
```
CYS{THE_CLOCKS_WERE_LYING}
```
