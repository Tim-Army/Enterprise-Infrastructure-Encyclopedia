# Chapter 05: Interfaces, Routing, NAT, Virtual Domains, and High Availability

## Learning Objectives

- Configure physical interfaces, VLAN sub-interfaces, and static/policy
  routes on FortiGate.
- Explain source NAT, destination NAT (VIP), and the difference between
  policy-based NAT and central NAT.
- Enable multi-VDOM mode, create VDOMs, and connect them with an
  inter-VDOM link.
- Configure a two-member FGCP high-availability cluster and validate
  session synchronization.
- Diagnose routing, NAT, and HA issues using FortiOS diagnostic commands.

## Theory and Architecture

### Interface types

FortiOS interfaces fall into several categories that a single deployment
typically combines:

| Type | Description |
| --- | --- |
| Physical interface | A hardware or virtual NIC (`port1`, `port2`, ...) |
| VLAN sub-interface | An 802.1Q-tagged logical interface bound to a physical parent |
| Aggregate (LACP) | Multiple physical interfaces bonded via 802.3ad for bandwidth and link redundancy |
| Software switch | Multiple physical interfaces bridged into a single logical Layer 2 segment, common on smaller appliance models |
| Loopback | A virtual, always-up interface commonly used as a stable router ID or BGP/VPN endpoint |
| Zone | A named grouping of interfaces referenced together in firewall policy, simplifying policy authoring when several interfaces share a security posture |

### Routing

FortiGate supports static routing, policy-based routing, and dynamic
routing protocols (OSPF, BGP, RIP, and IS-IS depending on model and
license). Static and policy routes are the NSE 4 foundation this chapter
covers in depth; dynamic routing protocol configuration follows the same
`config router <protocol>` pattern and is introduced here conceptually.

- **Static routes** (`config router static`) match by destination
  subnet and select an egress interface/gateway, with an administrative
  distance used to arbitrate between multiple matching routes.
- **Policy routes** (`config router policy`) match on richer
  criteria — source address, incoming interface, protocol, and port — and
  override the destination-based routing table lookup for matching
  traffic, which is the mechanism SD-WAN (Chapter 08) builds on for
  application-aware path selection.
- **Equal-cost multi-path (ECMP)** allows multiple static routes of equal
  distance and priority to the same destination to load-share, a
  precursor concept to SD-WAN's more application-aware load distribution.

### NAT models

FortiGate implements NAT at the firewall policy level, with two distinct
architectural approaches:

- **Policy-based NAT** (the traditional and most commonly taught model)
  enables NAT directly on a firewall policy (`set nat enable`), optionally
  drawing from a defined **IP pool** (`config firewall ippool`) for
  source address translation instead of always using the egress
  interface's own IP.
- **Central NAT** (`config firewall central-snat-map` alongside
  `set central-nat enable` under `config system settings`) separates NAT
  rule definition from firewall policy definition entirely, evaluating a
  dedicated central SNAT table independent of which policy matched the
  traffic. Central NAT scales better for large policy sets with complex,
  differentiated NAT requirements but adds a layer of indirection; most
  new, moderately sized deployments use policy-based NAT for its more
  direct one-to-one mapping between a policy and its NAT behavior.

**Destination NAT** on FortiGate is implemented through **Virtual IPs
(VIPs)** (`config firewall vip`), which map an external IP (and
optionally port) to an internal address, referenced as the destination
address in an inbound firewall policy rather than as a separate NAT
construct.

### Virtual Domains (VDOMs)

A VDOM partitions a single physical or virtual FortiGate into multiple
logically independent virtual firewalls, each with its own routing table,
firewall policies, and (optionally) administrative scope. A device starts
in **single-VDOM mode** with an implicit `root` VDOM; enabling
**multi-VDOM mode** exposes the ability to create additional VDOMs and
introduces a `global` configuration scope for settings that apply across
every VDOM (interface hardware assignment, HA configuration, and system-
wide settings) versus per-VDOM scope for everything else (policies,
routing, security profiles).

