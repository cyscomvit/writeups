---
layout: writeup

title: Heisenberg's Vault
difficulty: Hard
point: 500
categories: [Web, Cryptography]
tags: []

flag: FLAG{heisenberg_was_not_the_only_one_breaking_bad}
---

Heisenberg's Vault

Madrigal Security has detected unusual activity inside one of its secure facilities.

An operator has access to the internal security portal, but their clearance is insufficient to access the highly classified vault.

The challenge combines two vulnerabilities:

1. **Web authorization bypass through Unicode normalization**
2. **Cryptographic keystream reuse**

The intended solution is to first escalate from a normal operator to an administrator, then use information exposed by the diagnostic endpoint to recover the vault's encrypted flag.

---

## 1. Initial Access

The challenge begins at the Madrigal Security login portal.

The provided credentials are:

```
Username: madrigal_047
Password: LosPollos47
```

After logging in, the player receives a normal user/operator authentication token.

The dashboard displays:

```
Role: user
```

The application uses the following token format:

```
username.timestamp.role.signature
```

For example:

```
madrigal_047.1750000000.u.<HMAC>
```

The role is represented internally using:

- `u` = user
- `a` = admin

---

## 2. Enumerating the Application

The dashboard exposes several API endpoints:

```
/api/status
/api/profile
/api/token-info
/api/token
/api/diagnostic
/api/vault
```

The first useful endpoint is:

```
/api/token-info
```

It reveals information about the token format:

```json
{
    "format": "username.timestamp.role.signature",
    "algorithm": "HMAC-SHA256",
    "role_encoding": {
        "u": "operator",
        "a": "administrator"
    },
    "normalization": "enabled"
}
```

The important clue is:

```
"normalization": "enabled"
```

This suggests that the application's handling of role values may be worth investigating.

---

## 3. Investigating the Clearance Endpoint

The next interesting endpoint is:

```
POST /api/token
```

A normal request looks like:

```http
POST /api/token
Content-Type: application/json

{
    "role": "user"
}
```

Trying the obvious privilege escalation:

```json
{
    "role": "admin"
}
```

results in:

```
403 Forbidden
```

The application responds with an error such as:

```
CLEARANCE REQUEST REJECTED.
```

At first glance, the endpoint appears secure. However, the source code reveals an important flaw.

---

## 4. Unicode Normalization Vulnerability

The application checks the requested role **before** performing Unicode normalization:

```python
if requested_role == "admin":
    return jsonify({
        "error": "CLEARANCE REQUEST REJECTED."
    }), 403

canonical_role = unicodedata.normalize(
    "NFKC",
    requested_role
)
```

This creates a mismatch between:

- **Security Check:** `requested_role`
- **Value Used by the Application:** `canonical_role`

The application first checks whether the original value is literally `admin`. It then normalizes the value using `NFKC`.

Unicode NFKC normalization converts compatibility characters into their canonical equivalents. For example:

```
ａｄｍｉｎ  →  admin
```

---

## 5. Exploiting the Normalization

Instead of sending:

```json
{
    "role": "admin"
}
```

the player sends:

```json
{
    "role": "ａｄｍｉｎ"
}
```

The server first evaluates:

```
requested_role == "admin"
```

This evaluates to `False`, because `ａｄｍｉｎ` is not literally the ASCII string `admin`. The request therefore passes the blacklist.

The application then performs:

```python
unicodedata.normalize("NFKC", requested_role)
```

which produces `admin`. The application subsequently creates a token using `admin` as the role.

---

## 6. Why the HMAC Does Not Save the Application

The token uses HMAC-SHA256, so it may initially appear impossible to forge. However, the player does not need to forge the HMAC.

The vulnerable `/api/token` endpoint generates a valid HMAC-signed token itself.

The process is effectively:

```
Attacker input
      ↓
ａｄｍｉｎ
      ↓
NFKC normalization
      ↓
admin
      ↓
create_token()
      ↓
valid HMAC
      ↓
administrator token
```

Therefore, the cryptographic integrity of the token is not directly broken. The problem is the authorization logic that decides what gets signed.

---

## 7. Obtaining Administrator Access

The response from `/api/token` contains the newly generated token.

Once the token is used as the authentication cookie, the application recognizes the player as:

```
role = admin
```

