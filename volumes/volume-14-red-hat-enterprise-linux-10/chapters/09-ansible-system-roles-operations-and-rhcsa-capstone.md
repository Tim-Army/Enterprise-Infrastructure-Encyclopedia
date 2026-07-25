# Chapter 09: Ansible, System Roles, Operations, and RHCSA Capstone

![Lab flow for this chapter: a single Ansible playbook builds a scoped service account, an LVM-backed XFS filesystem, an SELinux file context, an httpd virtual host, an open firewall port, and a nightly timer in one run; a second run reports zero changes for every task except the always-changed context-restore command. Independent verification checks every domain directly, exactly as an RHCSA practical would require. As a negative test, the SELinux context is manually reverted; the web service now fails at the SELinux layer with a corresponding denial in the audit log, and re-running the playbook restores the correct context and working service — demonstrating both MAC enforcement and idempotent remediation together.](../../../diagrams/volume-14-red-hat-enterprise-linux-10/chapter-09-rhcsa-capstone-selinux-remediation-flow.svg)

*Figure 9-1. Flow used throughout this chapter's Hands-On Lab: an integrated Ansible capstone build across identity, storage, SELinux, firewall, and scheduled work, tested against a manual SELinux regression.*

## Learning Objectives

- Explain Ansible's agentless, inventory-driven architecture and its
  idempotent execution model.
- Write and run playbooks and roles that configure RHEL 10 hosts
  reproducibly, including variables, templates, and handlers.
- Apply RHEL System Roles to standardize common administrative tasks
  across a fleet.
- Describe how Ansible Automation Platform extends ad hoc playbook
  execution into a governed, auditable operations practice.
- Integrate the identity, storage, SELinux, firewall, and service
  topics from Chapters 03–08 into a single automated build.
- Complete an RHCSA-aligned capstone lab exercising multiple
  certification objective domains in one continuous exercise.

## Theory and Architecture

Every prior chapter in this volume covered a domain — boot and
services, identity and networking, storage, SELinux and cryptography,
common server services, containers — through manual commands run
directly on a host. This chapter closes the volume by doing two
things: introducing Ansible as the mechanism that turns those manual
commands into reproducible, version-controlled automation, and then
using that automation (plus manual verification) to build and validate
a single host touching nearly every domain covered so far, in the
spirit of the RHCSA (EX200) performance-based exam format.

### Ansible's agentless architecture

Ansible manages remote hosts over standard SSH (or, for local
execution, a direct connection), pushing small Python modules to the
target, executing them, and removing them — no persistent agent
process runs on managed hosts. This is a deliberate architectural
choice: a managed host's only prerequisite is SSH access and a Python
interpreter, both already present on a standard RHEL 10 install, so
there is no additional daemon, port, or attack surface to maintain
fleet-wide purely for automation reachability.

The **control node** is the machine (an administrator's workstation, a
CI runner, or an Ansible Automation Platform execution environment)
that runs `ansible` or `ansible-playbook`; **managed nodes** are the
targets, described in an **inventory** — a static INI or YAML file, or
a dynamic inventory script/plugin querying a cloud provider or CMDB
for current host membership.

### Idempotency as the organizing principle

Every Ansible **module** is designed to be idempotent: running a task
against a host already in the desired state reports `ok` (no change),
while running it against a host not yet in that state reports
`changed` and performs the necessary action — the same principle
[Chapter 02](02-essential-tools-shell-scripting-and-software-management.md) introduced for shell scripts, now enforced structurally by
the module system rather than left to script discipline. This is why
Ansible playbooks are safe to re-run repeatedly (including on a
schedule, via `cron` or a systemd timer from [Chapter 03](03-boot-systemd-processes-logging-and-scheduled-work.md)) without
manually tracking which hosts already received a given change.

### Playbooks, roles, and templates

