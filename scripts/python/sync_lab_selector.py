#!/usr/bin/env python3
"""Keep the data embedded in the Lab Selector page in step with the lab-scripts files and the lab chapters.

Usage: sync_lab_selector.py [--check]
       sync_lab_selector.py --package-args
       sync_lab_selector.py --set-links

The Lab Selector page (volume 901, lab-scripts/selector/lab-selector.html) carries
a copy of lab-scripts/common/lab201-vms.json (the manifest),
lab-scripts/common/flavors.json (the Linux flavors),
lab-scripts/common/fortiswitch-features.json (which switch model series support
the lab features), and the lab data, so that it works with no server.

The lab data comes from lab-scripts/common/lab-catalog.json and from the chapters
that the catalog names. The catalog lists the lab kinds (SRG labs, certification
labs, learning labs) and the lab sets (the labs of one volume). For each lab set
the script reads the labs of its chapters: the features a lab's text names, the
SRG requirements in its table, the switch its Uses line names, the machines it
uses, the hosts it uses that no script builds, and the lab networks it uses.
From the shared lab (the base of the catalog, Chapter 999 of Volume CCI) it
reads the service names of the Hosts table with their hosts and addresses, and
the networks of the Segments table, each with its IPv4 block. From the Chapter
999 of every other lab set
it reads the Address plan table: the hosts that the set adds, which no script
builds, and the hosts of another set that it reuses.

Without --check the copies are rewritten. With --check the script prints a
message and exits with status 1 if a copy is out of date, which validate.sh uses.

The script also compares the numbers that the documents state about the labs and
the page (how many SRG requirements the lab chapters test, how many lab networks
take a subnet, and how many checks the self-test of the page makes) with what
the lab chapters and the page give. STATED lists those numbers. The script never
changes a document. It names the document, the line, and both numbers, and exits
with status 1, with or without --check.

The script checks the address plan too: the blocks of the Segments table do not
overlap, the segments list of the manifest gives the same blocks, and every
address of a machine, of a service name, and of a host of a lab set lies in the
block of a lab network. A problem is printed, and the script exits with status 1.

With --package-args the script prints one SOURCE=DEST line for each file that
the site build adds to the published lab-scripts folder: the lab diagram and the
lab chapters, each under the short name it has in the zip of the Lab Selector.

With --set-links the script prints one line for each lab set: the folder of its
volume, its id, and its name, with tabs between them. The site build gives the
portal page of each such volume a link that opens the Lab Selector with that
lab set ticked (lab-selector.html?sets=<id>).
"""