VDOMs communicate with each other only through an explicit
**inter-VDOM link** (a pair of virtual interfaces, one assigned to each
VDOM, functioning like a point-to-point cable between two logically
separate firewalls) or through physical/VLAN interfaces reassigned between
VDOMs — VDOMs do not implicitly trust or route to each other. This is a
deliberate isolation boundary, commonly used to separate a managed
service provider's customers, or to separate a large enterprise's
business units or compliance-scoped network segments (for example, a
cardholder-data VDOM isolated from the general corporate VDOM) on a single
physical appliance.

### FGCP high availability

**FortiGate Clustering Protocol (FGCP)** is FortiGate's native
high-availability mechanism, clustering two (or more, in limited
configurations) identically licensed and configured devices:

- **Active-passive (A-P)** mode runs one device actively forwarding
  traffic while the other remains in synchronized standby, taking over on
  failure.
- **Active-active (A-A)** mode load-shares session processing across
  cluster members for additional throughput, at the cost of added
  complexity and is less commonly deployed than A-P in enterprise
  branch/edge designs.
- **Heartbeat interfaces** (`hbdev`) — typically two dedicated interfaces
  for redundancy — continuously exchange cluster health and
  synchronization traffic between members; loss of all heartbeat links
  without a corresponding loss of data-plane connectivity is the classic
  cause of a **split-brain** condition, where both members believe they
  should be primary.
- **Virtual MAC address** — the cluster presents a single virtual MAC/IP
  identity on each data interface regardless of which physical member is
  currently primary, so failover does not require the upstream/downstream
  network to relearn a new MAC-to-IP mapping.
- **Configuration and session synchronization** — FGCP synchronizes
  configuration automatically across cluster members (a change on the
  primary propagates to the secondary) and synchronizes active session
  state, so most in-progress sessions survive a failover rather than
  needing to re-establish.

## Design Considerations

- **VDOM licensing and model limits.** VDOM count is licensed per device
  (a base allocation, expandable by license on supported models); confirm
  the target platform's VDOM capacity before designing an architecture
  that assumes a specific VDOM count.
- **Inter-VDOM routing design.** Decide deliberately which VDOMs are
  permitted to reach each other and through which link, rather than
  connecting every VDOM to every other VDOM by default — VDOM isolation
  only provides its intended security boundary if inter-VDOM links are
  applied narrowly and reviewed like any other trust boundary.
- **NAT design: pool sizing and PAT vs. one-to-one.** Port address
  translation (PAT, "overload") lets many internal hosts share one public
  IP using distinct source ports, appropriate for general outbound
  internet access; a dedicated one-to-one NAT mapping is appropriate where
  a specific internal host needs a consistent, individually identifiable
  external address (partner-facing services, some VPN scenarios). Undersized
  PAT pools under high concurrent connection counts can exhaust available
  source ports; monitor and size pools against realistic peak
  concurrent-session counts.
- **HA heartbeat interface redundancy and isolation.** Dedicate physical
  interfaces to `hbdev` that do not also carry data-plane traffic, and use
  two heartbeat links on separate physical paths where possible — a single
  shared heartbeat/data interface risks both a split-brain scenario and
  heartbeat traffic contending with production traffic.
- **HA upgrade strategy.** FGCP supports an uninterruptible upgrade
  process that upgrades the secondary member first, fails over, then
  upgrades the former primary — reducing planned-maintenance downtime to
  a single controlled failover rather than a full outage; plan firmware
  upgrade windows around this workflow rather than upgrading both members
  simultaneously.

## Implementation and Automation

### Physical and VLAN sub-interfaces

