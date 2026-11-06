#!/usr/bin/env python3
"""Keep the manifest embedded in the Lab Builder page in step with lab201-vms.json.

Usage: sync_lab_builder.py [--check]

The Lab Builder page (volume 201, lab-scripts/builder/lab-builder.html) carries a
copy of lab-scripts/common/lab201-vms.json so that it works with no server.
Without --check the copy is rewritten. With --check the script prints a message
and exits with status 1 if the copy is out of date, which validate.sh uses.
"""

import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
VOL = os.path.join(ROOT, "volumes", "volume-201-fortiswitch-stig-and-srg-mapping", "lab-scripts")
MANIFEST = os.path.join(VOL, "common", "lab201-vms.json")
PAGE = os.path.join(VOL, "builder", "lab-builder.html")
PATTERN = re.compile(r'(<script id="lab201-manifest" type="application/json">\n)(.*?)(\n</script>)', re.S)


def embedded_text():
    with open(MANIFEST, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    return json.dumps(data, indent=2, ensure_ascii=False).replace("</", "<\\/")


def main(argv):
    check = "--check" in argv
    with open(PAGE, "r", encoding="utf-8") as fh:
        page = fh.read()
    m = PATTERN.search(page)
    if not m:
        print("sync_lab_builder.py: no manifest block found in %s" % PAGE, file=sys.stderr)
        return 2
    want = embedded_text()
    if m.group(2) == want:
        print("lab builder manifest: OK (matches lab201-vms.json)")
        return 0
    if check:
        print("lab builder manifest: OUT OF DATE. Run: python scripts/python/sync_lab_builder.py", file=sys.stderr)
        return 1
    page = page[: m.start(2)] + want + page[m.end(2):]
    with open(PAGE, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(page)
    print("lab builder manifest: updated")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
