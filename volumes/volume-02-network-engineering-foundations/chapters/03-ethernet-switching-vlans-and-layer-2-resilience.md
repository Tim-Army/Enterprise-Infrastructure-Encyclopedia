# Chapter 3: Ethernet Switching, VLANs, and Layer 2 Resilience

## Learning Objectives

- Explain how Ethernet switches learn MAC addresses, build a forwarding
  table, and flood unknown-unicast, broadcast, and multicast traffic.
- Design VLAN segmentation using access and trunk ports, and describe how
  802.1Q tagging carries VLAN membership across a trunk.
- Explain the Spanning Tree Protocol family (802.1D, Rapid STP/802.1w,
  Multiple STP/802.1s) and why loop prevention is mandatory in any
  redundantly cabled Layer 2 topology.
- Configure and reason about link aggregation (802.3ad/LACP) for bandwidth
  and resilience between two switches or a switch and a server.
- Identify common Layer 2 resilience techniques beyond STP, including
  storm control, BPDU Guard, and root guard.
- Diagnose common Layer 2 failure modes: broadcast storms, MAC flapping,
  native VLAN mismatch, and trunk misconfiguration.

## Theory and Architecture

### MAC Learning and the Forwarding Table

An Ethernet switch builds a Content-Addressable Memory (CAM) / MAC address
table by inspecting the source MAC address of every frame it receives and
associating it with the ingress port and VLAN. When a frame arrives destined
for a MAC address already in the table, the switch forwards it out only the
associated port (unicast forwarding). When the destination MAC is not yet
known, or is a broadcast (`FF:FF:FF:FF:FF:FF`) or multicast address, the
switch floods the frame out every port in the same VLAN except the one it
arrived on. This flood-and-learn behavior is what makes an unmanaged flat
Layer 2 network fragile at scale: every unknown-unicast or broadcast frame
consumes bandwidth on every segment in the broadcast domain.

```text
device# show mac address-table vlan 20
Vlan    Mac Address       Type       Ports
----    -----------       ----       -----
20      0050.5600.1a2b    DYNAMIC    Gi1/0/3
20      0050.5600.1a2c    DYNAMIC    Gi1/0/7
20      0050.5600.1a2d    STATIC     Gi1/0/1
```

### VLANs: Access and Trunk Ports

A Virtual LAN (VLAN) is a logical broadcast domain that exists independently
of physical switch or port placement. Two port modes carry VLAN traffic:

- **Access ports** carry traffic for exactly one VLAN and deliver it to the
  end host untagged; the host has no awareness a VLAN exists.
- **Trunk ports** carry traffic for multiple VLANs between switches (or to a
  VLAN-aware host/hypervisor) using 802.1Q tagging, which inserts a 4-byte
  tag containing a 12-bit VLAN ID (1–4094) into the Ethernet frame header so
  the receiving switch can determine which VLAN each frame belongs to.

```text
Untagged 802.3 frame:
[Dest MAC][Src MAC][EtherType][Payload][FCS]

802.1Q tagged frame:
[Dest MAC][Src MAC][0x8100 TPID][TCI: PCP+DEI+VLAN ID][EtherType][Payload][FCS]
```

One VLAN per trunk may be designated the **native VLAN**, whose traffic is
sent untagged for backward compatibility with non-VLAN-aware equipment. A
native VLAN mismatch between the two ends of a trunk — a common
misconfiguration — causes traffic from mismatched VLANs to bleed into the
wrong broadcast domain and is flagged as an error by modern switches via
Cisco Discovery Protocol/Link Layer Discovery Protocol (LLDP) consistency
checks where supported.

### VLAN Trunking and Distribution Protocols

Historically, proprietary protocols such as VTP propagated VLAN databases
automatically across a switched domain; contemporary best practice
generally favors explicit, version-controlled VLAN configuration per switch
(pushed via automation) over automatic database propagation, because
uncontrolled VLAN propagation has caused well-documented outages when a
switch with a higher revision number and an empty or wrong VLAN database
joined a domain. This volume treats explicit, automated VLAN configuration
as the default approach; vendor-specific trunking protocol behavior is
covered in Volume III.

### Spanning Tree Protocol (STP)

