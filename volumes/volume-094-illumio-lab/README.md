# Volume XCIV — Illumio Segmentation Build-It-Yourself Lab

> A build-it-yourself microsegmentation lab on a single Windows 11 host: five virtual machines
> across three isolated VMware segments — a three-legged Linux router, an nginx application tier, a
> PostgreSQL database, a Windows SCADA/HMI station, and an agentless "PLC" speaking Modbus TCP 502 —
> built, deliberately broken to reproduce lateral movement across a flat network, then contained
> with **Illumio**: the **PCE/VEN** split, the four-dimensional **label** model (Role, Application,
> Environment, Location), **Illumination** traffic discovery, the four **enforcement states** (Idle,
> Visibility Only, Selective, Full), draft-then-**provision** policy, and Illumio's distinctive
> answer for a device that can host no agent — represent it as an **unmanaged workload** and enforce
> its protection on the managed neighbors around it. **31 walkthrough labs** across nine chapters,
> each written on two tracks — a real Illumio PCE and VEN, or the native `nftables` and Windows
> Filtering Platform primitives the VEN itself programs — with every policy proved by a negative
> test before it is enforced, and a break-glass rollback rehearsed before teardown.

## Overview

Volume XCIV is a **hands-on lab volume**. Where
[Volume LXXXVII (Microsegmentation Options)](../volume-087-microsegmentation-options/README.md)
compares vendors and
[its Chapter 04](../volume-087-microsegmentation-options/chapters/04-workload-agent-based-platforms.md)
summarizes host-agent platforms including Illumio, this volume is the **build**: 31 walkthrough labs
that construct the estate, break it, and segment it with Illumio.

The estate is deliberately heterogeneous, because that heterogeneity is the reason a platform like
Illumio exists. You finish with modern Linux servers, a Windows server, and an unpatchable
"programmable logic controller" that cannot accept a security agent — the exact mix that forces an
architect to enforce policy in more than one place: with an agent on the hosts that can take one, and
from a managed neighbor for the host that cannot.

### An honest scope note

Illumio is **commercial software**. There is no single-laptop community edition of the control plane
(the PCE ships as SaaS or as a licensed on-premises cluster), and the VEN is generated and paired
against a PCE you have been granted. Every exercise in Chapters 06–08 is therefore written on **two
tracks**:

- **Track 1 — Real Illumio.** The actual console navigation, `illumio-ven-ctl` commands, pairing
  profiles, and verification points, for readers whose employer, partner account, or Illumio trial
  has granted a PCE. Tenant-specific values appear as placeholders such as `<pce-fqdn>:8443`.
- **Track 2 — Native equivalent.** A faithful path that runs today with no PCE, driving the *same
  enforcement primitives the VEN drives*: `nftables`/`iptables` on Linux and the Windows Filtering
  Platform on Windows.

Track 2 is not a mock-up. The VEN does not invent a packet filter; it programs the native OS
firewall. Writing the nftables rule yourself produces the artifact the PCE's policy compiler would
have generated. Exercises that genuinely cannot be reproduced without the product — Illumination flow
correlation, the policy compiler, a Network Enforcement Node — are marked **Design Exercise** and are
written analysis with a model answer, not pretend clicking.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Host Preparation](chapters/02-host-preparation.md) | 2.1–2.4 |
| 03 | [Building the Virtual Networks](chapters/03-virtual-networks.md) | 3.1–3.4 |
| 04 | [Building the Virtual Machines](chapters/04-building-the-virtual-machines.md) | 4.1–4.6 |
| 05 | [The Flat Network and Lateral Movement](chapters/05-flat-network-and-lateral-movement.md) | 5.1–5.3 |
| 06 | [Illumio Visibility, VENs, and Labels](chapters/06-illumio-visibility-and-labels.md) | 6.1–6.4 |
| 07 | [Enforcement and Label-Based Policy](chapters/07-enforcement-and-label-policy.md) | 7.1–7.4 |
| 08 | [Protecting the Agentless PLC](chapters/08-protecting-the-agentless-plc.md) | 8.1–8.3 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

## What you will be able to do

- Explain the PCE/VEN split and what the VEN programs on Linux (`iptables`/`nftables`) and Windows (WFP).
- Apply the Role/Application/Environment/Location label model and write policy against labels, not addresses.
- Move workloads through Idle → Visibility Only → Selective → Full Enforcement, using Visibility Only as a safety net.
- Discover flows in Illumination (or a native `conntrack` flow map) before writing a rule.
- Protect an agentless device by the unmanaged-workload model plus managed-neighbor and path enforcement.
- Troubleshoot a stuck VEN, an unprovisioned change, and an unexpected block — and roll back under pressure.

## Prerequisites

- A Windows 11 host: 4+ cores, 16 GB RAM (32 GB comfortable), 250 GB free SSD.
- VMware Workstation Pro 17.6.3 or 26H1 (free), Ubuntu Server 22.04.5 LTS, Windows Server 2022 Evaluation.
- Optional for Track 1: access to an Illumio PCE (SaaS trial or partner tenant) and the VEN package.

## See also

- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab pairs with.
- [Volume XCIII — ColorTokens Xshield Build-It-Yourself Lab](../volume-093-colortokens-xshield-lab/README.md) — the same estate, contained with a multi-mode platform and an inline agentless Gatekeeper.
- [Volume X — Enterprise Cybersecurity](../volume-010-enterprise-cybersecurity/README.md) and [Volume XXXV — Zscaler Zero Trust Exchange](../volume-035-zscaler-zero-trust-exchange/README.md) for the zero-trust context.
