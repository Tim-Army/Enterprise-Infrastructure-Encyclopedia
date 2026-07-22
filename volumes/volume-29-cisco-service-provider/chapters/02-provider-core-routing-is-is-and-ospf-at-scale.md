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

On the Chapter 01 core: bring up IS-IS L2-only with wide metrics,
passive loopbacks, keychain authentication, and meaningful per-link
metrics. Verify full adjacencies, a consistent database, and loopback
reachability across the core. Then induce and diagnose three faults:
set one link's MTU low and observe the adjacency failure signature;
change one interface to a different level and observe no adjacency;
set `set-overload-bit on-startup` and reload a P router, showing it is
avoided for transit until it clears. Tune SPF timers and confirm
faster reconvergence on a link flap (measure it). Export the config;
Chapter 04 enables SR on this exact IS-IS instance.

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