A **playbook** is a YAML file listing **plays** — a set of **tasks**
targeted at a group of hosts from the inventory. A **role** packages
related tasks, variables, templates, handlers, and default values into
a reusable, self-contained unit with a standard directory structure
(`tasks/`, `handlers/`, `templates/`, `defaults/`, `vars/`), making it
straightforward to apply the same configuration logic across many
playbooks or many projects. **Jinja2 templates** (`.j2` files,
deployed with the `template` module) let a configuration file's
content vary per host or group based on inventory variables — the
mechanism behind generating a correct `httpd` virtual host, a
`chrony.conf`, or an `/etc/exports` entry per host role from one
shared template. **Handlers** are tasks that run only when notified by
another task that reported `changed` — the standard pattern for "only
restart this service if its configuration actually changed."

### RHEL System Roles

**RHEL System Roles** (the `rhel-system-roles` package) are a
collection of pre-built, Red Hat–supported Ansible roles covering
common RHEL administrative domains: `timesync` (chrony, [Chapter 07](07-dns-ntp-web-database-and-common-server-services.md)),
`network` (NetworkManager profiles, [Chapter 04](04-users-privilege-ssh-networking-and-firewalld.md)), `storage` (partitions,
LVM, and filesystems, [Chapter 05](05-storage-lvm-filesystems-swap-and-shared-storage-services.md)), `selinux` (booleans and file
contexts, [Chapter 06](06-selinux-permissions-cryptography-and-system-hardening.md)), `firewall` (zones and rules, [Chapter 04](04-users-privilege-ssh-networking-and-firewalld.md)), and
many others. Using a System Role instead of hand-writing equivalent
tasks gets an administrator a tested, Red Hat–maintained
implementation of the exact configuration patterns this volume covers
manually, callable with a small set of role variables rather than
dozens of individual tasks — the difference between "automating what I
already know how to do by hand" and "re-deriving a correct
implementation from scratch."

### From ad hoc automation to Ansible Automation Platform

Running `ansible-playbook` from a workstation is sufficient for
individual work and small environments, but enterprise operations
generally outgrow that model as the number of playbooks, credentials,
and stakeholders grows. **Ansible Automation Platform (AAP)** adds a
control plane on top of core Ansible: a credential store (so
playbooks reference a named credential rather than an embedded
secret), role-based access control over who can run what against
which inventory, a scheduling and job-history audit trail, and
execution environments (containerized, version-pinned Ansible
runtimes) that make "the playbook worked on my machine" failures far
less common. The relationship mirrors this encyclopedia's broader
automation architecture theme from [Volume I](../../volume-01-enterprise-engineering-foundations/README.md): local execution proves a
playbook works, and a governed platform is what makes that same
playbook a safe, auditable, repeatable operational practice at fleet
scale.

## Design Considerations

- **Role granularity.** Build roles around a coherent unit of
  configuration (a "webserver" role, a "hardened-baseline" role)
  rather than either one monolithic playbook per environment or one
  microscopic role per task; both extremes make reuse and review
  harder than a well-scoped middle ground.
- **System Roles vs. custom roles.** Default to a RHEL System Role
  when one exists for the domain being automated — it is
  Red Hat–tested against the exact platform this volume targets;
  write a custom role only for logic genuinely specific to an
  organization's environment, and consider layering a thin custom role
  on top of a System Role rather than duplicating its logic.
- **Variable precedence and secrets.** Plan where a given setting
  lives deliberately — role defaults for safe fallbacks, group/host
  variables for environment-specific values, and Ansible Vault (or an
  AAP-managed credential) for anything secret — rather than
  discovering Ansible's variable precedence order under pressure
  during an incident.
- **Idempotency as a design constraint, not an afterthought.** Prefer
  Ansible modules (which enforce idempotency structurally) over raw
  `shell`/`command` tasks wherever an equivalent module exists; a
  `shell` task re-running a non-idempotent command on every playbook
  run silently breaks the "safe to re-run" guarantee the rest of the
  playbook relies on.
- **Local playbook execution vs. AAP adoption timing.** Local
  `ansible-playbook` execution is entirely appropriate for a single
  administrator or a small, low-change-velocity environment; the
  point at which multiple people need shared, audited, credential-
  scoped execution is the point at which AAP's operational overhead
  becomes worth it, not before.
