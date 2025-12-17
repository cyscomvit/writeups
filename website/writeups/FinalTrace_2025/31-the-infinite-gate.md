---
layout: writeup

title: The Infinite Gate
difficulty: Medium
points: 500
categories: [Web]
tags: []

flag: CYS{c00k1eS_ar3_m34nt_t0_b3_br0k3n}
---

## The Infinite Gate

- **Category**: Web
- **Author**: Aadhyanth

## Challenge Description

Hark, seeker of the Inner Sanctum! Before thee looms the Infinite Gate, an edifice not wrought by mortal hands, but sung into existence from the very stone of eternity. Its Guardian, ancient beyond reckoning, permits none to pass save those deemed worthy. Upon presenting thy claim, a fragment of thy very essence - thy digital soul-print, if you will - is etched by the Gate's magic. This token, unseen yet potent, marks thee as either Guest or... something more.

The mechanism of this ward is steeped in the forgotten lore of Elara the Astromancer. She who mapped the celestial curves believed that identity itself could be represented, measured, perhaps even... altered. It is said the Gate judges not the strength of thy arm nor the purity of thy heart, but the subtle quality of the essence-token it bestows upon thee.

The Guardian speaks true: a pass is merely a token. Can such a thing, once given, be reshaped by mortal will? Can simple wit suffice where might fails? Approach the Gate, receive thy mark, and discover if thou possess the wit to bend its ancient, rigid judgment to thy purpose. The Inner Sanctum awaits only those who can prove their essence is more than what the Gate initially perceives.

### Tools Used

- Devtools
- Python

### Step-by-Step Solution

#### Step 1:

Open devtools (F12) view cookies under the Application tab and log in with any username and password

#### Step 2:

Alter the UserCunning cookie from false to true and move to the next page

#### Step 3: [Step Title]

Copy the given json file and decrypt using Elliptic-Curve Cryptography

```python
import json

def solve_challenge():
    """
    Loads challenge.json, solves the ECC challenge, and prints the flag.
    """
    print("Loading challenge.json...")
    try:
        with open('challenge.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: challenge.json not found in the same directory.")
        return
    except json.JSONDecodeError:
        print("Error: Could not decode challenge.json.")
        return

    p = data["p"]
    a = data["a"]
    b = data["b"]
    xs_hex = data["xs_hex"]
    flag_bits_len = data["flag_bits_len"]

    # The p % 8 check is no longer relevant
    # if p % 8 != 5:
    #     print(f"Warning: Prime p % 8 is not 5 (it's {p % 8}).")
    #     print("The mod_sqrt function may not be optimal, but let's proceed.")

    print(f"Loaded curve parameters and {len(xs_hex)} x-coordinates.")

    bit_string = ""

    for i, x_hex in enumerate(xs_hex):
        x = int(x_hex, 16)

        # Calculate y^2 = x^3 + ax + b (mod p)
        # We use pow(x, 3, p) for (x^3 % p)
        x3 = pow(x, 3, p)
        ax = (a * x) % p

        # Ensure intermediate results stay positive
        y_squared = (x3 + ax + b) % p
        if y_squared < 0:
            y_squared += p

        # --- MODIFIED LOGIC ---
        # The error "No modular square root" indicates that y^2 is not
        # always a quadratic residue. This implies the flag bit is
        # encoded in the *existence* of a root, not its value.
        # We check this using the Legendre symbol.

        # legendre = pow(y_squared, (p - 1) // 2, p)
        #
        # legendre == 1  => y^2 is a quadratic residue (y exists, y != 0)
        # legendre == p - 1 => y^2 is a quadratic non-residue (y does not exist)
        # legendre == 0  => y^2 is 0 (y = 0)

        legendre_symbol = pow(y_squared, (p - 1) // 2, p)

        # Hypothesis: Bit is 1 if it's a residue, 0 otherwise.
        # We treat the y=0 case (legendre_symbol == 0) as bit 0,
        # as the LSB of y=0 would be 0.
        if legendre_symbol == 1:
            bit_string += "1"
        else:
            # This covers non-residues (p-1) and the y=0 case (0)
            bit_string += "0"

        # --- END MODIFIED LOGIC ---

    print(f"Successfully generated {len(bit_string)} bits.")

    if len(bit_string) != flag_bits_len:
        print(f"Error: Expected {flag_bits_len} bits, but got {len(bit_string)}.")
        return

    # Convert the full bit string into bytes
    try:
        flag_bytes = bytearray()
        for i in range(0, flag_bits_len, 8):
            byte_str = bit_string[i:i+8]
            byte_val = int(byte_str, 2)
            flag_bytes.append(byte_val)

        # Decode the bytes as an ASCII string
        flag = flag_bytes.decode('ascii')
        print("\n--- FLAG ---")
        print(flag)
        print("--------------")

    except UnicodeDecodeError:
        print("\nError: Could not decode the resulting bytes into ASCII.")
        print(f"Raw bytes: {flag_bytes.hex()}")
    except Exception as e:
        print(f"\nAn error occurred during flag decoding: {e}")

if __name__ == "__main__":
    solve_challenge()


```

The above is working code that you can easily get through prompt engineering

### Flag

```
CYS{c00k1eS_ar3_m34nt_t0_b3_br0k3n}
```