```text
FGT-LAB-01 # config system interface
FGT-LAB-01 (interface) # edit "port1"
FGT-LAB-01 (port1) # set alias "wan1"
FGT-LAB-01 (port1) # set ip 203.0.113.10 255.255.255.0
FGT-LAB-01 (port1) # set allowaccess ping
FGT-LAB-01 (port1) # next
FGT-LAB-01 (interface) # edit "port3"
FGT-LAB-01 (port3) # set alias "dmz"
FGT-LAB-01 (port3) # set ip 10.10.20.1 255.255.255.0
FGT-LAB-01 (port3) # next
FGT-LAB-01 (interface) # edit "port2.20"
FGT-LAB-01 (port2.20) # set interface "port2"
FGT-LAB-01 (port2.20) # set vlanid 20
FGT-LAB-01 (port2.20) # set ip 10.10.30.1 255.255.255.0
FGT-LAB-01 (port2.20) # next
FGT-LAB-01 (interface) # end
```

### Static and policy routes

```text
FGT-LAB-01 # config router static
FGT-LAB-01 (static) # edit 1
FGT-LAB-01 (1) # set dst 0.0.0.0 0.0.0.0
FGT-LAB-01 (1) # set gateway 203.0.113.1
FGT-LAB-01 (1) # set device "port1"
FGT-LAB-01 (1) # next
FGT-LAB-01 (static) # end
FGT-LAB-01 # config router policy
FGT-LAB-01 (policy) # edit 1
FGT-LAB-01 (1) # set srcaddr "DMZ-SUBNET"
FGT-LAB-01 (1) # set dstaddr "all"
FGT-LAB-01 (1) # set output-device "port1"
FGT-LAB-01 (1) # set gateway 203.0.113.1
FGT-LAB-01 (1) # next
FGT-LAB-01 (policy) # end
```

### Address objects, IP pool, and policy-based source NAT

```text
FGT-LAB-01 # config firewall address
FGT-LAB-01 (address) # edit "LAN-SUBNET"
FGT-LAB-01 (LAN-SUBNET) # set subnet 10.10.10.0 255.255.255.0
FGT-LAB-01 (LAN-SUBNET) # next
FGT-LAB-01 (address) # edit "DMZ-SUBNET"
FGT-LAB-01 (DMZ-SUBNET) # set subnet 10.10.20.0 255.255.255.0
FGT-LAB-01 (DMZ-SUBNET) # next
FGT-LAB-01 (address) # end
FGT-LAB-01 # config firewall ippool
FGT-LAB-01 (ippool) # edit "WAN1-POOL"
FGT-LAB-01 (WAN1-POOL) # set type overload
FGT-LAB-01 (WAN1-POOL) # set startip 203.0.113.30
FGT-LAB-01 (WAN1-POOL) # set endip 203.0.113.35
FGT-LAB-01 (WAN1-POOL) # next
FGT-LAB-01 (ippool) # end
```

The firewall policy referencing `set nat enable`, `set ippool enable`, and
`set poolname "WAN1-POOL"` is created in Chapter 06 once firewall policy
concepts are covered in full; this chapter establishes the routing, address,
and pool objects that policy will consume.

### Destination NAT with a Virtual IP

```text
FGT-LAB-01 # config firewall vip
FGT-LAB-01 (vip) # edit "DMZ-WEB-VIP"
FGT-LAB-01 (DMZ-WEB-VIP) # set extip 203.0.113.20
FGT-LAB-01 (DMZ-WEB-VIP) # set extintf "port1"
FGT-LAB-01 (DMZ-WEB-VIP) # set mappedip "10.10.20.50"
FGT-LAB-01 (DMZ-WEB-VIP) # set portforward enable
FGT-LAB-01 (DMZ-WEB-VIP) # set protocol tcp
FGT-LAB-01 (DMZ-WEB-VIP) # set extport 443
FGT-LAB-01 (DMZ-WEB-VIP) # set mappedport 443
FGT-LAB-01 (DMZ-WEB-VIP) # next
FGT-LAB-01 (vip) # end
```

### Enabling multi-VDOM mode and creating VDOMs

