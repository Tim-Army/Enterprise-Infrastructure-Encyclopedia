# Volume IX — Infrastructure Automation

> Terraform and Ansible as the volume's core engines, extended through API
> and event integration, pipelines and policy gates, identity and secrets,
> workflow orchestration, supply-chain security, and the observability and
> lifecycle discipline the automation control plane needs as a production
> system in its own right.

## Overview

Volume IX builds the infrastructure automation practice this encyclopedia
relies on from Volume II onward: declarative infrastructure as code,
idempotent configuration management, and the pipelines, identity, and
governance controls that make both trustworthy at enterprise scale. It
assumes the repository architecture, automation architecture, and
engineering practices established in
[Volume I — Enterprise Engineering Foundations](../volume-01-enterprise-engineering-foundations/README.md),
and its Terraform and Ansible baseline is used throughout every later
volume that provisions or configures infrastructure.

The volume is organized in three arcs:

- **Chapters 01–03** establish the automation operating model and the two
  core engines: infrastructure as code with Terraform (state, providers,
  modules) and configuration management with Ansible (idempotency,
  inventory, roles).
- **Chapters 04–06** extend those engines outward: integrating with APIs,
  webhooks, and event sources; building the plan/test/policy/approve/apply
  pipeline that delivers changes safely; and issuing the federated
  identity and secrets that pipeline stages actually run as.
- **Chapters 07–09** cover what happens once automation is orchestrating
  multi-step, event-driven operations at scale: workflow orchestration,
  supply-chain security and governance, and the observability, reliability,
  and lifecycle discipline the automation control plane needs as a
  production system.

Every chapter follows the same structure — learning objectives, theory and
architecture, design considerations, implementation and automation,
validation and troubleshooting, security and best practices, references
and knowledge checks, a hands-on lab, and a summary and completion
checklist — defined in [templates/chapter.md](../../templates/chapter.md)
and enforced by [EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md).
Each hands-on lab is a reproducible, disposable exercise with a stated
objective, prerequisites, numbered steps, expected results, a negative
test, and cleanup instructions; nearly every lab in this volume runs
entirely without cloud credentials, using local providers, dev-mode Vault,
or local HTTP servers.

## Chapters

1. [Automation Operating Models and Engineering Foundations](chapters/01-automation-operating-models-and-engineering-foundations.md) — the automation maturity curve, operating models, Team Topologies applied to automation, and repository/branch practices for infrastructure code.
2. [Infrastructure as Code, State, Providers, and Modules](chapters/02-infrastructure-as-code-state-providers-and-modules.md) — Terraform's plan/apply lifecycle, remote state and locking, providers, modules, `moved`/`import`/`check` blocks, and `terraform test`.
3. [Configuration Management and Desired-State Convergence](chapters/03-configuration-management-and-desired-state-convergence.md) — idempotency, Ansible inventory and variable precedence, roles and collections, Molecule testing, and execution environments.
4. [API, Event, and Integration Automation](chapters/04-api-event-and-integration-automation.md) — synchronous versus event-driven integration, idempotency keys, webhook signature verification, and the Terraform-to-Ansible inventory handoff.
5. [Automation Pipelines, Testing, and Policy Gates](chapters/05-automation-pipelines-testing-and-policy-gates.md) — pipeline stages, the infrastructure test pyramid, and policy as code with Open Policy Agent and Conftest against Terraform plan JSON.
6. [Automation Identity, Secrets, and Privileged Execution](chapters/06-automation-identity-secrets-and-privileged-execution.md) — OIDC federation, HashiCorp Vault AppRole and dynamic secrets, `ansible-vault`, and plan/apply credential separation.
7. [Workflow Orchestration and Event-Driven Operations](chapters/07-workflow-orchestration-and-event-driven-operations.md) — the event-driven automation loop, Event-Driven Ansible rulebooks, approval-gated workflows, and guarding against automation feedback loops.
8. [Automation Security, Governance, and Supply Chains](chapters/08-automation-security-governance-and-supply-chains.md) — the automation supply chain, SLSA, SBOM generation, `cosign` signing, and governed dependency updates.
9. [Automation Observability, Reliability, and Lifecycle Operations](chapters/09-automation-observability-reliability-and-lifecycle-operations.md) — observability for the automation control plane itself, reliability indicators, backup/restore drills, and module deprecation policy.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.

## Software and platform baseline

Chapters in this volume are written against the dated baseline recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md): Terraform 1.9.x and
Ansible core 2.17 / ansible 10.x. Supporting tools referenced throughout —
Conftest/OPA, HashiCorp Vault, Event-Driven Ansible, Checkov, `cosign`, and
`syft` — are used at their current stable releases as of the same baseline
date; update [SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md), not
individual chapters, when the baseline changes.

## Building and validating this volume

From the repository root, after completing
[SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-09-infrastructure-automation

# Build a single chapter.
scripts/bash/build-book.sh --format all \
  --chapter volumes/volume-09-infrastructure-automation/chapters/05-automation-pipelines-testing-and-policy-gates.md
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
