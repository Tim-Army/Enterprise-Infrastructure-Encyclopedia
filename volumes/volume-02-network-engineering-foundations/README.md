# Volume II — Network Engineering Foundations

> Vendor-neutral enterprise networking: addressing, switching, routing, core
> services, wireless, resilient design, observability, and structured
> troubleshooting — the shared networking foundation every vendor-specific
> and higher-layer volume in this encyclopedia builds on.

## Overview

Volume II establishes vendor-neutral network engineering as a dependency
for the rest of the encyclopedia. It assumes Volume I's engineering
practices and conceptual foundations, and is itself named as a prerequisite
by Volume III (Cisco Enterprise Networking), Volume VII (Cloud
Infrastructure), Volume X (Enterprise Cybersecurity), and the
vendor-focused security and visibility volumes (XV, XVI, XVIII, XIX, XX) in
[ROADMAP.md](../../ROADMAP.md). Deep vendor-specific CLI and platform
configuration — Cisco IOS XE, Catalyst Center, and SD-Access — belongs to
Volume III and is deliberately not duplicated here; this volume teaches the
underlying protocols and design principles that vendor implementation
builds on.

The volume is organized as a progression from fundamentals to operations:

- **Chapters 01–04** cover foundational protocol and forwarding theory: the
  OSI/TCP-IP layered model and encapsulation, IPv4/IPv6 addressing and
  VLSM, Ethernet switching and VLANs with Layer 2 resilience, and IP
  routing fundamentals including static routing, OSPF, and BGP basics.
- **Chapters 05–06** cover the services and access technologies built on
  top of that foundation: DNS, DHCP, NTP, and NAT/PAT as core network
  services, and RF fundamentals, WLAN architecture, and wireless security
  as wireless foundations.
- **Chapters 07–09** zoom out to design and operations: hierarchical and
  spine-leaf network design with first-hop redundancy and resilience
  patterns, the observability stack (SNMP, syslog, flow telemetry,
  streaming telemetry) that makes a network's state knowable, and a
  structured troubleshooting and operations methodology that ties every
  earlier chapter's toolset together.

Every chapter follows the same structure — learning objectives, theory and
architecture, design considerations, implementation and automation,
validation and troubleshooting, security and best practices, references
and knowledge checks, a hands-on lab, and a summary and completion
checklist — defined in [templates/chapter.md](../../templates/chapter.md)
and enforced by [EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md).
Each hands-on lab is a reproducible, disposable exercise built primarily
with Linux network namespaces, `scapy`, and standard open-source tooling
(`dnsmasq`, `keepalived`, `chrony`), with a stated objective, prerequisites,
numbered steps, expected results, a negative test, and cleanup
instructions.

## Chapters

1. [Network Models and Protocol Architecture](chapters/01-network-models-and-protocol-architecture.md) — the OSI and TCP/IP layered models, encapsulation, PDUs, and standards bodies.
2. [IP Addressing and Subnetting](chapters/02-ip-addressing-and-subnetting.md) — IPv4/IPv6 address structure, CIDR, VLSM, route summarization, and public/private/shared address space.
3. [Ethernet Switching, VLANs, and Layer 2 Resilience](chapters/03-ethernet-switching-vlans-and-layer-2-resilience.md) — MAC learning, VLANs and trunking, Spanning Tree, and link aggregation.
4. [IP Routing Fundamentals](chapters/04-ip-routing-fundamentals.md) — the routing table and forwarding decision, static routing, OSPF area design, BGP fundamentals, and redistribution.
5. [Core Network Services](chapters/05-core-network-services.md) — DNS resolution and records, DHCP (DORA and relay), NTP stratum hierarchy, and NAT/PAT.
6. [Wireless Network Foundations](chapters/06-wireless-network-foundations.md) — RF fundamentals, 802.11 standard evolution, controller-based WLAN architecture, roaming, and WPA2/WPA3-Enterprise security.
7. [Enterprise Network Design and Resilience](chapters/07-enterprise-network-design-and-resilience.md) — hierarchical and spine-leaf design, first-hop redundancy protocols, ECMP, and redundant WAN edge design.
8. [Network Validation and Observability](chapters/08-network-validation-and-observability.md) — monitoring vs. observability vs. validation, SNMP, syslog, flow telemetry, streaming telemetry, and baselines.
9. [Network Troubleshooting and Operations](chapters/09-network-troubleshooting-and-operations.md) — structured troubleshooting methodology, the network change lifecycle, runbooks, root cause analysis, and post-incident review.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.

## Software and platform baseline

Chapters in this volume reference the dated baseline recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md) where a specific
platform version is cited (for example, Cisco IOS XE references that
anticipate Volume III). Protocol-level content (IPv4/IPv6, Ethernet,
802.11, DNS, DHCP, NTP, SNMP, syslog) is dated to the IETF/IEEE standards
cited in each chapter's references rather than to a single product
version, consistent with this volume's vendor-neutral scope.

## Building and validating this volume

From the repository root, after completing
[SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-02-network-engineering-foundations

# Build a single chapter.
scripts/bash/build-book.sh --format all \
  --chapter volumes/volume-02-network-engineering-foundations/chapters/09-network-troubleshooting-and-operations.md
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
