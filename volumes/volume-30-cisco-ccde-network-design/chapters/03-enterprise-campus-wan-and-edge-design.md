# Chapter 03: Enterprise Campus, WAN, and Edge Design

## Learning Objectives

- Apply hierarchical and modular design principles to enterprise
  networks
- Design campus architectures — including fabric (SD-Access) — with
  appropriate resiliency and scale
- Design the WAN and internet edge, including SD-WAN, for cost,
  resilience, and performance
- Reason about failure domains, and size them to availability
  requirements
- Design addressing and summarization strategy at the architecture
  level

## Theory and Architecture

### Hierarchy and modularity: the enduring foundations

CCDE Domain 3 (Network Design, 30%) is the exam's largest, and it
rests on principles that predate every specific technology:

- **Hierarchy** — access, distribution, core (and the collapsed-core
  simplification for smaller sites). Hierarchy bounds failure domains,
  makes traffic patterns predictable, and localizes change. The design
  decision is how many tiers a given site warrants — a three-tier
  campus for a large site is resilient; the same for a 20-user branch
  is waste.
- **Modularity** — the network as building blocks (campus, WAN,
  internet edge, data center, cloud) joined by well-defined
  boundaries, so each can be designed, scaled, and changed with
  bounded blast radius. Modularity is what makes large networks
  operable and Agile delivery (Chapter 02) possible.

These are not dated concepts — SD-Access and spine-leaf are hierarchy
and modularity in modern clothing, and the CCDE tests the principles
beneath the products.

### Campus design

The campus carries users to services, and the design axes are:

