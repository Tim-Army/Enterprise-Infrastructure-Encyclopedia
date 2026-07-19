# Chapter 03: Configuration Management and Desired-State Convergence

![Lab flow for this chapter: the motd role deploys a managed file via the template module; the first playbook run reports changed=1 and the second reports changed=0 across all tasks, the idempotency contract holding. As a negative test, a raw shell task appending a timestamp is added to the same role; its second run also reports changed=1 again — idempotency broken, because a raw shell/command task has no built-in concept of desired state and needs an explicit creates, removes, or when guard before it belongs in a convergence-oriented playbook.](../../../diagrams/volume-09-infrastructure-automation/chapter-03-ansible-idempotency-broken-flow.svg)

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

### Objective

Write and converge an idempotent role against a local container, prove
idempotency with a second run, and demonstrate a non-idempotent task
failing the same check.

### Prerequisites

- Python 3.12, `pip install "ansible-core==2.17.*" ansible-lint`.
- Docker or Podman available locally for a target container (or substitute
  `localhost` with `connection: local` if container runtime access is
  unavailable — steps below use a local connection for portability).

### Steps

1. Create the lab layout:

   ```bash
   mkdir -p ansible-lab/roles/motd/tasks ansible-lab/roles/motd/templates
   cd ansible-lab
   ```

2. Create an inventory targeting the local machine:

   ```bash
   cat > inventory.yml <<'EOF'
   all:
     hosts:
       localhost:
         ansible_connection: local
   EOF
   ```

3. Create an idempotent role that manages `/tmp/ansible-lab-motd`:

   ```bash
   cat > roles/motd/templates/motd.j2 <<'EOF'
   Welcome to {{ inventory_hostname }} — managed by Ansible.
   EOF

   cat > roles/motd/tasks/main.yml <<'EOF'
   ---
   - name: Deploy managed motd file
     ansible.builtin.template:
       src: motd.j2
       dest: /tmp/ansible-lab-motd
       mode: "0644"
   EOF
   ```

4. Create the playbook:

   ```bash
   cat > site.yml <<'EOF'
   ---
   - name: Converge motd
     hosts: all
     gather_facts: true
     roles:
       - motd
   EOF
   ```

5. Lint, then run twice to prove idempotency:

   ```bash
   ansible-lint .
   ansible-playbook -i inventory.yml site.yml   # expect changed=1
   ansible-playbook -i inventory.yml site.yml   # expect changed=0
   ```

### Expected Results

- The first run reports `changed=1` for the `template` task.
- The second run reports `changed=0` across all tasks — the idempotency
  contract holding.

### Negative Test

Add a non-idempotent task and confirm it breaks the contract:

```bash
cat >> roles/motd/tasks/main.yml <<'EOF'

- name: Append a timestamp (deliberately non-idempotent)
  ansible.builtin.shell: echo "Last run: $(date)" >> /tmp/ansible-lab-motd
EOF
ansible-playbook -i inventory.yml site.yml   # expect changed=1
ansible-playbook -i inventory.yml site.yml   # expect changed=1 again -- idempotency broken
```

Confirm the second run still reports `changed=1` for the shell task,
demonstrating why raw `shell`/`command` tasks need explicit `creates`,
`removes`, or `when` guards before they belong in a convergence-oriented
playbook.

### Cleanup

```bash
rm -f /tmp/ansible-lab-motd
cd .. && rm -rf ansible-lab
```

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
