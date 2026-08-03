# Volume CVI — Cloud-Native Segmentation Build-It-Yourself Lab

> A build-it-yourself microsegmentation lab that uses **only the cloud providers' own native network
> controls** — no host agent, no CNI, no service mesh. It builds the same three-tier estate (web, database,
> operator) on **AWS, Azure, and GCP**, proves a permissive default lets the operator reach the database
> (lateral movement), then contains it natively: AWS **security groups that reference each other** plus a
> stateless **Network ACL**; Azure **NSG rules written by Application Security Group**; GCP **firewall
> rules targeting network tags, then the stronger service account**. It compares the three models side by
> side, adds organization-level guardrails (prefix lists, hierarchical policies, Azure Policy), turns on
> native flow logs to see the denial, and ends with a **thorough, cost-first teardown**. Because the
> clouds are real accounts this volume is **single-track** — and cost discipline is part of the lab. **~30
> walkthrough labs** across nine chapters, opening the cloud-native tier of the microsegmentation series.

## Overview

Volume CVI is a **hands-on lab volume** and the first of the cloud-native tier. Where
[Volume LXXXVII (Microsegmentation Options)](../volume-087-microsegmentation-options/README.md)
compares vendors and approaches, this volume is the **build**: it stands up a real estate on each major
cloud and segments it with the primitive that cloud ships for free.

Its distinguishing idea is that **every cloud already has a microsegmentation engine** — you are paying
for it whether you use it or not. Security groups, NSGs with Application Security Groups, and VPC firewall
rules with service accounts are genuine identity-aware, default-deny-capable controls. The skill is
knowing each one's model and its sharp edges: AWS security groups are allow-only and stateful while its
NACLs are stateless (the return-traffic trap); Azure and GCP evaluate by ascending priority where the
first match wins; GCP rules are network-wide, not per-instance. The lab teaches all three by building the
identical policy — "only web reaches the database" — three times, then reads it back as one intent in
three grammars.

Because the accounts are real, **cost and teardown discipline is a first-class part of the lab**: you set
a budget alert before creating anything and run a complete teardown at the end.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Accounts, CLIs, and Cost Guardrails](chapters/02-accounts-clis-and-cost-guardrails.md) | 2.1–2.3 |
| 03 | [AWS — Security Groups and Network ACLs](chapters/03-aws-security-groups-and-nacls.md) | 3.1–3.5 |
| 04 | [Azure — Network Security Groups and Application Security Groups](chapters/04-azure-nsgs-and-asgs.md) | 4.1–4.4 |
| 05 | [GCP — VPC Firewall Rules, Tags, and Service Accounts](chapters/05-gcp-firewall-rules-and-tags.md) | 5.1–5.4 |
| 06 | [Cross-Cloud Comparison](chapters/06-cross-cloud-comparison.md) | 6.1 |
| 07 | [Advanced Native Controls](chapters/07-advanced-native-controls.md) | 7.1–7.3 |
| 08 | [Flow Logs and Detection](chapters/08-flow-logs-and-detection.md) | 8.1–8.3 |
| 09 | [Operations, Cost Control, and Teardown](chapters/09-operations-cost-control-and-teardown.md) | 9.1–9.4 |

## What you will be able to do

- Build a three-tier estate and segment it natively on AWS, Azure, and GCP.
- Write identity-based rules — SG references, ASGs, service accounts — instead of brittle CIDRs.
- Survive the AWS NACL stateless return-traffic trap and Azure/GCP priority ordering.
- Enforce guardrails with prefix lists, hierarchical policies, and Azure Policy.
- Enable native flow logs, locate a denial, and run the observe-then-enforce loop.
- Tear down every billable resource and verify the account is empty.

## Prerequisites

- A free-tier account on at least one of AWS, Azure, or GCP (you do not need all three).
- The corresponding CLI installed and authenticated (Chapter 02 walks through each).
- Willingness to set a budget alert and run the teardown — the estate costs a small amount while it runs.

## See also

- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab pairs with.
- [Volume XVII — AWS Architecture and Security](../volume-017-aws-architecture-security/README.md) and [Volume XXXIII — Microsoft Azure Certification Tracks](../volume-033-microsoft-azure-certifications/README.md) — deeper cloud platform coverage.
- [Volume CI — Calico](../volume-101-calico-lab/README.md) through [Volume CV — Consul](../volume-105-consul-lab/README.md) — the overlay products you pair with native controls for workload identity and L7.
