# Volume III — Cisco Enterprise Networking

> Designing, deploying, automating, securing, and operating a modern Cisco
> enterprise campus, WAN, and wireless estate on Catalyst 9000 switching,
> Catalyst 9800 wireless, and IOS XE 17.x.

## Overview

Volume III applies the vendor-neutral networking foundations from
[Volume II](../volume-02-network-engineering-foundations/README.md) to
Cisco's current enterprise portfolio: Catalyst 9000 campus switching,
IOS XE routing and WAN transport, Catalyst 9800 wireless, Cisco
Identity Services Engine–backed access control, IOS XE programmability,
and Cisco Catalyst Center–managed SD-Access. Volume II is this volume's
declared dependency in [ROADMAP.md](../../ROADMAP.md); readers should be
comfortable with OSI/TCP-IP fundamentals, VLANs, routing protocol
concepts, and IP addressing before starting Chapter 1.

The volume is organized as a progression from platform fundamentals
through increasingly centralized operation:

- **Chapters 01–04** establish the Cisco Enterprise Architecture model,
  IOS XE platform fundamentals, campus switching and Layer 2/3
  resiliency, enterprise routing and path control, and WAN/internet-edge
  transport including Catalyst SD-WAN.
- **Chapters 05–07** cover the services layered on top of that
  foundation: wireless architecture and operations, QoS and application
  delivery, and identity-based access control and segmentation.
- **Chapters 08–09** move from per-device configuration to centralized
  operation: IOS XE model-driven programmability and automation, and
  Cisco Catalyst Center–managed SD-Access fabric with Assurance.

Every chapter follows the same structure — learning objectives, theory
and architecture, design considerations, implementation and automation,
validation and troubleshooting, security and best practices, references
and knowledge checks, a hands-on lab, and a summary and completion
checklist — defined in [templates/chapter.md](../../templates/chapter.md)
and enforced by [EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md).
Each hands-on lab is a reproducible, disposable exercise with a stated
objective, prerequisites, numbered steps, expected results, a negative
test, and cleanup instructions, built around Cisco Modeling Labs (CML),
physical Catalyst hardware, or a Cisco DevNet sandbox where the platform
(Catalyst Center) is not practically self-hosted in a small lab.

## Chapters

1. [Cisco Enterprise Architecture and IOS XE Foundations](chapters/01-cisco-enterprise-architecture-and-ios-xe-foundations.md) — the Cisco Enterprise Architecture model, hierarchical and routed-access campus design, Catalyst 9000 platform architecture, install vs. bundle mode, and Smart Licensing Using Policy.
2. [Catalyst Campus Switching and Resiliency](chapters/02-catalyst-campus-switching-and-resiliency.md) — VLANs and trunking, Rapid PVST+/MST, EtherChannel/LACP, HSRP/VRRP/GLBP, and StackWise-480/StackWise Virtual.
3. [Cisco Enterprise Routing and Path Control](chapters/03-cisco-enterprise-routing-and-path-control.md) — OSPF and EIGRP design, BGP at the enterprise edge, route redistribution and filtering, and VRF-lite macro-segmentation.
4. [Enterprise WAN, Internet Edge, and Catalyst SD-WAN](chapters/04-enterprise-wan-internet-edge-and-catalyst-sd-wan.md) — MPLS L3VPN, DMVPN Phase 3, dual-ISP internet edge design, and the Catalyst SD-WAN Manager/Controller/Validator/Edge architecture.
5. [Catalyst Wireless Architecture and Operations](chapters/05-catalyst-wireless-architecture-and-operations.md) — split-MAC CAPWAP architecture, Catalyst 9800 deployment models, RF fundamentals and RRM, WLAN/policy/tag configuration, and WPA3/802.11r-k-v.
6. [Cisco Network Services, QoS, and Application Delivery](chapters/06-cisco-network-services-qos-and-application-delivery.md) — DHCP/NTP/multicast services, the DiffServ trust-boundary model, MQC classification/marking/queuing/shaping, NBAR2, and PIM sparse mode/IGMP snooping.
7. [Cisco Identity, Access Control, and Segmentation](chapters/07-cisco-identity-access-control-and-segmentation.md) — TACACS+/RADIUS AAA, 802.1X with MAC Authentication Bypass, Cisco ISE policy roles, and TrustSec Security Group Tag micro-segmentation.
8. [IOS XE Programmability and Network Automation](chapters/08-ios-xe-programmability-and-network-automation.md) — YANG data models, NETCONF/RESTCONF/gNMI, model-driven telemetry, Guest Shell and EEM on-box automation, and off-box automation with the `cisco.ios` Ansible collection.
9. [Catalyst Center, SD-Access, Assurance, and Operations](chapters/09-catalyst-center-sd-access-assurance-and-operations.md) — Catalyst Center's Discovery/Inventory/LAN Automation/Provision workflow, SD-Access fabric roles, LISP/VXLAN, Virtual Networks and SGTs, and Assurance health scores and Path Trace.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine
  chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.

