# Chapter 05: Traffic Engineering and Fast Restoration

## Learning Objectives

- Explain traffic engineering's purpose and compare RSVP-TE with
  SR-TE
- Configure SR-TE policies: explicit paths, dynamic paths with
  constraints, and steering
- Design sub-50-ms protection: LFA, remote LFA, and TI-LFA, and
  explain why TI-LFA guarantees a backup
- Deploy BFD for fast failure detection independent of protocol
  hellos
- Validate protection and TE behavior with failure testing and
  evidence

## Theory and Architecture

### Why engineer traffic at all

IGP shortest-path routing sends everything over the lowest-metric
path, which can congest one link while parallel capacity sits idle,
and cannot honor latency or affinity constraints a service demands.
**Traffic engineering** steers specific traffic along chosen paths —
for capacity, for latency, or to avoid particular links. SPCOR folds
TE into the MPLS/SR domain; the SP reality is that TE and fast
restoration are how SLAs get met.

### RSVP-TE versus SR-TE

**RSVP-TE** signals explicit LSPs and reserves bandwidth hop by hop —
powerful but stateful: every P router holds per-tunnel state, and the
control plane scales poorly with tunnel count. **SR-TE** expresses the
path as a **segment list** (a stack of prefix- and adjacency-SIDs from
Chapter 04) imposed at the headend; the core holds no per-path state
because the packet carries its own path. This is the same state-removal
win as SR transport, applied to engineering, and it is why new
deployments are SR-TE.

An **SR-TE policy** is defined by (headend, color, endpoint): *color*
encodes intent (low-latency, high-bandwidth), and BGP routes colored
to match are automatically steered onto the policy — **on-demand next
hop (ODN)** builds policies as colored routes appear. Paths are
**explicit** (an operator-specified segment list) or **dynamic**
(computed to optimize a metric — IGP, TE, or latency — subject to
constraints/affinities), optionally computed by a **PCE** (path
computation element) for network-wide optimization.

### Fast restoration: the sub-50-ms promise

SLAs demand restoration faster than IGP reconvergence, so the data
plane must have a precomputed backup ready before failure:

- **LFA (Loop-Free Alternate)** — a precomputed backup next-hop that
  is loop-free by inequality; simple but does not cover every
  topology (ring topologies notoriously).
- **Remote LFA (rLFA)** — extends coverage using a targeted LDP/label
  session to a distant loop-free release point.
- **TI-LFA (Topology-Independent LFA)** — uses SR's ability to encode
  an explicit backup path as a label stack, so it **guarantees a
  loop-free backup in any topology**, along the post-convergence path
  (so traffic does not thrash when the IGP later reconverges). TI-LFA
  is the SR-era answer and the one the exam expects as default.

**BFD** detects failures in milliseconds independent of protocol
hellos, triggering the precomputed switch — detection plus TI-LFA
together deliver the sub-50-ms behavior.

## Design Considerations

- **TI-LFA everywhere as the protection baseline**: with SR, per-prefix
  TI-LFA is a few lines and covers any topology — there is little
  reason to run bare LFA in a new design.
- **SR-TE by color/intent, not by hand-built tunnels**: model intents
  (latency, disjointness) as colors and let ODN instantiate policies;
  hand-crafted explicit paths are for exceptions.
- **BFD timers matched to platform and SLA**: aggressive timers detect
  faster but cost CPU and risk false positives on congested links —
  tune per platform capability.
- **Disjointness for protected services**: dual-plane or SRLG-aware
  path computation so a primary and its backup do not share a fate.

## Implementation and Automation

TI-LFA and BFD on the Chapter 04 SR core:

```text
router isis CORE
 interface GigabitEthernet0/0/0/0
  bfd minimum-interval 50
  bfd multiplier 3
  address-family ipv4 unicast
   fast-reroute per-prefix
   fast-reroute per-prefix ti-lfa      ! guaranteed backup, any topology
```

An SR-TE policy — explicit low-latency path, and dynamic with a
constraint:

```text
segment-routing
 traffic-eng
  policy LOW-LATENCY-PE2
   color 100 end-point ipv4 10.0.0.2
   candidate-paths
    preference 100
     explicit segment-list AVOID-CORE1
    preference 50
     dynamic
      metric type latency
  !
  segment-list AVOID-CORE1
   index 10 mpls adjacency 10.1.12.2   ! adjacency-SIDs building a path
   index 20 mpls label 16002           ! prefix-SID of PE2
```

```text
! Validation
show segment-routing traffic-eng policy
show mpls forwarding tunnels
show bfd session
show isis fast-reroute ipv4 detail        ! TI-LFA backup paths
```

## Validation and Troubleshooting

Protection is validated by **breaking things and measuring**: confirm
TI-LFA has installed a backup for the loopbacks (`show isis
fast-reroute detail`), start a continuous stream, fail the primary
link, and measure the loss window — sub-50-ms means the data plane
switched to the precomputed path before the control plane reconverged.
BFD's role shows as the trigger: with BFD, detection is milliseconds;
without, you wait for IGP hellos. SR-TE validation: the policy is up
and its segment list resolves (`show segment-routing traffic-eng
policy`), colored traffic actually takes it (trace the label stack),
and ODN instantiates policies as colored routes arrive. Faults:
TI-LFA "no backup" for a prefix usually means a genuinely
unprotectable topology or an SR/label gap (Chapter 04); an SR-TE
policy "down" traces to an unresolvable SID in the list (an
adjacency-SID for a failed link, a prefix-SID that is missing);
BFD flaps on a congested link argue for less aggressive timers or a
QoS fix (Chapter 08).

## Security and Best Practices

- Protection and TE are availability controls, and availability is
  security: a resilient core resists both faults and certain attacks.
- PCE and controller interfaces (Chapter 09) are privileged — they
  can steer traffic network-wide — so their access and authentication
  are held to the management-plane standard.
- Validate that backup paths honor the same policy/security boundaries
  as primaries; a backup that bypasses a scrubbing or inspection point
  is a hole.

## References and Knowledge Checks

- SPCOR MPLS and Segment Routing (20%, TE portion); SPRI MPLS/SR (25%)
- Cisco IOS XR SR-TE and fast-reroute configuration guides
- RFC 7490 (rLFA), RFC 8402 (SR), TI-LFA drafts/guides

Knowledge checks:

1. Contrast RSVP-TE and SR-TE by where per-path state lives, and why
   that drives new deployments to SR-TE.
2. Why does TI-LFA guarantee a loop-free backup where plain LFA
   cannot, and what SR capability makes that possible?
3. What are BFD and TI-LFA each responsible for in a sub-50-ms
   restoration, and what happens if you have one without the other?
4. An SR-TE policy is down. Name two segment-list conditions that
   cause it and how you would confirm each.

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **the traffic-engineering,
high-availability, and fast-restoration objectives of SPCOR 350-501 v1.1, SPRI
300-510 v1.1, and Domain 3 (High Availability) of SPCNI 300-540 v1.0** — mapped
in the volume README's coverage tables. Labs use the IOS XR CLI and the NFVI
fabric. Each ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 5.1–5.10** — an IOS XR core with Segment Routing,
TI-LFA and BFD available, redundant hardware (dual RP) or NSR/NSF, and a
multi-homed NFVI fabric for the SPCNI labs. **Cost:** none beyond lab resources.

### Lab 5.1 — Implement high availability (SPCOR Objective 2.8)

**Objective:** Verify control-plane HA (NSR/NSF, graceful restart).

```text
show redundancy
show bgp ipv4 unicast neighbors <peer> | include "GR|NSR|graceful"
show isis adjacency detail | include "restart|BFD"
```

**Expected result:** the redundant RP state and NSR/graceful-restart on the
protocols — HA keeps forwarding through a control-plane switchover: **NSR**
(non-stop routing) keeps sessions up across an RP failover, **NSF/GR** relies on
the neighbor to help, and BFD gives sub-second failure detection.

