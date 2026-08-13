# Chapter 08: NCM-MCI — Master Multicloud Infrastructure

## Learning Objectives

- Explain what the NCM-MCI certifies and how it differs from NCP-MCI.
- Summarize the six blueprint sections.
- Perform advanced administration, storage, data protection, and security.
- Manage workloads and networking at the master level.
- Complete a per-section walkthrough for each NCM-MCI domain.

## Theory and Architecture

The **Nutanix Certified Master — Multicloud Infrastructure (NCM-MCI)** validates
advanced, scenario-based administration of Nutanix — the master credential (**90
questions / 180 minutes**; higher rigor than NCP-MCI). Its blueprint has **six
sections**: **Administration and Planning**, **Storage**, **Data Protection**,
**Security**, **Workload Management**, and **Networking**. The master exam emphasizes
applied problem-solving over recall.

## Design Considerations

The master administrator plans capacity and **administration** at scale, tunes
**storage** efficiencies and containers, designs **data protection** (protection
domains, async/NearSync/Metro, recovery plans), hardens **security** (Flow
microsegmentation, cluster lockdown, STIG), manages **workloads** (affinity, resource
governance), and designs **networking** (Flow Virtual Networking, VPCs). Data
protection and security depth separate master from professional.

## Implementation and Automation

The labs use `ncli`/`acli`/Prism for each section — administration, storage, data
protection, security, workload management, and networking.

## Validation and Troubleshooting

Confirm the blueprint before studying:

```text
nutanix.com > NCM-MCI blueprint (90 Q / 180 min, 6 sections):
  1 Administration and Planning  2 Storage  3 Data Protection
  4 Security  5 Workload Management  6 Networking
```

Common pitfalls: choosing **Metro** where async suffices (or vice versa); and leaving
**cluster lockdown**/microseg unconfigured.

## Security and Best Practices

Plan capacity and lifecycle, tune storage per workload, match **data-protection**
tier (async/NearSync/Metro) to RPO, harden with **Flow** + cluster lockdown + STIG,
govern **workloads** with affinity/QoS, and design **Flow Virtual Networking**. Test
recovery plans regularly.

## References and Knowledge Checks

- nutanix.com: NCM-MCI blueprint guide; data protection, Flow, and security docs.

**Knowledge checks**

1. When do you use Metro Availability versus NearSync?
2. What does cluster lockdown enforce?
3. How does workload affinity affect placement?

## Hands-On Lab

Per-section walkthroughs — NCM-MCI. **Shared prerequisites** — a cluster/CE with
`ncli`/`acli`. **Cost:** none.

### Lab 8.1 — Administration and planning

**Objective:** Assess capacity for planning.

```bash
ncli cluster get-stats | grep -Ei 'storage|cpu|memory'
ncli storagepool ls
```

**Expected result:** capacity/utilization data to plan growth — the administration/
planning section.

**Negative test:** plan by gut feel; base decisions on **utilization + runway** data.

**Rollback:** none (read-only).

### Lab 8.2 — Storage

**Objective:** Review container efficiencies.

```bash
ncli container ls | grep -Ei 'Name|Compression|Dedup|Erasure'
```

**Expected result:** per-container efficiency settings — the storage section.

**Negative test:** enable every efficiency everywhere; match **compression/dedup/EC-X**
to the workload.

**Rollback:** none (read-only).

### Lab 8.3 — Data protection

**Objective:** Review protection domains / recovery.

```bash
ncli protection-domain ls
# Async / NearSync / Metro replicate to a remote site per RPO; recovery plans orchestrate failover.
```

**Expected result:** configured protection domains (and the tiering model) — the data-
protection section.

**Negative test:** rely on local snapshots only; **replicate** to a remote site for
site-loss protection.

**Rollback:** none (read-only).

### Lab 8.4 — Security

**Objective:** Check cluster security posture.

```bash
ncli cluster get-hypervisor-security-config 2>/dev/null || ncli cluster info | grep -i lockdown
# Flow microsegmentation policies + cluster lockdown (key-based SSH) + STIG hardening.
```

**Expected result:** the security config (lockdown/hardening) and Flow concept — the
security section.

**Negative test:** leave password SSH enabled; **cluster lockdown** enforces key-based
access — enable it.

**Rollback:** none (read-only).

### Lab 8.5 — Workload management

**Objective:** Set a VM-host affinity policy.

```bash
acli vm.affinity_set lab-vm host_list=<host-uuid>
acli vm.get lab-vm | grep -i affinity
```

**Expected result:** an affinity policy pinning the VM — the workload-management
section.

**Negative test:** pin everything to one host; use affinity **sparingly** to avoid
imbalance.

**Rollback:** `acli vm.affinity_unset lab-vm`.

### Lab 8.6 — Networking

**Objective:** Review Flow Virtual Networking / VPCs.

```bash
acli net.list
# Flow Virtual Networking: overlay VPCs, subnets, and policies on Prism Central.
```

**Expected result:** networks and the **Flow Virtual Networking** model — the
networking section.

**Negative test:** stretch one flat L2 everywhere; **VPC overlays** isolate and scale
tenant networks.

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The NCM-MCI certifies master-level Nutanix administration across six sections:
administration/planning, storage, data protection (async/NearSync/Metro), security
(Flow, lockdown, STIG), workload management, and networking (Flow Virtual Networking).

- [ ] I can plan capacity from utilization data.
- [ ] I can tune storage and design data protection by RPO.
- [ ] I can harden security with lockdown and Flow.
- [ ] I can manage workload placement and VPC networking.
- [ ] I completed Labs 8.1–8.6 including each negative test.
