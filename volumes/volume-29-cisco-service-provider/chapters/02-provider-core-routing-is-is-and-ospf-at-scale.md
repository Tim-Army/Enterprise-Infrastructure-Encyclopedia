# Chapter 02: Provider Core Routing: IS-IS and OSPF at Scale

## Learning Objectives

- Explain why IS-IS is the provider IGP of choice and how its
  level hierarchy scales
- Configure IS-IS on IOS XR for an SP core: levels, metrics, wide
  metrics, and authentication
- Design the IGP as the label-transport substrate — loopbacks,
  metrics, and the segment-routing readiness Chapter 04 builds on
- Compare OSPF's role where it appears in SP networks, and translate
  the design ideas across both
- Tune convergence: timers, fast flooding, and the LFA readiness that
  Chapter 05 completes

## Theory and Architecture

### Why IS-IS wins in the core

Both IS-IS and OSPF are link-state, but providers overwhelmingly run
**IS-IS** in the core, and SPRI's Unicast Routing domain (35%) expects
you to know why. IS-IS runs directly on the data link (not inside IP),
so it is address-family agnostic — one topology carries IPv4, IPv6,
and the segment-routing SIDs of Chapter 04 without redesign. Its TLV
(type-length-value) encoding extends cleanly, which is exactly how
Segment Routing bolted on without a protocol rewrite. And its two-level
hierarchy is simpler to operate at scale than OSPF's area-type zoo.

### IS-IS structure

- **Levels.** Level 1 is intra-area, Level 2 is the backbone between
  areas; an **L1/L2** router bridges them. Providers commonly run a
  single-level (L2-only) core for simplicity at moderate scale, or
  L1/L2 hierarchy for very large networks.
- **NET address.** The router's IS-IS identity (area + system ID +
  NSEL) — a different addressing scheme than IP, and an exam favorite
  to read correctly.
- **Wide metrics.** The 24-bit wide-metric style (versus the legacy
  6-bit narrow metric) is mandatory for modern designs and for
  Segment Routing; narrow metrics are legacy to recognize, not deploy.
