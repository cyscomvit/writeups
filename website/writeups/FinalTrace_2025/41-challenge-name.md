---
layout: writeup

title: Challenge Name
difficulty: Medium
points: 500
categories: [Web / ARG]
tags: []

flag: CYS{audit_recovered_1A3F_07XZ}
---

## Challenge Name
**CTF17 — Auditor Encounter**

- **Category**: Web / ARG
- **Author**: Oviya 

---

## Challenge Description
In this challenge, you encounter **The Auditor**, a mysterious entity that reviews your actions in the fractured timeline.  
Through an interactive dialogue, you must respond to his questions about your past interference in the archive.  
Each response leads to a different outcome — hidden clues, distinct checksums, and unique session identifiers, all combining to form your final flag.  

The true test lies in observation and deduction — the data is never handed over directly, but concealed cleverly in the background.  

---

## Solution

### Initial Analysis
On opening the webpage, the interface shows **The Auditor**, who initiates a conversation in a typewriter-style effect.  
After a few exchanges, the player is presented with **four choices**, each representing a possible action from the past.  

Inspecting the code reveals a `fetch()` request silently retrieving a hidden resource (which in this case is disguised or embedded), and a **flag format** hint inside the script logic.

The flag format is:
CYS{audit_recovered_<checksum>_<sessionid>}
---

### Tools Used
- Web Browser (Developer Tools → Network & Sources)
- Basic JavaScript inspection
- Notepad / VS Code for viewing HTML source

---

### Step-by-Step Solution

#### Step 1: Observation and Interaction
When the page loads, **The Auditor** introduces the scenario and begins questioning your actions.  
Once prompted, four choices appear, each corresponding to a distinct decision path.

#### Step 2: Inspecting the Network or Script
Upon selecting any choice, no flag is directly revealed.  
However, by checking the **Developer Tools → Sources or Network tab**, you can find that the hidden clue is retrieved or encoded within the script itself.  
Each path outputs a **checksum** and **sessionID** that you must fit into the given flag format.

#### Step 3: Reconstructing the Flag
Using the format and the given data, you reconstruct your flag as:
CYS{audit_recovered_<checksum>_<sessionid>}
---

### Path Outcomes and Flags  

Each decision leads to a unique audit result with a distinct checksum and session ID.  
These combine to form four valid flags depending on the path you choose:

| **Choice** | **Description** | **Checksum** | **SessionID** | **Final Flag** |
|-------------|-----------------|---------------|----------------|----------------|
| **Path A** | “I repaired corrupted echoes — I tried to restore what was lost.” | `1A3F` | `07XZ` | `CYS{audit_recovered_1A3F_07XZ}` |
| **Path B** | “I smashed the capsules — they were unstable and had to be purged.” | `B2D4` | `9KLM` | `CYS{audit_recovered_B2D4_9KLM}` |
| **Path C** | “I reconfigured terminals to read restricted vaults — truth needed access.” | `C3E7` | `Q4T1` | `CYS{audit_recovered_C3E7_Q4T1}` |
| **Path D** | “I observed only. I let the archive run its course.” | `D4F9` | `Z0OP` | `CYS{audit_recovered_D4F9_Z0OP}` |

---

### Explanation of Paths
- Each path represents a **different moral response** to the Auditor’s inquiry.  
- The **checksum** and **sessionID** act as identifiers for the version of the timeline recovered.  
- These unique flags determine which branch of the overarching story or challenge you progress into next.

---

### Flag Example
If the player selects the first option:
CYS{audit_recovered_1A3F_07XZ}
---