The previously inaccessible endpoint `/api/vault` now returns the encrypted vault payload.

Conceptually:

```json
{
    "service": "Madrigal Secure Vault",
    "classification": "HEISENBERG",
    "version": "3.0",
    "cipher": "VX-CTR",
    "nonce": "U1RBVElDLU5PTkNFLTIwMjY=",
    "payload": "azb3WqQl..."
}
```

At this point, the web portion of the challenge is complete.

---

## 8. Investigating the Cryptography

The player can now access:

```
/api/diagnostic
```

This endpoint exposes diagnostic information about the cryptographic system:

```
Cipher: VX-CTR
Nonce: STATIC-NONCE-2026
Message: <known plaintext>
Payload: <known ciphertext>
```

The known plaintext is:

```
MADRIGAL SECURITY NOTICE: SUPERLAB SYSTEMS OPERATIONAL; ALL PERSONNEL MUST MAINTAIN CURRENT CLEARANCE; VAULT MONITORING ACTIVE
```

The corresponding known ciphertext is:

```
YDvyT5YKbx09Z7dJUqJq2b4rB9lUGVqTG0poXF8OxtcfF+L1uoHZ85ZwRzblGgeAPGxVD0F3saC2AQqP+HoH5A2JxB2yTIWevY2C/whqgsGPtTjQ9/GHgjUDSWOxJ4Mtr3JxRIYvc4l3NByWJ1OokepH00g+oQo4dVsYBLvW
```

The vault ciphertext is:

```
azb3WqQlSzhuUZxoYoJE0pBqOsluP22JVQJeVmAl+OIBOqzDvLD/07pIDhfSADegDFg=
```

---

## 9. Understanding the Cipher

The implementation uses a custom XOR-based construction. Conceptually:

```
Ciphertext = Plaintext XOR Keystream
```

The keystream is generated using:

```
HMAC-SHA256 + static nonce + counter
```

The critical weakness is that the same keystream is reused. This creates the classic problem associated with reusing a one-time pad or stream-cipher keystream.

For the known plaintext `P_known` and known ciphertext `C_known`, we have:

```
C_known = P_known XOR K
```

Therefore:

```
K = P_known XOR C_known
```

The attacker can recover the keystream without knowing the secret key.

---

## 10. Recovering the Keystream

First, decode the Base64 ciphertext:

```python
known_ciphertext = base64.b64decode(KNOWN_CIPHERTEXT)
```

Convert the known plaintext into bytes:

```python
known_plaintext = KNOWN_MESSAGE.encode()
```

Then XOR the two:

```python
keystream = bytes(
    a ^ b
    for a, b in zip(
        known_plaintext,
        known_ciphertext
    )
)
```

This recovers the portion of the keystream corresponding to the known message.

---

## 11. Decrypting the Flag

The vault ciphertext is also Base64 encoded. Decode it:

```python
flag_ciphertext = base64.b64decode(
    FLAG_CIPHERTEXT
)
```

Then XOR it with the recovered keystream:

```python
flag = bytes(
    a ^ b
    for a, b in zip(
        flag_ciphertext,
        keystream
    )
)
```

Finally:

```python
print(flag.decode())
```

produces:

```
FLAG{heisenberg_was_not_the_only_one_breaking_bad}
```

---

## 12. Complete Solver

```python
import base64

KNOWN_MESSAGE = (
    "MADRIGAL SECURITY NOTICE: SUPERLAB SYSTEMS OPERATIONAL; "
    "ALL PERSONNEL MUST MAINTAIN CURRENT CLEARANCE; "
    "VAULT MONITORING ACTIVE"
)

KNOWN_CIPHERTEXT = (
    "YDvyT5YKbx09Z7dJUqJq2b4rB9lUGVqTG0poXF8OxtcfF+L1uoHZ85ZwRzblGgeAPGxVD0F3saC2AQqP+HoH5A2JxB2yTIWevY2C/whqgsGPtTjQ9/GHgjUDSWOxJ4Mtr3JxRIYvc4l3NByWJ1OokepH00g+oQo4dVsYBLvW"
)

FLAG_CIPHERTEXT = (
    "azb3WqQlSzhuUZxoYoJE0pBqOsluP22JVQJeVmAl+OIBOqzDvLD/07pIDhfSADegDFg="
)

known_plaintext = KNOWN_MESSAGE.encode()

known_ciphertext = base64.b64decode(
    KNOWN_CIPHERTEXT
)

flag_ciphertext = base64.b64decode(
    FLAG_CIPHERTEXT
)

keystream = bytes(
    p ^ c
    for p, c in zip(
        known_plaintext,
        known_ciphertext
    )
)

flag = bytes(
    c ^ k
    for c, k in zip(
        flag_ciphertext,
        keystream
    )
)

print(flag.decode())
```

