# Volume CII — Cilium Build-It-Yourself Lab

> A build-it-yourself Kubernetes microsegmentation lab on a single Linux host: a real `kind` cluster
> running the **Cilium** CNI with an **eBPF** dataplane, five workloads across two namespaces (a
> client, a PostgreSQL database, an HTTP API, an operator, and a Modbus "PLC"), broken to prove the
> cluster is flat at Layer 3/4 *and* unrestricted at Layer 7, then contained with real Cilium policy:
> identity-based **L3/L4 CiliumNetworkPolicy**, cluster-wide guardrails, and — the differentiator —
> **Layer 7 policy** that restricts which **HTTP** methods and paths a client may use and which **DNS**
> names it may reach, all observed in **Hubble**. Because Cilium is open source, this volume is
> **single-track**. **23 walkthrough labs** across nine chapters.

## Overview

Volume CII is a **hands-on lab volume** and the second of the open-source tier. Where
[Volume LXXXVII (Microsegmentation Options)](../volume-087-microsegmentation-options/README.md)
compares vendors and
[its Chapter 08](../volume-087-microsegmentation-options/chapters/08-cloud-native-and-kubernetes.md)
summarizes the Kubernetes options including Cilium, this volume is the **build**: 23 walkthrough labs
that stand up a real cluster, break it, and segment it.

Cilium's differences from a traditional CNI are the point of the lab, and they build on the Calico
volume rather than repeat it:

- **eBPF and identity.** Cilium enforces in the Linux kernel with eBPF and identifies workloads by a
  label-derived **security identity**, not by IP.
- **Hubble.** Every flow — with source and destination identity, verdict, and Layer 7 detail — is
  observable from a CLI and a service-map UI.
- **Layer 7 policy.** A `CiliumNetworkPolicy` can restrict **HTTP** methods and paths, and govern
  egress by **DNS name** (FQDN) — controls no Layer 3/4 firewall, and no standard Kubernetes
  NetworkPolicy, can express. The lab includes an HTTP API specifically so you can enforce and observe
  this.

Where the commercial **Cilium Enterprise (Isovalent)** edition adds features (Tetragon runtime
security at scale, a richer UI, cluster mesh), those are called out as an **Enterprise note**.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Host Preparation](chapters/02-host-preparation.md) | 2.1–2.2 |
| 03 | [Building the Cluster with Cilium](chapters/03-building-the-cluster.md) | 3.1–3.3 |
| 04 | [Deploying the Workloads](chapters/04-deploying-the-workloads.md) | 4.1–4.3 |
| 05 | [The Flat Cluster and Lateral Movement](chapters/05-flat-cluster-and-lateral-movement.md) | 5.1–5.3 |
| 06 | [Hubble and the Identity Model](chapters/06-hubble-and-the-identity-model.md) | 6.1–6.3 |
| 07 | [L3/L4 CiliumNetworkPolicy](chapters/07-l3-l4-ciliumnetworkpolicy.md) | 7.1–7.3 |
| 08 | [L7-Aware Policy](chapters/08-l7-aware-policy.md) | 8.1–8.3 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

## What you will be able to do

- Build a real Kubernetes cluster with the Cilium eBPF CNI and Hubble on one Linux host.
- Observe flows by identity and verdict, and read the Hubble service map.
- Write identity-based L3/L4 CiliumNetworkPolicy that survives pod restarts.
- Enforce Layer 7 policy: HTTP method/path restrictions and DNS/FQDN egress.
- Troubleshoot with Hubble and roll back safely.

## Prerequisites

- A Linux host — an Ubuntu 22.04 VM, a cloud VM, or WSL2 — with 2 vCPU, 4 GB RAM, 20 GB disk.
- Docker, `kind`, `kubectl`, the `cilium` CLI, and the `hubble` CLI (all free; installed in Chapter 02).

## See also

- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab pairs with.
- [Volume CI — Calico](../volume-101-calico-lab/README.md) — the preceding open-source Kubernetes lab; this volume assumes its L3/L4 concepts and goes to Layer 7.
- [Volume VIII — Containers and Platform Engineering](../volume-008-containers-platform-engineering/README.md) for Kubernetes fundamentals.
