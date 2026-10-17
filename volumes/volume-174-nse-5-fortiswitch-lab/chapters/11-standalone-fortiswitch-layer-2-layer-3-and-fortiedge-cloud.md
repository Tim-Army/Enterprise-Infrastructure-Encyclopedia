# Chapter 11: Standalone FortiSwitch: Layer 2, Layer 3, and FortiEdge Cloud

## Learning Objectives

- Name the managers a FortiSwitch can have (a FortiGate over **FortiLink**,
  **FortiEdge Cloud**, FortiSwitch Manager, or none, which is **standalone
  mode**), and state why only one of them can manage the switch at a time.
- Take a managed switch out of FortiLink mode with `set-standalone`, keep its
  controller entry, bring it up standalone from the console with zero-touch
  features turned off, and give it a hardened management address on the
  management port or on `internal`.
- Configure standalone VLANs, native, allowed, and untagged VLAN lists, an
  802.1Q uplink that carries two lab VLANs to the controller, a link
  aggregation group (a FortiSwitch **trunk**), and a local MSTP region.
- Add **switch virtual interfaces** (SVIs) and static routes, route between two
  VLANs on the switch, and explain why that routing bypasses the FortiGate's
  firewall policy; know which Layer 3 features need the Advanced Features
  license and which models route in software.
- Build standalone **ingress ACLs** with **ACL services** on every switch option,
  read their counters, and state the FS-1xx ACL limits; on the 200 Series, build
  a **private VLAN** and mark traffic with the ACL **remark** actions.
- Describe how **FortiEdge Cloud** manages a standalone switch, connect one if
  you have a FortiCloud account, and plan the migration of a standalone
  configuration into FortiLink mode.
- Return the switch to FortiLink management in the state Chapter 10 left, with
  backups of both the standalone and the managed configuration.

## Theory and Architecture

### Who manages the switch

A FortiSwitch running FortiSwitchOS 7.6 has one manager at a time:

| Manager | Where the configuration lives | How the switch finds it | This volume |
| --- | --- | --- | --- |
| A FortiGate over FortiLink | On the FortiGate (`config switch-controller managed-switch`), pushed to the switch | FortiLink discovery on the switch ports, then authorization on the FortiGate | Chapters 02–10 and 12 |
| FortiEdge Cloud | In the cloud service, pushed to the switch | The switch's cloud client (`config system flan-cloud`) contacts the dispatch service | Lab 11.5 (optional, needs a FortiCloud account) |
| FortiSwitch Manager | On a FortiSwitch Manager appliance or VM | Discovery settings on the switch | Not used |
| None (standalone) | On the switch itself | Console, SSH, HTTPS | Labs 11.1–11.5 |

The FortiLink Guide says that a new switch connects to whichever manager is
available, that "only one manager can be used at a time", and that a switch
cannot be authorized for more than one manager in most cases (p. 14). It also
warns that changes made directly on a managed switch are unknown to the
FortiGate and are missing after the switch restarts (p. 14). Standalone mode is
therefore not a feature you switch on: it is what a switch is when no manager
holds it. The exam page says the exam also tests FortiSwitch deployed in
standalone mode, which is why this chapter runs the lab switch on its own.

The feature matrix marks some features **standalone only** (a check mark) and
some as standalone and managed (a chain icon). For this volume's switches, the
standalone-only features that matter are ingress ACLs and ACL services on the
FS-108F and FS-124F (note 16), private VLANs and QoS marking on the 200 Series,
and FortiEdge Cloud configuration itself.

### Leaving FortiLink mode and coming back

The FortiLink Guide gives two controller commands that return a managed switch
to standalone mode (p. 322); Chapter 03 used the second:

| Command | Effect |
| --- | --- |
| `execute switch-controller factory-reset <switch-id>` | Factory defaults and reboot; a switch with FortiLink auto-discovery can be detected and authorized again |
| `execute switch-controller switch-action set-standalone <switch-id>` | Factory defaults and reboot, and the FortiGate does not detect and authorize it automatically |

Both commands reset the switch, so its FortiLink-mode configuration does not
survive on the switch. What survives is the **managed-switch entry on the
controller**: its description, profile, per-port settings, and STP instance
settings. This chapter keeps that entry, deauthorized, while the switch runs
standalone, and authorizes it again at the end so that the controller pushes the
same settings back. Neither guide describes this round trip as a procedure, so
Lab 11.5 checks every item of the Chapter 10 state after the switch returns and
gives a restore path if anything is missing.

On the switch side, the Administration Guide shows how to turn FortiLink off
completely in standalone mode (pp. 139–140): `set auto-fortilink-discovery
disable` and `set auto-isl disable` under `config switch global`, and the
`default` LLDP profile (which has auto-ISL off) on single ports. Auto topology
(`config switch auto-network`) is enabled again by every factory reset and must
be disabled by hand if you are not using it (Administration Guide, p. 384; CLI
Reference, p. 114).

Coming back is the reverse: reset the switch so that it is at zero-touch
defaults again, cable it to the FortiLink port, remove it from the controller's
`disable-discovery` list if `set-standalone` put it there, and authorize it.
The FortiLink Guide adds that a configured standalone switch loses its
standalone configuration when it is converted to FortiLink mode, and points
to the `fortilinkify.py` utility on the Fortinet Developer Network to translate
standalone configurations into FortiGate configuration (p. 34).

### Zero-touch defaults and what to turn off

A switch that `set-standalone` has just reset comes up with the zero-touch
defaults the FortiLink Guide lists (pp. 14–15): VLAN 1 native on every port
and on the internal interface, DHCP on `mgmt` and `internal` (with the default
gateway taken from DHCP), auto topology on, FortiLink auto-discovery on every
port, FortiLink CAPWAP discovery on, and FortiLAN Cloud enabled. When it
detects a Layer 2 network it applies MSTP to instances 0 and 15 and moves the
internal interface to native VLAN 4094. A reset also creates an SNMP community
named `public` (CLI Reference, p. 274) and forces you to set an admin password
at the first login (Administration Guide, p. 73).

For a switch that is meant to stay standalone, Lab 11.1 turns off auto
topology, FortiLink auto-discovery, and the cloud client, replaces DHCP with a
static management address, and removes the `public` community before the
switch is cabled to anything but the console.

### Management access in standalone mode

| Model type | Management interface | Default VLAN of `internal` | Lab 11.1 |
| --- | --- | --- | --- |
| With a dedicated management port | `mgmt`, an out-of-band port that is not a switch port | 4094 | `mgmt` cabled to the Nexus port in VLAN 99 |
| Without one | `internal`, the switch's own interface into its switching fabric, reached through a front port in the same VLAN | 1 | `internal` and `port3` moved to a local management VLAN 99; `port3` cabled to the Nexus port |

Both rows come from the Administration Guide (pp. 17–21). The second matches
Chapter 02, which reached `internal` through `port3` while upgrading firmware.
On a model without a management port, keeping management in VLAN 1 would put it
in the VLAN that every unused port is in; Volume CLXXII's prerequisite P10 asks
for management on its own VLAN, so Lab 11.1 moves `internal` and `port3` to VLAN
99 (the same number as the Nexus access VLAN, which is only a convenience: the
Nexus port is an access port and does not see the switch's VLAN tags).

Remote access needs a static route through the management router (`config
router static` with `device` and `gateway`, Administration Guide, pp. 23 and
484). Administrative access is limited per interface (`allowaccess`), per
account (`trusthost1` to `trusthost10` under `config system admin`), and
globally (`admintimeout`, `admin-lockout-threshold`, `admin-lockout-duration`,
and `pre-login-banner` under `config system global`; Administration Guide,
pp. 75 and 86).

### VLANs, native and allowed lists, and trunks

In standalone mode the switch's own objects replace the FortiOS ones:

| Standalone object | FortiLink-mode counterpart (Chapter 04) |
| --- | --- |
| `config switch vlan`, `edit <VLAN_ID>` (with a description) | A FortiGate VLAN interface on the FortiLink interface, pushed as a switch VLAN |
| `config switch interface`, `native-vlan`, `allowed-vlans`, `untagged-vlans` | `config ports`, `vlan`, `allowed-vlans`, `untagged-vlans` in the managed-switch entry |
| `config switch trunk` (a LAG: `static`, `lacp-active`, `lacp-passive`, or `fortinet-trunk`) | `config ports`, `type trunk` in the managed-switch entry |
| `config switch stp settings` and `stp instance` on each switch | `config switch-controller stp-settings` and `stp-instance` on the FortiGate |

The frame rules are those of Chapter 04, stated in the Administration Guide
(pp. 341–343): an untagged frame takes the port's native VLAN; a tagged frame is
accepted only if its VLAN is in the allowed list or is the native VLAN; on
egress, frames of the native VLAN and of the untagged list leave untagged,
frames of other allowed VLANs leave tagged, and everything else is dropped.
`discard-mode` can refuse all tagged or all untagged frames on a port.

A port that carries several VLANs tagged is what other vendors call a trunk
port. In FortiSwitchOS, **trunk** means a link aggregation group. LACP trunks
need a partner: an LACP member with nothing at the other end, or with a partner
that sends no LACP, does not join the aggregator, unless a `fallback-port` is
set (Administration Guide, pp. 164–167). Do not set `auto-isl` on a trunk that
you manage yourself (p. 166).

### Spanning tree on a standalone switch

Standalone MSTP uses the same model as Chapter 05: a region name, a revision,
and VLAN-to-instance mappings that must match on every switch of the region,
with per-instance priorities (CLI Reference, pp. 177–179; Administration Guide,
pp. 264–271). The difference is that each switch is configured on its own,
with `config switch stp settings` and `config switch stp instance`, and that
port protections are set on `config switch interface`: `edge-port`,
`stp-bpdu-guard` (which needs STP and edge port enabled on the port),
`stp-root-guard`, `stp-loop-protection`, `loop-guard`, and
`loop-guard-mac-move-threshold` (CLI Reference, pp. 126–131). The Administration
Guide recommends loop protection on all non-designated ports (p. 264).

### Switch virtual interfaces and static routes

An **SVI** is a `config system interface` entry with `interface internal` and a
`vlanid`; giving it an address lets the switch route between VLANs without an
external router (Administration Guide, pp. 24–26). Static routes use `config
router static` with `dst`, `gateway`, and `device`; a gateway must be in the
device's subnet, and a destination cannot be one of the switch's own subnets
(p. 486). The feature matrix marks SVIs and static routing as chain in both
columns (note 9: IPv4 only in managed mode), with **software-based routing
only** on the FS-1xx models and **hardware-based routing** on the 200 Series.

Dynamic routing is out of scope. In the 7.6.7 matrix, OSPF, RIP, VRRP, BGP, and
policy-based routing sit under the heading "Layer 3: Requires Advanced Features
License"; they are a dash in the 1xxE/1xxF column, and OSPF, RIP, VRRP, and
policy-based routing are a check (standalone only) in the 200 Series column,
where BGP is a dash. Inter-VLAN routing offload is a dash in both columns
(note 19).

Routing on the switch has a security consequence that the lab makes visible:
traffic routed between two SVIs never reaches the FortiGate, so the
controller's `FSW-LAN` intrazone deny no longer applies to it.

### ACLs in standalone mode

A FortiSwitch has three ACL stages, **ingress**, **prelookup**, and **egress**
(Administration Guide, p. 292). An ingress policy (`config switch acl ingress`)
has an ingress interface list or `ingress-interface-all`, a classifier, and
actions, and can use a named service from `config switch acl service custom`
(CLI Reference, pp. 104–112). For this volume's switches:

| Item | FS-108F, FS-124F (S1, S2) | 200 Series (S3) | Source |
| --- | --- | --- | --- |
| Ingress ACL | Check (standalone only; note 16 lists both models as having no ACL in FortiLink mode) | Chain | Feature matrix |
| ACL service | Check | Check | Feature matrix |
| Prelookup and egress ACL | Dash | Dash | Feature matrix |
| Multiple ingress ACLs (groups) | Dash | Check | Feature matrix |
| Classifier fields | Only `dst-ip-prefix`, `dst-mac`, `ether-type`, `service`, `src-ip-prefix`, `src-mac`, `vlan-id` | All ingress fields, including `cos` and `dscp` | Administration Guide, p. 293 |
| Actions | Only `cos-queue`, `count`, `drop`, `outer-vlan-tag`, `redirect`; not `drop` with `redirect` | All ingress actions, including `remark-cos` and `remark-dscp` | Administration Guide, p. 293 |
| Byte counters | Always 0 (packet counters work) | Available | Administration Guide, p. 302 |
| Classifier change limit | A classifier created with only Layer 2 fields cannot later take Layer 3 fields, and the reverse | — | Administration Guide, p. 293 |

Two details matter for testing. Ping packets addressed to one of the switch's
own IP addresses are redirected to the CPU **before** the ingress ACL, so an
ingress ACL cannot drop them; the guide points to prelookup or egress ACLs for
that (p. 296), which this volume's switches do not have. And ACL groups other
than group 1 hold user rules; group 1 holds internal rules that always win
(p. 295). `get switch acl usage` shows the free rules and counters, and `get
switch acl counters` the per-policy packets (pp. 295, 303).

### Private VLANs

A private VLAN divides a **primary** VLAN into secondary VLANs that keep its
subnet (Administration Guide, pp. 355–356). Ports in the single **isolated**
VLAN reach only **promiscuous** ports; ports in a **community** VLAN reach each
other and the promiscuous ports; no secondary VLAN reaches another. On the
switch, `config switch vlan` sets `private-vlan enable`, `isolated-vlan`, and
`community-vlans` on the primary VLAN, and each port is set to `private-vlan
promiscuous` or `sub-vlan`. The 7.6.7 matrix marks private VLANs as a dash in
the 1xxE/1xxF column and a check (standalone only) in the 200 Series column,
which is why Chapter 01's capability matrix gives S3 "Live (SA)" for them and
Lab 8.5 left them to this chapter.

### QoS marking with ACL remark actions

Chapter 10 classified and queued traffic; **marking** rewrites the priority
that a packet carries. FortiSwitchOS marks with ingress ACL actions:
`remark-cos` sets the 802.1Q CoS value and `remark-dscp` the DSCP value of
matching packets (CLI Reference, pp. 105–108). Marking does not change the
switch's own queuing, which still uses the trust maps and the original values
(Administration Guide, p. 366). QoS marking is a dash in the 1xxE/1xxF column
and a check in the 200 Series column, so the remark step of Lab 11.4 runs on S3
only; on the FS-1xx models the ingress actions do not include remarking at all
(p. 293).

Two related standalone items appear in Chapter 10's model table and are not run
here: real-time egress queue rates (`diagnose switch physical-ports qos-rates`,
a check in the 200 Series column and only the FS-148F models in the 1xx column,
note 11) and the drop policy (`qos-drop-policy` under `config switch global`;
tail-drop is a check in both columns, RED a check only in the 200 Series
column). Lab 11.4 reads the queue rates on S3 as an optional step.

### FortiEdge Cloud

FortiEdge Cloud is Fortinet's cloud service for managing FortiSwitch units (and
other devices) without a FortiGate. The 7.6.7 documents use two names for the
switch side of it: the Administration Guide's introduction sends FortiEdge Cloud
users to the FortiEdge Cloud User Guide (p. 11), while its GUI page is
**System > FortiLAN Cloud** (pp. 13–14), the CLI table is `config system
flan-cloud` ("FortiLAN Cloud or FortiLink over HTTPS", CLI Reference, p. 230),
and the feature matrix row is "FortiEdge Cloud configuration". This chapter
follows the documents and treats them as one service.

