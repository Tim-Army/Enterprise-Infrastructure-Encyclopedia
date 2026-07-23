# Chapter 18: The VCAP Advanced Professional Tier — VCF 9.0 Role Exams, DCV Design, and NV Deploy

![The VMware Certified Advanced Professional tier: a professional-tier (VCP) base row noting that a current VCP is the entry requirement, then the eight-exam VCF 9.0 role series on one 3V0 generation — Administrator (3V0-11.26), Architect (3V0-12.26), Support (3V0-13.26), Automation (3V0-21.25), Operations (3V0-22.25), Storage (3V0-23.25), VKS Kubernetes (3V0-24.25), Networking (3V0-25.25) — and two carried-over VCAP exams on older generations, VCAP-DCV Design (3V0-21.23) and VCAP-NV Deploy (3V0-41.22). Design-oriented VCAPs feed the Distinguished Expert defense in Chapter 19.](../../../diagrams/volume-05-vmware-virtualization/chapter-18-vcap-advanced-tier-map.svg)

*Figure 18-1. The advanced (3V0) tier: eight VCF 9.0 role exams on one generation, plus two carried-over VCAP exams. A current VCP is the gate; the design-oriented exams point onward to Chapter 19.*

## Learning Objectives

- Describe the VMware Certified Advanced Professional (VCAP) tier and how
  it differs from the VCP tier in [Chapters 12–17](17-completing-the-vcp-tier-dcv-vcf-architect-avi-and-private-cloud-security.md):
  advanced depth, a VCP prerequisite, and — for design exams — a bridge
  toward the Distinguished Expert defense.
- Identify the eight VCF 9.0 role-based VCAP exams and their codes, and
  explain why they share one `3V0` generation while the two carried-over
  VCAP exams do not.
- Map each advanced exam to the chapters in this volume that prepare it,
  and recognize where this volume's coverage is a foundation versus where
  Broadcom's advanced training is required to close the gap.
- Distinguish a *Design* VCAP (architecture judgment, no live build) from a
  *Deploy* VCAP (hands-on configuration against a clock) and prepare each
  in the way its format rewards.
- Sequence an advanced-tier plan realistically: which VCAP follows which
  VCP, and which design exams to prioritize if the Distinguished Expert
  credential is the goal.

## Theory and Architecture

The VCAP tier is the advanced level of the VMware certification hierarchy,
between the professional VCP tier and the Distinguished Expert. Where a VCP
attests competence in a role, a VCAP attests *advanced* competence — deeper
troubleshooting, larger-scale design, or hands-on deployment under time
pressure. A **current VCP is the prerequisite** for the VCAP tier; confirm
the exact qualifying VCP for each VCAP on Broadcom's page, since the
mapping is specific.

This chapter is study and review material, consistent with every
preparation chapter in this volume. It does not reproduce exam questions or
scoring weightings and is not a substitute for Broadcom's exam guides. The
codes below were verified against Broadcom's certification pages; verify
current blueprints, prerequisites, and delivery details directly before
scheduling, because the advanced tier is being actively rebuilt around VCF
9.0 and is the fastest-moving part of the program.

### The VCF 9.0 role series — eight exams, one generation

VMware Cloud Foundation 9.0 introduced a **role-based advanced series**:
eight VCAP exams on a common `3V0` generation, each attesting advanced
competence in one VCF role. They are the current heart of the tier:

| Role | Code | What it attests | This volume |
| --- | --- | --- | --- |
| Administrator | 3V0-11.26 | Advanced day-2 operation of a VCF fleet | [13](13-vcp-vmware-cloud-foundation-support-2v0-15-25-exam-preparation.md), [14](14-vcp-vmware-cloud-foundation-administrator-2v0-17-25-exam-preparation.md) |
| Architect | 3V0-12.26 | Advanced VCF design — feeds the Distinguished Expert defense | [10](10-installing-vmware-nsx.md), [11](11-configuring-vmware-nsx.md) + design |
| Support | 3V0-13.26 | Advanced cross-component diagnosis | [13](13-vcp-vmware-cloud-foundation-support-2v0-15-25-exam-preparation.md) |
| Automation | 3V0-21.25 | VCF Automation, infrastructure-as-code delivery | [9](09-vsphere-lifecycle-automation-observability-and-troubleshooting.md) |
| Operations | 3V0-22.25 | The VCF Operations suite (logs, metrics, flows) | [9](09-vsphere-lifecycle-automation-observability-and-troubleshooting.md), [13](13-vcp-vmware-cloud-foundation-support-2v0-15-25-exam-preparation.md) |
| Storage | 3V0-23.25 | vSAN and storage design/operation at scale | [6](06-vsphere-storage-and-vsan.md) |
| VKS (Kubernetes) | 3V0-24.25 | VCF Kubernetes Service / Supervisor | [8](08-vsphere-and-nsx-security-architecture.md) foundation |
| Networking | 3V0-25.25 | NSX within VCF 9.0 | [10](10-installing-vmware-nsx.md), [11](11-configuring-vmware-nsx.md) |

