#!/usr/bin/env python3
"""Write DISA STIG Viewer checklists (.cklb or .ckl) from the results of the SRG requirement labs.

    python make-ckl.py --results lab201-results.csv --disa <folder, zip, or xccdf file> [--format cklb|ckl|both] [--out checklists]

It joins three things:

- the results file that the Lab Selector saves (Download results (CSV)): one row for each SRG
  requirement, with its lab, the device it was tested on, and the result;
- the benchmark files of DISA (the SRG zips from the DoD Cyber Exchange, or the whole library
  zip): the rules of each SRG, with their check and fix texts. This script does not download them;
- the lab chapters: whether the product meets the requirement, meets part of it, cannot meet it,
  or does not have what the requirement is about.

It writes one checklist for each device and SRG. The format is .cklb, the JSON format of STIG
Viewer 3, unless --format asks for .ckl, the XML format of STIG Viewer 2, or for both. A checklist
holds every rule of the SRG. A rule that no lab tests on the device stays Not Reviewed.

DISA publishes a schema for .ckl (checklist schema 2.5) and none for .cklb. So a .cklb file
follows the files that STIG Viewer 3 saves: the same keys, in the same order, with the same kinds
of values.

How a lab result becomes a status:

    result of the lab          what the chapters say            status
    pass                       the product meets it             Not a Finding
    pass                       the product meets part of it     Open
    pass                       gap lab: it cannot meet it       Open
    pass                       gap lab: not applicable          Not Applicable
    fail                       anything                         Open
    blocked, skipped, none     anything                         Not Reviewed

A gap lab passes when it shows that the setting is absent and that the compensating control
works. So its pass is a finding for the requirement, and never a Not a Finding.

The status is a proposal. Read the finding details and the lab before you sign a checklist.

Python 3.8 or later, with no other package.
"""
import argparse
import csv
import io
import json
import os
import re
import sys
import uuid
import zipfile
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
XCCDF = "http://checklists.nist.gov/xccdf/1.1"
NS = {"x": XCCDF, "dc": "http://purl.org/dc/elements/1.1/"}
# The largest benchmark file that is read into memory. The largest of DISA's own is a few megabytes.
MAX_BYTES = 64 * 1024 * 1024

SRG_ID = re.compile(r"^SRG-[A-Z]+-\d{6}-[A-Z0-9]+-\d{6}$")
# A lab heading and a requirement row of a lab chapter:
#   ### Lab 4.9 — Gaps: VTP and UDLD
#   | `SRG-NET-000512-L2S-000004` | II | Enable UDLD ... | Not supported | FortiSwitchOS 7.6.7 CLI Reference p127 |
LAB_HEADING = re.compile(r"^### Lab (\d+\.\d+) — (.+?)\s*$")
SRG_ROW = re.compile(r"^\| `(SRG-[A-Z]+-\d{6}-[A-Z0-9]+-\d{6})` \| (I{1,3}) \| ([^|]*) \|(?: ([^|]*) \|)?")
# The header of a requirement table, with the name of its fourth column.
TABLE_HEAD = re.compile(r"^\| SRG ID \| CAT \| Requirement \|(?: ([^|]*) \|)?")
# The names that the Lab Selector gives the two switches under test, in the order of a row for both.
SWITCH_ROLES = ("Access switch", "Aggregation switch")
BOTH_SWITCHES = "Both switches"

# What the lab chapters say about a requirement.
MEETS, PARTIAL, GAP, NOT_APPLICABLE, UNKNOWN = "meets", "partial", "gap", "not applicable", "unknown"
# The statuses of a checklist, as the schema names them.
NOT_A_FINDING, OPEN, NA, NOT_REVIEWED = "NotAFinding", "Open", "Not_Applicable", "Not_Reviewed"
STATUS_TEXT = {NOT_A_FINDING: "Not a Finding", OPEN: "Open", NA: "Not Applicable", NOT_REVIEWED: "Not Reviewed"}

# The checklist schema 2.5 of STIG Viewer 2: the order of the elements and the values that it allows.
ASSET_ORDER = ["ROLE", "ASSET_TYPE", "MARKING", "HOST_NAME", "HOST_IP", "HOST_MAC", "HOST_GUID", "HOST_FQDN", "TARGET_COMMENT",
               "TECH_AREA", "TARGET_KEY", "STIG_GUID", "WEB_OR_DATABASE", "WEB_DB_SITE", "WEB_DB_INSTANCE"]
ASSET_OPTIONAL = {"MARKING", "HOST_GUID", "TARGET_COMMENT", "STIG_GUID"}
ROLES = {"None", "Workstation", "Member Server", "Domain Controller"}
ASSET_TYPES = {"Computing", "Non-Computing"}
TECH_AREAS = {"", "Application Review", "Boundary Security", "CDS Admin Review", "CDS Technical Review", "Database Review",
              "Domain Name System (DNS)", "Exchange Server", "Host Based System Security (HBSS)", "Internal Network", "Mobility",
              "Releasable Networks (REL)", "Releaseable Networks (REL)", "Traditional Security", "UNIX OS", "VVOIP Review",
              "Web Review", "Windows OS", "Other Review"}
SID_NAMES = ["version", "classification", "customname", "stigid", "description", "filename", "releaseinfo", "title", "uuid", "notice", "source"]
# The fields of a rule, in the order in which STIG Viewer writes them. LEGACY_ID and CCI_REF can repeat.
VULN_ATTRIBUTES = ["Vuln_Num", "Severity", "Group_Title", "Rule_ID", "Rule_Ver", "Rule_Title", "Vuln_Discuss", "IA_Controls",
                   "Check_Content", "Fix_Text", "False_Positives", "False_Negatives", "Documentable", "Mitigations",
                   "Potential_Impact", "Third_Party_Tools", "Mitigation_Control", "Responsibility", "Security_Override_Guidance",
                   "Check_Content_Ref", "Weight", "Class", "STIGRef", "TargetKey", "STIG_UUID", "LEGACY_ID", "CCI_REF"]
VULN_TAIL = ["STATUS", "FINDING_DETAILS", "COMMENTS", "SEVERITY_OVERRIDE", "SEVERITY_JUSTIFICATION"]
STATUSES = {NOT_A_FINDING, OPEN, NA, NOT_REVIEWED}
SEVERITY_OVERRIDES = {"", "low", "medium", "high"}
# The .cklb format of STIG Viewer 3. DISA publishes no schema for it, so these are the keys of a file that STIG
# Viewer 3 saved, in its order, and the words that it uses for the statuses.
CKLB_STATUS = {NOT_A_FINDING: "not_a_finding", OPEN: "open", NA: "not_applicable", NOT_REVIEWED: "not_reviewed"}
CKLB_TOP = ["title", "id", "stigs", "active", "mode", "has_path", "target_data", "cklb_version"]
CKLB_TARGET = ["target_type", "host_name", "ip_address", "mac_address", "fqdn", "comments", "role", "is_web_database",
               "technology_area", "web_db_site", "web_db_instance", "classification"]
CKLB_STIG = ["stig_name", "display_name", "stig_id", "release_info", "version", "uuid", "reference_identifier", "size", "rules"]
CKLB_RULE = ["group_id_src", "group_tree", "group_id", "severity", "group_title", "rule_id_src", "rule_id", "rule_version",
             "rule_title", "fix_text", "weight", "check_content", "check_content_ref", "classification", "discussion",
             "false_positives", "false_negatives", "documentable", "security_override_guidance", "potential_impacts",
             "third_party_tools", "ia_controls", "responsibility", "mitigations", "mitigation_control", "legacy_ids", "ccis",
             "reference_identifier", "uuid", "stig_uuid", "status", "overrides", "comments", "finding_details"]
# The text fields of a rule in a .cklb file, each with the name that it has in a .ckl file.
CKLB_FIELDS = [("discussion", "Vuln_Discuss"), ("false_positives", "False_Positives"), ("false_negatives", "False_Negatives"),
               ("documentable", "Documentable"), ("security_override_guidance", "Security_Override_Guidance"),
               ("potential_impacts", "Potential_Impact"), ("third_party_tools", "Third_Party_Tools"), ("ia_controls", "IA_Controls"),
               ("responsibility", "Responsibility"), ("mitigations", "Mitigations"), ("mitigation_control", "Mitigation_Control")]
UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
# What --format can ask for, and the kinds of file that each one writes.
FORMATS = {"cklb": ("cklb",), "ckl": ("ckl",), "both": ("cklb", "ckl")}
# The parts of a rule's description in a benchmark, and the checklist field of each.
DESCRIPTION_PARTS = [("VulnDiscussion", "Vuln_Discuss"), ("IAControls", "IA_Controls"), ("FalsePositives", "False_Positives"),
                     ("FalseNegatives", "False_Negatives"), ("Documentable", "Documentable"), ("Mitigations", "Mitigations"),
                     ("PotentialImpacts", "Potential_Impact"), ("ThirdPartyTools", "Third_Party_Tools"),
                     ("MitigationControl", "Mitigation_Control"), ("Responsibility", "Responsibility"),
                     ("SeverityOverrideGuidance", "Security_Override_Guidance")]


class Problem(Exception):
    """Something in the input that stops the run, with a message for the person at the keyboard."""


def say(text):
    print(text)


# The notes of a run. The self-test reads them and keeps them off the screen.
NOTES, QUIET = [], [False]


def warn(text):
    NOTES.append(text)
    if not QUIET[0]:
        print("make-ckl.py: note: %s" % text, file=sys.stderr)


# ------------------------------------------------------------------ the results file of the Lab Selector

def clean_cell(value):
    """A cell of the results file. The Lab Selector puts an apostrophe before a cell that starts like a formula."""
    value = (value or "").strip()
    if value[:1] == "'" and value[1:2] in ("=", "+", "-", "@"):
        value = value[1:]
    return value


def read_results(path):
    """The rows of the results file, each as a dictionary with the names of its header."""
    with io.open(path, "r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        names = reader.fieldnames or []
        missing = [n for n in ("SRG ID", "Lab", "Tested on", "Result") if n not in names]
        if missing:
            raise Problem("%s is not a results file of the Lab Selector: it has no column %s" % (path, ", ".join(missing)))
        rows = []
        for line in reader:
            row = dict((k, clean_cell(v)) for k, v in line.items() if k)
            row["SRG ID"] = row["SRG ID"].upper()
            row["Lab"] = row["Lab"].lower()
            row["Result"] = row["Result"].lower()
            if SRG_ID.match(row["SRG ID"]):
                rows.append(row)
    if not rows:
        raise Problem("%s has no row with an SRG ID" % path)
    return rows


def devices_of(row):
    """The devices that a row was tested on, each as (key, model).

    A lab of the switch lab set names a switch by its role, or both switches, and gives the models. A lab of
    another lab set names its unit under test.
    """
    tested, models = row.get("Tested on", ""), [m.strip() for m in row.get("Switch model", "").split(" and ") if m.strip()]
    if tested == BOTH_SWITCHES:
        return [(role, models[i] if i < len(models) else "") for i, role in enumerate(SWITCH_ROLES)]
    if not tested:
        return []
    return [(tested, models[0] if models else "")]


# ------------------------------------------------------------------ the lab chapters

def chapter_files(catalog_path, walkthroughs):
    """The lab chapters of every lab set, as (lab prefix, path).

    The catalog names them. They are in the walkthroughs folder under their short names (the published folder and
    the zip of the Lab Selector), or in the volumes of the repository under their own names.
    """
    with io.open(catalog_path, "r", encoding="utf-8") as fh:
        catalog = json.load(fh)
    repo = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(catalog_path)), "..", "..", ".."))
    folders = [walkthroughs] if walkthroughs else [os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(catalog_path)), "..", "walkthroughs"))]
    found, missing = [], []
    for entry in catalog.get("sets", []):
        for chapter in entry.get("chapters", []):
            places = [os.path.join(folder, chapter.get("short", "")) for folder in folders]
            if not walkthroughs:
                places.append(os.path.join(repo, entry.get("volume", ""), "chapters", chapter.get("file", "")))
            hit = [p for p in places if os.path.isfile(p)]
            if hit:
                found.append((entry.get("prefix", ""), hit[0]))
            else:
                missing.append(chapter.get("short") or chapter.get("file"))
    return found, missing


def read_requirements(chapters):
    """What the lab chapters say about each requirement of each lab: {(lab id, SRG ID): {...}}.

    A lab whose title starts with "Gap" is a gap lab: the product cannot meet its requirements. In the chapters
    of the switch lab set, the fourth cell of a row is its alignment in the crosswalk, and it tells a requirement
    that is not applicable from one that is not supported, and names one that is met in part.
    """
    known = {}
    for prefix, path in chapters:
        with io.open(path, "r", encoding="utf-8") as fh:
            lab = title = None
            support_words = False
            for line in fh.read().split("\n"):
                heading = LAB_HEADING.match(line)
                if heading:
                    lab, title = (prefix + "-" if prefix else "") + heading.group(1), heading.group(2)
                    support_words = False
                    continue
                head = TABLE_HEAD.match(line)
                if head:
                    # Only a column that is named Alignment can say how far the product meets a requirement. In another
                    # table the fourth column is free text, such as a list of features.
                    support_words = (head.group(1) or "").strip().lower().startswith("alignment")
                    continue
                row = SRG_ROW.match(line)
                if not row or not lab:
                    continue
                align, gap_lab = (row.group(4) or "").strip() if support_words else "", title.lower().startswith("gap")
                word = align.lower()
                if word.startswith("not applicable"):
                    kind = NOT_APPLICABLE
                elif word.startswith("not supported"):
                    kind = GAP
                elif word.startswith("partial"):
                    kind = PARTIAL
                else:
                    kind, align = (GAP if gap_lab else MEETS), ""
                known[(lab, row.group(1))] = {"kind": kind, "align": align, "gap_lab": gap_lab, "title": title}
    return known


# ------------------------------------------------------------------ the benchmarks of DISA

def release_number(info):
    m = re.search(r"Release:\s*(\d+)", info or "")
    return int(m.group(1)) if m else 0


