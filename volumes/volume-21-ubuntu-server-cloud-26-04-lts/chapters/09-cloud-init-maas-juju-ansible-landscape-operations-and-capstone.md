# Chapter 09: Cloud-init, MAAS, Juju, Ansible, Landscape, Operations, and Capstone

## Learning Objectives

- Explain cloud-init's datasource, module, and stage architecture, and
  diagnose a first-boot configuration failure.
- Describe MAAS's region/rack controller architecture for bare-metal
  provisioning.
- Deploy and relate applications using Juju charms and bundles.
- Manage an Ubuntu fleet with Ansible using distribution-appropriate
  modules.
- Integrate Landscape for ongoing fleet patch and compliance operations.
- Complete a capstone lab combining autoinstall, cloud-init, Ansible,
  and fleet visibility into one coherent workflow.

## Theory and Architecture

This closing chapter ties the volume together: [Chapter 01](01-installation-autoinstall-ubuntu-pro-repositories-and-landscape.md) introduced
autoinstall as a cloud-init subset and Landscape as a registration
target; this chapter returns to both in operational depth and adds the
remaining Canonical automation stack — MAAS for bare metal and Juju for
application modeling — alongside Ansible, the vendor-neutral automation
tool most fleets actually run day to day.

### Cloud-init architecture

**cloud-init** is the industry-standard cross-distribution tool that
initializes a Linux instance's identity, network, storage, and
software state on first boot, driven entirely by data the instance
receives from its environment rather than a human at a console.
Understanding its architecture explains most of the "why didn't my
configuration apply" failures administrators hit:

- **Datasources** — where cloud-init gets its configuration:
  `NoCloud` (a locally attached ISO or HTTP source, used by the
  autoinstall lab in [Chapter 01](01-installation-autoinstall-ubuntu-pro-repositories-and-landscape.md)), `Ec2`/`Azure`/`GCE`/`OpenStack`
  (cloud-provider metadata services), and others. cloud-init probes a
  prioritized list of datasources at boot and uses the first one that
  responds.
- **Configuration inputs** — `user-data` (the primary
  administrator-authored configuration, `#cloud-config` YAML or a
  script), `meta-data` (instance identity supplied by the platform:
  hostname, instance ID), and `vendor-data` (platform- or
  image-builder-supplied configuration, layered underneath user-data).
- **Boot stages** — cloud-init runs across four systemd-integrated
  stages: **Generator** (very early, decides whether cloud-init should
  run at all), **Local** (`cloud-init-local.service`, network not yet
  up, local datasources only), **Network** (`cloud-init.service`,
  network available, most datasources and modules run here), and
  **Final** (`cloud-init-final.service`, runs after most of the system
  is up — package installs, user scripts).

Each `user-data` module (users, packages, write_files, runcmd, and
dozens more) is independently idempotent by design, and cloud-init
records what it has already done so a re-run (`cloud-init clean` +
reboot) reproduces the same end state — the same idempotency principle
[Chapter 02](02-essential-tools-shell-scripting-apt-and-snap-management.md)'s scripting guidance emphasizes, here enforced by the tool
itself.

### MAAS: Metal as a Service

**MAAS** turns physical servers into cloud-like, API-provisionable
resources. Its architecture separates two roles:

- **Region controller** — the API, database, and web UI; the
  source of truth for machine inventory and configuration.
- **Rack controller** — runs closer to the actual hardware on each L2
  segment, providing DHCP, PXE/TFTP boot services, and image caching
  for the commissioning and deployment process.

A machine's MAAS lifecycle moves through defined states:
**Enlistment** (MAAS discovers a new machine via PXE boot),
**Commissioning** (MAAS boots an ephemeral image to inventory the
hardware — CPU, RAM, disks, NICs), **Allocation** (a user or automation
claims the machine for a purpose), and **Deployment** (MAAS installs
the target OS — typically driving the exact autoinstall/cloud-init flow
from [Chapter 01](01-installation-autoinstall-ubuntu-pro-repositories-and-landscape.md) — and hands the running machine to its owner). MAAS is
what makes autoinstall practical at fleet scale: instead of hand-
building a seed ISO per host, MAAS serves the right `user-data` to the
right machine automatically as part of its normal PXE-boot-and-deploy
flow.

### Juju: application modeling

**Juju** models applications and their relationships as first-class,
declarative objects rather than a sequence of imperative configuration
steps. Its core concepts:

- **Charms** — reusable, versioned operator code for deploying and
  operating a specific application (PostgreSQL, Kubernetes, Landscape
  Server itself), packaging not just installation but full lifecycle
  operations (upgrade, backup, scaling) as callable actions.
