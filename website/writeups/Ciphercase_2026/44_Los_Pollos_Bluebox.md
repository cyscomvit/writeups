---
layout: writeup

title: Los Pollos Bluebox
difficulty: Medium
points: 10
categories: [Web/Reverse Engineering]
tags: []

flag: CTF{P0LL0S_1704_W3STG4TE}
---

Los Pollos Bluebox

Author: [Author Name]

This is a web and reverse-engineering CTF challenge involving evidence analysis, HTTP response inspection, reverse engineering, and a path traversal vulnerability.

## Description

The challenge begins with two evidence files that reveal a route reference and gate. The recovered information is submitted to the hosted application, after which HTTP response data and a client identifier lead to a reverse-engineering step. The recovered path is then used to exploit a path traversal vulnerability and obtain the final handoff code.

## Exploit Path

### 1. Evidence

Inspect `route_manifest.jpg`.

It provides the route reference:

`17-04`

and the dock:

`WEST`

Next, inspect `night_desk_transmission.wav`.

The audio contains a clean 9 kHz Morse layer. Standard Morse timing decodes it to:

`WEST 1704`

This corroborates the information from the image.

### 2. Public Dispatch

Submit:

`1704`

to the hosted application.

This creates the investigation session and returns the public record, including:

`gate=west`

The participant JavaScript does not contain the archive endpoint, so inspect the live HTTP response/network activity.

The response exposes the next route through the `X-Audit-Route` header.

Request:

`/api/archive/1704?gate=west`

The server returns:

`client=dp-legacy-3`

and audit action:

`R17W`

### 3. Reverse Engineering

Run:

`dp-legacy-3 --audit R17W`

The program does not directly print its maintenance path. It only prints a checksum.

Reverse the embedded transformation in a decompiler/debugger:

`v = (blob[i] - i*7) & 0xff; v ^= key[i % 4]`

using the key:

`R17W`

Reversing the operation yields:

`../private/relay_1704.dat`

### 4. Web Exploitation

Use the recovered path against the download route:

`/download?name=../private/relay_1704.dat`

The endpoint requires the active investigation session but permits traversal into the private evidence directory.

The returned file contains:

`P0LL0S-1704`

### 5. Final Handoff

Use the recovered code in the handoff request:

`/api/handoff?code=P0LL0S-1704`

The server returns the final flag:

`CTF{P0LL0S_1704_W3STG4TE}`

## Vulnerability

The `/download` endpoint accepts a user-controlled relative path and does not securely confine the requested file to the intended directory.

This allows path traversal using:

`../private/relay_1704.dat`

The challenge intentionally permits traversal into the private evidence directory while still requiring an active investigation session.

## Final Flag

`CTF{P0LL0S_1704_W3STG4TE}`
