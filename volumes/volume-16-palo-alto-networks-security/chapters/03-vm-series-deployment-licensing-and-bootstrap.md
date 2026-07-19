# Chapter 03: VM-Series Deployment, Licensing, and Bootstrap

## Learning Objectives

- Describe the VM-Series architecture, its supported hypervisor and cloud
  targets, and how it differs operationally from a PA-Series hardware
  appliance.
- Compare VM-Series licensing models — bring-your-own-license (BYOL),
  pay-as-you-go (PAYG/usage-based), and flexible vCPU (credit-based)
  licensing — and select an appropriate model for a given deployment
  pattern.
- Build a bootstrap package (`init-cfg.txt`, `bootstrap.xml`, license, and
  content directories) that brings a VM-Series instance to a fully licensed,
  network-reachable state with zero manual first-boot configuration.
- Deploy a VM-Series firewall on a hypervisor using an OVF template and
  attach a bootstrap volume.
- Diagnose common bootstrap and licensing failures using VM-Series console
  and CLI output.

## Theory and Architecture

[Chapter 01](01-cybersecurity-apprentice-foundations.md) established that PAN-OS separates the management plane from the
dataplane on every platform. VM-Series is the software form factor of that
same PAN-OS image, running as a virtual machine instead of on dedicated
appliance hardware. The single-pass parallel processing engine, App-ID,
User-ID, and Content-ID are unchanged — what changes is how compute
resources are provisioned, how the instance is licensed, and how initial
configuration is delivered.

### Supported deployment targets

VM-Series ships as a set of hypervisor- and cloud-specific images built from
the same PAN-OS source:

| Target | Image format | Typical use case |
| --- | --- | --- |
| VMware ESXi / vCenter | OVF/OVA | Private cloud, data center virtualization ([Volume V](../../volume-05-vmware-virtualization/README.md)) |
| KVM (including OpenStack) | QCOW2 | Open-source hypervisor environments |
| Microsoft Hyper-V | VHD | Windows Server virtualization |
| AWS | AMI (Marketplace or BYOL) | Public cloud perimeter and VPC segmentation |
| Microsoft Azure | Managed image (Marketplace) | Public cloud perimeter and VNet segmentation |
| Google Cloud Platform | Compute Engine image | Public cloud perimeter and VPC segmentation |
| Cisco ACI / Nutanix AHV / OCI | Platform-specific | Software-defined data center and additional cloud targets |

Regardless of target, every VM-Series instance still exposes one management
interface (`MGT`) and a set of dataplane interfaces, and the same
`set`/`show`/`commit` CLI model from [Chapter 01](01-cybersecurity-apprentice-foundations.md) applies once the instance is
reachable. What differs by target is how those virtual network interface
cards (vNICs) are provisioned and mapped — a hypervisor administrator (or
Terraform/CloudFormation template, [Volume IX](../../volume-09-infrastructure-automation/README.md)) attaches vNICs to port
groups, subnets, or VPC ENIs *before* the firewall ever boots, and PAN-OS
enumerates them in the order presented by the hypervisor as `ethernet1/1`,
`ethernet1/2`, and so on.

### Model sizing and vCPU/memory tiers

VM-Series is licensed and sized by model, which maps to a vCPU and memory
allocation ceiling rather than to fixed hardware:

| Model | Typical vCPU | Typical memory | Session capacity class |
| --- | --- | --- | --- |
| VM-50 (Lite) | 2 | 6.5 GB | Small branch / low session count |
| VM-100 | 2 | 6.5 GB | Branch / small site |
| VM-300 | 4 | 9 GB | Mid-size site or moderate cloud workload |
| VM-500 | 8 | 16 GB | Larger data center or cloud perimeter |
| VM-700 | 16 | 56 GB | High-throughput data center / cloud hub |

Under-provisioning vCPU or memory below a model's requirement produces a
firewall that boots but fails to license correctly or throttles
performance; over-provisioning beyond what a license tier uses wastes
hypervisor capacity without added throughput, since the license — not the
raw hardware — caps what the dataplane will use.

### Licensing models

- **BYOL (bring-your-own-license).** A traditional term or perpetual
  license tied to a specific VM-Series serial number, activated with an
  auth code exactly as in [Chapter 02](02-cybersecurity-practitioner-and-platform-portfolio.md). The customer manages capacity
  planning explicitly by choosing a model size (VM-300, VM-500, and so on)
  up front.
