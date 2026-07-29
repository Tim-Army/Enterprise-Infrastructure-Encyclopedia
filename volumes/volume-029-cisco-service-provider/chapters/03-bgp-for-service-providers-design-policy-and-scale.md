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

This chapter carries a topic-level walkthrough lab for **the BGP and routing-
policy objectives of SPCOR 350-501 v1.1 (Domain 2) and Domains 1 and 3 of SPRI
300-510 v1.1** — mapped in the volume README's coverage tables. Labs use the IOS
XR CLI and Route Policy Language (RPL). Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 3.1–3.10** — an IOS XR network with IBGP (route
reflectors) and EBGP to a peer/customer, dual-stack address families, and RPL
policies applied to sessions. **Cost:** none beyond lab resources.

### Lab 3.1 — Describe the BGP path selection algorithm (SPCOR Objective 2.3)

**Objective:** Read why one path won over another.

```text
show bgp ipv4 unicast <prefix>
show bgp ipv4 unicast <prefix> bestpath-compare
```

**Expected result:** the best path with its attributes — BGP selects on the
ordered list (weight, local-pref, locally originated, AS-path length, origin,
MED, eBGP over iBGP, IGP metric to next-hop, oldest, router-id); the bestpath
output names the deciding step.

**Negative test:** expect the shortest AS-path to win when a higher local-pref is
set upstream; local-pref outranks AS-path — the order of the algorithm decides.

**Cleanup:** none (read-only).

### Lab 3.2 — Implement BGP for IPv4 and IPv6, IBGP and EBGP (SPCOR Objective 2.4)

**Objective:** Bring up IBGP (RR) and EBGP sessions across address families.

```text
show bgp all all summary
show bgp ipv6 unicast summary
show bgp sessions
```

**Expected result:** IBGP and EBGP neighbors `Established` across IPv4/IPv6 —
SP BGP uses route reflectors for IBGP scale and EBGP to customers/peers, with
next-hop-self or IGP-carried next-hops and consistent address-family activation.

**Negative test:** an IBGP session up but no routes learned usually means the RR
lacks `route-reflector-client` on the neighbor — the reflector must mark clients.

**Cleanup:** none (read-only).

### Lab 3.3 — Implement routing policy language and route maps (SPCOR Objective 2.5)

**Objective:** Apply an RPL policy and confirm its effect.

```text
show rpl route-policy SET-LP detail
show bgp ipv4 unicast neighbors <peer> routes | head
```

**Expected result:** the RPL policy and the attribute it sets/filters — IOS XR
uses **Route Policy Language** (structured `if/then`, sets, prefix-sets,
community-sets) applied inbound/outbound per neighbor, replacing IOS route-maps
with a composable language.

**Negative test:** apply an RPL policy that references an undefined prefix-set; the
commit fails — RPL requires its referenced sets to exist, catching errors at
commit.

**Cleanup:** remove the test policy from the neighbor.

### Lab 3.4 — Troubleshoot routing protocols (SPCOR Objective 2.6)

**Objective:** Diagnose a route not installed or a session down.

```text
show bgp ipv4 unicast <prefix> detail
show route ipv4 <prefix>
show bgp neighbor <peer> | include "state|last reset"
```

**Expected result:** the route state and the RIB decision — a BGP route present
but not in the RIB traces to next-hop unreachability or a lower-priority protocol;
a session flapping traces to the last-reset reason (hold timer, notification).

**Negative test:** blame policy for a route that is simply not selected because
its BGP next-hop is unreachable in the IGP — fix the next-hop reachability first.

**Cleanup:** none (read-only).

### Lab 3.5 — Describe BGP scalability and performance (SPRI Objective 1.4)

**Objective:** Read the scaling features on a large BGP node.

```text
show bgp process performance-statistics | head
show bgp summary | include "memory|prefixes"
show bgp update-group
```

