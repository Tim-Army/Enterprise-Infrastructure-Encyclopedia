# Chapter 04: PAN-OS Networking, NAT, Routing, and High Availability

![Lab topology for this chapter: Layer 3 interfaces route a default route out the untrust side, and a dynamic-IP-and-port source NAT rule translates outbound sessions, confirmed in the session table. As a negative test, a NAT policy lookup for an inbound destination NAT rule that does not yet exist reports no matching rule, confirming an unpublished internal service is not reachable inbound. Two firewalls in active/passive HA show one active and one passive with both HA links running; disabling the active member's monitored uplink causes the peer to transition to active within the failure-detection interval while the trust-zone test host stays reachable throughout, and restoring the interface returns the original member to a synchronized state.](../../../diagrams/volume-16-palo-alto-networks-security/chapter-04-nat-ha-failover-topology.svg)

*Figure 4-1. Topology used throughout this chapter's Hands-On Lab: Layer 3 interfaces, source NAT, and an active/passive HA pair, tested against an unpublished destination NAT lookup and a failover.*

## Learning Objectives

- Configure Layer 3 interfaces, subinterfaces, and security zones, and
  explain how zone membership — not IP addressing alone — drives PAN-OS
  policy evaluation.
- Build a virtual router with static routes and describe when OSPF or BGP
  is appropriate instead.
- Configure source NAT (dynamic IP and port, dynamic IP, static) and
  destination NAT rules, and explain PAN-OS NAT policy evaluation order.
- Explain the difference between Layer 3, virtual wire, and Layer 2
  deployment modes and when each is appropriate.
- Configure an active/passive high availability (HA) pair, including HA1
  control, HA2 data, and HA3 (if applicable) links, and validate failover.

## Theory and Architecture

[Chapter 03](03-vm-series-deployment-licensing-and-bootstrap.md) got a VM-Series instance reachable and licensed. This chapter
covers the networking constructs that turn a licensed firewall into an
enforcement point sitting between real network segments: interfaces, zones,
routing, NAT, and — because a single firewall is a single point of failure
— high availability.

### Interface deployment modes

PAN-OS interfaces support several modes, and a single firewall can mix
modes across different interfaces:

| Mode | Behavior |
| --- | --- |
| Layer 3 | Interface has an IP address; firewall routes between zones like a router |
| Layer 2 | Interface switches within a VLAN; firewall bridges without IP routing |
| Virtual wire (vWire) | Two interfaces are logically bound transparently; no MAC/IP change, no routing — the firewall is "invisible" on the wire |
| Tap | Passive monitoring off a SPAN/mirror port; visibility only, no enforcement |
| Aggregate Ethernet (AE) | Multiple physical interfaces bonded (802.3ad) for bandwidth and redundancy |
| Loopback | Virtual interface used for management services, dynamic routing router-IDs, and NAT/destination addressing that is not tied to a physical link |
| Tunnel | Logical endpoint for IPsec or GlobalProtect tunnels |

Virtual wire deployment is common for a first-time NGFW insertion into an
existing network — App-ID and Content-ID inspection is added between two
existing devices (for example, a core switch and a router) without
renumbering anything, at the cost of losing NAT and dynamic-routing
participation on that segment. Layer 3 mode is the default assumption for
the rest of this chapter and the majority of the volume, because it is the
mode required for NAT, dynamic routing, and most VPN termination.

### Zones: the actual unit of policy

A PAN-OS security zone is a logical grouping of one or more interfaces
(regardless of mode) that shares a trust level. Security policy rules
([Chapter 05](05-application-identity-threat-and-data-security-policy.md)) are written source-zone-to-destination-zone, not
source-interface-to-destination-interface — this is a deliberate design
choice that lets an administrator add a second interface to an existing
zone without rewriting every policy rule that references that zone.
Intrazone traffic (same zone on both sides) is allowed by an implicit rule
unless explicitly overridden; interzone traffic is denied by an implicit
rule unless a security policy rule explicitly permits it. Every packet's
zone is resolved before any App-ID/Content-ID inspection occurs, because
zone membership determines which policy rules are even eligible to match.

### Virtual routers and routing

A PAN-OS **virtual router (VR)** is an independent routing instance —
distinct from a zone — holding its own routing table, static routes, and
dynamic routing protocol instances (OSPF, OSPFv3, BGP, RIP). A firewall can
run multiple virtual routers to keep routing domains logically separate
(for example, an "Internet-VR" carrying a default route learned via BGP
from an ISP, and an "Internal-VR" carrying OSPF-learned enterprise routes),
with route redistribution or a static route explicitly bridging them where
traffic must cross. Static routes are appropriate for stable, simple
topologies (a branch firewall with one uplink); dynamic routing protocols
are appropriate where the firewall must react automatically to upstream
topology changes — a data-center pair peering with core routers via OSPF or
BGP for automatic failover and ECMP path selection.

### NAT policy and evaluation order

PAN-OS separates **NAT policy** from **security policy** as distinct rule
bases evaluated independently, in this general order for an outbound
session: security zone lookup uses the *pre-NAT* source and *pre-NAT*
destination zone for the initial policy lookup, while the actual security
rule match for the return and subsequent packets in the session considers
the zone the traffic is actually routed to and from — a frequent source of
confusion for engineers arriving from platforms where NAT and firewall
rules are unified into one table.

| NAT type | Direction | Common use |
| --- | --- | --- |
| Source NAT — dynamic IP and port (DIPP) | Outbound | Many internal hosts share one or a small pool of public IPs (PAT) |
| Source NAT — dynamic IP | Outbound | One-to-one mapping from a pool, without port translation |
| Source NAT — static IP | Outbound (or intrazone) | Fixed, predictable public source IP per internal host |
| Destination NAT — static | Inbound | Publish an internal server (for example, a web server) to a public or partner-facing IP |
| Destination NAT — dynamic (with port translation) | Inbound | Load-distribute or port-remap inbound connections |

NAT rules are evaluated top-down, first match wins, exactly like security
policy — rule order matters, and a broad NAT rule placed above a specific
one silently shadows it.

### High availability architecture

A single firewall is a single point of failure for every network segment
it protects. PAN-OS HA pairs two identical (or feature-equivalent)
firewalls together using dedicated HA links:

- **HA1 (control link).** Carries heartbeats, configuration
  synchronization, and state information between the pair. Often
  configured with a backup HA1 link on a separate physical path for
  resilience.
- **HA2 (data link).** Carries session state synchronization (session
  table, NAT translations, IPsec security associations) so the passive (or
  active-active peer) unit has current state and can take over without
  dropping established sessions. HA2 can be configured for full sync or
  can be omitted in configurations that accept session loss on failover, at
  the cost of a much larger outage per failover.
- **HA3 (packet forwarding link, active/active only).** Used in
  active/active deployments to forward packets between peers when a session
  is asymmetrically routed and owned by the other peer.

Two HA modes:

- **Active/passive.** One firewall actively processes traffic; the peer
  remains in a synchronized standby state and takes over automatically on
  a monitored failure. This is the simpler, more predictable mode and the
  default recommendation for most designs.
- **Active/active.** Both firewalls actively process traffic
  simultaneously, requiring session-ownership and HA3 packet-forwarding
  logic to handle asymmetric routing; it increases effective capacity but
  adds meaningful design and troubleshooting complexity, and is reserved
  for topologies that specifically require both units forwarding
  concurrently (for example, certain ECMP or per-flow load-sharing
  designs).

Failover is triggered by **link monitoring** (a defined physical interface
goes down), **path monitoring** (a defined destination IP becomes
unreachable, verified by ping), or loss of HA1 heartbeats interpreted per
the configured failure thresholds.

## Design Considerations

- **vWire for insertion, Layer 3 for everything else.** Choose virtual wire
  when the goal is adding inspection to an existing segment with zero
  renumbering, accepting the loss of NAT and dynamic routing on that
  segment; choose Layer 3 mode as the default for new deployments, hub
  sites, and anywhere NAT or dynamic routing participation is required.
- **Zone granularity.** Too few zones (for example, one large "Internal"
  zone for every internal segment) collapses East-West policy into
  intrazone-allow-by-default traffic with no App-ID/Content-ID enforcement
  between segments that should not implicitly trust each other. Too many
  zones creates policy-rule sprawl. A common, defensible starting point is
  one zone per distinct trust boundary (Untrust/Internet, DMZ, Trust/Internal,
  Guest, Management, and dedicated zones for high-value segments like a
  data center or OT network), refined as the environment's actual
  segmentation requirements become clear.
- **Static vs. dynamic routing.** Prefer static routing for simple,
  single-uplink branch topologies where the operational simplicity and
  predictability outweigh automatic convergence. Prefer OSPF or BGP for
  multi-homed or data-center topologies where manual static-route
  maintenance would not keep pace with upstream topology changes, and where
  automatic sub-second-to-seconds convergence materially reduces outage
  duration.
- **NAT rule ordering and specificity.** Order NAT rules from most specific
  to least specific, exactly as with security policy, and audit rule order
  whenever a new NAT rule is added — a new, broadly scoped rule inserted
  above an existing specific rule is a common cause of "NAT suddenly
  changed behavior for an unrelated host" incidents.
- **Active/passive vs. active/active.** Default to active/passive unless a
  specific, documented capacity or routing requirement justifies
  active/active's added complexity. Active/active troubleshooting requires
  reasoning about session ownership and HA3 forwarding that most
  organizations do not need for typical perimeter or data-center
  deployments.
- **HA link diversity.** Run HA1 and HA2 on physically separate interfaces
  and, where the platform and budget allow, separate physical paths
  (different switches, different fiber runs) from the data interfaces they
  protect — an HA link that shares a failure domain with the traffic it is
  meant to protect against defeats the purpose of the redundant pair.

## Implementation and Automation

### Configuring a Layer 3 interface and zone

```text
admin@pa-fw01# set network interface ethernet1/1 layer3 ip 203.0.113.2/30
admin@pa-fw01# set network interface ethernet1/2 layer3 ip 10.10.20.1/24
admin@pa-fw01# set zone untrust network layer3 ethernet1/1
admin@pa-fw01# set zone trust network layer3 ethernet1/2
admin@pa-fw01# commit
```

### Building a virtual router with a static default route

```text
admin@pa-fw01# set network virtual-router default interface [ ethernet1/1 ethernet1/2 ]
admin@pa-fw01# set network virtual-router default routing-table ip static-route default destination 0.0.0.0/0 nexthop ip-address 203.0.113.1
admin@pa-fw01# set network virtual-router default routing-table ip static-route to-trust destination 10.10.20.0/24 nexthop ip-address 10.10.20.1
admin@pa-fw01# commit
```

### Enabling OSPF on the virtual router (alternative to static)

```text
admin@pa-fw01# set network virtual-router default protocol ospf router-id 10.10.20.1
admin@pa-fw01# set network virtual-router default protocol ospf area 0.0.0.0 interface ethernet1/2 enable yes
admin@pa-fw01# set network virtual-router default protocol ospf enable yes
admin@pa-fw01# commit
```

### Source NAT (dynamic IP and port) for outbound internet access

```text
admin@pa-fw01# set rulebase nat rules Outbound-DIPP from trust to untrust source any destination any
admin@pa-fw01# set rulebase nat rules Outbound-DIPP source-translation dynamic-ip-and-port interface-address interface ethernet1/1
admin@pa-fw01# commit
```

### Destination NAT publishing an internal web server

```text
admin@pa-fw01# set rulebase nat rules Inbound-WebServer from untrust to untrust source any destination 203.0.113.10 destination-translation translated-address 10.10.20.50
admin@pa-fw01# commit
```

A matching security policy rule permitting `untrust` to `trust`,
application `web-browsing`/`ssl`, to the *pre-NAT* destination
(`203.0.113.10`) is still required — NAT translation and security policy
enforcement are independent rule bases, and configuring NAT alone does not
implicitly permit the traffic.

### Configuring active/passive HA

On the first (primary) member:

```text
admin@pa-fw01# set deviceconfig high-availability enabled yes
admin@pa-fw01# set deviceconfig high-availability group-id 10
admin@pa-fw01# set deviceconfig high-availability peer-ip 10.10.10.6
admin@pa-fw01# set deviceconfig high-availability interface ha1 port ethernet1/5
admin@pa-fw01# set deviceconfig high-availability interface ha1 ip-address 10.10.10.5 netmask 255.255.255.252
admin@pa-fw01# set deviceconfig high-availability interface ha2 port ethernet1/6
admin@pa-fw01# set deviceconfig high-availability election-option priority 100
admin@pa-fw01# commit
```

On the second (secondary) member, mirror the configuration with `peer-ip`
pointed back at the first member's HA1 address and a higher (numerically
larger, lower-preference) `priority` value, then commit on both.

