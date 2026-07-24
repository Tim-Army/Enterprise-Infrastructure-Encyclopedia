# Volume XXXI — Juniper Networks Certification Tracks

The Juniper certification program, end to end: Junos OS foundations,
the eight current tracks, and the expert-level practicals — with every
exam code verified against Juniper's certification pages and the labs
built on free vJunos images and Juniper vLabs.

## Overview

Juniper's program spans four levels (Associate, Specialist,
Professional, Expert) across eight tracks, all standing on one
operating system. This volume teaches the technology of each track at
certification depth — enterprise campus, service provider core, SRX
security, EVPN-VXLAN data centers, automation, Mist AI operations, and
design — and closes with JNCIE lab readiness. One volume, one Junos,
every track.

## Certification alignment

This volume maps to the Juniper (JNCIA/JNCIS/JNCIP/JNCIE) certification
tracks, as recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md).
Chapter content describes exam scope and points to Juniper's official
objectives lists; it does not reproduce proprietary exam questions or
licensed courseware. Always confirm the current exam code and
objectives on Juniper's certification pages before registering — this
program refreshes codes frequently.

### The exams

Verified against Juniper's certification track pages on **22 July
2026**. Every written exam is 90 minutes, 65 multiple-choice questions,
delivered by Pearson VUE; every JNCIE is a six-hour practical delivered
by Juniper. JNCIA-Junos is the prerequisite for the ENT and SP
specialist exams; each JNCIE requires its track's JNCIP.

| Track | Associate | Specialist | Professional | Expert |
| --- | --- | --- | --- | --- |
| Enterprise Routing & Switching | JNCIA-Junos **JN0-106** | JNCIS-ENT **JN0-352** | JNCIP-ENT **JN0-650** | JNCIE-ENT **JPR-946** |
| Service Provider Routing & Switching | JNCIA-Junos **JN0-106** | JNCIS-SP **JN0-364** | JNCIP-SP **JN0-664** | JNCIE-SP **JPR-962** |
| Security | JNCIA-SEC **JN0-232** | JNCIS-SEC **JN0-336** | JNCIP-SEC **JN0-637** | JNCIE-SEC **JPR-935** |
| Data Center | JNCIA-DC **JN0-281** | JNCIS-DC **JN0-481** | JNCIP-DC **JN0-683** | JNCIE-DC **JPR-981** |
| Automation & DevOps | JNCIA-DevOps **JN0-224** | JNCIS-DevOps **JN0-423** | — | — |
| Cloud | JNCIA-Cloud **JN0-214** | — | — | — |
| Mist AI | JNCIA-MistAI **JN0-253** | JNCIS-MistAI-Wireless **JN0-452** / JNCIS-MistAI-Wired **JN0-460** | JNCIP-MistAI **JN0-750** | — |
| Design | JNCIA-Design **JN0-1103** | — | — | — |

**Recent movements to know.** JN0-106 replaced JN0-105 when the older
JNCIA-Junos retired on 5 April 2026; the JNCIS-ENT refreshed in April
2026 (JN0-352) and the JNCIE-ENT in July 2026 — **JPR-946** first
delivered 13 July 2026, succeeding JPR-944, so confirm which code your
booking date carries. JNCIS-SP (JN0-364) is written to Junos OS 25.2,
JNCIS-SEC (JN0-336) and JNCIS-DevOps (JN0-423) to 24.4. The JNCIS-ENT
is an accepted alternative prerequisite for the JNCIP-DC. Domain lists
and weights live on each exam's page on Juniper's certification site —
that page is the authority this volume defers to.

## Chapters