| `config system flan-cloud` option | Meaning (CLI Reference, p. 230) | Default in the reference |
| --- | --- | --- |
| `status` | Whether the cloud client (or FortiLink over HTTPS) is active | `disable` |
| `service-type` | `flan-cloud` for the cloud, `fortilink-https` for FortiLink over HTTPS | `flan-cloud` |
| `name` | The cloud FQDN or address, or the FortiLink address for HTTPS | `fortiswitch-dispatch.forticloud.com` |
| `port` | The TCP port used to reach it | 443 |
| `interval` | Seconds allowed for DNS resolution | 3 |
| `source-ip` | Source address toward the manager | `0.0.0.0` |

`get system flan-cloud` shows the settings and `get system flan-cloud-mgr
connection-info` the state of the SSL tunnel (CLI Reference, pp. 519–520). The
switch never takes a FortiCloud user name or password: the account side of
FortiEdge Cloud (adding the switch to an inventory, licensing, and
configuration) happens in the FortiEdge Cloud portal, which this volume's local
references do not document. Treat the portal steps in Lab 11.5 as "follow the
FortiEdge Cloud User Guide and record what you did".

### Where the sources differ

| Topic | One source | Another source | This chapter |
| --- | --- | --- | --- |
| Cloud client default | FortiLink Guide: FortiLAN Cloud is enabled in the zero-touch defaults (p. 15) | CLI Reference: `status` default `disable` (p. 230) | Lab 11.1 records the value and sets `disable` |
| Edge-port default | CLI Reference: `edge-port` default `disable` (p. 130) | Administration Guide: STP and edge port are enabled on all ports (p. 268) | Sets `edge-port enabled` explicitly on the endpoint ports |
| Private-VLAN port options | Administration Guide example sets `primary-vlan` and `sub-vlan` on ports (p. 356) | CLI Reference's `config switch interface` syntax lists only `private-vlan` (p. 126) | Uses the guide's options; records what the switch accepts |
| `set-standalone` spelling | FortiLink Guide syntax line: `execute switch-controller switch-action set-standalone` | Its own example omits `switch-action` (p. 322) | Uses the syntax line (as Chapter 03) |
| Trunk example | Administration Guide: `set port-selection criteria src-dst-ip` (p. 166) | CLI Reference: `port-selection-criteria` (p. 180) | Leaves the default (`src-dst-ip`) |
| RED drop policy on FS-1xx | Administration Guide: RED can be set on the FS-124E, FS-148E, FS-124F, and FS-148F (p. 366) | Feature matrix: RED drop policy dash in the 1xxE/1xxF column | Not run; record if you try it |
| Restart on authorization | FortiLink Guide: after authorization the switch reboots in FortiLink mode (p. 41) | The same guide: a switch does not need to be restarted when it becomes managed (p. 14) | Lab 11.5 records which happens |
| Allowed VLAN list syntax | CLI Reference: `allowed-vlans {vlan1 vlan2 ...}` (p. 126) | Administration Guide examples: `set allowed-vlans 2,8` (pp. 166–167) | Uses the comma form of the guide's examples |

### Model support for this chapter

From the FortiSwitchOS 7.6.7 feature matrix (`temp/nse5fsw/fm767.txt`, the
position-based read); chain = standalone and managed, check = standalone only,
dash = not supported:

| Feature | 1xxE/1xxF (S1 FS-108F, S2 FS-124F) | 200 Series (S3) | Note |
| --- | --- | --- | --- |
| SVI | Chain | Chain | |
| Static routing (IPv4/IPv6) | Chain | Chain | Note 9: IPv4 only in managed mode |
| Software-based routing only | Check | Dash | |
| Hardware-based routing | Dash | Check | |
| DHCP server (IPv4) | Chain | Chain | Not used |
| OSPF, RIP, VRRP, policy-based routing | Dash | Check | Under "Requires Advanced Features License" |
| BGP | Dash | Dash | |
| Inter-VLAN routing offload | Dash | Dash | Note 19: advanced features license |
| Link aggregation group size | 8 | 8 | |
| MSTP instances | 0–31 | 0–31 | |
| STP root guard, BPDU guard, loop guard | Chain | Chain | |
| ACL (IPv4 ingress) | Check | Chain | Note 16 |
| ACL service (IPv4) | Check | Check | |
| Schedule for ACLs | Check | Check | Not used |
| Multiple ingress ACLs | Dash | Check | |
| ACL prelookup, ACL egress | Dash | Dash | |
| Private VLANs | Dash | Check | |
| QoS marking (IPv4/IPv6) | Dash | Check | ACL remark actions |
| Real-time egress queue rates | Only the 148F and 148F-POE in the column (note 11) | Check | Optional read on S3 |
| FortiEdge Cloud configuration | Check | Check | |
| FortiSwitch Manager | Check | Check | Not used |

## Design Considerations

### Exam tasks this chapter practices

| Exam task | Labs here | Track 2 mode |
| --- | --- | --- |
| 1.1 VLANs | 11.2 (primary) | Predict |
| 1.4 Switching and routing | 11.3 (primary), 11.2 | Predict |
| 1.5 STP | 11.2 (supporting) | Predict |
| 2.1 Configure and provision | 11.1, 11.5 (supporting) | Predict |
| 3.3 ACLs, security profiles, VLAN security | 11.4 (primary) | Predict |
| 1.2 QoS | 11.4 Part C (S3 marking) | Predict |

### How FSW-A leaves and rejoins FortiLink

| Step | Lab | Controller | Switch |
| --- | --- | --- | --- |
| Record and back up | 11.1 | `fgt-pre-11-1-174.conf`; `show` of the entry | Console capture of the managed configuration |
| Leave | 11.1 | `set-standalone`, then `fsw-wan1-admin disable`; the entry is kept | Factory defaults, reboot, FortiLink cable unplugged |
| Run standalone | 11.1–11.4 | Nothing changes | All configuration local |
| Back up standalone | 11.5 | — | `fsw-sa-11-174.conf` over TFTP |
| Rejoin | 11.5 | `disable-discovery` cleared, `fsw-wan1-admin enable` | `execute factoryreset`, FortiLink cable back |
| Check and back up managed | 11.5 | Chapter 10 state; `fgt-post-11-174.conf` | Console capture of the managed configuration |

Keeping the entry is the reason the round trip is cheap: the controller holds
every per-port and per-switch setting of Chapters 03–10. The alternative,
deleting the entry and adopting the switch from scratch as Lab 3.5 did, would
lose those settings; the restore path in Lab 11.5 (`fgt-pre-11-1-174.conf`)
exists for the case where they are lost anyway.

### Cabling while the switch is standalone

| Cable | Lab 11.1 | Labs 11.2–11.4 | Lab 11.5 (return) |
| --- | --- | --- | --- |
| Console | Connected | Connected | Connected |
| `mgmt` (or `port3`) to the Nexus port, VLAN 99 | Connected after the switch is configured | Connected | Unplugged; Nexus port shut |
| `<FSW_FL_PORT>` to the controller's FortiLink port | **Unplugged** as soon as `set-standalone` runs | Connected as an 802.1Q uplink carrying VLANs 1741 and 1743 | Connected (FortiLink) |
| `port1` endpoint A, `port2` endpoint B | Unplugged | Connected | Connected |
| `port5` loop cable (other end loose) | Unchanged | Unchanged; `port5` and `port6` form the test LAG | Unchanged |
| S3: `FSW-A` `port23`/`port24` to `FSW-B` | **Unplugged** before `set-standalone` | Unplugged | Connected after `FSW-A` is managed again |

The FortiLink cable and the endpoints stay unplugged in Lab 11.1 because a
freshly reset switch puts every port, the FortiLink port included, in VLAN 1:
with the Nexus cable also in VLAN 1 that would bridge the controller's FortiLink
network (and its DHCP server) into the out-of-band VLAN 99. On S3, `FSW-B`
reaches the controller only through `FSW-A` (Chapter 06), so it goes down while
`FSW-A` is standalone; unplugging the ICL keeps `FSW-B`'s MCLAG and FortiLink
traffic away from a switch that no longer runs them. `FSW-B` itself and its
controller entry are not changed.

### Addresses, VLANs, and names

