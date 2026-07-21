# Volume XXIII — Dell iDRAC 9 and 10 Administration

> Single-server, out-of-band administration of the integrated Dell Remote
> Access Controller — architecture, configuration, networking, identity
> and security, local and remote access, hardware health, storage,
> firmware, and automation — for the iDRAC9 and iDRAC10 generations.

## Overview

Volume XXIII covers the integrated Dell Remote Access Controller (iDRAC),
the baseboard management controller built into every Dell PowerEdge
server, across its two current generations: iDRAC9 (14th–16th generation
PowerEdge platforms) and iDRAC10 (17th generation and current platforms).
Volume IV — Enterprise Systems Administration is this volume's primary
dependency per [ROADMAP.md](../../ROADMAP.md); this volume assumes
comfort with general server administration and out-of-band management
concepts and focuses specifically on iDRAC's architecture, CLI (RACADM),
and API (Redfish) surface.

This volume is deliberately scoped to single-server administration. Where
an operation is more efficient or more appropriately performed at fleet
scale — discovery and inventory across many servers, firmware compliance
reporting, configuration templating across a fleet — the relevant chapter
points to the corresponding chapter in **Volume XXII — Dell OpenManage
Enterprise** rather than duplicating fleet-orchestration content here.
Every OpenManage Enterprise workflow ultimately resolves into the
per-server iDRAC operations this volume teaches directly, which is why
this volume is a practical prerequisite for troubleshooting OME-driven
operations that fail on a single unit.

The volume is organized as a progression from foundational access through
increasingly specialized administration domains, closing with an
automation-focused capstone:

- **Chapter 01** establishes iDRAC's architecture, the iDRAC9/iDRAC10
  generational split, license tiers, and first access.
- **Chapter 02** covers the escalation path from non-disruptive
  configuration export/import through iDRAC restart, factory reset, and
  full power cycle, plus recovery when iDRAC itself is unreachable.
- **Chapter 03** covers the management network: dedicated NIC vs. shared
  LOM, IPv4/IPv6, VLAN tagging, DNS, and NTP.
- **Chapter 04** covers identity and security: local and
  directory-integrated users, certificate management, the silicon root of
  trust, Secure Boot, System Lockdown Mode, and System Erase.
- **Chapter 05** covers local and remote interactive access: iDRAC
  Direct, Quick Sync, Virtual Console, Virtual Media, and the iDRAC
  Service Module.
- **Chapter 06** covers hardware health, power and thermal management,
  the System Event Log and Lifecycle Log, alerting, and the Tech Support
  Report.
- **Chapter 07** covers storage: PERC RAID controllers, BOSS boot
  storage, RAID level selection, hot spares, and drive maintenance.
- **Chapter 08** covers firmware update orchestration through the
  Lifecycle Controller: staged updates, catalog sourcing, sequencing, and
  rollback.
- **Chapter 09** is the automation-focused capstone: RACADM vs. Redfish
  vs. WS-Management, idempotent Python automation, the
  `dellemc.openmanage` Ansible collection, and an end-to-end provisioning
  runbook combining every prior chapter.

Every chapter follows the same structure — learning objectives, theory
and architecture, design considerations, implementation and automation,
validation and troubleshooting, security and best practices, references
and knowledge checks, a hands-on lab, and a summary and completion
checklist — defined in [templates/chapter.md](../../templates/chapter.md)
and enforced by [EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md).
Each hands-on lab is a reproducible, disposable exercise with a stated
objective, prerequisites, numbered steps, expected results, a negative
test where practical, recovery guidance, and cleanup instructions;
chapters covering genuinely disruptive or irreversible operations
(factory reset, full power cycle, System Erase) frame those procedures
with explicit safety guidance and scope hands-on execution to hardware
you are authorized to disrupt.

## Chapters