**Negative test:** rely on graceful restart with a neighbor that is not GR-capable;
the session resets on switchover — NSR (no neighbor help) is more robust for that
case.

**Cleanup:** none (read-only).

### Lab 5.2 — Describe traffic engineering (SPCOR Objective 3.2 — TE)

**Objective:** Read a TE/SR-TE policy and its path.

```text
show segment-routing traffic-eng policy all
show mpls traffic-eng tunnels brief 2>/dev/null | head
show cef <prefix> | include "SR policy|tunnel"
```

**Expected result:** the TE policy with its computed/explicit path — traffic
engineering steers flows off the IGP shortest path onto a bandwidth- or latency-
optimized path; SR-TE encodes it as a SID list (no RSVP core state), the modern
SP approach.

**Negative test:** expect a TE policy to attract traffic without a steering
mechanism (color/BSID/autoroute); the policy exists but no traffic uses it — the
steering must be configured.

**Cleanup:** none (read-only).

### Lab 5.3 — Implement fast convergence (SPRI Objective 1.7)

**Objective:** Verify BFD and LFA/TI-LFA for sub-second restoration.

```text
show bfd session
show isis fast-reroute summary
show route ipv4 <prefix> detail | include "Backup|repair"
```

**Expected result:** BFD sessions up and a TI-LFA backup path pre-installed —
fast convergence combines **BFD** (millisecond detection) with **TI-LFA**
(pre-computed loop-free backup installed in FIB), so failover is sub-50 ms without
waiting for IGP reconvergence.

**Negative test:** rely on IGP timers alone for convergence; failover takes
hundreds of ms to seconds — BFD + a pre-computed backup is what achieves the SLA.

**Cleanup:** none (read-only).

### Lab 5.4 — Implement Segment Routing traffic engineering (SPRI Objective 4.3)

**Objective:** Configure and verify an SR-TE policy with a SID list.

```text
show segment-routing traffic-eng policy name LOW-LATENCY detail
show segment-routing traffic-eng policy name LOW-LATENCY | include "Explicit|Dynamic|SID"
```

**Expected result:** the SR-TE policy with its SID list and metric objective —
SR-TE builds an explicit or dynamically-computed (by the headend or an SR-PCE)
path expressed as a label/SID stack, steered by color/binding-SID, delivering TE
without RSVP.

**Negative test:** a dynamic SR-TE policy optimizing for a metric no link
advertises (e.g., latency with no delay measurement) cannot compute a path — the
metric must be available in the topology.

**Cleanup:** none (read-only).

### Lab 5.5 — Implement technologies for high availability (SPCNI Objective 3.1)

**Objective:** Verify fabric-level HA (redundant paths, graceful switchover).

```text
show redundancy summary
show bfd session
show bundle 2>/dev/null | include "Active|Standby"
```

**Expected result:** redundant links/bundles and BFD — NFVI/fabric HA layers
device redundancy (dual RP/NSR), link redundancy (LAG/bundles with BFD), and path
redundancy (ECMP/TI-LFA), so no single failure drops the service.

**Negative test:** a "redundant" bundle whose members share one line card/fate
fails together — redundancy must span independent failure domains.

**Cleanup:** none (read-only).

### Lab 5.6 — Implement multi-homing (SPCNI Objective 3.2)

**Objective:** Verify a multi-homed site/NFVI with active-active or active-standby.

```text
show evpn ethernet-segment detail | include "ESI|Redundancy|DF"
show bgp l2vpn evpn | include "1:|4:"     ! ES / ES-AD routes
```

**Expected result:** the Ethernet Segment (ESI), its redundancy mode, and the
Designated Forwarder — multi-homing attaches a site to two PEs; EVPN elects a DF
for BUM and can load-balance (all-active) using ESI and aliasing.

**Negative test:** two PEs multi-homing a segment with mismatched ESIs act as
single-homed and can loop BUM traffic — the ESI must match on both PEs.

