# Chapter 03: BGP for Service Providers: Design, Policy, and Scale

## Learning Objectives

- Design provider BGP: iBGP full mesh versus route reflection, and
  eBGP at peering and customer edges
- Configure BGP on IOS XR with address families, and explain the
  multiprotocol structure that carries VPNs and IPv6
- Implement routing policy with RPL (Route Policy Language): filtering,
  attribute manipulation, and communities
- Scale and stabilize BGP: reflection hierarchy, update groups,
  maximum-prefix, dampening, and convergence
- Validate and troubleshoot BGP sessions, path selection, and policy
  outcomes with evidence

## Theory and Architecture

### BGP is the provider's product surface

The IGP (Chapter 02) moves loopbacks; **BGP moves everything a
provider actually sells and exchanges** — full internet tables, VPN
routes, peering and transit relationships. SPCOR's Networking domain
(30%) and SPRI's routing domains lean heavily here. The relationships:

- **iBGP** between all provider BGP speakers, carrying external routes
  internally. The full-mesh requirement (every iBGP speaker peers with
  every other) does not scale, so providers use **route reflectors**.
- **eBGP** to customers (the PE-CE relationship of Chapter 06 in the
  internet-access case), to transit providers, and at peering
  exchanges — each a policy boundary.

### Route reflection

A **route reflector (RR)** re-advertises iBGP routes to its clients,
replacing the full mesh: clients peer only with RRs, RRs peer with
each other. The rules that keep it loop-free — ORIGINATOR_ID and
CLUSTER_LIST — and the design choices (redundant RRs, hierarchy,
placement often on dedicated route-reflector platforms out of the
forwarding path) are core SP knowledge. The failure to avoid:
inconsistent RR client sets that cause some routers to miss routes —
a "works on some devices" outage of exactly the shape Chapter 02's
IGP could also produce, diagnosed the same way.

### Multiprotocol BGP: one protocol, many address families

Modern BGP is **MP-BGP**: one session negotiates multiple address
families — `ipv4 unicast`, `ipv6 unicast`, `vpnv4/vpnv6 unicast`
(the L3VPN carriers of Chapter 06), `l2vpn evpn` (Chapter 07),
`ipv4/ipv6 multicast`. The same iBGP/RR infrastructure carries all
of them, which is why the VPN chapters "just" add an address family
to sessions built here. Reading `show bgp <afi> <safi>` per family is
a daily SP skill.

### Path selection and policy

BGP best-path selection (weight, local-pref, AS-path, origin, MED, eBGP
over iBGP, IGP metric to next-hop, tie-breakers) is the mechanism;
**policy** is how a provider expresses business relationships onto it.
On IOS XR, policy is **RPL** — Route Policy Language — a structured,
readable policy language (versus IOS XE route-maps): match on prefix
sets, AS-path sets, and community sets; set local-preference,
communities, MED, and next-hop. Communities are the provider's
signaling fabric: customer/peer/transit tagging, no-export scopes, and
traffic-engineering community schemes that let one policy act on
thousands of routes by tag rather than by prefix.

## Design Considerations

- **RR hierarchy and redundancy first**: two RRs minimum per cluster,
  consistent client sets, RRs off the forwarding path where scale
  warrants — designed before the first client, because retrofitting
  reflection topology is disruptive.
- **Policy at every eBGP boundary, in both directions**: no eBGP
  session without explicit inbound and outbound policy — the SP
  equivalent of "never trust the customer edge," and a toll-fraud/
  route-leak defense.
- **Community scheme as architecture**: a documented community plan
  (relationship tags, geographic tags, TE tags) is what makes
  policy scale; ad-hoc communities become unmaintainable.
- **Protect the control plane from the table**: maximum-prefix on
  customer/peer sessions, dampening judiciously, and update-group
  efficiency so a churny peer does not destabilize the core.

## Implementation and Automation

BGP on the Chapter 02 core — RR plus a client PE, with RPL policy:

```text
route-policy CUSTOMER-IN
  if destination in CUSTOMER-PREFIXES then
    set local-preference 200
    set community (65000:100) additive
    pass
  else
    drop
  endif
end-policy

router bgp 65000
 bgp router-id 10.0.0.1
 address-family ipv4 unicast
 address-family vpnv4 unicast          ! carried for Chapter 06
 !
 neighbor-group RR-CLIENT
  remote-as 65000
  update-source Loopback0
  address-family ipv4 unicast
   route-reflector-client
  address-family vpnv4 unicast
   route-reflector-client
 !
 neighbor 10.0.0.2
  use neighbor-group RR-CLIENT         ! PE1 as an RR client
 !
 neighbor 203.0.113.1                  ! an eBGP customer/peer
  remote-as 64500
  address-family ipv4 unicast
   route-policy CUSTOMER-IN in
   route-policy CUSTOMER-OUT out
   maximum-prefix 1000 90
```

```text
! Validation
show bgp summary
show bgp ipv4 unicast 203.0.113.0/24          ! best-path reasoning
show bgp vpnv4 unicast summary
show rpl route-policy CUSTOMER-IN
show bgp neighbor 203.0.113.1 | include Prefix
```

## Validation and Troubleshooting

Work sessions, then paths, then policy. **Sessions**: Idle/Active
means the TCP/AS/source-address basics (iBGP needs `update-source
Loopback0` and IGP reachability to the loopback — a Chapter 02
dependency); Established but no routes is address-family or policy.
**Paths**: `show bgp <prefix>` narrates best-path selection field by
field — read it rather than guessing which attribute won.
**Policy**: RPL outcomes are testable — confirm the inbound policy set
the local-pref and community you intended, and that the outbound
policy advertised what it should (`show bgp neighbor ... advertised-
routes`). RR-specific: a client missing routes points at RR client-set
inconsistency or a next-hop-unreachable (the RR reflected a route
whose next-hop the client cannot resolve — `next-hop-self` or
Chapter 04 label reachability). Evidence at each step, always.

## Security and Best Practices

- Inbound and outbound policy on every eBGP session; prefix and
  AS-path filtering of customers, and RPKI origin validation where
  deployed, to blunt route leaks and hijacks.
- maximum-prefix with a warning threshold on customer/peer sessions;
  a customer that suddenly announces a full table should be limited,
  not obeyed.
- TTL security (GTSM) and MD5/TCP-AO on eBGP sessions; control-plane
  protection (Chapter 08) so BGP churn cannot exhaust the RP.

## References and Knowledge Checks

- SPCOR 350-501 v1.1 Networking (30%); SPRI 300-510 Unicast Routing
  (35%) and Routing Policy and Manipulation (25%)
- Cisco IOS XR BGP and RPL configuration guides
- RFC 4271 (BGP-4), RFC 4456 (route reflection), RFC 4760 (MP-BGP)

Knowledge checks:

1. Why does iBGP need a full mesh or route reflection, and which two
   attributes keep reflection loop-free?
2. One RR client is missing a set of routes others have. Give two
   distinct causes and the command that distinguishes them.
3. Walk `show bgp <prefix>` and name the order best-path attributes
   are evaluated to a decision.
4. How does a community scheme let one policy act on thousands of
   routes, and why is that better than prefix lists?

## Hands-On Lab

On the Chapter 02 IGP: build iBGP with a route reflector and PE
clients (loopback-sourced, `vpnv4` family carried for later), and one
eBGP "customer" with inbound/outbound RPL policy and maximum-prefix.
Prove: iBGP sessions Established over loopbacks, the eBGP customer's
routes arriving with the local-pref and community your policy set
(evidence from `show bgp <prefix>`), and outbound advertisements
filtered to policy. Break and diagnose three things: remove
`update-source Loopback0` on one iBGP session (watch it fail and fix
by the evidence), make one RR client set inconsistent (reproduce the
missing-routes symptom), and trip maximum-prefix by announcing beyond
the limit. Restore all.

## Lab Verification

Verification means iBGP/eBGP sessions established with policy visibly
applied, best-path reasoning was read from evidence, and all three
induced faults were diagnosed to cause and repaired. Until then, the
lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

BGP carries what a provider sells: internet tables and, via MP-BGP
address families, every VPN service in this volume. Route reflection
scales iBGP, RPL expresses business policy, communities make policy
scale by tag, and disciplined filtering and limits keep the control
plane safe. It is the heart of SPCOR's Networking domain and both of
SPRI's routing-and-policy domains.

- [ ] My iBGP scales by reflection with redundant, consistent RRs
- [ ] Every eBGP boundary has explicit two-way policy
- [ ] I read best-path from evidence, not intuition
- [ ] My `vpnv4` family is carried, ready for Chapter 06
