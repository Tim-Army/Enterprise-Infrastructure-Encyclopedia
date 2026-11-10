# Chapter 12: Automating the Lab Virtual Machines on Proxmox VE

## Learning Objectives

- Create the Linux bridges the lab needs on a Proxmox VE node, including two VLAN-aware trunk bridges, and say why the two trunk NICs must not share one host bridge.
- Run `deploy-lab201-proxmox.sh` to download the cloud image, render the seeds, create the twelve machines with `qm`, and start them.
- Explain how the cloud-init snippets (`--cicustom`) carry the lab's addresses, and check them with `qm cloudinit dump`.
- Remove the build NICs, take the `baseline-201` snapshots, and delete the lab.
- Name what is the same and what is different from the VMware chapters.

## Theory and Architecture

### What is the same and what is different

The twelve machines, their sizes, addresses, and cloud-init content are the same as in [Chapter 09](09-esxi-7-8-and-9-lab-virtual-machine-automation.md), and the script reads the same manifest and uses the same seed tool. Proxmox VE differs in how it does the work.

| Item | VMware chapters | Proxmox VE |
| --- | --- | --- |
| Tool | PowerCLI on a workstation | `qm` and `pvesm` on the node, as `root` |
| Networks | Virtual switches the script creates | Linux bridges that **you** create beforehand |
| VLAN tags | Port groups (Chapter 09, 10) or the guest (Chapter 11) | The bridge adds them: `tag=<VLAN>` on a VLAN-aware bridge |
| Cloud-init | A seed ISO on a CD drive | Proxmox's own cloud-init drive, with the seed files as **snippets** |
| Guest tools | `open-vm-tools` | `qemu-guest-agent` |
| Disk import | OVA import | The qcow2 cloud image, imported with `import-from` |

### Bridges

Proxmox puts VMs on Linux bridges defined in `/etc/network/interfaces`. The script does not change the host network, because a wrong change there cuts you off from the node. It checks that the bridges exist and that the two trunk bridges are VLAN-aware, then uses them. Create five bridges:

| Bridge | Default name | Ports | VLAN-aware | Purpose |
| --- | --- | --- | --- | --- |
| Trunk T1 | `vmbr2` | The NIC that cables to `sw-648f-1` | Yes | VLAN-tagged lab machines and `gw-201`'s first trunk |
| Trunk T2 | `vmbr3` | The NIC that cables to `sw-2048f-1` | Yes | `gw-201`'s second trunk and the T2 links of the peers |
| Out-of-band | `vmbr1` | The NIC that cables to the switch management ports | No | Segment 0 |
| WAN (build) | `vmbr0` | Your existing uplink | As is | The build adapters and the gateway's uplink |
| Segment 220 | `vmbr4` | None | No | Internal link between `rtr-peer-1` and `mcast-src-201` |

An example for the two trunk bridges and the internal bridge, in `/etc/network/interfaces` (replace the NIC names):

```text
auto vmbr2
iface vmbr2 inet manual
    bridge-ports enp3s0
    bridge-stp off
    bridge-fd 0
    bridge-vlan-aware yes
    bridge-vids 2-4094

auto vmbr3
iface vmbr3 inet manual
    bridge-ports enp4s0
    bridge-stp off
    bridge-fd 0
    bridge-vlan-aware yes
    bridge-vids 2-4094

auto vmbr4
iface vmbr4 inet manual
    bridge-ports none
    bridge-stp off
    bridge-fd 0
```

Apply it with `ifreload -a`, from the node's console or a session that does not use those NICs.

**Do not put both trunk NICs in one host bridge.** `gw-201` already bridges T1 and T2 inside the guest (as in Chapter 09), so a host bridge that also joins them is a Layer 2 loop.

### Cloud-init on Proxmox

