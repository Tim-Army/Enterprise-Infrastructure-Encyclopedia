# Chapter 03: Installing Proxmox VE

## Learning Objectives

- Obtain the Proxmox VE installer and present it to the server through the
  iDRAC virtual media.
- Install Proxmox VE onto the BOSS boot mirror, not the data array.
- Complete the installer's initial configuration correctly for this build.
- Reach the Proxmox web interface for the first time.
- Understand what the installer sets up and what is deferred to later
  chapters.

## Theory and Architecture

### What Proxmox VE is, and where it installs

**Proxmox VE** is a free, open-source virtualization platform built on
Debian Linux, KVM for virtual machines, and LXC for containers, managed
through a web interface. This build uses it as the hypervisor hosting the
ten virtual machines.

The critical installation decision is the **target disk**: Proxmox VE
installs onto the **BOSS RAID 1 mirror** from
[Chapter 02](02-storage-boss-boot-mirror-and-the-river-raid-5-array.md), not
the `river` RAID 5 array. This keeps the hypervisor on its small,
mirrored, independent boot device, leaving `river` entirely for virtual
machine storage. Installing onto the wrong disk — `river` — would consume
the data array with the OS and defeat the two-tier design.

### Installing through the iDRAC virtual media

Because the build is driven out-of-band, the installer is presented to the
server as **virtual media** through the iDRAC: the Proxmox VE ISO is mounted
over the network as if it were a CD in the server's drive, and the server is
told to boot from it. This is the same virtual-media mechanism the iDRAC
volume describes
([Volume XXIII, Chapter 05](../../volume-23-dell-idrac-9-10-administration/chapters/05-idrac-direct-virtual-console-virtual-media-and-local-service.md)),
and it means no physical media or crash cart is needed.

### What the installer configures

The Proxmox installer asks for a small set of decisions, and for this build
they are:

- **Target disk** — the BOSS mirror, with a filesystem (ext4 or ZFS; ext4
  is simple and sufficient for a boot device on hardware RAID).
- **Location, time zone, keyboard** — standard.
- **Root password and an administrative email.**
- **Management network** — a first IP for the host. This build's final
  management addressing (10.30.161.10/24 on the dedicated NIC) is set
  properly in [Chapter 05](05-network-architecture-management-nic-vlan-trunk-and-bridges.md);
  the installer just needs an initial reachable address to bring the web
  interface up.

The installer does *not* set up the VLAN trunk, the `river` datastore, or
the ISO repository — those are deliberate later steps.

## Design Considerations

- **Install to the BOSS mirror, and confirm the target before proceeding.**
  The single most important installer choice is the target disk; selecting
  `river` by mistake is the error that undoes the storage design. The
  installer lists disks by size and model — the ~256 GB BOSS mirror is
  distinguishable from the larger `river` array.
- **Keep the boot filesystem simple.** On a hardware-RAID boot mirror, ext4
  is a sound default. ZFS is powerful but adds complexity that the boot
  device does not need here; the VM storage decision is separate and made in
  [Chapter 06](06-proxmox-storage-the-river-datastore-and-iso-repository.md).
- **Give the installer a management address you can reach immediately.**
  Even though final networking comes later, the installer's address is how
  you first reach the web UI; make it one that is reachable from your
  workstation.
- **Do not attach `river` during installation.** Leaving the data array out
  of the install target removes any chance of installing onto it by
  accident; it is added as storage deliberately in Chapter 06.

## Implementation and Automation

### 1. Mounting the installer as virtual media

From the iDRAC web interface, or via RACADM:

```bash
# Attach the Proxmox VE ISO as virtual media over the network.
racadm -r 10.30.161.25 -u root -p <password> remoteimage \
  -c -l //fileserver/isos/proxmox-ve_9.iso -u <user> -p <pass>

# Set the next boot to the virtual CD/DVD, one time.
racadm -r 10.30.161.25 -u root -p <password> set iDRAC.ServerBoot.FirstBootDevice VCD-DVD
racadm -r 10.30.161.25 -u root -p <password> set iDRAC.ServerBoot.BootOnce Enabled

# Power-cycle to boot the installer.
racadm -r 10.30.161.25 -u root -p <password> serveraction powercycle
```

Then open the virtual console to drive the installer.

### 2. Running the installer

In the virtual console:

1. Select **Install Proxmox VE**.
2. Accept the license.
3. **Target disk:** select the BOSS mirror (the ~256 GB device). Confirm it
   is not the `river` array. Filesystem: `ext4`.
4. Set location, time zone, keyboard.
5. Set the root password and an administrative email.
6. **Management network:** set an initial address on the management network
   reachable from your workstation (final addressing is Chapter 05).
7. Confirm and install. Remove the virtual media when prompted, and let the
   server reboot from the BOSS mirror.

### 3. First contact with the web interface

After reboot, the Proxmox web interface listens on port 8006:

```bash
# From your workstation, confirm the web UI is up (self-signed cert).
curl -sk -o /dev/null -w '%{http_code}\n' https://<mgmt-ip>:8006/

# Confirm it booted from the BOSS mirror, not river.
# (After logging in, or via SSH:)
ssh root@<mgmt-ip> 'lsblk -o NAME,SIZE,MOUNTPOINT | grep -A2 boot'
```

