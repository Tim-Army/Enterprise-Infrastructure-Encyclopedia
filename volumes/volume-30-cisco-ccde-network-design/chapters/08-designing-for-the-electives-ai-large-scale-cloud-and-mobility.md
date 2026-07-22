# Chapter 08: Designing for the Electives: AI, Large-Scale, Cloud, and Mobility

## Learning Objectives

- Explain the CCDE Practical's elective model and how to choose an
  elective
- Design AI infrastructure at the architecture level (the AI
  Infrastructure elective)
- Design massive-scale networks (the Large Scale Networks elective)
- Design hybrid and multicloud connectivity (the On-Prem and Cloud
  Services elective)
- Design for the mobile and distributed workforce (the Workforce
  Mobility elective)

## Theory and Architecture

### The elective model

The CCDE Practical's first three modules are Core Enterprise; the
**fourth module is your selected elective**, chosen at the start of
the exam. There are four, and each is a design specialization with its
own technology list. You design against the same five domains
(business, planes, network, service, security) but in the elective's
context. This chapter surveys all four at design level so a reader can
choose and then go deep; each maps to a technology volume of this
encyclopedia for the implementation detail.

Choosing an elective is itself a decision: pick the one matching your
experience and the designs you actually do, because the Practical
rewards depth of design judgment in that area.

### AI Infrastructure elective

New prominence in v3.1. Designing infrastructure for AI/ML workloads
(the implementation is [Volume XXVII, Chapter 07](../volume-27-cisco-data-center/chapters/07-data-center-ai-infrastructure.md)):

- **The workload drives everything** — training's synchronized
  collective traffic makes **non-blocking, lossless** backend fabrics
  and **tail latency** the design metric; inference has its own
  latency-at-scale profile.
- **Design decisions** — rails-aligned backend fabric sizing (1:1
  oversubscription — the one place it is mandatory), RoCEv2 with
  PFC/ECN as a design requirement, GPU-scale power and cooling as
  facilities constraints that lead the design, and the storage
  pipeline that keeps GPUs fed.
- **Business framing** — the CCDE lens: the business wants AI
  capability; the designer translates that into fabric, power, and
  data-pipeline requirements and their considerable cost, and sizes
  them to the actual model/cluster scale rather than a generic maximum.

### Large Scale Networks elective

Designing at service-provider and hyperscale magnitudes (implementation
in [Volume XXIX](../volume-29-cisco-service-provider/README.md)):

- **Scale techniques as design** — hierarchy, route
  summarization/reflection, and **segment routing** (SR-MPLS/SRv6) to
  remove per-flow core state; the design chooses these because flat
  approaches collapse at scale.
- **Massive multi-tenancy** — L3VPN/EVPN at tens of thousands of
  instances, designed for isolation and operability.
- **Convergence and TE at scale** — TI-LFA and SR-TE as design
  requirements for SLA-grade restoration across a large topology.
- **Automation as survival** — at this scale the design *must* be
  automatable (Chapter 05), which constrains the architecture toward
  consistency and model-driven operation.

### On-Prem and Cloud Services elective

Designing hybrid and multicloud connectivity:

- **Cloud connectivity** — direct-connect/ExpressRoute-class private
  links versus VPN-over-internet, and the redundancy/latency design
  for each; cloud on-ramps and their placement.
- **Multicloud** — consistent policy, segmentation, and routing across
  providers whose native networking differs; the design abstracts the
  differences (SD-WAN/cloud-network overlays) or embraces per-cloud
  native design deliberately.
- **Addressing and DNS across the hybrid boundary** — the unglamorous
  design work that makes or breaks cloud migrations (overlapping
  space, split-horizon DNS, service discovery).
- **Workload placement** — the design influences and responds to where
  workloads live (latency to users, data gravity, egress cost — cloud
  egress charges are a real design constraint).

### Workforce Mobility elective

Designing for users and devices anywhere:

- **Wireless design** — high-density campus Wi-Fi (Wi-Fi 6/7),
  roaming, and location services (the CCNP Wireless implementation is
  [Volume III, the CCNP Wireless track](../volume-03-cisco-enterprise-networking/README.md)).
- **Remote and hybrid access** — SASE/SSE, VPN-less zero-trust access
  (Chapter 07), and enforcement that follows the user (no backhaul).
- **Unified policy** — one policy model for on-prem, remote, and
  cloud access, so a user's entitlements are consistent wherever they
  connect.
- **Experience and assurance** — designing for measurable user
  experience (the mobile workforce's "is it the network" is a design
  and assurance question).

