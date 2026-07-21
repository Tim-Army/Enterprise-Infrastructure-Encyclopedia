# Volume V — VMware Virtualization

> ESXi and vCenter Server architecture, virtual networking, storage and
> vSAN, availability and mobility, VMware NSX network virtualization and
> security, lifecycle automation and observability, and VMware Certified
> Professional (VCP) exam preparation across the current VMware Cloud
> Foundation and vSphere Foundation certification paths.

## Overview

Volume V covers VMware's enterprise virtualization platform end to end:
the architecture and design principles behind ESXi and vCenter Server,
hands-on host and cluster administration, vSphere's storage and networking
stacks, availability and mobility services, security architecture, and the
lifecycle automation and observability practices that keep a fleet current
and diagnosable in production. The second half of the volume installs and
configures VMware NSX for network virtualization and micro-segmentation,
then organizes the whole volume as study and review material for the five
VMware Certified Professional (VCP) exams that map to this content under
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md).

The volume is organized in four parts:

- **Chapters 01–04** establish the architectural foundation and core
  administration skills: virtualization theory and vSphere product
  architecture, ESXi installation and host operations, vCenter Server
  deployment and identity, and vSphere virtual networking.
- **Chapters 05–09** cover VM lifecycle and resource management, storage
  and vSAN, availability and mobility (HA, vMotion, DRS, Fault Tolerance),
  vSphere and NSX security architecture, and fleet-scale lifecycle
  automation, observability, and troubleshooting.
- **Chapters 10–11** install and configure VMware NSX: the management/
  control/data plane architecture, transport fabric, and the logical
  networking and security objects (segments, gateways, routing, NAT,
  Distributed Firewall) built on top of it.
- **Chapters 12–16** are exam-preparation chapters mapping this volume's
  content to the current VCP-NV, VCP-VCF Support, VCP-VCF Administrator,
  VCP-VVF Administrator, and VCP-VVF Support certification blueprints,
  organized as self-assessment study material rather than reproductions
  of proprietary exam content.

Every chapter follows the same structure — learning objectives, theory
and architecture, design considerations, implementation and automation,
validation and troubleshooting, security and best practices, references
and knowledge checks, a hands-on lab, and a summary and completion
checklist — defined in [templates/chapter.md](../../templates/chapter.md)
and enforced by [EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md).
Each hands-on lab is a reproducible, disposable exercise with a stated
objective, prerequisites, numbered steps, expected results, a negative
test, and cleanup instructions.

## Chapters

