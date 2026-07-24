# Chapter 02: Enterprise Routing and Switching — JNCIS-ENT to JNCIP-ENT

## Learning Objectives

- Configure EX/QFX Layer 2: VLANs, trunks, IRB interfaces, and
  spanning tree variants Junos actually runs
- Deploy OSPF and IS-IS for enterprise interiors and BGP at the edge,
  with Junos routing policy as the control layer
- Design campus high availability with Virtual Chassis and EVPN
  multihoming, and know when each fits
- Position the track's two written exams — JNCIS-ENT (JN0-352) and
  JNCIP-ENT (JN0-650) — and what separates them

## Theory and Architecture

### The track in one sentence

The Enterprise Routing and Switching track certifies the campus and
branch: Layer 2 access, routed distribution and core, the WAN edge,
and the services — DHCP, firewall filters, CoS — that make an
enterprise network operable. **JNCIS-ENT (JN0-352)** covers the
protocol mechanics; **JNCIP-ENT (JN0-650)** layers on scale, policy
nuance, EVPN, and troubleshooting depth. Both are 90-minute, 65-question
exams with JNCIA-Junos as the prerequisite (codes verified against
Juniper's track pages, 22 July 2026 — this is the lineup refreshed in
the April 2026 JNCIS-ENT update).

### Layer 2 the Junos way

VLANs live under `vlans` with members assigned per-interface
(`family ethernet-switching`); routing between them happens on **IRB
interfaces** referenced by the VLAN. Spanning tree defaults to RSTP,
with MSTP and VSTP for interop; loop protection adds BPDU protect on
edge ports and root protect toward the access. **Virtual Chassis**
collapses up to ten EX switches into one control plane — one
configuration, one upgrade, dual routing engines for free — the
enterprise answer before EVPN reached the campus.

### Routing: policy is the differentiator

OSPF and IS-IS configuration is compact (`set protocols ospf area 0
interface irb.10`), but Junos distinguishes itself in **policy-options**:
route filters with `exact`, `orlonger`, `prefix-length-range`, policy
chains applied import/export per protocol, and communities as
first-class match conditions. The JNCIP-ENT rewards fluency here —
redistribution with tagging, BGP attribute manipulation, and the
discipline of default-deny export policy on BGP.

## Design Considerations

- **Collapsed core vs. three tiers.** Most enterprises fit a routed
  collapsed core of two QFX/EX with ESI-LAG or Virtual Chassis at
  access; reserve three tiers for genuine scale.
- **EVPN in the campus.** JNCIP-ENT expects campus fabric literacy:
  EVPN-VXLAN with a QFX spine brings the DC operational model —
  anycast gateways, ESI multihoming — to large campuses, replacing
  stretched VLANs and MC-LAG.
- **The WAN edge** stays boring on purpose: eBGP to providers,
  conditional default origination inward, uRPF and filters at the rim.

## Implementation and Automation

```text
# Access + routed core in a dozen lines
set vlans USERS vlan-id 10 l3-interface irb.10
set interfaces ge-0/0/10 unit 0 family ethernet-switching
set interfaces ge-0/0/10 unit 0 family ethernet-switching vlan members USERS
set interfaces irb unit 10 family inet address 10.30.12.1/24
set protocols rstp interface ge-0/0/10 edge
set protocols rstp bpdu-block-on-edge

set protocols ospf area 0.0.0.0 interface irb.10 passive
set protocols ospf area 0.0.0.0 interface ae0.0

# Policy: advertise only aggregates at the edge
set policy-options policy-statement EDGE-OUT term AGG from route-filter 10.30.0.0/16 exact
set policy-options policy-statement EDGE-OUT term AGG then accept
set policy-options policy-statement EDGE-OUT then reject
set protocols bgp group ISP export EDGE-OUT
```

## Validation and Troubleshooting

- `show ethernet-switching table` and `show vlans` — is the MAC where
  you think it is?