### Configuring link and path monitoring

```text
admin@pa-fw01# set deviceconfig high-availability group monitoring link-monitoring link-group uplinks interface ethernet1/1
admin@pa-fw01# set deviceconfig high-availability group monitoring path-monitoring path-group internet-check destination-ip 8.8.8.8 source-ip 203.0.113.2
admin@pa-fw01# commit
```

## Validation and Troubleshooting

- **Routing table verification.** `show routing route` displays the active
  forwarding table per virtual router; confirm the expected static or
  dynamically learned routes are present and that the correct next hop and
  outgoing interface appear before troubleshooting further up the stack.
- **Zone-to-interface mapping errors.** A commit failure referencing a
  security or NAT rule that "references an undefined zone" almost always
  means an interface was reassigned or removed from a zone without
  updating the policy rules that reference it — `show zone` and `show
  interface all` confirm current mapping.
- **NAT translation not occurring.** `show session all filter
  destination <IP>` (or `source <IP>`) reveals whether a session is
  matching the expected NAT rule; `test nat-policy-match` (with source,
  destination, and zone parameters) simulates a lookup without generating
  live traffic and reports which NAT rule would match — invaluable for
  diagnosing an unexpected NAT outcome before changing production rules.
- **Security policy blocking despite correct NAT.** Remember NAT and
  security policy are separate rule bases: `test security-policy-match`
  simulates which security rule a given flow would hit, using *pre-NAT*
  addressing for the initial zone/rule lookup exactly as PAN-OS evaluates
  it live.
