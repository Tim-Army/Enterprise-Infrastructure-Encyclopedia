# Chapter 05: Spanning Tree and Loop Protection

## Learning Objectives

- Explain how a managed FortiSwitch runs the Multiple Spanning Tree Protocol
  (MSTP): regions, the internal spanning tree (instance 0), extra instances,
  port roles, and why the switch, not the FortiGate, is the root on a single
  FortiLink switch.
- Configure the global STP settings and an MSTP instance from the FortiGate,
  set a per-switch instance priority, and read the result from the controller
  and from the switch.
- Configure edge ports, BPDU guard, root guard, and loop guard on managed ports;
  state each feature's prerequisites, defaults, and recovery; and tell Fortinet
  **loop guard** apart from **STP loop protection**.
- Create a Layer 2 loop on the isolated lab switch with a patch cable, safely,
  and recognize it in the STP tables, the BPDU guard and loop guard status
  tables, and the port counters.
- Describe STP on the FortiLink side: why the FortiLink link itself does not run
  STP, the one documented topology where the FortiGate's FortiLink interface
  does, how a FortiGate is made the root of the common and internal spanning
  tree (CIST), and the rules for interoperating with a Rapid PVST+ (RPVST+)
  network.

## Theory and Architecture

### Where spanning tree runs in FortiLink mode

A managed FortiSwitch runs spanning tree itself; the FortiGate configures it.
The controller holds the global STP settings (`config switch-controller
stp-settings`), the MSTP instance map (`config switch-controller stp-instance`),
per-switch overrides under the managed-switch entry, and per-port settings under
`config ports` (FortiLink Guide 7.6.7, pp. 132–141). The switch builds the
spanning tree from those settings and reports it back.

The FortiLink link is not part of that tree. The FortiLink Guide says plainly
that STP is not supported between a FortiGate and a FortiSwitch in FortiLink mode
(p. 136), and its example output lists the switch's FortiLink trunk
(`__FoRtI1LiNk0__`) and `internal` interface as `DESIGNATED`, `FORWARDING`, with
STP status `DISABLED` (pp. 137–138). So on a single managed switch the switch is
the root bridge of every instance: no other bridge sends it BPDUs. On S3 the
second switch joins the tree in Chapter 06.

STP is enabled by default on the non-FortiLink ports of a managed switch, and
has been since FortiSwitch release 3.4.2; loop guard is disabled by default on
all ports (pp. 132, 136).

### MSTP in brief

FortiSwitchOS runs MSTP (IEEE 802.1s), which is built on RSTP (802.1w) and is
backward compatible with STP and RSTP; a network can mix switches running any of
the three (FortiLink Guide 7.6.7, p. 134; FortiSwitchOS 7.6.7 Administration
Guide, p. 261). The terms the exam and the diagnostics use:

| Term | Meaning (FortiSwitchOS 7.6.7 Administration Guide, pp. 261–263) |
| --- | --- |
| **Region** | Switches with the same MST configuration: region **name**, **revision**, and VLAN-to-instance map. The `MD5 Digest` in the diagnostics summarizes the map |
| **IST** (instance 0) | The internal spanning tree that connects all MST switches in a region. Every VLAN not mapped elsewhere is in it, and it is the only instance that sends BPDUs; the other instances ride in it as M-records |
| **CST** | The common spanning tree that connects MST regions and STP or RSTP bridges; with the ISTs it forms the CIST |
| **MST instance** (1 and up) | A separate tree for the VLANs mapped to it, with its own bridge priority and port costs. Do not map a VLAN to more than one instance |
| **Hop count** | Inside a region BPDUs age by `max-hops` (default 20), not by message age |

Port roles decide what a port does:

| Role | What it is | State when converged |
| --- | --- | --- |
| Root | The one port on a bridge that leads to the root bridge | Forwarding |
| Designated | The port on a segment closest to the root; it sends BPDUs on that segment | Forwarding |
| Alternate | Another path to the root, not chosen | Blocking (discarding) |
| Backup | Two or more ports of the **same switch** connected together: one is designated, the rest are backup | Blocking (discarding) |
| Disabled | No link, or STP not running on the port | — |

The **backup** role is the one this chapter's loop cable produces: `port5` and
`port6` are two ports of one switch joined by a patch cable, so one of them is
designated and the other is backup (Administration Guide, p. 262).

The switch's timers come from the global settings: `hello-time` 2 seconds,
`forward-time` 15 seconds, `max-age` 20 seconds, `max-hops` 20 (FortiOS 7.6.0
CLI Reference, `config switch-controller stp-settings`). Instance priorities are
multiples of 4096 from 0 to 61440, default 32768; the lowest bridge ID (priority,
then MAC address) becomes root (`config stp-instance` under the managed-switch
entry). From FortiSwitchOS 7.6.7, `auto-stp-priority` and `auto-stp-cost` under
the switch's `config switch global` control the automatic STP priority and the
cost of 1 that automatically formed ISLs receive; the FortiLink Guide describes
both under `auto-stp-priority` and warns that changing it takes FortiLink down
briefly (p. 134), while the FortiSwitchOS 7.6.7 CLI Reference splits them into
the two options (p. 114). This chapter leaves both alone.

### Instance counts

The 7.6.7 feature matrix gives **MSTP instances 0–31** for the 1xxE/1xxF column
(S1 and S2) and the 200 Series column (S3), and 0–63 for larger models. The
FortiSwitchOS 7.6.7 Administration Guide says the switch supports 15 MST
instances in a region (p. 261), and the CLI Reference says the instance range
differs by model. This lab uses instance 1 only, which every reading allows.

### Edge ports and the protection features

| Feature | Managed-port option (FortiOS 7.6.0) | What it does | Default | Prerequisites |
| --- | --- | --- | --- | --- |
| STP on the port | `stp-state {enabled \| disabled}` | Runs spanning tree on the port | `enabled` | — |
| Edge port | `edge-port {enable \| disable}` | Marks a port that has no bridge behind it; it goes straight to forwarding instead of passing through listening and learning | `enable` | — |
| BPDU guard | `stp-bpdu-guard {enabled \| disabled}`, `stp-bpdu-guard-timeout <0-120>` minutes | Any BPDU received takes the port down for the timeout; 0 means it stays down until reset | `disabled`, timeout 5 | Edge port and STP enabled on the port |
| Root guard | `stp-root-guard {enabled \| disabled}` | Superior BPDUs received on the port are ignored or dropped, so the port cannot become the path to a new root | `disabled` | STP enabled on the port |
| Loop guard | `loop-guard {enabled \| disabled}`, `loop-guard-timeout <0-120>` minutes | Fortinet's loop detector: the port broadcasts loop guard data packets (LGDP) and takes itself out of service if one comes back | `disabled`, timeout 45 | Use it separately from STP on a port |
| RPVST+ interoperation | `rpvst-port {enabled \| disabled}` | Lets the port exchange BPDUs with a Rapid PVST+ domain | `disabled` | Same VLANs as the RPVST+ domain |

The options and defaults are from the FortiOS 7.6.0 CLI Reference
(`config switch-controller managed-switch`, `config ports`); the behavior and
prerequisites are from the FortiLink Guide 7.6.7 (pp. 132–141) and the
FortiSwitchOS 7.6.7 Administration Guide (pp. 161–162, 262–270). Four details
are easy to get wrong:

- **Edge-port default.** The FortiOS 7.6.0 reference gives `enable` for managed
  ports, and the guide's example tables show `Edge YES` on every port
  (pp. 136–138). For standalone mode the FortiSwitchOS 7.6.7 CLI Reference gives
  `disable`, while its Administration Guide says STP and edge port are enabled on
  all ports (p. 268). Read your own ports instead of assuming.
- **BPDU guard timer name.** The FortiLink Guide prints `set stp-bpdu-guard-time`
  (p. 139); the FortiOS 7.6.0 CLI Reference names the option
  `stp-bpdu-guard-timeout` (0–120 minutes, default 5). This chapter uses the
  reference's name; type `?` if your build disagrees.
