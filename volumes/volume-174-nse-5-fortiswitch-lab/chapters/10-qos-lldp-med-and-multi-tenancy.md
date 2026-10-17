# Chapter 10: QoS, LLDP-MED, and Multi-Tenancy

## Learning Objectives

- Explain what an **LLDP profile** controls on a managed FortiSwitch port, read
  the profiles and LLDP settings the controller already has, and state which
  profile a managed port uses by default.
- Build an **LLDP-MED** profile with **voice** and **voice-signaling network
  policies**, apply it to a port, and show that the switch adds the voice VLAN
  to the port (`assign-vlan`) and advertises the VLAN, priority, and DSCP value
  to an LLDP-MED endpoint; state when a network policy is not sent at all.
- Describe the FortiSwitch QoS model: **trust** of 802.1p or DSCP values on
  ingress, **dot1p** and **DSCP maps** to eight **egress queues**, a **queue
  policy** with strict, round-robin, or weighted scheduling and per-queue rate
  limits, and the **QoS policy** that ties them to a port; map the FortiOS
  object names to the switch-side names.
- Apply a QoS policy to two ports, mark test traffic with DSCP values, and show
  the queue assignment through egress rate limits on every switch option and
  through queue counters on the 200 Series; state what feature matrix note 18
  (one QoS map on the FS-1xx models) means for S1 and S2.
- Explain the two **multi-tenancy** models of the switch controller: switch
  ports **dedicated** to a tenant VDOM (`export-to`, the virtual switch, the
  default virtual-switch VLAN, and **virtual port pools**), and **VLANs from
  different VDOMs on one port** with no administrative separation; know which
  features shared ports support and which they do not (DHCP snooping).
- Decide, for your controller option, whether multi-tenancy can run hands-on,
  and why the FortiGate-VM evaluation (C2) normally cannot.

## Theory and Architecture

### Where each feature lives in FortiLink mode

Everything in this chapter is configured on the FortiGate and pushed to the
switch. The table maps each feature to its FortiOS objects (FortiOS 7.6.0 CLI
Reference; FortiLink Guide 7.6.7, pp. 124–127, 164–177, and 285–290):

| Feature | FortiOS object | Key options |
| --- | --- | --- |
| LLDP global settings | `config switch-controller lldp-settings` | `tx-interval`, `tx-hold`, `fast-start-interval`, `management-interface`, `device-detection` |
| LLDP profile | `config switch-controller lldp-profile` | `med-tlvs`, `802.1-tlvs`, `802.3-tlvs`, `auto-isl` and the other auto-ISL options; `config med-network-policy`, `config med-location-service`, `config custom-tlvs` |
| Port LLDP | `config switch-controller managed-switch`, `config ports` | `lldp-profile`, `lldp-status` |
| LLDP asset tag | `config switch-controller managed-switch` | `switch-device-tag` |
| 802.1p map | `config switch-controller qos dot1p-map` | `priority-0` to `priority-7`, `egress-pri-tagging` |
| DSCP map | `config switch-controller qos ip-dscp-map`, `config map` | `diffserv`, `ip-precedence`, `value`, `cos-queue` |
| Queue policy | `config switch-controller qos queue-policy`, `config cos-queue` | `schedule`, `rate-by`; per queue `max-rate`, `min-rate`, `weight`, `drop-policy`, `ecn` |
| QoS policy | `config switch-controller qos qos-policy` | `trust-dot1p-map`, `trust-ip-dscp-map`, `default-cos`, `queue-policy` |
| Port QoS | `config ports` | `qos-policy` |
| Per-switch drop policy | `config switch-controller managed-switch` | `qos-drop-policy`, `qos-red-probability` |
| Multi-VDOM mode | `config system global` | `vdom-mode` (`no-vdom`, `multi-vdom`) |
| Dedicated tenant ports | `config ports` (in the VDOM that controls the switch) | `export-to`, `export-to-pool` |
| Tenant default VLAN | `config switch-controller global` (in the tenant VDOM) | `default-virtual-switch-vlan` |
| Virtual port pool | `config switch-controller virtual-port-pool` | `description` |
| Shared VLANs | `config system interface` (the VLAN's `vdom`), `config ports` | `vdom`, `interface`, `vlanid`; `vlan`, `allowed-vlans` |

### LLDP and LLDP-MED on a managed switch

**LLDP** (IEEE 802.1AB) lets each device advertise its identity and
capabilities to its directly connected neighbors in type-length-value (**TLV**)
fields. **LLDP-MED** (Media Endpoint Discovery, ANSI/TIA-1057) adds TLVs for
media endpoints such as IP phones: **network policy** (the VLAN, Layer 2
priority, and DSCP value a voice or video application should use), location
for emergency calls, extended power management for PoE, and inventory (FortiSwitchOS
7.6.7 Administration Guide, p. 175). A FortiSwitch acts as a **network
connectivity device** and sends only the TLVs meant for that role; it keeps up
to 16 LLDP neighbors per physical port (p. 176).

In FortiLink mode three objects decide what a port sends:

- **LLDP settings** (`config switch-controller lldp-settings`) are global:
  `tx-interval` (default 30 s, 5–4,095), `tx-hold` (4, so the packet TTL is
  `tx-hold` times `tx-interval`), `fast-start-interval` (2 s for the first four
  packets after link-up; 0 disables it), the advertised `management-interface`
  (`internal` or `mgmt`), and `device-detection` (FortiLink Guide 7.6.7,
  p. 174; FortiOS 7.6.0 CLI Reference). They reach every managed switch,
  including the FortiLink and ISL ports that this volume detects with LLDP
  (Chapter 02), so this chapter reads them and changes none.
- **An LLDP profile** per port (`config switch-controller lldp-profile`):
  which LLDP-MED TLVs to send (`med-tlvs`: `inventory-management`,
  `network-policy`, `power-management`, `location-identification`), the
  IEEE 802.1 port VLAN ID TLV (`802.1-tlvs port-vlan-id`), the IEEE 802.3
  maximum-frame-size and PoE power-negotiation TLVs, the eight **network
  policies**, the location services, custom TLVs, and the auto-ISL options
  (Chapter 06).
- **The port itself:** `lldp-profile` and `lldp-status` (`tx-rx`, `tx-only`,
  `rx-only`, `disable`) under `config ports` (p. 176).

The FortiOS 7.6.0 defaults matter more than any example. A managed port's
`lldp-profile` defaults to **`default-auto-isl`** and its `lldp-status` to
`tx-rx` (Chapter 06). A new profile defaults to `auto-isl enable`, so a profile
meant for an edge port should say `auto-isl disable`, as the predefined voice
profile does (p. 169). On the switch, the standalone CLI example shows the
`default-auto-isl` profile with an empty `med-tlvs` list and the `default`
profile with `inventory-management network-policy` (FortiSwitchOS 7.6.7 CLI
Reference, p. 500); Lab 10.1 reads what your switch received from the
controller.

### LLDP-MED network policies

The eight network policies have fixed names: `voice`, `voice-signaling`,
`guest-voice`, `guest-voice-signaling`, `softphone-voice`, `video-conferencing`,
`streaming-video`, and `video-signaling`. They cannot be added or deleted, only
enabled (CLI Reference, p. 143). Each takes these FortiOS 7.6.0 options:

| Option | Default | Meaning |
| --- | --- | --- |
| `status` | `disable` | `enable` transmits this TLV once a VLAN has been added to the port (the 7.6.0 description) |
| `vlan-intf` | none | The FortiGate VLAN interface to advertise (at most 15 characters); the switch receives its VLAN ID |
| `assign-vlan` | `disable` | `enable` adds that VLAN to the port's allowed VLANs when the profile is applied |
| `priority` | 0 | The advertised Layer 2 priority (802.1p CoS), 0–7 |
| `dscp` | 0 | The advertised DSCP value, 0–63 |

Two rules from the switch side explain most results (CLI Reference, p. 143;
Administration Guide, pp. 181, 183):

- **The cross-check.** The VLAN of each policy is checked against the native,
  allowed, and untagged VLANs of every port that uses the profile. A policy is
  sent only if its VLAN is native or allowed on the port, and it is marked
  **tagged** unless the VLAN is native or untagged there. A policy with VLAN 0
  is "priority tagged" and always sent. The TLV follows the port's actual
  state, not the configured value.
- **VLAN assignment.** With `med-tlvs network-policy`, the policy `enable`d,
  `assign-vlan enable`, LLDP enabled globally and on the port, and the port not
  in a trunk or a private VLAN, the switch adds the VLAN "as though it were
  configured in the `set allowed-vlans` setting"; if the VLAN is also untagged
  on the port it is added untagged, and if it is the native VLAN nothing
  changes.

So a phone plugged into a port whose native VLAN is a data VLAN learns a
**tagged** voice VLAN from LLDP-MED, while a PC behind it keeps sending untagged
frames into the data VLAN. In this lab the voice VLAN is `fsw-voice` (1742) and
the data VLAN on `port1` is `fsw-users` (1741), which Chapter 04 already
proved by tagging 1742 on `port1` by hand; here LLDP-MED does it.

The predefined profile **`fortivoice.fortilink`** enables `voice` and
`voice-signaling` on the auto-created `voice` VLAN with `assign-vlan enable` and
DSCP 46 (FortiLink Guide 7.6.7, p. 169). Chapter 09 used it unchanged as a
dynamic port policy action; this chapter builds its own profile and leaves the
predefined one alone. Related features covered elsewhere: voice devices are
detected from their LLDP messages (Chapter 09), and an 802.1X security policy
can put clients in a tagged voice VLAN learned from LLDP when the RADIUS
server times out (`authserver-timeout-tagged lldp-voice`, Chapter 07). On a
port that runs 802.1X and LLDP together, changing the LLDP profile requires a
manual reset of the authentication sessions (Administration Guide, p. 176).

Reading LLDP on both sides (FortiLink Guide 7.6.7, p. 176; CLI Reference,
p. 499):

| Where | Command | Shows |
| --- | --- | --- |
| Controller | `diagnose switch-controller switch-info lldp neighbors-summary <SN>` | Neighbors per port on one switch |
| Controller | `diagnose switch-controller switch-info lldp neighbors-detail <SN>` | Each neighbor's TLVs |
| Controller | `diagnose switch-controller switch-info lldp stats <SN> <port>` | Counters for one port |
| Switch | `get switch lldp neighbors-summary`, `neighbors-detail <port>`, `profile`, `settings`, `stats` | The same from the switch, plus the profiles it holds |

The Administration Guide prints a neighbor detail for an LLDP-MED phone that
ends with the policies it learned, for example `voice: VLAN: 400 (tagged),
Priority: 5 DSCP: 46` (pp. 187–188). Lab 10.1 reproduces that with a Linux
endpoint running `lldpd` as an LLDP-MED Class III (communication device)
endpoint, and optionally with a real phone.

### QoS on a managed switch

A FortiSwitch port has **eight egress queues**, `queue-0` (lowest) to
`queue-7` (highest). QoS on the switch has three steps (Administration Guide,
pp. 365–368; FortiLink Guide 7.6.7, pp. 285–287):

1. **Classification on ingress.** If the ingress port **trusts** 802.1p, the
   frame's CoS value (0–7) is looked up in a **dot1p map**; if it trusts DSCP,
   the packet's DSCP value (0–63) is looked up in a **DSCP map**. Each map
   returns a queue number. Values a map does not list go to queue 0. An
   untagged frame has no CoS value; the port's **default CoS** (0 unless set)
   stands in for it, and only when the port trusts dot1p.
2. **Marking** (rewriting CoS or DSCP) is done by an ACL action (`remark-cos`,
   `remark-dscp`) in standalone FortiSwitchOS; it does not change the queue,
   which still comes from the trust maps and the original values
   (Administration Guide, p. 366; CLI Reference, p. 105). FortiOS 7.6.0 has no
   marking action for managed switches.
3. **Queuing on egress.** The egress port's queue policy schedules the eight
   queues: **strict** (higher queue first; lower queues can starve),
   **round-robin** (one packet from each backlogged queue in turn), or
   **weighted** round-robin (weights 0–63; weight 0 makes a queue strict inside
   a weighted policy). Each queue can have a maximum rate (egress policing), a
   minimum rate, and a drop policy (tail drop by default, or WRED with optional
   ECN on models that support it).

Fortinet recommends not trusting dot1p and DSCP on the same interface; if both
are trusted, DSCP decides and the dot1p map is used only for packets without a
DSCP value (p. 285; Administration Guide, p. 366). The Administration Guide's
"Determining the egress queue" rules (p. 368) are worth reading once: in
particular, a port that trusts dot1p but not DSCP classifies an untagged IP
packet by the port's default CoS, not by its DSCP value. Queue 7 carries the
switch's own network control and management traffic; do not oversubscribe it
or use it for data (p. 368).

**The names differ between FortiOS and FortiSwitchOS.** This trips readers who
move between the FortiLink Guide and the switch CLI:

| FortiOS (controller) | FortiSwitchOS (switch) | Holds |
| --- | --- | --- |
| `switch-controller qos dot1p-map` | `switch qos dot1p-map` | CoS to queue |
| `switch-controller qos ip-dscp-map` | `switch qos ip-dscp-map` | DSCP or IP precedence to queue |
| `switch-controller qos queue-policy` | `switch qos qos-policy` | Scheduling and per-queue rates (the egress policy) |
| `switch-controller qos qos-policy` | `trust-dot1p-map`, `trust-ip-dscp-map`, `default-cos`, and `qos-policy` under `config switch interface` | The per-port bundle |
| `qos-policy` under `config ports` | The switch interface settings above | Applies the bundle to a port |

FortiOS 7.6.0 defaults: a dot1p map sends every priority to `queue-0`; a DSCP
map entry's `cos-queue` is 0; a queue policy uses `schedule round-robin` and
`rate-by kbps`, and each queue `weight 1`, `drop-policy taildrop`, `ecn
disable`, and rates 0 (no limit); a QoS policy uses `default-cos 0` and
`queue-policy "default"`; and a managed port's `qos-policy` is `"default"`.
Lab 10.2 reads what your controller holds before changing anything.

**The predefined voice QoS policy.** FortiOS ships `voice-qos`, built from
`voice-dot1p`, `voice-dscp`, and `voice-egress` (FortiLink Guide 7.6.7,
pp. 287–289):

| Traffic | DSCP | CoS | Queue |
| --- | --- | --- | --- |
| VoIP data | 46 | 5 | 1 |
| VoIP control | 24, 26 | 3 | 2 |
| Routing protocols | 48 | 6 | 2 |
| STP BPDUs | 56 | 7 | 2 |
| Real-time video | 34 | 3 | 3 |
| (continued) | Others | 2 | 3 |
| (continued) | Others | 0, 1 | 4 |

The table is printed that way; the `voice-dot1p` map printed on the next page
differs in places (it sends priority 3 to `queue-2` and priority 4 to
`queue-3`), so read the maps, not the table, when you predict a queue.

`voice-egress` is `schedule weighted` with `queue-1` weight 0 (so voice data is
served strictly first), `queue-2` 6, `queue-3` 37, and `queue-4` 12. Note that
`voice-dscp` itself maps only 46, 24, 26, 48, 56, and 34, so other DSCP values
fall to queue 0, not queue 4; the last rows come from the dot1p map. The
guide's bandwidth targets (up to 100% for voice data, 10% for control, 60% for
video, 20% for the rest) describe the intent, not settings. This chapter uses
these objects only as a reference and never edits them.

