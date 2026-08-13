# Chapter 02: Core Language for Automation

## Learning Objectives

- Use the core data types operations scripts rely on.
- Transform data with comprehensions.
- Structure code with functions and type hints.
- Handle errors robustly for unattended scripts.
- Complete a walkthrough for each core skill.

## Theory and Architecture

Automation scripts spend most of their time **shaping data**: lists and dicts of hosts,
records, and API responses. The core skills are the built-in **data structures** (list,
dict, set, tuple), **comprehensions** (concise transforms/filters), **functions** with
**type hints** (readable, checkable interfaces), and **exception handling** (so an
unattended script fails predictably rather than crashing mid-run). Idiomatic Python
favors clear, direct data manipulation over verbose loops.

## Design Considerations

Reach for a **dict** to index records by key, a **set** to dedupe/membership-test, and a
**comprehension** to transform a collection in one readable line. Add **type hints** for
maintainability and catch **specific exceptions** (not bare `except`) so real errors
surface.

## Implementation and Automation

The labs use core data structures, comprehensions, typed functions, and exception
handling on ops-shaped data.

## Validation and Troubleshooting

Confirm the core skills:

```text
Structures: list/dict/set/tuple. Comprehension: [f(x) for x in xs if cond].
Functions: def f(x: int) -> str. Errors: try/except SpecificError -> handle/log/raise.
```

Common pitfalls: bare `except:` (hides real errors); and mutating a list while iterating
it.

## Security and Best Practices

Index with **dicts**, dedupe with **sets**, transform with **comprehensions**, annotate
with **type hints**, and catch **specific exceptions** with logging. Fail loudly on
unexpected errors rather than swallowing them.

## Hands-On Lab

Core-language walkthroughs. **Shared prerequisites** — Python 3.12+. **Cost:** none.

### Lab 2.1 — Index records with a dict

**Objective:** Build a lookup keyed by hostname.

```python
hosts = [{"name":"web1","ip":"10.0.0.1"},{"name":"web2","ip":"10.0.0.2"}]
by_name = {h["name"]: h["ip"] for h in hosts}
print(by_name["web2"])   # 10.0.0.2
```

**Expected result:** **`10.0.0.2`** via O(1) lookup — dict indexing.

**Negative test:** scan the list linearly for each lookup; a **dict** is O(1) — index
once.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — Filter with a comprehension

**Objective:** Select matching records concisely.

```python
prod = [h for h in hosts if h["name"].startswith("web")]
print(len(prod))   # 2
```

**Expected result:** the filtered count — a readable one-line transform.

**Negative test:** build the result with an explicit loop + append; a **comprehension**
is clearer for simple filters.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — A typed function

**Objective:** Write a function with type hints.

```python
def ip_for(name: str, table: dict[str, str]) -> str | None:
    return table.get(name)
print(ip_for("web1", by_name))   # 10.0.0.1
```

**Expected result:** the IP for `web1` (or `None`) — a clear, typed interface.

**Negative test:** index with `table[name]` for a missing key; use `.get()` (returns
`None`) or handle **KeyError** — don't crash on absence.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.4 — Robust error handling

**Objective:** Handle a specific exception.

```python
def parse_port(s: str) -> int:
    try:
        return int(s)
    except ValueError:
        print(f"warning: bad port {s!r}, defaulting to 443")
        return 443
print(parse_port("nope"))   # 443
```

**Expected result:** a graceful default on bad input — predictable failure handling.

**Negative test:** wrap the body in bare `except:`; it **hides** real errors (e.g.,
KeyboardInterrupt) — catch the specific exception.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Automation is data shaping: dicts to index, sets to dedupe, comprehensions to transform,
typed functions for clear interfaces, and specific exception handling for unattended
robustness. This chapter applied each on ops-shaped data.

- [ ] I can index records with dicts.
- [ ] I can filter/transform with comprehensions.
- [ ] I can write typed functions.
- [ ] I can handle specific exceptions gracefully.
- [ ] I completed Labs 2.1–2.4 including each negative test.
