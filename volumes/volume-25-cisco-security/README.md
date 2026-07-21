# Volume XXV — Cisco Security

> The Cisco CCNP Security certification track end to end: security core
> technologies, network and cloud security, secure service edge, content
> and endpoint protection, secure network access, the Identity Services
> Engine, secure VPNs, zero-trust secure cloud access, and security
> infrastructure design — mapped to the SCOR core exam and the SVPN,
> SCAZT, SISE, and SDSI concentrations.

## Overview

Volume XXV covers the **Cisco CCNP Security** certification track: the
`350-701 SCOR` core exam and four concentration exams — `300-730 SVPN`,
`300-740 SCAZT`, `300-715 SISE`, and `300-745 SDSI`. It is a security
counterpart to [Volume III — Cisco Enterprise Networking](../volume-03-cisco-enterprise-networking/README.md),
which covers the CCNP *Enterprise* track, and it assumes that volume's
routing, switching, and IOS XE foundations rather than repeating them.

The volume also sits alongside the vendor-neutral and other-vendor
security material already in the encyclopedia — it does not duplicate it:

- **[Volume X — Enterprise Cybersecurity](../volume-10-enterprise-cybersecurity/README.md)**
  supplies the vendor-neutral security architecture, threat modeling, and
  operations vocabulary this volume applies to Cisco's product portfolio.
- **[Volume XVI — Palo Alto Networks Security](../volume-16-palo-alto-networks-security/README.md)**
  and
  **[Volume XIX — Fortinet Network Security](../volume-19-fortinet-network-security/README.md)**
  cover competing next-generation-firewall and secure-access platforms;
  the concepts transfer, the products and configuration do not.
- **[Volume II — Network Engineering Foundations](../volume-02-network-engineering-foundations/README.md)**
  and **Volume III** supply the networking on which every security control
  here is layered.

The volume is organized to follow the CCNP Security blueprint from core
to concentration:

- **Chapters 01–05** cover the `SCOR` core: security concepts and the
  threat landscape, network security with Cisco Secure Firewall, cloud
  security and the secure service edge, content and endpoint protection,
  and secure network access, visibility, and enforcement. Passing SCOR is
  required for CCNP Security regardless of which concentration follows,
  and SCOR is also the CCIE Security qualifying exam.
- **Chapter 06** covers the **Identity Services Engine** (`SISE`) in
  depth — the platform behind most of the access-control enforcement
  Chapter 05 introduces.
- **Chapter 07** covers **secure VPNs** (`SVPN`): site-to-site and remote
  access, FlexVPN and DMVPN, and the troubleshooting that dominates that
  exam.
- **Chapter 08** covers **zero-trust secure cloud access for users and
  endpoints** (`SCAZT`), the newest concentration and the one most
  aligned with Cisco's secure-service-edge direction.
- **Chapter 09** covers **designing security infrastructure** (`SDSI`),
  automation and DevSecOps, and a capstone that composes the whole track
  into one reference design.

Every chapter follows the same structure — learning objectives, theory
and architecture, design considerations, implementation and automation,
validation and troubleshooting, security and best practices, references
and knowledge checks, a hands-on lab, and a summary and completion
checklist — defined in [templates/chapter.md](../../templates/chapter.md)
and enforced by [EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md).

**A note on labs in this volume.** Cisco's security portfolio is
commercial and much of it has no free tier, which constrains what a
reproducible lab can be. Where a lab needs Cisco Secure Firewall, ISE, or
a licensed VPN headend, the chapter says so and provides the closest
honest substitute — Cisco's own evaluation and dCloud environments, or an
open equivalent that exercises the same protocol — rather than implying
the real product is freely reproducible. See *Practicing* below.

## Chapters

1. [Security Concepts, the Threat Landscape, and the CCNP Security Track](chapters/01-security-concepts-the-threat-landscape-and-the-ccnp-security-track.md)
2. [Network Security with Cisco Secure Firewall and IPS](chapters/02-network-security-with-cisco-secure-firewall-and-ips.md)
3. [Cloud Security and the Secure Service Edge](chapters/03-cloud-security-and-the-secure-service-edge.md)
4. [Content Security and Endpoint Protection](chapters/04-content-security-and-endpoint-protection.md)
5. [Secure Network Access, Visibility, and Enforcement](chapters/05-secure-network-access-visibility-and-enforcement.md)
6. [Identity Services Engine: Deployment, Policy, and Services](chapters/06-identity-services-engine-deployment-policy-and-services.md)
7. [Secure VPNs: Site-to-Site, Remote Access, and Troubleshooting](chapters/07-secure-vpns-site-to-site-remote-access-and-troubleshooting.md)
8. [Zero-Trust Secure Cloud Access for Users and Endpoints](chapters/08-zero-trust-secure-cloud-access-for-users-and-endpoints.md)
9. [Designing Security Infrastructure, Automation, and Capstone](chapters/09-designing-security-infrastructure-automation-and-capstone.md)

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across this volume.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.

