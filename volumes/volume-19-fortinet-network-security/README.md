# Volume XIX — Fortinet Network Security

> Cybersecurity awareness, threat landscape and portfolio literacy,
> Security Fabric architecture, and hands-on FortiOS administration —
> from NSE 1 digital safety fundamentals through NSE 4 enterprise
> FortiGate deployment.

## Overview

Volume XIX follows the Fortinet Network Security Expert (NSE) Training
Institute's certification progression from NSE 1 through NSE 4. It has no
required prerequisite volume for its awareness and portfolio chapters, but
readers benefit from Volume II's networking foundations before starting
the hands-on FortiOS chapters, consistent with the dependency recorded in
[ROADMAP.md](../../ROADMAP.md).

The volume is organized in two halves:

- **Chapters 01–03** cover NSE 1 through NSE 3: individual cybersecurity
  awareness and digital safety, the evolving threat landscape and the
  security technology categories that respond to it, and the Fortinet
  Security Fabric's architecture and product portfolio, ending with
  FortiGate operator-level foundations (safe, read-only navigation and
  diagnostics).
- **Chapters 04–09** cover NSE 4-level, hands-on FortiOS administration
  using real CLI syntax throughout: first deployment, licensing, and
  hardening; interfaces, routing, NAT, virtual domains, and high
  availability; firewall policy, authentication, VPN, and Zero Trust
  Network Access; FortiGuard security profiles and SSL inspection;
  SD-WAN, central management, and automation; and a capstone chapter that
  assembles every subsystem into a complete, redundant enterprise
  reference architecture.

Every chapter follows the same structure — learning objectives, theory
and architecture, design considerations, implementation and automation,
validation and troubleshooting, security and best practices, references
and knowledge checks, a hands-on lab, and a summary and completion
checklist — defined in [templates/chapter.md](../../templates/chapter.md)
and enforced by [EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md).
Each hands-on lab is a reproducible, disposable exercise with a stated
objective, prerequisites, numbered steps, expected results, a negative
test, and cleanup instructions. Chapters 04–09 build a continuous lab
environment — a FortiGate-VM64 instance named `FGT-LAB-01` (joined by a
second instance, `FGT-LAB-02`, for the high-availability and capstone
chapters) — so configuration built in one chapter is the working starting
point for the next.

## Chapters

1. [NSE 1 Cybersecurity Awareness and Digital Safety](chapters/01-nse-1-cybersecurity-awareness-and-digital-safety.md) — social engineering and phishing mechanics, malware categories, password hygiene, and multi-factor authentication.
2. [NSE 2 Threat Landscape, Security Technologies, and Fortinet Portfolio](chapters/02-nse-2-threat-landscape-security-technologies-and-fortinet-portfolio.md) — the evolution of cybercrime, the cyber kill chain, enterprise security technology categories, and the Fortinet Security Fabric product portfolio.
3. [NSE 3 Security Fabric and FortiGate Operator Foundations](chapters/03-nse-3-security-fabric-and-fortigate-operator-foundations.md) — the five Security Fabric pillars, FortiTelemetry and Security Rating, and safe, read-only FortiGate GUI/CLI operator navigation.
4. [FortiGate First Deployment, Licensing, Management, and Hardening](chapters/04-fortigate-first-deployment-licensing-management-and-hardening.md) — form factors, the FortiOS configuration model, FortiCare/FortiGuard licensing, and baseline administrative hardening.
5. [Interfaces, Routing, NAT, Virtual Domains, and High Availability](chapters/05-interfaces-routing-nat-virtual-domains-and-high-availability.md) — physical/VLAN interfaces, static and policy routing, source/destination NAT, multi-VDOM segmentation, and FGCP high availability.
6. [Firewall Policy, Authentication, VPN, and Zero-Trust Access](chapters/06-firewall-policy-authentication-vpn-and-zero-trust-access.md) — sequential policy matching, local/LDAP/RADIUS authentication, route-based IPsec and SSL VPN, and ZTNA architecture.
7. [FortiGuard Security Profiles, SSL Inspection, and Threat Prevention](chapters/07-fortiguard-security-profiles-ssl-inspection-and-threat-prevention.md) — antivirus, IPS, web filtering, and application control profiles; certificate vs. full SSL deep inspection; FortiSandbox integration.
8. [SD-WAN, Operations, Central Management, Automation, and Troubleshooting](chapters/08-sd-wan-operations-central-management-automation-and-troubleshooting.md) — SD-WAN zones, members, and SLA-based rules; FortiManager/FortiAnalyzer central management; REST API, Ansible, and automation stitches.
9. [NSE 4 FortiOS Administrator Training and Enterprise Capstone](chapters/09-nse-4-fortios-administrator-training-and-enterprise-capstone.md) — blueprint-to-chapter mapping, a full redundant reference architecture, configuration backup/restore, and a layered troubleshooting decision tree.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine
  chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.
- See also the encyclopedia-wide [master index](../../INDEX.md) and
  [master glossary](../../GLOSSARY.md) for cross-volume topics.

## Certification alignment

This volume aligns to the Fortinet NSE 1–4 training and certification
progression tracked in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). It
names blueprint domains and points to the Fortinet Training Institute as
the controlling source; it does not reproduce proprietary assessment
content. Always confirm the current blueprint against Fortinet's official
training site before using this volume for exam preparation.

## Software and platform baseline

Chapters in this volume reference the dated baseline recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md): **FortiOS 7.6.x**
(2026-07). CLI syntax, default behavior, and licensing terminology are
accurate to this baseline; confirm current syntax against the FortiOS CLI
Reference for the release actually in use before applying these examples
to a production device on a different release.

## Building and validating this volume

From the repository root, after completing
[SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-19-fortinet-network-security

# Build a single chapter.
scripts/bash/build-book.sh --format all \
  --chapter volumes/volume-19-fortinet-network-security/chapters/04-fortigate-first-deployment-licensing-management-and-hardening.md
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