1. [VMware Virtualization Architecture and Design](chapters/01-vmware-virtualization-architecture-and-design.md) — x86 virtualization fundamentals, ESXi internal architecture, the vSphere inventory hierarchy, and VMware Cloud Foundation/vSphere Foundation product packaging.
2. [ESXi Installation, Configuration, and Host Operations](chapters/02-esxi-installation-configuration-and-host-operations.md) — interactive, scripted, and PXE/UEFI HTTP boot installation methods, the boot bank/ESX-OSData architecture, image profiles and acceptance levels, and Host Profiles.
3. [vCenter Server Deployment, Identity, and Recovery](chapters/03-vcenter-server-deployment-identity-and-recovery.md) — the VCSA appliance architecture, SSO domain and identity federation, vCenter High Availability, and file-based backup and restore.
4. [vSphere Virtual Networking](chapters/04-vsphere-virtual-networking.md) — standard versus distributed vSwitches, VLAN tagging modes, NIC teaming and LACP, Network I/O Control, private VLANs, and custom TCP/IP stacks.
5. [Virtual Machine Lifecycle and Resource Management](chapters/05-virtual-machine-lifecycle-and-resource-management.md) — VM hardware versions, templates and Content Library, shares/reservations/limits, DRS, memory management, NUMA, and snapshot architecture.
6. [vSphere Storage and vSAN](chapters/06-vsphere-storage-and-vsan.md) — VMFS6/NFS/iSCSI/FC/NVMe-oF datastore transports, PSA/NMP/SATP/PSP multipathing, VASA/SPBM/vVols, and vSAN OSA/ESA architecture and storage policies.
7. [vSphere Availability, Mobility, and Cluster Services](chapters/07-vsphere-availability-mobility-and-cluster-services.md) — vSphere HA architecture, vMotion, Fault Tolerance, DRS, vSphere Cluster Services (vCLS), and stretched-cluster/multi-site availability patterns.
8. [vSphere and NSX Security Architecture](chapters/08-vsphere-and-nsx-security-architecture.md) — ESXi Lockdown Mode, Secure Boot and vTPM, key management, RBAC hardening, and the NSX Distributed Firewall and Gateway Firewall.
9. [vSphere Lifecycle, Automation, Observability, and Troubleshooting](chapters/09-vsphere-lifecycle-automation-observability-and-troubleshooting.md) — vSphere Lifecycle Manager images versus baselines, Auto Deploy, automation tooling (PowerCLI, Terraform, Ansible), the event/task/alarm model, and log architecture and support bundles.
10. [Installing VMware NSX](chapters/10-installing-vmware-nsx.md) — NSX management/control/data plane architecture, NSX Manager cluster deployment, transport zones, uplink profiles and TEP pools, host preparation, and Edge node/Edge cluster deployment.
11. [Configuring VMware NSX](chapters/11-configuring-vmware-nsx.md) — segments, Tier-0/Tier-1 gateways, BGP routing, NAT, DHCP services, full Distributed Firewall rule construction, Traceflow, and NSX Federation.
12. [VCP Network Virtualization 2V0-41.24 Exam Preparation](chapters/12-vcp-network-virtualization-2v0-41-24-exam-preparation.md) — blueprint-mapped study and review material for the VCP-NV certification, built on Chapters 8, 10, and 11.
13. [VCP VMware Cloud Foundation Support 2V0-15.25 Exam Preparation](chapters/13-vcp-vmware-cloud-foundation-support-2v0-15-25-exam-preparation.md) — support-role troubleshooting study material covering SDDC Manager, fleet management, Identity Broker, and VCF Operations.
14. [VCP VMware Cloud Foundation Administrator 2V0-17.25 Exam Preparation](chapters/14-vcp-vmware-cloud-foundation-administrator-2v0-17-25-exam-preparation.md) — administrator-role study material covering workload domain deployment, Cloud Builder versus SDDC Manager scope, fleet RBAC, licensing, and certificate lifecycle.
15. [VCP VMware vSphere Foundation Administrator 2V0-16.25 Exam Preparation](chapters/15-vcp-vmware-vsphere-foundation-administrator-2v0-16-25-exam-preparation.md) — administrator-role study material mapped directly to Chapters 1–9's standalone vSphere/vSAN content.
16. [VCP VMware vSphere Foundation Support 2V0-18.25 Exam Preparation](chapters/16-vcp-vmware-vsphere-foundation-support-2v0-18-25-exam-preparation.md) — support-role troubleshooting study material scoped to VVF's compute, storage, networking, and licensing failure domains.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all sixteen
  chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.

## Certification alignment

This volume is mapped to the current VMware Certified Professional
certification paths listed in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md): VCP-NV
(2V0-41.24), VCP-VCF Support (2V0-15.25), VCP-VCF Administrator
(2V0-17.25), VCP-VVF Administrator (2V0-16.25), and VCP-VVF Support
(2V0-18.25). Chapters 12 through 16 organize this volume's content against
each blueprint's publicly published domain structure as self-assessment
study material; they do not reproduce proprietary exam questions or
licensed courseware. Always confirm current blueprint domains, exam
length, and registration requirements against Broadcom's official exam
guides before scheduling, since blueprints are revised independently of
this repository's release cycle.

### The exams

All five are proctored, scored on a scaled 100–500 range with 300 to
pass, and priced at $250 US.

| Exam | Certification | Targets | Duration | Questions |
| --- | --- | --- | --- | --- |
| 2V0-16.25 | VCP-VVF Administrator | vSphere Foundation 9.0 | 135 min | 60 |
| 2V0-18.25 | VCP-VVF Support | vSphere Foundation 9.0 | 135 min | 60 |
| 2V0-17.25 | VCP-VCF Administrator | Cloud Foundation 9.0 | 135 min | 60 |
| 2V0-15.25 | VCP-VCF Support | Cloud Foundation 9.0 | 135 min | 60 |
| 2V0-41.24 | VCP-NV | NSX 4.x | 135 min | 70 |

