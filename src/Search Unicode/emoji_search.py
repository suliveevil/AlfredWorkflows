#!/usr/bin/python3

"""
Search for Unicode 12.1 Emoji Descriptions

uni binary from: https://github.com/arp242/uni
Twemoji updated to 12.1.4
"""

import sys
import re
import subprocess
import json
import csv
from pathlib import Path

if len(sys.argv) >= 2:
    query = sys.argv[1]

    try:
        out: str = subprocess.check_output(
            ["./uni", "-q", "emoji", query, "-f", "%(emoji q),%(name q),%(group q),%(subgroup q),%(cpoint q),%(cldr q)"]).decode()

        out = out.strip().splitlines()
        out = list(csv.reader(out, quotechar="'"))
    except subprocess.CalledProcessError:
        out = []

else:
    out = []

data = []

for i in out[:20]:
    char, name, cat, sub_cat, cpoint, cldr = i
    name = name.title()
    lookup_sequence = cpoint.replace("U+", "").replace(" ", "-").replace("-FE0F", "")

    p = Path(f"twemoji/{lookup_sequence}.png")
    if p.exists():
        icon_path = str(p)
    else:
        icon_path = "emoji.png"

    data.append({
        "uid": f"emoji_{lookup_sequence}",
        "title": f"{char} — {name}",
        "subtitle": f"{cpoint}: {cat}, {sub_cat}, {cldr}",
        "arg": char,
        "text": {
            "copy": char,
            "largetype": char
        },
        "icon": {
            "path": icon_path
        }
    })

json.dump({"items": data}, sys.stdout)
