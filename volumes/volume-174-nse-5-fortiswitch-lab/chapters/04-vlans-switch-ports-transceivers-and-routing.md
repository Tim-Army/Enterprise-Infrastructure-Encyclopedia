# Chapter 04: VLANs, Switch Ports, Transceivers, and Routing

## Learning Objectives

- Create FortiSwitch VLANs as VLAN interfaces on the FortiLink interface, give
  them addresses and a DHCP server, group them in a zone, and let them use the
  lab's firewall policies.
- Explain native, allowed, and untagged VLANs on a managed switch port, read a
  port's VLAN settings from the controller and from the switch, and predict
  which frames a port accepts and sends.
- Set port properties (description, speed, status), read port properties and
  statistics, use PoE where the model has it, run a cable test, and read the
  transceiver inventory.
- Build a link aggregation group (a FortiSwitch "trunk") to an endpoint and read
  its LACP state.
- State which FortiSwitch models support split ports, and describe how a split
  port is configured and what it costs.
- Route between FortiSwitch VLANs on the FortiGate, control that traffic with a
  zone setting, and describe the two ways a managed switch can route on its own
  (Layer 3 switch configuration and inter-VLAN routing offload) and their limits.

## Theory and Architecture

### Where FortiSwitch VLANs live

In FortiLink mode a FortiSwitch VLAN is a **VLAN interface on the FortiLink
interface** of the controller: `config system interface`, with `interface` set
to the FortiLink port and a `vlanid` (FortiLink Guide 7.6.7, p. 103). The
controller pushes the VLAN to the managed switches, and the FortiLink link
carries it tagged. The switch forwards the VLAN at Layer 2; the FortiGate holds
its address, serves its DHCP, routes it, and applies firewall policy to it.
Traffic between two VLANs therefore goes up the FortiLink link to the FortiGate
and back down, unless the switch is told to route it itself (see "Routing between
VLANs" below).

The auto-created VLANs of Chapter 03 (quarantine 4093, rspan 4092, and the
others) are interfaces of exactly this kind. This chapter adds the five lab
VLANs from Chapter 01:

| Interface | VLAN ID | Address | DHCP | Zone `FSW-LAN` | Later use |
| --- | --- | --- | --- | --- | --- |
| `fsw-users` | 1741 | `10.174.41.1/24` | `.100`–`.199` | Yes | Endpoint A, 802.1X (Chapter 07) |
| `fsw-voice` | 1742 | `10.174.42.1/24` | No | Yes | LLDP-MED voice (Chapter 10) |
| `fsw-iot` | 1743 | `10.174.43.1/24` | No | Yes | Endpoint B, NAC target (Chapter 09) |
| `fsw-guest` | 1744 | `10.174.44.1/24` | No | Yes | Guest and auth-fail VLAN (Chapter 07) |
| `fsw-tenant` | 1745 | `10.174.45.1/24` | No | No | Tenant VDOM (Chapter 10) |

Interface names are limited to 15 characters (FortiOS 7.6.0 CLI Reference,
`config system interface`), and FortiSwitch port settings refer to a VLAN by
this interface name, not by its ID.

The FortiLink Guide (p. 46) says that **VLAN optimization** is on by default:
the trunks that FortiLink forms automatically carry only user-defined VLANs
rather than VLANs 1–4093. The value names differ between references (the
FortiOS 7.6.0 CLI Reference lists `vlan-optimization` as `enable` or `disable`;
the guide uses `configured`, `prune`, and `none`), and this volume leaves the
default alone.

### Native, allowed, and untagged VLANs

Each managed-switch port has three VLAN settings (FortiLink Guide 7.6.7,
pp. 102–104), set under `config switch-controller managed-switch`,
`config ports`:

| Setting | Option | Ingress | Egress |
| --- | --- | --- | --- |
| Native VLAN | `vlan` | Untagged frames are put in this VLAN | Frames of this VLAN leave untagged |
| Allowed VLANs | `allowed-vlans` (or `allowed-vlans-all enable`) | A tagged frame is accepted only if its tag is the native VLAN or in this list | A frame leaves only if its VLAN is the native VLAN or in this list |
| Untagged VLANs | `untagged-vlans` | No effect (egress only) | Frames of these VLANs leave without a tag; each must also be an allowed VLAN |

A port with a native VLAN and nothing else is what other vendors call an
**access port**. A port that also carries allowed VLANs, tagged, is what they
call an **802.1Q trunk**. `allowed-vlans-all enable` allows every user-defined
VLAN, or every VLAN 1–4094 if `vlan-all-mode` is `all` (p. 104).
`discard-mode` (`none`, `all-tagged`, `all-untagged`) can additionally drop all
tagged or all untagged frames on a port (p. 123).

`set allowed-vlans` replaces the whole list. To add one VLAN to a port and keep
the others, use `append allowed-vlans`; this matters because every port already
lists a VLAN you must not lose.

### What a managed port looks like out of the box

The FortiLink Guide prints managed ports in their default VLAN state in several
examples (pp. 232 and 320):

```text
edit "port2"
set vlan "_default"
set allowed-vlans "quarantine"
set untagged-vlans "quarantine"
```

The native VLAN is the default VLAN, and the quarantine VLAN is allowed and
untagged. That is what lets the controller quarantine a host on any port
(Chapter 09): the host's frames move to the quarantine VLAN while the host still
sends and receives untagged frames. In this chapter, never remove `quarantine`
from a port's allowed list. Your build may name the default VLAN interface
differently from `_default`; Lab 4.2 reads it from your own port.

### A FortiSwitch "trunk" is a LAG

In FortiSwitchOS and in the switch controller, **trunk** means a **link
aggregation group** (802.3ad), not an 802.1Q tagged port. A trunk is an entry
under `config ports` with `type trunk`, a `mode` (`static`, `lacp-passive`, or
`lacp-active`), and `members` (FortiLink Guide 7.6.7, pp. 115–118). FortiLink's
own uplink and inter-switch links are trunks of this kind, formed automatically
(the `auto-isl` trunk of Lab 3.1). Keep the two meanings apart on the exam: a
question that says "trunk" about a FortiSwitch means a LAG.

Other trunk options are `lacp-speed` (`slow`, every 30 seconds; `fast`, every
second), `min-bundle` and `max-bundle`, `aggregator-mode` (`bandwidth`, the
default, or `count`), and, from FortiOS 7.4.4, an LACP `fallback-port` that stays
up for a device that is not running LACP yet, such as a PXE client (pp. 117–118).

### Port properties, PoE, cable tests, and transceivers

The controller sets a port's `description`, `speed`, and `status` (`up` or
`down`) (p. 109). Three read-only views help:

| View | Command | Source |
| --- | --- | --- |
| What the port can do: PoE standard and budget, connector, supported speeds | `diagnose switch-controller switch-info port-properties [<switch>] [<port>]` | FortiLink Guide 7.6.7, p. 110 |
| What the port is doing: link, speed, duplex, counters, errors | `diagnose switch-controller switch-info port-stats <switch> <port>` | FortiLink Guide 7.6.7, p. 336 |
| The same from the switch | `diagnose switch physical-ports summary`, `diagnose switch physical-ports list` | FortiSwitchOS 7.6.7 CLI Reference, pp. 367, 375 |

**PoE** applies only to models whose name carries a POE or FPOE suffix (feature
matrix note 1). The controller enables or disables it per port (`poe-status`)
and, from FortiOS 7.2.4, sets the port's PoE mode, priority, and power behavior
during a restart (`poe-port-power normal`, `perpetual`, or `perpetual-fast`)
(FortiLink Guide 7.6.7, pp. 112–114). The 7.6.7 matrix marks perpetual PoE as
supported in the 1xxE/1xxF column and not in the 200 Series column.

A **cable test** runs a time-domain reflectometer (TDR) on a copper port and
reports each pair as `Open`, `Short`, `Ok`, `Open_Short`, `Unknown`, or
`Crosstalk`; an empty port reads `Open` with length 0. It interrupts traffic for
several seconds on a port whose link is up (FortiLink Guide 7.6.7, p. 331).

**Transceivers.** The switch reports the module in each SFP or QSFP cage with
`get switch modules {summary | detail | status | limits} [<port>]`: the module
type, vendor, part and serial numbers, and, for modules with digital
diagnostics, temperature, voltage, laser bias, and transmit and receive power
(FortiSwitchOS 7.6.7 CLI Reference, pp. 503–504). The controller's FortiSwitch
Ports page shows transceiver information per port (FortiLink Guide 7.6.7,
p. 334). The 7.6.7 feature matrix has no row for supported transceivers; check
Fortinet's transceiver compatibility information for your model before you buy
optics.

### Split ports

On models with 40G or 100G QSFP ports, a breakout cable turns one port into
four 10G or 25G (or two 50G, or four 1G) subports, configured on the switch
with `config switch phy-mode` (FortiLink Guide 7.6.7, pp. 119–123). Three facts
matter for the exam:

- **Which models.** In the 7.6.7 feature matrix, split port is supported only in
  the 500 Series, 10xx (FS-1024E, FS-1048E, FS-1048G, FS-T1024E, FS-T1024F-FPOE),
  and 3032 (FS-3032E, FS-3032G) columns; the 1xxE/1xxF column (S1 and S2) and
  the 200 Series column (S3) show a dash. The guide lists the splittable ports:
  ports 29 and 30 on the FS-524D, ports 53 and 54 on the FS-548D, ports 25 and 26
  on the FS-1024E and FS-T1024E, ports 49–54 on the FS-1048E depending on its
  mode, and the QSFP ports of the FS-3032E (p. 119).
- **It costs a restart and configuration.** Changing `phy-mode` asks for
  confirmation, warns that ports will be added and removed and that removed
  ports lose their configuration, and requires a reboot (p. 122). From FortiOS
  7.2.0 the controller updates the port list itself after the switch restarts;
  before 7.2.0 the switch had to be deleted, rediscovered, and authorized again
  (pp. 119–121).
- **Naming and limits.** Subports are named with `.x`, for example `port29.1` to
  `port29.4` (p. 122). Split ports are not configured on pre-configured
  FortiSwitch entries (p. 119), so a pre-provisioned switch gets its split ports
  only after it joins. FortiSwitchOS 7.6.0 raised the software port limit to 128
  plus the internal and management interfaces, which allows more splitting
  (p. 119).

No switch option in this volume can split a port, so Lab 4.4 is read-and-predict
on every option.

### Routing between VLANs

**On the FortiGate (the default).** Each FortiSwitch VLAN interface is a
connected network on the controller, so the FortiGate routes between them with
no static routes. Whether the traffic is allowed is a firewall decision: a
firewall policy between the two interfaces, or, when both interfaces are in the
same zone, the zone's `intrazone` setting. `intrazone` allows or denies traffic
between interfaces of the zone, and its default is `deny` (FortiOS 7.6.0 CLI
Reference, `config system zone`, p. 1824). This lab puts four VLANs in the zone
`FSW-LAN`, so the zone, not a policy, decides whether they can reach each other.
That costs no policy slot on C2.

**On the switch: Layer 3 switch configuration (FortiOS 7.6.4 and later).** From
FortiOS 7.6.4 the controller can configure switch virtual interfaces (SVIs),
routed VLAN interfaces, static IPv4 routes, VRFs, and DHCP servers on "layer-3
managed switches", under the switch's managed-switch entry
(`config system-interface`, `config router-static`, `config router-vrf`;
FortiLink Guide 7.6.7, pp. 152–158). These sub-tables are not in the FortiOS
7.6.0 CLI Reference, and FGT-1 runs FortiOS 7.6.2, so on FGT-1 they are
read-and-predict. The guide does not list which models count as "layer-3
managed switches". The 7.6.7 feature matrix marks SVIs and static routing as
supported in standalone and managed mode in both the 1xxE/1xxF and 200 Series
columns, with note 9: in managed mode, static routing is IPv4 only. The matrix
also marks the 1xxE/1xxF column as software-based routing only and the 200
Series as hardware-based routing. VRF needs an advanced features license
(p. 157).

**On the switch: inter-VLAN routing offload (FortiOS 7.4.1 and later).** The
controller can program a managed switch to route trusted traffic between chosen
VLANs itself (FortiLink Guide 7.6.7, pp. 106–108). Each VLAN interface gets
`switch-controller-offload enable` and a `switch-controller-offload-ip`; one
VLAN gets `switch-controller-offload-gw enable`; the switch entry gets
`route-offload enable` (and `route-offload-mclag` with per-VLAN `router-ip` in
an MCLAG). The FortiGate then creates an SVI per VLAN on the switch, with the
offload address, and a default route in `vrf1` toward the gateway VLAN's
FortiGate address with `gw-l2-switch` enabled. Clients use the offload address as
their gateway. Offloaded traffic is not inspected by the FortiGate. It needs an
advanced features license, is not supported in multitenancy VDOMs, and in the
7.6.7 matrix is supported only in the 10xx, 2048F, and 3032 columns (note 19);
the 1xxE/1xxF and 200 Series columns show a dash. None of S1, S2, or S3 can do
it.

### Model support for this chapter

From the FortiSwitchOS 7.6.7 feature matrix (`temp/nse5fsw/fm767.txt`, the
position-based read); chain = standalone and managed, check = standalone only,
dash = not supported:

| Feature | 1xxE/1xxF (S1 FS-108F, S2 FS-124F) | 200 Series (S3) | Note |
| --- | --- | --- | --- |
| Link aggregation group size | 8 | 8 | |
| LAG min-max bundle, LACP fallback mode | Chain | Chain | |
| PoE modes, PoE pre-standard detection | Chain (PoE models only) | Chain (PoE models only) | Note 1 |
| Perpetual PoE | Chain | Dash | Note 14 for FS-1xx BIOS versions |
| TDR cable diagnostics | Chain | Chain | |
| Port statistics CLI | Chain | Chain | |
| Split port | Dash | Dash | Note 5; 500 Series, 10xx, 3032 only |
| SVI, static routing | Chain | Chain | Note 9: IPv4 only in managed mode |
| Inter-VLAN routing offload | Dash | Dash | Note 19; 10xx, 2048F, 3032 only |
| Block intra-VLAN traffic (access VLANs) | Chain | Chain | Note 7: at most 16 access VLANs on FS-1xxE, FS-108F, FS-124F |

Note 7 belongs to the "Block intra-VLAN traffic" row. An **access VLAN** in
FortiSwitch terms is a VLAN with intra-VLAN traffic blocked
(`switch-controller-access-vlan enable` on the FortiGate, `access-vlan enable`
on the switch; FortiLink Guide 7.6.7, pp. 261–263), such as the auto-created
quarantine VLAN. The limit of 16 counts those VLANs, not every VLAN; the matrix
rows read for this chapter give no general VLAN count for these models.

## Design Considerations

### The C2 interface cap and the lab VLANs

