# Volume XXXV — Zscaler Zero Trust Exchange

> The Zscaler Zero Trust Exchange and its certification program in one
> volume: ZIA, ZPA, ZDX, and the Client Connector, taught through the
> platform pillars the ZTCA, ZDTA, ZDXA, and ZDTE credentials assess.

## Overview

Volume XXXV covers Zscaler's **Zero Trust Exchange (ZTE)** — a
cloud-delivered Security Service Edge that brokers every connection inline
and grants per-session access to an application rather than to a network.
The volume is organized by the platform pillars the certifications draw
from: **Zscaler Internet Access (ZIA)** for internet and SaaS,
**Zscaler Private Access (ZPA)** for private applications,
**Zscaler Client Connector (ZCC)** for forwarding, identity as the policy
anchor, and **Zscaler Digital Experience (ZDX)** for operations.

Zscaler prepares candidates through **learning paths rather than
published, weighted exam domains**, so — as with the Forescout program in
Volume XV — this volume follows the vendor's own product structure and
official certification outcomes rather than reproducing any percentage
breakdown Zscaler does not publish openly. Every claim about the program
was taken from Zscaler's own Customer Success Center and Cyber Academy,
never a third-party exam-dump summary.

## Chapters

1. [The Zscaler Certification Program and the Zero Trust Exchange](chapters/01-zscaler-certification-program-and-the-zero-trust-exchange.md) — the four certifications and tiers, the zero-trust premise, the Zero Trust Exchange and its pillars, and confirming the lineup from Zscaler's own pages (ZTCA).
2. [ZIA — Secure Web Gateway and TLS Inspection](chapters/02-zia-secure-web-gateway-and-tls-inspection.md) — the cloud forward proxy, URL filtering and rule order, SSL inspection and its trust chain, and PAC-based forwarding.
3. [ZIA Threat Prevention — Cloud Firewall, DNS, IPS, and Sandbox](chapters/03-zia-threat-prevention-firewall-dns-ips-and-sandbox.md) — FWaaS, DNS Control, ATP/IPS, patient-zero sandboxing, validated safely with EICAR.
4. [ZIA Data Protection — DLP, CASB, and Browser Isolation](chapters/04-zia-data-protection-dlp-casb-and-browser-isolation.md) — inline DLP dictionaries and engines, inline versus API CASB, and Cloud Browser Isolation.
5. [ZPA — Zero Trust Access to Private Applications](chapters/05-zpa-zero-trust-access-to-private-applications.md) — App Connectors, application segments, server groups, the outbound-only dark-app model, and access policy.
6. [ZPA Advanced — Posture, Browser Access, and App Protection](chapters/06-zpa-advanced-posture-browser-access-and-app-protection.md) — device posture as a policy condition, clientless Browser Access, AppProtection, and Privileged Remote Access.
7. [Zscaler Client Connector and Traffic Forwarding](chapters/07-zscaler-client-connector-and-traffic-forwarding.md) — ZCC, Z-Tunnel 1.0 versus 2.0, forwarding and app profiles, and GRE/IPSec site tunnels.
8. [Identity, Authentication, and Policy](chapters/08-identity-authentication-and-policy.md) — SAML authentication and group claims, SCIM provisioning, MFA delegation, and identity-driven policy.
9. [Zscaler Digital Experience and Platform Operations](chapters/09-zscaler-digital-experience-and-platform-operations.md) — the ZDX Score, Cloud Path and deep tracing, admin roles, NSS/LSS log streaming, and API/Terraform automation (ZDXA).

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.

## Certification alignment

This volume maps to the **Zscaler** certification program, as recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). Zscaler
publishes four certifications across three tiers, all validating operation
of the Zero Trust Exchange rather than a single product:

| Certification | Tier | Focus | Primarily covered by |
| --- | --- | --- | --- |
| **ZTCA** — Zero Trust Cyber Associate | Associate | Zero-trust concepts, the platform, use cases | Chapter 01 |
| **ZDTA** — Digital Transformation Administrator | Administrator | Administering the Zero Trust Exchange for users (ZIA, ZPA, ZCC, identity, monitoring) | Chapters 02–08 |
| **ZDXA** — Digital Experience Administrator | Administrator | Administering ZDX digital-experience monitoring | Chapter 09 |
| **ZDTE** — Digital Transformation Engineer | Engineer | Engineering-level deployment and design across the platform | Depth across Chapters 02–09 |

**Course-is-the-blueprint.** Zscaler does not publish weighted exam
domains openly; its exams are the final step of a **learning path** (for
example, ZDTA completes *Zscaler for Users — Administrator*, EDU-200).
Confirm the current exam name, cost, language, and learning path on
Zscaler's Cyber Academy / Customer Success Center pages before scheduling,
and treat the platform pillars in these chapters — not any third-party
percentage breakdown — as the study structure.

## Lab coverage

Every chapter carries a Hands-On Lab of topic-level walkthroughs. Because
Zscaler is a cloud SaaS platform, labs pair **admin-portal configuration
walkthroughs** (with expected results and a negative test) with
**verifications that run locally or from an enrolled endpoint** — for
example, confirming egress through the Zero Trust Exchange
(`ip.zscaler.com`), reading a Zscaler-issued certificate on an inspected
site (`openssl`), evaluating a PAC file, validating malware protection
with the safe EICAR test file, checking that a ZPA App Connector is
outbound-only (`ss`), modeling DLP dictionary and posture logic, and
decoding a SAML assertion's group claims. Each lab ends with a
**`**Lab verified by:** *pending*`** sign-off until a human runs it.

Labs reference a Zscaler tenant for the portal steps; the verifications are
written so the reasoning and the local checks can be followed without one.

## Training access

Zscaler training and certification are delivered through **Zscaler Cyber
Academy** and the **Customer Success Center**
(`customer.zscaler.com/page/certification-exams`), with product
documentation on the **Zscaler Help Portal** (`help.zscaler.com`).
Learning paths bundle the eLearning and hands-on labs that lead to each
exam; the exams themselves are paid. Partners have an equivalent path
through the **Partner Academy** (`partneracademy.zscaler.com`).

## Software and platform baseline

Chapters reference the current Zscaler admin portals (ZIA, ZPA, ZDX, and
the Client Connector portal) and the Zscaler public APIs and Terraform
provider. Zscaler is a continuously updated cloud service and portal paths
and API bases differ by **cloud** (`zscaler.net`, `zscalertwo.net`,
`zscloud.net`, and others); confirm the tenant's cloud and verify current
syntax against Zscaler's documentation before production use.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-35-zscaler-zero-trust-exchange
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
