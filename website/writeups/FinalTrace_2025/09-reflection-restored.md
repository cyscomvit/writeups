---
layout: writeup

title: Reflection Restored
difficulty: Medium
points: 500
categories: [General]
tags: []

flag: CYS{r3fl3ct10n_r3st0r3d_B2A}
---

# Reflection Restored

**Category:** Reverse Engineering, Forensics  
**Author:** Sharon

## Description

The binary `repair` asks for an input. If the input matches a criteria, a passphrase is printed. This passphrase is the steg info for `repair_mirror.jpg` attached. Inside `repair_mirror.jpg` is a text file that was embedded using **steghide**. The player needs to reverse `repair` to get the passphrase.

---

## Solution

### Initial Analysis

Run the binary; it prompts for a key. Analyse the binary statically using a reverse-engineering tool like Ghidra.

### Step-by-step solution

#### Step 1: Statically analysing the binary

Upon opening the binary for static analysis, we notice the core functions and find the main function. In the decompile, we notice:

```c
    iVar2 = valid_input(local_128);
    if (iVar2 == 0) {
      puts("Wrong.");
    }
```

iVar2 checks a function called `valid_input`.

We need to escape this by giving a valid input. Now let's analyse what a valid input is:

```c
  sVar3 = strlen((char *)param_1);
  bVar2 = false;
  if ((int)sVar3 == 0xc) {
    ppuVar4 = __ctype_b_loc();
    pbVar1 = param_1 + 0xc;
    iVar6 = 0;
    iVar5 = 0;
    do {
      iVar5 = (iVar5 + 1) - (uint)(((*ppuVar4)[*param_1] & 0x100) == 0);
      iVar6 = (iVar6 + 1) - (uint)(((*ppuVar4)[*param_1] & 0x200) == 0);
      param_1 = param_1 + 1;
    } while (pbVar1 != param_1);
    bVar2 = 1 < iVar5 && 1 < iVar6;
  }
  return bVar2;
```

In the first few lines we notice that the input needs to be 12 characters long.
The function then loops over each byte in the input, counting how many uppercase (`0x100`) and lowercase (`0x200`) characters it contains. It only validates the input if there are **more than two** uppercase and **more than two** lowercase alphabets.


#### Step 2: Running the binary

Now we try running the binary with a valid input.

```bash
sharon123@Ramkumar:/mnt/c/Users/sramk/downloads/challenge$ ./unlocker
Enter key: ASfgertfghwe
Passphrase: CYS{mirror_restored_but_soul_shattered} (1st flag obtained)
```

This gives us a passphrase.

#### Step 3: Running Steg analysis on the jpg attached

```bash
sharon123@Ramkumar:/mnt/c/Users/sramk/downloads/challenge$ steghide info mirror.jpg
"mirror.jpg":
  format: jpeg
  capacity: 564.0 Byte
Try to get information about embedded data ? (y/n) y
Enter passphrase: # enter the obtained passphrase
  embedded file "flag.txt":
    size: 29.0 Byte
    encrypted: rijndael-128, cbc
    compressed: yes
```

Extract the embedded file with steghide:

```bash
sharon123@Ramkumar:/mnt/c/Users/sramk/downloads/challenge$ steghide extract -sf mirror.jpg
Enter passphrase:
wrote extracted data to "flag.txt".

sharon123@Ramkumar:/mnt/c/Users/sramk/downloads/challenge$ cat flag.txt
CYS{r3fl3ct10n_r3st0r3d_B2A}
```

---

## Flags

- `CYS{mirror_restored_but_soul_shattered}` — (this flag keeps the player in the denier path, B)
- `CYS{r3fl3ct10n_r3st0r3d_B2A}` — (this flag makes the player shift from denier path B, to healer path, A)

