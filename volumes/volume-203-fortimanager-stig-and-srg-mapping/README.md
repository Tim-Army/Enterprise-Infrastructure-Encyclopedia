# Volume CCIII — FortiManager STIG and SRG Mapping

**Plan a lab build:** [Lab Selector with the FortiManager labs ticked](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-901-lab-selector/lab-scripts/selector/lab-selector.html?sets=fortimanager)

> A requirement-by-requirement map of **Fortinet FortiManager** to the DISA
> Security Requirements Guide (SRG) that applies to it. DISA publishes no
> FortiManager STIG, so a FortiManager in a DoD environment is assessed against
> the Network Device Management SRG. This volume shows which FortiManager
> release introduced each feature, which SRG requirement it helps meet, and
> the command or GUI location that configures it. Every table has a CSV
> download. A lab chapter tests each of FortiManager's 79 requirements on a
> FortiManager-VM, in the lab that Chapter 999 builds.

## Overview

Volume CCIII is the **FortiManager volume of the Fortinet STIG work**. Volume
numbers 200 to 299 are reserved for that work (see
[Structure.md](../../Structure.md)). The vendor-neutral material this volume
builds on, the framework, the SRG catalog, the Fortinet overview, and the
Cisco overview, stays in [Volume CLXXII — DISA SRGs and STIGs](../volume-172-disa-srgs-and-stigs/README.md).
The content chapter here was Chapter 13 of that volume and
moved on 2026-11-20. Volume CLXXII keeps a short pointer page at the old
chapter number, so earlier links still work.

The volume has four chapters:

- **Chapter 01** is the **FortiManager feature, version, and SRG map**: 487
  FortiManager features (52 core platform features and the 435 features in
  the New Features Guides for FortiManager 7.0 to 8.0), the release that
  introduced each one, the Network Device Management SRG requirement it maps
  to, and the command or GUI location that meets the requirement, with a
  table of 23 prerequisites. A FortiManager can change every managed device,
  so the map gives the most weight to access control, auditing, and
  configuration-change control.
- **Chapter 02** holds the **Network Device Management SRG requirement
  labs**: seventeen labs for the 79 requirements of Chapter 01. A requirement
  FortiManager can meet gets a lab with a positive and a negative test. Lab
  2.17 is a gap lab for the one requirement the unit cannot meet, the check
  of new passwords against a list of compromised passwords: it proves that
  the setting is absent, applies the nearest compensating control, and
  records the disposition.
- **Chapter 90**, the as-built chapter, records how Chapter 01 was built, when, and
  from which sources, what changed after the first build, the move from
  Volume CLXXII, and how the labs were built.
- **Chapter 999** is the **shared lab infrastructure**: a FortiManager-VM on
  release 7.6 on the lab network of Volume CCI, with the FortiGate-VM of
  Volume CCII as its managed device. The labs reuse the service hosts of
  Volume CCI and the mail server of Volume CCII.

## CSV downloads

Each table in Chapter 01 has a CSV copy in this volume's `data/` folder and a
download link on the line above the table. `scripts/python/export_srg_tables.py`
writes the files from the chapter tables, so a file always has the same rows
as its table.

| Chapter | Table | Rows | File in `data/` |
| --- | --- | ---: | --- |
| 01 | FortiManager prerequisites | 23 | `01-fortimanager-feature-version-and-srg-map-prerequisites.csv` |
| 01 | The FortiManager feature map | 487 | `01-fortimanager-feature-version-and-srg-map-feature-map.csv` |
| 01 | Requirement reference | 79 | `01-fortimanager-feature-version-and-srg-map-requirements.csv` |

The files moved with the chapter, so the download addresses changed. The
addresses under `data/volume-172-disa-srgs-and-stigs/` that began with `13-`
no longer exist.

## Chapters

