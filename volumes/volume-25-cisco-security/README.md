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

### CCIE lab readiness

**CCIE Security v6.1** sits above the CCNP track, reached by first
passing the `SCOR 350-701` core (the same qualifier as CCNP Security).
It is an **eight-hour, hands-on practical exam** in the standard CCIE
two-module shape — a **3-hour Design** module (scenario-based, no device
access) and a **5-hour Deploy, Operate, and Optimize** module — in which
you design, deploy, operate, and optimize end-to-end security for a
**dual-stack (IPv4 and IPv6)** enterprise network, and are expected to
**program and automate** it as well. Cisco is adding a **new AI module**
to its CCIE practical exams — confirm the current format at
registration.

**What the lab adds over this volume.** These chapters build security
knowledge and configuration skill at professional depth; the lab tests
**speed, cross-product integration, and troubleshooting under time**.
You must stand up and interconnect Secure Firewall, ISE, VPNs, secure
access, and cloud/content controls quickly, then diagnose deliberately
broken scenarios — a distinct skill from knowing each product, built
only by full-scale timed labs.

**How to prepare.** Build a complete security topology in a lab
(Secure Firewall/FMC, ISE, and the VPN and secure-access components of
Chapters 02–08 together), and rehearse it against the clock: a full
build end to end, then the same estate broken for you to fix. Pair each
chapter's Hands-On Lab with a timed rebuild, drill the Design module
using the method in [Volume XXX](../volume-30-cisco-ccde-network-design/README.md),
and use Cisco's official CCIE Security practice labs and
equipment-rental or BYOD options before exam day. Confirm the current
lab blueprint and format on the Cisco Learning Network before
scheduling — CCIE lab topics are separate from the written exam topics
and change independently, and the SCOR qualifier itself moves v1.1→v2.0
on 26 August 2026.

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

## Topic-level lab coverage

Every exam topic across **all current Cisco Security certifications** — the
SCOR core, all seven CCNP Security concentrations, and CCIE Security — is
covered by a hands-on **walkthrough** lab or a Design Exercise. Exam topics
were harvested from Cisco's official exam-topics PDFs
(`learningcontent.cisco.com`) on 24 July 2026 (SCOR v2.0, the edition current
from 26 August 2026). Labs use the FTD/FMC, ISE, ASA/IOS, ESA/WSA, and Secure
Access / XDR CLIs and APIs; each carries `**Lab verified by:** *pending*`
until a human runs it. (SAUTO 300-735 is retired and excluded.)

| Certification | Exam | Coverage |
| --- | --- | --- |
| CCNP Sec. core / CCIE written | 350-701 SCOR v2.0 | Domains 1–6 across Chapters 01–08 (see below) |
| CCNP Sec. concentration | 300-710 SNCF | Chapter 02, Labs 2.1–2.22 |
| CCNP Sec. concentration | 300-715 SISE | Chapter 06, Labs 6.1–6.29 |
| CCNP Sec. concentration | 300-720 SESA | Chapter 04, Labs 4.1–4.31 |
| CCNP Sec. concentration | 300-725 SWSA | Chapter 04, Labs 4.32–4.68 |
| CCNP Sec. concentration | 300-730 SVPN | Chapter 07, Labs 7.1–7.20 |
| CCNP Sec. concentration | 300-740 SCAZT | Chapter 08, Labs 8.1–8.30 |
| CCNP Sec. concentration | 300-745 SDSI | Chapter 09 **Design Exercise** |
| **CCIE Security** | written 350-701 + 8-hr lab | see module map below |

**SCOR 350-701 v2.0** maps by domain: Domain 1 (Security Concepts) → Chapter
01 Labs 1.1–1.10; Domain 2 (Network Security) → the SNCF firewall labs
(Chapter 02) and SVPN labs (Chapter 07); Domain 3 (Cloud) → Chapter 03 Labs
3.1–3.7; Domain 4 (Secure Service Edge) → Chapter 03 Labs 3.8–3.12; Domain 5
(Endpoint) → the SESA/SWSA and Secure Endpoint labs (Chapter 04); Domain 6
(Secure Network Access, Visibility, Enforcement) → Chapter 05 Labs 5.1–5.8
and the ISE labs (Chapter 06).

