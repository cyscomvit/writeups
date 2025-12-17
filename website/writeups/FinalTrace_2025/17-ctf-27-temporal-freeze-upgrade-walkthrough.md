---
layout: writeup

title: CTF #27 – Temporal Freeze Upgrade | Walkthrough
difficulty: Medium
points: 500
categories: [General]
tags: []

flag: cys{T1M3_SYNC}
---

# CTF #27 – Temporal Freeze Upgrade | Walkthrough

## Objective
Solve the mirror puzzle to decrypt the flag: `cys{T1M3_SYNC}`

---

## Step 1: Understand the Mirrors
You have 4 mirrors to select in the correct order:
- Mirror 0 (◈) - 0x00
- Mirror 1 (◉) - 0x01
- Mirror 2 (◊) - 0x02
- Mirror 3 (◆) - 0x03

---

## Step 2: Find the Pattern
Look at the **QUANTUM_STATE_DECAY** values:
- Mirror 0: Decay = 5
- Mirror 1: Decay = 8
- Mirror 2: Decay = 3
- Mirror 3: Decay = 6

**Key Insight:** Order mirrors by lowest to highest dec ay value.

---

## Step 3: Correct Sequence
Click mirrors in this order:
1. **Mirror 2** (◊) - Decay 3
2. **Mirror 0** (◈) - Decay 5
3. **Mirror 3** (◆) - Decay 6
4. **Mirror 1** (◉) - Decay 8

---

## Step 4: Get the Encrypted Flag
When solved correctly, you'll see:
```
DECRYPTION_KEY: [encrypted characters]
```

Copy this encrypted string.

---

## Step 5: Decrypt the Flag
Open **Browser Console (F12)** and paste:
```javascript
const encryptedFlag = "[PASTE_YOUR_ENCRYPTED_KEY_HERE]";

for (let offset = 1; offset <= 50; offset++) {
    let decrypted = '';
    for (let i = 0; i < encryptedFlag.length; i++) {
        decrypted += String.fromCharCode(encryptedFlag.charCodeAt(i) - offset);
    }
    
    if (decrypted.startsWith('cys{')) {
        console.log('Flag: ' + decrypted);
        break;
    }
}
```

---

## Step 6: Submit Flag
The decrypted flag will appear in console:
```
cys{T1M3_SYNC}
```

---

## Tips
- Use **ANALYZE** button for hints if stuck
- Watch **TEMPORAL_ALIGNMENT** section as you select
- The **decay values are the key** to solving it
- Wrong sequence resets after 3 seconds
- Each solve generates a unique encrypted flag

---

## Quick Reference
| Position | Mirror | Symbol | Decay |
|----------|--------|--------|-------|
| 1st      | 2      | ◊      | 3     |
| 2nd      | 0      | ◈      | 5     |
| 3rd      | 3      | ◆      | 6     |
| 4th      | 1      | ◉      | 8     |

