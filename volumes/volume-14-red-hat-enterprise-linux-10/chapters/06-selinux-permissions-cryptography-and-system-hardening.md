# Chapter 06: SELinux, Permissions, Cryptography, and System Hardening

![Lab flow for this chapter: serving content from a relocated web directory fails because the directory does not carry the correct SELinux context, confirmed by an AVC denial in the audit log; applying the correct persistent file context and relabeling fixes it, and the same request now succeeds. An ACL separately grants one non-owner user write access without touching SELinux policy. A LUKS-encrypted loopback volume mounts and accepts a written file normally. As a negative test, the volume is unmounted and the LUKS mapping closed; searching the raw backing file for the plaintext string finds nothing, confirming the data is not recoverable from the backing file without the LUKS key.](../../../diagrams/volume-14-red-hat-enterprise-linux-10/chapter-06-selinux-acl-luks-flow.svg)

*Figure 6-1. Flow used throughout this chapter's Hands-On Lab: a relocated web content directory triggering and then resolving an SELinux denial, plus a LUKS volume tested for plaintext leakage.*

## Learning Objectives

- Apply and audit standard Linux permissions, special bits, and POSIX
  ACLs for fine-grained access control.
- Explain SELinux's type-enforcement model and operate confidently in
  enforcing mode, including context management and boolean tuning.
- Diagnose and resolve SELinux denials using `sealert`, `ausearch`, and
  `audit2allow` without resorting to permissive mode as a fix.
- Encrypt data at rest with LUKS and manage system-wide cryptographic
  policy.
- Apply automated compliance scanning and remediation with OpenSCAP.
- Build a layered hardening posture combining permissions, SELinux,
  encryption, and auditing.

## Theory and Architecture

RHEL 10 layers three independent access-control mechanisms, each
answering a different question: standard Unix permissions and ACLs
answer "which user or group may read/write/execute this file,"
SELinux answers "which process, regardless of the user running it, may
interact with this resource, and how," and system-wide cryptographic
policy and LUKS answer "is this data protected if the storage medium
itself is lost or the wire is intercepted." Hardening a RHEL 10 host
means getting all three layers right together, not treating any one of
them as sufficient on its own.

### Standard permissions, special bits, and ACLs

Every file carries an owning user, an owning group, and three
permission triads (owner/group/other) for read, write, and execute.
Three special bits extend that model:

| Bit | Effect on a file | Effect on a directory |
| --- | --- | --- |
| SUID (`4000`) | Executes with the file owner's privilege, not the invoking user's | No effect |
| SGID (`2000`) | Executes with the file's group privilege | New files/subdirectories inherit the directory's group |
| Sticky (`1000`) | No effect | Only the file's owner (or root) may delete/rename files inside, even with group/other write |

Standard permissions are coarse: they express exactly one owner and
one group. **POSIX ACLs** (`setfacl`/`getfacl`) extend that to
multiple named users or groups with independent permissions on the
same file or directory, without changing its base ownership — the
mechanism to reach for when "this one additional user needs write
access" would otherwise mean a group restructuring.

### SELinux: type enforcement beyond discretionary access control

Standard permissions and ACLs are **discretionary access control
(DAC)** — the resource owner decides who can access it, and a
compromised or misconfigured process running as that owner inherits
the owner's full DAC rights. SELinux adds **mandatory access control
(MAC)**: a kernel-enforced policy that constrains what a process may
do based on its **type**, independent of the Unix user running it and
independent of DAC permissions on the target file. Even a process
running as root is confined by SELinux policy — this is precisely
what limits the blast radius of a compromised network-facing daemon
that would otherwise have unrestricted root access to the filesystem.

