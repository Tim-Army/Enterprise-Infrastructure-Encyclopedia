# Volume CXVII — Cisco ACI Build-It-Yourself Lab

> A build-it-yourself microsegmentation lab modeled on **Cisco ACI (Application Centric Infrastructure)** —
> the Nexus 9000 spine-leaf fabric run by the **APIC**, whose model is **application-centric and whitelist
> by default**: endpoints live in **Endpoint Groups (EPGs)**, and traffic between two EPGs is **denied
> unless a contract permits it**. The lab places a four-tier estate in EPGs, applies **contracts** (with
> port filters, provided and consumed) so only `Web→DB:5432` and `Mgmt→OT:502` pass, then adds two finer
> controls ACI is known for: **uSeg micro-EPGs** that reclassify a compromised endpoint into a deny-all
> quarantine by *attribute*, and **intra-EPG isolation** that denies traffic even between members of the
> same EPG. Because ACI needs Nexus hardware and an APIC (the simulator models only the control plane),
> this volume is **two-track**: Track 1 describes APIC configuration at design level; **Track 2 is a fully
> buildable EPG/contract model** in nftables (EPGs as groups, contracts as filtered allows, whitelist
> default, uSeg override, intra-EPG isolation). Nine chapters, ~24 walkthrough labs; opens the
> hardware-fabric tier.

## Overview

Volume CXVII is a **hands-on lab volume** and the first of the hardware-fabric/DPU tier. Its defining idea
is the **application-centric whitelist**: policy is written between application groups (EPGs), the default
between groups is deny, and a contract is an explicit, port-scoped exception. It contrasts with the
tag-based fabric of [Volume CVII (TrustSec)](../volume-107-cisco-ise-trustsec-lab/README.md) — both are
Cisco fabrics, but ACI's grammar is EPG + contract (application-centric) where TrustSec's is SGT + SGACL
(identity-tag).

The lab makes the whole model concrete and adds the two finer controls that make ACI genuine
micro-segmentation rather than just zone firewalling: attribute-based uSeg quarantine and intra-EPG
isolation. It also draws the honest boundary: ACI enforces on the fabric, so off-fabric endpoints and L7
control need service graphs or complementary host/cloud controls.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Lab Preparation](chapters/02-lab-preparation.md) | 2.1–2.3 |
| 03 | [The Flat Network and Lateral Movement](chapters/03-flat-network-and-lateral-movement.md) | 3.1–3.3 |
| 04 | [Contracts — the Application-Centric Whitelist](chapters/04-contracts-whitelist.md) | 4.1–4.2 |
| 05 | [uSeg Micro-EPGs](chapters/05-useg-micro-epgs.md) | 5.1–5.2 |
| 06 | [Intra-EPG Isolation](chapters/06-intra-epg-isolation.md) | 6.1–6.2 |
| 07 | [Enforcement and Verification](chapters/07-enforcement-and-verification.md) | 7.1–7.3 |
| 08 | [Multi-Site, Scale, and the Boundary](chapters/08-multi-site-scale-and-boundary.md) | 8.1–8.3 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

## What you will be able to do

- Place endpoints in EPGs and apply the whitelist default between groups.
- Author contracts with port filters, provided and consumed, for the sanctioned flows.
- Reclassify a compromised endpoint into a deny-all uSeg micro-EPG by attribute.
- Enforce intra-EPG isolation so peers in a group cannot talk.
- Verify the whitelist, read denies, and state the on-fabric boundary.

## Prerequisites

- **Track 1:** an APIC + Nexus 9000 fabric, or the ACI Simulator (control-plane) — commercial; covered at design level.
- **Track 2:** one Ubuntu 22.04 host with `nftables` and `iproute2` (fully buildable, no Cisco software).

## See also

- [Volume CVII — Cisco ISE and TrustSec](../volume-107-cisco-ise-trustsec-lab/README.md) — the tag-based Cisco fabric model to contrast with EPG/contract.
- [Volume C — Cisco Secure Workload](../volume-100-cisco-secure-workload-lab/README.md) — agent-based segmentation that integrates with ACI.
- [Volume XXVII — Cisco Data Center](../volume-027-cisco-data-center/README.md) — broader Nexus/ACI coverage.
- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab pairs with.
