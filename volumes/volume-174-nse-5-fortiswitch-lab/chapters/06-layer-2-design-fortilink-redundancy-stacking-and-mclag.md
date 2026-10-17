# Chapter 06: Layer 2 Design: FortiLink Redundancy, Stacking, and MCLAG

## Learning Objectives

- Name the FortiLink topologies that the FortiLink Guide 7.6.7 documents, from a
  single FortiGate with a single switch to HA FortiGates with tiered MCLAG, and
  the FortiLink interface type that each one needs.
- Explain the three ways to make the FortiLink link itself redundant (a
  FortiLink LAG to one switch, a dual-homed active/standby FortiLink with the
  **FortiLink split interface**, and a FortiLink MCLAG), and say honestly which
  of them each controller option (C1, C2, C3) can build.
- Identify the ports a stack deployment needs (exam task 1.3): the FortiGate's
  FortiLink ports, the switch's auto-FortiLink ports, inter-switch link (ISL)
  ports, and inter-chassis link (ICL) ports, and how auto-ISL forms them.
- Add a second FortiSwitch to the stack over an automatic ISL, authorize it,
  bind it to the lab's switch profile, and keep it in the lab's MST region.
- Form an MCLAG peer group on two 200 Series switches from the FortiGate, read
  the ICL from the controller and the switch, and build an MCLAG trunk; state
  the MCLAG requirements and why S1 and S2 cannot run it.
- Choose a topology for a given site: HA FortiGates, FortiLink over a
  point-to-point Layer 2 network, FortiSwitch islands over Layer 3 and their
  limits, VXLAN management, and interconnected FortiLink fabrics.

## Theory and Architecture

### The managed switches are one Layer 2 stack

The FortiLink Guide calls the set of switches that one FortiLink interface
manages a **stack**. Whatever the topology, the managed switches work as one
Layer 2 stack in which the FortiGate manages each switch separately, and the
active FortiLink carries data as well as management traffic. The FortiLink
interface can be a physical interface or a logical one built on several
physical ports, and some topologies add a standby FortiLink (FortiLink Guide
7.6.7, p. 54). This is not stacking in the chassis sense: there is no stacking
cable and no shared control plane, only switches joined by trunks and each
managed by the controller.

The links in a stack have names that the exam and the diagnostics use:

| Link | Between | How it forms | Where you see it |
| --- | --- | --- | --- |
| **FortiLink** | The FortiGate's FortiLink interface and the first switch | Discovery on an auto-FortiLink port (Chapter 03) | Switch trunk with mode `lacp-active(auto-isl)`, named after the FortiGate's serial (Lab 3.1) |
| **ISL** (inter-switch link) | Two managed switches | Automatically: after a switch is in FortiLink mode, every port is enabled for FortiLink, and a second switch cabled to any port forms an ISL and is discovered (p. 31) | Switch trunk with mode `lacp-active(auto-isl)`, named after the peer switch's serial |
| **Static ISL** | Two switches | Created by hand (`set static-isl enable` under `config switch trunk`), for example for FortiLink over Layer 2 or Layer 3 networks, or to lock down an automatic topology (p. 31) | `static-isl` in the trunk |
| **ICL** (inter-chassis link) | The two switches of an MCLAG peer group | An ISL whose ports get the LLDP profile `default-auto-mclag-icl` (pp. 86–87) | Switch trunk with mode `lacp-active(mclag-icl)` (FortiSwitchOS 7.6.7 CLI Reference, pp. 379–381) |
| **MCLAG trunk** | A downstream device and both MCLAG peers | Configured, or formed automatically toward access switches once the peer group exists (p. 76) | Trunk mode `(mclag)` |

The trunk names are documented only by example: the automatically formed trunk
`8DN3X16000001-0` in the CLI Reference (p. 381) and `8EPTF18001384-0` in the
guide (p. 48) are the peer's serial without its first three characters, plus
`-0`; the ICL in the guide's upgrade example is `_FlInK1_ICL0_` (p. 99).
Record the names your switches use.

### Auto-ISL and the LLDP profiles

A managed switch decides whether a port may form an ISL from the port's **LLDP
profile**. Three profiles matter in this chapter:

| LLDP profile | Effect on the port | Source |
| --- | --- | --- |
| `default-auto-isl` | Automatic ISL allowed; the FortiOS 7.6.0 default for every managed port (`lldp-profile` under `config ports`) | FortiOS 7.6.0 CLI Reference |
| `default-auto-mclag-icl` | Turns the ports between two switches into an MCLAG ICL | FortiLink Guide 7.6.7, pp. 86–87 |
| `default` | The profile the guide uses on links between two separately managed fabrics, where no ISL must form, and the one Security Rating suggests for edge ports | pp. 96, 276 |

On the controller, `config switch-controller lldp-profile` holds `auto-isl`,
`auto-isl-hello-timer` (default 3 seconds), `auto-isl-port-group` (0–9),
`auto-isl-receive-timeout`, and `auto-mclag-icl` (FortiLink Guide 7.6.7,
pp. 172–173; FortiOS 7.6.0 CLI Reference). Two cautions: the FortiOS 7.6.0 CLI
Reference prints the option descriptions of `auto-isl` and `auto-mclag-icl`
swapped (its `auto-isl` entry describes "MCLAG inter chassis link"), and gives
`auto-isl-receive-timeout` a default of 60 in its table while the description
says 9, which is also the guide's figure. Read them with `show` or `get` on your
build rather than trusting either line. This chapter does not change any LLDP
profile except to form the ICL in Lab 6.3 and for one negative test.

### The FortiLink interface types

| FortiLink interface type | What it is | When the guide uses it |
| --- | --- | --- |
| Physical port | One FortiGate port | Single FortiGate, single switch or a stack below one switch (pp. 55–56) |
| 802.3ad aggregate | Several FortiGate ports as one LAG; the **default** FortiLink type, which Fortinet recommends keeping | FortiLink LAG, dual-homed FortiLink, FortiLink MCLAG (pp. 23, 26–27, 85–88) |
| Hardware switch | FortiGate ports switched in hardware; created instead of an aggregate on models that lack aggregates | Several switches each on one FortiGate port (p. 60); HA with STP on the FortiLink interface (p. 61, Chapter 05) |
| Software switch | Ports bridged in software | p. 60 says it is not recommended in most cases, because all traffic between switches crosses the FortiGate; p. 61 says it is not supported for the HA STP design |
| VXLAN | A VXLAN interface with `fortilink enable` | Management over a Layer 3 network (pp. 69–74) |

FortiLink is supported on every Ethernet port except HA and MGMT ports (p. 25),
and an aggregate FortiLink interface name has at most 11 characters (p. 26).

### Three ways to make FortiLink redundant

| Design | Cabling | FortiGate settings | What happens | Guide |
| --- | --- | --- | --- | --- |
| **FortiLink LAG** | Two or more aggregate members to the **same** switch | `type aggregate`; `fortilink-split-interface disable` | One LACP trunk; all members carry traffic; a member can fail | p. 27: if the members connect to the same switch, you **must** disable the split interface |
| **Dual-homed (active/standby)** | Exactly two members, one to the first switch and one to another switch of the stack (often the last) | `fortilink-split-interface enable`; `lacp-mode active` | One link is active and the other standby, which avoids a loop through the ISL | pp. 23, 56, 58 |
| **FortiLink MCLAG** | One or more members to each of two MCLAG peers | Form the ICL first; then `fortilink-split-interface disable`; `lacp-mode active` | Both links active, terminating on an MCLAG | pp. 85–88 |

