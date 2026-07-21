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

| Exam | Focus | Duration |
| --- | --- | --- |
| **D-VXR-DY-01** Dell VxRail Deploy v2 | Getting from nodes in a box to a working cluster: planning, installation, initialization, and post-deployment tasks | 120 minutes |
| **D-VXR-OE-01** Dell VxRail Operate v2 | Administering a running cluster: management, monitoring, expansion, maintenance, and troubleshooting | Not stated in the exam description |

`DES-6322` *Specialist – Implementation Engineer, VxRail* is the retired
predecessor to the Deploy exam; material written against it describes an
exam that is no longer offered, though much of its technical content
remains sound.

Note that the PowerEdge exams covered in
[Volume XXII](../volume-22-dell-openmanage-enterprise/README.md) and
[Volume XXIII](../volume-23-dell-idrac-9-10-administration/README.md) are
*not* prerequisites for the VxRail exams, but the hardware knowledge they
validate is assumed by them.

### Domain weights, mapped to this volume

Both sets of weights below are transcribed from Dell's published exam
description PDFs, which are the controlling source. Dell states that each
percentage "reflects the approximate distribution of the total question
set across the exam" — they are question-count proportions, not scoring
weights.

**D-VXR-DY-01 Deploy v2** — ten domains, summing to 100%:

| Domain | Weight | Chapters |
| --- | --- | --- |
| Deploying the VxRail Cluster | **24%** | [03](chapters/03-vxrail-manager-deployment-and-first-run-configuration.md) |
| VxRail Post-Deployment procedures | **18%** | [03](chapters/03-vxrail-manager-deployment-and-first-run-configuration.md), [04](chapters/04-vsphere-and-vsan-integration-and-the-division-of-management.md), [07](chapters/07-availability-stretched-clusters-and-data-protection.md) |
| VxRail Deployment Planning | 12% | [01](chapters/01-hci-architecture-vxrail-positioning-and-platform-models.md), [02](chapters/02-physical-installation-network-prerequisites-and-pre-deployment-planning.md) |
| VxRail Cluster Upgrade and Expansion | 10% | [05](chapters/05-cluster-expansion-scale-out-and-capacity-planning.md), [06](chapters/06-lifecycle-management-and-the-continuously-validated-state.md) |
| VxRail Hardware Installation and Initialization | 8% | [02](chapters/02-physical-installation-network-prerequisites-and-pre-deployment-planning.md) |
| VxRail Network Environment Requirements and Initialization | 8% | [02](chapters/02-physical-installation-network-prerequisites-and-pre-deployment-planning.md) |
| VxRail Troubleshooting | 6% | [09](chapters/09-day-2-operations-troubleshooting-support-and-capstone.md) |
| VxRail REST API | 6% | [08](chapters/08-vxrail-api-automation-and-ecosystem-integrations.md) |
| VxRail Physical Components | 4% | [01](chapters/01-hci-architecture-vxrail-positioning-and-platform-models.md), [02](chapters/02-physical-installation-network-prerequisites-and-pre-deployment-planning.md) |
| Using VxRail Configuration Tools | 4% | *Not covered — see below* |

**D-VXR-OE-01 Operate v2** — six domains:

| Domain | Weight | Chapters |
| --- | --- | --- |
| Manage the VxRail | **35%** | [04](chapters/04-vsphere-and-vsan-integration-and-the-division-of-management.md), [07](chapters/07-availability-stretched-clusters-and-data-protection.md) |
| Perform Maintenance and Troubleshooting | **20%** | [06](chapters/06-lifecycle-management-and-the-continuously-validated-state.md), [09](chapters/09-day-2-operations-troubleshooting-support-and-capstone.md) |
| VxRail Building blocks | 13% | [01](chapters/01-hci-architecture-vxrail-positioning-and-platform-models.md), [04](chapters/04-vsphere-and-vsan-integration-and-the-division-of-management.md) |
| Perform Additional Administrative Tasks | 13% | [03](chapters/03-vxrail-manager-deployment-and-first-run-configuration.md), [04](chapters/04-vsphere-and-vsan-integration-and-the-division-of-management.md), [07](chapters/07-availability-stretched-clusters-and-data-protection.md) |
| Perform Cluster Expansion and Contraction | 10% | [05](chapters/05-cluster-expansion-scale-out-and-capacity-planning.md), [09](chapters/09-day-2-operations-troubleshooting-support-and-capstone.md) |
| VxRail Appliance REST API | 10% | [08](chapters/08-vxrail-api-automation-and-ecosystem-integrations.md) |

