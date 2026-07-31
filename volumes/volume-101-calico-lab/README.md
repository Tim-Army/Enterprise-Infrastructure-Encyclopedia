# Volume CI — Calico Build-It-Yourself Lab

> A build-it-yourself Kubernetes microsegmentation lab on a single Linux host: a real `kind`
> cluster running the **Calico** CNI, a four-workload application across two namespaces (an nginx-style
> web client, a PostgreSQL database, an operator, and an unpatchable "PLC" on Modbus TCP 502), broken
> to prove that a default Kubernetes network lets any pod reach any other, then contained with real
> Calico policy: **Kubernetes NetworkPolicy** (default-deny, label-based allows), Calico
> **GlobalNetworkPolicy** and **tiers** (cluster-wide guardrails with explicit `Deny` and ordered
> evaluation), and Calico **NetworkSets** and **HostEndpoints** for the world beyond pods. Because
> Calico is **open source**, this volume is **single-track** — there is nothing to simulate; every
> command runs the real thing. **23 walkthrough labs** across nine chapters.

## Overview

Volume CI is a **hands-on lab volume** and the first of the open-source tier in this microsegmentation
series. Where
[Volume LXXXVII (Microsegmentation Options)](../volume-087-microsegmentation-options/README.md)
compares vendors and
[its Chapter 08](../volume-087-microsegmentation-options/chapters/08-cloud-native-and-kubernetes.md)
summarizes the cloud-native and Kubernetes options including Calico, this volume is the **build**: 23
walkthrough labs that stand up a real cluster, break it, and segment it.

Unlike the commercial platforms elsewhere in the series, Calico has no licensing barrier, so this
volume is **single-track**: you install the real open-source CNI and use it directly. Where the
commercial **Calico Enterprise / Calico Cloud** editions add features (a flow-visualization UI,
hierarchical RBAC at scale, DNS policy), those are called out as an **Enterprise note** rather than
reproduced.

The lab teaches the full Kubernetes segmentation arc: that namespaces are *not* a network boundary by
default; that a **default-deny** NetworkPolicy is the floor everything builds on; that **labels**, not
pod IPs, are the only durable way to write policy in a world of ephemeral pods; and that Calico
reaches **beyond pods** to external endpoints and the node itself.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Host Preparation](chapters/02-host-preparation.md) | 2.1–2.3 |
| 03 | [Building the Cluster with Calico](chapters/03-building-the-cluster.md) | 3.1–3.2 |
| 04 | [Deploying the Workloads](chapters/04-deploying-the-workloads.md) | 4.1–4.3 |
| 05 | [The Flat Cluster and Lateral Movement](chapters/05-flat-cluster-and-lateral-movement.md) | 5.1–5.3 |
| 06 | [NetworkPolicy and the Calico Model](chapters/06-networkpolicy-and-the-calico-model.md) | 6.1–6.3 |
| 07 | [GlobalNetworkPolicy and Tiers](chapters/07-globalnetworkpolicy-and-tiers.md) | 7.1–7.3 |
| 08 | [Beyond Pods — HostEndpoints and NetworkSets](chapters/08-beyond-pods-hostendpoints-and-networksets.md) | 8.1–8.3 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

## What you will be able to do

- Build a real Kubernetes cluster with the Calico CNI on one Linux host.
- Prove that Kubernetes namespaces are not a network boundary, and fix that with default-deny.
- Write label-based NetworkPolicy that survives pod restarts.
- Add cluster-wide, ordered, deny-capable guardrails with GlobalNetworkPolicy and tiers.
- Govern flows to external endpoints with NetworkSets, and understand HostEndpoints and failsafe ports.

## Prerequisites

- A Linux host — an Ubuntu 22.04 VM (VMware Workstation), a cloud VM, or WSL2 — with 2 vCPU, 4 GB RAM, 20 GB disk.
- Docker, `kind`, `kubectl`, `calicoctl` (all free; installed in Chapter 02).

## See also

- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab pairs with.
- [Volume VIII — Containers and Platform Engineering](../volume-008-containers-platform-engineering/README.md) for Kubernetes fundamentals.
- The other open-source microsegmentation labs in this series (Cilium, Istio, Linkerd, Consul).
