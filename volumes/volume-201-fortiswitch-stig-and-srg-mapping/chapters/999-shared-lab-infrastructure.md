# Chapter 999: Shared Lab Infrastructure

## Learning Objectives

- Use the lab address plan: `10.201.0.0/16` for IPv4 and
  `fd00:db8:201::/112` for IPv6, split into the segments every lab in this
  volume shares.
- Name the hosts, services, and links the labs depend on, and tie each one to
  the prerequisite (P1 to P17) it satisfies.
- Build the gateway, the service hosts, and the baseline configuration of the
  two switches under test.
- Connect a switch to RADIUS, syslog, NTP, SNMPv3, flow collectors, and a
  backup server, and prove each connection.
- Reserve address space for a new lab without overlapping an existing one.
- Reset the lab to the baseline between labs and keep evidence for each run.

## Theory and Architecture

### What this chapter is for

Chapters 01 to 03 map FortiSwitch settings to SRG requirements, and every
requirement a lab proves needs something around the switch: an authentication
server, a log server, a time source, a routing peer, a host that misbehaves.
This chapter defines that surroundings once. A lab chapter in this volume does
not draw its own network. It names the segments, hosts, and prerequisites it
uses from this chapter, lists only what it adds, and starts from the baseline
this chapter builds.

The chapter is numbered 999 so that it stays last, after the as-built chapter,
and so that its number does not change as lab chapters are added before it.

### The two switches under test

The workbook behind Chapters 01 to 03 records support for two models, so the
lab has one of each.

| Name | Model | License for Layer 3 features | Role |
| --- | --- | --- | --- |
| `sw-648f-1` | FS-648F-FPOE | Advanced Features License `FS-SW-LIC-600` | Access switch: 802.1X, MAB, DHCP snooping, port security, and routing |
| `sw-2048f-1` | FS-2048F | Advanced Features License `FS-SW-LIC-2000` | Aggregation switch: routing, VXLAN, and the second end of every pair test |

Several requirements are not supported on every model (for example dynamic ARP
inspection and uRPF on the FS-648F-FPOE). Prerequisite P9 in the workbook is
the check: a lab for such a requirement names the model it runs on, and a lab
for a requirement the model cannot meet records the gap instead of a result.
FortiSwitch has no virtual appliance, so the switches are hardware. Everything
else in the lab can be virtual.

### Topology

