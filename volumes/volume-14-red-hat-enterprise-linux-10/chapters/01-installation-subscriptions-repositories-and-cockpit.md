# Chapter 01: Installation, Subscriptions, Repositories, and Cockpit

## Learning Objectives

- Describe the RHEL 10 installation workflow, including Anaconda,
  Kickstart, and image-based provisioning with Image Builder.
- Register a system against Red Hat Subscription Management (RHSM) or
  Simple Content Access, and explain how entitlements map to content.
- Configure and prioritize `dnf` repositories, including BaseOS,
  AppStream, and custom or offline repositories.
- Install, enable, and securely access the Cockpit web console for
  day-to-day system administration.
- Validate a freshly installed system's registration, repository, and
  management-console state before handing it off to production use.

## Theory and Architecture

RHEL 10 is delivered as a modular, content-set-based distribution built
from CentOS Stream. Understanding how the installer, the subscription
service, and the package repositories relate to one another is
foundational to every other chapter in this volume, because almost
every later task — installing a service, applying a security update,
enabling a kernel module — ultimately depends on a correctly configured
package source.

### Installation methods

RHEL 10 supports three installation patterns that an enterprise
administrator will encounter, often in combination:

1. **Interactive Anaconda installation.** The graphical or text-mode
   installer (`anaconda`) walks through language, storage, network, and
   software selection, and writes the result to disk directly. This
   remains the standard method for one-off systems, lab builds, and
   initial image creation.
2. **Kickstart-driven automated installation.** Anaconda can consume a
   Kickstart file (`ks.cfg`) that declares every installation decision
   as data, enabling unattended, repeatable builds from PXE, an ISO, or
   a virtual machine's boot configuration. Kickstart is the backbone of
   fleet provisioning and is directly analogous to the declarative
   infrastructure-as-code approach used elsewhere in this encyclopedia.
3. **Image-based provisioning with Image Builder.** `osbuild-composer`
   and the `composer-cli` / Image Builder web console build a
   ready-to-boot image (QCOW2, AMI, VMDK, raw disk, or an OSTree/`bootc`
   container image) from a declarative blueprint, rather than running
   an installer at boot time. This is the preferred model for cloud and
   virtualization platforms where a golden image is deployed many times.

All three converge on the same underlying package set: **BaseOS** and
**AppStream**, the two repositories that make up a standard RHEL
installation tree.

### Subscription architecture

Red Hat entitles systems to content and support through **Red Hat
Subscription Management (RHSM)**, exposed to the administrator through
the `subscription-manager` command. Two enrollment models exist:

- **Traditional entitlement-based registration**, where a system
  consumes a specific subscription (a "pool") with a fixed quantity of
  entitlements, tracked by the Customer Portal or a Red Hat Satellite
  server.
- **Simple Content Access (SCA)**, the default for most modern Red Hat
  accounts, where any registered system under the account can consume
  any content the account is entitled to, without attaching to an
  individual pool. Registration still occurs through
  `subscription-manager register`, but the `attach`/`subscribe` step is
  no longer required.

Registration accomplishes three things: it authorizes the system to
pull content from Red Hat's Content Delivery Network (CDN) or a local
Satellite/Capsule server, it enrolls the host for support-case
eligibility, and — when paired with `insights-client` — it feeds
telemetry into Red Hat Insights for proactive vulnerability, compliance,
and configuration-drift analysis.

### Repository and content architecture

Once registered, `subscription-manager` writes repository definitions
consumed by `dnf`, RHEL's package manager (a DNF5-based successor to
`yum`/DNF4, using the same repository format). The two repositories
every RHEL 10 install depends on are:

| Repository | Content | Typical use |
| --- | --- | --- |
| BaseOS | Core OS packages: kernel, glibc, systemd, core utilities | Always enabled; required for a bootable, supported system |
| AppStream | Application-layer packages, including modules (multiple versions of a component, such as different database or language runtimes) | Enabled per-need; provides module streams |
| CodeReady Linux Builder (CRB) | Development headers and libraries not covered by the standard support SLA | Enabled for build environments and some EPEL dependencies |

AppStream introduces the **module** concept: a single package name (for
example `postgresql`) can offer multiple parallel-installable
**streams** (major versions), letting an administrator pin a specific
version lifecycle independent of the base OS release cadence.

### Cockpit architecture

