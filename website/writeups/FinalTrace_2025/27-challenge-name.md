---
layout: writeup

title: Challenge Name
difficulty: Medium
points: 500
categories: [Forensics (E)]
tags: []

flag: CYS{INH4RM0N1C_DO0R_UNL0CK3D}
---

## Challenge Name  
**Feed It the Fracture**

- **Category**: Forensics (E)
- **Author**: Vignesh K S

---

## Challenge Description  
An audio file contains a hidden passcode. Once you unlock the vault, you’ll find a series of clues — morse code, ASCII, Base64 — leading to the final flag.

---

## Solution

### Initial Analysis  
Started by listening to the audio file. The dialogue hinted at a number sequence. There was also a password-protected zip file named `vault.zip`.

---

### Tools Used  
- Morse Code Decoder  
- ASCII to Text Converter  
- Base64 Decoder  
- Rentry.org

---

### Step-by-Step Solution

#### Step 1: Decode the Passcode from Audio  
```
The conversation hinted at the pincode 600127.  
Removed the zeroes → got 6127.
```
Used `6127` to unlock `vault.zip`.

---

#### Step 2: Solve the Morse Code  
```
Found a morse code file inside the zip.  
Decoded it to get a string.
```

---

#### Step 3: Decode ASCII in the URL  
```
Converted ASCII values to text.  
Revealed a Base64 string.
```

---

#### Step 4: Decode Base64  
```
Decoded the Base64 string to get a URL.
```

---

#### Step 5: Visit the URL  
```
Opened the URL on rentry.org.  
Found the final flag.
```

---

### Flag  
```
CYS{INH4RM0N1C_DO0R_UNL0CK3D}
```