- `show spanning-tree interface` — role and state per port; a blocked
  uplink you did not expect is a topology drawing error
- `show ospf neighbor` / `show isis adjacency` — adjacency first,
  routes second; `show ospf database` when LSAs disagree with intent
- `show route advertising-protocol bgp <peer>` and
  `receive-protocol` — what you actually sent and got, post-policy
- `show evpn database` and `show ethernet-switching vxlan-tunnel-end-point`
  when the campus fabric misbehaves

## Security and Best Practices

- Storm control and BPDU protect on every access port, no exceptions
- Firewall filters on IRBs for inter-VLAN policy; loopback filters to
  protect the RE (the enterprise CoPP)
- DHCP snooping with dynamic ARP inspection on user VLANs
- 802.1X where identity matters, MAC-RADIUS where it cannot

## References and Knowledge Checks

- JNCIS-ENT (JN0-352) and JNCIP-ENT (JN0-650) objectives on Juniper's
  certification pages — the authority on domains and weights
- Junos documentation: Ethernet Switching, OSPF, BGP, EVPN user guides
- *Day One: Configuring EX Series Ethernet Switches*

Knowledge checks:

1. Traffic between two VLANs on one EX switch never leaves the box.
   Name the interface type that makes that true and its configuration
   linkage to the VLAN.
2. Your BGP export policy ends without an explicit `then reject`. On
   Junos, what leaks and why?
3. Contrast Virtual Chassis and EVPN ESI multihoming as campus
   redundancy strategies — control planes, failure domains, upgrades.

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **every exam objective of
the JNCIS-ENT (JN0-352) exam** — the Enterprise Routing and Switching specialist —
mapped in the volume README's coverage tables. Labs use the Junos CLI on EX/QFX
switches and MX/SRX routers. Each ends **`**Lab verified by:** *pending*`** until a
human runs it.

**Shared prerequisites for Labs 2.1–2.9** — a Junos switch and two routers running
Junos OS, trunk/access ports, and OSPF/IS-IS/BGP reachability between the routers.
**Cost:** none beyond lab resources.

### Lab 2.1 — Layer 2 Switching and VLANs (Objective: Layer 2 Switching and VLANs)

**Objective:** Configure VLANs, trunking, and inter-VLAN routing (IRB).

```text
configure
set vlans SALES vlan-id 10 l3-interface irb.10
set interfaces ge-0/0/1 unit 0 family ethernet-switching interface-mode access vlan members SALES
set interfaces ge-0/0/0 unit 0 family ethernet-switching interface-mode trunk vlan members [ SALES VOICE ]
set interfaces irb unit 10 family inet address 10.10.10.1/24
commit and-quit
show ethernet-switching table
show vlans
```

**Expected result:** the MAC table by VLAN and the VLAN-to-interface bindings —
Junos bridges within a VLAN, tags on trunks (802.1Q), and routes between VLANs via
an **IRB** (Integrated Routing and Bridging) interface, the L3 gateway for the VLAN.

**Negative test:** put an access port in a VLAN with no IRB and expect inter-VLAN
routing; frames bridge within the VLAN but cannot reach other VLANs — the IRB is the
routed gateway.

**Cleanup:** `configure; delete vlans SALES; delete interfaces irb unit 10; commit`.

### Lab 2.2 — Spanning Tree (Objective: Spanning Tree)

**Objective:** Enable RSTP and read port roles/states.

```text
configure
set protocols rstp interface ge-0/0/0
set protocols rstp interface ge-0/0/1
commit and-quit
show spanning-tree bridge
show spanning-tree interface
```

**Expected result:** the bridge ID/root and each port's role (root/designated/alt)
and state (forwarding/discarding) — RSTP prevents L2 loops by electing a root bridge
and blocking redundant paths, converging faster than legacy STP via proposal/
agreement.

**Negative test:** a link with a lower path cost unexpectedly becomes root port;
adjusting `cost`/`priority` changes the topology — port role follows cost/priority,
not cabling.

