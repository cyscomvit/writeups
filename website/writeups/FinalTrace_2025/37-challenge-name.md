---
layout: writeup

title: Auditor Encounter
difficulty: Medium
points: 500
categories: [Web / ARG]
tags: []

flag: CYS{aud1t_regr3t_pass}
---

- **Category**: Web / ARG
- **Author**: Oviya

## Challenge Description
An animated in-page “Auditor” asks a single question: “Do you regret what you created?”  
This is a static web challenge (HTML + CSS + JS). The player replies via a small dialogue input. If the player responds with `yes`, the Auditor prints the flag; `no` yields a cryptic denial. The flag is obfuscated (base64) inside the client-side script.

## Solution

### Initial Analysis
I opened the challenge in the browser and inspected the page source. Since the site is static, I looked for client-side JavaScript (either inline or linked as `static/script.js`). The flag was not directly visible in the HTML, so I checked the JavaScript file for any encoded strings or decode logic.

### Tools Used
- Browser Developer Tools (View Source / DevTools)
- Text editor (VSCode)
- Command line base64 utilities or Python for decoding

### Step-by-Step Solution

#### Step 1: Open the page and view source / linked script

In the browser: Right click → View Page Source
Or open linked file directly:
open static/script.js # or use your editor to open the file
Explanation: The page is static. The script reference (`static/script.js`) contains the dialogue logic and probably hides the flag in an encoded form.

#### Step 2: Locate the base64-encoded flag string in the JavaScript

Search for common patterns in the JS file
grep -n "FLAG_B64" static/script.js
or open the file and look for base64-like strings (long strings with letters/numbers/+ / =)
Explanation: The script held a variable named `FLAG_B64` with a base64 string. This indicates the flag is client-side but obfuscated.

#### Step 3: Decode the base64 string to obtain the flag

Example using Linux base64 tool (replace the string with the one found)
echo 'Q1lTfGF1ZGl0X3JlZ3JldC5wYXNzfQ==' | base64 --decode

OR using Python:
python3 -c "import base64; print(base64.b64decode('Q1lTfGF1ZGl0X3JlZ3JldC5wYXNzfQ==').decode())"

OR in browser console (if the site exposes it):
atob('Q1lTfGF1ZGl0X3JlZ3JldC5wYXNzfQ==')

Explanation: Decoding the base64 string reveals the flag in plain text. Any of the above methods will produce the same result.

### Flag
CYS{aud1t_regr3t_pass}
