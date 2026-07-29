# Volume XLII — HashiCorp Certification Tracks

> The whole HashiCorp certification program in one volume — the Terraform and
> Vault Associate and Professional exams — with a walkthrough lab for every exam
> objective, verified against the official HashiCorp exam objectives, plus the
> retired Consul track and the wider stack.

## Overview

Volume XLII maps the **HashiCorp** (now an **IBM company**) certification
program — the credentials for **infrastructure as code** (Terraform) and
**secrets management** (Vault). These skills cut across every cloud and platform:
Terraform is the lingua franca of multi-cloud provisioning and Vault a leading
secrets platform, so this volume sits alongside the encyclopedia's **automation
(IX)** and **cloud (XVII/XXXIII/XXXIV)** volumes.

This is a **certification-tracks** volume, like CompTIA (XXXIX), ISC2 (XL), and
CNCF/Kubernetes (XLI): its job is to map the program — which credentials exist,
their **exam objectives**, tiers, mechanics, and validity — and to teach each
objective with a hands-on walkthrough. Every objective in this volume was
**verified against the official HashiCorp exam objectives on 26 July 2026**,
which matters because the program changes: **Terraform Associate moved to 004**,
**Vault Associate to 003**, and the **Consul Associate exam retired on 15 July
2026**, leaving Terraform and Vault as the only certified products.

Chapters are organized by product, tier, and the wider stack:

- **Chapter 01** frames the whole program — the two products and two tiers,
  Associate vs lab-based Professional, two-year validity, and the IBM era.
- **Chapters 02–03** take Terraform: the Associate (004) and the Authoring and
  Operations Professional.
- **Chapters 04–05** take Vault: the Associate (003) and the Operations
  Professional.
- **Chapter 06** covers Consul (Associate retired) and the wider stack (Nomad,
  Packer, Boundary).
- **Chapter 07** covers keeping current — recertification, version bumps,
  retirements, and career paths.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-objective
hands-on labs and knowledge checks.

## Chapters

1. [The HashiCorp Certification Program](chapters/01-the-hashicorp-certification-program.md) — the two products and two tiers, Associate vs Professional, two-year validity, and the IBM acquisition.
2. [Terraform Associate (004)](chapters/02-terraform-associate-004.md) — infrastructure as code fundamentals; eight objectives.
3. [Terraform Authoring and Operations Professional](chapters/03-terraform-authoring-and-operations-professional.md) — advanced, lab-based authoring and operations; six objectives.
4. [Vault Associate (003)](chapters/04-vault-associate-003.md) — secrets management fundamentals; nine objectives.
5. [Vault Operations Professional](chapters/05-vault-operations-professional.md) — production Vault operations, lab-based; eight objectives.
6. [Consul and the Wider HashiCorp Stack](chapters/06-consul-and-the-wider-hashicorp-stack.md) — service discovery and mesh (Consul Associate retired 15 July 2026) plus Nomad, Packer, and Boundary.
7. [Keeping the HashiCorp Program Current and Career Paths](chapters/07-keeping-the-hashicorp-program-current-and-career-paths.md) — recertification, version bumps, retirements, and paths.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all seven chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for HashiCorp, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The full catalog
with the four active exams, objectives, mechanics, two-year validity, and the
HashiCorp Learn training model is in the
[HashiCorp certification appendix](../volume-997-master-appendices/chapters/16-appendix-hashicorp-certifications-and-course-access.md)
(Master Appendices, Volume CMXCVII). Deeper hands-on practice with these tools lives
in the automation (IX) and cloud (XVII/XXXIII/XXXIV) volumes.

## Lab coverage

The credential chapters go **per topic**: there is **one walkthrough lab for
every exam objective of every active HashiCorp credential** — **31 objective
labs** across the four exams (Terraform Associate 8, Terraform Professional 6,
Vault Associate 9, Vault Operations Professional 8) — plus Consul and
wider-stack labs in Chapter 06 and the program and currency labs in Chapters 01
and 07. Because these are hands-on infrastructure credentials, the walkthroughs
use the real CLIs — **`terraform`** (with the `local`/`random`/`null` providers,
no cloud account required), **`vault`** (against a local `-dev` server), and
**`consul`** (a local `-dev` agent) — as concrete demonstrations of each
objective. Each lab states an objective, commands, expected results, a negative
test, and cleanup, and ends with a **`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **HashiCorp Developer** (`developer.hashicorp.com`), the
official **HashiCorp Learn** tutorials, and the **Terraform**, **Vault**, and
**Consul** CLIs. Exam objectives, versions, and status were verified against
developer.hashicorp.com on 26 July 2026; HashiCorp bumps exam versions and
prunes the lineup, so confirm the current version and status before scheduling.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-042-hashicorp-certifications
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
