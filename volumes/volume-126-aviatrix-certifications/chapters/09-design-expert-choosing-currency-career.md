# Chapter 09: ACE Design Expert, Choosing a Path, and Currency

## Learning Objectives

- Cover the ACE Design Expert: designing scalable, resilient multicloud networks.
- Choose and sequence the ACE credentials for your role.
- Keep skills current as Aviatrix and the clouds evolve.

## ACE Design Expert

The **Design Expert** is the ACE capstone: not new features, but **synthesis** — designing multicloud networks that scale to hundreds of VPCs, survive failures, meet compliance, and stay operable. It draws on everything below it:

| Design dimension | Questions it answers |
|:---|:---|
| **Scale** | Transit topology for N spokes across M clouds; route/attachment limits; multi-region |
| **Resilience** | Active-active everywhere; failure domains; region/cloud failover |
| **Segmentation** | Network domains + DCF for isolation; where FireNet inspection belongs |
| **Egress** | Centralized vs distributed; compliance logging |
| **Connectivity** | User VPN, Site2Cloud, edge/backbone; overlapping-CIDR strategy |
| **Operations** | CoPilot visibility, Terraform automation, audit |

## Choosing your path

| If your role is… | Start with | Then |
|:---|:---|:---|
| Anyone entering cloud networking | **ACE Associate** (free) | — |
| Cloud/network engineer building multicloud | ACE Associate | **ACE Professional** |
| Architect designing multicloud networks | ACE Professional | **ACE Design Expert** |
| Security-focused | + **ACE Security** | DCF/FireNet depth |
| Platform/automation | + **ACE Automation** | Terraform at scale |
| Operations/SRE | + **ACE Operations** | CoPilot mastery |
| Hybrid/edge | + **ACE Hybrid Cloud** / **ACE Cloud Backbone** | edge-to-cloud |

The spine is **Associate → Professional → Design Expert**; the focused courses (Security, Automation, Operations, Hybrid Cloud, Cloud Backbone) add depth where your work needs it.

## Study approach

| Credential | Volume chapters | Lab |
|:---|:---|:---|
| ACE Associate | [02](02-associate-cloud-native-networking.md)–[03](03-associate-aviatrix-architecture.md) | free primitives; no cloud accounts |
| ACE Professional | [04](04-professional-multicloud-transit.md)–[07](07-professional-user-and-site-connectivity.md) | namespaces/nftables/FRR + design-level console |
| ACE Automation / Operations | [08](08-professional-automation-and-operations.md) | Terraform (validate) + CoPilot model |
| ACE Design Expert | this chapter | synthesize a design |

The Associate is genuinely free (code `acemulticloud`, includes the exam) and needs no cloud spend — start there today. Professional adds instructor-led hands-on labs; the free Linux models in this volume make the concepts concrete beforehand.

## Currency

- **The clouds change under the overlay.** New native transit features (TGW updates, Azure vWAN, GCP NCC, OCI DRG) shift what Aviatrix abstracts; re-verify the current design patterns on aviatrix.ai.
- **Distributed Cloud Firewall is growing.** DCF (distributed segmentation) is an expanding part of the platform and exams — track its policy model as it matures.
- **The program evolves.** Course names and focused electives change; confirm the current ACE catalog on aviatrix.ai before planning. This volume was verified 3 August 2026.
- **Cross-references.** Multicloud foundations sit alongside the cloud-provider volumes ([AWS XVII](../../volume-017-aws-architecture-security/README.md), [Azure XXXIII](../../volume-033-microsoft-azure-certifications/README.md), [Google Cloud XXXIV](../../volume-034-google-cloud-certifications/README.md)) and the microsegmentation landscape ([LXXXVII](../../volume-087-microsegmentation-options/README.md)).

## Hands-On Lab

### Lab 9.1 — Design a multicloud network (Design Expert)

**Objective:** Synthesize the volume into a design.

```bash
cat > my-multicloud-design.md <<'EOF'
Estate: ___ VPCs across AWS/Azure/GCP/OCI; ___ regions
Transit:   full-mesh peered transits? single backbone? (Ch04)
HA:        active-active pairs everywhere (Ch04)
Segment:   network domains: prod/dev/shared; DCF policy for east-west (Ch04, Ch06)
Inspect:   FireNet where deep L7/IPS needed; DCF elsewhere (Ch06)
Egress:    centralized (compliance) or distributed (latency)? FQDN allowlist (Ch05)
Connect:   user VPN (split tunnel), Site2Cloud, edge/backbone; overlapping-CIDR NAT (Ch07)
Operate:   Terraform-managed; CoPilot visibility + audit (Ch08)
EOF
cat my-multicloud-design.md
```

**Expected result:** A one-page design touching every ACE dimension — the synthesis the Design Expert certifies. Each line traces to a chapter you can defend.

**Negative test:** A design that adds a firewall or egress choke point with no HA — the Design Expert flags single points of failure; resilience is a first-class dimension, not an afterthought.

**Rollback:** Keep the design.

### Lab 9.2 — Currency check

**Objective:** Make re-verification routine.

```bash
cat <<'EOF'
Before relying on this volume, re-check on aviatrix.ai:
  [ ] the ACE catalog (Associate free? Professional/Design Expert current? focused courses?)
  [ ] Distributed Cloud Firewall policy model (fast-moving)
  [ ] native transit changes across AWS/Azure/GCP/OCI that shift the overlay's role
EOF
echo "verified 3 Aug 2026 — re-verify before scheduling"
```

**Expected result:** A short re-verification checklist — the ACE program and the underlying clouds both move, so confirm before committing study time.

**Negative test:** Studying a cached course list — Aviatrix reshapes its focused-course lineup periodically; the official catalog is authoritative.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The ACE Design Expert synthesis role understood.
- [ ] A path chosen (Associate → Professional → Design Expert + focused electives).
- [ ] A multicloud design drafted touching every dimension.
- [ ] Currency habit installed (re-verify the catalog and DCF model on aviatrix.ai).