The six implementation concentrations map one lab per exam topic:

**SNCF 300-710 → Chapter 2**

| Exam topic | Lab |
| --- | --- |
| 1.1 Implement Secure Firewall modes | Lab 2.1 |
| 1.2 Implement NGIPS modes | Lab 2.2 |
| 1.3 Implement high availability options | Lab 2.3 |
| 1.4 Describe virtual appliance on-premises and cloud deployment | Lab 2.4 |
| 2.1 Configure system settings in Secure Firewall Management Center | Lab 2.5 |
| 2.2 Configure policies in Secure Firewall Management Center | Lab 2.6 |
| 2.3 Configure these features using Secure Firewall Management Center | Lab 2.7 |
| 2.4 Configure objects using Secure Firewall Management Center | Lab 2.8 |
| 2.5 Configure devices using Secure Firewall Management Center | Lab 2.9 |
| 2.6 Describe the use of Snort within Secure Firewall Threat Defense | Lab 2.10 |
| 3.1 Troubleshoot with Secure Firewall Management Center GUI and device CLI | Lab 2.11 |
| 3.2 Configure dashboards and reporting in Secure Firewall Management Center | Lab 2.12 |
| 3.3 Troubleshoot using: | Lab 2.13 |
| 3.4 Analyze risk and standard reports | Lab 2.14 |
| 3.5 Describe device management tools | Lab 2.15 |
| 4.1 Configure Cisco Secure Firewall Malware Defense (formerly AMP for Networks) in | Lab 2.16 |
| 4.2 Configure Cisco Secure Endpoint (formerly AMP for Endpoints) integration with Secure | Lab 2.17 |
| 4.3 Implement Threat Intelligence Director for third-party security intelligence feeds | Lab 2.18 |
| 4.4 Describe using Cisco SecureX for security investigations | Lab 2.19 |
| 4.5 Describe Secure Firewall Management Center integration using pxGrid | Lab 2.20 |
| 4.6 Describe Rapid Threat Containment (RTC) functionality within Secure Firewall | Lab 2.21 |
| 4.7 Describe Cisco Security Analytics and Logging | Lab 2.22 |

**SESA 300-720 → Chapter 4**

| Exam topic | Lab |
| --- | --- |
| 1.1 Configure Cisco Secure Email Gateway features | Lab 4.1 |
| 1.2 Describe centralized services on a Cisco Secure Email and Web Manager | Lab 4.2 |
| 1.3 Configure mail policies | Lab 4.3 |
| 1.4 Integrate Cisco Secure Email Gateway with SecureX | Lab 4.4 |
| 1.5 Configure Cisco Secure Email Threat Defense | Lab 4.5 |
| 2.1 Control spam with Talos SenderBase and Antispam | Lab 4.6 |
| 2.2 Describe graymail management solution | Lab 4.7 |
| 2.3 Configure file reputation filtering and file analysis features | Lab 4.8 |
| 2.4 Implement malicious or undesirable URLs protection | Lab 4.9 |
| 2.5 Describe the bounce verification feature | Lab 4.10 |
| 3.1 Describe the functions and capabilities of content filters | Lab 4.11 |
| 3.2 Create text resources such as content dictionaries, disclaimers, and templates | Lab 4.12 |
| 3.3 Configure message filters components, rules, processing order, and attachment | Lab 4.13 |
| 3.4 Configure scan behavior | Lab 4.14 |
| 3.5 Configure the Cisco Secure Email Gateway to scan for viruses using Sophos and McAfee | Lab 4.15 |
| 3.6 Configure outbreak filters | Lab 4.16 |
| 3.7 Configure Data Loss Prevention (DLP) | Lab 4.17 |
| 4.1 Configure and verify LDAP servers and queries (Queries and Directory Harvest Attack) | Lab 4.18 |
| 4.2 Understand spam quarantine functions | Lab 4.19 |
| 4.3 Understand SMTP functionality | Lab 4.20 |
| 5.1 Configure Domain Keys and DKIM signing | Lab 4.21 |
| 5.2 Configure SPF and SIDF | Lab 4.22 |
| 5.3 Configure DMARC verification | Lab 4.23 |
| 5.4 Configure forged email detection | Lab 4.24 |
| 5.5 Configure email encryption | Lab 4.25 |
| 5.6 Describe S/MIME security services and communication encryption with other MTAs | Lab 4.26 |
| 5.7 Configure Cisco Secure Email | Lab 4.27 |
| 6.1 Configure quarantine (spam, policy, virus, and outbreak) | Lab 4.28 |
| 6.2 Use safelists and blocklists to control email delivery | Lab 4.29 |
| 6.3 Manage messages in local or external spam quarantines | Lab 4.30 |
| 6.4 Configure virtual gateways | Lab 4.31 |

