---
layout: writeup

title: Breaking Bad Broadcast
difficulty: Easy
points: 200
categories: [crypto]
tags: []

flag: CYS{h313nh3rg_bl3_sky_br0adcast}
---


## 1. Extract the Challenge Files

First, extract the provided `Operation_Kingpin.zip` archive:

```bash
unzip Operation_Kingpin.zip
```

The extracted directory contains:

- `README.txt`
- `madrigal_vault.zip`
- `burner_phone.txt`

---

## 2. Read the Challenge Instructions

Read the contents of `README.txt`:

```bash
cat README.txt
```

The README provides the instructions and hints required to proceed with the challenge.

---

## 3. Decode the Burner Phone Message

The `burner_phone.txt` file contains a Base64-encoded message.

```bash
cat burner_phone.txt
```

The encoded value can be decoded using a Base64 decoder. The decoded value is:

```text
LOS-POLLOS-HERMANOS-99PERCENT
```

This recovered value is used as the password for the encrypted archive.

---

## 4. Extract the Encrypted Madrigal Vault

Use `7z` to extract the encrypted archive:

```bash
7z x madrigal_vault.zip
```

When prompted for the password, enter:

```text
LOS-POLLOS-HERMANOS-99PERCENT
```

The archive is successfully extracted.

---

## 5. Inspect the Extracted Data

Navigate into the extracted directory:

```bash
cd madrigal_vault
ls
```

Inspect the recovered data-drop files:

```bash
cat drop_albuquerque.dat
cat drop_albuquerque.pub
cat drop_elpaso.pub
cat drop_elpaso.pub
cat drop_houston.pub
cat drop_houston.pub
```

The files contain large hexadecimal values required for the next stage.

---

## 6. Run the Solver

Run the provided solver:

```bash
python3 solver.py
```

The solver processes the recovered values and applies the required mathematical reconstruction, including the Chinese Remainder Theorem, to recover the hidden flag.

---

## 7. Flag

The recovered flag is:

```text
CYS{h313nh3rg_bl3_sky_br0adcast}
```

## Conclusion

The challenge was solved through the following sequence:

**ZIP Extraction → README Analysis → Base64 Decoding → Password Recovery → Encrypted Archive Extraction → Data-Drop Analysis → Solver Execution → Flag Recovery**
