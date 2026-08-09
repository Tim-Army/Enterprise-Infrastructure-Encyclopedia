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
| Platform | Cisco Nexus 9000 **C9396PX** (fixed 48× SFP+ 10 Gb on module 1, plus a 12× 40 Gb QSFP+ uplink module — the `M12PQ`/GEM in module 2) |
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

## Edge gateway and power

| Item | Role | Detail |
|------|------|--------|
| **UCGF** | Edge router / firewall | Ubiquiti UniFi Cloud Gateway Fiber — the lab's edge gateway. WAN uplink to the ISP modem; the default gateway for the lab segments (`10.30.161.1`, `10.30.99.1`, `10.30.10.1`, …), running inter-VLAN routing, NAT to the internet, and edge firewalling. Its gateway interfaces answer with a Ubiquiti `a8:9c:6c` MAC. Configuration detail in [Chapter 04](04-current-device-configurations.md) |
| ISP modem | Internet handoff | Feeds the UCGF WAN uplink. *Provider, modem model, and public IP are intentionally not recorded.* |
| **APC UPS** | Power | A 30 A APC UPS occupying the bottom **5 U** of the rack backs the whole rack — protected runtime for the host, switch, NAS, and gateway |

## Storage

| System | Type | Detail |
|--------|------|--------|
| `proxmox-1` | ZFS pool | `blue` — **active, `ONLINE`**: 5.23 TB raw, ~3.3 TB usable free, mounted `/blue`. The primary datastore — every VM disk (`vm-<id>-disk-N`) runs from it, and it backs the directory stores below. It replaces the former `river` PERC RAID-5 datastore, which is no longer a configured Proxmox storage |
| `proxmox-1` | Directory (on `blue`) | `iso`, `disk_image`, `import`, `backup`, `container`, `container_template`, `snippets` — directory stores living on the ZFS filesystem (ISOs, disk images, backups, snippets) |
| `proxmox-1` | LVM-thin | `local-lvm` (~136 GB) — present but empty; VM disks now live on `blue` |
| `proxmox-1` | Boot / system | `local` (~67 GB directory store on the Dell BOSS mirror) |
| `unraid-1` | Unraid NAS | `192.168.1.209/24` (VLAN 1), cabled Eth1/33–34. ISOs, backups, bulk. IPMI on Eth1/41 |

## Virtualization and key VMs

| ID | Name | What | Network |
|----|------|------|---------|
| 100 | `gns3` | GNS3 network emulator (nested virtualization); currently stopped | VLAN 3 |
| 120 | `fortigate-7-6-2` | FortiGate-VM eval, FortiOS 7.6.x ("FGT-1") — the primary lab firewall (Volume XIX) | port1 WAN on `vmbr1` (`10.30.99.99`); internal ports on `vmbr2` VLANs 200/202 |
| 121 | `fortigate-fgt2` | FortiGate-VM eval ("FGT-2") — second peer for the site-to-site IPsec lab | port1 on `vmbr1`; internal on `vmbr2` VLAN 60 |
| 122 | `fortigate-fgt3` | FortiGate-VM 8.0.0 eval ("FGT-3") — built for the EMS/ZTNA lab; awaiting a licensed FortiGate for strong crypto | port1 on `vmbr1`; VLAN 200 + VLAN 3 mgmt (`10.30.10.61`) |
| 130 | `ems-win` | Windows 11 — first FortiClient EMS host attempt; now spare / candidate Windows ZTNA endpoint | VLAN 200 (`10.200.0.50`) |
| 131 | `ems-linux` | Ubuntu 24.04 — **FortiClient EMS 7.4.8 server** (Linux-based EMS), licensed | VLAN 200 (`10.200.0.60`) + VLAN 3 mgmt (`10.30.10.60`) |
| 200 | `test-vlan200` | Minimal reachability-test endpoint for VLAN 200 | VLAN 200 |
| 202 | `test-vlan202` | Minimal reachability-test endpoint for VLAN 202 | VLAN 202 |
| 210 | `ubuntu-ws` | Ubuntu workstation + VLAN-200 jump host (XFCE, FortiClient/impacket/`sshpass` tooling) | VLAN 200 (`10.200.0.20`) |

`proxmox-1`'s four NICs land on the switch with distinct roles (from the
running-config): `nic1`→`Eth1/17` (access VLAN 1611, host mgmt `10.30.161.10`)
→ bridge `vmbr0`; `nic2`→`Eth1/18` (access VLAN 99, `10.30.99.0/24` — the
FortiGate WAN lives here as `10.30.99.99`) → `vmbr1`; and `nic3`+`nic4`→
`Eth1/19–20`, bonded as the switch's `port-channel2` (LACP, native VLAN 999,
data VLANs 3/6/10/200/202) → the VLAN-aware `vmbr2` that carries the lab's
FortiGate-served segments (VLAN 200/202, plus a Proxmox-local VLAN 60 between the
FortiGate peers). The bond is documented in Volume XXVI, Chapter 05.

Emulators in use: **GNS3** and **EVE-NG** (FortiGate and other appliance images
imported per Volumes XIX and XXVI). The nine VMs above are the live inventory;
the FortiGate and FortiClient EMS builds are exercised by the Volume XIX labs.

## Management planes

- **iDRAC** on every Dell host — out-of-band console, power, virtual media
  (access ports on VLAN 1611).
- **Nexus `mgmt0`** on the OOB subnet `10.30.99.0/24`.
- **Proxmox web UI** at `https://10.30.161.10:8006` (host management on VLAN
  1611).

The next chapter draws all of this — the physical/network topology, the rack
elevation, and the logical VLAN plan.
