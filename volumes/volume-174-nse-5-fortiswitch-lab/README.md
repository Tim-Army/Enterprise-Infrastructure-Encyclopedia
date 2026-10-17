# Volume CLXXIV — NSE 5 FortiSwitch Lab (Real Switch and FortiGate-Only)

> A build-it-yourself lab for **Fortinet NSE 5 - FortiSwitch 7.6 Administrator**
> (NSE5_FSW_AD-7.6). It covers FortiSwitch managed over **FortiLink** by a
> FortiGate, and the same switch in **standalone** FortiSwitchOS mode. **Track 1**
> uses a real FortiSwitch (an FS-108F, an FS-124F, or a pair of FS-2xx switches)
> managed by a FortiGate: a used hardware 40F or 60F, the lab's FortiGate-VM
> evaluation FGT-1, or a licensed FortiGate-VM. **Track 2** is a FortiGate-only
> path: it builds every switch-controller object on the FortiGate and turns
> switch-only tasks into read-and-predict exercises that use real FortiOS 7.6 and
> FortiSwitchOS 7.6 output. Twelve chapters, 50 labs, mapped to all 15 exam tasks.

## Overview

Volume CLXXIV is a **certification lab volume**, not a segmentation lab. It pairs
with [Volume XIX](../volume-019-fortinet-network-security/README.md), which places
NSE 5 in the restored NSE program, and with
[Volume CLXXII](../volume-172-disa-srgs-and-stigs/README.md), whose FortiSwitch SRG
map and crosswalks supply commands that the hardening lab reuses. It follows the
exam's four domains: FortiSwitch concepts, deployment and management, Layer 2
control and security, and monitoring and troubleshooting.

It is honest about limits. No FortiSwitch VM exists, so hands-on switching needs
hardware. The FortiGate-VM evaluation caps interfaces, firewall policies, and
routes at three each and VDOMs at two, and FortiLink on the evaluation license is
unconfirmed until Chapter 02's go/no-go test. Entry-level switches lack MCLAG,
split port, and FortiLink-mode ACLs. Chapter 01's capability matrix, checked
against the FortiSwitchOS 7.6.7 feature matrix, shows which labs each switch
option runs hands-on, and every lab opens with a platform note.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview, Topology, and Exam Map](chapters/01-lab-overview-topology-and-exam-map.md) | — |
| 02 | [Lab Preparation](chapters/02-lab-preparation.md) | 2.1–2.5 |
| 03 | [FortiLink Provisioning and the Managed-Switch Lifecycle](chapters/03-fortilink-provisioning-and-the-managed-switch-lifecycle.md) | 3.1–3.5 |
| 04 | [VLANs, Switch Ports, Transceivers, and Routing](chapters/04-vlans-switch-ports-transceivers-and-routing.md) | 4.1–4.5 |
| 05 | [Spanning Tree and Loop Protection](chapters/05-spanning-tree-and-loop-protection.md) | 5.1–5.3 |
| 06 | [Layer 2 Design: FortiLink Redundancy, Stacking, and MCLAG](chapters/06-layer-2-design-fortilink-redundancy-stacking-and-mclag.md) | 6.1–6.4 |
| 07 | [Port Security: 802.1X, MAB, Dynamic VLANs, and MAC Limits](chapters/07-port-security-8021x-mab-dynamic-vlans-and-mac-limits.md) | 7.1–7.4 |
| 08 | [Filtering, Antispoofing, ACLs, and VLAN Security](chapters/08-filtering-antispoofing-acls-and-vlan-security.md) | 8.1–8.5 |
| 09 | [NAC, Dynamic Port Policies, Quarantine, and Multicast](chapters/09-nac-dynamic-port-policies-quarantine-and-multicast.md) | 9.1–9.4 |
| 10 | [QoS, LLDP-MED, and Multi-Tenancy](chapters/10-qos-lldp-med-and-multi-tenancy.md) | 10.1–10.4 |
| 11 | [Standalone FortiSwitch: Layer 2, Layer 3, and FortiEdge Cloud](chapters/11-standalone-fortiswitch-layer-2-layer-3-and-fortiedge-cloud.md) | 11.1–11.5 |
| 12 | [Monitoring, Troubleshooting, Hardening, and Teardown](chapters/12-monitoring-troubleshooting-hardening-and-teardown.md) | 12.1–12.6 |

## What you will be able to do

- Enable the switch controller, build a FortiLink interface, and discover,
  authorize, upgrade, and retire a managed FortiSwitch.
- Build FortiSwitch VLANs, access and trunk ports, LAGs, and inter-VLAN routing,
  and know which models support split ports.
- Configure MSTP with edge ports, BPDU guard, root guard, and loop guard, and
  recognize a loop.
- Choose and build supported topologies: single and multi-tier, ISL stacks,
  MCLAG, and FortiLink over Layer 3. Share switch ports across VDOMs.
- Secure access ports with 802.1X, MAB, dynamic VLANs, MAC limits, sticky MAC,
  DHCP snooping, dynamic ARP inspection, storm control, ACLs, NAC, and quarantine.
- Apply QoS maps and policies and LLDP-MED voice policies.
- Run a FortiSwitch standalone with VLANs, SVIs, static routes, and ACLs, and know
  how FortiEdge Cloud manages it.
- Monitor with SNMP, sFlow, flow export, and packet capture, and troubleshoot
  FortiLink from its symptoms.

## Prerequisites

- **Track 1 controller (one of):** C1, a used FortiGate 40F or 60F on FortiOS 7.6,
  cabled directly to the switch; C2, FGT-1 (the FortiGate-VM evaluation on
  Proxmox, FortiOS 7.6) with `port3` taken over for FortiLink and a dedicated
  Proxmox NIC or PCI passthrough; or C3, a licensed FortiGate-VM with a dedicated
  NIC or passthrough.
- **Track 1 switch (one of):** S1, an FS-108F; S2, an FS-124F (recommended; a POE
  or FPOE variant for an LLDP-MED phone); or S3, a pair of FS-2xx switches such as
  the FS-224E or FS-248E, for MCLAG and FortiLink-mode ACLs. All on FortiSwitchOS
  7.6.x.
- **Track 1 extras:** a console cable, one or two endpoints (a laptop or a
  Raspberry Pi), a FreeRADIUS VM, and the TFTP VM (140, `10.30.99.50`) for
  firmware. Optional: a second switch for stacking.
- **Track 2:** any controller option, or FGT-1 alone, plus the FreeRADIUS VM. No
  switch and no extra Fortinet software.
- **Knowledge:** the NSE 4 / FortiGate 7.6 Administrator level (Volume XIX,
  Chapters 03–09) and basic Layer 2 switching.

## See also

- [Volume XIX — Fortinet NSE Certification Program](../volume-019-fortinet-network-security/README.md),
  Chapter 10 (the restored NSE program and tracks) and Chapter 11 (Secure
  Networking upper levels; Lab 11.1, FortiSwitch over FortiLink).
- [Volume CLXXII — DISA SRGs and STIGs](../volume-172-disa-srgs-and-stigs/README.md),
  [Chapter 11](../volume-172-disa-srgs-and-stigs/chapters/11-fortiswitch-feature-version-and-srg-map.md)
  (FortiSwitch feature, version, and SRG map).
- [Volume CIX — Fortinet ISFW and VDOM Lab](../volume-109-fortinet-isfw-vdom-lab/README.md)
  — FortiGate-VM evaluation caveats and VDOMs.
- [Volume CM — Tim's Lab Gear](../volume-900-tims-lab-gear/README.md) — Proxmox,
  addressing, and FGT-1.