Cockpit is a browser-based system administration console that runs as a
systemd-activated service (`cockpit.socket`) rather than a persistent
daemon, so it consumes no resources until a session connects. It
authenticates through PAM using the host's existing accounts (including
sudo/polkit-mediated privilege escalation inside the browser session),
and it is built from independently installable modules —
`cockpit-storaged` for storage, `cockpit-podman` for containers,
`cockpit-networkmanager` for networking, and others — so the installed
footprint matches the roles a given host actually performs. Because
Cockpit calls the same underlying tools (`systemd`, `NetworkManager`,
`storaged`, `podman`) that the command line uses, actions taken in the
browser and actions taken over SSH stay consistent with each other —
Cockpit is a view onto the same system state, not a separate management
plane.

## Design Considerations

- **Installer choice at scale.** Interactive Anaconda does not scale
  past a handful of systems. Any environment provisioning more than a
  few RHEL hosts should standardize on Kickstart (for PXE/bare-metal
  fleets) or Image Builder blueprints (for virtualization and cloud),
  and treat the Kickstart file or blueprint as version-controlled
  source, consistent with this encyclopedia's infrastructure-as-code
  principles from [Volume IX](../../volume-09-infrastructure-automation/README.md).
- **Minimal install vs. Server with GUI.** Production servers should
  default to a minimal package set (`@core` group) and add packages
  deliberately; every additional package is additional patch surface
  and additional Red Hat Insights findings to triage. Reserve
  Server with GUI for workstation-adjacent or vendor-appliance-style
  roles.
- **Registration model and connectivity.** Disconnected or
  air-gapped environments cannot reach the public CDN and must use Red
  Hat Satellite/Capsule, or manually synced offline repositories. Decide
  the connectivity model before writing Kickstart or Image Builder
  automation, because the `%post` registration steps differ materially
  (activation key against Satellite vs. against the public CDN vs. no
  registration at all for an offline repo).
- **Module stream selection.** Because module streams are chosen once
  and are difficult to change without removing and reinstalling the
  module, design which stream a fleet standardizes on (for example,
  `postgresql:16`) as a deliberate architectural decision, not a
  per-host improvisation.
- **Cockpit exposure.** Cockpit listens on TCP/9090 with TLS by
  default. Decide whether it is reachable from a general management
  VLAN, restricted to a bastion/jump host, or disabled entirely in
  favor of SSH and Ansible for hosts that do not need a GUI.
- **Activation keys over embedded credentials.** Kickstart and image
  blueprints are frequently stored in source control or baked into
  images; embedding a username and password for registration in those
  artifacts is a credential-leak risk. Activation keys scoped to a
  specific set of repositories and an expiry policy are the safer
  automation primitive.

## Implementation and Automation

### 1. Registering a system with subscription-manager

```bash
# Register using an activation key (preferred for automation)
subscription-manager register \
  --org="1234567" \
  --activationkey="rhel-10-baseos-appstream"

# Interactive registration (username/password), for manual builds only
subscription-manager register --username <RHN_USER>

# Confirm registration and entitlement status
subscription-manager status
subscription-manager identity
```

Simple Content Access accounts do not require an `attach` step; the
repositories become available immediately after `register` succeeds.
Legacy entitlement accounts still require:

```bash
subscription-manager attach --auto
```

### 2. Enrolling in Red Hat Insights

```bash
dnf install -y insights-client
insights-client --register
insights-client --status
```

### 3. Managing repositories with dnf

```bash
# List enabled repositories and their package counts
dnf repolist

# List every known repository, enabled or not
dnf repolist --all

# Enable the CodeReady Linux Builder repository
subscription-manager repos --enable codeready-builder-for-rhel-10-$(arch)-rpms

# Disable a repository without removing its definition
dnf config-manager --set-disabled epel

# Add a third-party or internal repository
dnf config-manager --add-repo https://internal.example.com/repo/custom.repo
```

Module streams are managed with `dnf module`:

```bash
dnf module list postgresql
dnf module enable postgresql:16
dnf install -y postgresql-server
```

### 4. Kickstart repository and registration snippet

A representative fragment from a Kickstart file automating both
registration and repository setup:

```text
# ks.cfg excerpt
%packages
@core
chrony
cockpit
%end

%post --log=/root/ks-post.log
subscription-manager register \
  --org="1234567" \
  --activationkey="rhel-10-baseos-appstream"
subscription-manager repos --enable codeready-builder-for-rhel-10-x86_64-rpms
systemctl enable --now cockpit.socket
%end
```

### 5. Building an image with Image Builder

```bash
dnf install -y osbuild-composer composer-cli
systemctl enable --now osbuild-composer.socket

# Create a minimal blueprint
cat > webserver.toml <<'EOF'
name = "webserver"
description = "Minimal hardened web server image"
version = "0.0.1"

[[packages]]
name = "httpd"
version = "*"

[[packages]]
name = "cockpit"
version = "*"
EOF

composer-cli blueprints push webserver.toml
composer-cli compose start webserver qcow2
composer-cli compose list
```

