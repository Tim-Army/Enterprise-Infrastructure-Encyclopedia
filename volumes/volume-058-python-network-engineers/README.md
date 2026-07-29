# Volume LVIII — Python for Network Engineers

> The network engineer's Python stack, end to end — Netmiko, output parsing, NAPALM,
> NETCONF/RESTCONF, Jinja2 templating, Nornir, pyATS/Genie validation, and GitOps CI —
> with hands-on labs targeting the modern network-automation ecosystem.

## Overview

Volume LVIII is a hands-on guide to **Python for network engineers** — the network-
specific automation stack that turns box-by-box CLI into programmable, source-of-truth-
driven operations. It builds on the general Python skills of Volume LVII and complements
the network foundations (II, III), automation (IX), and NetBox (LII) volumes.

Like the other tool/skills volumes, this is a **product/skills** volume — organized by
capability, with a **walkthrough lab for every major functional area**. It targets the
current network-automation ecosystem (Netmiko, NAPALM, ncclient, Nornir, Genie, Jinja2)
on **Python 3.12+**; parsing and templating labs run locally, while device labs show
runnable patterns against a virtual lab (containerlab / vendor sandboxes).

Chapters are organized by capability:

- **Chapter 01** frames the landscape and sets up the environment/lab.
- **Chapter 02** covers **SSH automation** with Netmiko.
- **Chapter 03** covers **parsing device output** (TextFSM, Genie, TTP).
- **Chapter 04** covers **multi-vendor abstraction** with NAPALM.
- **Chapter 05** covers **NETCONF and RESTCONF** (model-driven).
- **Chapter 06** covers **configuration templating** with Jinja2.
- **Chapter 07** covers **scaling with Nornir**.
- **Chapter 08** covers **testing and validation** (pyATS/Genie, pytest).
- **Chapter 09** covers **CI/CD, source of truth, and keeping current**.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on
labs and knowledge checks.

## Chapters

1. [Python for Network Automation — Landscape and Setup](chapters/01-python-for-network-automation-landscape-and-setup.md) — the stack, methods, and lab.
2. [SSH Automation with Netmiko](chapters/02-ssh-automation-with-netmiko.md) — connect, read, configure, scale.
3. [Parsing Device Output](chapters/03-parsing-device-output.md) — TextFSM/ntc-templates, TTP, Genie, regex.
4. [Multi-vendor Abstraction with NAPALM](chapters/04-multi-vendor-abstraction-with-napalm.md) — getters, merge/replace, diff, rollback.
5. [NETCONF and RESTCONF](chapters/05-netconf-and-restconf.md) — model-driven management with YANG.
6. [Configuration Templating with Jinja2](chapters/06-configuration-templating-with-jinja2.md) — intent to config.
7. [Scaling with Nornir](chapters/07-scaling-with-nornir.md) — inventory, tasks, parallelism, plugins.
8. [Testing and Validation](chapters/08-testing-and-validation.md) — pre/post checks, Genie diff, pytest.
9. [CI/CD, Source of Truth, and Keeping Current](chapters/09-cicd-source-of-truth-and-keeping-current.md) — GitOps for networks.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Lab coverage

There is a **walkthrough lab for every major functional area** — **35 labs** across the
nine chapters. The walkthroughs use the real network-automation stack — **Netmiko**,
**TextFSM/ntc-templates/TTP**, **NAPALM**, **ncclient/RESTCONF**, **Jinja2**, **Nornir**,
and **pyATS/Genie** — with parsing/templating labs fully runnable locally and device labs
shown as runnable patterns against a virtual lab. Each lab states an objective, code,
expected results, a negative test, and cleanup, and ends with a
**`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references the network-automation library docs (Netmiko, NAPALM, ncclient,
Nornir, Genie/pyATS, Jinja2), **Python 3.12+**, and a virtual lab (containerlab or vendor
sandboxes). The ecosystem evolves quickly, so track library releases; the stack was
current as of 27 July 2026.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-058-python-network-engineers
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