## Software and platform baseline

Chapters in this volume reference the dated baseline recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md): Cisco IOS XE 17.x on
the Catalyst 9000 series, and the current Catalyst Center SD-Access
release. Update that file, not individual chapters, when the baseline
changes.

## Certification alignment

This volume maps to the CCNA, CCNP Enterprise (ENCOR/ENARSI), and CCNP
Wireless (WLCOR/WLSD/WLSI) certification and training paths, as recorded
in [CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). Chapter
content describes blueprint domains and points to Cisco's official
training sources; it does not reproduce proprietary exam questions or
licensed courseware. Always confirm the current blueprint against Cisco
Learning & Certifications before using a chapter for exam preparation.

### The exams

| Exam | Version | Duration | Price (US) | Earns |
| --- | --- | --- | --- | --- |
| 200-301 CCNA | v1.1 | 120 min | $300 | CCNA |
| 350-401 ENCOR | v1.2 | 120 min | $400 | Enterprise Core specialist; core exam for CCNP Enterprise and CCIE Enterprise Infrastructure |
| 300-410 ENARSI | v1.1 | 90 min | $300 | Enterprise Advanced Infrastructure specialist; a CCNP Enterprise concentration |

CCNP Enterprise requires ENCOR plus one concentration exam; ENARSI is the
concentration this volume supports. All three use performance-based,
multiple-choice, and drag-and-drop question formats.

**A dated deadline worth planning around:** the last date to test CCNA
v1.1 is **2 February 2027**, with v2.0 first testable on 3 February 2027.
A reader starting CCNA close to that boundary should either finish
against v1.1 or prepare against v2.0 deliberately, not drift across it.

### Domain weights, mapped to this volume

**200-301 CCNA v1.1**

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Network Fundamentals | 20% | 01 |
| 2.0 Network Access | 20% | 02, 05 |
| 3.0 IP Connectivity | 25% | 03 |
| 4.0 IP Services | 10% | 06 |
| 5.0 Security Fundamentals | 15% | 07 |
| 6.0 Automation and Programmability | 10% | 08 |

**350-401 ENCOR v1.2**

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Architecture | 15% | 01, 04, 06, 09 |
| 2.0 Virtualization | 10% | 01, 04 |
| 3.0 Infrastructure | 30% | 02, 03, 06 |
| 4.0 Network Assurance | 10% | 09 |
| 5.0 Security | 20% | 07 |
| 6.0 Automation and Artificial Intelligence | 15% | 08 |

**300-410 ENARSI v1.1**

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Layer 3 Technologies | 35% | 03 |
| 2.0 VPN Technologies | 20% | 04 |
| 3.0 Infrastructure Security | 20% | 07 |
| 4.0 Infrastructure Services | 25% | 06 |

Infrastructure at 30% makes ENCOR a breadth exam: switching, routing,
wireless, and IP services together outweigh any single specialism. ENARSI
inverts that — Layer 3 alone is 35%, and the exam rewards depth in
troubleshooting rather than coverage.

### Study plans

