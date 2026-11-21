#!/usr/bin/env python3
"""Plan, scaffold, link, and check the SRG requirement labs of a Fortinet STIG
volume (volumes/volume-2NN-<product>-stig-and-srg-mapping). Run from the
repository root.

Usage:
  python .claude/skills/srg-labs-for/labs.py <product>                    plan: print the requirements and the labs, change nothing
  python .claude/skills/srg-labs-for/labs.py <product> --plan-file F      also write the plan to the file F (tab-separated)
  python .claude/skills/srg-labs-for/labs.py <product> --scaffold F       write the lab chapters from the filled plan file F
  python .claude/skills/srg-labs-for/labs.py <product> --lab-column       add or refresh the Lab column in the map and crosswalk tables
  python .claude/skills/srg-labs-for/labs.py <product> --check            check finished labs

Options for the plan and --check:
  --allow ID,ID   SRG IDs that the tables cite and that need no lab of their own,
                  for example a retired ID whose rule the map points at a current ID
  --scope map     count only the requirements of the map chapter's requirement
                  reference (the product's own requirements). The default, all,
                  also counts every SRG ID that a crosswalk table cites, as
                  Volume CCI does.

<product> is the name in the volume's folder, for example "FortiAnalyzer".

The labs follow Volume CCI (FortiSwitch): one lab chapter for each SRG, labs
that each prove a group of requirements with a positive and a negative test,
gap labs for requirements the product cannot meet, a shared lab chapter 999,
and a final Lab column in every SRG table of the map and crosswalk chapters.

The script does not commit, and it never writes a command or a test: it puts
a comment that starts "TODO srg-labs-for" wherever a person or Claude has to
write. --check fails while such a comment remains.
"""
import argparse
import io
import os
import re
import subprocess
import sys

MARK = "TODO srg-labs-for"
EXPORT = "scripts/python/export_srg_tables.py"
SHARED = "999-shared-lab-infrastructure.md"
AS_BUILT = "90-as-built-how-this-volume-was-built.md"
SRG_ID = re.compile(r"SRG-[A-Z]+-\d{6}-[A-Z0-9]+-\d{6}")
LAB_HEADING = re.compile(r"^### Lab (\d+)\.(\d+) — (.+?)\s*$")
SRG_ROW = re.compile(r"^\| `(SRG-[A-Z]+-\d{6}-[A-Z0-9]+-\d{6})` \| (I{1,3}) \| (.*?) \|")
PARTS = ["**Goal.**", "**Uses.**", "**Configure.**", "**Positive test.**", "**Negative test.**", "**Evidence.**",
         "**Return to baseline.**"]
COLUMNS = ["srg_id", "srg", "source", "cat", "requirement", "alignment", "features", "with_command", "kind", "lab",
           "lab_title"]
WORDS = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen " \
        "seventeen eighteen nineteen twenty".split()
# SRG names for the abbreviations the map chapters use. A map chapter that gives the abbreviation with the name
# ("**Central Log Server (CLS)**") adds to these.
SRG_NAMES = {"NDM": "Network Device Management", "CLS": "Central Log Server", "L2S": "Layer 2 Switch",
             "RTR": "Router", "AAA": "AAA Services"}
# Crosswalk alignments that mean the product has no setting for the requirement.
NO_SETTING = ("Not supported", "Not applicable")


def die(message):
    sys.exit("labs.py: " + message)


def read(path):
    return io.open(path, encoding="utf-8", newline="").read()


def write(path, text):
    io.open(path, "w", encoding="utf-8", newline="").write(text)


def cells(line):
    """The cells of a Markdown table row."""
    body = line.strip()
    body = body[1:] if body.startswith("|") else body
    body = body[:-1] if body.endswith("|") else body
    return [c.strip() for c in re.split(r"(?<!\\)\|", body)]


def slug(heading):
    """The anchor GitHub gives a heading: 'Lab 4.7 — Fail secure' -> 'lab-47--fail-secure'."""
    kept = "".join(c for c in heading.lower() if c.isalnum() or c in " -_")
    return kept.replace(" ", "-")


def table_kind(heading, is_map):
    """Which SRG table a heading opens, or None. These are the tables export_srg_tables.py exports, less prerequisites."""
    if is_map:
        if heading.startswith("### The ") and heading.endswith(" feature map"):
            return "feature map"
        if heading == "### Requirement reference":
            return "requirement reference"
    else:
        if heading == "### The crosswalk table":
            return "crosswalk"
        if re.match(r"### .+ requirements with no ", heading):
            return "unmatched"
    return None


def tables(text, is_map):
    """[(kind, first line index, last line index)] for the SRG tables of a chapter (header line to last row)."""
    lines, found, heading = text.split("\n"), [], ""
    i = 0
    while i < len(lines):
        if lines[i].startswith("#"):
            heading = lines[i].strip()
        kind = table_kind(heading, is_map)
        if kind and lines[i].startswith("|") and i + 1 < len(lines) and re.match(r"\|\s*:?-{3,}", lines[i + 1]):
            end = i + 1
            while end + 1 < len(lines) and lines[end + 1].startswith("|"):
                end += 1
            found.append((kind, i, end))
            heading = ""
            i = end
        i += 1
    return found