- **Capstone-style validation.** Treat any nontrivial automated build
  the way this chapter's capstone lab treats a fresh host: validate
  every domain independently after the automation runs (identity,
  storage, SELinux, firewall, service reachability) rather than
  trusting a green `ansible-playbook` exit code alone as proof the
  system is correctly configured end to end.

## Implementation and Automation

### 1. Inventory and ad hoc commands

```bash
dnf install -y ansible-core

mkdir -p ~/lab-ansible && cd ~/lab-ansible
cat > inventory.ini <<'EOF'
[web]
web01.lab.example.com

[db]
db01.lab.example.com

[rhel_hosts:children]
web
db
EOF

# Ad hoc: confirm connectivity and gather facts, no playbook required
ansible -i inventory.ini rhel_hosts -m ping
ansible -i inventory.ini rhel_hosts -m setup -a "filter=ansible_distribution*"
```

### 2. A basic playbook with variables, templates, and handlers

```bash
mkdir -p roles/webserver/{tasks,handlers,templates,defaults}

cat > roles/webserver/defaults/main.yml <<'EOF'
webserver_port: 80
webserver_docroot: /var/www/html
EOF

cat > roles/webserver/templates/vhost.conf.j2 <<'EOF'
<VirtualHost *:{{ webserver_port }}>
    ServerName {{ inventory_hostname }}
    DocumentRoot {{ webserver_docroot }}
</VirtualHost>
EOF

cat > roles/webserver/tasks/main.yml <<'EOF'
---
- name: Install httpd
  ansible.builtin.dnf:
    name: httpd
    state: present

- name: Deploy virtual host configuration
  ansible.builtin.template:
    src: vhost.conf.j2
    dest: /etc/httpd/conf.d/vhost.conf
    mode: "0644"
  notify: Restart httpd

- name: Ensure httpd is enabled and running
  ansible.builtin.service:
    name: httpd
    state: started
    enabled: true

- name: Open the firewall for HTTP
  ansible.posix.firewalld:
    service: http
    permanent: true
    immediate: true
    state: enabled
EOF

cat > roles/webserver/handlers/main.yml <<'EOF'
---
- name: Restart httpd
  ansible.builtin.service:
    name: httpd
    state: restarted
EOF

cat > site.yml <<'EOF'
---
- name: Configure web servers
  hosts: web
  become: true
  roles:
    - webserver
EOF

ansible-playbook -i inventory.ini site.yml --check   # dry run first
ansible-playbook -i inventory.ini site.yml
```

### 3. Using RHEL System Roles

```bash
dnf install -y rhel-system-roles

cat > timesync.yml <<'EOF'
---
- name: Standardize time synchronization
  hosts: rhel_hosts
  become: true
  vars:
    timesync_ntp_servers:
      - hostname: time.example.com
        iburst: true
  roles:
    - rhel-system-roles.timesync
EOF

ansible-playbook -i inventory.ini timesync.yml

cat > storage.yml <<'EOF'
---
- name: Provision an application data volume
  hosts: db
  become: true
  vars:
    storage_volumes:
      - name: vg_data-lv_appdata
        type: lvm
        pool: vg_data
        disks: [sdb]
        size: 20g
        fs_type: xfs
        mount_point: /appdata
  roles:
    - rhel-system-roles.storage
EOF

ansible-playbook -i inventory.ini storage.yml

cat > selinux.yml <<'EOF'
---
- name: Apply SELinux booleans and file contexts
  hosts: web
  become: true
  vars:
    selinux_booleans:
      - { name: httpd_can_network_connect, state: true, persistent: true }
    selinux_fcontexts:
      - { target: '/data/web(/.*)?', setype: httpd_sys_content_t }
  roles:
    - rhel-system-roles.selinux
EOF

ansible-playbook -i inventory.ini selinux.yml
```

### 4. Vault for secrets

