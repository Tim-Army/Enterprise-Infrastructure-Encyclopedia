# Volume CXVIII — Arista MSS-Group Build-It-Yourself Lab

> A build-it-yourself microsegmentation lab modeled on **Arista's Macro-Segmentation Service (MSS)** and
> **MSS-Group**, enforced in **EOS** switches and managed by **CloudVision**. Arista's model applies
> **group-based policy in the switching silicon at line rate**: endpoints are assigned to **security
> groups** and a policy states which group may reach which (with L4 rules), default-deny between groups,
> with no hairpin. The lab shows both flavors: **MSS-Group** (micro-segmentation — group-to-group policy
> directly in the fabric) and **MSS** (macro-segmentation — *redirecting* an inter-group flow through an
> inserted **firewall** for inspection without re-cabling). It places a four-tier estate in groups, permits
> only `SG-Web→SG-DB:5432` and `SG-Mgmt→SG-OT:502`, redirects the web→db flow through a firewall that
> blocks a malicious payload, and denies the operator's lateral path by default. Because MSS-Group's
> enforcement is in hardware, this volume is **two-track**: Track 1 describes EOS/CloudVision; **Track 2 is
> a fully buildable group-policy model** (groups as nftables sets, policy with default-deny, a firewall
> redirect). Nine chapters, ~24 walkthrough labs.

## Overview

Volume CXVIII is a **hands-on lab volume** and the second of the hardware-fabric/DPU tier. Its defining
ideas are **group policy at line rate** and the **micro/macro split**: MSS-Group segments the bulk of
east-west traffic cheaply in the fabric, while MSS macro selectively steers the flows that warrant
inspection through a firewall — keeping the firewall out of the path of most traffic. It sits alongside the
Cisco fabric models (TrustSec's SGT tags in [CVII](../volume-107-cisco-ise-trustsec-lab/README.md), ACI's
EPG/contract in [CXVII](../volume-117-cisco-aci-lab/README.md)) as a third fabric grammar: security groups
plus group policy, with optional firewall redirect.

The lab builds both modes concretely and reaches the honest boundary: MSS enforces on the EOS fabric, so
off-fabric endpoints and deep L7 control need the macro redirect or complementary host controls.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Lab Preparation](chapters/02-lab-preparation.md) | 2.1–2.3 |
| 03 | [Security Groups](chapters/03-security-groups.md) | 3.1–3.2 |
| 04 | [The Flat Network and Lateral Movement](chapters/04-flat-network-and-lateral-movement.md) | 4.1–4.3 |
| 05 | [MSS-Group Micro-Segmentation](chapters/05-mss-group-micro.md) | 5.1–5.2 |
| 06 | [MSS Macro-Segmentation — Firewall Redirect](chapters/06-mss-macro-firewall-redirect.md) | 6.1–6.2 |
| 07 | [Enforcement and Verification](chapters/07-enforcement-and-verification.md) | 7.1–7.3 |
| 08 | [CloudVision, Scale, and the Boundary](chapters/08-cloudvision-scale-and-boundary.md) | 8.1–8.3 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

## What you will be able to do

- Assign endpoints to security groups and write group-to-group policy with default-deny.
- Enforce the whitelist in the fabric and deny lateral movement.
- Redirect a selected inter-group flow through a firewall (MSS macro) and block a malicious payload.
- Read group denies and firewall drops; confirm group-membership-driven policy.
- State the on-fabric boundary and the micro/macro design trade-off.

## Prerequisites

- **Track 1:** Arista EOS (cEOS/vEOS) fabric + CloudVision + a firewall (account/commercial; design level).
- **Track 2:** one Ubuntu 22.04 host with `nftables`, `iproute2`, and `python3` (fully buildable, no Arista software).

## See also

- [Volume CXVII — Cisco ACI](../volume-117-cisco-aci-lab/README.md) and [Volume CVII — Cisco ISE and TrustSec](../volume-107-cisco-ise-trustsec-lab/README.md) — other fabric segmentation grammars to contrast.
- [Volume LXII — Arista Certification Tracks](../volume-062-arista-certifications/README.md) — broader Arista EOS/CloudVision coverage.
- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab pairs with.
