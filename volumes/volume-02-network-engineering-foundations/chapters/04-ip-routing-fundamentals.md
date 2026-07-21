# Chapter 4: IP Routing Fundamentals

![Lab topology for this chapter: router r1 (loopback 192.168.1.1/32) connects to r2 over 10.0.12.0/30; r2 connects to r3 (loopback 192.168.3.1/32) over 10.0.23.0/30; all three run FRRouting's ospfd advertising their connected interfaces into Area 0, and r1 learns a dynamic route to 192.168.3.1/32 via r2 despite having no direct link to r3. As a negative test, the r1–r2 link is set down; OSPF withdraws the route to 192.168.3.1/32, and a subsequent ping from r1 fails immediately with 'Network is unreachable' rather than timing out.](../../../diagrams/volume-02-network-engineering-foundations/chapter-04-ospf-three-router-topology.svg)

*Figure 4-1. Topology used throughout this chapter's Hands-On Lab: a three-router line topology running OSPF in a single area, with a simulated link failure to observe convergence.*

## Learning Objectives

- Explain how a router builds and uses a routing table, including the
  longest-prefix-match forwarding decision.
- Configure and justify the use of static routes, including default routes
  and floating static routes for backup paths.
- Compare distance-vector, link-state, and path-vector dynamic routing
  protocol families and identify a representative protocol for each.
- Explain administrative distance and route metrics, and how a router
  chooses among multiple sources offering a route to the same destination.
- Describe the fundamentals of OSPF area design and BGP's role at
  enterprise-to-provider boundaries, sufficient to reason about routing
  behavior even before vendor-specific configuration ([Volume III](../../volume-03-cisco-enterprise-networking/README.md)).
- Validate routing behavior and diagnose common routing failures using
  standard show/diagnostic commands.

## Theory and Architecture

### The Routing Table and Forwarding Decision

A router (or a Layer 3 switch acting as one) maintains a Routing
Information Base (RIB), commonly viewed as "the routing table," containing
destination prefixes, the next-hop address or exit interface for each, and
metadata used to select among competing sources. For every packet, the
router performs a **longest-prefix match**: among all routes that cover the
destination address, the most specific (longest) matching prefix wins,
regardless of which protocol installed it.

```text
device# show ip route
Codes: C - connected, S - static, O - OSPF, B - BGP

C    10.1.0.0/24 is directly connected, Vlan10
O    10.1.0.0/22 [110/20] via 10.254.0.2, 00:12:44, Vlan100
S*   0.0.0.0/0 [1/0] via 203.0.113.1
```

Given a packet destined for `10.1.0.5`, the router matches both the `/24`
connected route and the `/22` OSPF route, and forwards using the `/24`
because it is the longer (more specific) match — the `/22` would only be
used for destinations outside the `/24` but inside the `/22`, such as
`10.1.2.10`.

### Administrative Distance and Route Metrics

When multiple sources offer a route to the *same* prefix, the router first
compares **administrative distance (AD)** — a per-source trust ranking —
and installs the route from the lowest-AD source; only routes from the same
source with the same AD are then compared by protocol-specific **metric**
(cost, hop count, etc.) to select the best path.

| Route Source | Typical Administrative Distance |
| --- | --- |
| Directly connected | 0 |
| Static route | 1 |
| eBGP | 20 |
| OSPF | 110 |
| RIP | 120 |
| iBGP | 200 |

This is why a static route (AD 1) overrides a dynamic OSPF route (AD 110)
to the identical prefix by default — a property deliberately exploited by
**floating static routes**, which are configured with an elevated AD so
they remain inactive backups unless the preferred dynamic route is
withdrawn.

### Static Routing

A static route is an administrator-defined, fixed mapping from a
destination prefix to a next hop or exit interface. Static routing requires
no protocol overhead and is fully deterministic, making it appropriate for
small topologies, stub networks with a single exit, and explicit backup
paths — but it does not adapt automatically to topology changes, so its
use at scale requires an operational process (often automation-driven) to
keep it correct.

```text
device(config)# ip route 192.168.100.0 255.255.255.0 10.254.0.2
device(config)# ip route 0.0.0.0 0.0.0.0 203.0.113.1
device(config)# ip route 0.0.0.0 0.0.0.0 203.0.113.5 250
```

The third line is a floating static default route with AD 250, used only if
the primary default route (AD 1 implicitly, or explicitly set lower) is
withdrawn.

### Dynamic Routing Protocol Families

Dynamic routing protocols automatically discover topology and adapt to
changes. Three families matter for enterprise design:

- **Distance-vector** protocols (historically RIP) exchange reachability
  and a metric (hop count) with directly connected neighbors only, applying
  the Bellman-Ford algorithm; each router trusts its neighbors' advertised
  distance without independently knowing the full topology. Simple to
  configure, but slow to converge and prone to routing loops without
  mitigations (split horizon, route poisoning), which is why RIP is largely
  legacy in modern enterprise design.
- **Link-state** protocols (OSPF, IS-IS) flood link-state information to
  every router in an area so each router independently builds an identical
  topology map (the link-state database) and computes shortest paths with
  Dijkstra's algorithm. Converges faster and scales better than distance
  vector through hierarchical area design, at the cost of higher CPU/memory
  use for the topology database.
- **Path-vector** protocols (BGP) exchange full AS-path information rather
  than a simple metric, enabling policy-based route selection across
  administrative boundaries — the defining requirement at the boundary
  between an enterprise and its Internet service providers, and
  increasingly between an enterprise campus/data-center fabric's own
  autonomous routing domains.

### OSPF Area Design Fundamentals

OSPF (Open Shortest Path First, [RFC 2328](https://www.rfc-editor.org/rfc/rfc2328) for OSPFv2/IPv4, [RFC 5340](https://www.rfc-editor.org/rfc/rfc5340) for
OSPFv3/IPv6) organizes a routing domain into **areas** to bound the size of
the link-state database any single router must maintain. **Area 0** (the
backbone) is mandatory, and every other area must connect to it directly
or via a virtual link, because inter-area routes are summarized and
distributed through the backbone.

| Area Type | Characteristic |
| --- | --- |
| Backbone (Area 0) | Connects all other areas; required in any multi-area design |
| Standard area | Receives intra-area, inter-area, and external routes |
| Stub area | Blocks external (redistributed) routes; relies on a default route instead |
| Totally stubby area | Blocks external and inter-area routes; relies entirely on a default route |
| Not-So-Stubby Area (NSSA) | Stub area that still permits limited external route redistribution |

Routers connecting two areas are **Area Border Routers (ABRs)**; routers
connecting OSPF to another routing domain are **Autonomous System Boundary
Routers (ASBRs)**. Area design is a direct extension of the addressing
hierarchy from [Chapter 2](02-ip-addressing-and-subnetting.md): an area boundary should align with a
summarizable address block so the ABR can advertise one aggregate route
instead of every internal prefix.

### BGP Fundamentals

Border Gateway Protocol (BGP, [RFC 4271](https://www.rfc-editor.org/rfc/rfc4271)) is the path-vector protocol that
routes the global Internet and is used at the enterprise edge to exchange
routes with one or more Internet Service Providers, and increasingly
internally (iBGP) as a scalable alternative to link-state protocols in
large data-center fabrics. Every BGP speaker belongs to an **Autonomous
System (AS)**, identified by an AS number; **eBGP** sessions run between
routers in different autonomous systems (typically enterprise-to-ISP),
while **iBGP** sessions run between routers in the same AS. BGP's route
selection is policy-driven — attributes such as AS-path length, local
preference, and MED influence path selection far more than a simple
distance metric, which is what makes BGP suitable for expressing business
routing policy (preferred provider, backup provider, traffic engineering)
rather than pure shortest-path selection.

### Redistribution

**Redistribution** injects routes learned by one protocol (or static
routes) into another routing protocol's advertisements, commonly needed at
a boundary between an OSPF campus core and a legacy or acquired network
still running a different protocol, or when advertising static routes into
a dynamic protocol. Redistribution requires deliberate metric translation
and filtering (route maps or equivalent) to prevent routing loops and
unintended route leaking — an unfiltered two-way redistribution boundary
is one of the most common causes of large-scale routing instability in
enterprise networks.

## Design Considerations

- **Choose static vs. dynamic based on topology stability and exit
  diversity**, not team preference: a single-homed branch with one WAN
  circuit rarely benefits from a dynamic protocol's complexity, while a
  multi-homed data center core needs dynamic routing to adapt to link and
  device failures within seconds rather than requiring manual
  intervention.
- **Align OSPF area (or equivalent hierarchical) boundaries with the
  addressing plan** established in [Chapter 2](02-ip-addressing-and-subnetting.md), so that ABRs can summarize;
  retrofitting summarization onto a flat, single-area design later requires
  a coordinated readdressing effort.
- **Plan redistribution boundaries deliberately and filter both
  directions.** Every redistribution point is a place where routing
  information crosses an administrative or protocol boundary and needs
  explicit route filtering to prevent loops, route leaks, and unintended
  transit.
- **Size the routing domain to the failure domain you are willing to
  accept.** A single large OSPF area converges as one unit; a poorly
  planned single-area design across an entire enterprise means a link
  flap anywhere triggers a shortest-path recomputation everywhere.
- **At the Internet edge, plan for multi-homing requirements early** (single
  provider vs. dual provider, provider-independent vs. provider-assigned
  address space, and the AS number strategy) since these decisions affect
  BGP policy design, addressing portability, and failover behavior in ways
  that are expensive to change after the fact.

## Implementation and Automation

### Verifying and Configuring Routing (Vendor-Neutral Pseudo-CLI)

```text
device(config)# router ospf 1
device(config-router)# router-id 10.254.0.1
device(config-router)# network 10.1.0.0 0.0.0.255 area 0
device(config-router)# network 10.254.0.0 0.0.0.3 area 0
device(config-router)# area 10 stub

device(config)# router bgp 65001
device(config-router)# neighbor 203.0.113.1 remote-as 65010
device(config-router)# network 198.51.100.0 mask 255.255.255.0
```

### Automating Route Verification

Manually reading `show ip route` output across dozens of devices does not
scale; structured output (many platforms support a machine-readable output
mode) enables automated pre/post-change validation:

```bash
# Example using a NETCONF/RESTCONF- or gNMI-capable device via a Python
# automation library to confirm a specific prefix's next hop before and
# after a maintenance window
python3 - <<'PYEOF'
from napalm import get_network_driver

driver = get_network_driver("ios")
device = driver("10.254.0.1", "automation", "REDACTED")
device.open()
route_table = device.get_route_to(destination="10.1.0.0/24")
print(route_table)
device.close()
PYEOF
```

```yaml
# Ansible: assert the expected next hop is present after a change,
# failing the play (and the pipeline) if routing did not converge as expected
- name: Validate routing table after change window
  hosts: core_routers
  gather_facts: false
  tasks:
    - name: Gather routing facts
      cisco.ios.ios_facts:
        gather_subset: min
        gather_network_resources: static_routes

    - name: Assert default route is present
      ansible.builtin.assert:
        that:
          - "'0.0.0.0/0' in (ansible_network_resources.static_routes | json_query('[].address_families[].routes[].dest'))"
```

This kind of pre/post-change routing assertion, run automatically as part
of a change pipeline, catches routing regressions before they reach a
human reviewing logs — treating the routing table as a testable artifact
rather than something confirmed only by eye.

## Validation and Troubleshooting

```text
device# show ip route 10.1.0.0
device# show ip protocols
device# show ip ospf neighbor
device# show ip bgp summary
device# traceroute 10.1.0.5
```

| Symptom | Likely Cause | Diagnostic |
| --- | --- | --- |
| Expected route missing from the routing table | Route not advertised, filtered by a route map/prefix list, or protocol neighbor down | `show ip route`, `show ip ospf neighbor` / `show ip bgp summary` |
| Traffic takes an unexpected path | Administrative distance or metric favors a different source than expected | `show ip route <prefix>` (shows AD/metric), compare against design intent |
| OSPF neighbor stuck in `EXSTART`/`EXCHANGE` | MTU mismatch between neighbors | `show interface` (compare MTU), `show ip ospf interface` |
| OSPF neighbor never forms | Area mismatch, authentication mismatch, or mismatched hello/dead timers | `show ip ospf interface`, compare area ID and timers on both sides |
| BGP session stuck in `Active` or `Idle` | TCP reachability failure (ACL, firewall, or wrong neighbor IP) or AS number mismatch | `show ip bgp summary`, `telnet <neighbor> 179` to test TCP reachability |
| Routing loop (TTL exhausted, traceroute cycles) | Unfiltered redistribution between two protocols/domains | `traceroute`, review redistribution route-map filters |

Longest-prefix match is the first thing to check whenever traffic appears
to take an unexpected path: confirm which prefixes actually match the
destination and compare their length before assuming an AD or metric
problem, since a more specific route anywhere in the table always wins
regardless of AD or metric on a less specific competing route.

## Security and Best Practices

- Authenticate routing protocol adjacencies (MD5 or, where supported,
  stronger HMAC-based authentication for OSPF and BGP) to prevent
  unauthorized devices from forming a neighbor relationship and injecting
  false routes.
- Filter routes at every redistribution boundary and at every eBGP session
  using explicit prefix lists or route maps — never redistribute or accept
  routes unconditionally, since an unfiltered boundary allows routing
  information (and potential traffic interception via more-specific route
  injection) to cross a trust boundary unchecked.
- Apply BGP prefix limits (`maximum-prefix` or equivalent) on eBGP sessions
  with external peers to prevent a misconfigured or compromised peer from
  overwhelming the router with an excessive route count.
- Use unicast Reverse Path Forwarding (uRPF) at edges where source address
  spoofing is a concern, validating that the source address of an incoming
  packet is reachable via the interface it arrived on.
- Restrict which routers/interfaces can participate in a routing protocol
  (passive-interface by default, explicit `network` statements or
  interface-level protocol enablement) so that access-layer or
  user-facing segments never become routing protocol speakers.

## References and Knowledge Checks

**References**

- [RFC 2328 — OSPF Version 2](https://www.rfc-editor.org/rfc/rfc2328)
- [RFC 5340 — OSPF for IPv6 (OSPFv3)](https://www.rfc-editor.org/rfc/rfc5340)
- [RFC 4271 — A Border Gateway Protocol 4 (BGP-4)](https://www.rfc-editor.org/rfc/rfc4271)
- [RFC 2827 / BCP 38 — Network Ingress Filtering](https://www.rfc-editor.org/rfc/rfc2827)
- [RFC 1058 — Routing Information Protocol](https://www.rfc-editor.org/rfc/rfc1058)

**Knowledge Checks**

1. A router has both a `/24` static route and a `/22` OSPF route covering
   the same destination host. Which route forwards the packet, and why?
2. Explain the difference between administrative distance and metric, and
   give an example where they resolve a route selection differently.
3. Why is Area 0 mandatory in a multi-area OSPF design?
4. What operational problem does a floating static route solve, and how is
   it configured to remain inactive under normal conditions?
5. Why does unfiltered two-way redistribution between two routing domains
   create a risk of routing loops?
6. Name two BGP path attributes used in route selection and explain why
   path-vector policy control matters more at an enterprise's Internet edge
   than at its access layer.

## Hands-On Lab

**Objective.** Build a three-router topology using Linux network
namespaces and FRRouting (FRR), configure OSPF to dynamically learn routes
across it, and confirm convergence after a simulated link failure.

**Prerequisites**

- A Linux host with `sudo` access and FRRouting installed
  (`sudo apt-get install frr frr-pythontools`, or the equivalent for the
  lab distribution).
- `iproute2` and familiarity with the namespace conventions from earlier
  chapters in this volume.
- Enable the OSPF daemon in FRR's `/etc/frr/daemons` file
  (`ospfd=yes`) before starting the service, then restart FRR
  (`sudo systemctl restart frr`).

**Lab Steps**

1. Create three router namespaces (`r1`, `r2`, `r3`) connected in a line
   (`r1 - r2 - r3`) with veth pairs, each link on its own `/30`:

   ```bash
   sudo ip netns add r1
   sudo ip netns add r2
   sudo ip netns add r3

   sudo ip link add r1-r2 type veth peer name r2-r1
   sudo ip link add r2-r3 type veth peer name r3-r2
   sudo ip link set r1-r2 netns r1
   sudo ip link set r2-r1 netns r2
   sudo ip link set r2-r3 netns r2
   sudo ip link set r3-r2 netns r3

   sudo ip netns exec r1 ip addr add 10.0.12.1/30 dev r1-r2
   sudo ip netns exec r2 ip addr add 10.0.12.2/30 dev r2-r1
   sudo ip netns exec r2 ip addr add 10.0.23.1/30 dev r2-r3
   sudo ip netns exec r3 ip addr add 10.0.23.2/30 dev r3-r2

   for ns in r1 r2 r3; do
     sudo ip netns exec $ns ip link set r1-r2 up 2>/dev/null
     sudo ip netns exec $ns ip link set r2-r1 up 2>/dev/null
     sudo ip netns exec $ns ip link set r2-r3 up 2>/dev/null
     sudo ip netns exec $ns ip link set r3-r2 up 2>/dev/null
     sudo ip netns exec $ns ip link set lo up
   done
   ```

2. Give `r1` and `r3` each a simulated loopback "LAN" address to advertise:

   ```bash
   sudo ip netns exec r1 ip addr add 192.168.1.1/32 dev lo
   sudo ip netns exec r3 ip addr add 192.168.3.1/32 dev lo
   ```

3. Start an isolated FRR instance per namespace and configure OSPF on
   each, advertising all connected interfaces into Area 0:

   ```bash
   for r in r1 r2 r3; do
     sudo ip netns exec $r /usr/lib/frr/zebra -d -N $r
     sudo ip netns exec $r /usr/lib/frr/ospfd -d -N $r
   done

   sudo vtysh -N r1 -c "configure terminal" \
     -c "router ospf" -c "network 10.0.12.0/30 area 0" \
     -c "network 192.168.1.1/32 area 0"

   sudo vtysh -N r2 -c "configure terminal" \
     -c "router ospf" -c "network 10.0.12.0/30 area 0" \
     -c "network 10.0.23.0/30 area 0"

   sudo vtysh -N r3 -c "configure terminal" \
     -c "router ospf" -c "network 10.0.23.0/30 area 0" \
     -c "network 192.168.3.1/32 area 0"
   ```

4. Confirm OSPF neighbor adjacencies form and routes are learned
   dynamically end to end:

   ```bash
   sudo vtysh -N r2 -c "show ip ospf neighbor"
   sudo vtysh -N r1 -c "show ip route ospf"
   sudo ip netns exec r1 ping -c 3 192.168.3.1
   ```

   **Expected result:** `show ip ospf neighbor` on `r2` lists both `r1` and
   `r3` in state `Full`; `show ip route ospf` on `r1` shows
   `192.168.3.1/32` learned via `r2`; the ping from `r1` to `r3`'s
   loopback succeeds with 0% packet loss, confirming end-to-end dynamic
   routing across a router `r1` never has a direct link to.

**Negative Test**

Simulate a link failure between `r1` and `r2` (the only path to `r3`) and
confirm OSPF withdraws the route and reachability fails cleanly rather than
silently:

```bash
sudo ip netns exec r1 ip link set r1-r2 down
sleep 5
sudo vtysh -N r1 -c "show ip route ospf"
sudo ip netns exec r1 ping -c 3 -W 1 192.168.3.1
```

**Expected result:** `show ip route ospf` on `r1` no longer lists
`192.168.3.1/32`; the subsequent ping fails immediately with
"Network is unreachable" rather than timing out, confirming OSPF correctly
withdrew the now-unreachable route instead of leaving a stale forwarding
entry.

**Cleanup**

```bash
for r in r1 r2 r3; do
  sudo pkill -f "N $r" 2>/dev/null
  sudo ip netns del $r
done
```

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter covered how a router selects and installs routes (longest
prefix match, administrative distance, metric), static and floating static
routing, the three dynamic routing protocol families with OSPF and BGP as
the representative enterprise protocols, and the redistribution boundaries
that connect them. The hands-on lab used FRRouting to build a genuine
multi-router OSPF topology, confirmed dynamic route learning, and validated
correct route withdrawal after a simulated link failure.

**Completion Checklist**

- [ ] Can explain longest-prefix match and walk through a forwarding
      decision with overlapping routes.
- [ ] Can explain the difference between administrative distance and
      metric with a worked example.
- [ ] Can describe when static routing is preferable to dynamic routing
      and vice versa.
- [ ] Can explain OSPF area hierarchy and why Area 0 is mandatory.
- [ ] Can describe BGP's role at the enterprise edge and the difference
      between eBGP and iBGP.
- [ ] Built a working multi-router OSPF lab and confirmed convergence
      after a simulated failure.
- [ ] Can name at least two routing protocol security controls
      (authentication, prefix filtering, prefix limits).
