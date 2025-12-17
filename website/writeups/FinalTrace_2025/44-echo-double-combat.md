---
layout: writeup

title: Echo-Double Combat
difficulty: Medium
points: 500
categories: [Reverse Engineering]
tags: []

flag: cys{s3cr3t_1s_un10cked}
---

## Echo-Double Combat

- **Category**: Reverse Engineering
- **Author**: Suraj Kumar

## Challenge Description
A binary executable accepts a 9-character input key and validates it through XOR operations. The correct key is encoded in the binary and must be extracted by XORing stored bytes with `0x55`. Once the correct key is entered, the binary decrypts and reveals the flag using repeating-key XOR. A decoy flag is stored in encrypted form as a Base64 string (`WTNsemUyY3dYMkkwWTJ0ZmREQmZjM1EwY25SemZRPT0=`) in the binary's strings, which decodes to `cys{g0_b4ck_t0_st4rts}` — this is intentionally wrong and serves as a red herring.

## Solution

### Initial Analysis
Running basic reconnaissance on the binary revealed an encrypted decoy flag in the strings output. Further analysis required disassembling the binary to understand the validation logic and extract the encoded key array used for XOR operations.

### Tools Used
- Ghidra / IDA Pro / Binary Ninja
- strings, file, objdump, readelf
- Python 3
- base64 (command-line tool)
- GCC

### Step-by-Step Solution

#### Step 1: Initial Analysis
```bash
file challenge.dat
strings challenge.dat
```
Found a Base64-encoded string `WTNsemUyY3dYMkkwWTJ0ZmREQmZjM1EwY25SemZRPT0=`. Decoding it twice reveals `cys{g0_b4ck_t0_st4rts}` which is a decoy flag (intentionally wrong). The binary requires a 9-character key as input.

#### Step 2: Decode the Decoy (Red Herring)
```bash
echo "WTNsemUyY3dYMkkwWTJ0ZmREQmZjM1EwY25SemZRPT0=" | base64 -d | base64 -d
# Output: cys{g0_b4ck_t0_st4rts}
```
This decoy flag is not the answer and will fail if used as input. It exists to mislead players who rely only on strings output.

#### Step 3: Extract Encoded Arrays from Binary
```bash
objdump -s -j .data challenge.dat
# or
readelf -x .data challenge.dat
```
Located two arrays in the `.data` section:
```
key_enc:  34 39 3a 3d 3a 38 3a 27 34
flag_enc: 12 5f 0c 1a 5c 19 30 43 12 3e 19 01 59 5f 0e 04 17 05
```

#### Step 4: Analyze Validation Logic in Disassembler
Opened the binary in Ghidra and decompiled the `main` function. Identified the key derivation and validation:
```c
unsigned char key[9];
for (int i = 0; i < 9; i++) {
    key[i] = key_enc[i] ^ 0x55;
}

if (memcmp(input, key, 9) == 0) {
    for (int i = 0; i < 18; i++) {
        flag[i] = flag_enc[i] ^ key[i % 9];
    }
}
```

#### Step 5: Compute the Real Key
```python
key_enc = bytes.fromhex('34393a3d3a383a2734')
key = bytes(b ^ 0x55 for b in key_enc)
print(key.decode())  # Output: alohomora
```
The real key is: `alohomora`

#### Step 6: Decrypt the Flag
```python
flag_enc = bytes.fromhex('125f0c1a5c193043123e1901595f0e041705')
key = b'alohomora'
flag = bytes(flag_enc[i] ^ key[i % 9] for i in range(len(flag_enc)))
print(flag.decode())  # Output: s3cr3t_1s_un10cked
```

#### Step 7: Verify and Retrieve Flag
```bash
./challenge.dat
Speak the binding spell: alohomora
Flag: cys{s3cr3t_1s_un10cked}
```
Successfully retrieved the real flag by entering the correct key.
### Python solver script


### Flag
```
cys{s3cr3t_1s_un10cked}
```


### solver python code
the code could change for new binary file as hex dump locations might change