```text
FGT-LAB-01 # config system global
FGT-LAB-01 (global) # set vdom-admin enable
FGT-LAB-01 (global) # end
FGT-LAB-01 # config vdom
FGT-LAB-01 (vdom) # edit "VDOM-CORP"
FGT-LAB-01 (VDOM-CORP) # next
FGT-LAB-01 (vdom) # edit "VDOM-DMZ"
FGT-LAB-01 (VDOM-DMZ) # next
FGT-LAB-01 (vdom) # end
```

### Creating an inter-VDOM link and assigning interfaces

```text
FGT-LAB-01 # config global
FGT-LAB-01 # config system vdom-link
FGT-LAB-01 (vdom-link) # edit "vlink-corp-dmz"
FGT-LAB-01 (vlink-corp-dmz) # next
FGT-LAB-01 (vdom-link) # end
FGT-LAB-01 # config system interface
FGT-LAB-01 (interface) # edit "vlink-corp-dmz0"
FGT-LAB-01 (vlink-corp-dmz0) # set vdom "VDOM-CORP"
FGT-LAB-01 (vlink-corp-dmz0) # set ip 169.254.1.1 255.255.255.252
FGT-LAB-01 (vlink-corp-dmz0) # next
FGT-LAB-01 (interface) # edit "vlink-corp-dmz1"
FGT-LAB-01 (vlink-corp-dmz1) # set vdom "VDOM-DMZ"
FGT-LAB-01 (vlink-corp-dmz1) # set ip 169.254.1.2 255.255.255.252
FGT-LAB-01 (vlink-corp-dmz1) # next
FGT-LAB-01 (interface) # end
FGT-LAB-01 # config system interface
FGT-LAB-01 (interface) # edit "port3"
FGT-LAB-01 (port3) # set vdom "VDOM-DMZ"
FGT-LAB-01 (port3) # next
FGT-LAB-01 (interface) # end
```

Reassigning `port3` moves it (and the DMZ traffic it carries) out of the
`root`/global default scope into `VDOM-DMZ`; `VDOM-CORP` and `VDOM-DMZ`
now communicate only across the `vlink-corp-dmz` pair, each side routable
within its own VDOM's routing table.

### Configuring FGCP high availability

Applied identically on both cluster members (`FGT-LAB-01` and
`FGT-LAB-02`), except for `priority`, which should differ to give a
deterministic primary at initial cluster formation:

```text
FGT-LAB-01 # config system ha
FGT-LAB-01 (ha) # set group-id 10
FGT-LAB-01 (ha) # set group-name "NSE-LAB-HA"
FGT-LAB-01 (ha) # set mode a-p
FGT-LAB-01 (ha) # set password <HA_CLUSTER_PASSWORD>
FGT-LAB-01 (ha) # set hbdev "port4" 50 "port5" 50
FGT-LAB-01 (ha) # set override disable
FGT-LAB-01 (ha) # set priority 200
FGT-LAB-01 (ha) # end
```

On `FGT-LAB-02`, set `priority 100` (lower than `FGT-LAB-01`) with every
other field identical, including `group-id`, `group-name`, and
`password` — mismatched cluster identity or heartbeat configuration is the
most common reason two devices fail to form a cluster.

## Validation and Troubleshooting

- **Route verification.** `get router info routing-table all` shows the
  active routing table, including which route FortiOS selected among
  multiple candidates; `diagnose firewall proute list` shows configured
  policy routes and their match order, which takes precedence over the
  standard routing table for matching traffic.
- **NAT and VIP diagnostics.** `diagnose firewall vip list` confirms
  active VIP mappings; `get system ippool` (or the equivalent
  `diagnose firewall ippool` commands on some releases) confirms IP pool
  allocation state; a VIP that appears configured but does not respond
  externally is very often a missing or misordered firewall policy
  referencing it (covered in Chapter 06) rather than a VIP definition
  fault.
- **VDOM connectivity issues.** Confirm both ends of an inter-VDOM link
  interface are `up` (`get system interface physical`) and that each VDOM
  has a route directing traffic toward the link — an inter-VDOM link with
  no corresponding static route in one VDOM's routing table will pass
  traffic in only one direction.
