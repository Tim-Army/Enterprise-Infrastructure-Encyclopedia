# Chapter 01: Lab Overview and Topology

![Lab topology: the same web/db/hmi three-tier estate built on AWS, Azure, and GCP, each segmented with its native primitive — AWS security groups plus a stateless NACL, Azure NSG rules by Application Security Group, and GCP firewall rules by service account. In every cloud web-to-db:5432 is allowed and the hmi-to-db lateral flow is denied by identity.](../../../diagrams/volume-106-cloud-native-segmentation-lab/chapter-01-lab-topology.svg)

*Figure 1-1. One three-tier estate, three native segmentation models. The legitimate web to database flow on 5432 stays open while the operator's lateral path to the database is denied by identity on each cloud.*

**Host setup — creating these VMs on your hypervisor.** The per-hypervisor steps to create each VM (install from an ISO or boot a cloud image), size it, and map its NICs to the segments in this lab are the same for every hypervisor and are collected once in the Master Appendices: [Deploying Lab Appliance Images on Each Hypervisor](../../volume-997-master-appendices/chapters/73-appendix-deploying-lab-appliance-images-on-each-hypervisor.md) — Proxmox, KVM, ESXi/vSphere, Workstation/Fusion, VirtualBox, Hyper-V, EVE-NG, GNS3, containerlab, Nutanix AHV, and Xen.

## Learning Objectives

- State what this lab builds and why it needs no agent, cluster, or mesh.
- Read the three-tier topology reproduced identically on AWS, Azure, and GCP.
- Understand the native segmentation primitive of each cloud.
- Internalize the cost and teardown discipline before you create anything.

## How to Use This Guide

### What this lab is

This is a self-contained, build-it-yourself microsegmentation lab that uses **only the cloud providers' own native network controls** — no host agent, no Kubernetes CNI, no service mesh. Every major cloud already ships a microsegmentation primitive as part of the subscription; the skill is knowing each one's model and its sharp edges. This volume builds the **same three-tier estate on all three clouds** so you can segment it natively on whichever you use, and compare the models directly. The clouds are real accounts, so this volume is **single-track** — but it costs real (small) money, so **cost and teardown discipline is part of the lab, not an afterthought**.

You will build a web tier, a database, and an operator workstation in each cloud, prove that a permissive default network lets the operator reach the database (lateral movement), and then contain it with the cloud's native controls.

### The three native primitives

| Cloud | Primary primitive | Model | Grouping | Deny? |
|:---|:---|:---|:---|:---|
| **AWS** | **Security Group** (SG) | Stateful, attached to an ENI/instance | Reference another SG as source | Allow-only (implicit deny) |
| **AWS** | **Network ACL** (NACL) | Stateless, attached to a subnet | CIDR ranges | Allow **and** deny, numbered |
| **Azure** | **Network Security Group** (NSG) | Stateful, on a subnet or NIC | **Application Security Group** (ASG) | Allow **and** deny, priority-ordered |
| **GCP** | **VPC firewall rule** | Stateful, network-wide | **Network tags** and **service accounts** | Allow **and** deny, priority-ordered |

Two ideas recur and are worth holding on to:

- **Group by identity, not IP.** The best clouds let you write rules against a *group* — an AWS SG, an Azure ASG, a GCP tag or service account — so the rule reads "web may reach database" and keeps working as instances scale and re-address. Writing rules against raw IPs is the cloud version of the mistake every other lab in this series warns about.
- **Stateful vs stateless matters.** SGs, NSGs, and GCP firewall rules are **stateful** (return traffic is automatic). AWS **NACLs are stateless** (you must allow the return path explicitly) — the single most common cloud-firewall mistake.

### Topology (identical on each cloud)

```text
   VPC / VNet / VPC  (10.10.0.0/16)
   +-------------------------------------------------+
   |  app-subnet 10.10.1.0/24    db-subnet 10.10.2.0/24  |
   |   +---------+                 +---------+          |
   |   | web     |  --5432-->      | db      |          |
   |   | app tier|                 | :5432   |          |
   |   +---------+                 +---------+          |
   |                                   ^                |
   |  mgmt-subnet 10.10.3.0/24         | X  hmi->db     |
   |   +---------+                     |   (lateral,    |
   |   | hmi     | --------------------+    denied)     |
   |   | operator|                                       |
   |   +---------+                                       |
   +-------------------------------------------------+
```

The two legitimate flows are `web → db:5432` and administrative SSH/RDP to each instance from your own IP. The `hmi → db` flow is the lateral movement the native controls will deny.

### An honest cost and teardown warning — read before Chapter 02

- **The segmentation primitives are free.** Security groups, NSGs, ASGs, and firewall rules cost nothing. **Compute and some networking cost money.** The instances are chosen from each cloud's free tier (`t3.micro`/`t2.micro`, `B1s`, `e2-micro`), but free-tier has limits and some resources (a second instance, egress, public IPs beyond the allowance) can incur small charges.
- **Set a budget alert first** (Chapter 02) and **run the teardown in Chapter 09** the moment you finish. Every chapter's cleanup section reminds you; the last chapter deletes everything.
- **If in doubt, do one cloud.** You do not need all three — pick the cloud you already use.

### Time and effort

| Part | Content | Approximate time |
|:---|:---|:---|
| A | Accounts, CLIs, and budget alerts | 45 min |
| B–D | Build, break, and segment (per cloud you choose) | 60–90 min each |
| E | Cross-cloud comparison and advanced controls | 45 min |
| F | Flow logs and detection | 30 min |
| G | Teardown | 20 min |

Budget an evening per cloud.

## Conventions

| Convention | Meaning |
|:---|:---|
| `bash` code block | Run on your workstation with the cloud CLI configured; command lines are bare and any output follows on the next line |
| **AWS / Azure / GCP** | The cloud a step applies to |
| **Cost note** | A step that may incur charges |

Every exercise follows the same shape: **Objective**, **Walkthrough**, **Expected result**, **Negative test**, **Rollback**.

## Summary and Completion Checklist

- [ ] The three native primitives and their models understood.
- [ ] Stateful-vs-stateless and group-by-identity internalized.
- [ ] The cost and teardown discipline accepted; you will set a budget alert in Chapter 02.
- [ ] Cloud(s) chosen.