Each plan assumes **8–10 hours per week**. Times are for a reader with
production networking exposure; someone new to enterprise networking
should plan roughly half again as long for CCNA.

**CCNA — six to eight weeks**

| Week | Focus | Chapters |
| --- | --- | --- |
| 1 | Architecture, IOS XE, addressing, and the CLI | 01 |
| 2 | Switching, VLANs, trunking, EtherChannel, spanning tree | 02 |
| 3 | Routing tables, static routing, single-area OSPFv2, FHRP | 03 |
| 4 | Wireless fundamentals and WLC operation | 05 |
| 5 | IP services: NAT, NTP, DHCP, DNS, SNMP, syslog, QoS basics | 06 |
| 6 | Security fundamentals, port security, ACLs, wireless security | 07 |
| 7 | Automation, APIs, JSON, controller-based networking | 08 |
| 8 | Full-blueprint review and timed practice | — |

**ENCOR — eight to ten weeks**

| Week | Focus | Chapters |
| --- | --- | --- |
| 1 | Architecture: design principles, high availability, SD-WAN and SD-Access working principles, **and QoS interpretation** — QoS sits in this domain in v1.2, not in Infrastructure | 01, 04, 06, 09 |
| 2 | Virtualization: VRF, GRE/IPsec, LISP and VXLAN concepts | 01, 04 |
| 3–5 | **The heavy weeks.** Infrastructure in full: Layer 2 trunking, EtherChannel and RSTP/MST; Layer 3 EIGRP/OSPF comparison, OSPFv2/v3 multi-area, eBGP, policy-based routing; IP services NTP/PTP, NAT/PAT, HSRP/VRRP, and multicast | 02, 03, 06 |
| 6 | Network assurance: debugs, Flexible NetFlow, SPAN/RSPAN/ERSPAN, IP SLA, Catalyst Center, NETCONF/RESTCONF | 09 |
| 7–8 | Security: device access control, infrastructure security features, REST API security, network security design | 07 |
| 9 | Automation and AI: Python, JSON, YANG, Catalyst Center and SD-WAN Manager APIs, EEM applets, agent vs. agentless | 08 |
| 10 | Review weighted to Infrastructure and Security, then timed practice | — |

**Do not study wireless for ENCOR.** Version 1.2 removed it entirely —
the exam topics contain no reference to wireless, WLC, roaming, or access
points. [Chapter 05](chapters/05-catalyst-wireless-architecture-and-operations.md)
remains required for **CCNA**, whose Network Access domain still covers
Cisco wireless architectures, AP modes, WLAN components, and the WLC GUI.
It is simply not ENCOR material any more — that content moved to the new
professional wireless track, covered in **The CCNP Wireless track**
below.

**ENARSI — four to six weeks**, taken after ENCOR while the routing
material is fresh.

| Week | Focus | Chapters |
| --- | --- | --- |
| 1–2 | Layer 3: EIGRP, OSPF, BGP, redistribution, route policy | 03 |
| 3 | VPN technologies: MPLS, DMVPN, IPsec, SD-WAN context | 04 |
| 4 | Infrastructure security: ACLs, control-plane policing, device access | 07 |
| 5 | Infrastructure services: DHCP, logging, SLA, NetFlow, troubleshooting | 06 |
| 6 | Troubleshooting drills against deliberately broken topologies | — |

Sequence the path CCNA → ENCOR → ENARSI. ENCOR and ENARSI overlap enough
that taking ENARSI within a few months of ENCOR saves re-learning the
routing material.

### The CCNP Wireless track

Cisco split wireless into its own professional track on **19 March
2026**, realigning the content that ENCOR v1.2 removed. CCNP Wireless
requires the `WLCOR` core exam plus **one** concentration exam, and
`WLCOR` also replaces ENCOR as the qualifying written exam for **CCIE
Wireless** (renamed from CCIE Enterprise Wireless). Cisco highly
recommends the Understanding Cisco Wireless Foundations (WLFNDU)
training as foundation knowledge before attempting the track.

