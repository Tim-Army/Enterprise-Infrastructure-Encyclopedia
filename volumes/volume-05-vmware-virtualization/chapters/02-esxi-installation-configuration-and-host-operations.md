# Chapter 2: ESXi Installation, Configuration, and Host Operations

![Lab flow for this chapter: esxi-lab-01 is installed unattended via a kickstart file setting IP, hostname, NTP, and syslog forwarding; esxi-lab-02 is installed without NTP or syslog configured, deliberately non-standardized. A Host Profile (lab-standard-profile) extracted from esxi-lab-01 flags esxi-lab-02 as non-compliant on exactly the NTP/syslog settings. As a negative test, remediation without a required host-specific answer-file value fails or prompts rather than silently overwriting host identity; supplying the value and remediating again brings esxi-lab-02 to full compliance.](../../../diagrams/volume-05-vmware-virtualization/chapter-02-esxi-kickstart-host-profile-flow.svg)

*Figure 2-1. Flow used throughout this chapter's Hands-On Lab: a scripted ESXi install feeding a Host Profile that detects and remediates configuration drift on a second host.*

## Learning Objectives

- Compare interactive, scripted (kickstart), and PXE/UEFI HTTP network-boot
  ESXi installation methods, and select the correct one for a given
  deployment scale.
- Explain the modern ESXi boot architecture: the system boot partition, dual
  boot banks, and the ESX-OSData partition, and why persistent local storage
  now matters even for hosts that boot from removable media.
- Perform first-boot host configuration through the Direct Console User
  Interface (DCUI) and confirm it through `esxcli`.
- Explain image profiles, VIBs (vSphere Installation Bundles), and the four
  acceptance levels that govern what software ESXi will install.
- Build and apply a Host Profile to standardize and audit host
  configuration across a cluster, including per-host answer file overrides.
- Configure NTP, DNS, and syslog forwarding as day-one host services, and
  explain why time synchronization is a prerequisite for nearly everything
  else in a vSphere environment.
- Diagnose common host-level failures using the DCUI, `esxcli`, and
  `vmkernel.log`, including a Purple Screen of Death (PSOD) triage
  approach.

## Theory and Architecture

[Chapter 1](01-vmware-virtualization-architecture-and-design.md) introduced ESXi's internal architecture — the VMkernel, the
VMM/VMX process model, and the CIM/hostd/vpxa management stack. This
chapter starts one layer below that: how an ESXi host comes into existence
on physical (or nested) hardware, how its on-disk state is organized, and
how an administrator operates it day to day, both interactively and through
the same `esxcli`/PowerCLI tooling used throughout this volume.

### Installation methods

| Method | Mechanism | Typical scale | Key characteristic |
| --- | --- | --- | --- |
| Interactive | Boot the ESXi installer ISO, answer prompts | Single host, lab, initial bring-up | Manual, not repeatable without a script |
| Scripted (kickstart) | Installer ISO/USB with a `ks.cfg` install script | Small-to-medium fleets, standardized builds | Fully unattended given a valid script; same script can drive PXE installs |
| PXE / UEFI HTTP boot | Network boot the installer (or a stateless image) using DHCP options, TFTP/HTTP, and a kickstart script | Data-center-scale fleets, no local install media required | Requires DHCP option configuration and a boot infrastructure (TFTP or HTTP server) |
| vSphere Auto Deploy | Hosts PXE-boot directly into a vLCM-managed desired-state image supplied by vCenter Server, with no local ESXi install at all in the stateless case | Large, homogeneous, frequently-rebuilt fleets | Image and host assignment are centrally managed; covered further with vLCM in [Chapter 9](09-vsphere-lifecycle-automation-observability-and-troubleshooting.md) |

**Interactive installation** boots the standard ESXi ISO, walks through
disk selection, keyboard layout, and root password prompts, and installs to
the selected target device. It is the right tool for a single lab host or
initial proof-of-concept, and the wrong tool for anything that needs to be
repeated identically more than a handful of times.