**Expected result:** update-group batching and prefix/memory scale — BGP scales
via **route reflection** (no full mesh), **update groups** (shared outbound
policy = one update built for many peers), and features like **BGP PIC**/
**add-path** and selective RIB download; the statistics show the efficiency.

**Negative test:** give each peer a unique outbound policy and update groups
fragment, raising CPU on updates — shared policy keeps peers in one update group.

**Cleanup:** none (read-only).

### Lab 3.6 — Troubleshoot BGP (SPRI Objective 1.5)

**Objective:** Diagnose a stuck or missing BGP advertisement.

```text
show bgp ipv4 unicast neighbors <peer> advertised-routes | head
show bgp ipv4 unicast neighbors <peer> received routes 2>/dev/null | head
show bgp ipv4 unicast <prefix> detail | include "not advertised|suppressed"
```

**Expected result:** what is advertised vs received and any suppression — a prefix
not reaching a peer traces to an outbound policy deny, next-hop/validity, or
aggregation suppression; the advertised/received views localize the direction.

**Negative test:** expect a route to propagate through an RR to a non-client peer;
by IBGP rules a route learned from a client is reflected, but the topology and
client marking matter — check the RR client relationships.

**Cleanup:** none (read-only).

### Lab 3.7 — Compare routing policy language and route maps (SPRI Objective 3.1)

**Objective:** Contrast RPL structure with legacy route-map logic.

```text
show rpl route-policy <name>
show rpl prefix-set <name>
show rpl community-set <name>
```

**Expected result:** the modular RPL objects — RPL composes reusable **sets**
(prefix/community/as-path) and **policies** with parameters and boolean logic,
where IOS route-maps are sequential numbered clauses; RPL is more powerful and
testable but a different mental model.

**Negative test:** port a route-map's implicit "permit remaining" assumption to
RPL; RPL's default is `drop` if no `pass` is hit — the end-of-policy behavior
differs and must be explicit.

**Cleanup:** none (read-only).

### Lab 3.8 — Describe conditional matching (SPRI Objective 3.2)

**Objective:** Read a policy's conditional match constructs.

```text
show rpl route-policy MATCH-DEMO detail
```

**Expected result:** the `if` conditions (prefix-set, community, as-path,
med, tag) and their actions — conditional matching selects routes by attribute
and applies sets/pass/drop; nested `if/elseif/else` and `and/or` give fine-grained
control.

**Negative test:** a condition using an `exact` prefix-set match where a
`longer`/`orlonger` was intended silently matches nothing — the match modifier
changes the result set.

**Cleanup:** none (read-only).

### Lab 3.9 — Troubleshoot route manipulation for IGPs (SPRI Objective 3.3)

**Objective:** Diagnose IGP redistribution/filtering gone wrong.

```text
show route ipv4 <prefix> detail | include "redist|tag|metric"
show rpl route-policy IGP-REDIST detail
show isis | include redistribution 2>/dev/null
```

**Expected result:** the redistributed route's tag/metric and the controlling
policy — IGP route manipulation (redistribution, summarization, tagging) gone
wrong shows as missing routes, wrong metrics, or loops; the tag/policy localize
it.

**Negative test:** redistribute between two IGPs without tag-based loop prevention;
routes loop back and cause instability — tags/route-policy must break the loop.

**Cleanup:** none (read-only).

### Lab 3.10 — Troubleshoot route manipulation for BGP (SPRI Objective 3.4)

**Objective:** Diagnose a BGP attribute manipulation not taking effect.

```text
show bgp ipv4 unicast <prefix> detail | include "local pref|metric|community|as-path"
show rpl route-policy BGP-INOUT detail
```

**Expected result:** the applied attributes vs the policy intent — a local-pref or
community not applied traces to the policy attached to the wrong direction/neighbor,
an ordering issue, or a missing `pass`; the route detail vs the policy reveals it.

**Negative test:** set local-pref in an *outbound* policy to an EBGP peer expecting
it to influence the peer; local-pref is non-transitive (IBGP only) — it does not
cross the EBGP boundary.

**Cleanup:** none (read-only).

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