class Volume:
    def __init__(self, product):
        self.product = product.strip()
        pslug = re.sub(r"[^a-z0-9]+", "-", self.product.lower()).strip("-")
        hits = [d for d in sorted(os.listdir("volumes")) if re.match(r"volume-2\d\d-%s-stig-and-srg-mapping$" % re.escape(pslug), d)]
        if not hits:
            die("no volumes/volume-2NN-%s-stig-and-srg-mapping folder; move the product there first (/stig-volume-for)" % pslug)
        self.slug, self.pslug = hits[0], pslug
        self.folder = "volumes/" + self.slug
        self.number = int(self.slug[7:10])
        names = sorted(n for n in os.listdir(self.folder + "/chapters") if n.endswith(".md"))
        self.maps = [n for n in names if re.match(r"\d+-.*-feature-version-and-s[a-z]+-map\.md$", n)]
        self.crosswalks = [n for n in names if n.endswith("-crosswalk.md")]
        self.lab_chapters = [n for n in names if n.endswith("-requirement-labs.md")]
        self.names = names
        if not self.maps:
            die("%s has no map chapter (NN-...-feature-version-and-...-map.md)" % self.folder)
        self.load_tables()
        self.load_labs()

    def path(self, name):
        return "%s/chapters/%s" % (self.folder, name)

    def load_tables(self):
        """Read the SRG tables: which IDs they cite, and what the map says about each."""
        self.cited, self.info, self.srg_names = [], {}, dict(SRG_NAMES)
        for name in self.maps + self.crosswalks:
            text = read(self.path(name))
            lines = text.split("\n")
            for hit in re.finditer(r"(?m)^\| \*\*(.+?) \(([A-Za-z0-9]+)\)\*\* \| (V\d+R\d+) \|", text):
                self.srg_names[hit.group(2)] = hit.group(1)
            for kind, start, end in tables(text, name in self.maps):
                header = cells(lines[start])
                lab_col = header.index("Lab") if "Lab" in header else None

                def col(*words):
                    return next((i for i, h in enumerate(header) if all(w.lower() in h.lower() for w in words)), None)

                for line in lines[start + 2:end + 1]:
                    row = cells(line)
                    ids = []
                    for i, cell in enumerate(row):
                        if i != lab_col:
                            ids += [x for x in SRG_ID.findall(cell) if x not in ids]
                    for srg_id in ids:
                        if srg_id not in self.cited:
                            self.cited.append(srg_id)
                        self.info.setdefault(srg_id, {"srg": "", "cat": "", "title": "", "summary": "", "alignment": [],
                                                      "features": [], "with_command": 0, "source": "crosswalk",
                                                      "no_setting": False})
                    if kind == "requirement reference" and ids:
                        entry = self.info[ids[0]]
                        entry["srg"] = row[0]
                        entry["source"] = "map"
                        severity = col("severity")
                        title = col("requirement", "title")
                        if severity is not None:
                            entry["cat"] = row[severity].replace("CAT", "").strip()
                        if title is not None:
                            entry["title"] = row[title]
                    elif kind == "feature map":
                        feature, command, srg = col("feature"), col("command"), col("srg")
                        for srg_id in (SRG_ID.findall(row[srg]) if srg is not None else ids):
                            entry = self.info[srg_id]
                            if feature is not None and row[feature] not in entry["features"]:
                                entry["features"].append(row[feature])
                                if command is not None and row[command] not in ("", "—", "-"):
                                    entry["with_command"] += 1
                    elif kind == "crosswalk":
                        alignment, summary, severity = col("alignment"), col("requirement", "summary"), col("severity")
                        command = col(self.product, "command")
                        own = SRG_ID.findall(row[0])
                        if own and command is not None and row[command] in ("", "—", "-"):
                            self.info[own[0]]["no_setting"] = True
                        for srg_id in ids:
                            entry = self.info[srg_id]
                            if alignment is not None and row[alignment] and row[alignment] not in entry["alignment"]:
                                entry["alignment"].append(row[alignment])
                        if own and summary is not None:
                            self.info[own[0]]["summary"] = row[summary]
                            if severity is not None and not self.info[own[0]]["cat"]:
                                self.info[own[0]]["cat"] = row[severity].replace("CAT", "").strip()
        codes = {}
        for srg_id in self.cited:
            if self.info[srg_id]["srg"]:
                codes.setdefault(srg_id.split("-")[3], self.info[srg_id]["srg"])
        for srg_id in self.cited:
            entry = self.info[srg_id]
            entry["srg"] = entry["srg"] or codes.get(srg_id.split("-")[3], srg_id.split("-")[3])

    def load_labs(self):
        """Read the lab chapters: each lab with its number, title, requirement rows, and the parts it has."""
        self.labs = []
        for name in self.lab_chapters:
            lines = read(self.path(name)).split("\n")
            current = None
            for i, line in enumerate(lines):
                hit = LAB_HEADING.match(line)
                if hit:
                    current = {"chapter": name, "id": "%s.%s" % (hit.group(1), hit.group(2)), "title": hit.group(3),
                               "anchor": slug(line[4:].strip()), "rows": [], "parts": [], "line": i + 1}
                    self.labs.append(current)
                elif line.startswith("## "):
                    current = None
                elif current is not None:
                    row = SRG_ROW.match(line)
                    if row:
                        current["rows"].append((row.group(1), row.group(2), row.group(3)))
                    for part in PARTS:
                        if line.startswith(part):
                            current["parts"].append(part)
        self.lab_of = {}
        for lab in self.labs:
            for srg_id, _, _ in lab["rows"]:
                self.lab_of.setdefault(srg_id, []).append(lab)

    def srg_name(self, abbreviation):
        return self.srg_names.get(abbreviation, abbreviation)

    def lab_cell(self, ids):
        """The Lab column cell for a row that cites these IDs: each lab once, in the order of the IDs."""
        seen, links = [], []
        for srg_id in ids:
            for lab in self.lab_of.get(srg_id, []):
                if lab["id"] not in seen:
                    seen.append(lab["id"])
                    links.append("[Lab %s](%s#%s)" % (lab["id"], lab["chapter"], lab["anchor"]))
        return ", ".join(links) if links else "—"

    def with_lab_column(self, name):
        """The text of a map or crosswalk chapter with the Lab column added or refreshed."""
        text = read(self.path(name))
        lines = text.split("\n")
        for kind, start, end in tables(text, name in self.maps):
            header = cells(lines[start])
            has = header[-1] == "Lab"
            if not has:
                lines[start] = lines[start].rstrip() + " Lab |"
                lines[start + 1] = lines[start + 1].rstrip() + " --- |"
            for i in range(start + 2, end + 1):
                row = cells(lines[i])
                body = row[:-1] if has else row
                ids = []
                for cell in body:
                    ids += [x for x in SRG_ID.findall(cell) if x not in ids]
                cell = self.lab_cell(ids)
                if has:
                    cut = lines[i].rstrip()[:-1].rstrip()
                    cut = cut[:len(cut) - len(row[-1])].rstrip() if row[-1] else cut
                    lines[i] = cut + " " + cell + " |" if cut.endswith("|") else lines[i]
                else:
                    lines[i] = lines[i].rstrip() + " " + cell + " |"
        return "\n".join(lines)


