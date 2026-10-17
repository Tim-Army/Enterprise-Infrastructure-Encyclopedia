# Chapter 01: Lab Overview, Topology, and Exam Map

## Learning Objectives

- State what this volume builds, who it is for, and how it relates to the
  Fortinet NSE 5 FortiSwitch exam.
- Describe the exam's public facts: name, code, product versions, format, and
  its four domains and fifteen tasks.
- Explain the difference between **FortiLink mode** (a FortiSwitch managed by a
  FortiGate) and **standalone mode** (a FortiSwitch configured on its own).
- Choose a controller option (C1, C2, or C3) and a switch option (S1, S2, or
  S3), or Track 2, and know exactly which labs each choice runs hands-on.
- Read the topology for each controller option and the single addressing plan
  that every chapter uses.
- Find the labs that cover each exam task.

## How to Use This Guide

### What this lab is

This is a build-it-yourself lab volume for the **Fortinet NSE 5 FortiSwitch 7.6
Administrator** exam. It covers the two ways a FortiSwitch is run:

- **FortiLink mode (managed mode).** A FortiGate acts as the **switch
  controller**. The switch is discovered over a **FortiLink interface** on the
  FortiGate, authorized, and then configured entirely from the FortiGate:
  VLANs, ports, Spanning Tree, 802.1X, NAC, QoS, and monitoring. Most of the
  exam, and most of this volume, is FortiLink mode.
- **Standalone mode.** The same FortiSwitch is configured through its own
  FortiSwitchOS CLI or GUI, or from FortiEdge Cloud. Chapter 11 converts the lab
  switch to standalone mode for Layer 2, Layer 3, and ACL work.

The volume is for an infrastructure engineer who already works at the NSE 4 /
FortiGate 7.6 Administrator level (see
[Volume XIX](../../volume-019-fortinet-network-security/README.md), Chapters
03–09) and knows basic Layer 2 switching. It is a lab, not a course: each
chapter builds, breaks, and verifies something, and the exam map at the end of
this chapter shows which lab practices which exam task.