```python
def extract_data_from_binary(filename='l'):
    """Extract data from the binary file"""
    try:
        with open(filename, 'rb') as f:
            data = f.read()
        
        print(f"[+] File size: {len(data)} bytes (0x{len(data):x})")
        
        # The addresses are 0x404060 and 0x404070
        # We need to find the file offset for these virtual addresses
        
        # Common data section offsets to try
        possible_offsets = [
            0x3060,  # 0x404060 - 0x401000 (common base)
            0x2060,  # Alternative
            0x4060,  # Alternative (if base is 0x400000)
            0x3040,  # Another common offset
        ]
        
        for base_offset in possible_offsets:
            offset_60 = base_offset
            offset_70 = base_offset + 0x10
            
            if offset_60 + 9 <= len(data) and offset_70 + 18 <= len(data):
                data_404060 = data[offset_60:offset_60+9]
                data_404070 = data[offset_70:offset_70+18]
                
                print(f"\n[*] Trying base offset: 0x{base_offset:04x}")
                print(f"    data_404060 (offset 0x{offset_60:04x}): {data_404060.hex()}")
                print(f"    data_404070 (offset 0x{offset_70:04x}): {data_404070.hex()}")
                
                # Try to decode and check if it makes sense
                result = solve_with_data(data_404060, data_404070)
                if result and result['valid']:
                    return result
        
        # If nothing worked, try scanning the file
        print("\n[*] Trying to scan entire file for valid patterns...")
        return scan_for_data(data)
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return None
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def scan_for_data(data):
    """Scan the file for potential encoded data"""
    print("[*] Scanning for 9-byte sequences that decode to printable ASCII...")
    
    candidates = []
    for i in range(len(data) - 9):
        # Try XORing with 0x55
        spell = bytearray()
        valid = True
        for j in range(9):
            char = data[i+j] ^ 0x55
            if char < 0x20 or char > 0x7e:  # Not printable ASCII
                valid = False
                break
            spell.append(char)
        
        if valid:
            spell_str = spell.decode('ascii')
            print(f"    Found at offset 0x{i:04x}: {spell_str}")
            candidates.append((i, data[i:i+9]))
    
    if candidates:
        print(f"\n[*] Found {len(candidates)} candidate(s)")
        # Use the first candidate
        offset, data_404060 = candidates[0]
        # Look for data_404070 nearby (16 bytes after)
        data_404070 = data[offset+16:offset+16+18] if offset+16+18 <= len(data) else None
        
        if data_404070:
            print(f"[*] Using data at offset 0x{offset:04x}")
            return solve_with_data(data_404060, data_404070)
    
    return None

def solve_with_data(data_404060, data_404070):
    """Solve the challenge with extracted data"""
    
    # Step 1: Calculate the spell (key)
    # var_1d[i] = data_404060[i] ^ 0x55
    spell = bytearray()
    for i in range(9):
        spell.append(data_404060[i] ^ 0x55)
    
    print(f"\n[+] Calculated Spell:")
    print(f"    Hex: {spell.hex()}")
    
    # Try to decode as ASCII
    try:
        spell_str = spell.decode('ascii')
        print(f"    ASCII: {spell_str}")
        is_printable = all(32 <= b <= 126 for b in spell)
    except:
        spell_str = spell.decode('ascii', errors='replace')
        print(f"    ASCII (with errors): {spell_str}")
        is_printable = False
    
    # Step 2: Decode the flag (Mirror Key)
    # var_88[i] = var_1d[i % 9] ^ data_404070[i]
    flag = bytearray()
    for i in range(18):
        flag.append(spell[i % 9] ^ data_404070[i])
    
    print(f"\n[+] Decoded Mirror Key:")
    print(f"    Hex: {flag.hex()}")
    
    # Try to decode as ASCII
    try:
        flag_str = flag.decode('ascii')
        print(f"    ASCII: {flag_str}")
        flag_printable = all(32 <= b <= 126 for b in flag)
    except:
        flag_str = flag.decode('ascii', errors='replace')
        print(f"    ASCII (with errors): {flag_str}")
        flag_printable = False
    
    print(f"\n{'='*60}")
    print(f"SOLUTION:")
    print(f"{'='*60}")
    print(f"Ancient Spell to Enter: {spell_str}")
    print(f"Mirror Key (Flag): {flag_str}")
    print(f"{'='*60}\n")
    
    return {
        'spell': spell_str,
        'flag': flag_str,
        'valid': is_printable and flag_printable
    }

def manual_solve():
    """Manual solver - paste your hex data here"""
    print("="*60)
    print("MANUAL MODE")
    print("="*60)
    print("Enter the hex data from the binary\n")
    print("To get the data manually, use:")
    print("  readelf -x .data l")
    print("  or")
    print("  objdump -s -j .data l")
    print()
    
    data_404060_hex = input("Enter data_404060 (9 bytes in hex, e.g., 1a2b3c...): ").strip()
    data_404070_hex = input("Enter data_404070 (18 bytes in hex, e.g., 4d5e6f...): ").strip()
    
    try:
        # Remove spaces and common separators
        data_404060_hex = data_404060_hex.replace(" ", "").replace("0x", "")
        data_404070_hex = data_404070_hex.replace(" ", "").replace("0x", "")
        
        data_404060 = bytes.fromhex(data_404060_hex)
        data_404070 = bytes.fromhex(data_404070_hex)
        
        if len(data_404060) != 9:
            print(f"Error: data_404060 should be 9 bytes, got {len(data_404060)}")
            return
        
        if len(data_404070) != 18:
            print(f"Error: data_404070 should be 18 bytes, got {len(data_404070)}")
            return
        
        print()
        solve_with_data(data_404060, data_404070)
        
    except ValueError as e:
        print(f"Error parsing hex: {e}")

def main():
    import sys
    
    print("="*60)
    print("Echo-Double Challenge Solver")
    print("="*60)
    print()
    
    # Get filename
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'l'
    
    # Try automatic extraction first
    print(f"[*] Attempting automatic data extraction from '{filename}'...\n")
    result = extract_data_from_binary(filename)
    
    if not result:
        print("\n" + "="*60)
        print("Automatic extraction failed. Switching to manual mode...")
        print("="*60)
        print()
        manual_solve()

if __name__ == "__main__":
    main()
```