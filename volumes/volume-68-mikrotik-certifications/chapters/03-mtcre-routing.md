# Chapter 03: MTCRE — Routing

## Learning Objectives

- Explain the MTCRE scope: static and dynamic routing, PTP addressing, tunnels.
- Configure static routes and point-to-point addressing.
- Configure OSPF on RouterOS v7.
- Build tunnels (EoIP, GRE, IPIP) for site interconnection.
- Complete a walkthrough for each MTCRE topic.

## Theory and Architecture

**MTCRE** (Routing Engineer, requires MTCNA) covers moving packets between networks and sites. It
builds on **static routing** (explicit routes, default routes, distance/weights, recursive
next-hops) and **point-to-point (PTP) addressing** (/30 and /32 links), then adds **OSPF** — the
dynamic link-state IGP — which on **RouterOS v7** is configured with a changed model:
`/routing ospf instance`, `/routing ospf area`, and `/routing ospf interface-template` (different
from v6's `/routing ospf network`). MTCRE also covers **tunnels** for connecting sites over the
internet: **EoIP** (Ethernet over IP — bridges L2 across sites), **GRE** (generic L3 tunnel), and
**IPIP** (IP-in-IP), often secured with IPsec. These are the building blocks of a routed MikroTik
network and multi-site VPNs.

## Design Considerations

Use **static routes** for simple/stub networks and **OSPF** where topology changes need dynamic
convergence. Address PTP links with **/30 or /32**. Pick the tunnel by need: **EoIP** to bridge L2,
**GRE/IPIP** for L3 site links; secure them with **IPsec**. On v7, use the **new OSPF syntax**.

## Implementation and Automation

The labs configure a static route, OSPF (v7), and an EoIP/GRE tunnel.

## Validation and Troubleshooting

Confirm the routing model:

```text
Static: /ip route add dst-address=... gateway=...  PTP: /30 or /32 links.
OSPF (v7): /routing ospf instance + area + interface-template (NOT v6 'network').
Tunnels: EoIP (L2 bridge), GRE/IPIP (L3), + IPsec for security. MTCRE requires MTCNA.
```

Common pitfalls: using **v6 OSPF syntax** on v7; and a tunnel with **no route/bridge** to actually
carry traffic.

## Security and Best Practices

Authenticate **OSPF** where supported, secure **tunnels with IPsec**, and keep PTP addressing tidy
(/30 or /32). Summarize routes where possible. Verify the **route table** reflects intent before
trusting connectivity.

## Hands-On Lab

MTCRE walkthroughs. **Shared prerequisites** — two RouterOS nodes (CHR) with a link, in a lab.
**Cost:** none.

### Lab 3.1 — Static and default routes

**Objective:** Add explicit and default routes.

```text
/ip route add dst-address=10.20.0.0/24 gateway=10.0.0.2
/ip route add dst-address=0.0.0.0/0 gateway=192.0.2.1
/ip route print where dst-address=10.20.0.0/24
```

**Expected result:** a specific route to 10.20.0.0/24 and a **default route** — deterministic
forwarding.

**Negative test:** expect remote reachability with **no route**; add the route/next-hop.

**Cleanup:** `/ip route remove [find dst-address=10.20.0.0/24]`.

### Lab 3.2 — PTP addressing

**Objective:** Address a point-to-point link.

```text
/ip address add address=10.0.0.1/30 interface=ether1
# Far end: /ip address add address=10.0.0.2/30 interface=ether1
/ip address print where interface=ether1
```

**Expected result:** a **/30** PTP link between the two routers — an addressed transit link.

**Negative test:** use a large subnet for a two-router link; **/30 (or /32)** fits PTP — size it
right.

**Cleanup:** `/ip address remove [find interface=ether1]`.

### Lab 3.3 — OSPF on RouterOS v7

**Objective:** Bring up an OSPF adjacency (v7 syntax).

```text
/routing ospf instance add name=default version=2 router-id=10.0.0.1
/routing ospf area add name=backbone area-id=0.0.0.0 instance=default
/routing ospf interface-template add area=backbone networks=10.0.0.0/30 interfaces=ether1
/routing ospf neighbor print
```

**Expected result:** an **OSPF** neighbor (RouterOS **v7** model) in Full state — dynamic routing.

**Negative test:** configure `/routing ospf network` (v6 syntax) on v7; use the **v7
instance/area/interface-template** model.

**Cleanup:** `/routing ospf instance remove [find name=default]`.

### Lab 3.4 — EoIP tunnel

**Objective:** Bridge Layer 2 across sites.

```text
/interface eoip add name=eoip-siteB remote-address=203.0.113.2 tunnel-id=100
/interface bridge port add bridge=bridge-lan interface=eoip-siteB
/interface eoip print
```

**Expected result:** an **EoIP** tunnel bridged into the LAN — Layer-2 extension between sites.

**Negative test:** use EoIP but never **bridge** it; add it to the bridge to carry L2 traffic.

**Cleanup:** `/interface eoip remove eoip-siteB`.

### Lab 3.5 — GRE tunnel

**Objective:** Build a Layer-3 site tunnel.

```text
/interface gre add name=gre-siteB remote-address=203.0.113.2 local-address=203.0.113.1
/ip address add address=172.16.0.1/30 interface=gre-siteB
/ip route add dst-address=10.30.0.0/24 gateway=172.16.0.2
/interface gre print
```

**Expected result:** a **GRE** L3 tunnel with a route across it — site-to-site L3 connectivity
(add IPsec to secure).

**Negative test:** send private traffic over the internet with no tunnel; **encapsulate** with
GRE/IPIP (and IPsec) — don't expect bare routing.

**Cleanup:** `/interface gre remove gre-siteB`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

MTCRE covers static and dynamic routing (OSPF on the RouterOS v7 model), PTP addressing, and
tunnels (EoIP for L2, GRE/IPIP for L3, secured with IPsec). Use the v7 OSPF syntax, size PTP links
with /30 or /32, and pick the tunnel type by need.

- [ ] I can add static and default routes.
- [ ] I can address a PTP link.
- [ ] I can configure OSPF with the v7 model.
- [ ] I can build EoIP and GRE tunnels.
- [ ] I completed Labs 3.1–3.5 including each negative test.
