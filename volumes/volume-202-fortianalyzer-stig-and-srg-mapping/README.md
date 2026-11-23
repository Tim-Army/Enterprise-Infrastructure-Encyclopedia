# Volume CCII — FortiAnalyzer STIG and SRG Mapping

**Plan a lab build:** [Lab Selector with the FortiAnalyzer labs ticked](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-901-lab-selector/lab-scripts/selector/lab-selector.html?sets=fortianalyzer)

> A requirement-by-requirement map of **Fortinet FortiAnalyzer** to the DISA
> Security Requirements Guides (SRGs) that apply to it, and a crosswalk that
> aligns its requirements with the Cisco STIGs. DISA publishes no
> FortiAnalyzer STIG, so a FortiAnalyzer in a DoD environment is assessed
> against the Central Log Server SRG, with the Network Device Management SRG
> for a few management requirements. This volume shows which FortiAnalyzer
> release introduced each feature, which SRG requirement it helps meet, and
> the command or GUI location that configures it. Every table has a CSV
> download. Two lab chapters test each of FortiAnalyzer's 65 requirements on a
> FortiAnalyzer-VM, in the lab that Chapter 999 builds.

## Overview

Volume CCII is the **FortiAnalyzer volume of the Fortinet STIG work**. Volume
numbers 200 to 299 are reserved for that work (see
[Structure.md](../../Structure.md)), and
[Volume CCI](../volume-201-fortiswitch-stig-and-srg-mapping/README.md) holds
the FortiSwitch material. The vendor-neutral material this volume builds on,
the framework, the SRG catalog, the Fortinet overview, and the Cisco overview,
stays in [Volume CLXXII — DISA SRGs and STIGs](../volume-172-disa-srgs-and-stigs/README.md).
The two content chapters here were Chapters 12 and 38 of that volume and
moved on 2026-11-20. Volume CLXXII keeps a short pointer page at each old
chapter number, so earlier links still work.

The volume has six chapters:

- **Chapter 01** is the **FortiAnalyzer feature, version, and SRG map**: 349
  FortiAnalyzer features (53 core platform features and the 296 features in
  the New Features Guides for FortiAnalyzer 7.0 to 8.0), the release that
  introduced each one, the Central Log Server or Network Device Management
  SRG requirement it maps to, and the command or GUI location that meets the
  requirement, with a table of 30 prerequisites.
- **Chapter 02** is the **FortiAnalyzer and Cisco STIG crosswalk**: all 65
  FortiAnalyzer requirements from Chapter 01 aligned with the Cisco Secure
  Network Analytics (SNA) STIG rule and the rules in every other Cisco STIG
  that implement the same or an equivalent requirement, and with the Cisco
  rules that govern the sending side of each log-server requirement. No Cisco
  STIG implements the Central Log Server SRG, so the table is anchored on
  FortiAnalyzer's requirements and not on a Cisco STIG.
- **Chapter 03** holds the **Central Log Server SRG requirement labs**:
  fifteen labs for the 60 Central Log Server requirements of Chapter 01. A
  requirement FortiAnalyzer can meet gets a lab with a positive and a
  negative test. Lab 3.15 is a gap lab for the two requirements the lab unit
  cannot meet: it proves that the setting is absent, applies the nearest
  compensating control, and records the disposition.
- **Chapter 04** holds the **Network Device Management SRG requirement
  labs**: two labs for the five NDM requirements of Chapter 01.
- **Chapter 90**, the as-built chapter, records how Chapters 01 and 02 were
  built, when, and from which sources, what changed after the first build,
  the move from Volume CLXXII, and how the labs were built.
- **Chapter 999** is the **shared lab infrastructure**: a FortiAnalyzer-VM on
  release 7.6, a FortiGate-VM that sends it logs, and a mail server, added to
  the lab network of Volume CCI, whose service hosts the labs reuse.

The Cisco side of the crosswalk lives in Volume CLXXII: the
[Cisco overview](../volume-172-disa-srgs-and-stigs/chapters/31-cisco-products-stigs-and-srg-mapping.md)
lists the Cisco STIG packages, including SNA. The other crosswalks are
Chapters 34 to 36 of that volume and Chapters 02 and 03 of Volume CCI.

## CSV downloads

Each table in Chapters 01 and 02 has a CSV copy in this volume's `data/`
folder and a download link on the line above the table.
`scripts/python/export_srg_tables.py` writes the files from the chapter
tables, so a file always has the same rows as its table.

| Chapter | Table | Rows | File in `data/` |
| --- | --- | ---: | --- |
| 01 | FortiAnalyzer prerequisites | 30 | `01-fortianalyzer-feature-version-and-srg-map-prerequisites.csv` |
| 01 | The FortiAnalyzer feature map | 349 | `01-fortianalyzer-feature-version-and-srg-map-feature-map.csv` |
| 01 | Requirement reference | 65 | `01-fortianalyzer-feature-version-and-srg-map-requirements.csv` |
| 02 | FortiAnalyzer prerequisites | 16 | `02-fortianalyzer-and-cisco-stig-crosswalk-prerequisites.csv` |
| 02 | The crosswalk table | 65 | `02-fortianalyzer-and-cisco-stig-crosswalk-crosswalk.csv` |
| 02 | Cisco SNA requirements with no FortiAnalyzer requirement | 17 | `02-fortianalyzer-and-cisco-stig-crosswalk-unmatched.csv` |

The files moved with the chapters, so the download addresses changed. The
addresses under `data/volume-172-disa-srgs-and-stigs/` that began with `12-`
and `38-` no longer exist.

## Chapters