## Related volumes

- **Volume III — Cisco Enterprise Networking** — the CCNP Enterprise
  counterpart; shared IOS XE, routing, and switching foundations.
- **Volume X — Enterprise Cybersecurity** — vendor-neutral security
  architecture and operations this volume specializes to Cisco.
- **Volume XVI — Palo Alto Networks Security** and **Volume XIX —
  Fortinet Network Security** — competing security platforms.
- **Volume II — Network Engineering Foundations** — the networking every
  control here sits on.

## Certification alignment

This volume maps to the **Cisco CCNP Security** certification track,
recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). CCNP
Security requires the `SCOR` core exam plus **one** concentration exam;
this volume covers the core and four of the concentrations. `SCOR` is
also the qualifying exam for **CCIE Security**.

| Exam | Title | Duration | Role in the track |
| --- | --- | --- | --- |
| **350-701 SCOR** | Implementing and Operating Cisco Security Core Technologies | 120 min | Core — required for CCNP Security and CCIE Security |
| **300-730 SVPN** | Implementing Secure Solutions with Virtual Private Networks | 90 min | Concentration |
| **300-740 SCAZT** | Designing and Implementing Secure Cloud Access for Users and Endpoints | 90 min | Concentration |
| **300-715 SISE** | Implementing and Configuring Cisco Identity Services Engine | 90 min | Concentration |
| **300-745 SDSI** | Designing Cisco Security Infrastructure | 90 min | Concentration |

All are delivered through Pearson VUE. Question counts and cut scores are
set per exam and are not restated here; confirm them at registration.

### A live version transition to plan around

**The CCNP Security core and the ISE concentration both refresh on 26–27
August 2026**, and anyone beginning study now needs to know which edition
they will sit.

| Exam | Current edition | Incoming edition | Last day for current |
| --- | --- | --- | --- |
| 350-701 SCOR | v1.1 | **v2.0** | 26 August 2026 |
| 300-715 SISE | v1.1 | **v1.2** | 26 August 2026 |

Because a SCOR study plan runs eight to ten weeks (see below), **a
candidate starting after roughly mid-June 2026 will finish after the v1.1
cutoff and should prepare for v2.0.** This volume's SCOR mapping and study
plan target **v2.0** for that reason, and flag where v1.1 differs. SISE
v1.2 kept v1.1's exact domain structure and weights, so that transition
changes the edition label but not the preparation.