Two structural points matter. First, the eight share a generation, so a
candidate pursuing more than one benefits from the common VCF 9.0 platform
knowledge — the marginal cost of a second role exam is lower than the
first. Second, this volume is a **foundation** for these, not full advanced
coverage: the Automation, Operations, and VKS exams in particular reach
into VCF products (VCF Automation, the Operations suite, the VCF Kubernetes
Service) that Chapters 1–11 introduce but do not exhaust. Expect to
supplement with Broadcom's advanced training and hands-on time on the
specific product.

### The two carried-over VCAP exams — both retiring 31 July 2026

Alongside the VCF 9.0 series, two older-generation VCAP exams remain in
the catalog, but **both are retiring on 31 July 2026** — Broadcom's own
certification pages state no new exam registrations will be available
after that date (verified 23 July 2026). Treat them as closing, not as
options to plan a multi-month study path around:

- **VCAP-DCV Design (3V0-21.23) — retiring 31 July 2026.** Advanced
  vSphere 8 design. It historically was the most direct on-ramp to the
  Distinguished Expert defense (Chapter 19) because it exercises the same
  conceptual→logical→physical design discipline and the same
  requirement/constraint/assumption/risk analysis a defense demands. With
  its retirement, **the current design on-ramp is the VCF Architect role
  (3V0-12.26)** in the 9.0 series above — pursue that unless you can sit
  3V0-21.23 before the retirement date.
- **VCAP-NV Deploy (3V0-41.22) — retiring 31 July 2026.** Advanced NSX-T
  hands-on **deployment** — a live-build exam rather than a multiple-choice
  one. It pairs with [VCP-NV (Chapter 12)](12-vcp-network-virtualization-2v0-41-24-exam-preparation.md)
  and rewards the timed build-and-troubleshoot practice that chapter's lab
  trains, but with the retirement its deploy-format practice now points
  toward the VCF Networking role (3V0-25.25) for anyone starting fresh.

### Design versus Deploy — two different exams to prepare for

The tier contains two fundamentally different exam formats, and conflating
them wastes preparation:

- A **Design** exam (VCAP-DCV Design, the Architect role) tests
  *architecture judgment*. There is no live system to configure; you reason
  from requirements to a defensible design. Prepare by articulating design
  decisions and their justifications, not by drilling configuration.
- A **Deploy** exam (VCAP-NV Deploy) tests *hands-on configuration against
  a clock*. Prepare by building, breaking, and rebuilding in a lab until
  the procedures are muscle memory, as in Chapter 12's timed lab.

Read each exam guide for its format before planning; the same "VCAP" label
covers both.

## Design Considerations

- **VCAP follows the matching VCP — but confirm the exact prerequisite.**
  The natural path is VCP-VCF Administrator → VCAP Administrator, VCP-NV →
  VCAP-NV Deploy, and so on. Broadcom specifies the qualifying VCP per
  VCAP, and it is not always the identically named one; check the page
  before assuming.
- **Prioritize by goal, not by completeness.** Very few readers should
  pursue all ten advanced exams. If the goal is operational seniority, one
  or two role exams matching your job (Administrator, Operations) suffice.
  If the goal is Distinguished Expert, a **Design** exam is the one that
  matters, because it rehearses the defense — and with VCAP-DCV Design
  retiring 31 July 2026, that now means the **VCF Architect role
  (3V0-12.26)** for anyone not already booked on 3V0-21.23.
- **This volume is a floor for the advanced tier.** Treat Chapters 1–11 as
  establishing the platform knowledge each advanced exam assumes coming in,
  then close the remaining gap with Broadcom's advanced courses and
  product-specific lab time. Do not expect this volume alone to carry an
  advanced exam the way it can carry a VCP.
- **The advanced tier moves fastest — verify currency hardest.** The VCF
  9.0 role series is new (`.25`/`.26` codes) and still settling; exam
  availability, prerequisites, and even which roles exist may change. The
  currency-check discipline in [Chapter 20](20-vmware-telco-cloud-and-keeping-the-certification-program-current.md)
  applies most sharply here.
- **Deploy exams demand a real lab; design exams demand a whiteboard.**
  Allocate lab hardware to the Deploy exams (VCAP-NV Deploy) where it is
  indispensable, and allocate uninterrupted articulation practice to the
  Design exams where a running lab helps far less than the ability to
  reason a design aloud.

