# Chapter 05: Data Plane, Management Plane, Automation, and Operational Design

## Learning Objectives

- Design the data plane: forwarding paradigms, overlays, and their
  scaling and failure properties
- Design the management plane: out-of-band access, telemetry, and
  observability as architecture
- Treat automation and programmability as design inputs, not
  afterthoughts
- Design for operational sustainability: change, assurance, and
  lifecycle
- Reason about the three planes together and the consequences of
  separating or collapsing them

## Theory and Architecture

### Three planes, designed deliberately

CCDE Domain 2 (25%) treats the control, data, and management planes as
first-class design objects. Chapter 04 covered the control plane; this
chapter covers the other two and the operational design that runs the
whole network. The planes:

- **Control plane** — how forwarding decisions are computed (routing,
  LISP, BGP-EVPN).
- **Data plane** — how packets are actually forwarded (IP, MPLS
  labels, VXLAN/SRv6 encapsulation).
- **Management plane** — how the network is accessed, monitored, and
  changed.

The design decision that recurs: how separate to keep them. Strong
separation (out-of-band management, control-plane protection) improves
security and resilience; collapsing them saves cost and complexity.
The right degree is set by the availability and security requirements.

### Data-plane design

The data plane's design choices are about **encapsulation and scale**:

- **Native IP** — simplest, no overlay; suited to designs that do not
  need per-tenant isolation or transport abstraction.
- **MPLS** — label forwarding that decouples the core from customer/
  tenant routes (Volume XXIX); the enterprise sees it in some WAN and
  large-campus designs.
- **Overlays (VXLAN, SRv6)** — SD-Access and data-center fabrics
  (Volume XXVII) and modern SP transport (Volume XXIX). Overlays buy
  segmentation, mobility, and transport independence at the cost of
  encapsulation overhead, MTU planning, and a control plane to run
  them.

The design weighs what the overlay buys against its complexity — the
same judgment as fabric adoption in Chapter 03. MTU is a recurring
data-plane design constraint: every overlay adds header bytes, and the
end-to-end MTU must be designed, not discovered in production.

### Management plane and observability

Modern design treats **observability as architecture**, not a
bolt-on:

- **Out-of-band (OOB) management** — a separate management network so
  the network can be managed when the data plane is broken (and so
  management traffic cannot be attacked through the data plane). Its
  presence or absence is a resilience and security design decision.
- **Telemetry** — model-driven streaming telemetry (Volume XXIX,
  Chapter 09) versus legacy polling; the design provisions the
  collection, storage, and correlation the operations team needs to
  meet its assurance obligations.
- **Control-plane protection** — CoPP/LPTS as design elements
  protecting the devices that run everything.

### Automation and programmability as design inputs

The CCDE v3.x weights automation because *whether and how a network
can be automated is an architectural property*. A design that is
inconsistent, snowflake-heavy, and hand-configured cannot be
automated; a design that is templated, model-driven, and consistent
can. So automation shapes the design: standardized building blocks,
declared intent, a source of truth, and model-driven interfaces are
architectural decisions that pay off in operational sustainability.
Increasingly this includes **AI-assisted operations** (v3.1's AI/ML
additions) — anomaly detection and assurance driven by the telemetry
the design must produce.

### Operational sustainability

The through-line from Chapter 02: a network must be operable for
years by its team. Operational design covers change management (safe,
staged, rollback-capable — the commit discipline of Volume XXIX,
Chapter 01, as an architectural expectation), assurance (does the
network prove it is meeting requirements), and lifecycle (how
upgrades, growth, and technology refresh happen without redesign).

## Design Considerations

- **Plane separation to the requirement.** OOB management and
  control-plane protection where availability/security demand it;
  collapsed where cost dominates and the risk is acceptable — a stated
  decision either way.
- **Overlay only for what it buys.** Segmentation, mobility, or
  transport independence justify an overlay; without them, native IP
  is the simpler, more operable choice. Plan MTU end to end whenever
  an overlay is chosen.
- **Design for automatability.** Standardize building blocks and
  choose model-driven-capable platforms so the design *can* be
  automated; a snowflake design forecloses automation regardless of
  later intent.
