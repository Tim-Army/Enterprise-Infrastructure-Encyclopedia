# Volume CXIX — HPE Aruba CX 10000 Build-It-Yourself Lab

> A build-it-yourself microsegmentation lab modeled on the **HPE Aruba CX 10000 distributed services
> switch**, which embeds an **AMD Pensando DPU** in the top-of-rack switch and runs a **stateful firewall**
> — connection-tracked east-west policy, plus NAT and per-flow telemetry — at line rate **in the switch**,
> so every server-to-server flow in the rack is firewalled without hair-pinning to a separate appliance.
> The distinguishing property is **stateful enforcement in the fabric**: where the ASIC fabrics of the
> previous volumes (ACI, Arista MSS) enforce largely *stateless* group/contract ACLs, the CX 10000's DPU
> tracks **connection state** — return traffic is permitted automatically, and unsolicited or invalid
> packets are dropped, closing the reverse-tuple hole a stateless "allow the reply" rule leaves open. The
> lab applies a default-deny stateful policy permitting only `web→db:5432` and `hmi→plc:502`, proves the
> reply flows by state (no reverse rule), shows an unsolicited reverse packet dropped, and reads the DPU's
> per-flow connection table. Because enforcement lives in DPU hardware with no free emulator, this volume
> is **design-leaning two-track**: Track 1 describes the CX 10000/PSM; **Track 2 is a fully buildable
> stateful model** using nftables connection tracking — exactly the behavior the DPU accelerates. Nine
> chapters, ~24 walkthrough labs.

## Overview

Volume CXIX is a **hands-on lab volume** and the third of the hardware-fabric/DPU tier — the first of two
DPU-based volumes. Its defining idea is **stateful firewalling distributed to the top-of-rack**: firewall-
grade east-west policy (connection tracking, not just L3/L4 ACLs) applied in the switch DPU at line rate,
so stateful capacity scales with the fabric and there is no central-firewall bottleneck or traffic hairpin.

The lab makes the stateful advantage concrete — replies carried by connection state rather than a
mirror-image rule, and the unsolicited reverse-tuple packet that a stateless fabric would pass being
dropped — and reads the per-flow telemetry the DPU produces inline. It also draws the honest boundary: the
CX 10000 firewalls traffic crossing its ToR at L3/L4, so off-ToR servers and L7 need complementary
controls.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Lab Preparation](chapters/02-lab-preparation.md) | 2.1–2.3 |
| 03 | [The Flat Network and Lateral Movement](chapters/03-flat-network-and-lateral-movement.md) | 3.1–3.3 |
| 04 | [Stateful Microsegmentation at the ToR](chapters/04-stateful-microsegmentation.md) | 4.1–4.2 |
| 05 | [The Stateful Advantage](chapters/05-stateful-advantage.md) | 5.1–5.2 |
| 06 | [Per-Flow Telemetry and Connection Visibility](chapters/06-per-flow-telemetry.md) | 6.1–6.2 |
| 07 | [Enforcement and Verification](chapters/07-enforcement-and-verification.md) | 7.1–7.3 |
| 08 | [Fabric Composer, Scale, and the Boundary](chapters/08-fabric-composer-scale-and-boundary.md) | 8.1–8.3 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

## What you will be able to do

- Apply a default-deny stateful firewall permitting only the sanctioned east-west flows.
- Rely on connection state so return traffic needs no reverse rule.
- Show an unsolicited reverse-tuple packet dropped that a stateless fabric would pass.
- Read the DPU's per-flow connection table and deny log.
- State the per-ToR / L3-L4 boundary and where the DPU model fits alongside stateless fabrics.

## Prerequisites

- **Track 1:** an Aruba CX 10000 (embedded Pensando DPU) with PSM / Fabric Composer — hardware; covered at design level.
- **Track 2:** one Ubuntu 22.04 host with `nftables`, `iproute2`, and `conntrack` (fully buildable, no Aruba hardware).

## See also

- [Volume CXVII — Cisco ACI](../volume-117-cisco-aci-lab/README.md) and [Volume CXVIII — Arista MSS-Group](../volume-118-arista-mss-group-lab/README.md) — the stateless ASIC fabrics this stateful DPU model contrasts with.
- [Volume LXIV — HPE Aruba Networking Certification Tracks](../volume-064-aruba-certifications/README.md) — broader Aruba coverage.
- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab pairs with.
