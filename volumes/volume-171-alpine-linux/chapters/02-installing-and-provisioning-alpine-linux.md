# Chapter 02: Installing and Provisioning Alpine Linux

## Learning Objectives

- Choose the correct Alpine install image (standard, extended, virt, netboot) for
  a target.
- Install Alpine to disk with `setup-alpine` and understand each prompt.
- Provision Alpine from a cloud image on a hypervisor and fix the one thing cloud
  images routinely get wrong.
- Complete first-boot verification and capture a baseline.

## Theory and Architecture

Alpine ships several install images, and picking the right one saves time:

| Image | Contents | Use |
| --- | --- | --- |
| **Standard** | Kernel + base + firmware for bare metal | Physical machines, most VMs |
| **Extended** | Standard plus a larger package set on the media | Offline installs |
| **Virt** | Trimmed kernel for hypervisors (no bare-metal firmware) | VMs (smallest ISO) |
| **Netboot** | Kernel/initramfs/modloop for PXE | Diskless/PXE fleets |
| **Cloud (`nocloud`/generic)** | Pre-built disk image with cloud-init | Proxmox/OpenStack/public cloud |

Two provisioning paths dominate. The **ISO + `setup-alpine`** path boots the
installer environment (a diskless Alpine running in RAM), runs one interactive
script, and writes a **sys**-mode install to disk — this is the path for bare metal
and for VMs you build by hand. The **cloud-image** path imports a pre-built disk and
lets cloud-init set the hostname, network, SSH keys, and password on first boot —
faster for fleets and the natural fit for a hypervisor like Proxmox.

`setup-alpine` is the whole installer. It is a shell script that calls a series of
smaller `setup-*` helpers (`setup-keymap`, `setup-hostname`, `setup-interfaces`,
`setup-timezone`, `setup-apkrepos`, `setup-sshd`, `setup-disk`), any of which you
can also run individually later to reconfigure a running system.

## Design Considerations

- **Match the image to the platform.** On a hypervisor use the **virt** ISO (or a
  **cloud** image); the standard ISO's bare-metal firmware is dead weight in a VM.
- **Pick the install mode deliberately.** `setup-disk` offers `sys` (normal disk
  install), `data` (RAM system, `/var` on disk), and `lvm` layouts. For a server or
  a lab VM, choose **`sys`**.
- **Size the disk for the job, not the base.** A base install is tiny, but plan for
  what the box will hold — logs, a package cache, or, for this volume's TFTP server
  (Chapter 05), the firmware images it will serve. Cloud images ship a small root
  filesystem that you grow after import (Chapter 07).
- **Decide the network model up front.** A server wants a **static** address; a
  throwaway lab node can take DHCP, but convert it to static before you depend on
  it, so the address does not move.

## Implementation and Automation

### Path A — ISO install with `setup-alpine`

Boot the virt ISO, log in as `root` (no password in the installer), and run:

```sh
setup-alpine
```

The script walks these prompts (defaults in brackets):

```text
Select keyboard layout [none]: us
Select variant []: us
Enter system hostname [localhost]: alpine-lab
Which one to initialize? [eth0]: eth0
Ip address for eth0? (or 'dhcp', 'none') [dhcp]: 10.30.99.50
Netmask? [255.255.255.0]: 255.255.255.0
Gateway? (or 'none') [none]: 10.30.99.1
DNS domain name? (or '.' for none) []: lab.local
DNS nameserver(s)? []: 96.45.45.45 96.45.46.46
Which timezone? [UTC]: UTC
HTTP/FTP proxy URL? (or 'none') [none]: none
Which NTP client to run? (busybox, openntpd, chrony) [chrony]: chrony
Enter mirror number or URL: f          # 'f' picks the fastest mirror
Setup a user? (enter a lower-case loginname, or 'no') [no]: labadmin
Which SSH server? (openssh, dropbear, none) [openssh]: openssh
Which disk(s) would you like to use? [none]: sda
How would you like to use it? (sys, data, lvm, none) [none]: sys
WARNING: Erase the above disk(s) and continue? [n]: y
```

