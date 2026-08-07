# Chapter 02: Current Equipment

This is the as-built inventory of the lab, recorded from the live configuration
(the Proxmox host, the Nexus running-config, and the addressing in use).
Fields marked **TBD** are hardware specifics to be filled in by measurement;
everything else is confirmed from the running systems. No credentials, keys, or
passwords are recorded here — only topology, addressing, and roles.

## Compute — hosts

Five host positions are cabled to the switch, one per rack unit `ru08`–`ru12`,
each with four 10 Gb NICs (`vmnic0`–`vmnic3`) landing on consecutive Nexus
ports. `proxmox-1` (ru12) is confirmed as a Dell PowerEdge R640 running Proxmox
VE; the remaining positions are cabled and switch-described but their models and
roles are to be confirmed.

| Rack unit | Host | Model | OS / role | NICs → Nexus | Mgmt |
|-----------|------|-------|-----------|--------------|------|
| ru12 | `proxmox-1` | Dell PowerEdge R640 | Proxmox VE 9.2.9 | vmnic0–3 → Eth1/17–20 | iDRAC (Eth1/40, VLAN 1611); host `10.30.161.10` |
| ru11 | TBD | Dell PowerEdge (TBD) | TBD | vmnic0–3 → Eth1/13–16 | TBD |
| ru10 | TBD | Dell PowerEdge (TBD) | TBD | vmnic0–3 → Eth1/9–12 | TBD |
| ru09 | TBD | Dell PowerEdge (TBD) | TBD | vmnic0–3 → Eth1/5–8 | TBD |
| ru08 | TBD | Dell PowerEdge (TBD) | TBD | vmnic0–3 → Eth1/1–4 | TBD |

**Per-host specs (to complete):** CPU (2× Xeon Scalable, SKU TBD), RAM (TBD),
boot device (Dell BOSS mirror, TBD), local storage (TBD). `proxmox-1` boot/data
layout is captured under Storage below.

## Networking — switch

| Item | Value |
|------|-------|
| Hostname | `nexus-9k-1` |
| Platform | Cisco Nexus 9300-series (9396PX-class: 48× SFP+ 10 Gb on module 1, 12× 40 Gb uplink on module 2) — *inferred from the Eth1/1–48 + Eth2/1–12 layout* |
| NX-OS | `7.0(3)I2(2d)` |
| OOB management | `mgmt0` = `10.30.99.250/24`, default route `10.30.99.1` (management VRF) |
| Features | `lacp`, `lldp` |
| Uplink | `port-channel1` (member Eth1/47, `mode active`; Eth1/48 standalone trunk) — trunk, native VLAN 1611 |
| Host trunks | Eth1/1–20 (ru08–ru12 × 4), trunk, native VLAN 1611, allowed `3,8,1611-1615,3939` |
| iDRAC / OOB access ports | Eth1/40 `proxmox-idrac`, Eth1/41 `unraid-idrac`, Eth1/30 — access VLAN 1611 |
| Global | `system default switchport shutdown` (ports are shut unless explicitly `no shutdown`) |

## VLAN plan

| VLAN | Name | Purpose | Notes |
|------|------|---------|-------|
| 1 | default | Untagged / legacy (Unraid) | `192.168.1.0/24` |
| 3 | Servers | Server data segment | |
| 8 | SDx | Software-defined / lab segment | |
| 99 | core-mgmt | Core management (data-plane) | Added this session; trunked to hosts + Eth1/48 |
| 999 | native | Dedicated parking / native VLAN | Added this session; native on host trunks, carries no data |
| 1610 | Native-VLAN-1610 | Legacy native | |
| 1611 | External-Mgmt | Host mgmt + iDRAC | `10.30.161.0/24` — native on trunks |
| 1612 | vMotion | Live-migration transport | For clustering |
| 1613 | vSAN | Shared-storage transport | For clustering |
| 1614 | VmNetwork-A | VM data A | |
| 1615 | VmNetwork-B | VM data B | |
| 3939 | Private | Isolated segment | |

## Addressing

| Subnet | VLAN / plane | Gateway | Notes |
|--------|--------------|---------|-------|
| `10.30.161.0/24` | VLAN 1611 (External-Mgmt) | `10.30.161.1` | Host management: `proxmox-1` = `.10`; iDRACs |
| `10.30.99.0/24` | Out-of-band management | `10.30.99.1` | Nexus `mgmt0` = `.250`; **separate segment from the data VLANs** |
| `192.168.1.0/24` | VLAN 1 | TBD | Unraid NAS = `.209` |

> **OOB vs data-VLAN caution.** `10.30.99.0/24` is the out-of-band management
> subnet (the switch's `mgmt0`). It is reached from the host network by routing
> through `10.30.161.1`, not by an L2 VLAN — so a host cannot be placed on it by
> tagging a data VLAN. Data segments get their own subnets.

## Storage

| System | Type | Detail |
|--------|------|--------|
| `unraid-1` | Unraid NAS | `192.168.1.209/24` (VLAN 1), cabled Eth1/33–34. ISOs, backups, bulk. iDRAC/IPMI on Eth1/41 |
| `proxmox-1` local | LVM-thin | `local-lvm` (~136 GB) — running VM disks |
| `proxmox-1` local | Directory | `disk_image`, `import`, `iso` (dir stores, shared filesystem) |
| `proxmox-1` local | Boot | `local` (Dell BOSS mirror — TBD) |
| `proxmox-1` local | ZFS | `blue` zfspool — **inactive** (pool missing; needs import or removal) |
| `proxmox-1` array | RAID | `river` array (PERC RAID-5 — see Volume XXVI) — VM/data datastore |

## Virtualization and key VMs

| ID | Name | What | Network |
|----|------|------|---------|
| 100 | `gns3` | GNS3 network emulator VM (nested virtualization) | VLAN 3 |
| 120 | `fortigate-7-6-2` | FortiGate-VM 7.6.2 (build 3462), evaluation | port1 on VLAN 99 (`10.30.99.99`); port2 trunk |

`proxmox-1` bridges: `vmbr0` (management, on `nic1`/Eth1/17, `10.30.161.10/24`),
`vmbr1` (VLAN-aware trunk, on `nic2`/Eth1/18). A bonded uplink `bond2`
(`nic3`+`nic4`, LACP 802.3ad) is documented in Volume XXVI, Chapter 05.

Emulators in use: **GNS3** and **EVE-NG** (FortiGate and other appliance images
imported per Volumes XIX and XXVI).

## Management planes

- **iDRAC** on every Dell host — out-of-band console, power, virtual media
  (access ports on VLAN 1611).
- **Nexus `mgmt0`** on the OOB subnet `10.30.99.0/24`.
- **Proxmox web UI** at `https://10.30.161.10:8006` (host management on VLAN
  1611).

The next chapter draws all of this — the physical/network topology, the rack
elevation, and the logical VLAN plan.
