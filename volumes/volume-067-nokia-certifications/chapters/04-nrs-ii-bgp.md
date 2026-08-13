# Chapter 04: NRS II — BGP

## Learning Objectives

- Explain BGP's role in the NRS II curriculum.
- Configure IBGP and EBGP on SR OS.
- Apply route policies to control advertisement and selection.
- Verify BGP sessions and the routing table.
- Complete a walkthrough for each BGP topic.

## Theory and Architecture

**BGP** is the inter-domain and service-carrying protocol in a Nokia SR OS network. **EBGP**
exchanges routes between autonomous systems (peering, transit); **IBGP** distributes external and
service routes **within** an AS, typically in a full mesh or via **route reflectors** for scale.
BGP carries not just internet routes but the **VPN address families** (VPN-IPv4/EVPN) that make
L3VPN and EVPN services work — so BGP is the control plane for services, riding on the IGP for
next-hop reachability. On SR OS, BGP is configured under `configure router bgp` with **groups** and
**neighbors**, and **route policies** (prefix lists, AS-path, communities) filter and manipulate
advertisements and best-path selection. Mastery of IBGP/EBGP and policy is central to NRS II.

## Design Considerations

Use **route reflectors** to scale IBGP instead of a full mesh. Keep **next-hop reachability** in
the IGP (BGP relies on it). Control routes with **policies** (import/export), not by leaking
everything. Use **communities** to tag and act on routes consistently across the network.

## Implementation and Automation

The labs configure IBGP and EBGP, apply a route policy, and verify sessions and routes.

## Validation and Troubleshooting

Confirm the BGP model:

```text
EBGP (between AS) + IBGP (within AS; full mesh or route reflectors). Carries internet + VPN/EVPN AFs.
Next-hop from IGP. Route policies (prefix/AS-path/community) for filtering + best-path.
SR OS: configure router bgp group/neighbor + policy-options.
```

Common pitfalls: IBGP routes with an **unreachable next-hop** (fix the IGP or next-hop-self); and
advertising routes with **no policy** control.

## Security and Best Practices

Filter with **import/export policies**, authenticate sessions, and use **route reflectors** for
scale. Ensure BGP next-hops are IGP-reachable. Tag routes with **communities** for consistent
policy. Defensive, controlled advertisement throughout.

## Hands-On Lab

BGP walkthroughs. **Shared prerequisites** — SR OS nodes with an IGP up and system interfaces, in a
lab. **Cost:** none.

### Lab 4.1 — Configure IBGP

**Objective:** Peer two routers within the AS.

```text
A:router>config# router bgp group "internal" type internal peer-as 65000
A:router>config# router bgp group "internal" neighbor 10.0.0.2
A:router# show router bgp summary
```

**Expected result:** an **IBGP** session **Established** (sourced from system interfaces) — internal
route distribution.

**Negative test:** peer IBGP with an **unreachable** system IP; the IGP must reach the peer — fix
reachability first.

**Rollback:** `configure router bgp group "internal" shutdown`.

### Lab 4.2 — Configure EBGP

**Objective:** Peer with another AS.

```text
A:router>config# router bgp group "external" type external peer-as 65100
A:router>config# router bgp group "external" neighbor 172.16.0.2
A:router# show router bgp neighbor 172.16.0.2
```

**Expected result:** an **EBGP** session to AS 65100 **Established** — inter-domain routing.

**Negative test:** set the wrong **peer-as**; EBGP won't establish with an AS mismatch — match it.

**Rollback:** `configure router bgp group "external" shutdown`.

### Lab 4.3 — Apply a route policy

**Objective:** Control advertised prefixes.

```text
A:router>config# policy-options prefix-list "customer" prefix 192.168.0.0/16 longer
A:router>config# policy-options policy-statement "export-cust" entry 10 from prefix-list "customer" action accept
A:router>config# router bgp group "external" export "export-cust"
A:router# show router bgp neighbor 172.16.0.2 advertised-routes
```

**Expected result:** only the **customer** prefixes advertised to the peer — policy-controlled
advertisement.

**Negative test:** export with **no policy**; you may leak internal/transit routes — filter with a
policy.

**Rollback:** remove the export policy.

### Lab 4.4 — Verify BGP routes

**Objective:** Confirm received routes and best path.

```text
A:router# show router bgp routes
A:router# show router route-table protocol bgp
```

**Expected result:** received BGP routes and the selected **best paths** in the route table — BGP
working end to end.

**Negative test:** assume routes are installed without checking; verify **best path** and the route
table.

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

BGP in NRS II covers IBGP (full mesh or route reflectors) and EBGP, carrying internet and VPN/EVPN
address families on IGP-provided next-hops, with route policies controlling advertisement and
selection. Scale IBGP with reflectors, keep next-hops reachable, and control routes with policy.

- [ ] I can configure IBGP.
- [ ] I can configure EBGP.
- [ ] I can apply a route policy.
- [ ] I can verify BGP routes and best path.
- [ ] I completed Labs 4.1–4.4 including each negative test.
