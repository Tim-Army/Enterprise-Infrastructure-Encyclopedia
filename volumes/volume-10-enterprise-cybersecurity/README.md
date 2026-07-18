# Volume X — Enterprise Cybersecurity

> Defensive enterprise cybersecurity, end to end: governance and risk,
> identity and Zero Trust, platform and network defense, exposure and
> patch management, detection and SOC operations, incident response and
> digital forensics, data protection and ransomware resilience, and the
> automation and assurance practices that keep a security program honest.

## Overview

Volume X covers enterprise cybersecurity from a defender's perspective.
It does not cover offensive exploitation techniques, working malware, or
attack tooling; where adversary behavior is discussed (kill chains,
MITRE ATT&CK techniques, ransomware progression), it is discussed only to
the depth needed to design and validate the defensive control that
addresses it.

The volume builds cumulatively. Each chapter names the specific prior
chapter its controls depend on, and later chapters route findings back
into earlier disciplines — a confirmed incident (Chapter 7) feeds new
detection rules back into Chapter 6, a validated threat hunt (Chapter 9)
becomes a permanent detection, and every chapter's risk exceptions live
in the risk register introduced in Chapter 1. The nine chapters fall into
four loosely sequential groups:

- **Chapters 01–03 — Foundations.** Governance, risk, and security
  architecture; identity, Zero Trust, and privileged access; platform
  hardening and endpoint defense. These establish the control crosswalk,
  risk register, and identity model every later chapter references.
- **Chapters 04–05 — Infrastructure and exposure.** Network security
  architecture and infrastructure defense; vulnerability, exposure, and
  patch risk management. These reduce the attack surface the rest of the
  volume defends and monitors.
- **Chapters 06–07 — Detect and respond.** Security telemetry, detection
  engineering, and SOC operations; cybersecurity incident response and
  digital evidence. These build the pipeline that turns raw telemetry
  into a validated, evidence-preserving response.
- **Chapters 08–09 — Protect and improve.** Data security, cryptography,
  privacy, and ransomware resilience; security automation, assurance,
  threat hunting, and lifecycle operations. These protect data directly
  and close the loop that keeps the whole program measurably improving.

Every chapter follows the same structure — learning objectives, theory
and architecture, design considerations, implementation and automation,
validation and troubleshooting, security and best practices, references
and knowledge checks, a hands-on lab, and a summary and completion
checklist — defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md). Each hands-on lab
is a reproducible, disposable exercise with a stated objective,
prerequisites, numbered steps, expected results, a negative test, and
cleanup instructions; every lab in this volume was executed end to end
against its documented commands before publication.

## Chapters

1. [Cybersecurity Governance, Risk, and Architecture](chapters/01-cybersecurity-governance-risk-and-architecture.md) — the three lines of defense, NIST CSF 2.0, qualitative and FAIR quantitative risk scoring, control catalog crosswalks, and STRIDE-based security architecture review.
2. [Enterprise Identity, Zero Trust, and Privileged Access](chapters/02-enterprise-identity-zero-trust-and-privileged-access.md) — NIST SP 800-207 Zero Trust Architecture, phishing-resistant MFA, conditional access, and just-in-time privileged access management.
3. [Platform Hardening, Configuration, and Endpoint Defense](chapters/03-platform-hardening-configuration-and-endpoint-defense.md) — CIS Benchmarks and DISA STIGs, SELinux and AppArmor, endpoint detection and response, and application allow-listing.
4. [Network Security Architecture and Infrastructure Defense](chapters/04-network-security-architecture-and-infrastructure-defense.md) — segmentation and microsegmentation, NGFW and IDS/IPS, VPN-to-ZTNA migration, DNS security, DDoS protection, and SASE/SSE.
5. [Vulnerability, Exposure, and Patch Risk Management](chapters/05-vulnerability-exposure-and-patch-risk-management.md) — CVSS and EPSS-based prioritization, the CISA KEV catalog, Continuous Threat Exposure Management (CTEM), SBOM, and staged patch rollout.
6. [Security Telemetry, Detection Engineering, and SOC Operations](chapters/06-security-telemetry-detection-engineering-and-soc-operations.md) — the SIEM pipeline, the detection engineering lifecycle, MITRE ATT&CK coverage mapping, tiered SOC operations, and SOAR.
7. [Cybersecurity Incident Response and Digital Evidence](chapters/07-cybersecurity-incident-response-and-digital-evidence.md) — the NIST SP 800-61 incident response lifecycle, severity classification, digital forensics fundamentals, chain of custody, and tabletop exercises.
8. [Data Security, Cryptography, Privacy, and Ransomware Resilience](chapters/08-data-security-cryptography-privacy-and-ransomware-resilience.md) — data classification, envelope encryption and key management, PKI, DLP, privacy engineering, and the 3-2-1-1-0 ransomware-resilient backup rule.
9. [Security Automation, Assurance, Threat Hunting, and Lifecycle Operations](chapters/09-security-automation-assurance-threat-hunting-and-lifecycle-operations.md) — DevSecOps pipeline gates, continuous control validation, purple teaming, hypothesis-driven threat hunting, and security metrics and tool lifecycle management.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine
  chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.
- [Master index](../../INDEX.md) and
  [master glossary](../../GLOSSARY.md) — cross-volume topics and terms
  for the complete encyclopedia.

## Software and platform baseline

Chapters in this volume reference the dated baseline recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md) — Red Hat Enterprise
Linux 10 and Ubuntu Server 26.04 LTS as the hardening and lab baseline
platforms (Chapters 3 and 4), and Python 3.11+ for every scripted
example and lab. This volume is deliberately vendor-neutral for
commercial security platforms (SIEM, EDR, NGFW, PAM, KMS): patterns are
shown in vendor-neutral configuration and CLI form so the concepts
transfer directly to Volume XVI (Palo Alto Networks Security),
Volume XV (Forescout Platform and Certifications), Volume XVIII (Gigamon
Network Visibility), Volume XIX (Fortinet Network Security), and
Volume XX (Wireshark and Packet Analysis), which cover specific vendor
implementations of controls introduced here.

## Building and validating this volume

From the repository root, after completing
[SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-10-enterprise-cybersecurity

# Build a single chapter.
scripts/bash/build-book.sh --format all \
  --chapter volumes/volume-10-enterprise-cybersecurity/chapters/06-security-telemetry-detection-engineering-and-soc-operations.md
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
