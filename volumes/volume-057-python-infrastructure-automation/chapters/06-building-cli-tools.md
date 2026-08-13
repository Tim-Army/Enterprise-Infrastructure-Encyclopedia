# Chapter 06: Building CLI Tools

## Learning Objectives

- Parse arguments with `argparse`.
- Build richer CLIs with `click`.
- Add structured logging.
- Package a command as an entry point.
- Complete a walkthrough for each CLI skill.

## Theory and Architecture

Automation is most useful as **reusable CLI tools**, not one-off scripts. The standard
library **`argparse`** builds argument parsers (positional args, options, subcommands,
help). **`click`** (third-party) offers a more ergonomic, decorator-based API with less
boilerplate. Good tools add **logging** (via the `logging` module, not `print`, with
levels and destinations) and are **packaged** with a **console entry point** in
`pyproject.toml` so they install as a real command.

## Design Considerations

Use **`argparse`** for stdlib-only tools and **`click`** for larger CLIs. Add
**`--verbose`**/log levels via the **`logging`** module (so output is filterable and can
go to files/syslog). Package the tool with an **entry point** so users run `mytool`, not
`python script.py`.

## Implementation and Automation

The labs build an argparse CLI, a click command, logging, and an entry point.

## Validation and Troubleshooting

Confirm the skills:

```text
argparse: parser.add_argument(...); args = parser.parse_args().
click: @click.command() @click.option(...). Logging: logging.getLogger(__name__).
Packaging: [project.scripts] mytool = "pkg.module:main".
```

Common pitfalls: `print` instead of **logging** (no levels/filtering); and hard-coding
config instead of options/env.

## Security and Best Practices

Provide clear **`--help`**, use **logging** with levels (not print), accept config via
**options/env** (secrets via env), and package with an **entry point**. Validate/parse
inputs up front.

## Hands-On Lab

CLI walkthroughs. **Shared prerequisites** — Python 3.12+ (`pip install click`). **Cost:**
none.

### Lab 6.1 — Argparse CLI

**Objective:** Parse a positional arg and an option.

```python
import argparse
p = argparse.ArgumentParser(description="ping a host")
p.add_argument("host")
p.add_argument("--count", type=int, default=3)
args = p.parse_args(["web1", "--count", "5"])
print(args.host, args.count)   # web1 5
```

**Expected result:** **`web1 5`** — parsed arguments with a typed option.

**Negative test:** read `sys.argv` by hand and index it; **argparse** gives validation,
help, and types — use it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.2 — Click command

**Objective:** Build a command with decorators.

```python
import click
@click.command()
@click.argument("host")
@click.option("--count", default=3, help="pings")
def ping(host, count):
    click.echo(f"ping {host} x{count}")
# ping(["web1","--count","2"], standalone_mode=False)
```

**Expected result:** a `ping` command echoing `ping web1 x2` — an ergonomic CLI.

**Negative test:** hand-roll `--help` text and parsing; **click** generates help and
handles parsing — prefer it for bigger CLIs.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.3 — Structured logging

**Objective:** Log at levels instead of printing.

```python
import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
log = logging.getLogger("mytool")
log.info("starting"); log.debug("hidden at INFO level")
```

**Expected result:** the **INFO** line shown, the **DEBUG** line suppressed — leveled,
filterable output.

**Negative test:** `print()` everywhere; **logging** lets you filter by level and route
to files/syslog — use it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.4 — Package an entry point

**Objective:** Declare a console command.

```toml
# pyproject.toml
[project.scripts]
mytool = "mytool.cli:main"
```

**Expected result:** after `pip install .`, a **`mytool`** command on PATH — a real
installable tool.

**Negative test:** tell users to run `python /path/script.py`; an **entry point** gives a
clean command — package it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CLI tools use `argparse` (stdlib) or `click` (ergonomic) for arguments, the `logging`
module for leveled output, and a `pyproject.toml` entry point so they install as real
commands. This chapter built each piece.

- [ ] I can parse arguments with argparse.
- [ ] I can build a click command.
- [ ] I can log at levels instead of printing.
- [ ] I can package a console entry point.
- [ ] I completed Labs 6.1–6.4 including each negative test.
