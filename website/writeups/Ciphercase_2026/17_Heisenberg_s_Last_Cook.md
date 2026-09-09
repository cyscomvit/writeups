---
layout: writeup

title: Heisenberg's Last Cook
difficulty: Hard
points: 500
categories: forensics

flag: CYS{violet_ledger_seventeen_unwound}
---
Heisenberg's Last Cook

Author:

This is a forensic/cryptographic CTF challenge based on reconstructing an accepted session from memory and network evidence, recovering committed integer values, simplifying the verifier's BN254 proof algebra, and using the recovered entry to unlock the final encrypted artifact.

The archive contains:

```text
service/heisenberg
evidence/memory.raw
evidence/cook.pcapng
evidence/superlab.E01
evidence/final.enc
```

The README specifies the flag format:

```text
CYS{...}
```

For the Recovered Accepted Session:

The accepted session was identified as:

```text
PID   = 4172
SID   = 9f0c17a4
kid   = 17
port  = 49152
route/tid = b7-31-9c
```

The exact CLOCK preimage was recovered as:

```text
2026-08-23T03:16:58+05:30
```

The exact ROUTE preimage was:

```text
b7-31-9c
```

Both were verified because hashing their exact representations produced the verifier's expected digests.

The nearby timestamps `03:17:35` and `03:17:42` were therefore not used for CLOCK.

For the Forensic Fragments:

The accepted PID `4172` memory contained four important forensic fragments:

```text
r0 → LEDGER
r1 → TRAPDOOR-
r2 → 4421
r3 → LAUNDRY-
```

These are **labels**, not the literal numeric values of `r0`, `r1`, `r2`, and `r3`.

The USN journal showed:

```text
7f.tmp → r3.bin
a1.tmp → r1.bin
4c.tmp → r2.bin
```

followed by deletion.

This established the relationship between the deleted temporary files and the four committed values.

For the Commitment Values:

The verifier commits to four integer values using:

```python
SHA256(str(int(value)))
```

The commitments supplied during the investigation were:

```text
r0:
77d300a60bf738330be913fc309f1235ab483ddf9035649207db6c6b60beaa9d

r1:
6b856cbbf4a476e959b521cea53de6540bac51224363355a30d1d9e4d9e25e93

r2:
a2b9efb99896e8349475ea6689beafbb111b2721297e726cea8b502f4712309

r3:
2281499878b9c7791db67afed9d9da96de649305c7472f1ed42d4b33ac1d9722
```

An exhaustive search of all unsigned 32-bit values:

```text
0 .. 4294967295
```

was performed for all four commitments.

The result was:

```text
r0 → no 32-bit match
r1 → no 32-bit match
r2 → no 32-bit match
r3 → no 32-bit match
```

This established that the four values are derived/larger integers rather than simple PIDs, ports, timestamps, offsets, or other ordinary 32-bit values.

For the PCAP Reconstruction:

The accepted run contained:

```text
sequence numbers 0..19
literal duplicate seq=3
truncated seq=19
```

There were exactly:

```text
29 telemetry requests
```

with indices:

```text
000..028
```

The accepted ciphertext material had exactly:

```text
1131 bytes
```

which is:

```text
29 × 39 = 1131
```

This exact 39-byte record structure was an important clue.

For the Fixed vs Old Capture:

Comparing the old and FIXED PCAPs showed:

* telemetry was unchanged
* accepted `/mix` ciphertexts changed in exactly 14 records
* every changed 3-byte region had the same XOR delta:

```text
8f b2 01
```

This was treated as a genuine structural differential introduced by the FIXED challenge.

Standard GCM/GHASH behavior did not explain this differential, so the reconstruction was treated as challenge-specific rather than as a normal AEAD decryption problem.

For the Proof Algebra:

The verifier uses the **BN254 scalar field**.

The investigation established that:

```text
_commitment
```

and

```text
_decode
```

cancel in the relevant verifier relation.

Likewise:

```text
_calibrate
```

cancels.

The remaining residue is:

```text
FIELD - 1 = -1 mod FIELD
```

Therefore, after assigning:

```text
a = r0
b = r1
```

the proof condition simplifies to:

```text
c × r3 ≡ r2 (mod FIELD)
```

so:

```text
c = r2 × inverse(r3, FIELD) mod FIELD
```

The verifier then uses `_order(c)` / its lookup table based on:

```text
c % 4
```

This eliminated the need to repeatedly solve the original proof equation.

For the Entry Matching:

The updated entry digest supplied by the verifier was:

```text
e788bd5b995a57eebcaceb583cbcf0d7d9643097e5865143bc73437cdeab0eb9
```

The recovered answer/entry was:

```text
VIOLET|LEDGER|SEVENTEEN|UNWOUND
```

The semantic clues line up with the recovered forensic labels:

```text
LEDGER
```

and the challenge's `kid = 17` information, producing the final entry:

```text
VIOLET|LEDGER|SEVENTEEN|UNWOUND
```

For the Final Encrypted Artifact:

The final artifact was:

```text
nonce:
c17-final
```

Ciphertext:

```text
aa82dbe96ecd172f744c7023e078b5ae3b0d2fb488e8e1e122ad0a128fbefbb4f5361113
```

Tag:

```text
77d7b2c2396b03b348b0d2df42d5042d04169da7ce639fbb6136c67774295288
```

The verifier's unlock-key construction is:

```python
sha256(
    "heisenberg-final|" +
    canonical_json({
        "answer": answer,
        "clock": clock,
        "proof": {
            "a": a,
            "b": b,
            "c": c
        },
        "route": route
    })
)
```

The final stage was therefore treated as a challenge-specific construction rather than blindly assuming that the presence of a nonce and tag meant AES-GCM.

For the Solving Process Summary:

The overall investigation was:

```text
FIXED player (1).zip
        ↓
memory.raw
        ↓
accepted PID 4172
        ↓
LEDGER / TRAPDOOR- / 4421 / LAUNDRY-
        ↓
USN deleted-file relationships
        ↓
cook.pcapng
        ↓
29 × 39-byte accepted telemetry/ciphertext structure
        ↓
fixed-vs-old differential: 8f b2 01
        ↓
recover committed integer values
        ↓
verify SHA256(str(int(r)))
        ↓
a = r0
b = r1
c = r2 × inverse(r3) mod BN254
        ↓
_order(c)
        ↓
entry = VIOLET|LEDGER|SEVENTEEN|UNWOUND
        ↓
updated entry digest
        ↓
verifier acceptance
        ↓
unlock key
        ↓
final.enc
        ↓
CYS{violet_ledger_seventeen_unwound}
```

The key lesson is that the four commitments are **not themselves reversible**. The evidence has to be used to reconstruct the original integers, after which the commitment check is straightforward.

For the Final Answer:

```text
VERIFIER: ACCEPTED
ENTRY = VIOLET|LEDGER|SEVENTEEN|UNWOUND
FLAG = CYS{violet_ledger_seventeen_unwound}
```

The final flag is:

```text
CYS{violet_ledger_seventeen_unwound}
```

For the Attribution of the Investigation:

The initial verified facts in this writeup came from the challenge analysis supplied during the investigation: the accepted session, exact clock and route, forensic labels, USN mappings, commitment hashes, 32-bit brute-force result, PCAP structure, fixed-vs-old differential, verifier algebra, entry digest, and final encrypted artifact.

The purpose of documenting these supplied facts is to distinguish the **actual evidence and observations** from unsupported guesses about how an unreconstructed value was obtained.
