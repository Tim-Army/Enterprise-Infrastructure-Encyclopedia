# Chapter 03: Configuration Management and Desired-State Convergence

![Lab flow for this chapter: the motd role deploys a managed file via the template module; the first playbook run reports changed=1 and the second reports changed=0 across all tasks, the idempotency contract holding. As a negative test, a raw shell task appending a timestamp is added to the same role; its second run also reports changed=1 again — idempotency broken, because a raw shell/command task has no built-in concept of desired state and needs an explicit creates, removes, or when guard before it belongs in a convergence-oriented playbook.](../../../diagrams/volume-009-infrastructure-automation/chapter-03-ansible-idempotency-broken-flow.svg)

*Figure 3-1. Flow used throughout this chapter's Hands-On Lab: Ansible idempotency proven with a template task, then deliberately broken with a raw shell append.*

## Learning Objectives

- Explain idempotency and desired-state convergence, and why they matter
  more than raw execution speed for configuration management.
- Structure Ansible content using roles and collections with clear
  variable precedence.
- Build static and dynamic inventories, including group and host variable
  layering.
- Write idempotent playbooks using `ansible-core` 2.17 modules, handlers,
  and Jinja2 templating.
- Test roles with `ansible-lint` and Molecule, and package execution
  environments for consistent runs.
- Diagnose non-idempotent tasks and common inventory/variable precedence
  bugs.

## Theory and Architecture

Configuration management tools converge a host toward a declared desired
state, in contrast to a script that performs a fixed sequence of actions
regardless of the host's starting condition. This chapter uses Ansible
core 2.17, the baseline recorded in
[SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md), as the volume's
configuration management engine, and frames the concepts so they transfer
to Chef, Puppet, or Salt where an enterprise already standardizes on one of
those instead.

### Idempotency

A task is idempotent if running it once and running it a hundred times
produce the same end state, and only the first run (or a run that
encounters actual drift) reports a change. Ansible modules are written to
this contract: `ansible.builtin.package` checks whether a package is
already installed before invoking the package manager; `ansible.builtin.file`
checks the current owner, group, mode, and type before changing anything.
A raw shell command (`ansible.builtin.command`, `ansible.builtin.shell`) is
**not** idempotent by default — it runs every time — so playbooks that use
it must add explicit guards (`creates`, `removes`, or a `when` condition
based on a prior registered fact) to restore idempotency.

Idempotency is what makes convergence safe to run repeatedly and on a
schedule: a playbook run against a host that already matches desired state
should report zero changes, which is itself a useful health signal (see
Validation and Troubleshooting).

### Agentless push architecture

Ansible is agentless: the control node connects to managed hosts over SSH
(or WinRM for Windows) and pushes a Python (or PowerShell) payload that
executes modules locally on the target, then tears itself down. There is no
persistent daemon on managed hosts and no separate certificate-based
enrollment process to maintain, which is the main operational trade-off
against pull-based agent architectures (Puppet, Chef): lower footprint and
faster onboarding, at the cost of requiring inbound SSH/WinRM reachability
and credentials from the control node (or Ansible Automation Platform
execution node) to every managed host at run time.

### Inventory

Inventory describes the set of managed hosts and the groups they belong to.
Static inventory is a YAML or INI file; dynamic inventory queries an
external source (cloud provider API, CMDB) at run time through an inventory
plugin:

```yaml
# playbooks/inventory/dev.yml
all:
  children:
    webservers:
      hosts:
        web01.dev.acme.internal:
        web02.dev.acme.internal:
      vars:
        http_port: 8080
    databases:
      hosts:
        db01.dev.acme.internal:
          pg_role: primary
        db02.dev.acme.internal:
          pg_role: replica
  vars:
    ansible_user: svc_ansible
    environment_name: dev
```

A dynamic AWS EC2 inventory plugin replaces the static host list with
live discovery, keyed by tags:

```yaml
# playbooks/inventory/aws_ec2.yml
plugin: amazon.aws.aws_ec2
regions:
  - us-east-1
filters:
  tag:ManagedBy: ansible
keyed_groups:
  - key: tags.Role
    prefix: role
compose:
  ansible_host: private_ip_address
```

### Variable precedence

