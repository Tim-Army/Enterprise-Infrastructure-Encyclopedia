# Volume XXII — Dell OpenManage Enterprise

> One-to-many systems management for the Dell PowerEdge fleet: appliance
> architecture and deployment, identity and licensing, discovery and
> inventory, monitoring and alerting, firmware and driver lifecycle
> management across connected and air-gapped environments, configuration
> templates, and appliance operations.

## Overview

Volume XXII covers Dell OpenManage Enterprise (OME), Dell's virtual
appliance-based console for fleet-scale discovery, inventory, monitoring,
firmware and driver lifecycle management, configuration templating, and
compliance reporting across PowerEdge rack and tower servers. OME
orchestrates against each server's individual out-of-band management
controller (iDRAC, covered in depth in Volume XXIII) at scale rather than
replacing it; this volume treats OME as the aggregation and automation
layer, and assumes no prior familiarity with Dell systems management
beyond general infrastructure administration experience.

The volume is organized to follow the natural lifecycle of standing up
and operating an OME deployment:

- **Chapter 1** deploys the appliance and completes first-run
  configuration, establishing the architectural foundation — the
  appliance, its embedded database and job engine, and its plugin
  framework — that every later chapter builds on.
- **Chapter 2** establishes identity, licensing, security, and delegated
  administrative control before any devices are onboarded.
- **Chapter 3** brings the managed fleet under control: discovery,
  onboarding, inventory, device grouping, and device-control operations.
- **Chapter 4** covers monitoring, the alert pipeline, custom reporting,
  the job engine, and operational integrations including SupportAssist.
- **Chapters 5–7** cover the firmware and driver lifecycle in depth: the
  catalog/baseline/compliance/update model (Chapter 5), Dell's connected
  online repository workflow (Chapter 6), and fully offline, air-gapped
  repository workflows built on Dell Repository Manager (Chapter 7).
- **Chapter 8** extends the same baseline-and-compliance pattern from
  firmware to server configuration through deployment templates,
  configuration compliance, and fleet-scale REST API automation patterns.
- **Chapter 9** closes the volume with appliance backup, restore, upgrade,
  troubleshooting, and a capstone lab that exercises discovery,
  monitoring, firmware compliance, and appliance operations together as a
  single operational workflow.

Every chapter follows the same structure — learning objectives, theory
and architecture, design considerations, implementation and automation,
validation and troubleshooting, security and best practices, references
and knowledge checks, a hands-on lab, and a summary and completion
checklist — defined in [templates/chapter.md](../../templates/chapter.md)
and enforced by [EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md).
Each hands-on lab is a reproducible, disposable exercise with a stated
objective, prerequisites, numbered steps, expected results, a negative
test, and cleanup instructions; where a lab step depends on a real or
virtual PowerEdge/iDRAC target, the chapter says so explicitly and
provides a protocol-appropriate lab substitute (for example, an
SNMP-managed Linux host standing in for a third-party device) so the
core mechanics remain reproducible without requiring Dell hardware.

## Chapters

1. [Architecture, Requirements, Deployment, and First Configuration](chapters/01-architecture-requirements-deployment-and-first-configuration.md) — where OME fits relative to iDRAC and OME-Modular, appliance internals, sizing, deployment, and the first-run setup wizard.
2. [Identity, Licensing, Security, and Administrative Control](chapters/02-identity-licensing-security-and-administrative-control.md) — local and directory identity, role-based access control and scope, licensing tiers, TLS certificates, and login security.
3. [Discovery, Onboarding, Inventory, Groups, and Device Control](chapters/03-discovery-onboarding-inventory-groups-and-device-control.md) — discovery protocols by device class, credential profiles, static and dynamic groups, inventory collection, and device-control actions.
4. [Monitoring, Alerts, Reports, Jobs, and Operational Integrations](chapters/04-monitoring-alerts-reports-jobs-and-operational-integrations.md) — health status roll-up, the alert pipeline, custom reporting, the job engine, and SupportAssist/SMTP/syslog integrations.
5. [Firmware and Driver Catalogs, Baselines, Compliance, and Updates](chapters/05-firmware-and-driver-catalogs-baselines-compliance-and-updates.md) — the catalog/baseline/compliance/update model, Dell Update Packages, and update job orchestration.
6. [Connected Online Repositories and Update Workflows](chapters/06-connected-online-repositories-and-update-workflows.md) — Dell's hosted catalog source, proxy and connectivity requirements, refresh scheduling, and automation.
7. [Isolated Offline Repositories and Air-Gapped Updates](chapters/07-isolated-offline-repositories-and-air-gapped-updates.md) — Dell Repository Manager, offline catalog export, secure transfer, and custom catalog hosting for disconnected environments.
8. [Templates, Configuration Compliance, Automation, and APIs](chapters/08-templates-configuration-compliance-automation-and-apis.md) — configuration templates, Server Configuration Profiles, attribute pruning, configuration compliance, and fleet-scale REST API patterns.
9. [Backup, Restore, Upgrade, Troubleshooting, and Capstone Operations](chapters/09-backup-restore-upgrade-troubleshooting-and-capstone-operations.md) — appliance backup and restore, upgrade planning, diagnostics, cross-chapter troubleshooting, and a capstone operational lab.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine
  chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.

