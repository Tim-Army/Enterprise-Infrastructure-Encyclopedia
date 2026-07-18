# Chapter 03: Platform Hardening, Configuration, and Endpoint Defense

## Learning Objectives

- Apply CIS Benchmarks and DISA STIGs to harden server and endpoint
  operating systems, and explain how the two catalogs relate.
- Use security-relevant kernel and mandatory access control (MAC)
  mechanisms — SELinux, AppArmor, and Linux capabilities — to constrain
  process behavior beyond discretionary permissions.
- Design an endpoint detection and response (EDR) deployment and
  distinguish EDR from legacy signature-based antivirus.
- Build and validate a configuration-as-code hardening baseline using
  OpenSCAP and a compliance-as-code pipeline.
- Explain application allow-listing and its role in preventing
  living-off-the-land binary (LOLBin) abuse.
- Run a reproducible lab that hardens a Linux host against a documented
  baseline and validates the result with an automated scan.

## Theory and Architecture

### Hardening baselines: CIS Benchmarks and DISA STIGs

A **hardening baseline** is a documented, testable set of configuration
settings that reduces a system's attack surface relative to its default
installation state. Two catalogs dominate enterprise use:

- **CIS Benchmarks** — consensus-developed, vendor-agnostic baselines
  published by the Center for Internet Security for operating systems
  (RHEL, Ubuntu, Windows Server), hypervisors, cloud platforms, and network
  devices. Each benchmark defines Level 1 (broadly applicable, low
  operational impact) and Level 2 (defense-in-depth, higher assurance,
  potential operational impact) profiles.
- **DISA STIGs** (Security Technical Implementation Guides) — mandatory
  for U.S. Department of Defense systems and widely adopted by other
  regulated and government-adjacent organizations. STIGs are generally
  more prescriptive and stricter than CIS Level 1, and are distributed with
  a machine-readable **SCAP** (Security Content Automation Protocol)
  content stream that enables automated scanning.

The two catalogs overlap substantially (disabling unused network
protocols, enforcing password/account lockout policy, restricting SUID/SGID
binaries) but are not identical; an organization subject to both
obligations should reconcile them into a single internal baseline rather
than scanning against two independently maintained standards. For this
volume's baseline platforms — Red Hat Enterprise Linux 10 and Ubuntu
Server 26.04 LTS, per `SOFTWARE_VERSIONS.md` — current CIS Benchmarks and,
where applicable, STIGs should be pulled directly from CIS and DISA for
the specific release, since benchmark content is revised with each major
OS version.

### Mandatory access control: SELinux and AppArmor

Discretionary access control (standard Unix file permissions, Windows
ACLs) grants the *owner* of a resource control over who else can access
it. **Mandatory access control (MAC)** enforces a system-wide policy that
even a compromised or misconfigured process running as an authorized user
cannot override.

- **SELinux** (default on RHEL-family distributions, including RHEL 10)
  labels every process and object with a security context and enforces
  policy based on type enforcement: a compromised web server process
  running in the `httpd_t` domain cannot read files labeled outside
  `httpd_sys_content_t` even if the underlying Unix permissions would
  otherwise allow it. SELinux operates in three modes: `enforcing`
  (policy applied and violations blocked), `permissive` (violations logged
  but not blocked — useful for policy development), and `disabled`.
  Production systems should run `enforcing`; `permissive` should be a
  temporary troubleshooting state, not a standing configuration.
- **AppArmor** (default on Ubuntu and Debian-family distributions,
  including Ubuntu Server 26.04 LTS) achieves a similar goal through
  path-based profiles rather than SELinux's label-based type enforcement,
  and is generally considered simpler to author but less granular than
  SELinux for complex multi-tenant policy.
- **Linux capabilities** decompose the traditional all-or-nothing root
  privilege into discrete capabilities (`CAP_NET_BIND_SERVICE`,
  `CAP_SYS_ADMIN`, and similar). A process that needs only to bind to a
  privileged port should be granted `CAP_NET_BIND_SERVICE` rather than run
  as root outright — this is the same least-privilege principle from
  Chapter 2 applied at the process level instead of the identity level.

Disabling SELinux or AppArmor because an application "doesn't work with it
enabled" is one of the most common hardening regressions in production
environments; the correct remediation is nearly always to build or extend
a policy module for the application, not to remove the control.

