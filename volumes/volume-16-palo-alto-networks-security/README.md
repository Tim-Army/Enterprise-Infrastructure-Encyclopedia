# Volume XVI — Palo Alto Networks Security

> Next-generation firewall theory, VM-Series deployment, PAN-OS networking
> and high availability, App-ID/User-ID/Content-ID security policy,
> Panorama centralized management, fleet operations and automation, the
> role-based certification portfolio, and Cortex Cloud CNAPP security.

## Overview

Volume XVI is the encyclopedia's Palo Alto Networks Security volume,
depending on Volume II — Network Engineering Foundations for its
networking prerequisites. It takes a reader from portfolio-wide
conceptual literacy through hands-on PAN-OS and Panorama administration to
an integrated enterprise capstone and cloud-native application protection
with Cortex Cloud.

The volume is organized in three parts:

- **Chapters 01–02** establish certification-aligned foundations: the CIA
  triad, Zero Trust, and single-pass parallel processing mapped to the
  full Strata/Prisma/Cortex portfolio (Chapter 01), then licensing,
  cloud-delivered security services, Strata Cloud Manager, Prisma Access,
  and Cortex product depth (Chapter 02).
- **Chapters 03–07** build hands-on PAN-OS and Panorama administration
  skill: VM-Series deployment, licensing, and bootstrap (03); networking,
  NAT, routing, and high availability (04); App-ID/User-ID/Content-ID
  security policy and decryption (05); Panorama device groups, templates,
  and centralized logging (06); and fleet-scale operations,
  troubleshooting, upgrades, and API/Terraform/Ansible automation (07).
- **Chapters 08–09** synthesize and extend: the role-based certification
  portfolio with an integrated enterprise capstone build
  (08), and Cloud Security Professional coverage of CNAPP —
  CSPM, CWPP, CIEM, and IaC security scanning (09).

Every chapter follows the same structure — learning objectives, theory and
architecture, design considerations, implementation and automation,
validation and troubleshooting, security and best practices, references
and knowledge checks, a hands-on lab, and a summary and completion
checklist — defined in [templates/chapter.md](../../templates/chapter.md)
and enforced by [EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md).
Each hands-on lab is a reproducible, disposable exercise with a stated
objective, prerequisites, numbered steps, expected results, a negative
test, and cleanup instructions.

## Chapters

1. [Cybersecurity Apprentice Foundations](chapters/01-cybersecurity-apprentice-foundations.md) — CIA triad and defense-in-depth mapped to the portfolio, Zero Trust and App-ID/User-ID/Content-ID, single-pass parallel processing, and basic PAN-OS CLI navigation.
2. [Cybersecurity Practitioner and Platform Portfolio](chapters/02-cybersecurity-practitioner-and-platform-portfolio.md) — cloud-delivered security services, Strata Cloud Manager, Prisma Access and Prisma SD-WAN, and Cortex XDR/XSIAM/XSOAR/Xpanse.
3. [VM-Series Deployment, Licensing, and Bootstrap](chapters/03-vm-series-deployment-licensing-and-bootstrap.md) — hypervisor and cloud deployment targets, model sizing, BYOL/PAYG/flexible vCPU licensing, and the bootstrap package.
4. [PAN-OS Networking, NAT, Routing, and High Availability](chapters/04-pan-os-networking-nat-routing-and-high-availability.md) — interface modes, zones, virtual routers, static and dynamic routing, NAT policy, and active/passive HA.
5. [Application, Identity, Threat, and Data Security Policy](chapters/05-application-identity-threat-and-data-security-policy.md) — App-ID- and User-ID-based security policy, security profiles, and SSL Forward Proxy decryption.
6. [Panorama Installation, Central Management, and Logging](chapters/06-panorama-installation-central-management-and-logging.md) — deployment modes, device group hierarchy, template stacks, managed-device onboarding, and Collector Groups.
7. [Firewall Operations, Troubleshooting, Upgrades, and Automation](chapters/07-firewall-operations-troubleshooting-upgrades-and-automation.md) — HA-aware upgrade sequencing, the troubleshooting toolkit, and XML API/REST API/Terraform/Ansible automation.
8. [Role-Based Certification Portfolio and Enterprise Capstone](chapters/08-role-based-certification-portfolio-and-enterprise-capstone.md) — the four-level Network Security track, blueprint domains and weights, study sequencing and plans, and an integrated multi-firewall capstone build.
9. [Cloud Security Professional and the Cortex Cloud Platform](chapters/09-cortex-cloud-security-professional.md) — CNAPP architecture (CSPM, CWPP, CIEM, IaC/API security), agentless and agent-based workload visibility, and Checkov-based shift-left scanning.
10. [The Cortex Platform and the Security Operations Track](chapters/10-cortex-platform-and-the-security-operations-track.md) — Cortex XSIAM/XDR/XSOAR/Xpanse and the role-based Security Operations track (Security Operations Professional and Architect; the analyst/engineer split).
11. [Cortex XSIAM and XDR — Analyst and Engineer](chapters/11-cortex-xsiam-and-xdr-analyst-and-engineer.md) — causality-based investigation for analysts, data-source onboarding and detection engineering for engineers, and XQL across both.
12. [XSOAR Automation and the Cloud Security Engineer](chapters/12-xsoar-automation-and-cloud-security-engineer.md) — XSOAR playbooks and the automation-trust ladder in the SOC, and the Cloud Security Engineer certification closing the Cloud Security track.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.

