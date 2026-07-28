# Volume LXX — Trellix Certification Tracks

> The whole Trellix (McAfee Enterprise + FireEye) certification program in one volume — the
> per-product specialist tracks across ePO, Endpoint Security, EDR, Network Security, DLP, and
> Helix/XDR, tied together by the Data Exchange Layer — with hands-on, defensive administration and
> OpenDXL labs, verified against trellix.com.

## Overview

Volume LXX maps the **Trellix** certification program — the credentials for administering,
detecting, and responding with Trellix's endpoint, network, data, and SecOps platform. Trellix was
formed in 2022 from **McAfee Enterprise + FireEye**, and its Education Services program follows a
**per-product Certified Product Specialist** model. It joins the encyclopedia's security volumes
(CrowdStrike L, Palo Alto XVI/LXV, Cisco Security XXV, Fortinet XIX, Zscaler XXXV, Forescout XV).

This is a **certification-tracks** volume, like the other vendor volumes (XXXIX–LXIX): it maps the
program — the products and their certifications — and teaches each with a hands-on walkthrough.
Every product and credential was **verified against trellix.com on 28 July 2026**, with the
McAfee → Trellix rebrand and legacy exam-code transition noted throughout.

Chapters follow the platform:

- **Chapter 01** frames the program — the lineage, Education Services, and the DXL fabric.
- **Chapter 02** takes **ePolicy Orchestrator (ePO)** — the central management console.
- **Chapters 03–04** take **Endpoint Security (ENS)** and **EDR**.
- **Chapter 05** takes **Network Security (IPS)** and **Advanced Threat Defense**.
- **Chapter 06** takes **Data Loss Prevention (DLP)**.
- **Chapter 07** takes **Helix, XDR, and SecOps**.
- **Chapter 08** covers **OpenDXL and automation**.
- **Chapter 09** covers keeping current and career paths.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on labs and
knowledge checks.

> **Scope.** Trellix's EDR, network security, and DLP are defensive platforms. Every lab is
> **authorized administration, detection, hunting, response, or automation** — never an
> operational attack technique.

## Chapters

1. [The Trellix Certification Program](chapters/01-the-trellix-certification-program.md) — lineage, Education Services, DXL.
2. [ePolicy Orchestrator (ePO)](chapters/02-epolicy-orchestrator.md) — System Tree, tags, policies, API.
3. [Endpoint Security (ENS)](chapters/03-endpoint-security-ens.md) — Threat Prevention, Firewall, Web Control, ATP.
4. [Endpoint Detection and Response (EDR)](chapters/04-endpoint-detection-and-response.md) — hunting, investigation, reactions.
5. [Network Security (IPS) and Advanced Threat Defense](chapters/05-network-security-and-atd.md) — signatures, sandboxing.
6. [Data Loss Prevention (DLP)](chapters/06-data-loss-prevention.md) — classification, rules, incidents.
7. [Helix, XDR, and SecOps](chapters/07-helix-xdr-and-secops.md) — SIEM, correlation, playbooks.
8. [OpenDXL and Automation](chapters/08-opendxl-and-automation.md) — the DXL fabric and Python SDK.
9. [Keeping the Program Current and Career Paths](chapters/09-keeping-current-and-career.md) — the rebrand, recert.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for Trellix, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The full catalog with the products,
certifications, and lineage is in the
[Trellix certification appendix](../volume-97-master-appendices/chapters/36-appendix-trellix-certifications-and-course-access.md)
(Master Appendices, Volume XCVII). Related practice lives in the CrowdStrike (L), Palo Alto (XVI,
LXV), Cisco Security (XXV), and Enterprise Cybersecurity (X) volumes.

## Lab coverage

The credential chapters go **per topic**: there is **one walkthrough lab for every product domain**
— **34 labs** in all. Because Trellix is a defensive-security platform, the walkthroughs are
**authorized administration, detection, and response** — ePO/EDR/Helix policy and API patterns,
ENS/DLP configuration, detection and hunting queries, and the **OpenDXL** Python SDK (genuine
open-source code) — practiced on authorized lab instances. Each lab states an objective, commands,
expected results, a negative test, and cleanup, and ends with a **`**Lab verified by:** *pending*`**
sign-off.

## Software and platform baseline

This volume references **trellix.com** (the program and Education Services), the Trellix platform
(**ePO, ENS, EDR, Network Security/ATD, DLP, Helix**), and the **Data Exchange Layer (DXL)** with the
open-source **OpenDXL** Python SDK for automation. The program was verified against trellix.com on
28 July 2026; because of the McAfee → Trellix rebrand, confirm the current course names and exam
codes before scheduling.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-70-trellix-certifications
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