def plan_rows(volume, scope):
    rows = []
    for srg_id in volume.cited:
        entry = volume.info[srg_id]
        if scope == "map" and entry["source"] != "map":
            continue
        labs = volume.lab_of.get(srg_id, [])
        rows.append({
            "srg_id": srg_id, "srg": entry["srg"], "source": entry["source"], "cat": entry["cat"],
            "requirement": entry["summary"] or entry["title"], "alignment": "; ".join(entry["alignment"]),
            "features": str(len(entry["features"])), "with_command": str(entry["with_command"]),
            "kind": "gap" if (entry["features"] and not entry["with_command"]) or entry["no_setting"] or (
                entry["alignment"] and all(a in NO_SETTING for a in entry["alignment"])) else "requirement",
            "lab": labs[0]["id"] if labs else "", "lab_title": labs[0]["title"] if labs else ""})
    return rows


def show_plan(volume, allow, plan_file, scope):
    rows = plan_rows(volume, scope)
    print("Volume %s: %s" % (volume.number, volume.slug))
    print("  map chapters: %s" % ", ".join(volume.maps))
    print("  crosswalk chapters: %s" % (", ".join(volume.crosswalks) or "none"))
    print("  lab chapters: %s" % (", ".join(volume.lab_chapters) or "none yet"))
    print("  shared lab chapter (999): %s" % ("present" if SHARED in volume.names else "not written yet"))
    print("Requirements %s: %d" % ("of the map's requirement reference" if scope == "map" else "the tables cite", len(rows)))
    by_srg = {}
    for row in rows:
        by_srg.setdefault(row["srg"], []).append(row)
    used = [int(n.split("-", 1)[0]) for n in volume.names if int(n.split("-", 1)[0]) < 90]
    next_chapter = max(used) + 1
    for srg, group in by_srg.items():
        with_lab = [r for r in group if r["lab"]]
        gaps = [r for r in group if r["kind"] == "gap"]
        only = [r for r in group if r["source"] != "map"]
        print("  %-5s %-28s %3d requirements (%d cited only by a crosswalk), %3d with a lab, %3d gap lab candidates" % (
            srg, volume.srg_name(srg), len(group), len(only), len(with_lab), len(gaps)))
    without = [r for r in rows if not r["lab"] and r["srg_id"] not in allow]
    print("Requirements with no lab: %d%s" % (len(without), " (%d allowed with --allow)" % len(
        [r for r in rows if not r["lab"] and r["srg_id"] in allow]) if allow else ""))
    if not volume.lab_chapters:
        print("Chapter numbers free for lab chapters: %02d and up (one chapter for each SRG), and 999 for the shared lab" % next_chapter)
    print("Labs written: %d" % len(volume.labs))
    if plan_file:
        out = ["\t".join(COLUMNS)] + ["\t".join(row[c].replace("\t", " ") for c in COLUMNS) for row in rows]
        write(plan_file, "\n".join(out) + "\n")
        print("Plan written to %s: fill the lab and lab_title columns (and correct kind), then run --scaffold." % plan_file)
    else:
        print("Nothing was changed. Use --plan-file to write the plan for editing.")