`setup-alpine` then partitions `sda`, installs the base system, writes the
bootloader, and finishes. Reboot and remove the ISO:

```sh
reboot
```

The installed system boots from disk; log in as `root` (or the user you created)
with the password you set.

### Path B — cloud image on Proxmox VE

Import the generic cloud image as a VM disk, attach a cloud-init drive, and boot.
On the Proxmox host:

```sh
# Download the current generic cloud image (nocloud/UEFI variant), then:
qm create 140 --name tftp --memory 1024 --cores 1 --net0 virtio,bridge=vmbr1
qm importdisk 140 nocloud_alpine-3.24.0-x86_64-bios-cloudinit-r0.qcow2 local-lvm
qm set 140 --scsihw virtio-scsi-pci --scsi0 local-lvm:vm-140-disk-0
qm set 140 --ide2 local-lvm:cloudinit --boot order=scsi0 --serial0 socket
qm set 140 --ipconfig0 ip=10.30.99.50/24,gw=10.30.99.1 --ciuser root --cipassword '<password>'
qm resize 140 scsi0 100G          # grow the virtual disk (filesystem grown in Ch07)
qm start 140
```

**Host setup — deploying this image on your hypervisor.** The create/import and interface-mapping steps are the same for every appliance and are collected once in the Master Appendices: [Deploying Lab Appliance Images on Each Hypervisor](../../volume-997-master-appendices/chapters/73-appendix-deploying-lab-appliance-images-on-each-hypervisor.md) — Proxmox, KVM, ESXi/vSphere, Workstation/Fusion, VirtualBox, Hyper-V, EVE-NG, GNS3, containerlab, Nutanix AHV, and Xen.

Cloud-init applies the hostname, the static IP, and the credentials on first boot.
**The one thing to check every time:** Alpine's cloud-init commonly sets the IP
address but **not** a DNS resolver, so `/etc/resolv.conf` is empty and `apk` cannot
reach a mirror. Fix it immediately (Lab 2.2).

## Validation and Troubleshooting

First-boot checks, whichever path you used:

```sh
cat /etc/alpine-release           # the installed release
ip -brief address                 # interface and IP
cat /etc/resolv.conf              # nameserver(s) — MUST be non-empty
ping -c1 dl-cdn.alpinelinux.org   # name resolution + reachability
apk update                        # proves the mirror is reachable
```

Common failure modes:

- **`apk update` hangs or fails to resolve the mirror.** Empty or wrong
  `/etc/resolv.conf` (the cloud-image gotcha). Add a nameserver.
- **No network at all after a cloud install.** The interface name may differ
  (`eth0` vs `ens18`); check `ip link` and `/etc/network/interfaces`.
- **The root filesystem is far smaller than the disk.** Cloud images ship a small
  filesystem that does not auto-grow on Alpine; grow it with `resize2fs`
  (Chapter 07). This is expected, not a fault.

## Security and Best Practices

- Set a strong `root` password (or disable root SSH and use a sudo/`doas` user)
  during `setup-alpine`, not afterwards.
- Choose **openssh** over dropbear for a server, and disable password
  authentication once a key is in place.
- Convert DHCP lab nodes to **static** addressing before they carry a service, so
  the management address cannot move (Chapter 04).
- Snapshot the freshly-provisioned VM as a clean baseline before you install
  anything on top of it.

## References and Knowledge Checks

