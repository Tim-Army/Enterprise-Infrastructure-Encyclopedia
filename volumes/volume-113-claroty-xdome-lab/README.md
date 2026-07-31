# Volume CXIII — Claroty xDome Build-It-Yourself Lab

> A build-it-yourself microsegmentation lab modeled on **Claroty xDome**, whose method is the
> **observe-then-enforce** loop rather than blind rule-writing: a passive collector on a **SPAN/mirror**
> discovers every OT asset and baselines every conversation without touching the network, you group assets
> into **virtual zones** and **derive a least-privilege policy from the sanctioned baseline**, and — because
> Claroty is passive — the policy is **enforced through integration** with a firewall, NAC, or switch. The
> lab builds a flat four-zone estate, passively discovers it, reproduces a lateral movement (and shows the
> trap that it pollutes a naively-learned baseline), **curates** the baseline, derives a zone-to-zone
> policy, pushes it to an enforcer that denies everything unbaselined, and sees the lateral attempt raised
> as a **deviation**. Because xDome is commercial SaaS, this volume is **two-track**: Track 1 describes the
> real product at design level; **Track 2 is a fully buildable native model** — `tcpdump` as the collector,
> a derived `nftables` policy as the integrated enforcer. Nine chapters, ~24 walkthrough labs.

## Overview

Volume CXIII is a **hands-on lab volume** and the second of the OT-security tier. Its defining idea is that
the segmentation policy is **derived from observed traffic**, not authored blind — the approach that fits a
brownfield OT plant where no one has a complete inventory or flow map. The lab makes the whole loop
concrete: passive discovery, a communication baseline, the review step that keeps an attack out of the
policy, zone-to-zone derivation, integrated enforcement, and deviation detection.

It also teaches the model's honest limits: Claroty **decides but does not block** — segmentation is only as
good as the enforcer it integrates with — and a collector only knows what is mirrored to it. The Track 2
model reproduces the loop end to end on one host, including the crucial curation step that separates a safe
enforced policy from one that blesses whatever happened during monitoring.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Lab Preparation](chapters/02-lab-preparation.md) | 2.1–2.3 |
| 03 | [Passive Discovery and the Baseline](chapters/03-passive-discovery-and-baseline.md) | 3.1–3.2 |
| 04 | [The Flat Network and Baseline Review](chapters/04-flat-network-and-baseline-review.md) | 4.1–4.3 |
| 05 | [Virtual Zones and the Segmentation Policy](chapters/05-virtual-zones-and-policy.md) | 5.1–5.2 |
| 06 | [Enforcing via Integration](chapters/06-enforcing-via-integration.md) | 6.1–6.2 |
| 07 | [Anomaly Detection and Verification](chapters/07-anomaly-detection-and-verification.md) | 7.1–7.3 |
| 08 | [Exposure, Scale, and the Boundary](chapters/08-exposure-scale-and-boundary.md) | 8.1–8.3 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

## What you will be able to do

- Passively discover assets and build a communication baseline from a traffic mirror.
- Recognize and curate a baseline polluted by a lateral movement.
- Group assets into virtual zones and derive a least-privilege zone-to-zone policy.
- Push the policy to an enforcer (default-deny) and confirm the lateral flow is denied.
- See denied and unbaselined flows raised as deviations; state the passive-only boundary.

## Prerequisites

- **Track 1:** Claroty xDome (commercial SaaS; covered at design level).
- **Track 2:** one Ubuntu 22.04 host with `nftables`, `iproute2`, and `tcpdump` (fully buildable, no Claroty software).

## See also

- [Volume CXII — Xage Security](../volume-112-xage-security-lab/README.md) — identity-brokered OT access, a contrasting OT model.
- [Volume XV — Forescout Platform and Certifications](../volume-015-forescout-platform-certifications/README.md) — passive discovery and network access control.
- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab pairs with.
