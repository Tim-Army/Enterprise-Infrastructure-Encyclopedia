# Chapter 01: Installation, Autoinstall, Ubuntu Pro, Repositories, and Landscape

## Learning Objectives

- Explain Ubuntu Server's LTS release model, support timeline, and how
  Ubuntu Pro extends it.
- Install Ubuntu Server 26.04 LTS interactively with the Subiquity
  installer and unattended with autoinstall.
- Attach a host to Ubuntu Pro and enable Expanded Security Maintenance
  (ESM), Livepatch, and USG hardening profiles.
- Describe the APT repository model, including component pockets, the
  deb822 `.sources` format, and PPAs.
- Register a host with Landscape and perform a basic fleet operation.

## Theory and Architecture

Ubuntu Server 26.04 LTS ("Numbat," following Canonical's alliterative
release-naming convention) is a Long Term Support release: five years of
free standard maintenance from Canonical, extendable to ten years (and
optionally twelve for a small set of legacy packages) through an Ubuntu
Pro subscription. Canonical ships an LTS every two years in April
(`YY.04`) and a non-LTS interim release every six months; production
infrastructure should standardize on LTS releases, since interim
releases receive only nine months of support and are not a supported
upgrade path directly into another interim release.

### The Subiquity installer and installation media

Ubuntu Server uses the **Subiquity** installer, a Python/Curtin-based
system that replaced the older Debian-installer-derived text installer
starting with 20.04. Subiquity drives two installation experiences from
the same codebase:

- **Interactive installation** from the live-server ISO, where an
  administrator answers a sequence of screens (network, proxy, mirror,
  storage, profile, SSH, snaps).
- **Autoinstall**, where the identical set of questions is answered in
  advance by a YAML document, producing a fully unattended, scriptable
  installation suitable for PXE boot, ISO remastering, or cloud image
  customization.

Both paths use **Curtin** to partition disks and lay down the target
filesystem, and both finish by running `cloud-init` on first boot to
apply the boot-time configuration (hostname, users, SSH keys, packages)
that autoinstall or the interactive installer collected.

### Autoinstall as a cloud-init subset

Autoinstall is deliberately built as an extension of cloud-init: an
autoinstall document is a cloud-init user-data file containing an
`autoinstall:` top-level key. This is a significant architectural
choice — the same YAML dialect an administrator uses to seed a cloud
instance is (mostly) the same dialect used to unattended-install bare
metal, which is why [Chapter 09](09-cloud-init-maas-juju-ansible-landscape-operations-and-capstone.md) revisits cloud-init in depth rather than
treating it as a separate topic.

### Ubuntu Pro and Expanded Security Maintenance

Ubuntu Pro is Canonical's subscription layer on top of the free Ubuntu
base. Free for personal use on up to five machines and included at no
extra cost on most public cloud marketplace images, it unlocks:

| Capability | What it provides |
| --- | --- |
| ESM-Infra | Security patches for `main`/`restricted` packages beyond standard LTS support |
| ESM-Apps | Security patches for `universe`/`multiverse` packages (a much larger surface than `main` alone) |
| Livepatch | Kernel security patches applied without a reboot |
| USG (Ubuntu Security Guide) | Automated CIS and DISA-STIG hardening and compliance auditing |
| FIPS-validated crypto modules | Certified cryptographic modules for regulated workloads |
| Extended 10-year (12-year Legacy add-on) support | Security maintenance beyond the standard 5-year LTS window |

The `pro` client (package `ubuntu-advantage-tools`, upstream project
`ubuntu-pro-client`) manages attachment, service enablement, and status
reporting from the command line.

### The APT repository model

Ubuntu partitions its archive into four **components**, each with a
different support and licensing posture:

| Component | Support | License posture |
| --- | --- | --- |
| `main` | Canonical-supported, standard LTS window | Free/open source |
| `restricted` | Canonical-supported | Proprietary drivers/firmware |
| `universe` | Community-maintained (ESM-Apps under Pro) | Free/open source |
| `multiverse` | Community-maintained, not security-tracked by default | Restricted licensing |

Each component is further split into **pockets**: `release` (what
shipped), `updates` (stable post-release fixes), `security` (expedited
CVE fixes), and `backports` (newer upstream versions, opt-in, not
guaranteed regression-tested to the same bar). Ubuntu 24.04 and later
default to the **deb822** source format (`/etc/apt/sources.list.d/
ubuntu.sources`) instead of the legacy one-line-per-entry
`sources.list` syntax; both formats are still parsed by APT, but deb822
is now the generated default and supports multiple suites/components
per stanza more cleanly.

### Landscape

**Landscape** is Canonical's systems management platform for Ubuntu
fleets: inventory, patch management, compliance reporting, and
event-driven remediation across hundreds to thousands of hosts.
Landscape ships as Landscape SaaS (Canonical-hosted) or
Landscape Server (self-hosted, itself deployable via Juju — see Chapter
09). Each managed host runs `landscape-client`, a lightweight agent that
reports inventory and package state and executes administrator-approved
actions (package installs, script execution, reboots).

## Design Considerations

- **LTS vs. interim release selection.** Production and long-lived
  infrastructure should always target an LTS release; reserve interim
  releases for short-lived evaluation environments, since they exit
  support in nine months and cannot be upgraded directly to the next
  interim release.
- **Autoinstall vs. golden image.** Autoinstall is well suited to
  environments that provision physical or virtual machines from bare
  media (PXE, remastered ISO, MAAS — [Chapter 09](09-cloud-init-maas-juju-ansible-landscape-operations-and-capstone.md)) where install-time
  customization matters. Environments that provision from a
  pre-built cloud image (most public and private cloud deployments)
  typically skip autoinstall entirely and drive first boot with
  cloud-init user-data alone.
- **Ubuntu Pro attachment strategy.** Decide whether Pro is attached at
  image build time (baked into a golden image, requiring careful token
  handling) or at first boot via cloud-init/Landscape (better secret
  hygiene, but requires network reachability to `contracts.canonical.com`
  or a Pro-compatible proxy at boot time).
- **Universe/multiverse exposure.** A host that installs packages from
  `universe` without ESM-Apps enabled is running software Canonical does
  not security-patch on a defined SLA; treat `apt-cache policy` output
  as a genuine risk inventory question, not just a version check.
- **Backports discipline.** `-backports` is disabled by default for a
  reason — enable it per package with APT pinning rather than globally,
  so a single newer package doesn't silently pull in an entire tree of
  less-tested dependencies.
- **Landscape SaaS vs. self-hosted.** Landscape SaaS removes operational
  burden but sends fleet metadata to a Canonical-operated service;
  regulated or air-gapped environments typically self-host Landscape
  Server, which itself needs the same patch and backup discipline as any
  other production service.

## Implementation and Automation

### 1. Interactive installation reference points

The live-server ISO boots into Subiquity's TUI. Key screens an
administrator should not accept blindly in a production build: network
configuration (set a static address or confirm the DHCP reservation
matches inventory), proxy (mandatory in restricted networks), mirror
selection (point at an internal mirror if one exists), storage layout
(LVM by default — accept it unless a specific partitioning scheme is
required), and the SSH screen (import a GitHub/Launchpad key or paste a
public key; never finish an unattended-adjacent build with password
authentication only).

### 2. A minimal autoinstall document

