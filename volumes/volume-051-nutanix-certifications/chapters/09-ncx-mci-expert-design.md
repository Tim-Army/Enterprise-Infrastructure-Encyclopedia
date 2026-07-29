# Chapter 09: NCX-MCI — Expert Design

## Learning Objectives

- Explain what the NCX-MCI certifies and how it differs from NCM.
- Summarize the three blueprint sections of the expert exam.
- Translate customer requirements into conceptual, logical, and physical designs.
- Justify design decisions against constraints and risks.
- Complete a design exercise for each NCX-MCI section.

## Theory and Architecture

The **Nutanix Certified Expert — Multicloud Infrastructure (NCX-MCI)** is the top of
the program — a **design-and-defend** credential (the successor to NPX), assessed
against a scenario rather than by recall. Its blueprint centers on **three sections**:
**Customer Consultation** (gather and analyze requirements/constraints/risks/
assumptions), **Conceptual/Logical Design** (translate requirements into a logical
architecture), and **Physical Design** (specify the concrete build). Like the CCDE
design exercises in Volume XXX, this chapter is **design work**, not CLI.

## Design Considerations

The expert elicits **requirements** (functional and non-functional), separates
**constraints** from **assumptions**, identifies **risks**, produces a **logical**
design (fault domains, data-protection tiers, network segmentation, capacity model),
then a **physical** design (node models, disk/CPU/RAM, network topology, DR sites),
and **justifies** each decision back to a requirement.

## Implementation and Automation

The exercises below are **design deliverables** — requirement tables, logical
diagrams, and physical bills of materials — one per blueprint section. There are no
CLI commands; the "expected result" is a defensible artifact.

## Validation and Troubleshooting

Confirm the blueprint before studying:

```text
nutanix.com > NCX-MCI blueprint:
  1 Customer Consultation (requirements, constraints, assumptions, risks)
  2 Conceptual/Logical Design
  3 Physical Design
Design-and-defend format (scenario-based).
```

Common pitfalls: jumping to a **physical** BOM before the logical design; and
conflating a **constraint** (imposed) with an **assumption** (unverified).

## Security and Best Practices

Trace every design element to a **requirement**, record **constraints/assumptions/
risks** explicitly, design **logical before physical**, build in fault domains and DR,
and be ready to **defend** trade-offs. Document so another architect can implement it.

## Hands-On Lab

Design exercises — NCX-MCI. **Shared prerequisites** — the scenario below; a document/
diagram tool. **Cost:** none.

> **Scenario.** A retailer needs a 3-site Nutanix design: a primary datacenter (500
> VMs, mixed DB/VDI), a DR site (RPO 15 min for tier-1), and 40 stores (small edge
> clusters). Budget and a 4-hour tier-1 RTO are constraints.

### Exercise 9.1 — Customer consultation (requirements)

**Objective:** Produce a requirements/constraints/assumptions/risks (RCAR) table.

```text
Deliverable (RCAR table), e.g.:
  Requirement: tier-1 RPO <= 15 min; RTO <= 4h; 500 VMs primary; 40 edge sites
  Constraint:  fixed budget; existing 10GbE at stores
  Assumption:  WAN bandwidth to DR >= 200 Mbps (to verify)
  Risk:        store links are single-homed -> edge outage risk
```

**Expected result:** a complete **RCAR table** separating requirements, constraints,
assumptions, and risks — the customer-consultation section.

**Negative test:** list only requirements; unstated **constraints/assumptions/risks**
sink designs — capture all four.

**Cleanup:** none.

### Exercise 9.2 — Conceptual/logical design

**Objective:** Produce a logical architecture meeting the RCAR.

```text
Deliverable (logical design):
  - Primary: single cluster, RF2, Flow segmentation (DB/VDI/mgmt zones)
  - DR: NearSync (15-min RPO) for tier-1; async for the rest; recovery plans for RTO
  - Edge: small RF2 clusters per store, centrally managed via Prism Central
  - Capacity model: N+1 fault tolerance; growth headroom 30%
```

**Expected result:** a **logical design** that maps each choice to a requirement
(NearSync → 15-min RPO; recovery plans → 4-h RTO) — the logical-design section.

**Negative test:** pick Metro (0 RPO) when 15-min suffices; **match the tier** to the
requirement to control cost.

**Cleanup:** none.

### Exercise 9.3 — Physical design

**Objective:** Produce a physical build (BOM + topology).

```text
Deliverable (physical design):
  - Primary: 6x NX-8170 (RF2, N+1), NVMe+SSD, dual 25GbE ToR, Prism Central
  - DR: 4x NX-8170 in DR site; NearSync replication link sized to change rate
  - Edge: 3-node NX-1065 per store x40, 10GbE, centrally managed
  - Network: leaf-spine core; store WAN with backup link (mitigates the risk)
```

**Expected result:** a **physical design** (node models, disks, network, sites) that
implements the logical design and mitigates the identified risks — the physical-design
section.

**Negative test:** size the BOM before the logical design; **logical first**, then the
physical build follows from it.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The NCX-MCI is Nutanix's expert design-and-defend credential across three sections:
customer consultation (RCAR), conceptual/logical design, and physical design. Like the
CCDE exercises, it is design work — trace every decision to a requirement and defend
the trade-offs.

- [ ] I can capture requirements, constraints, assumptions, and risks.
- [ ] I can produce a logical design mapped to requirements.
- [ ] I can produce a physical design that implements the logical one.
- [ ] I can defend design trade-offs (e.g., NearSync vs Metro).
- [ ] I completed Exercises 9.1–9.3 including each negative test.