Ansible resolves the same variable name from many possible sources — role
defaults, inventory group vars, inventory host vars, play vars, `-e`
extra vars, and facts — using a well-defined precedence order (from lowest
to highest: role `defaults/`, inventory group vars, inventory host vars,
play vars, role `vars/`, block/task vars, and finally `-e` extra vars,
which always wins). Bugs where "the variable I set didn't take effect"
are almost always a precedence misunderstanding, not a bug in Ansible
itself — put genuinely overridable defaults in `defaults/main.yml` and
reserve `vars/main.yml` for values a role's own logic depends on and
callers should not casually override.

### Roles and collections

A **role** is the reusable unit of configuration content: a directory
structure of tasks, handlers, templates, files, defaults, and vars with a
conventional layout that Ansible auto-discovers. A **collection** is the
distribution and versioning unit — a packaged bundle of roles, modules,
plugins, and documentation published to Ansible Galaxy or a private
Automation Hub, referenced by a `requirements.yml`:

```yaml
# playbooks/requirements.yml
collections:
  - name: community.general
    version: "9.2.0"
  - name: amazon.aws
    version: "8.1.0"
```

```bash
ansible-galaxy collection install -r requirements.yml
```

## Design Considerations

### Role granularity

Design roles around a single responsibility that maps to how the role will
be reused and tested independently — `nginx`, `postgresql_server`,
`node_exporter` — rather than one role per application stack. A role that
installs and configures three unrelated services cannot be reused
piecemeal and cannot be Molecule-tested in isolation with a meaningful
scope.

### Push cadence: ad hoc versus continuous convergence

Decide deliberately whether configuration is applied only on change
(triggered by a pipeline merge) or continuously reconciled on a schedule
(a periodic `cron`-triggered run, or Ansible Automation Platform's
scheduled job templates). Continuous reconciliation catches configuration
drift caused by out-of-band changes but adds load and requires idempotent,
side-effect-free playbooks throughout — a playbook with a
non-idempotent task that is safe to run once during a deploy can cause
real damage if it silently reruns every fifteen minutes.

### Execution environments

Ansible Automation Platform and `ansible-navigator` package the control
node's Python interpreter, `ansible-core`, collections, and their
dependencies into a container image called an **execution environment**,
built with `ansible-builder`. This solves the classic "collection X needs a
newer `ansible-core` than collection Y" dependency conflict by isolating
each pipeline or team's execution environment, and it makes the exact
runtime reproducible in CI, matching the version-pinning principle from
[Chapter 01](01-automation-operating-models-and-engineering-foundations.md).

### Choosing when Ansible is (and is not) the right tool

Ansible excels at host- and application-level configuration, orchestrated
multi-tier rollouts, and ad hoc operational tasks. It is a poor fit for
resources with a well-defined, provider-managed lifecycle that Terraform
already models cleanly (cloud infrastructure provisioning) — using Ansible
to loop-and-poll-create cloud resources reimplements, without state
tracking, what Terraform already does correctly. A common, effective
pattern is Terraform for provisioning and Ansible for configuring what
Terraform provisioned, handed off through a Terraform output consumed as
Ansible inventory (see [Chapter 04](04-api-event-and-integration-automation.md) for the integration mechanics).

## Implementation and Automation

### Role layout

```text
playbooks/roles/nginx/
├── defaults/
│   └── main.yml
├── vars/
│   └── main.yml
├── tasks/
│   └── main.yml
├── handlers/
│   └── main.yml
├── templates/
│   └── nginx.conf.j2
├── files/
│   └── acme-ca.crt
└── meta/
    └── main.yml
```

```yaml
# playbooks/roles/nginx/defaults/main.yml
nginx_worker_processes: auto
nginx_listen_port: 8080
nginx_server_name: "{{ inventory_hostname }}"
```

```yaml
# playbooks/roles/nginx/tasks/main.yml
---
- name: Install nginx
  ansible.builtin.package:
    name: nginx
    state: present

- name: Deploy nginx configuration
  ansible.builtin.template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    owner: root
    group: root
    mode: "0644"
    validate: "nginx -t -c %s"
  notify: Reload nginx

- name: Ensure nginx is enabled and running
  ansible.builtin.service:
    name: nginx
    state: started
    enabled: true
```