| Item | Value | Where |
| --- | --- | --- |
| Management address | `10.30.99.174/24` on `<MGMT_IF>` (`mgmt`, or `internal` in local VLAN 99), gateway `10.30.99.1` | Lab 11.1 (Chapter 01 addressing plan) |
| Hostname | `fsw-a-sa-174` | Lab 11.1 |
| Admin trusted host | `<ADMIN_WS>`, the workstation you administer from (Volume CM's admin workstation is `10.30.12.172`) | Lab 11.1 |
| Switch VLANs | 1741 `fsw-users`, 1743 `fsw-iot` (descriptions); 99 `mgmt-174` on models without a management port | Lab 11.2 |
| Uplink | `<FSW_FL_PORT>` native VLAN 1 (unchanged), allowed `1741,1743` | Lab 11.2 |
| Test LAG | `lag-174`, `lacp-active`, members `port5` and `port6` | Lab 11.2 |
| MSTP | Region `lab-174-sa`, revision 1, instance 1 = VLANs 1741 and 1743, priority 16384 | Lab 11.2 |
| SVIs | `svi-users-174` `10.174.41.2/24` (VLAN 1741), `svi-iot-174` `10.174.43.2/24` (VLAN 1743) | Lab 11.3 |
| Static routes | 1: `0.0.0.0/0` via `10.30.99.1` on `<MGMT_IF>`; 2: `10.200.0.0/24` via `10.174.41.1` on `svi-users-174` | Labs 11.1, 11.3 |
| ACL objects | Service `icmp-echo-174`; ingress policies 1–3 (all options), 4 (S3) | Lab 11.4 |
| Private VLAN (S3) | Primary 1746 `pvlan-174`, isolated 1747, community 1748; test addresses `10.174.46.20` (B) and `10.174.46.30` (A) | Lab 11.4 |
| Backups on VM 140 | `fgt-pre-11-1-174.conf`, `fsw-sa-11-174.conf`, `fgt-post-11-174.conf` | Labs 11.1, 11.5 |
| Console captures | `fsw-managed-pre-11-174.txt`, `fsw-managed-post-11-174.txt` on the console host | Labs 11.1, 11.5 |

The SVI addresses `.2` sit outside the controller's DHCP range (`.100`–`.199`)
and next to the controller's `.1` gateways, because the uplink carries the same
VLANs to the controller: endpoint A keeps its DHCP lease from `fsw-users`, and
endpoint B keeps `10.174.43.20` with gateway `10.174.43.1`. VLANs 1746–1748 and
`10.174.46.0/24` exist only on `FSW-A` during Lab 11.4 Part B and are never
carried to the controller. All these names disappear with the factory reset in
Lab 11.5.

### The controller and the C2 budget

The controller changes only in three ways: the managed-switch entry is
deauthorized and authorized again, its `disable-discovery` list may gain and
lose `<SWITCH_SN>`, and its existing VLAN interfaces `fsw-users` and `fsw-iot`
serve the endpoints through the standalone switch in Labs 11.2–11.4. No
firewall policy, interface, or route is added; on C2, P3 stays free. The
switch's syslog test in Lab 11.3 uses the existing P2 (`FSW-LAN` to the
services segment, UDP 514 included).

The controller does not normally see tagged traffic from a switch it does not
manage on its FortiLink interface, and neither guide describes that case. Lab
11.2 tests it: if endpoint A gets no lease through the standalone switch,
record it and continue with the switch-only checks that the lab marks.

### Lab order and state

| Lab | Builds | Rollback leaves |
| --- | --- | --- |
| 11.1 | Standalone switch with hardened management; controller entry kept, deauthorized | Kept for Lab 11.2 (Lab 11.5 Part C is the full rollback) |
| 11.2 | VLANs 1741 and 1743, endpoint ports, uplink, `lag-174`, MSTP region | Kept; `lag-174` may be deleted |
| 11.3 | SVIs, static route 2, syslog to `ubuntu-ws`, endpoint host routes | Kept for Lab 11.4; endpoint host routes removed at the end of 11.4 |
| 11.4 | ACL service and policies; S3: private VLAN, remark policy | ACL objects and the private VLAN removed; endpoints back to their addresses |
| 11.5 | Optional cloud connection; standalone backup; switch managed again | Chapter 10 state (ADDENDUM 10), with managed backups |

Labs 11.2–11.4 build on each other and do not need individual rollbacks to
continue; each rollback says how to undo only that lab if you stop there.

### What carries into Chapter 12

At the end of Lab 11.5, `FSW-A` is managed again: `<SWITCH_SN>` is
`Authorized/Up` (at `10.255.1.2`, or the address Lab 11.5 records), with the
description, profile, ports, and STP settings of Chapter 10, the Lab 3.3
firmware, and on S3 `FSW-B` managed behind the ICL again. The controller has no
new objects. The Nexus port used for standalone management is shut. Nothing of
the standalone configuration remains on the switch; its copy is
`fsw-sa-11-174.conf` on VM 140. Chapter 12's last lab can return the switch to
standalone mode with the same `set-standalone` command.

## Implementation and Automation

The labs are the implementation. Four habits keep the round trip safe.

**Capture text you cannot get back.** The switch's managed configuration is
pushed by the controller, but a console capture of it is the only record of
what the switch actually ran. `picocom` writes everything it shows to a file
with `--logfile` (`picocom(1)`); if the output stops at a `--More--` prompt,
press the space bar:

```bash
picocom -b 9600 --logfile fsw-managed-pre-11-174.txt /dev/ttyUSB0
```

**Configure from the console before you cable.** Every change in Lab 11.1 is
made on the console with only the console cable connected, so that a
half-configured switch never touches the Nexus or the controller.

**Back up a standalone switch over TFTP.** With the management address in
place, the switch sends its configuration to VM 140 (CLI Reference, p. 410):

```text
FSW # execute backup config tftp fsw-sa-11-174.conf 10.30.99.50
```

**Test routed paths from both endpoints.** A route on one side is not enough:
endpoint A's default gateway is the controller, so a reply to a packet that the
switch routed returns through the controller unless endpoint A has a route back
through the switch. Lab 11.3 adds host routes on both endpoints (`ip-route(8)`):

```bash
# endpoint A
sudo ip route add 10.174.43.0/24 via 10.174.41.2
# endpoint B
sudo ip route add 10.174.41.0/24 via 10.174.43.2
```

The FortiSwitchOS configuration commands in this chapter were checked against
the FortiSwitchOS 7.6.7 CLI Reference with `temp/nse5fsw/verify.py`, and its
`execute`, `get`, and `diagnose` commands against the command lines that
reference prints. These were matched by hand: the VLAN-list values of
`allowed-vlans` (the comma form of the Administration Guide's examples,
pp. 166–167), `vlan-range` (CLI Reference, p. 177), and `community-vlans`
(p. 185), which the verifier cannot parse; the private-VLAN port options
`primary-vlan` and `sub-vlan`, which appear only in the Administration Guide's
example (p. 356) and not in the CLI Reference syntax; and `show` (the whole
configuration), `show switch acl service custom` (Administration Guide,
p. 300), `show system snmp community` (CLI Reference, p. 274), and, in the
troubleshooting table, `show system admin` and `show switch interface <port>`,
which are the `show` forms of documented tables. The FortiOS configuration
commands were checked against the FortiOS 7.6.0 CLI Reference; `execute
switch-controller switch-action set-standalone`, `execute switch-controller
get-conn-status`, and `execute switch-controller get-sync-status` against the
FortiLink Guide 7.6.7, and `execute backup config`, `execute restore config`,
`execute dhcp lease-list`, `execute ping`, and `diagnose sniffer packet`
against the FortiOS 8.0.1 CLI Reference as a cross-check. `unselect
disable-discovery` was matched by hand to the FortiLink Guide (p. 322), as in
Chapter 03. The Nexus lines follow Chapter 02, and the endpoint commands follow
`ip-address(8)`, `ip-route(8)`, `ip-link(8)`, `ping(8)`, `tcpdump(8)`,
`ssh(1)`, and `picocom(1)`.

## Validation and Troubleshooting

| Symptom | Likely cause | Check |
| --- | --- | --- |
| The switch rejoins the controller during the chapter | FortiLink discovery was not disabled, or the controller entry is still authorized | `get switch global`; `show switch-controller managed-switch <SWITCH_SN>` on the controller |
| No management access after Lab 11.1 | Wrong `<MGMT_IF>`; on a model without a management port, `port3` and `internal` are not both in VLAN 99; the Nexus port is shut | `get system interface physical`; `diagnose switch vlan list`; the Nexus port state |
| SSH refused from the workstation | The workstation is not `trusthost1`, or the account is locked out after failed logins | Log in on the console; `show system admin` |
| Two default routes, or remote access fails after a reboot | `mgmt` or `internal` still uses DHCP with `defaultgw enable` (zero-touch default) | `get router info routing-table all`; set `mode static` |
| Endpoint A gets no lease through the standalone switch | VLAN 1741 is not native on `port1` or not allowed on `<FSW_FL_PORT>`; or the controller does not accept tagged traffic from an unmanaged switch on its FortiLink interface (undocumented) | `diagnose switch vlan list`; `execute dhcp lease-list fsw-users` on the controller |
| `lag-174` stays down | No LACP partner (expected in this lab) | `diagnose switch trunk list` |
| Endpoint A cannot ping endpoint B although both SVIs answer | One endpoint lacks its host route, so the reply goes through the controller, which denies intrazone traffic | `ip route` on both endpoints |
| Syslog from the switch never reaches `ubuntu-ws` | Static route 2 missing or disabled; `source-ip` is not in `fsw-users`; P2 does not include `FSW-LAN` | `get router info routing-table all`; `diagnose sniffer packet` on the controller |
| An ACL is refused | The FS-1xx models accept only the classifier fields and actions on p. 293, and a classifier cannot mix Layer 2 and Layer 3 fields after creation | Recreate the policy with supported fields |
| An ACL does not drop pings to a switch address | Pings to local addresses go to the CPU before the ingress ACL (p. 296) | Expected |
| ACL byte counters stay at 0 | FS-1xxE and FS-1xxF have packet counters only (p. 302) | Expected |
| Private-VLAN ports do not isolate | `primary-vlan` or `sub-vlan` refused or unset; the model is not a 200 Series switch | `get switch vlan`; `show switch interface <port>` |
| The cloud tunnel does not come up | No DNS server, no route to the internet, the switch is not in a FortiEdge Cloud inventory, or `status disable` | `get system dns`; `get system flan-cloud-mgr connection-info` |
| After the return, the switch stays `Discovered` or is not seen | It is still in `disable-discovery`, the entry is still deauthorized, or it was not reset | `show switch-controller global`; `get-conn-status` |
| After the return, ports are at defaults | The deauthorized entry did not keep its port settings | Restore `fgt-pre-11-1-174.conf` (Lab 11.5 Part C) |

## Security and Best Practices

- **Decide who manages each switch, and remove the others.** A reset switch
  looks for every kind of manager at once (pp. 14–15); a standalone switch
  should have FortiLink discovery, auto topology, and the cloud client off, and
  a cloud-managed switch should be removed from the cloud inventory before it is
  handed to a FortiGate.
- **Keep management out of the default VLAN.** On models without a management
  port, put `internal` and the management uplink in a VLAN that no user port is
  in (Volume CLXXII P10); leave unused ports in a VLAN that reaches nothing.
- **Limit administrative access in three places**: `allowaccess` per interface
  (no HTTP or Telnet), trusted hosts per administrator, and lockout and idle
  timeout globally. Keep console access as the recovery path.
- **Remove the factory SNMP community.** A reset creates a community named
  `public` (CLI Reference, p. 274); if SNMP is needed, use SNMPv3 (Chapter 12).
- **Remember that switch routing bypasses the firewall.** SVIs on two VLANs
  join them inside the switch; put inter-VLAN policy on the FortiGate by not
  routing on the switch, or enforce it on the switch with ACLs.
- **Write ACLs for the hardware you have.** Check the model's classifier and
  action list, check `get switch acl usage` before and after, and remember that
  traffic to the switch itself is not filtered by ingress ACLs.
- **Mark priority only at the trust boundary.** Remark traffic where it enters
  from untrusted hosts, so that downstream devices that trust DSCP see values
  you set.
- **Never type cloud credentials outside the cloud portal.** FortiEdge Cloud
  credentials belong only in Fortinet's FortiCloud sign-in page; the switch, the
  lab hosts, and this volume never need them.
- **Back up before every change of manager.** A change of manager discards
  the switch's configuration in both directions (FortiLink Guide, p. 34).

## References and Knowledge Checks

**References**

