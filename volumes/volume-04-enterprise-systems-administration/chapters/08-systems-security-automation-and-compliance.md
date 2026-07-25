# Chapter 08: Systems Security, Automation, and Compliance

![Lab flow for this chapter: a baseline oscap xccdf eval against the CIS profile records a nonzero fail count on a fresh VM; harden-ssh.yml sets PermitRootLogin no via lineinfile and reloads sshd, and a re-scan shows the root-login rule now passing where it previously failed. As a negative test, PermitRootLogin is manually reverted to yes and sshd reloaded; a targeted re-scan catches the regression, showing the same rule failing again, demonstrating why the automation feedback loop must include re-scanning rather than trusting a one-time remediation.](../../../diagrams/volume-04-enterprise-systems-administration/chapter-08-openscap-ansible-remediation-flow.svg)

*Figure 8-1. Flow used throughout this chapter's Hands-On Lab: an OpenSCAP baseline scan driving a targeted Ansible fix, with a regression re-scan proving the feedback loop actually closes.*

## Learning Objectives

- Apply CIS Benchmark and DISA STIG hardening baselines through
  automation, extending the enforcing-mode SELinux/AppArmor guidance from
  [Chapter 02](02-enterprise-linux-administration.md) and the Server Core/hardening guidance from [Chapter 03](03-windows-server-administration.md).
- Automate compliance scanning on Linux with OpenSCAP and on Windows with
  local security policy and baseline tooling.
- Configure host-based audit logging — `auditd` on Linux, Advanced Audit
  Policy on Windows — to produce evidence for compliance frameworks.
- Detect and remediate drift from a security baseline using the
  configuration management tooling introduced in [Chapter 06](06-configuration-software-and-patch-management.md).
- Design an exception-management process for baseline items that conflict
  with a specific application's requirements.
- Explain how host-level compliance automation in this chapter feeds the
  broader security program covered in [Volume X](../../volume-10-enterprise-cybersecurity/README.md).

## Theory and Architecture

Earlier chapters mentioned hardening in passing — SELinux/AppArmor
enforcing mode ([Chapter 02](02-enterprise-linux-administration.md)), Server Core and disabled legacy protocols
([Chapter 03](03-windows-server-administration.md)), tiered administration ([Chapter 04](04-enterprise-identity-and-directory-services.md)). This chapter treats
security hardening and compliance as their own discipline: where
authoritative baselines come from, how to scan and remediate against them
as code rather than by hand, and how to produce the audit evidence a
compliance program actually needs. Enterprise-wide security architecture,
threat detection, and incident response are covered in [Volume X](../../volume-10-enterprise-cybersecurity/README.md); this
chapter stays at the individual host's configuration and audit-logging
layer.

### Hardening baseline sources

| Source | Publisher | Character |
| --- | --- | --- |
| CIS Benchmarks | Center for Internet Security | Community-developed, consensus-based; Level 1 (broadly safe) and Level 2 (stricter, more operational impact) profiles per platform |
| DISA STIG | Defense Information Systems Agency | U.S. government-mandated for DoD systems, widely adopted elsewhere; findings categorized by severity (CAT I highest, CAT III lowest) |
| Vendor security baselines | Microsoft (Security Compliance Toolkit), Red Hat, Canonical | Vendor-authored recommended settings, often the input CIS/STIG themselves partially draw from |

All three ultimately map back to control families in frameworks like
NIST SP 800-53 — a compliance program typically selects one baseline as
its primary implementation standard and demonstrates that baseline
satisfies the higher-level control framework an auditor is actually
assessing against.

### Compliance as code

Manually walking a STIG checklist against each host does not scale and is
not repeatable evidence. **OpenSCAP** implements the SCAP (Security
Content Automation Protocol) standard on Linux: XCCDF documents define
checklist structure and remediation, OVAL definitions define the actual
system checks, and a **profile** (a named subset of rules — `cis`,
`stig`, and others) selects which rules apply for a given scan. The
`scap-security-guide` package ships ready-made profiles for RHEL and other
major distributions. Windows has no single equivalent tool, but the same
compliance-as-code pattern applies through **DSC's `SecurityPolicyDsc`
resource module**, **`secedit`** for local security policy export/import,
and Group Policy for domain-wide baseline delivery (extending [Chapter 04](04-enterprise-identity-and-directory-services.md)).

