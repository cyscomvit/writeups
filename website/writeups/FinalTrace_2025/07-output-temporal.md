---
layout: writeup

title: Output: TEMPORAL
difficulty: Medium
points: 500
categories: [General]
tags: []

flag: FLAG{ECHO_VAULT_MEMORY_FRAGMENT_7A_RESTORED}
---

Challenge Name: VAULT_7A

Category: Forensics / Steganography
Author: Vishal V
Difficulty: Easy


Challenge Description
Within the Echo Maze, you discover a flickering hologram capsule labeled "VAULT_7A". The projection stutters between timeframes, overlaying multiple moments into a single distorted image.
Lyra's voice echoes: "Some memories hide in layers... peel them back carefully."

Downloads:
temporal_fragment.jpg
hint.txt


Solution:
Initial Analysis
Upon downloading the challenge files, I was presented with:
A JPEG image file (temporal_fragment.jpg)
A hint file (hint.txt)

First, I examined the basic file properties:
bash: file temporal_fragment.jpg
Output:temporal_fragment.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, baseline, precision 8, 360x360, components 3
No immediate clue was found. From challenge description "...peel them back..." , we can infer it must be something related to steganography. 

Tools Used:
steghide - JPEG/BMP steganography tool
base64 - Base64 decoder (built-in Linux/Mac command)
zbarimg - QR code scanner (from zbar-tools package)
Online Caesar cipher decoder (or manual decoding)
Online QR scanner (https://webqr.com) as alternative


Step-by-Step Solution
Step 1: Decode the Passphrase from hint.txt
Reading the hint file revealed an encoded passphrase:
bash: cat hint.txt


Key information found:
- Encoded passphrase: ALTWVYHS
- Hint: "Time shifts all things forward. To find truth, shift backwards 7 times."
- Encryption method: TEMPORAL SHIFT PROTOCOL (Caesar/ROT cipher)

The hint indicates a Caesar cipher with shift of 7. To decrypt, I needed to shift each letter backward by 7 positions in the alphabet.

Manual decoding:

A - 7 = T
L - 7 = E  
T - 7 = M
W - 7 = P
V - 7 = O
Y - 7 = R
H - 7 = A
S - 7 = L

Result: TEMPORAL
Alternatively, using an online ROT decoder or Python:
Python code: 
def rot_decode(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - start - shift) % 26 + start)
        else:
            result += char
    return result

print(rot_decode("ALTWVYHS", 7))

# Output: TEMPORAL
Passphrase obtained: temporal
Step 2: Check for any hidden images inside the given image: 
bash: steghide info temporal_fragment.jpg 
Output: steghide info temporal_fragment.jpg
"temporal_fragment.jpg":
  format: jpeg
  capacity: 634.0 Byte
Try to get information about embedded data ? (y/n) y
Enter passphrase: 
  embedded file "qr_secret.png":
    size: 481.0 Byte
    encrypted: rijndael-128, cbc
    compressed: yes
Found a embedded file qr_secret.png!!

Step 3: Extract Hidden Data Using Steghide
With the passphrase decoded, I used steghide to extract hidden data from the image:
bash: steghide extract -sf temporal_fragment.jpg -p "temporal"

Output:
wrote extracted data to "qr_secret.png"
Success! The steghide tool extracted a hidden PNG file.


Step 4: Decode the QR Code
Using zbarimg to scan the QR code:
bash: zbarimg qr_secret.png
```

Output:

QR-Code:RkxBR3tFQ0hPX1ZBVUVUX01FTU9SWV9GUkFHTUVOVF83QV9SRVNUT1JFRH0=
The QR code contained a base64-encoded string.

OR 
use a online qr decoder.

Step 5: Decode Base64 String
The QR output was clearly base64 (ending with = padding). Decoding it:
bash: echo "RkxBR3tFQ0hPX1ZBVUVUX01FTU9SWV9GUkFHTUVOVF83QV9SRVNUT1JFRH0=" | base64 -d
Output: 
FLAG{ECHO_VAULT_MEMORY_FRAGMENT_7A_RESTORED}




Alternative Solution Paths
Without Knowing the Password
If the passphrase wasn't decoded, players could use stegseek to brute-force it:
bash# Install stegseek
sudo apt-get install stegseek

# Crack with common wordlist
stegseek temporal_fragment.jpg /usr/share/wordlists/rockyou.txt
This would find "temporal" in seconds since it's a common word.

Using Online Tools
For players without CLI tools:
Use online Caesar decoder: https://cryptii.com/pipes/caesar-cipher
Extract with steghide (requires installation)
Use online QR scanner: https://webqr.com
Use online base64 decoder: https://www.base64decode.org