```bash
ansible-vault create group_vars/db/vault.yml
# Enter and confirm a vault password when prompted, then add:
# db_admin_password: "ChangeMe!23"

ansible-playbook -i inventory.ini site.yml --ask-vault-pass
```

## Validation and Troubleshooting

- **Confirm idempotency directly.** Run a playbook twice in
  succession; the second run should report `changed=0` for every task
  if the playbook and modules are correctly written. A task that
  reports `changed` on every run (most often a raw `shell`/`command`
  task without a proper idempotency check) should be rewritten using a
  dedicated module or a `creates=`/`changed_when=` guard.
- **Diagnose a task failure.** `ansible-playbook -vvv` shows the exact
  module arguments and remote command output; `--check` (dry run) plus
  `--diff` shows what a task would change without applying it, useful
  for reviewing a playbook against production before running it live.
- **Diagnose connectivity/authentication failures before blaming the
  playbook.** `ansible -m ping <host>` isolates whether the problem is
  SSH/authentication ([Chapter 04](04-users-privilege-ssh-networking-and-firewalld.md)) versus something in the playbook
  itself; a playbook failing on its very first task against a specific
  host is very often an inventory or credential problem, not a task
  logic problem.
- **Diagnose a System Role producing unexpected results.** Read the
  role's own README and default variables
  (`/usr/share/ansible/roles/rhel-system-roles.<name>/`) rather than
  guessing at variable names; System Roles are versioned with the
  `rhel-system-roles` package, so confirm the installed version
  matches the documentation being referenced.
- **Validate the end state independently of the automation tool.**
  After any playbook run, verify with the same manual commands used
  throughout this volume (`systemctl status`, `firewall-cmd
  --list-all`, `getsebool`, `lsblk`) rather than trusting the
  playbook's own "changed"/"ok" summary as sufficient proof —
  automation can succeed at applying a wrong configuration just as
  easily as a right one.
- **Common failure: variable precedence surprises.** A value set in
  `roles/<role>/defaults/main.yml` is the lowest-precedence source and
  is silently overridden by inventory, group_vars, host_vars, or
  extra-vars; when a role does not seem to pick up an expected value,
  check for a competing definition in a higher-precedence location
  before assuming the role itself is broken.

## Security and Best Practices

- Store secrets in Ansible Vault or an AAP-managed credential, never
  in plain text in a playbook or inventory file committed to version
  control.
- Use `become: true` with a scoped, audited privilege-escalation
  account rather than direct root SSH, consistent with the `sudo`
  guidance in [Chapter 04](04-users-privilege-ssh-networking-and-firewalld.md).
- Pin `rhel-system-roles` and `ansible-core` versions deliberately
  against [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) rather
  than floating on "whatever is currently in the repository," so a
  playbook's behavior does not silently change on a future host
  rebuild.
- Run `--check --diff` against production-representative infrastructure
  before any first live run of a new or significantly changed
  playbook.
- Adopt Ansible Automation Platform's role-based access control and
  credential separation once more than a small number of people run
  playbooks against production, rather than continuing to share a
  workstation-based `ansible.cfg` and local SSH keys indefinitely.
- Keep playbooks and roles in version control with the same review
  discipline as application code — a playbook is infrastructure code,
  and an unreviewed change to one can affect an entire fleet in a
  single run.
- Log and retain job history (native to AAP, or via CI pipeline logs
  for ad hoc `ansible-playbook` runs) so any fleet-wide change has an
  audit trail independent of any individual administrator's local
  shell history.

## References and Knowledge Checks

**References**

