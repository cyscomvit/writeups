---
layout: writeup

title: Blue Sky Dead Drop v2
difficulty: Hard
points: 500
categories: [Forensics / Network (DNS exfiltration) + Crypto + Reversing]
tags: []

flag: CYS{c4rb0n_c0py_dr0ps_d0nt_c0unt}
---

Blue Sky Dead Drop v2

Author: Gokul

## TL;DR of the solve chain

```
PCAP (DNS only)
  └─> exfil subdomains:  s<idx><type>.<hex>.<d1>.<d2>.<domain>
        │   "zero comes before A"   → base32hex alphabet (0-9a-v)
        │   "clean copies count once" → dedupe / ignore corrupted retries + 'r' rejects
        │   "check the order of delivery" → sort by base-36 sequence number
        ▼
      base32hex → 32-byte chunks → gzip → tar
        └─> labcheck (ELF)  +  cook_notes.txt  +  manifest.enc  +  drops.dat
              │  "manager special" = POLLOS7 (current slip)
              │  "token before batch stamp, one-char joiner"  →  TOKEN$B30852
              ▼
      labcheck accepts  POLLOS7$B30852
              ▼
      PBKDF2-HMAC-SHA256 → AES-256-GCM (AAD "BSC2") → decrypt manifest.enc
              └─> route=RV-052, window=15:08:52Z, key_fragment=d7d4299869b9d8c55138
              ▼
      payload XOR repeated_SHA256(fragment|route|window)  →  FLAG
```

---

## 0. Recon — what's actually in the capture

The README says a workstation was flagged for "unusual DNS activity" and only the
packet capture survived. Loading the PCAP with Scapy:

```python
from scapy.all import *
pkts = rdpcap('capture.pcap')
print(len(pkts))            # 464 packets
```

Every single packet is DNS. There are two populations:

1. **Background noise** — normal-looking lookups (`auth.corp.local`,
   `clients4.google.com`, `cdn.jsdelivr.net`, `time.cloudflare.com`, …) that all
   resolve to `203.0.113.x` (TEST-NET-3 documentation addresses). These exist to make
   the exfil traffic blend in.

2. **The exfil channel** — weird high-entropy labels of the form:

   ```
   s<INDEX><TYPE>.<HEX4>.<D1>.<D2>.<DOMAIN>
   e.g.  s000o.7a5b.619uabmtbvlj9h15j3n7.4p7vboikcm08ih3h69g.updates.madrigal-cache.net
   ```

Breaking that name down:

| part  | example      | meaning |
|-------|--------------|---------|
| `s000o` | `000` + `o` | base-36 **sequence number** (`000`) + **type** (`o`) |
| `7a5b` | hex          | a small 2-byte field (role unclear — see §Notes) |
| `d1`  | 619uabmtbvlj9h15j3n7 | payload chunk part 1 |
| `d2`  | 4p7vboikcm08ih3h69g | payload chunk part 2 |
| `edge` / `api` / `updates` / `img` | C2 domain | "which drop point this batch went to" |

Grouping the records by type:

| type | count (unique) | index pattern   | d1/d2 length | domain      |
|------|----------------|-----------------|--------------|-------------|
| `o`  | 24             | `36·k` (0,36,72,…) | 20 + 19      | api/updates/img |
| `q`  | 170            | `4 + 36·k`      | 26 + 26      | edge        |
| `r`  | 4              | scattered       | 26 + 26      | edge        |

Two observations that matter enormously:

* **`r` records are rejected batches.** Several `r` queries get an `rcode=3`
  (NXDOMAIN) response and are then retransmitted — they're the failed/dirty batches.
* **Some `q` indices appear twice** with payloads that differ by a single character
  (e.g. index `0b4` → `v5tebnsd…` vs `u5tebnsd…`). One copy is corrupted; the other is clean.

---

## 1. Reading the hints (the TXT records)

Three TXT answers in the capture carry the "cook's" instructions:

```
qa-note.madrigal-cache.net.
   TXT "QA memo: zero comes before A; clean copies count once;
        position precedes run length."

special.pollos.local.      TXT "Manager special: POLLOS7"
special.cache0.pollos.local TXT "Manager special: FAMILIA2"
special.cache1.pollos.local TXT "Manager special: VEGGIE4"
special.cache2.pollos.local TXT "Manager special: COMBO12"
```