## Certification alignment

This volume aligns to the Palo Alto Networks certification and training
paths recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md):
Cybersecurity Apprentice, Cybersecurity Practitioner, the role-based
Network Security track (Network Security Professional, Network Security
Analyst, Next-Generation Firewall Engineer, SD-WAN Engineer, Security
Service Edge Engineer, and Network Security Architect), the **Security
Operations track** (Security Operations Professional, Security Operations
Architect, and the role-based Cortex certifications — XSIAM Analyst and
Engineer, XDR Analyst and Engineer, XSOAR Engineer), and the **Cloud
Security track** (Cloud Security Professional and Cloud Security
Engineer). All three tracks were verified against Palo Alto Networks'
certification pages on 22 July 2026. The product-centric exams this volume originally
tracked — PCNSA and PCNSE — were retired during 2025; see
[Chapter 08](chapters/08-role-based-certification-portfolio-and-enterprise-capstone.md)
for where that material now maps. Chapters
describe blueprint domains and point to official Palo Alto Networks
Education sources; they do not reproduce proprietary assessment content.
Always confirm the current blueprint against the vendor's official page
before using a chapter for exam preparation.

## Topic-level lab coverage

Every blueprint domain across the volume's certifications is covered by
hands-on **walkthrough** labs — **72 topic-level labs** plus one integrative
lab per chapter and two Design Exercises. Because Palo Alto Networks
publishes its exam datasheets through a dynamic portal rather than
downloadable blueprints, coverage is measured against the blueprint
**domains and weights** documented in Chapter 08 (Network Security track,
from the official datasheets, verified 22 July 2026) and each Cortex
certification's documented capability areas; re-confirm against the live
datasheets on the certification-currency cycle. Labs use the PAN-OS CLI,
XML/REST APIs, Panorama, and the Cortex Cloud / XSIAM / XSOAR REST APIs, and
each carries `**Lab verified by:** *pending*` until a human runs it.

The two design credentials — **Network Security Architect** and, in the
SecOps track, the architect tier — are covered by Design Exercises
(Chapter 08 and the reasoning throughout), consistent with the design-exam
treatment used for Cisco CCDE, VMware VCDX, and the cloud architect exams.

### Network Security track

**Next-Generation Firewall Engineer (Domains → labs)**

| Domain | Weight | Labs |
| --- | --- | --- |
| 1. PAN-OS Networking Configuration | 40% | 4.1–4.8 |
| 2. PAN-OS Device Setting Configuration | 40% | 3.1–3.7, 5.3–5.7 |
| 3. Integration and Automation | 20% | 7.1, 7.3–7.5, 7.7 |

**Network Security Analyst**

| Domain | Weight | Labs |
| --- | --- | --- |
| 1. Object Configuration Creation and Application | 30% | 5.1 |
| 2. Policy Creation and Application | 30% | 5.2–5.9 |
| 3. Management and Operations | 26% | 6.1–6.7, 7.5, 7.7 |
| 4. Troubleshooting | 14% | 7.2, 7.6 |

**Network Security Professional** — spans the platform: Fundamentals 1.1–1.7;
NGFW/SASE functionality 2.1–2.6; platform tools 3.1–3.7; maintenance and
configuration 3.5, 7.1; CDSS and infrastructure 5.3–5.5, 6.5; connectivity
and security 4.1–4.9, 5.1–5.9.

**Cybersecurity Practitioner** — the six domains map to Labs 2.1–2.6.

**Cybersecurity Apprentice** — the seven domains map to Labs 1.1–1.7.

**SD-WAN Engineer** — Deployment and Configuration 4.9; Planning/Design,
Troubleshooting, Operations, and Unified SASE draw on 4.1–4.8 and 2.3.

**Security Service Edge Engineer** — Prisma Access planning/services and
Prisma Browser map to 2.3; Administration and Troubleshooting to 7.2, 7.6.

**Network Security Architect** — the ten design domains are covered by the
Chapter 08 **Design Exercise** and capstone.

### Security Operations and Cloud Security tracks (Cortex)

**Cloud Security Professional** — CSPM 9.1–9.2; CIEM 9.3; CWPP 9.4; code/IaC
security 9.5; compliance 9.6.

**XSIAM Analyst** — investigation and response 11.1–11.3; platform operation
10.1, 10.3, 10.5.

**XSIAM Engineer** — ingestion and detection engineering 11.4–11.6; platform
build 10.2, 10.4.

**XSOAR Engineer** — playbooks, integrations, and automation 12.1–12.3;
platform 10.5.

**Cloud Security Engineer** — cloud remediation and policy-as-code 12.4–12.5,
9.3–9.5.

## Software and platform baseline

Chapters in this volume reference the dated baseline recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md): PAN-OS 11.x and
Panorama 11.x. Update that file, not individual chapters, when the
baseline changes.

## Building and validating this volume

From the repository root, after completing
[SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-16-palo-alto-networks-security

# Build a single chapter.
scripts/bash/build-book.sh --format all \
  --chapter volumes/volume-16-palo-alto-networks-security/chapters/05-application-identity-threat-and-data-security-policy.md
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