def unescape(text):
    """The description of a rule is XML text inside an XML element, so a mark in it is escaped a second time."""
    for mark, char in (("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"'), ("&apos;", "'"), ("&amp;", "&")):
        text = text.replace(mark, char)
    return text


def parse_benchmark(data, name):
    """A benchmark (XCCDF 1.1) as a dictionary, or None when the data is something else."""
    head = data[:4096]
    if b"<!DOCTYPE" in data or b"<!ENTITY" in data:
        warn("%s has a document type declaration, which a benchmark of DISA does not have. It was not read" % name)
        return None
    if b"Benchmark" not in head:
        return None
    try:
        root = ET.fromstring(data)
    except ET.ParseError as err:
        warn("%s is not well-formed XML (%s). It was not read" % (name, err))
        return None
    if root.tag != "{%s}Benchmark" % XCCDF:
        return None
    text = lambda node, path: (node.findtext(path, "", NS) or "").strip()
    release = ""
    for plain in root.findall("x:plain-text", NS):
        if plain.get("id") == "release-info":
            release = (plain.text or "").strip()
    notice = root.find("x:notice", NS)
    bench = {"id": root.get("id") or "", "title": text(root, "x:title"), "description": text(root, "x:description"),
             "version": text(root, "x:version"), "release": release, "notice": notice.get("id") if notice is not None else "",
             "source": text(root, "x:reference/dc:source"), "filename": os.path.basename(name.replace("\\", "/")), "from": name, "rules": []}
    for group in root.iter("{%s}Group" % XCCDF):
        rule = group.find("x:Rule", NS)
        if rule is None:
            continue
        description = rule.findtext("x:description", "", NS) or ""
        parts = {}
        for tag, field in DESCRIPTION_PARTS:
            m = re.search(r"<%s>(.*?)</%s>" % (tag, tag), description, re.S)
            parts[field] = unescape(m.group(1).strip()) if m else ""
        ref = rule.find("x:check/x:check-content-ref", NS)
        legacy, cci = [], []
        for ident in rule.findall("x:ident", NS):
            (legacy if "legacy" in (ident.get("system") or "") else cci).append((ident.text or "").strip())
        fields = {"Vuln_Num": group.get("id") or "", "Severity": rule.get("severity") or "", "Group_Title": text(group, "x:title"),
                  "Rule_ID": rule.get("id") or "", "Rule_Ver": text(rule, "x:version"), "Rule_Title": text(rule, "x:title"),
                  "Check_Content": text(rule, "x:check/x:check-content"), "Fix_Text": text(rule, "x:fixtext"),
                  "Check_Content_Ref": ref.get("name") if ref is not None and ref.get("name") else "M",
                  "Weight": rule.get("weight") or "10.0", "Class": "Unclass", "TargetKey": text(rule, "x:reference/dc:identifier")}
        fields.update(parts)
        bench["rules"].append({"fields": fields, "legacy": legacy, "cci": cci, "group_description": text(group, "x:description"),
                               "check_href": ref.get("href") if ref is not None and ref.get("href") else ""})
    bench["uuid"] = str(uuid.uuid5(uuid.NAMESPACE_URL, "disa-benchmark:%s:%s:%s" % (bench["id"], bench["version"], bench["release"])))
    return bench if bench["rules"] else None


def members_of(archive, label, only_srg):
    """The benchmark files inside a zip of DISA, and inside the zips that the library zip holds."""
    for info in archive.infolist():
        name = info.filename
        if info.is_dir() or info.file_size > MAX_BYTES:
            continue
        low = name.lower()
        if low.endswith("xccdf.xml"):
            yield "%s!%s" % (label, name), archive.read(info)
        elif low.endswith(".zip") and (not only_srg or "srg" in os.path.basename(low)):
            try:
                inner = zipfile.ZipFile(io.BytesIO(archive.read(info)))
            except zipfile.BadZipFile:
                continue
            for item in members_of(inner, "%s!%s" % (label, name), only_srg):
                yield item


def benchmark_data(paths, only_srg):
    """Every benchmark file under the paths that were given, as (name, bytes). Nothing is unpacked to disk."""
    for path in paths:
        if os.path.isdir(path):
            names = sorted(os.listdir(path))
            files = [os.path.join(path, n) for n in names if n.lower().endswith((".zip", ".xml"))]
        elif os.path.isfile(path):
            files = [path]
        else:
            raise Problem("%s was not found" % path)
        for file in files:
            low = os.path.basename(file).lower()
            direct = file in paths
            if low.endswith(".xml"):
                if os.path.getsize(file) <= MAX_BYTES:
                    with open(file, "rb") as fh:
                        yield file, fh.read()
            elif low.endswith(".zip") and (direct or not only_srg or "srg" in low):
                try:
                    with zipfile.ZipFile(file) as archive:
                        for item in members_of(archive, file, only_srg and not direct):
                            yield item
                except zipfile.BadZipFile:
                    warn("%s is not a zip file. It was not read" % file)


def find_benchmarks(paths, wanted):
    """The benchmarks that hold a rule for a requirement of the results file: the newest release of each."""
    best = {}
    for only_srg in (True, False):
        for name, data in benchmark_data(paths, only_srg):
            bench = parse_benchmark(data, name)
            if not bench or not any(rule["fields"]["Rule_Ver"] in wanted for rule in bench["rules"]):
                continue
            key = (int(bench["version"]) if bench["version"].isdigit() else 0, release_number(bench["release"]))
            if bench["id"] not in best or key > best[bench["id"]][0]:
                best[bench["id"]] = (key, bench)
        if best:
            break
    return [best[k][1] for k in sorted(best)]


# ------------------------------------------------------------------ the status of a rule

def status_of(kind, result):
    """The status that a lab result gives a requirement. See the table at the top of this file."""
    if result == "fail":
        return OPEN
    if result != "pass":
        return NOT_REVIEWED
    return {MEETS: NOT_A_FINDING, PARTIAL: OPEN, GAP: OPEN, NOT_APPLICABLE: NA}.get(kind, NOT_REVIEWED)


def merge(statuses):
    """One status for a rule that more than one lab tests on a device."""
    if not statuses:
        return NOT_REVIEWED
    if OPEN in statuses:
        return OPEN
    return statuses[0] if len(set(statuses)) == 1 else NOT_REVIEWED


def lab_name(row):
    title = row.get("Lab title", "")
    return "Lab %s" % row["Lab"] + (" (%s)" % title if title else "")


def why(kind, result, row, known):
    """One sentence that says why a result became its status, where the two words differ."""
    lab = "Lab %s" % row["Lab"]
    if result == "fail":
        return "Status Open: the lab failed."
    if result in ("blocked", "skipped"):
        return "Status Not Reviewed: the lab was %s." % result
    if result != "pass":
        return ""
    if kind == PARTIAL:
        return "Status Open: the lab passed, and the crosswalk says that the product meets only part of this requirement."
    if kind == GAP:
        return "Status Open: %s is a gap lab. It passed, which shows that the product cannot meet this requirement and that the compensating control of the lab works." % lab
    if kind == NOT_APPLICABLE:
        return "Status Not Applicable: %s is a gap lab. It passed, which shows that the product does not have what this requirement is about." % lab
    if kind == UNKNOWN:
        return "Status Not Reviewed: the lab chapters do not list this requirement in %s, so the script cannot tell what a pass means." % lab
    return ""


def rule_entry(rule_ver, device, rows, known):
    """The status, the finding details, and the comments of one rule on one device."""
    mine = [r for r in rows.get(rule_ver, []) if any(key == device["key"] for key, _ in devices_of(r))]
    others = [r for r in rows.get(rule_ver, []) if r not in mine]
    statuses, details, comments = [], [], []
    for row in mine:
        info = known.get((row["Lab"], rule_ver))
        kind, result = (info["kind"] if info else UNKNOWN), row["Result"]
        statuses.append(status_of(kind, result))
        note = "%s tests this requirement on this device." % lab_name(row)
        if info and info["align"]:
            note += " Alignment in the crosswalk: %s." % info["align"]
        elif info and info["gap_lab"]:
            note += " It is a gap lab."
        if row.get("Planned", "").lower() == "no":
            note += " The lab is not in the lab plan of this build."
        comments.append(note)
        if result in ("pass", "fail", "blocked", "skipped"):
            lines = ["%s: %s%s." % (lab_name(row), result, " on %s" % row["Date"] if row.get("Date") else "")]
            on = [x for x in (row.get("Tested on"), row.get("Switch model"), "FortiSwitchOS %s" % row["FortiSwitchOS"] if row.get("FortiSwitchOS") else "") if x]
            lines.append("Tested on: %s." % ", ".join(on))
            if row.get("Result comes from"):
                lines.append("The result comes from: %s of PROGRESS.md." % row["Result comes from"])
            if row.get("Evidence"):
                lines.append("Evidence: %s" % row["Evidence"])
            if row.get("Note"):
                lines.append("Note: %s" % row["Note"])
            reason = why(kind, result, row, known)
            if reason:
                lines.append(reason)
            details.append("\n".join(lines))
    for row in others:
        comments.append("%s tests this requirement on another device (%s), not on this one." % (lab_name(row), row.get("Tested on", "")))
    if not mine and not others:
        comments.append("No lab in the results file tests this requirement.")
    return merge(statuses), "\n\n".join(details), "\n".join(comments), bool(mine)


# ------------------------------------------------------------------ the checklist file

def xml_text(value):
    """Text for an XML element: without the characters that XML 1.0 does not allow, and with its marks escaped."""
    value = (value or "").replace("\r\n", "\n").replace("\r", "\n")
    kept = []
    for ch in value:
        code = ord(ch)
        if ch in "\t\n" or 0x20 <= code <= 0xD7FF or 0xE000 <= code <= 0xFFFD or code >= 0x10000:
            kept.append(ch)
    return "".join(kept).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def element(tabs, name, value):
    return "%s<%s>%s</%s>" % ("\t" * tabs, name, xml_text(value), name)


def checklist_text(device, bench, entries, marking):
    """The text of one checklist: one device, one benchmark, and an entry for each of its rules."""
    target_key = next((r["fields"]["TargetKey"] for r in bench["rules"] if r["fields"]["TargetKey"]), "")
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           "<!--Made by make-ckl.py, a lab script of the Enterprise Infrastructure Encyclopedia. STIG Viewer checklist schema 2.5.-->",
           "<CHECKLIST>", "\t<ASSET>", element(2, "ROLE", "None"), element(2, "ASSET_TYPE", "Computing")]
    if marking:
        out.append(element(2, "MARKING", marking))
    out += [element(2, "HOST_NAME", device["host"]), element(2, "HOST_IP", device["ip"]), element(2, "HOST_MAC", device["mac"]),
            element(2, "HOST_FQDN", device["fqdn"]), element(2, "TARGET_COMMENT", device["comment"]), element(2, "TECH_AREA", ""),
            element(2, "TARGET_KEY", target_key), element(2, "WEB_OR_DATABASE", "false"), element(2, "WEB_DB_SITE", ""),
            element(2, "WEB_DB_INSTANCE", ""), "\t</ASSET>", "\t<STIGS>", "\t\t<iSTIG>", "\t\t\t<STIG_INFO>"]
    info = {"version": bench["version"], "classification": "UNCLASSIFIED", "customname": None, "stigid": bench["id"],
            "description": bench["description"], "filename": bench["filename"], "releaseinfo": bench["release"], "title": bench["title"],
            "uuid": bench["uuid"], "notice": bench["notice"], "source": bench["source"]}
    for name in SID_NAMES:
        out += ["\t\t\t\t<SI_DATA>", element(5, "SID_NAME", name)]
        if info[name] is not None:
            out.append(element(5, "SID_DATA", info[name]))
        out.append("\t\t\t\t</SI_DATA>")
    out.append("\t\t\t</STIG_INFO>")
    stig_ref = "%s :: Version %s, %s" % (bench["title"], bench["version"], bench["release"])
    for rule, (status, details, comments, _) in zip(bench["rules"], entries):
        fields = dict(rule["fields"], STIGRef=stig_ref, STIG_UUID=bench["uuid"])
        out.append("\t\t\t<VULN>")
        for name in VULN_ATTRIBUTES:
            # STIG Viewer writes two LEGACY_ID fields also for a rule that has none.
            values = (rule["legacy"] + ["", ""])[:max(2, len(rule["legacy"]))] if name == "LEGACY_ID" else rule["cci"] if name == "CCI_REF" else [fields.get(name, "")]
            for value in values:
                out += ["\t\t\t\t<STIG_DATA>", element(5, "VULN_ATTRIBUTE", name), element(5, "ATTRIBUTE_DATA", value), "\t\t\t\t</STIG_DATA>"]
        out += [element(4, "STATUS", status), element(4, "FINDING_DETAILS", details), element(4, "COMMENTS", comments),
                element(4, "SEVERITY_OVERRIDE", ""), element(4, "SEVERITY_JUSTIFICATION", ""), "\t\t\t</VULN>"]
    out += ["\t\t</iSTIG>", "\t</STIGS>", "</CHECKLIST>", ""]
    return "\n".join(out)


def checklist_problems(text):
    """What in a checklist does not follow the checklist schema 2.5. An empty list means that it does."""
    problems = []
    try:
        root = ET.fromstring(text.encode("utf-8"))
    except ET.ParseError as err:
        return ["it is not well-formed XML: %s" % err]

    def in_order(node, order, optional, where):
        names = [child.tag for child in node]
        rest = list(names)
        for name in order:
            if rest and rest[0] == name:
                rest.pop(0)
            elif name not in optional:
                problems.append("%s: %s is missing or out of order" % (where, name))
                return
        if rest:
            problems.append("%s: %s is not expected there" % (where, rest[0]))

    if root.tag != "CHECKLIST" or [c.tag for c in root] != ["ASSET", "STIGS"]:
        return ["the root is not CHECKLIST with ASSET and STIGS"]
    asset = root.find("ASSET")
    in_order(asset, ASSET_ORDER, ASSET_OPTIONAL, "ASSET")
    for name, allowed in (("ROLE", ROLES), ("ASSET_TYPE", ASSET_TYPES), ("TECH_AREA", TECH_AREAS), ("WEB_OR_DATABASE", {"true", "false", "0", "1"})):
        if (asset.findtext(name) or "") not in allowed:
            problems.append("ASSET: %s has the value %r" % (name, asset.findtext(name)))
    stigs = list(root.find("STIGS"))
    if not stigs or any(s.tag != "iSTIG" for s in stigs):
        problems.append("STIGS has to hold iSTIG elements only, and one at least")
    for stig in stigs:
        children = [c.tag for c in stig]
        if children[:1] != ["STIG_INFO"] or len(children) < 2 or any(c != "VULN" for c in children[1:]):
            problems.append("iSTIG has to hold STIG_INFO and then VULN elements")
            continue
        for item in stig.find("STIG_INFO"):
            tags = [c.tag for c in item]
            if item.tag != "SI_DATA" or tags not in (["SID_NAME"], ["SID_NAME", "SID_DATA"]) or item.findtext("SID_NAME") not in SID_NAMES:
                problems.append("STIG_INFO: an SI_DATA element is wrong (%s)" % item.findtext("SID_NAME"))
        for vuln in stig.findall("VULN"):
            tags = [c.tag for c in vuln]
            count = len([t for t in tags if t == "STIG_DATA"])
            number = next((d.findtext("ATTRIBUTE_DATA") for d in vuln.findall("STIG_DATA") if d.findtext("VULN_ATTRIBUTE") == "Vuln_Num"), "?")
            if count < 1 or tags != ["STIG_DATA"] * count + VULN_TAIL:
                problems.append("VULN %s: its elements are missing or out of order" % number)
                continue
            for data in vuln.findall("STIG_DATA"):
                if [c.tag for c in data] != ["VULN_ATTRIBUTE", "ATTRIBUTE_DATA"] or data.findtext("VULN_ATTRIBUTE") not in VULN_ATTRIBUTES:
                    problems.append("VULN %s: a STIG_DATA element is wrong (%s)" % (number, data.findtext("VULN_ATTRIBUTE")))
            if vuln.findtext("STATUS") not in STATUSES:
                problems.append("VULN %s: the status %r is not one of the schema" % (number, vuln.findtext("STATUS")))
            if (vuln.findtext("SEVERITY_OVERRIDE") or "") not in SEVERITY_OVERRIDES:
                problems.append("VULN %s: the severity override %r is not one of the schema" % (number, vuln.findtext("SEVERITY_OVERRIDE")))
    return problems


# ------------------------------------------------------------------ the checklist file of STIG Viewer 3 (.cklb)

def plain_text(value):
    """Text for a JSON value: with one kind of line end, and without control characters."""
    value = (value or "").replace("\r\n", "\n").replace("\r", "\n")
    return "".join(ch for ch in value if ch in "\t\n" or ord(ch) >= 0x20)


def short_title(title):
    """The name of a benchmark without the words that every one of them ends with, as STIG Viewer 3 shows it."""
    for tail in (" Security Technical Implementation Guide", " Security Requirements Guide"):
        if title.endswith(tail):
            return title[:-len(tail)]
    return title


def cklb_text(device, bench, entries, marking, title):
    """The text of one checklist in the .cklb format: one device, one benchmark, and an entry for each of its rules."""
    # An identifier is made from the device and the benchmark. So the same input gives the same file, and two
    # checklists never share an identifier.
    seed = "lab-checklist:%s:%s:%s:%s" % (device["host"], bench["id"], bench["version"], bench["release"])
    make = lambda *parts: str(uuid.uuid5(uuid.NAMESPACE_URL, ":".join((seed,) + parts)))
    stig_uuid = make("stig")
    target_key = next((r["fields"]["TargetKey"] for r in bench["rules"] if r["fields"]["TargetKey"]), "")
    rules = []
    for rule, (status, details, comments, _) in zip(bench["rules"], entries):
        fields = rule["fields"]
        rule_id = fields["Rule_ID"]
        item = {"group_id_src": fields["Vuln_Num"],
                "group_tree": [{"id": fields["Vuln_Num"], "title": fields["Group_Title"], "description": rule["group_description"]}],
                "group_id": fields["Vuln_Num"], "severity": fields["Severity"],
                # STIG Viewer 3 writes the title of the rule here. The title of the group, an SRG number, is in group_tree.
                "group_title": fields["Rule_Title"],
                "rule_id_src": rule_id, "rule_id": rule_id[:-len("_rule")] if rule_id.endswith("_rule") else rule_id,
                "rule_version": fields["Rule_Ver"], "rule_title": fields["Rule_Title"], "fix_text": fields["Fix_Text"],
                "weight": fields["Weight"], "check_content": fields["Check_Content"],
                "check_content_ref": {"href": rule["check_href"], "name": fields["Check_Content_Ref"]},
                "classification": "Unclassified", "legacy_ids": list(rule["legacy"]), "ccis": list(rule["cci"]),
                "reference_identifier": fields["TargetKey"], "uuid": make("rule", rule_id), "stig_uuid": stig_uuid,
                "status": CKLB_STATUS[status], "overrides": {}, "comments": plain_text(comments), "finding_details": plain_text(details)}
        for key, name in CKLB_FIELDS:
            item[key] = fields.get(name, "")
        rules.append(dict((key, item[key]) for key in CKLB_RULE))
    stig = {"stig_name": bench["title"], "display_name": short_title(bench["title"]), "stig_id": bench["id"], "release_info": bench["release"],
            "version": bench["version"], "uuid": stig_uuid, "reference_identifier": target_key, "size": len(rules), "rules": rules}
    target = {"target_type": "Computing", "host_name": device["host"], "ip_address": device["ip"], "mac_address": device["mac"],
              "fqdn": device["fqdn"], "comments": plain_text(device["comment"]), "role": "None", "is_web_database": False,
              "technology_area": "", "web_db_site": "", "web_db_instance": "", "classification": marking or None}
    # active, mode, and has_path belong to the window of STIG Viewer 3. Files that other programs write for it have these
    # values. What STIG Viewer 3 does with them was not tested.
    checklist = {"title": title, "id": make("checklist"), "stigs": [stig], "active": False, "mode": 1, "has_path": True,
                 "target_data": target, "cklb_version": "1.0"}
    return json.dumps(checklist, indent=2, ensure_ascii=False) + "\n"


def cklb_problems(text):
    """What in a .cklb checklist differs from a file that STIG Viewer 3 saves. An empty list means nothing.

    DISA publishes no schema for the format. So this compares the keys, their order, and the kinds of values.
    """
    try:
        doc = json.loads(text)
    except ValueError as err:
        return ["it is not JSON: %s" % err]
    if not isinstance(doc, dict) or list(doc) != CKLB_TOP:
        return ["the keys of the checklist are not %s" % ", ".join(CKLB_TOP)]
    problems = []
    if doc["cklb_version"] != "1.0" or not isinstance(doc["title"], str) or not UUID.match(str(doc["id"])) \
            or not isinstance(doc["active"], bool) or not isinstance(doc["has_path"], bool) or type(doc["mode"]) is not int:
        problems.append("a value at the top of the checklist is wrong: the version is 1.0, and the title, the identifier, and the three window values have fixed kinds")
    target = doc["target_data"]
    if not isinstance(target, dict) or list(target) != CKLB_TARGET:
        problems.append("the keys of target_data are not %s" % ", ".join(CKLB_TARGET))
    elif not (isinstance(target["host_name"], str) and target["host_name"]):
        problems.append("target_data has no host name")
    elif target["target_type"] not in ASSET_TYPES or target["role"] not in ROLES or target["technology_area"] not in TECH_AREAS \
            or not isinstance(target["is_web_database"], bool) or not (target["classification"] is None or isinstance(target["classification"], str)):
        problems.append("a value of target_data is wrong: the type, the role, and the technology area have fixed values")
    stigs = doc["stigs"]
    if not isinstance(stigs, list) or not stigs:
        return problems + ["stigs has to be a list with one benchmark at least"]
    for stig in stigs:
        if not isinstance(stig, dict) or list(stig) != CKLB_STIG:
            problems.append("the keys of a benchmark are not %s" % ", ".join(CKLB_STIG))
            continue
        rules = stig["rules"]
        if not isinstance(rules, list) or not rules or stig["size"] != len(rules):
            problems.append("%s: size is not the number of its rules" % stig["stig_id"])
            continue
        if not UUID.match(str(stig["uuid"])) or any(not isinstance(stig[key], str) for key in CKLB_STIG[:7]):
            problems.append("%s: a value of the benchmark is not text, or its identifier is wrong" % stig["stig_id"])
        seen = set()
        for rule in rules:
            number = rule.get("group_id", "?") if isinstance(rule, dict) else "?"
            if not isinstance(rule, dict) or list(rule) != CKLB_RULE:
                problems.append("rule %s: its keys are missing or out of order" % number)
                continue
            if rule["status"] not in CKLB_STATUS.values():
                problems.append("rule %s: the status %r is not one of the format" % (number, rule["status"]))
            tree, ref = rule["group_tree"], rule["check_content_ref"]
            if not (isinstance(tree, list) and tree and all(isinstance(g, dict) and list(g) == ["id", "title", "description"] for g in tree)):
                problems.append("rule %s: group_tree is not a list of groups with id, title, and description" % number)
            if not (isinstance(ref, dict) and list(ref) == ["href", "name"]):
                problems.append("rule %s: check_content_ref does not have href and name" % number)
            if not (isinstance(rule["legacy_ids"], list) and isinstance(rule["ccis"], list) and all(isinstance(x, str) for x in rule["legacy_ids"] + rule["ccis"])):
                problems.append("rule %s: legacy_ids and ccis have to be lists of text" % number)
            if not isinstance(rule["overrides"], dict):
                problems.append("rule %s: overrides is not an object" % number)
            if rule["stig_uuid"] != stig["uuid"] or not UUID.match(str(rule["uuid"])) or rule["uuid"] in seen:
                problems.append("rule %s: its identifier is wrong or used twice, or it names another benchmark" % number)
            seen.add(rule["uuid"])
            wrong = [key for key in CKLB_RULE if key not in ("group_tree", "check_content_ref", "legacy_ids", "ccis", "overrides") and not isinstance(rule[key], str)]
            if wrong:
                problems.append("rule %s: %s is not text" % (number, ", ".join(wrong)))
            if rule["rule_id_src"] not in (rule["rule_id"], rule["rule_id"] + "_rule") or rule["group_id"] != rule["group_id_src"]:
                problems.append("rule %s: rule_id and group_id do not match their sources" % number)
    return problems


# ------------------------------------------------------------------ the devices

def read_lab_values(path):
    """The host names of the two switches and the addresses of the hosts, from the LAB-VALUES.md of the Lab Selector."""
    hosts, addresses = {}, {}
    with io.open(path, "r", encoding="utf-8") as fh:
        for line in fh.read().split("\n"):
            m = re.match(r"^\| (%s) \| `([^`]+)` \|" % "|".join(re.escape(r) for r in SWITCH_ROLES), line)
            if m:
                hosts[m.group(1)] = m.group(2)
            m = re.match(r"^\| `([a-z][a-z0-9-]*)`[^|]*\| [^|]* \| `(\d+\.\d+\.\d+\.\d+)` \|", line)
            if m:
                addresses[m.group(1)] = m.group(2)
    return hosts, addresses


def find_devices(rows, lab_values, assets):
    """The devices of the results file, each with what the checklist says about it."""
    hosts, addresses = read_lab_values(lab_values) if lab_values else ({}, {})
    devices = {}
    for row in rows:
        for key, model in devices_of(row):
            device = devices.setdefault(key, {"key": key, "model": "", "release": "", "host": "", "ip": "", "mac": "", "fqdn": ""})
            device["model"] = device["model"] or model
            device["release"] = device["release"] or (row.get("FortiSwitchOS", "") if model else "")
    for key, device in devices.items():
        device["host"] = hosts.get(key, "" if device["model"] else key)
        device["ip"] = addresses.get(device["host"], "")
    for spec in assets or []:
        key, _, value = spec.partition("=")
        parts = [p.strip() for p in value.split(",")]
        if key.strip() not in devices or not parts[0]:
            raise Problem("--asset %s: use DEVICE=HOST[,IP[,MAC[,FQDN]]], and a device of the results file: %s" % (spec, ", ".join(sorted(devices))))
        for name, part in zip(("host", "ip", "mac", "fqdn"), parts):
            devices[key.strip()][name] = part
    for key, device in devices.items():
        what = [x for x in (key if key != device["host"] else "", device["model"], "FortiSwitchOS %s" % device["release"] if device["release"] else "") if x]
        device["comment"] = "%sLab device of the SRG requirement labs. The statuses come from the lab results." % ("%s. " % ", ".join(what) if what else "")
        device["file"] = re.sub(r"[^A-Za-z0-9._-]+", "-", device["host"] or key).strip("-").lower() or "device"
        # A program that reads a checklist can refuse one with no host name, so a device without one takes the name of its file.
        device["host"] = device["host"] or device["file"]
    return [devices[k] for k in sorted(devices)]


# ------------------------------------------------------------------ the run

def write_checklists(rows, known, benchmarks, devices, out, marking, kinds=FORMATS["cklb"]):
    """Write one checklist for each device and benchmark that share a requirement, in each kind of file that is asked for.

    Returns the lines of the summary about the files, the lines about what no checklist has, and the count of the files.
    """
    by_rule = {}
    for row in rows:
        by_rule.setdefault(row["SRG ID"], []).append(row)
    in_benchmark = set(rule["fields"]["Rule_Ver"] for bench in benchmarks for rule in bench["rules"])
    os.makedirs(out, exist_ok=True)
    files, notes, written = [], [], 0
    for device in devices:
        for bench in benchmarks:
            entries = [rule_entry(rule["fields"]["Rule_Ver"], device, by_rule, known) for rule in bench["rules"]]
            tested = sum(1 for e in entries if e[3])
            if not tested:
                continue
            base = "%s_%s_V%sR%d" % (device["file"], re.sub(r"[^A-Za-z0-9._-]+", "-", bench["id"]), bench["version"], release_number(bench["release"]))
            for kind in kinds:
                if kind == "cklb":
                    text = cklb_text(device, bench, entries, marking, base)
                    problems = cklb_problems(text)
                else:
                    text = checklist_text(device, bench, entries, marking)
                    problems = checklist_problems(text)
                if problems:
                    raise Problem("The .%s checklist of %s for %s does not follow its format: %s" % (kind, device["key"], bench["id"], "; ".join(problems[:3])))
                with io.open(os.path.join(out, "%s.%s" % (base, kind)), "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(text)
                written += 1
            count = dict((s, sum(1 for e in entries if e[0] == s)) for s in (NOT_A_FINDING, OPEN, NA, NOT_REVIEWED))
            files.append("%s%s: %d rules, %d with a lab on this device. %s" % (
                base, " and ".join(".%s" % kind for kind in kinds), len(entries), tested,
                ", ".join("%s %d" % (STATUS_TEXT[s], count[s]) for s in (NOT_A_FINDING, OPEN, NA, NOT_REVIEWED))))
    outside = sorted(set((row["SRG ID"], row["Lab"], row["Result"]) for row in rows if row["SRG ID"] not in in_benchmark))
    if outside:
        notes.append("%d requirement(s) of the results file are in no benchmark that was given, so no checklist has them:" % len(set(o[0] for o in outside)))
        notes += ["  %s (Lab %s, result: %s)" % o for o in outside]
    unknown = sorted(set((row["SRG ID"], row["Lab"]) for row in rows if (row["Lab"], row["SRG ID"]) not in known and row["Result"] == "pass"))
    if unknown:
        notes.append("%d passed requirement(s) are not in the lab chapters that were read, so they stay Not Reviewed:" % len(unknown))
        notes += ["  %s (Lab %s)" % u for u in unknown]
    return files, notes, written


def selftest():
    """Build checklists from a small benchmark, a small chapter, and a small results file, and check them."""
    import tempfile

    def benchmark(release):
        xml = ('<?xml version="1.0" encoding="utf-8"?><Benchmark xmlns="%s" xmlns:dc="http://purl.org/dc/elements/1.1/" id="Test_SRG">'
               '<title>Test Security Requirements Guide</title><description>A benchmark for the self-test.</description>'
               '<notice id="terms-of-use"/><reference href="https://example.invalid"><dc:source>STIG.DOD.MIL</dc:source></reference>'
               '<plain-text id="release-info">Release: %d Benchmark Date: 01 Jan 2026</plain-text><version>1</version>' % (XCCDF, release))
        for i in range(1, 9):
            ver = "SRG-NET-00000%d-TST-00000%d" % (i, i)
            xml += ('<Group id="V-10000%d"><title>%s</title><description>&lt;GroupDescription&gt;&lt;/GroupDescription&gt;</description><Rule id="SV-10000%dr%d_rule" weight="10.0" severity="medium"><version>%s</version>'
                    '<title>Rule %d &amp; its title</title><description>&lt;VulnDiscussion&gt;Why rule %d matters &amp;amp; more.&lt;/VulnDiscussion&gt;'
                    '&lt;Documentable&gt;false&lt;/Documentable&gt;</description><reference><dc:identifier>4321</dc:identifier></reference>'
                    '<ident system="http://cyber.mil/legacy">SV-9000%d</ident><ident system="http://cyber.mil/cci">CCI-00000%d</ident>'
                    '<ident system="http://cyber.mil/cci">CCI-00100%d</ident><fixtext fixref="F-1">Fix %d.</fixtext>'
                    '<check system="C-1"><check-content-ref href="x.xml" name="M"/><check-content>Check %d &lt; 5.</check-content></check></Rule></Group>'
                    % (i, ver[:14], i, release, ver, i, i, i, i, i, i, i))
        return (xml + "</Benchmark>").encode("utf-8")

    table = ["| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |", "| --- | --- | --- | --- | --- |"]
    chapter = "\n".join([
        "### Lab 1.1 — A requirement lab", ""] + table + [
        "| `SRG-NET-000001-TST-000001` | II | Meet it | Equivalent setting | p1 |", "| `SRG-NET-000002-TST-000002` | II | Meet part of it | Partial | p2 |",
        "| `SRG-NET-000005-TST-000005` | II | Fail it | Same requirement | p5 |", "| `SRG-NET-000006-TST-000006` | II | Not run | Same requirement | p6 |", "",
        "### Lab 1.2 — Gaps: two things", ""] + table + [
        "| `SRG-NET-000003-TST-000003` | II | Cannot meet it | Not supported | p3 |", "| `SRG-NET-000004-TST-000004` | II | Nothing to secure | Not applicable | p4 |", "",
        "### Lab 1.3 — A lab with a list of features", "", "| SRG ID | CAT | Requirement | Features in Chapter 01 |", "| --- | --- | --- | --- |",
        "| `SRG-NET-000007-TST-000007` | II | Meet it too | Partial installation of a policy package |"])
    checks, failed = [0], []

    def ok(cond, text):
        checks[0] += 1
        if not cond:
            failed.append(text)

    QUIET[0] = True
    del NOTES[:]
    with tempfile.TemporaryDirectory() as folder:
        # The benchmark as DISA gives it: a file, an SRG zip, an older release, and the library zip that holds a zip.
        disa = os.path.join(folder, "disa")
        os.makedirs(disa)
        with open(os.path.join(disa, "U_Test_SRG_V1R2_Manual-xccdf.xml"), "wb") as fh:
            fh.write(benchmark(2))
        for release in (1, 2):
            with zipfile.ZipFile(os.path.join(disa, "U_Test_V1R%d_SRG.zip" % release), "w") as z:
                z.writestr("U_Test_V1R%d_Manual_SRG/U_Test_SRG_V1R%d_Manual-xccdf.xml" % (release, release), benchmark(release))
        inner = io.BytesIO()
        with zipfile.ZipFile(inner, "w") as z:
            z.writestr("U_Test_V1R2_Manual_SRG/U_Test_SRG_V1R2_Manual-xccdf.xml", benchmark(2))
        with zipfile.ZipFile(os.path.join(disa, "U_SRG-STIG_Library_Test.zip"), "w") as z:
            z.writestr("U_Test_V1R2_SRG.zip", inner.getvalue())
        with open(os.path.join(disa, "U_Other_SRG_V1R1_Manual-xccdf.xml"), "wb") as fh:
            fh.write(b'<?xml version="1.0"?><!DOCTYPE Benchmark [<!ENTITY a "b">]><Benchmark xmlns="%s" id="Other"/>' % XCCDF.encode("ascii"))
        with open(os.path.join(disa, "not-a-zip_SRG.zip"), "wb") as fh:
            fh.write(b"this is no zip file")
        wanted = set("SRG-NET-00000%d-TST-00000%d" % (i, i) for i in range(1, 8))
        found = find_benchmarks([disa], wanted)
        ok(len(found) == 1 and found[0]["release"].startswith("Release: 2") and len(found[0]["rules"]) == 8, "the newest release of a benchmark is found once, in a file, a zip, and a zip inside a zip")
        ok(any("document type" in note for note in NOTES) and any("not a zip" in note for note in NOTES), "a file with a document type declaration and a broken zip are left out, with a note")
        ok(find_benchmarks([os.path.join(disa, "U_Test_V1R1_SRG.zip")], wanted)[0]["release"].startswith("Release: 1") and find_benchmarks([disa], {"SRG-NET-000001-XXX-000001"}) == [], "a zip that is named is used, and a benchmark with no requirement of the results file is not")
        bench = found[0]

        path = os.path.join(folder, "04-test.md")
        with io.open(path, "w", encoding="utf-8") as fh:
            fh.write(chapter)
        known = read_requirements([("", path)])
        ok(known[("1.3", "SRG-NET-000007-TST-000007")]["kind"] == MEETS and known[("1.1", "SRG-NET-000002-TST-000002")]["kind"] == PARTIAL
           and known[("1.2", "SRG-NET-000003-TST-000003")]["kind"] == GAP and known[("1.2", "SRG-NET-000004-TST-000004")]["kind"] == NOT_APPLICABLE,
           "the words Partial, Not supported, and Not applicable count in an alignment column only")
        head = "SRG ID,CAT,Requirement,Lab,Lab title,Tested on,Switch model,FortiSwitchOS,Planned,Result,Result comes from,Date,Evidence,Note"
        body = ["SRG-NET-000001-TST-000001,II,Meet it,1.1,A requirement lab,Both switches,FS-A and FS-B,7.6.7,yes,pass,requirement row,2026-01-02,evidence/1.1,\"a <note> & more\"",
                "SRG-NET-000002-TST-000002,II,Meet part of it,1.1,A requirement lab,Access switch,FS-A,7.6.7,yes,pass,lab steps,2026-01-02,,",
                "SRG-NET-000003-TST-000003,II,Cannot meet it,1.2,Gaps: two things,Access switch,FS-A,7.6.7,yes,pass,lab steps,2026-01-03,,",
                "SRG-NET-000004-TST-000004,II,Nothing to secure,1.2,Gaps: two things,Access switch,FS-A,7.6.7,yes,pass,lab steps,2026-01-03,,",
                "SRG-NET-000005-TST-000005,II,Fail it,1.1,A requirement lab,Access switch,FS-A,7.6.7,yes,fail,requirement row,2026-01-02,,'-a note that starts like a formula",
                "SRG-NET-000006-TST-000006,II,Not run,1.1,A requirement lab,Aggregation switch,FS-B,7.6.7,no,not tested,,,,",
                "SRG-NET-000007-TST-000007,II,Meet it too,1.3,A lab with a list of features,Access switch,FS-A,7.6.7,yes,pass,lab steps,2026-01-04,,",
                "SRG-NET-000007-TST-000007,II,Meet it too,9.9,A lab that the chapters do not have,Aggregation switch,FS-B,7.6.7,yes,pass,lab steps,2026-01-04,,",
                "SRG-NET-000099-TST-000099,II,In no benchmark,1.1,A requirement lab,Access switch,FS-A,7.6.7,yes,pass,lab steps,2026-01-02,,"]
        results = os.path.join(folder, "results.csv")
        with io.open(results, "w", encoding="utf-8-sig", newline="") as fh:
            fh.write("\r\n".join([head] + body) + "\r\n")
        rows = read_results(results)
        values = os.path.join(folder, "LAB-VALUES.md")
        with io.open(values, "w", encoding="utf-8") as fh:
            fh.write("| Role | Host name | Model |\n| --- | --- | --- |\n| Access switch | `sw-a-1` | FS-A |\n| Aggregation switch | `sw-b-1` | FS-B (the labs were written for the FS-2048F) |\n")
        devices = find_devices(rows, values, ["Access switch=sw-a-1,192.0.2.11"])
        out = os.path.join(folder, "out")
        files, notes, written = write_checklists(rows, known, [bench], devices, out, "", FORMATS["both"])
        names = sorted(os.listdir(out))
        ok(written == 4 and names == ["sw-a-1_Test_SRG_V1R2.ckl", "sw-a-1_Test_SRG_V1R2.cklb", "sw-b-1_Test_SRG_V1R2.ckl", "sw-b-1_Test_SRG_V1R2.cklb"],
           "one checklist of each kind for each switch, named after its host: %s" % names)
        lines = files + notes
        write_checklists(rows, known, [bench], devices, os.path.join(folder, "default"), "")
        ok(sorted(os.listdir(os.path.join(folder, "default"))) == ["sw-a-1_Test_SRG_V1R2.cklb", "sw-b-1_Test_SRG_V1R2.cklb"], "the format is .cklb unless another one is asked for")
        ok(all(d["host"] for d in find_devices(rows, None, None)) and [d["host"] for d in find_devices(rows, None, None)] == ["access-switch", "aggregation-switch"],
           "a device without a host name takes the name of its file")

        def read(name):
            with io.open(os.path.join(out, name), encoding="utf-8") as fh:
                text = fh.read()
            root = ET.fromstring(text.encode("utf-8"))
            vulns = dict((next(d.findtext("ATTRIBUTE_DATA") for d in v.findall("STIG_DATA") if d.findtext("VULN_ATTRIBUTE") == "Rule_Ver"), v) for v in root.iter("VULN"))
            return text, root, vulns

        text, root, vulns = read("sw-a-1_Test_SRG_V1R2.ckl")
        status = dict((k, v.findtext("STATUS")) for k, v in vulns.items())
        ok(checklist_problems(text) == [], "the checklist follows the schema: %s" % checklist_problems(text)[:2])
        ok(len(status) == 8, "the checklist has every rule of the benchmark")
        ok(status.get("SRG-NET-000001-TST-000001") == NOT_A_FINDING and status.get("SRG-NET-000007-TST-000007") == NOT_A_FINDING, "a pass of a requirement that the product meets is Not a Finding")
        ok(status.get("SRG-NET-000002-TST-000002") == OPEN, "a pass of a requirement that is met in part is Open")
        ok(status.get("SRG-NET-000003-TST-000003") == OPEN, "a pass of a gap lab is Open")
        ok(status.get("SRG-NET-000004-TST-000004") == NA, "a pass of a gap lab for a requirement that is not applicable is Not Applicable")
        ok(status.get("SRG-NET-000005-TST-000005") == OPEN, "a failed lab is Open")
        ok(status.get("SRG-NET-000006-TST-000006") == NOT_REVIEWED and status.get("SRG-NET-000008-TST-000008") == NOT_REVIEWED, "a rule that was not tested on the device stays Not Reviewed")
        first, fail, other = vulns["SRG-NET-000001-TST-000001"], vulns["SRG-NET-000005-TST-000005"], vulns["SRG-NET-000006-TST-000006"]
        ok("a <note> & more" in first.findtext("FINDING_DETAILS") and "evidence/1.1" in first.findtext("FINDING_DETAILS"), "the finding details hold the note and the evidence")
        ok("Note: -a note that starts like a formula" in fail.findtext("FINDING_DETAILS"), "the apostrophe before a cell that starts like a formula is taken off")
        ok("another device (Aggregation switch)" in other.findtext("COMMENTS") and "No lab in the results file" in vulns["SRG-NET-000008-TST-000008"].findtext("COMMENTS"), "a rule that is tested on the other switch, or by no lab, says so")
        ok(root.findtext("ASSET/HOST_NAME") == "sw-a-1" and root.findtext("ASSET/HOST_IP") == "192.0.2.11" and root.findtext("ASSET/TARGET_KEY") == "4321" and root.find("ASSET/MARKING") is None, "the asset has its name, its address, and the target key, and no marking unless one is given")
        data = dict((d.findtext("VULN_ATTRIBUTE"), d.findtext("ATTRIBUTE_DATA")) for d in first.findall("STIG_DATA"))
        ok(data["Vuln_Num"] == "V-100001" and data["Rule_ID"] == "SV-100001r2_rule" and data["Rule_Title"] == "Rule 1 & its title" and data["Vuln_Discuss"] == "Why rule 1 matters & more."
           and data["Check_Content"] == "Check 1 < 5." and data["Fix_Text"] == "Fix 1." and data["Documentable"] == "false" and data["STIGRef"] == "Test Security Requirements Guide :: Version 1, Release: 2 Benchmark Date: 01 Jan 2026", "the fields of a rule come from the benchmark")
        ok([d.findtext("ATTRIBUTE_DATA") for d in first.findall("STIG_DATA") if d.findtext("VULN_ATTRIBUTE") == "CCI_REF"] == ["CCI-000001", "CCI-001001"]
           and [d.findtext("ATTRIBUTE_DATA") or "" for d in first.findall("STIG_DATA") if d.findtext("VULN_ATTRIBUTE") == "LEGACY_ID"] == ["SV-90001", ""], "a rule keeps its CCI numbers and its legacy numbers")
        text2, root2, vulns2 = read("sw-b-1_Test_SRG_V1R2.ckl")
        ok(vulns2["SRG-NET-000001-TST-000001"].findtext("STATUS") == NOT_A_FINDING and vulns2["SRG-NET-000002-TST-000002"].findtext("STATUS") == NOT_REVIEWED and root2.findtext("ASSET/HOST_NAME") == "sw-b-1", "a lab on both switches counts for each of them, and a lab on one switch for that one")
        ok(vulns2["SRG-NET-000007-TST-000007"].findtext("STATUS") == NOT_REVIEWED and any("not in the lab chapters" in line for line in lines), "a pass in a lab that the chapters do not have stays Not Reviewed, and the summary says so")
        ok(any("SRG-NET-000099-TST-000099" in line for line in lines), "a requirement that is in no benchmark is named in the summary")
        ok(checklist_problems(text.replace("<STATUS>Open</STATUS>", "<STATUS>Closed</STATUS>", 1)) != [] and checklist_problems(text.replace("\t\t<ROLE>None</ROLE>\n", "", 1)) != []
           and checklist_problems(text.replace("<COMMENTS>", "<COMMENT>", 1).replace("</COMMENTS>", "</COMMENT>", 1)) != [], "the check of the schema finds a wrong status, a missing element, and a wrong name")
        marked = checklist_text(devices[0], bench, [(NOT_REVIEWED, "", "", False)] * 8, "CUI")
        ok(checklist_problems(marked) == [] and "<MARKING>CUI</MARKING>" in marked, "a marking that is given is written")
        # The .cklb file of the same device: the same statuses and texts, in the keys and the words of STIG Viewer 3.
        with io.open(os.path.join(out, "sw-a-1_Test_SRG_V1R2.cklb"), encoding="utf-8") as fh:
            jtext = fh.read()
        doc = json.loads(jtext)
        stig = doc["stigs"][0]
        jrules = dict((r["rule_version"], r) for r in stig["rules"])
        ok(cklb_problems(jtext) == [], "the .cklb checklist has the keys and the kinds of values of the format: %s" % cklb_problems(jtext)[:2])
        ok(list(doc) == CKLB_TOP and doc["cklb_version"] == "1.0" and len(doc["stigs"]) == 1 and list(stig) == CKLB_STIG and stig["size"] == 8
           and len(stig["rules"]) == 8 and all(list(r) == CKLB_RULE for r in stig["rules"]), "a .cklb file has the keys of a file that STIG Viewer 3 saves, in its order")
        ok(all(jrules[k]["status"] == CKLB_STATUS[status[k]] for k in status) and sorted(set(r["status"] for r in stig["rules"])) == ["not_a_finding", "not_applicable", "not_reviewed", "open"],
           "a .cklb file has the statuses of the .ckl file, in the words of its format")
        ok(all(jrules[k]["finding_details"] == (v.findtext("FINDING_DETAILS") or "") and jrules[k]["comments"] == (v.findtext("COMMENTS") or "") for k, v in vulns.items()),
           "the finding details and the comments are the same in both kinds of file")
        one = jrules["SRG-NET-000001-TST-000001"]
        ok(one["group_id"] == "V-100001" and one["group_id_src"] == "V-100001" and one["rule_id_src"] == "SV-100001r2_rule" and one["rule_id"] == "SV-100001r2"
           and one["group_title"] == "Rule 1 & its title" and one["rule_title"] == "Rule 1 & its title"
           and one["group_tree"] == [{"id": "V-100001", "title": "SRG-NET-000001", "description": "<GroupDescription></GroupDescription>"}]
           and one["check_content_ref"] == {"href": "x.xml", "name": "M"} and one["ccis"] == ["CCI-000001", "CCI-001001"] and one["legacy_ids"] == ["SV-90001"]
           and one["discussion"] == "Why rule 1 matters & more." and one["check_content"] == "Check 1 < 5." and one["fix_text"] == "Fix 1." and one["weight"] == "10.0"
           and one["documentable"] == "false" and one["classification"] == "Unclassified" and one["overrides"] == {} and one["reference_identifier"] == "4321"
           and one["stig_uuid"] == stig["uuid"], "the fields of a rule in a .cklb file come from the benchmark")
        target = doc["target_data"]
        ok(list(target) == CKLB_TARGET and target["host_name"] == "sw-a-1" and target["ip_address"] == "192.0.2.11" and target["target_type"] == "Computing"
           and target["classification"] is None and stig["reference_identifier"] == "4321" and stig["stig_name"] == "Test Security Requirements Guide"
           and stig["display_name"] == "Test" and stig["stig_id"] == "Test_SRG" and stig["version"] == "1" and stig["release_info"].startswith("Release: 2")
           and doc["title"] == "sw-a-1_Test_SRG_V1R2", "the target data and the benchmark of a .cklb file are those of the device and of the benchmark")
        with io.open(os.path.join(out, "sw-b-1_Test_SRG_V1R2.cklb"), encoding="utf-8") as fh:
            other_doc = json.loads(fh.read())
        mine, theirs = set(r["uuid"] for r in stig["rules"]), set(r["uuid"] for r in other_doc["stigs"][0]["rules"])
        ok(len(mine) == 8 and not mine & theirs and other_doc["id"] != doc["id"] and other_doc["stigs"][0]["uuid"] != stig["uuid"], "no two checklists share an identifier")
        ok(cklb_problems(jtext.replace('"status": "open"', '"status": "closed"', 1)) != [] and cklb_problems(jtext.replace('"host_name": "sw-a-1"', '"host_name": ""', 1)) != []
           and cklb_problems(json.dumps(dict(doc, extra=1))) != [] and cklb_problems(jtext.replace('"size": 8', '"size": 7', 1)) != [] and cklb_problems("{") != [],
           "the check of a .cklb file finds a wrong status, a missing host name, a key that is not of the format, and a wrong count")
        ok(json.loads(cklb_text(devices[0], bench, [(NOT_REVIEWED, "", "", False)] * 8, "CUI", "t"))["target_data"]["classification"] == "CUI", "a marking that is given is written to a .cklb file too")
        write_checklists(rows, known, [bench], devices, os.path.join(folder, "again"), "", FORMATS["both"])
        with io.open(os.path.join(folder, "again", "sw-a-1_Test_SRG_V1R2.ckl"), encoding="utf-8") as fh:
            same = fh.read() == text
        with io.open(os.path.join(folder, "again", "sw-a-1_Test_SRG_V1R2.cklb"), encoding="utf-8") as fh:
            ok(same and fh.read() == jtext, "the same input gives the same files")
        try:
            read_results(values)
            ok(False, "a file that is no results file is refused")
        except Problem:
            ok(True, "")
    QUIET[0] = False
    if failed:
        for text in failed:
            print("make-ckl.py selftest: FAILED: %s" % text, file=sys.stderr)
        return 1
    say("make-ckl.py selftest: OK (%d checks)" % checks[0])
    return 0


def main(argv):
    parser = argparse.ArgumentParser(description="Write STIG Viewer checklists (.cklb, or .ckl) from the results file of the Lab Selector and the benchmark files of DISA.")
    parser.add_argument("--results", help="the results file that the Lab Selector saves (lab201-results.csv)")
    parser.add_argument("--disa", nargs="+", help="where the benchmark files of DISA are: a folder, an SRG zip, the library zip, or an xccdf file")
    parser.add_argument("--walkthroughs", help="the folder with the lab chapters under their short names (default: beside this script, or the volumes of the repository)")
    parser.add_argument("--catalog", default=os.path.join(HERE, "lab-catalog.json"), help="the lab catalog (default: lab-catalog.json beside this script)")
    parser.add_argument("--lab-values", help="the LAB-VALUES.md of the Lab Selector zip, for the host names and the addresses")
    parser.add_argument("--asset", action="append", metavar="DEVICE=HOST[,IP[,MAC[,FQDN]]]", help="the host name and addresses of a device, for example \"Access switch=sw-648f-1,10.200.0.11\"")
    parser.add_argument("--format", choices=sorted(FORMATS), default="cklb", help="cklb for STIG Viewer 3 (default), ckl for STIG Viewer 2, or both")
    parser.add_argument("--marking", default="", help="the marking of the checklists, for example CUI (default: none)")
    parser.add_argument("--out", default="checklists", help="the folder for the checklists (default: checklists)")
    parser.add_argument("--selftest", action="store_true", help="check the script with a small benchmark that it carries, and stop")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.results or not args.disa:
        parser.error("--results and --disa are needed")
    try:
        rows = read_results(args.results)
        chapters, missing = chapter_files(args.catalog, args.walkthroughs)
        if not chapters:
            raise Problem("No lab chapter was found (%s). The chapters say what a passed lab means for a requirement. Name their folder with --walkthroughs" % ", ".join(missing))
        known = read_requirements(chapters)
        benchmarks = find_benchmarks(args.disa, set(row["SRG ID"] for row in rows))
        if not benchmarks:
            raise Problem("No benchmark under %s has a rule for a requirement of the results file. Give the SRG zips of DISA, or the folder that holds them" % ", ".join(args.disa))
        devices = find_devices(rows, args.lab_values, args.asset)
        files, notes, written = write_checklists(rows, known, benchmarks, devices, args.out, args.marking, FORMATS[args.format])
    except Problem as err:
        print("make-ckl.py: %s" % err, file=sys.stderr)
        return 1
    except (OSError, ValueError) as err:
        print("make-ckl.py: %s" % err, file=sys.stderr)
        return 1
    say("Benchmarks used:")
    for bench in benchmarks:
        say("  %s, Version %s, %s (%d rules)" % (bench["title"], bench["version"], bench["release"], len(bench["rules"])))
    say("")
    say("%d checklist(s) written to %s:" % (written, os.path.abspath(args.out)))
    for line in files:
        say("  " + line)
    # A long list of requirements is cut short on the screen. The summary file has all of it.
    listed, left = 0, 0
    for line in notes:
        if line.startswith("  SRG-"):
            listed += 1
            if listed > 12:
                left += 1
                continue
        else:
            if left:
                say("  ... and %d more, in checklists-summary.txt" % left)
            listed, left = 0, 0
            say("")
        say(line)
    if left:
        say("  ... and %d more, in checklists-summary.txt" % left)
    if missing and any("not in the lab chapters" in line for line in notes):
        say("These lab chapters were not found: %s. Name their folder with --walkthroughs." % ", ".join(missing))
    with io.open(os.path.join(args.out, "checklists-summary.txt"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("Checklists made by make-ckl.py from %s\n\nBenchmarks used:\n" % os.path.basename(args.results))
        fh.write("".join("  %s, Version %s, %s (%d rules)\n" % (b["title"], b["version"], b["release"], len(b["rules"])) for b in benchmarks))
        fh.write("\nChecklists:\n" + "".join("  %s\n" % line for line in files))
        fh.write("".join(("%s\n" if line.startswith("  ") else "\n%s\n") % line for line in notes))
        fh.write("\nA status is a proposal from the lab result and the lab chapters. Read the finding details and the lab before you sign a checklist.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
