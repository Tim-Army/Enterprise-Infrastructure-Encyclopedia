# Chapter 01: Lab Overview and Topology

## Learning Objectives

- State what this lab builds and how Linkerd differs from Istio.
- Read the mesh topology and each workload's identity.
- Assemble the bill of materials before starting.
- Explain Linkerd's headline: automatic, zero-config mutual TLS.

## How to Use This Guide

### What this lab is

This is a self-contained, build-it-yourself Kubernetes microsegmentation lab, and it is the second **service mesh** in the series. Like Istio, Linkerd puts a proxy beside each workload and secures service-to-service traffic with identity and mTLS. Unlike Istio, Linkerd is deliberately **small and opinionated** — a Rust micro-proxy, a handful of resources, and almost no knobs. Linkerd is open source, so this volume is **single-track**.

The lab builds the same shape as the Istio lab — meshed workloads plus one un-meshed PLC — so you can compare the two meshes directly. Three ideas define Linkerd's model:

- **Automatic mTLS, zero configuration.** The single biggest difference from Istio: the moment a workload is meshed, all of its mesh traffic is **mutually authenticated and encrypted** — automatically, with nothing to enable. There is no `PeerAuthentication` object to write; mTLS is simply on.
- **Identity from the ServiceAccount.** Each workload's identity is issued as a TLS certificate derived from its Kubernetes **ServiceAccount** — for example `sa-web.dc.serviceaccount.identity.linkerd.cluster.local`. Authorization is on this authenticated identity.
- **A small, explicit policy model.** Segmentation uses three resources: a **`Server`** (a port on a set of pods), a **`MeshTLSAuthentication`** (a set of authorized identities), and an **`AuthorizationPolicy`** binding them. Defining a `Server` flips that port to **deny by default**; you then authorize the identities that may reach it.

### Topology

A single-node `kind` cluster running Linkerd, with meshed workloads across two namespaces plus one un-meshed PLC.

![Lab topology: a single Linux host running a kind Kubernetes cluster with Linkerd. Meshed workloads (each with a Linkerd micro-proxy and a ServiceAccount identity) are web, api, and db in namespace dc, and hmi in namespace ot; the plc in ot is un-meshed. Automatic mTLS secures mesh traffic; a Server plus AuthorizationPolicy allows web to db and api by identity and denies the hmi-to-db lateral movement.](../../../diagrams/volume-104-linkerd-lab/chapter-01-lab-topology.svg)

*Figure 1-1. The workloads this lab builds: `web`, `api`, and `db` in namespace `dc` and `hmi` in namespace `ot` are meshed, each with a Linkerd proxy and a ServiceAccount identity; `plc` in `ot` is un-meshed. Linkerd secures mesh traffic with automatic mTLS and authorizes by identity — permitting web→db and web→api and hmi→plc, and denying the hmi→db lateral movement.*

A text-only rendering:

```text
  +------------------------------------------------------------------+
  |  Single Linux host — Docker + kind + kubectl + linkerd           |
  |  +------------------------------------------------------------+  |
  |  |  kind Kubernetes cluster · Linkerd control plane           |  |
  |  |                                                            |  |
  |  |   namespace: dc  (linkerd.io/inject: enabled)              |  |
  |  |   +-----------+   +-----------+   +-----------+             |  |
  |  |   | web       |==>| api       |   | db        |            |  |
  |  |   | +proxy    |   | +proxy    |   | +proxy    |            |  |
  |  |   | sa-web    |   | sa-api    |   | sa-db     |            |  |
  |  |   +-----------+   +-----------+   +-----------+            |  |
  |  |     \\ automatic mTLS + Server/AuthorizationPolicy //      |  |
  |  |                                                            |  |
  |  |   namespace: ot                                            |  |
  |  |   +-----------+                    +-----------+            |  |
  |  |   | hmi       | --502--> (egress)  | plc       |  NOT      |  |
  |  |   | +proxy    |    X hmi->db        | no proxy  |  meshed   |  |
  |  |   | sa-hmi    |    (denied)         | app=plc   |           |  |
  |  |   +-----------+                    +-----------+            |  |
  |  +------------------------------------------------------------+  |
  +------------------------------------------------------------------+
```

### Bill of materials

| Item | Where | Notes |
|:---|:---|:---|
| A Linux host | Ubuntu 22.04 VM, cloud VM, or WSL2 | 2 vCPU, 4 GB RAM, 20 GB disk |
| Docker, kind, kubectl | as in the earlier Kubernetes labs | Kubernetes on one host |
| linkerd CLI | `linkerd.io` (`run.linkerd.io/install`) | installs Linkerd and inspects the mesh |

All free and open source. Where **Buoyant Enterprise for Linkerd** adds features (FIPS builds, lifecycle automation, a hosted control plane), those are called out as an **Enterprise note**.

### Time and effort

| Part | Content | Approximate time |
|:---|:---|:---|
| A | Host preparation | 30–45 min |
| B | Install Linkerd and linkerd viz | 20 min |
| C | Deploy meshed workloads | 20 min |
| D | Flat mesh and lateral movement | 20 min |
| E | Automatic mTLS and identity | 40 min |
| F | Server / AuthorizationPolicy and the mesh boundary | 80 min |
| G | Operations, troubleshooting, teardown | 30 min |

Budget an evening.

## Conventions

| Convention | Meaning |
|:---|:---|
| `$` prefix | Run on the Linux host as your normal user |
| `kubectl` / `linkerd` | Run against the kind cluster from the host |
| **Enterprise note** | A capability that needs Buoyant Enterprise, described but not built |

Every exercise follows the same shape: **Objective**, **Walkthrough**, **Expected result**, **Negative test**, **Rollback**.

## Summary and Completion Checklist

- [ ] Topology (meshed workloads, identities, the un-meshed PLC) understood.
- [ ] The three Linkerd ideas — automatic mTLS, ServiceAccount identity, Server/AuthorizationPolicy — understood.
- [ ] Bill of materials downloaded.
- [ ] Host with 2 vCPU / 4 GB RAM ready.
