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

This volume covers NSE 1–4 of the Fortinet NSE 1–8 training and
certification program, tracked in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). It
names blueprint domains and points to the Fortinet Training Institute as
the controlling source; it does not reproduce proprietary assessment
content. Always confirm the current blueprint against Fortinet's official
training site before using this volume for exam preparation.

### The program changed on 15 July 2026 — and changed back

Fortinet's certification naming has now moved twice. The NSE 1–8 levels
were replaced by named credentials — FCF, FCA, FCP, FCSS, and FCX — and
then, **effective 15 July 2026, those five were retired and NSE levels
returned**, in an expanded eight-level form.

This volume's NSE naming is therefore current again, but for an accident
of timing rather than because it was never revised. The structure it
describes is now incomplete: the program runs to NSE 8 and branches at
the upper levels.

| Level | Structure after 15 July 2026 |
| --- | --- |
| NSE 1–3 | Entry-level, foundational |
| NSE 4 | Administrator level — where this volume ends |
| NSE 5, 6, 7 | Four tracks each: Secure Networking, Security Operations, SASE, Cloud Security |
| NSE 8 | Expert |
| Industry | Separate certifications in OT Security and MSSP Security |

**If you hold an FCP or FCSS, you have not lost it.** Fortinet maps
existing credentials automatically, and exams passed on or after **15
July 2024** qualify for the new mappings even without an active prior
certification. Published examples: FCP FortiGate Administrator maps to
NSE 4; FortiManager Administrator to NSE 6; FCSS Network Security Support
Engineer to NSE 6; Enterprise Firewall Administrator to NSE 7.

This transition is days old at the time of writing. Treat every detail
here as needing confirmation against the Fortinet Training Institute, and
expect third-party material — courses, practice exams, study guides — to
lag the naming in both directions for some months. Material written
against FCP is not wrong about the technology; it is wrong about the
label.

### The NSE 4 exam, and how Fortinet publishes weights

NSE 4 is where this volume ends and the first level with a substantial
proctored exam behind it. The current exam is **Fortinet NSE 4 — FortiOS
7.6 Administrator**, which matches the FortiOS baseline in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md).

| Term | Detail |
| --- | --- |
| Duration | 80–90 minutes |
| Questions | 50–55 |
| Format | Multiple choice and drag-and-drop, built on operational scenarios, configuration extracts, and troubleshooting captures |
| Scoring | Answers must be **100% correct** to score; no partial credit, and no deduction for wrong answers |
| Languages | English and Japanese |
| Product version | FortiOS 7.6.0 |

**Fortinet publishes weights as ranges, not fixed percentages** — a
different convention from most vendors in this encyclopedia, and one that
changes how the numbers should be read:

| Objective | Weight | Chapters |
| --- | --- | --- |
| Content Inspection | **25–30%** | [07](chapters/07-fortiguard-security-profiles-ssl-inspection-and-threat-prevention.md) |
| Deployment and System Configuration | **20–25%** | [04](chapters/04-fortigate-first-deployment-licensing-management-and-hardening.md), [05](chapters/05-interfaces-routing-nat-virtual-domains-and-high-availability.md) |
| Firewall Policies and Authentication | **20–25%** | [06](chapters/06-firewall-policy-authentication-vpn-and-zero-trust-access.md) |
| Routing | 10–15% | [05](chapters/05-interfaces-routing-nat-virtual-domains-and-high-availability.md), [08](chapters/08-sd-wan-operations-central-management-automation-and-troubleshooting.md) |
| VPNs | 10–15% | [06](chapters/06-firewall-policy-authentication-vpn-and-zero-trust-access.md) |

**The ranges do not sum to 100% at either bound** — the minimums total
85% and the maximums 110%. That is not an error to correct; it is what
ranges mean. Any given sitting lands somewhere inside, and the practical
consequence is that you cannot budget study time by exact proportion the
way a Dell or Cisco blueprint allows. Plan against the *upper* bound of
each objective, because a sitting weighted toward the top of one range is
entirely possible.

**Content inspection is the largest single objective** at up to 30%, and
it is the one candidates most often under-prepare: SSL/SSH deep
inspection, web filtering behavior differences across inspection modes,
application control, antivirus scanning modes, and IPS. All of it lands
in [Chapter 07](chapters/07-fortiguard-security-profiles-ssl-inspection-and-threat-prevention.md).

Two things inside the objectives are worth flagging because they sit
outside the classic on-box FortiGate picture: the deployment objective
now names **cloud-native firewall, public cloud solutions, and FortiSASE
administration**. A candidate preparing only against an on-premises
FortiGate VM will meet questions the lab did not cover.

### Study plan

Six to eight weeks to NSE 4 at eight to ten hours a week for someone with
general networking experience, assuming NSE 1–3 are taken as they are
reached rather than studied separately — they are short, free, and
largely awareness-level.

| Week | Focus | Objective weight |
| --- | --- | --- |
| 1 | NSE 1–3 end to end: cybersecurity awareness, threat landscape, the Fortinet portfolio, and Security Fabric concepts. Chapters 01–03. Sit all three as you finish them. | — |
| 2 | First FortiGate deployment: initial configuration, licensing, administrative access, DHCP, logging and diagnostics, hardening. Chapter 04. | part of 20–25% |
| 3 | Interfaces, routing, NAT, VDOMs, and FGCP high availability. Chapters 04–05. Add SD-WAN load balancing from Chapter 08 here, since routing owns it. | 10–15% + rest of 20–25% |
| 4 | Firewall policies, inspection modes, SNAT and DNAT with VIPs, and authentication — LDAP, RADIUS, FSSO. Chapter 06. | 20–25% |
| 5–6 | **The heavy weeks.** Content inspection in full: SSL/SSH inspection, web filtering across modes, application control, antivirus scanning modes, IPS. Chapter 07, with deliberate time on inspection-mode differences rather than reading them once. | 25–30% |
| 7 | IPsec VPN implementation and troubleshooting, then cloud-native firewall and FortiSASE — the objectives an on-box lab does not reach. Chapters 06 and 08. | 10–15% + cloud coverage |
| 8 | The capstone in [Chapter 09](chapters/09-nse-4-fortios-administrator-training-and-enterprise-capstone.md), then targeted revision. | — |

**Practice the scoring rule, not just the material.** Multi-select
questions score only when *every* selection is right, with no partial
credit — so a candidate who half-knows six topics scores worse than one
who fully knows four. When revising, drill to the point of being able to
exclude wrong options confidently rather than to the point of
recognition.

### Practicing without hardware

Fortinet's own training is unusually accessible compared with most
vendors in this encyclopedia:

| Route | Cost | Notes |
| --- | --- | --- |
| [Fortinet Training Institute](https://training.fortinet.com/) | Free self-paced tiers | The entry levels have long been free; this volume's Chapters 01–03 follow them |
| FortiGate VM trial | Free, own hypervisor | A time-limited evaluation image — the practical route to Chapters 04–08 |
| Fortinet Free NSE Training | Free | Self-paced courses with lab access varying by course |
| Instructor-led courses | Paid | Delivered by Fortinet and Authorized Training Centers |

The FortiGate VM evaluation image is the important one. Chapters 04
through 08 — deployment, interfaces and routing, policy and VPN, security
profiles, SD-WAN — are all reachable on a virtual FortiGate in a
hypervisor, which is the same break-and-rebuild loop the labs in those
chapters assume. Confirm current evaluation terms before planning around
them, since licensing conditions change more often than the software.

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
