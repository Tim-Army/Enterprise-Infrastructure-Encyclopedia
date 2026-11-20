# Chapter 11: Automating the Lab Virtual Machines in VMware Workstation Pro for Windows

## Learning Objectives

- Prepare the Virtual Network Editor with the three networks the lab needs, and say why the trunk and the out-of-band network share the one bridged network.
- Explain why Workstation needs the guests to create their own VLAN interfaces, and what that changes in the seed files.
- Run `Deploy-Lab201-Workstation.ps1` to import the cloud image, clone the twelve machines, write their `.vmx` settings, and start them.
- Test whether a Windows network adapter passes 802.1Q tags, and decide what to do if it does not.
- Remove the build adapters and take the `baseline-201` snapshots with `vmrun`.

## Theory and Architecture

### What Workstation changes

The twelve machines, their addresses, and their cloud-init seeds are the same as in [Chapter 09](09-esxi-7-8-and-9-lab-virtual-machine-automation.md). Read the machine table and the seed description there. Workstation differs in three ways.

1. **No VLAN-aware switch.** An ESXi port group, a Proxmox VLAN-aware bridge, and a vSphere distributed port group all add and remove VLAN tags for a machine. A Workstation virtual network (a *vmnet*) is a plain Layer 2 switch with no VLAN setting. The **guests** therefore create the VLAN interfaces themselves. The script renders the seeds with `--tagging guest`, so `svc-201a`'s adapter on trunk T1 gets a netplan VLAN interface (`nic1v2`) for VLAN 2, and the adapter itself carries tagged frames.
2. **Bridged networks reach the cable.** A vmnet bridged to a physical Windows adapter connects the machines to that adapter's cable. Workstation supports one bridged network, so the lab uses one: the trunk and the out-of-band network share it, and trunks T1 and T2 become a single trunk. The gateway then has one trunk adapter. Two trunk adapters on one bridged network would make the gateway bridge them into a loop.
3. **The tool is `vmrun`.** Workstation has no PowerCLI. The script drives `vmrun.exe` (clone, start, stop), `ovftool.exe` (import the OVA), and `vmware-vdiskmanager.exe` (grow a disk), and edits each machine's `.vmx` file as text.

### The networks

Create these in the Virtual Network Editor (Edit, Virtual Network Editor, then *Change Settings*, which asks for administrator rights). Turn the DHCP service off on each lab network, because the lab has its own DHCP server.

| Lab network | Default vmnet | Type | Connects to |
| --- | --- | --- | --- |
| `lab201-t1` (the one trunk) and `lab201-oob` (segment 0) | `vmnet0` | Bridged to one Windows adapter | A switch port that carries the lab VLANs as tags and the out-of-band network untagged, and reaches both switches |
| `lab201-mcast` (segment 12) | `vmnet5` | Host-only, DHCP off | No cable |
| `lab201-wan` (build) | `vmnet8` | NAT (the default NAT network) | The internet, through the host |

`vmnet0` is the automatic bridge to the host's primary adapter. The script treats `vmnet8` as NAT, `vmnet0` as automatic bridging, and every other name as a custom vmnet. You can pass different names with `-BridgeVmnet`, `-McastVmnet`, and `-WanVmnet`. The script stops if the manifest still has a second trunk (`lab201-t2`), so generate the manifest with the Lab Builder for Workstation, which merges T1 and T2.

### A caution about VLAN tags on Windows

For a trunk to work, 802.1Q tags must pass between the guest, the vmnet, the Windows adapter's driver, and the cable. Many Windows network drivers remove or block tags, and a driver setting (often called *Priority & VLAN*, or a registry value that stops VLAN stripping) controls it. This book has not tested which adapters pass tags, so treat the trunks as unproven until you run the test in Lab 11.2. If no adapter you own passes tags, use a USB or PCIe adapter whose driver does, or build the lab on [Chapter 12](12-proxmox-ve-lab-virtual-machine-automation.md) or [Chapter 09](09-esxi-7-8-and-9-lab-virtual-machine-automation.md).

### Workstation versions

