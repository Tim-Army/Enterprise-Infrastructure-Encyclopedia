# Chapter 03: Files, Config, and Data Formats

## Learning Objectives

- Work with paths and files using `pathlib`.
- Read and write JSON, the API/config lingua franca.
- Parse YAML and TOML configuration.
- Process CSV inventory data.
- Complete a walkthrough for each format.

## Theory and Architecture

Infrastructure scripts constantly read and write **structured data**: JSON from APIs,
YAML for config (Kubernetes, Ansible), TOML for tool config (`pyproject.toml`), and CSV
for inventories/exports. The standard library covers **`json`**, **`tomllib`** (read),
and **`csv`**; **YAML** needs the third-party `pyyaml`. File and path handling is done
with **`pathlib`** (object-oriented paths) rather than string manipulation.

## Design Considerations

Use **`pathlib.Path`** for portable path handling, **`json`** for API payloads, **YAML**
for human-edited config, and **`tomllib`** to read tool config. Always handle files with
context managers (`with open(...)`) so they close reliably.

## Implementation and Automation

The labs use pathlib, json, yaml, and csv on ops data.

## Validation and Troubleshooting

Confirm the tools:

```text
Paths: pathlib.Path. JSON: json.load/dump. YAML: yaml.safe_load (pyyaml).
TOML: tomllib.load (read-only, stdlib 3.11+). CSV: csv.DictReader/DictWriter.
```

Common pitfalls: `yaml.load` without `safe_load` (arbitrary object construction); and
string path concatenation instead of `pathlib`.

## Security and Best Practices

Always **`yaml.safe_load`** untrusted YAML, use **`pathlib`** for paths, open files with
**context managers**, and validate parsed data before use. Never `eval` config.

## Hands-On Lab

Data-format walkthroughs. **Shared prerequisites** — Python 3.12+ (`pip install pyyaml`).
**Cost:** none.

### Lab 3.1 — Paths with pathlib

**Objective:** Build and inspect a path.

```python
from pathlib import Path
p = Path("configs") / "prod" / "app.yaml"
print(p.suffix, p.parent, p.name)   # .yaml configs/prod app.yaml
```

**Expected result:** the suffix, parent, and name — object-oriented path handling.

**Negative test:** join paths with `+ "/"` strings; **pathlib** handles separators
portably (Windows/POSIX) — use it.

**Cleanup:** none.

### Lab 3.2 — Read/write JSON

**Objective:** Round-trip a record through JSON.

```python
import json
data = {"host":"web1","tags":["prod","web"]}
s = json.dumps(data)
back = json.loads(s)
print(back["tags"][0])   # prod
```

**Expected result:** **`prod`** after a dumps/loads round-trip — the API data format.

**Negative test:** build JSON by string formatting; **`json.dumps`** escapes correctly —
never hand-format JSON.

**Cleanup:** none.

### Lab 3.3 — Parse YAML config

**Objective:** Load a YAML document safely.

```python
import yaml
doc = yaml.safe_load("service:\n  name: web\n  replicas: 3\n")
print(doc["service"]["replicas"])   # 3
```

**Expected result:** **`3`** parsed from YAML — human-edited config loaded.

**Negative test:** use `yaml.load` on untrusted input; it can **construct arbitrary
objects** — always `safe_load`.

**Cleanup:** none.

### Lab 3.4 — Process CSV inventory

**Objective:** Read an inventory with DictReader.

```python
import csv, io
raw = "name,ip\nweb1,10.0.0.1\nweb2,10.0.0.2\n"
rows = list(csv.DictReader(io.StringIO(raw)))
print(rows[1]["ip"])   # 10.0.0.2
```

**Expected result:** **`10.0.0.2`** from the second row — structured CSV access.

**Negative test:** `split(",")` the lines by hand; **`csv`** handles quoting/escaping —
use it for real data.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Infra scripts read/write structured data — JSON (APIs), YAML (config), TOML (tool
config), CSV (inventory) — with `pathlib` for paths and context managers for files. This
chapter round-tripped each format safely.

- [ ] I can handle paths with pathlib.
- [ ] I can round-trip JSON.
- [ ] I can safely parse YAML.
- [ ] I can process CSV with DictReader.
- [ ] I completed Labs 3.1–3.4 including each negative test.