1. [Junos OS Foundations and the JNCIA-Junos](chapters/01-junos-os-foundations-and-the-jncia-junos.md)
2. [Enterprise Routing and Switching — JNCIS-ENT to JNCIP-ENT](chapters/02-enterprise-routing-and-switching-jncis-ent-to-jncip-ent.md)
3. [Service Provider Routing and Switching — MPLS and the Core](chapters/03-service-provider-routing-and-switching-mpls-and-the-core.md)
4. [Juniper Security — SRX from JNCIA-SEC to JNCIP-SEC](chapters/04-juniper-security-srx-from-jncia-sec-to-jncip-sec.md)
5. [Data Center Fabrics — EVPN-VXLAN and the DC Track](chapters/05-data-center-fabrics-evpn-vxlan-and-the-dc-track.md)
6. [Automation, DevOps, and Cloud — Junos as Code](chapters/06-automation-devops-and-cloud-junos-as-code.md)
7. [Mist AI and the AI-Driven Enterprise](chapters/07-mist-ai-and-the-ai-driven-enterprise.md)
8. [Network Design and the JNCIA-Design](chapters/08-network-design-and-the-jncia-design.md)
9. [JNCIE Lab Readiness and Certification Operations](chapters/09-jncie-lab-readiness-and-certification-operations.md)

## Track-to-chapter alignment

| Track | Chapters |
| --- | --- |
| Enterprise Routing & Switching | 01, 02, 09 |
| Service Provider | 01, 03, 09 |
| Security | 01, 04, 09 |
| Data Center | 01, 05, 09 |
| Automation & DevOps / Cloud | 01, 06 |
| Mist AI | 07 (with 02 for wired foundations) |
| Design | 08 (drawing on all) |

## Topic-level lab coverage

Every exam objective of the **associate and specialist written exams** across all
Juniper tracks documented in this volume is covered by a hands-on Junos **walkthrough**
lab; the **JNCIA-Design** track is covered by the Chapter 08 Design Exercise, and the
**JNCIE** practical tracks by the Chapter 09 integrative timed-build labs. Objectives
were harvested from Juniper's official per-exam pages on
`juniper.net/us/en/training/certification` on 24 July 2026. Labs use the Junos CLI
(operational and configuration modes), SRX security, EVPN-VXLAN and Apstra, Junos
automation (PyEZ, Ansible, NETCONF/gNMI, YANG), and the Juniper Mist cloud/API.
Each carries `**Lab verified by:** *pending*` until a human runs it. **60 numbered
labs** plus a Design Exercise, one lab per exam objective:

**JNCIA-Junos JN0-106 → Chapter 01**

| Exam objective | Lab |
| --- | --- |
| Networking Fundamentals | Lab 1.1 |
| Junos OS Fundamentals | Lab 1.2 |
| User Interfaces | Lab 1.3 |
| Configuration Basics | Lab 1.4 |
| Operational Monitoring and Maintenance | Lab 1.5 |
| Routing Fundamentals | Lab 1.6 |
| Routing Policy and Firewall Filters | Lab 1.7 |

**JNCIS-ENT JN0-352 → Chapter 02**

| Exam objective | Lab |
| --- | --- |
| Layer 2 Switching and VLANs | Lab 2.1 |
| Spanning Tree | Lab 2.2 |
| Layer 2 Security | Lab 2.3 |
| Protocol-Independent Routing | Lab 2.4 |
| OSPF | Lab 2.5 |
| IS-IS | Lab 2.6 |
| BGP | Lab 2.7 |
| IP Tunnels | Lab 2.8 |
| High Availability | Lab 2.9 |

**JNCIS-SP JN0-364 → Chapter 03**

| Exam objective | Lab |
| --- | --- |
| Protocol-Independent Routing | Lab 3.1 |
| OSPF | Lab 3.2 |
| IS-IS | Lab 3.3 |
| BGP | Lab 3.4 |
| Layer 2 Bridging or VLANs | Lab 3.5 |
| Spanning-Tree Protocols | Lab 3.6 |
| MPLS | Lab 3.7 |
| IPv6 | Lab 3.8 |
| Tunnels | Lab 3.9 |
| High Availability | Lab 3.10 |

**JNCIS-SEC JN0-336 → Chapter 04**

| Exam objective | Lab |
| --- | --- |
| IDP | Lab 4.1 |
| IPsec VPN | Lab 4.2 |
| Juniper Advanced Threat Prevention Cloud | Lab 4.3 |
| HA Clustering | Lab 4.4 |
| Identity-Aware Security Policies | Lab 4.5 |
| SSL Proxy | Lab 4.6 |
| Security Director | Lab 4.7 |

**JNCIS-DC JN0-481 → Chapter 05**