The script creates a cloud-init drive (`--ide2 <storage>:cloudinit`) for each machine and points Proxmox at three snippet files with `--cicustom`: `user=`, `network=`, and `meta=`. The files come from `make-seed.py` (`--guest-agent qemu --tagging hypervisor`) and are copied to the node's snippets directory, as `lab201-<machine>-user.yml` and so on. A custom `user=` snippet **replaces** the user configuration Proxmox would generate from its own settings, so set nothing in the Cloud-Init tab of the web interface for these machines. Proxmox can show what a machine will receive:

```bash
qm cloudinit dump 20102 user
qm cloudinit dump 20102 network
```

The snippets directory belongs to a storage with the **Snippets** content type. The default `local` storage has the directory (`/var/lib/vz/snippets`), but the content type may be off. Turn it on under Datacenter, Storage, `local`, Content.

### Machine numbers

Machines get IDs from `--vmid-base` plus their position in the manifest, so with the default 20100 `gw-201` is 20101, `svc-201a` is 20102, and `attacker-201` is 20112. Pick a base whose range is free.

### Versions

The script uses `qm set ... --scsi0 <storage>:0,import-from=<image>`, which imports a disk image in one step. It was written for Proxmox VE 8.1 and later, which includes the 9.x releases. On an older node, the two-step `qm importdisk` and `qm set` form is needed instead. Check `pveversion` first.

## Design Considerations

- **Bridges are a prerequisite.** Creating them is a host network change, so it stays a manual step, with the example above.
- **Trunk VLAN lists.** `gw-201`'s two trunk NICs use `trunks=2-4094` on the VLAN-aware bridges, so all VLANs pass. VLAN 1 is not trunked. If your switch uses VLAN 1 anywhere, change the script.
- **VLAN-tagged machines.** Other machines get `tag=<VLAN>` on `vmbr2` or `vmbr3`, so they see untagged frames, as with VST on ESXi.
- **Firewall.** The script sets `firewall=0` on every NIC. The Proxmox firewall's MAC and IP filters would block the gateway's bridging. Use the lab's own `nftables` on `gw-201` for filtering.
- **CPU type.** The machines use `x86-64-v2-AES`, which Ubuntu 24.04 needs or better, and which lets them move between nodes of different generations. Use `host` for speed if you do not migrate.
- **Storage.** `--storage` receives the disks and the cloud-init drives. `local-lvm` is typical. Use a directory or ZFS storage if you prefer.
- **Images and flavors.** Each machine can use its own Linux flavor. `resolve-image.py` finds the newest published image for each flavor in use, downloads it, and checks it against the publisher's checksum, removing the file on a mismatch. Proxmox VE imports qcow2 images directly, so every published flavor works here without conversion.
- **Idempotence.** A machine whose ID exists is skipped. A rerun after a failure carries on.

## Implementation and Automation

### What the script does, in order

1. Checks that it runs where `qm`, `pvesm`, `python3`, and `curl` exist.
2. Checks that each bridge exists and that the two trunk bridges are VLAN-aware.
3. Finds the snippets directory with `pvesm path`, and stops if the storage has no snippets content type.
4. Downloads and checks the image.
5. Renders the seeds into `--workdir`.
6. For each machine: copies the three snippets, runs `qm create` with the CPU, memory, and one `--netN` for each manifest adapter (`virtio=<MAC>,bridge=<bridge>,tag=<VLAN>`, or `trunks=` for a trunk), imports the disk, resizes it, adds the cloud-init drive, sets the boot order, and sets `--cicustom`.
7. Starts `gw-201` first, then the rest.

### Options

