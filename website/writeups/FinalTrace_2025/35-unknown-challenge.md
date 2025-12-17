---
layout: writeup

title: Unknown Challenge
difficulty: Medium
points: 500
categories: [General]
tags: []

flag: CYS{temporal_merge_success}
---

CTF61: Temporal Mergepoint
Category: Web

Author: riya mishra

Challenge Description
Access control in a futuristic research portal fails. Users can view logs via /portal?user_id=<id>. Can you find the secret flag by manipulating parameters?

Solution
Initial Analysis
Visited / and saw hints about the portal endpoint. Tried accessing my user ID first.

Tools Used
Web Browser (Chrome/Edge)

Burp Suite (optional)

Python Flask server

Step-by-Step Solution
Step 1: Check my own logs
text
Visited: http://127.0.0.1:5000/portal?user_id=10
Result: {"user":"player","log":"Access denied: unauthorized"}
Access was denied for default user.

Step 2: Test other IDs
text
Changed to: http://127.0.0.1:5000/portal?user_id=9
Result: {"user":"admin","log":"CYS{temporal_merge_success}"}
Found that the server returned the flag for user ID 9.

Flag
text
CYS{temporal_merge_success}