Where the FortiLink Guide prints QoS statistics, it uses `diagnose
switch-controller switch-info qos-stats <SN> <port>` (p. 287); the switch-side
equivalents are `diagnose switch physical-ports qos-stats` (per-queue packet,
byte, and drop counters) and `qos-rates` (real-time egress rates) (CLI
Reference, pp. 370–372). Both depend on model support (see the model table).

**FS-1xx limits.** Feature matrix note 18 says the FS-1xxE, FS-1xxF, FS-110G-FPOE,
FS-124G, and FS-124G-FPOE support **a single QoS map, and if there is more than
one, the first configured map is used**; the FortiLink Guide repeats it for
the FS-1xxE and FS-1xxF (p. 285). The Administration Guide lists, for the
FS-124F, FS-148F, FS-124E, FS-148E, and some G models, one dot1p map and one DSCP
map per switch, no `min-rate`, `min-rate-percent`, `drop-policy`, or
`wred-slope` in the queue policy, `max-rate` rounded to a multiple of 16 kbps
(0 disables it), no `egress-pri-tagging`, and one drop policy per switch under
`config switch global` (pp. 365–366); the CLI Reference names only the FS-124E
and FS-148E families for the one-map limit (pp. 165–166). The FS-108F (S1)
appears in note 18 through the FS-1xxF family but in none of the
Administration Guide's model lists. Lab 10.2 therefore uses only `max-rate`
in multiples of 16, and it records which map the switch actually uses.

`default-cos` is not available on the FS-224D-FPOE, FS-248D, FS-224E,
FS-224E-POE, FS-248E-POE, and FS-248E-FPOE, among other models
(Administration Guide, p. 370), so S3 pairs of those models skip the
default-CoS step of Lab 10.2. The FortiGate itself does not apply QoS to
hardware or software switch ports (FortiLink Guide 7.6.7, p. 285); this chapter
is about QoS on the FortiSwitch.

### Multi-tenancy: VDOMs and the switch controller

A **VDOM** (virtual domain) divides one FortiGate into independent virtual
firewalls, each with its own interfaces, zones, policies, routing, and users
(FortiLink Guide 7.6.7, p. 124). Multi-VDOM mode is switched on globally
(`set vdom-mode multi-vdom` under `config system global`; the 7.6.0 options are
`no-vdom`, the default, and `multi-vdom`). From then on the CLI has two kinds of
context: `config global` for system-wide objects (`system global`, `system
interface`, `system vdom`) and `config vdom`, `edit <VDOM>` for everything that
belongs to one VDOM, including the whole switch controller (pp. 45, 128,
176–177). The FortiLink interface, and so the managed switches, belong to one
VDOM, usually `root`; the guide's HA topology requirements say that FortiSwitch
units must be connected on a NAT VDOM (p. 80), FortiLink is not supported in
transparent mode (Chapter 01), and the switches are not visible in other VDOMs
(p. 127). Initial-config
template interfaces outside `root` are named from the template name and the
SNMP index, for example `quarantined.29` (p. 34).

The switch controller offers two multi-tenancy models (pp. 124–127):

| | Ports dedicated to a VDOM | VLANs from several VDOMs on one port |
| --- | --- | --- |
| Who configures the port | The tenant VDOM's administrator, for the ports exported to it | The administrator of the VDOM that controls the switch (usually `root`) |
| Mechanism | `export-to <VDOM>` on the port, or `export-to-pool <pool>` and a claim from the tenant | A VLAN interface whose `vdom` is the tenant but whose parent is the FortiLink interface in `root`, assigned to ports as `vlan` or `allowed-vlans` |
| What the tenant sees | A **virtual switch**: the managed-switch entry with `type virtual`, `owner-vdom "root"`, and only its exported ports | No switch at all |
| Default VLAN | `default-virtual-switch-vlan` (set in the tenant VDOM) becomes the native VLAN of exported ports | — |
| Separation | Administrative and traffic | Traffic only |

**Dedicated ports.** In the guide's example the tenant VDOM `bbb` creates a VLAN
interface whose `interface` is the FortiLink interface in `root`, makes it the
tenant's `default-virtual-switch-vlan`, and the `root` administrator exports
`port10` with `set export-to bbb`. The tenant then sees the switch with `set
type virtual` and `set owner-vdom "root"`, and the port with `set vlan
"bbb-vlan99"`, "even though there is no FortiLink interface in the bbb VDOM";
the `root` view of the port shows only `set export-to "bbb"` (pp. 124–126).
From FortiOS 6.2.0 these features are supported on ports shared between VDOMs:
PoE pre-standard detection, the dynamic MAC learning limit, the QoS egress CoS
queue policy, and the port security policy (p. 124). From FortiOS 6.4.3 a tenant
can also set `lldp-status` and `lldp-profile` on its virtual ports; `auto-isl`
is ignored there and stays disabled (p. 176). **Shared ports do not support
DHCP snooping** (p. 126), which matters because Chapter 08's snooping lab put
snooping on VLANs, not ports, and nothing in this lab enables it.

**Virtual port pools.** Instead of exporting a port directly, the `root`
administrator can place it in a pool (`config switch-controller
virtual-port-pool`, then `set export-to-pool <pool>` on the port); the tenant
administrator claims it with `execute switch-controller virtual-port-pool
request <SN> <port>`, after which the port shows both `export-to-pool` and
`export-to` in `root`. `execute switch-controller virtual-port-pool show` and
`show-by-pool <pool>` list the pools (pp. 125–126). To move a pooled port to a
different pool, leave and re-enter the port's configuration (p. 126).

**Shared VLANs.** In the second model all ports and VLANs are created and
assigned by the controlling VDOM's administrator. The FortiOS GUI cannot assign
a VLAN of another VDOM as a port's native VLAN, so use the CLI (pp. 126–127).

**QinQ.** VLAN stacking gives each customer of a managed service provider its
own customer VLAN range in its own VDOM, carried inside a service VLAN that
must be in the VDOM of the FortiLink interface (pp. 127–130). It is a dash in
the matrix's 1xxE/1xxF column and a chain in the 200 Series column, and DHCP
relay, DHCP snooping, IGMP snooping, IP source guard, private VLANs, and STP
are not supported with it. This volume treats QinQ as read-and-predict.

Two more facts: the Security Rating feature (Chapter 06's topology
recommendations) is available only when VDOMs are disabled (p. 279), and
inter-VLAN routing offload is not supported in multitenancy VDOMs (Chapter 04).

### VDOM capacity on the lab controllers

VDOM counts depend on the platform and license, and the local references do not
list them for the lab's FortiGates. What the volume knows:

| Option | What to expect | Source |
| --- | --- | --- |
| C1 (40F or 60F) | VDOMs are a FortiGate feature on these models; record the count your unit reports | `get system status` (Lab 10.3 step 1) |
| C2 (FGT-1 evaluation) | Chapter 01 lists the evaluation cap as two VDOMs. Volume CIX found that the evaluation allows only **one traffic VDOM**: creating a second traffic VDOM failed with `Could not create VD, all VD licenses have been used`, and setting `root` to an admin VDOM still left one traffic VDOM. This lab's FortiLink, VLANs, and policies live in `root`, which must stay a traffic VDOM, so a tenant traffic VDOM is expected to fail: **multi-tenancy NO-GO on C2** unless your test says otherwise | [Volume CIX, Chapter 07](../../volume-109-fortinet-isfw-vdom-lab/chapters/07-vdoms-for-hard-separation.md); Lab 10.3 step 3 |
| C3 (licensed FortiGate-VM) | Depends on the VM license; record what yours allows | `get system status` |

### Where the sources differ

