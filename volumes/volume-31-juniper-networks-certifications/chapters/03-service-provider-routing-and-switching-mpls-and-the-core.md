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

Four vJunos routers: two P, two PE. IS-IS level 2 with LDP across the
core; one L3VPN with a CE routing instance per PE and eBGP to
simulated CEs; MP-BGP between PE loopbacks. Prove end-to-end customer
reachability, then break it twice — remove one PE's vrf-target import
and take down the LDP session on a core link — capturing the distinct
signatures (bgp.l3vpn.0 route present but not imported; inet.3 next-hop
gone) before repairing both.

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
