# Chapter 04: Layer 2 Switch SRG Requirement Labs

## Learning Objectives

- Prove each Layer 2 Switch SRG requirement in the crosswalk on the lab from Chapter 999, with a positive and a negative test.
- Configure 802.1X and MAC authentication bypass, spanning tree guards, storm control, DHCP snooping, dynamic ARP inspection, and IP source guard on FortiSwitchOS.
- Apply VLAN hygiene: access ports, a dedicated native VLAN, pruned trunks, parked unused ports, and a management VLAN.
- Run the managed-mode network access control requirements from a FortiGate.
- Show, for requirements FortiSwitch cannot meet, that the setting is absent, and apply and record a compensating control.
- Collect and store the evidence for each lab so it can support an assessment.

## Theory and Architecture

The Layer 2 Switch SRG sets requirements for switches that forward frames inside a network: how endpoints are identified, how spanning tree and VLANs are protected, and how floods and spoofed traffic are contained. DISA publishes no FortiSwitch STIG, so a FortiSwitch is assessed against this SRG directly. Chapters 01 and 02 map each Layer 2 Switch requirement to a FortiSwitch feature and a command. This chapter turns those mappings into labs.

Every lab runs on the lab network that [Chapter 999](999-shared-lab-infrastructure.md) defines: segments 40, 41, 42, and 50 for endpoints, segment 10 for the services, segment 30 for management, and the two switches `sw-648f-1` and `sw-2048f-1`. A lab names the hosts it uses, starts from the `baseline-201` snapshot, and returns to it.

The requirements fall into five groups. *Identification and access control* decides which endpoint may connect. *Spanning tree* keeps one device from taking over the Layer 2 topology. *Flood and spoof control* limits broadcast storms and forged DHCP, ARP, and IP traffic. *VLAN hygiene* keeps the default VLAN, untagged traffic, and trunks tidy. *Resilience and baseline* covers failing safely and running only what is needed.

### Requirements and labs

The crosswalk lists 31 distinct Layer 2 Switch SRG requirements. Each one has a lab or a gap lab in this chapter, so none is left without a test.

| Lab | Requirements | Kind |
| --- | --- | --- |
| 4.1 | 1 | Requirement lab: Authenticate every endpoint (802.1X and MAC authentication bypass) |
| 4.2 | 4 | Requirement lab: Managed-mode network access control, quarantine, and security attributes |
| 4.3 | 4 | Requirement lab: Spanning tree protections: root guard, BPDU guard, loop guard, and rapid convergence |
| 4.4 | 4 | Requirement lab: Flood control: storm control, unknown unicast, multicast snooping, and QoS |
| 4.5 | 3 | Requirement lab: DHCP snooping, dynamic ARP inspection, and IP source guard |
| 4.6 | 8 | Requirement lab: VLAN hygiene: access ports, native VLANs, trunk pruning, unused ports, and management VLAN |
| 4.7 | 5 | Requirement lab: Fail secure, alternate paths, non-essential capabilities, and secure settings |
| 4.8 | 2 | Gap lab: Gaps: VTP and UDLD |

A **requirement lab** configures the FortiSwitch setting, proves it with a positive test, and proves the control with a negative test. A **gap lab** covers requirements that FortiSwitch cannot meet (alignment *Not supported* or *Not applicable* in the crosswalk): it proves the setting is absent, applies the nearest compensating control, and records the disposition and residual risk.

## Design Considerations

- **One group of requirements per lab.** Requirements that share a setting or a test (for example the three spanning tree guards) share a lab, so the lab shows how the controls interact.
- **Test the control, not only the setting.** A passing `show` command proves a setting exists. The negative test proves it blocks what it should, which is what an assessor needs.
- **Pick the right switch.** Some features are not supported on the FS-648F-FPOE (for example dynamic ARP inspection); each lab says which switch to use, and the workbook's Model Support sheet is the reference.
- **Managed mode is a separate lab.** The FortiLink requirements need a FortiGate and change the switch's management mode, so they run in one lab and the switch returns to standalone afterward.
- **Rates are packets per second.** FortiSwitchOS storm control uses packet rates, not Cisco percentages, so thresholds in the labs are chosen from the lab traffic generator.
- **Gaps are labs too.** A requirement the switch cannot meet is documented with the evidence that the setting is absent, the compensating control, and the residual risk.