| FortiLink Guide 7.6.7 | FortiOS 7.6.0 CLI Reference or FortiSwitchOS 7.6.7 | This chapter |
| --- | --- | --- |
| `lldp-settings` table: `device-detection` "By default, this setting is disabled" (p. 174); the same page group says dynamic detection is enabled in FortiOS and disabled on managed switches (p. 172) | FortiOS 7.6.0: `device-detection` default `enable`; FortiSwitchOS: `disable`, FortiLink mode only (CLI Reference, p. 144) | Reads it; changes nothing |
| `management-interface {internal \| management}` (p. 174) | FortiOS 7.6.0: `internal` or `mgmt` | Reads it |
| LLDP profile syntax lists `config-tlvs` (p. 173) and omits `assign-vlan` (p. 172), but the examples use `custom-tlvs` (p. 175) and `assign-vlan` (p. 169) | FortiOS 7.6.0: `custom-tlvs`, `assign-vlan` | Uses the 7.6.0 names |
| Network policy VLAN by interface name, `vlan-intf` | FortiSwitchOS: `vlan <0-4094>` by number (CLI Reference, p. 139) | Lab 10.1 records the VLAN number the switch receives |
| DSCP map syntax `configure map <map_name>` (p. 286) | FortiOS 7.6.0: `config map` | `config map` |
| Queue weights 0–63 (p. 286) | FortiOS 7.6.0: integer, 0 to 4294967295 | Uses no weights |
| Tenant VLAN example enables `switch-controller-dhcp-snooping` (p. 124) | The same guide: shared ports do not support DHCP snooping (p. 126) | Leaves DHCP snooping off |
| FS-1xxE and FS-1xxF: a single QoS map (p. 285) | Matrix note 18 adds the FS-110G-FPOE and FS-124G; the Administration Guide lists one dot1p and one DSCP map per switch for named E, F, and G models (p. 365); the CLI Reference names only the FS-124E and FS-148E families (pp. 165–166) | Lab 10.2 records which map is used |

### Model support for this chapter

From the FortiSwitchOS 7.6.7 feature matrix (`temp/nse5fsw/fm767.txt`, the
position-based read); chain = standalone and managed, check = standalone only,
dash = not supported:

| Feature | 1xxE/1xxF (S1 FS-108F, S2 FS-124F) | 200 Series (S3) | Note |
| --- | --- | --- | --- |
| LLDP transmit | Chain | Chain | |
| LLDP-MED | Chain | Chain | |
| LLDP-MED: ELIN support | Chain | Chain | Location TLVs; not used here |
| 802.1p support, including priority queuing, trunk and WRED | Chain | Chain | Note 18: one QoS map on FS-1xx models |
| QoS queue counters | Dash | Chain | |
| Tail-drop policy | Check | Check | Standalone only, so the drop policy is not a FortiLink lab item |
| RED drop policy | Dash | Check | |
| WRED drop policy | Dash | Dash | |
| QoS marking (IPv4/IPv6) | Dash | Check | ACL remark actions, standalone |
| Summary of configured queue mappings | Chain | Chain | |
| Egress priority tagging (IPv4/IPv6) | Dash | Chain | `egress-pri-tagging` in a dot1p map |
| ECN (IPv4/IPv6) | Dash | Dash | ECN models are the FS-3032E/D, FS-1048E/D, FS-5xxD, and FS-4xxE (FortiLink Guide, p. 289) |
| Real-time egress queue rates | Only the 148F and 148F-POE in the column (note 11) | Check | Standalone `qos-rates` |
| VLAN stacking (QinQ) | Dash | Chain | |
| Multi-tenancy (VDOMs) | No row | No row | A FortiGate feature; the FortiLink Guide states no model limit |

## Design Considerations

### Exam tasks this chapter practices

| Exam task | Labs here | Track 2 mode |
| --- | --- | --- |
| 1.2 QoS and LLDP-MED | 10.1, 10.2 (primary) | Build + predict |
| 2.3 Multi-tenancy | 10.3, 10.4 (primary) | Build within the controller's VDOM capacity + predict |
| 4.3 View and extract information | 10.1 (LLDP neighbors), 10.2 (QoS statistics) | Predict |

### Hosts, ports, and VLANs

| Lab | Port and host | VLAN plan |
| --- | --- | --- |
| 10.1 LLDP-MED | `port1`, endpoint A running `lldpd`; optionally an LLDP-MED phone on `port4` | `fsw-users` native (DHCP), `fsw-voice` (1742) added tagged by `assign-vlan`; endpoint A gets `10.174.42.30/24` on a 1742 subinterface |
| 10.2 QoS | `port2` endpoint B (sender), `port1` endpoint A (receiver) | Both in `fsw-users`; `port2` moves there temporarily with `10.174.41.20/24`, as in Chapters 08 and 09 |
| 10.3 Dedicated ports | `port2` endpoint B exported to `tenant-174`; switch `port4` through the pool `pool-174` | `fsw-tenant` (1745) moved into `tenant-174`; endpoint B adds `10.174.45.20/24` |
| 10.4 Shared VLANs | `port2` endpoint B | `fsw-iot` native (root) plus `fsw-tenant` tagged (tenant), then `fsw-tenant` native |

`port1` and `port2` keep BPDU guard (Chapter 05); `lldpd` sends LLDP, not
BPDUs, so it is safe on `port1`. Port changes use `set lldp-profile`, `set
qos-policy`, `set vlan`, `append allowed-vlans`, and `export-to`; a list is set
back only to the value you recorded, which includes `quarantine` (as Chapter 04
restored `<PORT1_ALLOWED>`). Lab 10.4 records `port2`'s list as
`<PORT2_ALLOWED>`. Switch `port4` is the switch's port, not the FortiGate
`port4` that is the FortiLink port on C3.

### The FortiLink interface name and the VDOM contexts

Commands are written for C2's names where it matters: the FortiLink interface
is `port3` on C2, `port4` on C3, and `<FL_PORT>` (or `fortilink`) on C1, as in
Chapter 04. No command in this chapter names it directly except in read-only
`show` steps.

Labs 10.3 and 10.4 run in multi-VDOM mode. A block that starts with `FGT #
config vdom` and `edit <VDOM>`, or with `FGT # config global`, enters that
context; the `FGT #` lines that follow inside it are commands at that context's
prompt, and a final `FGT # end` leaves it. Outside those two labs the controller
is in its normal single-VDOM mode.

### The C2 budget

No lab adds a firewall policy, an interface, or a route. Lab 10.3 **moves** the
existing `fsw-tenant` interface into the tenant VDOM instead of creating one,
and no lab needs traffic between VDOMs, so no inter-VDOM link (which would be
interfaces) or policy is built. LLDP profiles, QoS objects, pools, and VDOM
settings do not count against the caps. On C2, Labs 10.1 and 10.2 run in full
when Lab 4.1's lab VLANs were a GO (after a NO-GO, Chapter 04 sends this
chapter to C1 or C3); Labs 10.3 and 10.4 are expected to stop at the VDOM
go/no-go (see the capacity table) and continue read-and-predict.

### Lab order and state

| Lab | Builds | Rollback leaves |
| --- | --- | --- |
| 10.1 | LLDP profile `lldp-med-174`; `port1` (and optionally `port4`) using it; `switch-device-tag`; `lldpd` on endpoint A | All removed; `port1` back to its recorded profile and allowed list |
| 10.2 | `dot1p-174`, `dscp-174`, `queue-174`, `qos-174`; `port1` and `port2` using `qos-174`; `port2` in `fsw-users`; `iperf` on endpoint A | All removed; ports back to their recorded QoS policy; `port2` in `fsw-iot` |
| 10.3 | Multi-VDOM mode, VDOM `tenant-174`, `fsw-tenant` in it, `default-virtual-switch-vlan`, `port2` exported, `pool-174` with switch `port4` claimed | All removed; single-VDOM mode; `fsw-tenant` back in `root` |
| 10.4 | The same VDOM state as 10.3 (or carried over from it); `fsw-tenant` tagged and then native on `port2` | All removed; single-VDOM mode |

Each lab returns the controller, `FSW-A`, and the endpoints to the state
Chapter 09 left (ADDENDUM 9), with one documented shortcut: if you run Lab 10.4
straight after Lab 10.3, you may stop Lab 10.3's rollback where it says so and
keep the VDOM state for Lab 10.4, whose rollback then finishes the teardown. On
S3 the profile and QoS objects reach `FSW-B` too, but only `FSW-A`'s ports are
changed.

### What to keep after this chapter

Nothing. The predefined LLDP profiles and QoS objects stay as they were, and
the endpoints keep only the packages they had (`tcpdump` on both, `iperf` on
endpoint B).

## Implementation and Automation

The labs are the implementation. Four habits make them traceable.

**Read the predefined objects first and never edit them.** Record what exists
before creating anything; the lab objects all end in `-174`:

```text
FGT # show switch-controller lldp-profile
FGT # show switch-controller qos qos-policy
FGT # show switch-controller qos queue-policy
```

**Generate marked traffic from Linux.** `iperf` (version 2) sets the IP type of
service byte with `-S` (DSCP shifted left by two bits, so EF, DSCP 46, is
`0xB8`, and CS3, DSCP 24, is `0x60`), and `ping -Q` does the same for ICMP
(`iperf(1)`, `ping(8)`):

```bash
# endpoint A (receiver)
iperf -s -u -i 5
# endpoint B (sender), 8 Mbit/s for 20 s with DSCP EF
iperf -c <LEASE_A> -u -b 8M -t 20 -S 0xB8
```

**Make a Linux host look like an LLDP-MED phone.** `lldpd` sends LLDP-MED frames
as the class given with `-M` (3 is a Class III communication device, the class
of an IP phone), and `lldpcli show neighbors details` prints what it received,
including LLDP-MED network policies (`lldpd(8)`, `lldpcli(8)`). Running it in
the foreground with `-d` avoids any dependence on how the distribution's service
passes options:

```bash
# endpoint A
sudo systemctl stop lldpd
sudo lldpd -d -M 3
# second window
sudo lldpcli show neighbors details
```

**Know which context you are in.** In multi-VDOM mode, `get system status`
shows the current VDOM, and a command in the wrong context either fails or, for
`config system interface` and `edit` of a new name, creates something in the
wrong place. Check before each block in Labs 10.3 and 10.4.

The FortiOS configuration commands in this chapter were checked against the
FortiOS 7.6.0 CLI Reference with `temp/nse5fsw/verify.py`. `execute`,
`diagnose`, and `get` commands were checked against the FortiLink Guide 7.6.7
where it prints them (`diagnose switch-controller switch-info lldp
neighbors-summary`, `neighbors-detail`, and `stats`, `diagnose
switch-controller switch-info qos-stats`, `execute switch-controller
virtual-port-pool request` and `show`, `execute switch-controller
get-conn-status`) and otherwise against the FortiOS 8.0.1 CLI Reference as a
cross-check (`execute backup config`, `execute restore config`, and `execute
switch-controller virtual-port-pool show-by-pool`, which the guide also prints
with a placeholder, p. 126); `get system
status` and `get router info routing-table all` are standard FortiOS commands
that no local reference prints. The context commands `config vdom` and `config
global` are not tables in the 7.6.0 reference; they were matched by hand to the
FortiLink Guide 7.6.7, which prints `config vdom` with `edit` (pp. 128, 176–177)
and `config global` (p. 45). Switch commands were checked against the
FortiSwitchOS 7.6.7 CLI Reference, with these matched by hand: `get switch
lldp neighbors-summary`, `neighbors-detail <port>`, `profile`, and `settings`
(alternatives of a syntax line that wraps and that the verifier cannot expand,
p. 499), `diagnose switch physical-ports qos-stats list [<port_list>]` (an
optional argument, p. 372), and `show switch lldp profile`, `show switch
physical-port`, and `show switch interface`, which are the `show` forms of
documented `config` tables (the Administration Guide prints `show switch lldp
profile Forti670i`, `show switch physical-port port4`, and `show switch
interface port4`, pp. 186–187). The endpoint commands follow `lldpd(8)`,
`lldpcli(8)`, `iperf(1)` (version 2), `ip-link(8)`, `ip-address(8)`, and
`ping(8)`.

