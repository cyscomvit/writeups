---
layout: writeup

title: It ain't here
level:
difficulty: hard
points: 500
categories: [Reverse engineering]
tags: []

flag: CBCV{b07faa19997299630d615b1a9579d64f}
---
### It ain't here

* Author: Aakansh Gupta (Unknown)

Lets first run the file and its properties

```bash
┌──(kali㉿kali)-[~/Desktop/Cyscom/6]
└─$ ./challenge.run
Verifying archive integrity...  100%   MD5 checksums are OK. All good.
Uncompressing It ain't here  100%  
Can you really break the pincode? ...
Try if you must: 
```

Entering any wrong pin shows bad pin and exits the program. What we can try is "Keyboard Interrupt In Linux" by pressing ctrl+c during execution. This shows us the location of the executing python script.

```bash
Can you really break the pincode? ...
Try if you must: ^CTraceback (most recent call last):
  File "/tmp/selfgz116517/./pin_checker.py", line 105, in <module>
    main()
  File "/tmp/selfgz116517/./pin_checker.py", line 82, in main
    pin = input("Try if you must: ")
KeyboardInterrupt
Signal caught, cleaning up
```

But visiting it after execution shows nothing. So we try and access it while executing the program. Here we find a python file with tons of flags.

But what we need is the flag from this function:

```python
{% raw %}
def generate_real_flag(pin):
    FLAG_PREFIX =  "CBCV{%s}"

    hashed_pin = hashlib.blake2b((pin + "blindinglights").encode("utf-8")).hexdigest()[:32]
    return FLAG_PREFIX % hashed_pin
{% endraw %}
```

This is called when entered pin is 98315. Use this to get the correct flag with the program.

```python
if pin == "98315":
        print("Looks good to me...")
        print("I guess I'll generate a flag")

        try:
            req = requests.get("http://example.com", timeout=2)
            req.raise_for_status()
        except requests.exceptions.RequestException:
            print("Warning: Could not verify secondary network status.")

     
        real_flag = generate_real_flag(pin)
        print(real_flag)

    else:
        print("Bad pin!")
```

<img src="./images/aint.png" />


### The flag found is:
## CBCV{b07faa19997299630d615b1a9579d64f}