Every process and every file carries an SELinux **context**, expressed
as `user:role:type:level`. In targeted policy (RHEL's default), the
**type** is what almost all policy decisions hinge on: a process
running with type `httpd_t` is only permitted to read files labeled
with types the policy allows for `httpd_t` (such as `httpd_sys_content_t`),
regardless of standard Unix permissions on those files. This is why a
web server can be denied access to a file it has full Unix read
permission on — the DAC and MAC decisions are independent, and both
must permit an action for it to succeed.

SELinux has three modes:

- **Enforcing** — policy violations are blocked and logged. The
  required state for production.
- **Permissive** — policy violations are logged but not blocked, used
  for building and testing new policy or diagnosing a suspected
  SELinux issue without disrupting service.
- **Disabled** — SELinux is off entirely. Strongly discouraged in any
  environment with a security or compliance obligation; permissive
  mode, not disabled, is the correct troubleshooting state, because
  disabling SELinux entirely also stops it from labeling new files,
  which complicates re-enabling it later.

### Booleans and file contexts

Two mechanisms let an administrator tune targeted policy without
writing custom policy modules:

- **Booleans** (`getsebool`/`setsebool`) are pre-defined on/off
  switches for common policy variations — for example,
  `httpd_can_network_connect`, which controls whether the web server
  type is permitted to make outbound network connections (needed for
  a reverse-proxy or database-backed application, unnecessary for a
  purely static site).
- **File contexts** (`semanage fcontext`, applied with `restorecon`)
  define which SELinux type a given path pattern should carry. This
  matters because moving or creating a file with `cp`/`mv`/a text
  editor does not automatically give it the "correct" context for its
  new location — `restorecon` reapplies the policy-defined context
  based on the path, which is the standard fix for "I moved a file
  and now the service that reads it gets denied."

### Cryptography: LUKS and system-wide crypto policy

**LUKS (Linux Unified Key Setup)** provides full-disk or
full-partition encryption at the block device layer, beneath LVM and
the filesystem, protecting data at rest if a drive is lost, stolen, or
improperly decommissioned. A LUKS-encrypted device requires a
passphrase or key file to unlock before the filesystem above it is
even visible to the kernel.

RHEL 10 also defines **system-wide cryptographic policy**
(`update-crypto-policies`), a single control point that sets the
allowed TLS, SSH, IPsec, and Kerberos cryptographic algorithms for
every policy-aware application on the host simultaneously, rather than
requiring each service to be hardened individually. Standard
predefined levels (`DEFAULT`, `FUTURE`, `LEGACY`, and a `FIPS` mode)
trade compatibility against cryptographic strength, and a custom
sub-policy can adjust specific algorithm exceptions without abandoning
the baseline entirely.

### Automated compliance: OpenSCAP

**OpenSCAP** (`oscap`) evaluates a system against a machine-readable
security profile — commonly a CIS Benchmark or a DISA STIG profile
distributed as SCAP content — producing a scored report of pass/fail
results per control, and can generate a remediation script or Kickstart
snippet to bring a system into compliance automatically. This turns
"harden the system" from a manual checklist exercise into a repeatable,
auditable, versionable process consistent with this encyclopedia's
infrastructure-as-code approach elsewhere.

## Design Considerations

- **SELinux is not optional in a hardened design.** Treat "just set it
  to permissive/disabled" as a debugging step, never a permanent
  architecture decision; a compensating control for "this application
  doesn't work under SELinux" is to build correct policy (a boolean, a
  custom module via `audit2allow`, or a corrected file context), not
  to remove the control.
- **ACLs vs. group restructuring.** Reach for an ACL when an access
  need is genuinely exceptional (one contractor needs write access to
  one directory); reach for proper group design when the need is
  structural (an entire team needs ongoing access) — ACL sprawl across
  many files becomes its own audit burden.
- **Where encryption belongs in the stack.** LUKS at the block-device
  layer protects data at rest against physical loss of the medium; it
  does not protect data from a process with legitimate access to the
  mounted, unlocked filesystem, and it does not replace TLS for data
  in transit — a complete design addresses both, deliberately, rather
  than assuming one covers the other.
- **Crypto policy level selection.** `DEFAULT` is the correct starting
  point for most environments; `FIPS` is a compliance requirement in
  specific regulated environments (and has real interoperability
  consequences that should be tested before enforcing broadly);
  `LEGACY` should only be a deliberate, time-boxed exception for a
  specific interoperability need, not a default fallback.
- **Compliance profile selection and drift.** Choose the SCAP profile
  (CIS vs. STIG, and which level/category) that matches actual
  regulatory or contractual obligation, then schedule recurring scans
  — a one-time hardening pass without recurring validation degrades as
  configuration drifts.
- **Key management for LUKS.** A LUKS volume unlockable only by a
  human-entered passphrase does not survive an unattended reboot;
  production designs typically add a key file protected by restrictive
  permissions, a TPM-backed unlock (via `clevis`/`tang`), or an
  automation-supplied key from a secrets manager, chosen deliberately
  rather than defaulting to passphrase-only.

## Implementation and Automation

### 1. Standard permissions, special bits, and ACLs

```bash
# Apply SGID to a shared project directory so new files inherit its group
chgrp projectteam /srv/shared/project
chmod 2770 /srv/shared/project

# Grant one additional user read/write access via ACL, without
# changing group ownership
setfacl -m u:contractor1:rwx /srv/shared/project
getfacl /srv/shared/project

# Set a default ACL so new files inherit the same grant
setfacl -d -m u:contractor1:rwx /srv/shared/project

# Audit for unexpected SUID binaries (a routine hardening check)
find / -xdev -type f -perm -4000 -exec ls -l {} \;
```

