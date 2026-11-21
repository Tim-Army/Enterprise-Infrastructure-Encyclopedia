---
name: srg-labs-for
description: Build the SRG requirement labs for a Fortinet product volume of the 200 to 299 block, the way Volume CCI (FortiSwitch) has them — a shared lab chapter 999, one lab chapter for each SRG with requirement labs and gap labs, and a Lab column in every SRG table of the map and crosswalk chapters. Use when the user runs /srg-labs-for <product> or asks for labs for a product's SRG map.
argument-hint: <Fortinet product that has a volume of its own, for example "FortiAnalyzer">
---

# /srg-labs-for

Build the requirement labs for one product volume, the way Volume CCI
(FortiSwitch) was built: Chapter 999 for the shared lab, Chapters 04 to 07
for the labs (41 labs for 185 requirements), and a **Lab** column in
Chapters 01 to 03. The product must already have a volume of its own; if it
does not, run `/stig-volume-for` first. Everything happens inside this
repository.

Paths used below:

- `VOL` = `volumes/volume-2NN-<product>-stig-and-srg-mapping`
- `SKILL` = `.claude/skills/srg-labs-for`
- `LABS` = `python SKILL/labs.py`, run from the repository root
- The plan file goes in `temp/<product>-labs/plan.tsv` (`temp/` is ignored
  by git). Write no `.md` files under `temp/`.

The argument is the product name in the volume's folder, for example
`FortiAnalyzer`. If it is missing, ask for it.

## What the workflow produces

1. **Chapter 999, Shared Lab Infrastructure**: the lab every requirement lab
   runs on, with its hosts, address plan, the host or service behind each
   prerequisite of Chapter 01, the build labs (999.1, 999.2, and so on), and
   a baseline that every lab returns to.
2. **One lab chapter for each SRG**, numbered after the map and crosswalk
   chapters and titled "<SRG name> SRG Requirement Labs". Its labs are
   numbered `<chapter>.<n>`. Each lab proves a group of related requirements.
3. **A Lab column** as the last column of every SRG table in the map and
   crosswalk chapters (the feature map, the requirement reference, the
   crosswalk table, and the unmatched-requirement table), which links each
   SRG ID to its lab, and the same column in the CSV downloads.
4. **Updated records**: `book.yml`, the root `README.md`,
   `PROJECT_STATUS.md`, and the volume's README, index, glossary, and
   Chapter 90.

## Rules

- **Every requirement gets one lab.** A requirement the product can meet
  goes in a requirement lab. A requirement it cannot meet goes in a gap lab.
  None is left without a test.
- **A requirement lab has a positive test and a negative test.** It
  configures the setting, shows that the control works, and shows that the
  control refuses what it must refuse.
- **A gap lab proves the gap.** It shows that the setting does not exist,
  applies the nearest compensating control, and records the disposition.
- **Take every command from the map or crosswalk chapter.** Put in the lab's
  values from Chapter 999. Do not write a command that those chapters do not
  have. If a lab needs one, leave the step as words and say what is missing.
- **Do not change a row or a command of the map and crosswalk chapters.**
  Only the Lab column is added to them.
- **Do not say a lab was run.** The Lab Verification sign-off stays
  *pending* until a person has run the labs, and each lab chapter says that
  its commands have not been run in this lab.
- **Do not download anything** without the user's go-ahead, for example a
  virtual machine image to try a lab.
- **Do not commit or push** as part of this workflow. See *Commit* below.

## Steps

### 1. Plan

```bash
python .claude/skills/srg-labs-for/labs.py "<product>"
```

The script changes nothing. It prints the map and crosswalk chapters it
read, the number of requirements for each SRG, how many are cited only by a
crosswalk, how many already have a lab, how many are gap lab candidates, and
the chapter numbers that are free.

### 2. Agree the lab design with the user

Show the user the plan and settle these points before you write anything:

- **Scope.** Volume CCI gives a lab to every SRG ID that its tables cite,
  because its crosswalks use the Cisco rules as a FortiSwitch checklist. A
  crosswalk that is anchored on the product, such as FortiAnalyzer's, also
  cites IDs of the other vendor's rules. Ask whether those get labs. If
  not, use `--scope map` in every later command, which counts only the
  requirements of the map chapter's requirement reference.
- **IDs with no lab of their own.** A retired SRG ID whose rule the map
  points at a current ID needs no lab. Pass such IDs with `--allow`, and
  name them in Chapter 90.
- **The product under test.** Hardware or virtual machine, the release, and
  the license.
- **The lab network.** Reuse the lab of Volume CCI Chapter 999 where the
  same services serve (authentication, logging, time, certificates), or
  build a smaller lab. List the host or service for each prerequisite of
  Chapter 01.

### 3. Group the requirements into labs

```bash
python .claude/skills/srg-labs-for/labs.py "<product>" --plan-file temp/<product>-labs/plan.tsv
```

The plan file has one row for each requirement. Fill two columns and check
one:

- `lab`: the lab number, `<chapter>.<n>`. Use one chapter for each SRG, and
  number the labs of a chapter 1, 2, 3 with no gap.
- `lab_title`: the lab's title, on at least one row of the lab.
- `kind`: `requirement` or `gap`. The script proposes `gap` when no feature
  of the map has a command for the requirement, when the crosswalk shows no
  command for it, or when every alignment is *Not supported* or *Not
  applicable*. Read the map before you accept or change it. A lab holds
  rows of one kind.

