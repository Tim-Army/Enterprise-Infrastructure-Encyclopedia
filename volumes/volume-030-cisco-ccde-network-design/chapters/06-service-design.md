# Chapter 06: Service Design

## Learning Objectives

- Design network services — VPNs, overlays, and segmentation — to
  business requirements
- Design QoS as an end-to-end architecture, not a device feature
- Design multicast where the application demands it
- Design SD-WAN and SD-Access as service architectures, weighing
  their capabilities against complexity
- Reason about service assurance and the service-level obligations a
  design must meet

## Theory and Architecture

### Services are what the network delivers

CCDE Domain 4 (Service Design, 15%) is about the products the network
provides to its users and applications — connectivity with specific
properties (isolation, priority, replication) — designed to
requirements. Where Chapters 03–05 designed the infrastructure, this
chapter designs what rides on it.

### VPN and segmentation services

Segmentation is the recurring service requirement — regulatory
(PCI, HIPAA), organizational (research vs admin, tenant vs tenant),
or security (zero-trust microsegmentation, Chapter 07). The design
choices span layers:

- **L3VPN/VRF** — routed isolation, overlapping address support
  (Volume XXIX, Chapter 06); the enterprise sees it in MPLS WANs and
  as VN/VRF in SD-Access.
- **L2VPN/EVPN** — Layer 2 extension and data-center interconnect
  (Volume XXVII, XXIX); designed carefully because extending broadcast
  domains extends failure domains.
- **Group-based segmentation** — SD-Access's scalable group tags
  (SGTs) decouple policy from topology and addressing — powerful for
  large, mobile, policy-rich estates, complex for simple ones.

The design matches the segmentation mechanism to the requirement's
granularity and the estate's scale and operability — the same "does
the payoff justify the complexity" judgment as fabric adoption.

### QoS as architecture

QoS is a design domain, not a knob: an **end-to-end** model where
traffic is classified and marked at trusted edges, queued consistently
across every hop, and admitted within capacity. The CCDE designs the
class model (how many classes, what each guarantees), the trust
boundaries (where marking is believed vs re-marked), and the admission
strategy (call admission control, over-provisioning) — sized to the
applications' real needs. Real-time media and, increasingly, storage/
AI traffic (Volume XXVII) drive the strictest requirements. The design
principle: QoS manages contention; if there is no contention it does
nothing, and if the class model is inconsistent hop-to-hop it does
worse than nothing.

### Multicast

Where an application replicates one-to-many (market data, IPTV,
imaging, some AI patterns), **multicast** is a service to design: the
PIM model, RP placement and redundancy, and (across VPNs) mVPN
(Volume XXIX, Chapter 08). Multicast is designed only where the
application needs it — imposing it elsewhere is complexity without
benefit.

### SD-WAN and SD-Access as service architectures

These are not just transport (Chapter 03) — they are **service
platforms**: centralized policy, application-aware routing,
integrated segmentation and security, and assurance. Designing with
them means designing the policy model and the controller architecture,
and weighing their considerable capability against a new control plane
and skill requirement. The recurring decision: adopt where the policy/
segmentation/assurance capabilities are needed and will be used;
otherwise their complexity is unpaid-for.

### Service assurance

A service with an SLA needs a design that can *prove* it is met —
telemetry (Chapter 05), synthetic testing, and per-service monitoring.
Assurance is designed alongside the service, not after.

## Design Considerations

- **Segmentation mechanism to requirement granularity.** VRF/L3VPN for
  routed isolation; group-based (SGT) for policy-rich, mobile, large
  estates; do not impose SGT complexity where a handful of VRFs
  suffice.
- **QoS is end-to-end or it is nothing.** A consistent class model and
  trust boundaries across every hop; an inconsistent model is worse
  than none. Size classes to real application needs.
- **Multicast only where applications replicate.** Design RP
  redundancy and mVPN where needed; do not carry multicast complexity
  for its own sake.
- **SD-WAN/SD-Access for their policy and assurance, not as default.**
  Adopt where the capabilities are used; account for the controller
  architecture and skills.
- **Assurance is part of the service design.** If the service has an
  SLA, design how it is proven met.

## Applied Design Reasoning

Brief fragment — *"A media company distributes live video to 200
sites, needs strict latency/jitter for the video, has a separate
corporate traffic class, wants central policy control, and must prove
SLA compliance to content partners."* — reasoned:

```text
Requirements: one-to-many live video (replication); strict latency/
  jitter for video; separation of video vs corporate; central policy;
  provable SLA.
Constraints: 200-site scale; partner-facing SLA (assurance is
  contractual).
Design decisions:
  - Multicast for the live video distribution (one-to-many at 200
    sites -> replication in the network, not 200 unicast streams),
    with redundant RPs and mVPN across the WAN.
  - End-to-end QoS: a strict-priority class for video sized to the
    stream rate, corporate in a separate guaranteed class, consistent
    marking/trust from ingest to every site.
  - SD-WAN for central application-aware policy and integrated
    assurance, because central policy + provable SLA are explicit
    requirements and 200 sites justify the controller model.
  - Per-service assurance (synthetic video probes + streaming
    telemetry) feeding SLA reports, because compliance is contractual.
  Trade-off: multicast + SD-WAN + assurance pipeline is significant
  design complexity -> accepted, because replication efficiency,
  strict media QoS, central policy, and provable SLA are all explicit
  requirements that simpler designs cannot meet.
```