```yaml
# playbooks/roles/nginx/handlers/main.yml
---
- name: Reload nginx
  ansible.builtin.service:
    name: nginx
    state: reloaded
```

```jinja
{# playbooks/roles/nginx/templates/nginx.conf.j2 #}
worker_processes {{ nginx_worker_processes }};

events {
  worker_connections 1024;
}

http {
  server {
    listen {{ nginx_listen_port }};
    server_name {{ nginx_server_name }};
  }
}
```

The `validate` argument on the `template` task runs `nginx -t` against the
rendered file *before* it replaces the live configuration, so a syntax
error fails the task cleanly instead of leaving nginx running on a broken
config after a reload. The handler only fires when `template` reports a
change, keeping repeat runs from unnecessarily reloading a service that is
already correctly configured — idempotency applied at the orchestration
level, not just the module level.

### Playbook composition

```yaml
# playbooks/site.yml
---
- name: Configure web tier
  hosts: webservers
  become: true
  roles:
    - role: nginx
      nginx_listen_port: 8080

- name: Configure database tier
  hosts: databases
  become: true
  serial: 1
  roles:
    - role: postgresql_server
```

`serial: 1` rolls the play through the `databases` group one host at a
time, so a bad configuration is caught on the first host before it reaches
the rest of the tier — the Ansible equivalent of a canary rollout.

### Linting and testing

```bash
ansible-lint playbooks/
```

Molecule drives role tests inside disposable containers, verifying both
that a role converges cleanly and that a second run reports no changes
(the idempotency test):

```yaml
# playbooks/roles/nginx/molecule/default/molecule.yml
driver:
  name: docker
platforms:
  - name: instance
    image: docker.io/rockylinux/rockylinux:9
    pre_build_image: true
provisioner:
  name: ansible
verifier:
  name: ansible
```

```bash
cd playbooks/roles/nginx
molecule test
```

`molecule test` runs create, converge, idempotence, verify, and destroy in
sequence; the built-in idempotence stage runs `converge` a second time and
fails the pipeline if any task reports `changed` on that second pass —
turning the idempotency principle from a design goal into an automated
gate.

### CI integration

```yaml
# .github/workflows/ansible-ci.yml
name: ansible-ci

on:
  pull_request:
    paths:
      - "playbooks/**"

jobs:
  lint-and-molecule:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install "ansible-core==2.17.*" ansible-lint molecule molecule-plugins[docker]
      - run: ansible-galaxy collection install -r playbooks/requirements.yml
      - run: ansible-lint playbooks/
      - name: Molecule test (nginx role)
        working-directory: playbooks/roles/nginx
        run: molecule test
```

## Validation and Troubleshooting

- **Second run reports changes that should be idempotent.** Almost always
  a `command`/`shell` task without a `creates`/`removes` guard, or a
  `template`/`lineinfile` task whose rendered output is non-deterministic
  (unsorted dictionary iteration, embedded timestamps). Run with `-v` and
  compare the module's diff output (`--diff`) between the first and second
  run to isolate the offending task.
- **"The variable I set isn't taking effect."** Print effective variable
  resolution with `ansible-inventory --host <hostname> --vars` or
  `ansible -m debug -a "var=my_variable" <hostname>`, and check the
  precedence order in Theory and Architecture — an inventory host var
  cannot override a role's `vars/main.yml`, and extra vars (`-e`) override
  everything, which surprises engineers who expect defaults to win.
- **`UNREACHABLE` errors at scale.** Check SSH connectivity, known_hosts
  entries, and `ansible_python_interpreter` on managed hosts with an
  unusual or minimal Python install; use `ansible -m ping <group>` to
  isolate connectivity from playbook logic before debugging further.
- **Molecule idempotence stage fails in CI but passes locally.** Usually a
  timing- or fact-dependent value (a generated password, a current
  timestamp used as a tag) baked into a template. Make such values
  deterministic (derived from a fixed seed or fetched once and stored) or
  explicitly excluded from the idempotency check.
- **Dynamic inventory returns zero hosts.** Confirm the inventory plugin's
  credentials and filters independently of the playbook:
  `ansible-inventory -i playbooks/inventory/aws_ec2.yml --graph`.