### Audit logging architecture

- **`auditd`** (Linux) loads rules that watch specific files, syscalls, or
  syscall arguments, writing tamper-evident records to
  `/var/log/audit/audit.log`. Rules live in `/etc/audit/rules.d/*.rules`
  and are compiled/loaded with `augenrules`. `ausearch` and `aureport`
  query the resulting log; raw `grep` against `audit.log` is possible but
  loses the structured-record advantages those tools provide.
- **Windows Advanced Audit Policy** replaces the older, coarser basic
  audit policy with granular subcategories (Logon, Object Access, Process
  Creation, and others), each independently configurable for success
  and/or failure auditing. Key event IDs administrators query most often:
  `4624`/`4625` (successful/failed logon), `4688` (process creation, with
  command-line auditing enabled separately), and `4732`
  (member added to a security-enabled local group).

### The automation feedback loop

Compliance automation is a loop, not a one-time project: **scan** against
the chosen profile, **report** findings, **remediate** through the
configuration management tooling from [Chapter 06](06-configuration-software-and-patch-management.md) (never by hand, so the
fix is repeatable and auditable), and **re-scan** to confirm. Running
remediation automatically in production before validating it in a
non-production ring is the most common way hardening automation causes an
outage — a setting that is correct per the baseline can still break a
specific application's assumption.

## Design Considerations

- **Choose the baseline level deliberately.** CIS Level 2 and STIG CAT I
  items are often stricter than a given environment needs and can disable
  functionality (for example, ICMP restrictions that break latency
  monitoring) — select the level per workload class, and document why a
  stricter or looser level applies where it deviates from the fleet
  default.
- **Scan-and-report before auto-remediate in production.** Run the scan
  loop in audit-only mode against a new baseline version first, review the
  finding delta, then enable automated remediation once the findings are
  understood — the same crawl-walk-run discipline as any other automation
  rollout.
- **Exceptions must be documented and time-bound.** A baseline item that
  genuinely conflicts with an application's requirement needs a recorded,
  approved, expiring waiver — not a silent permanent skip that erodes
  scan-result trust over time.
- **Balance audit verbosity against downstream cost.** Auditing every
  object access on a busy file server can produce more log volume than
  the SIEM/retention budget can absorb ([Chapter 09](09-monitoring-troubleshooting-and-lifecycle-operations.md)); scope audit rules to
  what the compliance requirement and threat model actually need.
- **Protect who can change the baseline automation itself.** Baseline
  playbooks/configurations are high-leverage code — apply the same
  CODEOWNERS/branch-protection discipline from [Volume I](../../volume-01-enterprise-engineering-foundations/README.md) so a change to the
  security baseline gets reviewed like any other security-relevant
  change.
- **Re-scan after every patch cycle**, not only on a fixed calendar —
  [Chapter 06](06-configuration-software-and-patch-management.md)'s patch process can silently revert a hardening setting a
  vendor update touches.

## Implementation and Automation

### Scanning a Linux host with OpenSCAP

```bash
# Install SCAP content and evaluate the CIS profile, producing both a
# machine-readable results file and a human-readable HTML report.
sudo dnf install -y openscap-scanner scap-security-guide

sudo oscap xccdf eval \
  --profile xccdf_org.ssgproject.content_profile_cis \
  --results /var/log/scap/results.xml \
  --report /var/log/scap/report.html \
  /usr/share/xml/scap/ssg/content/ssg-rhel10-ds.xml
```

### Remediating findings through configuration management

```yaml
# ansible/playbooks/harden-ssh.yml — a targeted remediation for a common
# CIS/STIG finding (root SSH login, already flagged conceptually in
# Chapter 02), applied through the same idempotent tooling as Chapter 06
# rather than a manual edit.
---
- name: Harden sshd against a known baseline finding
  hosts: linux
  become: true
  tasks:
    - name: Disable direct root SSH login
      ansible.builtin.lineinfile:
        path: /etc/ssh/sshd_config
        regexp: '^#?PermitRootLogin'
        line: 'PermitRootLogin no'
      notify: reload sshd

  handlers:
    - name: reload sshd
      ansible.builtin.service:
        name: sshd
        state: reloaded
```

