---
layout: writeup

title: The Blackwood Manor Case File
difficulty: Medium
points: 300
categories: [Web/Applied Cryptography]
tags: [JWT, Algorithm Confusion, RS256, HS256]

flag: CYS{alg_confusion_ashworth_forged_the_seal}
---

The Blackwood Manor Case File

The challenge is a web-based applied cryptography challenge involving a **JWT algorithm confusion vulnerability**.

The server-side token examiner trusts the `alg` value specified in the JWT header and selects the verification method accordingly.

For `RS256`, it performs RSA signature verification using the RSA public key.

For `HS256`, it performs HMAC-SHA256 verification but incorrectly uses the **same RSA public key text as the HMAC secret**.

Since the RSA public key is not secret, we can use it to forge a valid HS256 token.

## Finding the Public Key

Firstly, we open `index.html` in a browser and inspect the page source.

Searching for:

```text
BEGIN PUBLIC KEY
```

reveals the RSA public key inside a hidden element:

```html
<pre id="exhibit-4">
```

This is the public key used by the token examiner to verify the JWT signature.

We copy the complete PEM block exactly as it appears, including the `BEGIN PUBLIC KEY` and `END PUBLIC KEY` lines and the line breaks.

## Inspecting the Guest Token

The page also displays the decoded payload of the guest token.

The payload has the following structure:

```json
{
  "sub": "...",
  "name": "...",
  "role": "guest",
  "case": "blackwood-manor",
  "iat": "..."
}
```

The important field is `role`, which is currently set to:

```text
guest
```

We need to change this to:

```text
chief_inspector
```

## Exploiting JWT Algorithm Confusion

The vulnerability occurs because the examiner trusts the algorithm specified in the JWT header.

The original token uses RSA-based signing:

```json
{
  "alg": "RS256",
  "typ": "JWT"
}
```

We can change the algorithm to `HS256`:

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

We then create a payload with the required role:

```json
{
  "sub": "attacker",
  "name": "A. Ashworth",
  "role": "chief_inspector",
  "case": "blackwood-manor"
}
```

The crucial mistake is that the application uses the RSA **public key text** as the HMAC secret when `HS256` is selected.

Therefore, we can sign our forged token ourselves using the publicly available RSA key.

## Creating the Forged Token

This can be done using tools such as jwt.io or locally with libraries such as `jose` or `PyJWT`.

Using jwt.io, set the header to:

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

and the payload to:

```json
{
  "sub": "attacker",
  "name": "A. Ashworth",
  "role": "chief_inspector",
  "case": "blackwood-manor"
}
```

Next, paste the RSA public key copied from the page source into the secret field.

Make sure **"secret base64 encoded" is unchecked**, so the public key is interpreted as raw UTF-8 bytes.

jwt.io then calculates the HMAC-SHA256 signature using the RSA public key text as the secret.

The resulting JWT has the usual three components:

```text
header.payload.signature
```

Copy the complete token.

## Accessing the Evidence Room

Paste the forged JWT into **Present Credentials** and submit it.

The examiner reads the JWT header and sees:

```text
alg: HS256
```

It therefore performs HMAC-SHA256 verification using the RSA public key text.

Since we used the exact same public key text to generate the HMAC signature, the signature verification succeeds.

The examiner then checks the token's role:

```text
chief_inspector
```

Access is granted and the Evidence Room is unsealed.

The flag is revealed:

```text
CYS{alg_confusion_ashworth_forged_the_seal}
```

The complete attack chain is:

```text
Inspect page source
        ↓
Extract RSA public key
        ↓
Inspect guest JWT
        ↓
Change RS256 → HS256
        ↓
Change role → chief_inspector
        ↓
Sign using RSA public key as HMAC secret
        ↓
Submit forged JWT
        ↓
Access Evidence Room
        ↓
Flag
```