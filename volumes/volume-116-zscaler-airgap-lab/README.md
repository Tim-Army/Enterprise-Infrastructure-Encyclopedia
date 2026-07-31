# Volume CXVI — Zscaler/Airgap Build-It-Yourself Lab

> A build-it-yourself microsegmentation lab modeled on **Airgap Networks** (acquired by **Zscaler**), whose
> approach is unlike any earlier volume: it segments **agentlessly and without changing VLANs** by taking
> control of the **network layer** — controlling **ARP/DHCP** so every device becomes its own microsegment,
> a **network of one**, with no direct Layer 2 path to any other device even on the same subnet. All
> east-west traffic is forced through an enforcement point that denies by default, so ransomware has no
> lateral path — and a single **kill switch** severs all east-west instantly during an incident. Zscaler
> pairs this with the **Zero Trust Exchange** for identity-based north-south access (ZTNA). The lab builds a
> flat VLAN, simulates a worm spreading across it, collapses every device into a network of one **without
> changing any IP**, re-permits only the single sanctioned flow, and exercises the kill switch. Because
> Zscaler/Airgap is commercial, this volume is **two-track**: Track 1 describes the product; **Track 2 is a
> fully buildable agentless-isolation model** in `iproute2` + nftables. Nine chapters, ~22 walkthrough labs.

## Overview

Volume CXVI is a **hands-on lab volume** and the fifth and final volume of the OT-security tier. Its
distinctive idea is **agentless isolation as the default**: no software on the endpoints and no
re-subnetting — the control lives at the network layer and makes every device an island, granting
connectivity only by exception. That directly targets ransomware and worm propagation, the lateral
movement a flat VLAN invites.

The lab makes the whole model concrete — a worm reaching every peer on a flat VLAN, then every device
collapsed to a network of one so the same worm reaches nothing, then a single sanctioned flow re-permitted
and a kill switch that severs everything on demand. It also draws the honest boundary: network-of-one stops
the *reach* but does not inspect payloads or lock down hosts, so it pairs with the protocol inspection and
endpoint controls of the earlier OT-security volumes and with the Zero Trust Exchange for access.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Lab Preparation](chapters/02-lab-preparation.md) | 2.1–2.3 |
| 03 | [Lateral Spread on the Flat VLAN](chapters/03-lateral-spread.md) | 3.1–3.2 |
| 04 | [Network of One](chapters/04-network-of-one.md) | 4.1–4.2 |
| 05 | [Zero-Trust East-West Policy](chapters/05-zero-trust-policy.md) | 5.1–5.2 |
| 06 | [The Ransomware Kill Switch](chapters/06-ransomware-kill-switch.md) | 6.1–6.2 |
| 07 | [Enforcement and Verification](chapters/07-enforcement-and-verification.md) | 7.1–7.3 |
| 08 | [Zero Trust Exchange, Scale, and the Boundary](chapters/08-zero-trust-exchange-and-boundary.md) | 8.1–8.3 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

## What you will be able to do

- Simulate lateral/worm spread across a flat VLAN.
- Collapse every device into a network of one without changing any IP or VLAN.
- Enforce isolate-by-default east-west policy and re-permit only sanctioned flows.
- Throw and disengage a ransomware kill switch.
- Explain the north-south ZTNA pairing and the reach-vs-payload boundary.

## Prerequisites

- **Track 1:** Zscaler/Airgap (commercial; covered at design level).
- **Track 2:** one Ubuntu 22.04 host with `nftables` and `iproute2` (fully buildable, no Zscaler software).

## See also

- [Volume XXXV — Zscaler Zero Trust Exchange](../volume-035-zscaler-zero-trust-exchange/README.md) — the north-south ZTNA platform this pairs with.
- [Volume CXV — TXOne Networks](../volume-115-txone-networks-lab/README.md), [Volume CXIV — Nozomi Networks](../volume-114-nozomi-networks-lab/README.md), and [Volume CXII — Xage Security](../volume-112-xage-security-lab/README.md) — the other OT-security models.
- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab pairs with.
