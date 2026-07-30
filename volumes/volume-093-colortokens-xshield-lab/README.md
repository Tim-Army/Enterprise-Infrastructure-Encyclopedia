# Volume XCIII — ColorTokens Xshield Build-It-Yourself Lab

> A single-laptop, five-virtual-machine microsegmentation lab: build a heterogeneous enterprise in
> miniature on VMware Workstation, prove that a flat network lets an attacker move sideways, then
> contain that movement with ColorTokens Xshield concepts — host-agent enforcement on Linux and
> Windows, tag-based policy, Observe-before-Enforce, and the agentless Gatekeeper fronting a device
> that can host no agent. Every exercise is written on two tracks: real Xshield console steps, and a
> native-equivalent path using the same enforcement primitives the agent programs.

## Overview

Volume XCIII is a **hands-on lab volume**. Where
[Volume LXXXVII (Microsegmentation Options)](../volume-087-microsegmentation-options/README.md)
compares vendors and
[its Chapter 07](../volume-087-microsegmentation-options/chapters/07-colortokens-xshield.md)
summarizes ColorTokens Xshield, this volume is the **build**: 30 walkthrough labs that construct the
estate, break it, and segment it.

The estate is deliberately heterogeneous, because that heterogeneity is the reason a platform like
Xshield exists. You finish with modern Linux servers, a Windows server, and an unpatchable
"programmable logic controller" that cannot accept a security agent — the exact mix that forces an
architect to choose a **different enforcement mode per asset**.

### An honest scope note

ColorTokens Xshield is **commercial SaaS**. There is no public download or self-service trial of the
agent (the installer is generated per tenant and its file name embeds a Product Key), and the console
cannot be run locally. Every exercise in Chapters 06–08 is therefore written on **two tracks**:

- **Track 1 — Real Xshield.** The actual console navigation, agent commands, and verification points,
  for readers whose employer, partner account, or ColorTokens evaluation has granted a tenant.
  Tenant-specific values appear as placeholders such as `<your-instance>.colortokens.com`.
- **Track 2 — Native equivalent.** A faithful path that runs today with no tenant, driving the *same
  underlying enforcement primitives the Xshield agent drives*: `nftables`/`iptables` on Linux and the
  Windows Filtering Platform on Windows.

Track 2 is not a mock-up. The host agent does not invent a packet filter; it programs the native OS
firewall. Writing the nftables rule yourself produces the artifact the policy compiler would have
generated. Exercises that genuinely cannot be reproduced without the product — the flow map, the AI
policy assistant, EDR-mediated enforcement — are marked **Design Exercise** and are written analysis
with a model answer, not pretend clicking.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Host Preparation](chapters/02-host-preparation.md) | 2.1–2.3 |
| 03 | [Building the Virtual Networks](chapters/03-virtual-networks.md) | 3.1–3.4 |
| 04 | [Building the Virtual Machines](chapters/04-building-the-virtual-machines.md) | 4.1–4.6 |
| 05 | [The Flat Network and Lateral Movement](chapters/05-flat-network-and-lateral-movement.md) | 5.1–5.3 |
| 06 | [Xshield Visibility and Ring-Fencing](chapters/06-xshield-visibility-and-policy.md) | 6.1–6.4 |
| 07 | [Enforcement and Tag-Based Policy](chapters/07-enforcement-and-tag-based-policy.md) | 7.1–7.4 |
| 08 | [The Gatekeeper: Agentless OT Segmentation](chapters/08-gatekeeper-agentless-ot.md) | 8.1–8.3 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

Chapter 01 is orientation — topology, address plan, resource budget, and bill of materials — and
carries no numbered lab; its completion checklist is the pre-flight gate instead.

## What you build

Three isolated Layer 2 segments joined by one multi-homed Linux router that doubles as the
Gatekeeper-equivalent for the OT cell:

| Host | Role | IT/NAT | Data Center | OT Cell |
| --- | --- | --- | --- | --- |
| Windows 11 host | Admin console; "IT laptop" | 192.168.170.1 | 10.10.20.1 | *(none — by design)* |
| **ct-gw** | Router; Gatekeeper-equivalent | 192.168.170.10 | 10.10.20.254 | 10.10.30.254 |
| **ct-app01** | Web/app tier, nginx :80 | — | 10.10.20.11 | — |
| **ct-db01** | PostgreSQL :5432 | — | 10.10.20.12 | — |
| **ct-win01** | Windows workload; SCADA/HMI | — | 10.10.20.21 | — |
| **ct-ot01** | "PLC", Modbus TCP :502, agentless | — | — | 10.10.30.50 |

The OT segment has **no host virtual adapter**. The Windows host has no Layer 2 presence there, so
every packet reaching the PLC must be routed by `ct-gw` — the physical property a real Gatekeeper
appliance depends on, and the reason "make the Gatekeeper the default gateway" is an instruction
rather than a suggestion.

## Prerequisites

- A Windows 11 host: **minimum** 4 physical cores, 16 GB RAM, 250 GB free SSD; **comfortable** 8
  cores, 32 GB RAM, 400 GB free NVMe.
- VMware Workstation Pro (17.6.3 as written; 26H1 works identically for every step this lab
  touches). Free for commercial, educational, and personal use since 11 November 2024.
- Ubuntu Server 22.04.5 LTS and Windows Server 2022 Evaluation ISOs (~8 GB of downloads total).
- Budget two comfortable days or four evenings; Chapter 04 is the long pole and is mostly waiting.

## Scope and ethics

The lateral-movement exercise in Chapter 05 exists to **measure blast radius on your own lab estate**
so the remaining chapters can eliminate it. It uses ordinary reachability checks and the lab's own
documented throwaway database credential — no exploit code and no attack tooling. Everything in this
volume is authorized administration of infrastructure you built yourself, and the sole purpose is
defensive: containment, verification, and rollback.

Product specifics change. Verify current Xshield details against ColorTokens' official documentation
before any production decision; the facts this lab relies on are listed in
[Chapter 09, Appendix C](chapters/09-operations-troubleshooting-teardown.md).

## Origin and lab numbering

This volume was contributed as a standalone lab guide and split into chapters for the encyclopedia.
Its original Part/Exercise labels map to chapter labs as follows:

| Original | Chapter | Labs |
| --- | --- | --- |
| Part A — Host Preparation | 02 | A1–A3 → 2.1–2.3 |
| Part B — Virtual Networks | 03 | B1–B4 → 3.1–3.4 |
| Part C — Virtual Machines | 04 | C1–C6 → 4.1–4.6 |
| Part D — Flat Network | 05 | D1–D3 → 5.1–5.3 |
| Part E — Visibility and Policy | 06 | E1–E4 → 6.1–6.4 |
| Part E — Enforcement | 07 | E5–E8 → 7.1–7.4 |
| Part F — Gatekeeper | 08 | F1–F3 → 8.1–8.3 |
| Part G — Operations | 09 | G1–G3 → 9.1–9.3 |

VM snapshot names keep their original labels (`C1-base-router`, `C3-base-db`, and so on) because they
are values you create and type, not cross-references.

## See also

- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) —
  vendor comparison, enforcement models, and the decision matrix.
- [Volume X — Enterprise Cybersecurity](../volume-010-enterprise-cybersecurity/README.md)
- [Volume LXXI — VMware vSphere 7](../volume-071-vmware-vsphere-7/README.md) and
  [Volume LXXII — VMware vSphere 8](../volume-072-vmware-vsphere-8/README.md)
- [Volume XXVI — Proxmox Virtualization Lab](../volume-026-proxmox-lab-poweredge-r640/README.md) —
  a comparable build-it-yourself lab volume.

Volume [INDEX](INDEX.md) · [GLOSSARY](GLOSSARY.md) · [master index](../../INDEX.md)