**Output:**

```
FLAG{heisenberg_was_not_the_only_one_breaking_bad}
```

---

## 13. Full Attack Chain

```
HEISENBERG'S VAULT
        │
        ▼
Login as operator
        │
        ▼
Explore API endpoints
        │
        ▼
/api/token-info
        │
        ▼
Discover role normalization
        │
        ▼
Try normal "admin" → 403
        │
        ▼
Send Unicode full-width role
"ａｄｍｉｎ"
        │
        ▼
NFKC normalization
        │
        ▼
"admin"
        │
        ▼
Server signs administrator token
        │
        ▼
Access /api/vault
        │
        ▼
Obtain flag ciphertext
        │
        ▼
Access /api/diagnostic
        │
        ▼
Obtain known plaintext
and known ciphertext
        │
        ▼
Known Plaintext XOR Ciphertext
        │
        ▼
Recover keystream
        │
        ▼
Flag Ciphertext XOR Keystream
        │
        ▼
FLAG{heisenberg_was_not_the_only_one_breaking_bad}
```

---

## 14. Vulnerabilities Used

### Vulnerability 1 — Improper Unicode Canonicalization

**Root Cause**

The application validates the raw input before normalizing it:

```python
if requested_role == "admin":
```

followed by:

```python
canonical_role = unicodedata.normalize(
    "NFKC",
    requested_role
)
```

**Correct Design**

Normalization should happen before authorization:

```python
canonical_role = unicodedata.normalize(
    "NFKC",
    requested_role
)

if canonical_role == "admin":
    ...
```

Even better, authorization should be based on server-controlled roles rather than accepting a role from an untrusted client.

### Vulnerability 2 — Keystream Reuse

The encryption follows:

```
C = P XOR K
```

The same `K` is reused for multiple messages.

Once `P_known` and `C_known` are available:

```
K = P_known XOR C_known
```

The attacker can then decrypt another ciphertext encrypted with the same keystream.

**Correct Design**

A stream cipher or CTR-style construction should use a unique nonce/IV for every encryption operation. Never reuse the same keystream for different plaintexts.

---

## 15. Why SQL Injection Is Not Part of the Intended Solution

The login query uses parameterized SQL:

```python
conn.execute(
    """
    SELECT id, username, role
    FROM users
    WHERE username = ? AND password = ?
    """,
    (username, password)
)
```

The `?` placeholders prevent normal SQL injection through the login fields. Therefore, SQL injection is not an intended attack path.

The challenge is designed around a controlled exploitation chain rather than unrelated vulnerabilities.

---

## 16. Why the HMAC Is Not Broken

The HMAC implementation itself is not the intended weakness.

The attacker never needs to calculate:

```
HMAC(secret, malicious_data)
```

Instead, the application calculates it for them. The problem is:

```
Untrusted role
      ↓
Normalization
      ↓
Token generation
      ↓
HMAC signing
```

The server is effectively signing an attacker-controlled authorization decision.

Therefore: the cryptographic primitive is functioning correctly; the authorization logic around it is not.

---

## 17. Intended Learning Outcomes

**Web Security**
- Authentication vs authorization
- Role-based access control
- Unicode canonicalization
- Input normalization
- Privilege escalation
- Why signing bad data does not make an authorization decision secure

**Cryptography**
- XOR properties
- Stream-cipher concepts
- Keystreams
- Known-plaintext attacks
- Nonce reuse
- Why a secure primitive can become insecure through incorrect implementation

---

## 18. Final Flag

```
FLAG{heisenberg_was_not_the_only_one_breaking_bad}
```

**Challenge lesson:** The system didn't need to be hacked in the traditional sense. It trusted the wrong representation of the user's clearance, then reused cryptographic material in a way that exposed the encrypted secret.
