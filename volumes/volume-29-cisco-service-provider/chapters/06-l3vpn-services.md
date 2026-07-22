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

On the Chapter 04 SR transport: build CUST-A as an any-to-any L3VPN
across two PEs with eBGP PE-CE, then add CUST-B with **overlapping**
address space to prove isolation is real. Verify control plane
(VPNv4 routes with correct RD/RT, imported at the remote PE), data
plane (end-to-end CE-to-CE with the two-label stack visible in
forwarding), and **isolation** (CUST-B's VRF has none of CUST-A's
routes; cross-customer ping fails). Add IPv6 to CUST-A (6VPE) and
prove dual-stack reachability over the same core. Break and diagnose:
mistype one import RT (reproduce "sites can't see each other"), and
remove the transport LSP to the egress PE (reproduce "routes present,
traffic dead"). Restore both.

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