1. [FortiAnalyzer Feature, Version, and SRG Map](chapters/01-fortianalyzer-feature-version-and-srg-map.md) — 349 FortiAnalyzer features (53 core platform features and every feature in the 7.0 to 8.0 New Features Guides) with the release that introduced each, the Central Log Server or NDM SRG requirement it maps to, and the command that meets it.
2. [FortiAnalyzer and Cisco STIG Crosswalk](chapters/02-fortianalyzer-and-cisco-stig-crosswalk.md) — all 65 FortiAnalyzer requirements from Chapter 01 (60 Central Log Server, 5 NDM) aligned with the Cisco SNA STIG rule and the rules in every other Cisco STIG that implement the same or an equivalent requirement, plus the Cisco rules on the log-source side (5 same requirement, 18 equivalent, 9 log-source counterpart only, 33 with no Cisco counterpart, because no Cisco STIG implements the Central Log Server SRG), with verified SNA settings, corrected SNA fix text, and the 17 SNA rules no FortiAnalyzer requirement covers.
3. [Central Log Server SRG Requirement Labs](chapters/03-central-log-server-srg-requirement-labs.md) — fifteen labs for the 60 Central Log Server requirements: administrator access, logon protections, password policy, certificates, the unit's own audit records, cryptography, time, receiving logs, protecting stored logs, retention and storage, off-loading and backup, alerting, analysis and reporting, and the software release, plus a gap lab for account inactivity and for SHA-2 signatures for SAML on release 7.6.
4. [Network Device Management SRG Requirement Labs](chapters/04-network-device-management-srg-requirement-labs.md) — two labs for the five NDM requirements: SNMPv3, authenticated NTP sources, and authentication servers, then the configuration backup and the unit's own logs to a central log server.
90. [As-Built — How This Volume Was Built](chapters/90-as-built-how-this-volume-was-built.md) — how and when Chapters 01 and 02 were built, from which sources, and what changed after the first build, including the move from Volume CLXXII and the labs of Chapters 03, 04, and 999.
999. [Shared Lab Infrastructure](chapters/999-shared-lab-infrastructure.md) — the lab for this volume's requirement labs: a FortiAnalyzer-VM on release 7.6, a FortiGate-VM log source, a mail server, and an optional second FortiAnalyzer on the lab network of Volume CCI, the host or service behind each of the 30 prerequisites, four build labs, and the `baseline-202` snapshots.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all six chapters.
- [Glossary](GLOSSARY.md) — definitions for terms used in this volume.

## Related volumes

- **Other Fortinet STIG volumes:** [Volume CCI — FortiSwitch STIG and SRG Mapping](../volume-201-fortiswitch-stig-and-srg-mapping/README.md), [Volume CCIII — FortiManager STIG and SRG Mapping](../volume-203-fortimanager-stig-and-srg-mapping/README.md).
- [Volume CLXXII — DISA SRGs and STIGs](../volume-172-disa-srgs-and-stigs/README.md)
  for the framework (Chapters 01 to 09), the Fortinet overview (Chapter 10), the
  other Fortinet product maps, and the Cisco chapters this volume's crosswalk
  uses.
- [Volume CMI — Lab Selector](../volume-901-lab-selector/README.md), whose page plans a lab build for the
  requirement labs of this volume:
  [open it with the FortiAnalyzer lab set ticked](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-901-lab-selector/lab-scripts/selector/lab-selector.html?sets=fortianalyzer).
- [Volume XIX — Fortinet NSE Certification Program](../volume-019-fortinet-network-security/README.md),
  whose security operations chapter covers FortiAnalyzer as a product.

## Lab coverage

Chapters 01, 02, and 90 have **no hands-on labs**, by design: they are
reference chapters that map requirements and record how the volume was built.
Chapter 999 has the labs (999.1 to 999.4) that add the FortiAnalyzer and its
log sources to the lab network of Volume CCI and take the baseline. Chapters
03 and 04 have the requirement labs that run on that lab: 17 labs for the 65
requirements of Chapter 01. The Lab column of Chapters 01 and 02 links each
SRG ID to its lab.

The labs have not been run. Each lab chapter carries a sign-off that stays
pending until a person has run its labs, and the commands come from Chapter
01, which checked them against the FortiAnalyzer 8.0.0 CLI Reference. The
labs are written for release 7.6, and they say where that release differs.

## Software and platform baseline

DISA content is the 2026-10 quarterly release recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md). From that release the
chapters use the Central Log Server SRG V3R5, the Network Device Management
SRG V5R5, and the Cisco STIG packages, including the Cisco SNA STIG V1R1.
Version data in Chapter 01 comes
from the FortiAnalyzer New Features Guides for release trains 7.0, 7.2, 7.4,
7.6, and 8.0, which cover FortiAnalyzer 7.0.0 through 8.0.1. Commands were
checked against the FortiAnalyzer 8.0.0 CLI Reference. The labs of Chapters
03, 04, and 999 are written for a FortiAnalyzer-VM on release 7.6 and for the
lab network of Volume CCI. Confirm the current release of any STIG or SRG on
the DoD Cyber Exchange before assessing against it.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-202-fortianalyzer-stig-and-srg-mapping
```

After changing a table in Chapter 01 or 02, regenerate the CSV downloads
(written to this volume's `data/` folder) and refresh the download links:

```bash
python scripts/python/export_srg_tables.py
```

After adding, renaming, or renumbering a lab, refresh the Lab column of
Chapters 01 and 02, then check the labs:

```bash
python .claude/skills/srg-labs-for/labs.py FortiAnalyzer --lab-column
```

```bash
python .claude/skills/srg-labs-for/labs.py FortiAnalyzer --check --scope map
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