- **PAYG (pay-as-you-go / usage-based).** Consumed directly from a cloud
  marketplace (AWS, Azure, GCP) with hourly or annual billing bundled into
  the cloud provider invoice; no separate Palo Alto Networks auth code is
  required for the base firewall, though CDSS subscriptions may still need
  separate activation depending on the marketplace listing (bundled vs.
  bring-your-own-subscription).
- **Flexible vCPU licensing (credit-based).** A pool-based model where an
  organization purchases a block of credits and deploys VM-Series instances
  of varying sizes against that pool, resizing or redeploying instances
  without re-licensing each one individually — well suited to autoscaling
  groups and elastic cloud topologies where instance count and size change
  frequently.

A Practitioner-level engineer chooses among these based on deployment
elasticity: static, long-lived data-center VM-Series instances are
frequently BYOL; cloud-native autoscaling groups favor PAYG or flexible
vCPU credits precisely because instance count is not fixed at design time.

### The bootstrap package

A factory-default VM-Series instance requires the same first-boot
configuration as any PAN-OS firewall ([Chapter 01](01-cybersecurity-apprentice-foundations.md)) — hostname, management
IP, license, content, and initial policy. Doing this by hand does not scale
to dozens or hundreds of cloud instances. The **bootstrap package** solves
this by presenting a structured set of files to the instance at first boot,
either as an attached virtual disk/ISO (on-premises hypervisors), an AWS S3
bucket, an Azure storage account/blob, or a GCP storage bucket (public
cloud), so the instance licenses, configures, and joins Panorama management
with no manual console interaction.

```text
bootstrap/
├── config/
│   └── init-cfg.txt        # Day-0 network, Panorama, and DNS parameters
│   └── bootstrap.xml        # Optional full or partial candidate config
├── content/                 # Preloaded Applications/Threats, AV, WildFire content
├── software/                 # Optional preloaded PAN-OS software image
├── license/                  # Optional auth-code or license key files
└── plugins/                  # Optional cloud/plugin packages
```

`init-cfg.txt` is a flat key-value file that answers the minimum questions
needed to bring the instance onto the network and under Panorama
management; `bootstrap.xml` (optional) is a full or partial PAN-OS XML
configuration applied on top, useful for pre-staging zones, interfaces, and
a baseline security policy so the instance is enforcing policy from its
first commit rather than passing all traffic by default during an
unconfigured window.

## Design Considerations

- **BYOL vs. PAYG for a given workload.** Favor BYOL for firewalls with a
  predictable, long-lived footprint (data-center hub, branch office) where
  centralized license and support-contract tracking matters. Favor PAYG or
  flexible vCPU credits for elastic cloud workloads — auto-scaling
  application tiers, ephemeral CI/CD-triggered environments — where
  instance count is not known at procurement time.
