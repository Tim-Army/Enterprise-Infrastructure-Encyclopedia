# Chapter 06: Router SRG Requirement Labs

## Learning Objectives

- Prove each Router SRG requirement in the crosswalk on the Chapter 999 lab, with a positive and a negative test, or confirm and document why FortiSwitch cannot meet it.
- Configure interface hygiene, ACL information-flow control and drop logging, perimeter filtering, and control-plane protection on FortiSwitchOS.
- Authenticate OSPF and VRRP, and protect BGP sessions and routes with keys, TTL security, prefix lists, AS-path checks, and maximum prefixes.
- Separate routing domains with VRFs and limit PIM-SSM to the interfaces that need it.
- Document the router requirements that belong to roles FortiSwitch cannot take: MPLS, provider edge, rendezvous point, and MSDP.
- Keep the evidence for each lab so it can support an assessment.

## Theory and Architecture

The Router SRG applies to a device that routes packets between networks. A FortiSwitch with the Advanced Features License routes IPv4 and IPv6, runs OSPF, BGP, RIP, IS-IS, VRRP, PIM-SSM, VRFs, and VXLAN, so the Router SRG applies to it wherever it routes. It is the largest family in the crosswalk (92 requirements) and the one where FortiSwitch meets the least: 46 requirements have a setting or a procedure behind them, and 46 describe features that FortiSwitchOS does not have, such as MPLS, VPLS, a rendezvous point, and MSDP.

The first ten labs prove the 46 requirements FortiSwitch can meet. The last six are gap labs for the other 46: each one proves that the setting is absent, applies the nearest compensating control where one exists, and records the disposition so an assessor can see what was tested.

All labs use the routed links and peers from [Chapter 999](999-shared-lab-infrastructure.md): L1 to L5, `rtr-peer-1` (AS 65202), `rtr-peer-2` (AS 65203), and the loopbacks. The Advanced Features License must be installed on both switches.

### Requirements and labs

The crosswalk lists 92 distinct Router SRG requirements. Each one has a lab or a gap lab in this chapter, so none is left without a test.

| Lab | Requirements | Kind |
| --- | --- | --- |
| 6.1 | 7 | Requirement lab: Interface and IPv6 hygiene |
| 6.2 | 4 | Requirement lab: ACL information-flow control and logging of dropped packets |
| 6.3 | 11 | Requirement lab: Perimeter filtering: default deny, bogons, source validation, and management traffic |
| 6.4 | 2 | Requirement lab: Control-plane protection and QoS |
| 6.5 | 2 | Requirement lab: Routing protocol and gateway redundancy authentication |
| 6.6 | 12 | Requirement lab: BGP session and route protection |
| 6.7 | 1 | Requirement lab: VRF separation |
| 6.8 | 3 | Requirement lab: Multicast routing: PIM interfaces, neighbor filters, and boundaries |
| 6.9 | 2 | Requirement lab: Hashed routing authentication with key lifetimes of 180 days or less |
| 6.10 | 2 | Requirement lab: Turn off call-home and drop fragmented ICMP |
| 6.11 | 7 | Gap lab: Gaps: ICMP and ARP behavior, auxiliary port, forwarding architecture, and IP options |
| 6.12 | 7 | Gap lab: Gaps: IPv6 extension-header filtering |
| 6.13 | 5 | Gap lab: Gaps: MPLS, LDP, and RSVP-TE |
| 6.14 | 13 | Gap lab: Gaps: provider-edge L3VPN, L2VPN, VPLS, and provider QoS roles |
| 6.15 | 8 | Gap lab: Gaps: rendezvous-point and designated-router multicast controls |
| 6.16 | 6 | Gap lab: Gaps: MSDP |

A **requirement lab** configures the FortiSwitch setting, proves it with a positive test, and proves the control with a negative test. A **gap lab** covers requirements that FortiSwitch cannot meet (alignment *Not supported* or *Not applicable* in the crosswalk): it proves the setting is absent, applies the nearest compensating control, and records the disposition and residual risk.

## Design Considerations

- **Use the peers to attack.** The router requirements are about what a neighbor can do to the switch. `rtr-peer-1` and `rtr-peer-2` announce bad routes, send forged packets, and exceed limits, so each negative test comes from a peer.
- **One protocol at a time.** Enable only the routing protocol a lab tests and remove it afterward, so a failed test is not mixed with another protocol.
- **Pick the switch that supports the feature.** uRPF is not supported on the FS-648F-FPOE, so the source-validation tests run on the FS-2048F.
- **Generate keys per lab.** Routing keys come from Chapter 999's rule: one key per lab, never reused.
- **Gap labs prove absence.** A requirement that FortiSwitch cannot meet is shown by the missing CLI branch and the missing Feature Matrix entry, not by assertion.
- **Name the disposition.** Each gap lab ends with a recorded disposition: Does Not Meet with a mitigation, or Not Applicable with the reason.

## Implementation and Automation

Each lab lists commands in the order to enter them. Commands come from the crosswalk workbook (FortiSwitchOS 7.6.7 syntax) with lab values substituted: loopbacks `10.201.250.<host>/32`, peer links L1 to L5 from Chapter 999, and AS numbers 65201 to 65203. Where the workbook row reads "See ... Worksheet", the lab says to use the worksheet's ACL or interface rows for that ID.

On the peers, use FRR (`vtysh`) or a FortiGate-VM to announce test prefixes. Save evidence in `evidence/<lab>/<date>/` on `admin-201`.

## Validation and Troubleshooting

Before each lab, confirm the links: `execute ping 10.201.200.1` for L1 and the same for the others. After each lab, remove the routing configuration and restore the baseline.

| Symptom | Cause | Fix |
| --- | --- | --- |
| A BGP session stays Idle | The peer address, AS, or key differs, or the link is down | Check `get router info bgp summary` and the link |
| A rejected prefix still appears | The prefix list is not bound inbound on the neighbor | Bind it with `prefix-list-in` and reset the session softly |
| The OSPF adjacency never forms | Authentication keys differ or the keys have expired | Match the key ID and key, and check the key lifetimes |
| uRPF command is rejected | The model does not support it | Use the FS-2048F |
| PIM shows no neighbor | PIM is not enabled on both ends, or the link is not up | Enable PIM-SSM on both interfaces |

## Security and Best Practices

- Keep the lab routing separate from any production network, and never announce lab prefixes outward.
- Use strong, unique keys for each protocol and delete them after the lab.
- Start every gap lab by capturing the evidence of absence, before you apply a mitigation.
- Record which switch and release produced each result.
- Treat a negative test that fails to block as a finding.

## References and Knowledge Checks

**References:**

