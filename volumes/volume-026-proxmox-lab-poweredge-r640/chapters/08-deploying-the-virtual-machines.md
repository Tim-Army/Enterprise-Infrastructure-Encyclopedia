# Chapter 08: Deploying the Virtual Machines

## Learning Objectives

- Create each of the ten virtual machines with its exact parameters.
- Place each VM on its assigned VLAN using the VLAN-aware bridge.
- Assign each VM its fixed address, gateway, and hostname.
- Distinguish installer-ISO VMs from imported-appliance VMs.
- Verify every VM reaches its gateway on the correct VLAN.

## Theory and Architecture

### The ten machines and their addressing

This chapter deploys the workload the whole build has been leading to: ten
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
| NetBox | `netbox` | 10.30.10.62/24 | 10.30.10.1 | 3 |

The pattern is consistent: **VLAN 6 machines** (`ubuntu1`, `rhel-desktop1`,
`win11-1`) are the desktops on 10.30.12.0/24; **VLAN 3 machines** (everything
else) are the servers on 10.30.10.0/24, gateway 10.30.10.1.

### NetBox: an application on a new Ubuntu Server guest

Nine of the ten machines are deployed from an operating-system image — an
installer ISO or an imported appliance. **NetBox is the exception, and it
is worth being clear about why.** NetBox Community Edition is a Django web
application for network source-of-truth and IP-address management; it is not
an operating system and ships as no bootable ISO. It is deployed by
building a **new Ubuntu Server guest** — from the same Ubuntu Server image
already in the library — and installing NetBox onto it.

This is the same one-image-serves-two-machines pattern the RHEL image
already follows for the two Red Hat machines: the Ubuntu Server image now
backs both `ubuntu-server1` and `netbox`. The `netbox` VM is a full server
in its own right — VLAN 3, 10.30.10.62/24, gateway 10.30.10.1 — that happens
to run NetBox as its purpose.

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

Most of the ten are installed from an ISO — you attach the installer,
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
  target for all ten; none belong on the boot mirror.

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

Repeat the appropriate pattern for all ten, tagging each NIC to its VLAN and
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
netbox         VLAN 3  10.30.10.62/24   gw 10.30.10.1   (Ubuntu guest + NetBox)
```

### 5. Deploying the NetBox machine

NetBox is deployed as an Ubuntu Server guest with NetBox installed on it,
rather than from a NetBox ISO. First build the guest exactly as any other
Ubuntu Server VM, tagged VLAN 3 and addressed 10.30.10.62/24, hostname
`netbox`:

```bash
# A new Ubuntu Server guest for NetBox — VLAN 3, on river.
qm create 118 --name netbox --memory 4096 --cores 2 \
  --scsihw virtio-scsi-single \
  --scsi0 river-vm:32 \
  --net0 virtio,bridge=vmbr1,tag=3 \
  --ide2 river-iso:iso/ubuntu-<ver>-live-server-amd64.iso,media=cdrom \
  --boot order=ide2
qm start 118
# In the installer set: address 10.30.10.62/24, gateway 10.30.10.1,
# hostname netbox.
```

Then install NetBox Community Edition on the running guest. NetBox is a
Django application with a small set of dependencies; the two supported
routes are its documented bare-metal install and its container deployment:

```bash
# On the netbox guest. NetBox needs PostgreSQL, Redis, and Python; the
# official installation documents the exact steps and current versions.
sudo apt update && sudo apt install -y \
  postgresql redis-server python3 python3-pip python3-venv \
  build-essential libxml2-dev libxslt1-dev libffi-dev libpq-dev \
  libssl-dev zlib1g-dev git

# Then follow the official NetBox installation to create the database,
# clone/unpack NetBox, configure it, and serve it behind gunicorn + nginx.
# (Alternatively, netbox-docker runs the same application via Docker
# Compose on this guest — a container deployment rather than bare-metal.)
```

Confirm NetBox answers on the guest at `https://10.30.10.62/` once its web
front end is running.

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
- [Volume XXI](../../volume-021-ubuntu-server-cloud-26-04-lts/README.md)
  and [Volume XIV](../../volume-014-red-hat-enterprise-linux-10/README.md)
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

This chapter carries a topic-level walkthrough lab for **each VM-deployment step** — creating a VM,
building a cloud-init template, cloning it into the fleet, and the container alternative. Commands
are runnable `qm`/`pct`. Each ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 8.1–8.4** — a Proxmox node with the `river` datastore, ISOs and a
cloud image in the library (Chapters 06–07), a VLAN-aware bridge (Chapter 05), and root SSH.
**Cost:** none.

### Lab 8.1 — Create a VM from an ISO (Topic: VM creation)

**Objective:** Build one VM the manual way.

