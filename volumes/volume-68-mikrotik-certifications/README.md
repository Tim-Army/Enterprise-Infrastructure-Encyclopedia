# Volume LXVIII — MikroTik Certification Tracks

> The whole MikroTik certification program in one volume — the MTCNA foundation and the specialist
> certificates (MTCRE, MTCTCE, MTCWE, MTCUME, MTCINE, MTCSE, MTCSWE, MTCIPv6E) — on RouterOS,
> with hands-on CLI, WinBox, REST-API, and CHR labs, verified against mikrotik.com.

## Overview

Volume LXVIII maps the **MikroTik** certification program — the credentials for deploying
**RouterOS** on RouterBOARD, CHR, and x86 across routing, switching, wireless, traffic control,
user management, and security. It joins the encyclopedia's networking volumes (Cisco XXV/XXIX,
Juniper XXXI, Arista LXII, Aruba LXIV, Nokia LXVII, F5 LXVI) and the automation volumes (NetBox
LII, Python for Network Engineers LVIII, Ansible LIX).

This is a **certification-tracks** volume, like the other vendor volumes (XXXIX–LXVII): it maps the
program — the certificates and their focus — and teaches each with a hands-on walkthrough.
**MTCNA is the prerequisite for every other certificate**; every credential was **verified against
mikrotik.com on 28 July 2026**.

Chapters follow the program:

- **Chapter 01** frames the program — MTCNA and the specialist certificates, and RouterOS.
- **Chapter 02** takes the **MTCNA** foundation.
- **Chapters 03–08** take the specialist certificates: **MTCRE** (routing); **MTCTCE** (traffic
  control); **MTCWE** (wireless); **MTCUME** (user management); **MTCINE** (inter-networking);
  and **MTCSE/MTCSWE/MTCIPv6E** (security, switching, IPv6).
- **Chapter 09** covers automation, currency, and career paths.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on labs and
knowledge checks.

## Chapters

1. [The MikroTik Certification Program](chapters/01-the-mikrotik-certification-program.md) — MTCNA and the specialist tracks.
2. [MTCNA — RouterOS Fundamentals](chapters/02-mtcna-routeros-fundamentals.md) — addressing, DHCP, NAT, firewall.
3. [MTCRE — Routing](chapters/03-mtcre-routing.md) — static, OSPF (v7), tunnels.
4. [MTCTCE — Traffic Control](chapters/04-mtctce-traffic-control.md) — packet flow, mangle, queues, proxy.
5. [MTCWE — Wireless](chapters/05-mtcwe-wireless.md) — APs, security, CAPsMAN.
6. [MTCUME — User Management](chapters/06-mtcume-user-management.md) — PPPoE, hotspot, RADIUS.
7. [MTCINE — Inter-networking](chapters/07-mtcine-internetworking.md) — BGP (v7), MPLS, VPLS.
8. [Security, Switching, and IPv6 (MTCSE, MTCSWE, MTCIPv6E)](chapters/08-mtcse-switching-and-ipv6.md) — hardening/IPsec, VLANs, IPv6.
9. [Automation, Currency, and Career Paths](chapters/09-automation-currency-and-career.md) — REST API, scripting, Ansible, recert.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for MikroTik, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The full catalog with the
certificates, prerequisites, and delivery model is in the
[MikroTik certification appendix](../volume-997-master-appendices/chapters/34-appendix-mikrotik-certifications-and-course-access.md)
(Master Appendices, Volume CMXCVII). Related practice lives in the Cisco (XXV, XXIX), Juniper (XXXI),
Nokia (LXVII), NetBox (LII), and Python for Network Engineers (LVIII) volumes.

## Lab coverage

The credential chapters go **per topic**: there is **one walkthrough lab for every certificate
domain** — **36 labs** in all. Because RouterOS is a hands-on platform, the walkthroughs use real
tooling — the **RouterOS CLI**, the **REST API**, **RouterOS scripting**, and the full feature set
(firewall/NAT/queues, OSPF/BGP/MPLS, wireless/CAPsMAN, PPP/hotspot/RADIUS, VLANs, IPsec, IPv6) —
runnable free on **CHR (Cloud Hosted Router)** in GNS3/EVE-NG. Each lab states an objective,
commands, expected results, a negative test, and cleanup, and ends with a
**`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **mikrotik.com/training** (the program) and **RouterOS** (v6 and **v7**) on
RouterBOARD/CHR/x86, with the CLI, WinBox/WebFig, the REST API, RouterOS scripting, and Ansible
`community.routeros` for automation. The program was verified against mikrotik.com on 28 July 2026;
MikroTik adds certificates and RouterOS v7 changed routing syntax, so confirm the current
certificates and version before scheduling.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-68-mikrotik-certifications
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
