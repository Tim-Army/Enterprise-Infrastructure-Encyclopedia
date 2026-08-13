# Chapter 01: Python for Infrastructure — Setup and Environments

## Learning Objectives

- Explain why Python is the default language for infrastructure automation.
- Create isolated environments with `venv`.
- Manage dependencies with `pip` and `pyproject.toml`.
- Run scripts and use the REPL for exploration.
- Verify the Python version.

## Theory and Architecture

**Python** is the lingua franca of infrastructure automation: it is readable, has a
vast ecosystem (`requests`, `boto3`, `netmiko`, `ansible`, `pyyaml`), ships on nearly
every OS, and is the scripting language behind major tooling. For operations work its
strengths are glue — calling APIs, parsing config, orchestrating processes — rather than
raw performance.

The foundation is **isolation**: each project gets a **virtual environment** (`venv`)
with its own dependencies, so a tool's requirements never collide with the system Python
or another project. Dependencies are declared in **`pyproject.toml`** (the modern
standard) and installed with **`pip`**. This volume targets **Python 3.12+** (3.13 is
the current stable series).

## Design Considerations

Never `pip install` into the **system Python** — use a **venv** per project. Declare
dependencies explicitly (pin for reproducibility) and keep scripts small and testable.
Prefer the standard library first; reach for third-party packages when they clearly help.

## Implementation and Automation

Create an environment and install a dependency:

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install requests
```

## Validation and Troubleshooting

Confirm the fundamentals:

```text
Isolation: python3 -m venv .venv  ->  activate  ->  pip install ...
Dependencies: pyproject.toml (or requirements.txt); pip freeze to snapshot.
Run: python3 script.py ; explore in the REPL (python3).
```

Common pitfalls: installing into system Python (breaks the OS); and un-pinned deps
(non-reproducible builds).

## Security and Best Practices

Use a **venv per project**, pin dependencies for reproducibility, keep the interpreter
patched, and avoid `sudo pip`. Vet third-party packages before adding them.

## References and Knowledge Checks

- docs.python.org: the tutorial, standard library, and `venv`/`pip` docs.

**Knowledge checks**

1. Why use a virtual environment?
2. Where are modern project dependencies declared?
3. How do you check the running Python version?

## Hands-On Lab

Setup walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — Python 3.12+ (`python3`).
**Cost:** none.

### Lab 1.1 — Create and activate a venv

**Objective:** Make an isolated environment.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -c "import sys; print('venv:', sys.prefix != sys.base_prefix)"
```

**Expected result:** **`venv: True`** — an active isolated environment.

**Negative test:** `pip install` without a venv into system Python; it can **break OS
tooling** — always isolate.

**Rollback:** `deactivate && rm -rf .venv`.

### Lab 1.2 — Install and pin a dependency

**Objective:** Add a dependency and snapshot it.

```bash
pip install requests
pip freeze | grep -i requests
```

**Expected result:** a pinned line like **`requests==2.x.y`** — a reproducible dependency.

**Negative test:** ship code depending on `requests` with no declared dependency; it
**fails on a clean machine** — declare/pin it.

**Rollback:** none (inside the venv).

### Lab 1.3 — Verify the version and run a script

**Objective:** Confirm the interpreter and run code.

```bash
python --version
echo 'print("infra automation ready")' > hello.py
python hello.py
```

**Expected result:** a **3.12+** version and the script output — a working toolchain.

**Negative test:** assume `python` is Python 3; on some systems `python` is 2 or absent —
use **`python3`**/the venv and check `--version`.

**Rollback:** `rm hello.py`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Python is the default infrastructure-automation language for its readability and
ecosystem; the foundation is per-project isolation with `venv`, explicit dependencies in
`pyproject.toml`/`pip`, and a known interpreter version. This chapter created an
environment, pinned a dependency, and ran a script.

- [ ] I can explain why Python suits infra automation.
- [ ] I can create and activate a venv.
- [ ] I can install and pin dependencies.
- [ ] I can verify the version and run scripts.
- [ ] I completed Labs 1.1–1.3 including each negative test.
