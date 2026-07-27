# Volume LVI — Infoblox Certification Tracks

> The whole Infoblox certification program in one volume — NIOS DDI (Operator,
> Administrator, Expert), Universal DDI and Threat Defense, NetMRI Administrator, and
> the vendor-agnostic Industry Learning credentials — with hands-on WAPI/Portal-API
> labs mapped to every topic area, verified against education.infoblox.com.

## Overview

Volume LVI maps the **Infoblox** certification program — the credentials for operating
**DDI** (DNS, DHCP, and IP address management) and **DNS-layer security** across the
on-premises **NIOS Grid**, cloud-native **Universal DDI**, **Threat Defense**, and
**NetMRI**. It sits with the encyclopedia's **network foundations** (II) and **security**
(X) volumes and complements the NetBox source-of-truth volume (LII).

This is a **certification-tracks** volume, like the other vendor volumes (XXXIX–LI): it
maps the program — which credentials exist, their **topic areas**, and levels — and
teaches each with a hands-on walkthrough. Every credential was **verified against
launchpad.education.infoblox.com on 27 July 2026**. Infoblox publishes **topic areas**
but not question counts or weightings, so this volume maps a lab to each topic area.

Chapters are organized by credential:

- **Chapter 01** frames the program — DDI, the credential families, and the WAPI.
- **Chapters 02–04** take the **NIOS DDI** ladder: **INO** (Operator), **INA**
  (Administrator), **INE** (Expert).
- **Chapter 05** takes **Universal DDI** (NIOS-X and the Infoblox Portal).
- **Chapter 06** takes **Threat Defense** (DNS-layer security).
- **Chapter 07** takes **NetMRI Administrator (IMA)**.
- **Chapter 08** takes the vendor-agnostic **Industry Learning** credentials (DDIA/DDIP,
  DSA/DSP).
- **Chapter 09** covers keeping current and career paths.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on
labs and knowledge checks. The Threat Defense content is **defensive** DNS security only.

## Chapters

1. [The Infoblox Certification Program](chapters/01-the-infoblox-certification-program.md) — DDI, the credential families, and the WAPI.
2. [INO — NIOS DDI Operator](chapters/02-ino-nios-ddi-operator.md) — Grid fundamentals, DHCP, DNS, IPAM, object management.
3. [INA — NIOS DDI Administrator](chapters/03-ina-nios-ddi-administrator.md) — members, advanced DHCP/DNS, Discovery, access control, remote auth.
4. [INE — NIOS DDI Expert](chapters/04-ine-nios-ddi-expert.md) — Grid HA, upgrades, root-cause analysis, troubleshooting.
5. [Universal DDI](chapters/05-universal-ddi.md) — the Infoblox Portal, NIOS-X, DNS/DHCP, records/views/zones, redundancy.
6. [Threat Defense](chapters/06-threat-defense.md) — DNS-layer security: proxies, policies, endpoints, Threat Insight.
7. [IMA — NetMRI Administrator](chapters/07-ima-netmri-administrator.md) — discovery, config/change, compliance, automation.
8. [Industry Learning — DDI and DNS Security](chapters/08-industry-learning-ddi-and-dns-security.md) — the vendor-agnostic DDIA/DDIP and DSA/DSP.
9. [Keeping the Infoblox Program Current and Career Paths](chapters/09-keeping-the-infoblox-program-current-and-career-paths.md) — badges, program change, and paths.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for Infoblox, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The full catalog with
credentials, topic areas, and the Infoblox Education training model is in the
[Infoblox certification appendix](../volume-97-master-appendices/chapters/26-appendix-infoblox-certifications-and-course-access.md)
(Master Appendices, Volume XCVII). Related practice lives in the network foundations (II),
cybersecurity (X), and NetBox (LII) volumes.

## Lab coverage

The credential chapters go **per topic**: there is **one walkthrough lab for every topic
area** of each Infoblox credential — **38 labs** across the program. Because Infoblox is
an API-driven platform, the walkthroughs use real tooling — the **WAPI** (the NIOS REST
API), the **Infoblox Portal REST API** (Universal DDI and Threat Defense), the **NetMRI
API**, and standard **`dig`** for the vendor-agnostic material — against a NIOS Grid or
Portal tenant (with read-only patterns where no environment is available). Each lab
states an objective, commands, expected results, a negative test, and cleanup, and ends
with a **`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **education.infoblox.com** and
**launchpad.education.infoblox.com** (catalog and topic areas), the **NIOS Grid** and
**WAPI**, **Universal DDI** (the Infoblox Portal and NIOS-X), **Threat Defense**, and
**NetMRI**. Credentials and topic areas were verified against education.infoblox.com on
27 July 2026; Infoblox revises the program as the platform evolves, so confirm the
current catalog before scheduling.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-56-infoblox-certifications
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
