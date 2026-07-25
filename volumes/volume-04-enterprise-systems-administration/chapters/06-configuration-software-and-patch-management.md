# Chapter 06: Configuration, Software, and Patch Management

![Lab flow for this chapter: baseline.yml, run against localhost, uses the copy module to enforce /etc/lab-baseline.conf's content; the first real run reports changed=1 and the second reports changed=0, proving idempotency, and out-of-band drift is corrected automatically by re-running the same playbook. As a negative test, a copy of the playbook with an added shell append task reports changed=1 on every run and grows the file with a new timestamped line each time, demonstrating the anti-pattern the chapter's Design Considerations section warns against.](../../../diagrams/volume-04-enterprise-systems-administration/chapter-06-ansible-idempotent-baseline-flow.svg)

*Figure 6-1. Flow used throughout this chapter's Hands-On Lab: an idempotent Ansible baseline that self-heals drift, contrasted with a non-idempotent shell-append anti-pattern.*

## Learning Objectives

- Distinguish configuration management, software deployment, and patch
  management as related but separate disciplines, and identify the tooling
  category each depends on.
- Describe push versus pull configuration management architectures and
  where Ansible and PowerShell Desired State Configuration (DSC) fit.
- Design a staged patch-ring strategy across Linux (`dnf`/`apt`) and
  Windows (WSUS/Windows Update for Business) that respects the change
  windows introduced in [Chapter 01](01-systems-administration-architecture-and-operating-model.md).
- Build and reason about a golden-image pipeline for repeatable
  provisioning.
- Detect and remediate configuration drift using the automation
  established in [Volume I](../../volume-01-enterprise-engineering-foundations/README.md).
- Pin and control package versions deliberately, rather than allowing
  uncontrolled "latest wins" installs across the fleet.

## Theory and Architecture

[Chapter 01](01-systems-administration-architecture-and-operating-model.md) introduced the layered automation stack (local, CI, CD,
infrastructure) and the declarative/imperative distinction. This chapter
applies that stack to three related but distinct disciplines that every
systems administrator touches daily:

| Discipline | Question it answers | Representative tooling |
| --- | --- | --- |
| Configuration management | "What state should this host be in, continuously?" | Ansible, PowerShell DSC, Puppet, Chef |
| Software deployment | "What software is installed on this host, and from where?" | `dnf`/`apt`, Chocolatey/`winget`, internal package repositories |
| Patch management | "Which vendor-issued updates have been applied, and on what schedule?" | WSUS, Windows Update for Business, `dnf`/`apt` update channels |

They overlap in practice — a configuration management run often also
installs software — but keeping the questions distinct clarifies which
tool and which change-control process applies to a given task.

### Push versus pull configuration management

- **Push** tools connect outward from a control node to each target and
  apply state over an existing transport: Ansible connects over SSH
  (Linux) or WinRM (Windows) and requires no persistent agent on the
  target. This encyclopedia's automation examples default to Ansible
  (baseline: Ansible core 2.17 / `ansible` 10.x) for this reason — no
  agent lifecycle to manage, and the same control node can reach both
  platforms.
- **Pull** tools run an agent on the target that periodically checks in
  with a central server and reconciles to the last-published desired
  state: Puppet agent/server, Chef client/server, and PowerShell DSC's
  Local Configuration Manager (LCM) in `ApplyAndAutoCorrect` mode all
  follow this pattern. Pull architectures scale reconciliation frequency
  independent of a control node's reach, at the cost of an agent to patch
  and secure on every target.

### Golden image pipeline

A **golden image** is a validated, versioned base image — built with a
tool such as Packer — that new hosts provision from, rather than each host
installing its full software stack from scratch at boot. A mature image
pipeline has four stages: **build** (bake the image from a defined
manifest), **validate** (automated smoke tests and, ideally, the
compliance scan from [Chapter 08](08-systems-security-automation-and-compliance.md)), **promote** (mark the image as the
current default for new provisioning), and **retire** (remove an image
version once no host still depends on it). Treat the image manifest as
version-controlled source, identical in spirit to the repository practices
in [Volume I](../../volume-01-enterprise-engineering-foundations/README.md).

### Patch management architecture

