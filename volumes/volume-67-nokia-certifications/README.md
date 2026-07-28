# Volume LXVII — Nokia Certification Tracks

> The whole Nokia Service Routing Certification (SRC) program in one volume — NRS I fundamentals,
> the NRS II professional credential (composite written plus the practical lab), and the Service
> Routing Architect — on SR OS, with hands-on classic-CLI/MD-CLI, IGP/BGP/MPLS/services, and
> pySROS labs, verified against nokia.com.

## Overview

Volume LXVII maps the **Nokia Service Routing Certification (SRC)** program — the credentials for
designing and operating IP/MPLS service-provider networks on Nokia's **SR OS** (the 7750 SR, 7450
ESS, and 7950 XRS platforms). It joins the encyclopedia's service-provider and networking volumes
(Cisco Service Provider XXIX, Juniper XXXI, Arista LXII, Aruba LXIV, F5 LXVI) and the automation
volumes (NetBox LII, Python for Network Engineers LVIII) that its model-driven content builds on.

This is a **certification-tracks** volume, like the other vendor volumes (XXXIX–LXVI): it maps the
program — the levels, exams, and technologies — and teaches each with a hands-on walkthrough. Every
credential was **verified against nokia.com on 28 July 2026**.

Chapters follow the ladder:

- **Chapter 01** frames the program — NRS I/II and SRA, the exams, and the SR OS platform.
- **Chapter 02** takes **NRS I** (fundamentals and base SR OS).
- **Chapters 03–07** take **NRS II** (IGP; BGP; MPLS/Segment Routing; services; the practical lab).
- **Chapter 08** takes the **Service Routing Architect (SRA)** design credential.
- **Chapter 09** covers automation, currency, and career paths.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on labs and
knowledge checks.

## Chapters

1. [The Nokia Service Routing Certification Program](chapters/01-the-nokia-service-routing-certification-program.md) — NRS I/II, SRA, SR OS.
2. [NRS I — IP and Services Foundations](chapters/02-nrs-i-foundations.md) — 4A0-100: TCP/IP, SR OS CLI/MD-CLI.
3. [NRS II — IGP: OSPF and IS-IS](chapters/03-nrs-ii-igp-ospf-and-isis.md) — the 4A0-C03/C04 variants.
4. [NRS II — BGP](chapters/04-nrs-ii-bgp.md) — IBGP/EBGP and route policy.
5. [NRS II — MPLS and Segment Routing](chapters/05-nrs-ii-mpls-and-segment-routing.md) — LDP, RSVP-TE, SR.
6. [NRS II — Services](chapters/06-nrs-ii-services.md) — Epipe/VLL, VPLS, VPRN, EVPN.
7. [NRS II — The Practical Lab](chapters/07-nrs-ii-practical-lab.md) — 4A0-N01: integration and troubleshooting.
8. [Service Routing Architect (SRA)](chapters/08-sra-service-routing-architect.md) — 4A0-112: end-to-end design.
9. [Automation, Currency, and Career Paths](chapters/09-automation-currency-and-career.md) — MD-CLI/NETCONF/pySROS, recert.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for Nokia, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The full catalog with levels and
exams is in the
[Nokia certification appendix](../volume-97-master-appendices/chapters/33-appendix-nokia-certifications-and-course-access.md)
(Master Appendices, Volume XCVII). Related practice lives in the Cisco Service Provider (XXIX),
Juniper (XXXI), Arista (LXII), NetBox (LII), and Python for Network Engineers (LVIII) volumes.

## Lab coverage

The credential chapters go **per topic**: there is **one walkthrough lab for every exam domain** of
the ladder — **35 labs** in all. Because SR OS is a hands-on platform, the walkthroughs use real
tooling — the **classic CLI** and **MD-CLI**, **OSPF/IS-IS/BGP/MPLS/SR** configuration, the
**service model** (Epipe/VPLS/VPRN/EVPN), and **pySROS/NETCONF** automation — runnable on **SR OS
VSR** in containerlab/EVE-NG. Each lab states an objective, commands, expected results, a negative
test, and cleanup, and ends with a **`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **nokia.com/networks/training/src** (the program and exams) and **Nokia SR
OS** (classic CLI and MD-CLI), with **pySROS**, **NETCONF**, and **gRPC/gNMI** for automation. The
program was verified against nokia.com on 28 July 2026; Nokia evolves the SRC program with the
platform (Segment Routing, SRv6, EVPN), so confirm the current exams before scheduling.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-67-nokia-certifications
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
