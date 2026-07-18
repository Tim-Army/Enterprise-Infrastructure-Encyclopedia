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
