# Chapter 10: Automating the Lab Virtual Machines Through VMware vCenter 7, 8, and 9

## Learning Objectives

- Explain what vCenter adds to the build in [Chapter 09](09-esxi-7-8-and-9-lab-virtual-machine-automation.md): templates and clones, folders, and distributed switches.
- Choose between standard and distributed switches for the lab trunks, and set the distributed switch version that matches vCenter 7 or vCenter 8.
- Run `Deploy-Lab201-Vcenter.ps1` against a vCenter Server, then check, adjust, and snapshot the twelve lab machines.
- Keep the lab machines on the one host that owns the trunk NICs, and prevent a cluster from moving them.
- Say how vCenter 7 and vCenter 8 differ for this build: distributed switch version, virtual hardware version, and support status.

## Theory and Architecture

### What changes when vCenter manages the host

[Chapter 09](09-esxi-7-8-and-9-lab-virtual-machine-automation.md) builds the lab on a standalone host. The manifest, the machine list, the MAC addresses, the cloud-init seeds, and the gateway that bridges the two trunks are the same here, so this chapter covers only what vCenter changes. Read Chapter 09 first for those.

| Item | Standalone ESXi (Chapter 09) | Through vCenter (this chapter) |
| --- | --- | --- |
| Creating a machine | Imports the OVA once for each machine | Imports the OVA once as a template, then clones it |
| Where machines live | The host's root folder | A `lab201` folder in the datacenter |
| Switches | Standard switches only | Standard switches, or one distributed switch for each network |
| License | Needs a license that allows API writes | vCenter manages licensed hosts, and the free ESXi license cannot be managed by vCenter |
| Virtual hardware version | Chosen from the host's version | Chosen from the host's version, with the vCenter version checked first |

### One host owns the trunks

The two trunks and the out-of-band network are cables to physical NICs, and a physical NIC belongs to one host. The lab machines therefore all run on **one host**, named by `-VMHostName`, even when that host is in a cluster. The script puts every machine on that host. Two settings stop the cluster from undoing that:

- Set the DRS automation level for the `lab201` machines to manual, or add a VM-Host rule that keeps them on the host (Cluster, Configure, VM/Host Rules).
- Do not vMotion them. A machine moved to a host without the trunk NICs loses its trunk, with no error.

### Standard or distributed switches

With `-NetworkType Standard` the script creates the same standard switches and port groups as Chapter 09, on the one host. That is the simplest choice.

With `-NetworkType Distributed` it creates one distributed switch for each network (`dvs-lab201-t1`, `dvs-lab201-t2`, and so on), adds the host, attaches the uplink NIC to the switch, and creates distributed port groups. The gateway's trunk port groups are VLAN trunks with the range `0-4094`, and have the same promiscuous, forged transmit, and MAC change settings. A distributed switch lets you add more hosts later and see the lab in one place, but it moves a physical NIC to the distributed switch, which cannot be undone while machines use it.

**Distributed switch version.** A distributed switch has its own version, which must not exceed what the hosts and vCenter support.

| Platform | Default `-VdsVersion` | Notes |
| --- | --- | --- |
| vCenter 7.0 | `7.0.3` | Supported by vCenter 7.0 U3 and ESXi 7.0 U3 hosts. Use `7.0.0` for an earlier update |
| vCenter 8.0 | `8.0.0` | Works with every 8.0 update. Newer versions exist in later updates, so raise it only if you need a feature |
| vCenter 9.0 | `9.0.0` | Version 9.0.0 needs ESX 9.0 hosts. Broadcom's article on distributed switch versions lists the features of each version |

Pass `-VdsVersion` to override. A lower version is always safe, and a higher one than the hosts support fails at the `New-VDSwitch` step.

### vCenter 7, 8, and 9

| Item | vCenter 7.0 | vCenter 8.0 | vCenter 9.0 |
| --- | --- | --- | --- |
| `-VsphereVersion` check | vCenter must report `7.*` | vCenter must report `8.*` | vCenter must report `9.*` |
| Virtual hardware version | `vmx-19` (7.0 U2 and later) | `vmx-20` (8.0 and U1), `vmx-21` (8.0 U2 and U3) | `vmx-22` |
| Distributed switch version | `7.0.3` | `8.0.0` | `9.0.0` |
| Support status | End of general support 2 October 2025 | Supported | Current release; licensed only through vSphere Foundation or Cloud Foundation |
| PowerCLI | 13.3 | 13.3 | The release that supports vSphere 9 (VCF PowerCLI) |

