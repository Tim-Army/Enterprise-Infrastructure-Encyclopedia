# Chapter 07: L2VPN and EVPN Services

## Learning Objectives

- Explain L2VPN service types: point-to-point pseudowires (VPWS) and
  multipoint bridging (VPLS), and their control planes
- Configure a pseudowire and a VPLS instance on IOS XR
- Explain EVPN: its BGP control plane, route types, and why it
  supersedes legacy L2VPN signaling
- Deliver EVPN services — EVPN-VPWS and EVPN multipoint — with
  all-active multihoming
- Validate MAC learning, redundancy, and forwarding, and troubleshoot
  the L2VPN data and control planes

## Theory and Architecture

### Selling Layer 2 across a Layer 3 core

Some customers buy **Layer 2** transport — the provider carries their
Ethernet frames between sites as if a wire connected them, and the
customer runs their own routing over it. The service types (SPVI's
Layer 2 VPNs, 30%):

- **VPWS (Virtual Private Wire Service)** — a point-to-point
  **pseudowire**: one attachment circuit at each end, frames carried
  transparently. The Ethernet-line product.
- **VPLS (Virtual Private LAN Service)** — a multipoint bridge: many
  sites share one emulated LAN, the provider learns MACs and floods
  BUM traffic. The Ethernet-LAN product.

A **pseudowire** is, again, a label stack: a transport label to the
egress PE (Chapter 04) and a service (PW) label identifying the
circuit — the same two-label pattern as L3VPN, carrying frames instead
of packets.

### The legacy control planes and their limits

Traditional L2VPN signals pseudowires with **targeted LDP** (T-LDP)
and builds VPLS with LDP or BGP auto-discovery. VPLS's weaknesses are
exactly what EVPN fixes: MAC learning is in the **data plane**
(flood-and-learn, no control-plane visibility), multihoming is hard
(active/standby at best, with loop and duplication risks), and there is
no clean all-active redundancy. It works, and it is deployed, and the
exam expects you to recognize it — but new services are EVPN.

### EVPN: the modern L2VPN (and more)

**EVPN** moves MAC/IP learning into **BGP** — the same MP-BGP control
plane as Chapters 03 and 06, with the `l2vpn evpn` address family. It
is the provider-scale sibling of the data-center EVPN in
[Volume XXVII](../volume-27-cisco-data-center/README.md), and the
route types are the shared vocabulary:

- **Type 2** — MAC/IP advertisement: control-plane MAC learning, no
  flooding to learn.
- **Type 3** — inclusive multicast: BUM replication endpoints.
- **Type 1** — Ethernet Auto-Discovery: per-ES and per-EVI,
  underpinning fast withdrawal and aliasing.
- **Type 4** — Ethernet Segment: designated-forwarder election for
  multihoming.

What EVPN delivers that VPLS could not: **all-active multihoming** (a
CE dual-homed to two PEs uses both links, with DF election preventing
loops and aliasing load-balancing flows), control-plane MAC learning
(visibility, faster convergence, MAC mobility handling), and one
control plane for VPWS, multipoint, and integrated routing/bridging.

## Design Considerations

- **EVPN for new services, recognize legacy**: deploy EVPN-VPWS and
  EVPN multipoint; keep the ability to read T-LDP pseudowires and
  VPLS in brownfield estates.
- **Ethernet Segment identifiers (ESI) planned**: multihoming depends
  on consistent ESI configuration across the PEs a CE dual-homes to —
  a design artifact, not an afterthought.
- **BUM and replication**: ingress replication is simple; where
  multicast underlay exists, it scales BUM better — one decision per
  service, consistent within it (the same discipline as Volume XXVII).
- **MTU end to end**: L2 services carry the customer's frames plus
  labels — the Chapter 02/04 MTU discipline is a hard requirement, or
  large customer frames silently drop.

## Implementation and Automation

EVPN-VPWS and an EVPN multipoint instance on IOS XR PEs (on the
Chapter 04 SR transport, `l2vpn evpn` added to the Chapter 03
sessions):

```text
router bgp 65000
 address-family l2vpn evpn

evpn
 interface Bundle-Ether1              ! the dual-homed attachment
  ethernet-segment
   identifier type 0 00.11.22.33.44.55.66.77.88   ! ESI, consistent on both PEs

l2vpn
 xconnect group CUST-C
  p2p EVPN-VPWS-1
   interface GigabitEthernet0/0/0/4
   evpn evi 100 target 10 source 20   ! EVPN-signalled pseudowire
 !
 bridge group CUST-D
  bridge-domain SITE-LAN
   interface GigabitEthernet0/0/0/5
   evi 200                            ! EVPN multipoint (E-LAN)
```

