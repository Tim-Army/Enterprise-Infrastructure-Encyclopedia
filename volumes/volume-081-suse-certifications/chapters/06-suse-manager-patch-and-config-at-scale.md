# Chapter 06: SUSE Manager — Patch and Config at Scale

## Learning Objectives

- Describe SUSE Manager and its architecture.
- Manage patches across a fleet with content lifecycle.
- Automate configuration with Salt.
- Organize systems and enforce state.
- Complete a walkthrough for each SUSE Manager topic.

## Theory and Architecture

**SUSE Manager** is SUSE's **infrastructure management** platform — one console to patch, configure,
and provision **fleets** of Linux systems (SLES and other distributions). It centralizes **software
channels** (repositories) and uses a **Content Lifecycle Management** workflow to promote a tested set
of patches through **environments** (dev → test → prod), so patches are validated before hitting
production. Configuration and automation run on **Salt** — SUSE Manager acts as a Salt master, so
administrators can apply **states** (declarative configuration) and run commands across thousands of
minions from one place. Systems are organized into **groups** for scoped actions and reporting. The
value is **consistency and control at scale**: instead of patching servers one by one, you manage the
whole estate — validated patches, enforced configuration, and audit. This chapter teaches each with a
hands-on walkthrough (content lifecycle reasoning, Salt state logic, and fleet organization).

## Design Considerations

Centralize **channels** and promote patches through **Content Lifecycle** environments (test before
prod). Automate configuration with **Salt states** (declarative, idempotent). Organize systems into
**groups** for scoped actions. Schedule patching. Report compliance. Never patch production without
**staging**.

## Implementation and Automation

The labs reason about content lifecycle, write a Salt state, and organize systems.

## Validation and Troubleshooting

Confirm the SUSE Manager model:

```text
SUSE Manager = fleet patch/config/provisioning. Software channels + Content Lifecycle Management (promote patches dev->test->prod). Automation: Salt (master + minions, declarative states). Systems in groups for scoped actions + reporting.
Value: validated patches + enforced config + audit at scale.
```

Common pitfalls: patching **prod directly** from vendor channels (no validation); and ad-hoc
configuration instead of **Salt states**.

## Security and Best Practices

Promote patches through **Content Lifecycle** environments, enforce configuration with **Salt states**,
organize into **groups**, and report compliance. Stage before production. All work is authorized fleet
administration.

## Hands-On Lab

SUSE Manager walkthroughs. **Shared prerequisites** — `python3` (SUSE Manager is a server product;
labs model its logic). **Cost:** none.

### Lab 6.1 — Reason about content lifecycle

**Objective:** Validate patches before prod.

```python
python3 - <<'PY'
lifecycle=["clone vendor channels into a 'test' environment (snapshot of patches)",
           "patch test systems + validate","promote the same snapshot to 'prod'","patch prod with validated set"]
for i,s in enumerate(lifecycle,1): print(f"{i}. {s}")
print("SUSE Manager: Content Lifecycle promotes a fixed, tested patch set dev->test->prod")
PY
```

**Expected result:** the **Content Lifecycle** promotion (test → prod) — validated fleet patching.

**Negative test:** point prod directly at live vendor channels; an untested patch could break it —
**stage** via content lifecycle.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.2 — Write a Salt state

**Objective:** Enforce configuration declaratively.

```yaml
# Salt state (applied by SUSE Manager to minions):
ssh_config:
  file.managed:
    - name: /etc/ssh/sshd_config.d/hardening.conf
    - contents: |
        PermitRootLogin no
        PasswordAuthentication no
sshd_service:
  service.running:
    - name: sshd
    - watch:
      - file: ssh_config
```

**Expected result:** a **Salt state** enforcing SSH hardening across the fleet — declarative,
idempotent configuration.

**Negative test:** SSH into each server to edit sshd_config by hand; it drifts and doesn't scale —
enforce a **Salt state**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.3 — Organize systems into groups

**Objective:** Scope actions.

```python
python3 - <<'PY'
groups={"web-servers":["web01","web02"],"db-servers":["db01"],"all-prod":["web01","web02","db01"]}
def patch(group): return f"apply validated patch set to {groups[group]}"
print(patch("web-servers"))
print(patch("all-prod"))
print("SUSE Manager: groups scope patching/config/reporting to the right systems")
PY
```

**Expected result:** actions **scoped to groups** — organized fleet management.

**Negative test:** run a patch action against **all systems** when only web servers need it; scope by
**group**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.4 — Report patch compliance

**Objective:** Prove the fleet is current.

```python
python3 - <<'PY'
fleet=[{"host":"web01","missing_patches":0},{"host":"web02","missing_patches":3},{"host":"db01","missing_patches":0}]
noncompliant=[s["host"] for s in fleet if s["missing_patches"]>0]
print("systems missing patches:", noncompliant)
print("SUSE Manager: compliance reporting shows which systems need patching (audit)")
PY
```

**Expected result:** the **non-compliant** systems flagged — fleet patch compliance.

**Negative test:** assume the fleet is patched without a **compliance report**; drift hides — report
it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

SUSE Manager manages Linux fleets at scale — Content Lifecycle Management to promote validated patches,
Salt states for declarative configuration, system groups for scoped actions, and compliance reporting —
consistency and control across the estate.

- [ ] I can reason about content lifecycle.
- [ ] I can write a Salt state.
- [ ] I can organize systems into groups.
- [ ] I can report patch compliance.
- [ ] I completed Labs 6.1–6.4 including each negative test.
