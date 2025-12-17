---
layout: writeup

title: Do you know XOR well enough?
difficulty: Medium
points: 500
categories: [General]
tags: []

flag: Dynamic Flag
---

# Do you know XOR well enough?

 * Category: Cryptography
 * Author: P C Guhan 

## Description

> Random numbers, AES encryption, SHA 256, HMAC, constant-time hash checking... what more do you want?
> All are imported functions, hence highly secure
> Or is it??

## Solution
![AES CBC Encryption](image.png)
![AES CBC Decryption](image-1.png)

This method uses the previous block to encrypt the next block. The same follows for decryption also. Hence, a bit flip will alter the plaintext.

Each hex requires two characters. The length of "admin=0" is 7. 
The hex output consists of the 16 bit IV and the 16 bit padded ciphertext. The IV is XOred with the decrypted ciphertext.

To get admin=1, we XOR the 6th character block with 1.
i.e. IV[6] ^ decrypted(message[6]) ^ 1 = 0 ^ 1
since 0 ^ 1 = 1, 

IV[6] ^ decrypted(message[6]) ^ 1 = 1
giving us admin=1

A corresponding hash can be generated as the hashing algorithm is open source.

To mitigate this vulnerability while still using AES CBC mode, AEAD (Authenticated Encryption and Additional Data) must be used i.e. hashing with a secret key.

## Script
```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import hashlib
import hmac
import random

# --- setup (same as challenge) ---
key = get_random_bytes(16)
iv = get_random_bytes(16)

part1 = "AES"
part2 = ''.join(random.choices(string.ascii_uppercase, k=5))
part3 = "AEAD"
part4 = f"{random.randint(0, 999999):06d}"
part5 = ''.join(random.choices(string.ascii_uppercase, k=3))
flag = "CYS{" + f"{part1}_{part2}_{part3}_{part4}_{part5}" + "}"

def encrypt_data(data):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    enc = cipher.encrypt(pad(data.encode(), 16, style='pkcs7'))
    return enc.hex()

def decrypt_data(encryptedParams):
    data = bytes.fromhex(encryptedParams)
    if len(data) < 16:
        raise ValueError("Ciphertext too short")
    iv_in = data[:16]
    ciphertext = data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv_in)
    paddedParams = cipher.decrypt(ciphertext)
    plaintext = unpad(paddedParams, 16, style='pkcs7')
    return plaintext.decode(errors='ignore')


print("Just copy and paste? Hash is also given...")
msg = "admin=0"
print("\nCurrent authentication message is : " + msg)
print("Turn it to admin=1")

cipher_hex = encrypt_data(msg)
iv_cipher = iv.hex() + cipher_hex
print("\nEncryption of authentication message in hex : " + iv_cipher)


hashed_value = hashlib.sha256(iv_cipher.encode('utf-8')).hexdigest()
print("SHA-256: ", hashed_value)

# -----------------------------
# Solution
# Reliable CBC bit-flip to change admin=0 -> admin=1
# -----------------------------
orig_msg = "admin=0"
target_msg = "admin=1"

p0 = pad(orig_msg.encode(), 16, style='pkcs7')[:16]
p1 = pad(target_msg.encode(), 16, style='pkcs7')[:16]

delta = bytes(a ^ b for a, b in zip(p0, p1))

iv_prime = bytes(a ^ b for a, b in zip(iv, delta))

enc_msg = iv_prime.hex() + cipher_hex
enc_hash = hashlib.sha256(enc_msg.encode('utf-8')).hexdigest()


# --- setup (same as challenge) ---
try:
    if hmac.compare_digest(hashlib.sha256(enc_msg.encode('utf-8')).hexdigest(), enc_hash):
        final_dec_msg = decrypt_data(enc_msg)
        print(final_dec_msg)

        if "admin=1" == final_dec_msg:
            print(flag)
        else:
            print('\nTry again you can do it!!')
    else:
        print("\nHashing failed")
        print(hashlib.sha256(enc_msg.encode('utf-8')).hexdigest() + "\n\n")
        print(enc_hash)
except Exception as e:
    print('\nbye bye!!', e)

```