### 2. SELinux mode, context, and boolean management

```bash
# Show current mode and policy
getenforce
sestatus

# Set enforcing/permissive at runtime (does not persist across reboot)
setenforce 1     # enforcing
setenforce 0     # permissive

# Persist the mode via /etc/selinux/config
sed -i 's/^SELINUX=.*/SELINUX=enforcing/' /etc/selinux/config

# Show the SELinux context of files and processes
ls -Z /var/www/html
ps -eZ | grep httpd

# Correct a mislabeled file after moving it into a served directory
cp /home/jsmith/index.html /var/www/html/
restorecon -Rv /var/www/html

# Define a persistent custom context for a nonstandard content directory
semanage fcontext -a -t httpd_sys_content_t "/data/web(/.*)?"
restorecon -Rv /data/web

# List and toggle booleans
getsebool -a | grep httpd
setsebool -P httpd_can_network_connect on
```

### 3. Diagnosing and resolving denials

```bash
# Human-readable denial analysis (requires setroubleshoot-server)
sealert -a /var/log/audit/audit.log

# Raw denial search
ausearch -m avc -ts recent

# Generate a custom policy module from recent, reviewed denials
ausearch -m avc -ts recent | audit2allow -M local_httpd_fix
semodule -i local_httpd_fix.pp
```

### 4. LUKS full-disk encryption

```bash
# Encrypt an unused block device (destroys existing data)
cryptsetup luksFormat /dev/sdc1

# Open the encrypted device, creating a mapped device node
cryptsetup luksOpen /dev/sdc1 secure_data

# Format and mount the mapped device like any other block device
mkfs.xfs /dev/mapper/secure_data
mkdir -p /secure_data
mount /dev/mapper/secure_data /secure_data

# Add a second unlock key (for automation or a break-glass key file)
cryptsetup luksAddKey /dev/sdc1 /root/luks-keyfile

# Persist unlocking via /etc/crypttab (key file example)
echo "secure_data  UUID=$(cryptsetup luksUUID /dev/sdc1)  /root/luks-keyfile  luks" >> /etc/crypttab
echo "/dev/mapper/secure_data  /secure_data  xfs  defaults  0 0" >> /etc/fstab
```

### 5. System-wide cryptographic policy

```bash
# Show the current policy level
update-crypto-policies --show

# Set a stricter or FIPS-aligned policy
update-crypto-policies --set FUTURE
# update-crypto-policies --set FIPS

# Apply and confirm
update-crypto-policies
update-crypto-policies --is-applied
```

### 6. OpenSCAP scanning and remediation

```bash
dnf install -y openscap-scanner scap-security-guide

# List available profiles for this platform
oscap info /usr/share/xml/scap/ssg/content/ssg-rhel10-ds.xml

# Evaluate against the CIS profile and produce an HTML report
oscap xccdf eval \
  --profile xccdf_org.ssgproject.content_profile_cis \
  --results /root/scap-results.xml \
  --report /root/scap-report.html \
  /usr/share/xml/scap/ssg/content/ssg-rhel10-ds.xml

# Generate (then review before running) a remediation script
oscap xccdf generate fix \
  --profile xccdf_org.ssgproject.content_profile_cis \
  --output /root/scap-remediate.sh \
  /usr/share/xml/scap/ssg/content/ssg-rhel10-ds.xml
```

## Validation and Troubleshooting

- **Confirm effective access, not just intended access.** A denied
  action can fail at the DAC layer, the SELinux layer, or both; check
  standard permissions (`ls -l`, `getfacl`) and SELinux context
  (`ls -Z`, `sealert`) independently rather than assuming the first
  plausible cause is correct.
- **Diagnose an SELinux denial systematically.** Reproduce the action,
  then immediately check `ausearch -m avc -ts recent`; `sealert`
  translates the raw denial into a plain-language explanation and
  usually suggests the exact `setsebool` or `semanage fcontext`
  command to resolve it — read the suggestion critically rather than
  applying it blindly, since a boolean is sometimes the wrong fix for
  what is actually a mislabeled file.
- **Confirm a fix actually changed policy, not just logged intent.**
  `audit2allow -M` writes a policy module file but does not load it —
  `semodule -i <module>.pp` is required, and `semodule -l | grep
  <name>` confirms it loaded.