1. [Architecture, Generations, Licensing, and First Access](chapters/01-architecture-generations-licensing-and-first-access.md) — iDRAC architecture, the iDRAC9/iDRAC10 generational split, license tiers, and first network and iDRAC Direct access.
2. [Configuration, Restart, Factory Reset, Full Power Cycle, and Recovery](chapters/02-configuration-restart-factory-reset-full-power-cycle-and-recovery.md) — Server Configuration Profile export/import, iDRAC restart, factory reset scope, full AC power cycle, and recovery paths.
3. [Management Network, IPv4, IPv6, DNS, NTP, and Connectivity](chapters/03-management-network-ipv4-ipv6-dns-ntp-and-connectivity.md) — dedicated NIC vs. shared LOM, VLAN tagging, IPv4/IPv6 addressing, DNS, and NTP.
4. [Identity, Certificates, Security, and Compliance](chapters/04-identity-certificates-security-and-compliance.md) — local and directory-integrated users, certificate lifecycle, silicon root of trust, Secure Boot, System Lockdown Mode, and System Erase.
5. [iDRAC Direct, Virtual Console, Virtual Media, and Local Service](chapters/05-idrac-direct-virtual-console-virtual-media-and-local-service.md) — iDRAC Direct, Quick Sync, Virtual Console, Virtual Media, and the iDRAC Service Module.
6. [Hardware Health, Power, Thermal, Logs, and Support](chapters/06-hardware-health-power-thermal-logs-and-support.md) — health rollup, power capping and PSU redundancy, thermal control, System Event Log vs. Lifecycle Log, alerting, and the Tech Support Report.
7. [Storage Arrays, BOSS, RAID Configuration, and Maintenance](chapters/07-storage-arrays-boss-raid-configuration-and-maintenance.md) — PERC and BOSS controllers, RAID level selection, RAID vs. HBA mode, hot spares, and predictive failure response.
8. [Firmware, iDRAC, BIOS, Lifecycle Controller, and Platform Updates](chapters/08-firmware-idrac-bios-lifecycle-controller-and-platform-updates.md) — Lifecycle Controller update orchestration, staged updates, catalog sourcing, sequencing, and rollback.
9. [RACADM, Redfish, OpenManage, Automation, and Capstone Operations](chapters/09-racadm-redfish-openmanage-automation-and-capstone-operations.md) — RACADM vs. Redfish vs. WS-Management, idempotent automation, the `dellemc.openmanage` Ansible collection, and an end-to-end provisioning capstone.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine
  chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.

## Related volumes

- **Volume IV — Enterprise Systems Administration** — primary dependency;
  general server administration and out-of-band management foundations
  this volume builds on.
- **Volume XXII — Dell OpenManage Enterprise** — fleet-scale discovery,
  inventory, firmware compliance, configuration templating, and
  monitoring across many iDRACs at once, orchestrating the same
  per-server operations this volume teaches directly.
- **Volume IX — Infrastructure Automation** — general automation
  principles (idempotency, declarative vs. imperative automation) applied
  throughout this volume's implementation sections, particularly
  Chapter 09.

## Certification alignment

Dell's server certifications sit in the **Dell Technologies Proven
Professional** program, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). Two
exams cover this volume's material, and both span it and
[Volume XXII](../volume-22-dell-openmanage-enterprise/README.md):

| Exam | Level | Duration | Questions |
| --- | --- | --- | --- |
| **D-PE-FN-01** PowerEdge Foundations v2 | Foundational | 90 min | Not stated in the exam description |
| **D-PE-OE-01** PowerEdge Operate v2 | Specialist | 90 min | 50 |

Both are delivered through Pearson VUE. Operate v2 is offered in English,
French, and Japanese.

**`D-PE-OE-23` PowerEdge Operate 2023 has been superseded by
`D-PE-OE-01`.** This is not a renumbering — the blueprint was rebuilt.
The 2023 exam ran 120 minutes across five domains led by Server
Troubleshooting at 32%; the v2 exam runs 90 minutes across five
*different* domains, and its recommended training is built explicitly
around **iDRAC 10**. Material written against `D-PE-OE-23`, including
earlier revisions of this volume, describes an exam that is no longer
offered. Dell Learning currently lists only `D-PE-OE-01`.

### Domain weights, mapped to this volume

Transcribed from Dell's published exam descriptions. Both sets sum to
exactly 100%. Dell states each percentage "reflects the approximate
distribution of the total question set" — question-count proportions, not
scoring weights.

**D-PE-OE-01 Operate v2** — and note how flat it is:

| Domain | Weight | Chapters here | In Volume XXII |
| --- | --- | --- | --- |
| Server Management | 22% | [01](chapters/01-architecture-generations-licensing-and-first-access.md), [05](chapters/05-idrac-direct-virtual-console-virtual-media-and-local-service.md), [07](chapters/07-storage-arrays-boss-raid-configuration-and-maintenance.md), [09](chapters/09-racadm-redfish-openmanage-automation-and-capstone-operations.md) | 01–04, 08 |
| Troubleshooting | 22% | [02](chapters/02-configuration-restart-factory-reset-full-power-cycle-and-recovery.md), [06](chapters/06-hardware-health-power-thermal-logs-and-support.md) | 09 |
| Server Monitoring | 20% | [06](chapters/06-hardware-health-power-thermal-logs-and-support.md) | 04 |
| System Administration | 20% | [04](chapters/04-identity-certificates-security-and-compliance.md), [05](chapters/05-idrac-direct-virtual-console-virtual-media-and-local-service.md) | 02, 03 |
| Server Maintenance | 16% | [08](chapters/08-firmware-idrac-bios-lifecycle-controller-and-platform-updates.md) | 05, 06, 07 |

