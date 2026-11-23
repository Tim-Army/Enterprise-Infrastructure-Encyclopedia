# Volume CMI — Lab Selector

**Open the page:** [Lab Selector](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-901-lab-selector/lab-scripts/selector/lab-selector.html) · **Lab scripts:** [all platforms (.zip)](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-901-lab-selector/volume-901-lab-selector-lab-scripts.zip)

> The **Lab Selector** is one page that plans a lab build for the labs you
> choose: SRG labs today, with certification labs and learning labs to follow.
> This volume holds the page, the data it works from, and the scripts that
> build the lab machines on seven platforms. It explains how to use the page
> and how to add the labs of another volume to it.

## Overview

Volume CMI is the **home of the Lab Selector and its data**. The page was the
Lab Builder of [Volume CCI — FortiSwitch STIG and SRG Mapping](../volume-201-fortiswitch-stig-and-srg-mapping/README.md)
until 2026-11-20, and it built for one set of labs. It now offers the labs of
more than one volume, so the page, its data, and the build scripts moved here.
The volume number follows [Volume CM — Tim's Lab Gear](../volume-900-tims-lab-gear/README.md),
outside the block that is reserved for Fortinet STIG work (see
[Structure.md](../../Structure.md)).

On the page you choose three things: the labs to run, the platform the lab
machines run on, and what to build. The page then writes a manifest, the
commands, a checklist, and the lab walkthroughs of that build, and bundles
them in a zip. Everything runs in the browser, and nothing is sent anywhere.

The labs come in **kinds** and **lab sets**:

| Kind of labs | Lab sets today |
| --- | --- |
| SRG labs | FortiSwitch (Volume CCI), FortiAnalyzer (Volume CCII), and FortiManager (Volume CCIII) |
| Certification labs | None yet |
| Learning labs | None yet |

A link can open the page with a lab set already ticked:

| Lab set | Link |
| --- | --- |
| FortiSwitch | [Lab Selector with the FortiSwitch labs ticked](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-901-lab-selector/lab-scripts/selector/lab-selector.html?sets=fortiswitch) |
| FortiAnalyzer | [Lab Selector with the FortiAnalyzer labs ticked](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-901-lab-selector/lab-scripts/selector/lab-selector.html?sets=fortianalyzer) |
| FortiManager | [Lab Selector with the FortiManager labs ticked](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-901-lab-selector/lab-scripts/selector/lab-selector.html?sets=fortimanager) |

Every lab set runs on the **shared lab** of Volume CCI's Chapter 999: a
gateway, VLANs, and service hosts, which the scripts of this volume build. The
lab network is `10.200.0.0/16`. The FortiAnalyzer and FortiManager lab sets
add hosts that no script builds, such as the FortiAnalyzer-VM itself, and the
page lists them with their addresses.

The volume has three chapters:

- **Chapter 01** describes the **Lab Selector**: the kinds of labs and the
  lab sets, the shared lab and what a lab set adds to it, every option of the
  page, the zip and how to hand it to Claude, and how the progress of the labs
  comes back into the page. It has one lab, which plans a build.
- **Chapter 02** describes the **lab data**: the catalog of lab kinds and lab
  sets, the manifest, what the sync script reads from a lab chapter, and how
  to add a lab set or a kind of labs.
- **Chapter 90**, the as-built chapter, records where the page and the scripts
  came from, what moved here and what stayed, the choices behind the lab sets,
  and what was tested.

## The lab-scripts folder

The `lab-scripts` folder of this volume is published as files and as one zip.

| Folder | What it holds |
| --- | --- |
| `selector/` | The Lab Selector page |
| `common/` | The lab catalog, the manifest, the Linux flavor catalog, the switch feature data, the seed tool, and the image resolver |
| `esxi/`, `vcenter/`, `workstation/`, `proxmox/`, `kvm/`, `wsl/` | One build script for each platform. Volume CCI, Chapters 09 to 14 explain them |

The folder has a `README.md` of its own, which is in the zip.

## Chapters

1. [The Lab Selector](chapters/01-the-lab-selector.md) — the page that plans a lab build: the three kinds of labs, the FortiSwitch, FortiAnalyzer, and FortiManager lab sets, the shared lab and the hosts that no script builds, the links that tick lab sets, every option of the page, the zip for Claude, and the progress of the labs, with a lab that plans a build.
2. [Lab Data and How to Add a Lab Set](chapters/02-lab-data-and-how-to-add-a-lab-set.md) — the catalog, the manifest, and the other data files, what the sync script reads from a lab chapter and from a Chapter 999, lab ids and prefixes, what is published where, and the steps to add a lab set or a kind of labs.
90. [As-Built — How This Volume Was Built](chapters/90-as-built-how-this-volume-was-built.md) — where the page and the scripts came from, the move from Volume CCI on 2026-11-20, the choices behind the lab sets, what was tested, and what was not.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all three chapters.
- [Glossary](GLOSSARY.md) — definitions for terms used in this volume.

## Related volumes

- [Volume CCI — FortiSwitch STIG and SRG Mapping](../volume-201-fortiswitch-stig-and-srg-mapping/README.md)
  for the shared lab (Chapter 999), the FortiSwitch requirement labs, and
  the chapters that explain each platform (Chapters 09 to 14).
- [Volume CCII — FortiAnalyzer STIG and SRG Mapping](../volume-202-fortianalyzer-stig-and-srg-mapping/README.md)
  and [Volume CCIII — FortiManager STIG and SRG Mapping](../volume-203-fortimanager-stig-and-srg-mapping/README.md)
  for the labs and the hosts of the other two lab sets.
- [Volume CM — Tim's Lab Gear](../volume-900-tims-lab-gear/README.md) for the
  hardware that the scripts were tested on.

## Lab coverage

Chapter 01 has one lab, which plans a build on the page and downloads its zip.
It builds no machine. Chapters 02 and 90 have **no hands-on labs**, by design:
they describe the data and record how the volume was built. The labs that the
page plans are in Volumes CCI, CCII, and CCIII.

The lab of Chapter 01 has not been run on the published page by a person, and
its sign-off is pending. The self-test of the page checks the same steps on
its own controls.

## Software and platform baseline

The page is plain HTML, CSS, and JavaScript with no library, and it was tested
in one Chromium browser. The build scripts target VMware ESXi 7, 8, and 9,
vCenter 7, 8, and 9, Dell VxRail, VMware Workstation Pro, Proxmox VE 8.1 and
later, KVM with virt-install 4.0 and later, and WSL 2, as
[Volume CCI](../volume-201-fortiswitch-stig-and-srg-mapping/README.md) records.
The lab sets are written for FortiSwitchOS 7.6, FortiAnalyzer 7.6, and
FortiManager 7.6. Other software versions follow
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md).

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-901-lab-selector
```

After changing a data file of the `lab-scripts` folder, the catalog, or a lab
chapter that the catalog names, copy the data into the page:

```bash
python scripts/python/sync_lab_selector.py
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
