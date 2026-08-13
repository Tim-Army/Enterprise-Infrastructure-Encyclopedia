# Chapter 02: NCA — Nutanix Certified Associate

## Learning Objectives

- Explain what the NCA certifies and its target audience.
- Summarize the four blueprint sections.
- Recognize Nutanix solutions/tools and perform platform administration.
- Configure and maintain a cluster and monitor platform health.
- Complete a per-section walkthrough for each NCA domain.

## Theory and Architecture

The **Nutanix Certified Associate (NCA)** validates foundational knowledge of the
Nutanix Cloud Platform — the entry credential (current versions **6.10** and **7.5**;
**50 questions / 90 minutes**). Its blueprint has **four sections**: **Recognize
Nutanix Solutions and Tools**, **Describe Nutanix Platform Administration**,
**Describe Cluster Configuration and Maintenance**, and **Understand Platform Health
and Monitoring**.

## Design Considerations

The associate understands the **portfolio** (NCI/AHV/AOS/Prism plus Files, Objects,
NDB, NC2) and **tools** (Prism Element/Central, `ncli`/`acli`), performs basic
**administration** (VMs, networking, storage, licensing), knows **cluster** options
and maintenance (LCM upgrades), and reads **health/alerts/performance**.

## Implementation and Automation

The labs use `ncli`/`acli` and Prism for each section — solutions/tools,
administration, cluster maintenance, and health monitoring.

## Validation and Troubleshooting

Confirm the blueprint before studying:

```text
nutanix.com > NCA blueprint (50 Q / 90 min):
  1 Recognize Nutanix Solutions and Tools
  2 Describe Nutanix Platform Administration
  3 Describe Cluster Configuration and Maintenance
  4 Understand Platform Health and Monitoring
```

Common pitfalls: confusing **Prism Element** (per-cluster) with **Prism Central**
(multi-cluster); and skipping **LCM** for upgrades.

## Security and Best Practices

Learn the portfolio and tools, use **Prism Central** for fleet management, drive
upgrades through **LCM**, and monitor with the **health dashboard** and alerts.
Practice everything on **Community Edition**.

## References and Knowledge Checks

- nutanix.com: NCA blueprint guide; Prism, AOS, and AHV administration docs.

**Knowledge checks**

1. What is the difference between Prism Element and Prism Central?
2. What does LCM manage?
3. Where do you see cluster health at a glance?

## Hands-On Lab

Per-section walkthroughs — NCA. **Shared prerequisites** — a cluster or Community
Edition with `ncli`/`acli`. **Cost:** none.

### Lab 2.1 — Recognize Nutanix solutions and tools

**Objective:** Identify AOS/AHV versions and the hypervisor.

```bash
ncli cluster info | grep -Ei 'version|hypervisor'
acli host.list
```

**Expected result:** the **AOS version**, **AHV** hypervisor, and host list — the
solutions/tools section.

**Negative test:** assume ESXi; `acli host.list` shows the actual hypervisor — Nutanix
runs **AHV** by default.

**Rollback:** none (read-only).

### Lab 2.2 — Describe Nutanix platform administration

**Objective:** List VMs and networks.

```bash
acli vm.list
acli net.list
```

**Expected result:** the cluster's **VMs and virtual networks** — the platform
administration section.

**Negative test:** manage VMs on the host with libvirt directly; use **`acli`/Prism**
so AOS tracks state consistently.

**Rollback:** none (read-only).

### Lab 2.3 — Describe cluster configuration and maintenance

**Objective:** Review cluster nodes and check upgrades (LCM).

```bash
ncli host list | grep -Ei 'Name|Status'
# LCM (Life Cycle Manager) inventories and upgrades firmware/software from Prism.
ncli cluster get-domain-fault-tolerance-status type=node
```

**Expected result:** node list and the cluster's **fault-tolerance** status — the
configuration/maintenance section.

**Negative test:** upgrade firmware by hand; **LCM** orchestrates it safely — use it.

**Rollback:** none (read-only).

### Lab 2.4 — Understand platform health and monitoring

**Objective:** Read health checks and alerts.

```bash
ncli health-check list | head
ncli alert ls | head
```

**Expected result:** health-check results and current **alerts** — the health/
monitoring section.

**Negative test:** wait for users to report issues; the **health dashboard/alerts**
surface problems proactively — watch them.

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The NCA certifies foundational Nutanix knowledge across four sections: solutions and
tools, platform administration, cluster configuration and maintenance, and platform
health and monitoring — using Prism and `ncli`/`acli` on Community Edition.

- [ ] I can identify AOS/AHV and the tools.
- [ ] I can list VMs and networks.
- [ ] I can review nodes, LCM, and fault tolerance.
- [ ] I can read health checks and alerts.
- [ ] I completed Labs 2.1–2.4 including each negative test.
