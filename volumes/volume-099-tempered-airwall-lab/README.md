# Volume XCIX — Tempered Airwall Build-It-Yourself Lab

> A build-it-yourself microsegmentation lab on a single Windows 11 host: five virtual machines
> across three isolated VMware underlay segments — a three-legged Linux router, an nginx application
> tier, a PostgreSQL database, a Windows SCADA/HMI station, and an agentless "PLC" speaking Modbus
> TCP 502 — built, deliberately broken to reproduce lateral movement across a flat underlay, then
> contained with **Tempered Airwall**: the **Host Identity Protocol (HIP)** encrypted overlay
> (cryptographic device identity, always-on encryption, **cloaking** so protected devices go dark on
> the underlay, and default-deny), microsegmentation expressed as **overlay trust policy** in the
> Airwall Conductor, and the **Airwall Gateway** that carries a device which can hold no identity of
> its own onto the overlay. **29 walkthrough labs** across nine chapters, each on two tracks — a real
> Airwall deployment (Conductor, Agents, Gateways), or a genuine encrypted overlay built with
> **WireGuard**: public-key identities, a hub that enforces trust policy, underlay cloaking, and a
> gateway for the agentless PLC. This is the one volume in the series whose native track is a real
> encrypted overlay rather than host-firewall rules — because that is what Airwall is.

## Overview

Volume XCIX is a **hands-on lab volume**. Where
[Volume LXXXVII (Microsegmentation Options)](../volume-087-microsegmentation-options/README.md)
compares vendors and
[its Chapter 13](../volume-087-microsegmentation-options/chapters/13-identity-based-and-overlay-independents.md)
summarizes Tempered Airwall, this volume is the **build**: 29 walkthrough labs that construct the
estate, break it, and segment it.

Airwall does not filter the network you have; it builds a **new encrypted overlay** and moves your
protected devices onto it, then goes **dark** on the underlay. The distinctive lesson is that
microsegmentation becomes *overlay membership and cryptographic identity*, not firewall rules — and
that an un-agentable device is carried onto the overlay by a **gateway** rather than left behind. The
native track uses WireGuard, whose public-key identities, encryption, default-deny, and silent
cloaking reproduce the HIP model almost one-for-one.

### An honest scope note

Tempered Airwall is **commercial software** (Johnson Controls); the Conductor, Agents, and Gateways
are licensed. Every exercise in Chapters 06–08 is therefore written on **two tracks**:

- **Track 1 — Real Airwall.** The Conductor workflow — provisioning Agents and Gateways, licensing
  identities, and building overlay networks and trust.
- **Track 2 — Native equivalent.** A real encrypted overlay with **WireGuard**: cryptographic
  identities, a hub on `aw-gw` that enforces trust policy, underlay cloaking, and an `aw-gw` gateway
  that carries the agentless PLC onto the overlay.

Exercises that genuinely cannot be reproduced without the product — Conductor-managed identity
lifecycle, revocation, and scale — are marked **Design Exercise** with a model answer.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Host Preparation](chapters/02-host-preparation.md) | 2.1–2.4 |
| 03 | [Building the Virtual Networks](chapters/03-virtual-networks.md) | 3.1–3.3 |
| 04 | [Building the Virtual Machines](chapters/04-building-the-virtual-machines.md) | 4.1–4.6 |
| 05 | [The Flat Network and Lateral Movement](chapters/05-flat-network-and-lateral-movement.md) | 5.1–5.3 |
| 06 | [The HIP Overlay and Cloaking](chapters/06-the-hip-overlay-and-cloaking.md) | 6.1–6.3 |
| 07 | [Overlay Microsegmentation](chapters/07-overlay-microsegmentation.md) | 7.1–7.4 |
| 08 | [The Airwall Gateway for the Agentless PLC](chapters/08-airwall-gateway-for-the-plc.md) | 8.1–8.3 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

## What you will be able to do

- Explain the HIP overlay model (identity, encryption, cloaking, default-deny) and map it to WireGuard.
- Build an encrypted overlay, give each device a cryptographic identity, and cloak the underlay.
- Express microsegmentation as overlay trust policy and enforce it on the hub.
- Carry an agentless device onto the overlay with a gateway and authorize only the flow it needs.
- Troubleshoot overlay connectivity versus authorization, and roll back via an out-of-band path.

## Prerequisites

- A Windows 11 host: 4+ cores, 16 GB RAM (32 GB comfortable), 250 GB free SSD.
- VMware Workstation Pro 17.6.3 or 26H1 (free), Ubuntu Server 22.04.5 LTS, Windows Server 2022 Evaluation.
- WireGuard (free, open source) for Track 2; optional Airwall deployment for Track 1.

## See also

- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab pairs with.
- [Volume XCIII — ColorTokens](../volume-093-colortokens-xshield-lab/README.md) through [Volume XCVIII — Elisity](../volume-098-elisity-lab/README.md) — the same estate contained with host-agent, agentless, and identity-network platforms.
