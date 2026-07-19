# Chapter 01: Command Quick Reference and Safe Administration

## Learning Objectives

- Translate a common administrative task into the equivalent command on
  Linux (RHEL 10 / Ubuntu 26.04 LTS), Windows Server, Cisco IOS XE, PAN-OS,
  FortiOS, VMware ESXi/vCenter, and AWS CLI without consulting per-volume
  chapters.
- Apply the four safe-administration gates (authorization, backup, dry run,
  rollback plan) before executing any state-changing command in production.
- Distinguish read-only ("show") operations from state-changing operations
  across platforms so that unfamiliar commands can be assessed for risk
  before they are run.
- Build a personal or team command quick-reference card using the format
  established in this chapter.
- Recognize the audit and logging implications of privileged command
  execution on each platform family covered by this encyclopedia.

## Theory and Architecture

Every platform in Volumes I through XXIII exposes a command-line or
API-driven administrative surface, but the verbs, nouns, and safety idioms
differ by vendor lineage. Three lineages account for nearly everything an
enterprise engineer touches:

- **POSIX/Linux lineage** (RHEL 10, Ubuntu 26.04 LTS, and most container and
  automation tooling): verb-noun or noun-first commands, plain-text
  configuration, systemd unit management, and package managers (`dnf`,
  `apt`).
- **Cisco IOS-style lineage** (Cisco IOS XE, and by convention FortiOS and
  many other network operating systems): a `show` namespace for read-only
  state, a global/interface configuration mode entered with `configure
  terminal`, and a running-config/startup-config duality that separates the
  active state from the persisted state.
- **Security-appliance lineage** (PAN-OS, FortiOS): a candidate-configuration
  model where changes are staged and only take effect after an explicit
  commit, mirroring database transaction semantics rather than immediate
  effect.

A fourth pattern, the **declarative/API lineage** (Kubernetes, Terraform,
AWS CLI, VMware PowerCLI/REST), replaces imperative commands with desired-
state manifests reconciled by a controller. Quick-reference material for
this lineage is command syntax for inspecting and applying state, not a
sequence of manual steps.

Safe administration is a property of the *process* wrapped around a
command, not of any single command. The same `no shutdown` or `systemctl
restart` can be routine or catastrophic depending on whether it was
authorized, backed up, tested, and reversible.

## Design Considerations

- **Standardize the read path before the write path.** Teams that agree on
  a common set of `show`/`get`/`describe` commands reduce mean time to
  diagnose (MTTD) far more than teams that standardize configuration syntax,
  because diagnosis happens under time pressure and configuration changes do
  not.
- **Decide where quick-reference material lives.** A wiki page that drifts
  from the actual fleet is worse than no reference at all. Bind quick
  references to the same version-control and review process as
  infrastructure-as-code (see Chapter 04).
- **Map commands to change risk, not to platform.** A useful internal
  taxonomy is: Tier 0 (read-only, always safe), Tier 1 (state-changing,
  reversible within the session, for example an ACL append), Tier 2
  (state-changing, requires a maintenance window, for example a routing
  protocol change), Tier 3 (destructive or hard to reverse, for example a
  factory reset or `rm -rf`). Gate Tier 2 and Tier 3 commands behind change
  management regardless of platform.
- **Account for shell differences on Windows.** PowerShell cmdlets
  (`Get-Verb-Noun`) are the modern baseline for Windows Server; `cmd.exe`
  legacy commands remain present but should not be the reference standard
  for new documentation.
- **Plan for command deprecation.** Vendor CLIs change between major
  releases (see `SOFTWARE_VERSIONS.md`). Quick-reference tables must record
  the baseline version they were validated against.

## Implementation and Automation

### Cross-platform command quick reference

The table below maps common administrative intents to the concrete command
on each platform family, using the dated baselines in
[`SOFTWARE_VERSIONS.md`](../../../SOFTWARE_VERSIONS.md). Read-only commands
are marked **RO**; state-changing commands are marked **RW**.

