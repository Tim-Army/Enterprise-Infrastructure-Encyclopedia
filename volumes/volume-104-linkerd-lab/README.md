# Volume CIV — Linkerd Build-It-Yourself Lab

> A build-it-yourself Kubernetes microsegmentation lab on a single Linux host: a real `kind` cluster
> running the **Linkerd** service mesh — the lightweight, security-first alternative to Istio — with
> meshed workloads (a client, an HTTP API, a PostgreSQL database, and an operator, each with a Rust
> micro-proxy and a **ServiceAccount identity**) plus one deliberately **un-meshed** PLC. The lab
> proves the mesh secures traffic but does not restrict it by default, then contains it with real
> Linkerd security: **automatic, zero-configuration mutual TLS**; the `Server` +
> `MeshTLSAuthentication` + `AuthorizationPolicy` model (a `Server` flips a port to deny-by-default,
> identities are authorized explicitly); a namespace `default-inbound-policy=deny` guardrail; and an
> honest look at the **mesh boundary** — why it cannot protect the un-meshed PLC and is paired with a
> CNI network policy. Because Linkerd is open source, this volume is **single-track**. **23 walkthrough
> labs** across nine chapters.

## Overview

Volume CIV is a **hands-on lab volume** and the fourth of the open-source tier. Where
[Volume LXXXVII (Microsegmentation Options)](../volume-087-microsegmentation-options/README.md)
compares vendors and
[its Chapter 12](../volume-087-microsegmentation-options/chapters/12-service-mesh-and-workload-identity.md)
summarizes service meshes including Linkerd, this volume is the **build**: 23 walkthrough labs that
stand up a real mesh, break it, and segment it.

Linkerd is deliberately the *simple* mesh, and the lab is built to compare directly with the Istio
volume that precedes it. The headline difference: **mTLS is automatic and needs no configuration** —
where Istio required a `PeerAuthentication` object, Linkerd encrypts and mutually-authenticates mesh
traffic the moment a workload is meshed. Its policy model is small and explicit — a `Server`, a
`MeshTLSAuthentication`, and an `AuthorizationPolicy` — and its `linkerd viz` extension gives
lightweight observability (`edges`, `stat`, `tap`).

The lab is also honest about the mesh boundary, exactly as the Istio lab is: a mesh secures only what
is *in* the mesh, so the un-meshed PLC needs a CNI network policy beneath it. Running Linkerd and a
CNI policy engine together is the standard production pattern.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Host Preparation](chapters/02-host-preparation.md) | 2.1–2.2 |
| 03 | [Building the Cluster and Installing Linkerd](chapters/03-installing-linkerd.md) | 3.1–3.3 |
| 04 | [Deploying the Workloads](chapters/04-deploying-the-workloads.md) | 4.1–4.3 |
| 05 | [The Flat Mesh and Lateral Movement](chapters/05-flat-mesh-and-lateral-movement.md) | 5.1–5.3 |
| 06 | [Automatic mTLS and Identity](chapters/06-automatic-mtls-and-identity.md) | 6.1–6.3 |
| 07 | [Server and AuthorizationPolicy](chapters/07-server-and-authorizationpolicy.md) | 7.1–7.3 |
| 08 | [The Mesh Boundary](chapters/08-the-mesh-boundary.md) | 8.1–8.3 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

## What you will be able to do

- Install Linkerd and mesh workloads with per-workload ServiceAccount identities.
- Confirm mesh traffic is mTLS with zero configuration, using `linkerd viz`.
- Authorize traffic by identity with `Server` + `MeshTLSAuthentication` + `AuthorizationPolicy`.
- Set a namespace default-deny guardrail and understand the health-probe caveat.
- Explain the mesh boundary and why meshes are paired with CNI network policy.

## Prerequisites

- A Linux host — an Ubuntu 22.04 VM, a cloud VM, or WSL2 — with 2 vCPU, 4 GB RAM, 20 GB disk.
- Docker, `kind`, `kubectl`, and the `linkerd` CLI (all free; installed in Chapter 02).

## See also

- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab pairs with.
- [Volume CIII — Istio](../volume-103-istio-lab/README.md) — the heavier mesh this volume compares against.
- [Volume CI — Calico](../volume-101-calico-lab/README.md) and [Volume CII — Cilium](../volume-102-cilium-lab/README.md) — the CNI policy engines a mesh is paired with.