- [Fortinet, *FortiSwitchOS 7.6.7 Administration Guide (Standalone Mode)*](https://docs.fortinet.com/document/fortiswitch/7.6.7/administration-guide)
  — managers and FortiEdge Cloud pointer (p. 11), FortiLAN Cloud page
  (pp. 13–14), management ports and examples (pp. 17–24), SVIs (pp. 24–26),
  administrator password, lockout, idle timeout, and banners (pp. 73–75, 86),
  disabling FortiLink (pp. 139–140), link aggregation groups (pp. 164–167),
  MSTP configuration (pp. 264–271), ACL notes, groups, ingress policies,
  services, counters, and examples (pp. 292–304), VLAN frame processing
  (pp. 341–344), private VLANs (pp. 355–356), QoS model notes and marking
  (p. 366), auto topology (p. 384), static routes (pp. 484–486).
- [Fortinet, *FortiSwitchOS 7.6.7 CLI Reference*](https://docs.fortinet.com/document/fortiswitch/7.6.7/fortiswitchos-cli-reference)
  — `config log syslogd setting` (p. 29), `config router static` (pp. 96–97),
  `config switch acl ingress` (pp. 104–108), `config switch acl service custom`
  (pp. 110–112), `config switch auto-network` and `config switch global`
  (pp. 114–115), `config switch interface` (pp. 126–131), `config switch stp
  instance` and `settings` (pp. 177–179), `config switch trunk` (pp. 179–182),
  `config switch vlan` (pp. 184–190), `config system flan-cloud` (p. 230),
  `config system snmp community` (p. 274), `diagnose stp` (pp. 341–343),
  `diagnose switch trunk` (pp. 379–381), `diagnose switch vlan list` (p. 383),
  `execute backup config` (pp. 410–411), `execute factoryreset` (pp. 420–421),
  `execute switch-controller get-conn-status` (p. 451), `get router info
  routing-table` (pp. 485–486), `get switch acl` (p. 493), `get switch vlan`
  (p. 512), `get system flan-cloud` and `flan-cloud-mgr connection-info`
  (pp. 519–520), `get system interface physical` (p. 525), `get system status`
  (p. 535).
- [Fortinet, *FortiLink Guide (FortiOS 7.6.7)*](https://docs.fortinet.com/document/fortiswitch/7.6.7/fortilink-guide)
  — zero-touch management, one manager at a time, and factory defaults
  (pp. 14–15), migrating standalone configurations with `fortilinkify.py`
  (p. 34), FortiLink with HTTPS and `flan-cloud-mgr` output (pp. 50–52),
  converting to standalone mode and `disable-discovery` (p. 322).
- [Fortinet, FortiOS 7.6 documentation](https://docs.fortinet.com/product/fortigate/7.6)
  — the FortiOS 7.6.0 CLI Reference: `config switch-controller managed-switch`
  (`fsw-wan1-admin`), `config switch-controller global` (`disable-discovery`).
- FortiOS 8.0.1 CLI Reference (cross-check only) — `execute backup config`,
  `execute restore config`, `diagnose sniffer packet`.
- FortiSwitchOS 7.6.7 feature matrix (`temp/fsw/FSW-7.6.7-Feature-Matrix.pdf`)
  — the System, Layer 2, Layer 3, Security, and Quality of Service rows used in
  the model table; notes 9, 11, 16, and 19.
- [Volume CLXXII, Chapter 11](../../volume-172-disa-srgs-and-stigs/chapters/11-fortiswitch-feature-version-and-srg-map.md)
  — prerequisites P10 (management interface), P13 (VLANs), and P16 (FortiEdge
  Cloud or FortiSwitch Manager).
- [`picocom(1)`](https://manpages.ubuntu.com/manpages/noble/man1/picocom.1.html),
  [`ip-address(8)`](https://manpages.ubuntu.com/manpages/noble/man8/ip-address.8.html),
  [`ip-route(8)`](https://manpages.ubuntu.com/manpages/noble/man8/ip-route.8.html),
  [`ip-link(8)`](https://manpages.ubuntu.com/manpages/noble/man8/ip-link.8.html),
  [`ping(8)`](https://manpages.ubuntu.com/manpages/noble/man8/ping.8.html),
  [`tcpdump(8)`](https://manpages.ubuntu.com/manpages/noble/man8/tcpdump.8.html),
  [`ssh(1)`](https://manpages.ubuntu.com/manpages/noble/man1/ssh.1.html).

**Knowledge checks**

1. Name the two controller commands that return a managed switch to standalone
   mode, and the one difference between them.
2. What remains on the controller after `set-standalone`, and why does this
   chapter keep it?
3. Which zero-touch features must you turn off on a switch that will stay
   standalone, and why must you repeat that after every factory reset?
4. On a model without a dedicated management port, which interface carries the
   management address, and how is it reached from the network?
5. In FortiSwitchOS, what is a trunk, and what does an LACP trunk member do if
   it receives no LACP from a partner?
6. An untagged frame arrives on a port with native VLAN 1743 and allowed VLANs
   1741. Which VLAN does it join? A frame tagged 1745 arrives on the same port.
   What happens to it?
7. Why does traffic routed between two SVIs on the switch escape the
   controller's `FSW-LAN` intrazone deny?
8. Which Layer 3 features need the Advanced Features license, and which of them
   are available on the FS-124F?
9. List the ingress ACL classifier fields and actions available on an FS-124F.
   Why does an ingress ACL not drop a ping to one of the switch's own addresses?
10. In a private VLAN, which ports can an isolated port reach? Which can a
    community port reach?
11. Does an ACL `remark-dscp` action change the egress queue that the marking
    switch uses?
12. Where are FortiEdge Cloud credentials entered, and what does the switch
    itself need to reach the service?
13. What happens to a standalone switch's configuration when it is converted to
    FortiLink mode, and what tool does Fortinet offer for it?

## Hands-On Lab

**Shared prerequisites.** Chapter 10 complete (ADDENDUM 10 state):
`<SWITCH_SN>` `Authorized/Up` at `10.255.1.2`, description `FSW-A lab-174`,
profile `fsw-174-prof` (on S3, `FSW-A`; `FSW-B` managed behind the MCLAG ICL on
`port23`/`port24`); `port1` native `fsw-users` (endpoint A, DHCP, BPDU guard,
allowed list `<PORT1_ALLOWED>`), `port2` native `fsw-iot` (endpoint B,
`10.174.43.20/24`, BPDU guard, allowed list `<PORT2_ALLOWED>`); the controller
in single-VDOM mode with VLAN interfaces `fsw-users` (1741, `10.174.41.1/24`,
DHCP `.100`–`.199`) and `fsw-iot` (1743, `10.174.43.1/24`) in zone `FSW-LAN`
with intrazone deny, P1 and P2 as Chapter 04 left them, and on C2 P3 free.
`ubuntu-ws` runs the rsyslog UDP listener from Lab 2.5. The Nexus port
`Eth1/<free>` from Lab 2.4 (access VLAN 99, edge, no BPDU guard) is shut.
Endpoints have `tcpdump`; endpoint B has `iperf`. Track 2: nothing beyond the
controller. **Optional:** a FortiCloud account for Lab 11.5 Part A. **Cost:**
none (FortiEdge Cloud licensing, if any applies to your account, is outside this
volume).

`FGT #` is the controller on any option and `FSW #` the switch console (or SSH
once Lab 11.1 is done). `<MGMT_IF>` is `mgmt` on a model with a dedicated
management port and `internal` on one without. `<IFACE>` and `<IFACE_B>` are
endpoint A's and endpoint B's wired interfaces, and `<LEASE_A>` endpoint A's
current `fsw-users` address (`ip -br addr show <IFACE>`). `<ADMIN_WS>` is your
administration workstation's address. Your recorded switch admin password is
the one Chapter 02 set and `fsw-174-prof` enforces.

### Lab 11.1 — Leave FortiLink mode and bring the switch up standalone

**Objective:** Record and back up the managed state, convert `FSW-A` to
standalone mode while keeping its controller entry, and bring it up from the
console with zero-touch features off, a static management address, and
hardened administrative access; show that it does not rejoin the controller.

**Platform notes:** Hands-on on C1, C2, and C3 with S1, S2, or S3 (on S3,
`FSW-A` only; its ICL cables are unplugged first and `FSW-B` goes down until Lab
11.5). Models with a dedicated management port use `mgmt`; models without one use
`internal` through `port3` (step 6's `get system interface physical` lists
`mgmt` only on a model that has the port). The
switch reboots once; allow 20 minutes. No policy, interface, or route is added
on the controller. Track 2: read-and-predict.

**Track 1, Part A — record and leave:**

1. Record the managed state and back up the controller. Save the output of the
   `show` command in your notes; it is the reference for Lab 11.5:

   ```text
   FGT # execute switch-controller get-conn-status
   FGT # show switch-controller managed-switch <SWITCH_SN>
   FGT # show switch-controller global
   FGT # execute backup config tftp fgt-pre-11-1-174.conf 10.30.99.50
   ```

2. Capture the switch's managed configuration from the console into a file
   (see Implementation and Automation), then log out:

   ```bash
   picocom -b 9600 --logfile fsw-managed-pre-11-174.txt /dev/ttyUSB0
   ```

   ```text
   FSW # get system status
   FSW # show
   ```

   Record `Version` (the Lab 3.3 build) and `Serial-Number`.

3. S3 only: unplug `FSW-A`'s `port23` and `port24` (the ICL to `FSW-B`). After a
   minute, `get-conn-status` shows `FSW-B` no longer `Up`; record its STATUS.

4. Convert the switch. It returns to factory defaults and reboots (FortiLink
   Guide 7.6.7, p. 322). As soon as the console shows the switch restarting,
   unplug the cables in `<FSW_FL_PORT>`, `port1`, and `port2` (leave the
   console), so that the reset switch boots with no path to the controller:

   ```text
   FGT # execute switch-controller switch-action set-standalone <SWITCH_SN>
   ```

5. Deauthorize the entry, but do not delete it, and read the result:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   set fsw-wan1-admin disable
   next
   end
   FGT # execute switch-controller get-conn-status
   FGT # show switch-controller global
   ```

   Record the STATUS of `<SWITCH_SN>` and whether `set-standalone` added it to
   `disable-discovery` (Chapter 03 recorded what your build did). Then run
   `show switch-controller managed-switch <SWITCH_SN>` and compare it with step
   1: the description, profile, and `config ports` settings should still be
   there. Record any difference; Lab 11.5 depends on them.

**Track 1, Part B — first boot from the console:**

6. Log in as `admin` with no password and set your recorded password when
   prompted (Administration Guide, p. 73). Read the defaults before changing
   anything:

   ```text
   FSW # get system status
   FSW # get switch global
   FSW # get system flan-cloud
   FSW # get system interface physical
   FSW # execute switch-controller get-conn-status
   ```

   Predict: `Version` is still the Lab 3.3 build; `get switch global` shows
   `auto-fortilink-discovery` and `auto-isl` enabled; `mgmt` and `internal` use
   DHCP. Record the cloud client's `status`: the FortiLink Guide lists FortiLAN
   Cloud as enabled by default (p. 15) and the CLI Reference gives `disable`
   (p. 230). `get-conn-status` on the switch reports no FortiLink session.

7. Turn off the zero-touch features so that the switch neither forms ISLs,
   answers FortiLink discovery, nor calls the cloud (Administration Guide,
   pp. 139–140 and 384):

   ```text
   FSW # config switch auto-network
   set status disable
   end
   FSW # config switch global
   set auto-fortilink-discovery disable
   set auto-isl disable
   end
   FSW # config system flan-cloud
   set status disable
   end
   ```

8. Give the switch its management address and a default route. On a model with
   a dedicated management port:

   ```text
   FSW # config system interface
   edit mgmt
   set mode static
   set ip 10.30.99.174 255.255.255.0
   set allowaccess ping https ssh
   next
   end
   FSW # config router static
   edit 1
   set dst 0.0.0.0 0.0.0.0
   set gateway 10.30.99.1
   set device mgmt
   next
   end
   ```

   On a model without one, create a local management VLAN, move `internal` and
   `port3` into it, and put the address on `internal`. `internal` is a switch
   interface with a native VLAN of its own (FortiLink Guide, p. 15; auto
   topology sets it to 4094); the guides show no example of setting it by
   hand, so record whether the switch accepts it, and if it does not, leave
   `internal` and `port3` in VLAN 1 as in Chapter 02:

   ```text
   FSW # config switch vlan
   edit 99
   set description "mgmt-174"
   next
   end
   FSW # config switch interface
   edit "internal"
   set native-vlan 99
   next
   edit "port3"
   set native-vlan 99
   next
   end
   FSW # config system interface
   edit internal
   set mode static
   set ip 10.30.99.174 255.255.255.0
   set allowaccess ping https ssh
   next
   end
   FSW # config router static
   edit 1
   set dst 0.0.0.0 0.0.0.0
   set gateway 10.30.99.1
   set device internal
   next
   end
   ```

9. Harden administrative access. First record the current values, then set
   the idle timeout explicitly to the 5-minute default, which the CLI Reference
   advises keeping (p. 236); keep the lockout threshold at its default of 3
   failed logins and lengthen the lockout from the default 60 seconds to 300
   (p. 235); and add a banner, a hostname, and a trusted host for the `admin`
   account. The guides do not say whether trusted hosts also apply to the
   console; keep the console connected in case you lock yourself out of the
   network logins:

   ```text
   FSW # get system global
   FSW # show system snmp community
   FSW # config system global
   set hostname fsw-a-sa-174
   set admintimeout 5
   set admin-lockout-threshold 3
   set admin-lockout-duration 300
   set pre-login-banner "Authorized lab use only (Volume CLXXIV)"
   end
   FSW # config system admin
   edit "admin"
   set trusthost1 <ADMIN_WS> 255.255.255.255
   next
   end
   ```

   If `show system snmp community` lists the `public` community that a factory
   reset creates (CLI Reference, p. 274), note its entry ID as
   `<COMMUNITY_ID>` and delete it; `allowaccess` already excludes SNMP:

   ```text
   FSW # config system snmp community
   delete <COMMUNITY_ID>
   end
   ```

10. Cable `<MGMT_IF>`'s port (`mgmt`, or `port3`) to the Nexus port and enable
    it:

    ```text
    interface Ethernet1/<free>
      no shutdown
    ```

    Then check reachability and the routing table from the switch:

    ```text
    FSW # execute ping 10.30.99.1
    FSW # execute ping 10.30.99.50
    FSW # get router info routing-table all
    ```

    Predict the routing table. **Answer:** a connected route for
    `10.30.99.0/24` on `<MGMT_IF>` and the static default via `10.30.99.1`, in
    the shape the CLI Reference prints (`S>* 0.0.0.0/0 [...] via ...`, p. 486);
    nothing learned from DHCP.

11. From `<ADMIN_WS>`, log in over SSH, see the banner, and list the sessions:

    ```bash
    ssh admin@10.30.99.174
    ```

    ```text
    FSW # get system admin list
    ```

    The session shows `sshv2` on `<MGMT_IF>` from `<ADMIN_WS>`.

**Track 2: read-and-predict.**

1. The CLI Reference prints this `get system status`, trimmed (p. 535):

   ```text
   S124EN4N17002351 # get system status
   Version: FortiSwitch-124E v7.6.2,build1071,250326 (Interim)
   Serial-Number: S124EN4N17002351
   Firmware Signature: invalid
   Hostname: S124EN4N17002351
   ```

   After `set-standalone` and the steps above, predict which of these lines
   change on your switch. **Answer:** only `Hostname`, which becomes
   `fsw-a-sa-174`; a reset does not change the firmware image or the serial
   number. At factory defaults the hostname is the serial number, as in the
   reference's example, until you set one.
2. A colleague runs `execute switch-controller factory-reset <switch-id>`
   instead of `set-standalone`, and leaves the FortiLink cable connected and
   automatic authorization on. Predict. **Answer:** the switch comes back with
   FortiLink auto-discovery and can be detected and automatically authorized
   again (FortiLink Guide, p. 322), so it is managed, not standalone.
3. A standalone switch keeps the zero-touch DHCP settings on both `mgmt` and
   `internal`, and both networks offer a default gateway. Predict. **Answer:**
   the switch installs both default routes and uses ECMP between them, which the
   FortiLink Guide warns can break management; it recommends `set defaultgw
   disable` on the interface not used for management (p. 15).

**Expected result:** Track 1: `fgt-pre-11-1-174.conf` and
`fsw-managed-pre-11-174.txt` exist; the controller entry is deauthorized and
still holds its settings; the switch runs standalone at `10.30.99.174` with
auto topology, FortiLink discovery, and the cloud client off, a static default
route, hardened access, and no `public` community; SSH works from `<ADMIN_WS>`.
Track 2: the predictions are answered.

**Negative test:** From VM 140 (`10.30.99.50`), which is not a trusted host,
try to log in:

```bash
ssh admin@10.30.99.174
```

Predict: the switch refuses the login. Record how (closed connection or a
message) and whether VM 140's `ping 10.30.99.174` is answered: the guides do
not say whether trusted hosts also restrict ping on FortiSwitchOS. Then check on
the controller that `<SWITCH_SN>` is not `Authorized/Up`
(`execute switch-controller get-conn-status`). Track 2: prediction 2 is the
negative test.

**Rollback:** None before Lab 11.2: the standalone switch is the base for Labs
11.2–11.4. If you stop the chapter here, run Lab 11.5 Part C, which resets the
switch and returns it to the controller.

**Lab verified by:** *pending*

### Lab 11.2 — Standalone VLANs, an 802.1Q uplink, a LAG, and local MSTP

**Objective:** Create VLANs 1741 and 1743 on the standalone switch, make
`port1` and `port2` access ports with BPDU guard, carry both VLANs tagged to
the controller on `<FSW_FL_PORT>` so that the endpoints keep their gateways,
build a LACP trunk and read why it stays down, and configure a local MSTP
region with `FSW-A` as the instance 1 root.

**Platform notes:** Hands-on on S1, S2, and S3 with any controller option:
VLANs, LAGs (up to 8 members), MSTP (instances 0–31), and BPDU guard are in
both matrix columns. The controller only serves `fsw-users` and `fsw-iot` as
before; whether it accepts their tagged frames from a switch it does not manage
is undocumented, so step 4 records it. Track 2: read-and-predict.

**Track 1:**

1. Create the VLANs and read the VLAN table (CLI Reference, p. 184):

   ```text
   FSW # config switch vlan
   edit 1741
   set description "fsw-users"
   next
   edit 1743
   set description "fsw-iot"
   next
   end
   FSW # diagnose switch vlan list
   ```

   Predict: VLAN 1 still lists almost every port; VLANs 1741 and 1743 list no
   port yet; on a model without a management port, VLAN 99 lists `port3` and
   `internal`.

2. Make the endpoint ports access ports with descriptions, edge ports, and BPDU
   guard (BPDU guard needs STP and edge port enabled on the port, CLI
   Reference, p. 131), and make the uplink carry both VLANs tagged. The uplink's
   native VLAN stays 1, as it was on the FortiLink port:

   ```text
   FSW # config switch interface
   edit "port1"
   set native-vlan 1741
   set description "endpoint A"
   set edge-port enabled
   set stp-bpdu-guard enabled
   next
   edit "port2"
   set native-vlan 1743
   set description "endpoint B"
   set edge-port enabled
   set stp-bpdu-guard enabled
   next
   edit "<FSW_FL_PORT>"
   set allowed-vlans 1741,1743
   set description "uplink to controller"
   next
   end
   ```

3. Plug the cables back into `<FSW_FL_PORT>`, `port1`, and `port2`, and read the
   result:

   ```text
   FSW # diagnose switch vlan list
   FSW # get switch interface
   FSW # diagnose switch mac-address list
   ```

   Predict: VLAN 1741 lists `port1` and `<FSW_FL_PORT>`, VLAN 1743 lists `port2`
   and `<FSW_FL_PORT>`; after the endpoints send traffic, the MAC table shows
   endpoint A's MAC in VLAN 1741 on `port1`, endpoint B's in VLAN 1743 on
   `port2`, and the controller's MAC on `<FSW_FL_PORT>` in both VLANs.

4. Renew endpoint A's lease and test both endpoints:

   ```bash
   # endpoint A
   sudo ip link set <IFACE> down && sudo ip link set <IFACE> up
   sleep 10; ip -br addr show <IFACE>
   ping -c 3 10.174.41.1
   # endpoint B
   ping -c 3 10.174.43.1
   ```

   ```text
   FGT # execute dhcp lease-list fsw-users
   FGT # execute switch-controller get-conn-status
   ```

   Record `<LEASE_A>`. Predict: endpoint A leases an address from `.100`–`.199`
   and both pings answer, because the frames reach the controller's VLAN
   interfaces tagged exactly as they did from the managed switch. If endpoint A
   gets no lease or the pings fail, record it as the controller's behavior with
   an unmanaged switch on its FortiLink interface, give endpoint A
   `10.174.41.30/24` by hand for Labs 11.3 and 11.4, and skip the steps that
   need the controller. In `get-conn-status`, record how `<SWITCH_SN>` appears
   now that its LLDP reaches the controller again (for example `Discovered`, or
   not listed); it must not be `Authorized/Up`.

5. Predict whether endpoint A can ping endpoint B (`10.174.43.20`), then try.
   **Answer:** no. Both endpoints use the controller as their gateway, so the
   traffic crosses the controller, where the `FSW-LAN` intrazone deny blocks
   it; the standalone switch only bridges.

6. Build a LACP trunk on `port5` and `port6` (the loop cable's free end stays
   loose) and read it (CLI Reference, pp. 179–181):

   ```text
   FSW # config switch trunk
   edit "lag-174"
   set mode lacp-active
   set members "port5" "port6"
   set description "test LAG, no partner"
   next
   end
   FSW # diagnose switch trunk summary
   FSW # diagnose switch trunk list
   ```

   Predict the status and partner. **Answer:** `down(0/2)`, with no active port;
   `port5`'s link is down because nothing is at the far end of its cable, and
   `port6` has no cable; the partner MAC address is `00:00:00:00:00:00`, as in
   the CLI Reference's example of a trunk without a partner (p. 380).

7. Configure the MSTP region and instance 1 (CLI Reference, pp. 177–179), then
   read them:

   ```text
   FSW # config switch stp settings
   set name lab-174-sa
   set revision 1
   end
   FSW # config switch stp instance
   edit 1
   set priority 16384
   set vlan-range 1741 1743
   next
   end
   FSW # diagnose stp mst-config list
   FSW # diagnose stp instance list 1
   ```

   Predict: the MST configuration name `lab-174-sa`, revision 1, instance 1
   mapped to VLANs 1741 and 1743 with priority 16384; in instance 1 the switch
   is the regional root, `port1` and `port2` are designated and forwarding with
   the `ED` (edge) flag, and `<FSW_FL_PORT>` is designated (the controller's
   FortiLink interface runs no STP, Chapter 05). On a model without a management
   port, also run `diagnose stp instance list 0` and record which bridge is the
   CIST root: `port3` connects to the Nexus, which runs its own spanning tree on
   VLAN 99, so the CIST root may be outside the switch.

**Track 2: read-and-predict.**

1. The CLI Reference prints this trunk summary (p. 381), trimmed:

   ```text
   S524DF4K15000024 # diagnose switch trunk summary
   Trunk Name       Mode                   PSC        MAC               Status
   Mclag-icl-trunk  lacp-active(mclag-icl) N/A        08:5B:0E:F1:95:F4 down(0/2)
   8DN3X16000001-0  lacp-active(auto-isl)  src-dst-ip 08:5B:0E:F0:9B:90 up(1/1)
   ```

   Predict the line for `lag-174` with two members and no partner, and what
   changes if a second switch runs `lacp-passive` on the other end of both
   links. **Answer:** `lag-174 lacp-active N/A ... down(0/2)`; with a partner
   it becomes `up(2/2)` with a port selection algorithm, because LACP active
   and passive ends bundle (Administration Guide, pp. 165–166 show exactly that
   pair).
2. A port has native VLAN 1743 and allowed VLANs 1741. Predict the VLAN of an
   untagged frame, and what happens to a frame tagged 1745. **Answer:** the
   untagged frame joins VLAN 1743; the tagged 1745 frame is dropped at ingress,
   because 1745 is neither allowed nor native (Administration Guide, p. 342).
3. The CLI Reference prints this MST configuration (p. 343):

   ```text
   S524DF4K15000024 # diagnose stp mst-config list
   MST Configuration Name: region1
   MST Configuration Revision: 1
   Instance ID Mapped VLANs Priority
   0                        32768
   1                        8192
   ```

   A second switch has the same name and revision but maps VLAN 1743 to
   instance 2. Predict. **Answer:** the configuration digests differ, so the
   two switches are in different MST regions, and instance 1 does not span
   both (Chapter 05).

**Expected result:** Track 1: VLANs 1741 and 1743 exist; `port1` and `port2` are
access ports with BPDU guard; the uplink carries both VLANs tagged; endpoint A
leased `<LEASE_A>` and endpoint B reached `10.174.43.1` through the standalone
switch (or the controller's refusal is recorded); A could not reach B;
`lag-174` is down with no partner; region `lab-174-sa` revision 1 has `FSW-A` as
instance 1 root. Track 2: the predictions are answered.

**Negative test:** Remove VLAN 1743 from the uplink and test endpoint B again:

```text
FSW # config switch interface
edit "<FSW_FL_PORT>"
set allowed-vlans 1741
next
end
```

Predict: endpoint B's ping to `10.174.43.1` fails while endpoint A's still
works; VLAN 1743 now lists only `port2` in `diagnose switch vlan list`. Put the
list back with `set allowed-vlans 1741,1743` and confirm that endpoint B's ping
answers again. Track 2: prediction 2 is the negative test.

**Rollback:** Keep the VLANs, ports, and MSTP settings for Lab 11.3. To undo
only this lab's trunk and MSTP instance:

```text
FSW # config switch trunk
delete "lag-174"
end
FSW # config switch stp instance
delete 1
end
```

The factory reset in Lab 11.5 Part C removes the VLANs and the port settings.

**Lab verified by:** *pending*

### Lab 11.3 — Switch virtual interfaces and static routes

**Objective:** Add SVIs on VLANs 1741 and 1743, route between endpoint A and
endpoint B on the switch and show that this bypasses the controller's intrazone
deny, add a static route toward the controller's services segment, and prove it
with syslog from the switch to `ubuntu-ws`.

**Platform notes:** Hands-on on S1, S2, and S3 with any controller option. SVIs
and static routing are chain in both columns; the FS-1xx models route in
software and the 200 Series in hardware, which changes performance, not the
steps. No dynamic routing (the Advanced Features license rows). The controller
gains no route or policy: the syslog test uses P2 (on C1, its source NAT). If
Lab 11.2 step 4 recorded that the controller does not pass traffic from the
standalone switch, run steps 1–4 and skip steps 5–7. Track 2: read-and-predict.

**Track 1:**

1. Create the SVIs (Administration Guide, pp. 19–20 and 24–25):

   ```text
   FSW # config system interface
   edit "svi-users-174"
   set interface internal
   set vlanid 1741
   set ip 10.174.41.2 255.255.255.0
   set allowaccess ping
   next
   edit "svi-iot-174"
   set interface internal
   set vlanid 1743
   set ip 10.174.43.2 255.255.255.0
   set allowaccess ping
   next
   end
   FSW # get system interface vlan
   FSW # get router info routing-table all
   ```

   Predict the routing table. **Answer:** connected routes for
   `10.174.41.0/24` on `svi-users-174` and `10.174.43.0/24` on `svi-iot-174`,
   in addition to the management subnet and the default route of Lab 11.1.

2. From each endpoint, ping its local SVI and the other SVI, without host routes
   yet:

   ```bash
   # endpoint A
   ping -c 3 10.174.41.2
   ping -c 3 10.174.43.2
   # endpoint B
   ping -c 3 10.174.43.2
   ```

   Predict. **Answer:** each local SVI answers. Endpoint A's ping to
   `10.174.43.2` goes to its default gateway, the controller, which routes it to
   `fsw-iot` and applies the `FSW-LAN` intrazone deny, so it fails; record the
   result.

3. Add host routes on both endpoints so that each reaches the other's subnet
   through the switch:

   ```bash
   # endpoint A
   sudo ip route add 10.174.43.0/24 via 10.174.41.2
   ping -c 3 10.174.43.20
   # endpoint B
   sudo ip route add 10.174.41.0/24 via 10.174.43.2
   ping -c 3 <LEASE_A>
   ```

   Predict the result and the TTL that endpoint A sees in the replies.
   **Answer:** both pings answer, with `ttl=63` from a Linux host (64 minus the
   one hop through the switch): the switch routes between its two SVIs and the
   traffic never reaches the controller, so the controller's intrazone deny does
   not apply. This is the security point of the lab.

4. Add a static route toward the services segment through the controller's
   `fsw-users` address (CLI Reference, p. 96):

   ```text
   FSW # config router static
   edit 2
   set dst 10.200.0.0 255.255.255.0
   set gateway 10.174.41.1
   set device svi-users-174
   set comment "services via controller"
   next
   end
   FSW # get router info routing-table static
   ```

   Predict: two static routes, the default via `10.30.99.1` on `<MGMT_IF>` and
   `10.200.0.0/24` via `10.174.41.1` on `svi-users-174`; the longer prefix wins
   for `ubuntu-ws`.

5. Send the switch's log to `ubuntu-ws` from the `fsw-users` address, so that
   P2 (source `FSW-LAN`, service `lab-svc-174` with UDP 514, destination
   `ubuntu-ws`) carries it (CLI Reference, p. 29):

   ```text
   FSW # config log syslogd setting
   set status enable
   set server 10.200.0.20
   set source-ip 10.174.41.2
   end
   ```

6. Generate events and watch them arrive. Log out of the SSH session and log in
   again from `<ADMIN_WS>`, then on `ubuntu-ws`:

   ```bash
   # ubuntu-ws
   sudo grep fsw-a-sa-174 /var/log/syslog | tail -n 5
   ```

   On the controller, watch the packets cross `fsw-users` (`diagnose sniffer
   packet` with an interface, a filter, verbosity, and a count):

   ```text
   FGT # diagnose sniffer packet fsw-users 'udp port 514' 4 5
   ```

   Predict: the sniffer shows `10.174.41.2` sending to `10.200.0.20.514`, and
   `ubuntu-ws` logs lines with the hostname `fsw-a-sa-174`. If no lines arrive
   but the sniffer shows packets, record which events the switch's default
   syslog filter sends: the default severity of `config log syslogd filter` is
   not stated in the pages this chapter uses.

7. Check that the route is what carries the traffic: compare the route lookup
   with the sniffer output from step 6. The packets leave the switch on
   `svi-users-174`, toward `10.174.41.1`, not on `<MGMT_IF>`.

**Track 2: read-and-predict.**

1. The CLI Reference prints this routing table (p. 486), trimmed:

   ```text
   S524DF4K15000024 # get router info routing-table all
   S>* 0.0.0.0/0 [5/0] via 169.254.1.1, internal, 00:36:02
   C>* 169.254.1.0/24 is directly connected, internal, 1d00h57m
   C>* 192.168.2.0/24 is directly connected, mgmt, 01:51:05
   ```

   Predict the lines for this lab's switch after step 4. **Answer:** `S>*
   0.0.0.0/0 ... via 10.30.99.1, <MGMT_IF>`, `S>* 10.200.0.0/24 ... via
   10.174.41.1, svi-users-174`, and `C>*` lines for `10.30.99.0/24`,
   `10.174.41.0/24`, and `10.174.43.0/24`.
2. Two hosts in different VLANs use a FortiGate as their gateway, and the
   FortiGate denies traffic between the VLANs. An administrator adds SVIs for
   both VLANs on the access switch and host routes on both hosts. Predict.
   **Answer:** the hosts now reach each other through the switch, and the
   FortiGate never sees the traffic, so its policy does not apply.
3. An FS-124F should run OSPF with a core router. Predict. **Answer:** not
   possible: OSPF is a dash in the 1xxE/1xxF column; on the 200 Series it is a
   standalone feature under the Advanced Features license heading.

**Expected result:** Track 1: both SVIs answer; with host routes, endpoints A and
B reach each other through the switch with TTL 63, which the controller's
policy no longer controls; static route 2 sends the switch's syslog through the
controller's `fsw-users` interface to `ubuntu-ws`. Track 2: the predictions are
answered.

**Negative test:** (a) Remove endpoint A's host route and ping endpoint B again:

```bash
# endpoint A
sudo ip route del 10.174.43.0/24 via 10.174.41.2
ping -c 3 10.174.43.20
```

Predict: the ping fails. Endpoint A sends to the controller again, which denies
it, even though endpoint B would still answer through the switch. Add the route
back for Lab 11.4. (b) Disable static route 2 and repeat step 6:

```text
FSW # config router static
edit 2
set status disable
next
end
```

Predict: `get router info routing-table all` no longer shows `10.200.0.0/24`,
and the syslog packets disappear from the controller's sniffer on `fsw-users`.
Record whether the switch now sends them out `<MGMT_IF>` (through the default
route) and whether anything arrives at `ubuntu-ws` that way; that depends on
the UCGF's routing, which this volume does not document. Set `status enable`
again. Track 2: prediction 2 is the negative test.

**Rollback:** Keep the SVIs, the routes, and the endpoint host routes for Lab
11.4. To undo only this lab:

```text
FSW # config log syslogd setting
set status disable
end
FSW # config router static
delete 2
end
FSW # config system interface
delete "svi-users-174"
delete "svi-iot-174"
end
```

```bash
# endpoint A
sudo ip route del 10.174.43.0/24 via 10.174.41.2
# endpoint B
sudo ip route del 10.174.41.0/24 via 10.174.43.2
```

**Lab verified by:** *pending*

### Lab 11.4 — Standalone ingress ACLs, ACL services, private VLANs, and QoS marking

**Objective:** Build an ACL service and ingress ACLs that drop and count
endpoint B's traffic on every switch option, read the counters and the TCAM
use, show that an ingress ACL cannot drop pings to the switch itself; on the 200
Series, build a private VLAN and show isolated and community behavior, and mark
endpoint B's traffic with `remark-dscp`.

**Platform notes:** Part A is hands-on on S1, S2, and S3: ingress ACLs and ACL
services are a check (standalone only) on the FS-108F and FS-124F, which is the
hands-on ACL work that Lab 8.4 deferred to this lab, and chain on the 200
Series. Parts B (private VLAN) and C (QoS marking) are hands-on only on S3,
where both are a check in the 200 Series column; on S1 and S2 they are
read-and-predict (the 1xxE/1xxF column has a dash for both). Part D is optional
on S3. Lab 11.3's SVIs and host routes are in place. Track 2: read-and-predict.

**Track 1, Part A — ingress ACLs and an ACL service (S1, S2, S3):**

1. Read the ACL state and the predefined services first (Administration Guide,
   pp. 295 and 300):

   ```text
   FSW # get switch acl usage
   FSW # get switch acl ingress
   FSW # show switch acl service custom
   ```

   Record the free ingress rules and counters, and whether any ingress policy
   exists already.

2. Create an ACL service for ICMP echo requests (CLI Reference, pp. 110–111):

   ```text
   FSW # config switch acl service custom
   edit "icmp-echo-174"
   set protocol ICMP
   set icmptype 8
   set icmpcode 0
   set comment "ICMP echo request"
   next
   end
   ```

3. Create three ingress policies on `port2`. Policy 1 drops and counts endpoint
   B's pings to the controller's `fsw-iot` address; policy 2 only counts
   endpoint B's traffic to endpoint A's subnet; policy 3 tries to drop pings to
   the switch's own `svi-iot-174` address. Every classifier uses only fields
   that the FS-1xx models accept (Administration Guide, p. 293):

   ```text
   FSW # config switch acl ingress
   edit 1
   set description "drop B ping to fsw-iot gw"
   set ingress-interface "port2"
   config classifier
   set service "icmp-echo-174"
   set dst-ip-prefix 10.174.43.1 255.255.255.255
   end
   config action
   set drop enable
   set count enable
   end
   next
   edit 2
   set description "count B to A subnet"
   set ingress-interface "port2"
   config classifier
   set src-ip-prefix 10.174.43.20 255.255.255.255
   set dst-ip-prefix 10.174.41.0 255.255.255.0
   end
   config action
   set count enable
   end
   next
   edit 3
   set description "try to drop B ping to switch"
   set ingress-interface "port2"
   config classifier
   set service "icmp-echo-174"
   set dst-ip-prefix 10.174.43.2 255.255.255.255
   end
   config action
   set drop enable
   set count enable
   end
   next
   end
   ```

   Record whether the switch accepts each policy; the switch rejects a policy
   that its hardware cannot support (p. 294).

4. Clear the counters, then send ten pings to each target from endpoint B:

   ```text
   FSW # execute acl clear-counter ingress
   ```

   ```bash
   # endpoint B
   ping -c 10 10.174.43.1
   ping -c 10 <LEASE_A>
   ping -c 10 10.174.43.2
   ```

   ```text
   FSW # get switch acl counters ingress
   FSW # get switch acl usage
   ```

   Predict the pings and the counters. **Answer:** the pings to `10.174.43.1`
   all fail and policy 1 counts at least 10 packets; the pings to `<LEASE_A>`
   all answer (routed by the switch) and policy 2 counts at least 10 packets,
   more if other traffic matched; the pings to `10.174.43.2` **answer**,
   because pings to a local address go to the CPU before the ingress ACL
   (Administration Guide, p. 296), so policy 3 cannot drop them; record what its
   counter shows. On S1 and S2 every `Bytes` value is 0, because the FS-1xxE and
   FS-1xxF have packet counters only (p. 302). `get switch acl usage` shows
   fewer free ingress rules and counters than in step 1.

5. Make policy 1 inactive and repeat its ping:

   ```text
   FSW # config switch acl ingress
   edit 1
   set status inactive
   next
   end
   ```

   Predict: the pings to `10.174.43.1` answer again and policy 1's counter
   stops rising. Set `status active` again.

6. On S1 or S2, try one action that the FS-1xx models do not offer, and record
   the response:

   ```text
   FSW # config switch acl ingress
   edit 2
   config action
   set remark-dscp 46
   end
   next
   end
   ```

   Predict: the switch refuses the setting or the policy, because the FS-1xx
   ingress actions are limited to `cos-queue`, `count`, `drop`,
   `outer-vlan-tag`, and `redirect` (p. 293), and QoS marking is a dash in the
   1xxE/1xxF column. On S3 skip this step; Part C uses the action.

**Track 1, Part B — private VLAN (S3 only):**

7. Create a primary VLAN with an isolated and a community VLAN (Administration
   Guide, p. 356; CLI Reference, p. 185):

   ```text
   FSW # config switch vlan
   edit 1747
   set description "pvlan-iso-174"
   next
   edit 1748
   set description "pvlan-com-174"
   next
   edit 1746
   set description "pvlan-174"
   set private-vlan enable
   set isolated-vlan 1747
   set community-vlans 1748
   next
   end
   ```

8. Make `port1` promiscuous and `port2` an isolated host port, and give the
   endpoints test addresses in one subnet. The port options `primary-vlan` and
   `sub-vlan` come from the Administration Guide's example (p. 356); the CLI
   Reference's syntax lists only `private-vlan`, so record what the switch
   accepts:

   ```text
   FSW # config switch interface
   edit "port1"
   set private-vlan promiscuous
   set primary-vlan 1746
   next
   edit "port2"
   set private-vlan sub-vlan
   set primary-vlan 1746
   set sub-vlan 1747
   next
   end
   FSW # get switch vlan
   ```

   ```bash
   # endpoint A
   sudo ip addr add 10.174.46.30/24 dev <IFACE>
   # endpoint B
   sudo ip addr add 10.174.46.20/24 dev <IFACE_B>
   ping -c 3 10.174.46.30
   ```

   Predict `get switch vlan` and the ping. **Answer:** VLAN 1746 shows
   `private-vlan-type: primary` with isolated VLAN 1747 and community VLAN 1748,
   and 1747 and 1748 show as isolated and community sub-VLANs of 1746 (the
   shape on CLI Reference p. 512); the ping answers, because an isolated port
   reaches a promiscuous port.

9. Make `port1` an isolated host port too and ping again:

   ```text
   FSW # config switch interface
   edit "port1"
   set private-vlan sub-vlan
   set primary-vlan 1746
   set sub-vlan 1747
   next
   end
   ```

   Predict: the ping fails; two ports in the isolated VLAN cannot reach each
   other.

10. Put both ports in the community VLAN and ping again:

    ```text
    FSW # config switch interface
    edit "port1"
    set sub-vlan 1748
    next
    edit "port2"
    set sub-vlan 1748
    next
    end
    ```

    Predict: the ping answers; ports in the same community VLAN reach each
    other.

11. Undo Part B before Part C: remove the private-VLAN settings from the ports
    and delete the VLANs and the test addresses. The ports return to their Lab
    11.2 native VLANs; record whether `native-vlan` must be set again:

    ```text
    FSW # config switch interface
    edit "port1"
    set private-vlan disabled
    set native-vlan 1741
    next
    edit "port2"
    set private-vlan disabled
    set native-vlan 1743
    next
    end
    FSW # config switch vlan
    delete 1746
    delete 1747
    delete 1748
    end
    ```

    ```bash
    # endpoint A
    sudo ip addr del 10.174.46.30/24 dev <IFACE>
    ping -c 3 10.174.41.1
    # endpoint B
    sudo ip addr del 10.174.46.20/24 dev <IFACE_B>
    ping -c 3 10.174.43.1
    ```

**Track 1, Part C — QoS marking with an ACL remark action (S3 only):**

12. Add policy 4, which marks endpoint B's traffic to endpoint A's subnet
    with DSCP 46 (EF) and counts it (CLI Reference, pp. 105–108). Policy 2
    matches the same packets, so put policy 4 in a second ACL group: the
    Administration Guide says that groups let one packet match several rules
    and that all non-conflicting actions are performed (p. 295), and multiple
    ingress ACLs are a check in the 200 Series column:

    ```text
    FSW # config switch acl ingress
    edit 4
    set description "remark B to A as EF"
    set group 2
    set ingress-interface "port2"
    config classifier
    set src-ip-prefix 10.174.43.20 255.255.255.255
    set dst-ip-prefix 10.174.41.0 255.255.255.0
    end
    config action
    set remark-dscp 46
    set count enable
    end
    next
    end
    ```

    If the switch refuses `group 2`, record the response, remove the line, and
    set policy 2 to `status inactive` instead, so that the two rules do not
    overlap. After step 13, read `get switch acl counters ingress`: with two
    groups, both policy 2 and policy 4 count the pings.

13. Capture on endpoint A while endpoint B sends unmarked pings:

    ```bash
    # endpoint A
    sudo tcpdump -i <IFACE> -v -c 4 icmp and src host 10.174.43.20
    # endpoint B
    ping -c 4 -Q 0 <LEASE_A>
    ```

    Predict the `tos` field. **Answer:** `tos 0xb8` (DSCP 46 shifted left by two
    bits) on the echo requests that endpoint A receives, although endpoint B
    sent `tos 0x0`; the replies from endpoint A to endpoint B are not marked,
    because they enter on `port1`, where no remark policy applies. The switch's
    own queuing of the marked packets still follows the original value
    (Administration Guide, p. 366).

**Track 1, Part D — real-time queue rates (optional, S3 only):**

14. While endpoint B sends a stream to endpoint A (`iperf -c <LEASE_A> -u -b
    8M -t 20` on endpoint B, with `iperf -s -u` on endpoint A if you reinstall
    it), read the per-queue rates (CLI Reference, pp. 370–371):

    ```text
    FSW # diagnose switch physical-ports qos-rates non-zero
    ```

    Record which egress queue on `port1` carries the stream; Chapter 10
    explains why marking alone does not move it. Remove `iperf` from endpoint A
    again if you installed it.

**Track 2: read-and-predict.**

1. The Administration Guide prints this ACL usage for an FS-108F (p. 295):

   ```text
   S108FNTV21000005 # get switch acl usage
   Device RULES      COUNTERS   POLICERS  STAGE    GROUP
          (total/free) (total/free) (total/free)
   0      640 /640   256 /247   0 /0      ingress  1
   ```

   After you add three ingress policies with `count` enabled, predict what
   changes. **Answer:** the free rules and the free counters both fall; the
   exact amounts depend on how the hardware allocates each classifier
   (p. 295), so record them. There are no egress or prelookup lines: those
   stages are a dash for the FS-108F.
2. The Administration Guide prints this counter output (p. 303), trimmed:

   ```text
   FS3E32T419000041 # get switch acl counters all
   ingress:
   ID Group Color Packets Bytes description
   1  1     all   0       0     test1
   ```

   An FS-124F drops ten pings with a `count` and `drop` policy. Predict
   `Packets` and `Bytes`. **Answer:** `Packets` 10 and `Bytes` 0, because the
   FS-1xxF has no ACL byte counters (p. 302).
3. The CLI Reference prints this VLAN list (p. 512):

   ```text
   # get switch vlan
   == [ 1 ]
   id: 1 private-vlan-type: primary isolated-vlan: 2 community-vlans: 3
   == [ 2 ]
   id: 2 private-vlan-type: isolated sub-VLAN primary-vlan: 1
   == [ 3 ]
   id: 3 private-vlan-type: community sub-VLAN primary-vlan: 1
   ```

   Hosts H1 and H2 are on ports in sub-VLAN 2, H3 on a port in sub-VLAN 3, and
   a router on a promiscuous port. Predict which pairs can communicate.
   **Answer:** each host reaches the router; H1 and H2 cannot reach each other
   (isolated); neither reaches H3 (different secondary VLANs).
4. An administrator writes an ingress ACL on an FS-124F that matches `dscp 46`
   and sets `remark-cos 5`. Predict. **Answer:** the switch refuses it: `dscp`
   is not among the FS-1xx classifier fields and `remark-cos` is not among
   their actions (p. 293); QoS marking is a 200 Series feature in standalone
   mode.

**Expected result:** Track 1: on every switch option, policy 1 dropped and
counted endpoint B's pings to the controller's `fsw-iot` address, policy 2
counted traffic to endpoint A's subnet, and policy 3 did not stop pings to the
switch's own address; byte counters were 0 on S1 and S2, and the remark action
was refused there. On S3, the private VLAN let an isolated port reach a
promiscuous port but not another isolated port, and community ports reached
each other; policy 4 marked endpoint B's echo requests with DSCP 46. Track 2:
the predictions are answered.

**Negative test:** Apply policy 1 to the wrong port and repeat endpoint B's
ping:

```text
FSW # config switch acl ingress
edit 1
set ingress-interface "port1"
next
end
```

Predict: endpoint B's pings to `10.174.43.1` answer again, because an ingress
ACL acts only on traffic arriving on its own ports; the counter does not move.
Set `ingress-interface "port2"` again. Track 2: prediction 4 is the negative
test.

**Rollback:** Delete the ACL objects and the endpoint host routes from Lab
11.3:

```text
FSW # config switch acl ingress
delete 1
delete 2
delete 3
end
FSW # config switch acl service custom
delete "icmp-echo-174"
end
```

On S3, also `delete 4` under `config switch acl ingress`. Part B's rollback is
step 11.

```bash
# endpoint A
sudo ip route del 10.174.43.0/24 via 10.174.41.2
# endpoint B
sudo ip route del 10.174.41.0/24 via 10.174.43.2
```

Confirm that `get switch acl ingress` lists no lab policy, that endpoint A
reaches `10.174.41.1`, and that endpoint B reaches `10.174.43.1`.

**Lab verified by:** *pending*

### Lab 11.5 — FortiEdge Cloud, migrating the configuration, and returning to FortiLink

**Objective:** Optionally connect the standalone switch to FortiEdge Cloud and
read the tunnel state; map the standalone configuration onto FortiLink-mode
objects and back it up; then return the switch to FortiLink management, confirm
the Chapter 10 state item by item, and back up the managed configuration.

**Platform notes:** Part A is hands-on only with a FortiCloud account (any
switch option: FortiEdge Cloud configuration is a check in both columns);
without one it is read-and-predict. Parts B and C are hands-on on every switch
and controller option; on S3, Part C reconnects `FSW-B`. Part C changes the
controller only by authorizing the existing entry. Allow 30 minutes for Part C.
Track 2: Part B is a paper exercise; the rest is read-and-predict.

**Track 1, Part A — FortiEdge Cloud (optional):**

1. In a browser, sign in to FortiCloud and open FortiEdge Cloud, and add this
   switch to your inventory as the FortiEdge Cloud User Guide describes. Sign
   in only on Fortinet's FortiCloud page: never type your FortiCloud
   credentials on the switch, on a lab host, or anywhere else. The User Guide
   is not among this volume's local references; record the steps you followed
   and anything the portal requires (registration, licensing).

2. Give the switch a DNS server that resolves public names, then point the
   cloud client at the dispatch service (CLI Reference, pp. 229–230):

   ```text
   FSW # get system dns
   FSW # config system dns
   set primary <DNS_SERVER>
   end
   FSW # config system flan-cloud
   set service-type flan-cloud
   set name "fortiswitch-dispatch.forticloud.com"
   set port 443
   set status enable
   end
   ```

3. Read the tunnel state on the switch:

   ```text
   FSW # get system flan-cloud
   FSW # get system flan-cloud-mgr connection-info
   ```

   Predict which fields show a working connection. **Answer:** in the CLI
   Reference's example (p. 520), `SSL verify Code : ok`, an `Access Service`
   line with an address, port 443, and a `Connected on` time, `State-Machine :
   State= FLAN_MGR_STATE_READY`, and a growing `SSL Tunnel Uptime`; the example
   is for FortiLink over HTTPS, so record your `Service Name` and `User
   Account-ID` values (do not publish them).

4. In the portal, confirm that the switch appears online, and look at (without
   changing) the configuration the portal shows for it. Then remove the switch
   from your FortiEdge Cloud inventory as the User Guide describes, so that the
   cloud does not claim it after the reset in Part C, and turn the client off:

   ```text
   FSW # config system flan-cloud
   set status disable
   end
   ```

   Record the portal's state for the switch after the removal.

**Track 1, Part B — the standalone configuration and its FortiLink equivalents:**

5. Back up the standalone configuration to VM 140 (CLI Reference, p. 410), and
   check that the file arrived:

   ```text
   FSW # execute backup config tftp fsw-sa-11-174.conf 10.30.99.50
   ```

   ```bash
   # VM 140
   ls -l /tftpboot/fsw-sa-11-174.conf
   ```

6. The FortiLink Guide says that a configured standalone switch loses its
   configuration when converted to FortiLink mode, and offers `fortilinkify.py`
   on the Fortinet Developer Network to translate standalone configurations
   (p. 34). The script's instructions come with it and are not part of this
   volume; if you have access, run it against `fsw-sa-11-174.conf` and compare
   its output with this table. Otherwise, fill in the right-hand column
   yourself from Chapters 04–10 and check it against this answer:

   | Standalone object in `fsw-sa-11-174.conf` | FortiLink-mode equivalent | Status in this volume |
   | --- | --- | --- |
   | `config switch vlan` 1741, 1743 | VLAN interfaces `fsw-users`, `fsw-iot` on the FortiLink interface | Exist (Chapter 04) |
   | `port1` and `port2` `native-vlan`, `description`, `edge-port`, `stp-bpdu-guard` | `config ports`: `vlan`, `description`, `stp-bpdu-guard` (edge port is the 7.6.0 default) | Exist in the kept entry |
   | Uplink `allowed-vlans` | Not needed: the FortiLink trunk carries the controller's VLANs | — |
   | `config switch trunk` `lag-174` | `config ports`, `type trunk`, `members` | Not recreated |
   | `config switch stp settings` and `instance` | `config switch-controller stp-settings`, `stp-instance`, and the entry's `config stp-instance` | Exist (Chapter 05) |
   | SVIs and `config router static` | FortiGate routing; managed-switch `system-interface` and `router-static` need FortiOS 7.6.4 or later (Chapter 04) | Not recreated |
   | `config switch acl ingress` and services | `config switch-controller acl ingress` and `acl group`; not on the FS-108F or FS-124F in FortiLink mode (note 16); FortiOS has no ACL service table of this kind | Not recreated |
   | Private VLAN, `remark-dscp` | None: standalone-only on the 200 Series | — |
   | Management address, admin hardening, syslog | FortiLink management on `10.255.1.2`; the switch profile and Chapter 12's `remote-log` | Profile exists; Chapter 12 |

**Track 1, Part C — return to FortiLink:**

7. Prepare the controller: remove `<SWITCH_SN>` from `disable-discovery` if Lab
   11.1 step 5 found it there (`unselect` inside the table, FortiLink Guide,
   p. 322), and confirm that the entry still holds its settings:

   ```text
   FGT # config switch-controller global
   unselect disable-discovery <SWITCH_SN>
   end
   FGT # show switch-controller global
   FGT # show switch-controller managed-switch <SWITCH_SN>
   ```

8. Reset the switch from the console. It returns to the zero-touch defaults,
   with FortiLink discovery enabled, and reboots; set your recorded admin
   password at the next login:

   ```text
   FSW # execute factoryreset
   ```

9. While it reboots, unplug the Nexus cable from `mgmt` (or `port3`) and shut
   the Nexus port; keep `<FSW_FL_PORT>`, `port1`, and `port2` cabled:

   ```text
   interface Ethernet1/<free>
     shutdown
   ```

10. Wait for the switch to appear, then authorize the existing entry:

    ```text
    FGT # execute switch-controller get-conn-status
    FGT # config switch-controller managed-switch
    edit <SWITCH_SN>
    set fsw-wan1-admin enable
    next
    end
    ```

    The FortiLink Guide says both that the switch reboots in FortiLink mode
    after authorization (p. 41) and that a switch does not need a restart when
    it becomes managed (p. 14); record which happens. Wait for
    `Authorized/Up`:

    ```text
    FGT # execute switch-controller get-conn-status
    FGT # execute switch-controller get-sync-status all
    FGT # execute ping 10.255.1.2
    ```

    Predict: STATUS `Authorized/Up`, VERSION the Lab 3.3 build, ADDRESS
    `10.255.1.2` (record the address if it differs), and an in-sync result like
    the one Lab 3.4 recorded.

11. S3 only: plug `FSW-A`'s `port23` and `port24` back in. Wait until `FSW-B`
    is `Authorized/Up` again, and check the ICL on `FSW-A`:

    ```text
    FSW # diagnose switch trunk summary
    ```

    The MCLAG ICL trunk is up with two members, as at the end of Chapter 06.

12. Check the Chapter 10 state item by item against Lab 11.1 step 1 and
    ADDENDUM 10:

    ```text
    FGT # show switch-controller managed-switch <SWITCH_SN>
    FSW # get system status
    FSW # diagnose stp instance list 1
    FSW # diagnose switch vlan list
    ```

    ```bash
    # endpoint A
    sudo ip link set <IFACE> down && sudo ip link set <IFACE> up
    sleep 10; ip -br addr show <IFACE>
    # endpoint B
    ping -c 3 10.174.43.1
    ```

    | Item | Expected |
    | --- | --- |
    | Entry | Description `FSW-A lab-174`, `switch-profile "fsw-174-prof"` |
    | `port1` | Native `fsw-users`, allowed `<PORT1_ALLOWED>` (with `quarantine`), BPDU guard, description `endpoint A`, LLDP profile and QoS policy as recorded |
    | `port2` | Native `fsw-iot`, allowed `<PORT2_ALLOWED>`, BPDU guard, description `endpoint B` |
    | STP | Instance 1 priority 16384 on the switch, region `lab-174` revision 1 |
    | Switch | The Lab 3.3 build; hostname back to the serial number |
    | Endpoints | Endpoint A leases from `fsw-users`; endpoint B reaches `10.174.43.1` |
    | S3 | `FSW-B` `Authorized/Up`; ICL up |

    If any item is missing because the deauthorized entry did not keep it,
    record which, then restore the controller from the Lab 11.1 backup. The
    controller reboots, and the restored entry is authorized again:

    ```text
    FGT # execute restore config tftp fgt-pre-11-1-174.conf 10.30.99.50
    ```

    After the reboot, wait for `Authorized/Up` and repeat this step.

13. Back up the managed configuration: the controller, which holds it, and a
    console capture of what the switch runs:

    ```text
    FGT # execute backup config tftp fgt-post-11-174.conf 10.30.99.50
    ```

    ```bash
    picocom -b 9600 --logfile fsw-managed-post-11-174.txt /dev/ttyUSB0
    ```

    ```text
    FSW # show
    ```

    Compare `fsw-managed-post-11-174.txt` with `fsw-managed-pre-11-174.txt`;
    record any difference other than timestamps and generated secrets.

**Track 2: read-and-predict.**

1. The CLI Reference prints this cloud client state (p. 519):

   ```text
   S524DF4K15000024 # get system flan-cloud
   interval : 3
   name : fortiswitch-dispatch.forticloud.com
   service-type : flan-cloud
   port : 443
   status : enable
   ```

   Predict what the switch needs, besides these settings, before the tunnel
   comes up. **Answer:** a DNS server that resolves the dispatch name, a route
   to the internet, and an entry for the switch in a FortiEdge Cloud inventory;
   the account side is done in the portal, never on the switch.
2. A switch that is still in a FortiEdge Cloud inventory is reset and cabled to
   a FortiGate's FortiLink port. Predict. **Answer:** the zero-touch defaults
   enable both FortiLink discovery and the cloud client (FortiLink Guide,
   p. 15), and a switch can be authorized by only one manager in most cases
   (p. 14), so it may be claimed by the cloud instead of the FortiGate; remove
   it from the inventory first.
3. The FortiLink Guide prints this `get-conn-status` (p. 52), trimmed:

   ```text
   SWITCH-ID        VERSION        STATUS          FLAG ADDRESS
   S524DN4K16000116 v7.4.0 (0796)  Authorized/Up   2T   10.255.1.2
   S248EPTF18001827 N/A            Discovered/Down 2    N/A
   ```

   Predict the line for `<SWITCH_SN>` after step 8 and before step 10, and
   after step 10. **Answer:** before authorization, `Discovered/Down` with
   VERSION and ADDRESS `N/A` (if the switch is not in `disable-discovery`);
   after it, `Authorized/Up` with the switch's version and `10.255.1.2`. Your
   FLAG may lack the `T` (tunnel), which marks FortiLink over HTTPS in the
   guide's example.
4. Complete Part B's table on paper; the answer is in the table.

**Expected result:** Track 1: Part A (optional) showed a ready cloud tunnel and
the switch was removed from the inventory again; `fsw-sa-11-174.conf` is on VM
140 and the mapping table is complete; `<SWITCH_SN>` is `Authorized/Up` with
every Chapter 10 item in place (on S3 `FSW-B` too); `fgt-post-11-174.conf` and
`fsw-managed-post-11-174.txt` exist; the Nexus port is shut. Track 2: the
predictions and the table are done.

**Negative test:** Between steps 8 and 10, with the switch reset and cabled,
wait five minutes without authorizing it. Predict: `get-conn-status` shows it
`Discovered/Down`, not `Authorized/Up`, because the entry is deauthorized and
this lab's controller does not authorize automatically; the endpoints have no
connectivity, because a switch at factory defaults has none of the lab VLANs.
Track 2: prediction 2 is the negative test.

**Rollback:** Part C is the rollback of the whole chapter. If the switch does
not come back, repeat steps 7–10; if the entry is damaged, use the restore in
step 12. If you connected FortiEdge Cloud and could not remove the switch from
the inventory, do not reset it again until the portal shows it removed.

**Lab verified by:** *pending*

## Lab Verification

Complete this sign-off once Labs 11.1 to 11.5 have been run end to end,
including each negative test. Until then, the labs are unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

A FortiSwitch has one manager at a time, and standalone mode is simply the
state with none. `set-standalone` resets a managed switch and keeps the
controller from adopting it; keeping the deauthorized entry lets the controller
push the same configuration back later. A standalone switch should have auto
topology, FortiLink discovery, and the cloud client off, a static management
address on `mgmt` or on `internal` in its own VLAN, and hardened administrative
access. Standalone VLANs, native and allowed lists, LACP trunks, and MSTP use
the switch's own tables with the same frame rules as FortiLink mode. SVIs and
static routes route on the switch (in software on the FS-1xx models), which
bypasses the FortiGate's policy; dynamic routing needs the Advanced Features
license and a 200 Series switch. Standalone ingress ACLs with ACL services work
on every switch option, with a reduced field and action set and no byte
counters on the FS-1xx models, and cannot filter traffic to the switch itself;
private VLANs and remark actions are 200 Series standalone features. FortiEdge
Cloud manages a switch through its `flan-cloud` client, with the account side
only in the portal. Converting to FortiLink discards the standalone
configuration, so the chapter backs up both configurations and ends with the
switch managed in the Chapter 10 state.

- [ ] I backed up the controller and captured the managed configuration before
      leaving FortiLink mode.
- [ ] `set-standalone` reset the switch, the deauthorized entry kept its
      settings, and the switch did not rejoin on its own.
- [ ] The standalone switch has auto topology, FortiLink discovery, and the
      cloud client off, a static management address, a trusted host, a
      lockout, and no `public` community, and refuses SSH from an untrusted
      host.
- [ ] VLANs 1741 and 1743 reached the controller tagged over the uplink (or I
      recorded the controller's refusal), and `lag-174` stayed down without a
      partner.
- [ ] Endpoints A and B reached each other through the switch's SVIs with TTL
      63, and I can explain why the controller's intrazone deny did not apply.
- [ ] Static route 2 carried the switch's syslog to `ubuntu-ws`.
- [ ] Ingress ACLs dropped and counted endpoint B's traffic on my switch, and I
      saw that pings to the switch itself are not filtered.
- [ ] On S3, the private VLAN isolated two isolated ports, and `remark-dscp`
      marked endpoint B's packets with DSCP 46; on S1 or S2, I recorded the
      refusal of the remark action.
- [ ] I connected FortiEdge Cloud (or answered its predictions), and I can map
      the standalone configuration onto FortiLink-mode objects.
- [ ] `<SWITCH_SN>` is `Authorized/Up` in the Chapter 10 state, and
      `fsw-sa-11-174.conf`, `fgt-post-11-174.conf`, and both console captures
      exist.
