# Volume XVII — AWS Architecture and Security

> Designing, securing, automating, and operating enterprise workloads on
> Amazon Web Services, from account foundations through detection and
> incident response, mapped to the AWS Certified Solutions Architect and
> AWS Certified Security certification paths.

## Overview

Volume XVII applies the Well-Architected Framework introduced in its own
first chapter across a complete AWS enterprise stack: account and
organization design, identity and governance, networking and hybrid
connectivity, compute and application architecture, storage and databases,
reliability and disaster recovery, observability and cost governance, and
security detection and incident response. Each chapter builds on the
account, identity, and network foundations established in Chapters 01–03,
and Chapter 09 closes the volume with a capstone that integrates every
preceding chapter into one reference architecture and one hands-on build.

The volume is organized in three parts:

- **Chapters 01–02** establish the account as the unit of isolation, the
  Well-Architected Framework as the volume's design vocabulary, and the
  multi-account, identity, and governance model (AWS Organizations, IAM,
  IAM Identity Center, and AWS Control Tower) every later chapter assumes.
- **Chapters 03–07** cover the technical domains an AWS architecture is
  built from: secure networking and hybrid/edge connectivity, compute and
  application architecture (EC2, containers, and serverless), storage and
  databases with data protection, reliability and disaster recovery, and
  observability, automation, and cost governance.
- **Chapters 08–09** complete the volume with security architecture,
  detection, and incident response, and a capstone chapter that
  synthesizes every prior chapter into one reference architecture and maps
  the volume to both certification paths.

Every chapter follows the same structure — learning objectives, theory and
architecture, design considerations, implementation and automation,
validation and troubleshooting, security and best practices, references
and knowledge checks, a hands-on lab, and a summary and completion
checklist — defined in [templates/chapter.md](../../templates/chapter.md)
and enforced by [EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md).
Each hands-on lab is a reproducible, disposable exercise with a stated
objective, prerequisites, numbered steps, expected results, a negative
test, and explicit cost implications with cleanup instructions to avoid
ongoing billing.

## Chapters

1. [Cloud Foundations, Accounts, and Well-Architected Design](chapters/01-cloud-foundations-accounts-and-well-architected-design.md) — the shared responsibility model, AWS global infrastructure, the six Well-Architected pillars, and root-account hardening.
2. [Multi-Account Identity, Governance, and Landing Zones](chapters/02-multi-account-identity-governance-and-landing-zones.md) — AWS Organizations, service control policies, IAM, IAM Identity Center, and AWS Control Tower landing zones.
3. [Secure Networking, Hybrid Connectivity, and Edge](chapters/03-secure-networking-hybrid-connectivity-and-edge.md) — VPC design, security groups and NACLs, Transit Gateway and PrivateLink, Direct Connect and Site-to-Site VPN, and Route 53/CloudFront/WAF at the edge.
4. [Compute, Containers, Serverless, and Application Architecture](chapters/04-compute-containers-serverless-and-application-architecture.md) — EC2 Auto Scaling, Amazon ECS and EKS, AWS Lambda, load balancer selection, and event-driven orchestration with Step Functions and EventBridge.
5. [Storage, Databases, Analytics, and Data Protection](chapters/05-storage-databases-analytics-and-data-protection.md) — S3, EBS, and EFS; RDS, Aurora, and DynamoDB; the Redshift/Glue/Athena/Lake Formation analytics stack; KMS encryption; and AWS Backup.
6. [Reliability, Migration, Multi-Region, and Disaster Recovery](chapters/06-reliability-migration-multi-region-and-disaster-recovery.md) — RTO/RPO-driven DR strategy selection, Route 53 failover, multi-Region replication, and migration with the 7 Rs, MGN, and DMS.
7. [Observability, Automation, Performance, and Cost Governance](chapters/07-observability-automation-performance-and-cost-governance.md) — CloudWatch, X-Ray, AWS Config, Systems Manager, infrastructure as code, and cost governance with Cost Explorer, Budgets, and Compute Optimizer.
8. [Security Architecture, Detection, and Incident Response](chapters/08-security-architecture-detection-and-incident-response.md) — GuardDuty, Inspector, Macie, and Security Hub; automated detection-to-response pipelines; and AWS-specific incident response phases.
9. [Solutions Architect and Security Training Capstone](chapters/09-solutions-architect-and-security-training-capstone.md) — a synthesized reference architecture, a certification blueprint domain map, and a capstone hands-on build spanning the full volume.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine
  chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.

## Software and platform baseline

Chapters in this volume reference the current GA AWS service surface as
recorded in [SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md), dated
2026-07. AWS service behavior and console paths evolve continuously;
treat the CLI and Terraform (AWS provider, Terraform 1.9.x) examples in
this volume as correct against that baseline and verify current syntax
against official AWS documentation before applying them in production.

## Certification alignment

This volume maps to the **AWS Certified Solutions Architect** and
**AWS Certified Security** certification paths, as recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). Chapter
09 provides a chapter-to-domain mapping and capstone exercise; always
confirm current blueprint domains and weighting against the official AWS
Training and Certification exam guide, since blueprints change
independently of this repository's release cycle.

## Building and validating this volume

From the repository root, after completing
[SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-17-aws-architecture-security

# Build a single chapter.
scripts/bash/build-book.sh --format all \
  --chapter volumes/volume-17-aws-architecture-security/chapters/01-cloud-foundations-accounts-and-well-architected-design.md
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
