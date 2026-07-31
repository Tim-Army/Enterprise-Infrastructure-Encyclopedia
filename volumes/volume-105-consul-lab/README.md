# Volume CV — HashiCorp Consul Build-It-Yourself Lab

> A build-it-yourself Kubernetes microsegmentation lab on a single Linux host, and the widest-reaching
> mesh in the series: a real `kind` cluster running **HashiCorp Consul** with Connect, meshed services
> (a client, an HTTP API, a PostgreSQL database, and an operator, each with a Consul sidecar and a
> **SPIFFE** identity) plus one un-meshed PLC. The lab proves Connect's mTLS secures traffic but does
> not restrict it, then contains it with **service intentions** — Consul's readable "who may call
> whom" authorization, default-deny by a wildcard then exact allows, at L4 and L7 (HTTP method/path) —
> and shows Consul's defining trait: the same intentions govern services on **VMs** as on Kubernetes,
> **one mesh across platforms**. Because Consul is open source, this volume is **single-track**. **22
> walkthrough labs** across nine chapters, completing the open-source tier of the microsegmentation
> lab series.

## Overview

Volume CV is a **hands-on lab volume** and the fifth and final volume of the open-source tier. Where
[Volume LXXXVII (Microsegmentation Options)](../volume-087-microsegmentation-options/README.md)
compares vendors and
[its Chapter 12](../volume-087-microsegmentation-options/chapters/12-service-mesh-and-workload-identity.md)
summarizes service meshes including Consul, this volume is the **build**: 22 walkthrough labs that
stand up a real mesh, break it, and segment it.

Consul's distinguishing trait, and the reason it closes the open-source tier, is **reach**: Istio and
Linkerd mesh Kubernetes pods, but Consul meshes **services on VMs and bare metal in the same mesh** as
pods, governed by the same **intentions**. An intention — "source service may call destination
service" — is written by service *name*, so it means the same thing whether the service runs as a pod
here or on a VM elsewhere. The lab builds the Kubernetes half hands-on and scripts how the VM half
joins, and it reaches the same honest boundary as the other mesh labs: the un-meshed PLC needs a CNI
network policy beneath the mesh.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Host Preparation](chapters/02-host-preparation.md) | 2.1–2.2 |
| 03 | [Building the Cluster and Installing Consul](chapters/03-installing-consul.md) | 3.1–3.3 |
| 04 | [Deploying the Workloads](chapters/04-deploying-the-workloads.md) | 4.1–4.2 |
| 05 | [The Flat Mesh and Lateral Movement](chapters/05-flat-mesh-and-lateral-movement.md) | 5.1–5.3 |
| 06 | [mTLS and Identity with Connect](chapters/06-mtls-and-identity.md) | 6.1–6.3 |
| 07 | [Service Intentions](chapters/07-service-intentions.md) | 7.1–7.3 |
| 08 | [Multi-Platform Reach and the Boundary](chapters/08-multi-platform-and-the-boundary.md) | 8.1–8.3 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

## What you will be able to do

- Install Consul with Connect, TLS, and ACLs on a real cluster, and mesh workloads.
- Confirm Connect secures service-to-service traffic with mTLS and SPIFFE identity.
- Write service intentions — default-deny plus exact allows — at L4 and L7.
- Explain how a VM service joins the same mesh under the same intentions.
- Recognize the un-meshed boundary and pair the mesh with a CNI network policy.

## Prerequisites

- A Linux host — an Ubuntu 22.04 VM, a cloud VM, or WSL2 — with 2 vCPU, 4 GB RAM (6 GB comfortable), 20 GB disk.
- Docker, `kind`, `kubectl`, `helm`, and the `consul` CLI (all free; installed in Chapter 02).

## See also

- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab pairs with.
- [Volume CIII — Istio](../volume-103-istio-lab/README.md) and [Volume CIV — Linkerd](../volume-104-linkerd-lab/README.md) — the Kubernetes-only meshes this volume extends beyond.
- [Volume CI — Calico](../volume-101-calico-lab/README.md) and [Volume CII — Cilium](../volume-102-cilium-lab/README.md) — the CNI policy engines a mesh is paired with.
