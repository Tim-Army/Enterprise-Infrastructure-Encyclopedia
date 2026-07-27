# Volume LII — NetBox Community Edition

> The open-source network source of truth, end to end — DCIM, IPAM, virtualization,
> circuits, tenancy, customization, and API-driven automation — with hands-on
> `pynetbox`/REST/GraphQL labs against a `netbox-docker` deployment, pinned to the
> NetBox 4.6.x Community release.

## Overview

Volume LII is a hands-on guide to **NetBox Community Edition**, the open-source
(Apache-2.0) **network source of truth (NSoT)** for IP address management (IPAM),
data-center infrastructure (DCIM), and the automation built on top of them. It sits
with the encyclopedia's **network** and **automation** volumes (Network Engineering
Foundations II, Automation IX, Observability XI) — NetBox is the intended-state data
model those disciplines reconcile against.

Unlike the certification-tracks volumes, this is a **product/skills** volume: it teaches
the tool itself, organized by capability, with a **walkthrough lab for every major
functional area**. It targets the **4.6.x** Community series (latest release verified on
github.com/netbox-community/netbox on 27 July 2026) and runs on the community
**`netbox-docker`** project, so every lab is reproducible for free.

Chapters are organized by capability:

- **Chapter 01** introduces NetBox, its architecture, and standing it up.
- **Chapters 02–03** cover **DCIM** — sites/racks/devices, then interfaces/cabling/
  power.
- **Chapter 04** covers **IPAM** — prefixes, addresses, VLANs, and VRFs.
- **Chapter 05** covers **virtualization, circuits, and tenancy**.
- **Chapter 06** covers **customization** — custom fields, tags, and config contexts.
- **Chapter 07** covers **automation** — REST, GraphQL, and event rules.
- **Chapter 08** covers **operations** — permissions, change logging, and upgrades.
- **Chapter 09** covers **integration and keeping current** — Ansible, Terraform,
  plugins.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on
labs and knowledge checks.

## Chapters

1. [Introduction and Architecture](chapters/01-introduction-and-architecture.md) — NSoT, the stack, and standing up NetBox.
2. [DCIM — Sites, Racks, and Devices](chapters/02-dcim-sites-racks-and-devices.md) — the physical hierarchy and device types.
3. [DCIM — Interfaces, Cabling, and Power](chapters/03-dcim-interfaces-cabling-and-power.md) — components, cables/tracing, and power.
4. [IPAM — Prefixes, Addresses, VLANs, and VRFs](chapters/04-ipam-prefixes-addresses-vlans-and-vrfs.md) — logical addressing and allocation.
5. [Virtualization, Circuits, and Tenancy](chapters/05-virtualization-circuits-and-tenancy.md) — VMs, WAN circuits, and ownership.
6. [Customization — Fields, Tags, and Config Contexts](chapters/06-customization-fields-tags-and-config-contexts.md) — extending the model.
7. [Automation — REST, GraphQL, and Event Rules](chapters/07-automation-rest-graphql-and-event-rules.md) — the API surfaces and webhooks.
8. [Operations — Permissions, Change Logging, and Upgrades](chapters/08-operations-permissions-change-logging-and-upgrades.md) — access, audit, lifecycle.
9. [Integration, Plugins, and Keeping Current](chapters/09-integration-plugins-and-keeping-current.md) — Ansible, Terraform, plugins, releases.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Lab coverage

There is a **walkthrough lab for every major functional area** — **35 labs** across the
nine chapters. Because NetBox is API-first, the walkthroughs use the real tooling — the
**`pynetbox`** Python SDK, the **REST API** (`curl`), and the **GraphQL API** — plus
**Ansible** and **Terraform** for integration, all against a local **`netbox-docker`**
deployment (NetBox 4.6.x). Each lab states an objective, commands, expected results, a
negative test, and cleanup, and ends with a **`**Lab verified by:** *pending*`**
sign-off.

## Software and platform baseline

This volume references **github.com/netbox-community/netbox** and
**docs.netbox.dev** (the open-source project and docs), the **`netbox-docker`**
deployment project, and **NetBox Community 4.6.x**. NetBox releases frequently, so
confirm the running version (`/api/status/`) — the latest release was verified on
27 July 2026.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-52-netbox-community
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
