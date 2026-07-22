# Chapter 08: Deploying the Virtual Machines

## Learning Objectives

- Create each of the nine virtual machines with its exact parameters.
- Place each VM on its assigned VLAN using the VLAN-aware bridge.
- Assign each VM its fixed address, gateway, and hostname.
- Distinguish installer-ISO VMs from imported-appliance VMs.
- Verify every VM reaches its gateway on the correct VLAN.

## Theory and Architecture

### The nine machines and their addressing

This chapter deploys the workload the whole build has been leading to: nine
virtual machines, each from an image in the
[Chapter 07](07-building-the-iso-library.md) library, each on its assigned
VLAN through the [Chapter 05](05-network-architecture-management-nic-vlan-trunk-and-bridges.md)
bridge, with a fixed address:

| VM | Hostname | IP | Gateway | VLAN |
| --- | --- | --- | --- | --- |
| Ubuntu Desktop | `ubuntu1` | 10.30.12.100/24 | 10.30.12.1 | 6 |
| Ubuntu Server | `ubuntu-server1` | 10.30.10.100/24 | 10.30.10.1 | 3 |
| EVE-ng | `eve-ng` | 10.30.10.85/24 | 10.30.10.1 | 3 |
| GNS3 | `gns3` | 10.30.10.86/24 | 10.30.10.1 | 3 |
| Cisco CML | `cml` | 10.30.10.87/24 | 10.30.10.1 | 3 |
| Red Hat Desktop | `rhel-desktop1` | 10.30.12.101/24 | 10.30.12.1 | 6 |
| Red Hat Server | `rhel-server1` | 10.30.10.88/24 | 10.30.10.1 | 3 |
| Windows 11 | `win11-1` | 10.30.12.102/24 | 10.30.12.1 | 6 |
| Windows Server | `win-server1` | 10.30.10.89/24 | 10.30.10.1 | 3 |

The pattern is consistent: **VLAN 6 machines** (`ubuntu1`, `rhel-desktop1`,
`win11-1`) are the desktops on 10.30.12.0/24; **VLAN 3 machines** (everything
else) are the servers on 10.30.10.0/24, gateway 10.30.10.1.

### Two corrections carried into this chapter

The addressing above reflects the two corrections applied to the original
specification, stated again here because this is where they land:

- **Windows Server is `win-server1` at 10.30.10.89**, not 10.30.10.88. The
  original specification assigned .88 to both Red Hat Server and Windows
  Server; Red Hat Server keeps .88 and Windows Server moves to .89. Deploying
  both at .88 would be an immediate duplicate-address conflict on VLAN 3.
- **EVE-ng is on VLAN 3.** The original specification gave EVE-ng no VLAN;
  since it sits on the 10.30.10.0/24 server subnet, it belongs on VLAN 3 with
  the other server machines.

### VLAN tagging at the virtual NIC

A VM is placed on a VLAN by setting a **VLAN tag** on its virtual network
interface, attached to the VLAN-aware bridge `vmbr1`. The bridge and the
trunk carry that tag out to the switch, so a VM tagged VLAN 3 lands on
10.30.10.0/24 and one tagged VLAN 6 on 10.30.12.0/24. The address itself is
set *inside* the guest OS during or after installation; the VLAN tag on the
virtual NIC is what puts the guest on the right layer-2 network to reach that
address's gateway.

### Installer ISOs versus imported appliances

Most of the nine are installed from an ISO — you attach the installer,
boot, and run setup. Two are different:

- **GNS3** and **EVE-ng** are **appliances** (Chapter 07). They are imported
  as existing disks/appliances rather than installed from an OS installer.

The VM-creation procedure differs slightly for these: an installer VM boots
its ISO into setup; an appliance VM is created around an imported disk.

## Design Considerations

- **Set the VLAN tag on the virtual NIC to match the intended subnet.** A VM
  on VLAN 3 must be tagged 3 to reach 10.30.10.1; tagging it 6 would put it on
  the desktop network with the wrong gateway. The tag and the in-guest
  address must agree.
- **Give each VM sane resources for its role.** The desktops and servers need
  modest CPU/RAM; the network-emulation VMs (EVE-ng, GNS3, CML) are
  resource-hungry and benefit from nested virtualization enabled and generous
  RAM. Size them to their job.
- **Enable nested virtualization for the emulators.** EVE-ng, GNS3, and CML
  run virtual devices *inside* the VM, which requires the host to expose
  virtualization extensions to the guest. Without it, those platforms run
  slowly or not at all.
- **Use consistent naming.** VM names matching the hostnames (`ubuntu1`,
  `cml`, `win-server1`) keep the inventory legible and reduce the chance of
  configuring the wrong machine.
- **Store every VM disk on `river`.** The VM datastore from Chapter 06 is the
  target for all nine; none belong on the boot mirror.

## Implementation and Automation

