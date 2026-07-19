# Chapter 7: Enterprise Network Design and Resilience

![Lab topology for this chapter: ns-r1 (10.60.0.2/24, priority 150) and ns-r2 (10.60.0.3/24, priority 100) both run keepalived for VRRP group 60, sharing the virtual IP 10.60.0.1/24 over the bridge br-vrrp; ns-r1 wins the election as Master and holds the VIP, while ns-client (10.60.0.100/24) reaches the VIP as its default gateway. As a negative test, keepalived is killed on ns-r1; a continuous ping shows one to three missed replies (consistent with the 1-second advertisement interval) before the VIP reappears on ns-r2, confirming Backup promotes to Master.](../../../diagrams/volume-02-network-engineering-foundations/chapter-07-vrrp-failover-topology.svg)

*Figure 7-1. Topology used throughout this chapter's Hands-On Lab: two VRRP peers sharing a bridge and a virtual gateway IP, with a measured failover after the Master is killed.*

## Learning Objectives

- Explain the three-tier hierarchical design model (core, distribution,
  access) and when a collapsed-core variant is appropriate.
- Explain spine-leaf (Clos) fabric architecture as introduced conceptually
  in [Chapter 3](03-ethernet-switching-vlans-and-layer-2-resilience.md), and contrast its convergence and scalability properties
  with traditional hierarchical design.
- Configure and explain First-Hop Redundancy Protocols (HSRP, VRRP, GLBP)
  for default-gateway resilience.
- Explain Equal-Cost Multi-Path (ECMP) routing and why it requires a
  routed, loop-free topology rather than Spanning Tree's blocked-path
  model.
- Design a redundant WAN edge using dual-homed connectivity and BGP as an
  edge routing protocol.
- Apply resilience patterns (N+1, active/active, active/standby) to
  network infrastructure design decisions.
- Validate and troubleshoot first-hop redundancy and multi-path forwarding.

## Theory and Architecture

Chapters 3 and 4 established switching and routing as independent
mechanisms; this chapter is about the architectural decisions that combine
them into a resilient enterprise network — decisions about topology shape,
default-gateway redundancy, and path diversity that determine how much of
the network survives any single failure.

### Hierarchical Network Design: Core, Distribution, Access

The traditional enterprise campus design separates the network into three
functional tiers:

| Tier | Role | Typical Characteristics |
| --- | --- | --- |
| Access | Connects end devices (workstations, phones, APs, printers) | High port density, VLAN trunking to distribution, PoE |
| Distribution | Aggregates access-layer uplinks, enforces policy, performs inter-VLAN routing | Layer 3 boundary, route summarization point, redundant uplinks to core |
| Core | High-speed backbone connecting distribution blocks and the WAN/data center edge | Simple, fast forwarding; policy and complexity kept out of the core deliberately |

The core's defining design principle is to keep it *simple*: policy
enforcement, ACLs, and complex features belong at distribution or access,
not the core, because every packet on the network potentially traverses the
core, and complexity there has the largest blast radius.

**Collapsed core** merges the distribution and core tiers into a single
tier — appropriate for smaller sites or campuses where the traffic volume
and redundancy requirements do not justify a dedicated core tier. This
reduces cost and operational complexity at the expense of the clean
separation of concerns the three-tier model provides; it remains a common
and correct choice for branch offices and small campuses.

### Spine-Leaf (Clos) Fabric Architecture

[Chapter 3](03-ethernet-switching-vlans-and-layer-2-resilience.md) introduced spine-leaf fabric conceptually as an alternative to
Spanning Tree-based Layer 2 designs. A spine-leaf (Clos) fabric consists of
two tiers:

```text
        [Spine1]     [Spine2]     [Spine3]     [Spine4]
           |  \      /  |  \      /  |  \      /  |
           |   \    /   |   \    /   |   \    /   |
        [Leaf1]    [Leaf2]    [Leaf3]    [Leaf4]
          |            |            |            |
       Servers      Servers      Servers      Servers
```

Every leaf switch connects to every spine switch, and no leaf connects
directly to another leaf, nor does any spine connect to another spine. This
non-blocking, uniform topology is the data-center-native alternative to the
three-tier campus model, and it differs from hierarchical design in a way
that matters operationally:

| Property | Three-Tier Hierarchical | Spine-Leaf Fabric |
| --- | --- | --- |
| Loop prevention mechanism | Spanning Tree blocks redundant Layer 2 paths | Fully routed (Layer 3 to the access/leaf); no blocked links |
| Path utilization | Blocked links carry zero traffic until a failure | All spine-leaf links forward simultaneously via ECMP |
| Convergence on link/node failure | STP reconvergence (sub-second with RSTP, but still an event) | ECMP simply stops hashing to the failed path; no protocol reconvergence delay for the surviving paths |
| Scalability pattern | Add distribution blocks; core becomes a bottleneck if not re-architected | Add leaf switches for server capacity, add spine switches for fabric bandwidth — independently |
| Typical domain | Campus | Data center |

The practical consequence, referenced from [Chapter 3](03-ethernet-switching-vlans-and-layer-2-resilience.md)'s discussion of
convergence behavior: a spine-leaf fabric does not "converge" around a
failed link in the way STP does, because it never blocked any link to begin
with — every spine-leaf link was already forwarding traffic, and ECMP
simply redistributes flows away from a failed path onto the remaining
active ones.

### First-Hop Redundancy Protocols (FHRP)

Distribution- or access-layer hosts need a single, stable default gateway
address, but the actual routing device behind that address should be
redundant. FHRPs solve this by presenting a shared **virtual IP (VIP)** and
virtual MAC address, backed by two or more physical routers that elect an
active forwarder:

| Protocol | Standard | Election Model | Notes |
| --- | --- | --- | --- |
| VRRP (Virtual Router Redundancy Protocol) | [RFC 5798](https://www.rfc-editor.org/rfc/rfc5798), open standard | Highest-priority router becomes Master; others are Backup | Multi-vendor interoperable |
| HSRP (Hot Standby Router Protocol) | Cisco-proprietary | Highest-priority router becomes Active; others are Standby | Covered in vendor-specific depth in [Volume III](../../volume-03-cisco-enterprise-networking/README.md) |
| GLBP (Gateway Load Balancing Protocol) | Cisco-proprietary | All group members can actively forward simultaneously | Adds load balancing on top of FHRP's basic redundancy model |

This chapter treats VRRP as the primary vendor-neutral example since it is
an open IETF standard implementable across vendors; HSRP and GLBP behave
similarly at a conceptual level (a virtual gateway address shared across
physical routers) but are Cisco-specific implementations covered alongside
Cisco platform configuration in [Volume III](../../volume-03-cisco-enterprise-networking/README.md).

All three protocols share the same basic mechanism: group members exchange
periodic hello messages carrying priority; the highest-priority (or, for
VRRP, highest-priority with the lowest IP as tiebreaker) member owns the
virtual IP and answers ARP requests for it with the shared virtual MAC.
Should the active member fail to send hellos within the hold timer, a
backup member detects the absence and takes over the virtual IP/MAC,
typically within one to three seconds by default (tunable lower).

### Equal-Cost Multi-Path (ECMP) Routing

ECMP allows a router to install and use multiple equal-cost next hops for
the same destination simultaneously, rather than selecting only one and
leaving the others idle. This is what makes spine-leaf fabric's "every link
forwards" property possible: a leaf switch with four equal-cost paths to a
given spine-reachable destination hashes each flow (typically on a
combination of source/destination IP and Layer 4 port) to one of the four
paths, spreading load across all of them while keeping any single flow's
packets on one consistent path to avoid reordering.

```text
Leaf1 routing table entry for 10.10.0.0/24:
  via Spine1  (equal cost)
  via Spine2  (equal cost)
  via Spine3  (equal cost)
  via Spine4  (equal cost)
```

ECMP requires a routed (Layer 3) topology with genuinely equal-cost paths;
it is unrelated to and does not require Spanning Tree, which is precisely
why spine-leaf fabrics are built as routed topologies (often with the
Layer 3 boundary extended down to the access/leaf layer, sometimes paired
with an overlay such as VXLAN to preserve Layer 2 adjacency where
applications require it — overlay design is out of this volume's scope).

### Redundant WAN Edge Design

An enterprise's connection to external networks (internet, or a private
WAN/MPLS provider) is itself a single point of failure if not deliberately
designed otherwise. Common redundancy patterns:

| Pattern | Description |
| --- | --- |
| Dual-homed, single ISP | Two circuits to the same provider; protects against a single circuit/interface failure, not a provider-wide outage |
| Dual-homed, dual ISP | Two circuits to two different providers; protects against a provider-wide outage, at higher cost and complexity |
| BGP-based edge routing | The enterprise runs BGP (introduced in [Chapter 4](04-ip-routing-fundamentals.md)) with its edge routers, advertising and receiving routes from each provider, allowing automatic failover and, with an autonomous system number and provider-independent address space, mobility between providers |
| Static-route edge (no BGP) | Simpler, but failover typically depends on interface/route tracking rather than routing-protocol convergence, and does not support provider-independent addressing |

Enterprises large enough to require provider independence or fine-grained
inbound/outbound path control typically justify running BGP at the edge
despite its operational complexity ([Chapter 4](04-ip-routing-fundamentals.md)); smaller sites commonly
accept static or tracked-route failover as a simpler, adequately resilient
option.

### Resilience Patterns

| Pattern | Description | Trade-off |
| --- | --- | --- |
| Active/Standby | One path or device actively forwards; the redundant unit is idle until failure | Simple to reason about; wastes standby capacity |
| Active/Active | Both units forward traffic simultaneously (e.g., ECMP, GLBP) | Better resource utilization; more complex failure and capacity-planning math |
| N+1 | One spare unit of capacity beyond the minimum required (N) | Tolerates exactly one failure without capacity shortfall |
| 2N | Full duplicate capacity | Tolerates a full-site or full-tier failure; highest cost |

The choice between these patterns is a design decision informed by the
availability requirement of the service being protected, not a default —
covered further in Design Considerations below.

## Design Considerations

- **Choose the topology to match the domain.** Three-tier hierarchical
  design remains the right default for campus/branch networks with
  north-south (client-to-server/internet) traffic patterns; spine-leaf
  fabric fits data center environments with heavy east-west
  (server-to-server) traffic that a hierarchical design's core would
  otherwise bottleneck.
- **Size oversubscription deliberately at every tier boundary.** An
  access-to-distribution oversubscription ratio (for example, 20:1)
  reflects a design assumption about how much simultaneous demand access
  ports will actually generate; verify that assumption against real
  traffic patterns rather than inheriting a default from a previous design.
- **Match the FHRP protocol to the environment.** VRRP is the correct
  choice in genuinely multi-vendor environments; a single-vendor Cisco
  environment may reasonably prefer HSRP or GLBP for tighter platform
  integration ([Volume III](../../volume-03-cisco-enterprise-networking/README.md) covers the trade-offs in vendor-specific depth).
- **Decide active/active vs. active/standby per service, not globally.**
  A stateful firewall pair may require active/standby to keep session
  state simple, while an ECMP-routed core benefits from active/active
  utilization — apply the pattern that fits each component's own
  constraints.
- **Plan physical path diversity, not just logical redundancy.** Two
  circuits that share the same conduit, the same building entrance, or the
  same upstream carrier's shared infrastructure are not truly redundant;
  confirm diverse physical routing for links meant to protect against a
  physical fault, not merely diverse logical configuration.
- **Test convergence, don't assume it.** A design that is redundant on
  paper but has never had a link or device failure deliberately induced in
  a controlled window carries unverified risk; planned failure testing
  ([Chapter 9](09-network-troubleshooting-and-operations.md)) is part of validating a resilience design, not a separate
  concern.

## Implementation and Automation

### VRRP Configuration (Vendor-Neutral Pseudo-CLI)

```text
router1(config)# interface vlan 20
router1(config-if)# ip address 10.1.2.130 255.255.255.192
router1(config-if)# vrrp 20 ip 10.1.2.129
router1(config-if)# vrrp 20 priority 150
router1(config-if)# vrrp 20 authentication text <SHARED_SECRET>

router2(config)# interface vlan 20
router2(config-if)# ip address 10.1.2.131 255.255.255.192
router2(config-if)# vrrp 20 ip 10.1.2.129
router2(config-if)# vrrp 20 priority 100
router2(config-if)# vrrp 20 authentication text <SHARED_SECRET>
```

`router1` becomes VRRP Master (priority 150 beats 100) and answers ARP for
the shared virtual IP `10.1.2.129`, which matches the gateway address
convention established in [Chapter 2](02-ip-addressing-and-subnetting.md)'s addressing-by-function design.

### ECMP Verification (Vendor-Neutral Pseudo-CLI)

```text
leaf1# show ip route 10.10.0.0/24
10.10.0.0/24 [110/20] via 10.99.1.1, Spine1
             [110/20] via 10.99.1.5, Spine2
             [110/20] via 10.99.1.9, Spine3
             [110/20] via 10.99.1.13, Spine4
```

### Automating Redundancy Validation Before Maintenance

```python
# Illustrative pre-maintenance check: confirm both FHRP peers are healthy
# and both ECMP paths are installed before a planned maintenance window,
# using a NETCONF/RESTCONF- or gNMI-capable device library.
import sys

def check_fhrp_pair(peer_a_state, peer_b_state):
    valid_pairs = {("Master", "Backup"), ("Backup", "Master")}
    if (peer_a_state, peer_b_state) not in valid_pairs:
        print(f"FHRP pair unhealthy: {peer_a_state}/{peer_b_state}")
        sys.exit(1)
    print("FHRP pair healthy — safe to proceed with maintenance on one peer.")

check_fhrp_pair("Master", "Backup")
```

```yaml
# Ansible: fail the play if fewer than the expected number of ECMP
# next hops are installed for a critical prefix before proceeding
- name: Verify ECMP path count before maintenance
  hosts: leaf_switches
  tasks:
    - name: Gather routing table for critical prefix
      network.device.command:
        commands: "show ip route 10.10.0.0/24 | json"
      register: route_output

    - name: Assert all four expected next hops are present
      ansible.builtin.assert:
        that:
          - route_output.stdout[0].next_hops | length == 4
        fail_msg: "Expected 4 ECMP paths, found {{ route_output.stdout[0].next_hops | length }} — do not proceed with maintenance."
```

## Validation and Troubleshooting

```bash
# Confirm which FHRP peer currently holds the Master/Active role
router1# show vrrp brief

# Confirm ECMP is actually load-sharing (not silently pinned to one path)
leaf1# show ip cef 10.10.0.0/24 detail

# From an end host, confirm the gateway ARP entry resolves to the
# virtual MAC, not a specific physical router's MAC
ip neigh show 10.1.2.129
```

| Symptom | Likely Cause | Diagnostic |
| --- | --- | --- |
| Both FHRP peers show as Master/Active simultaneously (split-brain) | Hello traffic blocked between peers (ACL, VLAN misconfiguration, STP blocking the peer link) | Verify Layer 2 connectivity and hello reachability between peers |
| Failover takes much longer than expected | Hold timer set too high, or hello timer mismatch between peers | Compare configured timers on both peers |
| Traffic uses only one of several ECMP paths | Hashing algorithm producing poor distribution, or one path not actually equal-cost | Check per-path traffic counters; confirm metrics are truly equal |
| Asymmetric routing after a link failure | ECMP path selection differs between forward and return direction for a stateful flow | Trace both directions; confirm stateful devices (firewalls, NAT from [Chapter 5](05-core-network-services.md)) sit where path symmetry is guaranteed |
| Gateway unreachable after a planned router reload | FHRP priority not preserved correctly, or preemption disabled when expected | Check `vrrp brief` state and preemption configuration on both peers |
| Spine-leaf fabric shows uneven link utilization | Hash polarization or insufficient flow entropy (few large flows) rather than a fault | Compare against expected flow characteristics before treating as a defect |

A useful validation habit before *and* after any change to redundant
infrastructure: confirm the redundant path or peer independently, not just
the primary — a design can appear healthy in normal operation while its
backup path or peer has silently failed, a state that only a deliberate
check (or an actual failure event) reveals.

## Security and Best Practices

- **Authenticate FHRP hello traffic** (VRRP/HSRP authentication) to prevent
  a rogue device from injecting a higher-priority advertisement and hijacking
  the default gateway role — an attack that gives the attacker a
  man-in-the-middle position over every host using that gateway.
- **Apply control-plane policing** on core, distribution, and spine devices
  to protect routing protocol and FHRP control traffic from being starved
  by a traffic flood, which would otherwise degrade convergence exactly
  when it matters most.
- **Test failover in a controlled window, not only in production
  emergencies.** A redundancy design that has never been deliberately
  exercised carries unverified assumptions; schedule periodic failover
  tests as an operational practice (developed further in [Chapter 9](09-network-troubleshooting-and-operations.md)).
- **Maintain physical path diversity for links protecting critical
  services**, and periodically re-verify that diversity — carrier
  mergers, facility changes, and undocumented rerouting can silently
  collapse previously diverse paths onto shared physical infrastructure.
- **Scope BGP edge sessions with explicit prefix filters and maximum-prefix
  limits** (introduced in [Chapter 4](04-ip-routing-fundamentals.md)) on every external session, since a
  redundant WAN edge that accepts unfiltered routes from two providers
  doubles the blast radius of a provider-side routing leak instead of
  halving the risk.

## References and Knowledge Checks

**References**

- [RFC 5798 — Virtual Router Redundancy Protocol (VRRP) Version 3](https://www.rfc-editor.org/rfc/rfc5798)
- [RFC 4786 — Operation of Anycast Services](https://www.rfc-editor.org/rfc/rfc4786)
- [RFC 2992 — Analysis of an Equal-Cost Multi-Path Algorithm](https://www.rfc-editor.org/rfc/rfc2992)
- [RFC 4271 — A Border Gateway Protocol 4 (BGP-4)](https://www.rfc-editor.org/rfc/rfc4271)
- [Charles Clos — "A Study of Non-Blocking Switching Networks," Bell System Technical Journal, 1953 (origin of Clos network topology)](https://ieeexplore.ieee.org/document/6771586)

**Knowledge Checks**

1. Explain why a spine-leaf fabric does not need Spanning Tree even though
   every leaf connects to every spine, creating many physical loops.
2. What specific problem does ECMP solve that a single default route
   cannot, and what does it require of the underlying topology?
3. A VRRP-protected gateway briefly shows both peers as Master at the same
   time. What is this condition called, and what is the most likely root
   cause?
4. Why does the enterprise core deliberately avoid hosting ACLs and
   complex policy, compared to the distribution tier?
5. Contrast active/active and active/standby resilience patterns, and give
   one enterprise example where each is the better choice.
6. Why is a dual-homed connection to a single ISP a weaker redundancy
   design than dual-homing to two separate ISPs, and what does BGP add to
   that design?

## Hands-On Lab

**Objective.** Build a VRRP-protected default gateway across two router
namespaces sharing a Linux bridge, validate normal Master/Backup election
and end-to-end reachability, then induce a controlled failure and measure
failover.

**Prerequisites**

- A Linux host with `sudo` access and `iproute2`.
- `keepalived` installed:

  ```bash
  sudo apt-get update && sudo apt-get install -y keepalived
  ```

**Lab Steps**

1. Create two router namespaces, a client namespace, and a shared bridge
   connecting all three (VRRP requires a shared Layer 2 segment):

   ```bash
   sudo ip netns add ns-r1
   sudo ip netns add ns-r2
   sudo ip netns add ns-client

   sudo ip link add br-vrrp type bridge
   sudo ip link set br-vrrp up

   sudo ip link add veth-r1 type veth peer name veth-r1-br
   sudo ip link add veth-r2 type veth peer name veth-r2-br
   sudo ip link add veth-cl type veth peer name veth-cl-br

   sudo ip link set veth-r1 netns ns-r1
   sudo ip link set veth-r2 netns ns-r2
   sudo ip link set veth-cl netns ns-client

   for p in veth-r1-br veth-r2-br veth-cl-br; do
     sudo ip link set "$p" master br-vrrp
     sudo ip link set "$p" up
   done
   ```

2. Address each namespace on the shared `10.60.0.0/24` segment:

   ```bash
   sudo ip netns exec ns-r1 ip addr add 10.60.0.2/24 dev veth-r1
   sudo ip netns exec ns-r1 ip link set veth-r1 up
   sudo ip netns exec ns-r1 ip link set lo up

   sudo ip netns exec ns-r2 ip addr add 10.60.0.3/24 dev veth-r2
   sudo ip netns exec ns-r2 ip link set veth-r2 up
   sudo ip netns exec ns-r2 ip link set lo up

   sudo ip netns exec ns-client ip addr add 10.60.0.100/24 dev veth-cl
   sudo ip netns exec ns-client ip link set veth-cl up
   sudo ip netns exec ns-client ip route add default via 10.60.0.1
   ```

3. Write `keepalived` configuration for each router, with `ns-r1` as the
   higher-priority (Master) peer:

   ```bash
   cat <<'EOF' | sudo tee /tmp/keepalived-r1.conf
   vrrp_instance VRRP_LAB {
       state MASTER
       interface veth-r1
       virtual_router_id 60
       priority 150
       advert_int 1
       virtual_ipaddress { 10.60.0.1/24 }
   }
   EOF

   cat <<'EOF' | sudo tee /tmp/keepalived-r2.conf
   vrrp_instance VRRP_LAB {
       state BACKUP
       interface veth-r2
       virtual_router_id 60
       priority 100
       advert_int 1
       virtual_ipaddress { 10.60.0.1/24 }
   }
   EOF
   ```

4. Start `keepalived` in each router namespace and confirm election:

   ```bash
   sudo ip netns exec ns-r1 keepalived -f /tmp/keepalived-r1.conf \
     -p /tmp/keepalived-r1.pid -n -D &
   sudo ip netns exec ns-r2 keepalived -f /tmp/keepalived-r2.conf \
     -p /tmp/keepalived-r2.pid -n -D &
   sleep 5

   sudo ip netns exec ns-r1 ip addr show veth-r1 | grep 10.60.0.1
   ```

   **Expected result:** `10.60.0.1/24` appears as a secondary address on
   `ns-r1`'s `veth-r1`, confirming `ns-r1` (priority 150) won the election
   and holds the virtual IP.

5. Confirm the client reaches the virtual gateway and identify which
   physical router is currently answering:

   ```bash
   sudo ip netns exec ns-client ping -c 3 10.60.0.1
   ```

   **Expected result:** 3 packets transmitted, 3 received, 0% loss.

**Negative Test**

Kill `keepalived` on the Master (`ns-r1`) to simulate a router failure, and
measure the failover using a continuous ping:

```bash
sudo ip netns exec ns-client ping -i 0.5 10.60.0.1 > /tmp/vrrp-failover.log 2>&1 &
PING_PID=$!
sleep 3
sudo kill "$(cat /tmp/keepalived-r1.pid)"
sleep 8
sudo kill "$PING_PID"

grep -c "bytes from" /tmp/vrrp-failover.log
sudo ip netns exec ns-r2 ip addr show veth-r2 | grep 10.60.0.1
```

**Expected result:** the ping log shows a short gap (typically one to three
missed replies around the kill event, consistent with `advert_int 1`'s
roughly 3-second default failure-detection window) but resumes
successfully, and `10.60.0.1` now appears on `ns-r2`, confirming the
Backup assumed the Master role — this is the expected, correct behavior of
FHRP failover, quantified rather than just described.

**Cleanup**

```bash
sudo kill "$(cat /tmp/keepalived-r1.pid)" 2>/dev/null || true
sudo kill "$(cat /tmp/keepalived-r2.pid)" 2>/dev/null || true
sudo ip netns del ns-r1 2>/dev/null || true
sudo ip netns del ns-r2 2>/dev/null || true
sudo ip netns del ns-client 2>/dev/null || true
sudo ip link del br-vrrp 2>/dev/null || true
rm -f /tmp/keepalived-r1.* /tmp/keepalived-r2.* /tmp/vrrp-failover.log
```

## Summary and Completion Checklist

This chapter connected the switching ([Chapter 3](03-ethernet-switching-vlans-and-layer-2-resilience.md)) and routing ([Chapter 4](04-ip-routing-fundamentals.md))
building blocks into deliberate, resilient network architectures: the
three-tier hierarchical campus model and its collapsed-core variant,
spine-leaf fabric as the data-center-native alternative referenced from
[Chapter 3](03-ethernet-switching-vlans-and-layer-2-resilience.md), first-hop redundancy protocols for gateway availability, ECMP
for active/active path utilization, and redundant WAN edge design. The
hands-on lab built a working VRRP-protected gateway, measured an actual
failover event with a continuous ping, and confirmed the Backup peer
correctly assumed the Master role — turning "the network is redundant" from
a design claim into an observed, timed result.

**Completion Checklist**

- [ ] Can explain the role of each tier in three-tier hierarchical design
      and when a collapsed core is appropriate.
- [ ] Can contrast spine-leaf fabric with hierarchical design on
      convergence and scalability.
- [ ] Can configure and explain VRRP Master/Backup election.
- [ ] Understands what ECMP requires of the underlying topology and why it
      does not depend on Spanning Tree.
- [ ] Can describe at least two WAN edge redundancy patterns and BGP's role
      in them.
- [ ] Built and validated a working VRRP gateway and measured a real
      failover event.