- **Bootstrap vs. manual first-boot for cloud instances.** Manual
  console-based first-boot configuration ([Chapter 01](01-cybersecurity-apprentice-foundations.md)'s lab) does not scale
  past a handful of instances and is operationally incompatible with
  autoscaling groups, where instances are created and destroyed by
  automation with no human present at boot. Any VM-Series instance deployed
  by Terraform, CloudFormation, or a cloud-native autoscaler should be
  bootstrapped, not manually configured.
- **Secrets in the bootstrap package.** `init-cfg.txt` can contain a
  Panorama VM auth key and, if `bootstrap.xml` is used, potentially
  sensitive baseline configuration. Treat the bootstrap storage location
  (S3 bucket, Azure blob, ISO image) with the same access-control rigor as
  a secrets store — an overly permissive bucket policy leaks the means to
  onboard a rogue firewall into Panorama management.
- **Model sizing against expected session count and throughput,** not just
  against available hypervisor headroom. Under-sizing produces silent
  session or throughput ceilings during peak load rather than an obvious
  failure; capacity plan against the vendor's published session and
  throughput tables for the intended VM-Series model, and revisit sizing
  after production traffic baselines are available.
- **Interface count and mapping discipline.** Because vNIC order determines
  `ethernet1/N` mapping, define and document a consistent vNIC attachment
  order in the deployment template (Terraform module, OVF customization
  spec) so that `ethernet1/1` is always the untrust-facing interface across
  every instance built from that template — inconsistent ordering across
  instances is a common source of "the new firewall's zones are backwards"
  incidents.

## Implementation and Automation

### Building an init-cfg.txt file

```text
type=dhcp-client
ip-address=
default-gateway=
netmask=
ipv6-address=
ipv6-default-gateway=
hostname=pa-vmseries-01
panorama-server=10.20.30.10
panorama-server-2=10.20.30.11
tplname=vmseries-branch-template
dgname=vmseries-branch-dg
dns-primary=10.10.10.2
dns-secondary=10.10.10.3
op-command-modes=jumbo-frame
vm-auth-key=1234567890123456
auth-key=
plugin-op-commands=
dhcp-send-hostname=yes
dhcp-send-client-id=yes
dhcp-accept-server-hostname=yes
dhcp-accept-server-domain=yes
```

Set `type=static` and populate `ip-address`, `default-gateway`, and
`netmask` explicitly for environments without a management-network DHCP
service. `panorama-server`, `tplname`, and `dgname` bind the instance to a
specific Panorama template and device group ([Chapter 06](06-panorama-installation-central-management-and-logging.md)) at first boot, and
`vm-auth-key` is the one-time VM auth key generated on Panorama
(`request bootstrap vm-auth-key generate lifetime <minutes>`) that
authorizes this instance to register.

### Preparing the bootstrap package (on-premises ISO)

```bash
mkdir -p bootstrap/config bootstrap/content bootstrap/license bootstrap/software
cp init-cfg.txt bootstrap/config/
cp bootstrap.xml bootstrap/config/          # optional
cp panup-all-contents-*.tgz bootstrap/content/   # optional preloaded content

# Build an ISO the hypervisor can attach as a CD-ROM at first boot.
genisoimage -o vmseries-bootstrap.iso -V config -J -R bootstrap/
```

### Preparing the bootstrap package (AWS S3)

```bash
aws s3 mb s3://acme-vmseries-bootstrap-branch01
aws s3 cp init-cfg.txt s3://acme-vmseries-bootstrap-branch01/config/
aws s3 cp bootstrap.xml s3://acme-vmseries-bootstrap-branch01/config/
```

The EC2 instance's IAM role (not embedded static credentials) grants the
VM-Series instance read access to the bucket at boot — a pattern consistent
with [Volume VII](../../volume-07-cloud-infrastructure/README.md)'s cloud identity guidance and preferable to any
credential embedded in the bootstrap files themselves.

### Deploying the OVF template (VMware ESXi/vCenter)

```bash
# From a workstation with ovftool installed:
ovftool \
  --datastore=datastore01 \
  --network="dvPortGroup-Untrust=Untrust-PG" \
  --network="dvPortGroup-Trust=Trust-PG" \
  --diskMode=thin \
  --acceptAllEulas \
  --name=pa-vmseries-01 \
  PA-VM-ESX-11.1.4.ova \
  vi://administrator@vsphere.local@vcenter.acme.local/Datacenter1/host/Cluster1
```

Attach the bootstrap ISO as the instance's CD-ROM device (or, for cloud
platforms, associate the bootstrap bucket/blob via instance metadata or
user-data) before first power-on, then power on the VM.

### Confirming bootstrap completion

```text
admin@pa-vmseries-01> show system info | match hostname
hostname: pa-vmseries-01

admin@pa-vmseries-01> show system bootstrap
Bootstrap: SUCCESS
```

## Validation and Troubleshooting

- **Bootstrap ISO not detected at boot.** Confirm the ISO is attached as a
  CD-ROM device (not a floppy or secondary hard disk) and that the
  hypervisor boot order allows the instance to read it during first boot.
  On cloud platforms, confirm the bootstrap bucket/blob location is passed
  correctly via user-data/instance metadata per the cloud-specific
  bootstrap method.
- **`show system bootstrap` reports FAILURE.** Check
  `/opt/panlogs/vm-series-bootstrap.log` via a support/tech-support file
  bundle, or the platform's serial console output — the log names the
  specific stage that failed (network reachability to Panorama, malformed
  `init-cfg.txt` syntax, invalid `vm-auth-key`, or missing required
  fields).