Redundant Layer 2 links (added for resilience) create physical loops. A
frame flooded into a loop is re-flooded endlessly, exponentially
multiplying broadcast traffic within milliseconds — a broadcast storm that
can saturate every link in the domain and require a physical intervention
to stop prior to STP's invention. STP (IEEE 802.1D) and its successor Rapid
STP (802.1w, now folded into 802.1D-2004) solve this by electing a **root
bridge** (lowest bridge ID, itself priority + MAC address) and computing a
loop-free tree of **forwarding** ports rooted at that bridge, placing all
other ports that would complete a loop into a **blocking** (or, in RSTP,
**discarding**) state. Multiple Spanning Tree Protocol (MSTP, 802.1s) maps
groups of VLANs to independent spanning-tree instances so that different
VLANs can use different forwarding topologies and load-share across
redundant links instead of leaving one path fully idle.

| Port Role | Description |
| --- | --- |
| Root port | Best path back to the root bridge, one per non-root switch |
| Designated port | Best path onto a given segment, forwards traffic |
| Alternate port (RSTP) / Blocking (STP) | Backup path, does not forward to prevent a loop |
| Backup port (RSTP) | Backup path to a segment the switch already reaches via another port |

RSTP dramatically reduces convergence time versus legacy 802.1D (typically
sub-second versus the 30–50 seconds of listening/learning states in
classic STP) through proposal/agreement handshakes and edge-port fast
transition, making it the practical default in modern deployments.

### Link Aggregation (LACP / 802.3ad)

Where STP prevents loops by disabling redundant paths, Link Aggregation
Control Protocol (LACP, IEEE 802.3ad, now part of 802.1AX) instead bundles
multiple physical links between the same two devices into a single logical
channel, providing both increased bandwidth and resilience (a member link
failure does not take down the channel) without triggering STP
recalculation, because the bundle presents as one logical link to the
spanning tree. Load distribution across bundle members is hash-based
(commonly on source/destination MAC, IP, or Layer 4 port combinations) —
traffic for a single flow always traverses the same member link to
preserve ordering, so aggregate throughput scales with the diversity of
flows, not with any single flow's speed.

### Layer 2 Resilience Add-Ons

- **BPDU Guard** disables a port immediately if it receives a Bridge
  Protocol Data Unit (BPDU), protecting access ports (which should never
  see switch-to-switch STP traffic) from an accidentally or maliciously
  connected switch/hub.
- **Root Guard** prevents a port from being allowed to become a root port,
  protecting the intended root bridge placement from being overridden by a
  rogue or misconfigured switch advertising a superior (lower) bridge ID.
- **Storm Control** rate-limits broadcast, multicast, or unknown-unicast
  traffic per port, containing the blast radius of a storm even if a loop
  briefly forms before STP converges.
- **UniDirectional Link Detection (UDLD)** detects one-way fiber link
  failures that STP's own BPDU exchange might not catch quickly enough to
  prevent a loop.

## Design Considerations

- **Broadcast domain sizing.** Every VLAN's broadcast traffic (ARP, DHCP
  discovery, IPv6 Neighbor Discovery) is delivered to every port in that
  VLAN; oversized VLANs (a `/16` flattened onto Layer 2, for instance)
  degrade performance and enlarge the fault domain of any single Layer 2
  issue. Right-size VLANs to the addressing plan from Chapter 2, not the
  reverse.
- **Redundant topology vs. spanning-tree complexity.** A design that relies
  purely on STP blocking to handle redundancy (a "traditional" hierarchical
  design with STP-blocked uplinks) trades wasted bandwidth on the blocked
  path for architectural simplicity; multi-chassis link aggregation or
  fabric-based designs (introduced conceptually in Chapter 7) instead keep
  all redundant links active, at the cost of additional design and
  operational complexity.
- **Trunk VLAN pruning.** Only allow the VLANs actually required on a given
  trunk (`switchport trunk allowed vlan <list>` in common CLI syntax)
  rather than defaulting to "all VLANs," to reduce unnecessary flooding
  and limit the blast radius of a misconfiguration on a remote switch.
- **Consistent native VLAN and trunk encapsulation** across every trunk in
  the domain, and dedicate the native VLAN to a purpose that carries no
  production data (or disable it) to reduce the impact of tag-stripping
  attacks (see Security section).
- **Where to terminate Layer 2 vs. Layer 3.** Deciding how far VLANs extend
  before being terminated at a Layer 3 boundary (access/distribution vs.
  routed access) materially changes STP's scope, failure domain, and
  convergence behavior — this decision is developed further in Chapter 7.

## Implementation and Automation

### Vendor-Neutral VLAN and Trunk Configuration