**The Operate weights sum to 101%, not 100%.** That is what the published
document says; it is a rounding artifact of "approximate distribution"
and not a transcription error here. Do not read significance into it, and
do not expect the arithmetic to close.

**Read the concentration before planning time.** On Deploy, the two
largest domains — deploying the cluster and post-deployment procedures —
are **42% together**, and both are Chapter 03 territory. On Operate, a
single domain, *Manage the VxRail*, is **35%** on its own, more than
twice the next largest, and it is almost entirely vSAN administration:
health, capacity, performance, services, storage policies, HCI Mesh, and
cluster availability. A candidate who studies VxRail Manager thoroughly
and vSAN lightly has misread this exam.

### Where this volume does not cover the blueprint

Stated plainly, because a study plan that hides its gaps is worse than
one that admits them:

- **Using VxRail Configuration Tools (4% of Deploy)** — the VxRail
  Configuration Portal, used to build and validate a configuration
  project before deployment, is not covered in this volume at all.
  [Chapter 02](chapters/02-physical-installation-network-prerequisites-and-pre-deployment-planning.md)
  produces an equivalent planning record by hand, which teaches the same
  decisions but not the tool the exam asks about. Cover this from Dell's
  planning course.
- **vSAN HCI Mesh** — named explicitly under Operate's largest domain,
  and reached here only obliquely through dynamic nodes in Chapter 02.
- **SolVe procedure generation** — named in Operate's expansion domain.
  [Chapter 09](chapters/09-day-2-operations-troubleshooting-support-and-capstone.md)
  refers to Dell's procedure-generation resources without working
  through SolVe itself.
- **VxRail Manager file-based backup, password management, and power
  control operations** — all named under Operate's maintenance domain.
  Chapter 07 covers workload and vCenter backup; Chapter 09 covers
  troubleshooting and support. The VxRail-appliance-specific procedures
  are not stepped through.

Together these account for roughly 4% of Deploy and a meaningful slice of
Operate's 35% and 20% domains. This volume is not a substitute for the
recommended training on those points.

### A version gap to plan around

The exam descriptions name **VxRail 8.0.XXX, vSphere 8.0, vSAN 8.0, and
vCenter 8.0**. This volume's baseline in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md) tracks the current
vSphere 9.x line, and
[Volume V](../volume-05-vmware-virtualization/README.md) is written to it.

That gap is real and runs in the awkward direction: the encyclopedia is
*ahead* of the exam. Where a vSphere 9 behavior differs from vSphere 8,
the exam tests the 8 behavior. The Deploy blueprint's explicit mention of
initialization *with vSAN ESA* is the clearest instance — know the
express storage architecture as VxRail 8.0 presents it, not only as the
current vSAN documentation describes it.

### Study plan

Six to eight weeks per exam for a candidate with working vSphere
experience, assuming eight to ten hours a week. Without vSphere
experience, work
[Volume V](../volume-05-vmware-virtualization/README.md) first — these
exams assume it rather than teach it, and no amount of VxRail study
substitutes.

**D-VXR-DY-01 Deploy — weeks 1–6**