- **Loop guard is not STP loop protection.** Loop guard (`loop-guard`) sends its
  own probe packets and shuts a port that hears them back. **STP loop
  protection** (`stp-loop-protection`, a FortiSwitchOS interface option) keeps an
  alternate or backup port blocking even if it stops receiving BPDUs, for
  example after a one-way link failure; Fortinet recommends it on all
  non-designated ports (Administration Guide, pp. 262–263). The FortiOS 7.6.0
  managed-switch `ports` table has no `stp-loop-protection` option; the switch's
  STP table still shows a `Loop Protection` column. Chapter 11 can set it in
  standalone mode.
- **Loop guard and STP.** The FortiLink Guide says loop guard is designed to work
  in concert with STP, not to replace it (p. 132), and also that loop guard and
  STP should be used separately for loop protection (p. 134). Lab 5.2 reads the
  second sentence as "on a given port, use one or the other" and turns STP off on
  the two loop ports before it tests loop guard.

The FortiSwitchOS Administration Guide adds a MAC-move variant of loop guard
(`loop-guard-mac-move-threshold`, moves per second sustained for six seconds;
p. 162). It is a switch-side option; the FortiOS 7.6.0 managed-switch `ports`
table does not list it.

### Reading the STP table

`diagnose switch-controller switch-info stp <switch> <instance>` on the
controller (FortiLink Guide 7.6.7, pp. 136–138) and `diagnose stp instance list`
on the switch (FortiSwitchOS 7.6.7 CLI Reference, pp. 341–343) print the same
two parts: an instance header and a port table. The guide's example, trimmed:

```text
MST Instance Information, primary-Channel:
Instance ID : 0
Switch Priority : 24576
Root MAC Address : 085b0ef195e4
Root Priority: 24576
Root Pathcost: 0
Regional Root MAC Address : 085b0ef195e4
...
This bridge is the root
Port Speed Cost Priority Role State Edge STP-Status Loop Protection
port1 - 200000000 128 DISABLED DISCARDING YES ENABLED NO
internal 1G 20000 128 DESIGNATED FORWARDING YES DISABLED NO
__FoRtI1LiNk0__ 1G 20000 128 DESIGNATED FORWARDING YES DISABLED NO
```

A port with no link shows speed `-`, the placeholder cost 200000000, role
`DISABLED`, state `DISCARDING`. A 1G port with a link costs 20000. The switch-side
version uses a `Flags` column instead, with the legend `EN` (STP enable), `ED`
(edge), `LP` (loop protection), `RG` (root guard triggered), and `BG` (BPDU
guard triggered) (CLI Reference, p. 343). `diagnose stp mst-config list` prints
the region name, revision, digest, and the instance-to-VLAN map with priorities
(p. 343). Note that the CLI Reference heads that command `diagnose stp
mst-config list` but prints its syntax line as `diagnose snmp mst-config list`,
an evident typo; use the `stp` form.

### STP on the FortiLink side

Three documented facts cover the FortiGate's part:

- **The FortiLink interface has an `stp` option.** `config system interface`
  has `stp` (default `disable`), `stp-edge`, `stp-ha-secondary` (`disable`,
  `enable`, or `priority-adjust`, the default, which lowers the HA secondary's
  priority below the primary's), `stpforward`, and `stpforward-mode`. The
  reference marks `stp`, `stp-edge`, and `stp-ha-secondary` with an asterisk:
  the parameter may not exist on some models (FortiOS 7.6.0 CLI Reference).
- **One topology uses it.** For HA FortiGates whose FortiLink interface is a
  **hardware switch**, with each FortiSwitch on one port of it and an ISL between
  the switches for redundancy, the guide sets `set stp enable` on the FortiLink
  hardware-switch interface. LLDP transmission must be enabled first; STP and STP
  forwarding are supported on a FortiLink hardware switch, a software switch is
  not supported, and if the FortiGate model does not support aggregate interfaces
  it must be made the **CIST root**: give it the lowest STP priority with
  `set switch-priority` under `config system stp`, and put each switch in a
  different region with `set revision` under the switch's `config stp-settings`
  (FortiLink Guide 7.6.7, p. 61).
- **`config system stp` is a hardware feature.** The FortiOS 7.6.0 CLI Reference
  lists `config system stp` (`switch-priority`, `hello-time`, `forward-delay`,
  `max-age`, `max-hops`) for hardware models that include the FortiGate 40F and
  60F, and says it is **not available for FortiGate-VM64**. So C1 can read it; C2
  and C3 cannot.

Two more notes from the guide: in FortiLink over a Layer 3 network with DHCP
discovery, from FortiOS 7.4.1 with FortiSwitchOS 7.4.1, the top FortiSwitch (the
one with the `_FlinkDhcpDisc_` trunk) automatically takes STP priority 24576
instead of 32768 (p. 64); and in a Layer 3 topology with a Layer 2 loop, STP must
be enabled on the FortiLink Layer 3 trunk (p. 67).

### Interoperating with RPVST+

From FortiOS 6.4.2, managed switches interoperate with a network running Rapid
PVST+, so an existing RPVST+ network can keep its configuration and add the
FortiSwitch units as an extended region (FortiLink Guide 7.6.7, pp. 140–141).
Interoperation is off by default and is turned on per port with `rpvst-port`.
The boundary FortiSwitch behaves in one of two ways:

| Where the CIST root is | What the boundary FortiSwitch does | Rule the RPVST+ side must follow |
| --- | --- | --- |
| Inside the MSTP region | Copies the instance 0 information into one BPDU per VLAN and sends them to the RPVST+ domain | RPVST+ VLANs other than VLAN 1 must have bridge priorities **worse** (numerically greater) than the CIST root's |
| Inside the RPVST+ domain | Processes only the VLAN 1 BPDUs; the BPDUs of VLANs 2 and up are used only for consistency checks | The RPVST+ root priority of VLANs other than VLAN 1 must be **better** (numerically lower) than VLAN 1's |

The FortiSwitch must carry the same VLANs as the RPVST+ domain, and the number
of VLANs it supports (native VLANs included) comes from the feature matrix
(p. 141): 32 for the 1xxE/1xxF column and 64 for the 200 Series in 7.6.7. On the
switch, `diagnose stp rapid-pvst-port list [<port_name>]` shows the port status
and, for a port in the `IC` (inconsistent) state, whether the VLAN priorities are
inconsistent, the VLAN configuration does not match, or both (FortiSwitchOS
7.6.7 CLI Reference, p. 344).

### Model support for this chapter

From the FortiSwitchOS 7.6.7 feature matrix (`temp/nse5fsw/fm767.txt`, the
position-based read); chain = standalone and managed, check = standalone only,
dash = not supported:

| Feature | 1xxE/1xxF (S1 FS-108F, S2 FS-124F) | 200 Series (S3) | Note |
| --- | --- | --- | --- |
| MSTP instances | 0–31 | 0–31 | Larger models 0–63 |
| STP root guard | Chain | Chain | |
| STP BPDU guard | Chain | Chain | |
| Loop guard | Chain | Chain | |
| Rapid PVST interoperation | Chain | Chain | |
| VLANs supported by RPVST+ | 32 | 64 | |
| Storm control, per-port storm control | Chain | Chain | |
| Storm-control monitoring | Check | Check | Note 21: no `storm-control-high-rate` or `storm-control-rate-filter` on FS-1xxE, FS-1xxF, FS-110G-FPOE, FS-124G |
| STP supported in MCLAGs | Dash | Chain | Chapter 06 |

Every feature this chapter configures is available in managed mode on all three
switch options.

## Design Considerations

### Make the loop safe before you make it

A Layer 2 loop with nothing to stop it floods every broadcast and unknown
frame around the loop until the link saturates, and every switch in the VLAN
(and the FortiGate interface for that VLAN, up the FortiLink link) receives the
flood. Lab 5.2 creates a loop on purpose, so it builds four layers of safety
first:

| Layer | What it is | Why |
| --- | --- | --- |
| Isolation | The lab switch is cabled only to the controller's FortiLink port and the endpoints; its management port stays unplugged until Chapter 11; on C2 and C3 FortiLink uses the dedicated NIC, never the Nexus (Chapter 01) | A loop cannot reach any other switch |
| Containment | `port5` and `port6` get native VLAN `fsw-guest`, a lab VLAN with no hosts and no DHCP | A flood stays out of the endpoints' VLANs and the default VLAN |
| Rate cap | A storm-control policy, `storm-loop-174`, on `port5` and `port6`: broadcast, unknown unicast, and unknown multicast capped at 500 packets per second | Even a loop that nothing detects carries a bounded flood |
| Recovery | The patch cable itself, a console session to the switch, and the reset commands below | Unplugging the cable ends any loop at once |

The storm-control policy is the one form of storm control this chapter uses; the
global and per-switch storm-control settings, and storm control as a feature,
are Lab 8.3's subject. `burst-size-level` is FortiOS 7.6.4 and later, so it is
not used (FGT-1 runs 7.6.2).

**Recovery, in order.** (1) Unplug the cable from `port6`. (2) If a port was shut
by BPDU guard or loop guard, wait for its timeout (two minutes in this lab), or
reset it: on the switch, `execute bpdu-guard reset port<N>` or `execute
loop-guard reset <port>` (FortiSwitchOS 7.6.7 CLI Reference, pp. 414, 428); from
the controller, `execute switch-controller switch-action bpdu-guard reset
<switch> <port>` or `... loop-guard reset <switch> <port>` (FortiOS 8.0.1 CLI
Reference, cross-check; check with `?` on 7.6). (3) If the controller loses the
switch, use the console: `config switch physical-port`, `edit port6`, `set status
down` takes the port down locally (FortiSwitchOS 7.6.7 CLI Reference). A change
made on a managed switch's own CLI is not known to the controller and can be
overwritten at the next synchronization, so put the same change on the
controller as soon as it is reachable again, then fix the cause.

### Which VLANs go in which instance

MSTP pays off when two switches can share the load: VLANs in one instance block
one uplink, VLANs in another block the other. On one switch there is nothing to
share, so the lab maps the four `FSW-LAN` VLANs to instance 1 to learn the
mechanics and to give Chapter 06 a ready map. Two constraints shape that choice:

- **802.1X and dynamic VLANs.** The FortiSwitchOS Administration Guide advises,
  for 802.1X ports, either disabling STP on them or making sure their STP
  instances belong to the dynamic, guest, and auth-fail VLANs; otherwise
  connectivity fails after the port is moved to one of those VLANs (p. 247).
  Keeping `fsw-users` and `fsw-guest`, the user and guest/auth-fail VLANs of
  Chapter 07, in the **same** instance satisfies that.
- **`fsw-tenant` stays in instance 0.** Chapter 10 decides how the tenant VDOM
  uses VLAN 1745, and an `stp-instance` that refers to the interface would be one
  more reference to remove.

The controller's `vlan-range` takes **VLAN interface names** (FortiOS 7.6.0 CLI
Reference, `config switch-controller stp-instance`); the switch-side
`config switch stp instance` takes VLAN IDs and ranges. The FortiLink Guide
prints the controller command as `config vlan-range <names>` (p. 135); the
reference's `set vlan-range` is the form this chapter uses.

