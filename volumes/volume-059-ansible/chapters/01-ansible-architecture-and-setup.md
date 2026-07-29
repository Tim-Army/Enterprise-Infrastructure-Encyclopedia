# Chapter 01: Ansible Architecture and Setup

## Learning Objectives

- Explain Ansible's agentless, push-based architecture.
- Identify the core components: control node, inventory, modules, playbooks.
- Explain idempotence and why it matters.
- Install Ansible and run an ad-hoc command.
- Verify the version.

## Theory and Architecture

**Ansible** is an open-source (Red Hat) **automation engine** for configuration
management, application deployment, and orchestration. It is **agentless** and
**push-based**: a **control node** connects to managed hosts over **SSH** (or WinRM/APIs)
and executes **modules** — no persistent agent runs on the targets. Automation is
expressed as **playbooks** (YAML) that run **tasks** (each invoking a module) against an
**inventory** of hosts. The engine is **`ansible-core`** (current series **2.21.x**), and
content ships as **collections** (via Ansible Galaxy).

The defining property is **idempotence**: a well-written task describes desired **state**,
so running it repeatedly converges to that state and reports **changed** only when it
actually changes something. This makes runs safe to repeat.

## Design Considerations

Ansible's **agentless** model means low overhead and easy adoption — targets just need SSH
and Python. Write tasks for **desired state** (idempotent modules), not imperative
commands, so re-runs are safe. Keep the **control node** as the single push point with
version-controlled content.

## Implementation and Automation

Install Ansible and run an ad-hoc command:

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install ansible-core
ansible localhost -m ping
```

## Validation and Troubleshooting

Confirm the fundamentals:

```text
Agentless push over SSH; control node -> inventory hosts -> modules.
Playbooks (YAML) run tasks; content = collections (Galaxy). Engine: ansible-core 2.21.x.
Idempotence: desired-state tasks report 'changed' only when they change something.
```

Common pitfalls: using the `command`/`shell` module where an **idempotent** module exists
(always reports changed); and targets missing Python.

## Security and Best Practices

Prefer **idempotent state modules** over `shell`, keep content in **version control**,
secure the control node and SSH keys, and use **check mode** to preview. Store secrets in
Vault (Chapter 07).

## References and Knowledge Checks

- docs.ansible.com: getting started, playbooks, modules, and collections.

**Knowledge checks**

1. What makes Ansible "agentless"?
2. What is idempotence, and why does it matter?
3. What does a collection provide?

## Hands-On Lab

Setup walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — Python 3.12+; SSH to
localhost (or a target). **Cost:** none.

### Lab 1.1 — Install and ping

**Objective:** Install Ansible and reach a host.

```bash
pip install ansible-core
ansible localhost -m ping
```

**Expected result:** a **`"ping": "pong"`** SUCCESS — a working control node reaching a
target.

**Negative test:** target a host with no Python; the module **fails** — Ansible needs
Python on targets (or use raw/network modules).

**Cleanup:** none.

### Lab 1.2 — Run an ad-hoc command

**Objective:** Use a module ad hoc.

```bash
ansible localhost -m ansible.builtin.setup -a "filter=ansible_distribution*"
```

**Expected result:** gathered **facts** (distribution info) — ad-hoc module execution.

**Negative test:** run `shell: uname` to gather facts; the **setup** module returns
structured facts — prefer purpose-built modules.

**Cleanup:** none.

### Lab 1.3 — Verify the version

**Objective:** Confirm the ansible-core version.

```bash
ansible --version | head -1
```

**Expected result:** an **ansible-core 2.21.x** version line — the running engine.

**Negative test:** assume features exist regardless of version; **check `--version`** —
modules/collections track the core version.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Ansible is an agentless, push-based automation engine: a control node runs modules over
SSH against an inventory, expressed as idempotent YAML playbooks, with content in
collections. This chapter installed Ansible, pinged a host, and gathered facts.

- [ ] I can explain the agentless, push-based model.
- [ ] I can name the core components.
- [ ] I can explain idempotence.
- [ ] I can install Ansible and run ad-hoc modules.
- [ ] I completed Labs 1.1–1.3 including each negative test.