**Cleanup:** none (read-only).

### Lab 5.7 — Implement EVLAG (SPCNI Objective 3.3)

**Objective:** Verify an Ethernet Virtual LAG / MC-LAG to a dual-homed device.

```text
show bundle bundle-ether 1
show redundancy 2>/dev/null | include "mLACP|ICCP"
show iccp group 2>/dev/null
```

**Expected result:** the bundle active across two chassis via ICCP/mLACP — EVLAG
(multi-chassis LAG) presents one logical LAG from two PEs to a dual-homed CE/host,
active-active forwarding without spanning tree, synchronized over ICCP.

**Negative test:** an EVLAG with ICCP down splits into two independent LAGs and can
loop or blackhole — the inter-chassis control link is essential.

**Cleanup:** none (read-only).

### Lab 5.8 — Implement a virtual private cloud (SPCNI Objective 3.4)

**Objective:** Verify tenant isolation for a VPC over the fabric.

```text
show vrf VPC-TENANT-A detail
show bgp vpnv4 unicast vrf VPC-TENANT-A summary
show l2vpn bridge-domain group VPC-A 2>/dev/null
```

**Expected result:** the tenant VRF/bridge-domain isolating the VPC — a virtual
private cloud gives a tenant an isolated L2/L3 domain over shared infrastructure
(VRF + EVPN/L3VPN), with its own address space and policy.

**Negative test:** two VPCs sharing a route-target leak routes between tenants —
the RT import/export must isolate each VPC.

**Cleanup:** none (read-only).

### Lab 5.9 — Implement ECMP from NFVI to physical (SPCNI Objective 3.5)

**Objective:** Verify equal-cost multipath from the NFVI to the fabric.

```text
show cef <prefix> | include "per-destination|via"
show bgp <prefix> | include "multipath"
show route <prefix> | include "via"
```

**Expected result:** multiple next-hops for the prefix — ECMP from NFVI to the
physical fabric (BGP multipath, OSPF/IS-IS equal-cost, bundle hashing) load-shares
and adds path redundancy between the virtual functions and the network.

**Negative test:** BGP learns two equal paths but `maximum-paths` is 1, so only one
installs; no load-sharing — multipath must be explicitly enabled.

**Cleanup:** none (read-only).

### Lab 5.10 — Recommend design models for high availability (SPCNI Objective 3.6)

**Objective:** Read the HA elements across DNS, routing, and load balancing.

```text
show route <service-vip>            ! anycast/ECMP to the service
show bgp <service-vip>              ! health-injected route
! DNS/LB: confirm GSLB/health-checked records and LB pool members
```

**Expected result:** an anycast/health-injected service route plus DNS/LB
redundancy — HA design layers **DNS** (GSLB, health-checked records), **routing**
(anycast, BGP health injection, ECMP), and **load balancing** (redundant pools,
health checks) so a failure at any tier reroutes automatically.

**Negative test:** rely on DNS failover alone with long TTLs; clients cache the
dead record for minutes — anycast/BGP withdrawal gives faster failover than DNS.

**Cleanup:** none (read-only).

## Lab Verification

Verification means TI-LFA restoration was measured under 50 ms and
contrasted with the BFD-off case, the SR-TE policy steered and fell
back with label-stack evidence, and the broken policy was diagnosed
to its unresolved SID. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Traffic engineering steers traffic for capacity and latency, and
SR-TE does it with no core state by carrying the path as a segment
list; fast restoration meets SLAs with precomputed backups, where
TI-LFA guarantees coverage in any topology and BFD triggers the
switch in milliseconds. Together they are how a provider keeps its
promises, and they complete SPCOR's and SPRI's MPLS/SR domains.

- [ ] I can contrast RSVP-TE and SR-TE by state location
- [ ] TI-LFA + BFD gave me measured sub-50-ms restoration
- [ ] My SR-TE policy steered by color and fell back on failure
- [ ] I diagnosed a down policy to its unresolved segment