- **Instance boots but never appears in Panorama.** Confirm
  `panorama-server` in `init-cfg.txt` is reachable from the management (or
  dataplane, if Panorama is reached over a data interface) network, that
  the `vm-auth-key` has not expired (`request bootstrap vm-auth-key
  generate` accepts a `lifetime` in minutes), and that the device group and
  template names in `dgname`/`tplname` exist on Panorama exactly as
  spelled — a typo produces a silent registration failure rather than an
  explicit error in some releases.
- **License activation fails after bootstrap.** If `auth-key` was supplied
  in `init-cfg.txt` for BYOL activation, confirm outbound HTTPS reachability
  to the Palo Alto Networks licensing service, exactly as in [Chapter 02](02-cybersecurity-practitioner-and-platform-portfolio.md)'s
  license troubleshooting. PAYG instances do not use `auth-key` and license
  automatically against the marketplace subscription; supplying one
  unnecessarily on a PAYG image has no effect but indicates a template
  built from the wrong reference.
- **Interfaces appear in the wrong zone after deployment.** This is almost
  always a vNIC-ordering issue at the hypervisor or cloud template level,
  not a PAN-OS defect — verify vNIC attachment order against the documented
  standard in Design Considerations before assuming `bootstrap.xml` is
  wrong.

## Security and Best Practices

- Never commit a populated `init-cfg.txt` or `bootstrap.xml` containing a
  live `vm-auth-key`, `auth-key`, or embedded administrator credential to a
  version control repository; template the file and inject secrets at
  build time from a secrets manager ([Volume IX](../../volume-09-infrastructure-automation/README.md)).
- Generate `vm-auth-key` values with the shortest practical `lifetime` for
  the deployment window, not an indefinite key reused across every future
  instance — a leaked long-lived key allows an attacker to bootstrap a
  rogue firewall directly into Panorama management.
- Restrict bootstrap storage (S3 bucket, Azure blob container, on-premises
  ISO repository) to the minimum principals that need read access, and
  enable access logging on cloud storage bootstrap locations so
  unauthorized reads are detectable.
- Preload `bootstrap.xml` with a default-deny baseline security policy
  ([Chapter 05](05-application-identity-threat-and-data-security-policy.md)) rather than leaving the instance to rely on any factory
  default allow-all behavior during the window between boot and the first
  administrator-applied policy.
- Right-size the VM-Series model to the workload; over-provisioning is a
  cost and attack-surface consideration (a larger allocated instance is a
  larger footprint to patch and monitor at the hypervisor/cloud layer), not
  merely a spending decision.

## References and Knowledge Checks

**References**

- Palo Alto Networks, *VM-Series Deployment Guide* (version 11.1).
- Palo Alto Networks, *VM-Series Bootstrap Guide*.
- Palo Alto Networks, *VM-Series Licensing* documentation (BYOL, PAYG,
  flexible vCPU credits).
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — PAN-OS 11.x
  baseline used throughout this volume.
- [Volume V](../../volume-05-vmware-virtualization/README.md) — VMware Virtualization, for ESXi/vCenter deployment
  prerequisites shared with any OVF-based appliance.
- [Volume VII](../../volume-07-cloud-infrastructure/README.md) — Cloud Infrastructure, for cloud identity and secrets
  patterns referenced above.

**Knowledge checks**

1. Which bootstrap file supplies day-0 network and Panorama parameters, and
   which optional file supplies a full or partial candidate configuration?
2. Why is flexible vCPU (credit-based) licensing generally preferred over
   BYOL for an autoscaling cloud deployment?
3. What PAN-OS CLI or Panorama action generates the `vm-auth-key` value
   used in `init-cfg.txt`, and why should its lifetime be kept short?
4. Name two consequences of inconsistent vNIC attachment order across
   VM-Series instances built from the same deployment template.

## Hands-On Lab

**Objective:** Build a bootstrap package for a VM-Series instance, deploy it
on a hypervisor with the bootstrap volume attached, and validate that the
instance reaches a licensed, network-configured state without manual
console configuration — including a negative test using a deliberately
malformed bootstrap file.

**Prerequisites**

- A hypervisor capable of running VM-Series (ESXi, KVM, or a comparable lab
  virtualization host) with the VM-Series OVA/QCOW2 image available, or a
  cloud lab account with the VM-Series Marketplace image if a hypervisor is
  unavailable.
