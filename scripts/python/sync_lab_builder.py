#!/usr/bin/env python3
"""Keep the data embedded in the Lab Builder page in step with the lab-scripts files.

Usage: sync_lab_builder.py [--check]

The Lab Builder page (volume 201, lab-scripts/builder/lab-builder.html) carries a
copy of lab-scripts/common/lab201-vms.json (the manifest),
lab-scripts/common/flavors.json (the Linux flavors), the lab walkthroughs named
in lab-scripts/walkthroughs.list with the lab headings of those chapters, and
lab-scripts/common/fortiswitch-features.json (which switch model series support
the lab features), so that it works with no server. Without --check the copies are rewritten. With
--check the script prints a message and exits with status 1 if a copy is out of
date, which validate.sh uses.
"""

import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
VOLUME = os.path.join(ROOT, "volumes", "volume-201-fortiswitch-stig-and-srg-mapping")
VOL = os.path.join(VOLUME, "lab-scripts")
PAGE = os.path.join(VOL, "builder", "lab-builder.html")
FEATURES = os.path.join(VOL, "common", "fortiswitch-features.json")
LAB_HEADING = re.compile(r"^### Lab (\d+\.\d+) — (.+?)\s*$")


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def load_labs():
    """The walkthrough chapters, their short names in the zip, and the labs in each.

    Each lab also lists the switch features its text names, found with the
    keywords in fortiswitch-features.json, so the Lab Builder can say which labs
    a switch model cannot run.
    """
    keywords = load_json(FEATURES).get("keywords", {})
    patterns = [(key, re.compile(words, re.I)) for key, words in keywords.items()]
    walkthroughs, labs = [], []
    with open(os.path.join(VOL, "walkthroughs.list"), "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            name, _, short = (part.strip() for part in line.partition("="))
            walkthroughs.append({"file": name, "short": short or name})
            lab, body = None, []

            def close():
                if lab is not None:
                    text = "\n".join(body)
                    lab["features"] = [key for key, pattern in patterns if pattern.search(text)]
                    labs.append(lab)

            with open(os.path.join(VOLUME, "chapters", name), "r", encoding="utf-8") as chapter:
                for text in chapter:
                    m = LAB_HEADING.match(text)
                    if m or text.startswith("## "):
                        close()
                        lab, body = ({"id": m.group(1), "title": m.group(2), "file": name}, [text]) if m else (None, [])
                    elif lab is not None:
                        body.append(text)
            close()
    return {"walkthroughs": walkthroughs, "labs": labs}


BLOCKS = [
    ("lab201-manifest", "lab201-vms.json", lambda: load_json(os.path.join(VOL, "common", "lab201-vms.json"))),
    ("lab201-flavors", "flavors.json", lambda: load_json(os.path.join(VOL, "common", "flavors.json"))),
    ("lab201-labs", "walkthroughs.list and the lab chapters", load_labs),
    ("lab201-switch-features", "fortiswitch-features.json", lambda: load_json(FEATURES)),
]


def pattern(block_id):
    return re.compile(r'(<script id="%s" type="application/json">\n)(.*?)(\n</script>)' % re.escape(block_id), re.S)


def embedded_text(data):
    return json.dumps(data, indent=2, ensure_ascii=False).replace("</", "<\\/")


def main(argv):
    check = "--check" in argv
    with open(PAGE, "r", encoding="utf-8") as fh:
        page = fh.read()
    stale = []
    for block_id, label, load in BLOCKS:
        m = pattern(block_id).search(page)
        if not m:
            print("sync_lab_builder.py: no %s block found in %s" % (block_id, PAGE), file=sys.stderr)
            return 2
        want = embedded_text(load())
        if m.group(2) != want:
            stale.append(label)
            if not check:
                page = page[: m.start(2)] + want + page[m.end(2):]
    if not stale:
        print("lab builder data: OK (matches lab201-vms.json, flavors.json, and the lab chapters)")
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
