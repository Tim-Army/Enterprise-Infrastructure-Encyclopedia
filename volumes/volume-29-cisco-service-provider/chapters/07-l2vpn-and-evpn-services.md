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

This chapter carries a topic-level walkthrough lab for **the L2VPN objective of
SPCOR 350-501 v1.1, Domains 1 and 2 of SPVI 300-515 v1.1, and Domain 2 (Cloud
Interconnect) of SPCNI 300-540 v1.0** — mapped in the volume README's coverage
tables. Labs use the IOS XR CLI. Each ends **`**Lab verified by:** *pending*`**
until a human runs it.

**Shared prerequisites for Labs 7.1–7.9** — an IOS XR core with L2VPN/EVPN
enabled, two PEs bridging a customer L2 service, an EVPN control plane over
BGP, and a DCI path for the cloud-interconnect labs. **Cost:** none beyond lab
resources.

### Lab 7.1 — Configure L2VPN and Carrier Ethernet (SPCOR Objective 4.2)

**Objective:** Bring up a point-to-point L2VPN (VPWS xconnect) and verify.

```text
show l2vpn xconnect
show l2vpn xconnect detail | include "state|PW|MTU"
show l2vpn forwarding interface <ac> detail 2>/dev/null | head
```

**Expected result:** the xconnect `UP` with its pseudowire — Carrier Ethernet
delivers E-Line (VPWS point-to-point), E-LAN (VPLS/EVPN multipoint), and E-Tree
services; a VPWS stitches an attachment circuit to a pseudowire across the MPLS/SR
core.

**Negative test:** an xconnect with mismatched MTU or pseudowire-class between PEs
stays down; `show l2vpn xconnect detail` flags the mismatch — the AC/PW parameters
must agree.

**Cleanup:** none (read-only).

### Lab 7.2 — Describe the Layer 2 service architecture (SPVI Objective 1.3)

**Objective:** Read the bridge-domain / EVI service constructs.

```text
show l2vpn bridge-domain summary
show l2vpn bridge-domain bd-name CUST-A detail | include "AC|PW|EVI|MAC"
```

**Expected result:** the bridge domain with its ACs, PWs/EVIs, and MAC table —
the L2 service architecture binds attachment circuits and pseudowires/EVPN
instances into a bridge domain (E-LAN) or xconnect (E-Line), with MAC learning
(data-plane for VPLS, control-plane for EVPN).

**Negative test:** expect MAC scale from a flood-and-learn VPLS bridge domain
equal to EVPN; VPLS floods unknown unicast and learns in the data plane, capping
scale — EVPN's control-plane learning scales further.

**Cleanup:** none (read-only).

### Lab 7.3 — Troubleshoot L2VPN services (SPVI Objective 2.1)

**Objective:** Diagnose a down pseudowire or missing MAC.

```text
show l2vpn xconnect detail | include "state|PW.*down"
show l2vpn forwarding bridge-domain mac-address location 0/RP0/CPU0 2>/dev/null | head
show mpls forwarding prefix <remote-PE>/32
```

**Expected result:** the PW state and MAC table — an L2VPN failure traces to the
AC (down interface/EFP), the PW (label/LSP or class mismatch), or the core LSP;
missing MACs point to a learning/flooding or split-horizon issue.

**Negative test:** blame the customer for absent MACs when the PE-PE LSP is down —
no transport means no PW, so no L2 service; verify the underlay first (as in Lab
6.4).

**Cleanup:** none (read-only).

### Lab 7.4 — Describe EVPN concepts (SPVI Objective 2.2)

**Objective:** Read the EVPN route types on a PE.

```text
show bgp l2vpn evpn summary
show bgp l2vpn evpn route-type 2 | head        ! MAC/IP
show bgp l2vpn evpn route-type 3 | head        ! inclusive multicast
```

**Expected result:** EVPN routes — Type-1 (Ethernet Auto-Discovery, multihoming),
Type-2 (MAC/IP advertisement), Type-3 (inclusive multicast for BUM), Type-4
(Ethernet Segment/DF), Type-5 (IP prefix) — EVPN uses BGP as a unified L2/L3
control plane with multihoming and MAC mobility.

