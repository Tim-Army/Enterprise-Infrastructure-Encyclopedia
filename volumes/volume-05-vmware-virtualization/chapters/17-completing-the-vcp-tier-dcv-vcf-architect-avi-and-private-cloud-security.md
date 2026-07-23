# Chapter 17: Completing the VCP Tier — Data Center Virtualization, VCF Architect, Avi, and Private Cloud Security

![The VMware Certified Professional tier shown complete: the five 2V0-generation exams already covered in Chapters 12–16 (VCP-NV 2V0-41.24, VCP-VCF Administrator 2V0-17.25, VCP-VCF Support 2V0-15.25, VCP-VVF Administrator 2V0-16.25, VCP-VVF Support 2V0-18.25) in one group, and the four professional-level exams this chapter adds in a second group — VCP-DCV Data Center Virtualization (2V0-21.23, on the older vSphere 8 generation), VCP-VCF Architect (2V0-13.25), and two specialist-code VCPs, VCP-AVI Avi Load Balancer Administrator (6V0-22.25) and VCP-PCS Private Cloud Security Administrator (6V0-21.25). All nine sit at the same professional tier and none is a prerequisite for another.](../../../diagrams/volume-05-vmware-virtualization/chapter-17-vcp-tier-landscape.svg)

*Figure 17-1. The complete VCP tier: the five exams mapped in Chapters 12–16, plus the four this chapter adds. Same tier throughout — sequence by the role you hold, not by exam number.*

## Learning Objectives

- Place the four remaining professional-level VMware exams — VCP-DCV
  (2V0-21.23), VCP-VCF Architect (2V0-13.25), VCP-AVI (6V0-22.25), and
  VCP-PCS (6V0-21.25) — against the content already in this volume, and
  identify which existing chapters prepare each.
- Explain why VCP-DCV sits on the older vSphere 8 generation while the
  VVF/VCF exams target 9.0, and what that means for a candidate choosing
  between VCP-DCV and VCP-VVF Administrator.
- Distinguish the 2V0 mainstream-VCP code family from the 6V0 code family
  the Avi and Private Cloud Security exams carry, and read what that
  numbering signals about scope.
- Identify the VCP-VCF Architect exam as the design-role entry point that
  leads toward the VCAP Architect exam (Chapter 18) and, beyond it, the
  Distinguished Expert defense (Chapter 19).
- Build a self-assessment plan for each of the four exams that reuses this
  volume's existing labs rather than assuming a separate lab build.

## Theory and Architecture

Chapters 12 through 16 mapped five VMware Certified Professional exams to
this volume's content. They are not the whole professional tier. Broadcom's
current VCP lineup includes four more exams that this volume's material
already substantially prepares a reader for, and this chapter organizes
them the same way the earlier preparation chapters do: as blueprint-mapped
self-assessment material, not as reproductions of proprietary exam content.

As with every preparation chapter in this volume, this is study and review
material. It does not reproduce exam questions, does not reveal scoring
weightings, and is not a substitute for Broadcom's own exam guide. Confirm
current domain names, exam length, item count, and price against the
official exam guide before scheduling — the codes below were verified
against Broadcom's certification pages, but blueprints and delivery details
are revised independently of this repository's release cycle.

### The four exams and what each is

- **VCP-DCV — Data Center Virtualization (2V0-21.23).** The long-running
  flagship VCP, and the one most people mean by "the VCP." Its code
  (`.23`) places it on the **vSphere 8 generation**, one generation behind
  the 9.0-targeted VVF and VCF exams in Chapters 13–16. It tests core
  vSphere administration end to end — installation, configuration, VM and
  resource management, storage and vSAN, availability and mobility — which
  is exactly the ground [Chapters 1–9](01-vmware-virtualization-architecture-and-design.md)
  cover. For a reader whose environment is vSphere 8, this is the closest
  match; for a reader on 9.0, [VCP-VVF Administrator](15-vcp-vmware-vsphere-foundation-administrator-2v0-16-25-exam-preparation.md)
  is the current-generation equivalent.

- **VCP-VCF Architect (2V0-13.25).** The **design-role** VCP for VMware
  Cloud Foundation 9.0. Where VCP-VCF Administrator (Chapter 14) tests
  building and operating a VCF estate, the Architect exam tests *designing*
  one: turning requirements, constraints, and assumptions into a defensible
  conceptual, logical, and physical design. It is the professional-tier
  entry point to the design discipline that continues through
  [VCAP Architect (Chapter 18)](18-the-vcap-advanced-professional-tier-vcf-9-0-role-exams-dcv-design-and-nv-deploy.md)
  and culminates in the [Distinguished Expert defense (Chapter 19)](19-vcdx-the-distinguished-expert-design-defense-discipline.md).