| Exam | Title | Duration | Role in the track |
| --- | --- | --- | --- |
| **350-101 WLCOR** v1.0 | Implementing and Operating Cisco Wireless Core Technologies | 120 min | Core — required for CCNP Wireless and CCIE Wireless |
| **300-110 WLSD** v1.2 | Designing Cisco Wireless Networks | 90 min | Concentration |
| **300-120 WLSI** v1.2 | Implementing Cisco Wireless Advanced Solutions | 90 min | Concentration |

All are delivered through Pearson VUE. Question counts, cut scores, and
pricing are set per exam and are not restated here; confirm them at
registration.

**350-101 WLCOR v1.0**

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 RF Fundamentals | 15% | 05 |
| 2.0 802.11 Technology Fundamentals | 10% | 05 |
| 3.0 Wireless Network Implementation | 10% | 05, 09 |
| 4.0 Wireless Network Operation | 20% | 05, 07, 09 |
| 5.0 Client Connectivity Configuration | 20% | 05, 07 |
| 6.0 Wireless Monitoring and Management | 15% | 05, 09 |
| 7.0 Automation and AI | 10% | 08, 09 |

**300-110 WLSD v1.2**

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Wireless Site Survey | 25% | 05 |
| 2.0 Wired and Wireless Infrastructure | 30% | 02, 05 |
| 3.0 Mobility | 25% | 05 |
| 4.0 WLAN High Availability | 20% | 05 |

**300-120 WLSI v1.2**

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 FlexConnect | 15% | 05 |
| 2.0 QoS on a Wireless Network | 10% | 06 |
| 3.0 Multicast | 10% | 03, 06 |
| 4.0 Location Services | 10% | 09 |
| 5.0 Advanced Location Services | 10% | 09 |
| 6.0 Security for Wireless Client Connectivity | 20% | 05, 07 |
| 7.0 Monitoring | 15% | 09 |
| 8.0 Device Hardening | 10% | 07 |

Be clear-eyed about depth. [Chapter 05](chapters/05-catalyst-wireless-architecture-and-operations.md)
anchors the track — CAPWAP split-MAC architecture, Catalyst 9800
deployment models, AP modes, RF fundamentals, fast roaming, tags and
profiles — and chapters 02–09 carry the wired, QoS, multicast, identity,
automation, and assurance domains. But the concentrations reach beyond
this volume: WLSD's site-survey methodology (25% of that exam) and
WLSI's location services (20% across its two location domains) are
wireless-specialist material with no dedicated chapter here. Treat this
volume as the architecture-and-operations backbone and pair it with
wireless-specific lab time on a Catalyst 9800 — the 9800-CL virtual
controller runs in Cisco Modeling Labs.

**WLCOR — eight weeks**, using the same 8–10 hours per week as the plans
above:

| Week | Focus | Chapters |
| --- | --- | --- |
| 1 | RF fundamentals and 802.11: propagation, signal measurements, antennas, governance, bands and channels, MIMO — a quarter of the exam | 05 |
| 2–3 | **The heavy block at 30%.** Implementation and operation: architectures (local, mesh, fabric, cloud), physical infrastructure, AP discovery and join, AP modes, WLAN access, client policy across WLC, Catalyst Center, ISE, and Spaces | 05, 09 |
| 4–5 | Client connectivity: WLAN authentication on and off the controller, client-side configuration, roaming, guest networking | 05, 07 |
| 6 | Monitoring and management: maintenance, client monitoring, connectivity troubleshooting, platform integrations | 05, 09 |
| 7 | Automation and AI: Python, NETCONF/YANG, wireless APIs, AI analytics, AI operations, and AI-RRM in Catalyst Center | 08, 09 |
| 8 | Full-blueprint review and timed practice | — |

Then take the concentration within a few months, three to four weeks
each: for **WLSD**, weight study toward wired and wireless
infrastructure (30%) and site surveys (25%), and practice a predictive
survey end to end; for **WLSI**, weight it toward client security (20%)
and the FlexConnect-plus-monitoring pair (30% together), and lab CWA and
LWA flows against ISE before exam day.

### Study materials