def load_plan(path):
    lines = [l for l in read(path).replace("\r\n", "\n").split("\n") if l.strip()]
    if lines[0].split("\t") != COLUMNS:
        die("%s does not start with the plan's column names" % path)
    rows = []
    for line in lines[1:]:
        values = line.split("\t") + [""] * len(COLUMNS)
        rows.append(dict(zip(COLUMNS, [v.strip() for v in values])))
    return rows


def todo(words):
    return "<!-- %s: %s -->" % (MARK, words)


def scaffold(volume, plan_path):
    rows = load_plan(plan_path)
    labs, order = {}, []
    for row in rows:
        if not re.match(r"\d+\.\d+$", row["lab"]):
            die("%s has no lab number in the plan (expected N.M)" % row["srg_id"])
        if row["kind"] not in ("requirement", "gap"):
            die("%s: kind must be requirement or gap" % row["srg_id"])
        lab = labs.setdefault(row["lab"], {"id": row["lab"], "title": "", "rows": [], "kinds": set(), "srgs": []})
        if row["lab"] not in order:
            order.append(row["lab"])
        if row["lab_title"]:
            if lab["title"] and lab["title"] != row["lab_title"]:
                die("Lab %s has two titles in the plan" % row["lab"])
            lab["title"] = row["lab_title"]
        lab["rows"].append(row)
        lab["kinds"].add(row["kind"])
        lab["srgs"].append(row["srg"])
    chapters = {}
    for lab_id in sorted(order, key=lambda x: [int(p) for p in x.split(".")]):
        lab = labs[lab_id]
        if not lab["title"]:
            die("Lab %s has no title in the plan" % lab_id)
        if len(lab["kinds"]) != 1:
            die("Lab %s mixes requirement and gap rows; a lab is one or the other" % lab_id)
        chapters.setdefault(int(lab_id.split(".")[0]), []).append(lab)
    taken = set(int(n.split("-", 1)[0]) for n in volume.names)
    files = {}
    for number, chapter_labs in sorted(chapters.items()):
        if number in taken or number >= 90:
            die("chapter %d is taken or reserved; lab chapters take free numbers below 90" % number)
        if [int(l["id"].split(".")[1]) for l in chapter_labs] != list(range(1, len(chapter_labs) + 1)):
            die("the labs of chapter %d are not numbered %d.1, %d.2, ... without a gap" % (number, number, number))
        srgs = sorted(set(s for lab in chapter_labs for s in lab["srgs"]))
        if len(srgs) != 1:
            die("chapter %d holds labs of %s; use one chapter for each SRG" % (number, " and ".join(srgs)))
        name = volume.srg_name(srgs[0])
        file_name = "%02d-%s-srg-requirement-labs.md" % (number, re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-"))
        files[file_name] = lab_chapter(volume, number, name, chapter_labs)
    if SHARED not in volume.names:
        files[SHARED] = shared_chapter(volume, sorted(files))
    manual = register(volume, files)
    for file_name, text in files.items():
        write(volume.path(file_name), text)
    print("Wrote %d chapter(s) in %s/chapters:" % (len(files), volume.folder))
    for file_name in sorted(files):
        print("  %s" % file_name)
    print("TODO comments to replace: %d" % sum(text.count(MARK) for text in files.values()))
    print("Steps the script cannot do: %d" % len(manual))
    for step in manual:
        print("  " + step)
    print("Nothing was committed. Next: write the labs, then run --lab-column and --check.")


def lab_chapter(volume, number, name, chapter_labs):
    ids = [row["srg_id"] for lab in chapter_labs for row in lab["rows"]]
    has_alignment = any(row["alignment"] for lab in chapter_labs for row in lab["rows"])
    first_map = volume.maps[0]
    # With --scope map the plan leaves out the IDs that only a crosswalk cites, and the chapter has to say so.
    srg = chapter_labs[0]["srgs"][0]
    others = [i for i in volume.cited if volume.info[i]["srg"] == srg and i not in ids]
    if others:
        covered = ("Chapter 01 lists %d distinct %s SRG requirements for %s. Each one has a lab or a gap lab in this "
                   "chapter, so none is left without a test. The crosswalk also cites %d %s IDs that belong to the "
                   "other vendor's rules. They are not requirements of %s, and they have no lab." % (
                       len(set(ids)), name, volume.product, len(others), srg, volume.product))
    else:
        covered = ("This volume's tables cite %d distinct %s SRG requirements. Each one has a lab or a gap lab in this "
                   "chapter, so none is left without a test." % (len(set(ids)), name))
    out = ["# Chapter %02d: %s SRG Requirement Labs" % (number, name), "", "## Learning Objectives", "",
           "- Prove each %s SRG requirement of this volume on the Chapter 999 lab, with a positive and a "
           "negative test." % name,
           "- " + todo("add three or four objectives that name what the reader configures in these labs."),
           "- Store the evidence for each lab so it can support an assessment.", "",
           "## Theory and Architecture", "",
           todo("one paragraph on what this SRG covers for %s, and one on the order of the labs and why." % volume.product), "",
           "All labs run on the network from [Chapter 999](%s)." % SHARED, "",
           "### Requirements and labs", "",
           covered, "",
           "| Lab | Requirements | Kind |", "| --- | --- | --- |"]
    for lab in chapter_labs:
        kind = "Gap lab" if "gap" in lab["kinds"] else "Requirement lab"
        out.append("| %s | %d | %s: %s |" % (lab["id"], len(lab["rows"]), kind, lab["title"]))
    out += ["",
            "A **requirement lab** configures the %s setting, proves it with a positive test, and proves the control "
            "with a negative test. A **gap lab** covers requirements that %s cannot meet: it proves that the setting is "
            "absent, applies the nearest compensating control, and records the disposition." % (volume.product, volume.product), "",
            "## Design Considerations", "",
            todo("four to six bullets, each with a bold lead, on how to run these labs safely and what the evidence must show."), "",
            "## Implementation and Automation", "",
            "Each lab lists its commands in the order to enter them. Commands come from "
            "[Chapter 01](%s), with the lab's values from Chapter 999 substituted." % first_map,
            todo("name the placeholders the labs use and where each value comes from."), "",
            "Save the evidence for each lab in `evidence/<lab>/<date>/`, as Chapter 999 describes.", "",
            "## Validation and Troubleshooting", "",
            todo("the baseline checks to run before and after each lab, then a table of symptom, cause, and fix."), "",
            "## Security and Best Practices", "",
            todo("four or five bullets on running the tests only in the lab and on handling secrets and evidence."), "",
            "## References and Knowledge Checks", "", "**References:**", "",
            "- [Chapter 01](%s)%s for the rows these labs prove." % (first_map, "".join(
                " and [Chapter %s](%s)" % (c.split("-", 1)[0], c) for c in volume.crosswalks)),
            "- [Chapter 999](%s) for the lab network, hosts, and baseline." % SHARED,
            "- " + todo("the SRG with its release, and the vendor documents the commands come from."),
            "- [Volume CLXXII, Chapter 03](../../volume-172-disa-srgs-and-stigs/chapters/"
            "03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md) for assessing a product that has no STIG.", "",
            "**Knowledge checks:**", "", "1. " + todo("four or five questions that the labs answer."), "",
            "## Hands-On Lab", "",
            "**Shared prerequisites.** The infrastructure from Chapter 999 and its baseline. "
            + todo("the accounts, tools, and access every lab of this chapter needs, and any cost."), ""]
    for lab in chapter_labs:
        gap = "gap" in lab["kinds"]
        header = "| SRG ID | CAT | Requirement |" + (" Alignment in Chapter 02 |" if has_alignment else "") + " Features in Chapter 01 |"
        out += ["### Lab %s — %s" % (lab["id"], lab["title"]), "",
                "**Goal.** " + todo("one sentence: what this lab shows." if not gap else
                                    "one sentence: confirm the setting is absent, apply the nearest compensating control, "
                                    "and record the disposition."), "",
                header, "| --- | --- | --- |" + (" --- |" if has_alignment else "") + " --- |"]
        for row in lab["rows"]:
            entry = volume.info.get(row["srg_id"], {"features": []})
            features = entry["features"][:3] + (["and %d more" % (len(entry["features"]) - 3)] if len(entry["features"]) > 3 else [])
            out.append("| `%s` | %s | %s |%s %s |" % (
                row["srg_id"], row["cat"] or "II", row["requirement"].replace("|", "\\|"),
                (" %s |" % (row["alignment"] or "—")) if has_alignment else "", "; ".join(features) or "—"))
        out += ["", "**Uses.** " + todo("the lab hosts this lab needs, by their Chapter 999 names."), "",
                "**Configure.**", "",
                todo("numbered steps, each with its command in a text code block. Take every command from Chapter 01 and "
                     "put in the lab's values." if not gap else
                     "numbered steps: show that the setting does not exist (the command and what to keep as proof), then "
                     "configure the nearest compensating control from Chapter 01."), "",
                "**Positive test.** " + todo("what to do and what must happen when the control works."), "",
                "**Negative test.** " + todo("what to try that the control must refuse, and how the refusal shows."), "",
                "**Evidence.** " + todo("the outputs and log lines to keep."), "",
                "**Return to baseline.** " + todo("how to undo this lab, by the baseline lab of Chapter 999."), ""]
    first, last = chapter_labs[0]["id"], chapter_labs[-1]["id"]
    out += ["## Lab Verification", "",
            "Complete this sign-off once Labs %s to %s have been run end to end, including each negative test. Until then, "
            "the labs are unverified, and the commands in this chapter come from Chapter 01 and have not been run in this "
            "lab." % (first, last), "",
            "- **Lab verified by:** *pending*", "- **Date:** *pending*", "",
            "## Summary and Completion Checklist", "",
            todo("two sentences on what the chapter proves and which requirements %s cannot meet." % volume.product), "",
            "- [ ] Has run each requirement lab and its negative test.",
            "- [ ] Has recorded the gap evidence and the compensating control for each gap lab.",
            "- [ ] Has stored the evidence for each lab.", ""]
    return "\n".join(out)


def shared_chapter(volume, lab_files):
    """A first version of Chapter 999, with the product's prerequisites listed for mapping to lab hosts."""
    prerequisites = []
    lines = read(volume.path(volume.maps[0])).split("\n")
    inside = False
    for line in lines:
        if line.startswith("### "):
            inside = line.strip().endswith(" prerequisites")
        elif inside and re.match(r"\| P\d+ \|", line):
            row = cells(line)
            prerequisites.append((row[0], row[1]))
    out = ["# Chapter 999: Shared Lab Infrastructure", "", "## Learning Objectives", "",
           "- Build the lab that every requirement lab of this volume runs on.",
           "- " + todo("add four or five objectives: the hosts, the address plan, the baseline, and the evidence folders."), "",
           "## Theory and Architecture", "",
           "### What this chapter is for", "",
           "The requirement labs of this volume share one lab, so that each lab starts from the same known state and "
           "the evidence of one lab can be compared with another. This chapter builds that lab and its baseline.", "",
           "### The %s under test" % volume.product, "",
           todo("the model or virtual machine, the release, the license, and how it is reached."), "",
           "### Topology", "", todo("the hosts and how they connect, with a diagram if one exists."), "",
           "### Address plan", "",
           todo("the networks, and a table of hosts with their addresses and services. Reuse the lab network of "
                "Volume CCI Chapter 999 where the same services serve, and say so."), "",
           "### How prerequisites map to this lab", "",
           "Each prerequisite of [Chapter 01](%s) needs a host or a service in the lab." % volume.maps[0], "",
           "| ID | Prerequisite | Lab host or service |", "| --- | --- | --- |"]
    for pid, text in prerequisites:
        out.append("| %s | %s | %s |" % (pid, text, todo("the host or service, or 'not built in this lab' with the reason.")))
    out += ["", "## Design Considerations", "",
            todo("four to six bullets: isolation from production, the baseline and how labs return to it, and licenses."), "",
            "## Implementation and Automation", "", "### Evidence", "",
            "Save the output that each lab's **Evidence** line names in `evidence/<lab>/<date>/`, with the model and the "
            "release at the top of each file, and replace passwords, keys, and secrets with `<SECRET>`.", "",
            "## Validation and Troubleshooting", "", todo("the checks that show the lab is at its baseline, and common faults."), "",
            "## Security and Best Practices", "", todo("four or five bullets on keeping the lab apart and handling secrets."), "",
            "## References and Knowledge Checks", "", "**References:**", "",
            "- [Chapter 01](%s) for the prerequisites this lab provides." % volume.maps[0],
            "- " + todo("the vendor documents for installing the product and the lab services."), "",
            "**Knowledge checks:**", "", "1. " + todo("three or four questions on the lab's design."), "",
            "## Hands-On Lab", "",
            "### Lab 999.1 — " + todo("replace this heading's comment with the title of the first build lab, and write "
                                      "the build labs: one for each part of the lab, the last one takes the baseline and "
                                      "resets to it."), "",
            "## Lab Verification", "",
            "Complete this sign-off once the build labs have been run end to end. Until then, the lab is unverified.", "",
            "- **Lab verified by:** *pending*", "- **Date:** *pending*", "",
            "## Summary and Completion Checklist", "", todo("two sentences on what the lab provides."), "",
            "- [ ] Has built the lab and taken its baseline.",
            "- [ ] Can return the lab to its baseline between labs.", ""]
    return "\n".join(out)


def register(volume, files):
    """Register new chapters in book.yml, the root README.md, PROJECT_STATUS.md, and the volume README. Returns manual steps."""
    manual, added = [], len(files)
    titles = dict((name, read_title(text)) for name, text in files.items())
    lines = read("book.yml").split("\n")
    start = next((i for i, line in enumerate(lines) if line == "  - id: volume-%d" % volume.number), None)
    if start is None:
        die("book.yml has no volume-%d" % volume.number)
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("  - id: ")), len(lines))
    count = next(i for i in range(start, end) if lines[i].startswith("    chapter_count: "))
    lines[count] = "    chapter_count: %d" % (int(lines[count].split(":")[1]) + added)
    for name in sorted(files, key=lambda n: int(n.split("-", 1)[0])):
        number = name.split("-", 1)[0]
        entry = ["      - id: %s" % number, '        title: "%s"' % titles[name], "        path: %s" % volume.path(name)]
        spot = next((i for i in range(start, end) if re.match(r"      - id: (\d+)$", lines[i])
                     and int(lines[i].split(":")[1]) > int(number)), end)
        lines[spot:spot] = entry
        end += len(entry)
    write("book.yml", "\n".join(lines))

    text = read("README.md")
    hit = re.search(r"(\d+) volumes, (\d+) chapters\. Each volume has a dedicated", text)
    row = re.search(r"(?m)^(\| [A-Z]+ \| \[[^\]]+\]\(%s/README\.md\) \| )(\d+)( \|)$" % re.escape(volume.folder), text)
    if not hit or not row:
        die("README.md has no chapter total or no row for %s" % volume.slug)
    text = text[:row.start()] + row.group(1) + str(int(row.group(2)) + added) + row.group(3) + text[row.end():]
    hit = re.search(r"(\d+) volumes, (\d+) chapters\. Each volume has a dedicated", text)
    text = text[:hit.start()] + "%s volumes, %d chapters. Each volume has a dedicated" % (
        hit.group(1), int(hit.group(2)) + added) + text[hit.end():]
    write("README.md", text)

    text = read("PROJECT_STATUS.md")
    title = read(volume.folder + "/README.md").split("\n", 1)[0][2:].strip().replace("Volume ", "", 1)
    row = re.search(r"(?m)^(\| %s \| )(\d+)( \| Drafted \|)$" % re.escape(title), text)
    hit = re.search(r"\*\*Total declared chapters:\*\* (\d+) of (\d+) drafted", text)
    if not hit or not row:
        die("PROJECT_STATUS.md has no chapter total or no row for '%s'" % title)
    text = text[:row.start()] + row.group(1) + str(int(row.group(2)) + added) + row.group(3) + text[row.end():]
    hit = re.search(r"\*\*Total declared chapters:\*\* (\d+) of (\d+) drafted", text)
    text = text[:hit.start()] + "**Total declared chapters:** %d of %d drafted" % (
        int(hit.group(1)) + added, int(hit.group(2)) + added) + text[hit.end():]
    write("PROJECT_STATUS.md", text)

    path = volume.folder + "/README.md"
    lines = read(path).split("\n")
    last = next((i for i, line in enumerate(lines) if line.startswith("90. [")), None)
    if last is None:
        manual.append("%s: list the new chapters under Chapters." % path)
    else:
        new = ["%d. [%s](chapters/%s) — %s" % (int(n.split("-", 1)[0]), titles[n].split(": ", 1)[1], n,
                                                 todo("one sentence: how many labs for how many requirements, and their topics."))
               for n in sorted(files, key=lambda n: int(n.split("-", 1)[0]))]
        lines[last:last] = [l for l in new if not l.startswith("999.")]
        last = next(i for i, line in enumerate(lines) if line.startswith("90. ["))
        lines[last + 1:last + 1] = [l for l in new if l.startswith("999.")]
        text = "\n".join(lines)
        total = len(volume.names) + added
        for pattern in (r"(The volume has )(\w+)( chapters:)", r"(across all )(\w+)( chapters\.)"):
            hit = re.search(pattern, text)
            if hit and total < len(WORDS):
                text = text[:hit.start()] + hit.group(1) + WORDS[total] + hit.group(3) + text[hit.end():]
            else:
                manual.append("%s: update the chapter count in the sentence that matches '%s'." % (path, pattern))
        write(path, text)
    manual.append("%s: describe the new chapters in the Overview and change the Lab coverage section." % path)
    manual.append("%s: add index entries and glossary terms for the labs." % volume.folder)
    manual.append("%s: record how the labs were built." % volume.path(AS_BUILT))
    return manual