- **VCP-AVI — Avi Load Balancer Administrator (6V0-22.25).** Covers the
  **VMware Avi Load Balancer** (formerly Avi Networks / NSX Advanced Load
  Balancer): a software-defined, scale-out application delivery controller
  providing load balancing, WAF, and GSLB with centralized policy. Its
  `6V0` code marks it as a **specialist** exam rather than a mainstream
  `2V0` VCP — narrower product scope, and independent of the vSphere/VCF
  sequence. It complements the North-South and application-delivery
  material adjacent to [Chapter 11](11-configuring-vmware-nsx.md)'s load
  balancing discussion.

- **VCP-PCS — Private Cloud Security Administrator (6V0-21.25).** Covers
  securing a VMware private cloud — the vDefend Distributed Firewall and
  Advanced Threat Prevention, micro-segmentation, and the platform
  hardening that [Chapter 8](08-vsphere-and-nsx-security-architecture.md)
  builds. Like VCP-AVI it carries a `6V0` specialist code and stands
  outside the administrator/support pairing.

### Reading the code families

The exam number's prefix is a genuine signal, not decoration:

- **`2V0-…`** is the mainstream professional (VCP) family — VCP-DCV,
  VCP-VCF Architect/Administrator/Support, VCP-VVF Administrator/Support,
  VCP-NV. These are the broad, role-defining exams.
- **`6V0-…`** is the specialist family — narrower single-product scope
  (Avi, Private Cloud Security here). A `6V0` still confers a VCP-branded
  credential, but its blueprint is scoped to one product area rather than a
  whole platform role.
- **`3V0-…`** is the advanced (VCAP) family, and **`5V0-…`** the
  specialist-skills family — both covered in later chapters (18 and 20).

Knowing the family tells you roughly how wide to prepare before you open
the exam guide: a `2V0` expects platform breadth, a `6V0` expects depth in
one product.

## Design Considerations

- **DCV or VVF Administrator — pick by product generation, not prestige.**
  These two overlap heavily in content; the deciding factor is which
  vSphere generation you run and certify against. On vSphere 8, VCP-DCV
  (2V0-21.23) is the direct match. On vSphere Foundation 9.0, VCP-VVF
  Administrator (2V0-16.25) is current. Holding both adds little for most
  readers — they test the same core skill against different generations.
- **Architect before you can defend.** If the goal is the Distinguished
  Expert credential, VCP-VCF Architect is where the design vocabulary
  starts — requirements/constraints/assumptions/risks, and the
  conceptual→logical→physical progression. Treat it as the first rung of
  the design path, not a sideways option, and carry its habits into
  Chapters 18 and 19.
- **Specialist exams reward a running product, not reading.** VCP-AVI and
  VCP-PCS are `6V0` product exams; both are far easier to pass with the
  product actually deployed in a lab than from documentation. For Avi, that
  means a controller and service-engine pair with at least one virtual
  service configured; for PCS, a vDefend Distributed Firewall enforcing a
  real micro-segmentation policy as in [Chapter 8](08-vsphere-and-nsx-security-architecture.md).
- **Currency cuts hardest on the older generation.** VCP-DCV's vSphere 8
  blueprint is the most likely of the four to shift as a 9.0-generation DCV
  successor appears. Before committing study time, confirm on Broadcom's
  page that 2V0-21.23 is still the current DCV exam rather than assuming it
  from this chapter.
- **Ethical preparation boundary.** As with every exam in this volume,
  prepare only from authorized sources: Broadcom's documentation and exam
  guide, official training, and hands-on practice. Material claiming to
  reproduce actual scored questions violates the certification agreement
  and is frequently wrong against the live blueprint — treat any such
  resource as disqualifying rather than helpful.

## Implementation and Automation

### Mapping each exam to existing chapters