Every switch in a region needs the same name, revision, and map. The global
`stp-settings` and `stp-instance` apply to all managed switches, so when
Chapter 06 adds `FSW-B` on S3 it joins the same region. The per-switch priority
set in Lab 5.1 (16384 for instance 1 on `FSW-A`) makes `FSW-A` the instance 1
root when that happens.

### Where to use each guard

| Port type | Edge port | BPDU guard | Root guard | Loop guard |
| --- | --- | --- | --- | --- |
| Host port (endpoint, phone, printer) | Enable | Enable | Optional (BPDU guard already shuts the port) | Optional, if an unmanaged switch might be added |
| Port to a downstream switch you manage | Disable | Disable | Enable, so the downstream switch cannot become root | — |
| Uplink toward the root | Disable | Disable | **Never** (the guide: do not enable root guard on the root port) | — |
| FortiLink and ISL trunks | Leave as FortiLink sets them | Leave | Leave | Leave |

The guide's rule for root guard is "enable root guard on all ports that should
not be root bridges" and never on the root port (p. 138). In this volume's lab,
the host ports `port1` and `port2` end the chapter with BPDU guard enabled.

### What to keep after this chapter

| Object | Kept | Why |
| --- | --- | --- |
| Global `stp-settings`: name `lab-174`, revision 1, default timers | Yes | Chapter 06's `FSW-B` joins this region |
| `stp-instance` 1 = `fsw-users`, `fsw-voice`, `fsw-iot`, `fsw-guest` | Yes | Ready for Chapter 06; one instance for Chapter 07's VLANs |
| Instance 1 priority 16384 on `<SWITCH_SN>` (`FSW-A`) | Yes | `FSW-A` is the instance 1 root on S3 |
| `port1`, `port2`: BPDU guard enabled, timeout 5 (default); edge port and STP at defaults | Yes | Host-port protection for Chapters 06–12 |
| `port5`, `port6`: native VLAN back to `<DEFAULT_VLAN>`, STP, edge port, guards, and storm control at defaults | Yes (defaults) | Lab 8.3 and Chapter 12 start from defaults |
| Loop cable | Connected to `port5` only, other end loose | Ready for later labs without a standing loop |
| Storm-control policy `storm-loop-174` | No | Lab 5.2 deletes it |
| Root guard on `port1`, RPVST+ on `port6` | No | Test settings only |

## Implementation and Automation

The labs are the implementation. Three habits help with spanning tree work.

**Read both trees.** The controller shows what it configured and what the
switch reports; the switch shows its own view with flags:

```text
FGT # diagnose switch-controller switch-info stp <SWITCH_SN> 0
FSW # diagnose stp instance list 0
FSW # diagnose stp mst-config list
```

**Keep a ping running.** Before a change that can reconverge the tree, start a
continuous ping from endpoint A to its gateway in a second window; any gap in it
is the user's view of the change:

```bash
# endpoint A
ping -O 10.174.41.1
```

**Watch the counters during a loop.** A loop shows as broadcast counters that
climb far faster than the lab's traffic can explain:

```text
FGT # diagnose switch-controller switch-info port-stats <SWITCH_SN> port6
FSW # diagnose switch physical-ports summary port6
```

The FortiOS configuration commands in this chapter were checked against the
FortiOS 7.6.0 CLI Reference; `execute`, `diagnose`, and `get` commands against
the FortiLink Guide 7.6.7, or the FortiOS 8.0.1 CLI Reference as a cross-check
where the guide prints no syntax line (each case is marked). Switch commands were
checked against the FortiSwitchOS 7.6.7 CLI Reference. The Linux commands use
`iproute2` (`ip-link(8)`) and `tcpdump(8)`.

## Validation and Troubleshooting

| Symptom | Likely cause | Check |
| --- | --- | --- |
| A port that should forward shows `DISCARDING` with role `BACKUP` or `ALTERNATE` | STP is blocking a redundant path (intended in Lab 5.2) | `diagnose switch-controller switch-info stp <SWITCH_SN> 0`; follow the cable |
| A host port goes down a few seconds after something is plugged in | BPDU guard received a BPDU (a switch, a bridge, or a looped cable on that port) | `diagnose switch-controller switch-info bpdu-guard-status <SWITCH_SN>`; on the switch `diagnose bpdu-guard display status` |
| A port goes out of service and the BPDU guard table shows nothing | Loop guard detected a loop | `diagnose loop-guard status` on the switch; `diagnose switch-controller switch-info loop-guard <SWITCH_SN>` (FortiOS 8.0.1 cross-check) |
| The port comes back, then goes down again | The cause is still connected; the timeout only re-enables the port | Unplug or fix first, then reset |
| `RG` in the switch's flags; the endpoint's bridge is not root | Root guard dropped superior BPDUs (intended in Lab 5.2) | `diagnose stp instance list 0 port1` on the switch |
| Two switches each claim to be root of instance 1 | They are in different regions: name, revision, or map differ | `diagnose stp mst-config list` on each; compare the digest |
| Broadcast counters climb by thousands per second | A loop that nothing is blocking | Unplug the loop cable at once; then find which protection was off |
| The controller loses the switch during a loop test | The flood reached the FortiLink link | Unplug the loop cable; console to the switch; see "Make the loop safe" |
| `get system stp` fails on the controller | FortiGate-VM: `config system stp` is not available for FortiGate-VM64 | Intended on C2 and C3 |
| An 802.1X client loses connectivity after a dynamic VLAN assignment (Chapter 07) | The assigned VLAN is in a different STP instance from the port's other VLANs | `diagnose stp vlan list <VLAN_ID>` on the switch; keep those VLANs in one instance |

