# Chapter 10: Appendix — Virtual Machine Inventory and Access Reference

This appendix is a single, as-built reference for every virtual machine on
the R640 node (`claude@10.30.161.10`): its VMID, hostname, operating system
or role, the VLAN its interfaces land on, its IPv4 addresses, and how to log
in. It consolidates the addressing that is otherwise spread across
[Chapter 08's current-additions table](08-deploying-the-virtual-machines.md)
(which carries vCPU/RAM and bridge detail), the
[Lab 8.7 ISFW cell and cluster tables](08-deploying-the-virtual-machines.md),
and the [Master Appendices IPv4/IPv6 address tables](../../volume-997-master-appendices/chapters/02-appendix-proxmox-lab-ipv4-and-ipv6-address-tables.md).
It is a snapshot as of 15 August 2026; the VLAN column is taken directly from
`qm config` (the hypervisor's own view), so it is the ground truth even where a
narrative elsewhere in the volume predates a rebuild.

**Every credential here is a throwaway lab value and is printed in full.** All
managed guests share the single lab password `ISEisC00L123@2026`; the username
per guest is in the *Login* column. Nothing on this list is a real, personal, or
externally reachable account. Cells marked **‡** are unconfirmed — a build or
appliance default that could not be verified live from the host at snapshot time
(the client/EMS guests on VLANs 200/202 have no management path back to the
Proxmox node, and CirrOS/GNS3 appliances may retain their vendor defaults if they
were never rebuilt).

## The network segments

The VLAN column below refers to these Proxmox bridges and tags. Gateways ending
in `.1` are FortiGate interfaces; the management segments are switched, not
routed by a FortiGate.

| Bridge / VLAN | Subnet | Role and gateway |
| --- | --- | --- |
| `vmbr0` (untagged, VLAN 1611) | `10.30.161.0/24` | Host/out-of-band management — Proxmox `10.30.161.10`, iDRAC `10.30.161.25`, and each ISFW cell's second NIC; gateway `10.30.161.1` |
| `vmbr1` (untagged, VLAN 99) | `10.30.99.0/24` | FortiGate `port1` (WAN/OOB) and the TFTP/PXE box; also the Nexus `mgmt0` OOB |
| `vmbr2` VLAN 2001 | `10.30.1.0/24` | ISFW **APP** segment; gateway `10.30.1.1` (FGT-3 `port2`) |
| `vmbr2` VLAN 2002 | `10.30.2.0/24` | ISFW **DB** segment; gateway `10.30.2.1` (FGT-3 `port3`) |
| `vmbr2` VLAN 2003 | `10.30.3.0/24` | ISFW **HMI** segment; gateway `10.30.3.1` (intended — see note) |
| `vmbr2` VLAN 2004 | `10.30.4.0/24` | ISFW **PLC/OT** segment; gateway `10.30.4.1` (intended — see note) |
| `vmbr2` VLAN 200 | `10.200.0.0/24` | Client / FortiClient-EMS segment; gateway `10.200.0.1` (FGT-1 `port2`) |
| `vmbr2` VLAN 202 | `10.202.0.0/24` ‡ | Second client/EMS segment |
| `vmbr2` VLAN 3 | `10.30.10.0/24` | Server-management segment |

> **ISFW segment note.** The licensed evaluation FortiGate caps at three physical
> interfaces, so only VLAN 2001 (`port2`) and VLAN 2002 (`port3`) have live
> gateways on the current build; the HMI (2003) and PLC (2004) cells are addressed
> and reachable over their management NICs but their data gateways are the intended
> design, not yet wired. See [Chapter 08, Lab 8.7 Part A](08-deploying-the-virtual-machines.md).

## Virtual machine inventory

| VMID | Hostname | OS / Role | VLAN | IPv4 address(es) | Login |
| --- | --- | --- | --- | --- | --- |
| 100 | `gns3` | GNS3 network emulator — **powered off on purpose** (nested-virtualization appliance, started only when needed) | `vmbr0` (mgmt) | *not assigned while off* | `gns3` ‡ |
| 101 | `FGT-101` | FortiGate-VM 7.6.7 — standalone site-to-site IPsec peer | `vmbr1` (99); data `vmbr2` 2001/2002 | `10.30.99.101` (`port1`) | `admin` |
| 110 | `fortigate-fgt10` | FortiGate-VM, FortiOS 8.0 — firmware up/downgrade test unit | `vmbr1` (99); `vmbr2` (native) | `10.30.99.110` (`port1`) | `admin` |
| 120 | `fortigate-7-6-2` | FortiGate-VM 7.6.2 — "FGT-1", client/EMS-lab firewall | `vmbr1` (99); data `vmbr2` 200/202 | `10.30.99.99` (`port1`) | `admin` |
| 121 | `fortigate-fgt2` | FortiGate-VM 7.6.7 — **FGT-2**, HA secondary | `vmbr1` (99); data `vmbr2` 2001/2002 | `10.30.99.98` (`port1`, answers only when primary — cluster VIP is `.122`) | `admin` |
| 122 | `fortigate-fgt3` | FortiGate-VM 7.6.7 — **FGT-3**, ISFW / HA primary | `vmbr1` (99); data `vmbr2` 2001/2002 | `10.30.99.122` (`port1`); `10.30.1.1` (`port2`), `10.30.2.1` (`port3`) | `admin` |
| 130 | `ems-win` | Windows 11 (25H2) — FortiClient EMS host | `vmbr2` 200 | `10.200.0.50` | `Administrator` ‡ |
| 131 | `ems-linux` | Ubuntu 24.04 — FortiClient EMS server (licensed) | `vmbr2` 200 + 3 | `10.200.0.60`; mgmt `10.30.10.60` | ‡ (Ubuntu login unconfirmed) |
| 140 | `tftp` | Alpine — TFTP/PXE server (FortiGate firmware and configs) | `vmbr1` (99) | `10.30.99.50` | `root` ‡ |
| 200 | `test-vlan200` | CirrOS — VLAN 200 reachability probe | `vmbr2` 200 | `10.200.0.0/24` host octet unconfirmed ‡ | `cirros` ‡ |
| 202 | `test-vlan202` | CirrOS — VLAN 202 reachability probe | `vmbr2` 202 | `10.202.0.0/24` unconfirmed ‡ | `cirros` ‡ |
| 210 | `ubuntu-ws` | Ubuntu — workstation / VLAN-200 jump host | `vmbr2` 200 | `10.200.0.20` | ‡ (Ubuntu login unconfirmed) |
| 230 | `c109-web` | Alpine — ISFW APP tier | data `vmbr2` 2001; mgmt `vmbr0` | `10.30.1.10`; mgmt `10.30.161.230` | `root` |
| 231 | `c109-db` | Alpine — ISFW DB tier (listens tcp/5432) | data `vmbr2` 2002; mgmt `vmbr0` | `10.30.2.10`; mgmt `10.30.161.231` | `root` |
| 232 | `c109-hmi` | Alpine — ISFW HMI tier | data `vmbr2` 2003; mgmt `vmbr0` | `10.30.3.10`; mgmt `10.30.161.232` | `root` |
| 233 | `c109-plc` | Alpine — ISFW PLC/OT cell (listens tcp/502) | data `vmbr2` 2004; mgmt `vmbr0` | `10.30.4.10`; mgmt `10.30.161.233` | `root` |

**How to reach a guest.** The five FortiGates answer HTTPS/SSH on their `port1`
addresses (`10.30.99.x`); the FGT-2 secondary is reached from the primary with
`execute ha manage 1 admin`. The four `c109-*` Alpine cells have no SSH path on
their data VLANs, so each is driven over its management NIC (`10.30.161.23x`),
which shares the Proxmox host's L2 — `ssh root@10.30.161.23x` from the node. The
client/EMS guests on VLANs 200/202 are reachable only through FGT-1 and from a
peer on the same segment (for example the `ubuntu-ws` jump host), not from the
management network.

## Keeping this appendix current

Regenerate the VLAN and NIC columns from the hypervisor with `qm config <vmid>`
(the `bridge=` and `tag=` fields), and confirm which guests are live with
`qm list`. Addresses inside a guest come from the guest itself — `ip -4 addr` on
the Linux and Alpine guests, `get system interface physical` on the FortiGates —
because Proxmox does not track in-guest IPs without the guest agent. When a
**‡**-marked cell is verified, drop its mark; when a VM is added or removed, update
both this table and [Chapter 08's current-additions table](08-deploying-the-virtual-machines.md).