```text
# Reuse this volume's chapters as the study spine for all four exams.
# Rate each row 1–5; treat anything below 3 as needing lab time first.

Exam (code)                         | Primary chapters      | Self-rating
------------------------------------|-----------------------|------------
VCP-DCV (2V0-21.23)                 | 1,2,3,4,5,6,7,8,9     |
VCP-VCF Architect (2V0-13.25)       | 1,8,10,11 + design    |
VCP-AVI (6V0-22.25)                 | 4,11 (app delivery)   |
VCP-PCS (6V0-21.25)                 | 8,10,11 (vDefend)     |
```

### An Avi controller inventory drill (self-generated design questions)

```bash
# Against a lab Avi Controller, pull the virtual-service and pool
# inventory over the REST API, then practice explaining *why* each
# object is configured as it is — a design-judgment drill, not a
# config walkthrough. Replace host/credentials with your lab values.
curl -k -s -u 'admin:<AVI_ADMIN_PASSWORD>' \
  https://avi-controller.corp.example/api/virtualservice | \
  jq '.results[] | {name, enabled, services}'
curl -k -s -u 'admin:<AVI_ADMIN_PASSWORD>' \
  https://avi-controller.corp.example/api/pool | \
  jq '.results[] | {name, lb_algorithm, health_monitor_refs}'
```

### A Private Cloud Security posture check (reuse Chapter 8's lab)

```bash
# Confirm a micro-segmentation policy is actually enforcing before
# treating PCS preparation as done. Pull the DFW policy and rule
# inventory from NSX Manager (as in Chapter 8) and verify a
# default-deny plus scoped-allow structure exists.
curl -k -s -u 'admin:<NSX_ADMIN_PASSWORD>' \
  https://nsx-vip.corp.example/policy/api/v1/infra/domains/default/security-policies | \
  jq '.results[] | {display_name, category}'
```

## Validation and Troubleshooting

- **Generation check before DCV.** The single most common misstep on
  VCP-DCV is preparing against the wrong vSphere generation. Verify the
  live exam guide targets the version you have lab access to; a 9.0-only
  lab is a weaker fit for a vSphere 8 blueprint than it looks.
- **Design articulation for the Architect exam.** The readiness signal for
  VCP-VCF Architect is being able to state, out loud and unaided, why a
  given requirement forces a specific design decision and what constraint
  or assumption bounds it — not recognizing a correct diagram. Practice
  narrating a design, not reviewing one.
- **Specialist exams need the product running.** If VCP-AVI or VCP-PCS
  concepts are understood only well enough to recognize in documentation
  but not to configure unaided, treat them as not yet exam-ready. Both
  blueprints assume hands-on administration of the specific product.
- **Cross-check the 6V0 scope boundary.** A frequent trap on specialist
  exams is over-preparing platform breadth (the `2V0` mindset) and
  under-preparing the one product's depth. Confirm your study is scoped to
  Avi or vDefend specifically, not vSphere generally.

## Security and Best Practices

- Register only through Broadcom's authorized testing partner, and confirm
  current identification and proctoring requirements from the official
  registration portal before exam day; these vary by delivery method and
  change over time.
- Do not purchase or reference unauthorized exam dumps — beyond the
  contractual violation, they are commonly inaccurate against the live
  blueprint, which for VCP-DCV's older generation is a particular risk.
- Run the Avi and vDefend preparation labs in an isolated environment, not
  against production application-delivery or security enforcement — a
  mis-scoped DFW rule or a misconfigured virtual service can black-hole
  real traffic.
- Protect lab credentials (Avi Controller, NSX Manager) with the same
  discipline as production, per [Chapter 8](08-vsphere-and-nsx-security-architecture.md)'s
  RBAC and credential-hygiene guidance; building the habit in preparation
  reinforces it for the real deployment the credential attests to.

## References and Knowledge Checks

**References**