The four 2025-generation exams use multiple choice and multiple-selection
multiple choice only. **VCP-NV is the outlier**: a 2024-generation exam
with 70 questions and a much wider format range — drag and drop, point and
click, hot-area, and matching alongside multiple choice. Prepare for the
interaction styles, not only the content.

Language availability differs too: 2V0-18.25 and 2V0-41.24 are English
only, while the other three are offered in English and Japanese.

### The five standardized blueprint sections

Broadcom standardized VMware exam blueprints into five sections, and its
exam guides state plainly that some **may not appear** in a given exam
where that exam has no testable objectives for them:

1. IT Architectures, Technologies, Standards
2. VMware Solution
3. Plan and Design the VMware Solution
4. Install, Configure, Administrate the VMware Solution
5. Troubleshoot and Optimize the VMware Solution

Chapters 12–16 map this volume against each exam's section structure.

### What Broadcom does not publish

**Percentage weights.** The exam guides list sections and their testable
objectives but assign no weighting to them. That is a real difference
from AWS, Cisco, and Palo Alto Networks, and it has a practical
consequence: you cannot allocate study time by exam emphasis, because the
emphasis is not stated. Sequence by dependency and by your own weakest
objectives instead — which is what the study trackers in Chapters 12–16
are built to surface.

Exam guides do state a **minimally qualified candidate** profile, which is
the closest thing to a difficulty signal. VCP-NV's, for example, expects
roughly six months with NSX and two years in IT.

### Study materials

| Role | Resource | Why |
| --- | --- | --- |
| Official blueprint | The exam guide for your exam number | Authority on sections and testable objectives; download it before planning anything |
| Official training | The recommended course named on each exam page | VVF Administrator points at *vSphere Foundation: Build, Manage and Operate*; both Support exams at *VMware Cloud Foundation: Troubleshooting*; VCF Administrator at *Build, Manage, and Secure* plus *Automate and Operate* |
| Reference | Broadcom Tech Docs | Product documentation for vSphere, vSAN, NSX, and VCF Operations |
| Practice exams | Third-party banks | Useful for pacing against 135 minutes; verify the bank targets your exam number, since the 9.0-generation codes are recent |
| Lab | VMware Hands-on Labs, or nested ESXi under Workstation/Fusion | The administrator and support exams reward console familiarity that reading does not build; see the licensing note below before planning a home lab |
| Community | VMware Certification community and VMUG | Where blueprint revisions and exam-version changes surface first |

**Lab licensing is now a chicken-and-egg problem, and it is worth
planning around.** The EvalExperience program that once bundled 365-day
evaluation licenses with a VMUG Advantage subscription ended in 2024.
VMUG Advantage membership alone no longer entitles you to download the
software. Personal-use licenses are now unlocked by *passing a VCP exam*
— VCP-VCF, for instance, releases three-year VMware Cloud Foundation
licenses at 128 cores, along with vDefend Firewall and Avi Load Balancer
entitlements.

Read that ordering carefully: **VMUG Advantage is a reward for
certifying, not a route to preparing for it.** Budgeting for it as study
tooling, as was reasonable a few years ago, no longer works.

For preparation before you hold a certification, the practical options
are VMware Hands-on Labs — free, browser-based, and requiring no
licensing at all — nested ESXi under VMware Workstation or Fusion, which
are free for personal use, and whatever evaluation period the product
currently offers at the time you download it. Confirm the current terms
rather than assuming, since this is the part of the VMware landscape that
has changed most since the Broadcom acquisition.

### Mapping this volume to VMware Hands-on Labs