- **Adjacencies** form per level over the link; point-to-point links
  skip DIS election, broadcast links elect a DIS (IS-IS's lighter
  analog to OSPF's DR).

### The IGP as transport substrate

In an MPLS/SR provider network the IGP's job is not to carry customer
routes — BGP does that (Chapter 03). The IGP carries **loopbacks and
link addresses only**, precisely and quickly, because everything else
is built on top: LDP/SR labels follow IGP loopback reachability, BGP
next-hops resolve through it, and TE and FRR compute against its
topology. Design consequences: every router's `Loopback0` is its
identity and BGP source; IGP metrics reflect real link cost/latency
because SR and TE honor them; and IGP convergence speed sets the floor
for everything above.

### OSPF where it appears, and convergence

OSPF persists in some SP edges, enterprise-facing designs, and PE-CE
links (Chapter 06). The design ideas port directly — areas map to
levels, LSAs to LSPs — and the volume shows IS-IS as the core case
while noting OSPF equivalents. Convergence, common to both: fast
hello/dead or BFD (Chapter 05) for detection, LSP/LSA fast flooding
and SPF throttling tuned so a link failure reconverges in low tens of
milliseconds, and LFA/TI-LFA precomputed backups so data-plane
restoration does not even wait for SPF.

## Design Considerations

- **Single-level core until scale forces hierarchy**: L2-only is
  simpler to reason about; introduce L1/L2 areas when LSDB size or
  flooding overhead demands it, not preemptively.
- **Wide metrics and one metric style network-wide**: mixing narrow
  and wide is a migration hazard and an SR blocker.
- **Loopback /32s (and /128s) as the routing core**: summarize
  customer and infrastructure prefixes elsewhere, never the loopbacks
  SR and BGP depend on.
- **Metrics that mean something**: set them from bandwidth/latency
  policy so TE and SR paths are sensible by default.

## Implementation and Automation

IS-IS on the Chapter 01 XR core, built as SR-ready transport:

```text
router isis CORE
 is-type level-2-only
 net 49.0001.0100.0000.0001.00
 log adjacency changes
 address-family ipv4 unicast
  metric-style wide
  ! segment-routing enabled here in Chapter 04
 !
 interface Loopback0
  passive
  address-family ipv4 unicast
 !
 interface GigabitEthernet0/0/0/0
  point-to-point
  address-family ipv4 unicast
   metric 100
  !
  hello-password keychain ISIS-KEY
```

```text
! Validation
show isis adjacency
show isis database
show route isis
show isis interface brief
```

Fast-convergence posture (completed with BFD/TI-LFA in Chapter 05):

```text
router isis CORE
 address-family ipv4 unicast
  spf-interval maximum-wait 5000 initial-wait 50 secondary-wait 200
  fast-reroute per-prefix           ! LFA; TI-LFA in Ch.05
```

## Validation and Troubleshooting

Validate hierarchy and reachability: adjacencies up at the expected
level (`show isis adjacency` — a link stuck in "Init" is usually an
MTU or level mismatch), the database consistent across the area
(`show isis database` LSP counts match on every node), and every
loopback reachable (`show route isis`). The classic faults: **MTU
mismatch** blocks adjacency formation on IS-IS distinctly (it pads
hellos — a small-MTU link fails to bring up cleanly); **level
mismatch** (an L1 router meeting an L2-only neighbor forms no
adjacency); **metric-style mismatch** silently degrades or blocks SR;
**area/NET typos** put a router in the wrong area. Method: prove the
adjacency layer before the database, the database before the routes —
the same layer discipline the whole encyclopedia teaches.

## Security and Best Practices

- IS-IS authentication (keychain-based, per-level and per-interface)
  so a rogue device cannot inject LSPs into the core.
- Passive loopbacks and careful interface enumeration so the IGP runs
  only where intended.
- BFD (Chapter 05) for detection independent of protocol hellos, and
  overload-bit discipline (`set-overload-bit on-startup`) so a
  rebooting router does not attract transit before BGP is ready — a
  subtle SP correctness item the exam rewards.

## References and Knowledge Checks

- SPRI 300-510 v1.1 Unicast Routing domain (35%); SPCOR Networking
  domain (30%)
- Cisco IOS XR IS-IS configuration guide
- ISO 10589 / RFC 1195 (IS-IS) and the SR IS-IS extensions

Knowledge checks:

1. Give two reasons IS-IS suits SR-MPLS transport that OSPFv2 does
   not match as cleanly.
2. Why does the core IGP carry only loopbacks and links, and what
   carries everything else?
3. An IS-IS link stays in "Init." Name the two most common causes
   and how each presents.
4. What does the startup overload bit prevent, and why does an SP
   care more than an enterprise?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **the IS-IS/OSPF
objectives of SPCOR 350-501 v1.1 (Domain 2) and Domain 1 (Unicast Routing) of
SPRI 300-510 v1.1** covering the IGP — mapped in the volume README's coverage
tables. Labs use the IOS XR CLI on a provider core. Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 2.1–2.6** — an IOS XR core of at least three
routers with loopbacks, dual-stack (IPv4/IPv6) addressing, and the ability to
form IS-IS and OSPF adjacencies. **Cost:** none beyond lab resources.

### Lab 2.1 — Implement IS-IS for IPv4 and IPv6 (SPCOR Objective 2.1)

**Objective:** Bring up a dual-stack IS-IS core and verify adjacencies.

```text
show isis neighbors
show isis interface brief
show route ipv6 unicast isis
```

**Expected result:** IS-IS neighbors `Up` on the core links and IPv6 routes
learned — IS-IS (single-topology or multi-topology) is the SP core IGP of choice:
it runs directly on CLNS, scales flat with levels, and carries IPv4 and IPv6 in
one process.

**Negative test:** mismatch the IS-IS network type (point-to-point vs broadcast)
on two ends; the adjacency stalls — the interface circuit type must match.

**Cleanup:** none (read-only).

### Lab 2.2 — Implement OSPF v2 and v3 (SPCOR Objective 2.2)

**Objective:** Bring up OSPFv2 (IPv4) and OSPFv3 (IPv6) and verify.

```text
show ospf neighbor
show ospfv3 neighbor
show route ipv4 ospf
```

**Expected result:** OSPFv2 and OSPFv3 neighbors `FULL` and routes installed —
OSPF is the alternative SP IGP; v2 carries IPv4, v3 carries IPv6 (and can carry
both with address families), area design bounding LSA flooding.

**Negative test:** an OSPF area/type mismatch or MTU mismatch leaves neighbors in
`EXSTART`; `show ospf neighbor` shows the stuck state — MTU and area must match.

**Cleanup:** none (read-only).

### Lab 2.3 — Compare OSPF and IS-IS (SPRI Objective 1.1)

**Objective:** Read the design attributes that differentiate the two IGPs.

```text
show isis database | utility head -20
show ospf database database-summary
```

**Expected result:** the IS-IS LSP database vs OSPF LSDB — IS-IS scales the SP
core well (fewer LSP types, runs on CLNS not IP so it is harder to attack, easy
multi-topology), while OSPF's area/LSA model is familiar and granular; SP cores
often favor IS-IS for its simplicity and scale.

**Negative test:** assume area design is identical; OSPF areas require an ABR and
area 0 backbone, IS-IS uses flat levels (L1/L2) — the topology constraints differ.

**Cleanup:** none (read-only).

### Lab 2.4 — Troubleshoot OSPF multiarea operations (SPRI Objective 1.2)

**Objective:** Diagnose an inter-area route not appearing.

```text
show ospf neighbor
show ospf border-routers
show route ipv4 ospf | include "IA"
```

**Expected result:** the ABR and inter-area (IA) routes — a missing inter-area
route traces to an ABR not generating the Type-3 summary, an area misconfiguration,
or a discontiguous area 0; the border-routers and IA routes localize it.

**Negative test:** blame the remote area for a route absent because the local ABR
lost its area-0 adjacency — without a backbone connection the ABR cannot inject
inter-area routes.

**Cleanup:** none (read-only).

### Lab 2.5 — Troubleshoot IS-IS multilevel operations (SPRI Objective 1.3)

**Objective:** Diagnose an L1/L2 route leaking/attachment issue.

```text
show isis topology level-1
show isis topology level-2
show route ipv4 isis | include "i L1|i L2|ia"
```

**Expected result:** the L1 and L2 topologies and the attached-bit behavior — an
L1-only router reaches other areas via the nearest L1/L2 router's default (attached
bit); a missing inter-area route traces to route leaking (L2→L1) not configured, or
the attached bit absent.

