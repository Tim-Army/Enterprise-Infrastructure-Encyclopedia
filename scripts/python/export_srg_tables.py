#!/usr/bin/env python3
"""Export the SRG tables of Volume CLXXII's product map chapters to CSV.

For every chapter matching volumes/volume-172-disa-srgs-and-stigs/chapters/
NN-*-feature-version-and-s*-map.md, this script:

- writes the feature map table to data/<chapter>-feature-map.csv and the
  requirement reference table to data/<chapter>-requirements.csv (UTF-8 with a
  byte-order mark, so spreadsheet programs show dashes and quotes correctly);
- inserts, or refreshes, a download link on the line before each table.

The links point at the published Pages portal, because the HTML and EPUB
builds do not rewrite relative links to non-Markdown files.
scripts/bash/build-download-site.sh copies volumes/*/data/*.csv into the
portal at data/<volume>/.

Run it from the repository root after changing any of these tables:

    python scripts/python/export_srg_tables.py
"""
import csv
import glob
import os
import re

VOLUME = "volume-172-disa-srgs-and-stigs"
PORTAL = "https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia"
TABLES = [
    # (heading prefix, csv suffix, link text)
    ("### The ", "feature-map", "Download the feature map as CSV"),
    ("### Requirement reference", "requirements", "Download the requirement reference as CSV"),
]
LINK_RE = re.compile(r"^\[Download the (?:feature map|requirement reference) as CSV\]\(")


def split_row(line):
    body = line.strip().removeprefix("|").removesuffix("|")
    cells = re.split(r"(?<!\\)\|", body)
    return [plain(c.strip().replace("\\|", "|")) for c in cells]


def plain(cell):
    cell = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cell)   # links -> text
    cell = cell.replace("**", "")
    return cell.replace("`", "")


def process(path):
    stem = os.path.basename(path)[:-3]
    lines = open(path, encoding="utf-8").read().split("\n")
    out, i, written = [], 0, []
    heading = None
    while i < len(lines):
        line = lines[i]
        if line.startswith("### "):
            heading = next((t for t in TABLES if line.startswith(t[0])), None)
        if LINK_RE.match(line):
            # drop an old link (and the blank line after it); it is re-added below
            i += 1
            if i < len(lines) and lines[i] == "":
                i += 1
            continue
        if heading and line.startswith("| ") and i + 1 < len(lines) and lines[i + 1].startswith("| ---"):
            _, suffix, text = heading
            rows, j = [], i
            while j < len(lines) and lines[j].startswith("|"):
                if not lines[j].startswith("| ---"):
                    rows.append(split_row(lines[j]))
                j += 1
            name = f"{stem}-{suffix}.csv"
            os.makedirs(f"volumes/{VOLUME}/data", exist_ok=True)
            with open(f"volumes/{VOLUME}/data/{name}", "w", encoding="utf-8-sig", newline="") as fh:
                csv.writer(fh).writerows(rows)
            written.append((name, len(rows) - 1))
            out.append(f"[{text}]({PORTAL}/data/{VOLUME}/{name}) ({len(rows) - 1} rows).")
            out.append("")
            out.extend(lines[i:j])
            i = j
            heading = None
            continue
        out.append(line)
        i += 1
    new = "\n".join(out)
    if new != "\n".join(lines):
        open(path, "w", encoding="utf-8", newline="\n").write(new)
    return written


def main():
    for path in sorted(glob.glob(f"volumes/{VOLUME}/chapters/*-feature-version-and-s*-map.md")):
        for name, n in process(path):
            print(f"{name}: {n} rows")


if __name__ == "__main__":
    main()
