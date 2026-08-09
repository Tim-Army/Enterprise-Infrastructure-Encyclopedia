# Chapter 04: Current Device Configurations

Chapter 02 inventoried *what* is in the rack; this chapter records *how the three
infrastructure devices below the hypervisors are configured*, from their live
running state. Those three are the **ISP modem** (the internet handoff), the
**UCGF** (the edge router, firewall, DHCP server, and Wi‑Fi controller), and
**N9K1** (the Layer‑2 switch fabric). As everywhere in this volume, no
credentials, keys, or public addressing are recorded — only roles, addressing,
and configuration structure.

## The edge path

The three devices layer from the internet inward:

```text
ISP modem ──▶ UCGF port 5 (WAN1, "ISP") ──▶ UCGF routes + NATs the lab VLANs
          ──▶ UCGF port 6 (SFP+ 10 GbE, "N9K1-P48") ──▶ N9K1 Eth1/48 trunk
          ──▶ N9K1 48× 10 Gb switch fabric ──▶ the five PowerEdge hosts
```

The division of labor is clean: **the UCGF does all Layer 3** (routing between
VLANs, DHCP, NAT, edge firewalling, Wi‑Fi); **N9K1 is pure Layer 2** (it trunks
VLANs to the hosts and has no SVIs or routing beyond its own management
interface). That is why every subnet's gateway (`.1`) lives on the UCGF and the
Nexus `mgmt0` default‑routes to `10.30.99.1`.

## N9K1 — Cisco Nexus 9000 C9396PX (Layer 2 fabric)

| Item | Value |
|------|-------|
| Model | Cisco Nexus9000 **C9396PX** (48× SFP+ 10 Gb fixed + a 12× 40 Gb QSFP+ uplink module) |
| Hostname | `nexus-9k-1` |
| NX-OS | `7.0(3)I2(2d)` (BIOS 07.41) |
| Role | Pure Layer 2 — VLAN trunking to hosts; all routing/DHCP is on the UCGF |
| Features | `lacp`, `lldp`; `system default switchport shutdown` (ports shut unless explicitly enabled); `copp profile strict`; RSTP |
| Management | `mgmt0` = `10.30.99.250/24` in the `management` VRF; VRF default route `0.0.0.0/0 → 10.30.99.1` (the UCGF) |
| Jumbo | Host trunks set `mtu 9216` |

**VLANs defined:** `1,3,8,99,200,202,999,1610-1615,3939` — named `Servers` (3),
`SDx` (8), `core-mgmt` (99), `native` (999), `Native-VLAN-1610`, `External-Mgmt`
(1611), `vMotion` (1612), `vSAN` (1613), `VmNetwork-A` (1614), `VmNetwork-B`
(1615), `Private` (3939). (VLANs 200/202 are trunked to `proxmox-1` for the
FortiGate lab; see the note under the UCGF below.)

**Port-channels:**

| PC | Members | Mode | Native | Allowed VLANs | Purpose |
|----|---------|------|--------|---------------|---------|
| `port-channel1` | Eth1/47 (`active`) | trunk | 1611 | 1,3,8,1611-1615,3939 | Northbound LACP uplink |
| `port-channel2` | Eth1/19–20 (`active`) | trunk | 999 | 3,6,10,200,202 | **`proxmox-1` data bond** (`nic3`+`nic4`) |

**Key interface roles:**

