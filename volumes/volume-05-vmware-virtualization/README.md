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
| Lab | Nested ESXi, VMware Workstation, or a VMUG Advantage subscription | The administrator and support exams reward console familiarity that reading does not build |
| Community | VMware Certification community and VMUG | Where blueprint revisions and exam-version changes surface first |

A note on lab access. Broadcom's licensing changes have made evaluation
licenses harder to obtain than they once were. VMUG Advantage remains the
most reliable route to a legitimate home lab for these exams, and it is
worth budgeting for alongside the $250 exam fee.

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
