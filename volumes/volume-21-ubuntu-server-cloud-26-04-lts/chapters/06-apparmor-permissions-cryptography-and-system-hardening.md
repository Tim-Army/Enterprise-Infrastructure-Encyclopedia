# Chapter 06: AppArmor, Permissions, Cryptography, and System Hardening

## Learning Objectives

- Explain AppArmor's profile-based confinement model and how it differs
  from SELinux's label-based model.
- Build, test, and enforce a custom AppArmor profile using the
  `aa-genprof`/`aa-logprof` workflow.
- Apply POSIX ACLs and extended attributes where standard Unix
  permissions are insufficient.
- Encrypt a block device with LUKS, including TPM2-backed automatic
  unlock.
- Apply CIS-aligned hardening using the Ubuntu Security Guide (USG).

## Theory and Architecture

Ubuntu's mandatory access control (MAC) layer is **AppArmor**, not
SELinux. Both frameworks constrain what a process can do beyond
standard discretionary Unix permissions, but they take structurally
different approaches, and conflating them is a common source of
confusion for administrators moving between RHEL-family and
Debian-family systems.

### AppArmor vs. SELinux

| Aspect | AppArmor (Ubuntu) | SELinux (RHEL) |
| --- | --- | --- |
| Confinement basis | Filesystem path | Security label (context) |
| Profile authoring | Plain-text, path-based rules | Type Enforcement policy language |
| Default posture | Profiles apply only to explicitly confined applications | Every subject/object carries a label; unlabeled is denied by policy |
| Learning workflow | `aa-genprof`/`aa-logprof` interactively build a profile from observed behavior | `audit2allow` generates policy from AVC denials |
| Modes | `enforce`, `complain` (log-only) | `enforcing`, `permissive` |

