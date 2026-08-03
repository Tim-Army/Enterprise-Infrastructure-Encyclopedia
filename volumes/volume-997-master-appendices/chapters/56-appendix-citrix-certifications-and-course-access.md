# Chapter 56: Appendix — Citrix Certifications and Course Access

The **Citrix** certification program under **Cloud Software Group** — the exams, their modules, and the
training model — organized for course access. The program was verified on **3 August 2026** from
**citrix.com/training-and-certifications**, **netscaler.com** (training page), the **Webassessor**
(Kryterion) platform landing, and the five official **exam prep guides** (updated 15 September 2025) —
the same sources that anchor
[Volume CXXII — Citrix Certification Tracks](../../volume-122-citrix-certifications/README.md).
Third-party exam-dump sites were excluded as sources.

**How access works.** Exams are delivered on **Webassessor** (webassessor.com/citrix); holders of legacy
certifications recover their records there with their certification email plus a password reset, and
badges live on **Credly**. Instructor-led courses run through **Authorized Training Providers** (for
example Layer 8 Training); **on-demand eLearning is hosted on Pluralsight** under the Citrix/NetScaler
partnership — included at no additional cost for customers with an active Citrix or NetScaler
subscription (the CVAD Academy and NetScaler Administrator Academy paths). Hands-on practice for the
NetScaler exams is free with **NetScaler CPX Express**.

> **Currency.** The program is under an **announced comprehensive overhaul** ("additional certifications
> are being planned"), the **Expert tier (CCE-V, CCE-N) is discontinued**, and **1Y0-204 is retired**
> (the CCA-V exam replaced it). Re-verify the certification list on citrix.com and Webassessor before
> registering — mid-overhaul programs change with little notice.

## Free and low-cost resources and entry points

- **[Citrix training and certifications](https://www.citrix.com/training-and-certifications/)** — the
  authoritative program page
- **[NetScaler training and certification](https://www.netscaler.com/resources/training-certification)**
  — the NetScaler-side program page and course list
- **[Webassessor (Citrix)](https://www.webassessor.com/citrix)** — exam registration, catalog, and
  credential recovery
- **Official exam prep guides (PDF)** — the public module lists for all five exams:
  [CCA-V](https://www.citrix.com/content/dam/citrix61/en_us/documents/exam-prep-guides/citrix-certified-associate-virtualization-cca-v-exam-prep-guide.pdf) ·
  [CCP-V](https://www.citrix.com/content/dam/citrix61/en_us/documents/exam-prep-guides/citrix-certified-professional-virtualization-ccp-v-exam-prep-guide_updated.pdf) ·
  [CCA-AppDS-Gateway](https://www.citrix.com/content/dam/citrix61/en_us/documents/exam-prep-guides/citrix-certified-associate-app-delivery-and-security-cca-appds-gateway-exam-prep-guide.pdf) ·
  [CCA-AppDS-Traffic Management](https://www.citrix.com/content/dam/citrix61/en_us/documents/exam-prep-guides/citrix-certified-associate-app-delivery-and-security-cca-appds-traffic-management-exam-prep-guide.pdf) ·
  [CCP-AppDS](https://www.citrix.com/content/dam/citrix61/en_us/documents/exam-prep-guides/citrix-certified-professional-appds-exam-prep-guide.pdf)
- **NetScaler CPX Express** — free containerized NetScaler for CLI practice
- **Pluralsight academies** — CVAD Academy and NetScaler Administrator Academy (included with an active
  subscription)

## Fees, delivery, and renewal

- **Fees:** exam pricing is published in the **Webassessor catalog at registration** (sign-in required);
  confirm there before budgeting. CPX Express practice is **free**; Pluralsight eLearning is included
  with an active product subscription.
- **Delivery:** Webassessor (Kryterion), proctored. CCA-V ~60–65 questions / 90 minutes / ~65% pass /
  English. CCP-V 60–70 questions / 64% pass. AppDS exams 60–70 questions per form, **~10%
  performance-based items**, English + Japanese; the Traffic Management exam may include **CLI
  simulations**.
- **Prerequisites:** none for the associate exams; CCP-V requires CCA-V; CCP-AppDS requires either
  CCA-AppDS exam.
- **Validity and renewal:** re-verify the current recertification policy on the official pages — the
  overhaul makes the historical three-year term unsafe to assume.

## The certifications

Verified against the sources above on 3 August 2026.

| Credential | Exam and modules |
| --- | --- |
| CCA-V | *Citrix Virtual Apps and Desktops Administration* (replaces 1Y0-204); course CVAD-201 (2402 LTSR); 9 modules: deploying, providing resources, providing access, security, monitoring, troubleshooting, printing, PowerShell, Citrix Cloud |
| CCP-V | *Citrix Virtual Apps and Desktops 7 Advanced Administration*; prereq CCA-V; course CVAD-301 (2402 LTSR); 7 modules: advanced administration, advanced user access, policies/profiles, WEM, security, troubleshooting, cloud concepts |
| CCA-AppDS (Gateway option) | *NetScaler 14.x Essentials and NetScaler Gateway*; courses CNS-225 / NS-232; 11 modules: networking, HA, load balancing, SSL offload, Gateway, authentication/authorization, end-user access, troubleshooting, CVAD integration, AppExpert/rewrite/responder, content switching |
| CCA-AppDS (Traffic Management option) | *Deploy and Manage Citrix ADC 14.x with Traffic Management*; course NS-201 (formerly CNS-225); 12 modules: getting started, networking, platforms (MPX/VPX/CPX/BLX/SDX), HA, load balancing, SSL offload, securing the ADC, troubleshooting, rewrite/responder/URL transform, content switching, optimization, GSLB |
| CCP-AppDS | **1Y0-342** *NetScaler Advanced Topics — Security, Management and Optimization*; prereq either CCA-AppDS; course NS-301; 12 modules: WAF intro, WAF profiles/policies, protections, advanced security (bot/API), security and filtering, AAA/nFactor intro, nFactor use cases, AAA customization, NetScaler Console intro, Console management/monitoring, apps/configs via Console (Stylebooks), tuning/optimization |

## Notes

- **The two CCA-AppDS exams grant the same credential**; either satisfies the CCP-AppDS prerequisite.
  Choose Gateway if you front CVAD with remote access, Traffic Management if you run the ADC estate.
- **Course renumbering:** NS-201 is the current name of the course formerly labeled CNS-225; older
  CNS-22x/CNS-320 course codes still appear on partner sites.
- **The Expert tier is gone.** If the overhaul reintroduces one, expect it to build on the current
  Professional certifications.
