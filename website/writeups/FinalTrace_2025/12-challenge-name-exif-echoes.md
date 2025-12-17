---
layout: writeup

title: Challenge Name - EXIF ECHOES
difficulty: Medium
points: 500
categories: [Forensics/OSint]
tags: []

flag: CYS{T1m3_Fr4gm3nt5_R3v34l_Th3_P4th}
---

## Challenge Name - EXIF ECHOES
- **Category**: [Forensics/OSint]
- **Author**: [ram]

## Challenge Description
[This `m0ment` is more than it appears. Its very properties are... peculiar. Only by understanding its deepest whispers can you unlock the path.]

## Solution

### Initial Analysis
[As the challenge title suggests "EXIF," the first step is to run `exiftool` on the image. This would reveal two unusual timestamps. The "echoes" hint at a combination of these two values.]
### Tools Used
- [exiftool]
- [timestamp->epoch unix ( https://www.epochconverter.com/ ) ]
- [ Hexadecimal XOR calculator (e.g., [https://xor.pw/] ]
- [stegseek]

### Step-by-Step Solution

#### Step 1: [Discover and Convert Timestamps]
```
[exiftool m0ment.jpg]
```
[they scan exiftool, encounter a fake flag , which is a pastebin link which gives them sime vague hint ( btw bonus flag hidden as the authorname )(pastebin.com/r3LnLw4G ) ]


#### Step 2: [Generate the Passphrase via XOR]
```
[# No command, but use a hex XOR calculator
# Input 1 (hex): 1681140600
# Input 2 (hex): 1727203620 
# Output (hex): 1a6343020]
```
[This step accomplishes the core trick of the challenge. By treating the two epoch values as hexadecimal numbers and XORing them, we generate the final passphrase (1a6343020) needed for extraction.]

#### Step 3: [Extract the Hidden File , and hence the flag]
```
echo "1a6343020" > pass.txt
stegseek m0ment.jpg pass.txt
cat m0ment.jpg.out
```
[This command uses stegseek to rapidly test our generated password (1a6343020) against the image. stegseek confirms the password is correct and extracts the hidden file, saving it as m0ment.jpg.out.]

### Flags
```
CYS{b0nus_fl1g_686}
CYS{T1m3_Fr4gm3nt5_R3v34l_Th3_P4th}
```
