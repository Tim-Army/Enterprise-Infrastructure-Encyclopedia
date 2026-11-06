# Volume CCI — FortiSwitch STIG and SRG Mapping

**Download this volume:** [Word (.docx)](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-201-fortiswitch-stig-and-srg-mapping/volume-201-fortiswitch-stig-and-srg-mapping.docx) · [PDF](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-201-fortiswitch-stig-and-srg-mapping/volume-201-fortiswitch-stig-and-srg-mapping.pdf) · **Lab scripts:** [all five platforms (.zip)](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-201-fortiswitch-stig-and-srg-mapping/volume-201-fortiswitch-stig-and-srg-mapping-lab-scripts.zip)

> A requirement-by-requirement map of **Fortinet FortiSwitch** to the DISA
> Security Requirements Guides (SRGs) that apply to it, and two crosswalks that
> align the Cisco switch STIGs with FortiSwitch settings. DISA publishes no
> FortiSwitch STIG, so a FortiSwitch in a DoD environment is assessed against
> the SRGs for its functions. This volume shows which FortiSwitchOS release
> lists each feature, which SRG requirement it helps meet, and the command that
> configures it. It also carries the SRG mapping workbook behind those chapters,
> with a searchable table and CSV downloads.

## Overview

Volume CCI is the **FortiSwitch volume of the Fortinet STIG work**. Volume
numbers 200 to 299 are reserved for that work (see
[Structure.md](../../Structure.md)). The vendor-neutral material it builds on,
the framework, the SRG catalog, the Fortinet overview, and the Cisco switch
map, stays in [Volume CLXXII — DISA SRGs and STIGs](../volume-172-disa-srgs-and-stigs/README.md).
The three content chapters here were Chapters 11, 33, and 37 of that volume and
moved on 2026-11-04. Volume CLXXII keeps a short pointer page at each old
chapter number, so earlier links still work.

The volume has fifteen chapters:

- **Chapter 01** is the **FortiSwitch feature, version, and SRG map**: all 235
  FortiSwitchOS 8.0.0 features, the release that first lists each one, the
  Layer 2 Switch, Network Device Management, Router, or AAA Services SRG
  requirement it maps to, and the command that meets the requirement, with a
  prerequisites table and a Reference and Page column that points to the
  FortiSwitchOS 7.6.7 documentation.
- **Chapter 02** is the **FortiSwitch and Cisco Catalyst Switch STIG
  crosswalk**: all 152 rules of the Cisco IOS XE Switch STIGs aligned, through
  the SRG requirement each implements, with the FortiSwitch setting and command
  that meets it, so the Cisco rules can serve as a FortiSwitch checklist.
- **Chapter 03** is the **Cisco NX-OS Switch and FortiSwitch STIG crosswalk**:
  all 142 Cisco NX-OS Switch STIG rules aligned the same way, reusing Chapter
  02's FortiSwitch side where the requirements match.
- **Chapters 04 to 07** are the **requirement labs**, one chapter per SRG
  family, covering all 185 distinct requirements in the crosswalk. Chapter 04
  covers the Layer 2 Switch SRG (33 requirements), Chapter 05 the Network Device
  Management SRG (53), Chapter 06 the Router SRG (92), and Chapter 07 the AAA
  Services SRG (7). A requirement FortiSwitch can meet gets a lab with a positive
  and a negative test. A requirement it cannot meet gets a gap lab that proves
  the setting is absent, applies the nearest compensating control, and records
  the disposition. Every lab runs on the network from Chapter 999.
- **Chapter 08** is the **OpenGear IM7216-2-DAC-LMV console server (firmware 5.5.3)** and an **optional console lab**: what the device can do, how it joins the Chapter 999 network on segment 0 at `.13` with one new segment (100) for break-glass access, and seven labs for serial access to both switches, RADIUS logins, logging, hardening, break-glass and cellular access, and recovery from a lost management path. A second diagram shows the console paths.
- **Chapters 09 to 13** automate the creation of the Chapter 999 virtual machines, one chapter for each place they can run: **VMware ESXi 7, 8, and 9** (Chapter 09), **VMware vCenter 7, 8, and 9** (Chapter 10), **VMware Workstation Pro for Windows** (Chapter 11), **Proxmox VE** (Chapter 12), and **WSL** (Chapter 13, the service hosts only). All five read one manifest of twelve machines and one cloud-init seed tool, so a machine has the same name, addresses, and packages on every platform. A [Lab Builder page](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-201-fortiswitch-stig-and-srg-mapping/lab-scripts/builder/lab-builder.html) turns your choices (platform, version, machine names and sizes, address block) into a manifest, the commands to run, and a checklist. The scripts are [downloadable as one zip](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-201-fortiswitch-stig-and-srg-mapping/volume-201-fortiswitch-stig-and-srg-mapping-lab-scripts.zip) and none has been run against a real host yet.
- **Chapter 90**, the as-built chapter, records how Chapters 01 to 03 and the
  workbook were built, when, and from which sources, and what changed after the
  first build.