## Security and Best Practices

- Run managed-host tasks with the minimum privilege required; use
  `become: true` scoped to the specific tasks that need root rather than
  an entire play, and prefer a dedicated `svc_ansible` service account
  with sudo rules limited to the commands automation actually needs.
- Never hardcode secrets in playbooks, templates, or inventory; use
  `ansible-vault` or an external secrets lookup plugin ([Chapter 06](06-automation-identity-secrets-and-privileged-execution.md)).
- Pin collection versions in `requirements.yml` and commit
  `ansible-galaxy`-generated lockfile-equivalents; treat unpinned
  collections as a supply-chain risk exactly like unpinned Terraform
  providers ([Chapter 08](08-automation-security-governance-and-supply-chains.md)).
- Use `--check --diff` (dry-run mode) in a pre-production pipeline stage
  before every apply against a production inventory, and treat a
  `--check` run that fails with module-support warnings as a signal that
  the play is not safe to trust blindly in check mode.
- Validate rendered configuration before it takes effect wherever the
  target service supports it (the `nginx -t` `validate` pattern above)
  rather than discovering a syntax error only after a reload breaks the
  service.
- Log and archive playbook run output (job IDs, changed/failed task
  counts, `--diff` output) for audit purposes; Ansible Automation
  Platform's job history and centralized logging ([Chapter 09](09-automation-observability-reliability-and-lifecycle-operations.md)) are the
  enterprise-scale mechanism for this.

## References and Knowledge Checks

### References

- Red Hat, *Ansible Documentation*, ansible-core 2.17 —
  <https://docs.ansible.com/ansible-core/2.17/>
- Red Hat, *Ansible Lint Documentation* —
  <https://ansible.readthedocs.io/projects/lint/>
- Ansible, *Molecule Documentation* —
  <https://ansible.readthedocs.io/projects/molecule/>
- Red Hat, *Ansible Builder Documentation* —
  <https://ansible.readthedocs.io/projects/builder/>

### Knowledge Checks

1. Why is a bare `ansible.builtin.shell` task not idempotent by default,
   and what two task arguments commonly restore idempotency?
2. Rank role `defaults/main.yml`, inventory host vars, and `-e` extra vars
   from lowest to highest precedence.
3. What does Molecule's idempotence stage actually test, and why is it a
   stronger check than "the playbook ran without errors"?
4. Why is Terraform generally preferred over Ansible for provisioning
   cloud infrastructure, and Ansible preferred for configuring what was
   provisioned?
5. What problem do execution environments solve that a shared control
   node's system Python installation does not?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each configuration-management skill** —
inventory/ad-hoc, idempotent playbooks, roles, and templating — the convergence half of the
Infrastructure-and-Automation domain. Labs use Ansible against `localhost`, so they need no
remote fleet. Each ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 3.1–3.4** — `ansible-core` installed and a scratch dir
`mkdir -p ~/ans && cd ~/ans`. **Cost:** none.

### Lab 3.1 — Inventory and ad-hoc commands (Topic: Inventory)

**Objective:** Define hosts and run a one-off module.

```bash
cd ~/ans
cat > inventory.ini <<'EOF'
[local]
localhost ansible_connection=local
EOF
ansible -i inventory.ini local -m ping
ansible -i inventory.ini local -m ansible.builtin.setup -a "filter=ansible_distribution*" | head
```

**Expected result:** `ping` returns `SUCCESS`/`pong` and `setup` gathers facts about the host —
the inventory names the hosts/groups Ansible manages, and ad-hoc `-m module` runs a single task
without a playbook, useful for quick checks and facts.

**Negative test:** target a host missing from the inventory; Ansible reports it does not match —
the inventory is the authoritative host list, and only listed hosts/groups can be targeted.

**Cleanup:** none.

### Lab 3.2 — Idempotent playbooks (Topic: Playbooks)

**Objective:** Converge a host to a declared state, twice.

