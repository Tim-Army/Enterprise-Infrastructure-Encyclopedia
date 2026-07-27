# Volume LIII — LibreNMS

> The open-source, auto-discovering network monitoring system, end to end — SNMP
> discovery and polling, alerting, graphing and dashboards, the REST API,
> integrations, and scaling — with hands-on `lnms`/REST/SNMP labs against a
> `librenms-docker` deployment, pinned to the LibreNMS 26.7.x rolling release.

## Overview

Volume LIII is a hands-on guide to **LibreNMS**, the open-source (GPL), agentless,
**SNMP-based network monitoring system**. It sits with the encyclopedia's
**observability and operations** volumes (Observability XI, Gigamon XVIII, Wireshark
XX) and complements the **NetBox** source-of-truth volume (LII): NetBox holds intended
state, LibreNMS observes actual state.

Like NetBox, this is a **product/skills** volume — it teaches the tool, organized by
capability, with a **walkthrough lab for every major functional area**. It targets the
**26.7.x** rolling (CalVer) release (latest verified on
github.com/librenms/librenms on 27 July 2026) and runs on the community
**`librenms-docker`** project, so every lab is reproducible for free.

Chapters are organized by capability:

- **Chapter 01** introduces LibreNMS, its architecture, and standing it up.
- **Chapter 02** covers **adding and discovering devices** (SNMP, groups).
- **Chapter 03** covers **polling and data collection** (poller, RRD, ping).
- **Chapter 04** covers **alerting** (rules, transports, templates, maintenance).
- **Chapter 05** covers **graphing and dashboards**.
- **Chapter 06** covers **the API and automation**.
- **Chapter 07** covers **integrations** (Grafana, Oxidized, syslog, NetBox).
- **Chapter 08** covers **scaling and operations** (distributed polling, rrdcached).
- **Chapter 09** covers **maintenance and keeping current**.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on
labs and knowledge checks.

## Chapters

1. [Introduction and Architecture](chapters/01-introduction-and-architecture.md) — agentless SNMP monitoring, the components, and standing it up.
2. [Adding and Discovering Devices](chapters/02-adding-and-discovering-devices.md) — SNMP onboarding, discovery, and dynamic groups.
3. [Polling and Data Collection](chapters/03-polling-and-data-collection.md) — the poller, RRD/rrdcached, ping, and applications.
4. [Alerting — Rules, Transports, and Templates](chapters/04-alerting-rules-transports-and-templates.md) — conditions, delivery, and maintenance.
5. [Graphing and Dashboards](chapters/05-graphing-and-dashboards.md) — RRD graphs, time ranges, and widgets.
6. [The API and Automation](chapters/06-the-api-and-automation.md) — the REST API, device lifecycle, and Ansible.
7. [Integrations — Grafana, Oxidized, and Syslog](chapters/07-integrations-grafana-oxidized-and-syslog.md) — visualization, config backup, events, NetBox.
8. [Scaling and Operations](chapters/08-scaling-and-operations.md) — distributed polling, rrdcached, and the dispatcher.
9. [Maintenance and Keeping Current](chapters/09-maintenance-and-keeping-current.md) — rolling updates, validation, and backups.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Lab coverage

There is a **walkthrough lab for every major functional area** — **35 labs** across the
nine chapters. Because LibreNMS is API- and CLI-driven, the walkthroughs use the real
tooling — the **`lnms`** CLI, the **REST API** (`curl`), **`snmpget`**, `validate.php`,
and Ansible — all against a local **`librenms-docker`** deployment (LibreNMS 26.7.x).
Each lab states an objective, commands, expected results, a negative test, and cleanup,
and ends with a **`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **github.com/librenms** and **docs.librenms.org** (the
open-source project and docs), the **`librenms-docker`** deployment project, and
**LibreNMS 26.7.x**. LibreNMS is a rolling release, so confirm the running version
(`validate.php` / the API) — the latest release was verified on 27 July 2026.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-53-librenms
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