**Cleanup:** `configure; delete protocols rstp; commit`.

### Lab 2.3 — Layer 2 Security (Objective: Layer 2 Security)

**Objective:** Apply BPDU/root protection, storm control, and a Layer 2 filter.

```text
configure
set protocols rstp bpdu-block-on-edge
set switch-options interface ge-0/0/1 no-mac-learn 2>/dev/null
set forwarding-options storm-control-profiles SC all bandwidth-level 1000
set interfaces ge-0/0/1 unit 0 family ethernet-switching storm-control SC
commit and-quit
show ethernet-switching interface ge-0/0/1
```

**Expected result:** the port with storm-control and edge BPDU blocking — Layer 2
security hardens the access edge: **BPDU/root/loop protection** (keep the topology
stable against rogue switches), **port security** (MAC limiting, DHCP snooping, DAI,
IP source guard), **MACsec**, and **storm control**.

**Negative test:** a host port receiving BPDUs with `bpdu-block-on-edge` is disabled
(BPDU-inconsistent) — the protection blocks a switch plugged into an access port.

**Cleanup:** `configure; delete forwarding-options storm-control-profiles;
delete protocols rstp bpdu-block-on-edge; commit`.

### Lab 2.4 — Protocol-Independent Routing (Objective: Protocol-Independent Routing)

**Objective:** Configure static/aggregate routes and per-flow load balancing.

```text
configure
set routing-options aggregate route 172.16.0.0/16
set policy-options policy-statement ECMP then load-balance per-packet
set routing-options forwarding-table export ECMP
commit and-quit
show route 172.16.0.0/16
show route forwarding-table destination 172.16.0.0
```

**Expected result:** the aggregate route and per-flow load-balancing in the FIB —
protocol-independent components (static, aggregate, generated routes, RIB groups,
load balancing, filter-based forwarding) shape forwarding regardless of the routing
protocol; the `per-packet` policy enables ECMP in the FIB (Junos hashes per flow).

**Negative test:** an aggregate route with no contributing (more-specific) route is
not active; Junos suppresses it until a contributor exists — aggregates need a
contributing route.

**Cleanup:** `configure; delete routing-options aggregate; delete routing-options
forwarding-table export; commit`.

### Lab 2.5 — OSPF (Objective: OSPF)

**Objective:** Bring up OSPF and read the LSDB and adjacencies.

```text
configure
set protocols ospf area 0.0.0.0 interface ge-0/0/0.0
set protocols ospf area 0.0.0.0 interface lo0.0 passive
commit and-quit
show ospf neighbor
show ospf database
show route protocol ospf
```

**Expected result:** OSPF neighbors in `Full`, the link-state database, and learned
routes — OSPF floods LSAs within an area to build a common LSDB, elects DR/BDR on
broadcast links, and computes SPF; Junos shows neighbor state, LSDB, and results.

**Negative test:** an MTU or area-ID mismatch leaves the neighbor stuck in
`ExStart`/`Init`; `show ospf neighbor` reveals the non-Full state — parameters must
match.

**Cleanup:** `configure; delete protocols ospf; commit`.

### Lab 2.6 — IS-IS (Objective: IS-IS)

**Objective:** Bring up IS-IS and read levels/adjacencies.

```text
configure
set interfaces lo0 unit 0 family iso address 49.0001.0100.0000.0001.00
set protocols isis interface ge-0/0/0.0
set protocols isis interface lo0.0 passive
commit and-quit
show isis adjacency
show isis database
show route protocol isis
```

**Expected result:** IS-IS adjacencies (L1/L2), the LSP database, and learned routes
— IS-IS runs on CLNS with a NET address, forms L1 (intra-area) and L2 (inter-area)
adjacencies, and floods LSPs; Junos requires the `iso` family and a NET on lo0.

**Negative test:** omit the `iso` family/NET on lo0; IS-IS never forms an adjacency —
the NET address is mandatory.