| Ports | Description | Mode |
|-------|-------------|------|
| Eth1/1–16 | Host trunks `ru08`–`ru11` (`vmnic0`–`vmnic3` each), native 1611, allowed 3,8,1611-1615,3939, MTU 9216 | trunk |
| Eth1/17 | `ru12;nic1` — `proxmox-1` management, `10.30.161.10/24` | access VLAN 1611 |
| Eth1/18 | `ru12;nic2` — `10.30.99.0/24` core-mgmt (the FortiGate WAN, `10.30.99.99`, lives here) | access VLAN 99 |
| Eth1/19–20 | `ru12;nic3-4` — data-VLAN bond (`port-channel2`) | trunk (native 999) |
| Eth1/30 | spare | access VLAN 1611 |
| Eth1/33–34 | `unraid-1` (`192.168.1.209`, VLAN 1) | access |
| Eth1/40–41 | `proxmox-idrac`, `unraid-idrac` | access VLAN 1611 |
| Eth1/47 | Northbound LACP uplink (`port-channel1`) | trunk |
| Eth1/48 | **UCGF port 6** — the 10 GbE data uplink (standalone trunk; allows 1,3,8,99,999,1611-1615,3939) | trunk |
| Eth2/1–12 | 40 Gb QSFP+ module — all unconfigured | — |

## UCGF — Ubiquiti UniFi Cloud Gateway Fiber (edge router / firewall / DHCP / Wi-Fi)

The UCGF (`CGF`/`UCG Fiber` in the UniFi Network console) is the lab's edge — it
routes between every VLAN, runs DHCP, NATs to the internet, applies the edge
firewall, and is the Wi‑Fi controller.

**Gateway ports (7):** RJ45 `1`–`5` (GbE), SFP+ `6`–`7` (10 GbE).

| Port | Name (label) | Assignment | Speed | Connects to |
|------|------|------------|-------|-------------|
| 1 | `ISPN9K1-mgmt0;10.30.99.205;VLAN-99` | Unassigned | GbE | N9K1 `mgmt0` (OOB, VLAN 99) |
| 2 | `MSP` | Unassigned | GbE | — |
| 3 | `AP` | Unassigned | GbE | access point |
| 4 | `AP` | Unassigned | GbE (PoE) | access point |
| 5 | `ISP` | **WAN1 (Primary, Online)** | GbE | ISP modem |
| 6 | `N9K1-P48` | Unassigned (LAN uplink) | **10 GbE (SFP+)** | N9K1 `Eth1/48` (data trunk) |
| 7 | `Office-Sw-1` | Unassigned | GbE | TP-Link 8-port Gigabit unmanaged switch (office) |

WAN mode is **Failover Only** (single primary WAN1); an automatic speed test runs
daily at 05:00.

**Routed networks (VLANs) — the authoritative lab plan.** The UCGF is the router
and DHCP server for each:

| VLAN | Name | Subnet | DHCP |
|------|------|--------|------|
| 1 | `Core_1` | `192.168.1.0/24` | Server |
| 2 | `Eve-ng_…` | `192.168.2.0/24` | None |
| 3 | `Servers` | `10.30.10.0/24` (+ IPv6 ULA) | Server |
| 4 | `Guest` | `10.30.100.0/24` | Server |
| 5 | `Doc_Box_5` | `10.30.101.0/24` | Server |
| 6 | `Workstations` | `10.30.12.0/24` (+ IPv6 ULA) | Server |
| 7 | `Printers` | `10.30.11.0/24` | Server |
| 8 | `SDx-10-1-255` | `10.1.255.0/24` | Server |
| 9 | `IoT_5G` | `10.30.200.0/24` | Server |
| 10 | `isp` | `192.168.10.0/24` | None |
| 40 | `Doc_Box_3` | `192.168.40.0/24` | Server |
| 90 | `Core_90` | `10.30.90.0/24` | Server |
| 98 | `Lab_Mgmt_98` | `10.30.98.0/24` | Server |
| 99 | `Core_Mgmt_99` | `10.30.99.0/24` (+ IPv6 ULA) | Server |
| 200 | `Lab_Core_200` | `10.31.0.0/24` | Server |
| 201 | `Lab_Enterprises_201` | `10.31.1.0/24` | Server |
| 202 | `Lab_Services_202` | `10.31.11.0/24` (+ IPv6 ULA) | Server |
| 301 | `Home_Core` | `10.30.0.0/24` | Server |
| 971 | `IoT_2G` | `192.168.97.0/24` | Server |
| 1610 | `Native_VLAN_1610` | `10.30.164.0/24` (+ IPv6 ULA) | Server |
| 1611 | `Lab_Mgmt_1611` | `10.30.161.0/24` (+ IPv6 ULA) | Server |
| 1612 | `vMotion` | `10.30.95.0/24` | None |
| 1613 | `vSAN` | `10.30.96.0/24` (+ IPv6 ULA) | Server |
| 1614 | `VmNetwork_A_1614` | `10.30.162.0/24` (+ IPv6 ULA) | Server |
| 1615 | `VmNetwork_B_1615` | `10.30.163.0/24` (+ IPv6 ULA) | Server |
| 2129 | `Eve-ng_NAT_…` | `172.29.129.0/24` | None |
| 4009 | `native` | `10.99.99.0/24` | Server |

