# Volume LXII — Arista Certification Tracks

> The whole Arista Certified Engineer (ACE) program in one volume — Network Foundations
> (Associate), the Data Center, Campus, and WAN Routing Specialist tracks, and the
> Automation track to Professional — on EOS and CloudVision, with hands-on CLI, eAPI,
> EVPN/VXLAN, and AVD labs mapped to every track, verified against training.arista.com.

## Overview

Volume LXII maps the **Arista** certification program — the credentials for operating,
engineering, and automating **Arista EOS** networks managed by **CloudVision**. It joins
the encyclopedia's **networking** volumes (Cisco III/XXV/XXVII–XXX, Juniper XXXI) and the
automation volumes (NetBox LII, Python for Network Engineers LVIII, Ansible LIX) that its
Automation track builds on.

This is a **certification-tracks** volume, like the other vendor volumes (XXXIX–LXI): it
maps the program — which credentials exist, their topic areas, and levels — and teaches
each with a hands-on walkthrough. The program was **revised on 1 June 2025** into a Learning
Track model (Associate → Specialist → Professional), and every credential was **verified
against training.arista.com on 27 July 2026**.

Chapters are organized by track:

- **Chapter 01** frames the program — EOS, CloudVision, the tracks/tiers, and eAPI.
- **Chapter 02** takes **Network Foundations (Associate)**.
- **Chapters 03–04** take the **Data Center** track (Operations, then Engineering/
  EVPN-VXLAN).
- **Chapter 05** takes the **Campus** track (Operations and Engineering).
- **Chapter 06** takes the **WAN Routing** track (MPLS Core).
- **Chapter 07** takes the **Automation** track (Foundations and Advanced → Professional).
- **Chapter 08** covers **CloudVision** across all tracks.
- **Chapter 09** covers keeping current and career paths.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on
labs and knowledge checks.

## Chapters

1. [The Arista Certification Program](chapters/01-the-arista-certification-program.md) — EOS, CloudVision, tracks/tiers, and eAPI.
2. [Network Foundations — Associate](chapters/02-network-foundations-associate.md) — EOS, switching, routing.
3. [Data Center — Operations](chapters/03-data-center-operations.md) — leaf-spine, MLAG, telemetry, troubleshooting.
4. [Data Center — Engineering (EVPN/VXLAN)](chapters/04-data-center-engineering-evpn-vxlan.md) — underlay, overlay, EVPN, anycast gateway.
5. [Campus — Operations and Engineering](chapters/05-campus-operations-and-engineering.md) — PoE, 802.1X, campus fabric, MSS.
6. [WAN Routing — MPLS Core](chapters/06-wan-routing-mpls-core.md) — MPLS/LDP and L3VPN.
7. [Automation — Foundations and Advanced](chapters/07-automation-foundations-and-advanced.md) — eAPI/pyeapi, Ansible, Jinja, AVD.
8. [CloudVision Across the Tracks](chapters/08-cloudvision-across-the-tracks.md) — Studios, telemetry, Change Control, MSS.
9. [Keeping the Arista Program Current and Career Paths](chapters/09-keeping-the-arista-program-current-and-career-paths.md) — the 2025 revision, recert, and paths.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for Arista, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The full catalog with
tracks, tiers, and the Arista Academy training model is in the
[Arista certification appendix](../volume-997-master-appendices/chapters/28-appendix-arista-certifications-and-course-access.md)
(Master Appendices, Volume CMXCVII). Related practice lives in the Cisco (III, XXV,
XXVII–XXX), Juniper (XXXI), NetBox (LII), Python for Network Engineers (LVIII), and Ansible
(LIX) volumes.

## Lab coverage

The credential chapters go **per topic**: there is **one walkthrough lab for every topic
area** of each ACE track — **36 labs** across the program. Because Arista is a hands-on
platform, the walkthroughs use real tooling — the **EOS CLI**, **eAPI** (JSON-RPC) and
**pyeapi**, **EVPN/VXLAN** and **MPLS** config, **Ansible `arista.eos`** and **AVD**, and
the **CloudVision** API — runnable on free **cEOS/vEOS** images (containerlab) or Arista
Test Drive. Each lab states an objective, commands, expected results, a negative test, and
cleanup, and ends with a **`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **training.arista.com** and **arista.com** (the ACE program and
docs), **Arista EOS** and **CloudVision (CVP)**, free **cEOS/vEOS** images and **Arista Test
Drive** for practice, and eAPI/AVD automation. The program (revised 1 June 2025) and its
tracks were verified against training.arista.com on 27 July 2026; Arista revises the program
as the platform evolves, so confirm the current tracks before scheduling.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-062-arista-certifications
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