**SWSA 300-725 → Chapter 4**

| Exam topic | Lab |
| --- | --- |
| 1.1 Describe Cisco Secure Web Appliance features and functionality | Lab 4.32 |
| 1.2 Describe Secure Web Appliance solutions | Lab 4.33 |
| 1.3 Integrate Cisco Secure Web Appliance with Advanced Web Security Reporting | Lab 4.34 |
| 1.4 Integrate Cisco Secure Web Appliance with Cisco ISE | Lab 4.35 |
| 1.5 Troubleshoot data security and external data loss using log files | Lab 4.36 |
| 2.1 Perform initial configuration tasks on Cisco Secure Web Appliance | Lab 4.37 |
| 2.2 Configure an access policy | Lab 4.38 |
| 2.3 Configure and verify web proxy features | Lab 4.39 |
| 2.4 Configure a referrer header to filter web categories | Lab 4.40 |
| 3.1 Describe deployment options | Lab 4.41 |
| 3.2 Describe these features: | Lab 4.42 |
| 3.3 Describe the functions of a Proxy Auto-Configuration (PAC) file | Lab 4.43 |
| 3.4 Describe the SOCKS protocol and the SOCKS proxy services | Lab 4.44 |
| 4.1 Describe authentication features | Lab 4.45 |
| 4.2 Configure traffic redirection to Cisco Secure Web Appliance using transparent proxy | Lab 4.46 |
| 4.3 Describe the FTP proxy authentication | Lab 4.47 |
| 4.4 Troubleshoot authentication issues | Lab 4.48 |
| 5.1 Describe SSL and TLS inspection | Lab 4.49 |
| 5.2 Configure HTTPS capabilities | Lab 4.50 |
| 5.3 Configure self-signed and intermediate certificates within SSL/TLS transactions | Lab 4.51 |
| 6.1 Describe access policies | Lab 4.52 |
| 6.2 Describe identification profiles and authentication | Lab 4.53 |
| 6.3 Troubleshoot using access logs | Lab 4.54 |
| 7.1 Configure URL filtering | Lab 4.55 |
| 7.2 Configure time-based and traffic volume acceptable use policies and end user | Lab 4.56 |
| 7.3 Configure web application visibility and control (Office 365, third-party feeds) | Lab 4.57 |
| 7.4 Create a corporate global acceptable use policy | Lab 4.58 |
| 7.5 Implement policy trace tool to verify corporate global acceptable use policy | Lab 4.59 |
| 7.6 Configure Secure Web Appliance to inspect archive file types | Lab 4.60 |
| 8.1 Describe scanning engines | Lab 4.61 |
| 8.2 Configure file reputation filtering and file analysis | Lab 4.62 |
| 8.3 Describe Cisco Secure Endpoint | Lab 4.63 |
| 8.4 Describe integration with Cognitive Intelligence | Lab 4.64 |
| 9.1 Configure and analyze web tracking reports | Lab 4.65 |
| 9.2 Configure Cisco Advanced Web Security Reporting (AWSR) | Lab 4.66 |
| 9.3 Troubleshoot connectivity issues | Lab 4.67 |
| 9.4 Interpret system health using the System Health Dashboard | Lab 4.68 |
| 9.5 Describe REST API support | Lab 4.69 |

