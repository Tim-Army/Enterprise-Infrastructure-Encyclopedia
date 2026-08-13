# Chapter 01: The Aviatrix Certified Engineer (ACE) Program

![The Aviatrix ACE certification family: the free, self-paced ACE Associate (multicloud networking foundations) as the gateway to the instructor-led ACE Professional (hands-on multicloud transit, firewall insertion, egress, and user access) and ACE Design Expert (scalable multicloud design), alongside focused ACE courses — Security, Hybrid Cloud, Cloud Backbone, Automation, and Operations. All built on the Aviatrix Controller + CoPilot managing gateways across AWS, Azure, GCP, and OCI.](../../../diagrams/volume-126-aviatrix-certifications/chapter-01-certification-program.svg)

*Figure 1-1. The ACE program: a free foundational Associate, an instructor-led Professional, a Design Expert capstone, and focused electives — all teaching the Aviatrix overlay (Controller, CoPilot, gateways) across the four major clouds.*

## Learning Objectives

- Describe the Aviatrix Certified Engineer (ACE) program: Associate, Professional, Design Expert, and focused courses.
- Understand the Aviatrix architecture the exams assume: Controller, CoPilot, and gateways over cloud-native constructs.
- Know the exam logistics: the free Associate, its Professional prerequisite chain, and delivery.
- Set up a free study environment (no cloud spend required for the Associate).

## What Aviatrix is, and why it certifies

Aviatrix builds a **multicloud network overlay**: instead of stitching together each cloud's native networking by hand, you deploy Aviatrix **gateways** into your VPCs/VNets and manage them centrally from the **Controller**, with **CoPilot** for visibility. The overlay delivers consistent transit, encryption, egress control, firewall insertion, and segmentation across **AWS, Azure, Google Cloud, and OCI** — abstracting away each provider's quirks (route-table limits, overlapping CIDRs, transit-gateway differences).

The **ACE program** certifies engineers on both the multicloud networking fundamentals and the Aviatrix platform that implements them.

## The certification family

Verified on aviatrix.ai, 3 August 2026:

| Credential | Format | Prerequisite | Focus |
|:---|:---|:---|:---|
| **ACE Associate** | Self-paced (~4 hrs) + final exam; **FREE** | none | Multicloud networking foundations across the four clouds |
| **ACE Professional** | Instructor-led, **3 days** + hands-on labs + exam | ACE Associate + ~1 yr cloud experience | Multicloud transit, firewall insertion, egress, user access — hands-on |
| **ACE Design Expert** | Instructor-led | ACE Professional-level knowledge | Designing scalable, resilient multicloud networks |

Focused **ACE courses** deepen specific areas: **ACE Security** (securing cloud networks), **ACE Hybrid Cloud** (secure hybrid connectivity), **ACE Cloud Backbone** (edge-to-cloud backbone), **ACE Automation** (Terraform/infrastructure-as-code), and **ACE Operations** (access, visibility, compliance via CoPilot).

The ladder is deliberate: **Associate is free and gateless** (the industry on-ramp to multicloud networking), and it is the **mandatory prerequisite** for Professional, which adds real hands-on labs.

## The architecture the exams assume

| Component | Role |
|:---|:---|
| **Controller** | The central control plane — deploys and orchestrates gateways, programs routing, holds policy |
| **CoPilot** | Observability and operations — topology maps, flow visibility, FlowIQ, alerts, compliance |
| **Gateway** | The data-plane instance Aviatrix deploys into each VPC/VNet (transit, spoke, egress, firewall, VPN roles) |
| **Transit** | The multicloud backbone: transit gateways peered across regions and clouds, with active-active HA |
| **Spoke** | Workload VPCs/VNets attached to transit |
| **FireNet** | Firewall Network Service — inserts NGFWs (Palo Alto, Fortinet, Check Point) into the inspection path |
| **Distributed Cloud Firewall (DCF)** | Aviatrix's distributed, policy-based segmentation across the fabric |

The mental model: **cloud-native constructs at the bottom, the Aviatrix overlay on top, one control plane across all clouds.**

## Hands-On Lab

The Associate needs **no cloud accounts**. This volume's labs model the networking concepts with **free Linux primitives** (namespaces, nftables, FRR/iproute2) and real **Terraform** syntax, plus design-level Aviatrix console steps where the platform is required. **Cost:** none.

### Lab 1.1 — Register for the free Associate and map the family

**Objective:** Enroll and confirm the certification structure.

```bash
cat <<'EOF'
ACE Associate: aviatrix.ai/training/ace-associate  (FREE, code: acemulticloud — includes the final exam)
  -> prerequisite for ACE Professional (3-day instructor-led + labs)
    -> ACE Design Expert (design capstone)
Focused courses: Security | Hybrid Cloud | Cloud Backbone | Automation | Operations
EOF
```

**Expected result:** A clear map: free Associate first, Professional next (gated on Associate), Design Expert as the capstone, with focused electives — the sequence this volume follows.

**Negative test:** Attempting ACE Professional without the Associate — blocked; the Associate certificate is a hard prerequisite, not a suggestion.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Build the study lab

**Objective:** Stand up the free primitives the volume's labs use.

```bash
sudo apt-get update -qq && sudo apt-get install -y iproute2 nftables netcat-openbsd frr 2>/dev/null || \
  echo "install iproute2, nftables, netcat, frr (routing) on your distro"
ip netns add probe 2>/dev/null && ip netns list | grep probe && sudo ip netns del probe
command -v terraform || echo "install terraform (or opentofu) for the automation chapter"
echo "lab ready: namespaces model VPCs/gateways, nftables models egress/firewall, FRR models transit routing"
```

**Expected result:** Namespace creation works and the tooling is present — this volume models Aviatrix's transit/egress/firewall/VPN concepts on one Linux host, so the ideas are concrete even without cloud spend.

**Negative test:** Expecting the labs to *be* Aviatrix — they model the **concepts** the exams test; the real Controller/CoPilot need cloud accounts and appear at design level.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The ACE family (Associate/Professional/Design Expert + focused courses) understood.
- [ ] The Aviatrix architecture (Controller, CoPilot, gateways, transit, FireNet, DCF) internalized.
- [ ] Free Associate registration and the Professional prerequisite chain known.
- [ ] The free study lab stood up.
