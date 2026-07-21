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

| Exam | Level | Duration | Domains |
| --- | --- | --- | --- |
| **D-PE-FN-01** PowerEdge Foundations v2 | Foundational | 90 min | Introduction to Servers 28%; Server Architecture and Roles 22%; Maintenance 18%; Server Management 14%; Security 12%; Networking and Connectivity 6% |
| **D-PE-OE-23** PowerEdge Operate | Specialist | 120 min | Server Troubleshooting 32%; Server Components 26%; System Administration 18%; Server Management and Configuration Tools 14%; Server Portfolio and Features 10% |

Both are delivered through Pearson VUE. Question counts and cut scores
are set per exam and are not restated here; confirm them at registration.

**This volume is the higher-value one for the Operate exam.**
Troubleshooting at 32% and server components at 26% together make up 58%
of it, and both map to chapters here rather than to fleet management.
Take Foundations first — its heaviest domains, introduction to servers
(28%) and architecture (22%), are also grounded in this volume.

| Domain | Weight in Operate | Chapters here |
| --- | --- | --- |
| Server Troubleshooting | 32% | [02](chapters/02-configuration-restart-factory-reset-full-power-cycle-and-recovery.md), [06](chapters/06-hardware-health-power-thermal-logs-and-support.md) |
| Server Components | 26% | [06](chapters/06-hardware-health-power-thermal-logs-and-support.md), [07](chapters/07-storage-arrays-boss-raid-configuration-and-maintenance.md) |
| System Administration | 18% | [04](chapters/04-identity-certificates-security-and-compliance.md), [07](chapters/07-storage-arrays-boss-raid-configuration-and-maintenance.md) |
| Server Management and Configuration Tools | 14% | [05](chapters/05-idrac-direct-virtual-console-virtual-media-and-local-service.md), [09](chapters/09-racadm-redfish-openmanage-automation-and-capstone-operations.md) |
| Server Portfolio and Features | 10% | [01](chapters/01-architecture-generations-licensing-and-first-access.md) |

For Foundations, [Chapter 01](chapters/01-architecture-generations-licensing-and-first-access.md)
covers portfolio and architecture,
[Chapter 03](chapters/03-management-network-ipv4-ipv6-dns-ntp-and-connectivity.md)
the 6% networking domain,
[Chapter 04](chapters/04-identity-certificates-security-and-compliance.md)
security, and [Chapter 08](chapters/08-firmware-idrac-bios-lifecycle-controller-and-platform-updates.md)
maintenance.

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