### 1. Creating an installer-ISO VM

The pattern for an installer VM (shown for Ubuntu Server, applied to each ISO
machine), via the web UI (Create VM) or `qm`:

```bash
# Create the VM shell with a disk on river and a NIC on the VLAN-aware
# bridge tagged to the machine's VLAN. Example: ubuntu-server1, VLAN 3.
qm create 110 --name ubuntu-server1 --memory 4096 --cores 2 \
  --scsihw virtio-scsi-single \
  --scsi0 river-vm:32 \
  --net0 virtio,bridge=vmbr1,tag=3 \
  --ide2 river-iso:iso/ubuntu-<ver>-live-server-amd64.iso,media=cdrom \
  --boot order=ide2

qm start 110
# Then run the OS installer in the console and set, inside the guest:
#   address 10.30.10.100/24, gateway 10.30.10.1, hostname ubuntu-server1
```

The `tag=3` on `net0` is what places the VM on VLAN 3; change it to `tag=6`
for the desktop machines.

### 2. Creating an imported-appliance VM

For GNS3 and EVE-ng, import the appliance rather than booting an installer:

```bash
# Import an appliance disk (OVA/qcow2) into a new VM, on river, tagged to
# its VLAN. Example: gns3, VLAN 3.
qm create 113 --name gns3 --memory 8192 --cores 4 \
  --net0 virtio,bridge=vmbr1,tag=3
qm importdisk 113 gns3-appliance.qcow2 river-vm
qm set 113 --scsihw virtio-scsi-single --scsi0 river-vm:vm-113-disk-0
qm set 113 --boot order=scsi0
# Enable nested virtualization for the emulator.
qm set 113 --cpu host
qm start 113
# Set the appliance's address to 10.30.10.86/24, gateway 10.30.10.1.
```

### 3. Setting addresses and hostnames in the guests

