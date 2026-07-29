# Chapter 06: L3VPN Services

## Learning Objectives

- Explain the MPLS L3VPN model: VRFs, route distinguishers, route
  targets, and the VPNv4/VPNv6 address families
- Configure a PE for L3VPN: VRF definition, PE-CE routing, and MP-BGP
  route exchange
- Design PE-CE routing with each protocol option and explain their
  route-import behavior
- Deliver IPv6 L3VPN (6VPE) and explain how it reuses the same
  machinery
- Validate customer isolation and reachability, and troubleshoot the
  L3VPN control and data planes

## Theory and Architecture

### The L3VPN idea

An **MPLS L3VPN** sells a customer a private routed network across the
shared provider core, with the provider participating in the
customer's routing. It is the flagship provider service and the bulk
of SPVI (Layer 3 VPNs, 35%). The mechanism composes Chapters 02–04:

- **VRF (VPN Routing and Forwarding)** on the PE — a per-customer
  routing table and interface set, so customer A and customer B are
  isolated even with overlapping address space.
- **Route Distinguisher (RD)** — prepended to a customer prefix to
  make it globally unique in BGP (customer A's 10.0.0.0/8 and customer
  B's 10.0.0.0/8 become different VPNv4 routes). The RD makes prefixes
  unique; it does **not** control import/export — a perennial exam
  trap.
- **Route Target (RT)** — the extended community that *does* control
  which VRFs import which routes. Export RTs tag routes; import RTs
  select them. RT design is VPN topology: hub-and-spoke, any-to-any,
  and extranet are all RT policies.
- **VPNv4/VPNv6 address families** — MP-BGP (Chapter 03) carries the
  RD+prefix with its RT and a **VPN label**; the transport label
  (Chapter 04) gets the packet to the egress PE, and the VPN label
  tells that PE which VRF to use. Two labels, two jobs.

### The end-to-end path

A CE sends a packet to its PE; the ingress PE looks up the VRF, imposes
the VPN label (inner) and the transport label to the egress PE (outer),
and the core label-switches on the outer label alone — ignorant of the
customer route. The egress PE pops to the VPN label, which selects the
VRF, and forwards to the correct CE. This is why Chapter 04 insisted IP
reachability and label reachability are different questions: an L3VPN
needs the label path, not just the route.

### PE-CE routing

The PE and CE exchange the customer's routes by:

- **Static** — simplest, for stable stub sites.
- **eBGP** — the most common and flexible; the customer runs a
  private AS, and AS-override or SoO handles the AS-path loop concerns
  of hub-and-spoke.
- **OSPF** — with the VPN "sham link" and domain-ID handling so the
  provider backbone looks like a super-backbone; the down-bit prevents
  loops.
- **EIGRP / RIP** — supported where the customer runs them.

Each redistributes into MP-BGP at the PE; SPVI expects you to know the
import behavior and loop-prevention specifics of each.

### IPv6 L3VPN (6VPE)

**6VPE** delivers IPv6 L3VPN over the same MPLS core using the
**VPNv6** address family — same RDs, RTs, and two-label forwarding,
IPv6 prefixes. It reuses everything, which is the point and the exam's
framing (SPVI's IPv6 VPNs, 10%): no new transport, one more address
family.

## Design Considerations

- **RT scheme is the VPN topology**: document RT allocation
  (any-to-any uses one RT per VPN; hub-and-spoke uses separate hub-
  export/spoke-import RTs) — ad-hoc RTs become unmanageable at scale.
- **RD per PE-per-VRF (unique RDs)** aids troubleshooting and enables
  BGP best-path to keep multiple PE copies of a route (multihoming);
  a single RD per VPN is simpler but loses that.
- **PE-CE protocol per customer need**: eBGP as the flexible default;
  match the customer's existing IGP only when required, and know its
  loop-prevention knobs.
- **Scale the VRF/label/route counts**: PEs have limits; distribute
  customers and use RT-constrain to avoid importing VPNv4 routes a PE
  does not need.

## Implementation and Automation

L3VPN on the Chapter 03 PEs — a customer VRF, eBGP PE-CE, any-to-any:

```text
vrf CUST-A
 address-family ipv4 unicast
  import route-target 65000:100
  export route-target 65000:100
 address-family ipv6 unicast          ! 6VPE, same RTs
  import route-target 65000:100
  export route-target 65000:100

router bgp 65000
 vrf CUST-A
  rd 10.0.0.1:100                      ! unique per PE
  address-family ipv4 unicast
   redistribute connected
  neighbor 192.0.2.2                   ! the CE
   remote-as 64512
   address-family ipv4 unicast
    route-policy CE-IN in
    route-policy CE-OUT out
    as-override                        ! hub-spoke AS-path handling

interface GigabitEthernet0/0/0/3
 vrf CUST-A
 ipv4 address 192.0.2.1 255.255.255.252
```

```text
! Validation — control plane then data plane then isolation
show bgp vpnv4 unicast rd 10.0.0.1:100
show route vrf CUST-A
show bgp vpnv4 unicast summary
show mpls forwarding                          ! VPN + transport labels
! Prove isolation: CUST-B must NOT see CUST-A routes
show route vrf CUST-B
```

## Validation and Troubleshooting

Validate in three layers — control, data, isolation — and the third
is the one that matters for a *multi-tenant* product. **Control**:
the CE's routes appear in the VRF and as VPNv4 routes with the right
RD/RT (`show bgp vpnv4`), and the remote PE imports them by RT. **Data**:
the label path resolves — the classic "routes present, traffic fails"
L3VPN fault is a transport-label gap (Chapter 04): the VPN route is
learned but the transport LSP to the egress PE is missing, so the two-
label stack cannot form. **Isolation**: prove the negative — CUST-B's
VRF does not contain CUST-A's routes, and a CUST-A CE cannot reach
CUST-B. Faults cluster around RTs (import RT typo → routes exported but
nobody imports them → "my other site can't see me"); RD confusion
(expecting the RD to filter — it does not); PE-CE loop-prevention
(OSPF down-bit, BGP AS-path in hub-spoke); and next-hop/label
reachability between PEs.

## Security and Best Practices

- Isolation is the product's security guarantee: test it explicitly
  per VPN (prove-the-negative), because a route leak between customers
  is the worst failure an SP can ship.
- Per-VRF route limits (`maximum prefix` inside the VRF) so one
  customer's misconfiguration cannot exhaust PE resources.
- PE-CE eBGP with the Chapter 03 discipline — inbound/outbound policy,
  maximum-prefix — because the CE is the customer's, i.e., untrusted.
- Management and route-target schemes documented and change-
  controlled; an RT edit can merge two customers' networks.

## References and Knowledge Checks

- SPVI 300-515 v1.1 Layer 3 VPNs (35%), VPN Architecture (25%), IPv6
  VPNs (10%); SPCOR Services (20%)
- Cisco IOS XR L3VPN configuration guide
- RFC 4364 (BGP/MPLS IP VPNs), RFC 4659 (6VPE)

Knowledge checks:

1. State precisely what the RD does and does not do, and what
   actually controls VPN import/export.
2. A customer's two sites cannot see each other though both PEs show
   the VRF up. Name the two most likely RT/label causes.
3. Trace the two-label stack for a CUST-A packet across the core and
   say what each label is for.
4. How does 6VPE reuse the L3VPN machinery, and what is genuinely
   new about it?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **the L3VPN objectives of
SPCOR 350-501 v1.1 (Domain 4) and Domains 1, 3, and 4 of SPVI 300-515 v1.1** —
mapped in the volume README's coverage tables. Labs use the IOS XR CLI on PE and
P routers. Each ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 6.1–6.14** — an IOS XR MPLS/SR core with two PEs,
VPNv4/VPNv6 IBGP (via RR), customer VRFs with route-targets, and CE routers.
**Cost:** none beyond lab resources.

### Lab 6.1 — Describe VPN services (SPCOR Objective 4.1)

**Objective:** Enumerate the VPN service types the PE offers.

```text
show vrf all brief
show l2vpn xconnect summary
show bgp vpnv4 unicast summary
```

**Expected result:** L3VPNs (VRFs) and L2VPNs on the PE — SP VPN services span
**L3VPN** (RFC 4364, per-VRF routing over MPLS/SR), **L2VPN** (VPWS/VPLS/EVPN),
and their IPv6 variants; the PE multiplexes many customers over one core.

**Negative test:** assume all customer isolation comes from the core; isolation is
the **VRF + RT** construct at the PE — the core just label-switches, oblivious to
customers.

**Cleanup:** none (read-only).

### Lab 6.2 — Configure L3VPN (SPCOR Objective 4.3)

**Objective:** Bring up an MPLS L3VPN and verify end-to-end customer routes.

```text
show vrf CUST-A detail | include "RD|Import|Export"
show bgp vpnv4 unicast vrf CUST-A
show route vrf CUST-A <customer-prefix>
```

**Expected result:** the VRF with its RD/RTs, VPNv4 routes, and the customer route
in the VRF RIB — L3VPN: the PE holds a per-customer VRF, redistributes CE routes
into VPNv4 BGP tagged with RTs, and the remote PE imports them by RT into its VRF.

**Negative test:** matching export RT on one PE but not importing it on the other
leaves the route in VPNv4 BGP but not in the remote VRF — RT import/export must
pair.

**Cleanup:** none (read-only).

### Lab 6.3 — Compare VPN architecture (SPVI Objective 1.1)

**Objective:** Contrast L3VPN, L2VPN, and EVPN architectures.

```text
show vrf all brief
show l2vpn bridge-domain summary
show evpn summary
```

**Expected result:** the coexisting service constructs — **L3VPN** routes at L3
per VRF; **L2VPN** (VPWS point-to-point, VPLS multipoint) bridges at L2; **EVPN**
uses BGP as the L2 control plane (MAC/IP routes) unifying L2 and L3 services with
multihoming — the modern convergence point.

**Negative test:** deploy VPLS for a large multipoint L2 service and hit
flood-and-learn scaling limits; EVPN's control-plane MAC learning is the scalable
successor — the architecture choice sets the scale ceiling.

**Cleanup:** none (read-only).

### Lab 6.4 — Troubleshoot the underlay (SPVI Objective 1.2)

**Objective:** Diagnose a VPN outage caused by the underlay LSP.

```text
show mpls forwarding prefix <remote-PE-loopback>/32
traceroute mpls ipv4 <remote-PE-loopback>/32
show bgp vpnv4 unicast <prefix> | include "not a best|inaccessible"
```

**Expected result:** the PE-PE LSP state — a VPN with correct RTs still fails if
the underlay LSP between PEs is broken; the VPNv4 route shows the next-hop
inaccessible and `traceroute mpls` finds the broken hop.

**Negative test:** debug VRF/RT config for a service that is fine at L3VPN but
broken in the core LSP — the underlay is the dependency; verify it first.

**Cleanup:** none (read-only).

### Lab 6.5 — Describe the L3VPN control plane (SPVI Objective 1.4)

**Objective:** Trace how a customer route becomes a VPNv4 route.

```text
show bgp vpnv4 unicast <prefix> detail | include "RD|Extended community|label"
show bgp vrf CUST-A <prefix>
```

**Expected result:** the route with its RD, RT extended community, and VPN label —
the control plane: CE route → PE VRF → redistributed into VPNv4 BGP with an RD
(uniqueness) and RT (membership) and a per-VRF/per-prefix VPN label → advertised
to remote PEs via RR.

**Negative test:** two customers using the same RD but different RTs still stay
isolated (RT governs import); the RD only guarantees uniqueness in BGP — confusing
RD with RT is a classic error.

**Cleanup:** none (read-only).

### Lab 6.6 — Describe the L3VPN data plane (SPVI Objective 1.5)

**Objective:** Read the two-label VPN forwarding stack.

```text
show cef vrf CUST-A <prefix> detail | include "label"
show mpls forwarding vrf CUST-A 2>/dev/null | head
```

**Expected result:** the transport (outer) label and the VPN (inner) label — the
data plane pushes two labels: the outer switches the packet PE→PE across the core
(SR/LDP), the inner tells the egress PE which VRF/next-hop to use; the core never
inspects the inner label.

**Negative test:** expect the core P routers to know the customer; they only swap
the outer label — penultimate hop pops it, and only the egress PE reads the VPN
label.

**Cleanup:** none (read-only).

### Lab 6.7 — Describe routing requirements (SPVI Objective 3.1)

**Objective:** Read the PE-CE routing protocol and redistribution.

```text
show bgp vrf CUST-A neighbors <CE> 2>/dev/null | include "state"
show ospf vrf CUST-A neighbor 2>/dev/null
show route vrf CUST-A <prefix> | include "redist|via"
```

**Expected result:** the PE-CE protocol (BGP, OSPF, EIGRP, or static) and its
redistribution into VPNv4 — L3VPN routing requirements cover the PE-CE protocol
choice, redistribution, and loop prevention (down-bit/domain-tag for OSPF, SoO for
BGP).

**Negative test:** run OSPF PE-CE across two sites without the domain-tag/down-bit
handling; routes can loop as inter-area — the loop-prevention attributes are
required.

**Cleanup:** none (read-only).

### Lab 6.8 — Troubleshoot Intra-AS L3VPNs (SPVI Objective 3.2)

**Objective:** Diagnose a customer route missing at the remote site.

```text
show bgp vpnv4 unicast rd <RD> <prefix>
show bgp vrf CUST-A <prefix>
show route vrf CUST-A <prefix>
```

**Expected result:** where the route stops — present in VPNv4 but not the remote
VRF is an RT import problem; present in the VRF BGP but not RIB is a next-hop/best-
path problem; absent from VPNv4 is a PE-CE/redistribution problem. The three views
localize it.

**Negative test:** blame the core for a route that never entered VPNv4 because
PE-CE redistribution was missing — the ingress PE side is the fault.

**Cleanup:** none (read-only).

### Lab 6.9 — Implement multicast VPN (SPVI Objective 3.3)

**Objective:** Verify mVPN (multicast over L3VPN) state.

```text
show mrib vrf CUST-A route summary
show pim vrf CUST-A neighbor
show bgp ipv4 mvpn 2>/dev/null | head
```

**Expected result:** the customer multicast state carried over the core — **mVPN**
delivers customer multicast across the SP: a provider tunnel (mLDP or SR P2MP, or
GRE) carries the customer (C-)multicast, with BGP MVPN (or PIM) as the control
plane.

**Negative test:** expect customer multicast to flow with only unicast L3VPN
configured; without a provider multicast tunnel the (S,G) has no core transport —
mVPN must be enabled.

**Cleanup:** none (read-only).

### Lab 6.10 — Implement extranet / shared services (SPVI Objective 3.4)

**Objective:** Verify controlled route leaking between VRFs.

```text
show vrf CUST-A detail | include "Import|Export"
show vrf SHARED detail | include "Import|Export"
show route vrf CUST-A <shared-service-prefix>
```

**Expected result:** the shared-service route imported into the customer VRF via
RT — extranet/shared services leak specific routes between VRFs by exporting a
service RT and importing it selectively, giving many customer VRFs access to a
shared resource without merging them.

**Negative test:** import the shared RT broadly and customers can reach each other
through the shared VRF — leak only the specific service prefixes, not full tables.

**Cleanup:** none (read-only).

### Lab 6.11 — Describe Inter-AS L3VPNs (SPVI Objective 3.5)

**Objective:** Read an Inter-AS VPN option (A/B/C) at the ASBR.

```text
show bgp vpnv4 unicast summary | include ASBR 2>/dev/null
show bgp vpnv4 unicast neighbors <ASBR-peer> | include "state|next-hop-self"
show mpls forwarding | include "Aggregate|BGP" | head
```

**Expected result:** the ASBR's inter-AS VPN handling — **Option A** (back-to-back
VRFs), **Option B** (VPNv4 exchange between ASBRs, next-hop rewrite + label swap),
**Option C** (multihop VPNv4 between RRs, labeled IPv4 for loopbacks) trade
isolation for scale.

**Negative test:** use Option C between untrusted SPs; it exposes loopbacks/labels
across the boundary — Option A/B give better isolation between distrusting ASes.

**Cleanup:** none (read-only).

### Lab 6.12 — Describe CSC concepts (SPVI Objective 3.6)

**Objective:** Read a Carrier Supporting Carrier setup.

```text
show bgp vpnv4 unicast vrf CSC-CUST 2>/dev/null | head
show mpls forwarding vrf CSC-CUST 2>/dev/null | head
show route vrf CSC-CUST <customer-carrier-loopback> | include label
```

**Expected result:** labeled routes handed to the customer-carrier in a VRF —
**CSC** lets one SP (the backbone carrier) provide MPLS transport to another SP
(the customer carrier) by exchanging labels on the PE-CE link, so the customer
carrier runs its own VPNs over the backbone.

**Negative test:** run CSC without label exchange on the PE-CE link (plain IP);
the customer carrier's VPN labels have no transport — CSC requires labeled PE-CE.

**Cleanup:** none (read-only).

### Lab 6.13 — Describe routing requirements for IPv6 VPN (SPVI Objective 4.1)

**Objective:** Read the 6VPE VRF and VPNv6 routes.

```text
show vrf CUST-A detail | include "ipv6"
show bgp vpnv6 unicast vrf CUST-A
show route vrf CUST-A ipv6 <prefix>
```

**Expected result:** VPNv6 routes in the customer VRF — **6VPE** carries customer
IPv6 over an IPv4/MPLS (or SRv6) core: the PE holds IPv6 in the VRF, advertises it
as VPNv6 with an RD/RT and label, exactly mirroring L3VPN for IPv4.

**Negative test:** enable IPv6 in the VRF but not the VPNv6 address family in BGP;
the routes never leave the PE — the VPNv6 AF must be activated on the RR sessions.

**Cleanup:** none (read-only).

### Lab 6.14 — Troubleshoot IPv6 VPN provider edge (SPVI Objective 4.2)

**Objective:** Diagnose a 6VPE route not reaching the remote CE.

```text
show bgp vpnv6 unicast <prefix> detail | include "RD|label|next hop"
show cef vrf CUST-A ipv6 <prefix> detail | include label
show route vrf CUST-A ipv6 <prefix>
```

**Expected result:** the VPNv6 route's label/next-hop and the CEF entry — a 6VPE
failure traces to the same places as L3VPN (RT import, PE-PE LSP, PE-CE routing)
plus IPv6-specific issues (VPNv6 AF not activated, IPv6 next-hop encoding).

**Negative test:** an IPv4-mapped IPv6 next-hop misread as unreachable; 6VPE
encodes the next-hop as IPv4-mapped IPv6 over an IPv4 core — expecting a native
IPv6 next-hop misdiagnoses it.

**Cleanup:** none (read-only).

## Lab Verification

Verification means both customers were isolated with overlapping
space proven, the two-label data path and 6VPE both worked, and both
induced faults were diagnosed to RT and transport-label causes
respectively. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

L3VPN is the provider's flagship: VRFs isolate customers, RDs make
prefixes unique, RTs control import as VPN topology, and a two-label
stack carries traffic across a core that never learns a customer
route. PE-CE routing offers a protocol per need, 6VPE extends it to
IPv6 for free, and isolation is the guarantee to test above all. This
is the largest slice of SPVI and the core of SPCOR's Services domain.

- [ ] I can state the RD-versus-RT distinction without hesitation
- [ ] My two customers are isolated with overlapping space proven
- [ ] I traced the two-label path and diagnosed a transport-label gap
- [ ] 6VPE works over the same core
