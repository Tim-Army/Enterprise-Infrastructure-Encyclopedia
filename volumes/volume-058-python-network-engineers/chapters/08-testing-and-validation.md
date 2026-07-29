# Chapter 08: Testing and Validation

## Learning Objectives

- Explain why network changes need pre/post validation.
- Validate operational state with parsed data.
- Use pyATS/Genie for structured testing.
- Snapshot and diff network state.
- Complete a walkthrough for each validation skill.

## Theory and Architecture

A network change is only safe if you can **prove** it did what you intended and broke
nothing. The pattern is **pre-change snapshot → change → post-change snapshot → compare**:
capture structured state (interfaces up, BGP neighbors established, routes present) before
and after, and assert it matches expectations. **pyATS/Genie** (Cisco's test framework)
provides device connections, structured **parsers**, and **`diff`** of Genie objects, plus
a testcase runner. Even without pyATS, you assert on parsed data (Chapter 03) with
`pytest`. Validation turns automation from "it ran" into "it's correct".

## Design Considerations

Define the **expected state** (BGP up, no new down interfaces) and **assert** it after
changes. Snapshot **before and after** and **diff** — a change that flaps a neighbor
should fail the run. Integrate validation into the deploy pipeline so bad changes are
caught automatically.

## Implementation and Automation

The labs validate parsed state, use Genie diff, and assert with pytest.

## Validation and Troubleshooting

Confirm the model:

```text
Pre snapshot -> change -> post snapshot -> compare.
Genie: device.parse(...) -> structured; genie diff of two snapshots.
Assertions: assert all(intf up); assert bgp neighbors == established.
```

Common pitfalls: deploying without a **post-check**; and comparing raw text instead of
**structured** state.

## Security and Best Practices

Always **pre/post snapshot** and **diff structured state**, define **explicit expected
conditions**, fail the pipeline on regressions, and keep validation in version control.
Test the validation logic itself.

## Hands-On Lab

Validation walkthroughs. **Shared prerequisites** — Python 3.12+ (`pip install pytest`;
`pyats[full]`/`genie` optional). Labs use embedded data where a device isn't available.
**Cost:** none.

### Lab 8.1 — Assert on parsed state

**Objective:** Verify all interfaces are up.

```python
interfaces = [{"intf":"Gi1","status":"up"},{"intf":"Gi2","status":"up"}]
down = [i["intf"] for i in interfaces if i["status"] != "up"]
assert not down, f"down interfaces: {down}"
print("all interfaces up")
```

**Expected result:** **`all interfaces up`** — a passing state assertion.

**Negative test:** eyeball `show ip int brief`; **assert on parsed data** so validation is
automatic and repeatable.

**Cleanup:** none.

### Lab 8.2 — Compare pre/post snapshots

**Objective:** Detect a regression between snapshots.

```python
pre  = {"bgp": {"10.0.0.2": "Established"}}
post = {"bgp": {"10.0.0.2": "Idle"}}
regressions = {n:s for n,s in post["bgp"].items() if s != pre["bgp"].get(n)}
assert not regressions, f"BGP regressions: {regressions}"
```

**Expected result:** an **AssertionError** flagging the BGP regression — the diff caught a
break.

**Negative test:** deploy with no post-check; a **flapped neighbor** slips by — always
compare pre/post.

**Cleanup:** none.

### Lab 8.3 — Genie parse and diff (pattern)

**Objective:** Describe structured testing with Genie.

```python
# from genie.testbed import load
# dev = testbed.devices["r1"]; dev.connect()
# pre = dev.parse("show ip route"); # ... change ...; post = dev.parse("show ip route")
# print(pre.diff(post))   # structured route diff
print("Genie: device.parse -> structured; pre.diff(post) -> structured change report")
```

**Expected result:** the Genie **parse + diff** pattern — deep structured validation.

**Negative test:** diff raw `show` text; **Genie's structured diff** ignores cosmetic
noise and highlights real changes.

**Cleanup:** none.

### Lab 8.4 — Wrap validation in pytest

**Objective:** Make validation a test suite.

```python
# test_state.py
def bgp_ok(state): return all(s == "Established" for s in state.values())
def test_bgp():
    assert bgp_ok({"10.0.0.2":"Established"})
```

```bash
pytest -q test_state.py
```

**Expected result:** a **passing** validation test — repeatable, CI-ready checks.

**Negative test:** validate by hand each deploy; **pytest** runs it consistently in CI —
automate it.

**Cleanup:** `rm test_state.py`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Validation proves changes are correct: assert on structured state, snapshot pre/post and
diff, use pyATS/Genie for deep structured testing, and wrap it in pytest for CI. This
chapter asserted state, compared snapshots, and built a validation test.

- [ ] I can assert on parsed operational state.
- [ ] I can compare pre/post snapshots for regressions.
- [ ] I can describe Genie parse-and-diff validation.
- [ ] I can wrap validation in pytest for CI.
- [ ] I completed Labs 8.1–8.4 including each negative test.
