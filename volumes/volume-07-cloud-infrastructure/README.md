# Volume VII — Cloud Infrastructure

> Provider-neutral cloud architecture: service and deployment models,
> identity and cryptographic services, networking and hybrid connectivity,
> compute placement, data services, hybrid/multicloud design, governance
> and FinOps, and the automation and observability practices that keep a
> cloud environment trustworthy over time.

## Overview

Volume VII covers the concepts, architecture, and operating practices
common to public cloud infrastructure regardless of provider. Illustrative
code examples throughout the volume use generic, Terraform-style HCL
rather than any single provider's console or CLI, so the concepts transfer
directly to whichever provider (or providers) an organization operates.
Volume XVII applies this volume's concepts to AWS's specific console, CLI,
and service implementation in depth; readers looking for AWS-specific
service names, console paths, and CLI syntax should pair this volume with
Volume XVII.

The volume is organized in three movements:

- **Chapters 01–02** establish the foundational vocabulary and governed
  environment every workload lands into: service and deployment models,
  the shared responsibility model, provider physical/logical architecture,
  and the landing zone pattern — resource hierarchy, guardrails, and
  account vending — that precedes any workload onboarding.
- **Chapters 03–06** cover the core infrastructure domains a workload is
  built from: identity and cryptographic services, networking and hybrid
  connectivity, compute placement, and storage/database/data services.
- **Chapters 07–09** zoom out to cross-cutting architecture and operating
  practice: hybrid and multicloud design, governance/security/FinOps, and
  the automation, observability, resilience, and lifecycle operations
  practices that keep a cloud environment trustworthy as it changes over
  time.

Every chapter follows the same structure — learning objectives, theory and
architecture, design considerations, implementation and automation,
validation and troubleshooting, security and best practices, references
and knowledge checks, a hands-on lab, and a summary and completion
checklist — defined in [templates/chapter.md](../../templates/chapter.md)
and enforced by [EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md).
Each hands-on lab is a reproducible, disposable exercise with stated
prerequisites, numbered steps, expected results, a negative test, and
cleanup instructions; every lab in this volume runs entirely on the local
filesystem using Terraform's built-in providers or `conftest`, requiring
no cloud account or credentials.

## Chapters

1. [Cloud Operating Models and Architecture Foundations](chapters/01-cloud-operating-models-and-architecture-foundations.md) — IaaS/PaaS/SaaS/FaaS service models, the shared responsibility model, deployment models, regions/zones/edge, a Well-Architected-style pillar framework, and composite-availability math.
2. [Landing Zones, Resource Organization, and Guardrails](chapters/02-landing-zones-resource-organization-and-guardrails.md) — resource hierarchy design, preventive/detective/responsive guardrails, policy as code with OPA/conftest, and repeatable multi-account/subscription vending.
3. [Cloud Identity, Access, and Cryptographic Services](chapters/03-cloud-identity-access-and-cryptographic-services.md) — human/workload/federated identity, RBAC vs. ABAC, SAML 2.0/OIDC federation and workload identity federation, key management models, and secrets management.
4. [Cloud Networking and Hybrid Connectivity](chapters/04-cloud-networking-and-hybrid-connectivity.md) — CIDR allocation and subnetting, routing constructs, hub-and-spoke vs. transit-gateway topology, VPN vs. dedicated private connectivity, hybrid DNS, and network segmentation.
5. [Cloud Compute and Workload Placement](chapters/05-cloud-compute-and-workload-placement.md) — VM/container/serverless placement decisions, instance family sizing, on-demand/reserved/spot purchasing strategy, autoscaling models, and immutable golden-image pipelines.
6. [Cloud Storage, Databases, and Data Services](chapters/06-cloud-storage-databases-and-data-services.md) — object/block/file storage, storage lifecycle tiering, managed relational/NoSQL/cache database selection, the CAP theorem in practice, and RPO/RTO-driven backup and recovery design.
7. [Hybrid and Multicloud Architecture](chapters/07-hybrid-and-multicloud-architecture.md) — hybrid vs. multicloud drivers, portability vs. active multi-provider redundancy, abstraction layer limits, cross-provider consistency, and edge computing as a hybrid extension.
8. [Cloud Governance, Security, and FinOps](chapters/08-cloud-governance-security-and-finops.md) — continuous cloud security posture management, compliance control mapping to the shared responsibility model, the FinOps Inform/Optimize/Operate cycle, and cost allocation and commitment-discount management.
9. [Cloud Automation, Observability, Resilience, and Lifecycle Operations](chapters/09-cloud-automation-observability-resilience-and-lifecycle-operations.md) — plan/apply pipeline separation, drift detection and reconciliation, monitoring vs. observability across metrics/logs/traces, chaos engineering, and resource lifecycle/decommissioning.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine
  chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.
- [Master index](../../INDEX.md) and
  [master glossary](../../GLOSSARY.md) — cross-volume topics and terms
  across the complete encyclopedia.

## Software and platform baseline

Chapters in this volume reference the dated baseline recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md) — principally Terraform
1.9.x for illustrative infrastructure-as-code examples. Provider-specific
service names, quotas, and CLI syntax are deliberately out of scope for
this volume; consult the current vendor documentation for those, and see
Volume XVII for an AWS-specific deep dive built on the concepts introduced
here. Update `SOFTWARE_VERSIONS.md`, not individual chapters, when the
baseline changes.

## Building and validating this volume

From the repository root, after completing
[SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-07-cloud-infrastructure

# Build a single chapter.
scripts/bash/build-book.sh --format all \
  --chapter volumes/volume-07-cloud-infrastructure/chapters/01-cloud-operating-models-and-architecture-foundations.md
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
