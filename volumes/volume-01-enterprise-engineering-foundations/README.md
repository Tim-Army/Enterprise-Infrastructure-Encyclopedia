# Volume I — Enterprise Engineering Foundations

> The engineering practices, repository architecture, automation, project
> workflow, documentation, and conceptual infrastructure foundations every
> other volume in this encyclopedia builds on.

## Overview

Volume I is the encyclopedia's foundation volume. It has no prerequisite
volume, and every subsequent volume that involves version-controlled
configuration, automation, or governance assumes the practices established
here — most directly Volumes II, IV, V, VI, VII, and IX, which name Volume
I as a dependency in [ROADMAP.md](../../ROADMAP.md).

The volume is organized in two halves:

- **Chapters 01–05** cover the engineering practices an infrastructure team
  needs before it manages any infrastructure at all: a reproducible
  developer workstation, repository architecture, automation architecture,
  GitHub-native project and workflow management, and a documentation
  pipeline that treats content as code.
- **Chapters 06–08** zoom out from tooling to the conceptual foundations
  that frame the rest of the encyclopedia: what enterprise infrastructure
  is and how its domains map to Volumes II through XXIV, how enterprise
  architecture governs technology decisions, and how infrastructure moves
  through a managed lifecycle from planning to decommissioning.

Every chapter follows the same structure — learning objectives, theory and
architecture, design considerations, implementation and automation,
validation and troubleshooting, security and best practices, references
and knowledge checks, a hands-on lab, and a summary and completion
checklist — defined in [templates/chapter.md](../../templates/chapter.md)
and enforced by [EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md).
Each hands-on lab is a reproducible, disposable exercise with a stated
objective, prerequisites, numbered steps, expected results, a negative
test, and cleanup instructions.

## Chapters

1. [Building the Enterprise Developer Workstation](chapters/01-building-the-enterprise-developer-workstation.md) — reproducible workstation configuration, package management, version managers, Git identity and commit signing, and container runtime setup.
2. [Repository Architecture](chapters/02-repository-architecture.md) — monorepo/polyrepo/hybrid topologies, directory-layout contracts, CODEOWNERS, branch protection, and pre-commit structural validation.
3. [Automation Architecture](chapters/03-automation-architecture.md) — the layered local/CI/CD/infrastructure automation stack, declarative vs. imperative automation, OIDC federation, and separating plan from apply.
4. [GitHub Project and Workflow Management](chapters/04-github-project-and-workflow-management.md) — issues, labels, milestones, Projects (v2), pull request linkage, required reviews, and merge queues.
5. [Documentation Pipelines and Publishing](chapters/05-documentation-pipelines-and-publishing.md) — the docs-as-code model, Markdown as source of truth, multi-format Pandoc builds, and validated static-site publishing.
6. [Understanding Enterprise Infrastructure](chapters/06-understanding-enterprise-infrastructure.md) — what distinguishes enterprise infrastructure, the domain taxonomy this encyclopedia is organized around, consumption models, and availability vocabulary.
7. [Enterprise Architecture Fundamentals](chapters/07-enterprise-architecture-fundamentals.md) — TOGAF's Architecture Development Method, the Zachman Framework, the BDAT domains, Architecture Decision Records, and architecture governance.
8. [Infrastructure Lifecycle Management](chapters/08-infrastructure-lifecycle-management.md) — lifecycle stages mapped to the ITIL 4 service value chain, CMDB and ITAM, change management, patch and capacity management, and secure decommissioning.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all eight chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.

## Software and platform baseline

Chapters in this volume reference the dated baseline recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md) (Node.js, pnpm, and
Pandoc for the publishing toolchain; Terraform and Ansible for the
automation examples). Update that file, not individual chapters, when the
baseline changes.

## Building and validating this volume

From the repository root, after completing
[SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-01-enterprise-engineering-foundations

# Build a single chapter.
scripts/bash/build-book.sh --format all \
  --chapter volumes/volume-01-enterprise-engineering-foundations/chapters/06-understanding-enterprise-infrastructure.md
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