```text
device(config)# vlan 20
device(config-vlan)# name Users
device(config)# vlan 30
device(config-vlan)# name Voice

device(config)# interface gigabitethernet1/0/3
device(config-if)# switchport mode access
device(config-if)# switchport access vlan 20
device(config-if)# switchport voice vlan 30
device(config-if)# spanning-tree portfast
device(config-if)# spanning-tree bpduguard enable

device(config)# interface gigabitethernet1/0/24
device(config-if)# switchport mode trunk
device(config-if)# switchport trunk native vlan 999
device(config-if)# switchport trunk allowed vlan 20,30,40
```

### Link Aggregation Configuration

```text
device(config)# interface range gigabitethernet1/0/22-23
device(config-if-range)# channel-group 1 mode active
device(config)# interface port-channel 1
device(config-if)# switchport mode trunk
device(config-if)# switchport trunk allowed vlan 20,30,40
```

### Automating VLAN Deployment

Manually keying VLAN and trunk configuration across dozens of switches is
error-prone; Ansible's network modules apply the same intended-state
definition consistently:

```yaml
# playbook: deploy-access-vlans.yml
- name: Ensure standard access VLANs exist
  hosts: access_switches
  gather_facts: false
  tasks:
    - name: Configure VLAN database
      cisco.ios.ios_vlans:
        config:
          - vlan_id: 20
            name: Users
          - vlan_id: 30
            name: Voice
        state: merged

    - name: Configure access port VLAN and BPDU Guard
      cisco.ios.ios_interfaces:
        config:
          - name: GigabitEthernet1/0/3
            enabled: true
        state: merged
```

```bash
# Dry-run against the intended state before pushing
ansible-playbook deploy-access-vlans.yml --check --diff
```

Regardless of vendor module, the discipline that matters is treating the
VLAN and trunk-allowed list as declared, version-controlled state rather
than a manually maintained runtime configuration — this is what prevents
VLAN sprawl and undocumented trunk pruning drift.

## Validation and Troubleshooting

```text
device# show spanning-tree vlan 20
device# show interfaces trunk
device# show etherchannel summary
device# show mac address-table count vlan 20
```

| Symptom | Likely Cause | Diagnostic |
| --- | --- | --- |
| Intermittent network-wide slowness, high CPU on switches | Broadcast storm from an accidental Layer 2 loop | `show spanning-tree`, check for ports flapping between blocking/forwarding |
| A MAC address "moves" rapidly between two ports in logs | Loop or duplicate cabling causing MAC flapping | `show mac address-table` repeated samples, correlate with `show spanning-tree` topology changes |
| Two switches disagree on which VLAN a trunk's untagged traffic belongs to | Native VLAN mismatch | Compare `switchport trunk native vlan` on both ends |
| A newly added redundant uplink causes an outage instead of adding resilience | STP not yet converged, or BPDU Guard/loop protection misconfigured | `show spanning-tree`, check port states before removing the old link |
| LACP bundle will not come up | Mismatched channel mode (active/active required, or active/passive) | `show etherchannel summary`, confirm both ends use `active` or one `active`/one `passive` |
| Host cannot reach anything despite correct access VLAN | Port is administratively down or in `err-disabled` state (commonly BPDU Guard triggered) | `show interface status`, look for `err-disabled` |

A broadcast storm is the signature Layer 2 failure: switch CPU utilization
spikes, port LEDs indicate near-constant activity, and `show
spanning-tree` reveals a topology change count incrementing rapidly.
Immediate mitigation is to physically or administratively disable the
suspected looped link while root cause (usually an unauthorized switch/hub
connection, or an STP feature disabled during a previous change) is
identified.

## Security and Best Practices

- Enable BPDU Guard on all access ports and Root Guard on ports facing
  switches that should never become the STP root, to prevent both
  accidental and malicious topology manipulation.
- Disable unused switch ports or place them in a dedicated, unrouted
  "quarantine" VLAN, and disable auto-negotiation of trunking
  (dynamic trunk negotiation protocols) on access ports to prevent VLAN
  hopping attacks, where an attacker forces a port into trunk mode to gain
  access to VLANs beyond the intended one.
- Never use VLAN 1 (or any factory-default VLAN) as the native VLAN or as a
  production data VLAN; double-tagging VLAN-hopping attacks specifically
  exploit a native VLAN that matches an attacker-reachable access VLAN.
- Apply storm control thresholds on access ports to contain the blast
  radius of both accidental loops and deliberate broadcast-flood attacks
  before STP fully converges.
- Enforce port security (limiting the number of learned MAC addresses per
  access port) to reduce the impact of MAC flooding attacks against the
  switch's forwarding table, which can force a switch into a fail-open
  flooding state functionally similar to a hub.

## References and Knowledge Checks