**Negative test:** expect an L1 router to have specific inter-area routes without
route-leak; it only gets a default via the attached bit — enable L2→L1 leaking for
specifics.

**Cleanup:** none (read-only).

### Lab 2.6 — Describe IPv6 tunneling mechanisms (SPRI Objective 1.6)

**Objective:** Read an IPv6-over-IPv4 (or 6PE/6VPE) transition mechanism.

```text
show tunnel 2>/dev/null | head
show bgp ipv6 unicast labels | head        ! 6PE labels
show cef ipv6 <prefix>
```

**Expected result:** the tunnel or 6PE label path — IPv6 transition over an IPv4
core uses tunneling (6in4, GRE), or MPLS-based **6PE**/**6VPE** that label-switches
IPv6 across an IPv4/MPLS core without dual-stacking every P router.

**Negative test:** expect native IPv6 forwarding across an IPv4-only MPLS core;
without 6PE the IPv6 packets have no transport — the tunneling/6PE mechanism is
required.

**Cleanup:** none (read-only).

## Lab Verification

Verification means the IGP converged with authenticated adjacencies
and reachable loopbacks, all three faults were produced and diagnosed
by signature, and the overload-bit behavior was observed. Until then,
the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

IS-IS is the provider core IGP because it is address-family agnostic,
TLV-extensible (the door Segment Routing walked through), and simple
to scale by levels. Its job is fast, precise loopback transport —
customer routes ride BGP above it — and its convergence sets the floor
for everything in Chapters 03–08. This is the larger half of SPCOR's
Networking domain and the core of SPRI.

- [ ] I can justify IS-IS over OSPF for SR-MPLS transport
- [ ] My core carries loopbacks precisely and authenticates LSPs
- [ ] I diagnosed MTU, level, and overload behaviors from evidence
- [ ] My IS-IS is wide-metric and SR-ready for Chapter 04
