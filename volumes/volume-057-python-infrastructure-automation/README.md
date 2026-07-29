# Volume LVII — Python for Infrastructure and Automation

> Python as the infrastructure engineer's toolkit, end to end — environments, the core
> language for data-shaping, config formats, system interaction, APIs/HTTP, CLI tools,
> concurrency, testing, and packaging — with hands-on, runnable labs targeting Python
> 3.12+.

## Overview

Volume LVII is a hands-on guide to **Python for infrastructure and automation** — not a
generic language tutorial, but the subset and patterns an operations/platform engineer
uses daily: calling APIs, parsing config, orchestrating processes, and shipping reliable
CLI tools. It underpins the encyclopedia's **automation** (IX) volume and the tools built
on Python throughout (Ansible, NetBox's `pynetbox`, cloud SDKs).

Like the other tool/skills volumes, this is a **product/skills** volume — organized by
capability, with a **runnable walkthrough lab for every major functional area**. It
targets **Python 3.12+** (3.13 is the current stable series) and every lab runs with a
stock `python3` plus a few `pip` packages, so it is reproducible for free.

Chapters are organized by capability:

- **Chapter 01** covers environments and setup (`venv`, `pip`, `pyproject.toml`).
- **Chapter 02** covers the core language for automation (data shaping, errors).
- **Chapter 03** covers files and data formats (JSON, YAML, TOML, CSV, `pathlib`).
- **Chapter 04** covers system interaction (`subprocess`, env, files).
- **Chapter 05** covers APIs and HTTP (`requests`, auth, pagination, retries).
- **Chapter 06** covers building CLI tools (`argparse`, `click`, logging, packaging).
- **Chapter 07** covers concurrency for I/O-bound automation (`concurrent.futures`,
  `asyncio`).
- **Chapter 08** covers testing and quality (`pytest`, mocking, `ruff`/`mypy`).
- **Chapter 09** covers packaging, distribution, and keeping current.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on
labs and knowledge checks.

## Chapters

1. [Python for Infrastructure — Setup and Environments](chapters/01-python-for-infrastructure-setup-and-environments.md) — venv, pip, pyproject.
2. [Core Language for Automation](chapters/02-core-language-for-automation.md) — data structures, comprehensions, typed functions, errors.
3. [Files, Config, and Data Formats](chapters/03-files-config-and-data-formats.md) — pathlib, JSON, YAML, TOML, CSV.
4. [Interacting with the System](chapters/04-interacting-with-the-system.md) — subprocess, environment, files.
5. [Working with APIs and HTTP](chapters/05-working-with-apis-and-http.md) — requests, auth, pagination, retries.
6. [Building CLI Tools](chapters/06-building-cli-tools.md) — argparse, click, logging, entry points.
7. [Concurrency for I/O-bound Automation](chapters/07-concurrency-for-io-bound-automation.md) — threads, asyncio, bounding.
8. [Testing and Quality](chapters/08-testing-and-quality.md) — pytest, fixtures, mocking, ruff/mypy.
9. [Packaging, Distribution, and Keeping Current](chapters/09-packaging-distribution-and-keeping-current.md) — pyproject, wheels, pipx, versions.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Lab coverage

There is a **runnable walkthrough lab for every major functional area** — **35 labs**
across the nine chapters. The walkthroughs use the real toolchain — the **standard
library**, **`requests`**, **`click`**, **`pytest`**, **`ruff`/`mypy`**, and the packaging
tools (**`build`**, **`pipx`**) — all runnable with a stock `python3`. Each lab states an
objective, code, expected results, a negative test, and cleanup, and ends with a
**`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **docs.python.org** (the language and standard library), **Python
3.12+** (3.13 stable), and the common ecosystem (`requests`, `pyyaml`, `click`, `pytest`,
`ruff`, `mypy`, `build`, `pipx`). Python ships a new minor release yearly, so target
supported versions — the 3.12+ baseline was current as of 27 July 2026.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-057-python-infrastructure-automation
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