| Exam objective | Lab |
| --- | --- |
| Data Center Architectures | Lab 5.1 |
| Juniper Apstra Architecture | Lab 5.2 |
| Apstra Design Phase | Lab 5.3 |
| Apstra Build and Deploy Phases | Lab 5.4 |
| Blueprint Operations | Lab 5.5 |
| Data Center Multitenancy | Lab 5.6 |
| Intent-Based Analytics | Lab 5.7 |

**JNCIS-DevOps JN0-423 (+ JNCIA-DevOps/Cloud) → Chapter 06**

| Exam objective | Lab |
| --- | --- |
| Platform Automation Overview | Lab 6.1 |
| gRPC | Lab 6.2 |
| Ansible | Lab 6.3 |
| Junos Automation Scripts | Lab 6.4 |
| YANG | Lab 6.5 |
| foundational — JNCIA-DevOps | Lab 6.6 |
| foundational — JNCIA-DevOps | Lab 6.7 |
| foundational — JNCIA-Cloud | Lab 6.8 |

**JNCIA-MistAI JN0-253 → Chapter 07**

| Exam objective | Lab |
| --- | --- |
| Juniper Mist Cloud Fundamentals | Lab 7.1 |
| Juniper Mist Configuration Basics | Lab 7.2 |
| Juniper Mist Network Operations and Management | Lab 7.3 |
| Juniper Mist Monitoring and Analytics | Lab 7.4 |
| Marvis Virtual Network Assistant AI | Lab 7.5 |
| Location-based Services | Lab 7.6 |
| Juniper Mist Cloud Operations | Lab 7.7 |

**JNCIE lab readiness (integrative) → Chapter 09**

| Exam objective | Lab |
| --- | --- |
| Enterprise expert readiness | Lab 9.1 |
| Service Provider expert readiness | Lab 9.2 |
| Security expert readiness | Lab 9.3 |
| Data Center expert readiness | Lab 9.4 |

**Higher and adjacent exams.** The **professional** exams (JNCIP-ENT/SP/SEC/DC) and
the **expert** JNCIE practicals build on these specialist objectives at greater depth
and integration; their readiness is covered by the Chapter 09 integrative builds. The
**JNCIP-MistAI** and **JNCIS-MistAI-Wired/Wireless** deepen Chapter 07's Mist
objectives. The **JNCIA-Junos** baseline (Chapter 01) is the shared prerequisite for
the Enterprise and Service Provider tracks.

## Study plans

**JNCIA-Junos — three weeks** at 8–10 hours per week: Chapter 01 with
the lab twice over (week 1 concepts and CLI, week 2 the full lab and
rollback drills, week 3 objectives review against Juniper's JN0-106
list and timed practice).

**Specialist tier — four to six weeks per track** after the associate:
the track chapter in depth, its lab with induced failures, then the
exam objectives walked line by line against your own configurations.
Pair ENT or DC study with Chapter 06 — the automation habits halve the
verification time the labs demand.

**JNCIP tier — eight weeks**, adding the adjacent chapter (ENT
candidates add 05 for EVPN campus; SEC candidates add 03 for the
routing depth JNCIP-SEC assumes) and weekly timed scenario blocks.

**JNCIE — twelve weeks minimum** on Chapter 09's regimen: weekly
half-mocks, two full six-hour mocks as the booking gate, error journal
throughout.

## Study materials

| Role | Resource | Why |
| --- | --- | --- |
| Official objectives | Juniper certification pages (per-exam) | The authority on domains, weights, and current codes |
| Free labs | Juniper vLabs; vJunos-switch/router images | Every written exam's objectives are practicable at no cost |
| Free library | Juniper Day One books | Platform-accurate, free, and current |
| Paid courseware | Juniper Learning Portal on-demand and ILT (per-track) | The official course for each exam, named on its exam page |

## Volume resources

- [Volume index](INDEX.md)
- [Volume glossary](GLOSSARY.md)
- [Master table of contents](../../MASTER_TOC.md)
- [Juniper courses appendix — Volume XCVII](../volume-97-master-appendices/README.md)

## Building and validating this volume

```bash
# Full validation and repo-wide link checks.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-31-juniper-networks-certifications
```
