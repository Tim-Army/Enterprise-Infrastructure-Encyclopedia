# Volume CIII — Istio Build-It-Yourself Lab

> A build-it-yourself Kubernetes microsegmentation lab on a single Linux host, segmenting at a
> different layer than a CNI: a real `kind` cluster running the **Istio** service mesh, with meshed
> workloads (a client, an HTTP API, a PostgreSQL database, and an operator — each with an Envoy
> sidecar and a **SPIFFE** identity from its ServiceAccount) plus one deliberately **un-meshed** PLC.
> The lab proves the mesh is permissive by default, then contains it with real Istio security:
> **mutual TLS** everywhere (`PeerAuthentication` STRICT), **AuthorizationPolicy** that authorizes by
> cryptographically-authenticated **principal** at Layer 4 and Layer 7 (HTTP method/path), a `Sidecar`
> resource to confine a compromised client's egress, and an honest look at the **mesh boundary** — why
> a mesh cannot protect the un-meshed PLC and is paired with a CNI NetworkPolicy. Because Istio is open
> source, this volume is **single-track**. **22 walkthrough labs** across nine chapters.

## Overview

Volume CIII is a **hands-on lab volume** and the third of the open-source tier. Where
[Volume LXXXVII (Microsegmentation Options)](../volume-087-microsegmentation-options/README.md)
compares vendors and
[its Chapter 12](../volume-087-microsegmentation-options/chapters/12-service-mesh-and-workload-identity.md)
summarizes service meshes including Istio, this volume is the **build**: 22 walkthrough labs that
stand up a real mesh, break it, and segment it.

Istio segments differently from the Calico and Cilium CNIs that precede it. It is a **service mesh**:
an Envoy sidecar beside each workload secures **service-to-service** traffic with **mTLS** and
authorizes it by **identity**. The identity is a **SPIFFE** ID derived from the Kubernetes
ServiceAccount and proven by a certificate — so authorization is on an *authenticated principal*, not
an IP or label an attacker could imitate. And because the sidecar is an L7 proxy, `AuthorizationPolicy`
can restrict HTTP methods and paths, not just ports.

The lab is also honest about the model's boundary: a mesh secures only what is *in* the mesh. The PLC
runs no sidecar, so Chapter 08 shows what Istio can (confine the meshed client's egress) and cannot
(enforce on the PLC) do, and why production pairs a mesh with a CNI network policy.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Host Preparation](chapters/02-host-preparation.md) | 2.1–2.2 |
| 03 | [Building the Cluster and Installing Istio](chapters/03-building-the-cluster.md) | 3.1–3.2 |
| 04 | [Deploying the Workloads](chapters/04-deploying-the-workloads.md) | 4.1–4.3 |
| 05 | [The Flat Mesh and Lateral Movement](chapters/05-flat-mesh-and-lateral-movement.md) | 5.1–5.3 |
| 06 | [mTLS and Workload Identity](chapters/06-mtls-and-workload-identity.md) | 6.1–6.3 |
| 07 | [AuthorizationPolicy](chapters/07-authorizationpolicy.md) | 7.1–7.3 |
| 08 | [The Mesh Boundary](chapters/08-the-mesh-boundary.md) | 8.1–8.3 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

## What you will be able to do

- Install Istio on a real cluster and enroll workloads in the mesh with per-workload identities.
- Require mTLS mesh-wide and inspect the SPIFFE identity each workload carries.
- Authorize traffic by authenticated principal at Layer 4 and by HTTP method/path at Layer 7.
- Confine a compromised client's egress with a `Sidecar` resource.
- Explain the mesh boundary and why meshes are paired with CNI network policy.

## Prerequisites

- A Linux host — an Ubuntu 22.04 VM, a cloud VM, or WSL2 — with 2 vCPU, 4 GB RAM, 20 GB disk.
- Docker, `kind`, `kubectl`, and `istioctl` (all free; installed in Chapter 02).

## See also

- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab pairs with.
- [Volume CI — Calico](../volume-101-calico-lab/README.md) and [Volume CII — Cilium](../volume-102-cilium-lab/README.md) — the CNI-based Kubernetes labs a mesh is paired with.
- The lighter-weight mesh **Linkerd** and the multi-platform **Consul**, later in this series.
