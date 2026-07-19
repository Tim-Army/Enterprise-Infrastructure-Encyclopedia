# Chapter 02: Catalyst Campus Switching and Resiliency

![Lab topology for this chapter: DIST-01 and DIST-02 form an HSRP pair across VLANs 10 and 20 with active/standby roles reversed per VLAN (DIST-01 Active for VLAN 10 and Standby for VLAN 20; DIST-02 the inverse), both connected to ACCESS-01 by independent two-member LACP EtherChannel trunks carrying VLANs 10, 20, and 99 with native VLAN 999; DIST-01 is Rapid PVST+ root for all three VLANs. As a negative test, attaching an unauthorized switch that emits BPDUs to ACCESS-01's BPDU Guard-protected access port causes it to transition to err-disabled, logging a SPANTREE-2-BLOCK_BPDUGUARD event.](../../../diagrams/volume-03-cisco-enterprise-networking/chapter-02-hsrp-distribution-lacp-topology.svg)

*Figure 2-1. Topology used throughout this chapter's Hands-On Lab: an HSRP distribution pair with load spread across two VLANs, LACP-trunked to an access switch with BPDU Guard on its edge port.*

## Learning Objectives

- Configure VLANs, 802.1Q trunking, and VLAN Trunking Protocol (VTP) modes
  on Catalyst 9000 switches.
- Explain Spanning Tree Protocol (Rapid PVST+ and MST) operation and apply
  the STP toolkit that protects a switched access layer.
- Build resilient Layer 2 uplinks with EtherChannel/LACP and select the
  correct first-hop redundancy protocol for a distribution pair.
- Configure StackWise-480 and StackWise Virtual and explain their failure
  behavior.
- Apply loop and storm protection (UDLD, BPDU Guard, Root Guard, Loop
  Guard, storm control) to a production access layer.

## Theory and Architecture

### VLANs and trunking

A VLAN is a Layer 2 broadcast domain implemented independently of physical
topology. Catalyst 9000 switches carry VLANs across links using IEEE
802.1Q trunking, which inserts a 4-byte tag (12-bit VLAN ID, 3-bit priority
field used for CoS) into the Ethernet frame. A trunk's **native VLAN**
carries untagged frames; mismatched native VLANs between two ends of a
trunk are a common source of silent connectivity and security problems, so
distribution and access switches must agree on native VLAN for every trunk.

VTP (VLAN Trunking Protocol) propagates VLAN database changes across a
domain in versions 1–3. Because a misconfigured VTP client/server
relationship can wipe a switch's VLAN database, most current campus designs
run VTP in **transparent mode** (VLANs configured locally, VTP messages
only relayed) or disable VTP domain synchronization entirely in favor of
automation-managed, per-switch VLAN configuration ([Chapter 8](08-ios-xe-programmability-and-network-automation.md)).

### Spanning Tree Protocol

Any switched topology with redundant Layer 2 paths requires a loop
prevention protocol. Rapid PVST+ (IEEE 802.1w per VLAN, Cisco's default) and
Multiple Spanning Tree (MST, IEEE 802.1s, one or more instances mapped to
VLAN groups) are the two STP variants used in current Catalyst designs:

- **Rapid PVST+** runs one spanning-tree instance per VLAN. It scales
  administratively well for small-to-medium VLAN counts and converges in
  the sub-second range using the 802.1w proposal/agreement handshake, but
  CPU and control-plane load grow with VLAN count.
  
- **MST** maps many VLANs onto a small number of spanning-tree instances,
  which keeps control-plane overhead flat as VLAN count grows. MST requires
  every switch in a region to agree on the same region name, revision
  number, and VLAN-to-instance mapping or the switches fall into different
  MST regions and treat each other as legacy STP participants.

Regardless of variant, STP elects one **root bridge** per instance (lowest
bridge ID: priority + MAC), computes least-cost paths from every other
switch to the root, and blocks redundant links to eliminate loops. Root
bridge placement should always be explicit (`spanning-tree vlan <id>
root primary`) rather than left to default priority/MAC-address tiebreaks,
because an access switch accidentally winning root election can pull
traffic paths away from the intended distribution/core topology.

### EtherChannel

EtherChannel bundles 2–8 physical links into one logical interface for both
bandwidth aggregation and resiliency — STP treats the bundle as a single
link, so a member-link failure is handled by the channel's own hashing and
hardware failover rather than by a full STP recalculation. Link Aggregation
Control Protocol (LACP, IEEE 802.3ad) negotiates the bundle dynamically and
is preferred in production over Cisco's proprietary PAgP or static
(`on` mode) channels, because LACP detects misconfigured/miscabled members
before they are forwarded into an inconsistent bundle.

### First-hop redundancy

Endpoints need a single, stable default gateway even when that gateway is
implemented by a redundant pair of distribution switches. Three protocols
solve this:

| Protocol | Standard | Active/standby model | Load balancing |
| --- | --- | --- | --- |
| HSRP | Cisco proprietary | One active, one standby per group | Per-VLAN active router via multiple groups |
| VRRP | IETF standard ([RFC 5798](https://www.rfc-editor.org/rfc/rfc5798)) | One master, one+ backup per group | Per-VLAN master via multiple groups |
| GLBP | Cisco proprietary | One AVG, multiple AVFs | Per-host, within a single group |

HSRP and VRRP both require multiple groups (one per VLAN, alternating the
active router) to spread traffic across both distribution switches; GLBP
achieves per-host load balancing within a single group by handing out
different virtual MAC addresses to different clients' ARP requests. Most
current Catalyst campus designs use HSRP for its maturity and tight IOS XE
tooling (object tracking, preemption delay) unless a specific need for
per-host load distribution favors GLBP.

### Stacking and virtual chassis behavior

StackWise-480 members share a single control plane; the **active** switch
runs IOSd and programs forwarding tables, the **standby** switch maintains
synchronized state for fast failover (sub-second in most designs), and
remaining members are line cards from a control-plane perspective. Losing
the active member triggers the standby to take over without a full reload
of the surviving members.

StackWise Virtual (SVL) achieves the same logical-single-switch model
between two physically separate chassis using a high-bandwidth SVL link
(typically two or more 10/25/40/100GbE ports) plus a dedicated Dual-Active
Detection (DAD) link. If the SVL link fails but both chassis remain
individually healthy, DAD prevents a split-brain (both chassis believing
they are active) by having the surviving/losing chassis recover its role
once DAD confirms dual-active state.

## Design Considerations

- **Rapid PVST+ vs. MST** — choose Rapid PVST+ for campuses with a modest,
  fairly static VLAN count where per-VLAN load balancing across uplinks
  (different VLANs preferring different uplinks) is valuable; choose MST
  when VLAN count is large or growing and control-plane scale matters more
  than per-VLAN path granularity.
- **Root bridge placement** — always pin primary/secondary root explicitly
  at the distribution or core layer; never allow root election to default.
- **Uplink diversity** — pair EtherChannel uplinks with diverse physical
  paths (different line cards, different fiber runs) so a single hardware
  or cable fault cannot take down the whole bundle.
- **FHRP selection** — default to HSRP for operational familiarity and
  IOS XE object-tracking integration; reserve GLBP for scenarios that
  specifically need per-host load spread within one VLAN.
- **Stack vs. SVL vs. standalone with FHRP** — a single stack/SVL pair
  removes the need for FHRP at that tier but creates a single logical
  control-plane domain that must be upgraded and monitored as one unit;
  weigh this against a standalone-pair-plus-FHRP design, which keeps two
  independent control planes at the cost of needing FHRP tuning and dual
  monitoring.
- **Native VLAN and VLAN 1 hygiene** — never use VLAN 1 as a trunk's native
  VLAN or as the management VLAN in a production design; reserve it as an
  unused, shut-down placeholder consistent with [Chapter 1](01-cisco-enterprise-architecture-and-ios-xe-foundations.md)'s hardening
  baseline.
- **Storm-control thresholds** — size broadcast/multicast/unknown-unicast
  thresholds against measured baseline traffic, not a copy-pasted default,
  since undersized thresholds cause false-positive port shutdowns during
  legitimate bursts (for example, ARP storms during a large DHCP lease
  renewal wave).

## Implementation and Automation

### VLANs and trunk configuration

```text
DIST-01(config)# vlan 10
DIST-01(config-vlan)# name USERS
DIST-01(config-vlan)# exit
DIST-01(config)# vlan 20
DIST-01(config-vlan)# name VOICE
DIST-01(config-vlan)# exit
DIST-01(config)# vlan 99
DIST-01(config-vlan)# name MGMT
DIST-01(config-vlan)# exit
DIST-01(config)# interface TenGigabitEthernet1/0/1
DIST-01(config-if)# description Trunk to ACCESS-01
DIST-01(config-if)# switchport trunk encapsulation dot1q
DIST-01(config-if)# switchport mode trunk
DIST-01(config-if)# switchport trunk native vlan 999
DIST-01(config-if)# switchport trunk allowed vlan 10,20,99
DIST-01(config-if)# no shutdown
```

VLAN 999 above is an unused, dedicated "parking" VLAN for the native VLAN
so that double-tagging/VLAN-hopping attacks against a real production VLAN
are not possible (see Security and Best Practices).

### Rapid PVST+ and MST

```text
! Rapid PVST+
DIST-01(config)# spanning-tree mode rapid-pvst
DIST-01(config)# spanning-tree vlan 10,20,99 root primary
DIST-02(config)# spanning-tree vlan 10,20,99 root secondary

! MST (alternative, larger VLAN counts)
DIST-01(config)# spanning-tree mode mst
DIST-01(config)# spanning-tree mst configuration
DIST-01(config-mst)# name CAMPUS-REGION-1
DIST-01(config-mst)# revision 1
DIST-01(config-mst)# instance 1 vlan 1-999
DIST-01(config-mst)# exit
DIST-01(config)# spanning-tree mst 1 root primary
```

### EtherChannel with LACP

```text
DIST-01(config)# interface range TenGigabitEthernet1/0/1-2
DIST-01(config-if-range)# channel-protocol lacp
DIST-01(config-if-range)# channel-group 1 mode active
DIST-01(config-if-range)# exit
DIST-01(config)# interface Port-channel1
DIST-01(config-if)# switchport mode trunk
DIST-01(config-if)# switchport trunk allowed vlan 10,20,99
DIST-01(config-if)# no shutdown
```

### HSRP with object tracking

```text
DIST-01(config)# track 1 interface TenGigabitEthernet1/0/24 line-protocol
DIST-01(config)# interface Vlan10
DIST-01(config-if)# ip address 10.10.10.2 255.255.255.0
DIST-01(config-if)# standby version 2
DIST-01(config-if)# standby 10 ip 10.10.10.1
DIST-01(config-if)# standby 10 priority 110
DIST-01(config-if)# standby 10 preempt delay minimum 60
DIST-01(config-if)# standby 10 track 1 decrement 20
DIST-01(config-if)# exit
```

`DIST-02` mirrors this with a lower priority (for example, 100) so it
remains standby under normal conditions and only becomes active if
`DIST-01` loses priority through the tracked object or fails outright.

### StackWise Virtual

```text
DIST-01(config)# stackwise-virtual
DIST-01(config-stackwise-virtual)# domain 10
DIST-01(config-stackwise-virtual)# exit
DIST-01(config)# interface TenGigabitEthernet1/1/1
DIST-01(config-if)# stackwise-virtual link 1
DIST-01(config-if)# exit
DIST-01(config)# interface TenGigabitEthernet1/1/2
DIST-01(config-if)# stackwise-virtual dual-active-detection
DIST-01(config-if)# exit
```

Mirror the domain ID and link roles on the peer chassis, then reload both
switches together; they form a single logical switch (switch 1/switch 2)
after the SVL link comes up.

## Validation and Troubleshooting

```text
DIST-01# show vlan brief
DIST-01# show interfaces trunk
DIST-01# show spanning-tree summary
DIST-01# show spanning-tree vlan 10
DIST-01# show etherchannel summary
DIST-01# show standby brief
DIST-01# show switch stack-ports summary
DIST-01# show stackwise-virtual
DIST-01# show stackwise-virtual dual-active-detection
```

| Symptom | Likely cause | Check |
| --- | --- | --- |
| Trunk shows `(native VLAN mismatch)` in `show interfaces trunk` | Native VLAN differs between trunk ends | Compare `switchport trunk native vlan` on both sides |
| VLAN not passing traffic across a trunk | VLAN pruned from `switchport trunk allowed vlan` | `show interfaces trunk`, verify allowed-VLAN list on every hop |
| Port stuck in `BLK` state unexpectedly | Unintended root bridge election or a Root Guard/Loop Guard trigger | `show spanning-tree vlan <id>`, `show spanning-tree inconsistentports` |
| EtherChannel member shown as `suspended (D)` | LACP mode or VLAN/trunk mismatch between bundle members | `show etherchannel summary`, confirm identical `channel-protocol`, trunk, and speed/duplex on both member ports |
| HSRP flapping between active/standby | Tracked interface flapping, or preempt delay too short after a real failure | `show standby brief`, `show track 1`, increase `preempt delay` |
| StackWise Virtual shows `STANDBY` never converging to `READY` | SVL link bandwidth/count insufficient, or DAD link missing | `show stackwise-virtual link`, confirm both SVL and DAD links are up |

## Security and Best Practices

- Never use VLAN 1 for user data, management, or as a trunk's native VLAN;
  reassign it to an unused, administratively shut-down purpose.
- Set an explicit, unused native VLAN (as shown above) on every trunk to
  eliminate 802.1Q double-tagging VLAN-hopping exposure.
- Enable BPDU Guard on every access-facing (edge) port so that an
  unauthorized switch plugged into a user port is immediately
  error-disabled rather than allowed to participate in STP:

  ```text
  ACCESS-01(config)# interface range GigabitEthernet1/0/1-48
  ACCESS-01(config-if-range)# spanning-tree portfast edge
  ACCESS-01(config-if-range)# spanning-tree bpduguard enable
  ```

- Enable Root Guard on distribution-facing ports that should never become
  root, and Loop Guard on point-to-point non-designated ports to protect
  against unidirectional link failures that BPDU loss alone would not
  catch:

  ```text
  DIST-01(config-if)# spanning-tree guard root
  DIST-01(config-if)# spanning-tree guard loop
  ```

- Enable UDLD in aggressive mode on fiber uplinks to detect unidirectional
  link faults that autonegotiation cannot see:

  ```text
  DIST-01(config)# udld aggressive
  ```

- Apply storm control on access ports, sized from a measured baseline
  rather than a guess:

  ```text
  ACCESS-01(config-if)# storm-control broadcast level pps 2k
  ACCESS-01(config-if)# storm-control action shutdown
  ```

- Use `errdisable recovery` with a bounded interval rather than leaving
  error-disabled ports for manual re-enable only, but keep the interval
  long enough (300 seconds or more) that a transient flap doesn't mask a
  real, recurring problem:

  ```text
  DIST-01(config)# errdisable recovery cause bpduguard
  DIST-01(config)# errdisable recovery interval 300
  ```

## References and Knowledge Checks

**Authoritative references**

- Cisco, *Catalyst 9000 Series Switches Layer 2 Configuration Guide*, IOS XE
  17.x.
- IEEE 802.1Q (VLAN tagging), 802.1w (Rapid Spanning Tree), 802.1s
  (Multiple Spanning Tree), 802.3ad (Link Aggregation).
- [RFC 5798](https://www.rfc-editor.org/rfc/rfc5798), *Virtual Router Redundancy Protocol Version 3*.
- Cisco, *StackWise Virtual Configuration Guide*.

**Knowledge checks**

1. Why should the native VLAN on a trunk be set to an unused VLAN ID
   instead of left at the default?
2. What operational trade-off does MST solve compared to Rapid PVST+, and
   what must every switch in an MST region agree on?
3. Why is LACP generally preferred over static (`on` mode) EtherChannel in
   production?
4. Contrast HSRP, VRRP, and GLBP on load-balancing behavior.
5. What is the role of the Dual-Active Detection link in a StackWise
   Virtual domain, and what happens if it is missing when the SVL link
   fails?

## Hands-On Lab

**Objective:** Build a two-switch distribution pair with HSRP and an
access switch attached by a trunked, EtherChannel uplink, then verify loop
protection.

**Prerequisites**

- Two Catalyst 9000-series distribution switches (or CML nodes) with at
  least two interconnecting links each, plus one access switch, or an
  equivalent three-node CML topology.
- Console or SSH access to all three devices per [Chapter 1](01-cisco-enterprise-architecture-and-ios-xe-foundations.md)'s bring-up
  procedure.

**Procedure**

1. On both distribution switches, create VLANs 10, 20, and 99, and set
   Rapid PVST+ root roles as shown in Implementation (`DIST-01` primary,
   `DIST-02` secondary for all three VLANs).

2. Configure a two-member LACP EtherChannel trunk between `DIST-01` and the
   access switch, and a single trunk (or its own EtherChannel, if
   interfaces allow) between `DIST-02` and the access switch, allowing
   VLANs 10, 20, and 99 with native VLAN 999 on every trunk.

3. Configure HSRP for VLAN 10 as shown, with `DIST-01` as active
   (priority 110) and `DIST-02` as standby (priority 100). Repeat for
   VLAN 20 but reverse the priorities so `DIST-02` is active for VLAN 20 —
   this spreads active-gateway load across both distribution switches.

4. Verify convergence and role assignment:

   ```text
   DIST-01# show standby brief
   DIST-02# show standby brief
   DIST-01# show spanning-tree summary
   ```

   **Expected result:** `DIST-01` shows `Active` for group 10 and
   `Standby` for group 20; `DIST-02` shows the inverse. Spanning-tree
   summary shows `DIST-01` as root for VLANs 10/20/99.

5. On the access switch, enable BPDU Guard and PortFast edge on a spare
   access port, then verify the port is forwarding for an end host:

   ```text
   ACCESS-01# show spanning-tree interface GigabitEthernet1/0/10 detail
   ```

   **Expected result:** the port shows `PortFast enabled`, `Bpdu Guard
   enabled`, and state `FWD`.

6. **Negative test:** connect a second switch (or a switch simulator/hub
   configured to emit BPDUs) to the BPDU Guard–protected access port, or
   temporarily enable `spanning-tree bpdufilter disable` removal to allow a
   test BPDU through a lab-only unmanaged switch.

   ```text
   ACCESS-01# show interfaces status err-disabled
   ACCESS-01# show logging | include BPDUGUARD
   ```

   **Expected result:** the port transitions to `err-disabled` and a
   `%SPANTREE-2-BLOCK_BPDUGUARD` (or `%PM-4-ERR_DISABLE`) message appears
   in the log, confirming the unauthorized switch was blocked rather than
   allowed to participate in STP.

7. Re-enable the port after the negative test:

   ```text
   ACCESS-01# interface GigabitEthernet1/0/10
   ACCESS-01(config-if)# shutdown
   ACCESS-01(config-if)# no shutdown
   ```

**Cleanup**

- Remove the test cabling used for the negative test.
- If the lab environment is shared, restore interfaces to their prior
  administrative state and remove lab-only VLANs:

  ```text
  DIST-01(config)# no vlan 10
  DIST-01(config)# no vlan 20
  DIST-01(config)# no vlan 99
  ```

- Save or discard configuration per your lab's standard practice.

## Summary and Completion Checklist

Campus resiliency rests on three cooperating layers: VLAN/trunk hygiene
that prevents Layer 2 leakage, a correctly rooted and guarded spanning-tree
topology that prevents loops without sacrificing convergence speed, and
EtherChannel plus FHRP that turn physically redundant links and switches
into a logically single, fast-failing-over forwarding path.

- [ ] Can configure VLANs, trunks, and explain native-VLAN hygiene.
- [ ] Can explain Rapid PVST+ vs. MST and correctly pin root bridge roles.
- [ ] Can build an LACP EtherChannel and diagnose a suspended member.
- [ ] Can configure HSRP with object tracking and explain GLBP/VRRP
      trade-offs.
- [ ] Can configure and validate StackWise Virtual.
- [ ] Completed the hands-on lab, including the BPDU Guard negative test
      and cleanup.
