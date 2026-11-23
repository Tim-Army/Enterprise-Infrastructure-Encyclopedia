#!/usr/bin/env python3
"""Build lab-scripts/common/fortiswitch-features.json from Fortinet's feature matrix.

Usage: build_fortiswitch_features.py VERSION=MATRIX.txt [VERSION=MATRIX.txt ...]

Fortinet publishes the Feature Matrix for each FortiSwitchOS release as a PDF.
It lists every feature and, in one column for each model series, whether the
series supports it. This script reads the text of that PDF and keeps the rows
the Volume CCI labs use, so the Lab Selector can say which lab features a switch
model supports.

Make each MATRIX.txt from the PDF with xpdf's pdftotext in table mode:

    pdftotext -table FortiSwitch-8.0.0-Feature-Matrix.pdf matrix-8.0.0.txt

The PDF is not kept in the repository. A supported cell is an icon that
pdftotext does not extract, so a cell is read as supported unless it holds
"--". Every "--" sits at the character position of its column's header label;
the script stops if one does not, or if a feature it needs is missing. A cell
can also hold a note, such as the models of the series that have the feature.
"""

import collections
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "volumes", "volume-901-lab-selector", "lab-scripts", "common", "fortiswitch-features.json")

# The column layouts Fortinet has used. Each entry is the start of a header label as
# pdftotext prints it, and the column name used in the output. The first layout whose
# labels are all in a page header is the one in use.
LAYOUTS = [
    [("GUI", "GUI"), ("FSR-108F", "FSR-108F"), ("FSR-112F-", "FSR-112F-POE"), ("FSR-216F-", "FSR-216F-POE"), ("FSR-424F-", "FSR-424F-POE"),
     ("1xxE,", "1xxE, 1xxF"), ("110G-FPOE,", "110G-FPOE, 124G, 124G-FPOE"), ("200", "200 Series"), ("324G,", "324G, 324G-FPOE, 348G, 348G-FPOE"),
     ("4xxE", "4xxE"), ("500", "500 Series"), ("6xxF", "6xxF"), ("1024E,", "1024E, 1048E, 1048G, T1024E, T1024F-FPOE"), ("2048F", "2048F"),
     ("3032E,", "3032E, 3032G")],
    [("GUI", "GUI"), ("FSR-108F", "FSR-108F"), ("FSR-112F-", "FSR-112F-POE"), ("FSR-216F-", "FSR-216F-POE"), ("FSR-424F-", "FSR-424F-POE"),
     ("1xxF", "1xxF"), ("110G-FPOE,", "110G-FPOE, 124G, 124G-FPOE"), ("200", "200 Series"), ("4xxE", "4xxE"), ("6xxF", "6xxF"),
     ("1024E,", "1024E, 1048E, 1048G, T1024E, T1024F-FPOE"), ("2048F", "2048F"), ("3032E,", "3032E, 3032G")],
]
DASH = re.compile(r"(?<![-\w])--(?![-\w])")