```bash
# OpenSCAP can also drive its own remediation directly for rules that
# ship an OVAL fix action — useful for a first pass, but track exactly
# which rules it changed before trusting it unattended in production.
sudo oscap xccdf eval \
  --profile xccdf_org.ssgproject.content_profile_cis \
  --remediate \
  --results /var/log/scap/remediated-results.xml \
  /usr/share/xml/scap/ssg/content/ssg-rhel10-ds.xml
```

### `auditd` rules for compliance evidence

```bash
# /etc/audit/rules.d/compliance.rules — watch changes to core identity
# files and log every execve call, both common STIG/CIS requirements.
sudo tee /etc/audit/rules.d/compliance.rules <<'EOF'
-w /etc/passwd -p wa -k identity_changes
-w /etc/shadow -p wa -k identity_changes
-w /etc/sudoers -p wa -k privilege_changes
-a always,exit -F arch=b64 -S execve -k process_execution
EOF

sudo augenrules --load
sudo systemctl status auditd

# Query the resulting evidence.
sudo ausearch -k identity_changes -ts today
sudo aureport -k --summary
```

### Windows Advanced Audit Policy and local security policy

```powershell
# Enable success and failure auditing for logon events and privileged
# use — the Windows analog to the auditd rules above.
auditpol /set /subcategory:"Logon" /success:enable /failure:enable
auditpol /set /subcategory:"Sensitive Privilege Use" /success:enable /failure:enable
auditpol /get /category:* | Out-File C:\baseline\current-audit-policy.txt

# Export current local security policy, edit against the baseline
# offline, then import — secedit is built in and requires no additional
# toolkit download.
secedit /export /cfg C:\baseline\current.inf
secedit /configure /db C:\Windows\security\local.sdb `
    /cfg C:\baseline\stig-baseline.inf /overwrite /log C:\baseline\secedit.log
```

### Continuous compliance scanning on a schedule

```bash
sudo tee /etc/systemd/system/compliance-scan.service <<'EOF'
[Unit]
Description=Weekly OpenSCAP compliance scan

[Service]
Type=oneshot
ExecStart=/usr/bin/oscap xccdf eval --profile xccdf_org.ssgproject.content_profile_cis \
  --results /var/log/scap/results-%d.xml --report /var/log/scap/report-%d.html \
  /usr/share/xml/scap/ssg/content/ssg-rhel10-ds.xml
EOF

sudo tee /etc/systemd/system/compliance-scan.timer <<'EOF'
[Unit]
Description=Run compliance scan weekly

[Timer]
OnCalendar=weekly
Persistent=true