| Week | Focus | Weight covered |
| --- | --- | --- |
| 1 | Architecture, physical components, node models, positioning. Chapter 01 and its sizing lab. | 4% + part of 12% |
| 2 | Deployment planning end to end: networks, discovery, DNS, vSAN options, vCenter topology. Chapter 02. | 12% |
| 3 | Hardware installation, iDRAC and time configuration, network environment validation. Chapter 02 labs, plus [Volume XXIII Chapter 03](../volume-23-dell-idrac-9-10-administration/chapters/03-management-network-ipv4-ipv6-dns-ntp-and-connectivity.md). | 16% |
| 4–5 | **The heavy weeks.** Cluster initialization in all three variants — VxRail-managed vCenter, customer-managed vCenter, and vSAN ESA — then post-deployment validation, vSAN settings, and native backups. Chapters 03, 04, 07. | 42% |
| 6 | Upgrade and expansion, troubleshooting, REST API. Chapters 05, 06, 08, 09. Then the Configuration Portal from Dell's planning course, which this volume does not cover. | 22% + the 4% gap |

**D-VXR-OE-01 Operate — weeks 1–6**

| Week | Focus | Weight covered |
| --- | --- | --- |
| 1 | Building blocks: cluster architecture, deployment options, validating vSAN configuration. Chapters 01 and 04. | 13% |
| 2–3 | **The heavy weeks.** *Manage the VxRail* in full: the vCenter plugin, vSAN health, capacity and performance monitoring, vSAN services, storage policies, HCI Mesh, and cluster availability. Chapters 04 and 07, with [Volume V Chapter 06](../volume-05-vmware-virtualization/chapters/06-vsphere-storage-and-vsan.md) alongside. | 35% |
| 4 | Maintenance and troubleshooting: file-based backup, software upgrade, basic troubleshooting, password management, power control. Chapters 06 and 09. | 20% |
| 5 | Expansion and contraction including SolVe, plus additional administrative tasks — networking, stretched clusters, certificates. Chapters 05, 03, 07. | 23% |
| 6 | REST API, then the practice test, then targeted revision on whatever it exposes. Chapter 08. | 10% |

**Take the practice test before you think you are ready, not after.**
Dell publishes one for Operate (`D-VXR-OE-P-01`), and its value is
diagnostic rather than confirmatory — a passing practice score does not
guarantee a passing exam score, as Dell states directly. Used in week 4
rather than week 6, it redirects study while there is still time to
redirect it.

### Study materials

Dell's recommended training, transcribed from the exam descriptions with
course numbers so they can be found in the catalogue. These are paid,
commercial courses.

**For D-VXR-DY-01 Deploy** — all on-demand:

| Course | Number |
| --- | --- |
| VxRail 8.0.XXX Concepts | `ESCPXD05504` |
| VxRail 8.0.XXX Planning | `ESCPXD07957` |
| VxRail 8.0.XXX Installation | `ESCPXD05509` |
| VxRail 8.0.XXX Implementation | `ESCPXD05510` |
| VxRail 8.0.XXX Implementation: On Demand Lab | `ESCPXD05512` |
| VxRail 8.0.XXX Feature — REST API | `ESCPXD05505` |

**For D-VXR-OE-01 Operate** — Dell offers two routes:

| Option | Course | Number | Mode | Duration |
| --- | --- | --- | --- | --- |
| 1 | VxRail 8.0.XXX Administration | `ESCPXD06622` | On demand | 9h |
| 1 | VxRail 8.0.XXX Administration: On Demand Lab | `ESCPXD06623` | On-demand lab | 9h |
| 1 | VxRail 8.0.XXX Feature: REST API | `ESCPXD05505` | On demand | 2h |
| 2 | VxRail Administration | `ES124CPX00078` | Classroom / virtual classroom | 24h |
| 2 | VxRail 8.0.XXX Feature: REST API | `ESCPXD05505` | On demand | 2h |

**The on-demand labs are the ones worth paying for.** Given that VxRail
has no free or virtual edition — see *Practicing* below — `ESCPXD05512`
and `ESCPXD06623` are, for a candidate without employer hardware, the
only realistic route to touching VxRail Manager at all. The lecture
courses cover material this volume also covers; the labs cover what it
cannot.

**Currency warning.** The Deploy description is dated 10 May 2024 and the
Operate description carries an unfilled placeholder where its date should
be, reading "as of Date exam is being published". Course numbers and
weights both drift. Confirm against
[Dell Learning](https://learning.dell.com/content/dell/en-us/home/certification-overview.html)
at registration rather than trusting this table.

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
