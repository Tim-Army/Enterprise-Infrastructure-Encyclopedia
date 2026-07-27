# Chapter 03: Playbooks and Tasks

## Learning Objectives

- Structure a playbook with plays and tasks.
- Demonstrate idempotence across repeated runs.
- Preview changes with check mode and diff.
- Trigger handlers on change.
- Complete a walkthrough for each playbook skill.

## Theory and Architecture

A **playbook** is a YAML file of one or more **plays**; each play targets a host group and
runs an ordered list of **tasks**, each invoking a **module** with parameters. Well-chosen
modules are **idempotent**: the first run reports **changed**, subsequent runs report
**ok** (nothing to do). **Check mode** (`--check`) previews what would change without
making changes, and **`--diff`** shows the content difference. **Handlers** are tasks that
run only when **notified** by a changed task (e.g., restart a service after its config
changes), and run once at the end of the play.

## Design Considerations

Name every task (readable output), use **state modules** for idempotence, gate risky runs
with **check mode**, and use **handlers** so services restart only when their config
actually changed. Keep plays focused on one host group and purpose.

## Implementation and Automation

The labs write and run a playbook, prove idempotence, use check/diff, and add a handler.

## Validation and Troubleshooting

Confirm the model:

```text
Playbook -> plays (hosts + tasks) -> modules. Idempotent: changed once, ok after.
--check (preview), --diff (show delta). Handlers: run on notify, once at play end.
```

Common pitfalls: `shell`/`command` (always changed, not idempotent); and handlers that
never fire because nothing notifies them.

## Security and Best Practices

Use **idempotent modules**, **name** tasks, preview with **`--check --diff`**, and drive
restarts through **handlers**. Avoid `shell` unless wrapped with `creates`/`changed_when`.

## Hands-On Lab

Playbook walkthroughs. **Shared prerequisites** — ansible-core; a writable temp dir; an
inventory targeting localhost (`ansible_connection=local`). **Cost:** none.

### Lab 3.1 — Write and run a playbook

**Objective:** Create a file with an idempotent module.

```yaml
# site.yml
- hosts: localhost
  connection: local
  tasks:
    - name: ensure a marker file exists
      ansible.builtin.copy:
        content: "managed by ansible\n"
        dest: /tmp/ansible_marker.txt
```

```bash
ansible-playbook site.yml
```

**Expected result:** the play runs with **changed=1** (file created) — a working playbook.

**Negative test:** use `shell: echo ... > file`; it reports **changed every run** — the
`copy` module is idempotent.

**Cleanup:** `rm -f /tmp/ansible_marker.txt`.

### Lab 3.2 — Prove idempotence

**Objective:** Re-run and see no change.

```bash
ansible-playbook site.yml
```

**Expected result:** the second run reports **changed=0, ok=1** — idempotence in action.

**Negative test:** expect changes on every run; a **desired-state** module converges and
then reports ok — that's correct.

**Cleanup:** none.

### Lab 3.3 — Check mode and diff

**Objective:** Preview a change without applying it.

```bash
# edit content in site.yml, then:
ansible-playbook site.yml --check --diff
```

**Expected result:** the **diff** of what would change, with **nothing applied** — a safe
preview.

**Negative test:** apply changes to production untested; **`--check --diff`** previews
first — use it.

**Cleanup:** none.

### Lab 3.4 — Handlers

**Objective:** Run a task only when notified.

```yaml
- hosts: localhost
  connection: local
  tasks:
    - name: write config
      ansible.builtin.copy: { content: "cfg v2\n", dest: /tmp/ansible_cfg.txt }
      notify: reload service
  handlers:
    - name: reload service
      ansible.builtin.debug: { msg: "service reloaded" }
```

**Expected result:** the handler runs **only when** the config task changed — change-driven
actions.

**Negative test:** restart the service every run unconditionally; a **handler** fires only
on change — avoid needless restarts.

**Cleanup:** `rm -f /tmp/ansible_cfg.txt`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Playbooks are YAML plays of idempotent tasks; re-runs converge (changed→ok), check/diff
preview changes, and handlers run only when notified. This chapter wrote a playbook,
proved idempotence, previewed with check mode, and used a handler.

- [ ] I can structure a playbook with plays and tasks.
- [ ] I can demonstrate idempotence.
- [ ] I can preview with --check --diff.
- [ ] I can trigger handlers on change.
- [ ] I completed Labs 3.1–3.4 including each negative test.
