# Chapter 04: Multi-vendor Abstraction with NAPALM

## Learning Objectives

- Explain what NAPALM abstracts across vendors.
- Retrieve state with getters.
- Apply configuration with merge and replace.
- Preview diffs and roll back changes.
- Complete a walkthrough for each NAPALM skill.

## Theory and Architecture

**NAPALM** (Network Automation and Programmability Abstraction Layer with Multivendor
support) gives a **single API** across drivers (`ios`, `eos`, `junos`, `nxos_ssh`, …). Its
two halves: **getters** return normalized structured state (`get_facts`, `get_interfaces`,
`get_bgp_neighbors`) in the same shape regardless of vendor; and **configuration
management** loads candidate config with **merge** (add to running) or **replace** (make
running match the file), shows a **diff** before you commit, and supports **rollback**.
This diff-and-commit model makes changes safe and reviewable.

## Design Considerations

Use **getters** for read-only inventory/state in a vendor-neutral shape. For changes,
prefer **`load_replace_candidate`** (declarative — running matches intended) with
**`compare_config`** to review the diff, then **`commit_config`**; keep **rollback**
ready. Use **merge** for additive changes.

## Implementation and Automation

The labs use NAPALM getters, config merge/replace, diff, and rollback.

## Validation and Troubleshooting

Confirm the model:

```text
driver = get_network_driver("ios"); dev.open()
Getters: dev.get_facts()/get_interfaces()/... (normalized).
Config: load_merge_candidate / load_replace_candidate -> compare_config -> commit_config / discard_config; rollback().
```

Common pitfalls: **replace** without reviewing the diff (unintended removals); and no
**rollback** plan.

## Security and Best Practices

Read with **getters**, always **`compare_config`** before commit, prefer **declarative
replace** for intended-state, keep **rollback** available, and test in a lab. Store the
intended config in source control.

## Hands-On Lab

NAPALM walkthroughs. **Shared prerequisites** — Python 3.12+ (`pip install napalm`); a lab
device (or the patterns shown). **Cost:** none.

### Lab 4.1 — Retrieve facts with a getter

**Objective:** Get normalized device facts.

```python
from napalm import get_network_driver
driver = get_network_driver("ios")
dev = driver("10.0.0.11", "admin", "admin")
dev.open()
print(dev.get_facts()["os_version"])
dev.close()
```

**Expected result:** the OS version in a **normalized** facts dict — vendor-neutral state.

**Negative test:** parse `show version` text per vendor; **getters** return the same shape
everywhere — use them.

**Cleanup:** `dev.close()` (done above).

### Lab 4.2 — Merge configuration

**Objective:** Add config with a merge.

```python
dev.open()
dev.load_merge_candidate(config="interface Loopback101\n description napalm-merge\n")
print(dev.compare_config())   # review the diff
dev.commit_config()
dev.close()
```

**Expected result:** the **diff** shown, then committed — an additive change.

**Negative test:** commit without `compare_config`; **review the diff** first to catch
mistakes.

**Cleanup:** merge `no interface Loopback101` and commit.

### Lab 4.3 — Replace (declarative) and diff

**Objective:** Make running config match a file.

```python
dev.open()
dev.load_replace_candidate(filename="intended_r1.cfg")
diff = dev.compare_config()
print("changes:\n", diff)
dev.discard_config()          # or commit_config() to apply
dev.close()
```

**Expected result:** the full diff between running and intended — declarative
replace-preview.

**Negative test:** `replace` and commit blindly; it can **remove** anything not in the
file — review the diff.

**Cleanup:** `discard_config()` (done above).

### Lab 4.4 — Rollback

**Objective:** Revert to the previous config.

```python
dev.open()
dev.rollback()                # revert the last committed change
dev.close()
```

**Expected result:** the device reverted to the prior config — safe recovery.

**Negative test:** make risky changes with no rollback path; NAPALM's **rollback** undoes
the last commit — keep it available.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

NAPALM abstracts vendors: normalized getters for state, and merge/replace configuration
with diff-preview, commit, and rollback. This chapter read facts, merged and replaced
config with diffs, and rolled back.

- [ ] I can retrieve normalized state with getters.
- [ ] I can merge configuration and review the diff.
- [ ] I can preview a declarative replace.
- [ ] I can roll back a change.
- [ ] I completed Labs 4.1–4.4 including each negative test.
