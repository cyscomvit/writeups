---
layout: writeup

title: Corelight Museum Archive
difficulty: Hard
points: 500
categories: [Reverse Engineering / Steganography/ Cryptography]
tags: []

flag: CYS{restoration_record_0217}
---

# Corelight Museum Archive

Author: Sagnik

This challenge is a combination of steganography, PNG file analysis, reverse engineering, and cryptography.

We are given a single PNG image which appears to be an old archival photograph. The image contains multiple independent artifacts. We need to recover three clues from the image, find the encrypted payload hidden in the PNG, and then reverse engineer an appended executable to understand how the clues are turned into the encryption key.

The overall solve path is:

```text
PNG Image
   |
   +--> Metadata
   |
   +--> LSB steganography
   |
   +--> Visual clue
   |
   +--> Custom PNG chunk
   |
   +--> Appended ELF
             |
             v
      Reverse engineering
             |
             v
       FNV-1a key derivation
             |
             v
          ChaCha20
             |
             v
            FLAG
```

## Firstly, inspect the image metadata

The challenge description says:

> "As with every restoration, begin by identifying the creator."

This strongly suggests checking the image metadata.

We can use:

```bash
exiftool archive.png
```

Among the PNG metadata, the `Artist` field contains:

```text
see_hidden_notes
```

This is not a normal artist name and is clearly intended as a clue.

So our first recovered value is:

```text
EXIF = see_hidden_notes
```

The metadata is therefore one of the inputs to the later key derivation.

## Next, inspect the image for hidden data

The image also contains information hidden using LSB steganography.

A tool such as `zsteg` can be used to inspect the different bit planes:

```bash
zsteg archive.png
```

The relevant information is hidden in the least significant bits of the image.

Extracting the embedded message gives:

```text
beyond_last_pixel
```

Therefore our second clue is:

```text
LSB = beyond_last_pixel
```

The important point is that this message is not visible when the PNG is simply opened normally.

## Inspect the photograph itself

The challenge description also says that the archive is self-contained and that we should begin by identifying the creator. After checking the metadata and hidden data, we should also inspect the photograph itself.

A visual reference is present in the image:

```text
REF-0217
```

This gives us the third clue:

```text
VIS = REF-0217
```

At this point we have:

```text
EXIF = see_hidden_notes
LSB  = beyond_last_pixel
VIS  = REF-0217
```

However, we still need to determine how these values are used.

## Inspect the PNG structure

A PNG consists of a sequence of chunks, so we should inspect the actual file structure rather than treating it only as an image.

Using:

```bash
pngcheck -v archive.png
```

reveals an unusual custom chunk:

```text
chunk coRe at offset 0x382464, length 29
    unknown private, ancillary, safe-to-copy chunk
```

The `coRe` chunk is suspicious because it is not one of the normal PNG chunks.

A PNG chunk has the structure:

```text
Length  4 bytes
Type    4 bytes
Data    N bytes
CRC     4 bytes
```

The reported offset points to the beginning of the length field. Therefore, the actual chunk data begins 8 bytes after the reported offset.

The chunk contains 29 bytes of data, which is the encrypted payload.

We can extract it with:

```bash
dd if=archive.png of=core.bin bs=1 skip=3679340 count=29
```

Then inspect the result:

```bash
xxd core.bin
```

The output is binary data and does not resemble plaintext.

This tells us that we still need to recover the encryption method and key.

## Check for data after the PNG

`pngcheck` also reports:

```text
additional data after IEND chunk
```

This is another important clue.

A valid PNG normally ends at its `IEND` chunk. If there is additional data after `IEND`, something else has been appended to the file.

We can use:

```bash
binwalk archive.png
```

This identifies an ELF executable after the PNG.

The ELF begins at:

```text
3679381
```

We can extract it using:

```bash
dd if=archive.png of=archive_encoder bs=1 skip=3679381
```

Then verify it:

```bash
file archive_encoder
```

It is a Linux x86-64 ELF executable.

Make it executable if desired:

```bash
chmod +x archive_encoder
```

The appended executable is effectively the missing restoration software referenced by the challenge.

## Reverse engineer the executable

We can load `archive_encoder` into Ghidra.

We can also start with:

```bash
strings -a archive_encoder
```

Some useful strings include:

```text
Corelight Restoration Encoder
[record] assembling capture record from scene-tag, hidden-note, visual-ref
[record] record layout: EXIF:<scene-tag>|LSB:<hidden-note>|VIS:<visual-ref>
[signature] deriving archive signature from capture record
[transform] preparing archive transform state
[protect] applying payload protection
```

The most important string is:

```text
EXIF:<scene-tag>|LSB:<hidden-note>|VIS:<visual-ref>
```

This tells us exactly how the three clues are combined.

Using the values recovered earlier, the record becomes:

```text
EXIF:see_hidden_notes|LSB:beyond_last_pixel|VIS:REF-0217
```

The order and separators are important.

## Identify the hash function

The encoder contains a function that initializes a 32-bit value with:

```text
0x811C9DC5
```

and repeatedly XORs each byte before multiplying by:

```text
0x01000193
```

These are the standard constants for FNV-1a.

The equivalent Python implementation is:

```python
def fnv1a32(data):
    h = 0x811C9DC5

    for b in data:
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF

    return h
```

The first hash is therefore:

```text
H1 = FNV-1a32(
    "EXIF:see_hidden_notes|LSB:beyond_last_pixel|VIS:REF-0217"
)
```

The encoder then hashes three calibration strings:

```text
CHUNK_A
CHUNK_B
CHUNK_C
```

and chains them with XOR:

```text
H1 = FNV1a32(record)

H2 = FNV1a32("CHUNK_A") XOR H1

H3 = FNV1a32("CHUNK_B") XOR H2

H4 = FNV1a32("CHUNK_C") XOR H3
```

These four 32-bit values form the archive signature.

## Expand the signature into the key

The executable then expands the four 32-bit signature values into a 32-byte key.

The relevant logic is equivalent to:

```c
for (int i = 0; i < 8; i++) {
    uint32_t shift = (i % 4) * 8;

    key[i]      = (sig[0] >> shift) & 0xff;
    key[i + 8]  = (sig[1] >> shift) & 0xff;
    key[i + 16] = (sig[2] >> shift) & 0xff;
    key[i + 24] = (sig[3] >> shift) & 0xff;
}
```

So each signature value contributes eight bytes to the final key, with its four little-endian bytes repeated twice.

The resulting key can be reproduced from the four signature values rather than guessed.

## Identify the encryption algorithm

The executable contains a custom implementation of ChaCha20.

The initialization constants are:

```text
0x61707865
0x3320646e
0x79622d32
0x6b206574
```

These correspond to:

```text
expand 32-byte k
```

which is the standard ChaCha20 constant.

The quarter-round also uses the standard ChaCha20 rotations:

```text
16
12
8
7
```

Therefore the payload is protected using:

```text
ChaCha20
```

The parameters recovered from the executable are:

```text
Cipher:  ChaCha20
Nonce:   000000000000000000000000
Counter: 1
```

The nonce is 12 zero bytes and the initial counter is 1.

## Decrypt the `coRe` payload

We now have everything needed:

```text
EXIF clue
    +
LSB clue
    +
visual reference
    |
    v
capture record
    |
    v
FNV-1a + chained XOR
    |
    v
32-byte key
    |
    v
ChaCha20
    |
    v
coRe ciphertext
    |
    v
plaintext
```

The repository also contains a decryption script that reproduces the recovered algorithm.

The important part is:

```python
key = derive_key()

cipher = ChaCha20.new(
    key=key,
    nonce=b"\x00" * 12
)

cipher.seek(64)

plaintext = cipher.decrypt(ciphertext)
```

The `seek(64)` advances to counter 1 because one ChaCha20 block is 64 bytes.

Running the decryption produces:

```text
CYS{restoration_record_0217}
```

## Complete solve chain

```text
                         archive.png
                              |
              +---------------+---------------+
              |               |               |
              v               v               v
           EXIF            RGB LSB        Photograph
              |               |               |
              v               v               v
   see_hidden_notes   beyond_last_pixel     REF-0217
              |               |               |
              +---------------+---------------+
                              |
                              v
       EXIF:see_hidden_notes|LSB:beyond_last_pixel|VIS:REF-0217
                              |
                              v
                           FNV-1a
                              |
                              v
                    CHUNK_A / CHUNK_B / CHUNK_C
                              |
                              v
                       4 x 32-bit values
                              |
                              v
                         32-byte key
                              |
                              v
                          ChaCha20
                              |
                              v
                     coRe encrypted chunk
                              |
                              v
                             FLAG
```

There is also a second important path through the file:

```text
archive.png
    |
    +--> PNG image
    |
    +--> coRe chunk
    |       |
    |       +--> encrypted payload
    |
    +--> IEND
    |
    +--> appended ELF
            |
            +--> key derivation
            +--> cipher implementation
```

The PNG provides the clues and ciphertext, while the appended executable provides the algorithm required to turn those clues into the decryption key.

## Final Flag

```text
CYS{restoration_record_0217}
```