A vCenter of one major version can manage hosts of the previous version, so the script checks the **vCenter** version against `-VsphereVersion` and takes the hardware version from the **host** it deploys to. Do not mix: deploy ESXi 7 hosts under a vCenter 8 only if you pass a `-HardwareVersion` the host supports.

### Dell VxRail

Dell VxRail runs vSphere and vSAN on Dell nodes and is managed by VxRail Manager. VxRail 8.0.x runs vSphere 8 and VxRail 9.0.x runs vSphere 9, so the same script builds the lab on it. VxRail needs three changes, which the script has as options and the [Lab Builder](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-201-fortiswitch-stig-and-srg-mapping/lab-scripts/builder/lab-builder.html) sets when you choose Dell VxRail.

- **An existing switch.** `-UseExistingSwitch <name>` reuses VxRail's distributed switch and adds only port groups to it (`lab201-...`). The script changes no switch, uplink, or physical NIC, and `-NoUplinkChanges` confirms that. VxRail Manager owns the uplinks.
- **A cluster, not a host.** `-ClusterName` places the machines in the cluster, so they can run on any host. The script imports the template through the first connected host. Cable the trunk uplinks on every host, or keep the lab on one host with a VM-Host rule, because a machine that moves to a host with no trunk loses it.
- **One trunk.** VxRail has one set of uplinks, and `gw-201` bridges its trunk adapters, so two trunks on the same uplinks would loop. The Builder rewrites the manifest with one trunk: T1 and T2 become one network, the gateway has one trunk adapter, and the peers' second links (VLANs 2003 and 2004) use it too. Both hardware switches must then reach the VxRail uplinks, for example through an external trunk.

Storage goes on the vSAN datastore, and with the default mirroring policy the thin disks can use about twice their size in raw space. VxRail 9.0.x needs vSphere 9 and vSAN licenses managed through VCF Operations, and Dell's knowledge base says perpetual licenses from 8.x do not carry over. Do not upgrade vCenter or ESXi outside VxRail Manager. None of this has been run on a VxRail.

## Design Considerations

- **Template first.** The script imports the OVA once into `lab201-ubuntu-template` and converts it to a template. Clones are quick and use thin disks. If you already keep an Ubuntu template, change `$tplName` in the script.
- **Folder, not resource pool.** A VM folder (`lab201`) keeps the machines together and makes `-Action Status` and `-Action Remove` simple. Use a resource pool as well if the cluster is busy.
- **Permissions.** Run the script as an account whose role can create virtual machines, upload to the datastore, assign networks, and, for distributed switches, create and modify them. A lab role is better than an administrator. Check the privilege list in the vSphere documentation for your version before you build the role.
- **Content Library.** A content library can hold the template and share it between vCenters. The script does not use one, to keep the sample short.
- **Management network.** Never give the script the physical NIC that carries the host's management or vCenter traffic. A mistake there disconnects the host and can leave vCenter unable to reach it.
- **Same data as Chapter 09.** The manifest, the MAC addresses, and the `lab201-seeds` ISO folder on the datastore are identical, so a lab built under vCenter can be rebuilt on a standalone host by running Chapter 09's script against the same manifest.

## Implementation and Automation

### What the script does, in order

1. Connects to vCenter and checks that its version matches `-VsphereVersion`.
2. Finds the datacenter, host, and datastore, and chooses the virtual hardware version and the distributed switch version.
3. Creates the `lab201` folder.
4. Creates the networks, as standard or distributed switches. Trunk networks get the promiscuous, forged transmit, and MAC change settings.
5. Downloads the OVA (checking its SHA-256 sum) and imports it as the template.
6. Renders the seed ISOs with `--guest-agent vmware --tagging hypervisor`.
7. For each machine: clones the template onto the host and datastore, sets the CPU and memory, grows the disk, replaces the adapters with VMXNET 3 adapters that have the manifest's MAC addresses, uploads the seed ISO to `lab201-seeds/`, and attaches it.
8. Powers on `gw-201` first, then the rest.

### Parameters that differ from Chapter 09

