"""Vocalizes Hebrew text with Dicta's Nakdan (needs *.dicta.org.il in the allowed domains).

Usage: python3 nakdan.py "טקסט לניקוד"
Prints the vocalized line, then each word's top options.

Check the options before using the line: Dicta picks the masculine form for
second-person verbs by default (בָּחַרְתָּ, not בָּחַרְתְּ), and Michal's audience is women.
"""
import json
import sys
import urllib.request

API = "https://nakdan-2-0.loadbalancer.dicta.org.il/api"


def main():
    text = sys.argv[1]
    body = json.dumps({"task": "nakdan", "data": text, "genre": "modern"}).encode()
    req = urllib.request.Request(API, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        tokens = json.load(r)

    line, notes = [], []
    for t in tokens:
        if t["sep"] or not t["options"]:
            line.append(t["word"])
            continue
        opts = [o.replace("|", "") for o in t["options"]]
        line.append(opts[0])
        if len(opts) > 1:
            notes.append(f"{t['word']}: " + " / ".join(opts[:4]))

    print("".join(line))
    print()
    print("\n".join(notes))


if __name__ == "__main__":
    main()