- **Diagnose a LUKS volume that fails to unlock at boot.** Check
  `/etc/crypttab` syntax and key file permissions/path first;
  `cryptsetup luksDump /dev/sdc1` confirms the device is genuinely a
  LUKS volume and shows its key slots; a dropped-to-emergency-shell
  boot prompting for a LUKS passphrase interactively is expected
  behavior when no key file is configured for unattended unlock.
- **Diagnose a crypto policy compatibility break.** A client that
  previously connected via TLS/SSH but now fails after
  `update-crypto-policies --set FUTURE` or `FIPS` is often failing
  because it only supports an algorithm the new policy no longer
  permits; `update-crypto-policies --show` combined with the specific
  service's negotiated-cipher log output identifies the mismatch.
- **Interpret an OpenSCAP report correctly.** A failed check is not
  automatically a required fix in every environment — review each
  failure against actual organizational policy before applying
  generated remediation, since some CIS/STIG controls assume a
  deployment context (a workstation, a specific compliance regime)
  that may not match the host being scanned.
- **Common failure: disabling SELinux to "fix" an unrelated
  problem.** A denial appearing in `ausearch` output at the same time
  as an unrelated failure does not prove causation; test with
  `setenforce 0` temporarily to confirm SELinux is actually the cause
  before building a permanent fix, and always return to `setenforce 1`
  once confirmed either way.

## Security and Best Practices

- Run SELinux in enforcing mode on every system with a security or
  compliance requirement; treat a request to disable it as a request
  requiring the same scrutiny as removing any other control, not a
  routine troubleshooting step.
- Prefer `semanage fcontext` plus `restorecon` (a persistent, correct
  file label) over a broad boolean toggle or, worse, an
  `audit2allow`-generated allow-everything module, whenever the root
  cause is actually a mislabeled path.
- Encrypt any volume holding regulated, sensitive, or credential data
  with LUKS, and manage unlock keys through a deliberate process (key
  file with restrictive permissions, `clevis`/`tang`, or a secrets
  manager) rather than a passphrase typed manually at every boot for
  production automation.
- Apply the strictest system-wide crypto policy level compatible with
  actual client/server requirements, and re-evaluate it whenever a
  compliance mandate (FIPS 140-3, for example) changes.
- Run OpenSCAP scans on a recurring schedule (a systemd timer, per
  [Chapter 03](03-boot-systemd-processes-logging-and-scheduled-work.md)) rather than only at initial build time, and track
  remediation as a normal change-managed activity.
- Minimize SUID/SGID binaries to the set actually required, and audit
  for unexpected new ones as part of routine hardening review — a new
  SUID binary appearing outside of a known package update is a strong
  indicator worth investigating.
- Keep ACL usage minimal and documented; an undocumented ACL grant is
  invisible to a standard `ls -l` review and is a common source of
  access nobody remembers authorizing.

## References and Knowledge Checks

**References**

