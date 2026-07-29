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

## Design Exercises

These Design Exercises cover the CCDE enterprise **campus, WAN, and edge** design topics. Work each
to a written High-Level Design, stating every major choice as a *decision → driver → cost* sentence
and reviewing against the brief both ways. They share the chapter's **`**Lab verified by:**
*pending*`** sign-off.

### Design Exercise 3.1 — Campus hierarchy and fabric (Topic: Campus design)

> **Scenario.** A university refreshes a 12,000-port campus across eight buildings: mixed staff,
> student, IoT, and guest devices; a mandate to segment these populations; and a five-year growth
> allowance of 40%.

Produce an HLD: a module diagram (campus zones, distribution/core, WAN, internet edge); the
hierarchy depth per zone (two-tier collapsed core vs three-tier) with justification; the
segmentation approach and **where a fabric (SD-Access/EVPN) is and is not warranted**; a
summarizable addressing plan with growth room; and how wired/wireless converge.

**Expected result:** a hierarchy and segmentation design justified by size, growth, and the
segmentation mandate — a fabric where policy-based macro/micro-segmentation across many device
classes earns its complexity, and simpler L2/L3 where it does not.

**Common mistake:** deploying a fabric everywhere because it is modern; the added control-plane and
operational complexity must be justified by a real segmentation/mobility requirement, not adopted by
default.

### Design Exercise 3.2 — WAN transport and resilience (Topic: WAN design)

> **Scenario.** 60 branches connect to two data centers and cloud. Requirements: sub-second failover
> for voice, internet-direct breakout for SaaS, and a 30% transport-cost reduction target.

Design the WAN: transport mix (MPLS, internet, LTE/5G backup) per branch tier; **SD-WAN vs
traditional routing** and what it buys against its cost; the path-selection and failover model that
meets the voice SLA; and where local internet breakout is safe. Tie the transport choice to the
cost-reduction and resilience drivers.

**Expected result:** a transport and overlay design where SD-WAN's application-aware path selection
and internet breakout are justified by the SaaS/cost/resilience requirements — the WAN decision is
driven by cost, application SLAs, and resilience, each traded explicitly.

**Common mistake:** keeping expensive MPLS everywhere "for reliability" while the requirement is
cost reduction with a voice SLA; a hybrid with tested failover often meets the SLA at lower cost —
the design must serve the stated cost driver.

### Design Exercise 3.3 — Internet edge and DMZ (Topic: Edge design)

> **Scenario.** An enterprise consolidates three internet edges into one hardened edge serving
> inbound web services, outbound user traffic, and site-to-site/remote-access VPN, with a DDoS and
> resilience requirement.

Design the internet edge: the security zones (outside/DMZ/inside) and what lives in each; redundancy
(dual ISP, BGP multihoming or a simpler model) and its failover behavior; DDoS mitigation placement;
and how inbound services, outbound traffic, and VPN termination are separated. State the
availability and blast-radius consequences.

**Expected result:** a layered edge with clear zones, ISP redundancy sized to the availability
requirement, and DDoS mitigation positioned before the assets it protects — the internet edge is a
concentrated risk, so zoning and resilience are the primary design drivers.

**Common mistake:** collapsing inbound services, user traffic, and VPN onto one undifferentiated
edge; a compromise or overload in one then affects all — separation of function at the edge bounds
the blast radius.

### Design Exercise 3.4 — Addressing and summarization (Topic: Addressing strategy)

> **Scenario.** Design the IPv4/IPv6 addressing for the multi-site enterprise above, anticipating
> mergers, cloud, and 40% growth.

Produce an addressing strategy: a hierarchical, summarizable allocation that aligns to the topology
(so summarization boundaries match routing/failure domains); IPv6 alongside IPv4; room for growth
and acquisitions; and how overlap with a future acquisition would be handled. Explain how the plan
supports summarization and thus routing scalability.

**Expected result:** a hierarchical addressing plan whose boundaries enable route summarization at
the distribution/WAN edges, containing routing-table size and failure propagation — addressing is a
design decision that determines routing scalability, not an afterthought.

**Common mistake:** allocating addresses flatly or by first-come; without hierarchy you cannot
summarize, so routing tables and failure domains grow unbounded — the addressing plan must be
designed to summarize.

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
