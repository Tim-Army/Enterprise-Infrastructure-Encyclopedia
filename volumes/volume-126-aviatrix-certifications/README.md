# Volume CXXVI — Aviatrix Certification Tracks

> The certification map for **Aviatrix** — the multicloud network overlay — verified on aviatrix.ai,
> 3 August 2026. The **Aviatrix Certified Engineer (ACE)** program runs a free, self-paced **ACE
> Associate** (multicloud networking foundations across **AWS, Azure, Google Cloud, and OCI** — the
> mandatory gateway credential) into the instructor-led, hands-on **ACE Professional** (multicloud
> transit + HA, egress security, firewall insertion, and secure user/site connectivity) and the **ACE
> Design Expert** capstone (scalable, resilient multicloud design), alongside focused **ACE** courses —
> **Security**, **Hybrid Cloud**, **Cloud Backbone**, **Automation** (Terraform), and **Operations**
> (CoPilot). The volume teaches the Aviatrix architecture the exams assume — **Controller** (control
> plane), **CoPilot** (observability), and **gateways** forming transit/spoke, with **FireNet** (NGFW
> insertion) and **Distributed Cloud Firewall** (distributed segmentation) — and drills each exam
> objective with a walkthrough lab. Because the ACE Associate needs **no cloud accounts**, the labs
> model transit, egress, firewall insertion, and VPN with **free Linux primitives** (namespaces,
> nftables, FRR, WireGuard) and real **Terraform** syntax, plus design-level console steps where the
> platform is required — every lab runs at no cost.

## Overview

Volume CXXVI is a **certification-tracks volume** for a platform, not an exam-code catalog: Aviatrix's
credentials are course-and-exam (the Associate is free and gateless; Professional is instructor-led).
The volume mirrors the exam objectives — the Associate's two pillars (cloud-native networking, then the
Aviatrix overlay) and the Professional's four (transit/HA, egress, firewall insertion, connectivity) —
each as a runnable walkthrough on free primitives. It sits alongside the cloud-provider volumes (AWS,
Azure, Google Cloud) as the **multicloud networking** layer above them, and connects to the
microsegmentation landscape ([Volume LXXXVII](../volume-087-microsegmentation-options/README.md)) through
Distributed Cloud Firewall.

Its standing disciplines are honest track/design synthesis and currency: the ACE catalog and the
Distributed Cloud Firewall model move, and the native clouds shift what the overlay abstracts, so the
volume flags re-verification on aviatrix.ai.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The Aviatrix Certified Engineer (ACE) Program](chapters/01-the-ace-program.md) | 1.1–1.2 |
| 02 | [ACE Associate — Cloud-Native Networking Foundations](chapters/02-associate-cloud-native-networking.md) | 2.1–2.4 |
| 03 | [ACE Associate — Aviatrix Architecture and Design Patterns](chapters/03-associate-aviatrix-architecture.md) | 3.1–3.4 |
| 04 | [ACE Professional — Multicloud Transit and High Availability](chapters/04-professional-multicloud-transit.md) | 4.1–4.4 |
| 05 | [ACE Professional — Egress Security and FQDN Filtering](chapters/05-professional-egress-security.md) | 5.1–5.4 |
| 06 | [ACE Professional — Firewall Insertion (FireNet) and DCF](chapters/06-professional-firewall-insertion.md) | 6.1–6.3 |
| 07 | [ACE Professional — Secure User and Site Connectivity](chapters/07-professional-user-and-site-connectivity.md) | 7.1–7.4 |
| 08 | [ACE Automation and Operations](chapters/08-professional-automation-and-operations.md) | 8.1–8.4 |
| 09 | [ACE Design Expert, Choosing a Path, and Currency](chapters/09-design-expert-choosing-currency-career.md) | 9.1–9.2 |

## What you will be able to do

- Map the ACE program (Associate → Professional → Design Expert + focused courses) and its prerequisites.
- Explain multicloud networking across AWS/Azure/GCP/OCI and the native constraints Aviatrix solves.
- Build and reason about multicloud transit, active-active HA, egress FQDN filtering, FireNet, DCF, and VPN.
- Manage the overlay as Terraform and observe it with CoPilot (FlowIQ, compliance).
- Synthesize a scalable, resilient multicloud design and keep the plan current.

## Prerequisites

- Cloud fundamentals for at least one provider; for the Professional path, ~1 year of cloud experience (Aviatrix's stated prerequisite).
- A Linux host with `iproute2`, `nftables`, `frr`, `wireguard-tools`, and `terraform` for the free labs.

## See also

- [Volume XVII — AWS Architecture and Security](../volume-017-aws-architecture-security/README.md), [Volume XXXIII — Microsoft Azure](../volume-033-microsoft-azure-certifications/README.md), [Volume XXXIV — Google Cloud](../volume-034-google-cloud-certifications/README.md) — the cloud-provider networking Aviatrix overlays.
- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the segmentation landscape Distributed Cloud Firewall sits within.
- [Master Appendices — Aviatrix appendix](../volume-997-master-appendices/chapters/60-appendix-aviatrix-certifications-and-course-access.md) — the ACE catalog, the free Associate, and course access.