- Alpine wiki — [Installation](https://wiki.alpinelinux.org/wiki/Installation) and
  [setup-alpine](https://wiki.alpinelinux.org/wiki/Setup_alpine).
- Alpine wiki — [Alpine Linux in a VM / cloud](https://wiki.alpinelinux.org/wiki/Alpine_Linux_and_Cloud).
- [Alpine downloads](https://alpinelinux.org/downloads/) (image variants).

**Knowledge checks:**

1. Which ISO variant is smallest for a VM, and why?
2. Which `setup-disk` mode produces a normal, persistent disk install?
3. What does an Alpine cloud image most often fail to configure, and how do you
   detect it?

## Hands-On Lab

**Objective:** Stand up a working Alpine host two ways — a `setup-alpine` disk
install and a Proxmox cloud image — and reach a verified first boot.

**Shared prerequisites** — a hypervisor (Proxmox VE used here) and an Alpine virt
ISO plus a generic cloud image for the chosen release. **Cost:** none.

### Lab 2.1 — Install to disk with `setup-alpine`

**Objective:** Produce a `sys`-mode install on a VM.

1. Create a VM with the **virt** ISO attached, boot it, and log in as `root`.
2. Run `setup-alpine` and answer the prompts as in Implementation, choosing
   `sda` and `sys`.
3. `reboot`, detach the ISO, and log in to the installed system.

```sh
# after reboot, on the installed system:
cat /etc/alpine-release
lsblk                         # sda partitioned by setup-disk
rc-status                     # OpenRC brought services up
```

**Expected result:** the release string, a partitioned `sda`, and running services
— a normal, persistent Alpine install.

**Negative test:** answer `none` at the disk prompt; the system runs only in RAM
and loses everything on reboot — choose `sys` for a persistent install.

**Rollback:** keep the VM for later chapters, or delete it.

### Lab 2.2 — Provision from a cloud image and fix DNS

**Objective:** Import a cloud image on Proxmox, boot it, and repair the missing
resolver.

1. Import and boot the cloud image as in Path B above.
2. Log in (serial console or SSH) and check the network:

```sh
ip -brief address             # 10.30.99.50/24 present
cat /etc/resolv.conf          # EMPTY — the cloud-image gotcha
apk update                    # fails: cannot resolve the mirror
```

3. Add a resolver and retry:

```sh
printf 'nameserver 96.45.45.45\nnameserver 96.45.46.46\n' > /etc/resolv.conf
ping -c1 dl-cdn.alpinelinux.org
apk update
```

**Expected result:** before the fix, `apk update` cannot resolve the mirror; after
writing `/etc/resolv.conf`, name resolution works and `apk update` fetches the
index. This is the single most common Alpine-cloud-image surprise.

**Negative test:** try to `apk add` a package before fixing DNS; it fails to
resolve the mirror even though the IP and gateway are correct — the address was set
but the resolver was not.

**Rollback:** none — the resolver fix is wanted. (Make it durable in Chapter 04.)

### Lab 2.3 — First-boot verification and baseline

**Objective:** Confirm a healthy host and capture a baseline.

```sh
cat /etc/os-release
ip -brief address; ip route
apk update && apk upgrade
rc-status -a | head
```

**Expected result:** the release, correct addressing and default route, an
up-to-date package set, and OpenRC services running — a host ready for the rest of
the volume.

**Negative test:** skip `apk update` before installing packages later; you may pull
stale indexes or miss a security update — always refresh the index first.

**Rollback:** snapshot the VM as `baseline` (`qm snapshot 140 baseline` on Proxmox).

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Alpine installs two ways: `setup-alpine` writes a `sys`-mode disk install from the
virt ISO after one interactive script, and a cloud image imports a pre-built disk
that cloud-init provisions on first boot. The cloud path is faster but routinely
leaves `/etc/resolv.conf` empty, so the first move after a cloud boot is to add a
nameserver and confirm `apk update` reaches a mirror. Either way, verify the
release, addressing, and services, then snapshot a baseline.

- [ ] Can choose the right Alpine image for a platform.
- [ ] Can install Alpine to disk with `setup-alpine` in `sys` mode.
- [ ] Can import and boot an Alpine cloud image on a hypervisor.
- [ ] Can detect and fix the empty-`resolv.conf` cloud-image gotcha.
- [ ] Completed Labs 2.1–2.3 including each negative test.