```bash
cd ~/ans
cat > site.yml <<'EOF'
---
- name: Converge local state
  hosts: local
  tasks:
    - name: Ensure a marker file exists
      ansible.builtin.copy:
        content: "managed\n"
        dest: /tmp/ansible-marker
    - name: Ensure a directory exists
      ansible.builtin.file:
        path: /tmp/ansible-dir
        state: directory
EOF
ansible-playbook -i inventory.ini site.yml | grep -E "changed=|ok="
ansible-playbook -i inventory.ini site.yml | grep -E "changed=|ok="   # second run: changed=0
```

**Expected result:** the first run reports `changed`, the **second reports `changed=0`** —
Ansible modules are declarative and idempotent: they check current state and act only if a
change is needed, so re-running a playbook is safe and converges rather than repeats.

**Negative test:** use the `command`/`shell` module to `echo` into the file instead of `copy`;
it reports `changed` every run — raw commands are not idempotent, so prefer state-based modules.

**Cleanup:** `rm -rf /tmp/ansible-marker /tmp/ansible-dir`.

### Lab 3.3 — Roles and variables (Topic: Roles)

**Objective:** Structure reusable automation as a role.

```bash
cd ~/ans && ansible-galaxy init roles/marker -q 2>/dev/null || mkdir -p roles/marker/tasks roles/marker/defaults
cat > roles/marker/defaults/main.yml <<'EOF'
marker_text: "default marker"
EOF
cat > roles/marker/tasks/main.yml <<'EOF'
- name: Write the marker
  ansible.builtin.copy: { content: "{{ marker_text }}\n", dest: /tmp/role-marker }
EOF
cat > play.yml <<'EOF'
- hosts: local
  roles:
    - { role: marker, marker_text: "from playbook" }
EOF
ansible-playbook -i inventory.ini play.yml >/dev/null && cat /tmp/role-marker
```

**Expected result:** the role writes `from playbook` (the caller's variable overriding the
role default) — roles package tasks, defaults, templates, and handlers as a reusable unit with a
clear variable-precedence model, the standard way to organize non-trivial automation.

**Negative test:** put everything in one giant playbook with no roles; it becomes unmaintainable
and hard to share — roles are what make automation modular and reusable across projects.

**Cleanup:** `rm -rf ~/ans/roles ~/ans/play.yml /tmp/role-marker`.

### Lab 3.4 — Templates and handlers (Topic: Templating)

**Objective:** Render config from a template and trigger a handler on change.

```bash
cd ~/ans
cat > conf.yml <<'EOF'
---
- hosts: local
  vars: { port: 8080 }
  tasks:
    - name: Render config from a Jinja2 template
      ansible.builtin.copy:
        content: "listen {{ port }}\n"
        dest: /tmp/app.conf
      notify: reload app
  handlers:
    - name: reload app
      ansible.builtin.debug: { msg: "would reload after config change" }
EOF
ansible-playbook -i inventory.ini conf.yml | grep -E "reload app|changed="
```

**Expected result:** the config renders with the variable and the `reload app` handler fires
**only because the config changed** — templating (Jinja2) generates configuration from
variables/facts, and handlers run once at the end only when notified, so services reload on
change rather than every run.

**Negative test:** reload the service in a normal task on every run instead of via a
change-notified handler; you cause needless restarts — handlers exist to act only when something
actually changed.

**Cleanup:** `rm -f ~/ans/conf.yml /tmp/app.conf`.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Configuration management's value comes from idempotent, desired-state
convergence rather than one-shot scripting: modules check before they act,
roles package reusable configuration with a clear variable contract, and
Molecule's idempotence stage turns "runs cleanly twice" from a hope into an
automated gate. Ansible core 2.17 pairs naturally with Terraform from
[Chapter 02](02-infrastructure-as-code-state-providers-and-modules.md) — Terraform provisions, Ansible configures — and both feed the
pipeline and policy patterns covered in [Chapter 05](05-automation-pipelines-testing-and-policy-gates.md).

- [ ] Can explain idempotency and identify a non-idempotent task on sight.
- [ ] Can build and layer a static or dynamic inventory with group and
      host variables.
- [ ] Has written a role with defaults, tasks, handlers, and a validated
      template.
- [ ] Has run `ansible-lint` and a Molecule idempotence test against a
      role.
- [ ] Understands variable precedence well enough to debug an "override
      didn't take effect" report.
