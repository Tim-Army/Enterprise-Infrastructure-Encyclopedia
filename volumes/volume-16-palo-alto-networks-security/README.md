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
- **Chapters 08–09** synthesize and extend: the role-based PCNSA/PCNSE
  certification portfolio with an integrated enterprise capstone build
  (08), and Cortex Cloud Security Professional coverage of CNAPP —
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
8. [Role-Based Certification Portfolio and Enterprise Capstone](chapters/08-role-based-certification-portfolio-and-enterprise-capstone.md) — PCNSA/PCNSE blueprint mapping, study sequencing, and an integrated multi-firewall capstone build.
9. [Cortex Cloud Security Professional](chapters/09-cortex-cloud-security-professional.md) — CNAPP architecture (CSPM, CWPP, CIEM, IaC/API security), agentless and agent-based workload visibility, and Checkov-based shift-left scanning.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.

## Certification alignment

This volume aligns to the Palo Alto Networks certification and training
paths recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md):
Cybersecurity Apprentice, Cybersecurity Practitioner, the role-based
PCNSA/PCNSE portfolio, and Cortex Cloud Security Professional. Chapters
describe blueprint domains and point to official Palo Alto Networks
Education sources; they do not reproduce proprietary assessment content.
Always confirm the current blueprint against the vendor's official page
before using a chapter for exam preparation.

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
