# Chapter 01: Python for Network Automation — Landscape and Setup

## Learning Objectives

- Explain why Python dominates network automation.
- Map the network-automation library landscape.
- Choose a connection method (CLI/SSH, NETCONF, RESTCONF).
- Set up a reproducible lab and environment.
- Verify the toolchain.

## Theory and Architecture

Network engineering has shifted from box-by-box CLI to **programmable, source-of-truth-
driven automation**, and **Python** is its lingua franca — readable, with a mature
ecosystem of network libraries. This volume builds on the general Python skills of Volume
LVII and focuses on the **network-specific** stack.

The landscape by connection method:

- **CLI over SSH** — **Netmiko** (multi-vendor SSH), **Scrapli** (fast, async-capable).
- **Multi-vendor abstraction** — **NAPALM** (unified getters + config merge/replace with
  diffs and rollback).
- **Model-driven** — **ncclient** (NETCONF/YANG over SSH) and **RESTCONF** (HTTP/JSON or
  XML).
- **Parsing** — **TextFSM**/**ntc-templates**, **TTP**, and **Genie** parsers turn CLI
  text into structured data.
- **Templating** — **Jinja2** renders configs from data.
- **Orchestration** — **Nornir** (a Python inventory + task framework) and **pyATS/Genie**
  for testing.

Practice on a **virtual lab** (containerlab with cEOS/vJunos/others, or vendor sandboxes)
so labs are reproducible.

## Design Considerations

Prefer **model-driven** interfaces (NETCONF/RESTCONF) where devices support them — they
return structured data and validate config. Fall back to **SSH + parsing** for CLI-only
gear. Drive everything from a **source of truth** (NetBox, Volume LII) rather than
hard-coded values.

## Implementation and Automation

Set up an environment for the network stack:

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install netmiko napalm ncclient nornir jinja2 textfsm ntc-templates
```

## Validation and Troubleshooting

Confirm the landscape:

```text
SSH/CLI: netmiko, scrapli. Abstraction: napalm. Model-driven: ncclient (NETCONF), RESTCONF.
Parsing: textfsm/ntc-templates, TTP, Genie. Templating: jinja2. Orchestration: nornir; testing: pyATS/Genie.
Lab: containerlab / vendor sandboxes.
```

Common pitfalls: screen-scraping CLI where **NETCONF/RESTCONF** is available; and no
lab (untested automation against production).

## Security and Best Practices

Use **model-driven** APIs when possible, store credentials in a vault/env (never in
code), drive from a **source of truth**, and always test in a **lab** before production.
Read-only getters first; config changes with review and rollback.

## References and Knowledge Checks

- The library docs: Netmiko, NAPALM, ncclient, Nornir, Genie; and device platform guides.

**Knowledge checks**

1. When do you prefer NETCONF/RESTCONF over SSH/CLI?
2. What does NAPALM abstract?
3. Why drive automation from a source of truth?

## Hands-On Lab

Setup walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — Python 3.12+; optionally
a lab device (containerlab). **Cost:** none.

### Lab 1.1 — Set up the environment

**Objective:** Install the core network stack.

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install netmiko napalm jinja2 textfsm ntc-templates
python -c "import netmiko, napalm, jinja2; print('net stack ready')"
```

**Expected result:** **`net stack ready`** — the libraries import cleanly.

**Negative test:** `pip install` into system Python; isolate with a **venv** so device
libs don't collide with the OS.

**Rollback:** `deactivate`.

### Lab 1.2 — Choose a connection method

**Objective:** Map devices to the right interface.

```python
methods = {
 "IOS-XE (CLI only role)": "netmiko (SSH) + textfsm parse",
 "IOS-XE (RESTCONF on)": "RESTCONF (requests) or NETCONF (ncclient)",
 "Junos": "NETCONF (ncclient/PyEZ) preferred",
 "Arista EOS": "eAPI (pyeapi) or NETCONF",
}
for k,v in methods.items(): print(f"{k:24}: {v}")
```

**Expected result:** device-to-interface mappings — choosing the right method per platform.

**Negative test:** SSH-scrape a device that offers **NETCONF**; use the structured
interface for reliability.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.3 — Verify a lab device is reachable (optional)

**Objective:** Confirm SSH reachability before automating.

```bash
# Against a lab device (containerlab cEOS/IOL, etc.):
nc -z -w3 <device-ip> 22 && echo "ssh reachable" || echo "unreachable"
```

**Expected result:** **`ssh reachable`** for a running lab device — a target to automate.

**Negative test:** run playbooks against unreachable devices; **check connectivity** first
to fail fast.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Python is the network engineer's automation language; the stack spans SSH/CLI (Netmiko),
abstraction (NAPALM), model-driven interfaces (NETCONF/RESTCONF), parsing (TextFSM/Genie),
templating (Jinja2), and orchestration (Nornir/pyATS), practiced in a virtual lab. This
chapter set up the environment and mapped methods.

- [ ] I can explain Python's role in network automation.
- [ ] I can map the library landscape.
- [ ] I can choose a connection method per platform.
- [ ] I can set up the environment and a lab.
- [ ] I completed Labs 1.1–1.3 including each negative test.
