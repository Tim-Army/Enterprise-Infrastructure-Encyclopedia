# Volume CIX — Fortinet ISFW and VDOM Build-It-Yourself Lab

> A build-it-yourself microsegmentation lab on **Fortinet FortiGate**, using the **Internal Segmentation
> Firewall (ISFW)** — a FortiGate placed *inside* the network so east-west traffic must pass a full
> policy — and **Virtual Domains (VDOMs)**, which split one FortiGate into independent virtual firewalls
> for hard multi-tenant separation. The lab puts a four-tier estate (web/db/hmi/plc) behind an ISFW,
> proves a permit-all lets the operator reach the database, contains it with least-privilege policies
> (permit only APP→DB PGSQL and MGMT→OT MODBUS, rely on the implicit deny), then hardens the OT tier into
> its own **VDOM** so IT↔OT crosses only a tightly scoped inter-VDOM link. Because FortiOS is commercial,
> this volume is **two-track**: Track 1 on a real **FortiGate-VM** evaluation, Track 2 a native
> **Linux/nftables** zone-and-table model on one host. Nine chapters, ~24 walkthrough labs.

## Overview

Volume CIX is a **hands-on lab volume** and the third of the fabric/firewall tier. It sits alongside
[Volume CVII (Cisco ISE + TrustSec)](../volume-107-cisco-ise-trustsec-lab/README.md) and
[Volume CVIII (Juniper Connected Security)](../volume-108-juniper-connected-security-lab/README.md) as the
third network-enforcement model: a stateful firewall placed internally (ISFW) plus hard partitioning
(VDOMs).

Its distinguishing ideas are the **ISFW pattern** — moving a full firewall from the perimeter to the
interior so east-west traffic is inspected, not just north-south — and **VDOMs**, which give total
default separation between virtual firewalls so IT and OT can share one box yet be as isolated as two.
The lab builds ISFW zone policy first, then demonstrates VDOM isolation and a single scoped inter-VDOM
crossing, and reaches the honest boundary: an ISFW only sees what transits it, so intra-zone and bypassed
traffic still need segmentation design or host controls.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Lab Preparation](chapters/02-lab-preparation.md) | 2.1–2.3 |
| 03 | [Zones and Address Objects](chapters/03-zones-and-address-objects.md) | 3.1–3.2 |
| 04 | [The Flat Policy and Lateral Movement](chapters/04-flat-policy-and-lateral-movement.md) | 4.1–4.3 |
| 05 | [Firewall Policies](chapters/05-firewall-policies.md) | 5.1–5.2 |
| 06 | [VDOMs for Hard Separation](chapters/06-vdoms-for-hard-separation.md) | 6.1–6.2 |
| 07 | [Enforcement and Verification](chapters/07-enforcement-and-verification.md) | 7.1–7.3 |
| 08 | [Security Fabric, Automation, and the Boundary](chapters/08-security-fabric-and-boundary.md) | 8.1–8.3 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

## What you will be able to do

- Place a FortiGate as an ISFW and group interfaces into zones.
- Author least-privilege firewall policies scoped by address object and service.
- Rely on the implicit deny and remove a permit-all safely.
- Split a tier into its own VDOM and permit only a scoped inter-VDOM crossing.
- Read policy lookups, session lists, and logs; contain a host with an automation stitch; identify the boundary.

## Prerequisites

- **Track 1:** a **FortiGate-VM** evaluation (KVM/ESXi/Workstation) with five interfaces and four endpoint VMs.
- **Track 2:** one Ubuntu 22.04 host with `nftables` and `iproute2` (no Fortinet software required).

## See also

- [Volume CVII — Cisco ISE and TrustSec](../volume-107-cisco-ise-trustsec-lab/README.md) and [Volume CVIII — Juniper Connected Security](../volume-108-juniper-connected-security-lab/README.md) — the other fabric/firewall models to contrast.
- [Volume XIX — Fortinet NSE Certification Program](../volume-019-fortinet-nse-certification/README.md) — broader FortiGate and FortiOS coverage.
- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab pairs with.