**The v2 blueprint is materially flatter than the one it replaced.** The
2023 exam spread 22 percentage points between its largest and smallest
domain; v2 spreads six. There is no dominant domain to prioritize and no
domain small enough to skip — every one is worth between a sixth and
roughly a quarter of the questions. Study strategies built around
"troubleshooting is a third of the exam" no longer apply.

**D-PE-FN-01 Foundations v2** — unchanged, and still front-loaded:

| Domain | Weight | Chapters here |
| --- | --- | --- |
| Introduction to Servers | 28% | [01](chapters/01-architecture-generations-licensing-and-first-access.md), [07](chapters/07-storage-arrays-boss-raid-configuration-and-maintenance.md) |
| Server Architecture and Roles | 22% | [01](chapters/01-architecture-generations-licensing-and-first-access.md) |
| Maintenance | 18% | [06](chapters/06-hardware-health-power-thermal-logs-and-support.md), [08](chapters/08-firmware-idrac-bios-lifecycle-controller-and-platform-updates.md) |
| Server Management | 14% | [01](chapters/01-architecture-generations-licensing-and-first-access.md), [05](chapters/05-idrac-direct-virtual-console-virtual-media-and-local-service.md) |
| Security | 12% | [04](chapters/04-identity-certificates-security-and-compliance.md) |
| Server Networking and Connectivity | 6% | [03](chapters/03-management-network-ipv4-ipv6-dns-ntp-and-connectivity.md) |

**Take Foundations first.** Half of it — introduction to servers plus
architecture and roles — is hardware knowledge this volume grounds
directly, and Operate assumes it.

### Where the exams reach beyond this volume

Foundations is broader than iDRAC administration. Two of its domains ask
about things no amount of iDRAC study covers:

- **Server Architecture and Roles (22%)** asks candidates to position
  PowerEdge for edge/ROBO, cloud, and core, and to compare storage
  topologies (DAS, NAS, SAN) and workload solutions for file sharing,
  HPC, and generative AI. That is portfolio and solution-design material,
  covered here only in passing.
- **Introduction to Servers (28%)** includes chassis form factors,
  generations, and nomenclature at a level of product detail this volume
  assumes rather than teaches.

For both, Dell's `ESSVRD05641` concepts course is the efficient route;
[Volume IV](../volume-04-enterprise-systems-administration/README.md)
supplies the general systems-administration grounding.

### Study plan

Six to eight weeks for both exams together, at eight to ten hours a week,
for a candidate with general server administration experience. Take
Foundations at the end of week 3 and Operate at the end of week 7 — the
gap matters, because Operate's Server Management domain assumes the
management-tool vocabulary Foundations tests.

**Weeks 1–3 — Foundations (D-PE-FN-01)**

| Week | Focus | Weight |
| --- | --- | --- |
| 1 | Servers, components, storage (HDD/SSD/PERC/BOSS/M.2/backplanes), generations and nomenclature. Chapters 01 and 07 here. | 28% |
| 2 | Architecture and roles, form factors, data flow, storage topologies, workload positioning. Chapter 01, plus `ESSVRD05641` for the portfolio material this volume does not carry. | 22% |
| 3 | Management concepts (in-band, out-of-band, at-the-box, BIOS vs UEFI, iDRAC licensing tiers, OMSA), maintenance, security, networking. Chapters 03, 04, 05, 06, 08. **Sit the exam.** | 50% |

**Weeks 4–7 — Operate (D-PE-OE-01)**

| Week | Focus | Weight |
| --- | --- | --- |
| 4 | Server Management: iDRAC settings, the tool landscape (Lifecycle Controller, RACADM, iSM, OME), and storage management. Chapters 01, 05, 07, 09, plus [Volume XXII](../volume-22-dell-openmanage-enterprise/README.md) 01–04. | 22% |
| 5 | Monitoring and System Administration: health checks, iDRAC monitoring, OS installation via virtual media, server security. Chapters 04, 05, 06. | 40% |
| 6 | Troubleshooting and Maintenance: hardware faults, proactive detection, firmware and BIOS updates through iDRAC, Lifecycle Controller, and CLI. Chapters 02, 06, 08. | 38% |
| 7 | Consolidation on the capstone in [Chapter 09](chapters/09-racadm-redfish-openmanage-automation-and-capstone-operations.md), which exercises the whole blueprint end to end. **Sit the exam.** | — |