The split interface has three more documented details. It is **enabled by
default** (p. 23; the FortiOS 7.6.0 CLI Reference also gives `enable`), although
the guide's own example of a factory `fortilink` aggregate shows `set
fortilink-split-interface disable` (p. 29), so read your controller's value. With
the split interface enabled, the standby link is **down** when neighbor
detection is `fortilink` and **up with LACP inactive** when it is `lldp`
(p. 24); this volume uses `lldp` (Chapter 02). And the order matters both ways:
the split interface must be enabled **before** MCLAG is enabled on the
switches, and if you later disable the MCLAG ICL you must enable the split
interface again (pp. 23, 88). The read-only `fortilink-backup-link` field of
`config system interface` is described as the "FortiLink split interface backup
link" (FortiOS 7.6.0 CLI Reference).

HA FortiGates add a fourth dimension: both cluster members connect FortiLink to
the first switch (and optionally to the last) with matching FortiLink ports and
interface types (pp. 57–59). This volume has no FortiGate cluster, so HA designs
are Lab 6.4's design exercise.

### What each controller option can build

Redundant FortiLink needs a FortiLink interface with two ports in it. That is a
property of the controller, not of the switch:

| Controller | FortiLink interface today | FortiLink LAG / dual-homed / MCLAG FortiLink | Why |
| --- | --- | --- | --- |
| **C1** with the factory `fortilink` interface of type `aggregate` | Aggregate (Chapter 02 used it as `<FL_PORT>` if it existed) | **Hands-on.** Add a second member (or cable one that is already a member) | Adding a member to an existing aggregate keeps every reference (VLAN interfaces, DHCP servers, zone, policies) in place |
| **C1** with a plain physical `<FL_PORT>`, or a factory `fortilink` of type hardware switch | Physical port or hardware switch | **Read-and-predict** | A physical interface cannot become an aggregate; you would have to build a new aggregate FortiLink interface and move every object that refers to the old one (the five lab VLAN interfaces and their DHCP servers, the auto-created VLANs, `FSW-LAN`, P1, P2). This volume does not do that. A hardware switch has no split interface |
| **C2** (FGT-1 evaluation) | `port3`, physical | **Read-and-predict** | A second FortiLink port would be a fourth interface; the evaluation allows three (Chapter 01) |
| **C3** (licensed FortiGate-VM) | `port4`, physical | **Read-and-predict** | The same rebuild as a physical C1 port. In addition, the references used for this volume do not say whether FortiOS 7.6 on a FortiGate-VM builds an 802.3ad aggregate with LACP, and Chapter 02's `vmbrFL` bridge forwards LLDP only (`group_fwd_mask` 16384): LACP frames go to `01:80:C2:00:00:02`, and the Linux bridge code does not allow the low three group-address bits (STP, pause, slow protocols) to be set in `group_fwd_mask`. A C3 FortiLink LAG would need two passed-through NIC ports and an aggregate rebuilt from scratch |

The switch side is not the limit for a FortiLink LAG: the guide says LAG is
supported on all FortiSwitch models (p. 26), and the feature matrix gives a LAG
size of 8 for the 1xxE/1xxF and 200 Series columns. So C1 with an aggregate can
build a FortiLink LAG on S1, S2, or S3. The **dual-homed** design needs a second
switch in the stack, and the **FortiLink MCLAG** needs an MCLAG peer group,
which only S3 supports.

### MCLAG

A multichassis LAG groups two FortiSwitch units so that they appear to the
network as one switch; if either fails, the MCLAG keeps working without the
delays of spanning tree (FortiLink Guide 7.6.7, p. 85). The **MCLAG peer
group** is the pair joined by the ICL; **MCLAG trunks** are LAGs whose members
belong to different peers (p. 116).

The documented requirements (pp. 85–86):

- At least two links for the ICL.
- Devices that connect to an MCLAG peer group use an 802.3ad aggregate to both
  peers.
- At most two switches per MCLAG; both should be the same hardware model and
  the same software version. Mismatched configurations might work but are
  unsupported.
- The routing feature is not available within an MCLAG.
- `min_bundle` and `max_bundle` apply only to the local aggregate.
- On the switch, `mclag-stp-aware` must be enabled and STP must be enabled on
  all ICL trunks; both are on by default.
- For IGMP snooping in an MCLAG, `mclag-igmpsnooping-aware` must be enabled, and
  the flood settings `mcast-snooping-flood-traffic` and
  `igmp-snooping-flood-reports` must be disabled on ISL and FortiLink trunks and
  enabled on ICL trunks. The guide says `mclag-igmpsnooping-aware` is enabled by
  default; the FortiSwitchOS 7.6.7 CLI Reference gives its default as `disable`
  (`config switch global`, p. 118). Chapter 09 checks it before IGMP snooping.

An MCLAG trunk is configured on **each** peer with the **same trunk name**; the
member ports may differ, and LACP can be enabled after MCLAG (p. 117). LACP
fallback mode must not be configured on both MCLAG peers (p. 118).

The switch-side MCLAG options in `config switch global` are
`mclag-stp-aware` (default `enable`), `mclag-split-brain-detect` (default
`disable`), `mclag-split-brain-priority` (0–100, default 50; the lower priority
goes dormant, and on a tie the lower MAC address), and
`mclag-split-brain-all-ports-down` (FortiSwitchOS 7.6.7 CLI Reference,
pp. 118–119). `diagnose switch mclag icl` prints the ICL, its ports, the local and
peer MAC addresses and serials, `MCLAG-STP-mac`, the keepalive interval (1) and
timeout (60), the dormant candidate, and the split-brain state (p. 357).

**Tiers.** MCLAG can be deployed in up to three tiers (p. 83). Tier 1 is the
core pair, formed as above. For tier 2 and tier 3, the upper pair needs an
`auto-isl-port-group` for each lower pair, configured **directly on the
switch** (`config switch auto-isl-port-group`), or by binding a custom command
from the FortiGate, so that the ports to the two lower peers are grouped into
one MCLAG when the ISLs form (pp. 90–92; FortiSwitchOS 7.6.7 CLI Reference,
p. 113). Fortinet recommends at least one link from each lower-tier peer to
each of its two upper-tier switches (fully meshed tiers), which also lets
Security Rating detect possible tier-2 and tier-3 MCLAGs (p. 83).

**Upgrades.** The guide's procedure for an MCLAG pair (impact within 5 seconds)
is: disable split-brain protection if it is on, find the switch with the lower
MAC address with `diagnose switch mclag icl`, stage the image on both, restart
the lower-MAC switch, wait until its links are up, restart the other, and
re-enable split-brain protection (pp. 99–100).

### Model support for this chapter

From the FortiSwitchOS 7.6.7 feature matrix (`temp/nse5fsw/fm767.txt`); chain =
standalone and managed mode, check = standalone only, dash = not supported:

| Feature | 1xxE/1xxF (S1 FS-108F, S2 FS-124F) | 200 Series (S3) | Note |
| --- | --- | --- | --- |
| Auto topology | Chain | Chain | Automatic ISL formation |
| Link aggregation group size | 8 | 8 | |
| LAG min-max bundle, LACP fallback mode | Chain | Chain | |
| MCLAG | Dash | Chain | GUI column: Partial |
| STP supported in MCLAGs | Dash | Chain | |
| IGMP snooping support in MCLAG | Dash | Chain | |
| FortiLink management over VXLAN | Dash | Dash | Only some larger models (4xxE, 500, 10xx, 2048F, 3032, FSR-424F) |
| FortiSwitch VLANs over VXLAN | Dash | Dash | Larger models only |

So on S1 and S2, MCLAG and STP in MCLAG are read-and-predict. Stacking (auto-ISL)
works on every model, so a second switch of any model makes Lab 6.2 hands-on.
The guide adds two model notes: the FS-124E/F and FS-148E/F families support
only the default `0x8100` TPID for FortiLink over a point-to-point Layer 2
network (p. 62), and Security Rating recommends a custom auto-config policy when
`port8` of an FS-108F is used for an ISL (p. 277), which is why this chapter
uses `port4` for the S1 ISL.

## Design Considerations

### Which ports this chapter uses

Chapter 01's reserved ports stay untouched: `port1` and `port2` (endpoints, with
BPDU guard since Chapter 05), `port5` and `port6` (loop cable, still loose at one
end), `<FSW_FL_PORT>`, and `port3` (temporary in-band management on models
without a MGMT port). The new cables:

| Placeholder | Use | S1 FS-108F | S2 FS-124F | S3 FS-224E | S3 FS-248E |
| --- | --- | --- | --- | --- | --- |
| `<FL_PORT2>` | C1 only: the second member of the `fortilink` aggregate | A member of `fortilink` not yet cabled, or a free port removed from the `lan` hardware switch | same | same | same |
| `<FSW_FL_PORT2>` | Second FortiLink port on `FSW-A` (Lab 6.1) | `port8` | `port22` | `port22` | `port46` |
| `<ISL_PORT>` | `FSW-A` end of the ISL to the second switch | `port4` | `port23` | `port23` | `port23` |
| `<FSWB_ISL_PORT>` | Second switch end of the ISL; a default auto-FortiLink port of that model (Chapter 02 table) | — | — | `port23` | `port47` |
| `port24` / `<FSWB_ICL_PORT2>` | Second ICL link (Lab 6.3, S3 only) | — | — | `port24` / `port24` | `port24` / `port48` |
| `<FSWB_FL_PORT>` | C1 only: `FSW-B` end of the dual-homed FortiLink (Labs 6.2, 6.3) | — | — | `port21` | `port45` |

On S1 or S2, a second switch of any model can be the ISL peer in Lab 6.2: cable
`<ISL_PORT>` to one of that model's default auto-FortiLink ports (FortiLink
Guide 7.6.7, pp. 30–31). Every port pair above must match in media and speed.

### Keep the second switch in the region

The global `stp-settings` (region `lab-174`, revision 1) and `stp-instance` 1 (the
four `FSW-LAN` VLANs) apply to every managed switch, so `FSW-B` receives the same
region name, revision, and map as soon as it is authorized; that is why
Chapter 05 put them in global settings. Two things would split the region, and
this chapter does neither: a per-switch `config stp-settings` with
`local-override enable` and a different revision on either switch (Chapter 05,
Lab 5.3), and a per-switch instance map. `FSW-A`'s instance 1 priority of 16384
(Lab 5.1) beats `FSW-B`'s default 32768, so `FSW-A` stays the instance 1 root.
Instance 0 is decided by the two switches' instance 0 priorities and then their
MAC addresses, which the lab records rather than sets.

### MCLAG needs matching switches and builds

Both MCLAG peers should be the same model on the same FortiSwitchOS build
(p. 85). Lab 2.4 upgraded `FSW-B` to a 7.6.x build, but Lab 3.3 may have moved
`FSW-A` to a different one. Lab 6.2 compares the two and pushes `FSW-A`'s build
to `FSW-B` from the controller if they differ. An FS-224E paired with an FS-248E
is a mismatched pair: it may work, but it is unsupported, so record it as such.

### What to keep after this chapter

| Object | Kept | Why |
| --- | --- | --- |
| S3: `FSW-B` (`<FSWB_SN>`) authorized, description `FSW-B lab-174`, profile `fsw-174-prof`, same build as `FSW-A` | Yes | Later chapters may use the pair (FortiLink-mode ACLs and IP source guard in Chapter 08) |
| S3: ICL between `FSW-A` `port23`/`port24` and `FSW-B` `<FSWB_ISL_PORT>`/`<FSWB_ICL_PORT2>`, ports on `default-auto-mclag-icl` | Yes | The MCLAG peer group is the S3 baseline |
| S3: `FSW-B` in region `lab-174` revision 1; `FSW-A` instance 1 root | Yes | Chapter 07 keeps its VLANs in instance 1 |
| MCLAG test trunk `mclag-ep-174` | No | Lab 6.3 deletes it |
| C1: second FortiLink member and the dual-homed cable | No | Lab 6.3's rollback returns FortiLink to one cable; Chapter 12's fault clinic and teardown start from one link |
| S1 or S2: a borrowed second switch | No | Lab 6.2 retires it; later chapters use one switch |
| `FSW-A` ports `port1`–`port6`, `<FSW_FL_PORT>` | Unchanged | As Chapter 05 left them |

No firewall policy, route, or FortiGate interface is added, so the C2 budget is
unchanged (P1 and P2 used, P3 free). On C1 the aggregate gains a member for the
duration of the labs only.

## Implementation and Automation

The labs are the implementation. Three habits help.

**Read the stack from both ends.** The controller shows the stack and the
physical graph; each switch shows its own trunks:

```text
FGT # execute switch-controller get-conn-status
FGT # execute switch-controller get-physical-conn standard port3
FGT # diagnose switch-controller switch-info lldp neighbors-summary <SWITCH_SN>
FSW # diagnose switch trunk summary
```

**Keep a ping running** from endpoint A to its gateway during every cabling
change, so each link failure and recovery has a measured cost:

```bash
# endpoint A
ping -O 10.174.41.1
```

**Change the order, not just the settings.** Split interface before MCLAG, ICL
before disabling the split interface, split interface back on before the ICL is
removed. Each lab says which step must come first.

The FortiOS configuration commands in this chapter were checked against the
FortiOS 7.6.0 CLI Reference; `execute`, `diagnose`, and `get` commands against
the FortiLink Guide 7.6.7, or against the FortiOS 8.0.1 CLI Reference as a
cross-check where the guide prints no syntax line (marked in each case). Switch
commands were checked against the FortiSwitchOS 7.6.7 CLI Reference; two take
an optional or bracketed argument and were matched by hand to its syntax lines:
`get switch lldp auto-isl-status <port>` (p. 499, also in the FortiLink Guide,
p. 182) and `diagnose switch trunk summary [<trunk_name>]` (p. 381). The
FortiLink Guide also prints `execute switch-controller get-physical-conn {dot |
standard} <FortiLink_interface>` (p. 181).

## Validation and Troubleshooting

| Symptom | Likely cause | Check |
| --- | --- | --- |
| The second switch never appears in `get-conn-status` | The ISL did not form: cable on a port whose LLDP profile is not auto-ISL, a media mismatch, or the switch is not at factory defaults | `diagnose switch trunk summary` on `FSW-A`; `get switch lldp auto-isl-status <port>`; reset the new switch |
| The second switch is `Discovered/Down` | Automatic authorization is off (this volume's setting) | Authorize it (Lab 6.2) |
| FortiLink LAG shows only one member in the switch trunk | Split interface still enabled with both members on the same switch | `get system interface fortilink`; set `fortilink-split-interface disable` (p. 27) |
| Dual-homed FortiLink: both links forward and broadcasts loop | Split interface disabled without an MCLAG ICL | Enable the split interface at once (pp. 56, 88) |
| The standby FortiLink link shows link up | Expected with `lldp` neighbor detection: up, LACP inactive (p. 24) | `diagnose netlink aggregate name fortilink` |
| The ICL does not form | ICL ports not on `default-auto-mclag-icl` on both switches, a model without MCLAG, or mismatched builds | `diagnose switch-controller switch-info mclag icl`; `get-conn-status` VERSION |
| An MCLAG trunk works on one peer only | Different trunk names on the two peers | `diagnose switch mclag peer-consistency-check` |
| The two switches each claim to be root of instance 1 | They are in different regions | `diagnose stp mst-config list` on each; compare name, revision, digest |
| The controller loses `FSW-B` when one cable is pulled | Only one ISL or ICL link | Add the second link; Security Rating flags single ISLs (p. 275) |

## Security and Best Practices

- **Use at least two links between switches.** The guide asks for two ICL links,
  and Security Rating fails an ISL with a single link and a directly connected
  switch without redundant FortiLinks (pp. 85, 274–275).
- **Lock down the topology once it is stable.** Static ISLs (Lockdown ISL in the
  GUI) keep an automatically formed ISL or ICL from being deleted by accident,
  and Security Rating recommends it; edge ports should use the `default` LLDP
  profile so a switch plugged into an access port cannot join the stack
  (pp. 31–33, 276–278). This lab leaves the topology unlocked so that it can be
  rebuilt; lock a production stack.
- **Never disable the split interface without an MCLAG.** It is the only thing
  that stops a dual-homed FortiLink from forming a loop through the ISL.
- **Do not put the FortiGate in a ring.** The guide's stack topologies say
  plainly: do not create loops or rings with the FortiGate unit in the path
  (pp. 56, 60).
- **Match MCLAG peers.** Same model, same build, and the same trunk names;
  upgrade them one at a time in the documented order.
- **Keep BPDU guard on host ports.** Adding switches multiplies the number of
  ports where a rogue bridge can appear; only ISL, ICL, and FortiLink ports
  should run without edge protection.

## References and Knowledge Checks

**References**

- [Fortinet, *FortiLink Guide (FortiOS 7.6.7)*](https://docs.fortinet.com/document/fortiswitch/7.6.7/fortilink-guide)
  — supported models and limits (p. 12), FortiLink interface types and the split
  interface (pp. 23–24), custom FortiLink interfaces, FortiLink LAG
  (pp. 25–27), auto-discovery ports, automatic and static ISLs, lockdown
  (pp. 30–33), auto-config policies (pp. 44–45), automatically formed trunks
  (p. 48), determining the network topology (pp. 54–74), switch redundancy with
  MCLAG (pp. 75–84), MCLAG peer groups, requirements, transitioning from a split
  interface to an MCLAG, deploying and upgrading MCLAG topologies (pp. 85–100),
  trunks and MCLAG trunks (pp. 115–118), LLDP profiles (pp. 172–173), LLDP
  display commands (p. 176), physical connections (p. 181), Security Rating
  FortiSwitch tests (pp. 274–278), stacked firmware example (p. 345).
- [Fortinet, *FortiSwitchOS 7.6.7 CLI Reference*](https://docs.fortinet.com/document/fortiswitch/7.6.7/fortiswitchos-cli-reference)
  — `config switch auto-isl-port-group` (p. 113), `config switch global`
  MCLAG options (pp. 118–119), `config switch trunk` (pp. 179–180),
  `diagnose switch mclag` (pp. 356–357), `diagnose switch trunk list` and
  `summary` (pp. 379–381), `get switch lldp` (p. 499).
- [Fortinet, FortiOS 7.6 documentation](https://docs.fortinet.com/product/fortigate/7.6)
  — FortiOS 7.6.0 CLI Reference: `config system interface` (`type`, `member`,
  `fortilink-split-interface`, `fortilink-backup-link`, `lacp-mode`),
  `config system virtual-switch`, `config switch-controller managed-switch`
  (`ports`: `lldp-profile`, `type`, `mode`, `members`, `mclag`),
  `config switch-controller lldp-profile`.
- FortiOS 8.0.1 CLI Reference (cross-check only) — `diagnose netlink aggregate
  name`, `execute switch-controller get-physical-conn`.
- FortiSwitchOS 7.6.7 feature matrix (`temp/fsw/FSW-7.6.7-Feature-Matrix.pdf`)
  — auto topology, LAG size, MCLAG, STP and IGMP snooping in MCLAG, VXLAN
  management.

**Knowledge checks**

1. A FortiGate's aggregate FortiLink interface has two members, both cabled to
   the same switch. Which split-interface setting is required, and why?
2. With the split interface enabled and neighbor detection `lldp`, what state is
   the standby link in? With `fortilink`?
3. Why can C1 with a factory `fortilink` aggregate build a FortiLink LAG while C2
   cannot, and what stands in C3's way?
4. A second switch is cabled to `port23` of a managed switch. What forms, what
   does the controller show, and what must the administrator do in this volume?
5. Name four MCLAG requirements from the FortiLink Guide.
6. In what order do you enable the split interface, form the ICL, and disable the
   split interface to reach a FortiLink MCLAG, and what must happen first when
   the ICL is removed?
7. Why must `auto-isl-port-group` be configured on the switch, not the
   FortiGate, in a tiered MCLAG, and on which tier?
8. Name three limitations of FortiSwitch islands managed over a Layer 3 network.

## Hands-On Lab

**Shared prerequisites.** Chapter 05 complete: `<SWITCH_SN>` (`FSW-A`)
`Authorized/Up` at `10.255.1.2` with `fsw-174-prof`; region `lab-174` revision 1,
instance 1 = the four `FSW-LAN` VLANs with priority 16384 on `FSW-A`; `port1` and
`port2` with BPDU guard; the loop cable in `port5` only. S3: `FSW-B` upgraded in
Lab 2.4, at factory defaults with your recorded admin password, not cabled. S1
or S2: optionally a second FortiSwitch of any model, prepared like Lab 2.4
(FortiSwitchOS 7.6.x, factory defaults, admin password set). A console cable.
Patch cables: one for Lab 6.1 (C1), one or two for Lab 6.2, one more for Lab 6.3.
Track 2: the Lab 2.2 pre-provisioning outcome. **Cost:** patch cables; a second
switch only if you add one.

As in earlier chapters, `FGT #` is the controller on any option, and blocks
written for `port3` apply to C3 with `port4` and to C1 with `<FL_PORT>` (the
factory `fortilink` interface if you used it). `<SWITCH_SN>` is `FSW-A`'s serial;
`<FSWB_SN>` is the second switch's serial; port placeholders are in Design
Considerations. On Track 2, `<SWITCH_SN>` is `S248EPTF18000000`. Before the first
change, back up the controller:

```text
FGT # execute backup config tftp fgt-pre-6-1-174.conf 10.30.99.50
```

### Lab 6.1 — FortiLink LAG and the FortiLink split interface

**Objective:** Read the controller's FortiLink interface type and split-interface
setting; on a controller with an aggregate FortiLink interface, add a second
FortiLink link to `FSW-A`, prove that FortiLink survives the loss of either link,
and show why the split interface must be off when both links reach one switch.

**Platform notes:** Hands-on on **C1 whose `<FL_PORT>` is the factory `fortilink`
interface of type `aggregate`**, with S1, S2, or S3 (on S3, `FSW-A`). Step 1 runs
on every controller. C1 with a physical port or a hardware-switch `fortilink`,
C2 (interface cap), and C3 (physical `port4`; see "What each controller option
can build") use the read-and-predict steps. Switch ports: `<FSW_FL_PORT2>` is
`port8` (S1), `port22` (S2, FS-224E), or `port46` (FS-248E). Track 2:
read-and-predict.

**Track 1:**

1. Read the FortiLink interface. `get` prints defaults that `show` hides:

   ```text
   FGT # get system interface port3
   ```

   Record `type`, `member`, `fortilink-split-interface`, `lacp-mode`,
   `fortilink-neighbor-detect`, and `fortilink-backup-link`. Predict
   `fortilink-split-interface` before you read. **Answer:** `enable`, the FortiOS
   7.6.0 default and the guide's statement (p. 23); the guide's example of a
   factory `fortilink` aggregate shows `disable` (p. 29), so record what yours
   says. If `type` is not `aggregate`, stop here and do the read-and-predict
   steps: the rest of this lab needs an aggregate.

2. C1 with an aggregate: choose `<FL_PORT2>`. If `member` already lists a second
   port that is not cabled (some models ship with two), use it and skip to
   step 3. Otherwise take a free port out of the `lan` hardware switch and add it
   to the aggregate; `set member` replaces the list, so name the existing member
   (`<FL_MEMBER1>`) too:

   ```text
   FGT # config system virtual-switch
   edit "lan"
   config port
   delete <FL_PORT2>
   end
   next
   end
   FGT # config system interface
   edit "fortilink"
   set member <FL_MEMBER1> <FL_PORT2>
   next
   end
   ```

3. Both links will reach the same switch, so disable the split interface (p. 27)
   and make sure LACP is active:

   ```text
   FGT # config system interface
   edit "fortilink"
   set fortilink-split-interface disable
   set lacp-mode active
   next
   end
   ```

4. Start the ping from endpoint A. Cable `<FL_PORT2>` to `<FSW_FL_PORT2>` on
   `FSW-A`. Wait one minute, then read both ends (`diagnose netlink aggregate` is
   printed by the guide, p. 88, without output; its syntax is from the FortiOS
   8.0.1 CLI Reference, cross-check):

   ```text
   FGT # diagnose netlink aggregate name fortilink
   FGT # execute switch-controller get-conn-status
   FSW # diagnose switch trunk summary
   ```

   Predict the FortiGate-facing trunk on `FSW-A`. **Answer (expected):** the
   same trunk as in Lab 3.1 (mode `lacp-active(auto-isl)`, named after the
   FortiGate's serial), now `up(2/2)`, because both links lead to the same LACP
   partner; the documentation shows the status format (CLI Reference, p. 381)
   but no two-member FortiLink example, so record whether the second port joins
   that trunk or forms another. `get-conn-status` still shows one switch,
   `Authorized/Up`. Record the aggregate's member states and whether the ping
   lost any replies.

5. Pull the original link: unplug `<FL_MEMBER1>`'s cable at the FortiGate, wait 30
   seconds, read the same three commands, then plug it back in. Repeat with
   `<FL_PORT2>`. **Expected:** the switch stays `Authorized/Up`, the trunk drops
   to `up(1/2)` and returns, and the ping loses at most a few replies. Record the
   gap each time.

**Track 2: read-and-predict.** (C2, C3, and C1 without an aggregate do these
too; run step 1 on your controller first.)

1. A controller's FortiLink interface has `type aggregate`, members `port4` and
   `port5`, both cabled to one FortiSwitch, and `fortilink-split-interface
   enable`. Predict what the switch's FortiGate-facing trunk shows. **Answer:**
   only one link is active; the split interface forces one active link and keeps
   the rest standby (p. 58), which is wrong here: the guide says the split
   interface must be disabled when the members connect to the same switch
   (p. 27).
2. The same interface with neighbor detection `lldp`. Predict the state of the
   standby link. **Answer:** link up, LACP inactive; with `fortilink` neighbor
   detection it would be down (p. 24).
3. Your controller is C2. Predict whether you can add `port4` as a second
   FortiLink port. **Answer:** no. FGT-1 already uses `port1`, `port2`, and
   `port3`; a fourth interface exceeds the evaluation's three-interface cap.
4. Your controller is C3 with FortiLink on the physical `port4`. Predict what a
   FortiLink LAG would require. **Answer:** a new aggregate FortiLink interface
   with two ports and every FortiLink reference moved to it, two FortiGate-VM
   ports that can pass LACP (passthrough, because the `vmbrFL` Linux bridge
   cannot forward slow-protocol frames), and an aggregate that the FortiGate-VM
   supports; the references used here document none of the last two, so this
   volume does not attempt it.

**Expected result:** Track 1 (C1 with an aggregate): `fortilink` has two members
with the split interface disabled; `FSW-A`'s FortiGate-facing trunk is `up(2/2)`;
pulling either link leaves the switch `Authorized/Up` with the ping gaps
recorded. Other options: step 1's values are recorded and the predictions are
answered.

**Negative test:** With both links on `FSW-A`, set `fortilink-split-interface
enable`, wait one minute, and read step 4's three commands. Predict and record:
one member becomes standby (with `lldp` detection, up but not in LACP), the
switch trunk shows one active port, and `fortilink-backup-link` changes. Then set
`fortilink-split-interface disable` again. Track 2: prediction 1.

**Rollback:** On S3 with C1, keep the aggregate and the second cable for Lab 6.2.
Otherwise unplug `<FL_PORT2>`, set `member` back to the value recorded in step 1,
set `fortilink-split-interface` back to the recorded value, and, if you took
`<FL_PORT2>` from `lan`, add it back under `config system virtual-switch`,
`edit "lan"`, `config port`, `edit <FL_PORT2>`; or restore
`fgt-pre-6-1-174.conf`.

**Lab verified by:** *pending*

### Lab 6.2 — Stacking: add a second switch over an automatic ISL

**Objective:** Cable a second FortiSwitch to `FSW-A`, watch the automatic ISL form
and the new switch appear behind `FSW-A`, authorize it with the lab's description
and switch profile, match its firmware, confirm that it joined region `lab-174`
with `FSW-A` as instance 1 root, and (C1 with an aggregate) dual-home FortiLink
to both switches with the split interface.

**Platform notes:** Hands-on on S3 (`FSW-B`) with C1, C2, or C3; on S1 or S2 only
with a second switch of any model running FortiSwitchOS 7.6.x, otherwise
read-and-predict. Auto topology is chain in both matrix columns. C2 and C3 add no
interface: the second switch is reached through `FSW-A`. Step 9 (dual-homed
FortiLink) only on C1 with an aggregate (Lab 6.1). `<ISL_PORT>` is `port4` (S1)
or `port23` (S2, S3). Track 2: read-and-predict.

**Track 1:**

1. Back up the controller, and on the second switch's console confirm the
   starting state:

   ```text
   FGT # execute backup config tftp fgt-pre-6-2-174.conf 10.30.99.50
   FSW # get system status
   ```

   Record `Serial-Number` (`<FSWB_SN>`), `Version`, and `Model name`. The second
   switch must be at factory defaults (Lab 2.4 step 9); if it is not, run
   `execute factoryreset` and set the admin password again.

2. Before cabling, predict what `get-conn-status` will show a few minutes after
   the ISL comes up. **Answer:** a second row, `<FSWB_SN>`, `Discovered/Down`,
   FLAG `2`, VERSION and ADDRESS `N/A`: after `FSW-A` is in FortiLink mode every
   port is enabled for FortiLink, so the new switch forms an ISL and is
   discovered by the FortiGate (FortiLink Guide 7.6.7, p. 31), and automatic
   authorization is off in this volume (Chapter 02).

3. Cable `FSW-A` `<ISL_PORT>` to the second switch's `<FSWB_ISL_PORT>` (a default
   auto-FortiLink port of that model). Wait three minutes and read:

   ```text
   FGT # execute switch-controller get-conn-status
   FSW # diagnose switch trunk summary
   FSW # get switch lldp auto-isl-status <ISL_PORT>
   ```

   Run the two `FSW #` commands on `FSW-A`. Predict the new trunk's mode and
   name. **Answer:** mode `lacp-active(auto-isl)`, `up(1/1)`, named, if it follows
   the documented examples, after `<FSWB_SN>` without its first three characters
   plus `-0` (pp. 48, 381). Record the actual name.

4. Authorize the second switch, give it a description, and bind the lab's
   profile so that its admin password and revision backups are under controller
   control (Chapter 03):

   ```text
   FGT # config switch-controller managed-switch
   edit <FSWB_SN>
   set description "FSW-B lab-174"
   set switch-profile "fsw-174-prof"
   set fsw-wan1-admin enable
   next
   end
   ```

5. The switch reboots in FortiLink mode (p. 41). Repeat `get-conn-status` every
   minute until both rows read `Authorized/Up`, then read the leases:

   ```text
   FGT # execute switch-controller get-conn-status
   FGT # execute dhcp lease-list port3
   ```

   Record `FSW-B`'s address as `<FSWB_IP>`. The documentation does not say which
   lease it takes; Chapter 01 expects the next one. Compare your table with the
   guide's four-switch stack (p. 345), where every switch below the first is
   listed under the same FortiLink interface with its own address.

6. Compare the builds in the VERSION column. If `FSW-B`'s differs from `FSW-A`'s
   (S3: required for Lab 6.3; S1 or S2: optional), push `FSW-A`'s build with the
   image uploaded in Lab 3.3 (Lab 3.3 steps 3 to 6):

   ```text
   FGT # execute switch-controller switch-software list-available
   FGT # execute switch-controller switch-software upgrade <FSWB_SN> <IMAGE_NAME>
   FGT # execute switch-controller get-upgrade-status
   ```

7. Check the spanning tree from both switches:

   ```text
   FGT # diagnose switch-controller switch-info stp <FSWB_SN> 1
   FSW # diagnose stp mst-config list
   ```

   Run `diagnose stp mst-config list` on both switches. Predict before you read.
   **Answer:** both show `MST Configuration Name: lab-174`, revision 1, and the
   **same digest**, so they are one region (the map came from the global
   `stp-instance`); `FSW-B` instance 1 priority 32768 against `FSW-A`'s 16384, so
   in `FSW-B`'s instance 1 table the root is `FSW-A` and `FSW-B`'s ISL trunk is
   its root port, `FORWARDING`. For instance 0, record which switch is root: both
   start at the same default priority, so the lower MAC address wins. If the
   digests differ, stop: something set a per-switch STP override.

8. See the topology from the controller:

   ```text
   FGT # execute switch-controller get-physical-conn standard port3
   FGT # diagnose switch-controller switch-info lldp neighbors-summary <SWITCH_SN>
   FGT # get switch-controller managed-switch <SWITCH_SN>
   ```

   In the last output, find `<ISL_PORT>` under `ports` and record the read-only
   fields `isl-local-trunk-name`, `isl-peer-device-name`, and
   `isl-peer-port-name` (FortiOS 7.6.0 CLI Reference). The GUI's **Topology**
   view under **WiFi & Switch Controller > Managed FortiSwitches** draws the two
   switches as a two-tier stack.

9. **C1 with an aggregate, second switch present:** dual-home FortiLink. Unplug
   the `<FL_PORT2>` cable from `FSW-A`, enable the split interface **first**, then
   cable `<FL_PORT2>` to `<FSWB_FL_PORT>` on `FSW-B`:

   ```text
   FGT # config system interface
   edit "fortilink"
   set fortilink-split-interface enable
   set lacp-mode active
   next
   end
   ```

   Wait one minute and read:

   ```text
   FGT # diagnose netlink aggregate name fortilink
   FGT # get system interface fortilink | grep fortilink-backup-link
   FGT # execute switch-controller get-conn-status
   ```

   Predict which link carries traffic. **Answer:** one link is active and the
   other standby, which avoids a loop through the ISL (p. 58); with `lldp`
   detection the standby link is up but not in LACP (p. 24). Then unplug the
   active link's cable at the FortiGate with the ping running: FortiLink should
   move to the standby link, and both switches stay `Authorized/Up` (`FSW-A` is
   now reached through `FSW-B` and the ISL). Record the gap, and plug the cable
   back in.

**Track 2: read-and-predict.**

1. The guide's stack example (p. 345) lists four switches, `S108FF5918003577`,
   `S108FP5918008265`, `S224ENTF18001408`, `S224ENTF18001432`, all
   `Authorized/Up` with addresses `10.105.22.2`–`.6`, under
   `STACK-NAME: FortiSwitch-Stack-flink`. Only one of them is cabled to the
   FortiGate. Predict how the others reached `Authorized/Up`. **Answer:** each was
   cabled to a port of an already managed switch, formed an automatic ISL, was
   discovered by the FortiGate through the stack, and was authorized; the
   FortiGate manages each switch separately over the one active FortiLink
   (pp. 31, 54).
2. `FSW-A`'s `diagnose switch trunk summary` shows
   `8DN3X16000001-0 lacp-active(auto-isl) src-dst-ip ... up(1/1)` (CLI Reference,
   p. 381). Predict what kind of peer this trunk leads to. **Answer:** an
   automatically formed trunk to another Fortinet device, either the FortiGate
   (the FortiLink) or a switch (an ISL); the name is the peer's serial without
   its first three characters plus `-0`. `up(1/1)` means one of one member is
   up, so Security Rating would recommend a second link for an ISL (p. 275).
3. A new switch was authorized into a stack whose global STP region is `lab-174`
   revision 1. An administrator then set `local-override enable` and `revision 2`
   under the new switch's `config stp-settings`. Predict the effect. **Answer:**
   the new switch leaves the region and becomes a region of its own; the two
   regions meet at a boundary and instance 1 is no longer shared (Chapter 05,
   Lab 5.3).
4. Predict the FortiGate setting a dual-homed FortiLink (one aggregate member to
   each of two switches with an ISL between them, no MCLAG) needs. **Answer:**
   `fortilink-split-interface enable` with `lacp-mode active` (p. 58).

**Expected result:** Track 1: the ISL formed on `<ISL_PORT>`; `<FSWB_SN>` went from
`Discovered/Down` to `Authorized/Up` with description `FSW-B lab-174` and profile
`fsw-174-prof`, on `FSW-A`'s build; both switches show region `lab-174` revision 1
with the same digest, and `FSW-A` is instance 1 root; C1 with an aggregate:
dual-homed FortiLink with one active and one standby link, failover recorded.
Track 2: the predictions are answered.

**Negative test:** Show that the LLDP profile decides whether an ISL forms. If you
did step 9, first undo it (unplug `<FL_PORT2>` from `FSW-B`), so that `FSW-B`'s
only path is the ISL. With the ping running only as a reference, set `FSW-A`'s
ISL port to the `default` profile:

```text
FGT # config switch-controller managed-switch
edit <SWITCH_SN>
config ports
edit "<ISL_PORT>"
set lldp-profile "default"
next
end
next
end
```

Predict and record: the guide uses `default` on ports where no ISL must form
(p. 96), so the ISL trunk is expected to disappear from `diagnose switch trunk
summary` on `FSW-A` and `FSW-B` to go `Authorized/Down`. Then set
`lldp-profile "default-auto-isl"` on the port again and wait until `FSW-B` is
`Authorized/Up`. Track 2: prediction 3.

**Rollback:** S3: keep `FSW-B` for Lab 6.3; keep step 9's cabling on C1. S1 or S2
with a borrowed switch: if you did step 9, set the aggregate back as in Lab 6.1's
rollback; then retire the second switch as in Lab 3.5 steps 2 and 4
(`execute switch-controller switch-action set-standalone <FSWB_SN>`, then set
`fsw-wan1-admin disable` and `delete <FSWB_SN>`), unplug the ISL cable, and
remove `<FSWB_SN>` from `disable-discovery` if the controller added it. Or restore
`fgt-pre-6-2-174.conf` and unplug the second switch.

**Lab verified by:** *pending*

### Lab 6.3 — MCLAG peer group, MCLAG trunks, and tiered MCLAG

**Objective:** Turn the ISL between `FSW-A` and `FSW-B` into a two-link MCLAG ICL
from the FortiGate, read the ICL from both ends, confirm that STP still runs
correctly across the pair, build and inspect an MCLAG trunk, and (C1 with an
aggregate) make the dual-homed FortiLink active on both links; work out how
tier-2 and tier-3 MCLAGs are built.

**Platform notes:** Hands-on on S3 only (MCLAG, STP in MCLAGs: chain in the 200
Series column, dash in 1xxE/1xxF), with C1, C2, or C3; S1 and S2 use the
read-and-predict steps. Step 7 (FortiLink MCLAG) only on C1 with an aggregate and
Lab 6.2 step 9 done. Tiered MCLAG needs at least four MCLAG-capable switches and
is read-and-predict on every option. Second ICL link: `FSW-A` `port24` to
`<FSWB_ICL_PORT2>` (`port24` on an FS-224E, `port48` on an FS-248E). Track 2:
read-and-predict.

**Track 1:**

1. Back up the controller and check the pair against the MCLAG requirements:
   same model and same build in `get-conn-status` (p. 85):

   ```text
   FGT # execute backup config tftp fgt-pre-6-3-174.conf 10.30.99.50
   FGT # execute switch-controller get-conn-status
   ```

2. Add the second link. Cable `FSW-A` `port24` to `FSW-B` `<FSWB_ICL_PORT2>` and read
   `FSW-A`'s trunks:

   ```text
   FSW # diagnose switch trunk summary
   ```

   **Expected:** the ISL trunk to `FSW-B` is now `up(2/2)`.

3. Read the MCLAG settings on both switches:

   ```text
   FSW # get switch global
   ```

   Record `mclag-stp-aware`, `mclag-split-brain-detect`,
   `mclag-igmpsnooping-aware`, and `mclag-peer-info-timeout`. Predict the first
   two. **Answer:** `mclag-stp-aware` `enable` (it must be, and it is the default)
   and `mclag-split-brain-detect` `disable` (FortiSwitchOS 7.6.7 CLI Reference,
   pp. 118–119; FortiLink Guide 7.6.7, p. 85). Record
   `mclag-igmpsnooping-aware`, whose default the two documents state differently.

4. Form the ICL from the FortiGate: put the ISL ports of **both** switches on the
   `default-auto-mclag-icl` LLDP profile (pp. 86–87). Start the ping first:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port23"
   set lldp-profile "default-auto-mclag-icl"
   next
   edit "port24"
   set lldp-profile "default-auto-mclag-icl"
   next
   end
   next
   end
   FGT # config switch-controller managed-switch
   edit <FSWB_SN>
   config ports
   edit "<FSWB_ISL_PORT>"
   set lldp-profile "default-auto-mclag-icl"
   next
   edit "<FSWB_ICL_PORT2>"
   set lldp-profile "default-auto-mclag-icl"
   next
   end
   next
   end
   ```

   The GUI alternative (FortiOS 7.2.4 and later) is **Security Fabric > Security
   Rating**, **Failed > Enable MC-LAG**, then **Create MC-LAG pair** on the ISL in
   the Topology view (p. 86).

5. Read the ICL from the controller and from `FSW-A` (the controller command is
   printed in the guide without output, p. 89):

   ```text
   FGT # diagnose switch-controller switch-info mclag icl
   FSW # diagnose switch mclag icl
   FSW # diagnose switch trunk summary
   ```

   Predict the switch-side output before you read it, using the CLI Reference
   example (p. 357):

   ```text
   Switch1 # diagnose switch mclag icl
   ICL-trunk
   icl-ports 47-48
   egress-block-ports 3,37
   interface-mac 08:5b:0e:73:fb:e7
   local-serial-number FS1D483Z14000113
   peer-mac 08:5b:0e:73:f8:87
   peer-serial-number FS1D483Z14000097
   ...
   MCLAG-STP-mac 08:5b:0e:73:f8:86
   keepalive interval 1
   keepalive timeout 60
   dormant candidate Peer
   split-brain Normal
   ```

   **Answer:** a trunk name (the guide's 3032E example uses `_FlInK1_ICL0_`,
   p. 99), `icl-ports` listing `FSW-A`'s ports 23–24, `local-serial-number`
   `<SWITCH_SN>`, `peer-serial-number` `<FSWB_SN>`, keepalive interval 1 and
   timeout 60, and a `split-brain` line (the example shows `Normal`; the guide's
   example with protection off shows `Disabled`, p. 99, so expect `Disabled`
   with the default `mclag-split-brain-detect disable`). In the trunk summary,
   the trunk's mode reads `lacp-active(mclag-icl)`, `up(2/2)`. Record the
   `dormant candidate` and compare the two `interface-mac` values: the switch
   with the lower MAC address is the one the upgrade procedure restarts first
   (p. 99).

6. Check spanning tree across the peer group:

   ```text
   FGT # diagnose switch-controller switch-info stp <FSWB_SN> 1
   FSW # diagnose stp instance list 1
   FSW # diagnose stp mst-config list
   ```

   Predict: still one region (same digest on both), `FSW-A` still the instance 1
   root, and STP enabled on the ICL trunk, as the MCLAG requirements demand
   (p. 85). Record the ICL trunk's role and state in `FSW-B`'s table.

7. **C1 with an aggregate and Lab 6.2 step 9 done:** move from the split interface
   to a FortiLink MCLAG. The ICL now exists, so the split interface can be
   disabled (pp. 87–88):

   ```text
   FGT # config system interface
   edit "fortilink"
   set fortilink-split-interface disable
   set lacp-mode active
   next
   end
   FGT # diagnose netlink aggregate name fortilink
   FSW # diagnose switch trunk summary
   ```

   Run the trunk summary on both switches. Predict: both FortiGate members are
   active in one LACP aggregate; each switch shows a FortiGate-facing trunk with
   one member up. Record the mode string each switch prints for that trunk (the
   documentation does not show it). Then pull each FortiGate link in turn with
   the ping running, as in Lab 6.1 step 5, and record the gaps.

8. Build an MCLAG trunk. Each peer gets a trunk with the **same name**, here on
   `port7` of each switch (p. 117); no device is attached, so it will stay down:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "mclag-ep-174"
   set type trunk
   set mode lacp-active
   set members "port7"
   set mclag enable
   next
   end
   next
   end
   FGT # config switch-controller managed-switch
   edit <FSWB_SN>
   config ports
   edit "mclag-ep-174"
   set type trunk
   set mode lacp-active
   set members "port7"
   set mclag enable
   next
   end
   next
   end
   ```

   Read it:

   ```text
   FGT # diagnose switch-controller switch-info mclag list
   FSW # diagnose switch mclag list mclag-ep-174
   FSW # diagnose switch mclag peer-consistency-check
   FSW # diagnose switch trunk summary mclag-ep-174
   ```

   Predict the trunk summary line. **Answer:** mode `lacp-active(mclag)`, status
   `down(0/1)`, uptime `N/A`: the CLI Reference's MCLAG example shows the same
   shape for a static MCLAG trunk with no partner (`static(mclag) ...
   down(0/1)`, p. 381). Record what `peer-consistency-check` reports for
   `mclag-ep-174`.

**Track 2: read-and-predict.** (S1 and S2 do these too.)

1. Your switches are an FS-124F and an FS-108F joined by two cables. Predict
   whether `default-auto-mclag-icl` on those ports forms an ICL. **Answer:** no;
   MCLAG is a dash in the 1xxE/1xxF column of the 7.6.7 feature matrix, and the
   two are different models in any case (p. 85). The two cables remain an ISL
   with two members, and STP blocks nothing because they form one LACP trunk.
2. The CLI Reference prints (p. 381):

   ```text
   Mclag-icl-trunk lacp-active(mclag-icl) N/A 08:5B:0E:F1:95:F4 down(0/2)
   first-mclag static(mclag) N/A 08:5B:0E:F1:95:E7 down(0/1)
   8DN3X16000001-0 lacp-active(auto-isl) src-dst-ip 08:5B:0E:F0:9B:90 up(1/1)
   ```

   Predict what each line is. **Answer:** the ICL (two members, both down), an
   MCLAG trunk toward a device (static mode, one local member, down), and an
   automatically formed FortiLink or ISL trunk that is up with one member.
3. An administrator configured `mclag-to-srv` on `FSW-A` and `mclag-srv` on
   `FSW-B`, each with `mclag enable`, for one dual-homed server. Predict the
   problem. **Answer:** the trunk name must be the same on both peers (p. 117),
   so the two halves are not one MCLAG; `diagnose switch mclag
   peer-consistency-check` is the tool to find such mismatches.
4. A site has a tier-1 MCLAG core (`FSW-1`, `FSW-2`) and adds a tier-2 pair
   (`FSW-3`, `FSW-4`) in a closet, fully meshed to the core on core ports `port1`
   and `port2`. Predict what must be configured, and where, so that the core
   groups those ports into one MCLAG. **Answer:** on each tier-1 switch, directly
   in the FortiSwitch CLI (or through a bound custom command), an
   `auto-isl-port-group` for the closet with members `port1` and `port2`; then
   `default-auto-mclag-icl` on the ICL ports of `FSW-3` and `FSW-4` from the
   FortiGate (pp. 91–92):

   ```text
   FSW # config switch auto-isl-port-group
   edit "tier2-closet-1"
   set members "port1" "port2"
   next
   end
   ```

5. The FortiGate has a dual-homed FortiLink with the split interface disabled
   and an MCLAG ICL between the two switches. The administrator removes the ICL.
   Predict what must be done first. **Answer:** enable the split interface; if the
   MCLAG ICL is disabled, the guide says you need to enable
   `fortilink-split-interface` (p. 88), because without the ICL two active links
   to two switches joined by an ISL form a loop.

**Expected result:** Track 1: the ICL is up on two links with the expected local
and peer serials; region `lab-174` and the instance 1 root are unchanged; the
MCLAG trunk `mclag-ep-174` exists on both peers, down with no partner, and the
consistency check result is recorded; C1 with an aggregate: both FortiLink links
active, failover gaps recorded. Track 2: the predictions are answered.

**Negative test:** Unplug the `port24` ICL cable and read `diagnose switch mclag icl`
and `diagnose switch trunk summary` on `FSW-A`. Predict and record: the ICL stays
up on one link (`up(1/2)`), `FSW-B` stays `Authorized/Up`, and the instance 1
root does not change; this is why the guide asks for two ICL links (p. 85).
Plug it back in. Track 2: prediction 1.

**Rollback:** Delete the test trunk on both switches (`config ports`,
`delete "mclag-ep-174"` under each switch's entry). C1 with an aggregate: enable
the split interface **first**, then unplug `<FL_PORT2>` from `FSW-B`, set `member`
back to the value recorded in Lab 6.1 step 1, set `fortilink-split-interface`
back to the recorded value, and return `<FL_PORT2>` to `lan` if you took it from
there. Keep the ICL and `FSW-B`. To dissolve the peer group as well, set the four
ICL ports back to `lldp-profile "default-auto-isl"` and record whether the trunk
returns to `auto-isl` mode; or restore `fgt-pre-6-3-174.conf` (which predates the
ICL but not `FSW-B`).

**Lab verified by:** *pending*

### Lab 6.4 — Topology selection

**Objective:** Choose a documented FortiLink topology for each of eight site
descriptions, name its FortiLink interface type and the settings or limits that
decide it, and read your own lab's topology markers.

**Platform notes:** Design plus read-and-predict on every option (C1–C3, S1–S3,
Track 2). Step 1 is hands-on with a managed switch on any option, and on
Track 2 against the stand-in entry or not at all. No configuration changes.

**Track 1:**

1. Read your lab's topology markers:

   ```text
   FGT # execute switch-controller get-conn-status
   FGT # get system interface port3 | grep switch-controller-source-ip
   ```

   Record the FLAG of each switch and the `MAX` on the last line. Predict them.
   **Answer:** FLAG `2` (Layer 2) for each switch, because every switch reaches
   the FortiGate over Layer 2 FortiLink; `3` would mean Layer 3, `V` VXLAN, and
   `T` FortiLink over HTTPS (the tunnel) (pp. 52, 74). `MAX` is your model's
   managed-switch limit (8 on a 40F or FortiGate-VM01, 24 on a 60F; p. 12).
   `switch-controller-source-ip` reads `outbound` (the default) unless changed;
   `fixed` makes the FortiLink interface the source address for FortiLink over
   Layer 3 (p. 63; FortiOS 7.6.0 CLI Reference, which marks the option "may not
   exist in some models", so record whether your controller prints it).

2. Work the design exercise below. For each site, write down the topology, the
   FortiLink interface type, and the deciding setting or limit, then compare with
   the answer.

**Track 2:** Run step 1's second command on your controller (it reads only the
FortiLink interface). Do the design exercise.

**Track 2: read-and-predict.** (Every option does these.)

| # | Site | Your answer |
| --- | --- | --- |
| 1 | One FortiGate, 12 users, one switch, no redundancy budget | |
| 2 | One FortiGate, four switches in a row, and a wish to survive the loss of the uplink switch | |
| 3 | An HA pair of FortiGates, two distribution switches that support MCLAG, and access switches in each closet | |
| 4 | An HA pair of FortiGates whose model has no aggregate interface, and two switches without MCLAG | |
| 5 | Two buildings joined by a wireless bridge, one FortiGate in building A, a switch in building B | |
| 6 | A branch switch reached across a routed WAN, no Layer 2 path to the FortiGate | |
| 7 | A FS-124F at a remote site, to be managed over a VXLAN tunnel | |
| 8 | Two FortiGates, each with its own MCLAG fabric, that must exchange one VLAN | |

**Answers:**

1. **Single FortiGate, single switch** (p. 55): a physical or aggregate FortiLink
   interface; for an aggregate whose members all go to that switch, the split
   interface must be disabled (pp. 27, 55). This is the volume's own topology.
2. **Single FortiGate, a stack of several switches** (p. 56): the FortiGate
   connects to the first switch; the others connect by ISLs; optionally a standby
   FortiLink to the last switch, using an aggregate with
   `fortilink-split-interface enable` and `lacp-mode active`. Do not create loops
   or rings with the FortiGate in the path.
3. **HA-mode one-tier MCLAG** or **HA with dual-homed access** (pp. 77–78): both
   FortiGates connect FortiLink to the MCLAG distribution pair with matching
   FortiLink ports and types; once the MCLAG peer group exists, MCLAG trunks to
   the access switches form automatically (p. 77); the split interface is
   disabled only after the ICL exists (pp. 85–88).
4. **HA-mode FortiGates using hardware-switch interfaces and STP** (p. 61): each
   switch on one port of each FortiGate's FortiLink hardware switch, an ISL
   between the switches, `set stp enable` on the hardware-switch interface after
   `lldp-transmission enable`; because the model has no aggregates, the
   FortiGate must be the CIST root (lowest `switch-priority` under `config system
   stp`) and each switch in a different region (Chapter 05, Lab 5.3).
5. **FortiLink over a point-to-point Layer 2 network** (p. 62, FortiSwitchOS 6.4.0
   and later): an ISL between two switches across the bridge, with `set
   fortilink-p2p enable` on the port at each end (`config switch physical-port`);
   LLDP is sent to the broadcast MAC address to pass the middle device; the TPID
   (`fortilink-p2p-tpid`, FortiLink mode only) must match, and FS-124E/F and
   FS-148E/F models support only the default `0x8100`.
6. **FortiLink mode over a Layer 3 network** (pp. 63–68): a FortiSwitch island
   with in-band (`internal`) or out-of-band (`mgmt`) management, DHCP option 138
   or static discovery, and NTP. The limits: no FortiSwitch NAC; no Layer 2 data
   path component such as a VLAN can span the Layer 3 network to the FortiGate;
   all switches of an island connect to the same FortiGate; a working Layer 3
   route is needed to the FortiGate and to every service such as syslog or
   802.1X; no NAT between switch and FortiGate; with a `mgmt`-port island, only
   one switch; and downgrading FortiSwitchOS afterward is not supported.
   FLAG `3` in `get-conn-status`.
7. **Not this model.** The guide documents managing FortiSwitch units over VXLAN
   interfaces (pp. 69–74, FLAG `V`), but the 7.6.7 feature matrix gives "FortiLink
   management over VXLAN" a dash in the 1xxE/1xxF and 200 Series columns; choose
   a supported model, or use FortiLink over Layer 3 (answer 6) with its limits.
8. **Interconnecting FortiLink fabrics** (pp. 96–99): each FortiGate manages its
   own switches; the interconnection ports use the `default` LLDP profile so that
   no ISL forms (auto-ISL disabled), an MCLAG trunk on each side carries the
   shared VLAN with matching VLAN IDs (names may differ) and matching native and
   allowed VLANs, and optionally each FortiGate lists the other fabric's switches
   in `disable-discovery`.

**Expected result:** Track 1: the flags, `MAX`, and `switch-controller-source-ip`
are recorded and explained. Every option: eight answers written and compared,
each with its interface type and deciding setting or limit.

**Negative test:** For site 6, an administrator plans 802.1X with dynamic VLAN
assignment and a guest VLAN that is routed on the FortiGate. Predict whether the
design works. **Answer:** not as planned: FortiSwitch NAC is not supported on a
Layer 3 island, and no VLAN can span the Layer 3 network to the FortiGate, so
the guest VLAN cannot terminate on the FortiGate at Layer 2; the switch needs its
own Layer 3 path to the RADIUS server (pp. 67–68).

**Rollback:** None; this lab changes nothing.

**Lab verified by:** *pending*

## Lab Verification

Complete this sign-off once Labs 6.1 to 6.4 have been run end to end on your
options, including each negative test, and the cabling and settings to keep are
as listed in Design Considerations. Until then, the labs are unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

All switches below one FortiLink interface form one Layer 2 stack that the
FortiGate manages switch by switch. The first switch connects over FortiLink;
others join over automatic ISLs on any port of a managed switch, as long as the
port's LLDP profile allows auto-ISL. FortiLink itself becomes redundant in three
ways: a FortiLink LAG to one switch (split interface disabled), a dual-homed
active/standby FortiLink (split interface enabled), or a FortiLink MCLAG (split
interface disabled after the ICL forms). Only a controller with a two-port
FortiLink interface can do any of them: in this volume, C1 with its factory
`fortilink` aggregate. MCLAG needs two switches of the same model and build that
support it, which among the volume's options means S3; the ICL forms from the
FortiGate with the `default-auto-mclag-icl` LLDP profile, and tiered MCLAG adds
`auto-isl-port-group` on the switches. The lab ends with, on S3, `FSW-B`
authorized under `fsw-174-prof` in region `lab-174` with `FSW-A` as instance 1
root and an ICL between the pair, and FortiLink back on one cable.

- [ ] I read my controller's FortiLink interface type and split-interface
      setting, and can say what my controller option can build.
- [ ] (C1 with an aggregate) I built a FortiLink LAG to `FSW-A` and pulled each
      link without losing the switch.
- [ ] I can state when the split interface must be enabled and when it must be
      disabled.
- [ ] I added a second switch over an automatic ISL, authorized it, and bound
      `fsw-174-prof` (or answered the predictions).
- [ ] Both switches show region `lab-174` revision 1 with the same digest, and
      `FSW-A` is instance 1 root.
- [ ] (S3) I formed the MCLAG ICL from the FortiGate, read it from both ends, and
      built and deleted an MCLAG trunk.
- [ ] I can list the MCLAG requirements and say why S1 and S2 cannot run MCLAG.
- [ ] I chose a topology for each of the eight sites and can state the limits of
      FortiLink over Layer 3.
