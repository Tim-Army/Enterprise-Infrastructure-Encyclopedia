# Chapter 05: The Ansible Track — RHCE (EX294)

## Learning Objectives

- Map the Ansible track: RHCSA → EX294 (RHCE, Engineer) → Specialists → RHCA.
- Cover the EX294 objectives: playbooks, variables, templates, roles, and system roles.
- Drill each as a performance task with real Ansible runs.

## The track

In the 2026 structure, **RHCE is the Ansible track's Engineer credential**: *Red Hat Certified Engineer — Advanced System Administrator in Ansible*, exam **EX294**, prerequisite RHCSA. It is performance-based: you write and run Ansible against managed nodes.

| Level | Credential | Exam |
|:---|:---|:---|
| L2 | RHCSA | EX200 |
| L3 (Engineer) | **RHCE** (Advanced System Admin in Ansible) | **EX294** |
| L4 | Ansible-track Specialists | various |
| L5 | RHCA in Ansible | EX294 + three same-track Specialists |

## Hands-On Lab

One control node with `ansible-core` and at least one managed node (a second VM or `localhost`). Free everywhere. **Cost:** none.

### Lab 5.1 — Inventory and ad-hoc (foundations)

**Objective (task):** "Build a static inventory with a group and run an ad-hoc command against it."

```bash
sudo dnf install -y ansible-core >/dev/null 2>&1 || pip install --quiet ansible-core
mkdir -p ~/ex294 && cd ~/ex294
cat > inventory <<'EOF'
[web]
localhost ansible_connection=local
EOF
ansible web -i inventory -m ping
ansible web -i inventory -m command -a "uptime"
```

**Expected result:** `localhost | SUCCESS => ... "ping": "pong"` and the uptime output — inventories (static/dynamic, groups, host vars) and ad-hoc modules are EX294's foundation. `ansible_connection=local` lets the whole exam run on one box for practice.

**Negative test:** Target a group that isn't in the inventory — `ansible: no hosts matched`; group names must match, a precision the exam expects.

**Rollback:** Keep `~/ex294`.

### Lab 5.2 — Playbooks with variables and handlers

**Objective (task):** "Write a playbook that installs and starts a service, using a variable and a handler."

```bash
cat > web.yml <<'EOF'
- name: Configure web
  hosts: web
  become: true
  vars:
    pkg: httpd
  tasks:
    - name: Install package
      ansible.builtin.dnf: { name: "{{ pkg }}", state: present }
      notify: Start web
  handlers:
    - name: Start web
      ansible.builtin.service: { name: "{{ pkg }}", state: started, enabled: true }
EOF
ansible-playbook -i inventory web.yml --syntax-check && echo "syntax OK"
```

**Expected result:** `syntax OK` (run it with a real managed node to install) — plays, tasks, `become`, variables (`{{ }}`), and **handlers notified by tasks** are EX294 core. Idempotence means a second run reports `changed=0`.

**Negative test:** Reference `{{ pkg }}` without defining it — `undefined variable`; the exam tests variable scoping and precedence.

**Rollback:** Keep for the next lab.

### Lab 5.3 — Templates with Jinja2

**Objective (task):** "Deploy a config file from a Jinja2 template using host facts."

```bash
cat > motd.j2 <<'EOF'
Welcome to {{ ansible_facts['hostname'] }}
Managed by Ansible — {{ ansible_facts['distribution'] }} {{ ansible_facts['distribution_version'] }}
EOF
cat > motd.yml <<'EOF'
- hosts: web
  become: true
  tasks:
    - name: Deploy motd
      ansible.builtin.template: { src: motd.j2, dest: /etc/motd }
EOF
ansible-playbook -i inventory motd.yml --syntax-check && echo "template play OK"
ansible web -i inventory -m setup -a "filter=ansible_distribution*" | head -8
```

**Expected result:** `template play OK` and gathered facts (`ansible_distribution`, version) — Jinja2 templates driven by **facts** (`ansible_facts`) and the `setup` module are heavily tested; the template module is the exam's most common file-deployment task.

**Negative test:** Use `{{ ansible_hostname }}` when fact-gathering is disabled (`gather_facts: false`) — undefined; templates depend on facts being gathered.

**Rollback:** Keep for the next lab.

### Lab 5.4 — Roles and Ansible Galaxy structure

**Objective (task):** "Create a role skeleton and use it from a playbook."

```bash
ansible-galaxy init roles/webrole 2>/dev/null && ls roles/webrole
cat > roles/webrole/tasks/main.yml <<'EOF'
- name: Ensure package
  ansible.builtin.dnf: { name: httpd, state: present }
EOF
cat > site.yml <<'EOF'
- hosts: web
  become: true
  roles:
    - webrole
EOF
ansible-playbook -i inventory site.yml --syntax-check && echo "role play OK"
```

**Expected result:** The standard role skeleton (`tasks/ handlers/ templates/ defaults/ vars/ meta/`) and a playbook consuming it — roles (structure, defaults vs vars precedence, dependencies) are a major EX294 objective; `ansible-galaxy init` produces the exam-expected layout.

**Negative test:** Put a value in both `defaults/main.yml` and `vars/main.yml` — `vars` wins; role variable precedence is a guaranteed exam question.

**Rollback:** Keep for the next lab.

### Lab 5.5 — RHEL System Roles

**Objective (task):** "Use a Red Hat System Role to configure a subsystem (e.g. timesync or firewall)."

```bash
sudo dnf install -y rhel-system-roles >/dev/null 2>&1 || ansible-galaxy collection install redhat.rhel_system_roles 2>/dev/null
ls /usr/share/ansible/roles/ 2>/dev/null | grep -i system | head -5 || echo "system roles ship as a collection"
cat > timesync.yml <<'EOF'
- hosts: web
  become: true
  roles:
    - rhel-system-roles.timesync
  vars:
    timesync_ntp_servers:
      - hostname: 0.pool.ntp.org
EOF
ansible-playbook -i inventory timesync.yml --syntax-check && echo "system-role play OK"
```

**Expected result:** The system-role playbook validating — **RHEL System Roles** (pre-built, supported roles for timesync, firewall, selinux, storage, network, etc.) are an explicit EX294 objective: you configure subsystems by setting the role's variables, not by writing tasks.

**Negative test:** Reinvent timesync with hand-written `lineinfile` tasks on chrony.conf — works but isn't what the exam wants; System Roles are the sanctioned, idempotent, portable approach.

**Rollback:** `rm -rf ~/ex294`.

## Summary and Completion Checklist

- [ ] Inventory, ad-hoc, playbooks, variables, and handlers drilled.
- [ ] Jinja2 templates with facts, and roles with precedence, done.
- [ ] RHEL System Roles used for a subsystem — the EX294 differentiator.