- [`chmod(1)`, `setfacl(1)`, `getfacl(1)` man pages.](https://man7.org/linux/man-pages/man1/chmod.1.html)
- [`sestatus(8)`, `setsebool(8)`, `semanage(8)`, `restorecon(8)` man
  pages.](https://man7.org/linux/man-pages/man8/sestatus.8.html)
- [`sealert(8)`, `ausearch(8)`, `audit2allow(1)` man pages.](https://man7.org/linux/man-pages/man8/ausearch.8.html)
- [`cryptsetup(8)`, `crypttab(5)` man pages.](https://man7.org/linux/man-pages/man8/cryptsetup.8.html)
- [`update-crypto-policies(8)` man page.](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/security_hardening/using-system-wide-cryptographic-policies)
- [SCAP Security Guide project documentation (`scap-security-guide`).](https://www.open-scap.org/security-policies/scap-security-guide/)
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — RHEL 10
  baseline referenced throughout this chapter.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  RHCSA (EX200) blueprint mapping for this volume.

**Knowledge checks**

1. Why can a process be denied access to a file it has full standard
   Unix read permission on?
2. What is the practical difference between fixing an SELinux problem
   with `setsebool` versus `semanage fcontext`, and how do you decide
   which applies?
3. Why is permissive mode an appropriate troubleshooting state but
   disabled mode is not?
4. What does LUKS encryption protect against that TLS does not, and
   vice versa?

## Hands-On Lab

**Objective:** Deliberately trigger and resolve an SELinux denial for
a relocated web content directory, apply an ACL for exceptional
access, and encrypt a scratch volume with LUKS.

**Prerequisites**

- A RHEL 10 host or VM with root/sudo access.
- `httpd` installed (`dnf install -y httpd`) and a spare block device
  or loopback file for the LUKS portion.

**Steps**

1. Create a non-default content directory and serve from it:

   ```bash
   sudo mkdir -p /data/web
   echo "<h1>SELinux lab</h1>" | sudo tee /data/web/index.html
   sudo sed -i 's#DocumentRoot "/var/www/html"#DocumentRoot "/data/web"#' /etc/httpd/conf/httpd.conf
   sudo systemctl enable --now httpd
   curl -s http://localhost/ || echo "Request failed as expected"
   ```

   **Expected result:** the `curl` request fails (connection succeeds
   but returns a 403, or `httpd` fails to start cleanly), because
   `/data/web` does not carry the `httpd_sys_content_t` context.

2. Confirm the denial in the audit log:

   ```bash
   sudo ausearch -m avc -ts recent | tail -20
   sudo sealert -a /var/log/audit/audit.log | head -40
   ```

   **Expected result:** the output identifies `httpd_t` being denied
   access to a path labeled with a type other than
   `httpd_sys_content_t`.

3. Apply the correct persistent fix:

   ```bash
   sudo semanage fcontext -a -t httpd_sys_content_t "/data/web(/.*)?"
   sudo restorecon -Rv /data/web
   curl -s http://localhost/
   ```

   **Expected result:** the request now returns the lab's HTML content
   successfully.

4. Grant one additional non-owner user write access to the content
   directory using an ACL:

   ```bash
   sudo useradd -m contentwriter 2>/dev/null || true
   sudo setfacl -m u:contentwriter:rwx /data/web
   sudo -u contentwriter touch /data/web/from-acl.html && echo "ACL grant confirmed"
   getfacl /data/web
   ```

5. Create and mount a LUKS-encrypted scratch volume using a loopback
   file (no spare disk required):

   ```bash
   sudo dd if=/dev/zero of=/root/luks-lab.img bs=1M count=200
   sudo losetup -fP /root/luks-lab.img
   LOOPDEV=$(sudo losetup -j /root/luks-lab.img | cut -d: -f1)
   sudo cryptsetup luksFormat "$LOOPDEV" --batch-mode
   sudo cryptsetup luksOpen "$LOOPDEV" lab_secure
   sudo mkfs.xfs /dev/mapper/lab_secure
   sudo mkdir -p /mnt/lab_secure
   sudo mount /dev/mapper/lab_secure /mnt/lab_secure
   echo "encrypted lab data" | sudo tee /mnt/lab_secure/secret.txt
   ```

   **Expected result:** the file writes successfully to the mounted,
   decrypted volume.

6. **Negative test:** confirm the underlying loopback file is
   unreadable as plaintext while the mapping is closed:

   ```bash
   sudo umount /mnt/lab_secure
   sudo cryptsetup luksClose lab_secure
   sudo strings /root/luks-lab.img | grep -i "encrypted lab data" \
     || echo "Plaintext not found, as expected"
   ```

   **Expected result:** the `strings` search finds nothing, confirming
   the data is not recoverable from the raw backing file without the
   LUKS key.

7. **Cleanup:**

   ```bash
   sudo losetup -d "$LOOPDEV" 2>/dev/null
   sudo rm -f /root/luks-lab.img
   sudo userdel -r contentwriter
   sudo semanage fcontext -d "/data/web(/.*)?"
   sudo sed -i 's#DocumentRoot "/data/web"#DocumentRoot "/var/www/html"#' /etc/httpd/conf/httpd.conf
   sudo systemctl restart httpd
   sudo rm -rf /data/web
   ```

## Summary and Completion Checklist

Standard permissions and ACLs express discretionary, owner-granted
access; SELinux adds a mandatory, kernel-enforced layer that confines
every process by type regardless of the Unix user or file ownership
involved, and should remain enforcing in production with denials
resolved through correct context and boolean management rather than
disabled. LUKS and system-wide crypto policy protect data at rest and
in transit respectively, and OpenSCAP turns compliance hardening into
a repeatable, auditable process rather than a manual checklist.

- [ ] Can apply special permission bits and POSIX ACLs for
      fine-grained access control.
- [ ] Can operate a system in SELinux enforcing mode and correctly
      diagnose and resolve a denial.
- [ ] Can create, unlock, and persist a LUKS-encrypted volume.
- [ ] Can view and set system-wide cryptographic policy.
- [ ] Can run an OpenSCAP scan and interpret its results.
- [ ] Completed the hands-on lab, including the negative test and
      cleanup.
