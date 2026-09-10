---
layout: writeup

title: Heisenberg's Lab
difficulty: Medium
points: 30
categories: [Web]
tags: []

flag: CYS{MY_NAME_1S_SK7L4R_WH1TE_Y0}
---

Heisenberg's Lab

Author: keshav

This is a web-based CTF challenge demonstrating a Server-Side Request Forgery (SSRF) style recon step chained with an access-control bypass via header spoofing and a derived key.

The challenge is a Breaking Bad-themed portfolio site. Reaching the flag requires clearing two independent layers (a spoofed "lab network" header and a derived vault key), then decoding a flag that is split into two reversed base64 halves.

Note: requests need custom headers, so use curl (with -L to follow Vercel's canonical redirect) or Burp. The browser address bar cannot set headers.

Firstly, recon:

We access the site and inspect the page source, and probe the import endpoint with no parameter:

/api/import

The error response names an internal registry at /api/svc-map and notes it is restricted to lab-network clients (X-Lab-Client: 10.10.x.x).

We confirm the import feature is a URL fetcher (SSRF):

/api/import?url=https://example.com

The server returns the fetched content, confirming it fetches arbitrary URLs.

For the first layer (header spoofing):

Hitting the internal registry directly is denied:

curl -L "http://<host>/api/svc-map"

This returns "Access denied: lab network only". We spoof the custom lab-network header with a 10.10.x.x value:

curl -L "http://<host>/api/svc-map" -H "X-Lab-Client: 10.10.1.5"

The registry now responds, revealing the credential vault path /api/v1/vault/superlab and the key scheme: the vault name reversed, then base64.

For the second layer (key derivation):

The vault name is "superlab". Reversed it becomes "balrepus". Base64-encoded it becomes "YmFscmVwdXM=". This is the key.

We reach the vault with both the spoofed header and the derived key:

curl -L "http://<host>/api/v1/vault/superlab?key=YmFscmVwdXM=" -H "X-Lab-Client: 10.10.1.5"

The vault returns two values, material_a and material_b.

For the flag decoding:

Each half is reversed. We un-reverse both halves, concatenate them (material_a + material_b), and base64-decode the result to recover the flag.

The vulnerability chain is: an SSRF-style import endpoint that aids recon, an access-control check that trusts a spoofable client header (X-Lab-Client) instead of a real network boundary, and a weakly derived vault key (the resource name reversed and base64-encoded). None of these individually protect the resource, and together they can be bypassed by an attacker who reads the recon hints.

Deployment note (for organizers): the flag is provided at runtime via the FLAG environment variable, and Vercel Deployment Protection must be disabled or every request is redirected to a Vercel login page.
