# Chapter 03: Cisco Enterprise Routing and Path Control

## Learning Objectives

- Configure and tune OSPFv2 in a multi-area enterprise topology.
- Configure EIGRP as a comparison/coexistence protocol and explain when it
  is still an appropriate choice.
- Configure eBGP/iBGP for enterprise edge and multi-site scenarios.
- Redistribute routes safely between protocols using route maps and
  filtering to prevent routing loops.
- Apply policy-based routing (PBR) and IP SLA–driven path control.
- Use VRF-lite to segment routing tables on a shared physical
  infrastructure.

## Theory and Architecture

### Interior gateway protocol selection

Enterprise campus and branch routing is built almost entirely on two
interior gateway protocols (IGPs): OSPFv2 and EIGRP, plus BGP at
inter-domain boundaries (WAN edge, internet edge, and increasingly as an
underlay/overlay control plane, covered further in [Chapter 4](04-enterprise-wan-internet-edge-and-catalyst-sd-wan.md) and Chapter
9).

**OSPFv2** is a link-state protocol that floods link-state advertisements
(LSAs) within an area and computes shortest paths with Dijkstra's algorithm.
Its area structure (a mandatory backbone, Area 0, with other areas
attaching to it) bounds LSA flooding domains, which keeps convergence and
CPU load predictable as the network grows. OSPF is vendor-neutral (RFC
2328), which makes it the default IGP choice in mixed-vendor or
acquisition-heavy enterprise environments.

**EIGRP** is a Cisco-developed advanced distance-vector protocol using the
Diffusing Update Algorithm (DUAL) to guarantee loop-free paths and
extremely fast convergence via pre-computed feasible successors. EIGRP has
no strict area hierarchy; instead it relies on route summarization at
manually chosen boundaries. EIGRP remains a valid, often simpler-to-operate
choice in single-vendor Cisco estates, particularly where its faster
default convergence and simpler configuration outweigh OSPF's
vendor-neutral portability.

Neither protocol is categorically "better" — the decision is a design
choice driven by vendor mix, existing operational skill, and convergence
requirements, and is documented in the Design Considerations below.

### OSPF area design

| Area type | Purpose |
| --- | --- |
| Area 0 (backbone) | Mandatory transit area; every other area must attach directly to it (or via a virtual link, a design smell to avoid) |
| Standard area | Carries intra-area and inter-area (Type 3) routes |
| Stub area | Blocks external (Type 5) LSAs; a default route replaces them |
| Totally stubby area | Blocks external and inter-area LSAs; only a default route enters |
| NSSA | Like a stub area but allows limited external redistribution (Type 7, translated to Type 5 at the ABR) |

Stub/totally-stubby/NSSA area types exist to shrink the routing table and
LSA flooding load on smaller branch or edge areas that do not need full
topology visibility — a branch area rarely needs to see every external
route in detail when a default route to the distribution/core will get
traffic there anyway.

### BGP in the enterprise

BGP (RFC 4271) is a path-vector protocol built for policy-driven routing
between administratively distinct domains. In an enterprise, BGP typically
appears at three boundaries:

- **Internet edge** — eBGP peering with one or more Internet Service
  Providers, usually receiving a default route (or a full/partial table
  when multihoming requires more granular path selection) and advertising
  the enterprise's own public prefixes.
- **MPLS L3VPN WAN edge** — eBGP peering with a provider PE router per site,
  common in traditional MPLS WAN designs ([Chapter 4](04-enterprise-wan-internet-edge-and-catalyst-sd-wan.md)).
- **Data center / multi-site fabric underlay-overlay** — iBGP or eBGP
  used as a scalable control plane between sites or between fabric border
  nodes ([Chapter 9](09-catalyst-center-sd-access-assurance-and-operations.md), [Volume VI](../../volume-06-enterprise-storage-data-protection/README.md), [Volume VIII](../../volume-08-containers-platform-engineering/README.md)).