- **Models** — an isolated workspace (typically mapped to a cloud
  project or a set of machines) that a set of deployed applications
  lives in.
- **Relations** — declared integrations between charms (a web
  application charm related to a database charm automatically
  exchanges connection credentials and configuration, no manual wiring)
  that the charms themselves implement.
- **Bundles** — a YAML document describing a complete set of
  applications and relations, deployed together in one operation — the
  Juju equivalent of a docker-compose file, but for a fleet of
  potentially many machines or containers rather than one host.

### Ansible for Ubuntu fleets

**Ansible** is not Ubuntu-specific, but its Ubuntu-facing module
surface deserves explicit treatment: the `ansible.builtin.apt` module
(not `yum`/`dnf`) is the package-management primitive, `ansible.
builtin.systemd_service` manages units the same way [Chapter 03](03-boot-systemd-processes-logging-and-scheduled-work.md) does
manually, and Ansible's own `gather_facts`/`ansible_facts.
os_family == "Debian"` conditionals let a mixed-OS playbook branch
correctly when it must also support non-Ubuntu hosts. For an
Ubuntu-only fleet, playbooks can assume APT and systemd directly
without the abstraction overhead a genuinely cross-distribution
playbook needs.

### Landscape operations

[Chapter 01](01-installation-autoinstall-ubuntu-pro-repositories-and-landscape.md) covered Landscape registration; in ongoing operations,
Landscape's real value is **fleet-scale patch management and
compliance reporting**: administrators define patch policies (which
package origins auto-update, on what schedule, with what maintenance
window), review a security-relevant-CVE dashboard across every
registered host, and push approved changes (package installs, script
execution) to defined machine groups rather than touching hosts
individually.

## Design Considerations

- **cloud-init vs. Ansible for first-boot configuration.** cloud-init
  owns the instance's very first boot (before it's reliably reachable
  over SSH by anything else); Ansible is the right tool for ongoing
  configuration management and drift correction after that first boot.
  Use cloud-init to get a host to a minimally manageable state (network,
  SSH keys, an Ansible-manageable user) and Ansible for everything
  after.
- **MAAS vs. cloud-provider-native provisioning.** MAAS earns its
  operational overhead specifically for bare-metal or private-cloud
  fleets; a workload already provisioning exclusively through a public
  cloud API generally doesn't need MAAS, since the cloud platform
  already plays MAAS's role.
- **Juju charms vs. Ansible playbooks for application deployment.**
  Juju's relation model is a genuine advantage when deploying
  charmed, Canonical-supported applications with complex inter-service
  wiring (a full OpenStack or Kubernetes-on-MAAS deployment); Ansible
  remains the broader, vendor-neutral choice for applications with no
  charm, or where the team's existing automation investment is already
  in Ansible.
- **Landscape SaaS vs. self-hosted, revisited.** With Juju now in
  scope, self-hosting Landscape Server via a Juju charm becomes a
  realistic option for regulated or air-gapped fleets that couldn't
  use Landscape SaaS at all — factor that into the [Chapter 01](01-installation-autoinstall-ubuntu-pro-repositories-and-landscape.md) decision
  once Juju is available as a deployment mechanism.
- **Automation layering discipline.** A fleet running autoinstall +
  cloud-init + Ansible + Landscape should have a clear, documented
  boundary for what each tool owns; overlapping ownership (cloud-init
  and Ansible both trying to manage the same package's version, for
  example) produces confusing, hard-to-audit drift.

## Implementation and Automation

### 1. Inspecting and debugging cloud-init

```bash
# Overall status and any errors from the last boot
cloud-init status --long

# Full boot-stage timing, useful for both debugging and boot-budget review
cloud-init analyze show

# Which datasource was actually used
cloud-init query -a | grep -i datasource

# Re-run cloud-init's full first-boot sequence against a cloned image
# (never on a live production host — this resets machine identity)
sudo cloud-init clean --logs
sudo cloud-init init
sudo cloud-init modules --mode=config
sudo cloud-init modules --mode=final

# Primary log locations
sudo less /var/log/cloud-init.log
sudo less /var/log/cloud-init-output.log
```

### 2. A representative cloud-config user-data document

```yaml
#cloud-config
hostname: app02
users:
  - name: opsadmin
    groups: sudo
    shell: /bin/bash
    sudo: ALL=(ALL) NOPASSWD:ALL
    ssh_authorized_keys:
      - ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... opsadmin@bastion
package_update: true
package_upgrade: true
packages:
  - chrony
  - ansible