| Option | Meaning |
| --- | --- |
| `--ssh-key FILE` | Public key for `labadmin` (repeatable). Required for `deploy`. |
| `--action` | `deploy` (default), `status`, `remove-build-nics`, or `remove`. |
| `--storage`, `--snippets-storage` | Storage for disks and storage for snippets. |
| `--bridge-wan`, `--bridge-oob`, `--bridge-t1`, `--bridge-t2`, `--bridge-lan220` | The bridge for each network. |
| `--vmid-base` | The ID offset (default 20100). |
| `--workdir` | Where the images and the rendered seeds go (default `/var/tmp/lab201`). |
| `--rhel-image FILE` | The Red Hat Enterprise Linux 10 qcow2 image, needed for the `rhel-10` flavors. |
| `--license-file FILE` | JSON file with keys to apply: Red Hat, Ubuntu Pro, a Windows product key, and a Proxmox subscription key (Chapter 09). |
| `--iso FLAVOR=VOLUME` | The install ISO of a Windows, Linux Mint, or Tiny Core flavor, as a Proxmox volume such as `local:iso/Server2025.iso` (repeatable). |
| `--iso-storage NAME` | Storage with the `iso` content type, where the script puts each machine's answer-file CD (default `local`). |
| `--dry-run` | Print each command instead of running it. |

## Validation and Troubleshooting

| Check | Command | Expected |
| --- | --- | --- |
| Machines exist | `./deploy-lab201-proxmox.sh --action status` | Twelve machines, `status: running` |
| Cloud-init finished | In a guest: `cloud-init status --long` | `status: done` |
| The seed is what you expect | `qm cloudinit dump 20102 network` | The netplan for `svc-201a` with its MAC addresses |
| Guest agent | `qm agent 20102 ping` | No error once the agent runs |
| Addresses | In a guest: `ip -br addr` | The Chapter 999 addresses |
| Tags on the trunk | On `gw-201`: `sudo tcpdump -e -n -i nic2 vlan` | Tagged frames from the switch |

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `Bridge vmbr2 is not VLAN-aware` | `bridge-vlan-aware yes` missing | Add it and run `ifreload -a` |
| `Storage local has no snippets content type` | Snippets not enabled | Enable the content type on the storage |
| `qm set ... import-from` is not accepted | Proxmox VE older than the script expects | Upgrade, or use `qm importdisk` |
| A machine boots with the wrong network settings | A custom snippet was ignored or overridden | Compare `qm cloudinit dump` with the snippet; clear fields in the web interface's Cloud-Init tab |
| `gw-201` passes no tagged frames | `trunks=` did not apply, or the bridge is not VLAN-aware | Run `bridge vlan show dev tap20101i2`; check the NIC line with `qm config 20101` |
| The lab loops or floods | Both trunk NICs were put in one host bridge | Give each NIC its own bridge |

## Security and Best Practices

- **Run as root, review first.** The script needs `root` on the node. Read it, run it with `--dry-run`, and do not run it on a production cluster node that you cannot afford to disturb.
- **Keep the build NIC short-lived.** `--action remove-build-nics` removes `net0` from every machine. That is the only NIC on the WAN bridge, and for `gw-201` it is also the uplink, so the gateway loses its internet access too. Run it when the packages are in, and put its first NIC back with the same MAC address, so the seed's netplan still matches it (`qm set 20101 --net0 virtio=00:50:56:2d:01:00,bridge=vmbr0,firewall=0`), when you next need packages.
- **Snippet permissions.** Snippets are readable by anyone who can read the storage. They hold public keys and, if you set one, a password hash. Do not put secrets in them, and delete them at the end.
- **Cloud-init privilege.** Treat the Proxmox permission that lets a user edit cloud-init settings as administrator access to the guests, because the settings run as root on first boot.
- **Firewall on the host.** Keep the node's management interface off the lab bridges and behind the Proxmox firewall or your network firewall.
- **Updates.** Keep Proxmox VE patched, because lab machines with test attacks run on the same kernel as the node.

## References and Knowledge Checks

**References:**