**References**

- [IEEE 802.1Q — Bridges and Bridged Networks (VLAN Tagging)](https://standards.ieee.org/ieee/802.1Q/6844/)
- [IEEE 802.1D-2004 — MAC Bridges (includes RSTP)](https://standards.ieee.org/ieee/802.1D/3646/)
- [IEEE 802.1AX — Link Aggregation](https://standards.ieee.org/ieee/802.1AX/7195/)
- [RFC 3069 — VLAN Aggregation for Efficient IP Address Allocation](https://www.rfc-editor.org/rfc/rfc3069)

**Knowledge Checks**

1. Explain why an unknown-unicast frame is flooded rather than dropped, and
   what condition causes a switch to stop flooding a given destination.
2. Why does a native VLAN mismatch between two trunk ports cause traffic to
   appear on the wrong VLAN instead of simply failing?
3. Compare how STP and LACP each respond to a redundant physical link
   between two switches, and why only one of them keeps both links actively
   forwarding traffic.
4. What is the operational risk of leaving BPDU Guard disabled on access
   ports in an area with public physical access?
5. A newly connected LACP bundle stays down. What two channel-mode
   combinations will successfully negotiate, and which combination never
   will?
6. Why is VLAN 1 a poor choice for a trunk's native VLAN in a security-
   conscious design?

## Hands-On Lab

**Objective.** Build a two-VLAN, trunk-connected topology using Linux
bridges with 802.1Q VLAN filtering, confirm broadcast-domain isolation, and
observe how enabling the bridge's built-in STP prevents a loop that would
otherwise cause a storm.

**Prerequisites**

- A Linux host with `sudo` access and `iproute2` (the `ip` and `bridge`
  commands).
- Familiarity with Chapter 2's network namespace conventions.

**Lab Steps**

1. Create two host namespaces and one "switch" namespace, and a
   VLAN-aware Linux bridge inside the switch namespace:

   ```bash
   sudo ip netns add ns-host-a
   sudo ip netns add ns-host-b
   sudo ip netns add ns-switch

   sudo ip netns exec ns-switch ip link add br0 type bridge vlan_filtering 1
   sudo ip netns exec ns-switch ip link set br0 up
   ```

2. Connect both hosts to the bridge with veth pairs, and configure the
   bridge side of each link as an access port tagged internally to VLAN 20:

   ```bash
   sudo ip link add veth-a type veth peer name veth-a-br
   sudo ip link add veth-b type veth peer name veth-b-br
   sudo ip link set veth-a netns ns-host-a
   sudo ip link set veth-b netns ns-host-b
   sudo ip link set veth-a-br netns ns-switch
   sudo ip link set veth-b-br netns ns-switch

   sudo ip netns exec ns-switch ip link set veth-a-br master br0
   sudo ip netns exec ns-switch ip link set veth-b-br master br0
   sudo ip netns exec ns-switch ip link set veth-a-br up
   sudo ip netns exec ns-switch ip link set veth-b-br up

   # Access-port behavior: untag on egress, accept only VLAN 20 (PVID 20)
   sudo ip netns exec ns-switch bridge vlan add dev veth-a-br vid 20 pvid untagged
   sudo ip netns exec ns-switch bridge vlan add dev veth-b-br vid 20 pvid untagged
   sudo ip netns exec ns-switch bridge vlan del dev veth-a-br vid 1
   sudo ip netns exec ns-switch bridge vlan del dev veth-b-br vid 1
   ```

3. Address and bring up both host interfaces, then confirm reachability
   across the simulated VLAN 20 access ports:

   ```bash
   sudo ip netns exec ns-host-a ip addr add 10.20.0.2/24 dev veth-a
   sudo ip netns exec ns-host-a ip link set veth-a up
   sudo ip netns exec ns-host-a ip link set lo up

   sudo ip netns exec ns-host-b ip addr add 10.20.0.3/24 dev veth-b
   sudo ip netns exec ns-host-b ip link set veth-b up
   sudo ip netns exec ns-host-b ip link set lo up

   sudo ip netns exec ns-host-a ping -c 3 10.20.0.3
   ```

   **Expected result:** 3 packets transmitted, 3 received, 0% loss —
   confirming Layer 2 connectivity through the simulated access switch.

4. Confirm broadcast-domain isolation by adding a third host on a
   different VLAN (VLAN 30) attached to the same bridge, and show that it
   cannot reach hosts on VLAN 20 despite sharing the same physical bridge:

   ```bash
   sudo ip netns add ns-host-c
   sudo ip link add veth-c type veth peer name veth-c-br
   sudo ip link set veth-c netns ns-host-c
   sudo ip link set veth-c-br netns ns-switch
   sudo ip netns exec ns-switch ip link set veth-c-br master br0
   sudo ip netns exec ns-switch ip link set veth-c-br up
   sudo ip netns exec ns-switch bridge vlan add dev veth-c-br vid 30 pvid untagged
   sudo ip netns exec ns-switch bridge vlan del dev veth-c-br vid 1

   sudo ip netns exec ns-host-c ip addr add 10.20.0.4/24 dev veth-c
   sudo ip netns exec ns-host-c ip link set veth-c up
   sudo ip netns exec ns-host-c ip link set lo up

   sudo ip netns exec ns-host-c ping -c 3 -W 1 10.20.0.2
   ```

   **Expected result:** 100% packet loss — VLAN 30 is a separate broadcast
   domain from VLAN 20 even though both attach to the same bridge,
   demonstrating VLAN-based segmentation.

5. Observe the bridge's MAC forwarding table populated by the learning
   process described in this chapter:

   ```bash
   sudo ip netns exec ns-switch bridge fdb show br br0 | grep -v permanent
   ```

   **Expected result:** dynamic entries for the MAC addresses of
   `veth-a`, `veth-b`, and `veth-c`, each associated with its ingress port
   and learned VLAN.

**Negative Test**

Add a second link between `ns-host-a` and the switch bridge (simulating a
redundant, but looped, cable) with STP disabled, and observe the resulting
duplicate-frame/loop symptom; then enable the bridge's STP and confirm the
loop is broken.

```bash
# Add a second, looping connection from host A back to the same bridge
sudo ip link add veth-a2 type veth peer name veth-a2-br
sudo ip link set veth-a2 netns ns-host-a
sudo ip link set veth-a2-br netns ns-switch
sudo ip netns exec ns-switch ip link set veth-a2-br master br0
sudo ip netns exec ns-switch bridge vlan add dev veth-a2-br vid 20 pvid untagged
sudo ip netns exec ns-switch bridge vlan del dev veth-a2-br vid 1
sudo ip netns exec ns-host-a ip link set veth-a2 up
sudo ip netns exec ns-switch ip link set veth-a2-br up

# Without STP, this creates a genuine bridging loop; observe rapidly
# growing broadcast traffic with a short capture, then stop it immediately
sudo timeout 3 ip netns exec ns-switch tcpdump -i br0 -nn broadcast or multicast | wc -l

# Now enable STP on the bridge and confirm it blocks the redundant path
sudo ip netns exec ns-switch ip link set br0 type bridge stp_state 1
sleep 5
sudo ip netns exec ns-switch bridge -d link show | grep -E "veth-a-br|veth-a2-br"
```

**Expected result:** the pre-STP capture shows a rapidly climbing broadcast
frame count characteristic of a loop; after enabling `stp_state 1` and
allowing convergence, `bridge -d link show` reports one of the two links
to host A in a `state blocking` (or `discarding`) state while the other
remains `state forwarding`, confirming STP has broken the loop exactly as
described in this chapter's theory section.

**Cleanup**

```bash
sudo ip netns del ns-host-a
sudo ip netns del ns-host-b
sudo ip netns del ns-host-c
sudo ip netns del ns-switch
```

## Summary and Completion Checklist

This chapter covered Ethernet's flood-and-learn switching behavior, VLAN
segmentation via access and trunk ports with 802.1Q tagging, loop
prevention through Spanning Tree Protocol and its faster successors, and
link aggregation as a resilience mechanism that keeps redundant links
active rather than blocked. The hands-on lab built a working VLAN-segmented
topology and reproduced both a broadcast-domain isolation test and a real
Layer 2 loop, then resolved the loop with STP — the same fault class and
fix an enterprise network engineer encounters on physical hardware.

**Completion Checklist**

- [ ] Can explain MAC learning, flooding, and the forwarding table
      lifecycle.
- [ ] Can configure access and trunk ports, including native VLAN and
      allowed-VLAN pruning, in vendor-neutral terms.
- [ ] Can explain root bridge election and port role assignment in STP/RSTP.
- [ ] Can distinguish what LACP solves from what STP solves.
- [ ] Built and validated a VLAN-segmented, trunk-connected lab topology.
- [ ] Reproduced a Layer 2 loop and confirmed STP resolves it.
- [ ] Can list at least three Layer 2 hardening controls (BPDU Guard, Root
      Guard, storm control, port security) and what each prevents.