[Install]
WantedBy=timers.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now compliance-scan.timer
```

## Validation and Troubleshooting

- Confirm a scan actually ran and produced evidence: check the report's
  pass/fail summary and timestamp, not just that the command exited `0`.
- Confirm remediation did not break the workload it touched: after
  running the SSH-hardening playbook, confirm `sshd` reloaded cleanly
  (`systemctl status sshd`) and that a legitimate non-root administrator
  can still authenticate.
- Confirm `auditd` rules loaded: `sudo auditctl -l` should list every rule
  from the rules file; a rule that fails to load (often due to a syntax
  error) is silently absent rather than erroring loudly at boot.
- Confirm Windows audit policy applied as configured:
  `auditpol /get /category:*` should show the enabled subcategories; a
  Group Policy-delivered audit policy that conflicts with a locally set
  one can silently override the local setting at the next `gpupdate`.

| Symptom | Likely cause | Diagnostic step |
| --- | --- | --- |
| OpenSCAP scan reports many more failures after a routine patch | Vendor update reset a previously remediated setting | Compare current results against the last known-good report; re-run remediation and re-scan |
| `auditd` rule silently missing from `auditctl -l` | Syntax error in the rules file, or rules not reloaded after edit | `augenrules --check`; `sudo systemctl status auditd` for load errors |
| SSH hardening playbook locks out legitimate access | `PermitRootLogin no` applied without confirming a non-root admin account with `sudo` exists and works first | Test on a canary host with an active out-of-band console session before fleet-wide rollout |
| Windows audit policy reverts after `gpupdate` | A domain GPO's audit policy setting is overriding the local `secedit` configuration | `gpresult /r`; find and reconcile the conflicting GPO rather than re-applying the local setting repeatedly |
| Compliance scan timer never runs | Timer not enabled, or `OnCalendar` expression malformed | `systemctl list-timers compliance-scan.timer`; `systemd-analyze calendar weekly` to validate the expression |

## Security and Best Practices

- Treat baseline automation (playbooks, DSC configurations, `secedit`
  templates) as security-critical code: version-controlled, reviewed, and
  protected by the same CODEOWNERS/branch-protection controls as any
  other sensitive change (Volume I).
- Grant exceptions as documented, time-bound waivers with an owner and an
  expiration/re-review date — never as a silent, permanent scan exclusion.
- Forward audit logs to a remote collector immediately (Chapter 09; deep
  dive in Volume XI) rather than relying on local retention alone — a
  host-local audit log is not trustworthy evidence once an attacker has
  local privilege.
- Restrict who can modify or clear `auditd` rules and the Windows
  Security event log; both are themselves high-value targets for an
  attacker attempting to hide activity.
- Re-scan after every patch cycle and after every baseline version bump,
  not only on a fixed calendar, so drift introduced by an update is caught
  quickly.
- Resist the temptation to disable a control just to make a scan pass
  without understanding what the control was protecting against — that
  converts a compliance program into a metric-gaming exercise rather than
  an actual security control.

## References and Knowledge Checks

**References**

- [NIST SP 800-53 Rev. 5](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) — control catalog most CIS/STIG baselines map
  back to.
- [CIS Benchmarks (Center for Internet Security)](https://www.cisecurity.org/cis-benchmarks) — Linux and Windows Server
  benchmark documents.
- [DISA STIG documents (Cyber Exchange) for RHEL and Windows Server.](https://public.cyber.mil/stigs/downloads/)
- [Red Hat documentation: "Security hardening" (OpenSCAP, `scap-security-
  guide`).](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/security_hardening/index)
- [Microsoft Learn: "Advanced security audit policy settings" and
  "SecurityPolicyDsc module."](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/advanced-audit-policy-configuration)
- [`auditd(8)`, `auditctl(8)`, `ausearch(1)` man pages.](https://man7.org/linux/man-pages/man8/auditd.8.html)

**Knowledge Checks**

1. What is the difference between CIS Benchmark Level 1 and Level 2
   profiles, and why might an enterprise apply different levels to
   different workload classes?
2. Why should compliance remediation run in audit-only/report mode
   before automated remediation is enabled in production?
3. What tamper-evidence advantage does `auditd`'s structured logging
   have over relying on general syslog messages alone?
4. Why must a security-baseline exception be time-bound rather than a
   permanent scan exclusion?
5. What is a plausible reason a compliance scan's pass rate would drop
   immediately after a routine patch cycle, and how would you confirm
   that hypothesis?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each security-and-compliance skill** —
hardening baselines, access control, security automation, and audit/compliance — cross-platform. Each
ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 8.1–8.4** — a Linux host (`sudo`) and a Windows host where noted.
**Cost:** none.

### Lab 8.1 — Hardening baselines (Topic: Hardening)

**Objective:** Assess a host against a security benchmark.

```bash
# Linux: scan against a CIS/STIG profile (OpenSCAP) or a quick audit (Lynis)
sudo lynis audit system --quick 2>/dev/null | grep -E "Hardening index|Warning" | head || \
  echo "OpenSCAP: oscap xccdf eval --profile cis ... grades against the benchmark"
