# Chapter 09: CI/CD, Source of Truth, and Keeping Current

## Learning Objectives

- Build a network CI/CD pipeline around the tools in this volume.
- Drive automation from a source of truth.
- Apply GitOps to network configuration.
- Track the ecosystem and keep skills current.
- Complete a walkthrough for each operational skill.

## Theory and Architecture

Mature network automation is **GitOps**: intended state lives in Git (data in a **source
of truth** like NetBox, templates and playbooks in the repo), and a **CI/CD pipeline**
renders, validates, and deploys changes on merge. A typical pipeline: **lint/parse-check**
templates → **render** config (Jinja2) → **dry-run/diff** against devices (NAPALM) →
**deploy** on approval → **post-validate** (pyATS/pytest). The **source of truth** (NetBox,
Volume LII) feeds the inventory and variables so devices reconcile to intended state. The
ecosystem moves quickly — track library releases and Python versions.

## Design Considerations

Keep **intent in Git**, render/validate in **CI**, require **diff review** before deploy,
and **post-validate** every change. Source inventory and variables from **NetBox** so
there is one authoritative model. Gate merges on tests.

## Implementation and Automation

The labs sketch a pipeline, a source-of-truth-driven render, and a currency check.

## Validation and Troubleshooting

Confirm the model:

```text
GitOps: intent in Git + source of truth (NetBox) -> CI: lint -> render -> diff -> deploy -> validate.
Inventory/vars from NetBox. Gate merges on tests + diff review.
```

Common pitfalls: deploying from laptops (no review/audit); and drift between the source of
truth and devices.

## Security and Best Practices

Store **intent in Git**, drive from a **source of truth**, deploy only through **reviewed
CI**, require **diff approval**, **post-validate**, and keep secrets in a vault. Detect and
remediate **drift** on a schedule.

## Hands-On Lab

Pipeline walkthroughs. **Shared prerequisites** — Python 3.12+; `git`; the tools from
earlier chapters. **Cost:** none.

### Lab 9.1 — Sketch the pipeline stages

**Objective:** Define the CI stages.

```python
stages = ["lint/parse-check templates", "render config (jinja2)",
          "diff vs device (napalm compare_config)", "deploy on approval",
          "post-validate (pytest/genie)"]
for i,s in enumerate(stages,1): print(f"{i}. {s}")
```

**Expected result:** the ordered **pipeline stages** — a reviewable deploy flow.

**Negative test:** deploy straight from a laptop; a **CI pipeline** adds review, audit, and
validation — use it.

**Cleanup:** none.

### Lab 9.2 — Render from a source of truth

**Objective:** Drive rendering from NetBox-style data.

```python
from jinja2 import Template
sot = {"device":"r1","interfaces":[{"name":"Gi1","ip":"10.0.0.1"}]}  # from NetBox API
cfg = Template("hostname {{ device }}\n{% for i in interfaces %}interface {{ i.name }}\n ip address {{ i.ip }} 255.255.255.0\n{% endfor %}").render(**sot)
print(cfg)
```

**Expected result:** config rendered from **source-of-truth** data — intent → config in
CI.

**Negative test:** keep variables in the pipeline scripts; source them from the **source
of truth** so there's one model.

**Cleanup:** none.

### Lab 9.3 — Gate on validation

**Objective:** Fail the pipeline on a bad diff.

```python
def gate(diff: str) -> int:
    dangerous = "no router bgp" in diff
    return 1 if dangerous else 0
print("exit:", gate("+interface Lo1\n-no router bgp"))   # 1 -> blocked
```

**Expected result:** a **non-zero** exit blocking a dangerous change — an automated gate.

**Negative test:** auto-approve every diff; **gate** on dangerous patterns and require
review.

**Cleanup:** none.

### Lab 9.4 — Track the ecosystem

**Objective:** Check a library's current release.

```bash
pip index versions netmiko 2>/dev/null | head -1 || pip show netmiko | grep -i version
```

**Expected result:** the installed/available **netmiko** version — what to track for
updates.

**Negative test:** pin libraries once and never update; **track releases** and update
deliberately (they add platform support/fixes).

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Mature network automation is GitOps: intent in Git and a source of truth (NetBox), a CI
pipeline that lints, renders, diffs, deploys on approval, and post-validates, with merges
gated on tests. This chapter sketched the pipeline, rendered from a source of truth,
gated on validation, and tracked the ecosystem.

- [ ] I can describe the network CI/CD stages.
- [ ] I can render config from a source of truth.
- [ ] I can gate deploys on validation.
- [ ] I can track library/Python currency.
- [ ] I completed Labs 9.1–9.4 including each negative test.