## Related volumes

- **Volume XXIII — Dell iDRAC 9 and 10 Administration** covers the
  per-server out-of-band management controller that OME orchestrates
  against at scale; this volume treats iDRAC as a discovery and update
  target and does not duplicate iDRAC's own administration in depth.
- **Volume I — Enterprise Engineering Foundations** covers the general
  automation, documentation, and lifecycle-management practices this
  volume applies specifically to OME.
- **Volume VI — Enterprise Storage and Data Protection** covers backup
  and data-protection patterns for the workloads running on the servers
  OME manages, distinct from the appliance-level backup covered in
  Chapter 9.

## Certification alignment

Dell's server certifications sit in the **Dell Technologies Proven
Professional** program, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). Two
exams cover this volume's material, and both span it and
[Volume XXIII](../volume-23-dell-idrac-9-10-administration/README.md):

| Exam | Level | Duration | Questions |
| --- | --- | --- | --- |
| **D-PE-FN-01** PowerEdge Foundations v2 | Foundational | 90 min | Not stated in the exam description |
| **D-PE-OE-01** PowerEdge Operate v2 | Specialist | 90 min | 50 |

Both are delivered through Pearson VUE. Operate v2 is offered in English,
French, and Japanese.

**`D-PE-OE-23` PowerEdge Operate 2023 has been superseded by
`D-PE-OE-01`**, and the blueprint was rebuilt rather than renumbered. See
[Volume XXIII](../volume-23-dell-idrac-9-10-administration/README.md#certification-alignment)
for the full weights of both exams, the domain-to-chapter mapping across
the pair, the study plan, and Dell's recommended courses — that volume
carries the heavier share of both blueprints, so the combined walkthrough
lives there rather than being split across two files.

### What the exams ask of *this* volume

OpenManage Enterprise sits inside **Server Management**, worth 22% of
Operate v2 and 14% of Foundations, alongside iDRAC, the Lifecycle
Controller, RACADM, iSM, and OMSA. OME is one item in a list.

| Operate v2 domain | Weight | Chapters here | In Volume XXIII |
| --- | --- | --- | --- |
| Server Management | 22% | 01–04, 08 | 01, 05, 07, 09 |
| Troubleshooting | 22% | 09 | 02, 06 |
| Server Monitoring | 20% | 04 | 06 |
| System Administration | 20% | 02, 03 | 04, 05 |
| Server Maintenance | 16% | 05, 06, 07 | 08 |

**This volume goes considerably deeper than either exam requires.** A
reader working it end to end will be far past what the exams ask about
OME specifically. That is not wasted effort — it is the daily work of
managing a fleet — but a candidate optimizing purely for exam pass should
weight Volume XXIII more heavily than the chapter count here suggests.

**The v2 rewrite did not change that conclusion, though it changed the
reasoning.** Under the superseded 2023 blueprint the argument was
lopsidedness: troubleshooting at 32% plus server components at 26% put
well over half the exam in hardware territory. Under v2 the spread is
only six percentage points across five domains, so the case is no longer
that one area dominates — it is that four of the five domains
(management, troubleshooting, monitoring, and system administration, 84%
together) are anchored in per-server work rather than fleet workflows.
Same recommendation, different arithmetic.

### Practicing

The OpenManage Enterprise appliance is a **free download** from Dell
Support and runs on any supported hypervisor — including Proxmox VE 9.0+,
which [Chapter 01](chapters/01-architecture-requirements-deployment-and-first-configuration.md)
covers. That makes this volume unusually cheap to practice: no
entitlement is needed to stand up the console itself.

What costs money is the fleet underneath it. Dell publishes **trial
licenses for iDRAC, OpenManage Enterprise, the OpenManage Integration
for Windows Admin Center, and DPAT**, which is the practical route to
exercising licensed features without buying them. Without any PowerEdge
hardware, the console can still be deployed, configured, secured, and
explored end to end — discovery and inventory are where a lab without
servers stops.

## Software and platform baseline

Chapters in this volume reference the dated baseline recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md): Dell OpenManage
Enterprise 4.7.x. UI paths, exact API field names, and licensing tier
boundaries have shifted across OME releases; where a chapter's guidance
depends on a build-specific detail, it says so explicitly and points to
validating the current behavior against your appliance's own console and
API reference rather than treating any single screenshot or field name as
timeless. Update `SOFTWARE_VERSIONS.md`, not individual chapters, when the
baseline changes.

## Building and validating this volume

From the repository root, after completing
[SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-22-dell-openmanage-enterprise

# Build a single chapter.
scripts/bash/build-book.sh --format all \
  --chapter volumes/volume-22-dell-openmanage-enterprise/chapters/05-firmware-and-driver-catalogs-baselines-compliance-and-updates.md
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