Confirm the current blueprint and edition against
[Cisco's exam pages](https://www.cisco.com/site/us/en/learn/training-certifications/exams/index.html)
at registration; the transition dates above are Cisco's stated schedule
and can move.

### Domain weights, mapped to this volume

All weights below are transcribed from Cisco's published exam-topics
documents and each set sums to 100%.

**350-701 SCOR v2.0** — the edition to prepare for if starting now:

| Domain | Weight | Chapters |
| --- | --- | --- |
| Network Security | **25%** | [02](chapters/02-network-security-with-cisco-secure-firewall-and-ips.md) |
| Security Concepts | 20% | [01](chapters/01-security-concepts-the-threat-landscape-and-the-ccnp-security-track.md) |
| Cloud Security | 15% | [03](chapters/03-cloud-security-and-the-secure-service-edge.md) |
| Endpoint Protection and Detection | 15% | [04](chapters/04-content-security-and-endpoint-protection.md) |
| Network Access, Visibility, and Enforcement | 15% | [05](chapters/05-secure-network-access-visibility-and-enforcement.md), [06](chapters/06-identity-services-engine-deployment-policy-and-services.md) |
| Secure Service Edge | 10% | [03](chapters/03-cloud-security-and-the-secure-service-edge.md), [08](chapters/08-zero-trust-secure-cloud-access-for-users-and-endpoints.md) |

**What changed from SCOR v1.1**, because material written to the older
edition is still in wide circulation:

- v1.1 had a **Content Security** domain (15%); v2.0 removed it as a
  standalone domain. Content-security topics still appear, folded into
  network and cloud security. [Chapter 04](chapters/04-content-security-and-endpoint-protection.md)
  keeps them because they remain examinable material and are core to the
  role, but they no longer carry their own weight line.
- v2.0 **added Secure Service Edge** (10%) as a new domain, reflecting
  Cisco's SASE/SSE direction — the same subject the SCAZT concentration
  develops in full.
- Network Security rose from 20% to **25%** (now the largest domain);
  Security Concepts fell from 25% to 20%; Endpoint rose from 10% to 15%.

**300-715 SISE v1.1 / v1.2** (identical weights):

| Domain | Weight | Chapters |
| --- | --- | --- |
| Policy Enforcement | **25%** | [06](chapters/06-identity-services-engine-deployment-policy-and-services.md) |
| Web Auth and Guest Services | 15% | [06](chapters/06-identity-services-engine-deployment-policy-and-services.md) |
| Profiler | 15% | [06](chapters/06-identity-services-engine-deployment-policy-and-services.md) |
| BYOD | 15% | [06](chapters/06-identity-services-engine-deployment-policy-and-services.md) |
| Architecture and Deployment | 10% | [06](chapters/06-identity-services-engine-deployment-policy-and-services.md) |
| Endpoint Compliance | 10% | [06](chapters/06-identity-services-engine-deployment-policy-and-services.md) |
| Network Access Device Administration | 10% | [06](chapters/06-identity-services-engine-deployment-policy-and-services.md) |

**300-730 SVPN v1.1** — note where the weight actually is:

| Domain | Weight | Chapters |
| --- | --- | --- |
| Troubleshooting Using ASDM and CLI | **35%** | [07](chapters/07-secure-vpns-site-to-site-remote-access-and-troubleshooting.md) |
| Secure Communications Architectures | 30% | [07](chapters/07-secure-vpns-site-to-site-remote-access-and-troubleshooting.md) |
| Remote Access VPNs | 20% | [07](chapters/07-secure-vpns-site-to-site-remote-access-and-troubleshooting.md) |
| Site-to-Site VPNs on Routers and Firewalls | 15% | [07](chapters/07-secure-vpns-site-to-site-remote-access-and-troubleshooting.md) |

**300-740 SCAZT v1.0:**

| Domain | Weight | Chapters |
| --- | --- | --- |
| Application and Data Security | **25%** | [08](chapters/08-zero-trust-secure-cloud-access-for-users-and-endpoints.md) |
| User and Device Security | 20% | [08](chapters/08-zero-trust-secure-cloud-access-for-users-and-endpoints.md) |
| Network and Cloud Security | 20% | [08](chapters/08-zero-trust-secure-cloud-access-for-users-and-endpoints.md), [03](chapters/03-cloud-security-and-the-secure-service-edge.md) |
| Visibility and Assurance | 15% | [08](chapters/08-zero-trust-secure-cloud-access-for-users-and-endpoints.md) |
| Cloud Security Architecture | 10% | [08](chapters/08-zero-trust-secure-cloud-access-for-users-and-endpoints.md), [03](chapters/03-cloud-security-and-the-secure-service-edge.md) |
| Threat Response | 10% | [08](chapters/08-zero-trust-secure-cloud-access-for-users-and-endpoints.md) |

**300-745 SDSI v1.0:**

| Domain | Weight | Chapters |
| --- | --- | --- |
| Secure Infrastructure | **30%** | [09](chapters/09-designing-security-infrastructure-automation-and-capstone.md), [02](chapters/02-network-security-with-cisco-secure-firewall-and-ips.md) |
| Risk, Events, and Requirements | **30%** | [09](chapters/09-designing-security-infrastructure-automation-and-capstone.md), [01](chapters/01-security-concepts-the-threat-landscape-and-the-ccnp-security-track.md) |
| Applications | 25% | [09](chapters/09-designing-security-infrastructure-automation-and-capstone.md), [04](chapters/04-content-security-and-endpoint-protection.md) |
| Artificial Intelligence, Automation, and DevSecOps | 15% | [09](chapters/09-designing-security-infrastructure-automation-and-capstone.md) |

**Read the concentration weights before choosing one.** SVPN concentrates
**65%** of its exam in troubleshooting and architecture, not in building
tunnels — a candidate who can configure a VPN but not diagnose one has
misread it. SDSI is a **design** exam with no single dominant domain and
almost no configuration; it rewards architecture judgment, not CLI
fluency. SISE and SCAZT are more evenly spread. Match the concentration to
how you actually think, not only to the technology you know.

### Study plan

CCNP Security is **SCOR plus one concentration**, so the realistic plan is
two exams, sequenced. SCOR first: it is required, it is the broadest, and
it teaches the vocabulary the concentrations assume.

**SCOR (350-701 v2.0) — ten weeks** at eight to ten hours per week, for a
candidate with CCNP Enterprise-level networking (Volume III) already in
place. Without it, work Volumes II–III first.

| Week | Focus | Domain | Chapters |
| --- | --- | --- | --- |
| 1 | Security concepts, the threat landscape, common attacks, cryptography and PKI foundations | Security Concepts 20% | 01 |
| 2–3 | **The heavy weeks.** Network security: Cisco Secure Firewall (ASA and FTD), NGFW policy, IPS, network-based segmentation | Network Security 25% | 02 |
| 4 | Cloud security: workload protection, cloud-delivered security, and the secure service edge model | Cloud Security 15% + SSE 10% | 03 |
| 5 | Endpoint protection and detection (Secure Endpoint), and the content-security topics folded in from v1.1 | Endpoint 15% | 04 |
| 6–7 | Secure network access, visibility, and enforcement: 802.1X, TrustSec, NetFlow/telemetry, and the ISE role | Access/Visibility 15% | 05, 06 |
| 8 | Automation and programmability of the security stack — APIs across the portfolio | (cross-domain) | 09 |
| 9 | Weak-area drill against the v2.0 blueprint, and confirm you are sitting v2.0 not v1.1 | — | — |
| 10 | Full-blueprint timed review | — | — |

**Then one concentration — four to six weeks each**, taken while SCOR is
fresh:

| Concentration | Focus of the weeks | Primary chapter |
| --- | --- | --- |
| **SISE** (300-715) | Weeks 1–2 policy enforcement (25%) and ISE architecture; week 3 profiler, BYOD, guest; week 4 posture, TACACS+ device admin; then lab repetition | 06 |
| **SVPN** (300-730) | Weeks 1–2 site-to-site and remote-access configuration; **weeks 3–4 troubleshooting (35%) and architectures (30%)** — the bulk of the exam; deliberately break and diagnose tunnels | 07 |
| **SCAZT** (300-740) | Week 1 cloud/user/device security; weeks 2–3 application and data security (25%) and network/cloud security; week 4 visibility, assurance, threat response | 08 |
| **SDSI** (300-745) | A **design** exam: weeks 1–2 secure infrastructure and risk/requirements (60% together); week 3 application security; week 4 AI/automation/DevSecOps. Practice justifying designs, not configuring them | 09 |

**Take a Cisco practice/assessment before you feel ready.** For a
performance-adjacent, scenario-heavy exam like SCOR, an early diagnostic
redirects study while there is still time to redirect it.

### Study materials

Cisco's own recommended training, plus the sources exam items are written
against. These named courses are paid, commercial offerings.

| Exam | Cisco course | Delivery |
| --- | --- | --- |
| 350-701 SCOR | *Implementing and Operating Cisco Security Core Technologies* (SCOR) | Instructor-led / e-learning |
| 300-730 SVPN | *Implementing Secure Solutions with Virtual Private Networks* (SVPN) | Instructor-led / e-learning |
| 300-740 SCAZT | *Designing and Implementing Secure Cloud Access for Users and Endpoints* (SCAZT) | Instructor-led / e-learning |
| 300-715 SISE | *Implementing and Configuring Cisco Identity Services Engine* (SISE) | Instructor-led / e-learning |
| 300-745 SDSI | *Designing Cisco Security Infrastructure* (SDSI) | Instructor-led / e-learning |

Beyond the courses: the **exam-topics document** for each exam is the
controlling source and lists subtopics far more specific than the domain
titles; the **Cisco Security product documentation** (Secure Firewall,
ISE, Secure Client, Umbrella) is where items are written against; and the
Cisco U. and Cisco Learning Network communities carry current,
transition-aware discussion. Confirm every course code and edition at
[Cisco Learning Network](https://learningnetwork.cisco.com/) before
purchase — the August 2026 refresh is retiring and replacing courseware
alongside the exams.

## Practicing

**Cisco's security portfolio is commercial, and most of it has no free
tier.** That makes this a costly track to practice, closer to the Dell
and VMware volumes than to the free-to-run Ubuntu or Wireshark ones.

| Route | Cost | What it gives you |
| --- | --- | --- |
| Cisco dCloud | Free with a Cisco account | Guided, time-boxed labs on Secure Firewall, ISE, and more — the closest free analogue to hands-on time |
| Cisco Modeling Labs (CML) | Paid (personal tier is modestly priced) | Build routed and firewalled topologies; the practical route for SVPN site-to-site and routing-adjacent work |
| Secure Firewall / ISE evaluation | Free eval licenses, time-limited | Stand up FMC/FTD and ISE in a hypervisor; the route to sustained ISE and firewall practice |
| Employer or partner lab | Varies | The only way to exercise the licensed, integrated stack as it behaves in production |

**Be honest about what each concentration needs.** SVPN is the most
reproducible without buying much — routers and firewalls in CML carry
most of it. SISE genuinely needs ISE, which the evaluation license makes
reachable for a month at a time. SCAZT and SDSI are design- and
cloud-weighted; dCloud plus reading covers more of them than a home lab
would. A reader without any Cisco security hardware or licenses should
treat SVPN as the most lab-backed concentration and the design-heavy
exams as reading-plus-dCloud.

## Software and platform baseline

Chapters in this volume reference the dated baseline recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md). Cisco's security
products version independently of one another and of the exams; where a
chapter's guidance depends on a build-specific detail it says so and
points to the current product documentation rather than treating any
single release as timeless. Update that file, not individual chapters,
when the baseline changes.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-25-cisco-security
```
