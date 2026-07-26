# Volume XLIII — Offensive Security (OffSec) Certification Tracks

> The whole OffSec certification program in one volume — the OSCP+ and the
> penetration-testing, web, exploit-development, defensive, and AI red-teaming
> credentials — with hands-on methodology walkthroughs for each course's topic
> areas, verified against offsec.com, taught ethically and paired with defenses.

## Overview

Volume XLIII maps the **OffSec** (Offensive Security) certification program — the
industry's benchmark for **hands-on, practical** security certification. Unlike
knowledge exams, OffSec credentials are earned through **proctored practical
exams plus a professional report**, so this volume sits at the practitioner tier
alongside the encyclopedia's cybersecurity (X) and vendor-security volumes and
the CompTIA PenTest+/Ethical Hacker material (XXXIX).

This is a **certification-tracks** volume, like CompTIA (XXXIX), ISC2 (XL),
CNCF/Kubernetes (XLI), and HashiCorp (XLII). Because OffSec publishes **course
syllabi** rather than weighted domains, its per-topic labs map **one walkthrough
per major syllabus topic area** of each course. Every course, code, and exam
detail was **verified against offsec.com on 26 July 2026**, which matters because
the program changed substantially: **OSCP became OSCP+** (a renewable version
alongside the lifetime OSCP), and OffSec added whole new tracks — **CyberCore
(OSCC)** and the **AI Red Teamer (OSAI, AI-300)**.

**Ethics and authorization.** Every technique in this volume is taught to be
**understood and defended against**, and every lab targets **only your own
system or an authorized lab**. Offensive knowledge is presented with its
defensive counterpart, and authorization is treated as the first control.

Chapters are organized by discipline:

- **Chapter 01** frames the program — practical exams, the report, the OSCE³
  designation, the "+" renewal model, and authorization/ethics.
- **Chapter 02** covers the foundational tier: OSCC (CyberCore) and KLCP (Kali).
- **Chapter 03** covers the flagship OSCP+ (PEN-200).
- **Chapters 04–06** cover the offensive specializations: advanced pentest (OSEP,
  OSWP), web (OSWA, OSWE), and exploit development (OSED, OSEE).
- **Chapter 07** covers the defensive track (OSDA, OSIR, OSTH).
- **Chapter 08** covers AI security (OSAI) and the OSCE³ expert track.
- **Chapter 09** covers keeping current — the "+" renewal, new tracks, and career
  paths.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic
hands-on labs and knowledge checks.

## Chapters

1. [The OffSec Certification Program](chapters/01-the-offsec-certification-program.md) — practical exams and reports, the course-code system, OSCE³, the "+" renewal model, and authorization/ethics.
2. [Foundational — OSCC (CyberCore) and KLCP](chapters/02-foundational-oscc-cybercore-and-klcp.md) — cybersecurity fundamentals (SEC-100/SJD-100) and Kali Linux (PEN-103).
3. [OSCP+ (PEN-200)](chapters/03-oscp-plus-pen-200.md) — the flagship penetration-testing methodology across the kill chain.
4. [Advanced Penetration Testing — OSEP and OSWP](chapters/04-advanced-penetration-testing-osep-and-oswp.md) — evasion and breaching (PEN-300) and wireless (PEN-210).
5. [Web Security — OSWA and OSWE](chapters/05-web-security-oswa-and-oswe.md) — black-box assessment (WEB-200) and white-box code review (WEB-300).
6. [Exploit Development — OSED and OSEE](chapters/06-exploit-development-osed-and-osee.md) — Windows user-mode (EXP-301) and advanced exploitation (EXP-401), as memory-safety engineering.
7. [Defensive Security — OSDA, OSIR, and OSTH](chapters/07-defensive-security-osda-osir-osth.md) — detection (SOC-200), incident response (IR-200), and threat hunting (TH-200).
8. [AI Security (OSAI) and the OSCE³ Expert Track](chapters/08-ai-security-osai-and-the-osce3-expert-track.md) — the new AI Red Teamer (AI-300) and the OSCE³ umbrella.
9. [Keeping the OffSec Program Current and Career Paths](chapters/09-keeping-the-offsec-program-current-and-career-paths.md) — the "+" renewal, new tracks, and career paths.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for OffSec, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The full catalog
with the courses, credentials, practical-exam formats, the "+" renewal model, and
the OffSec training model is in the
[OffSec certification appendix](../volume-97-master-appendices/chapters/17-appendix-offsec-certifications-and-course-access.md)
(Master Appendices, Volume XCVII). Related hands-on security practice lives in
Volume X (Cybersecurity) and the vendor-security volumes (XVI, XIX, XXV, XXXV).

## Lab coverage

The credential chapters go **per topic**: there is **one methodology walkthrough
for every major syllabus topic area** of each OffSec course — roughly **49
topic-area labs** across the program — plus the program and currency labs in
Chapters 01 and 09. Because OffSec publishes course syllabi rather than weighted
domains, each course's labs follow its published topic areas. **Every lab is
educational, authorization-first, and defense-paired:** commands target only the
reader's own host or an authorized lab (`nmap` on localhost, cracking your own
hashes, analyzing your own binaries), and the more sensitive areas (evasion,
exploit development, AI red-teaming) are taught at the level of **concept,
methodology, and mitigation** rather than operational attack. Each lab states an
objective, commands, expected results, a negative test, and cleanup, and ends
with a **`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **offsec.com** (courses and certifications), the **Kali
Linux** distribution, and the **PSI**-style proctored practical-exam model.
Courses, codes, and exam details were verified against offsec.com on 26 July
2026; OffSec updates course codes and adds tracks, so confirm the current course
and status before registering.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-43-offensive-security-certifications
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