Decoding the memo:

* **"zero comes before A"** → the data alphabet does not start at `a`; it starts at `0`.
  The `d1`/`d2` fields use *exactly* the 32-character set
  `0123456789abcdefghijklmnopqrstuv` — that's **base32hex** (RFC 4648 "Extended Hex
  Alphabet"). (The sequence numbers also use base-36 `0-9a-z`.)

* **"clean copies count once"** → deduplicate. For every logical chunk there may be
  several copies on the wire (retries, corrupted retransmits, and `r` rejects).
  Only *one clean copy* of each chunk goes into the message.

* **"position precedes run length"** → ordering/chunking matters: you must respect the
  position (sequence number) of each chunk when reassembling.

* **"the cook never repeats a recipe… check the order of delivery"** (README) →
  reassemble in sequence-number order, not capture order.

* **"the kitchen manager changed the special during the shift; Gus was particular
  about which slip was current"** → there are *several* "manager special" values, but
  only the **current** one (`special.pollos.local` → `POLLOS7`, no `.cacheN` suffix) is
  the live slip. The others are stale.

---

## 2. Reassembling and decoding the exfil stream

### 2.1 Collect & dedupe the records

```python
import re
from scapy.all import *

pkts = rdpcap('capture.pcap')
recs = []
for p in pkts:
    if not p.haslayer(DNS):
        continue
    q = p[DNS].qd.qname.decode().rstrip('.')
    m = re.match(r'^s([0-9a-z]{3})([a-z])\.([0-9a-f]{4})\.([0-9a-z]+)\.([0-9a-z]+)\.([a-z0-9.-]+)$', q)
    if m:
        idx, typ, hx, d1, d2, dom = m.groups()
        recs.append((int(idx, 36), typ, hx, d1, d2, dom, p[DNS].rcode))
```

### 2.2 base32hex → bytes

Each `q` record has `d1+d2 = 26+26 = 52` base32hex characters = `52 × 5 = 260` bits.
That's `32.5` bytes, so every label actually carries **32 bytes** with 4 bits of
padding. The important subtlety: the chunks are **self-contained** — decode each
label's 52 chars to 32 bytes individually (do *not* concatenate the strings and decode
in one shot, or the 4 padding bits per label desynchronise the bit stream).

```python
B32 = "0123456789abcdefghijklmnopqrstuv"

def b32hex_decode(s):                      # 52 chars -> 32 bytes
    bits = ''.join(f'{B32.index(c):05b}' for c in s)
    n = (len(bits) // 8) * 8
    return bytes(int(bits[i:i+8], 2) for i in range(0, n, 8))
```

### 2.3 Sort, choose clean copies, decompress

Sort the unique `q` records by sequence number, pick the clean copy at each of the
7 conflicted indices (validated by the gzip CRC32 — a wrong byte almost always fails
the CRC, which is exactly what "clean copies count once" exploits), drop the `r`
rejects, and decompress:

```python
import gzip

# dedupe: keep one variant per (idx, d1, d2)
uniq = {}
for r in recs:
    uniq.setdefault((r[0], r[2], r[3], r[4], r[5]), r)

q = sorted([r for r in uniq.values() if r[1] == 'q'], key=lambda r: r[0])

raw = b''.join(b32hex_decode(r[3] + r[4]) for r in q)
data = gzip.decompress(raw)          # -> POSIX tar archive
```

The first bytes are `1f 8b 08…` — the gzip magic confirms the encoding is right.

