---
layout: writeup

title: HOLA AMIGOS
difficulty: Hard
points: 500
categories: [Reverse Engineering]
tags: []

flag: CYS{you_godamn_wright!}
---

HOLA AMIGOS

Author : Anirudh

## Challenge Overview


The program asks for two values:

```text
Enter shipment ID:
Enter batch number:
```

The objective is to reverse engineer the executable, determine the correct inputs, and recover the flag.

The correct values are:

```text
Shipment ID: 67
Batch Number: 40
```

The final flag is:

```text
CYS{you_godamn_wright!}
```

---

## 1. Initial Reconnaissance

Open `hola_amigos.exe` in **Ghidra**.

Create a new project, import the executable, and allow Ghidra to perform its default analysis.

Open:

**Window -> Defined Strings**

You will find only a few useful strings:

```text
HOLA AMIGOS
SECURE SYSTEM
Enter shipment ID:
Enter batch number:
STATUS: 1
STATUS: 0
```

There is no plaintext flag.

This means searching for `CYS{` will not immediately reveal anything.

---

## 2. Start at `main()`

Open the `main` function in the decompiler.

The program reads two integers:

```cpp
int shipmentID;
int batchNumber;
```

These values are passed through several functions.

Because the binary has been stripped of useful symbols, Ghidra may give the functions generic names such as:

```text
FUN_140001230
FUN_140001410
FUN_1400016A0
```

Rename them as you understand their purpose. This makes following the program much easier.

The important data flow is:

```text
Shipment ID
     |
     v
First transformation
     |
     v
Second transformation
     |
     v
Third transformation
     |
     v
Result
     |
     v
Comparison with target
```

There is also a decoy calculation which does not affect the final result.

---

## 3. Find the First Mathematical Function

Follow the function that receives the shipment ID and batch number.

After simplifying some of the encoded constants, you will find:

```cpp
x = shipmentID - 12;
y = batchNumber - 45;
```

The next calculation looks more complicated:

```cpp
p = (x + y) * (x + y);
q = (x - y) * (x - y);

distance = (p + q) >> 1;
```

The important observation is:

```text
((x + y)^2 + (x - y)^2) / 2
```

Expanding this:

```text
(x + y)^2 = x^2 + 2xy + y^2

(x - y)^2 = x^2 - 2xy + y^2
```

Adding them:

```text
2x^2 + 2y^2
```

Dividing by 2:

```text
x^2 + y^2
```

Therefore the first stage is equivalent to:

```text
d = (shipmentID - 12)^2 + (batchNumber - 45)^2
```

This is the first important mathematical observation.

---

## 4. Reverse the Second Stage

Follow the value returned from the first function.

The next function performs:

```text
z = (7 * d^2 + 13 * d + 97) % 10007
```

So the pipeline is now:

```text
Shipment ID + Batch Number
            |
            v
            d
            |
            v
            z
```

---

## 5. Reverse the Third Stage

The next function performs:

```text
k = (z^3 + 17*z^2 + 43*z + 7) % 65537
```

It then performs an XOR operation:

```text
result = k XOR 0x5A17
```

Therefore the complete transformation is:

```text
d
 |
 v
z = (7*d^2 + 13*d + 97) % 10007
 |
 v
k = (z^3 + 17*z^2 + 43*z + 7) % 65537
 |
 v
result = k XOR 0x5A17
```

---

## 6. Find the Target Value

Return to `main()` and inspect the comparison:

```cpp
if (result == target)
```

Follow the function responsible for generating `target`.

Instead of storing the target directly, the binary constructs it from several constants.

After simplifying the operations, the target calculation becomes:

```text
x = 0x91C3 XOR 0x4A27
x = x + 0x1234
target = x XOR 0x1B58
```

Calculate the first operation:

```text
0x91C3 XOR 0x4A27 = 0xDBE4
```

Then:

```text
0xDBE4 + 0x1234 = 0xEE18
```

Finally:

```text
0xEE18 XOR 0x1B58 = 0xF540
```

Therefore:

```text
Target = 0xF540
```

The mathematical pipeline must produce `0xF540`.

---

## 7. Solve for the Inputs

We now have the important equation:

```text
d = (shipmentID - 12)^2 + (batchNumber - 45)^2
```

The intended solution is:

```text
shipmentID = 67
batchNumber = 40
```

Substitute these values:

```text
d = (67 - 12)^2 + (40 - 45)^2
```

```text
d = 55^2 + (-5)^2
```

```text
d = 3025 + 25
```

Therefore:

```text
d = 3050
```

Now calculate the next stage:

```text
z = (7 * 3050^2 + 13 * 3050 + 97) % 10007
```

This gives:

```text
z = 1670
```

Next:

```text
k = (1670^3 + 17 * 1670^2 + 43 * 1670 + 7) % 65537
```

giving:

```text
k = 44887
```

Finally:

```text
44887 XOR 0x5A17 = 0xF540
```

This matches the target recovered from the binary.

Therefore:

```text
Shipment ID  = 67
Batch Number = 40
```

---

## 8. Follow the Successful Branch

Now inspect what happens when:

```cpp
result == target
```

is true.

The program calls another function which contains an array of seemingly random bytes.

There is no readable flag stored in the array.

This is the final stage of the challenge.

---

## 9. Reverse the Flag Key

Inside the flag-processing function, look at how the decryption key is generated.

The relevant logic is equivalent to:

```text
key = (d & 255) XOR (z >> 4) XOR (result >> 8) XOR 0xA7
```

For the correct values:

```text
d      = 3050
z      = 1670
result = 0xF540
```

Calculate:

```text
3050 & 255 = 0xEA
```

```text
1670 >> 4 = 0x68
```

```text
0xF540 >> 8 = 0xF5
```

Therefore:

```text
key = 0xEA XOR 0x68 XOR 0xF5 XOR 0xA7
```

which gives:

```text
key = 0xD0
```

---

## 10. Decrypt the Flag

The program XORs every byte in the encrypted array with `0xD0`.

Conceptually:

```cpp
for each byte:
    plaintext = encrypted_byte XOR 0xD0;
```

Doing this reveals:

```text
CYS{you_godamn_wright!}
```

The plaintext flag is therefore never stored directly in the executable.

---

## 11. Verify the Solution

Run the executable and enter:

```text
Enter shipment ID: 67
Enter batch number: 40
```

The program reaches the successful branch and decrypts the embedded message.

Final flag:

```text
CYS{you_godamn_wright!}
```

---

## 12. Ghidra Workflow Summary

The intended solving process is:

```text
Import EXE
    |
    v
Run Ghidra analysis
    |
    v
Open main()
    |
    v
Trace Shipment ID + Batch Number
    |
    v
Follow the mathematical functions
    |
    v
Recognize the disguised distance calculation
    |
    v
Recover d -> z -> k -> result
    |
    v
Find target reconstruction
    |
    v
Recover target = 0xF540
    |
    v
Solve for Shipment ID = 67
Batch Number = 40
    |
    v
Follow successful branch
    |
    v
Find encrypted byte array
    |
    v
Reverse key generation
    |
    v
Recover key = 0xD0
    |
    v
XOR encrypted bytes
    |
    v
CYS{you_godamn_wright!}
```

## Final Solution

**Shipment ID:** `67`

**Batch Number:** `40`

**Flag:**

```text
CYS{you_godamn_wright!}
```
