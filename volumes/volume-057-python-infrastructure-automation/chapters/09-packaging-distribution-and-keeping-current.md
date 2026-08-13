# Chapter 09: Packaging, Distribution, and Keeping Current

## Learning Objectives

- Structure and build a package with `pyproject.toml`.
- Distribute tools with pipx and the modern toolchain.
- Manage environments and versions reproducibly.
- Track Python releases and the ecosystem.
- Complete a walkthrough for each packaging skill.

## Theory and Architecture

To share automation, **package** it: a `pyproject.toml` declares metadata, dependencies,
and entry points; **`build`** produces a wheel; distribution goes to an internal index or
PyPI. End users install CLI tools in isolation with **`pipx`** (each tool in its own
venv). The modern toolchain increasingly uses **`uv`** (a fast resolver/installer/venv
manager) alongside `pip`/`venv`. Python itself ships a **new minor release yearly**
(3.12, 3.13, …) with a defined support window — track it and test against supported
versions.

## Design Considerations

Declare everything in **`pyproject.toml`** (deps, entry points, metadata), **pin** for
reproducibility (lockfiles via `uv`/`pip-tools`), install CLI tools with **`pipx`**, and
keep to **supported Python versions**. Test against the versions you deploy on.

## Implementation and Automation

The labs build a package, install with pipx, and check the Python version status.

## Validation and Troubleshooting

Confirm the toolchain:

```text
Build: python -m build -> dist/*.whl. Install a CLI tool isolated: pipx install <tool>.
Fast toolchain: uv venv / uv pip install / uv run. Track: supported Python 3.x versions.
```

Common pitfalls: distributing a bare script (no deps/entry point); and running an
**end-of-life** Python.

## Security and Best Practices

Package with **`pyproject.toml`**, **pin/lock** dependencies, distribute CLI tools via
**`pipx`**, and stay on **supported** Python versions (patch promptly). Sign/verify
internal artifacts where required.

## Hands-On Lab

Packaging walkthroughs. **Shared prerequisites** — Python 3.12+ (`pip install build
pipx`). **Cost:** none.

### Lab 9.1 — A minimal pyproject.toml

**Objective:** Declare a buildable package.

```toml
[project]
name = "mytool"
version = "0.1.0"
dependencies = ["requests>=2.31"]
[project.scripts]
mytool = "mytool.cli:main"
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**Expected result:** a valid **`pyproject.toml`** with deps and an entry point — a
buildable package.

**Negative test:** ship a lone `.py` with imports and no metadata; users can't install
its **deps/command** — package it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Build a wheel

**Objective:** Produce a distributable artifact.

```bash
python -m build
ls dist/*.whl
```

**Expected result:** a **`.whl`** under `dist/` — a distributable package.

**Negative test:** email a zip of source; a **wheel** installs cleanly with deps —
distribute that.

**Rollback:** `rm -rf dist build *.egg-info`.

### Lab 9.3 — Install a CLI tool with pipx

**Objective:** Install a tool in isolation.

```bash
pipx install ruff
ruff --version
```

**Expected result:** `ruff` installed in its **own venv** and on PATH — isolated tool
distribution.

**Negative test:** `pip install` CLI tools into system Python; **pipx** isolates each —
avoid dependency collisions.

**Rollback:** `pipx uninstall ruff`.

### Lab 9.4 — Check the Python version status

**Objective:** Confirm you're on a supported version.

```bash
python --version
python -c "import sys; print('supported (3.12+):', sys.version_info[:2] >= (3,12))"
```

**Expected result:** a **3.12+** version and **`supported: True`** — a current runtime.

**Negative test:** run an **end-of-life** Python (e.g., 3.8); upgrade to a **supported**
release for security fixes.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Distribution means packaging with `pyproject.toml`, building wheels, installing CLI tools
isolated with `pipx` (or the fast `uv` toolchain), and staying on supported Python
versions. This chapter packaged, built, installed, and version-checked.

- [ ] I can declare a package in pyproject.toml.
- [ ] I can build a wheel.
- [ ] I can install CLI tools with pipx.
- [ ] I can confirm a supported Python version.
- [ ] I completed Labs 9.1–9.4 including each negative test.