1. [FortiManager Feature, Version, and SRG Map](chapters/01-fortimanager-feature-version-and-srg-map.md) — 487 FortiManager features (52 core platform features and every feature in the 7.0 to 8.0 New Features Guides) with the release that introduced each, the NDM SRG requirement it maps to, and the command that meets it.
2. [Network Device Management SRG Requirement Labs](chapters/02-network-device-management-srg-requirement-labs.md) — seventeen labs for the 79 NDM requirements: roles and ADOMs, the management path, logon protections, password policy, authentication servers, certificates, audit events and their content, changes and privileged commands, protecting, storing, and off-loading the event log, time, cryptography, change control for managed devices, configuration backup, and the software release, plus a gap lab for the check of new passwords against a list of compromised passwords.
90. [As-Built — How This Volume Was Built](chapters/90-as-built-how-this-volume-was-built.md) — how and when Chapter 01 was built, from which sources, and what changed after the first build, including the move from Volume CLXXII and the labs of Chapters 02 and 999.
999. [Shared Lab Infrastructure](chapters/999-shared-lab-infrastructure.md) — the lab for this volume's requirement labs: a FortiManager-VM on release 7.6 on the lab network of Volume CCI, the FortiGate-VM of Volume CCII as its managed device, the reused mail server and service hosts, the host or service behind each of the 23 prerequisites, four build labs, and the `baseline-203` snapshots.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all four chapters.
- [Glossary](GLOSSARY.md) — definitions for terms used in this volume.

## Related volumes

- **Other Fortinet STIG volumes:** [Volume CCI — FortiSwitch STIG and SRG Mapping](../volume-201-fortiswitch-stig-and-srg-mapping/README.md), [Volume CCII — FortiAnalyzer STIG and SRG Mapping](../volume-202-fortianalyzer-stig-and-srg-mapping/README.md).
- [Volume CLXXII — DISA SRGs and STIGs](../volume-172-disa-srgs-and-stigs/README.md)
  for the framework (Chapters 01 to 09), the Fortinet overview (Chapter 10), the
  product maps and crosswalks that have not moved, and the Cisco chapters.
- [Volume CMI — Lab Selector](../volume-901-lab-selector/README.md), whose page plans a lab build for the
  requirement labs of this volume:
  [open it with the FortiManager lab set ticked](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-901-lab-selector/lab-scripts/selector/lab-selector.html?sets=fortimanager).
- [Volume XIX — Fortinet NSE Certification Program](../volume-019-fortinet-network-security/README.md).

## Lab coverage

Chapters 01 and 90 have **no hands-on labs**, by design: they are reference
chapters that map requirements and record how the volume was built. Chapter
999 has the labs (999.1 to 999.4) that add the FortiManager and its managed
device to the lab network of Volume CCI and take the baseline. Chapter 02 has
the requirement labs that run on that lab: 17 labs for the 79 requirements of
Chapter 01. The Lab column of Chapter 01 links each SRG ID to its lab.

The labs have not been run. Each lab chapter carries a sign-off that stays
pending until a person has run its labs, and the commands come from Chapter
01, which checked them against the FortiManager 8.0.1 CLI Reference. The labs
are written for release 7.6, and they say where that release differs.

## Software and platform baseline

DISA content is the quarterly release recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md).
From that release the chapter uses the Network Device Management SRG V5R5.
Version data in Chapter 01 comes from the FortiManager New Features Guides
for release trains 7.0, 7.2, 7.4, 7.6, and 8.0, which cover FortiManager
7.0.0 through 8.0.1. Commands were checked against the FortiManager 8.0.1 CLI
Reference. The labs of Chapters 02 and 999 are written for a FortiManager-VM
on release 7.6 and for the lab network of Volume CCI.
Confirm the current release of any STIG or SRG on the DoD Cyber Exchange
before assessing against it.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-203-fortimanager-stig-and-srg-mapping
```

After changing a table in Chapter 01, regenerate the CSV downloads
(written to this volume's `data/` folder) and refresh the download links:

```bash
python scripts/python/export_srg_tables.py
```

After adding, renaming, or renumbering a lab, refresh the Lab column of
Chapter 01, then check the labs:

```bash
python .claude/skills/srg-labs-for/labs.py FortiManager --lab-column
```

```bash
python .claude/skills/srg-labs-for/labs.py FortiManager --check
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