- [`ansible-playbook(1)`, `ansible-doc(1)` man pages and command help.](https://docs.ansible.com/projects/ansible/latest/cli/ansible-playbook.html)
- [Ansible documentation](https://docs.ansible.com/) — Playbooks, Roles, and Templating
  (docs.ansible.com).
- [RHEL System Roles documentation, Red Hat Customer Portal.](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html-single/automating_system_administration_by_using_rhel_system_roles/index)
- [Red Hat Ansible Automation Platform documentation](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/) — execution
  environments, credentials, and role-based access control.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — Ansible
  baseline referenced in this chapter.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  RHCSA (EX200) blueprint mapping for this volume.

**Knowledge checks**

1. Why does Ansible not require a persistent agent process on managed
   nodes, and what does a managed node need instead?
2. What is the practical difference between a role's `defaults/`
   variables and `vars/` in Ansible's precedence order, and why does
   that difference matter for reusability?
3. Why would an organization prefer a RHEL System Role over an
   equivalent hand-written role for a task like time synchronization
   or firewall configuration?
4. What operational capability does Ansible Automation Platform add on
   top of local `ansible-playbook` execution that becomes important as
   a team, not just a fleet, grows?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **Ansible automation (the RHCE EX294
core) and an integrative RHCSA capstone**. Ansible is the Red Hat Certified Engineer path
built on RHCSA; the capstone chains RHCSA objectives into one timed build the way EX200 does.
Every step is a runnable RHEL 10 command. Each ends **`**Lab verified by:** *pending*`**
until a human runs it.

**Shared prerequisites for Labs 9.1–9.4** — a control node with `ansible-core` installed, one
or more managed RHEL 10 hosts reachable by SSH key with a `sudo`-capable user, and (for the
capstone) a spare disk. **Cost:** none.

### Lab 9.1 — Inventory and ad-hoc commands (Topic: Ansible basics)

**Objective:** Define an inventory and run ad-hoc modules.

```bash
sudo dnf install -y ansible-core
cat > inventory.ini <<'EOF'
[web]
node1.example.com
node2.example.com
EOF
ansible -i inventory.ini web -m ping
ansible -i inventory.ini web -m dnf -a "name=tree state=present" --become
```

**Expected result:** `ping` returns `SUCCESS` (`pong`) for each host, and the `dnf` module
installs `tree` with privilege escalation (`--become`) — Ansible is agentless over SSH; the
inventory names hosts/groups and ad-hoc `-m module -a args` runs one task without a playbook.

**Negative test:** run a privileged task without `--become` (or `become: true`); it fails with
permission denied — privilege escalation must be requested explicitly.

**Cleanup:** `ansible -i inventory.ini web -m dnf -a "name=tree state=absent" --become`.

### Lab 9.2 — A playbook with tasks, handlers, and variables (Topic: Playbooks)

**Objective:** Write and run an idempotent playbook.

```bash
cat > web.yml <<'EOF'
---
- name: Configure web servers
  hosts: web
  become: true
  vars:
    page_content: "Deployed by Ansible"
  tasks:
    - name: Install httpd
      ansible.builtin.dnf:
        name: httpd
        state: present
    - name: Deploy index page
      ansible.builtin.copy:
        content: "{{ page_content }}\n"
        dest: /var/www/html/index.html
      notify: Restart httpd
    - name: Start and enable httpd
      ansible.builtin.service:
        name: httpd
        state: started
        enabled: true
  handlers:
    - name: Restart httpd
      ansible.builtin.service:
        name: httpd
        state: restarted
EOF
ansible-playbook -i inventory.ini web.yml
ansible-playbook -i inventory.ini web.yml    # second run: all "ok", nothing "changed"
```

**Expected result:** the first run reports `changed` for the installs/copies and fires the
handler; the **second run reports zero changes** — idempotence is the point of Ansible, and
handlers run only when a task reports a change (the restart fires on content change, not every
run).

**Negative test:** use `command`/`shell` to `echo` content into the file instead of the
`copy` module; it reports `changed` every run and is not idempotent — prefer modules over raw
commands so state, not actions, drives the result.

**Cleanup:** an uninstall playbook, or `ansible -i inventory.ini web -m dnf -a "name=httpd
state=absent" --become`.

### Lab 9.3 — RHEL System Roles (Topic: System roles)

**Objective:** Apply a supported role for a standard subsystem.

```bash
sudo dnf install -y rhel-system-roles
cat > timesync.yml <<'EOF'
---
- name: Configure time synchronization
  hosts: web
  become: true
  vars:
    timesync_ntp_servers:
      - hostname: 0.rhel.pool.ntp.org
        iburst: true
  roles:
    - redhat.rhel_system_roles.timesync
EOF
ansible-playbook -i inventory.ini timesync.yml
ansible -i inventory.ini web -m command -a "chronyc sources" --become
```

**Expected result:** the `timesync` role configures chrony on every host consistently, and
`chronyc sources` confirms it — RHEL System Roles are Red-Hat-supported Ansible roles that
apply best-practice configuration to subsystems (time, firewall, storage, networking, SELinux)
without writing the tasks by hand.

**Negative test:** hand-write chrony config across many hosts with slightly different playbooks;
they drift — a supported System Role gives one consistent, maintained implementation.

**Cleanup:** none (time sync is a good state to leave).

### Lab 9.4 — RHCSA capstone: an integrative timed build (Topic: Synthesis)

**Objective:** Chain multiple RHCSA objectives into one build, as EX200 does — then verify
the end state, not the commands.

```bash
# On a fresh RHEL 10 host, perform in one sitting (target: brisk, exam-like pace):
# 1. Users/security: create user 'ops', add to wheel, set 60-day password aging
sudo useradd ops && sudo usermod -aG wheel ops && sudo chage -M 60 ops
# 2. Storage: PV/VG/LV 'applv' on a spare disk, XFS, persistent mount at /app
sudo pvcreate /dev/vdb1 && sudo vgcreate appvg /dev/vdb1 && sudo lvcreate -L 1G -n applv appvg
sudo mkfs.xfs /dev/appvg/applv && sudo mkdir -p /app
echo "/dev/appvg/applv /app xfs defaults 0 0" | sudo tee -a /etc/fstab && sudo mount -a
# 3. Service + firewall + SELinux: serve /app content over httpd on port 8080
sudo semanage fcontext -a -t httpd_sys_content_t "/app(/.*)?" && sudo restorecon -Rv /app
sudo semanage port -a -t http_port_t -p tcp 8080
sudo firewall-cmd --permanent --add-port=8080/tcp && sudo firewall-cmd --reload
# 4. Verify the END STATE:
mount | grep /app ; sudo chage -l ops | grep Maximum ; sudo firewall-cmd --list-ports
```

**Expected result:** a single host that ends in the required state across users, storage,
services, firewall, and SELinux — the capstone mirrors EX200: you are scored on whether the
system ends correct and complete, done at a brisk pace, not on any individual command.

**Negative test:** configure each piece but skip `mount -a` / a reboot check; a bad `fstab`
entry that "worked" interactively renders the system unbootable — the exam (and this capstone)
rewards verifying the persistent end state, because that is what is graded.

**Cleanup:** reverse the build — remove the port/context, unmount and remove the LV/VG/PV,
delete the `fstab` line and the `ops` user — or rebuild the throwaway VM.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Ansible's agentless, idempotent execution model — playbooks, roles,
templates, and handlers — turns the manual, single-host procedures
built throughout this volume into reproducible, version-controlled
automation, and RHEL System Roles provide Red Hat–tested
implementations of the most common of those procedures. The capstone
lab in this chapter deliberately re-exercises identity, storage,
SELinux, firewalld, a web service, and scheduled work together on one
host, mirroring both the integrated nature of real production builds
and the performance-based, multi-domain format of the RHCSA (EX200)
exam this volume aligns to.

- [ ] Can explain Ansible's agentless architecture and idempotent
      execution model.
- [ ] Can write a playbook using variables, templates, and handlers.
- [ ] Can apply at least one RHEL System Role to a managed host.
- [ ] Can explain what Ansible Automation Platform adds over local
      `ansible-playbook` execution.
- [ ] Can independently verify identity, storage, SELinux, firewall,
      and service state after an automated build, without relying
      solely on the automation tool's own success report.
- [ ] Completed the capstone hands-on lab, including the negative test
      and cleanup.
