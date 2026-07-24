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

The volume is organized in five parts:

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
- **Chapters 17–20** extend that coverage across the rest of the
  Broadcom certification program: the remaining professional-tier exams
  (VCP-DCV, VCP-VCF Architect, VCP-AVI, VCP-PCS), the advanced VCAP tier
  (the eight-exam VCF 9.0 role series plus VCAP-DCV Design and VCAP-NV
  Deploy), the Distinguished Expert (VCDX) design-defense discipline, and
  the Telco Cloud specialist exams — closing with a recurring
  currency-check discipline for keeping the whole program map accurate.

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
17. [Completing the VCP Tier — Data Center Virtualization, VCF Architect, Avi, and Private Cloud Security](chapters/17-completing-the-vcp-tier-dcv-vcf-architect-avi-and-private-cloud-security.md) — the four remaining professional-tier exams: VCP-DCV (2V0-21.23), VCP-VCF Architect (2V0-13.25), and the 6V0 specialist VCPs VCP-AVI (6V0-22.25) and VCP-PCS (6V0-21.25).
18. [The VCAP Advanced Professional Tier — VCF 9.0 Role Exams, DCV Design, and NV Deploy](chapters/18-the-vcap-advanced-professional-tier-vcf-9-0-role-exams-dcv-design-and-nv-deploy.md) — the advanced tier: the eight-exam VCF 9.0 role series (3V0-11.26 through 3V0-25.25) plus VCAP-DCV Design (3V0-21.23) and VCAP-NV Deploy (3V0-41.22), prepared by format (Design vs Deploy).
19. [VCDX — The Distinguished Expert Design-Defense Discipline](chapters/19-vcdx-the-distinguished-expert-design-defense-discipline.md) — the apex credential as a peer-juried design defense rather than a written exam: authoring, submitting, and defending a production-grade design with full requirement/constraint/assumption/risk traceability.
20. [VMware Telco Cloud, and Keeping the Certification Program Current](chapters/20-vmware-telco-cloud-and-keeping-the-certification-program-current.md) — the Telco Cloud specialist skills exams (5V0-36.22, 5V0-37.22, 5V0-44.21) and a four-step, primary-source currency check that keeps this volume, the appendix, and the blueprint accurate as the program churns.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all twenty
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

