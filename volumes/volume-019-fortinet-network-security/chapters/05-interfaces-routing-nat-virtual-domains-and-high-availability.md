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

**Shared prerequisites for Labs 5.1–5.6** — a FortiGate on FortiOS 7.6 with at least
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

**Cleanup:**

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

**Cleanup:**

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

**Cleanup:**

```text
config firewall policy
    delete 10
end
config firewall ippool
    delete lan-snat
end
```

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
diagnose firewall vip realservers list 2>/dev/null | head
```

**Expected result:** external `203.0.113.80:443` maps to `10.10.10.50:443`; a policy
referencing the VIP as destination admits the inbound flow — DNAT publishes an internal
service on a public address.

**Negative test:** create the VIP but write the policy with `dstaddr all`; the DNAT
still occurs but every service is exposed, not just HTTPS — the VIP as `dstaddr` plus a
tight service is what scopes exposure.

**Cleanup:**

```text
config firewall policy
    delete 20
end
config firewall vip
    delete web-vip
end
```

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

**Cleanup:**

```text
config vdom
    delete tenant-a
end
config system global
    set vdom-mode no-vdom
end
```

### Lab 5.6 — High availability (Topic: HA)

**Eval FortiGate — licensed-only.** HA needs a **second** FortiGate of matching model and firmware; a lone eval VM can write the config but cannot form a cluster. On the eval, treat this as a read-and-design lab.

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

**Cleanup:** `set mode standalone` on the lab unit to leave the cluster.

### Lab 5.7 — The evaluation interface budget and the VLAN purge (Topic: Eval limitations)

**Eval FortiGate — this lab *is* the limitation.** It reproduces the free evaluation
FortiGate-VM's caps rather than working around them; the two labs that follow are shaped by
what it shows. Labs 5.7–5.9 were validated live on a 7.6.7 evaluation VM on 12 August 2026.

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

**Cleanup:** none — the next two labs rebuild the topology inside the budget.

### Lab 5.8 — Segments on physical ports with hypervisor VLAN tagging (Topic: Eval-fit segmentation)

**Eval FortiGate — capable.** This is the design that fits the evaluation budget: physical
ports instead of VLAN sub-interfaces, so there is nothing for the license to purge.

**Objective:** Build a two-segment routed topology inside the eval's three-interface budget by
giving the FortiGate one **physical port per segment** and letting the **hypervisor** apply the
VLAN tag — the remedy Chapter 04 names, carried out end to end.

**The shift.** Lab 5.1 carries many segments as VLAN sub-interfaces of one trunk — correct on a
licensed FortiGate, impossible on the eval (Lab 5.7). The eval-fit alternative moves the tagging
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
instead; the second sub-interface (or the next reboot) fails or purges (Lab 5.7). Physical ports
are tied to real vNICs and are never purged — that is the whole point of the shift.

**Cleanup:** none — Lab 5.9 validates this topology.

### Lab 5.9 — Proving segmentation and reboot-survival (Topic: Eval-fit validation)

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
segmentation still holds. This is what the design shift buys: run Lab 5.7's four-VLAN topology
through the same reboot and the segment-A host's gateway ping goes to **100% loss**, because
`10.30.1.1` no longer exists.

**Negative test:** conclude "it works" from the pre-reboot test alone. On the eval the reboot
is the real exam — the VLAN design passes Step 1 and fails Step 2; the physical-port design
passes both.

**Cleanup:** leave the topology in place — it is the working eval-fit ISFW the rest of your labs
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
(Labs 5.7–5.9) that meets the evaluation FortiGate-VM's three-interface budget by moving VLAN
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
      diagnosing a split-brain condition.
- [ ] Can explain the evaluation FortiGate-VM's three-interface/policy/route
      budget and the boot-time purge of over-budget VLAN sub-interfaces.
- [ ] Can build an eval-fit two-segment ISFW on physical ports with
      hypervisor VLAN tagging, and prove it enforces segmentation and
      survives a reboot.
- [ ] Completed the hands-on lab, including the negative test.