### Endpoint detection and response

Legacy antivirus relies primarily on signature matching against known
malicious file hashes and patterns — effective against commodity malware,
ineffective against novel or fileless techniques. **Endpoint Detection and
Response (EDR)** platforms instead instrument the operating system kernel
and monitor behavioral telemetry — process creation trees, command-line
arguments, network connections, registry/file-system modification
patterns — and correlate that telemetry against behavioral detection
logic, often mapped to MITRE ATT&CK techniques (see Chapter 6). EDR
platforms typically provide:

- Continuous telemetry collection, forwarded to a cloud or on-premises
  analytics backend.
- Behavioral and machine-learning-based detection, in addition to
  signature matching.
- Remote response capability: process termination, host network
  isolation, and file quarantine, initiated from the console without
  physical or interactive host access.
- Retrospective search ("hunt back") — since telemetry is retained, a
  newly identified indicator of compromise can be searched against
  historical activity across the entire fleet, not just detected going
  forward.

**Extended Detection and Response (XDR)** extends the same behavioral
correlation model beyond the endpoint to network, identity, and cloud
telemetry, feeding into or overlapping with the SIEM described in
Chapter 6.

### Application allow-listing and LOLBin abuse

Adversaries increasingly rely on legitimate, pre-installed system
utilities — "living off the land" binaries (LOLBins) such as scripting
interpreters, archive utilities, and remote management tools — to execute
malicious actions without introducing detectable malware files.
**Application allow-listing** (Windows Defender Application Control,
`fapolicyd` on RHEL, or third-party allow-listing agents) inverts the
default posture from "block known-bad" to "permit only known-good,"
blocking execution of any binary or script not explicitly authorized by
policy, publisher signature, or path. This is one of the highest-leverage
hardening controls available — CIS Controls v8.1 ranks application
control among its top safeguards — but it carries meaningful operational
overhead: every legitimate new application, update, or script must be
authorized before it will run, requiring a change-managed allow-list
maintenance process.

### Configuration drift and compliance-as-code

A hardening baseline applied once at provisioning time degrades over time
as administrators make ad hoc changes, patches alter defaults, or
emergency troubleshooting leaves temporary exceptions in place permanently
— **configuration drift**. **OpenSCAP** and equivalent tooling evaluate a
running system against a machine-readable SCAP content stream (frequently
distributed as the same content DISA and CIS publish) and produce a
pass/fail report per rule, which can be scheduled to run continuously and
feed drift back into a remediation pipeline, closing the loop between the
baseline defined in Chapter 1's control crosswalk and the runtime state of
the fleet.

## Design Considerations

- **CIS Level 1 vs. Level 2 trade-off.** Level 2 settings (for example,
  disabling core dumps, stricter audit scope, USB storage restrictions)
  provide meaningful defense in depth but can break legitimate debugging
  workflows or removable-media-dependent business processes. Pilot Level 2
  changes against a representative workload before fleet-wide rollout, and
  document any Level 2 control that is deliberately not applied, with
  compensating controls, in the risk register from Chapter 1.
- **SELinux/AppArmor policy authoring effort** scales with application
  complexity. Off-the-shelf, widely used services (web servers, database
  engines) usually ship well-maintained policy modules; custom in-house
  applications require dedicated policy development time, which should be
  budgeted into the application's deployment timeline rather than
  discovered as a blocker at go-live.
- **EDR agent placement and performance impact.** Kernel-level telemetry
  collection has a measurable CPU and I/O cost, particularly on
  I/O-intensive systems (database servers, build systems). Validate EDR
  performance impact in a representative environment before fleet-wide
  deployment, and use the vendor's exclusion mechanism sparingly and only
  for well-understood, high-volume, low-risk I/O paths — broad exclusions
  reintroduce blind spots.
- **Allow-listing rollout sequencing.** Deploy application allow-listing in
  audit/log-only mode first to characterize the legitimate application
  inventory across the fleet, then move to enforcing mode by workload tier
  (starting with narrowly-scoped, high-value servers) rather than
  attempting a single enterprise-wide enforcing cutover.
- **Baseline reconciliation across regulatory obligations.** When both CIS
  and STIG apply, build one internal baseline that is a documented superset
  or reconciled subset of both, referencing the control crosswalk pattern
  from Chapter 1, so evidence collection satisfies every applicable
  framework from a single scan.
