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

## Certification alignment

This volume maps to the **Cisco Automation** certification track, as
recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). Cisco
rebranded its DevNet certifications as **CCNA, CCNP, and CCIE
Automation on 3 February 2026**, migrating existing DevNet holders to
the new names; the exam-topics documents still carry their DevNet-era
titles, which is a naming lag, not a content difference. Cisco has also
announced upcoming v1.2 minor updates across the Automation exams —
re-confirm versions at the next currency check. Chapter content
describes blueprint domains and points to Cisco's official sources; it
does not reproduce proprietary exam content.

### The exams

| Exam | Title | Duration | Role in the track |
| --- | --- | --- | --- |
| **200-901** v1.1 | CCNA Automation (published as "DevNet Associate Exam") | 120 min | Associate |
| **350-901** v1.1 | Developing Applications using Cisco Core Platforms and APIs | 120 min | Core — required for CCNP Automation |
| CCIE Automation | Practical (lab) exam | — | Expert tier; Cisco is adding an AI module to its practical exams |

CCNP Automation requires the core exam plus **one** concentration exam;
the concentration set carried over from the DevNet specialist exams and
is not restated here — confirm the current list with Cisco at
registration, along with question counts and pricing.

**200-901 CCNA Automation v1.1**

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Software Development and Design | 15% | 01, 05 |
| 2.0 Understanding and Using APIs | 20% | 04 |
| 3.0 Cisco Platforms and Development | 15% | 04 |
| 4.0 Application Deployment and Security | 15% | 05, 06 |
| 5.0 Infrastructure and Automation | 20% | 02, 03, 07 |
| 6.0 Network Fundamentals | 15% | Volume II |

**350-901 CCNP Automation core v1.1**

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Software Development and Design | 20% | 01, 05 |
| 2.0 Using APIs | 20% | 04 |
| 3.0 Cisco Platforms | 20% | 04 |
| 4.0 Application Deployment and Security | 20% | 05, 06, 08 |
| 5.0 Infrastructure and Automation | 20% | 02, 03, 07, 09 |

Be clear-eyed about depth: this volume is deliberately vendor-neutral —
its Terraform, Ansible, pipeline, and orchestration material carries the
automation domains well, but the **Cisco Platforms** domains test
platform-specific APIs (Catalyst Center, Meraki, Webex, and peers) that
a vendor-neutral volume does not drill. Pair the associate plan below
with Cisco U. platform sandboxes, and expect the platform domain to need
dedicated lab time.

**CCNA Automation — six weeks** at 8–10 hours per week, assuming the
Python fluency this volume already expects:

| Week | Focus | Chapters |
| --- | --- | --- |
| 1 | Software development and design: version control, formats, methodologies | 01 |
| 2 | APIs in depth: REST semantics, authentication, webhooks — **a fifth of the exam** | 04 |
| 3 | Cisco platform APIs and SDKs, against live sandboxes | 04 |
| 4 | Deployment and security: containers, CI/CD, secrets handling | 05, 06 |
| 5 | Infrastructure and automation: IaC, configuration management, orchestration — the other heavy domain | 02, 03, 07 |
| 6 | Network fundamentals refresh, then full-blueprint timed practice | Volume II |

For the core exam afterward, extend the same structure by three to four
weeks, weighting evenly — its five domains are a flat 20% each, so
weakest-domain-first beats weight-ordered study.

### CCIE lab readiness

**CCIE Automation** — rebranded from DevNet Expert on 3 February 2026 —
is the expert tier above this track, reached by first passing the
`350-901` core. It is a **hands-on practical lab exam** in which you
design, build, and operate software and automation solutions across
Cisco platforms end to end; Cisco has announced **minor (v1.2) updates**
and is adding a **new AI module** to its CCIE practical exams, so confirm
the current format at registration. Unlike the infrastructure CCIEs, the
Automation lab is a **programming and automation** exam — pipelines,
APIs, model-driven interfaces, and orchestration under time — rather than
a device-configuration one.

**What the lab adds over this volume.** These chapters build automation
as a vendor-neutral discipline — IaC, configuration management, CI/CD,
event-driven orchestration, and secure execution — and that discipline
is exactly what the lab assumes. What the lab tests further is **speed
and Cisco-platform depth**: driving Catalyst Center, Meraki, NSO, IOS XR
model-driven interfaces, and the Cisco API surface specifically, and
building working automation against them under an exam clock. That
platform-specific breadth is deliberately beyond a vendor-neutral volume
— pair these chapters with hands-on time on the Cisco platforms
themselves.

**How to prepare.** Take the idempotent, asserted, vaulted habits this
volume teaches and apply them repeatedly against **Cisco DevNet
sandboxes** (Catalyst Center, Meraki, NSO, IOS XR) until building and
debugging Cisco-platform automation is fast and reflexive. Rehearse full
automation scenarios end to end against the clock, drill the design and
architecture reasoning using [Volume XXX](../volume-30-cisco-ccde-network-design/README.md),
and draw platform depth from the Cisco technology volumes —
[XXVII](../volume-27-cisco-data-center/README.md) and
[XXIX](../volume-29-cisco-service-provider/README.md) for their
model-driven and NSO material. Confirm the current lab blueprint and
format on the Cisco Learning Network before scheduling — CCIE lab topics
are separate from the written exam topics and change independently.

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
