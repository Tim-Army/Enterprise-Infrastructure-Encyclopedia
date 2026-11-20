# Volume CCIII — FortiManager STIG and SRG Mapping

> A requirement-by-requirement map of **Fortinet FortiManager** to the DISA
> Security Requirements Guide (SRG) that applies to it. DISA publishes no
> FortiManager STIG, so a FortiManager in a DoD environment is assessed against
> the Network Device Management SRG. This volume shows which FortiManager
> release introduced each feature, which SRG requirement it helps meet, and
> the command or GUI location that configures it. Every table has a CSV
> download.

## Overview

Volume CCIII is the **FortiManager volume of the Fortinet STIG work**. Volume
numbers 200 to 299 are reserved for that work (see
[Structure.md](../../Structure.md)). The vendor-neutral material this volume
builds on, the framework, the SRG catalog, the Fortinet overview, and the
Cisco overview, stays in [Volume CLXXII — DISA SRGs and STIGs](../volume-172-disa-srgs-and-stigs/README.md).
The content chapter here was Chapter 13 of that volume and
moved on 2026-11-20. Volume CLXXII keeps a short pointer page at the old
chapter number, so earlier links still work.

The volume has two chapters:

- **Chapter 01** is the **FortiManager feature, version, and SRG map**: 487
  FortiManager features (52 core platform features and the 435 features in
  the New Features Guides for FortiManager 7.0 to 8.0), the release that
  introduced each one, the Network Device Management SRG requirement it maps
  to, and the command or GUI location that meets the requirement, with a
  table of 23 prerequisites. A FortiManager can change every managed device,
  so the map gives the most weight to access control, auditing, and
  configuration-change control.
- **Chapter 90**, the as-built chapter, records how Chapter 01 was built, when, and
  from which sources, what changed after the first build, and the move from
  Volume CLXXII.

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
90. [As-Built — How This Volume Was Built](chapters/90-as-built-how-this-volume-was-built.md) — how and when Chapter 01 was built, from which sources, and what changed after the first build, including the move from Volume CLXXII.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all two chapters.
- [Glossary](GLOSSARY.md) — definitions for terms used in this volume.

## Related volumes

- **Other Fortinet STIG volumes:** [Volume CCI — FortiSwitch STIG and SRG Mapping](../volume-201-fortiswitch-stig-and-srg-mapping/README.md), [Volume CCII — FortiAnalyzer STIG and SRG Mapping](../volume-202-fortianalyzer-stig-and-srg-mapping/README.md).
- [Volume CLXXII — DISA SRGs and STIGs](../volume-172-disa-srgs-and-stigs/README.md)
  for the framework (Chapters 01 to 09), the Fortinet overview (Chapter 10), the
  product maps and crosswalks that have not moved, and the Cisco chapters.
- [Volume XIX — Fortinet NSE Certification Program](../volume-019-fortinet-network-security/README.md).

## Lab coverage

This volume has **no hands-on labs**, by design. It is a reference. Each
chapter keeps its implementation examples (commands and configuration
snippets) and its knowledge checks, but omits the Hands-On Lab and Lab
Verification sections of the standard chapter template.

## Software and platform baseline

DISA content is the quarterly release recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md).
From that release the chapter uses the Network Device Management SRG V5R5.
Version data in Chapter 01 comes from the FortiManager New Features Guides
for release trains 7.0, 7.2, 7.4, 7.6, and 8.0, which cover FortiManager
7.0.0 through 8.0.1. Commands were checked against the FortiManager 8.0.1 CLI
Reference.
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

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