- **Immutable and golden-image patterns** (covered further in Chapter 9)
  reduce configuration drift risk structurally, by replacing
  configuration-in-place with redeployment from a hardened, version-
  controlled image — a design choice that changes how hardening validation
  should be scheduled (at image build time, continuously post-deployment,
  or both).

## Implementation and Automation

### CIS-aligned SSH hardening (RHEL 10 / Ubuntu Server 26.04 LTS)

```bash
# /etc/ssh/sshd_config.d/99-hardening.conf
Protocol 2
PermitRootLogin no
PasswordAuthentication no
KbdInteractiveAuthentication no
X11Forwarding no
MaxAuthTries 4
ClientAliveInterval 300
ClientAliveCountMax 2
AllowTcpForwarding no
LogLevel VERBOSE
```

```bash
sudo sshd -t                              # validate syntax before reload
sudo systemctl reload sshd
```

### SELinux: verifying enforcing mode and troubleshooting denials

```bash
# Confirm enforcing mode (RHEL 10)
getenforce
sestatus

# Never disable SELinux to resolve an application issue — investigate first
sudo ausearch -m avc -ts recent            # review recent AVC denials
sudo sealert -a /var/log/audit/audit.log   # human-readable denial analysis

# Generate a targeted policy module from a denial, then review before loading
sudo audit2allow -a -M local_webapp_policy
cat local_webapp_policy.te                 # review the generated rule
sudo semodule -i local_webapp_policy.pp    # load only after review
```

### AppArmor: enforcing mode on Ubuntu Server 26.04 LTS

```bash
sudo aa-status                             # list profiles and their mode
sudo aa-enforce /etc/apparmor.d/usr.sbin.nginx
sudo systemctl reload apparmor
```

### OpenSCAP baseline scan and remediation

```bash
# RHEL 10 — evaluate against the CIS profile shipped with SCAP Security Guide
sudo oscap xccdf eval \
  --profile xccdf_org.ssgproject.content_profile_cis \
  --results /var/log/scap/cis-results.xml \
  --report /var/log/scap/cis-report.html \
  /usr/share/xml/scap/ssg/content/ssg-rhel10-ds.xml

# Generate a remediation (Ansible) playbook for failed rules, review before applying
sudo oscap xccdf generate fix \
  --fix-type ansible \
  --profile xccdf_org.ssgproject.content_profile_cis \
  /usr/share/xml/scap/ssg/content/ssg-rhel10-ds.xml \
  > cis-remediation.yml
```

Treat the generated remediation playbook as a pull request, not an
auto-applied script: review every task for operational impact before
running it against production, consistent with the compliance-as-code
practice introduced in Chapter 1.

### fapolicyd allow-listing (RHEL)

```bash
sudo systemctl enable --now fapolicyd

# Audit mode first — log would-be denials without blocking
sudo fapolicyd-cli --set-permissive

# Add a trusted directory (build artifacts, internal tooling) to the trust database
sudo fapolicyd-cli --file add /opt/internal-tools --trust-file custom-tools

# After the audit period confirms no unexpected denials, enforce
sudo fapolicyd-cli --set-enforce
sudo systemctl restart fapolicyd
```

### EDR-adjacent host telemetry validation

```bash
# Confirm the EDR agent service is active and reporting (vendor-neutral pattern)
systemctl status edr-agent
edr-cli agent status --check-connectivity --check-last-checkin

# Confirm auditd is capturing process execution for cross-validation with EDR
sudo auditctl -l | grep execve
sudo ausearch -m execve -ts today | tail -20
```

## Validation and Troubleshooting

- **Validate hardening, do not assume it.** A configuration change applied
  once (SSH hardening, SELinux policy) should be re-verified by an
  independent scan (OpenSCAP, or the vendor EDR/CSPM posture check) on a
  recurring schedule, since drift accumulates from patches, emergency
  changes, and manual troubleshooting.
- **Common failure: SELinux/AppArmor disabled during troubleshooting and
  never re-enabled.** Track MAC enforcement state as a fleet-wide metric
  (percentage of hosts in `enforcing`/`enforce` mode) and alert on any host
  that drops out of enforcing mode outside a documented, time-boxed
  maintenance window.
