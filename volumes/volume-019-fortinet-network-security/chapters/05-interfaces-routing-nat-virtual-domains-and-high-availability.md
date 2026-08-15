# Chapter 05: Interfaces, Routing, NAT, Virtual Domains, and High Availability

![Lab topology for this chapter: two firewalls form an FGCP HA cluster with heartbeat interfaces connected between them; within minutes the cluster shows one primary and one secondary, with configuration changes synchronizing automatically. Separately, multi-VDOM mode connects two virtual domains over an inter-VDOM link with confirmed connectivity. As a negative test, both heartbeat interfaces on the secondary are disconnected simultaneously; each member may independently report itself as primary — a split-brain condition — until the heartbeat links are reconnected, at which point the cluster automatically resynchronizes to a single primary.](../../../diagrams/volume-019-fortinet-network-security/chapter-05-fgcp-ha-split-brain-topology.svg)

*Figure 5-1. Topology used throughout this chapter's Hands-On Lab: interfaces, multi-VDOM routing, and a two-member FGCP HA cluster, tested against a dual-heartbeat-link failure.*

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
- Work within the evaluation FortiGate-VM's interface budget by building
  segments on physical ports with hypervisor VLAN tagging instead of
  purge-prone VLAN sub-interfaces.

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
  traffic, which is the mechanism SD-WAN ([Chapter 08](08-sd-wan-operations-central-management-automation-and-troubleshooting.md)) builds on for
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
`set poolname "WAN1-POOL"` is created in [Chapter 06](06-firewall-policy-authentication-vpn-and-zero-trust-access.md) once firewall policy
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
  referencing it (covered in [Chapter 06](06-firewall-policy-authentication-vpn-and-zero-trust-access.md)) rather than a VIP definition
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
  translation — [Chapter 07](07-fortiguard-security-profiles-ssl-inspection-and-threat-prevention.md) covers logging configuration within security
  profiles and policy in depth.

## References and Knowledge Checks

**References**