## Security and Best Practices

- **Never create a loop outside an isolated lab.** Lab 5.2's loop is safe
  because the switch is connected to nothing but its controller and two
  endpoints. Do not repeat it on a switch with any other uplink, and never on a
  production network.
- **Enable BPDU guard on host ports.** A user who plugs in a small switch or a
  bridge, or loops a cable between two wall jacks, takes one port down instead of
  the VLAN.
- **Pick a timeout you will notice.** A long or zero BPDU guard timeout keeps an
  offending port down until someone resets it, which is safer but needs a
  process; the default is 5 minutes.
- **Fence the root with root guard.** On every port toward a switch that must
  never be root, enable root guard; never on the root port.
- **Set bridge priorities deliberately.** Choose which switch is root for each
  instance with a priority, rather than letting the lowest MAC address decide.
- **Keep storm control as a backstop.** Storm control does not prevent a loop,
  but it limits the damage when every other protection is off; Lab 8.3 covers it
  fully.
- **Do not turn STP off to fix a symptom.** If STP blocks a port you expected to
  forward, find the redundant path; disabling STP on a port is for a reason, such
  as loop guard on that port or an 802.1X design that requires it.

## References and Knowledge Checks

**References**

- [Fortinet, *FortiLink Guide (FortiOS 7.6.7)*](https://docs.fortinet.com/document/fortiswitch/7.6.7/fortilink-guide)
  — HA FortiGates with a hardware-switch FortiLink interface and STP (p. 61),
  STP priority in FortiLink over Layer 3 (p. 64), Layer 2 loops in Layer 3
  topologies (p. 67), DHCP blocking, STP, loop guard, BPDU guard, and root guard
  on managed ports (p. 132), edge ports (p. 133), loop guard and STP settings
  (pp. 134–136), STP on ports and `diagnose switch-controller switch-info stp`
  (pp. 136–138), root guard (p. 138), BPDU guard and `bpdu-guard-status`
  (pp. 139–140), RPVST+ interoperation and `switch-info rpvst` (pp. 140–141),
  storm control (pp. 144–146), port statistics (pp. 335–338).
- [Fortinet, *FortiSwitchOS 7.6.7 Administration Guide (Standalone Mode)*](https://docs.fortinet.com/document/fortiswitch/7.6.7/administration-guide)
  — loop guard and LGDP (pp. 161–163), 802.1X and STP instances (p. 247), STP,
  MSTP terms, port roles, loop protection, root guard, BPDU guard, edge ports
  (pp. 261–271).
- [Fortinet, *FortiSwitchOS 7.6.7 CLI Reference*](https://docs.fortinet.com/document/fortiswitch/7.6.7/fortiswitchos-cli-reference)
  — `config switch global` (`auto-stp-priority`, `auto-stp-cost`, p. 114),
  `config switch interface` (p. 126), `config switch stp instance` and
  `settings` (pp. 177–178), `diagnose bpdu-guard display status` (p. 301),
  `diagnose loop-guard status` (pp. 336–337), `diagnose stp instance list`,
  `mst-config list`, `rapid-pvst-port`, and `vlan list` (pp. 341–345),
  `execute bpdu-guard reset` (p. 414), `execute loop-guard reset` (p. 428),
  `get switch stp instance` and `settings` (pp. 510–511),
  `config switch physical-port`.
- [Fortinet, FortiOS 7.6 documentation](https://docs.fortinet.com/product/fortigate/7.6)
  — the FortiOS 7.6.0 CLI Reference: `config switch-controller stp-settings`,
  `config switch-controller stp-instance`,
  `config switch-controller storm-control-policy`,
  `config switch-controller managed-switch` (`ports`, `stp-instance`,
  `stp-settings`), `config system interface` (`stp`, `stp-edge`,
  `stp-ha-secondary`), `config system stp` (model availability).
- FortiOS 8.0.1 CLI Reference (cross-check only) — `diagnose
  switch-controller switch-info loop-guard`; `execute switch-controller
  switch-action bpdu-guard reset` and `loop-guard reset`.
- FortiSwitchOS 7.6.7 feature matrix (`temp/fsw/FSW-7.6.7-Feature-Matrix.pdf`)
  — MSTP instances, root guard, BPDU guard, loop guard, Rapid PVST
  interoperation and its VLAN counts, storm control (note 21), STP in MCLAGs.
- [`ip-link(8)`](https://man7.org/linux/man-pages/man8/ip-link.8.html) — Linux
  bridge options `stp_state` and `priority`;
  [`tcpdump(8)`](https://www.tcpdump.org/manpages/tcpdump.1.html) and
  [`pcap-filter(7)`](https://www.tcpdump.org/manpages/pcap-filter.7.html) — the
  `stp` filter.

**Knowledge checks**

1. On a single managed FortiSwitch, which bridge is the root of instance 0, and
   why is it not the FortiGate?
2. `port5` and `port6` of one switch are joined by a cable with STP enabled.
   Which roles do the two ports take, and which one forwards?
3. Name the two prerequisites for BPDU guard on a managed port, and what a
   timeout of 0 means.
4. What is the difference between Fortinet loop guard and STP loop protection,
   and which one can the FortiOS 7.6.0 managed-switch `ports` table set?
5. Two FortiSwitch units have the same instance map but different revisions.
   What happens to their spanning tree?
6. Why can C1 read `config system stp` but C2 and C3 cannot, and what is it for
   in a FortiLink design?
7. The CIST root is inside the MSTP region and connects to an RPVST+ domain.
   What must be true of the RPVST+ priorities of VLANs other than VLAN 1?

## Hands-On Lab

**Shared prerequisites.** Chapter 04 complete: `<SWITCH_SN>` `Authorized/Up`
at `10.255.1.2` with profile `fsw-174-prof` (on S3, `FSW-A` only); the lab VLANs
1741–1745 (or the C2 NO-GO recorded in Lab 4.1); `port1` native `fsw-users`
(endpoint A), `port2` native `fsw-iot` (endpoint B, `10.174.43.20/24`); `port3`,
`port4`, `port5`, `port6` at defaults; `<DEFAULT_VLAN>` recorded in Lab 4.2. A
patch cable for `port5`↔`port6`, **not connected yet**. A console cable to the
switch, with a session open during Lab 5.2. The switch's management port
unplugged, and no cable from the switch to anything but the controller and the
endpoints. Track 2: the Lab 2.2 pre-provisioning outcome, and the stand-in entry
`S248EPTF18000000` if that outcome allowed it. **Cost:** one patch cable.

As in earlier chapters, `FGT #` is the controller on any option, and blocks
written for `port3` apply to C3 with `port4` and to C1 with `<FL_PORT>` (the
factory `fortilink` interface if you used it). `<SWITCH_SN>` is your switch's
serial number; on Track 2 it is `S248EPTF18000000`. `<IFACE>` is endpoint A's
wired interface. After a C2 NO-GO in Lab 4.1, use `video` wherever these labs
name a lab VLAN (Lab 5.1's instance map and Lab 5.2's loop VLAN). Before the first
change, back up the controller:

```text
FGT # execute backup config tftp fgt-pre-5-1-174.conf 10.30.99.50
```

### Lab 5.1 — MSTP settings and instances from the FortiGate

**Objective:** Read the managed switch's default spanning tree, set the region
name and revision, map the four `FSW-LAN` VLANs to MSTP instance 1, give the
switch a priority for that instance, and confirm the result from the controller
and from the switch.

**Platform notes:** Hands-on on C1, C2, and C3 with S1, S2, or S3 (on S3,
`FSW-A`; `FSW-B` joins the region in Chapter 06). Instance 1 is within every
model's range (0–31 in the 7.6.7 feature matrix for all three options). After a
C2 NO-GO in Lab 4.1, map `video` instead of the lab VLANs. Track 2: steps 2 and
3 are controller configuration and run live; step 4 only on the stand-in entry,
if it exists; the switch-side steps are read-and-predict.

**Track 1:**

1. Read the defaults from both sides:

   ```text
   FGT # show switch-controller stp-settings
   FGT # show switch-controller stp-instance
   FGT # diagnose switch-controller switch-info stp <SWITCH_SN> 0
   FSW # diagnose stp mst-config list
   FSW # get switch stp settings
   ```

   Record the region name, revision, and digest, and any instances already
   listed. Before you read the STP table, predict three things: which bridge is
   root, what `port1` shows, and what `port5` shows. **Answer:** the switch
   itself (`This bridge is the root`), because the FortiLink link does not run
   STP and no other bridge sends it BPDUs (FortiLink Guide 7.6.7, p. 136);
   `port1` has endpoint A, so `DESIGNATED`, `FORWARDING`, edge `YES`; `port5` has
   no link, so speed `-`, cost 200000000, `DISABLED`, `DISCARDING`
   (pp. 136–137). Record the `Switch Priority` you see: the guide's managed
   example shows 24576 (p. 136) and the switch reference's standalone default
   is 32768 (FortiSwitchOS 7.6.7 CLI Reference, p. 342); the documentation does
   not say which a managed switch starts with. Record the name of the FortiLink
   trunk row and its `STP-Status`.

2. Start a continuous ping from endpoint A to `10.174.41.1` in a second window.
   Set the region name and revision. The timers are left at their defaults
   (hello 2, forward 15, max-age 20, max-hops 20):

   ```text
   FGT # config switch-controller stp-settings
   set name "lab-174"
   set revision 1
   end
   ```

3. Map the four `FSW-LAN` VLANs to instance 1. The controller takes VLAN
   interface names:

   ```text
   FGT # config switch-controller stp-instance
   edit "1"
   set vlan-range "fsw-users" "fsw-voice" "fsw-iot" "fsw-guest"
   next
   end
   ```

4. Give this switch priority 16384 for instance 1 (the value the guide's example
   uses, p. 135):

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config stp-instance
   edit "1"
   set priority 16384
   next
   end
   next
   end
   ```

5. Read the result. Stop the ping and record any lost replies:

   ```text
   FGT # show switch-controller stp-instance
   FGT # diagnose switch-controller switch-info stp <SWITCH_SN> 1
   FSW # diagnose stp mst-config list
   FSW # get switch stp instance
   ```

   Predict the `diagnose stp mst-config list` output before you read it.
   **Answer:** name `lab-174`, revision 1, a new digest (the map changed),
   instance 0 at the priority you recorded in step 1, and instance 1 mapped to
   VLANs 1741–1744 with priority 16384 (the shape of the CLI Reference example,
   p. 343).

6. Check which instance a VLAN belongs to:

   ```text
   FSW # diagnose stp vlan list 1741
   FSW # diagnose stp vlan list 1745
   ```

   Predict the `Instance ID` of each. **Answer:** 1 for VLAN 1741 (mapped in
   step 3) and 0 for VLAN 1745 (`fsw-tenant` is not mapped, so it stays in the
   IST).

**Track 2:** Run step 1's two `show` commands, then steps 2 and 3, and check them
with `show switch-controller stp-settings` and `show switch-controller
stp-instance`. If the stand-in entry exists (Lab 2.2's second or third outcome),
run step 4 against `S248EPTF18000000` and record whether FortiOS accepts a
per-switch instance priority on a switch that has never joined. Skip the
switch-side commands.

**Track 2: read-and-predict.**

1. The FortiSwitchOS 7.6.7 CLI Reference (p. 343) prints:

   ```text
   S524DF4K15000024 # diagnose stp mst-config list
   MST Configuration Identification Information
   Unit: primary
   MST Configuration Name: region1
   MST Configuration Revision: 1
   MST Configuration Digest: ac36177f50283cd4b83821d8ab26de62
   Instance ID Mapped VLANs Priority
   ____________________________________________________
   0 32768
   1 8192
   ```

   A second switch shows the same name and revision but a different digest.
   Predict whether the two are in one region. **Answer:** no. A region needs the
   same name, revision, **and** VLAN-to-instance map; a different digest means a
   different map, so each switch is its own region and they meet at a boundary
   (Administration Guide, p. 261).
2. In that example, which switch is root of instance 1 if the other switch, in
   the same region, has instance 1 priority 32768? **Answer:** this one; 8192 is
   lower, and the lowest bridge ID wins. Instance 0 is decided separately, by
   the instance 0 priorities (both 32768 here), then the lower MAC address.
3. Your controller's step 3 lists `"fsw-users" "fsw-voice" "fsw-iot"
   "fsw-guest"`. What does the switch receive? **Answer:** the VLAN IDs 1741–1744;
   the controller refers to VLANs by interface name, and the switch's own
   `config switch stp instance` uses IDs and ranges (FortiSwitchOS 7.6.7 CLI
   Reference, `config switch stp instance`).

**Expected result:** The region is `lab-174` revision 1; instance 1 holds
VLANs 1741–1744 (or `video` after a C2 NO-GO) with priority 16384 on
`<SWITCH_SN>`, and the switch is root of instances 0 and 1; VLAN 1745 is in
instance 0. The ping gap, if any, is recorded. Track 2: the global objects exist,
the stand-in result is recorded, and the predictions are answered.

**Negative test:** Set a priority that is not a multiple of 4096:

```text
FGT # config switch-controller managed-switch
edit <SWITCH_SN>
config stp-instance
edit "1"
set priority 1000
next
end
next
end
```

FortiOS refuses it: `priority` is an option with the fixed values 0, 4096, …,
61440 (FortiOS 7.6.0 CLI Reference). Record the message. Track 2: run it against
the stand-in entry if it exists; otherwise prediction 2 is the negative test.

**Rollback:** Normally keep everything for Labs 5.2 and 5.3 and later chapters.
To remove it: under the switch's `config stp-instance`, `delete "1"`; under
`config switch-controller stp-instance`, `delete "1"`; and under
`config switch-controller stp-settings`, set `name` and `revision` back to the
values recorded in step 1; or restore `fgt-pre-5-1-174.conf`.

**Lab verified by:** *pending*

### Lab 5.2 — Edge ports, BPDU guard, root guard, and loop guard on a real loop

**Objective:** Build the loop safety net, create a loop with the `port5`↔`port6`
cable and watch STP block it, then let BPDU guard shut the loop, then turn STP
off on the loop ports and let loop guard find it; use a Linux bridge on endpoint
A to trigger root guard; leave the host ports protected by BPDU guard.

**Platform notes:** Hands-on on C1, C2, and C3 with S1, S2, or S3 (on S3,
`FSW-A`); `port5` and `port6` exist on every option. All four features are chain
(managed and standalone) in the 1xxE/1xxF and 200 Series columns. After a C2
NO-GO in Lab 4.1, use `video` as the loop VLAN in Part A. Track 2: build the
storm-control policy live; build the port settings on the stand-in entry only if
Lab 2.2's third outcome (ports accepted); otherwise read-and-predict.

> **Warning: this lab creates a Layer 2 loop on purpose.** Do it only on the
> isolated lab switch, connected to nothing but its controller's FortiLink port
> and the two endpoints: management port unplugged, no cable to the Nexus or any
> other switch. Finish Part A (the storm-control policy and the loop VLAN)
> before the cable goes in, keep the console session open, and keep a hand on
> the cable. If the broadcast counters climb by thousands per second, endpoint A
> loses its gateway, or the controller loses the switch, **unplug the cable from
> `port6` first** and then follow the recovery steps in Design Considerations.

**Track 1, Part A — the safety net and the starting state:**

1. Read `port5` and `port6`. Record each port's `vlan`, `edge-port`,
   `stp-state`, `stp-bpdu-guard`, `stp-root-guard`, `loop-guard`, and
   `storm-control-policy` (a line that `show` omits is at its default):

   ```text
   FGT # show switch-controller managed-switch <SWITCH_SN>
   FGT # diagnose switch-controller switch-info bpdu-guard-status <SWITCH_SN>
   FSW # diagnose loop-guard status
   ```

   Predict the defaults. **Answer:** STP `enabled`, edge port `enable`, BPDU
   guard, root guard, and loop guard `disabled` (FortiOS 7.6.0 CLI Reference;
   FortiLink Guide 7.6.7, p. 132), and native VLAN `<DEFAULT_VLAN>`.

2. Create the storm-control policy (FortiOS 7.6.0 CLI Reference; the guide's
   example form, p. 146):

   ```text
   FGT # config switch-controller storm-control-policy
   edit "storm-loop-174"
   set description "Lab 5.2 loop safety net"
   set storm-control-mode override
   set rate 500
   set broadcast enable
   set unknown-unicast enable
   set unknown-multicast enable
   next
   end
   ```

3. Put `port5` and `port6` in the empty `fsw-guest` VLAN and apply the policy.
   `set vlan` changes only the native VLAN; the allowed list (with `quarantine`)
   is untouched:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port5"
   set description "Lab 5.2 loop A"
   set vlan "fsw-guest"
   set storm-control-policy "storm-loop-174"
   next
   edit "port6"
   set description "Lab 5.2 loop B"
   set vlan "fsw-guest"
   set storm-control-policy "storm-loop-174"
   next
   end
   next
   end
   ```

   Check on the switch that both ports show VLAN 1744:

   ```text
   FSW # diagnose switch physical-ports summary port5
   FSW # diagnose switch physical-ports summary port6
   ```

**Track 1, Part B — STP blocks the loop:**

4. With STP on (the default) and the guards off, plug the cable into `port5`,
   then into `port6`. Wait 30 seconds and read the tree:

   ```text
   FGT # diagnose switch-controller switch-info stp <SWITCH_SN> 0
   FSW # diagnose stp instance list 0 port5
   FSW # diagnose stp instance list 0 port6
   ```

   Predict the roles and states before you read. **Answer:** one port
   `DESIGNATED` and `FORWARDING`, the other in the **backup** role and
   `DISCARDING`: two ports of one switch joined together give one designated port
   and one backup (Administration Guide, p. 262). The BPDUs on the two ports
   carry the same root, cost, and bridge ID, so the tie is broken by the sending
   port's identifier, normally in favor of the lower-numbered port: expect
   `port5` designated and `port6` backup. The guide's sample output shows no
   backup row, so record the exact role string your switch prints, and whether
   the `Edge` column changes for the two ports now that they receive BPDUs.

5. Check that nothing is flooding. Run the counters twice, ten seconds apart:

   ```text
   FGT # diagnose switch-controller switch-info port-stats <SWITCH_SN> port6
   ```

   The broadcast and multicast counters should barely move; endpoint A's ping
   (if still running) is unaffected.

**Track 1, Part C — BPDU guard shuts the loop:**

6. Unplug the cable from `port6`. Enable BPDU guard on both loop ports with a
   two-minute timeout. Edge port and STP, its prerequisites, are already on:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port5"
   set edge-port enable
   set stp-state enabled
   set stp-bpdu-guard enabled
   set stp-bpdu-guard-timeout 2
   next
   edit "port6"
   set edge-port enable
   set stp-state enabled
   set stp-bpdu-guard enabled
   set stp-bpdu-guard-timeout 2
   next
   end
   next
   end
   ```

7. Plug the cable into `port6` again, wait ten seconds, and read both status
   tables:

   ```text
   FGT # diagnose switch-controller switch-info bpdu-guard-status <SWITCH_SN>
   FSW # diagnose bpdu-guard display status
   FSW # diagnose switch physical-ports summary port6
   ```

   Predict what happens. **Answer:** the first BPDU that arrives on an edge port
   with BPDU guard takes that port down for the timeout (FortiLink Guide 7.6.7,
   p. 139). Both ports send BPDUs, so one or both trip; when one port goes down,
   the cable's link drops on the other too. In the status table, the tripped
   port's `Count` rises from 0 and `Last-Event` gets a time. The documentation
   prints only untriggered rows (`Status` `-`), so record the `Status` value a
   tripped port shows, and record which port tripped. The switch-side `Flags`
   column in `diagnose stp instance list` shows `BG` for a port whose BPDU guard
   has triggered (CLI Reference, p. 343).

8. Recover. Unplug the cable from `port6` first; a reset with the cable still in
   would trip the port again. Then either wait two minutes, or reset the port
   from the switch, or from the controller (FortiOS 8.0.1 CLI Reference,
   cross-check; check with `?` on your build):

   ```text
   FSW # execute bpdu-guard reset port6
   FGT # execute switch-controller switch-action bpdu-guard reset <SWITCH_SN> port6
   ```

   Read `bpdu-guard-status` again and confirm the port is no longer shown as
   triggered.

**Track 1, Part D — loop guard finds the loop with STP off:**

9. With the cable out of `port6`, turn BPDU guard and STP off on both loop ports
   and turn loop guard on, with a two-minute timeout. The storm-control policy
   stays on:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port5"
   set stp-bpdu-guard disabled
   set stp-state disabled
   set loop-guard enabled
   set loop-guard-timeout 2
   next
   edit "port6"
   set stp-bpdu-guard disabled
   set stp-state disabled
   set loop-guard enabled
   set loop-guard-timeout 2
   next
   end
   next
   end
   FSW # diagnose loop-guard status
   ```

   Both ports should now read `enabled` with timeout 2.

10. **This is the step with no STP on the loop.** Read the counters once, plug
    the cable into `port6`, and read the loop guard status and the counters
    every few seconds for up to 30 seconds. The controller command is from the
    FortiOS 8.0.1 CLI Reference (cross-check):

    ```text
    FSW # diagnose loop-guard status
    FGT # diagnose switch-controller switch-info loop-guard <SWITCH_SN>
    FGT # diagnose switch-controller switch-info port-stats <SWITCH_SN> port6
    ```

    Predict the result. **Answer:** the documentation says each loop guard port
    periodically broadcasts LGDP packets and takes itself out of service when a
    broadcast comes back to the sending port, and that the system logs
    `Loop Guard: loop detected on <port_name>. Shutting down <port_name>`
    (Administration Guide, p. 162); the status table's `Count` and `Last-Event`
    then change for that port. It does not describe a loop through two ports of
    the **same** switch, so record what happens: which port, if any, was shut,
    and how long it took. **If no port is shut within 30 seconds, or the
    broadcast counters climb by thousands per second, unplug the cable at once**
    and record "not detected"; the storm-control policy has been capping the
    flood at 500 packets per second per type in the meantime.

11. Recover: unplug the cable from `port6`; wait two minutes, or reset the port
    from the switch, or from the controller (FortiOS 8.0.1 CLI Reference,
    cross-check):

    ```text
    FSW # execute loop-guard reset port6
    FGT # execute switch-controller switch-action loop-guard reset <SWITCH_SN> port6
    ```

12. Return `port5` and `port6` to the STP defaults, so no port in the loop is
    unprotected:

    ```text
    FGT # config switch-controller managed-switch
    edit <SWITCH_SN>
    config ports
    edit "port5"
    set loop-guard disabled
    set stp-state enabled
    next
    edit "port6"
    set loop-guard disabled
    set stp-state enabled
    next
    end
    next
    end
    ```

**Track 1, Part E — root guard and a rogue root:**

13. Turn endpoint A into a bridge that claims to be root. A Linux bridge with
    kernel STP and priority 0 sends 802.1D BPDUs whose bridge ID beats the
    switch's (`ip-link(8)`, bridge options `stp_state` and `priority`). First
    enable root guard on `port1` (STP is on there by default; BPDU guard must
    stay off for this test):

    ```text
    FGT # config switch-controller managed-switch
    edit <SWITCH_SN>
    config ports
    edit "port1"
    set stp-state enabled
    set stp-root-guard enabled
    next
    end
    next
    end
    ```

    ```bash
    # endpoint A (its address on <IFACE> is lost until step 15)
    sudo ip link add br-stp type bridge stp_state 1 priority 0
    sudo ip link set <IFACE> master br-stp
    sudo ip link set br-stp up
    sudo tcpdump -i <IFACE> -c 3 -e stp
    ```

    `tcpdump` should show BPDUs leaving the endpoint every two seconds.

14. Read the switch's view of `port1`:

    ```text
    FGT # diagnose switch-controller switch-info stp <SWITCH_SN> 0
    FSW # diagnose stp instance list 0 port1
    ```

    Predict the root MAC address and `port1`'s flags. **Answer:** the switch is
    still root (`This bridge is the root`), because root guard ignores or drops
    the superior BPDUs that arrive on `port1` (FortiLink Guide 7.6.7, p. 138), and
    the switch-side flags show `RG` (root guard triggered) for `port1`
    (CLI Reference, p. 343). The guide does not say whether the port also stops
    forwarding while it receives superior BPDUs; record the `Role` and `State`
    columns.

15. Remove the bridge from endpoint A and take root guard off `port1`; bounce the
    link so endpoint A renews its lease (Lab 4.2 step 4):

    ```bash
    # endpoint A
    sudo ip link delete br-stp
    sudo ip link set <IFACE> down && sudo ip link set <IFACE> up
    sleep 10; ip -br addr show <IFACE>
    ```

    ```text
    FGT # config switch-controller managed-switch
    edit <SWITCH_SN>
    config ports
    edit "port1"
    set stp-root-guard disabled
    next
    end
    next
    end
    ```

**Track 1, Part F — leave the host ports protected and clean up:**

16. Enable BPDU guard on the two host ports with the default timeout, and return
    `port5` and `port6` to their starting VLAN and storm-control setting (the
    values recorded in step 1; `unset` returns an option to its default):

    ```text
    FGT # config switch-controller managed-switch
    edit <SWITCH_SN>
    config ports
    edit "port1"
    set stp-bpdu-guard enabled
    set stp-bpdu-guard-timeout 5
    next
    edit "port2"
    set stp-bpdu-guard enabled
    set stp-bpdu-guard-timeout 5
    next
    edit "port5"
    unset description
    set vlan <DEFAULT_VLAN>
    unset storm-control-policy
    unset stp-bpdu-guard-timeout
    unset loop-guard-timeout
    next
    edit "port6"
    unset description
    set vlan <DEFAULT_VLAN>
    unset storm-control-policy
    unset stp-bpdu-guard-timeout
    unset loop-guard-timeout
    next
    end
    next
    end
    ```

    Then delete the policy:

    ```text
    FGT # config switch-controller storm-control-policy
    delete "storm-loop-174"
    end
    FGT # diagnose switch-controller switch-info bpdu-guard-status <SWITCH_SN>
    ```

    `port1` and `port2` should read `enabled` with timeout 5. Leave the cable in
    `port5` with its other end loose.

**Track 2:** Run step 2 (the storm-control policy) and step 16's policy deletion
on your controller, and check each with `show switch-controller
storm-control-policy`. If Lab 2.2's third outcome applies, also run steps 3, 6, 9,
12, 13 (the controller block only), 15 (the controller block), and 16 against
`S248EPTF18000000`, and check them with `show switch-controller managed-switch
S248EPTF18000000`. Skip the cable, switch-side, and endpoint steps.

**Track 2: read-and-predict.**

1. The FortiLink Guide (p. 139) prints, after BPDU guard was set on `port1` with
   a 10-minute timer:

   ```text
   FG100D3G15817028 # diagnose switch-controller switch-info bpdu-guard-status S524DF4K15000024
   Managed Switch : S524DF4K15000024 0
   Portname State Status Timeout(m) Count Last-Event
   _________________ _______ _________ ___________ _____ _______________
   port1 enabled - 10 0 -
   port2 disabled - - - -
   ```

   Predict what changes on the `port1` row after a hub with a looped cable is
   plugged into it. **Answer:** a BPDU arrives on an edge port with BPDU guard,
   so the port goes down for 10 minutes: `Count` rises to at least 1,
   `Last-Event` records the time, and `Status` changes from `-` (the guide does
   not print the triggered value). It comes back after 10 minutes, and trips
   again if the loop is still there.
2. A port has `stp-bpdu-guard enabled` but `edge-port disable`. Predict whether
   it is protected. **Answer:** no; BPDU guard requires the port to be an edge
   port and STP to be enabled on it (FortiLink Guide 7.6.7, p. 139).
3. The guide's STP table (p. 137) shows every port with `Loop Protection` `NO`.
   An administrator says "loop guard is off on every port, then". Predict whether
   that follows. **Answer:** no. The `Loop Protection` column is STP loop
   protection (`stp-loop-protection`), which keeps a blocking port blocked
   without BPDUs; loop guard is the separate LGDP feature, shown by `diagnose
   loop-guard status` or the controller's loop-guard command (Administration
   Guide, pp. 161–163, 262–263).
4. Two ports of one switch are joined by a cable, STP is on, no guards. Predict
   the roles. **Answer:** one designated (forwarding), one backup (discarding)
   (Administration Guide, p. 262).

**Expected result:** Track 1: with STP on, the loop was blocked (one port
designated, one backup); with BPDU guard on, one or both loop ports went down and
came back after a reset; with STP off and loop guard on, the result (detected or
not, and how fast) is recorded; root guard kept the switch as root while endpoint
A advertised priority 0, with `RG` shown; `port1` and `port2` end with BPDU guard
enabled; `port5` and `port6` are back at their recorded settings; the policy
`storm-loop-174` is gone. Track 2: the policy was created and deleted, the
stand-in port settings are recorded (if accepted), and the predictions are
answered.

**Negative test:** Part B is the control (STP alone blocks the loop). For the
negative test, show that BPDU guard on a host port is stronger than root guard:
repeat step 13 on endpoint A **without** root guard, now that `port1` has BPDU
guard (step 16). Predict and observe: `port1` goes down within seconds and
`bpdu-guard-status` shows it triggered; endpoint A loses its link. Remove the
bridge (step 15's endpoint block), unplug and replug endpoint A's cable after the
5-minute timeout or reset the port (step 8's commands with `port1`), and check
the lease. Track 2: prediction 2.

**Rollback:** Step 16 is the rollback for the loop ports. To return `port1` and
`port2` to the Chapter 04 state, set `stp-bpdu-guard disabled` on both. If
anything else differs from step 1's record, set it back, or restore
`fgt-pre-5-1-174.conf`. Leave the loop cable unplugged from `port6`.

**Lab verified by:** *pending*

### Lab 5.3 — STP on the FortiLink side, the CIST root, and RPVST+

**Objective:** Show that the FortiLink link does not run STP, read the
FortiGate's own STP options, work out how a FortiGate becomes the CIST root in
the one topology that needs it, and enable and read RPVST+ interoperation on a
managed port.

**Platform notes:** Steps 1, 2, and 4 are hands-on on C1, C2, and C3 with S1, S2,
or S3 (on S3, `FSW-A`). Step 3 differs by controller: on C1 (40F or 60F)
`config system stp` exists and is read; on C2 and C3 (FortiGate-VM) it is not
available, and the step is the negative test. This volume never connects the
lab switch to an RPVST+ network (the Nexus stays out of the FortiLink path, and
Lab 5.2's isolation rule applies) and builds no HA pair with a hardware-switch
FortiLink interface, so the
CIST-root design and the RPVST+ priority rules are read-and-predict on every
option. RPVST+ supports 32 VLANs on S1 and S2 and 64 on S3. Track 2: steps 2 and
3 run live on the controller; step 4 on the stand-in entry only with Lab 2.2's
third outcome; the rest is read-and-predict.

**Track 1:**

1. Find the FortiLink link in the switch's spanning tree:

   ```text
   FGT # diagnose switch-controller switch-info stp <SWITCH_SN> 0
   FSW # diagnose stp instance list 0
   ```

   Predict the `STP-Status` of the FortiLink trunk row (named
   `__FoRtI1LiNk0__` in the guide's example) and of `internal`. **Answer:**
   `DISABLED` on both, with role `DESIGNATED` and state `FORWARDING`
   (FortiLink Guide 7.6.7, pp. 137–138): STP is not supported between a
   FortiGate and a FortiSwitch in FortiLink mode (p. 136). Record the trunk's
   name in your build.

2. Read the STP options of the controller's FortiLink interface. `get` shows
   every field, defaults included:

   ```text
   FGT # get system interface port3 | grep stp
   ```

   Predict the values. **Answer:** `stp` `disable`, `stp-edge` `disable`,
   `stp-ha-secondary` `priority-adjust` (FortiOS 7.6.0 CLI Reference). The
   reference marks these three with an asterisk, "may not exist in some
   models"; record which lines your controller prints. Do not enable `stp` here:
   the guide uses it only for a hardware-switch FortiLink interface in an HA
   design (p. 61).

3. Read the FortiGate's own bridge settings. On C1:

   ```text
   FGT # get system stp
   ```

   Predict the priority. **Answer:** `switch-priority` 32768, the default, with
   `hello-time` 2, `forward-delay` 15, `max-age` 20, `max-hops` 20 (FortiOS 7.6.0
   CLI Reference, `config system stp`). On C2 and C3, run the same command and
   record the error: the reference says `config system stp` is not available
   for FortiGate-VM64.

4. Enable RPVST+ interoperation on `port6` (the loop cable is unplugged from it),
   read it from both sides, and disable it again. The guide prints the commands
   but no output (pp. 140–141), so record what you see:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port6"
   set rpvst-port enabled
   next
   end
   next
   end
   FGT # diagnose switch-controller switch-info rpvst <SWITCH_SN> port6
   FSW # diagnose stp rapid-pvst-port list port6
   ```

   With no RPVST+ neighbor on the port, expect no `IC` (inconsistent) state;
   the CLI Reference says `IC` appears when VLAN priorities are inconsistent or
   the VLAN configuration does not match (p. 344). Then:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port6"
   set rpvst-port disabled
   next
   end
   next
   end
   ```

**Track 2:** Run steps 2 and 3 on your controller (on FGT-1, step 3 is the
negative test). If Lab 2.2's third outcome applies, run step 4's two controller
configuration blocks against `S248EPTF18000000` and check them with `show
switch-controller managed-switch S248EPTF18000000`. Skip the diagnostics.

**Track 2: read-and-predict.** (Track 1 does these too.)

1. An HA pair of FortiGates has a **hardware-switch** FortiLink interface; two
   FortiSwitch units each connect to one port of it, with an ISL between the
   switches for redundancy. Predict what must be configured on the FortiLink
   hardware-switch interface, and what must come first. **Answer:** `set stp
   enable` on that interface, after LLDP transmission has been enabled with
   `set lldp-transmission enable`. STP and STP forwarding are supported on the
   hardware switch; a software switch is not supported (FortiLink Guide 7.6.7,
   p. 61). Without STP the two FortiGate ports and the ISL form a loop.
2. The same design on a FortiGate model with no aggregate-interface support.
   Predict how the FortiGate becomes the root of the CIST, and why each switch
   goes in its own region. **Answer:** give the FortiGate the lowest priority
   with `set switch-priority` under `config system stp` (for example 4096, below
   the switches' priorities), and give each switch a different MST revision with
   `set revision` under its own `config stp-settings` (with `local-override
   enable`) (p. 61; FortiOS 7.6.0 CLI Reference). With each switch a region of its
   own, the regions and the FortiGate meet in the CST, where the lowest bridge ID,
   the FortiGate's, is the CIST root. That command would be, per switch:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config stp-settings
   set local-override enable
   set revision 2
   end
   next
   end
   ```

   It is shown for reading only; do not run it in this lab, because on S3 it
   would split `FSW-A` and `FSW-B` into separate regions before Chapter 06.
3. A FortiSwitch region whose CIST root is inside the region connects to an
   RPVST+ network. In the RPVST+ network, VLAN 20 has bridge priority 4096 and
   the CIST root's priority is 16384. Predict whether the design follows the
   guide's rule. **Answer:** no. With the CIST root in the MSTP region, the
   RPVST+ VLANs other than VLAN 1 must have priorities worse (numerically
   greater) than the CIST root's; 4096 is better. Raise VLAN 20's priority above
   16384, or lower the CIST root's (FortiLink Guide 7.6.7, p. 140).
4. Now the CIST root is in the RPVST+ network. Predict which BPDUs the boundary
   FortiSwitch uses to build its tree. **Answer:** only VLAN 1's; the BPDUs for
   VLANs 2 and up are used for consistency checks, so their root priorities must
   be better (numerically lower) than VLAN 1's (p. 140).
5. On a single managed switch with the controller as its only neighbor, predict
   which bridge is root and whether anything changes if the FortiGate is a 60F
   with `switch-priority 0`. **Answer:** the switch is root either way. The
   FortiGate's bridge priority matters only on an interface where the FortiGate
   runs STP, which a normal FortiLink interface does not (`stp` default
   `disable`; p. 136).

**Expected result:** Track 1: the FortiLink trunk and `internal` show STP status
`DISABLED`; the controller's FortiLink interface shows `stp disable` (or the
lines are absent on your model); C1 shows `config system stp` with priority
32768, and C2 or C3 refuses it; `port6` showed RPVST+ state while enabled and is
back to `disabled`. Track 2: the same controller results and the five
predictions answered.

**Negative test:** On C2 or C3 (and on Track 2 with FGT-1), `get system stp` is
refused, because `config system stp` is not available for FortiGate-VM64. On C1,
try a priority that is not in the list:

```text
FGT # config system stp
set switch-priority 1000
end
```

FortiOS refuses it: the allowed values are 0, 4096, …, 57344 in steps of 4096
(FortiOS 7.6.0 CLI Reference). Record the message either way.

**Rollback:** Make sure `port6` reads `rpvst-port disabled` (or the line is
absent). Nothing else was changed.

**Lab verified by:** *pending*

## Lab Verification

Complete this sign-off once Labs 5.1 to 5.3 have been run end to end, including
each negative test and Lab 5.2's loop steps with the safety net in place. Until
then, the labs are unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

A managed FortiSwitch runs MSTP itself from settings the FortiGate pushes: a
region name and revision, a VLAN-to-instance map, per-switch priorities, and
per-port STP, edge port, BPDU guard, root guard, loop guard, and RPVST+ options.
The FortiLink link does not run STP, so a single managed switch is its own root;
only an HA design with a hardware-switch FortiLink interface puts the FortiGate in
the tree, as the CIST root. Two ports of one switch joined by a cable become a
designated and a backup port; BPDU guard shuts an edge port on the first BPDU;
root guard keeps a port from leading to a new root; loop guard shuts a port that
hears its own probe come back, and is not the same as STP loop protection. The
lab ends with region `lab-174`, instance 1 for the `FSW-LAN` VLANs with priority
16384 on `FSW-A`, BPDU guard on `port1` and `port2`, and the loop ports at their
defaults with the cable out of `port6`.

- [ ] I read the default spanning tree and explained why the switch is root.
- [ ] I set the region name and revision, mapped the `FSW-LAN` VLANs to
      instance 1, and set its priority to 16384 on my switch.
- [ ] I built the loop safety net (isolation, `fsw-guest`, `storm-loop-174`)
      before connecting the loop cable.
- [ ] I saw STP put one loop port in the backup role.
- [ ] I tripped BPDU guard with the loop and recovered the port.
- [ ] I recorded whether loop guard detected the loop with STP off, and recovered.
- [ ] I triggered root guard with a Linux bridge on endpoint A.
- [ ] `port1` and `port2` have BPDU guard enabled; `port5` and `port6` are back at
      their defaults; `storm-loop-174` is deleted.
- [ ] I can state why C1 has `config system stp` and C2 and C3 do not, and how a
      FortiGate becomes the CIST root.
- [ ] I can state the two RPVST+ interoperation rules.