- **Common failure: allow-listing enforcement blocking a legitimate
  emergency change.** Maintain a documented, audited break-glass process
  for temporarily permitting an unlisted binary during an incident, with
  mandatory retrospective review — mirroring the break-glass pattern from
  Chapter 2.
- **Diagnosing SELinux denials**: always start with `ausearch -m avc` and
  `sealert`, not a broad `setenforce 0`; the denial log identifies exactly
  which type enforcement rule blocked the action, usually resolvable with a
  targeted policy module rather than disabling enforcement.
- **Diagnosing EDR agent silence**: a host that stops reporting telemetry
  is itself a detection-worthy event — cross-reference agent
  last-check-in status against the fleet inventory on a schedule, and
  treat a silent-but-online host as higher priority than a host that is
  simply offline, since agent tampering is a known adversary technique for
  evading detection.
- **Reconciling OpenSCAP findings against risk acceptance**: not every
  failed rule warrants immediate remediation — some will have documented,
  approved exceptions in the risk register from Chapter 1. Filter scan
  results against the exception list before treating a report as an
  action queue, so the operations team is not repeatedly asked to
  "re-fix" an accepted risk.

## Security and Best Practices

- Run SELinux or AppArmor in enforcing mode on every production host;
  treat permissive mode as a time-boxed diagnostic state with a tracked
  expiration, never a standing configuration.
- Prefer generating and reviewing targeted policy modules
  (`audit2allow`, custom AppArmor profile edits) over broad exceptions or
  disabling MAC entirely.
- Deploy EDR fleet-wide with centralized, tamper-resistant management —
  local administrators should not be able to disable or uninstall the
  agent without a logged, approved exception.
- Roll out application allow-listing in audit mode first, then enforce by
  workload tier, prioritizing internet-facing and high-value systems.
- Automate baseline scanning (OpenSCAP or equivalent) on a recurring
  schedule and treat scan results as input to the same risk register and
  patch-priority workflow covered in Chapter 5, not a standalone report
  that nobody actions.
- Harden the golden image or build pipeline, not just running instances,
  so new deployments inherit the current baseline automatically rather
  than depending on post-deployment remediation.
- Document every accepted deviation from the baseline with a business
  justification, compensating control, and review date — an unexplained
  deviation is indistinguishable from an unnoticed regression during
  audit.

## References and Knowledge Checks

**References**

- Center for Internet Security, *CIS Benchmarks* (RHEL, Ubuntu, and
  platform-specific editions)
- DISA, *Security Technical Implementation Guides (STIGs)*
- NIST, *SCAP (Security Content Automation Protocol)* specifications
- Red Hat, *SELinux User's and Administrator's Guide* (RHEL 10
  documentation)
- Canonical, *AppArmor documentation* (Ubuntu Server 26.04 LTS)
- MITRE ATT&CK, techniques T1218 (System Binary Proxy Execution) and
  T1562 (Impair Defenses) as reference points for LOLBin abuse and EDR
  tampering detection coverage
- CIS Controls v8.1, Control 4 (Secure Configuration) and Control 2
  (Inventory and Control of Software Assets)

**Knowledge Checks**

1. What is the practical difference between CIS Level 1 and Level 2
   profiles, and how should that difference influence rollout planning?
2. How does SELinux type enforcement differ from standard discretionary
   Unix file permissions?
3. Why is disabling SELinux or AppArmor considered a hardening regression
   rather than a valid fix for an application compatibility issue?
4. What distinguishes EDR from legacy signature-based antivirus in terms
   of detection method and response capability?
5. Why should application allow-listing be deployed in audit mode before
   enforcing mode?
6. What does configuration drift mean in the context of a hardening
   baseline, and what control addresses it?

## Hands-On Lab

**Objective:** Apply a documented SSH hardening baseline to a Linux host,
verify SELinux enforcement, and validate the configuration with an
automated check — including a negative test that confirms a denied
authentication path.

**Prerequisites**

- A RHEL 10 (or compatible) lab VM or container with `sudo` access, SSH
  server installed, and network access limited to a lab/test segment.
- A second host or terminal session capable of initiating an SSH
  connection to the lab VM for validation.
- Do not perform this lab against a host you depend on for your only
  remote access, since the changes disable password authentication.

