"""Inventory every XCCDF STIG under a folder.

Usage: python stigs.py <folder>

Writes <folder>/stigs.json with, for each STIG: file, title, version, release
line (release and benchmark date), rule counts by severity, rule-ID prefixes,
and every rule (ID, severity, SRG ID, title, fix text). Prints a one-line
summary per STIG.
"""
import collections
import glob
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

NS = {"x": "http://checklists.nist.gov/xccdf/1.1"}
root_dir = sys.argv[1]
out = []
for f in sorted(glob.glob(os.path.join(root_dir, "**", "*xccdf*.xml"), recursive=True)):
    r = ET.parse(f).getroot()
    release = next((p.text.strip() for p in r.findall("x:plain-text", NS)
                    if p.get("id") == "release-info" and p.text), "")
    rules = []
    for g in r.findall("x:Group", NS):
        ru = g.find("x:Rule", NS)
        fix = ru.find("x:fixtext", NS)
        rules.append({
            "srg": g.find("x:title", NS).text.strip(),
            "id": ru.find("x:version", NS).text.strip(),
            "sev": ru.get("severity"),
            "title": re.sub(r"\s+", " ", ru.find("x:title", NS).text.strip()),
            "fix": (fix.text or "").strip() if fix is not None else "",
        })
    sev = collections.Counter(x["sev"] for x in rules)
    out.append({
        "file": os.path.basename(f),
        "title": r.find("x:title", NS).text.strip(),
        "version": r.find("x:version", NS).text.strip(),
        "release": release,
        "count": len(rules), "high": sev["high"], "medium": sev["medium"], "low": sev["low"],
        "prefix": sorted({re.sub(r"-\d+$", "", x["id"]) for x in rules}),
        "rules": rules,
    })
with open(os.path.join(root_dir, "stigs.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1)
for s in out:
    print(f'{s["title"]} | V{s["version"]} | {s["release"]} | '
          f'{s["count"]} ({s["high"]}/{s["medium"]}/{s["low"]}) | {",".join(s["prefix"])}')
print(f"{len(out)} STIGs, {sum(s['count'] for s in out)} rules")