# The features the labs use: key, the row label in the matrix, a short name, and the
# words that show a lab uses the feature (matched without case in the lab text).
FEATURES = [
    ("dot1x", "802.1X port mode", "802.1X port authentication", r"802\.1x"),
    ("mab", "802.1X: MAB", "MAC authentication bypass (MAB)", r"\bmab\b|mac authentication bypass"),
    ("radsec", "802.1X: RadSec (IPv4)", "RadSec for 802.1X", r"radsec"),
    ("radius_admin", "RADIUS for administrative authentication", "RADIUS for administrators", r"radius"),
    ("tacacs", "TACACS+ for administrative authentication", "TACACS+ for administrators", r"tacacs"),
    ("dhcp_snooping", "DHCP snooping", "DHCP snooping", r"dhcp[- ]snooping"),
    ("dai", "Dynamic ARP inspection (IPv4)", "Dynamic ARP inspection", r"arp[- ]inspection|dynamic arp"),
    ("ipsg", "IP source guard (IPv4)", "IP source guard", r"ip[- ]source[- ]guard"),
    ("ra_guard", "IPv6 RA guard", "IPv6 RA guard", r"ra[- ]guard"),
    ("storm", "Storm control", "Storm control", r"storm[- ]control"),
    ("loop_guard", "Loop guard", "Loop guard", r"loop[- ]guard"),
    ("root_guard", "STP root guard", "STP root guard", r"root[- ]guard"),
    ("bpdu_guard", "STP BPDU guard", "STP BPDU guard", r"bpdu[- ]guard"),
    ("igmp", "IGMP snooping", "IGMP snooping", r"igmp[- ]snooping"),
    ("mac_limit", "MAC learning limit", "MAC learning limit", r"learning[- ]limit"),
    ("sticky_mac", "Sticky MAC", "Sticky MAC", r"sticky"),
    ("pvlan", "Private VLANs", "Private VLANs", r"private vlan"),
    ("span", "SPAN", "Port mirroring (SPAN)", r"\bspan\b|port mirroring"),
    ("erspan", "RSPAN and ERSPAN (IPv4)", "RSPAN and ERSPAN", r"erspan|rspan"),
    ("sflow", "sFlow (IPv4)", "sFlow", r"sflow"),
    ("flow_export", "Flow export (IPv4)", "Flow export (NetFlow and IPFIX)", r"netflow|ipfix|flow[- ]export"),
    ("macsec", "MACsec: PSK mode", "MACsec", r"macsec"),
    ("acl_in4", "ACL (IPv4 ingress)", "IPv4 ingress ACL", r"\bacl\b"),
    ("acl_out4", "ACL (IPv4 egress)", "IPv4 egress ACL", r"egress acl|acl[^.\n]{0,20}egress"),
    ("acl_in6", "ACL (IPv6 ingress)", "IPv6 ingress ACL", r"ipv6 acl|acl[^.\n]{0,20}ipv6"),
    ("syslog_tls", "Reliable syslog", "Reliable syslog", r"reliable syslog|reliable \(tcp\) syslog"),
    ("fips", "FIPS 140-3 (Level 1) and CC support", "FIPS-CC mode", r"fips"),
    ("static_route", "Static routing (IPv4/IPv6)", "Static routing", r"static rout"),
    ("urpf", "uRPF", "Unicast reverse-path forwarding (uRPF)", r"urpf|reverse[- ]path"),
    ("pbr", "Policy-based routing (IPv4)", "Policy-based routing", r"policy[- ]based routing"),
    ("vrf", "VRF (IPv4/IPv6)", "VRF", r"\bvrf\b"),
    ("ospf", "OSPF (IPv4/IPv6)", "OSPF", r"\bospf"),
    ("rip", "RIP (IPv4/IPv6)", "RIP", r"\brip\b"),
    ("vrrp", "VRRP (IPv4/IPv6)", "VRRP", r"vrrp"),
    ("bgp", "BGP (IPv4/IPv6)", "BGP", r"\bbgp\b"),
    ("isis", "IS-IS (IPv4/IPv6)", "IS-IS", r"is-is"),
    ("pim", "PIM-SSM (IPv4)", "PIM-SSM", r"\bpim\b"),
    ("evpn", "VXLAN: BGP EVPN", "VXLAN BGP EVPN", r"evpn"),
    ("dhcp_relay", "DHCP relay (IPv4)", "DHCP relay", r"dhcp[- ]relay"),
]


def header_positions(lines):
    """Return the character position and the name of every column of a page, or None."""
    for line in lines:
        if "FSR-108F" in line and "GUI" in line:
            for layout in LAYOUTS:
                pos = [line.find(label) for label, _name in layout]
                if min(pos) >= 0 and pos == sorted(pos):
                    return pos, [name for _label, name in layout]
    return None


def column_of(x, pos):
    """A cell is centered under its header, so it starts at or after the start of the label and before the next label.

    Returns the column and how far the cell is from the start of the label.
    """
    col = 0
    for c, start in enumerate(pos):
        if start <= x:
            col = c
    return col, x - pos[col]


def clean(label):
    return re.sub(r"\s*\(See notes?[^)]*\)?\s*$", "", re.sub(r"\s+", " ", label)).strip()


