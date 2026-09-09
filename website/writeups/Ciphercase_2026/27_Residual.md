---
layout: writeup

title: Residual
difficulty: Hard
points: 500
categories: [Reverse Engineering]
tags: [ELF, Ghidra, Linux, Self-Inspection]

flag: CYS{i_am_the_one_who_knocks}
---

Residual

Author: Manasa

This is a Breaking Bad-themed reverse-engineering CTF challenge involving a stripped Linux ELF binary, encoded runtime checks, a fake flag, self-inspection through `/proc/self/exe`, a custom `.x9` section, and a reversible byte transformation.

The goal is to satisfy the binary's filename, environment-variable, and command-line checks, analyze the generated dead drop, and recover the real flag.

## 1. What We Receive

The challenge gives us one executable:

```bash
memory
```

The flag format is:

```text
CYS{...}
```

The challenge story tells us that the binary came from an abandoned lab and that previous analysts recovered conflicting answers. That is our first warning: **the first flag we see may be a bad batch**.

---

## 2. Identify the File

Start with the normal first command for an unknown binary:

```bash
file memory
```

We should see something similar to:

```text
memory: ELF 64-bit LSB pie executable, x86-64, dynamically linked, stripped
```

This tells us that it is a 64-bit Linux ELF and that symbols have been stripped. In Ghidra, many functions will therefore appear with generic names such as `FUN_...` rather than useful original names.

If the executable bit was lost during download:

```bash
chmod +x memory
```

---

## 3. Run It Normally

Execute:

```bash
./memory
```

We get:

```text
The cook enters the lab...
Alias accepted.
The blue formula is missing a signal.
```

There are already two useful clues here.

`Alias accepted.` suggests that the program checks the name it is running under, while `missing a signal` suggests another external condition is required.

---

## 4. Check Printable Strings

Run:

```bash
strings memory | less
```

Search specifically for flag-shaped strings:

```bash
strings memory | grep 'CYS{'
```

We find:

```text
CYS{crystal_blue_is_too_obvious}
```

This is intentionally tempting, but it is a fake flag. The wording itself is a hint that an obvious blue crystal is not necessarily a clean batch.

Submitting it fails, so we need to reverse the executable rather than trust `strings`.

We can also check for obvious secrets:

```bash
strings memory | grep SIGNAL
strings memory | grep MIRROR
strings memory | grep -- '--listen'
```

The important values are not stored directly in plaintext.

---

## 5. Open the Binary in Ghidra

Start Ghidra:

```bash
ghidra
```

Then create a non-shared project and import `memory`:

```text
File → Import File → memory
```

Accept the detected ELF format, open the program, click **Yes** when Ghidra asks to analyze it, and keep the default analyzers enabled.

Because the file is stripped, focus on **what functions do**, not their names.

---

## 6. Start From `main`

Locate `main` and inspect the decompiled control flow.

Conceptually it performs several checks:

```text
print lab message
    ↓
check executable identity
    ↓
check environment
    ↓
check command-line argument
    ↓
produce dead drop
```

Work through those checks one at a time.

---

## 7. Recover the Expected Filename

The first validation routine uses `argv[0]`, which normally contains the path/name used to launch the program.

Inside that routine, an encoded byte array is transformed and compared against the basename of `argv[0]` using `strcmp()`.

Reversing the small transformation gives:

```text
memory
```

The supplied challenge file already has that name, which explains:

```text
Alias accepted.
```

We can prove the check exists:

```bash
cp memory test
chmod +x test
./test
```

Now the program says:

```text
The cook enters the lab...
This alias does not belong in the lab.
```

Remove the copy:

```bash
rm test
```

---

## 8. Investigate the Missing Signal

The next failed message is:

```text
The blue formula is missing a signal.
```

In Ghidra, follow the next validation function. It eventually calls:

```c
getenv()
```

That tells us the program expects an environment variable.

The variable name is reconstructed from encoded bytes. Reversing that decoder gives:

```text
SIGNAL
```

The returned value is compared against another reconstructed string:

```text
MIRROR
```

Therefore the required environment is:

```text
SIGNAL=MIRROR
```

Test it without permanently exporting anything:

```bash
SIGNAL=MIRROR ./memory
```

Now we get:

```text
The cook enters the lab...
Alias accepted.
Signal locked. The batch is getting cleaner.
You are not listening to the lab carefully enough.
```

So the environment check is solved.

---

## 9. Recover the Required Argument

Continue through `main` in Ghidra.

The next check operates on `argv[1]`. Another encoded array is transformed and compared against the argument.

Reversing the transformation gives:

```text
--listen
```

So the intended execution is:

```bash
SIGNAL=MIRROR ./memory --listen
```

Run it:

```text
The cook enters the lab...
Alias accepted.
Signal locked. The batch is getting cleaner.
Cook complete. Package the evidence.
Dead drop: b37a61397fc78d045c6a702fb50ddc0b029817065e948361683f165d
```

We have reached the correct execution path, but the dead drop is hexadecimal data rather than the flag.

---

## 10. Find the Dead-Drop Function in Ghidra

Search Ghidra for the string:

```text
Dead drop:
```

Use either the Defined Strings window or:

```text
Search → For Strings
```

Find `Dead drop:` and follow its **XREF**. An XREF tells us which function references that string.

That function builds several internal fragments, combines them, passes the result through a final byte transformation, and prints each transformed byte as two hexadecimal digits.

This is the function we need to understand.

---

## 11. Recover the First Flag Fragment

One small function contains these bytes:

```text
52 4b 40 6f
```

The decompiled loop is equivalent to:

```c
out[i] = data[i] ^ (0x11 + i);
```

Decode them:

```text
0x52 XOR 0x11 = 0x43 = C
0x4b XOR 0x12 = 0x59 = Y
0x40 XOR 0x13 = 0x53 = S
0x6f XOR 0x14 = 0x7b = {
```

So fragment 1 is:

```text
CYS{
```

That confirms we have found the real flag reconstruction path.

---

## 12. Recover the Second Fragment

Another function contains:

```text
6b 64 69 78 6d 85 7c 7c 79 8c 8e
```

The transformation is:

```c
out[i] = data[i] - ((i * 3) + 2);
```

Instead of doing all 11 bytes manually, reproduce it:

```bash
cat > part2.py <<'PY'
data = [
    0x6b, 0x64, 0x69, 0x78, 0x6d, 0x85,
    0x7c, 0x7c, 0x79, 0x8c, 0x8e
]

result = []
for i, value in enumerate(data):
    result.append(value - ((i * 3) + 2))

print(bytes(result).decode())
PY

python3 part2.py
```

Output:

```text
i_am_the_on
```

So far:

```text
CYS{i_am_the_on
```

---

## 13. Notice That the Third Fragment Depends on Something Else

The third fragment function contains:

```text
45 7e 51 4f 4b 7f 4a 48 48 47 4b 52 5b
```

But unlike the first two fragments, its key depends on the return value of another function.

Follow that function.

You will encounter imports such as:

```text
readlink
fopen
fread
fseek
```

The program is reading a file and parsing data from it.

---

## 14. Discover That the Binary Reads Itself

The path passed to `readlink()` is itself reconstructed from encoded bytes.

Decoding it gives:

```text
/proc/self/exe
```

On Linux, `/proc/self/exe` points to the currently running executable.

So the cook is literally inspecting its own recipe.

The program opens its own ELF file and begins parsing ELF structures.

---

## 15. Find the Custom ELF Section

The self-reading routine reads:

```text
ELF header
section headers
section-name string table
```

It reconstructs another short string and searches the section table for it.

That section name is:

```text
.x9
```

Confirm it from the terminal:

```bash
readelf -S memory | grep '\.x9'
```

Then dump the section:

```bash
readelf -x .x9 memory
```

The important 32 bytes are:

```text
91 2f c4 77 18 a3 5d e1
42 9b 06 d8 31 af 64 be
73 0c f1 55 28 99 b2 47
da 11 6e 83 3c f7 20 51
```

They are not text. They are input to a custom rolling mixer.

---

## 16. Reproduce the `.x9` Mixer

The relevant decompiled function behaves like:

```c
state = 0;
for each byte:
    state = (state * 33) ^ byte;
```

The state is one byte, so keep only the low 8 bits.

Create:

```bash
cat > x9.py <<'PY'
data = [
    0x91, 0x2f, 0xc4, 0x77, 0x18, 0xa3, 0x5d, 0xe1,
    0x42, 0x9b, 0x06, 0xd8, 0x31, 0xaf, 0x64, 0xbe,
    0x73, 0x0c, 0xf1, 0x55, 0x28, 0x99, 0xb2, 0x47,
    0xda, 0x11, 0x6e, 0x83, 0x3c, 0xf7, 0x20, 0x51
]

state = 0
for value in data:
    state = ((state * 33) ^ value) & 0xff

print("self key =", hex(state))
print("low nibble =", hex(state & 0x0f))
PY

python3 x9.py
```

Output:

```text
self key = 0xaa
low nibble = 0xa
```

Therefore:

```text
self_key = 0xAA
derived = 0x0A
```

---

## 17. Decode the Third Fragment

The decoder uses:

```text
key = (0x2A + (i % 5)) XOR derived
```

with:

```text
derived = 0x0A
```

Create:

```bash
cat > part3.py <<'PY'
data = [
    0x45, 0x7e, 0x51, 0x4f, 0x4b, 0x7f, 0x4a,
    0x48, 0x48, 0x47, 0x4b, 0x52, 0x5b
]

derived = 0x0a
base = 0x2a
result = []

for i, value in enumerate(data):
    key = (base + (i % 5)) ^ derived
    result.append(value ^ key)

print(bytes(result).decode())
PY

python3 part3.py
```

Output:

```text
e_who_knocks}
```

The internal message therefore becomes:

```text
CYS{i_am_the_one_who_knocks}
```

But the program does not print this plaintext. It passes it through one more transformation before producing the dead drop.

---

## 18. Understand the Final Transformation

The final routine uses the `.x9` key again:

```text
self_key = 0xAA
```

The seed is:

```text
seed = ((self_key XOR 0x63) + 7) & 0xFF
```

Calculate it:

```bash
python3 - <<'PY'
self_key = 0xaa
seed = ((self_key ^ 0x63) + 7) & 0xff
print(hex(seed))
PY
```

Output:

```text
0xd0
```

For each plaintext byte at index `i`, the binary then performs:

```text
1. XOR with seed + (i * 5)
2. rotate left by 3 bits
3. add (i XOR 0x17)
```

Encoding direction:

```text
plaintext → XOR → ROL 3 → addition → dead-drop byte
```

To recover the plaintext, reverse the order:

```text
dead-drop byte → subtraction → ROR 3 → XOR → plaintext
```

---

## 19. Write the Final Solver

Use the dead drop printed by the program:

```text
b37a61397fc78d045c6a702fb50ddc0b029817065e948361683f165d
```

Create:

```bash
cat > solve.py <<'PY'
transmission = "b37a61397fc78d045c6a702fb50ddc0b029817065e948361683f165d"

data = bytes.fromhex(transmission)
self_key = 0xaa
seed = ((self_key ^ 0x63) + 7) & 0xff


def ror8(value, bits):
    return ((value >> bits) | (value << (8 - bits))) & 0xff


result = []

for i, value in enumerate(data):
    value = (value - (i ^ 0x17)) & 0xff
    value = ror8(value, 3)
    value ^= (seed + (i * 5)) & 0xff
    result.append(value)

print(bytes(result).decode())
PY

python3 solve.py
```

Output:

```text
CYS{i_am_the_one_who_knocks}
```

---

# Final Flag

```text
CYS{i_am_the_one_who_knocks}
```

---

## Full Intended Solve Flow

```text
memory
  ↓
file / strings
  ↓
CYS{crystal_blue_is_too_obvious}  ← fake batch
  ↓
Ghidra
  ↓
argv[0] → memory
  ↓
getenv() → SIGNAL=MIRROR
  ↓
argv[1] → --listen
  ↓
SIGNAL=MIRROR ./memory --listen
  ↓
Dead drop: b37a...
  ↓
follow Dead drop XREF
  ↓
self-reading through /proc/self/exe
  ↓
ELF section .x9
  ↓
rolling mixer → 0xAA
  ↓
reverse final byte transformation
  ↓
CYS{i_am_the_one_who_knocks}
```

The challenge is designed so both static and dynamic approaches are valid. A strong reverser can reproduce every deterministic value without relying on hidden server-side secrets.
