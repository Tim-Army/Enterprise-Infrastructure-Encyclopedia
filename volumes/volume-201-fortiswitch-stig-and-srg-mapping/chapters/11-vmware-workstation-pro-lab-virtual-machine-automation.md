# Chapter 11: Automating the Lab Virtual Machines in VMware Workstation Pro for Windows

## Learning Objectives

- Prepare the Virtual Network Editor with the five networks the lab needs, and say which one connects to which switch cable.
- Explain why Workstation needs the guests to create their own VLAN interfaces, and what that changes in the seed files.
- Run `Deploy-Lab201-Workstation.ps1` to import the cloud image, clone the twelve machines, write their `.vmx` settings, and start them.
- Test whether a Windows network adapter passes 802.1Q tags, and decide what to do if it does not.
- Remove the build adapters and take the `baseline-201` snapshots with `vmrun`.

## Theory and Architecture

### What Workstation changes

The twelve machines, their addresses, and their cloud-init seeds are the same as in [Chapter 09](09-esxi-7-8-and-9-lab-virtual-machine-automation.md). Read the machine table and the seed description there. Workstation differs in three ways.

1. **No VLAN-aware switch.** An ESXi port group, a Proxmox VLAN-aware bridge, and a vSphere distributed port group all add and remove VLAN tags for a machine. A Workstation virtual network (a *vmnet*) is a plain Layer 2 switch with no VLAN setting. The **guests** therefore create the VLAN interfaces themselves. The script renders the seeds with `--tagging guest`, so `svc-201a`'s adapter on trunk T1 gets a netplan VLAN interface (`nic1v10`) for VLAN 10, and the adapter itself carries tagged frames.
2. **Bridged networks reach the cable.** A vmnet bridged to a physical Windows adapter connects the machines to that adapter's cable. Each trunk is one vmnet bridged to the adapter that cables to a switch.
3. **The tool is `vmrun`.** Workstation has no PowerCLI. The script drives `vmrun.exe` (clone, start, stop), `ovftool.exe` (import the OVA), and `vmware-vdiskmanager.exe` (grow a disk), and edits each machine's `.vmx` file as text.

### The networks

Create these in the Virtual Network Editor (Edit, Virtual Network Editor, then *Change Settings*, which asks for administrator rights). Turn the DHCP service off on each lab network, because the lab has its own DHCP server.

| Lab network | Default vmnet | Type | Connects to |
| --- | --- | --- | --- |
| `lab201-t1` (trunk T1) | `vmnet2` | Bridged to one Windows adapter | The cable to `sw-648f-1` |
| `lab201-t2` (trunk T2) | `vmnet3` | Bridged to one Windows adapter | The cable to `sw-2048f-1` |
| `lab201-oob` (segment 0) | `vmnet4` | Bridged to one Windows adapter | The cables to the switch management ports |
| `lab201-lan220` (segment 220) | `vmnet5` | Host-only, DHCP off | No cable |
| `lab201-wan` (build) | `vmnet8` | NAT (the default NAT network) | The internet, through the host |

`vmnet0` is the automatic bridge to the host's primary adapter. The script treats `vmnet8` as NAT, `vmnet0` as automatic bridging, and every other name as a custom vmnet. You can pass different names with `-T1Vmnet`, `-T2Vmnet`, `-OobVmnet`, `-Lan220Vmnet`, and `-WanVmnet`.

### A caution about VLAN tags on Windows

For a trunk to work, 802.1Q tags must pass between the guest, the vmnet, the Windows adapter's driver, and the cable. Many Windows network drivers remove or block tags, and a driver setting (often called *Priority & VLAN*, or a registry value that stops VLAN stripping) controls it. This book has not tested which adapters pass tags, so treat the trunks as unproven until you run the test in Lab 11.2. If no adapter you own passes tags, use a USB or PCIe adapter whose driver does, or build the lab on [Chapter 12](12-proxmox-ve-lab-virtual-machine-automation.md) or [Chapter 09](09-esxi-7-8-and-9-lab-virtual-machine-automation.md).

### Workstation versions