Because v2 is flat, resist the urge to over-weight any single week. The
plan above deliberately pairs domains rather than isolating them.

### Study materials

Dell's recommended training, transcribed with course numbers. These are
paid, commercial courses.

**For D-PE-FN-01 Foundations v2** — a single course:

| Course | Number | Mode |
| --- | --- | --- |
| Dell PowerEdge Server Concepts | `ESSVRD05641` | On demand |

**For D-PE-OE-01 Operate v2** — two routes, both built around iDRAC 10:

| Option | Course | Number | Mode | Duration |
| --- | --- | --- | --- | --- |
| 1 | Dell PowerEdge Features, Administration and Troubleshooting with iDRAC 10 | `ESSVRS08588` | ILT / VILT | 24h |
| 2 | Dell PowerEdge Features with iDRAC10 | `ESSVRD08582` | On demand | 8h |
| 2 | Dell PowerEdge Administration with iDRAC10 | `ESSVRD08583` | On demand | 4.5h |
| 2 | Dell PowerEdge Troubleshooting with iDRAC10 | `ESSVRD08584` | On demand | 4.5h |

**The iDRAC 10 framing is the clearest signal that v2 is a genuine
refresh**, not a renumbering — the superseded 2023 courses
(`ESSVRD05997`, `ESSVRD05893`, `ESSVRD05894`) carried no generation in
their titles. This volume covers iDRAC 9 and 10 together and flags
generational differences in
[Chapter 01](chapters/01-architecture-generations-licensing-and-first-access.md),
which is the right shape for the current exam.

**Currency warning.** The Foundations description is dated 28 March 2025;
the Operate v2 description carries no date at all. Confirm codes,
weights, and course numbers against
[Dell Learning](https://learning.dell.com/content/dell/en-us/home/certification-overview.html)
at registration rather than trusting this table.

### Practicing — the hardware problem

iDRAC is the one platform in this encyclopedia with **no software-only
practice path**. It is a physical baseboard management controller; there
is no virtual appliance, no hosted sandbox, and no simulator. The console
this volume teaches exists only on a PowerEdge server.

That leaves three honest routes:

| Route | Notes |
| --- | --- |
| Second-hand PowerEdge | An older generation with iDRAC9 is inexpensive and covers most of this volume; note that iDRAC10 features will be absent |
| Employer hardware | A non-production or decommissioned server is the ideal lab, since [Chapter 02](chapters/02-configuration-restart-factory-reset-full-power-cycle-and-recovery.md)'s factory reset and recovery work needs a machine you may safely break |
| Dell trial licenses | Dell publishes trials for iDRAC, OpenManage Enterprise, OMIWAC and DPAT — these unlock Enterprise and Datacenter-tier iDRAC features on hardware you already have, not access to hardware |

**Plan around the license tier, not just the hardware.** Much of what
this volume covers — virtual console, virtual media, and the automation
in [Chapter 09](chapters/09-racadm-redfish-openmanage-automation-and-capstone-operations.md)
— requires iDRAC Enterprise or Datacenter rather than the base license.
A trial license on an otherwise basic server is often the difference
between a lab that exercises this volume and one that cannot.

The complementary move is
[Volume XXII](../volume-22-dell-openmanage-enterprise/README.md): the
OpenManage Enterprise appliance is a free download and runs on a
hypervisor, so fleet-management practice needs no hardware at all. A
reader without a PowerEdge should work Volume XXII first and treat this
volume as reading until hardware is available.

## Software and platform baseline

Chapters in this volume reference the dated baseline recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md): iDRAC9 and iDRAC10.
Attribute names, Redfish resource shapes, and RACADM command syntax
shown throughout this volume are accurate to that baseline; every chapter
explicitly flags where a specific attribute, action name, or entitlement
boundary should be confirmed against the current Dell documentation or a
running unit's own Attribute Registry/Redfish schema before being
scripted against a production fleet, since these details shift across
firmware releases within both generations.

## Building and validating this volume

From the repository root, after completing
[SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-23-dell-idrac-9-10-administration

# Build a single chapter.
scripts/bash/build-book.sh --format all \
  --chapter volumes/volume-23-dell-idrac-9-10-administration/chapters/01-architecture-generations-licensing-and-first-access.md
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