- **Topology** — traditional hierarchical Layer 2/3, routed access
  (Layer 3 to the access edge for smaller failure domains and faster
  convergence), or **SD-Access** fabric (a VXLAN overlay with an LISP
  control plane and group-based policy — Volume III's implementation).
  The choice weighs operational familiarity, segmentation needs, and
  scale against complexity.
- **Resiliency** — redundant nodes and links, first-hop redundancy or
  fabric anycast gateways, and convergence design (Chapter 04). The
  question is always "sized to what availability requirement" —
  redundancy is not free.
- **Scale and mobility** — user counts, device density, and roaming;
  wireless is integral (the Workforce Mobility elective, Chapter 08,
  goes deeper).

### WAN and internet edge

The WAN connects sites and is often the largest recurring cost, so it
is where business strategy (Chapter 02) and design meet hardest:

- **Transport options** — MPLS (predictable, SLA-backed, expensive),
  internet (cheap, ubiquitous, best-effort), and hybrids. The modern
  default is **SD-WAN**: an overlay across any transport with
  centralized policy, application-aware routing, and integrated
  segmentation and security — cutting cost while adding capability,
  at the price of a new control plane to operate.
- **Internet edge** — redundant providers, BGP multihoming design,
  address independence (provider-independent space, NAT strategy),
  and where security enforcement lives (Chapter 07).
- **Resilience** — path diversity that is real (two circuits in one
  conduit are one failure), and failover that meets the RTO.

### Failure domains and addressing

Two architecture-level disciplines thread through campus, WAN, and
edge:

- **Failure-domain sizing** — every boundary (a summarization point, a
  fabric border, an area edge) contains failures. Smaller domains
  converge faster and fail smaller but cost more devices and
  complexity; the size is set by the availability requirement.
- **Addressing and summarization** — a hierarchical, summarizable
  addressing plan is what lets the network scale and converge;
  designing it (contiguous blocks per module/region, room for growth,
  IPv6 strategy) is a CCDE deliverable, not an afterthought. Mergers
  (overlapping space) and cloud (address coordination) are the classic
  complications.

## Design Considerations

- **Tier count per site size.** Do not impose three tiers everywhere;
  match hierarchy depth to each site's scale and availability need.
- **Fabric where its policy pays off.** SD-Access earns its complexity
  in estates that will use group-based segmentation and mobility;
  imposing it as a "modern default" without that need buys complexity
  without payoff — the same judgment as ACI in Volume XXVII.
- **SD-WAN as a cost-and-capability decision, staged.** It cuts WAN
  cost and adds segmentation, but respect existing contracts
  (Chapter 02) and the team's ability to operate a new control plane;
  phase it.
- **Summarizable addressing is designed up front.** Retrofitting a
  summarization hierarchy onto a flat plan is a renumbering project;
  design contiguity and growth room from the start.
- **Diversity must be genuine.** Two paths sharing a conduit, a
  building entrance, or a provider POP are one failure domain — verify
  physical diversity, not just logical.

## Applied Design Reasoning

Brief fragment — *"A university wants a campus refresh: 40,000
students and devices, heavy Wi-Fi, research groups needing isolation
from administrative systems, tight capital budget, and a capable but
small central network team."* — reasoned:

```text
Requirements: high-density user/device scale; strong isolation
  (research vs admin); pervasive mobility; low capex; operable by a
  small central team.
Constraints: tight capital budget; small team (operability).
Design decisions:
  - Routed access (Layer 3 to the access) for small failure domains
    and fast convergence, because high density + availability, and it
    is simpler for a small team than a full fabric everywhere.
  - SD-Access fabric ONLY in the zones needing group-based isolation
    (research vs admin), because the segmentation requirement justifies
    its complexity there but not campus-wide (budget + operability).
  - Hierarchical IPv6-capable addressing per building/module,
    summarized at the distribution, because 40k endpoints demand
    summarizable scale.
  Trade-off named: mixing routed-access and fabric zones adds design
  heterogeneity -> accepted, because uniform fabric would exceed both
  budget and the team's operational capacity for the isolation actually
  required.
```

## Verification and Design Review

Campus/WAN/edge design is verified by checking that hierarchy depth
and failure-domain sizes match the availability requirement; that
redundancy and path diversity are real, not nominal; that the
addressing plan is summarizable and has growth room; that any fabric
or SD-WAN adoption traces to a requirement (segmentation, mobility,
cost) rather than fashion; and that the result is operable by the
named team. Review both directions: every requirement served, no
element unjustified.

## References and Knowledge Checks

- CCDE v3.1 Network Design domain (30%)
- Cisco Enterprise campus, SD-Access, and SD-WAN design guides (CVDs)
- Volumes II and III for campus, routing, and SD-Access/SD-WAN
  implementation detail

Knowledge checks:

1. When is routed access the better campus choice than a Layer 2
   access with FHRP, and what requirement decides it?
2. Give two requirements that justify SD-Access fabric and one
   situation where it is over-design.
3. Why must addressing be designed for summarization up front, and
   what does a merger do to that plan?
4. Two WAN circuits are "redundant." What must you verify before
   believing it?

## Design Exercise

Take the university brief (or a campus/WAN refresh from your
experience) and produce an HLD: a module diagram (campus zones, WAN,
internet edge) described in words or a simple sketch; the hierarchy
depth chosen per zone with its justification; the segmentation
approach and where fabric is/ isn't used; a summarizable addressing
strategy with growth room; and the WAN transport decision tied to cost
and resilience requirements. Write each major choice as a
decision-with-driver-and-cost sentence, and review against the brief
both ways.

## Lab Verification

The exercise is verified when hierarchy and failure-domain sizing
match the availability requirement, redundancy/diversity is genuine,
the addressing plan is summarizable with growth room, every
fabric/SD-WAN choice traces to a requirement, and the design is
operable by the named team. Until a reviewer confirms that, the
exercise is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Enterprise network design rests on hierarchy and modularity —
principles beneath every product — sized to availability requirements
through failure-domain and redundancy decisions. Campus choice (routed
access versus fabric), WAN transport (MPLS, internet, SD-WAN), and a
summarizable addressing plan are the core deliverables, each justified
by a requirement or constraint and each operable by the team that will
run it. This is the largest CCDE domain and the heart of the Practical's
Core modules.

- [ ] I size hierarchy and failure domains to availability
      requirements
- [ ] I adopt fabric/SD-WAN only where a requirement justifies the
      complexity
- [ ] My addressing plans are summarizable with growth room
- [ ] I verify path diversity is physical, not just logical