**Negative test:** expect L2 reachability with EVPN peers up but no Type-3 routes;
without inclusive-multicast routes BUM traffic has no path — Type-3 must be present
for flooding.

**Cleanup:** none (read-only).

### Lab 7.5 — Implement Ethernet OAM (SPVI Objective 2.3)

**Objective:** Verify E-OAM (CFM/link OAM) on a service.

```text
show ethernet cfm peer meps
show ethernet cfm local meps detail | include "MEP|CCM|status"
show ethernet oam summary 2>/dev/null
```

**Expected result:** CFM peer MEPs up and CCMs exchanged — Ethernet OAM provides
service (CFM: continuity check, loopback, linktrace across the service) and link
(802.3ah) fault management, so the SP can detect and localize L2 service faults
end to end.

**Negative test:** CFM MEPs at mismatched maintenance levels or domains do not see
each other; continuity check fails though the service forwards — the MD level/MA
must match.

**Cleanup:** none (read-only).

### Lab 7.6 — Implement EVPN (SPVI Objective 2.4)

**Objective:** Bring up an EVPN ELAN and verify control-plane MAC learning.

```text
show evpn evi detail
show l2route evpn mac all 2>/dev/null | head
show bgp l2vpn evpn route-type 2 | include <customer-mac>
```

**Expected result:** the EVI with MACs learned as Type-2 routes — EVPN implements
the L2 service with BGP advertising MAC/IP (Type-2), so remote MACs are learned
via the control plane (not flooding), with aliasing and mass-withdrawal for
multihoming.

**Negative test:** a MAC learned locally but not advertised (Type-2 missing) is
unreachable remotely; check the EVI's BGP export — control-plane advertisement is
what makes EVPN scale.

**Cleanup:** none (read-only).

### Lab 7.7 — Describe carrier-neutral facilities (SPCNI Objective 2.1)

**Objective:** Read the peering/interconnect at a carrier-neutral facility.

```text
show bgp ipv4 unicast summary | include <ixp-peer>
show bgp ipv4 unicast neighbors <ixp-peer> | include "state|Description"
```

**Expected result:** the peering sessions at the exchange — a **carrier-neutral
facility** (colocation/IXP) is where many networks interconnect; the SP peers over
a shared fabric (public peering at a route server, or private cross-connects) to
exchange traffic without a transit provider.

**Negative test:** rely solely on a route-server (public) peering for critical
traffic; a private interconnect (PNI) gives dedicated capacity and better control
— the facility offers both, chosen by traffic volume.

**Cleanup:** none (read-only).

### Lab 7.8 — Evaluate WAN infrastructure connectivity (SPCNI Objective 2.2)

**Objective:** Read the WAN uplinks and their capacity/redundancy.

```text
show interface | include "line protocol|rate"
show bundle | include "Active|bandwidth"
show bgp ipv4 unicast summary | include <transit-peer>
```

**Expected result:** the WAN links, bundles, and transit sessions — evaluating WAN
connectivity for cloud interconnect weighs capacity (bundled uplinks), redundancy
(diverse paths/providers), and the connection type (dedicated, IP transit, cloud
on-ramp) against cost and SLA.

**Negative test:** a single high-bandwidth uplink with no diverse second path is a
single point of failure regardless of speed — redundancy, not just capacity, is
the WAN requirement.

**Cleanup:** none (read-only).

### Lab 7.9 — Troubleshoot DCI solutions (SPCNI Objective 2.3)

**Objective:** Diagnose a Data Center Interconnect (EVPN/L2 stretch) fault.

```text
show evpn evi detail | include "EVI|multicast"
show bgp l2vpn evpn route-type 3
show l2vpn bridge-domain bd-name DCI-A detail | include "PW|EVI|state"
```

**Expected result:** the DCI EVPN/bridge-domain state — DCI stretches L2/L3 between
data centers (EVPN over MPLS/SR or VXLAN); a fault traces to the EVPN control plane
(missing Type-2/3), the transport LSP, or a mismatched EVI/VNI between sites.

**Negative test:** stretch L2 across sites without storm control / BUM optimization
and a broadcast storm in one DC crosses the DCI to the other — DCI needs
BUM/storm controls, unlike an intra-DC fabric.

**Cleanup:** none (read-only).

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
