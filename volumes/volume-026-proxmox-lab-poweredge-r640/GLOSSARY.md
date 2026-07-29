# Volume XXVI Glossary

Definitions for terms introduced in **Volume XXVI — Proxmox Virtualization
Lab on Dell PowerEdge R640**, alphabetized. See also the
[volume index](INDEX.md) for pointers back to the chapter section each term
is drawn from, and the [master glossary](../../GLOSSARY.md) for cross-volume
terminology.

**Appliance (VM)** — A pre-built virtual machine image imported as an
existing disk rather than installed from an operating-system installer.
GNS3 and EVE-ng are deployed this way. Introduced in Chapter 07.

**BOSS (Boot Optimized Storage Solution)** — A dedicated Dell controller
carrying a small mirrored pair of SSDs for the boot operating system,
separate from the main data array. In this build it holds Proxmox VE on a
RAID 1 mirror of two 256 GB SSDs. Introduced in Chapter 02.

**Content type** — In Proxmox storage, the category of data a storage holds
— `images` for VM disks, `iso` for installation media, and others. One
storage can declare several. Introduced in Chapter 06.

**Enterprise repository** — Proxmox's subscription-gated update stream,
enabled by default and requiring a paid key. It must be disabled for a
no-subscription setup. Introduced in Chapter 04.

**iDRAC (integrated Dell Remote Access Controller)** — The out-of-band
management controller inside a Dell PowerEdge server, with its own network
port and address, providing remote console, power control, and hardware
management independent of the host OS. Set to 10.30.161.25 in this build.
Introduced in Chapter 01.

**LVM-Thin** — A thin-provisioned block-storage type in Proxmox that
supports snapshots and efficient space use for VM disks; it holds VM images
but not ISO files. Introduced in Chapter 06.

**NetBox** — A free, open-source Django web application for network
source-of-truth and IP-address management. It has no operating-system ISO;
in this build it is deployed as an application on a new Ubuntu Server guest
(`netbox`, 10.30.10.62, VLAN 3), so the Ubuntu Server image serves two
machines. Introduced in Chapter 08.

**No-subscription repository** — Proxmox's free update stream, requiring no
key, enabled in place of the enterprise repository for a lab. Enabling it is
what "activating the free version" of Proxmox actually means. Introduced in
Chapter 04.

**Proxmox VE** — A free, open-source virtualization platform built on
Debian, KVM, and LXC, managed through a web interface; the hypervisor this
build installs. Introduced in Chapter 03.

**RAID 1 (mirror)** — A RAID level that writes identical data to two drives
so either can fail without data loss, prioritizing survivability over
capacity. Used for the BOSS boot mirror. Introduced in Chapter 02.

**RAID 5** — A RAID level striping data with distributed parity across
three or more drives, tolerating one drive failure and providing the usable
capacity of all drives but one. Used for the `river` array. Introduced in
Chapter 02.

**`river`** — The name of this build's RAID 5 array across the six front
drives, holding virtual machine storage and the ISO repository. Introduced
in Chapter 02.

**Trunk (802.1Q)** — A single network link carrying traffic for multiple
VLANs, each frame tagged with its VLAN ID. Port 1 of this build is a trunk
carrying VLANs 3, 6, 10, 200, and 202. Introduced in Chapter 05.

**VLAN-aware bridge** — A Proxmox Linux bridge that passes VLAN-tagged
traffic, letting each virtual machine select its VLAN by a tag on its
virtual NIC rather than needing a separate bridge per VLAN. Introduced in
Chapter 05.

**VLAN tag** — The VLAN ID set on a virtual machine's network interface,
which places the VM on that VLAN's layer-2 network. A VM tagged 3 lands on
10.30.10.0/24; one tagged 6 on 10.30.12.0/24. Introduced in Chapter 08.

**Virtual media** — An installation image mounted to a server over the
network through the iDRAC, as if it were a physical disc, used to install
Proxmox VE without physical media. Introduced in Chapter 03.