## Implementation and Automation

### An advanced-tier study spine

```text
# Sequence advanced exams after the matching VCP. Rate readiness per
# exam 1–5; below 3 means supplement with Broadcom advanced training
# before booking. "Format" drives how you prepare, not just what.

Advanced exam (code)             | Format  | After VCP        | Rating
---------------------------------|---------|------------------|-------
VCAP-DCV Design (3V0-21.23)*     | Design  | VCP-DCV          |
VCAP-NV Deploy (3V0-41.22)*      | Deploy  | VCP-NV           |
  * both retiring 31 July 2026 — no new registrations after that date
VCF Administrator (3V0-11.26)    | Written | VCP-VCF Admin    |
VCF Architect (3V0-12.26)        | Design  | VCP-VCF Architect|
VCF Support (3V0-13.26)          | Written | VCP-VCF Support  |
VCF Automation (3V0-21.25)       | Written | VCP-VCF (role)   |
VCF Operations (3V0-22.25)       | Written | VCP-VCF (role)   |
VCF Storage (3V0-23.25)          | Written | VCP-VCF (role)   |
VCF VKS (3V0-24.25)              | Written | VCP-VCF (role)   |
VCF Networking (3V0-25.25)       | Written | VCP-NV / VCP-VCF |
```

### A Deploy-exam timed-build harness (reuse Chapter 12's approach)

```bash
# VCAP-NV Deploy rewards timed, unaided NSX builds. Wrap Chapter 12's
# lab in a timer and log elapsed time per phase so you can see which
# procedure is still too slow. Adapt paths to your lab.
start=$(date +%s)
echo "Phase 1 — transport zone, uplink profile, TEP pool, host prep"
# ... perform the build unaided ...
echo "Phase 1 elapsed: $(( ($(date +%s) - start) / 60 )) min"
```

### A Design-exam articulation template

```text
# For a Design exam (VCAP-DCV Design or Architect), practice turning a
# requirement into a justified design. Fill this from memory for a given
# scenario, then defend each cell aloud — that is the exam's real skill.

Requirement:
Constraint(s):
Assumption(s):
Risk(s) + mitigation:
Conceptual decision:
Logical decision:
Physical decision:
Justification (why this, not the alternative):
```

## Validation and Troubleshooting

- **Confirm the format before you prepare.** The clearest early
  self-check: can you state whether your target exam is Design, Deploy, or
  written? Preparing a Deploy exam with flashcards, or a Design exam with
  configuration drills, is the most common wasted effort at this tier.
- **Deploy readiness is a stopwatch, not a checklist.** For VCAP-NV Deploy,
  the readiness signal is completing Chapter 12's build phases unaided and
  within their time boxes repeatedly — not once. Log times across several
  attempts and watch the slowest phase, not the average.
- **Design readiness is an unaided justification.** For a Design exam, the
  signal is defending each design decision aloud against "why not the
  alternative?" without notes. If a decision can be stated but not defended,
  it is not yet ready.
- **Prerequisite gaps surface at registration, not before.** Because each
  VCAP requires a specific current VCP, verify your qualifying VCP is
  current and correct for the exact VCAP before investing study time; a
  lapsed or mismatched VCP blocks the booking.
- **Watch for role-series churn.** If a VCF 9.0 role exam code you prepared
  against no longer resolves on Broadcom's page, treat it as possibly
  renumbered or superseded and re-verify against the live certification
  landing page before rescheduling.

## Security and Best Practices

- Register only through Broadcom's authorized testing partner; Deploy exams
  in particular have specific lab-delivery and identification requirements —
  confirm them from the official portal well before exam day.
- Prepare Deploy exams in an isolated lab, never against production NSX —
  the timed, deliberately disruptive drills are unsafe against systems
  carrying real workloads.
- Do not use unauthorized dumps; at the advanced tier they are both a
  contractual violation and especially unreliable, since the VCF 9.0 series
  is new enough that circulating material is likely stale or fabricated.
- Handle any design document you author for practice as you would a real
  customer design — it will contain realistic architecture detail, and the
  habit of protecting it matters for the Distinguished Expert defense in
  [Chapter 19](19-vcdx-the-distinguished-expert-design-defense-discipline.md),
  where the design is the deliverable.

## References and Knowledge Checks

**References**