## Validation and Troubleshooting

| Symptom | Likely cause | Check |
| --- | --- | --- |
| The endpoint shows no LLDP-MED network policy | The port still uses `default-auto-isl`, `med-tlvs` lacks `network-policy`, the policy is not `enable`d, or the VLAN is neither native nor allowed on the port | `show switch-controller managed-switch`; `show switch lldp profile <name>` on the switch |
| The voice policy disappears after a VLAN change | The TLV follows the port's actual VLANs; the VLAN was removed or `assign-vlan` is off | `show switch interface <port>` |
| The voice VLAN is advertised untagged | The voice VLAN is the port's native VLAN or in its untagged list | `show switch interface <port>` |
| An edge port forms an ISL with a host | Its LLDP profile has `auto-isl enable` (the default for new profiles) | `show switch-controller lldp-profile` |
| FortiLink or ISL detection becomes slow after an LLDP change | Global LLDP timers were changed | `get switch-controller lldp-settings`; restore the recorded values |
| Marked traffic is not prioritized | The ingress port does not trust the right map, both maps are trusted, or (FS-1xx) another map was configured first | `show switch interface <port>`; `get switch qos ip-dscp-map` |
| `max-rate` seems ignored on an FS-1xx model | The value is not a multiple of 16 kbps, or rounded to 0 | Use multiples of 16 |
| `qos-stats` prints nothing useful on S1 or S2 | QoS queue counters are a dash in the 1xxE/1xxF column | Use the rate-limit method of Lab 10.2 |
| `Could not create VD, all VD licenses have been used` | The controller's license allows no more traffic VDOMs (C2) | `get system status`; use C1 or C3 |
| The tenant VDOM shows no managed switch | No port is exported to it, or the export was refused | `show switch-controller managed-switch` in `root` |
| An exported port carries the wrong VLAN | `default-virtual-switch-vlan` is unset in the tenant VDOM | `get switch-controller global` in the tenant VDOM |
| A tenant VLAN cannot be chosen as a native VLAN in the GUI | Documented GUI limitation for VLANs of another VDOM | Use the CLI (p. 126) |
| `fsw-tenant` cannot be moved between VDOMs | Something still refers to it (a port, the tenant default VLAN, a DHCP server, a policy) | Remove the reference first |

## Security and Best Practices

- **Give edge ports an edge profile.** A profile with `auto-isl disable` on
  host ports stops a rogue switch from forming an ISL into the fabric; keep
  `default-auto-isl` for ports that really connect switches.
- **Advertise only the TLVs you need.** LLDP-MED inventory and location TLVs
  tell any listener what the switch is and where; enable `network-policy` for
  phones and leave the rest off unless a service uses them.
- **Put voice in its own VLAN and trust markings only where they come from a
  trusted device.** A host can set DSCP 46 on any packet; trust DSCP on phone
  ports and uplinks, not on general user ports, or police the high-priority
  queue.
- **Never starve queue 7.** It carries the switch's own control traffic.
- **Treat the VDOM boundary as the tenant boundary.** Dedicated ports give a
  tenant administrator control of only its own ports; shared VLANs give no
  administrative separation at all, so use them only when one team runs every
  VDOM.
- **Plan VDOM mode before deployment.** Switching a FortiGate between
  single-VDOM and multi-VDOM mode reorganizes its configuration and its CLI;
  take a backup and expect administrators to be logged out.
- **Remember what shared ports lose.** DHCP snooping is not supported on them;
  use other controls (802.1X, the learning limit, ACLs on the 200 Series) on
  tenant ports.

## References and Knowledge Checks

**References**