> **Brute-forcing the corrupt copies.** The 7 duplicated indices each have 2–3
> variants, so there are 192 combinations; a tiny loop that tries every combination
> and calls `gzip.decompress` until one succeeds pinpoints the clean copy of each
> chunk. (gzip's built-in CRC32 is the "QA checker".)

### 2.4 Extract the tar

```
tar -xf q_dec.bin
  labcheck         x86-64 ELF, stripped   ("Pollos QA / calibration gate")
  cook_notes.txt   the recipe
  manifest.enc     430 bytes, "BSC2" seal
  drops.dat        drop records
```

`cook_notes.txt`:

```
The resolver logged the manager special during the shift. That token is the first ingredient.
Batch stamp: B30852
Gus writes the menu token before the batch stamp. The QA checker knows the one-character joiner.
Whatever labcheck accepts is the exact sealing phrase for manifest.enc.

Seal recipe:
  header = BSC2 | iterations(le32) | salt(16) | nonce(12) | plaintext_sha256(32) | ciphertext+tag
  KDF    = PBKDF2-HMAC-SHA256, header iteration count, 32-byte key
  cipher = AES-256-GCM
  AAD    = BSC2
```

---

## 3. Reversing `labcheck` — the sealing phrase

`labcheck` is the "QA gate": feed it a phrase and it prints *Calibration accepted.*
or *rejected*. Disassembly (`objdump -d -M intel`) of `main` (at `0x4010a0`) shows the
validation:

```asm
40111b: call  strlen@plt
401120: cmp   rax,0xe          ; length must be 14
401124: jne   401272           ; -> rejected
40112a: cmp   BYTE PTR [rsp+0x67],0x24   ; char[7] must be '$'
401160: cmp   BYTE PTR [rsp+0x68],0x42   ; char[8] must be 'B'
; chars[0..6] must each be A-Z or 0-9
401140: movzx edx,BYTE PTR [rax]
401143: lea   ecx,[rdx-0x41]   ; 'A'
401146: cmp   cl,0x19          ; <= 'Z' ?
40114b: sub   edx,0x30         ; else '0'
40114e: cmp   dl,0x9           ; <= '9' ?
; chars[9..13] must be digits
401170: movzx eax,BYTE PTR [rbx+rdx*1]
401174: sub   eax,0x30
401177: cmp   al,0x9
```

So the accepted format is:

```
XXXXXXXX$B#####      (7 × [A-Z0-9], '$', 'B', 5 × digits)
```

→ "menu token before the batch stamp, joined by `$`" → `TOKEN$B30852`.

The current special is `POLLOS7`, and trying the four candidates:

```
POLLOS7$B30852  ->  Calibration accepted.   ✅
FAMILIA2$B30852 ->  Calibration rejected.
VEGGIE4$B30852  ->  Calibration rejected.
COMBO12$B30852  ->  Calibration rejected.
```

So the sealing phrase is **`POLLOS7$B30852`** (the `$` is the "one-character joiner").

---

## 4. Decrypting `manifest.enc`

Parse the header and decrypt per the recipe:

```python
import hashlib
from Crypto.Cipher import AES

data   = open('manifest.enc','rb').read()
magic  = data[0:4]            # b'BSC2'
iters  = int.from_bytes(data[4:8], 'little')   # 150000
salt   = data[8:24]
nonce  = data[24:36]
sha    = data[36:68]
ct     = data[68:]            # ciphertext + 16-byte tag

key = hashlib.pbkdf2_hmac('sha256', b'POLLOS7$B30852', salt, iters, 32)

cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
cipher.update(b'BSC2')                    # AAD
pt = cipher.decrypt_and_verify(ct[:-16], ct[-16:])
assert hashlib.sha256(pt).digest() == sha # integrity check
```

Plaintext:

```
FRING DISTRIBUTION // VERIFIED MANIFEST
route=RV-052
window=15:08:52Z
key_fragment=d7d4299869b9d8c55138
drops_sha256=38a1d08e82459795af146e448ed7ddba0611e1da8a2eb417652f89de7647257f
mask_rule=SHA256(key_fragment + "|" + route + "|" + window); repeat digest and XOR payload bytes
instruction=Use the record matching route and window in drops.dat.
```

---

## 5. Unmasking the drop

`drops.dat` is a table of `DROP2|route|window|payload_hex` rows. The manifest points at
`RV-052 @ 15:08:52Z`:

```
RV-052|15:08:52Z|61abdaeef3a48947d50f2b854c80bf8360d0dcdd8bcdbcf6976730d600e044845f
```

The `mask_rule` is a classic repeating-key XOR stream cipher keyed by a SHA-256 digest:

```python
import hashlib

payload = bytes.fromhex("61abdaeef3a48947d50f2b854c80bf8360d0dcdd8bcdbcf6976730d600e044845f")
mask = hashlib.sha256(b"d7d4299869b9d8c55138|RV-052|15:08:52Z").digest()
mask = (mask * (len(payload)//len(mask) + 1))[:len(payload)]

flag = bytes(a ^ b for a, b in zip(payload, mask))
print(flag.decode())
```

Output:

```
CYS{c4rb0n_c0py_dr0ps_d0nt_c0unt}
```

The flag is self-referential — *"carbon-copy drops don't count"* — a callback to the
whole deduplication theme of the challenge. 🍗

---

## Appendix — consolidated solver

```python
#!/usr/bin/env python3
import re, gzip, tarfile, hashlib, itertools
from scapy.all import *
from Crypto.Cipher import AES

B32 = "0123456789abcdefghijklmnopqrstuv"
def b32hex_decode(s):
    bits = ''.join(f'{B32.index(c):05b}' for c in s)
    n = (len(bits)//8)*8
    return bytes(int(bits[i:i+8],2) for i in range(0,n,8))

# ---- 1. parse the exfil records ----
recs = []
for p in rdpcap('capture.pcap'):
    if not p.haslayer(DNS): continue
    q = p[DNS].qd.qname.decode().rstrip('.')
    m = re.match(r'^s([0-9a-z]{3})([a-z])\.([0-9a-f]{4})\.([0-9a-z]+)\.([0-9a-z]+)\.([a-z0-9.-]+)$', q)
    if m:
        idx, typ, hx, d1, d2, dom = m.groups()
        recs.append((int(idx,36), typ, hx, d1, d2, dom, p[DNS].rcode))

# ---- 2. rebuild the stream (dedupe, sort by index, drop 'r' rejects) ----
from collections import defaultdict
by = defaultdict(list)
for r in recs:
    if r[1] in ('q','r'):
        by[r[0]].append(r)

order = sorted(i for i in by if i % 36 == 4)
variants = {i: [] for i in order}
for i in order:
    for r in by[i]:
        v = (r[2], r[3], r[4])
        if v not in variants[i]: variants[i].append(v)

dup = [i for i in order if len(variants[i]) > 1]
for combo in itertools.product(*[range(len(variants[i])) for i in dup]):
    sel = {}
    for k,i in enumerate(dup): sel[i] = variants[i][combo[k]]
    for i in order:
        if i not in sel: sel[i] = variants[i][0]
    raw = b''.join(b32hex_decode(sel[i][1]+sel[i][2]) for i in order)
    try:
        tar = gzip.decompress(raw); break
    except Exception: pass

with open('q_dec.bin','wb') as f: f.write(tar)

# ---- 3. decrypt the manifest ----
data = open('manifest.enc','rb').read()
key  = hashlib.pbkdf2_hmac('sha256', b'POLLOS7$B30852',
                           data[8:24], int.from_bytes(data[4:8],'little'), 32)
c = AES.new(key, AES.MODE_GCM, nonce=data[24:36]); c.update(b'BSC2')
pt = c.decrypt_and_verify(data[68:-16], data[-16:])
print(pt.decode())

# ---- 4. unmask the drop ----
payload = bytes.fromhex('61abdaeef3a48947d50f2b854c80bf8360d0dcdd8bcdbcf6976730d600e044845f')
mask    = hashlib.sha256(b'd7d4299869b9d8c55138|RV-052|15:08:52Z').digest()
flag    = bytes(a^b for a,b in zip(payload, (mask*10)[:len(payload)]))
print(flag.decode())   # CYS{c4rb0n_c0py_dr0ps_d0nt_c0unt}
```

---

## Notes on red herrings & dead ends

* **The `o`-series and the 2-byte hex field.** I spent a while trying to make the
  24 `o` records (indices `36·k`, interleaved with the `q` series in the same
  namespace) and the per-record `hex4` field decode into something (RLE, checksums,
  positions). They appear to be filler/timing noise that makes the channel look busier
  — the actual file came entirely from the `q` series. The `hex4` field is likely a
  per-chunk tag that the "QA checker" (gzip CRC) ended up making redundant.

* **"position precedes run length"** reads like a hint toward a run-length encoding,
  but the recovered payload is just gzip — the phrase effectively reinforces that
  chunk **positions** (sequence numbers) must be respected before content is consumed.
  It isn't load-bearing for the final decode.

* **`drops_sha256` in the manifest** is the SHA-256 of the *cleartext* drop record
  (a consistency check for the route table), not of the masked payload.
