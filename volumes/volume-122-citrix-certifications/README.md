# Volume CXXII — Citrix Certification Tracks

> The certification map for **Citrix** under **Cloud Software Group**: two tracks, five exams, and an
> explicitly announced program overhaul. The **Virtualization** track runs **CCA-V** (*Citrix Virtual
> Apps and Desktops Administration*, the replacement for the retired 1Y0-204) to **CCP-V** (*Advanced
> Administration*, prerequisite CCA-V). The **App Delivery and Security** track runs **CCA-AppDS** —
> one credential, two exam options: *NetScaler 14.x Essentials and NetScaler Gateway* or *Deploy and
> Manage Citrix ADC 14.x with Traffic Management* — to **CCP-AppDS** (**1Y0-342**, *NetScaler Advanced
> Topics: Security, Management and Optimization*, the last exam with a legacy code). The **Expert tier
> (CCE-V, CCE-N) is discontinued**, exams are delivered on **Webassessor** (Kryterion), AppDS forms
> carry **~10% performance-based items** (the TM exam adds CLI simulations), and the official prep
> guides (updated 15 Sep 2025) declare the module lists this volume's **per-module walkthrough labs**
> follow — 51 modules across the five exams, drilled at the CVAD PowerShell SDK and the NetScaler CLI
> (free against **CPX Express**). Program facts verified on citrix.com, netscaler.com, and Webassessor,
> 3 August 2026.

## Overview

Volume CXXII is a **certification-tracks volume**. It maps the current Citrix program — smaller and
flatter than its 1Y0-era ancestor, and mid-overhaul with "additional certifications planned" — onto
nine chapters with a walkthrough lab per exam module. The CVAD chapters run the broker PowerShell
(`Get-Broker*`) the way exam scenarios read; the NetScaler chapters drill the `add/set/bind/show` CLI
shapes the performance-based items and simulations present, all runnable free on CPX Express.

The volume's standing warning is the overhaul itself: verification-before-scheduling is built into the
study plans, with a one-command currency check against the official page.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The Citrix Certification Program](chapters/01-the-citrix-certification-program.md) | 1.1–1.2 |
| 02 | [CCA-V — Deploying and Delivering Virtual Apps and Desktops](chapters/02-cca-v-deploying-and-delivering.md) | 2.1–2.3 |
| 03 | [CCA-V — Security, Monitoring, and Operations](chapters/03-cca-v-security-monitoring-operations.md) | 3.1–3.6 |
| 04 | [CCP-V — Advanced Administration](chapters/04-ccp-v-advanced-administration.md) | 4.1–4.7 |
| 05 | [CCA-AppDS — NetScaler Platform, Networking, and Load Balancing](chapters/05-appds-netscaler-platform-and-load-balancing.md) | 5.1–5.6 |
| 06 | [CCA-AppDS-Gateway — Secure Remote Access](chapters/06-cca-appds-gateway-secure-remote-access.md) | 6.1–6.7 |
| 07 | [CCA-AppDS-Traffic Management — ADC Administration](chapters/07-cca-appds-traffic-management.md) | 7.1–7.6 |
| 08 | [CCP-AppDS — Web App Firewall, nFactor, and NetScaler Console](chapters/08-ccp-appds-waf-nfactor-console.md) | 8.1–8.8 |
| 09 | [Choosing Your Track, Currency, and Career](chapters/09-choosing-currency-and-career.md) | 9.1–9.2 |

## What you will be able to do

- Name the current program precisely: five exams, two tracks, no Expert tier, and what was retired.
- Administer a CVAD site the way CCA-V/CCP-V scenarios expect, from the broker PowerShell up.
- Build NetScaler load balancing, Gateway ICA proxy, content switching, GSLB, WAF, and nFactor at the CLI.
- Read NetScaler Console as the fleet pane: dashboards, events, Stylebooks, configuration audit.
- Keep a certification plan current through the announced program overhaul.

## Prerequisites

- Networking and Windows administration fundamentals ([Volume II](../volume-002-network-engineering-foundations/README.md), [Volume IV](../volume-004-enterprise-systems-administration/README.md)).
- A lab: CVAD trial/eval for the Virtualization chapters; **NetScaler CPX Express** (free) or a lab VPX for the AppDS chapters.

## See also

- [Volume V — VMware Virtualization](../volume-005-vmware-virtualization/README.md) — the other EUC/virtualization stack and its certification ladder.
- [Volume LXVI — F5 Certification Tracks](../volume-066-f5-certifications/README.md) — the neighboring ADC vendor's program.
- [Master Appendices — Citrix appendix](../volume-997-master-appendices/chapters/56-appendix-citrix-certifications-and-course-access.md) — courses, access, and fees.