import ipaddress
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
VOLUMES = os.path.join(ROOT, "volumes")
# The volume that holds the Lab Selector, its data, and the lab scripts.
HOME = "volume-901-lab-selector"
VOL = os.path.join(VOLUMES, HOME, "lab-scripts")
PAGE = os.path.join(VOL, "selector", "lab-selector.html")
CATALOG = os.path.join(VOL, "common", "lab-catalog.json")
MANIFEST = os.path.join(VOL, "common", "lab201-vms.json")
FEATURES = os.path.join(VOL, "common", "fortiswitch-features.json")
LAB_HEADING = re.compile(r"^### Lab (\d+\.\d+) — (.+?)\s*$")
# A row of a lab's requirement table: | `SRG ID` | CAT | Requirement | ...
SRG_ROW = re.compile(r"^\| `(SRG-[A-Z]+-\d{6}-[A-Z0-9]+-\d{6})` \| (I{1,3}) \| (.*?) \|")
# A row of the Hosts table in Chapter 999 that puts a service name on a machine: | radius-201a | RADIUS server 1 on svc-201a | ...
HOST_ROW = re.compile(r"^\| ([a-z][a-z0-9-]*) \| [^|]*? on ([a-z][a-z0-9-]*) \|")
# The same kind of row, with the IPv4 address of the service name: ... | P1, P2 | 2 | `10.200.0.42` | ...
SERVICE_ROW = re.compile(r"^\| ([a-z][a-z0-9-]*) \| ([^|]*?) on ([a-z][a-z0-9-]*) \| [^|]* \| [^|]* \| `(\d+\.\d+\.\d+\.\d+)` \|")
# A row of the Segments table in Chapter 999: | 2 | 2 | Lab-Services | `10.200.0.32/27` | `fd00:db8:201::200/120` | `10.200.0.33` gw-201 | Purpose |
NETWORK_ROW = re.compile(r"^\| (\d+) \| ([^|]*?) \| ([A-Za-z0-9-]+) \| (?:`(\d+\.\d+\.\d+\.\d+/\d+)`|none) \| (?:`[^`]*`|none) \| ([^|]*?) \| ([^|]*?) \|\s*$")
# The first row of the Segments table, which is the supernet of the lab and no network:
# | all | all | Supernet | `10.200.0.0/22` | `fd00:db8:201::/112` | none | The whole lab, from ... `10.200.0.0` to its last, `10.200.3.255` |
SUPERNET_ROW = re.compile(r"^\| [^|]*? \| [^|]*? \| Supernet \| `(\d+\.\d+\.\d+\.\d+/\d+)` \| [^|]* \| [^|]* \| ([^|]*?) \|\s*$")
# A row of the Hosts table with an IPv4 address. The host name is empty on a row that continues the host above it.
HOST_ADDR_ROW = re.compile(r"^\|\s*([a-z][a-z0-9-]*)?\s*\|[^|]*\|[^|]*\|[^|]*\|\s*`(\d+\.\d+\.\d+\.\d+)`\s*\|")
# A row of the Address plan table in the Chapter 999 of a lab set that reuses the shared lab:
# | faz-202 | FortiAnalyzer-VM 7.6 under test | This volume | `10.200.0.54` | `fd00:db8:201::216` |
PLAN_ROW = re.compile(r"^\| ([a-z][a-z0-9-]*) \| ([^|]*?) \| (This volume|Volume [CDILMVX]+) \| `(\d+\.\d+\.\d+\.\d+)` \| (?:`([^`]*)`|[^|]*?) \|\s*$")
TOKEN = re.compile(r"`([a-z][a-z0-9-]*)`")
# The host names of the two switches under test in the lab chapters (SW_DEFAULT in the Lab Selector page).
SWITCHES = {"sw-648f-1": "a", "sw-2048f-1": "b"}
# Names in the lab text that look like hosts and are not.
NOT_HOSTS = {"baseline-201", "baseline-202", "baseline-203", "lab-202", "lab-203"}
WARNINGS = []
# What is wrong with the address plan. The script exits with status 1 when the list is not empty.
PLAN_PROBLEMS = []


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def chapter_path(volume, name):
    return os.path.join(VOLUMES, volume, "chapters", name)


