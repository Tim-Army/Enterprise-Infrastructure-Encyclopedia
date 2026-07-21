# Volume XXIV — Dell VxRail Hyperconverged Infrastructure

> Deploying and operating Dell VxRail as a jointly engineered
> hyperconverged platform: HCI architecture and platform models, VxRail
> Manager and first run, physical and network prerequisites, vSphere and
> vSAN integration, scale-out, lifecycle management, availability and
> stretched clusters, automation, and day-2 operations.

## Overview

Volume XXIV covers Dell VxRail, the hyperconverged infrastructure
appliance jointly engineered by Dell and Broadcom/VMware. VxRail is not
simply PowerEdge hardware running vSphere: it is a integrated system in
which the hardware, the hypervisor, vSAN, and the management layer are
version-locked together and lifecycle-managed as one unit through VxRail
Manager. That single design decision — the *continuously validated state*
— is what distinguishes VxRail from a build-your-own vSphere cluster on
PowerEdge, and it shapes nearly every operational procedure in this
volume.

This volume sits at the intersection of three others and assumes them
rather than repeating them:

- **[Volume V — VMware Virtualization](../volume-05-vmware-virtualization/README.md)**
  is the primary dependency. VxRail runs vSphere and vSAN underneath, and
  this volume assumes the ESXi, vCenter, cluster services, and vSAN
  material from Volume V rather than re-teaching it. Where VxRail changes
  how a vSphere operation must be performed — and it frequently does —
  the chapter says so explicitly and explains why.
- **[Volume XXII — Dell OpenManage Enterprise](../volume-22-dell-openmanage-enterprise/README.md)**
  and
  **[Volume XXIII — Dell iDRAC 9 and 10 Administration](../volume-23-dell-idrac-9-10-administration/README.md)**
  cover the PowerEdge management layer beneath VxRail. VxRail Manager
  orchestrates against iDRAC in much the way OpenManage Enterprise does,
  and the hardware-layer troubleshooting in Volume XXIII applies directly
  when a VxRail node fails.
- **[Volume VI — Enterprise Storage and Data Protection](../volume-06-enterprise-storage-data-protection/README.md)**
  supplies the storage design vocabulary the vSAN chapters assume.

The volume is organized in the order a VxRail cluster is actually
delivered and then operated:

- **Chapters 01–03** establish what VxRail is and get a cluster to first
  boot: HCI architecture and where VxRail sits among the alternatives,
  the platform and node models, VxRail Manager's role, physical
  installation, and the network prerequisites that must be correct
  *before* deployment because they are painful to change afterwards.
- **Chapters 04–05** cover the virtualization layer as VxRail presents
  it — vSphere and vSAN integration, and what VxRail manages on your
  behalf versus what remains yours — followed by cluster expansion,
  scale-out, and capacity planning.
- **Chapters 06–07** cover the two areas where VxRail differs most from
  a self-built cluster: lifecycle management against the continuously
  validated state, and availability design including stretched clusters
  and data protection.
- **Chapters 08–09** cover automation through the VxRail API and
  ecosystem integrations, then close with day-2 operations, a structured
  troubleshooting methodology, support engagement, and a capstone that
  exercises the whole platform.

Every chapter follows the same structure — learning objectives, theory
and architecture, design considerations, implementation and automation,
validation and troubleshooting, security and best practices, references
and knowledge checks, a hands-on lab, and a summary and completion
checklist — defined in [templates/chapter.md](../../templates/chapter.md)
and enforced by [EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md).

**A note on labs in this volume.** VxRail is an appliance platform with
no free or virtual edition, which constrains what a reproducible lab can
be. Where a procedure requires real VxRail hardware, the chapter says so
plainly and provides the closest honest substitute — usually a nested
vSphere and vSAN environment that exercises the same underlying
mechanism without VxRail Manager. See *Practicing* below; this
constraint is stated rather than worked around.

## Chapters

