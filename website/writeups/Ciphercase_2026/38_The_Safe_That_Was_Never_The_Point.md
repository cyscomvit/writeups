---
layout: writeup

title: The Safe That Was Never the Point
difficulty: Hard
points: 500
categories: Cryptography

flag: CYS{y0uR_$h@M1r_$ecR3ts_aR3_s@f3_w1th_Me_uNd3r_tHr8_0f_d1sB@rM3nt}
---

The Safe That Was Never the Point

Author: Om

This is a cryptography challenge combining Shamir Secret Sharing, Feldman VSS on secp256k1, RSA Hastad Broadcast Attack with CRT, SHA-256-based key derivation, XOR-based fragment recovery, and Lagrange interpolation to reconstruct the final flag.

For the Shamir shares and Feldman VSS verification:

The challenge contains ten Shamir shares. Some of them have been corrupted.

The story hints that some pages have invalid seals.

The commitments in `archived_pages.json` allow verification using Feldman VSS.

The curve used is secp256k1.

For every share:

```text id="f6qf91"
yG = C0 + xC1 + x²C2 + ... + x⁹C9
```

If both sides match, the share is valid.

```python id="g5x5j1"
import json
from ecdsa import SECP256k1, ellipticcurve

curve = SECP256k1
G = curve.generator
N = curve.order


def point_from_json(obj):
    return ellipticcurve.Point(
        curve.curve,
        int(obj["x"],16),
        int(obj["y"],16),
        N
    )


def verify_share(x,y,commitments):

    lhs = y * G
    rhs = ellipticcurve.INFINITY

    power = 1

    for c in commitments:
        rhs += power * point_from_json(c)
        power = (power*x) % N

    return lhs == rhs


with open("archived_pages.json") as f:
    data=json.load(f)


valid=[]

for share in data["shares"]:

    x=share["x"]
    y=int(share["y"],16)

    if verify_share(
        x,
        y,
        data["commitments"]
    ):
        valid.append((x,y))


print("Valid shares:")
print([x for x,y in valid])
```

The output is:

```text id="8f6t8s"
Valid shares:
[2,5,6,9]
```

These four shares are used for RSA selection.

For the RSA record selection:

Only the valid shares are used.

They are sorted by x value and encoded as:

```text id="l9n3h4"
x || y
```

where:

* x is 1 byte
* y is 32 bytes

The SHA-256 hash of this data selects the RSA record:

```text id="n7sgji"
record = SHA256(data) % 4
```

```python id="3z8f9n"
import hashlib

valid.sort()

payload=b""

for x,y in valid:

    payload += x.to_bytes(1,"big")
    payload += y.to_bytes(32,"big")


digest = hashlib.sha256(
    payload
).digest()


record = int.from_bytes(
    digest,
    "big"
) % 4


print(record)
```

The output is:

```text id="k8f7x2"
3
```

Therefore:

```text id="r3n4w6"
sealed_folders.json -> 3
```

is the real RSA record.

For recovering the corrupted shares via the RSA Hastad Broadcast Attack:

The selected RSA record contains three ciphertexts.

The story hints:

* same plaintext
* three RSA encryptions
* no padding
* cube root recovery

This is RSA Hastad Broadcast Attack.

The exponent is:

```text id="v9k2s4"
e = 3
```

CRT combines the ciphertexts:

```text id="p3c7x1"
c1,c2,c3
```

into:

```text id="h4m8q2"
m³
```

Then the integer cube root gives the plaintext.

```python id="z6n1r8"
import json
from math import prod


def crt(records):

    N=prod(
        n for n,c in records
    )

    result=0

    for n,c in records:

        Ni=N//n
        inv=pow(Ni,-1,n)

        result += c*Ni*inv

    return result % N


def cube_root(n):

    lo=0
    hi=1<<(n.bit_length()//3+2)

    while lo<hi:

        mid=(lo+hi+1)//2

        if mid**3<=n:
            lo=mid
        else:
            hi=mid-1

    return lo


with open("sealed_folders.json") as f:
    data=json.load(f)


selected=data["records"]["3"]

records=[
    (r["n"],r["c"])
    for r in selected
]


m3=crt(records)

m=cube_root(m3)

payload=m.to_bytes(
    (m.bit_length()+7)//8,
    "big"
)


print(payload.hex())


records=[]

for offset in range(0, len(payload), 33):

    x = payload[offset]
    y = int.from_bytes(
        payload[offset + 1:offset + 33],
        "big"
    )

    records.append((x, y))


recovered = [
    {"x": x, "y": hex(y)}
    for x, y in records
]

with open("recovered_shares.json", "w") as f:
    json.dump(recovered, f, indent=4)

print("recovered_shares.json written")
```

The recovered payload contains:

```text id="c8j5w3"
6 original (x,y) pairs
```

These correspond to the corrupted shares:

```text id="u2m6k9"
x = 1,3,4,7,8,10
```

For repairing the shares:

The RSA plaintext gives the original values of corrupted shares.

Replace those values in `shares.json`.

```python id="q4v8s2"
import json

with open("archived_pages.json") as f:
    shares_data = json.load(f)

with open("recovered_shares.json") as f:
    recovered = json.load(f)

recovered_map = {r["x"]: r["y"] for r in recovered}

for share in shares_data["shares"]:
    if share["x"] in recovered_map:
        share["y"] = recovered_map[share["x"]]

with open("repaired_shares.json", "w") as f:
    json.dump(shares_data, f, indent=4)

print("repaired_shares.json written")
```

After repair, Feldman verification should mark all shares as valid.

The output file becomes:

```text id="j5r2n7"
repaired_shares.json
```

For reconstructing the Shamir secret:

The repaired shares can reconstruct the Shamir secret.

The secret is:

```text id="b8w3q6"
f(0)
```

using Lagrange interpolation.

This is only a verification step.

The secret is not the flag.

For recovering the XOR-encoded flag fragments:

`hidden_strips.json` contains only encoded fragments.

The missing x values are recovered from the RSA payload.

For every recovered share:

```text id="e7t4m9"
mask = SHA256(
"CYS-XOR" || x || original_y
)
```

Then:

```text id="s1n6p8"
fragment = encoded XOR mask
```

The decoded fragments are sorted by x and joined.

```python id="w2k9f5"
import json
import hashlib


with open("recovered_shares.json") as f:
    recovered=json.load(f)

with open("hidden_strips.json") as f:
    fragments=json.load(f)


recovered.sort(
    key=lambda x:x["x"]
)


def mask(x,y):

    data=(
        b"CYS-XOR"
        + x.to_bytes(1,"big")
        + y.to_bytes(32,"big")
    )

    return hashlib.sha256(data).digest()


flag=[]


for share,fragment in zip(
    recovered,
    fragments["fragments"]
):

    x=share["x"]
    y=int(share["y"],16)

    encoded=bytes.fromhex(
        fragment["encoded"]
    )

    m=mask(x,y)

    flag.append(
        bytes(
            a^b
            for a,b in zip(
                encoded,
                m
            )
        )
    )


print(
    b"".join(flag).decode()
)
```

The final flag is:

```text id="r7c4x1"
CYS{y0uR_$h@M1r_$ecR3ts_aR3_s@f3_w1th_Me_uNd3r_tHr8_0f_d1sB@rM3nt}
```