**Steps**

1. Confirm current SSH configuration and SELinux status:

   ```bash
   sudo sshd -T | grep -E "passwordauthentication|permitrootlogin"
   getenforce
   ```

2. Apply the hardening drop-in file from the Implementation and Automation
   section:

   ```bash
   sudo tee /etc/ssh/sshd_config.d/99-hardening.conf > /dev/null << 'EOF'
   Protocol 2
   PermitRootLogin no
   PasswordAuthentication no
   KbdInteractiveAuthentication no
   X11Forwarding no
   MaxAuthTries 4
   ClientAliveInterval 300
   ClientAliveCountMax 2
   AllowTcpForwarding no
   LogLevel VERBOSE
   EOF
   ```

3. Validate syntax and reload:

   ```bash
   sudo sshd -t && sudo systemctl reload sshd
   ```

4. **Expected result:** `sshd -t` prints no output (syntax valid) and the
   reload succeeds. Confirm the new settings are active:

   ```bash
   sudo sshd -T | grep -E "passwordauthentication|permitrootlogin"
   ```

   Output should show `passwordauthentication no` and
   `permitrootlogin no`.

5. From a second host, confirm key-based access still succeeds (assuming
   an authorized key is already configured for your lab user):

   ```bash
   ssh -o PreferredAuthentications=publickey labuser@<lab-host>
   ```

   **Expected result:** The connection succeeds using the public key.

6. **Negative test:** From the second host, attempt password
   authentication explicitly:

   ```bash
   ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no labuser@<lab-host>
   ```

   **Expected result:** The connection is refused with
   `Permission denied (publickey)` — password authentication is rejected
   at the protocol level rather than prompting, confirming the hardening
   control is enforced.

7. Confirm SELinux is enforcing (RHEL 10 lab hosts):

   ```bash
   getenforce
   ```

   **Expected result:** Output is `Enforcing`. If it is not, do not
   proceed to production use of this configuration without first
   remediating SELinux mode, since this lab assumes an enforcing baseline.

8. Run an OpenSCAP evaluation (if SCAP Security Guide content is
   installed) to independently verify the SSH-related baseline rules:

   ```bash
   sudo oscap xccdf eval \
     --profile xccdf_org.ssgproject.content_profile_cis \
     --results /tmp/cis-results.xml \
     --report /tmp/cis-report.html \
     /usr/share/xml/scap/ssg/content/ssg-rhel10-ds.xml
   grep -i "sshd" /tmp/cis-report.html | head -5
   ```

   **Expected result:** The report includes SSH-related rules (root login
   restriction, password authentication) marked `pass`.

**Cleanup**

```bash
sudo rm -f /etc/ssh/sshd_config.d/99-hardening.conf
sudo sshd -t && sudo systemctl reload sshd
rm -f /tmp/cis-results.xml /tmp/cis-report.html
```

Re-enable password authentication only if your lab environment's baseline
requires it; in a production-representative environment, the hardened
state should remain in place.

## Summary and Completion Checklist

This chapter covered platform hardening as a layered discipline: baseline
selection (CIS Benchmarks and DISA STIGs), mandatory access control
(SELinux and AppArmor) as a backstop against compromised or misconfigured
processes, endpoint detection and response as the behavioral successor to
signature-based antivirus, and application allow-listing as a high-
leverage control against living-off-the-land techniques. Compliance-as-
code tooling (OpenSCAP) closes the loop between a documented baseline and
the actual runtime state of the fleet. The hands-on lab applied a real SSH
hardening baseline, validated it with both a positive and negative
authentication test, and cross-checked the result with an automated SCAP
scan.

- [ ] I can explain the relationship between CIS Benchmarks and DISA
      STIGs and how to reconcile them into one internal baseline.
- [ ] I can explain how SELinux type enforcement or AppArmor path-based
      profiles constrain a compromised process beyond Unix permissions.
- [ ] I can distinguish EDR's behavioral detection model from legacy
      signature-based antivirus.
- [ ] I can describe a safe rollout sequence for application
      allow-listing, from audit mode to enforcement.
- [ ] I can run an OpenSCAP evaluation and interpret its report against a
      documented baseline.
- [ ] I applied and validated an SSH hardening baseline in the hands-on
      lab, including a negative test proving password authentication is
      rejected.