| Intent | Linux (RHEL 10 / Ubuntu 26.04) | Windows Server (PowerShell) | Cisco IOS XE 17.x | PAN-OS 11.x | FortiOS 7.6.x | VMware vSphere 9.x (PowerCLI/esxcli) | AWS CLI |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Show interface status (RO) | `ip -br addr` / `nmcli device status` | `Get-NetAdapter` | `show ip interface brief` | `show interface all` | `get system interface` | `Get-VMHostNetworkAdapter` | `aws ec2 describe-network-interfaces` |
| Show routing table (RO) | `ip route show` | `Get-NetRoute` | `show ip route` | `show routing route` | `get router info routing-table all` | `esxcli network ip route ipv4 list` | `aws ec2 describe-route-tables` |
| Show running configuration (RO) | `systemctl cat <unit>` / config file review | `Get-Content <path>` | `show running-config` | `show config running` | `show full-configuration` | `Get-VMHost \| Get-VMHostNetwork` | `aws configservice get-resource-config-history` |
| Restart a service (RW) | `systemctl restart <service>` | `Restart-Service <name>` | n/a (process restart via `process restart`) | `debug software restart process <proc>` | `diagnose sys restart` (targeted daemon) | `Restart-VMHostService` | `aws ecs update-service --force-new-deployment` |
| Check disk/storage usage (RO) | `df -hT` / `lsblk` | `Get-Volume` | `show file systems` | `show system disk-space` | `diagnose sys flash list` | `Get-Datastore` | `aws ce get-cost-and-usage` (billing) / `aws s3 ls --summarize` |
| Tail system/security logs (RO) | `journalctl -f -u <unit>` | `Get-WinEvent -LogName Security -MaxEvents 50` | `show logging \| last 50` | `show log system` | `execute log filter` + `execute log display` | `Get-VIEvent` | `aws logs tail <log-group> --follow` |
| Add/modify a local user (RW) | `useradd` / `usermod` | `New-LocalUser` / `Set-LocalUser` | `username <name> privilege <n> secret <pw>` | `set mgt-config users <user>` | `config system admin` | `New-VIAccount` (host) | `aws iam create-user` |
| Update/patch packages (RW) | `dnf upgrade` / `apt upgrade` | `Install-WindowsUpdate` | `install add file <path> activate commit` | `request system software install` | `execute update-now` | `esxcli software vib update` | `aws ssm send-command --document-name AWS-RunPatchBaseline` |
| Apply a firewall/ACL rule (RW) | `nft add rule ...` / `firewall-cmd --add-rich-rule` | `New-NetFirewallRule` | `access-list` + apply to interface | `set rulebase security rules <rule>` | `config firewall policy` | `New-VMHostFirewallException` (host only) | `aws ec2 authorize-security-group-ingress` |
| Back up running configuration (RW*) | `tar czf` of `/etc` + package manifest | `wbadmin start backup` | `copy running-config startup-config` + `copy startup-config tftp:` | `save config to <file>` | `execute backup config tftp` | `Get-VM \| Export-VApp` / config snapshot | `aws backup start-backup-job` |
| Commit staged configuration (RW) | n/a (immediate apply, no candidate stage) | n/a | n/a (immediate apply) | `commit` | `execute cfg save` (auto-commit per command; use `config` transactions for batches) | n/a | `aws cloudformation deploy` (declarative apply) |
| Show current sessions/connections (RO) | `ss -tunap` | `Get-NetTCPConnection` | `show users` / `show ip sockets` | `show session all` | `diagnose sys session list` | `Get-VIEvent -Types Info -Start (Get-Date).AddHours(-1)` | `aws ec2 describe-instances --query 'Reservations[].Instances[].State'` |
| Reboot the device/host (RW, Tier 2) | `systemctl reboot` | `Restart-Computer` | `reload` | `request restart system` | `execute reboot` | `Restart-VMHost` | `aws ec2 reboot-instances` |

\* Backups are classified RW because they write output but do not change
production state; treat the destination and retention of the backup as a
Tier 1 concern (see Chapter 04 for baseline and retention conventions).

### The four safe-administration gates

Apply these gates to every Tier 1–3 command, regardless of platform:

1. **Authorization** — a change record exists (Chapter 04) with an approver
   distinct from the executor for Tier 2/3 changes.
2. **Backup** — the current state (configuration, database, VM snapshot) is
   captured and its location is recorded before the change begins.
3. **Dry run** — the platform's non-committing preview is used first:
   `ansible-playbook --check --diff`, `terraform plan`, PAN-OS/FortiOS
   candidate-config review before `commit`, `kubectl diff`, or a lab/staging
   run for platforms without a native preview mode.
4. **Rollback plan** — a specific, tested command or procedure to return to
   the prior state is written down before the forward change is executed,
   not improvised afterward.

```bash
# Example: safe-administration wrapper pattern for a Linux service change
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak.$(date +%Y%m%d%H%M)
sudo nginx -t                      # dry run / syntax check
sudo systemctl reload nginx        # apply
sudo systemctl status nginx --no-pager  # verify
# Rollback if needed:
# sudo cp /etc/nginx/nginx.conf.bak.<timestamp> /etc/nginx/nginx.conf && sudo systemctl reload nginx
```

## Validation and Troubleshooting

- After any Tier 1+ command, re-run the equivalent Tier 0 read command from
  the table above and diff the output against the pre-change capture.
- On IOS XE, PAN-OS, and FortiOS, use `show archive config differences` /
  configuration audit logs / `diff` against the last saved revision to
  confirm only the intended lines changed.
- For systemd services, `systemctl status <unit>` combined with
  `journalctl -xe` distinguishes a failed start from a failed dependency.
- For PowerShell changes, `Get-EventLog` or `Get-WinEvent` immediately after
  a change surfaces provider-level errors that the cmdlet itself may not
  raise.
- If validation fails, execute the rollback plan captured in gate 4 above
  immediately rather than attempting a forward fix under time pressure;
  forward fixes belong in a follow-up change record.

## Security and Best Practices