def read_lines(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read().split("\n")


def base_lines(catalog):
    return read_lines(chapter_path(catalog["base"]["volume"], catalog["base"]["chapter"]))


def load_hosts(catalog):
    """The lab machines, the service names that the shared lab puts on them, and the hosts no script builds."""
    manifest = load_json(MANIFEST)
    machines = [vm["name"] for vm in manifest["vms"]]
    aliases = {}
    for line in base_lines(catalog):
        m = HOST_ROW.match(line)
        if m and m.group(2) in machines and m.group(1) not in machines:
            aliases[m.group(1)] = m.group(2)
    other = []
    for entry in manifest.get("not_automated", []):
        other += [name.strip() for name in entry["name"].split(",")]
    return machines, aliases, other


def load_services(catalog):
    """The service names of the Hosts table of the shared lab, with the host each one is on and its IPv4 address.

    The Lab Selector writes them into its picture of the lab, beside the address that the page gives each one.
    """
    services = []
    for line in base_lines(catalog):
        m = SERVICE_ROW.match(line)
        if m:
            services.append({"name": m.group(1), "on": m.group(3), "ipv4": m.group(4), "optional": "(optional)" in m.group(2)})
    return services


def load_networks(catalog):
    """The networks of the Segments table of the shared lab, in the order of the table, each with its IPv4 block.

    The Lab Selector gives each one that a build uses the lowest free block of its size, in the order of the
    table, so the size of a network is the size of its block in the table. A network with no host and no gateway
    (the parking VLAN and the native VLAN) takes no subnet, and "hosts" is false for it.
    """
    networks = []
    for line in base_lines(catalog):
        m = NETWORK_ROW.match(line)
        if not m:
            continue
        number, vlan, name, cidr, gateway, purpose = ((part or "").strip() for part in m.groups())
        if not cidr:
            # A VLAN with no hosts and no gateway (the parking VLAN and the native VLAN) has no subnet.
            networks.append({"id": int(number), "name": name, "vlan": vlan, "hosts": False})
            continue
        try:
            block = ipaddress.IPv4Network(cidr)
        except ValueError:
            PLAN_PROBLEMS.append("Segment %s of the shared lab has the subnet %s, which is not the address of a network with its prefix length" % (number, cidr))
            continue
        networks.append({"id": int(number), "name": name, "vlan": vlan, "cidr": str(block), "hosts": not (gateway == "none" and "no hosts" in purpose)})
    return networks


def check_supernet_row(catalog, networks, prefix):
    """Compare the supernet row of the Segments table with the networks under it.

    The supernet is the smallest block that starts at the first address of the IPv4 block of the lab and holds
    every lab network, as BOOK_RANGE in the Lab Selector page. The row is written by hand, so a network that is
    added to the table can make it wrong. The page puts the supernet of a build in the row of a chapter copy,
    and it finds the values to replace only when the row is right.
    """
    blocks = [ipaddress.IPv4Network(n["cidr"]) for n in networks if n.get("cidr")]
    if not blocks:
        return
    start, end, length, size = int(ipaddress.IPv4Address(prefix + ".0.0")), max(int(b.broadcast_address) for b in blocks) + 1, 32, 1
    while length > 0 and start + size < end:
        length, size = length - 1, size * 2
    want = "%s/%d" % (ipaddress.IPv4Address(start), length)
    first, last = str(ipaddress.IPv4Address(start)), str(ipaddress.IPv4Address(start + size - 1))
    lines = base_lines(catalog)
    rows = [i for i, line in enumerate(lines) if SUPERNET_ROW.match(line)]
    if len(rows) != 1:
        PLAN_PROBLEMS.append("The Segments table of the shared lab has %d rows for the supernet that can be read. It needs one, as its first row: "
                             "| all | all | Supernet | `%s` | ... | with `%s` and `%s` in its last cell" % (len(rows), want, first, last))
        return
    m = SUPERNET_ROW.match(lines[rows[0]])
    said = re.findall(r"`(\d+\.\d+\.\d+\.\d+)`", m.group(2))
    if m.group(1) != want or said != [first, last]:
        PLAN_PROBLEMS.append("The supernet row of the Segments table of the shared lab gives %s with the addresses %s. The networks under it need %s, from %s to %s"
                             % (m.group(1), " and ".join(said) or "none", want, first, last))
    if any(NETWORK_ROW.match(line) for line in lines[:rows[0]]):
        PLAN_PROBLEMS.append("The supernet row of the Segments table of the shared lab has to be the first row of the table")


def net_of(address, networks):
    """The number of the lab network whose block holds an IPv4 address, or None."""
    try:
        ip = ipaddress.IPv4Address(address)
    except ValueError:
        return None
    for n in networks:
        if n.get("cidr") and ip in ipaddress.IPv4Network(n["cidr"]):
            return n["id"]
    return None


def load_host_nets(catalog, networks):
    """The lab networks in which each host of the Hosts table of the shared lab has an address."""
    nets, name = {}, None
    for line in base_lines(catalog):
        m = HOST_ADDR_ROW.match(line)
        if not m:
            if not line.startswith("|"):
                name = None
            continue
        name = m.group(1) or name
        net = net_of(m.group(2), networks)
        if net is None:
            PLAN_PROBLEMS.append("The Hosts table of the shared lab gives %s the address %s, which is in no block of the Segments table" % (name or "a host", m.group(2)))
        elif name:
            nets.setdefault(name, set()).add(net)
    return nets


def load_set_hosts(catalog, networks):
    """What the Address plan table of each lab set's own Chapter 999 says.

    A row that is from "This volume" is a host that the set adds. No script builds it. A row that is from the volume
    of another lab set is a host of that set which this one reuses. A row from the volume of the shared lab is one of
    its machines or service names, which the lab's text already ties to the set, so it is not listed here.
    """
    by_roman = dict((s["roman"], s["id"]) for s in catalog["sets"])
    base_roman = catalog["base"]["roman"]
    found = {}
    for entry in catalog["sets"]:
        hosts, reuses = [], []
        shared = entry.get("shared")
        if shared:
            for line in read_lines(chapter_path(entry["volume"], shared["file"])):
                m = PLAN_ROW.match(line)
                if not m:
                    continue
                name, role, source, ipv4, ipv6 = m.groups()
                optional = "(optional)" in role
                role = role.replace("(optional)", "").replace("`", "").strip()
                if source == "This volume":
                    net = net_of(ipv4, [n for n in networks if n["hosts"]])
                    if net is None:
                        PLAN_PROBLEMS.append("%s of %s has the address %s, which is in no block of the Segments table of the shared lab, so the Lab Selector cannot place it"
                                             % (name, entry["name"], ipv4))
                        continue
                    hosts.append({"name": name, "role": role, "ipv4": ipv4, "ipv6": ipv6 or "",
                                  "net": net, "optional": optional})
                elif source != "Volume " + base_roman:
                    owner = by_roman.get(source[len("Volume "):])
                    if owner is None:
                        WARNINGS.append("%s of %s is from %s, which is not the volume of a lab set in lab-catalog.json" % (name, entry["name"], source))
                    elif owner != entry["id"]:
                        reuses.append({"name": name, "set": owner, "role": role, "optional": optional})
            if not hosts:
                WARNINGS.append("The Address plan table of %s names no host that the volume adds" % entry["name"])
        found[entry["id"]] = (hosts, reuses)
    # A reused host has to be one that its set adds.
    for entry in catalog["sets"]:
        for item in found[entry["id"]][1]:
            if item["name"] not in [h["name"] for h in found[item["set"]][0]]:
                WARNINGS.append("%s reuses %s, which the Address plan table of its volume does not add" % (entry["name"], item["name"]))
    return found


def lab_facts(lab, body, patterns, machines, aliases, other, host_nets, networks, block, switches_set):
    """What one lab's text says: the features it names, its SRG rows, the switch it runs on, the hosts it uses,
    and the lab networks it uses.

    The switch comes from the lab's Uses line only, because the rest of the text can name the other switch
    in passing. The machines come from the whole lab, so that leaving out the others cannot break a step.
    A lab uses a network when its text has an address in it, or names a host that has one. Only the labs of a
    lab set that runs on the switches name switch features and a switch.
    """
    text = "\n".join(body)
    lab["features"] = [key for key, pattern in patterns if pattern.search(text)] if switches_set else []
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
    switches = [SWITCHES[t] for t in TOKEN.findall(uses) if t in SWITCHES] if switches_set else []
    if switches_set and re.search(r"\bboth switches\b", uses, re.I):
        switches = ["a", "b"]
    lab["switches"] = sorted(set(switches))
    found = set()
    for token in TOKEN.findall(text):
        if token in machines:
            found.add(token)
        elif token in aliases:
            found.add(aliases[token])
    lab["machines"] = [name for name in machines if name in found]
    # The hosts no script builds: the ones the Uses line names. A lab that builds the hosts of its lab set has no Uses
    # line, so its whole text counts.
    named = TOKEN.findall(text if lab["shared"] and lab["set"] and not switches_set else uses)
    lab["other"] = [name for name in other if name in named]
    with_hosts = [n for n in networks if n["hosts"]]
    nets = set(net_of(a, with_hosts) for a in re.findall(r"(?<![0-9.])(%s\.\d{1,3}\.\d{1,3})(?![0-9])" % re.escape(block), text))
    for token in TOKEN.findall(text):
        nets |= host_nets.get(token, set())
    net_ids = set(n["id"] for n in with_hosts)
    lab["nets"] = sorted(n for n in nets if n in net_ids)
    if not lab["shared"] and not uses:
        WARNINGS.append("Lab %s has no Uses line, so the Lab Selector cannot tell which %s it runs on" % (lab["id"], "switch" if switches_set else "hosts"))
    known = set(machines) | set(aliases) | set(SWITCHES) | set(other) | NOT_HOSTS
    for token in TOKEN.findall(uses):
        if re.search(r"-20\d[a-z]?$", token) and token not in known:
            WARNINGS.append("Lab %s names %s, which is not a lab machine, a service name of the shared lab, or a host no script builds" % (lab["id"], token))


def walkthrough_list(catalog):
    """The lab chapters that travel in the zip, in walkthrough order: the shared lab, then each lab set.

    Each entry names its volume, its chapter file, the short name it has in the zip, the lab set it belongs to
    ("" for the shared lab), and whether its labs build hosts (shared) or prove requirements.
    """
    base = catalog["base"]
    items = [{"file": base["chapter"], "short": base["short"], "set": "", "volume": base["volume"], "roman": base["roman"],
              "name": "Build the shared lab", "shared": True}]
    for entry in catalog["sets"]:
        shared = entry.get("shared")
        if shared:
            items.append({"file": shared["file"], "short": shared["short"], "set": entry["id"], "volume": entry["volume"], "roman": entry["roman"],
                          "name": shared["name"], "shared": True})
        for chapter in entry["chapters"]:
            items.append({"file": chapter["file"], "short": chapter["short"], "set": entry["id"], "volume": entry["volume"], "roman": entry["roman"],
                          "name": chapter["name"], "shared": False})
    shorts = [w["short"] for w in items]
    for short in sorted(set(s for s in shorts if shorts.count(s) > 1)):
        raise SystemExit("sync_lab_selector.py: lab-catalog.json gives the short name %s to more than one chapter" % short)
    return items


def load_labs():
    """The lab kinds, the lab sets, the walkthrough chapters, and the labs in each.

    Each lab lists the switch features its text names (found with the keywords in fortiswitch-features.json), the
    SRG requirements in its table, the switch its Uses line names (a, b, or both), the lab machines it uses, and the
    hosts it uses that no script builds. The Lab Selector uses them to say which labs a switch model cannot run,
    which machines and hosts the planned labs need, and how far each requirement has been tested.

    A lab has a number (num), which is the one in its chapter, and an id, which is its number with the prefix of
    its lab set before it (faz-3.1), because two volumes can both have a Lab 3.1. The labs of the lab set with no
    prefix keep their number as their id.
    """
    catalog = load_json(CATALOG)
    keywords = load_json(FEATURES).get("keywords", {})
    patterns = [(key, re.compile(words, re.I)) for key, words in keywords.items()]
    machines, aliases, other = load_hosts(catalog)
    del WARNINGS[:]
    del PLAN_PROBLEMS[:]
    networks = load_networks(catalog)
    check_supernet_row(catalog, networks, load_json(MANIFEST).get("ipv4_prefix", "10.200"))
    host_nets = load_host_nets(catalog, networks)
    set_hosts = load_set_hosts(catalog, networks)
    for entry in catalog["sets"]:
        for host in set_hosts[entry["id"]][0]:
            if host["name"] not in other:
                other.append(host["name"])
            host_nets.setdefault(host["name"], set()).add(host["net"])
    block = load_json(MANIFEST).get("ipv4_prefix", "10.200")
    base, by_id = catalog["base"], dict((s["id"], s) for s in catalog["sets"])
    walkthroughs, labs = [], []
    for item in walkthrough_list(catalog):
        entry = by_id[item["set"] or base["set"]]
        prefix = by_id[item["set"]]["prefix"] if item["set"] else ""
        walkthroughs.append({"file": item["file"], "short": item["short"], "set": item["set"], "volume": item["volume"], "roman": item["roman"],
                             "name": item["name"], "chapter": item["file"].split("-")[0], "shared": item["shared"]})
        lab, body = None, []

        def close():
            if lab is not None:
                lab_facts(lab, body, patterns, machines, aliases, other, host_nets, networks, block, bool(entry.get("switches")))
                labs.append(lab)

        with open(chapter_path(item["volume"], item["file"]), "r", encoding="utf-8") as chapter:
            for text in chapter:
                m = LAB_HEADING.match(text)
                if m or text.startswith("## "):
                    close()
                    if m:
                        owner = item["set"]
                        if not owner and m.group(1) not in base["always"]:
                            # A lab of the shared lab chapter that prepares the switches belongs to the lab set that uses them.
                            owner = base["set"]
                        lab = {"id": (prefix + "-" if prefix else "") + m.group(1), "num": m.group(1), "title": m.group(2), "file": item["file"],
                               "doc": item["short"], "set": owner, "shared": item["shared"]}
                        body = [text]
                    else:
                        lab, body = None, []
                elif lab is not None:
                    body.append(text)
        close()
    ids = [lab["id"] for lab in labs]
    for lab_id in sorted(set(i for i in ids if ids.count(i) > 1)):
        raise SystemExit("sync_lab_selector.py: two labs have the id %s. Give one lab set another prefix in lab-catalog.json" % lab_id)
    for always in base["always"]:
        if always not in ids:
            raise SystemExit("sync_lab_selector.py: lab-catalog.json names the lab %s, which the shared lab chapter does not have" % always)
    kinds = [{"id": k["id"], "name": k["name"], "sub": k["sub"]} for k in catalog["kinds"]]
    sets = []
    for entry in catalog["sets"]:
        if entry["kind"] not in [k["id"] for k in kinds]:
            raise SystemExit("sync_lab_selector.py: the lab set %s has the kind %s, which lab-catalog.json does not list" % (entry["id"], entry["kind"]))
        hosts, reuses = set_hosts[entry["id"]]
        sets.append({"id": entry["id"], "kind": entry["kind"], "name": entry["name"], "volume": entry["volume"], "roman": entry["roman"],
                     "prefix": entry["prefix"], "selected": bool(entry.get("selected")), "switches": bool(entry.get("switches")),
                     "about": entry["about"], "hosts": hosts, "reuses": reuses})
    return {"kinds": kinds, "sets": sets, "walkthroughs": walkthroughs, "labs": labs, "services": load_services(catalog), "networks": networks}


BLOCKS = [
    ("lab201-manifest", "lab201-vms.json", lambda: load_json(MANIFEST)),
    ("lab201-flavors", "flavors.json", lambda: load_json(os.path.join(VOL, "common", "flavors.json"))),
    ("lab201-labs", "lab-catalog.json and the lab chapters", load_labs),
    ("lab201-switch-features", "fortiswitch-features.json", lambda: load_json(FEATURES)),
]

V201 = "volume-201-fortiswitch-stig-and-srg-mapping"

# The numbers that the documents state about the labs and the page: the volume, the document (under the volume
# folder), the words around the number, and what the number counts. In the words, # is the number, and a space is
# any white space, so a line break in the document does not matter. The words must be found once in the document.
# What a number counts: "ids" is the distinct SRG requirements of a lab set, "rows" is the SRG rows of its labs,
# and "labs" is its requirement labs, each followed by @ and the lab set. "ids:04" is the distinct requirements of
# the chapter with that number in the lab set with no prefix. "checks" and "nets" belong to the page and the shared lab.
STATED = [
    (V201, "README.md", "covering all # distinct requirements", "ids@fortiswitch"),
    (V201, "README.md", "the Layer 2 Switch SRG (# requirements)", "ids:04"),
    (V201, "README.md", "the Network Device Management SRG (#)", "ids:05"),
    (V201, "README.md", "the Router SRG (#)", "ids:06"),
    (V201, "README.md", "the AAA Services SRG (#)", "ids:07"),
    (V201, "chapters/04-layer-2-switch-srg-requirement-labs.md", "The crosswalk lists # distinct Layer 2 Switch SRG requirements", "ids:04"),
    (V201, "chapters/05-network-device-management-srg-requirement-labs.md", "in the crosswalk: # requirements", "ids:05"),
    (V201, "chapters/06-router-srg-requirement-labs.md", "in the crosswalk (# requirements)", "ids:06"),
    (V201, "chapters/07-aaa-services-srg-requirement-labs.md", "The crosswalk lists # distinct AAA Services SRG requirements", "ids:07"),
    (HOME, "lab-scripts/README.md", "each of the # SRG requirements", "rows@fortiswitch"),
    (HOME, "lab-scripts/README.md", "A full build uses # of them", "nets"),
    (HOME, "chapters/01-the-lab-selector.md", "each of the # FortiSwitch requirements", "rows@fortiswitch"),
    (HOME, "chapters/01-the-lab-selector.md", "it runs # checks", "checks"),
    (HOME, "chapters/01-the-lab-selector.md", "A full build uses # of them", "nets"),
    (HOME, "chapters/01-the-lab-selector.md", "| FortiSwitch | CCI | # |", "labs@fortiswitch"),
    (HOME, "chapters/01-the-lab-selector.md", "| FortiAnalyzer | CCII | # |", "labs@fortianalyzer"),
    (HOME, "chapters/01-the-lab-selector.md", "| FortiManager | CCIII | # |", "labs@fortimanager"),
    (HOME, "chapters/01-the-lab-selector.md", "The FortiSwitch labs prove # requirements", "ids@fortiswitch"),
    (HOME, "chapters/01-the-lab-selector.md", "the FortiAnalyzer labs prove # requirements", "ids@fortianalyzer"),
    (HOME, "chapters/01-the-lab-selector.md", "the FortiManager labs prove # requirements", "ids@fortimanager"),
    (HOME, "chapters/90-as-built-how-this-volume-was-built.md", "| # checks pass in a Chromium browser", "checks"),
    (HOME, "chapters/90-as-built-how-this-volume-was-built.md", "The page passes # checks", "checks"),
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


def lab_numbers(data, page):
    """What each kind of number in STATED is now, and the words that name it in a message."""
    labs, networks = data["labs"], data["networks"]
    numbers = {
        "checks": (selftest_checks(page), "the checks that the self-test of the Lab Selector makes"),
        "nets": (len([n for n in networks if n.get("hosts", True)]) or None, "the lab networks in the Segments table of the shared lab that take a subnet"),
    }
    for entry in data["sets"]:
        mine = [lab for lab in labs if lab["set"] == entry["id"] and not lab["shared"]]
        ids = set(row["id"] for lab in mine for row in lab["srg"])
        numbers["ids@" + entry["id"]] = (len(ids), "the distinct SRG requirements in the labs of %s" % entry["name"])
        numbers["rows@" + entry["id"]] = (sum(len(lab["srg"]) for lab in mine), "the SRG requirements that the Lab Selector lists for %s" % entry["name"])
        numbers["labs@" + entry["id"]] = (len([lab for lab in mine if lab["srg"]]), "the requirement labs of %s" % entry["name"])
        if not entry["prefix"]:
            chapters = {}
            for lab in mine:
                chapters.setdefault(lab["file"].split("-")[0], set()).update(row["id"] for row in lab["srg"])
            for chapter, found in chapters.items():
                numbers["ids:" + chapter] = (len(found), "the distinct SRG requirements in the labs of Chapter %s" % chapter)
    return numbers


def stated_problems(data, page):
    """Compare each number in STATED with the lab chapters and the page. Returns the problems and the documents read."""
    numbers = lab_numbers(data, page)
    problems, texts = [], {}
    for volume, name, words, kind in STATED:
        path = os.path.join(VOLUMES, volume, *name.split("/"))
        shown = "volumes/%s/%s" % (volume, name)
        if shown not in texts:
            try:
                with open(path, "r", encoding="utf-8") as fh:
                    texts[shown] = fh.read()
            except OSError:
                texts[shown] = None
        text = texts[shown]
        if text is None:
            problems.append("%s cannot be read" % shown)
            continue
        want, what = numbers.get(kind, (None, kind))
        if want is None:
            problems.append("%s: there is nothing to count for %s" % (shown, what))
            continue
        found = list(stated_pattern(words).finditer(text))
        if len(found) != 1:
            problems.append('%s: the words "%s" were found %d times, and must be found once. If the sentence changed, change STATED in scripts/python/sync_lab_selector.py'
                            % (shown, words, len(found)))
            continue
        said = int(found[0].group(1))
        if said != want:
            line = text.count("\n", 0, found[0].start(1)) + 1
            problems.append("%s line %d states %d for %s. The number is now %d" % (shown, line, said, what, want))
    return problems, len(texts)


def plan_problems(data, manifest):
    """What is wrong with the address plan, beyond what was found while the chapters were read.

    The Segments table of the shared lab is the plan. The segments list of the manifest has to give the same
    blocks, because the lab scripts read the manifest and not the chapter. No two blocks may overlap. The first
    row of the table names the supernet that holds them, which check_supernet_row compared with them. Every
    address of a machine has to lie in a block, with the prefix length of the block unless the address is one
    end of a routed link (/31) or a loopback (/32), and it may not be the network or the broadcast address.
    """
    problems = list(PLAN_PROBLEMS)
    blocks = dict((n["id"], ipaddress.IPv4Network(n["cidr"])) for n in data["networks"] if n.get("cidr"))
    ids = sorted(blocks)
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            if blocks[a].overlaps(blocks[b]):
                problems.append("Segments %d and %d of the shared lab overlap: %s and %s" % (a, b, blocks[a], blocks[b]))
    listed = dict((int(s["id"]), s.get("ipv4")) for s in manifest.get("segments", []))
    for seg in sorted(set(ids) | set(listed)):
        want, has = (str(blocks[seg]) if seg in blocks else None), listed.get(seg)
        if want != has:
            problems.append("Segment %d is %s in the Segments table of the shared lab and %s in the segments list of lab201-vms.json"
                            % (seg, want or "missing", has or "missing"))
    for vm in manifest.get("vms", []):
        slots = [(a, nic.get("gateway4")) for nic in vm.get("nics", []) for a in nic.get("ipv4", [])]
        slots += [(a, None) for d in vm.get("dummies", []) for a in d.get("ipv4", [])]
        for cidr, gateway in slots:
            iface = ipaddress.IPv4Interface(cidr)
            seg = net_of(str(iface.ip), data["networks"])
            if seg is None:
                problems.append("%s has the address %s, which is in no block of the Segments table" % (vm["name"], cidr))
                continue
            block, length = blocks[seg], iface.network.prefixlen
            if length not in (31, 32):
                if length != block.prefixlen:
                    problems.append("%s has the address %s, and segment %d is %s" % (vm["name"], cidr, seg, block))
                elif iface.ip in (block.network_address, block.broadcast_address):
                    problems.append("%s has the address %s, which is the network or the broadcast address of segment %d" % (vm["name"], cidr, seg))
            if gateway and net_of(gateway, data["networks"]) != seg:
                problems.append("%s has the gateway %s, which is not in segment %d with its address %s" % (vm["name"], gateway, seg, cidr))
    for service in data["services"]:
        if net_of(service["ipv4"], data["networks"]) is None:
            problems.append("The service name %s has the address %s, which is in no block of the Segments table" % (service["name"], service["ipv4"]))
    return problems, len(blocks)


def pattern(block_id):
    return re.compile(r'(<script id="%s" type="application/json">\n)(.*?)(\n</script>)' % re.escape(block_id), re.S)


def embedded_text(data):
    return json.dumps(data, indent=2, ensure_ascii=False).replace("</", "<\\/")


def package_args():
    """One SOURCE=DEST line for each file the site build adds to the published lab-scripts folder."""
    catalog = load_json(CATALOG)
    lines = []
    diagram = catalog["base"].get("diagram")
    if diagram and os.path.isfile(os.path.join(ROOT, *diagram.split("/"))):
        lines.append("%s=diagrams/lab-topology.svg" % diagram)
    for item in walkthrough_list(catalog):
        source = "volumes/%s/chapters/%s" % (item["volume"], item["file"])
        if not os.path.isfile(os.path.join(ROOT, *source.split("/"))):
            raise SystemExit("sync_lab_selector.py: lab-catalog.json names a missing chapter: %s" % source)
        lines.append("%s=walkthroughs/%s" % (source, item["short"]))
    return lines


def set_links():
    """One line for each lab set: the folder of its volume, its id, and its name, with tabs between them."""
    catalog = load_json(CATALOG)
    for entry in catalog["sets"]:
        if not re.match(r"^[a-z][a-z0-9-]*$", entry["id"]):
            raise SystemExit("sync_lab_selector.py: the id of a lab set goes into a link, so use lowercase letters, digits, and hyphens: %s" % entry["id"])
    return ["%s\t%s\t%s" % (entry["volume"], entry["id"], entry["name"]) for entry in catalog["sets"]]


def main(argv):
    if "--package-args" in argv:
        print("\n".join(package_args()))
        return 0
    if "--set-links" in argv:
        print("\n".join(set_links()))
        return 0
    check = "--check" in argv
    with open(PAGE, "r", encoding="utf-8") as fh:
        page = fh.read()
    stale, loaded = [], {}
    for block_id, label, load in BLOCKS:
        m = pattern(block_id).search(page)
        if not m:
            print("sync_lab_selector.py: no %s block found in %s" % (block_id, PAGE), file=sys.stderr)
            return 2
        loaded[block_id] = load()
        want = embedded_text(loaded[block_id])
        if m.group(2) != want:
            stale.append(label)
            if not check:
                page = page[: m.start(2)] + want + page[m.end(2):]
    if not check:
        for warning in WARNINGS:
            print("lab selector data: note: %s" % warning, file=sys.stderr)
    status = 0
    if not stale:
        print("lab selector data: OK (matches lab201-vms.json, flavors.json, lab-catalog.json, and the lab chapters)")
    elif check:
        print("lab selector data: OUT OF DATE (%s). Run: python scripts/python/sync_lab_selector.py" % ", ".join(stale), file=sys.stderr)
        status = 1
    else:
        with open(PAGE, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(page)
        print("lab selector data: updated (%s)" % ", ".join(stale))
    # The documents state some of these numbers in their text. No copy step keeps those in step, so compare them.
    problems, documents = stated_problems(loaded["lab201-labs"], page)
    if problems:
        print("stated numbers: WRONG. A document states a number that the lab chapters or the page do not give:", file=sys.stderr)
        for problem in problems:
            print("  %s" % problem, file=sys.stderr)
        status = 1
    else:
        print("stated numbers: OK (%d numbers in %d documents match the lab chapters and the page)" % (len(STATED), documents))
    # The address plan: the blocks of the Segments table, the same blocks in the manifest, and every address in a block.
    problems, blocks = plan_problems(loaded["lab201-labs"], loaded["lab201-manifest"])
    if problems:
        print("address plan: WRONG. The Segments table of the shared lab, the manifest, and the addresses do not agree:", file=sys.stderr)
        for problem in problems:
            print("  %s" % problem, file=sys.stderr)
        status = 1
    else:
        print("address plan: OK (%d lab networks, no two overlap, and every address of the manifest and of the chapters lies in a block)" % blocks)
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