### 6. Installing and enabling Cockpit

```bash
dnf install -y cockpit cockpit-storaged cockpit-podman
systemctl enable --now cockpit.socket
firewall-cmd --add-service=cockpit --permanent
firewall-cmd --reload
```

Cockpit is now reachable at `https://<hostname-or-ip>:9090` and accepts
the same local or directory-service credentials as SSH.

## Validation and Troubleshooting

- **Confirm registration.** `subscription-manager status` should
  report `Overall Status: Current`. A `Status: Unknown` or `Invalid`
  result usually means the activation key does not match the
  organization ID, or the system clock is skewed enough to fail
  certificate validation — check `chronyc tracking` first.
- **Confirm repository availability.** `dnf repolist` must show
  `rhel-10-for-x86_64-baseos-rpms` and `rhel-10-for-x86_64-appstream-rpms`
  (naming varies slightly by architecture) with a nonzero package
  count. If repositories are missing entirely, re-run
  `subscription-manager refresh` and check
  `/etc/yum.repos.d/redhat.repo` was generated.
- **Diagnose dnf transaction failures.** `dnf history list` shows
  recent transactions; `dnf history info <id>` shows exactly what a
  given transaction changed, which is the fastest way to confirm what
  a failed or partial update actually did before deciding whether to
  `dnf history undo <id>`.
- **Diagnose installer failures.** Anaconda logs to
  `/tmp/anaconda.log`, `/tmp/program.log`, and `/tmp/storage.log`
  during installation, and copies them to `/var/log/anaconda/` on the
  installed system — always check `/var/log/anaconda/ks-script*.log`
  first when a Kickstart `%post` script silently fails.
- **Verify Cockpit is listening and reachable.**

  ```bash
  systemctl status cockpit.socket
  ss -tlnp | grep 9090
  curl -Ik https://localhost:9090
  ```

  A connection refused error typically means `cockpit.socket` is not
  enabled; a TLS handshake failure from a remote client usually means
  the firewall rule for the `cockpit` service was never added.
- **Common failure: module stream conflicts.** Installing a package
  from an unintended stream (`dnf install postgresql` without first
  enabling a stream) silently defaults to the module's default stream,
  which may not match fleet standards. Always run `dnf module list
  <name>` and explicitly `dnf module enable <name>:<stream>` before
  installing.

## Security and Best Practices

- Use activation keys, not stored username/password pairs, for every
  automated registration path (Kickstart, Image Builder, configuration
  management).
- Scope activation keys narrowly — one key per fleet role — so a leaked
  key exposes the minimum useful repository set, and rotate/revoke keys
  through the Customer Portal or Satellite when a build pipeline is
  retired.
- Enroll every registered system in Red Hat Insights; it is the fastest
  path to fleet-wide visibility into known CVEs, misconfigurations, and
  compliance drift without deploying a separate agent.
- Keep Cockpit behind TLS (the default, self-signed unless you supply
  an organizational certificate) and replace the self-signed
  certificate with one issued by an internal CA before exposing it
  beyond a lab network.
- Restrict Cockpit's firewall exposure to management-network sources
  using a firewalld rich rule or a dedicated zone, rather than opening
  TCP/9090 to every network the host is attached to.
- Install only the Cockpit modules a host's role requires;
  `cockpit-machines` or `cockpit-podman` on a host that runs neither
  libvirt nor containers is unnecessary attack surface.
- Treat Kickstart files and Image Builder blueprints as source-of-truth
  artifacts in version control, reviewed like any other infrastructure
  code, since they define the security posture of every system built
  from them.

## References and Knowledge Checks

**References**

- [Red Hat Enterprise Linux 10 Installation Guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10) — Anaconda and
  Kickstart reference, Red Hat Customer Portal.
