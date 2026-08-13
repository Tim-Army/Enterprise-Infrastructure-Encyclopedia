# Chapter 73: Appendix — Deploying Lab Appliance Images on Each Hypervisor

Every lab in this encyclopedia that stands up a virtual machine — a vendor appliance shipped as
a disk image, or an operating system installed from an ISO — assumes the VM already exists on
your hypervisor before the in-guest walkthrough begins. This appendix is the single reference
those labs link to for the **host side**: how to import a disk image or install from an ISO,
size the VM, attach a console, and map its interfaces, on each hypervisor the encyclopedia uses.

Each lab supplies the *specifics* — the image file name, the vCPU/RAM/disk to give it, and which
virtual NIC lands on which segment of that lab's topology. This appendix supplies the
*mechanics* that are the same every time. Where a lab needs something unusual (a serial-only
appliance, a second data disk, a licensed form factor), it says so and points here for the rest.

## Image artifact types

Vendors ship a virtual appliance in one or more of these forms; pick the one your hypervisor
consumes:

| Artifact | Native to | Also usable on |
| --- | --- | --- |
| `qcow2` disk | Proxmox, KVM/QEMU, EVE-NG, GNS3, containerlab, Nutanix AHV | VirtualBox/VMware/Hyper-V after conversion |
| `.ova` / `.ovf` + `.vmdk` | VMware ESXi/vSphere, Workstation/Fusion | VirtualBox (import OVA) |
| `.vhd` / `.vhdx` | Microsoft Hyper-V | VirtualBox; convert to qcow2 for KVM |
| `.iso` (installer) | Any hypervisor | — (you install the OS, then it becomes a disk) |
| Cloud image (`qcow2`/`vmdk` + cloud-init) | Any hypervisor with a cloud-init drive | — |

Convert between forms with `qemu-img convert` when a lab ships only one:
`qemu-img convert -O qcow2 disk.vmdk disk.qcow2` (or `-O vpc` for VHD, `-O vmdk` for VMDK).

## Common settings