**Scripted installation** uses a kickstart file (conventionally `ks.cfg`,
though the filename is arbitrary) — a plain-text script using ESXi's
kickstart command set — to answer every installer prompt without operator
interaction. The same kickstart file can be burned onto installation media,
referenced from a USB key, or served over HTTP/TFTP to a PXE-booted
installer, making it the common thread between "scripted install from
local media" and "network install" — the only difference is how the
installer image and the script reach the host.

**PXE / UEFI HTTP boot** removes physical media entirely: the host's NIC
firmware requests an address and boot file over DHCP, retrieves a boot
loader (traditionally via TFTP with PXELINUX/iPXE; increasingly via UEFI
HTTP boot, which uses HTTP instead of TFTP and is materially more reliable
at scale since HTTP tolerates network conditions TFTP does not), and loads
either the ESXi installer (for a scripted install to local/remote disk) or
a stateless boot image.

**Auto Deploy** is the fullest expression of network boot: vCenter Server
maintains a rules engine mapping physical hosts (by MAC address, IP range,
or other criteria) to a vLCM desired-state image and, optionally, a Host
Profile and location in the inventory. On PXE boot, the host loads that
image directly into memory rather than installing it to local disk
(**stateless caching** can persist a local cache purely to speed
subsequent boots, and **stateful install** mode uses Auto Deploy purely as
the initial provisioning mechanism, writing a normal persistent
installation to local disk after which the host boots from disk like any
other host). Auto Deploy's day-2 image lifecycle mechanics are covered in
depth in [Chapter 9](09-vsphere-lifecycle-automation-observability-and-troubleshooting.md); this chapter treats it only as one more way an ESXi
host's initial software gets onto (or into the memory of) the host.

### Boot device architecture: boot banks and ESX-OSData

Since the redesign introduced ahead of the vSphere 7 generation and carried
forward through the 9.x baseline, ESXi's on-disk layout uses three logical
components rather than the many small, separately sized partitions earlier
releases used:

- A small **system boot partition** (FAT) containing the boot loader.
- Two **boot banks**, each holding a complete, bootable copy of the ESXi
  image. Every upgrade writes to the inactive boot bank and only switches
  the active pointer to it after a successful boot, which is what makes
  "roll back to the previous build" a supported, low-risk operation rather
  than a full reinstall.
- A single **ESX-OSData** partition (VMFS-L-based) that consolidates what
  used to be separate scratch, locker (`/locker`, historically holding
  VMware Tools ISO images and configuration), and core dump partitions.

This consolidation has a direct operational consequence: **ESX-OSData
needs meaningfully more capacity and I/O durability than the old scratch
partition did**, because it now also holds core dumps and system logs by
default. VMware's current guidance is to install to a device with at least
tens of gigabytes of free space for ESX-OSData (sizing scales with host
memory, since core dumps must accommodate host RAM), and to avoid relying
on a USB or SD card as the *sole* persistent target for ESX-OSData in
production — boot banks can still live on read-only-friendly USB/SD media,
but ESX-OSData should be redirected to separate, more durable persistent
local storage (an internal SSD/HDD or a dedicated boot device with
sufficient write endurance) where the hardware platform provides one.
Deploying a host with only a low-endurance USB key and no separate
persistent local disk is a supported configuration but not the recommended
one for any host expected to run production workloads long-term — plan
physical boot media accordingly at hardware-selection time, not after
install.

```bash
# esxcli: confirm current boot device and ESX-OSData partition placement
esxcli storage core device list
esxcli system boot device get

# esxcli: report core dump partition configuration and current active config
esxcli system coredump partition get
```

### Image profiles, VIBs, and acceptance levels

ESXi software is packaged and installed as **VIBs (vSphere Installation
Bundles)** — the unit of packaging for the base ESXi image itself, drivers,
CIM providers, and third-party agents. An **image profile** is a named,
ordered collection of VIBs that together form a bootable ESXi image; the
standard VMware-published ESXi ISO is built from a base image profile, and
custom image profiles (built with Image Builder, or authored directly as a
vLCM cluster image) let an organization bake specific OEM drivers or
partner components into a single deployable image rather than installing
them as a separate post-install step on every host.

