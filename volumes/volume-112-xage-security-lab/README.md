# Volume CXII — Xage Security Build-It-Yourself Lab

> A build-it-yourself microsegmentation lab modeled on **Xage Security**, whose approach to protecting
> operational technology is fundamentally different from the firewalls and fabrics of the previous tier:
> instead of filtering packets by address, Xage places an **enforcement point in front of each asset** and
> **brokers every connection through an identity check**, so a legacy PLC that speaks unauthenticated
> Modbus becomes reachable only by a named, authenticated identity with an explicit grant — the device is
> *wrapped*, not changed. Policy and identity live in the decentralized, tamper-resistant **Xage Fabric**,
> so there is no central controller to compromise. The lab isolates a legacy PLC and a database so they
> have no direct path, stands up an **identity-brokering proxy** that forwards only for a valid, granted
> identity, proves a compromised host and an ungranted identity are denied, and shows credential rotation
> and decentralized resilience. Because Xage has no open evaluation, this volume is **two-track**: Track 1
> describes the real Xage Fabric at architecture level; **Track 2 is a fully buildable native
> identity-broker model** on one Linux host. Nine chapters, ~22 walkthrough labs; opens the OT-security
> tier.

## Overview

Volume CXII is a **hands-on lab volume** and the first of the OT-security tier. It stands apart from the
fabric/firewall models (Volumes CVII–CXI) because its unit of policy is **identity**, not address, and its
target is **brownfield OT**: devices that cannot be patched, cannot authenticate, and cannot defend
themselves. Xage's answer is to remove the direct path to the asset and broker every session through an
identity check, adding authentication, authorization, and a per-connection audit trail to a device that
has none of its own.

The Track 2 model builds this concretely — an isolated OT cell, a broker that validates an identity token
against a grant before proxying to the asset, and nftables ensuring the asset is reachable *only* through
the broker — so the identity-brokered property is demonstrable on a laptop. The lab also models the
decentralized fabric (policy that survives a manager outage) and reaches the honest boundary: brokering
and isolation are one control, and a bypass path defeats it.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Lab Preparation](chapters/02-lab-preparation.md) | 2.1–2.3 |
| 03 | [Identities and the Fabric](chapters/03-identities-and-the-fabric.md) | 3.1–3.2 |
| 04 | [The Flat Network and Lateral Movement](chapters/04-flat-network-and-lateral-movement.md) | 4.1–4.3 |
| 05 | [Identity-Brokered Segmentation](chapters/05-identity-brokered-segmentation.md) | 5.1–5.2 |
| 06 | [Legacy OT and the Decentralized Fabric](chapters/06-legacy-ot-and-decentralized-fabric.md) | 6.1–6.2 |
| 07 | [Enforcement and Verification](chapters/07-enforcement-and-verification.md) | 7.1–7.3 |
| 08 | [Secrets, Scale, and the Boundary](chapters/08-secrets-scale-and-boundary.md) | 8.1–8.3 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

## What you will be able to do

- Isolate a legacy asset so it has no direct network path.
- Broker access to it through an identity-checking proxy that forwards only granted identities.
- Prove a compromised host and a valid-but-ungranted identity are both denied.
- Rotate a credential without changing the access policy.
- Explain the decentralized fabric and the isolation-plus-brokering boundary.

## Prerequisites

- **Track 1:** the real Xage Fabric (commercial; this volume covers it at design level).
- **Track 2:** one Ubuntu 22.04 host with `nftables`, `iproute2`, and `socat` (fully buildable, no Xage software).

## See also

- [Volume XV — Forescout Platform and Certifications](../volume-015-forescout-platform-certifications/README.md) — OT/IoT visibility and network access control.
- [Volume CXI — VMware NSX Distributed Firewall](../volume-111-vmware-nsx-dfw-lab/README.md) — the distributed-firewall model to contrast with identity brokering.
- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab pairs with.