- **HA cluster fails to form.** `diagnose sys ha status` and
  `diagnose sys ha checksum show` compare configuration checksums between
  members; a checksum mismatch, mismatched `group-id`/`group-name`, or a
  firmware version mismatch between members are the most common causes.
  Confirm heartbeat interfaces are cabled/connected correctly and that no
  switch port between them blocks the heartbeat VLAN.
- **Split-brain suspected.** `diagnose sys ha status` on each member
  independently shows whether each believes itself primary; if both do,
  heartbeat connectivity has been lost while data-plane connectivity
  persisted on both members — restore heartbeat connectivity and expect
  FGCP to resynchronize and re-elect a single primary automatically once
  heartbeat is restored.

## Security and Best Practices

- Treat VDOM boundaries as real security boundaries: apply the same
  policy rigor, logging, and change review to inter-VDOM links as to any
  other network segmentation point, since a permissive inter-VDOM link
  undermines the isolation VDOMs are meant to provide.
- Restrict `allowaccess` on WAN-facing interfaces to nothing (no
  administrative protocols, not even `ping` if the organization's policy
  requires blocking reconnaissance pings) and confirm no VIP inadvertently
  exposes an administrative service to the internet.
- Use a dedicated, isolated management VDOM or `global` administrative
  access pattern for HA and system-wide configuration rather than mixing
  administrative reachability into a VDOM carrying general user traffic.
- Dedicate heartbeat interfaces exclusively to HA traffic, on separate
  physical NICs where hardware allows, and never disable heartbeat
  encryption/authentication on a production cluster.
- Log NAT and VIP-related sessions where compliance or forensic
  requirements demand identifiable source/destination mapping after
  translation — Chapter 07 covers logging configuration within security
  profiles and policy in depth.

## References and Knowledge Checks

**References**

- Fortinet, *FortiOS Administration Guide* — interfaces, routing, NAT,
  VDOMs, and FGCP high availability.
- Fortinet, *FortiOS CLI Reference* — `config system interface`,
  `config router static`, `config router policy`, `config firewall vip`,
  `config vdom`, `config system ha`.
- Fortinet NSE Training Institute, *NSE 4: FortiGate Infrastructure*
  course (routing, VDOM, and HA domains).
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — FortiOS 7.6.x
  baseline used throughout this volume.

**Knowledge checks**

1. What is the architectural difference between policy-based NAT and
   central NAT, and when would an organization prefer central NAT?
2. Why do two VDOMs on the same physical FortiGate not communicate by
   default, and what construct connects them deliberately?
3. Name two common root causes of an FGCP cluster failing to form, and the
   diagnostic command that surfaces a configuration mismatch between
   members.
4. What is a split-brain condition in an FGCP cluster, and which
   architectural control (heartbeat interface redundancy) is designed to
   prevent it?

## Hands-On Lab

**Objective:** Configure interfaces, static and policy routing, a source
NAT IP pool, and a destination NAT VIP; enable multi-VDOM mode and connect
two VDOMs with an inter-VDOM link; then build and validate a two-member
FGCP HA cluster, including a forced-failover negative test.

**Prerequisites**

- FGT-LAB-01 from Chapter 04, licensed and hardened.
- A second FortiGate-VM64 instance, `FGT-LAB-02`, deployed identically to
  FGT-LAB-01 (same FortiOS build) but not yet configured, for the HA
  portion of this lab.
- At least four available virtual/physical interfaces per device: two data
  interfaces already in use (`port1`/`port2` from prior chapters), plus
  `port3` (DMZ), and `port4`/`port5` reserved for HA heartbeat.

**Steps**

1. Configure `port1` (WAN), `port3` (DMZ), and a VLAN sub-interface
   (`port2.20`) as shown in Implementation and Automation.

   **Expected result:** `get system interface physical` shows all
   interfaces `up` with the assigned IP addresses.