The FortiOS 7.6.0 Administration Guide page
[Permanent trial mode for FortiGate-VM](https://docs.fortinet.com/document/fortigate/7.6.0/administration-guide/441460)
says only "Maximum of three interfaces, firewall policies, and routes". It does
**not** say which kinds of interface count. Chapters 01 and 02 planned the lab
VLANs on the assumption that VLAN interfaces do not count; the FortiOS
documentation does not settle that, and the evidence that exists points the
other way:

- A Fortinet staff member answered on the Fortinet Community (April 2023, about
  FortiOS 7.2.2 and later) that the trial allows three interfaces, "physical and
  VLAN interfaces combined", after users reported
  "Maximum number of entries has been reached." when they created a VLAN on a
  trial VM with three ports
  ([thread](https://community.fortinet.com/t5/Support-Forum/Fortigate-trial-4-inerfaces-limitation/td-p/243345)).
  A Community answer is not documentation, and it predates FortiOS 7.6.
- On C2, FGT-1 already has three physical ports (`port1`, `port2`, `port3`).
  If VLAN interfaces count, the first lab VLAN is refused.
- Chapter 03 (Lab 3.2) recorded whether the auto-created FortiLink VLAN
  interfaces exist on your controller. If they exist on C2, the switch
  controller created them despite the cap; that does not tell you whether an
  administrator can create more.

So Lab 4.1 starts on C2 with a test: create `fsw-users` alone and read the
result. If FortiOS accepts it, create the rest one at a time and record any
refusal. If it refuses, record **lab VLANs: NO-GO on C2**. Then:

| Path | What changes |
| --- | --- |
| Move Track 1 to C1 or C3 (the Chapter 02 fallbacks) | Nothing in the labs; the C1 and C3 steps apply |
| Stay on C2 for this chapter | Labs 4.2 and 4.3 run their port steps with the auto-created `video` VLAN in place of `fsw-users` and `fsw-iot`, endpoint to endpoint at Layer 2 with static addresses; the DHCP, policy, and routing steps of Labs 4.1 and 4.5 become read-and-predict. Chapters 07, 09, and 10, which use the lab VLANs, then need C1 or C3 |
| Track 2 on FGT-1 alone | The same refusal; build nothing that the cap refuses, and read-and-predict the rest |

Do not delete physical ports to make room: `port1` carries management and TFTP,
`port2` the services segment, and `port3` FortiLink.

### Names, the zone, and the policies

The VLAN interfaces use Chapter 01's names. `role lan` is set on each, as the
FortiLink Guide recommends for VLAN interfaces used in firewall policies when the
security rating feature is used (pp. 42, 102), and `device-identification
enable` prepares for NAC in Chapter 09. A zone must be built from interfaces
that are in no other zone and **have no firewall policies yet** (FortiOS 7.6.0
CLI Reference, p. 1824), so Lab 4.1 creates `FSW-LAN` before any policy refers
to its members.

The policy plan from Chapters 01 and 02 adds `FSW-LAN` to two existing
policies, so no slot is used:

| Slot | Before this chapter | After Lab 4.1 |
| --- | --- | --- |
| P1 | FGT-1's VLAN 200 internet policy, `port2` to `port1` (C2 and C3), if kept | Sources `port2` and `FSW-LAN`. On C1, where Chapter 02 built no internet policy, Lab 4.1 creates `P1-fsw-lan-internet` (`FSW-LAN` to `<WAN_PORT>`, NAT) |
| P2 | `P2-fortilink-services`, `port3` to `port2`, service `lab-svc-174` | Sources `port3` (`<FL_PORT>`, `port4`) and `FSW-LAN` |
| P3 | Free | Free |

Two details of P1 on C2 and C3. If P1's source address is not `all` (for
example a VLAN 200 subnet object), FSW-LAN traffic does not match it; Lab 4.1
adds an address object `fsw-lan-174` (`10.174.40.0/21`, which covers
`10.174.40.0`–`10.174.47.255`) to P1's sources. And if P1 does not use NAT, the
upstream router (the UCGF) needs a route back to `10.174.40.0/21`, which this
volume does not add; in that case use P3 for an `FSW-LAN` to `port1` policy with
NAT instead of changing P1, because enabling NAT on P1 also changes FGT-1's VLAN
200 traffic.

`fsw-tenant` (1745) is created in the root VDOM and kept out of the zone;
Chapter 10 decides how the tenant VDOM uses it.

### Port plan for this chapter

| Switch port | After this chapter | Built in |
| --- | --- | --- |
| `port1` | Endpoint A; native `fsw-users`; allowed list as found (with `quarantine`) | Lab 4.2 |
| `port2` | Endpoint B; native `fsw-iot`; allowed list as found | Lab 4.2 |
| `port3`, `port4` | Back to their defaults (the LAG of Lab 4.3 is removed) | Lab 4.3 |
| `port5`, `port6` | Untouched (loop cable, Chapter 05) | — |
| `<FSW_FL_PORT>` | Untouched | — |

`port3` and `port4` carry the temporary LAG because no later lab uses them while
the switch is managed (Chapter 11 uses `port3` for management only after the
switch is standalone).

### What to keep after this chapter

| Object | Kept | Why |
| --- | --- | --- |
| VLAN interfaces `fsw-users`, `fsw-voice`, `fsw-iot`, `fsw-guest`, `fsw-tenant` | Yes (if the controller accepted them) | Chapters 05–12 |
| Zone `FSW-LAN` (1741–1744), `intrazone deny` | Yes | One policy covers the four VLANs; inter-VLAN traffic stays blocked |
| DHCP server on `fsw-users` (`.100`–`.199`) | Yes | Endpoint A, Chapter 07 |
| `FSW-LAN` in the sources of P1 and P2 (C1: `P1-fsw-lan-internet`) | Yes | Internet and services for the lab VLANs |
| Address object `fsw-lan-174` | Only if P1 needed it | P1's source match |
| `port1` native `fsw-users`, `port2` native `fsw-iot` | Yes | Endpoints for Chapters 05–09 |
| LAG `lag-174` | No | Lab 4.3 removes it |
| Switch SVI and static route (FortiOS 7.6.4 and later, Lab 4.5) | No | Lab 4.5 removes them |

## Implementation and Automation

The labs are the implementation. Three habits help.

**Read before you write.** Before changing a port, save its current settings,
because `set allowed-vlans` replaces a list and the default list matters:

```text
FGT # show switch-controller managed-switch <SWITCH_SN>
```

**Check both ends.** The controller shows what it intends; the switch shows what
it received:

```text
FGT # diagnose switch-controller switch-info port-stats <SWITCH_SN> port1
FSW # diagnose switch physical-ports summary port1
FSW # diagnose switch vlan list 1741
```

**Test from the endpoint.** A VLAN is proven only when an endpoint in it gets an
address, reaches its gateway, and is or is not allowed further, as intended.

The FortiOS configuration commands in this chapter were checked against the
FortiOS 7.6.0 CLI Reference; `execute`, `diagnose`, and `get` commands against
the FortiLink Guide 7.6.7, or the FortiOS 8.0.1 CLI Reference as a cross-check
where the guide prints no syntax line (each case is marked). The Layer 3 switch
sub-tables of Lab 4.5 are from the FortiLink Guide 7.6.7 only (FortiOS 7.6.4 and
later). Switch commands were checked against the FortiSwitchOS 7.6.7 CLI
Reference. The Linux commands use `iproute2` (`ip-link(8)`, `ip-address(8)`).

## Validation and Troubleshooting

| Symptom | Likely cause | Check |
| --- | --- | --- |
| `Maximum number of entries has been reached.` when you create a VLAN interface | The evaluation's interface cap (C2) | Record the NO-GO; see Design Considerations |
| The zone refuses a VLAN interface | The interface is already in a policy or another zone | `diagnose sys cmdb refcnt show system.interface.name <VLAN_IF>`; build the zone before the policies |
| Endpoint A gets no DHCP lease | `port1` native VLAN not `fsw-users`; no DHCP server on `fsw-users`; the switch is not `Authorized/Up` | `show switch-controller managed-switch <SWITCH_SN>`; `show system dhcp server`; `execute dhcp lease-list fsw-users` |
| A tagged VLAN does not reach the endpoint | The VLAN is not in the port's `allowed-vlans`; the endpoint's VLAN subinterface has the wrong ID | `diagnose switch physical-ports summary port1` on the switch; `ip -d link show` on the endpoint |
| Quarantine stops working on a port after a VLAN change | `set allowed-vlans` replaced the list and removed `quarantine` | Restore the recorded list; use `append` next time |
| A LAG stays down, members `BLOCK` | The endpoint is not running LACP, or runs it on different ports | `diagnose switch trunk list lag-174` on the switch; the endpoint's bond state |
| Hosts in two lab VLANs cannot reach each other | Intended: both VLANs are in `FSW-LAN` with `intrazone deny` | `show system zone FSW-LAN`; `diagnose debug flow` |
| `get switch modules` shows no module | No SFP or QSFP module inserted, or a copper-only port | Check the cage; run it on an SFP port |
| `config system-interface` under the switch entry is rejected | FortiOS earlier than 7.6.4 | `get system status` on the controller |

## Security and Best Practices

- **Keep users off the default VLAN.** Give every access port a lab or
  production native VLAN and leave the default VLAN for nothing but switch
  defaults.
- **Allow only what a port needs.** Add tagged VLANs with `append`, remove them
  when the device leaves, and never use `allowed-vlans-all` on an access port.
- **Keep quarantine reachable.** Do not remove `quarantine` from a port's
  allowed and untagged lists, or the controller cannot quarantine a host there.
- **Deny between VLANs by default.** `intrazone deny` (the default) keeps the
  lab VLANs apart; open specific traffic with a policy when a design needs it.
- **Shut unused ports.** `set status down` on unused ports, and give each port a
  description, so an unexpected link stands out.
- **Know what is not inspected.** Traffic routed by the switch (Layer 3 switch
  configuration or routing offload) does not pass through the FortiGate's
  firewall policies; use it only between VLANs you trust with each other.

## References and Knowledge Checks

**References**

- [Fortinet, *FortiLink Guide (FortiOS 7.6.7)*](https://docs.fortinet.com/document/fortiswitch/7.6.7/fortilink-guide)
  — roles for FortiLink VLAN interfaces (p. 42), VLAN optimization and pruning
  (pp. 46–47), creating VLANs and native, allowed, and untagged VLANs
  (pp. 101–104), software switches (p. 105), inter-VLAN routing offload
  (pp. 106–108), port speed and status, port properties, flap guard
  (pp. 109–112), PoE (pp. 112–114), link aggregation groups and LACP fallback
  (pp. 115–118), split ports and FEC (pp. 119–123), `discard-mode` (p. 123),
  Layer 3 switch configuration (pp. 152–158), default port extracts (pp. 232,
  320), blocking intra-VLAN traffic (pp. 261–263), cable test (pp. 331–332),
  FortiSwitch ports display (p. 334), port statistics (pp. 335–338).
- [Fortinet, *FortiSwitchOS 7.6.7 CLI Reference*](https://docs.fortinet.com/document/fortiswitch/7.6.7/fortiswitchos-cli-reference)
  — `diagnose switch physical-ports cable-diag` (p. 363), `list` (p. 367),
  `summary` (p. 375), `diagnose switch trunk list` and `summary` (pp. 379–381),
  `diagnose switch vlan list` (p. 382), `get router info routing-table`
  (p. 485), `get switch modules` (pp. 503–504), `get switch phy-mode` and
  `physical-port` (p. 506), `get switch poe inline` (p. 507),
  `config switch phy-mode`.
- [Fortinet, FortiOS 7.6 documentation](https://docs.fortinet.com/product/fortigate/7.6)
  — the FortiOS 7.6.0 CLI Reference: `config system interface`
  (pp. 1383–1432), `config switch-controller managed-switch` and its `ports`
  table (p. 1076), `config system zone` (p. 1824), `config system dhcp server`,
  `config firewall policy`; and
  [Permanent trial mode for FortiGate-VM](https://docs.fortinet.com/document/fortigate/7.6.0/administration-guide/441460).
- FortiOS 8.0.1 CLI Reference (cross-check only) — `diagnose switch-controller
  switch-info trunk`, `modules`, and `poe`; `execute switch-controller
  switch-action cable-diag` and `poe reset`; `diagnose debug flow`;
  `diagnose sniffer packet`; `execute ping-options source`.
- FortiSwitchOS 7.6.7 feature matrix (`temp/fsw/FSW-7.6.7-Feature-Matrix.pdf`)
  — split port (note 5), inter-VLAN routing offload (note 19), static routing
  (note 9), access VLANs (note 7), LAG size, PoE (notes 1, 14), TDR.
- [Fortinet Community, *Fortigate trial 4 interfaces limitation*](https://community.fortinet.com/t5/Support-Forum/Fortigate-trial-4-inerfaces-limitation/td-p/243345)
  — a staff answer on VLAN interfaces and the trial's interface cap (not
  documentation).
- [`ip-link(8)`](https://man7.org/linux/man-pages/man8/ip-link.8.html) — VLAN
  and bond links on the Linux endpoints.

**Knowledge checks**

1. A port has native VLAN `fsw-users` and allowed VLANs `quarantine` and
   `fsw-voice`. A frame tagged 1743 arrives. What happens, and why?
2. You run `set allowed-vlans "fsw-voice"` on a port that showed
   `allowed-vlans "quarantine"`. What did you lose, and what should you have
   typed?
3. On a FortiSwitch, what is a "trunk"? How does that differ from an 802.1Q
   trunk on most other switches?
4. Which FortiSwitch models in the 7.6.7 feature matrix support split ports, and
   what happens to the configuration of ports removed by a `phy-mode` change?
5. Two hosts in `fsw-users` and `fsw-iot` cannot ping each other, although both
   reach their gateways. Name the setting responsible and its default.
6. Why can none of this volume's switch options do inter-VLAN routing offload,
   even with an advanced features license?
7. What does the FortiOS documentation say about whether VLAN interfaces count
   against the FortiGate-VM evaluation's interface cap?

## Hands-On Lab

**Shared prerequisites.** Chapter 03 complete: `<SWITCH_SN>` `Authorized/Up` at
`10.255.1.2` with description `FSW-A lab-174` and profile `fsw-174-prof` (on S3,
`FSW-A` only); templates and auto-created VLANs at their defaults; P1 (if kept)
and P2 in place; the TFTP VM 140 at `10.30.99.50`. Endpoint A (Linux) cabled to
`port1` and endpoint B (Linux) to `port2`; for Lab 4.3, a second Ethernet port on
endpoint A (for example a USB adapter) and a second patch cable. Track 2: the
Lab 2.2 pre-provisioning outcome, and the stand-in entry `S248EPTF18000000` if
that outcome allowed it. **Cost:** none beyond earlier chapters; a USB Ethernet
adapter if endpoint A has one port.

As in earlier chapters, `FGT #` is the controller on any option, and blocks
written for `port3` apply to C3 with `port4` and to C1 with `<FL_PORT>` (the
factory `fortilink` interface if you used it). `<SWITCH_SN>` is your switch's
serial number; on Track 2 it is `S248EPTF18000000`. `<IFACE>` is the endpoint's
wired interface (`ip -br link` shows it). Before the first change, back up the
controller:

```text
FGT # execute backup config tftp fgt-pre-4-1-174.conf 10.30.99.50
```

### Lab 4.1 — Create the FortiSwitch VLANs, DHCP, the zone, and the policies

**Objective:** Create the five lab VLANs as FortiLink VLAN interfaces with the
Chapter 01 addresses, a DHCP server on `fsw-users`, the zone `FSW-LAN`, and add
the zone to the sources of P1 and P2.

**Platform notes:** Hands-on on C1 and C3 with S1, S2, or S3, and on Track 2 (it
is all controller configuration). On C2, steps 1–2 are a go/no-go test for the
evaluation's interface cap; after a NO-GO, follow Design Considerations. The
parent interface is `<FL_PORT>` (or `fortilink`) on C1, `port3` on C2, `port4`
on C3. P1 differs by option: C1 creates it, C2 and C3 extend FGT-1's existing
one. No switch port changes yet.

**Track 1:**

1. Record the starting point:

   ```text
   FGT # show system interface port3
   FGT # show firewall policy
   ```

   Record the IDs of P1 (if kept) and P2 as `<P1_ID>` and `<P2_ID>`, and P1's
   `srcaddr` and `nat` settings.

2. Create the first VLAN interface alone. On C2 this is the cap test:

   ```text
   FGT # config system interface
   edit "fsw-users"
   set vdom "root"
   set ip 10.174.41.1 255.255.255.0
   set allowaccess ping
   set role lan
   set device-identification enable
   set interface "port3"
   set vlanid 1741
   next
   end
   ```

   Before you press Enter on `end`, predict what C2 does. **Answer:** the
   documentation does not say; a Fortinet staff answer on the Community says the
   trial counts VLAN interfaces with physical ones, which predicts the error
   `Maximum number of entries has been reached.` Record the result exactly. If
   it is refused, record **lab VLANs: NO-GO on C2** and stop this lab here.

3. Create the other four, one at a time, recording any refusal:

   ```text
   FGT # config system interface
   edit "fsw-voice"
   set vdom "root"
   set ip 10.174.42.1 255.255.255.0
   set allowaccess ping
   set role lan
   set device-identification enable
   set interface "port3"
   set vlanid 1742
   next
   edit "fsw-iot"
   set vdom "root"
   set ip 10.174.43.1 255.255.255.0
   set allowaccess ping
   set role lan
   set device-identification enable
   set interface "port3"
   set vlanid 1743
   next
   edit "fsw-guest"
   set vdom "root"
   set ip 10.174.44.1 255.255.255.0
   set allowaccess ping
   set role lan
   set device-identification enable
   set interface "port3"
   set vlanid 1744
   next
   edit "fsw-tenant"
   set vdom "root"
   set ip 10.174.45.1 255.255.255.0
   set allowaccess ping
   set role lan
   set interface "port3"
   set vlanid 1745
   next
   end
   ```

4. Create the zone before any policy refers to its members (an interface with
   policies cannot join a zone, FortiOS 7.6.0 CLI Reference, p. 1824).
   `intrazone deny` is the default; it is written out so the intent is visible:

   ```text
   FGT # config system zone
   edit "FSW-LAN"
   set interface "fsw-users" "fsw-voice" "fsw-iot" "fsw-guest"
   set intrazone deny
   next
   end
   ```

5. Add the DHCP server for `fsw-users`, in the form of the FortiLink Guide's
   VLAN example (p. 103):

   ```text
   FGT # config system dhcp server
   edit 0
   set interface "fsw-users"
   set default-gateway 10.174.41.1
   set netmask 255.255.255.0
   set dns-service default
   config ip-range
   edit 1
   set start-ip 10.174.41.100
   set end-ip 10.174.41.199
   next
   end
   next
   end
   ```

6. Add `FSW-LAN` to P2's sources. `append` keeps `port3`:

   ```text
   FGT # config firewall policy
   edit <P2_ID>
   append srcintf "FSW-LAN"
   next
   end
   ```

7. P1. **C2 and C3:** add `FSW-LAN` to the sources of FGT-1's existing policy.
   If its `srcaddr` (step 1) is not `all`, also create and append the address
   object; if it is `all`, skip the address lines:

   ```text
   FGT # config firewall address
   edit "fsw-lan-174"
   set subnet 10.174.40.0 255.255.248.0
   next
   end
   FGT # config firewall policy
   edit <P1_ID>
   append srcintf "FSW-LAN"
   append srcaddr "fsw-lan-174"
   next
   end
   ```

   If P1 has no `nat enable`, read Design Considerations and decide between
   adding an upstream route (outside this volume) and a P3 policy with NAT; do
   not change P1's NAT. If FGT-1 has no P1, create it as on C1 with `port1` as
   the destination. **C1:** create the internet policy:

   ```text
   FGT # config firewall policy
   edit 0
   set name "P1-fsw-lan-internet"
   set srcintf "FSW-LAN"
   set dstintf "<WAN_PORT>"
   set srcaddr "all"
   set dstaddr "all"
   set action accept
   set schedule "always"
   set service "ALL"
   set nat enable
   set logtraffic all
   next
   end
   ```

   On C1, step 6 used `<FL_PORT>`'s policy; the commands are the same.

8. Review the result:

   ```text
   FGT # show system interface fsw-users
   FGT # show system zone FSW-LAN
   FGT # show firewall policy
   FGT # get router info routing-table all
   ```

   Predict which of the five networks appear as connected routes on Track 1.
   **Answer:** all five (`10.174.41.0/24` to `10.174.45.0/24`), because their
   parent FortiLink port has a link; zone membership has nothing to do with
   routing. In the GUI, **WiFi & Switch Controller > FortiSwitch VLANs** lists
   the five beside the auto-created VLANs, with a Ref count for each (FortiLink
   Guide 7.6.7, p. 104).

9. Look from the switch. VLAN optimization lets the FortiLink trunk carry
   user-defined VLANs (p. 46); record whether the switch already lists VLAN 1741
   although no port uses it yet:

   ```text
   FSW # diagnose switch vlan list 1741
   ```

**Track 2:** Run steps 1–8 on your controller (on FGT-1 alone, the C2 cap test of
step 2 applies first). Skip step 9. In step 8, record which of the five networks
appear in the routing table while the FortiLink port has no link; the local
references do not say whether FortiOS lists the connected routes of an interface
whose parent is down.

**Track 2: read-and-predict.** The FortiLink Guide (p. 105) shows two FortiLink
VLANs created for a software switch:

```text
edit "vlan1"
set vdom "root"
set device-identification enable
set role lan
set snmp-index 46
set interface "fortilink"
set vlanid 3501
next
```

1. Predict what makes this a FortiSwitch VLAN and not a VLAN on an ordinary
   port. **Answer:** `set interface "fortilink"`: its parent is the FortiLink
   interface, so the controller carries it to the managed switches.
2. These two VLANs are then members of a software switch. Predict whether they
   can keep IP addresses. **Answer:** no. The guide says FortiSwitch VLANs in a
   software switch must be configured without IP addresses (p. 105); the
   software switch holds the address, and its `intra-switch-policy` (default
   `implicit`) allows traffic between members. This lab uses a zone instead,
   which keeps one address per VLAN and blocks traffic between them by default.

**Expected result:** The five VLAN interfaces exist on the FortiLink port with
the Chapter 01 addresses (or, on C2, the cap test result is recorded); `FSW-LAN`
holds 1741–1744 with `intrazone deny`; `fsw-users` has a DHCP server for
`.100`–`.199`; P2 and P1 (C1: `P1-fsw-lan-internet`) list `FSW-LAN` among their
sources; Track 1 shows five connected routes. On C2 no policy slot was used:
P1 and P2 used, P3 free.

**Negative test:** Create a second interface with VLAN ID 1741 on the same
FortiLink port:

```text
FGT # config system interface
edit "fsw-dup"
set vdom "root"
set interface "port3"
set vlanid 1741
next
end
```

Expect FortiOS to refuse it, because two interfaces with the same VLAN ID on one
parent would claim the same tagged frames; the local references do not print
the error, so record the message (on C2 the cap may refuse it first; record
which error you see). If it was created, delete it with `delete "fsw-dup"` under
`config system interface`.

**Rollback:** Put P2's source back to `port3` (`set srcintf "port3"`), and P1's
sources back to what step 1 recorded (on C1, delete `P1-fsw-lan-internet`);
delete the DHCP server, the zone, `fsw-lan-174`, and the five interfaces, in that
order; or restore `fgt-pre-4-1-174.conf`. Normally keep everything for Lab 4.2.

**Lab verified by:** *pending*

### Lab 4.2 — Native and allowed VLANs on access and tagged ports

**Objective:** Put endpoint A in `fsw-users` and endpoint B in `fsw-iot` as
access ports, carry `fsw-voice` tagged on endpoint A's port, and see which
frames a port accepts.

**Platform notes:** Hands-on on C1, C2 (after a GO in Lab 4.1, or with the
`video` VLAN after a NO-GO), and C3 with S1, S2, or S3 (on S3, `FSW-A`). Port
names `port1` and `port2` are the same on every switch option. Track 2: build
the port settings on the stand-in entry only if Lab 2.2's third outcome
(ports accepted); otherwise read-and-predict.

**Track 1:**

1. Read `port1` and `port2` as they are now. Record each port's `vlan`,
   `allowed-vlans`, and `untagged-vlans`; record the default VLAN's name as
   `<DEFAULT_VLAN>` and the allowed list as `<PORT1_ALLOWED>`:

   ```text
   FGT # show switch-controller managed-switch <SWITCH_SN>
   ```

   Before you read, predict the allowed and untagged lists. **Answer:** the
   guide's examples show `allowed-vlans "quarantine"` and `untagged-vlans
   "quarantine"` with the default VLAN as native (pp. 232, 320); record what
   your build shows.

2. Make both ports access ports in their lab VLANs and describe them:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port1"
   set description "endpoint A"
   set vlan "fsw-users"
   next
   edit "port2"
   set description "endpoint B"
   set vlan "fsw-iot"
   next
   end
   next
   end
   ```

3. Check on the switch that the native VLAN changed (the Vlan column of the
   summary, FortiSwitchOS 7.6.7 CLI Reference, p. 375):

   ```text
   FSW # diagnose switch physical-ports summary port1
   FSW # diagnose switch physical-ports summary port2
   ```

4. Endpoint A takes a DHCP lease from `fsw-users`. Bounce the link to renew,
   then check the address and the gateway:

   ```bash
   # endpoint A
   sudo ip link set <IFACE> down && sudo ip link set <IFACE> up
   sleep 10; ip -br addr show <IFACE>
   ping -c 3 10.174.41.1
   ```

   ```text
   FGT # execute dhcp lease-list fsw-users
   ```

5. Endpoint B uses a static address in `fsw-iot` (that VLAN has no DHCP server).
   Remove any address your OS assigned on `<IFACE>`, then:

   ```bash
   # endpoint B
   sudo ip addr add 10.174.43.20/24 dev <IFACE>
   sudo ip route replace default via 10.174.43.1
   ping -c 3 10.174.43.1
   ```

6. Carry `fsw-voice` tagged on `port1`. `append` adds it and keeps `quarantine`:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port1"
   append allowed-vlans "fsw-voice"
   next
   end
   next
   end
   ```

   On endpoint A, add a VLAN 1742 subinterface and reach the `fsw-voice`
   gateway:

   ```bash
   # endpoint A
   sudo ip link add link <IFACE> name <IFACE>.1742 type vlan id 1742
   sudo ip addr add 10.174.42.10/24 dev <IFACE>.1742
   sudo ip link set <IFACE>.1742 up
   ping -c 3 10.174.42.1
   ```

   `port1` now carries `fsw-users` untagged and `fsw-voice` tagged: an access
   port with one tagged VLAN, which other vendors would call a trunk.

7. Use the internet and services policies from endpoint A (P1 and P2 of Lab
   4.1). The syslog line goes to `ubuntu-ws` over UDP 514, which P2 allows:

   ```bash
   # endpoint A
   ping -c 3 10.30.99.1
   logger -n 10.200.0.20 -P 514 -d "fsw-users syslog test"
   ```

   ```bash
   # ubuntu-ws
   grep "fsw-users syslog test" /var/log/syslog
   ```

8. Remove the tagged VLAN, returning `port1`'s allowed list to the value you
   recorded in step 1, and delete the endpoint's subinterface:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port1"
   set allowed-vlans <PORT1_ALLOWED>
   next
   end
   next
   end
   ```

   ```bash
   # endpoint A
   sudo ip link delete <IFACE>.1742
   ```

**Track 2:** If Lab 2.2's third outcome applies, run steps 1, 2, 6, and 8 against
`S248EPTF18000000` and check them with
`show switch-controller managed-switch S248EPTF18000000`. Record whether FortiOS
shows the default allowed and untagged lists on a switch that has never joined.
Skip the switch-side and endpoint steps. Otherwise do the read-and-predict only.

**Track 2: read-and-predict.**

1. The FortiLink Guide (p. 118) shows this trunk in a VDOM whose VLAN names end
   in `.39`:

   ```text
   edit "first-mclag"
   set vlan "_default.39"
   set allowed-vlans "quarantine.39"
   set untagged-vlans "quarantine.39"
   set type trunk
   set mode lacp-active
   set mclag enable
   set members "port7" "port8"
   set fallback-port "port8"
   ```

   Predict how a frame of the quarantine VLAN leaves this LAG. **Answer:**
   untagged. `quarantine.39` is in the untagged list, which applies on egress,
   and it is also in the allowed list, as an untagged VLAN must be (p. 102).
   Frames of the native `_default.39` VLAN also leave untagged.
2. `port1` has native `fsw-users` and allowed `quarantine` and `fsw-voice`. A
   frame tagged 1744 (`fsw-guest`) arrives. **Answer:** it is dropped. A tagged
   frame is accepted only if its tag is the native VLAN or in the allowed list
   (p. 102).
3. An administrator types `set allowed-vlans "fsw-voice"` on a default port.
   Predict the side effect. **Answer:** `quarantine` is no longer allowed on
   the port, so quarantining a host there no longer moves it into the
   quarantine VLAN. `append allowed-vlans` would have kept it.

**Expected result:** Track 1: `port1` has native `fsw-users` and its original
allowed list; `port2` has native `fsw-iot`; endpoint A holds a lease from
`.100`–`.199` and reaches `10.174.41.1`, the UCGF, and the syslog listener;
endpoint B reaches `10.174.43.1`; while `fsw-voice` was allowed, endpoint A's
VLAN 1742 subinterface reached `10.174.42.1`. Track 2: the stand-in's ports show
the settings (if accepted), and the predictions are answered.

**Negative test:** Send tagged frames for a VLAN the port does not allow. On
endpoint A, create a VLAN 1743 subinterface and ping the `fsw-iot` gateway:

```bash
# endpoint A
sudo ip link add link <IFACE> name <IFACE>.1743 type vlan id 1743
sudo ip addr add 10.174.43.10/24 dev <IFACE>.1743
sudo ip link set <IFACE>.1743 up
ping -c 3 -I <IFACE>.1743 10.174.43.1
sudo ip link delete <IFACE>.1743
```

The ping fails: 1743 is neither `port1`'s native VLAN nor in its allowed list,
so the switch drops the frames at ingress. Track 2: the read-and-predict item 2
is the negative test.

**Rollback:** Set `port1` and `port2` back to `set vlan <DEFAULT_VLAN>` and the
recorded allowed and untagged lists, and remove their descriptions; remove the
static address from endpoint B. Normally keep both ports for Lab 4.3 and later
chapters.

**Lab verified by:** *pending*

### Lab 4.3 — Port properties, PoE, cable test, a LAG, and transceivers

**Objective:** Read and set port properties, use PoE where the model has it, run
a cable test, build an LACP link aggregation group to an endpoint and read its
state, read the transceiver inventory, and remove the LAG again.

**Platform notes:** Hands-on on C1, C2, and C3 with S1, S2, or S3 (on S3,
`FSW-A`). PoE steps need a POE or FPOE model (feature matrix note 1); on other
models they are read-and-predict. The transceiver step needs a module in an SFP
or QSFP cage (for example the FortiLink link, if it uses one). The LAG uses
`port3` and `port4` and a second Ethernet port on endpoint A; after a C2 NO-GO in
Lab 4.1, use `video` as the LAG's native VLAN. LAG size is 8 ports on all three
options. Track 2: read-and-predict, plus the LAG entry on the stand-in if Lab
2.2's third outcome applies.

**Track 1:**

1. Read what `port1` can do and what it is doing (FortiLink Guide 7.6.7,
   pp. 110 and 336):

   ```text
   FGT # diagnose switch-controller switch-info port-properties <SWITCH_SN> port1
   FGT # diagnose switch-controller switch-info port-stats <SWITCH_SN> port1
   ```

   Record the PoE line, the connector, the speed list, and the negotiated speed
   and duplex.

2. Set the port's speed explicitly to auto-negotiation (the documented example,
   p. 110) and confirm the switch's view:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port1"
   set speed auto
   set status up
   next
   end
   next
   end
   FSW # diagnose switch physical-ports list port1
   ```

3. PoE (POE and FPOE models only). Read the PoE budget and per-port state from
   both sides. The FortiLink Guide's syntax line omits `poe`, but its example
   reads `get switch-controller poe <switch> <port>` (p. 114); the summary
   command is from the FortiOS 8.0.1 CLI Reference (cross-check):

   ```text
   FSW # get switch poe inline
   FGT # get switch-controller poe <SWITCH_SN> port4
   FGT # diagnose switch-controller switch-info poe summary <SWITCH_SN>
   ```

   Disable PoE on `port4` (nothing is connected there yet), check, and enable it
   again:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port4"
   set poe-status disable
   next
   end
   next
   end
   FSW # get switch poe inline
   ```

   Then repeat the block with `set poe-status enable`. A PoE reset is
   `execute switch-controller poe-reset <switch> <port>` in the FortiLink Guide
   (p. 114) and `execute switch-controller switch-action poe reset <switch>
   <port>` in the FortiOS 8.0.1 CLI Reference; check with `?` on your build.

4. Run a cable test on the empty `port4` (it interrupts traffic on a port with a
   link, FortiLink Guide 7.6.7, p. 331). From the switch (FortiSwitchOS 7.6.7 CLI
   Reference, p. 363), and from the controller (FortiOS 8.0.1 CLI Reference,
   cross-check; the guide documents only the GUI, **Diagnostics and Tools >
   Cable Test**):

   ```text
   FSW # diagnose switch physical-ports cable-diag port4
   FGT # execute switch-controller switch-action cable-diag <SWITCH_SN> port4
   ```

   Predict the result. **Answer:** every pair `Open`, length 0 meters; the guide
   says an unconnected port reads `Open` with length 0.

5. Build the LAG. Connect endpoint A's second Ethernet port and a second cable
   so that endpoint A has one link to `port3` and one to `port4` (keep its
   `port1` link only if it has three ports; otherwise move the `port1` cable to
   `port3`). Configure the trunk on the controller (pp. 115–116):

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "lag-174"
   set type trunk
   set mode lacp-active
   set lacp-speed fast
   set members "port3" "port4"
   set vlan "fsw-users"
   set description "Lab 4.3 LAG to endpoint A"
   next
   end
   next
   end
   ```

6. Before the endpoint runs LACP, read the trunk on the switch (pp. 379–381):

   ```text
   FSW # diagnose switch trunk summary lag-174
   FSW # diagnose switch trunk list lag-174
   ```

   Predict the Status column and the member states. **Answer:** down, with the
   members listed as non-active (`BLOCK`): the documented examples of trunks
   without an LACP partner show `down(0/2)` and `BLOCK` (p. 381).

7. Bond the two endpoint ports with LACP. `<IF1>` and `<IF2>` are the endpoint
   ports cabled to `port3` and `port4`; the address is in `fsw-users` but
   outside the DHCP range:

   ```bash
   # endpoint A
   sudo ip link add bond0 type bond mode 802.3ad lacp_rate fast miimon 100
   sudo ip link set <IF1> down && sudo ip link set <IF1> master bond0
   sudo ip link set <IF2> down && sudo ip link set <IF2> master bond0
   sudo ip link set bond0 up
   sudo ip addr add 10.174.41.50/24 dev bond0
   cat /proc/net/bonding/bond0
   ping -c 3 10.174.41.1
   ```

8. Read the trunk again from the switch and from the controller (FortiOS 8.0.1
   CLI Reference, cross-check, for the controller command):

   ```text
   FSW # diagnose switch trunk summary lag-174
   FSW # diagnose switch trunk list lag-174
   FGT # diagnose switch-controller switch-info trunk status <SWITCH_SN> lag-174
   ```

   Expect `up(2/2)` and both members active. In `diagnose switch trunk list`,
   the LACP actor state letters decode as Active or Passive, Slow or Fast,
   Aggregatable or Individual, In sync or Out of sync, collection Enabled or
   Disabled, distribution Enabled or Disabled (p. 380). Unplug one cable and
   read the summary again: `up(1/2)`, and the ping keeps working.

9. Read the transceiver inventory. Use an SFP or QSFP port that holds a module
   (`<SFP_PORT>`, for example the FortiLink port if it is a fiber link);
   `status` shows values only for modules with digital diagnostics
   (FortiSwitchOS 7.6.7 CLI Reference, pp. 503–504). The controller command is
   from the FortiOS 8.0.1 CLI Reference (cross-check):

   ```text
   FSW # get switch modules summary
   FSW # get switch modules detail <SFP_PORT>
   FSW # get switch modules status <SFP_PORT>
   FGT # diagnose switch-controller switch-info modules summary <SWITCH_SN>
   ```

   In the GUI, **WiFi & Switch Controller > FortiSwitch Ports** shows the
   transceiver information per port (FortiLink Guide 7.6.7, p. 334). If no
   module is inserted, record that the summary lists none.

10. Remove the LAG and return endpoint A to `port1` alone:

    ```bash
    # endpoint A
    sudo ip link delete bond0
    ```

    ```text
    FGT # config switch-controller managed-switch
    edit <SWITCH_SN>
    config ports
    delete "lag-174"
    end
    next
    end
    FGT # show switch-controller managed-switch <SWITCH_SN>
    ```

    Record the VLAN settings `port3` and `port4` show after the trunk is
    deleted; the guide does not say whether former members return to the
    default VLAN settings. If they do not, set them back to
    `<DEFAULT_VLAN>` and the default allowed and untagged lists from Lab 4.2
    step 1. Re-cable endpoint A to `port1` and check its lease again (Lab 4.2
    step 4).

**Track 2:** If Lab 2.2's third outcome applies, run step 5 against
`S248EPTF18000000`, show the entry, and delete the trunk again (step 10's
controller block). Record whether FortiOS accepts a trunk on a switch that has
never joined. Otherwise do the read-and-predict only.

**Track 2: read-and-predict.**

1. The FortiLink Guide (p. 110) prints:

   ```text
   FortiGate-100F # diagnose switch-controller switch-info port-properties S524DF4K15000024 port18
   Vdom: root
   Switch: S524DF4K15000024
   Port: port18
   PoE : 802.3af/at,30.0W
   Connector : RJ45
   Speed : 10Mhalf/10Mfull/100Mhalf/100Mfull/1Gauto/auto
   ```

   Predict the most power this port can deliver, and whether `set speed
   10000full` is a sensible setting for it. **Answer:** 30.0 W (802.3af/at),
   and no: the speed list stops at 1 G auto on an RJ-45 connector.
2. The FortiLink Guide (p. 114) prints a PoE status:

   ```text
   # get switch-controller poe FS108D3W14000967 port6
   Port(6) Power:3.90W, Power-Status: Delivering Power
   Power-Up Mode: Normal Mode
   Remote Power Device Type: IEEE802.3AT PD
   Power Class: 4
   Defined Max Power: 30.0W, Priority:3
   ```

   Predict what happens to this device's power while the switch restarts.
   **Answer:** it loses power. Normal mode provides no PoE power while the
   switch restarts; `poe-port-power perpetual` keeps power through a soft reboot
   and `perpetual-fast` through a hard one (p. 114), on models that support
   perpetual PoE.
3. The FortiSwitchOS 7.6.7 CLI Reference (p. 503) prints, for an SFP port,
   `identifier SFP/SFP+`, `transceiver 1000-Base-T`, `length_cable 100 meter`,
   `vendor FINISAR CORP.`, `vendor_pn FCLF-8521-3`. Predict what kind of module
   this is. **Answer:** a copper SFP (1000BASE-T over up to 100 m of cable), not
   an optic, so `get switch modules status` would have no optical power values
   to show.
4. In `diagnose switch trunk summary` (p. 381), a row reads
   `8DN3X16000001-0 lacp-active(auto-isl) src-dst-ip ... up(1/1)`. Predict who
   created this trunk. **Answer:** the switch, automatically: `auto-isl` marks
   a trunk formed toward a FortiLink peer or another FortiSwitch (Lab 3.1), named
   after the peer's serial number.

**Expected result:** Track 1: you recorded `port1`'s properties and statistics;
on a PoE model, `poe-status disable` and `enable` changed `port4`'s state in
`get switch poe inline`; the cable test on the empty port read `Open`, length 0;
`lag-174` came up `up(2/2)` with LACP and survived the loss of one member;
the transceiver inventory is recorded (or recorded as empty); the LAG is gone and
endpoint A is back on `port1` with a lease. Track 2: the predictions are answered
(and the stand-in's trunk recorded, if accepted).

**Negative test:** Shut endpoint A's port from the controller and watch both
ends:

```text
FGT # config switch-controller managed-switch
edit <SWITCH_SN>
config ports
edit "port1"
set status down
next
end
next
end
FGT # diagnose switch-controller switch-info port-stats <SWITCH_SN> port1
```

`port-stats` reports the port as administratively down, endpoint A loses its
link, and its ping to `10.174.41.1` fails. Set `status up` again and confirm the
lease returns. Track 2: in read-and-predict item 1, `set speed 10000full` is the
negative case.

**Rollback:** Step 10 is the rollback for the LAG. Restore PoE to `enable` on
`port4`, and remove `port1`'s description and speed setting if you want the
defaults.

**Lab verified by:** *pending*

### Lab 4.4 — Split ports

**Objective:** Establish from the switch and the documentation that your switch
cannot split a port, and predict how a split port is configured, named, and paid
for on a model that can.

**Platform notes:** Read-and-predict on every option and both tracks: in the
FortiSwitchOS 7.6.7 feature matrix, split port is supported only in the 500
Series, 10xx, and 3032 columns, not on S1, S2, or S3 (note 5). Track 1 runs two
read-only checks on the switch and one rejected configuration on the
controller.

**Track 1:**

1. Ask the switch which ports are split, and list its ports and their speeds
   (FortiSwitchOS 7.6.7 CLI Reference, p. 506; FortiLink Guide 7.6.7, p. 110):

   ```text
   FSW # get switch phy-mode
   FSW # get switch physical-port
   FGT # diagnose switch-controller switch-info port-properties <SWITCH_SN>
   ```

   The reference documents `get switch phy-mode` with an FS-524D's output but
   does not say what a model without splittable ports prints; record what yours
   prints (an error, nothing, or a list).

2. Confirm from the speed lists that no port is a 40G or 100G QSFP port. A
   split needs such a port and a breakout cable (p. 119).

**Track 2:** No configuration. Do the read-and-predict.

**Track 2: read-and-predict.** (Track 1 does it too.)

1. Four switches: FS-108F, FS-248E-POE, FS-524D, FS-1048E. Predict which can
   split a port. **Answer:** the FS-524D (ports 29 and 30, as 4 x 10G) and the
   FS-1048E (ports 49–54, depending on its port configuration). The FS-108F
   (1xxE/1xxF column) and the FS-248E-POE (200 Series column) have a dash in the
   feature matrix (FortiLink Guide 7.6.7, p. 119; feature matrix note 5).
2. On an FS-524D, an administrator enters (FortiLink Guide 7.6.7, p. 122):

   ```text
   config switch phy-mode
   set port29-phy-mode 4x10G
   end
   ```

   and the switch answers:

   ```text
   This change will cause a ports to be added and removed, this will cause loss of configuration on
   removed ports. The system will have to reboot to apply this change.
   Do you want to continue? (y/n)y
   ```

   Predict what happens to `port29`'s configuration and what the controller must
   do. **Answer:** `port29` is removed and its configuration is lost; the switch
   reboots with four new ports. From FortiOS 7.2.0 the controller updates the
   switch's port list itself after the restart and logs the change; before 7.2.0
   the switch had to be deleted from the controller, rediscovered, and
   authorized again (pp. 119–121).
3. Before the change, `get switch phy-mode` printed
   `port29-phy-mode : 1x40G` (FortiSwitchOS 7.6.7 CLI Reference, p. 506).
   Predict the names of the new ports. **Answer:** `port29.1` to `port29.4`;
   split ports use `.x` (FortiLink Guide 7.6.7, p. 122).
4. A pre-provisioned entry for an FS-1048E lists `port49.1`. Predict whether the
   controller splits port 49 when the switch joins. **Answer:** no. Split ports
   are not configured for pre-configured FortiSwitch units (p. 119); split the
   port on the switch after it joins.
5. A 4 x 25G split on an FS-3032E links up with errors at the far end. Which
   port setting is worth checking? **Answer:** forward error correction
   (`fec-state`): Clause 74 FC-FEC for 25G subports, Clause 91 RS-FEC for 100G
   ports, with `detect-by-module` the default from FortiOS 7.4.2 on FEC-capable
   switches (pp. 121–122).

**Expected result:** Track 1 recorded what `get switch phy-mode` prints on its
model and that no port is a 40G or 100G QSFP port. Both tracks answered the five
predictions.

**Negative test:** Track 1: ask the controller for a split subport that does not
exist:

```text
FGT # config switch-controller managed-switch
edit <SWITCH_SN>
config ports
edit "port1.1"
next
end
next
end
FGT # show switch-controller managed-switch <SWITCH_SN>
```

Record whether FortiOS refuses `edit "port1.1"` or creates an entry; the
documentation does not say. If an entry was created, delete it
(`delete "port1.1"` under `config ports`); it matches no physical port. Track 2:
prediction 4 is the negative case.

**Rollback:** None, beyond deleting `port1.1` if it was created.

**Lab verified by:** *pending*

### Lab 4.5 — Routing between VLANs

**Objective:** Route between two lab VLANs on the FortiGate, control the traffic
with the zone's `intrazone` setting, trace the decision, and (on FortiOS 7.6.4
and later) give the switch an SVI and a static route; predict inter-VLAN routing
offload.

**Platform notes:** Part A is hands-on on C1, C2 (after a GO in Lab 4.1), and C3
with S1, S2, or S3; it adds no policy or route, so the C2 budget is unchanged.
Part B (switch SVI and static route) needs FortiOS 7.6.4 or later on the
controller: it is read-and-predict on FGT-1 (FortiOS 7.6.2, C2 and C3) and on
any C1 below 7.6.4. Inter-VLAN routing offload is read-and-predict on every
option (not supported on S1–S3, note 19). Track 2: build the zone change live and
read-and-predict the rest.

**Track 1, Part A — routing on the FortiGate:**

1. Check the routing table. Both networks are connected routes; no static route
   is needed:

   ```text
   FGT # get router info routing-table all
   ```

2. Trace a ping from endpoint A (`fsw-users`) to endpoint B (`fsw-iot`,
   `10.174.43.20`). Start the trace on the controller:

   ```text
   FGT # diagnose debug flow filter clear
   FGT # diagnose debug flow filter addr 10.174.43.20
   FGT # diagnose debug flow show function-name enable
   FGT # diagnose debug enable
   FGT # diagnose debug flow trace start 10
   ```

   ```bash
   # endpoint A
   ping -c 3 10.174.43.20
   ```

   ```text
   FGT # diagnose debug disable
   ```

   Predict the result. **Answer:** the ping fails. Both VLANs are in
   `FSW-LAN`, whose `intrazone` is `deny` (the default, FortiOS 7.6.0 CLI
   Reference, p. 1824), and no policy allows `fsw-users` to `fsw-iot`. The trace
   shows the route lookup succeed and the packet then denied by the policy
   check; record the exact message.

3. Allow traffic inside the zone and ping again:

   ```text
   FGT # config system zone
   edit "FSW-LAN"
   set intrazone allow
   next
   end
   ```

   ```bash
   # endpoint A
   ping -c 3 10.174.43.20
   ```

   Predict the TTL in the replies. **Answer:** one less than endpoint B's
   initial TTL (63 for a Linux host's default of 64): the FortiGate routed the
   packets between the VLANs. Watch them cross the FortiLink port in both VLANs
   (FortiOS 8.0.1 CLI Reference, cross-check):

   ```text
   FGT # diagnose sniffer packet any 'icmp and host 10.174.43.20' 4 6
   ```

4. Return the zone to `deny`. The rest of the volume keeps the lab VLANs apart:

   ```text
   FGT # config system zone
   edit "FSW-LAN"
   set intrazone deny
   next
   end
   ```

   On C1 and C3, a firewall policy from `FSW-LAN` to `FSW-LAN`, with address
   objects for the two subnets, would allow the same traffic selectively (once
   interfaces are zone members, policies name the zone, not the interfaces);
   on C2 it would take slot P3, which the zone setting does not.

**Track 1, Part B — the switch routes (FortiOS 7.6.4 and later only):**

The commands below are from the FortiLink Guide 7.6.7 (pp. 152–157). They are
not in the FortiOS 7.6.0 CLI Reference; type `?` inside the switch's entry to
check that your build offers them. Run them only if `get system status` shows
FortiOS 7.6.4 or later.

1. Give the switch an SVI in `fsw-tenant` and a static route back to
   `fsw-users` through the FortiGate (IPv4 only in managed mode, note 9):

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config system-interface
   edit "svi-1745"
   set switch-id <SWITCH_SN>
   set mode static
   set ip 10.174.45.2 255.255.255.0
   set allowaccess ping
   set vlan "fsw-tenant"
   set type vlan
   set status enable
   next
   end
   config router-static
   edit 1
   set switch-id <SWITCH_SN>
   set device "svi-1745"
   set dst 10.174.41.0 255.255.255.0
   set gateway 10.174.45.1
   next
   end
   next
   end
   ```

2. Check the switch's routing table and ping the SVI from the controller,
   first from `fsw-tenant`'s own address and then sourced from `fsw-users`'
   address (`execute ping-options source`, FortiOS 8.0.1 CLI Reference,
   cross-check):

   ```text
   FSW # get router info routing-table all
   FGT # execute ping 10.174.45.2
   FGT # execute ping-options source 10.174.41.1
   FGT # execute ping 10.174.45.2
   FGT # execute ping-options reset
   ```

   The first ping is Layer 2 within `fsw-tenant`. The second needs the switch's
   static route for the reply. The guide does not describe how a managed
   switch's own routes interact with its FortiLink management route; record
   both results and the route the switch shows for `10.174.41.0/24`.

3. Remove the SVI and the route:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config router-static
   delete 1
   end
   config system-interface
   delete "svi-1745"
   end
   next
   end
   ```

**Track 2:** Run Part A steps 3 and 4 (the zone change and its return) and
check each with `show system zone FSW-LAN`. Run Part A step 1 and record which
lab networks are listed while the FortiLink port has no link.

**Track 2: read-and-predict.** (Track 1 does items 2 and 3 too; on a controller
below 7.6.4, also item 1.)

1. The FortiLink Guide (pp. 156–157) prints a static route on a managed switch:

   ```text
   config router-static
   edit 1
   set switch-id "S524DN4K16000116"
   set device "rvi22"
   set dst 10.5.5.6 255.255.255.255
   set gateway 10.2.2.1
   next
   end
   ```

   Predict which device holds this route, and why the entry repeats the serial
   number. **Answer:** the FortiSwitch `S524DN4K16000116`, not the FortiGate; it
   is configured under the switch's managed-switch entry, and the guide marks
   `switch-id` as required and equal to the entry's serial (p. 156). On the
   FortiGate it does not count as one of the evaluation's three routes, because
   it is switch configuration, not `config router static` (the evaluation page
   does not say either way; this is a reading of where the route lives).
2. The guide's offload example (pp. 107–108) gives `vlan.10` the address
   `192.168.10.1/24`, `switch-controller-offload-ip 192.168.10.2`, and
   `switch-controller-offload-gw enable`. Predict which address the hosts in
   VLAN 10 use as their gateway, and where their traffic to VLAN 20 is routed.
   **Answer:** `192.168.10.2`, the offload address, so traffic between VLAN 10
   and VLAN 20 is routed on the FortiSwitch closest to the FortiGate that
   supports offload, without FortiGate inspection. The FortiGate creates an SVI
   per VLAN on the switch and a default route in `vrf1` toward `192.168.10.1`
   (the gateway VLAN's FortiGate address) with `gw-l2-switch` enabled
   (pp. 106–108).
3. Predict whether an FS-124F with an advanced features license can run that
   example. **Answer:** no. Inter-VLAN routing offload has a dash in the 1xxE/1xxF
   column of the 7.6.7 feature matrix and is supported only in the 10xx, 2048F,
   and 3032 columns; the license (note 19) is necessary but not sufficient.

**Expected result:** Track 1 Part A: the routing table lists both networks as
connected; with `intrazone deny` the ping failed and the trace showed a policy
denial; with `intrazone allow` it succeeded with TTL reduced by one; the zone is
back at `deny`. Part B (7.6.4 and later): the switch listed its SVI and static
route, both pings are recorded, and both objects are removed. Track 2: the zone
change and the routing-table observation are recorded, and the three predictions
answered.

**Negative test:** Part A step 2 is the negative test: with the default
`intrazone deny`, traffic between two VLANs of the same zone is dropped although
the FortiGate has a route for both. Track 2: prediction 3.

**Rollback:** Make sure `FSW-LAN` reads `intrazone deny`; on FortiOS 7.6.4 and
later, Part B step 3. Lab 4.5 leaves nothing else behind.

**Lab verified by:** *pending*

## Lab Verification

Complete this sign-off once Labs 4.1 to 4.5 have been run end to end, including
each negative test and, on C2, the interface-cap test of Lab 4.1. Until then,
the labs are unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

FortiSwitch VLANs are VLAN interfaces on the FortiLink interface; the FortiGate
holds their addresses, DHCP, routing, and policy, and the switch forwards them at
Layer 2. A port's native VLAN takes untagged frames, its allowed list admits
tagged ones, and its untagged list strips tags on egress; `append` keeps the
`quarantine` VLAN that every port needs. On a FortiSwitch, a trunk is a LAG.
Port properties, statistics, PoE, cable tests, and transceiver data are readable
from both the controller and the switch. Split ports and inter-VLAN routing
offload belong to larger models than S1–S3, and the switch's own SVIs and static
routes come from the controller only in FortiOS 7.6.4 and later. The lab ends
with five lab VLANs, `FSW-LAN` (`intrazone deny`) in the sources of P1 and P2,
endpoint A on `fsw-users`, and endpoint B on `fsw-iot`.

- [ ] I created the five lab VLANs (or recorded the C2 interface-cap result),
      the DHCP server on `fsw-users`, and the zone `FSW-LAN`.
- [ ] `FSW-LAN` is in the sources of P1 and P2, and no policy slot was added
      on C2.
- [ ] Endpoint A has a lease in `fsw-users`; endpoint B reaches `10.174.43.1`.
- [ ] I carried a tagged VLAN on `port1` with `append` and restored the
      original allowed list.
- [ ] I read port properties and statistics, ran a cable test, and (on a PoE
      model) toggled PoE.
- [ ] I built `lag-174` with LACP, saw it come up and survive a member loss, and
      removed it.
- [ ] I recorded the transceiver inventory.
- [ ] I can name the models that split ports and explain what a `phy-mode`
      change costs.
- [ ] I routed between two lab VLANs on the FortiGate with `intrazone allow`,
      traced the denial with `intrazone deny`, and left the zone at `deny`.
- [ ] I can explain why S1–S3 cannot offload inter-VLAN routing.
