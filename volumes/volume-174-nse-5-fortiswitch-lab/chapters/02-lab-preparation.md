# Chapter 02: Lab Preparation

## Learning Objectives

- Prepare the controller for your option: reset, upgrade, register, and cable a
  used FortiGate 40F or 60F (C1); measure and free the evaluation budget on
  FGT-1 and release `port3` (C2); or add `port4` to a licensed FortiGate-VM
  (C3).
- Enable the switch controller and build the FortiLink interface
  (`10.255.1.1/24`, alias `fortilink`) on any controller, with or without a
  switch attached.
- Build a Layer 2 path from a FortiGate-VM to a physical switch that passes
  LLDP and Spanning Tree BPDUs: a dedicated NIC on a plain Proxmox bridge
  (`vmbrFL`), or PCI passthrough.
- Bring a FortiSwitch (S1, S2, or S3) to factory defaults on FortiSwitchOS
  7.6.x over the console and TFTP, and check its model against the capability
  matrix.
- Run the FortiLink go/no-go test and know what to do when it fails.
- Build the shared services: the `radius-174` FreeRADIUS VM, the syslog
  listener on `ubuntu-ws`, the endpoints, and the services policy.

## Theory and Architecture

### What this chapter establishes

Every later chapter assumes four things exist: a controller running FortiOS
7.6 with a FortiLink interface, a Layer 2 path from that interface to the
switch, a switch on FortiSwitchOS 7.6.x in its factory-default state, and the
services the switch will talk to (RADIUS, syslog, TFTP). Labs 2.1 to 2.5 build
them in that order. Track 2 builds the controller and the services and reads the
rest.

| Lab | Builds | Track 1 | Track 2 |
| --- | --- | --- | --- |
| 2.1 | Controller baseline: version, license, budget, FortiLink port reserved | Hands-on | Hands-on |
| 2.2 | Switch controller and FortiLink interface | Hands-on | Hands-on (unlinked port), plus the pre-provisioning test |
| 2.3 | Physical FortiLink path | Hands-on | Read-and-predict |
| 2.4 | Switch reset, firmware, capability check, go/no-go test | Hands-on | Read-and-predict |
| 2.5 | RADIUS, syslog listener, endpoints, services policy | Hands-on | Hands-on |

### What crosses the FortiLink link

The FortiLink link is an ordinary Ethernet link, but it carries more than one
kind of traffic, and a virtual path must pass all of it:

- **Management and data VLANs together.** The switch's management traffic,
  including the DHCP exchange that gives it its address from the FortiLink
  interface, uses the FortiLink management VLAN (4094 by default;
  `switch-controller-mgmt-vlan`, FortiLink Guide 7.6.7, p. 34). The lab VLANs
  (1741–1745) and the auto-created VLANs (4089–4093) ride the same link tagged.
  A Proxmox vNIC with a VLAN tag, or a VLAN-aware bridge, would deliver only
  one VLAN.
- **LLDP.** FortiOS detects FortiSwitch neighbors with LLDP or with the
  FortiLink protocol (`fortilink-neighbor-detect {fortilink | lldp}`). The
  FortiOS 7.6.0 CLI Reference lists `fortilink` as the default; the FortiLink
  Guide 7.6.7 (p. 24) says that from FortiOS 7.6.1 LLDP is the default. LLDP
  frames go to the link-local group address `01:80:C2:00:00:0E`.
- **Spanning Tree BPDUs** to `01:80:C2:00:00:00`. The switch runs MSTP, and
  Chapter 05 needs those BPDUs to reach the controller.
- **The management session** between the switch and the controller (CAPWAP by
  default, or HTTPS; FortiLink Guide 7.6.7, p. 50), carried over IP on the
  FortiLink subnet.

### Why a Linux bridge needs `group_fwd_mask`

A Linux bridge does not forward frames sent to the link-local range
`01:80:C2:00:00:0X` unless the bridge's `group_fwd_mask` allows it. The
`ip-link(8)` manual describes the mask as a bitmask over those addresses,
default 0 (forward none). Bit *X* corresponds to address `0X`, so LLDP
(`0E`, decimal 14) needs bit 14: 2^14 = **16384**. With STP turned off, the
bridge runs no Spanning Tree of its own and is expected to pass the switch's
BPDUs; the manual pages consulted do not say so explicitly, so Lab 2.3 checks it
with `tcpdump` instead of assuming it. PCI
passthrough avoids the question: the FortiGate-VM owns the NIC and sees every
frame.

### FortiSwitchOS factory defaults

From FortiSwitchOS 7.2.0, a new or reset switch looks for a manager on its own
(zero-touch management, FortiLink Guide 7.6.7, pp. 14–15). Its factory defaults
include VLAN 1 as the native VLAN on every port and on the internal interface,
DHCP on the `mgmt` and `internal` interfaces, auto topology (auto-network)
enabled, FortiLink auto-discovery and CAPWAP discovery enabled, and FortiLAN
Cloud enabled. The guide says that all ports are enabled for auto-discovery,
and also gives a table of default auto-FortiLink ports per model (pp. 30–31);
this chapter uses a port from that table for `<FSW_FL_PORT>`. The FortiLink
Guide (p. 41) states the precondition plainly: a switch that is not in its
factory-default configuration must be reset with `execute factoryreset` before
it is connected.

### The evaluation-license question

FortiLink on the FortiGate-VM evaluation license is **unconfirmed**: no Fortinet
document or community post found while planning this volume says that it works
or that it does not. The evaluation allows low encryption only, and the
FortiLink management session uses DTLS (CAPWAP) or HTTPS. Chapter 01 therefore
made C2 conditional. Lab 2.4 ends with a go/no-go test that settles it on your
FGT-1, and C1 and C3 are the fallbacks. Track 2 does not depend on the answer,
because it never manages a switch.

## Design Considerations

### What each controller option needs

| Step | C1 hardware 40F/60F | C2 FGT-1 evaluation | C3 licensed FortiGate-VM |
| --- | --- | --- | --- |
| Factory reset | Yes (used unit) | No | No |
| Firmware | Upgrade to FortiOS 7.6 along the supported path | Stay on 7.6.x (FGT-1 runs 7.6.2) | Stay on 7.6.x |
| Registration | Register the serial in FortiCare to download firmware | Already licensed (evaluation) | Already licensed |
| FortiLink port | `<FL_PORT>`: a free port, or the factory `fortilink` interface | `port3`, taken from VLAN 202 | New `port4` |
| Physical path | Patch cable to the switch | Dedicated NIC with `vmbrFL`, or PCI passthrough | Same as C2 |
| Policy and route budget | No cap | 3 policies, 3 routes, 3 interfaces | No cap |
| Go/no-go test | Recommended smoke test | **Required** | Recommended smoke test |

FortiLink needs a FortiGate in NAT mode, not transparent mode (FortiLink Guide
7.6.7, p. 12). The FortiOS 7.6.0 CLI Reference lists
`config switch-controller managed-switch` as available on the FortiGate 40F,
FortiGate 60F, and FortiGate-VM64, and `config system virtual-switch` on the 40F
and 60F but not on the VM.

### Bridge or passthrough (C2 and C3)

| | `vmbrFL` plain bridge | PCI passthrough |
| --- | --- | --- |
| What the VM sees | A virtual NIC (the model already used by FGT-1) | The physical NIC and its driver |
| Link-local frames | Need `group_fwd_mask 16384` for LLDP; STP off | All frames reach the VM |
| Host visibility | `tcpdump` on the NIC and the tap device works | The host cannot use or see the NIC |
| Requirements | Any NIC Linux supports | VT-d, IOMMU, the NIC in its own IOMMU group, and a NIC driver in FortiOS |
| Interface order | Unchanged (`port3` stays `port3`) | Check which `portN` the passed-through NIC becomes |
| Recommendation | **Default** | Use when the bridge cannot be made to pass LLDP or you prefer a clean path |