```

```powershell
# Windows: baseline via Security Compliance Toolkit / secedit analysis
secedit /export /cfg C:\baseline.inf 2>$null; Get-Content C:\baseline.inf | Select-String "PasswordLength"
```

**Expected result:** a hardening score/report against a recognized benchmark (CIS/STIG) — hardening
reduces attack surface by disabling unneeded services and enforcing secure settings, measured against
a standard baseline so compliance is provable, not assumed.

**Negative test:** deploy servers with vendor defaults and no benchmark; unnecessary services and weak
settings remain — a hardening pass against CIS/STIG closes the well-known exposures.

**Cleanup:** `rm -f C:\baseline.inf` on Windows if created.

### Lab 8.2 — Access control and least privilege (Topic: Authorization)

**Objective:** Grant only the privileges a role requires.

```bash
# Linux: scoped sudo via a drop-in (not blanket root)
echo '%dbadmin ALL=(ALL) /usr/bin/systemctl restart postgresql' | sudo tee /etc/sudoers.d/dbadmin
sudo visudo -cf /etc/sudoers.d/dbadmin
```

```powershell
# Windows: delegate specific rights / groups rather than Domain Admins
Get-ADGroupMember "Domain Admins" | Select Name   # audit: should be minimal
```

**Expected result:** a dbadmin role that can restart only PostgreSQL (not full root), and a minimal
Domain Admins membership — least privilege grants each role only the specific rights it needs, so a
compromised account cannot do more than its function; over-privileged accounts are a top attack path.

**Negative test:** give operators full sudo/Domain Admin "for convenience"; any compromise becomes
total — scoped privileges (specific sudo commands, delegated rights) contain the blast radius.

**Cleanup:** `sudo rm -f /etc/sudoers.d/dbadmin`.

### Lab 8.3 — Security automation (Topic: Automation)

**Objective:** Enforce security config as code.

```yaml
# Ansible enforces a security control fleet-wide (idempotent, auditable):
- hosts: all
  become: true
  tasks:
    - name: Disable root SSH login (Linux)
      ansible.builtin.lineinfile:
        path: /etc/ssh/sshd_config
        regexp: '^#?PermitRootLogin'
        line: 'PermitRootLogin no'
      notify: restart sshd
      when: ansible_os_family != "Windows"
```

**Expected result:** the security control (no root SSH) is enforced across the fleet from code and
re-applied on drift — security automation makes controls consistent and self-healing: the policy is
version-controlled, applied everywhere, and drift is corrected, rather than configured by hand and
forgotten.

**Negative test:** apply security settings by hand on each host; they drift, some hosts are missed,
and there is no audit trail — automation applies the control uniformly and provably.

**Cleanup:** revert lab-only changes.

### Lab 8.4 — Audit and compliance (Topic: Compliance)

**Objective:** Produce evidence of the security posture.

```bash
# Linux: auditd records security-relevant events for compliance/forensics
sudo auditctl -w /etc/passwd -p wa -k identity 2>/dev/null && sudo ausearch -k identity 2>/dev/null | tail -3 || \
  echo "auditd watches sensitive files; compliance = benchmark scan results + audit logs + access reviews"
```

**Expected result:** an audit rule recording changes to sensitive files, feeding the compliance
evidence trail — compliance combines benchmark scan results (Lab 8.1), audit logs (who changed what),
and periodic access reviews into provable evidence that the fleet meets policy, which auditors and
frameworks require.

**Negative test:** claim compliance with no audit logging, scans, or access reviews; you cannot prove
the posture and an audit fails — compliance is evidence-based, produced by continuous auditing and
scanning.

**Cleanup:** `sudo auditctl -W /etc/passwd -p wa -k identity 2>/dev/null; true`.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Security hardening becomes a durable control, rather than a one-time
project, when it is scanned, remediated, and re-scanned as code: CIS
Benchmarks and DISA STIG supply the baseline, OpenSCAP and Windows
security-policy tooling automate the scan, the configuration management
tooling from Chapter 06 automates the fix, and `auditd`/Advanced Audit
Policy produce the evidence a compliance program needs. This host-level
loop is the foundation the broader Volume X security program builds on.

- [ ] Can explain the difference between a CIS Benchmark, a DISA STIG,
      and a vendor security baseline.
- [ ] Can run an OpenSCAP scan, interpret its results, and remediate a
      specific finding through idempotent automation rather than a manual
      edit.
- [ ] Can configure `auditd` rules or Windows Advanced Audit Policy to
      produce compliance evidence for a specific control.
- [ ] Can explain why remediation must be validated on a canary host
      before fleet-wide rollout.
- [ ] Completed the hands-on lab, including the negative test proving a
      re-scan catches a deliberately reintroduced regression.