**Cleanup:** `configure; delete protocols isis; delete interfaces lo0 unit 0 family
iso; commit`.

### Lab 2.7 — BGP (Objective: BGP)

**Objective:** Establish EBGP/IBGP and read path selection.

```text
configure
set protocols bgp group EXT type external peer-as 65002 neighbor 10.0.0.2
set routing-options autonomous-system 65001
commit and-quit
show bgp summary
show route receive-protocol bgp 10.0.0.2
show route 203.0.113.0/24 detail
```

**Expected result:** the BGP session `Established`, received routes, and the best-
path attributes — BGP exchanges NLRI with path attributes and selects best by the
ordered algorithm (local-pref, AS-path, origin, MED, …); IBGP vs EBGP differ in
next-hop and loop-prevention rules.

**Negative test:** an IBGP peer with no `next-hop self` or IGP route to the next-hop
leaves routes hidden — IBGP next-hop reachability must be resolved.

**Cleanup:** `configure; delete protocols bgp; commit`.

### Lab 2.8 — IP Tunnels (Objective: IP Tunnels)

**Objective:** Build a GRE tunnel and verify it carries traffic.

```text
configure
set interfaces gr-0/0/0 unit 0 tunnel source 10.0.0.1 destination 10.0.0.2
set interfaces gr-0/0/0 unit 0 family inet address 172.31.0.1/30
commit and-quit
show interfaces gr-0/0/0
ping 172.31.0.2
```

**Expected result:** the GRE interface `up` and a successful ping across it — IP
tunnels (GRE, IP-IP) encapsulate traffic to connect networks across an intermediate
IP network; the tunnel needs a routable source/destination and a tunnel PIC/service.

**Negative test:** a GRE tunnel whose destination is unreachable in the underlay
stays down; `show interfaces gr-0/0/0` shows no session — the underlay path to the
tunnel endpoint is required.

**Cleanup:** `configure; delete interfaces gr-0/0/0; commit`.

### Lab 2.9 — High Availability (Objective: High Availability)

**Objective:** Configure a LAG and VRRP, and verify redundancy.

```text
configure
set interfaces ae0 aggregated-ether-options lacp active
set interfaces ge-0/0/2 ether-options 802.3ad ae0
set interfaces ge-0/0/3 ether-options 802.3ad ae0
set interfaces irb unit 10 family inet address 10.10.10.2/24 vrrp-group 1 virtual-address 10.10.10.1
set interfaces irb unit 10 family inet address 10.10.10.2/24 vrrp-group 1 priority 200
commit and-quit
show lacp interfaces ae0
show vrrp
```

**Expected result:** the LAG with LACP up and VRRP with a master/backup — HA in Junos
spans link (LAG/RTG), device (Virtual Chassis), control-plane (GRES, NSR, NSB,
graceful restart), and gateway (VRRP) redundancy, plus BFD for fast detection and
ISSU for hitless upgrades.

**Negative test:** a VRRP group with mismatched virtual-address or authentication
between routers elects two masters (both active) — the group parameters must match.

**Cleanup:** `configure; delete interfaces ae0; delete interfaces irb unit 10 family
inet address 10.10.10.2/24 vrrp-group 1; commit`.

## Lab Verification

Verification means inter-VLAN traffic flows through the IRBs, the
spanning-tree roles match the design drawing, OSPF and BGP tables
carry exactly the intended routes (aggregate out, nothing more), and
both induced failures were demonstrated with distinct evidence and
then repaired with commit-confirmed discipline.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

- [ ] Layer 2: VLANs, IRB, RSTP protection configured and explained
- [ ] OSPF interior with passive edges; policy-controlled BGP rim
- [ ] Virtual Chassis vs. EVPN campus multihoming articulated
- [ ] JNCIS-ENT (JN0-352) and JNCIP-ENT (JN0-650) scopes distinguished
- [ ] Lab failures induced, evidenced, and repaired
