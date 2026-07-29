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

## Design Exercises

These Design Exercises cover the CCDE **data-plane, management-plane, automation, and operational**
design topics. Work each to a written design, stating every choice as a *decision → driver → cost*
sentence. They share the chapter's **`**Lab verified by:** *pending*`** sign-off.

### Design Exercise 5.1 — QoS design (Topic: Data-plane / QoS)

> **Scenario.** A converged network carries voice, interactive video, business-critical apps, bulk
> replication, and scavenger traffic over congested WAN links. Voice and video have strict SLAs.

Design end-to-end QoS: the **trust boundary** (where marking is trusted vs re-marked); a class model
(how many classes and their mapping to the traffic types); the queuing/scheduling and drop policy
per class; and how the model stays consistent across campus, WAN, and any SD-WAN/overlay. State the
trade-off between the number of classes and operational simplicity.

**Expected result:** a coherent class model with a defined trust boundary, priority queuing for
real-time traffic, and consistent treatment end to end — QoS is a data-plane design decision driven
by application SLAs and link congestion, and the trust boundary is where it starts.

**Common mistake:** trusting markings from untrusted edges, or designing a different class model per
domain; both break end-to-end SLAs — the trust boundary and a single consistent class model are the
design's backbone.

### Design Exercise 5.2 — Multicast or overlay data-plane design (Topic: Data-plane forwarding)

> **Scenario.** A media enterprise distributes live video to thousands of receivers across the WAN,
> and separately runs a data-center overlay (VXLAN/EVPN) for east-west traffic.

Choose one to design: (a) **multicast** — PIM mode (SSM vs ASM), RP placement/redundancy (anycast
RP), and how you scope and scale the trees; or (b) the **overlay data plane** — encapsulation
(VXLAN), the control plane (EVPN) for MAC/IP distribution, and how BUM traffic is handled. Justify
the forwarding model against the traffic pattern.

**Expected result:** a forwarding design matched to the pattern — SSM for well-known one-to-many
sources with anycast-RP redundancy where ASM is needed; or VXLAN/EVPN with a defined BUM strategy —
the data-plane/overlay choice follows the traffic model and its scale.

**Common mistake:** using ASM with a single RP for a large source set (RP is a single point of
failure and suboptimal), or an overlay with no control plane (flood-and-learn) at scale — the
control-plane/redundancy design is what makes the data plane scale.

### Design Exercise 5.3 — Management plane and automation (Topic: Management design)

> **Scenario.** A 500-device network must move from CLI-by-hand to model-driven operations:
> consistent config, telemetry-based monitoring, and safe automated change.

Design the management plane: **in-band vs out-of-band** management (and a hybrid) with its
resilience trade-off; the automation model (source-of-truth/IaC, model-driven config via NETCONF/
YANG, CI/CD with validation gates); and streaming telemetry vs SNMP polling for monitoring. State
how the design makes change safer, not just faster.

**Expected result:** a management design with resilient (ideally out-of-band) reachability,
model-driven automation gated by validation, and telemetry-based observability — the management/
automation plane is a first-class design concern, and safety (rollback, gates) is as important as
speed.

**Common mistake:** automating change with no out-of-band path or validation gates; an automated
bad change can cut the very in-band path used to fix it — OOB reachability and gated rollback are
what make automation safe.

### Design Exercise 5.4 — Operational and Day-2 design (Topic: Operational design)

> **Scenario.** A design must be operable by a modest team: predictable troubleshooting, bounded
> change risk, and clear observability.

Design for operations: how **modularity and consistency** (repeated building blocks, standard
templates) reduce cognitive load; the observability strategy (what is measured, where alerts fire,
how a fault is localized to a module); and the change model (maintenance windows, canary, rollback).
Argue that operability is a design property, not an afterthought.

**Expected result:** a design whose repeated, standardized modules and clear observability make
faults localizable and changes bounded — CCDE explicitly values *operational* design, because a
technically elegant network that the team cannot operate safely has failed a real requirement.

**Common mistake:** optimizing purely for technical elegance or minimal device count while producing
a bespoke, hard-to-troubleshoot network; operability (consistency, observability, bounded change) is
a graded requirement, not a nicety.

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