- [Broadcom Education Services — VMware certification](https://www.broadcom.com/support/education/vmware) —
  the authoritative exam guides for the VCF 9.0 role series (3V0-11.26
  through 3V0-25.25), VCAP-DCV Design (3V0-21.23), and VCAP-NV Deploy
  (3V0-41.22); confirm current codes, prerequisites, format, and price.
- [VMware Cloud Foundation documentation](https://techdocs.broadcom.com/us/en/vmware-cis/vcf.html) —
  product reference for the VCF 9.0 role exams.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  this repository's certification-to-volume mapping.
- [Appendix — VMware and Broadcom Certifications and Course Access](../../volume-97-master-appendices/chapters/07-appendix-vmware-broadcom-certifications-and-course-access.md) —
  official training mapped to each advanced exam.
- See [Chapter 17](17-completing-the-vcp-tier-dcv-vcf-architect-avi-and-private-cloud-security.md)
  for the professional tier below this one, and
  [Chapter 19](19-vcdx-the-distinguished-expert-design-defense-discipline.md)
  for the design defense above it.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any Broadcom exam item)*

1. Explain how a VCAP differs from a VCP in what it attests, and name the
   general prerequisite the VCAP tier imposes.
2. Why do the eight VCF 9.0 role exams share a `3V0` generation, and what
   practical advantage does that give a candidate taking more than one?
3. Distinguish a Design VCAP from a Deploy VCAP by format, and state how
   preparation should differ between them.
4. Which single advanced exam most directly rehearses the Distinguished
   Expert defense, and why?
5. Where is this volume a foundation rather than full coverage for the
   advanced tier, and how would you close that gap responsibly?

## Hands-On Lab

**Objective:** Produce, without booking any exam, one concrete readiness
artifact for each of the two advanced-exam formats — a timed Deploy log and
a defended Design chain — so you can judge which format you are closer to
ready for.

**Prerequisites**

- The NSX lab from [Chapters 10–11](10-installing-vmware-nsx.md), reset to
  a clean state, and a timer (for the Deploy artifact).
- The Design articulation template from the Implementation section and one
  realistic scenario (for the Design artifact).
- No reference material open during the timed and articulation portions.

**Steps**

1. **Deploy artifact (timed, target 45 minutes).** Run
   [Chapter 12](12-vcp-network-virtualization-2v0-41-24-exam-preparation.md)'s
   NSX build (transport zone through Tier-0 BGP and a DFW policy) unaided,
   logging elapsed time per phase.

   **Expected result:** a per-phase time log, with the slowest phase
   identified as the VCAP-NV Deploy weak point to drill next.

2. **Design artifact (target 30 minutes).** Take one requirement (for
   example, "the design must survive the loss of any single availability
   zone with no data loss") and complete the Design articulation template
   from memory — conceptual, logical, physical, plus constraints,
   assumptions, and risks.

   **Expected result:** a filled template whose every decision you can
   defend aloud against "why not the alternative?"

3. **Defend the design (target 15 minutes).** Have a partner (or, working
   alone, a recorded self-review) challenge each design decision. Mark any
   decision you cannot justify unaided.

   **Expected result:** a list of design decisions needing more depth —
   the VCAP Design / Architect weak points.

4. **Compare formats.** Judge which artifact was stronger. A clean Deploy
   log with a slow but improving time points toward a Deploy exam; a design
   you can defend end to end points toward a Design exam and, beyond it,
   Chapter 19.

5. **Cleanup:** tear down the NSX build to its clean baseline and archive
   (do not discard) the design artifact — it is the seed of a Distinguished
   Expert design document.

## Lab Verification

Complete this sign-off once both artifacts have been produced and the
design defended. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The VCAP tier is the advanced level between VCP and Distinguished Expert,
gated by a current VCP. Its current heart is the eight-exam VCF 9.0 role
series on one `3V0` generation — Administrator (3V0-11.26), Architect
(3V0-12.26), Support (3V0-13.26), Automation (3V0-21.25), Operations
(3V0-22.25), Storage (3V0-23.25), VKS (3V0-24.25), and Networking
(3V0-25.25) — alongside two carried-over exams, VCAP-DCV Design (3V0-21.23)
and VCAP-NV Deploy (3V0-41.22), **both retiring 31 July 2026**. Prepare by
format, not by label: Design
exams reward defensible architecture judgment, Deploy exams reward timed
unaided builds. This volume is the foundation the tier assumes; close the
remainder with Broadcom's advanced training. If Distinguished Expert is the
goal, a Design exam is the one that rehearses it.

- [ ] Can describe how the VCAP tier differs from the VCP tier and the
      prerequisite it imposes.
- [ ] Can list the eight VCF 9.0 role exams and why they share a
      generation.
- [ ] Can distinguish a Design exam from a Deploy exam and prepare each
      accordingly.
- [ ] Knows which advanced exam most rehearses the Distinguished Expert
      defense.
- [ ] Has produced both a timed Deploy log and a defended Design chain.
- [ ] Has verified the current codes, prerequisites, and formats against
      Broadcom before scheduling.
- [ ] Completed the hands-on lab, including archiving the design artifact.