write_files:
  - path: /etc/ansible-managed
    content: |
      This host is managed by Ansible after first boot.
    permissions: '0644'
runcmd:
  - [systemctl, enable, --now, chrony]
```

### 3. MAAS: commissioning and deploying a machine

```bash
# Log in to the MAAS CLI (API key from the MAAS web UI)
maas login admin http://maas.example.com:5240/MAAS <API_KEY>

# List machines and their current state
maas admin machines read | jq '.[] | {hostname, status_name}'

# Commission a newly enlisted machine
maas admin machine commission <system_id>

# Allocate and deploy Ubuntu Server 26.04 LTS to it,
# supplying the same style of cloud-init user-data as Chapter 01
maas admin machines allocate
maas admin machine deploy <system_id> \
  user_data="$(base64 -w0 user-data.yaml)"

# Poll deployment status
maas admin machine read <system_id> | jq '.status_name'
```

### 4. Juju: deploying a related application bundle

```bash
sudo snap install juju --classic

# Bootstrap a controller onto a cloud/substrate (MAAS, LXD, or a public cloud)
juju bootstrap localhost lxd-controller

# Create a model to deploy into
juju add-model production-app

# Deploy applications and relate them
juju deploy postgresql
juju deploy mattermost-k8s mattermost
juju relate mattermost postgresql

# Or deploy an entire pre-defined bundle in one step
juju deploy ./bundle.yaml

# Check status of the deployed model
juju status
```

### 5. Ansible against an Ubuntu fleet

```ini
# inventory.ini
[ubuntu_servers]
app01.lab.example.com
app02.lab.example.com

[ubuntu_servers:vars]
ansible_user=opsadmin
ansible_python_interpreter=/usr/bin/python3
```

```yaml
# site.yml
- name: Baseline configuration for Ubuntu fleet
  hosts: ubuntu_servers
  become: true
  tasks:
    - name: Update apt cache
      ansible.builtin.apt:
        update_cache: true
        cache_valid_time: 3600

    - name: Ensure baseline packages are present
      ansible.builtin.apt:
        name:
          - chrony
          - ufw
          - unattended-upgrades
        state: present

    - name: Ensure chrony is enabled and running
      ansible.builtin.systemd_service:
        name: chrony
        enabled: true
        state: started

    - name: Enforce default-deny inbound firewall policy
      community.general.ufw:
        policy: deny
        direction: incoming
```

```bash
ansible-playbook -i inventory.ini site.yml --check   # dry run first
ansible-playbook -i inventory.ini site.yml
```

### 6. Landscape fleet operations

```bash
# List registered machines and their pending security updates
landscape-api get-computers --query 'alert:security-upgrades'

# Push a package upgrade to a defined machine group, via a scripted activity
landscape-api apply-package-upgrades \
  --query "tag:app-servers" \
  --security-only

