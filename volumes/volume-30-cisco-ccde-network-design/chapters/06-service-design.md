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

## Design Exercise

Take the media-distribution brief (or a service-design scenario from
your experience) and produce a service HLD: the segmentation design
matched to requirement granularity; an end-to-end QoS class model with
trust boundaries and class sizing; a multicast design (if the
application needs it) with RP redundancy; the SD-WAN/SD-Access decision
tied to used capabilities; and the assurance design for any SLA. Write
each as a decision-with-driver-and-cost and review against the brief
both ways.

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
