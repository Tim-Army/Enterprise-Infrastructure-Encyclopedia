# Chapter 03: NCP-MCI — Multicloud Infrastructure

## Learning Objectives

- Explain what the NCP-MCI certifies and its target role.
- Summarize the six blueprint sections.
- Manage clusters, storage, and networking on Nutanix.
- Analyze performance and remediate alerts; deploy and configure VMs.
- Complete a per-section walkthrough for each NCP-MCI domain.

## Theory and Architecture

The **Nutanix Certified Professional — Multicloud Infrastructure (NCP-MCI)** validates
administering a Nutanix cluster — the flagship professional credential (current
versions **6.10** and **7.5**; ~**120 minutes**). Its blueprint has **six sections**:
**Manage Cluster, Nodes, and Features**; **Manage Cluster Storage**; **Configure
Cluster Networking and Network Security**; **Analyze and Remediate Performance
Issues**; **Configure, Analyze, and Remediate Alerts and Events**; and **Manage VM
Deployment and Configuration**.

## Design Considerations

The administrator manages **nodes/features** (add/remove, LCM), **storage** (containers,
compression/dedup/erasure coding), **networking** (AHV bridges, VLANs, microseg via
Flow), **performance** (analysis and remediation), **alerts/events**, and **VM**
lifecycle. Storage containers and Flow network security are recurring themes.

## Implementation and Automation

The labs use `acli`/`ncli` and Prism for each section — cluster/nodes, storage,
networking, performance, alerts, and VM management.

## Validation and Troubleshooting

Confirm the blueprint before studying:

```text
nutanix.com > NCP-MCI blueprint (6 sections):
  1 Manage Cluster, Nodes, and Features  2 Manage Cluster Storage
  3 Configure Cluster Networking and Network Security
  4 Analyze and Remediate Performance Issues
  5 Configure, Analyze, and Remediate Alerts and Events
  6 Manage VM Deployment and Configuration
```

Common pitfalls: enabling **dedup** on unsuitable workloads; and flat networks with no
**Flow** microsegmentation.

## Security and Best Practices

Right-size **storage container** efficiencies per workload, segment with **Flow**,
baseline and remediate **performance**, act on **alerts**, and standardize **VM**
builds. Drive upgrades with **LCM** and protect data with snapshots/replication.

## References and Knowledge Checks

- nutanix.com: NCP-MCI blueprint guide; AOS storage, AHV networking, and Flow docs.

**Knowledge checks**

1. When is deduplication appropriate on a container?
2. What does Nutanix Flow provide?
3. How do you baseline VM performance?

## Hands-On Lab

Per-section walkthroughs — NCP-MCI. **Shared prerequisites** — a cluster or Community
Edition with `acli`/`ncli`. **Cost:** none.

### Lab 3.1 — Manage cluster, nodes, and features

**Objective:** Review cluster resiliency and nodes.

```bash
ncli cluster get-domain-fault-tolerance-status type=node
ncli host list | grep -Ei 'Id|Name|Status'
```

**Expected result:** node fault-tolerance status and host inventory — the cluster/
nodes section.

**Negative test:** run a cluster at RF1; **redundancy factor 2+** protects against a
node/disk failure — verify resiliency.

**Cleanup:** none (read-only).

### Lab 3.2 — Manage cluster storage

**Objective:** Create a storage container with an efficiency setting.

```bash
ncli container create name=lab-ctr sp-name=SP01 \
  finger-print-on-write=true on-disk-dedup=OFF compression-enabled=true
ncli container ls name=lab-ctr
```

**Expected result:** a container with **compression** enabled — the storage section.

**Negative test:** enable **on-disk dedup** for a VDI-unfriendly workload; match the
efficiency to the data or you waste CPU/RAM.

**Cleanup:** `ncli container remove name=lab-ctr`.

### Lab 3.3 — Configure cluster networking and security

**Objective:** Create an AHV VLAN network.

```bash
acli net.create lab-net vlan=42
acli net.list | grep lab-net
# Flow (microsegmentation) enforces east-west security policies on categories.
```

**Expected result:** a VLAN-backed AHV network (and the Flow concept) — the
networking/security section.

**Negative test:** put all VMs on one flat network; use **VLANs + Flow** to segment.

**Cleanup:** `acli net.delete lab-net`.

### Lab 3.4 — Analyze and remediate performance issues

**Objective:** Read VM/cluster performance stats.

```bash
ncli cluster get-stats
# Prism > Analysis: build charts for latency, IOPS, CPU/memory to find the bottleneck.
```

**Expected result:** cluster performance stats to locate a **bottleneck** — the
performance section.

**Negative test:** add hardware blindly; **analyze first** (CPU vs storage vs network)
then remediate the real bottleneck.

**Cleanup:** none (read-only).

### Lab 3.5 — Configure, analyze, and remediate alerts and events

**Objective:** Review and acknowledge alerts.

```bash
ncli alert ls | head
# ncli alert acknowledge id=<alert-id>   (after triage)
```

**Expected result:** current alerts for triage — the alerts/events section.

**Negative test:** disable noisy alerts wholesale; **tune thresholds** and remediate
root cause instead of muting.

**Cleanup:** none (read-only unless you acknowledge).

### Lab 3.6 — Manage VM deployment and configuration

**Objective:** Create and configure a VM.

```bash
acli vm.create lab-vm memory=2G num_vcpus=2
acli vm.disk_create lab-vm create_size=20G container=lab-ctr
acli vm.nic_create lab-vm network=lab-net
acli vm.on lab-vm
```

**Expected result:** a running VM with disk and NIC — the VM deployment section.

**Negative test:** oversize every VM; right-size vCPU/RAM to avoid contention.

**Cleanup:** `acli vm.off lab-vm && acli vm.delete lab-vm`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The NCP-MCI certifies administering a Nutanix cluster across six sections: cluster/
nodes/features, storage, networking and security (Flow), performance, alerts/events,
and VM deployment — with `acli`/`ncli` and Prism.

- [ ] I can verify cluster resiliency and manage nodes.
- [ ] I can create storage containers with the right efficiencies.
- [ ] I can build VLAN networks and describe Flow.
- [ ] I can analyze performance, triage alerts, and deploy VMs.
- [ ] I completed Labs 3.1–3.6 including each negative test.