def parse(text):
    """Return the rows of the matrix: label, the columns that hold "--", and the notes in cells."""
    rows, problems = [], []
    for page_no, page in enumerate(text.split("\f"), 1):
        lines = page.split("\n")
        header = header_positions(lines)
        if not header:
            continue
        pos, names = header
        first_col = pos[0]
        current = None
        for line in lines:
            if not line.strip() or ("FSR-108F" in line and "GUI" in line):
                continue
            label = line[:first_col].strip()
            rest = line[first_col:]
            dashes = []
            for m in DASH.finditer(line):
                col, dist = column_of(m.start(), pos)
                if dist < 0 or dist > 14:
                    problems.append("page %d: a dash at character %d is %d from the start of a column: %s" % (page_no, m.start(), dist, line.strip()[:60]))
                dashes.append(names[col])
            notes = [(names[column_of(m.start() + first_col, pos)[0]], m.group(0).strip())
                     for m in re.finditer(r"\S+(?: {1,2}\S+)*", DASH.sub("  ", rest))]
            if label:
                starts_new = True
                if current is not None:
                    prev = current["label"]
                    wrapped = re.match(r"^[a-z(]|^\d+\.\s*\)|^and |^or |^of ", label) and not re.match(r"^(uRPF|sFlow|iBGP|eBGP|mDNS)", label)
                    if prev.count("(") > prev.count(")") or wrapped or prev.endswith(("-", " and", " of", " for", " in", ",", "/", " to", " the")):
                        starts_new = False
                if starts_new:
                    current = {"label": label, "page": page_no, "no": [], "notes": [], "columns": names}
                    rows.append(current)
                else:
                    current["label"] += " " + label
            if current is None:
                continue
            current["no"].extend(d for d in dashes if d not in current["no"])
            current["notes"].extend(notes)
    return rows, problems


def features_of(version, path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    title = re.search(r"Feature Matrix for FortiSwitchOS\s+([0-9.]+)", text)
    if not title or title.group(1) != version:
        raise SystemExit("%s is not the feature matrix for FortiSwitchOS %s" % (path, version))
    rows, problems = parse(text)
    if problems:
        raise SystemExit("could not place every cell of %s:\n  %s" % (path, "\n  ".join(problems[:10])))
    by_label = collections.OrderedDict()
    for r in rows:
        by_label.setdefault(clean(r["label"]), r)
    out = []
    for key, label, name, _words in FEATURES:
        row = by_label.get(label)
        if not row:
            # A feature the release does not list is not available in it.
            out.append({"key": key, "name": name, "row": label, "listed": False})
            continue
        notes = collections.OrderedDict()
        for col, note in row["notes"]:
            if col != "GUI":
                notes.setdefault(col, []).append(note)
        out.append({"key": key, "name": name, "row": label, "listed": True, "page": row["page"],
                    "unsupported": [c for c in row["columns"] if c in row["no"] and c != "GUI"],
                    "notes": {k: re.sub(r"\s+", " ", " ".join(v)) for k, v in notes.items()}})
    series = [c for c in rows[0]["columns"] if c != "GUI"] if rows else []
    return {"rows_read": len(rows), "series": series, "features": out}


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    versions = collections.OrderedDict()
    for spec in argv[1:]:
        version, _, path = spec.partition("=")
        versions[version] = features_of(version, path)
        missing = [f["row"] for f in versions[version]["features"] if not f["listed"]]
        print("FortiSwitchOS %s: %d rows read, %d of %d lab features listed%s" % (
            version, versions[version]["rows_read"], len(FEATURES) - len(missing), len(FEATURES),
            (" (not listed: %s)" % "; ".join(missing)) if missing else ""))
    data = {
        "description": "Which FortiSwitch model series support the features the Volume CCI labs use, read from Fortinet's Feature Matrix "
                       "for each FortiSwitchOS release by scripts/python/build_fortiswitch_features.py. A series is supported unless it is "
                       "listed as unsupported. A note names the models of a series that have the feature, or a limit. The matrix lists "
                       "model series, not every model, so check the matrix for your exact model before you rely on a feature.",
        "source": "Fortinet, Feature Matrix for FortiSwitchOS (PDF), https://docs.fortinet.com/product/fortiswitch",
        "keywords": collections.OrderedDict((key, words) for key, _label, _name, words in FEATURES),
        "versions": versions,
    }
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print("wrote %s" % os.path.relpath(OUT, ROOT).replace(os.sep, "/"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
