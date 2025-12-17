---
layout: writeup

title: Reconfiguration Terminal
difficulty: Medium
points: 500
categories: [General]
tags: []

flag: CYS{7h3_h0ur6l455_5h4773r3d_bu7_m3m0ry_r3m41n5_1n_fr46m3n75_pl3453_l1573n_cl053r_65537_2025}
---

# Reconfiguration Terminal

Category: Web Exploitation
Author: Yashwant Gokul P

## Challenge Description:

- The site is minimal but the hint “Numbers are truth…” suggests a numeric resource pattern; a quick, low-noise check of `robots.txt` confirmed a disallowed numeric path and pointed toward a `/safe/<id>` namespace. Manual requests to a few `/safe/<n>` pages returned single characters inside the HTML (200 for valid indices, 404 at the end), which indicates an information-disclosure/enumeration weakness — essentially a CTF-style IDOR/predictable resource issue. The logical next step is to automate sequential requests to `/safe/1`, `/safe/2`, …, parse each response for the character, and concatenate them to reconstruct the `CYS{...}` flag

## Solution:

### Initial Analysis:

- The site is minimal but the hint “Numbers are truth…” suggests a numeric resource pattern; a quick, low-noise check of `robots.txt` confirmed a disallowed numeric path and pointed toward a `/safe/<id>` namespace. Manual requests to a few `/safe/<n>` pages returned single characters inside the HTML (200 for valid indices, 404 at the end), which indicates an information-disclosure/enumeration weakness — essentially a CTF-style IDOR/predictable resource issue. The logical next step is to automate sequential requests to `/safe/1`, `/safe/2`, …, parse each response for the character, and concatenate them to reconstruct the `CYS{...}` flag.

### Tools Used:

- Python3

### **Step-by-Step Solution:**

1. You are given with a url [https://reconfiguration-terminal.netlify.app/](https://reconfiguration-terminal.netlify.app/)
    
    ![image.png](image.png)
    
2. The site looks minimal, and it even displays the line “Numbers are truth, and truth always leaks through the cracks,” hinting at a possible IDOR weakness and suggesting there could be hidden clues in the page source, cookies, or other client-side artifacts. A good next step is to check the site’s `robots.txt` (e.g., `https://example.com/robots.txt`). That file, located at a site’s root, tells crawlers which paths to index or avoid—so it’s often a quick way to discover hidden or disallowed endpoints that might reveal useful information.
    
    ![image.png](image%201.png)
    
3. We found something interesting in `robots.txt`: `Disallow: /safe/420`. That suggests the site might expose a hidden page and could indicate an IDOR (Insecure Direct Object Reference) issue. Let’s probe `/safe/1` to see whether the site is vulnerable.Our intuition paid off: changing the page ID (for example to `2` and `3`) returned `Y` and `S`, which matches the expected flag pattern. We don’t yet know the flag’s length, so manually visiting pages would be slow and error-prone. Instead, we’ll automate the process with a simple Python script that requests `/safe/<n>`, extracts the character from each page, and builds the flag for us.
    
    ![image.png](image%202.png)
    
4. Our intuition paid off: changing the page ID (for example to `2` and `3`) returned `Y` and `S`, which matches the expected flag pattern. We don’t yet know the flag’s length, so manually visiting pages would be slow and error-prone. Instead, we’ll automate the process with a simple Python script that requests `/safe/<n>`, extracts the character from each page, and builds the flag for us.
    
    ```python
    import requests
    from bs4 import BeautifulSoup
    
    BASE = "https://reconfiguration-terminal.netlify.app/safe/{}"
    flag = ""
    i = 1
    
    while True:
        url = BASE.format(i)
        r = requests.get(url)
    
        if r.status_code == 404:
            print("404 reached. Stopping.")
            break
        elif r.status_code == 200:
            # parse the HTML and get only the text inside <p>
            soup = BeautifulSoup(r.text, "html.parser")
            p = soup.find("p")
            if p:
                char = p.text.strip()
                flag += char
                print(f"Page {i} found. Flag so far: {flag}")
            else:
                print(f"Page {i} found but no <p> tag!")
    
        i += 1
    
    print("\nFinal Flag:", flag)
    
    ```
    
    chatgpt chat history : [https://chatgpt.com/share/68f10e84-a100-8003-b373-216bc62c34b0](https://chatgpt.com/share/68f10e84-a100-8003-b373-216bc62c34b0)
    
5. If we run this code on our system, it will automatically fetch all the pages and reveal the flag.
    
    ![image.png](image%203.png)
    

## Flag:

> CYS{7h3_h0ur6l455_5h4773r3d_bu7_m3m0ry_r3m41n5_1n_fr46m3n75_pl3453_l1573n_cl053r_65537_2025}
>