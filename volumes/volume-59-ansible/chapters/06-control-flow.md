# Chapter 06: Control Flow

## Learning Objectives

- Run tasks conditionally with `when`.
- Repeat tasks with loops.
- Group tasks and handle errors with blocks.
- Organize runs with tags.
- Complete a walkthrough for each control-flow skill.

## Theory and Architecture

Real playbooks need **control flow**. **`when`** runs a task only if a condition holds
(often based on facts or registered results). **`loop`** repeats a task over a list. A
**`block`** groups tasks and enables structured error handling with **`rescue`** (run on
failure) and **`always`** (run regardless), like try/except/finally. **Tags** label tasks
so a run can include/skip subsets (`--tags`, `--skip-tags`). Together these turn linear
task lists into adaptable automation.

## Design Considerations

Use **`when`** for host-adaptive behavior, **`loop`** for repetition (never copy-paste
tasks), **`block`/`rescue`/`always`** for error handling and cleanup, and **tags** so
large playbooks can run targeted subsets. Keep conditions readable.

## Implementation and Automation

The labs use `when`, `loop`, `block/rescue`, and tags.

## Validation and Troubleshooting

Confirm the constructs:

```text
when: <condition>. loop: [items] (item). block/rescue/always: try/except/finally.
tags: [name] -> ansible-playbook --tags name / --skip-tags name.
```

Common pitfalls: copy-pasted tasks instead of a **loop**; and no **rescue** for failure
cleanup.

## Security and Best Practices

Make plays **adaptive with `when`**, iterate with **`loop`**, handle failure with
**`block/rescue/always`**, and label with **tags** for targeted runs. Keep destructive
tasks guarded by conditions.

## Hands-On Lab

Control-flow walkthroughs. **Shared prerequisites** — ansible-core; a localhost inventory.
**Cost:** none.

### Lab 6.1 — Conditional task

**Objective:** Run a task only when a condition holds.

```yaml
- hosts: localhost
  connection: local
  tasks:
    - ansible.builtin.debug: { msg: "python 3 host" }
      when: ansible_python_version is version('3.0', '>=')
```

**Expected result:** the task runs (Python 3 host) — conditional execution.

**Negative test:** run a task unconditionally on all hosts; a **`when`** limits it to where
it applies.

**Cleanup:** none.

### Lab 6.2 — Loop

**Objective:** Repeat a task over a list.

```yaml
- hosts: localhost
  connection: local
  tasks:
    - ansible.builtin.debug: { msg: "vlan {{ item }}" }
      loop: [10, 20, 30]
```

**Expected result:** three iterations (vlan 10/20/30) — a loop replacing copy-paste.

**Negative test:** write three near-identical tasks; a **loop** stays correct as the list
grows.

**Cleanup:** none.

### Lab 6.3 — Block with rescue

**Objective:** Handle a failure gracefully.

```yaml
- hosts: localhost
  connection: local
  tasks:
    - block:
        - ansible.builtin.command: /bin/false
      rescue:
        - ansible.builtin.debug: { msg: "recovered from failure" }
      always:
        - ansible.builtin.debug: { msg: "cleanup runs regardless" }
```

**Expected result:** the **rescue** and **always** blocks run after the failure —
try/except/finally control.

**Negative test:** let a failed task abort the play with no recovery; a **rescue** handles
it and continues.

**Cleanup:** none.

### Lab 6.4 — Tags

**Objective:** Run a subset of tasks by tag.

```yaml
- hosts: localhost
  connection: local
  tasks:
    - ansible.builtin.debug: { msg: "config task" }
      tags: [config]
    - ansible.builtin.debug: { msg: "deploy task" }
      tags: [deploy]
```

```bash
ansible-playbook flow.yml --tags config
```

**Expected result:** only the **config**-tagged task runs — targeted execution.

**Negative test:** run the whole playbook when you only need one part; **tags** run just
the relevant subset.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Control flow makes playbooks adaptive: `when` for conditions, `loop` for repetition,
`block/rescue/always` for error handling, and tags for targeted runs. This chapter used
each construct.

- [ ] I can run tasks conditionally with `when`.
- [ ] I can repeat tasks with loops.
- [ ] I can handle failures with block/rescue/always.
- [ ] I can target subsets with tags.
- [ ] I completed Labs 6.1–6.4 including each negative test.