The script needs `vmrun.exe`, `vmware-vdiskmanager.exe`, and `ovftool.exe`. Workstation Pro 17 puts all three under its install folder, in `OVFTool\` for the last. Workstation 26.0 installs under `C:\Program Files\VMware\VMware Workstation` instead of `Program Files (x86)`, and one 26.0.0 install that was checked has all three tools there, with OVF Tool in `OVFTool\`. The script looks in both folders, and `-WorkstationDir` names another one. On Workstation Pro 17, use the `Program Files (x86)` path in the snapshot command of Lab 11.3. Whether 25H2 bundles OVF Tool was not confirmed when this chapter was written. If it does not, install OVF Tool separately and pass `-OvfToolPath`. Broadcom has made Workstation Pro available free of charge, and its terms for commercial use differ between sources, so read the current license terms before you use it for work.

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
| `-VmRoot` | Folder for the machines. Without it, the script uses a `lab201` folder inside Workstation's default folder for virtual machines (the one set in Preferences, or `Documents\Virtual Machines`) and prints the path. |
| `-SshKeyFile` | Public key files for `labadmin`. |
| `-BridgeVmnet`, `-McastVmnet`, `-WanVmnet` | The bridged vmnet (trunk and out-of-band), the host-only vmnet for segment 12, and the build vmnet. |
| `-WorkstationDir`, `-OvfToolPath` | Install locations, if not the defaults. |
| `-FlavorImages`, `-LicenseFile` | OVA paths for Linux flavors that publish none, and the license file for Red Hat and Ubuntu Pro keys (Chapter 09). The script imports one base machine for each flavor in use. The ISO-based flavors (Windows, Linux Mint, Tiny Core) are not available here, because Workstation has no VLAN-aware switch and those guests cannot tag the trunks. |
| `-Action` | `Deploy` (default), `Check`, `Status`, `RemoveBuildNics`, `Snapshot`, `Restore`, or `Remove`. `Check` changes nothing: it tests Python and `pycdlib`, the SSH key, the Workstation tools, the manifest, memory, disk space, and the networks, and says how to fix what is missing. `Status` lists each machine, its state, whether its first boot has finished, and the `ssh` line that logs in to it. `Snapshot` takes the baseline snapshot of every machine, and refuses while a machine still has its build adapter (adapter 0). `Restore` returns every machine to that snapshot and starts it. |
| `-Wait`, `-WaitMinutes` | With `-Action Status`: keep checking until every machine reports that its first boot has finished, for at most `-WaitMinutes` (30 by default). Each machine hands its state to Workstation through VMware Tools about once a minute, as the guest variable `lab201`, and `vmrun readVariable` reads it with no login. If no machine reports within six minutes, the wait stops and says so. |
| `-SnapshotName` | The snapshot that `Snapshot` and `Restore` use. The default is `baseline-201`. |
| `-AddToLibrary` | Opens each machine in Workstation after the build, which lists it in the Library. Not tested yet. |

`-WhatIf` is supported for every action that changes something.

## Validation and Troubleshooting

| Check | Command | Expected |
| --- | --- | --- |
| Machines exist and run | `.\Deploy-Lab201-Workstation.ps1 -Action Status` | Twelve machines, `running` |
| The first boot finished | The same command with `-Wait` | `ok` in the Build column of every machine. `failed` names a missing package or a lab service that does not run |
| Cloud-init finished | On a machine: `lab201-status`, then `cloud-init status --long` | A line that starts `lab201 ok`, and `status: done` |
| Guest-tagged interfaces | On `svc-201a`: `ip -d link show nic1v2` | A VLAN interface with `id 2` |
| Addresses | `ip -br addr` | The Chapter 999 addresses, both families |
| Tags reach the cable | On `gw-201`: `sudo tcpdump -e -n -i nic2 vlan` while a switch sends traffic | Frames with `vlan` tags |

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `Not found: ...ovftool.exe` | OVF Tool is not part of this Workstation release | Install it and pass `-OvfToolPath` |
| `vmrun clone` fails | The base machine is running or has a snapshot problem | Power off `lab201-base`; delete its snapshots; rerun |
| The machines run but are not in the Workstation library | `vmrun` does not add machines to the library | Right-click **My Computer** in the Library, choose **Scan for Virtual Machines**, and pick the machines folder that the script printed |
| Workstation warns that `preset` is not a valid value for `powerType.powerOff` | The imported cloud image carries that setting, and Workstation uses `soft` instead | Harmless. The script removes the `powerType` settings from each machine it builds |
| A machine will not start | A bad `.vmx` key, or a vmnet that does not exist | Check `vmware.log` in its folder; create the vmnet; rerun with `-Action Remove` first |
| No tagged frames on `nic2` | The Windows driver strips tags | Change the adapter's VLAN setting, change adapters, or use another chapter's platform |
| Build adapter has no address | `vmnet8` is not NAT or its DHCP is off | Restore the default NAT network and its DHCP |
| Host is slow | Memory pressure | Start fewer machines; close other programs |

## Security and Best Practices

- **Bridged networks reach real cables.** A machine on the bridged network shares that cable with the switches under test. Do not bridge the lab to your production adapter, and use an adapter that cables only to the lab.
- **NAT is the build path only.** `vmnet8` gives every machine internet access until you run `-Action RemoveBuildNics`. Run it as soon as the packages are installed. When the manifest has `uplink` (the **Uplink** box of the Lab Builder, [Chapter 09](09-esxi-7-8-and-9-lab-virtual-machine-automation.md)), `RemoveBuildNics` and `Snapshot` leave adapter 0 of the gateway on, because it is the uplink to the external firewall.
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

1. Why can Workstation not give `svc-201a` an untagged adapter on VLAN 2 the way ESXi does?
2. Which `make-seed.py` option changes where the VLAN tag is applied, and what does it add to a machine's netplan?
3. What does a custom bridged vmnet need before it connects a machine to a switch?
4. A trunk shows no tagged frames in `tcpdump`. List two places the tags could be lost.
5. Why does the script clone full machines and not linked clones?

## Hands-On Lab

**Prerequisites.** A Windows 11 or Windows 10 host with VMware Workstation Pro, about 32 GiB of memory and 250 GB free, one adapter for the bridged lab network (it can be a USB adapter), PowerShell 7 or Windows PowerShell 5.1, Python 3.8 or later with `pip install pycdlib`, and an SSH key pair. Switch-side configuration is Chapter 999, Lab 999.3 and later.

### Lab 11.1: Create the networks

1. Open the Virtual Network Editor as administrator. Bind the bridged network `vmnet0` to the lab adapter instead of leaving it on automatic, and create `vmnet5` as host-only.
2. Turn the DHCP service off on `vmnet5`. Leave `vmnet8` as the default NAT network.
3. In the adapter properties of the bridged Windows adapter, clear every protocol except *VMware Bridge Protocol*, so Windows does not use the adapter itself.

**Expected result.** Four lab networks and the NAT network exist, each with the right binding.

### Lab 11.2: Build the lab

1. Unpack the lab-scripts zip and open PowerShell in the `workstation` folder.
2. Run with `-WhatIf` and read the output, then run for real:

   ```powershell
   .\Deploy-Lab201-Workstation.ps1 -SshKeyFile ~\.ssh\id_ed25519.pub
   ```

3. Run `.\Deploy-Lab201-Workstation.ps1 -Action Status -Wait`. It ends when every machine reports that its first boot has finished, and prints the line that logs in to each. Then check `lab201-status` and `cloud-init status --long` on three of them. If no machine reports its state, that check by hand is the one to rely on.
4. **Tag test.** With the switch trunk configured (Lab 999.3), run `sudo tcpdump -e -n -i nic2 vlan` on `gw-201`.

**Expected result.** Twelve running machines with the Chapter 999 addresses, and tagged frames in the capture. If the capture shows no tags, see the troubleshooting table before continuing.

### Lab 11.3: Remove the build adapters and take the baseline

1. Run `.\Deploy-Lab201-Workstation.ps1 -Action RemoveBuildNics`. It stops each machine, switches off adapter 0, and starts it again.
2. Snapshot each machine. The script finds the machines folder itself, the one it printed as `Machines folder`. It refuses, and names the machines, if adapter 0 is still on in one of them:

   ```powershell
   .\Deploy-Lab201-Workstation.ps1 -Action Snapshot
   ```

3. Between labs, return every machine to that snapshot. It discards what changed on the machines since the snapshot. `vmrun` leaves a reverted machine suspended, so the script starts it again:

   ```powershell
   .\Deploy-Lab201-Workstation.ps1 -Action Restore
   ```

**Negative test.** From `static-1`, run `curl -m 5 https://cloud-images.ubuntu.com`. It must fail.