Every VIB carries an **acceptance level** that determines how it is
signed and how much VMware has validated it, and ESXi enforces a
**host acceptance level** that only permits installing VIBs at that level
or higher trust:

| Acceptance level | Meaning | Typical source |
| --- | --- | --- |
| VMwareCertified | Highest validation; passed VMware's certification test suite | Core ESXi components, select certified I/O drivers |
| VMwareAccepted | Built and tested by VMware, less rigorous than certification testing | VMware-authored partner-facing tools |
| PartnerSupported | Built by a partner (hardware/software vendor), verified through a partner program | OEM drivers, HBA/NIC vendor packages |
| CommunitySupported | Not signed to any VMware or partner program | Community/experimental tools |

By default, ESXi's host acceptance level is `PartnerSupported`, which
blocks installation of `CommunitySupported` VIBs unless the host's
acceptance level is deliberately lowered — a change that should be treated
as a deliberate, documented, and temporary exception rather than a
standing configuration on any host running production workloads.

```bash
# esxcli: inspect and set the host software acceptance level
esxcli software acceptance get
esxcli software acceptance set --level=PartnerSupported

# esxcli: list installed VIBs and their acceptance level/source
esxcli software vib list
```

### Direct Console User Interface (DCUI) and first-boot configuration

Immediately after install, a freshly booted ESXi host presents the
**DCUI** — a text-mode console (accessible directly at the physical/virtual
console, or via `Alt+F1` from the installer) used to perform the minimum
configuration required before any remote tool can reach the host:
management network VLAN/IP configuration (DHCP or static), root account
password, and, where required, restarting the management network stack
after a change. Every other host configuration task in this chapter —
NTP, syslog, licensing, joining vCenter — happens afterward through
`esxcli`, PowerCLI, or the vSphere Client, once the management network is
reachable. The DCUI remains available for the life of the host and is the
correct recovery tool when the management network itself is broken and no
remote path exists — including a **DCUI-accessible restart of management
agents** (`hostd`, `vpxa`) without a full reboot, useful when those
services have hung without the underlying host being unhealthy.

### Host Profiles and answer files

A **Host Profile** captures a reference host's configuration — networking,
storage, security/services settings, advanced system settings, and more —
as a reusable, comparable template. Host Profiles serve two purposes at
once: **provisioning** (apply a profile to bring a new or reimaged host
into compliance quickly) and **compliance auditing** (periodically check
every host in a cluster against its assigned profile and surface drift,
whether from manual changes, a failed automation run, or a partial
remediation). Because some settings are host-specific by nature (a
management IP address cannot be identical across every host in a cluster),
Host Profiles separate those into an **answer file** — a per-host set of
values collected the first time a profile is applied to a given host,
after which subsequent compliance checks and remediations use the correct
per-host value automatically rather than requiring the operator to supply
it every time.

```powershell
# PowerCLI: create a Host Profile from a known-good reference host
$reference = Get-VMHost -Name "esxi01.corp.example"
New-VMHostProfile -Name "profile-cluster-a-standard" -ReferenceHost $reference

# PowerCLI: check compliance of another host against that profile
$profile = Get-VMHostProfile -Name "profile-cluster-a-standard"
Test-VMHostProfileCompliance -VMHost (Get-VMHost -Name "esxi02.corp.example") -Profile $profile
```

## Design Considerations

- **Boot media versus ESX-OSData placement.** Do not conflate "supports
  booting from USB/SD" with "is a good production target for the full
  ESX-OSData partition." Confirm the server platform provides a separate
  durable local storage target for ESX-OSData (or accept the write-endurance
  and core-dump-capacity risk explicitly) before standardizing a boot media
  choice across a hardware refresh.
- **Installation method by fleet size and churn.** Interactive installs do
  not scale past a handful of hosts; scripted/kickstart installs from
  standard media are appropriate for moderate, infrequent deployments;
  PXE/UEFI HTTP boot with kickstart or Auto Deploy is justified once host
  count or rebuild frequency makes maintaining physical/virtual install
  media per host impractical. Match the investment in boot infrastructure
  (DHCP scopes, TFTP/HTTP servers, image repositories) to actual fleet
  churn, not aspirational scale.
