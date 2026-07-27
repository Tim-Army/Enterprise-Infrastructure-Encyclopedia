# Chapter 07: NCP-CI — Cloud Integration (NC2 on AWS and Azure)

## Learning Objectives

- Explain what the NCP-CI-AWS and NCP-CI-Azure credentials certify.
- Summarize the four blueprint sections shared by both.
- Plan, deploy, configure, and manage NC2 on AWS and on Azure.
- Contrast the AWS and Azure cloud-integration specifics.
- Complete a per-section walkthrough for each domain of both exams.

## Theory and Architecture

The **Nutanix Certified Professional — Cloud Integration** credentials validate
running **Nutanix Cloud Clusters (NC2)** on public cloud — **NCP-CI-AWS** (91
questions / 180 minutes) and **NCP-CI-Azure** (83 questions / 180 minutes). Both
blueprints share **four sections**: **Planning**, **Deploying**, **Configuring**, and
**Managing** an NC2 environment on the respective cloud. NC2 runs AOS/AHV on bare-metal
cloud instances with a cloud-side network and the NC2 console.

## Design Considerations

The engineer plans cloud prerequisites (accounts/subscriptions, IAM/roles, networking/
VPC-or-VNet, bare-metal capacity), deploys the cluster via the **NC2 console**,
configures cloud networking/security and connectivity (Flow Virtual Networking,
security groups/NSGs), and manages nodes/clusters/hibernation and health. AWS uses
**VPC + bare-metal EC2**; Azure uses **VNet + BareMetal**.

## Implementation and Automation

The labs use the NC2 console/API and cloud CLIs for each section — plan, deploy,
configure, and manage — once for AWS (7.1–7.4) and once for Azure (7.5–7.8).

## Validation and Troubleshooting

Confirm both blueprints before studying:

```text
nutanix.com > NCP-CI-AWS (91 Q) / NCP-CI-Azure (83 Q), 180 min, 4 sections each:
  1 Planning   2 Deploying   3 Configuring   4 Managing  (an NC2 environment)
```

Common pitfalls: undersized/unavailable **bare-metal** capacity; and cloud networking
(VPC/VNet, routing, security groups/NSGs) mismatched to NC2 requirements.

## Security and Best Practices

Plan **IAM/roles** and **networking** to NC2 requirements, reserve **bare-metal**
capacity, deploy via the **NC2 console**, secure with **Flow Virtual Networking** and
cloud security groups/NSGs, and manage cost with **hibernation** when idle. Keep
cloud and on-prem connectivity (VPN/Direct Connect/ExpressRoute) resilient.

## References and Knowledge Checks

- nutanix.com: NCP-CI-AWS and NCP-CI-Azure blueprint guides; NC2 on AWS/Azure docs.

**Knowledge checks**

1. What cloud resource type runs NC2 (not standard VMs)?
2. How do AWS and Azure networking differ for NC2?
3. How does hibernation control NC2 cost?

## Hands-On Lab

Per-section walkthroughs — NCP-CI. **Shared prerequisites** — an NC2 subscription and
an AWS account / Azure subscription (or the CLIs). Commands shown as cloud CLI / NC2
patterns. **Cost:** bare-metal cloud instances incur charges — use hibernation and
tear down.

### Lab 7.1 — AWS: Plan the NC2 deployment

**Objective:** Verify AWS prerequisites (VPC, bare-metal capacity).

```bash
aws ec2 describe-vpcs --query 'Vpcs[].VpcId'
aws ec2 describe-instance-type-offerings \
  --filters Name=instance-type,Values='*metal*' --query 'InstanceTypeOfferings[].InstanceType' | head
```

**Expected result:** an existing **VPC** and available **bare-metal** instance types —
the planning section (AWS).

**Negative test:** plan on standard instances; NC2 needs **bare-metal** — confirm the
type is offered in your region.

**Cleanup:** none (read-only).

### Lab 7.2 — AWS: Deploy the cluster

**Objective:** Describe the NC2-console deploy flow.

```text
# NC2 console: create cluster -> select AWS region/AZ + bare-metal type + node count
#   -> select/create VPC + management subnet -> launch. NC2 orchestrates EC2 metal.
"deploy: NC2 console provisions bare-metal EC2 + AOS/AHV cluster"
```