[Hands-on Labs](https://labs.hol.vmware.com/HOL/catalog) are the closest
substitute for a licensed home lab: a running environment in the browser,
no download, no entitlement.

**Sign in.** The catalog can be browsed anonymously, but the public view
shows roughly a fifth of what is there — around 99 labs are available to
a signed-in account against about twenty visible without one. Several of
the labs below, and the whole Odyssey category, appear only after signing
in. Registration is free.

| Chapters | Topic | Hands-on Lab |
| --- | --- | --- |
| 01 | Virtualization fundamentals | `HOL-2535-01-VCF-L` Virtualization 101 |
| 01–02 | vSphere platform and what's new | `HOL-2630-01-VCF-L` What's New with vSphere in VCF 9.0 |
| 02–05 | Host and VM administration depth | `HOL-2637-02-VCF-L` vSphere in VCF 9.0 — Advanced Topics |
| 02, 09 | Host configuration at fleet scale | `HOL-2538-01-VCF-L` vSphere Configuration Profiles |
| 05, 07 | Performance and resource contention | `HOL-2637-07-VCF-L` Introduction to vSphere Performance |
| 05, 07 | Host subsystem performance testing | `HOL-2637-09-VCF-L` vSphere Performance Testing of ESXi Host Subsystems |
| 06 | Storage, vSAN, SPBM, stretched clusters | `HOL-2634-01-VCF-L` vSAN — Getting Started and Advanced Topics |
| 06, 07 | Replication and recovery | `HOL-2634-02-VCF-S` Enhanced vSphere Replication |
| 08 | Platform security | `HOL-2530-03-VCF-L` vSphere Security — Getting Started |
| 08, 11 | Distributed Firewall and micro-segmentation | `HOL-2670-01-ANS-L` vDefend Distributed Firewall Getting Started |
| 08 | Advanced threat protection | `HOL-2670-04-ANS-L` vDefend Firewall with Advanced Threat Protection |
| 09 | Automation with PowerCLI | `HOL-2637-05-VCF-L` vSphere Automation — PowerCLI |
| 09 | API and SDK automation | `HOL-2530-05-VCF-L` vSphere Automation and Development — API and SDK |
| 09, 13, 16 | Operations, logs, metrics, troubleshooting | `HOL-2601-04-VCF-L` Troubleshooting the Private Cloud with VCF Operations |
| 09, 13 | Log and flow analysis | `HOL-2601-06-VCF-L` VCF 9.0 Operations — Analyzing Logs, Metrics, and Network Flows |
| 10–11 | NSX logical networking and VPCs | `HOL-2640-01-VCF-L` Simplified Application Networking with NSX VPC |
| 10–11 | NSX resilience | `HOL-2640-02-VCF-L` Building Resilient Networks with NSX |
| 11 | Multi-tenant NSX | `HOL-2640-03-VCF-L` Multi-Tenant Networking with NSX |
| 08, 11 | Gateway firewall and rule analysis | `HOL-2670-03-ANS-L` Advanced Security with vDefend Firewall |
| 03 | Identity and single sign-on | `HOL-2610-50-VCF-S` VCF 9 Single Sign-On Configuration |
| 13–14 | VCF platform and operations | `HOL-2610-01-VCF-L` What's New in VCF 9.0 — Platform |
| 14 | VCF automation | `HOL-2610-02-VCF-L` What's New in VCF 9.0 — Automation |
| 13–14, 16 | Day-2 operations, lifecycle, certificates | `HOL-2608-01-VCF-L` VCF — Maintaining Your Private Cloud |
| 13–14 | VCF advanced operations tooling | `HOL-2608-03-VCF-L` VCF Advanced Operations and Tools |
| 13 | Upgrade and migration paths | `HOL-2603-01-VCF-S` VCF 9.0 — Upgrading from vSphere 8 |

### Odyssey: the unguided half

Standard Hands-on Labs are guided — they teach a workflow but do not make
you derive it, which is precisely what the Support-track exams test. The
**Odyssey** labs are the answer to that: timed, scored skill challenges
that set an objective and leave you to reach it.

| Level | Lab |
| --- | --- |
| Introductory | `HOL-2530-81-ODY` vSphere Learning the Basics |
| Intermediate | `HOL-2530-82-ODY` Building Your vSphere Skills |
| Advanced | `HOL-2530-83-ODY` Mastering vSphere |

A second set — `HOL-2530-84-ODY` through `-86-ODY` — repeats the three
levels with different scenarios, which matters because the value is in
working an unfamiliar problem rather than repeating a remembered one.

Use the guided labs to see a feature work, then Odyssey to prove you can
do it cold. That pairing is a closer analogue to the exams than either
half alone, and it is free.

**One real gap remains.** No lab walks through deploying NSX from
scratch — Manager cluster, transport zones, uplink profiles, Edge nodes —
which is exactly what [Chapter 10](chapters/10-installing-vmware-nsx.md)
covers. The NSX labs above start from a working fabric. For that build,
Chapters 10–11 and VCP-NV preparation still need a nested lab or the
instructor-led course below.

Note also that labs cycle through maintenance windows; a lab listed here
may show as unavailable temporarily rather than having been withdrawn.

For the NSX build specifically, the depth exists on **Learning@Broadcom**
rather than in Hands-on Labs. The three courses named on the VCP-NV exam
page —
*VMware NSX: Install, Configure, Manage [V4.0]*, *VMware NSX:
Troubleshooting and Operations [V4.x]*, and *VMware NSX: Design [V4.x]* —
run 40 hours each and are the install-and-configure coverage the free
labs lack. The platform also hosts the official exam guides as
downloadable material, including 2V0-41.24's. Access depends on your
organization's entitlement, which is worth checking before assuming a
paid course is the only route.

Note also that NSX continues past VCP. The same catalog carries exam
guides for **3V0-42.23** (NSX 4.x Advanced Design) and **3V0-41.22**
(Advanced Deploy NSX-T 3.x) at the VCAP level, which is where Chapters
10–11's design material points if you continue beyond VCP-NV.

Lab IDs rotate as the catalog is refreshed — the `HOL-25xx`, `HOL-26xx`,
and `HOL-27xx` prefixes above reflect different catalog generations that
were all live when this was written. Search the catalog by title if an
identifier no longer resolves.

### Official courses by exam

Where Hands-on Labs give a guided hour, the instructor-led courses on
Learning@Broadcom are the depth behind each exam. These are the courses
Broadcom names on the certification pages themselves, all 40 hours unless
noted:

| Exam | Official course |
| --- | --- |
| 2V0-16.25 VCP-VVF Administrator | VMware vSphere Foundation: Build, Manage and Operate [V9.0] |
| 2V0-17.25 VCP-VCF Administrator | VMware Cloud Foundation: Build, Manage and Secure [V9.0] **and** VMware Cloud Foundation: Automate and Operate [V9.0] |
| 2V0-15.25 VCP-VCF Support | VMware Cloud Foundation: Troubleshooting [V9.0] |
| 2V0-18.25 VCP-VVF Support | VMware Cloud Foundation: Troubleshooting [V9.0] |
| 2V0-41.24 VCP-NV | VMware NSX: Install, Configure, Manage [V4.0]; Troubleshooting and Operations [V4.x]; Design [V4.x] |

Two observations that matter when planning.

**The two Support exams share one course.** *VMware Cloud Foundation:
Troubleshooting [V9.0]* serves both 2V0-15.25 and 2V0-18.25, which makes
taking them close together considerably more efficient than treating them
as separate tracks.

**Course versions do not always match exam versions.** The VCF and VVF
exams target 9.0 and have matching V9.0 courses, and a V9.1 edition of
*Build, Manage and Secure* already exists. NSX is the outlier: VCP-NV
tests NSX 4.x against V4.0 and V4.x courses, consistent with it being the
older-generation exam. Where a course version leads the exam, the extra
material is not wasted, but the blueprint remains the authority on what
is testable.

Beyond the VCP path, the catalog also carries *VMware Cloud Foundation:
Solution Architecture and Design [V9.0]* for the architect track, and
supporting courses worth knowing about if a specific area is weak —
*VMware vSAN: Install, Configure, Manage [V8]* (32 hours) and *vSAN:
Troubleshooting [V8]* (16 hours) for Chapter 06, *vSphere: Troubleshooting
[V8]* for Chapters 07 and 09, and *VMware Data Center Virtualization: Core
Technical Skills* (32 hours) as an on-ramp for readers new to the
platform.

## Software and platform baseline

Chapters in this volume reference the dated baseline recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md): VMware vSphere / ESXi /
vCenter Server 9.x and VMware NSX 4.x, both dated 2026-07. Update that
file, not individual chapters, when the baseline changes.

## Building and validating this volume

From the repository root, after completing
[SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-05-vmware-virtualization

# Build a single chapter.
scripts/bash/build-book.sh --format all \
  --chapter volumes/volume-05-vmware-virtualization/chapters/06-vsphere-storage-and-vsan.md
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