- **Linux** repositories are channel-based: a package manager (`dnf` for
  RPM-family distributions, `apt` for Debian-family) resolves dependencies
  against one or more configured repositories. Enterprises commonly run an
  internal mirror with **staged repository channels** — for example, a
  `current` channel that tracks upstream closely and a `validated` channel
  that only receives packages after they pass a ring of test hosts —
  rather than pointing every host directly at a vendor's public repository.
- **Windows** patch management centers on **WSUS** (Windows Server Update
  Services), which downloads updates once from Microsoft and lets
  administrators approve them into named computer groups (rings), and
  **Windows Update for Business**, which uses deferral and deployment-ring
  policies (delivered via Group Policy or Intune) without requiring a WSUS
  server at all. Both models exist because Windows Server has shipped a
  single cumulative update per month since Windows Server 2016, replacing
  the old model of many independent patches — approval now happens at the
  cumulative-update level, not per-fix.

### Drift detection

**Configuration drift** is the gap between a host's declared desired state
and its actual running state, caused by manual out-of-band changes,
partial automation failures, or software that modifies its own
configuration at runtime. Pull-based tools with continuous reconciliation
(DSC's `ApplyAndAutoCorrect`, a Puppet agent's default interval) close
drift automatically; push-based tools like Ansible require a scheduled,
recurring run (`ansible-pull` on a `systemd` timer, or a CI/CD pipeline
running on a cron trigger) to achieve the same effect, since nothing
enforces state between runs by default.

## Design Considerations

- **Idempotency is not optional.** Every configuration management task
  must produce the same end state whether it runs once or a hundred times
  — this is the same idempotency principle from [Volume I](../../volume-01-enterprise-engineering-foundations/README.md), and it is what
  makes drift-correction runs safe to schedule unattended.
- **Ring design should mirror the change windows from [Chapter 01](01-systems-administration-architecture-and-operating-model.md).** A
  canary/pilot ring, a broad ring, and a final "everything else" ring,
  each separated by a minimum soak time, catches a bad patch or a bad
  configuration change before it reaches the full fleet — design the ring
  boundaries and soak duration before the first incident forces the
  question.
- **Reboot orchestration must respect availability, not just patch
  compliance.** Patching every node in a load-balanced tier simultaneously
  can cause an outage that patching one node at a time, behind the load
  balancer, would not. Sequence reboots explicitly (a rolling-update
  playbook, or a WSUS/cluster-aware update run) rather than triggering
  them all from the same maintenance-window trigger.
- **Repository and package trust.** Only consume signed packages from
  repositories your organization controls or explicitly trusts; an
  internal mirror is both a performance win and a trust boundary, since it
  is the point where a compromised upstream package would be caught (or
  missed) before reaching production.
- **Secrets never belong in plaintext configuration source.** Ansible
  Vault (or an external secrets manager referenced via lookup plugin) and
  DSC's credential encryption certificate exist specifically so playbooks
  and configuration MOFs can be committed to version control without
  embedding a plaintext password.
- **Choose declarative or imperative deliberately per task.** [Chapter 01](01-systems-administration-architecture-and-operating-model.md)
  established this distinction generally; here it becomes concrete —
  desired-state package presence is naturally declarative
  (`ansible.builtin.package: state=present`), while a one-time data
  migration triggered by a patch is naturally imperative (a scripted
  task, run once, not reconciled).

## Implementation and Automation

### Cross-platform desired state with Ansible

```yaml
# ansible/playbooks/baseline-web.yml — declares package presence and a
# managed configuration file, targeting both platform families from the
# inventory established in Chapter 01.
---
- name: Baseline web tier configuration
  hosts: web
  become: true
  tasks:
    - name: Ensure the web server package is installed (Linux)
      ansible.builtin.package:
        name: "{{ 'httpd' if ansible_os_family == 'RedHat' else 'apache2' }}"
        state: present
      when: ansible_system == 'Linux'

    - name: Deploy managed virtual host configuration
      ansible.builtin.template:
        src: templates/vhost.conf.j2
        dest: /etc/httpd/conf.d/app.conf
        mode: '0644'
      when: ansible_os_family == 'RedHat'
      notify: reload web server

  handlers:
    - name: reload web server
      ansible.builtin.service:
        name: httpd
        state: reloaded
```

```bash
# Dry-run first — --check --diff shows what would change without
# applying it, the Ansible analog to Chapter 01's plan/apply separation.
ansible-playbook -i inventory/production.yml playbooks/baseline-web.yml \
  --check --diff

# Apply for real once the plan is reviewed.
ansible-playbook -i inventory/production.yml playbooks/baseline-web.yml
```