The script needs `vmrun.exe`, `vmware-vdiskmanager.exe`, and `ovftool.exe`. Workstation Pro 17 puts all three under its install folder, in `OVFTool\` for the last. Whether the current release (25H2) still bundles OVF Tool was not confirmed when this chapter was written. If it does not, install OVF Tool separately and pass `-OvfToolPath`. Broadcom has made Workstation Pro available free of charge, and its terms for commercial use differ between sources, so read the current license terms before you use it for work.

## Design Considerations

- **Size.** The twelve machines take 17 vCPUs and 21.5 GiB of memory, so a Windows host needs about 32 GiB of memory and 250 GB of free disk, preferably on an SSD. On a smaller host, start `gw-201`, `svc-201a`, `svc-201b`, `admin-201`, and the machines a lab needs, and leave the others off.
- **Virtualization conflicts.** Workstation shares the CPU's virtualization support with Hyper-V, Windows Subsystem for Linux, and other Windows Hypervisor Platform users. It runs beside them, slower than on a host without them. If a machine will not start, check *Virtualization Based Security* and Hyper-V settings.
- **One full clone each.** The script clones full machines, not linked clones, because a linked clone depends on the base machine and the lab is meant to be moved and deleted as a set.
- **Static MAC addresses.** The `.vmx` files set `ethernetN.addressType = "static"` with the manifest's MAC addresses, which are in the range Workstation accepts for manual addresses (`00:50:56:00:00:00` to `00:50:56:3F:FF:FF`).
- **Edits happen to cloned files.** The script changes only the clones' `.vmx` files. The base machine `lab201-base` stays unmodified and is the source for every clone.
- **VMX is fragile.** A bad key can stop a machine from opening. The script keeps its changes small and does not back the file up, so if a machine will not open, delete it (`-Action Remove`) and deploy again.

## Implementation and Automation

### What the script does, in order

1. Finds `vmrun.exe`, `ovftool.exe`, and `vmware-vdiskmanager.exe`, and stops if one is missing.
2. Downloads the Ubuntu cloud image OVA and checks its SHA-256 sum.
3. Renders seed ISOs with `--guest-agent vmware --tagging guest`.
4. Imports the OVA once with `ovftool` as `lab201-base` under `-VmRoot`.
5. For each machine: `vmrun clone` to a new folder, then rewrite the clone's `.vmx` with the name, memory, CPU count, the network adapters (VMXNET 3, custom or NAT, the static MAC address), and the seed ISO on `ide1:0`, then grow the disk with `vmware-vdiskmanager -x`.
6. Starts `gw-201` first and then the rest, with `vmrun start ... nogui`.

### Parameters

| Parameter | Meaning |
| --- | --- |
| `-VmRoot` | Folder for the machines (default `D:\VMs\lab201`). |
| `-SshKeyFile` | Public key files for `labadmin`. |
| `-T1Vmnet`, `-T2Vmnet`, `-OobVmnet`, `-Lan220Vmnet`, `-WanVmnet` | The vmnet for each lab network. |
| `-WorkstationDir`, `-OvfToolPath` | Install locations, if not the defaults. |
| `-FlavorImages`, `-LicenseFile` | OVA paths for Linux flavors that publish none, and the license file for Red Hat and Ubuntu Pro keys (Chapter 09). The script imports one base machine for each flavor in use. |
| `-Action` | `Deploy` (default), `Status`, `RemoveBuildNics`, or `Remove`. |

`-WhatIf` is supported for every action that changes something.

## Validation and Troubleshooting

| Check | Command | Expected |
| --- | --- | --- |
| Machines exist and run | `.\Deploy-Lab201-Workstation.ps1 -Action Status` | Twelve machines, `running` |
| Cloud-init finished | On a machine: `cloud-init status --long` | `status: done` |
| Guest-tagged interfaces | On `svc-201a`: `ip -d link show nic1v10` | A VLAN interface with `id 10` |
| Addresses | `ip -br addr` | The Chapter 999 addresses, both families |
| Tags reach the cable | On `gw-201`: `sudo tcpdump -e -n -i nic2 vlan` while a switch sends traffic | Frames with `vlan` tags |

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `Not found: ...ovftool.exe` | OVF Tool is not part of this Workstation release | Install it and pass `-OvfToolPath` |
| `vmrun clone` fails | The base machine is running or has a snapshot problem | Power off `lab201-base`; delete its snapshots; rerun |
| A machine will not start | A bad `.vmx` key, or a vmnet that does not exist | Check `vmware.log` in its folder; create the vmnet; rerun with `-Action Remove` first |
| No tagged frames on `nic2` | The Windows driver strips tags | Change the adapter's VLAN setting, change adapters, or use another chapter's platform |
| Build adapter has no address | `vmnet8` is not NAT or its DHCP is off | Restore the default NAT network and its DHCP |
| Host is slow | Memory pressure | Start fewer machines; close other programs |

## Security and Best Practices

- **Bridged networks reach real cables.** A machine on `vmnet2`, `vmnet3`, or `vmnet4` shares those cables with the switches under test. Do not bridge a lab network to your production adapter, and use adapters that cable only to the lab.
- **NAT is the build path only.** `vmnet8` gives every machine internet access until you run `-Action RemoveBuildNics`. Run it as soon as the packages are installed.
- **Administrator rights.** The Virtual Network Editor needs them, and `vmrun` does not. Run the script as a normal user.
- **Protect the key and the folder.** The private key of `-SshKeyFile` stays out of the repository and the lab folders. `work\` holds the seeds. Delete it when you finish.
- **Isolate the host.** The lab holds test attackers. Do not enable Windows network sharing between the lab adapters and other adapters, and do not let Windows bridge them.
- **Keep Workstation current.** Hypervisor fixes matter on a host that also holds your other work.

## References and Knowledge Checks

**References:**

- Broadcom, VMware Workstation Pro documentation: the Virtual Network Editor, the `vmrun` command, and the `vmware-vdiskmanager` command.
- Broadcom, [VMware Workstation Pro 25H2 release information](https://www.neowin.net/amp/vmware-workstation-pro-25h2-is-out-with-new-command-line-tool-usb-32-support-and-more/) (a news summary; check Broadcom's release notes for the exact tools included).
- Broadcom, OVF Tool documentation.
- Canonical, [Ubuntu cloud images](https://cloud-images.ubuntu.com/noble/current/).
- [Chapter 09](09-esxi-7-8-and-9-lab-virtual-machine-automation.md) for the manifest and seeds, [Chapter 999](999-shared-lab-infrastructure.md) for the lab.

**Knowledge checks:**

1. Why can Workstation not give `svc-201a` an untagged adapter on VLAN 10 the way ESXi does?
2. Which `make-seed.py` option changes where the VLAN tag is applied, and what does it add to a machine's netplan?
3. What does a custom bridged vmnet need before it connects a machine to a switch?
4. A trunk shows no tagged frames in `tcpdump`. List two places the tags could be lost.
5. Why does the script clone full machines and not linked clones?

## Hands-On Lab

**Prerequisites.** A Windows 11 or Windows 10 host with VMware Workstation Pro, about 32 GiB of memory and 250 GB free, three adapters for T1, T2, and out-of-band (they can be USB adapters), PowerShell 7 or Windows PowerShell 5.1, Python 3.8 or later with `pip install pycdlib`, and an SSH key pair. Switch-side configuration is Chapter 999, Lab 999.3 and later.

### Lab 11.1: Create the networks

1. Open the Virtual Network Editor as administrator and create `vmnet2` and `vmnet3` as bridged networks, each bound to its own adapter, `vmnet4` as bridged to the out-of-band adapter, and `vmnet5` as host-only.
2. Turn the DHCP service off on all four. Leave `vmnet8` as the default NAT network.
3. In the adapter properties of each bridged Windows adapter, clear every protocol except *VMware Bridge Protocol*, so Windows does not use the adapter itself.

**Expected result.** Four lab networks and the NAT network exist, each with the right binding.

### Lab 11.2: Build the lab

1. Unpack the lab-scripts zip and open PowerShell in the `workstation` folder.
2. Run with `-WhatIf` and read the output, then run for real:

   ```powershell
   .\Deploy-Lab201-Workstation.ps1 -VmRoot D:\VMs\lab201 -SshKeyFile ~\.ssh\id_ed25519.pub
   ```

3. Run `-Action Status` until all twelve machines run, then check `cloud-init status --long` on three of them.
4. **Tag test.** With the switch trunk configured (Lab 999.3), run `sudo tcpdump -e -n -i nic2 vlan` on `gw-201`.

**Expected result.** Twelve running machines with the Chapter 999 addresses, and tagged frames in the capture. If the capture shows no tags, see the troubleshooting table before continuing.

### Lab 11.3: Remove the build adapters and take the baseline

1. Run `.\Deploy-Lab201-Workstation.ps1 -Action RemoveBuildNics`. It stops each machine, switches off adapter 0, and starts it again.
2. Snapshot each machine:

   ```powershell
   Get-ChildItem D:\VMs\lab201 -Recurse -Filter *.vmx | Where-Object { $_.BaseName -ne 'lab201-base' } |
     ForEach-Object { & 'C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe' -T ws snapshot $_.FullName baseline-201 }
   ```

**Negative test.** From `static-1`, run `curl -m 5 https://cloud-images.ubuntu.com`. It must fail.