- **Host acceptance level as a standing control.** Treat the host
  acceptance level as security-relevant configuration, not a one-time
  install-time setting — Host Profile compliance checking (below) should
  include it, since a host quietly lowered to `CommunitySupported` to
  install one troubleshooting tool and never restored is a real, observed
  drift pattern.
- **Host Profile scope versus answer-file sprawl.** A profile that captures
  too much host-specific state as answer-file entries becomes hard to
  reason about; a profile that captures too little misses real
  configuration drift. Start from a profile extracted off a genuinely
  representative, fully configured reference host, and review which
  settings the profile marks as host-specific before relying on it for
  compliance auditing.
- **NTP as a foundational dependency, not a checklist item.** Certificate
  validation (VMCA-issued host certificates, SSO token validation), vSAN
  cluster membership, and log/event correlation across hosts all silently
  degrade or fail outright under sufficient clock drift. Design time
  synchronization (below) before any other host service, and monitor it
  continuously rather than only at initial configuration.
- **Syslog retention and centralization.** ESX-OSData's log retention is
  bounded by local partition capacity and is not a substitute for a
  centralized, retained log target — plan remote syslog forwarding as a
  day-one requirement (see Implementation and Automation) rather than an
  operational afterthought discovered during the first serious incident.

## Implementation and Automation

### Scripted installation with a kickstart file

```text
# ks.cfg: unattended ESXi installation to the first local disk, minimal example
vmaccepteula
rootpw --iscrypted <ENCRYPTED_ROOT_PASSWORD_HASH>
install --firstdisk --overwritevmfs
network --bootproto=static --ip=10.10.10.21 --netmask=255.255.255.0 \
  --gateway=10.10.10.1 --nameserver=10.10.10.5 --hostname=esxi21.corp.example \
  --addvmportgroup=0
reboot

%firstboot --interpreter=busybox
esxcli network firewall ruleset set -e true -r syslog
esxcli system syslog config set --loghost='udp://10.10.10.50:514'
esxcli system syslog reload
```

The `%firstboot` section runs once, on the first boot after installation
completes, and is the standard place to apply configuration that the
kickstart command set itself does not directly express — here, enabling
outbound syslog forwarding immediately rather than as a separate manual
step after the host is reachable.

### Serving a kickstart install over PXE (UEFI HTTP boot)

```text
# DHCP option excerpt (server-specific syntax varies): point UEFI HTTP boot
# clients at the boot loader and, from there, at the kickstart file served
# over HTTP alongside the installer image.
option vendor-class-identifier "HTTPClient";
option bootfile-name "http://10.10.10.5/esxi/mboot.efi";
```

```text
# Boot loader argument passed to the installer, referencing the kickstart
# script location:
ks=http://10.10.10.5/esxi/ks-cluster-a.cfg
```

### Configuring NTP, DNS, and syslog on an existing host

```bash
# esxcli: configure and enable NTP, then verify synchronization state
esxcli system ntp set --server=10.10.10.10 --server=10.10.10.11
esxcli system ntp set --enabled=true
esxcli system ntp get

# esxcli: confirm DNS resolver configuration
esxcli network ip dns server list
esxcli network ip dns search list

# esxcli: forward syslog to a remote collector over UDP and open the firewall
esxcli system syslog config set --loghost='udp://10.10.10.50:514'
esxcli system syslog reload
esxcli network firewall ruleset set -e true -r syslog
```

```powershell
# PowerCLI: apply the same NTP/syslog configuration across every host in a cluster
$cluster = Get-Cluster -Name "prod-cluster-a"
foreach ($vmhost in (Get-VMHost -Location $cluster)) {
  Add-VmHostNtpServer -VMHost $vmhost -NtpServer "10.10.10.10", "10.10.10.11"
  Get-VMHostService -VMHost $vmhost | Where-Object { $_.Key -eq "ntpd" } |
    Start-VMHostService
  Set-VMHostSysLogServer -VMHost $vmhost -SysLogServer "udp://10.10.10.50:514"
}
```

