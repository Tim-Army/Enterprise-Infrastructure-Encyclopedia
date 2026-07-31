# Chapter 01: Lab Overview and Topology

## Learning Objectives

- State what this lab builds and how Consul differs from Istio and Linkerd.
- Read the topology, including the workloads meshed on Kubernetes and the one beyond it.
- Assemble the bill of materials before starting.
- Explain Consul's model: service intentions, mTLS, and one mesh across VMs and Kubernetes.

## How to Use This Guide

### What this lab is

This is a self-contained, build-it-yourself Kubernetes microsegmentation lab, and it is the third **service mesh** in the series — but the one with the widest reach. Istio and Linkerd mesh Kubernetes pods. **Consul** meshes Kubernetes pods **and** services running on **VMs and bare metal**, in a single mesh governed by a single policy model. That multi-platform span is Consul's defining trait, and it is the reason many organizations with a mix of Kubernetes and long-lived VMs choose it. Consul is open source, so this volume is **single-track**.

Three ideas define the model:

- **Service intentions.** Consul's authorization primitive is simple and readable: an **intention** declares that source service *A* may (or may not) talk to destination service *B*. Segmentation is a list of "who may call whom," by **service identity**, not by IP — and it applies identically to a pod or a VM.
- **Automatic mTLS via Connect.** Consul Connect injects an Envoy sidecar and secures service-to-service traffic with **mutual TLS** and a **SPIFFE** identity, exactly as the other meshes do.
- **One mesh, many platforms.** A service on a VM runs a Consul dataplane, joins the same mesh, and is governed by the same intentions as a pod. This lab builds the Kubernetes half hands-on and shows how the VM half joins.

### Topology

A single-node `kind` cluster running Consul, with meshed workloads plus one un-meshed PLC — and a look at how a non-Kubernetes service would join the same mesh.

![Lab topology: a single Linux host running a kind Kubernetes cluster with HashiCorp Consul. Meshed services (each with a Consul Connect sidecar and a SPIFFE identity) are web, api, and db; the operator hmi is meshed; the plc is un-meshed. Service intentions authorize web to db and api and deny the hmi-to-db lateral movement; a VM service can join the same mesh governed by the same intentions.](../../../diagrams/volume-105-consul-lab/chapter-01-lab-topology.svg)

*Figure 1-1. The services this lab builds: `web`, `api`, `db`, and `hmi` are meshed on Kubernetes with Consul Connect (each with a sidecar and SPIFFE identity); `plc` is un-meshed. Consul service intentions permit web→db and web→api and deny the hmi→db lateral movement. Beyond Kubernetes, a service on a VM joins the same mesh and obeys the same intentions — Consul's multi-platform reach.*

A text-only rendering:

```text
  +------------------------------------------------------------------+
  |  Single Linux host — Docker + kind + kubectl + helm + consul     |
  |  +------------------------------------------------------------+  |
  |  |  kind Kubernetes cluster · Consul servers + Connect        |  |
  |  |                                                            |  |
  |  |   +-----------+   +-----------+   +-----------+             |  |
  |  |   | web       |==>| db        |   | api       |            |  |
  |  |   | +sidecar  |   | +sidecar  |   | +sidecar  |            |  |
  |  |   +-----------+   +-----------+   +-----------+            |  |
  |  |   | hmi       |    X hmi->db (intention: deny)             |  |
  |  |   | +sidecar  |                                            |  |
  |  |   +-----------+    | plc: no sidecar (un-meshed)           |  |
  |  |     \\ mTLS (Connect) + service intentions //              |  |
  |  +------------------------------------------------------------+  |
  |                                                                  |
  |   ...and beyond Kubernetes: a service on a VM runs a Consul      |
  |      dataplane, joins the SAME mesh, obeys the SAME intentions   |
  +------------------------------------------------------------------+
```

### Bill of materials

| Item | Where | Notes |
|:---|:---|:---|
| A Linux host | Ubuntu 22.04 VM, cloud VM, or WSL2 | 2 vCPU, 4 GB RAM (6 GB comfortable), 20 GB disk |
| Docker, kind, kubectl | as in the earlier Kubernetes labs | Kubernetes on one host |
| helm | `helm.sh` | installs Consul |
| consul CLI | `developer.hashicorp.com/consul` | inspect intentions and the catalog |

All free and open source. Where **Consul Enterprise (HashiCorp/IBM)** adds features (admin partitions, namespaces, network segments), those are called out as an **Enterprise note**.

### Time and effort

| Part | Content | Approximate time |
|:---|:---|:---|
| A | Host preparation | 30–45 min |
| B | Install Consul on Kubernetes | 25 min |
| C | Deploy meshed workloads | 20 min |
| D | Flat mesh and lateral movement | 20 min |
| E | mTLS and identity | 40 min |
| F | Service intentions and the multi-platform boundary | 90 min |
| G | Operations, troubleshooting, teardown | 30 min |

Budget an evening.

## Conventions

| Convention | Meaning |
|:---|:---|
| `$` prefix | Run on the Linux host as your normal user |
| `kubectl` / `consul` / `helm` | Run against the kind cluster from the host |
| **Enterprise note** | A capability that needs Consul Enterprise, described but not built |

Every exercise follows the same shape: **Objective**, **Walkthrough**, **Expected result**, **Negative test**, **Cleanup**.

## Summary and Completion Checklist

- [ ] Topology (meshed services, the un-meshed PLC, the VM reach) understood.
- [ ] The three Consul ideas — intentions, mTLS via Connect, one mesh across platforms — understood.
- [ ] Bill of materials downloaded.
- [ ] Host with 2 vCPU / 4 GB RAM (6 GB comfortable) ready.