- **Chapter 999**, the **shared lab infrastructure**, defines the lab that
  every requirement lab in this volume runs in: the address plan (`10.201.0.0/16`
  for IPv4 and `fd00:db8:201::/112` for IPv6), the hosts and services that
  satisfy the workbook's prerequisites P1 to P17, and the baseline of the two
  switches under test. It is numbered 999 so that it stays last.

The Cisco side of the crosswalks lives in Volume CLXXII: the
[Cisco overview](../volume-172-disa-srgs-and-stigs/chapters/31-cisco-products-stigs-and-srg-mapping.md)
and the
[Cisco Catalyst switch map](../volume-172-disa-srgs-and-stigs/chapters/32-cisco-catalyst-switch-feature-version-and-stig-map.md).

## The SRG mapping workbook

The `data/` folder holds the workbook
`01-fortiswitch-feature-version-and-srg-map-feature-map-20261103.xlsx`, a
working copy of the FortiSwitch SRG mapping. Its main sheets are the original
Milestone-1 sheet, the FortiSwitch-versus-Cisco crosswalk (438 rows), the
prerequisites list (17 entries), the references, and a FortiSwitchOS 7.6.7
model-support sheet (235 features, for the FS-648F-FPOE and FS-2048F). Each
crosswalk row records the SRG ID, severity, the Cisco and FortiSwitch settings,
the command, the documentation reference and page, and who verified the
command in the CLI or the GUI.

Three CSV files carry the crosswalk, prerequisites, and model-support sheets.
`scripts/python/export_srg_workbook.py` writes them, and also writes a
self-contained interactive page with search, filters, sorting, and CSV
download. On the published portal the page is at `interactive/fortiswitch-srg-crosswalk.html`.

Two cautions apply to the workbook. A row marked with an "x" in the
documentation column was found in the documentation but still needs
verification in the CLI or the GUI; a row counts as verified only when a CLI or
GUI verifier is recorded. The SRG IDs and SRG versions were compared with a
third-party mirror (Cyber Trackr) and still need confirmation against DISA's
own files.

## Chapters