- [Fortinet, *FortiLink Guide (FortiOS 7.6.7)*](https://docs.fortinet.com/document/fortiswitch/7.6.7/fortilink-guide)
  — `config global` (p. 45), VLAN interface templates per VDOM (p. 34),
  FortiSwitch units on a NAT VDOM (p. 80), multitenancy and VDOMs, dedicated
  ports, virtual port pools, shared VLANs, and QinQ (pp. 124–130), voice device
  detection with `fortivoice.fortilink` and `voice-qos` (pp. 164–171), LLDP-MED
  settings, LLDP profiles, LLDP settings, asset tags, MED policies, LLDP display
  commands, and tenant LLDP (pp. 172–177), Security Rating and VDOMs (p. 279),
  QoS with managed switches, the voice QoS policy, and ECN (pp. 285–290).
- [Fortinet, *FortiSwitchOS 7.6.7 Administration Guide (Standalone Mode)*](https://docs.fortinet.com/document/fortiswitch/7.6.7/administration-guide)
  — LLDP-MED, configuration notes, network policies, VLAN assignment, and the
  deployment example (pp. 175–188), QoS: model differences, classification,
  marking, queuing, determining the egress queue, and maps (pp. 365–370).
- [Fortinet, *FortiSwitchOS 7.6.7 CLI Reference*](https://docs.fortinet.com/document/fortiswitch/7.6.7/fortiswitchos-cli-reference)
  — ACL actions `remark-cos` and `remark-dscp` (pp. 103–105), `config switch
  interface` (`default-cos`, `trust-dot1p-map`, `trust-ip-dscp-map`,
  pp. 126–131), `config switch lldp profile` (pp. 139–143), `config switch lldp
  settings` (p. 144), `config switch physical-port` (`lldp-profile`, p. 157),
  `config switch qos dot1p-map`, `ip-dscp-map`, and `qos-policy` (pp. 165–170),
  `diagnose switch physical-ports qos-rates` and `qos-stats` (pp. 370–372), `get
  switch lldp` (pp. 499–500), `get switch qos` (p. 508).
- [Fortinet, FortiOS 7.6 documentation](https://docs.fortinet.com/product/fortigate/7.6)
  — the FortiOS 7.6.0 CLI Reference: `config switch-controller lldp-profile`,
  `lldp-settings`, `qos dot1p-map`, `qos ip-dscp-map`, `qos queue-policy`, `qos
  qos-policy`, `virtual-port-pool`, `switch-interface-tag`, `global`
  (`default-virtual-switch-vlan`), `config switch-controller managed-switch`
  (`ports`: `lldp-profile`, `lldp-status`, `qos-policy`, `export-to`,
  `export-to-pool`; `switch-device-tag`, `qos-drop-policy`, `owner-vdom`,
  `type`), `config system global` (`vdom-mode`), `config system vdom`, `config
  system settings` (`vdom-type`), `config system interface` (`vdom`).
- FortiOS 8.0.1 CLI Reference (cross-check only) — `execute backup config`,
  `execute restore config`.
- FortiSwitchOS 7.6.7 feature matrix (`temp/fsw/FSW-7.6.7-Feature-Matrix.pdf`)
  — the LLDP, Quality of Service, and VLAN stacking rows; notes 11 and 18.
- [Volume CIX, Chapter 07](../../volume-109-fortinet-isfw-vdom-lab/chapters/07-vdoms-for-hard-separation.md)
  — the FortiGate-VM evaluation's single traffic VDOM.
- [`lldpd(8)`](https://manpages.ubuntu.com/manpages/noble/man8/lldpd.8.html),
  [`lldpcli(8)`](https://manpages.ubuntu.com/manpages/noble/man8/lldpcli.8.html),
  [`iperf(1)`](https://manpages.ubuntu.com/manpages/noble/man1/iperf.1.html),
  [`ip-link(8)`](https://manpages.ubuntu.com/manpages/noble/man8/ip-link.8.html),
  [`ping(8)`](https://manpages.ubuntu.com/manpages/noble/man8/ping.8.html).

**Knowledge checks**

1. Which LLDP profile does a managed port use by default in FortiOS 7.6.0, and
   why should a profile for host ports set `auto-isl disable`?
2. An LLDP-MED voice policy names a VLAN that is neither native nor allowed on
   the port. What does the switch send, and what does `assign-vlan enable`
   change?
3. When is a voice VLAN advertised tagged, and when untagged?
4. Name the FortiSwitchOS object that corresponds to a FortiOS `queue-policy`,
   and the switch settings that a FortiOS `qos-policy` becomes.
5. A port trusts both dot1p and DSCP. Which value decides the queue of a tagged
   IP packet, and why does Fortinet advise against trusting both?
6. A port trusts dot1p only. Which queue does an untagged packet with DSCP 46
   use?
7. What does feature matrix note 18 say, and why does Lab 10.2 use rate limits
   instead of queue counters on S1 and S2?
8. In the dedicated-port model, what does the tenant VDOM see, and which VLAN
   becomes the native VLAN of an exported port?
9. What does a virtual port pool add to a direct export?
10. Which feature do shared ports not support, and how does the shared-VLAN
    model differ from dedicated ports in who may configure the port?
11. Why is live multi-tenancy expected to fail on the FortiGate-VM evaluation
    in this lab?

## Hands-On Lab

**Shared prerequisites.** Chapter 09 complete (ADDENDUM 9 state):
`<SWITCH_SN>` `Authorized/Up` at `10.255.1.2` with profile `fsw-174-prof` (on
S3, `FSW-A`; `FSW-B` managed and in the MCLAG of Chapter 06); `port1` native
`fsw-users` (endpoint A, DHCP, BPDU guard, allowed list `<PORT1_ALLOWED>` with
`quarantine`) and `port2` native `fsw-iot` (endpoint B, `10.174.43.20/24`, BPDU
guard), both with no security policy and no port policy; switch `port4` up with
no description; VLAN interfaces `fsw-voice` (1742, `10.174.42.1/24`, ping, no
DHCP) and `fsw-tenant` (1745, `10.174.45.1/24`, ping, in `root`, in no zone);
P1 and P2 as Chapter 04 left them, and on C2 P3 free; the controller in
single-VDOM mode. Endpoints A and B have `tcpdump`; endpoint B has `iperf`.
Track 2: the Lab 2.2 pre-provisioning outcome and the stand-in entry
`S248EPTF18000000` if that outcome allowed it. **Optional:** an LLDP-MED IP
phone (on a POE or FPOE switch, or with a PoE injector). **Cost:** none.

`FGT #` is the controller on any option. `<SWITCH_SN>` is your switch's serial
number (on Track 2, `S248EPTF18000000`). `<IFACE>` and `<IFACE_B>` are endpoint
A's and endpoint B's wired interfaces, and `<LEASE_A>` endpoint A's current
`fsw-users` address (`ip -br addr show <IFACE>`). Before the first change, back
up the controller:

```text
FGT # execute backup config tftp fgt-pre-10-1-174.conf 10.30.99.50
```

### Lab 10.1 — LLDP profiles and an LLDP-MED voice policy

**Objective:** Read the controller's LLDP settings and profiles and the
switch's LLDP view, make endpoint A an LLDP-MED endpoint, build an LLDP profile
with voice and voice-signaling network policies for `fsw-voice`, apply it to
`port1`, and show that endpoint A learns the voice VLAN, priority, and DSCP
value and can use VLAN 1742 on `port1`; predict what a phone learns from the
default profile.

**Platform notes:** Hands-on on C1 and C3 (and C2 when Lab 4.1's lab VLANs
were a GO) with S1, S2, or S3 (on S3, `FSW-A`): LLDP transmit and LLDP-MED are
chain in both columns. No policy, interface, or route is added. Step 9 (a real
phone on `port4`) is optional and needs PoE or an injector. The LLDP timers are
read only on every option. Track 2: the profile is built live; the port step
runs on the stand-in only with Lab 2.2's third outcome; the endpoint and switch
steps are read-and-predict.

**Track 1, Part A — what exists:**

1. Read the controller side:

   ```text
   FGT # get switch-controller lldp-settings
   FGT # show switch-controller lldp-profile
   FGT # show switch-controller managed-switch <SWITCH_SN>
   ```

   Record `tx-interval` (30), `tx-hold` (4), `fast-start-interval` (2),
   `management-interface`, and `device-detection` (the 7.6.0 default is
   `enable`; the guide's table says disabled, p. 174). List the profiles: expect
   `default`, `default-auto-isl`, `default-auto-mclag-icl`, and
   `fortivoice.fortilink` (Chapter 09 recorded whether it exists). For
   `port1`, record `lldp-profile` and `lldp-status`; a missing line means the
   7.6.0 defaults, `default-auto-isl` and `tx-rx`. Record `port1`'s
   `allowed-vlans` and `untagged-vlans` and check them against
   `<PORT1_ALLOWED>`.

2. Read the switch side and the neighbors:

   ```text
   FSW # get switch lldp settings
   FSW # get switch lldp profile
   FSW # get switch lldp neighbors-summary
   FGT # diagnose switch-controller switch-info lldp neighbors-summary <SWITCH_SN>
   ```

   Predict the neighbors. **Answer:** the controller on `<FSW_FL_PORT>` (the
   FortiLink peer, detected with LLDP since Chapter 02) and, on S3, `FSW-B` on
   the ICL ports; nothing on `port1` or `port2`, because Chapter 09 removed
   `lldpd` from the endpoints. In `get switch lldp profile`, record the
   `med-tlvs` of `default-auto-isl`; the CLI Reference's standalone example
   shows it empty (p. 500).

**Track 1, Part B — endpoint A as an LLDP-MED endpoint:**

3. Install `lldpd` on endpoint A and run it as a Class III endpoint in the
   foreground:

   ```bash
   # endpoint A
   sudo apt install -y lldpd
   sudo systemctl stop lldpd
   sudo lldpd -d -M 3
   ```

   In a second window, after 30 seconds:

   ```bash
   # endpoint A
   sudo lldpcli show neighbors details
   ```

   ```text
   FSW # get switch lldp neighbors-detail port1
   ```

   The switch lists endpoint A on `port1`, and endpoint A lists the switch.
   Predict whether endpoint A receives an LLDP-MED network policy now.
   **Answer:** no voice policy for VLAN 1742: `port1` still uses its recorded
   profile, which has no network policy for `fsw-voice`, and VLAN 1742 is not
   allowed on `port1` (the cross-check, CLI Reference, p. 143). Record any
   LLDP-MED TLVs endpoint A does receive and the `MED type` the switch shows
   for endpoint A (the Administration Guide's phone example shows
   `Communication Device Endpoint (Class III)`, p. 187).

4. Show that VLAN 1742 is not usable on `port1` yet:

   ```bash
   # endpoint A
   sudo ip link add link <IFACE> name <IFACE>.1742 type vlan id 1742
   sudo ip addr add 10.174.42.30/24 dev <IFACE>.1742
   sudo ip link set <IFACE>.1742 up
   ping -c 3 -I <IFACE>.1742 10.174.42.1
   ```

   The ping fails: the switch drops VLAN 1742 frames on a port that does not
   allow it. Leave the subinterface in place.

**Track 1, Part C — the LLDP-MED profile:**

5. Create the profile. `auto-isl disable` makes it an edge profile; the voice
   values follow the predefined voice QoS table (DSCP 46 and CoS 5 for voice
   data, DSCP 24 and CoS 3 for control):

   ```text
   FGT # config switch-controller lldp-profile
   edit "lldp-med-174"
   set med-tlvs inventory-management network-policy
   set auto-isl disable
   config med-network-policy
   edit "voice"
   set status enable
   set vlan-intf "fsw-voice"
   set assign-vlan enable
   set priority 5
   set dscp 46
   next
   edit "voice-signaling"
   set status enable
   set vlan-intf "fsw-voice"
   set assign-vlan enable
   set priority 3
   set dscp 24
   next
   end
   next
   end
   FGT # show switch-controller lldp-profile lldp-med-174
   ```

   Record whether the `show` lists the other six network policies (they cannot
   be added or deleted on the switch, p. 143).

6. Apply it to `port1`:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port1"
   set lldp-profile "lldp-med-174"
   next
   end
   next
   end
   ```

7. Read what the switch received and what endpoint A learns:

   ```text
   FSW # show switch lldp profile lldp-med-174
   FSW # show switch physical-port port1
   FSW # show switch interface port1
   FGT # show switch-controller managed-switch <SWITCH_SN>
   ```

   Predict three things. (a) The VLAN in the switch's `voice` policy.
   **Answer:** `set vlan 1742`: the switch's network policy takes a VLAN number
   (p. 139), and FortiOS translates `vlan-intf "fsw-voice"`. Record what the
   switch shows. (b) Whether VLAN 1742 is now allowed on `port1`. **Answer:**
   yes, by `assign-vlan` (Administration Guide, p. 183); record whether it
   appears in the switch's `show switch interface port1` and whether FortiOS
   changed `port1`'s `allowed-vlans` in its own configuration (the
   documentation does not say; record what happens). (c) How endpoint A's
   `lldpcli show neighbors details` shows the voice policy. **Answer:** VLAN
   1742, tagged, priority 5, DSCP 46, and a voice-signaling policy with VLAN
   1742, priority 3, DSCP 24: tagged because 1742 is neither native nor
   untagged on `port1` (p. 143). Repeat step 4's ping; it now works.

8. Read the neighbor from the controller and give the switch an asset tag for
   the inventory TLV:

   ```text
   FGT # diagnose switch-controller switch-info lldp neighbors-detail <SWITCH_SN>
   FGT # diagnose switch-controller switch-info lldp stats <SWITCH_SN> port1
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   set switch-device-tag "fsw-a-174"
   next
   end
   ```

   The neighbor detail shows endpoint A on `port1` with its LLDP-MED
   capabilities. After the next LLDP transmission, record whether endpoint A's
   `lldpcli show neighbors details` shows `fsw-a-174` in the switch's inventory
   section; the guide says the tag is used by LLDP (p. 175) but not which TLV
   carries it, so record what happens.

9. Optional, a real phone. Apply the profile to `port4` (record its
   `lldp-profile` first), plug in an LLDP-MED phone, and read the neighbor:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port4"
   set lldp-profile "lldp-med-174"
   next
   end
   next
   end
   FSW # get switch lldp neighbors-detail port4
   ```

   Record the phone's `MED type` and the network policies the switch lists for
   it (compare the Administration Guide's example, pp. 187–188), and the VLAN
   the phone's own network screen reports. `fsw-voice` has no DHCP server
   (Chapter 04), so the phone gets no address in VLAN 1742 unless you give it
   a static one; that is expected.

**Track 2:** Run steps 1 and 5 on your controller. If Lab 2.2's third outcome
applies, run step 6 against `S248EPTF18000000` and check it with `show
switch-controller managed-switch S248EPTF18000000`. Skip the switch and
endpoint steps.

**Track 2: read-and-predict.**

1. The CLI Reference prints this standalone switch's profiles (p. 500):

   ```text
   S524DF4K15000024 # get switch lldp profile
   == [ default ]
   name: default 802.1-tlvs: 802.3-tlvs: med-tlvs: inventory-management network-policy
   == [ default-auto-isl ]
   name: default-auto-isl 802.1-tlvs: 802.3-tlvs: med-tlvs:
   ```

   Predict what an LLDP-MED phone on a port with `default-auto-isl` learns
   about its voice VLAN on that switch. **Answer:** nothing: `default-auto-isl`
   sends no LLDP-MED TLVs, so the phone gets no network policy and stays in the
   port's native VLAN. Because `default-auto-isl` is also the FortiOS default
   for managed ports, a phone port needs its own profile.
2. The Administration Guide's deployment example (pp. 186–188) gives `port4`
   `allowed-vlans 400` and a profile whose `voice` policy has `vlan 400`,
   priority 5, DSCP 46; the phone's neighbor detail ends with:

   ```text
   LLDP-MED, Network Policies:
   voice: VLAN: 400 (tagged), Priority: 5 DSCP: 46
   voice-signaling: VLAN: 400 (tagged), Priority: 4 DSCP: 35
   streaming-video: VLAN: 400 (tagged), Priority: 3 DSCP: 40
   ```

   Predict why VLAN 400 is tagged. **Answer:** it is allowed on `port4` but is
   neither the native VLAN nor in the untagged list (p. 143).
3. The same profile on a port where VLAN 400 is not allowed and `assign-vlan`
   is disabled. Predict. **Answer:** the voice policy is not sent at all: a
   VLAN-tagged policy is transmitted only if the VLAN is on the interface
   (p. 143). The negative test checks this live.

**Expected result:** Track 1: the LLDP settings, profiles, and `port1`'s
defaults are recorded; endpoint A, running `lldpd -M 3`, received no voice
policy from the recorded profile and could not use VLAN 1742; with
`lldp-med-174` on `port1`, the switch added VLAN 1742 and endpoint A learned a
tagged voice policy (1742, priority 5, DSCP 46) and voice-signaling policy and
reached `10.174.42.1` over VLAN 1742; the asset tag result is recorded. Track
2: the profile exists and the predictions are answered.

**Negative test:** Turn VLAN assignment off in both policies and wait one
`tx-interval`:

```text
FGT # config switch-controller lldp-profile
edit "lldp-med-174"
config med-network-policy
edit "voice"
set assign-vlan disable
next
edit "voice-signaling"
set assign-vlan disable
next
end
next
end
```

Predict and observe: VLAN 1742 leaves `port1` (`show switch interface port1`),
step 4's ping fails, and endpoint A's `lldpcli show neighbors details` no longer
lists the voice and voice-signaling policies, because a tagged policy is sent
only while its VLAN is on the port (p. 143). Record how long endpoint A keeps
the old policy (its TTL is `tx-hold` times `tx-interval`, 120 s with the
defaults). Track 2: prediction 3 is the negative test.

**Rollback:** Stop `lldpd` with Ctrl+C in its window, then put the ports back
to the profile recorded in step 1 (shown here as the 7.6.0 default), remove the
tag and the profile, and clean up endpoint A:

```text
FGT # config switch-controller managed-switch
edit <SWITCH_SN>
unset switch-device-tag
config ports
edit "port1"
set lldp-profile "default-auto-isl"
next
end
next
end
FGT # config switch-controller lldp-profile
delete "lldp-med-174"
end
```

If you did step 9, set `port4`'s `lldp-profile` back to its recorded value in
the same `config ports` block before deleting the profile, and unplug the phone.

```bash
# endpoint A
sudo ip link delete <IFACE>.1742
sudo apt remove -y lldpd
```

Confirm with `show switch-controller managed-switch <SWITCH_SN>` that `port1`'s
allowed and untagged lists equal the values recorded in step 1
(`<PORT1_ALLOWED>`, with `quarantine`); if FortiOS left VLAN 1742 there, set
`allowed-vlans` back to `<PORT1_ALLOWED>`. Confirm that endpoint A still leases
from `fsw-users` and reaches `10.174.41.1`.

**Lab verified by:** *pending*

### Lab 10.2 — QoS maps, queue policies, and QoS policies on ports

**Objective:** Read the controller's QoS objects and what the switch holds,
build a dot1p map, a DSCP map, a queue policy with egress rate limits, and a
QoS policy, apply the QoS policy to `port1` and `port2`, and show with marked
`iperf` traffic which queue each DSCP value uses: through the rate limits on
every switch option, and through queue counters on S3; then show that trusting
dot1p instead of DSCP sends the same traffic to the default queue.

**Platform notes:** Hands-on on C1 and C3 (and C2 with a lab-VLAN GO) with S1,
S2, or S3 (on S3, `FSW-A`): 802.1p queuing is chain in both columns. On S1 and
S2, note 18 allows one QoS map, so step 8 records which map the switch uses;
QoS queue counters (step 9) are hands-on only on S3 (dash in 1xxE/1xxF); the
default-CoS step (negative test, part b) is not available on the FS-224E,
FS-224E-POE, FS-248E-POE, and FS-248E-FPOE (Administration Guide, p. 370).
QoS marking, real-time queue rates, drop policies, egress priority tagging,
and ECN are read-and-predict here on every option (standalone or unsupported
in the matrix; QoS marking on S3 belongs to standalone mode). Track 2: the QoS
objects are built live; the port step runs on the stand-in only with Lab 2.2's
third outcome; the traffic steps are read-and-predict.

**Track 1, Part A — what exists:**

1. Read the controller's QoS objects and the ports:

   ```text
   FGT # show switch-controller qos dot1p-map
   FGT # show switch-controller qos ip-dscp-map
   FGT # show switch-controller qos queue-policy
   FGT # show switch-controller qos qos-policy
   FGT # show switch-controller managed-switch <SWITCH_SN>
   ```

   Record the predefined objects: expect `voice-dot1p`, `voice-dscp`,
   `voice-egress`, and `voice-qos` (p. 289), and, because the 7.6.0 defaults
   name them, a queue policy and a QoS policy called `default`. For `port1` and `port2`, record
   `qos-policy`; a missing line means the 7.6.0 default, `"default"`. Also
   record the switch's `qos-drop-policy` and `qos-red-probability` (7.6.0
   default 12) without changing them: the matrix marks the drop policies as
   standalone-only or unsupported in both columns.

2. Read the switch:

   ```text
   FSW # get switch qos dot1p-map
   FSW # get switch qos ip-dscp-map
   FSW # get switch qos qos-policy
   FSW # show switch interface port1
   ```

   Predict which maps the switch holds. **Answer:** the documentation does not
   say whether FortiOS pushes maps that no port uses; record the names and their
   order. In `show switch interface port1`, record `trust-dot1p-map`,
   `trust-ip-dscp-map`, `default-cos`, and `qos-policy`. On S1 and S2 the order
   matters: note 18 says the first configured map is used.

**Track 1, Part B — build the QoS objects:**

3. Create the maps. The DSCP map sends EF to queue 5 and CS3 to queue 3; the
   dot1p map sends CoS 5 to queue 5 and CoS 3 to queue 3. Everything else falls
   to queue 0 by default:

   ```text
   FGT # config switch-controller qos ip-dscp-map
   edit "dscp-174"
   set description "Lab 10.2 EF and CS3"
   config map
   edit "ef"
   set diffserv EF
   set cos-queue 5
   next
   edit "cs3"
   set diffserv CS3
   set cos-queue 3
   next
   end
   next
   end
   FGT # config switch-controller qos dot1p-map
   edit "dot1p-174"
   set description "Lab 10.2 CoS 5 and 3"
   set priority-3 queue-3
   set priority-5 queue-5
   next
   end
   ```

4. Create the queue policy. `queue-0` is limited to 2,048 kbps. `queue-1` is a
   trap: `voice-dscp` would send EF to queue 1, so limiting it to 4,096 kbps
   shows whether the switch used `voice-dscp` instead of `dscp-174`. Queues 3 and
   5 are not limited. Both limits are multiples of 16 kbps for the FS-1xx
   models (Administration Guide, p. 365):

   ```text
   FGT # config switch-controller qos queue-policy
   edit "queue-174"
   set schedule strict
   set rate-by kbps
   config cos-queue
   edit "queue-0"
   set description "default, 2048 kbps"
   set max-rate 2048
   next
   edit "queue-1"
   set description "voice-dscp EF trap, 4096 kbps"
   set max-rate 4096
   next
   edit "queue-5"
   set description "EF, no limit"
   next
   end
   next
   end
   ```

5. Create the QoS policy. It trusts DSCP only, as Fortinet recommends:

   ```text
   FGT # config switch-controller qos qos-policy
   edit "qos-174"
   set trust-ip-dscp-map "dscp-174"
   set queue-policy "queue-174"
   set default-cos 0
   next
   end
   ```

**Track 1, Part C — the test path and a baseline:**

6. Put endpoint B in `fsw-users`, install `iperf` on endpoint A, and measure
   without the policy:

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port2"
   set vlan "fsw-users"
   next
   end
   next
   end
   ```

   ```bash
   # endpoint B
   sudo ip addr add 10.174.41.20/24 dev <IFACE_B>
   ping -c 3 <LEASE_A>
   # endpoint A
   sudo apt install -y iperf
   iperf -s -u -i 5
   # endpoint B, once with each marking
   iperf -c <LEASE_A> -u -b 8M -t 20
   iperf -c <LEASE_A> -u -b 8M -t 20 -S 0xB8
   ```

   With the ports still on their recorded QoS policy, endpoint A's server
   report should show about 8 Mbit/s for both runs. Record both.

**Track 1, Part D — apply the QoS policy:**

7. Apply `qos-174` to both ports: `port2` classifies on ingress (trust), and
   `port1` schedules and limits on egress (queue policy):

   ```text
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port1"
   set qos-policy "qos-174"
   next
   edit "port2"
   set qos-policy "qos-174"
   next
   end
   next
   end
   FSW # show switch interface port2
   FSW # get switch qos qos-policy
   ```

   Predict what `show switch interface port2` gains. **Answer:**
   `trust-ip-dscp-map "dscp-174"` and `qos-policy "queue-174"`: the FortiOS
   queue policy becomes the switch's QoS policy, and the FortiOS QoS policy
   becomes interface settings (CLI Reference, pp. 126–131, 167). Record what
   the switch shows.

8. Repeat the three runs:

   ```bash
   # endpoint B
   iperf -c <LEASE_A> -u -b 8M -t 20
   iperf -c <LEASE_A> -u -b 8M -t 20 -S 0xB8
   iperf -c <LEASE_A> -u -b 8M -t 20 -S 0x60
   ```

   Predict endpoint A's received rate for each. **Answer:** unmarked traffic
   (DSCP 0) goes to queue 0 and arrives at about 2 Mbit/s with heavy loss; EF
   goes to queue 5 and arrives at about 8 Mbit/s; CS3 goes to queue 3 and
   arrives at about 8 Mbit/s. Read the EF result as a test of note 18 on S1 and
   S2: about 8 Mbit/s means the switch used `dscp-174`; about 4 Mbit/s means it
   used `voice-dscp` (EF to queue 1, the trap); about 2 Mbit/s means no DSCP map
   was applied. Record which you got and compare it with the map order recorded
   in step 2. If the unmarked run is not limited at all, record that too: the
   documentation describes egress policing (p. 285) but does not show it on an
   FS-1xx port.

9. On S3, read the queue counters while an EF run is going (skip on S1 and S2,
   where QoS queue counters are a dash; record what the commands print there):

   ```text
   FGT # diagnose switch-controller switch-info qos-stats <SWITCH_SN> port1
   FSW # diagnose switch physical-ports qos-stats list port1
   ```

   Queue 5's unicast packet counter grows during the EF run and queue 0's
   during the unmarked run, with drops on queue 0. The switch command's port
   argument is optional (matched by hand, p. 372).

**Track 2:** Run steps 1, 3, 4, and 5 on your controller. If Lab 2.2's third
outcome applies, run step 7's controller block against `S248EPTF18000000`.
Check with `show switch-controller qos qos-policy qos-174` and `show
switch-controller qos queue-policy queue-174`.

**Track 2: read-and-predict.**

1. The CLI Reference prints this `qos-stats` output for one port (p. 372),
   trimmed:

   ```text
   S524DF4K15000024 # diagnose switch physical-ports qos-stats list 1
   port1 QoS Stats:
   queue | unicast pkts | unicast bytes | multicast pkts | multicast bytes
   ----------------------------------------------------------------------------------
   0 | 0 | 0 | 0 | 0
   5 | 0 | 0 | 0 | 0
   queue | ucast drop pkts | ucast drop bytes | mcast drop pkts | mcast drop bytes
   ----------------------------------------------------------------------------------
   0 | 0 | 0 | 0 | 0
   ```

   With `qos-174` on the port and an 8 Mbit/s EF stream followed by an
   8 Mbit/s unmarked stream, predict which counters grow. **Answer:** queue 5's
   unicast packets and bytes during the EF stream; queue 0's unicast counters
   and its unicast drop counters during the unmarked stream, because queue 0 is
   limited to 2,048 kbps.
2. A port uses `voice-qos`. A phone sends a tagged frame with CoS 0 carrying
   an IP packet with DSCP 26. Predict the queue. **Answer:** queue 2: `voice-qos`
   trusts both maps, DSCP wins when present (p. 285), and `voice-dscp` maps 26
   to queue 2. With trust of dot1p alone, CoS 0 would give queue 4.
3. An FS-124F has `voice-dot1p` and `voice-dscp` from an earlier
   configuration, and an administrator adds and applies `dscp-174`. Predict.
   **Answer:** feature matrix note 18: the FS-1xxF supports a single QoS map,
   and the first configured map is used, so the port can keep classifying with
   the older map; step 8's trap queue is the way to see it.

**Expected result:** Track 1: the predefined objects, the ports' QoS policy,
and the switch's maps are recorded; with `qos-174` on both ports, unmarked
traffic was limited to about 2 Mbit/s while EF and CS3 passed at about
8 Mbit/s (or the note 18 result is recorded on S1 and S2); on S3 queue 5 and
queue 0 counters moved as predicted. Track 2: the objects exist and the
predictions are answered.

**Negative test:** (a) Trust dot1p instead of DSCP and repeat the EF run:

```text
FGT # config switch-controller qos qos-policy
edit "qos-174"
unset trust-ip-dscp-map
set trust-dot1p-map "dot1p-174"
next
end
```

Predict and observe: EF now arrives at about 2 Mbit/s. Endpoint B's frames are
untagged, so they carry no CoS; with dot1p trusted and DSCP not, the switch uses
the port's default CoS (0), and `dot1p-174` sends priority 0 to queue 0
(Administration Guide, p. 368). (b) Except on the models listed in the platform
notes, set `default-cos 5` in `qos-174` and repeat the unmarked run: predict
about 8 Mbit/s, because every untagged frame on `port2` now counts as CoS 5,
which `dot1p-174` maps to queue 5. Record both results. Track 2: prediction 2
is the negative test.

**Rollback:** Stop the `iperf` server with Ctrl+C. Put the ports back to the
values recorded in step 1 (shown here as the 7.6.0 default), then delete the
objects in dependency order:

```text
FGT # config switch-controller managed-switch
edit <SWITCH_SN>
config ports
edit "port1"
set qos-policy "default"
next
edit "port2"
set qos-policy "default"
set vlan "fsw-iot"
next
end
next
end
FGT # config switch-controller qos qos-policy
delete "qos-174"
end
FGT # config switch-controller qos queue-policy
delete "queue-174"
end
FGT # config switch-controller qos ip-dscp-map
delete "dscp-174"
end
FGT # config switch-controller qos dot1p-map
delete "dot1p-174"
end
```

```bash
# endpoint B
sudo ip addr del 10.174.41.20/24 dev <IFACE_B>
ping -c 3 10.174.43.1
# endpoint A
sudo apt remove -y iperf
```

Confirm that `show switch-controller qos qos-policy` lists only the objects
recorded in step 1, that `show switch interface port1` on the switch shows the
trust and QoS settings recorded in step 2, and that `show
switch-controller managed-switch <SWITCH_SN>` shows `port2` native `fsw-iot`
with `quarantine` in its lists.

**Lab verified by:** *pending*

### Lab 10.3 — Switch ports dedicated to a tenant VDOM

**Objective:** Record your controller's VDOM capacity, switch it to
multi-VDOM mode, create the tenant VDOM `tenant-174`, move `fsw-tenant` into it
and make it the tenant's default virtual-switch VLAN, export `port2` to the
tenant and see the virtual switch from the tenant's side, let the tenant claim
switch `port4` from a virtual port pool, and show that the tenant's network is
isolated from `root`.

**Platform notes:** Hands-on on C1 and C3 when the license allows a second
traffic VDOM (step 3 is the test), with S1, S2, or S3 (on S3, `FSW-A`):
multi-tenancy has no matrix row. On C2, steps 1 to 3 are an optional go/no-go
that is expected to fail (one traffic VDOM on the evaluation, Volume CIX
Chapter 07); after a NO-GO the rest of the lab is read-and-predict, and step 3
says how to leave multi-VDOM mode. Multi-VDOM mode changes the whole
controller's CLI and logs administrators out (record what happens); do this lab
in a maintenance window if the controller serves anything else (on C3, FGT-1
still carries VLAN 202). No policy, route, or interface is added. Track 2: on
a C1 or C3 controller without a switch, steps 1 to 5 and step 10's pool run
live, and the export steps run on the stand-in only with Lab 2.2's third
outcome; on FGT-1 alone, steps 1 to 3 are the same go/no-go; the switch and
endpoint steps are read-and-predict.

**Track 1, Part A — capacity and VDOM mode:**

1. Back up and read the starting state:

   ```text
   FGT # execute backup config tftp fgt-pre-10-3-174.conf 10.30.99.50
   FGT # get system status
   FGT # show system interface fsw-tenant
   ```

   Record the VDOM lines of `get system status` (whether VDOMs are enabled and
   how many your license allows). Confirm that `fsw-tenant` is in `root` with
   `10.174.45.1/24`, `allowaccess ping`, parent `port3` (C2), `port4` (C3), or
   `<FL_PORT>` (C1), and VLAN ID 1745, and that nothing refers to it.

2. Enable multi-VDOM mode:

   ```text
   FGT # config system global
   set vdom-mode multi-vdom
   end
   ```

   Predict what happens to your session. **Answer:** the local references do
   not say; expect to be logged out, and record it. Log in again and run `get
   system status` (record the current VDOM and the VDOM lines). Everything that
   existed is now in `root`.

3. Create the tenant VDOM and read both VDOMs' type:

   ```text
   FGT # config vdom
   edit tenant-174
   next
   end
   FGT # config vdom
   edit root
   FGT # get system settings
   FGT # end
   ```

   Record whether `tenant-174` was created and `root`'s `vdom-type`
   (`traffic`, the 7.6.0 default). **GO/NO-GO:** if FortiOS refuses the new
   VDOM (on C2, Volume CIX recorded `Could not create VD, all VD licenses have
   been used`), record **multi-tenancy: NO-GO** with the message, leave
   multi-VDOM mode now, and continue with Track 2: read-and-predict:

   ```text
   FGT # config global
   FGT # config system global
   set vdom-mode no-vdom
   end
   FGT # end
   ```

   Do not set `root` to an admin VDOM to make room: `root` carries FortiLink,
   the lab VLANs, and P1 and P2, and an admin VDOM does not pass traffic.

**Track 1, Part B — the tenant VLAN:**

4. Move `fsw-tenant` into the tenant VDOM. Its parent stays the FortiLink
   interface in `root`, as in the guide's example (p. 124):

   ```text
   FGT # config global
   FGT # config system interface
   edit "fsw-tenant"
   set vdom "tenant-174"
   next
   end
   FGT # show system interface fsw-tenant
   FGT # end
   ```

   Predict. **Answer:** accepted, because nothing refers to the interface; it
   keeps its address, VLAN ID, and parent. If FortiOS refuses the move, record
   the message and recreate the interface in the tenant instead (delete it, then
   `edit "fsw-tenant"` with `set vdom "tenant-174"` and Chapter 04's other
   settings); the interface count does not change.

5. Make it the tenant's default virtual-switch VLAN:

   ```text
   FGT # config vdom
   edit tenant-174
   FGT # config switch-controller global
   set default-virtual-switch-vlan "fsw-tenant"
   end
   FGT # get switch-controller global
   FGT # end
   ```

**Track 1, Part C — export `port2`:**

6. In `root`, record `port2` and export it:

   ```text
   FGT # config vdom
   edit root
   FGT # show switch-controller managed-switch <SWITCH_SN>
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port2"
   set export-to "tenant-174"
   next
   end
   next
   end
   FGT # show switch-controller managed-switch <SWITCH_SN>
   FGT # end
   ```

   Record `port2`'s `vlan`, `allowed-vlans`, `untagged-vlans`, `stp-bpdu-guard`,
   and `stp-bpdu-guard-timeout` before the export. Predict what the `root` view
   of `port2` shows after it. **Answer:** `set export-to "tenant-174"` and few
   other lines, as in the guide's `root` view of an exported port (p. 125);
   record which of the recorded settings are still shown.

7. Look from the tenant's side:

   ```text
   FGT # config vdom
   edit tenant-174
   FGT # show switch-controller managed-switch
   FGT # execute switch-controller get-conn-status
   FGT # end
   ```

   Predict the `show`. **Answer:** one entry, `<SWITCH_SN>`, with `set type
   virtual`, `set owner-vdom "root"`, and only `port2`, whose `vlan` is
   `fsw-tenant`, the default virtual-switch VLAN (pp. 125–126). Record what
   `get-conn-status` prints in the tenant: the guide says switches are not
   visible in non-root VDOMs (p. 127) but prints no tenant output.

8. Check the switch and endpoint B:

   ```text
   FSW # show switch interface port2
   ```

   ```bash
   # endpoint B
   sudo ip addr add 10.174.45.20/24 dev <IFACE_B>
   ping -c 3 10.174.45.1
   ping -c 3 10.174.43.1
   ```

   The switch shows `port2` with native VLAN 1745. The ping to `10.174.45.1`
   (the tenant VDOM's interface) works and the ping to `10.174.43.1` fails:
   `port2`'s untagged traffic is now in `fsw-tenant`.

9. Let the tenant set LLDP on its port (FortiOS 6.4.3 and later, p. 176):

   ```text
   FGT # config vdom
   edit tenant-174
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port2"
   set lldp-status rx-only
   next
   end
   next
   end
   FGT # end
   FSW # show switch physical-port port2
   ```

   Record whether the switch shows `lldp-status rx-only` on `port2`.

**Track 1, Part D — a virtual port pool:**

10. In `root`, create the pool and put switch `port4` in it:

    ```text
    FGT # config vdom
    edit root
    FGT # config switch-controller virtual-port-pool
    edit "pool-174"
    set description "Lab 10.3 tenant pool"
    next
    end
    FGT # config switch-controller managed-switch
    edit <SWITCH_SN>
    config ports
    edit "port4"
    set export-to-pool "pool-174"
    next
    end
    next
    end
    FGT # execute switch-controller virtual-port-pool show
    FGT # end
    ```

    Predict whether the tenant already sees `port4`. **Answer:** no: a pooled
    port is pre-assigned but not exported until the tenant claims it (p. 125).

11. Claim it from the tenant and read both sides:

    ```text
    FGT # config vdom
    edit tenant-174
    FGT # execute switch-controller virtual-port-pool request <SWITCH_SN> port4
    FGT # show switch-controller managed-switch
    FGT # execute switch-controller virtual-port-pool show-by-pool pool-174
    FGT # end
    FGT # config vdom
    edit root
    FGT # show switch-controller managed-switch <SWITCH_SN>
    FGT # end
    ```

    The tenant now lists `port2` and `port4`, both with `vlan "fsw-tenant"`;
    the `root` view of `port4` shows `set export-to-pool "pool-174"` and `set
    export-to "tenant-174"` (p. 126). Record the `show-by-pool` output.

**Track 2:** On a C1 or C3 controller without a switch, run steps 1 to 5 and
step 10's pool block (without the `port4` part). If Lab 2.2's third outcome
applies, run step 6's export and step 10's `port4` block against
`S248EPTF18000000` and read step 7's tenant view. On FGT-1 alone, steps 1 to 3
are the go/no-go; after a NO-GO, leave multi-VDOM mode as step 3 shows. Skip the
switch and endpoint steps.

**Track 2: read-and-predict.**

1. The guide's tenant view of an exported switch (p. 125), trimmed:

   ```text
   config switch-controller managed-switch
   edit "S548DF4K15000276"
   set type virtual
   set owner-vdom "root"
   config ports
   edit "port10"
   set vlan "bbb-vlan99"
   next
   end
   next
   end
   ```

   Predict what `type virtual` and `owner-vdom "root"` tell the tenant
   administrator. **Answer:** the tenant does not manage the switch; `root`,
   which holds the FortiLink interface, owns it, and the tenant sees a virtual
   switch made of the ports exported to it, with the tenant's default VLAN as
   their native VLAN, "even though there is no FortiLink interface" in the
   tenant VDOM (p. 125).
2. A tenant administrator asks for DHCP snooping on an exported port. Predict.
   **Answer:** not supported: shared ports do not support DHCP snooping
   (p. 126), even though the guide's own example enables snooping on the
   tenant VLAN (p. 124); use other controls.
3. Which of these can the tenant apply to its exported port: a port security
   (802.1X) policy, a QoS egress queue policy, DHCP snooping, a MAC learning
   limit? **Answer:** all but DHCP snooping (p. 124 lists the first, second,
   and fourth as supported on shared ports from FortiOS 6.2.0).

**Expected result:** Track 1: the VDOM capacity is recorded; in multi-VDOM mode
`tenant-174` exists with `fsw-tenant` in it as its default virtual-switch VLAN;
exporting `port2` gave the tenant a virtual switch with `port2` in VLAN 1745,
and endpoint B reached `10.174.45.1`; the tenant set LLDP on its port and
claimed `port4` from `pool-174`. On C2 the NO-GO and its message are recorded.
Track 2: the objects your controller allows exist and the predictions are
answered.

**Negative test:** Try to reach `root`'s network from the tenant. On endpoint
B, add a route through the tenant VDOM and ping endpoint A:

```bash
# endpoint B
sudo ip route add 10.174.41.0/24 via 10.174.45.1
ping -c 3 <LEASE_A>
```

```text
FGT # config vdom
edit tenant-174
FGT # get router info routing-table all
FGT # end
```

Predict and observe: the ping fails. The tenant VDOM's routing table holds only
its connected network `10.174.45.0/24`; it has no route, interface, or policy
toward `root`, and VDOMs exchange traffic only through an inter-VDOM link and
policies, which this lab does not build. Delete the route afterwards (`sudo ip
route del 10.174.41.0/24`). Track 2: prediction 1 is the negative test.

**Rollback:** Undo in the reverse order: the tenant's settings, then the
exports and the pool in `root`, then the interface, the VDOM, and VDOM mode.
First the tenant:

```text
FGT # config vdom
edit tenant-174
FGT # config switch-controller managed-switch
edit <SWITCH_SN>
config ports
edit "port2"
set lldp-status tx-rx
next
end
next
end
FGT # config switch-controller global
unset default-virtual-switch-vlan
end
FGT # end
```

Then `root`, putting `port2` back to the values recorded in step 6 (shown here
as Chapter 09's state):

```text
FGT # config vdom
edit root
FGT # config switch-controller managed-switch
edit <SWITCH_SN>
config ports
edit "port2"
set export-to "root"
set vlan "fsw-iot"
next
edit "port4"
unset export-to-pool
set export-to "root"
next
end
next
end
FGT # config switch-controller virtual-port-pool
delete "pool-174"
end
FGT # show switch-controller managed-switch <SWITCH_SN>
FGT # end
```

Compare `port2` with step 6's record. If `quarantine` is missing from its
lists, `append allowed-vlans "quarantine"` and `append untagged-vlans
"quarantine"`; if BPDU guard is missing, `set stp-bpdu-guard enable` and `set
stp-bpdu-guard-timeout 5`. On endpoint B:

```bash
# endpoint B
sudo ip addr del 10.174.45.20/24 dev <IFACE_B>
ping -c 3 10.174.43.1
```

**Shortcut to Lab 10.4:** if you go straight on to Lab 10.4, stop here and keep
multi-VDOM mode, `tenant-174`, and `fsw-tenant` in it. Otherwise finish the
teardown in global context:

```text
FGT # config global
FGT # config system interface
edit "fsw-tenant"
set vdom "root"
next
end
FGT # config system vdom
delete "tenant-174"
end
FGT # config system global
set vdom-mode no-vdom
end
FGT # end
```

If FortiOS refuses the VDOM deletion or the mode change, or if anything else
differs from the starting state, restore the backup (`execute restore config
tftp fgt-pre-10-3-174.conf 10.30.99.50`, under `config global` while in
multi-VDOM mode; the controller reboots). Confirm with `get system status` that
VDOMs are disabled, with `show system interface fsw-tenant` that it is back in
`root` with its Chapter 04 settings, and with `show firewall policy` that P1 and
P2 are unchanged.

**Lab verified by:** *pending*

### Lab 10.4 — VLANs from two VDOMs on one switch port

**Objective:** With `fsw-tenant` in the tenant VDOM, let the `root`
administrator put that tenant VLAN on `port2` next to `root`'s own `fsw-iot`,
first tagged and then as the native VLAN, and show that one port carries the
VLANs of two VDOMs while the tenant sees no switch at all.

**Platform notes:** Hands-on on C1 and C3 when Lab 10.3's step 3 was a GO, with
S1, S2, or S3 (on S3, `FSW-A`). On C2 (and after any multi-tenancy NO-GO) the
lab is read-and-predict. No policy, route, or interface is added. Step 6 (the
GUI check) is optional. Track 2: on a C1 or C3 controller without a switch, the
VDOM steps run live, and the port steps run on the stand-in only with Lab 2.2's
third outcome; the switch and endpoint steps are read-and-predict.

**Track 1:**

1. If you kept the VDOM state from Lab 10.3 (its shortcut), skip to step 3.
   Otherwise back up and repeat Lab 10.3's steps 2 to 4 (multi-VDOM mode, the
   VDOM `tenant-174`, and `fsw-tenant` moved into it):

   ```text
   FGT # execute backup config tftp fgt-pre-10-4-174.conf 10.30.99.50
   ```

2. Check that `fsw-tenant` is in the tenant VDOM:

   ```text
   FGT # config global
   FGT # show system interface fsw-tenant
   FGT # end
   ```

3. In `root`, record `port2` as `<PORT2_ALLOWED>` (its `allowed-vlans`) and its
   `vlan` and `untagged-vlans`, then add the tenant VLAN as a tagged VLAN:

   ```text
   FGT # config vdom
   edit root
   FGT # show switch-controller managed-switch <SWITCH_SN>
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port2"
   append allowed-vlans "fsw-tenant"
   next
   end
   next
   end
   FGT # end
   ```

   Predict whether `root` may name a VLAN of another VDOM on its port.
   **Answer:** yes, from the CLI: in this model the controlling VDOM's
   administrator assigns all ports and VLANs (p. 126).

4. Use both VLANs from endpoint B:

   ```text
   FSW # show switch interface port2
   ```

   ```bash
   # endpoint B
   sudo ip link add link <IFACE_B> name <IFACE_B>.1745 type vlan id 1745
   sudo ip addr add 10.174.45.20/24 dev <IFACE_B>.1745
   sudo ip link set <IFACE_B>.1745 up
   ping -c 3 -I <IFACE_B>.1745 10.174.45.1
   ping -c 3 10.174.43.1
   ```

   The switch shows `port2` with native VLAN 1743 and 1745 allowed. Both pings
   work: tagged 1745 frames reach the tenant VDOM's `fsw-tenant`, and untagged
   frames reach `root`'s `fsw-iot`, over one port.

5. Make the tenant VLAN the native VLAN, from the CLI:

   ```text
   FGT # config vdom
   edit root
   FGT # config switch-controller managed-switch
   edit <SWITCH_SN>
   config ports
   edit "port2"
   set vlan "fsw-tenant"
   next
   end
   next
   end
   FGT # end
   ```

   ```bash
   # endpoint B
   sudo ip link delete <IFACE_B>.1745
   sudo ip addr add 10.174.45.20/24 dev <IFACE_B>
   ping -c 3 10.174.45.1
   ping -c 3 10.174.43.1
   ```

   Now the untagged ping to `10.174.45.1` works and the ping to `10.174.43.1`
   fails: `port2`'s native VLAN belongs to the tenant VDOM, although `root`
   still controls the port.

6. Optional, the GUI. In `root`, open **WiFi & Switch Controller > FortiSwitch
   Ports** and look at `port2`. Record how the native VLAN `fsw-tenant` is shown
   and whether the GUI lets you select a VLAN of another VDOM as the native VLAN;
   the guide says it cannot (p. 126). Do not save a change in the GUI.

**Track 2:** On a C1 or C3 controller without a switch, set up the VDOM state
(step 1), and if Lab 2.2's third outcome applies, run steps 3 and 5's
controller blocks against `S248EPTF18000000`. Skip the switch and endpoint
steps.

**Track 2: read-and-predict.**

1. In this model, the tenant VDOM's administrator runs `show
   switch-controller managed-switch`. Predict. **Answer:** nothing: no port is
   exported, so the tenant has no virtual switch; "FortiSwitch units are not
   visible in non-root VDOMs", and there is no administrative separation
   (pp. 126–127). The negative test checks this live.
2. A managed service provider gives each customer its own VLAN range in its own
   VDOM, carried in a service VLAN on one port. Predict which feature that is,
   where the service VLAN must be defined, and whether S1 and S2 can do it.
   **Answer:** QinQ (VLAN stacking); the service VLAN must be in the VDOM of the
   FortiLink interface (p. 128); the 1xxE/1xxF column is a dash, so S1 and S2
   cannot, while the 200 Series (S3) is a chain. STP, DHCP snooping, and IGMP
   snooping are not supported with QinQ (p. 127).
3. A tenant VLAN is the native VLAN of a shared port, and the root administrator
   enables DHCP snooping for it. Predict. **Answer:** the guide says shared ports
   do not support DHCP snooping (p. 126); do not rely on it there, and record
   what happens if you test it.

**Expected result:** Track 1: `port2` carried `root`'s `fsw-iot` untagged and
the tenant's `fsw-tenant` tagged at the same time, endpoint B reached both
gateways, and after the change from the CLI `fsw-tenant` was the native VLAN.
Track 2: the VDOM state your controller allows exists and the predictions are
answered.

**Negative test:** Look for the switch from the tenant VDOM:

```text
FGT # config vdom
edit tenant-174
FGT # show switch-controller managed-switch
FGT # execute switch-controller get-conn-status
FGT # end
```

Predict and observe: the tenant VDOM shows no managed switch, although its VLAN
is the native VLAN of `port2`: in the shared-VLAN model the tenant has traffic
separation only, and only `root` can configure the port (pp. 126–127). Record
what `get-conn-status` prints. Track 2: prediction 1 is the negative test.

**Rollback:** Put `port2` back in `root`, using the list recorded in step 3,
which includes `quarantine`:

```text
FGT # config vdom
edit root
FGT # config switch-controller managed-switch
edit <SWITCH_SN>
config ports
edit "port2"
set vlan "fsw-iot"
set allowed-vlans <PORT2_ALLOWED>
next
end
next
end
FGT # show switch-controller managed-switch <SWITCH_SN>
FGT # end
```

```bash
# endpoint B
sudo ip addr del 10.174.45.20/24 dev <IFACE_B>
ping -c 3 10.174.43.1
```

Then finish the teardown in global context, as at the end of Lab 10.3's
rollback:

```text
FGT # config global
FGT # config system interface
edit "fsw-tenant"
set vdom "root"
next
end
FGT # config system vdom
delete "tenant-174"
end
FGT # config system global
set vdom-mode no-vdom
end
FGT # end
```

Nothing else is left to undo: the shortcut comes after Lab 10.3's tenant and
`root` rollback blocks, and if you started this lab at step 1, nothing was
exported. If anything differs, restore `fgt-pre-10-4-174.conf` (or
`fgt-pre-10-3-174.conf` if you came from the shortcut). Confirm with `get
system status` that VDOMs are disabled, that `port2` is native `fsw-iot` with
`<PORT2_ALLOWED>` and BPDU guard, and that endpoint B reaches `10.174.43.1`.

**Lab verified by:** *pending*

## Lab Verification

Complete this sign-off once Labs 10.1 to 10.4 have been run end to end,
including each negative test. Until then, the labs are unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

An LLDP profile decides what a managed port advertises, and FortiOS gives every
managed port `default-auto-isl`, which sends no LLDP-MED; a phone port needs
its own profile with `auto-isl disable`, `med-tlvs network-policy`, and enabled
voice policies. A network policy is sent only while its VLAN is on the port,
tagged unless it is native or untagged there, and `assign-vlan` puts the voice
VLAN on the port for you. FortiSwitch QoS classifies on ingress by trusting
dot1p or DSCP maps, queues in eight egress queues scheduled strictly,
round-robin, or by weight, and can police each queue; the FortiOS queue policy
is the switch's QoS policy, and the FortiOS QoS policy is the port's bundle of
trust maps and queue policy. The FS-1xx models use one QoS map and have no
queue counters, so rate limits show the queue there. Multi-tenancy either
exports ports to a tenant VDOM, which then sees a virtual switch with its own
default VLAN, or lets the controlling VDOM put VLANs of several VDOMs on one
port without administrative separation; shared ports lose DHCP snooping, and the
FortiGate-VM evaluation cannot add a tenant traffic VDOM next to the lab's
`root`. The chapter ends with every object removed and the controller back in
single-VDOM mode.

- [ ] I recorded the LLDP settings, the profiles, and `port1`'s default
      profile, and I can say why a phone learns nothing from it.
- [ ] Endpoint A learned a tagged voice policy for VLAN 1742 from
      `lldp-med-174` and used VLAN 1742 on `port1`, and lost it when
      `assign-vlan` was disabled.
- [ ] I can map FortiOS `dot1p-map`, `ip-dscp-map`, `queue-policy`, and
      `qos-policy` to the switch's objects.
- [ ] With `qos-174`, unmarked traffic was limited and EF and CS3 traffic was
      not; I recorded which map S1 or S2 used, or read queue counters on S3.
- [ ] Trusting dot1p instead of DSCP sent untagged EF traffic to queue 0.
- [ ] I recorded my controller's VDOM capacity and the multi-tenancy GO or
      NO-GO.
- [ ] On a GO, the tenant saw a virtual switch with `port2` and the claimed
      `port4` in `fsw-tenant`, and `port2` later carried VLANs of both VDOMs.
- [ ] Every object from Labs 10.1 to 10.4 is removed, the controller is in
      single-VDOM mode, `fsw-tenant` is back in `root`, and `port1` and `port2`
      are as Chapter 09 left them.