- `ovftool` (VMware) or the equivalent hypervisor import tooling, and
  `genisoimage`/`mkisofs` (or platform equivalent) to build an ISO.
- A lab or evaluation auth code, or a PAYG image, for licensing.
- Completion of [Chapter 01](01-cybersecurity-apprentice-foundations.md) (basic PAN-OS CLI familiarity) and [Chapter 02](02-cybersecurity-practitioner-and-platform-portfolio.md)
  (license/content mechanics).

**Steps**

1. Create the bootstrap directory structure:

   ```bash
   mkdir -p bootstrap/config bootstrap/content bootstrap/license bootstrap/software
   ```

2. Create `bootstrap/config/init-cfg.txt` with static management addressing
   for your lab network:

   ```text
   type=static
   ip-address=10.10.10.15
   default-gateway=10.10.10.1
   netmask=255.255.255.0
   hostname=pa-vmseries-lab01
   dns-primary=10.10.10.2
   op-command-modes=jumbo-frame
   ```

   Omit `panorama-server`, `tplname`, `dgname`, and `vm-auth-key` for this
   standalone lab (Panorama-managed bootstrap is exercised in [Chapter 06](06-panorama-installation-central-management-and-logging.md)).

3. Build the bootstrap ISO:

   ```bash
   genisoimage -o vmseries-bootstrap.iso -V config -J -R bootstrap/
   ```

4. Deploy the VM-Series OVA to your hypervisor, attach `vmseries-bootstrap.iso`
   as the CD-ROM device, map dataplane vNICs to lab port groups, and power
   on the instance.

5. Connect to the instance console and confirm bootstrap success:

   ```text
   admin@pa-vmseries-lab01> show system bootstrap
   ```

   **Expected result:** `Bootstrap: SUCCESS`, and `show system info` reflects
   the hostname and management IP from `init-cfg.txt` without any manual
   configuration having been entered.

6. Confirm management reachability from your workstation:

   ```bash
   ssh admin@10.10.10.15
   ```

   **Expected result:** A successful login prompt.

7. **Negative test:** Edit `bootstrap/config/init-cfg.txt` to introduce a
   malformed `netmask` value (for example, `netmask=999.255.255.0`),
   rebuild the ISO under a new filename, attach it to a second lab instance
   (or redeploy), and power on:

   ```bash
   genisoimage -o vmseries-bootstrap-bad.iso -V config -J -R bootstrap/
   ```

   **Expected result:** The instance either fails bootstrap validation
   (`show system bootstrap` reports `FAILURE`) or falls back to its factory
   default management IP, confirming that PAN-OS does not silently accept
   invalid `init-cfg.txt` values. Inspect the bootstrap log referenced in
   Validation and Troubleshooting to identify the specific rejected field.

8. Correct the file and confirm the instance recovers on redeploy, or
   discard the failed instance if this is a disposable lab.

9. **Cleanup:** Power off and remove the lab VM-Series instance(s) if they
   will not be reused, detach and delete the bootstrap ISO file(s), and
   remove any lab-only port group mappings created solely for this
   exercise.

## Summary and Completion Checklist

VM-Series brings PAN-OS to any hypervisor or public cloud as software,
governed by the same App-ID/User-ID/Content-ID engine covered in Chapter
01, but requiring deliberate decisions about model sizing, licensing model,
and — critically for any deployment beyond a handful of instances — a
bootstrap package that eliminates manual first-boot configuration. The
bootstrap mechanism is the foundation that later chapters build on: Chapter
06 extends `init-cfg.txt` to bind instances directly into Panorama device
groups and templates, and [Chapter 07](07-firewall-operations-troubleshooting-upgrades-and-automation.md) revisits fleet-scale automation for
software and content lifecycle across bootstrapped instances.

- [ ] Can compare BYOL, PAYG, and flexible vCPU licensing and select an
      appropriate model for a given workload pattern.
- [ ] Can build a valid `init-cfg.txt` and package it for on-premises
      (ISO) or cloud (object storage) bootstrap delivery.
- [ ] Can deploy a VM-Series OVA on a hypervisor with a bootstrap volume
      attached.
- [ ] Can diagnose a failed bootstrap using console output and the
      bootstrap log.
- [ ] Completed the hands-on lab, including the negative test and cleanup.