> **FortiGate-lab tag reuse.** The Volume XIX FortiGate labs run their own
> internal segments on `proxmox-1`'s `vmbr2` using VLAN tags **200/202** with
> addressing `10.200.0.0/24` and `10.202.0.0/24`, gated and NATed *behind the
> FortiGate*. Those are distinct from the UCGF's routed `Lab_Core_200`
> (`10.31.0.0/24`) and `Lab_Services_202` (`10.31.11.0/24`) despite sharing the
> tag numbers — the FortiGate segments never leave `proxmox-1`, so the collision
> is harmless, but it is worth knowing when tracing a `10.200.x` address.

**Global L2 / switching settings:** Spanning Tree **RSTP**; IGMP snooping on
(queriers off — third-party switches); Jumbo Frames off; 802.1X off; Rogue-DHCP
detection off. Default RADIUS profile `Default (UCG Fiber)`.

**Firewall / security:** default security posture **Allow All**; gateway mDNS
proxy Auto. Named network lists used by policy include `RFC1918`, `Management`,
`Main_GW`, `Doc_Box_Group`, `VPN_7.0` (`192.168.7.0/24`), `NIST`,
`Block_Internet_IPv4`/`IPv6`, `Allow_Internet_IPv4`, and `IPv6_Mgmt`.
**CyberSecure** is on the **Standard (Free)** tier (~32,000 threat signatures,
updated daily); Intrusion Prevention and Region Blocking are off, Encrypted DNS
off, and the block page is served with the UniFi SSL certificate.

**Wi-Fi (SSIDs):**

| SSID | Network | Band | Security |
|------|---------|------|----------|
| `Platinum` | `Core_90` (90) | 5 GHz | WPA2 |
| `Platinum_Silver_5G` | Native | 5 GHz | WPA2 |
| `Platinum_IoT_2G` | Native | 2.4 GHz | WPA2 |
| `Platinum_Silver_2G` | Native | 2.4 GHz | WPA2 |
| `Doc_Box` | Native | 2.4 / 5 GHz | WPA2 / WPA3 |

Channel widths run 20 MHz (2.4 GHz) / 80 MHz (5 GHz) / 320 MHz (6 GHz), Extended
5 GHz (DFS) enabled, wireless meshing on with the gateway as mesh monitor.

## ISP modem — internet handoff

The ISP modem provides the WAN uplink into **UCGF port 5 (WAN1)** — the WAN
interface carries the (redacted) public IP, and WAN mode is Failover Only with
this as the sole primary. *The service provider, modem model, and public IP
address are intentionally not recorded in this volume.*

## N9K1 running-config (verbatim)

The complete `show running-config` from `nexus-9k-1`, exactly as it runs. The
only changes are the two `username … password 5 …` hashes, replaced with
`<redacted>` — publishing a password hash invites offline cracking, and this
volume records no credentials. Everything else is verbatim.