| Parameter | Meaning |
| --- | --- |
| `-VcenterServer` | The vCenter Server name or address. |
| `-Datacenter`, `-VMHostName` | The datacenter and the host that owns the trunk NICs. |
| `-FolderName` | The VM folder (default `lab201`). |
| `-NetworkType` | `Standard` (default) or `Distributed`. |
| `-VdsVersion` | Distributed switch version, if you need to override the default. |
| `-ClusterName`, `-UseExistingSwitch`, `-NoUplinkChanges` | Dell VxRail and other managed clusters (see above). |
| `-LicenseFile`, `-FlavorImages` | The license file, and OVA paths for flavors that publish none (Chapter 09). |

The other parameters (`-VsphereVersion`, `-SshKeyFile`, `-Datastore`, the four `-…Nic` uplinks, `-Action`, `-HardwareVersion`, `-SkipCertificateCheck`) work as in Chapter 09, and the actions `Status`, `RemoveBuildNics`, and `Remove` do the same.

Example for vCenter 8 with distributed switches:

```powershell
.\Deploy-Lab201-Vcenter.ps1 -VcenterServer <VCENTER> -Datacenter <DATACENTER> -VMHostName <HOST> `
  -Datastore <DATASTORE> -VsphereVersion 8 -NetworkType Distributed -SshKeyFile ~\.ssh\id_ed25519.pub `
  -Trunk1Nic vmnic1 -Trunk2Nic vmnic2 -OobNic vmnic3 -WanNic vmnic0 -WhatIf
```

## Validation and Troubleshooting

The checks in Chapter 09 (cloud-init status, hostnames, addresses, the gateway bridge) apply unchanged. Add these for vCenter.

| Check | Command | Expected |
| --- | --- | --- |
| Template exists | `Get-Template lab201-ubuntu-template` | One template |
| Machines are in the folder | `.\Deploy-Lab201-Vcenter.ps1 -Action Status -VcenterServer <VCENTER>` | Twelve machines in `lab201` |
| Distributed switch version | `Get-VDSwitch dvs-lab201-t1 \| Select Name, Version` | `7.0.3` or `8.0.0` unless you overrode it |
| Trunk policy | `Get-VDPortgroup lab201-t1-trunk \| Get-VDSecurityPolicy` | Promiscuous, forged transmits, MAC changes all allowed |
| Machines stay put | `Get-VM -Location lab201 \| Select Name, VMHost` | The single host in every row |

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `vCenter reports version 8.0.3, but -VsphereVersion is 7` | Wrong `-VsphereVersion` | Pass the vCenter's major version |
| `New-VDSwitch` fails on `-Version` | The version is higher than a host supports | Pass a lower `-VdsVersion` |
| `Add-VDSwitchPhysicalNetworkAdapter` fails | The NIC is in use by another switch | Pick a spare NIC and remove it from its other switch first |
| Clone fails with a hardware version error | The template's hardware version is above the host's | Pass a lower `-HardwareVersion` and rebuild the template (`Remove-Template lab201-ubuntu-template`) |
| A machine loses its trunk after a cluster event | DRS or HA moved it | Add the VM-Host rule and set DRS to manual |
| Cannot upload the seed ISO | The account lacks datastore privileges | Add the *Datastore, Low level file operations* privilege to the role |

## Security and Best Practices

Everything in Chapter 09's security section applies. In addition:

- **Least privilege.** Give the build account the privileges the script uses and no more, scoped to the lab folder and the one host. Remove or disable the account when the build is done.
- **vCenter as a target.** The credentials you type can administer the whole vCenter. Prefer a dedicated lab vCenter, and never reuse a production vCenter's administrator account.
- **Distributed switch changes are shared.** A distributed switch is a vCenter object, so a mistake in the trunk policy is visible to every host that uses it. The script gives each network its own switch to limit that.
- **Template hygiene.** The template holds the cloud image with no machine identity. Do not power it on, and delete it (and the `work/` folder) when the lab is retired, because it is a copy of a general-purpose image that will age.
- **Patch level.** Run a vCenter and hosts that still receive fixes. vSphere 7 reached end of general support on 2 October 2025, so a lab on 7 needs another control, such as isolation from other networks, and no production data.

## References and Knowledge Checks

**References:**

