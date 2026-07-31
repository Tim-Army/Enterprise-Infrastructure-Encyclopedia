# Chapter 01: Lab Overview and Topology

## Learning Objectives

- State what this lab builds and why it is single-track.
- Read the mesh topology: which workloads are in the mesh, and their identities.
- Assemble the bill of materials before starting.
- Explain how Istio differs from a CNI: mTLS, cryptographic identity, and L7 authorization.

## How to Use This Guide

### What this lab is

This is a self-contained, build-it-yourself Kubernetes microsegmentation lab, and it segments at a different layer than the two that precede it. Calico and Cilium are **CNIs** — they filter the network. **Istio is a service mesh** — it puts an **Envoy proxy** alongside each workload and secures **service-to-service** communication with **mutual TLS** and identity-based authorization. Istio is open source, so this volume is **single-track**: you install and use the real thing.

Three ideas define the model and shape the lab:

- **mTLS everywhere.** Meshed workloads talk over automatic **mutual TLS**. Traffic is encrypted, and — crucially — each side **cryptographically proves its identity** with a certificate. An attacker cannot simply send packets from an allowed IP; it must present a valid identity.
- **Cryptographic workload identity (SPIFFE).** Each workload's identity is a **SPIFFE ID** derived from its Kubernetes **ServiceAccount** — for example `spiffe://cluster.local/ns/dc/sa/sa-web`. Policy authorizes on this *authenticated principal*, not on an IP or a label an attacker could imitate.
- **AuthorizationPolicy.** Istio's `AuthorizationPolicy` authorizes traffic by source **principal**, namespace, and **Layer 7** attributes (HTTP method, path, headers, JWT claims), enforced right at the destination's sidecar.

### Topology

A single-node `kind` cluster running Istio, with meshed workloads across two namespaces — plus one deliberately **un-meshed** device (the PLC) to show the mesh's boundary.

![Lab topology: a single Linux host running a kind Kubernetes cluster with Istio. Meshed workloads (each with an Envoy sidecar and a SPIFFE identity from its ServiceAccount) are web, api, and db in namespace dc, and hmi in namespace ot; the plc in ot is not meshed. mTLS secures mesh traffic; AuthorizationPolicy allows web to api and db by principal, allows hmi to plc, and denies the hmi-to-db lateral movement.](../../../diagrams/volume-103-istio-lab/chapter-01-lab-topology.svg)

*Figure 1-1. The workloads this lab builds: `web`, `api`, and `db` in namespace `dc` and `hmi` in namespace `ot` are in the mesh, each with an Envoy sidecar and a SPIFFE identity from its ServiceAccount; `plc` in `ot` is un-meshed (an OT device that can run no sidecar). Istio secures mesh traffic with mTLS and authorizes by principal — permitting web→api (L7) and web→db (L4) and hmi→plc, and denying the hmi→db lateral movement because the HMI's principal is not authorized.*

A text-only rendering:

```text
  +------------------------------------------------------------------+
  |  Single Linux host — Docker + kind + kubectl + istioctl          |
  |  +------------------------------------------------------------+  |
  |  |  kind Kubernetes cluster · Istio control plane (istiod)    |  |
  |  |                                                            |  |
  |  |   namespace: dc  (istio-injection=enabled)                 |  |
  |  |   +-----------+   +-----------+   +-----------+             |  |
  |  |   | web       |==>| api       |   | db        |            |  |
  |  |   | +sidecar  |   | +sidecar  |   | +sidecar  |            |  |
  |  |   | sa-web    |   | sa-api    |   | sa-db     |            |  |
  |  |   +-----------+   +-----------+   +-----------+            |  |
  |  |        \\ mTLS + AuthorizationPolicy (by principal) //     |  |
  |  |                                                            |  |
  |  |   namespace: ot  (istio-injection=enabled)                 |  |
  |  |   +-----------+                    +-----------+            |  |
  |  |   | hmi       | --502--> (egress)  | plc       |  NOT      |  |
  |  |   | +sidecar  |    X hmi->db        | no sidecar|  meshed   |  |
  |  |   | sa-hmi    |    (denied)         | app=plc   |           |  |
  |  |   +-----------+                    +-----------+            |  |
  |  +------------------------------------------------------------+  |
  +------------------------------------------------------------------+
```

### Bill of materials

| Item | Where | Notes |
|:---|:---|:---|
| A Linux host | Ubuntu 22.04 VM, cloud VM, or WSL2 | 2 vCPU, 4 GB RAM, 20 GB disk |
| Docker, kind, kubectl | as in the Calico/Cilium labs | Kubernetes on one host |
| istioctl | `istio.io` download | installs Istio and inspects the mesh |

All free and open source. Where **commercial meshes/managed Istio** (for example an enterprise distribution) add features, those are called out as an **Enterprise note**.

### Time and effort

| Part | Content | Approximate time |
|:---|:---|:---|
| A | Host preparation | 30–45 min |
| B | Build the cluster and install Istio | 25 min |
| C | Deploy meshed workloads with identities | 25 min |
| D | Flat mesh and lateral movement | 20 min |
| E | mTLS and workload identity | 45 min |
| F | AuthorizationPolicy (L4 and L7) and the mesh boundary | 90 min |
| G | Operations, troubleshooting, teardown | 30 min |

Budget an evening.

## Conventions

| Convention | Meaning |
|:---|:---|
| `$` prefix | Run on the Linux host as your normal user |
| `kubectl` / `istioctl` | Run against the kind cluster from the host |
| **Enterprise note** | A capability that needs a commercial mesh, described but not built |

Every exercise follows the same shape: **Objective**, **Walkthrough**, **Expected result**, **Negative test**, **Cleanup**.

## Summary and Completion Checklist

- [ ] Topology (meshed workloads, identities, the un-meshed PLC) understood.
- [ ] The three Istio ideas — mTLS, SPIFFE identity, AuthorizationPolicy — understood.
- [ ] Bill of materials downloaded.
- [ ] Host with 2 vCPU / 4 GB RAM ready.
