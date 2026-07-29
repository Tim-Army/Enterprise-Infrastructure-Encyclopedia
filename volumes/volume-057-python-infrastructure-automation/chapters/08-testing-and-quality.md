# Chapter 08: Testing and Quality

## Learning Objectives

- Write tests with `pytest`.
- Use fixtures for setup/teardown.
- Mock external calls to test in isolation.
- Enforce quality with linting and type checking.
- Complete a walkthrough for each quality skill.

## Theory and Architecture

Automation that changes infrastructure must be **tested** — a bug can break production.
**`pytest`** is the standard: plain `assert`-based tests, **fixtures** for reusable
setup/teardown, and **parametrization** for table-driven cases. External dependencies
(APIs, subprocesses) are **mocked** (`unittest.mock`) so tests are fast and deterministic.
Quality gates add a **linter/formatter** (**`ruff`**) and a **type checker** (**`mypy`**)
run in CI, plus **coverage** to see what's exercised.

## Design Considerations

Test the **logic** (parsing, decisions, transforms) and **mock** the I/O (don't call real
APIs in unit tests). Use **fixtures** for shared setup and **parametrize** for many
cases. Run **ruff** + **mypy** in CI so style and type errors fail the build.

## Implementation and Automation

The labs write a pytest test, a fixture, a mock, and describe lint/type gates.

## Validation and Troubleshooting

Confirm the tools:

```text
pytest: def test_x(): assert ... ; fixtures via @pytest.fixture; @pytest.mark.parametrize.
Mock: unittest.mock.patch("module.requests.get", ...). Gates: ruff check; mypy .
Coverage: pytest --cov.
```

Common pitfalls: tests that call **real APIs** (slow/flaky); and no CI gates (style/type
regressions slip in).

## Security and Best Practices

**Mock** external I/O in unit tests, use **fixtures**/parametrization for clarity, and run
**ruff + mypy + coverage** in CI. Test the failure paths (bad input, API errors), not just
the happy path.

## Hands-On Lab

Testing walkthroughs. **Shared prerequisites** — Python 3.12+ (`pip install pytest`).
**Cost:** none.

### Lab 8.1 — A pytest test

**Objective:** Write and run a simple test.

```python
# test_ports.py
def parse_port(s): return int(s) if s.isdigit() else 443
def test_parse_port_default():
    assert parse_port("nope") == 443
    assert parse_port("8080") == 8080
```

```bash
pytest -q test_ports.py
```

**Expected result:** **passing** tests (`2 passed`) — verified logic.

**Negative test:** ship the parser with no test; a regression **breaks silently** — test
it.

**Cleanup:** `rm test_ports.py`.

### Lab 8.2 — A fixture

**Objective:** Share setup with a fixture.

```python
import pytest
@pytest.fixture
def hosts():
    return [{"name":"web1"},{"name":"web2"}]
def test_count(hosts):
    assert len(hosts) == 2
```

**Expected result:** the test uses the **fixture** data and passes — reusable setup.

**Negative test:** duplicate setup in every test; a **fixture** centralizes it — DRY.

**Cleanup:** none.

### Lab 8.3 — Mock an external call

**Objective:** Test without hitting a real API.

```python
from unittest.mock import patch
def get_status(client): return client.get("/health").status_code
def test_status():
    with patch("builtins.__import__"):  # illustrative; normally patch the client
        class Fake: 
            def get(self,_): 
                class R: status_code=200
                return R()
        assert get_status(Fake()) == 200
```

**Expected result:** the test passes using a **fake client** — isolated, deterministic.

**Negative test:** call the real API in a unit test; it's **slow and flaky** — mock the
boundary.

**Cleanup:** none.

### Lab 8.4 — Lint and type gates

**Objective:** Run quality gates.

```bash
pip install ruff mypy
ruff check .        # style/lint
mypy --strict mytool  # types (if annotated)
```

**Expected result:** **ruff** and **mypy** reporting clean (or actionable findings) —
enforced quality.

**Negative test:** rely on review alone for style/types; **ruff + mypy** catch them
mechanically in CI — gate on them.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Quality means pytest tests (with fixtures and parametrization), mocked external I/O for
isolation, and ruff + mypy + coverage gates in CI. This chapter wrote a test, a fixture,
a mock, and ran the gates.

- [ ] I can write and run pytest tests.
- [ ] I can share setup with fixtures.
- [ ] I can mock external calls.
- [ ] I can run ruff and mypy as quality gates.
- [ ] I completed Labs 8.1–8.4 including each negative test.