- **HA pair stuck in "non-functional" or split-brain-like state.** `show
  high-availability state` reports each member's role (active/passive) and
  state (initial, non-functional, suspended, active, passive) plus the
  specific reason for a non-functional state (for example, mismatched
  PAN-OS versions, mismatched HA group ID, or an HA1 link that cannot reach
  the peer). Version and content mismatches between HA peers are a common
  cause — [Chapter 07](07-firewall-operations-troubleshooting-upgrades-and-automation.md) covers coordinated upgrade procedures that avoid this.
- **Failover did not occur as expected.** `show high-availability
  link-monitoring` and `show high-availability path-monitoring` confirm
  whether the configured monitored interfaces/paths are actually being
  tracked and whether their state matches the physical/logical reality;
  a monitored group with no member interfaces configured silently monitors
  nothing.

## Security and Best Practices

- Apply zone protection profiles (`Network > Zone Protection`) to
  Internet-facing zones to mitigate flood, reconnaissance, and
  packet-based attacks at the zone level, independent of and prior to
  security policy rule evaluation.
- Never place an HA1 or HA2 link on the same physical switch or path as the
  data interfaces it protects without a documented, accepted risk — a
  shared failure domain defeats the purpose of the HA pair.
- Restrict which interfaces can reach the HA1 control link; an attacker
  with access to the HA1 segment can potentially disrupt heartbeat
  communication and force an unwanted failover.