2. Create the default static route and a policy route for DMZ-sourced
   traffic, then verify:

   ```text
   FGT-LAB-01 # get router info routing-table all
   FGT-LAB-01 # diagnose firewall proute list
   ```

3. Create the `LAN-SUBNET` and `DMZ-SUBNET` address objects and the
   `WAN1-POOL` IP pool.

4. Create the `DMZ-WEB-VIP` virtual IP mapping `203.0.113.20:443` to
   `10.10.20.50:443`, then confirm it is registered:

   ```text
   FGT-LAB-01 # diagnose firewall vip list
   ```

   **Expected result:** The VIP appears with the correct external and
   mapped addresses; note that external reachability additionally requires
   a firewall policy, completed in Chapter 06.

5. Enable multi-VDOM mode, create `VDOM-CORP` and `VDOM-DMZ`, create the
   `vlink-corp-dmz` inter-VDOM link, and reassign `port3` into
   `VDOM-DMZ`.

   **Expected result:** `config global` then `diagnose sys vd list` (or the
   GUI's VDOM list) shows both VDOMs with their assigned interfaces.

6. From within `VDOM-CORP`, add a static route pointing toward
   `169.254.1.2` (the DMZ-side vlink address) for the `10.10.20.0/24`
   destination, and confirm connectivity across the link:

   ```text
   FGT-LAB-01 # config vdom
   FGT-LAB-01 (vdom) # edit VDOM-CORP
   FGT-LAB-01 (VDOM-CORP) # execute ping 169.254.1.2
   ```

   **Expected result:** Ping succeeds across the inter-VDOM link.

7. On both FGT-LAB-01 and FGT-LAB-02, configure FGCP HA exactly as shown
   in Implementation and Automation (priority 200 on FGT-LAB-01, priority
   100 on FGT-LAB-02), with heartbeat interfaces `port4` and `port5`
   connected between the two devices.

   **Expected result:** Within a few minutes, `diagnose sys ha status` on
   both members shows a formed cluster with FGT-LAB-01 as primary
   (higher priority) and FGT-LAB-02 as secondary.

8. Confirm configuration synchronization by making a trivial, reversible
   change on the primary (for example, adding a comment to the `DMZ-WEB-VIP`
   object) and confirming it appears on the secondary via
   `show firewall vip` issued through the cluster's single management
   session.

9. **Negative test:** Disconnect (or administratively disable) both
   heartbeat interfaces on the secondary member simultaneously, then check
   `diagnose sys ha status` on each member independently.

   **Expected result:** Each member may report itself as primary
   (split-brain) while heartbeat is down; reconnect the heartbeat
   interfaces and confirm the cluster resynchronizes to a single primary
   within a short interval, demonstrating both the failure mode and FGCP's
   automatic recovery once heartbeat is restored.

**Cleanup**

- Leave interfaces, routing, VDOMs, and the HA cluster in place; Chapter 06
  builds firewall policy and VPN configuration on top of this topology. If
  a shared lab environment requires resetting to single-device state,
  disable HA (`config system ha` `set mode standalone` `end`) on both
  members before making further independent changes.

## Summary and Completion Checklist

This chapter built FGT-LAB-01's data-plane foundation: physical and VLAN
interfaces, static and policy routing, NAT via an IP pool and a
destination-NAT VIP, VDOM segmentation connected through an inter-VDOM
link, and a two-member FGCP high-availability cluster validated through a
forced heartbeat-loss negative test. Chapter 06 builds firewall policy,
authentication, and VPN configuration directly on top of this network and
HA foundation.

- [ ] Can configure physical, VLAN, static, and policy routing on
      FortiGate.
- [ ] Can explain the difference between policy-based NAT, central NAT,
      and VIP-based destination NAT.
- [ ] Can enable multi-VDOM mode, create VDOMs, and connect them with an
      inter-VDOM link.
- [ ] Can configure and validate a two-member FGCP HA cluster, including
      diagnosing a split-brain condition.
- [ ] Completed the hands-on lab, including the negative test.
