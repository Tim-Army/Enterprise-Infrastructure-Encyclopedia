# Chapter 14: Automating the Lab Virtual Machines on KVM and libvirt

## Learning Objectives

- Describe how a plain Linux host with KVM and libvirt builds the Chapter 999 lab, and what is the same and different from Proxmox VE and the VMware platforms.
- Create the Linux bridges the lab needs, and say why plain bridges are enough when the guests tag VLANs themselves.
- Run `deploy-lab201-kvm.sh` to download and check one cloud image for each Linux flavor, make a copy-on-write disk for each machine, and create the machines with `virt-install`.
- Remove the build NICs, take the `baseline-201` snapshots, and delete the lab.
- Choose a Linux flavor for each machine, and know which flavors need an image or a subscription from you.

## Theory and Architecture

### What is the same and what is different

The twelve machines, their sizes, addresses, cloud-init content, and the Linux flavors are the same as in [Chapter 09](09-esxi-7-8-and-9-lab-virtual-machine-automation.md) and [Chapter 12](12-proxmox-ve-lab-virtual-machine-automation.md). The script reads the same manifest and uses the same seed tool and image resolver. KVM with libvirt differs in how it does the work.

| Item | Proxmox VE (Chapter 12) | KVM and libvirt (this chapter) |
| --- | --- | --- |
| Tool | `qm` on a Proxmox node | `virt-install`, `virsh`, and `qemu-img` on any Linux host |
| VLAN tags | The VLAN-aware bridge adds them (`tag=`) | The guests add them (the seeds use `--tagging guest`) |
| Bridges | Two must be VLAN-aware | Plain Linux bridges |
| Cloud-init | Proxmox's cloud-init drive with snippets | `virt-install --cloud-init`, which builds the data source |
| Disks | Imported into a Proxmox storage | A copy-on-write qcow2 file for each machine, backed by the flavor's image |

### Guest tagging

libvirt can place a guest on a bridge, but it cannot tag a Linux bridge port the way a Proxmox VLAN-aware bridge can. So the guests create their own VLAN interfaces, exactly as on VMware Workstation ([Chapter 11](11-vmware-workstation-pro-lab-virtual-machine-automation.md)). A plain Linux bridge passes 802.1Q frames, so the bridges need no VLAN settings. `gw-201` still bridges its two trunk adapters inside the guest and holds `.1` on every segment, as in the other chapters.

### The bridges

Create these before you run the script. It checks that each one exists, and does not change the host network.

| Bridge | Default name | Ports | Purpose |
| --- | --- | --- | --- |
| Trunk T1 | `br-t1` | The NIC that cables to `sw-648f-1` | VLAN-tagged lab machines and the gateway's first trunk |
| Trunk T2 | `br-t2` | The NIC that cables to `sw-2048f-1` | The gateway's second trunk and the peers' T2 links |
| Out-of-band | `br-oob` | The NIC that cables to the switch management ports | Segment 0 |
| Segment 220 | `br-lan220` | None | Internal link between `rtr-peer-1` and `mcast-src-201` |
| Build (internet) | `virbr0` | libvirt's NAT network | The build adapters and the gateway's uplink |

**Do not put both trunk NICs in one host bridge.** `gw-201` already bridges them inside the guest, so a host bridge that also joins them is a Layer 2 loop.

### Disks and images

For each flavor in use, `resolve-image.py` finds the newest published qcow2 image, downloads it into `--workdir`, and checks it against the publisher's checksum (SHA-256 or SHA-512, in whichever format the publisher uses). The script then makes one disk for each machine with `qemu-img create -f qcow2 -F qcow2 -b <image>`, so a machine stores only what it changes, and grows it to the manifest's size. Do not move or delete the image while machines use it, because their disks point to it.

Red Hat Enterprise Linux has no public download, so it needs `--rhel-image`, the qcow2 file from the Red Hat Customer Portal, and a subscription for the machines to install packages.

### Requirements

A Linux host with hardware virtualization (check `egrep -c '(vmx|svm)' /proc/cpuinfo`), libvirt running, `virt-install` 4.0 or later (the `--cloud-init` option came with that release), `qemu-img`, and Python 3. Run the script as `root` or as a member of the `libvirt` group.

## Design Considerations

