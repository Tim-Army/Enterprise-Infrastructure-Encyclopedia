# Volume LIX — Ansible

> The Ansible automation engine, end to end — architecture, inventory, playbooks,
> variables/facts/templates, roles and collections, control flow, Ansible Vault,
> testing (ansible-lint/Molecule), and scaling with AWX — with hands-on, runnable
> labs targeting ansible-core 2.21.x.

## Overview

Volume LIX is a hands-on guide to **Ansible**, the open-source, agentless automation
engine for configuration management, deployment, and orchestration. It builds on the
Python (LVII) and network-automation (LVIII) volumes and complements the Infrastructure
Automation (IX) volume — Ansible is the declarative, playbook-driven layer of the
automation stack.

Like the other tool/skills volumes, this is a **product/skills** volume — organized by
capability, with a **runnable walkthrough lab for every major functional area**. It
targets **ansible-core 2.21.x** (verified on github.com/ansible/ansible on 27 July 2026);
most labs run locally against `localhost`, so the volume is reproducible for free.

Chapters are organized by capability:

- **Chapter 01** covers the agentless architecture and setup.
- **Chapter 02** covers inventory and connections.
- **Chapter 03** covers playbooks and tasks (idempotence, check mode, handlers).
- **Chapter 04** covers variables, facts, and templates.
- **Chapter 05** covers roles and collections.
- **Chapter 06** covers control flow (conditionals, loops, blocks, tags).
- **Chapter 07** covers secrets with Ansible Vault.
- **Chapter 08** covers testing and quality (ansible-lint, Molecule).
- **Chapter 09** covers scaling, AWX/Automation Platform, and keeping current.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on
labs and knowledge checks.

## Chapters

1. [Ansible Architecture and Setup](chapters/01-ansible-architecture-and-setup.md) — agentless push, components, idempotence.
2. [Inventory and Connections](chapters/02-inventory-and-connections.md) — static/dynamic inventory, group/host vars.
3. [Playbooks and Tasks](chapters/03-playbooks-and-tasks.md) — plays, idempotence, check/diff, handlers.
4. [Variables, Facts, and Templates](chapters/04-variables-facts-and-templates.md) — precedence, facts, register, Jinja2.
5. [Roles and Collections](chapters/05-roles-and-collections.md) — reuse, Galaxy, requirements.yml.
6. [Control Flow](chapters/06-control-flow.md) — when, loop, block/rescue, tags.
7. [Secrets with Ansible Vault](chapters/07-secrets-with-ansible-vault.md) — encrypting vars and files.
8. [Testing and Quality](chapters/08-testing-and-quality.md) — ansible-lint, syntax-check, assert, Molecule.
9. [Scaling, AWX, and Keeping Current](chapters/09-scaling-awx-and-keeping-current.md) — forks/strategies, AWX/AAP, execution environments.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Lab coverage

There is a **runnable walkthrough lab for every major functional area** — **35 labs**
across the nine chapters. The walkthroughs use the real toolchain — **`ansible`**,
**`ansible-playbook`**, **`ansible-inventory`**, **`ansible-galaxy`**, **`ansible-vault`**,
and **`ansible-lint`** — most runnable locally against `localhost`. Each lab states an
objective, code, expected results, a negative test, and cleanup, and ends with a
**`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **docs.ansible.com** and **github.com/ansible** (the project and
docs), **ansible-core 2.21.x**, Ansible **Galaxy** collections, and **AWX / Ansible
Automation Platform**. Ansible ships regular ansible-core releases, so target supported
versions — the 2.21.x baseline was verified on 27 July 2026.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-059-ansible
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
