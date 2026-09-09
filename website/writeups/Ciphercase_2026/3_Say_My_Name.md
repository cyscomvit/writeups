---
layout: writeup

title: Blindside
difficulty: Medium
points: 300
categories: [Forensics / Network + Cryptography + Steganography]
tags: []

flag: CYS{s4y_my_n4m3_h315enb3rg}
---

Blindside

Author : P S Suraj Kumar 

A single pcap, two carrier flows, three hiding spots for the flag, and a
decoy zip entry to punish anyone who just greps for `CYS{`. Nothing here
needs the Wireshark GUI — tshark covers every step, and the point of the
challenge was to make sure a headless box could still solve it.

## What's actually going on

The "evidence file" leaves the network in two pieces over two different
protocols: half over a plain HTTP GET, the rest hours later over FTP-DATA,
same two hosts both times. That split alone is a mild evasion trick
against anyone only watching one flow. The FTP control channel logs in
with a cleartext password, which turns out to double as the zip password
later — reusing credentials across services is basically a running joke
in these captures.

Once you glue the two halves back together you get a normal-looking PDF,
except it keeps going well past its own `%%EOF`. That tail is a zip file
XOR'd with a single byte, so `file` and `binwalk` just see noise instead
of `PK\x03\x04`. Inside the zip, three files: two images and a readme.
The readme has a flag-shaped string in it. It's wrong. Ignore it.

The real flag is split across the two images and the zip's own comment
field, each one hidden with a different trick — EXIF metadata, LSB
steganography, and the archive comment (which, notably, isn't encrypted
at all and doesn't need the password).

## Pulling it apart

Start with the conversations to see what's even in the capture:

```
tshark -r capture.pcapng -q -z conv,tcp
```

Three TCP streams show up: HTTP on port 80, FTP control on 21, FTP-DATA
on 20, all between the same pair of hosts, with the FTP pair kicking off
about eight seconds after HTTP wraps up. That's the "hours apart" from
the flavor text, compressed for the sake of not making people wait
around.

Grab the HTTP body without touching a GUI:

```
tshark -r capture.pcapng --export-objects http,./httpobjs
```

For the FTP-DATA half, find the right stream and follow it raw:

```
tshark -r capture.pcapng -Y "ftp-data" -T fields -e tcp.stream | sort -u
tshark -r capture.pcapng -q -z follow,tcp,raw,<stream id>
```

Stick the HTTP body and the FTP-DATA payload together in that order and
you get back the original PDF. The password, while you're in there, is
sitting in plaintext on the control channel:

```
tshark -r capture.pcapng -Y "ftp.request.command==PASS" -T fields -e ftp.request.arg
```

That gives `1_Am_The_Danger_99` — worth remembering, it comes back later.

The PDF itself is fine right up to `%%EOF`. Everything after that is
high-entropy garbage with no file magic, which is the usual tell for "XOR
this." Only 256 keys to try, so just brute force it looking for a decoded
`PK\x03\x04`. Key turns out to be `0x37`.

Before doing anything else with the recovered zip, check its comment —
it costs nothing and doesn't need a password:

```
unzip -z recovered.zip
```

That's one third of the flag, sitting right there. Then unlock the rest:

```
unzip -P '1_Am_The_Danger_99' recovered.zip
```

which drops `part1_carrier.jpg`, `part2_carrier.png`, and the decoy
`readme.txt`. `exiftool` on the jpeg pulls the `UserComment` field
straight out — that's part one. The png doesn't have anything visible
sitting on top; it's LSB steganography, least significant bit of each RGB
channel in raster order, first 32 bits are a length header in bytes, rest
is the message.

Once you've got all three pieces, the ordering isn't really a puzzle —
one starts with `CYS{`, one ends with `}`, so there's only one way they
fit together.

## Solver

```python
#!/usr/bin/env python3
"""Solver for 'Say My Name'. Usage: python3 solve.py capture.pcapng"""
import sys, zipfile, io
from scapy.all import rdpcap, TCP, Raw
from PIL import Image
import piexif

def main(pcap_path):
    pkts = rdpcap(pcap_path)

    http_data = b""
    for p in pkts:
        if TCP in p and Raw in p and p[TCP].sport == 80:
            http_data += bytes(p[Raw])
    sep = http_data.find(b"\r\n\r\n")
    part1_net = http_data[sep + 4:]

    part2_net = b""
    for p in pkts:
        if TCP in p and Raw in p and p[TCP].sport == 20:
            part2_net += bytes(p[Raw])

    combined = part1_net + part2_net

    ftp_ctrl = b""
    for p in pkts:
        if TCP in p and Raw in p and (p[TCP].sport == 21 or p[TCP].dport == 21):
            ftp_ctrl += bytes(p[Raw])
    pass_line = next(l for l in ftp_ctrl.split(b"\r\n") if l.startswith(b"PASS "))
    zip_password = pass_line.split(b" ", 1)[1].decode()

    eof = combined.find(b"%%EOF")
    tail = combined[eof + len(b"%%EOF") + 1:]

    key = next(k for k in range(256)
               if bytes(b ^ k for b in tail[:4]) == b"PK\x03\x04")
    zip_bytes = bytes(b ^ key for b in tail)

    zf = zipfile.ZipFile(io.BytesIO(zip_bytes))
    part3 = zf.comment.decode()

    zf.setpassword(zip_password.encode())
    jpg_bytes = zf.read("part1_carrier.jpg")
    with open("/tmp/_part1.jpg", "wb") as f:
        f.write(jpg_bytes)
    exif = piexif.load("/tmp/_part1.jpg")
    uc = exif["Exif"][piexif.ExifIFD.UserComment]
    part1 = uc[8:].decode() if uc[:5] == b"ASCII" else uc.decode()

    png_bytes = zf.read("part2_carrier.png")
    img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    pixels = list(img.getdata())
    bits = "".join(str(ch & 1) for px in pixels for ch in px)
    length = int(bits[:32], 2)
    msg_bits = bits[32:32 + length * 8]
    msg_bytes = bytes(int(msg_bits[i:i+8], 2) for i in range(0, len(msg_bits), 8))
    part2 = msg_bytes.decode()

    print("part1:", part1)
    print("part2:", part2)
    print("part3:", part3)
    print("flag: ", part1 + part2 + part3)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "capture.pcapng")
```

Needs `pip install scapy Pillow piexif --break-system-packages`.

## Loose ends

- `readme.txt` carries a fake flag with the old `CYSCOM{...}` prefix —
  this event's flags all use the shorter `CYS{...}` format, so it's also
  a trap for people running a blind regex over everything they find.
- The "you are goddamn right" line in the cover memo is just flavor —
  it echoes the FTP/zip password (`1_Am_The_Danger_99`) but doesn't hold
  any part of the flag. Don't spend time trying to extract something from
  it.
- Re-solved the whole thing from a clean capture using nothing but
  tshark, scapy, and PIL to make sure nobody actually needs Wireshark's
  desktop app open to get through this.
