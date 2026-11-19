#!/usr/bin/env python3
"""Keep the data embedded in the Lab Builder page in step with the lab-scripts files.

Usage: sync_lab_builder.py [--check]

The Lab Builder page (volume 201, lab-scripts/builder/lab-builder.html) carries a
copy of lab-scripts/common/lab201-vms.json (the manifest),
lab-scripts/common/flavors.json (the Linux flavors), the lab walkthroughs named
in lab-scripts/walkthroughs.list with the labs of those chapters (each with the
features its text names, the SRG requirements in its table, the switch its Uses
line names, the machines it uses, and the lab networks it uses), the service
names of the Hosts table in Chapter 999 with their hosts and addresses, the
networks of the Segments table in Chapter 999, and
lab-scripts/common/fortiswitch-features.json (which switch model series support
the lab features), so that it works with no server. Without --check the copies are rewritten. With
--check the script prints a message and exits with status 1 if a copy is out of
date, which validate.sh uses.

The script also compares the numbers that the documents of the volume state
about the labs and the page (how many SRG requirements the lab chapters test,
how many lab networks take a subnet, and how many checks the self-test of the
page makes) with what the lab chapters
and the page give. STATED lists those numbers. The script never changes a
document. It names the document, the line, and both numbers, and exits with
status 1, with or without --check.
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
# A row of a lab's requirement table: | `SRG ID` | CAT | Requirement | ...
SRG_ROW = re.compile(r"^\| `(SRG-[A-Z]+-\d{6}-[A-Z0-9]+-\d{6})` \| (I{1,3}) \| (.*?) \|")
# A row of the Hosts table in Chapter 999 that puts a service name on a machine: | radius-201a | RADIUS server 1 on svc-201a | ...
HOST_ROW = re.compile(r"^\| ([a-z][a-z0-9-]*) \| [^|]*? on ([a-z][a-z0-9-]*) \|")
# The same kind of row, with the IPv4 address of the service name: ... | P1, P2 | 10 | `10.201.10.10` | ...
SERVICE_ROW = re.compile(r"^\| ([a-z][a-z0-9-]*) \| ([^|]*?) on ([a-z][a-z0-9-]*) \| [^|]* \| [^|]* \| `(\d+\.\d+\.\d+\.\d+)` \|")
# A row of the Segments table in Chapter 999: | 10 | 10 | Lab-Services | `10.201.10.0/24` | `fd00:db8:201::a00/120` | .1 gw-201 | Purpose |
NETWORK_ROW = re.compile(r"^\| (\d+) \| ([^|]*?) \| ([A-Za-z0-9-]+) \| `\d+\.\d+\.(\d+)\.0/24` \| `[^`]*` \| ([^|]*?) \| ([^|]*?) \|\s*$")
# A row of the Hosts table with an IPv4 address. The host name is empty on a row that continues the host above it.
HOST_ADDR_ROW = re.compile(r"^\|\s*([a-z][a-z0-9-]*)?\s*\|[^|]*\|[^|]*\|[^|]*\|\s*`\d+\.\d+\.(\d+)\.\d+`\s*\|")
TOKEN = re.compile(r"`([a-z][a-z0-9-]*)`")
# The host names of the two switches under test in the lab chapters (SW_DEFAULT in the Lab Builder page).
SWITCHES = {"sw-648f-1": "a", "sw-2048f-1": "b"}
# Names in the lab text that look like hosts and are not.
NOT_HOSTS = {"baseline-201"}
WARNINGS = []


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def load_hosts():
    """The lab machines, the service names that Chapter 999 puts on them, and the hosts no script builds."""
    manifest = load_json(os.path.join(VOL, "common", "lab201-vms.json"))
    machines = [vm["name"] for vm in manifest["vms"]]
    aliases = {}
    with open(os.path.join(VOLUME, "chapters", "999-shared-lab-infrastructure.md"), "r", encoding="utf-8") as fh:
        for line in fh:
            m = HOST_ROW.match(line)
            if m and m.group(2) in machines and m.group(1) not in machines:
                aliases[m.group(1)] = m.group(2)
    other = []
    for entry in manifest.get("not_automated", []):
        other += [name.strip() for name in entry["name"].split(",")]
    return machines, aliases, other


def load_services():
    """The service names of the Hosts table in Chapter 999, with the host each one is on and its IPv4 address.

    The Lab Builder writes them into its picture of the lab, beside the address that the page gives each one.
    """
    services = []
    with open(os.path.join(VOLUME, "chapters", "999-shared-lab-infrastructure.md"), "r", encoding="utf-8") as fh:
        for line in fh:
            m = SERVICE_ROW.match(line)
            if m:
                services.append({"name": m.group(1), "on": m.group(3), "ipv4": m.group(4), "optional": "(optional)" in m.group(2)})
    return services


def load_networks():
    """The networks of the Segments table in Chapter 999, in the order of the table.

    The Lab Builder gives each one that a build uses the next /24 of the lab network range, so the order of the
    table is the order of the subnets. A network with no host and no gateway (the parking VLAN and the native
    VLAN) takes no subnet, and "hosts" is false for it.
    """
    networks = []
    with open(os.path.join(VOLUME, "chapters", "999-shared-lab-infrastructure.md"), "r", encoding="utf-8") as fh:
        for line in fh:
            m = NETWORK_ROW.match(line)
            if not m:
                continue
            number, vlan, name, octet, gateway, purpose = (part.strip() for part in m.groups())
            if int(octet) != int(number):
                WARNINGS.append("Segment %s of Chapter 999 has the subnet with third octet %s, so the Lab Builder cannot number it" % (number, octet))
                continue
            networks.append({"id": int(number), "name": name, "vlan": vlan, "hosts": not (gateway == "none" and "no hosts" in purpose)})
    return networks


def load_host_nets():
    """The lab networks in which each host of the Hosts table in Chapter 999 has an address."""
    nets, name = {}, None
    with open(os.path.join(VOLUME, "chapters", "999-shared-lab-infrastructure.md"), "r", encoding="utf-8") as fh:
        for line in fh:
            m = HOST_ADDR_ROW.match(line)
            if not m:
                if not line.startswith("|"):
                    name = None
                continue
            name = m.group(1) or name
            if name:
                nets.setdefault(name, set()).add(int(m.group(2)))
    return nets


def lab_facts(lab, body, patterns, machines, aliases, other, host_nets, net_ids, block):
    """What one lab's text says: the features it names, its SRG rows, the switch it runs on, the hosts it uses,
    and the lab networks it uses.

    The switch comes from the lab's Uses line only, because the rest of the text can name the other switch
    in passing. The machines come from the whole lab, so that leaving out the others cannot break a step.
    A lab uses a network when its text has an address in it, or names a host of the Hosts table that has one.
    """
    text = "\n".join(body)
    lab["features"] = [key for key, pattern in patterns if pattern.search(text)]
    srg, seen = [], set()
    uses = ""
    for line in body:
        m = SRG_ROW.match(line)
        if m and m.group(1) not in seen:
            seen.add(m.group(1))
            srg.append({"id": m.group(1), "cat": m.group(2), "text": m.group(3).strip()})
        if line.startswith("**Uses.**"):
            uses = line
    lab["srg"] = srg
    switches = [SWITCHES[t] for t in TOKEN.findall(uses) if t in SWITCHES]
    if re.search(r"\bboth switches\b", uses, re.I):
        switches = ["a", "b"]
    lab["switches"] = sorted(set(switches))
    found = set()
    for token in TOKEN.findall(text):
        if token in machines:
            found.add(token)
        elif token in aliases:
            found.add(aliases[token])
    lab["machines"] = [name for name in machines if name in found]
    lab["other"] = [name for name in other if name in TOKEN.findall(uses)]
    nets = set(int(n) for n in re.findall(r"(?<![0-9.])%s\.(\d{1,3})\.\d" % re.escape(block), text))
    for token in TOKEN.findall(text):
        nets |= host_nets.get(token, set())
    lab["nets"] = sorted(n for n in nets if n in net_ids)
    if lab["file"][:2] in ("04", "05", "06", "07", "08") and not uses:
        WARNINGS.append("Lab %s has no Uses line, so the Lab Builder cannot tell which switch it runs on" % lab["id"])
    known = set(machines) | set(aliases) | set(SWITCHES) | set(other) | NOT_HOSTS
    for token in TOKEN.findall(uses):
        if re.search(r"-201[a-z]?$", token) and token not in known:
            WARNINGS.append("Lab %s names %s, which is not a lab machine, a service name in Chapter 999, or a host no script builds" % (lab["id"], token))


def load_labs():
    """The walkthrough chapters, their short names in the zip, and the labs in each.

    Each lab lists the switch features its text names (found with the keywords in
    fortiswitch-features.json), the SRG requirements in its table, the switch its
    Uses line names (a, b, or both), and the lab machines it uses. The Lab Builder
    uses them to say which labs a switch model cannot run, which machines the
    planned labs need, and how far each requirement has been tested.
    """
    keywords = load_json(FEATURES).get("keywords", {})
    patterns = [(key, re.compile(words, re.I)) for key, words in keywords.items()]
    machines, aliases, other = load_hosts()
    del WARNINGS[:]
    networks, host_nets = load_networks(), load_host_nets()
    net_ids = set(n["id"] for n in networks if n["hosts"])
    block = load_json(os.path.join(VOL, "common", "lab201-vms.json")).get("ipv4_prefix", "10.201")
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
                    lab_facts(lab, body, patterns, machines, aliases, other, host_nets, net_ids, block)
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
    return {"walkthroughs": walkthroughs, "labs": labs, "services": load_services(), "networks": networks}


BLOCKS = [
    ("lab201-manifest", "lab201-vms.json", lambda: load_json(os.path.join(VOL, "common", "lab201-vms.json"))),
    ("lab201-flavors", "flavors.json", lambda: load_json(os.path.join(VOL, "common", "flavors.json"))),
    ("lab201-labs", "walkthroughs.list and the lab chapters", load_labs),
    ("lab201-switch-features", "fortiswitch-features.json", lambda: load_json(FEATURES)),
]


# The numbers that the documents state about the labs and the page: the document (under the volume folder), the
# words around the number, and what the number counts. In the words, # is the number, and a space is any white
# space, so a line break in the document does not matter. The words must be found once in the document.
STATED = [
    ("README.md", "covering all # distinct requirements", "ids"),
    ("README.md", "the Layer 2 Switch SRG (# requirements)", "ids:04"),
    ("README.md", "the Network Device Management SRG (#)", "ids:05"),
    ("README.md", "the Router SRG (#)", "ids:06"),
    ("README.md", "the AAA Services SRG (#)", "ids:07"),
    ("chapters/04-layer-2-switch-srg-requirement-labs.md", "The crosswalk lists # distinct Layer 2 Switch SRG requirements", "ids:04"),
    ("chapters/05-network-device-management-srg-requirement-labs.md", "in the crosswalk: # requirements", "ids:05"),
    ("chapters/06-router-srg-requirement-labs.md", "in the crosswalk (# requirements)", "ids:06"),
    ("chapters/07-aaa-services-srg-requirement-labs.md", "The crosswalk lists # distinct AAA Services SRG requirements", "ids:07"),
    ("lab-scripts/README.md", "each of the # SRG requirements", "rows"),
    ("chapters/09-esxi-7-8-and-9-lab-virtual-machine-automation.md", "each of the # SRG requirements", "rows"),
    ("chapters/09-esxi-7-8-and-9-lab-virtual-machine-automation.md", "it runs # checks", "checks"),
    ("chapters/09-esxi-7-8-and-9-lab-virtual-machine-automation.md", "A full build uses # of them", "nets"),
    ("lab-scripts/README.md", "A full build uses # of them", "nets"),
]


def stated_pattern(words):
    """The words of a STATED entry as a pattern, with the number as its one group."""
    before, after = ([re.escape(word) for word in part.split(" ")] for part in words.split("#"))
    return re.compile(r"\s+".join(before) + r"(\d+)" + r"\s+".join(after))


def selftest_checks(page):
    """How many checks the self-test of the page makes, or None when the page has no self-test.

    Each check is one call of ok() in selftest() or uitest(), and no call is in a loop, so the calls in the
    code are counted. A check that runs more than once would need another count.
    """
    start = page.find("function selftest()")
    if start < 0:
        return None
    code = page[start:]
    return len(re.findall(r"(?<![\w.$])ok\(", code)) - len(re.findall(r"\bfunction ok\(", code))


def lab_numbers(labs, page, networks=()):
    """What each kind of number in STATED is now, and the words that name it in a message."""
    ids, rows = {}, 0
    for lab in labs:
        rows += len(lab["srg"])
        ids.setdefault(lab["file"].split("-")[0], set()).update(row["id"] for row in lab["srg"])
    numbers = {
        "ids": (len(set().union(*ids.values())), "the distinct SRG requirements in the lab chapters"),
        "rows": (rows, "the SRG requirements that the Lab Builder lists"),
        "checks": (selftest_checks(page), "the checks that the self-test of the Lab Builder makes"),
        "nets": (len([n for n in networks if n.get("hosts", True)]) or None, "the lab networks in the Segments table of Chapter 999 that take a subnet"),
    }
    for chapter, found in ids.items():
        numbers["ids:" + chapter] = (len(found), "the distinct SRG requirements in the labs of Chapter %s" % chapter)
    return numbers


def stated_problems(labs, page, networks=()):
    """Compare each number in STATED with the lab chapters and the page. Returns the problems and the documents read."""
    numbers = lab_numbers(labs, page, networks)
    problems, texts = [], {}
    for name, words, kind in STATED:
        path = os.path.join(VOLUME, *name.split("/"))
        shown = "volumes/%s/%s" % (os.path.basename(VOLUME), name)
        if name not in texts:
            try:
                with open(path, "r", encoding="utf-8") as fh:
                    texts[name] = fh.read()
            except OSError:
                texts[name] = None
        text = texts[name]
        if text is None:
            problems.append("%s cannot be read" % shown)
            continue
        want, what = numbers.get(kind, (None, kind))
        if want is None:
            problems.append("%s: there is nothing to count for %s" % (shown, what))
            continue
        found = list(stated_pattern(words).finditer(text))
        if len(found) != 1:
            problems.append('%s: the words "%s" were found %d times, and must be found once. If the sentence changed, change STATED in scripts/python/sync_lab_builder.py'
                            % (shown, words, len(found)))
            continue
        said = int(found[0].group(1))
        if said != want:
            line = text.count("\n", 0, found[0].start(1)) + 1
            problems.append("%s line %d states %d for %s. The number is now %d" % (shown, line, said, what, want))
    return problems, len(texts)


def pattern(block_id):
    return re.compile(r'(<script id="%s" type="application/json">\n)(.*?)(\n</script>)' % re.escape(block_id), re.S)


def embedded_text(data):
    return json.dumps(data, indent=2, ensure_ascii=False).replace("</", "<\\/")


def main(argv):
    check = "--check" in argv
    with open(PAGE, "r", encoding="utf-8") as fh:
        page = fh.read()
    stale, loaded = [], {}
    for block_id, label, load in BLOCKS:
        m = pattern(block_id).search(page)
        if not m:
            print("sync_lab_builder.py: no %s block found in %s" % (block_id, PAGE), file=sys.stderr)
            return 2
        loaded[block_id] = load()
        want = embedded_text(loaded[block_id])
        if m.group(2) != want:
            stale.append(label)
            if not check:
                page = page[: m.start(2)] + want + page[m.end(2):]
    if not check:
        for warning in WARNINGS:
            print("lab builder data: note: %s" % warning, file=sys.stderr)
    status = 0
    if not stale:
        print("lab builder data: OK (matches lab201-vms.json, flavors.json, and the lab chapters)")
    elif check:
        print("lab builder data: OUT OF DATE (%s). Run: python scripts/python/sync_lab_builder.py" % ", ".join(stale), file=sys.stderr)
        status = 1
    else:
        with open(PAGE, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(page)
        print("lab builder data: updated (%s)" % ", ".join(stale))
    # The documents state some of these numbers in their text. No copy step keeps those in step, so compare them.
    problems, documents = stated_problems(loaded["lab201-labs"]["labs"], page, loaded["lab201-labs"]["networks"])
    if problems:
        print("stated numbers: WRONG. A document states a number that the lab chapters or the page do not give:", file=sys.stderr)
        for problem in problems:
            print("  %s" % problem, file=sys.stderr)
        status = 1
    else:
        print("stated numbers: OK (%d numbers in %d documents match the lab chapters and the page)" % (len(STATED), documents))
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
