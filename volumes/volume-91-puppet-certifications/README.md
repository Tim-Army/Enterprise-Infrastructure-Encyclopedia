# Volume XCI — Puppet Certification Tracks

> The Puppet certification program in one volume — the Puppet Certified Professional (PPT-PCP-24) across
> the eight exam domains: concepts, the Puppet language, module authoring, Hiera, classification,
> environments, Puppet Enterprise administration, and orchestration with Bolt — with hands-on `puppet
> apply` labs, verified against puppet.com.

## Overview

Volume XCI maps the **Puppet** certification program — the credential for automating and administering
system infrastructure with **Puppet**, the declarative configuration-management platform (now a
**Perforce** company). The program centers on one credential, the **Puppet Certified Professional
(PPT-PCP-24)**, whose exam spans eight domains from the core concepts and the Puppet language to module
authoring, Hiera data separation, classification, environments, Puppet Enterprise administration, and
orchestration with Bolt. This volume continues the encyclopedia's DevOps & observability cluster and
complements Ansible (LIX) as the other major configuration-management platform.

This is a **certification-tracks** volume, like the other vendor volumes (XXXIX–XC): it maps the program
— the credential and its exam domains — and teaches each with a hands-on `puppet` walkthrough. The
certification and exam details were **verified against puppet.com on 29 July 2026** (the certification
and exam-details pages), and the exam is based on **Open Source Puppet 8.9+ and Puppet Enterprise
2023.8+**; third-party exam-dump sites were excluded as sources.

Chapters follow the exam domains:

- **Chapter 01** frames the program — the PCP exam, delivery, and the declarative, idempotent Puppet model.
- **Chapter 02** takes **Concepts** — resource abstraction, idempotence, facts, the catalog, and the agent lifecycle.
- **Chapter 03** takes the **Puppet Language** — resources, classes, defined types, variables, and dependencies.
- **Chapter 04** takes **Module Authoring** — module structure, the Forge, roles and profiles, and testing.
- **Chapter 05** takes **Hiera and data separation**.
- **Chapter 06** takes **Classification and Environments** — node classification and code deployment.
- **Chapter 07** takes **Puppet Enterprise Administration** — the primary server, agents, PuppetDB, and reporting.
- **Chapter 08** takes **Orchestration and Tasks** — Bolt, tasks, plans, and the Orchestrator.
- **Chapter 09** takes **Troubleshooting, prep, and career**.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on labs and
knowledge checks.

> **Scope.** Puppet configuration management is authorized infrastructure work — declaratively defining,
> enforcing, and standardizing the desired state of your own systems. Enforcing idempotent desired state
> and correcting drift is defensive administration of your own infrastructure.

## Chapters

1. [The Puppet Certification Program](chapters/01-the-puppet-certification-program.md) — the PCP exam, delivery, and the Puppet model.
2. [Concepts](chapters/02-concepts.md) — resource abstraction, idempotence, facts, the catalog, the agent lifecycle.
3. [The Puppet Language](chapters/03-the-puppet-language.md) — resources, classes, defined types, variables, dependencies.
4. [Module Authoring](chapters/04-module-authoring.md) — module structure, the Forge, roles and profiles, testing.
5. [Hiera and Data Separation](chapters/05-hiera-and-data-separation.md) — the hierarchy, lookup, automatic parameter lookup.
6. [Classification and Environments](chapters/06-classification-and-environments.md) — node classification, directory environments, code deployment.
7. [Puppet Enterprise Administration](chapters/07-puppet-enterprise-administration.md) — primary server, agents, PuppetDB, reporting.
8. [Orchestration and Tasks](chapters/08-orchestration-and-tasks.md) — Bolt, tasks, plans, the Orchestrator.
9. [Troubleshooting, Prep, and Career](chapters/09-troubleshooting-prep-and-career.md) — debugging, exam prep, career.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for Puppet, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md) and the Master Appendices
course-catalog appendix. Every chapter carries one hands-on `puppet` walkthrough lab per exam domain,
verified against puppet.com on 29 July 2026.
