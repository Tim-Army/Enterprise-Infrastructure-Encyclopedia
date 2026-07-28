# Volume LXVI — F5 Certification Tracks

> The whole F5 certification ladder in one volume — the BIG-IP Administrator (rebuilt in 2025
> into five focused exams), the Technology Specialist specializations (LTM, DNS, Advanced WAF,
> APM), and the Security Solution Expert — on BIG-IP/TMOS, with hands-on tmsh, iControl REST,
> AS3, and iRules labs, verified against education.f5.com.

## Overview

Volume LXVI maps the **F5** certification program — the credentials for deploying, securing, and
automating **BIG-IP**, F5's application delivery and security platform running **TMOS**. It joins
the encyclopedia's networking and security volumes (Cisco XXV, Palo Alto XVI/LXV, Zscaler XXXV)
and the automation volumes (NetBox LII, Python for Network Engineers LVIII, Ansible LIX) that its
Automation Toolchain content builds on.

This is a **certification-tracks** volume, like the other vendor volumes (XXXIX–LXV): it maps the
program — the levels, specializations, and exams — and teaches each with a hands-on walkthrough.
F5 **rebuilt the Administrator credential in 2025** into five focused exams (F5CAB1–F5CAB5),
retiring the legacy 101/201 path; every credential was **verified against education.f5.com and
clouddocs.f5.com on 28 July 2026**.

Chapters follow the ladder:

- **Chapter 01** frames the program — the levels, the 2025 restructure, and the platform.
- **Chapters 02–04** take the **Administrator (F5-CA)** exams (TMOS/data-plane concepts; data-plane
  configuration; control plane and troubleshooting).
- **Chapters 05–08** take the **Technology Specialist** specializations (LTM; DNS; Advanced WAF/ASM;
  APM) and the **Solution Expert**.
- **Chapter 09** covers automation, currency, and career paths.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on labs and
knowledge checks.

> **Scope.** The Advanced WAF (ASM) and APM modules are security controls. Every lab is
> **authorized administration, policy, and defense** — never an operational attack technique.

## Chapters

1. [The F5 Certification Program](chapters/01-the-f5-certification-program.md) — levels, the 2025 restructure, platform.
2. [Administrator — TMOS and Data Plane Concepts](chapters/02-administrator-tmos-and-data-plane-concepts.md) — F5CAB1/F5CAB2.
3. [Administrator — Data Plane Configuration](chapters/03-administrator-data-plane-configuration.md) — F5CAB3: virtual servers, pools, profiles.
4. [Administrator — Control Plane and Troubleshooting](chapters/04-administrator-control-plane-and-troubleshooting.md) — F5CAB4/F5CAB5: HA, backups, qkview.
5. [Technology Specialist — LTM](chapters/05-cts-ltm.md) — 301a/301b: load balancing, persistence, iRules.
6. [Technology Specialist — DNS](chapters/06-cts-dns.md) — 302: BIG-IP DNS/GTM, wide IPs, GSLB.
7. [Technology Specialist — Advanced WAF (ASM)](chapters/07-cts-advanced-waf-asm.md) — 303: WAF policy, signatures, bot defense.
8. [Technology Specialist — APM and Solution Expert](chapters/08-cts-apm-and-solution-expert.md) — 304 access; 401 integrated security.
9. [Automation, Currency, and Career Paths](chapters/09-automation-currency-and-career.md) — AS3/DO/TS, recert, paths.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for F5, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The full catalog with levels,
specializations, and exams is in the
[F5 certification appendix](../volume-97-master-appendices/chapters/32-appendix-f5-certifications-and-course-access.md)
(Master Appendices, Volume XCVII). Related practice lives in the Cisco (XXV), Palo Alto (XVI, LXV),
Zscaler (XXXV), NetBox (LII), Python for Network Engineers (LVIII), and Ansible (LIX) volumes.

## Lab coverage

The credential chapters go **per topic**: there is **one walkthrough lab for every exam domain**
of the ladder — **36 labs** in all. Because BIG-IP is a hands-on platform, the walkthroughs use
real tooling — the **tmsh** CLI, the **iControl REST API**, **AS3** declarations, and **iRules** —
practiced on **BIG-IP Virtual Edition** in an authorized lab. Each lab states an objective,
commands, expected results, a negative test, and cleanup, and ends with a
**`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **education.f5.com**, **my.f5.com**, and **clouddocs.f5.com** (the program
and documentation), **BIG-IP/TMOS** and its modules (LTM, DNS, Advanced WAF/ASM, APM), and the
**F5 Automation Toolchain** (AS3/DO/TS) with iControl REST for automation. The program and its
exams were verified against education.f5.com and clouddocs.f5.com on 28 July 2026; F5 revises the
program (the 2025 Administrator restructure, plus NGINX and Distributed Cloud), so confirm the
current exams before scheduling.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-66-f5-certifications
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
