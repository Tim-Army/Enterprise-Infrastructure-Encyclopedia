#!/usr/bin/env python3
"""Keep the data embedded in the Lab Builder page in step with the lab-scripts files.

Usage: sync_lab_builder.py [--check]

The Lab Builder page (volume 201, lab-scripts/builder/lab-builder.html) carries a
copy of lab-scripts/common/lab201-vms.json (the manifest) and
lab-scripts/common/flavors.json (the Linux flavors) so that it works with no
server. Without --check the copies are rewritten. With --check the script prints
a message and exits with status 1 if a copy is out of date, which validate.sh uses.
"""

import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
VOL = os.path.join(ROOT, "volumes", "volume-201-fortiswitch-stig-and-srg-mapping", "lab-scripts")
PAGE = os.path.join(VOL, "builder", "lab-builder.html")
BLOCKS = [
    ("lab201-manifest", os.path.join(VOL, "common", "lab201-vms.json")),
    ("lab201-flavors", os.path.join(VOL, "common", "flavors.json")),
]


def pattern(block_id):
    return re.compile(r'(<script id="%s" type="application/json">\n)(.*?)(\n</script>)' % re.escape(block_id), re.S)


def embedded_text(path):
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    return json.dumps(data, indent=2, ensure_ascii=False).replace("</", "<\\/")


def main(argv):
    check = "--check" in argv
    with open(PAGE, "r", encoding="utf-8") as fh:
        page = fh.read()
    stale = []
    for block_id, path in BLOCKS:
        m = pattern(block_id).search(page)
        if not m:
            print("sync_lab_builder.py: no %s block found in %s" % (block_id, PAGE), file=sys.stderr)
            return 2
        want = embedded_text(path)
        if m.group(2) != want:
            stale.append(os.path.basename(path))
            if not check:
                page = page[: m.start(2)] + want + page[m.end(2):]
    if not stale:
        print("lab builder data: OK (matches lab201-vms.json and flavors.json)")
        return 0
    if check:
        print("lab builder data: OUT OF DATE (%s). Run: python scripts/python/sync_lab_builder.py" % ", ".join(stale), file=sys.stderr)
        return 1
    with open(PAGE, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(page)
    print("lab builder data: updated (%s)" % ", ".join(stale))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
