# Volume LXIV — HPE Aruba Networking Certification Tracks

> The whole HPE Aruba Networking certification program in one volume — the Associate,
> Professional, and Expert tiers across Campus Access, Switching, Network Security, Mobility,
> and Data Center, plus the Network Architect design tier — on AOS-CX, Aruba Central, and
> ClearPass, with hands-on CLI, REST, pyaoscx, and Ansible labs, verified against
> certification-learning.hpe.com.

## Overview

Volume LXIV maps the **HPE Aruba Networking** certification program — the credentials for
operating, securing, and automating Aruba's campus, wireless, security, and data-center
platform (**AOS-CX**, **Aruba Central**, **ClearPass**, gateways). It joins the encyclopedia's
networking volumes (Cisco III/XXV/XXVII–XXX, Juniper XXXI, Arista LXII) and the automation
volumes (NetBox LII, Python for Network Engineers LVIII, Ansible LIX) that its automation
content builds on.

This is a **certification-tracks** volume, like the other vendor volumes (XXXIX–LXIII): it maps
the program — the tiers, tracks, and exam codes — and teaches each with a hands-on walkthrough.
The program was rebranded from "Aruba Certified" to **HPE Aruba Networking Certified** and
renumbered (HPE6-/HPE7- codes); every credential was **verified against
certification-learning.hpe.com and hpepress.hpe.com on 28 July 2026**.

Chapters are organized by track:

- **Chapter 01** frames the program — tiers, tracks, exam codes, and the platform.
- **Chapter 02** takes the **Campus Access** track.
- **Chapter 03** takes the **Switching** track (AOS-CX, VSX, VSF).
- **Chapter 04** takes the **Network Security** track (ClearPass, PEF, dynamic segmentation).
- **Chapter 05** takes **Mobility / WLAN**.
- **Chapter 06** takes the **Data Center** track (EVPN-VXLAN, CX 10000).
- **Chapter 07** covers **Aruba Central and automation** (REST, pyaoscx, Ansible).
- **Chapter 08** covers the **Network Architect** design tier.
- **Chapter 09** covers keeping current and career paths.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on labs and
knowledge checks.

## Chapters

1. [The HPE Aruba Networking Certification Program](chapters/01-the-hpe-aruba-networking-certification-program.md) — tiers, tracks, codes, platform.
2. [Campus Access Track](chapters/02-campus-access-track.md) — AOS-CX access, Central, dynamic segmentation.
3. [Switching Track](chapters/03-switching-track.md) — VLANs, routing, VSX, VSF, REST.
4. [Network Security Track](chapters/04-network-security-track.md) — ClearPass, 802.1X, PEF, NAC.
5. [Mobility and WLAN](chapters/05-mobility-and-wlan.md) — SSIDs, WPA3, RF, gateways.
6. [Data Center Track](chapters/06-data-center-track.md) — EVPN-VXLAN, VSX, CX 10000.
7. [Aruba Central and Automation](chapters/07-aruba-central-and-automation.md) — REST, pyaoscx, Ansible, NetConductor.
8. [Design and the Network Architect Tier](chapters/08-design-and-network-architect.md) — HPE7-A03/A04 design.
9. [Keeping the Aruba Program Current and Career Paths](chapters/09-keeping-current-and-career-paths.md) — recert, rebrand, paths.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for HPE Aruba Networking, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The full catalog with tiers,
tracks, exam codes, and the HPE training model is in the
[HPE Aruba Networking certification appendix](../volume-997-master-appendices/chapters/30-appendix-hpe-aruba-networking-certifications-and-course-access.md)
(Master Appendices, Volume CMXCVII). Related practice lives in the Cisco (III, XXV, XXVII–XXX),
Juniper (XXXI), Arista (LXII), NetBox (LII), Python for Network Engineers (LVIII), and Ansible
(LIX) volumes.

## Lab coverage

The credential chapters go **per topic**: there is **one walkthrough lab for every topic area**
of the tracks — **36 labs** across the program. Because Aruba is a hands-on platform, the
walkthroughs use real tooling — the **AOS-CX CLI**, the **AOS-CX REST API** and **pyaoscx** SDK,
**ClearPass** policy, the **Aruba Central** API, **EVPN-VXLAN** and **VSX** config, and **Ansible
`arubanetworks.aos_cx`** — runnable on virtual AOS-CX (GNS3/containerlab), Aruba Central trials,
and the ClearPass eval. Each lab states an objective, commands, expected results, a negative
test, and cleanup, and ends with a **`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **certification-learning.hpe.com** and **hpe.com/networkingtraining**
(the program and datasheets), **AOS-CX**, **Aruba Central**, **ClearPass**, and Aruba gateways,
with **pyaoscx** and **Ansible `arubanetworks.aos_cx`** for automation. The program and its exam
codes were verified against certification-learning.hpe.com and hpepress.hpe.com on 28 July 2026;
HPE rebrands and renumbers as the platform evolves, so confirm the current tracks and codes
before scheduling.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-64-aruba-certifications
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