def read_title(text):
    return text.split("\n", 1)[0][2:].strip()


def lab_column(volume):
    changed = []
    for name in volume.maps + volume.crosswalks:
        new = volume.with_lab_column(name)
        if new != read(volume.path(name)):
            write(volume.path(name), new)
            changed.append(name)
    print("Lab column: %d chapter(s) changed%s" % (len(changed), ": " + ", ".join(changed) if changed else ""))
    done = subprocess.run([sys.executable, EXPORT], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    print("CSV export: %s" % ("ran" if done.returncode == 0 else "FAILED"))
    return done.returncode


def check(volume, allow, scope):
    problems = []
    if not volume.lab_chapters:
        problems.append("the volume has no lab chapter (NN-...-srg-requirement-labs.md)")
    if SHARED not in volume.names:
        problems.append("the volume has no %s" % SHARED)
    elif not re.search(r"(?m)^### Lab 999\.\d+ — ", read(volume.path(SHARED))):
        problems.append("%s has no build lab (### Lab 999.N — ...)" % SHARED)
    for name in volume.lab_chapters + ([SHARED] if SHARED in volume.names else []):
        text = read(volume.path(name))
        for i, line in enumerate(text.split("\n"), 1):
            if MARK in line:
                problems.append("%s line %d: a TODO comment is left" % (name, i))
        if "## Lab Verification" not in text or "**Lab verified by:**" not in text:
            problems.append("%s has no Lab Verification sign-off" % name)
        for target in re.findall(r"\]\(([^)\s#]+)(?:#[^)\s]*)?\)", text):
            if "://" not in target and not os.path.exists(os.path.normpath(os.path.join(volume.folder, "chapters", target))):
                problems.append("%s: the link to %s does not resolve" % (name, target))
    for i, line in enumerate(read(volume.folder + "/README.md").split("\n"), 1):
        if MARK in line:
            problems.append("README.md line %d: a TODO comment is left" % i)
    for name in volume.lab_chapters:
        text = read(volume.path(name))
        number = int(name.split("-", 1)[0])
        mine = [lab for lab in volume.labs if lab["chapter"] == name]
        if [lab["id"] for lab in mine] != ["%d.%d" % (number, i) for i in range(1, len(mine) + 1)]:
            problems.append("%s: its labs are not numbered %d.1, %d.2, ... in order" % (name, number, number))
        for lab in mine:
            if lab["parts"] != PARTS:
                missing = [p for p in PARTS if p not in lab["parts"]]
                problems.append("%s Lab %s: %s" % (name, lab["id"], ("missing " + ", ".join(missing)) if missing
                                                   else "its parts are out of order or repeated"))
            if not lab["rows"]:
                problems.append("%s Lab %s has no requirement row (| `SRG-...` | CAT | Requirement | ...)" % (name, lab["id"]))
        ids = [srg_id for lab in mine for srg_id, _, _ in lab["rows"]]
        stated = re.search(r"(?:lists|cite) (\d+) distinct", text)
        if not stated:
            problems.append("%s does not state how many distinct requirements it covers" % name)
        elif int(stated.group(1)) != len(set(ids)):
            problems.append("%s says %s distinct requirements, and its labs hold %d" % (name, stated.group(1), len(set(ids))))
        summary = dict((m.group(1), (int(m.group(2)), m.group(3), m.group(4))) for m in re.finditer(
            r"(?m)^\| (\d+\.\d+) \| (\d+) \| (Requirement lab|Gap lab): (.+?) \|$", text))
        for lab in mine:
            if lab["id"] not in summary:
                problems.append("%s: the Requirements and labs table has no row for Lab %s" % (name, lab["id"]))
            else:
                count, _, title = summary[lab["id"]]
                if count != len(lab["rows"]):
                    problems.append("%s: the table says Lab %s has %d requirements, and the lab lists %d" % (
                        name, lab["id"], count, len(lab["rows"])))
                if title != lab["title"]:
                    problems.append("%s: the table and the heading of Lab %s have different titles" % (name, lab["id"]))
        for lab_id in summary:
            if lab_id not in [lab["id"] for lab in mine]:
                problems.append("%s: the table lists Lab %s, which the chapter does not have" % (name, lab_id))
    for srg_id in volume.cited:
        if scope == "map" and volume.info[srg_id]["source"] != "map":
            continue
        if srg_id not in volume.lab_of and srg_id not in allow:
            problems.append("%s is cited by the tables and has no lab" % srg_id)
    for srg_id in allow:
        if srg_id in volume.lab_of:
            problems.append("%s is on the --allow list and has a lab" % srg_id)
    for name in volume.maps + volume.crosswalks:
        text = read(volume.path(name))
        lines = text.split("\n")
        for kind, start, _ in tables(text, name in volume.maps):
            if cells(lines[start])[-1] != "Lab":
                problems.append("%s: the %s table has no Lab column" % (name, kind))
        if volume.with_lab_column(name) != text:
            problems.append("%s: the Lab column is out of date; run --lab-column" % name)
    print("Check of the labs of %s: %s" % (volume.slug, "OK" if not problems else "%d problem(s)" % len(problems)))
    for problem in problems[:60]:
        print("  " + problem)
    if len(problems) > 60:
        print("  ... and %d more" % (len(problems) - 60))
    if not problems:
        print("  %d labs in %d chapter(s) cover %d requirements. Now run scripts/bash/validate.sh." % (
            len(volume.labs), len(volume.lab_chapters), len(volume.lab_of)))
    return 1 if problems else 0


def main():
    parser = argparse.ArgumentParser(description="Plan, scaffold, link, and check the SRG requirement labs of a volume.")
    parser.add_argument("product", help='the product in the volume folder name, for example "FortiAnalyzer"')
    parser.add_argument("--plan-file", help="write the plan to this tab-separated file")
    parser.add_argument("--scaffold", metavar="PLAN", help="write the lab chapters from this filled plan file")
    parser.add_argument("--lab-column", action="store_true", help="add or refresh the Lab column")
    parser.add_argument("--check", action="store_true", help="check finished labs")
    parser.add_argument("--allow", default="", help="SRG IDs that need no lab of their own, separated by commas")
    parser.add_argument("--scope", choices=["all", "map"], default="all",
                        help="all: every SRG ID the tables cite; map: only the map's requirement reference")
    args = parser.parse_args()
    if not os.path.exists("book.yml") or not os.path.isdir("volumes"):
        die("run this from the repository root")
    allow = [x.strip() for x in args.allow.split(",") if x.strip()]
    volume = Volume(args.product)
    if args.scaffold:
        scaffold(volume, args.scaffold)
    elif args.lab_column:
        sys.exit(lab_column(volume))
    elif args.check:
        sys.exit(check(volume, allow, args.scope))
    else:
        show_plan(volume, allow, args.plan_file, args.scope)


if __name__ == "__main__":
    main()