- [Red Hat Subscription Management documentation](https://access.redhat.com/products/red-hat-subscription-management) — registration, Simple
  Content Access, and activation keys.
- [Image Builder / `osbuild-composer` documentation](https://osbuild.org/docs/on-premises/overview/) — blueprint syntax
  and supported output image types.
- [Cockpit Project documentation](https://cockpit-project.org/documentation) — module list and PAM integration.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — this
  chapter's RHEL 10 baseline.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  RHCSA (EX200) blueprint mapping for this volume.

**Knowledge checks**

1. What is the practical difference between traditional entitlement
   registration and Simple Content Access, and which `subscription-manager`
   step does SCA remove?
2. Why are BaseOS and AppStream split into two repositories instead of
   one, and what does a module stream add on top of AppStream?
3. Why should Kickstart automation prefer an activation key over an
   embedded username and password?
4. Which systemd unit makes Cockpit resource-idle until a browser
   session connects, and how do you confirm it is both enabled and
   listening?

## Hands-On Lab

**Objective:** Configure repository access from a local installation
source (no live subscription required), install and secure Cockpit, and
verify both from the command line and a browser.

**Prerequisites**

- A RHEL 10 virtual machine or bare-metal lab host with root or sudo
  access, and the RHEL 10 installation ISO available locally or over
  HTTP.
- Network access to the host's management interface from your
  workstation browser.

**Steps**

1. Mount the installation ISO and inspect its content sets:

   ```bash
   sudo mkdir -p /mnt/rhel10-iso
   sudo mount -o loop /path/to/rhel-10.0-x86_64-dvd.iso /mnt/rhel10-iso
   ls /mnt/rhel10-iso/BaseOS/Packages | head
   ls /mnt/rhel10-iso/AppStream/Packages | head
   ```

2. Define local repositories pointing at the mounted media, disabling
   any conflicting subscription-based repos for this lab:

   ```bash
   sudo tee /etc/yum.repos.d/rhel10-local.repo <<'EOF'
   [rhel10-local-baseos]
   name=RHEL 10 Local BaseOS
   baseurl=file:///mnt/rhel10-iso/BaseOS
   enabled=1
   gpgcheck=1
   gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release

   [rhel10-local-appstream]
   name=RHEL 10 Local AppStream
   baseurl=file:///mnt/rhel10-iso/AppStream
   enabled=1
   gpgcheck=1
   gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
   EOF
   ```

3. Verify the new repositories resolve correctly:

   ```bash
   dnf repolist
   dnf clean all && dnf makecache
   ```

   **Expected result:** both `rhel10-local-baseos` and
   `rhel10-local-appstream` appear with a nonzero package count.

4. Install and enable Cockpit and a storage module from the local
   repository:

   ```bash
   sudo dnf install -y cockpit cockpit-storaged
   sudo systemctl enable --now cockpit.socket
   ```

5. Open the firewall for Cockpit and confirm the port is listening:

   ```bash
   sudo firewall-cmd --add-service=cockpit --permanent
   sudo firewall-cmd --reload
   ss -tlnp | grep 9090
   ```

6. **Expected result:** From your workstation browser, navigate to
   `https://<lab-host-ip>:9090`, accept the self-signed certificate
   warning for this lab environment, and log in with a local account.
   The Overview page must show the host's hostname, uptime, and
   resource graphs.

7. **Negative test:** Stop the Cockpit socket and confirm the console
   becomes unreachable, proving the firewall rule alone is not what
   provides the service:

   ```bash
   sudo systemctl stop cockpit.socket
   curl -Ik --max-time 5 https://localhost:9090 || echo "Connection failed as expected"
   ```

   **Expected result:** the `curl` command fails to connect (connection
   refused or timeout), confirming Cockpit's socket activation — not
   just the open firewall port — is required for access.

8. **Cleanup:**

   ```bash
   sudo systemctl enable --now cockpit.socket   # restore service if keeping the lab host
   sudo firewall-cmd --remove-service=cockpit --permanent
   sudo firewall-cmd --reload
   sudo rm -f /etc/yum.repos.d/rhel10-local.repo
   sudo umount /mnt/rhel10-iso
   sudo rmdir /mnt/rhel10-iso
   dnf clean all
   ```

## Summary and Completion Checklist

RHEL 10 systems are provisioned through Anaconda, Kickstart, or Image
Builder, and every one of those paths depends on the same underlying
BaseOS/AppStream content, made reachable either through Red Hat
Subscription Management or a local/offline repository. Cockpit layers a
browser-based console on top of the same systemd, NetworkManager, and
storage tooling used from the command line, activated on demand through
`cockpit.socket`. Registration automation should rely on scoped
activation keys, and Cockpit exposure should be deliberately firewalled
and TLS-protected.

- [ ] Can explain the difference between Anaconda, Kickstart, and Image
      Builder provisioning, and when to use each.
- [ ] Can register a system with `subscription-manager` using an
      activation key and confirm status.
- [ ] Can manage `dnf` repositories, including module streams and local
      /offline repository definitions.
- [ ] Can install, enable, firewall, and verify the Cockpit web console.
- [ ] Completed the hands-on lab, including the negative test and
      cleanup.
