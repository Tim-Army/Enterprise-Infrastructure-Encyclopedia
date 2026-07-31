# Volume CVII — Cisco ISE and TrustSec Build-It-Yourself Lab

> A build-it-yourself microsegmentation lab on **Cisco TrustSec** — the fabric approach where every packet
> carries a **Security Group Tag (SGT)** naming what the sender *is*, and the network enforces a matrix of
> **Security Group ACLs (SGACLs)** keyed on *(source tag → destination tag)* rather than IP. **Cisco ISE**
> is the policy brain; IOS-XE switches are the enforcers. The lab assigns SGTs (WEB/DB/HMI/PLC) via
> IP-SGT mappings, distributes them with **SXP**, proves a permissive matrix lets the operator reach the
> database, then contains it with an egress matrix that is **default-deny** with two exact permits — and
> reads the `show cts role-based counters` drops. Because TrustSec is commercial and hardware-assisted,
> this volume is **two-track**: Track 1 on real **ISE + IOS-XE** (eval VM + Catalyst 9000v/physical), and
> Track 2 a native **Linux/nftables** model that reproduces the SGT binding table and tag-to-tag matrix on
> one host with no Cisco kit. Nine chapters, ~26 walkthrough labs, opening the fabric/firewall tier of the
> microsegmentation series.

## Overview

Volume CVII is a **hands-on lab volume** and the first of the fabric/firewall tier. Where
[Volume LXXXVII (Microsegmentation Options)](../volume-087-microsegmentation-options/README.md)
compares approaches, this volume is the **build** for the network-fabric approach: it stands up TrustSec
end to end and segments a four-tier estate by group tag.

Its distinguishing idea is **enforcement in the network, by group**. Unlike the host-agent products
(Volumes XCIII–C) and the Kubernetes meshes (Volumes CI–CV), TrustSec puts the policy in the switches and
routers: the SGT rides with the packet (or is derived from an SXP binding), and the enforcer applies an
SGACL on egress toward the destination group. The policy — "WEB may reach DB on 5432; HMI may not reach DB
at all" — is written once in ISE, independent of VLANs and IP addressing, and survives any re-addressing.
The lab reaches the honest boundary too: endpoints the fabric cannot tag are `Unknown`, and that group
must be a deliberate decision, paired with host controls where the fabric has no reach.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Lab Preparation](chapters/02-lab-preparation.md) | 2.1–2.4 |
| 03 | [Enabling TrustSec](chapters/03-enabling-trustsec.md) | 3.1–3.3 |
| 04 | [Assigning Security Group Tags](chapters/04-assigning-sgts.md) | 4.1–4.3 |
| 05 | [The Flat Network and Lateral Movement](chapters/05-flat-network-and-lateral-movement.md) | 5.1–5.3 |
| 06 | [Authoring the SGACL Matrix](chapters/06-authoring-the-sgacl-matrix.md) | 6.1–6.2 |
| 07 | [Enforcement and Verification](chapters/07-enforcement-and-verification.md) | 7.1–7.3 |
| 08 | [Inline Tagging, Scale, and the Boundary](chapters/08-inline-tagging-scale-and-boundary.md) | 8.1–8.3 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

## What you will be able to do

- Define SGTs and register an enforcer so it learns the group catalogue from ISE.
- Assign tags by IP-SGT mapping and distribute them with SXP.
- Author SGACLs and place them in a default-deny egress matrix.
- Prove the lateral flow is denied and read the per-cell drop counters.
- Plan a monitor-mode rollout and identify what the fabric cannot tag.

## Prerequisites

- **Track 1:** a Cisco ISE 3.x evaluation VM (4 vCPU / 16 GB) and an IOS-XE device — a Catalyst 9000v in Cisco Modeling Labs, or a physical Catalyst 9300 — plus four endpoint VMs.
- **Track 2:** one Ubuntu 22.04 host with `nftables` and `iproute2` (no Cisco account required).

## See also

- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab pairs with.
- [Volume XXV — Cisco Security](../volume-025-cisco-security/README.md) — broader Cisco ISE and identity coverage.
- [Volume CVI — Cloud-Native Segmentation](../volume-106-cloud-native-segmentation-lab/README.md) and [Volume C — Cisco Secure Workload](../volume-100-cisco-secure-workload-lab/README.md) — adjacent segmentation approaches to compare with the fabric model.