**SISE 300-715 → Chapter 6**

| Exam topic | Lab |
| --- | --- |
| 1.1 Configure personas | Lab 6.1 |
| 1.2 Describe deployment options | Lab 6.2 |
| 1.3 Describe hardware and virtual machine performance specifications | Lab 6.3 |
| 1.4 Describe zero-touch provisioning | Lab 6.4 |
| 2.1 Configure native AD and LDAP | Lab 6.5 |
| 2.2 Describe identity store options | Lab 6.6 |
| 2.3 Configure wireless network access using 802.1X | Lab 6.7 |
| 2.4 Configure wired network access using 802.1X and IBNS 2.0 | Lab 6.8 |
| 2.5 Implement MAB | Lab 6.9 |
| 2.6 Configure Cisco TrustSec | Lab 6.10 |
| 2.7 Configure policies including authentication and authorization profiles | Lab 6.11 |
| 3.1 Configure web authentication | Lab 6.12 |
| 3.2 Configure guest access services | Lab 6.13 |
| 3.3 Configure sponsor and guest portals | Lab 6.14 |
| 4.1 Implement profiler services | Lab 6.15 |
| 4.2 Implement probes | Lab 6.16 |
| 4.3 Implement CoA | Lab 6.17 |
| 4.4 Configure endpoint identity management | Lab 6.18 |
| 5.1 Describe Cisco BYOD functionality | Lab 6.19 |
| 5.2 Configure BYOD device on-boarding using internal CA with Cisco switches and Cisco | Lab 6.20 |
| 5.3 Configure certificates for BYOD | Lab 6.21 |
| 5.4 Configure block list/allow list | Lab 6.22 |
| 6.1 Describe endpoint compliance, posture services, and client provisioning | Lab 6.23 |
| 6.2 Configure posture conditions and policy, and client provisioning | Lab 6.24 |
| 6.3 Configure the compliance module | Lab 6.25 |
| 6.4 Configure posture agents and operational modes | Lab 6.26 |
| 6.5 Describe supplicant, supplicant options, authenticator, and server | Lab 6.27 |
| 7.1 Compare AAA protocols | Lab 6.28 |
| 7.2 Configure TACACS+ device administration and command authorization | Lab 6.29 |

**SVPN 300-730 → Chapter 7**

| Exam topic | Lab |
| --- | --- |
| 1.1 Describe GETVPN | Lab 7.1 |
| 1.2 Implement DMVPN | Lab 7.2 |
| 1.3 Implement FlexVPN using local AAA | Lab 7.3 |
| 2.1 Implement AnyConnect IKEv2 VPNs on ASA and routers | Lab 7.4 |
| 2.2 Implement AnyConnect SSL VPN on ASA | Lab 7.5 |
| 2.3 Implement Clientless SSL VPN on ASA | Lab 7.6 |
| 2.4 Implement Flex VPN on routers | Lab 7.7 |
| 3.1 Troubleshoot IPsec | Lab 7.8 |
| 3.2 Troubleshoot DMVPN | Lab 7.9 |
| 3.3 Troubleshoot FlexVPN | Lab 7.10 |
| 3.4 Troubleshoot AnyConnect IKEv2 and SSL VPNs on ASA and routers | Lab 7.11 |
| 3.5 Troubleshoot and Clientless SSL VPN on ASA | Lab 7.12 |
| 4.1 Identify functional components of GETVPN, FlexVPN, DMVPN, and IPsec for site-to-site | Lab 7.13 |
| 4.2 Identify functional components of FlexVPN, IPsec, and Clientless SSL for remote access | Lab 7.14 |
| 4.3 Identify VPN technology based on configuration output for site-to-site VPN solutions | Lab 7.15 |
| 4.4 Identify VPN technology based on configuration output for remote access VPN solutions | Lab 7.16 |
| 4.5 Identify split tunneling requirements for remote access VPN solutions | Lab 7.17 |
| 4.6 Design site-to-site VPN solutions | Lab 7.18 |
| 4.7 Design remote access VPN solutions | Lab 7.19 |
| 4.8 Identify Elliptic Curve Cryptography (ECC) algorithms | Lab 7.20 |