- **Observability is provisioned, not assumed.** The telemetry
  pipeline the operations team needs is part of the design, sized to
  the assurance obligations.
- **Change and rollback are architectural.** Favor architectures and
  platforms that make change safe and reversible; this is a
  sustainability requirement, not an operational nicety.

## Applied Design Reasoning

Brief fragment — *"A bank wants a new branch architecture for 900
branches; regulators require the network be manageable and auditable
even during a data-plane outage; the ops team is small and wants to
automate branch turn-up; each branch runs card-processing (segmented)
plus general traffic."* — reasoned:

```text
Requirements: manage/audit during data-plane outage (regulatory);
  automate branch turn-up (small team); segmentation for card data.
Constraints: 900-site scale; small ops team; compliance audit.
Design decisions:
  - Out-of-band management (cellular/secondary path) at every branch,
    because regulators require manageability during a data-plane
    outage -> plane separation is mandatory here, cost accepted.
  - Standardized, templated branch design (one building block x900)
    with model-driven config, because a small team must automate
    turn-up at scale -> automatability is an architectural requirement.
  - Segmentation via overlay (SD-WAN/SD-Access-style) carrying card
    vs general traffic, with end-to-end MTU designed, because PCI
    segmentation is required and the overlay also enables the
    automation.
  - Streaming telemetry to a central assurance platform, because audit
    + a small team need automated evidence and anomaly detection.
  Trade-off: OOB + overlay + telemetry raise per-branch cost x900 ->
  accepted, because regulatory manageability and small-team
  operability are binding, and standardization amortizes the design
  cost across 900 identical sites.
```

## Verification and Design Review

This domain is verified by checking plane-separation decisions against
availability/security requirements; overlay choices against what they
buy (with MTU designed); the design's automatability (standardized,
model-driven, consistent); observability provisioned to the assurance
obligation; and change/lifecycle handled safely. The distinctive
review question: **could a small team actually operate and automate
this at the stated scale** — if not, the design fails sustainability
regardless of technical merit.

## References and Knowledge Checks

- CCDE v3.1 Control, Data, Management Plane, and Operational Design
  (25%)
- Volume IX (automation), Volume XI (observability), Volume XXIX
  (telemetry, model-driven interfaces), Volume XXVII (overlays)

Knowledge checks:

1. Give a requirement that makes out-of-band management mandatory,
   and one context where collapsing it is acceptable.
2. What does an overlay buy, and what does it cost — name the design
   constraint every overlay imposes.
3. Why is automatability an architectural property rather than an
   operational one? Give a design choice that forecloses it.
4. How does observability become part of the design rather than a
   bolt-on, and what sizes it?

## Design Exercise

Take the bank-branch brief (or a large-scale operational design from
your experience) and produce an HLD for the non-control planes: the
plane-separation decisions (OOB, control-plane protection) with their
drivers; the data-plane/overlay choice with MTU handling; the
automation architecture (building blocks, source of truth, model-
driven interfaces) that makes turn-up automatable; and the
observability/assurance design sized to the compliance/operational
obligation. State each as a decision-with-driver-and-cost, and confirm
a small team could run it at scale.

## Lab Verification

The exercise is verified when plane separation matches the
availability/security requirement, overlays are justified with MTU
designed, the architecture is demonstrably automatable at scale,
observability is provisioned to the assurance obligation, and the
result is operable by the named team. Until a reviewer confirms that,
the exercise is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The data and management planes and the operational design are
first-class CCDE concerns: plane separation sized to availability and
security, overlays chosen for what they buy (with MTU designed),
automatability treated as an architectural property, observability
provisioned to assurance obligations, and change and lifecycle made
safe. AI-assisted operations extend this in v3.1. Together with
Chapter 04 this completes the 25% plane-design domain, always tested
against operational sustainability.

- [ ] I decide plane separation from availability and security needs
- [ ] I choose overlays for what they buy and design MTU end to end
- [ ] My designs are automatable — standardized and model-driven
- [ ] I provision observability and prove a small team can operate it
