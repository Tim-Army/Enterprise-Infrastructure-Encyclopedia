# Chapter 05: Hardening Linux to the STIG

## Learning Objectives

- Describe what the RHEL 9 STIG covers and which areas cause the most
  operational impact.
- Build a STIG-aligned Linux system at install time, using the installer's
  security profile or a kickstart file.
- Remediate an existing system with ComplianceAsCode Ansible content and
  OpenSCAP, and measure the improvement.
- Apply the same approach to Ubuntu with the Ubuntu Security Guide.
- Recognize the STIG settings most likely to break applications, and plan for
  them.

## Theory and Architecture

The Linux STIGs implement the General Purpose Operating System SRG for a
specific distribution and release. DISA publishes STIGs for Red Hat Enterprise
Linux, Canonical Ubuntu LTS releases, SUSE Linux Enterprise, Oracle Linux, and
others. This chapter uses the **RHEL 9 STIG** as its main example because it is
the most widely deployed and best supported by tooling. The approach transfers
to other distributions.

### What the RHEL 9 STIG covers

A Linux STIG runs to several hundred rules. They cluster into a handful of
areas:

| Area | Typical requirements |
| --- | --- |
| **Cryptography** | FIPS mode enabled; system-wide crypto policy restricted to FIPS-approved algorithms |
| **Authentication** | Password length, complexity, and aging; account lockout with `pam_faillock`; no blank passwords; multifactor support |
| **Remote access** | SSH protocol settings, approved ciphers and MACs, no root login, idle timeouts, DoD logon banner |
| **Auditing** | `auditd` running, comprehensive audit rules, audit log protection, and actions when audit storage fills |
| **Integrity** | AIDE file integrity checking; `fapolicyd` application allowlisting; signed package verification |
| **Access control** | SELinux enforcing; `sudo` requiring reauthentication; restrictive file permissions and umask |
| **Filesystems** | Separate partitions for `/var`, `/var/log`, `/var/log/audit`, `/tmp`, and `/home`; `nodev`, `nosuid`, and `noexec` mount options |
| **Attack surface** | Remove unneeded packages and services; disable USB storage and wireless; `firewalld` with a default-deny policy |
| **Sessions** | Session lock and inactivity logout; graphical session settings if a GUI is installed |

### Two ways to get there

```text
Install time                              After install
──────────────                            ─────────────
Installer security profile or kickstart   Scan → remediate → rescan
├── correct partition layout              ├── OpenSCAP --remediate, or
├── FIPS enabled from first boot          ├── generated or packaged Ansible, or
└── STIG profile applied before use       └── a maintained STIG role
```

Install-time hardening is easier and more complete. Partition layout and FIPS
mode are much harder to change on a running system, and applying the profile
before any workload exists avoids surprises. Remediating an existing system is
still common, and the scan, remediate, rescan loop is the same one you use to
keep systems compliant over time.

### Where the remediation content comes from

| Source | What it is | Notes |
| --- | --- | --- |
| **ComplianceAsCode / SCAP Security Guide** | OpenSCAP data streams plus generated Bash and Ansible fixes for the `stig` profile | Shipped in the `scap-security-guide` package; prebuilt playbooks under `/usr/share/scap-security-guide/ansible/` |
| **Ansible Lockdown** | Community Ansible roles (for example `RHEL9-STIG`) that implement the DISA STIG rule by rule | Tagged by STIG ID; useful for selective application |
| **DISA supplemental automation** | Automation content DISA publishes for some STIGs | Check the STIG's download page for availability |
| **Ubuntu Security Guide (USG)** | Canonical's audit and fix tool for Ubuntu, with a `disa_stig` profile | Requires an Ubuntu Pro subscription (free for personal use on a few machines) |

## Design Considerations

- **Harden at build time, then keep it that way.** Make the STIG part of your
  golden image or kickstart. Remediating each server by hand does not scale and
  drifts.
- **Enable FIPS mode at install.** On RHEL 9, enabling FIPS after installation
  is possible but install-time enablement is the supported, cleaner path. Keys
  and certificates created before FIPS mode may need regenerating.
- **Plan partitions up front.** Retrofitting separate `/var/log/audit` and
  `/tmp` partitions on a running system means downtime and data moves.
- **Expect these to break things:**
  - `fapolicyd` blocks any binary not in its trust database, including
    third-party agents and software installed outside RPM.
  - `noexec` on `/tmp` and `/var/tmp` breaks installers and scripts that
    execute from temporary directories.
  - Password aging rules can expire existing service account passwords.
  - Account lockout can lock out automation that retries a bad password.
  - Restricted SSH ciphers and MACs can block older clients and tools.
  - Verbose audit rules generate a lot of log data; size `/var/log/audit` and
    the log pipeline for it.
- **Apply in stages and test.** Run the full profile in a test environment
  first, then roll out with the workload owner involved.
- **Record deliberate exceptions.** If a rule must stay unremediated (for
  example `fapolicyd` for an unsupported agent), document it as a deviation
  (Chapter 09) and exclude it from automation explicitly, so it is not silently
  reverted.

## Implementation and Automation

### Install time: the installer's security profile

In the RHEL 9 graphical installer, open **Security Profile**, choose the **DISA
STIG for Red Hat Enterprise Linux 9** profile, and select **Apply security
policy**. The installer then flags partitioning that does not meet the profile
and applies the remaining rules during installation. For unattended builds, the
equivalent kickstart section is:

```text
%addon com_redhat_oscap
    content-type = scap-security-guide
    profile = xccdf_org.ssgproject.content_profile_stig
%end
```

Combine it with a kickstart partition layout that creates the separate
filesystems the STIG requires, and add `fips=1` to the kernel command line used
for the installation so FIPS mode is on from first boot.

### After install: scan, remediate, rescan

Install the tools:

```bash
sudo dnf install -y openscap-scanner scap-security-guide ansible-core
```

Take a baseline:

```bash
DS=/usr/share/xml/scap/ssg/content/ssg-rhel9-ds.xml
PROFILE=xccdf_org.ssgproject.content_profile_stig
sudo oscap xccdf eval --profile "$PROFILE" \
  --report ~/stig-before.html --results-arf ~/stig-before-arf.xml "$DS"
```

Generate an Ansible playbook for the profile (or use the prebuilt one under
`/usr/share/scap-security-guide/ansible/`):

```bash
oscap xccdf generate fix --fix-type ansible --profile "$PROFILE" \
  --output ~/stig-fix.yml "$DS"
```

Review the playbook, then run it locally. Install any Ansible collections the
playbook reports as missing (commonly `ansible.posix` and `community.general`):

```bash
ansible-galaxy collection install ansible.posix community.general
sudo ansible-playbook -i "localhost," -c local ~/stig-fix.yml
sudo reboot
```

Rescan and compare:

```bash
sudo oscap xccdf eval --profile "$PROFILE" \
  --report ~/stig-after.html --results-arf ~/stig-after-arf.xml "$DS"
```

To recheck a single rule after a change, add `--rule` with the rule's
ComplianceAsCode ID, for example
`xccdf_org.ssgproject.content_rule_sshd_disable_root_login`.

### Ubuntu with the Ubuntu Security Guide

```bash
sudo pro attach <UBUNTU_PRO_TOKEN>
sudo pro enable usg
sudo apt install -y usg
sudo usg audit disa_stig      # writes an HTML report and results
sudo usg fix disa_stig        # applies the profile; review before production
```

USG also supports tailoring files, so you can generate a tailoring file, switch
off rules you have documented exceptions for, and pass it to `audit` and `fix`.

## Validation and Troubleshooting

- **Score did not reach 100 percent after remediation.** Expected. Some rules
  need manual action (partitioning, MFA, organization-specific values), and some
  cannot be fixed automatically by design. Read the remaining failures in the
  after-report one by one.
- **Locked out over SSH after remediation.** Check `/etc/ssh/sshd_config` and
  drop-ins under `/etc/ssh/sshd_config.d/` for disabled root login, the cipher
  list, and the banner, and check `faillock --user <USER>` for a lockout. Keep
  console access to test VMs.
- **An application stopped starting.** Check `fapolicyd` denials
  (`sudo fapolicyd-cli --list` and the audit log) and SELinux denials
  (`sudo ausearch -m AVC -ts recent`).
- **`/var/log/audit` fills up.** The STIG configures `auditd` to act when audit
  storage fills, which can include halting the system. Size the partition and
  forward logs off the host.
- **FIPS checks still fail.** Confirm with `fips-mode-setup --check` and
  `cat /proc/sys/crypto/fips_enabled`. A system installed without FIPS may need
  re-enabling and a reboot.

## Security and Best Practices

- Keep console or out-of-band access to every system you remediate for the
  first time. Several STIG settings can lock out remote access if a value is
  wrong.
- Snapshot or back up before applying the profile to an existing system.
- Run the remediation from version-controlled automation, not ad hoc commands,
  so the same result can be reapplied after drift.
- Remember the ComplianceAsCode `stig` profile is aligned with the DISA STIG but
  maintained separately. For DoD evidence, confirm results with the DISA SCAP
  benchmark and a checklist (Chapter 04).
- Pair hardening with patching. A fully STIG-compliant system with missing
  security updates is still vulnerable.

## References and Knowledge Checks

**References:**

- DISA Red Hat Enterprise Linux 9 STIG and SCAP benchmark (DoD Cyber Exchange).
- Red Hat, *Security hardening* guide for RHEL 9, chapters on scanning and
  remediating with OpenSCAP.
- ComplianceAsCode content project (`github.com/ComplianceAsCode/content`).
- Ansible Lockdown RHEL9-STIG role (`github.com/ansible-lockdown/RHEL9-STIG`).
- Canonical, Ubuntu Security Guide documentation.

**Knowledge checks:**

1. Why is install-time hardening more complete than remediating a running
   system?
2. Name four STIG settings that commonly break applications, and why.
3. What does `oscap xccdf generate fix --fix-type ansible` produce?
4. Why might a fully remediated system still not score 100 percent?
5. What is the Ubuntu equivalent of the ComplianceAsCode STIG profile, and what
   does it require?

## Summary and Completion Checklist

Linux STIGs implement the General Purpose Operating System SRG, covering
cryptography, authentication, SSH, auditing, integrity, SELinux, filesystems,
attack surface, and sessions. The cleanest path is install-time hardening with
the installer's security profile or kickstart, with FIPS on and the right
partition layout. For existing systems, the scan, remediate, rescan loop with
ComplianceAsCode Ansible content gets most of the way, and the remainder needs
manual work or documented deviations. Ubuntu uses the same approach through the
Ubuntu Security Guide.

- [ ] Can list the main areas the RHEL 9 STIG covers.
- [ ] Can harden at install time with the security profile or kickstart.
- [ ] Can remediate with generated Ansible and measure the result.
- [ ] Can name the settings most likely to break applications.
