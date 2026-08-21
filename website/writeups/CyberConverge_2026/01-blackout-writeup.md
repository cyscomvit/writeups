---
layout: writeup

title: Blackout Profile
difficulty: Easy
points: 10
categories: [Crypto/Web]
tags: []

flag: CYS{idor_is_just_an_object_reference}
---

Blackout Profile

Author: Advika

This is a crypto+web-based CTF challenge demonstrating an Insecure Direct Object Reference (IDOR) vulnerability.

Firstly for the Crypto part:

We can use common online tools like Cyberchef to solve the following 3 challenges.

The challenges are basic base64 encoding, caeser cipher (bruteforce), simple xor with the given key. 

For the IDOR part:
First, we access the login page

The application provides a login form. Use the credentials provided with the previous challenge:

Username: Alice
Password: very_secure_pwd

After logging in, the application redirects to:

/idor/profile/1001

Since the profile ID is directly exposed in the URL, we test whether changing it allows access to another user's profile.

We change the profile value 1001 to 1

The application returns another employee profile, confirming that it does not properly verify whether the authenticated user is authorized to access the requested profile.

The vulnerability is an Insecure Direct Object Reference (IDOR). The application exposes an internal object identifier directly in the URL:

/idor/profile/<user_id>

The server accepts an arbitrary user_id and retrieves the corresponding profile without checking whether the current user is authorized to access it.
