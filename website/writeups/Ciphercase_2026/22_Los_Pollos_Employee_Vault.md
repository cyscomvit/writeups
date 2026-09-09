---
layout: writeup

title: Los Pollos Employee Vault
difficulty: Hard
points: 500
categories: Web/SQLi
flag: CYS{Dynamic}

---

Los Pollos Employee Vault

Author: Vitul

This is a web-based CTF challenge demonstrating a SQL injection vulnerability chained with an insecure privilege-handoff mechanism.

For the SQLi part:

The only injectable endpoint is the legacy directory search, /employees?q=. Every other query in the application is parameterized, so this is the sole entry point.

We craft a six-column UNION-based SQL injection against /employees?q= to enumerate the users table. Note that SQLite executes only a single statement per query, so stacked write statements are not possible here — the injection is read-only.

Using this, we're able to dump the employee directory and identify that Gustavo Fring holds the role of manager.

For the privilege-handoff part:

Knowing Gustavo is a manager isn't enough on its own — the runtime flag isn't revealed by the SQLi alone. We follow the intended chain:

Directory SQLi → Gus is manager → Audit: Vault-03 → Production: Batch 753
→ Gustavo's verified handoff → Vault-03 session grant → /vault

We review the Audit section, where Vault-03 is referenced, then check Production and locate Batch 753. Combining the directory-reconciled manager evidence (Gustavo) with the Audit and Production review completed in the current session lets us trigger Gustavo's verified handoff.

The server cross-checks this against the matching database records, then grants a Vault-03 session — this does not upgrade our role to manager, it simply grants scoped access to Vault-03.

With this session grant, we can access /vault, which accepts either a real manager account or a valid Vault-03 session grant, and the flag is rendered at runtime once vault authorization succeeds.

The vulnerability is a combination of SQL injection (unparameterized query on /employees?q=) and an overly trusting server-side delegation mechanism that grants vault access based on reconciled evidence rather than a properly scoped, short-lived credential.

Remediation: Parameterize the directory search endpoint, suppress verbose database errors, and remove the legacy handoff mechanism entirely. Where delegation between roles is genuinely required, it should be implemented server-side, short-lived, and narrowly scoped to the specific resource.