**Evidence.** The `Status` output, the `tcpdump` lines with tags, `ip -d link show` from one machine, and the failed `curl`.

### Cleanup

Run `-Action Remove`. Delete `lab201-base`, `work\`, and the lab vmnets if you no longer need them.

## Lab Verification

Complete this sign-off once Labs 11.1 to 11.3 have been run end to end on a real Windows host with a real switch trunk. Until then the script is unverified. It was checked for syntax, and its `.vmx` rewriting was tested on a sample file, but it has not been run against Workstation. The behavior of OVF Tool in the current release, the `vmrun clone` of the imported machine, and whether the host's adapters pass 802.1Q tags are the first things to confirm.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter built the lab in Workstation Pro on Windows. Because a vmnet cannot add VLAN tags, the guests create the VLAN interfaces, and whether the trunks work depends on a Windows adapter that passes 802.1Q tags, which the lab must test. The script clones twelve full machines from one imported cloud image, rewrites each `.vmx` with static MAC addresses and the seed ISO, and starts them.

- [ ] Can say why Workstation needs guest tagging and what it changes in the seeds.
- [ ] Has created the five lab networks in the Virtual Network Editor.
- [ ] Has run the script, and checked for tagged frames on a trunk.
- [ ] Has removed the build adapters and taken the `baseline-201` snapshots.
- [ ] Knows which other chapter to use if no adapter passes tags.