There is no FortiSwitch virtual machine. Fortinet staff on the Fortinet
Community have said that no FortiSwitch VM image exists for any virtual
environment, and that no FSW-VM image is publicly available
([2022 thread](https://community.fortinet.com/t5/Support-Forum/FortiSwitch-OS/m-p/203053),
[2023 thread](https://community.fortinet.com/t5/Support-Forum/vSwitch-for-Lab-and-Exam-Preparation/m-p/251383)).
Hands-on switching therefore needs a physical switch. That is why the volume
has two tracks.

### The exam

All facts in this section come from Fortinet's public exam and course pages and
Pearson VUE's Fortinet exam list, checked on 2026-10-16. The volume does not
reproduce Fortinet courseware or exam questions; check the official pages before
you book.

| Item | Public fact |
| --- | --- |
| Exam name | Fortinet NSE 5 - FortiSwitch 7.6 Administrator |
| Exam code | NSE5_FSW_AD-7.6 (the only FortiSwitch exam on the Pearson VUE list; no 8.0 version is listed) |
| Program position | Secure Networking track, NSE 5 level (see [Volume XIX, Chapter 10](../../volume-019-fortinet-network-security/chapters/10-the-restored-nse-program-and-the-four-tracks.md)) |
| Product versions | FortiSwitchOS 7.6 and FortiOS 7.6 |
| Format | 70 minutes, 35–40 questions, pass or fail, English and Japanese |
| Delivery | Pearson VUE; status Available |
| Recommended preparation | The FortiSwitch 7.6 Administrator course; the FortiSwitch 7.6 Administration Guide, FortiLink Guide, and FortiSwitchOS CLI Reference; at least six months of hands-on experience |

The exam page says the exam tests applied knowledge of FortiLink management,
provisioning, configuration, operation, and day-to-day administration, and of
FortiSwitch in standalone mode. It also says that questions can include
topologies, configuration extracts, and troubleshooting captures. That last
point is the basis of this volume's **read-and-predict** exercises.

Pearson VUE posted two notices in 2026: OnVUE online delivery ended for
"certain exams" from 21 September 2026, and NSE exam fees change on 2 November
2026. This volume records no fee; check Pearson VUE for delivery options and the
current price.

The exam's four domains and fifteen tasks are below. The task IDs (1.1 to 4.3)
are this volume's own shorthand; the task names follow Fortinet's published
topic list.

| Domain | Task | Task name |
| --- | --- | --- |
| 1. FortiSwitch concepts | 1.1 | Configure VLANs using FortiSwitch |
| | 1.2 | Use QoS and LLDP-MED on FortiSwitch |
| | 1.3 | Configure the ports required for stack deployment |
| | 1.4 | Configure switching and routing on FortiSwitch |
| | 1.5 | Configure STP to prevent network loops |
| | 1.6 | Configure switch ports, split port, and available transceivers |
| 2. Deployment and management | 2.1 | Configure and provision FortiSwitch |
| | 2.2 | Deploy FortiSwitch supported deployment topologies |
| | 2.3 | Deploy and configure FortiSwitch in a multi-tenancy environment |
| 3. Layer 2 control and security | 3.1 | Use port security options on FortiSwitch |
| | 3.2 | Use filtering and antispoofing techniques on FortiSwitch |
| | 3.3 | Use ACLs, security profiles, and VLAN security mechanisms on FortiSwitch |
| 4. Monitoring and troubleshooting | 4.1 | Use packet capturing methods to monitor and troubleshoot traffic issues |
| | 4.2 | Troubleshoot FortiLink issues |
| | 4.3 | Use tools to view and extract network information from FortiSwitch |

Fortinet's matching course is FortiSwitch Administrator (self-paced or
instructor-led, with FortiGate 7.6 Administrator as its prerequisite). Its
agenda is public, but its lab list is not. This volume's labs are built from the
public FortiOS 7.6 and FortiSwitchOS 7.6.7 documentation, not from the course.

**Sources:**
[Fortinet exam page](https://training.fortinet.com/local/staticpage/view.php?page=fortiswitch_administrator_exam),
[Fortinet course page](https://training.fortinet.com/local/staticpage/view.php?page=library_fortiswitch-administrator),
[Pearson VUE Fortinet exam list](https://wsr.pearsonvue.com/testtaker/registration/examlist/FORTINET?locale=en_US),
[Pearson VUE Fortinet notices](https://home.pearsonvue.com/fortinet).

### The two tracks

**Track 1 — a real switch.** A physical FortiSwitch running FortiSwitchOS 7.6
is managed over FortiLink by a FortiGate running FortiOS 7.6 (any controller
option C1–C3). The same switch is converted to standalone mode in Chapter 11.
This is the only track that gives hands-on switching experience.

**Track 2 — FortiGate only.** No switch. Use any controller option, or FGT-1
(the lab's FortiGate-VM evaluation) alone. Everything that is FortiGate
configuration is built live: the switch controller, the FortiLink interface
(with no link), switch VLAN interfaces and DHCP, initial-config templates, STP
settings, storm-control, LLDP and QoS profiles, the 802.1X security policy, a
RADIUS server tested with `diagnose test authserver` against a real FreeRADIUS
VM, NAC and dynamic port policies, quarantine, ACL objects, IGMP snooping,
SNMP, sFlow, remote logging, switch profiles, a pre-provisioned managed-switch
entry, firewall policies, and the VDOM objects for multi-tenancy. Every task
that needs a switch becomes a read-and-predict exercise.

Track 2 **cannot** exercise:

- Discovery and authorization of a switch, or a firmware push to it.
- Any live switch state: connection status, STP, LLDP neighbors, the MAC
  table, 802.1X sessions, MCLAG, or ARP inspection.
- Per-port configuration that needs the switch's port list (whether FortiOS
  accepts it for a pre-provisioned switch is tested in Chapter 02).
- STP convergence or a real loop; real 802.1X or MAB supplicants.
- DHCP snooping and dynamic ARP inspection enforcement.
- An MCLAG or ISL forming; packet capture on switch ports; sFlow samples.
- Any of standalone FortiSwitchOS (Chapter 11 is read-and-predict only).

Track 2 prepares you for the exam's configuration-extract and
troubleshooting-capture questions. It gives **no hands-on switching
experience**. If you can, do Track 1.

### Read-and-predict

A read-and-predict step shows a real output shape taken from the FortiOS 7.6 or
FortiSwitchOS 7.6.7 documentation (for example, the table that
`execute switch-controller get-conn-status` prints), asks you to predict one
field before you read on, and then gives the answer and the reason. Track 2 uses
these for every switch-dependent step. Track 1 uses them only where your
hardware lacks a feature (see the capability matrix below).

## Platform Options

The volume supports every combination of one controller option and one switch
option below, plus Track 2. Pick one of each before Chapter 02.

### Controller options (the FortiLink controller)

| Option | Controller | FortiLink attachment | Limits to know |
| --- | --- | --- | --- |
| **C1** | A used hardware **FortiGate 40F or 60F** running FortiOS 7.6 | The switch cables directly to a FortiGate port; no Proxmox NIC changes | Managed-switch maximum: 8 on the 40F, 24 on the 60F (FortiLink Guide 7.6.7, p. 12) |
| **C2** | **FGT-1**, the FortiGate-VM evaluation on Proxmox (VM 120, FortiOS 7.6) | FGT-1 `port3` becomes the FortiLink port, on a dedicated Proxmox NIC (plain bridge) or PCI passthrough; VLAN 202 is unavailable while the lab runs | Evaluation caps: 3 interfaces, 3 firewall policies, 3 routes, 2 VDOMs but only one *traffic* VDOM (Volume CIX Chapter 07), low encryption only. **FortiLink on the evaluation license is unconfirmed**: Chapter 02 runs a go/no-go test, with C1 or C3 as the fallbacks |
| **C3** | A **licensed FortiGate-VM** on Proxmox (no evaluation caps); the plan assumes FGT-1 with a full license | A new `port4` becomes the FortiLink port, on a dedicated NIC or passthrough as in C2; VLAN 202 stays in service | Managed-switch maximum: 8 on a FortiGate-VM01, more on larger VM licenses (FortiLink Guide 7.6.7, p. 12) |

The evaluation caps come from the FortiOS 7.6.0 Administration Guide,
[Permanent trial mode for FortiGate-VM](https://docs.fortinet.com/document/fortigate/7.6.0/administration-guide/441460).
The guide does not say whether VLAN subinterfaces count against the interface
cap. A Fortinet staff answer on the Fortinet Community (2023, FortiOS 7.2.2 and
later) says VLAN and physical interfaces count together, which would leave no
room for the lab VLANs on C2. Lab 4.1 tests it as a go/no-go step and gives the
fallbacks. FortiLink is not supported
when the FortiGate is in transparent mode (FortiLink Guide 7.6.7, p. 12), so every
controller runs in NAT mode. Check the FortiLink Compatibility table for your
FortiOS and FortiSwitchOS versions in Chapter 02.

### Switch options (Track 1)

| Option | Switch | Feature-matrix column | Why choose it |
| --- | --- | --- | --- |
| **S1** | **FS-108F** (any POE/FPOE variant) | 1xxE, 1xxF | The cheapest. Loses sFlow, flow export, and on-switch packet capture, FortiLink-mode ACLs, and MCLAG |
| **S2** | **FS-124F** (FS-124F-POE or -FPOE for PoE and an LLDP-MED phone) | 1xxE, 1xxF | The recommended single switch. Loses FortiLink-mode ACLs (ACLs run in standalone mode) and MCLAG |
| **S3** | A **pair of FS-2xx switches**, for example FS-224E or FS-248E | 200 Series | Adds hands-on MCLAG, FortiLink-mode ACLs, IP source guard, RSPAN/ERSPAN, and a redundant (dual-homed) FortiLink |

A single FS-108F or FS-124F can be joined by a second switch of any model for the
stacking lab (Lab 6.2); without one, that lab is read-and-predict.

### Capability matrix

Every cell below was checked against the **Feature Matrix for FortiSwitchOS
7.6.7** (`temp/fsw/FSW-7.6.7-Feature-Matrix.pdf`). In that PDF the first mark
column is **GUI** support, not a model; the FS-108F and FS-124F share the
**1xxE, 1xxF** column, and FS-2xx models are in the **200 Series** column. A
chain icon means supported in standalone and managed mode; a check mark means
standalone mode only; a dash means not supported. Where a cell lists models (for
example "124F, 148E, 148F"), only those models in the column have the feature.

**Key:** **Live** = hands-on in FortiLink mode. **Live (SA)** = hands-on in
standalone mode only. **Build + predict** = FortiGate objects built live, switch
behavior read-and-predict. **Predict** = read-and-predict only. **Design** =
a design exercise.

| Labs | Feature group | S1 FS-108F | S2 FS-124F | S3 FS-2xx pair | Track 2 | Feature-matrix basis (7.6.7) |
| --- | --- | --- | --- | --- | --- | --- |
| 2.1–2.5 | Baseline, FortiLink interface, physical path, firmware, shared services | Live | Live | Live | Build + predict (2.3, 2.4 predict) | Not a matrix row (controller and lab setup) |
| 3.1–3.5 | Discovery, authorization, templates, firmware push, switch profiles, retire | Live | Live | Live | Build + predict (3.1, 3.3, 3.5 predict) | Centralized configuration and centralized firmware management: chain in both columns |
| 4.1–4.2 | FortiSwitch VLANs, access and trunk ports | Live | Live | Live | Build (4.1) + predict (4.2) | Note 7 limits only VLANs that block intra-VLAN traffic (16 on FS-108F and FS-124F); it is not a general VLAN limit; 4,095 on other models |
| 4.3 | Port properties, LAG, PoE, transceivers, cable test | Live (PoE on POE/FPOE only) | Live (PoE on POE/FPOE only) | Live | Predict | LAG size 8 in both columns; PoE rows apply only to POE/FPOE models (note 1); TDR chain in both; no transceiver row |
| 4.4 | Split port | Predict | Predict | Predict | Predict | Dash in both columns; only the 500 Series, FS-1024E/1048E/T1024E/T1024F-FPOE, and FS-3032E have it |
| 4.5 | Routing: FortiGate inter-VLAN routing, switch static routes | Live (static routes IPv4 only when managed) | Live (static routes IPv4 only when managed) | Live (static routes IPv4 only when managed) | Build (FortiGate) + predict (switch) | Static routing chain in both (note 9: IPv4 only in managed mode); inter-VLAN routing offload dash in both (note 19: advanced license, larger models only) |
| 5.1–5.3 | MSTP, edge ports, root guard, BPDU guard, loop guard, RPVST+ interoperation | Live | Live | Live | Build (5.1) + predict (5.2, 5.3) | MSTP instances 0–31; root guard, BPDU guard, loop guard, Rapid PVST interoperation: chain in both; RPVST+ VLANs 32 (1xx) or 64 (200) |
| 6.1 | FortiLink redundancy (FortiLink LAG, dual-homed FortiLink) | Live with C1 (factory `fortilink` aggregate); predict with C2/C3 | Live with C1 (factory `fortilink` aggregate); predict with C2/C3 | Live with C1 (factory `fortilink` aggregate); predict with C2/C3 | Predict | Not a matrix row; it needs a second FortiLink port in an aggregate. C2's interface cap does not allow one; on C3, FortiGate-VM aggregate support is undocumented and the Proxmox bridge cannot pass LACP (Chapter 06) |
| 6.2 | Stacking: auto-ISL and inter-switch trunks | Live with a second switch, else predict | Live with a second switch, else predict | Live | Predict | Not a matrix row; Auto topology chain in both columns |
| 6.3 | MCLAG pair and tiered MCLAG | Predict | Predict | Live | Predict | MCLAG: dash in 1xxE/1xxF, chain in 200 Series; STP and IGMP snooping in MCLAG: chain in 200 Series |
| 6.4 | Topology selection (HA FortiGate, FortiLink over Layer 3, islands) | Design + predict | Design + predict | Design + predict | Design + predict | Not a matrix row (FortiLink Guide topology chapter) |
| 7.1 | RADIUS server and user group on the controller | Live | Live | Live | Live | Not a matrix row (FortiGate only) |
| 7.2–7.3 | 802.1X port-based and MAC-based, MAB, guest and auth-fail VLANs, dynamic VLAN | Live | Live | Live | Build + authserver test + predict | 802.1X port mode, MAC-based mode, MAB, user-based VLAN assignment: chain in both |
| 7.4 | MAC learning limit, sticky MAC | Live (no per-VLAN limit) | Live (no per-VLAN limit) | Live (no per-VLAN limit on FS-248E-POE/-FPOE; violation action standalone only) | Predict | MAC learning limit and sticky MAC chain in both; note 3; learning-limit violation action: chain in 1xxE/1xxF, check in 200 Series; learning-limit violation log: check (standalone only) in 1xxE/1xxF and 200 Series, so an empty log is a valid result |
| 8.1 | DHCP snooping, trusted ports, option 82, rogue server test | Live (25 VLANs max) | Live (25 VLANs max) | Live | Build + predict | DHCP snooping and option 82 chain in both; note 15: 25 VLANs on FS-1xx models |
| 8.2 | Dynamic ARP inspection; IP source guard | Live (DAI); predict (IP source guard) | Live (DAI); predict (IP source guard) | Live (both) | Build + predict | DAI chain in both; IP source guard dash in 1xxE/1xxF, chain in 200 Series |
| 8.3 | Storm control | Live (no high-rate or rate-filter settings) | Live (no high-rate or rate-filter settings) | Live | Build + predict | Storm control chain in both; note 21 for FS-1xx models |
| 8.4 | ACLs in FortiLink mode | Predict; do Lab 11.4 (standalone) | Predict; do Lab 11.4 (standalone) | Live | Build ACL objects + predict | ACL (IPv4 ingress): check in 1xxE/1xxF (note 16 names FS-108F and FS-124F as having no ACL in FortiLink mode), chain in 200 Series |
| 8.5 | Block intra-VLAN traffic, native VLAN hygiene, private VLANs | Live; private VLANs predict | Live; private VLANs predict | Live; private VLANs Live (SA) | Build + predict | Block intra-VLAN traffic chain in both; private VLANs dash in 1xxE/1xxF, check in 200 Series |
| 9.1–9.3 | Device detection, NAC policies, dynamic port policies, quarantine | Live; LAN segments predict (note 12: no FS-108F directly connected to the FortiGate) | Live | Live (adds network device detection; NAC device telemetry only on models in the FortiLink Guide p. 205 list, which omits the plain FS-248E) | Build + predict | NAC, dynamic port policies, host quarantine, device detection: chain in both; network device detection and NAC device telemetry: dash in 1xxE/1xxF, chain in 200 Series |
| 9.4 | IGMP snooping | Live (5 VLANs max) | Live (5 VLANs max) | Live | Build + predict | IGMP snooping chain in both; note 23: 5 VLANs on FS-1xx models |
| 10.1 | LLDP profiles, LLDP-MED voice policy | Live | Live | Live | Build + predict | LLDP transmit and LLDP-MED chain in both |
| 10.2 | QoS maps, QoS policies, queue policies | Live (one QoS map; no marking or queue counters) | Live (one QoS map; no marking or queue counters) | Live; QoS marking (ACL remark action) Live (SA) in Chapter 11 | Build + predict | 802.1p queuing chain in both; note 18: one QoS map on FS-1xx; QoS marking dash in 1xxE/1xxF, check in 200 Series; QoS queue counters dash in 1xxE/1xxF, chain in 200 Series |
| 10.3–10.4 | Multi-tenancy: switch ports for VDOMs, shared ports | Live within the controller's VDOM limits | Live within the controller's VDOM limits | Live within the controller's VDOM limits | Build (C2: multi-VDOM mode only; the tenant VDOM is an expected NO-GO, since the evaluation allows one traffic VDOM and root must stay one) + predict | Not a matrix row (FortiGate VDOM feature) |
| 11.1–11.3 | Standalone first boot, VLANs, trunks, SVIs, static routes | Live (SA) | Live (SA) | Live (SA) | Predict | SVI and static routing chain in both; FS-1xx software-based routing only, 200 Series hardware-based routing |
| 11.4 | Standalone ingress ACLs and ACL services | Live (SA) | Live (SA) | Live (SA) | Predict | ACL (IPv4 ingress) and ACL service: check or chain in both; prelookup and egress ACLs dash in both; FS-1xx limits classifiers and actions (Admin Guide p. 293), so no remark action on S1/S2 |
| 11.5 | FortiEdge Cloud; moving a standalone configuration to FortiLink | Live (SA) with a FortiCloud account, else predict | Live (SA) with a FortiCloud account, else predict | Live (SA) with a FortiCloud account, else predict | Predict | FortiEdge Cloud configuration: check in both |
| 12.1 | MAC table, LLDP neighbors, port statistics, topology | Live | Live | Live | Predict | Port-statistics CLI and MAC notification trap chain in both |
| 12.2 | SNMP, sFlow, flow export | SNMP Live; sFlow and flow export predict | Live | Live | Build + predict | SNMP OID chain in both; sFlow chain, 1xx cell "124F, 148E, 148F"; flow export chain, 1xx cell "124F, 148F"; both chain in 200 Series |
| 12.3 | Packet capture: FortiGate sniffer, on-switch capture, RSPAN/ERSPAN, port mirror | FortiGate sniffer and SPAN Live; on-switch capture and RSPAN predict | FortiGate sniffer, on-switch capture, SPAN Live; RSPAN predict | Live | Predict | Packet capture chain, 1xx cell "124F, 148E, 148F", chain in 200 Series; SPAN chain in both; RSPAN and ERSPAN dash in 1xxE/1xxF, chain in 200 Series |
| 12.4 | FortiLink fault clinic | Live | Live | Live | Predict | Not a matrix row (troubleshooting) |
| 12.5–12.6 | Hardening against Volume CLXXII, teardown | Live | Live | Live | Build (FortiGate side only) | Syslog collection chain in both |

Three details are easy to miss. The FS-108F and FS-124F share a column, so they
differ only where a cell names models (sFlow, flow export, packet capture) or a
note names one of them (note 12, NAC LAN segments, names the FS-108F). In the
200 Series column, notes name individual models: the FS-248E-POE and
FS-248E-FPOE lack the per-VLAN and per-trunk MAC learning limit (note 3, which
also lists the FS-248D), and FortiSwitchOS image signature verification is not
supported on the FS-224D-FPOE and FS-248D (note 17); check your exact model against the notes. FortiLink
redundancy, stacking, and multi-tenancy have no matrix row at all; they depend
on the topology and the controller, so Chapter 06 and Chapter 10 verify them
against the FortiLink Guide 7.6.7.

For the model-by-model SRG view of the same features, see
[Volume CLXXII, Chapter 11](../../volume-172-disa-srgs-and-stigs/chapters/11-fortiswitch-feature-version-and-srg-map.md).

## Topology and Addressing

### The single addressing plan

One addressing plan serves every option. Only the physical attachment of the
FortiLink port and the controller's own interface names change.

| Item | Address or ID | Notes |
| --- | --- | --- |
| FortiLink interface (controller) | `10.255.1.1/24` | Alias `fortilink` on every option |
| Switch-controller reserved network | `10.255.0.0/16` | FortiOS default |
| FortiSwitch FortiLink address | `10.255.1.2` | First FortiLink DHCP lease; the S3 second switch's lease is recorded in Lab 6.2 as `<FSWB_IP>` |
| FortiLink management VLAN | 4094 | FortiOS default |
| Auto-created VLANs | default 1, quarantine 4093 (`10.255.11.1/24`), rspan 4092 (`10.255.12.1/24`), voice 4091, video 4090, onboarding 4089 (NAC), nac-segment (`10.255.13.1/24`) | FortiOS initial-config templates (FortiLink Guide 7.6.7, pp. 34–35) |
| VLAN 1741 `fsw-users` | `10.174.41.0/24`, gateway `.1`, DHCP `.100`–`.199` | Users and 802.1X (Chapters 04, 07) |
| VLAN 1742 `fsw-voice` | `10.174.42.0/24`, gateway `.1` | LLDP-MED voice (Chapter 10) |
| VLAN 1743 `fsw-iot` | `10.174.43.0/24`, gateway `.1` | NAC and dynamic port policy target (Chapter 09) |
| VLAN 1744 `fsw-guest` | `10.174.44.0/24`, gateway `.1` | Guest and auth-fail VLAN (Chapter 07) |
| VLAN 1745 `fsw-tenant` | `10.174.45.0/24`, gateway `.1` | Tenant VDOM (Chapter 10) |
| Zone `FSW-LAN` | VLANs 1741–1744 | One policy covers them all |
| Standalone switch management | `10.30.99.174/24`, gateway `10.30.99.1` | Switch management port on the Nexus, access VLAN 99 (Chapter 11) |
| FreeRADIUS VM `radius-174` | `10.200.0.174` on VLAN 200 | New VM, built in Chapter 02 |
| Collector on `ubuntu-ws` | `10.200.0.20` on VLAN 200 | sFlow, flow export, syslog |
| TFTP VM 140 | `10.30.99.50` | Switch firmware |

The lab VLAN IDs (1741–1745) do not collide with the existing lab tags in
[Volume CM](../../volume-900-tims-lab-gear/README.md). The lab adds only five
VLANs of its own. Feature matrix note 7's limit of 16 "access VLANs" on the
FS-108F and FS-124F belongs to the "Block intra-VLAN traffic" row: it counts only
VLANs with intra-VLAN blocking enabled, not every VLAN (Chapter 04 explains).

The controller's own interfaces depend on the option:

| Role | C1 hardware FortiGate | C2 FGT-1 evaluation | C3 FGT-1 licensed |
| --- | --- | --- | --- |
| WAN and out-of-band (VLAN 99) | `<WAN_PORT>` `10.30.99.175/24`, gateway `10.30.99.1` | `port1` `10.30.99.99/24` | `port1` `10.30.99.99/24` |
| Services (VLAN 200) | `<SVC_PORT>` `10.200.0.175/24` | `port2` `10.200.0.1/24` | `port2` `10.200.0.1/24` |
| FortiLink | `<FL_PORT>` `10.255.1.1/24` | `port3` `10.255.1.1/24` | `port4` `10.255.1.1/24` |

On C1, the VLAN 200 hosts keep FGT-1 (`10.200.0.1`) as their gateway, so the
C1 policy toward the services segment must use source NAT; Chapter 02 builds it.
If C3 is a licensed FortiGate-VM other than FGT-1, give it the C1 addresses.

Switch ports, the same on every switch option because every model has at least
eight ports:

| Switch port | Use |
| --- | --- |
| `<FSW_FL_PORT>` | FortiLink uplink to the controller (Chapter 02 names it per model) |
| `port1` | Endpoint A: users, 802.1X supplicant |
| `port2` | Endpoint B: MAB, NAC, rogue DHCP server tests |
| `port5` and `port6` | Patch cable between them for the STP loop lab (Chapter 05) |
| Management port | Nexus `Eth1/<free>`, access VLAN 99; used in standalone mode (Chapter 11) |

### Topology C1: hardware FortiGate

The switch cables straight to the FortiGate. Proxmox is not changed.

```text
   UCGF (10.30.99.1) ---- Nexus 9396PX ---------------------------+
                           |  acc VLAN 99        |  acc VLAN 200   |  acc VLAN 99
                           |                     |                 |
                  <WAN_PORT> 10.30.99.175   <SVC_PORT> 10.200.0.175 |
                 +----------------------------------+              |
                 |  FortiGate 40F/60F  FortiOS 7.6  |              |
                 |  <FL_PORT> "fortilink" 10.255.1.1 |              |
                 +-----------------|----------------+              |
                                   | FortiLink (VLANs 1741-1745,    |
                                   | 4089-4094 tagged)              |
                             <FSW_FL_PORT>                  mgmt port 10.30.99.174
                 +----------------------------------+    (standalone, Ch 11)
                 |  FortiSwitch (S1/S2/S3) 10.255.1.2 |-------------+
                 +--port1-----port2-----port5==port6--+
                      |         |          (loop cable, Ch 05)
                 endpoint A  endpoint B
   VLAN 200 on proxmox-1 (via the Nexus): radius-174 10.200.0.174, ubuntu-ws 10.200.0.20
```

### Topology C2 and C3: FortiGate-VM on Proxmox

A FortiGate-VM needs a direct Layer 2 path to the switch. Add a dedicated
physical NIC to proxmox-1 and either attach it to a new plain Linux bridge
`vmbrFL` (not VLAN-aware, STP off, `group_fwd_mask` 16384 so LLDP frames pass)
or pass the NIC through to the VM with PCI passthrough. Cable that NIC directly
to the switch. Do not route FortiLink through the Nexus: it would consume LLDP
and STP BPDUs, and a VLAN-tagged vNIC drops the other switch-controller VLANs.

```text
   UCGF (10.30.99.1) -- Nexus 9396PX ---------------------------------+
                          | Eth1/18 acc VLAN 99 (vmbr1)                | acc VLAN 99
   +----------------------|---- proxmox-1 ---------------------+      |
   | vmbr1 (VLAN 99) ---- port1 10.30.99.99                    |      |
   | vmbr2 (VLAN 200) --- port2 10.200.0.1 --- radius-174 .174 |      |
   |                                       \-- ubuntu-ws .20   |      |
   |                 [ FGT-1  FortiOS 7.6 ]                    |      |
   | vmbrFL or passthrough (new NIC)                           |      |
   |   C2: port3  /  C3: port4   "fortilink" 10.255.1.1/24     |      |
   |   VLANs 1741-1745 and 4089-4094 ride on this port         |      |
   +-----------------------|-----------------------------------+      |
                           | FortiLink                                 |
                     <FSW_FL_PORT>                           mgmt port 10.30.99.174
                 +----------------------------------+     (standalone, Ch 11)
                 |  FortiSwitch (S1/S2/S3) 10.255.1.2 |--------------+
                 +--port1-----port2-----port5==port6--+
                      |         |          (loop cable, Ch 05)
                 endpoint A  endpoint B
```

On C2, `port3` leaves VLAN 202 for the duration of the volume and returns in
Lab 12.6. On C3, `port4` is new and VLAN 202 is untouched.

### Topology S3: the switch pair

With S3, both switches sit below the controller. `FSW-A` keeps `10.255.1.2`
and the standalone address; `FSW-B` takes a FortiLink lease, recorded in Lab 6.2. The pair is
joined by an inter-switch link, which becomes the MCLAG peer link in Lab 6.3. On
C1, when its FortiLink port is the factory `fortilink` aggregate, the controller
can dual-home FortiLink to both switches (Lab 6.1). On C2 the interface cap
allows only a single FortiLink port, and on C3 FortiGate-VM aggregate support is
undocumented, so dual-homing is read-and-predict on both.

```text
                  [ controller "fortilink" 10.255.1.1 ]
                     |                         :  (second FortiLink link,
                     |                         :   C1 aggregate only, Lab 6.1)
            +--------+--------+       +--------+--------+
            |  FSW-A 10.255.1.2 |=====| FSW-B <FSWB_IP>  |
            +--port1--port2-----+ ISL / MCLAG peer link +---+
                 |      |               (Labs 6.2, 6.3)
            endpoint A  endpoint B
```

### Topology for Track 2

Track 2 uses the controller alone. On C2, `port3` is still taken from VLAN 202
and configured as the FortiLink interface with no link. VLANs 1741–1745 and every
switch-controller object exist, and `radius-174` and `ubuntu-ws` are reached
through `port2` (or the C1 services port).

### The C2 policy and interface budget

The evaluation allows three firewall policies. The plan uses:

| Policy | From | To | Purpose |
| --- | --- | --- | --- |
| P1 | `FSW-LAN` | `port1` | NAT to the internet and updates |
| P2 | `fortilink` and `FSW-LAN` | `port2` | RADIUS 1812/1813, syslog, sFlow 6343, SNMP traps |
| P3 | Chapter-specific | Chapter-specific | One lab policy per chapter (for example the tenant VDOM or NAC VLAN), swapped as needed |

Count FGT-1's existing VLAN 200 and VLAN 202 policies first; Chapter 02 does so.
C1 and C3 have no such cap.

## Exam Objective to Lab Map

Every exam task has at least one primary lab. "Track 2 mode" says how a
FortiGate-only reader covers it.

| Task | Primary labs | Supporting labs | Track 2 mode |
| --- | --- | --- | --- |
| 1.1 VLANs | 4.1, 4.2, 11.2 | 3.2, 8.5 | Build 4.1 and 3.2; predict 4.2 and 11.2 |
| 1.2 QoS and LLDP-MED | 10.1, 10.2 | 9.2 | Build + predict |
| 1.3 Stack ports | 6.2 | 6.1, 3.1 | Predict |
| 1.4 Switching and routing | 4.3, 4.5, 11.3 | 12.1 | Build FortiGate routing; predict the switch |
| 1.5 STP | 5.1, 5.2, 5.3 | 11.2 | Build 5.1; predict 5.2 and 5.3 |
| 1.6 Ports, split port, transceivers | 4.3, 4.4 | — | Predict (4.4 is predict on both tracks) |
| 2.1 Configure and provision | 2.2, 3.1, 3.2, 3.3, 3.4 | 3.5, 11.1, 11.5 | Build 2.2, 3.2, 3.4; predict 3.1, 3.3 |
| 2.2 Topologies | 6.1, 6.3, 6.4 | 6.2 | Design + predict |
| 2.3 Multi-tenancy | 10.3, 10.4 | — | Build within the controller's VDOM limits + predict |
| 3.1 Port security | 7.2, 7.3, 7.4 | 7.1 | Build + authserver test + predict |
| 3.2 Filtering and antispoofing | 8.1, 8.2, 8.3 | 7.4 | Build + predict |
| 3.3 ACLs, security profiles, VLAN security | 8.4, 8.5, 9.1, 9.3, 11.4 | 7.2 | Build + predict |
| 4.1 Packet capture | 12.3 | 8.1 | Predict (the live FortiGate sniffer on FortiLink is Track 1 only) |
| 4.2 FortiLink troubleshooting | 12.4 | 2.3, 3.1, 3.5 | Predict the fault signatures |
| 4.3 View and extract information | 12.1, 12.2 | 5.1, 7.2, 8.2 | Predict |

In 3.3, the 802.1X security policy of Lab 7.2 is the FortiSwitch "security
profile". Topics from the course agenda that the exam list does not name are
also covered: IGMP snooping (Lab 9.4), SNMP and sFlow (Lab 12.2), quarantine
(Lab 9.3), and FortiEdge Cloud (Lab 11.5).

## Using This Volume

### Chapter order

Work the chapters in order. Chapter 02 prepares the controller, the switch, and
the shared services, and contains the C2 go/no-go test. Chapters 03–10 work in
FortiLink mode. Chapter 11 converts the switch to standalone mode. Chapter 12
monitors, troubleshoots, hardens, and tears down the lab, returning FGT-1's
`port3` to VLAN 202 on C2.

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | Lab Overview, Topology, and Exam Map | — |
| 02 | Lab Preparation | 2.1–2.5 |
| 03 | FortiLink Provisioning and the Managed-Switch Lifecycle | 3.1–3.5 |
| 04 | VLANs, Switch Ports, Transceivers, and Routing | 4.1–4.5 |
| 05 | Spanning Tree and Loop Protection | 5.1–5.3 |
| 06 | Layer 2 Design: FortiLink Redundancy, Stacking, and MCLAG | 6.1–6.4 |
| 07 | Port Security: 802.1X, MAB, Dynamic VLANs, and MAC Limits | 7.1–7.4 |
| 08 | Filtering, Antispoofing, ACLs, and VLAN Security | 8.1–8.5 |
| 09 | NAC, Dynamic Port Policies, Quarantine, and Multicast | 9.1–9.4 |
| 10 | QoS, LLDP-MED, and Multi-Tenancy | 10.1–10.4 |
| 11 | Standalone FortiSwitch: Layer 2, Layer 3, and FortiEdge Cloud | 11.1–11.5 |
| 12 | Monitoring, Troubleshooting, Hardening, and Teardown | 12.1–12.6 |

### The shape of every lab

Each lab is headed `### Lab N.M — <title>` and has the same parts:

1. **Objective** — what the lab proves.
2. **Platform notes** — one line before the steps saying which options run the
   lab hands-on and which use the read-and-predict steps, plus any
   option-specific differences (FortiGate hardware port names versus `port3` or
   `port4`; switch port counts).
3. **Track 1** walkthrough.
4. **Track 2** walkthrough, or **Track 2: read-and-predict**.
5. **Expected result**, a **Negative test**, and **Rollback**.

Each chapter after this one ends with a **Lab Verification** block whose
"Lab verified by" and "Date" fields stay *pending* until someone runs the labs
end to end.

### Versions and sources

The volume is written against FortiOS 7.6 and FortiSwitchOS 7.6.x. FortiGate
commands are checked against the FortiOS 7.6.0 CLI Reference and the FortiLink
Guide (FortiOS 7.6.7). Switch-local commands are checked against the
FortiSwitchOS 7.6.7 CLI Reference and Administration Guide. Model support comes
from the FortiSwitchOS 7.6.7 feature matrix. FortiSwitchOS 8.0 references are
used only as a cross-check, and any 8.0-only syntax is flagged.

### Related volumes

- [Volume XIX](../../volume-019-fortinet-network-security/README.md) places NSE 5
  in the Fortinet program. Its
  [Lab 11.1](../../volume-019-fortinet-network-security/chapters/11-secure-networking-upper-levels-switching-wireless-and-management.md#lab-111--fortiswitch-managed-over-fortilink-topic-fortiswitch)
  adopts a FortiSwitch over FortiLink in a few commands; this volume expands that
  lab into a full exam lab.
- [Volume CLXXII, Chapter 11](../../volume-172-disa-srgs-and-stigs/chapters/11-fortiswitch-feature-version-and-srg-map.md)
  maps FortiSwitch features to DISA SRG requirements; Lab 12.5 reuses its
  commands after re-checking them against 7.6.7.
- [Volume CM](../../volume-900-tims-lab-gear/README.md) describes the physical
  lab: proxmox-1, the Nexus, the UCGF, FGT-1, and the existing VLANs.

## Conventions

| Convention | Meaning |
| --- | --- |
| **Track 1** | Steps on a real FortiSwitch managed by the controller (C1, C2, or C3) |
| **Track 2** | Steps on the controller alone; switch behavior is read-and-predict |
| **C1, C2, C3** | Controller options: hardware FortiGate, FGT-1 evaluation, licensed FortiGate-VM |
| **S1, S2, S3** | Switch options: FS-108F, FS-124F, FS-2xx pair |
| `FGT #` | FortiOS CLI on the controller, whichever option you use |
| `FSW #` | FortiSwitchOS CLI on the switch (console or SSH) |
| `bash` block | The Proxmox host or a Linux endpoint |
| `<SWITCH_SN>`, `<FL_PORT>` | Placeholders; replace them with your values |

## Summary and Completion Checklist

This volume is a two-track lab for NSE5_FSW_AD-7.6. Track 1 manages a real
FortiSwitch from a FortiGate and later runs it standalone; Track 2 builds every
FortiGate-side object and predicts the rest, but gives no hands-on switching. The
capability matrix shows which labs each switch option runs live, and the exam map
shows that every one of the fifteen exam tasks has a primary lab.

- [ ] I can name the exam, its code, its format, and its four domains.
- [ ] I have chosen a controller option (C1, C2, or C3) or Track 2.
- [ ] I have chosen a switch option (S1, S2, or S3) and read its row limits in
      the capability matrix.
- [ ] I know what Track 2 cannot exercise.
- [ ] I have read the topology for my controller option and the addressing plan.
- [ ] I can find the primary lab for any exam task.