- Broadcom, [End of General Support for vSphere 7.0](https://knowledge.broadcom.com/external/article/415405/end-of-general-support-for-vsphere.html).
- Broadcom, VMware PowerCLI documentation and [PowerCLI 13.3 release notes](https://docs.vmware.com/en/VMware-PowerCLI/latest/rn/powercli-133-release-notes.html); `New-VDSwitch`, `New-VDPortgroup`, `Import-VApp`, and `New-VM` cmdlet references.
- Broadcom, VMware Product Interoperability Matrix, for the vCenter and ESXi combinations you run, and the virtual hardware versions article.
- Broadcom, [VDS Improvements and Features per Version](https://knowledge.broadcom.com/external/article/416520), for the distributed switch versions through 9.0.0.
- Broadcom, vSphere documentation on distributed switch versions and VLAN trunking on distributed port groups.
- [Chapter 09](09-esxi-7-8-and-9-lab-virtual-machine-automation.md) for the manifest, seeds, and gateway design, and [Chapter 999](999-shared-lab-infrastructure.md) for the lab itself.

**Knowledge checks:**

1. Why must all twelve machines run on one host, even if the cluster has several?
2. A vCenter 8 manages an ESXi 7.0 U3 host. Which version decides the distributed switch version, and which the hardware version?
3. What does a distributed port group's VLAN trunk range do that VLAN ID 4095 on a standard port group also does?
4. Name two actions that would silently disconnect a machine from the trunk after the build.
5. Why does the script give each lab network its own distributed switch?

## Hands-On Lab

**Prerequisites.** A vCenter Server 7, 8, or 9, one ESXi host it manages with four spare physical NICs, a datastore with 250 GB free, the account and role described above, and the same client tools as Chapter 09 (PowerShell 7, PowerCLI, Python with `pycdlib`, an SSH key pair).

### Lab 10.1: Preview the build

1. Unpack the lab-scripts zip and open PowerShell in the `vcenter` folder.
2. Run the script with `-WhatIf`, using `-NetworkType Standard`. Read every line.

**Expected result.** The folder, the six networks and port groups, the template, and twelve clones are listed, and nothing is created.

### Lab 10.2: Build with standard switches

1. Run the command without `-WhatIf`.
2. Run `-Action Status` until every machine reports an address.
3. On `gw-201`, run `bridge link` and `ip -br addr show type vlan`.

**Expected result.** Twelve machines in the `lab201` folder, each with the Chapter 999 addresses, and `gw-201` showing both trunks in `br-trunk`.

### Lab 10.3: Keep the lab on its host and take the baseline

1. Add a VM-Host rule (or set DRS to manual) for the `lab201` folder.
2. Run `-Action RemoveBuildNics`.
3. Snapshot every machine as `baseline-201`.

**Negative test.** Try a vMotion of `svc-201a` to another host. The rule or the manual DRS level must stop it, or you must see the trunk fail on arrival.

### Lab 10.4 (optional): Rebuild with distributed switches

1. Run `-Action Remove`, then deploy again with `-NetworkType Distributed`.
2. Confirm `Get-VDSwitch` shows the version for your vCenter.

**Evidence.** The `Status` output, the `bridge link` output, the VM-Host rule, and the refused or failed vMotion.

### Cleanup

Run `-Action Remove`. Delete the template, the `lab201` folder, the `lab201-seeds` folder on the datastore, the standard or distributed switches, and the local `work/` folder.

## Lab Verification

Complete this sign-off once Labs 10.1 to 10.3 have been run end to end under a real vCenter 7 and a real vCenter 8. Until then the script is unverified. It was written against the PowerCLI documentation and checked for syntax and for the shared seed output only. The distributed switch version defaults, the clone of the imported template, and the trunk security policy on distributed port groups are the first things to confirm.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter built the same twelve lab machines through vCenter. The script imports the cloud image once as a template, clones each machine into a `lab201` folder on the one host that owns the trunk NICs, and builds standard or distributed switches, with the distributed switch version matched to vCenter 7 or 8. The host-pinning rule matters more than the switch type, because a cluster that moves a machine breaks its trunk without an error.

- [ ] Can say what vCenter adds to the Chapter 09 build.
- [ ] Can choose standard or distributed switches and set the distributed switch version for vCenter 7, 8, and 9.
- [ ] Has built the lab through vCenter and confirmed the machines stay on one host.
- [ ] Has removed the build adapters and taken the `baseline-201` snapshots.
- [ ] Can explain why vSphere 7's support status changes how the lab should be isolated.
