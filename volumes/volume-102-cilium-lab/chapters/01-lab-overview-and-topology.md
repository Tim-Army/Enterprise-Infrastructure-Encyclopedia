# Chapter 01: Lab Overview and Topology

## Learning Objectives

- State what this lab builds and why it is single-track.
- Read the Kubernetes topology, including the HTTP service used for Layer 7 policy.
- Assemble the bill of materials before starting.
- Explain what makes Cilium different: eBPF, identity, Hubble, and L7-aware policy.

## How to Use This Guide

### What this lab is

This is a self-contained, build-it-yourself Kubernetes microsegmentation lab. Like the Calico lab that precedes it, **Cilium is open source**, so this volume is **single-track** — you install and use the real thing; there is nothing to simulate.

You will build a real Kubernetes cluster on a single Linux host, deploy a small application, prove the cluster is flat, and then contain it with **Cilium** — and Cilium's differences from a traditional CNI are the point of the lab:

- **eBPF dataplane.** Cilium enforces policy in the Linux kernel with eBPF rather than iptables, and it identifies workloads by a **security identity** derived from their labels, not by IP.
- **Hubble.** Cilium's observability layer shows every flow — source and destination identity, verdict (forwarded/dropped), and even Layer 7 detail — with a CLI and a service-map UI.
- **L7-aware policy.** A `CiliumNetworkPolicy` can enforce at **Layer 7**: which **HTTP** methods and paths are allowed, which **DNS** names a workload may resolve and reach, and protocol-aware rules for Kafka and gRPC. This is the capability a Layer 3/4 firewall — and standard Kubernetes NetworkPolicy — cannot express.

### Topology

A single-node `kind` cluster running Cilium, with workloads across two namespaces. One extra workload — an HTTP API — exists specifically so you can enforce and observe **Layer 7** policy.

![Lab topology: a single Linux host running a kind Kubernetes cluster with the Cilium CNI (eBPF). Namespace dc holds web (client), db (PostgreSQL), and api (an HTTP service); namespace ot holds hmi (operator) and plc (Modbus). Cilium enforces L3/L4 policy (web to db on 5432, hmi to plc on 502) and L7 policy (web may only GET /get on the api), and denies the hmi-to-db lateral movement; Hubble observes every flow.](../../../diagrams/volume-102-cilium-lab/chapter-01-lab-topology.svg)

*Figure 1-1. The workloads this lab builds: namespace `dc` holds `web` (client), `db` (PostgreSQL :5432), and `api` (an HTTP service for the L7 demo); namespace `ot` holds `hmi` (operator) and `plc` (Modbus :502). Cilium permits web→db and hmi→plc at L3/L4, restricts web→api to specific HTTP methods and paths at L7, and denies the hmi→db lateral movement — with Hubble showing every verdict.*

A text-only rendering:

```text
  +------------------------------------------------------------------+
  |  Single Linux host — Docker + kind + kubectl + cilium + hubble   |
  |  +------------------------------------------------------------+  |
  |  |  kind Kubernetes cluster   (CNI = Cilium, eBPF dataplane)  |  |
  |  |                                                            |  |
  |  |   namespace: dc                       namespace: ot        |  |
  |  |   +----------+   +----------+          +----------+         |  |
  |  |   | web      |-->| db       |          | hmi      |         |  |
  |  |   | app=web  |   | app=db   |          | app=hmi  |         |  |
  |  |   +----+-----+   | :5432    |          +----+-----+         |  |
  |  |        |         +----------+               | --502-->      |  |
  |  |        | HTTP L7      ^  X hmi->db (denied)  v              |  |
  |  |        v              |                 +----+-----+        |  |
  |  |   +----------+        +---------------- | plc      |        |  |
  |  |   | api      |  GET /get  ALLOW         | app=plc  |        |  |
  |  |   | app=api  |  POST /post DENY (L7)    | :502     |        |  |
  |  |   | :8080    |                          +----------+        |  |
  |  |   +----------+                                              |  |
  |  |         Hubble observes every flow and verdict             |  |
  |  +------------------------------------------------------------+  |
  +------------------------------------------------------------------+
```

### Bill of materials

| Item | Where | Notes |
|:---|:---|:---|
| A Linux host | Ubuntu 22.04 VM, cloud VM, or WSL2 | 2 vCPU, 4 GB RAM, 20 GB disk |
| Docker | `get.docker.com` | kind runs the cluster |
| kind | `kind.sigs.k8s.io` | Kubernetes in Docker |
| kubectl | Kubernetes release | cluster CLI |
| cilium CLI | `github.com/cilium/cilium-cli` | installs Cilium, manages Hubble |
| hubble CLI | `github.com/cilium/hubble` | observe flows |

All free and open source. Where **Cilium Enterprise (Isovalent)** adds features (Tetragon runtime security at scale, a richer UI, mesh across clusters), those are called out as an **Enterprise note**.

### Time and effort

| Part | Content | Approximate time |
|:---|:---|:---|
| A | Host preparation | 30–45 min |
| B | Build the cluster with Cilium + Hubble | 25 min |
| C | Deploy the workloads | 20 min |
| D | Flat cluster and lateral movement | 20 min |
| E | Hubble and the identity model | 45 min |
| F | L3/L4 and L7 policy | 90 min |
| G | Operations, troubleshooting, teardown | 30 min |

Budget an evening.

## Conventions

| Convention | Meaning |
|:---|:---|
| `$` prefix | Run on the Linux host as your normal user |
| `kubectl` / `cilium` / `hubble` | Run against the kind cluster from the host |
| **Enterprise note** | A capability that needs Cilium Enterprise / Isovalent, described but not built |

Every exercise follows the same shape: **Objective**, **Walkthrough**, **Expected result**, **Negative test**, **Rollback**.

## Summary and Completion Checklist

- [ ] Topology (namespaces, pods, the HTTP api for L7) understood.
- [ ] The four Cilium differences — eBPF, identity, Hubble, L7 — understood.
- [ ] Bill of materials downloaded.
- [ ] Host with 2 vCPU / 4 GB RAM ready.
