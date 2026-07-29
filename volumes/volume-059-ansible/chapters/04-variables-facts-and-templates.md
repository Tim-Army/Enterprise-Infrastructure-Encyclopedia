# Chapter 04: Variables, Facts, and Templates

## Learning Objectives

- Define and reference variables and understand precedence.
- Gather and use facts.
- Capture task output with `register`.
- Generate files with the template module.
- Complete a walkthrough for each data skill.

## Theory and Architecture

Ansible data comes from **variables** (defined in vars, group_vars/host_vars, extra-vars,
etc., with a defined **precedence** where more specific wins), **facts** (system data
Ansible **gathers** from hosts, e.g., `ansible_facts['distribution']`), and **registered
results** (`register` captures a task's output for use in later tasks). Files are generated
with the **`template`** module, which renders a **Jinja2** template using all available
variables/facts — the same intent-to-config pattern as elsewhere, applied by Ansible.

## Design Considerations

Keep variables in **group_vars/host_vars** and pass overrides via **extra-vars** for
one-offs. Use **facts** to make plays adapt to each host (OS, IP). **Register** results to
branch on them. Use **`template`** (not `copy` with inline content) for generated config.

## Implementation and Automation

The labs set variables, gather facts, register output, and render a template.

## Validation and Troubleshooting

Confirm the model:

```text
Vars precedence (low->high): role defaults < group_vars < host_vars < play vars < extra-vars.
Facts: ansible_facts[...] from setup. register: capture result. template: Jinja2 -> file.
```

Common pitfalls: relying on precedence you don't understand (wrong value wins); and
inlining config that should be a **template**.

## Security and Best Practices

Organize vars in **group_vars/host_vars**, reserve **extra-vars** for overrides, use
**facts** for host-adaptive plays, and generate config with **templates** under version
control. Keep secret vars in Vault.

## Hands-On Lab

Data walkthroughs. **Shared prerequisites** — ansible-core; an inventory targeting
localhost. **Cost:** none.

### Lab 4.1 — Variables and precedence

**Objective:** Override a var with extra-vars.

```bash
cat > vars.yml <<'YAML'
- hosts: localhost
  connection: local
  vars: { greeting: "from play vars" }
  tasks:
    - ansible.builtin.debug: { msg: "{{ greeting }}" }
YAML
ansible-playbook vars.yml -e greeting="from extra-vars"
```

**Expected result:** the message shows **"from extra-vars"** — extra-vars wins precedence.

**Negative test:** expect the play var to win over `-e`; **extra-vars** has the highest
precedence — know the order.

**Cleanup:** `rm -f vars.yml`.

### Lab 4.2 — Use facts

**Objective:** Read a gathered fact.

```bash
ansible localhost -m ansible.builtin.setup -a "filter=ansible_python_version"
```

**Expected result:** the host's **Python version** fact — host data for adaptive plays.

**Negative test:** hard-code the OS/version in a play; **facts** let one play adapt per
host.

**Cleanup:** none.

### Lab 4.3 — Register task output

**Objective:** Capture and reuse a result.

```yaml
- hosts: localhost
  connection: local
  tasks:
    - ansible.builtin.command: date +%Y
      register: year
    - ansible.builtin.debug: { msg: "year is {{ year.stdout }}" }
```

**Expected result:** the message shows the current **year** from the registered result —
using output downstream.

**Negative test:** re-run the command to get the value again; **register** captures it once
for reuse.

**Cleanup:** none.

### Lab 4.4 — Render a template

**Objective:** Generate a file from Jinja2.

```bash
echo "host {{ inventory_hostname }} python {{ ansible_python_version | default('?') }}" > motd.j2
cat > tmpl.yml <<'YAML'
- hosts: localhost
  connection: local
  tasks:
    - ansible.builtin.template: { src: motd.j2, dest: /tmp/ansible_motd.txt }
YAML
ansible-playbook tmpl.yml && cat /tmp/ansible_motd.txt
```

**Expected result:** a rendered file with host/version substituted — the template module.

**Negative test:** build the file with `copy` + inline string interpolation; **template**
renders Jinja2 with all vars/facts — use it for generated files.

**Cleanup:** `rm -f motd.j2 tmpl.yml /tmp/ansible_motd.txt`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Ansible data is variables (with precedence), gathered facts, and registered results,
rendered into files with the Jinja2 template module. This chapter overrode a var, read a
fact, registered output, and rendered a template.

- [ ] I can define variables and reason about precedence.
- [ ] I can gather and use facts.
- [ ] I can register task output.
- [ ] I can render a template from Jinja2.
- [ ] I completed Labs 4.1–4.4 including each negative test.
