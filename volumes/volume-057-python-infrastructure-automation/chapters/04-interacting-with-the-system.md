# Chapter 04: Interacting with the System

## Learning Objectives

- Run external commands safely with `subprocess`.
- Capture output and check exit codes.
- Read environment variables and manage files.
- Avoid shell-injection pitfalls.
- Complete a walkthrough for each system-interaction skill.

## Theory and Architecture

Automation frequently **shells out** to existing tools (`git`, `kubectl`, `terraform`) or
manipulates the filesystem. The modern interface is **`subprocess.run`** — it runs a
command (as an **argument list**, not a shell string), captures **stdout/stderr**, and
reports the **exit code**. Configuration comes from **environment variables**
(`os.environ`), and file operations use **`pathlib`**/**`shutil`**. The cardinal rule:
pass commands as lists and avoid `shell=True` with untrusted input to prevent
**injection**.

## Design Considerations

Run commands as **argument lists** (`["git","status"]`), capture output with
`capture_output=True, text=True`, and check **`returncode`** (or `check=True` to raise on
failure). Read secrets/config from **environment variables**, not hard-coded values.

## Implementation and Automation

The labs use subprocess, environment variables, and file operations.

## Validation and Troubleshooting

Confirm the skills:

```text
subprocess.run(["cmd","arg"], capture_output=True, text=True, check=True)
-> .stdout / .stderr / .returncode. Env: os.environ.get("VAR").
Files: Path.write_text/read_text; shutil.copy/move.
```

Common pitfalls: `shell=True` with interpolated input (**injection**); and ignoring the
exit code.

## Security and Best Practices

Pass commands as **lists** (never build shell strings from input), use **`check=True`**
to fail on error, read config from **env vars**, and handle timeouts. Avoid `shell=True`
unless you fully control the string.

## Hands-On Lab

System-interaction walkthroughs. **Shared prerequisites** — Python 3.12+; a shell with
common tools. **Cost:** none.

### Lab 4.1 — Run a command and capture output

**Objective:** Run a command as an argument list.

```python
import subprocess
r = subprocess.run(["echo", "hello infra"], capture_output=True, text=True)
print("out:", r.stdout.strip(), "rc:", r.returncode)
```

**Expected result:** **`out: hello infra rc: 0`** — captured output and a success code.

**Negative test:** `subprocess.run(f"echo {user_input}", shell=True)`; that risks
**injection** — use an argument list.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — Check exit codes

**Objective:** Fail the script when a command fails.

```python
import subprocess
try:
    subprocess.run(["false"], check=True)
except subprocess.CalledProcessError as e:
    print("command failed with rc", e.returncode)   # rc 1
```

**Expected result:** the caught failure (**rc 1**) — exit-code-aware automation.

**Negative test:** ignore `returncode`; a failed step **passes silently** — use
`check=True`.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.3 — Read environment variables

**Objective:** Get config from the environment.

```python
import os
token = os.environ.get("API_TOKEN", "<unset>")
print("token set:", token != "<unset>")
```

**Expected result:** whether **`API_TOKEN`** is set — externalized config/secret.

**Negative test:** hard-code a token in the script; read it from the **environment** so
secrets stay out of code.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.4 — File operations

**Objective:** Write and read a file with pathlib.

```python
from pathlib import Path
Path("state.txt").write_text("ok\n")
print(Path("state.txt").read_text().strip())   # ok
```

**Expected result:** **`ok`** written and read back — simple, portable file I/O.

**Negative test:** `open()` without a context manager and forget to close; **`write_text`/
`read_text`** (or `with`) close reliably — use them.

**Rollback:** `Path("state.txt").unlink()`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

System interaction is `subprocess.run` (argument lists, captured output, checked exit
codes), environment variables for config/secrets, and `pathlib`/`shutil` for files — all
avoiding shell injection. This chapter ran commands, checked codes, read env, and did
file I/O.

- [ ] I can run commands as argument lists.
- [ ] I can check exit codes and fail on error.
- [ ] I can read config from environment variables.
- [ ] I can do file I/O with pathlib.
- [ ] I completed Labs 4.1–4.4 including each negative test.