### Extracting, attaching, and remediating a Host Profile

```powershell
# PowerCLI: attach a profile to a cluster and remediate every non-compliant host
$cluster = Get-Cluster -Name "prod-cluster-a"
$profile = Get-VMHostProfile -Name "profile-cluster-a-standard"
Apply-VMHostProfile -Entity $cluster -Profile $profile -Confirm:$false

foreach ($vmhost in (Get-VMHost -Location $cluster)) {
  $result = Test-VMHostProfileCompliance -VMHost $vmhost -Profile $profile
  if ($result.IncompliantConfiguration.Count -gt 0) {
    Apply-VMHostProfile -Entity $vmhost -Profile $profile -Confirm:$false
  }
}
```

### Joining a host to vCenter Server

```powershell
# PowerCLI: add a freshly configured host to an existing cluster
Connect-VIServer -Server vcenter01.corp.example
Add-VMHost -Name "esxi21.corp.example" -Location (Get-Cluster -Name "prod-cluster-a") `
  -User "root" -Password "<ROOT_PASSWORD>" -Force
```

## Validation and Troubleshooting

- **Management network reachability.** If a host cannot be reached
  remotely immediately after install, the DCUI's `Network Restart
  Management Network` option (also reachable non-interactively via
  `esxcli network ip interface` commands once any console access exists)
  is the first diagnostic step — confirm VLAN tagging, IP configuration,
  and physical link state before assuming a higher-layer failure.
- **NTP synchronization state.** `esxcli system ntp get` reports whether
  NTP is enabled and which servers are configured, but confirming actual
  sync requires checking `esxcli system time get` (or the vSphere Client's
  time configuration status) against expected drift; a host that shows
  NTP enabled but has not actually synchronized (commonly due to a
  firewall blocking outbound UDP/123 to the configured servers) will still
  drift and eventually produce certificate and cluster-membership symptoms
  that look unrelated to time at first glance.
- **VIB installation failures.** `esxcli software vib install` failures
  most commonly trace to an acceptance-level mismatch (attempting to
  install a `CommunitySupported` VIB against a `PartnerSupported` host) or
  a maintenance-mode requirement not met; `esxcli software vib list -v`
  and the installer's own error text (which names the specific
  precondition that failed) are the first place to look rather than
  assuming a generic package-manager fault.
- **Host Profile compliance failures.** A remediation failure most often
  traces to either a missing answer-file value for a host-specific setting
  the profile expects, or a setting the profile is trying to change that
  is currently in use (an active VMkernel adapter binding, for instance)
  — `Test-VMHostProfileCompliance` output names the specific non-compliant
  item, and the vSphere Client's Host Profile remediation pre-check
  surfaces the same detail with more context before committing the
  change.
- **PSOD (Purple Screen of Death) triage.** A PSOD is the VMkernel's fatal
  exception handler output — it indicates the VMkernel itself has
  determined it cannot continue safely, not merely that a single VM or
  service failed. Record the exception type and backtrace shown on the
  physical/virtual console (or retrieve it after reboot from
  `/var/core/` and the automatically generated core dump), check it
  against the VMware Compatibility Guide and current known-issues
  guidance for the exact ESXi build, and treat repeated PSODs on the same
  host as a hardware or driver-compatibility investigation, not something
  resolved by reboot alone.

  ```bash
  # esxcli: confirm core dump configuration is active before relying on
  # a future PSOD producing a usable dump for analysis
  esxcli system coredump partition get
  esxcli system coredump network get
  ```

## Security and Best Practices

- Keep host acceptance level at `PartnerSupported` or higher in production;
  treat any temporary reduction to `CommunitySupported` as an exception
  requiring explicit approval, a defined rollback time, and Host Profile
  compliance monitoring to catch hosts left in that state.
- Set the root account password at install time to a value meeting
  organizational complexity policy, and immediately transition day-to-day
  administrative access to named accounts through Active Directory
  integration and role-based access control rather than shared root use —
  the identity and RBAC model is covered in Chapter 3, and ESXi Lockdown
  Mode (restricting direct host-level API/SSH access once vCenter manages
  the host) is covered in full in Chapter 8.
- Enable outbound syslog forwarding to a centralized, retained log
  collector for every host at build time, not after the first incident
  that needed logs the local host had already rotated away.
- Validate NTP source authenticity and reachability as part of routine
  health monitoring — a host silently free-running without synchronized
  time is a security-relevant condition (log timestamp integrity, certificate
  validity windows) as much as an operational one.
- Apply firmware and driver updates through validated, HCL-confirmed
  combinations only; an unsupported ESXi build/driver/firmware combination
  is a common root cause of both instability and PSODs that is entirely
  avoidable through pre-change compatibility validation.
- Use Host Profiles as a continuous compliance control, not only a
  provisioning convenience — schedule recurring compliance checks and
  alert on drift so unauthorized or accidental configuration changes are
  caught quickly.

## References and Knowledge Checks

**References**

- [VMware vSphere 9.x Documentation](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-0.html) — *Installing and Setting Up ESXi* (interactive,
  scripted, PXE/UEFI HTTP boot, and Auto Deploy installation methods).
- [VMware vSphere 9.x Documentation](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-0.html) — *ESXi Installation and Boot Options* (boot
  bank architecture, ESX-OSData sizing guidance).
- [VMware vSphere 9.x Documentation](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-0.html) — *Host Profiles*.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — dated vSphere
  9.x / NSX 4.x baseline referenced throughout this volume.
- See [Chapter 1](01-vmware-virtualization-architecture-and-design.md) for ESXi's internal process architecture (VMkernel, VMM,
  hostd/vpxa).
- See [Chapter 3](03-vcenter-server-deployment-identity-and-recovery.md) for vCenter Server identity integration that replaces
  direct root-account host administration.
- See [Chapter 8](08-vsphere-and-nsx-security-architecture.md) for Lockdown Mode and full host security hardening.
- See [Chapter 9](09-vsphere-lifecycle-automation-observability-and-troubleshooting.md) for vSphere Lifecycle Manager images, cluster-scale
  remediation, and Auto Deploy's desired-state image lifecycle.

**Knowledge checks**

1. Why does the consolidation of scratch, locker, and core dump partitions
   into a single ESX-OSData partition change boot-media planning guidance
   compared to older ESXi releases?
2. A VIB fails to install with an acceptance-level error. What two things
   should be checked before lowering the host's acceptance level to
   resolve it?
3. What is the functional difference between what a Host Profile captures
   directly and what it defers to a per-host answer file, and why is that
   split necessary?
4. Why is NTP described as a prerequisite for certificate validation and
   cluster membership rather than simply "good practice"?
5. What distinguishes stateless Auto Deploy caching from a stateful Auto
   Deploy-initiated install, in terms of where the host's running image
   actually resides after boot?

## Hands-On Lab

**Objective:** Perform a scripted ESXi installation using a kickstart file
in a nested lab, configure NTP and syslog forwarding, extract a Host
Profile from the result, apply it to a second host, deliberately introduce
configuration drift, detect it, and remediate.

**Prerequisites**

- A nested-ESXi-capable lab (a physical or virtual host capable of running
  nested ESXi VMs with hardware virtualization exposed), the standard
  ESXi 9.x installer ISO, and at least two target nested-ESXi VMs with a
  virtual disk sized for a comfortable ESX-OSData partition (40 GB or
  greater is a safe lab minimum).
- A reachable HTTP or TFTP server (or simply attaching the kickstart file
  to boot media) to serve `ks.cfg`; a lab DHCP scope if testing PXE boot.
- A lab syslog receiver (any host listening on UDP/514 is sufficient — a
  simple `nc -ul 514` listener works for validation purposes).
- PowerCLI connected to a lab vCenter Server with host-add and Host
  Profile privileges.

**Steps**

1. Author a kickstart file for the first nested host, adjusting IP,
   hostname, and syslog target to lab values, using the `ks.cfg` example
   in Implementation and Automation as a starting point. Attach it to the
   installer boot process (as a secondary CD-ROM/ISO referencing
   `ks=cdrom:/KS.CFG`, or via a served URL for a PXE-style test).

   **Expected result:** the host completes an unattended installation and
   reboots to the DCUI showing the configured static management IP.

2. From a workstation with network access to the new host, confirm NTP and
   syslog were applied by the `%firstboot` section:

   ```bash
   esxcli system syslog config get
   ```

   **Expected result:** the configured loghost matches the lab syslog
   target, and test log entries generated on the host (for example,
   restarting a service) appear at the syslog receiver.

3. Repeat interactive or scripted installation for a second nested host
   using a different static IP/hostname, but *without* NTP or syslog
   configured, to create a deliberately non-standardized second host.

4. Join both hosts to a lab vCenter cluster, then extract a Host Profile
   from the first (correctly configured) host:

   ```powershell
   Connect-VIServer -Server vcenter-lab.local
   $reference = Get-VMHost -Name "esxi-lab-01.local"
   New-VMHostProfile -Name "lab-standard-profile" -ReferenceHost $reference
   ```

   **Expected result:** the new profile appears under
   `vSphere Client > Policies and Profiles > Host Profiles`.

5. Check the second host's compliance against the profile:

   ```powershell
   $profile = Get-VMHostProfile -Name "lab-standard-profile"
   Test-VMHostProfileCompliance -VMHost (Get-VMHost -Name "esxi-lab-02.local") -Profile $profile
   ```

   **Expected result:** the compliance check reports non-compliant items
   specifically covering the NTP and syslog settings that differ from the
   reference host.

6. **Negative test:** attempt to remediate without first supplying
   required answer-file values for host-specific settings (if the profile
   includes a host-specific network setting not yet answered for the
   second host):

   ```powershell
   Apply-VMHostProfile -Entity (Get-VMHost -Name "esxi-lab-02.local") -Profile $profile -Confirm:$false
   ```

   **Expected result:** remediation either prompts for or fails on the
   missing host-specific value, demonstrating that Host Profiles do not
   silently overwrite host-specific identity with the reference host's
   values — confirm the specific failure reason matches a host-specific
   (not global) setting.

7. Supply the required answer-file value and remediate again:

   **Expected result:** `Test-VMHostProfileCompliance` now reports the
   second host as compliant, and `esxcli system syslog config get` on that
   host shows the same loghost as the reference host.

8. **Cleanup:** remove the Host Profile, and if the nested hosts are lab
   scratch resources, power off and delete both nested-ESXi VMs; otherwise
   revert syslog/NTP configuration on the second host to its prior state.

   ```powershell
   Get-VMHostProfile -Name "lab-standard-profile" | Remove-VMHostProfile -Confirm:$false
   ```

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

ESXi installation scales from a manual interactive install through
scripted kickstart-driven installs to full network boot via PXE/UEFI HTTP
boot and Auto Deploy, with the choice governed by fleet size and rebuild
frequency rather than a single universally correct method. The modern boot
architecture's consolidated ESX-OSData partition changes boot-media
planning compared to older releases, making persistent local storage a
first-class hardware decision rather than an afterthought. Image profiles,
VIBs, and acceptance levels govern what software a host will install and
at what trust level, and Host Profiles turn both initial provisioning and
ongoing configuration compliance into a repeatable, auditable process built
on a reference host plus per-host answer files. NTP, DNS, and syslog are
day-one host services, not later hardening steps, because so much of the
rest of the platform — certificate validity, cluster membership, log
correlation — silently depends on them.

- [ ] Can choose the correct ESXi installation method for a given fleet
      size and boot-infrastructure investment.
- [ ] Can explain the boot bank / ESX-OSData architecture and its
      implication for boot-media hardware selection.
- [ ] Can explain VIB acceptance levels and their security implication.
- [ ] Can extract, apply, and remediate a Host Profile, including
      correctly handling host-specific answer-file values.
- [ ] Can configure NTP and centralized syslog forwarding on a host and
      validate both.
- [ ] Can perform first-pass PSOD triage and knows where core dump
      configuration and output live.
- [ ] Completed the hands-on lab, including the answer-file negative test
      and cleanup.