```yaml
#cloud-config
autoinstall:
  version: 1
  locale: en_US.UTF-8
  keyboard:
    layout: us
  network:
    version: 2
    ethernets:
      ens160:
        dhcp4: true
  identity:
    hostname: ubuntu-srv01
    username: opsadmin
    # Generate with: mkpasswd --method=sha-512
    password: "$6$rounds=10000$exampleSaltValue$hashedPasswordExampleOnly"
  ssh:
    install-server: true
    allow-pw: false
    authorized-keys:
      - ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... opsadmin@bastion
  storage:
    layout:
      name: lvm
  packages:
    - chrony
    - ufw
    - unattended-upgrades
  updates: security
  late-commands:
    - curtin in-target --target=/target -- systemctl enable ssh
```

Serve this as `user-data` (with an empty `meta-data` file) over an
attached ISO, a local HTTP server, or PXE, and boot the live-server ISO
with `autoinstall ds=nocloud-net;s=http://<host>/` on the kernel
command line. Subiquity validates the document against its JSON schema
before proceeding and will halt with a schema error rather than guess
at intent — treat that validation as a feature, not friction.

### 3. Attaching Ubuntu Pro

```bash
# Attach using a contract token from ubuntu.com/pro
sudo pro attach C1234567890abcdef1234567890abcd

# Confirm status and enabled services
pro status --all

# Enable specific services
sudo pro enable esm-infra esm-apps livepatch usg

# Non-interactive attach for automation (cloud-init, Ansible)
sudo pro attach --format json C1234567890abcdef1234567890abcd
```

`pro status` after a successful attach shows `esm-infra` and `esm-apps`
as `enabled`, and `apt update` output gains explicit `-security` and
`-infra-security`/`-apps-security` pocket lines confirming the extra
repositories are now in play.

### 4. Repository management

```bash
# Inspect the deb822 default sources file (24.04+)
cat /etc/apt/sources.list.d/ubuntu.sources

# Show what APT actually knows about a package and from which pocket
apt-cache policy nginx

# Add a PPA (Personal Package Archive) — third-party, not Canonical-supported
sudo add-apt-repository ppa:example/ppa
sudo apt update

# Pin a package to prefer a specific release/pocket
cat <<'EOF' | sudo tee /etc/apt/preferences.d/99-pin-backports
Package: *
Pin: release a=noble-backports
Pin-Priority: 100
EOF

# Point at an internal mirror instead of the public archive
sudo sed -i 's|http://archive.ubuntu.com/ubuntu|http://mirror.internal.example.com/ubuntu|' \
  /etc/apt/sources.list.d/ubuntu.sources
```

### 5. Registering a host with Landscape

```bash
# Install the client
sudo apt install -y landscape-client

# Register non-interactively against Landscape SaaS
sudo landscape-config \
  --account-name my-organization \
  --registration-key "REDACTED-REG-KEY" \
  --computer-title "ubuntu-srv01" \
  --silent

# Confirm the client is running and check its last exchange
sudo systemctl status landscape-client
sudo landscape-config --is-registered
```

## Validation and Troubleshooting

- **Autoinstall document fails schema validation.** Subiquity prints
  the offending key and constraint immediately; validate locally first
  with `sudo snap install subiquity --classic` and
  `subiquity-schema-validate user-data` (or Canonical's published JSON
  schema) before burning an ISO or PXE cycle.
- **Autoinstall completes but first boot has no cloud-init changes
  applied.** Check `cloud-init status --long` and
  `/var/log/cloud-init.log`; a common cause is a `user-data` datasource
  that was reachable during install but not on first boot (a NoCloud
  ISO that was ejected, or a network profile that changed).
- **`pro attach` fails to reach the contract service.** Confirm outbound
  HTTPS reachability to `contracts.canonical.com` and
  `esm.ubuntu.com`; in a proxied environment, set
  `sudo pro config set http_proxy=... https_proxy=...` before
  attaching.
- **A package installs from `universe` without ESM-Apps.** Run
  `apt-cache policy <package>` and confirm the origin; `pro status`
  will show `esm-apps` as disabled if the subscription was never
  enabled for that service, which is a compliance gap worth alerting
  on.
