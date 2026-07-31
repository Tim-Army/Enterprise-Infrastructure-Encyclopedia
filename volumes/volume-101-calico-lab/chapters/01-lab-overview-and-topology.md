# Chapter 01: Lab Overview and Topology

## Learning Objectives

- State what this lab builds and why it needs no two-track structure.
- Read the Kubernetes topology: namespaces, pods, labels, and the flows between them.
- Assemble the bill of materials before starting.
- Explain how Calico enforces policy in the cluster and beyond it.

## How to Use This Guide

### What this lab is

This is a self-contained, build-it-yourself microsegmentation lab, and it differs from the commercial-platform labs in this series in one important way: **Calico is open source and free**, so there is nothing to simulate. You build a real Kubernetes cluster, deploy a real application, break it, and segment it with real Calico policy — every command runs, every result is genuine. There is no "Track 2"; this whole volume is Track 1.

You will build a small Kubernetes cluster on a single Linux host, deploy a four-workload application, prove that a default Kubernetes network lets any pod reach any other (lateral movement), and then contain it with **Calico**: Kubernetes **NetworkPolicy**, Calico's extended **GlobalNetworkPolicy** and **tiers**, and Calico **HostEndpoints** for the world beyond pods.

The workloads are intentionally heterogeneous — a web tier, a database, an operator client, and an unpatchable "PLC" — because that mix is the reason microsegmentation exists, in Kubernetes as much as on VMs.

### Why no two tracks

Every other lab in this microsegmentation series is written on two tracks because the product is commercial and cannot be fully reproduced without a license. Calico has no such constraint: the open-source project **is** the enforcement engine. So you install the real thing and use it directly. Where Calico's commercial edition (Calico Enterprise / Calico Cloud) adds features the open-source project lacks — flow visualization UI, hierarchical RBAC at scale, DNS policy — those are called out as **Enterprise note** rather than reproduced.

### Topology

A single-node Kubernetes cluster (built with `kind` — Kubernetes in Docker) running the Calico CNI, with four workloads across two namespaces.

![Lab topology: a single Linux host running a kind Kubernetes cluster with the Calico CNI. Two namespaces, dc and ot, hold four pods — web (nginx), db (postgres), hmi (client), and plc (Modbus) — with the two legitimate flows (web to db on 5432, hmi to plc on 502) allowed and the compromised-hmi-to-db lateral movement denied by Calico policy.](../../../diagrams/volume-101-calico-lab/chapter-01-lab-topology.svg)

*Figure 1-1. The four-pod application this lab builds: namespace `dc` holds `web` (nginx) and `db` (PostgreSQL); namespace `ot` holds `hmi` (operator client) and `plc` (Modbus). Calico policy permits web→db on 5432 and hmi→plc on 502 and denies everything else, including the compromised-hmi-to-db lateral movement. Calico also protects the cluster node itself with a HostEndpoint.*

A text-only rendering of the same topology follows for reference:

```text
  +------------------------------------------------------------------+
  |  Single Linux host (Ubuntu 22.04 VM, cloud VM, or WSL2)          |
  |  Docker + kind + kubectl + calicoctl                            |
  |                                                                  |
  |  +------------------------------------------------------------+  |
  |  |  kind Kubernetes cluster   (CNI = Calico)                  |  |
  |  |                                                            |  |
  |  |   namespace: dc                    namespace: ot           |  |
  |  |   +----------------+               +--------------------+  |  |
  |  |   | web (nginx)    |  --5432-->    | hmi (client)       |  |  |
  |  |   | app=web        |     |         | app=hmi            |  |  |
  |  |   +----------------+     |         +---------+----------+  |  |
  |  |                          v                   | --502-->     |  |
  |  |   +----------------+  [ db ]                  v              |  |
  |  |   | db (postgres)  |<-------- app=web    +----+-----------+  |  |
  |  |   | app=db :5432   |    X  hmi->db       | plc (modbus)   |  |  |
  |  |   +----------------+   DENIED (lateral)  | app=plc :502   |  |  |
  |  |                                          +----------------+  |  |
  |  +------------------------------------------------------------+  |
  |    Calico HostEndpoint protects the node itself                  |
  +------------------------------------------------------------------+
```

The two legitimate flows are `web → db:5432` and `hmi → plc:502`. Everything else — most importantly `hmi → db:5432` (the lateral-movement path) — is denied once Calico policy is in force.

### Bill of materials

| Item | Where | Notes |
|:---|:---|:---|
| A Linux host | Ubuntu 22.04 VM (VMware Workstation), a cloud VM, or WSL2 | 2 vCPU, 4 GB RAM, 20 GB disk is plenty |
| Docker Engine | `get.docker.com` | `kind` runs the cluster as containers |
| kind | `kind.sigs.k8s.io` | Kubernetes in Docker — a full cluster on one host |
| kubectl | Kubernetes release | the cluster CLI |
| calicoctl | Calico release | Calico's CLI for GlobalNetworkPolicy, HostEndpoints, and `NetworkSet` |
| Calico manifests | `docs.tigera.io` | the open-source CNI and policy engine |

All of it is free and open source. Total download is a few hundred megabytes of container images.

### Time and effort

| Part | Content | Approximate time |
|:---|:---|:---|
| A | Host preparation (Docker, kind, kubectl, calicoctl) | 30–45 min |
| B | Build the cluster with Calico | 20 min |
| C | Deploy the four workloads | 20 min |
| D | The flat cluster and lateral movement | 20 min |
| E | NetworkPolicy and the Calico model | 60 min |
| F | GlobalNetworkPolicy, tiers, and HostEndpoints | 90 min |
| G | Operations, troubleshooting, teardown | 30 min |

Budget an evening. Unlike the VM-based labs in this series, there are no long OS installs — containers start in seconds.

## Conventions

| Convention | Meaning |
|:---|:---|
| `$` prefix | Run on the **Linux host** as your normal user |
| `#` prefix | Run on the Linux host as root (or with `sudo`) |
| `kubectl ...` | Run against the kind cluster from the host |
| **Enterprise note** | A capability that needs Calico Enterprise/Cloud, described but not built |

Every exercise follows the same five-part shape: **Objective**, **Walkthrough**, **Expected result**, **Negative test**, **Cleanup**. Do not skip the negative tests — proving a thing is *blocked* is the entire product.

## Summary and Completion Checklist

- [ ] Topology (namespaces, pods, labels, flows) understood.
- [ ] Why this volume is single-track (open source) understood.
- [ ] Bill of materials downloaded.
- [ ] Host with 2 vCPU / 4 GB RAM ready.