Unless a lab says otherwise: give the VM the vendor-minimum vCPU/RAM the lab states, use the
paravirtual NIC and disk types (`virtio` on KVM/Proxmox, `vmxnet3`/PVSCSI on VMware, "Network
Adapter" on Hyper-V), and add a **serial console** for appliances that have no VGA login
(most network appliances). Take a **baseline snapshot** right after first boot so the lab's
rollback can return to a clean appliance.

---

## Proxmox VE

**Import a disk image** (`qcow2`/`vmdk`/`vhd` — `importdisk` converts on the way in):

```text
qm create 900 --name lab-vm --cores <n> --memory <MB> \
  --scsihw virtio-scsi-pci --serial0 socket --net0 virtio,bridge=vmbr0
qm importdisk 900 <image>.qcow2 local-lvm
qm set 900 --virtio0 local-lvm:vm-900-disk-0 --boot order=virtio0
qm start 900
```

**Install from an ISO** — attach the ISO as a CD-ROM and boot from it:

```text
qm create 900 --name lab-vm --cores <n> --memory <MB> --scsihw virtio-scsi-single \
  --scsi0 local-lvm:32 --ide2 local:iso/<installer>.iso,media=cdrom \
  --net0 virtio,bridge=vmbr0 --boot order='ide2;scsi0' --serial0 socket
qm start 900
```

**Map interfaces:** one `--netN virtio,bridge=vmbrX` per NIC; add `,tag=<vlan>` for a
VLAN-tagged segment (`--net1 virtio,bridge=vmbr2,tag=2001`). **Console:** `qm terminal 900`
(serial) or the web console.

## KVM / QEMU (libvirt)

**Disk image** (`qcow2`):

```text
virt-install --name lab-vm --memory <MB> --vcpus <n> --os-variant generic --import \
  --disk path=<image>.qcow2,bus=virtio --network bridge=br0,model=virtio \
  --graphics none --console pty,target_type=serial
```

**ISO install:** replace `--import` with `--cdrom <installer>.iso --disk size=32`.
**Interfaces:** repeat `--network bridge=brX,model=virtio` (or `network=<name>`) per NIC.
**Console:** `virsh console lab-vm`.

## VMware ESXi / vSphere

**OVA/OVF:** deploy from the vSphere client (*Deploy OVF Template*) or `ovftool`:

```text
ovftool --name=lab-vm --datastore=datastore1 --net:"<ovf-net>=<portgroup>" \
  appliance.ovf 'vi://<user>@<esxi-host>/'
```

**Bare VMDK:** upload to a datastore, then *New VM > Use an existing virtual disk*.
**ISO install:** *New VM*, attach the ISO from a datastore to the CD/DVD drive, set the NIC to a
port group, power on. **Interfaces:** map each adapter to a **port group** (use `vmxnet3`).

## VMware Workstation / Fusion

**OVA/OVF:** *File > Open* the `.ovf`/`.ova` and accept the import. **ISO install:** *Create a
New Virtual Machine* > point at the ISO. **Interfaces:** *VM > Settings > Network Adapter* — set
**Bridged**, **NAT**, **Host-only**, or a custom **VMnet** (LAN segment) per adapter to match
the lab's segments, before power-on.

## VirtualBox

**Import an OVA:**

```text
VBoxManage import appliance.ova --vsys 0 --vmname lab-vm
```

**ISO install:**

```text
VBoxManage createvm --name lab-vm --ostype Linux_64 --register
VBoxManage modifyvm lab-vm --memory <MB> --cpus <n>
VBoxManage createhd --filename lab-vm.vdi --size 32768
VBoxManage storagectl lab-vm --name SATA --add sata
VBoxManage storageattach lab-vm --storagectl SATA --port 0 --device 0 --type hdd --medium lab-vm.vdi
VBoxManage storageattach lab-vm --storagectl SATA --port 1 --device 0 --type dvddrive --medium <installer>.iso
```

**Interfaces:** `VBoxManage modifyvm lab-vm --nic<N> intnet --intnet<N> <segment>` (or
`hostonly` / `bridged`) per adapter.

## Microsoft Hyper-V

**VHD/VHDX** (Generation 1 for BIOS appliances, Generation 2 for UEFI):

```powershell
New-VM -Name lab-vm -Generation 1 -MemoryStartupBytes <MB>MB `
  -VHDPath <path>\disk.vhd -SwitchName vSwitch-Lab
Set-VMProcessor lab-vm -Count <n>
Start-VM lab-vm
```

**ISO install:** `New-VM ... -NewVHDPath disk.vhdx -NewVHDSizeBytes 32GB`, then
`Add-VMDvdDrive -VMName lab-vm -Path <installer>.iso` and set the DVD first in
`Set-VMFirmware`/BIOS boot order. **Interfaces:** one `Add-VMNetworkAdapter -SwitchName <vSwitch>`
per NIC; tag a VLAN with `Set-VMNetworkAdapterVlan`.

## EVE-NG

KVM `qcow2` images live under a version-named directory; the disk name follows the node type
(`virtioa.qcow2` for a generic QEMU node):

```text
mkdir -p /opt/unetlab/addons/qemu/<vendor>-<version>
cd /opt/unetlab/addons/qemu/<vendor>-<version>
tar zxf /root/<image>.tgz --strip-components=1     # or: mv <image>.qcow2 virtioa.qcow2
/opt/unetlab/wrappers/unl_wrapper -a fixpermissions
```

Add the node to the lab canvas and wire its interfaces to bridges/other nodes there.
**ISO/OS installs** use the same directory with the installer as `cdrom.iso`.

## GNS3

*File > Import appliance* and select the vendor's published `.gns3a` template, pointing it at
the `qcow2`; or *New template > Manually create a new QEMU VM*, attach the disk (or an ISO on
the CD-ROM), and set the vCPU/RAM. **Interfaces:** draw links on the topology to switches or
the `NAT`/`Cloud` node.

## containerlab

For appliances wrapped as VM nodes (vrnetlab), reference the built VM image by `kind`:

```yaml
# lab.clab.yml
topology:
  nodes:
    node1:
      kind: <vendor_platform>          # e.g. fortinet_fortigate, vr-csr, vr-veos
      image: <registry>/<image>:<tag>
  links:
    - endpoints: ["node1:eth1", "node2:eth1"]
```

`clab deploy -t lab.clab.yml`. Interfaces are the `endpoints` in the `links` list.

## Nutanix AHV

Upload the `qcow2`/`vmdk` under *Settings > Image Configuration* (type **Disk**), or an
installer as type **ISO**. Create the VM (*Compute & Storage*: set vCPU/RAM), **add the image
as a disk** (SCSI) or mount the ISO on the CD-ROM, and add **NICs** bound to the AHV networks
(subnets/VLANs) for the lab's segments, then power on.

## Xen / XCP-ng

Import a Xen appliance (`.xva`) with `xe vm-import filename=appliance.xva`, or import a
`qcow2`/`vmdk` as a VDI (`xe vdi-import` after `qemu-img convert`, or via XCP-ng Center). For an
ISO install, put the installer in an ISO SR and attach it. **Interfaces:** create VIFs bound to
the networks (`xe vif-create`) matching the lab's segments.

## Cloud images and cloud-init

Some OS labs use a **cloud image** (a pre-installed `qcow2`/`vmdk` that configures itself from a
cloud-init drive) instead of an ISO install. Attach a cloud-init drive that sets the hostname,
users, and network: on Proxmox, `qm set 900 --ide2 local-lvm:cloudinit` plus
`--ciuser`/`--sshkeys`/`--ipconfig0`; on KVM, `virt-install --cloud-init`; on VMware/Hyper-V,
supply a `seed.iso` built with `cloud-localds`. The lab states the cloud-init values it needs.

## After deployment

Open the **serial console** (headless network appliances have no VGA login) or the VGA/GUI
console, complete any first-boot prompt (many appliances force a password set), and confirm the
version and interface state. Take a **baseline snapshot** now — the lab's rollback returns here —
then continue with the lab's in-guest walkthrough.
