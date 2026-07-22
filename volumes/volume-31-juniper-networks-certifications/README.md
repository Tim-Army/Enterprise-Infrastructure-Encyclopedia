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
