# Volume CXI — VMware NSX Distributed Firewall Build-It-Yourself Lab

> A build-it-yourself microsegmentation lab on the **VMware NSX Distributed Firewall (DFW)** — the model
> that enforces in the **hypervisor kernel at every VM's vNIC**, so it filters east-west traffic *before it
> reaches the wire*, including traffic between two VMs on the **same subnet and host** that a centralized
> firewall never sees. The lab deliberately puts all four workloads (web/db/hmi/plc) on **one subnet**,
> proves the default Allow lets the operator reach the database directly, then contains it with DFW rules
> written against **tag-driven groups** and a **Drop default** (zero-trust) — and demonstrates the defining
> win: `hmi → db` is denied at the database's own vNIC with no gateway between the peers. Because NSX is
> commercial, this volume is **two-track**: Track 1 on a real **NSX Manager + ESXi** transport node, Track 2
> a native model where **each workload is a namespace enforcing its own nftables ruleset** — a faithful
> reproduction of distributed, at-the-vNIC enforcement. Nine chapters, ~24 walkthrough labs; the capstone
> of the fabric/firewall tier.

## Overview

Volume CXI is a **hands-on lab volume** and the fifth and final volume of the fabric/firewall tier,
completing the set alongside Cisco TrustSec ([CVII](../volume-107-cisco-ise-trustsec-lab/README.md)),
Juniper Connected Security ([CVIII](../volume-108-juniper-connected-security-lab/README.md)), Fortinet
ISFW/VDOM ([CIX](../volume-109-fortinet-isfw-vdom-lab/README.md)), and Check Point CloudGuard
([CX](../volume-110-checkpoint-cloudguard-lab/README.md)).

Its distinguishing idea is **distributed enforcement**: the firewall lives at each workload's vNIC, so
there is no chokepoint and — uniquely among the five models — **no blind spot for same-subnet east-west
traffic**, which was the honest boundary every centralized model in this tier had to concede. Policy is
written against groups whose membership is computed from **security tags**, so onboarding a workload is a
tagging action rather than a firewall change, and enforcement follows the VM across hosts. The Track 2
model captures the distributed property directly by having every namespace enforce its own ruleset.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Lab Preparation](chapters/02-lab-preparation.md) | 2.1–2.3 |
| 03 | [Security Tags and Groups](chapters/03-tags-and-groups.md) | 3.1–3.2 |
| 04 | [The Flat Network and Lateral Movement](chapters/04-flat-network-and-lateral-movement.md) | 4.1–4.3 |
| 05 | [The DFW Rulebase](chapters/05-dfw-rulebase.md) | 5.1–5.2 |
| 06 | [Distributed Enforcement and the Same-Subnet Win](chapters/06-distributed-enforcement.md) | 6.1–6.2 |
| 07 | [Enforcement and Verification](chapters/07-enforcement-and-verification.md) | 7.1–7.3 |
| 08 | [Dynamic Membership, Scale, and the Boundary](chapters/08-dynamic-membership-and-boundary.md) | 8.1–8.3 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

## What you will be able to do

- Prepare a host so the DFW enforces at every vNIC.
- Tag workloads and build dynamic groups whose membership follows the tags.
- Author DFW rules by group with a zero-trust Drop default.
- Prove same-subnet `hmi → db` is denied at the destination vNIC with no gateway.
- Onboard a workload by tag alone; read hit counts and DFW logs; identify the boundary.

## Prerequisites

- **Track 1:** an **NSX Manager + ESXi** transport node evaluation (with vCenter) and four VMs on one segment.
- **Track 2:** one Ubuntu 22.04 host with `nftables` and `iproute2` (no VMware software required).

## See also

- [Volume CVII](../volume-107-cisco-ise-trustsec-lab/README.md), [Volume CVIII](../volume-108-juniper-connected-security-lab/README.md), [Volume CIX](../volume-109-fortinet-isfw-vdom-lab/README.md), and [Volume CX](../volume-110-checkpoint-cloudguard-lab/README.md) — the other four fabric/firewall models; DFW closes the same-subnet boundary they concede.
- [Volume V — VMware Virtualization](../volume-005-vmware-virtualization/README.md) and [Volume LXXII — VMware vSphere 8](../volume-072-vmware-vsphere-8/README.md) — broader VMware platform coverage.
- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab pairs with.