**Expected result:** the cluster deploying from the **NC2 console** — the deploying
section (AWS).

**Negative test:** launch EC2 metal manually and install AOS; **NC2 console**
orchestrates it — use the managed flow.

**Cleanup:** terminate the cluster from the NC2 console if it was for the lab.

### Lab 7.3 — AWS: Configure networking and security

**Objective:** Confirm the cluster's cloud networking/security.

```bash
aws ec2 describe-security-groups --query 'SecurityGroups[].GroupName' | head
# Flow Virtual Networking overlays; ensure prism/CVM ports allowed within the VPC.
```

**Expected result:** the security groups and network config for the cluster — the
configuring section (AWS).

**Negative test:** open all ports to 0.0.0.0/0; scope **security groups** to required
ports/sources.

**Cleanup:** none (read-only).

### Lab 7.4 — AWS: Manage the environment

**Objective:** Describe node/cluster management and hibernation.

```text
# NC2 console: add/remove bare-metal nodes; hibernate cluster to save cost;
#   monitor cluster + cloud resource health.
"manage: scale nodes, hibernate/resume, monitor health"
```

**Expected result:** the management operations (scale, hibernate, monitor) — the
managing section (AWS).

**Negative test:** leave idle clusters running; **hibernate** to stop bare-metal
charges.

**Cleanup:** hibernate/terminate as appropriate.

### Lab 7.5 — Azure: Plan the NC2 deployment

**Objective:** Verify Azure prerequisites (VNet, BareMetal).

```bash
az network vnet list --query '[].name'
az vm list-skus --query "[?contains(name,'Metal')].name" -o tsv | head
```

**Expected result:** an existing **VNet** and available **BareMetal** SKUs — the
planning section (Azure).

**Negative test:** plan on standard VMs; NC2 on Azure needs **BareMetal** — confirm
availability in the region.

**Cleanup:** none (read-only).

### Lab 7.6 — Azure: Deploy the cluster

**Objective:** Describe the NC2-console deploy flow on Azure.

```text
# NC2 console: create cluster -> Azure region + BareMetal + node count
#   -> select/create VNet + delegated subnet -> launch.
"deploy: NC2 console provisions Azure BareMetal + AOS/AHV cluster"
```

**Expected result:** the cluster deploying on Azure from the **NC2 console** — the
deploying section (Azure).

**Negative test:** hand-build BareMetal; use the **NC2 console** managed flow.

**Cleanup:** delete the cluster from the NC2 console if it was for the lab.

### Lab 7.7 — Azure: Configure networking and security

**Objective:** Confirm NSGs and VNet config.

```bash
az network nsg list --query '[].name'
# Flow Virtual Networking overlays; ensure delegated subnet + NSGs allow CVM/Prism.
```

**Expected result:** the NSGs and VNet config for the cluster — the configuring
section (Azure).

**Negative test:** allow any-any in the NSG; scope **NSG rules** to required
ports/sources.

**Cleanup:** none (read-only).

### Lab 7.8 — Azure: Manage the environment

**Objective:** Describe node/cluster management and hibernation on Azure.

```text
# NC2 console (Azure): scale nodes, hibernate/resume, monitor cluster + cloud health.
"manage: scale, hibernate/resume, monitor (Azure)"
```

**Expected result:** the management operations on Azure — the managing section
(Azure).

**Negative test:** run idle BareMetal; **hibernate** to control cost.

**Cleanup:** hibernate/delete as appropriate.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The NCP-CI-AWS and NCP-CI-Azure credentials certify running Nutanix Cloud Clusters
(NC2) on public cloud across four shared sections — planning, deploying, configuring,
and managing — on bare-metal cloud instances via the NC2 console.

- [ ] I can plan AWS/Azure prerequisites (VPC/VNet, bare-metal).
- [ ] I can deploy NC2 via the console on both clouds.
- [ ] I can configure cloud networking and security (SG/NSG, Flow).
- [ ] I can manage, scale, and hibernate NC2 clusters.
- [ ] I completed Labs 7.1–7.8 including each negative test.