### Package version pinning

```bash
# RHEL-family: lock a package (and its currently installed version)
# against upgrades until explicitly unlocked — requires the versionlock
# plugin.
sudo dnf install -y dnf-plugin-versionlock
sudo dnf versionlock add httpd
dnf versionlock list

# Debian-family: hold a package at its current version.
sudo apt-mark hold nginx
apt-mark showhold
```

### Staged patching with Ansible

```yaml
# ansible/playbooks/patch-linux.yml — patches only the "canary" group
# first; the broader rollout is a separate, later run against "broad"
# and "remaining" groups, not a single fleet-wide command.
---
- name: Patch canary ring
  hosts: canary
  become: true
  serial: 1
  tasks:
    - name: Update all packages
      ansible.builtin.package:
        name: '*'
        state: latest
    - name: Reboot if a kernel update requires it
      ansible.builtin.reboot:
        reboot_timeout: 600
      when: ansible_facts.packages is defined
```

### Desired State Configuration on Windows

```powershell
# A DSC configuration declaring a Windows feature and a file's content —
# the Windows analog to the Ansible playbook above. Applies through the
# Local Configuration Manager, which can be set to continuously
# reconcile (ApplyAndAutoCorrect) rather than apply once.
Configuration WebBaseline {
    Import-DscResource -ModuleName PSDesiredStateConfiguration

    Node 'winsrv-web01' {
        WindowsFeature IIS {
            Name   = 'Web-Server'
            Ensure = 'Present'
        }
        File AppConfig {
            DestinationPath = 'C:\inetpub\wwwroot\app\web.config'
            SourcePath      = '\\fileserver\dsc-source\web.config'
            Ensure          = 'Present'
            Type            = 'File'
        }
    }
}

WebBaseline -OutputPath C:\DscConfigs
Set-DscLocalConfigurationManager -Path C:\DscConfigs -ComputerName winsrv-web01
Start-DscConfiguration -Path C:\DscConfigs -Wait -Verbose
```

### WSUS ring approval

```powershell
# Approve a specific update into the pilot computer group only, leaving
# the broad-deployment group untouched until the pilot ring has soaked.
$wsus   = Get-WsusServer
$update = $wsus.GetUpdate([Guid]'b3f1...update-guid...')
$group  = $wsus.GetComputerTargetGroups() | Where-Object Name -eq 'Pilot'

$update.Approve('Install', $group)
```

### Detecting drift on a schedule

```bash
# ansible-pull runs the playbook locally from a Git source, driven by a
# systemd timer on each target — a pull-style pattern built on top of a
# fundamentally push-oriented tool.
sudo tee /etc/systemd/system/config-drift-check.service <<'EOF'
[Unit]
Description=Ansible-pull configuration reconciliation

[Service]
Type=oneshot
ExecStart=/usr/bin/ansible-pull -U https://git.example.internal/infra/baseline.git \
  playbooks/baseline-web.yml
EOF

sudo tee /etc/systemd/system/config-drift-check.timer <<'EOF'
[Unit]
Description=Run configuration drift check every 4 hours

[Timer]
OnCalendar=*-*-* 0/4:00:00
Persistent=true

[Install]
WantedBy=timers.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now config-drift-check.timer
```

## Validation and Troubleshooting

- Confirm a playbook run changed only what was intended:
  `ansible-playbook ... --check --diff` before every apply, and review
  the diff output rather than trusting a clean exit code alone.
- Confirm DSC applied and remains in the desired state:
  `Test-DscConfiguration -ComputerName winsrv-web01` should return
  `True`; `Get-DscConfigurationStatus` shows the history of applied runs.
- Confirm patch compliance evidence, not just "update ran": `rpm -qa
  --last | head` (RHEL-family) or `apt list --upgradable` (Debian-family)
  for Linux; `Get-HotFix | Sort-Object InstalledOn -Descending` or the
  WSUS console's compliance report for Windows.
- Confirm a version lock is actually preventing upgrades: attempt
  `sudo dnf update httpd` (or `sudo apt upgrade nginx`) and confirm the
  locked/held package is skipped, not silently upgraded.