- Use path monitoring in addition to link monitoring for HA pairs behind an
  upstream device (a switch or router) whose failure would not show up as
  a local interface-down event — link monitoring alone cannot detect an
  upstream-only failure.
- Audit NAT and security rule order changes with the same rigor as any
  other production change; a misordered NAT rule can silently expose or
  hide a service without any commit error, since NAT rule conflicts are
  evaluated by precedence, not flagged as errors.
- Log and periodically review destination NAT rules specifically — every
  destination NAT rule represents an inbound exposure decision and should
  have a documented business justification, reviewed on the same cadence
  as firewall rule recertification ([Volume X](../../volume-10-enterprise-cybersecurity/README.md)).

## References and Knowledge Checks

**References**

- [Palo Alto Networks, *PAN-OS Administrator's Guide*](https://docs.paloaltonetworks.com/pan-os/11-0/pan-os-admin) — Networking, NAT, and
  High Availability chapters (version 11.1).
- [Palo Alto Networks, *NAT Configuration Examples* documentation.](https://docs.paloaltonetworks.com/pan-os/10-2/pan-os-networking-admin/nat/nat-configuration-examples)
- [Palo Alto Networks, *High Availability* technical documentation.](https://docs.paloaltonetworks.com/ngfw/administration/high-availability)
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — PAN-OS 11.x
  baseline used throughout this volume.

**Knowledge checks**

1. Why does PAN-OS evaluate security policy using zones rather than raw
   interface or subnet membership, and what operational flexibility does
   this provide?
2. What is the practical difference between HA1 and HA2 links, and what
   happens to established sessions on failover if HA2 is not configured?
3. Which CLI command simulates a NAT rule match without generating live
   traffic, and which command simulates a security policy match?
4. Give one scenario that justifies choosing virtual wire deployment mode
   over Layer 3 mode, and name one capability that is lost by that choice.

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for each sub-topic of the
**Next-Generation Firewall Engineer (PCNSE-successor) Domain 1 "PAN-OS
Networking Configuration"** and the **SD-WAN Engineer** deployment domain —
interfaces, zones, routing, NAT, HA, GlobalProtect, tunnels, and SD-WAN —
mapped in the volume README's coverage table. Each lab is a full PAN-OS CLI
walkthrough (configure, verify, a negative test, cleanup) and ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 4.1–4.9**

- Two lab PAN-OS 11.x firewalls (VM-Series is fine) with two+ data
  interfaces and a dedicated HA link, CLI access as `admin`, and an
  upstream gateway segment. Config-mode commands are shown at the `#`
  prompt, operational commands at the `>` prompt.
- **Cost:** none beyond lab resources; each lab ends by deleting its config
  and committing.

### Lab 4.1 — Configure Layer 3 interfaces and zones (Domain 1: Interfaces)

**Objective:** Bring up an L3 interface pair and bind them to security
zones.

```text
admin@pa-fw01# set network interface ethernet1/1 layer3 ip 203.0.113.2/30
admin@pa-fw01# set network interface ethernet1/2 layer3 ip 10.10.20.1/24
admin@pa-fw01# set zone untrust network layer3 ethernet1/1
admin@pa-fw01# set zone trust network layer3 ethernet1/2
admin@pa-fw01# commit
admin@pa-fw01> show interface ethernet1/1
```

**Expected result:** `show interface` reports `ethernet1/1` up with IP
`203.0.113.2/30` in zone `untrust` — the L3 boundary between zones.

**Negative test:** send traffic between two interfaces in the *same* zone
with intra-zone default set to deny; it is dropped — the zone, not the
interface, is the policy boundary.

**Cleanup:** `delete network interface ethernet1/1 layer3 ip 203.0.113.2/30` (and the zones), then `commit`.

### Lab 4.2 — Configure a virtual router and static routing (Domain 1: Routing)

**Objective:** Add a default static route on the virtual router.

```text
admin@pa-fw01# set network virtual-router default interface [ ethernet1/1 ethernet1/2 ]
admin@pa-fw01# set network virtual-router default routing-table ip static-route default destination 0.0.0.0/0 nexthop ip-address 203.0.113.1
admin@pa-fw01# commit
admin@pa-fw01> show routing route
```

**Expected result:** a `0.0.0.0/0` route via `203.0.113.1` with the correct
egress interface in the routing table.

**Negative test:** remove the interface from the virtual router; the route
disappears and traffic is dropped — an interface must belong to the VR to
route.

**Cleanup:** `delete network virtual-router default routing-table ip static-route default`, then `commit`.

### Lab 4.3 — Configure dynamic routing with BGP (Domain 1: Routing)

**Objective:** Establish a BGP peering on the virtual router.

```text
admin@pa-fw01# set network virtual-router default protocol bgp enable yes
admin@pa-fw01# set network virtual-router default protocol bgp router-id 10.10.20.1
admin@pa-fw01# set network virtual-router default protocol bgp local-as 65010
admin@pa-fw01# set network virtual-router default protocol bgp peer-group PG peer P1 peer-address ip 203.0.113.1 peer-as 65001
admin@pa-fw01# commit
admin@pa-fw01> show routing protocol bgp peer
```

**Expected result:** the BGP peer to AS 65001 reaches `Established` and
learned prefixes appear in `show routing route`.

**Negative test:** set the wrong `peer-as`; the session stays in
`Connect`/`Active` — the AS mismatch BGP will not establish over.

**Cleanup:** `delete network virtual-router default protocol bgp`, then `commit`.

### Lab 4.4 — Configure source and destination NAT (Domain 1: NAT)

**Objective:** Add outbound source NAT (DIPP) and an inbound destination
NAT.

```text
admin@pa-fw01# set rulebase nat rules Outbound-DIPP from trust to untrust source any destination any source-translation dynamic-ip-and-port interface-address interface ethernet1/1
admin@pa-fw01# set rulebase nat rules Inbound-Web from untrust to untrust source any destination 203.0.113.2 service service-https destination-translation translated-address 10.10.20.50
admin@pa-fw01# commit
admin@pa-fw01> show running nat-policy
```

**Expected result:** both NAT rules in the running policy; outbound sessions
share the egress IP, and 443 to `203.0.113.2` translates to `10.10.20.50`.

**Negative test:** set the destination-NAT rule's `to` zone to `trust`
(post-NAT) instead of `untrust` (pre-NAT); it never matches — NAT rules use
the pre-NAT zone.

**Cleanup:** `delete rulebase nat rules Outbound-DIPP` and `Inbound-Web`, then `commit`.

### Lab 4.5 — Configure active/passive HA (Domain 1: HA)

**Objective:** Build an active/passive HA pair and read peer state.

```text
admin@pa-fw01# set deviceconfig high-availability enabled yes
admin@pa-fw01# set deviceconfig high-availability group group-id 1 mode active-passive
admin@pa-fw01# set deviceconfig high-availability group group-id 1 peer-ip 1.1.1.2
admin@pa-fw01# set deviceconfig high-availability interface ha1 ip-address 1.1.1.1 netmask 255.255.255.0
admin@pa-fw01# commit
admin@pa-fw01> show high-availability state
```

**Expected result:** the local device `active`, peer `passive`, and HA links
`up` — a synchronized pair.

**Negative test:** mismatch the PAN-OS version between members; HA state
shows `non-functional` — version parity is required for A/P HA.

**Cleanup:** `set deviceconfig high-availability enabled no`, then `commit`.

### Lab 4.6 — Configure HA link and path monitoring (Domain 1: HA)

**Objective:** Add path monitoring so an upstream failure triggers failover.

```text
admin@pa-fw01# set deviceconfig high-availability group group-id 1 monitoring path-monitoring enabled yes
admin@pa-fw01# set deviceconfig high-availability group group-id 1 monitoring path-monitoring path-group virtual-router default virtual-router-name default destination-ip-group DG1 destination-ip 203.0.113.1
admin@pa-fw01# commit
admin@pa-fw01> show high-availability path-monitoring
```

**Expected result:** the monitored path to `203.0.113.1` shows `up`; if it
fails, the group's failover condition triggers.

**Negative test:** monitor an unreachable IP; the path shows `down` and
forces a failover even though the firewall itself is healthy — tune the
monitored target carefully.

**Cleanup:** disable path-monitoring, then `commit`.

### Lab 4.7 — Configure GlobalProtect portal and gateway (Domain 1: GlobalProtect)

**Objective:** Stand up a GlobalProtect gateway and portal for remote
access.

```text
admin@pa-fw01# set network interface tunnel units tunnel.1
admin@pa-fw01# set global-protect global-protect-gateway GP-GW local-address interface ethernet1/1 tunnel-interface tunnel.1
admin@pa-fw01# set global-protect global-protect-portal GP-Portal portal-config local-address interface ethernet1/1
admin@pa-fw01# commit
admin@pa-fw01> show global-protect-gateway current-user
```

**Expected result:** the gateway and portal are configured; a connected
client appears in `current-user` with an assigned tunnel IP.

**Negative test:** configure the gateway without a client/SSL certificate
bound to the portal; clients fail the TLS handshake — GlobalProtect requires
a valid certificate.

**Cleanup:** delete the GlobalProtect gateway, portal, and `tunnel.1`, then `commit`.

### Lab 4.8 — Configure an IPSec site-to-site tunnel (Domain 1: Tunnels)

**Objective:** Build an IPSec tunnel to a peer and confirm the SA.

```text
admin@pa-fw01# set network interface tunnel units tunnel.2
admin@pa-fw01# set network ike gateway IKE-GW protocol ikev2 dpd enable yes peer-address ip 198.51.100.1 local-address interface ethernet1/1
admin@pa-fw01# set network tunnel ipsec IPSEC-Tunnel tunnel-interface tunnel.2 auto-key ike-gateway IKE-GW
admin@pa-fw01# commit
admin@pa-fw01> show vpn ipsec-sa
```

**Expected result:** an IPSec SA to `198.51.100.1` in `active` state and the
tunnel interface up.

**Negative test:** mismatch the IKE pre-shared key or proposal; Phase 1 fails
and `show vpn ike-sa` shows no established gateway — the crypto must match
both ends.

**Cleanup:** delete the IPSec tunnel, IKE gateway, and `tunnel.2`, then `commit`.

### Lab 4.9 — Configure PAN-OS SD-WAN (SD-WAN Engineer: Deployment)

**Objective:** Enable SD-WAN and read link path health.

```text
admin@pa-fw01# set network sdwan enable yes
admin@pa-fw01# set network sdwan interface-profile ISP1 link-tag internet eligible yes
admin@pa-fw01# set network interface ethernet1/1 sdwan-link-settings enable yes sdwan-interface-profile ISP1
admin@pa-fw01# commit
admin@pa-fw01> show sdwan connection all
```

**Expected result:** the SD-WAN link's path quality (latency, jitter, loss)
reported — application traffic can now be steered by a path-quality policy.

**Negative test:** an SD-WAN policy that references a link tag no interface
carries has no eligible path; traffic falls back to the default route,
bypassing SD-WAN steering.

**Cleanup:** `set network sdwan enable no`, then `commit`.

### Lab 4.10 — Interfaces, routing, NAT, and A/P HA failover (integrative)

**Objective:** Configure Layer 3 interfaces, zones, a static default route,
a source NAT rule for outbound access, and validate an active/passive HA
pair with a deliberate failover test.

**Prerequisites**

- Two lab PAN-OS firewalls (physical, VM-Series, or a lab virtualization
  environment) with at least two data interfaces and one dedicated HA
  interface each, cabled or virtually networked so both members can reach
  each other on the HA1 link.
- Completion of Chapters 01–03 (CLI fluency, licensing, and a bootstrapped
  or manually configured instance).
- A lab internet or upstream gateway segment (can be simulated with a lab
  router or another firewall) for the outbound NAT test.

**Steps**

1. On the primary firewall, configure interfaces and zones:

   ```text
   admin@pa-fw01# set network interface ethernet1/1 layer3 ip 203.0.113.2/30
   admin@pa-fw01# set network interface ethernet1/2 layer3 ip 10.10.20.1/24
   admin@pa-fw01# set zone untrust network layer3 ethernet1/1
   admin@pa-fw01# set zone trust network layer3 ethernet1/2
   admin@pa-fw01# commit
   ```

2. Add the default route and verify the routing table:

   ```text
   admin@pa-fw01# set network virtual-router default interface [ ethernet1/1 ethernet1/2 ]
   admin@pa-fw01# set network virtual-router default routing-table ip static-route default destination 0.0.0.0/0 nexthop ip-address 203.0.113.1
   admin@pa-fw01# commit
   admin@pa-fw01> show routing route
   ```

   **Expected result:** A `0.0.0.0/0` route via `203.0.113.1` appears with
   the correct outgoing interface.

3. Add a source NAT rule for outbound traffic:

   ```text
   admin@pa-fw01# set rulebase nat rules Outbound-DIPP from trust to untrust source any destination any
   admin@pa-fw01# set rulebase nat rules Outbound-DIPP source-translation dynamic-ip-and-port interface-address interface ethernet1/1
   admin@pa-fw01# commit
   ```

4. Add a minimal security policy rule permitting trust-to-untrust web
   traffic (full policy syntax is covered in [Chapter 05](05-application-identity-threat-and-data-security-policy.md)):

   ```text
   admin@pa-fw01# set rulebase security rules Allow-Outbound-Web from trust to untrust source any destination any application [ web-browsing ssl ] action allow
   admin@pa-fw01# commit
   ```

5. From a trust-zone test host, generate traffic and confirm NAT
   translation:

   ```text
   admin@pa-fw01> show session all filter source 10.10.20.0/24
   ```

   **Expected result:** Active sessions show the translated source address
   matching `ethernet1/1`'s IP.

6. **Negative test:** Simulate a NAT lookup for a destination NAT rule that
   does not yet exist:

   ```text
   admin@pa-fw01> test nat-policy-match from untrust to untrust destination 203.0.113.10 protocol 6 destination-port 443
   ```

   **Expected result:** PAN-OS reports no matching NAT rule, confirming
   that an unpublished internal service is not reachable inbound —
   validate this before publishing any destination NAT rule so exposure is
   intentional.

7. On both firewalls, configure active/passive HA per the Implementation
   and Automation section, with distinct `priority` values (lower number =
   higher preference).

8. Verify HA state on both members:

   ```text
   admin@pa-fw01> show high-availability state
   ```

   **Expected result:** One member reports `active`, the other `passive`,
   with `Running` displayed for HA1/HA2 link status on both.

9. **Failover test:** On the active member, administratively disable the
   monitored uplink interface (or shut down the member itself if this is a
   disposable lab):

   ```text
   admin@pa-fw01# set network interface ethernet1/1 link-state down
   admin@pa-fw01# commit
   ```

   **Expected result:** Within the configured failure-detection interval,
   `show high-availability state` on the peer reports it transitioning to
   `active`. Confirm continued reachability of the trust-zone test host
   through the now-active peer.

10. Restore the interface and confirm the original member returns to a
    synchronized state (`passive` if preemption is disabled, or `active`
    again if preemption is enabled):

    ```text
    admin@pa-fw01# set network interface ethernet1/1 link-state auto
    admin@pa-fw01# commit
    ```

11. **Cleanup:** If this lab pair will be reused in later chapters, leave
    the HA and NAT configuration in place; otherwise remove the lab-only
    NAT and security rules and disable HA:

    ```text
    admin@pa-fw01# delete rulebase nat rules Outbound-DIPP
    admin@pa-fw01# delete rulebase security rules Allow-Outbound-Web
    admin@pa-fw01# delete deviceconfig high-availability enabled
    admin@pa-fw01# commit
    ```

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Interfaces, zones, virtual routers, and NAT are the constructs that place a
PAN-OS firewall meaningfully inside a real network topology, and high
availability is what keeps that placement from being a single point of
failure. Zone-based policy evaluation, the separation of NAT policy from
security policy, and the HA1/HA2 (and HA3, for active/active) link model
are foundational patterns that recur throughout the rest of this volume —
[Chapter 05](05-application-identity-threat-and-data-security-policy.md) builds security policy on top of the zones configured here, and
[Chapter 07](07-firewall-operations-troubleshooting-upgrades-and-automation.md) revisits HA-aware upgrade procedures.

- [ ] Can configure Layer 3 interfaces and zones and explain zone-based
      policy evaluation.
- [ ] Can build a virtual router with static routes and explain when
      dynamic routing is preferable.
- [ ] Can configure source and destination NAT rules and explain PAN-OS
      NAT policy evaluation order.
- [ ] Can configure and validate an active/passive HA pair, including a
      controlled failover test.
- [ ] Completed the hands-on lab, including the negative test and cleanup.
