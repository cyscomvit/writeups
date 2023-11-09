---
layout: writeup

title: Level 11 - Zypher RE
difficulty: medium
points: 50
categories: [reverse_engineering]
tags: []

flag: zyp{S4NI5Y_17T6CT_}
---

## Challenge

You are given a [Zypher_RE.py](writeupfiles/level11/Zypher_RE.py) file

## Solution

On running the file, it asks for the username that is ‘FOX3R’ as evident
from this part of code

```python
def ui_flow():
    intro()
    if username=='FOX3R':
        while loop:
            menu()
    else:
        print("Access denied")
ui_flow()
```

After providing the username as input, we get some messages pertaining
to the overall theme of the CTF event, ZYPHER.

![](writeupfiles/level11/1.png){:width="70%"}

Choosing the Rabbit option leads us to nowhere. It must be a rabbit hole as
the name suggests.

Choosing the enter key option, it asks for a key that leads us to the key
function

```python
def key(x):
    if x==hashlib.sha256(salt.encode('utf-8')).hexdigest()[4]:
        return True
```

```python
salt = "ZYPHER"
```

We can find x by running this piece of code(encrypting salt using SHA256
after encoding it in utf-8 format)

```python
import hashlib
import cryptography.fernet import Fernet
import base64
salt = "ZYPHER"
hashlib.sha256(salt.encode('utf-8')).hexdigest()
hashlib.sha256(salt.encode('utf-8')).hexdigest()[4]
```

Now that we have found the key, let us inspect the encrypt() function

```python
def encrypt(flag,key):
    enc=''.join([chr((ord(flag[i]) << key) + ord(flag[i + 1]))+chr(ord(salt[random.randint(1, 10)])<<key) for i in range(0, len(flag), 2)])
    print(enc)
    return enc

def decrypt(enc_text,key):
    ...
    #return flag
    #use the flag to unlock file
```

```
#encrypt('FLAG', x)
```

We’ve found the key as 8

The encrypt function takes the flag encrypts it with the key and returns the
ciphertext(enc)

The program is prompting us to write a decrypt function to take the
ciphertext and key as parameters and return the original flag.

Also the ciphertext is already given in this part of code

```python
salt='ZYPHER'

secret_key_prior='hacker{'
secret_key_main='匴倀义刀㕙䌀弱䬀㝔䬀㙃䄀呟刀'
secret_key_latter='}'
```

Carefully investigating the encryption code, we see that the program shifts
the bits for every other letter of the flag, left by 8 bits (1 byte). Then, it adds the next letter of the flag to the shifted value .Also every other letter of ciphertext is just a random character.

We can reverse this by first removing/skipping through the random
characters.

Then we shift the bits right to get the first letter in the pair and convert the
encoded character to bytes and get the last byte to get the second letter in
the pair. The following code [decrypt.py](https://github.com/Anyr00d/Zypher-CTF-challenge-5.2/blob/main/decrypt.py)

```python
c='匴倀义刀㕙䌀弱䬀㝔䬀㙃䄀呟刀'
a=''
for i in range(0,len(c),2):
    e=chr(ord(c[i])>>8)
    a+=e
    a+=chr(ord(c[i])-(ord(e)<<8))
print(a)
```

Here ‘a’ is the final flag. We have step 2 in range to skip the random
characters

On running this decryption code, we get the flag as `S4NI5Y_17T6CT_`
