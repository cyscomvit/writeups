---
layout: writeup

title: Tio's Bell
difficulty: Hard
points: 500
categories: [Reverse Engineering]
tags: []

flag: CYS{ekrfcozsmqktfpbmtcyq}
---

# Tio's Bell

Author: Sagnik

This challenge provides a Linux x86-64 ELF binary which appears to be a laboratory monitoring program.

The binary contains several chemistry-themed functions, a custom decoder, a state machine, and a final flag-generation routine. The intended solve is to reverse engineer the important execution path rather than simply searching the binary for the flag.

The overall solve path is:

```text
ELF
 ↓
main
 ↓
dispatcher
 ↓
crystallize()
 ↓
custom decoder
 ↓
hidden clue
 ↓
bell/state-machine sequence
 ↓
target resolution
 ↓
FNV-1a
 ↓
LCG + XOR
 ↓
FLAG
```

## Firstly, identify the binary

Run:

```bash
file lab_monitor
```

The binary is a Linux x86-64 ELF.

It is useful to inspect its strings as well:

```bash
strings -a lab_monitor
```

There are several laboratory-themed messages and diagnostic strings.

The binary also contains the flag format:

```text
{% raw %}CYS{%s}{% endraw %}
```

but the actual flag is generated at runtime.

## Find the main function

Open the binary in Ghidra and follow the ELF entry point until the call to `__libc_start_main`.

This leads to `main`.

The main function initializes the program state and then passes it through a dispatcher which calls several themed stages.

The interesting stages include functions associated with:

```text
purity
temperature
yield
crystallize
sensor
```

Most of the early logic is useful mainly for reconstructing the intended execution path.

## Follow the crystallize stage

The interesting function is the `crystallize()` stage.

It processes a 50-byte encoded blob using a 16-byte substitution table.

The binary contains the following table:

```text
13 5a 27 41 0d 6e 32 19
55 08 3c 72 24 4f 11 38
```

and a 50-byte encoded blob.

The function also maintains a rolling 32-bit state.

## Identify the LCG

The state update is:

```c
state = state * 0x19660D + 0x3C6EF35F;
```

with 32-bit wrapping.

The initial state is:

```text
737
```

This is a Linear Congruential Generator.

For every byte, the program advances the state and uses the high byte of the result as part of the decoder.

## Reverse the byte transformation

The Ghidra output contains a position-dependent rotation:

```text
(i % 5) + 3
```

The operation:

```c
x >> rotation | x << (8 - rotation)
```

is an 8-bit right rotation.

The decoder can therefore be reproduced conceptually as:

```python
state = 737

for i in range(50):
    state = (state * 0x19660D + 0x3C6EF35F) & 0xffffffff

    x = SUB_TABLE[i & 0xf] + ENC[i]
    x &= 0xff

    x ^= state >> 24

    x = ror8(x, (i % 5) + 3)

    plaintext[i] = x
```

Decoding the blob gives:

```text
IMMOBILE ELDER / PRIVATE RESIDENCE / SIGNAL DEVICE
```

This is the first major clue.

## Interpret the clue

The decoded text describes:

```text
IMMOBILE ELDER
PRIVATE RESIDENCE
SIGNAL DEVICE
```

This points toward Hector Salamanca from *Breaking Bad*, who is an elderly, largely immobile character associated with a bell used as his communication device.

The bell reference is important because it leads into the next stage of the binary.

## Reverse the sensor state machine

The next interesting function implements a state machine.

The expected sequence is embedded as:

```text
02 02 05 02 02
```

Therefore the required signal sequence is:

```text
2 2 5 2 2
```

Following the state transitions shows that successfully processing this sequence reaches:

```text
trigger_state = 6
trigger_ok = 1
```

This confirms that the bell clue is connected to the intended execution path.

## Resolve the target

The next stage checks that the clue and sensor state are valid.

It then evaluates the candidate records stored in the binary.

The matching candidate produces:

```text
target_id = 0x6d
```

or:

```text
109
```

in decimal.

This value is later mixed into the final flag-generation seed.

## Identify FNV-1a

The final flag-generation routine hashes the recovered clue.

The hash function starts with:

```text
0x811C9DC5
```

and multiplies by:

```text
0x01000193
```

after XORing each input byte.

These are the standard constants for FNV-1a.

The equivalent Python function is:

```python
def fnv1a(data):
    h = 0x811C9DC5

    for byte in data:
        h ^= byte
        h = (h * 0x01000193) & 0xffffffff

    return h
```

For:

```text
IMMOBILE ELDER / PRIVATE RESIDENCE / SIGNAL DEVICE
```

the resulting hash is:

```text
0x95516be4
```

## Construct the final seed

The program mixes the clue hash with the recovered target ID and trigger state:

```text
seed =
    clue_hash
    XOR target_id
    XOR trigger_state * 0x45D9F3B
    XOR 0x224BB268
```

This can be reproduced with:

```python
seed = (
    clue_hash
    ^ 0x6D
    ^ ((6 * 0x45D9F3B) & 0xffffffff)
    ^ 0x224BB268
) & 0xffffffff
```

This produces the initial state used by the final flag generator.

## Generate the flag

The program uses the same LCG:

```text
state = state * 0x19660D + 0x3C6EF35F
```

For each of 20 characters it:

1. advances the LCG;
2. takes the high byte;
3. rotates it;
4. XORs it with the 16-byte substitution table;
5. reduces the result modulo 26;
6. converts it into a lowercase letter.

The rotation is:

```text
(i % 5) + 3
```

The equivalent generation logic is:

```python
result = []

for i in range(20):
    seed = (
        seed * 0x19660D
        + 0x3C6EF35F
    ) & 0xffffffff

    byte = (seed >> 24) & 0xff

    rotation = (i % 5) + 3

    byte = rol8(byte, rotation)

    byte ^= SUB_TABLE[i & 0xf]

    result.append(
        chr(ord('a') + (byte % 26))
    )

flag = "CYS{" + "".join(result) + "}"
```

This produces:

```text
CYS{ekrfcozsmqktfpbmtcyq}
```

## Complete solve chain

```text
                     lab_monitor
                          |
                          v
                         main
                          |
                          v
                     dispatcher
                          |
                          v
                     crystallize
                          |
              +-----------+-----------+
              |                       |
        16-byte table            50-byte blob
              |                       |
              +-----------+-----------+
                          |
                          v
                      LCG decoder
                          |
                          v
       IMMOBILE ELDER / PRIVATE RESIDENCE /
                  SIGNAL DEVICE
                          |
                          v
                 sensor state machine
                          |
                          v
                      2 2 5 2 2
                          |
                          v
                     state = 6
                          |
                          v
                   target = 0x6d
                          |
                          v
                       FNV-1a
                          |
                          v
                 seed construction
                          |
                          v
                        LCG
                          |
                          v
                     ROL + XOR
                          |
                          v
                        % 26
                          |
                          v
                         FLAG
```

## Final Flag

```text
CYS{ekrfcozsmqktfpbmtcyq}
```