1. [HCI Architecture, VxRail Positioning, and Platform Models](chapters/01-hci-architecture-vxrail-positioning-and-platform-models.md) — what hyperconverged infrastructure actually consolidates, where VxRail sits against build-your-own vSphere and vSAN ReadyNodes, the jointly engineered model and the continuously validated state, node series and platform profiles, and the support boundary.
2. [Physical Installation, Network Prerequisites, and Pre-Deployment Planning](chapters/02-physical-installation-network-prerequisites-and-pre-deployment-planning.md) — the networks a cluster requires, IPv6 multicast node discovery, switch configuration and MTU, DNS and NTP preparation, node minimums and cluster types, and the deployment planning record.
3. [VxRail Manager Deployment and First-Run Configuration](chapters/03-vxrail-manager-deployment-and-first-run-configuration.md) — the six stages of first run, reaching the initialization interface, the vCenter topology decision at the point it becomes irreversible, reading validation failures, and post-deployment verification and baselining.
4. [vSphere and vSAN Integration and the Division of Management](chapters/04-vsphere-and-vsan-integration-and-the-division-of-management.md) — what VxRail owns versus what remains yours, storage policies and their capacity consequences, cluster services under VxRail's constraints, and the operations that are routine on vSphere and unsupported here.
5. [Cluster Expansion, Scale-Out, and Capacity Planning](chapters/05-cluster-expansion-scale-out-and-capacity-planning.md) — node addition stage by stage, version reconciliation, matching a shortage to the right remedy, capacity planning from raw to genuinely usable, and node removal preconditions.
6. [Lifecycle Management and the Continuously Validated State](chapters/06-lifecycle-management-and-the-continuously-validated-state.md) — what the bundle contains and why it is applied whole, the rolling upgrade sequence and realistic window estimation, connected and offline paths, pre-checks, and detecting drift between upgrades.
7. [Availability, Stretched Clusters, and Data Protection](chapters/07-availability-stretched-clusters-and-data-protection.md) — why availability, replication, and backup are three different things, fault domains, two-node clusters and witness placement, stretched cluster requirements and costs, and validating recovery rather than backup.
8. [VxRail API, Automation, and Ecosystem Integrations](chapters/08-vxrail-api-automation-and-ecosystem-integrations.md) — the two APIs and which owns what, asynchronous write operations and idempotent design, REST/Ansible/PowerCLI surfaces, drift detection, and call-home and fabric integrations.
9. [Day-2 Operations, Troubleshooting, Support, and Capstone](chapters/09-day-2-operations-troubleshooting-support-and-capstone.md) — daily, weekly, and quarterly operational cadences, the six-layer troubleshooting sequence, drive and node failure handling, engaging Dell support effectively, and a capstone spanning the whole volume.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across this volume.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.

## Related volumes

- **Volume V — VMware Virtualization** — primary dependency; vSphere,
  vCenter, and vSAN fundamentals this volume assumes throughout.
- **Volume XXII — Dell OpenManage Enterprise** — fleet management for
  PowerEdge, whose orchestration model parallels VxRail Manager's.
- **Volume XXIII — Dell iDRAC 9 and 10 Administration** — the per-node
  management controller beneath every VxRail node.
- **Volume VI — Enterprise Storage and Data Protection** — storage
  architecture and data-protection patterns underlying the vSAN chapters.

## Certification alignment

Dell certifies VxRail separately from PowerEdge, in the **Dell
Technologies Proven Professional** program recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). Two
exams are current:

| Exam | Focus |
| --- | --- |
| **D-VXR-DY-01** VxRail Deploy | Architecture, installation workflow, configuration, and post-deployment tasks |
| **D-VXR-OE-01** VxRail Operate | Day-2 operations, lifecycle management, and troubleshooting |

`DES-6322` *Specialist – Implementation Engineer, VxRail* is the retired
predecessor to the Deploy exam; material written against it describes an
exam that is no longer offered, though much of its technical content
remains sound.

Domain weights are not restated here until each exam description has
been read directly — the practice this encyclopedia follows for every
other vendor. Confirm current exam codes, weights, and mechanics against
Dell Learning before planning a study timeline.

Note that the PowerEdge exams covered in
[Volume XXII](../volume-22-dell-openmanage-enterprise/README.md) and
[Volume XXIII](../volume-23-dell-idrac-9-10-administration/README.md) are
*not* prerequisites for the VxRail exams, but the hardware knowledge they
validate is assumed by them.

## Practicing

**VxRail has no free, trial, or virtual edition.** There is no nested
VxRail, no evaluation appliance, and no hosted sandbox. VxRail Manager
expects the jointly engineered hardware it was built for, and the
continuously validated state is meaningless without it. This is the most
constrained practice environment of any volume in this encyclopedia —
more so than iDRAC, which at least runs on second-hand hardware within
reach of an individual.

Three routes exist, in descending order of fidelity:

| Route | What it gives you |
| --- | --- |
| Employer or partner hardware | The only way to exercise VxRail Manager, lifecycle upgrades, and the deployment workflow as they actually behave |
| Dell demo and lab environments | Dell provides guided environments through its partner and customer programs; access depends on your organization's relationship |
| Nested vSphere and vSAN | Free and reachable, and genuinely useful for Chapters 04–05 and 07 — but it teaches the layer *beneath* VxRail, not VxRail itself |

**Be clear about what the substitute teaches.** A nested vSphere and vSAN
cluster will exercise storage policies, cluster services, availability
behavior, and stretched-cluster concepts faithfully, because those are
vSphere mechanisms VxRail inherits. It will teach you nothing about
VxRail Manager, the lifecycle bundle, or the validated-state model —
which is precisely the material the Deploy and Operate exams weight most
heavily, and precisely what distinguishes this volume from Volume V.

A reader without VxRail access should treat Chapters 04, 05 and 07 as
lab-backed and the remainder as reading, and should be honest with
themselves that reading is not preparation for a deployment exam.

## Software and platform baseline

Chapters in this volume reference the dated baseline recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md). VxRail releases are
version-locked to specific vSphere and vSAN releases by design, so the
baseline names the VxRail version and the vSphere release it carries
rather than treating them independently. Update that file, not individual
chapters, when the baseline changes.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-24-dell-vxrail-hci
```