| Symptom | Likely cause | Diagnostic step |
| --- | --- | --- |
| Ansible playbook reports "changed" on every run against the same hosts | Task is not actually idempotent (for example, a raw `shell`/`command` task instead of a proper module) | Review the task for a module with native idempotent behavior; add a `changed_when` guard if a shell task is unavoidable |
| DSC configuration reports `False` from `Test-DscConfiguration` repeatedly | LCM not in `ApplyAndAutoCorrect` mode, or a resource dependency (like a required feature) failed | `Get-DscConfigurationStatus -All`; check the LCM meta-configuration's `ConfigurationMode` |
| Package "update" silently did nothing | Package was version-locked/held from a previous change and the lock was forgotten | `dnf versionlock list` / `apt-mark showhold`; remove the lock deliberately if the update should proceed |
| Patch approved in WSUS but client never installs it | Client not in the targeted computer group, or Group Policy `Configure Automatic Updates` pointed at the wrong WSUS server | `gpresult /r` on the client; confirm WSUS computer group membership in the console |
| `ansible-pull` timer runs but produces no changes despite known drift | Git source not updated, or the timer is pulling a stale branch/tag | Check the timer's last exit code (`systemctl status config-drift-check.service`) and confirm the Git ref being pulled |

## Security and Best Practices

- Store secrets in Ansible Vault or an external secrets manager, and DSC
  credentials behind an encryption certificate — never as plaintext in a
  playbook, MOF, or Git history.
- Sign and verify packages; configure `dnf`/`apt` to reject unsigned
  packages by default rather than opting into verification per install.
- Pin/hold packages deliberately and document why, then remove the pin as
  part of the next planned upgrade — a forgotten permanent pin is a
  silent, growing security gap.
- Separate the credential used to author/plan a configuration change from
  the credential used to apply it in production, mirroring the plan/apply
  separation from [Volume I](../../volume-01-enterprise-engineering-foundations/README.md)'s automation architecture chapter.
- Treat every hardening or baseline setting delivered through
  configuration management as subject to the same code review as
  application code ([Volume I](../../volume-01-enterprise-engineering-foundations/README.md), repository architecture) — this is what
  makes the change auditable after the fact.
- Patch known-exploited or critical-severity CVEs on an accelerated
  timeline outside the normal ring cadence; define that expedited path in
  advance rather than improvising it during an active vulnerability
  disclosure ([Volume X](../../volume-10-enterprise-cybersecurity/README.md) covers vulnerability management in depth).

## References and Knowledge Checks

**References**