Group the way Volume CCI does. Follow a sequence the reader can run, for
example the life of an administrator session in its Chapter 05: who may
connect, logon behavior, passwords, audit records, time, cryptography,
backup. Keep a lab to about one to ten requirements. Put the gap labs last
in the chapter and start their titles with "Gaps:". You may also shorten the
`requirement` text to a plain summary.

### 4. Scaffold

```bash
python .claude/skills/srg-labs-for/labs.py "<product>" --scaffold temp/<product>-labs/plan.tsv
```

The script writes one chapter for each SRG and, if the volume has none,
Chapter 999. It fills in what it can derive: the lab headings, the table of
requirements and labs, each lab's requirement rows (SRG ID, category,
requirement, alignment, and the features of Chapter 01), and the sign-off.
It registers the chapters in `book.yml`, the root `README.md`,
`PROJECT_STATUS.md`, and the volume README's chapter list. It puts a comment
that starts `TODO srg-labs-for` wherever you have to write.

### 5. Write Chapter 999

Model: Chapter 999 of Volume CCI. Write the product under test, the
topology, the address plan, the host or service for each prerequisite, the
build labs, and the baseline lab that the requirement labs return to. Name
every host, because the labs refer to hosts by these names.

### 6. Write the labs

Model: Chapters 04 to 07 of Volume CCI. Each lab has these parts, in this
order, and the check enforces them:

`**Goal.**`, the requirement table, `**Uses.**`, `**Configure.**`,
`**Positive test.**`, `**Negative test.**`, `**Evidence.**`,
`**Return to baseline.**`

- Under **Configure**, number the steps and put each command in a `text`
  code block.
- **Uses** names the Chapter 999 hosts the lab needs.
- **Evidence** names the outputs and log lines to keep.
- Replace every TODO comment in the chapter's other sections too.

### 7. Add the Lab column

```bash
python .claude/skills/srg-labs-for/labs.py "<product>" --lab-column
```

The script adds or refreshes the column and runs the CSV export. Run it
again whenever a lab is added, renamed, or renumbered. A row that cites
several SRG IDs lists each lab once, in the order of the IDs. A row with no
lab shows a dash.

### 8. Bring the volume's records up to date

The scaffold lists these as steps it cannot do:

- The volume README: describe the lab chapters in the Overview, replace the
  TODO comments in the chapter list, and rewrite the *Lab coverage* section,
  which says the volume has no labs.
- The index and the glossary: add the labs' topics and terms.
- Chapter 90: record how the labs were built, on what date, and from which
  chapters, with the scope and the `--allow` list.

A diagram of the lab network belongs in Chapter 999 and at the top of each
lab chapter's Hands-On Lab section, as in Volume CCI. Draw it only if the
user asks for it.

### 9. Check

```bash
python .claude/skills/srg-labs-for/labs.py "<product>" --check
```

```bash
bash scripts/bash/validate.sh
```

Add `--scope map` and `--allow` if you used them. The check fails while a
TODO comment remains, a lab lacks a part or a requirement row, the table of
requirements and labs disagrees with the labs, a requirement has no lab, a
link does not resolve, or the Lab column is out of date. Fix every failure.

### 10. Report

Tell the user how many labs cover how many requirements, which requirements
went to gap labs, and what is not verified. The labs have not been run, and
say so. Say that nothing is committed.

## Commit

Commit and push only when the user asks. Use one commit for the labs of a
volume, because the scaffold registers the lab chapters and Chapter 999
together and the Lab column needs the labs:

`Vol <ROMAN> Ch NN, MM, 999: SRG requirement labs for all <N> <Product> requirements`

The body lists the lab chapters with their counts, the gap labs, the scope
and the `--allow` list, the Lab column, and what was checked. It says that
the labs have not been run, and ends with the attribution line. After a
push, watch the Validate and Deploy Pages runs, then open a lab chapter on
the site and follow one Lab link from the map chapter.

## Keep the records current

Volume CLXXII's Chapter 90 describes this workflow under *Requirement labs
for a product volume*. When this skill or the script changes, update that
section in the same commit.

## How the script decides

- **Which requirements.** Every SRG ID in the feature map, the requirement
  reference, the crosswalk table, and the unmatched-requirement table. An ID
  of the requirement reference is the product's own requirement. Any other
  ID is "cited only by a crosswalk".
- **Which SRG.** The abbreviation in the requirement reference, for example
  CLS or NDM. The script knows the names of NDM, CLS, L2S, RTR, and AAA, and
  reads any other from a map chapter that writes the abbreviation after the
  name. If a chapter title comes out as an abbreviation, write the SRG's
  full name in the title, the file name, and `book.yml`.
- **Which lab a row links to.** The lab whose requirement table has the
  row's SRG ID. The link's anchor is the one GitHub gives the lab heading.
- **What it checked itself against.** On Volume CCI the script finds 41
  labs for 185 requirements, proposes the same 48 requirements for gap labs
  that the volume's gap labs hold, and reproduces the Lab column of
  Chapters 01 to 03 exactly. Its command there is
  `python SKILL/labs.py FortiSwitch --check --allow SRG-APP-000373-NDM-000298,SRG-APP-000516-NDM-000351`.