```text
version 7.0(3)I2(2d)
switchname nexus-9k-1
vdc nexus-9k-1 id 1
  limit-resource vlan minimum 16 maximum 4094
  limit-resource vrf minimum 2 maximum 4096
  limit-resource port-channel minimum 0 maximum 511
  limit-resource u4route-mem minimum 248 maximum 248
  limit-resource u6route-mem minimum 96 maximum 96
  limit-resource m4route-mem minimum 58 maximum 58
  limit-resource m6route-mem minimum 8 maximum 8

feature lacp
feature lldp

username admin password 5 <redacted>  role network-admin
username tim password 5 <redacted>  role network-operator
username tim role network-admin
ssh key rsa 2048
no ip domain-lookup
system default switchport shutdown
copp profile strict
rmon event 1 log trap public description FATAL(1) owner PMON@FATAL
rmon event 2 log trap public description CRITICAL(2) owner PMON@CRITICAL
rmon event 3 log trap public description ERROR(3) owner PMON@ERROR
rmon event 4 log trap public description WARNING(4) owner PMON@WARNING
rmon event 5 log trap public description INFORMATION(5) owner PMON@INFO

vlan 1,3,8,99,200,202,999,1610-1615,3939
vlan 3
  name Servers
vlan 8
  name SDx
vlan 99
  name core-mgmt
vlan 999
  name native
vlan 1610
  name Native-VLAN-1610
vlan 1611
  name External-Mgmt
vlan 1612
  name vMotion
vlan 1613
  name vSAN
vlan 1614
  name VmNetwork-A
vlan 1615
  name VmNetwork-B
vlan 3939
  name Private

vrf context management
  ip route 0.0.0.0/0 10.30.99.1

interface port-channel1
  switchport mode trunk
  switchport trunk native vlan 1611
  switchport trunk allowed vlan 1,3,8,1611-1615,3939

interface port-channel2
  description e1/19-20;ru12;nic3-4;vlans-3,6,10,200,202;data-vlans
  switchport mode trunk
  switchport trunk native vlan 999
  switchport trunk allowed vlan 3,6,10,200,202
  spanning-tree bpduguard enable
  spanning-tree bpdufilter enable
  flowcontrol receive on

interface Ethernet1/1
  description ru08;vmnic0
  switchport mode trunk
  switchport trunk native vlan 1611
  switchport trunk allowed vlan 3,8,1611-1615,3939
  spanning-tree bpduguard enable
  spanning-tree bpdufilter enable
  flowcontrol receive on
  mtu 9216
  no shutdown

interface Ethernet1/2
  description ru08;vmnic1
  switchport mode trunk
  switchport trunk native vlan 1611
  switchport trunk allowed vlan 3,8,1611-1615,3939
  spanning-tree bpduguard enable
  spanning-tree bpdufilter enable
  flowcontrol receive on
  mtu 9216
  no shutdown

interface Ethernet1/3
  description ru08;vmnic2
  switchport mode trunk
  switchport trunk native vlan 1611
  switchport trunk allowed vlan 3,8,1611-1615,3939
  spanning-tree bpduguard enable
  spanning-tree bpdufilter enable
  flowcontrol receive on
  mtu 9216
  no shutdown

interface Ethernet1/4
  description ru08;vmnic3
  switchport mode trunk
  switchport trunk native vlan 1611
  switchport trunk allowed vlan 3,8,1611-1615,3939
  spanning-tree bpduguard enable
  spanning-tree bpdufilter enable
  flowcontrol receive on
  mtu 9216
  no shutdown

interface Ethernet1/5
  description ru09;vmnic0
  switchport mode trunk
  switchport trunk native vlan 1611
  switchport trunk allowed vlan 3,8,1611-1615,3939
  spanning-tree bpduguard enable
  spanning-tree bpdufilter enable
  flowcontrol receive on
  mtu 9216
  no shutdown

interface Ethernet1/6
  description ru09;vmnic1
  switchport mode trunk
  switchport trunk native vlan 1611
  switchport trunk allowed vlan 3,8,1611-1615,3939
  spanning-tree bpduguard enable
  spanning-tree bpdufilter enable
  flowcontrol receive on
  mtu 9216
  no shutdown

interface Ethernet1/7
  description ru09;vmnic2
  switchport mode trunk
  switchport trunk native vlan 1611
  switchport trunk allowed vlan 3,8,1611-1615,3939
  spanning-tree bpduguard enable
  spanning-tree bpdufilter enable
  flowcontrol receive on
  mtu 9216
  no shutdown

interface Ethernet1/8
  description ru09;vmnic3
  switchport mode trunk
  switchport trunk native vlan 1611
  switchport trunk allowed vlan 3,8,1611-1615,3939
  spanning-tree bpduguard enable
  spanning-tree bpdufilter enable
  flowcontrol receive on
  mtu 9216
  no shutdown

interface Ethernet1/9
  description ru10;vmnic0
  switchport mode trunk
  switchport trunk native vlan 1611
  switchport trunk allowed vlan 3,8,1611-1615,3939
  spanning-tree bpduguard enable
  spanning-tree bpdufilter enable
  flowcontrol receive on
  mtu 9216
  no shutdown

interface Ethernet1/10
  description ru10;vmnic1
  switchport mode trunk
  switchport trunk native vlan 1611
  switchport trunk allowed vlan 3,8,1611-1615,3939
  spanning-tree bpduguard enable
  spanning-tree bpdufilter enable
  flowcontrol receive on
  mtu 9216
  no shutdown

interface Ethernet1/11
  description ru10;vmnic2
  switchport mode trunk
  switchport trunk native vlan 1611
  switchport trunk allowed vlan 3,8,1611-1615,3939
  spanning-tree bpduguard enable
  spanning-tree bpdufilter enable
  flowcontrol receive on
  mtu 9216
  no shutdown

interface Ethernet1/12
  description ru10;vmnic3
  switchport mode trunk
  switchport trunk native vlan 1611
  switchport trunk allowed vlan 3,8,1611-1615,3939
  spanning-tree bpduguard enable
  spanning-tree bpdufilter enable
  flowcontrol receive on
  mtu 9216
  no shutdown

interface Ethernet1/13
  description ru11;vmnic0
  switchport mode trunk
  switchport trunk native vlan 1611
  switchport trunk allowed vlan 3,8,1611-1615,3939
  spanning-tree bpduguard enable
  spanning-tree bpdufilter enable
  flowcontrol receive on
  mtu 9216
  no shutdown

interface Ethernet1/14
  description ru11;vmnic1
  switchport mode trunk
  switchport trunk native vlan 1611
  switchport trunk allowed vlan 3,8,1611-1615,3939
  spanning-tree bpduguard enable
  spanning-tree bpdufilter enable
  flowcontrol receive on
  mtu 9216
  no shutdown

interface Ethernet1/15
  description ru11;vmnic2
  switchport mode trunk
  switchport trunk native vlan 1611
  switchport trunk allowed vlan 3,8,1611-1615,3939
  spanning-tree bpduguard enable
  spanning-tree bpdufilter enable
  flowcontrol receive on
  mtu 9216
  no shutdown

interface Ethernet1/16
  description ru11;vmnic3
  switchport mode trunk
  switchport trunk native vlan 1611
  switchport trunk allowed vlan 3,8,1611-1615,3939
  spanning-tree bpduguard enable
  spanning-tree bpdufilter enable
  flowcontrol receive on
  mtu 9216
  no shutdown

interface Ethernet1/17
  description ru12;nic1;10.30.161.10/24;vlan-1611;proxmox-1
  switchport access vlan 1611
  spanning-tree port type edge
  spanning-tree bpduguard enable
  spanning-tree bpdufilter enable
  flowcontrol receive on
  no shutdown

interface Ethernet1/18
  description ru12;nic2;10.30.99.0/24;vlan-99;core-mgmt
  switchport access vlan 99
  spanning-tree port type edge
  spanning-tree bpduguard enable
  spanning-tree bpdufilter enable
  flowcontrol receive on
  no shutdown

interface Ethernet1/19
  description ru12;nic3;vlans-3,6,10,200,202;data-vlans
  switchport mode trunk
  switchport trunk native vlan 999
  switchport trunk allowed vlan 3,6,10,200,202
  spanning-tree bpduguard enable
  spanning-tree bpdufilter enable
  flowcontrol receive on
  channel-group 2 mode active
  no shutdown

interface Ethernet1/20
  description ru12;nic4;vlans-3,6,10,200,202;data-vlans
  switchport mode trunk
  switchport trunk native vlan 999
  switchport trunk allowed vlan 3,6,10,200,202
  spanning-tree bpduguard enable
  spanning-tree bpdufilter enable
  flowcontrol receive on
  channel-group 2 mode active
  no shutdown

interface Ethernet1/21
  switchport mode trunk
  switchport trunk native vlan 1611
  switchport trunk allowed vlan 1611-1615,3939
  spanning-tree bpduguard enable
  spanning-tree bpdufilter enable
  flowcontrol receive on
  mtu 9216
  no shutdown

interface Ethernet1/22
  switchport mode trunk
  switchport trunk native vlan 1611
  switchport trunk allowed vlan 1611-1615,3939
  spanning-tree bpduguard enable
  spanning-tree bpdufilter enable
  flowcontrol receive on
  mtu 9216
  no shutdown

interface Ethernet1/23
  switchport mode trunk
  switchport trunk native vlan 1611
  switchport trunk allowed vlan 1611-1615,3939
  spanning-tree bpduguard enable
  spanning-tree bpdufilter enable
  flowcontrol receive on
  mtu 9216
  no shutdown

interface Ethernet1/24
  switchport mode trunk
  switchport trunk native vlan 1611
  switchport trunk allowed vlan 1611-1615,3939
  spanning-tree bpduguard enable
  spanning-tree bpdufilter enable
  flowcontrol receive on
  mtu 9216
  no shutdown

interface Ethernet1/25

interface Ethernet1/26

interface Ethernet1/27

interface Ethernet1/28

interface Ethernet1/29

interface Ethernet1/30
  switchport access vlan 1611
  no shutdown

interface Ethernet1/31

interface Ethernet1/32

interface Ethernet1/33
  description unraid-1;192.168.1.209/24;vlan-1
  no shutdown

interface Ethernet1/34
  description unraid-1;192.168.1.209/24;vlan-1
  no shutdown

interface Ethernet1/35

interface Ethernet1/36

interface Ethernet1/37

interface Ethernet1/38

interface Ethernet1/39

interface Ethernet1/40
  description proxmox-idrac
  switchport access vlan 1611
  no shutdown

interface Ethernet1/41
  description unraid-idrac
  switchport access vlan 1611
  no shutdown

interface Ethernet1/42

interface Ethernet1/43

interface Ethernet1/44

interface Ethernet1/45

interface Ethernet1/46

interface Ethernet1/47
  switchport mode trunk
  switchport trunk native vlan 1611
  switchport trunk allowed vlan 1,3,8,1611-1615,3939
  channel-group 1 mode active
  no shutdown

interface Ethernet1/48
  switchport mode trunk
  switchport trunk native vlan 1611
  switchport trunk allowed vlan 1,3,8,99,999,1611-1615,3939
  no shutdown

interface Ethernet2/1

interface Ethernet2/2

interface Ethernet2/3

interface Ethernet2/4

interface Ethernet2/5

interface Ethernet2/6

interface Ethernet2/7

interface Ethernet2/8

interface Ethernet2/9

interface Ethernet2/10

interface Ethernet2/11

interface Ethernet2/12

interface mgmt0
  vrf member management
  ip address 10.30.99.250/24
line console
  exec-timeout 0
line vty
boot nxos bootflash:/nxos.7.0.3.I2.2d.bin
```
