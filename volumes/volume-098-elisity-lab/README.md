# Volume XCVIII — Elisity Build-It-Yourself Lab

> A build-it-yourself microsegmentation lab on a single Windows 11 host: five virtual machines
> across **four** isolated VMware segments — a four-legged Linux router that stands in for the
> Elisity-managed access switch, an nginx application tier, a PostgreSQL database on its own segment
> behind the enforcement point, a Windows SCADA/HMI station, and an agentless "PLC" speaking Modbus
> TCP 502 — built, deliberately broken to reproduce lateral movement across the enforcement point,
> then contained with **Elisity**: the **IdentityGraph** (classify every user, device, and workload
> from existing sources — AD/Entra ID, vCenter, ServiceNow, Infoblox, EDR — independent of IP),
> **identity-based policy groups**, and **network enforcement** with no endpoint agents and no new
> hardware. **30 walkthrough labs** across nine chapters, each on two tracks — a real Elisity Cloud
> deployment with a Virtual Edge on your switches, or a native IdentityGraph built from a CMDB source
> and compiled into identity-based `nftables` ACLs on the router.

## Overview

Volume XCVIII is a **hands-on lab volume**. Where
[Volume LXXXVII (Microsegmentation Options)](../volume-087-microsegmentation-options/README.md)
compares vendors and
[its Chapter 13](../volume-087-microsegmentation-options/chapters/13-identity-based-and-overlay-independents.md)
summarizes Elisity, this volume is the **build**: 30 walkthrough labs that construct the estate,
break it, and segment it.

Elisity is the first **identity-based, network-enforced, agentless** platform in this lab series, and
its build differs accordingly. There is no host agent anywhere; enforcement lives on the network. To
model that honestly in a router-only lab, the database sits on its **own segment behind `el-gw`**, so
every access to the crown jewel crosses the enforcement point — the way an access switch would see
it. The distinctive lesson is the **IdentityGraph**: classify by identity from existing sources, write
policy by identity, and let the enforcement point follow the identity across re-addressing and change.

### An honest scope note

Elisity is **commercial software**, and its real enforcement point is a **managed access switch** via
Elisity Cloud and a Virtual Edge connector — neither of which exists in a single-host VM lab. Every
exercise in Chapters 06–08 is therefore written on **two tracks**:

- **Track 1 — Real Elisity.** The Elisity Cloud workflow — connecting identity sources, reviewing the
  IdentityGraph, building policy groups and policy, enforcing through the Virtual Edge on switches.
- **Track 2 — Native equivalent.** A hand-built IdentityGraph from a CMDB source, compiled into
  identity-based `nftables` ACLs on `el-gw`, the network enforcement point standing in for the switch.

Exercises that genuinely cannot be reproduced without the product — live source ingestion, the Virtual
Edge, and switch programming at scale — are marked **Design Exercise** with a model answer.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Host Preparation](chapters/02-host-preparation.md) | 2.1–2.4 |
| 03 | [Building the Virtual Networks](chapters/03-virtual-networks.md) | 3.1–3.4 |
| 04 | [Building the Virtual Machines](chapters/04-building-the-virtual-machines.md) | 4.1–4.6 |
| 05 | [The Flat Network and Lateral Movement](chapters/05-flat-network-and-lateral-movement.md) | 5.1–5.3 |
| 06 | [The IdentityGraph and Policy Groups](chapters/06-identitygraph-and-policy-groups.md) | 6.1–6.3 |
| 07 | [Identity-Based Enforcement at the Network](chapters/07-enforcement-at-the-network.md) | 7.1–7.4 |
| 08 | [The Agentless PLC, Segmented by Identity](chapters/08-agentless-ot-by-identity.md) | 8.1–8.3 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

## What you will be able to do

- Explain how Elisity classifies assets in an IdentityGraph from existing sources and enforces on the network.
- Build an IdentityGraph by hand and derive identity-based policy groups.
- Enforce identity-based policy at a network point and see it follow identity across a re-address.
- Protect an agentless OT device with the same policy engine, no agent required.
- Troubleshoot classification-driven denies and roll back via out-of-band paths.

## Prerequisites

- A Windows 11 host: 4+ cores, 16 GB RAM (32 GB comfortable), 250 GB free SSD.
- VMware Workstation Pro 17.6.3 or 26H1 (free), Ubuntu Server 22.04.5 LTS, Windows Server 2022 Evaluation.
- Optional for Track 1: access to an Elisity Cloud deployment and switching infrastructure.

## See also

- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab pairs with.
- [Volume XCIII — ColorTokens](../volume-093-colortokens-xshield-lab/README.md) through [Volume XCVII — TrueFort](../volume-097-truefort-lab/README.md) — the same estate contained with host-agent and agentless platforms.