Do not carry FortiLink through the Nexus. The Nexus runs its own Spanning Tree
and LLDP and would consume those frames, and FortiLink is meant to be a direct
link (Chapter 01, Topology C2 and C3).

The dedicated NIC must match the switch port you cable it to in media and
speed. A 1 GbE RJ-45 NIC on a copper `<FSW_FL_PORT>` is the simplest match;
check the switch model's datasheet before choosing an SFP or SFP+ port.

### Choosing the switch FortiLink port

| Switch option | Default auto-FortiLink ports (FortiLink Guide 7.6.7, pp. 30–31) | Suggested `<FSW_FL_PORT>` |
| --- | --- | --- |
| S1 FS-108F, -POE, -FPOE | `port7`–`port10` | `port7` (or the port that matches your NIC's media) |
| S2 FS-124F, -POE, -FPOE | `port21`–`port28` | `port21` (or the port that matches your NIC's media) |
| S3 FS-224E, -POE | `port21`–`port28` | `port21` on `FSW-A` |
| S3 FS-248E-POE, -FPOE | `port45`–`port52` | `port45` on `FSW-A` |
| Any other model | See the guide's table | A port from the table; the guide adds that any port can be used for FortiLink if it is configured manually |

These choices avoid the ports Chapter 01 reserves: `port1` and `port2`
(endpoints), `port5` and `port6` (loop cable). This chapter also uses `port3`
briefly, for temporary in-band management while upgrading firmware, on a
model without a dedicated management port.

### Firmware, registration, and used hardware

- **Downloads need a support account.** FortiOS and FortiSwitchOS images come
  from the Fortinet support portal (`support.fortinet.com`). Whether your
  account can download a given image depends on Fortinet's entitlement rules
  for the registered product, which this volume cannot state for every case.
  Register the unit's serial number to your account first; if the unit is
  still registered to a previous owner, it must be transferred, which Fortinet
  support handles. Ask the seller about registration before you buy.
- **The evaluation cannot fetch switch firmware.** FGT-1 has no FortiGuard
  entitlement, so firmware goes through the TFTP VM (VM 140, `10.30.99.50`,
  the Alpine `in.tftpd` server from
  [Volume CLXXI, Chapter 05](../../volume-171-alpine-linux/chapters/05-building-a-linux-tftp-server-on-alpine.md),
  root `/tftpboot`).
- **Follow the supported upgrade path.** FortiOS enforces intermediate steps on
  multi-version jumps; check Fortinet's Upgrade Path tool before upgrading a C1
  unit ([Volume XIX, Lab 4.8](../../volume-019-fortinet-network-security/chapters/04-fortigate-first-deployment-licensing-management-and-hardening.md#lab-48--upgrading-firmware-over-tftp-from-the-cli-topic-firmware-lifecycle)
  shows the TFTP procedure). For FortiSwitchOS, read the 7.6.x release notes
  for the supported upgrade path from your starting version.
- **Check compatibility.** The FortiLink Guide (p. 12) points to the FortiLink
  Compatibility table for which FortiSwitchOS versions each FortiOS version
  supports. Check your exact pair (for example FortiOS 7.6.2 on FGT-1 with
  FortiSwitchOS 7.6.7) before the go/no-go test.

### The C2 budget

The evaluation counts every physical interface, firewall policy, and static
route. FGT-1 already has three physical interfaces, so FortiLink can only take
over `port3`. Whether VLAN subinterfaces of the FortiLink port count is not
documented; a Fortinet staff answer on the Community says they do, so Lab 4.1
tests it before the lab VLANs are built. The policy
plan from Chapter 01 becomes concrete here:

| Slot | Contents | Built in |
| --- | --- | --- |
| P1 | FGT-1's existing VLAN 200 internet policy (`port2` to `port1`), if it has one. Chapter 04 adds `FSW-LAN` to its sources | Existing; reviewed in Lab 2.1 |
| P2 | `fortilink` to `port2` (RADIUS, syslog, SNMP traps, sFlow). Chapter 04 adds `FSW-LAN` to its sources | Lab 2.5 |
| P3 | One chapter-specific policy at a time | Later chapters |

If FGT-1 has more than one existing policy after the VLAN 202 policies are
removed, decide in Lab 2.1 which to delete for the duration of the volume; the
Lab 2.1 backup restores them in Lab 12.6.

## Implementation and Automation

The labs below are the implementation. Two habits make them repeatable.

**Back up before every change of state.** Each controller and switch step that
changes firmware or releases an interface starts with a configuration backup to
the TFTP VM. Lab 12.6 restores from these files.

**Capture the path state in one place.** On C2 and C3, this read-only check
prints the bridge settings Lab 2.3 depends on and samples LLDP on both sides of
the bridge. Save it on proxmox-1 as `/root/fl-path-check.sh` (replace
`<NEW_NIC>` and the tap name; Proxmox names a VM's tap devices
`tap<VMID>i<N>`, so FGT-1's `net2` is `tap120i2` and `net3` is `tap120i3`).
It needs `tcpdump` on the host (`apt install tcpdump` if it is missing):

```bash
#!/bin/sh
# Read-only check of the FortiLink bridge on proxmox-1 (C2/C3, Option A).
BR=vmbrFL
NIC=<NEW_NIC>
TAP=tap120i2          # C2 port3 = net2; C3 port4 = net3 -> tap120i3
for f in group_fwd_mask stp_state vlan_filtering; do
  printf '%s = %s\n' "$f" "$(cat /sys/class/net/$BR/bridge/$f)"
done
bridge link show | grep "master $BR"
echo "LLDP seen on $NIC (from the switch or forwarded from the VM):"
timeout 35 tcpdump -i "$NIC" -e -n -c 2 ether dst 01:80:c2:00:00:0e
echo "LLDP seen on $TAP (from the VM or forwarded from the switch):"
timeout 35 tcpdump -i "$TAP" -e -n -c 2 ether dst 01:80:c2:00:00:0e
```

Expect `group_fwd_mask = 16384`, `stp_state = 0`, and `vlan_filtering = 0`.
The 35-second capture window allows for an LLDP transmit interval of up to 30
seconds; if your devices use a longer interval, raise it.

## Validation and Troubleshooting

| Symptom | Likely cause | Check |
| --- | --- | --- |
| The switch never appears in `execute switch-controller get-conn-status` | No Layer 2 path; LLDP filtered by the bridge; the switch is not at factory defaults; wrong neighbor-detect method | Link lights; `fl-path-check.sh`; `execute factoryreset` on the switch; try `set fortilink-neighbor-detect fortilink` |
| LLDP seen on the tap but not on the NIC (or the reverse) | `group_fwd_mask` is 0 | `cat /sys/class/net/vmbrFL/bridge/group_fwd_mask`; re-apply with `ifreload -a` |
| Only one VLAN reaches FGT-1 | The vNIC still has `tag=`, or `vmbrFL` is VLAN-aware | `qm config 120 \| grep ^net`; `vlan_filtering` must be 0 |
| The switch is Discovered but never Authorized/Up after authorization | Management session fails: no `fabric` access on the FortiLink interface, firmware incompatibility, or (C2) the evaluation license | `show system interface <FL_PORT>`; compatibility table; switch-side `execute switch-controller get-conn-status`; go/no-go fallbacks |
| The switch has no `10.255.1.x` address | No DHCP server on the FortiLink interface | `show system dhcp server`; `execute dhcp lease-list <FL_PORT>` |
| TFTP image transfer fails | Wrong file name or path, no route, or the server is down | `execute ping 10.30.99.50`; file in `/tftpboot` on VM 140 |
| `get system status` on the switch reports the firmware signature as invalid | Unsigned or interim image | Use a GA image from the support portal; `execute verify image primary` |
| `diagnose test authserver` fails | Wrong secret, the FortiGate's source address is not a FreeRADIUS client, or (FortiOS 7.6.1 and later) Message-Authenticator handling | `freeradius -X` on `radius-174`; clients in `clients.conf` |
| `port3` cannot be changed on C2 | Objects still reference it | `diagnose sys cmdb refcnt show system.interface.name port3` |

## Security and Best Practices

- **Back up first.** Take the Lab 2.1 controller backup before you touch
  `port3`, firmware, or policies, and keep it until Lab 12.6.
- **Set real passwords.** FortiSwitchOS forces you to create an admin password
  at the first login and after a factory reset (Administration Guide 7.6.7).
  From FortiOS 7.6.1, a FortiGate generates an admin password for a switch that
  has none when it is authorized (FortiLink Guide 7.6.7, p. 43), so set your own
  first and record it.
- **Keep FortiLink off shared infrastructure.** `vmbrFL` carries only FortiLink,
  has no host IP address, and is not connected to the Nexus.
- **Remove temporary access.** The switch's temporary VLAN 99 address and the
  Nexus access port used for the firmware upgrade are removed at the end of Lab
  2.4 by the factory reset; shut the Nexus port afterwards.
- **Treat the RADIUS secret as a secret.** Use a long random value, keep it out
  of screenshots and notes, and limit `clients.conf` to the three source
  networks this lab needs.
- **Use GA firmware with a valid signature.** Check `Firmware Signature` in
  `get system status` and run `execute verify image primary` after every switch
  upgrade.

## References and Knowledge Checks

**References**

- [Fortinet, *FortiLink Guide (FortiOS 7.6.7)*](https://docs.fortinet.com/document/fortiswitch/7.6.7/fortilink-guide)
  — switch controller, FortiLink interface, neighbor detection (pp. 22–24),
  auto-discovery ports (pp. 30–31), firmware provisioning (pp. 38–40),
  authorizing (p. 41), FortiLink with HTTPS (pp. 50–52).
- [Fortinet, *FortiSwitchOS 7.6.7 CLI Reference*](https://docs.fortinet.com/document/fortiswitch/7.6.7/fortiswitchos-cli-reference)
  — `execute factoryreset`, `execute restore image`, `get system status`,
  `get hardware status`, `config switch auto-network`.
- [Fortinet, *FortiSwitchOS 7.6.7 Administration Guide (Standalone Mode)*](https://docs.fortinet.com/document/fortiswitch/7.6.7/fortiswitchos-administration-guide)
  — administrator password, management interfaces, upgrading the firmware,
  image verification.
- [Fortinet, FortiOS 7.6 documentation](https://docs.fortinet.com/product/fortigate/7.6)
  — the FortiOS 7.6.0 CLI Reference (`config system interface`,
  `config switch-controller managed-switch`, `config user radius`) and
  [Permanent trial mode for FortiGate-VM](https://docs.fortinet.com/document/fortigate/7.6.0/administration-guide/441460).
- [Fortinet Community, *How to test FortiGate's RADIUS user authentication to the RADIUS server*](https://community.fortinet.com/fortigate-3/troubleshooting-tip-how-to-test-fortigate-s-radius-user-authentication-to-the-radius-server-99819)
  — argument order of `diagnose test authserver radius`.
- [Fortinet Community, *RADIUS authentication failure after the firmware upgrade to v7.2.10/v7.4.5/v7.6.1*](https://community.fortinet.com/fortigate-3/troubleshooting-tip-radius-authentication-failure-after-the-firmware-upgrade-to-v7-2-10-v7-4-5-v7-6-1-182769)
  — Message-Authenticator behavior.
- [Proxmox VE, *PCI(e) Passthrough*](https://pve.proxmox.com/wiki/PCI(e)_Passthrough)
  and the [`qm(1)` manual](https://pve.proxmox.com/pve-docs/qm.1.html) —
  IOMMU, vfio modules, `hostpci`, and the `--net[n]` syntax.
- [`ip-link(8)`](https://man7.org/linux/man-pages/man8/ip-link.8.html) — the
  bridge `group_fwd_mask`, `stp_state`, and `vlan_filtering` options.
- FreeRADIUS 3.2
  [`clients.conf`](https://github.com/FreeRADIUS/freeradius-server/blob/v3.2.x/raddb/clients.conf)
  and [`radtest(1)`](https://manpages.ubuntu.com/manpages/noble/man1/radtest.1.html).
- [Volume XXVI, Chapter 05](../../volume-026-proxmox-lab-poweredge-r640/chapters/05-network-architecture-management-nic-vlan-trunk-and-bridges.md)
  — Proxmox bridges and `ifreload -a` on proxmox-1.

**Knowledge checks**

1. Why must the FortiLink vNIC on C2 have no VLAN tag, and why must `vmbrFL`
   not be VLAN-aware?
2. Which `group_fwd_mask` value lets a Linux bridge forward LLDP, and how is it
   derived from the LLDP destination address?
3. FGT-1 runs FortiOS 7.6.2. Which FortiLink neighbor-detection method is its
   default, and which does the FortiOS 7.6.0 CLI Reference list as the default?
4. What must you do to a used FortiSwitch before you connect it to a FortiGate,
   and which document says so?
5. The go/no-go test on C2 ends with the switch Discovered but never
   Authorized/Up. Name two checks you make before you conclude that the
   evaluation license is the cause.

## Hands-On Lab

**Shared prerequisites.** Your controller option and switch option chosen in
Chapter 01. Console access to the controller (C1) and the switch: an RJ-45
console cable and a USB serial adapter. Admin access to proxmox-1 (C2 and C3).
The TFTP VM 140 running at `10.30.99.50` with its root at `/tftpboot`. A free
Nexus access port on VLAN 99 (switch firmware upgrade) and, for C1, two more
(WAN on VLAN 99, services on VLAN 200). **Cost:** the hardware you chose in
Chapter 01; a dedicated NIC for proxmox-1 on C2 and C3.

Throughout, `FGT #` is the controller on any option and `<FL_PORT>` is its
FortiLink port: `<FL_PORT>` on C1, `port3` on C2, `port4` on C3. Blocks written
for `port3` apply to C3 with `port4` and to C1 with `<FL_PORT>`.

### Lab 2.1 — Prepare and baseline the controller

**Objective:** Bring the controller to a known FortiOS 7.6 state, record its
version, license, interfaces, policies, and routes, back it up, and reserve the
FortiLink port.

**Platform notes:** Hands-on on every option and on Track 2 (the controller is
the whole of Track 2). C1 adds a factory reset, a firmware upgrade, registration,
and cabling of `<WAN_PORT>` and `<SVC_PORT>`. C2 measures the evaluation budget
and takes `port3` out of VLAN 202. C3 confirms the full license and adds `port4`.
No switch is needed.

**Track 1 — C1 (hardware FortiGate 40F or 60F):**

1. Connect to the console with the serial settings from your model's QuickStart
   Guide (Fortinet appliances have historically used 9600 bps, 8 data bits, no
   parity, 1 stop bit). Record the version and serial number:

   ```text
   FGT # get system status
   ```

2. Register the serial number in FortiCare at `support.fortinet.com` (see
   [Volume XIX, Chapter 04](../../volume-019-fortinet-network-security/chapters/04-fortigate-first-deployment-licensing-management-and-hardening.md#registering-with-forticare-and-licensing)).
   If the portal reports that the unit belongs to another account, stop and
   arrange the transfer before going further.
3. Reset the used unit to factory defaults. It reboots:

   ```text
   FGT # execute factoryreset
   ```

4. Cable `<WAN_PORT>` to a Nexus access port on VLAN 99 and give it its lab
   address, so the unit can reach the TFTP VM:

   ```text
   FGT # config system interface
   edit <WAN_PORT>
   set mode static
   set ip 10.30.99.175 255.255.255.0
   set allowaccess ping https ssh
   next
   end
   ```

   The Nexus port follows the pattern of the existing access ports in
   [Volume CM, Chapter 04](../../volume-900-tims-lab-gear/chapters/04-current-device-configurations.md)
   (the Nexus defaults to `switchport shutdown`, so `no shutdown` is required):

   ```text
   interface Ethernet1/<x>
     description c1-fgt;<WAN_PORT>;vlan-99
     switchport access vlan 99
     spanning-tree port type edge
     no shutdown
   ```

5. Upgrade to FortiOS 7.6. Download each image on the supported path from the
   support portal, copy it to `/tftpboot` on VM 140, check its checksum against
   the portal's, and load it. Repeat for each step of the path:

   ```text
   FGT # execute ping 10.30.99.50
   FGT # execute restore image tftp <FGT_IMAGE> 10.30.99.50
   ```

6. Complete the addressing from Chapter 01: the default route, the services
   port on a Nexus access port in VLAN 200, and a host name:

   ```text
   FGT # config system global
   set hostname c1-fgt
   end
   FGT # config router static
   edit 0
   set gateway 10.30.99.1
   set device <WAN_PORT>
   next
   end
   FGT # config system interface
   edit <SVC_PORT>
   set mode static
   set ip 10.200.0.175 255.255.255.0
   set allowaccess ping
   next
   end
   ```

7. Choose `<FL_PORT>`. Many desktop models ship with an interface named
   `fortilink` (the FortiLink Guide's example is an aggregate with members `a`
   and `b`), and their LAN ports are members of a hardware switch (`lan` or
   `internal`). Look at both:

   ```text
   FGT # show system interface fortilink
   FGT # show system virtual-switch
   ```

   If the factory `fortilink` interface exists, use it as `<FL_PORT>`: it is
   Fortinet's recommended default type (FortiLink Guide 7.6.7, p. 23), and
   later chapters read `<FL_PORT>` as `fortilink`. Otherwise pick a free
   physical port (FortiLink is supported on every Ethernet port except HA and
   MGMT ports, p. 25) and remove it from the hardware switch:

   ```text
   FGT # config system virtual-switch
   edit lan
   config port
   delete <FL_PORT>
   end
   end
   ```

8. Back up the baseline:

   ```text
   FGT # execute backup config tftp c1-fgt-base-174.conf 10.30.99.50
   ```

**Track 1 — C2 (FGT-1 evaluation):**

1. Record the version and license, then the budget: physical interfaces,
   policies, and routes.

   ```text
   FGT # get system status
   FGT # get system interface physical
   FGT # show firewall policy
   FGT # show router static
   FGT # get router info routing-table all
   ```

   Fill in this table from the output:

   | Item | Cap | Used now | Used by VLAN 202 (`port3`) | Left after Lab 2.1 |
   | --- | --- | --- | --- | --- |
   | Physical interfaces | 3 | | | 3 (`port3` becomes FortiLink) |
   | Firewall policies | 3 | | | |
   | Static routes | 3 | | | |

2. Back up the whole configuration before releasing `port3`. Lab 12.6 restores
   VLAN 202 from this file:

   ```text
   FGT # execute backup config tftp fgt1-pre-174.conf 10.30.99.50
   ```

3. Record `port3` and everything that refers to it, then remove the references:
   the VLAN 202 policies and the VLAN 202 DHCP server. Use the IDs from the
   `show` output:

   ```text
   FGT # show system interface port3
   FGT # show system dhcp server
   FGT # diagnose sys cmdb refcnt show system.interface.name port3
   FGT # config firewall policy
   delete <VLAN202_POLICY_ID>
   end
   FGT # config system dhcp server
   delete <VLAN202_DHCP_ID>
   end
   ```

   Keep one VLAN 200 internet policy as P1 if FGT-1 has one; delete any other
   policy that the budget table shows you cannot afford (it is in the backup).

4. Take `port3` off VLAN 202 at the hypervisor. On proxmox-1, find the `netN`
   line whose MAC matches `port3` (`diagnose hardware deviceinfo nic port3` on
   FGT-1 shows the MAC; on FGT-1 `port3` is normally `net2`), then set its link
   down while keeping its model and MAC, so FortiOS keeps the same port:

   ```bash
   # on proxmox-1
   qm config 120 | grep ^net
   qm set 120 --net2 <MODEL>=<PORT3_MAC>,bridge=vmbr2,tag=202,link_down=1
   ```

   `port3` stays on `vmbr2` with its link down until Lab 2.3 moves it to the
   FortiLink path. On Track 2 it stays this way for the whole volume.

**Track 1 — C3 (licensed FortiGate-VM):**

1. Confirm the license and version, and check that no evaluation caps apply:

   ```text
   FGT # get system status
   FGT # get system interface physical
   ```

2. Back up, then add `port4`. Shut the VM down, add a fourth virtual NIC with
   its link down (Lab 2.3 moves it to `vmbrFL`), and start it again:

   ```text
   FGT # execute backup config tftp fgt-c3-pre-174.conf 10.30.99.50
   ```

   ```bash
   # on proxmox-1 (FGT-1 is VM 120; use your VM ID if C3 is another VM)
   qm shutdown 120
   qm set 120 --net3 virtio,bridge=vmbr2,link_down=1
   qm start 120
   qm config 120 | grep ^net3
   ```

3. Confirm that FortiOS shows the new port:

   ```text
   FGT # get system interface physical
   ```

   If C3 is a licensed FortiGate-VM other than FGT-1, give it the C1 addresses
   from Chapter 01 (`10.30.99.175/24`, `10.200.0.175/24` with source NAT toward
   the services segment).

**Track 2:** Do the steps for your controller. On FGT-1 alone, do the C2 steps:
`port3` is released from VLAN 202 and left with its link down.

**Expected result:** The controller runs FortiOS 7.6, its serial number and
license are recorded, a baseline backup is on VM 140, and the FortiLink port is
reserved: `<FL_PORT>` free on C1, `port3` free of VLAN 202 references with its
link down on C2, `port4` present on C3. On C2, the budget table shows at most
one policy and one route in use.

**Negative test:** On C2, ping the VLAN 202 test VM (VM 202, `test-vlan202`) from
FGT-1. It fails, which shows that VLAN 202 is out of service as Chapter 01
planned:

```text
FGT # execute ping <TEST202_IP>
```

On C1, run `execute restore image tftp` with a file name that is not on the
server: the transfer fails and `get system status` still shows the previous
version. On C3, `show system interface port4` before step 2 finds no entry.

**Rollback:** Restore the backup (`execute restore config tftp <FILE>
10.30.99.50`) and, on C2, set `link_down=0` with `tag=202` on `net2`; on C3,
remove `net3` (`qm set 120 --delete net3`). The full return to service is Lab
12.6.

**Lab verified by:** *pending*

### Lab 2.2 — Enable the switch controller and build the FortiLink interface

**Objective:** Turn on the switch controller, configure the FortiLink interface
at `10.255.1.1/24` with LLDP neighbor detection and manual authorization, make
sure it serves DHCP to switches, and test whether FortiOS accepts per-port
configuration for a switch that has never connected.

**Platform notes:** Hands-on on every option and on Track 2. The commands are
the same everywhere; only the port name changes (`<FL_PORT>` on C1, `port3` on
C2, `port4` on C3). On C1 with the factory `fortilink` interface, edit
`fortilink` instead and skip `set alias`. On Track 2 the port has no link, so
nothing is discovered. The FortiLink Guide (p. 22) says to finish this
configuration before connecting a switch; do not cable the switch yet.

**Track 1:**

1. Enable the switch controller. It may already be enabled; the GUI equivalent
   is **System > Feature Visibility > Switch Controller** (FortiLink Guide
   7.6.7, p. 22):

   ```text
   FGT # config system global
   set switch-controller enable
   end
   ```

2. Configure the FortiLink interface. Automatic authorization stays off, because
   Lab 3.1 authorizes the switch by hand:

   ```text
   FGT # config system interface
   edit port3
   set alias "fortilink"
   set mode static
   set ip 10.255.1.1 255.255.255.0
   set allowaccess ping fabric
   set fortilink enable
   set fortilink-neighbor-detect lldp
   set lldp-reception enable
   set lldp-transmission enable
   set auto-auth-extension-device disable
   next
   end
   ```

   `allowaccess ping fabric` matches the FortiLink interface examples in the
   FortiLink Guide (pp. 28–29). `fortilink-neighbor-detect lldp` is set
   explicitly so the result does not depend on the FortiOS 7.6.x build's
   default (see Theory and Architecture). Leave the switch-controller reserved
   network (`10.255.0.0/16`) and the initial-config templates at their defaults;
   templates can only be changed before the first switch is authorized (p. 34),
   and Lab 3.2 works with the defaults.

3. Check that the FortiLink interface serves DHCP to switches. FortiOS normally
   creates this server with the FortiLink interface (the guide's example shows
   one with `vci-string "FortiSwitch"`, p. 37). Look for it:

   ```text
   FGT # show system dhcp server
   ```

   If no server names your FortiLink port as its interface, create one. Its
   first lease is `10.255.1.2`, the switch address in Chapter 01:

   ```text
   FGT # config system dhcp server
   edit 0
   set interface "port3"
   set default-gateway 10.255.1.1
   set netmask 255.255.255.0
   set dns-service local
   set ntp-service local
   config ip-range
   edit 1
   set start-ip 10.255.1.2
   set end-ip 10.255.1.254
   next
   end
   set vci-match enable
   set vci-string "FortiSwitch"
   next
   end
   ```

4. Review the result. In the GUI, **WiFi & Switch Controller** is now a menu,
   with **FortiLink Interface** under it:

   ```text
   FGT # show system interface port3
   FGT # execute switch-controller get-conn-status
   ```

**Track 2:** Run steps 1 to 4 on the unlinked port. Then answer the open
question from Chapter 01: does FortiOS accept per-port configuration for a
switch that has never connected? The FortiOS 7.6.0 CLI Reference documents a
`pre-provisioned` attribute on `config switch-controller managed-switch` but no
procedure, and the FortiLink Guide 7.6.7 does not describe one, so this is an
experiment. Use the example serial number that the FortiLink Guide prints for an
FS-248E-POE (`S248EPTF18000000`, p. 39), because FortiOS takes the switch model
from the serial number's prefix:

```text
FGT # config switch-controller managed-switch
edit S248EPTF18000000
set fsw-wan1-peer "port3"
set fsw-wan1-admin enable
config ports
edit "port1"
set description "q4-test"
next
end
next
end
FGT # show switch-controller managed-switch S248EPTF18000000
```

Record which of three outcomes you get: FortiOS rejects the entry; it accepts
the entry but rejects `config ports` or `edit "port1"`; or it accepts both. Only
the third outcome lets Track 2 build per-port settings (Labs 4.2, 5.2, 7.2, and
the port steps of Chapter 08) instead of predicting them. Then delete the test
entry:

```text
FGT # config switch-controller managed-switch
delete S248EPTF18000000
end
```

**Track 2: read-and-predict.** The FortiLink Guide (p. 52) shows this extract
of `execute switch-controller get-conn-status` with four switches, two of them
not yet authorized:

```text
SWITCH-ID VERSION STATUS FLAG ADDRESS JOIN-TIME
S248EPTF18001827 N/A Discovered/Down 2 N/A
S124EN5918003682 N/A Discovered/Down 2 N/A
Flags: C=config sync, U=upgrading, S=staged, D=delayed reboot pending, E=config sync error,
2=L2, 3=L3, V=VXLAN, T=tunnel, X=External
```

Predict what your own switch's row will show in the VERSION and ADDRESS columns
the first time it is cabled in Lab 2.4, before you authorize it. **Answer:**
`N/A` in both, with STATUS `Discovered/Down` and FLAG `2`. The controller has
heard the switch on Layer 2 but has no management session with it yet, so it
knows neither its running version nor a management address.

**Expected result:** `show system interface` shows the FortiLink port with
`fortilink enable`, IP `10.255.1.1 255.255.255.0`, and
`fortilink-neighbor-detect lldp`; a DHCP server serves the FortiLink port from
`10.255.1.2`; the GUI shows **WiFi & Switch Controller**. On Track 2 the
pre-provisioning outcome is recorded.

**Negative test:** `execute switch-controller get-conn-status` lists the
FortiLink interface and no switches. Configuration alone discovers nothing: the
controller needs the Layer 2 path of Lab 2.3 and a switch at factory defaults
(Lab 2.4).

**Rollback:** `set fortilink disable` on the port, delete any DHCP server you
created, and restore the port's previous settings from the Lab 2.1 backup. Leave
the switch controller enabled.

**Lab verified by:** *pending*

### Lab 2.3 — Build the physical FortiLink path

**Objective:** Give the FortiLink port a Layer 2 path to the switch that carries
tagged VLANs, LLDP, and BPDUs, and prove that LLDP crosses it.

**Platform notes:** C1: hands-on, a patch cable only (no Proxmox changes). C2
and C3: hands-on, a dedicated NIC in proxmox-1 with either Option A (`vmbrFL`)
or Option B (PCI passthrough); `net2` (`port3`) on C2, `net3` (`port4`) on C3.
The switch need not be upgraded yet; the LLDP checks below work with only the
FortiGate transmitting. Track 2: read-and-predict.

**Track 1 — C1:**

1. Cable `<FL_PORT>` to `<FSW_FL_PORT>` on the switch (Design Considerations
   gives `<FSW_FL_PORT>` per model). For the factory `fortilink` aggregate, cable
   one of its members.
2. Check the link:

   ```text
   FGT # get system interface physical
   FGT # diagnose hardware deviceinfo nic <FL_PORT>
   ```

**Track 1 — C2 and C3, common steps:**

1. Install the dedicated NIC in proxmox-1 and find its name and PCI address. Do
   not reuse `nic1` to `nic4`; all four are in service (Volume CM, Chapter 02):

   ```bash
   # on proxmox-1
   ip -br link
   lspci -nn | grep -i ethernet
   ```

2. Cable the new NIC to `<FSW_FL_PORT>` on the switch.

**Track 1 — Option A, the `vmbrFL` bridge:**

1. Add the bridge to `/etc/network/interfaces` on proxmox-1. It has no IP
   address, no `bridge-vlan-aware` line, STP off, and the LLDP bit in
   `group_fwd_mask`:

   ```text
   auto <NEW_NIC>
   iface <NEW_NIC> inet manual

   auto vmbrFL
   iface vmbrFL inet manual
       bridge-ports <NEW_NIC>
       bridge-stp off
       bridge-fd 0
       post-up echo 16384 > /sys/class/net/vmbrFL/bridge/group_fwd_mask
   ```

   Apply it with `ifreload -a` (or **Apply Configuration** in the GUI, as in
   [Volume XXVI, Chapter 05](../../volume-026-proxmox-lab-poweredge-r640/chapters/05-network-architecture-management-nic-vlan-trunk-and-bridges.md)).
   Proxmox VE accepted only `vmbr<N>` bridge names until a 2024 change that
   allows names starting with a letter (the patch series limits them to 10
   characters); proxmox-1 runs Proxmox VE 9.2.9. If your release rejects
   `vmbrFL`, use a numbered name such as `vmbr3` and read it for `vmbrFL`.

2. Move the FortiLink vNIC to the bridge, untagged and with its link up. Keep
   the model and MAC from `qm config`:

   ```bash
   # on proxmox-1
   ifreload -a
   qm set 120 --net2 <MODEL>=<PORT3_MAC>,bridge=vmbrFL     # C2: port3
   qm set 120 --net3 <MODEL>=<PORT4_MAC>,bridge=vmbrFL     # C3: port4
   qm config 120 | grep ^net
   ```

3. Run `/root/fl-path-check.sh` (Implementation and Automation). FGT-1 transmits
   LLDP on the FortiLink port (`lldp-transmission enable`, Lab 2.2), so LLDP
   frames appear on the tap device and, forwarded by the bridge, on the NIC. If
   the switch is powered and cabled, its LLDP frames appear in the other
   direction too.
4. With the switch cabled, check BPDUs the same way:

   ```bash
   # on proxmox-1
   timeout 35 tcpdump -i tap120i2 -e -n -c 2 ether dst 01:80:c2:00:00:00
   ```

**Track 1 — Option B, PCI passthrough:**

1. Enable VT-d (Intel Virtualization Technology for Directed I/O) in the
   server's BIOS. With kernel 6.8 or newer, which current Proxmox VE uses, the
   IOMMU is on by default for Intel CPUs (Proxmox VE wiki); older kernels need
   `intel_iommu=on`. Load the vfio modules and rebuild the initramfs, then
   reboot the host:

   ```bash
   # on proxmox-1
   printf 'vfio\nvfio_iommu_type1\nvfio_pci\n' > /etc/modules-load.d/vfio.conf
   update-initramfs -u -k all
   reboot
   ```

2. After the reboot, confirm the IOMMU and check that the NIC is alone in its
   IOMMU group:

   ```bash
   # on proxmox-1
   dmesg | grep -e DMAR -e IOMMU -e AMD-Vi
   pvesh get /nodes/proxmox-1/hardware/pci --pci-class-blacklist ""
   ```

3. Pass the NIC to the VM. On C2, delete `net2` first so the passed-through NIC
   can take the third interface slot (the evaluation allows three); on C3, add
   it beside the existing NICs:

   ```bash
   # on proxmox-1
   qm shutdown 120
   qm set 120 --delete net2          # C2 only
   qm set 120 -hostpci0 <PCI_ADDR>
   qm start 120
   ```

4. On the FortiGate, find which port the NIC became and that FortiOS has a
   driver for it:

   ```text
   FGT # get system interface physical
   FGT # diagnose hardware deviceinfo nic port3
   ```

   On C2 the passed-through NIC must appear as `port3`, so that the FortiLink
   configuration of Lab 2.2 applies to it; on C3, as `port4`. If FortiOS shows
   no new port, it has no driver for the card: use Option A. The host can no
   longer see or use the NIC (Proxmox VE wiki), so the `tcpdump` checks do not
   apply; Lab 2.4's discovery is the test.

**Track 2: read-and-predict.**

1. LLDP frames are sent to `01:80:C2:00:00:0E`. A Linux bridge forwards a
   frame sent to `01:80:C2:00:00:0X` only if bit *X* of `group_fwd_mask` is set.
   Predict the decimal mask that forwards LLDP and nothing else in that range.
   **Answer:** 16384. `0E` is 14, and 2^14 = 16384.
2. FGT-1's FortiLink vNIC is left with `tag=202` on the VLAN-aware `vmbr2`.
   Predict which of the switch's frames reach the FortiGate: its FortiLink
   management traffic, or its VLAN 1741 frames. **Answer:** neither. A tagged
   vNIC on a VLAN-aware bridge delivers only frames of its own VLAN (202); the
   switch's FortiLink port carries no VLAN 202. That is why Chapter 01 requires
   an untagged vNIC on a bridge that is not VLAN-aware.

**Expected result:** C1: `<FL_PORT>` shows link up. Option A: `group_fwd_mask =
16384`, `stp_state = 0`, `vlan_filtering = 0`; LLDP frames appear on both the tap
device and the NIC; with the switch cabled, BPDUs reach the tap. Option B: the
NIC appears in FortiOS as `port3` (C2) or `port4` (C3).

**Negative test:** On Option A, clear the mask and repeat the check. LLDP from
FGT-1 still appears on the tap device but no longer on the NIC, because the
bridge now drops it; with `fortilink-neighbor-detect lldp`, a switch on the far
side would never be discovered. Restore the mask afterwards:

```bash
# on proxmox-1
echo 0 > /sys/class/net/vmbrFL/bridge/group_fwd_mask
/root/fl-path-check.sh
echo 16384 > /sys/class/net/vmbrFL/bridge/group_fwd_mask
```

On C1, unplug the cable: `get system interface physical` shows `<FL_PORT>`
down.

**Rollback:** On C2, move `net2` back to `bridge=vmbr2,tag=202` (or remove
`hostpci0` and re-add `net2` with its old model and MAC); on C3, remove `net3`
or `hostpci0`. Remove the `vmbrFL` stanza and run `ifreload -a`. Lab 12.6 does
this at the end of the volume.

**Lab verified by:** *pending*

### Lab 2.4 — Prepare the switch and run the FortiLink go/no-go test

**Objective:** Reset the switch, upgrade it to FortiSwitchOS 7.6.x over TFTP,
check its model against the capability matrix, return it to factory defaults,
and prove that the controller can discover, authorize, and manage it.

**Platform notes:** Hands-on on S1, S2, and S3 (on S3, steps 1 to 10 on both
switches; only `FSW-A` is cabled for the go/no-go test, and `FSW-B` waits for
the chapter that adds it). The go/no-go test is **required on C2** and a
recommended smoke test on C1 and C3. Models with a dedicated management port use
`mgmt` for the temporary address; models without one use `internal` through
`port3`. Track 2: read-and-predict.

**Track 1 — switch preparation:**

1. Connect the console cable. From a Linux host with `picocom`, or any terminal
   program, use the serial settings from the model's QuickStart Guide (Fortinet
   switches have historically used 9600 bps, 8-N-1):

   ```bash
   picocom -b 9600 /dev/ttyUSB0
   ```

2. Log in as `admin` with no password. FortiSwitchOS makes you create an admin
   password at the first login and after every factory reset (Administration
   Guide 7.6.7). Record the starting state:

   ```text
   FSW # get system status
   FSW # get hardware status
   ```

   Note `Version`, `Serial-Number` (this is `<SWITCH_SN>`), `Firmware
   Signature`, and `Model name`.

3. Reset a used switch to factory defaults. It reboots, and you set the admin
   password again:

   ```text
   FSW # execute factoryreset
   ```

4. Download the FortiSwitchOS 7.6.x image for the exact model from the support
   portal, check the release notes' upgrade path from your starting version, and
   copy the image to `/tftpboot` on VM 140. Compare its checksum with the one
   the portal lists.
5. Give the switch a temporary address on VLAN 99. On a model with a
   dedicated management port, cable `mgmt` to a Nexus access port on VLAN 99
   and set:

   ```text
   FSW # config system interface
   edit mgmt
   set mode static
   set ip 10.30.99.174 255.255.255.0
   set allowaccess ping https ssh
   next
   end
   ```

   On a model without one, cable `port3` to the Nexus port instead and set the
   same address on `internal`; at factory defaults, VLAN 1 spans every front
   port and the internal interface (FortiLink Guide 7.6.7, p. 15):

   ```text
   FSW # config system interface
   edit internal
   set mode static
   set ip 10.30.99.174 255.255.255.0
   set allowaccess ping https ssh
   next
   end
   ```

   Configure the Nexus port like Lab 2.1's, but without BPDU guard: a
   FortiSwitch front-panel port runs MSTP and sends BPDUs, which would
   err-disable a port with `spanning-tree bpduguard enable`.

6. Load the image. The switch downloads it, writes it, and reboots:

   ```text
   FSW # execute ping 10.30.99.50
   FSW # execute restore image tftp <FSW_IMAGE> 10.30.99.50
   ```

7. After the reboot, check the version, the signature, and the stored image:

   ```text
   FSW # get system status
   FSW # execute verify image primary
   ```

   `Version` shows FortiSwitchOS 7.6.x, `Firmware Signature` is not `invalid`,
   and the verification reports no issue.

8. Check the model against the capability matrix. Find the `Model name` from
   `get hardware status` in Chapter 01's switch options and capability matrix,
   and read the notes for your exact model: the FS-108F and FS-124F share the
   **1xxE, 1xxF** column and differ only where a cell names models (sFlow, flow
   export, packet capture) or a note names one of them (note 12, NAC LAN
   segments, names the FS-108F); in the **200 Series** column, note 3 excludes
   the FS-248E-POE and FS-248E-FPOE from the per-VLAN MAC learning limit, and
   note 17 excludes the FS-224D-FPOE and FS-248D from image signature
   verification. On S3, confirm that both switches are 200 Series models.
9. Reset again, so the switch returns to zero-touch defaults (auto-network,
   FortiLink discovery on its ports) and the temporary address is gone. Set the
   admin password at the next login and record it:

   ```text
   FSW # execute factoryreset
   ```

10. Unplug the Nexus cable and shut that Nexus port (`shutdown`).

**Track 1 — the FortiLink go/no-go test:**

1. Cable `<FSW_FL_PORT>` to the controller's FortiLink path (Lab 2.3). Within a
   few minutes the switch appears as discovered:

   ```text
   FGT # execute switch-controller get-conn-status
   ```

   Look for `<SWITCH_SN>` with STATUS `Discovered/Down` and FLAG `2`.

2. Authorize it. The switch reboots in FortiLink mode (FortiLink Guide 7.6.7,
   p. 41; p. 14 of the same guide says no restart is needed, so record whether
   yours reboots):

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   set fsw-wan1-admin enable
   next
   end
   ```

3. Wait for the reboot, then check the connection, the lease, and reachability:

   ```text
   FGT # execute switch-controller get-conn-status
   FGT # execute dhcp lease-list port3
   FGT # execute ping 10.255.1.2
   ```

4. Decide:

   | Result | Meaning |
   | --- | --- |
   | STATUS `Authorized/Up`, VERSION showing the 7.6.x build, ADDRESS `10.255.1.2`, still Up after 10 minutes, and the ping answers | **GO.** The controller manages the switch. C2 is confirmed for Track 1 |
   | Never `Discovered` | Path problem, not a license problem: go back to Lab 2.3 |
   | `Discovered/Down` after authorization, `Authorized/Down`, or flapping | **Not yet NO-GO.** Work through the checks below |

5. Before calling NO-GO, check in this order:
   1. The path still passes LLDP (`fl-path-check.sh`), or switch detection to
      the FortiLink protocol and retry:

      ```text
      FGT # config system interface
      edit port3
      set fortilink-neighbor-detect fortilink
      next
      end
      ```

   2. `show system interface port3` includes `fabric` in `allowaccess`, and the
      switch has a lease from the FortiLink DHCP server.
   3. The FortiLink Compatibility table supports your FortiOS and FortiSwitchOS
      pair.
   4. On the switch console, the switch's own view of the session (FortiSwitchOS
      7.6.7 CLI Reference; it shows `Connection` and `DTLS Version`):

      ```text
      FSW # execute switch-controller get-conn-status
      ```

   5. Optionally, move FGT-1 to a later FortiOS 7.6.x build over TFTP
      ([Volume XIX, Lab 4.8](../../volume-019-fortinet-network-security/chapters/04-fortigate-first-deployment-licensing-management-and-hardening.md#lab-48--upgrading-firmware-over-tftp-from-the-cli-topic-firmware-lifecycle))
      and repeat the test.

6. If the switch still never reaches Authorized/Up on C2 while the same switch
   and firmware pass on a different controller, the result is **NO-GO**: the
   evaluation does not manage this switch. Record it, keep FGT-1 for Track 2
   (which does not need a managed switch), and move Track 1 to C1 (a hardware
   FortiGate) or C3 (a licensed FortiGate-VM). Without a second controller to
   compare, record the result as "NO-GO on this setup" and use C1 or C3 for
   Track 1.
7. After a GO, return the lab to the starting point of Lab 3.1, which
   authorizes the switch as its first step. Deauthorize it, reset it from its
   console (your admin password still works: FortiOS keeps an existing switch
   password, FortiLink Guide 7.6.7, p. 43), and delete its entry so that it is
   discovered afresh:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   set fsw-wan1-admin disable
   next
   end
   FSW # execute factoryreset
   FGT # config switch-controller managed-switch
   delete <SWITCH_SN>
   end
   ```

   If you set `fortilink-neighbor-detect fortilink` in step 5, record it; later
   chapters assume `lldp` unless your go/no-go record says otherwise.

**Track 2: read-and-predict.** The FortiSwitchOS 7.6.7 CLI Reference (p. 535)
prints this example of `get system status`:

```text
S124EN4N17002351 # get system status
Version: FortiSwitch-124E v7.6.2,build1071,250326 (Interim)
Serial-Number: S124EN4N17002351
Firmware Signature: invalid
```

1. Predict whether this switch is ready for the lab as it stands. **Answer:**
   no. It runs an interim build whose signature check reports `invalid`; the
   lab uses a GA FortiSwitchOS 7.6.x image whose signature verifies. The model
   (FS-124E) is not one of S1–S3 either, although it shares the **1xxE, 1xxF**
   column of the feature matrix.
2. Predict the value you would use in `edit <SWITCH_SN>` to authorize it.
   **Answer:** `S124EN4N17002351`, the `Serial-Number` field, which is also the
   factory host name in the prompt.
3. A switch was authorized on a controller and is now healthy. Predict its
   STATUS and the source of its ADDRESS in `get-conn-status`. **Answer:**
   `Authorized/Up`, with an address leased by the FortiLink interface's DHCP
   server; the FortiLink Guide's examples (pp. 40 and 52) show leases such as
   `10.255.1.2` from a `10.255.1.1` FortiLink interface.

**Expected result:** The switch runs a GA FortiSwitchOS 7.6.x image with a
verified signature, its model is checked against the capability matrix, it is
back at factory defaults with a known admin password, and the go/no-go result is
recorded (GO, or NO-GO with the fallback controller chosen). After a GO, the
switch is cabled, discovered, and unauthorized, ready for Lab 3.1.

**Negative test:** Before step 2 of the go/no-go test, leave the switch
unauthorized for ten minutes. It stays `Discovered/Down` with VERSION and
ADDRESS `N/A`: discovery alone gives no management session, which is what Lab
3.1's negative test builds on.

**Rollback:** `execute factoryreset` on the switch and delete its entry on the
controller, as in step 7. A failed upgrade can be repeated from step 6; the
switch keeps its previous image until a new one is written.

**Lab verified by:** *pending*

### Lab 2.5 — Build the shared services and the services policy

**Objective:** Build `radius-174` and prove the controller can authenticate
against it, prepare the syslog listener on `ubuntu-ws` and the endpoints, and
add the services policy (P2) so the switch can reach these services.

**Platform notes:** Hands-on on every option and on Track 2 (the RADIUS test is
live there too). On C1 the services policy uses source NAT, because the VLAN 200
hosts keep FGT-1 (`10.200.0.1`) as their gateway; on C2 and C3 it does not. On
C2 the policy is slot P2 of the evaluation's three. Endpoints are needed only on
Track 1.

**Track 1:**

1. Create the VM `radius-174` on proxmox-1: Ubuntu Server 24.04, 1 vCPU, 2 GB
   RAM, one virtio NIC on `vmbr2` with tag 200. The per-hypervisor creation
   steps are in
   [Volume 997, Appendix 73](../../volume-997-master-appendices/chapters/73-appendix-deploying-lab-appliance-images-on-each-hypervisor.md).
   VM ID 174 is free in the current inventory (Volume CM, Chapter 02):

   ```bash
   # on proxmox-1, after creating VM 174 from the Ubuntu ISO
   qm set 174 --net0 virtio,bridge=vmbr2,tag=200
   ```

2. Give it its static address in the netplan file the installer created under
   `/etc/netplan/` (replace its contents; the interface name is in
   `ip -br link`, commonly `ens18` for a Proxmox virtio NIC), apply it, and
   install FreeRADIUS:

   ```yaml
   network:
     version: 2
     ethernets:
       <IFACE>:
         addresses: [10.200.0.174/24]
         routes:
           - to: default
             via: 10.200.0.1
         nameservers:
           addresses: [<DNS_SERVER>]
   ```

   ```bash
   sudo netplan apply
   sudo apt update && sudo apt install -y freeradius freeradius-utils
   ```

3. Add the three RADIUS clients this volume uses to
   `/etc/freeradius/3.0/clients.conf`: FGT-1 (C2 and C3), the C1 services
   address, and the FortiLink subnet, from which a managed switch sends its own
   RADIUS requests in Chapter 07 (on C2 and C3 they arrive without NAT).
   `ipaddr` accepts CIDR ranges (FreeRADIUS 3.2 `clients.conf`):

   ```text
   client fgt-1 {
       ipaddr = 10.200.0.1
       secret = <RADIUS_SECRET>
   }
   client c1-svc {
       ipaddr = 10.200.0.175
       secret = <RADIUS_SECRET>
   }
   client fortilink-174 {
       ipaddr = 10.255.1.0/24
       secret = <RADIUS_SECRET>
   }
   ```

4. Add a test user at the top of the users file,
   `/etc/freeradius/3.0/mods-config/files/authorize`, in the format of the
   file's own example:

   ```text
   labuser Cleartext-Password := "<LAB_PASSWORD>"
   ```

5. Restart the service and test locally. The stock `clients.conf` defines a
   `localhost` client whose secret is `testing123`:

   ```bash
   sudo systemctl restart freeradius
   radtest labuser '<LAB_PASSWORD>' 127.0.0.1 10 testing123
   ```

6. Point the controller at the server and test it. The argument order (server,
   method, user, password) is from a Fortinet Community troubleshooting tip;
   neither local CLI reference prints it:

   ```text
   FGT # config user radius
   edit "radius-174"
   set server "10.200.0.174"
   set secret <RADIUS_SECRET>
   next
   end
   FGT # diagnose test authserver radius radius-174 pap labuser <LAB_PASSWORD>
   ```

   FortiOS 7.6.1 changed how FortiOS handles the RADIUS Message-Authenticator
   attribute. If the test reports a missing Message-Authenticator, the Fortinet
   Community tip on that change gives a per-server setting,
   `set require-message-authenticator disable`; it is not in the FortiOS 7.6.0
   CLI Reference, so check that your build offers it (type `?` at the prompt)
   before you use it. Run `sudo freeradius -X` on `radius-174` (after
   `sudo systemctl stop freeradius`) to watch each request.

7. Prepare the syslog listener on `ubuntu-ws` (`10.200.0.20`). The sFlow and
   flow-export collectors are installed in Lab 12.2. Create
   `/etc/rsyslog.d/10-fsw-174.conf`:

   ```text
   module(load="imudp")
   input(type="imudp" port="514")
   ```

   ```bash
   sudo systemctl restart rsyslog
   logger -n 127.0.0.1 -P 514 -d "fsw-174 syslog test"
   grep "fsw-174 syslog test" /var/log/syslog
   ```

8. Prepare the endpoints. Endpoint A (for `port1`) is a Linux laptop or a
   Raspberry Pi with `wpasupplicant` installed for Chapter 07; endpoint B (for
   `port2`) is a second Linux host with `dnsmasq` installed and disabled, for the
   rogue DHCP server test in Chapter 08. Record each endpoint's wired MAC address,
   which Chapters 07 and 09 use for MAB and NAC:

   ```bash
   sudo apt install -y wpasupplicant      # endpoint A
   sudo apt install -y dnsmasq && sudo systemctl disable --now dnsmasq   # endpoint B
   ip -br link
   ```

9. Add the services objects and policy P2 on the controller. The service object
   covers RADIUS (UDP 1812–1813), syslog (UDP 514), SNMP traps (UDP 162), and
   sFlow (UDP 6343). Chapter 04 adds the `FSW-LAN` zone to P2's sources. On C2
   and C3:

   ```text
   FGT # config firewall service custom
   edit "lab-svc-174"
   set udp-portrange 1812-1813 514 162 6343
   next
   end
   FGT # config firewall address
   edit "radius-174"
   set subnet 10.200.0.174 255.255.255.255
   next
   edit "ubuntu-ws"
   set subnet 10.200.0.20 255.255.255.255
   next
   end
   FGT # config firewall policy
   edit 0
   set name "P2-fortilink-services"
   set srcintf "port3"
   set dstintf "port2"
   set srcaddr "all"
   set dstaddr "radius-174" "ubuntu-ws"
   set action accept
   set schedule "always"
   set service "lab-svc-174"
   set logtraffic all
   next
   end
   ```

   On C1, build the same objects and the same policy with `srcintf
   "<FL_PORT>"`, `dstintf "<SVC_PORT>"`, and source NAT, so that replies from
   the VLAN 200 hosts come back to `10.200.0.175` instead of going to FGT-1:

   ```text
   FGT # config firewall policy
   edit 0
   set name "P2-fortilink-services"
   set srcintf "<FL_PORT>"
   set dstintf "<SVC_PORT>"
   set srcaddr "all"
   set dstaddr "radius-174" "ubuntu-ws"
   set action accept
   set schedule "always"
   set service "lab-svc-174"
   set nat enable
   set logtraffic all
   next
   end
   ```

10. On C2, update the Lab 2.1 budget table: P1 (if kept) and P2 used, P3 free.

**Track 2:** Do steps 1 to 7, 9, and 10 on your controller. Skip step 8; Track 2
has no endpoints. The RADIUS test in step 6 is a live test on Track 2 as well,
and it is the basis of Lab 7.1.

**Expected result:** `radtest` returns `Access-Accept`; the FortiGate test
reports that `labuser` authenticated against `pap` (the Community tip's sample
reads `authenticate 'raduser1' against 'pap' succeeded`); the syslog test line
is in `/var/log/syslog` on `ubuntu-ws`; the endpoints' MAC addresses are
recorded; P2 exists, with source NAT on C1 only. On C2, at most two of the three
policy slots are in use.

**Negative test:** Set a wrong secret on the controller and repeat the
authserver test. It fails, and `freeradius -X` on `radius-174` shows the request
arriving but failing its authenticator check. Restore the correct secret:

```text
FGT # config user radius
edit "radius-174"
set secret <WRONG_SECRET>
next
end
FGT # diagnose test authserver radius radius-174 pap labuser <LAB_PASSWORD>
```

**Rollback:** Delete P2, `lab-svc-174`, the two address objects, and
`radius-174` on the controller; stop VM 174; remove
`/etc/rsyslog.d/10-fsw-174.conf` on `ubuntu-ws`. Lab 12.6 does this at the end
of the volume.

**Lab verified by:** *pending*

## Lab Verification

Complete this sign-off once Labs 2.1 to 2.5 have been run end to end, including
each negative test and, on C2, the go/no-go test. Until then, the labs are
unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter prepared every platform option. The controller runs FortiOS 7.6
with a FortiLink interface at `10.255.1.1/24` that detects neighbors by LLDP and
authorizes switches by hand. On C2 and C3, a dedicated NIC on a plain bridge
(with `group_fwd_mask` 16384) or PCI passthrough gives the FortiGate-VM a direct
Layer 2 path. The switch runs a verified GA FortiSwitchOS 7.6.x image and is back
at factory defaults, and the go/no-go test has shown whether your controller can
manage it. RADIUS, syslog, TFTP, the endpoints, and the services policy are
ready. Track 2 has the same controller configuration, a live RADIUS test, and a
recorded answer to the pre-provisioning question.

- [ ] I recorded the controller's version, serial number, and license, and
      backed it up to VM 140.
- [ ] On C2, I filled in the budget table and released `port3` from VLAN 202.
- [ ] The FortiLink interface has `10.255.1.1/24`, LLDP neighbor detection,
      `fabric` access, and a DHCP server starting at `10.255.1.2`.
- [ ] On Track 2, I recorded whether FortiOS accepted a pre-provisioned switch
      and its port settings.
- [ ] LLDP crosses the FortiLink path in both directions (or the passed-through
      NIC is the FortiLink port).
- [ ] The switch runs FortiSwitchOS 7.6.x with a verified signature and is at
      factory defaults with a known admin password.
- [ ] I recorded the go/no-go result and, after a NO-GO on C2, chose C1 or C3
      for Track 1.
- [ ] `diagnose test authserver` succeeds against `radius-174`, and P2 exists.