Each guest gets its fixed address, gateway, and hostname set *inside* the OS —
during installation (the installer's network step) or afterward. The values
are the table above; the method is guest-specific (netplan on Ubuntu,
NetworkManager on RHEL, the Windows network settings, the appliance's own
console for CML/EVE-ng/GNS3).

### 4. The full deployment, machine by machine

Repeat the appropriate pattern for all nine, tagging each NIC to its VLAN and
setting each guest's address and hostname:

```text
ubuntu1        VLAN 6  10.30.12.100/24  gw 10.30.12.1   (installer ISO)
ubuntu-server1 VLAN 3  10.30.10.100/24  gw 10.30.10.1   (installer ISO)
eve-ng         VLAN 3  10.30.10.85/24   gw 10.30.10.1   (appliance)
gns3           VLAN 3  10.30.10.86/24   gw 10.30.10.1   (appliance)
cml            VLAN 3  10.30.10.87/24   gw 10.30.10.1   (licensed image)
rhel-desktop1  VLAN 6  10.30.12.101/24  gw 10.30.12.1   (installer ISO)
rhel-server1   VLAN 3  10.30.10.88/24   gw 10.30.10.1   (installer ISO)
win11-1        VLAN 6  10.30.12.102/24  gw 10.30.12.1   (installer ISO)
win-server1    VLAN 3  10.30.10.89/24   gw 10.30.10.1   (installer ISO)
```

## Validation and Troubleshooting

### Confirming each VM is placed and addressed correctly

For every VM:

| Check | Expectation | Failure means |
| --- | --- | --- |
| VLAN tag | Matches the table (3 or 6) | Wrong tag — VM on the wrong subnet |
| In-guest address | Matches the table | Address not set, or a typo |
| Gateway reachable | Guest can ping its gateway | VLAN/tag mismatch, or trunk missing the VLAN |
| Hostname | Matches the table | Hostname not set in the guest |
| No IP conflict | Each address unique | The .88/.89 correction not applied, or a duplicate |

### The VLAN-tag / gateway mismatch

The most common per-VM failure is a guest with the correct address but the
wrong VLAN tag — it cannot reach its gateway because it is on the wrong
layer-2 network. The symptom is "correct IP, no connectivity." Confirm the
NIC's `tag=` matches the subnet: VLAN 3 for 10.30.10.x, VLAN 6 for
10.30.12.x. This is where the Chapter 05 trunk correction pays off — a server
VM tagged 3 only works because VLAN 3 is now allowed on the trunk.

### The duplicate-address reminder

If Red Hat Server and Windows Server are both deployed at 10.30.10.88, they
conflict — the second to come up may fail to reach the network or cause
intermittent failures for both. The correction (Windows Server → .89) exists
to prevent exactly this; confirm the two are on distinct addresses.

## Security and Best Practices

- **Isolate VM networks by VLAN deliberately.** Desktops on VLAN 6, servers
  on VLAN 3 — the segmentation is a security boundary, and inter-VLAN traffic
  should pass only where the network policy intends.
- **Harden each guest to its role.** A server VM and a desktop VM warrant
  different hardening; the guest volumes (XIV, XXI) cover this, and the
  network-emulation appliances have their own admin surfaces to secure.
- **Do not over-provision the emulators onto shared resources carelessly.**
  EVE-ng, GNS3, and CML can consume significant CPU and RAM; sizing them
  against `river` and the host's capacity keeps them from starving the other
  VMs.
- **Track which VMs run evaluation or licensed images.** The Windows
  evaluation VMs expire, and CML is licensed; knowing which is which avoids
  surprises.

## References and Knowledge Checks

**References**

- [Chapter 05](05-network-architecture-management-nic-vlan-trunk-and-bridges.md)
  — the VLAN-aware bridge and trunk each VM's NIC attaches to.
- [Chapter 07](07-building-the-iso-library.md)
  — the image library each VM is built from.
- [Proxmox VE qm and VM documentation](https://pve.proxmox.com/pve-docs/qm.1.html)
  — VM creation, NIC tagging, and disk import.
- [Volume XXI](../../volume-21-ubuntu-server-cloud-26-04-lts/README.md)
  and [Volume XIV](../../volume-14-red-hat-enterprise-linux-10/README.md)
  — guest-OS installation and in-guest network configuration.

**Knowledge checks**

1. How is a VM placed on a specific VLAN, and where is its IP address
   actually set?
2. What are the two corrections carried into this chapter, and what does each
   prevent?
3. Which VMs are on VLAN 6 and which on VLAN 3, and what subnet does each
   VLAN correspond to?
4. How does deploying GNS3 or EVE-ng differ from deploying an OS from an
   installer ISO?
5. A guest has the right IP but cannot reach its gateway. What is the most
   likely cause?

## Hands-On Lab

**Objective:** Deploy all nine virtual machines with their exact VLANs,
addresses, gateways, and hostnames, and confirm each reaches its gateway.

**Prerequisites:** The VM datastore and verified ISO library from Chapters
06–07, and the VLAN-aware trunk bridge from Chapter 05 carrying VLAN 3.

**Reproducible to the extent your images allow** — the free-image VMs fully,
the licensed ones with your entitlements.

**Procedure**

1. Create each installer-ISO VM (Ubuntu ×2, RHEL ×2, Windows ×2, CML) with a
   disk on `river`, a NIC on `vmbr1` tagged to its VLAN, and the installer
   ISO attached; run setup and set the guest's address, gateway, and
   hostname per the table.
2. Create each appliance VM (GNS3, EVE-ng) by importing its appliance disk,
   tagging its NIC to VLAN 3, enabling nested virtualization, and setting its
   address per the table.
3. For each VM, confirm the NIC's VLAN tag matches its subnet (3 for
   10.30.10.x, 6 for 10.30.12.x).
4. From each guest, ping its gateway and confirm connectivity.
5. Confirm all nine addresses are unique — in particular that Red Hat Server
   (.88) and Windows Server (.89) do not collide.

**Negative test**

6. Change one server VM's NIC tag from 3 to 6 while leaving its 10.30.10.x
   address, and confirm it can no longer reach its gateway — the correct-IP,
   wrong-VLAN failure. Restore the tag to 3 and confirm connectivity returns.

**Expected results**

- All nine VMs running, each on its correct VLAN with its fixed address and
  hostname.
- Each guest reaches its gateway.
- No duplicate addresses — the .88/.89 split in effect.

**Cleanup**

7. Leave the VMs running; Chapter 09 validates the whole environment.
   Restore any tag changed in the negative test.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The nine virtual machines are the point of the whole build, each deployed
from the `river` ISO library onto `river` VM storage, each placed on its VLAN
by a tag on its virtual NIC on the VLAN-aware bridge, and each given its fixed
address, gateway, and hostname inside the guest. The desktops (`ubuntu1`,
`rhel-desktop1`, `win11-1`) sit on VLAN 6 / 10.30.12.0/24; the servers and
network emulators sit on VLAN 3 / 10.30.10.0/24. Two corrections land here:
Windows Server is `win-server1` at 10.30.10.89 (not the duplicate .88), and
EVE-ng joins VLAN 3 with the other server machines. GNS3 and EVE-ng are
imported appliances rather than installer-ISO builds, and the emulators need
nested virtualization. The failure to watch for is a guest with the right
address but the wrong VLAN tag — correct IP, no connectivity — which the
Chapter 05 trunk correction and careful tagging together prevent.

- [ ] All nine VMs created, each with its disk on `river`.
- [ ] Each NIC tagged to the correct VLAN (3 or 6).
- [ ] Each guest set to its fixed address, gateway, and hostname.
- [ ] GNS3 and EVE-ng imported as appliances with nested virtualization.
- [ ] Every address unique — Red Hat Server .88, Windows Server .89.
