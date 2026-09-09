---
layout: writeup

title: The Evidence
difficulty: Medium
points: 300
categories: [Steganography/Forensics,Cryptography]

flag: CYS{BlU3_G0ld3n_C4sh}
---
The Evidence

Author: Hait Patel

This is a steganography, forensics, and cryptography-based CTF challenge in which the flag is divided into two halves, F₁ and F₂. Both halves are protected using visual steganography, metadata pivot links, Word container structures, and custom PNG file chunks.

All true payload data and keys are hidden in the **Bit 0 channel (LSB)** across the primary color planes. Multiple decoy flags and trap keys exist across other bit planes to mislead automated tools and superficial visual inspection.

For the Tools Used:

* StegSolve (or `zsteg` on Linux)
* `exiftool`
* CyberChef
* A zip/archive utility

For Step 1 — Extract Key 1 and Decrypt Flag Part 1 (F₁):

**Files provided:** `RV_challenge.png`, `Lab_challenge.png`

For Recovering Key 1:

1. Open `RV_challenge.png` in StegSolve (or inspect via `zsteg` on Linux).
2. Cycle through the bit planes to **Red Plane 0 (R0)** to extract the plaintext key:

```text
METH_LAB_RED_KEY
```

For Extracting the Encrypted F₁ Payload:

1. Open `Lab_challenge.png` in StegSolve.
2. Navigate to **Analyse → Data Extract**.
3. Select **Blue 0 (B0)** (MSB first, Row order) and copy the extracted hex stream:

```text
0E 1C 07 33 1D 20 14 71 00 15 75
```

For Decrypting Part 1 in CyberChef:

Recipe:

1. `From Hex` (Delimiter: Auto)
2. `XOR` (Key: `METH_LAB_RED_KEY`, Type: `UTF8`, Scheme: `Standard`) → yields `CYS{BlU3_G0`

**Output (F₁):**

```text
CYS{BlU3_G0
```

For Step 2 — Locate the Word File via Metadata:

Inspect the metadata of `RV_challenge.png`:

```bash
exiftool RV_challenge.png
```

The metadata contains a link pointing to an external Word document, `challenge.docx`. Download this file.

For Step 3 — Extract the Nested Document Media & Folder Links:

Microsoft Word's UI strips ancillary PNG chunks and metadata when using "Save as Picture," so the raw media must be unpacked directly from the `.docx` archive.

1. Rename `challenge.docx` → `challenge.zip`.
2. Unzip the file and navigate to the media folder:

```text
challenge.zip/word/media/
```

3. Run `exiftool` on the second image (`image2.png`):

```bash
exiftool -Description -Comment image2.png
```

4. This reveals two separate links:

   * **Description** field → link to **Folder A** (holds the file containing the encrypted F₂ payload)
   * **Comment** field → link to **Folder B** (holds the file containing Key 2)
5. Download both files from their respective folders.

For Step 4 — Carve Embedded Files Using CyberChef:

Both downloaded files contain nested PNG structures injected into custom ancillary chunks.

1. Open CyberChef.
2. Drag and drop the file downloaded from **Folder A** into the Input panel.
3. Apply the **Extract Files** operation.
4. Save the carved inner image file: `flaghere_carved.png`.
5. Repeat the exact same steps for the file downloaded from **Folder B** to carve the key image file: `key_carved.png`.

For Step 5 — Extract Key 2 and Encrypted Flag Part 2 (F₂):

For Extracting Encrypted F₂:

1. Open `flaghere_carved.png` in StegSolve → **Analyse → Data Extract**.
2. Select **Blue 0 (B0)** (MSB, Row order) and scroll to the top of the output preview:

```text
ENC_F2_HEX: 2F 74 05 32 3D 3F 6C 14 1C 7B 03 5C 39 1A 0E 64
```

For Extracting Key 2:

1. Open `key_carved.png` in StegSolve → **Analyse → Data Extract**.
2. Select **Blue 0 (B0)** and scroll to the top of the output preview:

```text
REAL_KEY: M3TH_SUPR3M3_K3Y
```

For Step 6 — Decrypt Flag Part 2 (F₂) & Reassemble Flag:

**Input:**

```text
2F 74 05 32 3D 3F 6C 14 1C 7B 03 5C 39 1A 0E 64
```

**Recipe:**

1. `From Hex` (Delimiter: Auto)
2. `XOR` (Key: `M3TH_SUPR3M3_K3Y`, Type: `UTF8`, Scheme: `Standard`) → yields `bGQzbl9DNHNofQ==`
3. `From Base64`

**Output (F₂):**

```text
ld3n_C4sh}
```

For the Final Reassembly:

```text
F1 + F2 = CYS{BlU3_G0 + ld3n_C4sh} = CYS{BlU3_G0ld3n_C4sh}
```

For the Final Flag:

```text
CYS{BlU3_G0ld3n_C4sh}
```
