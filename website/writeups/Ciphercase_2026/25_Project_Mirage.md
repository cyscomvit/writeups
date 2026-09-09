---
layout: writeup

title: Project Mirage
difficulty: Medium
points: 300
categories: [Web]
flag: CYS{Dynamic}
---

Project Mirage

Author: Shubh

This is a standalone web-based CTF challenge demonstrating a Broken Object Level Authorization (BOLA / IDOR) vulnerability.

The application, DeployBox, simulates a deployment dashboard where logged-in users can view details about their own workspace's deployments.

First, we access the login page

The application provides a login form. Use the credentials provided with the challenge:

Username: Shubh\
Password: greatguy

After logging in, we land on the Dashboard.

Finding the vulnerable API

On the Dashboard, we click "View deployment" on one of our own deployments. Opening DevTools -> Network while doing this reveals the request the frontend makes to fetch deployment details:

GET /api/v1/deployments/dep_xxxxxx

This confirms the app fetches deployment data client-side by ID, via a REST-style endpoint.

Finding another workspace's deployment ID

Next, we go to the Activity page. This page lists recent deployment activity, including deployment IDs — and on inspection, not all of these IDs belong to our own workspace. One (or more) of them belongs to a different workspace entirely.

We take note of this "foreign" deployment ID, for example:

dep_63d0c9

Exploiting the IDOR

We now substitute this foreign ID directly into the API endpoint discovered earlier:

GET /api/v1/deployments/dep_63d0c9

The server does not verify that the requesting user's workspace owns the requested deployment ID — it simply looks up the deployment by ID and returns its data, regardless of ownership.

The response includes full deployment details belonging to another workspace, including a release_note field containing the flag.

Root cause

The vulnerability is a Broken Object Level Authorization (BOLA), a specific case of IDOR. The application exposes an internal, enumerable/guessable object identifier (the deployment ID) and trusts the client to only ever request IDs it's authorized to see:

/api/v1/deployments/<deployment_id>

The server retrieves whatever deployment matches the given ID without checking that it belongs to the authenticated user's workspace.

Note: Deployment IDs (and therefore the flag) are randomly generated per challenge instance/restart, so the exact ID and flag value will differ across runs — only the CTF{...} format is fixed.

Summary

Login -> find deployment-fetching API via Network tab -> find a foreign deployment ID via Activity page -> request it via the API -> flag is returned in release_note.