# Retrieve the CIS/compliance summary for a computer
landscape-api get-computers --with-annotations --query "hostname:app01*"
```

## Validation and Troubleshooting

- **cloud-init reports `status: done` but expected configuration never
  applied.** Check which datasource was actually used
  (`cloud-init query -a`); a datasource mismatch (the instance found a
  different datasource than the one the administrator seeded) means the
  intended `user-data` was never read at all.
- **A MAAS machine fails commissioning.** The MAAS UI's machine detail
  page and `maas admin machine read <system_id>` expose the
  commissioning script output; a common cause is a NIC or disk the
  commissioning scripts couldn't enumerate due to a firmware/driver gap
  — check the hardware against MAAS's certified hardware list.
- **A Juju relation doesn't establish.** `juju status` shows relation
  state per application, and `juju debug-log` streams the unit agent
  logs live; most relation failures trace back to a charm-specific
  configuration option that must be set before the relation can
  complete, visible in the charm's own documentation.
- **An Ansible playbook run partially fails across a fleet.** Always
  run with `--check` (dry run) before a real run against unfamiliar
  playbooks, and `--limit <host>` to isolate a single failing host;
  `ansible-playbook -vvv` gives full module invocation detail for
  a task that fails only on some hosts.
- **Landscape shows a host as "insecure" long after patching.**
  Confirm the Landscape client actually reported back after the patch
  (`sudo landscape-config --is-registered` and checking the client's
  last exchange time); a client whose scheduled check-in interval is
  longer than the patch-then-verify window will show stale status
  until its next exchange.

## Security and Best Practices

- Never embed long-lived secrets directly in `user-data`; use a secret
  manager reference, a short-lived bootstrap token exchanged for real
  credentials on first boot, or Landscape/Juju's own credential
  handling instead of a plaintext password or API key in cloud-init
  YAML.
- Scope MAAS API keys and Juju controller credentials narrowly per
  automation identity, the same least-privilege principle [Chapter 04](04-identity-privilege-ssh-netplan-and-firewalling.md)
  applies to `sudo`; a MAAS API key with full admin rights embedded in
  a CI pipeline is a significant blast-radius risk if that pipeline is
  compromised.
- Store Ansible inventories, playbooks, and any `vault`-encrypted
  secrets in version control with the same review discipline as
  application code; treat `ansible-vault` (or an external secrets
  backend) as mandatory for any variable holding a credential.
- Run Ansible playbooks with `--check` against production, and require
  a passing dry run in CI before an unattended apply, for any playbook
  capable of a destructive or service-impacting change.
- Use Landscape's patch policies to enforce, not just report, a maximum
  allowable exposure window for critical CVEs across the fleet, and
  alert when a host falls outside that window rather than relying on
  manual dashboard review.
- Treat the entire autoinstall → cloud-init → Ansible → Landscape chain
  as one audited pipeline: know, for any given host, exactly which
  stage last touched a given piece of configuration, so drift has a
  traceable origin.

## References and Knowledge Checks

**References**

- [cloud-init documentation, `cloudinit.readthedocs.io`.](https://cloudinit.readthedocs.io/)
- [MAAS documentation, `maas.io/docs`.](https://maas.io/docs)
- [Juju documentation, `juju.is/docs`.](https://canonical-juju.readthedocs-hosted.com/en/latest/)
- [Ansible documentation](https://docs.ansible.com/) — `ansible.builtin.apt`,
  `ansible.builtin.systemd_service` module references.
- [Landscape documentation and API reference, `ubuntu.com/landscape`.](https://documentation.ubuntu.com/landscape/)
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — Ubuntu Server
  26.04 LTS and Ansible baselines referenced throughout this volume.

**Knowledge checks**

1. What are cloud-init's four boot stages, and why does the
   distinction between the Local and Network stages matter for which
   modules can run at each?
2. What role does a MAAS rack controller play that the region
   controller does not, and why does that split matter for a
   multi-site deployment?
3. What problem does a Juju relation solve that a plain Ansible
   playbook deploying the same two applications would have to handle
   manually?
4. Why should cloud-init and Ansible generally not both try to manage
   the same piece of ongoing configuration on a host?

## Hands-On Lab

**Capstone objective:** Combine this volume's automation stack into one
workflow: boot a host with cloud-init user-data that hands it off in a
minimally configured, Ansible-manageable state, then use an Ansible
playbook to complete baseline configuration and verify the result —
with a negative test proving the dry-run (`--check`) mode catches an
unintended change before it applies.

**Prerequisites**

- A hypervisor able to launch a cloud image with a NoCloud cloud-init
  seed (this lab reuses the `cloud-localds` approach from [Chapter 01](01-installation-autoinstall-ubuntu-pro-repositories-and-landscape.md)).
- An Ubuntu Server 26.04 LTS cloud image (`.img`) rather than the
  installer ISO.
- A control host (can be the same VM host) with `ansible` installed.
- A non-production environment throughout.

**Steps**

1. Prepare a minimal cloud-init seed that creates an Ansible-manageable
   user and nothing else — deliberately leaving baseline hardening to
   Ansible:

   ```bash
   mkdir -p ~/lab-capstone/seed && cd ~/lab-capstone
   ssh-keygen -t ed25519 -C "capstone-lab" -f capstone-key -N ""

   cat > seed/meta-data <<'EOF'
   instance-id: capstone-01
   local-hostname: capstone-01
   EOF

   cat > seed/user-data <<EOF
   #cloud-config
   users:
     - name: ansible
       groups: sudo
       shell: /bin/bash
       sudo: ALL=(ALL) NOPASSWD:ALL
       ssh_authorized_keys:
         - $(cat capstone-key.pub)
   package_update: true
   EOF

   cloud-localds seed.iso seed/user-data seed/meta-data
   ```

2. Launch the cloud image with the seed attached:

   ```bash
   qemu-img create -f qcow2 -F qcow2 -b ubuntu-26.04-server-cloudimg-amd64.img capstone-01.qcow2 10G
   virt-install \
     --name capstone-01 \
     --memory 2048 --vcpus 2 \
     --disk capstone-01.qcow2 \
     --disk seed.iso,device=cdrom \
     --os-variant ubuntu24.04 \
     --import --graphics none --console pty,target_type=serial \
     --noautoconsole
   ```

3. Wait for cloud-init to finish, then confirm minimal-state hand-off:

   ```bash
   CAPSTONE_IP=$(virsh domifaddr capstone-01 | awk '/ipv4/{print $4}' | cut -d/ -f1)
   ssh -i capstone-key -o StrictHostKeyChecking=no ansible@"${CAPSTONE_IP}" \
     'cloud-init status --long; ufw status 2>&1 || echo "ufw not yet configured"'
   ```

   **Expected result:** `cloud-init status --long` shows `status: done`;
   `ufw` reports inactive or not installed, confirming hardening was
   deliberately left for Ansible, not cloud-init.

4. Build the Ansible inventory and baseline playbook:

   ```bash
   cat > inventory.ini <<EOF
   [capstone]
   ${CAPSTONE_IP} ansible_user=ansible ansible_ssh_private_key_file=$(pwd)/capstone-key ansible_ssh_common_args='-o StrictHostKeyChecking=no'
   EOF

   cat > site.yml <<'EOF'
   - name: Capstone baseline configuration
     hosts: capstone
     become: true
     tasks:
       - name: Install baseline packages
         ansible.builtin.apt:
           name: [chrony, ufw]
           state: present
           update_cache: true

       - name: Enable chrony
         ansible.builtin.systemd_service:
           name: chrony
           enabled: true
           state: started

       - name: Set default-deny inbound firewall policy
         community.general.ufw:
           policy: deny
           direction: incoming

       - name: Allow SSH through the firewall
         community.general.ufw:
           rule: allow
           name: OpenSSH

       - name: Enable ufw
         community.general.ufw:
           state: enabled
   EOF
   ```

5. **Negative test:** run the playbook in check mode first and confirm
   it correctly reports pending changes without applying them:

   ```bash
   ansible-playbook -i inventory.ini site.yml --check --diff
   ssh -i capstone-key ansible@"${CAPSTONE_IP}" 'ufw status'
   ```

   **Expected result:** the check-mode run reports tasks as "changed"
   (what *would* happen) but the live SSH check immediately after shows
   `ufw` is still inactive — proving `--check` made no real change to
   the host.

6. Apply the playbook for real and verify the end state:

   ```bash
   ansible-playbook -i inventory.ini site.yml
   ssh -i capstone-key ansible@"${CAPSTONE_IP}" \
     'ufw status verbose; systemctl is-active chrony'
   ```

   **Expected result:** `ufw status verbose` shows `Status: active`
   with a default-deny incoming policy and an OpenSSH allow rule;
   `systemctl is-active chrony` reports `active`.

7. Confirm idempotency by re-running the playbook:

   ```bash
   ansible-playbook -i inventory.ini site.yml | tail -5
   ```

   **Expected result:** the play recap shows `changed=0` for every
   task (aside from any facts-gathering), confirming the playbook is
   safe to re-run — the same idempotency principle [Chapter 02](02-essential-tools-shell-scripting-apt-and-snap-management.md)
   established for shell scripts and [Chapter 01](01-installation-autoinstall-ubuntu-pro-repositories-and-landscape.md) established for
   cloud-init modules now demonstrated end to end across the whole
   provisioning chain.

8. **Cleanup:**

   ```bash
   virsh destroy capstone-01 2>/dev/null || true
   virsh undefine capstone-01 --remove-all-storage
   cd ~ && rm -rf ~/lab-capstone
   ```

## Summary and Completion Checklist

cloud-init's datasource/module/stage architecture governs every
instance's first boot across every Ubuntu deployment path this volume
covers — autoinstall, MAAS, and plain cloud provisioning alike. MAAS
extends that same model to bare metal at fleet scale; Juju adds a
relation-aware application deployment model most useful for charmed,
multi-service applications; Ansible remains the vendor-neutral choice
for ongoing configuration management after first boot; and Landscape
closes the loop with fleet-wide patch and compliance visibility. Taken
together, these tools form a single, layered automation pipeline in
which each stage has a distinct, non-overlapping responsibility — the
principle this capstone lab exercised end to end.

- [ ] Can explain cloud-init's datasource, module, and boot-stage
      architecture and diagnose a first-boot failure.
- [ ] Can describe MAAS's region/rack controller split and the
      machine lifecycle it drives.
- [ ] Can deploy related applications with a Juju bundle.
- [ ] Can write and dry-run an Ansible playbook targeting an Ubuntu
      fleet using distribution-appropriate modules.
- [ ] Can perform a fleet-wide patch operation through Landscape.
- [ ] Completed the capstone hands-on lab end to end, including the
      negative test and cleanup.
