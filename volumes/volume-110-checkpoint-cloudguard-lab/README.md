# Volume CX — Check Point CloudGuard Build-It-Yourself Lab

> A build-it-yourself microsegmentation lab on **Check Point CloudGuard**, built around Check Point's
> **management/gateway split**: you define objects and a single ordered **access rulebase** on a
> management server (SmartConsole / the `mgmt_cli` API) and **install policy** to a **Security Gateway**
> that enforces it east-west. The lab segments a four-tier estate (web/db/hmi/plc), proves an any-any
> accept lets the operator reach the database, then contains it with least-privilege rules above an
> explicit **Cleanup rule** drop — and then converts the policy to **CloudGuard tag-based dynamic /
> data-center objects** so it *follows the workloads*: re-tagging a host changes its access with no rule
> edit. Because Check Point is commercial, this volume is **two-track**: Track 1 on a real **Management +
> Security Gateway** evaluation, Track 2 a native **Linux/nftables** model of objects, an ordered
> rulebase, and tag-updated sets. Nine chapters, ~26 walkthrough labs.

## Overview

Volume CX is a **hands-on lab volume** and the fourth of the fabric/firewall tier, alongside Cisco
TrustSec ([CVII](../volume-107-cisco-ise-trustsec-lab/README.md)), Juniper Connected Security
([CVIII](../volume-108-juniper-connected-security-lab/README.md)), and Fortinet ISFW/VDOM
([CIX](../volume-109-fortinet-isfw-vdom-lab/README.md)). It is the fourth distinct network-enforcement
model in the series.

Its distinguishing ideas are the **management/gateway separation with an explicit install step** — nothing
enforces until you install policy, and the classic mistake is publishing without installing — and
**CloudGuard data-center/dynamic objects**, whose membership is imported from cloud/vCenter/Kubernetes
**tags** so a rule written against `role=db` tracks the estate automatically. The lab builds a static
rulebase, converts it to tag-based objects, proves policy follows a re-tagged workload, and reaches the
honest boundary: a gateway only sees what transits it, so intra-segment and bypassed traffic still need
segment design or host controls.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Lab Preparation](chapters/02-lab-preparation.md) | 2.1–2.4 |
| 03 | [Objects and Policy Install](chapters/03-objects-and-policy-install.md) | 3.1–3.2 |
| 04 | [The Flat Network and Lateral Movement](chapters/04-flat-network-and-lateral-movement.md) | 4.1–4.3 |
| 05 | [The Segmentation Rulebase](chapters/05-segmentation-rulebase.md) | 5.1–5.2 |
| 06 | [CloudGuard Dynamic Objects](chapters/06-cloudguard-dynamic-objects.md) | 6.1–6.2 |
| 07 | [Enforcement and Verification](chapters/07-enforcement-and-verification.md) | 7.1–7.3 |
| 08 | [Identity Awareness, Scale, and the Boundary](chapters/08-identity-awareness-and-boundary.md) | 8.1–8.3 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

## What you will be able to do

- Establish SIC trust and install policy from management to a gateway.
- Author an ordered access rulebase with an explicit Cleanup drop.
- Convert static objects to tag-based dynamic/data-center objects so policy follows workloads.
- Prove a re-tagged host changes access with no rule edit.
- Read connections, rule hits, and logs; add Identity Awareness; identify the boundary.

## Prerequisites

- **Track 1:** a Check Point **Management + Security Gateway** evaluation (R81.x, KVM/ESXi) and four endpoint VMs.
- **Track 2:** one Ubuntu 22.04 host with `nftables` and `iproute2` (no Check Point software required).

## See also

- [Volume CVII — Cisco ISE and TrustSec](../volume-107-cisco-ise-trustsec-lab/README.md), [Volume CVIII — Juniper Connected Security](../volume-108-juniper-connected-security-lab/README.md), and [Volume CIX — Fortinet ISFW and VDOM](../volume-109-fortinet-isfw-vdom-lab/README.md) — the other fabric/firewall models to contrast.
- [Volume LXXIII — Check Point Certification Tracks](../volume-073-check-point-certifications/README.md) — broader Check Point coverage.
- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab pairs with.