```text
! Validation
show bgp l2vpn evpn                          ! route types 1-4
show evpn ethernet-segment detail            ! DF election, multihoming
show l2vpn xconnect                          ! pseudowire state
show l2vpn bridge-domain detail
show l2route evpn mac all                    ! control-plane MAC learning
```

## Validation and Troubleshooting

Validate the control plane (EVPN routes present — Type 2 for learned
MACs, Type 3 for BUM, Type 4 with a sensible DF election for multihomed
segments), the data plane (frames cross, MACs learned via BGP not
flood — `show l2route evpn mac`), and redundancy (with all-active
multihoming, both PE uplinks forward, and failing one converges fast
via Type-1 withdrawal). Legacy comparison faults still appear:
pseudowire down (`show l2vpn xconnect` — AC down, PW label mismatch,
or transport LSP missing — Chapter 04 again); VPLS MAC flapping
(a loop or a dual-homing done without EVPN's DF protection). EVPN
faults: **inconsistent ESI** across the dual-homed PEs breaks DF
election (duplicate frames or blackholing); **MTU** dropping large
frames while small ones pass (test with sized frames — the L2 analog
of Chapter 04's label-MTU lesson); **MAC mobility** storms if a host
flaps between segments. Method: control plane before data plane,
and prove MAC learning is via BGP to confirm EVPN is actually doing
its job.

## Security and Best Practices

- L2 services extend the customer's broadcast domain across the
  provider — storm control and MAC limits on attachment circuits
  protect the core from a customer's loop.
- EVPN's control-plane learning is itself a hardening: visibility into
  MACs beats flood-and-learn's blindness.
- Attachment-circuit security (the customer edge is untrusted) and
  consistent ESI/DF configuration reviewed as change-controlled
  artifacts.

## References and Knowledge Checks

- SPVI 300-515 v1.1 Layer 2 VPNs (30%), VPN Architecture (25%); SPCOR
  Services (20%)
- Cisco IOS XR L2VPN and EVPN configuration guides
- RFC 7432 (BGP EVPN), RFC 8214 (EVPN-VPWS)

Knowledge checks:

1. Contrast VPWS and VPLS by topology and control plane, and give a
   customer use case for each.
2. Name the four EVPN route types and the job of each in a multihomed
   E-LAN.
3. What does EVPN provide that VPLS cannot, and which route type
   makes all-active multihoming safe?
4. A dual-homed CE sees duplicate frames. Which EVPN construct is
   likely misconfigured, and where do you look?

## Hands-On Lab

On the Chapter 04–06 estate: build an **EVPN-VPWS** point-to-point
service between two PEs and prove transparent frame transport with the
PW label stack visible. Build an **EVPN multipoint** (E-LAN) across
three PEs and prove control-plane MAC learning (`show l2route evpn
mac` — MACs learned via BGP Type-2, not flooded). Dual-home one CE to
two PEs with a consistent ESI and demonstrate **all-active**
forwarding plus fast convergence on uplink failure (Type-1
withdrawal). Break and diagnose: mismatch the ESI between the two PEs
(reproduce the duplicate-frame/DF symptom), and set one AC's MTU low
(reproduce large-frame loss). Restore. For contrast, bring up one
legacy T-LDP pseudowire and read its state, noting the data-plane
learning difference.

## Lab Verification

Verification means EVPN-VPWS and E-LAN both forwarded with
control-plane MAC learning proven, all-active multihoming worked and
converged, and both induced faults (ESI, MTU) were diagnosed by
signature. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

L2VPN sells Ethernet across the core: VPWS as a wire, VPLS as a LAN,
both pseudowires at heart. EVPN moves MAC learning into BGP — the same
control plane as L3VPN — enabling all-active multihoming, visibility,
and one signaling plane for every L2 (and integrated L2/L3) service,
superseding VPLS's flood-and-learn. With Chapter 06 it completes
SPVI's VPN products and SPCOR's Services domain.

- [ ] I can place VPWS, VPLS, and EVPN and justify EVPN for new builds
- [ ] I proved control-plane MAC learning, not flood-and-learn
- [ ] My dual-homed CE forwarded all-active and converged fast
- [ ] I diagnosed ESI and MTU faults from their signatures