**Evidence.** The `Status` output, the `tcpdump` lines with tags, `ip -d link show` from one machine, and the failed `curl`.

### Cleanup

Run `-Action Remove`. Delete `lab201-base`, `work\`, and the lab vmnets if you no longer need them.

## Lab Verification

Complete this sign-off once Labs 11.1 to 11.3 have been run end to end on a real Windows host with a real switch trunk. Until then the labs are not signed off. The script itself has been run: on a Windows computer with Workstation Pro 26 and Python 3.15, it built and started all the lab machines from a Lab Builder zip whose values had been changed on the page, and a Claude Code session started from the zip's `CLAUDE.md` began at Lab 999.1. That run found four things the script and this chapter now cover: Workstation 26 installs under `Program Files`, a computer may have no `D:` drive, `python` can be the Microsoft Store stub, and `vmrun` does not add the machines to the Workstation library. Not yet run: the trunk to the hardware switches (whether the host's adapter passes 802.1Q tags), `-Action RemoveBuildNics`, and the labs themselves. The `Status -Wait`, `Snapshot`, and `Restore` actions were added after that run and have not been run against machines. `Snapshot` was run against stand-in `.vmx` files only: it refused while adapter 0 was on in one of them, and with `-WhatIf` it listed the machines once adapter 0 was off in all of them. The first thing to confirm for `Status -Wait` is that `vmrun readVariable` returns the build state a machine hands to Workstation.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter built the lab in Workstation Pro on Windows. Because a vmnet cannot add VLAN tags, the guests create the VLAN interfaces, and whether the trunks work depends on a Windows adapter that passes 802.1Q tags, which the lab must test. The script clones twelve full machines from one imported cloud image, rewrites each `.vmx` with static MAC addresses and the seed ISO, and starts them.

- [ ] Can say why Workstation needs guest tagging and what it changes in the seeds.
- [ ] Has created the five lab networks in the Virtual Network Editor.
- [ ] Has run the script, and checked for tagged frames on a trunk.
- [ ] Has removed the build adapters and taken the `baseline-201` snapshots.
- [ ] Knows which other chapter to use if no adapter passes tags.