- [Fortinet, *FortiOS Administration Guide*](https://docs.fortinet.com/product/fortigate/8.0.0) — interfaces, routing, NAT,
  VDOMs, and FGCP high availability.
- [Fortinet, *FortiOS CLI Reference*](https://docs.fortinet.com/document/fortigate/8.0.0/cli-reference/84566/fortios-cli-reference) — `config system interface`,
  `config router static`, `config router policy`, `config firewall vip`,
  `config vdom`, `config system ha`.
- [Fortinet NSE Training Institute, *NSE 4: FortiGate Infrastructure*
  course (routing, VDOM, and HA domains).](https://training.fortinet.com/local/staticpage/view.php?page=nse_4)
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

This chapter carries a topic-level walkthrough lab for **each task under the NSE 4
objectives *Routing* (10–15%) and the network-layer portion of *Deployment and System
Configuration*** — mapped in the volume README's coverage tables. Every command is a
real FortiOS 7.6 CLI action; each lab ends **`**Lab verified by:** *pending*`** until a
human runs it.

**Shared prerequisites for Labs 5.1–5.8** — a FortiGate on FortiOS 7.6 with at least
two data interfaces, a client host, and (for HA) a second identical FortiGate.
**Cost:** none beyond the appliances/VMs.

### Lab 5.1 — Interfaces, zones, and VLANs (Topic: Layer-2/3 interfaces)

**Eval FortiGate — capable.** Runs on the eval — but mind the free eval's **3-interface budget** (Chapter 04): carry several segments as VLAN subinterfaces of one trunk rather than separate physical ports.

**Objective:** Create a VLAN sub-interface and group interfaces into a zone.

```text
config system interface
    edit vlan100
        set vdom root
        set interface port2
        set vlanid 100
        set ip 10.100.0.1 255.255.255.0
        set allowaccess ping
    next
end
config system zone
    edit trust
        set interface port2 vlan100
    next
end
```

**Expected result:** `vlan100` appears tagged on `port2`, and the `trust` zone groups
the members so one policy can reference the zone — VLANs segment L2 domains and zones
simplify policy across many interfaces.

**Negative test:** reference `port2` directly in a policy after adding it to a zone;
FortiOS rejects it — a zoned interface is addressed only through its zone.

**Variant — hypervisor-tagged access ports (when VLAN sub-interfaces will not fit).** On a
FortiGate-VM under the evaluation license, the 3-interface budget (see the licensing gotchas
in [Chapter 04](04-fortigate-first-deployment-licensing-management-and-hardening.md)) cannot
hold a trunk parent plus two VLAN sub-interfaces alongside the management port. The same
routed topology fits if the **hypervisor applies the tags** instead: give the VM one vNIC per
segment as an access port (Proxmox: `qm set <vmid> --net1 virtio,bridge=vmbr2,tag=200` and
`--net2 ...,tag=202`), reboot so FortiOS enumerates the new port, and address the physical
interfaces directly — zero `vlanid` anywhere in FortiOS:

```text
config system interface
    edit port2
        set mode static
        set ip 10.200.0.1 255.255.255.0
        set allowaccess ping
        set role lan
    next
    edit port3
        set mode static
        set ip 10.202.0.1 255.255.255.0
        set allowaccess ping
        set role lan
    next
end
```

Do not skip `set role lan`: an interface without a role trips the **Security Rating** insight
"Interfaces that do not have a role assigned to them" as a standing orange banner in the GUI,
and the role also drives sensible GUI defaults for the interface. Firewall policies then
reference `port2`/`port3` exactly as they would `vlan200`/`vlan202`. The trade-off is visibility: the FortiGate no longer sees or enforces
tags, so a misconfigured hypervisor bridge (wrong `tag=`) silently moves a segment — the
switch/hypervisor layer becomes part of your security boundary. A successful cross-segment
ping shows `ttl=63`: the decrement from 64 is the proof the traffic was *routed* through the
firewall rather than switched around it.

**Rollback:**

```text
config system zone
    delete trust
end
config system interface
    delete vlan100
end
```

**Lessons from a live eval run.** Two behaviors surface immediately on a free evaluation
FortiGate-VM and shape every lab in this chapter:

- *The eval caps interfaces, policies, and routes at three entries each.* Creating a fourth
  entry in any of those tables fails with
  `Command fail. Return code -4 (reached the maximum number of entries)`. Plan around it:
  carry several segments as VLAN subinterfaces of one trunk rather than separate physical
  ports (this lab), delete-as-you-go once you exceed the route budget (Lab 5.2), and enable
  NAT on an existing policy rather than adding a fourth (Lab 5.3). A licensed FortiGate lifts
  the caps; registering the `FGVMEV` serial does not.
- *`show` hides defaults; `get` shows them.* `show` prints only settings that differ from
  their default, so `show <path> | grep <keyword>` returning nothing usually means the
  setting is at its default — not that it is unset. Confirm with `get`, which prints the full
  effective configuration. For example `show system settings | grep ecmp` is empty on a
  default box, while `get system settings | grep ecmp` reports `v4-ecmp-mode: source-ip-based`.

### Lab 5.2 — Static routing and route selection (Topic: Static routes)

**Eval FortiGate — capable.** Runs on the free/licensed evaluation FortiGate-VM as-is.

**Objective:** Add a static route and read how FortiOS chooses it.

```text
config router static
    edit 10
        set dst 192.168.50.0 255.255.255.0
        set gateway 10.10.10.254
        set device port2
        set distance 10
    next
end
get router info routing-table static
diagnose ip route list | grep 192.168.50
```

**Expected result:** the route appears in the routing table; FortiOS selects by longest
prefix, then administrative distance, then priority — the deterministic order the exam
tests.

**Negative test:** add a second route to the same prefix with a higher distance and
expect load-sharing; only the lower-distance route installs — equal distance (ECMP) is
required to share.

**Rollback:**

```text
config router static
    delete 10
end
```

**Lessons from a live eval run.** Confirmed on an evaluation FortiGate-VM:

- *A static route installs whenever its outbound interface is up — FortiOS does not require
  the gateway to sit on a connected subnet at configuration time.* A route configured with an
  off-subnet gateway still installs via its device and appears in both
  `get router info routing-table static` and `diagnose ip route list`; only actual forwarding
  would fail (the ARP for the gateway goes unanswered). Installation and *selection* — what
  this lab teaches — work regardless, so the textbook values run as-is.
- *The selection order is longest prefix, then administrative distance, then ECMP.* A more
  specific prefix installs alongside a less specific one regardless of distance — distance
  only breaks ties between routes to the **same** prefix; among same-prefix routes the lowest
  distance wins and the rest stay out of the RIB; and equal distance **and** priority yields
  ECMP, with both next-hops installed and load-sharing. `v4-ecmp-mode` (default
  `source-ip-based`) selects the hash and `ecmp-max-paths` caps the number of shared paths.
- *The eval's three-route cap bites here.* With the default route plus two test routes you are
  already at three; a fourth fails with
  `Command fail. Return code -4 (reached the maximum number of entries)`. Delete as you go, or
  use a licensed FortiGate, to hold more than three routes at once.

### Lab 5.3 — Source NAT (Topic: NAT)

**Eval FortiGate — capable.** Runs on the free/licensed evaluation FortiGate-VM as-is.

**Objective:** Configure outbound NAT with an IP pool.

```text
config firewall ippool
    edit lan-snat
        set type overload
        set startip 203.0.113.20
        set endip 203.0.113.20
    next
end
config firewall policy
    edit 10
        set name lan-to-wan
        set srcintf port2
        set dstintf port1
        set srcaddr all
        set dstaddr all
        set action accept
        set schedule always
        set service ALL
        set nat enable
        set ippool enable
        set poolname lan-snat
    next
end
diagnose firewall ippool list
```

**Expected result:** LAN traffic egresses translated to `203.0.113.20`; a session in
`diagnose sys session list` shows the SNAT mapping — source NAT hides internal
addressing behind a routable pool.

**Negative test:** enable `nat` but leave `ippool disable`; traffic uses the outgoing
interface IP instead of the pool — the pool binding is what selects the translated
address.

**Rollback:**

```text
config firewall policy
    delete 10
end
config firewall ippool
    delete lan-snat
end
```

**Lessons from a live eval run.** Confirmed on an evaluation FortiGate-VM (12 August 2026),
driving real traffic across the eval-fit two-segment topology of Labs 5.10–5.11:

- *`diagnose firewall ippool list` is the wrong lens for an `overload` pool.* It prints an
  empty `list ippool info:(vf=root)` header even while sessions are actively translating.
  Use `diagnose firewall ippool-all list` (the pool definition) and
  `diagnose firewall ippool-all stats`, which report the PAT port range
  (`startport: 5117  endport: 65533`) and the live `total ses`/`tcp ses` counters that rise
  and fall with traffic.
- *The session table is the authoritative proof of SNAT.* `diagnose sys session list` shows
  the translation directly:

  ```text
  hook=post dir=org   act=snat 10.30.1.10:41203->10.30.2.10:5432(203.0.113.20:41203)
  hook=pre  dir=reply act=dnat 10.30.2.10:5432->203.0.113.20:41203(10.30.1.10:41203)
  ```

  `act=snat` with the source rewritten to the pool address is the source NAT; the paired
  `act=dnat` reply line is the automatic reverse translation. `proto_state=07` confirms the
  TCP session is established, not a half-open SYN.
- *You need an established connection to observe it.* A probe to a closed port is a transient
  `SYN_SENT` session that expires in seconds and is hard to catch; a connection to a
  listening service (here PostgreSQL on 5432) stays established, so the translated session
  sits in the table long enough to read — hold several open at once to watch `tcp ses` climb.
- *Revert order matters.* Clear the policy's pool reference before deleting the pool:
  `unset poolname` → `set ippool disable` → `set nat disable`, then `delete` the pool.
  FortiOS refuses to delete an IP pool while a policy still references it.

### Lab 5.4 — Destination NAT with a VIP (Topic: Virtual IPs / DNAT)

**Eval FortiGate — capable.** Runs on the free/licensed evaluation FortiGate-VM as-is.

**Objective:** Publish an internal server with a Virtual IP.

```text
config firewall vip
    edit web-vip
        set extip 203.0.113.80
        set extintf port1
        set mappedip 10.10.10.50
        set portforward enable
        set extport 443
        set mappedport 443
    next
end
config firewall policy
    edit 20
        set name inbound-web
        set srcintf port1
        set dstintf port2
        set srcaddr all
        set dstaddr web-vip
        set action accept
        set schedule always
        set service HTTPS
    next
end
diagnose firewall vip realservers list
```

**Expected result:** external `203.0.113.80:443` maps to `10.10.10.50:443`; a policy
referencing the VIP as destination admits the inbound flow — DNAT publishes an internal
service on a public address.

**Negative test:** create the VIP but write the policy with `dstaddr all`; the DNAT
still occurs but every service is exposed, not just HTTPS — the VIP as `dstaddr` plus a
tight service is what scopes exposure.

**Rollback:**

```text
config firewall policy
    delete 20
end
config firewall vip
    delete web-vip
end
```

**Lessons from a live eval run.** Confirmed on an evaluation FortiGate-VM (12 August 2026),
publishing a PostgreSQL server through a VIP on the eval-fit two-segment box:

- *A VIP is a forward-DNAT **and** a reverse-SNAT.* The session table carries both hooks on the
  one session:

  ```text
  hook=pre  dir=org   act=dnat 10.30.1.10:39003->10.30.1.100:5432(10.30.2.10:5432)
  hook=post dir=reply act=snat 10.30.2.10:5432->10.30.1.10:39003(10.30.1.100:5432)
  ```

  The `dnat` line rewrites the destination from the VIP to the real server on the way in; the
  paired reply `act=snat` rewrites the source back to the VIP on the way out, so the client sees
  answers from the address it dialed. It is the exact mirror of the source-NAT session in
  Lab 5.3 (`snat` on org / `dnat` on reply). `proto_state=07` confirms it established.
- *`show` hides `set protocol tcp`.* TCP is the default protocol for a port-forward VIP, so
  `show firewall vip` omits it — an absent protocol line means the default, not "unset" (the same
  `show`-vs-`get` rule as elsewhere in this chapter).
- *`diagnose firewall vip realserver list` is for load-balance VIPs only.* The keyword is
  `realserver` (singular), and a plain port-forward VIP reports `alloc=0` because it has no
  real-server pool — that table populates only for `server-load-balance` VIPs. Do not read
  `alloc=0` as a fault.
- *FortiOS `diagnose`/`get` are not a shell.* Appending `2>/dev/null` (or any stderr
  redirection) throws `command parse error ... Return code -61`, and there is no
  `| head`/`| tail`/`| awk`. The one pipe filter is FortiOS's built-in `grep` — a single
  pattern with options `-i -n -v -f -c -A -B -C`, no `-E`/alternation (`grep -iE "a|b"`
  returns `grep: invalid option -- 'E'`); grep one term per line.

### Lab 5.5 — Virtual domains (VDOMs) (Topic: VDOMs)

**Eval FortiGate — licensed-only.** You can switch to multi-VDOM mode, but the eval license allows only **one traffic VDOM** — creating the tenant VDOM fails with `Could not create VD, all VD licenses have been used` (setting `root` to an admin VDOM still leaves one traffic VDOM). The split needs a licensed FortiGate; on the eval, read and design.

**Objective:** Enable multi-VDOM and create a tenant VDOM.

```text
config system global
    set vdom-mode multi-vdom
end
config vdom
    edit tenant-a
    next
end
config global
    get system status | grep -i "Virtual domain"
end
```

**Expected result:** the FortiGate reports multi-VDOM enabled and `tenant-a` exists as
an isolated virtual firewall with its own interfaces, policies, and routing table —
VDOMs partition one appliance into independent security domains.

**Negative test:** expect traffic to cross VDOMs automatically; it does not without an
inter-VDOM link — isolation is the point, and inter-VDOM routing is explicit.

**Rollback:**

```text
config vdom
    delete tenant-a
end
config system global
    set vdom-mode no-vdom
end
```

### Lab 5.6 — Active-passive HA (Topic: A-P HA)

**Eval FortiGate — capable with a second eval unit.** HA needs a **second** FortiGate of matching model and *exact* firmware; a lone eval VM writes the config but has no peer to cluster with. Two eval VMs *do* form a working, config-synced, failover-capable cluster — with one real constraint (the eval's three-interface cap forces a shared-interface heartbeat), documented in the live-run note after the lab.

**Objective:** Form an active-passive HA cluster.

```text
config system ha
    set group-name LAB-HA
    set mode a-p
    set hbdev port3 50
    set session-pickup enable
    set override disable
    set priority 200
end
get system ha status
diagnose sys ha checksum cluster
```

**Expected result:** two FortiGates form a cluster; `get system ha status` shows a
primary and secondary, and the checksum matches across members — active-passive HA
gives stateful failover with session pickup so flows survive a device failure.

**Negative test:** mismatch the `group-name` or heartbeat interface between units; they
never form a cluster and both stay primary (split-brain) — matching HA parameters and a
dedicated heartbeat link are mandatory.

**Rollback — tear the active-passive cluster back down to standalone.** Break it in order,
the **secondary first**, so it does not momentarily claim primary as the cluster dissolves:

```text
config system ha          # run on the SECONDARY first, then the PRIMARY
    set mode standalone
    unset group-name
    set group-id 0
    unset password
    unset hbdev
    set override disable
    set session-pickup disable
    set priority 128
end
```

`set mode standalone` **alone is not a complete rollback** — it stops the unit clustering but
leaves the group name, group ID, heartbeat devices, password, override, and priority in the
config, so `get system ha status` still reports the old `Group Name`/`Group ID`. Clear them
(above) so the unit is genuinely free of HA; confirm with `show system ha`, which collapses to
defaults (at most `set override disable` remains — itself the default). Each unit reboots out of
HA as a standalone device. **Plan for one consequence:** both units
now hold the *same* synchronized configuration — including identical interface IPs — so leaving
both connected to the same segments causes an address conflict. Re-address, shut down, or
restore the pre-cluster backup on the second unit before returning it to service. Verify each is
clear of HA with `get system ha status` (expect `Mode: Standalone`). To convert this cluster to
**active-active** instead of tearing it down, see Lab 5.7.

**Lessons from a live eval run.** Confirmed 12 August 2026 by clustering two evaluation
FortiGate-VMs (both `v7.6.7,build3704 (GA.M)`) on Proxmox — which corrects the "licensed-only"
assumption this lab historically carried:

- *Two eval VMs form a fully working FGCP cluster.* They negotiate the cluster, elect a
  primary/secondary, synchronize configuration to matching checksums, and fail over — the
  whole HA lifecycle runs on evaluation licenses. HA is **not** license-gated; a *single* eval
  VM simply has no peer.
- *The three-interface cap blocks a dedicated heartbeat.* A fourth vNIC is never instantiated
  on an eval VM — the interface cap applies to physical ports, not just VLANs (Lab 5.9) — so
  there is no spare port for a dedicated heartbeat link. Set an existing data interface as the
  heartbeat device instead: `set hbdev "port2" 50 "port3" 50`. FGCP lets a data interface
  carry heartbeat traffic alongside data; a licensed unit lifts the cap and restores a
  dedicated link.
- *Firmware must match exactly.* Both units must report the same `get system status` version
  **and** build (here `build3704`); a difference in build or branch prevents the cluster from
  forming.
- *Never hard-reset a FortiGate-VM.* Power-cycling the guest from the hypervisor
  (`qm reset`/`qm stop`, or a "reset" in any hypervisor) triggers *"WARNING: File System Check
  Recommended! An unsafe reboot may have caused an inconsistency in the disk drive"*, and the
  resulting config-partition damage makes the secondary loop forever on *"failed to sync with
  primary, will try again."* Always reboot with `execute reboot`; repair a flagged disk with
  `execute disk list` then `execute disk scan <ref#>`.
- *HA priority is per-unit and not config-synced.* Each member keeps its own `set priority`, so
  the cluster checksum still matches. `set override enable` plus a higher priority makes a unit
  reclaim primary after it rejoins; when override does not apply, **uptime** decides the
  election. The `get system ha status` "Primary selected using" log narrates every decision
  (`override priority is larger`, `uptime is larger`, `SET_AS_SECONDARY flag is set`, `only
  member`) — read it to understand why a given unit is primary.
- *Failover is transparent to the segments.* On primary failure the cluster's virtual MAC and
  interface IPs move to the new primary, so a downstream host keeps reaching its gateway and
  its permitted service across the reboot with no reconfiguration — verified by an
  uninterrupted `web→db` path during a primary reboot.

### Lab 5.7 — Active-active HA by converting an active-passive cluster (Topic: A-P to A-A)

**Eval FortiGate — capable with a second eval unit.** This converts the two-eval-VM cluster from
Lab 5.6, so the same "no dedicated heartbeat, shared `port2`/`port3` heartbeat" constraint
applies.

**Objective:** Convert the active-passive cluster to active-active, where both units process
traffic, and observe sessions load-balanced across the members.

**Prerequisites:** the two-member cluster from Lab 5.6 (or build one first), both units on
matching firmware with the shared-interface heartbeat.

**Background.** In active-active FGCP, both units process traffic. The primary receives all
traffic and distributes sessions to the secondary using a configurable schedule. By default A-A
load-balances only the CPU-heavy **proxy-based UTM inspection** sessions; `set load-balance-all
enable` extends distribution to *all* firewall sessions, which makes the effect visible in a lab
that runs no UTM. A-A raises aggregate inspection throughput across many sessions — it is **not**
a bandwidth multiplier for a single flow.

**Step 1 — switch the cluster to active-active.** Change the mode on the primary (it syncs to
the secondary) and add a schedule plus all-session load-balancing:

```text
config system ha
    set mode a-a
    set schedule leastconnection
    set load-balance-all enable
end
```

The cluster renegotiates briefly, then both units are active.

**Step 2 — verify the mode and membership:**

```text
get system ha status
```

**Expected result:** the header now reports **`Mode: HA A-A`** (was `A-P`), still two members,
both **in-sync**, heartbeat flowing on `port2`/`port3`.

**Step 3 — watch sessions distribute across both units.** A-A distributes **transit**
(through-the-firewall) sessions only — local and management sessions (your console/SSH, the
heartbeat itself) always stay on the primary — so you must push *transit* traffic to see the
effect. Generate several concurrent sessions **through** the cluster (a batch of `web→db`
connections from a segment host), then read the per-unit load:

```text
diagnose sys ha status
get system ha status | grep -A6 "System Usage"
```

Use `-A6`, not `-A3`: three lines of context stop at the second member's header and hide its
`sessions=` line, making the secondary look idle when it is not.

**Expected result:** `diagnose sys ha status` shows **both** members carrying sessions — the
schedule assigns each new session to the less-loaded unit, so the secondary is no longer idle.
The per-unit `sessions=` counters in `get system ha status` both climb, rather than every session
sitting on one unit as in active-passive. Read `traffic.local` against `traffic.total` in
`diagnose sys ha status` first: when `traffic.local` is almost the whole of `traffic.total`, the
cluster is carrying only local/management sessions and there is nothing to distribute yet —
generate through-traffic before concluding the secondary is idle.

**Negative test:** expect a single large transfer to run at twice a lone unit's throughput. It
does not — A-A distributes *sessions*, not the packets of one flow, so one connection is pinned
to one unit. A-A scales inspection across many sessions, not the speed of any one.

**Rollback:** return to active-passive (or all the way to standalone via Lab 5.6's rollback):

```text
config system ha
    set mode a-p
end
```

**Lessons from a live active-active run.** Confirmed 14 August 2026 on the same two eval
FortiGate-VMs from Lab 5.6 (FGT-3 primary / FGT-2 secondary, both `v7.6.7,build3704`). These are
the behaviors — resilience and failure modes alike — that active-active adds on top of active-passive:

- *A non-forwarding secondary blackholes the load-balanced path — 100%, not 50%.* Forwarding is
  license-gated; HA membership is not. So an **unlicensed** secondary joins the cluster, syncs,
  and shows a healthy heartbeat, yet cannot forward a single transit packet. With `schedule
  leastconnection` the trap is total: every session the secondary is handed dies instantly, its
  session count stays at zero, so it is *permanently* the least-loaded unit, so the scheduler
  keeps steering **new** sessions to it. The permitted `web→db:5432` path measured **0/12**, not
  the 6/12 a half-dead pair suggests — while the primary (`License Status: Valid`) forwarded that
  same path perfectly when standalone. **Confirm both members are licensed before running A-A:**
  on each unit, `get system status | grep -i license` must read `License Status: Valid`. The fast
  fix *and* proof is to drop back to A-P (`set mode a-p`) — only the Valid primary forwards and
  the path recovers immediately — or license the secondary (each HA member needs its own
  forwarding license).
- *Bringing a member into A-A — cold at boot, or rejoining after a reboot — briefly blackholes
  transit for the same reason an unlicensed one does permanently.* `schedule leastconnection` hands
  new sessions to whichever member holds the fewest, and a just-joined unit holds zero, so the
  scheduler steers new sessions onto it while it is still syncing state and learning ARP/neighbors
  and cannot yet forward. A live failover-and-rejoin cycle measured this against a client probing
  every three seconds: losing the **active** unit dropped a *single* probe (well under ten seconds)
  as the survivor took over, but powering a member back **on** dropped **three** consecutive probes
  (~20 seconds) as the returning unit warmed up. Bringing a unit back into an active-active cluster
  therefore disturbs transit much as losing one does — it is not seamless just because no failover
  is occurring, so plan maintenance windows accordingly. The warm-up hits *load-balanced* transit
  only, though: an established site-to-site IPsec tunnel is pinned to the primary that owns its SA
  and is not offloaded to the joining member, so it rides the rejoin untouched — zero dropped probes,
  measured in [Chapter 06](06-firewall-policy-authentication-vpn-and-zero-trust-access.md)'s Lab 6.4,
  against the ~20-second blip the plaintext path takes here.
- *An eval secondary cannot hold a licensed primary's richer config → permanent out-of-sync.* A
  full segmentation config (multiple VLAN interfaces, policies, routes) exceeds the eval
  three-interface / three-policy / three-route budget (Lab 5.9), so the secondary silently rejects
  the objects it cannot create and its checksum never matches. `get system ha status` then reports
  it `out-of-sync` with a differing `chksum dump`. The definitive diagnostic runs on the
  **secondary**: `diagnose debug config-error-log read` lists exactly which synced objects it
  refused, and why (interface / policy / route limit). An out-of-sync secondary in A-A is
  dangerous — it is handed sessions it lacks the policy to process.
- *Never reboot the primary while the cluster is out-of-sync.* While the primary is down the
  leaner secondary becomes primary; when the original primary returns it rejoins as **secondary**
  and syncs *from* the leaner unit — pulling the reduced config on top of its own good config, so
  now **both** members carry the broken config. Fix the sync first (or restore the primary's
  config from backup); do not reboot the primary to "clear" an out-of-sync state.
- *Both units reporting `(Primary)` for a few seconds at formation is normal, not split-brain.*
  FGCP takes several seconds to exchange heartbeats and elect; if you capture `get system ha
  status` the instant you type `end`, each unit still lists only itself. Wait 30–60 s and
  re-check — the lower-priority unit demotes to secondary. It is split-brain only if each unit
  *keeps* listing a single member after negotiation settles (then chase the heartbeat interface or
  a firmware-build mismatch, per Lab 5.6).
- *`config system ha` is a single object — there is no `edit`/`next`.* Typing `next` inside it
  returns `Unknown action 0`; use `set …` lines then `end`. (`edit`/`next` apply only inside a
  table such as `config system interface`.)
- *Verify HA membership from the CLI, not the GUI's fabric view.* The GUI device dropdown and
  **System > Firmware & Registration** list **Security Fabric** members — a different feature — so
  a cluster peer can be absent there while still fully in the HA cluster. The authoritative
  membership is `get system ha status`: read `number of member:` and the per-member lines
  (`FGT-3 …, HA cluster index = 0` / `FGT-2 …, HA cluster index = 1`). `execute ha manage ?` lists
  the manageable peers by index; `execute ha manage <index> admin` opens a secondary's CLI.
- *A stale `HA Health Status: ERROR: <serial> is lost @ <date>` is cosmetic.* It is the cluster
  remembering a former member (for example a rebuilt secondary's previous serial); it does not
  affect the current members and clears on its own. Several stale entries can accumulate — a live
  cluster showed one serial lost two days earlier alongside the one just powered off — and only the
  most recent, matching a member you actually removed, reflects current state.
- *The resilience payoff: with `set session-pickup enable`, live sessions survive failover —
  firewall-auth sessions included.* The primary synchronizes its session table to the secondary,
  which marks each synced entry `flag(400): ha`; on failover the promoted unit keeps serving those
  sessions, so users are not forced to reconnect or re-authenticate (the promoted entry even keeps
  its `flag(400): ha` marker rather than being re-created). Proven bidirectionally on the live pair
  — fail the primary, let it rejoin, then fail the new primary back — with an authenticated user
  staying logged in across both failovers. Without `session-pickup` the cluster still fails over but
  drops every live session. See
  [Chapter 06](06-firewall-policy-authentication-vpn-and-zero-trust-access.md) Lab 6.3 for the
  firewall-authentication case captured in full.

### Lab 5.8 — Active-active HA formed directly (Topic: A-A HA)

**Eval FortiGate — capable with a second eval unit.**

**Objective:** Stand up a running active-active cluster and leave it in service. FGCP does not
require staging through active-passive — `set mode a-a` can be applied at formation — but the
build, verification, and load-distribution commands are exactly those of Lab 5.7. Rather than
repeat them:

**Perform Lab 5.7, but do not run its rollback.** The active-active cluster Lab 5.7 produces
(`Mode: HA A-A`, both members carrying sessions) is the deliverable here — leave it running.
Forming "directly" only means placing `set mode a-a` in the initial HA block on both units
instead of forming active-passive first and converting; the resulting cluster is identical
either way, which is why the procedure is not duplicated.

**When to use which.** Convert from active-passive (Lab 5.7) when a cluster is already running in
production and you are enabling load sharing live; form active-active directly (this lab) when
you are building a new cluster you already know should share load.

**Rollback:** none in this lab — it intentionally leaves the active-active cluster running. To
tear it back down to standalone when finished, run Lab 5.6's rollback with two additions
(`set schedule none` and `set load-balance-all disable`).

### Lab 5.9 — The evaluation interface budget and the VLAN purge (Topic: Eval limitations)

**Eval FortiGate — this lab *is* the limitation.** It reproduces the free evaluation
FortiGate-VM's caps rather than working around them; the two labs that follow are shaped by
what it shows. Labs 5.9–5.11 were validated live on a 7.6.7 evaluation VM on 12 August 2026.

**Objective:** Observe the evaluation FortiGate-VM's three-entry caps on interfaces, policies,
and routes, and the boot-time purge of over-budget VLAN sub-interfaces.

**The budget.** The `FGVMEV` evaluation permits roughly **three interface entries, three
policies, and three routes**, and the factory configuration already spends the interface
budget — `port1`, `port2`, the switch-controller `fortilink`, and the wireless `default-mesh`
VAP are all entries. Confirm the tier and the live interface set:

```text
diagnose debug vm-print-license | grep -i model      # -> Model: EVAL
diagnose ip address list
```

**Step 1 — hit the cap directly.** Creating a fourth entry in any of the three tables fails
at once:

```text
FGT # config system interface
FGT (interface) # edit vlan99
FGT (vlan99) # set vlanid 99
FGT (vlan99) # set interface port2
FGT (vlan99) # next
Command fail. Return code -4 (reached the maximum number of entries)
```

The same `-4` appears on a fourth static route (Lab 5.2's live-run note) and a fourth firewall
policy (Lab 5.3's Gotcha) — one budget, three tables.

**Step 2 — the silent purge.** More dangerous than the create-time error: VLAN sub-interfaces
that fit *before* a license event are **deleted at the next boot** when the license
re-evaluates the budget. Build several VLANs (`v2001`–`v2004` on `port2`, as in Lab 5.1),
confirm they pass traffic, then reboot and re-check the running state:

```text
FGT # diagnose ip address list
IP=10.30.99.122->10.30.99.122/255.255.255.0 index=3 devname=port1
IP=127.0.0.1->127.0.0.1/255.0.0.0 index=7 devname=root
IP=10.255.1.1->10.255.1.1/255.255.255.0 index=10 devname=fortilink
```

**Expected result:** after the reboot the four VLAN gateways (`10.30.1.1`–`10.30.4.1`) are
**gone** — only `port1` and `fortilink` remain — and every zone or policy that referenced them
is orphaned. Downstream hosts lose their gateway with no error to explain it.

**Negative test:** trust `show system interface` — which still lists the VLANs in the *saved*
config — as proof they are active. `diagnose ip address list` (the running state) is the truth;
the saved config can describe interfaces the license refuses to instantiate.

**Rollback:** none — the next two labs rebuild the topology inside the budget.

### Lab 5.10 — Segments on physical ports with hypervisor VLAN tagging (Topic: Eval-fit segmentation)

**Eval FortiGate — capable.** This is the design that fits the evaluation budget: physical
ports instead of VLAN sub-interfaces, so there is nothing for the license to purge.

**Objective:** Build a two-segment routed topology inside the eval's three-interface budget by
giving the FortiGate one **physical port per segment** and letting the **hypervisor** apply the
VLAN tag — the remedy Chapter 04 names, carried out end to end.

**The shift.** Lab 5.1 carries many segments as VLAN sub-interfaces of one trunk — correct on a
licensed FortiGate, impossible on the eval (Lab 5.9). The eval-fit alternative moves the tagging
**off** the FortiGate and **onto** the hypervisor: each segment is a separate vNIC presented as
an access port, and the FortiGate addresses the physical `portN` directly. Two segments then
cost `port1` (management) + `port2` + `port3` = three interfaces, exactly at budget, with
**zero** sub-interfaces.

**Step 1 — hypervisor: one access-port vNIC per segment.** On Proxmox VE, make `port2` an
access port on VLAN 2001 and add `port3` as an access port on VLAN 2002 (the guest sees plain,
untagged ports):

```text
qm set 122 --net1 virtio=<MAC>,bridge=vmbr2,tag=2001    # port2 = segment A
qm set 122 --net2 virtio,bridge=vmbr2,tag=2002          # port3 = segment B (new vNIC)
```

Reboot the FortiGate so it detects the new port. On ESXi the equivalent is a per-VLAN port
group on the vSwitch; on KVM/libvirt, an interface bound to a tagged bridge.

**Step 2 — FortiGate: address the physical ports.** Because `port2` and `port3` already exist,
setting an IP is an **edit**, not a create, so the interface cap never fires:

```text
config system interface
    edit port2
        set alias APP
        set ip 10.30.1.1 255.255.255.0
        set allowaccess ping
        set role lan
    next
    edit port3
        set alias DB
        set ip 10.30.2.1 255.255.255.0
        set allowaccess ping
        set role lan
    next
end
diagnose ip address list
```

**Expected result:** both ports take their addresses with no `-4`, and the running state shows
them live:

```text
IP=10.30.1.1->10.30.1.1/255.255.255.0 index=4 devname=port2
IP=10.30.2.1->10.30.2.1/255.255.255.0 index=5 devname=port3
```

**Step 3 — one policy, using the ports directly** (no zones needed; well under the
three-policy cap):

```text
config firewall address
    edit web
        set subnet 10.30.1.10 255.255.255.255
    next
    edit db
        set subnet 10.30.2.10 255.255.255.255
    next
end
config firewall policy
    edit 1
        set name web-to-db
        set srcintf port2
        set dstintf port3
        set srcaddr web
        set dstaddr db
        set action accept
        set schedule always
        set service PGSQL
        set logtraffic all
    next
end
```

**Negative test:** carry the same two segments as VLAN sub-interfaces of one trunk on the eval
instead; the second sub-interface (or the next reboot) fails or purges (Lab 5.9). Physical ports
are tied to real vNICs and are never purged — that is the whole point of the shift.

**Rollback:** none — Lab 5.11 validates this topology.

### Lab 5.11 — Proving segmentation and reboot-survival (Topic: Eval-fit validation)

**Eval FortiGate — capable.** Confirms the eval-fit topology both enforces segmentation and
persists across the reboot that erased the VLAN design.

**Objective:** From a host on segment A, prove the policy permits only the allowed service and
denies the rest, then reboot the FortiGate and prove the whole topology survives.

**Prerequisites:** a host on segment A (this run used an **Alpine** VM at `10.30.1.10`, gateway
`port2`/`10.30.1.1`) and a service on segment B (a PostgreSQL host at `10.30.2.10:5432`, gateway
`port3`/`10.30.2.1`).

**Step 1 — segmentation, from the segment-A host:**

```text
ping -c3 10.30.1.1                       # gateway (port2)
ping -c2 10.30.2.10                       # far host, ICMP
nc -w5 -z 10.30.2.10 5432; echo $?        # far host, the allowed service
```

**Expected result:** the gateway answers, ICMP to the far host is **denied**, and PGSQL is
**allowed** — segmentation in three lines:

```text
10.30.1.1:  3 packets transmitted, 3 received, 0% packet loss, ttl=255   # gateway reachable
10.30.2.10: 2 packets transmitted, 0 received, 100% packet loss          # ICMP denied
0                                                                        # nc exit 0 = PGSQL allowed
```

Only the service named in policy 1 crosses the segment boundary; everything else hits the
implicit deny.

**Step 2 — reboot-survival:**

```text
execute reboot
# after it returns:
diagnose ip address list        # port2=10.30.1.1 and port3=10.30.2.1 still present
show firewall policy            # policy 1 web-to-db intact
```

Re-run Step 1; the results are identical.

**Expected result:** `port2`, `port3`, and the policy are **unchanged after the reboot**, and
segmentation still holds. This is what the design shift buys: run Lab 5.9's four-VLAN topology
through the same reboot and the segment-A host's gateway ping goes to **100% loss**, because
`10.30.1.1` no longer exists.

**Negative test:** conclude "it works" from the pre-reboot test alone. On the eval the reboot
is the real exam — the VLAN design passes Step 1 and fails Step 2; the physical-port design
passes both.

**Rollback:** leave the topology in place — it is the working eval-fit ISFW the rest of your labs
can build on.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter built FGT-LAB-01's data-plane foundation: physical and VLAN
interfaces, static and policy routing, NAT via an IP pool and a
destination-NAT VIP, VDOM segmentation connected through an inter-VDOM
link, and a two-member FGCP high-availability cluster validated through a
forced heartbeat-loss negative test, and closed with an eval-fit segmentation track
(Labs 5.9–5.11) that meets the evaluation FortiGate-VM's three-interface budget by moving VLAN
tagging to the hypervisor and building segments on physical ports — a design that survives the
reboot the VLAN approach does not. [Chapter 06](06-firewall-policy-authentication-vpn-and-zero-trust-access.md) builds firewall policy,
authentication, and VPN configuration directly on top of this network and
HA foundation.

- [ ] Can configure physical, VLAN, static, and policy routing on
      FortiGate.
- [ ] Can explain the difference between policy-based NAT, central NAT,
      and VIP-based destination NAT.
- [ ] Can enable multi-VDOM mode, create VDOMs, and connect them with an
      inter-VDOM link.
- [ ] Can configure and validate a two-member FGCP HA cluster, including
      diagnosing a split-brain condition, converting active-passive to
      active-active, and rolling the cluster back to standalone.
- [ ] Can explain the evaluation FortiGate-VM's three-interface/policy/route
      budget and the boot-time purge of over-budget VLAN sub-interfaces.
- [ ] Can build an eval-fit two-segment ISFW on physical ports with
      hypervisor VLAN tagging, and prove it enforces segmentation and
      survives a reboot.
- [ ] Completed the hands-on lab, including the negative test.
