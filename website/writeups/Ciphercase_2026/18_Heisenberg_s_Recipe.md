---
layout: writeup

title: Heisenberg's Recipe
difficulty: Medium
points: 300
categories: [Crypto/Reverse Engineering]
tags: [LFSR, S-Box, Reverse Engineering, XOR]

flag: CYS{99.6_p3rc3nt_pur3_meth_lfsr_c4t4lyst}
---

# Heisenberg's Recipe

Author: CTF Team

This is a cryptography and reverse-engineering CTF challenge based around a corrupted reactor terminal. The player is given only the `README.txt` file and the compiled `reactor` executable. The objective is to reverse engineer the executable, recover the encryption algorithm, and decrypt the encrypted production yield.

## Challenge Setup

The `README.txt` provides the following important information:

- The reactor was initialized with `0x1337`.
- The terminal contains an encrypted production yield.
- The player is given the recovered `reactor` executable.

The supplied package does not contain the original C++ source or the decryption script, so the intended approach is to reverse engineer the executable.

## Reverse Engineering the Binary

First, inspect the executable using standard reverse-engineering tools such as:

- `strings`
- `objdump`
- Ghidra
- IDA
- Binary Ninja
- A debugger such as `gdb`

The binary prints the reactor state and the encrypted yield when executed.

The important runtime values are:

```text
REACTOR STATUS: RECOVERED
INITIAL STATE: 0x1337
ENCRYPTED YIELD: ac0b2aa6c79c07ec7bb50af1e65374e0c367420542e596921950a0a14ea7343736d8798f2bc5a45ab6
```

The binary also contains a reactor class with three important pieces of logic:

1. A 16-bit state transition.
2. A 256-byte substitution table.
3. A rolling 8-bit pressure value.

## 1. Recovering the State Transition

The reactor maintains a 16-bit state called `reactor_temp`.

The state transition is:

```text
bit = ((state >> 15) ^ (state >> 13) ^
       (state >> 12) ^ (state >> 10)) & 1

state = ((state << 1) & 0xffff) | bit
```

This is an LFSR-style operation.

Two state transitions are performed for every encrypted output byte:

```text
state = step(state)
state = step(state)
```

The initial state is:

```text
0x1337
```

Therefore, the state must be advanced twice before processing each ciphertext byte.

## 2. Recovering the Substitution Table

The binary initializes a 256-byte table using:

```text
S[i] = (151 * i + 73) mod 256
```

Since `151` is relatively prime to `256`, this creates a permutation of all 256 byte values.

Therefore, the inverse substitution table can be constructed:

```text
for i in range(256):
    S[i] = (151 * i + 73) % 256
    inverse_S[S[i]] = i
```

This inverse table is required because the encryption process applies the substitution in the forward direction.

## 3. Recovering the Rolling Pressure Value

The reactor starts with:

```text
pressure = 0x42
```

For every ciphertext byte, the pressure value is updated after the byte is processed.

The update equation recovered from the executable is:

```text
pressure = (pressure + ciphertext_byte ^
            (state & 0xff)) & 0xff
```

Because the pressure value depends on the previous ciphertext byte and the current reactor state, the decryption must be performed sequentially from the first byte to the last.

## 4. Reversing the Encryption

The encryption function can be represented as:

```text
diffuse_heat()
diffuse_heat()

thermal_layer = (reactor_temp >> 8) & 0xff

reacted = S[(raw_material ^ pressure) & 0xff]

yield_product = reacted ^ thermal_layer

pressure = (pressure + yield_product ^
            (reactor_temp & 0xff)) & 0xff
```

The ciphertext is `yield_product`.

To recover `raw_material`, reverse these operations in the opposite order.

First remove the thermal layer:

```text
mixed = ciphertext_byte ^ thermal_layer
```

Then apply the inverse S-box:

```text
raw_xor_pressure = inverse_S[mixed]
```

Finally remove the pressure value:

```text
raw_material = raw_xor_pressure ^ pressure
```

The recovered byte is then converted to a character.

## Decryption Procedure

The complete decryption process is:

```text
ciphertext = bytes.fromhex(encrypted_yield)

state = 0x1337
pressure = 0x42

for cipher_byte in ciphertext:

    state = lfsr_step(state)
    state = lfsr_step(state)

    thermal_layer = (state >> 8) & 0xff

    mixed = cipher_byte ^ thermal_layer

    raw_xor_pressure = inverse_S[mixed]

    raw_material = raw_xor_pressure ^ pressure

    output raw_material

    pressure = (pressure + cipher_byte ^
                (state & 0xff)) & 0xff
```

A Python solver implementing the recovered algorithm is:

```python
def gen_inverse_sbox():
    sbox = [(151 * i + 73) % 256 for i in range(256)]
    inv_sbox = [0] * 256

    for i, value in enumerate(sbox):
        inv_sbox[value] = i

    return inv_sbox


def lfsr_step(state):
    bit = ((state >> 15) ^ (state >> 13) ^
           (state >> 12) ^ (state >> 10)) & 1

    return ((state << 1) & 0xFFFF) | bit


def decrypt_batch(hex_cipher, initial_state):
    ciphertext = bytes.fromhex(hex_cipher)
    inverse_sbox = gen_inverse_sbox()

    state = initial_state & 0xFFFF
    pressure = 0x42
    plaintext = []

    for cipher_byte in ciphertext:
        state = lfsr_step(state)
        state = lfsr_step(state)

        thermal_layer = (state >> 8) & 0xFF

        mixed = cipher_byte ^ thermal_layer
        raw_xor_pressure = inverse_sbox[mixed]
        raw_material = raw_xor_pressure ^ pressure

        plaintext.append(chr(raw_material))

        pressure = (
            pressure + cipher_byte ^ (state & 0xFF)
        ) & 0xFF

    return "".join(plaintext)


encrypted = (
    "ac0b2aa6c79c07ec7bb50af1e65374e0c367420542e596921950a0a14"
    "ea7343736d8798f2bc5a45ab6"
)

print(decrypt_batch(encrypted, 0x1337))
```

## Flag

Running the recovered decryption algorithm produces:

```text
CYS{99.6_p3rc3nt_pur3_meth_lfsr_c4t4lyst}
```

Therefore, the flag is:

```text
CYS{99.6_p3rc3nt_pur3_meth_lfsr_c4t4lyst}
```

## Conclusion

The challenge combines reverse engineering with custom byte-level cryptography.

The key observations are:

- The initial 16-bit state is `0x1337`.
- The reactor uses an LFSR-style state transition.
- The state advances twice per ciphertext byte.
- A 256-byte affine S-box is generated using `(151 * i + 73) % 256`.
- The S-box must be inverted during decryption.
- An 8-bit rolling pressure value starts at `0x42`.
- The encrypted yield is reversed byte-by-byte using the recovered state, inverse S-box, and rolling pressure value.

Once these operations are reconstructed from the binary, the encrypted production yield can be completely decrypted and the flag recovered.