![Shared lab network. Two FortiSwitches, sw-648f-1 (FS-648F-FPOE) and sw-2048f-1 (FS-2048F), are joined by routed link L5 (VLAN 2005). Each has an 802.1Q trunk to one hypervisor that hosts the gateway gw-201, the service hosts svc-201a and svc-201b, ca-201, dhcp-201, admin-201, the segment 42 hosts, an optional FortiGate fgt-201, and the routing peers rtr-peer-1 (AS 65202) and rtr-peer-2 (AS 65203). Routed links L1 and L2 join sw-648f-1 to the peers, and L3 and L4 join sw-2048f-1 to the peers. Test endpoints connect directly to the switches, and a dashed out-of-band management network joins each switch's management port to gw-201.](../../../diagrams/volume-201-fortiswitch-stig-and-srg-mapping/chapter-999-shared-lab-topology.svg)

Everything above the switches is virtual and runs on one hypervisor. Each
switch needs one trunk to the hypervisor (T1 and T2 in the diagram), its
management port, one port for each routed link (L1 to L5), and one port for
each physical test endpoint.

### Address plan

All lab addresses come from two blocks.

| Block | Use |
| --- | --- |
| `10.201.0.0/16` | IPv4. The third octet is the segment number, so `10.201.40.0/24` is segment 40. |
| `fd00:db8:201::/112` | IPv6. The last 16 bits are `<segment><host>` in hexadecimal, so segment 40 (`0x28`) is `fd00:db8:201::2800/120`. |

The IPv6 block is a /112, which holds 65,536 addresses, enough for 256 /120
segments of 256 addresses each. A /112 cannot be split into /64 subnets, and
stateless address autoconfiguration (SLAAC) needs a /64, so IPv6 hosts in this
lab take static addresses or addresses from a stateful DHCPv6 server. A
lab that needs router advertisements uses a link-local test as described in
its own chapter. The prefix is in the unique local range (`fc00::/7`), so it is
never routed on the internet.

In every segment the host part follows one convention, so a host keeps the same
number in IPv4 and IPv6 (`.10` is `::a` in the host group).

| Host part | Use |
| --- | --- |
| `.1` | Default gateway (`gw-201`, or the peer router on a routed segment) |
| `.2` to `.9` | Infrastructure that shares a segment with hosts (for example `dhcp-201`) |
| `.10` to `.99` | Static servers and hosts |
| `.100` to `.199` | DHCP scope |
| `.200` to `.254` | Test endpoints and attackers |

#### Segments

| Segment | VLAN | Name | IPv4 | IPv6 | Gateway | Purpose |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | none (physical) | OOB-Mgmt | `10.201.0.0/24` | `fd00:db8:201::/120` | .1 gw-201 | Switch management ports, gateway management port |
| 10 | 10 | Lab-Services | `10.201.10.0/24` | `fd00:db8:201::a00/120` | .1 gw-201 | RADIUS, syslog, NTP, SNMP, flow, files, CA, DHCP |
| 20 | 20 | Admin | `10.201.20.0/24` | `fd00:db8:201::1400/120` | .1 gw-201 | Administrator workstation and jump host |
| 30 | 30 | Switch-Mgmt | `10.201.30.0/24` | `fd00:db8:201::1e00/120` | .1 gw-201 | In-band management SVIs of the switches (P10) |
| 40 | 40 | Users-8021X | `10.201.40.0/24` | `fd00:db8:201::2800/120` | .1 gw-201 | 802.1X authenticated endpoints |
| 41 | 41 | Users-MAB | `10.201.41.0/24` | `fd00:db8:201::2900/120` | .1 gw-201 | MAC authentication bypass endpoints |
| 42 | 42 | Static-Hosts | `10.201.42.0/24` | `fd00:db8:201::2a00/120` | .1 gw-201 | Hosts without DHCP; IP-to-MAC bindings (P14); test attacker |
| 50 | 50 | Guest-AuthFail | `10.201.50.0/24` | `fd00:db8:201::3200/120` | .1 gw-201 | Guest and authentication-failure VLAN |
| 60 | 60 | Unused | `10.201.60.0/24` | `fd00:db8:201::3c00/120` | none | Parking VLAN for unused ports; no hosts, no gateway |
| 99 | 99 | Native-Dead | `10.201.99.0/24` | `fd00:db8:201::6300/120` | none | Native VLAN on trunks; no hosts, no gateway |
| 100 | none (isolated LAN) | Console-OOB | `10.201.100.0/24` | `fd00:db8:201::6400/120` | none | Optional: break-glass network for the console server's NET2 and `oob-admin-201` (Chapter 08) |
| 200 | 2001-2005 | Routed-Links | `10.201.200.0/24` | `fd00:db8:201::c800/120` | none | Point-to-point links, one /31 (IPv4) and /127 (IPv6) each |
| 210 | behind rtr-peer-1 | Peer1-Nets | `10.201.210.0/24` | `fd00:db8:201::d200/120` | rtr-peer-1 | Prefixes advertised by rtr-peer-1 (AS 65202) |
| 211 | behind rtr-peer-2 | Peer2-Nets | `10.201.211.0/24` | `fd00:db8:201::d300/120` | rtr-peer-2 | Prefixes advertised by rtr-peer-2 (AS 65203) |
| 220 | behind rtr-peer-1 | Mcast-Source | `10.201.220.0/24` | `fd00:db8:201::dc00/120` | rtr-peer-1 | Multicast source network for PIM-SSM labs |
| 230 | 230 (VNI 230) | VXLAN-Tenant | `10.201.230.0/24` | `fd00:db8:201::e600/120` | none | Tenant network carried over VXLAN between the two switches |
| 250 | none (loopbacks) | Loopbacks | `10.201.250.0/24` | `fd00:db8:201::fa00/120` | none | One /32 and /128 per router |
| 254 | FortiLink | FortiLink | `10.201.254.0/24` | `fd00:db8:201::fe00/120` | .1 fgt-201 | FortiLink interface of fgt-201 (managed-mode labs only) |

Segment 0 is the out-of-band network: it is reached through the switches'
management ports (and, in the optional console lab of
[Chapter 08](08-opengear-im7216-console-server-and-optional-console-lab.md),
the console server's NET1) and never carries test traffic. Segments 100 to 199 are
reserved for lab-specific segments: a lab that needs its own VLAN takes the
next free number in that range (VLAN ID equal to the third octet) and records it
in its own chapter. Every other number outside 100 to 199 that is not in the table is unassigned,
so a shared segment can be added without renumbering.

#### Hosts

| Host | Role | Prerequisite | Segment | IPv4 | IPv6 |
| --- | --- | --- | --- | --- | --- |
| gw-201 | Default gateway and firewall: FortiGate-VM or a Linux router VM | P7 (if a FortiGate) | 0 (management port) | `10.201.0.1` | `fd00:db8:201::1` |
|  |  |  | 10 | `10.201.10.1` | `fd00:db8:201::a01` |
|  |  |  | 20 | `10.201.20.1` | `fd00:db8:201::1401` |
|  |  |  | 30 | `10.201.30.1` | `fd00:db8:201::1e01` |
|  |  |  | 40 | `10.201.40.1` | `fd00:db8:201::2801` |
|  |  |  | 41 | `10.201.41.1` | `fd00:db8:201::2901` |
|  |  |  | 42 | `10.201.42.1` | `fd00:db8:201::2a01` |
|  |  |  | 50 | `10.201.50.1` | `fd00:db8:201::3201` |
| radius-201a | RADIUS server 1 (FreeRADIUS) on svc-201a | P1, P2 | 10 | `10.201.10.10` | `fd00:db8:201::a0a` |
| radius-201b | RADIUS server 2 on svc-201b | P1, P2 | 10 | `10.201.10.11` | `fd00:db8:201::a0b` |
| tacacs-201 | TACACS+ server (optional) on svc-201a | P1 | 10 | `10.201.10.12` | `fd00:db8:201::a0c` |
| syslog-201a | Central syslog 1 (rsyslog, TLS over TCP) on svc-201a | P4 | 10 | `10.201.10.20` | `fd00:db8:201::a14` |
| syslog-201b | Central syslog 2 on svc-201b | P4 | 10 | `10.201.10.21` | `fd00:db8:201::a15` |
| ntp-201a | Authenticated NTP server 1 (chrony) on svc-201a | P5 | 10 | `10.201.10.30` | `fd00:db8:201::a1e` |
| ntp-201b | Authenticated NTP server 2 on svc-201b | P5 | 10 | `10.201.10.31` | `fd00:db8:201::a1f` |
| nms-201 | SNMPv3 manager on svc-201a | P6 | 10 | `10.201.10.40` | `fd00:db8:201::a28` |
| flow-201 | sFlow, NetFlow, and IPFIX collector on svc-201b | P17 | 10 | `10.201.10.50` | `fd00:db8:201::a32` |
| files-201 | SFTP and TFTP server on svc-201b | P15, P16 | 10 | `10.201.10.60` | `fd00:db8:201::a3c` |
| ca-201 | Lab certificate authority with SCEP (stands in for the DoD CA) | P3 | 10 | `10.201.10.70` | `fd00:db8:201::a46` |
| dhcp-201 | DHCP server (Kea); also on VLANs 40, 41, and 50 | P12 | 10 (management) | `10.201.10.80` | `fd00:db8:201::a50` |
|  |  |  | 40 (scope .100-.199) | `10.201.40.2` | `fd00:db8:201::2802` |
|  |  |  | 41 (scope .100-.199) | `10.201.41.2` | `fd00:db8:201::2902` |
|  |  |  | 50 (scope .100-.199) | `10.201.50.2` | `fd00:db8:201::3202` |
| admin-201 | Administrator workstation and jump host |  | 20 | `10.201.20.10` | `fd00:db8:201::140a` |
| sw-648f-1 | FS-648F-FPOE under test | P8, P9, P10 | 0 (management port) | `10.201.0.11` | `fd00:db8:201::b` |
|  |  |  | 30 (management SVI) | `10.201.30.11` | `fd00:db8:201::1e0b` |
|  |  |  | 250 (loopback) | `10.201.250.11` | `fd00:db8:201::fa0b` |
| sw-2048f-1 | FS-2048F under test | P8, P9, P10 | 0 (management port) | `10.201.0.12` | `fd00:db8:201::c` |
|  |  |  | 30 (management SVI) | `10.201.30.12` | `fd00:db8:201::1e0c` |
|  |  |  | 250 (loopback) | `10.201.250.12` | `fd00:db8:201::fa0c` |
| fgt-201 | FortiGate for FortiLink managed mode (optional) | P7 | 254 (FortiLink interface) | `10.201.254.1` | `fd00:db8:201::fe01` |
| rtr-peer-1 | Routing peer 1 (FRR VM or FortiGate-VM), AS 65202 | P11 | 250 (loopback) | `10.201.250.21` | `fd00:db8:201::fa15` |
| rtr-peer-2 | Routing peer 2, AS 65203 | P11 | 250 (loopback) | `10.201.250.22` | `fd00:db8:201::fa16` |
| static-1 | Statically addressed host | P14 | 42 | `10.201.42.10` | `fd00:db8:201::2a0a` |
| static-2 | Statically addressed host | P14 | 42 | `10.201.42.11` | `fd00:db8:201::2a0b` |
| attacker-201 | Test host for spoofing and flooding tests |  | 42 | `10.201.42.200` | `fd00:db8:201::2ac8` |
| og-201 | Optional OpenGear console server (Chapter 08) |  | 0 (NET1) | `10.201.0.13` | `fd00:db8:201::d` |
|  |  |  | 100 (NET2) | `10.201.100.2` | `fd00:db8:201::6402` |
| oob-admin-201 | Optional break-glass laptop (Chapter 08) |  | 100 | `10.201.100.10` | `fd00:db8:201::640a` |
| mcast-src-201 | Multicast source behind rtr-peer-1 |  | 220 | `10.201.220.10` | `fd00:db8:201::dc0a` |
| vx-host-a | VXLAN tenant host on sw-648f-1 |  | 230 | `10.201.230.10` | `fd00:db8:201::e60a` |
| vx-host-b | VXLAN tenant host on sw-2048f-1 |  | 230 | `10.201.230.11` | `fd00:db8:201::e60b` |

The service hosts are two Linux virtual machines (`svc-201a` and `svc-201b`)
that each carry several of the service addresses as secondary addresses. Two
physical hosts for each service would mean more machines than the labs need,
but the requirements ask for two servers (two log servers, two NTP sources), so
each pair is split across the two machines.

#### Routed links

Each link between two routers is a /31 in IPv4 (RFC 3021) and a /127 in IPv6
(RFC 6164), with the lower address on the first router named.

| Link | VLAN | Lower address (IPv4) | Upper address (IPv4) | Lower address (IPv6) | Upper address (IPv6) | Ends |
| --- | --- | --- | --- | --- | --- | --- |
| L1 | 2001 | `10.201.200.0/31` (sw-648f-1) | `10.201.200.1/31` (rtr-peer-1) | `fd00:db8:201::c800/127` | `fd00:db8:201::c801/127` | sw-648f-1 to rtr-peer-1 |
| L2 | 2002 | `10.201.200.2/31` (sw-648f-1) | `10.201.200.3/31` (rtr-peer-2) | `fd00:db8:201::c802/127` | `fd00:db8:201::c803/127` | sw-648f-1 to rtr-peer-2 |
| L3 | 2003 | `10.201.200.4/31` (sw-2048f-1) | `10.201.200.5/31` (rtr-peer-1) | `fd00:db8:201::c804/127` | `fd00:db8:201::c805/127` | sw-2048f-1 to rtr-peer-1 |
| L4 | 2004 | `10.201.200.6/31` (sw-2048f-1) | `10.201.200.7/31` (rtr-peer-2) | `fd00:db8:201::c806/127` | `fd00:db8:201::c807/127` | sw-2048f-1 to rtr-peer-2 |
| L5 | 2005 | `10.201.200.8/31` (sw-648f-1) | `10.201.200.9/31` (sw-2048f-1) | `fd00:db8:201::c808/127` | `fd00:db8:201::c809/127` | sw-648f-1 to sw-2048f-1 |

Each link is a VLAN (2001 to 2005) with a Layer 3 interface on each end. Routed
protocol labs use these links and no others.

#### Routing parameters

| Item | Value |
| --- | --- |
| Lab switches | Autonomous system 65201 (private range, RFC 6996) |
| `rtr-peer-1` | AS 65202 |
| `rtr-peer-2` | AS 65203 |
| OSPF and OSPFv3 | Area `0.0.0.0` on L5; per-lab areas are set in the lab |
| Router ID | The router's IPv4 loopback (`10.201.250.<host>`) |
| Multicast | PIM-SSM range `232.0.0.0/8` and `ff3e::/32`; source `mcast-src-201` |
| VXLAN | VNI 230 carries segment 230 |
| Routing keys | One key per lab, generated for that lab; never reused between labs |

### How prerequisites map to this lab

The workbook lists 17 prerequisites (P1 to P17). This chapter satisfies each
one with a host or a baseline setting, so a lab chapter can say "P4" and mean
`syslog-201a` and `syslog-201b`.

| Prerequisite | Satisfied by |
| --- | --- |
| P1, P2: RADIUS or TACACS+ servers and a user group | `radius-201a`, `radius-201b`, and `tacacs-201` (optional), with the group `lab-radius` on each switch |
| P3: PKI and the DoD CA certificate | `ca-201`, a lab CA with SCEP. It stands in for the DoD CA, so a lab can prove the mechanism but not DoD trust |
| P4: Central syslog with TLS over TCP | `syslog-201a`, `syslog-201b` |
| P5: Authenticated NTP | `ntp-201a`, `ntp-201b` |
| P6: SNMPv3 manager | `nms-201` |
| P7: FortiGate managing the switch over FortiLink | `fgt-201` on segment 254, used only by managed-mode labs |
| P8: Advanced Features License | Installed on both switches (Lab 999.3) |
| P9: A model that supports the feature | `sw-648f-1` and `sw-2048f-1` |
| P10: Management interface with an address | The VLAN 30 management SVI on each switch |
| P11: Routing protocol with matching keys on every peer | `rtr-peer-1`, `rtr-peer-2`, and L1 to L5 |
| P12: DHCP snooping on the VLAN | `dhcp-201` is the trusted server; each lab enables snooping per VLAN |
| P13: User, native, management, and unused VLANs | VLANs 10 to 99 on the switches (Lab 999.3) |
| P14: IP-to-MAC bindings for static hosts | `static-1`, `static-2` on segment 42 |
| P15: SFTP server for configuration backups | `files-201` |
| P16: File server for firmware images | `files-201` (TFTP) |
| P17: Flow collector | `flow-201` |

## Design Considerations

- **Segment numbers equal VLAN IDs and third octets.** A reader who sees
  `10.201.41.150` knows it is in VLAN 41 and in IPv6 segment `0x29`. The
  convention is worth more than a tidy address plan.
- **IPv4 and IPv6 are dual-stack from the start.** Several requirements name
  IPv6 (for example the Router SRG's IPv6 requirements and the IPv6 forms of the
  FortiSwitch features), and adding a second address family to a finished lab is
  harder than building both at once.
- **One gateway, not one per segment.** `gw-201` holds `.1` on every shared
  segment. The switches carry only the management SVI in the baseline, so a
  Layer 2 lab proves its own switch behavior and a Layer 3 lab adds interfaces
  deliberately. If the switches also routed the user segments, a failed test
  could not be separated from a routing side effect.
- **The routed peers are separate from the gateway.** Router requirements
  (neighbor authentication, route filtering, maximum prefixes) need an
  adversary-shaped peer that can send bad routes. `rtr-peer-1` and
  `rtr-peer-2` are for that, and `gw-201` stays quiet.
- **Two of every redundant service.** The requirements ask for two log servers,
  two NTP sources, and two authentication servers. The lab proves that the
  switch fails over, which one server cannot show.
- **A lab CA is not the DoD CA.** `ca-201` lets a lab prove certificate
  enrollment, RadSec, and syslog TLS. It cannot prove that the switch trusts the
  DoD PKI. Where a requirement names the DoD CA, the lab chapter says what the
  test covers and what stays a procedural check.
- **Hardware you do not own.** The FS-648F-FPOE and FS-2048F are the models in
  the workbook. A lab run on another FortiSwitch model proves the command, not
  the model's support, and the chapter records the model it used.
- **Isolation.** `10.201.0.0/16` is separate from the `10.30.x.x` addresses of
  the lab in Volume CM, and from the `10.255.1.0/24` FortiLink network in Volume
  CLXXIV. Do not route the lab into either. `gw-201` NATs to the internet only
  for package installs and firmware downloads.
- **Secrets are generated, stored, and never shown in the book.** The command
  samples use `<SECRET>` placeholders. A lab generates its own values (for
  example `openssl rand -base64 24`) and keeps them in a password manager.

## Implementation and Automation

### Addressing and naming rules

1. Take the segment from the table above. Do not create a segment in 0 to 99 or
   200 to 254 without adding it to this chapter first.
2. A lab that needs its own segment takes the next free number from 100 to 199
   and records the VLAN, the IPv4 /24, and the IPv6 /120 in its own chapter.
3. Hostnames are lowercase, end in the instance number (`-1`, `-201a`), and
   match the DNS-style names in the host table. Set them with
   `config system global` and `set hostname` on a switch.
4. Never use the first or last address of a /24 for a host (`.0` and `.255`).

### Lab design for each requirement

Every lab chapter that follows this one has the same shape, so a lab can be run
from a clean state and compared with the baseline:

1. State the requirement (SRG ID and text) and the workbook row.
2. Name the segments, hosts, and prerequisites from this chapter it uses.
3. Start from the baseline snapshot (Lab 999.6).
4. Configure the FortiSwitch setting.
5. Run a positive test that shows the requirement met.
6. Run a negative test that shows the control blocks what it should.
7. Collect evidence (command output, a log line, a capture) as described under
   *Evidence*.
8. Return to the baseline.

### Evidence

Store each run in `evidence/<lab>/<date>/` on `admin-201`: the switch
configuration before and after (`show full-configuration`), the command output
that proves the result, the relevant log lines from `syslog-201a`, and a short
note of the model and FortiSwitchOS version (`get system status`). A finished
lab sign-off points at that folder.

## Validation and Troubleshooting

Check the shared infrastructure in this order. If a step fails, fix it before
you run a requirement lab.

| Step | Check | Expected |
| --- | --- | --- |
| 1 | From `admin-201`, `ping 10.201.30.11` and `ping -6 fd00:db8:201::1e0b` | Replies from `sw-648f-1` |
| 2 | From `sw-648f-1`, `execute ping 10.201.10.10` | Replies from `radius-201a` |
| 3 | `get system status` on each switch | The model you expect and a 7.6.x FortiSwitchOS release |
| 4 | `execute license status` on each switch | The Advanced Features License is valid |
| 5 | `get system ntp` | Synchronized to `10.201.10.30` or `10.201.10.31` |
| 6 | Log in with a RADIUS account | The login appears in the FreeRADIUS log and in `syslog-201a` |
| 7 | `execute backup config sftp <FILE> 10.201.10.60 <USER>` | The file appears on `files-201` |

| Symptom | Cause | Fix |
| --- | --- | --- |
| A switch cannot reach any service | The trunk does not carry VLAN 30, or the native VLAN is wrong | Check `allowed-vlans` and `native-vlan` on the trunk port, and the VLAN subinterfaces on `gw-201` |
| RADIUS login fails but the server is reachable | The shared secret differs, or the switch is not a client | Match the secret and add the switch's source address to `clients.conf` |
| Syslog arrives on UDP but not over TLS | The CA certificate is not trusted, or the port differs | Use port 6514 on both ends and install the lab CA on the switch |
| NTP never synchronizes | The key ID or key differs between the switch and `chrony` | Match `key-id` and `key`, and check `chronyc sources` |
| IPv6 pings fail while IPv4 works | A /112 host tried SLAAC, or the host has no static IPv6 address | Set the address statically; SLAAC cannot work on a /112 |
| A routed link is up but a route is missing | The peer does not know the lab prefix | Add the prefix on the peer, then check the routing table |

## Security and Best Practices

- **Treat the lab as hostile to itself.** `attacker-201` exists to break rules.
  Keep the lab off every production network, and keep `gw-201`'s default
  policy at deny.
- **Allow only what each segment needs.** The gateway policy below permits the
  switch management and test VLANs to reach the service ports they use and
  nothing else.
- **No shared secrets between labs.** Generate new RADIUS, NTP, SNMPv3, and
  routing keys for each lab, and delete them in the cleanup step.
- **Use the strongest settings that the requirement names.** The baseline uses
  SNMPv3 with SHA-2 authentication and AES privacy, TLS for syslog, and SSH for
  management. Do not enable Telnet, HTTP, or SNMPv1/v2c to make a test easier.
- **Back up before every change.** A saved configuration is what makes a lab
  repeatable (Lab 999.6).
- **Record what each lab did not prove.** A lab on a lab CA, or on a model that
  does not support the feature, says so in its sign-off.

## References and Knowledge Checks

**References:**

- [Chapter 01](01-fortiswitch-feature-version-and-srg-map.md) for the features,
  commands, and prerequisites P1 to P17 this chapter satisfies, and
  [Chapters 02](02-fortiswitch-and-cisco-catalyst-switch-stig-crosswalk.md) and
  [03](03-cisco-nx-os-switch-and-fortiswitch-stig-crosswalk.md) for the rules
  the labs prove.
- [Chapter 90](90-as-built-how-this-volume-was-built.md) for the workbook.
- FortiSwitchOS 7.6.7 CLI Reference and Administration Guide (Fortinet
  Document Library). The switch commands in this chapter were checked against
  the CLI Reference text.
- RFC 3021 (31-bit prefixes), RFC 4193 (unique local addresses), RFC 6164
  (127-bit IPv6 prefixes), and RFC 6996 (private autonomous system numbers).
- [Volume CM, Tim's Lab Gear](../../volume-900-tims-lab-gear/README.md) for the
  hypervisor host, and
  [Volume CLXXIV](../../volume-174-nse-5-fortiswitch-lab/README.md) for a
  FortiLink-based FortiSwitch lab that uses a different address plan.

**Knowledge checks:**

1. What does the third octet of a lab IPv4 address tell you, and how does it
   map to the IPv6 address?
2. Why can the IPv6 block not use SLAAC, and how do hosts get addresses?
3. Which host satisfies P4, and why are there two of them?
4. Why are the routed peers separate from `gw-201`?
5. What can `ca-201` prove, and what can it not?
6. Where does a new lab take its segment from?
7. What is in the evidence folder after a lab run?

## Hands-On Lab

**Shared prerequisites.** One FS-648F-FPOE and one FS-2048F on FortiSwitchOS
7.6.x, with a console cable or serial adapter for each. A hypervisor with
enough capacity for about nine small virtual machines (a router, two service
hosts, a CA, a DHCP server, an admin workstation, two routing peers, and test
hosts) and a physical network interface that can carry an 802.1Q trunk to each
switch. Ubuntu Server LTS images for the Linux machines (Volume XXI covers the
installation). An Advanced Features License key for each switch. Cost: the two
switches and the licenses; the virtual machines run on hardware you already
have.

Placeholders used below: `<SECRET>` is a value you generate for this lab.
`<PORT_TRUNK>`, `<PORT_MGMT>`, `<PORT_EP1>` and so on are physical switch port
names; read them with `get switch interface status` and write them in your
lab notes before you start.

**Automated build.** [Chapters 09 to 14](09-esxi-7-8-and-9-lab-virtual-machine-automation.md)
script the creation of the virtual machines below (not their service
configuration) on ESXi, vCenter, Dell VxRail, Workstation Pro, Proxmox VE, KVM, and WSL. They give
each machine its name, addresses, and packages, and `gw-201` its VLAN interfaces
and the baseline policy of this lab, so you can skip the netplan and `nftables`
steps of Lab 999.1 for the gateway if you use them.

### Lab 999.1 — Build the gateway and the VLANs

Goal: a gateway that holds `.1` on every shared segment, routes between them,
and allows only the traffic the baseline needs.

1. Create the virtual machine `gw-201` with a NIC on the lab trunk and a second
   NIC on your internet-facing network. This procedure uses a Linux router. A
   FortiGate-VM works equally well (and doubles as `fgt-201` for managed-mode
   labs).
2. Give the trunk NIC VLAN subinterfaces and addresses. With netplan, save this
   as `/etc/netplan/60-lab201.yaml` (replace `eth1` with the trunk NIC):

   ```yaml
   network:
     version: 2
     ethernets:
       eth1: {}
     vlans:
       vlan10: { id: 10, link: eth1, addresses: ["10.201.10.1/24", "fd00:db8:201::a01/120"] }
       vlan20: { id: 20, link: eth1, addresses: ["10.201.20.1/24", "fd00:db8:201::1401/120"] }
       vlan30: { id: 30, link: eth1, addresses: ["10.201.30.1/24", "fd00:db8:201::1e01/120"] }
       vlan40: { id: 40, link: eth1, addresses: ["10.201.40.1/24", "fd00:db8:201::2801/120"] }
       vlan41: { id: 41, link: eth1, addresses: ["10.201.41.1/24", "fd00:db8:201::2901/120"] }
       vlan42: { id: 42, link: eth1, addresses: ["10.201.42.1/24", "fd00:db8:201::2a01/120"] }
       vlan50: { id: 50, link: eth1, addresses: ["10.201.50.1/24", "fd00:db8:201::3201/120"] }
   ```

   Run `sudo netplan apply`. Segment 0 (out-of-band) is a separate NIC
   attached to the switches' management ports; give it `10.201.0.1/24` and
   `fd00:db8:201::1/120` the same way.
3. Turn on forwarding for both address families:

   ```bash
   printf 'net.ipv4.ip_forward=1\nnet.ipv6.conf.all.forwarding=1\n' | sudo tee /etc/sysctl.d/60-lab201.conf
   sudo sysctl --system
   ```

4. Install the baseline policy. It drops forwarded traffic by default, lets the
   switch management segments reach the service ports, lets the services reply
   and manage the switches, and lets the admin segment reach everything for
   administration. Endpoints on the user segments reach nothing beyond their own
   segment, except ping:

   ```bash
   sudo nft -f - <<'EOF'
   table inet lab201 {
     set svc4 { type ipv4_addr; flags interval; elements = { 10.201.10.0/24 } }
     set mgmt4 { type ipv4_addr; flags interval; elements = { 10.201.0.0/24, 10.201.30.0/24 } }
     set svc6 { type ipv6_addr; flags interval; elements = { fd00:db8:201::a00/120 } }
     set mgmt6 { type ipv6_addr; flags interval; elements = { fd00:db8:201::/120, fd00:db8:201::1e00/120 } }
     chain forward {
       type filter hook forward priority 0; policy drop;
       ct state established,related accept
       ip saddr 10.201.20.0/24 accept
       ip6 saddr fd00:db8:201::1400/120 accept
       ip saddr @mgmt4 ip daddr @svc4 tcp dport { 22, 514, 6514 } accept
       ip saddr @mgmt4 ip daddr @svc4 udp dport { 69, 123, 161, 162, 514, 1812, 1813, 2055, 4739, 6343 } accept
       ip6 saddr @mgmt6 ip6 daddr @svc6 tcp dport { 22, 514, 6514 } accept
       ip6 saddr @mgmt6 ip6 daddr @svc6 udp dport { 69, 123, 161, 162, 514, 1812, 1813, 2055, 4739, 6343 } accept
       ip saddr @svc4 ip daddr @mgmt4 accept
       ip6 saddr @svc6 ip6 daddr @mgmt6 accept
       icmp type echo-request accept
       icmpv6 type { echo-request, nd-neighbor-solicit, nd-neighbor-advert } accept
     }
   }
   EOF
   sudo nft list ruleset | sudo tee /etc/nftables.conf
   sudo systemctl enable --now nftables
   ```

   The ports are 22 (SFTP), 69 (TFTP), 123 (NTP), 161 and 162 (SNMP), 514 and
   6514 (syslog), 1812 and 1813 (RADIUS), 2055 and 4739 (NetFlow and IPFIX),
   and 6343 (sFlow). Adjust them if you change a service's port. The switches
   reach the services through `gw-201`, so a failed test points at this policy
   first.
5. Add masquerading on the internet NIC only if you want package installs from
   the lab, and remove it when the build is done.

**Expected result.** From `admin-201`, every `.1` on segments 10 to 50 answers a
ping over IPv4 and IPv6.

### Lab 999.2 — Build the service hosts

Goal: the servers behind P1 to P6, P12, and P15 to P17, each reachable at the
address in the host table.

1. Create `svc-201a` and `svc-201b` (Ubuntu Server LTS) on VLAN 10. Add the
   service addresses to each as secondary addresses, for example on `svc-201a`:

   ```yaml
   network:
     version: 2
     ethernets:
       ens18:
         addresses:
           - 10.201.10.10/24
           - 10.201.10.12/24
           - 10.201.10.20/24
           - 10.201.10.30/24
           - 10.201.10.40/24
           - fd00:db8:201::a0a/120
           - fd00:db8:201::a0c/120
           - fd00:db8:201::a14/120
           - fd00:db8:201::a1e/120
           - fd00:db8:201::a28/120
         routes:
           - { to: default, via: 10.201.10.1 }
   ```

   `svc-201b` carries `.11`, `.21`, `.31`, `.50`, and `.60` the same way.
2. **Time (P5).** On both hosts install chrony and make each an authenticated
   server for the lab. In `/etc/chrony/chrony.conf` keep the upstream `pool`
   or `server` lines, then add:

   ```text
   allow 10.201.0.0/16
   allow fd00:db8:201::/112
   keyfile /etc/chrony/chrony.keys
   ```

   and in `/etc/chrony/chrony.keys` add one key line, `1 SHA1 <SECRET>`, then
   restart `chrony`.
3. **Syslog with TLS (P4).** Install `rsyslog` and `rsyslog-gnutls`. Issue a
   server certificate from `ca-201` (step 6) and add `/etc/rsyslog.d/10-lab201.conf`:

   ```text
   module(load="imtcp"
          StreamDriver.Name="gtls"
          StreamDriver.Mode="1"
          StreamDriver.Authmode="anon")
   global(DefaultNetstreamDriverCAFile="/etc/ssl/lab201/ca.pem"
          DefaultNetstreamDriverCertFile="/etc/ssl/lab201/server.pem"
          DefaultNetstreamDriverKeyFile="/etc/ssl/lab201/server.key")
   input(type="imtcp" port="6514")
   template(name="PerHost" type="string" string="/var/log/lab201/%HOSTNAME%.log")
   *.* ?PerHost
   ```

   Create `/var/log/lab201`, then restart `rsyslog`.
4. **RADIUS (P1, P2).** Install `freeradius`. In
   `/etc/freeradius/3.0/clients.conf` add a client for each switch network, with
   a different `<SECRET>` per lab:

   ```text
   client switches-oob  { ipaddr = 10.201.0.0/24;  secret = <SECRET> }
   client switches-mgmt { ipaddr = 10.201.30.0/24; secret = <SECRET> }
   ```

   Add a test user to `/etc/freeradius/3.0/users`, restart `freeradius`, and
   test it locally with `radtest <USER> <PASSWORD> 127.0.0.1 0 testing123`
   (use the local `localhost` client's secret). Run the same configuration on
   `svc-201b` with its own secret.
5. **Collectors and file server (P15, P16, P17), on `svc-201b`.** Install
   `openssh-server` and `tftpd-hpa` (set `TFTP_DIRECTORY` and
   `TFTP_ADDRESS` in `/etc/default/tftpd-hpa`), create a backup user with an
   SFTP-only chroot, and install `nfdump` for NetFlow and IPFIX (`nfcapd -p 2055`)
   and `sflowtool` for sFlow (`sflowtool -p 6343`).
6. **Certificates (P3), on `ca-201`.** Install a small CA with SCEP support (for
   example `step-ca`). Create the CA, issue the two service certificates, and
   export the CA certificate to `/etc/ssl/lab201/ca.pem` on every host that
   needs it. This CA is for the lab only.
7. **DHCP (P12), on `dhcp-201`.** Give the machine NICs on VLANs 10, 40, 41, and
   50, with `.80` on VLAN 10 and `.2` on the others. Install `kea-dhcp4-server`
   and define one subnet per user VLAN, each with a pool of `.100` to `.199`,
   router `.1`, and DNS `10.201.10.1`.
8. **SNMPv3 manager (P6), on `svc-201a`.** Install `snmp` (for `snmpwalk`) and
   `snmptrapd`. The user you create on the switch in Lab 999.4 is the one you
   query with.

**Expected result.** Each service answers locally, and `ss -lntu` shows the
listeners on the right addresses.

### Lab 999.3 — Baseline the switches

Goal: both switches have a hostname, the Advanced Features License, the
shared VLANs, a trunk, and a management SVI that `gw-201` can reach. Run this
on each switch, with the values for `sw-648f-1` shown (`sw-2048f-1` uses
`.12`).

1. Connect to the console, then set the hostname and read the model:

   ```text
   config system global
       set hostname sw-648f-1
   end
   get system status
   ```

2. Add the license and check it:

   ```text
   execute license add <LICENSE_KEY>
   execute license status
   ```

3. Create the VLANs from the plan (P13). Repeat the block for 10, 20, 30, 40,
   41, 42, 50, 60, and 99:

   ```text
   config switch vlan
       edit 30
           set description SWITCH-MGMT
       next
       edit 99
           set description NATIVE-DEAD
       next
   end
   ```

4. Make the trunk to `gw-201`:

   ```text
   config switch interface
       edit <PORT_TRUNK>
           set native-vlan 99
           set allowed-vlans 10,20,30,40,41,42,50
       next
   end
   ```

5. Give the switch an in-band management address (P10) and a route to the
   gateway, and limit management to SSH and ping:

   ```text
   config system interface
       edit mgmt-svi
           set interface internal
           set vlanid 30
           set ip 10.201.30.11 255.255.255.0
           set allowaccess ping ssh
           config ipv6
               set ip6-address fd00:db8:201::1e0b/120
           end
       next
   end
   config router static
       edit 1
           set dst 0.0.0.0 0.0.0.0
           set gateway 10.201.30.1
       next
   end
   config router static6
       edit 1
           set dst ::/0
           set gateway fd00:db8:201::1e01
       next
   end
   ```

6. Address the out-of-band management port the same way
   (`10.201.0.11/24`, `fd00:db8:201::b/120`), reading its name from
   `get system interface physical`.
7. Park the unused ports (`<PORT_UNUSED>`) in VLAN 60 and set them down. Keep
   the list in your lab notes.

**Expected result.** `execute ping 10.201.30.1` and `execute ping6
fd00:db8:201::1e01` succeed from the switch, and `admin-201` reaches
`10.201.30.11` over SSH.

### Lab 999.4 — Connect the switch to the services

Goal: authentication, logging, time, SNMPv3, flow export, and backup, each
proven.

1. RADIUS and a group (P1, P2). Use the lab values from Lab 999.2:

   ```text
   config user radius
       edit radius-201a
           set server 10.201.10.10
           set secret <SECRET>
       next
       edit radius-201b
           set server 10.201.10.11
           set secret <SECRET>
       next
   end
   config user group
       edit lab-radius
           set member radius-201a radius-201b
       next
   end
   ```

2. Syslog to both log servers (P4):

   ```text
   config log syslogd setting
       set status enable
       set server 10.201.10.20
       set mode reliable
       set port 6514
       set enc-algorithm high
   end
   config log syslogd2 setting
       set status enable
       set server 10.201.10.21
       set mode reliable
       set port 6514
       set enc-algorithm high
   end
   ```

3. Authenticated NTP (P5):

   ```text
   config system ntp
       set ntpsync enable
       set authentication enable
       config ntpserver
           edit 1
               set server 10.201.10.30
               set authentication enable
               set key-id 1
               set key <SECRET>
           next
           edit 2
               set server 10.201.10.31
               set authentication enable
               set key-id 1
               set key <SECRET>
           next
       end
   end
   ```

4. An SNMPv3 user (P6):

   ```text
   config system snmp user
       edit lab-snmp
           set security-level auth-priv
           set auth-proto sha256
           set auth-pwd <SECRET>
           set priv-proto aes256
           set priv-pwd <SECRET>
           set queries enable
           set notify-hosts 10.201.10.40
       next
   end
   ```

5. Flow export (P17):

   ```text
   config system sflow
       config collectors
           edit 1
               set ip 10.201.10.50
           next
       end
   end
   config system flow-export
       set format ipfix
       config collectors
           edit 1
               set ip 10.201.10.50
               set port 4739
               set transport udp
           next
       end
   end
   ```

6. Point a lab administrator at the group (P2). Keep the local `admin` account
   for recovery:

   ```text
   config system admin
       edit <LAB_ADMIN>
           set accprofile super_admin
           set remote-auth enable
           set remote-group lab-radius
       next
   end
   ```

7. Prove each one:
   - Log in over SSH as `<LAB_ADMIN>` with the RADIUS password; confirm the
     access request in the FreeRADIUS log.
   - `get system ntp` and `chronyc clients` on `svc-201a`.
   - From `svc-201a`: `snmpwalk -v3 -l authPriv -u lab-snmp -a SHA-256 -A <SECRET> -x AES-256 -X <SECRET> 10.201.30.11 1.3.6.1.2.1.1`.
   - Confirm a configuration-change log line in
     `/var/log/lab201/sw-648f-1.log` on both log servers.
   - `execute backup config sftp baseline-648f.conf 10.201.10.60 <USER>
     <PASSWORD>`, and confirm the file on `files-201`.

**Expected result.** All the checks pass on `sw-648f-1` and again on
`sw-2048f-1`. If the AES-256 SNMP query fails, check which privacy protocol
the manager supports and note it for the SNMP requirement lab.

### Lab 999.5 — Build the routed links and the peers

Goal: L1 to L5 up, with each peer reachable by its loopback.

1. Create VLANs 2001 to 2005 and add them to the correct ports (`<PORT_L1>` and
   so on), tagged on both ends of each link.
2. Address each link on the switch end with a Layer 3 interface, for example L1
   on `sw-648f-1`:

   ```text
   config system interface
       edit l1
           set interface internal
           set vlanid 2001
           set ip 10.201.200.0 255.255.255.254
           config ipv6
               set ip6-address fd00:db8:201::c800/127
           end
       next
   end
   ```

   and give `sw-2048f-1` the other end of L5 (`10.201.200.9/31`,
   `fd00:db8:201::c809/127`).
3. Build `rtr-peer-1` and `rtr-peer-2` as small FRR virtual machines (or
   FortiGate-VMs). Give each its link addresses, its loopback
   (`10.201.250.21/32` and `fd00:db8:201::fa15/128` for peer 1;
   `10.201.250.22/32` and `fd00:db8:201::fa16/128` for peer 2), and the stub
   prefixes `10.201.210.0/24` (peer 1) and `10.201.211.0/24` (peer 2).
4. Verify reachability only: `execute ping 10.201.200.1` from `sw-648f-1`, and
   the same for every link. Do not enable a routing protocol in this lab. Each
   routing lab turns on the protocol it tests and the keys it uses.

**Expected result.** Every link end answers a ping over IPv4 and IPv6.

### Lab 999.6 — Take the baseline and reset to it

Goal: a saved state that every lab starts from.

1. On each switch, save the configuration on the flash and off the switch:

   ```text
   execute backup config flash baseline-201
   execute backup config sftp baseline-648f.conf 10.201.10.60 <USER> <PASSWORD>
   ```

2. Snapshot every virtual machine and name the snapshot `baseline-201`.
3. To reset between labs, restore the virtual machine snapshots and reload the
   baseline configuration from `files-201`. Use the commands in the FortiSwitchOS
   CLI Reference (`execute restore config`) and confirm the result with
   `show full-configuration`.
4. Create `evidence/` on `admin-201` and add a text file named `lab-notes.md`
   with the model, serial number, FortiSwitchOS version, ports, and the
   `<SECRET>` handling you used (where they are stored, not their values).

**Expected result.** After a reset, Labs 999.1 to 999.5 checks pass without any
edit.

### Cleanup

Delete the lab's `<SECRET>` values from every host when you finish a run of
labs, remove masquerading from `gw-201`, and, if you leave the lab idle,
shut the virtual machines down. The switches keep the baseline configuration.

## Lab Verification

Complete this sign-off once Labs 999.1 to 999.6 have been run end to end,
including the validation table. Until then, the labs are unverified, and the
commands in this chapter have been checked against the CLI Reference text but
not run.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter defines the lab every requirement lab in this volume runs in. The
address plan splits `10.201.0.0/16` into segments whose third octet is the VLAN
ID and splits `fd00:db8:201::/112` into /120 segments with the same numbers.
Two switches, a gateway, two service hosts, a CA, a DHCP server, an admin
workstation, and two routing peers satisfy prerequisites P1 to P17, and a
baseline snapshot lets each lab start from a known state.

- [ ] Can read an address and name its segment and VLAN.
- [ ] Can say why the IPv6 block uses static addresses and not SLAAC.
- [ ] Can map each prerequisite P1 to P17 to a host.
- [ ] Has built the gateway, the service hosts, and both switch baselines.
- [ ] Has proven RADIUS, syslog, NTP, SNMPv3, flow export, and backup from each
      switch.
- [ ] Can reset the lab to the baseline and keep evidence for each run.