- **Copy-on-write disks save space and time.** Twelve machines from one image take little more than the image plus what each machine writes. The cost is the dependency on the base image.
- **The gateway goes first.** `virt-install` starts each machine as it creates it, so the script creates `gw-201` first and then the others. There is no separate start step.
- **Generic OS variant.** The script passes `--os-variant generic`, which every libosinfo release knows. A specific variant can give better virtual hardware defaults, and you can change the line.
- **Names and MAC addresses.** Machine names are the libvirt domain names, and the MAC addresses are the manifest's, so the seeds match each adapter.
- **The build adapter.** Every machine has one on the build bridge for package installs. Remove them when the build is done: `--action remove-build-nics` detaches them live and in the saved configuration.
- **Flavors.** Each machine can use its own Linux flavor (`flavor` in the manifest, or `default_flavor`). Chapter 09 explains the catalog, the hardened flavors, and the license file. The ISO-based flavors (Windows, Linux Mint, Tiny Core) are not available on KVM, because this script has the guests tag VLANs and those guests cannot.

## Implementation and Automation

### What the script does, in order

1. Checks for `virsh`, `virt-install`, `qemu-img`, and Python, and (outside a dry run) that each bridge exists.
2. Resolves, downloads, and checks one image for each flavor in use.
3. Renders the seeds with `make-seed.py --tagging guest --guest-agent qemu`, passing `--license-file` if you gave one.
4. Creates `gw-201` first, then each other machine: a copy-on-write disk, then `virt-install --import` with the manifest's CPUs, memory, MAC addresses, bridges, and the three cloud-init files.

### Options

| Option | Meaning |
| --- | --- |
| `--ssh-key FILE` | Public key for `labadmin` (repeatable). Required for `deploy`. |
| `--action` | `deploy` (default), `status`, `remove-build-nics`, or `remove`. |
| `--bridge-wan`, `--bridge-oob`, `--bridge-t1`, `--bridge-t2`, `--bridge-lan220` | The bridge for each lab network. |
| `--disk-dir`, `--workdir` | Where the machine disks go, and where images and seeds are kept. |
| `--rhel-image FILE` | The Red Hat Enterprise Linux 10 qcow2 image. |
| `--license-file FILE` | JSON file with keys the seeds apply (Red Hat, Ubuntu Pro). |
| `--dry-run` | Print each command instead of running it. |

## Validation and Troubleshooting

| Check | Command | Expected |
| --- | --- | --- |
| Machines exist and run | `./deploy-lab201-kvm.sh --action status` | Twelve machines, `running` |
| Cloud-init finished | In a guest: `cloud-init status --long` | `status: done` |
| Guest-tagged interfaces | On `svc-201a`: `ip -d link show nic1v10` | A VLAN interface with `id 10` |
| Addresses | `ip -br addr` | The Chapter 999 addresses, both families |
| Tags on the trunk | On `gw-201`: `sudo tcpdump -e -n -i nic2 vlan` | Tagged frames from the switch |

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `Bridge br-t1 does not exist` | The bridge was not created | Create it, then rerun |
| `virt-install: unrecognized arguments: --cloud-init` | virt-install older than 4.0 | Upgrade virt-install |
| A machine boots but has no address | The seed files were not found, or the MAC address does not match | Check `virsh dumpxml <name>` for the MAC and `--cloud-init` paths |
| `checksum mismatch` | A damaged download | The script removes the file. Rerun it |
| No tagged frames on `nic2` | The host NIC or switch strips or drops tags | Check the NIC offload settings and the switch trunk |
| Packages are missing on a Rocky, Alma, or Red Hat machine | EPEL or the subscription is missing | Check `/var/log/cloud-init-output.log`; pass `--license-file` for Red Hat |

## Security and Best Practices

- **Run as root only when needed.** Use the `libvirt` group where you can.
- **Remove the build NICs.** `--action remove-build-nics` takes the lab off the internet. The gateway's uplink is also its build adapter, so it loses its internet access too.
- **Keep keys out of the repository.** The license file holds a Red Hat activation key, an Ubuntu Pro token, or both. Keep it outside the repository (it is ignored by git), and never put it in a zip. The keys are written only into the seed of the machines that need them.
- **Hardened flavors need a password hash.** The STIG forbids passwordless `sudo`. Set `LAB201_ADMIN_PASSWORD_HASH` to a crypt hash before building.
- **Isolate the lab bridges.** Do not give the host an address on `br-t1`, `br-t2`, or `br-oob` unless you mean to reach the lab from it.
- **Protect the images.** The base images are shared by every machine. Keep the folder writable only by root.

