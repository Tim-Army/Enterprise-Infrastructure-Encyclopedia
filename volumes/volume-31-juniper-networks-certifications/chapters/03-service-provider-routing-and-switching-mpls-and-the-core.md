# Chapter 03: Service Provider Routing and Switching — MPLS and the Core

## Learning Objectives

- Build a provider core on Junos: IS-IS or OSPF as the IGP, LDP and
  RSVP-TE label distribution, and segment routing where the track is
  heading
- Deliver L3VPN and L2VPN/EVPN services on MX-class PE routers
- Apply BGP at provider scale: route reflection, families, and policy
  that protects the core
- Position JNCIS-SP (JN0-364) and JNCIP-SP (JN0-664) and the depth
  jump between them

## Theory and Architecture

### The track in one sentence

The Service Provider track certifies the network that sells
connectivity: a label-switched core, service edges that keep customers
separated, and the discipline that keeps a shared infrastructure
stable. **JNCIS-SP (JN0-364)** — written to Junos OS 25.2, the most
current baseline in the program — covers core protocols and transport;
**JNCIP-SP (JN0-664)**, written to 22.3, goes deep on VPN services,
inter-domain, and multicast (both 90 minutes, 65 questions; codes and
versions verified against Juniper's track pages, 22 July 2026).

### The core: IGP for reachability, labels for service

Provider interiors overwhelmingly run **IS-IS** (level 2 flat, wide
metrics) or multi-area OSPF, but the IGP carries only infrastructure
routes — loopbacks and links. Services ride **MPLS**: LDP for
follow-the-IGP simplicity, RSVP-TE where traffic engineering and fast
reroute justify state, and **SR-MPLS** as the modern consolidation —
labels in the IGP itself, TI-LFA repair paths, no per-LSP soft state.
The JNCIP-SP expects fluency in all three and the migration logic
between them.

### Services: VRFs on the edge, BGP in the middle

L3VPN is the workhorse: per-customer routing instances
(`instance-type vrf`), route distinguishers, route targets as BGP
extended communities, and MP-BGP family `inet-vpn` between PEs. L2
services span BGP-signaled L2VPNs, LDP-signaled circuits, VPLS, and —
displacing all of them — **EVPN**. Route reflectors keep the iBGP mesh
sane; families multiply (`inet`, `inet-vpn`, `evpn`, `l2vpn`) on the
same sessions.

## Design Considerations

- **LDP vs. RSVP vs. SR.** Default to SR-MPLS for new cores (simplest
  state model, TI-LFA); RSVP-TE remains where bandwidth reservation
  and explicit paths are contractual; LDP persists as the legacy
  baseline the exams still test.
- **RR placement.** Out-of-path route reflectors on MX or virtualized
  RE instances; always pairs; cluster-id design to avoid path hiding.
- **Core protection is design, not afterthought:** no customer routes
  in the core, BGP only at the rim and the RRs, loopback filters and
  RE protection everywhere (the SRX chapter's mindset applied to MX).

## Implementation and Automation

```text
# IS-IS + LDP core, one PE slice of an L3VPN
set protocols isis interface ge-0/0/0.0 point-to-point
set protocols isis interface lo0.0 passive
set protocols isis level 1 disable
set protocols mpls interface ge-0/0/0.0
set protocols ldp interface ge-0/0/0.0

set routing-instances CUST-A instance-type vrf
set routing-instances CUST-A interface ge-0/0/2.100
set routing-instances CUST-A route-distinguisher 10.30.255.1:100
set routing-instances CUST-A vrf-target target:65000:100
set routing-instances CUST-A protocols bgp group CE neighbor 172.16.1.2 peer-as 65100

set protocols bgp group IBGP type internal local-address 10.30.255.1
set protocols bgp group IBGP family inet-vpn unicast
set protocols bgp group IBGP neighbor 10.30.255.10   # route reflector
```

## Validation and Troubleshooting

- `show isis adjacency` then `show route table inet.3` — no inet.3
  entry, no MPLS next-hop, no service
- `show ldp session` / `show rsvp session` / `show mpls lsp` — the
  transport truth stack
- `show route table CUST-A.inet.0` and
  `show route advertising-protocol bgp <rr> table bgp.l3vpn.0` — the
  service view versus what BGP actually carries
- `ping mpls ldp <fec>` and `traceroute mpls` — data-plane proof the
  control plane cannot fake
- Asymmetric VPN reachability is almost always a route-target import
  miss: `show route table bgp.l3vpn.0 | match <rd>` first

## Security and Best Practices

- Loopback firewall filters rate-limiting protocols, discarding the
  rest — on every core node
- `family inet-vpn` only where contracted; never `keep all` on RRs
  without cause
- TTL security (GTSM) and MD5/TCP-AO on eBGP; per-neighbor prefix
  limits at the customer edge
- Separate management VRF; the core forwards, it is not managed
  in-band through customer paths

## References and Knowledge Checks

- JNCIS-SP (JN0-364) and JNCIP-SP (JN0-664) objectives on Juniper's
  certification pages — the authority on domains and weights
- Junos MPLS, VPNs, and BGP user guides; *MPLS in the SDN Era*
  (O'Reilly, Juniper-centric)

Knowledge checks:

1. A PE learns a VPN route but the CE never sees it. Order the three
   tables you would inspect and the failure each would reveal.
2. Why does SR-MPLS eliminate LDP-IGP synchronization problems by
   construction?
3. Two RRs share one cluster-id versus two: what changes in stored
   state and in failure behavior?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **every exam objective of
the JNCIS-SP (JN0-364) exam** — the Service Provider Routing and Switching
specialist (written to Junos OS 25.2) — mapped in the volume README's coverage
tables. Labs use the Junos CLI on MX-class routers. Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 3.1–3.10** — a Junos SP core of at least three
MX routers with an IGP, MPLS-enabled core interfaces, dual-stack addressing, and
provider-bridging capable interfaces. **Cost:** none beyond lab resources.

### Lab 3.1 — Protocol-Independent Routing (Objective: Protocol-Independent Routing)

**Objective:** Configure RIB groups and filter-based forwarding.

```text
configure
set routing-options static route 198.51.100.0/24 next-hop 10.0.0.2
set routing-options rib-groups RG import-rib [ inet.0 inet.3 ]
commit and-quit
show route table inet.3
show route 198.51.100.0/24
```

**Expected result:** the static route and the RIB group leaking routes between
tables — protocol-independent components (static/aggregate/generated routes, RIB
groups, load balancing, filter-based forwarding) manipulate routing independent of
any protocol; RIB groups share routes across tables (e.g., into `inet.3` for MPLS).

**Negative test:** reference a RIB group that imports into a nonexistent table; the
commit fails — the target tables must exist.

**Cleanup:** `configure; delete routing-options rib-groups RG; delete
routing-options static route 198.51.100.0/24; commit`.

### Lab 3.2 — OSPF (Objective: OSPF)

**Objective:** Bring up OSPF as the SP core IGP and read the LSDB.

```text
configure
set protocols ospf area 0.0.0.0 interface ge-0/0/0.0 interface-type p2p
set protocols ospf area 0.0.0.0 interface lo0.0 passive
commit and-quit
show ospf neighbor
show ospf database router extensive | match "Adv|metric"
```

**Expected result:** OSPF neighbors `Full` on point-to-point core links and the
router LSAs — as the SP core IGP, OSPF advertises loopbacks (the BGP/MPLS next-hops)
and links; point-to-point interface type avoids DR/BDR overhead on core links.

**Negative test:** leave a core link as the default broadcast type; a needless
DR/BDR election adds LSAs and delay — `interface-type p2p` is the SP best practice.

**Cleanup:** `configure; delete protocols ospf; commit`.

### Lab 3.3 — IS-IS (Objective: IS-IS)

**Objective:** Bring up IS-IS with wide metrics for the SP core.

```text
configure
set interfaces lo0 unit 0 family iso address 49.0001.0100.0000.0001.00
set protocols isis interface ge-0/0/0.0 point-to-point
set protocols isis level 1 disable
set protocols isis interface lo0.0 passive
commit and-quit
show isis adjacency
show isis database extensive | match "metric|IP prefix"
```

**Expected result:** L2-only IS-IS adjacencies and wide-metric prefixes — SP cores
run IS-IS L2 flat with wide metrics (for traffic engineering) and the loopback
advertised for MPLS/BGP next-hop resolution.

**Negative test:** run narrow (6-bit) metrics where TE needs wide metrics; large
metrics wrap — wide-metrics (`level 2 wide-metrics-only`) is required for SP TE.

**Cleanup:** `configure; delete protocols isis; delete interfaces lo0 unit 0 family
iso; commit`.

### Lab 3.4 — BGP (Objective: BGP)

**Objective:** Build IBGP with route reflection and read path selection.

```text
configure
set protocols bgp group IBGP type internal local-address 10.0.0.1 cluster 10.0.0.1
set protocols bgp group IBGP neighbor 10.0.0.3
set routing-options autonomous-system 65001
commit and-quit
show bgp summary
show route protocol bgp 203.0.113.0/24 detail | match "localpref|as-path|med"
```

**Expected result:** the IBGP/RR session and best-path attributes — SP BGP uses
route reflectors to avoid a full IBGP mesh; the reflector marks clients with a
`cluster` ID and reflects routes, and path selection follows the standard algorithm.

**Negative test:** an RR without `cluster` reflecting between non-clients drops the
routes (standard IBGP no-readvertise rule) — the cluster/client config enables
reflection.

**Cleanup:** `configure; delete protocols bgp; commit`.

### Lab 3.5 — Layer 2 Bridging and VLANs (Objective: Layer 2 Bridging or VLANs)

**Objective:** Configure provider bridging (Q-in-Q) and an IRB.

```text
configure
set interfaces ge-0/0/1 flexible-vlan-tagging
set interfaces ge-0/0/1 encapsulation extended-vlan-bridge
set interfaces ge-0/0/1 unit 100 vlan-id-list 100 input-vlan-map push vlan-id 200
commit and-quit
show interfaces ge-0/0/1 detail | match "vlan|encapsulation"
show bridge domain
```

**Expected result:** the Q-in-Q (provider bridging) push of an outer S-tag — SP L2
bridging carries customer VLANs transparently by stacking a provider (S-)tag over
the customer (C-)tag (802.1ad Q-in-Q), with virtual switches and IRB for routing.

**Negative test:** single-tagged (no `flexible-vlan-tagging`) interfaces cannot push
an outer tag; Q-in-Q requires flexible/stacked VLAN tagging — the encapsulation must
support two tags.

**Cleanup:** `configure; delete interfaces ge-0/0/1; commit`.

### Lab 3.6 — Spanning-Tree Protocols (Objective: Spanning-Tree Protocols)

**Objective:** Configure MSTP/VSTP and verify per-instance topology.

```text
configure
set protocols mstp configuration-name SP-REGION
set protocols mstp msti 1 vlan 100-200
set protocols mstp interface ge-0/0/1
commit and-quit
show spanning-tree mstp configuration
show spanning-tree bridge msti 1
```

**Expected result:** the MSTP region and per-instance (MSTI) bridge/root — SP L2
uses MSTP (map many VLANs to a few instances) or VSTP (per-VLAN); port roles/states
and BPDU/loop/root protection secure the topology.

**Negative test:** two switches with different MSTP `configuration-name`/revision are
in different regions and fall back to a single CST instance — the region identity
must match for MSTI to span switches.

**Cleanup:** `configure; delete protocols mstp; commit`.

### Lab 3.7 — MPLS (Objective: MPLS)

**Objective:** Signal RSVP and LDP LSPs (and a segment-routing LSP) and verify.

```text
configure
set protocols mpls interface ge-0/0/0.0
set protocols rsvp interface ge-0/0/0.0
set protocols mpls label-switched-path TO-R3 to 10.0.0.3
set protocols ldp interface ge-0/0/0.0
commit and-quit
show mpls lsp
show route table mpls.0
show ldp session
```

**Expected result:** the RSVP LSP `Up`, MPLS label table, and LDP session — MPLS
label-switches packets across the core; **RSVP** signals traffic-engineered LSPs,
**LDP** builds hop-by-hop LSPs to loopbacks, and **segment routing** sources the
path as a label stack without per-LSP core state.

**Negative test:** enable `protocols mpls` on an interface but omit RSVP/LDP; no LSP
signals — a signaling protocol (or SR) is required to distribute labels.

**Cleanup:** `configure; delete protocols mpls; delete protocols rsvp; delete
protocols ldp; commit`.

### Lab 3.8 — IPv6 (Objective: IPv6)

**Objective:** Configure IPv6 routing (OSPFv3/IS-IS/BGP) and verify.

```text
configure
set interfaces ge-0/0/0 unit 0 family inet6 address 2001:db8::1/64
set protocols ospf3 area 0.0.0.0 interface ge-0/0/0.0
commit and-quit
show ospf3 neighbor
show route table inet6.0 protocol ospf3
```

**Expected result:** the OSPFv3 neighbor and IPv6 routes — SP IPv6 runs natively
(OSPFv3, IS-IS multi-topology, BGP inet6) or over an IPv4 core via tunneling/6PE;
Junos keeps IPv6 in `inet6.0`.

**Negative test:** configure `family inet6` addresses but no IPv6 routing protocol;
only directly-connected IPv6 works — dynamic IPv6 routing must be enabled
separately.

**Cleanup:** `configure; delete protocols ospf3; delete interfaces ge-0/0/0 unit 0
family inet6; commit`.

### Lab 3.9 — Tunnels (Objective: Tunnels)

**Objective:** Build a GRE tunnel over the SP core and verify.

```text
configure
set interfaces gr-0/0/10 unit 0 tunnel source 10.0.0.1 destination 10.0.0.3
set interfaces gr-0/0/10 unit 0 family inet address 172.31.1.1/30
commit and-quit
show interfaces gr-0/0/10 terse
ping 172.31.1.2
```

**Expected result:** the GRE tunnel `up` and reachable — IP tunnels (GRE) connect
sites or carry protocols across the SP core where a native path is unavailable, with
the tunnel endpoints routable in the underlay.

**Negative test:** a GRE tunnel needing a tunnel-services PIC/anchor that is not
present fails to come up — MX tunnels require tunnel services (a PIC or
`tunnel-services` bandwidth).

**Cleanup:** `configure; delete interfaces gr-0/0/10; commit`.

### Lab 3.10 — High Availability (Objective: High Availability)

**Objective:** Configure LAG + BFD and read graceful-restart/NSR state.

```text
configure
set interfaces ae0 aggregated-ether-options lacp active
set interfaces ge-0/0/2 ether-options 802.3ad ae0
set protocols bgp group IBGP bfd-liveness-detection minimum-interval 300
set routing-options nonstop-routing
set chassis redundancy graceful-switchover
commit and-quit
show bfd session
show task replication
```

**Expected result:** BFD sessions up and NSR replication active — SP HA combines LAG
(link), BFD (sub-second detection), and control-plane resilience (GRES + NSR keep
sessions across an RE switchover, graceful restart where NSR is unavailable).

**Negative test:** enable NSR without `graceful-switchover`; NSR requires GRES —
the commit or operation flags the missing dependency.

**Cleanup:** `configure; delete interfaces ae0; delete routing-options
nonstop-routing; delete chassis redundancy; delete protocols bgp group IBGP
bfd-liveness-detection; commit`.

## Lab Verification

Verification means CE-to-CE traffic crosses the labeled core, the
label stack is visible in `traceroute mpls`, both induced failures
showed their distinct control-plane signatures, and repairs were
committed with rollback discipline.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

- [ ] Core built: IS-IS, LDP/RSVP/SR roles articulated
- [ ] L3VPN delivered end to end with MP-BGP and RTs explained
- [ ] Transport vs. service troubleshooting stack demonstrated
- [ ] JNCIS-SP (JN0-364) and JNCIP-SP (JN0-664) scopes distinguished
- [ ] Lab failures induced, evidenced, repaired