- Proxmox VE documentation, the `qm` manual and the Cloud-Init Support chapter (`cicustom`, snippets, `qm cloudinit dump`).
- Proxmox VE documentation, Network Configuration: Linux bridges, VLAN-aware bridges, and `ifreload`.
- Canonical, [Ubuntu cloud images](https://cloud-images.ubuntu.com/noble/current/) (the qcow2 `.img` and `SHA256SUMS`).
- Cloud-init documentation, NoCloud data source and network configuration version 2.
- [Chapter 09](09-esxi-7-8-and-9-lab-virtual-machine-automation.md) for the manifest, seeds, and the gateway bridge, and [Chapter 999](999-shared-lab-infrastructure.md) for the lab.

**Knowledge checks:**

1. Why does the script refuse to create the bridges itself?
2. What happens if you put the T1 and T2 NICs in a single VLAN-aware host bridge as well as bridging them in `gw-201`?
3. What does a custom `user=` snippet replace, and how do you see what a machine will get?
4. Why does `gw-201`'s trunk NIC use `trunks=` and not `tag=`?
5. Which command removes a machine's build NIC, and what happens to the gateway's internet access afterwards?

## Hands-On Lab

**Prerequisites.** A Proxmox VE 8.1 or later node with 22 GiB of free memory, 250 GB of storage, and four NICs for the lab (T1, T2, out-of-band, WAN), root access, `python3` (installed by default), the lab-scripts zip unpacked on the node (for example in `/root/lab201`), and an SSH key pair on your workstation. Switch-side configuration is Chapter 999, Lab 999.3 and later.

### Lab 12.1: Create the bridges

1. Add the bridge blocks above for T1, T2, out-of-band, and segment 220, using your NIC names, to `/etc/network/interfaces`, and run `ifreload -a` from the console.
2. Enable the Snippets content type on the `local` storage.
3. Check: `bridge vlan show` lists VLANs 2 to 4094 on `enp3s0` and `enp4s0` (or your names).

**Expected result.** Each bridge exists, and both trunk bridges report VLAN filtering on.

### Lab 12.2: Build the lab

1. Copy your public key to the node, change to the `proxmox` folder, and run a dry run:

   ```bash
   ./deploy-lab201-proxmox.sh --ssh-key ~/lab201.pub --dry-run
   ```

2. Read the output, then run it without `--dry-run`. Add the `--bridge-…` options if your bridge names differ.
3. Run `--action status`, then check `qm cloudinit dump` and `cloud-init status --long` for three machines.

**Expected result.** Twelve running machines with the Chapter 999 addresses and cloud-init `done`.

### Lab 12.3: Remove the build NICs and take the baseline

1. Run `./deploy-lab201-proxmox.sh --action remove-build-nics`. It removes `net0` from every machine, including the gateway.
2. Snapshot every machine:

   ```bash
   for id in $(seq 20101 20112); do qm snapshot "$id" baseline-201 --description 'Lab 999.6 baseline'; done
   ```

**Negative test.** From `static-1`, run `curl -m 5 https://cloud-images.ubuntu.com`. It must fail.

**Evidence.** The `status` output, `qm cloudinit dump 20102 network`, a tagged `tcpdump` capture on `gw-201`, and the failed `curl`.

### Cleanup

Run `./deploy-lab201-proxmox.sh --action remove`, delete the snippet files (`/var/lib/vz/snippets/lab201-*`), and delete `/var/tmp/lab201`.

## Lab Verification

Complete this sign-off once Labs 12.1 to 12.3 have been run end to end on a real Proxmox VE node with a real switch trunk. Until then the script is unverified. It passes `shellcheck`, and its machine and adapter planning was run as a dry run against stubs, but it has not been run on a node. The `import-from` form, the `trunks=2-4094` range, and the interaction of `--cicustom` with the cloud-init drive are the first things to confirm.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter built the lab on Proxmox VE. The bridges are a manual prerequisite, and the script then creates the twelve machines with `qm`, tags each adapter on a VLAN-aware bridge, imports the cloud image directly, and passes the shared seeds as cloud-init snippets. `gw-201` bridges the two trunks, so the host must not.

- [ ] Can create VLAN-aware trunk bridges and say why T1 and T2 stay in separate host bridges.
- [ ] Can explain `--cicustom` and check the result with `qm cloudinit dump`.
- [ ] Has run the script with `--dry-run` and then for real.
- [ ] Has removed the build NICs and taken the `baseline-201` snapshots.
- [ ] Can say where Proxmox differs from the VMware chapters.