1. [FortiSwitch Feature, Version, and SRG Map](chapters/01-fortiswitch-feature-version-and-srg-map.md) — all 235 FortiSwitchOS 8.0.0 features with the releases that list them, the Layer 2 Switch, NDM, Router, or AAA Services SRG requirement each maps to, and the command that meets it.
2. [FortiSwitch and Cisco Catalyst Switch STIG Crosswalk](chapters/02-fortiswitch-and-cisco-catalyst-switch-stig-crosswalk.md) — all 152 Cisco IOS XE Switch STIG rules aligned, through the SRG requirement each implements, with the FortiSwitch setting and verified FortiSwitchOS 8.0.0 command that meets it (31 same requirement, 55 equivalent setting, 16 partial, 28 not supported, 20 not applicable, 2 by procedure), plus the 26 FortiSwitch SRG requirements no Cisco rule covers.
3. [Cisco NX-OS Switch and FortiSwitch STIG Crosswalk](chapters/03-cisco-nx-os-switch-and-fortiswitch-stig-crosswalk.md) — all 142 Cisco NX-OS Switch STIG rules (NDM, L2S, RTR) aligned through their SRG IDs with a corrected, script-verified Nexus 9000 NX-OS 10.5(x) command and the FortiSwitch setting and FortiSwitchOS 8.0.0 command that meet the same requirement (30 same requirement, 57 equivalent setting, 17 partial, 19 not supported, 17 not applicable, 2 by procedure; 120 rows reuse Chapter 02's FortiSwitch side), with vPC, VXLAN EVPN, and CoPP notes and the 25 FortiSwitch SRG requirements no NX-OS rule covers.
4. [Layer 2 Switch SRG Requirement Labs](chapters/04-layer-2-switch-srg-requirement-labs.md) — nine labs for the 33 Layer 2 Switch requirements: 802.1X and MAB, managed-mode NAC, spanning tree guards, flood control, DHCP snooping, DAI and IP source guard, VLAN hygiene, fail-secure and resilience, session capture with port mirroring, and a gap lab for VTP and UDLD.
5. [Network Device Management SRG Requirement Labs](chapters/05-network-device-management-srg-requirement-labs.md) — twelve labs for the 53 Network Device Management requirements: administrator access control, logon protections, password policy, audit events, audit content and time, storage and off-load, FIPS and SNMPv3, authentication servers and certificates, backup and firmware integrity, audit of privileged functions and session times, replay-resistant access, and denial-of-service safeguards.
6. [Router SRG Requirement Labs](chapters/06-router-srg-requirement-labs.md) — ten requirement labs for the 46 Router requirements FortiSwitch can meet (interface hygiene, ACL flow control, perimeter filtering, control plane, routing authentication, BGP protection, VRFs, multicast, hashed keys with lifetimes, call-home and fragmented ICMP) and six gap labs for the 46 it cannot (MPLS, provider edge, rendezvous point, MSDP, IPv6 extension headers, Cisco-specific behaviors).
7. [AAA Services SRG Requirement Labs](chapters/07-aaa-services-srg-requirement-labs.md) — four labs for the 7 AAA Services requirements: RadSec (RADIUS over TLS) with certificate validation, 802.1X with a secure EAP type, RADIUS accounting, and a unique shared secret per client.
8. [OpenGear IM7216-2-DAC-LMV Console Server (Firmware 5.5.3) and Optional Console Lab](chapters/08-opengear-im7216-console-server-and-optional-console-lab.md) — what the console server can do, how it joins the Chapter 999 network on segment 0 at `.13` plus one new break-glass segment (100), a console-access diagram, and seven labs: serial access to both switches, RADIUS logins, logging and SNMPv3, hardening, break-glass and cellular access, and recovery from a lost management path.
9. [Automating the Lab Virtual Machines on VMware ESXi 7, 8, and 9](chapters/09-esxi-7-8-and-9-lab-virtual-machine-automation.md) — the twelve lab machines, the shared manifest and cloud-init seeds, virtual switches and trunk port groups, and a PowerCLI script that builds them on a standalone ESXi 7 or 8 host.
10. [Automating the Lab Virtual Machines Through VMware vCenter 7, 8, and 9](chapters/10-vcenter-7-8-and-9-lab-virtual-machine-automation.md) — the same build through vCenter: a template and clones, a VM folder, standard or distributed switches, and the distributed switch and hardware versions for vSphere 7 and 8.
11. [Automating the Lab Virtual Machines in VMware Workstation Pro for Windows](chapters/11-vmware-workstation-pro-lab-virtual-machine-automation.md) — custom vmnets, guest-side VLAN tagging, and a script that drives `ovftool`, `vmrun`, and the `.vmx` files.
12. [Automating the Lab Virtual Machines on Proxmox VE](chapters/12-proxmox-ve-lab-virtual-machine-automation.md) — VLAN-aware bridges, cloud-init snippets, and a `qm` script that creates and starts the machines.
13. [Automating the Lab Service Hosts in WSL](chapters/13-wsl-lab-host-automation.md) — what WSL can and cannot build for this lab: eight service hosts as distributions that share one kernel and network namespace.
90. [As-Built — How This Volume Was Built](chapters/90-as-built-how-this-volume-was-built.md) — how and when Chapters 01 to 03 and the SRG mapping workbook were built, from which sources, and what changed after the first build, including the move from Volume CLXXII.
999. [Shared Lab Infrastructure](chapters/999-shared-lab-infrastructure.md) — the lab network for this volume's requirement labs: the `10.201.0.0/16` and `fd00:db8:201::/112` address plans split into segments, the routed links and routing peers, the service hosts behind prerequisites P1 to P17, and six labs that build and baseline the gateway, services, and both switches.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all fifteen chapters.
- [Glossary](GLOSSARY.md) — definitions for terms used in this volume.

## Related volumes

- [Volume CLXXII — DISA SRGs and STIGs](../volume-172-disa-srgs-and-stigs/README.md)
  for the framework (Chapters 01 to 09), the Fortinet overview (Chapter 10), the
  other Fortinet product maps, and the Cisco chapters this volume's crosswalks
  use.
- [Volume CLXXIV — NSE 5 FortiSwitch Lab](../volume-174-nse-5-fortiswitch-lab/README.md),
  whose hardening lab reuses commands from Chapters 01 to 03.
- [Volume XIX — Fortinet NSE Certification Program](../volume-019-fortinet-network-security/README.md).

## Lab coverage

Chapters 01 to 03 and 90 have **no hands-on labs**, by design: they are
reference chapters that map requirements and record how the volume was built.
Chapter 999 has the labs (999.1 to 999.6) that build the shared lab network and
baseline both switches. Chapters 04 to 07 have the requirement labs that run on
that network, one chapter per SRG family. Chapter 08 has the optional console server labs (8.1 to 8.7). Chapters 09 to 13 each have a build lab for one platform, with the scripts in the `lab-scripts` folder. For a
FortiLink-managed FortiSwitch lab built around an exam blueprint, see Volume
CLXXIV.

## Software and platform baseline

DISA content is the 2026-10 quarterly release recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md). Version data in Chapters
01 to 03 comes from the FortiSwitchOS feature matrices for 7.0.0 through
8.0.0; the documentation references and the workbook use FortiSwitchOS 7.6.7.
Confirm the current release of any STIG or SRG on the DoD Cyber Exchange
before assessing against it.

The lab automation in Chapters 09 to 13 targets VMware ESXi and vCenter 7.0 and
8.0 (the versions that volume was asked to cover, not the vSphere 9.x baseline
above), Workstation Pro 17 and 25H2, Proxmox VE 8.1 and later, WSL 2, and the
Ubuntu Server 24.04 LTS cloud image. Change `image` in
`lab-scripts/common/lab201-vms.json` to use another Ubuntu release.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-201-fortiswitch-stig-and-srg-mapping
```

After changing a table in Chapters 01 to 03, regenerate the CSV downloads
(written to this volume's `data/` folder) and refresh the download links:

```bash
python scripts/python/export_srg_tables.py
```

After changing the workbook, regenerate the workbook CSV files and the
interactive page:

```bash
python scripts/python/export_srg_workbook.py
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