**SCAZT 300-740 → Chapter 8**

| Exam topic | Lab |
| --- | --- |
| 1.1 Describe the components of the Cisco Security Reference Architecture | Lab 8.1 |
| 1.2 Describe use cases and the recommended capabilities within an integrated architecture | Lab 8.2 |
| 1.3 Describe industry security frameworks such as NIST, CISA, and DISA | Lab 8.3 |
| 1.4 Describe the SAFE architectural framework | Lab 8.4 |
| 1.5 Describe the SAFE Key structure | Lab 8.5 |
| 2.1 Implement user and device authentication via identity certificates | Lab 8.6 |
| 2.2 Implement multifactor authentication for users and devices | Lab 8.7 |
| 2.3 Implement endpoint posture policies for user access to resources | Lab 8.8 |
| 2.4 Configure SAML/SSO and OIDC using an identity provider connection | Lab 8.9 |
| 2.5 Configure user and device trust using SAML authentication for a mobile or web | Lab 8.10 |
| 3.1 Determine security policies for endpoints to permit access to cloud applications | Lab 8.11 |
| 3.2 Determine security policies for endpoints to permit access to SaaS applications such as | Lab 8.12 |
| 3.3 Determine security policies for remote users using VPN or application-based | Lab 8.13 |
| 3.4 Determine security policies for network security edge to enforce application policy | Lab 8.14 |
| 4.1 Describe the MITRE ATT&CK framework and attacker defense mitigation techniques | Lab 8.15 |
| 4.2 Describe cloud security attack tactics and mitigation strategies | Lab 8.16 |
| 4.3 Describe how web application firewall protect against DDoS attacks | Lab 8.17 |
| 4.4 Determine security policies for application enforcement using Cisco Secure Workload | Lab 8.18 |
| 4.5 Determine cloud (hybrid and multicloud) platform security policies based on application | Lab 8.19 |
| 5.1 Describe the Cisco XDR solution | Lab 8.20 |
| 5.2 Describe use cases for visibility and assurance automation | Lab 8.21 |
| 5.3 Describe benefits and capabilities of visibility and logging tools such as SIEM, Open | Lab 8.22 |
| 5.4 Validate traffic flow and telemetry reports for baseline and compliance behavior | Lab 8.23 |
| 5.5 Diagnose issues with user application and workload access | Lab 8.24 |
| 5.6 Verify user access to applications and data using tools (firewall logs, Duo, Umbrella, and | Lab 8.25 |
| 5.7 Analyze application dependencies using tools such as firewall logs and Cisco Secure | Lab 8.26 |
| 6.1 Describe use cases for response automation | Lab 8.27 |
| 6.2 Determine actions based on telemetry reports | Lab 8.28 |
| 6.3 Determine policies based on security audit reports | Lab 8.29 |
| 6.4 Determine action based on user or application compromise | Lab 8.30 |

### CCIE Security

The CCIE Security **written qualifier is 350-701 SCOR**, covered above. The
8-hour hands-on **lab** blueprint is expert-depth application of the same
technologies; its modules map to this volume's labs:

| CCIE Security lab module | Chapters / labs |
| --- | --- |
| Perimeter Security and Intrusion Prevention | Chapter 02 (Secure Firewall/IPS) |
| Secure Connectivity and Segmentation | Chapter 07 (VPNs), Chapters 05–06 (segmentation) |
| Infrastructure Security | Chapters 05–06 (802.1X, TrustSec, device hardening) |
| Identity Management, Information Exchange, Access Control | Chapter 06 (ISE) |
| Advanced Threat Protection and Content Security | Chapter 04 (email/web/endpoint) |
| Cloud, Zero-Trust, and Automation | Chapters 03, 08 (SSE/ZTNA), Chapter 09 (automation) |

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-25-cisco-security
```