- [Chapter 01](01-fortiswitch-feature-version-and-srg-map.md), [Chapter 02](02-fortiswitch-and-cisco-catalyst-switch-stig-crosswalk.md), and [Chapter 03](03-cisco-nx-os-switch-and-fortiswitch-stig-crosswalk.md) for the rows these labs prove.
- [Chapter 999](999-shared-lab-infrastructure.md) for the routed links, peers, and baseline.
- Router SRG (DISA, V5R2 as compared with a third-party mirror; confirm against DISA's own file).
- FortiSwitchOS 7.6.7 CLI Reference and Administration Guide (Fortinet Document Library).
- [Volume CLXXII, Chapter 31](../../volume-172-disa-srgs-and-stigs/chapters/31-cisco-products-stigs-and-srg-mapping.md) for the Cisco router STIGs.

**Knowledge checks:**

1. Why do the BGP negative tests come from the peers and not from the switch?
2. What does TTL security (GTSM) protect a BGP session from?
3. Why does the uRPF test run on the FS-2048F?
4. How does a gap lab prove that a setting is absent?
5. What is the difference between a Does Not Meet and a Not Applicable disposition?

## Hands-On Lab

**Shared prerequisites.** The infrastructure from Chapter 999 (Labs 999.1 to 999.6) including the routed links L1 to L5 and both routing peers, the Advanced Features License on both switches, and the `baseline-201` snapshot. On the peers: FRR with `vtysh`, `scapy`, and `tcpdump`. **Cost:** none beyond the Chapter 999 lab.

### Lab 6.1 — Interface and IPv6 hygiene

**Goal.** Show that unused Layer 3 interfaces are down, ICMP redirects and directed broadcasts are not used, IPv6 advertisements carry a safe hop limit, site-local addresses are absent, zero-touch provisioning is off, and LLDP is off on external ports.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-NET-000019-RTR-000007` | III | Disable inactive Layer 3 interfaces | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p243 |
| `SRG-NET-000362-RTR-000115` | II | Disable ICMP redirect messages on external interfaces | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p242 |
| `SRG-NET-000362-RTR-000112` | III | Disable IP directed broadcast on all interfaces | Partial | FortiSwitchOS 7.6.7 CLI Reference p104 |
| `SRG-NET-000512-RTR-000012` | III | Advertise a hop limit of at least 32 in IPv6 router advertisements | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p243 |
| `SRG-NET-000512-RTR-000013` | II | Do not use IPv6 site-local unicast addresses | By procedure | — p— |
| `SRG-NET-000362-RTR-000109` | II | Disable zero-touch deployment features on an operational network | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p230 |
| `SRG-NET-000364-RTR-000111` | III | Perimeter: disable LLDP on external interfaces | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p157 |

**Uses.** `sw-648f-1` with a routed link (L1) to `rtr-peer-1`, `admin-201`, and a capture on the peer.

**Configure.**

1. Shut down a Layer 3 interface that has no neighbor.

   ```text
   config system interface
       edit <UNUSED_L3_INTERFACE>
           set status down
   end
   ```

2. Turn off ICMP redirects on the external interface.

   ```text
   config system interface
       edit <EXTERNAL_INTERFACE>
           set icmp-redirect disable
   end
   ```

3. Block directed broadcasts with an ingress ACL.

   ```text
   config switch acl ingress
       edit <ID>
           set ingress-interface <PORT_EP1>
           config classifier
               set dst-ip-prefix <SUBNET_BROADCAST_IP> <HOST_MASK>
           end
           config action
               set drop enable
           end
   end
   ```

4. Set the IPv6 router-advertisement hop limit to at least 32 on the interface.

   ```text
   config system interface
       edit <INTERFACE>
           config ipv6
               set ip6-address <IPV6_ADDRESS>/<PREFIX_LENGTH> set ip6-send-adv enable
               set ip6-hop-limit 64
           end
   end
   ```

5. Turn off zero-touch provisioning features.

   ```text
   config system flan-cloud
       set status disable
   end
   config switch auto-network
       set status disable
   end
   ```

6. Turn off LLDP on the external port.

   ```text
   config switch physical-port
       edit <EXTERNAL_PORT>
           set lldp-status disable
   end
   ```

7. For site-local addresses (`SRG-NET-000512-RTR-000013`, by procedure): list every IPv6 address on the switch with `get system interface` and confirm none is in `fec0::/10`. The lab plan uses only `fd00:db8:201::/112`.

**Positive test.** The unused interface is down. `tcpdump` on `rtr-peer-1` shows no LLDP frames from the external port. Advertised IPv6 router advertisements, if sent, carry hop limit 32 or more. No address in `fec0::/10` is configured.

**Negative test.** Send a packet to the directed-broadcast address of the lab subnet from `rtr-peer-1`: the ACL drops it and the counter increments. Send a packet that would normally trigger a redirect: no redirect is sent. Attempt to re-enable the unused interface by sending traffic to it: no neighbor comes up.

**Evidence.** The interface and ACL configuration, the capture files on the peer, and the address list.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

### Lab 6.2 — ACL information-flow control and logging of dropped packets

**Goal.** Show that an ACL controls what may flow through the router, and that every packet the ACL drops is counted and recorded with where and from whom.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-NET-000018-RTR-000001` | II | Enforce approved information flow control on routed traffic | Same requirement | FortiSwitch 7.6.7 Feature Matrix p2; FortiSwitchOS 7.6.7 CLI Reference p101 |
| `SRG-NET-000078-RTR-000001` | III | Log all packets dropped by interface ACLs | Partial | FortiSwitchOS 7.6.7 CLI Reference p105 |
| `SRG-NET-000076-RTR-000001` | II | Record where each dropped-packet event occurred | Partial | FortiSwitchOS 7.6.7 CLI Reference p105 |
| `SRG-NET-000077-RTR-000001` | II | Record the source of each dropped-packet event | Partial | FortiSwitchOS 7.6.7 CLI Reference p105 |

**Uses.** `sw-648f-1`, a sender on segment 42 (`attacker-201`), a destination on segment 10, `syslog-201a`.

**Configure.**

1. Create an ingress ACL that permits the approved flow and drops the rest, with counting on.

   ```text
   config switch acl ingress
       edit <ID>
           set ingress-interface <PORT_EP1>
           config classifier
               set src-ip-prefix <IP> <MASK>
           end
           config action
               set drop enable
           end
   end
   ```

2. Count and log the drops.

   ```text
   config switch acl ingress
       edit <ID>
           config action
               set drop enable
               set count enable
           end
   end
   get switch acl counters ingress
   ```

3. Add `set count enable` to the drop action so the record names the ingress port (where) and read the source address from the counters and a capture (who). The FortiSwitch ACL counter holds the packet count, so use a mirror port or the syslog message for the packet details (`SRG-NET-000076-RTR-000001` and `SRG-NET-000077-RTR-000001`).

**Positive test.** Send the approved flow: it passes and the permit counter increments.

**Negative test.** Send a denied flow: it is dropped, the drop counter increments, and the log or capture records the ingress port and the source address. Remove the drop count and repeat: the counter stays at zero, which proves the setting makes the record.

**Evidence.** The ACL configuration, the counters before and after, and the capture or log with the source and port.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

### Lab 6.3 — Perimeter filtering: default deny, bogons, source validation, and management traffic

**Goal.** Show that the external interface denies by default, allows only authorized flows, drops bogon and spoofed sources, blocks outbound management traffic, suppresses IPv6 advertisements outward, and that management uses only the management interface.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-NET-000202-RTR-000001` | I | Perimeter: deny traffic by default and allow by exception | Partial | FortiSwitchOS 7.6.7 CLI Reference p104 |
| `SRG-NET-000019-RTR-000002` | II | Perimeter: control traffic between interconnected networks by policy | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p104 |
| `SRG-NET-000364-RTR-000109` | II | Perimeter: route inbound traffic only from authorized sources to authorized destinations | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p104 |
| `SRG-NET-000364-RTR-000110` | II | Perimeter: block inbound packets with bogon source addresses | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p104 |
| `SRG-NET-000205-RTR-000014` | I | Perimeter: drop outbound packets with illegitimate source addresses (egress filter or uRPF) | Same requirement | FortiSwitchOS 7.6.7 CLI Reference p243 |
| `SRG-NET-000205-RTR-000003` | II | Perimeter: filter traffic into the enclave as DoD Instruction 8551.01 requires | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p111 |
| `SRG-NET-000205-RTR-000004` | II | Perimeter: filter ingress traffic inbound on the external interface | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p104 |
| `SRG-NET-000205-RTR-000005` | II | Perimeter: filter egress traffic inbound on the internal interface | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p243 |
| `SRG-NET-000364-RTR-000113` | II | Perimeter: block all outbound management traffic | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p111 |
| `SRG-NET-000512-RTR-000014` | II | Perimeter: suppress IPv6 router advertisements on external interfaces | Same requirement | FortiSwitchOS 7.6.7 CLI Reference p171; FortiSwitchOS 7.6.7 CLI Reference p243 |
| `SRG-NET-000205-RTR-000012` | II | Permit management traffic only through the out-of-band management interface | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p244 |

**Uses.** `sw-2048f-1` with L3 to `rtr-peer-2` as the external side (uRPF is not supported on the FS-648F-FPOE), `attacker-201` on segment 42, `admin-201`. Workbook prerequisites: P9, P10 (P9 A switch model series that supports the feature; P10 A management interface with an address: the management port or a management SVI on a dedicated VLAN).

**Configure.**

1. Deny by default on the external interface and permit by exception.

   ```text
   config switch acl ingress
       edit <ID>
           set ingress-interface <EXTERNAL_PORT>
           config action
               set drop enable
           end
   end
   ```

2. Control traffic between interconnected networks by policy.

   ```text
   config switch acl ingress
       edit <ID>
           set ingress-interface <EXTERNAL_PORT>
           config classifier
               set src-ip-prefix <SOURCE> <MASK>
               set dst-ip-prefix <DESTINATION> <MASK>
           end
           config action
               set drop enable
           end
   end
   ```

3. Accept inbound traffic only from authorized sources to authorized destinations.

   ```text
   config switch acl ingress
       edit <ID>
           set ingress-interface <EXTERNAL_PORT>
           config classifier
               set src-ip-prefix <SOURCE> <MASK>
               set dst-ip-prefix <DESTINATION> <MASK>
               set service <SERVICE>
           end
   end
   ```

4. Drop bogon sources.

   ```text
   config switch acl ingress
       edit <ID>
           set ingress-interface <EXTERNAL_PORT>
           config classifier
               set src-ip-prefix <BOGON_PREFIX> <MASK>
           end
           config action
               set drop enable
           end
   end
   ```

5. Filter ingress traffic to the enclave by service.

   ```text
   config switch acl service custom
       edit <SERVICE>
           set protocol TCP/UDP/SCTP
           set tcp-portrange <PORT_EP1>
   end
   config switch acl ingress
       edit <ID>
           set ingress-interface <EXTERNAL_PORT>
           config classifier
               set service <SERVICE>
           end
   end
   ```

6. Filter inbound traffic on the external interface.

   ```text
   config switch acl ingress
       edit <ID>
           set ingress-interface <EXTERNAL_PORT>
           config classifier
               set src-ip-prefix <SOURCE> <MASK>
           end
           config action
               set drop enable
           end
   end
   ```

7. Check the source address on the internal interface (strict) to drop spoofed egress traffic.

   ```text
   config system interface
       edit <INTERNAL_INTERFACE>
           set src-check strict
   end
   ```

8. For the rows that read "See ... Worksheet" in the workbook (outbound management, IPv6 router advertisements, and management only on the out-of-band interface), apply the ACL or interface setting named in the workbook's worksheet rows for those IDs and confirm with the tests below.

**Positive test.** An authorized flow from the external peer to a segment 10 service passes. SSH to the management SVI works only from `admin-201` over segment 30 or the out-of-band port.

**Negative test.** From `rtr-peer-2`, send packets with source addresses `10.0.0.1`, `192.168.1.1`, and `127.0.0.1`: each is dropped. From `attacker-201`, send a packet with a spoofed source outside segment 42: the source check drops it. Try SSH to the switch from the external side and from a user VLAN: refused. Try a management connection leaving the switch toward the external side: blocked. Capture on the external link: no IPv6 router advertisements leave.

**Evidence.** The ACL and interface configuration, counters for each dropped class, and the captures.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

### Lab 6.4 — Control-plane protection and QoS

**Goal.** Show that the router limits control-plane resource use, and that a QoS policy keeps a flood from starving priority traffic.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-NET-000362-RTR-000110` | I | Protect the control plane against denial-of-service attacks | Partial | FortiSwitchOS 7.6.7 CLI Reference p69; FortiSwitchOS 7.6.7 CLI Reference p69, 174 |
| `SRG-NET-000193-RTR-000112` | II | Enforce a QoS policy that limits packet-flooding denial-of-service attacks | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p168 |

**Uses.** `sw-648f-1`, `rtr-peer-1` as an OSPF neighbor sending many routes, a traffic generator, and `flow-201`. Workbook prerequisites: P8, P9 (P8 FortiSwitch Advanced Features license; P9 A switch model series that supports the feature).

**Configure.**

1. Limit the OSPF database so an overflow cannot exhaust memory.

   ```text
   config router ospf
       set database-overflow enable
       set database-overflow-max-external-lsa <LSAS>
   end
   ```

2. Apply a weighted QoS policy on the uplink.

   ```text
   config switch qos qos-policy
       edit <POLICY>
           set schedule weighted
   end
   config switch interface
       edit <PORT_TRUNK>
           set qos-policy <POLICY>
   end
   ```

**Positive test.** The OSPF neighbor comes up with a normal number of routes. Priority traffic keeps its throughput while bulk traffic is also sent.

**Negative test.** Inject more routes than the overflow limit from the peer: the switch enters the overflow state, logs it, and stays responsive (check CPU with `get system performance status`). Without the QoS policy, flood bulk traffic and show priority traffic degrading; with it, show priority traffic preserved.

**Evidence.** The OSPF overflow log, CPU readings, and throughput results with and without the policy.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

### Lab 6.5 — Routing protocol and gateway redundancy authentication

**Goal.** Show that routing neighbors and VRRP peers must authenticate, and that keys have lifetimes.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-NET-000168-RTR-000078` | II | Authenticate routing protocols with FIPS 198-1 algorithms and keys with lifetimes of no more than 180 days | Partial | FortiSwitchOS 7.6.7 CLI Reference p35; FortiSwitchOS 7.6.7 CLI Reference p37 |
| `SRG-NET-000230-RTR-000001` | II | The router must be configured to implement message authentication for all control plane protocols. | feature row (no Cisco rule) | FortiSwitchOS 7.6.7 CLI Reference p244 |

**Uses.** `sw-648f-1`, `sw-2048f-1`, `rtr-peer-1`, `ntp-201a` (P5) for key lifetimes, Advanced Features License (P8). Workbook prerequisites: P5, P8, P9, P11 (P5 Authoritative NTP servers and their authentication keys; P8 FortiSwitch Advanced Features license; P9 A switch model series that supports the feature; P11 Routing protocol configured with its neighbors).

**Configure.**

1. Authenticate OSPF with keys that have lifetimes, on L5.

   ```text
   config router ospf
       config interface
           edit <INTERFACE>
               set authentication md5
               config md5-keys
                   edit 1
                       set key <KEY>
               end
       end
   end
   config router key-chain
       edit lab-keys
           config key
               edit 1
                   set key-string <KEY>
                   set accept-lifetime <START> <END>
                   set send-lifetime <START> <END>
           end
   end
   ```

2. Configure the VRRP group with its authentication-related settings on the segment 30 interface.

   ```text
   config system interface
       edit <INTERFACE>
           config vrrp
               edit <VRID>
                   set vrip <IP>
                   set priority <PRIORITY>
           end
   end
   ```

**Positive test.** The OSPF adjacency forms with matching keys. `get router info ospf neighbor` shows Full. The VRRP backup sees the master.

**Negative test.** Change the key on one end: the adjacency drops and the log names the authentication failure. Let a key expire (set its stop time in the past): the adjacency drops. Note that VRRP authentication on FortiSwitchOS may be limited to the VRRP version in use; record exactly what the switch supports for `SRG-NET-000230-RTR-000001`.

**Evidence.** Neighbor state before and after each change, and the authentication-failure log lines.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

### Lab 6.6 — BGP session and route protection

**Goal.** Show that BGP sessions use a loopback source, TTL security, and a unique key per peer, and that the switch rejects bogon, own-AS, wrongly originated, too-specific, and too-many prefixes and advertises only what it should.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-NET-000362-RTR-000124` | III | BGP: enable the Generalized TTL Security Mechanism (GTSM) | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p35 |
| `SRG-NET-000230-RTR-000002` | II | BGP: use a unique key for each autonomous system peered with | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p37 |
| `SRG-NET-000018-RTR-000002` | II | BGP: reject inbound advertisements of bogon prefixes | Same requirement | FortiSwitchOS 7.6.7 CLI Reference p37; FortiSwitchOS 7.6.7 CLI Reference p83 |
| `SRG-NET-000018-RTR-000003` | II | BGP: reject inbound advertisements of the local AS's own prefixes | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p83 |
| `SRG-NET-000018-RTR-000004` | II | BGP: reject advertisements from a CE for prefixes not allocated to that customer | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p35 |
| `SRG-NET-000018-RTR-000005` | II | BGP: advertise only customer and local AS prefixes | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p83 |
| `SRG-NET-000205-RTR-000006` | II | BGP: do not advertise IP core prefixes | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p83 |
| `SRG-NET-000018-RTR-000006` | III | BGP: reject routes whose AS_PATH does not start with the peer's AS | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p36 |
| `SRG-NET-000018-RTR-000010` | III | BGP: reject CE routes whose originating AS does not belong to that customer | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p33 |
| `SRG-NET-000362-RTR-000117` | II | BGP: limit the number of prefixes accepted from each peer | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p35 |
| `SRG-NET-000362-RTR-000118` | III | BGP: accept no inbound prefixes longer than /24 | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p83 |
| `SRG-NET-000512-RTR-000001` | III | BGP: source iBGP sessions from a loopback address | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p243 |

**Uses.** `sw-648f-1` (AS 65201), `rtr-peer-1` (AS 65202), `rtr-peer-2` (AS 65203), the Advanced Features License (P8), loopbacks from Chapter 999. Workbook prerequisites: P8, P9, P11 (P8 FortiSwitch Advanced Features license; P9 A switch model series that supports the feature; P11 Routing protocol configured with its neighbors).

**Configure.**

1. Source iBGP from the loopback.

   ```text
   config system interface
       edit <LOOPBACK>
           set type loopback
           set ip <LOOPBACK_IP> <HOST_MASK>
   end
   config router bgp
       config neighbor
           edit <IBGP_PEER>
               set update-source <LOOPBACK>
       end
   end
   ```

2. Enable TTL security and a unique key for the eBGP peer.

   ```text
   config router bgp
       config neighbor
           edit <EBGP_PEER>
               set ebgp-ttl-security-hops 1
       end
   end
   ```

3. Set the unique key.

   ```text
   config router bgp
       config neighbor
           edit <EBGP_PEER>
               set password <UNIQUE_KEY>
       end
   end
   ```

4. Reject bogon and own-AS prefixes with a prefix list.

   ```text
   config router prefix-list
       edit PREFIX_FILTER
           config rule
               edit 1
                   set action deny
                   set prefix <BOGON_PREFIX> <MASK>
                   set le 32
           end
   end
   config router bgp
       config neighbor
           edit <EBGP_PEER>
               set prefix-list-in PREFIX_FILTER
       end
   end
   ```

5. Reject prefixes not allocated to the customer edge peer.

   ```text
   config router bgp
       config neighbor
           edit <CE_PEER>
               set prefix-list-in <CUSTOMER_PREFIX_LIST>
       end
   end
   ```

6. Advertise only customer and local prefixes, and never the core.

   ```text
   config router prefix-list
       edit CE_PREFIX_ADVERTISEMENTS
           config rule
               edit 1
                   set action permit
                   set prefix <CUSTOMER_PREFIX> <MASK>
                   set le 32
           end
   end
   config router bgp
       config neighbor
           edit <CE_PEER>
               set prefix-list-out CE_PREFIX_ADVERTISEMENTS
       end
   end
   ```

7. Require the first AS in the path to be the peer's.

   ```text
   config router bgp
       config neighbor
           edit <EBGP_PEER>
               set enforce-first-as enable
       end
   end
   ```

8. Reject routes whose origin AS is not the customer's.

   ```text
   config router aspath-list
       edit <ASPATH_LIST>
           config rule
               edit 1
                   set action permit
                   set regexp <CUSTOMER_ASN_REGEX>
           end
   end
   config router bgp
       config neighbor
           edit <CE_PEER>
               set filter-list-in <ASPATH_LIST>
       end
   end
   ```

9. Limit the prefixes accepted from each peer.

   ```text
   config router bgp
       config neighbor
           edit <EBGP_PEER>
               set maximum-prefix <MAXIMUM>
       end
   end
   ```

10. Reject prefixes longer than /24.

   ```text
   config router prefix-list
       edit PREFIX_FILTER
           config rule
               edit 3
                   set action permit
                   set prefix any
                   set ge 8
                   set le 24
           end
   end
   ```

11. On the peers (FRR), announce the test prefixes: a bogon (`192.168.99.0/24`), the switch's own prefix, an unallocated prefix, a /25, and enough prefixes to exceed the maximum. For example on `rtr-peer-1`: `router bgp 65202`, `neighbor 10.201.200.0 remote-as 65201`, `address-family ipv4 unicast`, `network 192.168.99.0/24`.

**Positive test.** The eBGP session comes up with the same key on both ends, and `get router info bgp summary` shows Established. Allowed customer prefixes are installed. Only customer and local prefixes are advertised to the peer.

**Negative test.** Announce each bad prefix class from the peer and show it rejected: `get router info bgp neighbors <PEER> received-routes` lacks it. Change the key on one end: the session drops. Send BGP from a host more than one hop away (TTL below 254): the session is refused. Exceed the maximum prefix count: the session is torn down and logged. Prepend a wrong first AS: the route is rejected.

**Evidence.** `get router info bgp summary` and received-routes before and after each test, and the session logs.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

### Lab 6.7 — VRF separation

**Goal.** Show that interfaces bound to different VRFs cannot reach each other without an explicit route.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-NET-000512-RTR-000005` | I | PE: bind each VRF to the right interfaces to keep L3VPNs separate | Partial | FortiSwitchOS 7.6.7 CLI Reference p69; FortiSwitchOS 7.6.7 CLI Reference p99 |

**Uses.** `sw-2048f-1`, the Advanced Features License (P8), two test hosts in different VRFs. Workbook prerequisites: P8, P9 (P8 FortiSwitch Advanced Features license; P9 A switch model series that supports the feature).

**Configure.**

1. Create the VRF and bind the interface to it.

   ```text
   config router vrf
       edit <VRF>
           set vrfid <ID>
   end
   config system interface
       edit <INTERFACE>
           set vrf <VRF>
   end
   ```

**Positive test.** Hosts in the same VRF reach each other.

**Negative test.** A host in one VRF cannot reach a host in the other (no route and no leak). Adding an explicit route leak allows it, which proves the separation was the cause.

**Evidence.** `get router info routing-table all` for each VRF and the failed and successful pings.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

### Lab 6.8 — Multicast routing: PIM interfaces, neighbor filters, and boundaries

**Goal.** Show that PIM runs only on interfaces that need it, that PIM neighbors are filtered, and that administratively scoped multicast stops at a boundary.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-NET-000019-RTR-000003` | II | Multicast: disable PIM on interfaces that do not need multicast routing | Same requirement | FortiSwitchOS 7.6.7 CLI Reference p67 |
| `SRG-NET-000019-RTR-000004` | II | Multicast: bind a PIM neighbor filter to PIM interfaces | Partial | FortiSwitchOS 7.6.7 CLI Reference p67 |
| `SRG-NET-000019-RTR-000005` | III | Multicast edge: set boundaries for administratively scoped multicast | Partial | FortiSwitchOS 7.6.7 CLI Reference p104 |

**Uses.** `sw-648f-1`, `rtr-peer-1`, `mcast-src-201` on segment 220, and a receiver. PIM-SSM only; the Advanced Features License (P8). Workbook prerequisites: P8, P9 (P8 FortiSwitch Advanced Features license; P9 A switch model series that supports the feature).

**Configure.**

1. Enable PIM-SSM on the interface that needs it and nowhere else.

   ```text
   config router multicast
       config interface
           edit <INTERFACE>
               set pim-mode ssm-mode
       end
   end
   ```

2. Bind a PIM neighbor filter to the PIM interface.

   ```text
   config router multicast
       config interface
           edit <INTERFACE>
               set pim-mode ssm-mode
       end
   end
   ```

3. Block administratively scoped multicast at the boundary with an ACL.

   ```text
   config switch acl ingress
       edit <ID>
           set ingress-interface <BOUNDARY_PORT>
           config classifier
               set dst-ip-prefix <ADMIN_SCOPED_PREFIX> <MASK>
           end
           config action
               set drop enable
           end
   end
   ```

**Positive test.** An SSM join from the receiver builds the tree and the stream arrives.

**Negative test.** A PIM hello from an unfiltered neighbor on a non-PIM interface is ignored. A stream to an administratively scoped group (`239.0.0.0/8`) does not cross the boundary.

**Evidence.** `get router info multicast pim` output and the receiver's capture.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

### Lab 6.9 — Hashed routing authentication with key lifetimes of 180 days or less

**Goal.** Show that OSPF and BGP use hashed (MD5) authentication, never plain text, and that keys carry lifetimes of 180 days or less where the protocol supports them.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-NET-000168-RTR-000077` | II | Use hashed (MD5) rather than plain-text routing protocol authentication | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p70 |
| `SRG-NET-000230-RTR-000003` | II | Use routing protocol keys with lifetimes of no more than 180 days | Partial | FortiSwitchOS 7.6.7 CLI Reference p66 |

**Uses.** `sw-648f-1`, `sw-2048f-1` (OSPF on L5), `rtr-peer-1` (BGP on L1), `ntp-201a` (P5), Advanced Features License (P8). Workbook prerequisites: P5, P8, P9, P11 (P5 Authoritative NTP servers and their authentication keys; P8 FortiSwitch Advanced Features license; P9 A switch model series that supports the feature; P11 Routing protocol configured with its neighbors).

Lifetimes are partial on FortiSwitchOS: key chains with send and accept lifetimes serve RIP and IS-IS, while OSPF MD5 keys and BGP passwords have no lifetime. The lab sets the lifetime where it is available and, for OSPF and BGP, adds a rotation by procedure that you record with its date.

**Configure.**

1. Authenticate OSPF with MD5 on L5 (`10.201.200.8/31` to `10.201.200.9/31`).

   ```text
   config router ospf
       config interface
           edit l5-ospf
               set interface vlan2005
               set authentication md5
               config md5-keys
                   edit 1
                       set key <KEY_1>
                   next
               end
           next
       end
   end
   ```

2. Authenticate the BGP session to `rtr-peer-1` (AS 65202) with a TCP MD5 password.

   ```text
   config router bgp
       set as 65201
       config neighbor
           edit 10.201.200.1
               set remote-as 65202
               set password <KEY_2>
           next
       end
   end
   ```

3. Create the key chain with a lifetime of 180 days (15 552 000 seconds) or less, for the protocols that use one.

   ```text
   config router key-chain
       edit lab-keys
           config key
               edit 1
                   set key-string <KEY>
                   set accept-lifetime <START> <END>
                   set send-lifetime <START> <END>
           end
   end
   ```

4. For OSPF and BGP, write the rotation in the lab notes: new key, date, and the date the next rotation is due, no more than 180 days away.

**Positive test.** `get router info ospf neighbor` shows Full and `get router info bgp summary` shows Established. `get router info ospf interface` shows MD5 authentication.

**Negative test.** Set a different key on `rtr-peer-1` for each protocol: the OSPF adjacency and the BGP session drop and the log names the authentication failure. Set the OSPF interface to `authentication none` on one end only: the adjacency does not form. Set the key-chain accept lifetime in the past and confirm the key is rejected.

**Evidence.** The two neighbor tables before and after each change, the interface authentication line, the key-chain lifetimes, and the written rotation record.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

### Lab 6.10 — Turn off call-home and drop fragmented ICMP

**Goal.** Show that the switch does not call home to the vendor, and that fragmented ICMP packets addressed to it are dropped.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-NET-000131-RTR-000083` | II | Disable any feature that calls home to the vendor | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p230 |
| `SRG-NET-000205-RTR-000002` | II | Drop fragmented ICMP packets destined to the switch | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p173 |

**Uses.** `sw-648f-1`, `gw-201` with a packet capture, `attacker-201` with `hping3`.

The fragmented-ICMP check drops all ICMP fragments on models that support it, not only those addressed to the switch. Record that difference from the Cisco rule.

**Configure.**

1. Disable the FortiEdge Cloud (FortiLAN Cloud) connection.

   ```text
   config system flan-cloud
       set status disable
   end
   ```

2. Turn on the fragmented-ICMP hardware check.

   ```text
   config switch security-feature
       set icmp-frag enable
   end
   ```

**Positive test.** `get system flan-cloud-mgr connection-info` shows no connection and `get system flan-cloud` shows the setting disabled, and a 10-minute capture on the switch's uplink at `gw-201` shows no connection to a vendor address.

**Negative test.** Enable the cloud setting briefly: the capture shows the connection attempt, which proves the capture would have seen a call home. Turn it off again. From `attacker-201`, `hping3 --icmp -f 10.201.30.11 -c 50`: the switch drops the fragments and its counter rises, then disable the check and confirm the fragments arrive.

**Evidence.** The cloud setting, both captures, and the drop counters with the check on and off.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

### Lab 6.11 — Gaps: ICMP and ARP behavior, auxiliary port, forwarding architecture, and IP options

**Goal.** Confirm that FortiSwitchOS has no setting for these Cisco-specific behaviors, observe the behavior, and record the compensating control and residual risk.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-NET-000362-RTR-000111` | II | Disable gratuitous ARP on external interfaces | Not supported | FortiSwitchOS-7.6.7-Administration_Guide—Standalone_Mode.pdf p53 |
| `SRG-NET-000362-RTR-000113` | II | Disable ICMP unreachable messages on external interfaces | Not supported | — p235 |
| `SRG-NET-000362-RTR-000114` | II | Disable ICMP mask reply messages on external interfaces | Not supported | — p235 |
| `SRG-NET-000019-RTR-000001` | III | Disable the auxiliary port | Not applicable | — p— |
| `SRG-NET-000512-RTR-000100` | II | Enable Cisco Express Forwarding | Not applicable | — p— |
| `SRG-NET-000205-RTR-000015` | II | Perimeter: block all packets with IP options | Not supported | FortiSwitchOS-7.6.7_CLI_Reference.pdf p105 |
| `SRG-NET-000364-RTR-000112` | II | Perimeter: disable proxy ARP on external interfaces | Not applicable | FortiSwitchOS-7.6.7_CLI_Reference.pdf p231 -237 |

**Uses.** `sw-648f-1`, `rtr-peer-1` as a probe source.

**Configure.**

1. Confirm the absence. In the CLI, run `config system interface`, `edit <INTERFACE>`, `set ?` and `config switch acl ingress`, `edit 1`, `config classifier`, `set ?`, and search for gratuitous ARP, ICMP unreachable, ICMP mask reply, proxy ARP, and IP options. Compare with the 7.6.7 CLI Reference and keep the output.

   ```text
   config system interface
       edit <INTERFACE>
           set ?
       end
   config switch acl ingress
       edit 1
           config classifier
               set ?
           end
   ```

2. Observe each behavior: send a probe that triggers an ICMP unreachable, an ICMP mask request, and an ARP request for the router's address, and capture the replies on `rtr-peer-1`.

3. Apply the nearest control: place an upstream ingress ACL that drops the probe traffic before it reaches the switch, and note that the console port is the only out-of-band port (there is no auxiliary port, so `SRG-NET-000019-RTR-000001` does not apply as written).

**Positive test.** With the upstream ACL, the probes never reach the switch and no replies are seen.

**Negative test.** Without the ACL, the switch answers the probes, which proves the behavior cannot be switched off on the device. IP options packets pass the switch's ACL classifier, which cannot match them.

**Evidence.** The CLI help output, the captures, and the disposition record: Does Not Meet on the switch, with the upstream control as mitigation.

**Return to baseline.** Remove the upstream ACL and restore the baseline.

### Lab 6.12 — Gaps: IPv6 extension-header filtering

**Goal.** Confirm that FortiSwitchOS ACLs cannot match IPv6 extension headers, show the traffic passing, and record the mitigation.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-NET-000364-RTR-000200` | II | Perimeter: drop IPv6 packets with an undetermined transport | Not supported | FortiOS-7.6.7-CLI_Reference.pdf p515 |
| `SRG-NET-000364-RTR-000201` | II | Perimeter: drop IPv6 packets with a Routing Header type 0, 1, or 3 to 255 | Not supported | FortiOS-7.6.7-CLI_Reference.pdf p515 |
| `SRG-NET-000364-RTR-000202` | II | Perimeter: drop IPv6 Hop-by-Hop headers with invalid option types | Not supported | FortiOS-7.6.7-CLI_Reference.pdf p515 |
| `SRG-NET-000364-RTR-000203` | II | Perimeter: drop IPv6 Destination Option headers with invalid option types | Not supported | FortiOS-7.6.7-CLI_Reference.pdf p515 |
| `SRG-NET-000364-RTR-000204` | II | Perimeter: drop IPv6 extension headers with the Endpoint Identification option | Not supported | FortiOS-7.6.7-CLI_Reference.pdf p515 |
| `SRG-NET-000364-RTR-000205` | II | Perimeter: drop IPv6 Destination Option headers with the NSAP address option | Not supported | FortiOS-7.6.7-CLI_Reference.pdf p515 |
| `SRG-NET-000364-RTR-000206` | II | Perimeter: drop IPv6 Hop-by-Hop or Destination Option headers with undefined option types | Not supported | FortiOS-7.6.7-CLI_Reference.pdf p515 |

**Uses.** `sw-2048f-1`, a Linux host with `scapy` on segment 42 and a receiver on segment 10.

**Configure.**

1. Confirm the absence. In the ACL classifier, run `set ?` and look for IPv6 extension-header or routing-header fields; compare with the CLI Reference and keep the output.

   ```text
   config switch acl ingress
       edit 1
           config classifier
               set ?
           end
   ```

2. From the host, send IPv6 packets with a Routing Header type 0, a Hop-by-Hop header with an invalid option, a Destination Options header with an invalid option, and a packet with an undetermined upper-layer protocol, using `scapy`.

3. Apply the mitigation: drop IPv6 extension-header abuse on the device that supports it, such as the upstream firewall or router, or filter at the host.

**Positive test.** With the upstream filter, each crafted packet is dropped before the receiver.

**Negative test.** Without it, the packets reach the receiver, which proves the switch's ACL cannot stop them.

**Evidence.** The help output, the `scapy` commands, receiver captures, and the disposition record.

**Return to baseline.** Restore the baseline.

### Lab 6.13 — Gaps: MPLS, LDP, and RSVP-TE

**Goal.** Confirm that FortiSwitchOS has no MPLS, LDP, or RSVP-TE, and record why these requirements are not applicable to the product.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-NET-000512-RTR-000002` | III | MPLS: source LDP sessions from a loopback address | Not supported | FortiSwitchOS-7.6.7_CLI_Reference.pdf p29 |
| `SRG-NET-000512-RTR-000003` | III | MPLS: synchronize the IGP with LDP | Not supported | FortiSwitchOS-7.6.7_CLI_Reference.pdf p29 |
| `SRG-NET-000193-RTR-000001` | III | MPLS: pace RSVP-TE messages | Not supported | FortiSwitchOS-7.6.7_CLI_Reference.pdf p29 |
| `SRG-NET-000512-RTR-000004` | II | MPLS: disable TTL propagation | Not supported | FortiSwitchOS-7.6.7_CLI_Reference.pdf p29 |
| `SRG-NET-000343-RTR-000001` | II | PE: authenticate targeted LDP sessions for L2VPN with a FIPS-approved MAC | Not supported | — p29 |

**Uses.** `sw-648f-1`.

**Configure.**

1. Confirm the absence. Run `config router ?` and search for `mpls`, `ldp`, and `rsvp`. Compare with the CLI Reference and the Feature Matrix and keep the output.

   ```text
   config router ?
   ```

**Positive test.** `config router ?` lists no MPLS, LDP, or RSVP-TE branch, and the Feature Matrix lists none.

**Negative test.** Try `config router ldp` and `config router mpls`: the CLI rejects them.

**Evidence.** The CLI output and the Feature Matrix page, with the disposition record (not applicable: the product has no MPLS).

**Return to baseline.** Restore the baseline.

### Lab 6.14 — Gaps: provider-edge L3VPN, L2VPN, VPLS, and provider QoS roles

**Goal.** Confirm that FortiSwitch cannot take the provider-edge or provider-core role these requirements describe, apply the nearest per-port controls where the same intent exists, and record the disposition.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-NET-000512-RTR-000006` | I | PE: give each VRF the right route targets | Not supported | — p29 |
| `SRG-NET-000512-RTR-000007` | II | PE: give each VRF the right route distinguisher | Not supported | — p29 |
| `SRG-NET-000512-RTR-000008` | I | PE: set the right VC ID for each VPWS attachment circuit | Not supported | — p29 |
| `SRG-NET-000512-RTR-000009` | I | PE: define VPLS attachment circuits with a unique VPN ID per customer VLAN | Not supported | — p29 |
| `SRG-NET-000512-RTR-000010` | III | PE: enforce split horizon for all pseudowires in a VPLS bridge domain | Not supported | — p29 |
| `SRG-NET-000193-RTR-000002` | II | PE: set storm control thresholds on VPLS CE-facing interfaces | Not supported | — p29 |
| `SRG-NET-000362-RTR-000119` | III | PE: run IGMP or MLD snooping in each VPLS bridge domain | Not supported | — p29 |
| `SRG-NET-000192-RTR-000002` | II | PE: limit the MAC addresses learned in each VPLS bridge domain | Not supported | — p29 |
| `SRG-NET-000205-RTR-000007` | I | PE: block traffic destined to the IP core infrastructure | Not applicable | FortiSwitchOS 7.6.7 CLI Reference p104 |
| `SRG-NET-000205-RTR-000008` | II | PE: enable loose uRPF on CE-facing interfaces | Not applicable | FortiSwitchOS 7.6.7 CLI Reference p243 |
| `SRG-NET-000205-RTR-000016` | II | PE: drop or ignore all packets with IP options | Not applicable | — p— |
| `SRG-NET-000193-RTR-000113` | III | PE: enforce a QoS policy that favors mission-critical traffic | Not applicable | — p168, 541-543 |
| `SRG-NET-000193-RTR-000114` | III | P (MPLS core): enforce a QoS policy that favors mission-critical traffic | Not applicable | — p— |

**Uses.** `sw-2048f-1`, a traffic generator, and the BGP EVPN VXLAN configuration from Lab 6.6 for the route-target comparison.

**Configure.**

1. Confirm the absence. Run `config router ?`, `config switch ?`, and search for `vpls`, `vpws`, `l3vpn`, and `pseudowire`. Note that route targets and route distinguishers exist only under BGP EVPN VXLAN. Keep the output.

   ```text
   config router ?
   config switch ?
   ```

2. For the intents that have an equivalent control on other roles, apply them on the lab edge: an ingress ACL that drops traffic to core prefixes, loose source checking on an edge interface, and per-port MAC learning limits.

   ```text
   config switch acl ingress
       edit <ID>
           set ingress-interface <EDGE_PORT>
           config classifier
               set dst-ip-prefix <CORE_PREFIX> <MASK>
           end
           config action
               set drop enable
           end
   end
   ```

3. Apply a QoS policy to favor mission-critical traffic, using the QoS sample in the workbook.

**Positive test.** The edge ACL drops traffic to the core prefix, loose source checking passes a valid source, and the QoS policy keeps critical traffic ahead of bulk.

**Negative test.** `config router vpls` and similar commands are rejected. Traffic to a core prefix is dropped only because of the edge ACL, which proves the control is not part of a provider-edge function.

**Evidence.** The CLI output, the ACL and QoS results, and the disposition record (not applicable: the switch cannot be a provider edge or core).

**Return to baseline.** Restore the baseline.

### Lab 6.15 — Gaps: rendezvous-point and designated-router multicast controls

**Goal.** Confirm that FortiSwitchOS runs PIM-SSM only, with no rendezvous point, and has no IGMP/MLD join or source filter or per-interface state limit; apply SSM and snooping controls and record the residual gap.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-NET-000362-RTR-000120` | III | RP: limit the multicast forwarding cache (PIM and MSDP source-active state) | Not applicable | FortiSwitchOS 7.6.7 CLI Reference p66 |
| `SRG-NET-000019-RTR-000013` | III | RP: filter PIM Register messages for unwanted groups and sources | Not applicable | FortiSwitchOS 7.6.7 CLI Reference p66 |
| `SRG-NET-000019-RTR-000014` | III | RP: filter PIM Join messages for unwanted groups | Not applicable | FortiSwitchOS 7.6.7 CLI Reference p66 |
| `SRG-NET-000362-RTR-000121` | II | RP: rate-limit PIM Register messages | Not applicable | FortiSwitchOS 7.6.7 CLI Reference p66 |
| `SRG-NET-000364-RTR-000114` | III | DR: let hosts join only approved multicast groups (IGMP and MLD report filter) | Not supported | FortiSwitchOS 7.6.7 CLI Reference p66 |
| `SRG-NET-000364-RTR-000115` | II | DR: let hosts join groups only from approved sources | Not supported | FortiSwitchOS 7.6.7 CLI Reference p66 |
| `SRG-NET-000362-RTR-000122` | II | DR: limit the multicast route states created by IGMP and MLD reports | Not supported | FortiSwitchOS 7.6.7 CLI Reference p66 |
| `SRG-NET-000362-RTR-000123` | II | DR: set the SPT threshold to infinity where Any Source Multicast is used | Not applicable | FortiSwitchOS 7.6.7 CLI Reference p66 |

**Uses.** `sw-648f-1`, `mcast-src-201`, a receiver, `attacker-201` as a rogue receiver.

**Configure.**

1. Confirm the absence. Run `config router multicast`, then `set ?`, and `config router multicast`, `config pim-sm-global`, `set ?`, and search for rendezvous point and register settings. Keep the output.

   ```text
   config router multicast
       set ?
   end
   ```

2. Use PIM-SSM so no rendezvous point or register messages exist, and enable IGMP and MLD snooping on the receiver VLAN.

**Positive test.** An SSM join for an approved source and group builds the tree. Snooping limits the stream to the receiving port.

**Negative test.** From `attacker-201`, send IGMP reports for many unapproved groups: the switch accepts them (there is no per-interface limit or filter), which is the residual gap. Record it and the upstream control that limits it.

**Evidence.** The help output, the multicast state table, and the disposition record.

**Return to baseline.** Restore the baseline.

### Lab 6.16 — Gaps: MSDP

**Goal.** Confirm that FortiSwitchOS does not run MSDP and record why the MSDP requirements are not applicable.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-NET-000364-RTR-000116` | II | MSDP: accept MSDP packets only from known peers | Not applicable | FortiSwitchOS 7.6.7 CLI Reference p29 |
| `SRG-NET-000343-RTR-000002` | II | MSDP: authenticate all received MSDP packets | Not applicable | FortiSwitchOS 7.6.7 CLI Reference p29 |
| `SRG-NET-000018-RTR-000007` | III | MSDP: filter received source-active messages for unwanted groups and sources | Not applicable | FortiSwitchOS 7.6.7 CLI Reference p29 |
| `SRG-NET-000018-RTR-000008` | III | MSDP: filter source-active messages sent to external peers | Not applicable | FortiSwitchOS 7.6.7 CLI Reference p29 |
| `SRG-NET-000018-RTR-000009` | III | MSDP: limit source-active messages accepted from each peer | Not applicable | FortiSwitchOS 7.6.7 CLI Reference p29 |
| `SRG-NET-000512-RTR-000011` | III | MSDP: source MSDP traffic from a loopback address | Not applicable | FortiSwitchOS 7.6.7 CLI Reference p29 |

**Uses.** `sw-648f-1`.

**Configure.**

1. Confirm the absence. Run `config router ?` and search for `msdp`. Compare with the CLI Reference and keep the output.

   ```text
   config router ?
   ```

**Positive test.** `config router ?` lists no MSDP branch.

**Negative test.** `config router msdp` is rejected, and TCP port 639 does not answer on the switch.

**Evidence.** The CLI output, a port scan of TCP 639, and the disposition record (not applicable: no MSDP).

**Return to baseline.** Restore the baseline.

## Lab Verification

Complete this sign-off once Labs 6.1 to 6.16 have been run end to end, including each negative test. Until then, the labs are unverified, and the commands in this chapter come from the workbook's CLI-checked syntax and have not been run in this lab.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter proves the 46 Router SRG requirements that FortiSwitch can meet and documents the 46 it cannot, in ten requirement labs and six gap labs. Each lab ends with evidence and a return to the baseline.

- [ ] Has run each requirement lab and its negative test.
- [ ] Has captured the evidence of absence for each gap lab.
- [ ] Has recorded a disposition for every gap requirement.
- [ ] Knows which switch each feature needs.
