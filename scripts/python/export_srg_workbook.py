#!/usr/bin/env python3
"""Export the FortiSwitch SRG mapping workbook to CSV files and an interactive page.

Reads the workbook saved in volumes/volume-201-fortiswitch-stig-and-srg-mapping/data/ and writes:

- three CSV files beside it (UTF-8 with a byte-order mark and CRLF line ends, like
  the CSV files that export_srg_tables.py writes):
    01-fortiswitch-srg-workbook-crosswalk.csv      sheet "Fortiswitch vs Cisco"
    01-fortiswitch-srg-workbook-prerequisites.csv  sheet "Prerequisites"
    01-fortiswitch-srg-workbook-model-support.csv  sheet "Model Support 7.6.7"
- publishing/interactive/fortiswitch-srg-crosswalk.html, a self-contained,
  offline page with a searchable, sortable, filterable table for each sheet.

scripts/bash/build-download-site.sh copies the CSV files to the portal at
data/<volume>/ and the page to interactive/.

Needs openpyxl (pip install openpyxl). Run it from the repository root after
the workbook changes:

    python scripts/python/export_srg_workbook.py [--workbook PATH] [--date YYYY-MM-DD]
"""
import argparse
import csv
import datetime
import json
import os

import openpyxl

VOLUME = "volume-201-fortiswitch-stig-and-srg-mapping"
DATA = os.path.join("volumes", VOLUME, "data")
DEFAULT_WORKBOOK = os.path.join(DATA, "01-fortiswitch-feature-version-and-srg-map-feature-map-20261103.xlsx")
TEMPLATE = os.path.join("scripts", "python", "srg_workbook_page.html.tpl")
PAGE = os.path.join("publishing", "interactive", "fortiswitch-srg-crosswalk.html")

# (key in the page data, worksheet name, CSV file name)
SHEETS = [
    ("crosswalk", "Fortiswitch vs Cisco", "01-fortiswitch-srg-workbook-crosswalk.csv"),
    ("prerequisites", "Prerequisites", "01-fortiswitch-srg-workbook-prerequisites.csv"),
    ("model", "Model Support 7.6.7", "01-fortiswitch-srg-workbook-model-support.csv"),
]


def text(value):
    if value is None:
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def read_sheet(ws):
    rows = [[text(c) for c in row] for row in ws.iter_rows(values_only=True)]
    width = max((i + 1 for r in rows for i, c in enumerate(r) if c), default=0)
    rows = [r[:width] + [""] * (width - len(r)) for r in rows]
    while rows and not any(rows[-1]):
        rows.pop()
    return rows[0], [r for r in rows[1:] if any(r)]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--workbook", default=DEFAULT_WORKBOOK)
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    args = ap.parse_args()

    wb = openpyxl.load_workbook(args.workbook, read_only=True, data_only=True)
    data = {}
    for key, sheet, csv_name in SHEETS:
        columns, rows = read_sheet(wb[sheet])
        data[key] = {"columns": columns, "rows": rows}
        path = os.path.join(DATA, csv_name)
        with open(path, "w", encoding="utf-8-sig", newline="") as fh:
            writer = csv.writer(fh)
            writer.writerow(columns)
            writer.writerows(rows)
        print(f"wrote {path}: {len(rows)} rows, {len(columns)} columns")

    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    page = open(TEMPLATE, encoding="utf-8").read()
    page = (page.replace("__DATA__", payload)
                .replace("__SOURCE__", os.path.basename(args.workbook))
                .replace("__GENERATED__", args.date)
                .replace("__CSV_CROSSWALK__", SHEETS[0][2])
                .replace("__CSV_PREREQ__", SHEETS[1][2])
                .replace("__CSV_MODEL__", SHEETS[2][2]))
    with open(PAGE, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(page)
    print(f"wrote {PAGE} ({len(page) // 1024} KB)")


if __name__ == "__main__":
    main()