## Design Considerations

- **Design the elective in the five-domain frame.** Even a deeply
  technical elective is still business-aligned, plane-designed,
  serviced, and secured — do not drop the CCDE method because the
  topic is specialized.
- **AI: facilities and non-blocking lead.** Power/cooling and 1:1
  fabric are the leading constraints, sized to real cluster scale, not
  aspiration.
- **Large-scale: automatability and state-removal are architectural.**
  Choose SR and consistency because scale forbids the alternatives.
- **Cloud: the boring layers decide success.** Addressing, DNS, and
  egress cost are where hybrid designs live or die — design them
  explicitly.
- **Mobility: policy follows the user.** Consistent, backhaul-free
  enforcement is the defining requirement.

## Applied Design Reasoning

Choosing and framing an elective — brief fragment: *"A pharmaceutical
company is standing up AI drug-discovery clusters and wants the network
design; the same brief mentions hybrid cloud for burst compute and a
mobile research workforce."* — reasoned:

```text
Elective choice: AI Infrastructure is the primary ask (drug-discovery
  clusters) -> select it; but the brief touches cloud burst and
  mobility, so the Core modules and cross-elective awareness matter.
AI-elective design decisions (five-domain frame):
  - Business: the business wants faster discovery -> justify cluster
    scale and its cost against that outcome; size to the model scale,
    not a generic maximum.
  - Network/plane: non-blocking rails-aligned backend fabric, RoCEv2
    lossless design, OOB management; power/cooling lead the facilities
    design.
  - Service: the data pipeline (fast storage to feed GPUs) and burst
    connectivity to cloud (On-Prem and Cloud awareness) as designed
    services.
  - Security: training data and models are crown jewels -> segment and
    protect the cluster (Chapter 07), zero-trust access for the mobile
    researchers.
  Trade-off: a 1:1 non-blocking AI fabric plus facilities uplift is
  very costly -> accepted and sized to the actual cluster, because the
  workload's collective-traffic profile makes oversubscription a
  design failure.
```

## Verification and Design Review

Elective design is verified the same way as the core domains — every
decision traced to a requirement or constraint, trade-offs stated —
plus the elective-specific checks: AI (non-blocking backend, lossless
transport, facilities sized to real scale); large-scale (state-removal
and automatability as architecture); cloud (addressing/DNS/egress
designed, redundant on-ramps); mobility (policy follows the user,
no backhaul, measurable experience). And the elective still passes the
full five-domain review — specialization does not excuse missing the
business, security, or operability dimensions.

## References and Knowledge Checks

- CCDE v3.1 elective technology lists (AI Infrastructure, Large Scale
  Networks, On-Prem and Cloud Services, Workforce Mobility)
- Volume XXVII (AI infrastructure, data center), Volume XXIX
  (large-scale/SP), Volume VII (cloud), Volume XVI/X (mobility/SASE),
  Volume III (wireless)

Knowledge checks:

1. How should you choose which CCDE elective to take, and why does it
   matter for the Practical?
2. In the AI elective, why is oversubscription on the backend fabric a
   design failure, and what leads the facilities design?
3. Name the "boring" design layers that most often decide hybrid-cloud
   success.
4. What is the defining requirement of workforce-mobility design, and
   what architecture pattern meets it?

## Design Exercise

Choose one elective matching your experience. Take a brief in that
area (or one from your work) and produce an elective HLD *in the full
five-domain frame*: business justification and sizing; the plane/
network design specific to the elective (AI fabric, large-scale
state-removal, cloud connectivity, or mobility access); the services
and security design; and the operational/assurance design. Explicitly
size the elective's signature cost driver (AI facilities, large-scale
automation, cloud egress, mobility policy plane) to the real
requirement. Review both directions.

## Lab Verification

The exercise is verified when the elective design passes the full
five-domain review, the elective-specific requirements are met (per
the review checks above), and the signature cost driver is sized to
the real requirement rather than a generic maximum. Until a reviewer
confirms that, the exercise is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Practical's fourth module is a chosen elective — AI Infrastructure,
Large Scale Networks, On-Prem and Cloud Services, or Workforce
Mobility — each a design specialization approached through the same
five-domain CCDE method. Choose the one matching your design
experience, go deep, and remember that specialization never excuses
dropping the business, service, security, or operability dimensions.

- [ ] I can frame each elective in the five-domain method
- [ ] I chose an elective matching my real design experience
- [ ] I can size each elective's signature cost driver to requirements
- [ ] My elective designs still pass a full five-domain review
