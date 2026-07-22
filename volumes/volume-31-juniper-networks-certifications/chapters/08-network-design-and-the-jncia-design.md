# Chapter 08: Network Design and the JNCIA-Design

## Learning Objectives

- Apply a requirements-first design method: business goals to
  constraints to technical requirements to topology
- Choose among the architectures this volume built — campus, provider
  core, EVPN fabric, SRX edge, Mist cloud — with defensible trade-offs
- Produce design artifacts that survive contact with implementation:
  HLD/LLD, capacity and failure-domain analysis, migration plans
- Prepare for the JNCIA-Design (JN0-1103), the track's single current
  exam

## Theory and Architecture

### The track in one sentence

The Design track certifies the discipline before configuration:
gathering requirements, weighing trade-offs, and committing them to
paper. **JNCIA-Design (JN0-1103)** is its one current rung — 90
minutes, 65 questions, no prerequisite (verified on Juniper's pages,
22 July 2026) — making it the program's most accessible on-ramp for
architects; the specialist and professional design rungs of past years
are retired, their material absorbed into the technology tracks'
professional exams.

### The method is the content

Juniper's design doctrine matches this encyclopedia's: **business
requirements** (what the organization must do) beget **technical
requirements** (what the network must therefore do) under
**constraints** (budget, brownfield, compliance, staff skills). Every
architecture choice is a trade defended in those terms — never
"EVPN because modern," always "EVPN because dual-homing without
MC-LAG state and per-tenant Type-5 separation meet R7 and R11 within
the refresh budget." Greenfield designs top-down; brownfield designs
migration-first, where the sequencing *is* the design.

### The portfolio mapped to problems

Campus and branch: EX access with Virtual Chassis or ESI-LAG, Mist
operations, SRX at the branch edge. Data center: QFX ERB fabrics,
Apstra intent. WAN and core: MX with MPLS/SR, or SD-WAN via the Mist
WAN edge for the branch estate. Security: SRX zones everywhere
traffic changes trust. The JNCIA-Design tests recognizing which
problem class is in front of you.

## Design Considerations

- **Failure domains before bandwidth:** every shared fate — a Virtual
  Chassis, a fabric, a site — is drawn and sized before any link is
- Redundancy that cannot be tested is decoration; the design names
  its failover drills (Volume XII's doctrine, applied at design time)
- **Capacity with headroom rules** (50% link ceilings at steady
  state), lifecycle alignment (design to the Junos EOL calendar), and
  operability as a requirement: if the team runs Mist, a CLI-only
  design is a staffing decision in disguise
- Security zones and management OOB drawn on the first diagram, not
  retrofitted

## Implementation and Automation

Design's implementation is documents. The volume's deliverable set:

```text
design-package/
├── 01-requirements.md        # business, technical, constraints — numbered
├── 02-hld.md                 # architecture, failure domains, capacity model
├── 03-lld.md                 # per-device: addressing, VLAN/VNI, policy names
├── 04-migration-plan.md      # phases, rollback gates, success criteria
├── 05-test-plan.md           # per-requirement acceptance tests
└── diagrams/                 # topology, traffic flows, failure scenarios
```

Each LLD element traces to a numbered requirement; each requirement
appears in the test plan. That traceability is what the design exam's
scenario questions probe — and what makes the package automatable by
Chapter 06's pipeline afterward.

## Validation and Troubleshooting

Designs are validated, not debugged:

- **Requirements review:** every stated business goal maps to at least
  one technical requirement and one test
- **Failure walkthrough:** for each drawn domain, narrate the outage —
  blast radius, detection, recovery time — against the stated RTO
- **Capacity check:** the busiest link at peak with one failure,
  against the headroom rule
- **Migration dry run:** every phase has a rollback and a gate; a plan
  without reversals is a hope
- Peer review against the checklist — the design-time equivalent of
  commit-confirmed

## Security and Best Practices

- Trust boundaries and inspection points on the primary diagram; data
  flows annotated with their classification
- Management plane design (OOB, jump hosts, automation subnets) as a
  first-class section, never an appendix
- Compliance constraints written as requirements with test steps, so
  audits replay the acceptance run

## References and Knowledge Checks

- JNCIA-Design (JN0-1103) objectives on Juniper's certification pages
- Juniper validated designs library; this encyclopedia's Volumes II
  (foundations), XII (resilience), XXX (CCDE method — the expert-level
  extension of this chapter)

Knowledge checks:

1. A customer demands "no single point of failure." Turn that into
   two testable technical requirements and one explicit cost trade.
2. Why does a brownfield design lead with the migration plan rather
   than the target topology?
3. Your EVPN fabric design meets every technical requirement but the
   customer's team has never run BGP. What does the design method say
   happens next?

## Hands-On Lab

Produce a complete design package for a 3-site enterprise (HQ campus,
data center, branch) using this volume's portfolio: numbered
requirements (invent a realistic brief), HLD with failure domains and
capacity math, LLD tables for addressing and VLAN/VNI plans, a 4-phase
migration plan with rollback gates, and a test plan tracing every
requirement. Peer-review it against the validation walkthroughs above
and revise once.

## Lab Verification

Verification means the package's traceability is complete (every
requirement → design element → test), the failure walkthrough covers
each drawn domain with RTO math, and the revision log shows at least
one defensible change from review.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

- [ ] Requirements-to-design method practiced end to end
- [ ] Portfolio-to-problem mapping articulated
- [ ] Full design package produced and peer-reviewed
- [ ] JNCIA-Design (JN0-1103) scope recorded from primary source
- [ ] Migration-first brownfield thinking demonstrated
