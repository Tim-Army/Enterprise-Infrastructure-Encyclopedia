# Chapter 15: VCP VMware vSphere Foundation Administrator 2V0-16.25 Exam Preparation

![Lab flow for this chapter: four timed build steps reuse earlier chapters' procedures as one continuous exercise — 3 ESXi hosts plus vCenter Server with a Host Profile (target 30 minutes), a VDS with a tagged port group (20 minutes), vSAN with a RAID-1 FTT=1 policy and compliant test VM (25 minutes), and HA admission control plus DRS Fully Automated (20 minutes). Two timed negative tests follow: a host placed in maintenance mode with no data migration while the test VM has replica components on it, diagnosing the resulting reduced-redundancy state (15 minutes), and induced CPU contention diagnosed via esxtop percent-RDY (15 minutes). Total elapsed time under 2 hours, achieved largely unaided, is a strong readiness signal.](../../../diagrams/volume-05-vmware-virtualization/chapter-15-vvf-admin-timed-self-assessment-flow.svg)

*Figure 15-1. Flow used throughout this chapter's Hands-On Lab: a timed, combined vSphere/vSAN/HA-DRS build exercise culminating in two diagnostic negative tests.*

## Learning Objectives

- Map the 2V0-16.25 blueprint's fundamentals, design, deploy/configure/
  operate, and troubleshoot/optimize domains directly to Chapters 1
  through 9 of this volume.
- Explain how VMware vSphere Foundation (VVF) differs in scope from full
  VMware Cloud Foundation (VCF), and why this exam draws almost entirely
  on standalone vSphere/vSAN competency rather than NSX or SDDC Manager
  orchestration.
- Build a study plan weighted toward this volume's core vSphere chapters,
  since VVF administration is substantially the same skill set as
  standalone vSphere administration.
- Practice esxtop-based performance troubleshooting and DRS/HA
  optimization as the exam's most distinctive troubleshoot/optimize
  emphasis.
- Complete a comprehensive readiness lab spanning deployment, design
  judgment, and performance troubleshooting across a vSAN-backed cluster.

## Theory and Architecture

This chapter is study and review material for the **VMware Certified
Professional – VMware vSphere Foundation Administrator (VCP-VVF
Administrator), exam 2V0-16.25**. Confirm current domain names, item
count, and exam duration against Broadcom's published exam guide before
relying on this chapter — it organizes this volume's content against the
publicly published blueprint structure; it does not reproduce the
blueprint or any exam content.

### VVF scope versus VCF scope

[Chapter 1](01-vmware-virtualization-architecture-and-design.md) defined **VMware vSphere Foundation (VVF)** as the lighter SDDC
bundle: vSphere and vSAN for compute and storage, positioned for
organizations wanting an HCI-based private cloud without the full
NSX-based network virtualization and SDDC Manager-driven multi-domain
lifecycle automation VCF provides. This scope difference is the single
most important fact shaping how to prepare for this exam relative to
Chapters 13 and 14: **the VVF Administrator exam is, in substance, a
standalone vSphere and vSAN administration exam.** Its blueprint does not
carry the NSX-heavy content of [Chapter 12](12-vcp-network-virtualization-2v0-41-24-exam-preparation.md), nor the SDDC
Manager/fleet-orchestration content of Chapters 13–14 — it draws almost
entirely on the same competencies this volume's Chapters 1 through 9
already build for standalone vSphere deployments.

### Blueprint domain structure and its direct chapter mapping

- **Foundational/standards section** — general infrastructure and
  industry-standard concepts, maps to [Chapter 1](01-vmware-virtualization-architecture-and-design.md)'s virtualization
  fundamentals and [Chapter 4](04-vsphere-virtual-networking.md)'s general networking concepts.
- **VVF fundamentals section** — vSphere Foundation platform
  architecture: the roles of ESXi hosts, the vCenter Server Appliance,
  and how they interact. Maps directly to [Chapter 1](01-vmware-virtualization-architecture-and-design.md) (architecture) and
  the relationship between Chapters 2 (ESXi) and 3 (vCenter Server).
- **Plan and design section** — sizing ESXi hosts, designing vSAN
  clusters (minimum host counts, disk group configuration under OSA, or
  the simplified ESA model), planning network topology (VSS versus VDS,
  VLAN trunking, NIC teaming), and designing HA/DRS clusters. Maps
  directly to the Design Considerations sections of Chapters 4, 5, 6, and
  7.
- **Deploy, configure, and operate section** — the hands-on
  administration workload: host installation and configuration
  ([Chapter 2](02-esxi-installation-configuration-and-host-operations.md)), vCenter Server deployment ([Chapter 3](03-vcenter-server-deployment-identity-and-recovery.md)), virtual networking
  ([Chapter 4](04-vsphere-virtual-networking.md)), VM lifecycle and resource management ([Chapter 5](05-virtual-machine-lifecycle-and-resource-management.md)), storage
  and vSAN ([Chapter 6](06-vsphere-storage-and-vsan.md)), and availability/mobility services ([Chapter 7](07-vsphere-availability-mobility-and-cluster-services.md)).
  This is typically the largest-weighted section on administrator-focused
  VMware exams and rewards actual lab repetition across all of these
  chapters, not any single one in isolation.
- **Troubleshoot and optimize section** — esxtop-based performance
  analysis for CPU, memory, storage, and network bottlenecks;
  troubleshooting HA failover behavior; resolving vSAN health warnings;
  fixing vMotion failures; and optimizing DRS recommendations. Maps
  directly to the Validation and Troubleshooting sections of Chapters 5,
  6, 7, and 9.

### Why esxtop and DRS/HA optimization deserve extra attention

Among the domains above, esxtop interpretation and DRS/HA tuning are the
most distinctive to the troubleshoot/optimize section and the most likely
to be under-practiced by a reader who has only read this volume's
chapters rather than actually driven contention scenarios in a lab.
[Chapter 9](09-vsphere-lifecycle-automation-observability-and-troubleshooting.md)'s esxtop coverage and [Chapter 5](05-virtual-machine-lifecycle-and-resource-management.md)/7's DRS/HA design and
troubleshooting sections are the specific grounding for this domain;
treat the timed lab drills in this chapter's Hands-On Lab (which reuse
those chapters' scenarios) as the highest-leverage preparation activity
for this specific section.

## Design Considerations

- **Recognize the scope overlap and prepare efficiently.** Because VVF
  administration substantially equals standalone vSphere/vSAN
  administration, a reader who has completed the hands-on labs in
  Chapters 2 through 9 of this volume has already done the large majority
  of this exam's practical preparation — the incremental study need is
  narrower than for Chapters 12–14, and should focus on filling specific
  gaps (esxtop fluency, DRS/HA edge-case reasoning) rather than starting
  from scratch.
- **Design-domain judgment across multiple chapters simultaneously.**
  The plan/design section spans host sizing, vSAN cluster design, network
  topology, and HA/DRS design as a combined judgment exercise — practice
  scenarios that require reasoning across more than one of these at once
  (for example, a vSAN cluster's minimum host count interacting with HA
  admission control's failure-tolerance requirement), since the exam
  tests integrated design judgment, not each topic in isolation.
- **Deploy/configure/operate breadth over depth in any single area.**
  Given this section's likely largest weighting, prioritize broad,
  working competency across host install, vCenter deployment, networking,
  VM lifecycle, and storage/vSAN configuration over exhaustive depth in
  only one — an administrator exam rewards operational breadth.
- **esxtop fluency as a distinct, practiced skill.** Reading esxtop
  output correctly (distinguishing `%RDY` CPU contention from a
  guest-reported CPU problem, distinguishing storage-path latency from
  array-side latency using `DAVG`/`KAVG`) is a skill that requires actual
  screen-time with the tool under real or synthetic contention, not just
  reading [Chapter 9](09-vsphere-lifecycle-automation-observability-and-troubleshooting.md)'s description of it.
- **vSAN health warning literacy.** Practice recognizing common Skyline
  Health findings ([Chapter 6](06-vsphere-storage-and-vsan.md)) and mapping each to its likely root cause
  category (network, disk, cluster, data) as a fast-recognition skill,
  since the troubleshoot/optimize section rewards quick, correct
  categorization over exhaustive diagnostic depth on any single finding.

## Implementation and Automation

### Building a domain-mapped study tracker

```text
# Example self-assessment tracker for the VVF administrator-exam's domain structure

Domain                                  | Grounding chapter(s) | Self-rating | Notes
------------------------------------------|-------------------------|--------------|----------------------------------
Foundational/standards                    | 1, 4                     |              | General virtualization/networking
VVF fundamentals (ESXi/vCenter roles)     | 1, 2, 3                  |              | Architecture and interaction
Host sizing and design                    | 5                        |              | Shares/reservations/limits, DRS
vSAN cluster design                       | 6                        |              | OSA/ESA, FTT, minimum host counts
Network topology design                   | 4                        |              | VSS/VDS, VLAN trunking, NIC teaming
HA/DRS cluster design                     | 7                        |              | Admission control, migration threshold
Deploy/configure: ESXi and vCenter        | 2, 3                     |              | Install, Host Profiles, VCSA deploy
Deploy/configure: networking              | 4                        |              | VDS, LACP, NIOC
Deploy/configure: VM lifecycle            | 5                        |              | Templates, snapshots, resource pools
Deploy/configure: storage/vSAN            | 6                        |              | Datastores, storage policies
Troubleshoot: esxtop performance analysis | 9                        |              | %RDY, DAVG/KAVG interpretation
Troubleshoot: HA failover                 | 7                        |              | Isolation response, admission control
Troubleshoot: vSAN health                 | 6                        |              | Skyline Health finding categories
Troubleshoot: vMotion failures            | 7                        |              | Compatibility, network, encryption
Optimize: DRS recommendations             | 5, 7                     |              | Automation level, migration threshold
```

### Re-running prior labs as a combined design-and-execution drill

```text
# Suggested combined drill: build a small vSAN-backed HA/DRS cluster from
# scratch, reusing prior chapters' lab material as a single continuous
# exercise rather than isolated repetitions

1. Chapter 2 lab steps (scripted ESXi install, Host Profile) for 3 hosts.
2. Chapter 3 lab steps (VCSA deploy, AD identity source) for the managing vCenter.
3. Chapter 4 lab steps (VDS, port groups, LACP) for cluster networking.
4. Chapter 6 lab steps (vSAN enablement, RAID-1 policy, maintenance-mode
   negative test) for the storage layer.
5. Chapter 7 lab steps (HA admission control, vMotion, FT if capacity
   allows) for availability.
6. Chapter 9 lab steps (esxtop contention observation, vLCM compliance
   check) for lifecycle/troubleshooting.
```

### Practicing esxtop interpretation under synthetic contention

```bash
# esxtop: reproduce the contention-observation drill from Chapter 9,
# specifically timing how quickly %RDY, DAVG, and KAVG can be correctly
# interpreted without reference material
esxtop
# 'c' for CPU view (%RDY), 'd' for disk adapter view (DAVG/KAVG), 'n' for network view
```

## Validation and Troubleshooting

- **Design-scenario integration self-check.** Practice scenarios that
  combine at least two design domains at once (a stated workload profile
  requiring specific host sizing *and* a specific vSAN FTT level *and* a
  compatible minimum host count) and confirm the answer holds up under
  all constraints simultaneously, not just the first one considered.
- **esxtop speed-reading drill.** Time how long it takes to correctly
  identify the bottleneck layer (CPU scheduler contention, storage path
  latency, or network) from a live esxtop session under a synthetic load
  — a competent administrator should reach a confident, correct
  diagnosis within a minute or two of observation, not require extended
  analysis.
- **HA/DRS troubleshooting rehearsal.** Deliberately misconfigure an HA
  isolation address or a DRS affinity rule with no valid host remaining
  ([Chapter 7](07-vsphere-availability-mobility-and-cluster-services.md)) and practice diagnosing the resulting symptom without
  reference material.
- **vMotion failure triage rehearsal.** Deliberately break a vMotion
  compatibility prerequisite (mismatched EVC mode, or a VM configured
  with a device not eligible for migration) and practice reading the
  resulting error message to correctly identify the specific blocking
  factor, rather than treating "vMotion failed" as a single undifferentiated
  symptom category.

## Security and Best Practices

- Register for the exam only through Broadcom's authorized testing
  partner and verify current requirements directly from official
  registration channels before exam day.
- Do not use unauthorized exam dump material; this exam's design and
  troubleshoot/optimize sections in particular test judgment and
  diagnostic reasoning that memorized answers cannot substitute for.
- Perform all deliberate-fault troubleshooting rehearsal in an isolated
  lab environment, never against production vSphere/vSAN infrastructure —
  HA isolation-response and vSAN maintenance-mode negative tests in
  particular are disruptive by design.
- Apply the RBAC and credential hygiene practices from Chapters 3 and 8
  to lab accounts used during preparation, reinforcing habits that carry
  forward into real administrative work.

## References and Knowledge Checks

**References**

- [Broadcom Education Services](https://www.broadcom.com/support/education/vmware) — official 2V0-16.25 exam guide (current
  blueprint domains, item count, exam duration, and candidate profile —
  verify directly before scheduling).
- [VMware vSphere 9.x Documentation and VMware vSAN Documentation (the
  full documentation set referenced throughout Chapters 1–9).](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-0.html)
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  this repository's certification-to-volume mapping.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — dated vSphere
  9.x / NSX 4.x baseline referenced throughout this volume.
- See [Chapter 1](01-vmware-virtualization-architecture-and-design.md) for the VVF-versus-VCF scope distinction underpinning
  this chapter's preparation strategy.
- See Chapters 2 through 9 for the direct technical grounding of every
  blueprint domain discussed above.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any Broadcom exam item)*

1. Explain, in your own words, why this exam's preparation scope is
   substantially narrower than the VCF-focused exams in Chapters 13 and
   14, in terms of what product capabilities are and are not in scope.
2. Walk through, from memory, how to correctly interpret sustained high
   `%RDY` versus sustained high `DAVG` in an esxtop session — what
   different remediation paths does each point toward?
3. Given a vSAN cluster design requirement for RAID-6 FTT=2, what is the
   minimum viable host count, and why is designing to exactly that
   minimum a design-judgment mistake in practice?
4. Name three distinct categories of vMotion failure root cause and
   explain how their error signatures differ.
5. Why does this chapter recommend practicing design scenarios that span
   multiple domains (host sizing, vSAN, HA/DRS) simultaneously rather
   than studying each domain in isolation?

## Hands-On Lab

**Objective:** Execute a combined, timed build-and-troubleshoot exercise
spanning ESXi/vCenter deployment, networking, vSAN, HA/DRS, and esxtop-
based performance troubleshooting — the full deploy/configure/operate and
troubleshoot/optimize domain set — as a realistic administrator-exam
self-assessment.

**Prerequisites**

- A nested or physical lab environment capable of hosting at least 3
  ESXi hosts and one vCenter Server, with capacity for a small vSAN
  cluster (following the [Chapter 6](06-vsphere-storage-and-vsan.md) lab's disk requirements) and at least
  one CPU-contention-capable test workload.
- Completion of (or comfort with) the individual [Chapter 2](02-esxi-installation-configuration-and-host-operations.md), 3, 4, 6, 7,
  and 9 labs, since this lab reuses their procedures as a single
  continuous exercise.

**Steps**

1. **(Timed, target 30 minutes)** Deploy or confirm 3 ESXi hosts and a
   managing vCenter Server, applying a Host Profile for configuration
   consistency (Chapters 2–3).

   **Expected result:** all 3 hosts show connected, compliant status in
   vCenter Server.

2. **(Timed, target 20 minutes)** Build a VDS, add all 3 hosts, and
   create at least one tagged port group ([Chapter 4](04-vsphere-virtual-networking.md)).

   **Expected result:** all hosts show as VDS members with consistent
   port group configuration.

3. **(Timed, target 25 minutes)** Enable vSAN, create a RAID-1 FTT=1
   storage policy, and deploy a test VM using it ([Chapter 6](06-vsphere-storage-and-vsan.md)).

   **Expected result:** the vSAN datastore is healthy and the test VM
   reports compliant against its storage policy.

4. **(Timed, target 20 minutes)** Configure HA admission control and
   confirm DRS is set to Fully Automated with an appropriate migration
   threshold ([Chapter 7](07-vsphere-availability-mobility-and-cluster-services.md)).

   **Expected result:** the cluster shows HA and DRS both enabled and
   healthy.

5. **Negative test 1 (timed, target 15 minutes):** place one host into
   maintenance mode with no data migration while the test VM's storage
   object has replica components on that host (as in the [Chapter 6](06-vsphere-storage-and-vsan.md) lab),
   and diagnose the resulting compliance/redundancy state without
   reference material.

   **Expected result:** correctly identify the reduced-redundancy
   condition and confirm the VM remains available, consistent with
   FTT=1 tolerating exactly this single-host loss.

6. **Negative test 2 (timed, target 15 minutes):** exit maintenance mode,
   then deliberately induce CPU contention (start enough synthetic
   CPU-bound VMs to exceed the cluster's logical CPU capacity) and use
   esxtop to identify and report the specific contended VMs and their
   `%RDY` values without reference material.

   **Expected result:** correctly identify CPU scheduler contention (not
   a guest-level issue) as the root cause using `%RDY`, within the time
   box.

7. Total elapsed time under 2 hours across all steps, with all expected
   results achieved largely unaided, is a strong readiness signal for the
   deploy/configure/operate and troubleshoot/optimize domains
   specifically.

8. **Cleanup:** stop and remove synthetic load VMs, remove the test VM
   and storage policy, disable vSAN if it was enabled solely for this
   lab, and remove the VDS/port groups if created solely for this
   exercise.

## Summary and Completion Checklist

The VCP-VVF Administrator (2V0-16.25) exam is, in substance, a standalone
vSphere and vSAN administration exam — its blueprint domains map almost
entirely onto Chapters 1 through 9 of this volume, without the NSX or
SDDC Manager/fleet-orchestration content covered separately in Chapters
12 through 14. Preparation should therefore focus on filling specific
gaps (esxtop fluency, integrated multi-domain design judgment, DRS/HA and
vMotion failure triage) rather than treating this as unfamiliar new
material, and the combined, timed lab in this chapter is designed to
exercise the deploy/configure/operate and troubleshoot/optimize domains
together, the way the exam's own weighting emphasizes them.

- [ ] Can explain the VVF-versus-VCF scope distinction and its
      implication for exam preparation.
- [ ] Has mapped every blueprint domain to a specific chapter and
      self-rated readiness accordingly.
- [ ] Can correctly interpret esxtop `%RDY` and `DAVG`/`KAVG` under live
      contention within a short, timed window.
- [ ] Can reason through an integrated, multi-domain design scenario
      (host sizing + vSAN + HA/DRS) without contradiction.
- [ ] Can triage a vMotion failure to a specific root-cause category from
      its error signature.
- [ ] Has verified the current live exam guide against this chapter's
      summary before scheduling.
- [ ] Completed the comprehensive hands-on lab, including both negative
      tests and cleanup.