- [Ansible documentation: "Ansible Vault," "ansible-pull," and the
  `ansible.builtin.package` module reference (core 2.17 / `ansible` 10.x
  baseline).](https://docs.ansible.com/projects/ansible/latest/cli/ansible-vault.html)
- [Microsoft Learn: "PowerShell Desired State Configuration Overview" and
  "WSUS Deployment Guide."](https://learn.microsoft.com/en-us/powershell/dsc/overview)
- [Microsoft Learn: "Windows Update for Business deployment service."](https://learn.microsoft.com/en-us/windows/deployment/update/deployment-service-overview)
- [Red Hat documentation: "Managing software with DNF" (versionlock
  plugin).](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/managing_software_with_the_dnf_tool/index)
- [HashiCorp Packer documentation: "Golden image workflows."](https://developer.hashicorp.com/packer/tutorials/cloud-production/golden-image-with-hcp-packer)

**Knowledge Checks**

1. What distinguishes configuration management from software deployment
   from patch management, and why does treating them as one discipline
   cause change-control confusion?
2. What is the operational trade-off between a push architecture (Ansible)
   and a pull architecture (DSC, Puppet)?
3. Why should a load-balanced tier be patched with a rolling/sequenced
   reboot rather than all nodes at once?
4. What problem does `ansible-pull` on a `systemd` timer solve that a
   one-time `ansible-playbook` run does not?
5. Why is a forgotten, permanent package version lock a security risk
   rather than a neutral convenience?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each configuration-and-patch skill** —
configuration management, software deployment, patch management, and drift/compliance — cross-platform.
Each ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 6.1–6.4** — a Linux host, a Windows host where noted, and Ansible for
the config-management lab. **Cost:** none.

### Lab 6.1 — Configuration management (Topic: Configuration management)

**Objective:** Enforce desired state with a config-management tool.

```yaml
# Ansible converges both Linux and Windows to a declared state (idempotently):
- hosts: all
  tasks:
    - name: Ensure NTP package present (Linux)
      ansible.builtin.package: { name: chrony, state: present }
      when: ansible_os_family != "Windows"
    - name: Ensure a Windows feature (Windows)
      ansible.windows.win_feature: { name: Telnet-Client, state: present }
      when: ansible_os_family == "Windows"
```

**Expected result:** the same playbook converges Linux (package) and Windows (feature) to a declared
state idempotently — configuration management (Ansible/Puppet/DSC) enforces a *desired state* across
platforms from version-controlled code, so servers are consistent and drift is corrected rather than
hand-fixed.

**Negative test:** configure servers by hand or with one-off scripts; they drift apart and no source
of truth exists — declarative config management keeps the fleet convergent to a defined state.

**Cleanup:** revert lab-only state.

### Lab 6.2 — Software deployment (Topic: Software distribution)

**Objective:** Deploy software at scale from a managed source.

```bash
# Linux: internal repo/mirror serves approved packages
grep -rl "baseurl\|Types:" /etc/apt/sources.list* /etc/yum.repos.d/ 2>/dev/null | head
```

```powershell
# Windows: winget / MSI from a managed source (or SCCM/Intune in enterprise)
winget install --id Microsoft.PowerShell --source winget --accept-package-agreements 2>$null
```

**Expected result:** software installed from a managed/approved source (internal repo, winget, or
enterprise SCCM/Intune) — enterprise software deployment pulls from *controlled* sources so versions
are approved, consistent, and auditable, not downloaded ad-hoc from the internet.

**Negative test:** let each admin download and install software from arbitrary web sources; versions
diverge and supply-chain risk rises — a managed source/repo controls what is deployed.

**Cleanup:** none.

### Lab 6.3 — Patch management (Topic: Patching)

**Objective:** Apply and verify security patches.

```bash
# Linux: apply security updates (automate with unattended-upgrades / dnf-automatic)
sudo apt-get -s upgrade 2>/dev/null | grep -i security | head || \
  sudo dnf updateinfo list security 2>/dev/null | head
```

```powershell
# Windows: query/apply updates (WSUS/Intune manage this centrally)
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 5 HotFixID,InstalledOn
```

**Expected result:** available security updates (Linux) and installed hotfixes (Windows) — patch
management is a core security discipline: identify, test, stage, and apply patches on a cadence, with
tooling (unattended-upgrades/WSUS/Intune) automating it and reporting compliance.

**Negative test:** patch reactively only after an incident; known-vulnerable systems stay exposed for
weeks — a regular, automated patch cycle closes the window between disclosure and remediation.

**Cleanup:** none (read-only in simulation mode).

### Lab 6.4 — Drift detection and compliance (Topic: Compliance)

**Objective:** Detect configuration/patch non-compliance.

```bash
# Config-management check mode reports drift without changing anything:
ansible-playbook site.yml --check --diff 2>/dev/null | grep -E "changed:|ok:" | head || \
  echo "(--check reports what WOULD change = drift from desired state)"
```

**Expected result:** the check run reports resources that differ from the declared state (drift) —
compliance combines config-management check-mode (config drift) with patch/hardening scanning (CIS,
Chapter 08) to prove the fleet matches policy, and to catch the hosts that have drifted before they
cause an incident or audit finding.

**Negative test:** assume enforced-once configuration stays compliant; manual changes and failed
patches drift silently — periodic drift/compliance scanning is what surfaces non-compliant hosts.

**Cleanup:** none.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Configuration management, software deployment, and patch management are
three distinct questions answered by different tools working from the
same automation-first principles established in [Volume I](../../volume-01-enterprise-engineering-foundations/README.md): push
architectures like Ansible and pull architectures like DSC both enforce
idempotent desired state; golden images and staged repository channels
control what software reaches a host; and ring-based, availability-aware
patch rollout — WSUS approval groups or an Ansible `serial` rollout —
turns patching from a risky bulk operation into a controlled, observable
process.

- [ ] Can explain the distinct purpose of configuration management,
      software deployment, and patch management.
- [ ] Can write an idempotent Ansible task and prove idempotency with a
      `--check --diff` dry run followed by a real, then repeated, apply.
- [ ] Can design a patch ring with an explicit soak period and
      availability-aware reboot sequencing.
- [ ] Can pin/hold a package version deliberately and locate the
      lock later.
- [ ] Completed the hands-on lab, including the negative test showing a
      non-idempotent task's incorrect repeated-change behavior.