This volume is written to stand on its own, but the Cisco path rewards
pairing reading with a lab and a practice-exam bank:

| Role | Resource | Why |
| --- | --- | --- |
| Official blueprint | [Cisco Learning Network exam topics](https://learningnetwork.cisco.com/s/ccna-exam-topics) | Authority on domains, weights, and version — outranks any third-party material where they disagree |
| Reference text | Cisco Press Official Cert Guide (Odom for CCNA; Hucaby for ENCOR) | Blueprint-ordered and thorough; the closest thing to a canonical text |
| Video course | Jeremy's IT Lab (free, CCNA); CBT Nuggets or INE for CCNP | Jeremy's IT Lab is unusually complete for a free course; CCNP-level video is thinner and worth paying for |
| Practice exams | Boson ExSim-Max | Consistently the closest simulation of Cisco question style, with explanations that reason through the distractors |
| Lab | Cisco Packet Tracer (CCNA); Cisco Modeling Labs, EVE-NG, or GNS3 (CCNP) | Packet Tracer covers the CCNA blueprint; CCNP needs real IOS XE images |
| Official training | [Cisco U.](https://u.cisco.com/) | Guided paths, hands-on labs, and prep bundles from Cisco directly |

Build the topologies rather than reading about them. Cisco's
performance-based questions test configuration and troubleshooting under
time pressure, which passive study does not develop.

### CCIE lab readiness

Two expert-level labs sit above this volume's professional tracks, each
reached by first passing the matching core written exam (ENCOR for
Enterprise Infrastructure, WLCOR for Wireless):

| Lab | Version | Qualifying written |
| --- | --- | --- |
| **CCIE Enterprise Infrastructure** | v1.1 | 350-401 ENCOR |
| **CCIE Wireless** (renamed from CCIE Enterprise Wireless) | v1.1 | 350-101 WLCOR |

Both are **eight-hour, hands-on practical exams** in the standard CCIE
two-module shape: a **3-hour Design** module (scenario-based, no device
access — the reasoning skills of [Volume XXX](../volume-30-cisco-ccde-network-design/README.md)
applied to one track) followed by a **5-hour Deploy, Operate, and
Optimize** module on real equipment, over a **dual-stack (IPv4 and
IPv6)** network, with programmability and automation expected
throughout. Cisco is adding a **new AI module** to its CCIE practical
exams — confirm the current format at registration. The CCIE Wireless
lab now incorporates **Cisco Meraki** alongside Wi-Fi 6 and Wi-Fi 7,
and its written qualifier moved from ENCOR to WLCOR.

**What the lab adds over this volume.** These chapters build the
knowledge and the configuration skills at professional depth; the lab
tests something further — **speed, integration, and troubleshooting
under time pressure**. You must configure complex multi-technology
topologies quickly and correctly, diagnose deliberately broken
scenarios, and keep an eight-hour pace. That is a distinct skill from
knowing the technology, and it is built only by doing full-scale timed
labs, not by reading.

**How to prepare.** Build complete topologies in Cisco Modeling Labs
(the standalone Catalyst 9000v/IOS XE nodes for Enterprise
Infrastructure; a 9800-CL controller for Wireless), and rehearse them
repeatedly against the clock — a full scenario end to end, then the
same scenario broken for you to fix. Pair every chapter's Hands-On Lab
with a timed rebuild, drill the Design module using the CCDE-style
method in [Volume XXX](../volume-30-cisco-ccde-network-design/README.md),
and use Cisco's official CCIE practice labs and equipment-rental or
BYOD options to work on the real platforms before exam day. Confirm the
current lab blueprint and format on the Cisco Learning Network before
scheduling — CCIE lab topics are separate documents from the written
exam topics and change independently.

## Topic-level lab coverage

Every exam topic across **all current Cisco Enterprise certifications** — the
CCNP Enterprise core and concentrations, the wireless implementation exam,
the assurance and cloud-connectivity exams, and CCIE Enterprise
Infrastructure — is covered by a hands-on **walkthrough** lab or a Design
Exercise. Exam topics were harvested from Cisco's official exam-topics PDFs
(`learningcontent.cisco.com/documents/marketing/exam-topics`) on 24 July
2026. Labs use IOS XE CLI, Python (Netmiko/ncclient/requests), Ansible,
NETCONF/RESTCONF and model-driven telemetry, and the Catalyst Center /
vManage / Meraki / ThousandEyes REST APIs; each carries
`**Lab verified by:** *pending*` until a human runs it.

| Certification | Exam | Coverage |
| --- | --- | --- |
| CCNA | 200-301 | Domains 1–6 across Chapters 01–03, 05–08 (see alignment tables) |
| CCNP Ent. Core / CCIE written | 350-401 ENCOR | Domains 1–6 across Chapters 01–09 |
| CCNP Ent. concentration | 300-410 ENARSI | Ch. 03 (L3), 04 (VPN), 06–07 (services, security) |
| CCNP Ent. concentration | 300-415 ENSDWI | Chapter 04, Labs 4.4–4.29 |
| CCNP Ent. concentration | 300-420 ENSLD | Chapter 08 **Design Exercise** |
| CCNP Ent. concentration | 300-435 ENAUTO | Chapter 08, Labs 8.1–8.35 |
| CCNP Ent. concentration | 300-425 ENWLSD | Chapter 05 **Design Exercise** |
| CCNP Ent. concentration | 300-430 ENWLSI | Chapter 05, Labs 5.7–5.35 |
| CCNP Ent. concentration | 300-440 ENCC | Chapter 04 SD-WAN/cloud/IPsec labs (4.3–4.23) |
| CCNP Ent. concentration | 300-445 ENNA | Chapter 09, Labs 9.8–9.29 |
| **CCIE Enterprise Infrastructure** | written 350-401 + 8-hr lab | see module map below |

The CCNA, ENCOR, and ENARSI blueprint domains and their chapter mappings are
in the **Certification alignment** section above; every domain resolves to
the topic-level labs in the mapped chapters. The three implementation
concentrations map one lab per exam topic:

**ENSDWI 300-415 → Chapter 4**

| Exam topic | Lab |
| --- | --- |
| 1.1 Describe Cisco SD-WAN architecture and components | Lab 4.4 |
| 1.2 Describe Cisco SD-WAN Edge platforms and capabilities | Lab 4.5 |
| 1.3 Describe Cisco SD-WAN Cloud OnRamp | Lab 4.6 |
| 2.1 Describe controller cloud deployment | Lab 4.7 |
| 2.2 Describe controller on-premises deployment | Lab 4.8 |
| 2.3 Configure certificates and device lists | Lab 4.9 |
| 2.4 Troubleshoot control plane connectivity | Lab 4.10 |
| 3.1 Describe WAN Edge deployment | Lab 4.11 |
| 3.2 Configure Cisco SD-WAN data plane | Lab 4.12 |
| 3.3 Configure OMP | Lab 4.13 |
| 3.4 Configure TLOCs | Lab 4.14 |
| 3.6 Configure CLI and vManage feature configuration templates | Lab 4.15 |
| 3.7 Describe configuration groups, feature profiles, and workflows | Lab 4.16 |
| 4.1 Configure control policies | Lab 4.17 |
| 4.2 Configure data policies | Lab 4.18 |
| 4.3 Configure end-to-end segmentation | Lab 4.19 |
| 4.4 Configure Cisco SD-WAN application-aware routing | Lab 4.20 |
| 4.5 Configure direct Internet access | Lab 4.21 |
| 5.1 Configure service insertion | Lab 4.22 |
| 5.2 Describe Cisco SD-WAN security features | Lab 4.23 |
| 5.3 Describe Cloud security integration | Lab 4.24 |
| 5.4 Configure QoS treatment on WAN Edge routers | Lab 4.25 |
| 5.5 Describe Application Quality of Experience (App-QoE) | Lab 4.26 |
| 6.1 Describe authentication, monitoring, and reporting from vManage | Lab 4.27 |
| 6.2 Configure authentication, monitoring, and reporting | Lab 4.28 |
| 6.3 Describe REST API monitoring | Lab 4.29 |
| 6.4 Describe software image management from vManage | Lab 4.30 |

**ENAUTO 300-435 → Chapter 8**

| Exam topic | Lab |
| --- | --- |
| 1.1 Utilize common version control operations with git (add, clone, push, commit, diff, | Lab 8.1 |
| 1.2 Describe characteristics of API styles (REST and RPC) | Lab 8.2 |
| 1.3 Describe the challenges encountered and patterns used when consuming APIs | Lab 8.3 |
| 1.4 Interpret Python scripts containing data types, functions, classes, conditions, and | Lab 8.4 |
| 1.5 Describe the benefits of Python virtual environments | Lab 8.5 |
| 1.6 Explain the benefits of using network configuration tools such as Ansible and Terraform | Lab 8.6 |
| 2.1 Identify the JSON instance based on a YANG model (including YANG Suite) | Lab 8.7 |
| 2.2 Identify the XML instance based on a YANG model (including YANG Suite) | Lab 8.8 |
| 2.3 Interpret a YANG module tree generated per RFC8340 | Lab 8.9 |
| 2.4 Compare functionality, benefits, and uses of OpenConfig, IETF, and native YANG models | Lab 8.10 |
| 2.5 Compare functionality, benefits, and uses of NETCONF and RESTCONF | Lab 8.11 |
| 3.1 Implement device management and monitoring using NetMiko | Lab 8.12 |
| 3.2 Construct a Python script using ncclient that uses NETCONF to manage and monitor an | Lab 8.13 |
| 3.3 Configure device using RESTCONF API utilizing Python requests library | Lab 8.14 |
| 3.4 Utilize Ansible to configure an IOS XE device | Lab 8.15 |
| 3.5 Configure a subscription for model driven telemetry on an IOS XE device (CLI, NETCONF, | Lab 8.16 |
| 3.6 Compare publication and subscription telemetry models | Lab 8.17 |
| 3.7 Describe the benefits and usage of telemetry data in troubleshooting the network | Lab 8.18 |
| 3.8 Describe Day 0 provisioning methods | Lab 8.19 |
| 4.1 Compare traditional versus software-defined networks | Lab 8.20 |
| 4.2 Describe the features and capabilities of Cisco DNA Center | Lab 8.21 |
| 4.3 Implement Cisco DNA Center event outbound webhooks | Lab 8.22 |
| 4.4 Implement API requests for Cisco DNA Center to accomplish network management tasks | Lab 8.23 |
| 4.5 Implement API requests for Cisco DNA Center to accomplish network management tasks | Lab 8.24 |
| 4.6 Troubleshoot Cisco DNA Center automation process using Intent APIs | Lab 8.25 |
| 5.1 Describe features and capabilities of Cisco SD-WAN vManage APIs | Lab 8.26 |
| 5.2 Implement a Python script to perform API requests for Cisco SD-WAN vManage Device | Lab 8.27 |
| 5.3 Construct API requests for Cisco SD-WAN vManage Administration APIs | Lab 8.28 |
| 5.4 Implement a Python script to perform API requests for Cisco SD-WAN vManage | Lab 8.29 |
| 5.5 Construct API requests for Cisco SD-WAN vManage Monitoring APIs (including real-time) | Lab 8.30 |
| 5.6 Troubleshoot a Cisco SD-WAN deployment using vManage APIs | Lab 8.31 |
| 6.1 Describe features and capabilities of Cisco Meraki | Lab 8.32 |
| 6.2 Create a network using Cisco Meraki APIs | Lab 8.33 |
| 6.3 Configure a network using Cisco Meraki APIs | Lab 8.34 |
| 6.4 Implement a Python script for Cisco Meraki Alert WebHooks | Lab 8.35 |

**ENWLSI 300-430 → Chapter 5**

| Exam topic | Lab |
| --- | --- |
| 1.1 Deploy FlexConnect components such as switching and operating modes | Lab 5.7 |
| 1.2 Deploy FlexConnect capabilities | Lab 5.8 |
| 1.3 Implement Office Extend | Lab 5.9 |
| 2.1 Implement QoS schemes based on requirements including wired to wireless mapping | Lab 5.10 |
| 2.2 Implement QoS for wireless clients | Lab 5.11 |
| 2.3 Implement AVC including Fastlane (only on WLC) | Lab 5.12 |
| 3.1 Implement multicast components | Lab 5.13 |
| 3.2 Describe how multicast can affect wireless networks | Lab 5.14 |
| 3.3 Implement multicast on a WLAN | Lab 5.15 |
| 3.4 Implement mDNS | Lab 5.16 |
| 3.5 Implement Multicast Direct | Lab 5.17 |
| 4.1 Deploy CMX and Cisco Spaces on a wireless network | Lab 5.18 |
| 4.2 Implement location services | Lab 5.19 |
| 5.1 Implement CMX and Cisco Spaces components | Lab 5.20 |
| 5.2 Implement location-aware guest services using custom portal and Facebook Wi-Fi | Lab 5.21 |
| 5.3 Troubleshoot location accuracy using Cisco Hyperlocation | Lab 5.22 |
| 5.4 Troubleshoot CMX high availability | Lab 5.23 |
| 5.5 Implement wIPS using Cisco DNA Center | Lab 5.24 |
| 6.1 Configure client profiling on WLC and ISE | Lab 5.25 |
| 6.2 Implement BYOD and guest | Lab 5.26 |
| 6.3 Implement 802.1X and AAA on different wireless architectures and ISE | Lab 5.27 |
| 6.4 Implement Identity-Based Networking on different wireless architectures (VLANs, QoS, | Lab 5.28 |
| 7.1 Utilize reports on PI and Cisco DNA center | Lab 5.29 |
| 7.2 Manage alarms and rogues (APs and clients) | Lab 5.30 |
| 7.3 Manage RF interferers | Lab 5.31 |
| 7.4 Troubleshoot client connectivity | Lab 5.32 |
| 8.1 Implement device access controls (including RADIUS and TACACS+) | Lab 5.33 |
| 8.2 Implement access point authentication (including 802.1X) | Lab 5.34 |
| 8.3 Implement control plane ACLs on the controller | Lab 5.35 |

**ENCC 300-440 (Enterprise Cloud Connectivity)** — the connectivity
(internet/private/SaaS to AWS/Azure/GCP), IPsec-to-cloud, SD-WAN Cloud
OnRamp, and SD-WAN-policy topics map to Chapter 04's SD-WAN and VPN labs
(4.3, 4.6, 4.16–4.23); the recommend/design and cloud-native-security topics
draw on the same labs plus the Chapter 08 design reasoning.

**ENNA 300-445 (Enterprise Network Assurance)** — the 23 topics map to
Chapter 09 Labs 9.8–9.29 (ThousandEyes/Meraki/Catalyst Center assurance),
with ENCOR's assurance domain in Labs 9.2–9.7.

### CCIE Enterprise Infrastructure

The CCIE EI **written qualifier is 350-401 ENCOR**, fully covered above. The
8-hour hands-on **lab** blueprint is expert-depth application of the same
technologies; its modules map to this volume's labs:

| CCIE EI lab module | Chapters / labs |
| --- | --- |
| Network Infrastructure (L2/L3) | Chapters 02 (switching), 03 (routing) |
| Software-Defined Infrastructure | Chapters 04 (SD-WAN), 09 (SD-Access) |
| Transport Technologies and Solutions | Chapter 04 (MPLS, DMVPN, VPN) |
| Infrastructure Security and Services | Chapters 06 (services, QoS), 07 (security) |
| Infrastructure Automation | Chapter 08 (Python, NETCONF/RESTCONF, telemetry) |

## Building and validating this volume

From the repository root, after completing
[SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-03-cisco-enterprise-networking

# Build a single chapter.
scripts/bash/build-book.sh --format all \
  --chapter volumes/volume-03-cisco-enterprise-networking/chapters/09-catalyst-center-sd-access-assurance-and-operations.md
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
