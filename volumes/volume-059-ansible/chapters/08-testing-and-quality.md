# Chapter 08: Testing and Quality

## Learning Objectives

- Lint playbooks and roles with ansible-lint.
- Validate syntax before running.
- Assert conditions within plays.
- Test roles with Molecule.
- Complete a walkthrough for each quality skill.

## Theory and Architecture

Automation that changes infrastructure needs **quality gates**. **`ansible-lint`** checks
playbooks/roles against best-practice rules (idempotence risks, deprecated syntax, FQCN
usage). **`ansible-playbook --syntax-check`** catches YAML/structure errors before a run,
and **`--check --diff`** previews changes. The **`assert`** module fails a play when a
condition isn't met (guarding prerequisites/results). **Molecule** is the role-testing
framework: it spins up a container/VM, converges the role, and runs **idempotence** and
verification tests — the standard for CI-testing roles.

## Design Considerations

Run **`ansible-lint`** and **`--syntax-check`** in CI, gate playbook logic with **`assert`**,
and test roles with **Molecule** (including the **idempotence** check — a second converge
must report no changes). Keep tests in version control and run on every change.

## Implementation and Automation

The labs lint, syntax-check, assert, and describe Molecule.

## Validation and Troubleshooting

Confirm the tools:

```text
ansible-lint <playbook/role>. ansible-playbook --syntax-check. --check --diff (preview).
assert: fail play if condition false. Molecule: create -> converge -> idempotence -> verify.
```

Common pitfalls: skipping the **idempotence** test (a role that changes every run is
broken); and no lint in CI.

## Security and Best Practices

Gate CI on **ansible-lint + syntax-check**, guard prerequisites/results with **`assert`**,
and test roles with **Molecule** including the **idempotence** assertion. Fail the pipeline
on lint/test errors.

## Hands-On Lab

Quality walkthroughs. **Shared prerequisites** — ansible-core (`pip install ansible-lint`;
`molecule` optional). **Cost:** none.

### Lab 8.1 — Syntax-check a playbook

**Objective:** Catch structural errors before running.

```bash
cat > play.yml <<'YAML'
- hosts: localhost
  connection: local
  tasks:
    - ansible.builtin.debug: { msg: "ok" }
YAML
ansible-playbook --syntax-check play.yml
```

**Expected result:** **`playbook: play.yml`** with no errors — valid structure.

**Negative test:** run a playbook with a YAML typo directly; **`--syntax-check`** catches it
first — check before running.

**Cleanup:** `rm -f play.yml`.

### Lab 8.2 — Lint with ansible-lint

**Objective:** Check best practices.

```bash
ansible-lint play.yml 2>/dev/null || echo "(create play.yml first)"
```

**Expected result:** ansible-lint reporting clean (or actionable findings, e.g., FQCN,
naming) — enforced best practices.

**Negative test:** rely on review for style/idempotence risks; **ansible-lint** catches
them mechanically — gate on it.

**Cleanup:** none.

### Lab 8.3 — Assert a condition

**Objective:** Fail the play if a prerequisite isn't met.

```yaml
- hosts: localhost
  connection: local
  tasks:
    - ansible.builtin.assert:
        that:
          - ansible_python_version is version('3.0','>=')
        fail_msg: "Python 3 required"
```

**Expected result:** the assertion **passes** (Python 3) — a guarded prerequisite.

**Negative test:** proceed without checking prerequisites; an **`assert`** fails fast with a
clear message.

**Cleanup:** none.

### Lab 8.4 — Molecule idempotence (describe)

**Objective:** Describe role testing with Molecule.

```text
# molecule test: create (container) -> converge (run role) -> idempotence (converge again,
#   expect 0 changed) -> verify (assertions) -> destroy.
"idempotence gate: the second converge MUST report changed=0"
```

**Expected result:** the Molecule flow with the **idempotence** gate — CI-grade role
testing.

**Negative test:** ship a role that reports changes on every run; Molecule's **idempotence
test** fails it — fix the non-idempotent task.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Quality means ansible-lint and syntax-check in CI, assert-guarded prerequisites, and
Molecule role testing with an idempotence gate. This chapter syntax-checked, linted,
asserted, and described Molecule.

- [ ] I can syntax-check a playbook.
- [ ] I can lint with ansible-lint.
- [ ] I can guard with the assert module.
- [ ] I can describe Molecule's idempotence test.
- [ ] I completed Labs 8.1–8.4 including each negative test.