AppArmor's path-based model is generally considered easier to read and
author for a specific application, at the cost of being less precise
than a label-based system when a file legitimately needs to move
between differently-confined contexts (a path-based rule follows the
path, not the file's history). Ubuntu ships AppArmor enabled by default
with profiles for many common packages (`/etc/apparmor.d/`); most
administrators extend or tune existing profiles rather than authoring
one from a blank file.

### AppArmor profile anatomy

A profile is a plain-text rule set, one per confined binary, stored
under `/etc/apparmor.d/` and named after the binary's path with slashes
replaced by dots (`/usr/sbin/nginx` becomes
`usr.sbin.nginx`). Each profile declares:

- **Capabilities** — Linux capabilities the process may use
  (`capability net_bind_service`).
- **File access rules** — path patterns with an access mode
  (`/var/log/nginx/*.log w`, `/etc/nginx/** r`).
- **Network rules** — address family and socket type permissions.

A profile loads in one of two modes: **enforce** (violations are
blocked and logged) or **complain** (violations are logged only, the
action still proceeds) — the same enforce/permissive distinction
SELinux makes, used the same way: build and validate a profile in
complain mode against real traffic, then switch to enforce once the
log shows no unexpected denials.

### Extended permissions: ACLs and extended attributes

Standard Unix permissions (owner/group/other, read/write/execute)
cannot express "this specific additional user needs read access"
without changing group membership. **POSIX ACLs** (`setfacl`/`getfacl`)
add per-user and per-group entries beyond the standard three, and a
**default ACL** on a directory propagates automatically to new files
created within it. **Extended attributes** (`xattr`, manipulated with
`setfattr`/`getfattr`) store arbitrary metadata outside the file's
normal data stream; AppArmor itself, capabilities (`setcap`), and some
backup/replication tools all rely on extended attributes.

### Cryptography: LUKS and TPM2

**LUKS (Linux Unified Key Setup)**, managed through `cryptsetup`,
provides full-disk or per-volume encryption, protecting data at rest if
a disk is lost, stolen, or improperly decommissioned. A LUKS volume
normally requires a passphrase (or key file) at boot to unlock —
`systemd-cryptenroll` extends this to bind the unlock key to the host's
**TPM2** module, so the volume unlocks automatically on a specific,
unmodified machine (verified via TPM PCR measurements) without a human
entering a passphrase at every boot, while still requiring the
passphrase as a fallback if the TPM state changes (for example, after a
firmware or bootloader modification an attacker might have made).

### Hardening frameworks: USG and CIS

The **Ubuntu Security Guide (USG)**, delivered through Ubuntu Pro, is
Canonical's automated hardening and compliance tool: it applies and
audits configuration against published CIS Ubuntu Linux Benchmark and
DISA STIG profiles, using the same OpenSCAP engine RHEL's equivalent
tooling uses. USG can both *audit* (report drift from a profile,
non-destructively) and *fix* (apply the profile's required
configuration), which matters because blind application of a hardening
profile to a running production host without first auditing and
reviewing the diff is a common cause of unplanned outages.

## Design Considerations

- **complain-first profile rollout.** Never move a new or modified
  AppArmor profile straight to enforce mode in production; run it in
  complain mode against a full range of real application behavior
  (including rare code paths — log rotation, a scheduled batch job)
  first, and review `aa-logprof`'s suggestions deliberately rather than
  accepting every one.
  
- **ACL scope creep.** ACLs solve a real problem but are easy to
  overuse into an unreadable, undocumented access model; prefer group
  membership for anything long-lived and broad, and reserve ACLs for
  genuinely exceptional, narrowly-scoped access needs, documented at
  the point they're added.
- **LUKS passphrase vs. TPM2 auto-unlock trade-off.** TPM2 auto-unlock
  removes the operational burden of a human entering a passphrase on
  every boot (critical for unattended reboots and cloud/VM restarts),
  but shifts trust to the TPM's attestation of boot-chain integrity;
  keep a recovery passphrase or key-file escrow regardless, since a
  legitimate firmware update can change PCR measurements and require
  re-enrollment.
- **USG profile selection.** CIS Level 1 is broadly deployable with low
  operational risk; CIS Level 2 and DISA STIG profiles are stricter and
  more likely to conflict with specific application requirements —
  audit first, plan remediation for genuine conflicts, and don't
  disable a control silently just because it broke something without
  documenting the exception.
- **AppArmor coverage gaps.** Not every installed package ships an
  AppArmor profile; a security review should explicitly inventory which
  network-facing or privilege-sensitive applications on a host are
  actually confined (`aa-status`) rather than assuming AppArmor's
  presence means comprehensive coverage.

## Implementation and Automation

### 1. AppArmor status and profile modes

```bash
# Overall AppArmor status: loaded profiles and their mode
sudo aa-status

# Switch a profile between modes
sudo aa-enforce /etc/apparmor.d/usr.sbin.nginx
sudo aa-complain /etc/apparmor.d/usr.sbin.nginx

# Disable a profile entirely (rarely appropriate; prefer complain mode)
sudo ln -s /etc/apparmor.d/usr.sbin.nginx /etc/apparmor.d/disable/
sudo apparmor_parser -R /etc/apparmor.d/usr.sbin.nginx
```

### 2. Building a custom profile with aa-genprof

```bash
sudo apt install -y apparmor-utils

# Start interactive profile generation for a custom binary
sudo aa-genprof /usr/local/bin/report-agent

# In a second terminal, exercise every code path of the application
/usr/local/bin/report-agent --full-run

# Back in aa-genprof, press "S" to scan the log and step through
# each suggested rule (Allow/Deny/Glob/Abort), then "F" to finish

# Refine an existing profile after observing more traffic in complain mode
sudo aa-logprof
```

### 3. Reading AppArmor denials

```bash
# Live denials from the kernel audit stream
sudo journalctl -k -f | grep -i apparmor

# A structured denial looks like:
# apparmor="DENIED" operation="open" profile="usr.sbin.nginx"
#   name="/etc/nginx/secrets.conf" pid=4821 comm="nginx"
#   requested_mask="r" denied_mask="r"
```

### 4. ACLs and extended attributes

```bash
# Grant an additional user read+execute access without changing group ownership
sudo setfacl -m u:auditor:rx /srv/appdata

# Set a default ACL so new files inherit the same grant
sudo setfacl -d -m u:auditor:rx /srv/appdata

# Inspect current ACL entries
getfacl /srv/appdata

# Set and read an extended attribute directly
sudo setfattr -n user.classification -v "internal" /srv/appdata/report.csv
getfattr -n user.classification /srv/appdata/report.csv
```

### 5. LUKS full-disk/volume encryption with TPM2 auto-unlock

```bash
sudo apt install -y cryptsetup

# Initialize a LUKS2 volume on a spare partition
sudo cryptsetup luksFormat /dev/sdc1

# Open it, format the mapped device, and mount
sudo cryptsetup open /dev/sdc1 secure_data
sudo mkfs.ext4 /dev/mapper/secure_data
sudo mkdir -p /srv/secure
sudo mount /dev/mapper/secure_data /srv/secure

# Persist the mapping (with a passphrase prompt at boot) via crypttab
echo "secure_data UUID=$(blkid -s UUID -o value /dev/sdc1) none luks" | \
  sudo tee -a /etc/crypttab

# Bind automatic unlock to the TPM2 (PCR 7 covers Secure Boot state)
sudo apt install -y tpm2-tools
sudo systemd-cryptenroll --tpm2-device=auto --tpm2-pcrs=7 /dev/sdc1

# Confirm both the passphrase and TPM2 tokens are enrolled
sudo cryptsetup luksDump /dev/sdc1 | grep -A2 Tokens
```

### 6. Ubuntu Security Guide (CIS/STIG hardening)

```bash
# USG requires Ubuntu Pro attachment (Chapter 01)
sudo pro enable usg

# List available profiles
usg list

# Audit against CIS Level 1 without changing anything
sudo usg audit cis_level1_server

# Review the generated report before remediating
less /var/lib/usg/*/cis_level1_server-results.html

# Apply the profile after reviewing the audit findings
sudo usg fix cis_level1_server

# Re-audit to confirm remediation and capture residual exceptions
sudo usg audit cis_level1_server
```

## Validation and Troubleshooting

- **An application misbehaves after enabling enforce mode.** Check
  `journalctl -k | grep DENIED` for the exact path and permission
  AppArmor blocked; add the specific rule to the profile (or regenerate
  with `aa-logprof`) rather than disabling the profile outright.
- **`aa-status` shows a profile in complain mode indefinitely.** This is
  a real gap, not a passive state — complain mode logs but does not
  protect; track profiles still in complain mode as an explicit
  remediation backlog item, not a permanent configuration.
- **An ACL doesn't seem to take effect.** Confirm the filesystem was
  mounted with ACL support (`ext4`/`XFS` both support it by default on
  current kernels; verify with `tune2fs -l` or `xfs_info` if in doubt),
  and that no more specific ACL entry or the file's own permission bits
  override the expected grant — `getfacl` shows the effective mask.
- **A LUKS volume with TPM2 enrollment won't auto-unlock after a
  firmware update.** This is TPM2 attestation working as designed — a
  changed PCR 7 measurement (Secure Boot state changed) invalidates the
  TPM-bound token; unlock with the passphrase fallback, then re-enroll
  the TPM token (`systemd-cryptenroll --wipe-slot=tpm2 ...` followed by
  re-enrollment) for the new known-good state.
- **`usg fix` breaks a running application.** This is exactly why
  `usg audit` (non-destructive) should always precede `usg fix`;
  isolate which specific control caused the regression from the audit
  report, and document a scoped, justified exception rather than
  reverting the entire profile.

## Security and Best Practices

- Keep AppArmor enabled and enforcing for every profile Ubuntu ships by
  default; treat a profile stuck in complain mode as a tracked finding,
  not a resolved state.
- Author custom AppArmor profiles for any locally-developed or
  third-party application handling untrusted input or running with
  elevated privileges — an unconfined privileged process is a gap in
  the same class as a service running unnecessarily as root.
- Prefer group membership over ACLs for durable access grants; use ACLs
  sparingly and document each one's purpose at creation time so a
  future audit can determine whether it is still needed.
- Enroll LUKS volumes with both a TPM2 token (operational convenience)
  and an escrowed recovery passphrase or key file (disaster recovery);
  never rely on TPM2 auto-unlock alone with no recovery path.
- Run `usg audit` on a defined schedule (not just at initial hardening)
  so configuration drift away from the target CIS/STIG profile is
  caught before an audit or incident surfaces it.
- Treat any USG-flagged control an administrator chooses not to
  remediate as a documented, time-bound exception with a named owner,
  not a silent gap.

## References and Knowledge Checks

**References**

- AppArmor documentation — `apparmor.net`, `apparmor.d(5)` man page.
- `aa-genprof(8)`, `aa-logprof(8)`, `aa-status(8)` man pages.
- `setfacl(1)`, `getfacl(1)`, `setfattr(1)` man pages.
- `cryptsetup(8)`, `systemd-cryptenroll(1)` man pages.
- CIS Ubuntu Linux Benchmark, Center for Internet Security.
- Ubuntu Security Guide documentation, Canonical (Ubuntu Pro).
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — Ubuntu Server
  26.04 baseline referenced throughout this chapter.

**Knowledge checks**

1. What is the fundamental structural difference between AppArmor's
   confinement model and SELinux's, and what trade-off does that
   difference introduce?
2. Why should a new AppArmor profile be rolled out in complain mode
   before enforce mode, and what specific evidence justifies the switch?
3. What security property does binding LUKS unlock to a TPM2 PCR
   measurement provide that a static passphrase alone does not, and why
   must a recovery path still be retained?
4. Why does the Ubuntu Security Guide separate `audit` from `fix`, and
   what risk does skipping straight to `fix` on a production host
   introduce?

## Hands-On Lab

**Objective:** Confine a simple custom script with a hand-built
AppArmor profile, prove enforcement with a negative test, and encrypt a
scratch volume with LUKS.

**Prerequisites**

- An Ubuntu Server 26.04 LTS VM with `sudo` access and
  `apparmor-utils` installable.
- A spare loop device or virtual disk for the LUKS portion (a loop file
  is used below so no extra disk is required).
- A non-production system, since this lab loads and unloads a custom
  AppArmor profile.

**Steps**

1. Create a simple target script that reads one allowed file and one
   forbidden file:

   ```bash
   sudo mkdir -p /opt/labapp
   sudo tee /opt/labapp/read-config.sh <<'EOF'
   #!/usr/bin/env bash
   echo "Allowed read:"
   cat /opt/labapp/allowed.conf
   echo "Forbidden read attempt:"
   cat /etc/shadow
   EOF
   sudo chmod +x /opt/labapp/read-config.sh
   echo "setting=value" | sudo tee /opt/labapp/allowed.conf
   ```

2. Generate a profile interactively, exercising the script while
   `aa-genprof` watches:

   ```bash
   sudo apt install -y apparmor-utils
   sudo aa-genprof /opt/labapp/read-config.sh
   ```

   In a second terminal, run `sudo /opt/labapp/read-config.sh` while
   `aa-genprof` is waiting, then return to the first terminal and press
   `S` to scan the log. Approve the read of `/opt/labapp/allowed.conf`
   when prompted, but **deny** (or ignore/abort) any suggestion to
   allow `/etc/shadow`, then press `F` to finish and save the profile
   in enforce mode.

3. Confirm the profile is loaded and enforcing:

   ```bash
   sudo aa-status | grep read-config
   ```

   **Expected result:** the profile for `/opt/labapp/read-config.sh`
   appears under the `enforce` list.

4. Run the script again and confirm the allowed read still works:

   ```bash
   sudo /opt/labapp/read-config.sh
   ```

   **Expected result:** the `allowed.conf` content prints normally.

5. **Negative test:** confirm the forbidden read is now blocked and
   logged:

   ```bash
   sudo /opt/labapp/read-config.sh
   sudo journalctl -k -n 20 --no-pager | grep -i apparmor
   ```

   **Expected result:** the `cat /etc/shadow` line either errors
   (`Permission denied`) or returns nothing, and the journal shows an
   `apparmor="DENIED"` entry naming `/etc/shadow` and the
   `read-config.sh` profile — direct evidence enforcement is active.

6. Encrypt a loop-backed scratch volume with LUKS:

   ```bash
   sudo apt install -y cryptsetup
   sudo fallocate -l 200M /root/lab-luks.img
   sudo losetup /dev/loop20 /root/lab-luks.img
   echo -n "LabPassphrase123!" | sudo cryptsetup luksFormat /dev/loop20 -
   echo -n "LabPassphrase123!" | sudo cryptsetup open /dev/loop20 lab_secure -
   sudo mkfs.ext4 /dev/mapper/lab_secure
   sudo mkdir -p /mnt/lab_secure
   sudo mount /dev/mapper/lab_secure /mnt/lab_secure
   echo "encrypted content" | sudo tee /mnt/lab_secure/secret.txt
   ```

   **Expected result:** the file writes successfully, and
   `sudo cryptsetup luksDump /dev/loop20` shows one active keyslot.

7. **Cleanup:**

   ```bash
   sudo umount /mnt/lab_secure
   sudo cryptsetup close lab_secure
   sudo losetup -d /dev/loop20
   sudo rm -f /root/lab-luks.img
   sudo aa-complain /opt/labapp/read-config.sh
   sudo rm -f /etc/apparmor.d/opt.labapp.read-config.sh
   sudo apparmor_parser -R /opt/labapp/read-config.sh 2>/dev/null || true
   sudo rm -rf /opt/labapp
   ```

## Summary and Completion Checklist

AppArmor is Ubuntu's default mandatory access control layer, using
path-based profiles authored and refined through the
`aa-genprof`/`aa-logprof` complain-then-enforce workflow rather than
SELinux's label-based policy model. POSIX ACLs and extended attributes
extend standard Unix permissions for the narrow cases they genuinely
require. LUKS, optionally bound to a TPM2 module through
`systemd-cryptenroll`, protects data at rest with either a passphrase
or automatic, attestation-gated unlock. The Ubuntu Security Guide
brings CIS and DISA STIG hardening to Ubuntu through the same
audit-then-fix discipline that should govern any hardening change to a
production host.

- [ ] Can explain the structural difference between AppArmor and
      SELinux confinement models.
- [ ] Can build, test in complain mode, and enforce a custom AppArmor
      profile.
- [ ] Can apply POSIX ACLs and extended attributes appropriately.
- [ ] Can create a LUKS-encrypted volume and enroll TPM2 auto-unlock
      with a recovery passphrase retained.
- [ ] Can audit and remediate a host against a CIS profile using USG.
- [ ] Completed the hands-on lab, including the negative test and
      cleanup.
