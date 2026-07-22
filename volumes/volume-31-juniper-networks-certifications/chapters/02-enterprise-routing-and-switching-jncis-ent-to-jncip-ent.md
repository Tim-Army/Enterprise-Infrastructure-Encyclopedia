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

Three vJunos switches: two access, one collapsed core. VLANs 10/20
with IRBs and DHCP relay on the core; RSTP with edge protection at
access; OSPF area 0 between core loopbacks and a simulated WAN
router; eBGP at the edge exporting only the campus aggregate. Induce a
failure — unplug an access uplink and a bad export policy that leaks a
/24 — and capture both signatures before repairing them.

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