Browse to `https://<mgmt-ip>:8006/`, log in as `root`, and confirm the node
appears. It will show a subscription warning — that is expected and
addressed in [Chapter 04](04-no-subscription-repository-updates-and-core-services.md).

## Validation and Troubleshooting

### Confirming a correct install

| Check | Expectation | If wrong |
| --- | --- | --- |
| Boot device | The BOSS mirror | Installed to `river` — reinstall to the correct target |
| Web UI | Responds on :8006 | Network address unreachable, or install incomplete |
| Node visible | The node appears in the UI | Login or service issue |
| `river` untouched | The RAID 5 array is still empty/unassigned | It was used as the install target by mistake |

### The wrong-target-disk failure

The install error that matters is choosing `river` as the target. The
symptom is that the RAID 5 array now holds the OS and is not available as VM
storage in Chapter 06. The fix is a reinstall onto the BOSS mirror. The
guard is simply reading the target-disk size on the installer screen: the
~256 GB mirror is the target; the larger array is not.

### Reaching the web UI

If `https://<mgmt-ip>:8006/` does not respond, confirm the install completed
and the address the installer was given is reachable from your workstation.
Because final networking is deferred to Chapter 05, the installer's address
is temporary; it only needs to be reachable long enough to log in and
proceed.

## Security and Best Practices

- **Set a strong root password at install and store it in a vault.** The
  Proxmox root account controls the whole hypervisor and every VM on it.
- **Do not expose the web interface beyond the management network.** Port
  8006 is a full administrative surface; it belongs on the isolated
  management subnet, reached through the management NIC configured in
  Chapter 05.
- **Plan to replace the self-signed certificate.** Proxmox generates a
  self-signed certificate; for anything beyond a single-operator lab,
  replacing it with an internally-trusted certificate is worth doing.
- **Keep the installer image trusted.** Obtain the Proxmox VE ISO from the
  official source and verify its checksum before mounting it as virtual
  media; it is the software that becomes the hypervisor.

## References and Knowledge Checks

**References**

- [Proxmox VE documentation](https://pve.proxmox.com/pve-docs/)
  — the authoritative installation and administration reference.
- [Volume XXIII, Chapter 05](../../volume-23-dell-idrac-9-10-administration/chapters/05-idrac-direct-virtual-console-virtual-media-and-local-service.md)
  — iDRAC virtual media, the mechanism used to present the installer.
- [Volume XXII, Chapter 01](../../volume-22-dell-openmanage-enterprise/chapters/01-architecture-requirements-deployment-and-first-configuration.md)
  — deploying a virtual appliance on Proxmox, the sibling context.

**Knowledge checks**

1. Which disk does Proxmox VE install onto in this build, and why not
   `river`?
2. How is the installer presented to the server without physical media?
3. What does the installer configure, and what does it deliberately leave
   for later chapters?
4. What is the symptom of installing onto the wrong target disk, and how do
   you avoid it?
5. Why is the installer's management address temporary in this build?

## Hands-On Lab

**Objective:** Install Proxmox VE onto the BOSS boot mirror through the
iDRAC virtual media, and reach its web interface.

**Prerequisites:** The healthy BOSS mirror and `river` array from
[Chapter 02](02-storage-boss-boot-mirror-and-the-river-raid-5-array.md), the
Proxmox VE ISO (checksum-verified), and iDRAC access.

**This lab requires the physical server.** The install target is the
hardware BOSS mirror.

**Procedure**

1. Mount the Proxmox VE ISO as iDRAC virtual media and set a one-time boot
   to the virtual CD.
2. Power-cycle and open the virtual console.
3. Run the installer: select the **BOSS mirror** as the target (confirm by
   size), ext4 filesystem, set locale/time/keyboard, root password, admin
   email, and an initial reachable management address.
4. Complete the install, remove the virtual media, and reboot from the BOSS
   mirror.
5. Browse to `https://<mgmt-ip>:8006/`, log in as root, and confirm the node
   appears (the subscription warning is expected).

**Negative test**

6. On the installer's target-disk screen, note the two available targets by
   size — the ~256 GB BOSS mirror and the larger `river` array — and
   confirm you can tell them apart *before* selecting. This is the check
   that prevents installing onto the data array. (Select the BOSS mirror.)

**Expected results**

- Proxmox VE installed on and booting from the BOSS mirror.
- The web interface reachable on port 8006, node visible.
- `river` untouched, still available for Chapter 06.

**Cleanup**

7. Detach the virtual media. The installed hypervisor is the base for every
   later chapter; leave it running.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Proxmox VE — the free, Debian-based, KVM/LXC virtualization platform — is
installed onto the BOSS RAID 1 boot mirror, kept deliberately separate from
the `river` RAID 5 array so the hypervisor stays small, mirrored, and
independent of the VM storage. The installer is presented to the server as
iDRAC virtual media, so the whole install is driven out-of-band from the
virtual console. The single most important installer choice is the target
disk: the ~256 GB BOSS mirror, never the larger `river` array, which is
added as VM storage deliberately later. The installer brings the web
interface up on port 8006 at a temporary management address; final
networking, updates, and storage are the next chapters.

- [ ] Proxmox VE installed on the BOSS mirror and booting from it.
- [ ] Web interface reachable on :8006 and the node visible.
- [ ] `river` left untouched and still available.
- [ ] Root password set and vaulted.
- [ ] Virtual media detached after install.