- Every privileged command should be attributable to an individual, not a
  shared account: use `sudo` with per-user logging, TACACS+/RADIUS-backed
  device logins (Chapter 03), and named IAM principals rather than root/
  shared admin credentials.
- Enable command accounting (TACACS+ `aaa accounting commands`, Linux
  `auditd`, PowerShell transcription, AWS CloudTrail) so that Tier 1–3
  commands are logged centrally, not only on the local device.
- Never paste production credentials into command history; use credential
  vaults and short-lived tokens (see Volume X and Volume XVII) instead of
  inline `-p password` style flags, which persist in shell history and
  process lists.
- Time-box standing privileged access; prefer just-in-time elevation
  (`sudo` with re-authentication, PAN-OS/FortiOS role-based admin profiles,
  AWS IAM Identity Center permission sets) over permanently assigned
  administrator roles.
- Review this chapter's table after every `SOFTWARE_VERSIONS.md` baseline
  update; CLI syntax changes between major releases are a common source of
  reference drift.

## References and Knowledge Checks

**References**

- `SOFTWARE_VERSIONS.md` (repository root) — dated baseline for every
  platform version cited in this chapter.
- Cisco IOS XE Command Reference (Cisco.com, current release train).
- PAN-OS CLI Reference and PAN-OS Web Interface Reference (Palo Alto
  Networks TechDocs).
- FortiOS CLI Reference (Fortinet Document Library).
- Microsoft PowerShell documentation (`learn.microsoft.com/powershell`).
- AWS CLI Command Reference (`docs.aws.amazon.com/cli`).
- VMware PowerCLI and `esxcli` documentation (VMware by Broadcom TechDocs).

**Knowledge checks**

1. Which of the four safe-administration gates is most often skipped under
   time pressure, and what compensating control reduces that risk?
2. Explain why PAN-OS and FortiOS `commit`/save semantics change how a dry
   run must be performed compared with Cisco IOS XE.
3. A colleague pastes a command containing a plaintext password into a
   shared chat to "save time." What two risks does this create, and what
   should replace that workflow?
4. For a Tier 2 change on a Cisco IOS XE device, list the minimum evidence
   that should exist in the change record before execution.

## Hands-On Lab

**Objective:** Build a validated, versioned command quick-reference card for
your own environment, modeled on this chapter's table.

**Prerequisites:** Access to at least two platforms from the table above
(a lab VM running RHEL 10 or Ubuntu 26.04 is sufficient if no network/
security appliance lab is available); a Markdown editor; local Git
repository (optional but recommended).

1. Create a file `command-card.md` and add a Markdown table with columns
   `Intent`, `Platform`, `Command`, `Read-only or State-changing`, `Tier`.
   **Expected result:** a table skeleton with headers renders correctly in
   a Markdown preview.
2. For each platform available to you, populate five rows covering: show
   interface/network status, show logs, show running configuration, restart
   a service, and back up configuration. **Expected result:** at least five
   populated rows per platform.
3. Execute only the Tier 0 (read-only) commands from your card against a
   lab system and paste a one-line excerpt of real output as a footnote
   under each row. **Expected result:** each Tier 0 row is backed by
   observed output, not assumed syntax.
4. For one Tier 1 command (for example, restarting a non-critical lab
   service), apply the four safe-administration gates: write the
   authorization line, take the backup, run the dry run/verification
   command, and record the rollback command — before executing it.
   **Expected result:** a documented gate sequence exists in the file
   before the state-changing command is run.
5. Execute the Tier 1 command, then immediately run the Tier 0 validation
   command for the same resource and record the diff (or "no change"
   result). **Expected result:** validation output confirms the intended
   and only the intended change.
6. Negative test: intentionally mistype a flag on a *read-only* command
   (for example, an invalid option to `systemctl status`) and record the
   resulting error text in the card as a "common failure" note.
   **Expected result:** the card documents at least one real error message,
   improving its diagnostic value.
7. Commit the file to a personal or team repository with a message
   describing the platforms covered. **Expected result:** version history
   exists for the reference card, satisfying the design consideration that
   quick references must not drift silently.

**Cleanup:** Restart any lab service left in a non-default state, remove
temporary backup files created during the exercise, and revoke any
elevated access granted solely for the lab.

## Summary and Completion Checklist

This chapter established a cross-platform command quick-reference table
spanning Linux, Windows, Cisco IOS XE, PAN-OS, FortiOS, VMware, and AWS, and
defined the four safe-administration gates — authorization, backup, dry
run, and rollback plan — that convert an arbitrary command into a safe
production change. Command Tiering (0–3) gives a platform-independent way to
decide how much process should wrap a given command.

- [ ] I can locate the equivalent read-only and state-changing command for
      a given intent across at least four platform families.
- [ ] I can classify any command into Tier 0–3 and explain the process each
      tier requires.
- [ ] I applied all four safe-administration gates to a real state-changing
      command in the lab.
- [ ] I produced and version-controlled a personal command quick-reference
      card.
- [ ] I can name at least one platform-specific validation technique for
      confirming a change succeeded as intended.
