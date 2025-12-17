---
layout: writeup

title: Unknown Challenge
difficulty: Medium
points: 500
categories: [General]
tags: []

flag: FLAG{HOURGLASS_RECOVERED}
---

Challenge Name: Echoes in the Hourglass

Category: Forensics / Crypto / Binary
Author: Vishal V
Difficulty: Medium-Hard

Challenge Description
An hourglass image from the Citadel’s archives hides the encryption key to twelve lost timeline fragments (timeline_grain_*.bin).
Each fragment carries a piece of the Citadel’s final chronicle. Recover the cipher key, decrypt all fragments, and rebuild the temporal log to restore the flow of time — and uncover the last message trapped within.

Solution

Solution Summary (Internal Dev Notes):

1.Extract stego data → recover cipher_key.bin.
2.Decrypt fragments using the provided XOR script.
3.Decrypt the timestamp log via openssl aes-256-cbc.
4.Reassemble the decrypted fragments in chronological order.
5.The flag appears in one fragment: timeline_grain_autd.txt.

Initial Analysis
I listed the archive contents, inspected the image for hidden data, and examined the provided scripts. The image looked like a likely steganography container and the repository included a small XOR script (scripts/temporal_cipher.py) which suggested an XOR-based encryption of the fragments. There was also a timestamp_log.enc that was encrypted using openssl. A Hint.txt was also present having some necessary passwords which where md5 hashed.

Tools Used
•	steghide (to inspect/extract data from the image)
•	python3 (to run scripts/temporal_cipher.py)
•	Online  md5 decrypting tools 

Step-by-Step Solution

Step 1: Unpack and inspect
unzip citadel_memory_dump.zip
ls -lah
file hourglass_of_time.jpg
steghide info hourglass_of_time.jpg
I confirmed the hourglass_of_time.jpg contains embedded data(cipher_key.bin) with steghide info.
The passkey(echoes) for steghide was hidden in the hint.txt which could be broken using online md5 decrypting tools.

Step 2: Extract the cipher key from the image
steghide extract -sf hourglass_of_time.jpg -p echoes -xf cipher_key.bin
Using the steghide password (echoes), I extracted cipher_key.bin. This key is required to XOR-decrypt the timeline grains.

Step 3: Decrypt one fragment (smoke test)
chmod +x scripts/temporal_cipher.py
./scripts/temporal_cipher.py timeline_grain_ 3w@e.bin cipher_key.bin grain_ 3w@e.txt
This validated the key and script: the output showed readable part of the temporal log.
Step 4: Decrypt all fragments
for b in *.bin; do
  ./scripts/temporal_cipher.py "$b" cipher_key.bin "${b%.bin}.txt"
done 
Each fragment decrypted into a .txt file.

Step 5: Decrypt the timestamp_log.enc
file timestamp_log.enc
output: timestamp_log.enc: openssl enc'd data with salted password
This makes it clear that the file was encrypted using openssl. The password can be taken from hint.txt. The most common encryption in openssl is aes-256 hence try decrypting by that: 
openssl enc -aes-256-cbc -pbkdf2 -salt -in timestamp_log.txt -out timestamp_log.enc -pass pass:password
Decrypted file stored as timestamp_log.txt 

Step 6: Reconstruct the full log
With reference to timestamp_log.txt reconstruct each file fragment.
Concatenating the decrypted fragments in timestamp order reconstructed the original temporal log.

Step 7: Extract the flag
The flag is present in the final temporal log. 
Note: the flag is present in only one of the file fragments: timeline_grain_autd.txt, so instead of concatenating based on timestamp_log.txt the player may individually open all the 12 files to find the flag. Either way this makes this challenge time consuming. There are also 2 decoy files that are present only to confuse the player: corrupted_grain_xx.bin,memory_alpha.txt.

Flag:
FLAG{HOURGLASS_RECOVERED}