## Implementation and Automation

Each lab lists its commands in the order to enter them. Commands come from the crosswalk workbook (Chapter 01's FortiSwitchOS 7.6.7 syntax) with the lab's values substituted: `<PORT_EP1>`, `<PORT_EP2>`, `<PORT_TRUNK>`, and `<PORT_UNUSED>` are the port names you wrote in your lab notes in Chapter 999, VLAN 40 is the user VLAN, VLAN 99 the native VLAN, VLAN 60 the unused VLAN, and VLAN 30 the management VLAN. Commands that begin with `FortiGate:` in the workbook are entered on `fgt-201`.

Save the evidence for each lab in `evidence/<lab>/<date>/` on `admin-201`, as Chapter 999 describes.

## Validation and Troubleshooting

Before each lab, confirm the baseline: `execute ping 10.201.10.10` from the switch, `get system status`, and `get system ntp`. After each lab, restore the baseline and re-run the first two checks.

| Symptom | Cause | Fix |
| --- | --- | --- |
| An 802.1X port never authorizes | The switch's source address is not a RADIUS client, or the secret differs | Check `clients.conf` on `radius-201a` and the secret in `config user radius` |
| A guard setting appears to do nothing | The attack frame never reaches the port, or spanning tree is disabled | Confirm `get switch stp instance` and capture on the port |
| Storm control does not drop traffic | The generator rate is below the threshold, or the mode is not overridden on the port | Raise the generator rate and check `storm-control-mode override` |
| A feature command is rejected | The feature is not supported on that switch | Check the Model Support sheet and use the other switch |
| DHCP snooping blocks the real server | The server's port is not trusted | Set the server's port to trusted |

## Security and Best Practices

- Run the attack tests only on the lab segments, with `attacker-201`, never on a production network.
- Keep a console connection while you test port guards, because a guard can disable the port you are managing through.
- Generate fresh RADIUS secrets for each run and delete them in the cleanup step.
- Record the model and FortiSwitchOS version with every result, because behavior and support differ by model.
- Treat a negative test that fails to block as a finding, not a lab error.

## References and Knowledge Checks

**References:**

- [Chapter 01](01-fortiswitch-feature-version-and-srg-map.md) and [Chapter 02](02-fortiswitch-and-cisco-catalyst-switch-stig-crosswalk.md) for the rows these labs prove.
- [Chapter 999](999-shared-lab-infrastructure.md) for the lab network, hosts, and baseline.
- Layer 2 Switch SRG (DISA, V3R4 as compared with a third-party mirror; confirm against DISA's own file).
- FortiSwitchOS 7.6.7 CLI Reference and Administration Guide (Fortinet Document Library).
- [Volume CLXXII, Chapter 03](../../volume-172-disa-srgs-and-stigs/chapters/03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md) for assessing a product that has no STIG.

**Knowledge checks:**

1. Why does an 802.1X lab need both a positive and a negative test?
2. What is the difference between root guard and BPDU guard, and which port does each belong on?
3. Why can dynamic ARP inspection be enabled only where DHCP snooping is on?
4. What does a double-tagged frame test show about a native VLAN?
5. Which Layer 2 Switch requirements can FortiSwitch not meet, and what is the compensating control for each?

## Hands-On Lab

**Shared prerequisites.** The infrastructure from Chapter 999 (Labs 999.1 to 999.6), the `baseline-201` snapshot, and a console connection to each switch. Test tools on `attacker-201`: a packet generator (`hping3` or `mausezahn`), a bridge tool that can send spanning tree BPDUs, and `tcpdump`. Port names are those you recorded in your lab notes. **Cost:** none beyond the Chapter 999 lab.

### Lab 4.1 — Authenticate every endpoint (802.1X and MAC authentication bypass)

**Goal.** Show that a host port admits an endpoint only after 802.1X, or MAC authentication bypass for a device that cannot run a supplicant, succeeds against RADIUS.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-NET-000148-L2S-000015` | I | Identify and authenticate every endpoint before it connects | Same requirement | FortiOS 7.6.7 CLI Reference p1269; FortiOS 7.6.7 CLI Reference p1317 |

**Uses.** `sw-648f-1`, `radius-201a` and `radius-201b` (P1, P2), segments 40 (802.1X) and 41 (MAB), a laptop with a supplicant on `<PORT_EP1>` and a MAB device on `<PORT_EP2>`. Workbook prerequisites: P1, P2 (P1 Reachable RADIUS or TACACS+ servers; P2 User group that lists the authentication servers).

**Configure.**

1. Create the 802.1X port mode on the host port. Use `802.1X` for the supplicant host and `802.1X-mac-based` for the MAB device.

   ```text
   config switch interface
       edit <PORT_EP1>
           config port-security
               set port-security-mode 802.1X-mac-based
               set mac-auth-bypass enable
           end
           set security-groups lab-radius
   end
   config user group
       edit lab-radius
           set member radius-201a radius-201b
   end
   ```

2. In `radius-201a` and `radius-201b`, add the supplicant user and, for the MAB device, a user whose name and password are the device MAC address.

**Positive test.** Connect the laptop. `diagnose switch 802-1x status` lists the port as authorized, the laptop gets a DHCP address in VLAN 40, and the FreeRADIUS log shows an Access-Accept. Connect the MAB device: it is authorized on its MAC address and lands in VLAN 41.

**Negative test.** Connect a host that has no supplicant and whose MAC address is not in RADIUS. The port stays unauthorized, no DHCP address is issued, and the switch logs the failure. Repeat with a wrong password.

**Evidence.** `show full-configuration switch interface <PORT_EP1>`, the `802-1x status` output before and after, and the FreeRADIUS Access-Accept and Access-Reject lines.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

### Lab 4.2 — Managed-mode network access control, quarantine, and security attributes

**Goal.** Show that a FortiGate managing the switch over FortiLink authenticates endpoints, attaches security attributes to them, and isolates an endpoint into a quarantine or LAN segment.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-NET-000343-L2S-000016` | II | The layer 2 switch must authenticate all network-connected endpoint devices before establishing any connection. | feature row (no Cisco rule) | FortiOS 7.6.7 CLI Reference p1269; FortiSwitch 7.6.7 Feature Matrix p1 |
| `SRG-NET-000057-L2S-000005` | II | The layer 2 switch must dynamically associate security attributes with organization-defined subjects in accordance with organization-defined security policies as information is created and combined. | feature row (no Cisco rule) | FortiOS 7.6.7 CLI Reference p1226; FortiOS 7.6.7 CLI Reference p1234 |
| `SRG-NET-000520-L2S-000105` | II | The layer 2 switch must dynamically associate security attributes with organization-defined objects in accordance with organization-defined security policies as information is created and combined. | feature row (no Cisco rule) | FortiOS 7.6.7 CLI Reference p1226; FortiOS 7.6.7 CLI Reference p2149 |
| `SRG-NET-000715-L2S-000120` | II | The layer 2 switch must implement physically or logically separate subnetworks to isolate organization-defined critical system components and functions. | feature row (no Cisco rule) | FortiOS 7.6.7 CLI Reference p1234; FortiOS 7.6.7 CLI Reference p1335 |

**Uses.** `fgt-201` (P7) on segment 254, `sw-648f-1` in FortiLink managed mode, `radius-201a`, and a test endpoint. This lab changes the switch from standalone to managed mode, so run it last and restore the standalone baseline afterward.

Managed-mode commands run on the FortiGate, not on the switch. The workbook rows for these requirements are feature rows, so the steps below apply the FortiGate objects they name. Features that need FortiClient EMS, FortiVoice, or an IoT/OT feed are tested only if you have that product; otherwise record the row as covered by procedure.

**Configure.**

1. Authorize the switch under `fgt-201` and set the port access mode for NAC.

   ```text
   FortiGate: config switch-controller managed-switch
   edit <SWITCH_SN>
       config ports
           edit <PORT_EP1>
               set access-mode nac
       end
   ```

2. Enable host quarantine.

   ```text
   FortiGate: config switch-controller quarantine
   set quarantine enable
   config targets
       edit <MAC>
   end
   ```

3. Turn on VLAN isolation inside a segment.

   ```text
   FortiGate: config system interface
   edit <VLAN_INTERFACE>
       set switch-controller-access-vlan enable
   end
   ```

4. Bind an endpoint tag or vulnerability category to a NAC policy.

   ```text
   FortiGate: config user nac-policy
   edit <POLICY>
       set category ems-tag
       set ems-tag <TAG>
   end
   ```

**Positive test.** Plug in an endpoint that matches the NAC policy. It lands in the policy's VLAN. Add its MAC address to quarantine: it moves to the quarantine VLAN and loses access to segment 10.

**Negative test.** Plug in an endpoint that matches no policy and is not authenticated. It stays in the default (no-access) state. Try to reach another host in the same isolated VLAN: the traffic is dropped.

**Evidence.** The FortiGate NAC policy, the managed-switch port settings, the quarantine list, and the endpoint's VLAN before and after.

**Return to baseline.** Release the quarantine, return the switch to standalone mode, and restore the baseline.

### Lab 4.3 — Spanning tree protections: root guard, BPDU guard, loop guard, and rapid convergence

**Goal.** Show that spanning tree cannot be taken over from an access port or an unexpected uplink, and that loops and one-way blocking ports are contained.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-NET-000362-L2S-000021` | III | Enable Root Guard on ports facing access switches | Same requirement | FortiSwitchOS 7.6.7 CLI Reference p127 |
| `SRG-NET-000362-L2S-000022` | II | Enable BPDU Guard on user-facing and untrusted ports | Same requirement | FortiSwitchOS 7.6.7 CLI Reference p127 |
| `SRG-NET-000362-L2S-000023` | II | Enable STP Loop Guard | Same requirement | FortiSwitchOS 7.6.7 CLI Reference p126; FortiSwitchOS 7.6.7 CLI Reference p127 |
| `SRG-NET-000512-L2S-000003` | II | Run Rapid STP where VLANs span switches with redundant links | Same requirement | FortiSwitchOS 7.6.7 CLI Reference p115; FortiSwitchOS 7.6.7 CLI Reference p126 |

**Uses.** `sw-648f-1` and `sw-2048f-1` joined by a trunk, plus `attacker-201` on `<PORT_EP1>` with a bridge tool that can send BPDUs (for example a Linux bridge with a low priority).

**Configure.**

1. Enable spanning tree and the MSTP instance so every port converges rapidly.

   ```text
   config switch stp settings
       set status enable
   end
   config switch interface
       edit <PORT_EP1>
           set stp-state enabled
           set rpvst-port enabled
   end
   ```

2. Enable root guard on the port toward an access switch.

   ```text
   config switch interface
       edit <PORT_TRUNK>
           set stp-root-guard enabled
   end
   ```

3. Enable BPDU guard on the host port.

   ```text
   config switch interface
       edit <PORT_EP1>
           set stp-bpdu-guard enabled
   end
   ```

4. Enable loop protection and loop guard on the trunk ports.

   ```text
   config switch interface
       edit <PORT_EP1>
           set stp-loop-protection enabled
           set loop-guard enabled
   end
   ```

**Positive test.** Check that `sw-2048f-1` is the root bridge (`get switch stp instance`). Pull the L5 trunk and replace it: the topology re-converges in seconds.

**Negative test.** From `attacker-201`, send a BPDU with a better bridge priority into the host port: the port is disabled by BPDU guard and a log line is written. Send the superior BPDU into the root-guard port: the port goes to the root-inconsistent state and the root does not change. Remove the BPDU guard and repeat to show the root changing.

**Evidence.** `get switch stp instance` before and after each attack, the port state, and the syslog lines for the guard events.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

### Lab 4.4 — Flood control: storm control, unknown unicast, multicast snooping, and QoS

**Goal.** Show that broadcast, unknown unicast, and multicast floods are limited at the host port, that multicast is not flooded to every port, and that excess bandwidth cannot starve other traffic.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-NET-000512-L2S-000001` | III | Configure storm control on all host-facing ports | Same requirement | FortiSwitchOS 7.6.7 CLI Reference p115; FortiSwitchOS 7.6.7 CLI Reference p158 |
| `SRG-NET-000362-L2S-000024` | II | Enable Unknown Unicast Flood Blocking on host ports | Partial | FortiSwitchOS 7.6.7 CLI Reference p158 |
| `SRG-NET-000512-L2S-000002` | III | Enable IGMP or MLD snooping on all VLANs | Same requirement | FortiSwitchOS 7.6.7 CLI Reference p115; FortiSwitchOS 7.6.7 CLI Reference p185 |
| `SRG-NET-000193-L2S-000020` | II | Manage excess bandwidth to limit flooding denial-of-service attacks | Same requirement | FortiSwitchOS 7.6.7 CLI Reference p105; FortiSwitchOS 7.6.7 CLI Reference p108 |

**Uses.** `sw-648f-1`, `attacker-201` with a traffic generator (for example `hping3` or `mausezahn`) on `<PORT_EP1>`, a receiver on `<PORT_EP2>`, and `flow-201` to read counters. Rates are in packets per second on FortiSwitchOS. Workbook prerequisites: P9, P13 (P9 A switch model series that supports the feature; P13 The user).

**Configure.**

1. Set storm control on the host port.

   ```text
   config switch physical-port
       edit <PORT_EP1>
           set storm-control-mode override
           config storm-control
               set broadcast enable
               set unknown-unicast enable
               set rate <PPS>
           end
   end
   ```

2. Limit unknown unicast on the host port. The setting only partly matches the Cisco unknown-unicast flood block, because it limits the rate and does not block the traffic.

   ```text
   config switch physical-port
       edit <PORT_EP1>
           set storm-control-mode override
           config storm-control
               set unknown-unicast enable
               set broadcast disable
               set unknown-multicast disable
               set rate 0
           end
   end
   ```

3. Enable IGMP and MLD snooping on the user VLAN.

   ```text
   config switch vlan
       edit <VLAN>
           set igmp-snooping enable
           set mld-snooping enable
   end
   ```

4. Apply an egress QoS policy with weighted queues on the uplink.

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

**Positive test.** Send a modest broadcast rate: it passes. Join a multicast group from `<PORT_EP2>`: `get switch igmp-snooping group` shows the group on that port only. Run bulk traffic and voice-class traffic together: the weighted queues keep the voice class moving.

**Negative test.** Send a broadcast flood well above the threshold from `attacker-201`: the receiver sees the rate capped at the configured level and the storm-control counter increases. Send unknown-unicast frames above the limit: they are dropped. Disable storm control and repeat to show the receiver overwhelmed.

**Evidence.** The storm-control configuration, the receiver's measured rate with and without the control, and the port counters.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

### Lab 4.5 — DHCP snooping, dynamic ARP inspection, and IP source guard

**Goal.** Show that only the trusted port can serve DHCP, that forged ARP replies are dropped, and that a host cannot source traffic from an address it was not given.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-NET-000362-L2S-000025` | II | Enable DHCP snooping on all user VLANs | Same requirement | FortiSwitchOS 7.6.7 CLI Reference p184; FortiSwitchOS 7.6.7 CLI Reference p185 |
| `SRG-NET-000362-L2S-000027` | II | Enable Dynamic ARP Inspection on all user VLANs | Same requirement | FortiSwitchOS 7.6.7 CLI Reference p185; FortiSwitchOS 7.6.7 CLI Reference p185, 126 |
| `SRG-NET-000362-L2S-000026` | II | Enable IP Source Guard on user-facing and untrusted ports | Same requirement | FortiSwitch-7.6.0-Feature-Matrix.pdf p5; FortiSwitchOS 7.6.7 CLI Reference p115 |

**Uses.** `sw-2048f-1` for dynamic ARP inspection (the FS-648F-FPOE does not support it; check the Model Support sheet before you pick a switch for IP source guard), `dhcp-201` as the trusted server, `static-1` and `static-2` on segment 42 (P14), and `attacker-201` as a rogue DHCP server and ARP spoofer. Workbook prerequisites: P9, P12, P13, P14 (P9 A switch model series that supports the feature; P12 DHCP snooping enabled on the VLAN; P13 The user; P14 IP-to-MAC binding entries for statically addressed hosts).

**Configure.**

1. Enable DHCP snooping on the user VLAN and trust the uplink toward `dhcp-201` (P12).

   ```text
   config switch vlan
       edit <VLAN>
           set dhcp-snooping enable
   end
   config switch interface
       edit <PORT_TRUNK>
           set dhcp-snooping trusted
   end
   ```

2. Enable dynamic ARP inspection on the VLAN and trust the uplink.

   ```text
   config switch vlan
       edit <VLAN>
           set arp-inspection enable
   end
   config switch interface
       edit <PORT_TRUNK>
           set arp-inspection-trust trusted
   end
   ```

3. Enable IP source guard on the host port and add the binding for `static-1` (P14).

   ```text
   config switch interface
       edit <PORT_EP1>
           set ip-source-guard enable
   end
   ```

**Positive test.** A normal host receives a lease from `dhcp-201`, and `get switch dhcp-snooping` shows the binding. `static-1` pings `10.201.42.1` with its bound address and MAC.

**Negative test.** Start a rogue DHCP server on `attacker-201`: its offers are dropped on the untrusted port and no client receives them. Send a forged ARP reply claiming the gateway's address: the frame is dropped and a log line is written. Change `static-1`'s address to one with no binding: its traffic is dropped.

**Evidence.** The snooping binding table, the ARP-inspection and source-guard counters, and the capture on the victim host showing no forged traffic.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

### Lab 4.6 — VLAN hygiene: access ports, native VLANs, trunk pruning, unused ports, and management VLAN

**Goal.** Show that host ports carry one untagged user VLAN, trunks are static with a dedicated native VLAN and a pruned VLAN list, unused ports are parked, and management is on its own VLAN.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-NET-000512-L2S-000011` | II | Configure user-facing and untrusted ports as access ports | Same requirement | FortiSwitchOS 7.6.7 CLI Reference p126 |
| `SRG-NET-000512-L2S-000008` | II | Keep the default VLAN off host-facing ports | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p126 |
| `SRG-NET-000512-L2S-000013` | III | Assign no access ports to the native VLAN | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p126 |
| `SRG-NET-000512-L2S-000012` | II | Use a native VLAN other than the default VLAN on 802.1Q trunks | Same requirement | FortiSwitchOS 7.6.7 CLI Reference p126 |
| `SRG-NET-000512-L2S-000009` | II | Prune the default VLAN from trunks that do not need it | Same requirement | FortiSwitchOS 7.6.7 CLI Reference p115; FortiSwitchOS 7.6.7 CLI Reference p126 |
| `SRG-NET-000512-L2S-000005` | II | Enable all trunk links statically | Same requirement | FortiSwitchOS 7.6.7 CLI Reference p126, 179; FortiSwitchOS 7.6.7 CLI Reference p180 |
| `SRG-NET-000512-L2S-000007` | II | Put disabled ports in an unused VLAN | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p126 |
| `SRG-NET-000512-L2S-000010` | II | Keep management traffic off the default VLAN | Equivalent setting | FortiSwitchOS 7.6.7 CLI Reference p242 |

**Uses.** Both switches with the VLANs and trunk from Lab 999.3, `attacker-201` sending tagged frames, and `admin-201`. Workbook prerequisites: P10, P13 (P10 A management interface with an address: the management port or a management SVI on a dedicated VLAN; P13 The user).

**Configure.**

1. Make the host port an access port: native VLAN 40 and discard tagged frames.

   ```text
   config switch interface
       edit <PORT_EP1>
           set native-vlan 40
           set discard-mode all-tagged
   end
   ```

2. Set the trunk's native VLAN to 99 and list only the VLANs it needs, which prunes VLAN 1.

   ```text
   config switch interface
       edit <PORT_TRUNK>
           set native-vlan 99
           set allowed-vlans <VLANS>
   end
   ```

3. Make the trunk static and statically enabled.

   ```text
   config switch trunk
       edit <TRUNK>
           set mode static
   end
   ```

4. Park the unused port in VLAN 60 and shut it down.

   ```text
   config switch interface
       edit <PORT_UNUSED>
           set native-vlan 60
   end
   config switch physical-port
       edit <PORT_UNUSED>
           set status down
   end
   ```

5. Put the management SVI on VLAN 30.

   ```text
   config system interface
       edit mgmt-svi
           set vlanid 30
           set ip 10.201.30.11 <MASK>
           set allowaccess https ssh
   end
   ```

**Positive test.** `get switch interface` shows host ports untagged in VLAN 40, trunks tagged only for VLANs 10, 20, 30, 40, 41, 42, and 50 with native 99, and unused ports down in VLAN 60. SSH to `10.201.30.11` works from `admin-201`.

**Negative test.** From `attacker-201`, send a frame tagged with VLAN 30 into the host port: it is discarded. Send a double-tagged frame (outer 99, inner 30): it does not reach segment 30. Plug a host into an unused port: the link stays down.

**Evidence.** The port configuration, the capture on the VLAN 30 host showing no tagged-frame leak, and the unused-port status.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

### Lab 4.7 — Fail secure, alternate paths, non-essential capabilities, and secure settings

**Goal.** Show that the switch fails to a defined state, keeps working over a surviving link, runs only the services it needs, and authenticates its neighbors where the requirement asks.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-NET-000235-L2S-000031` | II | The layer 2 switch must be configured to fail securely in the event of an operational failure. | feature row (no Cisco rule) | FortiSwitchOS 7.6.7 CLI Reference p127; FortiSwitchOS-7.6.7-Administration_Guide—Standalone_Mode.pdf p62 |
| `SRG-NET-000760-L2S-000160` | II | The layer 2 switch must establish organization-defined alternate communications paths for system operations organizational command and control. | feature row (no Cisco rule) | FortiSwitchOS 7.6.7 CLI Reference p115; FortiSwitchOS 7.6.7 CLI Reference p123 |
| `SRG-NET-000131-L2S-000014` | II | The layer 2 switch must be configured to disable non-essential capabilities. | feature row (no Cisco rule) | FortiSwitch 7.6.7 Feature Matrix p10; FortiSwitch 7.6.7 Feature Matrix p2 |
| `SRG-NET-000512-L2S-000100` | II | The layer 2 switch must be configured in accordance with the security configuration settings based on DoD security configuration or implementation guidance, including STIGs, NSA configuration guides, CTOs, and DTMs. | feature row (no Cisco rule) | FortiSwitch 7.6.7 Feature Matrix p1; FortiSwitchOS 7.6.7 Administration Guide p53 |
| `SRG-NET-000325-L2S-000041` | II | The layer 2 switch must uniquely identify and authenticate source by organization, system, application, and/or individual for information transfer. | feature row (no Cisco rule) | FortiSwitch 7.6.7 Feature Matrix p2; FortiSwitchOS 7.6.7 CLI Reference p145 |

**Uses.** `sw-648f-1` and `sw-2048f-1` joined by two links for a link aggregation group (LAG), `radius-201a`, and a console cable. The MACsec part needs two ports that support it; check the Feature Matrix.

The row for the DoD security configuration settings (`SRG-NET-000512-L2S-000100`) is satisfied by the whole set of settings this volume proves; this lab records the configuration baseline and the checks that tie to it.

**Configure.**

1. Keep a second firmware image and fall back to a guest VLAN when RADIUS is down.

   ```text
   config system global
       set image-rotation enable
   end
   ```

2. Build a LAG between the switches with a minimum bundle size.

   ```text
   config switch trunk
       edit <TRUNK>
           set mode lacp-active
           set members <PORTS>
   end
   ```

3. Limit management services to what the lab needs and disable LLDP on ports that do not use it.

   ```text
   Disable all unused services, ports, and protocols. config system interface
   edit <MGMT, VLAN>
       set allowaccess https ssh
   end
   ```

4. Record the settings baseline: enable IP conflict detection and save `show full-configuration` as the baseline file.

   ```text
   config system global
       set detect_ip_conflict enable
   end
   ```

5. Protect the inter-switch link with MACsec using a pre-shared key, if the ports support it.

   ```text
   config switch macsec profile
       edit <PROFILE>
           set macsec-mode static-cak
           set cipher_suite GCM-AES-256
           config mka-psk
               edit <KEY>
                   set mka-cak <CAK>
                   set mka-ckn <CKN>
           end
   end
   config switch physical-port
       edit <PORT_EP1>
           set security-mode macsec
           set macsec-profile <PROFILE>
   end
   ```

**Positive test.** Pull one LAG member: traffic continues over the other and `get switch trunk` shows the member down. Stop both RADIUS servers: a new endpoint on the 802.1X port lands in the fail-open VLAN. Scan the management address from `admin-201`: only SSH answers.

**Negative test.** Pull the second LAG member so the bundle drops below the minimum: the LAG goes down instead of passing traffic on a degraded bundle. Enable a service you disabled (for example Telnet), confirm the scan shows it, then disable it again. Change the MACsec key on one end: the link does not pass traffic.

**Evidence.** `get system status` (shows both firmware images), the LAG state before and after each pull, the port-scan output, and the MACsec status.

**Return to baseline.** Restore the `baseline-201` snapshots and configuration (Lab 999.6).

### Lab 4.8 — Gaps: VTP and UDLD

**Goal.** Confirm that FortiSwitchOS has no VTP and no UDLD, apply the nearest compensating control, and record the disposition.

| SRG ID | CAT | Requirement | Alignment in Chapter 02 or 03 | Workbook reference |
| --- | --- | --- | --- | --- |
| `SRG-NET-000168-L2S-000019` | II | Authenticate VTP messages with the strongest available hash | Not applicable | FortiSwitchOS 7.6.7 CLI Reference p115 |
| `SRG-NET-000512-L2S-000004` | II | Enable UDLD to protect against one-way links | Not supported | FortiSwitchOS 7.6.7 CLI Reference p127 |

**Uses.** `sw-648f-1` and `sw-2048f-1` on the L5 trunk.

**Configure.**

1. Confirm there is no VTP or UDLD setting. In the CLI, type `config switch global` and then `set ?`, and `config switch interface`, `edit <PORT>`, `set ?`, and search the output for `vtp` and `udld`. Compare with the 7.6.7 CLI Reference. Keep the output.

   ```text
   config switch global
       set ?
   end
   config switch interface
       edit <PORT_EP1>
           set ?
       end
   ```

2. Keep VTP frames from being flooded between ports (the only VTP-related setting).

   ```text
   config switch global
       set flood-vtp disable
   end
   ```

3. Use STP loop protection as the compensating control for a one-way link on a blocking port.

   ```text
   config switch interface
       edit <PORT_EP1>
           set stp-loop-protection enabled
   end
   ```

**Positive test.** `get switch global` shows `flood-vtp disable`. After you break one direction of a fiber link (pull one strand), STP loop protection keeps the blocking port blocking.

**Negative test.** Without loop protection, break one direction of the link and observe the port move to forwarding and a loop forming. With it enabled, the loop does not form. A UDLD frame from a Cisco device is not processed by the switch; note this as the residual gap.

**Evidence.** The CLI help output proving the settings are absent, the configuration, and the one-way-link test result.

**Return to baseline.** Restore the baseline.

## Lab Verification

Complete this sign-off once Labs 4.1 to 4.8 have been run end to end, including each negative test. Until then, the labs are unverified, and the commands in this chapter come from the workbook's CLI-checked syntax and have not been run in this lab.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter proves the Layer 2 Switch SRG requirements on FortiSwitch, one lab per group of requirements, and documents the two the switch cannot meet. Each lab ends with evidence and a return to the baseline.

- [ ] Has run each requirement lab and its negative test.
- [ ] Can say which switch each feature needs.
- [ ] Has recorded the gap evidence and compensating control for VTP and UDLD.
- [ ] Has stored the evidence for each lab.