BGP path selection uses a well-defined, ordered attribute comparison
(weight, local preference, AS-path length, origin, MED, and so on); campus
and WAN engineers most commonly influence outbound path choice with local
preference and inbound path choice (from a peer's perspective) with
AS-path prepending or MED, in combination with route maps and prefix lists.

### Redistribution and loop risk

Any point where routes cross from one routing protocol into another is a
redistribution boundary, and every redistribution boundary is a potential
routing loop if information is allowed to flow back into the source
protocol after being converted. Two-way (mutual) redistribution between
protocols at more than one boundary point is the classic failure pattern:
a route redistributed from OSPF into EIGRP at Router A can be
re-redistributed back into OSPF at Router B with worse metric information,
creating a suboptimal or looping path. Every redistribution point must use
route maps, distribute lists, or tags to filter and mark redistributed
routes so they cannot re-enter their source protocol.

### Policy-based routing and IP SLA

Destination-based routing (the default: "forward based on the longest
prefix match to the destination address") is not always sufficient — for
example, sending guest wireless traffic that would otherwise route out the
primary WAN uplink over a dedicated internet-only path instead. Policy-Based
Routing (PBR) overrides the default forwarding decision using a route map
matched against source/destination address, protocol, or interface. IP SLA
combined with **object tracking** allows PBR (or a static route, or an
HSRP priority as seen in [Chapter 2](02-catalyst-campus-switching-and-resiliency.md)) to react automatically to a monitored
path's reachability or latency rather than only reacting to hard link-down
events.

### VRF-lite

Virtual Routing and Forwarding (VRF)-lite creates multiple independent
routing tables on one physical router or switch, each with its own
interfaces, routing protocol instances (or instances-within-instances via
address-family configuration), and forwarding table. It is the
single-device building block for network segmentation used throughout this
volume — [Chapter 7](07-cisco-identity-access-control-and-segmentation.md) layers TrustSec/SGT policy on top of VRF-lite
segmentation, and [Chapter 9](09-catalyst-center-sd-access-assurance-and-operations.md) uses the same VRF concept as the SD-Access
overlay's virtual network (VN) construct.

## Design Considerations

- **OSPF vs. EIGRP** — default to OSPF in mixed-vendor environments, when
  future vendor diversity is plausible, or when standards-based
  documentation/tooling matters; default to EIGRP in Cisco-only estates
  where its simpler summarization model and faster native convergence are
  valuable and vendor lock-in is an accepted trade-off.
- **Area/AS boundary placement** — align OSPF area boundaries (or EIGRP
  summarization boundaries) with the physical distribution-block topology
  from [Chapter 2](02-catalyst-campus-switching-and-resiliency.md), not with organizational boundaries that don't correspond
  to a physical aggregation point.
- **Redistribution governance** — redistribute at as few points as
  possible, always with route tagging and filtering, and document every
  redistribution point in the network's design record since it is the
  single most common source of production routing loops.
- **BGP multihoming design** — decide up front whether outbound path
  selection needs full-table granularity (justifying local preference and
  AS-path policy per prefix) or whether a simple default-route-plus-
  floating-static design is sufficient; full-table BGP multihoming adds
  meaningful operational and memory overhead that is not justified for
  every site.
- **PBR scope** — use PBR sparingly and only where destination-based
  routing genuinely cannot express the required policy; PBR configuration
  is easy to leave stale after a topology change and is harder to audit
  than standard routing.
- **VRF-lite scaling** — VRF-lite scales to a modest number of VRFs per
  device before configuration and troubleshooting overhead becomes
  significant; at true fabric scale, prefer the automated overlay model in
  [Chapter 9](09-catalyst-center-sd-access-assurance-and-operations.md) rather than hand-building large numbers of VRF-lite instances.

## Implementation and Automation

### Multi-area OSPF

```text
CORE-01(config)# router ospf 1
CORE-01(config-router)# router-id 10.255.0.1
CORE-01(config-router)# network 10.0.0.0 0.255.255.255 area 0
CORE-01(config-router)# area 10 stub no-summary
CORE-01(config-router)# passive-interface default
CORE-01(config-router)# no passive-interface TenGigabitEthernet1/0/1
CORE-01(config-router)# exit

DIST-01(config)# router ospf 1
DIST-01(config-router)# router-id 10.255.0.11
DIST-01(config-router)# network 10.10.0.0 0.0.255.255 area 10
DIST-01(config-router)# area 10 stub no-summary
DIST-01(config-router)# exit
```

`passive-interface default` followed by explicit `no passive-interface` on
transit links is a defensive default: it prevents OSPF from accidentally
forming adjacencies out of access-facing SVIs.

### EIGRP (named mode)

```text
BRANCH-01(config)# router eigrp CAMPUS
BRANCH-01(config-router)# address-family ipv4 unicast autonomous-system 100
BRANCH-01(config-router-af)# network 10.20.0.0 0.0.255.255
BRANCH-01(config-router-af)# af-interface default
BRANCH-01(config-router-af-interface)# passive-interface
BRANCH-01(config-router-af-interface)# exit-af-interface
BRANCH-01(config-router-af)# af-interface TenGigabitEthernet1/0/1
BRANCH-01(config-router-af-interface)# no passive-interface
BRANCH-01(config-router-af-interface)# exit-af-interface
BRANCH-01(config-router-af)# topology base
BRANCH-01(config-router-af-topology)# summary-metric 10.20.0.0/16
BRANCH-01(config-router-af-topology)# exit-af-topology
BRANCH-01(config-router-af)# exit-address-family
```

### eBGP at the internet edge

```text
EDGE-01(config)# router bgp 65001
EDGE-01(config-router)# bgp router-id 192.0.2.1
EDGE-01(config-router)# neighbor 203.0.113.1 remote-as 64500
EDGE-01(config-router)# neighbor 203.0.113.1 description ISP-A
EDGE-01(config-router)# address-family ipv4 unicast
EDGE-01(config-router-af)# network 198.51.100.0 mask 255.255.255.0
EDGE-01(config-router-af)# neighbor 203.0.113.1 activate
EDGE-01(config-router-af)# neighbor 203.0.113.1 prefix-list ISP-A-IN in
EDGE-01(config-router-af)# neighbor 203.0.113.1 prefix-list ADVERTISE-OUT out
EDGE-01(config-router-af)# neighbor 203.0.113.1 soft-reconfiguration inbound
EDGE-01(config-router-af)# exit-address-family
```

### Safe redistribution with route tagging

```text
CORE-01(config)# route-map EIGRP-INTO-OSPF permit 10
CORE-01(config-route-map)# match tag 100
CORE-01(config-route-map)# set metric-type type-1
CORE-01(config-route-map)# exit
CORE-01(config)# route-map OSPF-INTO-EIGRP permit 10
CORE-01(config-route-map)# match tag 200
CORE-01(config-route-map)# exit
CORE-01(config)# router ospf 1
CORE-01(config-router)# redistribute eigrp 100 subnets route-map EIGRP-INTO-OSPF tag 200
CORE-01(config-router)# exit
CORE-01(config)# router eigrp CAMPUS
CORE-01(config-router)# address-family ipv4 unicast autonomous-system 100
CORE-01(config-router-af)# topology base
CORE-01(config-router-af-topology)# redistribute ospf 1 route-map OSPF-INTO-EIGRP metric 10000 100 255 1 1500
CORE-01(config-router-af-topology)# exit-af-topology
CORE-01(config-router-af)# exit-address-family
```

Tagging routes with 100 on the EIGRP side and 200 on the OSPF side, and
matching only on the *opposite* tag during redistribution, ensures a route
that originated in OSPF and was redistributed into EIGRP is never
re-permitted back into OSPF at this same boundary router.

### Policy-based routing with IP SLA tracking

```text
EDGE-01(config)# ip sla 1
EDGE-01(config-ip-sla)# icmp-echo 198.51.100.254 source-interface GigabitEthernet0/0/1
EDGE-01(config-ip-sla-echo)# frequency 5
EDGE-01(config-ip-sla-echo)# exit
EDGE-01(config)# ip sla schedule 1 life forever start-time now
EDGE-01(config)# track 10 ip sla 1 reachability
EDGE-01(config)# access-list 101 permit ip 10.30.0.0 0.0.0.255 any
EDGE-01(config)# route-map GUEST-PBR permit 10
EDGE-01(config-route-map)# match ip address 101
EDGE-01(config-route-map)# set ip next-hop verify-availability 198.51.100.254 1 track 10
EDGE-01(config-route-map)# exit
EDGE-01(config)# interface Vlan30
EDGE-01(config-if)# ip policy route-map GUEST-PBR
```

### Configuring VRF-lite for guest traffic isolation

```text
BRANCH-01(config)# vrf definition GUEST
BRANCH-01(config-vrf)# rd 65001:30
BRANCH-01(config-vrf)# address-family ipv4
BRANCH-01(config-vrf-af)# exit-address-family
BRANCH-01(config-vrf)# exit
BRANCH-01(config)# interface Vlan30
BRANCH-01(config-if)# vrf forwarding GUEST
BRANCH-01(config-if)# ip address 10.30.0.1 255.255.255.0
BRANCH-01(config-if)# exit
BRANCH-01(config)# router ospf 2 vrf GUEST
BRANCH-01(config-router)# network 10.30.0.0 0.0.0.255 area 0
```

## Validation and Troubleshooting

```text
CORE-01# show ip ospf neighbor
CORE-01# show ip ospf database
CORE-01# show ip route ospf
CORE-01# show ip eigrp neighbors
CORE-01# show ip eigrp topology
EDGE-01# show ip bgp summary
EDGE-01# show ip bgp neighbors 203.0.113.1 advertised-routes
EDGE-01# show track 10
EDGE-01# show route-map GUEST-PBR
EDGE-01# show ip cef vrf GUEST
```

| Symptom | Likely cause | Check |
| --- | --- | --- |
| OSPF neighbor stuck in `EXSTART`/`EXCHANGE` | MTU mismatch between neighbors | `show interfaces` MTU on both sides; match or `ip ospf mtu-ignore` as a temporary workaround |
| OSPF neighbor stuck in `2WAY` on a broadcast segment | Expected on non-DR/BDR routers; only DR/BDR reach `FULL` | Confirm DR/BDR election with `show ip ospf interface` |
| EIGRP stuck in `Active` (SIA) | No feasible successor and query not answered in time by a downstream neighbor | `show ip eigrp topology active`, check downstream neighbor health and summarization boundaries |
| BGP neighbor stuck in `Idle` or `Active` (session state) | TCP reachability failure, wrong remote-as, or missing `neighbor activate` in the address family | `show ip bgp neighbors`, verify AS numbers and underlying IP reachability |
| Redistributed routes reappearing with worse metric at the source protocol | Missing or incorrect route tagging at a redistribution boundary | `show ip route <prefix>`, trace the tag through each `redistribute` statement |
| PBR not taking effect | Route map applied to the wrong interface direction, or ACL not matching intended traffic | `show route-map`, `show access-list 101`, confirm `ip policy route-map` is on the ingress SVI |

## Security and Best Practices

- Authenticate every routing adjacency: OSPF with SHA-based
  authentication, EIGRP with MD5/SHA key chains, and BGP with MD5 or, where
  supported, TCP-AO.

  ```text
  CORE-01(config)# interface TenGigabitEthernet1/0/1
  CORE-01(config-if)# ip ospf authentication message-digest
  CORE-01(config-if)# ip ospf message-digest-key 1 md5 <KEY>
  ```

- Filter routing information at every administrative or trust boundary
  (branch-to-core, extranet peer, internet edge) using prefix lists or
  distribute lists, not just at redistribution points.
- At the internet edge, apply strict inbound and outbound prefix filters
  and, at minimum, RFC 3704 (uRPF)/bogon filtering to reduce spoofed-source
  traffic and accidental route leaks.
- Use BGP maximum-prefix limits on eBGP sessions to protect the router (and
  the network) from a misbehaving or compromised peer flooding excessive
  routes.

  ```text
  EDGE-01(config-router-af)# neighbor 203.0.113.1 maximum-prefix 100 80 restart 15
  ```

- Log and alert on OSPF/EIGRP adjacency flaps and BGP session resets — they
  are frequently the first visible symptom of a physical, capacity, or
  security problem elsewhere.

## References and Knowledge Checks

**Authoritative references**

- RFC 2328, *OSPF Version 2*.
- RFC 4271, *A Border Gateway Protocol 4 (BGP-4)*.
- Cisco, *IP Routing: EIGRP Configuration Guide*, IOS XE 17.x.
- Cisco, *IP Routing: BGP Configuration Guide*, IOS XE 17.x.

**Knowledge checks**

1. Why must every non-backbone OSPF area attach directly to Area 0 (absent
   a virtual link)?
2. What mechanism prevents a redistribution loop when two routers mutually
   redistribute between OSPF and EIGRP?
3. Which BGP attribute is typically used to influence outbound path
   selection at a multihomed site, and which is used to influence how a
   peer selects a path toward you?
4. When is PBR the appropriate tool instead of adjusting IGP metrics or
   using a floating static route?
5. What problem does VRF-lite solve on a single physical router, and how
   does it relate to the SD-Access virtual network concept introduced
   later in this volume?

## Hands-On Lab

**Objective:** Build a two-area OSPF topology with EIGRP at one branch,
redistribute safely between them, and add IP SLA–tracked PBR for a guest
VRF.

**Prerequisites**

- Four routing-capable Catalyst 9000 devices (or CML IOL/CSR-equivalent
  nodes): `CORE-01` (Area 0/ASBR), `DIST-01` (Area 10), `BRANCH-01`
  (EIGRP AS 100), and a simulated internet-facing neighbor for the PBR
  reachability target.
- Basic IP addressing plan across at least three point-to-point or
  routed-SVI links.

**Procedure**

1. Configure OSPF Area 0 on `CORE-01` and Area 10 (totally stubby) on
   `DIST-01`, as shown in Implementation. Verify adjacency:

   ```text
   CORE-01# show ip ospf neighbor
   ```

   **Expected result:** neighbor state `FULL` on the `CORE-01`–`DIST-01`
   link.

2. Configure EIGRP AS 100 on `BRANCH-01` and `CORE-01`'s branch-facing
   interface, and verify adjacency:

   ```text
   CORE-01# show ip eigrp neighbors
   ```

   **Expected result:** `BRANCH-01` appears as an EIGRP neighbor in `Up`
   state.

3. On `CORE-01`, configure mutual redistribution between OSPF and EIGRP
   using route tags as shown in Implementation.

4. Verify that `DIST-01` learns the EIGRP-originated branch subnet as an
   OSPF external route, and that `BRANCH-01` learns the OSPF-originated
   core subnet as an EIGRP external route:

   ```text
   DIST-01# show ip route ospf
   BRANCH-01# show ip eigrp topology
   ```

   **Expected result:** each side shows the opposite protocol's routes
   present with the expected tag/metric, and no route reappears at its
   originating protocol with a different (looped) path.

5. Configure the GUEST VRF, IP SLA tracking, and PBR on `CORE-01` as shown
   in Implementation, pointing the tracked object at a reachable neighbor
   or loopback simulating an alternate exit path.

6. Verify tracking and PBR state:

   ```text
   CORE-01# show track 10
   CORE-01# show route-map GUEST-PBR
   ```

   **Expected result:** track state shows `Up`, and traffic sourced from
   the guest subnet (10.30.0.0/24) takes the PBR-specified next hop
   instead of the routing table's default path — confirm with `traceroute`
   sourced from a guest-VRF host or `traceroute vrf GUEST`.

7. **Negative test:** shut down the IP SLA target/next hop and confirm PBR
   fails over (or fails closed, per the `verify-availability` behavior)
   rather than silently black-holing traffic:

   ```text
   CORE-01# show track 10
   CORE-01# show ip route vrf GUEST
   ```

   **Expected result:** track state transitions to `Down`, and traffic
   matched by the PBR route map falls back to normal destination-based
   routing instead of being policy-routed to an unreachable next hop.

**Cleanup**

- Remove the PBR route map from the SVI, then remove the route map, ACL,
  IP SLA operation, and tracked object.
- Remove the GUEST VRF and its OSPF VRF instance if this was a shared lab
  device.
- Restore redistribution and area configuration to the lab's baseline or
  remove it entirely if the topology will be reused for a later chapter.

## Summary and Completion Checklist

Enterprise path control combines a chosen IGP (OSPF for vendor-neutral
scale, EIGRP for Cisco-native simplicity and fast convergence) with
disciplined, tagged redistribution at a minimal number of boundaries, BGP
policy at administrative edges, and targeted use of PBR/IP SLA tracking and
VRF-lite where destination-based routing and a single routing table are
not sufficient.

- [ ] Can design and configure a multi-area OSPF topology with appropriate
      stub area types.
- [ ] Can configure EIGRP named mode and explain DUAL's feasible-successor
      model.
- [ ] Can configure eBGP with inbound/outbound prefix filtering.
- [ ] Can redistribute between two IGPs without creating a routing loop.
- [ ] Can configure IP SLA–tracked PBR and VRF-lite segmentation.
- [ ] Completed the hands-on lab, including the IP SLA failover negative
      test and cleanup.
