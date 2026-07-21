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

This volume maps to the CCNA and CCNP Enterprise (ENCOR/ENARSI)
certification and training paths, as recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). Chapter
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
| 1.0 Architecture | 15% | 01, 09 |
| 2.0 Virtualization | 10% | 01, 04 |
| 3.0 Infrastructure | 30% | 02, 03, 05, 06 |
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
| 1 | Enterprise architecture, campus design, high availability | 01 |
| 2 | Virtualization: VRF, GRE/IPsec, LISP and VXLAN concepts | 01, 04 |
| 3–4 | Infrastructure: advanced switching and multi-area OSPF, BGP | 02, 03 |
| 5 | Infrastructure: wireless architecture, roaming, RF | 05 |
| 6 | Infrastructure: QoS and application delivery | 06 |
| 7 | Network assurance: SNMP, NetFlow, SPAN, IP SLA, Assurance | 09 |
| 8 | Security: access control, segmentation, device hardening | 07 |
| 9 | Automation and AI: Python, REST, YANG/NETCONF, Catalyst Center | 08 |
| 10 | Review weighted to Infrastructure, then timed practice | — |

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