## References and Knowledge Checks

**References:**

- libvirt documentation, and the `virt-install`, `virsh`, and `qemu-img` manual pages (`--cloud-init`, `--import`, `detach-interface`, `undefine`).
- Canonical, Debian, Rocky Linux, AlmaLinux, and Fedora, for the cloud images and checksum files that `resolve-image.py` reads.
- Cloud-init documentation, the NoCloud data source and network configuration version 2.
- [Chapter 09](09-esxi-7-8-and-9-lab-virtual-machine-automation.md) for the manifest, seeds, flavors, licensing, and the Lab Builder, [Chapter 12](12-proxmox-ve-lab-virtual-machine-automation.md) for the other Linux-host platform, and [Chapter 999](999-shared-lab-infrastructure.md) for the lab.

**Knowledge checks:**

1. Why can KVM use plain Linux bridges when Proxmox VE needs VLAN-aware ones?
2. What does a copy-on-write disk depend on, and what happens if you delete the image?
3. Why does the script create the gateway first instead of starting it in a separate step?
4. Which flavors need something from you before they can build, and what?
5. What does `--action remove-build-nics` do to the gateway's internet access?

## Hands-On Lab

**Prerequisites.** A Linux host with KVM, libvirt, virt-install 4.0 or later, and `qemu-img`; about 22 GiB of free memory and 250 GB of disk; four NICs for the lab (T1, T2, out-of-band, and a build uplink or the default `virbr0`); the lab-scripts zip unpacked on the host; and an SSH key pair. Switch-side configuration is Chapter 999, Lab 999.3 and later.

### Lab 14.1: Create the bridges

1. Create `br-t1`, `br-t2`, and `br-oob` with the NICs that cable to the switches (for example with NetworkManager or `/etc/network/interfaces`), and `br-lan220` with no port.
2. Check that each exists: `ip link show type bridge`.

**Expected result.** Four bridges exist, and `virbr0` is up.

### Lab 14.2: Build the lab

1. Run a dry run, and read every line:

   ```bash
   ./deploy-lab201-kvm.sh --ssh-key ~/lab201.pub --dry-run
   ```

2. Run it without `--dry-run`. Then run `--action status` until all twelve machines run, and check `cloud-init status --long` on three of them.
3. **Tag test.** With the switch trunk configured, run `sudo tcpdump -e -n -i nic2 vlan` on `gw-201`.

**Expected result.** Twelve running machines with the Chapter 999 addresses, and tagged frames in the capture.

### Lab 14.3: Remove the build NICs and take the baseline

1. Run `./deploy-lab201-kvm.sh --action remove-build-nics`.
2. Snapshot every machine:

   ```bash
   for n in $(virsh list --name | grep -v '^$'); do virsh snapshot-create-as "$n" baseline-201; done
   ```

**Negative test.** From `static-1`, run `curl -m 5 https://cloud-images.ubuntu.com`. It must fail.

**Evidence.** The `status` output, a tagged `tcpdump` capture, and the failed `curl`.

### Cleanup

Run `./deploy-lab201-kvm.sh --action remove`, then delete `--workdir` and `--disk-dir`.

## Lab Verification

Complete this sign-off once Labs 14.1 to 14.3 have been run end to end on a real KVM host with a real switch trunk. Until then the script is unverified. It passes `shellcheck`, and its machine and adapter planning ran as a dry run against stubs, but it has not been run on a host. The `--cloud-init` option's handling of `network-config`, guest tagging through plain bridges, and the non-Ubuntu flavors are the first things to confirm.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter built the lab on a Linux host with KVM and libvirt. The guests tag the VLANs, so plain bridges are enough, and each machine gets a copy-on-write disk from the image of its Linux flavor. `gw-201` is created first and bridges the two trunks.

- [ ] Can say why plain bridges work here and VLAN-aware ones are needed on Proxmox.
- [ ] Has created the lab bridges and run the script with `--dry-run` and then for real.
- [ ] Has removed the build NICs and taken the `baseline-201` snapshots.
- [ ] Can explain what a copy-on-write disk depends on.
- [ ] Knows which flavors need an image or a subscription from you.