Chapters 17 through 20 extend this alignment across the rest of the
Broadcom certification program — the remaining professional exams, the
advanced VCAP tier, the Distinguished Expert design defense, and the
Telco Cloud specialist exams — and are summarized under
[Beyond the five: the wider certification program](#beyond-the-five-the-wider-certification-program)
below. Every exam code in those chapters was verified against Broadcom's
own certification pages; the same "confirm before scheduling" caution
applies.

### The exams

All five are proctored, scored on a scaled 100–500 range with 300 to
pass, and priced at $250 US.

| Exam | Certification | Targets | Duration | Questions |
| --- | --- | --- | --- | --- |
| 2V0-16.25 | VCP-VVF Administrator | vSphere Foundation 9.0 | 135 min | 60 |
| 2V0-18.25 | VCP-VVF Support | vSphere Foundation 9.0 | 135 min | 60 |
| 2V0-17.25 | VCP-VCF Administrator | Cloud Foundation 9.0 | 135 min | 60 |
| 2V0-15.25 | VCP-VCF Support | Cloud Foundation 9.0 | 135 min | 60 |
| 2V0-41.24 | VCP-NV | NSX 4.x | 135 min | 55 |

The four 2025-generation exams use multiple choice and multiple-selection
multiple choice only. **VCP-NV is the outlier**: a 2024-generation exam
with the widest format range of the five — its exam guide names
build-list, matching, drag-and-drop, point-and-click, and hot-area
alongside multiple choice and multiple-selection multiple choice, and
notes that further item types may appear. Prepare for the interaction
styles, not only the content. It is also the *shortest* of the five at 55
items rather than 60, which cuts the other way: each question carries
more weight.

Language availability differs, and the exam guides are sparing about it.
Broadcom explicitly describes **2V0-15.25 and 2V0-18.25** as delivered
"in English"; the guides for 2V0-16.25, 2V0-17.25, and 2V0-41.24 make no
language statement at all. Absence of a statement is not a promise of
other languages — confirm what you need at registration rather than
inferring it from silence.

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

### Which exam to take, and in what order

Five exams is the largest certification surface in this encyclopedia, and
the first real question is not how to study but **which of these you
should sit at all**. Most readers should take one or two, not five.

| If you… | Take | Why |
| --- | --- | --- |
| Run vSphere without VCF | **2V0-16.25** VVF Administrator | The narrowest product boundary and the closest match to ordinary vSphere administration |
| Run vSphere and work a support queue | **2V0-18.25** VVF Support | Same product boundary, diagnostic emphasis |
| Run or are moving to VCF | **2V0-17.25** VCF Administrator | Adds SDDC Manager, workload domains, and lifecycle across the stack |
| Support a VCF estate | **2V0-15.25** VCF Support | Failure-domain reasoning across a much wider component set |
| Work primarily in NSX | **2V0-41.24** VCP-NV | Independent of the VVF/VCF split — a different product, not a different tier |

Two structural points that are easy to miss. **The administrator and
support exams are siblings, not a ladder** — neither is a prerequisite for
the other, and they differ in emphasis rather than difficulty, so taking
both of a pair is a modest increment over taking one. And **VCF is a
superset of VVF**, so the VCF exams assume the vSphere material the VVF
exams test; going VVF first is the lower-risk order even though nothing
requires it.

**VCP-NV sits outside the sequence entirely.** It targets NSX 4.x on a
2024-generation blueprint while the other four target 9.0 products on
2025-generation blueprints, and as noted above its question formats are
wider. Treat it as a separate project rather than a fifth step.

### Study plan

Eight weeks for a first VCP for a candidate already administering
vSphere, at eight to ten hours a week. A second exam within the same
family costs far less — typically three to four weeks, because the
product knowledge transfers and only the emphasis changes.

**Weeks 1–5 are common to all five exams**, because they are this
volume's core and every blueprint rests on them:

| Week | Focus | Chapters |
| --- | --- | --- |
| 1 | Architecture and design, ESXi installation and host operations | [01](chapters/01-vmware-virtualization-architecture-and-design.md), [02](chapters/02-esxi-installation-configuration-and-host-operations.md) |
| 2 | vCenter deployment, identity, and recovery; virtual networking | [03](chapters/03-vcenter-server-deployment-identity-and-recovery.md), [04](chapters/04-vsphere-virtual-networking.md) |
| 3 | VM lifecycle and resource management; storage and vSAN | [05](chapters/05-virtual-machine-lifecycle-and-resource-management.md), [06](chapters/06-vsphere-storage-and-vsan.md) |
| 4 | Availability, mobility, and cluster services — HA, DRS, vMotion | [07](chapters/07-vsphere-availability-mobility-and-cluster-services.md) |
| 5 | Security architecture; lifecycle, automation, and troubleshooting | [08](chapters/08-vsphere-and-nsx-security-architecture.md), [09](chapters/09-vsphere-lifecycle-automation-observability-and-troubleshooting.md) |

**Weeks 6–8 diverge by exam**, and each has a preparation chapter that
carries its own blueprint mapping and study tracker:

| Exam | Weeks 6–8 | Preparation chapter |
| --- | --- | --- |
| 2V0-16.25 VVF Administrator | Blueprint mapping, then `esxtop` and DRS/HA optimization, which that chapter singles out for extra attention | [15](chapters/15-vcp-vmware-vsphere-foundation-administrator-2v0-16-25-exam-preparation.md) |
| 2V0-18.25 VVF Support | Cross-layer diagnostic fluency and licensing-restriction recognition | [16](chapters/16-vcp-vmware-vsphere-foundation-support-2v0-18-25-exam-preparation.md) |
| 2V0-17.25 VCF Administrator | Workload domain deployment models and day-2 administration, plus certificate lifecycle | [14](chapters/14-vcp-vmware-cloud-foundation-administrator-2v0-17-25-exam-preparation.md) |
| 2V0-15.25 VCF Support | VCF component failure domains and certificate/credential expiration triage | [13](chapters/13-vcp-vmware-cloud-foundation-support-2v0-15-25-exam-preparation.md) |
| 2V0-41.24 VCP-NV | NSX blueprint mapping, plus deliberate practice on the wider question formats | [12](chapters/12-vcp-network-virtualization-2v0-41-24-exam-preparation.md) |

Run the Hands-on Labs mapped below **during weeks 1–5**, not saved for the
end. They are the only lab environment most readers will have, and used
alongside the chapters they reinforce, they substitute for the home lab
this volume otherwise assumes.

**Because Broadcom publishes no domain weights**, the study tracker in
each preparation chapter is doing the job a weight table would do
elsewhere: it forces you to record confidence per blueprint section, so
your own weakest area determines where time goes. That is a genuinely
worse instrument than published weights, and it is the best available
one — build it in week 6 rather than week 8, so it has time to redirect
you.

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

**Do not trust the product filters to find everything.** Filtering by
NSX returns three labs, but *Building Resilient Networks with NSX*
carries no product tag and so does not appear, and the vDefend
micro-segmentation labs are filed under vDefend Firewall rather than NSX.
Search by title, and browse the catalogs as well as the product list.

### Mind the version: 9.1 labs, 9.0 exams

The catalog is organized into several collections alongside the main
Hands-on Labs one — *Explore Labs 2025*, *Test your Skills Play Odyssey*,
and a **VCF 9.1 Labs** set covering material newer than any current exam:

| Lab | Covers |
| --- | --- |
| `HOL-2701-01-VCF-L` | What's New in VCF 9.1: Highlights |
| `HOL-2702-01-VCF-L` | Kubernetes updates in VCF 9.1 (VKS, VM Service, Supervisor) |
| `HOL-2703-01-VCF-L` | Memory Tiering in VCF 9.1 |

All five VCP exams target **9.0** releases. The 9.1 labs are worth doing
for currency in a production role, but their content sits ahead of every
blueprint — time spent there is professional development, not exam
preparation, and should not displace the 9.0 material when a test date is
booked.

Note finally that labs cycle through maintenance windows; a lab listed
here may show as unavailable temporarily rather than having been
withdrawn.

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

### Beyond the five: the wider certification program

The five VCP exams above are not the whole Broadcom certification program,
and Chapters 17–20 map the rest of it. All codes below were verified
against Broadcom's own certification pages; confirm currency before
scheduling, as this program churns faster than most.

**The rest of the professional (VCP) tier — [Chapter 17](chapters/17-completing-the-vcp-tier-dcv-vcf-architect-avi-and-private-cloud-security.md).**
Four more professional-level exams sit alongside the five above:

| Exam | Code | Note |
| --- | --- | --- |
| VCP-DCV — Data Center Virtualization | 2V0-21.23 | vSphere 8 generation; the classic flagship VCP |
| VCP-VCF Architect | 2V0-13.25 | design-role VCP; the on-ramp to VCAP Architect and VCDX |
| VCP-AVI — Avi Load Balancer Administrator | 6V0-22.25 | 6V0 specialist code; application delivery |
| VCP-PCS — Private Cloud Security Administrator | 6V0-21.25 | 6V0 specialist code; builds on Chapter 08 |

**The advanced (VCAP) tier — [Chapter 18](chapters/18-the-vcap-advanced-professional-tier-vcf-9-0-role-exams-dcv-design-and-nv-deploy.md).**
A current VCP is the entry gate. The VCF 9.0 role series is eight exams on
one 3V0 generation, joined by two carried-over VCAP exams:

| Exam | Code | Format |
| --- | --- | --- |
| VCF Administrator | 3V0-11.26 | written |
| VCF Architect | 3V0-12.26 | design |
| VCF Support | 3V0-13.26 | written |
| VCF Automation | 3V0-21.25 | written |
| VCF Operations | 3V0-22.25 | written |
| VCF Storage | 3V0-23.25 | written |
| VCF VKS (Kubernetes) | 3V0-24.25 | written |
| VCF Networking | 3V0-25.25 | written |
| VCAP-DCV Design | 3V0-21.23 | design — **retiring 31 July 2026** |
| VCAP-NV Deploy | 3V0-41.22 | deploy (live build) — **retiring 31 July 2026** |

**The Distinguished Expert (VCDX) — [Chapter 19](chapters/19-vcdx-the-distinguished-expert-design-defense-discipline.md).**
The apex credential, earned not by an exam but by authoring a
production-grade design and defending it live before a peer panel. There
is no written exam code; the design-oriented exams in Chapters 17–18 are
the intended on-ramps.

**Telco Cloud specialist skills — [Chapter 20](chapters/20-vmware-telco-cloud-and-keeping-the-certification-program-current.md).**
A service-provider NFV specialization on the older 5V0 generation —
Platform (5V0-36.22), NFV (5V0-37.22), and Automation (5V0-44.21) — off
the mainstream path. Chapter 20 also defines the four-step, primary-source
currency check that keeps this whole map, the
[course-catalog appendix](../volume-97-master-appendices/chapters/07-appendix-vmware-broadcom-certifications-and-course-access.md),
and [CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md)
accurate over time.

## Topic-level lab coverage

Every testable objective in all **fourteen** VMware/Broadcom exam guides
that publish one is covered by a hands-on **walkthrough** lab in this
volume — **243 topic-level labs** in all, plus one integrative lab per
exam chapter. Objectives were harvested from the authoritative Broadcom
exam guides (`docs.broadcom.com`) on 24 July 2026. Labs use PowerCLI,
`esxcli`, and the NSX / VCF / TCA / vCloud Director REST APIs; each is a
full walkthrough (command, expected result, a negative test, and cleanup)
and carries `**Lab verified by:** *pending*` until a human runs it.

Two credentials carry no per-objective labs by design: **VCDX**
(Chapter 19) is a design-defense credential with no exam and is covered by
a Design Exercise; the **eight VCF 9.0 role exams** (3V0-11.26 …
3V0-25.25) publish no objective guide yet and are covered against
Broadcom's standardized Deploy/Configure/Operate section (Lab 18.25). The
design exams — VCAP-DCV Design, VCP-VCF Architect — additionally carry a
reasoning-only Design Exercise alongside their command-driven walkthroughs.

### VCP-NV (2V0-41.24) — 16 objectives

Labs in [Chapter 12](chapters/12-vcp-network-virtualization-2v0-41-24-exam-preparation.md#hands-on-lab).

| Objective | Lab |
| --- | --- |
| 4.1 Prepare an NSX infrastructure for deployment | Lab 12.1 |
| 4.2 Configure segments | Lab 12.2 |
| 4.3 Deploy and configure NSX Edge Nodes | Lab 12.3 |
| 4.4 Configure the Tier-1 gateway | Lab 12.4 |
| 4.5 Create and configure a Tier-0 gateway with OSPF | Lab 12.5 |
| 4.6 Configure the Tier-0 gateway with BGP | Lab 12.6 |
| 4.7 Configure VRF Lite | Lab 12.7 |
| 4.8 Configure Network Address Translation (NAT) | Lab 12.8 |
| 4.9 Deploy Virtual Private Networks | Lab 12.9 |
| 4.10 Manage users and roles | Lab 12.10 |
| 4.11 Perform operations tasks in a VMware NSX environment (syslog, backup/restore etc.) | Lab 12.11 |
| 4.12 Monitor a VMware NSX implementation | Lab 12.12 |
| 4.13 Use NSX Intelligence | Lab 12.13 |
| 5.1 Use log files to troubleshoot issues | Lab 12.14 |
| 5.2 Identify Tools Available for Troubleshooting Issues | Lab 12.15 |
| 5.3 Troubleshoot Common NSX Issues | Lab 12.16 |

### VCP-VCF Support (2V0-15.25) — 10 objectives

Labs in [Chapter 13](chapters/13-vcp-vmware-cloud-foundation-support-2v0-15-25-exam-preparation.md#hands-on-lab).

| Objective | Lab |
| --- | --- |
| 5.1 Troubleshooting the Deployment of VMware Cloud Foundation (VCF) - VCF Fleet | Lab 13.1 |
| 5.3 Troubleshooting a VMware Cloud Foundation Fleet - VCF Workload Domains | Lab 13.2 |
| 5.4 Troubleshooting a VMware Cloud Foundation Fleet - VCF Operations Fleet Management | Lab 13.3 |
| 5.5 Troubleshooting a VMware Cloud Foundation Fleet - License Management | Lab 13.4 |
| 5.6 Troubleshooting a VMware Cloud Foundation Fleet - VCF Compute | Lab 13.5 |
| 5.7 Troubleshooting a VMware Cloud Foundation Fleet - VCF Storage | Lab 13.6 |
| 5.8 Troubleshooting a VMware Cloud Foundation Fleet - Networking | Lab 13.7 |
| 5.9 Troubleshooting a VMware Cloud Foundation Fleet - VCF Operations | Lab 13.8 |
| 5.10 Given a scenario, troubleshoot issues with VMware Cloud Foundation Identity Broker | Lab 13.9 |
| 5.11 Troubleshooting VMware Cloud Foundation - Workload Mobility | Lab 13.10 |

### VCP-VCF Administrator (2V0-17.25) — 6 objectives

Labs in [Chapter 14](chapters/14-vcp-vmware-cloud-foundation-administrator-2v0-17-25-exam-preparation.md#hands-on-lab).

| Objective | Lab |
| --- | --- |
| 2.1 Private Cloud Vision | Lab 14.1 |
| 2.2 VMware Compute Fundamentals | Lab 14.2 |
| 2.4 VMware Network Fundamentals | Lab 14.3 |
| 4.1 VCF: Deploy and Configure | Lab 14.4 |
| 4.2 VCF: Manage | Lab 14.5 |
| 4.3 VCF: Operations | Lab 14.6 |

### VCP-VVF Administrator (2V0-16.25) — 8 objectives

Labs in [Chapter 15](chapters/15-vcp-vmware-vsphere-foundation-administrator-2v0-16-25-exam-preparation.md#hands-on-lab).

| Objective | Lab |
| --- | --- |
| 2.1 Virtualization Fundamentals | Lab 15.1 |
| 2.2 VMware Compute Fundamentals | Lab 15.2 |
| 2.3 VMware Storage Fundamentals | Lab 15.3 |
| 2.4 VMware Network Fundamentals | Lab 15.4 |
| 4.1 VVF: Deploy and Configure (ready to write) | Lab 15.5 |
| 4.2 VVF: Manage | Lab 15.6 |
| 4.3 VVF: Operate | Lab 15.7 |
| 4.4 VVF: Consume and Automate | Lab 15.8 |

### VCP-VVF Support (2V0-18.25) — 9 objectives

Labs in [Chapter 16](chapters/16-vcp-vmware-vsphere-foundation-support-2v0-18-25-exam-preparation.md#hands-on-lab).

| Objective | Lab |
| --- | --- |
| 5.1 Troubleshooting the Deployment of VMware vSphere Foundation (VVF) Solution | Lab 16.1 |
| 5.2 Troubleshooting the Deployment of VMware vSphere Foundation (VVF) - VVF Upgrade | Lab 16.2 |
| 5.3 Troubleshooting a VMware vSphere Foundation (VVF) - Clusters | Lab 16.3 |
| 5.4 Troubleshooting a VMware vSphere Foundation (VVF) Deployment - License Management | Lab 16.4 |
| 5.5 Troubleshooting a VMware vSphere Foundation (VVF) Deployment - Compute | Lab 16.5 |
| 5.6 Troubleshooting a VMware vSphere Foundation (VVF) Deployment - Storage | Lab 16.6 |
| 5.7 Troubleshooting a VMware vSphere Foundation (VVF) Deployment - Networks | Lab 16.7 |
| 5.8 Troubleshooting a VMware vSphere Foundation (VVF) - VCF Operations | Lab 16.8 |
| 5.9 Troubleshooting a VMware vSphere Foundation (VVF) - VCF Operations Orchestrator | Lab 16.9 |

### VCP-DCV (2V0-21.23) — 32 objectives

Labs in [Chapter 17](chapters/17-completing-the-vcp-tier-dcv-vcf-architect-avi-and-private-cloud-security.md#hands-on-lab).

| Objective | Lab |
| --- | --- |
| 1.1 Identify the pre-requisites and components for a VMware vSphere 8.x implementation | Lab 17.1 |
| 1.2 Describe the components and topology of a VMware vCenter architecture | Lab 17.2 |
| 1.6 Describe VMware vSphere Lifecycle Manager concepts | Lab 17.3 |
| 1.12 Identify use cases for VMware Tools | Lab 17.4 |
| 2.1 Describe the role of VMware vSphere in the Software-Defined Data Center | Lab 17.5 |
| 2.3 Identify use cases for VMware vCenter Converter | Lab 17.6 |
| 4.3 Configure Virtual Standard Switch (VSS) advanced virtual networking options | Lab 17.7 |
| 4.5 Deploy and configure VMware vCenter Server Appliance (VCSA) | Lab 17.8 |
| 4.7 Deploy and configure VMware vCenter High Availability | Lab 17.9 |
| 4.11 Configure VMware vCenter file-based backup | Lab 17.10 |
| 4.12 Configure vSphere Trust Authority | Lab 17.11 |
| 4.14 Configure vSphere Lifecycle Manager | Lab 17.12 |
| 4.15 Configure different network stacks | Lab 17.13 |
| 4.16 Configure host profiles | Lab 17.14 |
| 5.2 Monitor resources of a VMware vCenter Server Appliance (VCSA) and vSphere 8.x environment | Lab 17.15 |
| 5.3 Identify and use resource monitoring tools | Lab 17.16 |
| 5.4 Configure Network I/O Control (NIOC) | Lab 17.17 |
| 5.5 Configure Storage I/O Control (SIOC) | Lab 17.18 |
| 5.6 Configure a virtual machine port group to be offloaded to a data processing unit (DPU) | Lab 17.19 |
| 5.7 Explain the performance impact of maintaining virtual machine snapshots | Lab 17.20 |
| 5.8 Use Update Planner to identify opportunities to update VMware vCenter | Lab 17.21 |
| 5.10 Use performance charts to monitor performance | Lab 17.22 |
| 5.11 Perform proactive management with VMware Skyline | Lab 17.23 |
| 5.12 Use VMware vCenter management interface to update VMware vCenter | Lab 17.24 |
| 6.1 Identify use cases for enabling vSphere Cluster Services (vCLS) retreat mode | Lab 17.25 |
| 6.3 Generate a log bundle | Lab 17.26 |
| 7.1 Create and manage virtual machine snapshots | Lab 17.27 |
| 7.5 Create DRS affinity and anti-affinity rules for common use cases | Lab 17.28 |
| 7.7 Configure role-based access control | Lab 17.29 |
| 7.8 Manage host profiles | Lab 17.30 |
| 7.10 Use predefined alarms in VMware vCenter | Lab 17.31 |
| 7.11 Create custom alarms | Lab 17.32 |

### VCP-VCF Architect (2V0-13.25) — 8 objectives

Labs in [Chapter 17](chapters/17-completing-the-vcp-tier-dcv-vcf-architect-avi-and-private-cloud-security.md#hands-on-lab).

| Objective | Lab |
| --- | --- |
| 1.1 Differentiate between business and technical requirements | Lab 17.33 |
| 1.2 Differentiate between a Conceptual Model, logical design and physical design | Lab 17.34 |
| 1.3 Differentiate between requirements, assumptions, constraints and risks | Lab 17.35 |
| 1.5 Develop and document a risk mitigation strategy | Lab 17.36 |
| 1.6 Document design decisions | Lab 17.37 |
| 1.7 Develop a design validation strategy | Lab 17.38 |
| 3.1 Gather and analyze business objectives and requirements | Lab 17.39 |
| 3.2 Given a set of business objectives, create a conceptual model | Lab 17.40 |

### VCP-AVI (6V0-22.25) — 21 objectives

Labs in [Chapter 17](chapters/17-completing-the-vcp-tier-dcv-vcf-architect-avi-and-private-cloud-security.md#hands-on-lab).

| Objective | Lab |
| --- | --- |
| 1.2 Identify what it means to have a distributed data plane | Lab 17.41 |
| 1.3 Identify the tasks performed by the Service Engine in an AVI architecture | Lab 17.42 |
| 1.4 Identify the characteristics of L4 from a load balancing perspective | Lab 17.43 |
| 1.5 Identify the characteristics of L7 from a load balancing perspective | Lab 17.44 |
| 1.7 Identify the characteristics of HA including Active Active/N+M and Active Standby | Lab 17.45 |
| 1.8 Identify the characteristics of Service Engine Groups | Lab 17.46 |
| 1.9 Identify the use case for elastic scale out | Lab 17.47 |
| 1.10 Identify the interaction of objects including virtual service, pool, and virtual IP | Lab 17.48 |
| 1.11 Identify the features inside an application profile | Lab 17.49 |
| 1.12 Identify the functions of policy engine | Lab 17.50 |
| 1.13 Identify how certificate management is conducted | Lab 17.51 |
| 1.14 Identify the steps to turn on and off a WAF | Lab 17.52 |
| 1.15 Identify the capacity impact of turning WAF on and off | Lab 17.53 |
| 5.1 Identify the capacity limitation of the service engine and the service engine group | Lab 17.54 |
| 5.2 Identify the impact of elastic scale out | Lab 17.55 |
| 5.3 Identify the performance limitations of real-time analytics and logs | Lab 17.56 |
| 6.1 Identify the meaning of significant and non-significant logging | Lab 17.57 |
| 6.3 Identify how to enable real-time analytics | Lab 17.58 |
| 6.4 Given a scenario about real-time analytics, identify where the problem exists | Lab 17.59 |
| 6.5 Given a scenario and a health score, interpret the score and what can affect the score | Lab 17.60 |
| 6.6 Identify how the logs will change when WAF is enabled | Lab 17.61 |

### VCP-PCS (6V0-21.25) — 11 objectives

Labs in [Chapter 17](chapters/17-completing-the-vcp-tier-dcv-vcf-architect-avi-and-private-cloud-security.md#hands-on-lab).

| Objective | Lab |
| --- | --- |
| 1 Private Cloud Data Center Security | Lab 17.62 |
| 2 VMware vDefend Firewall Architecture | Lab 17.63 |
| 3 VMware vDefend Firewall Management | Lab 17.64 |
| 6 Planning Application Segmentation with | Lab 17.65 |
| 9 Gateway Firewall | Lab 17.66 |
| 10 Security Automation | Lab 17.67 |
| 11 Security Operations | Lab 17.68 |
| 12 Role-Based Access Control | Lab 17.69 |
| 13 Troubleshooting | Lab 17.70 |
| 14 Advanced Threat Prevention | Lab 17.71 |
| 16 Malware Prevention Detection | Lab 17.72 |

### VCAP-NV Deploy (3V0-41.22) — 10 objectives

Labs in [Chapter 18](chapters/18-the-vcap-advanced-professional-tier-vcf-9-0-role-exams-dcv-design-and-nv-deploy.md#hands-on-lab).

| Objective | Lab |
| --- | --- |
| 4.1 Prepare VMware NSX-T Data Center Infrastructure | Lab 18.1 |
| 4.2 Create and Manage VMware NSX-T Data Center Virtual Networks | Lab 18.2 |
| 4.3 Deploy and Manage VMware NSX-T Data Center Network Services | Lab 18.3 |
| 4.4 Secure a virtual data center with VMware NSX-T Data Center | Lab 18.4 |
| 4.6 Deploy and Manage Central Authentication (Workspace ONE access) | Lab 18.5 |
| 5.1 Configure and Manage Enhanced Data Path (N-VDSe) | Lab 18.6 |
| 5.2 Configure and Manage Quality of Service (QoS) settings | Lab 18.7 |
| 6.1 Perform Advanced VMware NSX-T Data Center Troubleshooting | Lab 18.8 |
| 7.1 Perform Operational Management of a VMware NSX-T Data Center Implementation | Lab 18.9 |
| 7.2 Utilize API and CLI to manage a VMware NSX-T Data Center Deployment | Lab 18.10 |

### VCAP-DCV Design (3V0-21.23) — 14 objectives

Labs in [Chapter 18](chapters/18-the-vcap-advanced-professional-tier-vcf-9-0-role-exams-dcv-design-and-nv-deploy.md#hands-on-lab).

| Objective | Lab |
| --- | --- |
| 1.2 Differentiate conceptual, logical, and physical design | Lab 18.11 |
| 2.1 Describe VMware Cloud Foundation architecture | Lab 18.12 |
| 2.2 Describe VMware Validated Solutions architecture | Lab 18.13 |
| 3.1 Gather and analyze business objectives and requirements | Lab 18.14 |
| 3.2 Create a conceptual model | Lab 18.15 |
| 3.3 Create a logical design | Lab 18.16 |
| 3.4 Create a physical design | Lab 18.17 |
| 3.5 Design for manageability: capacity planning | Lab 18.18 |
| 3.6 Design for manageability: scalability | Lab 18.19 |
| 3.7 Design for manageability: lifecycle management | Lab 18.20 |
| 3.8 Design for availability | Lab 18.21 |
| 3.9 Design for performance | Lab 18.22 |
| 3.10 Design for security | Lab 18.23 |
| 3.11 Design for recoverability | Lab 18.24 |

### Telco Cloud Automation (5V0-44.21) — 42 objectives

Labs in [Chapter 20](chapters/20-vmware-telco-cloud-and-keeping-the-certification-program-current.md#hands-on-lab).

| Objective | Lab |
| --- | --- |
| 1.1 Identify the role of TCA within the NFV architecture | Lab 20.1 |
| 1.2 Identify the role of OVF within a network function | Lab 20.2 |
| 1.3 Identify the role of Helm chart with a CNF | Lab 20.3 |
| 1.4 Identify the characteristics of Life Cycle Management events | Lab 20.4 |
| 1.5 Identify the characteristics of self-healing | Lab 20.5 |
| 2.1 Identify the characteristics of the distributed architecture of VMware TCA | Lab 20.6 |
| 2.2 Identify why a VMware TCP control plane element is required | Lab 20.7 |
| 2.4 Identify the steps needed to integrate a VIM infrastructure | Lab 20.8 |
| 2.5 Identify how to integrate vRO with virtual infrastructures | Lab 20.9 |
| 2.6 Identify how tags are used in VMware Telco Cloud Automation | Lab 20.10 |
| 3.1 Identify how to verify the appropriate URL for connecting to a VIM | Lab 20.11 |
| 3.2 Identify the steps to configure a compute profile for a given VIM | Lab 20.12 |
| 4.1 Identify business benefits of automated CaaS deployment | Lab 20.13 |
| 4.2 Identify the differences between Kubernetes and VMware Tanzu Kubernetes Grid architectures | Lab 20.14 |
| 4.3 Identify the differences between the TKG cluster types | Lab 20.15 |
| 4.4 Identify the steps to deploy a Management cluster | Lab 20.16 |
| 4.5 Identify the steps to deploy a Workload cluster | Lab 20.17 |
| 4.6 Identify the steps to scale a node pool | Lab 20.18 |
| 4.7 Identify the prerequisites to deploy CaaS with no internet connectivity | Lab 20.19 |
| 5.1 Identify the steps to integrate Harbor with TCA | Lab 20.20 |
| 6.1 Identify the business benefit of infrastructure automation | Lab 20.21 |
| 6.2 Identify the characteristics of infrastructure automation versioning | Lab 20.22 |
| 7.1 Identify the differences between the roles of network services and network functions | Lab 20.23 |
| 7.2 Identify the differences between a CNF and VNF | Lab 20.24 |
| 7.3 Identify the characteristics of NFD and NSD | Lab 20.25 |
| 7.4 Given a descriptor, identify the attribute | Lab 20.26 |
| 7.5 Identify the steps to onboard a network function | Lab 20.27 |
| 7.6 Identify the prerequisites for onboarding a network service | Lab 20.28 |
| 7.7 Identify the role of late binding | Lab 20.29 |
| 7.9 Identify the steps to instantiate a VNF network function | Lab 20.30 |
| 7.11 Identify the characteristics of the network function inventory | Lab 20.31 |
| 8.1 Identify the role of a VMware vCenter Server® system in credential management | Lab 20.32 |
| 8.2 Identify the steps in creating a role within TCA | Lab 20.33 |
| 8.3 Identify the steps in creating a permission within TCA | Lab 20.34 |
| 8.4 Identify the steps to modify a permission to include tag-based filtering within TCA | Lab 20.35 |
| 9.1 Identify the steps required after upgrading VMware Telco Cloud Automation | Lab 20.36 |
| 9.2 Identify the key life cycle management events for a VNF | Lab 20.37 |
| 9.3 Identify the key life cycle management events for a CNF | Lab 20.38 |
| 9.4 Identify the key life cycle management events for a NS | Lab 20.39 |
| 9.5 Identify the differences between performing a CNF update and a VNF update | Lab 20.40 |
| 9.6 Identify the characteristics of performing healing on a network function | Lab 20.41 |
| 10.4 Given a system problem, identify the log that should be viewed to troubleshoot the problem | Lab 20.42 |

### Telco Cloud NFV (5V0-37.22) — 31 objectives

Labs in [Chapter 20](chapters/20-vmware-telco-cloud-and-keeping-the-certification-program-current.md#hands-on-lab).

| Objective | Lab |
| --- | --- |
| 1.1 Identify the key functions of Telco Cloud | Lab 20.43 |
| 1.2 Identify the components of the VMware Telco Cloud Infrastructure architecture | Lab 20.44 |
| 1.3 Identify valid VMware Telco Cloud Infrastructure deployment options | Lab 20.45 |
| 1.4 Identify the function of components of the VMware Cloud Director architecture | Lab 20.46 |
| 2.2 Identify the key VMware components that are part of VMware Cloud Director | Lab 20.47 |
| 3.1 Identify characteristics of physical and virtual infrastructures | Lab 20.48 |
| 3.2 Identify the advantages and components of the NFV infrastructure (NFVI) | Lab 20.49 |
| 3.3 Identify the function of network virtualization in the NFVI | Lab 20.50 |
| 3.4 Identify requirements of NFVI on VMware Cloud Director | Lab 20.51 |
| 3.5 Identify key networking use cases | Lab 20.52 |
| 3.6 Identify the storage options of VMware Cloud Director | Lab 20.53 |
| 4.2 Identify the function of resource pools | Lab 20.54 |
| 4.3 Identify the functional characteristics of vSAN storage polices | Lab 20.55 |
| 4.4 Identify how compute resources are provided to VMware Cloud Director | Lab 20.56 |
| 4.5 Identify how storage resources are provided to VMware Cloud Director | Lab 20.57 |
| 4.6 Identify characteristics of VMware Cloud Director organizations | Lab 20.58 |
| 4.7 Identify characteristics of VMware Cloud Director organization VDC | Lab 20.59 |
| 4.8 Identify characteristics of organization VDC allocation models | Lab 20.60 |
| 4.9 Identify characteristics of types of resources that can be allocated | Lab 20.61 |
| 4.11 Identify the process of adding and modifying elements in the catalog | Lab 20.62 |
| 4.12 Identify the characteristics of vApps | Lab 20.63 |
| 4.14 Identify key networking use cases in VMware Cloud Director | Lab 20.64 |
| 4.17 Identify characteristics of the architecture of VMware NSX-T Data Center | Lab 20.65 |
| 4.18 Identify the function of VMware Cloud Director supported features of NSX-T Data Center | Lab 20.66 |
| 4.19 Identify the benefits and challenges of networking between VDCs | Lab 20.67 |
| 5.1 Identify the function of key resources that need to be managed with VMware Cloud Director | Lab 20.68 |
| 5.2 Identify the characteristics of features of vRealize Operations Manager | Lab 20.69 |
| 5.3 Identify the purpose of the vRealize Operations Tenant App for VMware Cloud Director | Lab 20.70 |
| 5.4 Identify the steps to monitor VMware Cloud Director environments with vRealize Log Insight | Lab 20.71 |
| 6.3 Identify the use of logs in VMware Cloud Director | Lab 20.72 |
| 7.1 Identify the characteristics of role-based access | Lab 20.73 |

### Telco Cloud Platform (5V0-36.22) — 25 objectives

Labs in [Chapter 20](chapters/20-vmware-telco-cloud-and-keeping-the-certification-program-current.md#hands-on-lab).

| Objective | Lab |
| --- | --- |
| 1.1 Identify the characteristics of the architecture of VMware Telco Cloud Platform | Lab 20.74 |
| 1.2 Identify the characteristics of the VMware Telco Cloud Automation architecture | Lab 20.75 |
| 1.3 Identify the characteristics of VMware Telco Cloud Automation deployment options | Lab 20.76 |
| 1.4 Identify the characteristics of the vSphere architecture | Lab 20.77 |
| 2.1 Identify the key VMware components that are part of vSphere | Lab 20.78 |
| 2.2 Identify the characteristics of the networking options of vSphere | Lab 20.79 |
| 2.3 Identify the characteristics of the storage options of vSphere | Lab 20.80 |
| 2.4 Identify the role of containers in VMware Telco Cloud Platform | Lab 20.81 |
| 2.5 Identify the characteristics of the Kubernetes architecture | Lab 20.82 |
| 2.6 Identify the role of nodes and clusters | Lab 20.83 |
| 2.7 Identify the supporting components of Kubernetes | Lab 20.84 |
| 2.8 Identify the characteristics of the architecture of Tanzu Kubernetes Grid | Lab 20.85 |
| 2.9 Identify the characteristics of the types of network functions | Lab 20.86 |
| 2.11 Identify the key vSphere operations for VNFs | Lab 20.87 |
| 2.12 Identify the special requirements of containers for network functions | Lab 20.88 |
| 2.13 Identify the type of descriptors for containers | Lab 20.89 |
| 2.14 Identify the role of Harbor | Lab 20.90 |
| 4.1 Identify the requirements for infrastructure | Lab 20.91 |
| 4.2 Identify the process of deploying VMs | Lab 20.92 |
| 4.3 Identify VM onboarding requirements | Lab 20.93 |
| 4.4 Identify the CNF requirements for onboarding | Lab 20.94 |
| 5.1 Identify the characteristics of the key concepts like late binding | Lab 20.95 |
| 6.4 Identify how to use logs in VMware Telco Cloud Platform | Lab 20.96 |
| 6.5 Identify the functionality of the CLI tools that can be used for troubleshooting | Lab 20.97 |
| 7.1 Identify characteristics of the VNF life cycle management | Lab 20.98 |

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