```bash
qm create 100 --name test-vm --memory 2048 --cores 2 \
  --net0 virtio,bridge=vmbr0,tag=30 \
  --scsihw virtio-scsi-single --scsi0 river:32 \
  --ide2 riverfiles:iso/ubuntu-24.04-live-server-amd64.iso,media=cdrom \
  --boot order='scsi0;ide2' --ostype l26
qm start 100
qm status 100
```

**Expected result:** VM 100 is created with a 32 GB disk on `river`, a NIC on VLAN 30 via the
VLAN-aware bridge, the Ubuntu ISO attached, and it powers on to the installer — `qm create` defines a
VM entirely from the CLI (disk on the datastore, NIC on a tagged bridge, ISO as CD), the foundation
for scripting the fleet.

**Negative test:** attach the disk to `local` (boot mirror) instead of `river`; the VM competes with
the OS for the small boot device — VM disks belong on the `river` datastore.

**Cleanup:** `qm stop 100; qm destroy 100`.

### Lab 8.2 — Build a cloud-init template (Topic: Templates)

**Objective:** Turn a cloud image into a reusable template.

```bash
qm create 9000 --name ubuntu-2404-template --memory 2048 --cores 2 --net0 virtio,bridge=vmbr0,tag=30
qm importdisk 9000 /river/template/cache/noble-server-cloudimg-amd64.img river
qm set 9000 --scsihw virtio-scsi-single --scsi0 river:vm-9000-disk-0
qm set 9000 --ide2 river:cloudinit --boot order=scsi0 --serial0 socket --vga serial0
qm set 9000 --ciuser labadmin --sshkeys ~/.ssh/id_ed25519.pub --ipconfig0 ip=dhcp
qm template 9000
```

**Expected result:** VM 9000 becomes a **template** with the cloud image as its disk and a cloud-init
drive that injects user/SSH-key/network on first boot — a cloud-init template is a golden image;
clones of it come up fully configured with no interactive install.

**Negative test:** clone a VM that has no cloud-init drive expecting per-clone hostname/IP/keys; each
clone is an identical copy with the same identity — the cloud-init drive is what makes each clone
uniquely configured.

**Cleanup:** keep the template (Lab 8.3 clones it).

### Lab 8.3 — Clone the fleet (Topic: Fleet deployment)

**Objective:** Deploy the ten VMs from the template.

```bash
for id in $(seq 101 110); do
  qm clone 9000 "$id" --name "vm-$id" --full --storage river
  qm set "$id" --ipconfig0 ip=192.168.30.$id/24,gw=192.168.30.1
  qm start "$id"
done
qm list
```

**Expected result:** ten VMs (101–110) are cloned from the template, each with its own IP via
cloud-init, and started — cloning a cloud-init template in a loop deploys a consistent fleet in
minutes; `--full` makes independent copies (vs `--link` linked clones that share the base).

**Negative test:** deploy ten VMs by running the ISO installer ten times; it is slow and each may
differ subtly — templated cloning gives identical, fast, scriptable deployment (the point of the
ten-VM build).

**Cleanup:** `for id in $(seq 101 110); do qm stop $id; qm destroy $id; done` when tearing down.

### Lab 8.4 — Containers as a lighter alternative (Topic: Containers)

**Objective:** Deploy an LXC container where a full VM is overkill.

```bash
pveam update && pveam available --section system | grep -i ubuntu | head -1
pveam download riverfiles ubuntu-24.04-standard_24.04-2_amd64.tar.zst 2>/dev/null || true
pct create 200 riverfiles:vztmpl/ubuntu-24.04-standard_24.04-2_amd64.tar.zst \
  --hostname ct200 --memory 1024 --cores 1 --rootfs river:8 \
  --net0 name=eth0,bridge=vmbr0,tag=30,ip=192.168.30.200/24,gw=192.168.30.1
pct start 200 ; pct status 200
```

**Expected result:** an LXC container (200) starts with far less overhead than a VM — Proxmox runs
both full VMs (`qm`, hardware-virtualized, any OS) and system containers (`pct`, LXC, shared kernel,
lightweight); containers suit many Linux services where a full VM's isolation/overhead is
unnecessary.

**Negative test:** run a Windows or a custom-kernel workload in an LXC container; it cannot (LXC
shares the host kernel) — use a full VM (`qm`) for non-Linux or kernel-specific workloads, containers
for lightweight Linux services.

**Cleanup:** `pct stop 200; pct destroy 200`.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The ten virtual machines are the point of the whole build, each deployed
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

- [ ] All ten VMs created, each with its disk on `river`.
- [ ] Each NIC tagged to the correct VLAN (3 or 6).
- [ ] Each guest set to its fixed address, gateway, and hostname.
- [ ] GNS3 and EVE-ng imported as appliances with nested virtualization.
- [ ] Every address unique — Red Hat Server .88, Windows Server .89.
