---
layout: writeup

title: Encrypt Twice For Thrice The Fun
difficulty: Hard
points: 500
categories: [Cryptography]
tags: []

flag: CYS{dynamic}
---

Encrypt Twice For Thrice The Fun

Author: Utkarsh Raj

## Challenge Description

Players are given a small cryptographic service with two available functions. The service does not reveal the algorithm or key directly.

**Function 1** accepts a plaintext and a user-supplied key, then returns a ciphertext.

**Function 2** accepts a user-supplied key and returns a ciphertext derived from a hidden flag.

The player has only **two total function queries**, so the outputs must be analyzed carefully.

There are no dedicated cryptographic clue files. The challenge is intentionally blind, and the solution depends on studying the behavior of the service and researching the relevant cryptographic properties.

---

## 1. Observe Function 2 First

The intended order is **Function 2 → Function 1**.

Function 2 accepts:

```text
Key
```

and returns:

```text
Ciphertext
```

The operation is:

```text
FLAG
  |
  v
 3DES
  |
  v
XOR with hidden IV
  |
  v
Ciphertext
```

Therefore:

```text
C2 = E(FLAG, K) XOR IV
```

The same hidden IV is used by Function 1.

The challenge uses the fixed weak key:

```text
E0E0E0E0F1F1F1F1
```

Use this key for Function 2 and record the resulting ciphertext.

---

## 2. Feed Function 2 Into Function 1

Now use the **Function 2 ciphertext itself as the plaintext input to Function 1**.

Function 1 accepts:

```text
Plaintext
Key
```

and performs:

```text
Plaintext
    XOR
   hidden IV
    |
    v
  3DES
    |
    v
Ciphertext
```

Therefore:

```text
C1 = E(P XOR IV, K)
```

Set:

```text
P = C2
```

where `C2` is the ciphertext obtained from Function 2.

Then:

```text
C1 = E(C2 XOR IV, K)
```

From Function 2:

```text
C2 = E(FLAG, K) XOR IV
```

Therefore:

```text
C2 XOR IV = E(FLAG, K)
```

So Function 1 produces:

```text
C1 = E(E(FLAG, K), K)
```

This is the key relationship between the two functions.

---

## 3. Analyze the Repeated-Key Construction

The service uses EDE-style 3DES:

```text
E_K(D_K(E_K(P)))
```

with:

```text
K1 = K2 = K3 = K
```

The middle decryption cancels the first encryption:

```text
D_K(E_K(P)) = P
```

so the construction reduces to:

```text
E_K(P)
```

In other words, the repeated-key 3DES construction behaves as a single DES encryption with the supplied key.

---

## 4. Investigate the DES Weak Key

The challenge uses the fixed weak DES key:

```text
E0E0E0E0F1F1F1F1
```

The relevant property is that encryption with this weak key is self-inverse:

```text
E_K(E_K(P)) = P
```

Applying that property to the result of Function 1 gives:

```text
C1 = E(E(FLAG, K), K)
```

and therefore:

```text
C1 = FLAG
```

The Function 1 ciphertext is consequently the recovered flag.

---

## 5. Complete Recovery Process

The intended two-query sequence is:

### Step 1 — Function 2

Use:

```text
Key:
E0E0E0E0F1F1F1F1
```

Record:

```text
C2 = Function 2 ciphertext
```

### Step 2 — Function 1

Use the Function 2 ciphertext as the plaintext:

```text
Plaintext:
<C2>
```

and use:

```text
Key:
E0E0E0E0F1F1F1F1
```

The resulting Function 1 ciphertext is:

```text
C1 = E(C2 XOR IV, K)
```

Since:

```text
C2 XOR IV = E(FLAG, K)
```

we get:

```text
C1 = E(E(FLAG, K), K)
```

Using the weak-key property:

```text
C1 = FLAG
```

---

## 6. Offline Recovery

The important part is that the player does **not** need to recover the hidden IV separately.

The two functions are deliberately chained together:

```text
Function 2
    |
    v
E(FLAG, K) XOR IV
    |
    v
Function 1
    |
    v
E((E(FLAG, K) XOR IV) XOR IV, K)
    |
    v
E(E(FLAG, K), K)
    |
    v
FLAG
```

The hidden value cancels naturally when the Function 2 ciphertext is passed into Function 1.

---

## 7. Final Flag

The recovered Function 1 ciphertext is the final CTF flag:

```text
CYS{th3_l@st_b@tCh_w@s_d1fF3r3nT_b@tch!}
```

Submit it through the challenge website.

---

## 8. Summary

| Stage                | Action                                         |
| -------------------- | ---------------------------------------------- |
| Function 2           | Submit `E0E0E0E0F1F1F1F1` and obtain `C2`      |
| Function 1           | Use `C2` as the plaintext with the same key    |
| Analyze construction | Recognize repeated-key 3DES as single DES      |
| Identify property    | Recognize the weak key's self-inverse behavior |
| Recover flag         | Function 1 ciphertext becomes the flag         |
| Submit               | Submit the recovered flag through the website  |

---

## Final Flag

```text
CYS{dynamic_flag}
```