## Verification and Design Review

Service design is verified by matching each service to a requirement
(segmentation granularity, QoS classes, multicast need) without
over-building; confirming QoS is consistent end-to-end with sane trust
boundaries; confirming SD-WAN/SD-Access adoption traces to used
capabilities; and confirming any SLA has a designed assurance
mechanism. Review both directions: every service requirement met, no
service complexity unjustified.

## References and Knowledge Checks

- CCDE v3.1 Service Design domain (15%)
- Volume III (QoS, SD-Access, SD-WAN), Volume XXIX (L3VPN/L2VPN/EVPN,
  multicast/mVPN), Volume XXVII (data-center services)

Knowledge checks:

1. Match a segmentation mechanism to each of: routed isolation with
   overlapping space; policy-rich mobile campus; simple two-tenant
   split.
2. Why is an inconsistent end-to-end QoS model worse than no QoS, and
   what two design elements make it consistent?
3. When is multicast the right service design, and when is it
   needless complexity?
4. Name two capabilities that justify SD-WAN as a service platform
   rather than just cheaper transport.

## Design Exercises

These Design Exercises cover the CCDE **service design** topics — overlay/VPN services, SD-WAN, and
multi-tenancy. Work each to a written design, stating every choice as a *decision → driver → cost*
sentence. They share the chapter's **`**Lab verified by:** *pending*`** sign-off.

### Design Exercise 6.1 — L3VPN / EVPN service design (Topic: VPN services)

> **Scenario.** A service provider (or large enterprise acting as one) must offer isolated L3
> connectivity to 200 tenants over a shared core, with per-tenant routing and the ability to add
> tenants without touching the core.

Design the VPN service: **MPLS L3VPN vs EVPN** as the technology with its driver; the PE/CE model
and how tenant routes are kept isolated (VRFs, route-targets/route-distinguishers); how a new tenant
is provisioned at the edge only; and the scaling limits (VRF/route counts, RR capacity). State the
operational cost per tenant.

**Expected result:** a VPN service where per-tenant isolation lives in edge VRFs with RT/RD-based
import/export, the shared core is tenant-unaware, and adding a tenant is an edge-only operation —
the service design's value is isolation plus edge-only provisioning at scale.

**Common mistake:** carrying per-tenant state into the core (core must know every tenant); it does
not scale and every tenant change touches the core — the design keeps tenant state at the edge.

### Design Exercise 6.2 — SD-WAN service design (Topic: SD-WAN services)

> **Scenario.** An enterprise wants a managed overlay service across 300 sites: centralized policy,
> application-aware path selection, integrated security, and multi-cloud on-ramps.

Design the SD-WAN service: the **overlay control/orchestration model** (controllers/orchestrator and
their placement/redundancy); the policy model (application-aware routing, segmentation across the
overlay); how transport independence and failover are achieved; and cloud/SaaS on-ramp integration.
State the trade-off (centralized control simplicity vs controller dependency).

**Expected result:** a service design with redundant, well-placed control/orchestration, a
centralized application-aware policy model, transport-independent overlays with tested failover, and
defined cloud on-ramps — SD-WAN's value is centralized policy and application-awareness, and the
controller's resilience is the key risk to design around.

**Common mistake:** designing the data plane thoroughly but treating the controller/orchestrator as
an afterthought; its loss or a control-plane partition degrades policy for the whole overlay —
control-plane placement and redundancy are central to the service design.

### Design Exercise 6.3 — Multi-tenancy and segmentation service (Topic: Segmentation services)

> **Scenario.** A shared enterprise fabric must serve corporate, OT/industrial, guest, and partner
> traffic with strong isolation and per-segment policy, offered as an internal service.

Design the segmentation service: the **macro-segmentation** model (VRFs/VNs for the top-level tenants)
and **micro-segmentation** within them (group-based policy/SGTs); how policy is expressed and
enforced consistently across campus/DC/WAN; and how a new segment is onboarded. State the trade-off
between isolation strength and operational/policy complexity.

**Expected result:** a two-tier segmentation service (macro VRF/VN isolation plus micro group-based
policy) with a consistent, centrally-defined policy model — segmentation-as-a-service scales when the
isolation is hierarchical and the policy is expressed by group/intent rather than per-ACL.

**Common mistake:** implementing segmentation as sprawling per-device ACLs; it is unmaintainable and
inconsistent across domains — a hierarchical, intent/group-based model is what makes segmentation a
scalable service.

## Lab Verification

The exercise is verified when each service traces to a requirement
without over-building, QoS is end-to-end consistent with sane trust
boundaries, multicast (if used) is justified and RP-redundant,
SD-WAN/SD-Access adoption maps to used capabilities, and every SLA has
a designed assurance mechanism. Until a reviewer confirms that, the
exercise is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Service design delivers what the network is for: segmentation matched
to requirement granularity, QoS as an end-to-end architecture,
multicast where applications replicate, and SD-WAN/SD-Access adopted
for their policy and assurance capabilities — each justified, none
gold-plated, and every SLA paired with a designed way to prove it.

- [ ] I match segmentation mechanisms to requirement granularity
- [ ] My QoS is consistent end-to-end with deliberate trust boundaries
- [ ] I design multicast only where applications replicate
- [ ] Every SLA in my design has a designed assurance mechanism