- **Landscape client registers but never appears in the console.**
  Check `/var/log/landscape/landscape-client.log` for exchange errors,
  and confirm the registration key matches the target account; a stale
  `/etc/landscape/client.conf` from a cloned image is a frequent root
  cause — regenerate the client's identity with
  `sudo landscape-config --silent --force` on cloned hosts.

## Security and Best Practices

- Always disable password SSH authentication (`allow-pw: false` in
  autoinstall, or `PasswordAuthentication no` in `sshd_config` — see
  [Chapter 04](04-identity-privilege-ssh-netplan-and-firewalling.md)) on any host provisioned unattended.
- Treat Ubuntu Pro contract tokens as secrets: inject them via a secret
  manager or cloud-init's `write_files`/vendor-data mechanism with
  restrictive permissions, never bake them into a public golden image
  or commit them to version control.
- Enable `esm-infra` and `esm-apps` on every production host running
  packages outside `main`/`restricted`; a host silently running
  unpatched `universe` packages is a common and avoidable audit finding.
- Restrict `-backports` and PPAs to hosts and packages that specifically
  need them, pinned explicitly, rather than enabling them fleet-wide.
- Prefer an internal APT mirror or caching proxy (`apt-cacher-ng`,
  Landscape's built-in package mirroring) for any fleet larger than a
  handful of hosts, both for bandwidth and for consistent, auditable
  package provenance.
- Enroll production fleets in Landscape (or an equivalent CMDB/patch
  tool) from first boot via cloud-init, not as an afterthought —
  unmanaged hosts are the ones that drift out of patch compliance.

## References and Knowledge Checks

**References**

- [Ubuntu Server Guide](https://ubuntu.com/server/docs/) — Installation, Canonical documentation.
- [Subiquity and autoinstall reference, Canonical `ubuntu/subiquity`
  project documentation.](https://canonical-subiquity.readthedocs-hosted.com/en/latest/)
- [Ubuntu Pro documentation](https://documentation.ubuntu.com/pro/) — `ubuntu.com/pro` and `pro status`/`pro
  help` command output.
- [Debian/Ubuntu Repository Format ("deb822") specification.](https://repolib.readthedocs.io/en/latest/deb822-format.html)
- [Landscape documentation](https://documentation.ubuntu.com/landscape/) — `ubuntu.com/landscape`.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — Ubuntu Server
  26.04 LTS baseline referenced throughout this volume.

**Knowledge checks**

1. Why is autoinstall described as "a cloud-init subset" rather than a
   wholly separate installer language?
2. What is the practical difference in support posture between packages
   in `main` and packages in `universe`, and how does Ubuntu Pro change
   that for `universe`?
3. Why does Subiquity validate an autoinstall document against a JSON
   schema before proceeding, and what should an administrator do when
   that validation fails?
4. What risk does enabling `-backports` fleet-wide (rather than pinned
   per package) introduce?

## Hands-On Lab

**Objective:** Build and validate an autoinstall user-data document,
attach Ubuntu Pro, and confirm repository and ESM state — using a
disposable VM so the exercise is safe to repeat.

**Prerequisites**

- A hypervisor capable of booting from ISO with virtual CD-ROM/NoCloud
  seed support (KVM/QEMU, VirtualBox, or a cloud provider's custom-ISO
  path). `virt-install` examples below assume KVM/libvirt.
- The Ubuntu Server 26.04 LTS live-server ISO downloaded locally.
- (Optional) A free Ubuntu Pro token from `ubuntu.com/pro` for the
  ESM-attach steps — the lab notes how to skip this safely if unavailable.

**Steps**

1. Create the autoinstall seed files:

   ```bash
   mkdir -p ~/lab-autoinstall/seed && cd ~/lab-autoinstall
   cat > seed/meta-data <<'EOF'
   EOF
   cat > seed/user-data <<'EOF'
   #cloud-config
   autoinstall:
     version: 1
     locale: en_US.UTF-8
     keyboard:
       layout: us
     network:
       version: 2
       ethernets:
         enp1s0:
           dhcp4: true
     identity:
       hostname: lab-ubuntu01
       username: labadmin
       password: "$6$rounds=10000$labsaltvalue$examplehashdonotusefake"
     ssh:
       install-server: true
       allow-pw: true
     storage:
       layout:
         name: lvm
     packages:
       - chrony
     updates: security
   EOF
   ```

2. Build a NoCloud seed ISO from the two files:

   ```bash
   sudo apt install -y cloud-image-utils
   cloud-localds seed.iso seed/user-data seed/meta-data
   ```

3. Launch the installation as a VM, attaching both the installer ISO
   and the seed ISO:

   ```bash
   virt-install \
     --name lab-ubuntu01 \
     --memory 4096 --vcpus 2 \
     --disk size=20 \
     --cdrom ubuntu-26.04-live-server-amd64.iso \
     --disk seed.iso,device=cdrom \
     --os-variant ubuntu24.04 \
     --graphics none --console pty,target_type=serial \
     --extra-args 'autoinstall ds=nocloud;'
   ```

   **Expected result:** the installer boots, reads the seed
   automatically, and completes unattended in a few minutes, ending
   with the VM rebooting into the installed system.

4. Log in (console or SSH, per your seed) and confirm cloud-init
   finished successfully:

   ```bash
   cloud-init status --long
   ```

   **Expected result:** `status: done` with no errors listed.

5. Inspect the default repository configuration:

   ```bash
   cat /etc/apt/sources.list.d/ubuntu.sources
   apt-cache policy chrony
   ```

   **Expected result:** entries for `noble` (or the shipping LTS series)
   `release`, `updates`, `security`, and `backports` pockets across
   `main`, `restricted`, `universe`, and `multiverse`.

6. If you have a Pro token, attach it and enable ESM:

   ```bash
   sudo pro attach <YOUR_TOKEN>
   pro status --all
   ```

   **Expected result:** `esm-infra` and `esm-apps` show `enabled`. If
   you do not have a token, skip this step — the rest of the lab does
   not depend on it.

7. **Negative test:** attempt to attach with an invalid token and
   observe the failure mode:

   ```bash
   sudo pro attach invalid-token-000000
   ```

   **Expected result:** `pro` reports an invalid-token error and makes
   no changes to the system's repository configuration — confirming
   that a failed attach does not silently leave the host in a
   partially-configured state.

8. **Cleanup:**

   ```bash
   virsh destroy lab-ubuntu01 2>/dev/null || true
   virsh undefine lab-ubuntu01 --remove-all-storage
   rm -rf ~/lab-autoinstall
   ```

## Summary and Completion Checklist

Ubuntu Server 26.04 LTS installs either interactively through Subiquity
or unattended through autoinstall, itself a cloud-init dialect that
ties directly into the first-boot configuration covered in depth in
[Chapter 09](09-cloud-init-maas-juju-ansible-landscape-operations-and-capstone.md). Ubuntu Pro extends the free five-year LTS support window
with ESM coverage for both `main` and `universe`, Livepatch, and
automated hardening through USG. The APT archive's component/pocket
model determines which packages are Canonical-supported and on what
timeline, and Landscape provides fleet-scale visibility and control
across all of it.

- [ ] Can distinguish LTS from interim release support timelines and
      justify an LTS-only production standard.
- [ ] Can write and validate an autoinstall user-data document and boot
      it unattended.
- [ ] Can attach a host to Ubuntu Pro and enable ESM-Infra/ESM-Apps.
- [ ] Can explain the `main`/`restricted`/`universe`/`multiverse`
      component model and the `release`/`updates`/`security`/
      `backports` pocket model.
- [ ] Can register a host with Landscape and confirm successful
      check-in.
- [ ] Completed the hands-on lab, including the negative test and
      cleanup.