- [Broadcom Education Services — VMware certification](https://www.broadcom.com/support/education/vmware) —
  the authoritative exam guides for 2V0-21.23, 2V0-13.25, 6V0-22.25, and
  6V0-21.25 (current blueprint domains, item count, duration, price, and
  registration requirements — verify directly before scheduling).
- [VMware Avi Load Balancer documentation](https://techdocs.broadcom.com/us/en/vmware-security-load-balancing/avi-load-balancer.html) —
  product reference for VCP-AVI preparation.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  this repository's certification-to-volume mapping.
- [Appendix — VMware and Broadcom Certifications and Course Access](../../volume-97-master-appendices/chapters/07-appendix-vmware-broadcom-certifications-and-course-access.md) —
  the course catalog mapping official training to each exam.
- See [Chapter 8](08-vsphere-and-nsx-security-architecture.md) for the
  security foundation behind VCP-PCS.
- See [Chapters 1–9](01-vmware-virtualization-architecture-and-design.md)
  for the vSphere core behind VCP-DCV.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any Broadcom exam item)*

1. Explain why a reader running vSphere Foundation 9.0 might choose
   VCP-VVF Administrator over VCP-DCV, and when the reverse is correct.
2. From memory, distinguish what the `2V0` and `6V0` code families signal
   about an exam's breadth, and name one exam in each.
3. State the design progression VCP-VCF Architect begins and the two later
   milestones it leads to in this volume.
4. Given a lab with an Avi Controller and one virtual service, describe a
   design-judgment drill you could run without changing any configuration.
5. Why is preparing VCP-PCS from documentation alone weaker than for a
   `2V0` exam, and what minimum lab state closes that gap?

## Hands-On Lab

**Objective:** Confirm, without booking any exam, which of the four
professional-level exams in this chapter you are closest to ready for, by
running one scoped drill per exam against this volume's existing labs.

**Prerequisites**

- The lab environments from earlier chapters: a vSphere cluster (Chapters
  1–9), NSX with a vDefend DFW policy (Chapters 8, 10–11), and — if
  available — a lab Avi Controller with one virtual service.
- The domain-mapped tracker from the Implementation section above.
- No reference material open during each timed drill.

**Steps**

1. **VCP-DCV drill (target 20 minutes).** From memory, provision a VM from
   a template, apply a storage policy, and vMotion it between hosts.

   **Expected result:** all three complete unaided; note any step that
   needed [Chapters 5–7](05-virtual-machine-lifecycle-and-resource-management.md).

2. **VCP-VCF Architect drill (target 15 minutes).** Take one written
   requirement (for example, "recover a workload domain within four hours
   of a site failure") and write the conceptual, logical, and physical
   design decisions it forces, naming one constraint and one assumption.

   **Expected result:** a coherent three-level design chain on paper,
   defensible aloud.

3. **VCP-AVI drill (target 15 minutes).** If an Avi lab exists, inspect one
   virtual service and its pool, then explain its load-balancing algorithm
   and health monitor choice without opening documentation. If no Avi lab
   exists, record this as a lab gap to close before scheduling.

   **Expected result:** an unaided explanation, or an identified gap.

4. **VCP-PCS drill (target 15 minutes).** Verify a default-deny plus
   scoped-allow micro-segmentation policy is enforcing (reuse
   [Chapter 8](08-vsphere-and-nsx-security-architecture.md)'s lab), then
   explain how you would prove a specific flow is blocked by policy rather
   than by routing.

   **Expected result:** the policy enforces, and you can name the tool
   (Traceflow, DFW hit counters) that distinguishes the two causes.

5. **Score and target.** Rank the four drills by how far over time or how
   reference-dependent each was. The weakest is the exam furthest from
   ready; direct additional lab time there rather than re-reading a domain
   already strong.

6. **Cleanup:** revert the VM, remove any test design notes, and return the
   DFW policy and Avi objects to their baseline state so the labs are ready
   for future runs.

## Lab Verification

Complete this sign-off once the four drills have been run end to end. Until
then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The VMware Certified Professional tier is wider than the five exams
Chapters 12–16 map. VCP-DCV (2V0-21.23) is the vSphere 8-generation
flagship that this volume's Chapters 1–9 already cover; VCP-VCF Architect
(2V0-13.25) opens the design path that runs through VCAP Architect and the
Distinguished Expert defense; and VCP-AVI (6V0-22.25) and VCP-PCS
(6V0-21.25) are `6V0` specialist exams scoped to the Avi Load Balancer and
vDefend private-cloud security respectively. Read the code family to gauge
breadth, pick DCV versus VVF by product generation rather than prestige,
and prepare the specialist exams against a running product, not
documentation.

- [ ] Can place all four exams against specific chapters in this volume.
- [ ] Can choose between VCP-DCV and VCP-VVF Administrator by product
      generation.
- [ ] Can read what a `2V0` versus `6V0` code signals about exam breadth.
- [ ] Has identified VCP-VCF Architect as the start of the design path to
      Chapters 18 and 19.
- [ ] Has run one scoped drill per exam and identified the weakest.
- [ ] Has verified each code against Broadcom's live certification page
      before scheduling.
- [ ] Completed the hands-on readiness lab, including cleanup.
